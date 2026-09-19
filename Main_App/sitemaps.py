from django.contrib.sitemaps import Sitemap
from seo.models import LocationSEO
from seo.seo_generator import site_url, PAGE_TYPE_URL_INFO
from Admin_App.models import (
    RentalResidentialProperty,
    CommercialRentalProperty,
    PGColivingProperty,
    ResaleResidentialProperty,
    CommercialResaleProperty,
                  # NEW: was missing entirely
    IndustrialResaleProperty,
    AgriculturalResaleProperty,
    ResidentialPlotResaleProperty,
    CommercialPlotResaleProperty,
    IndustrialPlotResaleProperty,
    AgriculturalPlotResaleProperty,
    Blog,                          # NEW
    Service,                       # NEW
)

# Status values that should NEVER be in the sitemap. Adjust these strings
# to match whatever your listing_status/approval_status fields actually
# store (check Admin_App choices) — this is a guess based on common
# naming, verify before deploying.
EXCLUDED_STATUSES = {"pending", "rejected", "draft", "inactive", "expired"}


class BasePropertySitemap(Sitemap):
    changefreq = "daily"
    # NOTE: protocol/domain below are only used as a fallback for the
    # rare not-yet-backfilled row (see location()). Every normal row
    # returns an already-absolute https://... URL read from
    # LocationSEO.canonical_url, and Django's sitemap framework uses
    # absolute URLs exactly as given -- this is also what fixes the
    # "https://example.com/..." placeholder domain you may have seen
    # before: that came from django.contrib.sites' default Site record
    # (SITE_ID=1, domain defaults to "example.com" until changed in
    # /admin/sites/site/), which only gets used for *relative* paths.
    protocol = "https"
    model = None
    page_type = None       # NEW: matches the exact string used in signals.py / seo_generator.py
    pk_field = "id"        # NEW: overridable — PlotSaleProperty uses plot_property_id, not id

    def items(self):
        qs = self.model.objects.all()

        if hasattr(self.model, "is_deleted"):
            qs = qs.filter(is_deleted=False)
        if hasattr(self.model, "is_duplicate"):
            qs = qs.filter(is_duplicate=False)

        # NEW: exclude anything not actually live/approved yet. Also
        # catches Blog's own status field ("draft" vs "published") --
        # previously unchecked, so draft blog posts could end up in
        # the sitemap even though they're not meant to be public yet.
        results = []
        for obj in qs:
            status = str(getattr(obj, "listing_status", "") or "").strip().lower()
            approval = str(getattr(obj, "approval_status", "") or "").strip().lower()
            blog_status = str(getattr(obj, "status", "") or "").strip().lower()
            if status in EXCLUDED_STATUSES or approval in EXCLUDED_STATUSES:
                continue
            if blog_status == "draft":
                continue
            results.append(obj)
        return results

    def location(self, obj):
        # FIXED: this used to independently rebuild "/listing/<page_type>/<id>/"
        # -- a URL that matches NO route in Main_App/urls.py and 404s on
        # every click. It now reads the real canonical_url straight off
        # this object's own LocationSEO record (the exact same field
        # <link rel="canonical"> uses on the live page), so the sitemap
        # and the canonical tag can never say two different things again.
        pk_value = str(getattr(obj, self.pk_field))
        seo_row = (
            LocationSEO.objects
            .filter(pagetype=self.page_type, object_id=pk_value)
            .exclude(canonical_url__isnull=True)
            .exclude(canonical_url="")
            .first()
        )
        if seo_row:
            return seo_row.canonical_url

        # Fallback ONLY for rows that haven't been backfilled with a
        # LocationSEO record yet (run generate_auto_seo to close this
        # gap) -- still builds a real, resolvable route rather than the
        # old guaranteed-broken 2-segment shape.
        listing_type, category = PAGE_TYPE_URL_INFO.get(self.page_type, (None, None))
        if listing_type:
            return f"{site_url()}/listing/{listing_type}/{category}/{pk_value}/"
        return f"{site_url()}/listing/{self.page_type}/{pk_value}/"

    def lastmod(self, obj):
        return getattr(obj, "updated_at", None) or getattr(obj, "created_at", None)


