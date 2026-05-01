from django.db import models



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



class FAQ(models.Model):
    question = models.CharField(max_length=255)
    answer = models.TextField()  # Will use CKEditor widget
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.question
    
    
    


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

        
    

################################START MODEL SECTION OF THE RENTAL RESIDENTIAL LISTING####################

class RentalResidentialProperty(models.Model):
    # -------------------------
    # Basic Information
    # -------------------------
    property_title = models.CharField(max_length=255, blank=True, null=True)
    property_purpose = models.CharField(max_length=50, blank=True, null=True)
    property_type = models.CharField(max_length=100, blank=True, null=True)
    bhk_type = models.CharField(max_length=50, blank=True, null=True)
    renting_option = models.CharField(max_length=50, blank=True, null=True)
    furnishing_status = models.CharField(max_length=50, blank=True, null=True)
    available_for = models.CharField(max_length=50, blank=True, null=True)
    built_up_area = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    bathrooms = models.IntegerField(blank=True, null=True)
    balconies = models.IntegerField(blank=True, null=True)
    floor_number = models.CharField(max_length=50, blank=True, null=True)
    total_floors = models.IntegerField(blank=True, null=True)
    facing = models.CharField(max_length=50, blank=True, null=True)

    # -------------------------
    # Property Details
    # -------------------------
    zone = models.CharField(max_length=50, blank=True, null=True)
    ownership_type = models.CharField(max_length=50, blank=True, null=True)
    construction_status = models.CharField(max_length=50, blank=True, null=True)
    property_age = models.CharField(max_length=50, blank=True, null=True)
    carpet_area = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    plot_area = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    building_name = models.CharField(max_length=200, blank=True, null=True)

    # -------------------------
    # Availability
    # -------------------------
    possession_status = models.CharField(max_length=50, blank=True, null=True)
    available_from = models.DateField(blank=True, null=True)
    lease_duration = models.CharField(max_length=50, blank=True, null=True)
    brokerage = models.CharField(max_length=10, blank=True, null=True)
    brokerage_percentage = models.CharField(max_length=20, blank=True, null=True)
    manual_brokerage = models.CharField(max_length=20, blank=True, null=True)

    # -------------------------
    # Pricing
    # -------------------------
    monthly_rent = models.BigIntegerField(blank=True, null=True)
    security_deposit = models.BigIntegerField(blank=True, null=True)
    maintenance_type = models.CharField(max_length=50, blank=True, null=True)
    maintenance_amount = models.BigIntegerField(blank=True, null=True)
    expected_price = models.BigIntegerField(blank=True, null=True)

    # -------------------------
    # Location
    # -------------------------
    address = models.TextField(blank=True, null=True)
    city = models.CharField(max_length=150, blank=True, null=True)
    locality = models.CharField(max_length=150, blank=True, null=True)
    state = models.CharField(max_length=150, blank=True, null=True)
    pincode = models.CharField(max_length=10, blank=True, null=True)
    road_connectivity = models.CharField(max_length=150, blank=True, null=True)

    # -------------------------
    # Amenities & Facilities 
    # -------------------------
    amenities = models.TextField(blank=True, null=True)
    facilities = models.TextField(blank=True, null=True)

    # -------------------------
    # Description
    # -------------------------
    description = models.TextField(blank=True, null=True)
    rent_residential_desc = models.TextField(blank=True, null=True)

    # -------------------------
    # Owner Details
    # -------------------------
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

    def __str__(self):
        return str(self.property_title) if self.property_title else f"Property #{self.id}"

# ==========================================
# ✅ NEW MODEL FOR IMAGES
# ==========================================
class RentalResidentialImage(models.Model):
    property = models.ForeignKey(RentalResidentialProperty, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to="residential_rent/")
    
    def __str__(self):
        return f"Image for {self.property.id}"



################################END MODEL SECTION OF THE RENTAL RESIDENTIAL LISTING####################


############### Models Starts for Rental COMMERCIAL Property  model ############################ same in this this teh rental proeprty listing model so as per add the user role in ths also and give me the view of like this residenital view for data submit  



