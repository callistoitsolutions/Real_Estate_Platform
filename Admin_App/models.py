from django.db import models
from django.utils.timezone import now
from decimal import Decimal,InvalidOperation

import uuid
# 📂 Go to the VERY TOP of models.py
from django.db import models, transaction # 🚀 MAKE SURE ", transaction" IS ADDED HERE




import random

class SeoMetaTag(models.Model):
    page_name = models.CharField(max_length=60)
    meta_title = models.CharField(max_length=60)
    canonical_url = models.URLField(max_length=255, blank=True, null=True)
    meta_description = models.CharField(max_length=160)
    keywords = models.TextField(help_text="Comma-separated keywords", blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.page_name




class CommissionStructure(models.Model):
    # Foreign IDs (if you later connect with Lead/Agent/RM models)
    lead_id = models.CharField(max_length=50, blank=True, null=True)
    agent_id = models.CharField(max_length=50, blank=True, null=True)
    rm_id = models.CharField(max_length=50, blank=True, null=True)

    role = models.CharField(max_length=50, choices=[
        ('agent', 'Agent'),
        ('rm', 'Relationship Manager'),
    ])

    rate_type = models.CharField(max_length=50, choices=[
        ('percent', 'Percentage'),
        ('lumpsum', 'Lumpsum Amount'),
        ('fixed', 'Fixed Amount'),
    ])

    commission_value = models.DecimalField(max_digits=10, decimal_places=2)
    deduction = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)

    from_date = models.DateField()
    to_date = models.DateField()

    release_option = models.CharField(max_length=50, choices=[
        ('15th', 'Release on 15th of next month'),
        ('custom', 'Custom Date'),
        ('hold', 'Hold Payment'),
    ])
    custom_release_date = models.DateField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.role} - {self.rate_type} - {self.commission_value}"




    
    
class WhatsAppMessage(models.Model):
    phone_number = models.CharField(max_length=20)
    template = models.CharField(max_length=100)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.phone_number} - {self.template}"
    
    
class DynamicPage(models.Model):
    title = models.CharField(max_length=255)
    seo_meta = models.CharField(max_length=255)
    body = models.TextField()
    image = models.ImageField(upload_to='dynamic_pages/')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    
    
class BroadcastEmail(models.Model):
    subject = models.CharField(max_length=255)
    message = models.TextField()
    audience_segment = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Email to {self.audience_segment}: {self.subject}"
    
    
    
 

class HeroSection(models.Model):
    title = models.CharField(max_length=200)
    subtitle = models.TextField(blank=True)
    background_image = models.ImageField(upload_to="hero_images/")

    title_font_size = models.CharField(max_length=10, default="48px")
    subtitle_font_size = models.CharField(max_length=10, default="18px")
    text_color = models.CharField(max_length=20, default="#ffffff")
    overlay_color = models.CharField(max_length=20, default="#080808b3")

    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title





from django.utils.text import slugify

from ckeditor_uploader.fields import RichTextUploadingField



class Blog(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100, null=True, blank=True)
    featured_image = models.ImageField(upload_to="blog_images/")
    content = RichTextUploadingField()
    category = models.CharField(max_length=100, null=True, blank=True)  # ✅ FIX
    reading_time = models.CharField(max_length=50, null=True, blank=True)
    date_posted = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title







from ckeditor.fields import RichTextField

class Service(models.Model):
    title = models.CharField(max_length=200)
    icon = models.CharField(max_length=50, blank=True, help_text="Bootstrap icon class (e.g. bi bi-key)")
    short_description = models.TextField()
    content = RichTextField()   # CKEditor field
    featured_image = models.ImageField(upload_to="services/", blank=True, null=True)

    def __str__(self):
        return self.title





class AboutPage(models.Model):
    title = models.CharField(max_length=200)
    description = RichTextField(blank=True, null=True)

    intro_badge = models.CharField(max_length=100, blank=True, null=True)
    intro_heading = models.CharField(max_length=200, blank=True, null=True)
    intro_content = RichTextField(blank=True, null=True)

    founder_name = models.CharField(max_length=100, blank=True, null=True)
    founder_role = models.CharField(max_length=100, blank=True, null=True)
    founder_quote = models.TextField(blank=True, null=True)
    founder_image = models.ImageField(upload_to="about/founder/", blank=True, null=True)

    main_image = models.ImageField(upload_to="about/main/", blank=True, null=True)
    overlay_image = models.ImageField(upload_to="about/overlay/", blank=True, null=True)

    years_of_excellence = models.PositiveIntegerField(default=1)

    def __str__(self):
        return self.title or "About Page"





class Achievement(models.Model):
    icon_class = models.CharField(max_length=100, help_text="Bootstrap icon class, e.g., bi bi-key")
    number = models.PositiveIntegerField()
    suffix = models.CharField(max_length=10, blank=True, help_text="e.g., '+', '%', etc.")
    label = models.CharField(max_length=255)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.label







class PropertyFAQ(models.Model):

    PROPERTY_TYPES = (

        ("residential", "Residential"),
        ("commercial", "Commercial"),
        ("industrial", "Industrial"),
        ("plot", "Plot"),
        ("pg", "PG"),
        ("villa", "Villa"),
        ("coworking", "Coworking"),
        ("agriculture", "Agriculture"),

    )

    property_type = models.CharField(

        max_length=50,

        choices=PROPERTY_TYPES

    )

    question = models.CharField(max_length=500)

    answer = models.TextField()

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):

        return f"{self.property_type} - {self.question}"


class TimelineItem(models.Model):
    year = models.CharField(max_length=10)
    title = models.CharField(max_length=255)
    description = models.TextField()
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.year} - {self.title}"




class Ad(models.Model):
    title = models.CharField(max_length=200)
    category = models.CharField(max_length=100, blank=True)
    image = models.ImageField(upload_to="ads/")
    short_description = models.TextField()
    detail_content = RichTextField()  # CKEditor field
    badge_text = models.CharField(max_length=100, blank=True)
    badge_icon = models.CharField(max_length=50, default="bi bi-star")  # bootstrap icon class
    special_offer_title = models.CharField(max_length=200, blank=True)
    special_offer_description = RichTextField(blank=True)
    text_size_heading = models.CharField(max_length=10, default="1.6em")  # font size
    text_size_paragraph = models.CharField(max_length=10, default="1em")
    slug = models.SlugField(unique=True, blank=True, null=True)

    def __str__(self):
        return self.title



class Admin_Login(models.Model):

    name     = models.CharField(max_length=150, default="")
    email    = models.CharField(max_length=100, default="")
    password = models.CharField(max_length=100, default="")
    phone    = models.CharField(max_length=15, default="")
    role     = models.CharField(max_length=50, default="admin")

    def __str__(self):
        return str(self.email)
    

################ Active Visitors modal starts here ########################

######## Remove it in production ##############################
class ActiveVisitor(models.Model):
    session_key = models.CharField(max_length=255, unique=True)
    device_type = models.CharField(max_length=50) 
    last_seen = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.device_type} - {self.last_seen}"
    
############### Active Visitors modal ends here ##########################


################ Models start for ameneties details ########################
class Ameneties_Details(models.Model):
   
    amenties_icon = models.CharField(max_length=200,blank=True,null=True)
    amenties_name = models.CharField(max_length=200,blank=True,null=True)
    amenties_date = models.DateField(blank=True,null=True)
    amenties_time = models.TimeField(blank=True,null=True)

    def __str__(self):
        return str(self.amenties_name)+"-"+self.amenties_icon

########### Models end for ameneties details ###############################


############ Models starts for nearby facilities details #######################

class Facilities_Details(models.Model):
   
    facilities_icon = models.CharField(max_length=200,blank=True,null=True)
    facilities_name = models.CharField(max_length=200,blank=True,null=True)
    facilities_date = models.DateField(blank=True,null=True)
    facilities_time = models.TimeField(blank=True,null=True)

    def __str__(self):
        return str(self.facilities_name)+"-"+self.facilities_icon
    
############### Views end for nearby facilities details #############################


########### Models start for services type details of vendors ######################

class Service_Type_Details(models.Model):
   
    service_id = models.CharField(max_length=200,blank=True,null=True)
    service_name = models.CharField(max_length=200,blank=True,null=True)
    service_upload_date = models.DateField(blank=True,null=True)
    service_upload_time = models.TimeField(blank=True,null=True)

    def __str__(self):
        return str(self.service_id)+"-"+self.service_name
    
############## Models end for service type details of vendors ##########################


############### Models start for user details model ############################



class User_Details(models.Model):
   
    user_id = models.CharField(max_length=200,blank=True,null=True)
    user_name = models.CharField(max_length=200,blank=True,null=True)
    user_email = models.CharField(max_length=200,blank=True,null=True)
    user_phone = models.CharField(max_length=200,blank=True,null=True)
    user_state = models.CharField(max_length=200,blank=True,null=True)
    user_city = models.CharField(max_length=200,blank=True,null=True)
    user_address = models.TextField(blank=True,null=True)

    user_password = models.CharField(max_length=200,blank=True,null=True)
    user_profile = models.ImageField(upload_to="Profile/", blank=True, null=True)
    user_role = models.CharField(max_length=200,blank=True,null=True)

    user_agency_name = models.CharField(max_length=200,blank=True,null=True)
    user_license_number = models.CharField(max_length=200,blank=True,null=True)

    user_service_type = models.CharField(max_length=200,blank=True,null=True)
    user_company_name = models.CharField(max_length=200,blank=True,null=True)
    user_pan_number = models.CharField(max_length=200,blank=True,null=True)
    user_gstin_number = models.CharField(max_length=200,blank=True,null=True)

    user_operational_scope = models.CharField(max_length=10,default='all',null=True,blank=True)

    # This will store the comma-separated list of states or "ALL_INDIA"
    selected_regions = models.TextField(null=True, blank=True)

    user_register_date = models.DateField(blank=True,null=True)
    user_register_time = models.TimeField(blank=True,null=True)

    def __str__(self):
        return str(self.user_id)+"-"+self.user_name+"-"+self.user_role


############## Modal starts for subscription package details ###################

class Package_Details(models.Model):
   
    package_id = models.CharField(max_length=200,blank=True,null=True)
    package_name = models.CharField(max_length=200,blank=True,null=True)
    package_upload_date = models.DateField(blank=True,null=True)
    package_upload_time = models.TimeField(blank=True,null=True)

    def __str__(self):
        return str(self.package_id)+"-"+self.package_name

############# Modal starts for subscription plan type details ################

class Plan_Details(models.Model):
   
    plan_id = models.CharField(max_length=200,blank=True,null=True)
    plan_name = models.CharField(max_length=200,blank=True,null=True)
    plan_upload_date = models.DateField(blank=True,null=True)
    plan_upload_time = models.TimeField(blank=True,null=True)

    def __str__(self):
        return str(self.plan_id)+"-"+self.plan_name
    

########### Modal starts for subscription details model #########################


class Subscription_Details(models.Model):
   
    package_name = models.CharField(max_length=200,blank=True,null=True)
    plan_type = models.CharField(max_length=200,blank=True,null=True)
    plan_duration = models.CharField(max_length=200,blank=True,null=True)
    plan_for = models.CharField(max_length=200,blank=True,null=True)
    plan_base_price = models.CharField(max_length=200,blank=True,null=True)
    plan_offer_price = models.CharField(max_length=200,blank=True,null=True)
    plan_discount = models.CharField(max_length=200,blank=True,null=True)
    plan_max_listings = models.CharField(max_length=200,blank=True,null=True)

    plan_offer_start_date = models.DateField(blank=True,null=True)
    plan_offer_end_date = models.DateField(blank=True,null=True)
    plan_desc = models.TextField(blank=True, null=True)


    plan_upload_date = models.DateField(blank=True,null=True)
    plan_upload_time = models.TimeField(blank=True,null=True)

    def __str__(self):
        return str(self.package_name)+"-"+self.plan_type+"-"+self.plan_for

        
    

################################START MODEL SECTION OF THE RENTAL RESIDENTIAL LISTING####################







def generate_unique_rental_residential_id():
    return f"EFPRR-{uuid.uuid4().hex[:8].upper()}"


# ==========================================
# MAIN MODEL
# ==========================================

class RentalResidentialProperty(models.Model):

    id = models.CharField(
        max_length=20,
        primary_key=True,
        default=generate_unique_rental_residential_id,
        editable=False,
    )

    # =====================================================
    # LISTED BY  (Step 1, section 1 on the form)
    # =====================================================

    listing_type = models.CharField(max_length=100, blank=True, null=True)
    category = models.CharField(max_length=100, blank=True, null=True)


    listed_by_type = models.CharField(max_length=100, blank=True, null=True)
    assigned_to = models.CharField(max_length=50, blank=True, null=True)     # "id-role" value from dropdown, only if "other"
  

    listed_by_id = models.CharField(max_length=150, blank=True, null=True)
    listed_by_name = models.CharField(max_length=150, blank=True, null=True)
    listed_by_email = models.CharField(max_length=150, blank=True, null=True)
    listed_by_contact = models.CharField(max_length=20, blank=True, null=True)
    listed_by_role = models.CharField(max_length=100, blank=True, null=True) 
    
    property_unique_key = models.CharField(max_length=255, blank=True, null=True, db_index=True)
    duplicate_count = models.PositiveIntegerField(default=0)
    duplicate_group_id = models.CharField(max_length=255, blank=True, null=True, db_index=True)   # <-- drives the brokerage label

    # =====================================================
    # BASIC INFORMATION
    # =====================================================

    property_title = models.CharField(max_length=255, blank=True, null=True)   # auto-generated in save()

    property_type = models.CharField(max_length=100, blank=True, null=True)

    # INTERNAL ONLY — used for office verification, never shown publicly,
    # and deliberately excluded from property_title / description / FAQs.
    property_no = models.CharField(max_length=100, blank=True, null=True)
    bhk_type = models.CharField(max_length=100, blank=True, null=True)

    renting_option = models.CharField(max_length=50, blank=True, null=True)     # Full Property / Single Room / Shared Room

    built_up_area = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    bathrooms = models.IntegerField(blank=True, null=True)
    balconies = models.IntegerField(blank=True, null=True)

    building_configuration = models.CharField(max_length=20, blank=True, null=True)   # e.g. "G+3"
    total_floors = models.IntegerField(blank=True, null=True)

    facing_direction = models.CharField(max_length=50, blank=True, null=True)
    furnishing_status = models.CharField(max_length=50, blank=True, null=True)
    available_for = models.CharField(max_length=50, blank=True, null=True)

    # =====================================================
    # PROPERTY DETAILS
    # =====================================================

    carpet_area = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    city_zone = models.CharField(max_length=50, blank=True, null=True)
    ownership_type = models.CharField(max_length=50, blank=True, null=True)
    property_condition = models.CharField(max_length=50, blank=True, null=True)
    property_age = models.CharField(max_length=50, blank=True, null=True)
    wing_number = models.CharField(max_length=50, blank=True, null=True)
    building_name = models.CharField(max_length=200, blank=True, null=True)

    # =====================================================
    # AVAILABILITY & BROKERAGE
    # =====================================================

    availability_status = models.CharField(max_length=50, blank=True, null=True)
    available_from = models.DateField(blank=True, null=True)
    lease_duration = models.CharField(max_length=50, blank=True, null=True)

    # ONE column for the select value. The label shown above it on the
    # form ("Brokerage" / "Service Fee" / ...) is NOT stored here — see
    # get_brokerage_label() below. This is the only brokerage-related
    # column besides manual_brokerage.
    brokerage_percentage = models.CharField(max_length=30, blank=True, null=True)
    manual_brokerage = models.CharField(max_length=50, blank=True, null=True)   # only used if brokerage_percentage == "Fixed Amount"

    # =====================================================
    # PRICING DETAILS
    # =====================================================

    monthly_rent = models.BigIntegerField(blank=True, null=True)

    advance_rent_month = models.CharField(max_length=10, blank=True, null=True)   # "0".."11" or "fixed"
    advance_rent_amount = models.BigIntegerField(blank=True, null=True)           # only if advance_rent_month == "fixed"

    security_deposit_type = models.CharField(max_length=10, blank=True, null=True)  # "0".."11" or "fixed"
    security_deposit_amount = models.BigIntegerField(blank=True, null=True)          # only if security_deposit_type == "fixed"

    maintenance_type = models.CharField(max_length=50, blank=True, null=True)     # "Included in Rent" / "Extra"
    monthy_maintenance_amount = models.BigIntegerField(blank=True, null=True)     # only if maintenance_type == "Extra"

    total_move_in_cost = models.BigIntegerField(blank=True, null=True)

    # =====================================================
    # LOCATION DETAILS
    # =====================================================

    address = models.TextField(blank=True, null=True)
    city = models.CharField(max_length=150, blank=True, null=True)
    locality_area = models.CharField(max_length=150, blank=True, null=True)
    property_landmark = models.CharField(max_length=200, blank=True, null=True)
    state = models.CharField(max_length=150, blank=True, null=True)
    pincode = models.CharField(max_length=10, blank=True, null=True)
    main_road_connectivity = models.CharField(max_length=50, blank=True, null=True)
    google_maps_link = models.CharField(max_length=50, blank=True, null=True)
    latitude = models.CharField(max_length=50, blank=True, null=True)
    longitude = models.CharField(max_length=50, blank=True, null=True)

    # =====================================================
    # AMENITIES & FACILITIES
    # =====================================================

    amenities = models.TextField(blank=True, null=True)          # comma-separated, from amenities[]
    nearby_facilities = models.TextField(blank=True, null=True)  # comma-separated, from nearby_facilities[]

    # =====================================================
    # DESCRIPTION
    # =====================================================

    user_description = models.TextField(blank=True, null=True)         # user-entered, kept as-is
    description = models.TextField(blank=True, null=True)               # auto-generated on save()
    rent_residential_desc = models.TextField(blank=True, null=True)     # auto-generated on save()

    # =====================================================
    # MEDIA & LISTING STATUS
    # =====================================================

    listed_elsewhere = models.CharField(max_length=3, blank=True, null=True, default="No")
    portal_name = models.CharField(max_length=100, blank=True, null=True)

    # =====================================================
    # UPLOADED BY (system)
    # =====================================================

    uploaded_by_name = models.CharField(max_length=150, blank=True, null=True)
    uploaded_by_email = models.CharField(max_length=150, blank=True, null=True)
    uploaded_by_contact = models.CharField(max_length=20, blank=True, null=True)
    uploaded_by_role = models.CharField(max_length=100, blank=True, null=True)
    upload_file_name = models.CharField(max_length=255, blank=True, null=True)
    # Add this new field to store the actual file
    upload_file = models.FileField(upload_to='property_uploads/files/', blank=True, null=True)
   

    # =====================================================
    # STATUS
    # =====================================================

    is_deleted = models.BooleanField(default=False)
    is_duplicate = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(null=True, blank=True)
    deleted_by = models.CharField(max_length=150, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    listing_status = models.CharField(max_length=150, blank=True, null=True)
    approval_status = models.CharField(max_length=150, blank=True, null=True)

    # =====================================================
    # BROKERAGE LABEL — computed, never stored.
    # Mirrors updateBrokerageLabel(role) from the form's JS exactly.
    # =====================================================

    BROKERAGE_LABEL_MAP = {
        "admin": "EstateFlow Service Fee",
        "relationship manager": "Service Fee",
        "landlord": "Tenant Service Fee",
        "agent": "Brokerage",
        "agency/builder": "Service Fee",
        "builder": "Service Fee",
    }

   


    def get_brokerage_label(self):
        role = (self.listed_by_role or "").strip().lower()
        return self.BROKERAGE_LABEL_MAP.get(role, "Brokerage")   # default fallback


    def get_advance_rent_type_label(self):
        val = (self.advance_rent_month or "").strip()
        
        if val.lower() in ["fixed", "fixed amount"]:
            return "Fixed Amount"
            
        return val or "-"

    def get_security_deposit_type_label(self):
        val = (self.security_deposit_type or "").strip()
        
        if val.lower() in ["fixed", "fixed amount"]:
            return "Fixed Amount"
            
        return val or "-"
    def get_brokerage_display_value(self):
        """Returns the value that should sit next to the label — resolves
        the 'Fixed Amount' case to the manually typed figure."""
        if self.brokerage_percentage == "Fixed Amount":
            return self.manual_brokerage or "-"
        return self.brokerage_percentage or "-"

    def get_brokerage_display_value(self):
        """Returns the value that should sit next to the label — resolves
        the 'Fixed Amount' case to the manually typed figure."""
        if self.brokerage_percentage == "Fixed Amount":
            return self.manual_brokerage or "-"
        return self.brokerage_percentage or "-"

    # =====================================================
    # DERIVED MONEY HELPERS (month-based vs fixed selects)
    # =====================================================

    def get_advance_rent_amount(self):
        rent = self.monthly_rent or 0
        raw = (self.advance_rent_month or "").strip().lower()

        # 1. If explicitly set to Fixed Amount, use the fixed value
        if raw in ["fixed", "fixed amount"]:
            return self.advance_rent_amount or 0

        # 2. Try to calculate based on the dropdown string (e.g., "1 Month Rent")
        try:
            months = int(raw.split()[0])
            return months * rent
        except (TypeError, ValueError, IndexError):
            # 3. Final fallback ONLY if the dropdown value is unrecognized
            return self.advance_rent_amount or 0

    def get_security_deposit_amount(self):
        rent = self.monthly_rent or 0
        raw = (self.security_deposit_type or "").strip().lower()

        # 1. If explicitly set to Fixed Amount, use the fixed value
        if raw in ["fixed", "fixed amount"]:
            return self.security_deposit_amount or 0

        # 2. Try to calculate based on the dropdown string (e.g., "2 Months Rent")
        try:
            months = int(raw.split()[0])
            return months * rent
        except (TypeError, ValueError, IndexError):
            # 3. Final fallback ONLY if the dropdown value is unrecognized
            return self.security_deposit_amount or 0



    def get_brokerage_amount(self):
        rent = self.monthly_rent or 0
        choice = (self.brokerage_percentage or "").strip().lower()
        has_manual = self.manual_brokerage not in (None, "", "0", 0)

        if choice == "no brokerage":
            return 0
        elif choice == "15 days rent":
            return rent / 2
        elif choice == "1 month rent":
            return rent
        elif choice == "2 months rent":
            return rent * 2
        elif choice in ("fixed amount", "negotiable") or (has_manual and choice not in
                ("no brokerage", "15 days rent", "1 month rent", "2 months rent")):
            # explicit fixed/negotiable, OR the preset is blank/unrecognized but a
            # manual figure was typed in anyway — use it rather than silently dropping it
            try:
                return float(self.manual_brokerage or 0)
            except (TypeError, ValueError):
                return 0
        else:
            return 0

    def calculate_move_in_cost(self):
        advance = self.get_advance_rent_amount()
        deposit = self.get_security_deposit_amount()
        brokerage = self.get_brokerage_amount()

        maintenance = 0
        m_type = (self.maintenance_type or "").strip().lower()
        has_maint_amount = self.monthy_maintenance_amount not in (None, 0, "", "0")

        if "extra" in m_type or "exclud" in m_type or (has_maint_amount and "included" not in m_type):
            # matches "Extra", or common typos/variants like "Excluding"/"Exluding",
            # or type is blank/unrecognized but an amount was typed in anyway
            maintenance = self.monthy_maintenance_amount or 0

        total = advance + deposit + brokerage + maintenance
        self.total_move_in_cost = round(total)

    # =====================================================
    # AUTO DESCRIPTION GENERATOR
    # =====================================================

    def generate_auto_descriptions(self):
        # NOTE: property_no is intentionally NEVER used below —
        # it's internal-only and must not leak into public text.

        p_type = self.property_type or "property"
        renting = f" ({self.renting_option})" if self.renting_option else ""
        locality = self.locality_area or "a prime location"
        city_str = f", {self.city}" if self.city else ""
        furnishing = self.furnishing_status or "comfortable"
        available_for = self.available_for or "tenants"
        possession = self.availability_status or "soon"

        # -----------------------------------
        # SUMMARY TEXT
        # -----------------------------------
        summary = f"This {p_type}{renting} is available for rent in {locality}{city_str}. "

        if self.monthly_rent:
            summary += f"Available at a competitive rent of ₹{self.monthly_rent:,}/month. "

        if self.built_up_area:
            summary += f"It offers a spacious built-up area of {self.format_area(self.built_up_area)} sq.ft. "

        self.description = summary

        # -----------------------------------
        # LONG DESCRIPTION
        # -----------------------------------
        title_bit = f"{p_type}{renting}".strip()

        long_desc = f"<p>Experience comfortable living in this highly sought-after <strong>{title_bit}</strong> located in <strong>{locality}{city_str}</strong>.</p>"

        if self.building_name:
            long_desc += f"<p>Situated in the prestigious residential society of <strong>{self.building_name}</strong>, this home is meticulously designed to meet your lifestyle requirements while offering peace and privacy.</p>"

        long_desc += "<h3>Property Highlights:</h3><ul>"

        if self.built_up_area:
            carpet_str = ""

            if self.carpet_area:
                carpet_str = f" with a highly usable carpet area of {self.format_area(self.carpet_area)} sq.ft."

            long_desc += f"<li><strong>Space & Dimensions:</strong> Features a generous built-up area of {self.format_area(self.built_up_area)} sq.ft.{carpet_str}</li>"

        if self.monthly_rent:
            deposit_val = self.get_security_deposit_amount()
            deposit_str = f" (Security Deposit: ₹{deposit_val:,})" if deposit_val else ""
            long_desc += f"<li><strong>Pricing:</strong> Set at a reasonable monthly rent of ₹{self.monthly_rent:,}{deposit_str}.</li>"

        long_desc += f"<li><strong>Furnishing Status:</strong> The property is {furnishing}, saving you immense setup time and cost.</li>"

        if self.building_configuration or self.total_floors:
            config_str = f"{self.building_configuration} configuration" if self.building_configuration else ""
            total_str = f" across {self.total_floors} floors" if self.total_floors else ""
            wing_str = f" in {self.wing_number}" if self.wing_number else ""
            long_desc += f"<li><strong>Building Details:</strong> {config_str}{total_str}{wing_str}.</li>"

        if self.facing_direction:
            long_desc += f"<li><strong>Vastu & Orientation:</strong> {self.facing_direction}-facing property, ensuring ample natural sunlight.</li>"

        if self.main_road_connectivity:
            long_desc += f"<li><strong>Connectivity:</strong> {self.main_road_connectivity} from the main road.</li>"

        long_desc += f"<li><strong>Availability:</strong> The property status is {possession}.</li>"
        long_desc += f"<li><strong>Preferred Tenants:</strong> Highly suited for {available_for}.</li>"
        long_desc += "</ul>"

        # -----------------------------------
        # AMENITIES & FACILITIES
        # -----------------------------------
        extras = []
        if self.amenities:
            extras.append(str(self.amenities).strip())
        if self.nearby_facilities:
            extras.append(str(self.nearby_facilities).strip())

        if extras:
            extras_str = ", ".join(extras)
            long_desc += f"<h3>Top Amenities & Lifestyle:</h3><p>Residents will enjoy exclusive access to top-tier amenities & facilities including: <strong>{extras_str}</strong>.</p>"

        long_desc += "<p>This property provides seamless road connectivity to major commercial hubs, and medical options. Don't miss this opportunity.</p>"

        self.rent_residential_desc = long_desc

    # =====================================================
    # SAVE METHOD
    # =====================================================

    def save(self, *args, **kwargs):

        title_parts = []

        if self.furnishing_status:
            title_parts.append(self.furnishing_status)

        if self.property_type:
            title_parts.append(self.property_type)
        else:
            title_parts.append("Property")

        if self.renting_option:
            title_parts.append(f"({self.renting_option})")

        title_parts.append("for Rent")

        # property_no is deliberately NOT included — internal only.

        location = ""
        if self.building_name:
            location = f"in {self.building_name}"
        if self.locality_area:
            location = f"{location}, {self.locality_area}" if location else f"in {self.locality_area}"
        if self.city:
            location = f"{location}, {self.city}" if location else f"in {self.city}"
        if location:
            title_parts.append(location)

        if self.built_up_area:
            title_parts.append(
            f"({self.format_area(self.built_up_area)} sq.ft.)"
    )

        self.property_title = " ".join(title_parts).strip()[:255]

           

    # >>> BUILD UNIQUE KEY ONLY ON FIRST CREATE <
        if self._state.adding:
            key_source = f"{self.address}|{self.locality_area}|{self.city}|{self.bhk_type}|{self.monthly_rent}"
            self.property_unique_key = key_source.strip().lower().replace(" ", "")

        self.calculate_move_in_cost()
        self.generate_auto_descriptions()

        super(RentalResidentialProperty, self).save(*args, **kwargs)

    # >>> RECALCULATE DUPLICATE GROUP FROM ACTUAL DB STATE (idempotent) <
        if self.property_unique_key:
            group_qs = RentalResidentialProperty.objects.filter(
                property_unique_key=self.property_unique_key,
                is_deleted=False,
            )
            total = group_qs.count()

            if total > 1:
                original_id = group_qs.order_by("created_at").first().pk
                group_qs.update(
                    duplicate_count=total,
                    duplicate_group_id=original_id,
                    is_duplicate=True,
                )
            else:
                group_qs.update(
                    duplicate_count=1,
                    duplicate_group_id=None,
                    is_duplicate=False,
                )

        self.generate_auto_faqs()

    # =====================================================
    # AUTO FAQ GENERATOR
    # =====================================================

    def format_area(self, value):
        if value is None:
            return ""
        return f"{Decimal(value):.2f}"

    def generate_auto_faqs(self):

        self.faqs.all().delete()

        faq_pool = []

        rent_val = self.monthly_rent or 0
        deposit_val = self.get_security_deposit_amount()
        maint_val = self.monthy_maintenance_amount or 0

        # -----------------------------------
        # RENT FAQ
        # -----------------------------------
        if rent_val > 0:
            maint_str = ""
            if self.maintenance_type == "Extra" and maint_val > 0:
                maint_str = f" Maintenance is charged separately at ₹{maint_val:,}/month."
            elif self.maintenance_type == "Included in Rent":
                maint_str = " Maintenance charges are included in the rent."

            faq_pool.append({
                "q": f"What are the rent breakdown details and security deposit for this {self.property_type or 'property'}?",
                "a": f"The monthly rent for this property is ₹{rent_val:,}. A refundable security deposit of ₹{deposit_val:,} is required.{maint_str}",
            })

        # -----------------------------------
        # BROKERAGE / SERVICE FEE FAQ
        # -----------------------------------
        if self.brokerage_percentage:
            label = self.get_brokerage_label()
            value = self.get_brokerage_display_value()
            faq_pool.append({
                "q": f"Is there a {label.lower()} applicable on this listing?",
                "a": f"The applicable {label.lower()} for this property is: {value}.",
            })

        # -----------------------------------
        # AREA & BUILDING FAQ
        # -----------------------------------
        if self.carpet_area:
            carpet_str = (
                f" out of which the usable carpet area is "
                f"{self.format_area(self.carpet_area)} sq.ft.")
        

            building_str = ""
            if self.building_configuration or self.total_floors:
                building_str = f" The building configuration is {self.building_configuration or 'N/A'}" \
                                f"{f', spread across {self.total_floors} floors' if self.total_floors else ''}."

            faq_pool.append({
                "q": "How much space does this rental option offer?",
                  "a": (f"This residential unit offers a built-up area of "f"{self.format_area(self.built_up_area)} sq.ft."f"{carpet_str}{building_str}"),
            })

        # -----------------------------------
        # FURNISHING FAQ
        # -----------------------------------
        if self.furnishing_status:
            balcony_str = f" accompanied by {self.balconies} well-ventilated balcony areas" if self.balconies else ""
            faq_pool.append({
                "q": "What is the furnishing status and physical configuration of this property?",
                "a": f"The property is {self.furnishing_status}, with {self.bathrooms or 1} bathroom(s){balcony_str}.",
            })

        # -----------------------------------
        # FACING FAQ
        # -----------------------------------
        if self.facing_direction:
            faq_pool.append({
                "q": "Which direction does this rental unit face?",
                "a": f"This property features a {self.facing_direction}-facing layout orientation.",
            })

        # -----------------------------------
        # LEASE FAQ
        # -----------------------------------
        if self.available_for or self.lease_duration:
            faq_pool.append({
                "q": "Who is eligible to lease this home and what is the standard lease duration?",
                "a": f"This property is suited for {self.available_for or 'family or working professionals'}. The standard lease duration is {self.lease_duration or '11 Months'}.",
            })

        # -----------------------------------
        # POSSESSION FAQ
        # -----------------------------------
        if self.availability_status:
            date_str = " immediately"
            if self.available_from:
                try:
                    date_str = f" starting from {self.available_from.strftime('%d %B %Y')}"
                except Exception:
                    date_str = f" starting from {self.available_from}"

            faq_pool.append({
                "q": "When can tenants move into this property?",
                "a": f"The current availability status is '{self.availability_status}'. Possession can begin{date_str}.",
            })

        # -----------------------------------
        # CONNECTIVITY FAQ
        # -----------------------------------
        if self.main_road_connectivity:
            faq_pool.append({
                "q": "How well connected is this property to the main road?",
                "a": f"This property is located {self.main_road_connectivity.lower()} of the main road, ensuring convenient access.",
            })

        for item in faq_pool:
            RentalResidentialFAQ.objects.create(
                property=self,
                question=item["q"],
                answer=item["a"],
            )

    def __str__(self):
        return self.property_title if self.property_title else f"Property #{self.id}"


# ==========================================
# PROPERTY IMAGES
# ==========================================


class RentalResidentialImage(models.Model):
    CATEGORY_CHOICES = [
        ('exterior', 'Exterior / Building'),
        ('living',   'Living / Dining'),
        ('bedroom',  'Bedroom'),
        ('kitchen',  'Kitchen'),
        ('bathroom', 'Bathroom'),
        ('balcony',  'Balcony'),
        ('others',   'Others'),
    ]
    property = models.ForeignKey(RentalResidentialProperty, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to="residential_rent/")
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='others')
    sequence_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["category", "sequence_order"]





class RentalResidentialVideo(models.Model):
    SOURCE_CHOICES = [
        ('uploaded', 'Manually Uploaded'),
        ('auto', 'Auto Generated Slideshow'),
        ('rm_assisted', 'RM Assisted Link'),
    ]
    property = models.ForeignKey(RentalResidentialProperty, on_delete=models.CASCADE, related_name="video")
    video = models.FileField(upload_to="residential_rent/videos/", null=True, blank=True)
    video_url = models.URLField(null=True, blank=True)
    source = models.CharField(max_length=15, choices=SOURCE_CHOICES, default='auto')
    created_at = models.DateTimeField(auto_now_add=True)

    def youtube_thumbnail(self):
        import re
        if self.source == 'rm_assisted' and self.video_url:
            match = re.search(
                r'(?:youtube\.com/watch\?v=|youtu\.be/|youtube\.com/shorts/)([A-Za-z0-9_-]{6,})',
                self.video_url
            )
            if match:
                return f"https://img.youtube.com/vi/{match.group(1)}/hqdefault.jpg"
        return None

    # NEW: Identify the platform for better UI representation in the HTML table
    def get_platform_type(self):
        if not self.video_url:
            return 'unknown'
        url = self.video_url.lower()
        if 'youtube.com' in url or 'youtu.be' in url:
            return 'youtube'
        elif 'instagram.com' in url or 'instagr.am' in url:
            return 'instagram'
        elif 'facebook.com' in url or 'fb.watch' in url:
            return 'facebook'
        elif 'vimeo.com' in url:
            return 'vimeo'
        elif 'drive.google.com' in url:
            return 'gdrive'
        return 'external'

# ==========================================
# FAQ MODEL
# ==========================================

class RentalResidentialFAQ(models.Model):
    property = models.ForeignKey(RentalResidentialProperty, on_delete=models.CASCADE, related_name="faqs")
    question = models.CharField(max_length=255)
    answer = models.TextField()


# ==========================================
# ACTIVITY LOG  (unchanged from your original)
# ==========================================

