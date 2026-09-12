import json

from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.utils.text import slugify

from seo.models import LocationSEO


# =========================================================
# SITE DOMAIN (used to build canonical_url — set SITE_URL in settings.py)
# =========================================================

def site_url():
    return getattr(settings, "SITE_URL", "https://estateflow.nedient.co.in").rstrip("/")


# =========================================================
# NEW: single source of truth for the REAL, working public URL of
# each page_type. Must match Main_App/urls.py exactly.
#
# The previous build_canonical_url() built "/listing/<page_type>/<id>/"
# (e.g. /listing/rental_residential/EFPRR-34AF4D78/) which does not
# match ANY route Main_App/urls.py actually defines:
#
#   path('listing/<str:listing_type>/<str:category>/<str:slug>/<str:pk>/',
#        views.property_detail_view, name='property_detail')
#   path('listing/<str:listing_type>/<str:category>/<str:pk>/',
#        views.property_detail_view, name='property_detail_legacy')
#   path('blogs/<slug:slug>/', views.blog_details, name='blog_details')
#   path('services/<slug:slug>/', views.services_details, name='services_details')
#
# Every canonical_url saved before this fix, and every sitemap.xml URL
# built from it, 404s. This function builds the URL Main_App/urls.py
# actually resolves. Main_App/sitemaps.py reads canonical_url straight
# off the saved LocationSEO record instead of reconstructing it a
# second time, so the two can never drift apart again.
# =========================================================

PAGE_TYPE_URL_INFO = {
    "rental_residential":       ("rent", "residential"),
    "commercial_rental":        ("rent", "commercial"),
    "pg_coliving":               ("rent", "pg"),
    "resale_residential":       ("sale", "residential"),
    "commercial_resale":        ("sale", "commercial"),
    "plot_sale":                 ("sale", "plot"),          # legacy PlotSaleProperty model
    "industrial_sale":          ("sale", "industrial"),
    "agriculture_sale":         ("sale", "agriculture"),
    "residential_plot_resale":  ("sale", "plot"),
    "commercial_plot_resale":   ("sale", "plot"),
    "industrial_plot_resale":   ("sale", "plot"),
    "agricultural_plot_resale": ("sale", "plot"),
}


def build_public_path(page_type, object_id, slug=None):
    """Relative path only (no domain) -- used by build_canonical_url()
    below, and importable by Main_App/sitemaps.py as a fallback for any
    row that hasn't been backfilled with a LocationSEO record yet."""

    if page_type == "blog":
        return f"/blogs/{slug}/" if slug else f"/blogs/{object_id}/"
    if page_type == "service":
        return f"/services/{slug}/" if slug else f"/services/{object_id}/"

    listing_type, category = PAGE_TYPE_URL_INFO.get(page_type, (None, None))
    if not listing_type:
        # Unknown page_type (e.g. "subscription", which has no public
        # page of its own) -- keep the old shape rather than crash.
        return f"/listing/{page_type}/{object_id}/"

    if slug:
        return f"/listing/{listing_type}/{category}/{slug}/{object_id}/"
    # No slug available -- use the legacy 3-segment route, which
    # property_detail_view resolves identically to the slugged one.
    return f"/listing/{listing_type}/{category}/{object_id}/"


# =========================================================
# SAFE FIELD
# =========================================================

def safe(value):

    if value is None:
        return ""

    return str(value).strip()


# =========================================================
# FORMAT PRICE (display string, e.g. "12.5 Lakh")
# =========================================================

def format_price(value):

    if not value:
        return ""

    try:

        value = int(float(value))

        if value >= 10000000:
            return f"{round(value / 10000000, 2)} Cr"

        elif value >= 100000:
            return f"{round(value / 100000, 2)} Lakh"

        return f"{value}"

    except Exception:
        return str(value)


# =========================================================
# RAW NUMBER (real numeric price for schema "offers.price" — schema.org
# wants a plain number, NOT "12.5 Lakh")
# =========================================================

def raw_number(value):
    try:
        return float(value)
    except Exception:
        return None


# =========================================================
# LIMIT SEO DESCRIPTION
# =========================================================

def seo_limit(text, limit=155):

    text = " ".join(str(text).split())

    if len(text) <= limit:
        return text

    return text[:limit].rsplit(" ", 1)[0] + "..."


