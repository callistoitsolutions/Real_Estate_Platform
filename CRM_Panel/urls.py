from django.contrib import admin
from django.urls import path
from CRM_Panel import views

urlpatterns = [
      

      ##########urls for Lanlord#####
   
 
     path('crm_dashboard',views.crm_dashboard,name="crm_dashboard"),
    
     
    
     
 

 
   
     
 


     
]










    
    # Repeat pattern for all other forms, e.g.
    # path('manual-lead/new/', views.manual_lead_create, name='manual_lead_create'),
    # path('manual-lead/', views.manual_lead_list, name='manual_lead_list'), ...

   
     
    








