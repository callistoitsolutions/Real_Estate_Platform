"""
landing_views.py
==================================================================
NEW FILE — does not modify seo/views.py.

Two SEO landing pages + one lead-capture endpoint:

  owner_listing_landing()     /list-property/<city>/
                               /list-property/<city>/<locality>/

  property_search_landing()   /find/<page_type>/<city>/
                               /find/<page_type>/<city>/<locality>/
                               (this is the Eligibility Engine in action —
                               it will NOT render a thin page; it redirects
                               to your existing general listings page instead)

  quick_locality_enquiry()    POST target for the on-page "Request Callback"
                               form — saves into your existing Contact_Enquiry
                               model, no schema changes required.
==================================================================
"""

from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils.text import slugify
from django.views.decorators.http import require_POST

from seo.landing_seo import (
    CATEGORY_CONFIG,
    OWNER_CATEGORY_CHOICES,
    MIN_ELIGIBLE_PROPERTIES,
    get_matching_properties,
    get_recent_listings_for_city,
    generate_location_category_seo,
    generate_owner_listing_seo,
)

from Main_App.models import Contact_Enquiry, LocalityInsight, LocalityPriceTrend


# =========================================================
# 1. OWNER LISTING LANDING PAGE
# =========================================================

def owner_listing_landing(request, city, locality=None):
    city = city.replace("-", " ").title()
    locality_display = locality.replace("-", " ").title() if locality else None

    seo = generate_owner_listing_seo(city, locality_display)
    recent_listings = get_recent_listings_for_city(city, limit=4)

    context = {
        "city": city,
        "locality": locality_display,
        "seo": seo,
        "recent_listings": recent_listings,
        "owner_category_choices": OWNER_CATEGORY_CHOICES,
        "post_property_url": reverse("post_property"),
    }
    return render(request, "seo_user/owner_listing_landing.html", context)


# =========================================================
# 2. LOCATION + CATEGORY SEARCH LANDING PAGE
#    (Eligibility Engine lives here)
# =========================================================

def property_search_landing(request, page_type, city, locality=None, bhk=None):
    if page_type not in CATEGORY_CONFIG:
        return redirect("listings")

    city = city.replace("-", " ").title()
    locality_display = locality.replace("-", " ").title() if locality else None

    bhk = bhk or request.GET.get("bhk", "").strip() or None
    max_price = request.GET.get("max_price", "").strip() or None
    min_price = request.GET.get("min_price", "").strip() or None
    furnishing = request.GET.get("furnishing", "").strip() or None

    count, properties = get_matching_properties(
        page_type, city, locality=locality_display, bhk=bhk, limit=24,
        max_price=int(max_price) if max_price else None,
        min_price=int(min_price) if min_price else None,
        furnishing=furnishing,
    )

    # ---- ELIGIBILITY CHECK ----
    if count < MIN_ELIGIBLE_PROPERTIES:
        if locality_display:
            # not enough at locality level -> try the city-level page instead
            return redirect(
                "property_search_landing_city", page_type=page_type, city=slugify(city)
            )
        # not enough even at city level -> fall back to your general
        # search page, pre-filtered, instead of serving a thin page
        cfg = CATEGORY_CONFIG[page_type]
        fallback_url = (
            f"{reverse('listings')}?type={cfg['listing_type']}"
            f"&category={cfg['url_category']}&city_filter={city}"
        )
        return redirect(fallback_url)

    seo = generate_location_category_seo(
        page_type, city, locality_display, bhk, property_count=count
    )

    locality_insight = None
    price_trend = None
    nearby_localities = []
    if locality_display:
        locality_insight = LocalityInsight.objects.filter(
            city__iexact=city, locality__iexact=locality_display, is_active=True
        ).first()
        price_trend = LocalityPriceTrend.objects.filter(
            city__iexact=city, locality__iexact=locality_display
        ).first()
    nearby_localities = LocalityPriceTrend.objects.filter(city__iexact=city)
    if locality_display:
        nearby_localities = nearby_localities.exclude(locality__iexact=locality_display)
    nearby_localities = nearby_localities[:5]

    cfg = CATEGORY_CONFIG[page_type]

    context = {
        "page_type": page_type,
        "cfg": cfg,
        "city": city,
        "locality": locality_display,
        "bhk": bhk,
        "seo": seo,
        "properties": properties,
        "property_count": count,
        "locality_insight": locality_insight,
        "price_trend": price_trend,
        "nearby_localities": nearby_localities,
    }
    return render(request, "seo_user/property_search_landing.html", context)