class CommercialRentalProperty(models.Model):

    property_type = models.CharField(max_length=50)
    city = models.CharField(max_length=100)
    area_locality = models.CharField(max_length=200)
    property_address = models.TextField()
    building_name = models.CharField(max_length=200)

    possession_status = models.CharField(max_length=50)
    available_from = models.DateField(blank=True, null=True)
    age_of_property = models.CharField(max_length=20)

    zone_type = models.CharField(max_length=50, blank=True, null=True)
    location_hub = models.CharField(max_length=50, blank=True, null=True)

    property_condition = models.CharField(max_length=50)
    ownership_type = models.CharField(max_length=50)
    construction_status = models.CharField(max_length=20, blank=True, null=True)

    # AREA
    builtup_area = models.IntegerField()
    carpet_area = models.IntegerField(blank=True, null=True)
    expected_rent = models.IntegerField()

    security_deposit = models.IntegerField(blank=True, null=True)
    maintenance_charges = models.IntegerField(blank=True, null=True)

    negotiable = models.BooleanField(default=False)

    brokerage = models.CharField(max_length=5, blank=True, null=True)
    brokerage_percentage = models.CharField(max_length=20, blank=True, null=True)
    manual_brokerage = models.CharField(max_length=50, blank=True, null=True)

    # UTILITIES
    dg_ups_included = models.BooleanField(default=False)
    electricity_included = models.BooleanField(default=False)
    water_included = models.BooleanField(default=False)

    lockin_period = models.IntegerField(blank=True, null=True)
    rent_increase = models.FloatField(blank=True, null=True)

    # BUILDING
    total_floors = models.IntegerField(blank=True, null=True)
    your_floor = models.IntegerField(blank=True, null=True)
    staircases = models.IntegerField(blank=True, null=True)

    passenger_lifts = models.IntegerField(default=0)
    service_lifts = models.IntegerField(default=0)
    private_parking = models.IntegerField(default=0)

    # OFFICE
    min_seats = models.IntegerField(blank=True, null=True)
    max_seats = models.IntegerField(blank=True, null=True)
    cabins = models.IntegerField(blank=True, null=True)
    meeting_rooms = models.IntegerField(blank=True, null=True)

    private_washroom = models.IntegerField(default=0)
    public_washroom = models.IntegerField(default=0)

    flooring_type = models.CharField(max_length=50, blank=True, null=True)

    # ✅ LIST DATA
    amenities = models.JSONField(blank=True, null=True)
    nearby_facilities = models.JSONField(blank=True, null=True)

    # MEDIA (only floor plan + video here)
    floor_plan = models.ImageField(upload_to='commercial_rent/floorplan/', blank=True, null=True)
    video = models.FileField(upload_to='commercial_rent/videos/', blank=True, null=True)

    # OWNER
    owner_name = models.CharField(max_length=100)
    contact_number = models.CharField(max_length=20)
    email = models.EmailField()
    alternate_contact = models.CharField(max_length=20, blank=True, null=True)

    # UPLOADER
    uploaded_by_name = models.CharField(max_length=100, blank=True, null=True)
    uploaded_by_email = models.EmailField(blank=True, null=True)
    uploaded_by_contact = models.CharField(max_length=20, blank=True, null=True)
    uploaded_by_role = models.CharField(max_length=100, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.property_type} - {self.city}"


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




