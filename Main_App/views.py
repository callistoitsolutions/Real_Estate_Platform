
# Create your views here.
from django.shortcuts import render
from django.contrib import messages
from django.shortcuts import render,redirect,HttpResponse
from Main_App .models import *
from Admin_App .models import *
from django.views.decorators.http import require_POST
from CRM_Panel .models import *
from seo .models import *
from django.db.models import Q
# rental_app/views.py
import json
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
import random

from django.shortcuts import render
from django.db.models import Q
from itertools import chain
from datetime import datetime, timedelta
import random
from django.shortcuts import render
from django.db.models import Q
import re
from rapidfuzz import process, fuzz
from .apps import MainAppConfig


########### Crime Officer Views#######


from itertools import chain



from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.forms.models import model_to_dict
import json
from .apps import MainAppConfig
from datetime import datetime







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





def _normalize_rental(p):
    """Normalize rental residential property"""

    image_url = ""

    first_image = p.images.first()
    if first_image and first_image.image:
        image_url = first_image.image.url

    return {
        'id': p.id,

        'title': (
            f"{p.bhk_type} in {p.locality}"
            if p.bhk_type
            else (p.property_type or "Residential Property")
        ),

        # ✅ Correct field
        #  Correct field
        'price_display': f"₹{p.monthly_rent or 0}",

        'location': f"{p.locality}, {p.city}",

        'beds': p.bhk_type or "—",

        'baths': p.bathrooms or "—",

        'area': f"{p.carpet_area or '—'} sq.ft",

        'floor': p.floor_number or "—",



        'listing_type': 'rent',

        'category': 'residential',

        'owner': p.owner_name or "Owner",

        'owner_role': "Property Owner",

        'owner_initials': (
            p.owner_name[:2].upper()
            if p.owner_name else "OW"
        ),

        'phone': p.contact_number or "",

        'image_url': image_url,

        'is_new': True,

        'is_ai_match': True,
    }


def _normalize_commercial_rental(p):
    """Normalize commercial rental property - COMPLETE FIX"""
    
    # Get first image
    image_url = ""
    try:
        first_image = p.images.first()
        if first_image and hasattr(first_image, 'image') and first_image.image:
            image_url = first_image.image.url
    except:
        pass

    # Build title
    property_type = getattr(p, 'property_type', None) or 'Commercial Space'
    locality = getattr(p, 'locality', None)
    
    if locality:
        title = f"{property_type} in {locality}"
    else:
        title = property_type

    return {
        'id': p.id,
        'title': title,
        'price_display': f"₹{getattr(p, 'expected_rent', None) or 0}",
        'location': f"{getattr(p, 'locality', 'Unknown')}, {getattr(p, 'city', 'City')}",
        'beds': "—",
        'baths': "—",
        'area': f"{getattr(p, 'carpet_area', None) or '—'} sq.ft",
        'floor': f"{getattr(p, 'floor_number', None) or '—'}",
        'furnished': getattr(p, 'furnishing', None) or "Not Specified",
        'property_type': property_type,
        'listing_type': 'rent',
        'category': 'commercial',
        'owner': getattr(p, 'owner_name', None) or "Owner",
        'owner_role': "Property Owner",
        'owner_initials': (
            getattr(p, 'owner_name', 'OW')[:2].upper()
            if getattr(p, 'owner_name', None)
            else "OW"
        ),
        'phone': getattr(p, 'contact_number', ""),
        'image_url': image_url,
        'is_new': True,
        'is_ai_match': True,
    }



def _normalize_pg(p):
    """Normalize PG/Co-living property - FIXED"""
    room_price = "0"

    if hasattr(p, 'room_details') and p.room_details:
        try:
            rooms = json.loads(p.room_details)
            if rooms and isinstance(rooms, list):
                first_room = rooms[0]
                room_price = (
                    first_room.get('price')
                    or first_room.get('rent')
                    or first_room.get('monthly_rent')
                    or "0"
                )
        except Exception:
            room_price = "0"

    # Fixed: Check for different possible rent field names
    if room_price == "0":
        if hasattr(p, 'monthly_rent'):
            room_price = str(p.monthly_rent or 0)
        elif hasattr(p, 'expected_rent'):
            room_price = str(p.expected_rent or 0)
        elif hasattr(p, 'price'):
            room_price = str(p.price or 0)

    image_url = ""
    first_image = p.images.first()
    if first_image and first_image.image:
        image_url = first_image.image.url

    return {
        'id': p.id,
        'title': p.pg_name or "PG / Co-Living",
        'price_display': f"₹{room_price}",
        'location': f"{p.locality}, {p.city}",
        'beds': p.total_beds if hasattr(p, 'total_beds') else "—",
        'baths': "—",
        'area': "PG / Co-Living",
        'floor': "—",
        'furnished': p.furnishing_type or "Furnished" if hasattr(p, 'furnishing_type') else "Furnished",
        'property_type': "PG",
        'listing_type': 'rent',
        'category': 'pg',
        'owner': p.owner_name or "PG Owner",
        'owner_role': "PG Owner",
        'owner_initials': p.owner_name[:2].upper() if p.owner_name else "PG",
        'phone': p.contact_number or "",
        'image_url': image_url,
        'is_new': True,
        'is_ai_match': True,
    }


def _normalize_resale(p):
    """Normalize resale residential property"""

    image_url = ""

    first_image = p.images.first() if hasattr(p, 'images') else None

    if first_image and first_image.image:
        image_url = first_image.image.url

    return {
        'id': p.id,

        'title': f"{p.bhk} in {p.locality}" if p.bhk else (
            p.property_type or "Residential Property"
        ),

        'price_display': f"₹{p.expected_price or 0}",

        'location': f"{p.locality}, {p.city}",

        'beds': p.bhk or "—",

        'baths': p.bathrooms or "—",

        'area': f"{p.carpet_area or '—'} sq.ft",

        'floor': f"{p.floor_no or '—'}",

        'furnished': p.furnishing_type or "Not Specified",

        'property_type': p.property_type or "Residential",

        'listing_type': 'sale',

        'category': 'residential',

        'owner': p.owner_name or "Owner",

        'owner_role': "Property Owner",

        'owner_initials': (
            p.owner_name[:2].upper()
            if p.owner_name else "OW"
        ),

        'phone': p.owner_contact or "",

        'image_url': image_url,

        'is_new': True,

        'is_ai_match': True,
    }





def _normalize_commercial_resale(p):
    """Normalize commercial resale property"""
    image_url = ""
    first_image = p.images.first()
    if first_image and first_image.image:
        image_url = first_image.image.url

    title = p.property_type or 'Commercial Space'
    if hasattr(p, 'locality') and p.locality:
        title = f"{title} in {p.locality}"

    return {
        'id': p.id,
        'title': title,
        'price_display': f"₹{p.expected_price or 0}",
        'location': f"{p.locality}, {p.city}" if hasattr(p, 'locality') else p.city or "—",
        'beds': "—",
        'baths': "—",
        'area': f"{p.carpet_area or '—'} sq.ft" if hasattr(p, 'carpet_area') else "—",
        'floor': f"{p.floor_number or '—'}" if hasattr(p, 'floor_number') else "—",
        'furnished': p.furnishing or "Not Specified" if hasattr(p, 'furnishing') else "—",
        'property_type': p.property_type or "Commercial",
        'listing_type': 'sale',
        'category': 'commercial',
        'owner': p.owner_name or "Owner",
        'owner_role': "Property Owner",
        'owner_initials': p.owner_name[:2].upper() if p.owner_name else "OW",
        'phone': p.owner_contact or "",  # <-- Fixed here
        'image_url': image_url,
        'is_new': True,
        'is_ai_match': True,
    }




def _normalize_plot(p):
    """Normalize plot property"""
    image_url = ""
    first_image = p.images.first()
    if first_image and first_image.image:
        image_url = first_image.image.url

    return {
        'id': p.id,
        'title': f"Plot in {p.locality}" if hasattr(p, 'locality') and p.locality else "Plot for Sale",
        'price_display': f"₹{p.plot_price or 0}",
        'location': f"{p.locality}, {p.city}" if hasattr(p, 'locality') else p.plot_city or "—",
        'beds': "—",
        'baths': "—",
        'area': f"{p.plot_area or '—'} sq.ft" if hasattr(p, 'plot_area') else "—",
        'floor': "—",
        'furnished': "—",
        'property_type': "Plot",
        'listing_type': 'sale',
        'category': 'plot',
        'owner': p.plot_owner_name or "Owner",
        'owner_role': "Plot Owner",
        'owner_initials': p.plot_owner_name[:2].upper() if p.plot_owner_name else "OW",
        'phone': p.plot_owner_contact or "",
        'image_url': image_url,
        'is_new': True,
        'is_ai_match': True,
    }


def _normalize_industrial(p):
    """Normalize industrial property"""
    image_url = ""
    first_image = p.images.first()
    if first_image and first_image.image:
        image_url = first_image.image.url

    return {
        'id': p.id,
        'title': f"Industrial Property in {p.locality}" if hasattr(p, 'locality') and p.locality else "Industrial Property",
        'price_display': f"₹{p.expected_price or 0}",
        'location': f"{p.locality}, {p.city}" if hasattr(p, 'locality') else p.city or "—",
        'beds': "—",
        'baths': "—",
        'area': f"{p.plot_area or '—'} sq.ft" if hasattr(p, 'plot_area') else "—",
        'floor': "—",
        'furnished': "—",
        'property_type': "Industrial",
        'listing_type': 'sale',
        'category': 'industrial',
        'owner': p.owner_name or "Owner",
        'owner_role': "Property Owner",
        'owner_initials': p.owner_name[:2].upper() if p.owner_name else "OW",
        'phone': p.owner_contact or "",
        'image_url': image_url,
        'is_new': True,
        'is_ai_match': True,
    }


