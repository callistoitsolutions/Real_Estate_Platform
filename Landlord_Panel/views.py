from django.shortcuts import render,HttpResponse

# Create your views here.
from django.shortcuts import render
from django.contrib.auth.decorators import login_required



# Create your views here.
from django.shortcuts import render
from django.contrib import messages
from django.shortcuts import render,redirect
from Landlord_Panel .models import *
from Main_App .models import *
from Admin_App.models import *

# Create your views here.


############## Views start for calculate profile strength ##########################

def calculate_profile_strength(user_obj):
    """Calculates the profile completion percentage dynamically based on the user's role."""
    strength = 0
    
    # ---------------------------------------------------------
    # 1. BASE DETAILS (Applies to everyone - Total 50%)
    # ---------------------------------------------------------
    if user_obj.user_name: strength += 10
    if user_obj.user_email: strength += 10
    if user_obj.user_phone: strength += 10
    if user_obj.user_password: strength += 10
    if user_obj.user_role: strength += 10
    
    # ---------------------------------------------------------
    # 2. ROLE-SPECIFIC DETAILS (Remaining 50%)
    # ---------------------------------------------------------
    role = user_obj.user_role

    if role == 'Vendor':
        # Vendor requires 5 specific things (10% each)
        if getattr(user_obj, 'user_state', None): strength += 10
        if getattr(user_obj, 'user_city', None): strength += 10
        if getattr(user_obj, 'user_address', None): strength += 10
        if getattr(user_obj, 'user_profile', None) and user_obj.user_profile.name: strength += 10
        if getattr(user_obj, 'user_service_type', None): strength += 10 # <-- Change to your actual DB field
        if getattr(user_obj, 'user_company_name', None): strength += 10 # <-- Change to your actual DB field
        if getattr(user_obj, 'user_profile', None) and user_obj.user_profile.name: strength += 10
        
    elif role in ['Agent', 'Agency/Builder']:
        # Agents/Agencies require different fields (10% each)
        if getattr(user_obj, 'user_state', None): strength += 10
        if getattr(user_obj, 'user_city', None): strength += 10
        if getattr(user_obj, 'user_address', None): strength += 10
        if getattr(user_obj, 'user_license_number', None): strength += 10 # <-- Change to your actual DB field
        if getattr(user_obj, 'user_profile', None) and user_obj.user_profile.name: strength += 10
        
    else:
        # Default for Landlord, Tenant, and Buyer
        if getattr(user_obj, 'user_state', None): strength += 15
        if getattr(user_obj, 'user_city', None): strength += 15
        if getattr(user_obj, 'user_address', None): strength += 10
        if getattr(user_obj, 'user_profile', None) and user_obj.user_profile.name: strength += 10

    # Ensure it never accidentally goes over 100
    return min(strength, 100)

############# Views end for calculate profile strength ##########################



########### Crime Officer Views#######


def landlord_dashboard(request):
    # 1. Retrieve identity from browser session
    user_id = request.session.get('User_id')
    user_role = request.session.get('user_type')

    # 2. Access Control: If ID is missing OR role is wrong, redirect to login
    if not user_id or user_role != "Landlord":
        return redirect('login') 

    # 3. Data Fetching: Get the full user object for the template
    user_obj = User_Details.objects.get(id=user_id)

    completion_score = calculate_profile_strength(user_obj)
    
    context = {
        'user_obj': user_obj,
        'user_role': user_role,
        'profile_completion_percentage': completion_score,
    }
    
    return render(request, "landlord/landlord_dashboard.html", context) 

def commercialform(request):
    return render(request,"landlord/commercialform.html") 



def residential_landlord(request):
    return render(request,"landlord/residential_landlord.html")

def commercial_landlord(request):
    return render(request,"landlord/commercial_landlord.html")

def pg_coliving_landlord(request):
    return render(request,"landlord/pg_coliving_landlord.html")

def delete_confirmation(request):
    return render(request,"landlord/delete_confirmation.html")

def Subscription_Upgrade_Form(request):
    return render(request,"landlord/Subscription_Upgrade_Form.html")

def data_landlord(request):
    return render(request,"landlord/data_landlord.html")

def residential_landlord_edit(request):
    return render(request,"landlord/residential_landlord_edit.html")



def Subscription_Purchase_tenant(request):
    return render(request,"tenant_user/Subscription_Purchase_tenant.html")


def Property_Review_tenant(request):
    return render(request,"tenant_user/Property_Review_tenant.html")


