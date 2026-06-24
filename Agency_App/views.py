from django.shortcuts import render,HttpResponse,redirect
from Admin_App.models import *
from Landlord_Panel.views import calculate_profile_strength
from django.template.loader import render_to_string
from CRM_Panel.models import *

# Create your views here.


############## Views start for agency dashboard ######################

def Agency_Dashboard(request):
    # 1. Retrieve BOTH possible session IDs from the browser
    user_id = request.session.get('User_id')
    admin_id = request.session.get('Admin_id') 
    logged_in_role = request.session.get('user_type')

    # 2.  VIP Access Control
    is_valid_agency = (user_id and logged_in_role == "Agency/Builder")
    is_valid_admin = (admin_id and logged_in_role == "Admin" and 'impersonate_id' in request.session)

    # If they aren't a valid Agency/Builder, AND they aren't an Admin trying to impersonate... kick them out.
    if not is_valid_agency and not is_valid_admin:
        return redirect('login') 

    # 3.  The ID Swap
    if is_valid_admin:
        # Admin is visiting: pull the target Agency's ID
        dashboard_user_id = request.session.get('impersonate_id')
    else:
        # Normal Agency is visiting: use their normal ID
        dashboard_user_id = user_id

    # 4. Data Fetching: Get the full user object using the final decided ID
    user_obj = User_Details.objects.get(id=dashboard_user_id)

    # Calculate profile strength based on the swapped user object
    completion_score = calculate_profile_strength(user_obj)

    enquiry_obj_agency = PropertyEnquiry.objects.filter(assigned_to__id=user_obj.id).count()
    
    context = {
        'user_obj': user_obj,
        # Pass the object's actual role so the template renders the Agency UI correctly
        'user_role': user_obj.user_role,
        'profile_completion_percentage': completion_score,
        'enquiry_obj_agency':enquiry_obj_agency
    }
    
    return render(request, "agency_panel/agency_dashboard.html", context)

############# Views end for agency dashboard ###########################


############# Views start for update agency profile #####################

def Update_Profile_Agency(request):
    # 1. Retrieve BOTH possible session IDs from the browser
    user_id = request.session.get('User_id')
    admin_id = request.session.get('Admin_id') 
    logged_in_role = request.session.get('user_type')

    # 2.  VIP Access Control
    is_valid_agency = (user_id and logged_in_role == "Agency/Builder")
    is_valid_admin = (admin_id and logged_in_role == "Admin" and 'impersonate_id' in request.session)

    # If they aren't a valid Agency/Builder, AND they aren't an Admin trying to impersonate... kick them out.
    if not is_valid_agency and not is_valid_admin:
        return redirect('login') 

    # 3.  The ID Swap
    if is_valid_admin:
        # Admin is visiting: pull the target Agency's ID
        dashboard_user_id = request.session.get('impersonate_id')
    else:
        # Normal Agency is visiting: use their normal ID
        dashboard_user_id = user_id

    # 4. Data Fetching: Get the full user object using the final decided ID
    user_obj = User_Details.objects.get(id=dashboard_user_id)

    enquiry_obj_agency = PropertyEnquiry.objects.filter(assigned_to__id=user_obj.id).count()
    
    
    context = {
        'user_obj': user_obj,
        'user_role': user_obj.user_role,
        'enquiry_obj_agency':enquiry_obj_agency
    }
    
    return render(request, "agency_panel/Profile/agency_profile.html", context)

############# Views end for update agency profile ###########################


############## Views start for assign enquiries to agency/builder #################

