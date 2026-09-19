"""
landing_seo.py
==================================================================
NEW FILE — does not modify seo_generator.py, signals.py, or models.py.

Implements the two missing landing page types from the SEO Growth
Engine doc:

  1. OWNER LISTING SEO   -> "List Your Property in <City>"
  2. LOCATION+CATEGORY SEO -> "2 BHK Flats for Rent in <Locality>, <City>"
     (this is the Eligibility Engine + aggregate SEO Page Generator —
     the piece that was previously 0% built)

Reuses your existing helpers from seo_generator.py (site_url, safe,
format_price, seo_limit, get_image_url) so title/description style
stays consistent with your per-property pages.

CATEGORY_CONFIG below is built directly from the field names already
used in seo_generator.py for each page_type — nothing here is guessed.
==================================================================
"""

import json
from django.apps import apps
from django.conf import settings
from django.utils.text import slugify

from seo.models import LocationSEO
from seo.seo_generator import (
    site_url, safe, format_price, seo_limit, get_image_url,
)

# =========================================================
# MINIMUM LIVE PROPERTIES REQUIRED BEFORE A LOCATION+CATEGORY
# PAGE IS ALLOWED TO EXIST. THIS IS THE ELIGIBILITY ENGINE.
# Raise this once you have more inventory per locality.
# =========================================================

MIN_ELIGIBLE_PROPERTIES = 3

APP_LABEL = "Admin_App"

EXCLUDED_STATUSES = {"pending", "rejected", "draft", "inactive", "expired"}


# =========================================================
# CATEGORY CONFIG
# One entry per property page_type already used across
# seo_generator.py / signals.py / sitemaps.py — same keys,
# so nothing here can drift out of sync with those files.
#
# url_listing_type / url_category map to the exact values
# property_detail_view() in Main_App/views.py already expects
# (verified against that function directly).
# =========================================================

CATEGORY_CONFIG = {
    "rental_residential": {
        "model": "RentalResidentialProperty",
        "listing_type": "rent", "label": "Flats for Rent",
        "city_field": "city", "locality_field": "locality_area",
        "price_field": "monthly_rent", "pk_field": "id",
        "title_field": "property_title",
        "bhk_field": "bhk_type", "type_field": "property_type",
        "url_listing_type": "rent", "url_category": "residential",
    },
    "commercial_rental": {
        "model": "CommercialRentalProperty",
        "listing_type": "rent", "label": "Commercial Property for Rent",
        "city_field": "city", "locality_field": "locality",
        "price_field": "monthly_rent", "pk_field": "id",
        "title_field": "property_title", "type_field": "property_type",
        "url_listing_type": "rent", "url_category": "commercial",
    },
    "pg_coliving": {
        "model": "PGColivingProperty",
        "listing_type": "rent", "label": "PG / Co-living",
        "city_field": "city", "locality_field": "locality",
        "price_field": "monthly_rent", "pk_field": "id",
        "title_field": "property_title",
        "url_listing_type": "rent", "url_category": "pg",
    },
    "resale_residential": {
        "model": "ResaleResidentialProperty",
        "listing_type": "sale", "label": "Flats for Sale",
        "city_field": "city", "locality_field": "locality",
        "price_field": "selling_price", "pk_field": "id",
        "title_field": "property_title",
        "bhk_field": "bhk", "type_field": "property_type",
        "url_listing_type": "sale", "url_category": "residential",
    },
    "commercial_resale": {
        "model": "CommercialResaleProperty",
        "listing_type": "sale", "label": "Commercial Property for Sale",
        "city_field": "city", "locality_field": "locality",
        "price_field": "selling_price", "pk_field": "id",
        "title_field": "property_title", "type_field": "property_type",
        "url_listing_type": "sale", "url_category": "commercial",
    },
    "industrial_sale": {
        "model": "IndustrialResaleProperty",
        "listing_type": "sale", "label": "Industrial Property for Sale",
        "city_field": "city", "locality_field": "locality",
        "price_field": "selling_price", "pk_field": "id",
        "title_field": "property_title", "type_field": "property_type",
        "url_listing_type": "sale", "url_category": "industrial",
    },
    "agriculture_sale": {
        "model": "AgriculturalResaleProperty",
        "listing_type": "sale", "label": "Agricultural Land for Sale",
        "city_field": "city", "locality_field": "village",
        "price_field": "selling_price", "pk_field": "id",
        "title_field": "property_title",
        "url_listing_type": "sale", "url_category": "agricultural",
    },
    "residential_plot_resale": {
        "model": "ResidentialPlotResaleProperty",
        "listing_type": "sale", "label": "Residential Plots for Sale",
        "city_field": "city", "locality_field": "locality",
        "price_field": "selling_price", "pk_field": "id",
        "title_field": "property_title",
        "url_listing_type": "sale", "url_category": "plot",
    },
    "commercial_plot_resale": {
        "model": "CommercialPlotResaleProperty",
        "listing_type": "sale", "label": "Commercial Plots for Sale",
        "city_field": "city", "locality_field": "locality",
        "price_field": "selling_price", "pk_field": "id",
        "title_field": "property_title",
        "url_listing_type": "sale", "url_category": "plot",
    },
    "industrial_plot_resale": {
        "model": "IndustrialPlotResaleProperty",
        "listing_type": "sale", "label": "Industrial Plots for Sale",
        "city_field": "city", "locality_field": "locality",
        "price_field": "selling_price", "pk_field": "id",
        "title_field": "property_title",
        "url_listing_type": "sale", "url_category": "plot",
    },
    "agricultural_plot_resale": {
        "model": "AgriculturalPlotResaleProperty",
        "listing_type": "sale", "label": "Agricultural Plots for Sale",
        "city_field": "city", "locality_field": "locality",
        "price_field": "selling_price", "pk_field": "id",
        "title_field": "property_title",
        "url_listing_type": "sale", "url_category": "plot",
    },
}

