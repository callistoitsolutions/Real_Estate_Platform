from django.contrib import admin
from django.urls import path
from Tenant_App import views

urlpatterns = [
      
    ########### urls for tenant dashbaord #####################

    path('Tenant_Dashboard',views.Tenant_Dashboard,name="Tenant_Dashboard"),
    
]

    










