from django.contrib import admin
from django.urls import path
from RM_Dashboard import views

urlpatterns = [
      

      ##########urls for Lanlord#####
   
    path('rm_dashboard',views.rm_dashboard,name="rm_dashboard"),


    ############# urls for user logout ######################

    path('User_Logout',views.User_Logout,name="User_Logout"),
      
    path('affilate_page',views.affilate_page,name="affilate_page"),
    

    path('r/<str:code>/', views.referral_redirect, name='referral_redirect'),
    path('create-link/', views.create_affiliate_link, name='create_affiliate_link'),
    path('request-payout/', views.request_payout, name='request_payout'),
    path('admin-create-link/', views.admin_create_affiliate_link, name='admin_create_affiliate_link'),
   # path('rm-dashboard/', views.rm_dashboard, name='rm_dashboard'),
    path('user-links/', views.user_affiliate_links, name='user_affiliate_links'),
    path('admin/affiliate/<str:code>/', views.admin_affiliate_detail, name='admin_affiliate_detail'),


   # path('Lead_Status_Update_rm',views.Lead_Status_Update_rm,name="Lead_Status_Update_rm"),
  #  path('Add_Lead_Note',views.Add_Lead_Note,name="Add_Lead_Note"),
#path('Reassign_Lead',views.Reassign_Lead,name="Reassign_Lead"),
   # path('Commission_Claim',views.Commission_Claim,name="Commission_Claim"),
 #  path('reffrel_rm',views.reffrel_rm,name="reffrel_rm"),
   
    # RM
  #  path('rm/referral/new/', views.referral_create, name='rm_referral_new'),
  #  path('rm/referrals/', views.rm_my_referrals, name='rm_my_referrals'),

    # Admin (monitor only)
   # path('admin/referrals/', views.admin_monitor, name='admin_monitor'),

    # SuperAdmin review/approve
   # path('superadmin/referral/<int:referral_id>/', views.superadmin_review, name='superadmin_review'),
   # path('superadmin/referral/<int:referral_id>/closing_report/', views.download_closing_report, name='download_closing_report'),
]

     