def _normalize_agriculture(p):
    """Normalize agricultural property"""
    image_url = ""
    first_image = p.images.first()
    if first_image and first_image.image:
        image_url = first_image.image.url

    return {
        'id': p.id,
        'title': f"Agricultural Land in {p.locality}" if hasattr(p, 'locality') and p.locality else "Agricultural Land",
        'price_display': f"₹{p.expected_price or 0}",
        'location': f"{p.locality}, {p.city}" if hasattr(p, 'locality') else p.city or "—",
        'beds': "—",
        'baths': "—",
        'area': f"{p.plot_area or '—'} sq.ft" if hasattr(p, 'plot_area') else "—",
        'floor': "—",
        'furnished': "—",
        'property_type': "Agricultural",
        'listing_type': 'sale',
        'category': 'agriculture',
        'owner': p.owner_name or "Owner",
        'owner_role': "Land Owner",
        'owner_initials': p.owner_name[:2].upper() if p.owner_name else "OW",
        'phone': p.owner_contact or "",
        'image_url': image_url,
        'is_new': True,
        'is_ai_match': True,
    }




# =========================================================
# ACTIVE USER SUBSCRIPTION
# =========================================================




# =========================================================
# PROPERTY DETAIL VIEW
# =========================================================






# =====================================================
# SAVE ENQUIRY
# =====================================================

def save_property_enquiry(request):

    if request.method == "POST":

        PropertyEnquiry.objects.create(

            # USER
            name=request.POST.get("name"),
            phone=request.POST.get("phone"),
            email=request.POST.get("email"),
            message=request.POST.get("message"),

            # PROPERTY
            property_id=request.POST.get("property_id"),
            property_title=request.POST.get("property_title"),
            property_type=request.POST.get("property_type"),
            property_location=request.POST.get("property_location"),
            property_price=request.POST.get("property_price"),

            # TRACKING
            lead_source=request.POST.get("lead_source"),
            seo_slug=request.POST.get("seo_slug"),
            page_url=request.POST.get("page_url"),

            # USER INFO
            user_ip=get_client_ip(request),
            user_device=request.META.get("HTTP_USER_AGENT"),
            referrer_url=request.META.get("HTTP_REFERER"),

        )

        messages.success(

            request,
            "Enquiry sent successfully."

        )

        return redirect(request.META.get("HTTP_REFERER"))

    return redirect("/")


# =====================================================
# CLIENT IP
# =====================================================

def get_client_ip(request):

    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")

    if x_forwarded_for:

        ip = x_forwarded_for.split(",")[0]

    else:

        ip = request.META.get("REMOTE_ADDR")

    return ip


# =====================================================
# ENQUIRY REPORT PAGE
# =====================================================

def enquiry_report(request):

    enquiries = PropertyEnquiry.objects.all().order_by("-id")

    total_enquiries = enquiries.count()

    new_enquiries = enquiries.filter(
        enquiry_status="New"
    ).count()

    closed_enquiries = enquiries.filter(
        enquiry_status="Closed"
    ).count()

    context = {

        "enquiries": enquiries,

        "total_enquiries": total_enquiries,

        "new_enquiries": new_enquiries,

        "closed_enquiries": closed_enquiries,

    }

    return render(

        request,
        "home_page/enquiry_report.html",
        context

    )





import math
# =====================================================
# PROPERTY DETAIL VIEW
# =====================================================







########### Views start for ajax for send property enquiry ########################



from django.contrib.contenttypes.models import ContentType


@csrf_exempt
def Send_Property_Enquiry(request):
    if request.method != "POST":
        return JsonResponse({"status": "0", "msg": "Invalid request method."})

    data = request.POST.dict()   
    property_id = data.get('property_id')
    listing_type = data.get('listing_type', '').lower()
    category = data.get('category', '').lower()
    
    real_property = None

    # 1. Fetch Property
    try:
        if listing_type == "rent":
            if "residential" in category:
                real_property = RentalResidentialProperty.objects.get(id=property_id)
            elif "pg" in category:
                real_property = PGColivingProperty.objects.get(id=property_id)
            elif "commercial" in category:
                real_property = CommercialRentalProperty.objects.get(id=property_id)
        
        elif listing_type == "sale":
            if "residential" in category:
                real_property = ResaleResidentialProperty.objects.get(id=property_id)
            elif "commercial" in category:
                real_property = CommercialResaleProperty.objects.get(id=property_id)
            elif "plot" in category:
                real_property = PlotSaleProperty.objects.get(id=property_id)
            elif "industrial" in category:
                real_property = IndustrialResaleProperty.objects.get(id=property_id)
            elif "agriculture" in category:
                real_property = AgriculturalResaleProperty.objects.get(id=property_id)
    except Exception as e:
        return JsonResponse({"status": "0", "msg": f"Property not found: {str(e)}"})

    if not real_property:
        return JsonResponse({"status": "0", "msg": "Invalid property type or category."})

    # 2. Get User
    user_id = data.get('user_id')
    user_data = User_Details.objects.filter(id=user_id).first() if (user_id and user_id.strip()) else None

    # 3. Create Enquiry using ContentType
    try:
        # Get ContentType for the real_property model
        c_type = ContentType.objects.get_for_model(real_property)
        
        enquiry = PropertyEnquiry.objects.create(
            user=user_data,
            enquiry_name=data.get('enquiry_name'),
            enquiry_phone=data.get('enquiry_phone'),
            enquiry_email=data.get('enquiry_email'),
            enquiry_message=data.get('enquiry_message'),
            enquiry_date=date.today(),
            enquiry_time=datetime.now().time(),
            # Explicitly set the fields that were missing
            content_type=c_type,
            object_id=real_property.id
        )
        
        return JsonResponse({"status": "1", "msg": "Enquiry submitted successfully!"})
    
    except Exception as e:
        return JsonResponse({"status": "0", "msg": f"Error saving enquiry: {str(e)}"})
    

########### Views end for ajax for send property enquiry ######################







def subscription_plans(request):

    subscriptions = Subscription_Details.objects.filter(
        is_active=True
    ).order_by('plan_offer_price')

    context = {
        'subscriptions': subscriptions
    }

    return render(
        request,
        'home_page/subscription_plans.html',
        context
    )

def subscription_checkout(request, plan_id):

    plan = get_object_or_404(
        Subscription_Details,
        id=plan_id
    )

    context = {
        'plan': plan
    }

    return render(
        request,
        'home_page/subscription_checkout.html',
        context
    )
# =========================================================
# REVEAL PHONE
# =========================================================

@login_required
def reveal_phone(request, property_id):

    user_id = request.session.get('user_id')

    logged_user = User_Details.objects.filter(
        id=user_id
    ).first()

    if not logged_user:

        return JsonResponse({
            'success': False,
            'error': 'User not found.'
        })

    # =====================================================
    # PROPERTY FIND
    # =====================================================

    property_obj = None

    models_list = [

        RentalResidentialProperty,
        CommercialRentalProperty,
        PGColivingProperty,

        ResaleResidentialProperty,
        CommercialResaleProperty,
        PlotSaleProperty,
        IndustrialResaleProperty,
        AgriculturalResaleProperty,
    ]

    for model in models_list:

        try:

            property_obj = model.objects.get(id=property_id)
            break

        except:

            pass

    if not property_obj:

        return JsonResponse({
            'success': False,
            'error': 'Property not found.'
        })

    return _build_reveal_response(
        property_obj,
        logged_user,
        deduct=False
    )


# =========================================================
# INTERNAL RESPONSE
# =========================================================

def _build_reveal_response(property_obj, logged_user, deduct=False):

    owner_name = getattr(
        property_obj,
        'owner_name',
        'Owner'
    )

    owner_phone = getattr(
        property_obj,
        'phone',
        ''
    )

    user_subscription = get_active_subscription(logged_user)

    if user_subscription:

        if deduct:

            user_subscription.used_contacts += 1
            user_subscription.remaining_contacts -= 1

            if user_subscription.remaining_contacts <= 0:

                user_subscription.is_active = False

            user_subscription.save()

        return JsonResponse({

            'success': True,
            'phone_revealed': True,

            'owner_phone': owner_phone,

            'masked_phone':
                _mask_phone(owner_phone),

            'owner_name': owner_name,

            'contacts_remaining':
                user_subscription.remaining_contacts,
        })

    else:

        return JsonResponse({

            'success': True,
            'phone_revealed': False,

            'owner_phone': None,

            'masked_phone':
                _mask_phone(owner_phone),

            'owner_name': owner_name,

            'contacts_remaining': 0,
        })


# =========================================================
# MASK PHONE
# =========================================================

def _mask_phone(phone):

    if not phone:

        return '***** *****'

    phone = str(phone).strip()

    if len(phone) >= 10:

        return (
            phone[:2]
            + '*' * (len(phone) - 4)
            + phone[-2:]
        )

    return '***' + phone[-2:]


# =========================================================
# CLIENT IP
# =========================================================

def _get_client_ip(request):

    x_forwarded = request.META.get(
        'HTTP_X_FORWARDED_FOR'
    )

    if x_forwarded:

        return x_forwarded.split(',')[0].strip()

    return request.META.get(
        'REMOTE_ADDR',
        ''
    )













# ═══════════════════════════════════════════════════════════════════════
# 1. AI HELPER FUNCTIONS (Must be defined BEFORE listings_view)
# ═══════════════════════════════════════════════════════════════════════
def correct_query_text(query):
    query = query.lower().strip()
    query = re.sub(r'[^\w\s]', '', query) # Remove punctuation
    return query

def apply_fuzzy_correction(query):
    words = query.split()
    corrected_words = []
    
    valid_keywords = []
    # Check if cities loaded successfully in apps.py
    if hasattr(MainAppConfig, 'cities') and MainAppConfig.cities:
        valid_keywords = MainAppConfig.cities
        
    for word in words:
        if valid_keywords:
            match = process.extractOne(word, valid_keywords, scorer=fuzz.ratio)
            if match and match[1] > 80: # 80% similarity threshold
                corrected_words.append(match[0])
            else:
                corrected_words.append(word)
        else:
            corrected_words.append(word)
            
    return " ".join(corrected_words)

def extract_entities(query):
    # Sends the fuzzy-corrected text straight to the Sentence Transformer
    return query




