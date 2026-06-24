from django.shortcuts import render,HttpResponse
from django.contrib import messages
from django.shortcuts import render,redirect,get_object_or_404
from Agent_Dashboard .models import *
from django.contrib.auth.decorators import login_required
from Admin_App.models import *
from Landlord_Panel.views import calculate_profile_strength
from CRM_Panel.models import *
from django.template.loader import render_to_string


# Create your views here.

########### Crime Officer Views#######


def Wallet_Recharge_agent(request):
    return render(request,"agent/Wallet_Recharge_agent.html") 


def agent_dashboard(request):
    # 1. Retrieve BOTH possible session IDs from the browser
    user_id = request.session.get('User_id')
    admin_id = request.session.get('Admin_id') 
    logged_in_role = request.session.get('user_type')

    # 2.  VIP Access Control
    is_valid_agent = (user_id and logged_in_role == "Agent")
    is_valid_admin = (admin_id and logged_in_role == "Admin" and 'impersonate_id' in request.session)

    # If they aren't a valid Agent, AND they aren't an Admin trying to impersonate... kick them out.
    if not is_valid_agent and not is_valid_admin:
        return redirect('login') 

    # 3.  The ID Swap
    if is_valid_admin:
        # Admin is visiting: pull the target Agent's ID
        dashboard_user_id = request.session.get('impersonate_id')
    else:
        # Normal Agent is visiting: use their normal ID
        dashboard_user_id = user_id

    # 4. Data Fetching: Get the full user object using the final decided ID
    user_obj = User_Details.objects.get(id=dashboard_user_id)

    # Calculate profile strength based on the swapped user object
    completion_score = calculate_profile_strength(user_obj)

    enquiry_obj_agent = PropertyEnquiry.objects.filter(assigned_to__id=user_obj.id).count()
    
    context = {
        'user_obj': user_obj,
        # Pass the object's actual role so the template renders the Agent UI correctly
        'user_role': user_obj.user_role,
        'profile_completion_percentage': completion_score,
        'enquiry_obj_agent':enquiry_obj_agent
    }
    
    return render(request, "agent/agent_dashboard.html", context) 


############## Views start for update agent profile #########################

def Update_Profile_Agent(request):
    # 1. Retrieve BOTH possible session IDs from the browser
    user_id = request.session.get('User_id')
    admin_id = request.session.get('Admin_id') 
    logged_in_role = request.session.get('user_type')

    # 2.  VIP Access Control
    is_valid_agent = (user_id and logged_in_role == "Agent")
    is_valid_admin = (admin_id and logged_in_role == "Admin" and 'impersonate_id' in request.session)

    # If they aren't a valid Agent, AND they aren't an Admin trying to impersonate... kick them out.
    if not is_valid_agent and not is_valid_admin:
        return redirect('login') 

    # 3.  The ID Swap
    if is_valid_admin:
        # Admin is visiting: pull the target Agent's ID
        dashboard_user_id = request.session.get('impersonate_id')
    else:
        # Normal Agent is visiting: use their normal ID
        dashboard_user_id = user_id

    # 4. Data Fetching: Get the full user object using the final decided ID
    user_obj = User_Details.objects.get(id=dashboard_user_id)

    enquiry_obj_agent = PropertyEnquiry.objects.filter(assigned_to__id=user_obj.id).count()
    
    context = {
        'user_obj': user_obj,
        'user_role': user_obj.user_role,
        'enquiry_obj_agent':enquiry_obj_agent
    }
    
    return render(request, "agent/Profile/agent_profile.html", context)

############# Views end for update agent profile ##############################


############ Views start for assign enquiries to agent ########################

