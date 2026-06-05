from django.db import models
from django.utils.timezone import now
import uuid


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
        return str(self.user_name)+"-"+self.user_role
    

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

class RentalResidentialProperty(models.Model):

    # =====================================================
    # BASIC INFORMATION
    # =====================================================

    rental_residential_id = models.CharField(
        max_length=20,
        primary_key=True,
        default=generate_unique_rental_residential_id,
        editable=False,
        unique=True
    )

    property_title = models.CharField(max_length=255, blank=True, null=True)

    #property_purpose = models.CharField(max_length=50, blank=True, null=True)

    property_type = models.CharField(max_length=100, blank=True, null=True)

    bhk_type = models.CharField(max_length=50, blank=True, null=True)

    renting_option = models.CharField(max_length=50, blank=True, null=True)

    built_up_area = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True
    )

    bathrooms = models.IntegerField(blank=True, null=True)

    balconies = models.IntegerField(blank=True, null=True)

    floor_number = models.CharField(max_length=50, blank=True, null=True)

    total_floors = models.IntegerField(blank=True, null=True)

    facing = models.CharField(max_length=50, blank=True, null=True)

    furnishing_status = models.CharField(max_length=50, blank=True, null=True)

    available_for = models.CharField(max_length=50, blank=True, null=True)



    # =====================================================
    # PROPERTY DETAILS
    # =====================================================

    zone = models.CharField(max_length=50, blank=True, null=True)

    ownership_type = models.CharField(max_length=50, blank=True, null=True)

    construction_status = models.CharField(max_length=50, blank=True, null=True)

    property_age = models.CharField(max_length=50, blank=True, null=True)

    carpet_area = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True
    )

    plot_area = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True
    )

    building_name = models.CharField(max_length=200, blank=True, null=True)



    # =====================================================
    # AVAILABILITY DETAILS
    # =====================================================

    possession_status = models.CharField(max_length=50, blank=True, null=True)

    available_from = models.DateField(blank=True, null=True)

    lease_duration = models.CharField(max_length=50, blank=True, null=True)

    brokerage = models.CharField(max_length=10, blank=True, null=True)

    brokerage_percentage = models.CharField(max_length=20, blank=True, null=True)

    manual_brokerage = models.CharField(max_length=20, blank=True, null=True)



    # =====================================================
    # PRICING DETAILS
    # =====================================================

    monthly_rent = models.BigIntegerField(blank=True, null=True)

    security_deposit = models.BigIntegerField(blank=True, null=True)

    maintenance_type = models.CharField(max_length=50, blank=True, null=True)

    maintenance_amount = models.BigIntegerField(blank=True, null=True)



    # =====================================================
    # LOCATION DETAILS
    # =====================================================

    address = models.TextField(blank=True, null=True)

    city = models.CharField(max_length=150, blank=True, null=True)

    locality = models.CharField(max_length=150, blank=True, null=True)

    state = models.CharField(max_length=150, blank=True, null=True)

    pincode = models.CharField(max_length=10, blank=True, null=True)

    road_connectivity = models.CharField(max_length=150, blank=True, null=True)



    # =====================================================
    # AMENITIES & FACILITIES
    # =====================================================

    amenities = models.TextField(blank=True, null=True)

    facilities = models.TextField(blank=True, null=True)



    # =====================================================
    # DESCRIPTION
    # =====================================================

    description = models.TextField(blank=True, null=True)

    rent_residential_desc = models.TextField(blank=True, null=True)



    # =====================================================
    # OWNER DETAILS
    # =====================================================

    owner_name = models.CharField(max_length=150, blank=True, null=True)

    contact_number = models.CharField(max_length=15, blank=True, null=True)

    email = models.EmailField(blank=True, null=True)

    alternate_contact = models.CharField(max_length=15, blank=True, null=True)