class RentalActivityLog(models.Model):

    ACTION_CHOICES = [
        ("SEARCH", "Manual Query Search"),
        ("CREATE", "Property Entry Created"),
        ("UPDATE", "Record Update Action"),
        ("DELETE", "Deletion / Purge Record"),
        ("EXCEL_IMPORT", "Excel Sheet Import Data"),
    ]

    timestamp = models.DateTimeField(auto_now_add=True)
    user_identity = models.CharField(max_length=255, null=True, blank=True)
    user_role = models.CharField(max_length=100, null=True, blank=True)
    action_type = models.CharField(max_length=50, choices=ACTION_CHOICES)
    property_id = models.CharField(max_length=100, null=True, blank=True)
    targeted_fields = models.CharField(max_length=255, null=True, blank=True)
    associated_file = models.CharField(max_length=255, null=True, blank=True)
    action_payload = models.TextField(null=True, blank=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    status = models.CharField(max_length=20, default="SUCCESS")

    class Meta:
        ordering = ["-timestamp"]

################################END MODEL SECTION OF THE RENTAL RESIDENTIAL LISTING####################


############### Models Starts for Rental COMMERCIAL Property  model ############################ same in this this teh rental proeprty listing model so as per add the user role in ths also and give me the view of like this residenital view for data submit  




import uuid
import hashlib
from decimal import Decimal, InvalidOperation
from django.db import models

def generate_commercial_rental_id():
    return f"EFCPR-{uuid.uuid4().hex[:8].upper()}"

class CommercialRentalProperty(models.Model):
    id = models.CharField(
        max_length=20,
        primary_key=True,
        default=generate_commercial_rental_id,
        editable=False,
    )

    # ── STEP 1: LISTED BY ──────────────────────────────────────────────────
    listing_type = models.CharField(max_length=100, blank=True, null=True)
    category = models.CharField(max_length=100, blank=True, null=True)
    listed_by_type = models.CharField(max_length=100, blank=True, null=True)
    assigned_to = models.CharField(max_length=100, blank=True, null=True)
    listed_by_id = models.CharField(max_length=150, blank=True, null=True)
    listed_by_name = models.CharField(max_length=150, blank=True, null=True)
    listed_by_email = models.CharField(max_length=150, blank=True, null=True)
    listed_by_contact = models.CharField(max_length=50, blank=True, null=True)
    listed_by_role = models.CharField(max_length=100, blank=True, null=True)

    # DUPLICATE TRACKING FIELDS
    property_unique_key = models.CharField(max_length=255, blank=True, null=True, db_index=True)
    duplicate_count = models.PositiveIntegerField(default=0)
    duplicate_group_id = models.CharField(max_length=255, blank=True, null=True, db_index=True)

    # ── STEP 1: BASIC INFORMATION ──────────────────────────────────────────
    property_title = models.CharField(max_length=255, blank=True, null=True)
    property_type = models.CharField(max_length=100, blank=True, null=True)
    building_name = models.CharField(max_length=200, blank=True, null=True)
    wing_number = models.CharField(max_length=50, blank=True, null=True)
    property_no = models.CharField(max_length=100, blank=True, null=True) # Internal only

    availability_status = models.CharField(max_length=100, blank=True, null=True)
    available_from = models.DateField(blank=True, null=True)
    property_age = models.IntegerField(blank=True, null=True)
    zone_type = models.CharField(max_length=100, blank=True, null=True)
    ownership_type = models.CharField(max_length=100, blank=True, null=True)
    property_condition = models.CharField(max_length=100, blank=True, null=True)

    builtup_area = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    carpet_area = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)

    brokerage_percentage = models.CharField(max_length=50, blank=True, null=True)
    manual_brokerage = models.CharField(max_length=100, blank=True, null=True)

    # ── STEP 1: LOCATION DETAILS ───────────────────────────────────────────
    address = models.TextField(blank=True, null=True)
    locality = models.CharField(max_length=200, blank=True, null=True)
    property_landmark = models.CharField(max_length=200, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    state = models.CharField(max_length=100, blank=True, null=True)
    location_hub = models.CharField(max_length=100, blank=True, null=True)
    pincode = models.CharField(max_length=20, blank=True, null=True)
    google_maps_link = models.URLField(max_length=500, blank=True, null=True)
    latitude = models.CharField(max_length=50, blank=True, null=True)
    longitude = models.CharField(max_length=50, blank=True, null=True)

    # ── STEP 2: SPECIFICATIONS & PRICING ───────────────────────────────────
    dg_ups_included = models.BooleanField(default=False)
    electricity_included = models.BooleanField(default=False)
    water_included = models.BooleanField(default=False)

    building_configuration = models.CharField(max_length=50, blank=True, null=True)
    total_floors = models.IntegerField(blank=True, null=True)
    staircases = models.IntegerField(blank=True, null=True)
    passenger_lifts = models.IntegerField(default=0)
    service_lifts = models.IntegerField(default=0)
    private_parking = models.IntegerField(default=0)

    min_seats = models.IntegerField(blank=True, null=True)
    max_seats = models.IntegerField(blank=True, null=True)
    cabins = models.IntegerField(blank=True, null=True)
    meeting_rooms = models.IntegerField(blank=True, null=True)
    private_washroom = models.IntegerField(default=0)
    public_washroom = models.IntegerField(default=0)
    flooring_type = models.CharField(max_length=100, blank=True, null=True)

    monthly_rent = models.BigIntegerField(blank=True, null=True)
    advanced_rent_type = models.CharField(max_length=50, blank=True, null=True)
    advanced_rent_amount = models.BigIntegerField(blank=True, null=True)
    security_deposit_type = models.CharField(max_length=50, blank=True, null=True)
    security_deposit_amount = models.BigIntegerField(blank=True, null=True)
    maintenance_type = models.CharField(max_length=50, blank=True, null=True)
    maintenance_charges = models.BigIntegerField(blank=True, null=True)
    total_move_in_cost = models.BigIntegerField(blank=True, null=True)
    negotiable = models.CharField(max_length=10, default="Yes")
    lockin_period = models.IntegerField(blank=True, null=True)
    rent_increase = models.FloatField(blank=True, null=True)

    # ── STEP 3: AMENITIES & DESCRIPTIONS ───────────────────────────────────
    amenities = models.TextField(blank=True, null=True)
    nearby_facilities = models.TextField(blank=True, null=True)
    property_summary = models.TextField(blank=True, null=True)
    property_description = models.TextField(blank=True, null=True)
    user_description = models.TextField(blank=True, null=True)

    # ── STEP 4: MEDIA & STATUS ─────────────────────────────────────────────
    
    listed_elsewhere = models.CharField(max_length=10, default="No")
    portal_name = models.CharField(max_length=100, blank=True, null=True)

    uploaded_by_name = models.CharField(max_length=150, blank=True, null=True)
    uploaded_by_email = models.CharField(max_length=150, blank=True, null=True)
    uploaded_by_contact = models.CharField(max_length=50, blank=True, null=True)
    uploaded_by_role = models.CharField(max_length=100, blank=True, null=True)

    upload_file_name = models.CharField(max_length=255, blank=True, null=True)
    # Add this new field to store the actual file
    upload_file = models.FileField(upload_to='property_uploads/files/', blank=True, null=True)

    is_deleted = models.BooleanField(default=False)
    is_duplicate = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(null=True, blank=True)
    deleted_by = models.CharField(max_length=150, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    listing_status = models.CharField(max_length=150, blank=True, null=True)
    approval_status = models.CharField(max_length=150, blank=True, null=True)

    BROKERAGE_LABEL_MAP = {
        "admin": "EstateFlow Service Fee",
        "relationship manager": "Service Fee",
        "landlord": "Tenant Service Fee",
        "agent": "Brokerage",
        "agency/builder": "Service Fee",
        "builder": "Service Fee",
    }

    def get_brokerage_label(self):
        role = (self.listed_by_role or "").strip().lower()
        return self.BROKERAGE_LABEL_MAP.get(role, "Brokerage")

    def get_brokerage_display_value(self):
        if self.brokerage_percentage == "Fixed Amount":
            return self.manual_brokerage or "-"
        return self.brokerage_percentage or "-"

    # AREA FORMATTING HELPER (ALWAYS 2 DECIMAL PLACES, MATCHING DB STORAGE)
    def format_area(self, value):
        if value in (None, "", 0):
            return None
        try:
            return f"{Decimal(value):.2f}"
        except (InvalidOperation, TypeError, ValueError):
            return value

    # DERIVED MONEY HELPERS

    # DERIVED MONEY HELPERS
    def get_advance_rent_amount(self):
        rent = self.monthly_rent or 0
        raw = (self.advanced_rent_type or "").strip().lower()
        has_amount = self.advanced_rent_amount not in (None, 0, "", "0")

        if raw == "fixed amount" or has_amount:
            return self.advanced_rent_amount or 0
        try:
            months = int(raw.split()[0])
            return months * rent
        except (TypeError, ValueError, IndexError):
            return self.advanced_rent_amount or 0

    def get_security_deposit_amount(self):
        rent = self.monthly_rent or 0
        raw = (self.security_deposit_type or "").strip().lower()
        has_amount = self.security_deposit_amount not in (None, 0, "", "0")

        if raw == "fixed amount" or has_amount:
            return self.security_deposit_amount or 0
        try:
            months = int(raw.split()[0])
            return months * rent
        except (TypeError, ValueError, IndexError):
            return self.security_deposit_amount or 0

    def get_brokerage_amount(self):
        rent = self.monthly_rent or 0
        choice = (self.brokerage_percentage or "").strip().lower()
        has_manual = self.manual_brokerage not in (None, "", "0", 0)

        if choice == "no brokerage":
            return 0
        elif choice == "15 days rent":
            return rent / 2
        elif choice == "1 month rent":
            return rent
        elif choice in ("fixed amount", "negotiable") or has_manual:
            try:
                return float(self.manual_brokerage or 0)
            except (TypeError, ValueError):
                return 0
        return 0

    def calculate_move_in_cost(self):
        advance = self.get_advance_rent_amount()
        deposit = self.get_security_deposit_amount()
        brokerage = self.get_brokerage_amount()

        maintenance = 0
        m_type = (self.maintenance_type or "").strip().lower()
        has_maint_amount = self.maintenance_charges not in (None, 0, "", "0")

        if "exclud" in m_type or has_maint_amount:
            maintenance = self.maintenance_charges or 0

        total = advance + deposit + brokerage + maintenance
        self.total_move_in_cost = round(total)

    # AUTO DESCRIPTIONS WITHOUT NEARBY FACILITIES
    def generate_auto_descriptions(self):
        p_type = (self.property_type or "Commercial Space").replace("_", " ").title()
        p_cond = self.property_condition or "Well Maintained"
        loc = self.locality or "a prime commercial hub"
        city_str = f", {self.city}" if self.city else ""

        # 1. Summary
        summary = f"A premium {p_cond} {p_type} is available for rent in {loc}{city_str}. "
        if self.monthly_rent:
            summary += f"Available at a highly competitive rent of ₹{self.monthly_rent:,}/month. "
        if self.builtup_area or self.carpet_area:
            area_bits = []
            if self.builtup_area:
                area_bits.append(f"built-up area of {self.format_area(self.builtup_area)} sq.ft.")
            if self.carpet_area:
                area_bits.append(f"carpet area of {self.format_area(self.carpet_area)} sq.ft.")
            summary += f"This property offers an expansive {' and '.join(area_bits)} "
        self.property_summary = summary

        # 2. Detailed Description
        long_desc = f"<p>Elevate your enterprise footprint with this strategically positioned <strong>{p_cond} {p_type}</strong> in <strong>{loc}{city_str}</strong>.</p>"
        if self.building_name:
            long_desc += f"<p>Situated within the highly sought-after commercial complex of <strong>{self.building_name}</strong>, this property ensures prime visibility and professional appeal.</p>"

        long_desc += "<h3>Property Highlights:</h3><ul>"
        if self.builtup_area or self.carpet_area:
            if self.builtup_area and self.carpet_area:
                dim_text = f"Generous built-up area of {self.format_area(self.builtup_area)} sq.ft. (Carpet Area: {self.format_area(self.carpet_area)} sq.ft.)"
            elif self.builtup_area:
                dim_text = f"Generous built-up area of {self.format_area(self.builtup_area)} sq.ft."
            else:
                dim_text = f"Carpet area of {self.format_area(self.carpet_area)} sq.ft."
            long_desc += f"<li><strong>Space & Dimensions:</strong> {dim_text}.</li>"
        if self.monthly_rent:
            dep_val = self.get_security_deposit_amount()
            dep_str = f" (Security Deposit: ₹{dep_val:,})" if dep_val else ""
            long_desc += f"<li><strong>Financial Terms:</strong> Competitively priced at ₹{self.monthly_rent:,}/month{dep_str}. Negotiable: {self.negotiable or 'No'}.</li>"
        
        long_desc += f"<li><strong>Condition:</strong> Currently offered in a '{p_cond}' setup.</li>"
        
        if self.total_floors or self.building_configuration:
            config_str = f"Configuration '{self.building_configuration}'" if self.building_configuration else "Standard structure"
            floors_str = f" across {self.total_floors} constructed floors" if self.total_floors else ""
            long_desc += f"<li><strong>Building Structure:</strong> {config_str}{floors_str}.</li>"
        long_desc += "</ul>"

        if any([self.min_seats, self.cabins, self.meeting_rooms, self.passenger_lifts]):
            long_desc += "<h3>Workspace & Logistics Configuration:</h3><ul>"
            if self.min_seats or self.max_seats:
                long_desc += f"<li><strong>Seating Capacity:</strong> Optimized to support {self.min_seats or 0} to {self.max_seats or 0} workstations.</li>"
            if self.cabins:
                long_desc += f"<li><strong>Executive Cabins:</strong> Features {self.cabins} dedicated private cabins.</li>"
            if self.meeting_rooms:
                long_desc += f"<li><strong>Conference Rooms:</strong> {self.meeting_rooms} integrated board/meeting rooms.</li>"
            if self.passenger_lifts or self.service_lifts:
                long_desc += f"<li><strong>Vertical Transit:</strong> Equipped with {self.passenger_lifts} passenger elevators and {self.service_lifts} cargo lifts.</li>"
            long_desc += "</ul>"

        if self.amenities:
            long_desc += f"<h3> Amenities:</h3><p>Includes top-tier commercial amenities: <strong>{self.amenities}</strong>.</p>"
        
        if self.nearby_facilities:
            long_desc += f"<h3>Nearby Facilities:</h3><p>Strategically located with excellent connectivity and proximity to: <strong>{self.nearby_facilities}</strong>.</p>"
        
        
        long_desc += "<p>Don't miss out on establishing your business in a thriving hub. Contact us today to schedule a site inspection!</p>"
        self.property_description = long_desc

    # SAVE METHOD WITH SHA-256 DUPLICATE HASHING
    def save(self, *args, **kwargs):
        p_type = (self.property_type or "Commercial Space").replace("_", " ").title()
        loc = self.locality or ""
        b_name = f"in {self.building_name}" if self.building_name else ""
        city_name = f", {self.city}" if self.city else ""
        area_str = f"({self.format_area(self.builtup_area)} sq.ft.)" if self.builtup_area else ""

        # Auto-generate title without skipping
        title_parts = [p_type, "for Rent"]
        if b_name: title_parts.append(b_name)
        if loc or city_name: title_parts.append(f"{loc}{city_name}".strip())
        if area_str: title_parts.append(area_str)
        self.property_title = " ".join(title_parts).strip()[:255]

        # Enforce Backend Calculations & Descriptions
        self.calculate_move_in_cost()
        self.generate_auto_descriptions()

        # Build Unique Key Only on First Create
        if self._state.adding:
            key_source = f"{self.address}|{self.locality}|{self.city}|{self.property_type}|{self.monthly_rent}"
            self.property_unique_key = key_source.strip().lower().replace(" ", "")

        super().save(*args, **kwargs)

        # Recalculate Duplicate Group using SHA-256 Hash formatting
        if self.property_unique_key:
            hashed_group_id = hashlib.sha256(self.property_unique_key.encode('utf-8')).hexdigest()
            
            group_qs = CommercialRentalProperty.objects.filter(
                property_unique_key=self.property_unique_key,
                is_deleted=False,
            )
            total = group_qs.count()

            if total > 1:
                group_qs.update(
                    duplicate_count=total,
                    duplicate_group_id=hashed_group_id,
                    is_duplicate=True,
                )
                self.duplicate_count = total
                self.duplicate_group_id = hashed_group_id
                self.is_duplicate = True
            else:
                group_qs.update(
                    duplicate_count=1,
                    duplicate_group_id=None,
                    is_duplicate=False,
                )
                self.duplicate_count = 1
                self.duplicate_group_id = None
                self.is_duplicate = False

        self.generate_auto_faqs()

    def generate_auto_faqs(self):
        self.faqs.all().delete()
        faq_pool = []

        # FAQ 1: Rent & Deposit
        if self.monthly_rent:
            dep_val = self.get_security_deposit_amount()
            faq_pool.append({
                "q": f"What are the operational lease pricing and security deposit terms for this {self.property_type or 'commercial space'}?",
                "a": f"The monthly rent is pegged at ₹{self.monthly_rent:,}. A refundable security deposit of ₹{dep_val:,} applies. Maintenance charges are categorized as '{self.maintenance_type or 'Included'}'.",
            })

        # FAQ 2: Brokerage
        # FAQ 2: Brokerage
        if self.brokerage_percentage:
            label = self.get_brokerage_label()
            val = self.get_brokerage_display_value()
            
            if str(self.brokerage_percentage).strip().lower() == "no brokerage":
                faq_pool.append({
                    "q": f"Is there a {label.lower()} applicable on this commercial lease?",
                    "a": f"No, there is 0 {label.lower()} applicable on this property.",
                })
            else:
                faq_pool.append({
                    "q": f"Is there a {label.lower()} applicable on this commercial lease?",
                    "a": f"Yes, the applicable {label.lower()} for this property is: {val}.",
                })

        # FAQ 3: Built-up Area & Workstations
        if self.builtup_area or self.carpet_area:
            builtup_str = self.format_area(self.builtup_area) or '—'
            carpet_str = self.format_area(self.carpet_area) or '—'
            faq_pool.append({
                "q": "What are the total area dimensions and workspace setup metrics?",
                "a": f"The property features a built-up area of {builtup_str} sq.ft. (Carpet area: {carpet_str} sq.ft.). It can comfortably support {self.min_seats or 0} to {self.max_seats or 0} workstations along with {self.cabins or 0} private executive cabins.",
            })

        # FAQ 4: Utilities & Lifts
        faq_pool.append({
            "q": "What critical utilities and backup infrastructures service this facility?",
            "a": f"Dedicated DG/UPS power backup is {'Included' if self.dg_ups_included else 'Not Included'}. Grid electricity is {'Included' if self.electricity_included else 'Separately Metered'}, and water supply access is {'Included' if self.water_included else 'Separately Metered'}. Vertical mobility is supported via {self.passenger_lifts} passenger and {self.service_lifts} service elevators.",
        })

        # FAQ 5: Parking Details
        faq_pool.append({
            "q": "What parking accommodations are available with this commercial rental?",
            "a": f"The property provides {self.private_parking} dedicated private parking spots for executives and staff. Additionally, there are {self.public_washroom} public parking/washroom facilities located nearby for visitors.",
        })

        # FAQ 6: Lease Lock-in & Increases
        lockin_str = f" The standard lock-in period is {self.lockin_period} months." if self.lockin_period else " There is no specific lock-in period declared."
        increase_str = f" An annual rent escalation of {self.rent_increase}% applies." if self.rent_increase else " Rent escalations will be mutually discussed during contracting."
        faq_pool.append({
            "q": "What are the standard lock-in period and annual rent escalation terms?",
            "a": f"Rent negotiability is indicated as '{self.negotiable or 'Yes'}'.{lockin_str}{increase_str}",
        })

        # FAQ 7: Zone & Building Details
        faq_pool.append({
            "q": "Which commercial zone is this property located in, and what is its condition?",
            "a": f"The property operates within a registered '{self.zone_type or 'Commercial'}' zone. It is currently categorized as '{self.property_condition or 'Well Maintained'}'. The building configuration is {self.building_configuration or 'Standard'} spanning {self.total_floors or 'multiple'} total floors.",
        })

        for item in faq_pool:
            CommercialRentalFAQ.objects.create(property=self, question=item["q"], answer=item["a"])

    def __str__(self):
        return f"{self.property_title or 'Commercial Rental'} ({self.id})"

class CommercialRentalPropertyImage(models.Model):
    CATEGORY_CHOICES = [
        ('exterior', 'Building Exterior'),
        ('reception', 'Reception / Lobby'),
        ('workspace', 'Office Workspace'),
        ('cabins', 'Cabins / Manager Rooms'),
        ('meeting_room', 'Meeting / Conference Room'),
        ('shop_showroom', 'Shop / Showroom Area'),
        ('warehouse', 'Warehouse / Storage'),
        ('pantry', 'Pantry / Cafeteria'),
        ('washroom', 'Washroom'),
        ('parking', 'Parking'),
        ('amenities', 'Common Amenities'),
        ('floor_plan', 'Floor Plan'),
    ]

    property = models.ForeignKey(CommercialRentalProperty, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to="commercial_rent/images/")
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='amenities')
    sequence_order = models.PositiveIntegerField(default=0)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["category", "sequence_order", "uploaded_at"]
        



class CommercialRentalVideo(models.Model):
    SOURCE_CHOICES = [
        ('uploaded', 'Manually Uploaded'), 
        ('auto', 'Auto Generated Slideshow'),
        ('rm_assisted', 'RM Assisted Link')
    ]

    property = models.ForeignKey(CommercialRentalProperty, on_delete=models.CASCADE, related_name="walkthrough_video")
    
    video = models.FileField(upload_to="commercial_rent/videos/", null=True, blank=True)
    video_url = models.URLField(max_length=500, null=True, blank=True)
    
    source = models.CharField(max_length=20, choices=SOURCE_CHOICES, default='auto')
    video_status = models.CharField(max_length=100, default="Pending")
    
    created_at = models.DateTimeField(auto_now_add=True)

    def youtube_thumbnail(self):
        import re
        if self.source == 'rm_assisted' and self.video_url:
            match = re.search(
                r'(?:youtube\.com/watch\?v=|youtu\.be/|youtube\.com/shorts/)([A-Za-z0-9_-]{6,})',
                self.video_url
            )
            if match:
                return f"https://img.youtube.com/vi/{match.group(1)}/hqdefault.jpg"
        return None

    def get_platform_type(self):
        if not self.video_url: return 'unknown'
        url = self.video_url.lower()
        if 'youtube.com' in url or 'youtu.be' in url: return 'youtube'
        if 'instagram.com' in url or 'instagr.am' in url: return 'instagram'
        if 'facebook.com' in url or 'fb.watch' in url: return 'facebook'
        if 'vimeo.com' in url: return 'vimeo'
        return 'external'

class CommercialRentalFAQ(models.Model):
    property = models.ForeignKey(CommercialRentalProperty, on_delete=models.CASCADE, related_name="faqs")
    question = models.CharField(max_length=255)
    answer = models.TextField()

class CommercialRentalActivityLog(models.Model):
    ACTION_CHOICES = [
        ("CREATE", "Property Entry Created"),
        ("UPDATE", "Record Update Action"),
        ("DELETE", "Deletion / Purge Record"),
    ]
    timestamp = models.DateTimeField(auto_now_add=True)
    user_identity = models.CharField(max_length=255, null=True, blank=True)
    user_role = models.CharField(max_length=100, null=True, blank=True)
    action_type = models.CharField(max_length=50, choices=ACTION_CHOICES)
    property_id = models.CharField(max_length=100, null=True, blank=True)
    action_payload = models.TextField(null=True, blank=True)
    status = models.CharField(max_length=20, default="SUCCESS")

    class Meta:
        ordering = ["-timestamp"]


############### Models END for Rental COMMERICIAL  Property  model ############################ same in this this teh rental proeprty listing model so as per add the user role in ths also and give me the view of like this residenital view for data submit  



############### Models Starts for Rental PG_COLIVING Property  model ############################ same in this this teh rental proeprty listing model so as per add the user role in ths also and give me the view of like this residenital view for data submit  





def generate_unique_pg_property_id():
    return f"EFPG-{uuid.uuid4().hex[:8].upper()}"


class PGColivingProperty(models.Model):
    id = models.CharField(
        max_length=20,
        primary_key=True,
        default=generate_unique_pg_property_id,
        editable=False,
    )

    # ── STEP 1: LISTED BY ──────────────────────────────────────────────────
    listing_type = models.CharField(max_length=100, blank=True, null=True)
    category = models.CharField(max_length=100, blank=True, null=True)
    listed_by_type = models.CharField(max_length=100, blank=True, null=True)
    assigned_to = models.CharField(max_length=100, blank=True, null=True)
    listed_by_id = models.CharField(max_length=150, blank=True, null=True)
    listed_by_name = models.CharField(max_length=150, blank=True, null=True)
    listed_by_email = models.CharField(max_length=150, blank=True, null=True)
    listed_by_contact = models.CharField(max_length=50, blank=True, null=True)
    listed_by_role = models.CharField(max_length=100, blank=True, null=True)

    # DUPLICATE TRACKING FIELDS (added — mirrors CommercialRentalProperty)
    property_unique_key = models.CharField(max_length=255, blank=True, null=True, db_index=True)
    duplicate_count = models.PositiveIntegerField(default=0)
    duplicate_group_id = models.CharField(max_length=255, blank=True, null=True, db_index=True)

    # ── STEP 1: BASIC INFORMATION ──────────────────────────────────────────
    property_title = models.CharField(max_length=255, blank=True, null=True)
    building_name = models.CharField(max_length=200, blank=True, null=True)
    # INTERNAL ONLY — never exposed publicly
    property_no = models.CharField(max_length=100, blank=True, null=True)
    wing_number = models.CharField(max_length=50, blank=True, null=True)

    city = models.CharField(max_length=100, blank=True, null=True)
    locality = models.CharField(max_length=200, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    property_landmark = models.CharField(max_length=200, blank=True, null=True)
    state = models.CharField(max_length=100, blank=True, null=True)
    pincode = models.CharField(max_length=100, blank=True, null=True)
    google_maps_link = models.URLField(max_length=500, blank=True, null=True)
    latitude = models.CharField(max_length=50, blank=True, null=True)
    longitude = models.CharField(max_length=50, blank=True, null=True)

    pg_for = models.CharField(max_length=50, blank=True, null=True)  # Boys / Girls / Co-living
    furnishing_status = models.CharField(max_length=50, blank=True, null=True)
    best_suited_for = models.CharField(max_length=150, blank=True, null=True)

    meals_available = models.BooleanField(default=False)
    meal_offerings = models.CharField(max_length=150, blank=True, null=True)
    meal_speciality = models.CharField(max_length=150, blank=True, null=True)

    notice_period = models.IntegerField(blank=True, null=True)
    lockin_period = models.IntegerField(blank=True, null=True)
    minimum_stay = models.IntegerField(blank=True, null=True)
    available_from = models.DateField(blank=True, null=True)
    property_managed_by = models.CharField(max_length=100, blank=True, null=True)
    manager_stays = models.BooleanField(default=False)

    brokerage_percentage = models.CharField(max_length=50, blank=True, null=True)
    manual_brokerage = models.CharField(max_length=100, blank=True, null=True)

    # ── STEP 2: ROOM DETAILS & PRICING (MERGED/FLATTENED DIRECTLY) ─────────
    room_type = models.CharField(max_length=100, blank=True, null=True)  # Single / Double / Triple / Quad
    total_beds = models.IntegerField(blank=True, null=True)
    monthly_rent = models.BigIntegerField(blank=True, null=True)         # Rent per occupant
    advance_rent_month = models.CharField(max_length=50, blank=True, null=True)
    advance_rent_amount = models.BigIntegerField(blank=True, null=True)
    security_deposit_type = models.CharField(max_length=50, blank=True, null=True)
    security_deposit_amount = models.BigIntegerField(blank=True, null=True)
    maintenance_type = models.CharField(max_length=50, blank=True, null=True)
    maintenance_amount = models.BigIntegerField(blank=True, null=True)
    total_move_in_cost = models.BigIntegerField(blank=True, null=True)

    # ── STEP 3: REGULATIONS & AMENITIES ────────────────────────────────────
    opposite_gender_visitors_allowed = models.BooleanField(default=False)
    visitors_allowed = models.BooleanField(default=False)
    parents_guardians_allowed = models.BooleanField(default=False)
    entry_24x7_allowed = models.BooleanField(default=False)
    curfew_time = models.TimeField(blank=True, null=True)
    smoking_allowed = models.BooleanField(default=False)
    alcohol_consumption_allowed = models.BooleanField(default=False)
    couples_allowed = models.BooleanField(default=False)
    pets_allowed = models.BooleanField(default=False)
    cooking_allowed = models.BooleanField(default=False)
    police_verification_required = models.BooleanField(default=False)

    amenities = models.TextField(blank=True, null=True)
    nearby_facilities = models.TextField(blank=True, null=True)
    property_summary = models.TextField(blank=True, null=True)
    property_description = models.TextField(blank=True, null=True)
    user_description = models.TextField(blank=True, null=True)

    # ── STEP 4: MEDIA & STATUS ─────────────────────────────────────────────
    video = models.FileField(upload_to="pg/videos/", blank=True, null=True)
    listed_elsewhere = models.CharField(max_length=10, default="No")
    portal_name = models.CharField(max_length=100, blank=True, null=True)

    uploaded_by_name = models.CharField(max_length=150, blank=True, null=True)
    uploaded_by_email = models.CharField(max_length=150, blank=True, null=True)
    uploaded_by_contact = models.CharField(max_length=50, blank=True, null=True)
    uploaded_by_role = models.CharField(max_length=100, blank=True, null=True)
    upload_file_name = models.CharField(max_length=255, blank=True, null=True)
    # Add this new field to store the actual file
    upload_file = models.FileField(upload_to='property_uploads/files/', blank=True, null=True)

    is_deleted = models.BooleanField(default=False)
    is_duplicate = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(null=True, blank=True)
    deleted_by = models.CharField(max_length=150, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    listing_status = models.CharField(max_length=150, blank=True, null=True)
    approval_status = models.CharField(max_length=150, blank=True, null=True)

    # ═══════════════════════════════════════════════════════════════════════
    #  BROKERAGE LOGIC
    # ═══════════════════════════════════════════════════════════════════════
    BROKERAGE_LABEL_MAP = {
        "admin": "EstateFlow Service Fee",
        "relationship manager": "Service Fee",
        "landlord": "Tenant Service Fee",
        "agent": "Brokerage",
        "agency/builder": "Service Fee",
        "builder": "Service Fee",
    }

    def get_brokerage_label(self):
        role = (self.listed_by_role or "").strip().lower()
        return self.BROKERAGE_LABEL_MAP.get(role, "Brokerage")

    def get_brokerage_display_value(self):
        if self.brokerage_percentage == "Fixed Amount":
            return self.manual_brokerage or "-"
        return self.brokerage_percentage or "-"

    # ═══════════════════════════════════════════════════════════════════════
    #  DERIVED MONEY HELPERS (added — mirrors CommercialRentalProperty)
    # ═══════════════════════════════════════════════════════════════════════
    def get_advance_rent_amount(self):
        rent = self.monthly_rent or 0
        raw = (self.advance_rent_month or "").strip().lower()
        has_amount = self.advance_rent_amount not in (None, 0, "", "0")

        if raw == "fixed amount" or raw == "fixed" or has_amount:
            return self.advance_rent_amount or 0
        try:
            months = int(raw.split()[0])
            return months * rent
        except (TypeError, ValueError, IndexError):
            return self.advance_rent_amount or 0

    def get_security_deposit_amount(self):
        rent = self.monthly_rent or 0
        raw = (self.security_deposit_type or "").strip().lower()
        has_amount = self.security_deposit_amount not in (None, 0, "", "0")

        if raw == "fixed amount" or raw == "fixed" or has_amount:
            return self.security_deposit_amount or 0
        try:
            months = int(raw.split()[0])
            return months * rent
        except (TypeError, ValueError, IndexError):
            return self.security_deposit_amount or 0



    def get_advance_rent_type_label(self):
        val = (self.advance_rent_month or "").strip()
        
        if val.lower() in ["fixed", "fixed amount"]:
            return "Fixed Amount"
            
        return val or "-"

    def get_security_deposit_type_label(self):
        val = (self.security_deposit_type or "").strip()
        
        if val.lower() in ["fixed", "fixed amount"]:
            return "Fixed Amount"
            
        return val or "-"

    def get_brokerage_amount(self):
        rent = self.monthly_rent or 0
        choice = (self.brokerage_percentage or "").strip().lower()
        has_manual = self.manual_brokerage not in (None, "", "0", 0)

        if choice == "no brokerage":
            return 0
        elif choice == "15 days rent":
            return rent / 2
        elif choice == "1 month rent":
            return rent
        elif choice in ("fixed amount", "negotiable") or has_manual:
            try:
                return float(self.manual_brokerage or 0)
            except (TypeError, ValueError):
                return 0
        return 0

    def calculate_move_in_cost(self):
        advance = self.get_advance_rent_amount()
        deposit = self.get_security_deposit_amount()
        brokerage = self.get_brokerage_amount()

        maintenance = 0
        m_type = (self.maintenance_type or "").strip().lower()
        has_maint_amount = self.maintenance_amount not in (None, 0, "", "0")

        if "extra" in m_type or has_maint_amount:
            maintenance = self.maintenance_amount or 0

        total = advance + deposit + brokerage + maintenance
        self.total_move_in_cost = round(total)

    # ═══════════════════════════════════════════════════════════════════════
    #  AUTO DESCRIPTIONS ENGINE (now integrates nearby_facilities)
    # ═══════════════════════════════════════════════════════════════════════
    def generate_auto_descriptions(self):
        pg_target = self.pg_for or "Co-Living"
        loc = self.locality or "a prime location"
        city_str = f", {self.city}" if self.city else ""
        furnish = self.furnishing_status or "Fully Furnished"
        r_type = (self.room_type or "Shared").title()

        summary = f"A premium {furnish} {r_type} occupancy PG accommodation for {pg_target} is available in {loc}{city_str}. "
        if self.monthly_rent:
            summary += f"Available at ₹{self.monthly_rent:,}/month per occupant. "
        if self.meals_available:
            summary += f"Nutritious daily meals ({self.meal_offerings or 'All Meals'}) are served on site. "
        summary += "Ideal for students and working professionals seeking a secure and well-connected residence."
        self.property_summary = summary

        long_desc = f"<p>Experience comfortable living at this highly sought-after <strong>{furnish} PG for {pg_target}</strong> located in <strong>{loc}{city_str}</strong>.</p>"
        if self.building_name:
            long_desc += f"<p>Situated in the secure premises of <strong>{self.building_name}</strong>, this space is designed to meet your daily lifestyle needs.</p>"

        long_desc += "<h3>Key Highlights & Pricing:</h3><ul>"
        long_desc += f"<li><strong>Room Type & Capacity:</strong> {r_type} Occupancy option ({self.total_beds or 1} beds registered). Suited for {self.best_suited_for or 'Students & Professionals'}.</li>"
        if self.monthly_rent:
            dep_val = self.get_security_deposit_amount()
            dep_str = f" (Security Deposit: ₹{dep_val:,.0f})" if dep_val else ""
            long_desc += f"<li><strong>Monthly Rent:</strong> ₹{self.monthly_rent:,}/ per person{dep_str}.</li>"
        long_desc += f"<li><strong>Furnishing:</strong> Fully {furnish} living quarters.</li>"
        if self.meals_available:
            long_desc += f"<li><strong>Food & Dining:</strong> Bundled meal provisioning offering {self.meal_offerings} ({self.meal_speciality or 'Standard'}).</li>"
        else:
            long_desc += "<li><strong>Food & Dining:</strong> Self-catering / meals not included.</li>"
        long_desc += "</ul>"

        long_desc += "<h3>House Rules & Terms:</h3><ul>"
        if self.minimum_stay:
            long_desc += f"<li><strong>Minimum Commitment:</strong> {self.minimum_stay} Month(s) minimum stay requirement.</li>"
        long_desc += f"<li><strong>Curfew & Access:</strong> {'24x7 Entry Permitted' if self.entry_24x7_allowed else f'Curfew applies at {self.curfew_time}'}.</li>"
        long_desc += f"<li><strong>Restrictions:</strong> Smoking {'Allowed' if self.smoking_allowed else 'Prohibited'}, Alcohol {'Allowed' if self.alcohol_consumption_allowed else 'Prohibited'}.</li>"
        long_desc += "</ul>"

        if self.amenities:
            long_desc += f"<h3>Top Amenities:</h3><p>Enjoy access to facilities including: <strong>{self.amenities}</strong>.</p>"

        # NEW — integrate Nearby Facilities into the description (was missing before)
        if self.nearby_facilities:
            long_desc += f"<h3>Nearby Facilities:</h3><p>Conveniently located with easy access to: <strong>{self.nearby_facilities}</strong>.</p>"

        long_desc += "<p>Schedule a visit today and secure your bed in this well-managed, resident-friendly PG!</p>"
        self.property_description = long_desc

    # ═══════════════════════════════════════════════════════════════════════
    #  SAVE OVERRIDE (now builds property_unique_key + SHA-256 duplicate hash,
    #  mirroring CommercialRentalProperty.save())
    # ═══════════════════════════════════════════════════════════════════════
    def save(self, *args, **kwargs):
        gender = self.pg_for or "Co-Living"
        b_name = f"in {self.building_name}" if self.building_name else ""
        loc = self.locality or ""
        city_name = f", {self.city}" if self.city else ""

        self.property_title = " ".join(filter(bool, [f"Premium {gender} PG", b_name, loc + city_name]))[:255]

        # Enforce Backend Calculations & Descriptions
        self.calculate_move_in_cost()
        self.generate_auto_descriptions()

        # Build Unique Key Only on First Create
        if self._state.adding:
            key_source = f"{self.address}|{self.locality}|{self.city}|{self.property_no}|{self.pincode}"
            self.property_unique_key = key_source.strip().lower().replace(" ", "")

        super().save(*args, **kwargs)

        # Recalculate Duplicate Group using SHA-256 Hash formatting
        if self.property_unique_key:
            hashed_group_id = hashlib.sha256(self.property_unique_key.encode('utf-8')).hexdigest()

            group_qs = PGColivingProperty.objects.filter(
                property_unique_key=self.property_unique_key,
                is_deleted=False,
            )
            total = group_qs.count()

            if total > 1:
                group_qs.update(
                    duplicate_count=total,
                    duplicate_group_id=hashed_group_id,
                    is_duplicate=True,
                )
                self.duplicate_count = total
                self.duplicate_group_id = hashed_group_id
                self.is_duplicate = True
            else:
                group_qs.update(
                    duplicate_count=1,
                    duplicate_group_id=None,
                    is_duplicate=False,
                )
                self.duplicate_count = 1
                self.duplicate_group_id = None
                self.is_duplicate = False

        self.generate_auto_faqs()

    # ═══════════════════════════════════════════════════════════════════════
    #  AUTO FAQ ENGINE — now generates a consistent 7 FAQs (mirrors Commercial)
    # ═══════════════════════════════════════════════════════════════════════
    def generate_auto_faqs(self):
        self.faqs.all().delete()
        faq_pool = []

        rent_str = f"₹{self.monthly_rent:,}" if self.monthly_rent else "Standard rates"
        dep_val = self.get_security_deposit_amount()
        dep_str = f"₹{dep_val:,.0f}" if dep_val else (self.security_deposit_type or "Applicable terms")

        # FAQ 1: Rent & Security Deposit
        faq_pool.append({
            "q": "What is the rent breakdown and security deposit for this PG accommodation?",
            "a": f"The room rent is {rent_str}/month per occupant under '{self.room_type or 'Shared'}' sharing. A refundable security deposit of {dep_str} is required upon onboarding.",
        })

        # FAQ 2: Eligibility & Furnishing
        faq_pool.append({
            "q": "Who is eligible to stay at this PG and what is the furnishing status?",
            "a": f"This property is specifically designated for {self.pg_for or 'Co-Living'}. The rooms and common quarters are {self.furnishing_status or 'Well Furnished'}, and it is best suited for {self.best_suited_for or 'Students & Working Professionals'}.",
        })

        # FAQ 3: Brokerage
        label = self.get_brokerage_label()
        val = self.get_brokerage_display_value()
        if str(self.brokerage_percentage or "").strip().lower() == "no brokerage":
            faq_pool.append({
                "q": f"Is there a {label.lower()} applicable on this PG booking?",
                "a": f"No, there is 0 {label.lower()} applicable on this property.",
            })
        else:
            faq_pool.append({
                "q": f"Is there a {label.lower()} applicable on this PG booking?",
                "a": f"Yes, the applicable {label.lower()} for this property is: {val}.",
            })

        # FAQ 4: Meals
        if self.meals_available:
            faq_pool.append({
                "q": "Are food and daily meals provided to residents?",
                "a": f"Yes, daily meals ({self.meal_offerings or 'Breakfast, Lunch, Dinner'}) are served, accommodating '{self.meal_speciality or 'Standard'}' dietary preferences.",
            })
        else:
            faq_pool.append({
                "q": "Are food and daily meals provided to residents?",
                "a": "No, daily meal provisioning is not included in the baseline boarding package.",
            })

        # FAQ 5: House Rules & Access
        curfew_note = "24x7 Entry Allowed" if self.entry_24x7_allowed else f"Curfew applies at {self.curfew_time or 'a fixed time'}"
        faq_pool.append({
            "q": "What are the primary house rules regarding access and lifestyle restrictions?",
            "a": (
                f"Access: {curfew_note}. Visitors: {'Allowed' if self.visitors_allowed else 'Restricted'} "
                f"(Opposite gender visitors: {'Allowed' if self.opposite_gender_visitors_allowed else 'Not Allowed'}). "
                f"Smoking is {'Allowed' if self.smoking_allowed else 'Strictly Prohibited'}, and Alcohol consumption is "
                f"{'Allowed' if self.alcohol_consumption_allowed else 'Strictly Prohibited'}. "
                f"Couples: {'Allowed' if self.couples_allowed else 'Not Allowed'}. Pets: {'Allowed' if self.pets_allowed else 'Not Allowed'}. "
                f"Cooking in rooms: {'Allowed' if self.cooking_allowed else 'Not Allowed'}."
            ),
        })

        # FAQ 6: Stay Terms (Minimum Stay / Notice / Lock-in / Availability)
        notice_str = f"{self.notice_period} day(s)" if self.notice_period else "a standard notice period"
        lockin_str = f"{self.lockin_period} day(s)" if self.lockin_period else "no specific lock-in period"
        min_stay_str = f"{self.minimum_stay} month(s)" if self.minimum_stay else "a standard minimum duration"
        avail_str = self.available_from.strftime('%d %b %Y') if self.available_from else "immediately upon confirmation"
        faq_pool.append({
            "q": "What are the minimum stay, notice period, and lock-in terms for this PG?",
            "a": f"A minimum stay of {min_stay_str} is required. The notice period before vacating is {notice_str}, with a lock-in period of {lockin_str}. Available from {avail_str}.",
        })

        # FAQ 7: Management & Verification
        faq_pool.append({
            "q": "How is this PG managed, and is police verification required for residents?",
            "a": (
                f"The property is managed by '{self.property_managed_by or 'the owner/caretaker'}', and the manager "
                f"{'stays on-site' if self.manager_stays else 'does not reside on the premises'}. "
                f"Police verification {'is mandatory' if self.police_verification_required else 'is not mandatory'} "
                f"for all incoming residents."
            ),
        })

        for item in faq_pool:
            PGColivingFAQ.objects.create(property=self, question=item["q"], answer=item["a"])

    def __str__(self):
        return f"{self.property_title or 'PG Property'} ({self.id})"


# ---- MODIFY existing PGPropertyImage: add category ----
class PGPropertyImage(models.Model):
    CATEGORY_CHOICES = [
        ('exterior', 'Building Exterior'),
        ('single_room', 'Single Occupancy'),
        ('double_room', 'Double Sharing'),
        ('multi_room', 'Triple / Multi Sharing'),
        ('lounge', 'Common Lounge'),
        ('kitchen', 'Shared Kitchen'),
        ('dining', 'Dining Area'),
        ('washroom', 'Bathroom / Washroom'),
        ('laundry', 'Laundry Area'),
        ('parking', 'Parking'),
        ('amenities', 'Common Amenities'),
        ('floor_plan', 'Floor Plan'),
    ]
    property = models.ForeignKey(PGColivingProperty, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to="pg/images/")
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='amenities')  # NEW
    sequence_order = models.PositiveIntegerField(default=0)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["category", "sequence_order", "uploaded_at"]


# ---- NEW: video model (same pattern as RentalResidentialVideo) ----
class PGColivingVideo(models.Model):
    SOURCE_CHOICES = [
        ('uploaded', 'Uploaded by User'),
        ('auto', 'Auto Generated Slideshow'),
        ('rm_assisted', 'RM Assisted Link'),
    ]
    property = models.ForeignKey(PGColivingProperty, on_delete=models.CASCADE, related_name="videos")
    video = models.FileField(upload_to="pg/videos/", null=True, blank=True)
    video_url = models.URLField(null=True, blank=True)
    source = models.CharField(max_length=20, choices=SOURCE_CHOICES, default='uploaded')
    created_at = models.DateTimeField(auto_now_add=True)


class PGColivingFAQ(models.Model):
    property = models.ForeignKey(PGColivingProperty, on_delete=models.CASCADE, related_name="faqs")
    question = models.CharField(max_length=255)
    answer = models.TextField()


class PGColivingActivityLog(models.Model):
    ACTION_CHOICES = [
        ("CREATE", "Property Entry Created"),
        ("UPDATE", "Record Update Action"),
        ("DELETE", "Deletion / Purge Record"),
    ]
    timestamp = models.DateTimeField(auto_now_add=True)
    user_identity = models.CharField(max_length=255, null=True, blank=True)
    user_role = models.CharField(max_length=100, null=True, blank=True)
    action_type = models.CharField(max_length=50, choices=ACTION_CHOICES)
    property_id = models.CharField(max_length=100, null=True, blank=True)
    action_payload = models.TextField(null=True, blank=True)
    status = models.CharField(max_length=20, default="SUCCESS")

    class Meta:
        ordering = ["-timestamp"]

# ══════════════════════════════════════════════════════════════════════════════
#  END PG / CO-LIVING LISTING MODELS
# ══════════════════════════════════════════════════════════════════════════════






    ############### Models End for Rental PG_COLIVING Property  model ############################ same in this this teh rental proeprty listing model so as per add the user role in ths also and give me the view of like this residenital view for data submit  



############### Models Starts for Resale Resindential  Property  model ############################ 





# Helper function to generate the custom primary key
def generate_resale_unique_property_id():
    # Example format: EFRES-A1B2C3D4
    return f"EFRES-{uuid.uuid4().hex[:8].upper()}"




class ResaleResidentialProperty(models.Model):
    id = models.CharField(
        max_length=50, 
        primary_key=True, 
        default=generate_resale_unique_property_id, 
        editable=False,
        help_text="Automated unique serial lookup tracking tag"
    )

    ############# Category Fields ###########################
    listing_type = models.CharField(max_length=255, blank=True, null=True)
    category = models.CharField(max_length=255, blank=True, null=True)

    ############## Listed By Section ###############################
    listed_by_type = models.CharField(max_length=255, blank=True, null=True)
    assigned_to = models.CharField(max_length=255, blank=True, null=True)
    listed_by_id = models.CharField(max_length=255, blank=True, null=True)
    listed_by_name = models.CharField(max_length=255, blank=True, null=True)
    listed_by_email = models.CharField(max_length=255, blank=True, null=True)
    listed_by_contact = models.CharField(max_length=255, blank=True, null=True)
    listed_by_role = models.CharField(max_length=255, blank=True, null=True)

    property_unique_key = models.CharField(max_length=255, blank=True, null=True, db_index=True)
    duplicate_count = models.PositiveIntegerField(default=0)
    duplicate_group_id = models.CharField(max_length=255, blank=True, null=True, db_index=True)   # <-- drives the brokerage label

    ############# Basic Information Section #############################
    property_title = models.CharField(max_length=255, blank=True, null=True)
    property_type = models.CharField(max_length=255, blank=True, null=True) 
    property_no = models.CharField(max_length=100, blank=True, null=True)
    society_type = models.CharField(max_length=100, blank=True, null=True)      
    wing_no = models.CharField(max_length=100, blank=True, null=True)      
    water_type = models.CharField(max_length=100, blank=True, null=True)      
    furnishing_status = models.CharField(max_length=100, blank=True, null=True)      
    property_age = models.CharField(max_length=100, blank=True, null=True)      
    facing_direction = models.CharField(max_length=100, blank=True, null=True)      
    occupancy_status = models.CharField(max_length=100, blank=True, null=True)      
    floor_no = models.PositiveIntegerField(default=1, null=True, blank=True)  # ADD THIS FIELD

    ################## Property Measurements Section ###########################
    super_builtup_area = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)             
    builtup_area = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)             
    carpet_area = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)             
    plot_area = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)             
    building_configuration = models.CharField(max_length=100, blank=True, null=True)
    total_floors = models.PositiveIntegerField(default=1, null=True, blank=True)
    brokerage_percentage = models.CharField(max_length=100, blank=True, null=True)
    manual_brokerage = models.PositiveIntegerField(default=0, null=True, blank=True)

    ################## Property Configuration Section ###########################
    bhk = models.CharField(max_length=100, blank=True, null=True)
    bathrooms = models.IntegerField(default=0, null=True, blank=True) 
    balconies = models.IntegerField(default=0, null=True, blank=True) 
    covered_parking = models.IntegerField(default=0, null=True, blank=True) 
    open_parking = models.CharField(max_length=100, blank=True, null=True)

    ############# Legal and Pricing Section ##########################
    no_of_owners = models.CharField(max_length=50, blank=True, null=True)   
    ownership_status = models.CharField(max_length=50, blank=True, null=True)   
    ownership_document_type = models.CharField(max_length=50, blank=True, null=True)   
    title_clarity_status = models.CharField(max_length=50, blank=True, null=True)   
    encumbrance_status = models.CharField(max_length=50, blank=True, null=True)   
    property_loan = models.CharField(max_length=5, blank=True, null=True, default='no')   
    loan_amount = models.DecimalField(max_digits=14, decimal_places=2, null=True, blank=True)
    existing_tenants = models.CharField(max_length=5, default='no', blank=True, null=True)         
    tenant_details = models.TextField(blank=True, null=True) 
    any_legal_dispute = models.CharField(max_length=5, default='no', blank=True, null=True)
    dispute_details = models.TextField(blank=True, null=True)  
    government_tax = models.CharField(max_length=5, default='no', blank=True, null=True)
    pending_tax_amount = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    sanctioning_authority = models.TextField(blank=True, null=True)

    ################### Pricing Details ##############################
    selling_price = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    price_per_sqft = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True) 
    price_negotiable = models.CharField(max_length=5, default='yes', blank=True, null=True)

    ############# Amenities and Facilities Section ############################ 
    nearby_facilities = models.TextField(blank=True, null=True) 
    amenities = models.TextField(blank=True, null=True)
    property_summary = models.TextField(blank=True, null=True)
    property_description = models.TextField(blank=True, null=True)
    user_description = models.TextField(blank=True, null=True)
    
    ################ Location Details Section #############################
    city = models.CharField(max_length=100, blank=True, null=True)
    locality = models.CharField(max_length=150, blank=True, null=True)
    building_name = models.CharField(max_length=200, blank=True, null=True)
    pincode = models.CharField(max_length=200, blank=True, null=True)
    property_landmark = models.CharField(max_length=200, blank=True, null=True)
    state = models.CharField(max_length=200, blank=True, null=True)
    google_maps_link = models.CharField(max_length=200, blank=True, null=True)
    pincode = models.CharField(max_length=200, blank=True, null=True)
    latitude = models.CharField(max_length=200, blank=True, null=True)
    longitude = models.CharField(max_length=200, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    
    ############## Property Images Docs and Videos Section ###########################
    floor_plan = models.ImageField(upload_to='properties/floor_plans/', null=True, blank=True) 
    video_option = models.CharField(max_length=200, blank=True, null=True)
    property_video = models.FileField(upload_to='properties/videos/', null=True, blank=True)
    property_video_link = models.CharField(max_length=200, blank=True, null=True)
    listed_elsewhere = models.CharField(max_length=150, blank=True, null=True)
    portal_name = models.CharField(max_length=150, blank=True, null=True)

    ############## Listing Uploaded By Section ############################
    uploaded_by_name = models.CharField(max_length=150, blank=True, null=True)
    uploaded_by_email = models.EmailField(blank=True, null=True)
    uploaded_by_contact = models.CharField(max_length=30, blank=True, null=True)
    uploaded_by_role = models.CharField(max_length=50, blank=True, null=True)
  
    upload_file_name = models.CharField(max_length=255, blank=True, null=True)
    # Add this new field to store the actual file
    upload_file = models.FileField(upload_to='property_uploads/files/', blank=True, null=True)

    ############### Timestamp and other details ###########################
    is_deleted = models.BooleanField(default=False)
    is_duplicate = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(null=True, blank=True)
    deleted_by = models.CharField(max_length=150, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    listing_status = models.CharField(max_length=150, blank=True, null=True)
    approval_status = models.CharField(max_length=150, blank=True, null=True)

    class Meta:
        verbose_name = 'Resale Residential Property'
        verbose_name_plural = 'Resale Residential Properties'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.property_title or 'Property Block'} ({self.id})"

    # ═══════════════════════════════════════
    # HELPER: CLEAN TEXT FIELDS
    # ═══════════════════════════════════════
    def _clean_text_field(self, value):
        """Cleans list-like strings and returns a comma-separated string."""
        if not value:
            return ""
        if isinstance(value, list):
            return ", ".join(str(item).strip() for item in value if item)
        if isinstance(value, str):
            cleaned = value.replace("[", "").replace("]", "").replace("'", "").replace('"', "")
            if "," in cleaned:
                return ", ".join(item.strip() for item in cleaned.split(",") if item.strip())
            return cleaned.strip()
        return str(value).strip()

    from decimal import Decimal, InvalidOperation

    def _fmt_amount(self, value):   
        """Return the numeric value formatted with exactly 2 decimal places,
        no thousands separators — matches how it's stored in the DB."""
        if value is None or value == "":
            return "0.00"
        try:
            return f"{Decimal(str(value)):.2f}"
        except (InvalidOperation, ValueError, TypeError):
            return str(value)

    # ═══════════════════════════════════════
    # AUTO DESCRIPTION GENERATOR
    # ═══════════════════════════════════════
    def generate_auto_descriptions(self):
        """Generates property summary and detailed description based on field data."""
        
        bhk_str = str(self.bhk) if self.bhk else ""
        p_type = str(self.property_type) if self.property_type else "Property"
        furnish = str(self.furnishing_status) if self.furnishing_status else "well-maintained"
        loc = str(self.locality) if self.locality else "a prime location"
        city_str = f", {self.city}" if self.city else ""
        
        try: 
            price_val = self.selling_price or 0
        except:
            price_val = 0

        # -----------------------------------
        # 1. SUMMARY TEXT
        # -----------------------------------
        summary = f"A premium {furnish} {bhk_str} {p_type} is available for sale in {loc}{city_str}. "
        
        if price_val > 0:
            summary += f"Priced competitively at ₹{self._fmt_amount(price_val)}. "
            
        if self.builtup_area:
            summary += f"It offers a spacious built-up area of {self._fmt_amount(self.builtup_area)} sq.ft. "
            
        summary += f"Set in a {self.society_type or 'secure'} environment, this home is ideal for families looking for comfort and convenience."
        
        self.property_summary = summary.strip()

        # -----------------------------------
        # 2. LONG DESCRIPTION
        # -----------------------------------
        bhk_title = f"{bhk_str} {p_type}".strip()
        long_desc = f"<p>Upgrade your lifestyle with this beautifully designed <strong>{furnish} {bhk_title}</strong> located in the highly sought-after neighborhood of <strong>{loc}{city_str}</strong>.</p>"

        if self.building_name:
            long_desc += f"<p>Situated in the prestigious <strong>{self.building_name}</strong>, this residence guarantees a perfect blend of privacy, modern architecture, and community living.</p>"

        # --- Section A: Property Highlights ---
        long_desc += "<h3>Property Highlights:</h3><ul>"
        
        if self.builtup_area:
            carpet_str = f" (Carpet Area: {self._fmt_amount(self.carpet_area)} sq.ft.)" if self.carpet_area else ""
            long_desc += f"<li><strong>Space & Dimensions:</strong> Features a generous built-up area of {self._fmt_amount(self.builtup_area)} sq.ft.{carpet_str}</li>"
            
        if price_val > 0:
            neg_str = " (Negotiable)" if str(self.price_negotiable).lower() == 'yes' else ""
            long_desc += f"<li><strong>Pricing:</strong> Offered at ₹{self._fmt_amount(price_val)}{neg_str}</li>"
            
        long_desc += f"<li><strong>Condition & Age:</strong> The property is {furnish} and falls under the '{self.property_age or 'Standard'}' age bracket.</li>"
        
        if hasattr(self, 'floor_no') and self.floor_no is not None and self.total_floors:
            long_desc += f"<li><strong>Floor Details:</strong> Comfortably positioned on floor {self.floor_no} of a {self.total_floors}-story building.</li>"
            
        if self.facing_direction:
            long_desc += f"<li><strong>Vastu & Orientation:</strong> {self.facing_direction}-facing property, ensuring excellent natural light and ventilation.</li>"
            
        if self.ownership_status:
            long_desc += f"<li><strong>Ownership:</strong> {self.ownership_status} ownership title, ensuring a smooth transfer process.</li>"
            
        long_desc += "</ul>"

        # --- Section B: Configurations ---
        if any([self.bathrooms, self.balconies, self.covered_parking, self.open_parking]):
            long_desc += "<h3>Layout Configurations:</h3><ul>"
            if self.bathrooms:
                long_desc += f"<li><strong>Bathrooms:</strong> {self.bathrooms} well-fitted bathroom(s).</li>"
            if self.balconies:
                long_desc += f"<li><strong>Balconies:</strong> {self.balconies} spacious balcony(s) offering pleasant views.</li>"
            if self.covered_parking or self.open_parking:
                park_str = []
                if self.covered_parking: 
                    park_str.append(f"{self.covered_parking} covered")
                if self.open_parking: 
                    park_str.append(f"{self.open_parking} open")
                long_desc += f"<li><strong>Parking:</strong> Includes {' and '.join(park_str)} dedicated parking spot(s).</li>"
            long_desc += "</ul>"

        # --- Section C: Amenities & Location ---
        amenities_str = self._clean_text_field(self.amenities)
        if amenities_str.strip():
            long_desc += f"<h3>Lifestyle Amenities:</h3><p>Residents enjoy exclusive access to top-tier community facilities including: <strong>{amenities_str}</strong>.</p>"

        facilities_str = self._clean_text_field(self.nearby_facilities)
        if facilities_str.strip():
            long_desc += f"<h3>Location Advantages:</h3><p>Strategically located with seamless connectivity to major hubs, schools, hospitals, and: <strong>{facilities_str}</strong>.</p>"

        long_desc += "<p>Don't miss this opportunity to secure your dream home. Contact us today to schedule a site visit and discuss further details!</p>"

        self.property_description = long_desc

    # ═══════════════════════════════════════
    # SAVE METHOD
    # ═══════════════════════════════════════
    def save(self, *args, **kwargs):
        # 1. Price Per Sq.Ft calculation using Decimal fields
        if self.selling_price and self.builtup_area:
            try:
                area = Decimal(str(self.builtup_area))
                price = Decimal(str(self.selling_price))
                if area > 0:
                    self.price_per_sqft = (price / area).quantize(Decimal('0.01'))
            except (ValueError, TypeError, Decimal.InvalidOperation):
                pass

        # 2. Automated Title Generation
        if not self.property_title:
            bhk_string = str(self.bhk).upper() if self.bhk else ""
            type_string = str(self.property_type).capitalize() if self.property_type else "Property"
            project_context = f" in {self.building_name}" if self.building_name else ""
            location_context = f" at {self.locality}" if self.locality else ""
            city_context = f", {self.city}" if self.city else ""
            
            constructed_title = f"Spacious {bhk_string} {type_string}{project_context}{location_context}{city_context}"
            self.property_title = constructed_title.strip()

        # 3. Trigger Auto Description Generation BEFORE saving
        self.generate_auto_descriptions()

        # 4. Save Record
        super().save(*args, **kwargs)
        
        # 5. Dynamic Automated FAQ Engine Execution
        self.generate_auto_faqs()

    # ═══════════════════════════════════════
    # AUTO FAQ GENERATOR
    # ═══════════════════════════════════════
    def generate_auto_faqs(self):
        """Dynamic programmatic asset compliance engine for residential properties."""
        from .models import ResaleResidentialFAQ

        self.faqs.all().delete()
        faq_pool = []

        price_val = self.selling_price or 0
        loan_val = self.loan_amount or 0
        tax_val = self.pending_tax_amount or 0
        per_sqft_val = self.price_per_sqft or 0

        # FAQ 1: Financial & Valuation Structure
        if price_val > 0:
            loan_str = f" A lingering loan structure of ₹{self._fmt_amount(loan_val)} is declared against the property asset." if str(self.property_loan).lower() == 'yes' else " The property is declared free from active banking or mortgage encumbrances."
            tax_str = f" Outstanding municipal tax dues total ₹{self._fmt_amount(tax_val)}." if str(self.government_tax).lower() == 'yes' else " No pending sovereign tax liabilities are declared."
            
            brokerage_val = self.brokerage_percentage if self.brokerage_percentage else self.manual_brokerage
            brokerage_str = f" Professional commission applies via a system format of '{brokerage_val}'." if brokerage_val else " The pricing model avoids active external brokerage terms."
            
            faq_pool.append({
                "question": f"What is the total acquisition cost, financial status, and transactional framework for this {self.bhk or 'residential'} layout?",
                "answer": f"The strategic market valuation is established at ₹{self._fmt_amount(price_val)}, arriving at an estimated valuation metric of ₹{self._fmt_amount(per_sqft_val)} per sq.ft. The asset ownership confirms that price flexibility is: '{self.price_negotiable or 'No'}'.{loan_str}{tax_str}{brokerage_str}"
            })

        # FAQ 2: Architectural Spatial Profile & Inventory
        if self.builtup_area:
            plot_str = f" alongside an expansive baseline plot layout tracking at {self._fmt_amount(self.plot_area)} sq.ft." if self.plot_area else "."
            faq_pool.append({
                "question": "What are the structural measurement specifications and architectural interior configuration summaries?",
                "answer": f"The space introduces a premium built-up area of {self._fmt_amount(self.builtup_area)} sq.ft. matched to a high-efficiency liveable carpet operational space of {self._fmt_amount(self.carpet_area)} sq.ft.{plot_str} Internal room configurations trace out a structural {self.bhk or 'spacious'} asset layout completed with {self.bathrooms or 0} master/guest bathrooms and {self.balconies or 0} exterior ventilation balconies."
            })

        # FAQ 3: Property Logistics, Elevation & Essential Utilities
        floor_info = f"floor level {self.floor_no}" if hasattr(self, 'floor_no') and self.floor_no else "a premium floor level"
        total_floors_info = f"{self.total_floors}" if self.total_floors else "multiple"
        facing_info = f"'{self.facing_direction or 'Standard Orientation'}'"
        water_info = f"'{self.water_type or 'Municipal/Borewell'}'"
        society_info = f"'{self.society_type or 'Gated Community'}'"
        
        faq_pool.append({
            "question": "What structural tiering, property orientation, and primary utility access lines service this residence?",
            "answer": f"This residential inventory is positioned on {floor_info} within a comprehensive residential tower footprint rising to a total height of {total_floors_info} levels. The architectural layout faces the {facing_info} compass line. Local utilities confirm an integrated {water_info} water grid integration, set within a contextually secure {society_info} community format."
        })

        # FAQ 4: Legal Framework, Historical Tenure & Existing Occupations
        dispute_str = f" Note: Structural tracking records details regarding legal contest/disputes: '{self.dispute_details}'." if str(self.any_legal_dispute).lower() == 'yes' else " The real estate title passes complete risk screening with zero pending disputes or litigations."
        tenant_str = f" The asset currently houses sitting occupants under terms: {self.tenant_details or 'Standard Tenancy'}." if str(self.existing_tenants).lower() == 'yes' else " The block is offered entirely vacant for seamless operational transition."
        
        faq_pool.append({
            "question": "What regulatory ownership conditions, legal checks, and occupational timelines govern this block?",
            "answer": f"The legal ownership profile functions under a standard '{self.ownership_status or 'Freehold'}' deed register configuration, split across a multi-party listing headcount of {self.no_of_owners or 1} registered owner(s). Structural asset age tracks at '{self.property_age or 'New'}', with operational possession availability starting on immediate terms.{dispute_str}{tenant_str}"
        })

        # FAQ 5: Parking Distribution & Community Infrastructure
        if self.covered_parking or self.open_parking:
            faq_pool.append({
                "question": "What vehicle allocations and parking spaces are registered to this specific layout?",
                "answer": f"The residential tracking matrix assigns a dedicated vehicle storage allowance, separating space variables into {self.covered_parking or 0} secure covered parking bays and {self.open_parking or 'shared'} open common parking zones."
            })

        # FAQ 6: Geo-Location Framework & Feature Index
        amenities_str = self._clean_text_field(self.amenities) or "Standard Features"
        facilities_str = self._clean_text_field(self.nearby_facilities) or "Standard Locality Connections"
        
        faq_pool.append({
            "question": "Where is this asset located and what auxiliary amenities map to this residential zone?",
            "answer": f"The real estate asset is situated within the corporate geographic coordinates of {self.locality or 'Premium Locality'}, {self.city or 'Metropolitan City'}, cataloged inside the development project known as '{self.building_name or 'Independent Premium Block'}'. Full postal logistics resolve to: {self.address or 'Contact for details'}. Integrated lifestyle assets contain: {amenities_str}, matching local connectivity points of: {facilities_str}."
        })

        # FAQ 7: Registry Audit & Management Verification Profile
        faq_pool.append({
            "question": "Who represents this asset registry listing and what operational metadata marks its entry?",
            "answer": f"The primary asset title holder is validated under the registration index of {self.listed_by_name or 'Property Owner'} ({self.occupancy_status or 'Resident'}), accessible via verified contact metrics: {self.listed_by_contact or 'Contact Agent'} / {self.listed_by_email or 'info@property.com'}. System auditing records confirm deployment management by {self.uploaded_by_name or 'System Desk'} acting in the corporate capacity of {self.uploaded_by_role or 'Listing Administrator'}, tracking under reference ID {self.id}."
        })

        for item in faq_pool:
            ResaleResidentialFAQ.objects.create(
                property=self, 
                question=item["question"], 
                answer=item["answer"]
            )


# ═══════════════════════════════════════
# FAQ MODEL
# ═══════════════════════════════════════
class ResaleResidentialFAQ(models.Model):
    property = models.ForeignKey(ResaleResidentialProperty, on_delete=models.CASCADE, related_name='faqs')
    question = models.CharField(max_length=255)
    answer = models.TextField()

    def __str__(self):
        return f"FAQ for Residential Property: {self.property.id}"


# ═══════════════════════════════════════
# PROPERTY IMAGE MODEL
# ═══════════════════════════════════════
class ResalePropertyImage(models.Model):
    CATEGORY_CHOICES = [
        ('exterior', 'Exterior / Building'),
        ('living',   'Living / Dining'),
        ('bedroom',  'Bedroom'),
        ('kitchen',  'Kitchen'),
        ('bathroom', 'Bathroom'),
        ('balcony',  'Balcony'),
        ('others',   'Others'),
    ]
    property = models.ForeignKey(ResaleResidentialProperty, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to="resale_rent/")
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='others')
    sequence_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["category", "sequence_order"]