def property_bookmark(request):
    return render(request,"tenant_user/property_bookmark.html")

def chat_tenant(request):
    return render(request,"tenant_user/chat_tenant.html")


def boostlisting(request):
    return render(request,"landlord/boostlisting.html") 


############## Views start for update landlord profile page ######################

def Update_Profile_Landlord(request):
    # 1. Retrieve identity from browser session
    user_id = request.session.get('User_id')
    user_role = request.session.get('user_type')

    # 2. Access Control: If ID is missing OR role is wrong, redirect to login
    if not user_id or user_role != "Landlord":
        return redirect('login') 

    # 3. Data Fetching: Get the full user object for the template
    user_obj = User_Details.objects.get(id=user_id)
    
    context = {
        'user_obj': user_obj,
        'user_role': user_role
    }
    
    return render(request, "landlord/Profile/landlord_profile.html", context) 

########### Views end for update landlord profile page ##########################


def property_list(request):
    properties = ResidentialProperty.objects.all()
    return render(request, 'landlord/property_list.html', {'properties': properties})







from django.shortcuts import render, redirect
from .models import Property,CommercialProperty,PG_Property, BoostListing
from django.shortcuts import render, redirect, get_object_or_404



def property_list(request):
    properties = Property.objects.all()  # Fetch all properties
    return render(request, 'landlord/property_list.html', {'properties': properties})



def property_create(request):
    data = request.POST
    if request.method == 'POST':
        recommended_for = request.POST.getlist('recommended_for[]')
        video_platforms = request.POST.getlist('video_platforms[]')
        nearby_facilities = request.POST.getlist('nearby_facilities[]')
        amenities = request.POST.getlist('amenities[]')

        # Helper function to safely get numeric fields
        def get_number(field_name):
            value = request.POST.get(field_name)
            return int(value) if value and value.isdigit() else None

        # Helper function to safely get float fields
        def get_float(field_name):
            value = request.POST.get(field_name)
            try:
                return float(value) if value else None
            except ValueError:
                return None

        property = Property(
            property_title=request.POST.get('property_title'),
            city=request.POST.get('city'),
            area=request.POST.get('area'),
            property_address=request.POST.get('property_address'),
            property_type=request.POST.get('property_type'),
            builtup_area=get_number('builtup_area'),
            carpet_area=get_number('carpet_area'),
            zone=request.POST.get('zone'),
            society_type=request.POST.get('society_type'),
            recommended_for=",".join(recommended_for) if recommended_for else '',
            bedrooms=get_number('bedrooms'),
            bathrooms=get_number('bathrooms'),
            balconies=get_number('balconies'),
            furnishing=request.POST.get('furnishing'),
            floor_no=get_number('floor_no'),
            total_floors=get_number('total_floors'),
            age_of_property=get_number('age_of_property'),
            water_type=request.POST.get('water_type'),
            rent_price=get_float('rent_price'),
            security_deposit=get_float('security_deposit'),
            maintenance=get_float('maintenance') or 0,

            is_featured=request.POST.get('is_featured'),
            featured_days=get_number('featured_days'),
            manual_featured_days=get_number('manual_featured_days'),
            featured_start_date=request.POST.get('featured_start_date'),
            featured_end_date=request.POST.get('featured_end_date'),
            service_amount=get_float('service_amount'),
            placement=request.POST.get('placement'),
            is_verified=request.POST.get('is_verified'),

            property_images=request.FILES.get('property_images'),
            floor_plan=request.FILES.get('floor_plan'),
            upload_registry=request.FILES.get('upload_registry'),
            upload_house_tax=request.FILES.get('upload_house_tax'),
            upload_utility_bill=request.FILES.get('upload_utility_bill'),
            upload_aadhar=request.FILES.get('upload_aadhar'),
            upload_pan=request.FILES.get('upload_pan'),
            upload_index2=request.FILES.get('upload_index2'),

            brokerage_applicable=request.POST.get('brokerage_applicable'),
            brokerage_payer=request.POST.get('brokeragePayer'),
            brokerage_type=request.POST.get('brokerage_type'),
            brokerage_value=get_float('brokerageValue'),
            percentage_extra=get_float('percentageExtra'),
            brokerage_description=request.POST.get('brokerageDescription'),

            exclusive_property=True if request.POST.get('exclusive_property') == 'on' else False,
            upload_video=True if request.POST.get('upload_video') == 'on' else False,
            video_url=request.POST.get('video_url'),
            video_from=data.get("video_from") or None,
            video_to=data.get("video_to") or None,
            video_platforms=",".join(video_platforms) if video_platforms else '',

            nearby_facilities=",".join(nearby_facilities) if nearby_facilities else '',
            amenities=",".join(amenities) if amenities else ''
        )

        property.save()
        return redirect('property_list')

    return render(request, 'landlord/property_form.html')