# -------------------------
    # Uploaded By
    # -------------------------
    uploaded_by_name = models.CharField(max_length=150, blank=True, null=True)
    uploaded_by_email = models.CharField(max_length=150, blank=True, null=True)
    uploaded_by_contact = models.CharField(max_length=20, blank=True, null=True)
    uploaded_by_role = models.CharField(max_length=100, blank=True, null=True)
    
    upload_file_name = models.CharField(max_length=255, blank=True, null=True)
   

    
    is_deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(null=True, blank=True)
    deleted_by = models.CharField(max_length=150, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    



    def save(self, *args, **kwargs):
        title_parts = []
        if self.furnishing_status: title_parts.append(self.furnishing_status)
        if self.bhk_type: title_parts.append(self.bhk_type)
        title_parts.append(self.property_type if self.property_type else "Property")
        title_parts.append("for Rent")
        
        location = f"in {self.building_name}" if self.building_name else ""
        if self.locality: location += f", {self.locality}" if location else f"in {self.locality}"
        if self.city: location += f", {self.city}" if location else f"in {self.city}"
        if location: title_parts.append(location)
        
        if self.built_up_area:
            title_parts.append(f"({str(self.built_up_area).rstrip('0').rstrip('.')} sq.ft.)")
            
        self.property_title = " ".join(title_parts).strip()[:255]
        super(RentalResidentialProperty, self).save(*args, **kwargs)
        self.generate_auto_faqs()
    


    def generate_auto_faqs(self):
        """Dynamic programmatic structural data engine - handles potential data errors gracefully"""
        self.faqs.all().delete()
        faq_pool = []

        # Enforce safe casting metrics across numerical elements
        try: rent_val = int(float(str(self.monthly_rent or 0).replace(",", "").strip()))
        except: rent_val = 0
        try: deposit_val = int(float(str(self.security_deposit or 0).replace(",", "").strip()))
        except: deposit_val = 0
        try: maint_val = int(float(str(self.maintenance_amount or 0).replace(",", "").strip()))
        except: maint_val = 0

        if rent_val > 0:
            maint_str = f" Maintenance is configured as '{self.maintenance_type}' with an outlay of ₹{maint_val:,}." if maint_val > 0 else ""
            faq_pool.append({
                "q": f"What are the rent breakdown details and security deposit for this {self.bhk_type or ''} {self.property_type or 'Property'}?",
                "a": f"The scheduled monthly rental valuation for this property is ₹{rent_val:,}. Securing this listing requires a security deposit of ₹{deposit_val:,}.{maint_str}"
            })

        if self.built_up_area and self.floor_number:
            carpet_str = f" out of which the actual usable carpet area maps to {self.carpet_area} sq.ft." if self.carpet_area else ""
            faq_pool.append({
                "q": f"How much space does this rental option offer and which floor is it located on?",
                "a": f"This residential configuration encompasses a spacious built-up area of {self.built_up_area} sq.ft.{carpet_str} The home is comfortably positioned on the {self.floor_number} of a total structure height of {self.total_floors or 'multiple'} storeys."
            })

        if self.furnishing_status:
            balcony_str = f" accompanied by {self.balconies} well-ventilated balcony areas" if self.balconies else ""
            faq_pool.append({
                "q": f"What is the furnishing status and physical asset configuration of this property?",
                "a": f"The property is verified as {self.furnishing_status}. The functional architecture provides {self.bathrooms or 1} luxury bathrooms{balcony_str}."
            })

        if self.facing:
            faq_pool.append({
                "q": f"Which direction does this rental unit face, and does it receive natural lighting?",
                "a": f"This property features a strategic {self.facing}-facing architectural layout orientation. This guarantees optimal wind ventilation channels and premium morning/evening daylight exposure across the rooms."
            })

        if self.available_for or self.lease_duration:
            faq_pool.append({
                "q": f"Who is eligible to lease this home and what is the standard commitment duration?",
                "a": f"The property allocation preferences match expectations for a {self.available_for or 'verified family or working professional group'}. The operational leasing framework stipulates a baseline duration commitment of {self.lease_duration or '11 Months'}."
            })

        if self.possession_status:
            date_str = " immediately upon verification processing"
            if self.available_from:
                if isinstance(self.available_from, str):
                    try:
                        clean_d = self.available_from.strip().split(" ")[0]
                        parsed_d = datetime.strptime(clean_d, "%Y-%m-%d")
                        date_str = f" starting from {parsed_d.strftime('%d %B %Y')}"
                    except:
                        date_str = f" starting from {self.available_from}"
                else:
                    try: date_str = f" starting from {self.available_from.strftime('%d %B %Y')}"
                    except: date_str = f" starting from {self.available_from}"

            faq_pool.append({
                "q": f"When can tenants move into this property and what is the current occupancy status?",
                "a": f"The present structural readiness index stands classified as '{self.possession_status}'. Seamless key handover and tenant onboarding can be activated{date_str}."
            })

        for item in faq_pool:
            RentalResidentialFAQ.objects.create(property=self, question=item["q"], answer=item["a"])

    def __str__(self):
        return str(self.property_title) if self.property_title else f"Property #{self.rental_residential_id}"


# ==========================================
# ✅ NEW MODEL FOR IMAGES

class RentalResidentialImage(models.Model):
    property = models.ForeignKey(RentalResidentialProperty, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='residential_rent/')
    sequence_order = models.PositiveIntegerField(default=0)
    class Meta:
        ordering = ['sequence_order']

class RentalResidentialFAQ(models.Model):
    property = models.ForeignKey(RentalResidentialProperty, on_delete=models.CASCADE, related_name='faqs')
    question = models.CharField(max_length=255)
    answer = models.TextField()





class RentalActivityLog(models.Model):
    ACTION_CHOICES = [
        ('SEARCH', 'Manual Query Search'),
        ('CREATE', 'Property Entry Created'),
        ('UPDATE', 'Record Update Action'),
        ('DELETE', 'Deletion / Purge Record'),
        ('EXCEL_IMPORT', 'Excel Sheet Import Data'),
    ]

    timestamp = models.DateTimeField(auto_now_add=True)
    user_identity = models.CharField(max_length=255, null=True, blank=True) # e.g., "admin@example.com"
    user_role = models.CharField(max_length=100, null=True, blank=True)     # e.g., "Super Admin", "Agent"
    action_type = models.CharField(max_length=50, choices=ACTION_CHOICES)
    
    # Granular Target Trackers
    property_id = models.CharField(max_length=100, null=True, blank=True)    # The specific Rental Residential ID affected
    targeted_fields = models.CharField(max_length=255, null=True, blank=True) # Fields modified (e.g., "monthly_rent, brokerage")
    associated_file = models.CharField(max_length=255, null=True, blank=True) # File-wise Tracker (e.g., "june_listings.xlsx")[cite: 1]
    
    action_payload = models.TextField(null=True, blank=True)                 # Full snapshot of old vs new data JSON
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    status = models.CharField(max_length=20, default='SUCCESS')

    class Meta:
        ordering = ['-timestamp']


################################END MODEL SECTION OF THE RENTAL RESIDENTIAL LISTING####################


############### Models Starts for Rental COMMERCIAL Property  model ############################ same in this this teh rental proeprty listing model so as per add the user role in ths also and give me the view of like this residenital view for data submit  




class CommercialRentalProperty(models.Model):
    # ═══════════════════════════════════════
    # SYSTEM GENERATED FIELDS
    # ═══════════════════════════════════════
    commercial_rental_id = models.CharField(max_length=20, unique=True, blank=True)
    property_title = models.CharField(max_length=255, blank=True)

    # ═══════════════════════════════════════
    # STEP 1: BASIC INFORMATION
    # ═══════════════════════════════════════
    property_type = models.CharField(max_length=50)
    property_condition = models.CharField(max_length=50)
    city = models.CharField(max_length=100)
    area_locality = models.CharField(max_length=200)
    property_address = models.TextField()
    building_name = models.CharField(max_length=200)
    possession_status = models.CharField(max_length=50)
    available_from = models.DateField(blank=True, null=True)
    age_of_property = models.CharField(max_length=20)
    zone_type = models.CharField(max_length=50, blank=True, null=True)
    location_hub = models.CharField(max_length=50, blank=True, null=True)
    ownership_type = models.CharField(max_length=50)
    construction_status = models.CharField(max_length=20, blank=True, null=True)

    # ═══════════════════════════════════════
    # STEP 2: AREA, PRICING & BUILDING
    # ═══════════════════════════════════════
    builtup_area = models.IntegerField()
    carpet_area = models.IntegerField(blank=True, null=True)
    expected_rent = models.IntegerField()
    security_deposit = models.IntegerField(blank=True, null=True)
    maintenance_charges = models.IntegerField(blank=True, null=True)

    # Note: Changed to CharField because your HTML form sends 'Yes'/'No' string radio values
    negotiable = models.CharField(max_length=10, blank=True, null=True) 

    brokerage = models.CharField(max_length=5, blank=True, null=True)
    brokerage_percentage = models.CharField(max_length=20, blank=True, null=True)
    manual_brokerage = models.CharField(max_length=50, blank=True, null=True)

    dg_ups_included = models.BooleanField(default=False)
    electricity_included = models.BooleanField(default=False)
    water_included = models.BooleanField(default=False)

    lockin_period = models.IntegerField(blank=True, null=True)
    rent_increase = models.FloatField(blank=True, null=True)

    total_floors = models.IntegerField(blank=True, null=True)
    your_floor = models.IntegerField(blank=True, null=True)
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

    flooring_type = models.CharField(max_length=50, blank=True, null=True)

    # ═══════════════════════════════════════
    # STEP 3: AMENITIES & FACILITIES
    # ═══════════════════════════════════════
    amenities = models.JSONField(blank=True, null=True)
    nearby_facilities = models.JSONField(blank=True, null=True)
    property_summary = models.TextField(blank=True, null=True)
    property_description = models.TextField(blank=True, null=True)

    # ═══════════════════════════════════════
    # STEP 4: MEDIA, CONTACT & UPLOADER
    # ═══════════════════════════════════════
    
    video = models.FileField(upload_to='commercial_rent/videos/', blank=True, null=True)

    owner_name = models.CharField(max_length=100)
    contact_number = models.CharField(max_length=20)
    email = models.EmailField()
    alternate_contact = models.CharField(max_length=20, blank=True, null=True)

    uploaded_by_name = models.CharField(max_length=100, blank=True, null=True)
    uploaded_by_email = models.EmailField(blank=True, null=True)
    uploaded_by_contact = models.CharField(max_length=20, blank=True, null=True)
    uploaded_by_role = models.CharField(max_length=100, blank=True, null=True)

    # ═══════════════════════════════════════
    # SYSTEM TRACKING DATA
    # ═══════════════════════════════════════
    # auto_now_add=True records exactly what date and time the row was created in the DB
    created_at = models.DateTimeField(auto_now_add=True) 
    is_deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(null=True, blank=True)
    upload_file_name = models.CharField(max_length=255, blank=True, null=True)
    upload_file_hash = models.CharField(max_length=255, blank=True, null=True)
    deleted_by = models.CharField(max_length=150, blank=True, null=True)

    # ═══════════════════════════════════════
    # AUTO GENERATION LOGIC
    # ═══════════════════════════════════════
    def save(self, *args, **kwargs):
        
        # 1. Generate Custom ID (e.g., EFCR-5F8B2C) if it doesn't exist
        if not self.commercial_rental_id:
            unique_code = str(uuid.uuid4()).upper()[:6]
            self.commercial_rental_id = f"EFCPR-{unique_code}"
            
        # 2. Auto-generate the Property Title dynamically
        if not self.property_title:
            # Format raw strings (e.g., 'warm-shell' -> 'Warm Shell')
            condition = self.property_condition.replace('-', ' ').title() if self.property_condition else ""
            p_type = self.property_type.replace('-', ' ').title() if self.property_type else "Commercial Property"
            locality = self.area_locality.title() if self.area_locality else ""
            city_name = self.city.title() if self.city else ""
            area = f"({self.builtup_area} sq.ft.)" if self.builtup_area else ""

            # Build the title: "Fitted Office Space for Rent in Viman Nagar, Pune (1500 sq.ft.)"
            title_parts = []
            if condition: title_parts.append(condition)
            title_parts.append(p_type)
            title_parts.append("for Rent in")
            if locality: title_parts.append(f"{locality},")
            if city_name: title_parts.append(city_name)
            if area: title_parts.append(area)

            # Combine everything and remove any extra spaces
            self.property_title = " ".join(title_parts).strip()

        # Save to database
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.commercial_rental_id} | {self.property_title}"

