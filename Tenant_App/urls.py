from django.contrib import admin
from django.urls import path
from Tenant_App import views

app_name = 'Tenant_App'

urlpatterns = [
      
    ########### urls for tenant dashbaord #####################

    path('tenant_Dashboard',views.tenant_Dashboard,name="tenant_Dashboard"),

    ########### urls for update tenant profile ##########################

    path('Update_Profile_Tenant',views.Update_Profile_Tenant,name='Update_Profile_Tenant'),

    ############## urls for tenant subscriptions ###############################

    path('Subscriptions_Tenant',views.Subscriptions_Tenant,name='Subscriptions_Tenant'),

    ########## urls for buy plan for tenant #######################

    path('Buy_Plan_Tenant/<int:id>', views.Buy_Plan_Tenant, name='Buy_Plan_Tenant'),
    
]

    