def _normalize_any_property(obj, source):
    """Bridges all 8 models to the same HTML card layout"""
    
    # 1. Image Logic
    img_url = None
    if hasattr(obj, 'images') and obj.images.exists():
        img_url = obj.images.first().image.url
    elif hasattr(obj, 'property_image') and obj.property_image:
        img_url = obj.property_image.url
    elif hasattr(obj, 'floor_plan') and obj.floor_plan:
        img_url = obj.floor_plan.url # Fallback for commercial/pg if they only have floor plan

    # 2. Price Logic (With formatting for large numbers)
    price = "Price on Request"
    if hasattr(obj, 'monthly_rent') and obj.monthly_rent:
        price = f"₹{obj.monthly_rent}/mo"
    elif hasattr(obj, 'expected_rent') and obj.expected_rent:
        price = f"₹{obj.expected_rent}/mo"
    elif hasattr(obj, 'expected_price') and obj.expected_price:
        try:
            val = float(obj.expected_price)
            if val >= 10000000:
                price = f"₹{val/10000000:.2f} Cr"
            elif val >= 100000:
                price = f"₹{val/100000:.2f} L"
            else:
                price = f"₹{val:,.0f}"
        except:
            price = f"₹{obj.expected_price}"
    elif hasattr(obj, 'plot_price') and obj.plot_price:
        try:
            val = float(obj.plot_price)
            price = f"₹{val/100000:.2f} L" if val >= 100000 else f"₹{val:,.0f}"
        except:
             price = f"₹{obj.plot_price}"

    # 3. Dynamic Title Logic
    title_val = getattr(obj, 'property_title', getattr(obj, 'title', getattr(obj, 'plot_title', getattr(obj, 'pg_name', None))))
    beds_prefix = getattr(obj, 'bhk_type', getattr(obj, 'bhk', None))
    
    if not title_val:
        prefix = beds_prefix if beds_prefix else source
        title_val = f"{prefix} in {getattr(obj, 'locality', getattr(obj, 'village', 'this area'))}"

    # 4. Location Logic
    locality = getattr(obj, 'locality', getattr(obj, 'plot_locality', getattr(obj, 'area_locality', getattr(obj, 'village', ''))))
    city = getattr(obj, 'city', getattr(obj, 'plot_city', ''))
    
    # 5. Owner Info
    owner_name = getattr(obj, 'owner_name', getattr(obj, 'plot_owner_name', 'Owner'))

    # Return the massive dictionary that powers the Smart Card
    return {
        'id': obj.id,
        'category': source, 
        'listing_type': 'sale' if any(x in source for x in ['Resale', 'Sale', 'Agricultural']) else 'rent',
        
        # Display Basics
        'title': title_val,
        'location': f"{locality}, {city}".strip(', '),
        'price_display': price,
        'image_url': img_url,
        'is_ai_match': True,
        
        # Owner / Contact
        'owner': owner_name,
        'owner_initials': owner_name[0].upper() if owner_name else "O",
        'phone': getattr(obj, 'contact_number', getattr(obj, 'owner_contact', getattr(obj, 'plot_owner_contact', 'N/A'))),
        
        # --- SMART SPECS (Crucial for all 8 categories) ---
        
        # Areas
        'area': getattr(obj, 'total_area', getattr(obj, 'built_up_area', getattr(obj, 'builtup_area', getattr(obj, 'carpet_area', None)))),
        'plot_area': getattr(obj, 'plot_area', None),
        'land_area': getattr(obj, 'land_area', getattr(obj, 'plot_area', None)),
        
        # Configurations
        'beds': beds_prefix,
        'baths': getattr(obj, 'bathrooms', getattr(obj, 'baths', None)),
        'total_beds': getattr(obj, 'total_beds', None),
        'min_seats': getattr(obj, 'min_seats', None),
        'kva_capacity': getattr(obj, 'kva_capacity', None),
        
        # Tags / Types
        'property_type': getattr(obj, 'property_type', getattr(obj, 'agriculture_property_type', getattr(obj, 'resale_plot_type', None))),
        'furnished': getattr(obj, 'furnishing_status', getattr(obj, 'furnishing_type', None)),
        'sharing_type': getattr(obj, 'sharing_type', None),
        'pg_for': getattr(obj, 'pg_for', None),
        'plot_road_facing': getattr(obj, 'plot_road_facing', getattr(obj, 'facing', None)),
    }



from django.shortcuts import render
from django.db.models import Q, Case, When, IntegerField



def _sort_qs(qs, sort, price_field):
    if sort == 'newest':
        return qs.order_by('-id')
    elif sort == 'price-asc':
        return qs.order_by(price_field)
    elif sort == 'price-desc':
        return qs.order_by(f'-{price_field}')
    return qs






import math
import json
import re
from datetime import date
from django.utils.timezone import now
from django.shortcuts import render, get_object_or_404
from django.db.models import Case, When, IntegerField

# ─────────────────────────────────────────────────────────────
# HELPER: extract minimum price from PG room_details TextField
# ─────────────────────────────────────────────────────────────
def _get_pg_min_price(obj):
    room_details = getattr(obj, 'room_details', '') or ''
    if not room_details:
        return None
    try:
        data = json.loads(room_details)
        prices = []
        if isinstance(data, dict):
            for v in data.values():
                if isinstance(v, (int, float)) and v > 0:
                    prices.append(v)
        elif isinstance(data, list):
            for item in data:
                if isinstance(item, dict):
                    for v in item.values():
                        if isinstance(v, (int, float)) and v > 0:
                            prices.append(v)
        if prices:
            return min(prices)
    except Exception:
        pass
    # fallback: regex scan for plausible rent numbers
    nums = re.findall(r'[\d,]+', room_details)
    prices = []
    for n in nums:
        try:
            p = int(n.replace(',', ''))
            if 500 <= p <= 500000:
                prices.append(p)
        except Exception:
            pass
    return min(prices) if prices else None


# ─────────────────────────────────────────────────────────────
# HELPER: parse bed-wise prices from PG room_details
# Handles JSON dict, JSON list, or plain text with sharing labels
# ─────────────────────────────────────────────────────────────
def _parse_pg_room_prices(obj):
    result = {}
    room_details = getattr(obj, 'room_details', '') or ''
    if not room_details:
        return result

    KEY_MAP = {
        'single_sharing': ['single', 'single_sharing', '1_sharing', '1sharing', 'single bed'],
        'double_sharing': ['double', 'double_sharing', '2_sharing', '2sharing', 'double bed'],
        'triple_sharing': ['triple', 'triple_sharing', '3_sharing', '3sharing', 'triple bed'],
        'four_sharing':   ['four', 'four_sharing', '4_sharing', '4sharing', '4 sharing'],
        'five_sharing':   ['five', 'five_sharing', '5_sharing', '5sharing', '5 sharing'],
        'six_sharing':    ['six', 'six_sharing', '6_sharing', '6sharing', '6 sharing'],
    }

    try:
        data = json.loads(room_details)
        if isinstance(data, dict):
            lower_data = {k.lower(): v for k, v in data.items()}
            for field, keys in KEY_MAP.items():
                for key in keys:
                    if key in lower_data and lower_data[key]:
                        result[field] = lower_data[key]
                        break
        elif isinstance(data, list):
            for item in data:
                if not isinstance(item, dict):
                    continue
                sharing_label = str(
                    item.get('type', '') or item.get('sharing', '') or
                    item.get('sharing_type', '') or item.get('name', '')
                ).lower()
                price = item.get('price') or item.get('rent') or item.get('amount')
                if not price:
                    continue
                for field, keys in KEY_MAP.items():
                    for key in keys:
                        if key in sharing_label:
                            result[field] = price
                            break
    except Exception:
        # Plain text fallback: "Single: 8000, Double: 6000" etc.
        patterns = {
            'single_sharing': r'single[^0-9]*?([\d,]+)',
            'double_sharing': r'double[^0-9]*?([\d,]+)',
            'triple_sharing': r'triple[^0-9]*?([\d,]+)',
            'four_sharing':   r'(?:4|four)[^0-9]*?([\d,]+)',
            'five_sharing':   r'(?:5|five)[^0-9]*?([\d,]+)',
            'six_sharing':    r'(?:6|six)[^0-9]*?([\d,]+)',
        }
        for field, pat in patterns.items():
            m = re.search(pat, room_details, re.IGNORECASE)
            if m:
                try:
                    result[field] = int(m.group(1).replace(',', ''))
                except Exception:
                    pass

    return result


