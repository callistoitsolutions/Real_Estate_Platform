from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.contrib.auth.models import User
from django.utils.text import slugify

# Create your models here.
class Agent(models.Model):
    agency_name = models.CharField(max_length=200)
    contact_person = models.CharField(max_length=200)
    mobile = models.CharField(max_length=20)
    email = models.EmailField(blank=True)
    rera_registration_no = models.CharField(max_length=100, blank=True)
    office_address = models.TextField(blank=True)
    properties_managed = models.PositiveIntegerField(null=True, blank=True)
    service_areas = models.CharField(max_length=255, blank=True)
    subscription_plan = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.agency_name
    

############### Contact Enquiries Table/Modal Starts Here #####################

class Contact_Enquiry(models.Model):
    contact_name = models.CharField(max_length=200)
    contact_phone = models.CharField(max_length=200)
    contact_email = models.CharField(max_length=20)
    contact_en_title = models.CharField(max_length=100, blank=True)
    contact_message = models.TextField(blank=True)

    contact_enquiry_date = models.DateField(blank=True,null=True)
    contact_enquiry_time = models.TimeField(blank=True,null=True)

    def __str__(self):
        return f"{self.contact_name} - {self.contact_phone} - {self.contact_en_title}"
    
    
    


    
    
    
    
    


from django.utils import timezone

from django.contrib.auth.models import AbstractUser, Group, Permission





    
    

    
    
from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

# -------------------
# Custom User
# -------------------


# ========== USER SYSTEM ==========
ROLE_CHOICES = [
    ('tenant', 'Tenant'),
    ('landlord', 'Landlord / Owner'),
    ('broker', 'Broker / Agent / Agency'),
]

REFERRAL_CHOICES = [
    ('direct', 'Direct'),
    ('referral', 'Referral'),
]

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=30, choices=ROLE_CHOICES, default='tenant')
    referral_source = models.CharField(max_length=20, choices=REFERRAL_CHOICES, default='direct')
    mobile_number = models.CharField(max_length=20, blank=True, null=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return f"{self.username} ({self.role})"


class SignupDraft(models.Model):
    full_name = models.CharField(max_length=255)
    email = models.EmailField()
    role = models.CharField(max_length=30, choices=ROLE_CHOICES)
    referral_source = models.CharField(max_length=50, choices=REFERRAL_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)

    def __str__(self):
        return f"{self.full_name} - {self.email}"


# ========== LEAD CAPTURE ==========


import uuid
from django.utils.timezone import now
from datetime import date

class LeadCapture(models.Model):
    INTENT_CHOICES = (
        ("rent_lease", "Rent / Lease"),
        ("resale", "Resale Property"),
    )

    PROPERTY_CATEGORY_CHOICES = (
        ("residential", "Residential Property"),
        ("commercial", "Commercial Property"),
        ("industrial", "Industrial Property"),
        ("agricultural", "Agricultural Land"),
        ("open_plot", "Open Plot"),
        ("pg", "PG / Hostel"),
    )

    lead_id = models.CharField(max_length=20, unique=True, editable=False, null=True, blank=True)

    name = models.CharField(max_length=255)
    email = models.EmailField()
    designation = models.CharField(max_length=30, choices=ROLE_CHOICES, default="")
    intent_type = models.CharField(max_length=20, choices=INTENT_CHOICES, default="")
    property_category = models.CharField(max_length=50, choices=PROPERTY_CATEGORY_CHOICES, blank=True, null=True)
    property_subtype = models.CharField(max_length=100, blank=True, null=True)
    message = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        # Auto-generate unique Lead ID only on first save
        if not self.lead_id:
            self.lead_id = f"LEAD-{uuid.uuid4().hex[:8].upper()}"
        super().save(*args, **kwargs)

    @property
    def age_in_days(self):
        """Return age of lead in days"""
        if self.created_at:
            return (now().date() - self.created_at.date()).days
        return 0

    def __str__(self):
        return f"{self.lead_id} – {self.name}"





class ResaleProperty(models.Model):
    # Link to the user who posted the property (optional)
    posted_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    lead = models.ForeignKey(LeadCapture, on_delete=models.CASCADE, null=True, blank=True)
    # User designation
    DESIGNATION_CHOICES = [
        ('landlord', 'Landlord'),
        ('broker', 'Broker / Agent'),
    ]
    designation = models.CharField(max_length=20, choices=DESIGNATION_CHOICES)
    
    # Property type and location
    property_type = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    area_locality = models.CharField(max_length=150)
    property_address = models.TextField(blank=True)
    
    # Property details
    price = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    builtup_area = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    bedrooms = models.PositiveIntegerField(default=0)
    bathrooms = models.PositiveIntegerField(default=0)
    
    # Timestamp
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Optional fields you may want to add
    description = models.TextField(blank=True)
    is_featured = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.property_type} in {self.area_locality}, {self.city} - {self.price}"



