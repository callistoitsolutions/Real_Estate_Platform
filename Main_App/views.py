
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

from collections import Counter
from Main_App.registry import PROPERTY_REGISTRY
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
from django.core.mail import send_mail


########### Crime Officer Views#######


from itertools import chain



from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.forms.models import model_to_dict
import json
from .apps import MainAppConfig
from datetime import datetime
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.utils.crypto import get_random_string
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.contenttypes.models import ContentType







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







import math
# =====================================================
# PROPERTY DETAIL VIEW
# =====================================================







########### Views start for ajax for send property enquiry ########################


@csrf_exempt
def Send_Property_Enquiry(request):
    if request.method == "POST":
        data = request.POST.dict()
        
        print("=" * 50)
        print("Send_Property_Enquiry called")
        print("Received data:", data)
        print("=" * 50)
        
        # 1. Extract Data
        property_id = data.get('property_id')
        listing_type = data.get('listing_type', '')
        category = data.get('category', '')
        country_code = data.get('country_code', '+91')
        whatsapp_consent = data.get('whatsapp_consent', 'no') == 'yes'
        
        # Get UTM parameters
        utm_source = data.get('utm_source', '').strip()
        utm_medium = data.get('utm_medium', '').strip()
        utm_campaign = data.get('utm_campaign', '').strip()
        utm_term = data.get('utm_term', '').strip()
        utm_content = data.get('utm_content', '').strip()
        utm_path = data.get('utm_path', '').strip()
        page_url = data.get('page_url', '').strip()
        

        # 2. Find the property
        real_property = None
        
        try:
            if listing_type == "rent" and category == "residential-data":
                real_property = RentalResidentialProperty.objects.get(id=property_id)
            elif listing_type == "rent" and category == "pg-data":
                real_property = PGColivingProperty.objects.get(id=property_id)
            elif listing_type == "rent" and category == "commercial-data":
                real_property = CommercialRentalProperty.objects.get(id=property_id)
            elif listing_type == "sale" and category == "resale-residential":
                real_property = ResaleResidentialProperty.objects.get(id=property_id)
            elif listing_type == "sale" and category == "commercial-resale":
                real_property = CommercialResaleProperty.objects.get(id=property_id)
            elif listing_type == "sale" and category == "plot-resale":
                real_property = PlotSaleProperty.objects.get(id=property_id)
            elif listing_type == "sale" and category == "industrial-resale":
                real_property = IndustrialResaleProperty.objects.get(id=property_id)
            elif listing_type == "sale" and category == "agricultural-data":
                real_property = AgriculturalResaleProperty.objects.get(id=property_id)
        except ObjectDoesNotExist:
            return JsonResponse({"status": "0", "msg": "Property not found."})
        
        if not real_property:
            return JsonResponse({"status": "0", "msg": "Invalid property type."})
        
        # 3. Get or Create UTMLink using get()
        property_content_type = ContentType.objects.get_for_model(real_property)
        utm_link = None
        
        if utm_source and utm_medium:
            try:
                # ✅ Try to get existing UTMLink
                utm_link = UTMLink.objects.get(
                    utm_source=utm_source,
                    utm_medium=utm_medium,
                    utm_campaign=utm_campaign if utm_campaign else '',
                    utm_term=utm_term if utm_term else '',
                    utm_content=utm_content if utm_content else '',
                    content_type=property_content_type,
                    object_id=real_property.id,
                    listing_type=listing_type,
                    category=category,
                )
                print(f"✅ Found existing UTMLink: {utm_link.link_id}")
            except UTMLink.DoesNotExist:
                # ✅ Create new UTMLink if not exists
                import uuid
                link_id = str(uuid.uuid4())[:8]
                property_title = getattr(real_property, 'title', None) or getattr(real_property, 'property_title', str(real_property))
                
                utm_link = UTMLink.objects.create(
                    link_id=link_id,
                    content_type=property_content_type,
                    object_id=real_property.id,
                    property_title=property_title,
                    listing_type=listing_type,
                    category=category,
                    utm_path=utm_path or f"/listing/{listing_type}/{category}/{property_id}/",
                    utm_url=page_url,
                    utm_source=utm_source,
                    utm_medium=utm_medium,
                    utm_campaign=utm_campaign,
                    utm_term=utm_term,
                    utm_content=utm_content,
                    total_clicks=0,
                    total_enquiries=0
                )
                print(f"✅ Created new UTMLink: {utm_link.link_id}")
            except UTMLink.MultipleObjectsReturned:
                # If multiple found, get the first one (should not happen with unique_together)
                utm_link = UTMLink.objects.filter(
                    utm_source=utm_source,
                    utm_medium=utm_medium,
                    content_type=property_content_type,
                    object_id=real_property.id,
                ).first()
                print(f"⚠️ Multiple UTMLinks found, using first: {utm_link.link_id}")
        
        # 4. Save Enquiry with ONLY utm_link foreign key
        try:
            enquiry = PropertyEnquiry.objects.create(
                content_type=property_content_type,
                object_id=real_property.id,
                enquiry_name=data.get('enquiry_name', '').strip(),
                country_code=country_code,
                enquiry_phone=data.get('enquiry_phone', '').strip(),
                whatsapp_consent=whatsapp_consent,
                utm_link=utm_link,  # ✅ Only the foreign key
                enquiry_date=datetime.now().date(),
                enquiry_time=datetime.now().time()
            )
            
            print(f"✅ Enquiry saved - ID: {enquiry.id}")
            
            if utm_link:
                print(f"   ✅ Linked to UTMLink: {utm_link.link_id}")
                utm_link.total_enquiries = models.F('total_enquiries') + 1
                utm_link.save()
                print(f"   UTMLink total enquiries: {utm_link.total_enquiries + 1}")
            else:
                print(f"⚠️ No UTM tracking for this enquiry")
            
            return JsonResponse({
                "status": "1", 
                "msg": "Enquiry submitted successfully!"
            })
            
        except Exception as e:
            print(f"❌ Error: {e}")
            return JsonResponse({
                "status": "0", 
                "msg": "Could not save enquiry. Please try again."
            })
    
    return JsonResponse({"status": "0", "msg": "Invalid request."})
    

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



def extract_entities(query):
    # Sends the fuzzy-corrected text straight to the Sentence Transformer
    return query








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





import json
import math
import uuid
from datetime import date

from django.shortcuts import render, get_object_or_404
from django.utils.timezone import now



# ════════════════════════════════════════════════════════════
#  SAFE GLOBAL UTILITIES
# ════════════════════════════════════════════════════════════

def _safe_parse_list(val):
    """
    Safely convert a DB value → plain Python list of strings.
    Handles: None, list, JSON-string ('[...]'), comma-separated string.
    """
    if not val:
        return []
    if isinstance(val, list):
        return [str(x).strip() for x in val if x]
    if isinstance(val, str):
        val = val.strip()
        if val.startswith('['):
            try:
                parsed = json.loads(val)
                if isinstance(parsed, list):
                    return [str(x).strip() for x in parsed if x]
            except (ValueError, json.JSONDecodeError):
                pass
        return [x.strip() for x in val.split(',') if x.strip()]
    return []


def _safe_bool_field(obj, *attrs):
    """
    Return True if any of the given attribute names on obj
    is truthy or equals the strings 'yes' / 'true' / '1'.
    """
    for attr in attrs:
        v = getattr(obj, attr, None)
        if v is None:
            continue
        if isinstance(v, bool):
            return v
        if str(v).lower() in ('yes', 'true', '1'):
            return True
    return False


def _safe_parse_pg_room_prices(pg_obj):
    """
    Read PGRoomDetail rows and return a dict of
    { single_sharing, double_sharing, triple_sharing,
      four_sharing, five_sharing, six_sharing }
    mapped to their room_rent values (or None).
    """
    price_map = {
        'single': 'single_sharing',
        'double': 'double_sharing',
        'triple': 'triple_sharing',
        '4':      'four_sharing',
        '5':      'five_sharing',
        '6':      'six_sharing',
    }
    result = {v: None for v in price_map.values()}

    try:
        for room in pg_obj.rooms.all():
            rtype = str(room.room_type).lower().strip()
            for key, field in price_map.items():
                if key in rtype:
                    try:
                        result[field] = float(room.room_rent)
                    except (ValueError, TypeError):
                        pass
                    break
    except Exception:
        pass
    return result


def _safe_get_pg_min_price(pg_obj):
    """Return the minimum room_rent across all PGRoomDetail rows, or None."""
    try:
        rents = [float(r.room_rent) for r in pg_obj.rooms.all() if r.room_rent]
        return min(rents) if rents else None
    except Exception:
        return None


# ════════════════════════════════════════════════════════════
#  MAIN VIEW
# ════════════════════════════════════════════════════════════


def property_detail_view(request, listing_type, category, pk, slug=None):
    
    # ── 1. Identify the correct model ───────────────────────
        # ── 1. Identify the correct model ───────────────────────
    property_model = None
    seo_page_type  = ''
    sub_category   = None   # not currently passed via URL; defaulting to avoid NameError

    clean_category = str(category).lower().strip()
    clean_type = str(listing_type).lower().strip()


    

    if clean_type == 'rent':
        if clean_category in ('residential', 'residential-data'):
            from .models import RentalResidentialProperty
            property_model = RentalResidentialProperty
            seo_page_type  = 'rental_residential'
        elif clean_category in ('commercial', 'commercial-data'):
            from .models import CommercialRentalProperty
            property_model = CommercialRentalProperty
            seo_page_type  = 'commercial_rental'
        elif clean_category in ('pg', 'pg-data', 'pg-coliving'):
            from .models import PGColivingProperty
            property_model = PGColivingProperty
            seo_page_type  = 'pg_coliving'

    elif clean_type == 'sale':
        if clean_category in ('residential', 'resale-residential'):
            from .models import ResaleResidentialProperty
            property_model = ResaleResidentialProperty
            seo_page_type  = 'resale_residential'
        elif clean_category in ('commercial', 'commercial-resale'):
            from .models import CommercialResaleProperty
            property_model = CommercialResaleProperty
            seo_page_type  = 'commercial_resale'
        elif clean_category in ('industrial', 'industrial-resale'):
            from .models import IndustrialResaleProperty
            property_model = IndustrialResaleProperty
            seo_page_type  = 'industrial_sale'
        elif clean_category in ('agriculture', 'agricultural-data', 'agricultural-resale'):
            from .models import AgriculturalResaleProperty
            property_model = AgriculturalResaleProperty
            seo_page_type  = 'agriculture_sale'
        elif clean_category in ('plot', 'plot-resale'):
            # INTEGRATING THE 4 NEW PLOT MODELS
            from .models import AgriculturalPlotResaleProperty, ResidentialPlotResaleProperty, CommercialPlotResaleProperty, IndustrialPlotResaleProperty
            if str(pk).startswith('EFAPR'):
                property_model = AgriculturalPlotResaleProperty
                seo_page_type  = 'agricultural_plot_sale'
            elif ResidentialPlotResaleProperty.objects.filter(pk=pk).exists():
                property_model = ResidentialPlotResaleProperty
                seo_page_type  = 'residential_plot_sale'
            elif CommercialPlotResaleProperty.objects.filter(pk=pk).exists():
                property_model = CommercialPlotResaleProperty
                seo_page_type  = 'commercial_plot_sale'
            elif IndustrialPlotResaleProperty.objects.filter(pk=pk).exists():
                property_model = IndustrialPlotResaleProperty
                seo_page_type  = 'industrial_plot_sale'
            elif AgriculturalPlotResaleProperty.objects.filter(pk=pk).exists():
                property_model = AgriculturalPlotResaleProperty
                seo_page_type  = 'agricultural_plot_sale'

    if not property_model:
        return render(request, 'home_page/property_not_found.html', {
            'listing_type': listing_type,
            'category': category,
            'sub_category': sub_category,
        })

    # ── Derive property_group for template gating ──
    if clean_type == 'rent':
        property_group = 'rental'
    elif clean_category in ('plot', 'plot-resale'):
        property_group = 'resale_plot'
    else:
        property_group = 'resale'

    # ── 2. Fetch the object ──────────────────────────────────
    obj = get_object_or_404(property_model, pk=pk)

    from collections import defaultdict
    p = defaultdict(lambda: None)   # missing keys resolve to None instead of raising in templates

    # ════════════════════════════════════════════════════════
    # STEP 1 FIELDS — Basic Information
    # ════════════════════════════════════════════════════════

    p['id'] = obj.pk

    p['title'] = (
        getattr(obj, 'title',          None) or   
        getattr(obj, 'property_title', None) or   
        getattr(obj, 'plot_title',     None) or   
        getattr(obj, 'pg_name',        None) or
        getattr(obj, 'building_name',  None) or
        'Property Details'
    )

    # ════════════════════════════════════════════════════════