# ✅ MULTIPLE IMAGES MODEL
class CommercialRentalPropertyImage(models.Model):
    property = models.ForeignKey(
        CommercialRentalProperty,
        on_delete=models.CASCADE,
        related_name='images'
    )
    image = models.ImageField(upload_to='commercial_rent/images/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Image for {self.property.id}"
############### Models END for Rental COMMERICIAL  Property  model ############################ same in this this teh rental proeprty listing model so as per add the user role in ths also and give me the view of like this residenital view for data submit  



############### Models Starts for Rental PG_COLIVING Property  model ############################ same in this this teh rental proeprty listing model so as per add the user role in ths also and give me the view of like this residenital view for data submit  








def generate_unique_pg_property_id():
    return f"EFPG-{uuid.uuid4().hex[:8].upper()}"

class PGColivingProperty(models.Model):
    # UNIQUE IDENTIFIER & TIMESTAMPS
    pg_property_id = models.CharField(
        max_length=20,
        primary_key=True,
        default=generate_unique_pg_property_id,
        editable=False,
        unique=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # STEP 1: BASIC INFO
    property_title = models.CharField(max_length=200, blank=True, null=True, help_text="Auto-generated based on project context if empty")
    city = models.CharField(max_length=100)
    building_name = models.CharField(max_length=200, blank=True, null=True)
    locality = models.CharField(max_length=200)
    property_address = models.TextField()
    total_beds = models.IntegerField()
    pg_for = models.CharField(max_length=50)            # Boys, Girls, Co-living
    furnishing_type = models.CharField(max_length=50)    # Unfurnished, Semi-Furnished, Fully Furnished
    sharing_type = models.CharField(max_length=100, blank=True, null=True)
    best_suited_for = models.CharField(max_length=100, blank=True, null=True)
    
    # MEALS INFO
    meals_available = models.BooleanField(default=False)
    meal_offerings = models.CharField(max_length=100, blank=True, null=True)   # Breakfast, Lunch, Dinner
    meal_speciality = models.CharField(max_length=100, blank=True, null=True)   # Veg, Non-Veg, Jain
    
    # RULES & MANAGEMENTS
    notice_period = models.IntegerField(blank=True, null=True)
    lockin_period = models.IntegerField(blank=True, null=True)
    minimum_stay = models.IntegerField()
    available_from = models.DateField()
    property_managed_by = models.CharField(max_length=50, blank=True, null=True)
    manager_stays = models.BooleanField(default=False)

    # STEP 3: RULES & AMENITIES
    opposite_sex_allowed = models.BooleanField(default=False)
    any_time_allowed = models.BooleanField(default=False)
    visitors_allowed = models.BooleanField(default=False)
    guardian_allowed = models.BooleanField(default=False)
    drinking_allowed = models.BooleanField(default=False)
    smoking_allowed = models.BooleanField(default=False)
    property_description = models.TextField(blank=True, null=True)
    
    amenities = models.TextField(blank=True, null=True)          # Stored as comma-separated values
    nearby_facilities = models.TextField(blank=True, null=True)  # Stored as comma-separated values

    # STEP 4: MEDIA
    video = models.FileField(upload_to='pg/videos/', blank=True, null=True)

    # CONTACT INFO
    owner_name = models.CharField(max_length=100)
    contact_number = models.CharField(max_length=20)
    email = models.EmailField()
    alternate_contact = models.CharField(max_length=20, blank=True, null=True)

    uploaded_by_name = models.CharField(max_length=100, blank=True, null=True)
    uploaded_by_email = models.EmailField(blank=True, null=True)
    uploaded_by_contact = models.CharField(max_length=20, blank=True, null=True)
    uploaded_by_role = models.CharField(max_length=100, blank=True, null=True)

    # AUDITING SYSTEM
    is_deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(null=True, blank=True)
    upload_file_name = models.CharField(max_length=255, blank=True, null=True)
    deleted_by = models.CharField(max_length=150, blank=True, null=True)

    def save(self, *args, **kwargs):
        # ✅ FIXED: Target correct property_title attribute instead of invalid pg_property text string field
        if not self.property_title:
            gender_target = self.pg_for if self.pg_for else "Co-Living"
            b_name = f"{self.building_name} " if self.building_name else ""
            self.property_title = f"Premium {gender_target} PG at {b_name}{self.locality}".strip()
        super().save(*args, **kwargs)

    def __str__(self):
        # ✅ FIXED: References self.property_title correctly instead of old pg_property_title
        return f"{self.property_title} ({self.pg_property_id})"


class PGRoomDetail(models.Model):
    property = models.ForeignKey(PGColivingProperty, on_delete=models.CASCADE, related_name='rooms')
    room_type = models.CharField(max_length=50)
    room_beds = models.IntegerField()
    room_rent = models.DecimalField(max_digits=10, decimal_places=2)
    room_deposit = models.DecimalField(max_digits=10, decimal_places=2)
    room_brokerage = models.CharField(max_length=10) # Yes / No
    room_brokerage_percent = models.CharField(max_length=20, blank=True, null=True)
    room_manual_brokerage = models.CharField(max_length=50, blank=True, null=True)
    room_facilities = models.TextField(blank=True, null=True) # Comma-separated facilities list

    def __str__(self):
        return f"{self.room_type.capitalize()} Room - Property: {self.property.pg_property_id}"


class PGPropertyImage(models.Model):
    property = models.ForeignKey(PGColivingProperty, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='pg/images/')



    ############### Models End for Rental PG_COLIVING Property  model ############################ same in this this teh rental proeprty listing model so as per add the user role in ths also and give me the view of like this residenital view for data submit  



############### Models Starts for Resale Resindential  Property  model ############################ 









def generate_resale_unique_property_id():
    return f"EFRES-{uuid.uuid4().hex[:8].upper()}"

class ResaleResidentialProperty(models.Model):
    # ── SYSTEM CONTROL & IDENTIFICATION ─────────────────────
    # By removing primary_key=True, Django automatically handles the non-nullable background id, 
    # and this field will safely generate unique keys without breaking migrations!
    property_id = models.CharField(
        max_length=20, 
        unique=True, 
        editable=False, 
        blank=True, 
        null=True
    )
    property_title = models.CharField(max_length=255, blank=True, null=True)

    # ── STEP 1: BASIC INFO & CONFIGURATION ──────────────────
    property_type = models.CharField(max_length=50) 
    zone = models.CharField(max_length=50)          
    society_type = models.CharField(max_length=50)  
    water_type = models.CharField(max_length=50)    
    furnishing_type = models.CharField(max_length=50) 
    age_of_property = models.CharField(max_length=50) 
    facing = models.CharField(max_length=50)          
    available_from = models.DateField(null=True, blank=True)

    # Property Configuration
    bhk = models.CharField(max_length=20)             
    bathrooms = models.PositiveIntegerField(default=1)
    balconies = models.PositiveIntegerField(default=0)
    covered_parking = models.PositiveIntegerField(default=0)
    open_parking = models.PositiveIntegerField(default=0)

    # Measurements
    builtup_area = models.DecimalField(max_digits=12, decimal_places=2)
    carpet_area = models.DecimalField(max_digits=12, decimal_places=2)
    plot_area = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    floor_no = models.IntegerField() 
    total_floors = models.PositiveIntegerField()

    # ── STEP 2: LEGAL & PRICING DETAILS ─────────────────────
    ownership_type = models.CharField(max_length=50)   
    num_owners = models.CharField(max_length=20)       
    
    has_loan = models.CharField(max_length=5, default='no') 
    loan_amount = models.DecimalField(max_digits=14, decimal_places=2, null=True, blank=True)
    
    has_tenants = models.CharField(max_length=5, default='no')
    tenant_details = models.TextField(blank=True, null=True)
    
    has_legal_dispute = models.CharField(max_length=5, default='no')
    dispute_details = models.TextField(blank=True, null=True)
    
    has_tax_due = models.CharField(max_length=5, default='no')
    pending_tax_amount = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)

    expected_price = models.DecimalField(max_digits=15, decimal_places=2)
    price_per_sqft = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True) 
    is_negotiable = models.CharField(max_length=5, default='yes') 
    
    brokerage = models.CharField(max_length=5, blank=True, null=True) 
    brokerage_percentage = models.CharField(max_length=50, blank=True, null=True) 
    manual_brokerage = models.CharField(max_length=100, blank=True, null=True)
    
    description = models.TextField() 

    # ── STEP 3: AMENITIES & LOCATION ────────────────────────
    nearby_facilities = models.TextField(blank=True, null=True) 
    amenities = models.TextField(blank=True, null=True)         
    
    city = models.CharField(max_length=100)
    locality = models.CharField(max_length=150)
    building_name = models.CharField(max_length=200, blank=True, null=True)
    complete_address = models.TextField()

    owner_name = models.CharField(max_length=150)
    owner_contact = models.CharField(max_length=20)
    owner_email = models.EmailField()
    residential_status = models.CharField(max_length=20) 

    # ── STEP 4: PHOTOS & PUBLISH SYSTEM ─────────────────────
    floor_plan = models.ImageField(upload_to='properties/floor_plans/', null=True, blank=True) 
    property_video = models.FileField(upload_to='properties/videos/', null=True, blank=True)

    uploaded_by_name = models.CharField(max_length=150, blank=True, null=True)
    uploaded_by_email = models.EmailField(blank=True, null=True)
    uploaded_by_contact = models.CharField(max_length=30, blank=True, null=True)
    uploaded_by_role = models.CharField(max_length=50, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name = 'Resale Residential Property'
        verbose_name_plural = 'Resale Residential Properties'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.property_title or 'Property Block'} ({self.property_id})"

    def save(self, *args, **kwargs):
        # 0. Safely generate the unique ID format before saving if it's missing
        if not self.property_id:
            while True:
                new_id = generate_resale_unique_property_id()
                if not ResaleResidentialProperty.objects.filter(property_id=new_id).exists():
                    self.property_id = new_id
                    break

        # 1. Price Per Sq.Ft calculation
        if self.expected_price and self.builtup_area:
            try:
                area = float(self.builtup_area)
                price = float(self.expected_price)
                if area > 0:
                    self.price_per_sqft = round(price / area, 2)
            except (ValueError, TypeError):
                pass

        # 2. Automated Title Generation
        if not self.property_title:
            bhk_string = self.bhk.upper() if self.bhk else ""
            type_string = self.property_type.capitalize() if self.property_type else "Property"
            project_context = f" in {self.building_name}" if self.building_name else ""
            location_context = f" at {self.locality}, {self.city}" if self.locality and self.city else ""
            
            constructed_title = f"Spacious {bhk_string} {type_string}{project_context}{location_context}"
            self.property_title = constructed_title.strip()

        super().save(*args, **kwargs)