# ========== PROPERTY MODELS ==========
PURPOSE_CHOICES = [
    ('Rent/Lease', 'Rent/Lease'),
    ('Sell', 'Sell'),
]




# ------------------- Residential Property -------------------
class ResidentialProperty(models.Model):
    posted_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    lead = models.ForeignKey(LeadCapture, on_delete=models.CASCADE, null=True, blank=True)


    property_title = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    area = models.CharField(max_length=100)
    property_address = models.TextField(null=True, blank=True)

    property_type = models.CharField(max_length=50,default="")
    builtup_area = models.FloatField()
    carpet_area = models.FloatField()
    zone = models.CharField(max_length=50,default="")
    society_type = models.CharField(max_length=50,default="")
    recommended_for = models.CharField(max_length=255, null=True, blank=True)

    bedrooms = models.IntegerField()
    bathrooms = models.IntegerField()
    balconies = models.IntegerField()
    furnishing = models.CharField(max_length=50)
    floor_no = models.IntegerField()
    total_floors = models.IntegerField()
    water_type = models.CharField(max_length=50,default="")
    age_of_property = models.IntegerField(default=0)


    # Rent Details
    rent_price = models.FloatField()
    security_deposit = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    maintenance = models.FloatField(default=0)

    # Featured & Verified
    is_featured = models.CharField(max_length=10, blank=True, null=True)
    featured_days = models.IntegerField(blank=True, null=True)
    manual_featured_days = models.IntegerField(blank=True, null=True)
    featured_start_date = models.DateField(blank=True, null=True)
    featured_end_date = models.DateField(blank=True, null=True)
    service_amount = models.FloatField(blank=True, null=True)
    placement = models.CharField(max_length=50, blank=True, null=True)
    is_verified = models.CharField(max_length=10, blank=True, null=True)

    # Files
    property_images = models.FileField(upload_to='property_images/', blank=True, null=True)
    floor_plan = models.FileField(upload_to='floor_plans/', blank=True, null=True)
    upload_registry = models.FileField(upload_to='documents/', blank=True, null=True)
    upload_house_tax = models.FileField(upload_to='documents/', blank=True, null=True)
    upload_utility_bill = models.FileField(upload_to='documents/', blank=True, null=True)
    upload_aadhar = models.FileField(upload_to='documents/', blank=True, null=True)
    upload_pan = models.FileField(upload_to='documents/', blank=True, null=True)
    upload_index2 = models.FileField(upload_to='documents/', blank=True, null=True)

    # Brokerage
    brokerage_applicable = models.CharField(max_length=10, blank=True, null=True)
    brokerage_payer = models.CharField(max_length=50, blank=True, null=True)
    brokerage_type = models.CharField(max_length=50, blank=True, null=True)
    brokerage_value = models.FloatField(blank=True, null=True)
    percentage_extra = models.FloatField(blank=True, null=True)
    brokerage_description = models.TextField(blank=True, null=True)

    # New Fields
    exclusive_property = models.BooleanField(default=False)
    upload_video = models.BooleanField(default=False)
    video_url = models.URLField(blank=True, null=True)
    video_from = models.DateField(blank=True, null=True)
    video_to = models.DateField(blank=True, null=True)
    video_platforms = models.CharField(max_length=255, blank=True, null=True)  # comma separated platforms
    
    nearby_facilities = models.CharField(max_length=255, blank=True, null=True)  # comma separated
    amenities = models.CharField(max_length=255, blank=True, null=True) 
    description = models.CharField(max_length=255, blank=True, null=True) 
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.property_title


  






