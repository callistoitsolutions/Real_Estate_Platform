import json

from django.contrib.contenttypes.models import ContentType
from django.utils.text import slugify

from seo.models import LocationSEO


# =========================================================
# SAFE FIELD
# =========================================================

def safe(value):

    if value is None:
        return ""

    return str(value).strip()


# =========================================================
# FORMAT PRICE
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
# LIMIT SEO DESCRIPTION
# =========================================================

def seo_limit(text, limit=155):

    text = " ".join(str(text).split())

    if len(text) <= limit:
        return text

    return text[:limit].rsplit(" ", 1)[0] + "..."


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

        # =====================================================
        # RENTAL RESIDENTIAL
        # =====================================================

        if page_type == "rental_residential":

            bhk = safe(instance.bhk_type)
            property_type = safe(instance.property_type)
            locality = safe(instance.locality)
            city = safe(instance.city)
            rent = format_price(instance.monthly_rent)

            title = f"{bhk} {property_type} for Rent in {locality}, {city}"

            description = seo_limit(
                f"Premium {bhk} {property_type} available for rent in "
                f"{locality}, {city}. Monthly rent ₹{rent}. "
                f"Explore verified rental homes with modern amenities."
            )

            keyword = f"{bhk} property for rent in {city}"

            secondary_keywords = (
                f"flat for rent in {city}, "
                f"{property_type} rent, "
                f"rental homes in {locality}"
            )

            intro_html = f"""
            <h1>{title}</h1>

            <p>
            Find premium {bhk} {property_type} for rent in
            {locality}, {city}.
            </p>
            """

            schema = {
                "@context": "https://schema.org",
                "@type": "Residence",
                "name": title,
                "description": description,
            }

        # =====================================================
        # COMMERCIAL RENTAL
        # =====================================================

        elif page_type == "commercial_rental":

            property_type = safe(instance.property_type)
            locality = safe(instance.area_locality)
            city = safe(instance.city)
            rent = format_price(instance.expected_rent)

            title = f"{property_type} for Rent in {locality}, {city}"

            description = seo_limit(
                f"Commercial {property_type} available for rent in "
                f"{locality}, {city}. Expected rent ₹{rent}."
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

            schema = {
                "@context": "https://schema.org",
                "@type": "Office",
                "name": title,
                "description": description,
            }

        # =====================================================
        # PG COLIVING
        # =====================================================

        elif page_type == "pg_coliving":

            pg_name = safe(instance.pg_name)
            locality = safe(instance.locality)
            city = safe(instance.city)

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

            schema = {
                "@context": "https://schema.org",
                "@type": "Hostel",
                "name": pg_name,
                "description": description,
            }

        # =====================================================
        # RESALE RESIDENTIAL
        # =====================================================

        elif page_type == "resale_residential":

            property_title = safe(instance.title)
            property_type = safe(instance.property_type)
            locality = safe(instance.locality)
            city = safe(instance.city)
            bhk = safe(instance.bhk)
            price = format_price(instance.expected_price)

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
                "@context": "https://schema.org",
                "@type": "Residence",
                "name": property_title,
                "description": description,
                "address": {
                    "@type": "PostalAddress",
                    "addressLocality": locality,
                    "addressRegion": city,
                    "addressCountry": "India"
                }
            }

        # =====================================================
        # COMMERCIAL RESALE
        # =====================================================

        elif page_type == "commercial_resale":

            property_type = safe(instance.property_type)
            locality = safe(instance.locality)
            city = safe(instance.city)
            price = format_price(instance.expected_price)

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

            schema = {
                "@context": "https://schema.org",
                "@type": "Office",
                "name": title,
                "description": description,
            }

        # =====================================================
        # PLOT SALE
        # =====================================================

        elif page_type == "plot_sale":

            plot_title = safe(instance.plot_title)
            locality = safe(instance.plot_locality)
            city = safe(instance.plot_city)
            price = format_price(instance.plot_price)

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

            schema = {
                "@context": "https://schema.org",
                "@type": "Landform",
                "name": plot_title,
                "description": description,
            }

        # =====================================================
        # INDUSTRIAL SALE
        # =====================================================

        elif page_type == "industrial_sale":

            property_type = safe(instance.property_type)
            locality = safe(instance.locality)
            city = safe(instance.city)
            price = format_price(instance.expected_price)

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

            schema = {
                "@context": "https://schema.org",
                "@type": "IndustrialEstablishment",
                "name": title,
                "description": description,
            }

        # =====================================================
        # AGRICULTURE SALE
        # =====================================================

        elif page_type == "agriculture_sale":

            locality = safe(instance.village)
            city = safe(instance.city)
            price = format_price(instance.expected_price)

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
                "@context": "https://schema.org",
                "@type": "Landform",
                "name": title,
                "description": description,
            }

        # =====================================================
        # BLOG
        # =====================================================

        elif page_type == "blog":

            title = f"{safe(instance.title)} | Real Estate Blog"

            description = seo_limit(
                f"Read expert insights about {safe(instance.title)}."
            )

            keyword = safe(instance.title)

            secondary_keywords = "real estate blog"

            intro_html = f"""
            <h1>{title}</h1>
            """

            schema = {
                "@context": "https://schema.org",
                "@type": "BlogPosting",
                "headline": safe(instance.title),
                "description": description,
            }

        # =====================================================
        # SERVICE
        # =====================================================

        elif page_type == "service":

            title = f"{safe(instance.title)} Property Service"

            description = seo_limit(
                f"Professional {safe(instance.title)} services."
            )

            keyword = safe(instance.title)

            secondary_keywords = "property services"

            intro_html = f"""
            <h1>{title}</h1>
            """

            schema = {
                "@context": "https://schema.org",
                "@type": "Service",
                "name": safe(instance.title),
                "description": description,
            }

        # =====================================================
        # SUBSCRIPTION
        # =====================================================

        elif page_type == "subscription":

            title = f"{safe(instance.package_name)} Subscription Plan"

            description = seo_limit(
                f"Choose {safe(instance.package_name)} subscription plan."
            )

            keyword = safe(instance.package_name)

            secondary_keywords = "property subscription"

            intro_html = f"""
            <h1>{title}</h1>
            """

            schema = {
                "@context": "https://schema.org",
                "@type": "Offer",
                "name": safe(instance.package_name),
                "description": description,
            }

        else:
            return

        # =====================================================
        # SAVE SEO
        # =====================================================

        key = f"{page_type}-{instance.id}"

        LocationSEO.objects.update_or_create(

            key=key,

            defaults={

                "pagetype": page_type,

                "content_type": ContentType.objects.get_for_model(instance),

                "object_id": instance.id,

                "meta_title": title[:255],

                "meta_description": description[:155],

                "primary_keyword": keyword,

                "secondary_keywords": secondary_keywords,

                "slug": slugify(title),

                "schema_json": json.dumps(schema),

                "intro_html": intro_html,

                "is_active": True,
            }
        )

        print(f"SEO CREATED SUCCESSFULLY : {key}")

    except Exception as e:

        print("SEO ERROR :", str(e))