# categories owners are offered on the "List My Property" landing page
OWNER_CATEGORY_CHOICES = [
    ("rental_residential", "Flat / Apartment (Rent)"),
    ("resale_residential", "Flat / Apartment (Sale)"),
    ("pg_coliving", "PG / Co-living"),
    ("residential_plot_resale", "Residential Plot"),
    ("commercial_rental", "Commercial Property (Rent)"),
    ("commercial_resale", "Commercial Property (Sale)"),
    ("industrial_sale", "Industrial Property"),
    ("agriculture_sale", "Agricultural Land"),
]










# =========================================================
# SEARCH INTENT PARSER
# Reads a free-text query (from a search box, or a Google
# referral query string) and extracts every signal a real
# property portal uses to route a searcher correctly —
# not just budget, the full intent picture.
# =========================================================

import re

RENT_KEYWORDS = {"rent", "rental", "lease", "on rent", "for rent", "pg", "hostel", "coliving", "co-living"}
SALE_KEYWORDS = {"sale", "buy", "purchase", "resale", "for sale", "investment"}

CATEGORY_KEYWORDS = {
    "residential": {"flat", "apartment", "house", "home", "bhk", "villa", "residential"},
    "commercial": {"office", "shop", "showroom", "commercial", "workspace", "retail"},
    "pg": {"pg", "hostel", "coliving", "co-living", "paying guest"},
    "plot": {"plot", "land", "site"},
    "industrial": {"industrial", "warehouse", "factory", "godown"},
    "agricultural": {"agricultural", "farm", "farmland", "agriculture"},
}

FURNISHING_KEYWORDS = {
    "furnished": "Furnished",
    "semi furnished": "Semi Furnished",
    "semi-furnished": "Semi Furnished",
    "unfurnished": "Unfurnished",
}

NO_BROKERAGE_PHRASES = {"no brokerage", "without brokerage", "zero brokerage", "brokerage free", "direct owner"}

POSSESSION_KEYWORDS = {
    "ready to move": "Ready to Move",
    "immediate possession": "Immediate",
    "under construction": "Under Construction",
    "new launch": "New Launch",
}

# Multiplier words — "k"/"thousand" for rent-scale numbers,
# "lakh"/"lac"/"l" and "cr"/"crore" for sale-scale numbers
UNIT_MULTIPLIERS = [
    (r"crore|cr\b", 10000000),
    (r"lakh|lac\b|\bl\b", 100000),
    (r"thousand|k\b", 1000),
]

# Above this monthly figure, a bare number is almost certainly
# a SALE price, not a rent figure (nobody pays ₹2L/month rent
# for the property types this platform lists)
RENT_VS_SALE_THRESHOLD = 200000


