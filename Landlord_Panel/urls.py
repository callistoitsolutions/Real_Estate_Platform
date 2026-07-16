from django.contrib import admin
from django.urls import path
from Landlord_Panel import views

urlpatterns = [
      

      ##########urls for Lanlord#####
   
     path('landlord_dashboard',views.landlord_dashboard,name="landlord_dashboard"),
  


     ############# urls for update landlord profile page #####################

     path('Update_Profile_Landlord',views.Update_Profile_Landlord,name='Update_Profile_Landlord'),

     ########### urls for rental forms list for landlord #######################

    path('residential_landlord_list',views.residential_landlord_list,name="residential_landlord_list"),

    ######## urls for rental forms for landlord ########################

    path('residential_landlord',views.residential_landlord,name="residential_landlord"),

    ############ urls for edit rental forms for landlord #################

    path('residential_landlord_edit/<str:pk>',views.residential_landlord_edit,name="residential_landlord_edit"),

    ############## urls for view rental forms for landlord ###################

    path('residential_landlord_view/<str:pk>',views.residential_landlord_view,name="residential_landlord_view"),

    ########## urls for commercial rent forms for landlord ################

    path('commercial_landlord_list',views.commercial_landlord_list,name="commercial_landlord_list"),

    ############# urls for commercial forms for landlord ####################

    path('commercial_landlord',views.commercial_landlord,name="commercial_landlord"),

    ########### urls for pg list forms for landlord ###########################

    path('pg_landlord_list',views.pg_landlord_list,name="pg_landlord_list"),

    ########### urls for pg forms for landlord ###########################

    path('pg_landlord',views.pg_landlord,name="pg_landlord"),

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

     






