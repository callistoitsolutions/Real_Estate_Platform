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
    # GENERIC TENANT / BUYER SEARCH LANDING PAGES (legacy — kept working)
    # e.g. /find/rental_residential/nagpur/besa/?bhk=2
    # Also still the route every OTHER page_type uses
    # (commercial_rental, pg_coliving, commercial_resale, industrial_sale,
    #  agriculture_sale, the 4 plot-resale types) until each gets its
    # own friendly slug the same way flats-for-sale/rent did above.
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

]