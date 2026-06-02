from django.contrib import admin
from django.urls import path
from CRM_Panel import views

urlpatterns = [
      

      ##########urls for Lanlord#####
   
 
     path('crm_dashboard',views.crm_dashboard,name="crm_dashboard"),

     ############## urls for display utm links #######################

     path('utm_links_crm',views.utm_links_crm,name="utm_links_crm"),

     ############# urls for create utm link ######################

     path('create_utm_crm',views.create_utm_crm,name="create_utm_crm"),

     ############ urls for delete utm link #######################

     path('delete_utm_crm',views.delete_utm_crm,name="delete_utm_crm"),


    ############# urls for property enquiry sections ####################

    path('property_enquiry_crm',views.property_enquiry_crm,name="property_enquiry_crm"),

    ############## urls for delete property enquiry ########################

    path('delete_property_enquiry',views.delete_property_enquiry,name="delete_property_enquiry"),

    ############# urls for update property enquiry #####################

    path('update_property_enquiry/<int:id>',views.update_property_enquiry,name="update_property_enquiry"),

    ############ urls for ajax for update property enquiry ####################

    path('property_enquiry_ajax',views.property_enquiry_ajax,name="property_enquiry_ajax"),
    
     
    
     
 

 
   
     
 


     
]










    
    # Repeat pattern for all other forms, e.g.
    # path('manual-lead/new/', views.manual_lead_create, name='manual_lead_create'),
    # path('manual-lead/', views.manual_lead_list, name='manual_lead_list'), ...

   
     
    








