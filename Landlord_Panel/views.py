from django.shortcuts import render,HttpResponse

# Create your views here.
from django.shortcuts import render
from django.contrib.auth.decorators import login_required



# Create your views here.
from django.shortcuts import render
from django.contrib import messages
from django.shortcuts import render,redirect
from Landlord_Panel .models import *
from Main_App .models import *
from Admin_App.models import *

# Create your views here.


############## Views start for calculate profile strength ##########################

def calculate_profile_strength(user_obj):
    """Calculates the profile completion percentage dynamically based on the user's role."""
    strength = 0
    
    # ---------------------------------------------------------
    # 1. BASE DETAILS (Applies to everyone - Total 50%)
    # ---------------------------------------------------------
    if user_obj.user_name: strength += 10
    if user_obj.user_email: strength += 10
    if user_obj.user_phone: strength += 10
    if user_obj.user_password: strength += 10
    if user_obj.user_role: strength += 10
    
    # ---------------------------------------------------------
    # 2. ROLE-SPECIFIC DETAILS (Remaining 50%)
    # ---------------------------------------------------------
    role = user_obj.user_role

    if role == 'Vendor':
        # Vendor requires 5 specific things (10% each)
        if getattr(user_obj, 'user_state', None): strength += 10
        if getattr(user_obj, 'user_city', None): strength += 10
        if getattr(user_obj, 'user_address', None): strength += 10
        if getattr(user_obj, 'user_profile', None) and user_obj.user_profile.name: strength += 10
        if getattr(user_obj, 'user_service_type', None): strength += 10 # <-- Change to your actual DB field
        if getattr(user_obj, 'user_company_name', None): strength += 10 # <-- Change to your actual DB field
        if getattr(user_obj, 'user_profile', None) and user_obj.user_profile.name: strength += 10
        
    elif role in ['Agent', 'Agency/Builder']:
        # Agents/Agencies require different fields (10% each)
        if getattr(user_obj, 'user_state', None): strength += 10
        if getattr(user_obj, 'user_city', None): strength += 10
        if getattr(user_obj, 'user_address', None): strength += 10
        if getattr(user_obj, 'user_license_number', None): strength += 10 # <-- Change to your actual DB field
        if getattr(user_obj, 'user_profile', None) and user_obj.user_profile.name: strength += 10
        
    else:
        # Default for Landlord, Tenant, and Buyer
        if getattr(user_obj, 'user_state', None): strength += 15
        if getattr(user_obj, 'user_city', None): strength += 15
        if getattr(user_obj, 'user_address', None): strength += 10
        if getattr(user_obj, 'user_profile', None) and user_obj.user_profile.name: strength += 10

    # Ensure it never accidentally goes over 100
    return min(strength, 100)

############# Views end for calculate profile strength ##########################






def landlord_dashboard(request):
    # 1. Retrieve BOTH possible session IDs from the browser
    user_id = request.session.get('User_id')
    admin_id = request.session.get('Admin_id') 
    logged_in_role = request.session.get('user_type')

    # 2. VIP Access Control
    is_valid_landlord = (user_id and logged_in_role == "Landlord")
    is_valid_admin = (admin_id and logged_in_role == "Admin" and 'impersonate_id' in request.session)

    # If they aren't a valid Landlord, AND they aren't an Admin trying to impersonate... kick them out.
    if not is_valid_landlord and not is_valid_admin:
        return redirect('login') 

    # 3. The ID Swap
    if is_valid_admin:
        # Admin is visiting: pull the target Landlord's ID
        dashboard_user_id = request.session.get('impersonate_id')
    else:
        # Normal Landlord is visiting: use their normal ID
        dashboard_user_id = user_id

    # 4. Data Fetching: Get the full user object using the final decided ID
    user_obj = User_Details.objects.get(id=dashboard_user_id)

    # (Your original logic stays untouched here!)
    completion_score = calculate_profile_strength(user_obj)
    
    context = {
        'user_obj': user_obj,
        # Pass the object's role so the template behaves normally for the Landlord UI
        'user_role': user_obj.user_role, 
        'profile_completion_percentage': completion_score,
    }
    
    return render(request, "landlord/landlord_dashboard.html", context)













############## Views start for update landlord profile page ######################

def Update_Profile_Landlord(request):
    # 1. Retrieve BOTH possible session IDs from the browser
    user_id = request.session.get('User_id')
    admin_id = request.session.get('Admin_id') 
    logged_in_role = request.session.get('user_type')

    # 2. VIP Access Control
    is_valid_landlord = (user_id and logged_in_role == "Landlord")
    is_valid_admin = (admin_id and logged_in_role == "Admin" and 'impersonate_id' in request.session)

    # If they aren't a valid Landlord, AND they aren't an Admin trying to impersonate... kick them out.
    if not is_valid_landlord and not is_valid_admin:
        return redirect('login') 

    # 3. The ID Swap
    if is_valid_admin:
        # Admin is visiting: pull the target Landlord's ID
        dashboard_user_id = request.session.get('impersonate_id')
    else:
        # Normal Landlord is visiting: use their normal ID
        dashboard_user_id = user_id

    # 4. Data Fetching: Get the full user object using the final decided ID
    user_obj = User_Details.objects.get(id=dashboard_user_id)
    
    context = {
        'user_obj': user_obj,
        'user_role': user_obj.user_role
    }
    
    return render(request, "landlord/Profile/landlord_profile.html", context) 

########### Views end for update landlord profile page ##########################