# DIRECT PASSTHROUGH FIELDS — needed by the unified template,
# not already computed above via priority chains.
# ════════════════════════════════════════════════════════
    _direct_fields = [
    'property_type', 'property_no', 'wing_number', 'wing_no', 'building_configuration', 'residential_zone_type' , 'na_status' , 'layout_approval_status',
    'total_floors', 'facing_direction', 'furnishing_status', 'furnishing_type', 'gated_community' , 'layout_name' , 'plot_facing' , 'plot_fencing' , 'commercial_zone_type' ,
    'occupancy_status', 'floor_no', 'floor_number', 'society_type', 'water_type','city_zone' , 'availability_status' ,'land_area' ,
    'ownership_type' , 'locality_area' , 'property_landmark' , 'latitude' , 'longitude' , 'google_maps_link' , 'builtup_area' ,
    'property_category', 'zone_type', 'location_hub', 'property_condition', 'property_age', 'builtup_area' , 'main_road_connectivity' ,
    'super_builtup_area', 'no_staircases', 'num_cabins',
    'user_description', 'property_summary', 'property_description',
    'ownership_status', 'ownership_document_type', 'title_clarity_status',
    'encumbrance_status', 'property_loan', 'existing_tenants', 'any_legal_dispute',
    'government_tax', 'sanctioning_authority', 'no_of_owners', 'loan_amount',
    'pending_tax_amount', 'tenant_details', 'dispute_details',
    'selling_price', 'price_per_sqft', 'price_negotiable', 'brokerage_percentage',
    'manual_brokerage',
    'advanced_rent_type', 'advanced_rent_amount', 'security_deposit_type',
    'security_deposit_amount', 'maintenance_charges', 'negotiable', 'lockin_period',
    'rent_increase', 'total_move_in_cost',
    'room_type', 'advance_rent_month',
    'opposite_gender_visitors_allowed', 'visitors_allowed', 'curfew_time',
    'smoking_allowed', 'alcohol_consumption_allowed', 'couples_allowed',
    'pets_allowed', 'cooking_allowed', 'police_verification_required',
    'best_suited_for', 'property_managed_by', 'manager_stays',
    'kva_capacity', 'water_supply', 'truck_accessibility', 'loading_dock',
    'floor_load_capacity', 'factory_license_status', 'fire_noc_status',
    'pollution_control_approval', 'title_status', 'legal_dispute', 'tax_amount',
    'cultivation_status', 'fertility_status', 'nos_borewells', 'dist_main_road',
    'fencing_status', 'possession_status', 'seven_twelve_available', 'agri_dispute',
    'land_conversion_status', 'road_connectivity', 'main_road_connectivity',
    ]
    for _f in _direct_fields:
        if not p.get(_f):
            p[_f] = getattr(obj, _f, None)
    

    CATEGORY_BY_SEO_TYPE = {
        'rental_residential':     'Residential',
        'commercial_rental':      'Commercial',
        'pg_coliving':            'PG / Co-living',

        'resale_residential':     'Residential',
        'commercial_resale':      'Commercial',
        'industrial_sale':        'Industrial',
        'agriculture_sale':       'Agriculture',

        'agricultural_plot_sale': 'Plot',
        'residential_plot_sale':  'Plot',
        'commercial_plot_sale':   'Plot',
        'industrial_plot_sale':   'Plot',
    }

    SUBCATEGORY_BY_SEO_TYPE = {
        'agricultural_plot_sale': 'Agricultural Plot',
        'residential_plot_sale':  'Residential Plot',
        'commercial_plot_sale':   'Commercial Plot',
        'industrial_plot_sale':   'Industrial Plot',
        # everything else has no sub_category — stays None
    }

    p['category']          = CATEGORY_BY_SEO_TYPE.get(seo_page_type, category.title())
    p['category_name']     = p['category']
    p['sub_category_name'] = SUBCATEGORY_BY_SEO_TYPE.get(seo_page_type)  # None for non-plot listings

    # ── Property purpose / availability flags ────────────────
    p['property_purpose']    = getattr(obj, 'property_purpose',  None)
    p['renting_option']      = getattr(obj, 'renting_option',    None)
    p['available_for']       = getattr(obj, 'available_for',     None)
    p['construction_status'] = getattr(obj, 'construction_status', None)
    p['possession']          = getattr(obj, 'possession_status', None)
    p['available_from']      = getattr(obj, 'available_from',    None)

    # City lookup fallback layout sequence
    p['city'] = (
        getattr(obj, 'city',      None) or
        getattr(obj, 'plot_city', None) or
        ''
    )

    # Locality setup sequence
    p['locality'] = (
        getattr(obj, 'locality',      None) or   
        getattr(obj, 'locality_area',  None) or 
        getattr(obj, 'plot_locality', None) or   
        getattr(obj, 'village',       None) or   
        ''
    )

    # Full address routing fields
    p['address'] = (
        getattr(obj, 'complete_address', None) or   
        getattr(obj, 'property_address', None) or   
        getattr(obj, 'address',          None) or   
        getattr(obj, 'plot_address',     None) or   
        ''
    )

    p['building_name'] = getattr(obj, 'building_name', None)
    p['pincode']       = getattr(obj, 'pincode', '')

    # Agriculture specific fields configuration
    p['state']    = getattr(obj, 'state',    None)
    p['district'] = getattr(obj, 'district', None)
    p['taluka']   = getattr(obj, 'taluka',    None)
    p['village']  = getattr(obj, 'village',  None)

    # Commercial/Resale configurations
    p['zone']         = getattr(obj, 'zone',         None)  
    p['zone_type']    = getattr(obj, 'zone_type',    None)  
    p['location_hub'] = getattr(obj, 'location_hub', None)  
    p['society_type'] = getattr(obj, 'society_type', None)  
    p['water_type']   = getattr(obj, 'water_type',   None)  

    p['property_condition'] = getattr(obj, 'property_condition', None)
    p['age'] = getattr(obj, 'age_of_property', getattr(obj, 'property_age', None))

    # Ownership structural elements mapping
    p['ownership'] = (
        getattr(obj, 'ownership_type', None) or  
        getattr(obj, 'plot_ownership', None)     
    )
    p['num_owners'] = getattr(obj, 'num_owners', None)

    p['residential_status'] = (
        getattr(obj, 'residential_status', None) or
        getattr(obj, 'comm_residency',     None) or
        getattr(obj, 'residency_status',   None)
    )

    # ════════════════════════════════════════════════════════
    # NEW PLOT SPECIFIC METRICS EXTRACTOR (MAPPED FULLY)
    # ════════════════════════════════════════════════════════
    p['property_no'] = getattr(obj, 'property_no', None)
    p['land_use'] = getattr(obj, 'land_use', None)
    p['na_status'] = getattr(obj, 'na_status', None)
    p['layout_approval_status'] = getattr(obj, 'layout_approval_status', None)
    
    p['plot_frontage'] = getattr(obj, 'plot_frontage', None)
    p['plot_depth'] = getattr(obj, 'plot_depth', None)
    p['plot_shape'] = getattr(obj, 'plot_shape', None)
    p['road_width'] = getattr(obj, 'road_width', None)
    p['corner_plot'] = getattr(obj, 'corner_plot', None)
    p['current_possession_status'] = getattr(obj, 'current_possession_status', None)
    p['additional_charges'] = getattr(obj, 'additional_charges', None)
    
    p['ownership_document_type'] = getattr(obj, 'ownership_document_type', None)
    p['other_document_type'] = getattr(obj, 'other_document_type', None)
    p['rera_status'] = getattr(obj, 'rera_status', None)
    p['title_clearance'] = getattr(obj, 'title_clearance', None)
    p['property_encumbrance_status'] = getattr(obj, 'property_encumbrance_status', getattr(obj, 'encumbrance_status', None))
    p['property_tax_status'] = getattr(obj, 'property_tax_status', getattr(obj, 'government_tax', None))
    p['outstanding_tax_amount'] = getattr(obj, 'outstanding_tax_amount', getattr(obj, 'pending_tax_amount', getattr(obj, 'tax_amount', None)))
    p['pending_since'] = getattr(obj, 'pending_since', None)
    p['property_loan_status'] = getattr(obj, 'property_loan_status', getattr(obj, 'property_loan', None))
    p['financing_bank'] = getattr(obj, 'financing_bank', None)
    p['outstanding_loan_amount'] = getattr(obj, 'outstanding_loan_amount', getattr(obj, 'loan_amount', getattr(obj, 'plot_loan_amount', None)))

    # Residential Plot Specifics
    p['residential_zone_type'] = getattr(obj, 'residential_zone_type', None)
    p['gated_community'] = getattr(obj, 'gated_community', None)
    p['layout_name'] = getattr(obj, 'layout_name', None)

    # Commercial Plot Specifics
    p['commercial_zone_type'] = getattr(obj, 'commercial_zone_type', None)
    p['permissible_fsi'] = getattr(obj, 'permissible_fsi', getattr(obj, 'industrial_fsi', None))
    p['ground_coverage'] = getattr(obj, 'ground_coverage', None)
    p['plot_visibility'] = getattr(obj, 'plot_visibility', None)
    p['proposed_use'] = getattr(obj, 'proposed_use', None)
    p['parking_availability'] = getattr(obj, 'parking_availability', None)

    # Industrial Plot Specifics
    p['industrial_zone_type'] = getattr(obj, 'industrial_zone_type', None)
    p['industrial_estate_name'] = getattr(obj, 'industrial_estate_name', None)
    p['industrial_fsi'] = getattr(obj, 'industrial_fsi', None)
    p['power_load_kva'] = getattr(obj, 'power_load_kva', None)
    p['industrial_water_supply'] = getattr(obj, 'industrial_water_supply', None)
    p['effluent_treatment'] = getattr(obj, 'effluent_treatment', None)
    p['industry_type_permissible'] = getattr(obj, 'industry_type_permissible', None)
    p['midc_allotment'] = getattr(obj, 'midc_allotment', None)
    p['midc_transfer_noc'] = getattr(obj, 'midc_transfer_noc', None)
    p['environmental_clearance'] = getattr(obj, 'environmental_clearance', None)

    # Agricultural Plot Specifics
    p['agr_area_unit'] = getattr(obj, 'agr_area_unit', None)
    p['current_crop'] = getattr(obj, 'current_crop', None)
    p['irrigation_source'] = getattr(obj, 'irrigation_source', None)
    p['agr_electricity'] = getattr(obj, 'agr_electricity', None)
    p['highway_distance'] = getattr(obj, 'highway_distance', None)
    p['land_topography'] = getattr(obj, 'land_topography', None)
    p['govt_scheme'] = getattr(obj, 'govt_scheme', None)
    p['satbara_available'] = getattr(obj, 'satbara_available', None)
    p['khate_utara'] = getattr(obj, 'khate_utara', None)
    p['section63_clearance'] = getattr(obj, 'section63_clearance', None)
    p['land_conversion_status'] = getattr(obj, 'land_conversion_status', None)

    # ════════════════════════════════════════════════════════
    # STEP 1 FIELDS — Configuration (Residential only)
    # ════════════════════════════════════════════════════════

    p['bhk']      = getattr(obj, 'bhk',      None)
    p['bhk_type'] = getattr(obj, 'bhk_type', None)
    p['beds']     = p['bhk'] or p['bhk_type']

    p['bathrooms'] = getattr(obj, 'bathrooms', None)
    p['baths']     = getattr(obj, 'baths', p['bathrooms'])

    p['balconies'] = getattr(obj, 'balconies', None)

    p['covered_parking'] = getattr(obj, 'covered_parking', None)
    p['open_parking']    = getattr(obj, 'open_parking',    None)
    p['private_parking'] = getattr(obj, 'private_parking', None)
    p['public_parking']  = getattr(obj, 'public_parking',  None)

    p['floor'] = (
        getattr(obj, 'floor_number', None) or
        getattr(obj, 'floor_no',     None) or
        getattr(obj, 'your_floor',   None)
    )
    p['total_floors'] = getattr(obj, 'total_floors', None)
    p['facing'] = getattr(obj, 'facing', getattr(obj, 'plot_road_facing', None))

    # ════════════════════════════════════════════════════════
    # AREA SPECIFICATION ENGINE
    # ════════════════════════════════════════════════════════

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

    # ════════════════════════════════════════════════════════
    # STEP 2 FIELDS — Pricing
    # ════════════════════════════════════════════════════════

    p['furnished'] = (
        getattr(obj, 'furnishing_status', None) or
        getattr(obj, 'furnishing_type',   None) or
        getattr(obj, 'furnished',         None)
    )

    p['monthly_rent'] = (
        getattr(obj, 'monthly_rent',   None) or
        getattr(obj, 'expected_rent',  None)
    )
    p['security_deposit'] = getattr(obj, 'security_deposit', None)
    p['maintenance']      = (
        getattr(obj, 'maintenance_amount',  None) or
        getattr(obj, 'maintenance_charges', None)
    )
    p['maintenance_type'] = getattr(obj, 'maintenance_type', None)
    p['negotiable']       = getattr(obj, 'negotiable',    None)
    p['is_negotiable']    = getattr(obj, 'is_negotiable', None)

    # ADDED selling_price fallback to support the 4 new resale plot models
    raw_price = (
        getattr(obj, 'selling_price',  None) or
        getattr(obj, 'expected_price', None) or   
        getattr(obj, 'plot_price',     None) or   
        p['monthly_rent']                                          
    )

    def _safe_get_pg_min_price(o):
        try:
            return o.monthly_rent
        except:
            return None

    def _safe_parse_pg_room_prices(o):
        return {}

    if seo_page_type == 'pg_coliving':
        pg_prices = _safe_parse_pg_room_prices(obj)
        p.update(pg_prices)
        bed_prices = [v for v in pg_prices.values() if v]
        if bed_prices:
            p['monthly_rent'] = min(bed_prices)
            raw_price         = p['monthly_rent']
        else:
            pg_min = _safe_get_pg_min_price(obj)
            if pg_min:
                p['monthly_rent'] = pg_min
                raw_price         = pg_min

    p['raw_price']      = raw_price or 0
    p['expected_price'] = raw_price or 0

    try:
        price_f = float(raw_price) if raw_price else 0
        p['price_display'] = f"₹{price_f:,.0f}" if price_f > 0 else 'Price on Request'
    except Exception:
        p['price_display'] = str(raw_price) if raw_price else 'Price on Request'

    # ADDED plot_price_per_sqft and price_per_unit fallbacks
    p['price_sqft'] = (
        getattr(obj, 'price_per_sqft', None) or 
        getattr(obj, 'plot_price_per_sqft', None) or 
        getattr(obj, 'price_per_unit', None)
    )

    b_flag = str(getattr(obj, 'brokerage', '')).lower()
    p['brokerage'] = None
    if b_flag in ('yes', 'true', '1'):
        p['brokerage'] = (
            getattr(obj, 'brokerage_percentage', None) or
            getattr(obj, 'manual_brokerage',     None) or
            'Applicable'
        )

    p['lockin_period']  = getattr(obj, 'lockin_period',  None)
    p['rent_increase']  = getattr(obj, 'rent_increase',  None)
    p['lease_duration'] = getattr(obj, 'lease_duration', None)
    p['minimum_stay']   = getattr(obj, 'minimum_stay',   None)
    p['notice_period']  = getattr(obj, 'notice_period',  None)

    # ── SIDEBAR: Deposit / Advance / Maintenance display computation ──
    def _compute_multiplier_amount(type_val, amount_val, rent_val):
        if amount_val:
            try:
                return float(amount_val), None
            except (TypeError, ValueError):
                return amount_val, None
        if type_val in (None, ''):
            return None, None
        try:
            months = int(float(type_val))
            if 0 < months <= 12 and rent_val:
                return months * float(rent_val), months
        except (TypeError, ValueError):
            pass
        return type_val, None

    _rent_base = p['monthly_rent'] or 0

    import re

    def _compute_multiplier_amount_v2(type_val, amount_val, rent_val):
        """Returns (display_amount, months_or_None, is_fixed_bool)"""
        type_str = str(type_val).strip() if type_val else ''
        rent_float = 0
        try:
            rent_float = float(rent_val) if rent_val else 0
        except (TypeError, ValueError):
            rent_float = 0

        # Case 1: Fixed string
        if type_str.lower() in ('fixed', 'fixed amount', 'fixed_amount', 'manual'):
            try:
                return float(amount_val), None, True
            except (TypeError, ValueError):
                return amount_val or 'Price on Request', None, True

        # Case 2: Multiplier (e.g., "2 Months")
        match = re.search(r'^(\d+)', type_str)
        if match:
            months = int(match.group(1))
            if 0 < months <= 24 and rent_float > 0:
                return (months * rent_float), months, False
            elif amount_val:
                try:
                    return float(amount_val), None, True
                except:
                    pass
        
        # Case 3: Amount provided directly
        if amount_val:
            try:
                return float(amount_val), None, True
            except:
                return amount_val, None, True

        return type_str or amount_val, None, True

    _dep_amt, _dep_months, _dep_is_fixed = _compute_multiplier_amount_v2(
        p.get('security_deposit_type'),
        p.get('security_deposit_amount') or p.get('security_deposit'),
        _rent_base
    )
    p['deposit_display']  = _dep_amt
    p['deposit_months']   = _dep_months
    p['deposit_is_fixed'] = _dep_is_fixed

    _adv_amt, _adv_months, _adv_is_fixed = _compute_multiplier_amount_v2(
        p.get('advance_rent_month') or p.get('advanced_rent_type'),
        p.get('advanced_rent_amount'),
        _rent_base
    )
    p['advance_display']  = _adv_amt
    p['advance_months']   = _adv_months
    p['advance_is_fixed'] = _adv_is_fixed

    maint_type = str(p.get('maintenance_type') or '').lower()
    if maint_type in ('included', 'in rent', 'yes'):
        p['maintenance_display'] = 'Included'
        p['maintenance_note']    = 'In Rent'
    else:
        maint_amt = p.get('maintenance_amount') or p.get('maintenance_charges') or p.get('maintenance')
        p['maintenance_display'] = maint_amt if maint_amt else None
        p['maintenance_note']    = p.get('maintenance_type') or 'Extra'

    # ════════════════════════════════════════════════════════
    # COMMERCIAL METRICS EXTRACTOR
    # ════════════════════════════════════════════════════════

    p['min_seats']        = getattr(obj, 'min_seats',       None)
    p['max_seats']        = getattr(obj, 'max_seats',       None)
    p['cabins']           = getattr(obj, 'cabins',  getattr(obj, 'num_cabins', None))
    p['meeting_rooms']    = getattr(obj, 'meeting_rooms',   None)
    p['passenger_lifts']  = getattr(obj, 'passenger_lifts', None)
    p['service_lifts']    = getattr(obj, 'service_lifts',   None)
    p['private_washroom'] = getattr(obj, 'private_washroom', None)
    p['public_washroom']  = getattr(obj, 'public_washroom',  None)
    p['staircases']       = getattr(obj, 'staircases', getattr(obj, 'num_staircases', None))
    p['flooring_type']    = getattr(obj, 'flooring_type',   None)

    p['dg_ups_included']     = getattr(obj, 'dg_ups_included',     False)
    p['electricity_included'] = getattr(obj, 'electricity_included', False)
    p['water_included']       = getattr(obj, 'water_included',       False)

    # ════════════════════════════════════════════════════════
    # PG DETAILS CONFIGURATION
    # ════════════════════════════════════════════════════════

    p['total_beds']          = getattr(obj, 'total_beds',           None)
    p['sharing_type']        = getattr(obj, 'sharing_type',         None)
    p['pg_for']              = getattr(obj, 'pg_for', getattr(obj, 'best_suited_for', None))
    p['meals_available']     = getattr(obj, 'meals_available',      False)
    p['meal_offerings']      = getattr(obj, 'meal_offerings',       None)
    p['meal_speciality']     = getattr(obj, 'meal_speciality',      None)
    p['property_managed_by'] = getattr(obj, 'property_managed_by',  None)
    p['manager_stays']       = getattr(obj, 'manager_stays',        False)
    p['room_details']        = getattr(obj, 'room_details',         None)
    p['common_area']         = getattr(obj, 'common_area',          None)

    p['opposite_sex_allowed'] = getattr(obj, 'opposite_sex_allowed', False)
    p['any_time_allowed']     = getattr(obj, 'any_time_allowed',     False)
    p['visitors_allowed']     = getattr(obj, 'visitors_allowed',     False)
    p['guardian_allowed']     = getattr(obj, 'guardian_allowed',     False)
    p['drinking_allowed']     = getattr(obj, 'drinking_allowed',     False)
    p['smoking_allowed']      = getattr(obj, 'smoking_allowed',      False)
    p['non_veg_allowed']      = getattr(obj, 'non_veg_allowed',      False)

    def _safe_bool_field(o, *attrs):
        for a in attrs:
            val = getattr(o, a, None)
            if val is not None:
                if isinstance(val, bool):
                    return val
                return str(val).lower() in ['yes', 'true', '1']
        return False

    # ── Safe execution of helpers using scope protected unique calls ──
    p['plot_corner']           = _safe_bool_field(obj, 'plot_corner', 'corner_plot')
    p['plot_fencing']          = _safe_bool_field(obj, 'plot_fencing')
    p['plot_road_facing']      = getattr(obj, 'plot_road_facing', None)
    p['sanctioning_authority'] = (
        getattr(obj, 'sanctioning_authority', None) or
        getattr(obj, 'plot_authority',        None)
    )

    p['power_supply']          = getattr(obj, 'power_supply',          None)
    p['power_kva']              = getattr(obj, 'kva_capacity',          None)
    p['water_supply']          = getattr(obj, 'water_supply',          None)
    p['crane_heavy_machinery'] = getattr(obj, 'crane_heavy_machinery', False)
    p['road_connectivity']     = getattr(obj, 'road_connectivity',     None)
    p['worker_housing_nearby'] = getattr(obj, 'worker_housing_nearby', False)

    p['soil_type']           = getattr(obj, 'soil_type',          None)
    p['water_source']        = getattr(obj, 'water_source',       None)
    p['irrigation_facility'] = getattr(obj, 'irrigation_facility', None)
    p['fertility_status']    = getattr(obj, 'fertility_status',   None)
    p['previous_crops']      = getattr(obj, 'previous_crops',     None)

    # ════════════════════════════════════════════════════════
    # STEP 2 FIELDS — Legal & Compliance
    # ════════════════════════════════════════════════════════

    p['has_loan']    = _safe_bool_field(obj, 'has_loan', 'plot_loan', 'agri_loan', 'loan_on_property', 'property_loan_status', 'property_loan')
    p['loan_amount'] = (
        getattr(obj, 'loan_amount',             None) or
        getattr(obj, 'plot_loan_amount',        None) or
        getattr(obj, 'outstanding_loan_amount', None)
    )

    p['has_dispute']     = _safe_bool_field(obj, 'has_legal_dispute', 'legal_dispute', 'agri_dispute')
    p['dispute_details'] = getattr(obj, 'dispute_details', None)

    p['has_tax_due'] = _safe_bool_field(obj, 'has_tax_due', 'tax_due', 'agri_tax_due', 'pending_tax_due')
    p['tax_amount']  = (
        getattr(obj, 'pending_tax_amount',     None) or
        getattr(obj, 'tax_amount',             None) or
        getattr(obj, 'outstanding_tax_amount', None)
    )

    p['has_tenants']    = _safe_bool_field(obj, 'has_tenants', 'existing_tenants', 'agri_tenants')
    p['tenant_details'] = getattr(obj, 'tenant_details', None)

    p['fire_noc']            = getattr(obj, 'fire_noc',            None)
    p['tax_clearance_cert']  = getattr(obj, 'tax_clearance_cert',  False)
    p['encumbrance_cert']    = getattr(obj, 'encumbrance_cert',    None)
    p['compliance_docs']     = getattr(obj, 'compliance_docs',     None)

    # ════════════════════════════════════════════════════════
    # PARSE AMENITIES & DATA LAYOUT STRUCT
    # ════════════════════════════════════════════════════════

    def _safe_parse_list(val):
        if not val:
            return []
        if isinstance(val, list):
            return [str(v).strip() for v in val if v]
        val = str(val).replace('[', '').replace(']', '').replace("'", '').replace('"', '')
        if ',' in val:
            return [v.strip() for v in val.split(',') if v.strip()]
        return [val.strip()]

    amenities_list  = _safe_parse_list(getattr(obj, 'amenities',         ''))
    facilities_list = _safe_parse_list(getattr(obj, 'nearby_facilities', getattr(obj, 'facilities', '')))

    if p.get('dg_ups_included'):      amenities_list.append('DG / UPS Backup')
    if p.get('electricity_included'): amenities_list.append('Electricity Included')
    if p.get('water_included'):       amenities_list.append('Water Included')


    p['description'] = getattr(obj, 'description', None)
    p['rent_residential_desc'] = getattr(obj, 'rent_residential_desc', None)
    p['desc'] = (
        getattr(obj, 'description',              None) or   
        getattr(obj, 'property_description',     None) or   
        getattr(obj, 'rent_residential_desc',    None) or   
        getattr(obj, 'resale_agricultural_desc', None) or   
        getattr(obj, 'pg_description',           None) or   
        ''
    )

    # ════════════════════════════════════════════════════════
    # STEP 4 FIELDS — Media portfolio mappings
    # ════════════════════════════════════════════════════════

    p['video'] = (
        getattr(obj, 'property_video', None) or 
        getattr(obj, 'video',          None) or 
        getattr(obj, 'social_video',   None)     
    )

    p['floor_plan'] = getattr(obj, 'floor_plan', getattr(obj, 'layout_plan', None))

    p['owner_name'] = (
        getattr(obj, 'owner_name',      None) or
        getattr(obj, 'plot_owner_name', None) or
        'Property Owner'
    )
    p['owner_contact'] = (
        getattr(obj, 'contact_number',     None) or   
        getattr(obj, 'owner_contact',      None) or   
        getattr(obj, 'plot_owner_contact', None)      
    )
    p['owner_email'] = (
        getattr(obj, 'email',              None) or    
        getattr(obj, 'owner_email',        None) or    
        getattr(obj, 'plot_owner_email',  None)       
    )
    p['alternate_contact'] = getattr(obj, 'alternate_contact', None)

    p['uploaded_by_name']    = getattr(obj, 'uploaded_by_name',    None)
    p['uploaded_by_email']   = getattr(obj, 'uploaded_by_email',   None)
    p['uploaded_by_contact'] = getattr(obj, 'uploaded_by_contact', None)
    p['uploaded_by_role']    = getattr(obj, 'uploaded_by_role',    'Owner')

    property_images = []
    if hasattr(obj, 'images'):
        property_images = list(obj.images.all())


     # ════════════════════════════════════════════════════════
