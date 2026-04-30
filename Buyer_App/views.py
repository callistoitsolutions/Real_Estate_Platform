from django.shortcuts import render,HttpResponse,redirect
from Admin_App.models import *
from Landlord_Panel.views import calculate_profile_strength

# Create your views here.

############# Views start for tenant dashboard ##########################

def Buyer_Dashboard(request):
    # 1. Retrieve identity from browser session
    user_id = request.session.get('User_id')
    user_role = request.session.get('user_type')

    # 2. Access Control: If ID is missing OR role is wrong, redirect to login
    if not user_id or user_role != "Buyer":
        return redirect('login') 

    # 3. Data Fetching: Get the full user object for the template
    user_obj = User_Details.objects.get(id=user_id)

    completion_score = calculate_profile_strength(user_obj)
    
    context = {
        'user_obj': user_obj,
        'user_role': user_role,
        'profile_completion_percentage': completion_score,
    }
    
    return render(request, "buyer_panel/buyer_dashboard.html", context)

############ Views end for tenant dashboard ################################


############## Views start for update buyer profile #########################

def Update_Profile_Buyer(request):
    # 1. Retrieve identity from browser session
    user_id = request.session.get('User_id')
    user_role = request.session.get('user_type')

    # 2. Access Control: If ID is missing OR role is wrong, redirect to login
    if not user_id or user_role != "Buyer":
        return redirect('login') 

    # 3. Data Fetching: Get the full user object for the template
    user_obj = User_Details.objects.get(id=user_id)
    
    context = {
        'user_obj': user_obj,
        'user_role': user_role,
    }
    
    return render(request, "buyer_panel/Profile/buyer_profile.html", context)

############ Views end for update buyer profile #############################
