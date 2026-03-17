
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.urls import reverse
from django.db.models import Q
from .models import Vendor, VendorDocument,CommissionTransaction

import json
import uuid
from datetime import timedelta, datetime
from django.http import JsonResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.views.decorators.http import require_http_methods
from django.utils import timezone
from django.shortcuts import get_object_or_404
from .models import ServiceEnquiry, LeadShare, CommissionLedger, Vendor
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Q
from django.views.decorators.http import require_http_methods

from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.utils import timezone
from datetime import timedelta
from .models import ServiceEnquiry, LeadShare, Vendor
from django.shortcuts import render
from django.http import JsonResponse
from django.utils import timezone
from datetime import timedelta

from .models import ServiceEnquiry, Vendor, LeadShare
from decimal import Decimal, InvalidOperation
from django.db import transaction
from Admin_App.models import *






def vendors_Dashboard(request):
    # 1. Retrieve identity from browser session
    user_id = request.session.get('User_id')
    user_role = request.session.get('user_type')

    # 2. Access Control: If ID is missing OR role is wrong, redirect to login
    if not user_id or user_role != "Vendor":
        return redirect('login') 

    # 3. Data Fetching: Get the full user object for the template
    user_obj = User_Details.objects.get(id=user_id)
    
    context = {
        'user_obj': user_obj,
        'user_role': user_role
    }
    
    return render(request, "vendors_module/vendors_Dashboard.html", context) 



def vendor_registration(request):
    return render(request,"vendors_module/vendor_registration.html")













def register_vendor(request):
    if request.method == 'POST':
        try:
            data = request.POST
            files = request.FILES

            # Required fields check
            required = ['business_name','contact_person','phone','primary_service','service_mode','city','pincode','coverage_km']
            for f in required:
                if not data.get(f):
                    messages.error(request, f"Missing field: {f}")
                    return redirect(request.path)

            vendor = Vendor.objects.create(
                business_name=data['business_name'].strip(),
                contact_person=data['contact_person'].strip(),
                phone=data['phone'].strip(),
                email=data.get('email'),

                primary_service=data['primary_service'],
                service_mode=data['service_mode'],

                services=[],  # will update later

                special_tags=data.get('special_tags', '').strip(),
                city=data['city'],
                pincode=data['pincode'],

                company_reg_no=data.get('company_reg_no'),
                exp_year=int(data.get('exp_year') or 0),
                service_description=data.get('service_description', '').strip(),

                coverage_km=int(data['coverage_km']),

                pricing_model=data.get('pricing_model', 'flat'),
                price_flat=data.get('price_flat') or None,
                price_per_km=data.get('price_per_km') or None,
                price_per_hour=data.get('price_per_hour') or None,

                bank_account=data.get('bank_account'),
                vendor_status=data.get('vendor_status', 'normal'),
            )

            # Logo
            if 'logo' in files:
                vendor.logo = files['logo']
                vendor.save()

            # Multiple documents
            for doc in request.FILES.getlist('docs[]'):
                VendorDocument.objects.create(vendor=vendor, file=doc)

            # Multi services
            selected_services = data.getlist('services[]')
            vendor.services = selected_services
            vendor.save()

            messages.success(request, "Vendor registered successfully!")
            return redirect('vendor_directory')

        except Exception as e:
            messages.error(request, f"Error Saving Vendor → {str(e)}")
            print("SAVE ERROR:", e)
            return redirect(request.path)

    return render(request, 'vendors_module/vendor_registration.html')




def vendor_directory(request):
    # fetch all vendors, show featured first
    vendors = Vendor.objects.all().order_by('-vendor_status', '-created_at')  # vendor_status ordering may not be default; you can tweak
    context = {'vendors': vendors}
    return render(request, 'vendors_module/vendor_directory.html', context)


def vendor_filter(request):
    # GET params: category (primary_service), city, rating (optional)
    qs = Vendor.objects.all()
    category = request.GET.get('category')
    city = request.GET.get('city')
    rating = request.GET.get('rating')  # if you have rating stored; demo code does not have rating field

    if category:
        qs = qs.filter(primary_service__iexact=category)
    if city:
        qs = qs.filter(city__icontains=city)

    # If you have rating field, add filter: qs = qs.filter(rating__gte=float(rating))
    # For now we ignore rating.

    context = {'filtered_vendors': qs, 'filters': request.GET}
    return render(request, 'vendors_module/filter.html', context)


