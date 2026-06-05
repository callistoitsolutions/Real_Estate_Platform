from django.contrib import admin
from django.urls import path
from Main_App import views

urlpatterns = [
      

      ##########urls for Lanlord#####
   
    path('',views.index,name="index"),
   
   # path('api/advanced-search/', views.advanced_search_api, name='advanced_search'),

    path('portalpage',views.portalpage,name="portalpage"),
    
    path('signup/', views.signup_view, name='signup'),
    
    path('login', views.login_view, name='login'),
    path('dashboard/', views.dashboard_view, name='dashboard12'),
  

    ######### urls for check email alreay exists or not ######################

    path('Check_Email_Api', views.Check_Email_Api, name='Check_Email_Api'),

    ####### urls for if email exists directly login #######################

    path('Prop_Login_Api', views.Prop_Login_Api, name='Prop_Login_Api'),

    ######### urls for send otp to email ##########################

    path('Send_Otp_Api', views.Send_Otp_Api, name='Send_Otp_Api'),

    ########### urls for verify otp for email ###########################

    path('Verify_Otp_Api', views.Verify_Otp_Api, name='Verify_Otp_Api'),

    ######### urls for user registration ##############################

    path('Prop_Register_Api', views.Prop_Register_Api, name='Prop_Register_Api'),

    ############ urls for wishlist properties #############################

    path('Wishlist_Property', views.Wishlist_Property, name='Wishlist_Property'),

    ########## urls for ajax for add property to wishlist ###################

    path('Wishlist_Ajax', views.Wishlist_Ajax, name='Wishlist_Ajax'),
  
#path('property_details',views.property_details,name="property_details"),
   
    
#path('properties',views.properties,name="properties"),
    path('services',views.services,name="services"),

    path('about',views.about,name="about"),

    ############## urls for contact us page ##########################

    path('Contact_Us',views.Contact_Us,name="Contact_Us"),

    ############## urls for ajax for contact us page ##################

    path('Contact_Ajax',views.Contact_Ajax,name="Contact_Ajax"),

  
    #('blog', views.blog, name='blog'),
    
    path('blogs1/', views.blog, name="blog"),
   # path('<str:key>/', views.landing_page_view, name="landing_page"),
    path('contact', views.contact, name='contact'),


    path('Adminlogin', views.Adminlogin,name="Adminlogin"),

    ############## urls for admin logout ########################

    path('Admin_Logout',views.Admin_Logout,name='Admin_Logout'),
  
  
   

    path(
    "faqs/",
    views.dynamic_property_faq,
    name="dynamic_property_faq"
),
  
    path("categories/", views.category_list, name="category_list"),
    
    path("create/", views.create_blog, name="create_blog"),
   # path('blog/<int:id>/', views.blog_details, name='blog_detail'),# Blog create form
    #path('blog/<int:id>/', views.blog_details, name='blog_details'),
    path(
    "blogs/<slug:key>/",
    views.blog_details,
    name="blog_details"
),


    
  #  path('services_details', views.services_details, name='services_details'),
   # path("<int:pk>/", views.services_details, name="services_details"),
    path("service/<str:key>/", views.services_details, name="services_details"),
   # path("property/<str:type>/<int:id>/faqs/", views.property_faq_view, name="property_faq"),
    path("faqs/", views.all_faqs, name="all_faqs"),
    


    
    
    
    ##############Start URL Section Property Listing Page##########################
    
    path('api/search-suggestions/', views.search_suggestions_api, name='search_suggestions'),
    path('listingpage/', views.listings_view, name='listings'),
   
    path('listing/<str:listing_type>/<str:category>/<int:pk>/', views.property_detail_view, name='property_detail'),
    
    path(
        "save-property-enquiry/",
        views.save_property_enquiry,
        name="save_property_enquiry"
    ),

   
    ######### urls for ajax for send property enquiry #####################

    path('Send_Property_Enquiry', views.Send_Property_Enquiry, name='Send_Property_Enquiry'),

    

    

  
   


    # ================= RENTAL LISTING =================
    path('rent/residential/', views.rent_residential, name='rent_residential'),
    path('rent/commercial/', views.rent_commercial, name='rent_commercial'),
    path('rent/pg-coliving/', views.rent_pg_coliving, name='rent_pg_coliving'),

    # ================= RESALE LISTING =================
    path('resale/residential/', views.residential_resale_form, name='residential_resale_form'),
    path('resale/commercial/', views.resale_commercial_form, name='resale_commercial_form'),
    path('resale/agricultural/', views.resale_agricultural_form, name='resale_agricultural_form'),
    path('resale/plot/', views.resale_plot_form, name='resale_plot_form'),
    path('resale/industrial/', views.resale_industrial_form, name='resale_industrial_form'),

    #######################START URL SECTION OF POST PROPERTY####################################

   path('post_property', views.post_property, name='post_property'),


        #######################END URL SECTION OF POST PROPERTY##################################







 


]
    
    
    
    
    
    


    







    #path('property/<str:property_type>/<int:property_id>/', views.property_detail_page, name='property_detail_page'),



    



