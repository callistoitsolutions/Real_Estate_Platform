
# Create your views here.
from django.shortcuts import render
from django.contrib import messages
from django.shortcuts import render,redirect,HttpResponse
from Main_App .models import *
from Admin_App .models import *
from seo .models import *
from django.db.models import Q
# rental_app/views.py

from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.conf import settings
#from .models import CustomUser, SignupDraft, LeadCapture, ResidentialProperty, CommercialProperty, PGProperty
from captcha.models import CaptchaStore
from captcha.helpers import captcha_image_url


# ---------------- LOGIN ----------------
from django.shortcuts import resolve_url
from django.utils.http import url_has_allowed_host_and_scheme

from django.shortcuts import render, redirect, get_object_or_404

from datetime import datetime, timedelta
from datetime import date
import json
from Admin_App.models import *
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import traceback
from django.urls import reverse

# Create your views here.

########### Crime Officer Views#######


from itertools import chain







def portalpage(request):
    hero = HeroSection.objects.filter(is_active=True).first()
    blogs = Blog.objects.all().order_by("-date_posted")
    faqs = FAQ.objects.all().order_by('-created_at')

    # ✅ CORRECT FUNCTION CALL
    residential = list(get_featured_queryset(ResidentialProperty))
    commercial = list(get_featured_queryset(CommercialProperty))
    pg = list(get_featured_queryset(PGProperty))

    # Combine
    all_props = (
        [{"data": prop, "type": "Residential"} for prop in residential] +
        [{"data": prop, "type": "Commercial"} for prop in commercial] +
        [{"data": prop, "type": "PG"} for prop in pg]
    )

    random.shuffle(all_props)
    featured_props = all_props[:6]

    props = sorted(
        chain(residential, commercial, pg),
        key=lambda x: getattr(x, 'created_at', None),
        reverse=True
    )

    context = {
        "featured_props": featured_props,
        "props": props,
        "hero": hero,
        "blogs": blogs,
        "faqs": faqs,
    }

    return render(request, "home_page/portalpage.html", context)






import re



# ─────────────────────────────────────────────────────────────────────────────
#  MAIN VIEW
# ─────────────────────────────────────────────────────────────────────────────





def property_detail_view(request, listing_type, category, pk):
    # Fetch based on category to handle multiple models
    if listing_type == 'rent':
        if category == 'residential':
            obj = get_object_or_404(RentalResidentialProperty, pk=pk)
            p = _normalize_rental(obj)
        elif category == 'commercial':
            obj = get_object_or_404(CommercialRentalProperty, pk=pk)
            p = _normalize_commercial_rental(obj)
        elif category == 'pg':
            obj = get_object_or_404(PGColivingProperty, pk=pk)
            p = _normalize_pg(obj)
            
    elif listing_type == 'sale':
        if category == 'residential':
            obj = get_object_or_404(ResaleResidentialProperty, pk=pk)
            p = _normalize_resale(obj)
        elif category == 'commercial':
            obj = get_object_or_404(CommercialResaleProperty, pk=pk)
            p = _normalize_commercial_resale(obj)

    return render(request, 'home_page/property_detail.html', {'p': p, 'original': obj})


def listings_view(request):
    listing_type = request.GET.get('type',     'rent').strip()
    category     = request.GET.get('category', 'residential').strip()
    bhk          = request.GET.get('bhk',      '').strip()
    budget       = request.GET.get('budget',   '').strip()
    furnishing   = request.GET.get('furnishing','').strip()
    area         = request.GET.get('area',     '').strip()
    sort         = request.GET.get('sort',     'relevant').strip()

    # Normalize BHK: "2BHK" → "2 BHK"
    bhk = re.sub(r'(\d)(BHK)', r'\1 \2', bhk)
    bhk = re.sub(r'(\d)(RK)',  r'\1 \2', bhk)

    properties  = []
    page_title  = 'Properties'

    # ── RENT → RESIDENTIAL ───────────────────────────────────────────────────
    if listing_type == 'rent' and category == 'residential':
        page_title = 'Flats & Houses for Rent'
        qs = RentalResidentialProperty.objects.all()

        if bhk:
            qs = qs.filter(bhk_type__icontains=bhk)
        if budget:
            low, high = _parse_rent_budget(budget)
            if low  is not None: qs = qs.filter(monthly_rent__gte=low)
            if high is not None: qs = qs.filter(monthly_rent__lte=high)
        if furnishing:
            qs = qs.filter(furnishing_status__icontains=furnishing)
        if area:
            qs = qs.filter(Q(locality__icontains=area) | Q(city__icontains=area))

        qs = _sort_qs(qs, sort, 'monthly_rent')
        for p in qs:
            properties.append(_normalize_rental(p))

    # ── RENT → COMMERCIAL ────────────────────────────────────────────────────
    elif listing_type == 'rent' and category == 'commercial':
        page_title = 'Commercial Spaces for Rent'
        qs = CommercialRentalProperty.objects.all()

        if area:
            qs = qs.filter(Q(area_locality__icontains=area) | Q(city__icontains=area))
        if budget:
            low, high = _parse_rent_budget(budget)
            if low  is not None: qs = qs.filter(expected_rent__gte=low)
            if high is not None: qs = qs.filter(expected_rent__lte=high)

        qs = _sort_qs(qs, sort, 'expected_rent')
        for p in qs:
            properties.append(_normalize_commercial_rental(p))

    # ── RENT → PG / CO-LIVING ────────────────────────────────────────────────
    elif listing_type == 'rent' and category == 'pg':
        page_title = 'PG & Co-living Spaces'
        qs = PGColivingProperty.objects.all()

        if area:
            qs = qs.filter(Q(locality__icontains=area) | Q(city__icontains=area))
        if budget:
            low, high = _parse_rent_budget(budget)
            if low  is not None: qs = qs.filter(rent__gte=low)
            if high is not None: qs = qs.filter(rent__lte=high)
        if furnishing:
            qs = qs.filter(furnishing_type__icontains=furnishing)

        qs = _sort_qs(qs, sort, 'rent')
        for p in qs:
            properties.append(_normalize_pg(p))

    # ── SALE → RESIDENTIAL ───────────────────────────────────────────────────
    elif listing_type == 'sale' and category == 'residential':
        page_title = 'Flats & Houses for Sale'
        qs = ResaleResidentialProperty.objects.all()

        if bhk:
            qs = qs.filter(bhk__icontains=bhk)
        if budget:
            low, high = _parse_sale_budget(budget)
            if low  is not None: qs = qs.filter(expected_price__gte=low)
            if high is not None: qs = qs.filter(expected_price__lte=high)
        if furnishing:
            qs = qs.filter(furnishing_type__icontains=furnishing)
        if area:
            qs = qs.filter(Q(locality__icontains=area) | Q(city__icontains=area))

        qs = _sort_qs(qs, sort, 'expected_price')
        for p in qs:
            properties.append(_normalize_resale(p))

    # ── SALE → COMMERCIAL ────────────────────────────────────────────────────
    elif listing_type == 'sale' and category == 'commercial':
        page_title = 'Commercial Properties for Sale'
        qs = CommercialResaleProperty.objects.filter(is_active=True)

        if area:
            qs = qs.filter(Q(locality__icontains=area) | Q(city__icontains=area))
        if budget:
            low, high = _parse_sale_budget(budget)
            if low  is not None: qs = qs.filter(expected_price__gte=low)
            if high is not None: qs = qs.filter(expected_price__lte=high)

        qs = _sort_qs(qs, sort, 'expected_price')
        for p in qs:
            properties.append(_normalize_commercial_resale(p))

    # ── SALE → PLOT / AGRICULTURE / INDUSTRIAL (models pending) ─────────────
    elif listing_type == 'sale' and category in ('plot', 'agriculture', 'industrial'):
        page_title = f'{category.title()} Properties for Sale'
        # These models don't exist yet — show empty with friendly message
        properties = []

    # ── CONTEXT ──────────────────────────────────────────────────────────────
    context = {
        'properties':         properties,
        'listing_type':       listing_type,
        'category':           category,
        'page_title':         page_title,
        'total':              len(properties),
        'current_bhk':        bhk,
        'current_budget':     budget,
        'current_furnishing': furnishing,
        'current_area':       area,
        'current_sort':       sort,
    }
    return render(request, 'home_page/listingpage.html', context)