# ─────────────────────────────────────────────────────────────
# HELPER: normalise ANY property object to a flat dict for
# the listing page cards. Covers all 8 property types.
# ─────────────────────────────────────────────────────────────
def _normalize_any_property(obj, sheet_name):
    LISTING_TYPE = {
        "Residential Data": "rent",
        "Commercial Data":  "rent",
        "PG Data":          "rent",
        "Resale Residential": "sale",
        "Commercial Resale":  "sale",
        "Plot Resale":        "sale",
        "Agricultural Data":  "sale",
        "Industrial Resale":  "sale",
    }
    CATEGORY = {
        "Residential Data": "residential",
        "Commercial Data":  "commercial",
        "PG Data":          "pg",
        "Resale Residential": "residential",
        "Commercial Resale":  "commercial",
        "Plot Resale":        "plot",
        "Agricultural Data":  "agriculture",
        "Industrial Resale":  "industrial",
    }
    EMOJI = {
        "Residential Data": "🏠",
        "Commercial Data":  "🏢",
        "PG Data":          "🛏️",
        "Resale Residential": "🏡",
        "Commercial Resale":  "🏬",
        "Plot Resale":        "🌄",
        "Agricultural Data":  "🌾",
        "Industrial Resale":  "🏭",
    }

    lt  = LISTING_TYPE.get(sheet_name, "rent")
    cat = CATEGORY.get(sheet_name,     "residential")

    # ── Price ────────────────────────────────────────────────
    raw_price = (
        getattr(obj, 'monthly_rent',   None) or
        getattr(obj, 'expected_rent',  None) or
        getattr(obj, 'expected_price', None) or
        getattr(obj, 'plot_price',     None)
    )
    # PG special case
    if sheet_name == "PG Data" and not raw_price:
        raw_price = _get_pg_min_price(obj)

    try:
        price_f = float(raw_price) if raw_price else 0
        if price_f > 0:
            suffix = "/mo" if lt == "rent" else ""
            price_display = f"₹{price_f:,.0f}{suffix}"
        else:
            price_display = "Price on Request"
    except Exception:
        price_display = "Price on Request"

    # ── Title ────────────────────────────────────────────────
    title = (
        getattr(obj, 'title',          None) or
        getattr(obj, 'property_title', None) or
        getattr(obj, 'plot_title',     None) or
        getattr(obj, 'pg_name',        None) or
        getattr(obj, 'building_name',  None) or
        "Property"
    )

    # ── Location ────────────────────────────────────────────
    locality = (
        getattr(obj, 'locality',      None) or
        getattr(obj, 'area_locality', None) or
        getattr(obj, 'plot_locality', None) or
        getattr(obj, 'village',       None) or
        ""
    )
    city = (
        getattr(obj, 'city',      None) or
        getattr(obj, 'plot_city', None) or
        ""
    )
    location = f"{locality}, {city}".strip(", ") if (locality or city) else "Nagpur"

    # ── Area ────────────────────────────────────────────────
    area = (
        getattr(obj, 'builtup_area',  None) or
        getattr(obj, 'built_up_area', None) or
        None
    )
    land_area  = getattr(obj, 'land_area',  None)
    plot_area  = getattr(obj, 'plot_area',  None)
    total_beds = getattr(obj, 'total_beds', None)
    min_seats  = getattr(obj, 'min_seats',  None)
    kva_capacity = getattr(obj, 'kva_capacity', None)

    # ── Config ──────────────────────────────────────────────
    beds = getattr(obj, 'bhk', None) or getattr(obj, 'bhk_type', None)
    baths = getattr(obj, 'bathrooms', None) or getattr(obj, 'baths', None)

    # ── Furnishing ──────────────────────────────────────────
    furnished = (
        getattr(obj, 'furnishing_status', None) or
        getattr(obj, 'furnishing_type',   None) or
        getattr(obj, 'furnished',         None)
    )

    # ── Owner ───────────────────────────────────────────────
    owner_name = (
        getattr(obj, 'owner_name',       None) or
        getattr(obj, 'plot_owner_name',  None) or
        "Owner"
    )
    owner_initials = owner_name[0].upper() if owner_name else "O"

    phone = (
        getattr(obj, 'contact_number',      None) or
        getattr(obj, 'owner_contact',       None) or
        getattr(obj, 'plot_owner_contact',  None) or
        ""
    )

    # ── Image ───────────────────────────────────────────────
    image_url = None
    if hasattr(obj, 'images'):
        try:
            first = obj.images.first()
            if first and first.image:
                image_url = first.image.url
        except Exception:
            pass

    property_type = (
        getattr(obj, 'property_type',            None) or
        getattr(obj, 'agriculture_property_type', None) or
        getattr(obj, 'resale_plot_type',          None)
    )

    return {
        'id':             obj.id,
        'title':          title,
        'location':       location,
        'city':           city,
        'price_display':  price_display,
        'raw_price':      raw_price,
        'area':           area,
        'land_area':      land_area,
        'plot_area':      plot_area,
        'beds':           beds,
        'total_beds':     total_beds,
        'min_seats':      min_seats,
        'kva_capacity':   kva_capacity,
        'baths':          baths,
        'furnished':      furnished,
        'property_type':  property_type,
        'plot_road_facing': getattr(obj, 'plot_road_facing', None),
        'pg_for':         getattr(obj, 'pg_for', getattr(obj, 'best_suited_for', None)),
        'owner':          owner_name,
        'owner_initials': owner_initials,
        'phone':          phone,
        'image_url':      image_url,
        'emoji':          EMOJI.get(sheet_name, "🏠"),
        'listing_type':   lt,
        'category':       cat,
        'is_new':         False,
        'is_ai_match':    False,
    }


