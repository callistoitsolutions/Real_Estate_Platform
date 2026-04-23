from django.contrib import admin
from django.urls import path
from Agency_App import views

urlpatterns = [
      
    ########### urls for agency dashbaord #####################

    path('Agency_Dashboard',views.Agency_Dashboard,name="Agency_Dashboard"),

    ########### urls for update agency profile ###################

    path('Update_Profile_Agency',views.Update_Profile_Agency,name='Update_Profile_Agency'),
    
]

    










