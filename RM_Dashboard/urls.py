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

    ############## urls for assign enquiries to rm #########################

    path('Assign_Enquiry_Rm',views.Assign_Enquiry_Rm,name='Assign_Enquiry_Rm'),

    ############ urls for ajax for datewise filter for user ###################

    path('date_property_filter_user',views.date_property_filter_user,name="date_property_filter_user"),

    ############ urls for update property enquiry ############################

    path('update_enquiry_rm/<int:id>',views.update_enquiry_rm,name="update_enquiry_rm"),

    ########### urls for rental forms list for RM #######################

    path('residential_rm_list',views.residential_rm_list,name="residential_rm_list"),

    ######## urls for rental forms for RM ########################

    path('residential_rm',views.residential_rm,name="residential_rm"),
    path('residential_add_rm',views.residential_add_rm,name="residential_add_rm"),

    ############# urls for rental edit forms for RM ###################

       

    path('residential_rm_edit/<str:pk>',views.residential_rm_edit,name="residential_rm_edit"),

    ############# urls for rental Residential delete  for RM ###################

    path(
    'rental-residential-rm/delete/<str:pk>/',
    views.rental_residential_delete_rm,
    name='rental_residential_delete_rm'
    ),

    path('rental-residential-rm/bulk-delete/', views.rental_bulk_delete_rm, name='rental_bulk_delete_rm'),

 ############# urls for rental view forms for RM ###################

    path(
    'rental/residential_view_rm/<str:pk>/',
    views.rental_residential_view_rm,
    name='rental_residential_view_rm'
    ),


    path('residential_import_excel_rm/', views.import_residential_excel_rm, name='import_residential_excel_rm'),

    path('residential_download_template_rm/', views.download_residential_template_rm, name='download_residential_template_rm'),


    ########## urls Start for Rental commercial Listing Module for RM #####################################

    path('commercial_rm_list',views.commercial_rm_list,name="commercial_rm_list"),
    path('commercial_rm',views.commercial_rm,name="commercial_rm"),
    path('commercial_rental_add_rm', views.commercial_rental_add_rm, name='commercial_rental_add_rm'),
    
    path('commercial_rm_edit/<str:pk>', views.commercial_rm_edit, name="commercial_rm_edit"),
    path('commercial/view_rm/<str:pk>/',  views.commercial_view_rm,   name='commercial_view_rm'),
    path('commercial_rm/export/', views.export_commercial_rent_rm, name='export_commercial_rent_rm'),
    path('commercial-rm/import-excel/', views.import_commercial_rental_excel_rm, name='import_commercial_rental_excel_rm'),
    path('commercial-rm/commercial/download-template/', views.download_commercial_rental12_template_rm, name='download_commercial_rental12_template_rm'),
    path('commercial-rm/bulk-delete/', views.commercial_bulk_delete_rm, name='commercial_bulk_delete_rm'),
    path('commercial-rm/delete/<str:pk>/', views.commercial_delete_rm, name='commercial_delete_rm'),



    ########## urls End for Rental commercial Listing Module for RM ##################################




    ########### urls Start Rental pg listing module for RM ###########################

    path('pg_rm_list',views.pg_rm_list,name="pg_rm_list"),

  

    path('pg_rm',views.pg_rm,name="pg_rm"),
    path('add-pg-rm/', views.add_pg_rm, name='add_pg_rm'),
    path('pg-coliving-rm/export/', views.export_pg_coliving_rm, name='export_pg_coliving_rm'),
    path('pg-rm/edit/<str:pk>/', views.pg_rm_edit, name='pg_rm_edit'),
    path('pg-coliving-rm/view/<str:pk>/', views.pg_coliving_view_rm, name='pg_coliving_view_rm'),

    path('pg-rm/import-excel/',       views.import_pg_excel_rm,       name='import_pg_excel_rm'),
    path('pg-rm/pg/download-template/',  views.download_pg_template_rm,  name='download_pg_template_rm'),
    path('pg-coliving-rm/bulk-delete/', views.pg_bulk_delete_rm, name='pg_bulk_delete_rm'),
    path(
    'pg-coliving-rm/delete/<str:pk>/',
    views.pg_coliving_delete_rm,
    name='pg_coliving_delete_rm'
    ),

      ########### urls End Rental pg listing module for RM ###########################




 ################START URL SECTION RESALE INDUSTRIAL PLOT LISTING RM ######################################################




    path('industrial_plot_resale_list_rm',views.industrial_plot_resale_list_rm,name="industrial_plot_resale_list_rm"),
    path('industrial_plot_resale_rm',views.industrial_plot_resale_rm,name="industrial_plot_resale_rm"),
    path('industrial-plot-resale-rm/add/', views.industrial_plot_resale_add_rm, name='industrial_plot_resale_add_rm'),
    path('industrial-plot-rm/edit/<str:pk>/', views.industrial_plot_resale_edit_rm, name='industrial_plot_resale_edit_rm'),
    path('industrial-plot-rm/view/<str:pk>/', views.industrial_plot_resale_view_rm, name='industrial_plot_resale_view_rm'),
    path('industrial-plot-rm/delete/<str:pk>/', views.industrial_plot_resale_delete_rm, name='industrial_plot_resale_delete_rm'),
    path('industrial-plot-rm/bulk-delete/', views.industrial_plot_resale_bulk_delete_rm, name='industrial_plot_resale_bulk_delete_rm'),
    path('industrial-plot-resale-rm/export/', views.export_industrial_plot_resale_rm, name='export_industrial_plot_resale_rm'),



 ################END URL SECTION RESALE INDUSTRIAL PLOT LISTING RM ######################################################

    
 ################Start URL SECTION RESALE Agriculture PLOT LISTING RM ######################################################


    path('agricultural_plot_resale_list_rm',views.agricultural_plot_resale_list_rm,name="agricultural_plot_resale_list_rm"),

    path('agricultural_plot_resale_rm',views.agricultural_plot_resale_rm,name="agricultural_plot_resale_rm"),

    path(
        'agricultural-plot-resale-rm/add/',
        views.agricultural_plot_resale_add_rm,
        name='agricultural_plot_resale_add_rm'
    ),

    path(
        'agricultural-plot-resale-rm/edit/<str:pk>/',
        views.agricultural_plot_resale_edit_rm,
        name='agricultural_plot_resale_edit_rm'
    ),
    path(
        'agricultural-plot-resale-rm/delete/<str:pk>/',
        views.agricultural_plot_resale_delete_rm,
        name='agricultural_plot_resale_delete_rm'
    ),

    # Bulk Delete
    path(
        'agricultural-plot-resale-rm/bulk-delete/',
        views.agricultural_plot_resale_bulk_delete_rm,
        name='agricultural_plot_resale_bulk_delete_rm'
    ),


    path(
        'agricultural-plot-resale-rm/export/',
        views.export_agricultural_plot_resale_rm,
        name='export_agricultural_plot_resale_rm'
    ),

    path(
        'agricultural-plot-resale-rm/view/<str:pk>/',
        views.agricultural_plot_resale_view_rm,
        name='agricultural_plot_resale_view_rm'
    ),


   ################End URL SECTION RESALE Agriculture PLOT LISTING RM ######################################################


    ############## urls for resale property list #########################

    path('residential_resale_rm_list',views.residential_resale_rm_list,name="residential_resale_rm_list"),

    ########### urls for resale property form residential ################

    path('residential_resale_rm',views.residential_resale_rm,name="residential_resale_rm"),

    ############# urls for update resale property form residential ####################

    path('residential_resale_rm_update/<str:id>',views.residential_resale_rm_update,name="residential_resale_rm_update"),

    ######### urls for resale commercial property list #########################

    path('commercial_resale_rm_list',views.commercial_resale_rm_list,name="commercial_resale_rm_list"),

    ######## urls for resale property from commercial ######################

    path('commercial_resale_rm',views.commercial_resale_rm,name="commercial_resale_rm"),

    ######### urls for resale plot property list #######################

    path('plot_resale_rm_list',views.plot_resale_rm_list,name="plot_resale_rm_list"),

    ########## urls for resale property from plot #########################

    path('plot_resale_rm',views.plot_resale_rm,name="plot_resale_rm"),

    ############ urls for residential plot list from rm  #########################

    path('plot_resale_res_rm_list',views.plot_resale_res_rm_list,name="plot_resale_res_rm_list"),

    ############## urls for residential plot list form ########################

    path('plot_resale_res_rm',views.plot_resale_res_rm,name="plot_resale_res_rm"),

    ########### urls for commercial plot list for rm #######################

    path('plot_resale_comm_rm_list',views.plot_resale_comm_rm_list,name="plot_resale_comm_rm_list"),

    ############### urls for commercial plot list form #######################

    path('plot_resale_comm_rm',views.plot_resale_comm_rm,name="plot_resale_comm_rm"),

    ########### urls for industrial plot list for rm #######################

    path('plot_resale_ind_rm_list',views.plot_resale_ind_rm_list,name="plot_resale_ind_rm_list"),

    ############# urls for industrial plot for rm #####################

    path('plot_resale_ind_rm',views.plot_resale_ind_rm,name="plot_resale_ind_rm"),

    ############ urls for resale industrial property list ##########################

    path('industry_resale_rm_list',views.industry_resale_rm_list,name="industry_resale_rm_list"),

    ######## urls for industrial resale property form ######################

    path('industry_resale_rm',views.industry_resale_rm,name="industry_resale_rm"),

    ########### urls for agricultural plot list for rm #######################

    path('plot_resale_agri_rm_list',views.plot_resale_agri_rm_list,name="plot_resale_agri_rm_list"),

    ########### urls for agricultural plot list form  #######################

    path('plot_resale_agri_rm',views.plot_resale_agri_rm,name="plot_resale_agri_rm"),

    ########## urls for resale agricultural property list ###################

    path('agriculture_resale_rm_list',views.agriculture_resale_rm_list,name="agriculture_resale_rm_list"),

    ######### urls for agricutural resale property form ######################

    path('agriculture_resale_rm',views.agriculture_resale_rm,name="agriculture_resale_rm"),
      
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

     