# =========================================================
# NEW: FAQ SCHEMA — pulled from instance.faqs (every property model in
# Main_App already has this related_name, auto-generated on save()).
# This is the single biggest AEO win: without this, Google/AI Overviews
# have no idea your FAQ content is Q&A at all.
# =========================================================

def get_faq_schema(instance):
    faqs_rel = getattr(instance, "faqs", None)
    if faqs_rel is None:
        return None
    try:
        faqs = list(faqs_rel.all()[:15])
    except Exception:
        return None
    if not faqs:
        return None

    import re
    def strip_html(v):
        return re.sub(r"<[^>]+>", " ", str(v or "")).strip()

    return {
        "@type": "FAQPage",
        "mainEntity": [
            {
                "@type": "Question",
                "name": strip_html(f.question)[:300],
                "acceptedAnswer": {
                    "@type": "Answer",
                    "text": strip_html(f.answer)[:2000],
                },
            }
            for f in faqs
        ],
    }


# =========================================================
# NEW: first property image, absolute URL — for schema "image"
# =========================================================

def get_image_url(instance):
    images_rel = getattr(instance, "images", None)
    if images_rel is None:
        return None
    try:
        first = images_rel.first()
        if first and getattr(first, "image", None):
            return f"{site_url()}{first.image.url}"
    except Exception:
        pass
    return None


# =========================================================
# NEW: canonical URL — was declared on the model but never populated.
# Uses ONE consistent pattern shared with seo/sitemaps.py so the two
# never drift apart: /listing/<page_type>/<id>/
# =========================================================

def build_canonical_url(page_type, object_id, slug=None):
    return f"{site_url()}{build_public_path(page_type, object_id, slug)}"


# =========================================================
# NEW: wrap the main entity schema + FAQ schema together as one
# JSON-LD block using @graph — one <script> tag, both schemas valid.
# =========================================================

def combine_schema(entity_schema, faq_schema):
    graph = [entity_schema]
    if faq_schema:
        graph.append(faq_schema)
    if len(graph) == 1:
        out = {"@context": "https://schema.org"}
        out.update(entity_schema)
        return out
    return {"@context": "https://schema.org", "@graph": graph}


# =========================================================
# CREATE DYNAMIC SEO
# =========================================================