# ─────────────────────────────────────────────────────────────────────────────
#  SORT HELPER
# ─────────────────────────────────────────────────────────────────────────────

def _sort_qs(qs, sort, price_field):
    if sort == 'newest':
        return qs.order_by('-id')
    elif sort == 'price-asc':
        return qs.order_by(price_field)
    elif sort == 'price-desc':
        return qs.order_by(f'-{price_field}')
    return qs


# ─────────────────────────────────────────────────────────────────────────────
#  NORMALIZERS
# ─────────────────────────────────────────────────────────────────────────────

def _initials(name):
    return ''.join([w[0] for w in (name or 'UN').split() if w])[:2].upper()


def _normalize_rental(p):
    rent = p.monthly_rent or 0
    return {
        'id':             p.pk,
        'title':          p.property_title or 'Rental Property',
        'listing_type':   'rent',
        'category':       'residential',
        'price_display':  f'₹{rent:,}/mo',
        'price_num':      rent,
        'area':           f'{p.built_up_area} sqft' if p.built_up_area else '—',
        'beds':           p.bhk_type or '—',
        'baths':          p.bathrooms or 0,
        'floor':          f'{p.floor_number}/{p.total_floors}' if p.floor_number else '—',
        'location':       f'{p.locality}, {p.city}' if p.locality and p.city else (p.city or '—'),
        'furnished':      p.furnishing_status or '—',
        'available':      str(p.available_from) if p.available_from else 'Available Now',
        'owner':          p.owner_name or 'Owner',
        'owner_initials': _initials(p.owner_name),
        'owner_role':     p.uploaded_by_role or 'Owner',
        'phone':          p.contact_number or '',
        'is_new':         False,
        'badges':         [],
        'emoji':          '🏠',
    }


def _normalize_commercial_rental(p):
    rent = p.expected_rent or 0
    return {
        'id':             p.pk,
        'title':          p.property_title or p.property_type or 'Commercial Space',
        'listing_type':   'rent',
        'category':       'commercial',
        'price_display':  f'₹{rent:,}/mo',
        'price_num':      rent,
        'area':           f'{p.builtup_area} sqft' if p.builtup_area else '—',
        'beds':           '—',
        'baths':          p.private_washroom or 0,
        'floor':          f'{p.your_floor}/{p.total_floors}' if p.your_floor else '—',
        'location':       f'{p.area_locality}, {p.city}' if p.area_locality and p.city else (p.city or '—'),
        'furnished':      p.property_condition or '—',
        'available':      str(p.available_from) if p.available_from else 'Available Now',
        'owner':          p.owner_name or 'Owner',
        'owner_initials': _initials(p.owner_name),
        'owner_role':     p.uploaded_by_role or 'Owner',
        'phone':          p.contact_number or '',
        'is_new':         False,
        'badges':         ['commercial'],
        'emoji':          '🏗',
    }


def _normalize_pg(p):
    rent = p.rent or 0
    return {
        'id':             p.pk,
        'title':          p.pg_name or 'PG / Co-living',
        'listing_type':   'rent',
        'category':       'pg',
        'price_display':  f'₹{rent:,}/mo',
        'price_num':      rent,
        'area':           '—',
        'beds':           p.room_type or '—',
        'baths':          0,
        'floor':          '—',
        'location':       f'{p.locality}, {p.city}' if p.locality and p.city else (p.city or '—'),
        'furnished':      p.furnishing_type or '—',
        'available':      str(p.available_from) if p.available_from else 'Available Now',
        'owner':          p.owner_name or 'Owner',
        'owner_initials': _initials(p.owner_name),
        'owner_role':     p.uploaded_by_role or 'Owner',
        'phone':          p.contact_number or '',
        'is_new':         False,
        'badges':         ['pg'],
        'emoji':          '🏡',
    }


def _normalize_resale(p):
    price = int(p.expected_price) if p.expected_price else 0
    crore = price / 10_000_000
    lakh  = price / 100_000
    price_display = f'₹{crore:.2f} Cr' if crore >= 1 else f'₹{lakh:.1f} L'
    return {
        'id':             p.pk,
        'title':          p.title or 'Resale Property',
        'listing_type':   'sale',
        'category':       'residential',
        'price_display':  price_display,
        'price_num':      price,
        'area':           f'{p.builtup_area} sqft' if p.builtup_area else '—',
        'beds':           p.bhk or '—',
        'baths':          p.bathrooms or 0,
        'floor':          f'{p.floor_no}/{p.total_floors}' if p.floor_no else '—',
        'location':       f'{p.locality}, {p.city}' if p.locality and p.city else (p.city or '—'),
        'furnished':      p.furnishing_type or '—',
        'available':      str(p.available_from) if p.available_from else 'Available Now',
        'owner':          p.owner_name or 'Owner',
        'owner_initials': _initials(p.owner_name),
        'owner_role':     p.uploaded_by_role or 'Owner',
        'phone':          p.owner_contact or '',
        'is_new':         False,
        'badges':         ['sale'],
        'emoji':          '🏘',
    }


