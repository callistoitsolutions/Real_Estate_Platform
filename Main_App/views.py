
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
        'phone': p.contact_number or "",
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
        'price_display': f"₹{p.expected_price or 0}",
        'location': f"{p.locality}, {p.city}" if hasattr(p, 'locality') else p.city or "—",
        'beds': "—",
        'baths': "—",
        'area': f"{p.plot_area or '—'} sq.ft" if hasattr(p, 'plot_area') else "—",
        'floor': "—",
        'furnished': "—",
        'property_type': "Plot",
        'listing_type': 'sale',
        'category': 'plot',
        'owner': p.owner_name or "Owner",
        'owner_role': "Plot Owner",
        'owner_initials': p.owner_name[:2].upper() if p.owner_name else "OW",
        'phone': p.contact_number or "",
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
        'phone': p.contact_number or "",
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
        'phone': p.contact_number or "",
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



def property_detail_view(request, listing_type, category, pk):

    obj = None
    p = None

    amenities_list = []
    facilities_list = []
    property_images = []

    seo_page_type = ""

    # =====================================================
    # RENT PROPERTIES
    # =====================================================

    if listing_type == 'rent':

        # =================================================
        # RENT RESIDENTIAL
        # =================================================

        if category in ['residential', 'residential-data']:

            obj = get_object_or_404(
                RentalResidentialProperty,
                pk=pk
            )

            seo_page_type = "rental_residential"

            p = _normalize_rental(obj)

            property_images = obj.images.all()

            if hasattr(obj, 'amenities') and obj.amenities:

                amenities_list = [
                    x.strip()
                    for x in obj.amenities.split(',')
                    if x.strip()
                ]

            if hasattr(obj, 'facilities') and obj.facilities:

                facilities_list = [
                    x.strip()
                    for x in obj.facilities.split(',')
                    if x.strip()
                ]

        # =================================================
        # COMMERCIAL RENTAL
        # =================================================

        elif category in ['commercial', 'commercial-data']:

            obj = get_object_or_404(
                CommercialRentalProperty,
                pk=pk
            )

            seo_page_type = "commercial_rental"

            p = _normalize_commercial_rental(obj)

            property_images = obj.images.all()

            if hasattr(obj, 'amenities') and obj.amenities:

                amenities_list = [
                    x.strip()
                    for x in str(obj.amenities).split(',')
                    if x.strip()
                ]

            if hasattr(obj, 'nearby_facilities') and obj.nearby_facilities:

                facilities_list = [
                    x.strip()
                    for x in str(obj.nearby_facilities).split(',')
                    if x.strip()
                ]

        # =================================================
        # PG PROPERTY
        # =================================================

        elif category in ['pg', 'pg-data']:

            obj = get_object_or_404(
                PGColivingProperty,
                pk=pk
            )

            seo_page_type = "pg_coliving"

            p = _normalize_pg(obj)

            property_images = obj.images.all()

            if hasattr(obj, 'amenities') and obj.amenities:

                amenities_list = [
                    x.strip()
                    for x in obj.amenities.split(',')
                    if x.strip()
                ]

            if hasattr(obj, 'nearby_facilities') and obj.nearby_facilities:

                facilities_list = [
                    x.strip()
                    for x in obj.nearby_facilities.split(',')
                    if x.strip()
                ]

    # =====================================================
    # SALE PROPERTIES
    # =====================================================

    elif listing_type == 'sale':

        # =================================================
        # RESALE RESIDENTIAL
        # =================================================

        if category in ['residential', 'resale-residential']:

            obj = get_object_or_404(
                ResaleResidentialProperty,
                pk=pk
            )

            seo_page_type = "resale_residential"

            p = _normalize_resale(obj)

            property_images = obj.images.all()

            if hasattr(obj, 'amenities') and obj.amenities:

                amenities_list = [
                    x.strip()
                    for x in obj.amenities.split(',')
                    if x.strip()
                ]

            if hasattr(obj, 'nearby_facilities') and obj.nearby_facilities:

                facilities_list = [
                    x.strip()
                    for x in obj.nearby_facilities.split(',')
                    if x.strip()
                ]

        # =================================================
        # COMMERCIAL RESALE
        # =================================================

        elif category in ['commercial', 'commercial-resale']:

            obj = get_object_or_404(
                CommercialResaleProperty,
                pk=pk
            )

            seo_page_type = "commercial_resale"

            p = _normalize_commercial_resale(obj)

            property_images = obj.images.all()

            if hasattr(obj, 'amenities') and obj.amenities:

                amenities_list = [
                    x.strip()
                    for x in obj.amenities.split(',')
                    if x.strip()
                ]

            if hasattr(obj, 'nearby_facilities') and obj.nearby_facilities:

                facilities_list = [
                    x.strip()
                    for x in obj.nearby_facilities.split(',')
                    if x.strip()
                ]

        # =================================================
        # PLOT SALE
        # =================================================

        elif category in ['plot', 'plot-resale']:

            obj = get_object_or_404(
                PlotSaleProperty,
                pk=pk
            )

            seo_page_type = "plot_sale"

            p = _normalize_plot(obj)

            property_images = obj.images.all()

        # =================================================
        # INDUSTRIAL SALE
        # =================================================

        elif category in ['industrial', 'industrial-resale']:

            obj = get_object_or_404(
                IndustrialResaleProperty,
                pk=pk
            )

            seo_page_type = "industrial_sale"

            p = _normalize_industrial(obj)

            property_images = obj.images.all()

        # =================================================
        # AGRICULTURAL SALE
        # =================================================

        elif category in ['agriculture', 'agricultural-data']:

            obj = get_object_or_404(
                AgriculturalResaleProperty,
                pk=pk
            )

            seo_page_type = "agriculture_sale"

            p = _normalize_agriculture(obj)

            property_images = obj.images.all()

    # =====================================================
    # PROPERTY NOT FOUND
    # =====================================================

    if not p:

        return render(
            request,
            'home_page/property_not_found.html'
        )

    # =====================================================
    # SEO DATA
    # =====================================================

    seo = LocationSEO.objects.filter(

        content_type=ContentType.objects.get_for_model(obj),

        object_id=obj.id,

        pagetype=seo_page_type,

        is_active=True

    ).first()

    # =====================================================
    # LOGIN USER
    # =====================================================

    user_id = request.session.get('user_id')

    logged_user = None

    if user_id:

        logged_user = User_Details.objects.filter(
            id=user_id
        ).first()

    # =====================================================
    # USER SUBSCRIPTION
    # =====================================================

    

    # =====================================================
    # CONTACT ACCESS
    # =====================================================

    can_view_contact = False


    # =====================================================
    # MASK PHONE NUMBER
    # =====================================================

    masked_phone = "XXXXXXXXXX"

    if p.get('phone'):

        phone = str(p['phone'])

        if len(phone) >= 10:

            masked_phone = (
                phone[:2]
                + "XXXXXX"
                + phone[-2:]
            )

    # =====================================================
    # SIMILAR PROPERTIES
    # =====================================================

    similar = []

    # =====================================================
    # CONTEXT
    # =====================================================

    context = {

        # PROPERTY
        "p": p,
        "original": obj,

        # URL
        "listing_type": listing_type,
        "category": category,

        # IMAGES
        "property_images": property_images,

        # FEATURES
        "amenities_list": amenities_list,
        "facilities_list": facilities_list,

        # SIMILAR
        "similar": similar,

        # SEO
        "seo": seo,

        # USER
        "logged_user": logged_user,


        # CONTACT
        "can_view_contact": can_view_contact,
        "masked_phone": masked_phone,

        # DATE
        "today": date.today(),
        "now": now(),
    }

    # 🔹 3. Handle the logged-in user logic safely
    session_id = request.session.get('User_id')
    if session_id:
        
        user_obj = User_Details.objects.filter(id=session_id).first()
        if user_obj:
            context['user_obj'] = user_obj

    return render(
        request,
        'home_page/property_detail.html',
        context
    )