# IMAGE CATEGORY GROUPING (for lightbox category tabs)
# ════════════════════════════════════════════════════════
    grouped_images = {}
    for img in property_images:
        cat_key = getattr(img, 'category', 'others') or 'others'
        cat_label = img.get_category_display() if hasattr(img, 'get_category_display') else cat_key.replace('_', ' ').title()
        grouped_images.setdefault(cat_key, {'label': cat_label, 'images': []})
        grouped_images[cat_key]['images'].append(img)
    # ════════════════════════════════════════════════════════
# VIDEO RESOLUTION (RM Assisted Link > Manually Uploaded > Auto)
# ════════════════════════════════════════════════════════
    selected_video = None
    video_qs = None
    for rel_name in ('video', 'videos', 'walkthrough_video'):
        mgr = getattr(obj, rel_name, None)
        if mgr is not None and hasattr(mgr, 'all'):
            video_qs = mgr.all()
            break

    if video_qs is not None:
        priority = {'rm_assisted': 0, 'uploaded': 1, 'auto': 2}
        videos = sorted(video_qs, key=lambda v: priority.get(getattr(v, 'source', 'auto'), 3))
        for v in videos:
            if getattr(v, 'source', None) == 'rm_assisted' and getattr(v, 'video_url', None):
                selected_video = v
                break
            if getattr(v, 'video', None):
                selected_video = v
                break
        if not selected_video and videos:
            selected_video = videos[0]

    # ════════════════════════════════════════════════════════
    # MORTGAGE CALCULATOR
    # ════════════════════════════════════════════════════════

    base_emi = 0
    if clean_type == 'sale' and p['raw_price']:
        try:
            principal = float(p['raw_price']) * 0.80
            r         = 8.5 / 12 / 100
            n         = 20 * 12
            base_emi  = int(
                (principal * r * math.pow(1 + r, n)) /
                (math.pow(1 + r, n) - 1)
            )
        except Exception:
            base_emi = 0

    # ════════════════════════════════════════════════════════
    # NEIGHBORHOOD MAP COMPILATION
    # ════════════════════════════════════════════════════════

    similar = []
    try:
        city_val = p['city']
        similar_qs = property_model.objects.filter(is_deleted=False).exclude(pk=obj.pk)

        if city_val:
            if hasattr(property_model, 'city'):
                similar_qs = similar_qs.filter(city__icontains=city_val)
            elif hasattr(property_model, 'plot_city'):
                similar_qs = similar_qs.filter(plot_city__icontains=city_val)

        for s_obj in similar_qs[:3]:
            s_raw = (
                getattr(s_obj, 'selling_price',  None) or
                getattr(s_obj, 'expected_price', None) or
                getattr(s_obj, 'plot_price',     None) or
                getattr(s_obj, 'monthly_rent',   None) or
                getattr(s_obj, 'expected_rent',  None)
            )
            if seo_page_type == 'pg_coliving' and not s_raw:
                s_raw = _safe_get_pg_min_price(s_obj)

            try:
                s_price_str = f"₹{float(s_raw):,.0f}" if s_raw else 'Ask Price'
            except Exception:
                s_price_str = 'Ask Price'

            s_bhk  = getattr(s_obj, 'bhk',          getattr(s_obj, 'bhk_type', ''))
            s_area = (
                getattr(s_obj, 'builtup_area', None) or
                getattr(s_obj, 'land_area',    None) or
                getattr(s_obj, 'plot_area',    None) or
                getattr(s_obj, 'carpet_area',  None)
            )
            feature = s_bhk if s_bhk else (f"{s_area} Sq.Ft" if s_area else 'View Details')

            s_img_url = None
            if hasattr(s_obj, 'images'):
                try:
                    fi = s_obj.images.first()
                    if fi and fi.image:
                        s_img_url = fi.image.url
                except Exception:
                    pass

            similar.append({
                'id':            s_obj.pk,
                'title':         (
                    getattr(s_obj, 'title',          None) or
                    getattr(s_obj, 'property_title', None) or
                    getattr(s_obj, 'plot_title',     None) or
                    getattr(s_obj, 'pg_name',        None) or
                    'Property'
                ),
                'price_display': s_price_str,
                'location':      (
                    getattr(s_obj, 'locality',      None) or
                    getattr(s_obj, 'area_locality', None) or
                    getattr(s_obj, 'plot_locality', None) or
                    ''
                ),
                'feature':       feature,
                'listing_type':  listing_type,
                'category':      category,
                'image_url':     s_img_url,
            })
    except Exception:
        pass

    # ════════════════════════════════════════════════════════
    # METADATA RECOVERY
    # ════════════════════════════════════════════════════════

    seo = None
    try:
        from .models import LocationSEO
        from django.contrib.contenttypes.models import ContentType
        seo = LocationSEO.objects.filter(
            content_type=ContentType.objects.get_for_model(obj),
            object_id=obj.pk,
            pagetype=seo_page_type,
            is_active=True,
        ).first()
    except Exception:
        pass

    # ════════════════════════════════════════════════════════
    # SECURITY MASKS & SESSIONS
    # ════════════════════════════════════════════════════════

    user_id      = request.session.get('user_id') or request.session.get('User_id')
    logged_user  = None
    user_obj     = None
    user_subscription = None
    can_view_contact  = False

    if user_id:
        try:
            from .models import User_Details
            logged_user = User_Details.objects.filter(id=user_id).first()
            user_obj    = logged_user
            if logged_user:
                try:
                    from .utils import get_active_subscription
                    user_subscription = get_active_subscription(logged_user)
                    if user_subscription:
                        can_view_contact = True
                except Exception:
                    pass
        except Exception:
            pass

    masked_phone = 'XXXXXXXXXX'
    if p['owner_contact'] and len(str(p['owner_contact'])) >= 4:
        ph = str(p['owner_contact'])
        masked_phone = ph[:2] + 'X' * (len(ph) - 4) + ph[-2:]

    # DYNAMIC PRICE EXTRACTION FOR CONTEXT
    price_per_sqm = None
    if seo_page_type == 'industrial_plot_sale':
        price_per_sqm = getattr(obj, 'price_per_sqft', None)
    elif seo_page_type == 'commercial_plot_sale':
        price_per_sqm = getattr(obj, 'plot_price_per_sqft', None)
        
    price_per_unit = getattr(obj, 'price_per_unit', getattr(obj, 'price_per_acre_display', getattr(obj, 'price_per_acre', None)))


    
    locality_insight = None
    price_trend = None
    nearby_localities = []

    if p.get('city') and p.get('locality'):
        locality_insight = LocalityInsight.objects.filter(
            city__iexact=p['city'], locality__iexact=p['locality'], is_active=True
        ).first()
        price_trend = LocalityPriceTrend.objects.filter(
            city__iexact=p['city'], locality__iexact=p['locality']
        ).first()
        nearby_localities = LocalityPriceTrend.objects.filter(
            city__iexact=p['city']
        ).exclude(locality__iexact=p['locality'])[:5]
    # ════════════════════════════════════════════════════════
    # CONTEXT INTERFACE
    # ════════════════════════════════════════════════════════
    print("DEBUG LOCALITY:", p.get('city'), p.get('locality'))
    print("DEBUG INSIGHT:", locality_insight)
    print("DEBUG TREND:", price_trend)

    context = {
        'p':               p,
       
        'original':        obj,
        'locality_insight': locality_insight,
        'price_trend': price_trend,
        'nearby_localities': nearby_localities,
        'listing_type':    listing_type,
        'category':        category,
        'sub_category' :   sub_category,
        'property_group':  property_group,
        'seo_page_type':   seo_page_type,
        'property_images': property_images,
        'amenities_list':  amenities_list,
        'facilities_list': facilities_list,
        'similar':         similar,
        'base_emi':        base_emi,
        'raw_price':       p['raw_price'],
        'price_per_sqm':   price_per_sqm,
        'price_per_unit':  price_per_unit,
        'seo':             seo,
        'logged_user':     logged_user,
        'user_obj':        user_obj,
        'user_subscription': user_subscription,
        'can_view_contact':  can_view_contact,
        'masked_phone':      masked_phone,
        'today':           date.today(),
        'now':             now(),
        'selected_video':  selected_video,
        'grouped_images':  grouped_images,
    }

    return render(request, 'home_page/property_detail.html', context)


############ Views start for track utm link #########################

@csrf_exempt
def Track_utm_link(request):
    """Track UTM link clicks - creates new or updates existing"""
    
    try:
        # Parse request body
        data = json.loads(request.body)
        
        print("=" * 50)
        print("TRACK_UTM_LINK CALLED")
        print("Received data:", data)
        print("=" * 50)
        
        # Get data from request
        utm_source = data.get('utm_source')
        utm_medium = data.get('utm_medium')
        utm_campaign = data.get('utm_campaign', '')
        utm_term = data.get('utm_term', '')
        utm_content = data.get('utm_content', '')
        property_id = data.get('property_id')
        property_title = data.get('property_title', 'Unknown')
        listing_type = data.get('listing_type', 'rent')
        category = data.get('category', 'unknown')
        page_url = data.get('page_url', '')
        utm_path = data.get('utm_path', '/')
        utm_params = data.get('utm_params', '')
        
        print(f"UTM Path: {utm_path}")
        print(f"UTM Params: {utm_params}")
        
        # Validate required fields
        if not utm_source:
            return JsonResponse({'success': False, 'error': 'utm_source is required'})
        if not utm_medium:
            return JsonResponse({'success': False, 'error': 'utm_medium is required'})
        if not property_id:
            return JsonResponse({'success': False, 'error': 'property_id is required'})
        
        #  Find the property and get its ContentType
        real_property = None
        property_content_type = None
        
        # Map category to model
        try:
            if listing_type == "rent" and category == "residential-data":
                real_property = RentalResidentialProperty.objects.get(id=property_id)
                property_content_type = ContentType.objects.get_for_model(RentalResidentialProperty)
            elif listing_type == "rent" and category == "pg-data":
                real_property = PGColivingProperty.objects.get(id=property_id)
                property_content_type = ContentType.objects.get_for_model(PGColivingProperty)
            elif listing_type == "rent" and category == "commercial-data":
                real_property = CommercialRentalProperty.objects.get(id= property_id)
                property_content_type = ContentType.objects.get_for_model(CommercialRentalProperty)
            elif listing_type == "sale" and category == "resale-residential":
                real_property = ResaleResidentialProperty.objects.get(id=property_id)
                property_content_type = ContentType.objects.get_for_model(ResaleResidentialProperty)
            elif listing_type == "sale" and category == "commercial-resale":
                real_property = CommercialResaleProperty.objects.get(id=property_id)
                property_content_type = ContentType.objects.get_for_model(CommercialResaleProperty)
            elif listing_type == "sale" and category == "plot-resale":
                real_property = PlotSaleProperty.objects.get(id=property_id)
                property_content_type = ContentType.objects.get_for_model(PlotSaleProperty)
            elif listing_type == "sale" and category == "industrial-resale":
                real_property = IndustrialResaleProperty.objects.get(id=property_id)
                property_content_type = ContentType.objects.get_for_model(IndustrialResaleProperty)
            elif listing_type == "sale" and category == "agricultural-data":
                real_property = AgriculturalResaleProperty.objects.get(id=property_id)
                property_content_type = ContentType.objects.get_for_model(AgriculturalResaleProperty)
        except ObjectDoesNotExist as e:
            print(f"Property not found: {e}")
            return JsonResponse({'success': False, 'error': 'Property not found'})
        
        if not property_content_type or not real_property:
            return JsonResponse({'success': False, 'error': 'Invalid property type'})
        
        # Get property title if not provided
        if property_title == 'Unknown':
            property_title = getattr(real_property, 'title', None)
            if not property_title:
                property_title = getattr(real_property, 'property_title', str(real_property))
    
        #  Try to find existing UTM link using Generic FK
        utm_link = UTMLink.objects.filter(
            content_type=property_content_type,
            object_id=property_id,
            utm_source=utm_source,
            utm_medium=utm_medium,
            utm_campaign=utm_campaign if utm_campaign else '',
            listing_type=listing_type,
            category=category,
        ).first()
        
        print(f"Existing UTM link found: {utm_link is not None}")
        
        if utm_link:
            #  UPDATE EXISTING - INCREASE CLICK COUNT
            utm_link.total_clicks = models.F('total_clicks') + 1
            utm_link.save()
            utm_link.refresh_from_db()
            
            print(f"Updated click count: {utm_link.total_clicks}")
            
            return JsonResponse({
                'success': True,
                'message': 'Click tracked successfully',
                'total_clicks': utm_link.total_clicks,
                'created': False
            })
        else:
            # CREATE NEW UTM LINK (without property_id field)
            import uuid
            link_id = str(uuid.uuid4())[:8]
            
            utm_link = UTMLink.objects.create(
                link_id=link_id,
                content_type=property_content_type,
                object_id=property_id,
                property_title=property_title,
                listing_type=listing_type,
                category=category,
                utm_path=utm_path,
                utm_url=page_url,
                utm_source=utm_source,
                utm_medium=utm_medium,
                utm_campaign=utm_campaign,
                utm_term=utm_term,
                utm_content=utm_content,
                total_clicks=1,
                total_enquiries=0
            )
            
            print(f" Created new UTM link with ID: {link_id}")
            print(f"   Source: {utm_source}, Medium: {utm_medium}, Campaign: {utm_campaign}")
            
            return JsonResponse({
                'success': True,
                'message': 'New UTM link created and click tracked',
                'total_clicks': 1,
                'link_id': link_id,
                'created': True
            })
            
    except Exception as e:
        print(f" Error in Track_utm_link: {str(e)}")
        import traceback
        traceback.print_exc()
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)

