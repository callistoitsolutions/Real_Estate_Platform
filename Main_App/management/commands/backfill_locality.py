from django.core.management.base import BaseCommand
from django.apps import apps
from Main_App.locality_signals import (
    sync_locality_price_trend,
    sync_locality_insight_stub,
    get_locality_fields,
    PROPERTY_MODEL_NAMES,
)


class Command(BaseCommand):
    help = 'Backfill LocalityInsight and LocalityPriceTrend for existing properties'

    def handle(self, *args, **options):
        for model_name in PROPERTY_MODEL_NAMES:
            model = apps.get_model('Admin_App', model_name)
            count = 0
            for obj in model.objects.all():
                city, locality = get_locality_fields(obj)
                if city and locality:
                    sync_locality_price_trend(city, locality)
                    sync_locality_insight_stub(city, locality)
                    count += 1
            self.stdout.write(
                self.style.SUCCESS(f'{model_name}: processed {count} properties')
            )