# ═════════════════════════════════════════════════════════════
# PROPERTY DETAIL VIEW
# ═════════════════════════════════════════════════════════════
def property_detail_view(request, listing_type, category, pk):
    """
    COMPREHENSIVE PROPERTY DETAIL VIEW
    Supports 8 property types across rent / sale.
    """
    obj = None
    p   = {}
    amenities_list  = []
    facilities_list = []
    property_images = []
    seo_page_type   = ""
    base_emi        = 0
    property_model  = None

    # ── 1. Identify correct model ────────────────────────────
    if listing_type == 'rent':
        if category in ['residential', 'residential-data']:
            property_model = RentalResidentialProperty
            seo_page_type  = "rental_residential"
        elif category in ['commercial', 'commercial-data']:
            property_model = CommercialRentalProperty
            seo_page_type  = "commercial_rental"
        elif category in ['pg', 'pg-data']:
            property_model = PGColivingProperty
            seo_page_type  = "pg_coliving"

    elif listing_type == 'sale':
        if category in ['residential', 'resale-residential']:
            property_model = ResaleResidentialProperty
            seo_page_type  = "resale_residential"
        elif category in ['commercial', 'commercial-resale']:
            property_model = CommercialResaleProperty
            seo_page_type  = "commercial_resale"
        elif category in ['plot', 'plot-resale']:
            property_model = PlotSaleProperty
            seo_page_type  = "plot_sale"
        elif category in ['industrial', 'industrial-resale']:
            property_model = IndustrialResaleProperty
            seo_page_type  = "industrial_sale"
        elif category in ['agriculture', 'agricultural-data']:
            property_model = AgriculturalResaleProperty
            seo_page_type  = "agriculture_sale"

    if not property_model:
        return render(request, 'home_page/property_not_found.html')

    obj = get_object_or_404(property_model, pk=pk)

    # ── 2. Extract all data ──────────────────────────────────

    # BASIC
    p['id'] = obj.id
    p['title'] = (
        getattr(obj, 'title',          None) or
        getattr(obj, 'property_title', None) or
        getattr(obj, 'plot_title',     None) or
        getattr(obj, 'pg_name',        None) or
        getattr(obj, 'building_name',  None) or
        'Property Details'
    )

    p['property_purpose']   = getattr(obj, 'property_purpose', None)
    p['renting_option']     = getattr(obj, 'renting_option',   None)
    p['available_for']      = getattr(obj, 'available_for',    None)

    # Category name
    cat_raw = (
        getattr(obj, 'property_type',             None) or
        getattr(obj, 'agriculture_property_type', None) or
        getattr(obj, 'resale_plot_type',          None) or
        category
    )
    p['category_name'] = str(cat_raw).replace('_', ' ').title()

    # CONFIGURATION
    p['bhk']      = getattr(obj, 'bhk',      None)
    p['bhk_type'] = getattr(obj, 'bhk_type', None)
    p['beds']     = p['bhk'] or p['bhk_type']

    p['bathrooms'] = getattr(obj, 'bathrooms', None)
    p['baths']     = getattr(obj, 'baths', p['bathrooms'])

    p['balconies']       = getattr(obj, 'balconies',       None)
    p['covered_parking'] = getattr(obj, 'covered_parking', None)
    p['open_parking']    = getattr(obj, 'open_parking',    None)
    p['private_parking'] = getattr(obj, 'private_parking', None)
    p['public_parking']  = getattr(obj, 'public_parking',  None)

    # AREA
    p['area'] = (
        getattr(obj, 'builtup_area',  None) or
        getattr(obj, 'built_up_area', None) or
        getattr(obj, 'land_area',     None) or
        getattr(obj, 'plot_area',     None) or
        getattr(obj, 'total_area',    None)
    )
    p['carpet_area']  = getattr(obj, 'carpet_area',  None)
    p['plot_area']    = getattr(obj, 'plot_area',    None)
    p['builtup_area'] = getattr(obj, 'builtup_area', getattr(obj, 'built_up_area', None))

    # FURNISHING & AGE
    p['furnished'] = (
        getattr(obj, 'furnishing_status', None) or
        getattr(obj, 'furnishing_type',   None) or
        getattr(obj, 'furnished',         None)
    )
    p['age']                = getattr(obj, 'age_of_property',   getattr(obj, 'property_age', None))
    p['property_condition'] = getattr(obj, 'property_condition', None)
    p['construction_status']= getattr(obj, 'construction_status', None)

    # FACING & FLOOR
    p['facing'] = getattr(obj, 'facing', getattr(obj, 'plot_road_facing', None))
    p['floor']  = (
        getattr(obj, 'floor_number', None) or
        getattr(obj, 'floor_no',     None) or
        getattr(obj, 'your_floor',   None)
    )
    p['total_floors'] = getattr(obj, 'total_floors', None)

    # ZONE / LOCATION
    p['zone']          = getattr(obj, 'zone',          None)
    p['zone_type']     = getattr(obj, 'zone_type',     None)
    p['location_hub']  = getattr(obj, 'location_hub',  None)
    p['society_type']  = getattr(obj, 'society_type',  None)
    p['water_type']    = getattr(obj, 'water_type',    None)

    # POSSESSION
    p['possession']    = getattr(obj, 'possession_status', getattr(obj, 'available_from', None))
    p['available_from']= getattr(obj, 'available_from',    None)
    p['lease_duration']= getattr(obj, 'lease_duration',    None)

    # OWNERSHIP
    p['ownership']   = getattr(obj, 'ownership_type', getattr(obj, 'plot_ownership', None))
    p['num_owners']  = getattr(obj, 'num_owners',     None)

    # ── PRICING ────────────────────────────────────────────
    # Rental prices
    p['monthly_rent']     = getattr(obj, 'monthly_rent',     getattr(obj, 'expected_rent', None))
    p['security_deposit'] = getattr(obj, 'security_deposit', None)
    p['maintenance']      = getattr(obj, 'maintenance_amount', getattr(obj, 'maintenance_charges', None))
    p['maintenance_type'] = getattr(obj, 'maintenance_type', None)
    p['negotiable']       = getattr(obj, 'negotiable',       None)
    p['is_negotiable']    = getattr(obj, 'is_negotiable',    None)

    # Sale prices
    raw_price = (
        getattr(obj, 'expected_price', None) or
        getattr(obj, 'plot_price',     None) or
        getattr(obj, 'monthly_rent',   None) or
        getattr(obj, 'expected_rent',  None)
    )

    # PG: no direct price field — parse room_details
    if seo_page_type == "pg_coliving":
        pg_prices = _parse_pg_room_prices(obj)
        p.update(pg_prices)  # single_sharing, double_sharing, etc.

        # Set monthly_rent to minimum bed price for sidebar display
        bed_prices = [v for v in pg_prices.values() if v]
        if bed_prices:
            p['monthly_rent'] = min(bed_prices)
            raw_price = p['monthly_rent']
        else:
            pg_min = _get_pg_min_price(obj)
            if pg_min:
                p['monthly_rent'] = pg_min
                raw_price = pg_min

    p['raw_price']      = raw_price or 0
    p['expected_price'] = raw_price or 0

    try:
        price_f = float(raw_price) if raw_price else 0
        p['price_display'] = f"₹{price_f:,.0f}" if price_f > 0 else "Price on Request"
    except Exception:
        p['price_display'] = str(raw_price) if raw_price else "Price on Request"

    p['price_sqft'] = getattr(obj, 'price_per_sqft', None)

    # Brokerage
    b_flag = str(getattr(obj, 'brokerage', '')).lower()
    p['brokerage'] = None
    if b_flag in ['yes', 'true', '1']:
        p['brokerage'] = (
            getattr(obj, 'brokerage_percentage', None) or
            getattr(obj, 'manual_brokerage',     None) or
            'Applicable'
        )

    # COMMERCIAL SPECS
    p['min_seats']       = getattr(obj, 'min_seats',       None)
    p['max_seats']       = getattr(obj, 'max_seats',       None)
    p['cabins']          = getattr(obj, 'cabins',   getattr(obj, 'num_cabins',    None))
    p['meeting_rooms']   = getattr(obj, 'meeting_rooms',   None)
    p['passenger_lifts'] = getattr(obj, 'passenger_lifts', None)
    p['service_lifts']   = getattr(obj, 'service_lifts',   None)
    p['private_washroom']= getattr(obj, 'private_washroom', None)
    p['public_washroom'] = getattr(obj, 'public_washroom',  None)
    p['staircases']      = getattr(obj, 'staircases', getattr(obj, 'num_staircases', None))
    p['flooring_type']   = getattr(obj, 'flooring_type',   None)

    # UTILITIES (commercial)
    p['dg_ups_included']    = getattr(obj, 'dg_ups_included',    False)
    p['electricity_included']= getattr(obj, 'electricity_included', False)
    p['water_included']     = getattr(obj, 'water_included',     False)

    # RENTAL TERMS
    p['lockin_period']  = getattr(obj, 'lockin_period',  None)
    p['rent_increase']  = getattr(obj, 'rent_increase',  None)
    p['minimum_stay']   = getattr(obj, 'minimum_stay',   None)
    p['notice_period']  = getattr(obj, 'notice_period',  None)

    # PG SPECIFIC
    p['total_beds']          = getattr(obj, 'total_beds',         None)
    p['sharing_type']        = getattr(obj, 'sharing_type',       None)
    p['pg_for']              = getattr(obj, 'pg_for',  getattr(obj, 'best_suited_for', None))
    p['meal_offerings']      = getattr(obj, 'meal_offerings',     None)
    p['meals_available']     = getattr(obj, 'meals_available',    False)
    p['meal_speciality']     = getattr(obj, 'meal_speciality',    None)
    p['room_details']        = getattr(obj, 'room_details',       None)
    p['common_area']         = getattr(obj, 'common_area',        None)
    p['property_managed_by'] = getattr(obj, 'property_managed_by', None)
    p['manager_stays']       = getattr(obj, 'manager_stays',      False)

    # PG RULES
    p['non_veg_allowed']     = getattr(obj, 'non_veg_allowed',      False)
    p['opposite_sex_allowed']= getattr(obj, 'opposite_sex_allowed', False)
    p['any_time_allowed']    = getattr(obj, 'any_time_allowed',     False)
    p['visitors_allowed']    = getattr(obj, 'visitors_allowed',     False)
    p['guardian_allowed']    = getattr(obj, 'guardian_allowed',     False)
    p['drinking_allowed']    = getattr(obj, 'drinking_allowed',     False)
    p['smoking_allowed']     = getattr(obj, 'smoking_allowed',      False)

    # PLOT
    p['plot_corner']         = getattr(obj, 'plot_corner',         False)
    p['plot_fencing']        = getattr(obj, 'plot_fencing',        False)
    p['plot_road_facing']    = getattr(obj, 'plot_road_facing',    None)
    p['sanctioning_authority']= getattr(obj, 'sanctioning_authority', getattr(obj, 'plot_authority', None))

    # INDUSTRIAL
    p['power_kva']            = getattr(obj, 'kva_capacity',          getattr(obj, 'power_supply', None))
    p['power_supply']         = getattr(obj, 'power_supply',          None)
    p['water_supply']         = getattr(obj, 'water_supply',          None)
    p['crane_heavy_machinery']= getattr(obj, 'crane_heavy_machinery', False)
    p['road_connectivity']    = getattr(obj, 'road_connectivity',     None)
    p['worker_housing_nearby']= getattr(obj, 'worker_housing_nearby', False)

    # AGRICULTURE
    p['soil_type']          = getattr(obj, 'soil_type',          None)
    p['water_source']       = getattr(obj, 'water_source', getattr(obj, 'water_type', None))
    p['irrigation_facility']= getattr(obj, 'irrigation_facility', None)
    p['fertility_status']   = getattr(obj, 'fertility_status',   None)
    p['previous_crops']     = getattr(obj, 'previous_crops',     None)
    p['state']              = getattr(obj, 'state',              None)
    p['district']           = getattr(obj, 'district',           None)
    p['taluka']             = getattr(obj, 'taluka',             None)
    p['village']            = getattr(obj, 'village',            None)

    # LEGAL
    def _bool_field(*attrs):
        for a in attrs:
            v = getattr(obj, a, None)
            if v is not None:
                return str(v).lower() in ['yes', 'true', '1']
        return False

    p['has_loan']        = _bool_field('has_loan', 'plot_loan', 'agri_loan', 'loan_on_property')
    p['loan_amount']     = getattr(obj, 'loan_amount', getattr(obj, 'plot_loan_amount', None))
    p['has_dispute']     = _bool_field('has_legal_dispute', 'legal_dispute', 'agri_dispute')
    p['dispute_details'] = getattr(obj, 'dispute_details', None)
    p['has_tax_due']     = _bool_field('has_tax_due', 'tax_due', 'agri_tax_due')
    p['tax_amount']      = getattr(obj, 'pending_tax_amount', getattr(obj, 'tax_amount', None))
    p['has_tenants']     = _bool_field('has_tenants', 'existing_tenants', 'agri_tenants')
    p['tenant_details']  = getattr(obj, 'tenant_details', None)
    p['fire_noc']        = getattr(obj, 'fire_noc',            None)
    p['tax_clearance_cert']= getattr(obj, 'tax_clearance_cert', False)
    p['encumbrance_cert']  = getattr(obj, 'encumbrance_cert',   None)
    p['compliance_docs']   = getattr(obj, 'compliance_docs',    None)

    # LOCATION
    p['city']     = getattr(obj, 'city',     getattr(obj, 'plot_city', getattr(obj, 'state', '')))
    p['locality'] = (
        getattr(obj, 'locality',      None) or
        getattr(obj, 'plot_locality', None) or
        getattr(obj, 'area_locality', None) or
        getattr(obj, 'village',       None) or
        ''
    )
    p['address'] = (
        getattr(obj, 'complete_address',  None) or
        getattr(obj, 'property_address',  None) or
        getattr(obj, 'address',           None) or
        getattr(obj, 'plot_address',      None) or
        ''
    )
    p['building_name'] = getattr(obj, 'building_name', None)
    p['pincode']       = getattr(obj, 'pincode', '')

    # DESCRIPTION
    p['desc'] = (
        getattr(obj, 'description',            None) or
        getattr(obj, 'property_description',   None) or
        getattr(obj, 'rent_residential_desc',  None) or
        getattr(obj, 'resale_agricultural_desc', None) or
        getattr(obj, 'pg_description',         None) or
        ''
    )

    # MEDIA
    p['video'] = (
        getattr(obj, 'property_video', None) or
        getattr(obj, 'video',          None) or
        getattr(obj, 'social_video',   None)
    )
    p['floor_plan'] = getattr(obj, 'floor_plan', None)

    # OWNER
    p['owner_name']    = (
        getattr(obj, 'owner_name',       None) or
        getattr(obj, 'plot_owner_name',  None) or
        'Property Owner'
    )
    p['owner_contact'] = (
        getattr(obj, 'contact_number',      None) or
        getattr(obj, 'owner_contact',       None) or
        getattr(obj, 'plot_owner_contact',  None) or
        ''
    )
    p['owner_email'] = (
        getattr(obj, 'email',             None) or
        getattr(obj, 'owner_email',       None) or
        getattr(obj, 'plot_owner_email',  None) or
        ''
    )
    p['alternate_contact']  = getattr(obj, 'alternate_contact', None)
    p['residential_status'] = getattr(obj, 'residential_status', getattr(obj, 'comm_residency', None))

    # UPLOADED BY
    p['uploaded_by_role']    = getattr(obj, 'uploaded_by_role',    'Owner')
    p['uploaded_by_name']    = getattr(obj, 'uploaded_by_name',    None)
    p['uploaded_by_email']   = getattr(obj, 'uploaded_by_email',   None)
    p['uploaded_by_contact'] = getattr(obj, 'uploaded_by_contact', None)

    # ── 3. Images & Amenities ────────────────────────────────
    if hasattr(obj, 'images'):
        property_images = obj.images.all()

    def parse_list(val):
        if not val:
            return []
        if isinstance(val, list):
            return [str(x).strip() for x in val if x]
        if isinstance(val, str):
            try:
                parsed = json.loads(val)
                if isinstance(parsed, list):
                    return [str(x).strip() for x in parsed if x]
            except Exception:
                pass
            return [x.strip() for x in val.split(',') if x.strip()]
        return []

    amenities_list  = parse_list(getattr(obj, 'amenities',          ''))
    facilities_list = parse_list(getattr(obj, 'nearby_facilities',  getattr(obj, 'facilities', '')))

    if p.get('dg_ups_included'):    amenities_list.append("DG/UPS Backup")
    if p.get('electricity_included'): amenities_list.append("Electricity Included")
    if p.get('water_included'):     amenities_list.append("Water Included")

    # ── 4. EMI Calculator ────────────────────────────────────
    if listing_type == 'sale' and p['raw_price']:
        try:
            principal = float(p['raw_price']) * 0.80
            r = 8.5 / 12 / 100
            n = 20 * 12
            base_emi = int((principal * r * math.pow(1 + r, n)) / (math.pow(1 + r, n) - 1))
        except Exception:
            base_emi = 0

    # ── 5. Similar Properties ────────────────────────────────
    similar = []
    if p.get('city'):
        try:
            similar_qs = property_model.objects.filter(is_deleted=False).exclude(id=obj.id)

            city_val = p['city']
            if hasattr(property_model, 'city'):
                similar_qs = similar_qs.filter(city__icontains=city_val)
            elif hasattr(property_model, 'plot_city'):
                similar_qs = similar_qs.filter(plot_city__icontains=city_val)

            for s_obj in similar_qs[:3]:
                s_raw = (
                    getattr(s_obj, 'expected_price', None) or
                    getattr(s_obj, 'plot_price',     None) or
                    getattr(s_obj, 'monthly_rent',   None) or
                    getattr(s_obj, 'expected_rent',  None)
                )
                # PG similar price
                if seo_page_type == "pg_coliving" and not s_raw:
                    s_raw = _get_pg_min_price(s_obj)

                try:
                    s_price_str = f"₹{float(s_raw):,.0f}" if s_raw else "Ask Price"
                except Exception:
                    s_price_str = "Ask Price"

                s_bhk  = getattr(s_obj, 'bhk', getattr(s_obj, 'bhk_type', ''))
                s_area = (
                    getattr(s_obj, 'builtup_area', None) or
                    getattr(s_obj, 'land_area',    None) or
                    getattr(s_obj, 'plot_area',    None) or
                    getattr(s_obj, 'carpet_area',  None)
                )
                feature = s_bhk if s_bhk else (f"{s_area} Sq.Ft" if s_area else "Details")

                s_img_url = None
                if hasattr(s_obj, 'images'):
                    try:
                        fi = s_obj.images.first()
                        if fi and fi.image:
                            s_img_url = fi.image.url
                    except Exception:
                        pass

                similar.append({
                    'id':            s_obj.id,
                    'title':         (
                        getattr(s_obj, 'title',          None) or
                        getattr(s_obj, 'plot_title',     None) or
                        getattr(s_obj, 'pg_name',        None) or
                        getattr(s_obj, 'property_title', 'Property')
                    ),
                    'price_display': s_price_str,
                    'location':      (
                        getattr(s_obj, 'locality',      None) or
                        getattr(s_obj, 'plot_locality', None) or
                        getattr(s_obj, 'area_locality', None) or
                        ''
                    ),
                    'feature':       feature,
                    'listing_type':  listing_type,
                    'category':      category,
                    'image_url':     s_img_url,
                })
        except Exception:
            pass

    # ── 6. SEO & Auth ────────────────────────────────────────
    seo = None
    try:
        from .models import LocationSEO
        from django.contrib.contenttypes.models import ContentType
        seo = LocationSEO.objects.filter(
            content_type=ContentType.objects.get_for_model(obj),
            object_id=obj.id,
            pagetype=seo_page_type,
            is_active=True,
        ).first()
    except Exception:
        pass

    user_id = request.session.get('user_id') or request.session.get('User_id')
    logged_user = user_obj = user_subscription = None
    can_view_contact = False

    if user_id:
        try:
            from .models import User_Details
            logged_user = User_Details.objects.filter(id=user_id).first()
            user_obj    = logged_user
            try:
                from .utils import get_active_subscription
                user_subscription = get_active_subscription(logged_user)
                if user_subscription:
                    can_view_contact = True
            except Exception:
                pass
        except Exception:
            pass

    # Mask phone
    masked_phone = "XXXXXXXXXX"
    if p['owner_contact'] and len(str(p['owner_contact'])) >= 10:
        ph = str(p['owner_contact'])
        masked_phone = f"{ph[:2]}XXXXXX{ph[-2:]}"

    # ── 7. Context & Render ──────────────────────────────────
    context = {
        "p":                p,
        "original":         obj,
        "listing_type":     listing_type,
        "category":         category,
        "property_images":  property_images,
        "amenities_list":   amenities_list,
        "facilities_list":  facilities_list,
        "similar":          similar,
        "base_emi":         base_emi,
        "raw_price":        p['raw_price'],
        "seo":              seo,
        "logged_user":      logged_user,
        "user_obj":         user_obj,
        "user_subscription":user_subscription,
        "can_view_contact": can_view_contact,
        "masked_phone":     masked_phone,
        "today":            date.today(),
        "now":              now(),
    }
    return render(request, 'home_page/property_detail.html', context)


