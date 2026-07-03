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


     ############ urls for Rental Residential Listing ############################

    path('residential_agency',views.residential_agency,name="residential_agency"),
    path('rental_list_agency',views.rental_list_agency,name="rental_list_agency"),


     ############ urls for Rental Residential Listing ############################

    path('commercial_agency',views.commercial_agency,name="commercial_agency"),
    path('commercial_list_agency',views.commercial_list_agency,name="commercial_list_agency"),


     ############ urls for Rental Residential Listing ############################

    path('pg_coliving_agency',views.pg_coliving_agency,name="pg_coliving_agency"),
    path('pg_list_agency',views.pg_list_agency,name="pg_list_agency"),


       ############ urls for Resale Residential Listing ############################


    path('residential_resale_agency',views.residential_resale_agency,name="residential_resale_agency"),
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


 ############ urls for Resale Industrial Plot Listing ############################

   path('industrial_plot_resale_agency',views.industrial_plot_resale_agency,name="industrial_plot_resale_agency"),
   path('industrial_plot_resale_list_agency',views.industrial_plot_resale_list_agency,name="industrial_plot_resale_list_agency"),


 ############ urls for Resale Agricultural Plot Listing ############################
    
   path('agricultural_plot_resale_agency',views.agricultural_plot_resale_agency,name="agricultural_plot_resale_agency"),
   path('agricultural_plot_resale_list_agency',views.agricultural_plot_resale_list_agency,name="agricultural_plot_resale_list_agency"),
    
]

    










