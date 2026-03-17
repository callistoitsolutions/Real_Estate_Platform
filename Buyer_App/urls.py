from django.contrib import admin
from django.urls import path
from Buyer_App import views

urlpatterns = [
      
    ########### urls for buyer dashbaord #####################

    path('Buyer_Dashboard',views.Buyer_Dashboard,name="Buyer_Dashboard"),
    
]

    