def create_dynamic_seo(instance, page_type):

    try:

        title = ""
        description = ""
        keyword = ""
        secondary_keywords = ""
        intro_html = ""
        schema = {}

        # values used across many property types for the schema block
        price_raw = None
        image_url = get_image_url(instance)

        # =====================================================
        # RENTAL RESIDENTIAL
        # =====================================================

        if page_type == "rental_residential":

            bhk = safe(instance.bhk_type)
            property_type = safe(instance.property_type)
            locality_area = safe(instance.locality_area)
            city = safe(instance.city)
            rent = format_price(instance.monthly_rent)
            price_raw = raw_number(instance.monthly_rent)

            title = f"{bhk} {property_type} for Rent in {locality_area}, {city}"

            description = seo_limit(
                f"Premium {bhk} {property_type} available for rent in "
                f"{locality_area}, {city}. Monthly rent ₹{rent}. "
                f"Explore verified rental homes with modern amenities."
            )

            keyword = f"{bhk} property for rent in {city}"

            secondary_keywords = (
                f"flat for rent in {city}, "
                f"{property_type} rent, "
                f"rental homes in {locality_area}"
            )

            intro_html = f"""
            <h1>{title}</h1>

            <p>
            Find premium {bhk} {property_type} for rent in
            {locality_area}, {city}.
            </p>
            """

            # FIXED: "Residence" -> "RealEstateListing" (valid schema.org type
            # for a listing), added address + offers (price) + image.
            schema = {
                "@type": "RealEstateListing",
                "name": title,
                "description": description,
                "address": {
                    "@type": "PostalAddress",
                    "addressLocality": locality_area,
                    "addressRegion": city,
                    "addressCountry": "IN",
                },
            }

        # =====================================================
        # COMMERCIAL RENTAL
        # =====================================================

        elif page_type == "commercial_rental":

            property_type = safe(instance.property_type)
            locality = safe(instance.locality)
            city = safe(instance.city)
            rent = format_price(instance.monthly_rent)
            price_raw = raw_number(instance.monthly_rent)

            title = f"{property_type} for Rent in {locality}, {city}"

            description = seo_limit(
                f"Commercial {property_type} available for rent in "
                f"{locality}, {city}. Monthly rent ₹{rent}."
            )

            keyword = f"commercial property for rent in {city}"

            secondary_keywords = (
                f"office space rent, "
                f"shop for rent in {city}"
            )

            intro_html = f"""
            <h1>{title}</h1>

            <p>
            Explore commercial spaces for rent in
            {locality}, {city}.
            </p>
            """

            # FIXED: "Office" -> "RealEstateListing"
            schema = {
                "@type": "RealEstateListing",
                "name": title,
                "description": description,
                "address": {
                    "@type": "PostalAddress",
                    "addressLocality": locality,
                    "addressRegion": city,
                    "addressCountry": "IN",
                },
            }

        # =====================================================
        # PG COLIVING
        # =====================================================

        elif page_type == "pg_coliving":

            pg_name = safe(instance.property_title)
            locality = safe(instance.locality)
            city = safe(instance.city)
            price_raw = raw_number(getattr(instance, "monthly_rent", None))

            title = f"{pg_name} PG in {city}"

            description = seo_limit(
                f"Book verified PG and coliving accommodation in "
                f"{locality}, {city}."
            )

            keyword = f"PG in {city}"

            secondary_keywords = (
                f"boys pg in {city}, "
                f"girls pg in {city}"
            )

            intro_html = f"""
            <h1>{title}</h1>

            <p>
            Discover PG accommodation in
            {locality}, {city}.
            </p>
            """

            # FIXED: "Hostel" -> "RealEstateListing"
            schema = {
                "@type": "RealEstateListing",
                "name": pg_name,
                "description": description,
                "address": {
                    "@type": "PostalAddress",
                    "addressLocality": locality,
                    "addressRegion": city,
                    "addressCountry": "IN",
                },
            }

        # =====================================================
        # RESALE RESIDENTIAL
        # =====================================================

        elif page_type == "resale_residential":

            property_title = safe(instance.property_title)
            property_type = safe(instance.property_type)
            locality = safe(instance.locality)
            city = safe(instance.city)
            bhk = safe(instance.bhk)
            price = format_price(instance.selling_price)
            price_raw = raw_number(instance.selling_price)

            title = f"{bhk} {property_type} for Sale in {locality}, {city}"

            description = seo_limit(
                f"Buy verified {bhk} {property_type} in "
                f"{locality}, {city} at ₹{price}. "
                f"Premium residential property with modern amenities."
            )

            keyword = f"{bhk} property for sale in {city}"

            secondary_keywords = (
                f"flat for sale in {city}, "
                f"{property_type} for sale, "
                f"residential property in {locality}"
            )

            intro_html = f"""
            <h1>{title}</h1>

            <p>
            Explore premium {bhk} {property_type} for sale in
            {locality}, {city}.
            </p>
            """

            schema = {
                "@type": "RealEstateListing",
                "name": property_title,
                "description": description,
                "address": {
                    "@type": "PostalAddress",
                    "addressLocality": locality,
                    "addressRegion": city,
                    "addressCountry": "IN",
                },
            }

        # =====================================================
        # COMMERCIAL RESALE
        # =====================================================

        elif page_type == "commercial_resale":

            property_type = safe(instance.property_type)
            locality = safe(instance.locality)
            city = safe(instance.city)
            price = format_price(instance.selling_price)
            price_raw = raw_number(instance.selling_price)

            title = f"{property_type} Commercial Property for Sale in {city}"

            description = seo_limit(
                f"Commercial {property_type} available for sale in "
                f"{locality}, {city} at ₹{price}."
            )

            keyword = f"commercial property sale in {city}"

            secondary_keywords = (
                f"office for sale, "
                f"commercial investment"
            )

            intro_html = f"""
            <h1>{title}</h1>

            <p>
            Find commercial property for sale in
            {locality}, {city}.
            </p>
            """

            # FIXED: "Office" -> "RealEstateListing"
            schema = {
                "@type": "RealEstateListing",
                "name": title,
                "description": description,
                "address": {
                    "@type": "PostalAddress",
                    "addressLocality": locality,
                    "addressRegion": city,
                    "addressCountry": "IN",
                },
            }

        # =====================================================
        # PLOT SALE
        # =====================================================

        elif page_type == "plot_sale":

            plot_title = safe(instance.plot_title)
            locality = safe(instance.plot_locality)
            city = safe(instance.plot_city)
            price = format_price(instance.plot_price)
            price_raw = raw_number(instance.plot_price)

            title = f"Residential Plot for Sale in {locality}, {city}"

            description = seo_limit(
                f"Buy residential plot in {locality}, {city} at ₹{price}."
            )

            keyword = f"plot for sale in {city}"

            secondary_keywords = (
                f"land for sale, "
                f"residential plot"
            )

            intro_html = f"""
            <h1>{title}</h1>

            <p>
            Explore verified residential plots in
            {locality}, {city}.
            </p>
            """

            # FIXED: "Landform" -> "RealEstateListing" (Landform is for
            # geographic features like mountains, not a sellable listing type)
            schema = {
                "@type": "RealEstateListing",
                "name": plot_title,
                "description": description,
                "address": {
                    "@type": "PostalAddress",
                    "addressLocality": locality,
                    "addressRegion": city,
                    "addressCountry": "IN",
                },
            }

        # =====================================================
        # INDUSTRIAL SALE
        # =====================================================

        elif page_type == "industrial_sale":

            property_type = safe(instance.property_type)
            locality = safe(instance.locality)
            city = safe(instance.city)
            price = format_price(instance.selling_price)
            price_raw = raw_number(instance.selling_price)

            title = f"{property_type} Industrial Property in {city}"

            description = seo_limit(
                f"Industrial {property_type} available in "
                f"{locality}, {city} at ₹{price}."
            )

            keyword = f"industrial property in {city}"

            secondary_keywords = (
                f"warehouse sale, "
                f"factory property"
            )

            intro_html = f"""
            <h1>{title}</h1>

            <p>
            Explore industrial properties in
            {locality}, {city}.
            </p>
            """

            # NOTE: "IndustrialEstablishment" (a business, e.g. a running
            # factory) isn't right for a listing being sold either.
            schema = {
                "@type": "RealEstateListing",
                "name": title,
                "description": description,
                "address": {
                    "@type": "PostalAddress",
                    "addressLocality": locality,
                    "addressRegion": city,
                    "addressCountry": "IN",
                },
            }

        # =====================================================
        # AGRICULTURE SALE
        # =====================================================

        elif page_type == "agriculture_sale":

            locality = safe(instance.village)
            city = safe(instance.city)
            price = format_price(instance.selling_price)
            price_raw = raw_number(instance.selling_price)

            title = f"Agricultural Land for Sale in {locality}, {city}"

            description = seo_limit(
                f"Agricultural land available in {locality}, "
                f"{city} at ₹{price}."
            )

            keyword = f"agricultural land in {city}"

            secondary_keywords = (
                f"farm land sale, "
                f"orchard land"
            )

            intro_html = f"""
            <h1>{title}</h1>

            <p>
            Discover agricultural land in
            {locality}, {city}.
            </p>
            """

            schema = {
                "@type": "RealEstateListing",
                "name": title,
                "description": description,
                "address": {
                    "@type": "PostalAddress",
                    "addressLocality": locality,
                    "addressRegion": city,
                    "addressCountry": "IN",
                },
            }

        # =====================================================
        # RESIDENTIAL PLOT RESALE
        # =====================================================

        elif page_type == "residential_plot_resale":

            property_title = safe(instance.property_title)
            locality = safe(instance.locality)
            city = safe(instance.city)
            price = format_price(instance.selling_price)
            price_raw = raw_number(instance.selling_price)
            plot_area = safe(instance.plot_area)

            title = f"Residential Plot for Sale in {locality}, {city}"
            if property_title:
                title = property_title

            description = seo_limit(
                f"Buy residential plot in {locality}, {city} at ₹{price}. "
                f"Area: {plot_area} sq.ft. Premium residential land ready for construction."
            )

            keyword = f"residential plot for sale in {city}"

            secondary_keywords = (
                f"residential land for sale, "
                f"plot in {locality}"
            )

            intro_html = f"""
            <h1>{title}</h1>
            <p>
            Explore verified residential plots for sale in
            {locality}, {city}.
            </p>
            """

            schema = {
                "@type": "RealEstateListing",
                "name": title,
                "description": description,
                "address": {
                    "@type": "PostalAddress",
                    "addressLocality": locality,
                    "addressRegion": city,
                    "addressCountry": "IN",
                },
            }

        # =====================================================
        # COMMERCIAL PLOT RESALE
        # =====================================================

        elif page_type == "commercial_plot_resale":

            property_title = safe(instance.property_title)
            locality = safe(instance.locality)
            city = safe(instance.city)
            price = format_price(instance.selling_price)
            price_raw = raw_number(instance.selling_price)
            zone_type = safe(instance.commercial_zone_type)

            title = f"Commercial Plot for Sale in {locality}, {city}"
            if property_title:
                title = property_title

            description = seo_limit(
                f"Commercial plot available for sale in {locality}, {city} at ₹{price}. "
                f"Zone: {zone_type}. Ideal for business and retail development."
            )

            keyword = f"commercial plot for sale in {city}"

            secondary_keywords = (
                f"commercial land in {city}, "
                f"commercial property {locality}"
            )

            intro_html = f"""
            <h1>{title}</h1>
            <p>
            Find premium commercial plots for sale in
            {locality}, {city}.
            </p>
            """

            schema = {
                "@type": "RealEstateListing",
                "name": title,
                "description": description,
                "address": {
                    "@type": "PostalAddress",
                    "addressLocality": locality,
                    "addressRegion": city,
                    "addressCountry": "IN",
                },
            }

        # =====================================================
        # INDUSTRIAL PLOT RESALE
        # =====================================================

        elif page_type == "industrial_plot_resale":

            property_title = safe(instance.property_title)
            locality = safe(instance.locality)
            city = safe(instance.city)
            price = format_price(instance.selling_price)
            price_raw = raw_number(instance.selling_price)
            estate_name = safe(instance.industrial_estate_name)

            title = f"Industrial Plot for Sale in {locality}, {city}"
            if property_title:
                title = property_title

            description = seo_limit(
                f"Industrial plot for sale in {estate_name}, {locality}, {city} at ₹{price}. "
                f"Suitable for manufacturing and warehousing operations."
            )

            keyword = f"industrial plot for sale in {city}"

            secondary_keywords = (
                f"industrial land {locality}, "
                f"factory plot in {city}"
            )

            intro_html = f"""
            <h1>{title}</h1>
            <p>
            Explore verified industrial plots in
            {locality}, {city}.
            </p>
            """

            schema = {
                "@type": "RealEstateListing",
                "name": title,
                "description": description,
                "address": {
                    "@type": "PostalAddress",
                    "addressLocality": locality,
                    "addressRegion": city,
                    "addressCountry": "IN",
                },
            }

        # =====================================================
        # AGRICULTURAL PLOT RESALE
        # =====================================================

        elif page_type == "agricultural_plot_resale":

            property_title = safe(instance.property_title)
            locality = safe(instance.locality)
            city = safe(instance.city)
            price = format_price(instance.selling_price)
            price_raw = raw_number(instance.selling_price)
            area_unit = safe(instance.agr_area_unit)

            title = f"Agricultural Land for Sale in {locality}, {city}"
            if property_title:
                title = property_title

            description = seo_limit(
                f"Buy agricultural land in {locality}, {city} at ₹{price}. "
                f"Premium farmland measured in {area_unit}s available for cultivation."
            )

            keyword = f"agricultural land for sale in {city}"

            secondary_keywords = (
                f"farm land in {locality}, "
                f"agricultural plot {city}"
            )

            intro_html = f"""
            <h1>{title}</h1>
            <p>
            Discover agricultural land and farm plots in
            {locality}, {city}.
            </p>
            """

            schema = {
                "@type": "RealEstateListing",
                "name": title,
                "description": description,
                "address": {
                    "@type": "PostalAddress",
                    "addressLocality": locality,
                    "addressRegion": city,
                    "addressCountry": "IN",
                },
            }

        # =====================================================
        # BLOG
        # =====================================================

        elif page_type == "blog":

            blog_title = safe(instance.title)
            category = safe(instance.category)
            author = safe(instance.author)
            short_desc = safe(instance.short_description)
            pub_date = safe(instance.published_date)

            title_suffix = f" - {category}" if category else ""
            title = f"{blog_title}{title_suffix} | Real Estate Blog"

            description = seo_limit(
                short_desc if short_desc else f"Read expert insights about {blog_title}."
            )

            keyword = blog_title

            secondary_keywords = f"real estate blog, {category.lower() if category else 'property news'}"

            intro_html = f"""
            <h1>{title}</h1>
            """

            # BlogPosting is a valid, correct schema type — kept as-is.
            schema = {
                "@type": "BlogPosting",
                "headline": blog_title,
                "description": description,
                "author": {
                    "@type": "Person",
                    "name": author if author else "PropCRM Team"
                }
            }

            if pub_date:
                schema["datePublished"] = str(pub_date)

        # =====================================================
        # SERVICE
        # =====================================================

        elif page_type == "service":

            service_title = safe(instance.title)
            short_desc = safe(instance.short_description)
            category = safe(instance.category)

            title = f"{service_title} Property Service"

            description = seo_limit(
                short_desc if short_desc else f"Professional {service_title} services."
            )

            keyword = service_title

            cat_keyword = f", {category.replace('_', ' ')}" if category else ""
            secondary_keywords = f"property services{cat_keyword}"

            intro_html = f"""
            <h1>{title}</h1>
            """

            # Service is a valid, correct schema type — kept as-is.
            schema = {
                "@type": "Service",
                "name": service_title,
                "description": description,
            }

            if category:
                schema["category"] = category

        # =====================================================
        # SUBSCRIPTION
        # =====================================================

        elif page_type == "subscription":

            title = f"{safe(instance.package_name)} Subscription Plan"
            price_raw = raw_number(
                getattr(instance, "plan_offer_price", None) or getattr(instance, "plan_base_price", None)
            )

            description = seo_limit(
                f"Choose {safe(instance.package_name)} subscription plan."
            )

            keyword = safe(instance.package_name)

            secondary_keywords = "property subscription"

            intro_html = f"""
            <h1>{title}</h1>
            """

            # FIXED: bare "Offer" as top-level @type isn't standard usage —
            # "Product" with a nested "offers" is the correct schema.org pattern.
            schema = {
                "@type": "Product",
                "name": safe(instance.package_name),
                "description": description,
            }

        else:
            return

        # =====================================================
        # NEW: attach image + price/offers to schema where applicable
        # (kept out of each block above to avoid repeating this 14 times)
        # =====================================================

        if image_url:
            schema["image"] = image_url

        if price_raw:
            schema["offers"] = {
                "@type": "Offer",
                "price": price_raw,
                "priceCurrency": "INR",
                "availability": "https://schema.org/InStock",
            }

        # =====================================================
        # NEW: FAQ schema + canonical URL
        # =====================================================

        faq_schema = get_faq_schema(instance)

        # NEW: instance.id crashes for any model whose real primary key
        # field is named something else -- PlotSaleProperty's PK is
        # plot_property_id, not id, so this line previously raised
        # AttributeError for every plot-sale property (silently caught
        # by the try/except in signals.py, meaning those rows have
        # NEVER gotten an SEO record). instance.pk always resolves to
        # the correct primary key value regardless of its field name.
        canonical_url = build_canonical_url(page_type, instance.pk, slugify(title))
        final_schema = combine_schema(schema, faq_schema)

        # =====================================================
        # SAVE SEO
        # =====================================================

        key = f"{page_type}-{instance.pk}"

        LocationSEO.objects.update_or_create(

            key=key,

            defaults={

                "pagetype": page_type,

                "content_type": ContentType.objects.get_for_model(instance),

                "object_id": str(instance.pk),

                "meta_title": title[:255],

                "meta_description": description[:155],

                "primary_keyword": keyword,

                "secondary_keywords": secondary_keywords,

                "slug": slugify(title),

                # NEW: was always blank before
                "canonical_url": canonical_url,

                # NOW includes FAQPage schema via @graph when FAQs exist
                "schema_json": json.dumps(final_schema),

                "intro_html": intro_html,

                "is_active": True,
            }
        )

        print(f"SEO CREATED SUCCESSFULLY : {key}")

    except Exception as e:

        print("SEO ERROR :", str(e))
