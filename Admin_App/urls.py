from django.contrib import admin
from django.urls import path
from Admin_App import views

urlpatterns = [
      

      ##########urls for manage crime officer#####
     path('admin_page',views.admin_page,name="admin_page"),
     path('index3',views.index3,name="index3"),
     path('index2',views.index2,name="index2"),

     ############# Impersonation Url for super admin ###############

    path('Impersonate', views.Impersonate, name='Impersonate'),

    ############ urls for live statistical tracking ###################

    path('api/live-traffic/', views.get_live_traffic, name='api_live_traffic'),

    ########### urls for global search ###########################

    path('api/global-search/', views.global_search, name='global_search'),

    ############ urls for notifications ############################

    path('api/notifications/today/', views.get_todays_notifications, name='get_todays_notifications'),

     ############ urls for rental forms ##########################

     path('residential',views.residential,name="residential"),
     path('commercial',views.commercial,name="commercial"),
     path('pg_coliving',views.pg_coliving,name="pg_coliving"),


     ############ urls for contact enquiries list ##########################

     path('Contact_Enquiries_List',views.Contact_Enquiries_List,name="Contact_Enquiries_List"),

     ########### urls for delete contact enquiry ##########################

     path('Delete_Contact_Enquiry',views.Delete_Contact_Enquiry,name='Delete_Contact_Enquiry'),

     ############ urls for view contact enquiries ########################

     path('View_Contact_Enquiry/<int:id>',views.View_Contact_Enquiry,name="View_Contact_Enquiry"),

     ######## urls for upload contact enquiries data via excel ###############

     path('Contacts_Data',views.Contacts_Data,name="Contacts_Data"),

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

     ######### urls for delete vendor service details #####################

    path('Delete_Services',views.Delete_Services,name='Delete_Services'),

     ############# urls for update service details #######################

    path('Update_Services/<int:id>',views.Update_Services,name='Update_Services'),

    ########### urls for normal faqs list ################################

    path('Faqs_List',views.Faqs_List,name="Faqs_List"),

    ############# urls for add normal faqs ############################

    path('Add_FAQ',views.Add_FAQ,name="Add_FAQ"),

    ############## urls for ajax for normal faqs ####################

    path('Faq_Ajax',views.Faq_Ajax,name="Faq_Ajax"),

    ############# urls for upload faqs data via excel #####################

    path('Faq_Data',views.Faq_Data,name="Faq_Data"),

    ############## urls for delete faqs ############################

    path('Delete_Faqs',views.Delete_Faqs,name="Delete_Faqs"),

    ############ urls for update faqs #######################

    path('Update_Faqs/<int:id>',views.Update_Faqs,name="Update_Faqs"),

    ############# urls for subscription packages list ######################

    path('Subscriptions_Packages_List',views.Subscriptions_Packages_List,name="Subscriptions_Packages_List"),

    ########### urls for ajax for add/edit packages ####################

    path('Packages_Ajax',views.Packages_Ajax,name="Packages_Ajax"),

    ########### urls for delete packages #########################

    path('Delete_Packages',views.Delete_Packages,name="Delete_Packages"),

    ############ urls for update packages ######################

    path('Update_Packages/<int:id>',views.Update_Packages,name="Update_Packages"),

    ############ urls for subscription plan types list ####################

    path('Subscriptions_Plans_List',views.Subscriptions_Plans_List,name="Subscriptions_Plans_List"),

    ########### urls for ajax for add/edit plans ####################

    path('Plans_Ajax',views.Plans_Ajax,name="Plans_Ajax"),

    ############# urls for delete plans #####################

    path('Delete_Plans',views.Delete_Plans,name="Delete_Plans"),

    ########## urls for update plans ##############################

    path('Update_Plans/<int:id>',views.Update_Plans,name="Update_Plans"),

     ############# urls for subscriptions list ###########################

    path('Subscriptions_List',views.Subscriptions_List,name="Subscriptions_List"),

     ############# urls for add subscriptions ###########################

    path('Add_Subscriptions',views.Add_Subscriptions,name="Add_Subscriptions"),

     ########### urls for ajax for add/update subscriptions ##################

    path('Subscriptions_Ajax',views.Subscriptions_Ajax,name="Subscriptions_Ajax"),

     ############# urls for delete subscriptions ##########################

    path('Delete_Subscriptions',views.Delete_Subscriptions,name="Delete_Subscriptions"),

     ############# urls for update subscriptions #########################

    path('Update_Subscriptions/<int:id>',views.Update_Subscriptions,name="Update_Subscriptions"),

     ############ urls for upload subscription details via excel ########################

    path('Subscriptions_Data',views.Subscriptions_Data,name="Subscriptions_Data"),

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

     ############# urls for plot residential list ######################

     path('residential_plot_resale_list',views.residential_plot_resale_list,name="residential_plot_resale_list"),

     ########## urls for plot residdential form #######################

     path('residential_plot_resale',views.residential_plot_resale,name="residential_plot_resale"),

     ############ urls for plot commercial list ########################

     path('commercial_plot_resale_list',views.commercial_plot_resale_list,name="commercial_plot_resale_list"),

     ######### urls for plot commercial form #############################

     path('commercial_plot_resale',views.commercial_plot_resale,name="commercial_plot_resale"),

     ############## urls for plot industrial list ##########################

     path('industrial_plot_resale_list',views.industrial_plot_resale_list,name="industrial_plot_resale_list"),

     ############## urls for plot industrial form #######################

     path('industrial_plot_resale',views.industrial_plot_resale,name="industrial_plot_resale"),

     ########## urls for plot agricultural list  ######################
     
     path('agricultural_plot_resale_list',views.agricultural_plot_resale_list,name="agricultural_plot_resale_list"),

     ############## urls for plot agricultural form #######################

     path('agricultural_plot_resale',views.agricultural_plot_resale,name="agricultural_plot_resale"),

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

    ########### urls for ajax for delete bulk users #########################

    path('Users_Bulk_Delete', views.Users_Bulk_Delete, name='Users_Bulk_Delete'),



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
     
     
  
   
     path("about/add/", views.add_about, name="add_about"),
   
     path("achievements/", views.achievements_page, name="achievements_page"),
     path('admin/faqs/add/', views.faq_add, name='faq_add'),
     path("timeline/", views.timeline_page, name="timeline_page"),
   
     
    #path("ads/", views.ad_list, name="ad_list"),
    path("ads/add/", views.add_ad, name="add_ad"),


   # path("<str:page_type>/<slug:key>/", views.seo_landing_page, name="seo_landing_page"),
   
    
    
    path("seo_list", views.seo_list, name="seo_list"),
    path("toggle/<int:pk>/", views.toggle_seo_status, name="seo_toggle"),
    path("delete/<int:pk>/", views.delete_seo_page, name="seo_delete"),
    path("edit/<int:pk>/", views.edit_seo_page, name="seo_edit"),
    
    
     
    path('plans', views.plans_list, name='plans_list'),
    path('plans/add/', views.plan_add, name='plan_add'),
    path('plans/edit/<int:pid>/', views.plan_edit, name='plan_edit'),
    path('addons/add/', views.addon_create, name='addon_create'),
    
    path('addons/add/', views.addon_create, name='addon_create'),
    

################## START URL SECTION OF RENTAL RESIDENTIAL LISTING ###############################

    path('residential_list/', views.rental_list, name='residential_list'),

    path('rental_reports', views.rental_reports, name='rental_reports'),

    path('rental_residential_add', views.rental_residential_add, name='rental_residential_add'),

    path('rental/residential/edit/<str:pk>/', views.rental_residential_edit, name='rental_residential_edit'),

    ############ urls to get user details according to listing by ###############

    path('get_user_data',views.get_user_data,name='get_user_data'),

    

    path('system-audit-logs/', views.system_audit_logs, name='system_audit_logs'),
    path('rental-residential/bulk-delete/', views.rental_bulk_delete, name='rental_bulk_delete'),
    path('global_recycle_bin', views.global_recycle_bin, name='global_recycle_bin'),
    path('bulk-restore/<str:property_type>/', views.bulk_restore_route, name='bulk_restore_route'),

    #path('rental-residential/recycle-bin/', views.rental_recycle_bin, name='rental_recycle_bin'),
    path(
    'rental-residential/restore/<str:pk>/',
    views.rental_restore,
    name='rental_restore'
    ),

    path(
    'rental-residential/hard-delete/<str:pk>/',
    views.rental_hard_delete,
    name='rental_hard_delete'
    ),

    path(
    'rental-residential/delete/<str:pk>/',
    views.rental_residential_delete,
    name='rental_residential_delete'
    ),

    path(
    'rental/residential/view/<str:pk>/',
    views.rental_residential_view,
    name='rental_residential_view'
    ),

    path('rental-residential/activity-logs/', views.rental_residential_logs_view, name='rental_residential_logs'),
  
    path('bulk-hard-delete/<str:property_type>/', views.bulk_hard_delete_properties, name='bulk_hard_delete_properties'),
    path('residential_import_excel/', views.import_residential_excel, name='import_residential_excel'),

    path('residential_download_template/', views.download_residential_template, name='download_residential_template'),

    path('get_user_data',views.get_user_data,name='get_user_data'),
   
   ################## END URL SECTION OF RENTAL RESIDENTIAL LISTING ###############################


#########################START URL SECTION OF COMMERICIAL RENTAL LISTING##############################
   
    path('Admin_App/commercial/import-excel/', views.import_commercial_rental_excel, name='import_commercial_rental_excel'),
    path('Admin_App/commercial/download-template/', views.download_commercial_rental12__template, name='download_commercial_rental12__template'),
    
    path('commercial/list/',           views.commercial_list,   name='commercial_list'),
    path('commercial_reports',           views.commercial_reports,   name='commercial_reports'),
  
    path('commercial/bulk-delete/', views.commercial_bulk_delete, name='commercial_bulk_delete'),
    path('commercial/restore/<str:id>/', views.commercial_restore, name='commercial_restore'),
    path('commercial/hard-delete/<str:id>/', views.commercial_hard_delete, name='commercial_hard_delete'),
    path('commercial/view/<str:pk>/',  views.commercial_view,   name='commercial_view'),
    path('commercial/edit/<str:pk>/',  views.commercial_edit,   name='commercial_edit'),
    path('commercial/delete/<str:pk>/', views.commercial_delete, name='commercial_delete'),
    path('commercial_rental_add', views.commercial_rental_add, name='commercial_rental_add'),
    

    path('commercial/export/', views.export_commercial_rent, name='export_commercial_rent'),



#########################END URL SECTION OF COMMERICIAL RENTAL LISTING##############################


    ##############################START URL SECTION RENTAL PG_COLIVING LISTING#####################

    path('add-pg/', views.add_pg, name='add_pg'),
    path('Admin_App/pg/import-excel/',       views.import_pg_excel,       name='import_pg_excel'),
    path('Admin_App/pg/download-template/',  views.download_pg_template,  name='download_pg_template'),
   
    path('pg-coliving/export/', views.export_pg_coliving, name='export_pg_coliving'),

    path('pg-coliving/restore/<str:id>/', views.pg_restore, name='pg_restore'),
    path('pg-coliving/hard-delete/<str:id>/', views.pg_hard_delete, name='pg_hard_delete'),
    path('pg-coliving/bulk-delete/', views.pg_bulk_delete, name='pg_bulk_delete'),

    path('pg-coliving/view/<str:pk>/', views.pg_coliving_view, name='pg_coliving_view'),

    path(
    'pg-coliving/delete/<str:pk>/',
    views.pg_coliving_delete,
    name='pg_coliving_delete'
    ),


  
    # 1. Route to render the HTML Edit Form Page interface (GET request)
    path('Admin_App/pg/edit/page/<str:property_id>/', views.pg_edit_page, name='pg_edit_page'),

    # 2. Route to process the Form save transaction data (POST request)
    path('Admin_App/pg/edit/save/<str:property_id>/', views.pg_edit, name='pg_edit'),

    
     ##############################END URL SECTION RENTAL PG_COLIVING LISTING#####################


      ####################Start Urls Section For Resindential Resale Property #######################################
    

    path('resale-residential/bulk-delete/', views.resale_residential_bulk_delete, name='resale_residential_bulk_delete'),

   
    path('resale_residential_add',  views.resale_residential_add,    name='resale_residential_add'),
  #  path('resale_residential_list',            views.resale_residential_list,   name='resale_residential_list'),
    path('resale_residential_view/<str:pk>/',   views.resale_residential_view,   name='resale_residential_view'),
    path('resale_residential_delete/<str:pk>/', views.resale_residential_delete, name='resale_residential_delete'),
    path(
    'resale-residential/edit/<str:id>/',
    views.resale_residential_edit,
    name='resale_residential_edit'
    ),
    path('resale-residential/restore/<str:id>/', views.resale_restore, name='resale_restore'),
    path('resale-residential/hard-delete/<str:id>/', views.resale_hard_delete, name='resale_hard_delete'),
    
    # Excel Import & Sample Download
    path('resale/import-excel/',     views.resale_residential_import_excel,  name='resale_residential_import_excel'),
    path('resale/sample-excel/',     views.resale_residential_sample_excel,  name='resale_residential_sample_excel'),


    path('export_resale_csv/', views.export_resale_csv, name='export_resale_csv'),
    path('export_resale_excel/', views.export_resale_excel, name='export_resale_excel'),

    
    
    ####################End Urls Section For Resindential Resale Property #######################################
    
    #################### START Urls Section For Commercial Resale Property #######################################
    
 
    path('commercial/export/excel/', views.export_commercial_resale_excel, name='export_commercial_resale_excel'),
    path('commercial/export/csv/', views.export_commercial_resale_csv, name='export_commercial_resale_csv'),

     path('add_commercial_property', views.add_commercial_property, name='add_commercial_property'),

     path('commercial-resale/import/', views.import_commercial_data, name='import_commercial_data'),
     path('commercial-resale/download-sample/', views.download_commercial_sample_excel, name='download_commercial_sample_excel'),
     path('commercial/import/test/', views.import_test_view,            name='import_test_view'),       
     path('commercial_toggle',                 views.toggle_commercial_property,         name='toggle_commercial_property'),
     path('commercial_delete',                 views.delete_commercial_property,         name='delete_commercial_property'),
     path('commercial_import',                 views.import_commercial_data,             name='import_commercial_data'),
     
     path('commercial-resale/bulk-delete/', views.commercial_resale_bulk_delete, name='commercial_resale_bulk_delete'),
    
    path('commercial-resale/restore/<str:id>/', views.commercial_resale_restore, name='commercial_resale_restore'),
    path('commercial-resale/hard-delete/<str:id>/', views.commercial_resale_hard_delete, name='commercial_resale_hard_delete'),

    path('commercial-resale/view/<str:id>/', views.commercial_resale_view, name='commercial_resale_view'),
    path('commercial-resale/edit/<str:id>/', views.commercial_resale_edit, name='commercial_resale_edit'),


    ####################End Urls Section For Commercial Resale Property #######################################



#######################START URL SECTION RESALE PLOT LISTING###############


    path('plot-sale/add/', views.plot_sale_add, name='plot_sale_add'),
   
    

    path('plot-sale/bulk-delete/', views.plot_sale_bulk_delete, name='plot_sale_bulk_delete'),
       path('plots/template/download/',
         views.download_plot_resale_template,
         name='download_plot_resale_template'),
 
    path('plots/import/',
         views.import_plot_resale_excel,
         name='import_plot_resale_excel'),
 
    # ── NEW ──────────────────────────────────────────────────
    path('plots/export/',
         views.export_plot_resale_excel,
         name='export_plot_resale_excel'),

 
    path('plot-sale/restore/<str:id>/', views.plot_sale_restore, name='plot_sale_restore'),
    path('plot-sale/hard-delete/<str:id>/', views.plot_sale_hard_delete, name='plot_sale_hard_delete'),

    path('plot-resale/view/<str:id>/', views.plot_sale_view, name='plot_sale_view'),
    

    path(
    'plot-resale/delete/<str:id>/',
    views.plot_sale_delete,
    name='plot_sale_delete'
    ),
    path( 'plot-sale/edit/<str:plot_property_id>/',views.plot_sale_edit,name='plot_sale_edit'),



#######################END URL SECTION RESALE PLOT LISTING###############


##################START URL SECTION RESALE INDUSTRIAL LISTING###########################



    path('industrial-resale/add/', views.industrial_resale_add, name='industrial_resale_add'),
    
    # URL for Editing Industrial Resale
    path('industrial-resale/edit/<str:id>/', views.industrial_resale_edit, name='industrial_resale_edit'),

    
    path('industrial-resale/view/<str:id>/', views.industrial_resale_view, name='industrial_resale_view'),

    path('industrial-resale/restore/<str:id>/', views.industrial_resale_restore, name='industrial_resale_restore'),
    path('industrial-resale/hard-delete/<str:id>/', views.industrial_resale_hard_delete, name='industrial_resale_hard_delete'),

    path('industrial-resale/delete/<str:id>/', views.industrial_resale_delete, name='industrial_resale_delete'),

    path('industrial-resale/bulk-delete/', views.industrial_bulk_delete, name='industrial_bulk_delete'),
  
    # ... your existing urls ...
    path('industrial-resale/download-template/', views.download_industrial_resale_template, name='download_industrial_resale_template'),
    path('industrial-resale/import/', views.import_industrial_resale_excel, name='import_industrial_resale_excel'),


################END URL SECTION RESALE INDUSTRIAL LISTING######################################################

    
    ################START URL SECTION RESALE AGRICULTURAL LISTING######################################################
  
    path('admin/add-agricultural-property/', views.add_agricultural_property, name='add_agricultural_property'),
  
    path('admin/edit-agricultural/<str:pk>/', views.edit_agricultural_property, name='edit_agricultural_property'),

   
    path('agricultural-resale/bulk-delete/', views.agricultural_bulk_delete, name='agricultural_bulk_delete'),
    path('delete-agricultural/<str:pk>/', views.delete_agricultural_property, name='delete_agricultural_property'),

    path('admin/view-agricultural/<str:pk>/', views.view_agricultural_property, name='view_agricultural_property'),
    
    path('import_agricultural_resale_excel', views.import_agricultural_resale_excel, name='import_agricultural_resale_excel'),
    
    path('admin/download-agri-sample/', views.download_agri_sample_excel, name='download_agri_sample_excel'),

    path('export/agricultural-resale/excel/', views.export_agricultural_resale_excel, name='export_agricultural_resale_excel'),
    
    # CSV Export URL
    path('export/agricultural-resale/csv/', views.export_agricultural_resale_csv, name='export_agricultural_resale_csv'),

    


    path('agricultural-resale/restore/<str:id>/', views.agricultural_resale_restore, name='agricultural_resale_restore'),
    path('agricultural-resale/hard-delete/<str:id>/', views.agricultural_resale_hard_delete, name='agricultural_resale_hard_delete'),
    ################END URL SECTION RESALE AGRICULTURAL LISTING######################################################


#########################START URL SECTION Blogs##############################################################

     path("admin/add-blog/", views.add_blog, name="add_blog"),
     path("admin/blog-list/", views.blog_list, name="blog_list"),
     path("admin/blog-delete/<int:id>/", views.blog_delete, name="blog_delete"),
     path("admin/blog-edit/<int:id>/", views.blog_edit, name="blog_edit"),
  
    path('services/edit/<int:id>/', views.edit_service, name='edit_service'),


  
    path('blogs/import/', views.import_blog_excel, name='import_blog_excel'),


#########################START URL SECTION Blogs##############################################################



#########################START URL SECTION Services Landing Page##############################################################


     path("add_service", views.add_service, name="add_service"),
    
   
     path('services/import/', views.import_services_excel, name='import_services_excel'),
     path("services-list/", views.services_list, name="services_list"),
     path("delete-service/<int:service_id>/", views.delete_service, name="delete_service"),
     path("services/", views.services_list1, name="services_list1"),
    
    
    
    
    
     
 

#########################END URL SECTION Services Landing Page##############################################################

]






 



 



  
   

   