# ═════════════════════════════════════════════════════════════
# LISTINGS VIEW
# ═════════════════════════════════════════════════════════════
def listings_view(request):

    # GET FILTERS
    raw_types        = request.GET.get('types', '')
    selected_types   = [t.strip() for t in raw_types.split(',') if t.strip()] if raw_types else []
    ai_query         = request.GET.get('ai_query', '').strip()
    bhk_filter       = request.GET.get('bhk', '').strip()
    city_filter      = request.GET.get('city_filter', '').strip()
    listing_type     = request.GET.get('type', 'rent').strip()
    category         = request.GET.get('category', '').strip()
    area_filter      = request.GET.get('area', '').strip()
    budget_min       = request.GET.get('budget_min', '').strip()
    budget_max       = request.GET.get('budget_max', '').strip()
    furnishing_filter= request.GET.get('furnishing', '').strip()
    verified_filter  = request.GET.get('verified')
    featured_filter  = request.GET.get('featured')
    owner_filter     = request.GET.get('owner')
    pet_filter       = request.GET.get('pet')
    sort_filter      = request.GET.get('sort', 'relevant')

    normalized_properties = []

    # MODEL MAP
    model_map = {
        "Residential Data": RentalResidentialProperty,
        "Commercial Data":  CommercialRentalProperty,
        "PG Data":          PGColivingProperty,
        "Resale Residential": ResaleResidentialProperty,
        "Commercial Resale":  CommercialResaleProperty,
        "Plot Resale":        PlotSaleProperty,
        "Agricultural Data":  AgriculturalResaleProperty,
        "Industrial Resale":  IndustrialResaleProperty,
    }

    # AI SEARCH
    if ai_query:
        df           = MainAppConfig.get_ai_df()
        model_ai     = MainAppConfig.get_ai_model()
        faiss_index  = MainAppConfig.get_ai_faiss()
        query_vector = model_ai.encode([ai_query]).astype('float32')
        _, indices   = faiss_index.search(query_vector, k=100)
        results_df   = df.iloc[indices[0]].copy()

        if category:
            results_df = results_df[results_df['source_sheet'] == category]

        for _, row in results_df.iterrows():
            if len(normalized_properties) >= 20:
                break
            db_model = model_map.get(row.get('source_sheet'))
            if not db_model:
                continue
            obj_q = db_model.objects.filter(id=row.get('db_id'))
            if city_filter:
                obj_q = obj_q.filter(city__icontains=city_filter)
            if area_filter:
                for f in ('locality', 'area_locality', 'address'):
                    if hasattr(db_model, f):
                        obj_q = obj_q.filter(**{f'{f}__icontains': area_filter})
                        break
            real_obj = obj_q.first()
            if real_obj:
                normalized_properties.append(_normalize_any_property(real_obj, row.get('source_sheet')))

    # NORMAL SEARCH
    else:
        # Determine which models to query
        if listing_type == "rent":
            if category == "Residential Data":
                models_to_search = [("Residential Data", RentalResidentialProperty)]
            elif category == "Commercial Data":
                models_to_search = [("Commercial Data",  CommercialRentalProperty)]
            elif category == "PG Data":
                models_to_search = [("PG Data",          PGColivingProperty)]
            else:
                models_to_search = [
                    ("Residential Data", RentalResidentialProperty),
                    ("Commercial Data",  CommercialRentalProperty),
                    ("PG Data",          PGColivingProperty),
                ]
        elif listing_type == "sale":
            if category == "Resale Residential":
                models_to_search = [("Resale Residential", ResaleResidentialProperty)]
            elif category == "Commercial Resale":
                models_to_search = [("Commercial Resale",  CommercialResaleProperty)]
            elif category == "Plot Resale":
                models_to_search = [("Plot Resale",        PlotSaleProperty)]
            elif category == "Agricultural Data":
                models_to_search = [("Agricultural Data",  AgriculturalResaleProperty)]
            elif category == "Industrial Resale":
                models_to_search = [("Industrial Resale",  IndustrialResaleProperty)]
            else:
                models_to_search = [
                    ("Resale Residential", ResaleResidentialProperty),
                    ("Commercial Resale",  CommercialResaleProperty),
                    ("Plot Resale",        PlotSaleProperty),
                    ("Agricultural Data",  AgriculturalResaleProperty),
                    ("Industrial Resale",  IndustrialResaleProperty),
                ]
        else:
            models_to_search = list(model_map.items())

        for sheet_name, db_model in models_to_search:
            if len(normalized_properties) >= 20:
                break

            obj_q = db_model.objects.all()

            # Filter deleted
            if hasattr(db_model, 'is_deleted'):
                obj_q = obj_q.filter(is_deleted=False)

            # City filter
            if city_filter:
                if hasattr(db_model, 'city'):
                    obj_q = obj_q.filter(city__icontains=city_filter)
                elif hasattr(db_model, 'plot_city'):
                    obj_q = obj_q.filter(plot_city__icontains=city_filter)

            # Area filter (locality / area_locality / address / village)
            if area_filter:
                from django.db.models import Q
                area_q = Q()
                for f in ('locality', 'area_locality', 'plot_locality', 'address', 'village'):
                    if hasattr(db_model, f):
                        area_q |= Q(**{f'{f}__icontains': area_filter})
                if area_q:
                    obj_q = obj_q.filter(area_q)

            # BHK filter
            if bhk_filter:
                from django.db.models import Q
                bhk_q = Q()
                for f in ('bhk_type', 'bhk'):
                    if hasattr(db_model, f):
                        bhk_q |= Q(**{f'{f}__icontains': bhk_filter})
                if bhk_q:
                    obj_q = obj_q.filter(bhk_q)

            # Budget min
            if budget_min:
                try:
                    bmin = int(budget_min)
                    if hasattr(db_model, 'monthly_rent'):
                        obj_q = obj_q.filter(monthly_rent__gte=bmin)
                    elif hasattr(db_model, 'expected_rent'):
                        obj_q = obj_q.filter(expected_rent__gte=bmin)
                    elif hasattr(db_model, 'expected_price'):
                        obj_q = obj_q.filter(expected_price__gte=bmin)
                    elif hasattr(db_model, 'plot_price'):
                        obj_q = obj_q.filter(plot_price__gte=bmin)
                except ValueError:
                    pass

            # Budget max
            if budget_max:
                try:
                    bmax = int(budget_max)
                    if hasattr(db_model, 'monthly_rent'):
                        obj_q = obj_q.filter(monthly_rent__lte=bmax)
                    elif hasattr(db_model, 'expected_rent'):
                        obj_q = obj_q.filter(expected_rent__lte=bmax)
                    elif hasattr(db_model, 'expected_price'):
                        obj_q = obj_q.filter(expected_price__lte=bmax)
                    elif hasattr(db_model, 'plot_price'):
                        obj_q = obj_q.filter(plot_price__lte=bmax)
                except ValueError:
                    pass

            # Furnishing
            if furnishing_filter:
                for f in ('furnishing_status', 'furnishing_type', 'furnished'):
                    if hasattr(db_model, f):
                        obj_q = obj_q.filter(**{f'{f}__icontains': furnishing_filter})
                        break

            # Verified / Featured / Owner / Pet
            if verified_filter and hasattr(db_model, 'is_verified'):
                obj_q = obj_q.filter(is_verified=True)
            if featured_filter and hasattr(db_model, 'is_featured'):
                obj_q = obj_q.filter(is_featured=True)
            if owner_filter and hasattr(db_model, 'listed_by'):
                obj_q = obj_q.filter(listed_by__icontains='owner')
            if pet_filter and hasattr(db_model, 'pet_friendly'):
                obj_q = obj_q.filter(pet_friendly=True)

            # Sorting
            if sort_filter == "price-asc":
                for f in ('monthly_rent', 'expected_rent', 'expected_price', 'plot_price'):
                    if hasattr(db_model, f):
                        obj_q = obj_q.order_by(f)
                        break
            elif sort_filter == "price-desc":
                for f in ('monthly_rent', 'expected_rent', 'expected_price', 'plot_price'):
                    if hasattr(db_model, f):
                        obj_q = obj_q.order_by(f'-{f}')
                        break
            elif sort_filter == "newest":
                obj_q = obj_q.order_by('-id')
            else:
                # Relevance scoring
                conditions = []
                if hasattr(db_model, 'is_verified'):
                    conditions.append(When(is_verified=True, then=10))
                if hasattr(db_model, 'is_featured'):
                    conditions.append(When(is_featured=True, then=8))
                if area_filter:
                    for f in ('locality', 'area_locality', 'plot_locality'):
                        if hasattr(db_model, f):
                            conditions.append(When(**{f'{f}__icontains': area_filter}, then=12))
                            break
                if bhk_filter:
                    for f in ('bhk_type', 'bhk'):
                        if hasattr(db_model, f):
                            conditions.append(When(**{f'{f}__icontains': bhk_filter}, then=15))
                            break

                obj_q = obj_q.annotate(
                    relevance_score=Case(
                        *conditions,
                        default=1,
                        output_field=IntegerField(),
                    )
                ).order_by('-relevance_score', '-id')

            remaining = 20 - len(normalized_properties)
            for real_obj in obj_q[:remaining]:
                normalized_properties.append(_normalize_any_property(real_obj, sheet_name))

    # Active filter count
    active_filter_count = sum(1 for v in [
        area_filter, bhk_filter, budget_min, budget_max,
        furnishing_filter, verified_filter, featured_filter,
        owner_filter, pet_filter,
    ] if v)

    context = {
        'properties':          normalized_properties,
        'total':               len(normalized_properties),
        'category':            category if category else "All",
        'current_city':        city_filter if city_filter else "Nagpur",
        'listing_type':        listing_type,
        'current_bhk':         bhk_filter,
        'current_area':        area_filter,
        'budget_min':          budget_min,
        'budget_max':          budget_max,
        'current_furnishing':  furnishing_filter,
        'filter_verified':     verified_filter,
        'filter_featured':     featured_filter,
        'filter_owner':        owner_filter,
        'filter_pet':          pet_filter,
        'current_sort':        sort_filter,
        'active_filter_count': active_filter_count,
    }
    return render(request, 'home_page/listingpage.html', context)





