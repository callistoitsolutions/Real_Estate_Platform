from django.contrib import admin
from django.urls import path
from Buyer_App import views

urlpatterns = [
      
    ########### urls for buyer dashbaord #####################

    path('Buyer_Dashboard',views.Buyer_Dashboard,name="Buyer_Dashboard"),

    ######### urls for update buyer profile #######################

    path('Update_Profile_Buyer',views.Update_Profile_Buyer,name='Update_Profile_Buyer'),

    ############## urls for buyer subscriptions ###############################

    path('Subscriptions_Buyer',views.Subscriptions_Buyer,name='Subscriptions_Buyer'),

    ########## urls for buy plan for buyer #######################

    path('Buy_Plan_Buyer/<int:id>', views.Buy_Plan_Buyer, name='Buy_Plan_Buyer'),
    
]

    