############# Views end for track utm link #############################
 
# ─────────────────────────────────────────────────────────────
# HELPER: normalise ANY property object to a flat dict for
# the listing page cards. Covers all 8 property types.
# ─────────────────────────────────────────────────────────────
# def _normalize_any_property(obj, sheet_name):
#     LISTING_TYPE = {
#         "Residential Data": "rent",
#         "Commercial Data":  "rent",
#         "PG Data":          "rent",
#         "Resale Residential": "sale",
#         "Commercial Resale":  "sale",
#         "Plot Resale":        "sale",
#         "Agricultural Data":  "sale",
#         "Industrial Resale":  "sale",
#     }
#     CATEGORY = {
#         "Residential Data": "residential",
#         "Commercial Data":  "commercial",
#         "PG Data":          "pg",
#         "Resale Residential": "residential",
#         "Commercial Resale":  "commercial",
#         "Plot Resale":        "plot",
#         "Agricultural Data":  "agriculture",
#         "Industrial Resale":  "industrial",
#     }
#     EMOJI = {
#         "Residential Data": "🏠",
#         "Commercial Data":  "🏢",
#         "PG Data":          "🛏️",
#         "Resale Residential": "🏡",
#         "Commercial Resale":  "🏬",
#         "Plot Resale":        "🌄",
#         "Agricultural Data":  "🌾",
#         "Industrial Resale":  "🏭",
#     }

#     lt  = LISTING_TYPE.get(sheet_name, "rent")
#     cat = CATEGORY.get(sheet_name,     "residential")

#     # ── Price ────────────────────────────────────────────────
#     raw_price = (
#         getattr(obj, 'monthly_rent',   None) or
#         getattr(obj, 'expected_rent',  None) or
#         getattr(obj, 'expected_price', None) or
#         getattr(obj, 'plot_price',     None)
#     )
#     # PG special case
#     if sheet_name == "PG Data" and not raw_price:
#         raw_price = _get_pg_min_price(obj)

#     try:
#         price_f = float(raw_price) if raw_price else 0
#         if price_f > 0:
#             suffix = "/mo" if lt == "rent" else ""
#             price_display = f"₹{price_f:,.0f}{suffix}"
#         else:
#             price_display = "Price on Request"
#     except Exception:
#         price_display = "Price on Request"

#     # ── Title ────────────────────────────────────────────────
#     title = (
#         getattr(obj, 'title',          None) or
#         getattr(obj, 'property_title', None) or
#         getattr(obj, 'plot_title',     None) or
#         getattr(obj, 'pg_name',        None) or
#         getattr(obj, 'building_name',  None) or
#         "Property"
#     )

#     # ── Location ────────────────────────────────────────────
#     locality = (
#         getattr(obj, 'locality',      None) or
#         getattr(obj, 'area_locality', None) or
#         getattr(obj, 'plot_locality', None) or
#         getattr(obj, 'village',       None) or
#         ""
#     )
#     city = (
#         getattr(obj, 'city',      None) or
#         getattr(obj, 'plot_city', None) or
#         ""
#     )
#     location = f"{locality}, {city}".strip(", ") if (locality or city) else "Nagpur"

#     # ── Area ────────────────────────────────────────────────
#     area = (
#         getattr(obj, 'builtup_area',  None) or
#         getattr(obj, 'built_up_area', None) or
#         None
#     )
#     land_area  = getattr(obj, 'land_area',  None)
#     plot_area  = getattr(obj, 'plot_area',  None)
#     total_beds = getattr(obj, 'total_beds', None)
#     min_seats  = getattr(obj, 'min_seats',  None)
#     kva_capacity = getattr(obj, 'kva_capacity', None)

#     # ── Config ──────────────────────────────────────────────
#     beds = getattr(obj, 'bhk', None) or getattr(obj, 'bhk_type', None)
#     baths = getattr(obj, 'bathrooms', None) or getattr(obj, 'baths', None)

#     # ── Furnishing ──────────────────────────────────────────
#     furnished = (
#         getattr(obj, 'furnishing_status', None) or
#         getattr(obj, 'furnishing_type',   None) or
#         getattr(obj, 'furnished',         None)
#     )

#     # ── Owner ───────────────────────────────────────────────
#     owner_name = (
#         getattr(obj, 'owner_name',       None) or
#         getattr(obj, 'plot_owner_name',  None) or
#         "Owner"
#     )
#     owner_initials = owner_name[0].upper() if owner_name else "O"

#     phone = (
#         getattr(obj, 'contact_number',      None) or
#         getattr(obj, 'owner_contact',       None) or
#         getattr(obj, 'plot_owner_contact',  None) or
#         ""
#     )

#     # ── Image ───────────────────────────────────────────────
#     image_url = None
#     if hasattr(obj, 'images'):
#         try:
#             first = obj.images.first()
#             if first and first.image:
#                 image_url = first.image.url
#         except Exception:
#             pass

#     property_type = (
#         getattr(obj, 'property_type',            None) or
#         getattr(obj, 'agriculture_property_type', None) or
#         getattr(obj, 'resale_plot_type',          None)
#     )

#     return {
#         'id':             obj.id,
#         'title':          title,
#         'location':       location,
#         'city':           city,
#         'price_display':  price_display,
#         'area':           area,
#         'land_area':      land_area,}
    
#     p['carpet_area']  = getattr(obj, 'carpet_area',  None)
#     p['plot_area']    = getattr(obj, 'plot_area',    None)
#     p['builtup_area'] = getattr(obj, 'builtup_area', getattr(obj, 'built_up_area', None))

#     # FURNISHING & AGE
#     p['furnished'] = (
#         getattr(obj, 'furnishing_status', None) or
#         getattr(obj, 'furnishing_type',   None) or
#         getattr(obj, 'furnished',         None)
#     )
#     p['age']                = getattr(obj, 'age_of_property',   getattr(obj, 'property_age', None))
#     p['property_condition'] = getattr(obj, 'property_condition', None)
#     p['construction_status']= getattr(obj, 'construction_status', None)

#     # FACING & FLOOR
#     p['facing'] = getattr(obj, 'facing', getattr(obj, 'plot_road_facing', None))
#     p['floor']  = (
#         getattr(obj, 'floor_number', None) or
#         getattr(obj, 'floor_no',     None) or
#         getattr(obj, 'your_floor',   None)
#     )
#     p['total_floors'] = getattr(obj, 'total_floors', None)

#     # ZONE / LOCATION
#     p['zone']          = getattr(obj, 'zone',          None)
#     p['zone_type']     = getattr(obj, 'zone_type',     None)
#     p['location_hub']  = getattr(obj, 'location_hub',  None)
#     p['society_type']  = getattr(obj, 'society_type',  None)
#     p['water_type']    = getattr(obj, 'water_type',    None)

#     # POSSESSION
#     p['possession']    = getattr(obj, 'possession_status', getattr(obj, 'available_from', None))
#     p['available_from']= getattr(obj, 'available_from',    None)
#     p['lease_duration']= getattr(obj, 'lease_duration',    None)

#     # OWNERSHIP
#     p['ownership']   = getattr(obj, 'ownership_type', getattr(obj, 'plot_ownership', None))
#     p['num_owners']  = getattr(obj, 'num_owners',     None)

#     # ── PRICING ────────────────────────────────────────────
#     # Rental prices
#     p['monthly_rent']     = getattr(obj, 'monthly_rent',     getattr(obj, 'expected_rent', None))
#     p['security_deposit'] = getattr(obj, 'security_deposit', None)
#     p['maintenance']      = getattr(obj, 'maintenance_amount', getattr(obj, 'maintenance_charges', None))
#     p['maintenance_type'] = getattr(obj, 'maintenance_type', None)
#     p['negotiable']       = getattr(obj, 'negotiable',       None)
#     p['is_negotiable']    = getattr(obj, 'is_negotiable',    None)

#     # Sale prices
#     raw_price = (
#         getattr(obj, 'expected_price', None) or
#         getattr(obj, 'plot_price',     None) or
#         getattr(obj, 'monthly_rent',   None) or
#         getattr(obj, 'expected_rent',  None)
#     )

#     # PG: no direct price field — parse room_details
#     if seo_page_type == "pg_coliving":
#         pg_prices = _parse_pg_room_prices(obj)
#         p.update(pg_prices)  # single_sharing, double_sharing, etc.

#         # Set monthly_rent to minimum bed price for sidebar display
#         bed_prices = [v for v in pg_prices.values() if v]
#         if bed_prices:
#             p['monthly_rent'] = min(bed_prices)
#             raw_price = p['monthly_rent']
#         else:
#             pg_min = _get_pg_min_price(obj)
#             if pg_min:
#                 p['monthly_rent'] = pg_min
#                 raw_price = pg_min

#     p['raw_price']      = raw_price or 0
#     p['expected_price'] = raw_price or 0

#     try:
#         price_f = float(raw_price) if raw_price else 0
#         p['price_display'] = f"₹{price_f:,.0f}" if price_f > 0 else "Price on Request"
#     except Exception:
#         p['price_display'] = str(raw_price) if raw_price else "Price on Request"

#     p['price_sqft'] = getattr(obj, 'price_per_sqft', None)

#     # Brokerage
#     b_flag = str(getattr(obj, 'brokerage', '')).lower()
#     p['brokerage'] = None
#     if b_flag in ['yes', 'true', '1']:
#         p['brokerage'] = (
#             getattr(obj, 'brokerage_percentage', None) or
#             getattr(obj, 'manual_brokerage',     None) or
#             'Applicable'
#         )

#     # COMMERCIAL SPECS
#     p['min_seats']       = getattr(obj, 'min_seats',       None)
#     p['max_seats']       = getattr(obj, 'max_seats',       None)
#     p['cabins']          = getattr(obj, 'cabins',   getattr(obj, 'num_cabins',    None))
#     p['meeting_rooms']   = getattr(obj, 'meeting_rooms',   None)
#     p['passenger_lifts'] = getattr(obj, 'passenger_lifts', None)
#     p['service_lifts']   = getattr(obj, 'service_lifts',   None)
#     p['private_washroom']= getattr(obj, 'private_washroom', None)
#     p['public_washroom'] = getattr(obj, 'public_washroom',  None)
#     p['staircases']      = getattr(obj, 'staircases', getattr(obj, 'num_staircases', None))
#     p['flooring_type']   = getattr(obj, 'flooring_type',   None)

#     # UTILITIES (commercial)
#     p['dg_ups_included']    = getattr(obj, 'dg_ups_included',    False)
#     p['electricity_included']= getattr(obj, 'electricity_included', False)
#     p['water_included']     = getattr(obj, 'water_included',     False)

#     # RENTAL TERMS
#     p['lockin_period']  = getattr(obj, 'lockin_period',  None)
#     p['rent_increase']  = getattr(obj, 'rent_increase',  None)
#     p['minimum_stay']   = getattr(obj, 'minimum_stay',   None)
#     p['notice_period']  = getattr(obj, 'notice_period',  None)

#     # PG SPECIFIC
#     p['total_beds']          = getattr(obj, 'total_beds',         None)
#     p['sharing_type']        = getattr(obj, 'sharing_type',       None)
#     p['pg_for']              = getattr(obj, 'pg_for',  getattr(obj, 'best_suited_for', None))
#     p['meal_offerings']      = getattr(obj, 'meal_offerings',     None)
#     p['meals_available']     = getattr(obj, 'meals_available',    False)
#     p['meal_speciality']     = getattr(obj, 'meal_speciality',    None)
#     p['room_details']        = getattr(obj, 'room_details',       None)
#     p['common_area']         = getattr(obj, 'common_area',        None)
#     p['property_managed_by'] = getattr(obj, 'property_managed_by', None)
#     p['manager_stays']       = getattr(obj, 'manager_stays',      False)

#     # PG RULES
#     p['non_veg_allowed']     = getattr(obj, 'non_veg_allowed',      False)
#     p['opposite_sex_allowed']= getattr(obj, 'opposite_sex_allowed', False)
#     p['any_time_allowed']    = getattr(obj, 'any_time_allowed',     False)
#     p['visitors_allowed']    = getattr(obj, 'visitors_allowed',     False)
#     p['guardian_allowed']    = getattr(obj, 'guardian_allowed',     False)
#     p['drinking_allowed']    = getattr(obj, 'drinking_allowed',     False)
#     p['smoking_allowed']     = getattr(obj, 'smoking_allowed',      False)

#     # PLOT
#     p['plot_corner']         = getattr(obj, 'plot_corner',         False)
#     p['plot_fencing']        = getattr(obj, 'plot_fencing',        False)
#     p['plot_road_facing']    = getattr(obj, 'plot_road_facing',    None)
#     p['sanctioning_authority']= getattr(obj, 'sanctioning_authority', getattr(obj, 'plot_authority', None))

#     # INDUSTRIAL
#     p['power_kva']            = getattr(obj, 'kva_capacity',          getattr(obj, 'power_supply', None))
#     p['power_supply']         = getattr(obj, 'power_supply',          None)
#     p['water_supply']         = getattr(obj, 'water_supply',          None)
#     p['crane_heavy_machinery']= getattr(obj, 'crane_heavy_machinery', False)
#     p['road_connectivity']    = getattr(obj, 'road_connectivity',     None)
#     p['worker_housing_nearby']= getattr(obj, 'worker_housing_nearby', False)

#     # AGRICULTURE
#     p['soil_type']          = getattr(obj, 'soil_type',          None)
#     p['water_source']       = getattr(obj, 'water_source', getattr(obj, 'water_type', None))
#     p['irrigation_facility']= getattr(obj, 'irrigation_facility', None)
#     p['fertility_status']   = getattr(obj, 'fertility_status',   None)
#     p['previous_crops']     = getattr(obj, 'previous_crops',     None)
#     p['state']              = getattr(obj, 'state',              None)
#     p['district']           = getattr(obj, 'district',           None)
#     p['taluka']             = getattr(obj, 'taluka',             None)
#     p['village']            = getattr(obj, 'village',            None)

#     # LEGAL
#     def _bool_field(*attrs):
#         for a in attrs:
#             v = getattr(obj, a, None)
#             if v is not None:
#                 return str(v).lower() in ['yes', 'true', '1']
#         return False