class ResalePropertyImage(models.Model):
    property = models.ForeignKey(ResaleResidentialProperty, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='properties/images/')
    uploaded_at = models.DateTimeField(auto_now_add=True)






############## Models End for Resale Resindential  Property  model ############################ 




############## Models Start for Resale Commericial  Property  model ############################ 




class CommercialResaleProperty(models.Model):
    
    
    # ── SYSTEM CONTROL & IDENTIFICATION ─────────────────────
    # Internal automated sequential primary key to prevent migration collisions
    id = models.AutoField(primary_key=True)
    
    # Alphanumeric unique public registry key matching application code style
    commercial_id = models.CharField(
        max_length=50,
        unique=True,
        editable=False,
        blank=True,
        null=True,
        help_text="Automated unique serial lookup tracking tag"
    )
    
    # Updated from 'title' to 'property_title' per requested changes
    property_title = models.CharField(max_length=255, blank=True, null=True) 

    # ── STEP 1: BASIC INFO & SPECIFICATIONS ──────────────────
    # Section 1: Basic Information Fields Sequence
    property_type = models.CharField(max_length=50)        # office, shop, warehouse, industrial, land
    zone_type = models.CharField(max_length=50)            # industrial, commercial, residential, sez
    location_hub = models.CharField(max_length=50, blank=True, null=True) # it, business, mall, standalone
    property_condition = models.CharField(max_length=50)    # new, excellent, good, renovation
    ownership_type = models.CharField(max_length=50)        # freehold, leasehold, cooperative
    age_of_property = models.CharField(max_length=50)       # 0-1, 1-3, 3-5, 5-10, 10+
    available_from = models.DateField(blank=True, null=True)

    # Section 2: Commercial Specifications Fields Sequence
    num_staircases = models.PositiveIntegerField(default=0, blank=True, null=True)
    passenger_lifts = models.PositiveIntegerField(default=0)
    service_lifts = models.PositiveIntegerField(default=0)
    num_cabins = models.PositiveIntegerField(default=0, blank=True, null=True)
    meeting_rooms = models.PositiveIntegerField(default=0, blank=True, null=True)
    min_seats = models.PositiveIntegerField(blank=True, null=True)
    max_seats = models.PositiveIntegerField(blank=True, null=True)
    private_parking = models.PositiveIntegerField(default=0)
    public_parking = models.PositiveIntegerField(default=0, blank=True, null=True)

    # Section 3: Area Measurements Fields Sequence
    builtup_area = models.DecimalField(max_digits=12, decimal_places=2)
    carpet_area = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    plot_area = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)

    # ── STEP 2: LEGAL & PRICING DETAILS ─────────────────────
    # Section 4: Ownership & Legal Conditional Sequence
    num_owners = models.CharField(max_length=20)           # 1, 2, 3, 4+
    loan_on_property = models.CharField(max_length=5, default='no') # yes / no radio toggles
    loan_amount = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    existing_tenants = models.CharField(max_length=5, default='no') # yes / no radio toggles
    tenant_details = models.TextField(blank=True, null=True)
    legal_dispute = models.CharField(max_length=5, default='no')    # yes / no radio toggles
    dispute_details = models.TextField(blank=True, null=True)
    tax_due = models.CharField(max_length=5, default='no')          # yes / no radio toggles
    pending_tax_amount = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    fire_noc = models.CharField(max_length=5, blank=True, null=True) # yes / no radio toggles

    # Section 5: Pricing Metrics Fields Sequence
    brokerage = models.CharField(max_length=5, blank=True, null=True) # Yes / No Selection Dropdown
    brokerage_percentage = models.CharField(max_length=50, blank=True, null=True) # 1%, 1.5%, 2%, Negotiable, Manual
    manual_brokerage = models.CharField(max_length=100, blank=True, null=True)
    expected_price = models.DecimalField(max_digits=15, decimal_places=2)
    price_per_sqft = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True) 
    property_description = models.TextField() # CKEditor Text Box
    sanctioning_authority = models.TextField() # CKEditor Text Box

    # ── STEP 3: AMENITIES & LOCATION ────────────────────────
    # Section 6 & 7: Multi-Select System Parameter Storage Strings
    nearby_facilities = models.TextField(blank=True, null=True) # Comma-separated array list
    amenities = models.TextField(blank=True, null=True)         # Comma-separated array list

    # Section 8: Address Mapping Sequence
    city = models.CharField(max_length=100)
    locality = models.CharField(max_length=100)
    building_name = models.CharField(max_length=200, blank=True, null=True)
    property_address = models.TextField()

    # Section 9: Verified Owner Contact Sequence
    owner_name = models.CharField(max_length=100)
    owner_contact = models.CharField(max_length=20)
    owner_email = models.EmailField()
    residential_status = models.CharField(max_length=20)       # resident, nri, pio

    # ── STEP 4: PHOTOS & PUBLISH SYSTEM ─────────────────────
    # Section 10: Direct Media Portfolio Assets
    floor_plan = models.ImageField(upload_to='commercial/floor_plans/', null=True, blank=True) 
    property_video = models.FileField(upload_to='commercial/videos/', blank=True, null=True)

    # Section 11: Session User Profile Auditing Variables
    uploaded_by_name = models.CharField(max_length=100, blank=True, null=True)
    uploaded_by_email = models.EmailField(blank=True, null=True)
    uploaded_by_contact = models.CharField(max_length=30, blank=True, null=True)
    uploaded_by_role = models.CharField(max_length=50, blank=True, null=True)

    # ── METRIC TIMESTAMPS & AUDITING TRAILS ──────────────────
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(null=True, blank=True)
    deleted_by = models.CharField(max_length=150, blank=True, null=True)
    upload_file_name = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        verbose_name = "Commercial Property"
        verbose_name_plural = "Commercial Properties"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.property_title or 'Commercial Space'} ({self.commercial_id or self.id})"

    def save(self, *args, **kwargs):
        # 1. Generate Alphanumeric Tracking IDs: Sets up clean human-readable lookup codes safely
        if not self.commercial_id:
            self.commercial_id = f"EFCOM-{uuid.uuid4().hex[:8].upper()}"

        # 2. Secondary Mathematical Extraction Pipeline: Calculate exact Price Per Sq.Ft dynamically
        if self.expected_price and self.builtup_area:
            try:
                area = float(self.builtup_area)
                price = float(self.expected_price)
                if area > 0:
                    self.price_per_sqft = round(price / area, 2)
            except (ValueError, TypeError):
                pass

        # 3. Automated Title Assembly Pattern: Intuitively titles blank records matching context inputs
        if not self.property_title:
            type_lbl = self.property_type.replace('_', ' ').title() if self.property_type else "Commercial"
            area_lbl = f"{int(float(self.builtup_area))} Sqft" if self.builtup_area else ""
            building_ctx = f" in {self.building_name}" if self.building_name else ""
            locality_ctx = f" at {self.locality}, {self.city}" if self.locality and self.city else ""
            
            constructed_title = f"Premium {area_lbl} {type_lbl}{building_ctx}{locality_ctx}"
            self.property_title = " ".join(constructed_title.split()) 

        super().save(*args, **kwargs)


