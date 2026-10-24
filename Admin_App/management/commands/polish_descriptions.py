from django.core.management.base import BaseCommand
from Admin_App.models import (
    RentalResidentialProperty, CommercialRentalProperty, PGColivingProperty,
    ResaleResidentialProperty, CommercialResaleProperty, IndustrialResaleProperty,
    AgriculturalResaleProperty, ResidentialPlotResaleProperty,
    CommercialPlotResaleProperty, IndustrialPlotResaleProperty,
    AgriculturalPlotResaleProperty,
)

MODELS = [
    RentalResidentialProperty, CommercialRentalProperty, PGColivingProperty,
    ResaleResidentialProperty, CommercialResaleProperty, IndustrialResaleProperty,
    AgriculturalResaleProperty, ResidentialPlotResaleProperty,
    CommercialPlotResaleProperty, IndustrialPlotResaleProperty,
    AgriculturalPlotResaleProperty,
]

class Command(BaseCommand):
    help = "Polish user_description on every existing property and regenerate auto descriptions/FAQs."

    def handle(self, *args, **options):
        grand_total = 0
        for Model in MODELS:
            qs = Model.objects.all()
            count = qs.count()
            grand_total += count
            self.stdout.write(f"{Model.__name__}: {count} rows")
            for obj in qs.iterator():
                obj.polish_user_description()
                obj.generate_auto_descriptions()
                obj.generate_auto_faqs()
                obj.save()
        self.stdout.write(self.style.SUCCESS(f"Done. {grand_total} rows processed."))