class ResaleResidentialVideo(models.Model):
    SOURCE_CHOICES = [('uploaded', 'Manually Uploaded'), ('auto', 'Auto Generated Slideshow'),('rm_assisted', 'RM Assisted Link'),]
    property = models.ForeignKey(ResaleResidentialProperty, on_delete=models.CASCADE, related_name="video")
    video = models.FileField(upload_to="residential_resale/videos/")
    video_url = models.URLField(null=True, blank=True)
    source = models.CharField(max_length=100, choices=SOURCE_CHOICES, default='auto')
    video_status = models.CharField(max_length=255, blank=True, null=True,default="Pending")
    created_at = models.DateTimeField(auto_now_add=True)

    def youtube_thumbnail(self):
        import re
        if self.source == 'rm_assisted' and self.video_url:
            match = re.search(
                r'(?:youtube\.com/watch\?v=|youtu\.be/|youtube\.com/shorts/)([A-Za-z0-9_-]{6,})',
                self.video_url
            )
            if match:
                return f"https://img.youtube.com/vi/{match.group(1)}/hqdefault.jpg"
        return None


############## Models End for Resale Resindential Property  model ################




############## Models Start for Resale Commericial  Property  model ############################ 









# Helper function to generate the custom primary key
def generate_property_id():
    return f"EFCOM-{uuid.uuid4().hex[:8].upper()}"


