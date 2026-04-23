from django.contrib import admin
from django.urls import path
from Admin_App import views

urlpatterns = [
      

      ##########urls for manage crime officer#####
     path('admin_page',views.admin_page,name="admin_page"),
     path('index3',views.index3,name="index3"),
     path('index2',views.index2,name="index2"),

     ############ urls for rental forms ##########################

     path('residential',views.residential,name="residential"),
     path('commercial',views.commercial,name="commercial"),
     path('pg_coliving',views.pg_coliving,name="pg_coliving"),


     ############# urls for ameneties list ############################

     path('Ameneties_List',views.Ameneties_List,name="Ameneties_List"),

     ########## urls for ajax for add/update ameneties ######################

     path('Ameneties_Ajax',views.Ameneties_Ajax,name="Ameneties_Ajax"),

     ########## urls for upload ameneties data via excel ###################

     path('Ameneties_Data',views.Ameneties_Data,name="Ameneties_Data"),

     ######### urls for delete ameneties data ##########################

     path('Delete_Ameneties',views.Delete_Ameneties,name='Delete_Ameneties'),

     ########### urls for update ameneties data ######################

     path('Update_Ameneties/<int:id>',views.Update_Ameneties,name='Update_Ameneties'),

     ########### urls for nearby facilities list ########################

     path('Facilities_List',views.Facilities_List,name="Facilities_List"),

     ############# urls for ajax for add/update nearby facilities ##################

     path('Facilities_Ajax',views.Facilities_Ajax,name="Facilities_Ajax"),

     ############# urls for upload facilities data via excel ################

     path('Facilities_Data',views.Facilities_Data,name="Facilities_Data"),

     ############## urls for delete facilities data ####################

     path('Delete_Facilities',views.Delete_Facilities,name='Delete_Facilities'),

     ############## urls for update facilities data #######################

     path('Update_Facilities/<int:id>',views.Update_Facilities,name='Update_Facilities'),

     ########## urls of vendor services list ####################

     path('Services_List',views.Services_List,name="Services_List"),

     ########## urls for ajax for add/update service types ######################

     path('Services_Ajax',views.Services_Ajax,name="Services_Ajax"),

     ########### urls for upload service type details via excel ################

     path('Services_Data',views.Services_Data,name="Services_Data"),

     ############# urls for rental property list ########################

    # path('residential_list',views.residential_list,name="residential_list"),
     path('commercial_list',views.commercial_list,name="commercial_list"),
      
     path('pg_list',views.pg_list,name="pg_list"),

     path('residential_resale',views.residential_resale,name="residential_resale"),
     path('commercial_resale',views.commercial_resale,name="commercial_resale"),
     path('plot_resale',views.plot_resale,name="plot_resale"),
     path('industrial_resale',views.industrial_resale,name="industrial_resale"),
     path('agricultural_resale',views.agricultural_resale,name="agricultural_resale"),

     ########### urls for resale property list #########################

     path('residential_resale_list',views.residential_resale_list,name="residential_resale_list"),
     path('commercial_resale_list',views.commercial_resale_list,name="commercial_resale_list"),
     path('plot_resale_list',views.plot_resale_list,name="plot_resale_list"),
     path('industrial_resale_list',views.industrial_resale_list,name="industrial_resale_list"),
     path('agricultural_resale_list',views.agricultural_resale_list,name="agricultural_resale_list"),

     ############# urls for display rm list #######################

     path('rm_list',views.rm_list,name="rm_list"),

    ############# urls for add rm ##############################

    path('Add_RM',views.Add_RM,name="Add_RM"),

    ######## urls for upload rm data functionality via excel ###################

    path('Rm_Data',views.Rm_Data,name="Rm_Data"),

    ######### urls for delete rm details #########################

    path('Delete_RM',views.Delete_RM,name='Delete_RM'),

    ########## urls for update rm details #######################

    path('Update_RM/<int:id>',views.Update_RM,name='Update_RM'),

    ########### urls for ajax for add/update rm functionality ###############

    path('User_Ajax',views.User_Ajax,name="User_Ajax"),



    ######### urls for display landlords list #################

    path('Landlord_List',views.Landlord_List,name="Landlord_List"),

    ########## urls for add landlords #######################

    path('Add_Landlord',views.Add_Landlord,name="Add_Landlord"),

    ############ urls for upload landlord data functionality via excel #################

    path('Landlord_Data',views.Landlord_Data,name="Landlord_Data"),

    ########### urls for delete landlord details #################

    path('Delete_Landlord',views.Delete_Landlord,name='Delete_Landlord'),

    ########### urls for update landlord details ######################

    path('Update_Landlord/<int:id>',views.Update_Landlord,name='Update_Landlord'),

    ############ urls for display tenants list ####################

    path('Tenant_List',views.Tenant_List,name="Tenant_List"),

    ########## urls for add tenants ########################

    path('Add_Tenant',views.Add_Tenant,name="Add_Tenant"),

    ############ urls for upload tenant data functionality via excel ##############

    path('Tenant_Data',views.Tenant_Data,name="Tenant_Data"),

    ########### urls for delete tenant details ############################

    path('Delete_Tenant',views.Delete_Tenant,name='Delete_Tenant'),

    ########### urls for update tenant details ####################

    path('Update_Tenant/<int:id>',views.Update_Tenant,name='Update_Tenant'),

    ############## urls for display buyers list #####################

    path('Buyer_List',views.Buyer_List,name="Buyer_List"),

    ############## urls for add buyers #########################

    path('Add_Buyer',views.Add_Buyer,name="Add_Buyer"),

    ############# urls for buyer data functionality via excel #####################

    path('Buyer_Data',views.Buyer_Data,name="Buyer_Data"),

    ############# urls for delete buyer details #########################

    path('Delete_Buyer',views.Delete_Buyer,name='Delete_Buyer'),

    ############# urls for update buyer details ####################

    path('Update_Buyer/<int:id>',views.Update_Buyer,name='Update_Buyer'),

    ############# urls for display agents list ####################

    path('Agent_List',views.Agent_List,name="Agent_List"),

    ############# urls for add agents ####################

    path('Add_Agent',views.Add_Agent,name="Add_Agent"),

    ######### urls for upload agent data functionality via excel ################

    path('Agent_Data',views.Agent_Data,name="Agent_Data"),

    ######### urls for delete agent ########################

    path('Delete_Agent',views.Delete_Agent,name='Delete_Agent'),

    ############ urls for update agent details #####################

    path('Update_Agent/<int:id>',views.Update_Agent,name='Update_Agent'),


    ########### urls for display agency list ##############

    path('Agency_List',views.Agency_List,name="Agency_List"),

    ########### urls for add agency #######################

    path('Add_Agency',views.Add_Agency,name="Add_Agency"),

    ############ urls for upload agency data functionality via excel ###############

    path('Agency_Data',views.Agency_Data,name="Agency_Data"),

    ########### urls for delete agency ################################

    path('Delete_Agency',views.Delete_Agency,name='Delete_Agency'),

    ########## urls for update agency ######################

    path('Update_Agency/<int:id>',views.Update_Agency,name='Update_Agency'),

    ########### urls for display vendors list ####################

    path('Vendor_List',views.Vendor_List,name="Vendor_List"),

    ########### urls for add vendors ####################

    path('Add_Vendor',views.Add_Vendor,name="Add_Vendor"),

    ########## urls for upload vendor data functionality via excel ###################

    path('Vendor_Data',views.Vendor_Data,name="Vendor_Data"),

    ############ urls for delete vendor #########################

    path('Delete_Vendor',views.Delete_Vendor,name='Delete_Vendor'),

    ################ urls for update vendor #####################

    path('Update_Vendor/<int:id>',views.Update_Vendor,name='Update_Vendor'),

    ############## urls for update profile page ###########################

    path('Update_Profile_Admin',views.Update_Profile_Admin,name='Update_Profile_Admin'),

    ############# urls for ajax for update profile #######################

    path('Admin_Profile_Ajax',views.Admin_Profile_Ajax,name='Admin_Profile_Ajax'),

     

     
     path('admin_approval_form',views.admin_approval_form,name="admin_approval_form"),
     path('referral_closing',views.referral_closing,name="referral_closing"),
     
     path('data',views.data,name="data"),
     path('commercial_table',views.commercial_table,name="commercial_table"),
     path('pg_co_table',views.pg_co_table,name="pg_co_table"),
     path('seo_meta_tag',views.seo_meta_tag,name="seo_meta_tag"),
     path('seo_meta_tag_list',views.seo_meta_tag_list,name="seo_meta_tag_list"),
     #path('add_blog',views.add_blog,name="add_blog"),
 #    path('blog_list',views.blog_list,name="blog_list"),
     path('dynamic_page_edit',views.dynamic_page_edit,name="dynamic_page_edit"),
     path('dynamic_page_report',views.dynamic_page_report,name="dynamic_page_report"),
     path('Commission_Hold_Release',views.Commission_Hold_Release,name="Commission_Hold_Release"),
     path('commision_hold_table',views.commision_hold_table,name="commision_hold_table"),
      ########## end urls for manage crime officer#####

######## urls for manage user######
     path('other',views.other,name="other"),
     path('inquiry',views.inquiry,name="inquiry"),
     path('Subscription_Purchase',views.Subscription_Purchase,name="Subscription_Purchase"),
     path('GST_Invoice',views.GST_Invoice,name="GST_Invoice"),
     path('Wallet_Top_up',views.Wallet_Top_up,name="Wallet_Top_up"),
     path('Lead_Assignment',views.Lead_Assignment,name="Lead_Assignment"),
     path('Lead_Status_Update',views.Lead_Status_Update,name="Lead_Status_Update"),
     path('Property_Review',views.Property_Review,name="Property_Review"),
     path('chat',views.chat,name="chat"),
     path('profile_update',views.profile_update,name="profile_update"),
     path('broadcast_email',views.broadcast_email,name="broadcast_email"),
     path('send_message',views.send_message,name="send_message"),
     path('comission_structure_setup',views.comission_structure_setup,name="comission_structure_setup"),
     path('commision_release_cycle',views.commision_release_cycle,name="commision_release_cycle"),
     
     
  
     
     
     
     
  
    ######## urls for website section######
    
     path("hero-sections/add/", views.hero_section, name="hero_section"),
     path("hero-sections/", views.hero_section_list, name="hero_section_list"),
     path("hero-sections/<int:pk>/edit/", views.hero_section_edit, name="hero_section_edit"),
     path("hero-sections/<int:pk>/delete/", views.hero_section_delete, name="hero_section_delete"),
     path("hero-sections/<int:pk>/toggle/", views.hero_section_toggle, name="hero_section_toggle"),
     
     
     path("admin/add-blog/", views.add_blog, name="add_blog"),
     path("admin/blog-list/", views.blog_list, name="blog_list"),
     path("admin/blog-delete/<int:id>/", views.blog_delete, name="blog_delete"),
     path("admin/blog-edit/<int:id>/", views.blog_edit, name="blog_edit"),
     path("add_service", views.add_service, name="add_service"),
     path("about/add/", views.add_about, name="add_about"),
   
     path("achievements/", views.achievements_page, name="achievements_page"),
     path('admin/faqs/add/', views.faq_add, name='faq_add'),
     path("timeline/", views.timeline_page, name="timeline_page"),
     path("services-list/", views.services_list, name="services_list"),
     path("delete-service/<int:service_id>/", views.delete_service, name="delete_service"),
     
    #path("ads/", views.ad_list, name="ad_list"),
    path("ads/add/", views.add_ad, name="add_ad"),


   # path("<str:page_type>/<slug:key>/", views.seo_landing_page, name="seo_landing_page"),
    path("services/", views.services_list1, name="services_list1"),
    
    
    path("seo_list", views.seo_list, name="seo_list"),
    path("toggle/<int:pk>/", views.toggle_seo_status, name="seo_toggle"),
    path("delete/<int:pk>/", views.delete_seo_page, name="seo_delete"),
    path("edit/<int:pk>/", views.edit_seo_page, name="seo_edit"),
    
    
     
    path('plans', views.plans_list, name='plans_list'),
    path('plans/add/', views.plan_add, name='plan_add'),
    path('plans/edit/<int:pid>/', views.plan_edit, name='plan_edit'),
    path('addons/add/', views.addon_create, name='addon_create'),
    
    path('addons/add/', views.addon_create, name='addon_create'),
    
    
 
    #path('rental_list', views.rental_list, name='rental_list'),
    # Admin_App/urls.py

    # ... your existing urls ...
    path('residential_list/', views.rental_list, name='residential_list'),

    path('rental_residential_add', views.rental_residential_add, name='rental_residential_add'),
    path('rental/residential/view/<int:pk>/', views.rental_residential_view, name='rental_residential_view'),
    path('rental/residential/edit/<int:pk>/', views.rental_residential_edit, name='rental_residential_edit'),
  #  path('rental/residential/toggle/<int:pk>/', views.rental_residential_toggle, name='rental_residential_toggle'),
  #  path('rental/residential/delete/<int:pk>/', views.rental_residential_delete, name='rental_residential_delete'),
  
  
    path('residential_import_excel/', views.import_residential_excel, name='import_residential_excel'),

    path('residential_download_template/', views.download_residential_template, name='download_residential_template'),
   
   
   
    path('Admin_App/commercial/import-excel/', views.import_commercial_excel, name='import_commercial_excel'),
    path('Admin_App/commercial/download-template/', views.download_commercial_template, name='download_commercial_template'),
    
   # path('commercial/list/',           views.commercial_list,   name='commercial_list'),
    path('commercial/view/<int:pk>/',  views.commercial_view,   name='commercial_view'),
    path('commercial/edit/<int:pk>/',  views.commercial_edit,   name='commercial_edit'),
    path('commercial/delete/<int:pk>/',views.commercial_delete, name='commercial_delete'),
    path('commercial_rental_add', views.commercial_rental_add, name='commercial_rental_add'),


    path('Admin_App/pg/import-excel/',       views.import_pg_excel,       name='import_pg_excel'),
    path('Admin_App/pg/download-template/',  views.download_pg_template,  name='download_pg_template'),
    
    path('Admin_App/pg/delete/<int:pk>/', views.pg_delete, name='pg_delete'),
    
    
      ####################Start Urls Section For Resindential Resale Property #######################################
    
    
   
    path('resale_residential_add',  views.resale_residential_add,    name='resale_residential_add'),
  #  path('resale_residential_list',            views.resale_residential_list,   name='resale_residential_list'),
    path('resale_residential_view/<int:pk>/',   views.resale_residential_view,   name='resale_residential_view'),
    path('resale_residential_delete/<int:pk>/', views.resale_residential_delete, name='resale_residential_delete'),
    
    
    # Excel Import & Sample Download
    path('resale/import-excel/',     views.resale_residential_import_excel,  name='resale_residential_import_excel'),
    path('resale/sample-excel/',     views.resale_residential_sample_excel,  name='resale_residential_sample_excel'),
    
    
    ####################End Urls Section For Resindential Resale Property #######################################
    
    
    
     path('add_commercial_property', views.add_commercial_property, name='add_commercial_property'),
     
    
# ✅ CORRECT — add trailing slash
    # path('commercial/import/', views.import_commercial_data, name='import_commercial_data'),
     path('commercial/import/', views.import_commercial_data, name='import_commercial_data'),
     path('commercial/import/test/', views.import_test_view,            name='import_test_view'),       
     #path('commercial/list/',                   views.commercial_list_view,              name='commercial_list'),
     path('commercial_toggle',                 views.toggle_commercial_property,         name='toggle_commercial_property'),
     path('commercial_delete',                 views.delete_commercial_property,         name='delete_commercial_property'),
     path('commercial_import',                 views.import_commercial_data,             name='import_commercial_data'),
     path('commercial_sample_excel',           views.download_commercial_sample_excel,   name='download_commercial_sample_excel'),
    # path('commercial/view/<int:prop_id>/',     views.view_commercial_property,           name='view_commercial_property'),
    # path('commercial/edit/<int:prop_id>/',     views.edit_commercial_property,           name='edit_commercial_property'),
# ]
    
]





 



   ##########urls for complaint update######

   

   ########## End urls for complaint update######



  
   

   