# ─────────────────────────────────────────────────────────────────────────────
#  NORMALIZERS
# ─────────────────────────────────────────────────────────────────────────────

def _initials(name):
    return ''.join([w[0] for w in (name or 'UN').split() if w])[:2].upper()




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
        return JsonResponse({"status":"1",'msg': 'Logout Successfully '})
    except:
        print(traceback.format_exc())

############### Views end for admin logout ###########################





# Helper to get client IP
def get_client_ip(request):
    return request.META.get('REMOTE_ADDR')

# ---------------- HOME ----------------


# ---------------- SIGNUP ----------------

@csrf_exempt
def signup_view(request):
    if request.method == "POST":
        full_name = request.POST.get('full_name', '').strip()
        email = request.POST.get('email', '').strip()
        mobile_number = request.POST.get('mobile_number', '').strip()
        password = request.POST.get('password', '')
        role = request.POST.get('role', '').strip()

        # Basic Validation
        if not all([full_name, email, mobile_number, password, role]):
            return JsonResponse({
                'status': '0', 
                'msg': 'Please fill all the required fields.'
            })

        try:
            if User_Details.objects.filter(user_email=email,user_role=role).exists():
                return JsonResponse({
                    'status': '0', 
                    'msg': 'An account with this email address already exists.'
                })
            
            if User_Details.objects.filter(user_phone=mobile_number,user_role=role).exists():
                return JsonResponse({'status': '0', 'msg': 'This mobile number is already registered.'})

            # 3. Create the User
            User_Details.objects.create(
                user_name=full_name,
                user_email=email,
                user_phone=mobile_number,
                user_role=role,              
                user_password=password
            )
           
            user_qs = User_Details.objects.filter(user_email=email, user_password=password, user_role=role)
            
            if user_qs.exists():
                user_obj = user_qs.first()
                
                # --- SESSION LOGIC ---
                # Note: Logging in a new person will overwrite these session keys
                request.session['User_id'] = str(user_obj.id)
                request.session['user_type'] = role

            return JsonResponse({
                'status': '1', 
                'msg': 'Account created successfully!',
                'user_name': user_obj.user_name,    
                'user_role': user_obj.user_role,   
                'user_mobile': user_obj.user_phone,
            })

        except Exception as e:
            return JsonResponse({
                'status': '0', 
                'msg': f'An error occurred: {str(e)}'
            })

    return render(request, 'home_page/signup.html')


import json
import traceback
from django.shortcuts import render
from django.http import JsonResponse
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q 

@csrf_exempt
def login_view(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body.decode('utf-8'))
            user_identifier = data.get('user_identifier', '').strip()
            user_password = data.get('user_password', '')
            user_role = data.get('user_role') 

            user_qs = User_Details.objects.filter(
                Q(user_email=user_identifier) | Q(user_phone=user_identifier),
                user_password=user_password, 
                user_role=user_role
            )
            
            if user_qs.exists():
                user_obj = user_qs.first()
                
                # --- SESSION LOGIC ---
                request.session['User_id'] = str(user_obj.id)
                request.session['user_type'] = user_role
                

                # --- DYNAMIC REDIRECT LOGIC ---

                if user_role == 'Relationship Manager':
                    # Make sure 'rm_dashboard' matches the exact name in your urls.py!
                    url = reverse('rm_dashboard') 
                else:
                    url = reverse('index')
                
                return JsonResponse({
                    'status': '1', 
                    'msg': 'Success!',
                    'user_name': user_obj.user_name, 
                    'user_role': user_obj.user_role,
                    'user_mobile': user_obj.user_phone, 
                    'user_email': user_obj.user_email,
                    'redirect_url': url 
                })

            return JsonResponse({'status': 0, 'msg': 'Invalid Credentials or Role Selection'})

        except Exception:
            print(traceback.format_exc())
            return JsonResponse({'status': 0, 'msg': 'Something went wrong'})
    
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














def get_featured_queryset(model):
    return model.objects.filter(
       
    ).order_by('-created_at')[:6]








def index(request):
    today = datetime.now().date()
    fifteen_days_ago = today - timedelta(days=15)
    
    # ═══════════════════════════════════════════════════════
    # FETCH RENTAL PROPERTIES
    # ═══════════════════════════════════════════════════════
    rental_residential = RentalResidentialProperty.objects.prefetch_related('images').all().order_by('-id')
    rental_commercial = CommercialRentalProperty.objects.prefetch_related('images').all().order_by('-id')
    rental_pg = PGColivingProperty.objects.prefetch_related('images').all().order_by('-id')

    resale_residential = ResaleResidentialProperty.objects.prefetch_related('images').all().order_by('-id')
    resale_commercial = CommercialResaleProperty.objects.prefetch_related('images').filter(is_active=True).order_by('-id')
    resale_plot = PlotSaleProperty.objects.prefetch_related('images').all().order_by('-id')
    resale_industrial = IndustrialResaleProperty.objects.prefetch_related('images').all().order_by('-id')
    resale_agricultural = AgriculturalResaleProperty.objects.prefetch_related('images').all().order_by('-id')
    

    rental_map = {
        "Residential": rental_residential[:4],
        "Commercial": rental_commercial[:4],
        "PG / Co-Living": rental_pg[:4]
    }

    resale_map = {
        "Residential": resale_residential[:4],
        "Commercial": resale_commercial[:4],
        "Plots / Land": resale_plot[:4],
        "Industrial": resale_industrial[:4],
        "Agricultural": resale_agricultural[:4]
    }
    # ═══════════════════════════════════════════════════════
    # COMBINE RENTAL PROPERTIES
    # ═══════════════════════════════════════════════════════
    
    
    # ═══════════════════════════════════════════════════════
    # COMBINE RESALE PROPERTIES
    # ═══════════════════════════════════════════════════════
   
    
    # ═══════════════════════════════════════════════════════
    # GET RECENT PROPERTIES (LAST 30 DAYS)
    # ═══════════════════════════════════════════════════════
    
    
    # ═══════════════════════════════════════════════════════
    # OTHER DATA
    # ═══════════════════════════════════════════════════════
    hero = HeroSection.objects.filter(is_active=True).first()
    
    seo_pages = LocationSEO.objects.filter(is_active=True, pagetype="blog")
    
   # faqs = FAQ.objects.all().order_by('-created_at')[:4]
    
    # ═══════════════════════════════════════════════════════
    # CONTEXT
    # ═══════════════════════════════════════════════════════
    
   # faqs = FAQ.objects.all().order_by('-created_at')

    subscriptions = Subscription_Details.objects.all()
    services = LocationSEO.objects.filter(pagetype="service", is_active=True)

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
       
       
        "hero": hero,
        "seo_pages":seo_pages,
       # "faqs": faqs,
        "today": today,
        "fifteen_days_ago": fifteen_days_ago,
        'user_obj': None,
        'services': services,
        'subscriptions':subscriptions,
        "rental_map": rental_map,
        "resale_map": resale_map,
    }
    
    # ═══════════════════════════════════════════════════════
    # HANDLE LOGGED-IN USER
    # ═══════════════════════════════════════════════════════
    session_id = request.session.get('User_id')
    if session_id:
        user_obj = User_Details.objects.filter(id=session_id).first()
        if user_obj:
            context['user_obj'] = user_obj
    
    return render(request, "home_page/index.html", context)







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

    seo = get_object_or_404(
        LocationSEO,
        key=key,
        pagetype="service",
        is_active=True
    )

    service = seo.content_object

    keywords = []

    if seo.secondary_keywords:
        keywords = seo.secondary_keywords.split(",")

    return render(
        request,
        "home_page/services_details.html",
        {
            "seo": seo,
            "service": service,
            "keywords": keywords
        }
    )


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