#     p['has_loan']        = _bool_field('has_loan', 'plot_loan', 'agri_loan', 'loan_on_property')
#     p['loan_amount']     = getattr(obj, 'loan_amount', getattr(obj, 'plot_loan_amount', None))
#     p['has_dispute']     = _bool_field('has_legal_dispute', 'legal_dispute', 'agri_dispute')
#     p['dispute_details'] = getattr(obj, 'dispute_details', None)
#     p['has_tax_due']     = _bool_field('has_tax_due', 'tax_due', 'agri_tax_due')
#     p['tax_amount']      = getattr(obj, 'pending_tax_amount', getattr(obj, 'tax_amount', None))
#     p['has_tenants']     = _bool_field('has_tenants', 'existing_tenants', 'agri_tenants')
#     p['tenant_details']  = getattr(obj, 'tenant_details', None)
#     p['fire_noc']        = getattr(obj, 'fire_noc',            None)
#     p['tax_clearance_cert']= getattr(obj, 'tax_clearance_cert', False)
#     p['encumbrance_cert']  = getattr(obj, 'encumbrance_cert',   None)
#     p['compliance_docs']   = getattr(obj, 'compliance_docs',    None)

#     # LOCATION
#     p['city']     = getattr(obj, 'city',     getattr(obj, 'plot_city', getattr(obj, 'state', '')))
#     p['locality'] = (
#         getattr(obj, 'locality',      None) or
#         getattr(obj, 'plot_locality', None) or
#         getattr(obj, 'area_locality', None) or
#         getattr(obj, 'village',       None) or
#         ''
#     )
#     p['address'] = (
#         getattr(obj, 'complete_address',  None) or
#         getattr(obj, 'property_address',  None) or
#         getattr(obj, 'address',           None) or
#         getattr(obj, 'plot_address',      None) or
#         ''
#     )
#     p['building_name'] = getattr(obj, 'building_name', None)
#     p['pincode']       = getattr(obj, 'pincode', '')

#     # DESCRIPTION
#     p['desc'] = (
#         getattr(obj, 'description',            None) or
#         getattr(obj, 'property_description',   None) or
#         getattr(obj, 'rent_residential_desc',  None) or
#         getattr(obj, 'resale_agricultural_desc', None) or
#         getattr(obj, 'pg_description',         None) or
#         ''
#     )

#     # MEDIA
#     p['video'] = (
#         getattr(obj, 'property_video', None) or
#         getattr(obj, 'video',          None) or
#         getattr(obj, 'social_video',   None)
#     )
#     p['floor_plan'] = getattr(obj, 'floor_plan', None)

#     # OWNER
#     p['owner_name']    = (
#         getattr(obj, 'owner_name',       None) or
#         getattr(obj, 'plot_owner_name',  None) or
#         'Property Owner'
#     )
#     p['owner_contact'] = (
#         getattr(obj, 'contact_number',      None) or
#         getattr(obj, 'owner_contact',       None) or
#         getattr(obj, 'plot_owner_contact',  None) or
#         ''
#     )
#     p['owner_email'] = (
#         getattr(obj, 'email',             None) or
#         getattr(obj, 'owner_email',       None) or
#         getattr(obj, 'plot_owner_email',  None) or
#         ''
#     )
#     p['alternate_contact']  = getattr(obj, 'alternate_contact', None)
#     p['residential_status'] = getattr(obj, 'residential_status', getattr(obj, 'comm_residency', None))

#     # UPLOADED BY
#     p['uploaded_by_role']    = getattr(obj, 'uploaded_by_role',    'Owner')
#     p['uploaded_by_name']    = getattr(obj, 'uploaded_by_name',    None)
#     p['uploaded_by_email']   = getattr(obj, 'uploaded_by_email',   None)
#     p['uploaded_by_contact'] = getattr(obj, 'uploaded_by_contact', None)

#     # ── 3. Images & Amenities ────────────────────────────────
#     if hasattr(obj, 'images'):
#         property_images = obj.images.all()

#     def parse_list(val):
#         if not val:
#             return []
#         if isinstance(val, list):
#             return [str(x).strip() for x in val if x]
#         if isinstance(val, str):
#             try:
#                 parsed = json.loads(val)
#                 if isinstance(parsed, list):
#                     return [str(x).strip() for x in parsed if x]
#             except Exception:
#                 pass
#             return [x.strip() for x in val.split(',') if x.strip()]
#         return []

#     amenities_list  = parse_list(getattr(obj, 'amenities',          ''))
#     facilities_list = parse_list(getattr(obj, 'nearby_facilities',  getattr(obj, 'facilities', '')))

#     if p.get('dg_ups_included'):    amenities_list.append("DG/UPS Backup")
#     if p.get('electricity_included'): amenities_list.append("Electricity Included")
#     if p.get('water_included'):     amenities_list.append("Water Included")

#     # ── 4. EMI Calculator ────────────────────────────────────
#     if listing_type == 'sale' and p['raw_price']:
#         try:
#             principal = float(p['raw_price']) * 0.80
#             r = 8.5 / 12 / 100
#             n = 20 * 12
#             base_emi = int((principal * r * math.pow(1 + r, n)) / (math.pow(1 + r, n) - 1))
#         except Exception:
#             base_emi = 0

#     # ── 5. Similar Properties ────────────────────────────────
#     similar = []
#     if p.get('city'):
#         try:
#             similar_qs = property_model.objects.filter(is_deleted=False).exclude(id=obj.id)

#             city_val = p['city']
#             if hasattr(property_model, 'city'):
#                 similar_qs = similar_qs.filter(city__icontains=city_val)
#             elif hasattr(property_model, 'plot_city'):
#                 similar_qs = similar_qs.filter(plot_city__icontains=city_val)

#             for s_obj in similar_qs[:3]:
#                 s_raw = (
#                     getattr(s_obj, 'expected_price', None) or
#                     getattr(s_obj, 'plot_price',     None) or
#                     getattr(s_obj, 'monthly_rent',   None) or
#                     getattr(s_obj, 'expected_rent',  None)
#                 )
#                 # PG similar price
#                 if seo_page_type == "pg_coliving" and not s_raw:
#                     s_raw = _get_pg_min_price(s_obj)

#                 try:
#                     s_price_str = f"₹{float(s_raw):,.0f}" if s_raw else "Ask Price"
#                 except Exception:
#                     s_price_str = "Ask Price"

#                 s_bhk  = getattr(s_obj, 'bhk', getattr(s_obj, 'bhk_type', ''))
#                 s_area = (
#                     getattr(s_obj, 'builtup_area', None) or
#                     getattr(s_obj, 'land_area',    None) or
#                     getattr(s_obj, 'plot_area',    None) or
#                     getattr(s_obj, 'carpet_area',  None)
#                 )
#                 feature = s_bhk if s_bhk else (f"{s_area} Sq.Ft" if s_area else "Details")

#                 s_img_url = None
#                 if hasattr(s_obj, 'images'):
#                     try:
#                         fi = s_obj.images.first()
#                         if fi and fi.image:
#                             s_img_url = fi.image.url
#                     except Exception:
#                         pass

#                 similar.append({
#                     'id':            s_obj.id,
#                     'title':         (
#                         getattr(s_obj, 'title',          None) or
#                         getattr(s_obj, 'plot_title',     None) or
#                         getattr(s_obj, 'pg_name',        None) or
#                         getattr(s_obj, 'property_title', 'Property')
#                     ),
#                     'price_display': s_price_str,
#                     'location':      (
#                         getattr(s_obj, 'locality',      None) or
#                         getattr(s_obj, 'plot_locality', None) or
#                         getattr(s_obj, 'area_locality', None) or
#                         ''
#                     ),
#                     'feature':       feature,
#                     'listing_type':  listing_type,
#                     'category':      category,
#                     'image_url':     s_img_url,
#                 })
#         except Exception:
#             pass

#     # ── 6. SEO & Auth ────────────────────────────────────────
#     seo = None
#     try:
#         from .models import LocationSEO
#         from django.contrib.contenttypes.models import ContentType
#         seo = LocationSEO.objects.filter(
#             content_type=ContentType.objects.get_for_model(obj),
#             object_id=obj.id,
#             pagetype=seo_page_type,
#             is_active=True,
#         ).first()
#     except Exception:
#         pass

#     user_id = request.session.get('user_id') or request.session.get('User_id')
#     logged_user = user_obj = user_subscription = None
#     can_view_contact = False

#     if user_id:
#         try:
#             from .models import User_Details
#             logged_user = User_Details.objects.filter(id=user_id).first()
#             user_obj    = logged_user
#             try:
#                 from .utils import get_active_subscription
#                 user_subscription = get_active_subscription(logged_user)
#                 if user_subscription:
#                     can_view_contact = True
#             except Exception:
#                 pass
#         except Exception:
#             pass

#     # Mask phone
#     masked_phone = "XXXXXXXXXX"
#     if p['owner_contact'] and len(str(p['owner_contact'])) >= 10:
#         ph = str(p['owner_contact'])
#         masked_phone = f"{ph[:2]}XXXXXX{ph[-2:]}"

#     # ── 7. Context & Render ──────────────────────────────────
#     context = {
#         "p":                p,
#         "original":         obj,
#         "listing_type":     listing_type,
#         "category":         category,
#         "property_images":  property_images,
#         "amenities_list":   amenities_list,
#         "facilities_list":  facilities_list,
#         "similar":          similar,
#         "base_emi":         base_emi,
#         "raw_price":        p['raw_price'],
#         "seo":              seo,
#         "logged_user":      logged_user,
#         "user_obj":         user_obj,
#         "user_subscription":user_subscription,
#         "can_view_contact": can_view_contact,
#         "masked_phone":     masked_phone,
#         "today":            date.today(),
#         "now":              now(),
#     }
#     return render(request, 'home_page/property_detail.html', context)


# ═════════════════════════════════════════════════════════════
# LISTINGS VIEW
# ═════════════════════════════════════════════════════════════





from django.core.paginator import Paginator

# ─────────────────────────────────────────────────────────────



from django.http import JsonResponse

def search_suggestions_api(request):
    query        = request.GET.get('q', '').strip()
    listing_type = request.GET.get('type', 'rent').strip().lower()

    if len(query) < 2:
        return JsonResponse({'suggestions': []})

    suggestions = []
    seen        = set()

    # Safely handle both 'sale' and 'resale' URL params from the frontend
    if listing_type in ('sale', 'resale'):
        models_config = [
            (ResaleResidentialProperty, [
                ('locality', 'Locality'), ('city', 'City'),
                ('property_type', 'Property Type'),
                ('property_title', 'Listing'), ('building_name', 'Project'),
            ]),
            (CommercialResaleProperty, [
                ('locality', 'Locality'), ('city', 'City'),
                ('property_type', 'Property Type'),
                ('property_title', 'Listing'), ('building_name', 'Project'),
            ]),
            (IndustrialResaleProperty, [
                ('locality', 'Locality'), ('city', 'City'),
                ('property_type', 'Property Type'),
                ('property_title', 'Listing'),
            ]),
            (AgriculturalResaleProperty, [
                ('village', 'Locality'), ('locality', 'Locality'), ('city', 'City'),
                ('property_type', 'Property Type'),
                ('property_title', 'Listing'),
            ]),
            # ── LEGACY PLOT MODEL ──
            (PlotSaleProperty, [
                ('plot_locality', 'Locality'), ('plot_city', 'City'),
                ('resale_plot_type', 'Property Type'),
                ('plot_title', 'Listing'),
            ]),
            # ── 4 NEW PLOT MODELS (Corrected Field Mappings) ──
            (ResidentialPlotResaleProperty, [
                ('locality', 'Locality'), ('city', 'City'),
                ('property_type', 'Property Type'),
                ('property_title', 'Listing'),
            ]),
            (CommercialPlotResaleProperty, [
                ('locality', 'Locality'), ('city', 'City'),
                ('property_type', 'Property Type'),
                ('property_title', 'Listing'),
            ]),
            (IndustrialPlotResaleProperty, [
                ('locality', 'Locality'), ('city', 'City'),
                ('property_type', 'Property Type'),
                ('property_title', 'Listing'),
            ]),
            (AgriculturalPlotResaleProperty, [
                ('locality', 'Locality'), ('city', 'City'),
                ('property_type', 'Property Type'),
                ('property_title', 'Listing'),
            ]),
        ]
    else:  # rent (default)
        models_config = [
            (RentalResidentialProperty, [
                ('locality_area', 'Locality'), ('city', 'City'),
                ('property_type', 'Property Type'),
                ('property_title', 'Listing'), ('building_name', 'Project'),
            ]),
            (CommercialRentalProperty, [
                ('locality', 'Locality'), ('city', 'City'),
                ('property_type', 'Property Type'),
                ('property_title', 'Listing'), ('building_name', 'Project'),
            ]),
            (PGColivingProperty, [
                ('locality', 'Locality'), ('city', 'City'),
                ('pg_for', 'PG Type'),
                ('property_title', 'Listing'), ('building_name', 'Project'),
            ]),
        ]

    for model, fields in models_config:
        for field_name, field_label in fields:
            if not hasattr(model, field_name):
                continue
            try:
                qs = model.objects.filter(
                    is_deleted=False,
                    **{f'{field_name}__icontains': query}
                )
            except Exception:
                qs = model.objects.filter(
                    **{f'{field_name}__icontains': query}
                )

            values = qs.values_list(field_name, flat=True).distinct()[:10]
            for v in values:
                v = (v or '').strip()
                if v and v.lower() not in seen:
                    seen.add(v.lower())
                    suggestions.append({'text': v, 'type': field_label})

    # City → Locality → Property Type → everything else (Listing/Project)
    priority = {'City': 0, 'Locality': 1, 'Property Type': 2, 'PG Type': 2}
    suggestions.sort(key=lambda x: priority.get(x['type'], 3))

    return JsonResponse({'suggestions': suggestions[:10]})





def _collect_property_types(models_to_search):
    """Distinct, non-empty property-type values that actually exist
    right now for the models being searched — mirrors what Housing.com
    does (suggestions reflect live inventory, not a static list)."""
    type_fields = ('property_type', 'resale_plot_type')
    found = set()

    for _, db_model in models_to_search:
        qs = db_model.objects.all()
        if hasattr(db_model, 'is_deleted'):
            qs = qs.filter(is_deleted=False)

        for f in type_fields:
            if hasattr(db_model, f):
                values = (
                    qs.exclude(**{f: None})
                      .exclude(**{f: ''})
                      .values_list(f, flat=True)
                      .distinct()
                )
                found.update(v.strip() for v in values if v and v.strip())

    return sorted(found)