########### Views start for ajax for send property enquiry ########################

@csrf_exempt
def Send_Property_Enquiry(request):
    data = request.POST.dict()   
    
    real_property = None

    property_id = data['property_id']

    if data['listing_type'] == "rent" and data['category'] == "residential":
        real_property = RentalResidentialProperty.objects.get(id=property_id)

    elif data['listing_type'] == "rent" and data['category'] == "pg":
        real_property = PGColivingProperty.objects.get(id=property_id)

    elif data['listing_type'] == "rent" and data['category'] == "commercial":
            real_property = CommercialProperty.objects.get(id=property_id)

    # If we couldn't find a matching property type, stop here.
    if not real_property:
        return JsonResponse({"status": "0", "msg": "Invalid property type or category."})

    user_data = User_Details.objects.get(id=data['user_id'])
    PropertyEnquiry.objects.create(property_object=real_property,user=user_data,enquiry_name=data['enquiry_name'],enquiry_phone=data['enquiry_phone'],enquiry_email=data['enquiry_email'],enquiry_message=data['enquiry_message'],enquiry_date=datetime.today(),enquiry_time=datetime.now())

    return JsonResponse({"status":"1", "msg" : f"Enquiry submiited successfully we will get back to you soon"})


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

    # 2. Price Logic
    price = "Price on Request"
    if hasattr(obj, 'monthly_rent') and obj.monthly_rent:
        price = f"₹{obj.monthly_rent}/mo"
    elif hasattr(obj, 'expected_price') and obj.expected_price:
        price = f"₹{obj.expected_price}"
    elif hasattr(obj, 'rent') and obj.rent:
        price = f"₹{obj.rent}/mo"

    # 3. Specification Logic
    beds = getattr(obj, 'bhk_type', None)
    area = getattr(obj, 'total_area', getattr(obj, 'plot_area', getattr(obj, 'built_up_area', None)))

    return {
        'id': obj.id,
        'category': source, 
        'listing_type': 'rent' if 'Data' in source or 'PG' in source else 'sale',
        'title': f"{beds if beds else source} in {getattr(obj, 'locality', 'this area')}",
        'location': f"{getattr(obj, 'locality', '')}, {getattr(obj, 'city', '')}",
        'price_display': price,
        'image_url': img_url,
        'beds': beds,
        'area': f"{area} sqft" if area else None,
        'owner': getattr(obj, 'owner_name', 'Owner'),
        'phone': getattr(obj, 'contact_number', ''),
        'is_ai_match': True,
    }



