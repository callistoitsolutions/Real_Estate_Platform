# referrals/views.py
from django.shortcuts import render, redirect, get_object_or_404,HttpResponse
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import AffiliateLink, ReferralConversion, CommissionPayout
from .utils import make_code, calculate_commission_for
from django.views.decorators.http import require_POST
from decimal import Decimal
from django.db import models
from Admin_App.models import *
from django.views.decorators.csrf import csrf_exempt
import traceback


def referral_redirect(request, code):
    """
    Route: /r/<code>/  - sets cookie and redirects to the affiliate's target URL.
    """
    aff = get_object_or_404(AffiliateLink, code=code, active=True)
    target = aff.get_target_url()
    response = redirect(target)
    response.set_cookie('referral', aff.code, max_age=60*60*24*30, samesite='Lax')
    return response

@login_required
@require_POST
def create_affiliate_link(request):
    owner = request.user
    target_type = request.POST.get('target_type', 'subscription')
    target_id = request.POST.get('target_id')
    code = make_code(prefix=f'RM{owner.id}')
    # ensure uniqueness
    while AffiliateLink.objects.filter(code=code).exists():
        code = make_code(prefix=f'RM{owner.id}')
    aff = AffiliateLink.objects.create(owner=owner, created_by=request.user, code=code, target_type=target_type, target_id=target_id)
    # return full absolute URL
    link = request.scheme + '://' + request.get_host() + aff.get_target_url()
    return JsonResponse({'ok': True, 'code': aff.code, 'link': link})

@login_required
@require_POST
def request_payout(request):
    code = request.POST.get('code')
    try:
        aff = AffiliateLink.objects.get(code=code, owner=request.user)
    except AffiliateLink.DoesNotExist:
        return JsonResponse({'ok': False, 'error': 'Not found'}, status=404)
    amount = Decimal(request.POST.get('amount') or 0)
    if amount <= 0:
        return JsonResponse({'ok': False, 'error': 'Invalid amount'}, status=400)
    payout = CommissionPayout.objects.create(affiliate=aff, total_amount=amount, status='requested')
    return JsonResponse({'ok': True, 'payout_id': str(payout.id)})

def is_staff(user):
    return user.is_staff

@login_required
@user_passes_test(is_staff)
@require_POST
def admin_create_affiliate_link(request):
    owner_id = request.POST.get('owner_id')
    from django.contrib.auth import get_user_model
    User = get_user_model()
    owner = get_object_or_404(User, pk=owner_id)
    code = make_code(prefix=f'RM{owner.id}')
    while AffiliateLink.objects.filter(code=code).exists():
        code = make_code(prefix=f'RM{owner.id}')
    aff = AffiliateLink.objects.create(owner=owner, created_by=request.user, code=code, target_type=request.POST.get('target_type','subscription'), target_id=request.POST.get('target_id'))
    link = request.scheme + '://' + request.get_host() + aff.get_target_url()
    return JsonResponse({'ok': True, 'code': aff.code, 'link': link})


def rm_dashboard(request):
    # 1. Retrieve identity from browser session
    user_id = request.session.get('User_id')
    user_role = request.session.get('user_type')

    # 2. Access Control: If ID is missing OR role is wrong, redirect to login
    if not user_id or user_role != "Relationship Manager":
        return redirect('login') 

    # 3. Data Fetching: Get the full user object for the template
    user_obj = User_Details.objects.get(id=user_id)
    
    context = {
        'user_obj': user_obj,
        'user_role': user_role
    }
    
    return render(request, "rm_panel/rm_dashboard.html", context)


############### Views start for user logout #####################

@csrf_exempt
def User_Logout(request):
    try:
        del request.session['User_id']
        del request.session['user_type']
        return JsonResponse({"status":"1",'msg': 'Logout Successfully '})
    except:
        print(traceback.format_exc())

######### Views end for user logout #############################


############ Views start for update rm profile #####################

def Update_Profile_Rm(request):
    # 1. Retrieve identity from browser session
    user_id = request.session.get('User_id')
    user_role = request.session.get('user_type')

    # 2. Access Control: If ID is missing OR role is wrong, redirect to login
    if not user_id or user_role != "Relationship Manager":
        return redirect('login') 

    # 3. Data Fetching: Get the full user object for the template
    user_obj = User_Details.objects.get(id=user_id)
    
    context = {
        'user_obj': user_obj,
        'user_role': user_role
    }
    
    return render(request, "rm_panel/Profile/rm_profile.html", context)

############## Views end for update rm profile ########################


############ Views start for rental forms for RM ######################

def residential_rm_list(request):
    # 1. Retrieve identity from browser session
    user_id = request.session.get('User_id')
    user_role = request.session.get('user_type')

    # 2. Access Control: If ID is missing OR role is wrong, redirect to login
    if not user_id or user_role != "Relationship Manager":
        return redirect('login') 

    # 3. Data Fetching: Get the full user object for the template
    user_obj = User_Details.objects.get(id=user_id)
    
    context = {
        'user_obj': user_obj,
        'user_role': user_role
    }
    
    return render(request, "rm_panel/Reports/Rental/residential_list.html", context)

############### Views end foor rental forms for RM #####################


############## Views start for rental forms for RM ###################