def listings_view(request):
    city_filter       = request.GET.get('city_filter', '').strip()
    listing_type      = request.GET.get('type', 'rent').strip().lower()
    category          = request.GET.get('category', '').strip().lower()

    SearchLog.objects.create(
        listing_type=request.GET.get('type', ''),
        category=request.GET.get('category', ''),
        bhk=request.GET.get('bhk', ''),
        sub=request.GET.get('prop_type', ''),
        area=request.GET.get('areas', '') or request.GET.get('area', ''),
        city=request.GET.get('city_filter', ''),
    )

    # MULTIPLE AREA / FREE TEXT SEARCH
    areas_raw   = request.GET.get('areas', '').strip()
    areas_list  = [a.strip() for a in areas_raw.split(',') if a.strip()] if areas_raw else []

    single_area = request.GET.get('area', '').strip()
    if single_area and single_area not in areas_list:
        areas_list.append(single_area)

    bhk_filter        = request.GET.get('bhk',         '').strip()
    budget_min        = request.GET.get('budget_min', '').strip()
    budget_max        = request.GET.get('budget_max', '').strip()
    furnishing_filter = request.GET.get('furnishing', '').strip()
    prop_type_filter  = request.GET.get('prop_type',  '').strip()

    verified_filter   = request.GET.get('verified')
    featured_filter   = request.GET.get('featured')

    listed_by_filter = request.GET.get('listed_by', '').strip().lower()

    LISTED_BY_ROLE_MAP = {
        'landlord':       ['landlord', 'owner'],
        'rm':             ['relationship manager', 'rm'],
        'agent':          ['agent'],
        'admin':          ['admin'],
        'agency_builder': ['agency/builder', 'builder', 'agency'],
    }

    LISTED_BY_LABELS = {
        'landlord':       'Landlord',
        'rm':             'Relationship Manager',
        'agent':          'Agent',
        'admin':          'Admin',
        'agency_builder': 'Agency/Builder',
    }

    pet_filter        = request.GET.get('pet')
    lease_filter      = request.GET.get('lease',       '').strip()
    bathrooms_filter  = request.GET.get('bathrooms',   '').strip()
    area_range_filter = request.GET.get('area_range',  '').strip()
    age_filter        = request.GET.get('age',         '').strip()
    parking_filter    = request.GET.get('parking',     '').strip()
    added_filter      = request.GET.get('added',       '').strip()

    amenities_raw  = request.GET.get('amenities', '').strip()
    amenities_list = [a.strip() for a in amenities_raw.split(',') if a.strip()] if amenities_raw else []

    extra_filter_keys = [
        'seats', 'cabins', 'meeting_rooms', 'room_type', 'pg_for', 'meals',
        'road_facing', 'corner_plot', 'fencing', 'power_supply', 'crane',
        'loading_dock', 'soil_type', 'irrigation', 'water_source',
    ]
    extra_filters = {k: request.GET.get(k, '').strip() for k in extra_filter_keys}

    EXTRA_FIELD_MAP = {
        'seats': ['min_seats', 'max_seats'],
        'cabins': ['cabins', 'num_cabins'],
        'meeting_rooms': ['meeting_rooms'],
        'room_type': ['room_type'],
        'pg_for': ['pg_for'],
        'meals': ['meals_available'],
        'road_facing': ['plot_road_facing', 'facing_direction', 'plot_facing'],
        'corner_plot': ['corner_plot'],
        'fencing': ['plot_fencing'],
        'power_supply': ['power_supply'],
        'crane': ['crane_heavy_machinery'],
        'loading_dock': ['loading_dock'],
        'soil_type': ['soil_type'],
        'irrigation': ['irrigation_facility_active', 'irrigation_source'],
        'water_source': ['water_source', 'water_source_infrastructure'],
    }

    sort_filter  = request.GET.get('sort', 'relevant')
    page_number  = request.GET.get('page', 1)

    PER_PAGE    = 30
    MAX_COLLECT = 300

    # =========================================================
    # COMPREHENSIVE MODEL MAPPING (ALL CATEGORIES)
    # =========================================================
    models_to_search = []
    
    if listing_type == "rent":
        if category == "residential":
            models_to_search = [("residential", RentalResidentialProperty)]
        elif category == "commercial":
            models_to_search = [("commercial", CommercialRentalProperty)]
        elif category == "pg":
            models_to_search = [("pg", PGColivingProperty)]
        else:
            models_to_search = [
                ("residential", RentalResidentialProperty),
                ("commercial", CommercialRentalProperty),
                ("pg", PGColivingProperty),
            ]

    elif listing_type == "sale":
        if category == "residential":
            models_to_search = [("residential", ResaleResidentialProperty)]
        elif category == "commercial":
            models_to_search = [("commercial", CommercialResaleProperty)]
        elif category == "industrial":
            models_to_search = [("industrial", IndustrialResaleProperty)]
        elif category == "agricultural":
            models_to_search = [("agricultural", AgriculturalResaleProperty)]
        elif category == "plot":
            models_to_search = [
                ("plot", PlotSaleProperty),
                ("plot", ResidentialPlotResaleProperty),
                ("plot", CommercialPlotResaleProperty),
                ("plot", IndustrialPlotResaleProperty),
                ("plot", AgriculturalPlotResaleProperty),
            ]
        else:
            models_to_search = [
                ("residential", ResaleResidentialProperty),
                ("commercial", CommercialResaleProperty),
                ("industrial", IndustrialResaleProperty),
                ("agricultural", AgriculturalResaleProperty),
                ("plot", PlotSaleProperty),
                ("plot", ResidentialPlotResaleProperty),
                ("plot", CommercialPlotResaleProperty),
                ("plot", IndustrialPlotResaleProperty),
                ("plot", AgriculturalPlotResaleProperty),
            ]
    else:
        models_to_search = [("residential", RentalResidentialProperty)]

    available_prop_types = _collect_property_types(models_to_search)

    # =========================================================
    # SEARCH & FILTER EXECUTION
    # =========================================================
    all_properties = []

    for category_tag, db_model in models_to_search:
        if len(all_properties) >= MAX_COLLECT:
            break

        obj_q = db_model.objects.all()
        pk_field = db_model._meta.pk.name

        if hasattr(db_model, 'is_deleted'):
            obj_q = obj_q.filter(is_deleted=False)

        if city_filter:
            city_field = 'city' if hasattr(db_model, 'city') else 'plot_city' if hasattr(db_model, 'plot_city') else None
            if city_field:
                obj_q = obj_q.filter(**{f'{city_field}__icontains': city_filter})

        # FREE TEXT SEARCH EXPANDED
        if areas_list:
            area_q = Q()
            for term in areas_list:
                for f in ('locality', 'area_locality', 'plot_locality', 'address', 'village', 'property_title', 'building_name', 'property_type', 'resale_plot_type'):
                    if hasattr(db_model, f):
                        area_q |= Q(**{f'{f}__icontains': term})
            if area_q:
                obj_q = obj_q.filter(area_q)

        if bhk_filter:
            import re
            match = re.search(r'\d+', str(bhk_filter))
            bhk_num = int(match.group()) if match else None
            bhk_q = Q()
            for f in ['bhk_type', 'bhk', 'bedrooms', 'no_of_bedrooms']:
                if hasattr(db_model, f):
                    bhk_q |= Q(**{f: bhk_num})
                    bhk_q |= Q(**{f'{f}__icontains': str(bhk_num)})
            if bhk_q:
                obj_q = obj_q.filter(bhk_q)

        if budget_min:
            try:
                bmin = int(budget_min)
                budget_min_q = Q()
                for f in ('monthly_rent', 'expected_rent', 'expected_price', 'plot_price', 'selling_price'):
                    if hasattr(db_model, f):
                        budget_min_q |= Q(**{f'{f}__gte': bmin})
                if budget_min_q:
                    obj_q = obj_q.filter(budget_min_q)
            except (ValueError, TypeError):
                pass

        if budget_max:
            try:
                bmax = int(budget_max)
                budget_max_q = Q()
                for f in ('monthly_rent', 'expected_rent', 'expected_price', 'plot_price', 'selling_price'):
                    if hasattr(db_model, f):
                        budget_max_q |= Q(**{f'{f}__lte': bmax})
                if budget_max_q:
                    obj_q = obj_q.filter(budget_max_q)
            except (ValueError, TypeError):
                pass

        # ── SMART BYPASS FOR PROPERTY TYPES ──────────────────────────
        if prop_type_filter:
            ptype_lower = prop_type_filter.lower()
            
            is_dedicated_match = False
            if db_model == ResidentialPlotResaleProperty and 'residential' in ptype_lower:
                is_dedicated_match = True
            elif db_model == CommercialPlotResaleProperty and 'commercial' in ptype_lower:
                is_dedicated_match = True
            elif db_model == IndustrialPlotResaleProperty and 'industrial' in ptype_lower:
                is_dedicated_match = True
            elif db_model == AgriculturalPlotResaleProperty and ('agricultural' in ptype_lower or 'agriculture' in ptype_lower):
                is_dedicated_match = True

            # If the model does not inherently match the type, enforce the string filter
            if not is_dedicated_match:
                ptype_q = Q()
                for f in ('property_type', 'property_sub_type', 'flat_type', 'agriculture_property_type', 'resale_plot_type'):
                    if hasattr(db_model, f):
                        ptype_q |= Q(**{f'{f}__icontains': prop_type_filter})
                
                # Apply filter if fields exist, otherwise exclude the model
                if ptype_q:
                    obj_q = obj_q.filter(ptype_q)
                else:
                    obj_q = obj_q.none()

        if furnishing_filter:
            furn_q = Q()
            if hasattr(db_model, 'furnishing_status'):
                furn_q |= Q(furnishing_status__icontains=furnishing_filter)
            if furn_q:
                obj_q = obj_q.filter(furn_q)

        if listed_by_filter:
            role_values = LISTED_BY_ROLE_MAP.get(listed_by_filter, [listed_by_filter])
            if hasattr(db_model, 'listed_by_role'):
                role_q = Q()
                for rv in role_values:
                    role_q |= Q(listed_by_role__iexact=rv)
                obj_q = obj_q.filter(role_q)
            else:
                obj_q = obj_q.none()

        if bathrooms_filter:
            try:
                min_bath = int(bathrooms_filter)
                if hasattr(db_model, 'bathrooms'):
                    obj_q = obj_q.filter(bathrooms__gte=min_bath)
            except (ValueError, TypeError):
                pass

        for fk, fval in extra_filters.items():
            if not fval:
                continue
            fields = EXTRA_FIELD_MAP.get(fk, [])
            eq = Q()
            for f in fields:
                if hasattr(db_model, f):
                    field_obj = db_model._meta.get_field(f) if f in [x.name for x in db_model._meta.get_fields()] else None
                    is_bool = getattr(field_obj, 'get_internal_type', lambda: '')() == 'BooleanField' if field_obj else False
                    if is_bool or fval.lower() in ('1', 'yes', 'true'):
                        eq |= Q(**{f: True}) if is_bool else Q(**{f'{f}__iexact': 'yes'})
                    else:
                        eq |= Q(**{f'{f}__icontains': fval})
            if eq:
                obj_q = obj_q.filter(eq)

        if added_filter:
            try:
                days = int(added_filter)
                if hasattr(db_model, 'created_at'):
                    obj_q = obj_q.filter(created_at__gte=timezone.now() - timedelta(days=days))
            except (ValueError, TypeError):
                pass

        PRICE_FIELDS = ('monthly_rent', 'expected_rent', 'expected_price', 'plot_price', 'selling_price')
        if sort_filter == "price-asc":
            for pf in PRICE_FIELDS:
                if hasattr(db_model, pf):
                    obj_q = obj_q.order_by(pf)
                    break
        elif sort_filter == "price-desc":
            for pf in PRICE_FIELDS:
                if hasattr(db_model, pf):
                    obj_q = obj_q.order_by(f'-{pf}')
                    break
        elif sort_filter == "newest":
            obj_q = obj_q.order_by('-created_at' if hasattr(db_model, 'created_at') else f'-{pk_field}')
        else: 
            obj_q = obj_q.order_by(f'-{pk_field}')

        remaining = MAX_COLLECT - len(all_properties)
        for real_obj in obj_q[:remaining]:
            all_properties.append(_normalize_any_property(real_obj, category_tag, listing_type))

    paginator = Paginator(all_properties, PER_PAGE)
    page_obj  = paginator.get_page(page_number)

    active_filter_count = sum(1 for v in [areas_list, bhk_filter, budget_min, budget_max, furnishing_filter, prop_type_filter, verified_filter, listed_by_filter] if v)
    active_more_count = sum(1 for v in [verified_filter, lease_filter, bathrooms_filter, area_range_filter, age_filter, amenities_list, parking_filter, added_filter] if v)
    active_more_count += sum(1 for v in extra_filters.values() if v)

    context = {
        'properties': page_obj,
        'page_obj':   page_obj,
        'paginator':  paginator,
        'total':      len(all_properties),
        'category':     category if category else "all",
        'current_city': city_filter if city_filter else "Nagpur",
        'listing_type': listing_type,
        'areas_list':   areas_list,
        'areas_json':   json.dumps(areas_list),
        'current_bhk':        bhk_filter,
        'budget_min':         budget_min,
        'budget_max':         budget_max,
        'current_furnishing': furnishing_filter,
        'current_prop_type':  prop_type_filter,
        
        'filter_verified': verified_filter,
        'filter_listed_by':       listed_by_filter,
        'filter_listed_by_label': LISTED_BY_LABELS.get(listed_by_filter, ''),
        'filter_pet':      pet_filter,
        'filter_lease':    lease_filter,
        'amenities_list':  amenities_list,
        'amenities_json':  json.dumps(amenities_list),
        'current_sort':        sort_filter,
        'active_filter_count': active_filter_count,
        'active_more_count':   active_more_count,
        'extra_filters': extra_filters,
        'available_prop_types': available_prop_types,
    }

    return render(request, 'home_page/listingpage.html', context)


def _normalize_any_property(obj, url_category, listing_type):
    
    listed_by_name = (
        getattr(obj, 'listed_by_name', None)
        or getattr(obj, 'plot_owner_name', None)
        or getattr(obj, 'uploaded_by_name', None)
        or getattr(obj, 'owner_name', None)
    )
    listed_by_role = (
        getattr(obj, 'listed_by_role', None)
        or getattr(obj, 'plot_owner_role', None)
        or getattr(obj, 'uploaded_by_role', None)
    )

    images_list = []
    img_url = None
    image_count = 0
    if hasattr(obj, 'images') and obj.images.exists():
        for img_obj in obj.images.all():
            if img_obj and hasattr(img_obj, 'image') and img_obj.image:
                images_list.append(img_obj.image.url)
        image_count = len(images_list)
        img_url = images_list[0] if images_list else None

    elif hasattr(obj, 'property_image') and obj.property_image:
        img_url = obj.property_image.url
        image_count = 1

    video_url = _get_property_video_url(obj)

    price = "Price on Request"
    if hasattr(obj, 'monthly_rent') and obj.monthly_rent:
        price = f"₹{obj.monthly_rent:,}"
    elif hasattr(obj, 'selling_price') and obj.selling_price:
        try:
            val = float(obj.selling_price)
            price = f"₹{val/10000000:.2f} Cr" if val >= 10000000 else f"₹{val/100000:.2f} L" if val >= 100000 else f"₹{val:,.0f}"
        except Exception:
            price = f"₹{obj.selling_price}"
    elif hasattr(obj, 'plot_price') and obj.plot_price:
        try:
            val = float(obj.plot_price)
            price = f"₹{val/10000000:.2f} Cr" if val >= 10000000 else f"₹{val/100000:.2f} L" if val >= 100000 else f"₹{val:,.0f}"
        except Exception:
            price = f"₹{obj.plot_price}"

    title_val = getattr(obj, 'property_title', getattr(obj, 'plot_title', getattr(obj, 'title', None)))
    locality = getattr(obj, 'locality', getattr(obj, 'plot_locality', getattr(obj, 'village', '')))
    city = getattr(obj, 'city', getattr(obj, 'plot_city', ''))

    if not title_val:
        title_val = f"{url_category.capitalize()} Property in {locality}"

    # ── PRICE BREAKUP: Brokerage, Security Deposit, Advance Rent, Maintenance ──
    def _fmt_amt(val):
        try:
            v = float(val)
            if v <= 0:
                return None
            return f"₹{v:,.0f}"
        except (TypeError, ValueError):
            return None

    # Brokerage
    brokerage_display = None
    brokerage_label = "Brokerage"
    if hasattr(obj, 'get_brokerage_label'):
        try:
            brokerage_label = obj.get_brokerage_label()
        except Exception:
            pass
    if hasattr(obj, 'get_brokerage_amount'):
        try:
            b_val = obj.get_brokerage_amount()
            brokerage_display = _fmt_amt(b_val) or "No Brokerage"
        except Exception:
            brokerage_display = None
    if not brokerage_display:
        raw_brokerage = getattr(obj, 'brokerage_percentage', None)
        if raw_brokerage and str(raw_brokerage).strip().lower() == 'no brokerage':
            brokerage_display = "No Brokerage"
        elif raw_brokerage:
            brokerage_display = str(raw_brokerage)

    # Security Deposit
    security_deposit_display = None
    if hasattr(obj, 'get_security_deposit_amount'):
        try:
            sd_val = obj.get_security_deposit_amount()
            security_deposit_display = _fmt_amt(sd_val)
        except Exception:
            security_deposit_display = None
    if not security_deposit_display:
        raw_sd = getattr(obj, 'security_deposit_amount', None)
        security_deposit_display = _fmt_amt(raw_sd)

    # Advance Rent
    advance_rent_display = None
    if hasattr(obj, 'get_advance_rent_amount'):
        try:
            ar_val = obj.get_advance_rent_amount()
            advance_rent_display = _fmt_amt(ar_val)
        except Exception:
            advance_rent_display = None
    if not advance_rent_display:
        raw_ar = getattr(obj, 'advance_rent_amount', getattr(obj, 'advanced_rent_amount', None))
        advance_rent_display = _fmt_amt(raw_ar)

    # Maintenance
    maintenance_display = "Included in rent"
    m_type = (getattr(obj, 'maintenance_type', '') or '').strip().lower()
    m_amount = getattr(obj, 'monthy_maintenance_amount',
                 getattr(obj, 'maintenance_charges',
                   getattr(obj, 'maintenance_amount', None)))
    if ('extra' in m_type or 'exclud' in m_type) and m_amount:
        fmt_m = _fmt_amt(m_amount)
        if fmt_m:
            maintenance_display = f"{fmt_m}/mo"


        # Total Move-in Cost (already computed & stored by model's save())
    total_movein_display = None
    raw_total = getattr(obj, 'total_move_in_cost', None)
    total_movein_display = _fmt_amt(raw_total)
    if not total_movein_display:
        # Fallback: sum whatever pieces we do have
        try:
            pieces = []
            for d in (advance_rent_display, security_deposit_display, brokerage_display):
                if d and d.startswith('₹'):
                    pieces.append(float(d.replace('₹', '').replace(',', '')))
            if pieces:
                total_movein_display = f"₹{sum(pieces):,.0f}"
        except Exception:
            total_movein_display = None

    

    

    return {
        'id': obj.pk,
        'category': url_category,
        'url_category': url_category,
        'listing_type': listing_type,
        'title': title_val,
        'location': f"{locality}, {city}".strip(', '),
        'price_display': price,
        'image_url': img_url,
        'images_list': images_list,   
        'image_count': image_count,

        'uploaded_by_name': getattr(obj, 'uploaded_by_name', getattr(obj, 'owner_name', 'Unknown User')),
        'uploaded_by_role': getattr(obj, 'uploaded_by_role', 'Owner'),
        'listed_by_name': listed_by_name or 'Unknown User',
        'listed_by_role': (listed_by_role or 'owner').strip().lower(),

        'phone': getattr(obj, 'contact_number', getattr(obj, 'listed_by_contact', getattr(obj, 'phone_number', 'N/A'))),
        'area': getattr(obj, 'builtup_area', getattr(obj, 'built_up_area', getattr(obj, 'land_area', getattr(obj, 'plot_area', None)))),
        'beds': getattr(obj, 'bhk_type', getattr(obj, 'bhk', getattr(obj, 'total_beds', None))),
        'furnishing': getattr(obj, 'furnishing_status', None),
        'floor': getattr(obj, 'floor_no', None),
        'property_type': getattr(obj, 'property_type', getattr(obj, 'resale_plot_type', None)),
        'pg_for': getattr(obj, 'pg_for', None),
        'pet_friendly': getattr(obj, 'pet_friendly', False),
        'description': getattr(obj, 'property_description', getattr(obj, 'user_description', '')),
        'amenities': getattr(obj, 'amenities', []),
        'facing': getattr(obj, 'plot_road_facing', getattr(obj, 'facing_direction', None)),
        'brokerage_display': brokerage_display,
        'brokerage_label': brokerage_label,
        'security_deposit_display': security_deposit_display,
        'advance_rent_display': advance_rent_display,
        'maintenance_display': maintenance_display,

        'total_movein_display': total_movein_display,
        'video_url': video_url,
     
        
    }
    