class CommercialPropertyImage(models.Model):
    """Child entity designed to capture dynamic image collections handled during form Step 4."""
    property = models.ForeignKey(
        CommercialResaleProperty, 
        on_delete=models.CASCADE, 
        related_name='images'
    )
    image = models.ImageField(upload_to='commercial/images/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Image attachment for Commercial ID: {self.property.commercial_id or self.property.id}"


############## Models End for Resale Commericial  Property  model ############################ 

#########################Start Model of RESALE PLOT LISTING####################3





class PlotSaleProperty(models.Model):
    # --- Step 1: Plot Specs ---
    plot_title = models.CharField(max_length=255, blank=True, null=True)
    plot_area = models.FloatField(blank=True, null=True)
    resale_plot_type = models.CharField(max_length=100, blank=True, null=True)
    plot_road_facing = models.CharField(max_length=100, blank=True, null=True)
    plot_corner = models.BooleanField(default=False)
    available_from = models.DateField(blank=True, null=True)
    plot_authority = models.CharField(max_length=150, blank=True, null=True)
    plot_fencing = models.BooleanField(default=False)

    # --- Step 2: Pricing & Legal ---
    plot_price = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    brokerage = models.CharField(max_length=10, blank=True, null=True) # Yes/No
    brokerage_percentage = models.CharField(max_length=50, blank=True, null=True)
    plot_ownership = models.CharField(max_length=100, blank=True, null=True)
    plot_loan = models.BooleanField(default=False)
    plot_loan_amount = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)

    # --- Step 3: Media & Certificates ---
    encumbrance_cert = models.FileField(upload_to='plot_docs/certificates/', blank=True, null=True)
    social_video = models.FileField(upload_to='plot_docs/videos/', blank=True, null=True)

    # --- Step 4: Location & Contact ---
    plot_city = models.CharField(max_length=100, blank=True, null=True)
    plot_locality = models.CharField(max_length=150, blank=True, null=True)
    plot_address = models.TextField(blank=True, null=True)
    plot_owner_name = models.CharField(max_length=150, blank=True, null=True)
    plot_owner_contact = models.CharField(max_length=15, blank=True, null=True)
    plot_owner_email = models.EmailField(blank=True, null=True)

    # --- Uploaded By ------------------------------------
    uploaded_by_name    = models.CharField(max_length=100, blank=True, null=True)
    uploaded_by_email   = models.EmailField(blank=True, null=True)
    uploaded_by_contact = models.CharField(max_length=15, blank=True, null=True)
    uploaded_by_role    = models.CharField(max_length=50, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(null=True, blank=True)

    upload_file_name = models.CharField(max_length=255, blank=True, null=True)
    deleted_by = models.CharField(max_length=150, blank=True, null=True) # 👈 ADD THIS

    def __str__(self):
        return f"{self.plot_title} - {self.plot_locality}"

class PlotSaleImage(models.Model):
    property = models.ForeignKey(PlotSaleProperty, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='plot_docs/images/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Image for {self.property.plot_title}"
    

#############END MODEL SECTION RESALE PLOT LISTING##################


#######################START MODEL SECTION RESALE INDUSTRIAL LISTING######################



class IndustrialResaleProperty(models.Model):
    # --- Step 1: Property Specs ---
    property_type = models.CharField(max_length=100, blank=True, null=True)
    land_area = models.FloatField(blank=True, null=True) # sq.ft / acres
    available_from = models.DateField(blank=True, null=True)
    power_supply = models.BooleanField(default=False)
    kva_capacity = models.IntegerField(blank=True, null=True)
    water_supply = models.CharField(max_length=50, blank=True, null=True)
    crane_heavy_machinery = models.BooleanField(default=False)
    road_connectivity = models.CharField(max_length=100, blank=True, null=True)
    worker_housing_nearby = models.BooleanField(default=False)

    # --- Step 2: Pricing & Legal ---
    expected_price = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    brokerage = models.CharField(max_length=10, blank=True, null=True)
    brokerage_percentage = models.CharField(max_length=50, blank=True, null=True)
    manual_brokerage = models.CharField(max_length=100, blank=True, null=True)
    
    sanctioning_authority = models.CharField(max_length=150, blank=True, null=True)
    ownership_type = models.CharField(max_length=100, blank=True, null=True)
    
    has_loan = models.BooleanField(default=False)
    loan_amount = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    
    existing_tenants = models.BooleanField(default=False)
    tenant_details = models.TextField(blank=True, null=True)
    
    legal_dispute = models.BooleanField(default=False)
    dispute_details = models.TextField(blank=True, null=True)
    
    tax_due = models.BooleanField(default=False)
    tax_amount = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    tax_clearance_cert = models.BooleanField(default=False)
    
    property_description = models.TextField(blank=True, null=True) # CKEditor field

    # --- Step 3: Media & Compliance ---
    compliance_docs = models.FileField(upload_to='industrial_docs/compliance/', blank=True, null=True)
    social_video = models.FileField(upload_to='industrial_docs/videos/', blank=True, null=True)

    # --- Step 4: Location & Contact ---
    city = models.CharField(max_length=100, blank=True, null=True)
    locality = models.CharField(max_length=150, blank=True, null=True)
    complete_address = models.TextField(blank=True, null=True)
    owner_name = models.CharField(max_length=150, blank=True, null=True)
    owner_contact = models.CharField(max_length=15, blank=True, null=True)
    owner_email = models.EmailField(blank=True, null=True)
    residency_status = models.CharField(max_length=50, blank=True, null=True)

    # --- Uploaded By (Session Tracking) ---
    uploaded_by_name    = models.CharField(max_length=100, blank=True, null=True)
    uploaded_by_email   = models.EmailField(blank=True, null=True)
    uploaded_by_contact = models.CharField(max_length=15, blank=True, null=True)
    uploaded_by_role    = models.CharField(max_length=50, blank=True, null=True)
    upload_file_name = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)
    
    deleted_at = models.DateTimeField(null=True, blank=True)
    deleted_by = models.CharField(max_length=150, blank=True, null=True) # 👈 ADD THIS

    def __str__(self):
        return f"{self.property_type} in {self.locality}"

class IndustrialResaleImage(models.Model):
    property = models.ForeignKey(IndustrialResaleProperty, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='industrial_docs/images/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Image for {self.property.id}"
    

##################END MODEL SECTION INDUSTRIAL RESALE LISTING################


##################START MODEL SECTION AGRICULTURAL RESALE LISTING################





def generate_agricultural_unique_property_id():
    """Generates a secure, unique alphanumeric primary key identifier."""
    return f"EFAGR-{uuid.uuid4().hex[:8].upper()}"


class AgriculturalResaleProperty(models.Model):

    # ── SYSTEM CONTROL & IDENTIFICATION ─────────────────────────────────────
    agri_property_id = models.CharField(
        max_length=20,
        primary_key=True,
        default=generate_agricultural_unique_property_id,
        editable=False,
        unique=True,
    )
    # property_title: auto-generated by save(); never filled manually by the user.
    # The form sends a preview copy via the hidden field `property_title`,
    # but the backend always re-computes the canonical value in save().
    property_title = models.CharField(max_length=255, blank=True, null=True)

    # ── STEP 1: LAND DETAILS ─────────────────────────────────────────────────
    # Exact DB column sequence:
    #   agriculture_property_type → village → taluka → district
    #   → land_area → soil_type → irrigation_facility → water_source
    #   → previous_crops → fertility_status

    agriculture_property_type = models.CharField(max_length=50)        # agriculture_land | farm_land | orchard_land
    village                   = models.CharField(max_length=100)
    taluka                    = models.CharField(max_length=100)
    district                  = models.CharField(max_length=100)

    land_area                 = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)  # Acres
    soil_type                 = models.CharField(max_length=50, blank=True, null=True)              # red | black | alluvial | loamy
    irrigation_facility       = models.CharField(max_length=10, default='no')                      # yes | no
    water_source              = models.CharField(max_length=50, blank=True, null=True)              # well | borewell | canal | river | none
    previous_crops            = models.CharField(max_length=255, blank=True, null=True)
    fertility_status          = models.CharField(max_length=20, blank=True, null=True)              # high | medium | low

    # ── STEP 2: PRICING & LEGAL ──────────────────────────────────────────────
    # Exact DB column sequence:
    #   expected_price → brokerage → brokerage_percentage → manual_brokerage
    #   → ownership_type
    #   → agri_loan → loan_amount
    #   → agri_tenants → tenant_details
    #   → agri_dispute → dispute_details
    #   → agri_tax_due → pending_tax_amount
    #   → resale_agricultural_desc

    expected_price            = models.DecimalField(max_digits=15, decimal_places=2)
    brokerage                 = models.CharField(max_length=10, blank=True, null=True)              # Yes | No
    brokerage_percentage      = models.CharField(max_length=50, blank=True, null=True)              # 1% | 1.5% | 2% | Negotiable | Manual
    manual_brokerage          = models.CharField(max_length=50, blank=True, null=True)

    ownership_type            = models.CharField(max_length=50)                                     # freehold | leasehold

    agri_loan                 = models.CharField(max_length=10, default='no')                       # yes | no
    loan_amount               = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)

    agri_tenants              = models.CharField(max_length=10, default='no')                       # yes | no
    tenant_details            = models.TextField(blank=True, null=True)

    agri_dispute              = models.CharField(max_length=10, default='no')                       # yes | no
    dispute_details           = models.TextField(blank=True, null=True)

    agri_tax_due              = models.CharField(max_length=10, default='no')                       # yes | no
    pending_tax_amount        = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)

    resale_agricultural_desc  = models.TextField()                                                  # CKEditor rich-text description

    # ── STEP 3: LOCATION & OWNER ─────────────────────────────────────────────
    # Exact DB column sequence:
    #   city → state → locality → address
    #   → owner_name → owner_contact → owner_email → comm_residency

    city                      = models.CharField(max_length=100)
    state                     = models.CharField(max_length=100)
    locality                  = models.CharField(max_length=100)
    address                   = models.TextField()

    owner_name                = models.CharField(max_length=150)
    owner_contact             = models.CharField(max_length=20)
    owner_email               = models.EmailField()
    comm_residency            = models.CharField(max_length=20, default='resident')                 # resident | nri | pio

    # ── STEP 4: DOCUMENTS & PHOTOS ───────────────────────────────────────────
    # Multiple property images are stored in the AgriculturalResaleImage child model.
    encumbrance_cert          = models.FileField(upload_to='property/docs/encumbrance/')            # Required *
    property_video            = models.FileField(upload_to='property/videos/', blank=True, null=True)

    # Audit / uploader profile trackers
    uploaded_by_name          = models.CharField(max_length=100, blank=True, null=True)
    uploaded_by_email         = models.EmailField(blank=True, null=True)
    uploaded_by_contact       = models.CharField(max_length=20, blank=True, null=True)
    uploaded_by_role          = models.CharField(max_length=50, blank=True, null=True)

    # ── SYSTEM METRIC TIMESTAMPS & SOFT-DELETE ───────────────────────────────
    created_at                = models.DateTimeField(auto_now_add=True)
    updated_at                = models.DateTimeField(auto_now=True)
    is_deleted                = models.BooleanField(default=False)
    deleted_at                = models.DateTimeField(null=True, blank=True)
    deleted_by                = models.CharField(max_length=150, blank=True, null=True)
    upload_file_name          = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        verbose_name        = "Agricultural Property"
        verbose_name_plural = "Agricultural Properties"
        ordering            = ['-created_at']

    def __str__(self):
        return f"{self.property_title or 'Agricultural Asset'} ({self.agri_property_id})"

    def save(self, *args, **kwargs):
        """
        Auto-generates property_title if not already set.
        Pattern: "{area} Fertile {type} in {village}, {taluka} ({district})"
        The frontend mirrors this logic in buildAutoTitle() for the live preview.
        """
        if not self.property_title:
            type_lbl = (
                self.agriculture_property_type.replace('_', ' ').title()
                if self.agriculture_property_type
                else "Land"
            )

            try:
                area_val = float(self.land_area)
                area_lbl = (
                    f"{int(area_val)} Acres"
                    if area_val == int(area_val)
                    else f"{area_val} Acres"
                )
            except (ValueError, TypeError):
                area_lbl = ""

            location_ctx = (
                f" in {self.village}, {self.taluka}"
                if self.village and self.taluka
                else (f" in {self.village}" if self.village else "")
            )
            district_ctx = f" ({self.district})" if self.district else ""

            raw_title = f"{area_lbl} Fertile {type_lbl}{location_ctx}{district_ctx}"
            self.property_title = " ".join(raw_title.split())   # collapse whitespace

        super().save(*args, **kwargs)


class AgriculturalResaleImage(models.Model):
    """
    Child entity for multiple property images uploaded in Step 4.
    Related to AgriculturalResaleProperty via FK (related_name='images').
    """
    property    = models.ForeignKey(
        AgriculturalResaleProperty,
        on_delete=models.CASCADE,
        related_name='images',
    )
    image       = models.ImageField(upload_to='property/images/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Image for {self.property.agri_property_id}"


##################END MODEL SECTION AGRICULTURAL RESALE LISTING################