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



    ############ urls for Rental Residential Listing ############################

    path('residential_agent',views.residential_agent,name="residential_agent"),
    path('rental_list_agent',views.rental_list_agent,name="rental_list_agent"),


     ############ urls for Rental Residential Listing ############################

    path('commercial_agent',views.commercial_agent,name="commercial_agent"),
    path('commercial_list_agent',views.commercial_list_agent,name="commercial_list_agent"),


     ############ urls for Rental Residential Listing ############################

    path('pg_coliving_agent',views.pg_coliving_agent,name="pg_coliving_agent"),
    path('pg_list_agent',views.pg_list_agent,name="pg_list_agent"),


       ############ urls for Resale Residential Listing ############################


    path('residential_resale_agent',views.residential_resale_agent,name="residential_resale_agent"),
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


 ############ urls for Resale Industrial Plot Listing ############################

   path('industrial_plot_resale_agent',views.industrial_plot_resale_agent,name="industrial_plot_resale_agent"),
   path('industrial_plot_resale_list_agent',views.industrial_plot_resale_list_agent,name="industrial_plot_resale_list_agent"),


 ############ urls for Resale Agricultural Plot Listing ############################
    
   path('agricultural_plot_resale_agent',views.agricultural_plot_resale_agent,name="agricultural_plot_resale_agent"),
   path('agricultural_plot_resale_list_agent',views.agricultural_plot_resale_list_agent,name="agricultural_plot_resale_list_agent"),
    
]

    











    



    
  
     







