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

