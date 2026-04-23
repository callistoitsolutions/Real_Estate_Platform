from django.contrib import admin
from django.urls import path
from Vendors import views

app_name = 'Vendors'

urlpatterns = [
      
    ########### urls for tenant dashbaord #####################

    path('vendors_Dashboard',views.vendors_Dashboard,name="vendors_Dashboard"),

    ########### urls for update vendor profile ######################

    path('Update_Profile_Vendor',views.Update_Profile_Vendor,name='Update_Profile_Vendor'),

]

    










