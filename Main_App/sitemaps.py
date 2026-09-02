from django.contrib.sitemaps import Sitemap
from Admin_App.models import (
    RentalResidentialProperty,
    CommercialRentalProperty,
    PGColivingProperty,
    ResaleResidentialProperty,
    CommercialResaleProperty,
    IndustrialResaleProperty,
    AgriculturalResaleProperty,
    ResidentialPlotResaleProperty,
    CommercialPlotResaleProperty,
    IndustrialPlotResaleProperty,
    AgriculturalPlotResaleProperty,
)


class BasePropertySitemap(Sitemap):
    changefreq = "daily"
    protocol = "https"
    model = None
    listing_type = None
    category = None

    def items(self):
        qs = self.model.objects.all()
        if hasattr(self.model, "is_deleted"):
            qs = qs.filter(is_deleted=False)
        if hasattr(self.model, "is_duplicate"):
            qs = qs.filter(is_duplicate=False)
        return qs

    def location(self, obj):
        return f"/listing/{self.listing_type}/{self.category}/{obj.id}/"

    def lastmod(self, obj):
        return getattr(obj, "updated_at", None) or getattr(obj, "created_at", None)


class RentalResidentialSitemap(BasePropertySitemap):
    model = RentalResidentialProperty
    listing_type = "rental"
    category = "residential"


class RentalCommercialSitemap(BasePropertySitemap):
    model = CommercialRentalProperty
    listing_type = "rental"
    category = "commercial"


class RentalPGSitemap(BasePropertySitemap):
    model = PGColivingProperty
    listing_type = "rental"
    category = "pg"


class ResaleResidentialSitemap(BasePropertySitemap):
    model = ResaleResidentialProperty
    listing_type = "resale"
    category = "residential"


class ResaleCommercialSitemap(BasePropertySitemap):
    model = CommercialResaleProperty
    listing_type = "resale"
    category = "commercial"


class ResaleIndustrialSitemap(BasePropertySitemap):
    model = IndustrialResaleProperty
    listing_type = "resale"
    category = "industrial"


class ResaleAgriculturalSitemap(BasePropertySitemap):
    model = AgriculturalResaleProperty
    listing_type = "resale"
    category = "agricultural"


class PlotResidentialSitemap(BasePropertySitemap):
    model = ResidentialPlotResaleProperty
    listing_type = "resale_plot"
    category = "residential"


class PlotCommercialSitemap(BasePropertySitemap):
    model = CommercialPlotResaleProperty
    listing_type = "resale_plot"
    category = "commercial"


class PlotIndustrialSitemap(BasePropertySitemap):
    model = IndustrialPlotResaleProperty
    listing_type = "resale_plot"
    category = "industrial"


class PlotAgriculturalSitemap(BasePropertySitemap):
    model = AgriculturalPlotResaleProperty
    listing_type = "resale_plot"
    category = "agricultural"


sitemaps = {
    "rental_residential": RentalResidentialSitemap,
    "rental_commercial": RentalCommercialSitemap,
    "rental_pg": RentalPGSitemap,
    "resale_residential": ResaleResidentialSitemap,
    "resale_commercial": ResaleCommercialSitemap,
    "resale_industrial": ResaleIndustrialSitemap,
    "resale_agricultural": ResaleAgriculturalSitemap,
    "plot_residential": PlotResidentialSitemap,
    "plot_commercial": PlotCommercialSitemap,
    "plot_industrial": PlotIndustrialSitemap,
    "plot_agricultural": PlotAgriculturalSitemap,
}