def Assign_Enquiry_Agent(request):
    # 1. Retrieve BOTH possible session IDs from the browser
    user_id = request.session.get('User_id')
    admin_id = request.session.get('Admin_id') 
    logged_in_role = request.session.get('user_type')

    # 2.  VIP Access Control
    is_valid_agent = (user_id and logged_in_role == "Agent")
    is_valid_admin = (admin_id and logged_in_role == "Admin" and 'impersonate_id' in request.session)

    # If they aren't a valid Agent, AND they aren't an Admin trying to impersonate... kick them out.
    if not is_valid_agent and not is_valid_admin:
        return redirect('login') 

    # 3.  The ID Swap
    if is_valid_admin:
        # Admin is visiting: pull the target Agent's ID
        dashboard_user_id = request.session.get('impersonate_id')
    else:
        # Normal Agent is visiting: use their normal ID
        dashboard_user_id = user_id

    # 4. Data Fetching: Get the full user object using the final decided ID
    user_obj = User_Details.objects.get(id=dashboard_user_id)

    #Calculate profile strength based on the swapped user object

    completion_score = calculate_profile_strength(user_obj)

    enquiry_obj_agent = PropertyEnquiry.objects.filter(assigned_to__id=user_obj.id).count()


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

    rendered = render_to_string("agent/render_to_string/R_Enquiry/r_t_s_enquiry.html",{'enquiry_obj':enquiry_obj,'enquiry_obj_count':enquiry_obj_count,'fb_obj_count':fb_obj_count,'insta_obj_count':insta_obj_count,'whatsapp_obj_count':whatsapp_obj_count,'google_obj_count':google_obj_count,'linkedin_obj_count':linkedin_obj_count,'twitter_obj_count':twitter_obj_count,'youtube_obj_count':youtube_obj_count,'referral_obj_count':referral_obj_count,'pending_obj_count':pending_obj_count,'progress_obj_count':progress_obj_count,'hold_obj_count':hold_obj_count,'closed_obj_count':closed_obj_count,'cancelled_obj_count':cancelled_obj_count})
    
    context = {
        'user_obj': user_obj,
        'user_role': user_obj.user_role,
        'property_enquiry_list':rendered,
        'enquiry_obj_agent':enquiry_obj_agent,
        'profile_completion_percentage': completion_score
    }
    
    return render(request, "agent/Enquiry/assign_enquiry.html", context)

############## Views end for assign enquiries to agent #########################


########### Views start for update property enquiry ##########################

def update_enquiry_agent(request,id):
    # 1. Retrieve BOTH possible session IDs from the browser
    user_id = request.session.get('User_id')
    admin_id = request.session.get('Admin_id') 
    logged_in_role = request.session.get('user_type')

    # 2.  VIP Access Control
    is_valid_agent = (user_id and logged_in_role == "Agent")
    is_valid_admin = (admin_id and logged_in_role == "Admin" and 'impersonate_id' in request.session)

    # If they aren't a valid Agent, AND they aren't an Admin trying to impersonate... kick them out.
    if not is_valid_agent and not is_valid_admin:
        return redirect('login') 

    # 3.  The ID Swap
    if is_valid_admin:
        # Admin is visiting: pull the target Agent's ID
        dashboard_user_id = request.session.get('impersonate_id')
    else:
        # Normal Agent is visiting: use their normal ID
        dashboard_user_id = user_id

    # 4. Data Fetching: Get the full user object using the final decided ID
    user_obj = User_Details.objects.get(id=dashboard_user_id)

    enquiry = PropertyEnquiry.objects.get(id=id)

    enquiry_obj_agent = PropertyEnquiry.objects.filter(assigned_to__id=user_obj.id).count()
    
    context = {
        'user_obj': user_obj,
        'user_role': user_obj.user_role,
        'enquiry_obj_agent':enquiry_obj_agent,
        'enquiry':enquiry
    }
    
    return render(request, "agent/Enquiry/update_enquiry.html", context)

############ Views end for update property enquiry #########################



def chat_agent(request):
    return render(request,"agent/chat_agent.html")



def Sponserproperty(request):
    return render(request,"agent/Sponserproperty.html")




def lead_purchase_create(request):
    if request.method == "POST":
        lead_id = request.POST.get("lead_id")
        wallet_deduction = request.POST.get("wallet_deduction")

        if not lead_id or not wallet_deduction:
            messages.error(request, "All fields are required.")
            return redirect("lead_purchase_create")

        LeadPurchase.objects.create(
            lead_id=lead_id,
            wallet_deduction=wallet_deduction,
        )
        messages.success(request, f"Lead {lead_id} purchased successfully!")
       # return redirect("lead_purchase_list")

    return render(request, "agent/lead_purchase.html")


def lead_purchase_list(request):
    purchases = LeadPurchase.objects.all().order_by("-created_at")
    return render(request, "lead_purchase_list.html", {"purchases": purchases})





def wallet_recharge_create(request):
    if request.method == "POST":
        amount = request.POST.get("amount")
        payment_method = request.POST.get("payment_method")

        if not amount or not payment_method:
            messages.error(request, "All fields are required.")
            return redirect("wallet_recharge_create")

        WalletRecharge.objects.create(
            amount=amount,
            payment_method=payment_method,
        )
        messages.success(request, f"Wallet recharged with {amount} using {payment_method}!")
       # return redirect("wallet_recharge_list")

    return render(request, "agent/Wallet_Recharge_agent.html")


def wallet_recharge_list(request):
    recharges = WalletRecharge.objects.all().order_by("-created_at")
    return render(request, "agent/wallet_recharge_list.html", {"recharges": recharges})





