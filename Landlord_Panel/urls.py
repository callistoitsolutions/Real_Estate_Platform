from django.contrib import admin
from django.urls import path
from Landlord_Panel import views

urlpatterns = [
      

      ##########urls for Lanlord#####
   
     path('landlord_dashboard',views.landlord_dashboard,name="landlord_dashboard"),
     path('residential_landlord',views.residential_landlord,name="residential_landlord"),
     path('commercial_landlord',views.commercial_landlord,name="commercial_landlord"),
     path('pg_coliving_landlord',views.pg_coliving_landlord,name="pg_coliving_landlord"),
     path('delete_confirmation',views.delete_confirmation,name="delete_confirmation"),
     path('Subscription_Upgrade_Form',views.Subscription_Upgrade_Form,name="Subscription_Upgrade_Form"),
     path('data_landlord',views.data_landlord,name="data_landlord"),
     path('residential_landlord_edit',views.residential_landlord_edit,name="residential_landlord_edit"),
     path('boostlisting',views.boostlisting,name="boostlisting"),
     
     #path('create/', views.property_create, name='property_create'),


     ############# urls for update landlord profile page #####################

     path('Update_Profile_Landlord',views.Update_Profile_Landlord,name='Update_Profile_Landlord'),
     
  


     #path('property/add/', views.property_create, name='property_add'),
    path('property/', views.property_list, name='property_list'),
    path('property/add/', views.property_create, name='property_add'),
    path('property/edit/<int:pk>/', views.property_edit, name='property_edit'),
    path('property/delete/<int:pk>/', views.property_delete, name='property_delete'),


    path("commercialform", views.commercialform, name="commercialform"),
    path("commercial-property/add/", views.commercial_property_add, name="commercial_property_add"),
    path("commercial-property/list/", views.commercial_property_list, name="commercial_property_list"),
    
    path("pg-property/add/", views.add_pg_property, name="add_pg_property"),
    path("pg-property/list/", views.pg_property_list, name="pg_property_list"),
    
    
    path('boost/new/', views.boost_listing_create, name='boost_listing_create'),
    path('boost/', views.boost_listing_list, name='boost_listing_list'),
    
    path('enquiry/new/', views.enquiry_create, name='enquiry_create'),
    path('enquiry/', views.enquiry_list, name='enquiry_list'),
    path("property_inquiry", views.property_inquiry, name="property_inquiry"),


    path("properties/residential/", views.residential_property_list, name="residential_property_list"),
    path("properties/commercial/", views.commercial_property_list, name="commercial_property_list"),
    path("properties/pg/", views.pg_property_list, name="pg_property_list"),


    path('inquiries/residential/', views.residential_inquiries_view, name='residential_inquiries'),
#path('inquiries/commercial/', views.commercial_inquiries_view, name='commercial_inquiries'),
   # path('inquiries/pg/', views.pg_inquiries_view, name='pg_inquiries'),

    # Example property detail views
    path('property/residential/<int:pk>/', views.residential_property_detail, name='residential_property_detail'),


   # path("property/list/", views.commercial_property_list, name="commercial_property_list"),
]

     