def listings_view(request):
    ai_query = request.GET.get('ai_query', '').strip()
    
    # Clean up the types list to avoid ['']
    raw_types = request.GET.get('types', '')
    selected_types = [t.strip() for t in raw_types.split(',')] if raw_types else []
    
    city_filter = request.GET.get('city_filter', '').strip()
    
    normalized_properties = []

    # Moved this outside the if-statement so both AI and standard search can use it
    model_map = {
        "Residential Data": RentalResidentialProperty,
        "Commercial Data": CommercialRentalProperty,
        "PG Data": PGColivingProperty,
        "Resale Residential": ResaleResidentialProperty,
        "Commercial Resale": CommercialResaleProperty,
        "Plot Resale": PlotSaleProperty,
        "Agricultural Data": AgriculturalResaleProperty,
        "Industrial Resale": IndustrialResaleProperty,
    }

    if ai_query:
        # ==========================================
        # 1. AI VECTOR SEARCH (When user types a query)
        # ==========================================
        df = MainAppConfig.get_ai_df()
        model = MainAppConfig.get_ai_model()
        faiss_index = MainAppConfig.get_ai_faiss()

        query_vector = model.encode([ai_query]).astype('float32')
        _, indices = faiss_index.search(query_vector, k=100) 
        results_df = df.iloc[indices[0]].copy()

        # Strict Category Filtering
        if selected_types:
            results_df = results_df[results_df['source_sheet'].isin(selected_types)]

        for _, row in results_df.iterrows():
            if len(normalized_properties) >= 20: break 
            
            db_model = model_map.get(row.get('source_sheet'))
            if db_model:
                obj_query = db_model.objects.filter(id=row.get('db_id'))
                if city_filter:
                    obj_query = obj_query.filter(city__icontains=city_filter)
                
                real_obj = obj_query.first()
                if real_obj:
                    normalized_properties.append(_normalize_any_property(real_obj, row.get('source_sheet')))

    else:
        # ==========================================
        # 2. STANDARD DATABASE SEARCH (Default Browsing)
        # ==========================================
        # If user selected specific types, only search those. Otherwise, search all.
        models_to_search = [(k, v) for k, v in model_map.items() if k in selected_types] if selected_types else model_map.items()

        for sheet_name, db_model in models_to_search:
            if len(normalized_properties) >= 20: break
            
            # Get properties, optionally order by newest if you have a created_at field
            # e.g., db_model.objects.all().order_by('-id')
            obj_query = db_model.objects.all() 
            
            # Apply the Strict City Filter
            if city_filter:
                obj_query = obj_query.filter(city__icontains=city_filter)
            
            # Fetch a small chunk from this model to mix results, up to remaining capacity
            remaining_spots = 20 - len(normalized_properties)
            for real_obj in obj_query[:remaining_spots]:
                normalized_properties.append(_normalize_any_property(real_obj, sheet_name))


    # Send all variables to the template
    context = {
        'properties': normalized_properties,
        'total': len(normalized_properties),
        'category': selected_types[0] if selected_types else "All",
        'current_city': city_filter if city_filter else "Nagpur",
        'listing_type': 'rent' if any(x in ai_query.lower() for x in ['rent', 'pg']) else 'sale'
    }

    session_id = request.session.get('User_id')
    if session_id:
        user_obj = User_Details.objects.filter(id=session_id).first()
        if user_obj:
            context['user_obj'] = user_obj

            # 1. Initialize a structured dictionary of sets for fast lookup
            wishlist_records = {
                'residential': set(),
                'pg': set(),
                'commercial': set()
            }

            # 2. Fetch the items along with their ContentType details
            wishlist_items = WishlistProperty.objects.filter(user=user_obj).select_related('content_type')
        
            # 3. Sort the object_ids into their matching categories
            for item in wishlist_items:
                model_name = item.content_type.model  # e.g., 'rentalresidentialproperty'
                
                if 'residential' in model_name:
                    wishlist_records['residential'].add(item.object_id)
                elif 'pg' in model_name:
                    wishlist_records['pg'].add(item.object_id)
                elif 'commercial' in model_name:
                    wishlist_records['commercial'].add(item.object_id)

            # 4. Save the structured records into the context instead of the flat list
            context['wishlist_records'] = wishlist_records



    return render(request, 'home_page/listingpage.html', context)



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








