from django.db import models
from django.utils.timezone import now
from decimal import Decimal
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

class RentalResidentialProperty(models.Model):

    # =====================================================
    # BASIC INFORMATION
    # =====================================================

    id = models.CharField(
        max_length=20,
        primary_key=True,
        default=generate_unique_rental_residential_id,
        editable=False,
        unique=True,
        blank=True
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
        return str(self.id) if self.property_title else f"Property #{self.id}"


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




# Helper function to generate the custom primary key
def generate_commercial_rental_id():
    # Uses your 6-character uppercase UUID format: EFCPR-XXXXXX
    unique_code = str(uuid.uuid4()).upper()[:6]
    return f"EFCPR-{unique_code}"


class CommercialRentalProperty(models.Model):
    # ═══════════════════════════════════════
    # SYSTEM GENERATED FIELDS
    # ═══════════════════════════════════════
    id = models.CharField(
        max_length=50, 
        primary_key=True, 
        default=generate_commercial_rental_id, 
        editable=False,
        help_text="Automated unique serial lookup tracking tag"
    )
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

    created_at = models.DateTimeField(auto_now_add=True) 
    is_deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(null=True, blank=True)
    upload_file_name = models.CharField(max_length=255, blank=True, null=True)
    upload_file_hash = models.CharField(max_length=255, blank=True, null=True)
    deleted_by = models.CharField(max_length=150, blank=True, null=True)

    def save(self, *args, **kwargs):
        # 1. Auto-generate Title
        if not self.property_title:
            condition = self.property_condition.replace('-', ' ').title() if self.property_condition else ""
            p_type = self.property_type.replace('-', ' ').title() if self.property_type else "Commercial Property"
            locality = self.area_locality.title() if self.area_locality else ""
            city_name = self.city.title() if self.city else ""
            area = f"({self.builtup_area} sq.ft.)" if self.builtup_area else ""

            title_parts = []
            if condition: title_parts.append(condition)
            title_parts.append(p_type)
            title_parts.append("for Rent in")
            if locality: title_parts.append(f"{locality},")
            if city_name: title_parts.append(city_name)
            if area: title_parts.append(area)
            self.property_title = " ".join(title_parts).strip()

        super().save(*args, **kwargs)
        
        # 2. Trigger Auto FAQ Generation
        self.generate_auto_faqs()

    def generate_auto_faqs(self):
        """Dynamic programmatic structural commercial data engine."""
        self.faqs.all().delete()
        faq_pool = []

        try: rent_val = int(float(str(self.expected_rent or 0).replace(",", "").strip()))
        except: rent_val = 0
        try: deposit_val = int(float(str(self.security_deposit or 0).replace(",", "").strip()))
        except: deposit_val = 0
        try: maint_val = int(float(str(self.maintenance_charges or 0).replace(",", "").strip()))
        except: maint_val = 0

        # FAQ 1: Financial Structure
        if rent_val > 0:
            maint_str = f" Outgoing maintenance charges are assessed at ₹{maint_val:,} per month." if maint_val > 0 else " Maintenance variables are listed as non-standard or separate obligations."
            faq_pool.append({
                "q": f"What is the lease pricing model and security deposit requirement for this {self.property_type}?",
                "a": f"The financial framework outlines a monthly operational rent of ₹{rent_val:,}. Initiating tenancy requires a security deposit outlay of ₹{deposit_val:,}.{maint_str} The option is noted as negotiable: '{self.negotiable or 'No'}'"
            })

        # FAQ 2: Area and Layout Spatial Configurations
        if self.builtup_area:
            carpet_str = f" with a highly efficient usable carpet operational area of {self.carpet_area} sq.ft." if self.carpet_area else ""
            faq_pool.append({
                "q": f"What are the total area parameters and structural placement details for this property?",
                "a": f"This property delivers a total built-up operational footprint of {self.builtup_area} sq.ft.{carpet_str} The corporate floor plate is situated on floor level {self.your_floor or '—'} out of a complete infrastructure height of {self.total_floors or '—'} levels."
            })

        # FAQ 3: Workplace Capacity Metrics
        if self.min_seats or self.cabins:
            faq_pool.append({
                "q": f"What are the workplace setup limits, seating layouts, and cabin counts?",
                "a": f"Architectural planning indicators optimize this warm/fitted shell space for a workflow setup ranging between a minimum of {self.min_seats or 0} seats up to a peak scalability limit of {self.max_seats or 0} workstation spaces. Layout specs define {self.cabins or 0} private executive cabins and {self.meeting_rooms or 0} integrated team conference/meeting rooms."
            })

        # FAQ 4: Structural Utilities and Infrastructure Compliance
        faq_pool.append({
            "q": f"What is the status of critical backup services, power links, and logistical lifts?",
            "a": f"Logistical compliance values verify that dedicated DG/UPS backup is {'fully included' if self.dg_ups_included else 'omitted/external'}. Grid electricity provision is {'bundled' if self.electricity_included else 'metered separately'}, and internal plumbing water access matches: {'bundled' if self.water_included else 'metered separately'}. Vertical workspace access handles traffic via {self.passenger_lifts or 0} high-speed passenger lifts and {self.service_lifts or 0} heavy-duty commercial cargo/service lifts."
        })

        # FAQ 5: Lease Terms and Compliance Risk Index
        if self.lockin_period or self.rent_increase:
            faq_pool.append({
                "q": f"What terms govern the baseline lock-in period and annual rental increments?",
                "a": f"The legal contractual parameters outline a standard non-termination baseline lock-in duration of {self.lockin_period or 0} months. Compounded yearly lease escalation growth schedules are pinned at an annual adjustment increase rating of {self.rent_increase or 0}%."
            })

        # FAQ 6: Logistics Hub and Zonal Planning Permissions
        if self.zone_type or self.location_hub:
            faq_pool.append({
                "q": f"Which planning zone covers this commercial structure and what is its transit hub classification?",
                "a": f"The facility is positioned within an authorized '{self.zone_type or 'Commercial'}' corporate zone type. Logistics tracking maps this real estate plot safely under a '{self.location_hub or 'Standalone/Corporate Hub'}' strategic location cluster categorization."
            })

        for item in faq_pool:
            CommercialRentalFAQ.objects.create(property=self, question=item["q"], answer=item["a"])

    def __str__(self):
        return f"{self.id} | {self.property_title}"


class CommercialRentalFAQ(models.Model):
    property = models.ForeignKey(CommercialRentalProperty, on_delete=models.CASCADE, related_name='faqs')
    question = models.CharField(max_length=255)
    answer = models.TextField()

    def __str__(self):
        return f"FAQ for {self.property.id}"

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
    id = models.CharField(max_length=20, primary_key=True, default=generate_unique_pg_property_id, editable=False, unique=True)
    property_title = models.CharField(max_length=200, blank=True, null=True, help_text="Auto-generated based on project context if empty")
    city = models.CharField(max_length=100)
    building_name = models.CharField(max_length=200, blank=True, null=True)
    locality = models.CharField(max_length=200)
    property_address = models.TextField()
    total_beds = models.IntegerField()
    pg_for = models.CharField(max_length=50)            
    furnishing_type = models.CharField(max_length=50)    
    sharing_type = models.CharField(max_length=100, blank=True, null=True)
    best_suited_for = models.CharField(max_length=100, blank=True, null=True)
    
    meals_available = models.BooleanField(default=False)
    meal_offerings = models.CharField(max_length=100, blank=True, null=True)  
    meal_speciality = models.CharField(max_length=100, blank=True, null=True)  
    
    notice_period = models.IntegerField(blank=True, null=True)
    lockin_period = models.IntegerField(blank=True, null=True)
    minimum_stay = models.IntegerField()
    available_from = models.DateField()
    property_managed_by = models.CharField(max_length=50, blank=True, null=True)
    manager_stays = models.BooleanField(default=False)

    opposite_sex_allowed = models.BooleanField(default=False)
    any_time_allowed = models.BooleanField(default=False)
    visitors_allowed = models.BooleanField(default=False)
    guardian_allowed = models.BooleanField(default=False)
    drinking_allowed = models.BooleanField(default=False)
    smoking_allowed = models.BooleanField(default=False)
    property_description = models.TextField(blank=True, null=True)
    
    amenities = models.TextField(blank=True, null=True)          
    nearby_facilities = models.TextField(blank=True, null=True)  

    video = models.FileField(upload_to='pg/videos/', blank=True, null=True)

    owner_name = models.CharField(max_length=100)
    contact_number = models.CharField(max_length=20)
    email = models.EmailField()
    alternate_contact = models.CharField(max_length=20, blank=True, null=True)

    uploaded_by_name = models.CharField(max_length=100, blank=True, null=True)
    uploaded_by_email = models.EmailField(blank=True, null=True)
    uploaded_by_contact = models.CharField(max_length=20, blank=True, null=True)
    uploaded_by_role = models.CharField(max_length=100, blank=True, null=True)

    is_deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(null=True, blank=True)
    upload_file_name = models.CharField(max_length=255, blank=True, null=True)
    deleted_by = models.CharField(max_length=150, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        # Fallback generator if title arrives empty, blank, or as string 'None'
        if not self.property_title or str(self.property_title).strip() in ["", "None", "NaN"]:
            gender_target = self.pg_for if self.pg_for else "Co-Living"
            b_name = f"{self.building_name} " if self.building_name else ""
            self.property_title = f"Premium {gender_target} PG at {b_name}{self.locality}".strip()
            
        super().save(*args, **kwargs)
        
        # Executes FAQ generation safely after database transaction commits
        transaction.on_commit(lambda: self.generate_auto_faqs())

    def generate_auto_faqs(self):
        """Safely generates programmatic standard structural FAQ metrics."""
        if not PGColivingProperty.objects.filter(pk=self.pk).exists():
            return

        faq_pool = []

        # FAQ 1: Eligibility & Setup
        faq_pool.append({
            "q": "Who is eligible to stay at this PG and what are the sharing capacities?",
            "a": f"This property is specifically designated for {self.pg_for}. It maintains a total infrastructure capacity of {self.total_beds} beds, providing {self.sharing_type or 'multiple'} room sharing configurations. The rooms are {self.furnishing_type}."
        })

        # FAQ 2: Meals
        if self.meals_available:
            faq_pool.append({
                "q": "Are food and daily meals provided to the residents?",
                "a": f"Yes, culinary services are bundled. The management provides {self.meal_offerings or 'daily meals'} maintaining a focus on {self.meal_speciality or 'standard'} dietary preferences."
            })
        else:
            faq_pool.append({
                "q": "Are food and daily meals provided to the residents?",
                "a": "No, formal meal provisioning is not included in the standard boarding package at this PG."
            })

        # FAQ 3: Policies
        faq_pool.append({
            "q": "What are the baseline legal stay requirements?",
            "a": f"Tenants must commit to a minimum operational stay of {self.minimum_stay} months. The contractual lock-in period sits at {self.lockin_period or 0} days, requiring a formal exit notice period of {self.notice_period or 0} days prior to vacating."
        })

        # FAQ 4: Rules
        rules = []
        if not self.smoking_allowed: rules.append("smoking is strictly prohibited")
        if not self.drinking_allowed: rules.append("alcohol consumption is banned")
        if not self.visitors_allowed: rules.append("external visitors are restricted")
        if self.any_time_allowed: rules.append("24/7 entry/exit access is permitted")
        
        rule_str = ", and ".join(rules).capitalize() if rules else "Standard societal housing guidelines apply."
        
        faq_pool.append({
            "q": "What are the primary lifestyle restrictions and property rules?",
            "a": f"The property enforces strict living standards to ensure comfort. {rule_str}."
        })

        # Drop old entries to prevent duplicates
        self.faqs.all().delete()

        # Batch write optimization
        PGColivingFAQ.objects.bulk_create([
            PGColivingFAQ(property=self, question=item["q"], answer=item["a"])
            for item in faq_pool
        ])

    def __str__(self):
        return f"{self.property_title} ({self.id})"


class PGColivingFAQ(models.Model):
    property = models.ForeignKey(PGColivingProperty, on_delete=models.CASCADE, related_name='faqs')
    question = models.CharField(max_length=255)
    answer = models.TextField()

    def __str__(self):
        return f"FAQ for {self.property.id}"







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
        return f"{self.room_type.capitalize()} Room - Property: {self.property.id}"


class PGPropertyImage(models.Model):
    property = models.ForeignKey(PGColivingProperty, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='pg/images/')



    ############### Models End for Rental PG_COLIVING Property  model ############################ same in this this teh rental proeprty listing model so as per add the user role in ths also and give me the view of like this residenital view for data submit  



############### Models Starts for Resale Resindential  Property  model ############################ 





# Helper function to generate the custom primary key
def generate_resale_unique_property_id():
    # Example format: EFRES-A1B2C3D4
    return f"EFRES-{uuid.uuid4().hex[:8].upper()}"


class ResaleResidentialProperty(models.Model):
    # ── SYSTEM CONTROL & IDENTIFICATION ─────────────────────
    id = models.CharField(
        max_length=50, 
        primary_key=True, 
        default=generate_resale_unique_property_id, 
        editable=False,
        help_text="Automated unique serial lookup tracking tag"
    )
    property_title = models.CharField(max_length=255, blank=True, null=True)

    # ── STEP 1: BASIC INFO & CONFIGURATION ──────────────────
    property_type = models.CharField(max_length=50) 
    zone = models.CharField(max_length=50)          
    society_type = models.CharField(max_length=50)  
    water_type = models.CharField(max_length=50)    
    furnishing_type = models.CharField(max_length=50) 
    age_of_property = models.CharField(max_length=50) 
    facing_direction = models.CharField(max_length=50)          

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
    
    loan_on_property = models.CharField(max_length=5, default='no') 
    loan_amount = models.DecimalField(max_digits=14, decimal_places=2, null=True, blank=True)
    
    existing_tenants = models.CharField(max_length=5, default='no')
    tenant_details = models.TextField(blank=True, null=True)
    
    any_legal_dispute = models.CharField(max_length=5, default='no')
    dispute_details = models.TextField(blank=True, null=True)
    
    government_tax_dues = models.CharField(max_length=5, default='no')
    pending_tax_amount = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)

    expected_price = models.DecimalField(max_digits=15, decimal_places=2)
    price_per_sqft = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True) 
    price_negotiable = models.CharField(max_length=5, default='yes') 
    
    brokerage = models.CharField(max_length=5, blank=True, null=True) 
    brokerage_percentage = models.CharField(max_length=50, blank=True, null=True) 
    manual_brokerage = models.CharField(max_length=100, blank=True, null=True)
    
    property_description = models.TextField() 

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
    owner_role = models.CharField(max_length=50, blank=True, null=True)
    residential_status = models.CharField(max_length=20) 

    # ── STEP 4: PHOTOS & PUBLISH SYSTEM ─────────────────────
    floor_plan = models.ImageField(upload_to='properties/floor_plans/', null=True, blank=True) 
    property_video = models.FileField(upload_to='properties/videos/', null=True, blank=True)

    uploaded_by_name = models.CharField(max_length=150, blank=True, null=True)
    uploaded_by_email = models.EmailField(blank=True, null=True)
    uploaded_by_contact = models.CharField(max_length=30, blank=True, null=True)
    uploaded_by_role = models.CharField(max_length=50, blank=True, null=True)
    upload_file_name = models.CharField(max_length=255, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(null=True, blank=True)
    deleted_by = models.CharField(max_length=150, null=True, blank=True)

    class Meta:
        verbose_name = 'Resale Residential Property'
        verbose_name_plural = 'Resale Residential Properties'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.property_title or 'Property Block'} ({self.id})"

    def save(self, *args, **kwargs):
        # 1. Price Per Sq.Ft calculation using Decimal fields to preserve accuracy
        if self.expected_price and self.builtup_area:
            try:
                area = Decimal(str(self.builtup_area))
                price = Decimal(str(self.expected_price))
                if area > 0:
                    self.price_per_sqft = (price / area).quantize(Decimal('0.01'))
            except (ValueError, TypeError, KeyError):
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
        
        # 3. Dynamic Automated FAQ Engine Execution
        self.generate_auto_faqs()

    def generate_auto_faqs(self):
        """Dynamic programmatic asset compliance engine for residential properties."""
        self.faqs.all().delete()
        faq_pool = []

        try: price_val = int(float(str(self.expected_price or 0).strip()))
        except: price_val = 0
        try: loan_val = int(float(str(self.loan_amount or 0).strip()))
        except: loan_val = 0
        try: tax_val = int(float(str(self.pending_tax_amount or 0).strip()))
        except: tax_val = 0
        try: per_sqft_val = int(float(str(self.price_per_sqft or 0).strip()))
        except: per_sqft_val = 0

        # FAQ 1: Financial & Valuation Structure
        if price_val > 0:
            loan_str = f" A lingering loan structure of ₹{loan_val:,} is declared against the property asset." if self.loan_on_property == 'yes' else " The property is declared free from active banking or mortgage encumbrances."
            tax_str = f" Outstanding municipal tax dues total ₹{tax_val:,}." if self.government_tax_dues == 'yes' else " No pending sovereign tax liabilities are declared."
            brokerage_str = f" Professional commission applies via a system format of {self.brokerage_percentage or self.manual_brokerage or 'standard terms'}." if self.brokerage == 'yes' else " The pricing model avoids active external brokerage terms."
            
            faq_pool.append({
                "q": f"What is the total acquisition cost, financial status, and transactional framework for this {self.bhk} residential layout?",
                "a": f"The strategic market valuation is established at ₹{price_val:,}, arriving at an estimated valuation metric of ₹{per_sqft_val:,} per sq.ft. The asset ownership confirms that price flexibility is: '{self.price_negotiable or 'No'}'.{loan_str}{tax_str}{brokerage_str}"
            })

        # FAQ 2: Architectural Spatial Profile & Inventory
        if self.builtup_area:
            plot_str = f" alongside an expansive baseline plot layout tracking at {self.plot_area} sq.ft." if self.plot_area else "."
            faq_pool.append({
                "q": "What are the structural measurement specifications and architectural interior configuration summaries?",
                "a": f"The space introduces a premium built-up area of {self.builtup_area} sq.ft. matched to a high-efficiency liveable carpet operational space of {self.carpet_area} sq.ft.{plot_str} Internal room configurations trace out a structural {self.bhk} asset layout completed with {self.bathrooms} master/guest bathrooms and {self.balconies} exterior ventilation balconies."
            })

        # FAQ 3: Property Logistics, Elevation & Essential Utilities
        faq_pool.append({
            "q": "What structural tiering, property orientation, and primary utility access lines service this residence?",
            "a": f"This residential inventory is positioned on floor level {self.floor_no} within a comprehensive residential tower footprint rising to a total height of {self.total_floors} levels. The architectural layout faces the '{self.facing_direction or 'Standard Orientation'}' compass line. Local utilities confirm an integrated '{self.water_type or 'Municipal/Borewell'}' water grid integration, set within a contextually secure '{self.society_type or 'Gated Community'}' community format."
        })

        # FAQ 4: Legal Framework, Historical Tenure & Existing Occupations
        dispute_str = f" Note: Structural tracking records details regarding legal contest/disputes: '{self.dispute_details}'." if self.any_legal_dispute == 'yes' else " The real estate title passes complete risk screening with zero pending disputes or litigations."
        tenant_str = f" The asset currently houses sitting occupants under terms: {self.tenant_details or 'Standard Tenancy'}." if self.existing_tenants == 'yes' else " The block is offered entirely vacant for seamless operational transition."
        
        faq_pool.append({
            "q": "What regulatory ownership conditions, legal checks, and occupational timelines govern this block?",
            "a": f"The legal ownership profile functions under a standard '{self.ownership_type or 'Freehold'}' deed register configuration, split across a multi-party listing headcount of {self.num_owners or 1} registered owner(s). Structural asset age tracks at '{self.age_of_property or 'New'}', with operational possession availability starting on immediate terms.{dispute_str}{tenant_str}"
        })

        # FAQ 5: Parking Distribution & Community Infrastructure
        if self.covered_parking or self.open_parking:
            faq_pool.append({
                "q": "What vehicle allocations and parking spaces are registered to this specific layout?",
                "a": f"The residential tracking matrix assigns a dedicated vehicle storage allowance, separating space variables into {self.covered_parking} secure covered parking bays and {self.open_parking} open common parking zones."
            })

        # FAQ 6: Geo-Location Framework & Feature Index
        faq_pool.append({
            "q": "Where is this asset located and what auxiliary amenities map to this residential zone?",
            "a": f"The real estate asset is situated within the corporate geographic coordinates of {self.locality}, {self.city}, cataloged inside the development project known as '{self.building_name or 'Independent Premium Block'}'. Full postal logistics resolve to: {self.complete_address}. Integrated lifestyle assets contain: {self.amenities or 'Standard Features'}, matching local connectivity points of: {self.nearby_facilities or 'Standard Locality Connections'}."
        })

        # FAQ 7: Registry Audit & Management Verification Profile
        faq_pool.append({
            "q": "Who represents this asset registry listing and what operational metadata marks its entry?",
            "a": f"The primary asset title holder is validated under the registration index of {self.owner_name} ({self.residential_status or 'Resident'}), accessible via verified contact metrics: {self.owner_contact} / {self.owner_email}. System auditing records confirm deployment management by {self.uploaded_by_name or 'System Desk'} acting in the corporate capacity of {self.uploaded_by_role or 'Listing Administrator'}, tracking under reference ID {self.id}."
        })

        for item in faq_pool:
            ResaleResidentialFAQ.objects.create(property=self, question=item["q"], answer=item["a"])