class CommercialResaleProperty(models.Model):

    id = models.CharField(
        max_length=50,
        primary_key=True,
        default=generate_property_id,
        editable=False,
        help_text="Automated unique serial lookup tracking tag"
    )

    ############# Category Fields ###########################
    
    listing_type = models.CharField(max_length=255, blank=True, null=True)
    category = models.CharField(max_length=255, blank=True, null=True)

    ############## Listed By Section ###############################

    listed_by_type = models.CharField(max_length=255, blank=True, null=True)
    assigned_to = models.CharField(max_length=255, blank=True, null=True)
    listed_by_id = models.CharField(max_length=255, blank=True, null=True)
    listed_by_name = models.CharField(max_length=255, blank=True, null=True)
    listed_by_email = models.CharField(max_length=255, blank=True, null=True)
    listed_by_contact = models.CharField(max_length=255, blank=True, null=True)
    listed_by_role = models.CharField(max_length=255, blank=True, null=True)

    property_unique_key = models.CharField(max_length=255, blank=True, null=True, db_index=True)
    duplicate_count = models.PositiveIntegerField(default=0)
    duplicate_group_id = models.CharField(max_length=255, blank=True, null=True, db_index=True)   # <-- drives the brokerage label

    ############ Basic Information Section #############################

    property_title = models.CharField(max_length=255, blank=True, null=True)
    property_type = models.CharField(max_length=50,blank=True,null=True)  
    property_category = models.CharField(max_length=50,blank=True,null=True)  
    property_no = models.CharField(max_length=100, blank=True, null=True) 
    occupancy_status = models.CharField(max_length=50,blank=True,null=True)
    zone_type = models.CharField(max_length=50,blank=True,null=True)
    location_hub = models.CharField(max_length=50, blank=True, null=True)
    property_condition = models.CharField(max_length=50,blank=True,null=True)
    property_age = models.CharField(max_length=50,blank=True,null=True)
    furnishing_status = models.CharField(max_length=50,blank=True,null=True)
    facing_direction = models.CharField(max_length=50,blank=True,null=True)
    bhk = models.CharField(max_length=50,blank=True,null=True)

    ################# Area Measurements Section ##############################

    super_builtup_area = models.DecimalField(max_digits=12, decimal_places=2,blank=True,null=True)
    builtup_area = models.DecimalField(max_digits=12, decimal_places=2,blank=True,null=True)
    carpet_area = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    plot_area = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)

    ############# Commercial Specifications Section ############################

    no_staircases = models.PositiveIntegerField(default=0, blank=True, null=True)
    passenger_lifts = models.PositiveIntegerField(default=0, blank=True, null=True)
    service_lifts = models.PositiveIntegerField(default=0, blank=True, null=True)
    num_cabins = models.PositiveIntegerField(default=0, blank=True, null=True)
    meeting_rooms = models.PositiveIntegerField(default=0, blank=True, null=True)
    min_seats = models.PositiveIntegerField(default=0, blank=True, null=True)
    max_seats = models.PositiveIntegerField(default=0, blank=True, null=True)
    private_parking = models.PositiveIntegerField(default=0, blank=True, null=True)
    public_parking = models.PositiveIntegerField(default=0, blank=True, null=True)

    brokerage_percentage = models.CharField(max_length=100, blank=True, null=True)
    manual_brokerage = models.PositiveIntegerField(default=0, blank=True, null=True)

    ############### Ownership and Legal Details Section #######################
   
    no_of_owners = models.CharField(max_length=20,blank=True,null=True)
    ownership_status = models.CharField(max_length=20,blank=True,null=True)
    ownership_document_type = models.CharField(max_length=20,blank=True,null=True)
    title_clarity_status = models.CharField(max_length=20,blank=True,null=True)
    encumbrance_status = models.CharField(max_length=20,blank=True,null=True)
    property_loan = models.CharField(max_length=5, default='no')
    loan_amount = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    existing_tenants = models.CharField(max_length=5, default='no')
    tenant_details = models.TextField(blank=True, null=True)
    any_legal_dispute = models.CharField(max_length=5, default='no')
    dispute_details = models.TextField(blank=True, null=True)
    government_tax = models.CharField(max_length=5, default='no')
    pending_tax_amount = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    fire_safety_noc = models.CharField(max_length=5, blank=True, null=True)
    sanctioning_authority = models.TextField(blank=True, null=True)

    ################# Pricing Details Section ################################

    selling_price = models.DecimalField(max_digits=15, decimal_places=2)
    price_per_sqft = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True) 

    ############# Ameneties and Neacby Facilities Section ############################

    nearby_facilities = models.TextField(blank=True, null=True)  
    amenities = models.TextField(blank=True, null=True)
    property_summary = models.TextField(blank=True, null=True)
    property_description = models.TextField(blank=True, null=True)
    user_description = models.TextField(blank=True, null=True)

    ############## Address Details Section ############################

    city = models.CharField(max_length=100,blank=True,null=True)
    locality = models.CharField(max_length=100,blank=True,null=True)
    building_name = models.CharField(max_length=100,blank=True,null=True)
    address = models.TextField(blank=True,null=True)
    pincode = models.CharField(max_length=100,blank=True,null=True)
    property_landmark = models.CharField(max_length=100,blank=True,null=True)
    state = models.CharField(max_length=100,blank=True,null=True)
    google_maps_link = models.CharField(max_length=100,blank=True,null=True)
    latitude = models.CharField(max_length=100,blank=True,null=True)
    longitude = models.CharField(max_length=100,blank=True,null=True)

    ############# Property Images Docs and Videos Sections #########################

    floor_plan = models.ImageField(upload_to='commercial/floor_plans/', null=True, blank=True) 
    video_option = models.CharField(max_length=200, blank=True, null=True)
    property_video = models.FileField(upload_to='properties/videos/', null=True, blank=True)
    property_video_link = models.CharField(max_length=200, blank=True, null=True)
    listed_elsewhere = models.CharField(max_length=150, blank=True, null=True)
    portal_name = models.CharField(max_length=150, blank=True, null=True)

    ############# Listing Uploaded By Section ############################

    uploaded_by_name = models.CharField(max_length=100, blank=True, null=True)
    uploaded_by_email = models.EmailField(blank=True, null=True)
    uploaded_by_contact = models.CharField(max_length=30, blank=True, null=True)
    uploaded_by_role = models.CharField(max_length=50, blank=True, null=True)
    upload_file_name = models.CharField(max_length=255, blank=True, null=True)

    ############# Timestamp and other details section ##########################

    is_deleted = models.BooleanField(default=False)
    is_duplicate = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(null=True, blank=True)
    deleted_by = models.CharField(max_length=150, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    listing_status = models.CharField(max_length=150, blank=True, null=True)
    approval_status = models.CharField(max_length=150, blank=True, null=True)

    class Meta:
        verbose_name = "Commercial Property"
        verbose_name_plural = "Commercial Properties"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.property_title or 'Commercial Space'} ({self.id})"

    from decimal import Decimal, InvalidOperation

    # ═══════════════════════════════════════
    # HELPER FORMATTER
    # ═══════════════════════════════════════
    def _fmt_amount(self, value):   
        """Return the numeric value formatted with exactly 2 decimal places,
        no thousands separators — matches how it's stored in the DB."""
        if value is None or value == "":
            return "0.00"
        try:
            return f"{Decimal(str(value)):.2f}"
        except (InvalidOperation, ValueError, TypeError):
            return str(value)

    # ═══════════════════════════════════════
    # AUTO DESCRIPTION GENERATOR
    # ═══════════════════════════════════════
    def generate_auto_descriptions(self):
        # Fetch safe fallbacks using exact model field names
        p_type = str(self.property_type).replace('_', ' ').title() if self.property_type else "Commercial Space"
        p_cond = str(self.property_condition).lower() if self.property_condition else "well-maintained"
        loc = str(self.locality).strip() if self.locality else "a prime commercial area"
        city_str = f", {self.city}" if self.city else ""
        
        try:
            price_val = int(float(str(self.selling_price or 0).strip()))
        except (ValueError, TypeError):
            price_val = 0

        # -----------------------------------
        # 1. SUMMARY TEXT (Always Regenerates)
        # -----------------------------------
        summary = f"A premium {p_cond} {p_type} is available for sale in {loc}{city_str}. "
        
        if price_val > 0:
            summary += f"Priced competitively at ₹{price_val:,}. "
            
        if self.builtup_area:
            area = str(self.builtup_area).rstrip('0').rstrip('.') if '.' in str(self.builtup_area) else str(self.builtup_area)
            summary += f"It offers a spacious built-up area of {area} sq.ft. "
            
        summary += "Ideal for investors and businesses looking for a strategic corporate footprint."
        
        # Overwrite the field
        self.property_summary = summary.strip()

        # -----------------------------------
        # 2. LONG DESCRIPTION (Always Regenerates)
        # -----------------------------------
        long_desc = f"<p>Establish your business or expand your investment portfolio with this strategically located <strong>{p_cond} {p_type}</strong> in <strong>{loc}{city_str}</strong>.</p>"

        if self.building_name:
            long_desc += f"<p>Situated within the highly sought-after commercial complex of <strong>{self.building_name}</strong>, this property ensures excellent visibility, high footfall, and professional appeal for your brand.</p>"

        # --- Section A: Property Highlights ---
        long_desc += "<h3>Core Specifications:</h3><ul>"
        
        if self.builtup_area:
            area = str(self.builtup_area).rstrip('0').rstrip('.') if '.' in str(self.builtup_area) else str(self.builtup_area)
            carpet_str = f" (Carpet Area: {self.carpet_area} sq.ft.)" if self.carpet_area else ""
            plot_str = f" [Plot Area: {self.plot_area} sq.ft.]" if self.plot_area else ""
            long_desc += f"<li><strong>Space & Dimensions:</strong> Generous built-up area of {area} sq.ft.{carpet_str}{plot_str}, offering flexibility for diverse commercial layouts.</li>"
            
        if price_val > 0:
            long_desc += f"<li><strong>Pricing:</strong> Offered at ₹{price_val:,}.</li>"
            
        long_desc += f"<li><strong>Condition & Age:</strong> The space is currently provided in a {p_cond} status and is {self.property_age or '0-1'} years old.</li>"
        
        if self.ownership_status:
            long_desc += f"<li><strong>Ownership:</strong> {self.ownership_status.capitalize()} title, facilitating a smooth transfer process.</li>"
            
        if self.zone_type:
            long_desc += f"<li><strong>Zoning:</strong> Officially designated as a {self.zone_type.capitalize()} zone.</li>"
            
        long_desc += "</ul>"

        # --- Section B: Workplace & Infrastructure Configurations ---
        if any([self.min_seats, self.num_cabins, self.meeting_rooms, self.passenger_lifts, self.private_parking, self.public_parking]):
            long_desc += "<h3>Infrastructure & Layout Configurations:</h3><ul>"
            
            if self.min_seats or self.max_seats:
                min_s = self.min_seats or 0
                max_s = f" to {self.max_seats}" if self.max_seats else ""
                long_desc += f"<li><strong>Seating Capacity:</strong> Optimized to accommodate {min_s}{max_s} workstations comfortably.</li>"
                
            if self.num_cabins:
                long_desc += f"<li><strong>Private Cabins:</strong> Features {self.num_cabins} dedicated private cabin(s) for executive use.</li>"
                
            if self.meeting_rooms:
                long_desc += f"<li><strong>Meeting Rooms:</strong> {self.meeting_rooms} integrated conference/meeting room(s).</li>"
                
            if self.passenger_lifts or self.service_lifts:
                lifts = []
                if self.passenger_lifts: lifts.append(f"{self.passenger_lifts} passenger")
                if self.service_lifts: lifts.append(f"{self.service_lifts} service")
                long_desc += f"<li><strong>Vertical Transit:</strong> Equipped with {' and '.join(lifts)} lift(s).</li>"
                
            if self.private_parking or self.public_parking:
                park_str = []
                if self.private_parking: park_str.append(f"{self.private_parking} private")
                if self.public_parking: park_str.append(f"{self.public_parking} public")
                long_desc += f"<li><strong>Parking:</strong> Includes {' and '.join(park_str)} parking spots.</li>"
                
            long_desc += "</ul>"

        # --- Section C: Amenities & Facilities ---
        if self.amenities:
            amenities_str = ""
            if isinstance(self.amenities, list):
                amenities_str = ", ".join(str(a) for a in self.amenities)
            elif isinstance(self.amenities, str):
                amenities_str = str(self.amenities).replace("[", "").replace("]", "").replace("'", "").replace('"', "")
            if amenities_str.strip():
                long_desc += f"<h3>Facilities & Amenities:</h3><p>The building provides excellent amenities to support your operations, including: <strong>{amenities_str}</strong>.</p>"

        # --- Section D: Nearby Locations ---
        if self.nearby_facilities:
            facilities_str = ""
            if isinstance(self.nearby_facilities, list):
                facilities_str = ", ".join(str(f) for f in self.nearby_facilities)
            elif isinstance(self.nearby_facilities, str):
                facilities_str = str(self.nearby_facilities).replace("[", "").replace("]", "").replace("'", "").replace('"', "")
            if facilities_str.strip():
                long_desc += f"<h3>Location Advantages:</h3><p>Strategically located with excellent connectivity, offering immediate proximity to: <strong>{facilities_str}</strong>.</p>"

        # Closing Statement
        long_desc += "<p>Don't miss out on this fantastic opportunity to secure a premium commercial asset. Contact us today to schedule a site visit or to discuss further details.</p>"

        # Overwrite the field
        self.property_description = long_desc

    # ═══════════════════════════════════════
    # SAVE METHOD
    # ═══════════════════════════════════════
    def save(self, *args, **kwargs):
        # 1. Auto-calculate price_per_sqft — never trust the form value
        if self.selling_price and self.builtup_area:
            try:
                area = float(self.builtup_area)
                price = float(self.selling_price)
                if area > 0:
                    self.price_per_sqft = round(price / area, 2)
            except (ValueError, TypeError):
                pass

        # 2. Auto-generate title if not already set
        if not self.property_title:
            type_lbl = self.property_type.replace('_', ' ').title() if self.property_type else "Commercial"
            area_lbl = f"{int(float(self.builtup_area))} Sqft" if self.builtup_area else ""
            building_ctx = f" in {self.building_name}" if self.building_name else ""
            locality_ctx = f" at {self.locality}, {self.city}" if self.locality and self.city else ""

            constructed_title = f"Premium {area_lbl} {type_lbl}{building_ctx}{locality_ctx}"
            self.property_title = " ".join(constructed_title.split())

        # 3. Trigger Auto Description Generation BEFORE saving
        self.generate_auto_descriptions()

        # 4. Save Record
        super().save(*args, **kwargs)

        # 5. Auto-generate FAQs after save
        self.generate_auto_faqs()

    # ═══════════════════════════════════════
    # AUTO FAQ GENERATOR
    # ═══════════════════════════════════════
    def generate_auto_faqs(self):
        """Dynamic programmatic structural commercial data engine."""
        self.faqs.all().delete()
        faq_pool = []

        try:
            price_val = int(float(str(self.selling_price or 0).strip()))
        except (ValueError, TypeError):
            price_val = 0
            
        try:
            loan_val = int(float(str(self.loan_amount or 0).strip()))
        except (ValueError, TypeError):
            loan_val = 0
            
        try:
            tax_val = int(float(str(self.pending_tax_amount or 0).strip()))
        except (ValueError, TypeError):
            tax_val = 0

        # FAQ 1: Capital Structure & Transaction Parameters
        if price_val > 0:
            brokerage_details = (
                f" Managed via a designated brokerage model tracking at "
                f"{self.brokerage_percentage or self.manual_brokerage or 'standard commercial agency margins'}."
                if self.brokerage_percentage or self.manual_brokerage
                else " Dispatched direct from corporate inventory avoiding custom external agent brokerage rules."
            )
            faq_pool.append({
                "q": f"What are the financial terms, valuation details, and fee structures for this {self.property_type or 'Commercial Space'}?",
                "a": f"The commercial capital price point is pinned at ₹{price_val:,}, scaling out to an evaluation value of "
                     f"₹{self.price_per_sqft or 0:,} per sq.ft of built-up floorplate.{brokerage_details}"
            })

        # FAQ 2: Operational Scale & Spatial Boundaries
        if self.builtup_area:
            carpet_str = f" paired with a core carpet workspace footprint of {self.carpet_area} sq.ft." if self.carpet_area else "."
            plot_str = f" accompanied by a dedicated commercial plot baseline tracking at {self.plot_area} sq.ft." if self.plot_area else ""
            faq_pool.append({
                "q": "What exact area dimensions and horizontal space metrics define this business layout?",
                "a": f"The architectural blueprint declares a gross overall built-up operational footprint of "
                     f"{self.builtup_area} sq.ft.{carpet_str}{plot_str}"
            })

        # FAQ 3: Zoning Infrastructure & Strategic Logistics Hubs
        faq_pool.append({
            "q": "Which municipal zone covers this layout and what is its corporate hub placement?",
            "a": f"This property functions safely under an official '{self.zone_type or 'Commercial'}' corporate zone designation, anchored "
                 f"structurally inside a specialized '{self.location_hub or 'Standalone/Corporate Hub'}' logistical market hub "
                 f"configuration. Structural inspection records identify the infrastructure asset age as: '{self.property_age or '0-1'}' "
                 f"years, offering structural material integrity categorized as '{self.property_condition or 'Well Maintained'}'."
        })

        # FAQ 4: Operational Workplace Capacity & Workflow Systems
        if self.min_seats or self.num_cabins or self.meeting_rooms:
            faq_pool.append({
                "q": "What executive seating capacities, private offices, and conference specs are integrated?",
                "a": f"The interior fit-out profiles are structured to stabilize a high-density corporate workflow team ranging from "
                     f"a base floor threshold of {self.min_seats or 0} seats up to a scalability peak of {self.max_seats or 0} "
                     f"active workstations. Core management infrastructure features {self.num_cabins or 0} private executive cabins "
                     f"and {self.meeting_rooms or 0} dedicated strategic meeting/board rooms."
            })

        # FAQ 5: Core Vertical Logistics & Mobility Infrastructure
        faq_pool.append({
            "q": "What logistical mobility assets, fire escape systems, and parking bays service the premises?",
            "a": f"Internal building traffic management handles vertical transit density utilizing {self.passenger_lifts or 0} "
                 f"high-speed passenger elevators coupled with {self.service_lifts or 0} dedicated heavy-duty cargo/service lift "
                 f"corridors. Emergency exit routes are maintained via {self.no_staircases or 1} strategic fire-exit staircases. "
                 f"Dedicated corporate vehicle facilities assign {self.private_parking or 0} private executive parking slots alongside "
                 f"an auxiliary pool of {self.public_parking or 0} public common guest parking allocations."
        })

        # FAQ 6: Legal Framework, Risk Assurances & Governance Clearances
        loan_str = (f" The asset record notes an active capital mortgage balance outstanding at ₹{loan_val:,}."
                    if self.property_loan == 'yes'
                    else " The real estate asset title is clear of any active corporate banking liens or mortgage holds.")
        tenant_str = (f" Core operations note a pre-existing lease structure holding existing occupants: "
                      f"{self.tenant_details or 'Occupied under business terms'}."
                      if self.existing_tenants == 'yes'
                      else " The property features clear vacant possession for rapid enterprise deployment.")
        dispute_str = (f" Critical Note: Listing file logs ongoing legal actions or dispute data: '{self.dispute_details}'."
                       if self.any_legal_dispute == 'yes'
                       else " Continuous background checks verify clean legal titles with zero active litigation risks.")
        tax_str = (f" Sovereign records indicate a trailing tax balance due at ₹{tax_val:,}."
                   if self.government_tax == 'yes'
                   else " All local municipal property taxes are verified as fully settled.")

        faq_pool.append({
            "q": "What liability statements, tenant parameters, and legal clearances protect this commercial deed?",
            "a": f"The registry asset operates under a clean '{self.ownership_status or 'Self Owned'}' deed format, verified against a registered "
                 f"title ownership count of {self.no_of_owners or 1} signature holder(s). Operational compliance confirms that local fire "
                 f"marshal Fire NOC protection is: '{self.fire_safety_noc or 'Pending/Not Declared'}'."
                 f"{loan_str}{tenant_str}{dispute_str}{tax_str}"
        })

        # FAQ 7: Local Approvals, Corporate Context & Master Planning Authorities
        faq_pool.append({
            "q": "Which municipal board authorizes this property and what general development summary protects its use?",
            "a": f"The regulatory framework and layout patterns are fully verified by the authorized "
                 f"'{self.sanctioning_authority or 'Local Planning Board'}' board."
        })

        # FAQ 8: Geographic Address Mapping & Title Management Index
        faq_pool.append({
            "q": "What is the precise location address data and title verification identity for this commercial inventory?",
            "a": f"The site location resolves to the commercial sectors of {self.locality or 'N/A'}, {self.city or 'N/A'}, tracking inside the "
                 f"business infrastructure complex mapped as '{self.building_name or 'Premium Corporate Standalone Structure'}'. "
                 f"Detailed physical address lines settle to: {self.address or 'N/A'}. The main stakeholder title is mapped to "
                 f"listed entity {self.listed_by_name or 'N/A'} ({self.listed_by_role or 'Owner/Agent'}), with corporate lines running via "
                 f"{self.listed_by_contact or 'N/A'} / {self.listed_by_email or 'N/A'}. Technical database file tracking lists asset code {self.id} with "
                 f"deployment operations managed by client desk {self.uploaded_by_name or 'System Desk'} "
                 f"({self.uploaded_by_role or 'Administrator'})."
        })

        for item in faq_pool:
            CommercialResaleFAQ.objects.create(property=self, question=item["q"], answer=item["a"])


class CommercialResaleFAQ(models.Model):
    property = models.ForeignKey(CommercialResaleProperty, on_delete=models.CASCADE, related_name='faqs')
    question = models.CharField(max_length=255)
    answer = models.TextField()

    def __str__(self):
        return f"FAQ for Commercial Property: {self.property.id}"


class CommercialPropertyImage(models.Model):

    CATEGORY_CHOICES = [
            ('exterior', 'Exterior / Building'),
            ('living',   'Living / Dining'),
            ('bedroom',  'Bedroom'),
            ('kitchen',  'Kitchen'),
            ('bathroom', 'Bathroom'),
            ('balcony',  'Balcony'),
            ('others',   'Others'),
        ]
    property = models.ForeignKey(CommercialResaleProperty, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to="resale_commercial/")
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='others')
    sequence_order = models.PositiveIntegerField(default=0)
    
    class Meta:
        ordering = ["category", "sequence_order"]


class ResaleCommercialVideo(models.Model):
    SOURCE_CHOICES = [('uploaded', 'Manually Uploaded'), ('auto', 'Auto Generated Slideshow'),('rm_assisted', 'RM Assisted Link'),]
    property = models.ForeignKey(CommercialResaleProperty, on_delete=models.CASCADE, related_name="video")
    video = models.FileField(upload_to="commercial_resale/videos/")
    video_url = models.URLField(null=True, blank=True)
    source = models.CharField(max_length=100, choices=SOURCE_CHOICES, default='auto')
    video_status = models.CharField(max_length=255, blank=True, null=True,default="Pending")
    created_at = models.DateTimeField(auto_now_add=True)

    def youtube_thumbnail(self):
        import re
        if self.source == 'rm_assisted' and self.video_url:
            match = re.search(
                r'(?:youtube\.com/watch\?v=|youtu\.be/|youtube\.com/shorts/)([A-Za-z0-9_-]{6,})',
                self.video_url
            )
            if match:
                return f"https://img.youtube.com/vi/{match.group(1)}/hqdefault.jpg"
        return None


########### Models End for Resale Commericial  Property  model ############################ ###


############### Modal Start for Residential Resale Plot ########################

def generate_residential_resale_plot_id():
    return f"EFPLT-{uuid.uuid4().hex[:8].upper()}"

