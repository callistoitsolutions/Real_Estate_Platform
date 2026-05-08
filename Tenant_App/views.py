from django.shortcuts import render,HttpResponse,redirect
from Admin_App.models import *
from Landlord_Panel.views import calculate_profile_strength

# Create your views here.

############# Views start for tenant dashboard ##########################

def tenant_Dashboard(request):
    # 1. Retrieve BOTH possible session IDs from the browser
    user_id = request.session.get('User_id')
    admin_id = request.session.get('Admin_id') 
    logged_in_role = request.session.get('user_type')

    # 2. VIP Access Control
    is_valid_tenant = (user_id and logged_in_role == "Tenant")
    is_valid_admin = (admin_id and logged_in_role == "Admin" and 'impersonate_id' in request.session)

    # If they aren't a valid Tenant, AND they aren't an Admin trying to impersonate... kick them out.
    if not is_valid_tenant and not is_valid_admin:
        return redirect('login') 

    # 3.  The ID Swap
    if is_valid_admin:
        # Admin is visiting: pull the target Tenant's ID
        dashboard_user_id = request.session.get('impersonate_id')
    else:
        # Normal Tenant is visiting: use their normal ID
        dashboard_user_id = user_id

    # 4. Data Fetching: Get the full user object using the final decided ID
    user_obj = User_Details.objects.get(id=dashboard_user_id)

    # Calculate profile strength based on the swapped user object
    completion_score = calculate_profile_strength(user_obj)
    
    context = {
        'user_obj': user_obj,
        # Pass the object's actual role so the template renders the Tenant UI correctly
        'user_role': user_obj.user_role,
        'profile_completion_percentage': completion_score,
    }
    
    return render(request, "tenant_panel/tenant_dashboard.html", context)

############ Views end for tenant dashboard ################################


############ Views start for update tenant profile ##########################

def Update_Profile_Tenant(request):
    # 1. Retrieve BOTH possible session IDs from the browser
    user_id = request.session.get('User_id')
    admin_id = request.session.get('Admin_id') 
    logged_in_role = request.session.get('user_type')

    # 2. VIP Access Control
    is_valid_tenant = (user_id and logged_in_role == "Tenant")
    is_valid_admin = (admin_id and logged_in_role == "Admin" and 'impersonate_id' in request.session)

    # If they aren't a valid Tenant, AND they aren't an Admin trying to impersonate... kick them out.
    if not is_valid_tenant and not is_valid_admin:
        return redirect('login') 

    # 3.  The ID Swap
    if is_valid_admin:
        # Admin is visiting: pull the target Tenant's ID
        dashboard_user_id = request.session.get('impersonate_id')
    else:
        # Normal Tenant is visiting: use their normal ID
        dashboard_user_id = user_id

    # 4. Data Fetching: Get the full user object using the final decided ID
    user_obj = User_Details.objects.get(id=dashboard_user_id)
    
    context = {
        'user_obj': user_obj,
        'user_role': user_obj.user_role
    }
    
    return render(request, "tenant_panel/Profile/tenant_profile.html", context)

########### Views end for update tenant profile ##############################
