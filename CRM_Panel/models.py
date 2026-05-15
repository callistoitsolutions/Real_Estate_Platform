from django.db import models


class PropertyEnquiry(models.Model):

    # ==========================================
    # USER DETAILS
    # ==========================================

    name = models.CharField(
        max_length=200
    )

    phone = models.CharField(
        max_length=20
    )

    email = models.EmailField(
        blank=True,
        null=True
    )

    message = models.TextField(
        blank=True,
        null=True
    )


    # ==========================================
    # PROPERTY DETAILS
    # ==========================================

    property_id = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    property_title = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )

    property_type = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    property_location = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )

    property_price = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )


    # ==========================================
    # SEO / SOURCE TRACKING
    # ==========================================

    lead_source = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    seo_slug = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )

    page_url = models.URLField(
        blank=True,
        null=True
    )

    user_ip = models.GenericIPAddressField(
        blank=True,
        null=True
    )

    user_device = models.TextField(
        blank=True,
        null=True
    )

    referrer_url = models.URLField(
        blank=True,
        null=True
    )


    # ==========================================
    # STATUS
    # ==========================================

    enquiry_status = models.CharField(

        max_length=50,

        choices=[

            ("New", "New"),
            ("Contacted", "Contacted"),
            ("Site Visit", "Site Visit"),
            ("Closed", "Closed"),
            ("Rejected", "Rejected"),

        ],

        default="New"

    )


    # ==========================================
    # DATES
    # ==========================================

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )


    def __str__(self):

        return f"{self.name} - {self.property_title}"