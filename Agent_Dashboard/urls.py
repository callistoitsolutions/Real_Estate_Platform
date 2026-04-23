from django.contrib import admin
from django.urls import path
from Agent_Dashboard import views

urlpatterns = [
      

      ##########urls for Lanlord#####
   
    path('agent_dashboard',views.agent_dashboard,name="agent_dashboard"),
    
    ############ urls for update agent profile ###########################

    path('Update_Profile_Agent',views.Update_Profile_Agent,name='Update_Profile_Agent'),
    
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

]

    
  
     