def _normalize_commercial_resale(p):
    price = int(p.expected_price) if p.expected_price else 0
    crore = price / 10_000_000
    lakh  = price / 100_000
    price_display = f'₹{crore:.2f} Cr' if crore >= 1 else f'₹{lakh:.1f} L'
    return {
        'id':             p.pk,
        'title':          p.title or 'Commercial Property',
        'listing_type':   'sale',
        'category':       'commercial',
        'price_display':  price_display,
        'price_num':      price,
        'area':           f'{p.builtup_area} sqft' if p.builtup_area else '—',
        'beds':           '—',
        'baths':          0,
        'floor':          '—',
        'location':       f'{p.locality}, {p.city}' if p.locality and p.city else (p.city or '—'),
        'furnished':      p.property_condition or '—',
        'available':      str(p.available_from) if p.available_from else 'Available Now',
        'owner':          p.owner_name or 'Owner',
        'owner_initials': _initials(p.owner_name),
        'owner_role':     p.uploaded_by_role or 'Owner',
        'phone':          p.owner_contact or '',
        'is_new':         False,
        'badges':         ['commercial', 'sale'],
        'emoji':          '🏗',
    }


# ─────────────────────────────────────────────────────────────────────────────
#  BUDGET PARSERS
# ─────────────────────────────────────────────────────────────────────────────

def _parse_rent_budget(budget):
    MAP = {
        'Under ₹10K':  (None,  10000),
        '₹10K–20K':    (10000, 20000),
        '₹20K–35K':    (20000, 35000),
        'Under ₹8K':   (None,   8000),
        '₹8K–15K':     (8000,  15000),
        '₹15K–25K':    (15000, 25000),
        '₹25K–40K':    (25000, 40000),
        '₹40K+':       (40000,  None),
    }
    return MAP.get(budget, (None, None))


def _parse_sale_budget(budget):
    MAP = {
        'Under ₹30L':  (None,        3_000_000),
        '₹30L–60L':    (3_000_000,   6_000_000),
        '₹60L+':       (6_000_000,   None),
    }
    return MAP.get(budget, (None, None))

@csrf_exempt
def Adminlogin(request):
    session_id = request.session.get('Admin_id')
    user_type = request.session.get('user_type')
    if request.method == "POST":
        try:
            data = json.loads(request.body.decode('utf-8'))
            email = data['email']
            password = data['password']
            
            if Admin_Login.objects.filter(email=email, password=password):

                obj = Admin_Login.objects.get(email=email, password=password)
                
                request.session['Admin_id'] = str(obj.id)
                request.session['user_type'] = str('Admin')

                send_data = {'status':1,'msg':'Login Successful...'}
            else:
                send_data = {'status':0,'msg':'Invalid Credentials'}
        except:
            print(traceback.format_exc())
            send_data = {'status':0 , 'msg':'Something went wrong','error':traceback.format_exc()}
        return JsonResponse(send_data)
    else:
        if session_id and user_type == "Admin":
            return redirect('admin_page')
        else:
            return render(request,'home_page/Adminlogin.html')
        


############### Views start for admin logout ########################

@csrf_exempt
def Admin_Logout(request):
    try:
        del request.session['Admin_id']
        del request.session['user_type']
        return JsonResponse({"status":"1",'msg': 'Logout Successfully '})
    except:
        print(traceback.format_exc())

############### Views end for admin logout ###########################





# Helper to get client IP
def get_client_ip(request):
    return request.META.get('REMOTE_ADDR')

# ---------------- HOME ----------------


# ---------------- SIGNUP ----------------
def signup_view(request):
    if request.method == 'GET':
        new_key = CaptchaStore.generate_key()
        captcha_img = captcha_image_url(new_key)
        return render(request, 'home_page/signup.html', {
            'captcha_key': new_key,
            'captcha_img': captcha_img,
        })

    # Save draft safely
    SignupDraft.objects.create(
        full_name=request.POST.get('full_name'),
        email=request.POST.get('email'),
        role=request.POST.get('role'),
        referral_source=request.POST.get('referral_source') or "unknown",
        ip_address=get_client_ip(request),
    )

    # Captcha
    user_captcha = request.POST.get('captcha')
    captcha_key = request.POST.get('captcha_key')
    try:
        captcha_obj = CaptchaStore.objects.get(hashkey=captcha_key)
    except CaptchaStore.DoesNotExist:
        messages.error(request, "Captcha expired. Please try again.")
        return redirect('signup')

    if captcha_obj.response != (user_captcha or "").lower():
        messages.error(request, "Invalid captcha. Draft saved.")
        captcha_obj.delete()
        return redirect('signup')

    # Duplicate email
    if CustomUser.objects.filter(email=request.POST['email']).exists():
        messages.error(request, "User already exists. Please login.")
        captcha_obj.delete()
        return redirect('login')

    # Create user safely
    user = CustomUser.objects.create_user(
        username=request.POST['email'].split('@')[0],
        email=request.POST['email'],
        password=request.POST['password'],
        role=request.POST.get('role'),
        referral_source=request.POST.get('referral_source') or "unknown",
    )

    login(request, user, backend='django.contrib.auth.backends.ModelBackend')
    captcha_obj.delete()

    messages.success(request, "Signup successful! Welcome.")
    return redirect('dashboard12')


@csrf_exempt
def login_view(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body.decode('utf-8'))
            user_email = data['user_email']
            user_password = data['user_password']
            user_role = data.get('user_role') 
            
            user_qs = User_Details.objects.filter(user_email=user_email, user_password=user_password, user_role=user_role)
            
            if user_qs.exists():
                user_obj = user_qs.first()
                
                # --- SESSION LOGIC ---
                # Note: Logging in a new person will overwrite these session keys
                request.session['User_id'] = str(user_obj.id)
                request.session['user_type'] = user_role
                
                if user_role == "Relationship Manager":
                    url = reverse('rm_dashboard')
                
                if user_role == "Landlord":
                    url = reverse('landlord_dashboard')
                
                if user_role == "Agent":
                    url = reverse('agent_dashboard')

                if user_role == "Vendor":
                    url = reverse('Vendors:vendors_Dashboard')

                if user_role == "Tenant":
                    url = reverse('Tenant_App:tenant_Dashboard')

                if user_role == "Buyer":
                    url = reverse('Buyer_Dashboard')

                if user_role == "Agency/Builder":
                    url = reverse('Agency_Dashboard')

                return JsonResponse({'status': 1, 'msg': f'{user_role} Login Successful', 'redirect_url': url})

            return JsonResponse({'status': 0, 'msg': 'Invalid Credentials or Role Selection'})

        except Exception:
            print(traceback.format_exc())
            return JsonResponse({'status': 0, 'msg': 'Something went wrong'})
    
    # --- UPDATED GET LOGIC ---
    # We remove the auto-redirect here so that the login page 
    # is ALWAYS accessible for new users to log in.
    return render(request, 'home_page/login.html')


