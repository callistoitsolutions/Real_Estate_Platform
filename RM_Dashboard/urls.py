from django.contrib import admin
from django.urls import path
from RM_Dashboard import views

urlpatterns = [
      

      ##########urls for Lanlord#####
   
    path('rm_dashboard',views.rm_dashboard,name="rm_dashboard"),


    ############# urls for user logout ######################

    path('User_Logout',views.User_Logout,name="User_Logout"),

    ############ urls for update rm profile #######################

    path('Update_Profile_Rm',views.Update_Profile_Rm,name='Update_Profile_Rm'),

    ########### urls for rental forms list for RM #######################

    path('residential_rm_list',views.residential_rm_list,name="residential_rm_list"),

    ######## urls for rental forms for RM ########################

    path('residential_rm',views.residential_rm,name="residential_rm"),

    ########## urls for commercial rent forms for RM ################

    path('commercial_rm_list',views.commercial_rm_list,name="commercial_rm_list"),

    ############# urls for commercial forms for RM ####################

    path('commercial_rm',views.commercial_rm,name="commercial_rm"),

    ########### urls for pg list forms for RM ###########################

    path('pg_rm_list',views.pg_rm_list,name="pg_rm_list"),

    ########### urls for pg forms for RM ###########################

    path('pg_rm',views.pg_rm,name="pg_rm"),


    ############## urls for resale property list #########################

    path('residential_resale_rm_list',views.residential_resale_rm_list,name="residential_resale_rm_list"),
      
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

     





