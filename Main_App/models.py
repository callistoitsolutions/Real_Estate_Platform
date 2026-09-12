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
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True, blank=True)
    object_id = models.CharField(max_length=50, null=True, blank=True)   # ← changed from PositiveIntegerField
    property_object = GenericForeignKey('content_type', 'object_id')

    user = models.ForeignKey(User_Details, on_delete=models.CASCADE, blank=True, null=True)
    wishlist_date = models.DateField(blank=True, null=True)
    wishlist_time = models.TimeField(blank=True, null=True)

    
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



def generate_lead_id():
    return f"EF-AI-{uuid.uuid4().hex[:8].upper()}"


class ChatbotLead(models.Model):
    """One row per chatbot session. Upserted on every turn so RMs always see
    the latest captured requirement without the visitor filling a form."""

    LEAD_CLASS_CHOICES = [
        ("HOT", "🔥 Hot Lead"),
        ("WARM", "🟡 Warm / Qualified"),
        ("INFO", "🔵 Information Seeker"),
        ("TIMEPASS", "🟣 Timepass / Low Intent"),
        ("FRAUD", "🔴 Fraud / High Risk"),
    ]
    STAGE_CHOICES = [
        ("NEW", "New"),
        ("QUALIFIED", "Requirement Qualified"),
        ("CONTACTED", "RM Contacted"),
        ("VISIT_PLANNED", "Visit Planned"),
        ("VISIT_DONE", "Visit Completed"),
        ("NEGOTIATION", "Negotiation"),
        ("DOCUMENTATION", "Documentation"),
        ("BOOKED", "Booking"),
        ("CLOSED", "Deal Closed"),
        ("DROPPED", "Dropped"),
    ]
    TXN_CHOICES = [("rent", "Rent"), ("buy", "Buy / Resale"), ("unknown", "Unknown")]

    id = models.CharField(max_length=30, primary_key=True, default=generate_lead_id, editable=False)
    session_id = models.CharField(max_length=100, db_index=True)

    # Customer-provided
    customer_name = models.CharField(max_length=150, blank=True, null=True)
    mobile = models.CharField(max_length=20, blank=True, null=True)
    email = models.CharField(max_length=150, blank=True, null=True)
    customer_type = models.CharField(max_length=50, blank=True, null=True)  # Tenant/Buyer/Investor/Owner

    # Requirement (captured across the conversation, never re-asked once known)
    transaction_type = models.CharField(max_length=10, choices=TXN_CHOICES, default="unknown")
    category = models.CharField(max_length=50, blank=True, null=True)   # residential/commercial/pg/plot/industrial/agricultural
    city = models.CharField(max_length=100, blank=True, null=True)
    location = models.CharField(max_length=150, blank=True, null=True)
    bhk = models.CharField(max_length=20, blank=True, null=True)
    budget_min = models.BigIntegerField(blank=True, null=True)
    budget_max = models.BigIntegerField(blank=True, null=True)
    furnishing = models.CharField(max_length=50, blank=True, null=True)
    timeline = models.CharField(max_length=50, blank=True, null=True)      # "immediate" / "<=30d" / "1-3m" / etc.
    preferred_visit_time = models.CharField(max_length=100, blank=True, null=True)
    property_id_ref = models.CharField(max_length=50, blank=True, null=True)  # if chat centred on one listing

    # AI outputs
    primary_intent = models.CharField(max_length=100, blank=True, null=True)
    secondary_intents = models.CharField(max_length=255, blank=True, null=True)
    lead_score = models.IntegerField(default=0)
    lead_classification = models.CharField(max_length=20, choices=LEAD_CLASS_CHOICES, default="INFO")
    risk_level = models.CharField(max_length=10, default="LOW")  # LOW/MEDIUM/HIGH
    conversation_summary = models.TextField(blank=True, null=True)
    next_best_action = models.CharField(max_length=255, blank=True, null=True)

    # Behaviour flags
    rm_requested = models.BooleanField(default=False)
    visit_requested = models.BooleanField(default=False)
    negotiation_requested = models.BooleanField(default=False)
    properties_viewed = models.TextField(blank=True, null=True)   # comma-separated IDs shown to the visitor

    # CRM
    source = models.CharField(max_length=50, default="AI Assistant")
    stage = models.CharField(max_length=20, choices=STAGE_CHOICES, default="NEW")
    assigned_rm_id = models.CharField(max_length=50, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-updated_at"]

    def __str__(self):
        return f"{self.id} - {self.lead_classification} ({self.location or 'no location'})"


class ChatbotMessage(models.Model):
    lead = models.ForeignKey(ChatbotLead, on_delete=models.CASCADE, related_name="messages")
    sender = models.CharField(max_length=10, choices=[("user", "User"), ("bot", "Bot")])
    message = models.TextField()
    intent = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["created_at"]


class ChatbotRiskEvent(models.Model):
    RISK_CHOICES = [("LOW", "Low"), ("MEDIUM", "Medium"), ("HIGH", "High")]

    session_id = models.CharField(max_length=100, db_index=True)
    lead = models.ForeignKey(ChatbotLead, on_delete=models.SET_NULL, null=True, blank=True, related_name="risk_events")
    message = models.TextField()
    matched_rule = models.CharField(max_length=255, blank=True, null=True)
    risk_level = models.CharField(max_length=10, choices=RISK_CHOICES, default="HIGH")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]





class IntentMaster(models.Model):
    intent_id = models.CharField(max_length=20, unique=True)
    category = models.CharField(max_length=50)
    intent_name = models.CharField(max_length=150)
    customer_type = models.CharField(max_length=50)
    example_utterance = models.TextField()
    ai_logic_description = models.TextField()
    next_best_action = models.CharField(max_length=255)
    lead_classification = models.CharField(max_length=50)
    base_score = models.IntegerField(default=0)
    entities_to_extract = models.CharField(max_length=255, blank=True, null=True)
    requires_rm = models.CharField(max_length=20)
    risk_level = models.CharField(max_length=20)
    clarification_prompt = models.TextField()
    notes = models.TextField(blank=True, null=True)

class FraudRiskRule(models.Model):
    risk_id = models.CharField(max_length=20, unique=True)
    signal = models.CharField(max_length=150)
    example = models.TextField()
    risk_level = models.CharField(max_length=50)
    ai_action = models.TextField()
    human_action = models.CharField(max_length=150)
    data_to_log = models.CharField(max_length=255)

class LeadScoringRule(models.Model):
    rule_id = models.CharField(max_length=20, unique=True)
    signal = models.CharField(max_length=150)
    example = models.TextField()
    points = models.IntegerField(default=0)
    classification_impact = models.CharField(max_length=150)
    notes = models.TextField(blank=True, null=True)




        