# ---------------- DASHBOARD ----------------
@login_required
def dashboard_view(request):
    return render(request, 'home_page/dashboard12.html')


# ---------------- LEAD CAPTURE ----------------


from django.shortcuts import render, redirect
from django.contrib import messages
from .models import LeadCapture

def lead_capture_view(request):

    if request.method == 'GET':
        return render(request, 'home_page/lead_capture.html')

    # Create lead (no age field, auto-calculated)
    lead = LeadCapture.objects.create(
        name=request.POST.get('name'),
        email=request.POST.get('email'),
        designation=request.POST.get('designation'),
        intent_type=request.POST.get('intent_type'),
        property_category=request.POST.get('property_category'),
        property_subtype=request.POST.get('property_subtype'),
        message=request.POST.get('message', '')
    )

    # Store Lead ID in session
    request.session['lead'] = lead.lead_id

    messages.success(request, f"Lead captured successfully! Your Lead ID: {lead.lead_id}")

    return redirect('post_property')



# ---------------- POST PROPERTY ----------------




def post_property_view(request):
    context = {
        'is_guest': not request.user.is_authenticated,
        'lead_email': request.session.get('lead', ''),
    }

    if request.method == 'GET':
        return render(request, 'home_page/post_property.html', context)

    # Handle POST request
    # Lead capture for guests
    lead = None
    if not request.user.is_authenticated:
        lead_email = request.POST.get('email')
        lead_name = request.POST.get('name')
        designation = request.POST.get('designation', '')
        intent_type = request.POST.get('property_purpose', 'rent_lease')
        property_category = request.POST.get('property_category')
        property_subtype = request.POST.get('property_subtype', '')
        message = request.POST.get('message', '')

        lead, created = LeadCapture.objects.get_or_create(
            email=lead_email,
            defaults={
                'name': lead_name,
                'designation': designation,
                'intent_type': intent_type,
                'property_category': property_category,
                'property_subtype': property_subtype,
                'message': message,
            }
        )
        request.session['lead'] = lead.email

    prop_category = request.POST.get('property_category')
    purpose = request.POST.get('property_purpose') or 'Rent/Lease'
    subtype = request.POST.get('property_subtype') or ''
    designation = request.POST.get('designation') or 'tenant'

    try:
        # === RESIDENTIAL PROPERTY ===
        if prop_category == 'residential':
            # Helper function to get checkbox values as comma-separated string
            def get_checkbox_values(field_name):
                values = request.POST.getlist(field_name)
                return ','.join(values) if values else ''

            obj = ResidentialProperty(
                posted_by=request.user if request.user.is_authenticated else None,
                lead=lead if lead else None,
                
                # Basic Details
                property_title=request.POST.get('property_title', ''),
                city=request.POST.get('city', ''),
                area=request.POST.get('area', ''),
                property_address=request.POST.get('property_address', ''),
                property_type=request.POST.get('property_type', ''),
                builtup_area=float(request.POST.get('builtup_area') or 0),
                carpet_area=float(request.POST.get('carpet_area') or 0),
                zone=request.POST.get('zone', ''),
                society_type=request.POST.get('society_type', ''),
                recommended_for=get_checkbox_values('recommended_for[]'),
                
                # Property Details
                bedrooms=int(request.POST.get('bedrooms') or 0),
                bathrooms=int(request.POST.get('bathrooms') or 0),
                balconies=int(request.POST.get('balconies') or 0),
                furnishing=request.POST.get('furnishing', ''),
                floor_no=int(request.POST.get('floor_no') or 0),
                total_floors=int(request.POST.get('total_floors') or 0),
                age_of_property=int(request.POST.get('age_of_property') or 0),
                water_type=request.POST.get('water_type', ''),
                
                # Rent Details
                rent_price=float(request.POST.get('rent_price') or 0),
                security_deposit=float(request.POST.get('security_deposit') or 0),
                maintenance=float(request.POST.get('maintenance') or 0),
                
                # Featured & Verified
                is_featured=request.POST.get('is_featured', 'No'),
                featured_days=int(request.POST.get('featured_days') or 0) if request.POST.get('featured_days') else None,
                manual_featured_days=int(request.POST.get('manual_featured_days') or 0) if request.POST.get('manual_featured_days') else None,
                featured_start_date=request.POST.get('featured_start_date') or None,
                featured_end_date=request.POST.get('featured_end_date') or None,
                service_amount=float(request.POST.get('service_amount') or 0) if request.POST.get('service_amount') else None,
                placement=request.POST.get('placement', ''),
                is_verified=request.POST.get('is_verified', 'no'),
                
                # Brokerage
                brokerage_applicable=request.POST.get('brokerage_applicable', 'No'),
                brokerage_payer=request.POST.get('brokeragePayer', ''),
                brokerage_type=request.POST.get('brokerageType', ''),
                brokerage_value=float(request.POST.get('brokerageValue') or 0) if request.POST.get('brokerageValue') else None,
                percentage_extra=float(request.POST.get('percentageExtra') or 0) if request.POST.get('percentageExtra') else None,
                brokerage_description=request.POST.get('brokerageDescription', ''),
                
                # Video & Exclusive
                exclusive_property='exclusive_property' in request.POST,
                upload_video='upload_video' in request.POST,
                video_url=request.POST.get('video_url', ''),
                video_from=request.POST.get('video_from') or None,
                video_to=request.POST.get('video_to') or None,
                video_platforms=get_checkbox_values('video_platforms[]'),
                
                # Facilities & Amenities
                nearby_facilities=get_checkbox_values('nearby_facilities[]'),
                amenities=get_checkbox_values('amenities[]'),
                description=request.POST.get('description', ''),
                
                created_at=timezone.now(),
            )

        # === COMMERCIAL PROPERTY ===
        elif prop_category == 'commercial':
            def get_checkbox_values(field_name):
                values = request.POST.getlist(field_name)
                return ','.join(values) if values else ''

            obj = CommercialProperty(
                posted_by=request.user if request.user.is_authenticated else None,
                lead=lead if lead else None,
                
                # Basic Details
                property_type=request.POST.get('property_type', ''),
                city=request.POST.get('city', ''),
                area_locality=request.POST.get('area_locality', ''),
                property_address=request.POST.get('property_address', ''),
                building_name=request.POST.get('building_name', ''),
                possession_status=request.POST.get('possession_status', ''),
                age_of_property=int(request.POST.get('age_of_property') or 0),
                zone_type=request.POST.get('zone_type', ''),
                location_hub=request.POST.get('location_hub', ''),
                property_condition=request.POST.get('property_condition', ''),
                ownership_type=request.POST.get('ownership_type', ''),
                construction_status=request.POST.get('construction_status', ''),
                
                # Property Details
                builtup_area=int(request.POST.get('builtup_area') or 0),
                carpet_area=int(request.POST.get('carpet_area') or 0),
                total_floors=int(request.POST.get('total_floors') or 0),
                your_no=int(request.POST.get('your_no') or 0),
                no_of_staircase=int(request.POST.get('no_of_staircase') or 0),
                passenger_lifts=int(request.POST.get('passenger_lifts') or 0),
                service_lifts=int(request.POST.get('service_lifts') or 0),
                private_parking=int(request.POST.get('private_parking') or 0),
                public_parking=int(request.POST.get('public_parking') or 0),
                minimum_seats=int(request.POST.get('minimum_seats') or 0),
                maximum_seats=int(request.POST.get('maximum_seats') or 0),
                number_of_cabin=int(request.POST.get('number_of_cabin') or 0),
                meeting_room=int(request.POST.get('meeting_room') or 0),
                floring_type=request.POST.get('floring_type', ''),
                
                # Rent Details
                expected_rent=float(request.POST.get('expected_rent') or 0),
                security_deposit=float(request.POST.get('security_deposit') or 0),
                maintenance_charges=float(request.POST.get('maintenance_charges') or 0),
                rent_available_from=request.POST.get('available_from') or None,
                lock_in_period=int(request.POST.get('lock_in_period') or 0),
                rent_increase=float(request.POST.get('rent_increase') or 0),
                
                # Featured & Verified
                is_featured='is_featured' in request.POST or request.POST.get('is_featured') == 'Yes',
                featured_days=int(request.POST.get('featured_days') or 0) if request.POST.get('featured_days') else None,
                manual_featured_days=int(request.POST.get('manual_featured_days') or 0) if request.POST.get('manual_featured_days') else None,
                featured_start_date=request.POST.get('featured_start_date') or None,
                featured_end_date=request.POST.get('featured_end_date') or None,
                service_amount=float(request.POST.get('service_amount') or 0),
                placement=request.POST.get('placement', ''),
                is_verified='is_verified' in request.POST or request.POST.get('is_verified') == 'yes',
                
                # Brokerage
                brokerage_applicable=request.POST.get('brokerage_applicable', 'No'),
                brokerage_payer=request.POST.get('brokeragePayer', ''),
                brokerage_type=request.POST.get('brokerageType', ''),
                brokerage_value=float(request.POST.get('brokerageValue') or 0),
                percentage_extra=float(request.POST.get('percentageExtra') or 0),
                brokerage_description=request.POST.get('brokerageDescription', ''),
                
                # Video & Exclusive
                exclusive_property='exclusive_property' in request.POST,
                upload_video='upload_video' in request.POST,
                video_url=request.POST.get('video_url', ''),
                video_from=request.POST.get('video_from') or None,
                video_to=request.POST.get('video_to') or None,
                video_platforms=get_checkbox_values('video_platforms[]'),
                
                # Facilities
                nearby_facilities=get_checkbox_values('nearby_facilities[]'),
                amenities=get_checkbox_values('amenities[]'),
                
                created_at=timezone.now(),
            )

        # === PG PROPERTY ===
        elif prop_category == 'pg':
            def get_checkbox_values(field_name):
                values = request.POST.getlist(field_name)
                return ','.join(values) if values else ''

            obj = PGProperty(
                posted_by=request.user if request.user.is_authenticated else None,
                lead=lead if lead else None,
                
                # Basic Details
                property_type=request.POST.get('property_type', ''),
                city=request.POST.get('city', ''),
                area_locality=request.POST.get('area_locality', ''),
                address=request.POST.get('address', ''),
                
                # PG Specific
                furnishing_type=request.POST.get('furnishing_type', ''),
                sharing_type=request.POST.get('sharing_type', ''),
                meals_included='meals_included' in request.POST,
                meal_type=request.POST.get('meal_type', ''),
                minimum_stay=int(request.POST.get('minimum_stay') or 0) if request.POST.get('minimum_stay') else None,
                available_from=request.POST.get('available_from') or None,
                
                # Rent Details
                rent_price=float(request.POST.get('rent_price') or 0),
                security_deposit=float(request.POST.get('security_deposit') or 0),
                
                # Featured & Verified
                is_featured='Yes' if request.POST.get('is_featured') == 'Yes' else 'No',
                featured_days=int(request.POST.get('featured_days') or 0) if request.POST.get('featured_days') else None,
                manual_featured_days=int(request.POST.get('manual_featured_days') or 0) if request.POST.get('manual_featured_days') else None,
                featured_start_date=request.POST.get('featured_start_date') or None,
                featured_end_date=request.POST.get('featured_end_date') or None,
                service_amount=float(request.POST.get('service_amount') or 0) if request.POST.get('service_amount') else None,
                placement=request.POST.get('placement', ''),
                is_verified='yes' if request.POST.get('is_verified') == 'yes' else 'no',
                
                # Brokerage
                brokerage_applicable=request.POST.get('brokerage_applicable', ''),
                brokeragePayer=request.POST.get('brokeragePayer', ''),
                brokerageType=request.POST.get('brokerageType', ''),
                brokerageValue=float(request.POST.get('brokerageValue') or 0) if request.POST.get('brokerageValue') else None,
                percentageExtra=float(request.POST.get('percentageExtra') or 0) if request.POST.get('percentageExtra') else None,
                brokerageDescription=request.POST.get('brokerageDescription', ''),
                
                # Video & Exclusive
                exclusive_property='exclusive_property' in request.POST,
                upload_video='upload_video' in request.POST,
                video_url=request.POST.get('video_url', ''),
                video_from=request.POST.get('video_from') or None,
                video_to=request.POST.get('video_to') or None,
                video_platforms=get_checkbox_values('video_platforms[]'),
                
                # Facilities
                nearby_facilities=request.POST.get('nearby_facilities', ''),
                amenities=request.POST.get('amenities', ''),
                
                created_at=timezone.now(),
            )

        else:
            messages.error(request, "⚠️ Invalid property category selected.")
            return redirect('property_view_report')

        # File uploads for all property types
        file_fields = ['property_images', 'floor_plan', 'upload_registry', 'upload_house_tax',
                      'upload_utility_bill', 'upload_aadhar', 'upload_pan', 'upload_index2']
        
        for field in file_fields:
            if field in request.FILES:
                setattr(obj, field, request.FILES.get(field))

        obj.save()
        messages.success(request, f"✅ {prop_category.capitalize()} property posted successfully!")

    except Exception as e:
        messages.error(request, f"❌ Error while saving property: {str(e)}")
        import traceback
        print(traceback.format_exc())  # For debugging
        return redirect('post_property')

    return redirect('index')