def vendor_detail(request, vendor_id):
    vendor = get_object_or_404(Vendor, pk=vendor_id)
    documents = vendor.documents.all()
    return render(request, 'vendors_module/vendor_detail.html', {'vendor': vendor, 'documents': documents})


def vendor_profile(request, vendor_id):
    vendor = get_object_or_404(Vendor, id=vendor_id)
    return render(request, 'vendors_module/vendor_profile.html', {'vendor': vendor})









# vendors_module/views.py (append)


#@require_http_methods(["POST"])







def get_unique_enquiry_id():
    """Generate a guaranteed unique enquiry ID"""
    while True:
        eid = 'ENQ-' + uuid.uuid4().hex[:10].upper()
        if not ServiceEnquiry.objects.filter(enquiry_id=eid).exists():
            return eid





def create_enquiry(request):

    # -------------------------
    # GET → Show form
    # -------------------------
    if request.method == "GET":
        return render(request, "vendors_module/enquiry_form.html")

    # -------------------------
    # POST → Save enquiry
    # -------------------------
    if request.method == "POST":

        # Customer details
        customer_name = request.POST.get("customer_name")
        customer_mobile = request.POST.get("customer_mobile")

        # Service details
        service = request.POST.get("service")
        city = request.POST.get("city")

        pickup_address = request.POST.get("pickup_address", "")
        drop_address = request.POST.get("drop_address", "")
        notes = request.POST.get("notes", "")
        preferred_dt = request.POST.get("preferred_dt", None)

        # -------------------------
        # Validation
        # -------------------------
        if not customer_name or not customer_mobile:
            return JsonResponse({'error': 'Customer name and mobile are required'}, status=400)

        if not service or not city:
            return JsonResponse({'error': 'service and city required'}, status=400)

        # -------------------------
        # Generate Unique Enquiry ID
        # -------------------------
        enquiry_id = get_unique_enquiry_id()

        # -------------------------
        # Create the enquiry
        # -------------------------
        enq = ServiceEnquiry.objects.create(
            enquiry_id=enquiry_id,

            # Customer details
            customer_name=customer_name,
            customer_mobile=customer_mobile,

            # Service details
            service=service,
            city=city,
            pickup_address=pickup_address,
            drop_address=drop_address,
            notes=notes,
            preferred_dt=preferred_dt if preferred_dt else None,

            created_by=request.user if request.user.is_authenticated else None,
            status="shared",
            expires_at=timezone.now() + timedelta(minutes=10)
        )

        # -------------------------
        # Vendor Matching
        # -------------------------
        matches = Vendor.objects.filter(
            primary_service=service,
            city=city
        )[:3]

        # Save vendor share entries
        for v in matches:
            LeadShare.objects.create(enquiry=enq, vendor=v)

        # -------------------------
        # Success page
        # -------------------------
        return render(request, "vendors_module/enquiry_success.html", {
            "enquiry": enq,
            "vendors": matches
        })



def match_vendors_for_enquiry(service, city, top_n=3):
    """
    Safe vendor matching for all DB engines.
    Supports:
    - primary_service (string)
    - services (JSON list)
    - city priority
    - verified / featured vendor scoring
    """

    # STEP 1 — Get all vendors (cheap)
    all_vendors = Vendor.objects.all()

    # STEP 2 — Filter vendors manually in Python to avoid DB contains error
    matched = []
    service_lower = service.lower().strip()

    for v in all_vendors:
        # match primary service
        if v.primary_service.lower() == service_lower:
            matched.append(v)
            continue

        # match JSON services (safe)
        if isinstance(v.services, list):
            s_list = [s.lower() for s in v.services]
            if service_lower in s_list:
                matched.append(v)

    # STEP 3 — Score vendors
    def score(v):
        s = 0

        # same-city boost
        if v.city and v.city.lower() == city.lower():
            s += 30

        # verified
        try:
            if callable(v.is_verified) and v.is_verified():
                s += 20
        except:
            pass

        # featured
        try:
            if callable(v.is_featured) and v.is_featured():
                s += 10
        except:
            pass

        return s

    matched.sort(key=lambda v: score(v), reverse=True)
    return matched[:top_n]




