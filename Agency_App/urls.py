from django.contrib import admin
from django.urls import path
from Agency_App import views

urlpatterns = [
      
    ########### urls for agency dashbaord #####################

    path('Agency_Dashboard',views.Agency_Dashboard,name="Agency_Dashboard"),

    ########### urls for update agency profile ###################

    path('Update_Profile_Agency',views.Update_Profile_Agency,name='Update_Profile_Agency'),

    ############## urls for assign enquiries to agency/Builder #########################

    path('Assign_Enquiry_Agency',views.Assign_Enquiry_Agency,name='Assign_Enquiry_Agency'),

    ############ urls for update property enquiry ############################

    path('update_enquiry_agency/<int:id>',views.update_enquiry_agency,name="update_enquiry_agency"),


########################################## urls Start for Rental Residential Listing Module ############################

    path('residential_agency',views.residential_agency,name="residential_agency"),

    path('residential_add_agency',views.residential_add_agency,name="residential_add_agency"),
    path('residential_agency_edit/<str:pk>',views.residential_agency_edit,name="residential_agency_edit"),
    path('residential_agency_view/<str:pk>',views.residential_agency_view,name="residential_agency_view"),
    path('rental_list_agency',views.rental_list_agency,name="rental_list_agency"),
    path('rental-residential-agency/delete/<str:pk>/',
    views.rental_residential_delete_agency,
    name='rental_residential_delete_agency'
    ),

    path('rental-residential-agency/bulk-delete/', views.rental_bulk_delete_agency, name='rental_bulk_delete_agency'),




############ urls END for Rental Residential Listing Module #####################################################

################## ############ urls Start for Rental Residential Agency Listing Excel Upload & Dowload URLS  ############################

    path('download-residential-template-agency/',views.download_residential_template_agency, name='download_residential_template_agency'),
    path('import-residential-excel-agency/', views.import_residential_excel_agency, name='import_residential_excel_agency'),

############################ urls End for Rental Residential Agency Listing Excel Upload & Dowload URLS  ############################


################################ urls Start for Rental Commercial Agency Listing Module ############################

    path('commercial_agency',views.commercial_agency,name="commercial_agency"),
    path('commercial_list_agency',views.commercial_list_agency,name="commercial_list_agency"),
    path('commercial_rental_add_agency', views.commercial_rental_add_agency, name='commercial_rental_add_agency'),

        
    
    path('commercial_agency_edit/<str:pk>', views.commercial_agency_edit, name="commercial_agency_edit"),
    path('commercial/view_agency/<str:pk>/',  views.commercial_view_agency,   name='commercial_view_agency'),
    path('commercial_agency/export/', views.export_commercial_rent_agency, name='export_commercial_rent_agency'),
    #path('commercial-rm/import-excel/', views.import_commercial_rental_excel_rm, name='import_commercial_rental_excel_rm'),
   # path('commercial-rm/commercial/download-template/', views.download_commercial_rental12_template_rm, name='download_commercial_rental12_template_rm'),
    path('commercial-agency/bulk-delete/', views.commercial_bulk_delete_agency, name='commercial_bulk_delete_agency'),
    path('commercial-agency/delete/<str:pk>/', views.commercial_delete_agency, name='commercial_delete_agency'),



#################################### urls END for Rental Commercial Agency Listing Module ############################


############################################ urls for Rental Residential Listing ############################

    path('pg_coliving_agency',views.pg_coliving_agency,name="pg_coliving_agency"),
    path('pg_list_agency',views.pg_list_agency,name="pg_list_agency"),

    path('add-pg-agency/', views.add_pg_agency, name='add_pg_agency'),
    path('pg-coliving-agency/export/', views.export_pg_coliving_agency, name='export_pg_coliving_agency'),
    path('pg-agency/edit/<str:pk>/', views.pg_agency_edit, name='pg_agency_edit'),
    path('pg-coliving-agency/view/<str:pk>/', views.pg_coliving_view_agency, name='pg_coliving_view_agency'),

    #path('pg-rm/import-excel/',       views.import_pg_excel_rm,       name='import_pg_excel_rm'),
   # path('pg-rm/pg/download-template/',  views.download_pg_template_rm,  name='download_pg_template_rm'),
    path('pg-coliving-agency/bulk-delete/', views.pg_bulk_delete_agency, name='pg_bulk_delete_agency'),
    path(
    'pg-coliving-agency/delete/<str:pk>/',
    views.pg_coliving_delete_agency,
    name='pg_coliving_delete_agency'
    ),
    

################################ urls for Resale Residential Listing ############################


    path('residential_resale_agency',views.residential_resale_agency,name="residential_resale_agency"),

    ############ urls for view resale residential form ########################


    

    path('residential_resale_agency_view/<str:id>',views.residential_resale_agency_view,name="residential_resale_agency_view"),

    path('residential_resale_list_agency',views.residential_resale_list_agency,name="residential_resale_list_agency"),


    ############ urls for Resale Commercial Listing ############################


    path('commercial_resale_agency',views.commercial_resale_agency,name="commercial_resale_agency"),
    path('commercial_resale_list_agency',views.commercial_resale_list_agency,name="commercial_resale_list_agency"),

     





        ############ urls for Resale Industrial Listing ############################


    path('industrial_resale_agency',views.industrial_resale_agency,name="industrial_resale_agency"),
    path('industrial_list_agency',views.industrial_list_agency,name="industrial_list_agency"),

       ############ urls for Resale Agricultural Listing ############################


    path('agricultural_resale_agency',views.agricultural_resale_agency,name="agricultural_resale_agency"),
    path('agricultural_list_agency',views.agricultural_list_agency,name="agricultural_list_agency"),


     ############ urls for Resale Residential Plot Listing ############################


    path('residential_plot_resale_agency',views.residential_plot_resale_agency,name="residential_plot_resale_agency"),
    path('residential_plot_resale_list_agency',views.residential_plot_resale_list_agency,name="residential_plot_resale_list_agency"),



 ############ urls for Resale Commercial Plot Listing ############################

    path('commercial_plot_resale_agency',views.commercial_plot_resale_agency,name="commercial_plot_resale_agency"),

    path('commercial_plot_resale_list_agency',views.commercial_plot_resale_list_agency,name="commercial_plot_resale_list_agency"),


################START URL SECTION RESALE INDUSTRIAL PLOT LISTING  Agency ######################################################




    path('industrial_plot_resale_agency',views.industrial_plot_resale_agency,name="industrial_plot_resale_agency"),
    path('industrial_plot_resale_list_agency',views.industrial_plot_resale_list_agency,name="industrial_plot_resale_list_agency"),
    path('industrial-plot-resale-agency/add/', views.industrial_plot_resale_add_agency, name='industrial_plot_resale_add_agency'),
    path('industrial-plot-agency/edit/<str:pk>/', views.industrial_plot_resale_edit_agency, name='industrial_plot_resale_edit_agency'),
    path('industrial-plot-agency/view/<str:pk>/', views.industrial_plot_resale_view_agency, name='industrial_plot_resale_view_agency'),
    path('industrial-plot-agency/delete/<str:pk>/', views.industrial_plot_resale_delete_agency, name='industrial_plot_resale_delete_agency'),
    path('industrial-plot-agency/bulk-delete/', views.industrial_plot_resale_bulk_delete_agency, name='industrial_plot_resale_bulk_delete_agency'),
    path('industrial-plot-resale-agency/export/', views.export_industrial_plot_resale_agency, name='export_industrial_plot_resale_agency'),



 ################END URL SECTION RESALE INDUSTRIAL PLOT LISTING Agency ######################################################

    
 ################Start URL SECTION RESALE Agriculture PLOT LISTING Agency ######################################################


    path('agricultural_plot_resale_agency',views.agricultural_plot_resale_agency,name="agricultural_plot_resale_agency"),
    path('agricultural_plot_resale_list_agency',views.agricultural_plot_resale_list_agency,name="agricultural_plot_resale_list_agency"),


    path(
        'agricultural-plot-resale-agency/add/',
        views.agricultural_plot_resale_add_agency,
        name='agricultural_plot_resale_add_agency'
    ),

    path(
        'agricultural-plot-resale-agency/edit/<str:pk>/',
        views.agricultural_plot_resale_edit_agency,
        name='agricultural_plot_resale_edit_agency'
    ),
    path(
        'agricultural-plot-resale-agency/delete/<str:pk>/',
        views.agricultural_plot_resale_delete_agency,
        name='agricultural_plot_resale_delete_agency'
    ),

    # Bulk Delete
    path(
        'agricultural-plot-resale-agency/bulk-delete/',
        views.agricultural_plot_resale_bulk_delete_agency,
        name='agricultural_plot_resale_bulk_delete_agency'
    ),


    path(
        'agricultural-plot-resale-agency/export/',
        views.export_agricultural_plot_resale_agency,
        name='export_agricultural_plot_resale_agency'
    ),

    path(
        'agricultural-plot-resale-agency/view/<str:pk>/',
        views.agricultural_plot_resale_view_agency,
        name='agricultural_plot_resale_view_agency'
    ),


   ################End URL SECTION RESALE Agriculture PLOT LISTING Agency ######################################################


    
]

    










