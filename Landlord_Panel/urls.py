from django.contrib import admin
from django.urls import path
from Landlord_Panel import views

urlpatterns = [
      

      ##########urls for Lanlord#####
   
     path('landlord_dashboard',views.landlord_dashboard,name="landlord_dashboard"),
  


     ############# urls for update landlord profile page #####################

     path('Update_Profile_Landlord',views.Update_Profile_Landlord,name='Update_Profile_Landlord'),



   


   ######## urls Start for rental residential listing upload & download excel  for landlord ########################

    path('download-residential-template-landlord/', views.download_residential_template_landlord, name='download_residential_template_landlord'),
    path('import-residential-excel-landlord/', views.import_residential_excel_landlord, name='import_residential_excel_landlord'),

    

    ############ urls for edit rental residential listing module for landlord #################
    

    path('residential_landlord_edit/<str:pk>',views.residential_landlord_edit,name="residential_landlord_edit"),
    
    path('residential_landlord',views.residential_landlord,name="residential_landlord"),
    path('residential_landlord_view/<str:pk>',views.residential_landlord_view,name="residential_landlord_view"),

    path('residential_landlord_list',views.residential_landlord_list,name="residential_landlord_list"),
    path('residential_add_landlord',views.residential_add_landlord,name="residential_add_landlord"),
    
    path('rental-residential-landlord/delete/<str:pk>/',
    views.rental_residential_delete_landlord,
    name='rental_residential_delete_landlord'
    ),

    path('rental-residential-landlord/bulk-delete/', views.rental_bulk_delete_landlord, name='rental_bulk_delete_landlord'),


     ############ urls End for edit rental residential listing module for landlord #################

   

    ########## urls Starts for commercial rental listing Module for landlord ################



    path('commercial_landlord_list',views.commercial_landlord_list,name="commercial_landlord_list"),


    path('commercial_landlord',views.commercial_landlord,name="commercial_landlord"),
    path('commercial_rental_add_landlord', views.commercial_rental_add_landlord, name='commercial_rental_add_landlord'),

        
    
    path('commercial_landlord_edit/<str:pk>', views.commercial_landlord_edit, name="commercial_landlord_edit"),
    path('commercial/view_landlord/<str:pk>/',  views.commercial_view_landlord,   name='commercial_view_landlord'),
    path('commercial_landlord/export/', views.export_commercial_rent_landlord, name='export_commercial_rent_landlord'),
    #path('commercial-rm/import-excel/', views.import_commercial_rental_excel_rm, name='import_commercial_rental_excel_rm'),
   # path('commercial-rm/commercial/download-template/', views.download_commercial_rental12_template_rm, name='download_commercial_rental12_template_rm'),
    path('commercial-landlord/bulk-delete/', views.commercial_bulk_delete_landlord, name='commercial_bulk_delete_landlord'),
    path('commercial-landlord/delete/<str:pk>/', views.commercial_delete_landlord, name='commercial_delete_landlord'),






    ############# urls End for commercial rental listing Module for landlord ####################


########### urls for pg list forms for landlord ###########################

    path('pg_landlord_list',views.pg_landlord_list,name="pg_landlord_list"),

    

    path('pg_landlord',views.pg_landlord,name="pg_landlord"),
    path('add-pg-landlord/', views.add_pg_landlord, name='add_pg_landlord'),
    path('pg-coliving-landlord/export/', views.export_pg_coliving_landlord, name='export_pg_coliving_landlord'),
    path('pg-landlord/edit/<str:pk>/', views.pg_landlord_edit, name='pg_landlord_edit'),
    path('pg-coliving-landlord/view/<str:pk>/', views.pg_coliving_view_landlord, name='pg_coliving_view_landlord'),

    #path('pg-rm/import-excel/',       views.import_pg_excel_rm,       name='import_pg_excel_rm'),
   # path('pg-rm/pg/download-template/',  views.download_pg_template_rm,  name='download_pg_template_rm'),
    path('pg-coliving-landlord/bulk-delete/', views.pg_bulk_delete_landlord, name='pg_bulk_delete_landlord'),
    path(
    'pg-coliving-landlord/delete/<str:pk>/',
    views.pg_coliving_delete_landlord,
    name='pg_coliving_delete_landlord'
    ),
    



########### urls for pg forms for landlord ###########################


################START URL SECTION RESALE INDUSTRIAL PLOT LISTING RM ######################################################




    path('industrial_plot_resale_list_landlord',views.industrial_plot_resale_list_landlord,name="industrial_plot_resale_list_landlord"),
    path('industrial_plot_resale_landlord',views.industrial_plot_resale_landlord,name="industrial_plot_resale_landlord"),
    path('industrial-plot-resale-landlord/add/', views.industrial_plot_resale_add_landlord, name='industrial_plot_resale_add_landlord'),
    path('industrial-plot-landlord/edit/<str:pk>/', views.industrial_plot_resale_edit_landlord, name='industrial_plot_resale_edit_landlord'),
    path('industrial-plot-landlord/view/<str:pk>/', views.industrial_plot_resale_view_landlord, name='industrial_plot_resale_view_landlord'),
    path('industrial-plot-landlord/delete/<str:pk>/', views.industrial_plot_resale_delete_landlord, name='industrial_plot_resale_delete_landlord'),
    path('industrial-plot-landlord/bulk-delete/', views.industrial_plot_resale_bulk_delete_landlord, name='industrial_plot_resale_bulk_delete_landlord'),
    path('industrial-plot-resale-landlord/export/', views.export_industrial_plot_resale_landlord, name='export_industrial_plot_resale_landlord'),



 ################END URL SECTION RESALE INDUSTRIAL PLOT LISTING RM ######################################################

    
 ################Start URL SECTION RESALE Agriculture PLOT LISTING RM ######################################################


    path('agricultural_plot_resale_list_landlord',views.agricultural_plot_resale_list_landlord,name="agricultural_plot_resale_list_landlord"),

    path('agricultural_plot_resale_landlord',views.agricultural_plot_resale_landlord,name="agricultural_plot_resale_landlord"),

    path(
        'agricultural-plot-resale-landlord/add/',
        views.agricultural_plot_resale_add_landlord,
        name='agricultural_plot_resale_add_landlord'
    ),

    path(
        'agricultural-plot-resale-landlord/edit/<str:pk>/',
        views.agricultural_plot_resale_edit_landlord,
        name='agricultural_plot_resale_edit_landlord'
    ),
    path(
        'agricultural-plot-resale-landlord/delete/<str:pk>/',
        views.agricultural_plot_resale_delete_landlord,
        name='agricultural_plot_resale_delete_landlord'
    ),

    # Bulk Delete
    path(
        'agricultural-plot-resale-landlord/bulk-delete/',
        views.agricultural_plot_resale_bulk_delete_landlord,
        name='agricultural_plot_resale_bulk_delete_landlord'
    ),


    path(
        'agricultural-plot-resale-landlord/export/',
        views.export_agricultural_plot_resale_landlord,
        name='export_agricultural_plot_resale_landlord'
    ),

    path(
        'agricultural-plot-resale-landlord/view/<str:pk>/',
        views.agricultural_plot_resale_view_landlord,
        name='agricultural_plot_resale_view_landlord'
    ),


   ################End URL SECTION RESALE Agriculture PLOT LISTING Landlord ######################################################




    ############## urls for resale property list #########################

    path('residential_resale_landlord_list',views.residential_resale_landlord_list,name="residential_resale_landlord_list"),

    ########### urls for resale property form residential ################

    path('residential_resale_landlord',views.residential_resale_landlord,name="residential_resale_landlord"),

    ############ urls for resale property view form residential ##################

    path('residential_resale_landlord_view/<str:id>',views.residential_resale_landlord_view,name="residential_resale_landlord_view"),

    ######## urls for resale property edit form residential ######################

    path('residential_resale_landlord_edit/<str:id>',views.residential_resale_landlord_edit,name="residential_resale_landlord_edit"),

    ######### urls for resale commercial property list #########################

    path('commercial_resale_landlord_list',views.commercial_resale_landlord_list,name="commercial_resale_landlord_list"),

   ######## urls for resale property from commercial ######################

    path('commercial_resale_landlord',views.commercial_resale_landlord,name="commercial_resale_landlord"),

    ######### urls for resale plot property list #######################

    path('plot_resale_landlord_list',views.plot_resale_landlord_list,name="plot_resale_landlord_list"),

    ############ urls for residential plot list from landlord  #########################

    path('plot_resale_res_landlord_list',views.plot_resale_res_landlord_list,name="plot_resale_res_landlord_list"),

    ############ urls for residential plot from landlord  #########################

    path('plot_resale_res_landlord',views.plot_resale_res_landlord,name="plot_resale_res_landlord"),

    ############ urls for commercial plot list from landlord  #########################

    path('plot_resale_comm_landlord_list',views.plot_resale_comm_landlord_list,name="plot_resale_comm_landlord_list"),

    ############ urls for commercial plot from landlord  #########################

    path('plot_resale_comm_landlord',views.plot_resale_comm_landlord,name="plot_resale_comm_landlord"),

    ############ urls for industrial plot list from landlord  #########################

    path('plot_resale_ind_landlord_list',views.plot_resale_ind_landlord_list,name="plot_resale_ind_landlord_list"),

    ############ urls for industrial plot from landlord  #########################

    path('plot_resale_ind_landlord',views.plot_resale_ind_landlord,name="plot_resale_ind_landlord"),

    ############ urls for agricultural plot list from landlord  #########################

    path('plot_resale_agri_landlord_list',views.plot_resale_agri_landlord_list,name="plot_resale_agri_landlord_list"),

    ############ urls for agricultural plot from landlord  #########################

    path('plot_resale_agri_landlord',views.plot_resale_agri_landlord,name="plot_resale_agri_landlord"),

    ############ urls for resale industrial property list ##########################

    path('industry_resale_landlord_list',views.industry_resale_landlord_list,name="industry_resale_landlord_list"),

    ######## urls for industrial resale property form ######################

    path('industry_resale_landlord',views.industry_resale_landlord,name="industry_resale_landlord"),

   ######### urls for agricutural resale property form ######################

    path('agriculture_resale_landlord',views.agriculture_resale_landlord,name="agriculture_resale_landlord"),


]

     






