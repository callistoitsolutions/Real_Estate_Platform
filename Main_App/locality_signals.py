from django.db.models.signals import post_save
from django.apps import apps
from Main_App.models import LocalityInsight, LocalityPriceTrend

PROPERTY_MODEL_NAMES = [
    'RentalResidentialProperty', 'CommercialRentalProperty', 'PGColivingProperty',
    'ResaleResidentialProperty', 'CommercialResaleProperty', 'IndustrialResaleProperty',
    'AgriculturalResaleProperty', 'ResidentialPlotResaleProperty',
    'CommercialPlotResaleProperty', 'IndustrialPlotResaleProperty',
    'AgriculturalPlotResaleProperty',
]

APP_LABEL = 'Admin_App'   # this is where the property models actually live


def get_locality_fields(instance):
    city = getattr(instance, 'city', None)
    locality = (
        getattr(instance, 'locality', None) or
        getattr(instance, 'locality_area', None) or
        getattr(instance, 'plot_locality', None) or
        getattr(instance, 'village', None)
    )
    return city, locality



def get_instance_price(instance):
    per_unit = (
        getattr(instance, 'price_per_sqft', None) or
        getattr(instance, 'price_per_unit', None) or
        getattr(instance, 'plot_price_per_sqft', None)
    )
    if per_unit:
        return per_unit

    total_price = (
        getattr(instance, 'selling_price', None) or
        getattr(instance, 'plot_price', None)
    )
    area = (
        getattr(instance, 'builtup_area', None) or
        getattr(instance, 'land_area', None) or
        getattr(instance, 'plot_area', None) or
        getattr(instance, 'super_builtup_area', None)
    )
    if total_price and area:
        try:
            area_f = float(area)
            if area_f > 0:
                return float(total_price) / area_f
        except (TypeError, ValueError, ZeroDivisionError):
            return None

    return None


def sync_locality_price_trend(city, locality):
    prices = []
    for model_name in PROPERTY_MODEL_NAMES:
        try:
            model = apps.get_model(APP_LABEL, model_name)
        except LookupError:
            continue

        # skip models that don't have a 'city' field at all (e.g. agricultural/plot models using district/village)
        model_field_names = [f.name for f in model._meta.get_fields()]
        if 'city' not in model_field_names:
            continue

        for obj in model.objects.filter(city__iexact=city):
            _, loc = get_locality_fields(obj)
            if loc and loc.strip().lower() == locality.strip().lower():
                price = get_instance_price(obj)
                if price:
                    prices.append(price)

    if not prices:
        return

    avg_price = sum(prices) / len(prices)

    trend, _created = LocalityPriceTrend.objects.get_or_create(
        city=city, locality=locality,
        defaults={'avg_rate_per_sqft': avg_price}
    )
    trend.avg_rate_per_sqft = avg_price
    trend.save()


def sync_locality_insight_stub(city, locality):
    LocalityInsight.objects.get_or_create(
        city=city, locality=locality,
        defaults={'is_active': True}
    )


def locality_autocreate_receiver(sender, instance, **kwargs):
    city, locality = get_locality_fields(instance)
    if not city or not locality:
        return
    sync_locality_price_trend(city, locality)
    sync_locality_insight_stub(city, locality)


def connect_locality_signals():
    for model_name in PROPERTY_MODEL_NAMES:
        try:
            model = apps.get_model(APP_LABEL, model_name)
        except LookupError:
            continue
        post_save.connect(
            locality_autocreate_receiver,
            sender=model,
            dispatch_uid=f'locality_autocreate_{model_name}'
        )