def property_edit(request, pk):
    property = get_object_or_404(Property, pk=pk)
    if request.method == 'POST':
        # Similar to property_create: update all fields
        # property.field = request.POST.get(...)
        # property.save()
        return redirect('property_list')
    return render(request, 'landlord/property_form.html', {'property': property})


def property_delete(request, pk):
    property = get_object_or_404(Property, pk=pk)
    property.delete()
    return redirect('property_list')






import datetime

def commercial_property_add(request):
    if request.method == "POST":
        data = request.POST
        files = request.FILES

        def get_int(field, default=0):
            try:
                return int(data.get(field, default)) if data.get(field) else default
            except ValueError:
                return default

        def get_float(field, default=0.0):
            try:
                return float(data.get(field, default)) if data.get(field) else default
            except ValueError:
                return default

        # Date conversion
        def get_date(field):
            val = data.get(field)
            if val:
                try:
                    return datetime.datetime.strptime(val, "%Y-%m-%d").date()
                except:
                    return None
            return None

        property = CommercialProperty.objects.create(
            property_type=data.get("property_type"),
            city=data.get("city"),
            area_locality=data.get("area_locality"),
            property_address=data.get("property_address"),
            building_name=data.get("building_name"),
            possession_status=data.get("possession_status"),
            age_of_property=get_int("age_of_property"),
            zone_type=data.get("zone_type"),
            location_hub=data.get("location_hub"),
            property_condition=data.get("property_condition"),
            ownership_type=data.get("ownership_type"),
            construction_status=data.get("construction_status"),

            builtup_area=get_int("builtup_area"),
            carpet_area=get_int("carpet_area"),
            total_floors=get_int("total_floors"),
            your_no=get_int("your_no"),
            no_of_staircase=get_int("no_of_staircase"),
            passenger_lifts=get_int("passenger_lifts"),
            service_lifts=get_int("service_lifts"),
            private_parking=get_int("private_parking"),
            public_parking=get_int("public_parking"),
            minimum_seats = get_int("minimum_seats"),
            maximum_seats = get_int("maximum_seats"),
            number_of_cabin = get_int("number_of_cabin"),
            meeting_room = get_int("meeting_room"),
            floring_type = data.get("floring_type"), 

            expected_rent=get_float("expected_rent"),
            security_deposit=get_float("security_deposit"),
            maintenance_charges=get_float("maintenance_charges"),
            rent_available_from=get_date("available_from"),
            lock_in_period=get_int("lock_in_period"),
            rent_increase=get_float("rent_increase"),

            property_images=files.get("property_images"),
            floor_plan=files.get("floor_plan"),

            is_featured=True if data.get("is_featured") == "Yes" else False,
            featured_days=get_int("featured_days", None),
            manual_featured_days=get_int("manual_featured_days", None),
            featured_start_date=get_date("featured_start_date"),
            featured_end_date=get_date("featured_end_date"),
            service_amount=get_float("service_amount"),
            placement=data.get("placement"),
            is_verified=True if data.get("is_verified") == "yes" else False,

            upload_registry=files.get("upload_registry"),
            upload_house_tax=files.get("upload_house_tax"),
            upload_utility_bill=files.get("upload_utility_bill"),
            upload_aadhar=files.get("upload_aadhar"),
            upload_pan=files.get("upload_pan"),
            upload_index2=files.get("upload_index2"),

            brokerage_applicable=data.get("brokerage_applicable", "No"),
            brokerage_payer=data.get("brokeragePayer"),
            brokerage_type=data.get("brokerageType"),
            brokerage_value=get_float("brokerageValue"),
            percentage_extra=get_float("percentageExtra"),
            brokerage_description=data.get("brokerageDescription"),

            exclusive_property=True if data.get("exclusive_property") == "on" else False,
            upload_video=True if data.get("upload_video") == "on" else False,
            video_url=data.get("video_url"),
            video_from=data.get("video_from") or None,
            video_to=data.get("video_to") or None,
            video_platforms=",".join(data.getlist("video_platforms[]")),

            nearby_facilities=",".join(data.getlist("nearby_facilities[]")),
            amenities=",".join(data.getlist("amenities[]")),
        )

        return redirect("commercial_property_add")  # or change to list page

    return render(request, "landlord/commercial_property_form.html")




 

    # --- Rent Details ---