def _extract_amount(text_chunk):
    """Turns '20k' / '20,000' / '1.5 lakh' / '2 cr' into a raw number."""
    text_chunk = text_chunk.strip().lower().replace(",", "")
    num_match = re.search(r"(\d+(?:\.\d+)?)", text_chunk)
    if not num_match:
        return None
    value = float(num_match.group(1))
    for pattern, multiplier in UNIT_MULTIPLIERS:
        if re.search(pattern, text_chunk):
            return int(value * multiplier)
    return int(value)


def parse_search_intent(query):
    """
    Returns a dict of every signal detected in a free-text search
    query. City/locality are NOT resolved here (that needs a DB
    lookup against real data) — the caller resolves those against
    LocalityPriceTrend / known cities.
    """
    q = (query or "").strip().lower()

    result = {
        "raw_query": query,
        "listing_type": None,       # "rent" / "sale"
        "category_hint": None,      # "residential" / "commercial" / "pg" / "plot" / "industrial" / "agricultural"
        "bhk": None,
        "min_price": None,
        "max_price": None,
        "furnishing": None,
        "no_brokerage": False,
        "possession": None,
        "confidence": "low",
    }

    # ---- transaction type: explicit keywords first ----
    if any(kw in q for kw in RENT_KEYWORDS):
        result["listing_type"] = "rent"
    elif any(kw in q for kw in SALE_KEYWORDS):
        result["listing_type"] = "sale"

    # ---- category ----
    for cat, keywords in CATEGORY_KEYWORDS.items():
        if any(kw in q for kw in keywords):
            result["category_hint"] = cat
            break

    # PG queries are always rent, regardless of anything else typed
    if result["category_hint"] == "pg":
        result["listing_type"] = "rent"

    # ---- BHK ----
    bhk_match = re.search(r"(\d)\s*-?\s*bhk", q)
    if bhk_match:
        result["bhk"] = f"{bhk_match.group(1)} BHK"

    # ---- budget: "under/below/less than X", "above/over X", "between X and Y" ----
    between_match = re.search(
        r"between\s+([\d.,]+\s*(?:k|thousand|lakh|lac|l|cr|crore)?)\s+(?:and|to|-)\s+([\d.,]+\s*(?:k|thousand|lakh|lac|l|cr|crore)?)",
        q,
    )
    under_match = re.search(r"(?:under|below|less than|upto|up to|within)\s+([\d.,]+\s*(?:k|thousand|lakh|lac|l|cr|crore)?)", q)
    above_match = re.search(r"(?:above|over|more than)\s+([\d.,]+\s*(?:k|thousand|lakh|lac|l|cr|crore)?)", q)

    if between_match:
        result["min_price"] = _extract_amount(between_match.group(1))
        result["max_price"] = _extract_amount(between_match.group(2))
    elif under_match:
        result["max_price"] = _extract_amount(under_match.group(1))
    elif above_match:
        result["min_price"] = _extract_amount(above_match.group(1))

    # ---- if no explicit rent/sale keyword, infer from budget magnitude ----
    # (a monthly-scale number strongly implies rent; nobody types a
    # sale-price search without "buy"/"sale" somewhere in the query)
    if not result["listing_type"] and result["max_price"]:
        result["listing_type"] = "rent" if result["max_price"] <= RENT_VS_SALE_THRESHOLD else "sale"
        result["confidence"] = "medium"  # inferred, not explicit
    elif result["listing_type"]:
        result["confidence"] = "high"    # explicit keyword found

    # ---- furnishing ----
    for phrase, label in FURNISHING_KEYWORDS.items():
        if phrase in q:
            result["furnishing"] = label
            break

    # ---- no brokerage ----
    if any(phrase in q for phrase in NO_BROKERAGE_PHRASES):
        result["no_brokerage"] = True

    # ---- possession ----
    for phrase, label in POSSESSION_KEYWORDS.items():
        if phrase in q:
            result["possession"] = label
            break

    return result


