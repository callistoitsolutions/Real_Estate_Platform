from Main_App .models import *
from Admin_App .models import *

PROPERTY_MODELS = [
    (RentalResidentialProperty, "Rental Residential"),
    (CommercialRentalProperty, "Commercial Rental"),
    (PGColivingProperty, "PG / Co-living"),
    (ResaleResidentialProperty, "Resale Residential"),
    (CommercialResaleProperty, "Resale Commercial"),
    (PlotSaleProperty, "Plot Sale"),
    (IndustrialResaleProperty, "Industrial Resale"),
    (AgriculturalResaleProperty, "Agricultural Resale"),
    (ResidentialPlotResaleProperty, "Residential Plot Resale"),
    (CommercialPlotResaleProperty, "Commercial Plot Resale"),
    (IndustrialPlotResaleProperty, "Industrial Plot Resale"),
    (AgriculturalPlotResaleProperty, "Agricultural Plot Resale"),
]

def get_properties_for_user(user_id):
    results = []
    for model, label in PROPERTY_MODELS:
        qs = model.objects.filter(listed_by_id=user_id, is_deleted=False)
        for prop in qs:
            results.append({
                "type_label": label,
                "obj": prop,
            })
    return results