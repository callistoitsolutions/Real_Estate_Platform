from django.contrib import admin
from django.urls import path
from Main_App import views

urlpatterns = [
      

      ##########urls for Lanlord#####
   
    path('',views.index,name="index"),
    
    path('signup/', views.signup_view, name='signup'),
    
    path('login', views.login_view, name='login'),
    path('dashboard/', views.dashboard_view, name='dashboard12'),
    path('lead-capture/', views.lead_capture_view, name='lead_capture'),
    path('post_property', views.post_property_view, name='post_property'),
    path('property_view_report', views.property_view_report, name='property_view_report'),
#path('property_details',views.property_details,name="property_details"),
    
#path('properties',views.properties,name="properties"),
    path('services',views.services,name="services"),
    path('agents',views.agents,name="agents"),
    path('about',views.about,name="about"),
    #path('agent/create/', views.agent_create, name='agent_create'),
    path('complaint_form', views.complaint_form, name='complaint_form'),
    #('blog', views.blog, name='blog'),
    
    path('blogs1/', views.blog, name="blog"),
   # path('<str:key>/', views.landing_page_view, name="landing_page"),
    path('contact', views.contact, name='contact'),
   # path('blog_details', views.blog_details, name='blog_details'),
   ## path('property', views.property_listing_detail, name='property_detail'),
  #  path('property_view', views.property_view_report, name='property_view_report'),
    path('residential_property', views.residential_property, name='residential_property'),
    path('commercial', views.commercial, name='commercial'),
    path('pg_coliving', views.pg_coliving, name='pg_coliving'),
  #  path('signup', views.signup, name='signup'),
    #path('post_property', views.post_property, name='post_property'),
    path('renewal', views.renewal, name='renewal'),
    
 
    # Post Property
   


    #path("properties/", views.property_list, name="property_list"),
    # Property Detail + Inquiry
    #path("property/<slug:key>/", views.property_detail_page, name="property_detail_page"),
    #path("property/<str:property_type>/<int:property_id>/", views.property_detail_page, name="property_detail_page"),

    
   # path("dashboard/user/", views.user_dashboard, name="user_dashboard"),
    path("dashboard/admin/", views.admin_dashboard, name="admin_dashboard"),
    path('Adminlogin', views.Adminlogin,name="Adminlogin"),

    ############## urls for admin logout ########################

    path('Admin_Logout',views.Admin_Logout,name='Admin_Logout'),
  
    
    
  
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
  
   # path("blog", views.blog_detail, name="blog_detail"),  # using slug now
    path("ads/<str:key>/", views.add_details, name="add_details"),
#path("blog/<str:key>/", views.blog_details, name="blog_details"),
    path("add", views.add, name="add"),
    path("rm_portal", views.rm_portal, name="rm_portal"),
   # path("broker_dashboard", views.broker_dashboard, name="broker_dashboard"),
    # urls.py



    path("properties/", views.properties, name="properties"),
    path("agent_profile", views.agent_profile, name="agent_profile"),
  #  path("property/<slug:key>/", views.property_detail_page, name="property_detail_page"),


    path('properties/', views.property_listing, name='property_listing'),

 
    path('com', views.com, name='com'),
   
 
    path("properties/", views.properties, name="properties"),
    #path("property/<slug:key>/", views.property_detail_page, name="property_detail_page"),
    
    
    
   # path('add/', views.add_package, name='add_package'),
    #path('package_list', views.package_list, name='package_list'),
   # path('plans/', views.subscription_showcase, name='subscription_showcase'),
   # path('checkout/<int:package_id>/', views.checkout, name='checkout'),
   # path('invoice/<int:invoice_id>/', views.invoice_detail, name='invoice_detail'),
   # path('invoice/<int:invoice_id>/pdf/', views.download_invoice_pdf, name='download_invoice_pdf'),






    # Super-admin style pages
    

    
   # path('addons/add/', views.addon_add, name='addon_add'),
   
  #  path('invoice/<int:subscription_id>/', views.subscription_invoice, name='subscription_invoice'),# optional
    path('addons/', views.addon_list, name='addon_list'),
    
    path('addons/<slug:slug>/', views.addon_landing, name='addon_landing'),
    
   # path("<str:type>/<int:id>/", views.property_faq_detail, name="property_faq_detail"),
    path("property/<str:type>/<int:id>/faqs/", views.property_faq_view, name="property_faq"),
    path("faqs/", views.all_faqs, name="all_faqs"),
    

    path("create_ad", views.create_ad, name="create_ad"),
    path("list/", views.sponsored_ad_list_view, name="list_ads"),
    path('ads/<slug:slug>/', views.sponsored_ad_detail_view, name='ad_detail'),
]

    







    #path('property/<str:property_type>/<int:property_id>/', views.property_detail_page, name='property_detail_page'),



    



