from django.contrib import admin
from django.urls import path
from Agency_App import views

urlpatterns = [
      
    ########### urls for agency dashbaord #####################

    path('Agency_Dashboard',views.Agency_Dashboard,name="Agency_Dashboard"),
    
]

    










