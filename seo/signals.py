from django.db.models.signals import post_save
from django.dispatch import receiver

from seo.seo_generator import create_dynamic_seo

from Main_App.models import *
from Admin_App.models import *


# =====================================================
# RENTAL RESIDENTIAL
# =====================================================

@receiver(post_save, sender=RentalResidentialProperty)
def rental_residential_seo(sender, instance, created, **kwargs):

    print("RENTAL RESIDENTIAL SIGNAL")

    try:

        create_dynamic_seo(instance, "rental_residential")

        print("RENTAL RESIDENTIAL SEO CREATED")

    except Exception as e:

        print("RENTAL RESIDENTIAL SEO ERROR:", str(e))


# =====================================================
# COMMERCIAL RENTAL
# =====================================================

@receiver(post_save, sender=CommercialRentalProperty)
def commercial_rental_seo(sender, instance, created, **kwargs):

    print("COMMERCIAL RENTAL SIGNAL")

    try:

        create_dynamic_seo(instance, "commercial_rental")

        print("COMMERCIAL RENTAL SEO CREATED")

    except Exception as e:

        print("COMMERCIAL RENTAL SEO ERROR:", str(e))


# =====================================================
# PG / COLIVING
# =====================================================

@receiver(post_save, sender=PGColivingProperty)
def pg_seo(sender, instance, created, **kwargs):

    print("PG SIGNAL")

    try:

        create_dynamic_seo(instance, "pg_coliving")

        print("PG SEO CREATED")

    except Exception as e:

        print("PG SEO ERROR:", str(e))


# =====================================================
# RESALE RESIDENTIAL
# =====================================================

@receiver(post_save, sender=ResaleResidentialProperty)
def resale_residential_seo(sender, instance, created, **kwargs):

    print("RESALE RESIDENTIAL SIGNAL")

    try:

        create_dynamic_seo(instance, "resale_residential")

        print("RESALE RESIDENTIAL SEO CREATED")

    except Exception as e:

        print("RESALE RESIDENTIAL SEO ERROR:", str(e))


# =====================================================
# COMMERCIAL RESALE
# =====================================================

@receiver(post_save, sender=CommercialResaleProperty)
def commercial_resale_seo(sender, instance, created, **kwargs):

    print("COMMERCIAL RESALE SIGNAL")

    try:

        create_dynamic_seo(instance, "commercial_resale")

        print("COMMERCIAL RESALE SEO CREATED")

    except Exception as e:

        print("COMMERCIAL RESALE SEO ERROR:", str(e))


# =====================================================
# PLOT SALE
# =====================================================

@receiver(post_save, sender=PlotSaleProperty)
def plot_sale_seo(sender, instance, created, **kwargs):

    print("PLOT SALE SIGNAL")

    try:

        create_dynamic_seo(instance, "plot_sale")

        print("PLOT SALE SEO CREATED")

    except Exception as e:

        print("PLOT SALE SEO ERROR:", str(e))


# =====================================================
# INDUSTRIAL SALE
# =====================================================

@receiver(post_save, sender=IndustrialResaleProperty)
def industrial_sale_seo(sender, instance, created, **kwargs):

    print("INDUSTRIAL SALE SIGNAL")

    try:

        create_dynamic_seo(instance, "industrial_sale")

        print("INDUSTRIAL SALE SEO CREATED")

    except Exception as e:

        print("INDUSTRIAL SALE SEO ERROR:", str(e))


# =====================================================
# AGRICULTURAL SALE
# =====================================================

@receiver(post_save, sender=AgriculturalResaleProperty)
def agricultural_sale_seo(sender, instance, created, **kwargs):

    print("AGRICULTURAL SALE SIGNAL")

    try:

        create_dynamic_seo(instance, "agriculture_sale")

        print("AGRICULTURAL SALE SEO CREATED")

    except Exception as e:

        print("AGRICULTURAL SALE SEO ERROR:", str(e))


# =====================================================
# BLOG
# =====================================================

@receiver(post_save, sender=Blog)
def blog_seo(sender, instance, created, **kwargs):

    print("BLOG SIGNAL")

    try:

        create_dynamic_seo(instance, "blog")

        print("BLOG SEO CREATED")

    except Exception as e:

        print("BLOG SEO ERROR:", str(e))


# =====================================================
# SERVICE
# =====================================================

@receiver(post_save, sender=Service)
def service_seo(sender, instance, created, **kwargs):

    print("SERVICE SIGNAL")

    try:

        create_dynamic_seo(instance, "service")

        print("SERVICE SEO CREATED")

    except Exception as e:

        print("SERVICE SEO ERROR:", str(e))


# =====================================================
# SUBSCRIPTION
# =====================================================

@receiver(post_save, sender=Subscription_Details)
def subscription_seo(sender, instance, created, **kwargs):

    print("SUBSCRIPTION SIGNAL")

    try:

        create_dynamic_seo(instance, "subscription")

        print("SUBSCRIPTION SEO CREATED")

    except Exception as e:

        print("SUBSCRIPTION SEO ERROR:", str(e))