def make_sitemap(model, page_type, pk_field="id", changefreq="daily"):
    return type(
        f"Sitemap_{page_type}",
        (BasePropertySitemap,),
        {"model": model, "page_type": page_type, "pk_field": pk_field, "changefreq": changefreq},
    )


# =========================================================
# NEW: LOCATION+CATEGORY + OWNER-LISTING LANDING PAGES
#
# These two page types aren't 1:1 with a property model — they're
# generated lazily by landing_seo.py (generate_location_category_seo /
# generate_owner_listing_seo) the first time someone requests that
# URL, and stored as LocationSEO rows via update_or_create(). That
# LocationSEO row IS the eligibility-checked source of truth (it only
# gets created for city/locality combos that passed the
# MIN_ELIGIBLE_PROPERTIES check in landing_seo.py), so the sitemap
# reads directly from LocationSEO instead of re-deriving eligible
# combos a second time and risking drift between the two.
#
# NOTE: a landing page only gets a LocationSEO row (and therefore
# only appears in this sitemap) after it has been requested at least
# once. Pages nobody has ever visited yet won't show up here until
# the first hit creates the record — internal links (nearby-locality
# chips, owner cross-link band) are what get that first hit in
# practice, this sitemap then keeps it discoverable after that.
# canonical_url is already a full https:// URL (built by site_url()
# in landing_seo.py), so location() returns it as-is.
# =========================================================

class LocationCategorySitemap(Sitemap):
    changefreq = "daily"
    protocol = "https"

    def items(self):
        return (
            LocationSEO.objects
            .filter(pagetype="location_category", is_active=True, noindex=False)
            .exclude(canonical_url__isnull=True)
            .exclude(canonical_url="")
        )

    def location(self, obj):
        return obj.canonical_url


class OwnerListingSitemap(Sitemap):
    changefreq = "weekly"
    protocol = "https"

    def items(self):
        return (
            LocationSEO.objects
            .filter(pagetype="owner_listing", is_active=True, noindex=False)
            .exclude(canonical_url__isnull=True)
            .exclude(canonical_url="")
        )

    def location(self, obj):
        return obj.canonical_url


sitemaps = {
    "rental_residential": make_sitemap(RentalResidentialProperty, "rental_residential"),
    "commercial_rental": make_sitemap(CommercialRentalProperty, "commercial_rental"),
    "pg_coliving": make_sitemap(PGColivingProperty, "pg_coliving"),
    "resale_residential": make_sitemap(ResaleResidentialProperty, "resale_residential"),
    "commercial_resale": make_sitemap(CommercialResaleProperty, "commercial_resale"),

    # FIXED: PlotSaleProperty's PK is plot_property_id, not id — this
    # would have raised AttributeError with the old location() method.
    #"plot_sale": make_sitemap(PlotSaleProperty, "plot_sale", pk_field="plot_property_id"),

    "industrial_sale": make_sitemap(IndustrialResaleProperty, "industrial_sale"),
    "agriculture_sale": make_sitemap(AgriculturalResaleProperty, "agriculture_sale"),
    "residential_plot_resale": make_sitemap(ResidentialPlotResaleProperty, "residential_plot_resale"),
    "commercial_plot_resale": make_sitemap(CommercialPlotResaleProperty, "commercial_plot_resale"),
    "industrial_plot_resale": make_sitemap(IndustrialPlotResaleProperty, "industrial_plot_resale"),
    "agricultural_plot_resale": make_sitemap(AgriculturalPlotResaleProperty, "agricultural_plot_resale"),

    # NEW: Blog and Service now included
    "blog": make_sitemap(Blog, "blog", changefreq="weekly"),
    "service": make_sitemap(Service, "service", changefreq="monthly"),

    # NEW: location+category aggregation pages and owner-listing pages
    "location_category": LocationCategorySitemap,
    "owner_listing": OwnerListingSitemap,
}