class PGColivingProperty(models.Model):

    # BASIC
    city = models.CharField(max_length=100)
    building_name = models.CharField(max_length=200, blank=True, null=True)
    locality = models.CharField(max_length=200)
    pg_name = models.CharField(max_length=200)
    property_address = models.TextField()

    total_beds = models.IntegerField()

    pg_for = models.CharField(max_length=20)
    furnishing_type = models.CharField(max_length=20)
    sharing_type = models.CharField(max_length=50, blank=True, null=True)
    best_suited_for = models.CharField(max_length=50, blank=True, null=True)

    # ✅ ROOMS STORED AS TEXT (IMPORTANT CHANGE)
    room_details = models.TextField(default="", blank=True)

    # FACILITIES
    common_area = models.TextField(blank=True, null=True)
    amenities = models.TextField(blank=True, null=True)
    nearby_facilities = models.TextField(blank=True, null=True)

    # MEALS
    meals_available = models.BooleanField(default=False)
    meal_offerings = models.CharField(max_length=100, blank=True, null=True)
    meal_speciality = models.CharField(max_length=50, blank=True, null=True)

    # RULES
    notice_period = models.IntegerField(blank=True, null=True)
    lockin_period = models.IntegerField(blank=True, null=True)
    minimum_stay = models.IntegerField()
    available_from = models.DateField()

    property_managed_by = models.CharField(max_length=20, blank=True, null=True)
    manager_stays = models.BooleanField(default=False)

    non_veg_allowed = models.BooleanField(default=False)
    opposite_sex_allowed = models.BooleanField(default=False)
    any_time_allowed = models.BooleanField(default=False)
    visitors_allowed = models.BooleanField(default=False)
    guardian_allowed = models.BooleanField(default=False)
    drinking_allowed = models.BooleanField(default=False)
    smoking_allowed = models.BooleanField(default=False)

    # MEDIA
    floor_plan = models.ImageField(upload_to='pg/floorplans/', blank=True, null=True)
    video = models.FileField(upload_to='pg/videos/', blank=True, null=True)

    # CONTACT
    owner_name = models.CharField(max_length=100)
    contact_number = models.CharField(max_length=20)
    email = models.EmailField()
    alternate_contact = models.CharField(max_length=20, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)



class PGPropertyImage(models.Model):
    property = models.ForeignKey(PGColivingProperty, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='pg/images/')





    ############### Models End for Rental PG_COLIVING Property  model ############################ same in this this teh rental proeprty listing model so as per add the user role in ths also and give me the view of like this residenital view for data submit  



############### Models Starts for Resale Resindential  Property  model ############################ 




PROPERTY_TYPE_CHOICES = [
    ('apartment', 'Apartment'),
    ('house', 'Independent House/Villa'),
    ('floor', 'Independent Floor'),
    ('plot', 'Plot/Land'),
]
ZONE_CHOICES = [
    ('north', 'North Zone'), ('south', 'South Zone'),
    ('east', 'East Zone'),   ('west', 'West Zone'), ('central', 'Central Zone'),
]
SOCIETY_TYPE_CHOICES = [
    ('gated', 'Gated Community'), ('open', 'Open Society'),
    ('cooperative', 'Co-operative Housing'), ('apartment', 'Apartment Complex'),
]
WATER_TYPE_CHOICES = [
    ('municipal', 'Municipal Corporation'), ('borewell', 'Borewell'), ('both', 'Both'),
]
FURNISHING_CHOICES = [
    ('unfurnished', 'Unfurnished'), ('semi', 'Semi-Furnished'), ('fully', 'Fully Furnished'),
]
AGE_CHOICES = [
    ('0-1', '0-1 Year'), ('1-3', '1-3 Years'), ('3-5', '3-5 Years'),
    ('5-10', '5-10 Years'), ('10+', '10+ Years'),
]
FACING_CHOICES = [
    ('North','North'), ('South','South'), ('East','East'), ('West','West'),
    ('North-East','North-East'), ('North-West','North-West'),
    ('South-East','South-East'), ('South-West','South-West'),
]
BHK_CHOICES = [
    ('1rk','1 RK'), ('1bhk','1 BHK'), ('2bhk','2 BHK'),
    ('3bhk','3 BHK'), ('4bhk','4 BHK'), ('5+bhk','5+ BHK'),
]
OWNERSHIP_TYPE_CHOICES = [
    ('freehold','Freehold'), ('leasehold','Leasehold'),
    ('cooperative','Co-operative'), ('poa','Power of Attorney'),
]
NUM_OWNERS_CHOICES = [
    ('1','Single Owner'), ('2','2 Owners'), ('3','3 Owners'), ('4+','4+ Owners'),
]
NEGOTIABLE_CHOICES    = [('yes','Yes'), ('no','No - Fixed')]
BROKERAGE_CHOICES     = [('Yes','Yes'), ('No','No')]
BROKERAGE_PERCENTAGE_CHOICES = [
    ('1%','1%'), ('1.5%','1.5%'), ('2%','2%'),
    ('Negotiable','Negotiable'), ('Manual','Enter Manually'),
]
RESIDENTIAL_STATUS_CHOICES = [
    ('resident','Resident'), ('nri','NRI'), ('pio','PIO'),
]
UPLOADER_ROLE_CHOICES = [
    ('admin','Admin'), ('agent','Agent'), ('staff','Staff'), ('owner','Owner'),
]


