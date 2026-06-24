from django.db import models
from django.utils.timezone import now
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from Admin_App.models import *


############### UTM Link Modal Starts Here #######################

class UTMLink(models.Model):
      
    # Basic info
    link_id = models.CharField(max_length=50, unique=True)
    
    #  Generic Foreign Key to property (links to any of your 8 property types)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE,blank=True,null=True)

    object_id = models.PositiveIntegerField(blank=True, null=True)
    property_obj = GenericForeignKey('content_type', 'object_id')
    
    # Denormalized fields for quick access (optional - keep for performance)
    property_title = models.CharField(max_length=500, blank=True, null=True)
    listing_type = models.CharField(max_length=50, default='rent')
    category = models.CharField(max_length=100, blank=True, null=True, db_index=True)
    
    # The actual UTM URL
    utm_path = models.CharField(max_length=500, default='/')
    utm_url = models.TextField()
    
    # UTM Parameters
    utm_source = models.CharField(max_length=255)
    utm_medium = models.CharField(max_length=255)
    utm_campaign = models.CharField(max_length=255, blank=True, null=True)
    utm_term = models.CharField(max_length=255, blank=True, null=True)
    utm_content = models.CharField(max_length=255, blank=True, null=True)
    
    # Statistics
    total_clicks = models.IntegerField(default=0)
    total_enquiries = models.IntegerField(default=0)
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=['category', 'utm_source']),
            models.Index(fields=['listing_type', 'category']),
            models.Index(fields=['content_type', 'object_id']),
        ]
    
    def __str__(self):
        return f"{self.utm_source} - {self.property_title or self.property_obj}"
    

############### UTM Link Modal Ends Here ########################


############# Property Enquiry Modal Starts Here ######################

class PropertyEnquiry(models.Model):

    # 1. The type of property (PG, Commercial, etc.)
    content_type = models.ForeignKey(
        ContentType, 
        on_delete=models.CASCADE, 
        null=True, 
        blank=True
    )
    
    # 2. The ID of that specific property
    object_id = models.PositiveIntegerField(null=True, blank=True)

    # 3.The Generic Foreign Key (Combines the two above)
    property_object = GenericForeignKey('content_type', 'object_id')

    enquiry_name = models.CharField(max_length=200, blank=True, null=True)
    country_code = models.CharField(max_length=10, default="+91", blank=True, null=True)
    enquiry_phone = models.CharField(max_length=20, blank=True, null=True)

    whatsapp_consent = models.BooleanField(default=False)

    # IMPROVED: Foreign Key to UTMLink instead of duplicating fields
    utm_link = models.ForeignKey(
        'UTMLink', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='enquiries',
        db_index=True
    )

    # Lead Status

    assigned_to = models.ForeignKey(User_Details, on_delete=models.CASCADE, blank=True, null=True)
    lead_status = models.CharField(max_length=20, blank=True, null=True,default="Pending")
    followup_notes = models.TextField(blank=True,null=True)
    closed_date = models.DateField(null=True, blank=True)

    # Date Fields
    enquiry_date = models.DateField(blank=True, null=True)
    enquiry_time = models.TimeField(blank=True, null=True)

    def __str__(self):
        return f"{self.enquiry_name} - {self.enquiry_phone}"
    
    @property
    def get_utm_source(self):
        if self.utm_link:
            return self.utm_link.utm_source
        return self.utm_source
    
############## Property Enquiry Modal Ends Here ################################## 