def resolve_page_type(intent):
    """Maps parsed intent (listing_type + category_hint) to the
    exact page_type key CATEGORY_CONFIG already uses."""
    listing_type = intent.get("listing_type") or "rent"
    category = intent.get("category_hint") or "residential"

    mapping = {
        ("rent", "residential"): "rental_residential",
        ("rent", "commercial"): "commercial_rental",
        ("rent", "pg"): "pg_coliving",
        ("sale", "residential"): "resale_residential",
        ("sale", "commercial"): "commercial_resale",
        ("sale", "plot"): "residential_plot_resale",
        ("sale", "industrial"): "industrial_sale",
        ("sale", "agricultural"): "agriculture_sale",
    }
    return mapping.get((listing_type, category), "rental_residential")








def get_model(page_type):
    cfg = CATEGORY_CONFIG.get(page_type)
    if not cfg:
        return None, None
    try:
        return apps.get_model(APP_LABEL, cfg["model"]), cfg
    except LookupError:
        return None, cfg


# =========================================================
# ELIGIBILITY ENGINE + MATCHING PROPERTIES QUERY
# =========================================================

def get_matching_properties(page_type, city, locality=None, bhk=None, limit=24,
                             max_price=None, min_price=None, furnishing=None):
    """
    Returns (queryset_count, list_of_serialized_property_dicts).
    This IS the eligibility check — call this before deciding
    whether to render a location+category landing page at all.
    """
    model, cfg = get_model(page_type)
    if not model:
        return 0, []

    qs = model.objects.filter(**{f"{cfg['city_field']}__iexact": city})

    if locality:
        qs = qs.filter(**{f"{cfg['locality_field']}__iexact": locality})

    model_field_names = [f.name for f in model._meta.get_fields()]

    if "is_deleted" in model_field_names:
        qs = qs.filter(is_deleted=False)
    if "is_duplicate" in model_field_names:
        qs = qs.filter(is_duplicate=False)

    if bhk and cfg.get("bhk_field") and cfg["bhk_field"] in model_field_names:
        qs = qs.filter(**{f"{cfg['bhk_field']}__iexact": bhk})

    price_field = cfg.get("price_field")
    if price_field and price_field in model_field_names:
        if max_price:
            qs = qs.filter(**{f"{price_field}__lte": max_price})
        if min_price:
            qs = qs.filter(**{f"{price_field}__gte": min_price})

    if furnishing and "furnishing_status" in model_field_names:
        qs = qs.filter(furnishing_status__icontains=furnishing)

    # status filtering (same pattern as Main_App/sitemaps.py)
    results = []
    for obj in qs.order_by("-id")[: limit * 3]:  # overfetch, then status-filter
        status = str(getattr(obj, "listing_status", "") or "").strip().lower()
        approval = str(getattr(obj, "approval_status", "") or "").strip().lower()
        if status in EXCLUDED_STATUSES or approval in EXCLUDED_STATUSES:
            continue
        results.append(obj)
        if len(results) >= limit:
            break

    total_count = len(results) if len(results) < limit else qs.count()

    serialized = [serialize_property(obj, page_type, cfg) for obj in results]
    return total_count, serialized


def serialize_property(obj, page_type, cfg):
    price_raw = getattr(obj, cfg["price_field"], None)
    return {
        "id": getattr(obj, cfg["pk_field"]),
        "title": safe(getattr(obj, cfg.get("title_field", ""), "")) or cfg["label"],
        "bhk": safe(getattr(obj, cfg.get("bhk_field", ""), "")) if cfg.get("bhk_field") else "",
        "type": safe(getattr(obj, cfg.get("type_field", ""), "")) if cfg.get("type_field") else "",
        "price_display": format_price(price_raw),
        "locality": safe(getattr(obj, cfg["locality_field"], "")),
        "city": safe(getattr(obj, cfg["city_field"], "")),
        "image_url": get_image_url(obj),
        "detail_url": f"/listing/{cfg['url_listing_type']}/{cfg['url_category']}/{getattr(obj, cfg['pk_field'])}/",
    }


# =========================================================
# LOCATION + CATEGORY LANDING PAGE — SEO GENERATION
# =========================================================

def build_location_category_title(page_type, city, locality=None, bhk=None):
    cfg = CATEGORY_CONFIG[page_type]
    place = f"{locality}, {city}" if locality else city
    prefix = f"{bhk} " if bhk else ""
    return f"{prefix}{cfg['label']} in {place}"


