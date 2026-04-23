from django.contrib import admin
from django.urls import path
from Tenant_App import views

app_name = 'Tenant_App'

urlpatterns = [
      
    ########### urls for tenant dashbaord #####################

    path('tenant_Dashboard',views.tenant_Dashboard,name="tenant_Dashboard"),

    ########### urls for update tenant profile ##########################

    path('Update_Profile_Tenant',views.Update_Profile_Tenant,name='Update_Profile_Tenant'),
    
]

    










