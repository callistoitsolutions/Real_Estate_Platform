from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from Admin_App.models import *



    

############### Contact Enquiries Table/Modal Starts Here #####################

class Contact_Enquiry(models.Model):
    contact_name = models.CharField(max_length=200,blank=True,null=True)
    contact_phone = models.CharField(max_length=200,blank=True,null=True)
    contact_email = models.CharField(max_length=20,blank=True,null=True)
    contact_city = models.CharField(max_length=20,blank=True,null=True)

    contact_en_title = models.CharField(max_length=100, blank=True,null=True)
    contact_en_type = models.CharField(max_length=100, blank=True,null=True)
    contact_start_budget = models.CharField(max_length=100, blank=True,null=True)
    contact_end_budget = models.CharField(max_length=100, blank=True,null=True)
    contact_message = models.TextField(blank=True,null=True)

    contact_mode = models.CharField(max_length=100, blank=True,null=True)
    contact_time = models.CharField(max_length=100, blank=True,null=True)

    contact_enquiry_date = models.DateField(blank=True,null=True)
    contact_enquiry_time = models.TimeField(blank=True,null=True)

    def __str__(self):
        return f"{self.contact_name} - {self.contact_phone} - {self.contact_en_title}"
    


############### Wishlist Property Modal Starts Here ###########################

class WishlistProperty(models.Model):

    # 1. The type of property (PG, Commercial, etc.)
    content_type = models.ForeignKey(
        ContentType, 
        on_delete=models.CASCADE, 
        null=True, 
        blank=True
    )
    
    # 2. The ID of that specific property
    object_id = models.PositiveIntegerField(null=True, blank=True)

    # 3. The Generic Foreign Key (Combines the two above)
    property_object = GenericForeignKey('content_type', 'object_id')

    # --- Your existing fields stay the same ---
    user = models.ForeignKey(User_Details,on_delete=models.CASCADE,blank=True,null=True
    )

    wishlist_date = models.DateField(blank=True,null=True)
    wishlist_time = models.TimeField(blank=True,null=True)
    
################## Wishlist Property Modal Ends Here ############################


############## Normal FAQ Modal Starts Here ################################

class NormalFAQ(models.Model):

    faq_question = models.CharField(max_length=200,blank=True,null=True)
    faq_answer = models.TextField(blank=True,null=True)

    faq_date = models.DateField(blank=True,null=True)
    faq_time = models.TimeField(blank=True,null=True)

############## Normal FAQ Modal Ends Here ############################



class BrandAd(models.Model):
    PLACEMENT_CHOICES = [
    ('leaderboard', 'Leaderboard Carousel (below hero)'),
    ('hero_strip', 'Hero Strip (inside hero, below search)'),
    ('native', 'Native Strip (brand card row)'),
    ('mid_banner', 'Mid-Content Banner (between sections)'),
    ('inline_card', 'Inline Listing Card (inside property grid)'),
    ('footer', 'Footer Banner'),
]
    brand_name = models.CharField(max_length=100)
    priority = models.IntegerField(default=0, help_text="Higher shows first within a placement")
    tagline = models.CharField(max_length=150, blank=True, help_text="Only used for Native Strip ads")
    logo = models.ImageField(upload_to='ads/logos/', blank=True, null=True, help_text="Square logo, used for Native Strip")
    banner_image = models.ImageField(upload_to='ads/banners/', blank=True, null=True, help_text="Wide banner, used for Leaderboard")
    click_url = models.URLField()
    placement = models.CharField(max_length=20, choices=PLACEMENT_CHOICES)
    start_date = models.DateField()
    end_date = models.DateField()
    impressions = models.PositiveIntegerField(default=0)
    clicks = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.brand_name} ({self.get_placement_display()})"

    class Meta:
        ordering = ['-created_at']




class SearchLog(models.Model):
    listing_type = models.CharField(max_length=10)   # rent / sale
    category = models.CharField(max_length=30)        # residential/commercial/...
    bhk = models.CharField(max_length=20, blank=True, null=True)
    sub = models.CharField(max_length=50, blank=True, null=True)
    area = models.CharField(max_length=100, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=['category', 'listing_type']),
            models.Index(fields=['created_at']),
        ]




class LocalityInsight(models.Model):
    city = models.CharField(max_length=100)
    locality = models.CharField(max_length=150)

    # "What is good here"
    connectivity_points = models.TextField(blank=True, null=True)   # semicolon-separated
    recreation_points = models.TextField(blank=True, null=True)
    education_health_points = models.TextField(blank=True, null=True)
    green_space_points = models.TextField(blank=True, null=True)

    # "What can be better"
    road_traffic_issues = models.TextField(blank=True, null=True)
    internal_road_issues = models.TextField(blank=True, null=True)
    civic_issues = models.TextField(blank=True, null=True)

    confidence = models.CharField(max_length=20, default="Medium")   # High/Medium/Low
    freshness_note = models.CharField(max_length=50, blank=True, null=True)

    is_active = models.BooleanField(default=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('city', 'locality')

    def get_good_points(self):
        pts = []
        def split(v): return [x.strip() for x in (v or "").split(";") if x.strip()]
        t = split(self.connectivity_points)
        if t: pts.append(", ".join(t[:3]) + " provide convenient connectivity to important city areas.")
        r = split(self.recreation_points)
        if r: pts.append(", ".join(r[:4]) + " provide shopping, recreation or leisure options nearby.")
        e = split(self.education_health_points)
        if e: pts.append(", ".join(e[:4]) + " provide access to education and healthcare facilities.")
        g = split(self.green_space_points)
        if g: pts.append(", ".join(g[:3]) + " offer options for outdoor activity and relaxation.")
        return pts

    def get_better_points(self):
        pts = []
        for field in [self.road_traffic_issues, self.internal_road_issues, self.civic_issues]:
            if field:
                first = field.split(";")[0].strip()
                if first: pts.append(first + ".")
        return pts


class LocalityPriceTrend(models.Model):
    city = models.CharField(max_length=100)
    locality = models.CharField(max_length=150)
    avg_rate_per_sqft = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    yoy_change_percent = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)  # +/-
    price_range_min = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    price_range_max = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    # Monthly series for the chart, stored as JSON: [{"month":"Jan 2022","rate":4500}, ...]
    trend_series = models.JSONField(blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('city', 'locality')
