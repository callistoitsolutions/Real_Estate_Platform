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

    count, properties = get_matching_properties(
        page_type, city, locality=locality_display, bhk=bhk, limit=24
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