# ---------------- PROPERTY REPORT ----------------
@login_required
def property_view_report(request):
    res = ResidentialProperty.objects.filter(posted_by=request.user)
    com = CommercialProperty.objects.filter(posted_by=request.user)
    pg = PGProperty.objects.filter(posted_by=request.user)
    return render(request, 'home_page/property_view_report.html', {
        'residentials': res,
        'commercials': com,
        'pgs': pg,
    })







import random





from django.shortcuts import render
from django.db.models import Q
from itertools import chain
from datetime import datetime, timedelta
import random



def get_featured_queryset(model):
    return model.objects.filter(
       
    ).order_by('-created_at')[:6]


def index(request):
    hero = HeroSection.objects.filter(is_active=True).first()
    blogs = Blog.objects.all().order_by("-date_posted")
    faqs = FAQ.objects.all().order_by('-created_at')

    # ✅ CORRECT FUNCTION CALL
    residential = list(get_featured_queryset(ResidentialProperty))
    commercial = list(get_featured_queryset(CommercialProperty))
    pg = list(get_featured_queryset(PGProperty))

    # Combine
    all_props = (
        [{"data": prop, "type": "Residential"} for prop in residential] +
        [{"data": prop, "type": "Commercial"} for prop in commercial] +
        [{"data": prop, "type": "PG"} for prop in pg]
    )

    random.shuffle(all_props)
    featured_props = all_props[:6]

    props = sorted(
        chain(residential, commercial, pg),
        key=lambda x: getattr(x, 'created_at', None),
        reverse=True
    )

    context = {
        "featured_props": featured_props,
        "props": props,
        "hero": hero,
        "blogs": blogs,
        "faqs": faqs,
    }

    return render(request, "home_page/index.html", context)