class ResidentialResalePlot(models.Model):
    plot_property_id = models.CharField(
        max_length=20,
        primary_key=True,
        default=generate_residential_resale_plot_id,
        editable=False
    )

    ############## Listed By Section Details ############################

    listed_by_type = models.CharField(max_length=255, blank=True, null=True)
    assigned_to = models.CharField(max_length=255, blank=True, null=True)
    listed_by_id = models.CharField(max_length=255, blank=True, null=True)
    listed_by_name = models.CharField(max_length=255, blank=True, null=True)
    listed_by_email = models.CharField(max_length=255, blank=True, null=True)
    listed_by_contact = models.CharField(max_length=255, blank=True, null=True)
    listed_by_role = models.CharField(max_length=255, blank=True, null=True)

    ################## Basic Details Section #################################

    property_title = models.CharField(max_length=255, blank=True, null=True)
    plot_title = models.CharField(max_length=255,null=True,blank=True)
    property_no = models.CharField(max_length=255,null=True,blank=True)
    plot_area = models.DecimalField(max_digits=12, decimal_places=2)
    property_type = models.CharField(max_length=255,null=True,blank=True)
    
    ############ Zone Classification and Approval Details #######################

    land_use = models.CharField(max_length=150, blank=True, null=True)
    na_status = models.CharField(max_length=10, blank=True,null=True)
    layout_approval_status = models.CharField(max_length=10, blank=True,null=True)
    residential_zone_type = models.CharField(max_length=10, blank=True,null=True)
    gated_community = models.CharField(max_length=10, blank=True,null=True)
    layout_name = models.CharField(max_length=10, blank=True,null=True)

    ############ Plot specification and physical details #######################

    plot_frontage = models.PositiveIntegerField(blank=True,null=True)
    plot_depth = models.PositiveIntegerField(blank=True,null=True)
    plot_shape = models.CharField(max_length=500, blank=True,null=True)
    road_connectivity = models.CharField(max_length=500, blank=True,null=True)
    road_width = models.CharField(max_length=500, blank=True,null=True)
    corner_plot = models.CharField(max_length=500, blank=True,null=True)
    plot_facing = models.CharField(max_length=500, blank=True,null=True)
    plot_fencing = models.CharField(max_length=500, blank=True,null=True)
    current_possession_status = models.CharField(max_length=500, blank=True,null=True)

    ################# Pricing and Legal Detail Section ################################

    price_per_sqft       = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    brokerage            = models.CharField(max_length=10, default='No')
    brokerage_percentage = models.CharField(max_length=50, blank=True, null=True)
    ownership_type       = models.CharField(max_length=100)
    loan_on_property     = models.CharField(max_length=10, default='no')  # Kept as loan_on_property
    plot_loan_amount     = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)


    nearby_facilities = models.TextField(blank=True, null=True)  # Comma-separated list
    amenities = models.TextField(blank=True, null=True) 

    # ── STEP 3: Media & Certificates ─────────────────────────────
    encumbrance_cert  = models.FileField(upload_to='plot_docs/certificates/', null=True, blank=True)
    social_video      = models.FileField(upload_to='plot_docs/videos/', blank=True, null=True)

    # ── STEP 4: Location & Contact ────────────────────────────────
    plot_city          = models.CharField(max_length=100)
    plot_locality      = models.CharField(max_length=150)
    plot_address       = models.TextField()

    property_summary = models.TextField(blank=True, null=True)
    property_description = models.TextField(blank=True, null=True)
    user_description = models.TextField(blank=True, null=True)

    plot_owner_name    = models.CharField(max_length=150)
    plot_owner_contact = models.CharField(max_length=20)
    plot_owner_email   = models.EmailField()
    plot_owner_role    = models.CharField(max_length=20, null=True, blank=True)

    # ── Uploader / Audit ─────────────────────────────────────────
    uploaded_by_name    = models.CharField(max_length=100, blank=True, null=True)
    uploaded_by_role    = models.CharField(max_length=50, blank=True, null=True)
    uploaded_by_email   = models.EmailField(blank=True, null=True)
    uploaded_by_contact = models.CharField(max_length=30, blank=True, null=True)
    upload_file_name    = models.CharField(max_length=255, blank=True, null=True)

    listed_by_id = models.CharField(max_length=150, blank=True, null=True)

    listed_by_name = models.CharField(max_length=150, blank=True, null=True)

    listed_by_email = models.CharField(max_length=20, blank=True, null=True)

    listed_by_contact = models.CharField(max_length=100, blank=True, null=True)

    listed_by_role = models.CharField(max_length=255, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(null=True, blank=True)
    deleted_by = models.CharField(max_length=150, blank=True, null=True)

    class Meta:
        verbose_name        = "Plot Sale Property"
        verbose_name_plural = "Plot Sale Properties"
        ordering            = ['-created_at']

    def __str__(self):
        return f"{self.plot_title or 'Plot'} ({self.plot_property_id})"

############# Modal Ends for Residential Resale Plot ################################




#########################Start Model of RESALE PLOT LISTING####################





def generate_resale_unique_property_id():
    return f"EFPLT-{uuid.uuid4().hex[:8].upper()}"

class PlotSaleProperty(models.Model):
    plot_property_id = models.CharField(
        max_length=20,
        primary_key=True,
        default=generate_resale_unique_property_id,
        editable=False
    )
    property_title = models.CharField(max_length=255, blank=True, null=True)

    # ── STEP 1: Plot Specs ────────────────────────────────────────
    plot_title            = models.CharField(max_length=255)
    plot_area             = models.DecimalField(max_digits=12, decimal_places=2)
    resale_plot_type      = models.CharField(max_length=100)
    property_no = models.CharField(max_length=100, blank=True, null=True)
    plot_road_facing      = models.CharField(max_length=100)
    corner_plot           = models.CharField(max_length=10, default='no')  # Kept as corner_plot
   
    sanctioning_authority = models.CharField(max_length=150, blank=True, null=True)
    plot_fencing          = models.CharField(max_length=10, default='no')

    # ── STEP 2: Pricing & Legal ───────────────────────────────────
    plot_price           = models.DecimalField(max_digits=15, decimal_places=2)
    price_per_sqft       = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    brokerage            = models.CharField(max_length=10, default='No')
    brokerage_percentage = models.CharField(max_length=50, blank=True, null=True)
    ownership_type       = models.CharField(max_length=100)
    loan_on_property     = models.CharField(max_length=10, default='no')  # Kept as loan_on_property
    plot_loan_amount     = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)


    nearby_facilities = models.TextField(blank=True, null=True)  # Comma-separated list
    amenities = models.TextField(blank=True, null=True) 

    # ── STEP 3: Media & Certificates ─────────────────────────────
    encumbrance_cert  = models.FileField(upload_to='plot_docs/certificates/', null=True, blank=True)
    social_video      = models.FileField(upload_to='plot_docs/videos/', blank=True, null=True)

    # ── STEP 4: Location & Contact ────────────────────────────────
    plot_city          = models.CharField(max_length=100)
    plot_locality      = models.CharField(max_length=150)
    plot_address       = models.TextField()

    property_summary = models.TextField(blank=True, null=True)
    property_description = models.TextField(blank=True, null=True)
    user_description = models.TextField(blank=True, null=True)

    plot_owner_name    = models.CharField(max_length=150)
    plot_owner_contact = models.CharField(max_length=20)
    plot_owner_email   = models.EmailField()
    plot_owner_role    = models.CharField(max_length=20, null=True, blank=True)

    # ── Uploader / Audit ─────────────────────────────────────────
    uploaded_by_name    = models.CharField(max_length=100, blank=True, null=True)
    uploaded_by_role    = models.CharField(max_length=50, blank=True, null=True)
    uploaded_by_email   = models.EmailField(blank=True, null=True)
    uploaded_by_contact = models.CharField(max_length=30, blank=True, null=True)
    upload_file_name    = models.CharField(max_length=255, blank=True, null=True)

    listed_by_id = models.CharField(max_length=150, blank=True, null=True)

    listed_by_name = models.CharField(max_length=150, blank=True, null=True)

    listed_by_email = models.CharField(max_length=20, blank=True, null=True)

    listed_by_contact = models.CharField(max_length=100, blank=True, null=True)

    listed_by_role = models.CharField(max_length=255, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(null=True, blank=True)
    deleted_by = models.CharField(max_length=150, blank=True, null=True)

    class Meta:
        verbose_name        = "Plot Sale Property"
        verbose_name_plural = "Plot Sale Properties"
        ordering            = ['-created_at']

    def __str__(self):
        return f"{self.plot_title or 'Plot'} ({self.plot_property_id})"

    # ── AUTO-FAQ GENERATOR (MODIFIED TO MATCH MODEL PROPERTIES) ──
    def generate_auto_faqs(self):
        self.faqs.all().delete()
        faq_pool = []

        def safe_money(val):
            try:
                v = int(float(str(val or 0).replace(",", "").strip()))
                return f"Rs.{v:,}" if v else None
            except Exception:
                return None

        price_str     = safe_money(self.plot_price)
        loan_str      = safe_money(self.plot_loan_amount)
        per_sqft_str  = safe_money(self.price_per_sqft)

        # FAQ 1 — Core Specs
        faq_pool.append({
            "question": "What is the total plot area, type, and where exactly is it located?",
            "answer": (
                f"This is a {self.resale_plot_type or 'residential'} plot spanning {self.plot_area or 'unspecified'} Sqft, "
                f"located in {self.plot_locality or 'the listed locality'}, {self.plot_city or 'city'}."
            )
        })

        # FAQ 2 — Pricing
        brokerage_text = (
            f"A brokerage of {self.brokerage_percentage} applies."
            if str(self.brokerage or '').lower() in ['yes', 'true', '1']
            else "There is no brokerage applicable for this transaction."
        )
        faq_pool.append({
            "question": "What is the expected price and cost per square foot for this plot?",
            "answer": (
                f"The expected sale price is {price_str or 'available on request'}. "
                + (f"This translates to approximately {per_sqft_str} per Sqft. " if per_sqft_str else "")
                + brokerage_text
            )
        })

        # FAQ 3 — Road Facing & Corner (Fixed reference to corner_plot)
        corner_text = (
            "It is a corner plot, offering better road access and higher resale value."
            if str(self.corner_plot or '').lower() == 'yes'
            else "This is not a corner plot."
        )
        faq_pool.append({
            "question": "What is the road facing direction and is this a corner plot?",
            "answer": (
                f"The plot faces {self.plot_road_facing or 'the main road'}, ensuring good natural light "
                f"and ventilation for any future construction. {corner_text}"
            )
        })

        # FAQ 4 — Fencing & Development Ready
        faq_pool.append({
            "question": "Is fencing already done on this plot? Is it ready for immediate construction?",
            "answer": (
                "Yes, boundary fencing has already been completed on this plot, making it secure "
                "and ready for immediate construction without additional perimeter work."
                if str(self.plot_fencing or '').lower() == 'yes' else
                "Boundary fencing has not yet been done on this plot. The buyer may need to account "
                "for fencing costs as part of the initial development plan."
            )
        })

        # FAQ 5 — Authority & Ownership (Fixed reference to ownership_type & sanctioning_authority)
        faq_pool.append({
            "question": "Who is the sanctioning authority and what is the ownership type of this plot?",
            "answer": (
                f"The plot is held under {self.ownership_type or 'standard'} ownership. "
                + (f"It has been sanctioned and approved by {self.sanctioning_authority}." if self.sanctioning_authority else
                   "The sanctioning authority details are available on request from the owner.")
            )
        })

        # FAQ 6 — Encumbrance Certificate
        faq_pool.append({
            "question": "Is an encumbrance certificate available for this plot?",
            "answer": (
                "Yes, the encumbrance certificate for this plot is available and can be downloaded "
                "from the Documents section. This confirms the property is free from any undisclosed "
                "mortgages or legal claims up to the certified date."
                if self.encumbrance_cert else
                "An encumbrance certificate has not been uploaded for this plot at present. Buyers are "
                "advised to request it from the owner before proceeding with the transaction."
            )
        })

        # FAQ 7 — Loan / Mortgage (Fixed reference to loan_on_property)
        faq_pool.append({
            "question": "Is there any active loan or mortgage registered against this plot?",
            "answer": (
                f"Yes, there is an active loan of {loan_str} registered against this plot. "
                f"Buyers should verify clearance of this liability during title transfer."
                if str(self.loan_on_property or '').lower() == 'yes' else
                "No, there are no active financial loans or mortgages registered against this plot. "
                "The title is free of any banking encumbrances, enabling clean registration."
            )
        })

        # FAQ 8 — Why Buy This Plot (Fixed reference to corner_plot)
        faq_pool.append({
            "question": "What makes this plot a good investment opportunity?",
            "answer": (
                f"This {self.resale_plot_type or 'residential'} plot in {self.plot_locality or 'a prime locality'}, "
                f"{self.plot_city or 'city'} offers {self.plot_area or 'ample'} Sqft of land "
                f"with {self.plot_road_facing or 'good'} road facing. "
                + ("Being a corner plot adds visibility and access advantage. " if str(self.corner_plot or '').lower() == 'yes' else "")
                + ("Fencing is already done, reducing upfront development cost. " if str(self.plot_fencing or '').lower() == 'yes' else "")
                + f"Priced at {price_str or 'a competitive rate'}, it represents strong value in the current market."
            )
        })

        PlotSaleFAQ.objects.bulk_create([
            PlotSaleFAQ(property=self, question=f["question"], answer=f["answer"])
            for f in faq_pool
        ])

    # ═══════════════════════════════════════
    # AUTO DESCRIPTION GENERATOR
    # ═══════════════════════════════════════
    def generate_auto_descriptions(self):
        # Fetch safe fallbacks
        p_type = str(self.resale_plot_type).replace('_', ' ').title() if self.resale_plot_type else "Plot"
        loc = str(self.plot_locality).strip() if self.plot_locality else "a prime location"
        city_str = f", {self.plot_city}" if self.plot_city else ""
        
        try: price_val = int(float(str(self.plot_price or 0).strip()))
        except: price_val = 0
        
        try: 
            area = str(self.plot_area).rstrip('0').rstrip('.') if '.' in str(self.plot_area) else str(self.plot_area)
        except: 
            area = "unspecified"

        # -----------------------------------
        # 1. SUMMARY TEXT (Always Regenerates)
        # -----------------------------------
        summary = f"A premium {p_type} is available for sale in {loc}{city_str}. "
        
        if area != "unspecified":
            summary += f"Spanning across an expansive area of {area} sq.ft., "
            
        if price_val > 0:
            summary += f"it is competitively priced at ₹{price_val:,}. "
            
        corner_text = "corner " if str(self.corner_plot).lower() == 'yes' else ""
        summary += f"This {corner_text}plot presents an excellent investment opportunity for immediate construction or long-term capital appreciation."
        
        # Overwrite the field
        self.property_summary = summary.strip()

        # -----------------------------------
        # 2. LONG DESCRIPTION (Always Regenerates)
        # -----------------------------------
        long_desc = f"<p>Secure a prime piece of real estate with this strategically located <strong>{p_type}</strong> in the highly promising neighborhood of <strong>{loc}{city_str}</strong>.</p>"

        if self.plot_title:
            long_desc += f"<p>Part of the recognized <strong>{self.plot_title}</strong> project, this land parcel ensures a perfect blend of connectivity, accessibility, and high future valuation.</p>"

        # --- Section A: Property Specifications ---
        long_desc += "<h3>Plot Specifications:</h3><ul>"
        
        if area != "unspecified":
            long_desc += f"<li><strong>Total Area:</strong> Generous land footprint of {area} sq.ft.</li>"
            
        if price_val > 0:
            long_desc += f"<li><strong>Pricing:</strong> Offered at ₹{price_val:,}.</li>"
            
        if self.plot_road_facing:
            long_desc += f"<li><strong>Facing & Orientation:</strong> {self.plot_road_facing.capitalize()}-facing plot, ensuring great natural elements for future architectural planning.</li>"
            
        if str(self.corner_plot).lower() == 'yes':
            long_desc += f"<li><strong>Corner Plot Advantage:</strong> Yes, offering dual road access, better ventilation, and premium aesthetic potential.</li>"
            
        if str(self.plot_fencing).lower() == 'yes':
            long_desc += "<li><strong>Fencing & Boundary:</strong> Boundary fencing is already completed, securing the perimeter and saving upfront development costs.</li>"
            
        long_desc += "</ul>"

        # --- Section B: Legal & Ownership Framework ---
        long_desc += "<h3>Legal & Ownership Clearances:</h3><ul>"
        
        if self.ownership_type:
            long_desc += f"<li><strong>Ownership:</strong> {self.ownership_type.capitalize()} title, ensuring a smooth and clean transfer process.</li>"
            
        if self.sanctioning_authority:
            long_desc += f"<li><strong>Sanctioning Authority:</strong> Officially approved by {self.sanctioning_authority}.</li>"
            
        if str(self.loan_on_property).lower() == 'yes' and self.plot_loan_amount:
            try: loan_val = int(float(str(self.plot_loan_amount or 0).strip()))
            except: loan_val = 0
            long_desc += f"<li><strong>Financial Status:</strong> Notes an active loan/mortgage of ₹{loan_val:,} against the property.</li>"
        else:
            long_desc += "<li><strong>Financial Status:</strong> Free from active banking or mortgage encumbrances.</li>"
            
        if self.encumbrance_cert:
            long_desc += "<li><strong>Title Verification:</strong> Encumbrance Certificate (EC) is available, verifying the property is free of undisclosed legal claims.</li>"
            
        long_desc += "</ul>"

        long_desc += "<p>Don't miss this rare opportunity to acquire premium land. Contact us today to schedule a site visit and review documentation!</p>"

        # Overwrite the field
        self.property_description = long_desc

    # ═══════════════════════════════════════
    # SAVE METHOD
    # ═══════════════════════════════════════
    def save(self, *args, **kwargs):
        # 1. Auto-calculate price per sqft (Kept exact backend handling)
        if self.plot_price and self.plot_area:
            try:
                area  = float(self.plot_area)
                price = float(self.plot_price)
                if area > 0:
                    self.price_per_sqft = round(price / area, 2)
            except (ValueError, TypeError):
                pass

        # 2. Automated Title Generation
        if not self.property_title:
            type_lbl = self.resale_plot_type.replace('_', ' ').title() if self.resale_plot_type else "Plot"
            try:
                area_val = float(self.plot_area)
                area_lbl = f"{int(area_val):,} Sqft" if area_val == int(area_val) else f"{area_val:,} Sqft"
            except (ValueError, TypeError):
                area_lbl = ""
            project_ctx  = f" ({self.plot_title})" if self.plot_title else ""
            locality_ctx = f" at {self.plot_locality}, {self.plot_city}" if self.plot_locality and self.plot_city else ""
            self.property_title = " ".join(f"Premium {area_lbl} {type_lbl}{project_ctx}{locality_ctx}".split())

        # ---> Trigger Auto Description Generation BEFORE saving <---
        self.generate_auto_descriptions()

        # 3. Save Record
        super().save(*args, **kwargs)
        
        # 4. Trigger Auto FAQs
        self.generate_auto_faqs()

 

 
 
# ══════════════════════════════════════════════════════════════════
#  MODEL 2 — PlotSaleImage
# ══════════════════════════════════════════════════════════════════
 
class PlotSaleImage(models.Model):
    property    = models.ForeignKey(PlotSaleProperty, on_delete=models.CASCADE, related_name='images')
    image       = models.ImageField(upload_to='plot_docs/images/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
 
    class Meta:
        ordering = ['uploaded_at']
 
    def __str__(self):
        return f"Image for {self.property.plot_property_id}"
 
 
# ══════════════════════════════════════════════════════════════════
#  MODEL 3 — PlotSaleFAQ  (NEW)
#  Auto-populated by generate_auto_faqs() on every save
# ══════════════════════════════════════════════════════════════════
 
class PlotSaleFAQ(models.Model):
    property = models.ForeignKey(PlotSaleProperty, on_delete=models.CASCADE, related_name='faqs')
    question = models.CharField(max_length=500)
    answer   = models.TextField()
 
    class Meta:
        ordering = ['id']
 
    def __str__(self):
        return f"FAQ: {self.question[:60]}"

#############END MODEL SECTION RESALE PLOT LISTING##################


#######################START MODEL SECTION RESALE INDUSTRIAL LISTING######################




# Helper function to generate the custom primary key
def generate_industrial_id():
    return f"EFIND-{uuid.uuid4().hex[:8].upper()}"


class IndustrialResaleProperty(models.Model):
    # ── SYSTEM CONTROL & IDENTIFICATION ──────────────────────────────
    id = models.CharField(
        max_length=50,
        primary_key=True,
        default=generate_industrial_id,
        editable=False,
        help_text="Automated unique serial lookup tracking tag"
    )


    ############# Category Fields ###########################
        
    listing_type = models.CharField(max_length=255, blank=True, null=True)
    category = models.CharField(max_length=255, blank=True, null=True)
    
    ############## Listed By Section ###############################
    
    listed_by_type = models.CharField(max_length=255, blank=True, null=True)
    assigned_to = models.CharField(max_length=255, blank=True, null=True)
    listed_by_id = models.CharField(max_length=255, blank=True, null=True)
    listed_by_name = models.CharField(max_length=255, blank=True, null=True)
    listed_by_email = models.CharField(max_length=255, blank=True, null=True)
    listed_by_contact = models.CharField(max_length=255, blank=True, null=True)
    listed_by_role = models.CharField(max_length=255, blank=True, null=True)
    
    property_unique_key = models.CharField(max_length=255, blank=True, null=True, db_index=True)
    duplicate_count = models.PositiveIntegerField(default=0)
    duplicate_group_id = models.CharField(max_length=255, blank=True, null=True, db_index=True)   # <-- drives the brokerage label

    ########### Basic Property Details #################################

    property_title = models.CharField(max_length=255, blank=True, null=True)
    property_type  = models.CharField(max_length=100, null=True, blank=True)
    property_no = models.CharField(max_length=100, blank=True, null=True)
    land_area  = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    builtup_area  = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    industrial_zone_classification = models.CharField(max_length=200, blank=True, null=True)
    main_road_connectivity = models.CharField(max_length=200, blank=True, null=True)

   ################# Utilities and Infrastructure Details #####################
    
    power_supply = models.BooleanField(default=False)
    kva_capacity = models.IntegerField(blank=True, null=True)
    connected_power_load = models.IntegerField(blank=True, null=True)
    water_supply = models.CharField(max_length=50, blank=True, null=True)
    truck_accessibility = models.CharField(max_length=50, blank=True, null=True)
    loading_dock = models.CharField(max_length=50, blank=True, null=True)
    floor_load_capacity = models.CharField(max_length=50, blank=True, null=True)
    crane_heavy_machinery = models.BooleanField(default=False)
    worker_housing_nearby = models.BooleanField(default=False)

    ############## Pricing Details Section #############################

    selling_price= models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    price_per_sqft = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    brokerage = models.CharField(max_length=20,blank=True,null=True)
    brokerage_percentage  = models.CharField(max_length=50, blank=True, null=True)
    manual_brokerage  = models.CharField(max_length=100, blank=True, null=True)


    ################## Ownership and Legal Compilance Details ####################

    ownership_type = models.CharField(max_length=100, null=True, blank=True)
    ownership_document_type = models.CharField(max_length=100, null=True, blank=True)
    title_status = models.CharField(max_length=100, null=True, blank=True)
    sanctioning_authority = models.CharField(max_length=150, blank=True, null=True)
    property_loan = models.BooleanField(default=False)
    loan_amount = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    existing_tenants = models.BooleanField(default=False)
    tenant_details = models.TextField(blank=True, null=True)
    legal_dispute = models.BooleanField(default=False)
    dispute_details = models.TextField(blank=True, null=True)
    government_tax = models.BooleanField(default=False)
    tax_amount = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    tax_clearance_cert = models.BooleanField(default=False)

    ########## Industrial License and Compilance Details Section ##################

    factory_license_status = models.CharField(max_length=100, null=True, blank=True)
    fire_noc_status = models.CharField(max_length=100, null=True, blank=True)
    pollution_control_approval = models.CharField(max_length=100, null=True, blank=True)

    ########## Facilities and Ameneties Details Section #####################

    amenities = models.TextField(blank=True, null=True) 
    nearby_facilities = models.TextField(blank=True, null=True)
    property_summary = models.TextField(blank=True, null=True)
    property_description = models.TextField(blank=True, null=True)
    user_description = models.TextField(blank=True, null=True)

    ############# Location Details Section ############################

    city = models.CharField(max_length=100, blank=True, null=True)
    locality = models.CharField(max_length=150, null=True, blank=True)
    address = models.TextField(blank=True, null=True)
    property_landmark = models.CharField(max_length=150, null=True, blank=True)
    state = models.CharField(max_length=150, null=True, blank=True)
    residency_status = models.CharField(max_length=150, null=True, blank=True)
    google_maps_link = models.CharField(max_length=150, null=True, blank=True)
    latitude = models.CharField(max_length=150, null=True, blank=True)
    longitude = models.CharField(max_length=150, null=True, blank=True)
    pincode = models.CharField(max_length=150, null=True, blank=True)

    ############# Docs,Images and Video Section ################

    compliance_docs = models.FileField(upload_to='industrial_docs/compliance/', blank=True, null=True)
    video_option = models.CharField(max_length=200, blank=True, null=True)
    property_video = models.FileField(upload_to='properties/videos/', null=True, blank=True)
    property_video_link = models.CharField(max_length=200, blank=True, null=True)
    listed_elsewhere = models.CharField(max_length=150, null=True, blank=True)
    portal_name = models.CharField(max_length=150, null=True, blank=True)

    ############### Property Uploaded By Details ############################

    uploaded_by_name    = models.CharField(max_length=100, blank=True, null=True)
    uploaded_by_role    = models.CharField(max_length=50, blank=True, null=True)
    uploaded_by_email   = models.EmailField(blank=True, null=True)
    uploaded_by_contact = models.CharField(max_length=30, blank=True, null=True)
    upload_file_name = models.CharField(max_length=255, blank=True, null=True)
    
    ############# Timestamp and other details section ##########################
    
    is_deleted = models.BooleanField(default=False)
    is_duplicate = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(null=True, blank=True)
    deleted_by = models.CharField(max_length=150, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    listing_status = models.CharField(max_length=150, blank=True, null=True)
    approval_status = models.CharField(max_length=150, blank=True, null=True)

    class Meta:
        verbose_name        = "Industrial Property"
        verbose_name_plural = "Industrial Properties"
        ordering            = ['-created_at']

    def __str__(self):
        return self.property_title or f"Industrial #{self.id}"

    # ═══════════════════════════════════════
    # HELPER: CLEAN TEXT FIELDS
    # ═══════════════════════════════════════
    def _clean_text_field(self, value):
        """Cleans list-like strings and returns a comma-separated string."""
        if not value:
            return ""
        if isinstance(value, list):
            return ", ".join(str(item).strip() for item in value if item)
        if isinstance(value, str):
            cleaned = value.replace("[", "").replace("]", "").replace("'", "").replace('"', "")
            if "," in cleaned:
                return ", ".join(item.strip() for item in cleaned.split(",") if item.strip())
            return cleaned.strip()
        return str(value).strip()
    
    from decimal import Decimal, InvalidOperation
    
    def _fmt_amount(self, value):   
        """Return the numeric value formatted with exactly 2 decimal places,
        no thousands separators — matches how it's stored in the DB."""
        if value is None or value == "":
            return "0.00"
        try:
            return f"{Decimal(str(value)):.2f}"
        except (InvalidOperation, ValueError, TypeError):
            return str(value)

    # ── AUTO-FAQ GENERATOR (UPDATED FOR YOUR INDUSTRIAL RESALE MODEL) ──
    def generate_auto_faqs(self):
        self.faqs.all().delete()
        faq_pool = []

        price_val = self.selling_price or 0
        loan_val = self.loan_amount or 0
        tax_val = self.tax_amount or 0
        per_sqft_val = self.price_per_sqft or 0

        # FAQ 1 — Core Specs
        faq_pool.append({
            "question": "What is the total land area and specific property type of this industrial asset?",
            "answer": (
                f"This is an industrial {self.property_type or 'facility'} with a total land area of "
                f"{self.land_area or 'unspecified'} Sqft, situated in "
                f"{self.locality or 'the listed area'}, {self.city or 'city'}. "
                f"The property falls under {self.industrial_zone_classification or 'standard'} "
                f"industrial zone classification with {self.main_road_connectivity or 'adequate'} "
                f"road connectivity."
            )
        })

        # FAQ 2 — Pricing & Brokerage
        brokerage_text = ""
        if self.brokerage and self.brokerage_percentage:
            brokerage_text = f"A brokerage of {self.brokerage_percentage}% applies."
        elif self.manual_brokerage:
            brokerage_text = f"Brokerage details: {self.manual_brokerage}."
        else:
            brokerage_text = "There is no brokerage applicable for this transaction."

        faq_pool.append({
            "question": "What is the expected price and brokerage structure for this property?",
            "answer": (
                f"The expected sale price for this industrial property is ₹{self._fmt_amount(price_val)}. "
                + (f"This translates to approximately ₹{self._fmt_amount(per_sqft_val)} per Sqft. " if per_sqft_val else "")
                + brokerage_text
            )
        })

        # FAQ 3 — Power Supply
        if self.power_supply:
            faq_pool.append({
                "question": "What is the heavy industrial power supply capacity available at this facility?",
                "answer": (
                    f"The property is equipped with an active heavy industrial power supply infrastructure "
                    f"supporting up to {self.kva_capacity or 'standard'} KVA, making it ideal for "
                    f"high-load manufacturing, processing, and continuous industrial operations."
                )
            })
        else:
            faq_pool.append({
                "question": "Does this property have an industrial-grade power supply?",
                "answer": (
                    "Currently, no dedicated heavy industrial power supply is configured at this facility. "
                    "Standard commercial electricity lines may apply, and a heavy industrial connection "
                    "would need to be separately sanctioned from the local electricity board."
                )
            })

        # FAQ 4 — Water Supply
        faq_pool.append({
            "question": "What is the status and type of water supply available for industrial operations?",
            "answer": (
                f"The property utilises a {self.water_supply or 'standard municipal'} water supply system. "
                f"This is suitable for the current operational scope and can support standard industrial "
                f"washing, cooling, and processing requirements."
            )
        })

        # FAQ 5 — Logistics & Truck Accessibility
        faq_pool.append({
            "question": "How is the truck accessibility and loading infrastructure at this facility?",
            "answer": (
                f"The property offers {self.truck_accessibility or 'standard'} truck accessibility, "
                f"with {self.loading_dock or 'adequate'} loading dock facilities. "
                f"Floor load capacity is rated at {self.floor_load_capacity or 'standard'} "
                f"making it suitable for heavy equipment and storage operations."
            )
        })

        # FAQ 6 — Crane / Heavy Machinery
        faq_pool.append({
            "question": "Can this facility support heavy overhead cranes and large machinery operations?",
            "answer": (
                "Yes, the internal structural infrastructure and roofing framework of this facility are "
                "purpose-built to accommodate heavy machinery operations and overhead crane fitments, "
                "making it suitable for large-scale manufacturing and logistics."
                if self.crane_heavy_machinery else
                "No, this facility is not currently configured or structurally reinforced for heavy overhead "
                "crane installations. Standard equipment and floor-level machinery operations are supported."
            )
        })

        # FAQ 7 — Worker Housing
        faq_pool.append({
            "question": "Is worker housing or labour accommodation available near this industrial property?",
            "answer": (
                "Yes, worker housing and labour accommodation facilities are available in the immediate "
                "vicinity of this property, which is highly beneficial for managing factory shift workers "
                "and reducing daily commute for the workforce."
                if self.worker_housing_nearby else
                "There is no dedicated worker housing immediately adjacent to this property. Employers "
                "may need to arrange transportation or explore nearby residential areas for staff accommodation."
            )
        })

        # FAQ 8 — Legal Dispute & Tax
        dispute_text = (
            f"There is an active legal dispute on record: {self.dispute_details or 'Details available on request'}. "
            if self.legal_dispute else
            "The property title is completely clear of any legal disputes or encumbrances. "
        )
        tax_text = (
            f"There are pending municipal/property tax dues amounting to ₹{self._fmt_amount(tax_val)}. "
            if self.government_tax else
            "All property and municipal taxes are fully cleared and up to date. "
        )
        tax_clearance = (
            "A tax clearance certificate is available."
            if self.tax_clearance_cert else
            "Tax clearance certificate is currently not available."
        )
        faq_pool.append({
            "question": "Are there any pending legal disputes or outstanding tax dues on this property?",
            "answer": dispute_text + tax_text + tax_clearance
        })

        # FAQ 9 — Loan / Mortgage
        faq_pool.append({
            "question": "Is there any active financial loan or mortgage registered against this property?",
            "answer": (
                f"Yes, there is an active loan/mortgage of ₹{self._fmt_amount(loan_val)} currently registered against this "
                f"property. Buyers should account for this encumbrance during title verification and "
                f"financing arrangements."
                if self.property_loan else
                "No, there are no active financial loans or mortgages registered against this property. "
                "The title is free of any banking or financial institution encumbrances."
            )
        })

        # FAQ 10 — Ownership & Tenants
        ownership_text = (
            f"The property is held under {self.ownership_type or 'standard'} ownership with "
            f"{self.ownership_document_type or 'standard'} documentation. "
            f"Title status: {self.title_status or 'Clear'}. "
            + (f"Sanctioned by {self.sanctioning_authority}. " if self.sanctioning_authority else "")
        )
        tenant_text = (
            f"The property currently has active tenants. Details: {self.tenant_details or 'Available on request'}."
            if self.existing_tenants else
            "The property is completely vacant with no existing tenants, enabling immediate possession."
        )
        faq_pool.append({
            "question": "What is the ownership structure, and are there any existing tenants currently occupying this space?",
            "answer": ownership_text + tenant_text
        })

        # FAQ 11 — Factory License & Compliance
        faq_pool.append({
            "question": "What are the industrial licenses and compliance approvals in place?",
            "answer": (
                f"Factory license status: {self.factory_license_status or 'Under review'}. "
                f"Fire NOC status: {self.fire_noc_status or 'Under review'}. "
                f"Pollution control approval: {self.pollution_control_approval or 'Under review'}. "
                "All necessary industrial compliance documentation is available for verification."
            )
        })

        # FAQ 12 — Location & Accessibility
        faq_pool.append({
            "question": "Where exactly is this property located and what are the nearby facilities?",
            "answer": (
                f"This industrial property is located at {self.address or 'the listed address'} "
                f"in {self.locality or 'the locality'}, {self.city or 'city'}, {self.state or 'state'}. "
                f"Key landmark: {self.property_landmark or 'Available on request'}. "
                f"Residency status: {self.residency_status or 'Commercial'}. "
                f"Nearby facilities include: {self.nearby_facilities or 'Various industrial and commercial establishments'}."
            )
        })

        # FAQ 13 — Amenities & Features
        amenities_str = self._clean_text_field(self.amenities)
        if amenities_str.strip():
            faq_pool.append({
                "question": "What amenities and features does this industrial property offer?",
                "answer": (
                    f"This property comes with the following amenities: {amenities_str}. "
                    "These features enhance operational efficiency and worker convenience."
                )
            })

            # Bulk create FAQs
            IndustrialResaleFAQ.objects.bulk_create([
                IndustrialResaleFAQ(property=self, question=f["question"], answer=f["answer"])
                for f in faq_pool
            ])

    # ═══════════════════════════════════════
    # AUTO DESCRIPTION GENERATOR
    # ═══════════════════════════════════════
    def generate_auto_descriptions(self):
        p_type = str(self.property_type).replace('_', ' ').title() if self.property_type else "Industrial Facility"
        loc = str(self.locality).strip() if self.locality else "a prime industrial zone"
        city_str = f", {self.city}" if self.city else ""
        
        price_val = self.selling_price or 0
        
        try: 
            area = str(self.land_area).rstrip('0').rstrip('.') if '.' in str(self.land_area) else str(self.land_area)
        except: 
            area = "unspecified"

        # -----------------------------------
        # 1. SUMMARY TEXT
        # -----------------------------------
        summary = f"A strategic {p_type} is available for sale in {loc}{city_str}. "
        
        if area != "unspecified":
            summary += f"Spanning a massive land area of {area} sq.ft., "
            
        if price_val > 0:
            summary += f"it is competitively priced at ₹{self._fmt_amount(price_val)}. "
            
        if self.power_supply and self.kva_capacity:
            summary += f"Equipped with a heavy industrial power supply of {self.kva_capacity} KVA, "
            
        summary += "this facility is highly suitable for large-scale manufacturing, warehousing, and heavy industrial operations."
        
        self.property_summary = summary.strip()

        # -----------------------------------
        # 2. LONG DESCRIPTION
        # -----------------------------------
        long_desc = f"<p>Scale your manufacturing and logistics operations with this highly functional <strong>{p_type}</strong> located in the thriving industrial belt of <strong>{loc}{city_str}</strong>.</p>"
        long_desc += "<p>Designed to meet strict industrial compliance, this property ensures a seamless environment for heavy-duty commercial processing and workflow stabilization.</p>"

        # --- Section A: Core Specifications ---
        long_desc += "<h3>Core Specifications:</h3><ul>"
        
        if area != "unspecified":
            long_desc += f"<li><strong>Total Land Area:</strong> Expansive operational footprint of {area} sq.ft., providing ample space for plant setup and storage.</li>"
            
        if self.builtup_area:
            long_desc += f"<li><strong>Built-up Area:</strong> {self.builtup_area} sq.ft. of constructed space.</li>"
            
        if price_val > 0:
            long_desc += f"<li><strong>Pricing:</strong> Valued at ₹{self._fmt_amount(price_val)}.</li>"
            
        if self.ownership_type:
            long_desc += f"<li><strong>Ownership Status:</strong> Held under {self.ownership_type.capitalize()} ownership with {self.ownership_document_type or 'standard'} documentation.</li>"
            
        if self.title_status:
            long_desc += f"<li><strong>Title Status:</strong> {self.title_status}.</li>"
            
        if self.sanctioning_authority:
            long_desc += f"<li><strong>Sanctioning Authority:</strong> Officially approved and zoned by {self.sanctioning_authority}.</li>"
            
        long_desc += "</ul>"

        # --- Section B: Industrial Infrastructure & Utilities ---
        long_desc += "<h3>Industrial Infrastructure & Utilities:</h3><ul>"
        
        if self.power_supply:
            kva_str = f" supporting up to {self.kva_capacity} KVA" if self.kva_capacity else ""
            long_desc += f"<li><strong>Power Supply:</strong> Active heavy industrial power connection{kva_str}, ideal for continuous high-load operations.</li>"
        else:
            long_desc += "<li><strong>Power Supply:</strong> Standard commercial electricity. Heavy industrial connections require separate municipal sanctioning.</li>"
            
        if self.water_supply:
            long_desc += f"<li><strong>Water Infrastructure:</strong> Supported by a {self.water_supply} water supply system for industrial processing and cooling.</li>"
            
        if self.crane_heavy_machinery:
            long_desc += "<li><strong>Heavy Machinery Support:</strong> The structural framework is purpose-built and reinforced to accommodate heavy overhead cranes and massive floor-level machinery.</li>"
            
        if self.truck_accessibility:
            long_desc += f"<li><strong>Truck Accessibility:</strong> {self.truck_accessibility} access for heavy transport vehicles.</li>"
            
        if self.loading_dock:
            long_desc += f"<li><strong>Loading Dock:</strong> {self.loading_dock} loading facilities available.</li>"
            
        if self.floor_load_capacity:
            long_desc += f"<li><strong>Floor Load Capacity:</strong> Rated at {self.floor_load_capacity}.</li>"
            
        long_desc += "</ul>"

        # --- Section C: Logistics & Workforce ---
        long_desc += "<h3>Logistics & Workforce Accessibility:</h3><ul>"
        
        if self.main_road_connectivity:
            long_desc += f"<li><strong>Road Connectivity:</strong> Features {self.main_road_connectivity} connectivity, enabling smooth transit for heavy multi-axle trucks and shipping containers.</li>"
            
        if self.worker_housing_nearby:
            long_desc += "<li><strong>Workforce Housing:</strong> Labor accommodation and worker housing facilities are available nearby, ensuring easy shift management and reduced transit times.</li>"
            
        long_desc += "</ul>"

        # --- Section D: Compliance & Status ---
        long_desc += "<h3>Compliance & Property Status:</h3><ul>"
        
        if self.factory_license_status:
            long_desc += f"<li><strong>Factory License:</strong> {self.factory_license_status}.</li>"
            
        if self.fire_noc_status:
            long_desc += f"<li><strong>Fire NOC:</strong> {self.fire_noc_status}.</li>"
            
        if self.pollution_control_approval:
            long_desc += f"<li><strong>Pollution Control:</strong> {self.pollution_control_approval}.</li>"
            
        if self.existing_tenants:
            long_desc += f"<li><strong>Occupancy:</strong> Currently houses active operations/tenants ({self.tenant_details or 'Details on request'}).</li>"
        else:
            long_desc += "<li><strong>Occupancy:</strong> Offered with immediate vacant possession.</li>"
            
        if self.legal_dispute:
            long_desc += f"<li><strong>Legal Status:</strong> Active legal dispute noted ({self.dispute_details or 'Pending resolution'}).</li>"
        else:
            long_desc += "<li><strong>Legal Status:</strong> Verified clear title with no active legal disputes.</li>"
            
        if self.property_loan:
            loan_v = f" (₹{self._fmt_amount(self.loan_amount)})" if self.loan_amount else ""
            long_desc += f"<li><strong>Financial Encumbrances:</strong> Active loan/mortgage registered against the asset{loan_v}.</li>"
            
        if self.government_tax:
            tax_v = f" (₹{self._fmt_amount(self.tax_amount)})" if self.tax_amount else ""
            long_desc += f"<li><strong>Tax Compliance:</strong> Pending municipal/property tax dues{tax_v}.</li>"
            if self.tax_clearance_cert:
                long_desc += "<li><strong>Tax Clearance:</strong> Tax clearance certificate is available.</li>"
        else:
            long_desc += "<li><strong>Tax Compliance:</strong> All property taxes are fully cleared up to date.</li>"
            
        long_desc += "</ul>"

        long_desc += "<p>This is a high-value industrial asset tailored for scalable business operations. Contact us today to schedule a site inspection and review compliance documentation!</p>"

        self.property_description = long_desc

    # ═══════════════════════════════════════
    # SAVE METHOD
    # ═══════════════════════════════════════
    def save(self, *args, **kwargs):
        cleaned_amenities = self._clean_text_field(self.amenities)
        if cleaned_amenities:
            self.amenities = cleaned_amenities

        cleaned_facilities = self._clean_text_field(self.nearby_facilities)
        if cleaned_facilities:
            self.nearby_facilities = cleaned_facilities

        if self.selling_price and self.land_area:
            try:
                area = Decimal(str(self.land_area))
                price = Decimal(str(self.selling_price))
                if area > 0:
                    self.price_per_sqft = (price / area).quantize(Decimal('0.01'))
            except (ValueError, TypeError, Decimal.InvalidOperation):
                pass

        if not self.property_title:
            type_lbl = (
                self.property_type.replace('_', ' ').title()
                if self.property_type else "Industrial Asset"
            )
            try:
                area_val = self.land_area
                area_lbl = f"{area_val:,} Sqft" if area_val else ""
            except (ValueError, TypeError):
                area_lbl = ""
                
            locality_ctx = f" in {self.locality}" if self.locality else ""
            city_ctx = f", {self.city}" if self.city else ""
            self.property_title = " ".join(
                f"Industrial {area_lbl} {type_lbl}{locality_ctx}{city_ctx}".split()
            )

        self.generate_auto_descriptions()
        super().save(*args, **kwargs)
        self.generate_auto_faqs()

# ══════════════════════════════════════════════════════════════════════
#  MODEL 3 — IndustrialResaleFAQ  (NEW)
#  Auto-populated by generate_auto_faqs() — do NOT edit rows manually
# ══════════════════════════════════════════════════════════════════════

class IndustrialResaleFAQ(models.Model):
    property = models.ForeignKey(
        IndustrialResaleProperty,
        on_delete=models.CASCADE,
        related_name='faqs'
    )
    question = models.CharField(max_length=500)
    answer   = models.TextField()

    class Meta:
        ordering = ['id']

    def __str__(self):
        return f"FAQ: {self.question[:60]}"

class IndustrialPropertyImage(models.Model):

    CATEGORY_CHOICES = [
        ('front_elevation', 'Property Front Elevation'),
        ('main_entrance', 'Main Entrance'),
        ('warehouse_interior', 'Warehouse / Factory Interior'),
        ('loading_dock', 'Loading Dock'),
        ('truck_yard', 'Truck Yard'),
        ('office_area', 'Office Area'),
        ('machinery', 'Machinery'),
        ('storage_area', 'Storage Area'),
        ('fire_safety', 'Fire Safety'),
        ('parking', 'Parking'),
        ('road_connectivity', 'Road Connectivity'),
        ('aerial_drone', 'Aerial / Drone View'),
    ]
    property = models.ForeignKey(IndustrialResaleProperty, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to="resale_industrial/")
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='others')
    sequence_order = models.PositiveIntegerField(default=0)
    
    class Meta:
        ordering = ["category", "sequence_order"]


class ResaleIndustrialVideo(models.Model):
    SOURCE_CHOICES = [('uploaded', 'Manually Uploaded'), ('auto', 'Auto Generated Slideshow'),('rm_assisted', 'RM Assisted Link'),]
    property = models.ForeignKey(IndustrialResaleProperty, on_delete=models.CASCADE, related_name="video")
    video = models.FileField(upload_to="industry_resale/videos/")
    video_url = models.URLField(null=True, blank=True)
    source = models.CharField(max_length=100, choices=SOURCE_CHOICES, default='auto')
    video_status = models.CharField(max_length=255, blank=True, null=True,default="Pending")
    created_at = models.DateTimeField(auto_now_add=True)

    def youtube_thumbnail(self):
        import re
        if self.source == 'rm_assisted' and self.video_url:
            match = re.search(
                r'(?:youtube\.com/watch\?v=|youtu\.be/|youtube\.com/shorts/)([A-Za-z0-9_-]{6,})',
                self.video_url
            )
            if match:
                return f"https://img.youtube.com/vi/{match.group(1)}/hqdefault.jpg"
        return None



##################END MODEL SECTION INDUSTRIAL RESALE LISTING################


##################START MODEL SECTION AGRICULTURAL RESALE LISTING################


# Helper function to generate the custom primary key
def generate_agri_id():
    return f"EFAGR-{uuid.uuid4().hex[:8].upper()}"


class AgriculturalResaleProperty(models.Model):
    # ── SYSTEM CONTROL & IDENTIFICATION ──────────────────────────
    id = models.CharField(
        max_length=50,
        primary_key=True,
        default=generate_agri_id,
        editable=False,
        help_text="Automated unique registration tag"
    )

    ############# Category Fields ###########################
            
    listing_type = models.CharField(max_length=255, blank=True, null=True)
    category = models.CharField(max_length=255, blank=True, null=True)
        
    ############## Listed By Section ###############################
        
    listed_by_type = models.CharField(max_length=255, blank=True, null=True)
    assigned_to = models.CharField(max_length=255, blank=True, null=True)
    listed_by_id = models.CharField(max_length=255, blank=True, null=True)
    listed_by_name = models.CharField(max_length=255, blank=True, null=True)
    listed_by_email = models.CharField(max_length=255, blank=True, null=True)
    listed_by_contact = models.CharField(max_length=255, blank=True, null=True)
    listed_by_role = models.CharField(max_length=255, blank=True, null=True)
        
    property_unique_key = models.CharField(max_length=255, blank=True, null=True, db_index=True)
    duplicate_count = models.PositiveIntegerField(default=0)
    duplicate_group_id = models.CharField(max_length=255, blank=True, null=True, db_index=True)   # <-- drives the brokerage label

    ########### Basic Land Information #############################

    property_title = models.CharField(max_length=255, blank=True, null=True) 
    property_type = models.CharField(max_length=50,blank=True,null=True)
    property_no = models.CharField(max_length=100, blank=True, null=True)
    land_area = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    village = models.CharField(max_length=100,blank=True,null=True)
    taluka = models.CharField(max_length=100,blank=True,null=True)
    district = models.CharField(max_length=100,blank=True,null=True)
    state = models.CharField(max_length=100,blank=True,null=True)
    locality = models.CharField(max_length=100,blank=True,null=True)
    pincode = models.CharField(max_length=100,blank=True,null=True)
    address = models.TextField(blank=True,null=True)
    google_maps_link = models.CharField(max_length=100,blank=True,null=True)
    latitude = models.CharField(max_length=100,blank=True,null=True)
    longitude = models.CharField(max_length=100,blank=True,null=True)

    ############## Soil and Cultivation Details ######################

    soil_type = models.CharField(max_length=50, blank=True, null=True)
    cultivation_status = models.CharField(max_length=200, blank=True, null=True)
    fertility_status = models.CharField(max_length=200, blank=True, null=True)
    previous_crops = models.CharField(max_length=255, blank=True, null=True)
    property_age = models.CharField(max_length=10, blank=True,null=True) 

    ########## Water and Irrigation Details #################################

    water_source = models.CharField(max_length=50, blank=True, null=True)
    irrigation_facility = models.CharField(max_length=50, blank=True, null=True)
    irrigation_facility_active = models.CharField(max_length=50, blank=True, null=True)
    nos_borewells = models.CharField(max_length=50, blank=True, null=True)
    water_source_infrastructure = models.CharField(max_length=50, blank=True, null=True)
    
    ############# Accessibility and Road Details Section ##########################33
    
    road_access = models.CharField(max_length=50, blank=True, null=True)
    road_frontage = models.CharField(max_length=50, blank=True, null=True)
    dist_nearest_village = models.CharField(max_length=50, blank=True, null=True)
    dist_main_road = models.CharField(max_length=50, blank=True, null=True)
    dist_highway = models.CharField(max_length=50, blank=True, null=True)
    fencing_status = models.CharField(max_length=50, blank=True, null=True)

    ########### Pricing Details Section ###############################

    selling_price = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    price_per_acre = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    brokerage_percentage = models.CharField(max_length=50, blank=True, null=True)
    manual_brokerage = models.CharField(max_length=50, blank=True, null=True)

    ################ Ownership and Legal Status Section ######################

    ownership_type = models.CharField(max_length=100,blank=True,null=True)
    land_conversion_status = models.CharField(max_length=100,blank=True,null=True)
    ownership_document_type = models.CharField(max_length=100,blank=True,null=True)
    title_status = models.CharField(max_length=100,blank=True,null=True)
    encumbrance_status = models.CharField(max_length=100,blank=True,null=True)
    possession_status = models.CharField(max_length=100,blank=True,null=True)
    seven_twelve_available = models.CharField(max_length=10, default='no')
    mutation_entry_updated = models.CharField(max_length=10, default='no')
    property_loan = models.CharField(max_length=10, default='no')
    loan_amount = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    existing_tenants = models.CharField(max_length=10, default='no')
    tenant_details = models.TextField(blank=True, null=True)
    agri_dispute = models.CharField(max_length=10, default='no')
    dispute_details = models.TextField(blank=True, null=True)
    pending_tax_due = models.CharField(max_length=10, default='no')
    pending_tax_amount  = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)

    ########## Ameneties,Facilities and Description ###################
    
    nearby_facilities = models.TextField(blank=True, null=True) 
    amenities = models.TextField(blank=True, null=True) 
    property_summary = models.TextField(blank=True, null=True)
    property_description = models.TextField(blank=True, null=True)
    user_description = models.TextField(blank=True, null=True)

    ############# Docs,Images and Video Section ########################
    
    encumbrance_cert = models.FileField(upload_to='agricultural_docs/compliance/', blank=True, null=True)
    video_option = models.CharField(max_length=200, blank=True, null=True)
    property_video = models.FileField(upload_to='properties/videos/', null=True, blank=True)
    property_video_link = models.CharField(max_length=200, blank=True, null=True)
    listed_elsewhere = models.CharField(max_length=150, null=True, blank=True)
    portal_name = models.CharField(max_length=150, null=True, blank=True)
    
    ############### Property Uploaded By Details ############################
    
    uploaded_by_name = models.CharField(max_length=100, blank=True, null=True)
    uploaded_by_role = models.CharField(max_length=50, blank=True, null=True)
    uploaded_by_email = models.EmailField(blank=True, null=True)
    uploaded_by_contact = models.CharField(max_length=30, blank=True, null=True)
    upload_file_name = models.CharField(max_length=255, blank=True, null=True)
        
    ############# Timestamp and other details section ##########################
        
    is_deleted = models.BooleanField(default=False)
    is_duplicate = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(null=True, blank=True)
    deleted_by = models.CharField(max_length=150, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    listing_status = models.CharField(max_length=150, blank=True, null=True)
    approval_status = models.CharField(max_length=150, blank=True, null=True)

    class Meta:
        verbose_name        = "Agricultural Property"
        verbose_name_plural = "Agricultural Properties"
        ordering            = ['-created_at']

    def __str__(self):
        return f"{self.property_title or 'Agricultural Property'} ({self.id})"

    # ── AUTO-FAQ GENERATOR (FIXED FIELD NAMES TO MATCH ACTUAL MODEL) ──────────────
    def generate_auto_faqs(self):
        self.faqs.all().delete()
        faq_pool = []

        def safe_money(val):
            try:
                v = int(float(str(val or 0).replace(",", "").strip()))
                return f"Rs.{v:,}" if v else None
            except Exception:
                return None

        price_str     = safe_money(self.selling_price)
        loan_str      = safe_money(self.loan_amount)
        tax_str       = safe_money(self.pending_tax_amount)
        per_acre_str  = safe_money(self.price_per_acre_display)

        # FAQ 1 — Core Land Details
        faq_pool.append({
            "question": "What is the total land area, property type, and exact location of this agricultural property?",
            "answer": (
                f"This is a {self.property_type.replace('_',' ').title() if self.property_type else 'agricultural'} "
                f"land parcel spanning {self.land_area or 'unspecified'} Acres, situated in the village of "
                f"{self.village or '—'}, Taluka {self.taluka or '—'}, District {self.district or '—'}, {self.state or ''}."
            )
        })

        # FAQ 2 — Pricing & Brokerage (Upgraded with auto per-acre values)
        brokerage_applicable = str(self.brokerage_percentage or '').strip() not in ['', '0', '0%', 'no', 'none']
        brokerage_text = (
            f"A brokerage of {self.brokerage_percentage} applies."
            if brokerage_applicable
            else "There is no brokerage applicable for this transaction."
        )
        faq_pool.append({
            "question": "What is the expected price and brokerage structure for this agricultural land?",
            "answer": (
                f"The expected sale price for this land is {price_str or 'available on request'}. "
                + (f"This breaks down to approximately {per_acre_str} per Acre. " if per_acre_str else "")
                + brokerage_text
                + (f" Manual brokerage amount: {self.manual_brokerage}." if self.manual_brokerage else "")
            )
        })

        # FAQ 3 — Soil & Fertility
        faq_pool.append({
            "question": "What is the soil type, fertility status, and what crops have been grown previously?",
            "answer": (
                f"The land features {self.soil_type or 'standard'} soil with a fertility status classified as "
                f"'{self.fertility_status or 'not specified'}'. "
                + (f"Crops previously cultivated on this land include: {self.previous_crops}." if self.previous_crops else
                   "No specific previous crop history has been recorded.")
            )
        })

        # FAQ 4 — Irrigation & Water 
        faq_pool.append({
            "question": "Is irrigation available on this land, and what is the water source?",
            "answer": (
                f"Yes, irrigation facilities are available on this land. "
                f"The primary water source is {self.water_source_infrastructure or 'on-site/nearby'}. "
                f"This makes it suitable for year-round cultivation without dependency on seasonal rainfall."
                if str(self.irrigation_facility_active or '').lower() == 'yes' else
                f"Irrigation facilities are currently not available on this land. "
                f"Farming activities would depend on rainfall or the buyer would need to arrange independent "
                f"irrigation infrastructure. Water source: {self.water_source_infrastructure or 'Not specified'}."
            )
        })

        # FAQ 5 — Ownership & Legal
        faq_pool.append({
            "question": "What is the ownership type, and are there any active legal disputes on this land?",
            "answer": (
                f"The land is held under {self.ownership_type or 'standard'} ownership. "
                + (f"There is an active legal dispute on record: {self.dispute_section}. Buyers must verify status before proceeding."
                   if str(self.agri_dispute or '').lower() == 'yes' else
                   "The title is completely clear of any legal disputes or encumbrances.")
            )
        })

        # FAQ 6 — Tax & Loan
        tax_text = (
            f"There are pending land/revenue tax dues amounting to {tax_str}."
            if str(self.pending_tax_due or '').lower() == 'yes' else
            "All revenue and land taxes are fully cleared and up to date."
        )
        loan_text = (
            f"Yes, there is an active agricultural loan of {loan_str} registered against this property. "
            f"Buyers should account for this during title transfer."
            if str(self.property_loan or '').lower() == 'yes' else
            "No active loans or mortgages are registered against this land."
        )
        faq_pool.append({
            "question": "Are there any pending tax dues or active loans registered against this agricultural property?",
            "answer": tax_text + " " + loan_text
        })

        # FAQ 7 — Tenants / Lease
        faq_pool.append({
            "question": "Is this land currently under any tenancy or lease agreement?",
            "answer": (
                f"Yes, this land currently has active tenants or is under a lease agreement. "
                f"Tenancy details: {self.tenant_details or 'available on request'}. "
                f"Buyers must factor in tenant rights and lease terms before finalising the purchase."
                if str(self.existing_tenants or '').lower() == 'yes' else
                "This land is completely free of any tenancy or lease agreements, enabling the buyer "
                "to take immediate and unencumbered possession upon completing the sale."
            )
        })

        # FAQ 8 — Investment Potential
        faq_pool.append({
            "question": "Why is this agricultural land a good investment and what are its key highlights?",
            "answer": (
                f"This {self.property_type.replace('_',' ').title() if self.property_type else 'agricultural'} "
                f"land of {self.land_area or 'ample'} Acres in {self.village or 'a prime location'}, {self.district or ''} "
                f"offers {self.soil_type or 'fertile'} soil with {self.fertility_status or 'good'} fertility. "
                + ("Irrigation is readily available, enabling year-round cultivation. " if str(self.irrigation_facility_active or '').lower() == 'yes' else "")
                + (f"Crops like {self.previous_crops} have been successfully grown here. " if self.previous_crops else "")
                + f"Priced at {price_str or 'a competitive rate'} under {self.ownership_type or 'clear'} ownership, "
                f"it represents a strong long-term agricultural investment."
            )
        })

        AgriculturalResaleFAQ.objects.bulk_create([
            AgriculturalResaleFAQ(property=self, question=f["question"], answer=f["answer"])
            for f in faq_pool
        ])

    # ── SAVE OVERRIDE ─────────────────────────────────────────────
    # ═══════════════════════════════════════
    # AUTO DESCRIPTION GENERATOR
    # ═══════════════════════════════════════
    def generate_auto_descriptions(self):
        # Fetch safe fallbacks
        p_type = str(self.property_type).replace('_', ' ').title() if self.property_type else "Agricultural Land"
        loc = f"{self.village}, {self.taluka}, {self.district}" if (self.village and self.taluka and self.district) else "a prime agricultural zone"
        state_str = f", {self.state}" if self.state else ""

        try: price_val = int(float(str(self.selling_price or 0).strip()))
        except: price_val = 0

        try: 
            area = str(self.land_area).rstrip('0').rstrip('.') if '.' in str(self.land_area) else str(self.land_area)
        except: 
            area = "unspecified"

        # -----------------------------------
        # 1. SUMMARY TEXT (Always Regenerates)
        # -----------------------------------
        summary = f"Premium {p_type} is available for sale in {loc}{state_str}. "

        if area != "unspecified":
            summary += f"Spanning an expansive land area of {area} Acres, "

        if price_val > 0:
            summary += f"it is competitively priced at ₹{price_val:,}. "

        if str(self.irrigation_facility_active).lower() == 'yes':
            summary += "Equipped with active irrigation facilities, "

        summary += "this fertile parcel is highly suitable for robust farming, horticulture, and long-term agricultural investments."

        # Overwrite the field
        self.property_summary = summary.strip()

        # -----------------------------------
        # 2. LONG DESCRIPTION (Always Regenerates)
        # -----------------------------------
        long_desc = f"<p>Expand your agricultural portfolio with this strategically located <strong>{p_type}</strong> situated in the highly fertile belt of <strong>{loc}{state_str}</strong>.</p>"

        # --- Section A: Core Land Specifications ---
        long_desc += "<h3>Core Land Specifications:</h3><ul>"

        if area != "unspecified":
            long_desc += f"<li><strong>Total Land Area:</strong> Generous operational footprint of {area} Acres, providing ample space for scalable cultivation.</li>"

        if price_val > 0:
            long_desc += f"<li><strong>Pricing:</strong> Offered at ₹{price_val:,}.</li>"

        if self.soil_type:
            fertility = f" (Fertility Status: {self.fertility_status})" if self.fertility_status else ""
            long_desc += f"<li><strong>Soil Quality:</strong> Features {self.soil_type.capitalize()} soil profile{fertility}, optimal for diverse agricultural yields.</li>"

        if self.previous_crops:
            long_desc += f"<li><strong>Crop History:</strong> Previously cultivated crops include {self.previous_crops}, demonstrating proven land viability.</li>"

        long_desc += "</ul>"

        # --- Section B: Irrigation & Infrastructure ---
        long_desc += "<h3>Irrigation & Infrastructure:</h3><ul>"

        if str(self.irrigation_facility_active).lower() == 'yes':
            water_src = f" (Source: {self.water_source_infrastructure})" if self.water_source_infrastructure else ""
            long_desc += f"<li><strong>Irrigation Facilities:</strong> Active and functioning irrigation infrastructure is available on-site{water_src}, ensuring reliable water access for year-round farming.</li>"
        else:
            water_src = f" Nearby water source noted as {self.water_source_infrastructure}." if self.water_source_infrastructure else ""
            long_desc += f"<li><strong>Irrigation Facilities:</strong> No active structural irrigation on-site. Farming is dependent on seasonal rainfall or independent infrastructure setup.{water_src}</li>"

        long_desc += "</ul>"

        # --- Section C: Legal Clearances & Ownership Status ---
        long_desc += "<h3>Legal Clearances & Ownership Status:</h3><ul>"

        if self.ownership_type:
            long_desc += f"<li><strong>Ownership Status:</strong> Held under {self.ownership_type.capitalize()} ownership title.</li>"

        if str(self.existing_tenants).lower() == 'yes':
            long_desc += f"<li><strong>Occupancy:</strong> Currently leased or occupied by active farming tenants ({self.tenant_details or 'Details on request'}).</li>"
        else:
            long_desc += "<li><strong>Occupancy:</strong> Offered with immediate vacant possession.</li>"

        if str(self.agri_dispute).lower() == 'yes':
            long_desc += f"<li><strong>Legal Status:</strong> Active legal dispute noted ({self.dispute_section or 'Pending resolution'}).</li>"
        else:
            long_desc += "<li><strong>Legal Status:</strong> Verified clear agricultural title with no active legal disputes.</li>"

        if str(self.property_loan).lower() == 'yes':
            loan_v = f" (₹{self.loan_amount:,})" if self.loan_amount else ""
            long_desc += f"<li><strong>Financial Encumbrances:</strong> Active agricultural loan/mortgage registered against the asset{loan_v}.</li>"
        else:
            long_desc += "<li><strong>Financial Encumbrances:</strong> Free from active banking or mortgage holds.</li>"

        if str(self.pending_tax_due).lower() == 'yes':
            tax_v = f" (₹{self.pending_tax_amount:,})" if self.pending_tax_amount else ""
            long_desc += f"<li><strong>Tax Compliance:</strong> Pending land/revenue tax dues{tax_v}.</li>"
        else:
            long_desc += "<li><strong>Tax Compliance:</strong> All revenue and land taxes are fully cleared up to date.</li>"

        long_desc += "</ul>"

        long_desc += "<p>This is a high-value agricultural asset tailored for serious farming operations or long-term land banking. Contact us today to schedule a site inspection and review land records!</p>"

        # Overwrite the field
        self.property_description = long_desc

    # ═══════════════════════════════════════
    # SAVE METHOD
    # ═══════════════════════════════════════
    def save(self, *args, **kwargs):
        # 1. Auto-generate price per acre values
        if self.selling_price and self.land_area:
            try:
                area  = float(self.land_area)
                price = float(self.selling_price)
                if area > 0:
                    self.price_per_acre_display = round(price / area, 2)
            except (ValueError, TypeError):
                pass

        # 2. Auto-generate property_title
        if not self.property_title:
            type_lbl = self.property_type.replace('_', ' ').title() if self.property_type else "Land"
            try:
                area_val = float(self.land_area)
                area_lbl = f"{int(area_val)} Acres" if area_val == int(area_val) else f"{area_val} Acres"
            except (ValueError, TypeError):
                area_lbl = ""
            location_ctx = f" in {self.village}, {self.taluka}" if self.village and self.taluka else ""
            district_ctx = f" ({self.district})" if self.district else ""
            self.property_title = " ".join(f"{area_lbl} Fertile {type_lbl}{location_ctx}{district_ctx}".split())

        # ---> Trigger Auto Description Generation BEFORE saving <---
        self.generate_auto_descriptions()

        # 3. Save Record
        super().save(*args, **kwargs)

        # 4. Regenerate all FAQs on every create & update
        self.generate_auto_faqs()

# ══════════════════════════════════════════════════════════════════
#  MODEL 3 — AgriculturalResaleFAQ  (NEW)
#  Auto-populated by generate_auto_faqs() on every save
# ══════════════════════════════════════════════════════════════════

class AgriculturalResaleFAQ(models.Model):
    property = models.ForeignKey(
        AgriculturalResaleProperty,
        on_delete=models.CASCADE,
        related_name='faqs'
    )
    question = models.CharField(max_length=500)
    answer   = models.TextField()

    class Meta:
        ordering = ['id']

    def __str__(self):
        return f"FAQ: {self.question[:60]}"


class AgriculturalPropertyImage(models.Model):

    CATEGORY_CHOICES = [
        ('land_overview', 'Land Overview / Wide View'),
        ('soil_quality', 'Soil Quality & Texture'),
        ('water_source', 'Water Source (Borewell / Canal / Well)'),
        ('irrigation_system', 'Irrigation System'),
        ('crop_cultivation', 'Current Crops / Cultivation'),
        ('farm_house', 'Farmhouse / Built-up Structure'),
        ('electricity_setup', 'Electricity & Transformer Setup'),
        ('storage_shed', 'Storage Shed / Godown'),
        ('boundary_fencing', 'Boundary & Fencing'),
        ('approach_road', 'Approach Road / Connectivity'),
        ('tubewell_pump', 'Tubewell & Pump Room'),
        ('aerial_drone', 'Aerial / Drone View'),
    ]
    
    property = models.ForeignKey(AgriculturalResaleProperty, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to="resale_agricultural/")
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='others')
    sequence_order = models.PositiveIntegerField(default=0)
    
    class Meta:
        ordering = ["category", "sequence_order"]


class ResaleAgriculturalVideo(models.Model):
    SOURCE_CHOICES = [('uploaded', 'Manually Uploaded'), ('auto', 'Auto Generated Slideshow'),('rm_assisted', 'RM Assisted Link'),]
    property = models.ForeignKey(AgriculturalResaleProperty, on_delete=models.CASCADE, related_name="video")
    video = models.FileField(upload_to="agriculture_resale/videos/")
    video_url = models.URLField(null=True, blank=True)
    source = models.CharField(max_length=100, choices=SOURCE_CHOICES, default='auto')
    video_status = models.CharField(max_length=255, blank=True, null=True,default="Pending")
    created_at = models.DateTimeField(auto_now_add=True)

    def youtube_thumbnail(self):
        import re
        if self.source == 'rm_assisted' and self.video_url:
            match = re.search(
                r'(?:youtube\.com/watch\?v=|youtu\.be/|youtube\.com/shorts/)([A-Za-z0-9_-]{6,})',
                self.video_url
            )
            if match:
                return f"https://img.youtube.com/vi/{match.group(1)}/hqdefault.jpg"
        return None




################### Modal Start for Residential Resale Plot #########################


def generate_residential_plot_id():
    return f"EFIPR-{uuid.uuid4().hex[:8].upper()}"


class ResidentialPlotResaleProperty(models.Model):
    id = models.CharField(
        max_length=20,
        primary_key=True,
        default=generate_residential_plot_id,
        editable=False,
    )

    # ── STEP 1: LISTED BY ──────────────────────────────────────────────────
    listing_type = models.CharField(max_length=100, blank=True, null=True)
    category = models.CharField(max_length=100, blank=True, null=True)
    sub_category = models.CharField(max_length=100, blank=True, null=True)

    listed_by_type = models.CharField(max_length=100, blank=True, null=True)
    assigned_to = models.CharField(max_length=50, blank=True, null=True)
  
    listed_by_id = models.CharField(max_length=150, blank=True, null=True)
    listed_by_name = models.CharField(max_length=150, blank=True, null=True)
    listed_by_email = models.CharField(max_length=150, blank=True, null=True)
    listed_by_contact = models.CharField(max_length=20, blank=True, null=True)
    listed_by_role = models.CharField(max_length=100, blank=True, null=True)

    # ── DUPLICATE DETECTION ─────────────────────────────────────────────────
    property_unique_key = models.CharField(max_length=255, blank=True, null=True, db_index=True)
    duplicate_count = models.PositiveIntegerField(default=0)
    duplicate_group_id = models.CharField(max_length=255, blank=True, null=True, db_index=True)   # <-- drives the duplicate label

    ############# Basic Residential Plot Information ##########################

    property_title = models.CharField(max_length=255, blank=True, null=True)
    property_no = models.CharField(max_length=150, blank=True, null=True)
    plot_area = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    property_type = models.CharField(max_length=100, blank=True, null=True)

    ########## Zone Classiification and Township Approvals #######################

    land_use = models.CharField(max_length=100, blank=True, null=True)
    na_status = models.CharField(max_length=100, blank=True, null=True)
    layout_approval_status = models.CharField(max_length=200, blank=True, null=True)
    residential_zone_type = models.CharField(max_length=100, blank=True, null=True)
    gated_community = models.CharField(max_length=100, blank=True, null=True)
    layout_name = models.CharField(max_length=50, blank=True, null=True)

    ############# Plot Specification and Physical Details #######################

    plot_frontage = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)  # metres
    plot_depth = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)     # metres
    plot_shape = models.CharField(max_length=100, blank=True, null=True)
    road_connectivity = models.CharField(max_length=100, blank=True, null=True)
    road_width = models.CharField(max_length=50, blank=True, null=True)
    corner_plot = models.CharField(max_length=20, default="no")
    plot_facing = models.CharField(max_length=50, blank=True, null=True)
    plot_fencing = models.CharField(max_length=50, blank=True, null=True)
    current_possession_status = models.CharField(max_length=50, blank=True, null=True)

    ################# Pricing Details Section #############################

    selling_price = models.BigIntegerField(blank=True, null=True)
    plot_price_per_sqft = models.BigIntegerField(blank=True, null=True)
    price_negotiable = models.CharField(max_length=20, default="no")
    additional_charges = models.CharField(max_length=100, blank=True, null=True)
    brokerage_percentage = models.CharField(max_length=100, blank=True, null=True)
    manual_brokerage = models.CharField(max_length=100, blank=True, null=True)

    ############## Legal Title and Approval Status Details #######################

    ownership_type = models.CharField(max_length=100, blank=True, null=True)
    ownership_document_type = models.CharField(max_length=150, blank=True, null=True)
    other_document_type = models.CharField(max_length=150, blank=True, null=True)
    rera_status = models.CharField(max_length=100, blank=True, null=True)
    title_clearance = models.CharField(max_length=100, blank=True, null=True)
    property_encumbrance_status = models.CharField(max_length=100, blank=True, null=True)
    property_tax_status = models.CharField(max_length=100, blank=True, null=True)
    title_clearance = models.CharField(max_length=100, blank=True, null=True)
    outstanding_tax_amount = models.BigIntegerField(blank=True, null=True)
    pending_since = models.DateField(blank=True, null=True)
    property_loan_status = models.CharField(max_length=100, blank=True, null=True)
    financing_bank = models.CharField(max_length=150, blank=True, null=True)
    outstanding_loan_amount = models.BigIntegerField(blank=True, null=True)
    sanctioning_authority = models.TextField(blank=True, null=True)

    ################# Ameneties,Facilities and Location ######################

    amenities = models.TextField(blank=True, null=True)
    nearby_facilities = models.TextField(blank=True, null=True)
    user_description = models.TextField(blank=True, null=True)
    property_summary = models.TextField(blank=True, null=True)
    property_description = models.TextField(blank=True, null=True)

    state = models.CharField(max_length=100, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    locality = models.CharField(max_length=200, blank=True, null=True)
    property_landmark = models.CharField(max_length=200, blank=True, null=True)
    pincode = models.CharField(max_length=20, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    google_maps_link = models.URLField(max_length=500, blank=True, null=True)
    latitude = models.CharField(max_length=50, blank=True, null=True)
    longitude = models.CharField(max_length=50, blank=True, null=True)

    ################# Photos and Media Section ########################

    encumbrance_cert = models.FileField(upload_to="residential_plot/docs/", blank=True, null=True)
    layout_plan = models.FileField(upload_to="residential_plot/docs/", blank=True, null=True)
    video_option = models.CharField(max_length=200, blank=True, null=True)
    property_video = models.FileField(upload_to='properties/videos/', null=True, blank=True)
    property_video_link = models.CharField(max_length=200, blank=True, null=True)
    listed_elsewhere = models.CharField(max_length=10, default="No")
    portal_name = models.CharField(max_length=100, blank=True, null=True)

    ################## Property Uploaded By Section #########################

    uploaded_by_name = models.CharField(max_length=150, blank=True, null=True)
    uploaded_by_email = models.CharField(max_length=150, blank=True, null=True)
    uploaded_by_contact = models.CharField(max_length=50, blank=True, null=True)
    uploaded_by_role = models.CharField(max_length=100, blank=True, null=True)
    upload_file_name = models.CharField(max_length=255, blank=True, null=True)
    upload_file = models.FileField(upload_to='residential_resaleplot_property_uploads/files/', blank=True, null=True)

    is_deleted = models.BooleanField(default=False)
    
    is_duplicate = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(null=True, blank=True)
    deleted_by = models.CharField(max_length=150, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    listing_status = models.CharField(max_length=150, blank=True, null=True)
    approval_status = models.CharField(max_length=150, blank=True, null=True)

    # ═══════════════════════════════════════════════════════════════════════
    #  INDUSTRIAL RESALE BROKERAGE LOGIC
    # ═══════════════════════════════════════════════════════════════════════
    BROKERAGE_LABEL_MAP = {
        "admin": "EstateFlow Service Fee",
        "relationship manager": "Buyer Service Fee",
        "landlord": "Buyer Service Fee",
        "owner": "Buyer Service Fee",
        "seller": "Buyer Service Fee",
        "agent": "Brokerage",
        "agency/builder": "Brokerage / Service Fee",
        "builder": "Brokerage / Service Fee",
    }

    def get_brokerage_label(self):
        role = (self.listed_by_role or "").strip().lower()
        return self.BROKERAGE_LABEL_MAP.get(role, "Brokerage")

    def get_brokerage_display_value(self):
        if self.brokerage_percentage == "Fixed Amount":
            return self.manual_brokerage or "-"
        return self.brokerage_percentage or "-"

    # ═══════════════════════════════════════════════════════════════════════
    #  AUTO DESCRIPTIONS ENGINE
    # ═══════════════════════════════════════════════════════════════════════
    def generate_auto_descriptions(self):
        p_type = (self.property_type or "Residential Plot").replace("_", " ").title()
        area_str = f"{self.plot_area} sq.ft" if self.plot_area else "Prime Plot Area"
       
        loc = self.locality or "Prime Residential Area"
        city_str = f", {self.city}" if self.city else ""

        # Summary
        summary = f"A strategic {area_str} {p_type} is available for resale at {loc}{city_str}. "
        if self.selling_price:
            summary += f"Listed at an attractive price of ₹{self.selling_price:,}. "
        if self.gated_community and self.gated_community.lower() == 'yes':
            layout_text = f" in {self.layout_name}" if self.layout_name else ""
            summary += f"Located within a gated community{layout_text}. "
        summary += "Well-suited for custom home construction, independent villas, and long-term land investment."
        self.property_summary = summary

        # Detailed Description
        long_desc = f"<p>Build your dream home or secure a high-value asset with this strategically situated <strong>{area_str} {p_type}</strong> located in <strong>{loc}{city_str}</strong>.</p>"

        long_desc += "<h3>Key Plot Specifications:</h3><ul>"
        if self.plot_area:
            long_desc += f"<li><strong>Plot Area & Dimensions:</strong> Total area of {self.plot_area} sq.ft (Frontage: {self.plot_frontage or '—'} ft x Depth: {self.plot_depth or '—'} ft). Shape: {self.plot_shape or 'Regular'}.</li>"
        long_desc += f"<li><strong>Road Access & Facing:</strong> Abuts a {self.road_width or 'Standard'} ft road with '{self.road_connectivity or 'Direct Road Access'}'. Corner plot: {self.corner_plot.upper()}. Facing: {self.plot_facing or 'Not Specified'}.</li>"
        if self.selling_price:
            psq = round(float(self.selling_price) / float(self.plot_area)) if (self.plot_area and float(self.plot_area) > 0) else 0
            long_desc += f"<li><strong>Valuation:</strong> Listed at ₹{self.selling_price:,} (~₹{psq:,}/sq.ft). Negotiable: {self.price_negotiable.upper()}.</li>"
        long_desc += f"<li><strong>Current Possession Status:</strong> Offered in '{self.current_possession_status or 'Vacant & Immediate Possession'}' condition.</li>"
        long_desc += "</ul>"

        long_desc += "<h3>Zoning & Approvals:</h3><ul>"
        long_desc += f"<li><strong>Land Use & Zone:</strong> Classified under Land Use '{self.land_use or 'Residential'}' (Zone Type: {self.residential_zone_type or 'As per norms'}).</li>"
        long_desc += f"<li><strong>Legal Status (NA & Layout):</strong> NA Status: {self.na_status or 'Converted'}. Layout Approval: {self.layout_approval_status or 'Approved'}.</li>"
        long_desc += f"<li><strong>Community Type:</strong> Gated Community / Layout: {self.gated_community.upper()} {f'({self.layout_name})' if self.layout_name else ''}.</li>"
        long_desc += "</ul>"

        long_desc += "<h3>Legal & Title Clearances:</h3><ul>"
        long_desc += f"<li><strong>Tenure & Documentation:</strong> {self.ownership_type or 'Freehold'} tenure. Primary Document: {self.ownership_document_type or 'Sale Deed'}.</li>"
        long_desc += f"<li><strong>Title Clarity:</strong> Title status is verified as '{self.title_clearance or 'Clear & Marketable'}'. RERA Status: {self.rera_status or 'Exempt/Applicable'}.</li>"
        long_desc += "</ul>"

        if self.amenities:
            long_desc += f"<h3>Layout Infrastructure & Amenities:</h3><p>The property features community highlights including: <strong>{self.amenities}</strong>.</p>"

        long_desc += "<p>Contact us immediately to arrange a site visit or verify property documents with our legal team.</p>"
        self.property_description = long_desc

    # ═══════════════════════════════════════════════════════════════════════
    #  SAVE OVERRIDE
    # ═══════════════════════════════════════════════════════════════════════
    def save(self, *args, **kwargs):
        area_lbl = f"{self.plot_area} sq.ft" if self.plot_area else ""
        p_type = (self.property_type or "Residential Plot").replace("_", " ").title()
        loc = self.locality or ""
        city_name = f", {self.city}" if self.city else ""

        self.property_title = " ".join(filter(bool, [area_lbl, p_type, "for Sale in", loc + city_name]))[:255]
        self.generate_auto_descriptions()
        super().save(*args, **kwargs)
        self.generate_auto_faqs()

    # ═══════════════════════════════════════════════════════════════════════
    #  AUTO FAQ ENGINE
    # ═══════════════════════════════════════════════════════════════════════
    def generate_auto_faqs(self):
        """
        Automatically generates buyer-friendly FAQs for Residential Plot Resale.
        """

        # Delete previously generated FAQs before recreating them
        self.faqs.all().delete()

        faq_pool = []

        # ═══════════════════════════════════════════════════════════════════
        # 1. PLOT AREA & SPECIFICATIONS
        # ═══════════════════════════════════════════════════════════════════

        if self.plot_area or self.property_type or self.plot_frontage or self.plot_depth:

            dimensions = ""

            if self.plot_frontage and self.plot_depth:
                dimensions = (
                    f" The plot measures approximately "
                    f"{self.plot_frontage} ft frontage × {self.plot_depth} ft depth."
                )
            elif self.plot_frontage:
                dimensions = (
                    f" The available frontage is approximately "
                    f"{self.plot_frontage} ft."
                )
            elif self.plot_depth:
                dimensions = (
                    f" The available depth is approximately "
                    f"{self.plot_depth} ft."
                )

            plot_type = (
                (self.property_type or "Residential Plot")
                .replace("_", " ")
                .title()
            )

            shape = (
                f" The plot shape is {self.plot_shape}."
                if self.plot_shape
                else ""
            )

            faq_pool.append({
                "q": "What is the plot area and specification of this residential plot?",
                "a": (
                    f"This is a {plot_type} "
                    f"with a plot area of "
                    f"{self.plot_area or 'not specified'} sq.ft."
                    f"{dimensions}{shape}"
                ),
            })

        # ═══════════════════════════════════════════════════════════════════
        # 2. PRICE & BROKERAGE
        # ═══════════════════════════════════════════════════════════════════

        if self.selling_price or self.plot_price_per_sqft:

            price_parts = []

            if self.selling_price:
                price_parts.append(
                    f"The asking price is ₹{self.selling_price:,}."
                )

            if self.plot_price_per_sqft:
                price_parts.append(
                    f"The listed rate is approximately "
                    f"₹{self.plot_price_per_sqft:,} per sq.ft."
                )

            if self.price_negotiable:
                price_parts.append(
                    f"Price negotiability is marked as "
                    f"'{self.price_negotiable}'."
                )

            if self.additional_charges:
                price_parts.append(
                    f"Additional charges, if applicable, are "
                    f"'{self.additional_charges}'."
                )

            faq_pool.append({
                "q": "What is the price of this residential plot?",
                "a": " ".join(price_parts),
            })

        # Brokerage FAQ
        if self.brokerage_percentage or self.manual_brokerage:

            label = self.get_brokerage_label() if hasattr(self, 'get_brokerage_label') else "Brokerage"
            value = self.get_brokerage_display_value() if hasattr(self, 'get_brokerage_display_value') else (self.manual_brokerage or self.brokerage_percentage)

            faq_pool.append({
                "q": "Is there any brokerage or service fee applicable to this plot?",
                "a": (
                    f"The applicable {label.lower()} for this property "
                    f"is {value}."
                ),
            })

        # ═══════════════════════════════════════════════════════════════════
        # 3. ZONING & LAYOUT APPROVAL
        # ═══════════════════════════════════════════════════════════════════

        zoning_parts = []

        if self.land_use:
            zoning_parts.append(
                f"Land use is classified as '{self.land_use}'."
            )

        if self.na_status:
            zoning_parts.append(
                f"NA status is '{self.na_status}'."
            )

        if self.layout_approval_status:
            zoning_parts.append(
                f"Layout approval status is "
                f"'{self.layout_approval_status}'."
            )

        if self.residential_zone_type:
            zoning_parts.append(
                f"The residential zone type is "
                f"'{self.residential_zone_type}'."
            )

        if self.layout_name:
            zoning_parts.append(
                f"The plot is part of the '{self.layout_name}' layout."
            )

        if zoning_parts:
            faq_pool.append({
                "q": "Is this residential plot approved and suitable for residential use?",
                "a": " ".join(zoning_parts),
            })

        # ═══════════════════════════════════════════════════════════════════
        # 4. ROAD ACCESS & PLOT FEATURES
        # ═══════════════════════════════════════════════════════════════════

        access_parts = []

        if self.road_connectivity:
            access_parts.append(
                f"Road connectivity is described as "
                f"'{self.road_connectivity}'."
            )

        if self.road_width:
            access_parts.append(
                f"The road width is {self.road_width} ft."
            )

        if self.corner_plot:
            if str(self.corner_plot).lower() == "yes":
                access_parts.append(
                    "This is a corner plot with access from two roads."
                )
            else:
                access_parts.append(
                    "This is not marked as a corner plot."
                )

        if self.plot_facing:
            access_parts.append(
                f"The plot is {self.plot_facing}-facing."
            )

        if self.plot_fencing:
            access_parts.append(
                f"Plot fencing status is '{self.plot_fencing}'."
            )

        if access_parts:
            faq_pool.append({
                "q": "What are the road access, facing and plot features?",
                "a": " ".join(access_parts),
            })

        # ═══════════════════════════════════════════════════════════════════
        # 5. LEGAL, TITLE & DOCUMENTS
        # ═══════════════════════════════════════════════════════════════════

        legal_parts = []

        if self.ownership_type:
            legal_parts.append(
                f"Ownership type is '{self.ownership_type}'."
            )

        if self.ownership_document_type:
            legal_parts.append(
                f"Ownership document type is "
                f"'{self.ownership_document_type}'."
            )

        if self.rera_status:
            legal_parts.append(
                f"RERA status is '{self.rera_status}'."
            )

        if self.title_clearance:
            legal_parts.append(
                f"Title clearance status is "
                f"'{self.title_clearance}'."
            )

        if self.property_encumbrance_status:
            legal_parts.append(
                f"Property encumbrance status is "
                f"'{self.property_encumbrance_status}'."
            )

        if self.property_tax_status:
            legal_parts.append(
                f"Property tax status is "
                f"'{self.property_tax_status}'."
            )

        if self.sanctioning_authority:
            legal_parts.append(
                f"Sanctioning authority information: "
                f"{self.sanctioning_authority}."
            )

        if legal_parts:
            faq_pool.append({
                "q": "What are the legal, title and approval details of this plot?",
                "a": " ".join(legal_parts),
            })

        # ═══════════════════════════════════════════════════════════════════
        # 6. LOCATION, AMENITIES & CONNECTIVITY
        # ═══════════════════════════════════════════════════════════════════

        location_parts = []

        location_name = " ".join(
            filter(
                bool,
                [
                    self.locality,
                    self.city,
                    self.state
                ]
            )
        )

        if location_name:
            location_parts.append(
                f"The plot is located in {location_name}."
            )

        if self.property_landmark:
            location_parts.append(
                f"Nearby landmark: {self.property_landmark}."
            )

        if self.pincode:
            location_parts.append(
                f"The property PIN code is {self.pincode}."
            )

        if self.nearby_facilities:
            location_parts.append(
                f"Nearby facilities include: "
                f"{self.nearby_facilities}."
            )

        if self.amenities:
            location_parts.append(
                f"Available amenities/infrastructure include: "
                f"{self.amenities}."
            )

        if self.gated_community:
            location_parts.append(
                f"Gated community status is "
                f"'{self.gated_community}'."
            )

        if location_parts:
            faq_pool.append({
                "q": "Where is the plot located and what facilities are nearby?",
                "a": " ".join(location_parts),
            })

        # ═══════════════════════════════════════════════════════════════════
        # 7. POSSESSION, LOAN & INVESTMENT
        # ═══════════════════════════════════════════════════════════════════

        investment_parts = []

        if self.current_possession_status:
            investment_parts.append(
                f"Current possession status is "
                f"'{self.current_possession_status}'."
            )

        if self.property_loan_status:
            investment_parts.append(
                f"Property loan status is "
                f"'{self.property_loan_status}'."
            )

        if self.financing_bank:
            investment_parts.append(
                f"Financing bank: {self.financing_bank}."
            )

        if self.outstanding_loan_amount:
            investment_parts.append(
                f"Outstanding loan amount is "
                f"₹{self.outstanding_loan_amount:,}."
            )

        if self.property_tax_status:
            investment_parts.append(
                f"Property tax status is "
                f"'{self.property_tax_status}'."
            )

        if investment_parts:
            faq_pool.append({
                "q": "What is the possession and financial status of this plot?",
                "a": " ".join(investment_parts),
            })

        # ═══════════════════════════════════════════════════════════════════
        # CREATE FAQ RECORDS
        # ═══════════════════════════════════════════════════════════════════

        for item in faq_pool:
            ResidentialPlotResaleFAQ.objects.create(
                property=self,
                question=item["q"],
                answer=item["a"]
            )

    def __str__(self):
        return f"{self.property_title or 'Residential Plot Resale'} ({self.id})"


# ==========================================================
# INDUSTRIAL PLOT RESALE — IMAGE MODEL (Category-wise, like RentalResidentialImage)
# ==========================================================

class ResidentialPlotResaleImage(models.Model):
    CATEGORY_CHOICES = [
        ('front_view',       'Front View'),
        ('full_plot',        'Full Plot View'),
        ('road_facing',      'Road Facing'),
        ('entrance_access',  'Entrance / Access'),
        ('boundary',         'Boundary'),
        ('layout_plan',      'Layout Plan'),
        ('surroundings',     'Surroundings'),
        ('amenities_infra',  'Amenities / Infrastructure'),
    ]

    property = models.ForeignKey(
        'ResidentialPlotResaleProperty',
        on_delete=models.CASCADE,
        related_name="images"
    )
    image = models.ImageField(upload_to="residential_plot/images/")
    category = models.CharField(max_length=30, choices=CATEGORY_CHOICES, default='full_plot')
    sequence_order = models.PositiveIntegerField(default=0)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["category", "sequence_order", "uploaded_at"]

    def __str__(self):
        return f"{self.property_id} - {self.get_category_display()} ({self.sequence_order})"


# ==========================================================
# INDUSTRIAL PLOT RESALE — VIDEO MODEL (same 3-source pattern as RentalResidentialVideo)
# ==========================================================

class ResidentialPlotResaleVideo(models.Model):
    SOURCE_CHOICES = [
        ('uploaded',    'Manually Uploaded'),
        ('auto',        'Auto Generated Slideshow'),
        ('rm_assisted', 'RM Assisted Link'),
    ]
    property = models.ForeignKey(
        'ResidentialPlotResaleProperty',
        on_delete=models.CASCADE,
        related_name="video"
    )
    video = models.FileField(upload_to="residential_plot/videos/", null=True, blank=True)
    video_url = models.URLField(null=True, blank=True)
    source = models.CharField(max_length=15, choices=SOURCE_CHOICES, default='auto')
    video_status = models.CharField(max_length=255, blank=True, null=True,default="Pending")
    created_at = models.DateTimeField(auto_now_add=True)

    def youtube_thumbnail(self):
        import re
        if self.source == 'rm_assisted' and self.video_url:
            match = re.search(
                r'(?:youtube\.com/watch\?v=|youtu\.be/|youtube\.com/shorts/)([A-Za-z0-9_-]{6,})',
                self.video_url
            )
            if match:
                return f"https://img.youtube.com/vi/{match.group(1)}/hqdefault.jpg"
        return None

    def get_platform_type(self):
        if not self.video_url:
            return 'unknown'
        url = self.video_url.lower()
        if 'youtube.com' in url or 'youtu.be' in url:
            return 'youtube'
        elif 'instagram.com' in url or 'instagr.am' in url:
            return 'instagram'
        elif 'facebook.com' in url or 'fb.watch' in url:
            return 'facebook'
        elif 'vimeo.com' in url:
            return 'vimeo'
        elif 'drive.google.com' in url:
            return 'gdrive'
        return 'external'




class ResidentialPlotResaleFAQ(models.Model):
    property = models.ForeignKey(ResidentialPlotResaleProperty, on_delete=models.CASCADE, related_name="faqs")
    question = models.CharField(max_length=255)
    answer = models.TextField()


class ResidentialPlotResaleActivityLog(models.Model):
    ACTION_CHOICES = [
        ("CREATE", "Property Entry Created"),
        ("UPDATE", "Record Update Action"),
        ("DELETE", "Deletion / Purge Record"),
    ]
    timestamp = models.DateTimeField(auto_now_add=True)
    user_identity = models.CharField(max_length=255, null=True, blank=True)
    user_role = models.CharField(max_length=100, null=True, blank=True)
    action_type = models.CharField(max_length=50, choices=ACTION_CHOICES)
    property_id = models.CharField(max_length=100, null=True, blank=True)
    action_payload = models.TextField(null=True, blank=True)
    status = models.CharField(max_length=20, default="SUCCESS")

    class Meta:
        ordering = ["-timestamp"]


############ Modal End for Residential Resale Plot ##############################


############## Modal Start for Commercial Resale Plot ########################

def generate_commercial_plot_id():
    return f"EFIPR-{uuid.uuid4().hex[:8].upper()}"

class CommercialPlotResaleProperty(models.Model):
    id = models.CharField(
        max_length=20,
        primary_key=True,
        default=generate_commercial_plot_id,
        editable=False,
    )

    # ── STEP 1: LISTED BY ──────────────────────────────────────────────────
    listing_type = models.CharField(max_length=100, blank=True, null=True)
    category = models.CharField(max_length=100, blank=True, null=True)
    sub_category = models.CharField(max_length=100, blank=True, null=True)

    listed_by_type = models.CharField(max_length=100, blank=True, null=True)
    assigned_to = models.CharField(max_length=50, blank=True, null=True)
  
    listed_by_id = models.CharField(max_length=150, blank=True, null=True)
    listed_by_name = models.CharField(max_length=150, blank=True, null=True)
    listed_by_email = models.CharField(max_length=150, blank=True, null=True)
    listed_by_contact = models.CharField(max_length=20, blank=True, null=True)
    listed_by_role = models.CharField(max_length=100, blank=True, null=True)

    # ── DUPLICATE DETECTION ─────────────────────────────────────────────────
    property_unique_key = models.CharField(max_length=255, blank=True, null=True, db_index=True)
    duplicate_count = models.PositiveIntegerField(default=0)
    duplicate_group_id = models.CharField(max_length=255, blank=True, null=True, db_index=True)   # <-- drives the duplicate label

    ############# Basic Commercial Plot Information ##########################

    property_title = models.CharField(max_length=255, blank=True, null=True)
    property_no = models.CharField(max_length=150, blank=True, null=True)
    plot_area = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    property_type = models.CharField(max_length=100, blank=True, null=True)

    ########## Zone Classiification FSI and Commercial #######################

    land_use = models.CharField(max_length=100, blank=True, null=True)
    commercial_zone_type = models.CharField(max_length=100, blank=True, null=True)
    na_status = models.CharField(max_length=100, blank=True, null=True)
    layout_approval_status = models.CharField(max_length=200, blank=True, null=True)
    permissible_fsi = models.CharField(max_length=100, blank=True, null=True)
    ground_coverage = models.CharField(max_length=100, blank=True, null=True)

    ############# Plot Specification and Physical Details #######################

    plot_depth = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)  # metres
    plot_frontage = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)     # metres
    plot_shape = models.CharField(max_length=100, blank=True, null=True)
    road_connectivity = models.CharField(max_length=100, blank=True, null=True)
    road_width = models.CharField(max_length=50, blank=True, null=True)
    plot_visibility = models.CharField(max_length=200, blank=True, null=True)
    proposed_use = models.CharField(max_length=200, blank=True, null=True)
    parking_availability = models.CharField(max_length=200, blank=True, null=True)
    plot_fencing = models.CharField(max_length=50, blank=True, null=True)
    current_possession_status = models.CharField(max_length=50, blank=True, null=True)

    ################# Pricing Details Section #############################

    selling_price = models.BigIntegerField(blank=True, null=True)
    plot_price_per_sqft = models.BigIntegerField(blank=True, null=True)
    price_negotiable = models.CharField(max_length=20, default="no")
    additional_charges = models.CharField(max_length=100, blank=True, null=True)
    brokerage_percentage = models.CharField(max_length=100, blank=True, null=True)
    manual_brokerage = models.CharField(max_length=100, blank=True, null=True)

    ############## Legal Title and Approval Status Details #######################

    ownership_type = models.CharField(max_length=100, blank=True, null=True)
    ownership_document_type = models.CharField(max_length=150, blank=True, null=True)
    other_document_type = models.CharField(max_length=150, blank=True, null=True)
    rera_status = models.CharField(max_length=100, blank=True, null=True)
    title_clearance = models.CharField(max_length=100, blank=True, null=True)
    property_encumbrance_status = models.CharField(max_length=100, blank=True, null=True)
    property_tax_status = models.CharField(max_length=100, blank=True, null=True)
    outstanding_tax_amount = models.BigIntegerField(blank=True, null=True)
    pending_since = models.DateField(blank=True, null=True)
    property_loan_status = models.CharField(max_length=100, blank=True, null=True)
    financing_bank = models.CharField(max_length=150, blank=True, null=True)
    outstanding_loan_amount = models.BigIntegerField(blank=True, null=True)
    sanctioning_authority = models.TextField(blank=True, null=True)

    ################# Ameneties,Facilities and Location ######################

    amenities = models.TextField(blank=True, null=True)
    nearby_facilities = models.TextField(blank=True, null=True)
    user_description = models.TextField(blank=True, null=True)
    property_summary = models.TextField(blank=True, null=True)
    property_description = models.TextField(blank=True, null=True)

    state = models.CharField(max_length=100, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    locality = models.CharField(max_length=200, blank=True, null=True)
    property_landmark = models.CharField(max_length=200, blank=True, null=True)
    pincode = models.CharField(max_length=20, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    google_maps_link = models.URLField(max_length=500, blank=True, null=True)
    latitude = models.CharField(max_length=50, blank=True, null=True)
    longitude = models.CharField(max_length=50, blank=True, null=True)

    ################# Photos and Media Section ########################

    encumbrance_cert = models.FileField(upload_to="commercial_plot/docs/", blank=True, null=True)
    layout_plan = models.FileField(upload_to="commercial_plot/docs/", blank=True, null=True)
    video_option = models.CharField(max_length=200, blank=True, null=True)
    property_video = models.FileField(upload_to='properties/videos/', null=True, blank=True)
    property_video_link = models.CharField(max_length=200, blank=True, null=True)
    listed_elsewhere = models.CharField(max_length=10, default="No")
    portal_name = models.CharField(max_length=100, blank=True, null=True)

    ################## Property Uploaded By Section #########################

    uploaded_by_name = models.CharField(max_length=150, blank=True, null=True)
    uploaded_by_email = models.CharField(max_length=150, blank=True, null=True)
    uploaded_by_contact = models.CharField(max_length=50, blank=True, null=True)
    uploaded_by_role = models.CharField(max_length=100, blank=True, null=True)
    upload_file_name = models.CharField(max_length=255, blank=True, null=True)
    upload_file = models.FileField(upload_to='commercial_resaleplot_property_uploads/files/', blank=True, null=True)

    is_deleted = models.BooleanField(default=False)
    
    is_duplicate = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(null=True, blank=True)
    deleted_by = models.CharField(max_length=150, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    listing_status = models.CharField(max_length=150, blank=True, null=True)
    approval_status = models.CharField(max_length=150, blank=True, null=True)

    # ═══════════════════════════════════════════════════════════════════════
    #  INDUSTRIAL RESALE BROKERAGE LOGIC
    # ═══════════════════════════════════════════════════════════════════════
    BROKERAGE_LABEL_MAP = {
        "admin": "EstateFlow Service Fee",
        "relationship manager": "Buyer Service Fee",
        "landlord": "Buyer Service Fee",
        "owner": "Buyer Service Fee",
        "seller": "Buyer Service Fee",
        "agent": "Brokerage",
        "agency/builder": "Brokerage / Service Fee",
        "builder": "Brokerage / Service Fee",
    }

    def get_brokerage_label(self):
        role = (self.listed_by_role or "").strip().lower()
        return self.BROKERAGE_LABEL_MAP.get(role, "Brokerage")

    def get_brokerage_display_value(self):
        if self.brokerage_percentage == "Fixed Amount":
            return self.manual_brokerage or "-"
        return self.brokerage_percentage or "-"

    # ═══════════════════════════════════════════════════════════════════════
    #  AUTO DESCRIPTIONS ENGINE (COMMERCIAL PLOT)
    # ═══════════════════════════════════════════════════════════════════════
    def generate_auto_descriptions(self):
        p_type = (self.property_type or "Commercial Plot").replace("_", " ").title()
        area_str = f"{self.plot_area} sq.ft" if self.plot_area else "Prime Commercial Area"
       
        loc = self.locality or "Prime Commercial Zone"
        city_str = f", {self.city}" if self.city else ""

        # Summary
        summary = f"A strategic {area_str} {p_type} is available for resale at {loc}{city_str}. "
        if self.selling_price:
            summary += f"Listed at an attractive price of ₹{self.selling_price:,}. "
        if self.commercial_zone_type:
            summary += f"Zoned under {self.commercial_zone_type.replace('_', ' ').title()}. "
        summary += "Well-suited for commercial complexes, retail showrooms, warehouses, and long-term business investment."
        self.property_summary = summary

        # Detailed Description
        long_desc = f"<p>Secure a high-value commercial asset with this strategically situated <strong>{area_str} {p_type}</strong> located in <strong>{loc}{city_str}</strong>.</p>"

        long_desc += "<h3>Key Commercial Specifications:</h3><ul>"
        if self.plot_area:
            long_desc += f"<li><strong>Plot Area & Dimensions:</strong> Total area of {self.plot_area} sq.ft (Frontage: {self.plot_frontage or '—'} m x Depth: {self.plot_depth or '—'} m). Shape: {self.plot_shape or 'Regular'}.</li>"
        long_desc += f"<li><strong>Road Access & Visibility:</strong> Abuts a {self.road_width or 'Standard'} road with '{self.road_connectivity or 'Direct Access'}'. Visibility: {self.plot_visibility or 'Standard'}.</li>"
        if self.selling_price and self.plot_area and float(self.plot_area) > 0:
            psq = round(float(self.selling_price) / float(self.plot_area))
            long_desc += f"<li><strong>Valuation:</strong> Listed at ₹{self.selling_price:,} (~₹{psq:,}/sq.ft). Negotiable: {str(self.price_negotiable).upper()}.</li>"
        long_desc += f"<li><strong>Current Possession Status:</strong> Offered in '{self.current_possession_status or 'Vacant & Immediate Possession'}' condition.</li>"
        long_desc += "</ul>"

        long_desc += "<h3>Zoning, FSI & Approvals:</h3><ul>"
        long_desc += f"<li><strong>Land Use & Zone:</strong> Classified under Land Use '{self.land_use or 'Commercial'}' (Zone Type: {self.commercial_zone_type or 'As per norms'}).</li>"
        long_desc += f"<li><strong>FSI & Coverage:</strong> Permissible FSI: {self.permissible_fsi or 'As per municipal norms'}. Ground Coverage: {self.ground_coverage or 'As per bylaws'}.</li>"
        long_desc += f"<li><strong>Legal Status (NA & Layout):</strong> NA Status: {self.na_status or 'Converted'}. Layout Approval: {self.layout_approval_status or 'Approved'}.</li>"
        long_desc += "</ul>"

        long_desc += "<h3>Legal & Title Clearances:</h3><ul>"
        long_desc += f"<li><strong>Tenure & Documentation:</strong> {self.ownership_type or 'Freehold'} tenure. Primary Document: {self.ownership_document_type or 'Sale Deed'}.</li>"
        long_desc += f"<li><strong>Title Clarity:</strong> Title status is verified as '{self.title_clearance or 'Clear & Marketable'}'. RERA Status: {self.rera_status or 'Exempt/Applicable'}.</li>"
        long_desc += "</ul>"

        if self.amenities:
            long_desc += f"<h3>Commercial Infrastructure & Amenities:</h3><p>The property features business highlights including: <strong>{self.amenities}</strong>.</p>"

        long_desc += "<p>Contact us immediately to arrange a site visit or verify commercial property documents with our legal team.</p>"
        self.property_description = long_desc

    # ═══════════════════════════════════════════════════════════════════════
    #  SAVE OVERRIDE
    # ═══════════════════════════════════════════════════════════════════════
    def save(self, *args, **kwargs):
        area_lbl = f"{self.plot_area} sq.ft" if self.plot_area else ""
        p_type = (self.property_type or "Commercial Plot").replace("_", " ").title()
        loc = self.locality or ""
        city_name = f", {self.city}" if self.city else ""

        self.property_title = " ".join(filter(bool, [area_lbl, p_type, "for Sale in", loc + city_name]))[:255]
        self.generate_auto_descriptions()
        super().save(*args, **kwargs)
        self.generate_auto_faqs()

    # ═══════════════════════════════════════════════════════════════════════
    #  AUTO FAQ ENGINE (COMMERCIAL PLOT)
    # ═══════════════════════════════════════════════════════════════════════
    def generate_auto_faqs(self):
        if hasattr(self, 'faqs') and self.faqs.all():
            self.faqs.all().delete()

        faq_pool = []

        # 1. Plot Area & Dimensions
        if self.plot_area or self.property_type or self.plot_frontage or self.plot_depth:
            dimensions = ""
            if self.plot_frontage and self.plot_depth:
                dimensions = f" The plot measures approximately {self.plot_frontage} m frontage × {self.plot_depth} m depth."
            elif self.plot_frontage:
                dimensions = f" The available frontage is approximately {self.plot_frontage} m."
            elif self.plot_depth:
                dimensions = f" The available depth is approximately {self.plot_depth} m."

            plot_type = (self.property_type or "Commercial Plot").replace("_", " ").title()
            shape = f" The plot shape is {self.plot_shape}." if self.plot_shape else ""

            faq_pool.append({
                "q": "What is the plot area and specification of this commercial plot?",
                "a": f"This is a {plot_type} with a plot area of {self.plot_area or 'not specified'} sq.ft.{dimensions}{shape}"
            })

        # 2. Price & Brokerage
        if self.selling_price or self.plot_price_per_sqft:
            price_parts = []
            if self.selling_price:
                price_parts.append(f"The asking price is ₹{self.selling_price:,}.")
            if self.plot_price_per_sqft:
                price_parts.append(f"The listed rate is approximately ₹{self.plot_price_per_sqft:,} per sq.ft.")
            if self.price_negotiable:
                price_parts.append(f"Price negotiability is marked as '{self.price_negotiable}'.")
            if self.additional_charges:
                price_parts.append(f"Additional charges, if applicable, are '{self.additional_charges}'.")

            faq_pool.append({
                "q": "What is the price of this commercial plot?",
                "a": " ".join(price_parts)
            })

        # Brokerage FAQ
        if self.brokerage_percentage or self.manual_brokerage:
            label = self.get_brokerage_label() if hasattr(self, 'get_brokerage_label') else "Brokerage"
            value = self.get_brokerage_display_value() if hasattr(self, 'get_brokerage_display_value') else (self.manual_brokerage or self.brokerage_percentage)

            faq_pool.append({
                "q": "Is there any brokerage or service fee applicable to this plot?",
                "a": f"The applicable {label.lower()} for this property is {value}."
            })

        # 3. Zoning, FSI & Approvals
        zoning_parts = []
        if self.land_use:
            zoning_parts.append(f"Land use is classified as '{self.land_use}'.")
        if self.commercial_zone_type:
            zoning_parts.append(f"Commercial zone type is '{self.commercial_zone_type}'.")
        if self.na_status:
            zoning_parts.append(f"NA status is '{self.na_status}'.")
        if self.layout_approval_status:
            zoning_parts.append(f"Layout approval status is '{self.layout_approval_status}'.")
        if self.permissible_fsi:
            zoning_parts.append(f"Permissible FSI is {self.permissible_fsi}.")
        if self.ground_coverage:
            zoning_parts.append(f"Ground coverage is {self.ground_coverage}.")

        if zoning_parts:
            faq_pool.append({
                "q": "What are the zoning, FSI and approval details for this commercial plot?",
                "a": " ".join(zoning_parts)
            })

        # 4. Road Access & Commercial Features
        access_parts = []
        if self.road_connectivity:
            access_parts.append(f"Road connectivity is described as '{self.road_connectivity}'.")
        if self.road_width:
            access_parts.append(f"The road width is {self.road_width}.")
        if self.plot_visibility:
            access_parts.append(f"Plot visibility is '{self.plot_visibility}'.")
        if self.proposed_use:
            access_parts.append(f"Proposed commercial use: '{self.proposed_use}'.")
        if self.parking_availability:
            access_parts.append(f"Parking availability: '{self.parking_availability}'.")

        if access_parts:
            faq_pool.append({
                "q": "What are the road access, visibility and commercial features?",
                "a": " ".join(access_parts)
            })

        # 5. Legal, Title & Documents
        legal_parts = []
        if self.ownership_type:
            legal_parts.append(f"Ownership type is '{self.ownership_type}'.")
        if self.ownership_document_type:
            legal_parts.append(f"Ownership document type is '{self.ownership_document_type}'.")
        if self.rera_status:
            legal_parts.append(f"RERA status is '{self.rera_status}'.")
        if self.title_clearance:
            legal_parts.append(f"Title clearance status is '{self.title_clearance}'.")
        if self.property_encumbrance_status:
            legal_parts.append(f"Property encumbrance status is '{self.property_encumbrance_status}'.")
        if self.property_tax_status:
            legal_parts.append(f"Property tax status is '{self.property_tax_status}'.")
        if self.sanctioning_authority:
            legal_parts.append(f"Sanctioning authority: {self.sanctioning_authority}.")

        if legal_parts:
            faq_pool.append({
                "q": "What are the legal, title and approval details of this commercial plot?",
                "a": " ".join(legal_parts)
            })

        # 6. Location & Facilities
        location_parts = []
        location_name = " ".join(filter(bool, [self.locality, self.city, self.state]))
        if location_name:
            location_parts.append(f"The plot is located in {location_name}.")
        if self.property_landmark:
            location_parts.append(f"Nearby landmark: {self.property_landmark}.")
        if self.pincode:
            location_parts.append(f"The property PIN code is {self.pincode}.")
        if self.nearby_facilities:
            location_parts.append(f"Nearby facilities include: {self.nearby_facilities}.")
        if self.amenities:
            location_parts.append(f"Available amenities include: {self.amenities}.")

        if location_parts:
            faq_pool.append({
                "q": "Where is the commercial plot located and what facilities are nearby?",
                "a": " ".join(location_parts)
            })

        # 7. Possession & Financial Status
        investment_parts = []
        if self.current_possession_status:
            investment_parts.append(f"Current possession status is '{self.current_possession_status}'.")
        if self.property_loan_status:
            investment_parts.append(f"Property loan status is '{self.property_loan_status}'.")
        if self.financing_bank:
            investment_parts.append(f"Financing bank: {self.financing_bank}.")
        if self.outstanding_loan_amount:
            investment_parts.append(f"Outstanding loan amount is ₹{self.outstanding_loan_amount:,}.")

        if investment_parts:
            faq_pool.append({
                "q": "What is the possession and financial status of this commercial plot?",
                "a": " ".join(investment_parts)
            })

        # Create FAQ records using CommercialPlotResaleFAQ (or generic model if applicable)
        for item in faq_pool:
            if hasattr(self, 'faqs'):
                self.faqs.create(
                    question=item["q"],
                    answer=item["a"]
                )

    def __str__(self):
        return f"{self.property_title or 'Commercial Plot Resale'} ({self.id})"


# ==========================================================
# INDUSTRIAL PLOT RESALE — IMAGE MODEL (Category-wise, like CommercialPlotResaleImage)
# ==========================================================

class CommercialPlotResaleImage(models.Model):

    CATEGORY_CHOICES = [
        ('front_view',       'Front Elevation & Road Frontage'),
        ('full_plot',        'Full Plot / Land View'),
        ('road_facing',      'Main Road, Highway & Traffic View'),
        ('entrance_access',  'Approach Road & Heavy Vehicle Access'),
        ('boundary',         'Plot Boundary & Fencing'),
        ('layout_plan',      'Master Layout & Survey Plan'),
        ('surroundings',     'Commercial Vicinity & Neighboring Businesses'),
        ('amenities_infra',  'Power, Transformer, Water & Utilities'),
    ]

    property = models.ForeignKey(
        'CommercialPlotResaleProperty',
        on_delete=models.CASCADE,
        related_name="images"
    )
    image = models.ImageField(upload_to="commercial_plot/images/")
    category = models.CharField(max_length=30, choices=CATEGORY_CHOICES, default='full_plot')
    sequence_order = models.PositiveIntegerField(default=0)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["category", "sequence_order", "uploaded_at"]

    def __str__(self):
        return f"{self.property_id} - {self.get_category_display()} ({self.sequence_order})"


# ==========================================================
# INDUSTRIAL PLOT RESALE — VIDEO MODEL (same 3-source pattern as RentalResidentialVideo)
# ==========================================================

class CommercialPlotResaleVideo(models.Model):
    SOURCE_CHOICES = [
        ('uploaded',    'Manually Uploaded'),
        ('auto',        'Auto Generated Slideshow'),
        ('rm_assisted', 'RM Assisted Link'),
    ]
    property = models.ForeignKey(
        'CommercialPlotResaleProperty',
        on_delete=models.CASCADE,
        related_name="video"
    )
    video = models.FileField(upload_to="commercial_plot/videos/", null=True, blank=True)
    video_url = models.URLField(null=True, blank=True)
    source = models.CharField(max_length=15, choices=SOURCE_CHOICES, default='auto')
    video_status = models.CharField(max_length=255, blank=True, null=True,default="Pending")
    created_at = models.DateTimeField(auto_now_add=True)

    def youtube_thumbnail(self):
        import re
        if self.source == 'rm_assisted' and self.video_url:
            match = re.search(
                r'(?:youtube\.com/watch\?v=|youtu\.be/|youtube\.com/shorts/)([A-Za-z0-9_-]{6,})',
                self.video_url
            )
            if match:
                return f"https://img.youtube.com/vi/{match.group(1)}/hqdefault.jpg"
        return None

    def get_platform_type(self):
        if not self.video_url:
            return 'unknown'
        url = self.video_url.lower()
        if 'youtube.com' in url or 'youtu.be' in url:
            return 'youtube'
        elif 'instagram.com' in url or 'instagr.am' in url:
            return 'instagram'
        elif 'facebook.com' in url or 'fb.watch' in url:
            return 'facebook'
        elif 'vimeo.com' in url:
            return 'vimeo'
        elif 'drive.google.com' in url:
            return 'gdrive'
        return 'external'




class CommercialPlotResaleFAQ(models.Model):
    property = models.ForeignKey(CommercialPlotResaleProperty, on_delete=models.CASCADE, related_name="faqs")
    question = models.CharField(max_length=255)
    answer = models.TextField()


class CommercialPlotResaleActivityLog(models.Model):
    ACTION_CHOICES = [
        ("CREATE", "Property Entry Created"),
        ("UPDATE", "Record Update Action"),
        ("DELETE", "Deletion / Purge Record"),
    ]
    timestamp = models.DateTimeField(auto_now_add=True)
    user_identity = models.CharField(max_length=255, null=True, blank=True)
    user_role = models.CharField(max_length=100, null=True, blank=True)
    action_type = models.CharField(max_length=50, choices=ACTION_CHOICES)
    property_id = models.CharField(max_length=100, null=True, blank=True)
    action_payload = models.TextField(null=True, blank=True)
    status = models.CharField(max_length=20, default="SUCCESS")

    class Meta:
        ordering = ["-timestamp"]


############### Modal End for commercial resale plot ##############################


##################END MODEL SECTION AGRICULTURAL RESALE LISTING################


################## START MODEL SECTION Industrial Plot RESALE LISTING################






def generate_industrial_plot_id():
    return f"EFIPR-{uuid.uuid4().hex[:8].upper()}"

class IndustrialPlotResaleProperty(models.Model):
    id = models.CharField(
        max_length=20,
        primary_key=True,
        default=generate_industrial_plot_id,
        editable=False,
    )

    # ── STEP 1: LISTED BY ──────────────────────────────────────────────────
    listing_type = models.CharField(max_length=100, blank=True, null=True)
    category = models.CharField(max_length=100, blank=True, null=True)
    sub_category = models.CharField(max_length=100, blank=True, null=True)

    listed_by_type = models.CharField(max_length=100, blank=True, null=True)
    assigned_to = models.CharField(max_length=50, blank=True, null=True)     # "id-role" value from dropdown, only if "other"
  
    listed_by_id = models.CharField(max_length=150, blank=True, null=True)
    listed_by_name = models.CharField(max_length=150, blank=True, null=True)
    listed_by_email = models.CharField(max_length=150, blank=True, null=True)
    listed_by_contact = models.CharField(max_length=20, blank=True, null=True)
    listed_by_role = models.CharField(max_length=100, blank=True, null=True)

    # ── DUPLICATE DETECTION ─────────────────────────────────────────────────
    property_unique_key = models.CharField(max_length=255, blank=True, null=True, db_index=True)
    duplicate_count = models.PositiveIntegerField(default=0)
    duplicate_group_id = models.CharField(max_length=255, blank=True, null=True, db_index=True)   # <-- drives the duplicate label

    # ── STEP 1: BASIC INFORMATION & ZONE DETAILS ───────────────────────────
    property_title = models.CharField(max_length=255, blank=True, null=True)
   
    # INTERNAL ONLY — never shown publicly in auto titles, descriptions, or FAQs
    property_no = models.CharField(max_length=150, blank=True, null=True)

    plot_area = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)  # sq.m
    property_type = models.CharField(max_length=100, blank=True, null=True)
    land_use = models.CharField(max_length=100, blank=True, null=True)
    industrial_zone_type = models.CharField(max_length=100, blank=True, null=True)
    industrial_estate_name = models.CharField(max_length=200, blank=True, null=True)
    na_status = models.CharField(max_length=100, blank=True, null=True)
    layout_approval_status = models.CharField(max_length=100, blank=True, null=True)
    industrial_fsi = models.CharField(max_length=50, blank=True, null=True)

    # ── STEP 1: SPECIFICATIONS & INFRASTRUCTURE ────────────────────────────
    plot_frontage = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)  # metres
    plot_depth = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)     # metres
    plot_shape = models.CharField(max_length=100, blank=True, null=True)
    plot_road_facing = models.CharField(max_length=100, blank=True, null=True)
    road_width = models.CharField(max_length=50, blank=True, null=True)
    corner_plot = models.CharField(max_length=20, default="no")

    power_supply = models.CharField(max_length=100, blank=True, null=True)
    power_load_kva = models.IntegerField(blank=True, null=True)
    industrial_water_supply = models.CharField(max_length=100, blank=True, null=True)
    effluent_treatment = models.CharField(max_length=100, blank=True, null=True)
    industry_type_permissible = models.CharField(max_length=150, blank=True, null=True)
    plot_fencing = models.CharField(max_length=100, blank=True, null=True)
    loading_dock = models.CharField(max_length=100, blank=True, null=True)
    current_possession_status = models.CharField(max_length=100, blank=True, null=True)

    # ── STEP 2: PRICING & BROKERAGE ────────────────────────────────────────
    selling_price = models.BigIntegerField(blank=True, null=True)
    price_per_sqft = models.BigIntegerField(blank=True, null=True)
    price_negotiable = models.CharField(max_length=20, default="no")
    additional_charges = models.CharField(max_length=100, blank=True, null=True)
    brokerage_percentage = models.CharField(max_length=100, blank=True, null=True)
    manual_brokerage = models.CharField(max_length=100, blank=True, null=True)

    # ── STEP 2: LEGAL, TITLE & AUTHORITY COMPLIANCE ────────────────────────
    ownership_type = models.CharField(max_length=100, blank=True, null=True)
    ownership_document_type = models.CharField(max_length=150, blank=True, null=True)
    other_document_type = models.CharField(max_length=150, blank=True, null=True)
    midc_allotment = models.CharField(max_length=100, blank=True, null=True)
    midc_transfer_noc = models.CharField(max_length=100, blank=True, null=True)
    environmental_clearance = models.CharField(max_length=100, blank=True, null=True)
    rera_status = models.CharField(max_length=100, blank=True, null=True)
    title_clearance = models.CharField(max_length=100, blank=True, null=True)
    property_encumbrance_status = models.CharField(max_length=100, blank=True, null=True)

    property_tax_status = models.CharField(max_length=100, blank=True, null=True)
    outstanding_tax_amount = models.BigIntegerField(blank=True, null=True)
    pending_since = models.DateField(blank=True, null=True)
    property_loan_status = models.CharField(max_length=100, blank=True, null=True)
    financing_bank = models.CharField(max_length=150, blank=True, null=True)
    outstanding_loan_amount = models.BigIntegerField(blank=True, null=True)
    sanctioning_authority = models.TextField(blank=True, null=True)

    # ── STEP 3: AMENITIES & LOCATION DETAILS ───────────────────────────────
    amenities = models.TextField(blank=True, null=True)
    nearby_facilities = models.TextField(blank=True, null=True)
    user_description = models.TextField(blank=True, null=True)
    property_summary = models.TextField(blank=True, null=True)
    property_description = models.TextField(blank=True, null=True)

    state = models.CharField(max_length=100, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    locality = models.CharField(max_length=200, blank=True, null=True)
    property_landmark = models.CharField(max_length=200, blank=True, null=True)
    pincode = models.CharField(max_length=20, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    google_maps_link = models.URLField(max_length=500, blank=True, null=True)
    latitude = models.CharField(max_length=50, blank=True, null=True)
    longitude = models.CharField(max_length=50, blank=True, null=True)

    # ── STEP 4: MEDIA & STATUS ─────────────────────────────────────────────
    encumbrance_cert = models.FileField(upload_to="industrial_plot/docs/", blank=True, null=True)
    layout_plan = models.FileField(upload_to="industrial_plot/docs/", blank=True, null=True)
    social_video = models.FileField(upload_to="industrial_plot/videos/", blank=True, null=True)
    listed_elsewhere = models.CharField(max_length=10, default="No")
    portal_name = models.CharField(max_length=100, blank=True, null=True)

    uploaded_by_name = models.CharField(max_length=150, blank=True, null=True)
    uploaded_by_email = models.CharField(max_length=150, blank=True, null=True)
    uploaded_by_contact = models.CharField(max_length=50, blank=True, null=True)
    uploaded_by_role = models.CharField(max_length=100, blank=True, null=True)
    upload_file_name = models.CharField(max_length=255, blank=True, null=True)
    upload_file = models.FileField(upload_to='industrial_resaleplot_property_uploads/files/', blank=True, null=True)

    is_deleted = models.BooleanField(default=False)
    
    is_duplicate = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(null=True, blank=True)
    deleted_by = models.CharField(max_length=150, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    listing_status = models.CharField(max_length=150, blank=True, null=True)
    approval_status = models.CharField(max_length=150, blank=True, null=True)

    # ═══════════════════════════════════════════════════════════════════════
    #  INDUSTRIAL RESALE BROKERAGE LOGIC
    # ═══════════════════════════════════════════════════════════════════════
    BROKERAGE_LABEL_MAP = {
        "admin": "EstateFlow Service Fee",
        "relationship manager": "Buyer Service Fee",
        "landlord": "Buyer Service Fee",
        "owner": "Buyer Service Fee",
        "seller": "Buyer Service Fee",
        "agent": "Brokerage",
        "agency/builder": "Brokerage / Service Fee",
        "builder": "Brokerage / Service Fee",
    }

    def get_brokerage_label(self):
        role = (self.listed_by_role or "").strip().lower()
        return self.BROKERAGE_LABEL_MAP.get(role, "Brokerage")

    def get_brokerage_display_value(self):
        if self.brokerage_percentage == "Fixed Amount":
            return self.manual_brokerage or "-"
        return self.brokerage_percentage or "-"

    # ═══════════════════════════════════════════════════════════════════════
    #  AUTO DESCRIPTIONS ENGINE
    # ═══════════════════════════════════════════════════════════════════════
    # ── SMART AREA FORMATTER (Keeps decimals if present, strips zeros if whole number) ──
    # ── PRECISE 2-DECIMAL AREA FORMATTER ──
    def _clean_area(self):
        if self.plot_area is None:
            return ""
        try:
            # Converts the value to a float and formats it strictly with 2 decimal places
            # e.g., 1500 -> 1500.00, 1400.00 -> 1400.00, 1455.90 -> 1455.90
            f = float(self.plot_area)
            return f"{f:.2f}"
        except (TypeError, ValueError):
            return str(self.plot_area)

    # ═══════════════════════════════════════════════════════════════════════
    #  AUTO DESCRIPTIONS ENGINE
    # ═══════════════════════════════════════════════════════════════════════
    def generate_auto_descriptions(self):
        p_type = (self.property_type or "Industrial Plot").replace("_", " ").title()
        area_clean = self._clean_area()
        area_str = f"{area_clean} sq.m" if area_clean else "Prime Area"
        estate = f"in {self.industrial_estate_name}" if self.industrial_estate_name else ""
        loc = self.locality or "Industrial Zone"
        city_str = f", {self.city}" if self.city else ""

        # Summary
        summary = f"A strategic {area_str} {p_type} is available for resale {estate} at {loc}{city_str}. "
        if self.selling_price:
            summary += f"Listed at an attractive price of ₹{self.selling_price:,}. "
        if self.power_load_kva:
            summary += f"Equipped with {self.power_load_kva} KVA industrial power supply infrastructure. "
        summary += "Well-suited for manufacturing units, logistics warehousing, and processing industries."
        self.property_summary = summary

        # Detailed Description
        long_desc = f"<p>Expand your industrial footprint with this strategically situated <strong>{area_str} {p_type}</strong> located {estate} in <strong>{loc}{city_str}</strong>.</p>"

        long_desc += "<h3>Key Site Specifications:</h3><ul>"

        if self.plot_area:
            f_val = f"{self.plot_frontage:.2f}" if self.plot_frontage else "—"
            d_val = f"{self.plot_depth:.2f}" if self.plot_depth else "—"
            long_desc += f"<li><strong>Plot Area & Dimensions:</strong> Total area of {area_clean} sq.m (Frontage: {f_val}m x Depth: {d_val}m). Shape: {self.plot_shape or 'Regular'}.</li>"
        
        long_desc += f"<li><strong>Road Access:</strong> Abuts a {self.road_width or 'Standard'} road with '{self.plot_road_facing or 'Direct Road Access'}'. Corner plot: {self.corner_plot.upper()}.</li>"
        
        if self.selling_price and self.plot_area:
            try:
                psq = round(float(self.selling_price) / float(self.plot_area)) if float(self.plot_area) > 0 else 0
                long_desc += f"<li><strong>Commercial Valuation:</strong> Listed at ₹{self.selling_price:,} (~₹{psq:,}/sq.m). Negotiable: {self.price_negotiable.upper()}.</li>"
            except (TypeError, ValueError, ZeroDivisionError):
                pass

        long_desc += f"<li><strong>Current Site Status:</strong> Offered in '{self.current_possession_status or 'Vacant & Ready'}' condition.</li>"
        long_desc += "</ul>"

        long_desc += "<h3>Utility Infrastructure & Zoning:</h3><ul>"
        long_desc += f"<li><strong>Power Supply:</strong> Configured with '{self.power_supply or 'Standard Industrial Power'}' (Sanctioned Load: {self.power_load_kva or 'As per norms'} KVA).</li>"
        long_desc += f"<li><strong>Water & Drainage:</strong> Water Source: {self.industrial_water_supply or 'MIDC Piped Water'}. Effluent/Drainage: {self.effluent_treatment or 'Standard Layout'}.</li>"
        long_desc += f"<li><strong>Permissible Operations:</strong> Sanctioned for '{self.industry_type_permissible or 'Any Industrial Activity'}'. FSI: {self.industrial_fsi or '1.0'}.</li>"
        long_desc += "</ul>"

        long_desc += "<h3>Legal & Authority Clearances:</h3><ul>"
        long_desc += f"<li><strong>Tenure & Compliance:</strong> {self.ownership_type or 'Leasehold/Freehold'} tenure. MIDC/Authority Transfer NOC status: {self.midc_transfer_noc or 'Clear'}.</li>"
        long_desc += f"<li><strong>Title & Encumbrances:</strong> Title status is verified as '{self.title_clearance or 'Clear & Marketable'}'. Encumbrance status: {self.property_encumbrance_status or 'Nil'}.</li>"
        long_desc += "</ul>"

        if self.amenities or self.nearby_facilities:
            long_desc += "<h3>Estate Infrastructure & Location Advantages:</h3><p>The site offers superior logistics support and strategic advantages:</p><ul>"
            if self.amenities:
                long_desc += f"<li><strong>On-Site Amenities:</strong> {self.amenities}.</li>"
            if self.nearby_facilities:
                long_desc += f"<li><strong>Nearby Facilities & Connectivity:</strong> {self.nearby_facilities}.</li>"
            long_desc += "</ul>"

        long_desc += "<p>Contact us immediately to arrange a technical site inspection or verify MIDC / Authority documentation.</p>"
        self.property_description = long_desc

    # ═══════════════════════════════════════════════════════════════════════
    #  SAVE OVERRIDE
    # ═══════════════════════════════════════════════════════════════════════
    # ═══════════════════════════════════════════════════════════════════════
    #  SAVE OVERRIDE
    # ═══════════════════════════════════════════════════════════════════════
    def save(self, *args, **kwargs):
        # ── AUTO-CALCULATE PRICE PER SQ.M / SQ.FT ──
        if self.selling_price and self.plot_area:
            try:
                area_val = float(self.plot_area)
                if area_val > 0:
                    self.price_per_sqft = round(float(self.selling_price) / area_val)
                else:
                    self.price_per_sqft = None
            except (TypeError, ValueError, ZeroDivisionError):
                self.price_per_sqft = None
        else:
            self.price_per_sqft = None

        area_clean = self._clean_area()
        area_lbl = f"{area_clean} sq.m" if area_clean else ""
        p_type = (self.property_type or "Industrial Plot").replace("_", " ").title()
        loc = self.locality or ""
        city_name = f", {self.city}" if self.city else ""

        # Generates clean title (e.g., "1498 sq.m It Park Plot for Sale in ...")
        self.property_title = " ".join(filter(bool, [area_lbl, p_type, "for Sale in", loc + city_name]))[:255]
        
        # Forces regeneration of summaries and descriptions with the correct formatting on every save/edit
        self.generate_auto_descriptions()

        # >>> BUILD UNIQUE KEY ONLY ON FIRST CREATE <<<
        if self._state.adding:
            key_source = f"{self.address}|{self.locality}|{self.city}|{self.plot_area}|{self.property_no}"
            self.property_unique_key = key_source.strip().lower().replace(" ", "")

        super().save(*args, **kwargs)

        # >>> RECALCULATE DUPLICATE GROUP FROM ACTUAL DB STATE (idempotent) <<<
        if self.property_unique_key:
            group_qs = IndustrialPlotResaleProperty.objects.filter(
                property_unique_key=self.property_unique_key,
                is_deleted=False,
            )
            total = group_qs.count()

            if total > 1:
                original_id = group_qs.order_by("created_at").first().pk
                group_qs.update(
                    duplicate_count=total,
                    duplicate_group_id=original_id,
                    is_duplicate=True,
                )
            else:
                group_qs.update(
                    duplicate_count=1,
                    duplicate_group_id=None,
                    is_duplicate=False,
                )

        self.generate_auto_faqs()

    # ═══════════════════════════════════════════════════════════════════════
    #  AUTO FAQ ENGINE (Guaranteed 7 FAQs)
    # ═══════════════════════════════════════════════════════════════════════
    def generate_auto_faqs(self):
          # Ensure model is imported here if not at top

        self.faqs.all().delete()
        faq_pool = []

        # FAQ 1: Pricing
        if self.selling_price and self.plot_area:
            psq = round(float(self.selling_price) / float(self.plot_area)) if float(self.plot_area) > 0 else 0
            faq_pool.append({
                "q": "What is the total sale value and rate per square metre for this industrial plot?",
                "a": f"The total asking price is ₹{self.selling_price:,}, which translates to approximately ₹{psq:,} per sq.m. Price negotiability is indicated as: '{self.price_negotiable.upper()}'.",
            })
        else:
            faq_pool.append({
                "q": "Is the pricing for this industrial plot finalized?",
                "a": "The pricing details are currently available upon request. Please contact the listing manager for exact commercial valuations.",
            })

        # FAQ 2: Brokerage
        label = self.get_brokerage_label()
        val = self.get_brokerage_display_value()
        faq_pool.append({
            "q": f"Is there a {label.lower()} applicable on this industrial plot purchase?",
            "a": f"Yes, the applicable {label.lower()} for this property transaction is: {val}.",
        })

        # FAQ 3: Utilities
        faq_pool.append({
            "q": "What industrial power load and utility infrastructure are available on site?",
            "a": f"The plot features '{self.power_supply or 'Industrial Power Grid'}' with a sanctioned capacity of {self.power_load_kva or 'Standard'} KVA. Water provisioning is handled via '{self.industrial_water_supply or 'MIDC Piped Supply'}', and effluent treatment options include '{self.effluent_treatment or 'Standard Drainage'}'.",
        })

        # FAQ 4: Legal / Title
        faq_pool.append({
            "q": "What is the MIDC / Authority transfer NOC and title clearance status?",
            "a": f"The property ownership tenure is classified as '{self.ownership_type or 'Industrial Lease'}'. MIDC / Authority transfer NOC status is '{self.midc_transfer_noc or 'Clear'}', and the legal title is verified as '{self.title_clearance or 'Clear & Marketable'}'.",
        })

        # FAQ 5: Approvals / Permissibility
        faq_pool.append({
            "q": "What types of industries are permissible to operate on this plot?",
            "a": f"This zone is primarily sanctioned for '{self.industry_type_permissible or 'General Industrial Activity'}'. The current layout approval status is recorded as '{self.layout_approval_status or 'Approved'}' with an allowable FSI of {self.industrial_fsi or '1.0'}.",
        })

        # FAQ 6: Dimensions & Access
        faq_pool.append({
            "q": "What are the physical dimensions and road access specifications of the plot?",
            "a": f"The plot is '{self.plot_shape or 'Regular'}' in shape. It benefits from a '{self.plot_road_facing or 'Direct'}' facing towards a {self.road_width or 'Standard'} wide approach road. Corner plot advantage: {self.corner_plot.upper()}.",
        })

        # FAQ 7: Surroundings & Location
        faq_pool.append({
            "q": "What are the key location advantages and nearby facilities surrounding the plot?",
            "a": f"Located in {self.locality or 'an established industrial hub'}, the site boasts proximity to essential logistics infrastructure. Specifically, nearby facilities include: {self.nearby_facilities or 'Strategic transport nodes and local commercial support hubs'}.",
        })

        for item in faq_pool:
            IndustrialPlotResaleFAQ.objects.create(property=self, question=item["q"], answer=item["a"])

    def __str__(self):
        return f"{self.property_title or 'Industrial Plot Resale'} ({self.id})"


# ── CHILD MODELS ───────────────────────────────────────────────────────────






# ==========================================================
# INDUSTRIAL PLOT RESALE — IMAGE MODEL (Category-wise, like RentalResidentialImage)
# ==========================================================

class IndustrialPlotResaleImage(models.Model):
    CATEGORY_CHOICES = [
        ('full_plot',          'Full Plot View'),
        ('main_entrance',      'Main Entrance'),
        ('boundary_fencing',   'Boundary / Fencing'),
        ('road_facing',        'Road Facing View'),
        ('approach_road',      'Approach Road'),
        ('truck_access',       'Truck Access'),
        ('industrial_estate',  'Industrial Estate / Surroundings'),
        ('electricity_infra',  'Electricity / Power Infrastructure'),
        ('water_infra',        'Water Infrastructure'),
        ('aerial_drone',       'Aerial / Drone View'),
        ('layout_site_plan',   'Plot Layout / Site Plan'),
    ]

    property = models.ForeignKey(
        'IndustrialPlotResaleProperty',
        on_delete=models.CASCADE,
        related_name="images"
    )
    image = models.ImageField(upload_to="industrial_plot/images/")
    category = models.CharField(max_length=25, choices=CATEGORY_CHOICES, default='full_plot')
    sequence_order = models.PositiveIntegerField(default=0)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["category", "sequence_order", "uploaded_at"]

    def __str__(self):
        return f"{self.property_id} - {self.get_category_display()} ({self.sequence_order})"


# ==========================================================
# INDUSTRIAL PLOT RESALE — VIDEO MODEL (same 3-source pattern as RentalResidentialVideo)
# ==========================================================

class IndustrialPlotResaleVideo(models.Model):
    SOURCE_CHOICES = [
        ('uploaded',    'Manually Uploaded'),
        ('auto',        'Auto Generated Slideshow'),
        ('rm_assisted', 'RM Assisted Link'),
    ]
    property = models.ForeignKey(
        'IndustrialPlotResaleProperty',
        on_delete=models.CASCADE,
        related_name="video"
    )
    video = models.FileField(upload_to="industrial_plot/videos/", null=True, blank=True)
    video_url = models.URLField(null=True, blank=True)
    source = models.CharField(max_length=15, choices=SOURCE_CHOICES, default='auto')
    created_at = models.DateTimeField(auto_now_add=True)

    def youtube_thumbnail(self):
        import re
        if self.source == 'rm_assisted' and self.video_url:
            match = re.search(
                r'(?:youtube\.com/watch\?v=|youtu\.be/|youtube\.com/shorts/)([A-Za-z0-9_-]{6,})',
                self.video_url
            )
            if match:
                return f"https://img.youtube.com/vi/{match.group(1)}/hqdefault.jpg"
        return None

    def get_platform_type(self):
        if not self.video_url:
            return 'unknown'
        url = self.video_url.lower()
        if 'youtube.com' in url or 'youtu.be' in url:
            return 'youtube'
        elif 'instagram.com' in url or 'instagr.am' in url:
            return 'instagram'
        elif 'facebook.com' in url or 'fb.watch' in url:
            return 'facebook'
        elif 'vimeo.com' in url:
            return 'vimeo'
        elif 'drive.google.com' in url:
            return 'gdrive'
        return 'external'




class IndustrialPlotResaleFAQ(models.Model):
    property = models.ForeignKey(IndustrialPlotResaleProperty, on_delete=models.CASCADE, related_name="faqs")
    question = models.CharField(max_length=255)
    answer = models.TextField()


class IndustrialPlotResaleActivityLog(models.Model):
    ACTION_CHOICES = [
        ("SEARCH", "Manual Query Search"),
        ("CREATE", "Property Entry Created"),
        ("UPDATE", "Record Update Action"),
        ("DELETE", "Deletion / Purge Record"),
        ("EXCEL_IMPORT", "Excel Sheet Import Data"),
    ]

    timestamp = models.DateTimeField(auto_now_add=True)
    user_identity = models.CharField(max_length=255, null=True, blank=True)
    user_role = models.CharField(max_length=100, null=True, blank=True)
    action_type = models.CharField(max_length=50, choices=ACTION_CHOICES)
    property_id = models.CharField(max_length=100, null=True, blank=True)
    targeted_fields = models.CharField(max_length=255, null=True, blank=True)
    associated_file = models.CharField(max_length=255, null=True, blank=True)
    action_payload = models.TextField(null=True, blank=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    status = models.CharField(max_length=20, default="SUCCESS")

    class Meta:
        ordering = ["-timestamp"]




################## END MODEL SECTION Industrial Plot RESALE LISTING################



################## START MODEL SECTION Agricultural Plot RESALE LISTING################






def generate_agricultural_plot_id():
    return f"EFAPR-{uuid.uuid4().hex[:8].upper()}"


class AgriculturalPlotResaleProperty(models.Model):
    id = models.CharField(
        max_length=20,
        primary_key=True,
        default=generate_agricultural_plot_id,
        editable=False,
    )

    # ── STEP 1: LISTED BY ──────────────────────────────────────────────────
    listing_type = models.CharField(max_length=100, blank=True, null=True)
    category = models.CharField(max_length=100, blank=True, null=True)
    sub_category = models.CharField(max_length=100, blank=True, null=True)

    listed_by_type = models.CharField(max_length=100, blank=True, null=True)
    assigned_to = models.CharField(max_length=50, blank=True, null=True)

    listed_by_id = models.CharField(max_length=150, blank=True, null=True)
    listed_by_name = models.CharField(max_length=150, blank=True, null=True)
    listed_by_email = models.CharField(max_length=150, blank=True, null=True)
    listed_by_contact = models.CharField(max_length=20, blank=True, null=True)
    listed_by_role = models.CharField(max_length=100, blank=True, null=True)

    # ── DUPLICATE DETECTION ─────────────────────────────────────────────────
    property_unique_key = models.CharField(max_length=255, blank=True, null=True, db_index=True)
    duplicate_count = models.PositiveIntegerField(default=0)
    duplicate_group_id = models.CharField(max_length=255, blank=True, null=True, db_index=True)
    is_duplicate = models.BooleanField(default=False)

    # ── STEP 1: BASIC INFORMATION & REVENUE CLASSIFICATION ─────────────────
    property_title = models.CharField(max_length=255, blank=True, null=True)
    plot_title = models.CharField(max_length=100, default="agricultural_plot")

    # INTERNAL ONLY — Gat / Gut / Khasra / Survey Number (never shown publicly)
    property_no = models.CharField(max_length=150, blank=True, null=True)

    plot_area = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    agr_area_unit = models.CharField(max_length=50, default="acre")
    property_type = models.CharField(max_length=100, blank=True, null=True)
    land_use = models.CharField(max_length=100, blank=True, null=True)
    na_status = models.CharField(max_length=100, blank=True, null=True)
    layout_approval_status = models.CharField(max_length=100, blank=True, null=True)

    # ── STEP 1: SPECIFICATIONS & AGRICULTURAL DETAILS ──────────────────────
    plot_frontage = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    plot_depth = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    plot_shape = models.CharField(max_length=100, blank=True, null=True)
    plot_road_facing = models.CharField(max_length=100, blank=True, null=True)
    road_width = models.CharField(max_length=50, blank=True, null=True)
    corner_plot = models.CharField(max_length=20, default="no")

    soil_type = models.CharField(max_length=100, blank=True, null=True)
    current_crop = models.CharField(max_length=100, blank=True, null=True)
    irrigation_source = models.CharField(max_length=100, blank=True, null=True)
    agr_electricity = models.CharField(max_length=100, blank=True, null=True)
    highway_distance = models.CharField(max_length=100, blank=True, null=True)
    land_topography = models.CharField(max_length=100, blank=True, null=True)
    govt_scheme = models.CharField(max_length=100, blank=True, null=True)
    plot_fencing = models.CharField(max_length=100, blank=True, null=True)
    current_possession_status = models.CharField(max_length=100, blank=True, null=True)

    # ── STEP 2: PRICING & BROKERAGE ────────────────────────────────────────
    selling_price = models.BigIntegerField(blank=True, null=True)
    price_per_unit = models.BigIntegerField(blank=True, null=True)  # auto: selling_price / plot_area, label = "Rate per <unit>"
    price_negotiable = models.CharField(max_length=20, default="no")
    additional_charges = models.CharField(max_length=100, blank=True, null=True)
    brokerage_percentage = models.CharField(max_length=100, blank=True, null=True)
    manual_brokerage = models.CharField(max_length=100, blank=True, null=True)

    # ── STEP 2: LEGAL, REVENUE COMPLIANCE & TITLE ──────────────────────────
    ownership_type = models.CharField(max_length=100, blank=True, null=True)
    ownership_document_type = models.CharField(max_length=150, blank=True, null=True)
    other_document_type = models.CharField(max_length=150, blank=True, null=True)
    rera_status = models.CharField(max_length=100, blank=True, null=True)
    title_clearance = models.CharField(max_length=100, blank=True, null=True)
    property_encumbrance_status = models.CharField(max_length=100, blank=True, null=True)

    satbara_available = models.CharField(max_length=50, blank=True, null=True)
    khate_utara = models.CharField(max_length=50, blank=True, null=True)
    section63_clearance = models.CharField(max_length=100, blank=True, null=True)

    property_tax_status = models.CharField(max_length=100, blank=True, null=True)
    outstanding_tax_amount = models.BigIntegerField(blank=True, null=True)
    pending_since = models.DateField(blank=True, null=True)
    property_loan_status = models.CharField(max_length=100, blank=True, null=True)
    financing_bank = models.CharField(max_length=150, blank=True, null=True)
    outstanding_loan_amount = models.BigIntegerField(blank=True, null=True)
    sanctioning_authority = models.TextField(blank=True, null=True)

    # ── STEP 3: AMENITIES & LOCATION DETAILS ───────────────────────────────
    amenities = models.TextField(blank=True, null=True)
    nearby_facilities = models.TextField(blank=True, null=True)
    user_description = models.TextField(blank=True, null=True)
    property_summary = models.TextField(blank=True, null=True)
    property_description = models.TextField(blank=True, null=True)

    state = models.CharField(max_length=100, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    locality = models.CharField(max_length=200, blank=True, null=True)  # Village / Mouza / Taluka
    property_landmark = models.CharField(max_length=200, blank=True, null=True)
    pincode = models.CharField(max_length=20, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    google_maps_link = models.URLField(max_length=500, blank=True, null=True)
    latitude = models.CharField(max_length=50, blank=True, null=True)
    longitude = models.CharField(max_length=50, blank=True, null=True)

    # ── STEP 4: MEDIA & STATUS ─────────────────────────────────────────────
    encumbrance_cert = models.FileField(upload_to="agricultural_plot/docs/", blank=True, null=True)  # 7/12 & 8A
    layout_plan = models.FileField(upload_to="agricultural_plot/docs/", blank=True, null=True)       # Land Map
    social_video = models.FileField(upload_to="agricultural_plot/videos/", blank=True, null=True)
    listed_elsewhere = models.CharField(max_length=10, default="No")
    portal_name = models.CharField(max_length=100, blank=True, null=True)

    uploaded_by_name = models.CharField(max_length=150, blank=True, null=True)
    uploaded_by_email = models.CharField(max_length=150, blank=True, null=True)
    uploaded_by_contact = models.CharField(max_length=50, blank=True, null=True)
    uploaded_by_role = models.CharField(max_length=100, blank=True, null=True)
    upload_file_name = models.CharField(max_length=255, blank=True, null=True)
    upload_file = models.FileField(upload_to='agricultural_resaleplot_property_uploads/files/', blank=True, null=True)

    is_deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(null=True, blank=True)
    deleted_by = models.CharField(max_length=150, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    listing_status = models.CharField(max_length=150, blank=True, null=True)
    approval_status = models.CharField(max_length=150, blank=True, null=True)

    # ═══════════════════════════════════════════════════════════════════════
    #  AGRICULTURAL RESALE BROKERAGE LOGIC
    # ═══════════════════════════════════════════════════════════════════════
    BROKERAGE_LABEL_MAP = {
        "admin": "EstateFlow Service Fee",
        "relationship manager": "Buyer Service Fee",
        "landlord": "Buyer Service Fee",
        "owner": "Buyer Service Fee",
        "seller": "Buyer Service Fee",
        "agent": "Brokerage",
        "agency/builder": "Brokerage / Service Fee",
        "builder": "Brokerage / Service Fee",
    }

    def get_brokerage_label(self):
        role = (self.listed_by_role or "").strip().lower()
        return self.BROKERAGE_LABEL_MAP.get(role, "Brokerage")

    def get_brokerage_display_value(self):
        if self.brokerage_percentage == "Fixed Amount":
            return self.manual_brokerage or "-"
        return self.brokerage_percentage or "-"

    # ═══════════════════════════════════════════════════════════════════════
    #  RATE PER UNIT LABEL HELPER (e.g. "Rate per Hectare", "Rate per Acre")
    # ═══════════════════════════════════════════════════════════════════════
    def get_rate_label(self):
        unit = (self.agr_area_unit or "acre").strip()
        return f"Rate per {unit.capitalize()}"

    def _clean_area(self):
        if self.plot_area is None:
            return ""
        try:
            f = float(self.plot_area)
            return f"{f:.2f}"
        except (TypeError, ValueError):
            return str(self.plot_area)

    # ═══════════════════════════════════════════════════════════════════════
    #  AUTO DESCRIPTIONS ENGINE
    # ═══════════════════════════════════════════════════════════════════════
    def generate_auto_descriptions(self):
        unit = self.agr_area_unit or "acre"
        area_clean = self._clean_area()
        area_str = f"{area_clean} {unit}" if area_clean else "Prime Land Parcel"
        p_type = (self.property_type or "Agricultural Land").replace("_", " ").title()
        loc = self.locality or "Rural Cluster"
        city_str = f", {self.city}" if self.city else ""

        summary = f"A fertile {area_str} {p_type} parcel is offered for resale at {loc}{city_str}. "
        if self.selling_price:
            summary += f"Listed at ₹{self.selling_price:,}. "
        if self.irrigation_source:
            summary += f"Supported by water infrastructure categorized as '{self.irrigation_source.replace('_', ' ')}'. "
        summary += "Well-suited for farming, fruit orchards, or long-term agricultural asset appreciation."
        self.property_summary = summary

        long_desc = f"<p>Explore this prime agricultural investment opportunity: a <strong>{area_str} {p_type}</strong> located in village/taluka <strong>{loc}{city_str}</strong>.</p>"

        long_desc += "<h3>Land Specifications & Soil Profile:</h3><ul>"
        if self.plot_area:
            f_val = f"{self.plot_frontage:.2f}" if self.plot_frontage else "—"
            d_val = f"{self.plot_depth:.2f}" if self.plot_depth else "—"
            long_desc += f"<li><strong>Parcel Extent:</strong> Total area of {area_clean} {unit} (Frontage: {f_val} ft x Depth: {d_val} ft). Shape: {self.plot_shape or 'Regular'}. Topography: {self.land_topography or 'Level Flat'}.</li>"
        long_desc += f"<li><strong>Soil & Cultivation:</strong> Soil composition is '{self.soil_type or 'Fertile Agricultural'}'. Currently configured with crop/plantation: '{self.current_crop or 'Vacant/Fallow'}'.</li>"
        long_desc += f"<li><strong>Water & Power:</strong> Irrigation sourced via '{self.irrigation_source or 'Standard Agricultural Supply'}'. Power infrastructure: '{self.agr_electricity or 'Agricultural Connection Possible'}'.</li>"
        long_desc += f"<li><strong>Access & Boundary:</strong> Road/Track approach: '{self.plot_road_facing or 'Village Road Access'}' (Width: {self.road_width or 'Standard'}). Boundary demarcation: '{self.plot_fencing or 'Unmarked/Open'}'. Corner plot: {self.corner_plot.upper()}.</li>"
        long_desc += "</ul>"

        long_desc += "<h3>Revenue Clearances & Legal Compliance:</h3><ul>"
        long_desc += f"<li><strong>Revenue Records:</strong> Satbara (7/12) Extract availability: '{self.satbara_available or 'Yes'}'. Khate Utara (8A) record: '{self.khate_utara or 'Yes'}'.</li>"
        long_desc += f"<li><strong>Zoning & Conversion:</strong> Revenue land use classification is '{self.land_use or 'Agricultural'}'. NA Conversion status: '{self.na_status or 'Pure Agricultural'}'.</li>"
        long_desc += f"<li><strong>Special Clearances:</strong> Section 63/63-A clearance requirement: '{self.section63_clearance or 'Standard Agriculturist Norms'}'. Title clearance: '{self.title_clearance or 'Clear & Marketable'}'. Encumbrance: {self.property_encumbrance_status or 'Nil'}.</li>"
        long_desc += "</ul>"

        if self.selling_price and self.plot_area:
            try:
                ppa = round(float(self.selling_price) / float(self.plot_area)) if float(self.plot_area) > 0 else 0
                long_desc += f"<h3>Financial Terms:</h3><p>Total consideration is pegged at <strong>₹{self.selling_price:,}</strong> (~₹{ppa:,}/{unit}). Price negotiability: <strong>{self.price_negotiable.upper()}</strong>.</p>"
            except (TypeError, ValueError, ZeroDivisionError):
                pass

        if self.amenities or self.nearby_facilities:
            long_desc += "<h3>Amenities & Nearby Facilities:</h3><ul>"
            if self.amenities:
                long_desc += f"<li><strong>On-Site Amenities:</strong> {self.amenities}.</li>"
            if self.nearby_facilities:
                long_desc += f"<li><strong>Nearby Facilities & Connectivity:</strong> {self.nearby_facilities}.</li>"
            long_desc += "</ul>"

        long_desc += "<p>Reach out today for revenue document verification (7/12 & 8A extracts) or a guided farm inspection.</p>"
        self.property_description = long_desc

    # ═══════════════════════════════════════════════════════════════════════
    #  SAVE OVERRIDE
    # ═══════════════════════════════════════════════════════════════════════
    def save(self, *args, **kwargs):
        # ── AUTO-CALCULATE RATE PER UNIT (e.g. Rate per Hectare/Acre) ──
        if self.selling_price and self.plot_area:
            try:
                area_val = float(self.plot_area)
                if area_val > 0:
                    self.price_per_unit = round(float(self.selling_price) / area_val)
                else:
                    self.price_per_unit = None
            except (TypeError, ValueError, ZeroDivisionError):
                self.price_per_unit = None
        else:
            self.price_per_unit = None

        unit = self.agr_area_unit or "acre"
        area_clean = self._clean_area()
        area_lbl = f"{area_clean} {unit}" if area_clean else ""
        p_type = (self.property_type or "Agricultural Land").replace("_", " ").title()
        loc = self.locality or ""
        city_name = f", {self.city}" if self.city else ""

        self.property_title = " ".join(filter(bool, [area_lbl, p_type, "in", loc + city_name]))[:255]
        self.generate_auto_descriptions()

        # >>> BUILD UNIQUE KEY ONLY ON FIRST CREATE <
        if self._state.adding:
            key_source = f"{self.address}|{self.locality}|{self.city}|{self.plot_area}|{self.property_no}"
            self.property_unique_key = key_source.strip().lower().replace(" ", "")

        super().save(*args, **kwargs)

        # >>> RECALCULATE DUPLICATE GROUP FROM ACTUAL DB STATE (idempotent) <
        if self.property_unique_key:
            group_qs = AgriculturalPlotResaleProperty.objects.filter(
                property_unique_key=self.property_unique_key,
                is_deleted=False,
            )
            total = group_qs.count()
            if total > 1:
                original_id = group_qs.order_by("created_at").first().pk
                group_qs.update(duplicate_count=total, duplicate_group_id=original_id, is_duplicate=True)
            else:
                group_qs.update(duplicate_count=1, duplicate_group_id=None, is_duplicate=False)

        self.generate_auto_faqs()

    # ═══════════════════════════════════════════════════════════════════════
    #  AUTO FAQ ENGINE
    # ═══════════════════════════════════════════════════════════════════════
    def generate_auto_faqs(self):
        self.faqs.all().delete()
        faq_pool = []
        unit = self.agr_area_unit or "acre"

        if self.selling_price and self.plot_area:
            ppa = round(float(self.selling_price) / float(self.plot_area)) if float(self.plot_area) > 0 else 0
            faq_pool.append({
                "q": f"What is the total asking price and rate per {unit} for this agricultural land parcel?",
                "a": f"The total selling price is ₹{self.selling_price:,}, which computes to roughly ₹{ppa:,} per {unit}. Price negotiability status is: '{self.price_negotiable.upper()}'.",
            })
        else:
            faq_pool.append({
                "q": "Is the pricing for this agricultural plot finalized?",
                "a": "The pricing details are currently available upon request. Please contact the listing manager for exact valuations.",
            })

        label = self.get_brokerage_label()
        val = self.get_brokerage_display_value()
        faq_pool.append({
            "q": f"Is there a {label.lower()} applicable on purchasing this agricultural plot?",
            "a": f"Yes, the applicable {label.lower()} for this farm land transaction is: {val}.",
        })

        faq_pool.append({
            "q": "Are the 7/12 (Satbara) and 8A (Khate Utara) revenue extracts available?",
            "a": f"Satbara (7/12 extract) availability is listed as '{self.satbara_available or 'Available'}', and 8A Khate Utara availability is '{self.khate_utara or 'Available'}'. The title is verified as '{self.title_clearance or 'Clear Title'}'.",
        })

        faq_pool.append({
            "q": "What water irrigation and agricultural power connections service this parcel?",
            "a": f"Irrigation access is configured via '{self.irrigation_source or 'Standard Source'}', and agricultural electric supply status is '{self.agr_electricity or 'Connection Possible'}'.",
        })

        faq_pool.append({
            "q": "What is the current land use classification and NA conversion status?",
            "a": f"This parcel is classified as '{self.land_use or 'Agricultural'}' revenue land. NA Conversion status is recorded as '{self.na_status or 'Pure Agricultural'}'.",
        })

        faq_pool.append({
            "q": "What are the physical dimensions and road/track access to this land?",
            "a": f"The plot is '{self.plot_shape or 'Regular'}' in shape, with access via '{self.plot_road_facing or 'Village Road'}' (Width: {self.road_width or 'Standard'}). Corner plot advantage: {self.corner_plot.upper()}.",
        })

        faq_pool.append({
            "q": "What are the key location advantages and nearby facilities surrounding this land?",
            "a": f"Located in {self.locality or 'an established agricultural belt'}, the parcel is {self.highway_distance or 'conveniently placed'} from the nearest highway. Nearby facilities include: {self.nearby_facilities or 'local markets and village infrastructure'}.",
        })

        for item in faq_pool:
            AgriculturalPlotResaleFAQ.objects.create(property=self, question=item["q"], answer=item["a"])

    def __str__(self):
        return f"{self.property_title or 'Agricultural Plot Resale'} ({self.id})"


# ═══════════════════════════════════════════════════════════════════════════
#  CHILD MODELS
# ═══════════════════════════════════════════════════════════════════════════

class AgriculturalPlotResaleImage(models.Model):
    CATEGORY_CHOICES = [
        ('front_view',        'Agricultural Land Front View'),
        ('full_plot',         'Full Plot / Field View'),
        ('farm_gate',         'Farm Gate / Main Entrance'),
        ('boundary_fencing',  'Boundary / Fencing'),
        ('road_facing',       'Road Facing / Approach Road'),
        ('cultivated_area',   'Cultivated Area / Crops'),
        ('irrigation_source', 'Irrigation / Water Source'),
        ('borewell_well',     'Borewell / Well / Canal'),
        ('electricity_infra', 'Electricity / Power Infrastructure'),
        ('farmhouse_shed',    'Farmhouse / Shed / Existing Structure'),
        ('aerial_drone',      'Aerial / Drone View'),
        ('layout_site_plan',  'Plot Layout / Site Plan'),
    ]

    property = models.ForeignKey(
        'AgriculturalPlotResaleProperty',
        on_delete=models.CASCADE,
        related_name="images"
    )
    image = models.ImageField(upload_to="agricultural_plot/images/")
    category = models.CharField(max_length=25, choices=CATEGORY_CHOICES, default='front_view')
    sequence_order = models.PositiveIntegerField(default=0)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["category", "sequence_order", "uploaded_at"]

    def __str__(self):
        return f"{self.property_id} - {self.get_category_display()} ({self.sequence_order})"


class AgriculturalPlotResaleVideo(models.Model):
    SOURCE_CHOICES = [
        ('uploaded',    'Manually Uploaded'),
        ('auto',        'Auto Generated Slideshow'),
        ('rm_assisted', 'RM Assisted Link'),
    ]
    property = models.ForeignKey(
        'AgriculturalPlotResaleProperty',
        on_delete=models.CASCADE,
        related_name="video"
    )
    video = models.FileField(upload_to="agricultural_plot/videos/", null=True, blank=True)
    video_url = models.URLField(null=True, blank=True)
    source = models.CharField(max_length=15, choices=SOURCE_CHOICES, default='auto')
    created_at = models.DateTimeField(auto_now_add=True)

    def youtube_thumbnail(self):
        import re
        if self.source == 'rm_assisted' and self.video_url:
            match = re.search(
                r'(?:youtube\.com/watch\?v=|youtu\.be/|youtube\.com/shorts/)([A-Za-z0-9_-]{6,})',
                self.video_url
            )
            if match:
                return f"https://img.youtube.com/vi/{match.group(1)}/hqdefault.jpg"
        return None

    def get_platform_type(self):
        if not self.video_url:
            return 'unknown'
        url = self.video_url.lower()
        if 'youtube.com' in url or 'youtu.be' in url:
            return 'youtube'
        elif 'instagram.com' in url or 'instagr.am' in url:
            return 'instagram'
        elif 'facebook.com' in url or 'fb.watch' in url:
            return 'facebook'
        elif 'vimeo.com' in url:
            return 'vimeo'
        elif 'drive.google.com' in url:
            return 'gdrive'
        return 'external'


class AgriculturalPlotResaleFAQ(models.Model):
    property = models.ForeignKey(AgriculturalPlotResaleProperty, on_delete=models.CASCADE, related_name="faqs")
    question = models.CharField(max_length=255)
    answer = models.TextField()





class AgriculturalPlotResaleActivityLog(models.Model):

    ACTION_CHOICES = [
        ("SEARCH", "Manual Query Search"),
        ("CREATE", "Property Entry Created"),
        ("UPDATE", "Record Update Action"),
        ("DELETE", "Deletion / Purge Record"),
        ("EXCEL_IMPORT", "Excel Sheet Import Data"),
    ]

    timestamp = models.DateTimeField(auto_now_add=True)
    user_identity = models.CharField(max_length=255, null=True, blank=True)
    user_role = models.CharField(max_length=100, null=True, blank=True)
    action_type = models.CharField(max_length=50, choices=ACTION_CHOICES)
    property_id = models.CharField(max_length=100, null=True, blank=True)
    targeted_fields = models.CharField(max_length=255, null=True, blank=True)
    associated_file = models.CharField(max_length=255, null=True, blank=True)
    action_payload = models.TextField(null=True, blank=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    status = models.CharField(max_length=20, default="SUCCESS")

    class Meta:
        ordering = ["-timestamp"]

################## END MODEL SECTION Agricultural Plot RESALE LISTING################