############## Views start for contact us page #########################

def Contact_Us(request):

    context = {}
    # ═══════════════════════════════════════════════════════
    # HANDLE LOGGED-IN USER
    # ═══════════════════════════════════════════════════════
    session_id = request.session.get('User_id')
    if session_id:
        user_obj = User_Details.objects.filter(id=session_id).first()
        if user_obj:
            context['user_obj'] = user_obj
            
    return render(request,'home_page/contact.html',context)

############# Views end for contact us page ##############################


############ Views start for contact us page ########################

@csrf_exempt
def Contact_Ajax(request):
    data = request.POST.dict()

    data.pop("id", None)     
    data['contact_enquiry_date'] = datetime.today()
    data['contact_enquiry_time'] = datetime.now()
        
    Contact_Enquiry.objects.create(**data)
    return JsonResponse({"status":"1", "msg" : f"Contact Enquiry Details added successfully"})


########## Views end for contact us page ###########################
   

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
        
        
    elif type == "resale_residential":
        property_obj = get_object_or_404(ResaleResidentialProperty, id=id)
        faq_list = PropertyFAQ.objects.filter(resale_residential=property_obj)
        
    elif type == "resale_commericial":
        property_obj = get_object_or_404(CommercialResaleProperty, id=id)
        faq_list = PropertyFAQ.objects.filter(resale_commericial =property_obj)
        
    elif type == "resale_industrial":
        property_obj = get_object_or_404(IndustrialResaleProperty, id=id)
        faq_list = PropertyFAQ.objects.filter(resale_industrial =property_obj)
        
    elif type == "resale_plot":
        property_obj = get_object_or_404(PlotSaleProperty, id=id)
        faq_list = PropertyFAQ.objects.filter(resale_plot =property_obj)

    elif type == "resale_agriculture":
        property_obj = get_object_or_404(AgriculturalResaleProperty, id=id)
        faq_list = PropertyFAQ.objects.filter(resale_agriculture =property_obj)
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

    # 🔹 3. Handle the logged-in user logic safely
    session_id = request.session.get('User_id')
    if session_id:
        
        user_obj = User_Details.objects.filter(id=session_id).first()
        if user_obj:
            context['user_obj'] = user_obj

    return render(request, "Listing_Form/Rental_Property/rent_residential.html",context)



def rent_commercial(request):
    ameneties_obj = Ameneties_Details.objects.all()
    facilities_obj = Facilities_Details.objects.all()

    context = {'ameneties_obj':ameneties_obj,'facilities_obj':facilities_obj}

    # 🔹 3. Handle the logged-in user logic safely
    session_id = request.session.get('User_id')
    if session_id:
        
        user_obj = User_Details.objects.filter(id=session_id).first()
        if user_obj:
            context['user_obj'] = user_obj

    return render(request, "Listing_Form/Rental_Property/rent_commercial.html",context)

def rent_pg_coliving(request):
    ameneties_obj = Ameneties_Details.objects.all()
    facilities_obj = Facilities_Details.objects.all()

    context = {'ameneties_obj':ameneties_obj,'facilities_obj':facilities_obj}

    # 🔹 3. Handle the logged-in user logic safely
    session_id = request.session.get('User_id')
    if session_id:
        
        user_obj = User_Details.objects.filter(id=session_id).first()
        if user_obj:
            context['user_obj'] = user_obj

    return render(request, "Listing_Form/Rental_Property/rent_pg_coliving.html",context)


#######################End View Section For Rental Listing#################################



#######################Start View Section For Resale Listing#################################


def residential_resale_form(request):
    ameneties_obj = Ameneties_Details.objects.all()
    facilities_obj = Facilities_Details.objects.all()

    context = {'ameneties_obj':ameneties_obj,'facilities_obj':facilities_obj}

    # 🔹 3. Handle the logged-in user logic safely
    session_id = request.session.get('User_id')
    if session_id:
        
        user_obj = User_Details.objects.filter(id=session_id).first()
        if user_obj:
            context['user_obj'] = user_obj

    return render(request, "Listing_Form/Resale_Property/residential_resale_form.html",context)



def resale_commercial_form(request):
    ameneties_obj = Ameneties_Details.objects.all()
    facilities_obj = Facilities_Details.objects.all()

    context = {'ameneties_obj':ameneties_obj,'facilities_obj':facilities_obj}

    # 🔹 3. Handle the logged-in user logic safely
    session_id = request.session.get('User_id')
    if session_id:
        
        user_obj = User_Details.objects.filter(id=session_id).first()
        if user_obj:
            context['user_obj'] = user_obj

    return render(request, "Listing_Form/Resale_Property/resale_commercial_form.html",context)

def resale_agricultural_form(request):
    context = {}

    # 🔹 3. Handle the logged-in user logic safely
    session_id = request.session.get('User_id')
    if session_id:
        
        user_obj = User_Details.objects.filter(id=session_id).first()
        if user_obj:
            context['user_obj'] = user_obj

    return render(request, "Listing_Form/Resale_Property/resale_agricultural_form.html",context)


def resale_plot_form(request):
    context = {}

    # 🔹 3. Handle the logged-in user logic safely
    session_id = request.session.get('User_id')
    if session_id:
        
        user_obj = User_Details.objects.filter(id=session_id).first()
        if user_obj:
            context['user_obj'] = user_obj

    return render(request, "Listing_Form/Resale_Property/resale_plot_form.html",context)

def resale_industrial_form(request):
    context = {}

    # 🔹 3. Handle the logged-in user logic safely
    session_id = request.session.get('User_id')
    if session_id:
        
        user_obj = User_Details.objects.filter(id=session_id).first()
        if user_obj:
            context['user_obj'] = user_obj

    return render(request, "Listing_Form/Resale_Property/resale_industrial_form.html",context)





#######################End View Section For Resale Listing#################################



#######################START View Section For POST PROPERTY SECTION#################################

def post_property(request):
    # 🔹 3. Handle the logged-in user logic safely
    session_id = request.session.get('User_id')
    context={}
    if session_id:
        
        user_obj = User_Details.objects.filter(id=session_id).first()
        if user_obj:
            context['user_obj'] = user_obj

    return render(request, "Post_Property_pages/post_property.html",context)


#############################START VIEW SECTON OF BLOGS##########################

def blog_details(request, key):
    seo = get_object_or_404(LocationSEO, key=key, pagetype="blog", is_active=True)
    blog = seo.content_object

    return render(request, "home_page/blog_details.html", {"seo": seo, "blog": blog})

    
#############################END VIEW SECTON OF BLOGS##########################





def dynamic_property_faq(request):

    faq_sections = []

    # =========================================
    # RENTAL RESIDENTIAL
    # =========================================

    residential = RentalResidentialProperty.objects.filter(
        is_deleted=False
    )[:5]

    for p in residential:

        faq_sections.append({

            "title": p.property_title or "Residential Property",

            "category": "Rental Residential",

            "faqs": [

                {
                    "question": "What is the monthly rent?",
                    "answer": f"Monthly rent is ₹{p.monthly_rent}"
                },

                {
                    "question": "What is the BHK type?",
                    "answer": f"This property is {p.bhk_type}"
                },

                {
                    "question": "What is the furnishing status?",
                    "answer": p.furnishing_status
                },

                {
                    "question": "Where is the property located?",
                    "answer": f"{p.locality}, {p.city}"
                },

                {
                    "question": "What amenities are available?",
                    "answer": p.amenities
                },

            ]
        })

    # =========================================
    # COMMERCIAL RENTAL
    # =========================================

    commercial = CommercialRentalProperty.objects.filter(
        is_deleted=False
    )[:5]

    for p in commercial:

        faq_sections.append({

            "title": p.property_type,

            "category": "Commercial Rental",

            "faqs": [

                {
                    "question": "What is the expected rent?",
                    "answer": f"₹{p.expected_rent}"
                },

                {
                    "question": "What is the built-up area?",
                    "answer": f"{p.builtup_area} Sq.ft"
                },

                {
                    "question": "Where is the property located?",
                    "answer": f"{p.area_locality}, {p.city}"
                },

                {
                    "question": "How many parking spaces are available?",
                    "answer": f"{p.private_parking} parking spaces"
                },

            ]
        })

    # =========================================
    # PG
    # =========================================

    pg = PGColivingProperty.objects.filter(
        is_deleted=False
    )[:5]

    for p in pg:

        faq_sections.append({

            "title": p.pg_name,

            "category": "PG / Coliving",

            "faqs": [

                {
                    "question": "Where is this PG located?",
                    "answer": f"{p.locality}, {p.city}"
                },

                {
                    "question": "Is meal facility available?",
                    "answer": "Yes" if p.meals_available else "No"
                },

                {
                    "question": "What amenities are available?",
                    "answer": p.amenities
                },

                {
                    "question": "What is the minimum stay duration?",
                    "answer": f"{p.minimum_stay} months"
                },

            ]
        })

    return render(request, "home_page/property_faq.html", {
        "faq_sections": faq_sections
    })