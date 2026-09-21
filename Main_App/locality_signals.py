import logging
import math
from functools import reduce
from operator import or_

from django.apps import apps
from django.db import transaction
from django.db.models import FloatField, Q
from django.db.models.functions import Cast
from django.db.models.signals import post_save

from Main_App.models import LocalityInsight, LocalityPriceTrend

logger = logging.getLogger(__name__)

APP_LABEL = 'Admin_App'   # this is where the property models actually live

PROPERTY_MODEL_NAMES = [
    'RentalResidentialProperty', 'CommercialRentalProperty', 'PGColivingProperty',
    'ResaleResidentialProperty', 'CommercialResaleProperty', 'IndustrialResaleProperty',
    'AgriculturalResaleProperty', 'ResidentialPlotResaleProperty',
    'CommercialPlotResaleProperty', 'IndustrialPlotResaleProperty',
    'AgriculturalPlotResaleProperty',
]

# These models measure land in acres / hectares, so their rate is NOT "per sq.ft".
# They still create locality entries, but they are left out of the avg_rate_per_sqft calculation.
EXCLUDED_FROM_PRICE_TREND = {
    'AgriculturalResaleProperty',
    'AgriculturalPlotResaleProperty',
}

# IndustrialPlotResaleProperty stores plot_area in sq.m, so its rate is per sq.m.
# Dividing by 10.7639 converts it to a per sq.ft rate. Remove this line if you don't want the conversion.
RATE_DIVISOR = {
    'IndustrialPlotResaleProperty': 10.7639,
}

# Columns we read for the price calculation (only those that exist on the model are used)
PRICE_FIELDS = [
    'price_per_sqft', 'price_per_unit', 'plot_price_per_sqft',
    'selling_price', 'plot_price',
    'builtup_area', 'land_area', 'plot_area', 'super_builtup_area',
]

# Possible locality columns (a model can have more than one)
LOCALITY_FIELDS = ('locality', 'locality_area', 'plot_locality', 'village')

# Sanity limits for a rate per sq.ft (rupees). Anything outside is treated as bad data and ignored.
MIN_RATE = 1
MAX_RATE = 500000

BAD_TEXT = {'undefined', 'null', 'none', 'nan'}


# ─────────────────────────────────────────────────────────────
# Helpers
# ─────────────────────────────────────────────────────────────
def _clean_text(value):
    """Return a stripped string, or '' for None / 'undefined' / 'null' / 'nan'."""
    if value is None:
        return ''
    s = str(value).strip()
    return '' if s.lower() in BAD_TEXT else s


def _to_float(value):
    """Safe float conversion. Returns None for empty, invalid, NaN or infinite values."""
    if value in (None, ''):
        return None
    try:
        f = float(value)
    except (TypeError, ValueError):
        return None
    return f if math.isfinite(f) else None


def get_locality_fields(instance):
    city = _clean_text(getattr(instance, 'city', None))
    locality = ''
    for name in LOCALITY_FIELDS:
        locality = _clean_text(getattr(instance, name, None))
        if locality:
            break
    return city, locality


def _rate_from_values(values):
    """
    values: dict of field_name -> float/None.
    Uses the stored per-sqft rate when present, otherwise total price / area.
    Always returns a float or None.
    """
    per_unit = (
        values.get('price_per_sqft') or
        values.get('price_per_unit') or
        values.get('plot_price_per_sqft')
    )
    if per_unit:
        return per_unit

    total_price = values.get('selling_price') or values.get('plot_price')
    area = (
        values.get('builtup_area') or
        values.get('land_area') or
        values.get('plot_area') or
        values.get('super_builtup_area')
    )
    if total_price and area and area > 0:
        return total_price / area
    return None


def get_instance_price(instance):
    """Kept for compatibility: rate for a single model instance (float or None)."""
    values = {name: _to_float(getattr(instance, name, None)) for name in PRICE_FIELDS}
    return _rate_from_values(values)


# ─────────────────────────────────────────────────────────────
# Price trend
# ─────────────────────────────────────────────────────────────
def _prices_for_model(model_name, model, city, locality):
    """
    Collect rates for one model. Filtering happens in the database, only the needed
    columns are read, and every number is cast to FLOAT inside SQL. That means a row with a
    bad / oversized decimal value can no longer raise decimal.InvalidOperation.
    """
    names = {f.name for f in model._meta.concrete_fields}
    if 'city' not in names:
        return []

    loc_fields = [n for n in LOCALITY_FIELDS if n in names]
    if not loc_fields:
        return []

    wanted = [n for n in PRICE_FIELDS if n in names]
    if not wanted:
        return []

    loc_q = reduce(or_, [Q(**{f'{n}__iexact': locality}) for n in loc_fields])
    qs = model.objects.filter(Q(city__iexact=city) & loc_q)
    if 'is_deleted' in names:
        qs = qs.filter(is_deleted=False)

    qs = qs.annotate(**{f'c_{n}': Cast(n, FloatField()) for n in wanted})
    columns = [f'c_{n}' for n in wanted]

    divisor = RATE_DIVISOR.get(model_name, 1.0)
    prices = []
    for row in qs.values_list(*columns):
        values = {name: _to_float(val) for name, val in zip(wanted, row)}
        rate = _rate_from_values(values)
        if rate is None:
            continue
        rate = rate / divisor
        if MIN_RATE <= rate <= MAX_RATE:
            prices.append(rate)
    return prices


def sync_locality_price_trend(city, locality):
    prices = []
    for model_name in PROPERTY_MODEL_NAMES:
        if model_name in EXCLUDED_FROM_PRICE_TREND:
            continue
        try:
            model = apps.get_model(APP_LABEL, model_name)
        except LookupError:
            continue

        try:
            prices.extend(_prices_for_model(model_name, model, city, locality))
        except Exception:
            # one bad model must not stop the others (or the listing save)
            logger.exception(
                'Price trend skipped for %s (city=%s, locality=%s)',
                model_name, city, locality,
            )

    if not prices:
        return

    avg_price = round(sum(prices) / len(prices), 2)

    LocalityPriceTrend.objects.update_or_create(
        city=city,
        locality=locality,
        defaults={'avg_rate_per_sqft': avg_price},
    )


# ─────────────────────────────────────────────────────────────
# Locality insight stub
# ─────────────────────────────────────────────────────────────
def sync_locality_insight_stub(city, locality):
    LocalityInsight.objects.get_or_create(
        city=city,
        locality=locality,
        defaults={'is_active': True},
    )


# ─────────────────────────────────────────────────────────────
# Signal receiver
# ─────────────────────────────────────────────────────────────
def locality_autocreate_receiver(sender, instance, **kwargs):
    if kwargs.get('raw'):          # loaddata / fixtures
        return

    city, locality = get_locality_fields(instance)
    if not city or not locality:
        return

    try:
        # savepoint: if anything fails here, only this block is rolled back,
        # so the property itself is still saved
        with transaction.atomic():
            sync_locality_price_trend(city, locality)
            sync_locality_insight_stub(city, locality)
    except Exception:
        logger.exception('Locality signal failed for %s (city=%s, locality=%s)',
                         instance, city, locality)


def connect_locality_signals():
    for model_name in PROPERTY_MODEL_NAMES:
        try:
            model = apps.get_model(APP_LABEL, model_name)
        except LookupError:
            continue
        post_save.connect(
            locality_autocreate_receiver,
            sender=model,
            dispatch_uid=f'locality_autocreate_{model_name}',
        )