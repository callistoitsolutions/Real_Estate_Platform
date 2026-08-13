from django.contrib import admin
from django.urls import path
from Agent_Dashboard import views

urlpatterns = [
      

      ##########urls for Lanlord#####
   
    path('agent_dashboard',views.agent_dashboard,name="agent_dashboard"),
    
    ############ urls for update agent profile ###########################

    path('Update_Profile_Agent',views.Update_Profile_Agent,name='Update_Profile_Agent'),

    ############## urls for assign enquiries to agent #########################

    path('Assign_Enquiry_Agent',views.Assign_Enquiry_Agent,name='Assign_Enquiry_Agent'),

    ############ urls for update property enquiry ############################

    path('update_enquiry_agent/<int:id>',views.update_enquiry_agent,name="update_enquiry_agent"),
    
   # path('Wallet_Recharge_agent',views.Wallet_Recharge_agent,name="Wallet_Recharge_agent"),
    #path('lead_purchase',views.lead_purchase,name="lead_purchase"),
    #path('Commission_Report_Filter',views.Commission_Report_Filter,name="Commission_Report_Filter"),
    path('chat_agent',views.chat_agent,name="chat_agent"),
    path('Sponserproperty',views.Sponserproperty,name="Sponserproperty"),
    
    path("lead-purchase/new/", views.lead_purchase_create, name="lead_purchase_create"),
    path("lead-purchase/", views.lead_purchase_list, name="lead_purchase_list"),
    
 
    path("wallet-recharge/new/", views.wallet_recharge_create, name="wallet_recharge_create"),
    path("wallet-recharge/", views.wallet_recharge_list, name="wallet_recharge_list"),
    
    path("commission-report/", views.commission_report, name="commission_report"),
    
    path('overview/', views.subscription_overview, name='overview'),

    path('signup/submit/', views.signup_submit, name='signup_submit'),
    path('signup/success/<int:pk>/', views.signup_success, name='signup_success'),
    path('inquiry_list', views.inquiry_list, name='inquiry_list'),



    ############ urls Start for Rental Residential Listing For Agent ############################

    path('residential_agent',views.residential_agent,name="residential_agent"),
    path('residential_agent_edit/<str:pk>',views.residential_agent_edit,name="residential_agent_edit"),
    path('residential_list_agent',views.residential_list_agent,name="residential_list_agent"),
    path(
    'rental/residential_view_agent/<str:pk>/',
    views.rental_residential_view_agent,
    name='rental_residential_view_agent'
    ),
   path('residential_add_agent',views.residential_add_agent,name="residential_add_agent"),
    path('residential_import_excel_agent/', views.import_residential_excel_agent, name='import_residential_excel_agent'),

    path('residential_download_template_agent/', views.download_residential_template_agent, name='download_residential_template_agent'),
    path('rental-residential-agent/delete/<str:pk>/',
    views.rental_residential_delete_agent,
    name='rental_residential_delete_agent'
    ),

    path('rental-residential-agent/bulk-delete/', views.rental_bulk_delete_agent, name='rental_bulk_delete_agent'),



    ############ urls End for Rental Residential Listing For Agent ############################



    ############ urls Start for Rental Commercial Listing For Agent ############################

    path('commercial_agent',views.commercial_agent,name="commercial_agent"),
    path('commercial_list_agent',views.commercial_list_agent,name="commercial_list_agent"),
    path('commercial_rental_add_agent', views.commercial_rental_add_agent, name='commercial_rental_add_agent'),

        
    
    path('commercial_agent_edit/<str:pk>', views.commercial_agent_edit, name="commercial_agent_edit"),
    path('commercial/view_agent/<str:pk>/',  views.commercial_view_agent,   name='commercial_view_agent'),
    path('commercial_agent/export/', views.export_commercial_rent_agent, name='export_commercial_rent_agent'),
    #path('commercial-rm/import-excel/', views.import_commercial_rental_excel_rm, name='import_commercial_rental_excel_rm'),
   # path('commercial-rm/commercial/download-template/', views.download_commercial_rental12_template_rm, name='download_commercial_rental12_template_rm'),
    path('commercial-agent/bulk-delete/', views.commercial_bulk_delete_agent, name='commercial_bulk_delete_agent'),
    path('commercial-agent/delete/<str:pk>/', views.commercial_delete_agent, name='commercial_delete_agent'),



    ############ urls END for Rental Commercial Listing For Agent ############################

    
   ########### urls start for pg list forms for agent ###########################

    path('pg_agent_list',views.pg_agent_list,name="pg_agent_list"),

    

    path('pg_coliving_agent',views.pg_coliving_agent,name="pg_coliving_agent"),
    path('add-pg-agent/', views.add_pg_agent, name='add_pg_agent'),
    path('pg-coliving-agent/export/', views.export_pg_coliving_agent, name='export_pg_coliving_agent'),
    path('pg-agent/edit/<str:pk>/', views.pg_agent_edit, name='pg_agent_edit'),
    path('pg-coliving-agent/view/<str:pk>/', views.pg_coliving_view_agent, name='pg_coliving_view_agent'),

    #path('pg-rm/import-excel/',       views.import_pg_excel_rm,       name='import_pg_excel_rm'),
   # path('pg-rm/pg/download-template/',  views.download_pg_template_rm,  name='download_pg_template_rm'),
    path('pg-coliving-agent/bulk-delete/', views.pg_bulk_delete_agent, name='pg_bulk_delete_agent'),
    path(
    'pg-coliving-agent/delete/<str:pk>/',
    views.pg_coliving_delete_agent,
    name='pg_coliving_delete_agent'
    ),
    
########### urls End for pg forms for landlord ###########################


################START URL SECTION RESALE INDUSTRIAL PLOT LISTING Agent ######################################################




    path('industrial_plot_resale_list_agent',views.industrial_plot_resale_list_agent,name="industrial_plot_resale_list_agent"),
    path('industrial_plot_resale_agent',views.industrial_plot_resale_agent,name="industrial_plot_resale_agent"),
    path('industrial-plot-resale-agent/add/', views.industrial_plot_resale_add_agent, name='industrial_plot_resale_add_agent'),
    path('industrial-plot-agent/edit/<str:pk>/', views.industrial_plot_resale_edit_agent, name='industrial_plot_resale_edit_agent'),
    path('industrial-plot-agent/view/<str:pk>/', views.industrial_plot_resale_view_agent, name='industrial_plot_resale_view_agent'),
    path('industrial-plot-agent/delete/<str:pk>/', views.industrial_plot_resale_delete_agent, name='industrial_plot_resale_delete_agent'),
    path('industrial-plot-agent/bulk-delete/', views.industrial_plot_resale_bulk_delete_agent, name='industrial_plot_resale_bulk_delete_agent'),
    path('industrial-plot-resale-agent/export/', views.export_industrial_plot_resale_agent, name='export_industrial_plot_resale_agent'),



 ################END URL SECTION RESALE INDUSTRIAL PLOT LISTING Agent ######################################################

    
 ################Start URL SECTION RESALE Agriculture PLOT LISTING AGENT ######################################################


    path('agricultural_plot_resale_list_agent',views.agricultural_plot_resale_list_agent,name="agricultural_plot_resale_list_agent"),

    path('agricultural_plot_resale_agent',views.agricultural_plot_resale_agent,name="agricultural_plot_resale_agent"),

    path(
        'agricultural-plot-resale-agent/add/',
        views.agricultural_plot_resale_add_agent,
        name='agricultural_plot_resale_add_agent'
    ),

    path(
        'agricultural-plot-resale-agent/edit/<str:pk>/',
        views.agricultural_plot_resale_edit_agent,
        name='agricultural_plot_resale_edit_agent'
    ),
    path(
        'agricultural-plot-resale-agent/delete/<str:pk>/',
         views.agricultural_plot_resale_delete_agent,
        name='agricultural_plot_resale_delete_agent'
    ),

    # Bulk Delete
    path(
        'agricultural-plot-resale-agent/bulk-delete/',
        views.agricultural_plot_resale_bulk_delete_agent,
        name='agricultural_plot_resale_bulk_delete_agent'
    ),


    path(
        'agricultural-plot-resale-agent/export/',
        views.export_agricultural_plot_resale_agent,
        name='export_agricultural_plot_resale_agent'
    ),

    path(
        'agricultural-plot-resale-agent/view/<str:pk>/',
        views.agricultural_plot_resale_view_agent,
        name='agricultural_plot_resale_view_agent'
    ),


   ################End URL SECTION RESALE Agriculture PLOT LISTING Agent ######################################################



       ############ urls for Resale Residential Listing ############################


    path('residential_resale_agent',views.residential_resale_agent,name="residential_resale_agent"),

    ########### urls for view residential resale form ######################

    path('residential_resale_agent_view/<str:id>',views.residential_resale_agent_view,name="residential_resale_agent_view"),

   ########### urls for edit residential resale form ######################

    path('residential_resale_agent_edit/<str:id>',views.residential_resale_agent_edit,name="residential_resale_agent_edit"),

    path('residential_resale_list_agent',views.residential_resale_list_agent,name="residential_resale_list_agent"),


    ############ urls for Resale Commercial Listing ############################


    path('commercial_resale_agent',views.commercial_resale_agent,name="commercial_resale_agent"),
    path('commercial_resale_list_agent',views.commercial_resale_list_agent,name="commercial_resale_list_agent"),


        ############ urls for Resale Industrial Listing ############################


    path('industrial_resale_agent',views.industrial_resale_agent,name="industrial_resale_agent"),
    path('industrial_list_agent',views.industrial_list_agent,name="industrial_list_agent"),

       ############ urls for Resale Agricultural Listing ############################


    path('agricultural_resale_agent',views.agricultural_resale_agent,name="agricultural_resale_agent"),
    path('agricultural_list_agent',views.agricultural_list_agent,name="agricultural_list_agent"),



    ############ urls for Resale Residential Plot Listing ############################


    path('residential_plot_resale_agent',views.residential_plot_resale_agent,name="residential_plot_resale_agent"),
    path('residential_plot_resale_list_agent',views.residential_plot_resale_list_agent,name="residential_plot_resale_list_agent"),



 ############ urls for Resale Commercial Plot Listing ############################

    path('commercial_plot_resale_agent',views.commercial_plot_resale_agent,name="commercial_plot_resale_agent"),

    path('commercial_plot_resale_list_agent',views.commercial_plot_resale_list_agent,name="commercial_plot_resale_list_agent"),


 
    
]

    











    



    
  
     