class ResaleResidentialProperty(models.Model):

    # ── Basic Information ──────────────────────────────────
    title            = models.CharField(max_length=255)          # hidden field in form ✓
    property_type    = models.CharField(max_length=20, choices=PROPERTY_TYPE_CHOICES)
    zone             = models.CharField(max_length=20, choices=ZONE_CHOICES)
    society_type     = models.CharField(max_length=20, choices=SOCIETY_TYPE_CHOICES)
    water_type       = models.CharField(max_length=20, choices=WATER_TYPE_CHOICES)
    furnishing_type  = models.CharField(max_length=20, choices=FURNISHING_CHOICES)
    age_of_property  = models.CharField(max_length=10, choices=AGE_CHOICES)
    facing           = models.CharField(max_length=15, choices=FACING_CHOICES)
    available_from   = models.DateField(null=True, blank=True)

    # ── Property Configuration ─────────────────────────────
    bhk              = models.CharField(max_length=10, choices=BHK_CHOICES)
    bathrooms        = models.PositiveIntegerField(default=1)
    balconies        = models.PositiveIntegerField(default=0)
    covered_parking  = models.PositiveIntegerField(default=0)
    open_parking     = models.PositiveIntegerField(default=0)

    # ── Property Measurements ──────────────────────────────
    builtup_area     = models.DecimalField(max_digits=10, decimal_places=2)
    carpet_area      = models.DecimalField(max_digits=10, decimal_places=2)
    plot_area        = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    floor_no         = models.PositiveIntegerField()
    total_floors     = models.PositiveIntegerField()

    # ── Ownership & Legal ──────────────────────────────────
    ownership_type       = models.CharField(max_length=20, choices=OWNERSHIP_TYPE_CHOICES)
    num_owners           = models.CharField(max_length=5, choices=NUM_OWNERS_CHOICES)

    # FIX: was BooleanField — use CharField to match 'yes'/'no' from radio buttons
    has_loan             = models.CharField(max_length=3, default='no')
    loan_amount          = models.DecimalField(max_digits=14, decimal_places=2, null=True, blank=True)

    has_tenants          = models.CharField(max_length=3, default='no')
    tenant_details       = models.TextField(blank=True, null=True)

    has_legal_dispute    = models.CharField(max_length=3, default='no')
    dispute_details      = models.TextField(blank=True, null=True)

    has_tax_due          = models.CharField(max_length=3, default='no')
    pending_tax_amount   = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)

    # ── Pricing ────────────────────────────────────────────
    expected_price       = models.DecimalField(max_digits=14, decimal_places=2)
    price_per_sqft       = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    is_negotiable        = models.CharField(max_length=5, choices=NEGOTIABLE_CHOICES, default='yes')

    brokerage            = models.CharField(max_length=5, choices=BROKERAGE_CHOICES, blank=True, null=True)
    brokerage_percentage = models.CharField(max_length=20, choices=BROKERAGE_PERCENTAGE_CHOICES, blank=True, null=True)
    manual_brokerage     = models.CharField(max_length=20, blank=True, null=True)

    description          = models.TextField()

    # ── Media ──────────────────────────────────────────────
    floor_plan           = models.ImageField(upload_to='properties/floor_plans/', null=True, blank=True)
    property_video       = models.FileField(upload_to='properties/videos/', null=True, blank=True)

    # ── Facilities & Amenities ─────────────────────────────
    nearby_facilities    = models.CharField(max_length=255, blank=True, null=True)
    amenities            = models.CharField(max_length=255, blank=True, null=True)

    # ── Address ────────────────────────────────────────────
    city                 = models.CharField(max_length=100)
    locality             = models.CharField(max_length=150)
    building_name        = models.CharField(max_length=200, blank=True, null=True)
    complete_address     = models.TextField()

    # ── Owner ──────────────────────────────────────────────
    owner_name           = models.CharField(max_length=150)
    owner_contact        = models.CharField(max_length=10)
    owner_email          = models.EmailField()
    residential_status   = models.CharField(max_length=10, choices=RESIDENTIAL_STATUS_CHOICES)

    # ── Uploaded By ────────────────────────────────────────
    uploaded_by_name     = models.CharField(max_length=150, blank=True, null=True)
    uploaded_by_email    = models.EmailField(blank=True, null=True)
    uploaded_by_contact  = models.CharField(max_length=15, blank=True, null=True)
    uploaded_by_role     = models.CharField(max_length=20, choices=UPLOADER_ROLE_CHOICES, blank=True, null=True)

    # ── Timestamps ─────────────────────────────────────────
    created_at  = models.DateTimeField(auto_now_add=True)
    updated_at  = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name        = 'Resale Residential Property'
        verbose_name_plural = 'Resale Residential Properties'
        ordering            = ['-created_at']

    def __str__(self):
        return f"{self.title} - {self.city} ({self.bhk})"

    def save(self, *args, **kwargs):
        if self.expected_price and self.builtup_area and self.builtup_area > 0:
            self.price_per_sqft = round(float(self.expected_price) / float(self.builtup_area), 2)
        super().save(*args, **kwargs)