def commercial_property_list(request):
    properties = CommercialProperty.objects.all().order_by("-id")
    return render(request, "landlord/commercial_property_list.html", {"properties": properties})





def add_pg_property(request):
    if request.method == "POST":
        data = request.POST
        files = request.FILES

        prop = PG_Property(
            property_type=data.get("property_type"),
            city=data.get("city"),
            area_locality=data.get("area_locality"),
            address=data.get("address"),
            furnishing_type=data.get("Furnished"),
            sharing_type=data.get("sharing"),
            meals_included=True if data.get("custom_options[]") else False,
            meal_type=data.get("meal_type"),
            minimum_stay=data.get("minimum_stay") or 0,
            available_from=data.get("available_from"),
            rent_price=data.get("rent_price") or 0,
            security_deposit=data.get("security_deposit") or 0,
            property_images=files.get("property_images"),
            floor_plan=files.get("floor_plan"),
            is_featured=data.get("is_featured", "No"),
            featured_days=data.get("featured_days") or None,
            manual_featured_days=data.get("manual_featured_days") or None,
            featured_start_date=data.get("featured_start_date") or None,
            featured_end_date=data.get("featured_end_date") or None,
            service_amount=data.get("service_amount") or None,
            placement=data.get("placement"),
            is_verified=data.get("is_verified", "no"),
            upload_registry=files.get("upload_registry"),
            upload_house_tax=files.get("upload_house_tax"),
            upload_utility_bill=files.get("upload_utility_bill"),
            upload_aadhar=files.get("upload_aadhar"),
            upload_pan=files.get("upload_pan"),
            upload_index2=files.get("upload_index2"),
            brokerage_applicable=data.get("brokerage_applicable"),
            brokeragePayer=data.get("brokeragePayer"),
            brokerageType=data.get("brokerageType"),
            brokerageValue=data.get("brokerageValue") or None,
            percentageExtra=data.get("percentageExtra") or None,
            brokerageDescription=data.get("brokerageDescription"),
            exclusive_property=True if data.get("exclusive_property") else False,
            upload_video=True if data.get("upload_video") else False,
            video_url=data.get("video_url"),
            video_from=data.get("video_from") or None,
            video_to=data.get("video_to") or None,
            video_platforms=",".join(data.getlist("video_platforms[]")),
            nearby_facilities=",".join(data.getlist("nearby_facilities[]")),
            amenities=",".join(data.getlist("amenities[]")),
        )
        prop.save()
        #return redirect("property_list")

    return render(request, "landlord/pg_form.html")



def pg_property_list(request):
    properties = PG_Property.objects.all()
    return render(request, "landlord/pg_property_list.html", {"properties": properties})



def boost_listing_create(request):
    # listings is assumed to be a queryset of landlord's property objects
    listings = []  # Replace with ORM query to fetch user's properties
    if request.method == 'POST':
        BoostListing.objects.create(
            boost_type=request.POST.get('boost_type'),
            boost_duration=request.POST.get('boost_duration'),
            listing_id=request.POST.get('listing_id'),
            payment_method=request.POST.get('payment_method'),
            agree_terms='agree_terms' in request.POST
        )
        return redirect('boost_listing_list')
    return render(request, 'landlord/boost_listing_form.html', {'listings': listings})


def boost_listing_list(request):
    boostings = BoostListing.objects.all()
    return render(request, 'landlord/boost_listing_list.html', {'boostings': boostings})


def enquiry_create(request):
    if request.method == 'POST':
        Enquiry.objects.create(
            name=request.POST.get('name'),
            email=request.POST.get('email'),
            phone=request.POST.get('phone'),
            message=request.POST.get('message'),
        )
        return redirect('enquiry_list')
    return render(request, 'landlord/enquiry_form.html')


def enquiry_list(request):
    enquiries = Enquiry.objects.all()
    return render(request, 'landlord/enquiry_list.html', {'enquiries': enquiries})


from django.http import HttpResponseForbidden



from django.contrib.auth.decorators import login_required

from Main_App.models import (
    ResidentialProperty,
    CommercialProperty,
    PGProperty,
    ResidentialInquiry,
    CommercialInquiry,
    PGInquiry
)