def _get_property_video_url(obj):
    for related_name in ('video', 'videos', 'walkthrough_video'):
        related_manager = getattr(obj, related_name, None)
        if related_manager is None:
            continue
        try:
            video_obj = related_manager.all().first()
        except Exception:
            continue
        if not video_obj:
            continue
        video_file = getattr(video_obj, 'video', None)
        if video_file and getattr(video_file, 'name', None):
            try:
                return video_file.url
            except Exception:
                pass
        video_url_field = getattr(video_obj, 'video_url', None)
        if video_url_field:
            return video_url_field

    for field_name in ('property_video', 'social_video'):
        direct_file = getattr(obj, field_name, None)
        if direct_file and getattr(direct_file, 'name', None):
            try:
                return direct_file.url
            except Exception:
                pass

    for field_name in ('property_video_link',):
        direct_url = getattr(obj, field_name, None)
        if direct_url:
            return direct_url

    return None


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
    
    return render(request, 'home_page/login.html')


# ---------------- DASHBOARD ----------------
@login_required
def dashboard_view(request):
    return render(request, 'home_page/dashboard12.html')






# ---------------- POST PROPERTY ----------------


############### Views start for check email already exists or not ####################

@csrf_exempt
def Check_Email_Api(request):
    if request.method == "POST":
        email = request.POST.get('email', '').strip()
        # Check database for email
        user_exists = User_Details.objects.filter(user_email=email).exists()
        return JsonResponse({'exists': user_exists})
    return JsonResponse({'error': 'Invalid request'}, status=400)

########### Views end for check email already exists or not ##########################


########### Views start for if email exits directly login #########################

@csrf_exempt
def Prop_Login_Api(request):
    if request.method == "POST":
        try:
            user_identifier = request.POST.get('email', '').strip()
            password = request.POST.get('password', '')
            
            # Find the user by Email OR Phone
            user_qs = User_Details.objects.filter(
                Q(user_email=user_identifier) | Q(user_phone=user_identifier),
                user_password=password
            )
            
            if user_qs.exists():
                user_obj = user_qs.first()
                
                # 🟢 EXACT MATCH TO YOUR ORIGINAL SESSION LOGIC
                request.session['User_id'] = str(user_obj.id)
                request.session['user_type'] = user_obj.user_role
                
                # 🟢 DYNAMIC REDIRECT LOGIC
                if user_obj.user_role == 'Relationship Manager':
                    url = reverse('rm_dashboard') 
                else:
                    url = reverse('index')
                
                return JsonResponse({
                    'status': '1', 
                    'msg': 'Success!',
                    'redirect_url': url,
                    'user_name': user_obj.user_name,   
                    'user_role': user_obj.user_role,
                    'user_email': user_obj.user_email
                })

            return JsonResponse({'status': '0', 'msg': 'Incorrect password or user not found.'})

        except Exception as e:
            print(traceback.format_exc())
            return JsonResponse({'status': '0', 'msg': 'Something went wrong'})
            
    return JsonResponse({'status': '0', 'msg': 'Invalid request.'})

############ Views end for if email exists directly login ############################


############ Views start for send otp to email #############################

@csrf_exempt
def Send_Otp_Api(request):
    if request.method == "POST":
        user_identifier = request.POST.get('email', '').strip()
        otp = str(random.randint(1000, 9999))
        
        request.session['auth_otp'] = otp
        request.session['auth_identifier'] = user_identifier
        
        # 🟢 CRITICAL FIX: Force Django to save the session immediately
        request.session.modified = True 
        
        if '@' in user_identifier:
            try:
                send_mail(
                    subject='Your PropCRM Verification Code',
                    message=f'Hello!\n\nYour 4-digit verification code is: {otp}\n\nDo not share this code with anyone.',
                    from_email=None, 
                    recipient_list=[user_identifier],
                    fail_silently=True,
                )
            except Exception as e:
                print(f"Mail Error: {e}")
                
        print(f" OTP FOR {user_identifier}: {otp}")
        return JsonResponse({'status': 'success'})
    return JsonResponse({'error': 'Invalid request'}, status=400)

########## Views end for send otp to email ###########################


########## Views start for verify otp for email ########################

@csrf_exempt
def Verify_Otp_Api(request):
    if request.method == "POST":
        user_identifier = request.POST.get('email', '').strip()
        submitted_otp = request.POST.get('otp', '').strip()
        
        actual_otp = request.session.get('auth_otp')
        session_identifier = request.session.get('auth_identifier')
        
        if submitted_otp == actual_otp and user_identifier == session_identifier:
            #  CRITICAL FIX: Set a dedicated success flag and save immediately
            request.session['otp_verified_for'] = user_identifier
            request.session.modified = True
            return JsonResponse({'valid': True})
        else:
            return JsonResponse({'valid': False})
            
    return JsonResponse({'error': 'Invalid request'}, status=400)

########### Views end for verify otp for email #############################


############# Views start for user registration #########################

@csrf_exempt
def Prop_Register_Api(request):
    if request.method == "POST":
        user_identifier = request.POST.get('email', '').strip()
        name = request.POST.get('name', '').strip()
        mobile = request.POST.get('mobile', '').strip()
        role = request.POST.get('role', '').strip()
        
        #  CRITICAL FIX: Check the new success flag instead of the raw email
        verified_user = request.session.get('otp_verified_for')
        if verified_user != user_identifier:
             return JsonResponse({'status': '0', 'msg': 'Security timeout. Please request a new OTP.'})
             
        try:
            email_val = user_identifier if '@' in user_identifier else ''

            generated_password = get_random_string(
                length=12, 
                allowed_chars='abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^*'
            )
            
            # 1. Save user object details
            new_user = User_Details(
                user_email=email_val,
                user_name=name,
                user_phone=mobile,
                user_role=role,
                user_password=generated_password,
                user_register_date=datetime.today(),
                user_register_time=datetime.now()
            )
            new_user.save()
            
            # 2.  RENDER AND SEND EXTERNAL HTML EMAIL TEMPLATE
            if email_val:
                subject = "Welcome to PropCRM! "
                login_link = request.build_absolute_uri('/') 
                
                # Context variables to map directly into the template
                context = {
                    'name': name,
                    'email': email_val,
                    'role': role,
                    'login_link': login_link
                }
                
                # Compiles the standalone HTML file with our context data
                html_message = render_to_string('emails/welcome_mail.html', context)
                
                # Plain text version fallback for strict email clients
                plain_message = strip_tags(html_message)

                send_mail(
                    subject=subject,
                    message=plain_message,
                    from_email=None, 
                    recipient_list=[email_val],
                    html_message=html_message,
                    fail_silently=False,
                )
            
            # 3. Handle active user sessions setups
            request.session['User_id'] = str(new_user.id)
            request.session['user_type'] = new_user.user_role
            
            request.session.pop('auth_otp', None)
            request.session.pop('auth_identifier', None)
            request.session.pop('otp_verified_for', None)
            request.session.modified = True
            
            return JsonResponse({'status': '1', 'msg': 'Account Created Successfully!'})
            
        except Exception as e:
            print(traceback.format_exc())
            return JsonResponse({'status': '0', 'msg': f"Server Error: {str(e)}"})
            
    return JsonResponse({'status': '0', 'msg': 'Invalid request.'})

############ Views end for user registration ##############################


############# Views start for wishlist properties ######################

def Wishlist_Property(request):
    context = {}
    # ═══════════════════════════════════════════════════════
    # HANDLE LOGGED-IN USER
    # ═══════════════════════════════════════════════════════
    session_id = request.session.get('User_id')
    if session_id:
        user_obj = User_Details.objects.filter(id=session_id).first()
        if user_obj:     
            wishlist_property = WishlistProperty.objects.filter(user=user_obj).order_by('-id')
            context = {'user_obj':user_obj,
            'wishlist_property':wishlist_property}

    return render(request,'home_page/Wishlist/wishlist.html',context)

############## Views end for wishlist properties #######################


############# Views start for ajax for add property to wishlist ##################

@csrf_exempt
def Wishlist_Ajax(request):
    if request.method == "POST":
        data = request.POST.dict()   
        
        # 1.  SECURITY FIX: Get the user ID from the secure session, NOT the frontend data
        user_id = request.session.get('User_id')
        if not user_id:
            return JsonResponse({"status": "0", "msg": "User not authenticated. Please log in."})

        try:
            user_data = User_Details.objects.get(id=user_id)
        except User_Details.DoesNotExist:
            return JsonResponse({"status": "0", "msg": "Invalid user session."})

        real_property = None
        property_id = data.get('property_id')
        
        # 2.  CRASH PREVENTION: Safely try to get the property
        try:
            if data['listing_type'] == "rent" and data['category'] == "Residential Data":
                real_property = RentalResidentialProperty.objects.get(id=property_id)

            elif data['listing_type'] == "rent" and data['category'] == "PG Data":
                real_property = PGColivingProperty.objects.get(id=property_id)

            elif data['listing_type'] == "rent" and data['category'] == "Commercial Data":
                real_property = CommercialProperty.objects.get(id=property_id)

        except ObjectDoesNotExist:
            return JsonResponse({"status": "0", "msg": "Property not found in the database."})

        if not real_property:
            return JsonResponse({"status": "0", "msg": "Invalid property type or category."})
        
        property_content_type = ContentType.objects.get_for_model(real_property)

        # 3. TOGGLE LOGIC: Check if it's already in the wishlist
        # If it exists, delete it (Remove from wishlist)
        wishlist_item = WishlistProperty.objects.filter(
            content_type=property_content_type, 
            object_id=real_property.id, 
            user=user_data
        ).first()
        
        if wishlist_item:
            wishlist_item.delete()
            return JsonResponse({
                "status": "1", 
                "action": "removed", 
                "msg": "Property removed from wishlist."
            })
            
        # If it doesn't exist, create it (Add to wishlist)
        else:
            WishlistProperty.objects.create(
                content_type=property_content_type, # Passes the model type (e.g. CommercialProperty)
                object_id=real_property.id,         # Passes the ID (e.g. 5)
                user=user_data,
                wishlist_date=datetime.today(),
                wishlist_time=datetime.now()
            )
            return JsonResponse({
                "status": "1", 
                "action": "added", 
                "msg": "Property added to wishlist successfully!"
            })

    return JsonResponse({"status": "0", "msg": "Invalid request method."})

############ Views end for ajax for add property to wishlist #########################














def get_featured_queryset(model):
    return model.objects.filter(
       
    ).order_by('-created_at')[:6]






@require_POST
def track_interaction(request):
    prop_id = request.POST.get('id')
    prop_type = request.POST.get('type')       # must match a PROPERTY_REGISTRY key
    action = request.POST.get('action')         # view / click / whatsapp / call

    entry = PROPERTY_REGISTRY.get(prop_type)
    if entry and prop_id and action:
        PropertyInteraction.objects.create(
            content_type=ContentType.objects.get_for_model(entry['model']),
            object_id=prop_id,
            interaction_type=action,
            ip_address=request.META.get('REMOTE_ADDR'),
        )
        return JsonResponse({'ok': True})
    return JsonResponse({'ok': False}, status=400)


from datetime import datetime, timedelta





from itertools import chain








def _clean_short_text(value, max_len=28, max_words=5):
    """Reject anything that looks like a dumped property title/slug
    (too long, too many words) — only pass through genuine short search terms
    like 'Manish Nagar', '2BHK', 'Wardha Road'."""
    if not value:
        return None
    value = value.strip()
    if not value or len(value) > max_len or len(value.split()) > max_words:
        return None
    if any(ch in value for ch in ('(', ')', ',')):
        return None
    return value



CATEGORY_LABELS = {
    'residential': 'Residential',
    'commercial': 'Commercial',
    'pg': 'PG / Co-living',
    'plot': 'Plot / Land',
    'industrial': 'Industrial',
    'agricultural': 'Agricultural',
}


