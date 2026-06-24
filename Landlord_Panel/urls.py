from django.contrib import admin
from django.urls import path
from Landlord_Panel import views

urlpatterns = [
      

      ##########urls for Lanlord#####
   
     path('landlord_dashboard',views.landlord_dashboard,name="landlord_dashboard"),
  


     ############# urls for update landlord profile page #####################

     path('Update_Profile_Landlord',views.Update_Profile_Landlord,name='Update_Profile_Landlord'),


      ############# urls for update landlord profile page #####################

   
     
  


    



]

     