class ResaleResidentialFAQ(models.Model):
    property = models.ForeignKey(ResaleResidentialProperty, on_delete=models.CASCADE, related_name='faqs')
    question = models.CharField(max_length=255)
    answer = models.TextField()

    def __str__(self):
        return f"FAQ for Residential Property: {self.property.id}"


class ResalePropertyImage(models.Model):
    property = models.ForeignKey(ResaleResidentialProperty, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='properties/images/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Image attachment for Residential Property: {self.property.id}"


############## Models End for Resale Resindential  Property  model ############################ 




############## Models Start for Resale Commericial  Property  model ############################ 









# Helper function to generate the custom primary key
def generate_property_id():
    return f"EFCOM-{uuid.uuid4().hex[:8].upper()}"


class CommercialResaleProperty(models.Model):
    # ── SYSTEM CONTROL & IDENTIFICATION ─────────────────────
    id = models.CharField(
        max_length=50,
        primary_key=True,
        default=generate_property_id,
        editable=False,
        help_text="Automated unique serial lookup tracking tag"
    )
    property_title = models.CharField(max_length=255, blank=True, null=True)

    # ── STEP 1: BASIC INFO & SPECIFICATIONS ──────────────────
    property_type = models.CharField(max_length=50)        # office, shop, warehouse, industrial, land
    zone_type = models.CharField(max_length=50)            # industrial, commercial, residential, sez
    location_hub = models.CharField(max_length=50, blank=True, null=True)  # it, business, mall, standalone
    property_condition = models.CharField(max_length=50)   # new, excellent, good, renovation
    ownership_type = models.CharField(max_length=50)       # freehold, leasehold, cooperative
    age_of_property = models.CharField(max_length=50)      # 0-1, 1-3, 3-5, 5-10, 10+

    # Commercial Specifications
    num_staircases = models.PositiveIntegerField(default=0, blank=True, null=True)
    passenger_lifts = models.PositiveIntegerField(default=0)
    service_lifts = models.PositiveIntegerField(default=0)
    num_cabins = models.PositiveIntegerField(default=0, blank=True, null=True)
    meeting_rooms = models.PositiveIntegerField(default=0, blank=True, null=True)
    min_seats = models.PositiveIntegerField(blank=True, null=True)
    max_seats = models.PositiveIntegerField(blank=True, null=True)
    private_parking = models.PositiveIntegerField(default=0)
    public_parking = models.PositiveIntegerField(default=0, blank=True, null=True)

    # Area Measurements
    builtup_area = models.DecimalField(max_digits=12, decimal_places=2)
    carpet_area = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    plot_area = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)

    # ── STEP 2: LEGAL & PRICING DETAILS ─────────────────────
    num_owners = models.CharField(max_length=20)           # 1, 2, 3, 4+
    loan_on_property = models.CharField(max_length=5, default='no')
    loan_amount = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    existing_tenants = models.CharField(max_length=5, default='no')
    tenant_details = models.TextField(blank=True, null=True)
    any_legal_dispute = models.CharField(max_length=5, default='no')
    dispute_details = models.TextField(blank=True, null=True)
    government_tax_dues = models.CharField(max_length=5, default='no')
    pending_tax_amount = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    fire_safety_noc_available = models.CharField(max_length=5, blank=True, null=True)

    # Pricing Metrics
    brokerage = models.CharField(max_length=5, blank=True, null=True)
    brokerage_percentage = models.CharField(max_length=50, blank=True, null=True)
    manual_brokerage = models.CharField(max_length=100, blank=True, null=True)
    expected_price = models.DecimalField(max_digits=15, decimal_places=2)
    price_per_sqft = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)  # Auto-calculated in save()
    property_description = models.TextField()
    sanctioning_authority = models.TextField()

    # ── STEP 3: AMENITIES & LOCATION ────────────────────────
    nearby_facilities = models.TextField(blank=True, null=True)  # Comma-separated list
    amenities = models.TextField(blank=True, null=True)          # Comma-separated list

    city = models.CharField(max_length=100)
    area_locality = models.CharField(max_length=100)
    building_name = models.CharField(max_length=200, blank=True, null=True)
    property_address = models.TextField()

    # Contact Sequence
    owner_name = models.CharField(max_length=100)
    owner_contact = models.CharField(max_length=20)
    owner_email = models.EmailField()
    owner_role = models.CharField(max_length=100, blank=True, null=True)  # ✅ ADDED — matches form name="owner_role"
    residential_status = models.CharField(max_length=20)   # resident, nri, pio

    # ── STEP 4: PHOTOS & PUBLISH SYSTEM ─────────────────────
    floor_plan = models.ImageField(upload_to='commercial/floor_plans/', null=True, blank=True)
    property_video = models.FileField(upload_to='commercial/videos/', blank=True, null=True)

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
        return f"{self.property_title or 'Commercial Space'} ({self.id})"

    def save(self, *args, **kwargs):
        # 1. Auto-calculate price_per_sqft — never trust the form value
        if self.expected_price and self.builtup_area:
            try:
                area = float(self.builtup_area)
                price = float(self.expected_price)
                if area > 0:
                    self.price_per_sqft = round(price / area, 2)
            except (ValueError, TypeError):
                pass

        # 2. Auto-generate title if not already set
        if not self.property_title:
            type_lbl = self.property_type.replace('_', ' ').title() if self.property_type else "Commercial"
            area_lbl = f"{int(float(self.builtup_area))} Sqft" if self.builtup_area else ""
            building_ctx = f" in {self.building_name}" if self.building_name else ""
            locality_ctx = f" at {self.area_locality}, {self.city}" if self.area_locality and self.city else ""

            constructed_title = f"Premium {area_lbl} {type_lbl}{building_ctx}{locality_ctx}"
            self.property_title = " ".join(constructed_title.split())

        super().save(*args, **kwargs)

        # 3. Auto-generate FAQs after save
        self.generate_auto_faqs()

    def generate_auto_faqs(self):
        """Dynamic programmatic structural commercial data engine."""
        self.faqs.all().delete()
        faq_pool = []

        try: price_val = int(float(str(self.expected_price or 0).strip()))
        except: price_val = 0
        try: loan_val = int(float(str(self.loan_amount or 0).strip()))
        except: loan_val = 0
        try: tax_val = int(float(str(self.pending_tax_amount or 0).strip()))
        except: tax_val = 0

        # FAQ 1: Capital Structure & Transaction Parameters
        if price_val > 0:
            brokerage_details = (
                f" Managed via a designated brokerage model tracking at "
                f"{self.brokerage_percentage or self.manual_brokerage or 'standard commercial agency margins'}."
                if self.brokerage == 'Yes'
                else " Dispatched direct from corporate inventory avoiding custom external agent brokerage rules."
            )
            faq_pool.append({
                "q": f"What are the financial terms, valuation details, and fee structures for this {self.property_type}?",
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
            "a": f"This property functions safely under an official '{self.zone_type}' corporate zone designation, anchored "
                 f"structurally inside a specialized '{self.location_hub or 'Standalone/Corporate Hub'}' logistical market hub "
                 f"configuration. Structural inspection records identify the infrastructure asset age as: '{self.age_of_property}' "
                 f"years, offering structural material integrity categorized as '{self.property_condition}'."
        })

        # FAQ 4: Operational Workplace Capacity & Workflow Systems
        if self.min_seats or self.num_cabins:
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
            "a": f"Internal building traffic management handles vertical transit density utilizing {self.passenger_lifts} "
                 f"high-speed passenger elevators coupled with {self.service_lifts} dedicated heavy-duty cargo/service lift "
                 f"corridors. Emergency exit routes are maintained via {self.num_staircases or 1} strategic fire-exit staircases. "
                 f"Dedicated corporate vehicle facilities assign {self.private_parking} private executive parking slots alongside "
                 f"an auxiliary pool of {self.public_parking or 0} public common guest parking allocations."
        })

        # FAQ 6: Legal Framework, Risk Assurances & Governance Clearances
        loan_str = (f" The asset record notes an active capital mortgage balance outstanding at ₹{loan_val:,}."
                    if self.loan_on_property == 'yes'
                    else " The real estate asset title is clear of any active corporate banking liens or mortgage holds.")
        tenant_str = (f" Core operations note a pre-existing lease structure holding existing occupants: "
                      f"{self.tenant_details or 'Occupied under business terms'}."
                      if self.existing_tenants == 'yes'
                      else " The property features clear vacant possession for rapid enterprise deployment.")
        dispute_str = (f" Critical Note: Listing file logs ongoing legal actions or dispute data: '{self.dispute_details}'."
                       if self.any_legal_dispute == 'yes'
                       else " Continuous background checks verify clean legal titles with zero active litigation risks.")
        tax_str = (f" Sovereign records indicate a trailing tax balance due at ₹{tax_val:,}."
                   if self.government_tax_dues == 'yes'
                   else " All local municipal property taxes are verified as fully settled.")

        faq_pool.append({
            "q": "What liability statements, tenant parameters, and legal clearances protect this commercial deed?",
            "a": f"The registry asset operates under a clean '{self.ownership_type}' deed format, verified against a registered "
                 f"title ownership count of {self.num_owners} signature holder(s). Operational compliance confirms that local fire "
                 f"marshal Fire NOC protection is: '{self.fire_safety_noc_available or 'Pending/Not Declared'}'."
                 f"{loan_str}{tenant_str}{dispute_str}{tax_str}"
        })

        # FAQ 7: Local Approvals, Corporate Context & Master Planning Authorities
        faq_pool.append({
            "q": "Which municipal board authorizes this property and what general development summary protects its use?",
            "a": f"The regulatory framework and layout patterns are fully verified by the authorized "
                 f"'{self.sanctioning_authority or 'Local Planning Board'}' board. Technical usage boundaries track to the "
                 f"following master plan description guidelines: {self.property_description}."
        })

        # FAQ 8: Geographic Address Mapping & Title Management Index
        faq_pool.append({
            "q": "What is the precise location address data and title verification identity for this commercial inventory?",
            "a": f"The site location resolves to the commercial sectors of {self.area_locality}, {self.city}, tracking inside the "
                 f"business infrastructure complex mapped as '{self.building_name or 'Premium Corporate Standalone Structure'}'. "
                 f"Detailed physical address lines settle to: {self.property_address}. The main stakeholder title is mapped to "
                 f"corporate entity {self.owner_name} ({self.residential_status}), with corporate lines running via "
                 f"{self.owner_contact} / {self.owner_email}. Technical database file tracking lists asset code {self.id} with "
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
    """Child entity designed to capture dynamic image collections handled during form Step 4."""
    property = models.ForeignKey(
        CommercialResaleProperty,
        on_delete=models.CASCADE,
        related_name='images'
    )
    image = models.ImageField(upload_to='commercial/images/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Image attachment for Commercial ID: {self.property.id}"





############## Models End for Resale Commericial  Property  model ############################ 

#########################Start Model of RESALE PLOT LISTING####################3





def generate_resale_unique_property_id():
    return f"EFPLT-{uuid.uuid4().hex[:8].upper()}"

class PlotSaleProperty(models.Model):
    id = models.CharField(
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

    # ── STEP 3: Media & Certificates ─────────────────────────────
    encumbrance_cert  = models.FileField(upload_to='plot_docs/certificates/', null=True, blank=True)
    social_video      = models.FileField(upload_to='plot_docs/videos/', blank=True, null=True)

    # ── STEP 4: Location & Contact ────────────────────────────────
    plot_city          = models.CharField(max_length=100)
    plot_locality      = models.CharField(max_length=150)
    plot_address       = models.TextField()

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

    def save(self, *args, **kwargs):
        # Auto-calculate price per sqft (Kept exact backend handling)
        if self.plot_price and self.plot_area:
            try:
                area  = float(self.plot_area)
                price = float(self.plot_price)
                if area > 0:
                    self.price_per_sqft = round(price / area, 2)
            except (ValueError, TypeError):
                pass

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

        super().save(*args, **kwargs)
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
    property_title = models.CharField(max_length=255, blank=True, null=True)

    # ── STEP 1: PROPERTY SPECS ────────────────────────────────────────
    property_type         = models.CharField(max_length=100, null=True, blank=True)
    land_area             = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    
    power_supply          = models.BooleanField(default=False)
    kva_capacity          = models.IntegerField(blank=True, null=True)
    water_supply          = models.CharField(max_length=50, blank=True, null=True)
    crane_heavy_machinery = models.BooleanField(default=False)
    road_connectivity     = models.CharField(max_length=100, blank=True, null=True)
    worker_housing_nearby = models.BooleanField(default=False)

    # ── STEP 2: PRICING & LEGAL ───────────────────────────────────────
    expected_price        = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    # Added new database field for tracking cost metric strings within FAQ formatting logic
    price_per_sqft        = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    brokerage             = models.CharField(max_length=10, default='No')
    brokerage_percentage  = models.CharField(max_length=50, blank=True, null=True)
    manual_brokerage      = models.CharField(max_length=100, blank=True, null=True)
    sanctioning_authority = models.CharField(max_length=150, blank=True, null=True)
    ownership_type        = models.CharField(max_length=100, null=True, blank=True)

    loan_on_property      = models.BooleanField(default=False)
    loan_amount           = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    existing_tenants      = models.BooleanField(default=False)
    tenant_details        = models.TextField(blank=True, null=True)
    legal_dispute         = models.BooleanField(default=False)
    dispute_details       = models.TextField(blank=True, null=True)
    government_tax_dues   = models.BooleanField(default=False)
    tax_amount            = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    tax_clearance_cert    = models.BooleanField(default=False)
    property_description  = models.TextField(null=True, blank=True)

    # ── STEP 3: MEDIA & COMPLIANCE ───────────────────────────────────
    compliance_docs = models.FileField(upload_to='industrial_docs/compliance/', blank=True, null=True)
    social_video    = models.FileField(upload_to='industrial_docs/videos/', blank=True, null=True)

    # ── STEP 4: LOCATION & CONTACT ───────────────────────────────────
    city             = models.CharField(max_length=100, blank=True, null=True)
    locality_area    = models.CharField(max_length=150, null=True, blank=True)
    Property_address = models.TextField(blank=True, null=True)

    owner_name       = models.CharField(max_length=150, null=True, blank=True)
    owner_contact    = models.CharField(max_length=20, null=True, blank=True)
    owner_email      = models.EmailField(blank=True, null=True)
    owner_role       = models.CharField(max_length=20, null=True, blank=True)
    residency_status = models.CharField(max_length=50, null=True, blank=True)

    # ── UPLOADER Details ─────────────────────────────────────────────
    uploaded_by_name    = models.CharField(max_length=100, blank=True, null=True)
    uploaded_by_role    = models.CharField(max_length=50, blank=True, null=True)
    uploaded_by_email   = models.EmailField(blank=True, null=True)
    uploaded_by_contact = models.CharField(max_length=30, blank=True, null=True)
    upload_file_name    = models.CharField(max_length=255, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(null=True, blank=True)
    deleted_by = models.CharField(max_length=150, blank=True, null=True)

    class Meta:
        verbose_name        = "Industrial Property"
        verbose_name_plural = "Industrial Properties"
        ordering            = ['-created_at']

    def __str__(self):
        return self.property_title or f"Industrial #{self.id}"

    # ── AUTO-FAQ GENERATOR (UPDATED FOR DYNAMIC PRICING AND INTEGRATION)
    def generate_auto_faqs(self):
        self.faqs.all().delete()
        faq_pool = []

        def safe_money(val):
            try:
                v = int(float(str(val or 0).replace(",", "").strip()))
                return f"Rs.{v:,}" if v else None
            except Exception:
                return None

        price_str = safe_money(self.expected_price)
        loan_str  = safe_money(self.loan_amount)
        tax_str   = safe_money(self.tax_amount)
        per_sqft_str = safe_money(self.price_per_sqft)

        # FAQ 1 — Core Specs (Fixed self.locality reference to self.locality_area)
        faq_pool.append({
            "question": "What is the total land area and specific property type of this industrial asset?",
            "answer": (
                f"This is an industrial {self.property_type or 'facility'} with a total land area of "
                f"{self.land_area or 'unspecified'} Sqft, situated in "
                f"{self.locality_area or 'the listed area'}, {self.city or 'city'}. "
                
            )
        })

        # FAQ 2 — Pricing & Brokerage 
        brokerage_text = (
            f"A brokerage of {self.brokerage_percentage} applies."
            if str(self.brokerage or '').lower() in ['yes', 'true', '1']
            else "There is no brokerage applicable for this transaction."
        )
        faq_pool.append({
            "question": "What is the expected price and brokerage structure for this property?",
            "answer": (
                f"The expected sale price for this industrial property is {price_str or 'available on request'}. "
                + (f"This matches roughly {per_sqft_str} per Sqft. " if per_sqft_str else "")
                + brokerage_text
                + (f" Manual brokerage details: {self.manual_brokerage}." if self.manual_brokerage else "")
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

        # FAQ 4 — Crane / Heavy Machinery
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

        # FAQ 5 — Road Connectivity
        faq_pool.append({
            "question": "How is the road connectivity for heavy transport and logistics operations?",
            "answer": (
                f"The property benefits from {self.road_connectivity or 'standard'} road connectivity, "
                f"providing efficient access for heavy trucks, container vehicles, and regular material "
                f"logistics. This makes it operationally viable for round-the-clock industrial supply chains."
            )
        })

        # FAQ 6 — Worker Housing
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

        # FAQ 7 — Water Supply
        faq_pool.append({
            "question": "What is the status and type of water supply available for industrial operations?",
            "answer": (
                f"The property utilises a {self.water_supply or 'standard municipal'} water supply system. "
                f"This is suitable for the current operational scope and can support standard industrial "
                f"washing, cooling, and processing requirements."
            )
        })

        # FAQ 8 — Legal Dispute & Tax (Fixed self.tax_due to self.government_tax_dues)
        dispute_text = (
            f"There is an active legal dispute on record: {self.dispute_details}. "
            if self.legal_dispute else
            "The property title is completely clear of any legal disputes or encumbrances. "
        )
        tax_text = (
            f"There are pending municipal/property tax dues amounting to {tax_str}."
            if self.government_tax_dues else
            "All property and municipal taxes are fully cleared and up to date."
        )
        faq_pool.append({
            "question": "Are there any pending legal disputes or outstanding tax dues on this property?",
            "answer": dispute_text + tax_text
        })

        # FAQ 9 — Loan / Mortgage (Fixed self.has_loan to self.loan_on_property)
        faq_pool.append({
            "question": "Is there any active financial loan or mortgage registered against this property?",
            "answer": (
                f"Yes, there is an active loan/mortgage of {loan_str} currently registered against this "
                f"property. Buyers should account for this encumbrance during title verification and "
                f"financing arrangements."
                if self.loan_on_property else
                "No, there are no active financial loans or mortgages registered against this property. "
                "The title is free of any banking or financial institution encumbrances."
            )
        })

        # FAQ 10 — Ownership & Tenants
        ownership_text = (
            f"The property is held under {self.ownership_type or 'standard'} ownership"
            + (f", sanctioned by {self.sanctioning_authority}" if self.sanctioning_authority else "")
            + ". "
        )
        tenant_text = (
            f"The property currently has active tenants. Details: {self.tenant_details}."
            if self.existing_tenants else
            "The property is completely vacant with no existing tenants, enabling immediate possession."
        )
        faq_pool.append({
            "question": "What is the ownership structure, and are there any existing tenants currently occupying this space?",
            "answer": ownership_text + tenant_text
        })

        IndustrialResaleFAQ.objects.bulk_create([
            IndustrialResaleFAQ(property=self, question=f["question"], answer=f["answer"])
            for f in faq_pool
        ])

    # ── SAVE OVERRIDE ────────────────────────────────────────────────
    def save(self, *args, **kwargs):
        # 1. New Calculation: Auto-generate internal price per sq ft values
        if self.expected_price and self.land_area:
            try:
                area = float(self.land_area)
                price = float(self.expected_price)
                if area > 0:
                    self.price_per_sqft = round(price / area, 2)
            except (ValueError, TypeError):
                pass

        # 2. Auto-generate property_title if not yet assigned
        if not self.property_title:
            type_lbl = (
                self.property_type.replace('_', ' ').title()
                if self.property_type else "Industrial Asset"
            )
            try:
                area_val = float(self.land_area)
                area_lbl = (
                    f"{int(area_val):,} Sqft"
                    if area_val == int(area_val)
                    else f"{area_val:,} Sqft"
                )
            except (ValueError, TypeError):
                area_lbl = ""
                
            # Fixed self.locality to self.locality_area
            locality_ctx = f" in {self.locality_area}" if self.locality_area else ""
            city_ctx     = f", {self.city}" if self.city else ""
            self.property_title = " ".join(
                f"Industrial {area_lbl} {type_lbl}{locality_ctx}{city_ctx}".split()
            )

        # 3. Save record instance context
        super().save(*args, **kwargs)

        # 4. Build linked child FAQs
        self.generate_auto_faqs()

# ══════════════════════════════════════════════════════════════════════
#  MODEL 2 — IndustrialResaleImage
# ══════════════════════════════════════════════════════════════════════

class IndustrialResaleImage(models.Model):
    property    = models.ForeignKey(
        IndustrialResaleProperty,
        on_delete=models.CASCADE,
        related_name='images'
    )
    image       = models.ImageField(upload_to='industrial_docs/images/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['uploaded_at']

    def __str__(self):
        # Changed to reference self.property.id
        return f"Image for {self.property.id}"


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
    property_title = models.CharField(max_length=255, blank=True, null=True) 

    # ── STEP 1: LAND DETAILS ──────────────────────────────────────
    agriculture_property_type = models.CharField(max_length=50)
    land_area          = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    village                   = models.CharField(max_length=100)
    taluka                    = models.CharField(max_length=100)
    district                  = models.CharField(max_length=100)

    soil_type          = models.CharField(max_length=50, blank=True, null=True)
    irrigation_facility_active = models.CharField(max_length=10, default='no') 
    water_source_infrastructure      = models.CharField(max_length=50, blank=True, null=True) 
    fertility_status   = models.CharField(max_length=20, blank=True, null=True)
    previous_crops     = models.CharField(max_length=255, blank=True, null=True)

    # ── STEP 2: PRICING & LEGAL ───────────────────────────────────
    expected_price       = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    price_per_acre       = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    brokerage            = models.CharField(max_length=10, blank=True, null=True)
    brokerage_percentage = models.CharField(max_length=50, blank=True, null=True)
    manual_brokerage     = models.CharField(max_length=50, blank=True, null=True)

    ownership_type       = models.CharField(max_length=50)

    loan_on_property     = models.CharField(max_length=10, default='no')
    loan_amount          = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    existing_tenants     = models.CharField(max_length=10, default='no')
    tenant_details       = models.TextField(blank=True, null=True)
    agri_dispute         = models.CharField(max_length=10, default='no')
    dispute_details      = models.TextField(blank=True, null=True)
    pending_tax_due      = models.CharField(max_length=10, default='no')
    pending_tax_amount   = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)

    resale_agricultural_desc = models.TextField()

    # ── STEP 3: LOCATION & OWNER ──────────────────────────────────
    city     = models.CharField(max_length=100)
    state    = models.CharField(max_length=100)
    locality_area = models.CharField(max_length=100, blank=True, null=True)
    property_address  = models.TextField()

    owner_name     = models.CharField(max_length=150)
    owner_contact  = models.CharField(max_length=20)
    owner_email    = models.EmailField()
    owner_role    =  models.CharField(max_length=100, blank=True, null=True)
    residency_status = models.CharField(max_length=20, default='resident')

    # ── STEP 4: DOCUMENTS & PHOTOS ────────────────────────────────
    encumbrance_cert = models.FileField(upload_to='property/docs/encumbrance/', null=True, blank=True)
    property_video   = models.FileField(upload_to='property/videos/', blank=True, null=True)

    # ── UPLOADER / AUDIT ─────────────────────────────────────────
    uploaded_by_name    = models.CharField(max_length=100, blank=True, null=True)
    uploaded_by_email   = models.EmailField(blank=True, null=True)
    uploaded_by_contact = models.CharField(max_length=20, blank=True, null=True)
    uploaded_by_role    = models.CharField(max_length=50, blank=True, null=True)

    created_at       = models.DateTimeField(auto_now_add=True)
    updated_at       = models.DateTimeField(auto_now=True)
    is_deleted       = models.BooleanField(default=False)
    deleted_at       = models.DateTimeField(null=True, blank=True)
    deleted_by       = models.CharField(max_length=150, blank=True, null=True)
    upload_file_name = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        verbose_name        = "Agricultural Property"
        verbose_name_plural = "Agricultural Properties"
        ordering            = ['-created_at']

    def __str__(self):
        return f"{self.property_title or 'Agricultural Property'} ({self.id})"

    # ── AUTO-FAQ GENERATOR (FIXED MISALIGNED FIELDS) ──────────────
    def generate_auto_faqs(self):
        self.faqs.all().delete()
        faq_pool = []

        def safe_money(val):
            try:
                v = int(float(str(val or 0).replace(",", "").strip()))
                return f"Rs.{v:,}" if v else None
            except Exception:
                return None

        price_str     = safe_money(self.expected_price)
        loan_str      = safe_money(self.loan_amount)
        tax_str       = safe_money(self.pending_tax_amount)
        per_acre_str  = safe_money(self.price_per_acre)

        # FAQ 1 — Core Land Details
        faq_pool.append({
            "question": "What is the total land area, property type, and exact location of this agricultural property?",
            "answer": (
                f"This is a {self.agriculture_property_type.replace('_',' ').title() if self.agriculture_property_type else 'agricultural'} "
                f"land parcel spanning {self.land_area or 'unspecified'} Acres, situated in the village of "
                f"{self.village or '—'}, Taluka {self.taluka or '—'}, District {self.district or '—'}, {self.state or ''}."
            )
        })

        # FAQ 2 — Pricing & Brokerage (Upgraded with auto per-acre values)
        brokerage_text = (
            f"A brokerage of {self.brokerage_percentage} applies."
            if str(self.brokerage or '').lower() in ['yes', 'true', '1']
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
                + (f"There is an active legal dispute on record: {self.dispute_details}. Buyers must verify status before proceeding."
                   if str(self.agri_dispute or '').lower() == 'yes' else
                   "The title is completely clear of any legal disputes or encumbrances.")
            )
        })

        # FAQ 6 — Tax & Loan (Fixed field references)
        tax_text = (
            f"There are pending land/revenue tax dues amounting to {tax_str}."
            if str(self.pending_tax_due or '').lower() == 'yes' else
            "All revenue and land taxes are fully cleared and up to date."
        )
        loan_text = (
            f"Yes, there is an active agricultural loan of {loan_str} registered against this property. "
            f"Buyers should account for this during title transfer."
            if str(self.loan_on_property or '').lower() == 'yes' else
            "No active loans or mortgages are registered against this land."
        )
        faq_pool.append({
            "question": "Are there any pending tax dues or active loans registered against this agricultural property?",
            "answer": tax_text + " " + loan_text
        })

        # FAQ 7 — Tenants / Lease (Fixed field reference)
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
                f"This {self.agriculture_property_type.replace('_',' ').title() if self.agriculture_property_type else 'agricultural'} "
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
    def save(self, *args, **kwargs):
        # 1. Auto-generate price per acre values
        if self.expected_price and self.land_area:
            try:
                area  = float(self.land_area)
                price = float(self.expected_price)
                if area > 0:
                    self.price_per_acre = round(price / area, 2)
            except (ValueError, TypeError):
                pass

        # 2. Auto-generate property_title
        if not self.property_title:
            type_lbl = self.agriculture_property_type.replace('_', ' ').title() if self.agriculture_property_type else "Land"
            try:
                area_val = float(self.land_area)
                area_lbl = f"{int(area_val)} Acres" if area_val == int(area_val) else f"{area_val} Acres"
            except (ValueError, TypeError):
                area_lbl = ""
            location_ctx = f" in {self.village}, {self.taluka}" if self.village and self.taluka else ""
            district_ctx = f" ({self.district})" if self.district else ""
            self.property_title = " ".join(f"{area_lbl} Fertile {type_lbl}{location_ctx}{district_ctx}".split())

        super().save(*args, **kwargs)

        # 3. Regenerate all FAQs on every create & update
        self.generate_auto_faqs()

# ══════════════════════════════════════════════════════════════════
#  MODEL 2 — AgriculturalResaleImage
# ══════════════════════════════════════════════════════════════════

class AgriculturalResaleImage(models.Model):
    property    = models.ForeignKey(AgriculturalResaleProperty, related_name='images', on_delete=models.CASCADE)
    image       = models.ImageField(upload_to='property/images/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['uploaded_at']

    def __str__(self):
        # Adjusted to reference the new ID field
        return f"Image for {self.property.id}"


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



##################END MODEL SECTION AGRICULTURAL RESALE LISTING################