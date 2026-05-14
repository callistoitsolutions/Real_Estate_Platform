from django.contrib.auth.models import User
from django.db import models
from django.utils.timezone import now


class Property_Enquiry(models.Model):

    property_id = models.IntegerField(blank=True, null=True)

    user = models.ForeignKey(
        'Admin_App.User_Details',
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )

    owner_name = models.CharField(max_length=200, blank=True, null=True)

    owner_phone = models.CharField(max_length=20, blank=True, null=True)

    enquiry_name = models.CharField(max_length=200, blank=True, null=True)

    enquiry_phone = models.CharField(max_length=20, blank=True, null=True)

    enquiry_message = models.TextField(blank=True, null=True)

    enquiry_type = models.CharField(
        max_length=100,
        default="Phone Reveal"
    )

    ip_address = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):

        return str(self.enquiry_name)
        
class User_Subscription(models.Model):

    user = models.ForeignKey(
        'Admin_App.User_Details',
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )

    subscription = models.ForeignKey(
        'Admin_App.Subscription_Details',
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )

    total_contacts = models.IntegerField(default=3)

    used_contacts = models.IntegerField(default=0)

    remaining_contacts = models.IntegerField(default=3)

    is_active = models.BooleanField(default=True)

    start_date = models.DateField(blank=True, null=True)

    expiry_date = models.DateField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):

        return str(self.user.user_name)