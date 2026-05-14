import json

from django.contrib.contenttypes.models import ContentType
from django.utils.text import slugify

from seo.models import LocationSEO


def create_dynamic_seo(instance, page_type):

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

        title = f"{instance.property_title} for Rent in {instance.locality}, {instance.city} | {instance.bhk_type} Rental Property"

        description = (
            f"Find {instance.bhk_type} {instance.property_type} for rent in "
            f"{instance.locality}, {instance.city}. "
            f"Monthly Rent ₹{instance.monthly_rent}. "
            f"{instance.furnishing_status} property with "
            f"{instance.bathrooms} bathrooms."
        )

        keyword = f"{instance.bhk_type} property for rent in {instance.city}"

        secondary_keywords = (
            f"rental property in {instance.locality}, "
            f"flat for rent in {instance.city}, "
            f"{instance.property_type} for rent, "
            f"house rent, rental listing"
        )

        intro_html = f"""
        <h1>{instance.property_title}</h1>

        <p>
        Premium {instance.bhk_type} rental property available in
        {instance.locality}, {instance.city}.
        Monthly Rent ₹{instance.monthly_rent}.
        </p>
        """

        schema = {
            "@context": "https://schema.org",
            "@type": "Residence",
            "name": instance.property_title,
            "address": instance.address,
            "description": description
        }

    # =====================================================
    # COMMERCIAL RENTAL
    # =====================================================

    elif page_type == "commercial_rental":

        title = f"{instance.property_type} for Rent in {instance.city} | Commercial Space"

        description = (
            f"Commercial {instance.property_type} available in "
            f"{instance.area_locality}, {instance.city}. "
            f"Expected Rent ₹{instance.expected_rent}. "
            f"Builtup Area {instance.builtup_area} sqft."
        )

        keyword = f"commercial property for rent in {instance.city}"

        secondary_keywords = (
            f"office for rent, shop for rent, "
            f"commercial property in {instance.city}"
        )

        intro_html = f"""
        <h1>{instance.property_type} in {instance.city}</h1>
        """

        schema = {
            "@context": "https://schema.org",
            "@type": "Office",
            "name": instance.property_type,
            "description": description
        }

    # =====================================================
    # PG / COLIVING
    # =====================================================

    elif page_type == "pg_coliving":

        title = f"{instance.pg_name} PG in {instance.city} | Co-Living Space"

        description = (
            f"Book PG/Co-living in {instance.locality}, {instance.city}. "
            f"Sharing Type: {instance.sharing_type}. "
            f"Furnishing: {instance.furnishing_type}."
        )

        keyword = f"PG in {instance.city}"

        secondary_keywords = (
            f"boys pg, girls pg, coliving space, "
            f"student pg in {instance.city}"
        )

        intro_html = f"""
        <h1>{instance.pg_name}</h1>
        """

        schema = {
            "@context": "https://schema.org",
            "@type": "Hostel",
            "name": instance.pg_name,
            "description": description
        }

    # =====================================================
    # BLOG
    # =====================================================

    elif page_type == "blog":

        title = f"{instance.title} | Real Estate Blog"

        description = (
            f"Read complete insights about {instance.title}. "
            f"Latest real estate trends and property investment tips."
        )

        keyword = instance.title

        secondary_keywords = (
            "real estate blog, property blog, rental tips"
        )

        intro_html = f"""
        <h1>{instance.title}</h1>
        """

        schema = {
            "@context": "https://schema.org",
            "@type": "BlogPosting",
            "headline": instance.title
        }

    # =====================================================
    # SERVICE
    # =====================================================

    elif page_type == "service":

        title = f"{instance.title} | Property Service"

        description = (
            f"Professional property service for "
            f"{instance.title}."
        )

        keyword = f"{instance.title} service"

        secondary_keywords = (
            "property management, real estate services"
        )

        intro_html = f"""
        <h1>{instance.title}</h1>
        """

        schema = {
            "@context": "https://schema.org",
            "@type": "Service",
            "name": instance.title
        }

    # =====================================================
    # SUBSCRIPTION
    # =====================================================

    elif page_type == "subscription":

        title = f"{instance.package_name} Subscription Plan"

        description = (
            f"{instance.plan_type} subscription plan for "
            f"{instance.plan_for}. "
            f"Price ₹{instance.plan_offer_price}."
        )

        keyword = f"{instance.package_name} subscription"

        secondary_keywords = (
            "property subscription plans, listing packages"
        )

        intro_html = f"""
        <h1>{instance.package_name}</h1>
        """

        schema = {
            "@context": "https://schema.org",
            "@type": "Offer",
            "name": instance.package_name
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

            "meta_description": description,

            "primary_keyword": keyword,

            "secondary_keywords": secondary_keywords,

            "slug": slugify(title),

            "schema_json": json.dumps(schema),

            "intro_html": intro_html,

            "is_active": True,
        }
    )