def residential_rm(request):
    # 1. Retrieve identity from browser session
    user_id = request.session.get('User_id')
    user_role = request.session.get('user_type')

    # 2. Access Control: If ID is missing OR role is wrong, redirect to login
    if not user_id or user_role != "Relationship Manager":
        return redirect('login') 

    # 3. Data Fetching: Get the full user object for the template
    user_obj = User_Details.objects.get(id=user_id)
    
    context = {
        'user_obj': user_obj,
        'user_role': user_role
    }
    
    return render(request, "rm_panel/Forms/Rental/residential.html", context)

############# Views end for rental forms for RM #######################


############# Views start for commercial list for RM ################

def commercial_rm_list(request):
    # 1. Retrieve identity from browser session
    user_id = request.session.get('User_id')
    user_role = request.session.get('user_type')

    # 2. Access Control: If ID is missing OR role is wrong, redirect to login
    if not user_id or user_role != "Relationship Manager":
        return redirect('login') 

    # 3. Data Fetching: Get the full user object for the template
    user_obj = User_Details.objects.get(id=user_id)
    
    context = {
        'user_obj': user_obj,
        'user_role': user_role
    }
    
    return render(request, "rm_panel/Reports/Rental/commercial_list.html", context)

############ Views end for commercial list for RM #######################


########## Views start for commercial forms for RM #####################

def commercial_rm(request):
     # 1. Retrieve identity from browser session
    user_id = request.session.get('User_id')
    user_role = request.session.get('user_type')

    # 2. Access Control: If ID is missing OR role is wrong, redirect to login
    if not user_id or user_role != "Relationship Manager":
        return redirect('login') 

    # 3. Data Fetching: Get the full user object for the template
    user_obj = User_Details.objects.get(id=user_id)
    
    context = {
        'user_obj': user_obj,
        'user_role': user_role
    }
    
    return render(request, "rm_panel/Forms/Rental/commercial.html", context)

########### Views end for commercial forms for RM ########################


############# Views start for pg forms for RM ########################

def pg_rm_list(request):
    # 1. Retrieve identity from browser session
    user_id = request.session.get('User_id')
    user_role = request.session.get('user_type')

    # 2. Access Control: If ID is missing OR role is wrong, redirect to login
    if not user_id or user_role != "Relationship Manager":
        return redirect('login') 

    # 3. Data Fetching: Get the full user object for the template
    user_obj = User_Details.objects.get(id=user_id)
    
    context = {
        'user_obj': user_obj,
        'user_role': user_role
    }
    
    return render(request, "rm_panel/Reports/Rental/pg_list.html", context)

############ Views end for pg forms for RM ############################


########## Views start for pg forms for RM #############################

def pg_rm(request):
    # 1. Retrieve identity from browser session
    user_id = request.session.get('User_id')
    user_role = request.session.get('user_type')

    # 2. Access Control: If ID is missing OR role is wrong, redirect to login
    if not user_id or user_role != "Relationship Manager":
        return redirect('login') 

    # 3. Data Fetching: Get the full user object for the template
    user_obj = User_Details.objects.get(id=user_id)
    
    context = {
        'user_obj': user_obj,
        'user_role': user_role
    }
    
    return render(request, "rm_panel/Forms/Rental/pg_coliving.html", context)

############# Views end for pg forms for RM ############################


############# Views start for resale property list ####################

def residential_resale_rm_list(request):
    return HttpResponse("Residential Resale List")



@login_required
def user_affiliate_links(request):
    links = AffiliateLink.objects.filter(owner=request.user).order_by('-created_at')
    return render(request, 'rm_panel/user_links.html', {'links': links})

@login_required
@user_passes_test(is_staff)
def admin_affiliate_detail(request, code):
    aff = get_object_or_404(AffiliateLink, code=code)
    visits = aff.visits.all().order_by('-created_at')[:100]
    conversions = aff.conversions.all().order_by('-created_at')[:100]
    return render(request, 'rm_panel/admin_affiliate_detail.html', {'affiliate': aff, 'visits': visits, 'conversions': conversions})




# in your orders/views.py (example)
from RM_Dashboard.models import AffiliateLink, ReferralConversion
from RM_Dashboard.utils import calculate_commission_for
from decimal import Decimal
from django.db import models

def checkout_complete(request):
    # ... your order save logic here ...
    order = ...  # saved order instance
    ref_code = request.POST.get('referral_code') or request.session.get('referral_code') or request.COOKIES.get('referral')
    if ref_code:
        try:
            aff = AffiliateLink.objects.get(code=ref_code, active=True)
            amount = Decimal(getattr(order, 'total_amount', 0) or 0)
            comm = calculate_commission_for(aff, amount)
            ReferralConversion.objects.create(
                affiliate=aff,
                user=request.user if request.user.is_authenticated else None,
                order_id=str(order.pk),
                amount=amount,
                commission_amount=comm,
                status='pending'
            )
            AffiliateLink.objects.filter(pk=aff.pk).update(
                registration_count=models.F('registration_count')+1,
                conversion_count=models.F('conversion_count')+1,
                commission_total=models.F('commission_total')+comm
            )
        except AffiliateLink.DoesNotExist:
            pass
    # continue response




def affilate_page(request):
    return render(request,"rm_panel/affilate_page.html")