@require_http_methods(["GET"])
def auto_assign_enquiry(request, enquiry_id):

    # Admin only
    #if not request.user.is_staff:
       # return HttpResponseForbidden("Admin only")

    enquiry = get_object_or_404(ServiceEnquiry, enquiry_id=enquiry_id)

    # Already assigned / completed
    if enquiry.status in ["assigned", "completed"]:
        messages.error(request, "This enquiry is already assigned or completed.")
        return redirect("admin_enquiry_list")

    # Match vendors safely
    matches = match_vendors_for_enquiry(enquiry.service, enquiry.city, top_n=1)

    if not matches:
        enquiry.status = "no_response"
        enquiry.save()
        messages.warning(request, "No vendors matched for this enquiry.")
        return redirect("admin_enquiry_list")

    # choose top vendor
    vendor = matches[0]

    enquiry.assigned_vendor = vendor
    enquiry.status = "assigned"
    enquiry.save()

    # Create commission entry
    CommissionLedger.objects.create(
        enquiry=enquiry,
        vendor=vendor,
        total_amount=0,
        vendor_share=0,
        platform_profit=0
    )

    messages.success(request, f"Successfully assigned to {vendor.business_name}.")
    return redirect("admin_enquiry_list")




def manual_assign_enquiry(request, enquiry_id):
    #if not request.user.is_staff:
       # return HttpResponseForbidden('Admin only')

    enq = get_object_or_404(ServiceEnquiry, enquiry_id=enquiry_id)

    if request.method == "GET":
        vendors = Vendor.objects.all()
        return render(request, 'vendors_module/assign_enquiry.html', {
            'enquiry': enq,
            'vendors': vendors
        })

    # POST assign
    vendor_id = request.POST.get('vendor_id')
    if not vendor_id:
        return JsonResponse({'error': 'vendor_id required'}, status=400)

    vendor = get_object_or_404(Vendor, id=vendor_id)

    enq.assigned_vendor = vendor
    enq.status = 'assigned'
    enq.save()

    CommissionLedger.objects.update_or_create(
        enquiry=enq,
        defaults={'vendor': vendor, 'total_amount': 0, 'vendor_share': 0, 'platform_profit': 0}
    )

    return redirect('admin_enquiry_list')







#@login_required
def admin_enquiry_list(request):
    """
    Admin view page — renders template with enquiries for admin UI
    """
    #if not request.user.is_staff:
        #return redirect('vendor_directory')  # or permission denied

    enquiries = ServiceEnquiry.objects.all().order_by('-created_at')
    return render(request, 'vendors_module/admin_enquiry_list.html', {'enquiries': enquiries})

def enquiry_detail(request, enquiry_id):
    enq = get_object_or_404(ServiceEnquiry, enquiry_id=enquiry_id)
    shares = enq.lead_shares.all()
    return render(request, 'vendors_module/enquiry_detail.html', {'enquiry': enq, 'shares': shares})

def public_enquiry_list(request):
    """
    Optional list all enquiries for debug/pagination
    """
    qs = ServiceEnquiry.objects.all().order_by('-created_at')
    return render(request, 'vendors_module/enquiry_list.html', {'enquiries': qs})

def enquiry_form(request):
    return render(request, 'vendors_module/enquiry_form.html')


def all_links(request):
    return render(request, 'vendors_module/all_links.html')

def vendor_enquiries(request):
    test_city = "Ahmedabad"
    test_service = "Plumbing"

    enquiries = ServiceEnquiry.objects.filter(
        city__iexact=test_city,
        service__iexact=test_service
    ).exclude(status="assigned")

    return render(request, "vendors_module/vendor_enquiries.html", {"enquiries": enquiries})






# vendors_module/views.py (add these helpers & replace vendor_respond)


# --- Constants: tune these as per business rules ---
VENDOR_DEFAULT_COMMISSION_RATE = 60.0   # vendor keeps 60% by default (in percent)
PLATFORM_DEFAULT_COMMISSION_RATE = 40.0
INHOUSE_VENDOR_COMMISSION_RATE = 80.0   # if vendor is inhouse, they get more (example)
INHOUSE_PROMOTION_THRESHOLD = Decimal('50000.00')  # revenue threshold for auto-promotion
RM_BONUS_PERCENT = 5.0  # percentage of platform_profit that goes to RM (if assigned)

