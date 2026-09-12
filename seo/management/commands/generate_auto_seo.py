"""
generate_auto_seo
==================

Backfill command for the per-property SEO engine.

WHY THIS EXISTS
----------------
An SEO record (LocationSEO) is normally created by the post_save signal in
seo/signals.py, firing the moment a property is saved through the normal
form flow. Two situations leave a property with NO SEO record at all,
invisible to seo_generator.py, sitemaps.py and every landing page built on
top of it:

    1. Any property that existed in the database BEFORE the seo app's
       signals were wired up.
    2. Anything inserted with bulk_create() rather than .save() per row —
       bulk_create() does NOT fire post_save signals in Django. This is
       worth checking directly against the Excel bulk-import tooling
       already built for PG/co-living and rental residential.

This command loops over every property (+ blog/service/subscription) model,
calls create_dynamic_seo() for each row using the exact same page_type
strings signals.py uses, and reports a count. Safe to re-run any time --
create_dynamic_seo() uses update_or_create() internally, so running this
twice will not create duplicate LocationSEO records.

USAGE
-----
    python manage.py generate_auto_seo                # backfill everything
    python manage.py generate_auto_seo --dry-run       # count only, no writes
    python manage.py generate_auto_seo --model rental_residential
                                                        # backfill one type only
"""

from django.core.management.base import BaseCommand
from django.db import transaction

from seo.seo_generator import create_dynamic_seo

from Admin_App.models import (
    RentalResidentialProperty,
    CommercialRentalProperty,
    PGColivingProperty,
    ResaleResidentialProperty,
    CommercialResaleProperty,
    PlotSaleProperty,
    IndustrialResaleProperty,
    AgriculturalResaleProperty,
    ResidentialPlotResaleProperty,
    CommercialPlotResaleProperty,
    IndustrialPlotResaleProperty,
    AgriculturalPlotResaleProperty,
    Blog,
    Service,
    Subscription_Details,
)


# Same (model, page_type) pairs as seo/signals.py -- keep these two files
# in sync if a new property type is ever added.
MODEL_PAGE_TYPE_MAP = [
    (RentalResidentialProperty, "rental_residential"),
    (CommercialRentalProperty, "commercial_rental"),
    (PGColivingProperty, "pg_coliving"),
    (ResaleResidentialProperty, "resale_residential"),
    (CommercialResaleProperty, "commercial_resale"),
    (PlotSaleProperty, "plot_sale"),
    (IndustrialResaleProperty, "industrial_sale"),
    (AgriculturalResaleProperty, "agriculture_sale"),
    (ResidentialPlotResaleProperty, "residential_plot_resale"),
    (CommercialPlotResaleProperty, "commercial_plot_resale"),
    (IndustrialPlotResaleProperty, "industrial_plot_resale"),
    (AgriculturalPlotResaleProperty, "agricultural_plot_resale"),
    (Blog, "blog"),
    (Service, "service"),
    (Subscription_Details, "subscription"),
]


class Command(BaseCommand):
    help = (
        "Backfill LocationSEO records for every existing property/blog/service/"
        "subscription row -- covers rows created before the SEO signals were "
        "wired up, and rows inserted via bulk_create() (which skips post_save)."
    )

    def add_arguments(self, parser):
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="Report how many rows would be processed, without writing anything.",
        )
        parser.add_argument(
            "--model",
            type=str,
            default=None,
            help=(
                "Only backfill one page_type, e.g. --model rental_residential. "
                "Matches the second value in MODEL_PAGE_TYPE_MAP."
            ),
        )

    def handle(self, *args, **options):
        dry_run = options["dry_run"]
        only_page_type = options["model"]

        targets = MODEL_PAGE_TYPE_MAP
        if only_page_type:
            targets = [t for t in MODEL_PAGE_TYPE_MAP if t[1] == only_page_type]
            if not targets:
                valid = ", ".join(pt for _, pt in MODEL_PAGE_TYPE_MAP)
                self.stderr.write(self.style.ERROR(
                    f"Unknown --model '{only_page_type}'. Valid values: {valid}"
                ))
                return

        grand_total = 0
        grand_created_or_updated = 0
        grand_errors = 0

        for model_cls, page_type in targets:
            queryset = model_cls.objects.all()
            total = queryset.count()
            grand_total += total

            self.stdout.write(f"\n{model_cls.__name__} ({page_type}): {total} row(s)")

            if dry_run:
                continue

            done = 0
            errors = 0

            for instance in queryset.iterator():
                try:
                    with transaction.atomic():
                        create_dynamic_seo(instance, page_type)
                    done += 1
                except Exception as exc:
                    errors += 1
                    self.stderr.write(
                        self.style.WARNING(
                            f"  ! {model_cls.__name__} pk={instance.pk}: {exc}"
                        )
                    )

            grand_created_or_updated += done
            grand_errors += errors

            self.stdout.write(
                self.style.SUCCESS(f"  -> {done} SEO record(s) created/updated")
                + (f", {errors} error(s)" if errors else "")
            )

        self.stdout.write("\n" + "=" * 60)
        if dry_run:
            self.stdout.write(self.style.WARNING(
                f"DRY RUN -- {grand_total} row(s) would be processed. No SEO records written."
            ))
        else:
            self.stdout.write(self.style.SUCCESS(
                f"Done. {grand_created_or_updated}/{grand_total} SEO record(s) "
                f"created/updated across {len(targets)} model(s)."
            ))
            if grand_errors:
                self.stdout.write(self.style.ERROR(
                    f"{grand_errors} row(s) failed -- see warnings above."
                ))
