from django.contrib import admin
from django.urls import path
from Agency_App import views

urlpatterns = [
      
    ########### urls for agency dashbaord #####################

    path('Agency_Dashboard',views.Agency_Dashboard,name="Agency_Dashboard"),

    ########### urls for update agency profile ###################

    path('Update_Profile_Agency',views.Update_Profile_Agency,name='Update_Profile_Agency'),

    ############## urls for assign enquiries to agency/Builder #########################

    path('Assign_Enquiry_Agency',views.Assign_Enquiry_Agency,name='Assign_Enquiry_Agency'),

    ############ urls for update property enquiry ############################

    path('update_enquiry_agency/<int:id>',views.update_enquiry_agency,name="update_enquiry_agency"),
    
]

    