def blog_details(request, key):
    seo = get_object_or_404(LocationSEO, key=key, pagetype="blog", is_active=True)
    blog = seo.content_object

    return render(request, "home_page/blog_details.html", {"seo": seo, "blog": blog})



def property_details(request):
    return render(request,"home_page/property_details.html")

def agent_profile(request):
    return render(request,"home_page/agent_profile.html")


def com(request):
    return render(request,"home_page/com.html")






def property_detail_page(request, key):
    # Fetch SEO record
    seo = get_object_or_404(LocationSEO, key=key, is_active=True)
    prop = seo.content_object

    # Detect property type
    model_name = seo.content_type.model
    if model_name == "residentialproperty":
        InquiryModel = ResidentialInquiry
        fk_field = "residential_property"
    elif model_name == "commercialproperty":
        InquiryModel = CommercialInquiry
        fk_field = "commercial_property"
    else:
        InquiryModel = PGInquiry
        fk_field = "pg_property"

    # Handle inquiry form
    if request.method == "POST":
        if not request.user.is_authenticated:
            messages.error(request, "Please log in to submit an inquiry.")
            return redirect("login")

        InquiryModel.objects.create(
            **{fk_field: prop},
            name=request.POST.get("name"),
            email=request.POST.get("email"),
            phone=request.POST.get("phone"),
            message=request.POST.get("message"),
        )
        messages.success(request, "Inquiry submitted successfully!")

    # Amenities & nearby
    amenities = [a.strip() for a in (getattr(prop, "amenities", "") or "").split(",") if a.strip()]
    nearby_facilities = [f.strip() for f in (getattr(prop, "nearby_facilities", "") or "").split(",") if f.strip()]

    related_props = prop.__class__.objects.filter(city=prop.city).exclude(id=prop.id)[:4]

    context = {
        "seo": seo,
        "property": prop,
        "amenities": amenities,
        "nearby_facilities": nearby_facilities,
        "related_props": related_props,
    }
    return render(request, "home_page/property_detail_page.html", context)




def properties(request):
    query = request.GET.get('q', '').strip()
    prop_type = request.GET.get('type', '').strip()

    today = date.today()
    fifteen_days_ago = today - timedelta(days=15)

    def attach_seo(props):
        ctype = ContentType.objects.get_for_model(props.model)
        seo_map = {
            s.object_id: s for s in LocationSEO.objects.filter(content_type=ctype, is_active=True)
        }
        for p in props:
            p.locationseo = seo_map.get(p.id)
        return props

    if prop_type == 'residential':
        base_qs = ResidentialProperty.objects.all()
        if query:
            base_qs = base_qs.filter(
                Q(property_title__icontains=query) |
                Q(city__icontains=query) |
                Q(area__icontains=query) |
                Q(property_address__icontains=query)
            )
        residential_props = attach_seo(base_qs.order_by('-created_at'))
        commercial_props = pg_props = []

    elif prop_type == 'commercial':
        base_qs = CommercialProperty.objects.all()
        if query:
            base_qs = base_qs.filter(
                Q(property_type__icontains=query) |
                Q(city__icontains=query) |
                Q(area_locality__icontains=query) |
                Q(property_address__icontains=query)
            )
        commercial_props = attach_seo(base_qs.order_by('-created_at'))
        residential_props = pg_props = []

    elif prop_type == 'pg':
        base_qs = PGProperty.objects.all()
        if query:
            base_qs = base_qs.filter(
                Q(property_type__icontains=query) |
                Q(city__icontains=query) |
                Q(area_locality__icontains=query) |
                Q(address__icontains=query)
            )
        pg_props = attach_seo(base_qs.order_by('-created_at'))
        residential_props = commercial_props = []

    else:
        residential_props = attach_seo(ResidentialProperty.objects.all().order_by('-created_at'))
        commercial_props = attach_seo(CommercialProperty.objects.all().order_by('-created_at'))
        pg_props = attach_seo(PGProperty.objects.all().order_by('-created_at'))

    context = {
        "residential_props": residential_props,
        "commercial_props": commercial_props,
        "pg_props": pg_props,
        "query": query,
        "prop_type": prop_type,
        "today": today,
        "fifteen_days_ago": fifteen_days_ago,
    }
    return render(request, "home_page/properties.html", context)