# --- Utility helpers ---
def get_vendor_commission_rate(vendor):
    """
    Returns float percent (0-100) of vendor share.
    Order:
     - vendor.commission_rate if set
     - if vendor.is_inhouse -> INHOUSE_VENDOR_COMMISSION_RATE
     - fallback: VENDOR_DEFAULT_COMMISSION_RATE
    """
    try:
        if vendor.commission_rate is not None:
            return float(vendor.commission_rate)
        if getattr(vendor, 'is_inhouse', False):
            return float(INHOUSE_VENDOR_COMMISSION_RATE)
    except Exception:
        pass
    return float(VENDOR_DEFAULT_COMMISSION_RATE)

def update_vendor_counters_on_new_lead(vendor, accepted=False, total_amount=0):
    """
    Increment vendor counters: total_leads, accepted_leads, and cumulative_revenue
    """
    vendor.total_leads = (vendor.total_leads or 0) + 1
    if accepted:
        vendor.accepted_leads = (vendor.accepted_leads or 0) + 1
        try:
            vendor.cumulative_revenue = (vendor.cumulative_revenue or Decimal('0')) + Decimal(str(total_amount))
        except Exception:
            pass
    vendor.save(update_fields=['total_leads', 'accepted_leads', 'cumulative_revenue'])


def check_and_promote_vendor_if_needed(vendor):
    """
    If vendor cumulative_revenue exceeds threshold, mark as rm_candidate or inhouse.
    Admin should confirm or you can auto-promote — here we set is_rm_candidate=True for admin review.
    """
    try:
        if vendor.cumulative_revenue >= INHOUSE_PROMOTION_THRESHOLD and not vendor.is_inhouse:
            vendor.is_rm_candidate = True
            vendor.save(update_fields=['is_rm_candidate'])
    except Exception as e:
        print("Error while checking vendor promotion:", e)




@require_http_methods(["POST"])
def vendor_respond(request, enquiry_id):
    """
    Vendor accepts/rejects a lead.
    Auto updates:
      - Vendor.is_inhouse = True on accept
      - Vendor.is_rm_candidate = True on accept
    """
    data = request.POST or json.loads(request.body.decode('utf-8') or '{}')
    vendor_id = data.get('vendor_id') or request.POST.get('vendor_id')
    action = data.get('action') or request.POST.get('action')
    total_amount_raw = data.get('total_amount') or request.POST.get('total_amount')
    paid_amount_raw = data.get('paid_amount') or request.POST.get('paid_amount')

    if not vendor_id or not action:
        return JsonResponse({'error': 'vendor_id and action required'}, status=400)

    enq = get_object_or_404(ServiceEnquiry, enquiry_id=enquiry_id)
    vendor = get_object_or_404(Vendor, id=vendor_id)

    # find LeadShare entry if exists
    share = None
    try:
        share = LeadShare.objects.get(enquiry=enq, vendor=vendor)
    except LeadShare.DoesNotExist:
        share = None

    # ========== REJECT ==========
    if action == 'reject':
        if share:
            share.responded = True
            share.accepted = False
            share.response_at = timezone.now()
            share.save()

        # remove vendor from shared_vendors list
        if isinstance(enq.shared_vendors, list) and vendor.id in enq.shared_vendors:
            enq.shared_vendors = [vid for vid in enq.shared_vendors if vid != vendor.id]
            enq.save(update_fields=['shared_vendors'])

        return JsonResponse({'status': 'rejected', 'vendor_id': vendor.id})

    # ========== ACCEPT ==========
    elif action == 'accept':

        # update LeadShare
        if share:
            share.responded = True
            share.accepted = True
            share.response_at = timezone.now()
            share.save()

        # assign enquiry
        enq.assigned_vendor = vendor
        enq.status = 'assigned'
        enq.save(update_fields=['assigned_vendor', 'status'])

        # parse amounts
        total_amount = None
        paid_amount = None
        try:
            if total_amount_raw:
                total_amount = Decimal(str(total_amount_raw))
            if paid_amount_raw:
                paid_amount = Decimal(str(paid_amount_raw))
        except (InvalidOperation, TypeError):
            total_amount = None
            paid_amount = None

        # compute commission
        vendor_rate_percent = Decimal(str(get_vendor_commission_rate(vendor)))
        if total_amount is not None:
            vendor_share = (total_amount * vendor_rate_percent / Decimal('100.0')).quantize(Decimal('0.01'))
            platform_profit = (total_amount - vendor_share).quantize(Decimal('0.01'))
        else:
            vendor_share = Decimal('0.00')
            platform_profit = Decimal('0.00')

        # create / update ledger
        with transaction.atomic():
            cl, created = CommissionLedger.objects.update_or_create(
                enquiry=enq,
                defaults={
                    'vendor': vendor,
                    'total_amount': total_amount or 0,
                    'vendor_share': vendor_share,
                    'platform_profit': platform_profit
                }
            )

            # paid amount during accept
            if paid_amount and paid_amount > 0:
                paid_to_vendor_amt = min(paid_amount, vendor_share) if vendor_share else Decimal('0.00')

                CommissionTransaction.objects.create(
                    ledger=cl,
                    amount=paid_to_vendor_amt,
                    paid_to_vendor=True,
                    paid_at=timezone.now(),
                    note=f"Recorded during accept by vendor {vendor.id}"
                )

                cl.paid_amount = (cl.paid_amount or Decimal('0')) + paid_to_vendor_amt
                if cl.paid_amount >= cl.vendor_share:
                    cl.paid = True
                cl.save(update_fields=['paid_amount', 'paid'])

        # update vendor counters
        update_vendor_counters_on_new_lead(vendor, accepted=True, total_amount=total_amount or 0)

        # check promotion
        check_and_promote_vendor_if_needed(vendor)

        # ============================
        # NEW 1: Auto-mark INHOUSE
        # ============================
        vendor.is_inhouse = True

        # ============================
        # NEW 2: Auto-mark RM Candidate
        # ============================
        vendor.is_rm_candidate = True

        vendor.save(update_fields=['is_inhouse', 'is_rm_candidate'])

        # assign RM if enquiry has created_by
        if getattr(enq, 'created_by', None):
            CommissionLedger.objects.filter(enquiry=enq).update(
                assigned_rm=enq.created_by
            )

        return JsonResponse({
            'status': 'accepted',
            'vendor_id': vendor.id,
            'commission': {
                'total_amount': str(cl.total_amount),
                'vendor_share': str(cl.vendor_share),
                'platform_profit': str(cl.platform_profit),
                'paid_amount': str(cl.paid_amount),
                'outstanding': str(cl.total_amount - cl.paid_amount if cl.total_amount else 0)
            }
        })

    else:
        return JsonResponse({'error': 'invalid action'}, status=400)