def index(request):
    today = datetime.now().date()
    fifteen_days_ago = today - timedelta(days=15)
    
    # ═══════════════════════════════════════════════════════
    # FETCH RENTAL PROPERTIES
    # ═══════════════════════════════════════════════════════
    rental_residential = RentalResidentialProperty.objects.prefetch_related('images').all().order_by('-id')[:10]
    rental_commercial = CommercialRentalProperty.objects.prefetch_related('images').all().order_by('-id')[:10]
    rental_pg = PGColivingProperty.objects.prefetch_related('images').all().order_by('-id')[:10]

    resale_residential = ResaleResidentialProperty.objects.prefetch_related('images').all().order_by('-id')[:10]
    resale_commercial = CommercialResaleProperty.objects.prefetch_related('images').filter(is_active=True).order_by('-id')[:10]
    resale_plot = PlotSaleProperty.objects.prefetch_related('images').all().order_by('-id')[:10]
    resale_industrial = IndustrialResaleProperty.objects.prefetch_related('images').all().order_by('-id')[:10]
    resale_agricultural = AgriculturalResaleProperty.objects.prefetch_related('images').all().order_by('-id')[:10]
    
    # ═══════════════════════════════════════════════════════
    # COMBINE RENTAL PROPERTIES
    # ═══════════════════════════════════════════════════════
    all_rental_props = list(chain(
        [{"data": p, "type": "rental_residential", "listing_type": "rent", "category": "Residential"} for p in rental_residential],
        [{"data": p, "type": "rental_commercial", "listing_type": "rent", "category": "Commercial"} for p in rental_commercial],
        [{"data": p, "type": "rental_pg", "listing_type": "rent", "category": "PG"} for p in rental_pg]
    ))
    
    # ═══════════════════════════════════════════════════════
    # COMBINE RESALE PROPERTIES
    # ═══════════════════════════════════════════════════════
    all_resale_props = list(chain(
        [{"data": p, "type": "resale_residential", "listing_type": "sale", "category": "Residential"} for p in resale_residential],
        [{"data": p, "type": "resale_commercial", "listing_type": "sale", "category": "Commercial"} for p in resale_commercial],
        [{"data": p, "type": "resale_plot", "listing_type": "sale", "category": "Plots/Land"} for p in resale_plot],
        [{"data": p, "type": "resale_industrial", "listing_type": "sale", "category": "Industrial"} for p in resale_industrial],
        [{"data": p, "type": "resale_agricultural", "listing_type": "sale", "category": "Agricultural"} for p in resale_agricultural]
    ))
    
    # ═══════════════════════════════════════════════════════
    # GET FEATURED PROPERTIES (RENT + SALE)
    # ═══════════════════════════════════════════════════════
    all_props = all_rental_props + all_resale_props
    featured_props = [p for p in all_props if hasattr(p["data"], 'is_featured') and p["data"].is_featured]
    random.shuffle(featured_props)
    featured_props = featured_props[:6]
    
    # ═══════════════════════════════════════════════════════
    # GET RECENT PROPERTIES (LAST 30 DAYS)
    # ═══════════════════════════════════════════════════════
    recent_props = sorted(all_props, key=lambda x: x["data"].id, reverse=True)[:8]
    
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

    ########### Normal FAQ Table call ###########################

    faqs_obj = NormalFAQ.objects.all().order_by('-id')

    context = {
        "featured_props": featured_props,
        "recent_props": recent_props,
        "all_rental_props": all_rental_props[:6],
        "all_resale_props": all_resale_props[:6],
        "hero": hero,
        "seo_pages":seo_pages,
        "today": today,
        "fifteen_days_ago": fifteen_days_ago,
        'user_obj': None,
        'services': services,
        'subscriptions':subscriptions,
        'faqs_obj':faqs_obj
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

    context = {
        'services':services
    }

    session_id = request.session.get('User_id')
    if session_id:
        user_obj = User_Details.objects.filter(id=session_id).first()
        if user_obj:
            context['user_obj'] = user_obj

    return render(request, "home_page/services.html",context)



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

    session_id = request.session.get('User_id')
    if session_id:
        user_obj = User_Details.objects.filter(id=session_id).first()
        if user_obj:
            context['user_obj'] = user_obj

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

    context = {
        'faq_sections':faq_sections
    }

    session_id = request.session.get('User_id')
    if session_id:
        user_obj = User_Details.objects.filter(id=session_id).first()
        if user_obj:
            context['user_obj'] = user_obj

    return render(request, "home_page/property_faq.html",context)