def commission_report(request):
    lead_id = request.GET.get("lead_id")
    from_date = request.GET.get("from_date")
    to_date = request.GET.get("to_date")

    commissions = Commission.objects.all().order_by("-created_at")

    # Apply filters if provided
    if lead_id:
        commissions = commissions.filter(lead_id__icontains=lead_id)

    if from_date and to_date:
        commissions = commissions.filter(created_at__date__range=[from_date, to_date])
    elif from_date:  # only from date
        commissions = commissions.filter(created_at__date__gte=from_date)
    elif to_date:  # only to date
        commissions = commissions.filter(created_at__date__lte=to_date)

    context = {
        "commissions": commissions,
        "lead_id": lead_id or "",
        "from_date": from_date or "",
        "to_date": to_date or "",
    }
    return render(request, "agent/Commission_Report_Filter.html", context)




def subscription_overview(request):
    plans = SubscriptionPlan.objects.all().order_by('role', 'order')
    features = FeatureComparison.objects.all().order_by('order')
    # group plans by role as dict: {'Landlord': [...], ...}
    roles = {}
    for p in plans:
        roles.setdefault(p.role, []).append(p)
    return render(request, 'agent/overview.html', {
        'roles': roles,
        'features': features,
    })

def signup_submit(request):
    if request.method == 'POST':
        role = request.POST.get('role')
        plan_name = request.POST.get('selectedPlan')
        plan = SubscriptionPlan.objects.filter(name=plan_name, role=role).first()
        full_name = request.POST.get('owner_name') or request.POST.get('tenant_name') or request.POST.get('agency')
        # Collect other optional fields safely
        property_type = request.POST.get('property_type', '')
        amenities = request.POST.get('amenities', '')
        agency_name = request.POST.get('agency', '') if role == 'Agent' else ''
        service_areas = request.POST.get('service_areas', '') if role == 'Agent' else ''
        preferred_locations = request.POST.get('preferred_locations', '') if role == 'Tenant' else ''
        move_in_date = request.POST.get('move_in_date', None)
        if move_in_date == '':
            move_in_date = None

        signup = UserSignup.objects.create(
            role=role,
            selected_plan=plan,
            full_name=full_name,
            property_type=property_type,
            amenities=amenities,
            agency_name=agency_name,
            service_areas=service_areas,
            preferred_locations=preferred_locations,
            move_in_date=move_in_date
        )
        return redirect('agent:signup_success', pk=signup.pk)
    return redirect('agent:overview')

def signup_success(request, pk):
    signup = get_object_or_404(UserSignup, pk=pk)
    return render(request, 'agent/signup_success.html', {'signup': signup})

from Main_App .models import *


from django.http import HttpResponseForbidden

@login_required
def inquiry_list(request):
    user = request.user
    role = getattr(user, "role", "").lower()

    # Only agents can access this page
    if role != "agent":
        return HttpResponseForbidden("You do not have permission to view this page.")

    # Get all properties posted by the current user (agent manages these)
    residential_props = ResidentialProperty.objects.filter(posted_by=user)
    commercial_props = CommercialProperty.objects.filter(posted_by=user)
    pg_props = PGProperty.objects.filter(posted_by=user)

    # Get inquiries for those properties
    residential_inquiries = ResidentialInquiry.objects.filter(residential_property__in=residential_props)
    commercial_inquiries = CommercialInquiry.objects.filter(commercial_property__in=commercial_props)
    pg_inquiries = PGInquiry.objects.filter(pg_property__in=pg_props)

    # Helper to prepare inquiry data
    def prepare_inquiry_data(inquiries, fk_field):
        data = []
        for inquiry in inquiries:
            prop = getattr(inquiry, fk_field)
            owner = prop.posted_by
            data.append({
                "inquiry_name": inquiry.name,
                "inquiry_email": inquiry.email,
                "inquiry_phone": inquiry.phone,
                "inquiry_message": inquiry.message,
                "property_title": getattr(prop, "property_title", "N/A"),
                "property_type": prop.__class__.__name__,
                "property_location": getattr(prop, "location", "N/A"),
                "property_price": getattr(prop, "price", "N/A"),
                "property_owner_name": getattr(owner, "full_name", owner.username),
                "property_owner_role": getattr(owner, "role", "N/A"),
                "lead_age": getattr(inquiry, "lead_age", "N/A"),
            })
        return data

    # Prepare inquiry data
    data = {
        "residential_inquiries": prepare_inquiry_data(residential_inquiries, "residential_property"),
        "commercial_inquiries": prepare_inquiry_data(commercial_inquiries, "commercial_property"),
        "pg_inquiries": prepare_inquiry_data(pg_inquiries, "pg_property"),
        "role": user.role,
        "user_full_name": getattr(user, "full_name", user.username),
    }

    template = "agent/inquiry_list.html"
    return render(request, template, data)