# admin report view
def admin_vendor_performance(request):
    # if not request.user.is_staff: return redirect('vendor_directory')
    vendors = Vendor.objects.order_by('-cumulative_revenue')[:100]
    # You can annotate with counts if you want using Django ORM aggregates
    context = {'vendors': vendors}
    return render(request, 'vendors_module/admin_vendor_performance.html', context)

# vendor dashboard
#@login_required
def my_vendor_dashboard(request, vendor_id):
    vendor = get_object_or_404(Vendor, id=vendor_id)
    # ensure only vendor owner or admin can see
    # you must define an ownership rule (here we assume staff or maybe vendor has user owner)
    # For demo allow staff or superuser
    if not request.user.is_staff:
        # optionally check vendor.owner == request.user
        pass

    # stats
    total_leads = vendor.total_leads
    accepted_leads = vendor.accepted_leads
    revenue = vendor.cumulative_revenue
    unpaid_ledgers = CommissionLedger.objects.filter(vendor=vendor).exclude(paid=True)
    transactions = CommissionTransaction.objects.filter(ledger__vendor=vendor).order_by('-created_at')[:50]

    context = {
        'vendor': vendor,
        'total_leads': total_leads,
        'accepted_leads': accepted_leads,
        'revenue': revenue,
        'unpaid_ledgers': unpaid_ledgers,
        'transactions': transactions
    }
    return render(request, 'vendors_module/vendor_dashboard.html', context)



@require_http_methods(["POST"])
def admin_mark_inhouse(request, vendor_id):
   # if not request.user.is_staff:
      #  return HttpResponseForbidden("Admin only")
    v = get_object_or_404(Vendor, id=vendor_id)
    v.is_inhouse = True
    v.is_rm_candidate = False
    v.save(update_fields=['is_inhouse', 'is_rm_candidate'])
    messages.success(request, f"{v.business_name} marked as inhouse.")
    return redirect('admin_vendor_performance')