# =========================================================
# 3. QUICK ENQUIRY CAPTURE (tenant/buyer, from the landing page)
#    Saves into your EXISTING Contact_Enquiry model — no new
#    tables required. Attribution (which landing page this came
#    from) is embedded in contact_message until Contact_Enquiry
#    gets dedicated source/medium/landing_page fields.
# =========================================================

@require_POST
def quick_locality_enquiry(request):
    name = request.POST.get("name", "").strip()
    phone = request.POST.get("phone", "").strip()
    email = request.POST.get("email", "").strip()
    message = request.POST.get("message", "").strip()
    page_type = request.POST.get("page_type", "").strip()
    city = request.POST.get("city", "").strip()
    locality = request.POST.get("locality", "").strip()
    source_page = request.POST.get("source_page", "").strip()

    label = CATEGORY_CONFIG.get(page_type, {}).get("label", page_type or "Property")
    place = f"{locality}, {city}" if locality else city

    attributed_message = (
        f"[SEO Landing Page: {source_page}] "
        f"Interested in: {label} in {place}. "
        f"{message}"
    ).strip()

    Contact_Enquiry.objects.create(
        contact_name=name,
        contact_phone=phone,
        contact_email=email,
        contact_city=city[:20] if city else None,  # field is max_length=20
        contact_en_title=label[:100],
        contact_en_type=page_type[:100],
        contact_message=attributed_message,
    )

    if request.headers.get("x-requested-with") == "XMLHttpRequest":
        from django.http import JsonResponse
        return JsonResponse({"status": "ok", "message": "Thanks! Our team will contact you shortly."})

    return redirect(request.META.get("HTTP_REFERER", "/"))




# =========================================================
# 4. SMART SEARCH — free-text query in, correct landing page out.
#    Handles the full intent picture: transaction type, category,
#    BHK, budget, furnishing, no-brokerage, possession — not just
#    budget alone. This is what lets "2bhk under 20k besa no
#    brokerage" land the searcher on exactly the right filtered page.
# =========================================================

from seo.landing_seo import parse_search_intent, resolve_page_type
from Main_App.models import LocalityPriceTrend


def smart_search_redirect(request):
    query = request.GET.get("q", "").strip()
    if not query:
        return redirect("listings")

    intent = parse_search_intent(query)
    page_type = resolve_page_type(intent)

    # resolve city/locality against real data — simple substring
    # match against every known city/locality pair, longest match wins
    q_lower = query.lower()
    city_match, locality_match = None, None
    best_len = 0
    for row in LocalityPriceTrend.objects.values_list("city", "locality").distinct():
        city, locality = row
        if city and city.lower() in q_lower and len(city) > best_len:
            city_match, best_len = city, len(city)
        if locality and locality.lower() in q_lower:
            locality_match = locality

    if not city_match:
        # can't place it geographically — fall back to general search
        # with whatever filters we did detect
        cfg = CATEGORY_CONFIG.get(page_type, {})
        fallback = f"{reverse('listings')}?type={cfg.get('listing_type','')}&category={cfg.get('url_category','')}"
        return redirect(fallback)

    url_kwargs = {"page_type": page_type, "city": slugify(city_match)}
    url_name = "property_search_landing_city"
    if locality_match:
        url_kwargs["locality"] = slugify(locality_match)
        url_name = "property_search_landing"

    target = reverse(url_name, kwargs=url_kwargs)

    extra_params = []
    if intent["bhk"]:
        extra_params.append(f"bhk={intent['bhk']}")
    if intent["max_price"]:
        extra_params.append(f"max_price={intent['max_price']}")
    if intent["min_price"]:
        extra_params.append(f"min_price={intent['min_price']}")
    if intent["furnishing"]:
        extra_params.append(f"furnishing={intent['furnishing']}")
    if intent["no_brokerage"]:
        extra_params.append("no_brokerage=1")

    if extra_params:
        target += "?" + "&".join(extra_params)

    return redirect(target)