def generate_location_category_seo(page_type, city, locality=None, bhk=None, property_count=0):
    cfg = CATEGORY_CONFIG[page_type]
    place = f"{locality}, {city}" if locality else city

    title = build_location_category_title(page_type, city, locality, bhk)
    description = seo_limit(
        f"Browse {property_count}+ verified {cfg['label'].lower()} in {place}. "
        f"Compare prices, photos and amenities. Enquire directly with owners/agents on KANISHKAIMPERIA."
    )
    keyword = f"{cfg['label'].lower()} in {place}"

    slug_bits = [page_type, city, locality or "", bhk or ""]
    key = "loc-cat-" + slugify("-".join([b for b in slug_bits if b]))
    # FIXED: seo.urls is mounted at path('seo/', include('seo.urls')) in
    # the project's root urls.py -- so the real, working URL for this
    # view is /seo/find/..., not /find/.... Without the prefix here,
    # the canonical tag and every sitemap entry built from it pointed
    # at a URL that 404s. (If you later remount seo.urls at the root
    # to drop "/seo/" from public URLs -- worth doing for SEO -- update
    # this prefix to match at the same time.)
    canonical_path = f"/seo/find/{page_type}/{slugify(city)}/"
    if locality:
        canonical_path = f"/seo/find/{page_type}/{slugify(city)}/{slugify(locality)}/"
    canonical_url = f"{site_url()}{canonical_path}"

    schema = {
        "@context": "https://schema.org",
        "@type": "ItemList",
        "name": title,
        "description": description,
        "numberOfItems": property_count,
    }

    LocationSEO.objects.update_or_create(
        key=key,
        defaults={
            "pagetype": "location_category",
            "meta_title": title[:255],
            "meta_description": description[:155],
            "primary_keyword": keyword,
            "secondary_keywords": f"{place} properties, {cfg['label'].lower()}",
            "slug": slugify(title),
            "canonical_url": canonical_url,
            "schema_json": json.dumps(schema),
            "intro_html": f"<h1>{title}</h1>",
            "is_active": True,
        },
    )
    return LocationSEO.objects.get(key=key)


# =========================================================
# OWNER LISTING LANDING PAGE — SEO GENERATION
# =========================================================

def generate_owner_listing_seo(city, locality=None):
    place = f"{locality}, {city}" if locality else city
    title = f"List Your Property in {place} | KANISHKAIMPERIA"
    description = seo_limit(
        f"List your flat, PG, plot, commercial or agricultural property for rent or sale "
        f"in {place} for free on KANISHKAIMPERIA. Reach verified tenants and buyers directly."
    )
    keyword = f"list property in {place}"

    key = "owner-listing-" + slugify(f"{city}-{locality or 'all'}")
    # FIXED: same /seo/ prefix issue as generate_location_category_seo
    # above -- see that comment.
    canonical_path = f"/seo/list-property/{slugify(city)}/"
    if locality:
        canonical_path = f"/seo/list-property/{slugify(city)}/{slugify(locality)}/"
    canonical_url = f"{site_url()}{canonical_path}"

    schema = {
        "@context": "https://schema.org",
        "@type": "Service",
        "name": title,
        "description": description,
        "areaServed": place,
        "provider": {"@type": "Organization", "name": "KANISHKAIMPERIA"},
    }

    LocationSEO.objects.update_or_create(
        key=key,
        defaults={
            "pagetype": "owner_listing",
            "meta_title": title[:255],
            "meta_description": description[:155],
            "primary_keyword": keyword,
            "secondary_keywords": f"post property {place}, sell property {place}, rent out property {place}",
            "slug": slugify(title),
            "canonical_url": canonical_url,
            "schema_json": json.dumps(schema),
            "intro_html": f"<h1>{title}</h1>",
            "is_active": True,
        },
    )
    return LocationSEO.objects.get(key=key)


# =========================================================
# RECENT LISTINGS FOR SOCIAL PROOF ON THE OWNER LANDING PAGE
# =========================================================

def get_recent_listings_for_city(city, limit=4):
    """Pulls a small, mixed sample of recent live listings in the city —
    used as 'recently listed' social proof on the owner landing page."""
    sample_types = ["rental_residential", "resale_residential", "pg_coliving", "commercial_rental"]
    out = []
    for page_type in sample_types:
        if len(out) >= limit:
            break
        _, props = get_matching_properties(page_type, city, limit=1)
        out.extend(props)
    return out[:limit]