def services(request):
    services = LocationSEO.objects.filter(pagetype="service", is_active=True)
    return render(request, "home_page/services.html", {"services": services})



def services_details(request, key):
    seo = get_object_or_404(LocationSEO, key=key, pagetype="service", is_active=True)
    service = seo.content_object
    return render(request, "home_page/services_details.html", {"seo": seo, "service": service})


def agents(request):
    return render(request,"home_page/agents.html")

def complaint_form(request):
    return render(request,"home_page/complaint_form.html")

def rm_portal(request):
    return render(request,"home_page/rm_portal.html")


def blog(request):
    seo_pages = LocationSEO.objects.filter(is_active=True, pagetype="blog")
    
    context = {
        "blogs": seo_pages,
    }
    return render(request, "home_page/blog.html", context)



def about(request):
   
    about = AboutPage.objects.first()
    timeline_items = TimelineItem.objects.all
    achievements = Achievement.objects.all()# fetch the first record
    return render(request, "home_page/about.html", {"about": about,"achievements": achievements, "timeline_items" : timeline_items,})
   

def contact(request):
    return render(request,"home_page/contact.html")




def renewal(request):
    return render(request,"home_page/renewal.html")




#def residential(request):
  #  return render(request,"home_page/residential.html")


def commercial(request):
    return render(request,"home_page/commercial.html")


def residential_property(request):
    return render(request,"home_page/residential_property.html")

def pg_coliving(request):
    return render(request,"home_page/pg_coliving.html")








# -------------------
# Registration
# -------------------


# -------------------
# Login
# -------------------



# -------------------
# Logout

 

# -------------------------------
# 🔹 LEAD CAPTURE VIEW
# -------------------------------









# -------------------
# PG / Co-living Property Posting
# -------------------


# -------------------
# Property Detail Page + Inquiry
# -------------------

















def property_listing(request):
    query = request.GET.get('q', '').strip()
    prop_type = request.GET.get('type', '').strip()

    residential_props = commercial_props = pg_props = []

    if prop_type == 'residential':
        residential_props = ResidentialProperty.objects.filter(
            Q(property_title__icontains=query) |
            Q(city__icontains=query) |
            Q(area__icontains=query) |
            Q(property_address__icontains=query)
        ) if query else ResidentialProperty.objects.all()

    elif prop_type == 'commercial':
        commercial_props = CommercialProperty.objects.filter(
            Q(property_type__icontains=query) |
            Q(city__icontains=query) |
            Q(area_locality__icontains=query) |
            Q(property_address__icontains=query)
        ) if query else CommercialProperty.objects.all()

    elif prop_type == 'pg':
        pg_props = PGProperty.objects.filter(
            Q(property_type__icontains=query) |
            Q(city__icontains=query) |
            Q(area_locality__icontains=query) |
            Q(address__icontains=query)
        ) if query else PGProperty.objects.all()

    else:
        residential_props = ResidentialProperty.objects.all()
        commercial_props = CommercialProperty.objects.all()
        pg_props = PGProperty.objects.all()

    context = {
        "residential_props": residential_props,
        "commercial_props": commercial_props,
        "pg_props": pg_props,
        "query": query,
        "prop_type": prop_type,
    }
    return render(request, "home_page/property_listing.html", context)

    






# -------------------
# User Dashboard (to see own properties + inquiries)
# -------------------











def admin_dashboard(request):
    # Admin can see all properties
    residential_props = ResidentialProperty.objects.all()
    commercial_props = CommercialProperty.objects.all()
    pg_props = PGProperty.objects.all()

    # Get all inquiries for each property type
    residential_inquiries = ResidentialInquiry.objects.filter(residential_property__in=residential_props)
    commercial_inquiries = CommercialInquiry.objects.filter(commercial_property__in=commercial_props)
    pg_inquiries = PGInquiry.objects.filter(pg_property__in=pg_props)

    # Prepare inquiry data
    def prepare_inquiry_data(inquiries, fk_field):
        data = []
        for inquiry in inquiries:
            prop = getattr(inquiry, fk_field)
            owner = prop.posted_by
            data.append({
                "property_id": prop.id,
                "property_title": getattr(prop, "property_title", "N/A"),
                "property_owner_name": getattr(owner, "full_name", owner.username),
                "property_owner_role": getattr(owner, "role", "N/A"),
                "inquiry_name": getattr(inquiry, "name", "N/A"),
                "inquiry_email": getattr(inquiry, "email", "N/A"),
                "inquiry_phone": getattr(inquiry, "phone", "N/A"),
                "inquiry_message": getattr(inquiry, "message", "N/A"),
                "lead_age": getattr(inquiry, "lead_age", "N/A"),
            })
        return data

    context = {
        "residential_inquiries": prepare_inquiry_data(residential_inquiries, "residential_property"),
        "commercial_inquiries": prepare_inquiry_data(commercial_inquiries, "commercial_property"),
        "pg_inquiries": prepare_inquiry_data(pg_inquiries, "pg_property"),
        "residential_props": residential_props,
        "commercial_props": commercial_props,
        "pg_props": pg_props,
    }

    return render(request, "home_page/admin_dashboard.html", context)




def blog_list(request):
    blogs = Blog.objects.all().order_by("-created_at")
    return render(request, "home_page/blog_list.html", {"blogs": blogs})

#def blog_detail(request, slug):
   # blog = get_object_or_404(Blog, slug=slug)
    #return render(request, "home_page/blog_detail.html", {"blog": blog})


def category_list(request):
    if request.method == "POST":
        name = request.POST.get("name")
        if name:  # only add if not empty
            BlogCategory.objects.get_or_create(name=name)
        return redirect("category_list")

    categories = BlogCategory.objects.all().order_by("name")
    return render(request, "home_page/category_list.html", {"categories": categories})






def create_blog(request):
    categories = BlogCategory.objects.all()

    if request.method == "POST":
        try:
            blog = Blog.objects.create(
                title=request.POST.get('title'),
                description=request.POST.get('description'),
                content=request.POST.get('content'),
                author=request.POST.get('author'),
                primary_keyword=request.POST.get('primary_keyword'),
                secondary_keywords=request.POST.get('secondary_keywords'),
                img_position=request.POST.get('img_position'),
                featured_image=request.FILES.get('featured_image')
            )

            # Set selected categories
            selected_categories = request.POST.getlist('categories')
            if not selected_categories:
                messages.error(request, "Please select at least one category.")
                return render(request, "home_page/blog_create.html", {"categories": categories})

            blog.categories.set(selected_categories)
            blog.save()

            messages.success(request, "Blog created successfully!")
            return redirect("blog_list")

        except Exception as e:
            messages.error(request, f"Error while saving blog: {str(e)}")
            print("ERROR >>>", str(e))

    return render(request, "home_page/blog_create.html", {"categories": categories})