@login_required
def property_inquiry(request):
    user = request.user
    role = getattr(user, "role", "").lower()

    # Only landlords can access this page
    if role != "landlord":
        return HttpResponseForbidden("You do not have permission to view this page.")

    # Helper function to safely get a field if it exists
    def safe_getattr(obj, attr, default=None):
        return getattr(obj, attr, default) if hasattr(obj, attr) else default

    # Get all properties posted by the landlord
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
            prop = safe_getattr(inquiry, fk_field)
            landlord = safe_getattr(prop, 'posted_by')
            data.append({
                "inquiry_name": safe_getattr(inquiry, 'name', 'N/A'),
                "inquiry_email": safe_getattr(inquiry, 'email', 'N/A'),
                "inquiry_phone": safe_getattr(inquiry, 'phone', 'N/A'),
                "inquiry_message": safe_getattr(inquiry, 'message', 'N/A'),
                "property_title": safe_getattr(prop, 'property_title', 'N/A'),
                "property_type": prop.__class__.__name__ if prop else 'N/A',
                "property_location": safe_getattr(prop, 'location', 'N/A'),
                "property_price": safe_getattr(prop, 'price', 'N/A'),
                "property_landlord_name": safe_getattr(landlord, 'full_name', safe_getattr(landlord, 'username', 'N/A')),
                "property_landlord_role": safe_getattr(landlord, 'role', 'N/A'),
                "lead_age": safe_getattr(inquiry, 'lead_age', 'N/A'),
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

    template = "landlord/property_inquiry.html"
    return render(request, template, data)




@login_required
def residential_property_detail(request, pk):
    prop = get_object_or_404(ResidentialProperty, id=pk)
    return render(request, "landlord/residential_property_detail.html", {"property": prop})
# Residential Inquiries

@login_required
def residential_inquiries_view(request):
    user = request.user
    if getattr(user, "role", "").lower() != "landlord":
        return HttpResponseForbidden("Access denied.")

    inquiries = ResidentialInquiry.objects.filter(residential_property__posted_by=user).select_related('residential_property')
    context = {"inquiries": inquiries, "user_full_name": getattr(user, "full_name", user.username)}
    return render(request, "landlord/residential_inquiries.html", context)


# Commercial Inquiries
@login_required
def commercial_inquiries_view(request):
    user = request.user
    if getattr(user, "role", "").lower() != "landlord":
        return HttpResponseForbidden("Access denied.")

    inquiries = CommercialInquiry.objects.filter(commercial_property__posted_by=user).select_related('commercial_property')
    context = {"inquiries": inquiries, "user_full_name": getattr(user, "full_name", user.username)}
    return render(request, "landlord/commercial_inquiries.html", context)


# PG / Co-living Inquiries
@login_required
def pg_inquiries_view(request):
    user = request.user
    if getattr(user, "role", "").lower() != "landlord":
        return HttpResponseForbidden("Access denied.")

    inquiries = PGInquiry.objects.filter(pg_property__posted_by=user).select_related('pg_property')
    context = {"inquiries": inquiries, "user_full_name": getattr(user, "full_name", user.username)}
    return render(request, "landlord/pg_inquiries.html", context)




# Common helper to fetch properties based on role
def get_role_based_properties(user, model):
    role = getattr(user, "role", "").lower()
    if role == "agent":
        return model.objects.filter(posted_by=user)
  
    elif role == "landlord":
        return model.objects.filter(posted_by=user)

    else:
        return model.objects.none()

# --- Residential Property List ---



@login_required
def residential_property_list(request):
    user = request.user

    # ✅ Check if the user is a landlord
    if getattr(user, "role", "").lower() != "landlord":
        messages.warning(request, "Access denied. Only landlords can view this page.")
        return redirect("index")  # or another appropriate URL

    properties = get_role_based_properties(user, ResidentialProperty)

    context = {
        "properties": properties,
        "role": user.role,
        "user_full_name": getattr(user, "full_name", user.username),
    }

    return render(request, "landlord/residential_list.html", context)



# --- Commercial Property List ---







# --- PG Property List ---


@login_required
def pg_property_list(request):
    user = request.user

    # ✅ Allow only landlords
    if getattr(user, "role", "").lower() != "landlord":
        messages.warning(request, "Access denied. Only landlords can view this page.")
        return redirect("index")  # change "home" to your preferred page

    # ✅ Fetch PG properties for landlord
    properties = get_role_based_properties(user, PGProperty)

    context = {
        "properties": properties,
        "role": user.role,
        "user_full_name": getattr(user, "full_name", user.username),
    }
    return render(request, "landlord/pg_list.html", context)









