from django.db.models.signals import post_save
from django.dispatch import receiver

from seo.seo_generator import create_dynamic_seo

from Main_App.models import *
from Admin_App.models import *


# =========================================
# RENTAL RESIDENTIAL
# =========================================

@receiver(post_save, sender=RentalResidentialProperty)
def rental_residential_seo(sender, instance, created, **kwargs):

    create_dynamic_seo(
        instance,
        "rental_residential"
    )


# =========================================
# COMMERCIAL RENTAL
# =========================================

@receiver(post_save, sender=CommercialRentalProperty)
def commercial_rental_seo(sender, instance, created, **kwargs):

    create_dynamic_seo(
        instance,
        "commercial_rental"
    )


# =========================================
# PG
# =========================================

@receiver(post_save, sender=PGColivingProperty)
def pg_seo(sender, instance, created, **kwargs):

    create_dynamic_seo(
        instance,
        "pg_coliving"
    )


# =========================================
# BLOG
# =========================================

@receiver(post_save, sender=Blog)
def blog_seo(sender, instance, created, **kwargs):

    create_dynamic_seo(
        instance,
        "blog"
    )


# =========================================
# SERVICE
# =========================================

@receiver(post_save, sender=Service)
def service_seo(sender, instance, created, **kwargs):

    create_dynamic_seo(
        instance,
        "service"
    )


# =========================================
# SUBSCRIPTION
# =========================================

@receiver(post_save, sender=Subscription_Details)
def subscription_seo(sender, instance, created, **kwargs):

    create_dynamic_seo(
        instance,
        "subscription"
    )