# ── Separate model for multiple property images ────────
class ResalePropertyImage(models.Model):
    property    = models.ForeignKey(
                    ResaleResidentialProperty,
                    on_delete=models.CASCADE,
                    related_name='images'
                  )
    image       = models.ImageField(upload_to='properties/images/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Image for {self.property.title}"

def save(self, *args, **kwargs):
        # Convert values to floats safely before doing any math
        if self.expected_price and self.builtup_area:
            try:
                area = float(self.builtup_area)
                price = float(self.expected_price)
                
                # Now we can safely check if area > 0
                if area > 0:
                    self.price_per_sqft = round(price / area, 2)
            except (ValueError, TypeError):
                # If the values are empty strings or invalid text, just skip the math
                pass
                
        super().save(*args, **kwargs)


############## Models End for Resale Resindential  Property  model ############################ 




############## Models Start for Resale Commericial  Property  model ############################ 


class CommercialResaleProperty(models.Model):

    # ── Basic Information ──────────────────────────────
    PROPERTY_TYPE_CHOICES = [
        ('office', 'Office Space'),
        ('shop', 'Shop/Showroom'),
        ('warehouse', 'Warehouse/Godown'),
        ('industrial', 'Industrial Building'),
        ('land', 'Commercial Land'),
    ]
    ZONE_CHOICES = [
        ('industrial', 'Industrial'),
        ('commercial', 'Commercial'),
        ('residential', 'Residential'),
        ('sez', 'Special Economic Zone'),
    ]
    LOCATION_HUB_CHOICES = [
        ('it', 'IT Park'),
        ('business', 'Business District'),
        ('mall', 'Shopping Mall'),
        ('standalone', 'Standalone'),
    ]
    CONDITION_CHOICES = [
        ('new', 'Brand New'),
        ('excellent', 'Excellent'),
        ('good', 'Good'),
        ('renovation', 'Needs Renovation'),
    ]
    OWNERSHIP_CHOICES = [
        ('freehold', 'Freehold'),
        ('leasehold', 'Leasehold'),
        ('cooperative', 'Co-operative Society'),
    ]
    AGE_CHOICES = [
        ('0-1', '0-1 Year'),
        ('1-3', '1-3 Years'),
        ('3-5', '3-5 Years'),
        ('5-10', '5-10 Years'),
        ('10+', '10+ Years'),
    ]

    title            = models.CharField(max_length=255)
    property_type    = models.CharField(max_length=20, choices=PROPERTY_TYPE_CHOICES)
    zone_type        = models.CharField(max_length=20, choices=ZONE_CHOICES)
    location_hub     = models.CharField(max_length=20, choices=LOCATION_HUB_CHOICES, blank=True, null=True)
    property_condition = models.CharField(max_length=20, choices=CONDITION_CHOICES)
    ownership_type   = models.CharField(max_length=20, choices=OWNERSHIP_CHOICES)
    age_of_property  = models.CharField(max_length=10, choices=AGE_CHOICES)
    available_from   = models.DateField(blank=True, null=True)

    # ── Commercial Specifications ──────────────────────
    num_staircases   = models.PositiveIntegerField(default=0, blank=True, null=True)
    passenger_lifts  = models.PositiveIntegerField(default=0)
    service_lifts    = models.PositiveIntegerField(default=0)
    num_cabins       = models.PositiveIntegerField(default=0, blank=True, null=True)
    meeting_rooms    = models.PositiveIntegerField(default=0, blank=True, null=True)
    min_seats        = models.PositiveIntegerField(blank=True, null=True)
    max_seats        = models.PositiveIntegerField(blank=True, null=True)
    private_parking  = models.PositiveIntegerField(default=0)
    public_parking   = models.PositiveIntegerField(default=0, blank=True, null=True)

    # ── Area & Pricing ─────────────────────────────────
    builtup_area     = models.DecimalField(max_digits=12, decimal_places=2)
    carpet_area      = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    plot_area        = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    brokerage        = models.CharField(max_length=5, blank=True, null=True)      # Yes / No
    brokerage_percentage = models.CharField(max_length=20, blank=True, null=True)
    manual_brokerage = models.CharField(max_length=20, blank=True, null=True)
    expected_price   = models.DecimalField(max_digits=15, decimal_places=2)

    # ── Ownership & Legal ──────────────────────────────
    NUM_OWNERS_CHOICES = [('1','1'),('2','2'),('3','3'),('4+','4+')]
    num_owners         = models.CharField(max_length=5, choices=NUM_OWNERS_CHOICES)
    loan_on_property   = models.CharField(max_length=3)   # yes / no
    loan_amount        = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    existing_tenants   = models.CharField(max_length=3)   # yes / no
    tenant_details     = models.TextField(blank=True, null=True)
    legal_dispute      = models.CharField(max_length=3)   # yes / no
    dispute_details    = models.TextField(blank=True, null=True)
    tax_due            = models.CharField(max_length=3)   # yes / no
    pending_tax_amount = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    fire_noc           = models.CharField(max_length=3, blank=True, null=True)   # yes / no
    property_description = models.TextField()
    sanctioning_authority = models.TextField()

    # ── Media ──────────────────────────────────────────
    floor_plan       = models.ImageField(upload_to='commercial/floor_plans/', blank=True, null=True)
    property_video   = models.FileField(upload_to='commercial/videos/', blank=True, null=True)

    # ── Nearby Facilities & Amenities (stored as comma-separated) ──
    nearby_facilities = models.CharField(max_length=500, blank=True, null=True)
    amenities         = models.CharField(max_length=500, blank=True, null=True)

    # ── Address ────────────────────────────────────────
    city             = models.CharField(max_length=100)
    locality         = models.CharField(max_length=100)
    building_name    = models.CharField(max_length=200, blank=True, null=True)
    property_address = models.TextField()

    # ── Owner Contact ──────────────────────────────────
    RESIDENCY_CHOICES = [
        ('resident', 'Resident'),
        ('nri', 'NRI'),
        ('pio', 'PIO'),
    ]
    owner_name        = models.CharField(max_length=100)
    owner_contact     = models.CharField(max_length=10)
    owner_email       = models.EmailField()
    residential_status = models.CharField(max_length=10, choices=RESIDENCY_CHOICES)

    # ── Uploaded By ────────────────────────────────────
    uploaded_by_name    = models.CharField(max_length=100, blank=True, null=True)
    uploaded_by_email   = models.EmailField(blank=True, null=True)
    uploaded_by_contact = models.CharField(max_length=15, blank=True, null=True)
    uploaded_by_role    = models.CharField(max_length=50, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    

    # ... all your existing fields ...

    is_active = models.BooleanField(default=True)   # ← ADD THIS

  
    def __str__(self):
        return f"{self.title} ({self.property_type}) - {self.city}"

    class Meta:
        verbose_name = "Commercial Property"
        verbose_name_plural = "Commercial Properties"
        ordering = ['-created_at']


# ── Separate model for multiple property images ──────────────────
class CommercialPropertyImage(models.Model):
    property   = models.ForeignKey(CommercialResaleProperty, on_delete=models.CASCADE, related_name='images')
    image      = models.ImageField(upload_to='commercial/images/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Image for {self.property.title}"


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

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

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


class AgriculturalResaleProperty(models.Model):

    # STEP 1: Basic Info
    title = models.CharField(max_length=255, default="Agricultural Land Listing", blank=True, null=True)

    PROPERTY_TYPES = [
        ('agriculture_land', 'Agriculture Land'),
        ('farm_land', 'Farm Land'),
        ('orchard_land', 'Orchard Land'),
    ]
    agriculture_property_type = models.CharField(max_length=50, choices=PROPERTY_TYPES)

    # ✅ CHANGED: area → land_area (match form)
    land_area = models.DecimalField(
    max_digits=10,
    decimal_places=2,
    default=0.00
)

    state = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    district = models.CharField(max_length=100)
    taluka = models.CharField(max_length=100)
    village = models.CharField(max_length=100)

    # ✅ CHANGED: property_address → address
    address = models.TextField()

    # STEP 2: Land Details
    SOIL_TYPES = [
        ('red', 'Red Soil'),
        ('black', 'Black Soil'),
        ('alluvial', 'Alluvial Soil'),
        ('loamy', 'Loamy Soil'),
    ]
    soil_type = models.CharField(max_length=50, choices=SOIL_TYPES, blank=True, null=True)

    WATER_SOURCES = [
        ('well', 'Well'),
        ('borewell', 'Borewell'),
        ('canal', 'Canal'),
        ('river', 'River'),
        ('none', 'None'),
    ]
    water_source = models.CharField(max_length=50, choices=WATER_SOURCES, blank=True, null=True)

    YES_NO_CHOICES = [('yes', 'Yes'), ('no', 'No')]
    irrigation_facility = models.CharField(max_length=10, choices=YES_NO_CHOICES, default='no')

    FERTILITY_STATUS = [('high', 'High'), ('medium', 'Medium'), ('low', 'Low')]
    fertility_status = models.CharField(max_length=20, choices=FERTILITY_STATUS, blank=True, null=True)

    previous_crops = models.CharField(max_length=255, blank=True, null=True)

    resale_agricultural_desc = models.TextField()

    # STEP 3: Pricing & Legal
    expected_price = models.DecimalField(max_digits=15, decimal_places=2)

    brokerage = models.CharField(max_length=10, choices=[('Yes', 'Yes'), ('No', 'No')], blank=True, null=True)
    brokerage_percentage = models.CharField(max_length=50, blank=True, null=True)
    manual_brokerage = models.CharField(max_length=50, blank=True, null=True)

    OWNERSHIP_TYPES = [('freehold', 'Freehold'), ('leasehold', 'Leasehold')]
    ownership_type = models.CharField(max_length=50, choices=OWNERSHIP_TYPES)

    agri_loan = models.CharField(max_length=10, choices=YES_NO_CHOICES, default='no')
    loan_amount = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)

    agri_tenants = models.CharField(max_length=10, choices=YES_NO_CHOICES, default='no')
    tenant_details = models.TextField(blank=True, null=True)

    agri_dispute = models.CharField(max_length=10, choices=YES_NO_CHOICES, default='no')
    dispute_details = models.TextField(blank=True, null=True)

    agri_tax_due = models.CharField(max_length=10, choices=YES_NO_CHOICES, default='no')
    pending_tax_amount = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)

    # STEP 4: Media
    encumbrance_cert = models.FileField(upload_to='property/docs/encumbrance/')
    property_video = models.FileField(upload_to='property/videos/', blank=True, null=True)

    # Owner
    owner_name = models.CharField(max_length=150)
    owner_contact = models.CharField(max_length=15)
    owner_email = models.EmailField()

    RESIDENCY_STATUS = [('resident', 'Resident'), ('nri', 'NRI'), ('pio', 'PIO')]
    comm_residency = models.CharField(max_length=20, choices=RESIDENCY_STATUS, default='resident')

    # Uploaded By
    uploaded_by_name = models.CharField(max_length=100, blank=True, null=True)
    uploaded_by_email = models.EmailField(blank=True, null=True)
    uploaded_by_contact = models.CharField(max_length=20, blank=True, null=True)
    uploaded_by_role = models.CharField(max_length=50, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.agriculture_property_type} - {self.village}"
class AgriculturalResaleImage(models.Model):
    """
    Model to handle multiple image uploads (property_images[]).
    Limits should be enforced at the view/form level (max 10).
    """
    property = models.ForeignKey(AgriculturalResaleProperty, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='property/images/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Image for {self.property.title}"


##################END MODEL SECTION AGRICULTURAL RESALE LISTING################