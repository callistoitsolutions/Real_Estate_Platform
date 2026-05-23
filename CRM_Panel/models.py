from django.db import models
from django.utils.timezone import now
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from Admin_App.models import *


################### Property Enquiry Modal Starts Here ######################


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

    # 3. The Generic Foreign Key (Combines the two above)
    property_object = GenericForeignKey('content_type', 'object_id')

    # --- Your existing fields stay the same ---
    user = models.ForeignKey(User_Details,on_delete=models.CASCADE,blank=True,null=True
    )

    enquiry_name = models.CharField(max_length=200, blank=True, null=True)
    country_code = models.CharField(max_length=10, default="+91", blank=True, null=True)
    enquiry_phone = models.CharField(max_length=20, blank=True, null=True)

    whatsapp_consent = models.BooleanField(default=False)

    enquiry_date = models.DateField(blank=True,null=True)
    enquiry_time = models.TimeField(blank=True,null=True)

    def __str__(self):
        return str(self.enquiry_name)+"-"+self.enquiry_phone
    
############### Property Enquiry Modal Ends Here ############################
