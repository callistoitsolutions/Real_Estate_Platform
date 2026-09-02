from Admin_App.models import (
    RentalResidentialProperty, CommercialRentalProperty, PGColivingProperty,
    ResaleResidentialProperty, CommercialResaleProperty,
    IndustrialResaleProperty, AgriculturalResaleProperty,
    ResidentialPlotResaleProperty, CommercialPlotResaleProperty,
    IndustrialPlotResaleProperty, AgriculturalPlotResaleProperty,
)

# type_key -> everything we need to query/aggregate/track that model
PROPERTY_REGISTRY = {
    # ---------------- RENTAL (3) ----------------
    'rental_residential': {
        'model': RentalResidentialProperty,
        'listing_type': 'rent', 'category': 'residential',
        'price_field': 'monthly_rent', 'bhk_field': 'bhk_type',
        'city_field': 'city', 'locality_field': 'locality_area',
    },
    'rental_commercial': {
        'model': CommercialRentalProperty,
        'listing_type': 'rent', 'category': 'commercial',
        'price_field': 'monthly_rent', 'bhk_field': None,
        'city_field': 'city', 'locality_field': 'locality',
    },
    'rental_pg': {
        'model': PGColivingProperty,
        'listing_type': 'rent', 'category': 'pg',
        'price_field': 'monthly_rent', 'bhk_field': None,
        'city_field': 'city', 'locality_field': 'locality',
    },
    # ---------------- RESALE (4) ----------------
    'resale_residential': {
        'model': ResaleResidentialProperty,
        'listing_type': 'sale', 'category': 'residential',
        'price_field': 'selling_price', 'bhk_field': 'bhk',
        'city_field': 'city', 'locality_field': 'locality',
    },
    'resale_commercial': {
        'model': CommercialResaleProperty,
        'listing_type': 'sale', 'category': 'commercial',
        'price_field': 'selling_price', 'bhk_field': None,
        'city_field': 'city', 'locality_field': 'locality',
    },
    'resale_industrial': {
        'model': IndustrialResaleProperty,
        'listing_type': 'sale', 'category': 'industrial',
        'price_field': 'selling_price', 'bhk_field': None,
        'city_field': 'city', 'locality_field': 'locality',
    },
    'resale_agricultural': {
        'model': AgriculturalResaleProperty,
        'listing_type': 'sale', 'category': 'agricultural',
        'price_field': 'selling_price', 'bhk_field': None,
        'city_field': 'district', 'locality_field': 'village',
    },
    # ---------------- RESALE PLOT (4) ----------------
    'plot_residential': {
        'model': ResidentialPlotResaleProperty,
        'listing_type': 'sale', 'category': 'plot',
        'price_field': 'selling_price', 'bhk_field': None,
        'city_field': 'city', 'locality_field': 'locality',
    },
    'plot_commercial': {
        'model': CommercialPlotResaleProperty,
        'listing_type': 'sale', 'category': 'plot',
        'price_field': 'selling_price', 'bhk_field': None,
        'city_field': 'city', 'locality_field': 'locality',
    },
    'plot_industrial': {
        'model': IndustrialPlotResaleProperty,
        'listing_type': 'sale', 'category': 'plot',
        'price_field': 'selling_price', 'bhk_field': None,
        'city_field': 'city', 'locality_field': 'locality',
    },
    'plot_agricultural': {
        'model': AgriculturalPlotResaleProperty,
        'listing_type': 'sale', 'category': 'plot',
        'price_field': 'selling_price', 'bhk_field': None,
        'city_field': 'city', 'locality_field': 'locality',
    },
}


# reverse lookup: actual model class -> registry key (used everywhere we
# only have the db object, e.g. listing cards, property_detail_view)
MODEL_TO_REGISTRY_KEY = {entry['model']: key for key, entry in PROPERTY_REGISTRY.items()}