# Residential Inquiry
class ResidentialInquiry(models.Model):
    residential_property = models.ForeignKey('ResidentialProperty', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    message = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    @property
    def lead_age(self):
        if self.residential_property.lead and self.residential_property.lead.created_at:
            delta = timezone.now() - self.residential_property.lead.created_at
            if delta.days == 0:
                return "Today"
            elif delta.days == 1:
                return "1 day"
            return f"{delta.days} days"
        return "N/A"

# Commercial Inquiry
class CommercialInquiry(models.Model):
    commercial_property = models.ForeignKey('CommercialProperty', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    message = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    
    @property
    def lead_age(self):
        if self.commercial_property.lead and self.commercial_property.lead.created_at:
            delta = timezone.now() - self.commercial_property.lead.created_at
            if delta.days == 0:
                return "Today"
            elif delta.days == 1:
                return "1 day"
            return f"{delta.days} days"
        return "N/A"

# PG / Co-living Inquiry
class PGInquiry(models.Model):
    pg_property = models.ForeignKey('PGProperty', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    message = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    
    @property
    def lead_age(self):
        if self.pg_property.lead and self.pg_property.lead.created_at:
            delta = timezone.now() - self.pg_property.lead.created_at
            if delta.days == 0:
                return "Today"
            elif delta.days == 1:
                return "1 day"
            return f"{delta.days} days"
        return "N/A"



# ------------------- Commercial Property -------------------
class CommercialProperty(models.Model):
    posted_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    lead = models.ForeignKey(LeadCapture, on_delete=models.CASCADE, null=True, blank=True)

    
    
    property_type = models.CharField(max_length=100, default="Not Specified")
    city = models.CharField(max_length=100)
    area_locality = models.CharField(max_length=200,default="")
    #property_address = models.TextField()
    property_address = models.TextField(null=True, blank=True)

    building_name = models.CharField(max_length=200, blank=True, null=True)
    possession_status = models.CharField(max_length=100, blank=True, null=True)
    age_of_property = models.IntegerField(default=0)
    zone_type = models.CharField(max_length=100, blank=True, null=True)
    location_hub = models.CharField(max_length=150, blank=True, null=True)
    property_condition = models.CharField(max_length=150, blank=True, null=True)
    ownership_type = models.CharField(max_length=150, blank=True, null=True)
    construction_status = models.CharField(max_length=150, blank=True, null=True)

    # --- Property Details ---
    builtup_area = models.IntegerField(default=0)
    carpet_area = models.IntegerField(default=0)
    total_floors = models.IntegerField(default=0)
    your_no = models.IntegerField(default=0)   # floor no
    no_of_staircase = models.IntegerField(default=0)
    passenger_lifts = models.IntegerField(default=0)
    service_lifts = models.IntegerField(default=0)
    private_parking = models.IntegerField(default=0)
    public_parking = models.IntegerField(default=0)
    minimum_seats = models.IntegerField(default=0)
    maximum_seats = models.IntegerField(default=0)
    number_of_cabin = models.IntegerField(default=0)
    meeting_room = models.IntegerField(default=0)
    floring_type = models.CharField(max_length=150, blank=True, null=True)

    # --- Rent Details ---
    expected_rent = models.FloatField(default=0)
    security_deposit = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    maintenance_charges = models.FloatField(default=0)
    rent_available_from = models.DateField(blank=True, null=True)
    lock_in_period = models.IntegerField(default=0)
    rent_increase = models.FloatField(default=0.0)

    # --- Uploads ---
    property_images = models.FileField(upload_to="property/images/", blank=True, null=True)
    floor_plan = models.FileField(upload_to="property/floor_plans/", blank=True, null=True)

    # --- Featured & Verified ---
    is_featured = models.BooleanField(default=False)
    featured_days = models.IntegerField(blank=True, null=True)
    manual_featured_days = models.IntegerField(blank=True, null=True)
    featured_start_date = models.DateField(blank=True, null=True)
    featured_end_date = models.DateField(blank=True, null=True)
    service_amount = models.FloatField(default=0.0)
    placement = models.CharField(max_length=50, blank=True, null=True)
    is_verified = models.BooleanField(default=False)

    # --- Documents ---
    upload_registry = models.FileField(upload_to="property/docs/", blank=True, null=True)
    upload_house_tax = models.FileField(upload_to="property/docs/", blank=True, null=True)
    upload_utility_bill = models.FileField(upload_to="property/docs/", blank=True, null=True)
    upload_aadhar = models.FileField(upload_to="property/docs/", blank=True, null=True)
    upload_pan = models.FileField(upload_to="property/docs/", blank=True, null=True)
    upload_index2 = models.FileField(upload_to="property/docs/", blank=True, null=True)

    # --- Brokerage ---
    brokerage_applicable = models.CharField(max_length=10, default="No")   # Yes/No
    brokerage_payer = models.CharField(max_length=50, blank=True, null=True)
    brokerage_type = models.CharField(max_length=50, blank=True, null=True)
    brokerage_value = models.FloatField(default=0.0)
    percentage_extra = models.FloatField(default=0.0)
    brokerage_description = models.TextField(blank=True, null=True)

    # --- Exclusive & Video ---
    exclusive_property = models.BooleanField(default=False)
    upload_video = models.BooleanField(default=False)
    video_url = models.URLField(blank=True, null=True)
    video_from = models.DateField(blank=True, null=True)
    video_to = models.DateField(blank=True, null=True)
    video_platforms = models.CharField(max_length=200, blank=True, null=True)

    # --- Facilities & Amenities ---
    nearby_facilities = models.TextField(blank=True, null=True)
    amenities = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.property_type} in {self.city} - {self.area_locality}"

  




# ------------------- PG / Co-living Property -------------------
class PGProperty(models.Model):
    posted_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    lead = models.ForeignKey(LeadCapture, on_delete=models.CASCADE, null=True, blank=True)


    property_type = models.CharField(max_length=50,default="")
    city = models.CharField(max_length=100)
    area_locality = models.CharField(max_length=200,default="")
    address = models.TextField(default="", blank=True)

    furnishing_type = models.CharField(max_length=50,default="")
    sharing_type = models.CharField(max_length=50)
    meals_included = models.BooleanField(default=False)
    meal_type = models.CharField(max_length=50, blank=True, null=True)
    minimum_stay = models.IntegerField(null=True, blank=True)

    available_from = models.DateField(blank=True, null=True)

    # Rent details
    rent_price = models.DecimalField(max_digits=10, decimal_places=2)
    security_deposit = models.DecimalField(max_digits=10, decimal_places=2, default=0)


    # Images / Documents
    property_images = models.FileField(upload_to="property_images/", blank=True, null=True)
    floor_plan = models.FileField(upload_to="floor_plans/", blank=True, null=True)

    # Featured & verified
    is_featured = models.CharField(max_length=10, choices=[("Yes", "Yes"), ("No", "No")], default="No")
    featured_days = models.IntegerField(blank=True, null=True)
    manual_featured_days = models.IntegerField(blank=True, null=True)
    featured_start_date = models.DateField(blank=True, null=True)
    featured_end_date = models.DateField(blank=True, null=True)
    service_amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    placement = models.CharField(max_length=50, blank=True, null=True)
    is_verified = models.CharField(max_length=10, choices=[("yes", "Yes"), ("no", "No")], default="no")

    # Verification docs
    upload_registry = models.FileField(upload_to="docs/", blank=True, null=True)
    upload_house_tax = models.FileField(upload_to="docs/", blank=True, null=True)
    upload_utility_bill = models.FileField(upload_to="docs/", blank=True, null=True)
    upload_aadhar = models.FileField(upload_to="docs/", blank=True, null=True)
    upload_pan = models.FileField(upload_to="docs/", blank=True, null=True)
    upload_index2 = models.FileField(upload_to="docs/", blank=True, null=True)

    # Brokerage
    brokerage_applicable = models.CharField(max_length=10, blank=True, null=True)
    brokeragePayer = models.CharField(max_length=50, blank=True, null=True)
    brokerageType = models.CharField(max_length=50, blank=True, null=True)
    brokerageValue = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    percentageExtra = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    brokerageDescription = models.TextField(blank=True, null=True)

    # Exclusive property
    exclusive_property = models.BooleanField(default=False)

    # Video
    upload_video = models.BooleanField(default=False)
    video_url = models.URLField(blank=True, null=True)
    video_from = models.DateField(blank=True, null=True)
    video_to = models.DateField(blank=True, null=True)
    video_platforms = models.CharField(max_length=200, blank=True, null=True)

    # Facilities & Amenities
    nearby_facilities = models.CharField(max_length=200, blank=True, null=True)
    amenities = models.CharField(max_length=200, blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)
   

    def __str__(self):
        return f"{self.property_type} - {self.city}"















from django.utils.text import slugify

class LandingPage(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    content = models.TextField()

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return f"/pages/{self.slug}/"

    def __str__(self):
        return self.title




class Page(models.Model):
    property_title = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    area = models.CharField(max_length=100)
    property_type = models.CharField(max_length=50, default="")
    bedrooms = models.IntegerField(default=0)
    rent_price = models.FloatField()
    description = models.TextField(blank=True)
    slug = models.SlugField(max_length=255, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.property_title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return f"/property/{self.pk}/{self.slug}/"

    def __str__(self):
        return self.property_title