def Assign_Enquiry_Agency(request):
    # 1. Retrieve BOTH possible session IDs from the browser
    user_id = request.session.get('User_id')
    admin_id = request.session.get('Admin_id') 
    logged_in_role = request.session.get('user_type')

    # 2.  VIP Access Control
    is_valid_agency = (user_id and logged_in_role == "Agency/Builder")
    is_valid_admin = (admin_id and logged_in_role == "Admin" and 'impersonate_id' in request.session)

    # If they aren't a valid Agency/Builder, AND they aren't an Admin trying to impersonate... kick them out.
    if not is_valid_agency and not is_valid_admin:
        return redirect('login') 

    # 3.  The ID Swap
    if is_valid_admin:
        # Admin is visiting: pull the target Agency's ID
        dashboard_user_id = request.session.get('impersonate_id')
    else:
        # Normal Agency is visiting: use their normal ID
        dashboard_user_id = user_id

    # 4. Data Fetching: Get the full user object using the final decided ID
    user_obj = User_Details.objects.get(id=dashboard_user_id)

    enquiry_obj_agency = PropertyEnquiry.objects.filter(assigned_to__id=user_obj.id).count()

    # Calculate profile strength based on the swapped user object
    completion_score = calculate_profile_strength(user_obj)

    enquiry_obj = PropertyEnquiry.objects.filter(assigned_to__id=user_obj.id).order_by('-id')
    enquiry_obj_count = PropertyEnquiry.objects.filter(assigned_to__id=user_obj.id).count()

    ############## Enquiries Stats By Source ##############################

    fb_obj_count = PropertyEnquiry.objects.filter(utm_link__utm_source="facebook",assigned_to__id=user_obj.id).count()
    insta_obj_count = PropertyEnquiry.objects.filter(utm_link__utm_source="instagram",assigned_to__id=user_obj.id).count()
    whatsapp_obj_count = PropertyEnquiry.objects.filter(utm_link__utm_source="whatsapp",assigned_to__id=user_obj.id).count()
    google_obj_count = PropertyEnquiry.objects.filter(utm_link__utm_source="google",assigned_to__id=user_obj.id).count()
    linkedin_obj_count = PropertyEnquiry.objects.filter(utm_link__utm_source="linkedin",assigned_to__id=user_obj.id).count()
    twitter_obj_count = PropertyEnquiry.objects.filter(utm_link__utm_source="twitter",assigned_to__id=user_obj.id).count()
    youtube_obj_count = PropertyEnquiry.objects.filter(utm_link__utm_source="youtube",assigned_to__id=user_obj.id).count()
    referral_obj_count = PropertyEnquiry.objects.filter(utm_link__utm_source="referral",assigned_to__id=user_obj.id).count()

    ########### Enquiry Stats by lead source ################################

    pending_obj_count = PropertyEnquiry.objects.filter(lead_status="Pending",assigned_to__id=user_obj.id).count()
    progress_obj_count = PropertyEnquiry.objects.filter(lead_status="In Progress",assigned_to__id=user_obj.id).count()
    hold_obj_count = PropertyEnquiry.objects.filter(lead_status="Hold",assigned_to__id=user_obj.id).count()
    closed_obj_count = PropertyEnquiry.objects.filter(lead_status="Closed",assigned_to__id=user_obj.id).count()
    cancelled_obj_count = PropertyEnquiry.objects.filter(lead_status="Cancelled",assigned_to__id=user_obj.id).count()

    rendered = render_to_string("agency_panel/render_to_string/R_Enquiry/r_t_s_enquiry.html",{'enquiry_obj':enquiry_obj,'enquiry_obj_count':enquiry_obj_count,'fb_obj_count':fb_obj_count,'insta_obj_count':insta_obj_count,'whatsapp_obj_count':whatsapp_obj_count,'google_obj_count':google_obj_count,'linkedin_obj_count':linkedin_obj_count,'twitter_obj_count':twitter_obj_count,'youtube_obj_count':youtube_obj_count,'referral_obj_count':referral_obj_count,'pending_obj_count':pending_obj_count,'progress_obj_count':progress_obj_count,'hold_obj_count':hold_obj_count,'closed_obj_count':closed_obj_count,'cancelled_obj_count':cancelled_obj_count})
    
    
    context = {
        'user_obj': user_obj,
        'user_role': user_obj.user_role,
        'profile_completion_percentage': completion_score,
        'property_enquiry_list':rendered,
        'enquiry_obj_agency':enquiry_obj_agency
    }
    
    return render(request, "agency_panel/Enquiry/assign_enquiry.html", context)

############# Views end for assign enquiries to agency/builder ####################


############ Views start for update property enquiry #########################

def update_enquiry_agency(request,id):
    # 1. Retrieve BOTH possible session IDs from the browser
    user_id = request.session.get('User_id')
    admin_id = request.session.get('Admin_id') 
    logged_in_role = request.session.get('user_type')

    # 2.  VIP Access Control
    is_valid_agency = (user_id and logged_in_role == "Agency/Builder")
    is_valid_admin = (admin_id and logged_in_role == "Admin" and 'impersonate_id' in request.session)

    # If they aren't a valid Agency/Builder, AND they aren't an Admin trying to impersonate... kick them out.
    if not is_valid_agency and not is_valid_admin:
        return redirect('login') 

    # 3.  The ID Swap
    if is_valid_admin:
        # Admin is visiting: pull the target Agency's ID
        dashboard_user_id = request.session.get('impersonate_id')
    else:
        # Normal Agency is visiting: use their normal ID
        dashboard_user_id = user_id

    # 4. Data Fetching: Get the full user object using the final decided ID
    user_obj = User_Details.objects.get(id=dashboard_user_id)

    enquiry = PropertyEnquiry.objects.get(id=id)

    enquiry_obj_agency = PropertyEnquiry.objects.filter(assigned_to__id=user_obj.id).count()
    
    
    context = {
        'user_obj': user_obj,
        'user_role': user_obj.user_role,
        'enquiry_obj_agency':enquiry_obj_agency,
        'enquiry':enquiry
    }
    
    return render(request, "agency_panel/Enquiry/update_enquiry.html", context)

############# Views end for update property enquiry #################################