def index(request):
    today = timezone.localdate()
    fifteen_days_ago = today - timedelta(days=15)

    # ==========================================
    # RENTAL PROPERTIES
    # ==========================================
    rental_residential = RentalResidentialProperty.objects.filter(is_deleted=False).prefetch_related('images').order_by('-created_at')[:4]
    rental_commercial = CommercialRentalProperty.objects.filter(is_deleted=False).prefetch_related('images').order_by('-created_at')[:4]
    rental_pg = PGColivingProperty.objects.filter(is_deleted=False).prefetch_related('images').order_by('-created_at')[:4]

    # ==========================================
    # RESALE PROPERTIES
    # ==========================================
    resale_residential = ResaleResidentialProperty.objects.filter(is_deleted=False).prefetch_related('images').order_by('-created_at')[:4]
    resale_commercial = CommercialResaleProperty.objects.filter(is_deleted=False).prefetch_related('images').order_by('-created_at')[:4]
    resale_industrial = IndustrialResaleProperty.objects.filter(is_deleted=False).prefetch_related('images').order_by('-created_at')[:4]
    resale_agricultural = AgriculturalResaleProperty.objects.filter(is_deleted=False).prefetch_related('images').order_by('-created_at')[:4]

    resale_plots_combined = list(chain(
        PlotSaleProperty.objects.filter(is_deleted=False).prefetch_related('images').order_by('-created_at')[:4],
        ResidentialPlotResaleProperty.objects.filter(is_deleted=False).prefetch_related('images').order_by('-created_at')[:4],
        CommercialPlotResaleProperty.objects.filter(is_deleted=False).prefetch_related('images').order_by('-created_at')[:4],
        IndustrialPlotResaleProperty.objects.filter(is_deleted=False).prefetch_related('images').order_by('-created_at')[:4],
        AgriculturalPlotResaleProperty.objects.filter(is_deleted=False).prefetch_related('images').order_by('-created_at')[:4]
    ))
    resale_plots_combined.sort(key=lambda x: getattr(x, 'created_at'), reverse=True)
    resale_plot = resale_plots_combined[:4]

    rental_map = {"Residential": rental_residential, "Commercial": rental_commercial, "PG / Co-Living": rental_pg}
    resale_map = {
        "Residential": resale_residential, "Commercial": resale_commercial,
        "Plots / Land": resale_plot, "Industrial": resale_industrial, "Agricultural": resale_agricultural,
    }

    # ==========================================
    # OTHER DATA
    # ==========================================
    hero = HeroSection.objects.filter(is_active=True).first()
    seo_pages = LocationSEO.objects.filter(is_active=True, pagetype="blog")
    services = LocationSEO.objects.filter(pagetype="service", is_active=True)
    subscriptions = Subscription_Details.objects.all()
    faqs_obj = NormalFAQ.objects.all().order_by('-id')

    active_ads = BrandAd.objects.filter(is_active=True, start_date__lte=today, end_date__gte=today)
    localities = RentalResidentialProperty.objects.values('locality_area').annotate(count=Count('id')).order_by('-count')[:7]

    brand_ads = active_ads.filter(placement='native')[:4]
    if brand_ads:
        BrandAd.objects.filter(pk__in=[a.pk for a in brand_ads]).update(impressions=F('impressions') + 1)

    since_30d = timezone.now() - timedelta(days=30)

    # ==========================================
    # POPULAR SEARCHES — sanitized, short pills only (fixes the huge garbage-text chips)
    # ==========================================
    popular_searches = []
    raw_searches = (
        SearchLog.objects.filter(created_at__gte=since_30d)
        .exclude(area='').exclude(area__isnull=True)
        .values('area', 'listing_type')
        .annotate(total=Count('id'))
        .order_by('-total')
    )
    for row in raw_searches:
        clean_area = _clean_short_text(row['area'])
        if not clean_area:
            continue
        lt = row['listing_type'] or 'rent'
        popular_searches.append({
            'area': clean_area,
            'listing_type': lt,
            'label': f"{clean_area} · {'For Rent' if lt == 'rent' else 'For Sale'}",
            'total': row['total'],
            'url': f"/listingpage/?type={lt}&area={clean_area}",
        })
        if len(popular_searches) >= 6:
            break

    # ==========================================
    # POPULAR LOCALITIES — sanitized area names only
    # ==========================================
    popular_localities = []
    raw_localities = (
        SearchLog.objects.filter(created_at__gte=since_30d)
        .exclude(area='').exclude(area__isnull=True)
        .values('area')
        .annotate(total=Count('id'))
        .order_by('-total')
    )
    for row in raw_localities:
        clean_area = _clean_short_text(row['area'], max_len=24, max_words=4)
        if not clean_area:
            continue
        popular_localities.append({
            'area': clean_area,
            'total': row['total'],
            'url': f"/listingpage/?area={clean_area}",
        })
        if len(popular_localities) >= 7:
            break

    # ==========================================
    # TOP CITIES — sanitized city names only
    # ==========================================
    top_cities_search = []
    raw_cities = (
        SearchLog.objects.filter(created_at__gte=since_30d)
        .exclude(city='').exclude(city__isnull=True)
        .values('city')
        .annotate(total=Count('id'))
        .order_by('-total')
    )
    for row in raw_cities:
        clean_city = _clean_short_text(row['city'], max_len=24, max_words=3)
        if not clean_city:
            continue
        top_cities_search.append({
            'city': clean_city,
            'total': row['total'],
            'url': f"/listingpage/?city_filter={clean_city}",
        })
        if len(top_cities_search) >= 4:
            break

    # ==========================================
    # BHK counts (unchanged)
    # ==========================================
    bhk_counter = Counter()
    for key, entry in PROPERTY_REGISTRY.items():
        if entry['bhk_field']:
            qs = (
                entry['model'].objects.filter(is_deleted=False)
                .exclude(**{f"{entry['bhk_field']}__isnull": True})
                .exclude(**{entry['bhk_field']: ''})
                .values(entry['bhk_field']).annotate(total=Count('pk'))
            )
            for row in qs:
                bhk_key = (row[entry['bhk_field']] or '').replace(' ', '').upper()
                bhk_counter[bhk_key] += row['total']
    bhk_counts = dict(bhk_counter)

    category_counts = {key: entry['model'].objects.filter(is_deleted=False).count() for key, entry in PROPERTY_REGISTRY.items()}

    # ==========================================
    # Trending properties (unchanged)
    # ==========================================
    trending = (
        PropertyInteraction.objects.filter(interaction_type='view', created_at__gte=since_30d)
        .values('content_type', 'object_id').annotate(total=Count('id')).order_by('-total')[:8]
    )
    trending_props = []
    ct_map = {ContentType.objects.get_for_model(e['model']).id: (key, e) for key, e in PROPERTY_REGISTRY.items()}
    for row in trending:
        key, entry = ct_map.get(row['content_type'], (None, None))
        if entry:
            obj = entry['model'].objects.filter(pk=row['object_id'], is_deleted=False).first()
            if obj:
                trending_props.append({'type': key, 'data': obj, 'views': row['total']})

    # ==========================================
    # LIVE STATS (unchanged)
    # ==========================================
    live_stats = {
        'total_searches': SearchLog.objects.filter(created_at__gte=since_30d).count(),
        'total_views': PropertyInteraction.objects.filter(interaction_type='view', created_at__gte=since_30d).count(),
        'total_whatsapp_clicks': PropertyInteraction.objects.filter(interaction_type='whatsapp', created_at__gte=since_30d).count(),
        'total_listings_live': sum(category_counts.values()),
    }

    # ==========================================
    # USER SESSION
    # ==========================================
    user_obj = None
    session_id = request.session.get('User_id')
    if session_id:
        user_obj = User_Details.objects.filter(id=session_id).first()

    ad_footer = active_ads.filter(placement='footer').first()
    ad_leaderboard_slides = list(active_ads.filter(placement='leaderboard')[:5])
    if ad_leaderboard_slides:
        BrandAd.objects.filter(pk__in=[a.pk for a in ad_leaderboard_slides]).update(impressions=F('impressions') + 1)

    # ==========================================
    # Featured Properties (unchanged)
    # ==========================================
    featured_props = []
    for type_key, entry in PROPERTY_REGISTRY.items():
        qs = entry['model'].objects.filter(is_deleted=False).prefetch_related('images').order_by('-created_at')[:2]
        for obj in qs:
            featured_props.append({'type': type_key, 'listing_type': entry['listing_type'], 'url_category': entry['category'], 'data': obj})
    featured_props.sort(key=lambda x: x['data'].created_at, reverse=True)
    featured_props = featured_props[:8]

    context = {
        "hero": hero,
        "seo_pages": seo_pages,
        "today": today,
        "fifteen_days_ago": fifteen_days_ago,
        "user_obj": user_obj,
        "services": services,
        "subscriptions": subscriptions,
        "rental_map": rental_map,
        "resale_map": resale_map,
        "faqs_obj": faqs_obj,
        'brand_ads': brand_ads,
        'ad_footer': ad_footer,
        'ad_leaderboard_slides': ad_leaderboard_slides,
        'top_localities': localities,
        'popular_searches': popular_searches,
        'popular_localities': popular_localities,
        'top_cities': top_cities_search,
        'bhk_counts': bhk_counts,
        'category_counts': category_counts,
        'trending_props': trending_props,
        'featured_props': featured_props,
        'live_stats': live_stats,
    }

    return render(request, "home_page/index.html", context)


@require_POST
def track_search_click(request):
    SearchLog.objects.create(
        area=request.POST.get('area', '')[:100],
        city=request.POST.get('city', '')[:100],
        listing_type=request.POST.get('listing_type', 'rent')[:10],
        category=request.POST.get('category', '')[:30],
        bhk=request.POST.get('bhk', '')[:20],
    )
    return JsonResponse({'ok': True})
















from django.db.models import Count



# ==========================================
# SERVICES VIEWS
# ==========================================
def services(request):
    active_services = Service.objects.filter(status="active").order_by('sort_order', 'title')
    
    for s in active_services:
        # Fetch the real SEO slug from the database
        seo_record = LocationSEO.objects.filter(pagetype="service", object_id=str(s.id)).first()
        # Fallback to key if slug is missing for any reason
        s.seo_slug = seo_record.slug if seo_record and seo_record.slug else f"service-{s.id}"

    context = {'services': active_services}
    # ... (keep your user session logic here)
    return render(request, "home_page/services.html", context)


def services_details(request, slug):
    # Search by slug instead of key
    seo = LocationSEO.objects.filter(slug=slug, pagetype="service", is_active=True).first()
    if not seo:
        raise Http404("Service not found")
        
    service = seo.content_object
    keywords = seo.secondary_keywords.split(",") if seo.secondary_keywords else []

    return render(request, "home_page/services_details.html", {
        "seo": seo, "service": service, "keywords": keywords
    })


# ==========================================
# BLOG VIEWS
# ==========================================


from django.db.models import Count

def blog(request):
    # FIX: Used status__iexact to ignore case-sensitivity issues between "Published" and "published"
    blogs = Blog.objects.filter(status__iexact="published").order_by("-published_date")
    
    category_query = request.GET.get('category')
    if category_query:
        blogs = blogs.filter(category=category_query)
        
    for b in blogs:
        # Fetch the real SEO slug from the database
        seo_record = LocationSEO.objects.filter(pagetype="blog", object_id=str(b.id)).first()
        b.seo_slug = seo_record.slug if seo_record and seo_record.slug else f"blog-{b.id}"

    # FIX: Also applied __iexact to the category aggregation so the counts are accurate
    cat_data = Blog.objects.filter(status__iexact="published").values('category').annotate(count=Count('category'))
    
    # Optional: You can add the styling dictionaries back here if you want colored icons on the frontend
    guide_categories = [{'name': c['category'], 'count': c['count']} for c in cat_data if c['category']]

    context = {"blogs": blogs, "guide_categories": guide_categories}
    
    # (keep your user session logic here)
    
    return render(request, "home_page/blog.html", context)

    

def blog_details(request, slug):
    # Search by slug instead of key
    seo = LocationSEO.objects.filter(slug=slug, pagetype="blog", is_active=True).first()
    if not seo:
        raise Http404("Blog not found")
        
    blog = seo.content_object
    return render(request, "home_page/blog_details.html", {"seo": seo, "blog": blog})




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



def all_faqs(request):
    from Main_App.models import PropertyFAQ
    faqs = PropertyFAQ.objects.all().order_by('-created_at')

    return render(request, "home_page/all_faqs.html", {
        "faqs": faqs
    })
    
    
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

    context = {
        'faq_sections':faq_sections
    }

    session_id = request.session.get('User_id')
    if session_id:
        user_obj = User_Details.objects.filter(id=session_id).first()
        if user_obj:
            context['user_obj'] = user_obj

    return render(request, "home_page/property_faq.html",context)



from django.db.models import F


# --- ADD BRAND AD PAGE ---

def add_brand_ad(request):
    if request.method == 'POST':
        brand_name = request.POST.get('brand_name', '').strip()
        tagline = request.POST.get('tagline', '').strip()
        click_url = request.POST.get('click_url', '').strip()
        placement = request.POST.get('placement')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        is_active = request.POST.get('is_active') == 'on'
        logo = request.FILES.get('logo')
        banner_image = request.FILES.get('banner_image')

        # Basic validation
        errors = []
        if not brand_name:
            errors.append("Brand name is required.")
        if not click_url:
            errors.append("Click URL is required.")
        if placement not in ('leaderboard', 'native'):
            errors.append("Please select a valid placement.")
        if not start_date or not end_date:
            errors.append("Start and end dates are required.")
        if placement == 'leaderboard' and not banner_image:
            errors.append("Banner image is required for Leaderboard placement.")
        if placement == 'footer':
            banner_image = request.FILES.get('footer_banner_image')
        if not banner_image:
            errors.append("Banner image is required for Footer placement.")
        if placement == 'native' and not logo:
            errors.append("Logo is required for Native Strip placement.")

        if errors:
            for e in errors:
                messages.error(request, e)
            return render(request, 'home_page/add_brand_ad.html', {'form_data': request.POST})

        BrandAd.objects.create(
            brand_name=brand_name,
            tagline=tagline,
            click_url=click_url,
            placement=placement,
            start_date=start_date,
            end_date=end_date,
            is_active=is_active,
            logo=logo,
            banner_image=banner_image,
        )
        messages.success(request, f"Ad for '{brand_name}' created successfully.")
       # return redirect('brand_ad_list')

    return render(request, 'home_page/add_brand_ad.html')





@csrf_exempt
def log_search(request):
    if request.method == 'POST':
        d = json.loads(request.body)
        SearchLog.objects.create(
            listing_type=d.get('listing_type',''),
            category=d.get('category',''),
            bhk=d.get('bhk'),
            sub=d.get('sub'),
            area=d.get('area'),
            city=d.get('city'),
        )
        return JsonResponse({'ok': True})
    return JsonResponse({'ok': False}, status=405)


def popular_searches_api(request):
    category = request.GET.get('category', 'residential')
    listing_type = request.GET.get('type', 'rent')

    qs = SearchLog.objects.filter(category=category, listing_type=listing_type)

    top_bhk = (qs.exclude(bhk__isnull=True).exclude(bhk='')
                 .values('bhk').annotate(c=Count('id')).order_by('-c')[:4])
    top_sub = (qs.exclude(sub__isnull=True).exclude(sub='')
                 .values('sub').annotate(c=Count('id')).order_by('-c')[:4])
    top_area = (qs.exclude(area__isnull=True).exclude(area='')
                  .values('area').annotate(c=Count('id')).order_by('-c')[:6])

    return JsonResponse({
        'bhk': list(top_bhk),
        'sub': list(top_sub),
        'area': list(top_area),
    })


def popular_localities_api(request):
    # Real counts from your actual property tables — adjust model names to yours
    from django.db.models import Count
    localities = (
        RentalResidentialProperty.objects.values('locality')
        .annotate(c=Count('id')).order_by('-c')[:7]
    )
    return JsonResponse({'localities': list(localities)})





def property_analytics(request):
    """
    Standalone analytics dashboard — separate from the public homepage.
    Per category (all 11): weekly/monthly search volume, top keywords,
    view/click/whatsapp/call counts. Plus sitewide top properties & keywords.
    """
    now = timezone.now()
    week_ago = now - timedelta(days=7)
    month_ago = now - timedelta(days=30)

    CATEGORY_LABELS = {
        'rental_residential': 'Residential — Rent',
        'rental_commercial': 'Commercial — Rent',
        'rental_pg': 'PG / Co-living — Rent',
        'resale_residential': 'Residential — Sale',
        'resale_commercial': 'Commercial — Sale',
        'resale_industrial': 'Industrial — Sale',
        'resale_agricultural': 'Agricultural — Sale',
        'plot_residential': 'Residential Plot',
        'plot_commercial': 'Commercial Plot',
        'plot_industrial': 'Industrial Plot',
        'plot_agricultural': 'Agricultural Plot',
    }

    category_stats = []
    for key, entry in PROPERTY_REGISTRY.items():
        base_sl = SearchLog.objects.filter(
            listing_type=entry['listing_type'], category=entry['category']
        )

        weekly_searches = base_sl.filter(created_at__gte=week_ago).count()
        monthly_searches = base_sl.filter(created_at__gte=month_ago).count()

        top_keywords = list(
            base_sl.filter(created_at__gte=month_ago)
            .exclude(area='').exclude(area__isnull=True)
            .values('area')
            .annotate(total=Count('id'))
            .order_by('-total')[:5]
        )

        ct = ContentType.objects.get_for_model(entry['model'])
        base_pi = PropertyInteraction.objects.filter(content_type=ct)

        weekly_views     = base_pi.filter(interaction_type='view',     created_at__gte=week_ago).count()
        monthly_views    = base_pi.filter(interaction_type='view',     created_at__gte=month_ago).count()
        weekly_clicks    = base_pi.filter(interaction_type='click',    created_at__gte=week_ago).count()
        monthly_clicks   = base_pi.filter(interaction_type='click',    created_at__gte=month_ago).count()
        weekly_whatsapp  = base_pi.filter(interaction_type='whatsapp', created_at__gte=week_ago).count()
        monthly_whatsapp = base_pi.filter(interaction_type='whatsapp', created_at__gte=month_ago).count()
        weekly_calls     = base_pi.filter(interaction_type='call',     created_at__gte=week_ago).count()
        monthly_calls    = base_pi.filter(interaction_type='call',     created_at__gte=month_ago).count()

        category_stats.append({
            'key': key,
            'label': CATEGORY_LABELS.get(key, key),
            'live_count': entry['model'].objects.filter(is_deleted=False).count(),
            'weekly_searches': weekly_searches,
            'monthly_searches': monthly_searches,
            'top_keywords': top_keywords,
            'weekly_views': weekly_views, 'monthly_views': monthly_views,
            'weekly_clicks': weekly_clicks, 'monthly_clicks': monthly_clicks,
            'weekly_whatsapp': weekly_whatsapp, 'monthly_whatsapp': monthly_whatsapp,
            'weekly_calls': weekly_calls, 'monthly_calls': monthly_calls,
        })

    def top_properties_by(interaction_type, since, limit=10):
        rows = (
            PropertyInteraction.objects.filter(interaction_type=interaction_type, created_at__gte=since)
            .values('content_type', 'object_id')
            .annotate(total=Count('id'))
            .order_by('-total')[:limit]
        )
        ct_map = {ContentType.objects.get_for_model(e['model']).id: (k, e) for k, e in PROPERTY_REGISTRY.items()}
        results = []
        for row in rows:
            key, entry = ct_map.get(row['content_type'], (None, None))
            if not entry:
                continue
            obj = entry['model'].objects.filter(pk=row['object_id']).first()
            if obj:
                results.append({
                    'title': getattr(obj, 'property_title', str(obj.pk)),
                    'category': CATEGORY_LABELS.get(key, key),
                    'total': row['total'],
                    'id': obj.pk,
                })
        return results

    context = {
        'category_stats': category_stats,
        'top_viewed_properties': top_properties_by('view', month_ago),
        'top_whatsapp_properties': top_properties_by('whatsapp', month_ago),
        'top_keywords_weekly': list(
            SearchLog.objects.filter(created_at__gte=week_ago)
            .exclude(area='').exclude(area__isnull=True)
            .values('area').annotate(total=Count('id')).order_by('-total')[:10]
        ),
        'top_keywords_monthly': list(
            SearchLog.objects.filter(created_at__gte=month_ago)
            .exclude(area='').exclude(area__isnull=True)
            .values('area').annotate(total=Count('id')).order_by('-total')[:10]
        ),
        'total_searches_week': SearchLog.objects.filter(created_at__gte=week_ago).count(),
        'total_searches_month': SearchLog.objects.filter(created_at__gte=month_ago).count(),
    }
    return render(request, 'Search_log/property_analytics.html', context)