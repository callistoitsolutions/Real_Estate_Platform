from django.contrib import admin
from django.urls import path
from seo import views
from seo import landing_views

urlpatterns = [

    # =========================================================
    # OWNER / LANDLORD LANDING PAGES
    # "List Your Property in <City>" / "...in <Locality>, <City>"
    # =========================================================
    path(
        "list-property/<str:city>/",
        landing_views.owner_listing_landing,
        name="owner_listing_landing_city",
    ),
    path(
        "list-property/<str:city>/<str:locality>/",
        landing_views.owner_listing_landing,
        name="owner_listing_landing",
    ),

    # Same page, landlord-intent slug (rent-out vs sell reads the same way to Google
    # as "list-property" but matches how a landlord actually searches)
    path(
        "rent-out-property/<str:city>/",
        landing_views.owner_listing_landing,
        name="rent_out_property_city",
    ),
    path(
        "rent-out-property/<str:city>/<str:locality>/",
        landing_views.owner_listing_landing,
        name="rent_out_property",
    ),

    # =========================================================
    # BUYER — FLATS FOR SALE
    # /flats-for-sale/nagpur/
    # /flats-for-sale/nagpur/besa/
    # /flats-for-sale/nagpur/2-bhk/
    # /flats-for-sale/nagpur/besa/2-bhk/
    # =========================================================
    path(
        "flats-for-sale/<str:city>/",
        landing_views.property_search_landing,
        {"page_type": "resale_residential"},
        name="flats_for_sale_city",
    ),
    path(
        "flats-for-sale/<str:city>/<str:bhk>/",
        landing_views.property_search_landing,
        {"page_type": "resale_residential"},
        name="flats_for_sale_bhk",
    ),
    path(
        "flats-for-sale/<str:city>/<str:locality>/<str:bhk>/",
        landing_views.property_search_landing,
        {"page_type": "resale_residential"},
        name="flats_for_sale",
    ),

    # =========================================================
    # TENANT — FLATS FOR RENT
    # /flats-for-rent/nagpur/
    # /flats-for-rent/nagpur/besa/
    # /flats-for-rent/nagpur/2-bhk/
    # =========================================================
    path(
        "flats-for-rent/<str:city>/",
        landing_views.property_search_landing,
        {"page_type": "rental_residential"},
        name="flats_for_rent_city",
    ),
    path(
        "flats-for-rent/<str:city>/<str:bhk>/",
        landing_views.property_search_landing,
        {"page_type": "rental_residential"},
        name="flats_for_rent_bhk",
    ),
    path(
        "flats-for-rent/<str:city>/<str:locality>/<str:bhk>/",
        landing_views.property_search_landing,
        {"page_type": "rental_residential"},
        name="flats_for_rent",
    ),

    # =========================================================
    # COMMERCIAL — RENT
    # /commercial-space-for-rent/nagpur/
    # /commercial-space-for-rent/nagpur/besa/
    # =========================================================
    path(
        "commercial-space-for-rent/<str:city>/",
        landing_views.property_search_landing,
        {"page_type": "commercial_rental"},
        name="commercial_for_rent_city",
    ),
    path(
        "commercial-space-for-rent/<str:city>/<str:locality>/",
        landing_views.property_search_landing,
        {"page_type": "commercial_rental"},
        name="commercial_for_rent",
    ),

    # =========================================================
    # COMMERCIAL — SALE
    # /commercial-property-for-sale/nagpur/
    # /commercial-property-for-sale/nagpur/besa/
    # =========================================================
    path(
        "commercial-property-for-sale/<str:city>/",
        landing_views.property_search_landing,
        {"page_type": "commercial_resale"},
        name="commercial_for_sale_city",
    ),
    path(
        "commercial-property-for-sale/<str:city>/<str:locality>/",
        landing_views.property_search_landing,
        {"page_type": "commercial_resale"},
        name="commercial_for_sale",
    ),

    # =========================================================
    # PG / CO-LIVING
    # /pg-coliving/nagpur/
    # NOTE: kept generic for now — property_search_landing() does not
    # currently accept a gender filter, so no /pg-for-boys//pg-for-girls
    # routes here yet. Add those only after the view function itself is
    # updated to accept and filter on a pg_for param (separate step).
    # =========================================================
    path(
        "pg-coliving/<str:city>/",
        landing_views.property_search_landing,
        {"page_type": "pg_coliving"},
        name="pg_coliving_city",
    ),

    # =========================================================
    # PLOTS — SALE
    # /plots-for-sale/nagpur/
    # /plots-for-sale/nagpur/besa/
    # =========================================================
    path(
        "plots-for-sale/<str:city>/",
        landing_views.property_search_landing,
        {"page_type": "residential_plot_resale"},
        name="plots_for_sale_city",
    ),
    path(
        "plots-for-sale/<str:city>/<str:locality>/",
        landing_views.property_search_landing,
        {"page_type": "residential_plot_resale"},
        name="plots_for_sale",
    ),

    # =========================================================
    # INDUSTRIAL — SALE
    # /industrial-property-for-sale/nagpur/
    # =========================================================
    path(
        "industrial-property-for-sale/<str:city>/",
        landing_views.property_search_landing,
        {"page_type": "industrial_sale"},
        name="industrial_for_sale_city",
    ),

    # =========================================================
    # AGRICULTURAL — SALE
    # /agricultural-land-for-sale/nagpur/
    # =========================================================
    path(
        "agricultural-land-for-sale/<str:city>/",
        landing_views.property_search_landing,
        {"page_type": "agriculture_sale"},
        name="agricultural_for_sale_city",
    ),

    # =========================================================
    # GENERIC TENANT / BUYER SEARCH LANDING PAGES (legacy — kept working)
    # e.g. /find/rental_residential/nagpur/besa/?bhk=2
    # Still the fallback route for any page_type not given its own
    # friendly slug above (e.g. the 3 plot-resale types other than
    # residential: commercial_plot_resale, industrial_plot_resale,
    # agricultural_plot_resale).
    # =========================================================
    path(
        "find/<str:page_type>/<str:city>/",
        landing_views.property_search_landing,
        name="property_search_landing_city",
    ),
    path(
        "find/<str:page_type>/<str:city>/<str:locality>/",
        landing_views.property_search_landing,
        name="property_search_landing",
    ),

    # =========================================================
    # QUICK ENQUIRY CAPTURE (tenant/buyer) — used by both landing pages
    # =========================================================
    path(
        "quick-enquiry/",
        landing_views.quick_locality_enquiry,
        name="quick_locality_enquiry",
    ),


    path("search/", landing_views.smart_search_redirect, name="smart_search_redirect")

]