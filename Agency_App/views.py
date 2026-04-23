from django.shortcuts import render,HttpResponse,redirect
from Admin_App.models import *

# Create your views here.


############## Views start for agency dashboard ######################

def Agency_Dashboard(request):
    # 1. Retrieve identity from browser session
    user_id = request.session.get('User_id')
    user_role = request.session.get('user_type')

    # 2. Access Control: If ID is missing OR role is wrong, redirect to login
    if not user_id or user_role != "Agency/Builder":
        return redirect('login') 

    # 3. Data Fetching: Get the full user object for the template
    user_obj = User_Details.objects.get(id=user_id)
    
    context = {
        'user_obj': user_obj,
        'user_role': user_role
    }
    
    return render(request, "agency_panel/agency_dashboard.html", context)

############# Views end for agency dashboard ###########################


############# Views start for update agency profile #####################

def Update_Profile_Agency(request):
    # 1. Retrieve identity from browser session
    user_id = request.session.get('User_id')
    user_role = request.session.get('user_type')

    # 2. Access Control: If ID is missing OR role is wrong, redirect to login
    if not user_id or user_role != "Agency/Builder":
        return redirect('login') 

    # 3. Data Fetching: Get the full user object for the template
    user_obj = User_Details.objects.get(id=user_id)
    
    context = {
        'user_obj': user_obj,
        'user_role': user_role
    }
    
    return render(request, "agency_panel/Profile/agency_profile.html", context)

############# Views end for update agency profile ###########################