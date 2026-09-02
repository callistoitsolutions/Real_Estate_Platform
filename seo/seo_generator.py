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
            locality_area = safe(instance.locality_area)
            city = safe(instance.city)
            rent = format_price(instance.monthly_rent)

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
            locality = safe(instance.locality) # FIXED: Changed from area_locality to locality
            city = safe(instance.city)
            rent = format_price(instance.monthly_rent) # FIXED: Changed from expected_rent to monthly_rent

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

            pg_name = safe(instance.property_title) # FIXED: Changed from pg_name to property_title
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

            property_title = safe(instance.property_title) # FIXED: Changed from title to property_title
            property_type = safe(instance.property_type)
            locality = safe(instance.locality)
            city = safe(instance.city)
            bhk = safe(instance.bhk)
            price = format_price(instance.selling_price) # FIXED: Changed from expected_price to selling_price

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
            price = format_price(instance.selling_price) # FIXED: expected_price to selling_price

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
            price = format_price(instance.selling_price) # FIXED: expected_price to selling_price

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
            price = format_price(instance.selling_price) # FIXED: expected_price to selling_price

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
        # RESIDENTIAL PLOT RESALE
        # =====================================================

        elif page_type == "residential_plot_resale":

            property_title = safe(instance.property_title)
            locality = safe(instance.locality)
            city = safe(instance.city)
            price = format_price(instance.selling_price)
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
                "@context": "https://schema.org",
                "@type": "Landform",
                "name": title,
                "description": description,
            }

        # =====================================================
        # COMMERCIAL PLOT RESALE
        # =====================================================

        elif page_type == "commercial_plot_resale":

            property_title = safe(instance.property_title)
            locality = safe(instance.locality)
            city = safe(instance.city)
            price = format_price(instance.selling_price)
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
                "@context": "https://schema.org",
                "@type": "Landform",
                "name": title,
                "description": description,
            }

        # =====================================================
        # INDUSTRIAL PLOT RESALE
        # =====================================================

        elif page_type == "industrial_plot_resale":

            property_title = safe(instance.property_title)
            locality = safe(instance.locality)
            city = safe(instance.city)
            price = format_price(instance.selling_price)
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
                "@context": "https://schema.org",
                "@type": "Landform",
                "name": title,
                "description": description,
            }

        # =====================================================
        # AGRICULTURAL PLOT RESALE
        # =====================================================

        elif page_type == "agricultural_plot_resale":

            property_title = safe(instance.property_title)
            locality = safe(instance.locality)
            city = safe(instance.city)
            price = format_price(instance.selling_price)
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
                "@context": "https://schema.org",
                "@type": "Landform",
                "name": title,
                "description": description,
            }

        # =====================================================
        # BLOG
        # =====================================================

        # =====================================================
        # BLOG
        # =====================================================

        elif page_type == "blog":

            blog_title = safe(instance.title)
            category = safe(instance.category)
            author = safe(instance.author)
            short_desc = safe(instance.short_description)
            pub_date = safe(instance.published_date)

            # Dynamically add category to the title if it exists
            title_suffix = f" - {category}" if category else ""
            title = f"{blog_title}{title_suffix} | Real Estate Blog"

            # Use the newly added short_description for better SEO
            description = seo_limit(
                short_desc if short_desc else f"Read expert insights about {blog_title}."
            )

            keyword = blog_title

            secondary_keywords = f"real estate blog, {category.lower() if category else 'property news'}"

            intro_html = f"""
            <h1>{title}</h1>
            """

            # Enrich the schema with author and publish date for rich search results
            schema = {
                "@context": "https://schema.org",
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

            # Use the newly added short_description for better SEO
            description = seo_limit(
                short_desc if short_desc else f"Professional {service_title} services."
            )

            keyword = service_title

            # Include category in secondary keywords
            cat_keyword = f", {category.replace('_', ' ')}" if category else ""
            secondary_keywords = f"property services{cat_keyword}"

            intro_html = f"""
            <h1>{title}</h1>
            """

            schema = {
                "@context": "https://schema.org",
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

                "object_id": str(instance.id), # ensuring object_id is saved as a string to accommodate character-based UUIDs

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