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

     ############# urls for rental property list ########################

     path('residential_list',views.residential_list,name="residential_list"),
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

    ######### urls for display landlords list #################

    path('Landlord_List',views.Landlord_List,name="Landlord_List"),

    ########## urls for add landlords #######################

    path('Add_Landlord',views.Add_Landlord,name="Add_Landlord"),

    ############ urls for display tenants list ####################

    path('Tenant_List',views.Tenant_List,name="Tenant_List"),

    ########## urls for add tenants ########################

    path('Add_Tenant',views.Add_Tenant,name="Add_Tenant"),

    ############## urls for display buyers list #####################

    path('Buyer_List',views.Buyer_List,name="Buyer_List"),

    ############## urls for add buyers #########################

    path('Add_Buyer',views.Add_Buyer,name="Add_Buyer"),

    ############# urls for display agents list ####################

    path('Agent_List',views.Agent_List,name="Agent_List"),

    ############# urls for add agents ####################

    path('Add_Agent',views.Add_Agent,name="Add_Agent"),

    ########### urls for display agency list ##############

    path('Agency_List',views.Agency_List,name="Agency_List"),

    ########### urls for add agency #######################

    path('Add_Agency',views.Add_Agency,name="Add_Agency"),

    ########### urls for display vendors list ####################

    path('Vendor_List',views.Vendor_List,name="Vendor_List"),

    ########### urls for add vendors ####################

    path('Add_Vendor',views.Add_Vendor,name="Add_Vendor"),
     

     
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
]


 



   ##########urls for complaint update######

   

   ########## End urls for complaint update######



  
   

   