def landing_page(request, slug):
    page = get_object_or_404(LandingPage, slug=slug)
    seo = SeoMeta.objects.filter(object_id=page.id, content_type__model="landingpage").first()
    return render(request, "home_page/landing_page.html", {"page": page, "seo": seo})










def property_detail(request, pk, slug):
    prop = get_object_or_404(Page, pk=pk)
    seo = SeoMeta.objects.filter(object_id=prop.id, content_type__model="residentialproperty").first()
    return render(request, "home_page/detail.html", {"property": prop, "seo": seo})



def seo_page(request, slug):
    seo = get_object_or_404(SeoMeta, slug=slug, noindex=False)
    return render(request, "seo/seo_page.html", {"seo": seo, "content": seo.content_object})






def add(request):
  
    
    seo_pages = LocationSEO.objects.filter(is_active=True, pagetype="ad")
    
    context = {
        "ads": seo_pages,
    }
    return render(request, "home_page/add.html",context)






def add_details(request, key):
    seo = get_object_or_404(LocationSEO, key=key, pagetype="ad", is_active=True)
    ad = seo.content_object

    return render(request, "home_page/add_details.html", {"seo": seo, "ad": ad})







def addon_list(request):
    addons = Addon.objects.filter(isactive=True)
    return render(request, 'home_page/addon_list.html', {'addons': addons})


# --- Add-On Landing / SEO Page ---
def addon_landing(request, slug):
    addon = get_object_or_404(Addon, slug=slug)
    seo_data = LocationSEO.objects.filter(
        content_type__model='addon', object_id=addon.id
    ).first()
    return render(request, 'home_page/addon_landing.html', {
        'addon': addon,
        'seo': seo_data
    })
    
    
    
    

# views.py





def property_faq_view(request, type, id):

    if type == "residential":
        property_obj = get_object_or_404(ResidentialProperty, id=id)
        faq_list = PropertyFAQ.objects.filter(residential=property_obj)

    elif type == "commercial":
        property_obj = get_object_or_404(CommercialProperty, id=id)
        faq_list = PropertyFAQ.objects.filter(commercial=property_obj)

    elif type == "pg":
        property_obj = get_object_or_404(PGProperty, id=id)
        faq_list = PropertyFAQ.objects.filter(pg=property_obj)

    else:
        return HttpResponse("Invalid property type")

    return render(request, "home_page/property_faq.html", {
        "property": property_obj,
        "faq_list": faq_list,
        "type": type.capitalize(),
    })




def all_faqs(request):
    from Main_App.models import PropertyFAQ
    faqs = PropertyFAQ.objects.all().order_by('-created_at')

    return render(request, "home_page/all_faqs.html", {
        "faqs": faqs
    })
    
    
    

# --- Ad Creation ---
def create_ad(request):
    if request.method == "POST":
        title = request.POST.get("title")
        description = request.POST.get("description")
        business_name = request.POST.get("business_name")
        contact_url = request.POST.get("contact_url")
        placement = request.POST.get("placement")
        start_date = request.POST.get("start_date")
        end_date = request.POST.get("end_date")
        image = request.FILES.get("image")

        ad = SponsoredAd.objects.create(
            title=title,
            description=description,
            business_name=business_name,
            contact_url=contact_url,
            placement=placement,
            start_date=start_date,
            end_date=end_date,
            image=image,
          #  created_by=request.user if request.user.is_authenticated else None,
            active=True,
        )

        return redirect("index")

    return render(request, "home_page/create_ad.html")


# --- List Ads ---
def sponsored_ad_list_view(request):
    ads = SponsoredAd.objects.all().order_by("-created_at")
    return render(request, "home_page/list_ads.html", {"ads": ads})


def sponsored_ad_detail_view(request, slug):
    ad = get_object_or_404(SponsoredAd, slug=slug)
    seo_page = get_object_or_404(LocationSEO, content_type__model="sponsoredad", object_id=ad.id)
    return render(request, "home_page/ad_detail.html", {"ad": ad, "seo": seo_page})



#######################Start View Section For Rental Listing#################################


def rent_residential(request):
    ameneties_obj = Ameneties_Details.objects.all()
    facilities_obj = Facilities_Details.objects.all()

    context = {'ameneties_obj':ameneties_obj,'facilities_obj':facilities_obj}
    return render(request, "Listing_Form/Rental_Property/rent_residential.html",context)



def rent_commercial(request):
    ameneties_obj = Ameneties_Details.objects.all()
    facilities_obj = Facilities_Details.objects.all()

    context = {'ameneties_obj':ameneties_obj,'facilities_obj':facilities_obj}

    return render(request, "Listing_Form/Rental_Property/rent_commercial.html",context)

def rent_pg_coliving(request):
    ameneties_obj = Ameneties_Details.objects.all()
    facilities_obj = Facilities_Details.objects.all()

    context = {'ameneties_obj':ameneties_obj,'facilities_obj':facilities_obj}

    return render(request, "Listing_Form/Rental_Property/rent_pg_coliving.html",context)


#######################End View Section For Rental Listing#################################



#######################Start View Section For Resale Listing#################################


def residential_resale_form(request):
    ameneties_obj = Ameneties_Details.objects.all()
    facilities_obj = Facilities_Details.objects.all()

    context = {'ameneties_obj':ameneties_obj,'facilities_obj':facilities_obj}

    return render(request, "Listing_Form/Resale_Property/residential_resale_form.html",context)



def resale_commercial_form(request):
    ameneties_obj = Ameneties_Details.objects.all()
    facilities_obj = Facilities_Details.objects.all()

    context = {'ameneties_obj':ameneties_obj,'facilities_obj':facilities_obj}

    return render(request, "Listing_Form/Resale_Property/resale_commercial_form.html",context)

def resale_agricultural_form(request):

    return render(request, "Listing_Form/Resale_Property/resale_agricultural_form.html")


def resale_plot_form(request):

    return render(request, "Listing_Form/Resale_Property/resale_plot_form.html")

def resale_industrial_form(request):

    return render(request, "Listing_Form/Resale_Property/resale_industrial_form.html")


#######################End View Section For Resale Listing#################################