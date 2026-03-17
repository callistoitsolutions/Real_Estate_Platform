from django.shortcuts import render

# Create your views here.
from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from django.contrib import messages
from django.shortcuts import render,redirect,get_object_or_404
from Agent_Dashboard .models import *
from django.contrib.auth.decorators import login_required
from Admin_App.models import *


# Create your views here.

########### Crime Officer Views#######


def Wallet_Recharge_agent(request):
    return render(request,"agent/Wallet_Recharge_agent.html") 


def agent_dashboard(request):
    # 1. Retrieve identity from browser session
    user_id = request.session.get('User_id')
    user_role = request.session.get('user_type')

    # 2. Access Control: If ID is missing OR role is wrong, redirect to login
    if not user_id or user_role != "Agent":
        return redirect('login') 

    # 3. Data Fetching: Get the full user object for the template
    user_obj = User_Details.objects.get(id=user_id)
    
    context = {
        'user_obj': user_obj,
        'user_role': user_role
    }
    
    return render(request, "agent/agent_dashboard.html", context) 



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

