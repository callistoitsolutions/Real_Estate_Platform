from django.shortcuts import render,HttpResponse

# Create your views here.
from django.shortcuts import render
from django.contrib import messages
from django.shortcuts import render,redirect,get_object_or_404
from Admin_App .models import *
from Main_App .models import *
from seo .models import *
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from datetime import datetime
from openpyxl import load_workbook
from django.template.loader import render_to_string
import traceback
import json
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.db.models import Q
from django.core.paginator import Paginator  # ← ADD THIS
import csv

# Create your views here.

########### Crime Officer Views#######


def profile_update(request):
    return render(request,"admin_user/profile_update.html") 

def chat(request):
    return render(request,"admin_user/chat.html") 

def admin_approval_form(request):
    return render(request,"admin_user/admin_approval_form.html") 

def referral_closing(request):
    return render(request,"admin_user/referral_closing.html") 

def rm_register(request):
    return render(request,"admin_user/rm_register.html") 


def Property_Review(request):
    return render(request,"admin_user/Property_Review.html")  

def Lead_Status_Update(request):
    return render(request,"admin_user/Lead_Status_Update.html")  

def Lead_Assignment(request):
    return render(request,"admin_user/Lead_Assignment.html")

def Wallet_Top_up(request):
    return render(request,"admin_user/Wallet_Top_up.html")

def GST_Invoice(request):
    return render(request,"admin_user/GST_Invoice.html")

def Subscription_Purchase(request):
    return render(request,"admin_user/Subscription_Purchase.html")

def other(request):
    return render(request,"admin_user/other.html")

def inquiry(request):
    return render(request,"admin_user/inquiry.html")

def commision_hold_table(request):
    return render(request,"admin_user/commision_hold_table.html")


def Commission_Hold_Release(request):
    return render(request,"admin_user/Commission_Hold_Release.html")

def dynamic_page_report(request):
    return render(request,"admin_user/dynamic_page_report.html")


def dynamic_page_edit(request):
    
    if request.method == 'POST':
        title = request.POST.get('title')
        seo_meta = request.POST.get('seo_meta')
        body = request.POST.get('body')
        image = request.FILES.get('image')
        DynamicPage.objects.create(
            title=title,
            seo_meta=seo_meta,
            body=body,
            image=image
        )
      #  return redirect('dynamicpage_list')
    #return render(request, 'dynamicpage_form.html')

    return render(request,"admin_user/dynamic_page_edit.html")


#def blog_list(request):
   # return render(request,"admin_user/blog_list.html")





def comission_structure_setup(request):
    if request.method == "POST":
        role = request.POST.get("role")
        rate_type = request.POST.get("rateType")
        commission_value = request.POST.get("commissionValue")
        deduction = request.POST.get("deduction")
        from_date = request.POST.get("fromDate")
        to_date = request.POST.get("toDate")
        release_option = request.POST.get("releaseOption")
        custom_release_date = request.POST.get("customReleaseDate")

        CommissionStructure.objects.create(
            role=role,
            rate_type=rate_type,
            commission_value=commission_value,
            deduction=deduction or None,
            from_date=from_date,
            to_date=to_date,
            release_option=release_option,
            custom_release_date=custom_release_date or None,
        )

        return redirect("comission_structure_setup")  # reload page after save

    commission_list = CommissionStructure.objects.all().order_by("-created_at")
    return render(request, "admin_user/comission_structure_setup.html", {"commission_list": commission_list})



def seo_meta_tag(request):
    if request.method == "POST":
        page_name = request.POST.get("page_name")
        meta_title = request.POST.get("meta_title")
        canonical_url = request.POST.get("canonical_url")
        meta_description = request.POST.get("meta_description")
        keywords = request.POST.get("keywords")

        # Save in DB
        SeoMetaTag.objects.create(
            page_name=page_name,
            meta_title=meta_title,
            canonical_url=canonical_url,
            meta_description=meta_description,
            keywords=keywords,
        )
        messages.success(request, "SEO Meta Tag added successfully!")
        #return redirect("seo_meta_tag_list")

    # Display saved data
    seo_tags = SeoMetaTag.objects.all()
    return render(request, "admin_user/seo_meta_tag.html", {"seo_tags": seo_tags})


def seo_meta_tag_list(request):
   # seo_tags = SEOMetaTag.objects.all().order_by("-created_at")
    return render(request, "admin_user/seo_meta_tag_list.html")


def admin_page(request):
    session_id = request.session.get('Admin_id')
    if session_id:
        admin_obj = Admin_Login.objects.get(id=session_id)
        context = {'admin_obj':admin_obj}
        return render(request,"admin_user/admin_page.html",context)
    else:
        return render(request,'home_page/Adminlogin.html')
    

def index2(request):
    return render(request,"admin_user/index2.html")

def index3(request):
    return render(request,"admin_user/index3.html")


def data(request):
    return render(request,"admin_user/data.html")

def commercial_table(request):
    return render(request,"admin_user/commercial_table.html")

def pg_co_table(request):
    return render(request,"admin_user/pg_co_table.html")

def residential(request):
    session_id = request.session.get('Admin_id')
    if session_id:
        admin_obj = Admin_Login.objects.get(id=session_id)

        ameneties_obj = Ameneties_Details.objects.all()
        facilities_obj = Facilities_Details.objects.all()

        context = {'admin_obj':admin_obj,'ameneties_obj':ameneties_obj,'facilities_obj':facilities_obj}
        return render(request,"admin_user/residential.html",context)
    else:
        return render(request,'home_page/Adminlogin.html')


def commercial(request):
    session_id = request.session.get('Admin_id')
    if session_id:
        admin_obj = Admin_Login.objects.get(id=session_id)

        ameneties_obj = Ameneties_Details.objects.all()
        facilities_obj = Facilities_Details.objects.all()

        context = {'admin_obj':admin_obj,'ameneties_obj':ameneties_obj,'facilities_obj':facilities_obj}
        return render(request,"admin_user/commercial.html",context)
    else:
        return render(request,'home_page/Adminlogin.html')


def pg_coliving(request):
    session_id = request.session.get('Admin_id')
    if session_id:
        admin_obj = Admin_Login.objects.get(id=session_id)

        ameneties_obj = Ameneties_Details.objects.all()
        facilities_obj = Facilities_Details.objects.all()

        context = {'admin_obj':admin_obj,'ameneties_obj':ameneties_obj,'facilities_obj':facilities_obj}
        return render(request,"admin_user/pg_coliving.html",context)
    else:
        return render(request,'home_page/Adminlogin.html')
    

############## Views start for ameneties list ##########################

def Ameneties_List(request):
    session_id = request.session.get('Admin_id')
    if session_id:
        admin_obj = Admin_Login.objects.get(id=session_id)

        ameneties_obj = Ameneties_Details.objects.all().order_by('-id')
        ameneties_obj_count = Ameneties_Details.objects.all().count()

        rendered = render_to_string("admin_user/render_to_string/R_Ameneties/r_t_s_ameneties.html",{'ameneties_obj':ameneties_obj,'ameneties_obj_count':ameneties_obj_count})

        context = {'admin_obj':admin_obj,'ameneties_list':rendered}
        return render(request,"admin_user/Ameneties/ameneties_list.html",context)
    else:
        return render(request,'home_page/Adminlogin.html')

########### Views end for ameneties list ################################


########### Views start for ajax for add/update ameneties #####################

@csrf_exempt
def Ameneties_Ajax(request):
    data = request.POST.dict()

    if data.get('id') == "":
        data.pop("id", None)         
        data['amenties_date'] = datetime.today()
        data['amenties_time'] = datetime.now()
        Ameneties_Details.objects.create(**data)
        return JsonResponse({"status":"1", "msg" : f"Ameneties Details added successfully"})

    # UPDATE MODE
    else:
        try:
            ameneties = Ameneties_Details.objects.get(id=data['id'])
        except Ameneties_Details.DoesNotExist:
            return JsonResponse({'status': '0', 'msg': 'Ameneties Details not found'})


        # Update withdraw fields (unchanged)
        for key, value in data.items():
            setattr(ameneties, key, value)

        ameneties.save()
        return JsonResponse({"status":"1", "msg" : f"Ameneties Details updated successfully"})

############ Views end for ajax for add/update ameneties #########################


############# Views start for upload ameneties data via excel ##################

@csrf_exempt
def Ameneties_Data(request):

    if request.method == 'POST':

        excel_file = request.FILES.get('ameneties_file')

        wb = load_workbook(excel_file)
        sheet = wb.active

        for row in sheet.iter_rows(min_row=2, values_only=True):

            amenties_icon = row[0]
            amenties_name = row[1]

            if not amenties_icon or not amenties_name:
                continue

            Ameneties_Details.objects.update_or_create(
                amenties_name=amenties_name,  # condition to check existing
                defaults={
                    "amenties_icon": amenties_icon,
                    "amenties_date": datetime.today(),
                    "amenties_time": datetime.now()
                }
            )

        return JsonResponse({
            "status": "1",
            "msg": "Data Uploaded / Updated Successfully..."
        })

    return JsonResponse({
        "status": "0",
        "msg": "Something went wrong..."
    })

############## Views end for upload ameneties date via excel #######################


########### Views start for delete ameneties data #########################

@csrf_exempt
def Delete_Ameneties(request):
    try:
        try:
            ameneties_id = request.POST.get('ameneties_id')
            Ameneties_Details.objects.filter(id=ameneties_id).delete()
            return JsonResponse({'status':'1', 'msg':'Ameneties details deleted successfully...'}) 
        except:
            traceback.print_exc()
            return JsonResponse({"status":"0", "msg" : "Something went wrong..."})
    except:
        traceback.print_exc()
        return JsonResponse({"status":"0", "msg" : "Something went wrong..."})

############ Views end for delete ameneties data ############################


########## Views start for update ameneties data ####################

def Update_Ameneties(request,id):
    session_id = request.session.get('Admin_id')
    if session_id:
        admin_obj = Admin_Login.objects.get(id=session_id)

        ameneties = Ameneties_Details.objects.get(id=id)

        context = {'admin_obj':admin_obj,'ameneties':ameneties}
        return render(request,'admin_user/Ameneties/update_ameneties.html',context)
    else:
        return render(request,'home_page/Adminlogin.html')

########### Views end for update ameneties data #####################


############# Views start for nearby facilities list #####################

def Facilities_List(request):
    session_id = request.session.get('Admin_id')
    if session_id:
        admin_obj = Admin_Login.objects.get(id=session_id)

        facilities_obj = Facilities_Details.objects.all().order_by('-id')
        facilities_obj_count = Facilities_Details.objects.all().count()

        rendered = render_to_string("admin_user/render_to_string/R_Facilities/r_t_s_facilities.html",{'facilities_obj':facilities_obj,'facilities_obj_count':facilities_obj_count})

        context = {'admin_obj':admin_obj,'facilities_list':rendered}
        return render(request,"admin_user/Nearby_Facility/facilities_list.html",context)
    else:
        return render(request,'home_page/Adminlogin.html')

############ Views end for nearby facilities list ##########################


############# Views start for ajax for add/update nearby facilities ##############

@csrf_exempt
def Facilities_Ajax(request):
    data = request.POST.dict()

    if data.get('id') == "":
        data.pop("id", None)         
        data['facilities_date'] = datetime.today()
        data['facilities_time'] = datetime.now()
        Facilities_Details.objects.create(**data)
        return JsonResponse({"status":"1", "msg" : f"Nearby Facilities Details added successfully"})

    # UPDATE MODE
    else:
        try:
            facilities = Facilities_Details.objects.get(id=data['id'])
        except Facilities_Details.DoesNotExist:
            return JsonResponse({'status': '0', 'msg': 'Facilities Details not found'})


        # Update withdraw fields (unchanged)
        for key, value in data.items():
            setattr(facilities, key, value)

        facilities.save()
        return JsonResponse({"status":"1", "msg" : f"Nearby Facilities Details updated successfully"})

############# Views end for ajax for add/update nearby facilities #################


########### Views start for upload facilities data via excel ######################

@csrf_exempt
def Facilities_Data(request):
    if request.method == 'POST':

        excel_file = request.FILES.get('facilities_file')

        wb = load_workbook(excel_file)
        sheet = wb.active

        for row in sheet.iter_rows(min_row=2, values_only=True):

            facilities_icon = row[0]
            facilities_name = row[1]

            if not facilities_icon or not facilities_name:
                continue

            Facilities_Details.objects.update_or_create(
                facilities_name=facilities_name,  # condition to check existing
                defaults={
                    "facilities_icon": facilities_icon,
                    "facilities_date": datetime.today(),
                    "facilities_time": datetime.now()
                }
            )

        return JsonResponse({
            "status": "1",
            "msg": "Data Uploaded / Updated Successfully..."
        })

    return JsonResponse({
        "status": "0",
        "msg": "Something went wrong..."
    })

########### Views end for upload facilities data via excel ########################


############# Views start for delete facilities data ######################

@csrf_exempt
def Delete_Facilities(request):
    try:
        try:
            facilities_id = request.POST.get('facilities_id')
            Facilities_Details.objects.filter(id=facilities_id).delete()
            return JsonResponse({'status':'1', 'msg':'Facilities details deleted successfully...'}) 
        except:
            traceback.print_exc()
            return JsonResponse({"status":"0", "msg" : "Something went wrong..."})
    except:
        traceback.print_exc()
        return JsonResponse({"status":"0", "msg" : "Something went wrong..."})

############# Views end for delete facilities data ###########################


############### Views start for update facilities data ########################

def Update_Facilities(request,id):
    session_id = request.session.get('Admin_id')
    if session_id:
        admin_obj = Admin_Login.objects.get(id=session_id)

        facilities = Facilities_Details.objects.get(id=id)

        context = {'admin_obj':admin_obj,'facilities':facilities}
        return render(request,'admin_user/Nearby_Facility/update_facilities.html',context)
    else:
        return render(request,'home_page/Adminlogin.html')

############## Views end for update facilities data #########################


########## Views start for vendor services list ########################

def Services_List(request):
    session_id = request.session.get('Admin_id')
    if session_id:
        admin_obj = Admin_Login.objects.get(id=session_id)

        services_obj = Service_Type_Details.objects.all().order_by('-id')
        services_obj_count = Service_Type_Details.objects.all().count()

        rendered = render_to_string("admin_user/render_to_string/R_Services/r_t_s_services.html",{'services_obj':services_obj,'services_obj_count':services_obj_count})

        context = {'admin_obj':admin_obj,'services_list':rendered}

        return render(request,"admin_user/Service_Type/service_type_list.html",context)
    else:
        return render(request,'home_page/Adminlogin.html')

############## Views end for vendor services list ###########################


########## Views start for ajax for add/update service types ###################

@csrf_exempt
def Services_Ajax(request):
    data = request.POST.dict()

    if data.get('id') == "":
        data.pop("id", None)         
        data['service_upload_date'] = datetime.today()
        data['service_upload_time'] = datetime.now()
        Service_Type_Details.objects.create(**data)
        return JsonResponse({"status":"1", "msg" : f"Service Type Details added successfully"})

    # UPDATE MODE
    # else:
    #     try:
    #         ameneties = Ameneties_Details.objects.get(id=data['id'])
    #     except Ameneties_Details.DoesNotExist:
    #         return JsonResponse({'status': '0', 'msg': 'Ameneties Details not found'})


    #     # Update withdraw fields (unchanged)
    #     for key, value in data.items():
    #         setattr(ameneties, key, value)

    #     ameneties.save()
    #     return JsonResponse({"status":"1", "msg" : f"Ameneties Details updated successfully"})

########## Views end for ajax for add/update service types ########################


############ Views start for upload service type details via excel ###################

@csrf_exempt
def Services_Data(request):
    if request.method == 'POST':

        excel_file = request.FILES.get('services_file')

        wb = load_workbook(excel_file)
        sheet = wb.active

        for row in sheet.iter_rows(min_row=2, values_only=True):

            service_id = row[0]
            service_name = row[1]

            if not service_id or not service_id:
                continue

            Service_Type_Details.objects.update_or_create(
                service_id=service_id,  # condition to check existing
                defaults={
                    "service_name": service_name,
                    "service_upload_date": datetime.today(),
                    "service_upload_time": datetime.now()
                }
            )

        return JsonResponse({
            "status": "1",
            "msg": "Data Uploaded / Updated Successfully..."
        })

    return JsonResponse({
        "status": "0",
        "msg": "Something went wrong..."
    })

############ Views end for upload service type details via excel ######################


############  Views start for rental property list ########################



############ Views end for rental property list ###########################


########### Views start for commercial property list ###################





import io
import csv
from datetime import datetime, date

import openpyxl
from django.contrib import messages
from django.http import HttpResponse, JsonResponse
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST

from Admin_App.models import CommercialRentalProperty, Admin_Login  # ← update app name if needed


# ─────────────────────────────────────────────
#  Helper converters
# ─────────────────────────────────────────────

def _str(val):
    if val is None:
        return None
    s = str(val).strip()
    return s if s else None

def _int(val):
    try:
        return int(float(str(val).strip()))
    except (TypeError, ValueError):
        return None

def _float(val):
    try:
        return float(str(val).strip())
    except (TypeError, ValueError):
        return None

def _bool(val):
    if val is None:
        return False
    return str(val).strip().lower() in ('true', '1', 'yes')

def _date(val):
    if val is None:
        return None
    if isinstance(val, (date, datetime)):
        return val.date() if isinstance(val, datetime) else val
    try:
        return datetime.strptime(str(val).strip(), "%Y-%m-%d").date()
    except ValueError:
        try:
            return datetime.strptime(str(val).strip(), "%d-%m-%Y").date()
        except ValueError:
            return None


# ─────────────────────────────────────────────
#  Column map — matches Excel template exactly
# ─────────────────────────────────────────────

COMMERCIAL_COLUMN_MAP = [
    # Basic Info
    ("property_title",       "property_title",       _str),
    ("property_type",        "property_type",        _str),
    ("city",                 "city",                 _str),
    ("area_locality",        "area_locality",        _str),
    ("property_address",     "property_address",     _str),
    ("building_name",        "building_name",        _str),
    ("possession_status",    "possession_status",    _str),
    ("available_from",       "available_from",       _date),
    ("age_of_property",      "age_of_property",      _str),
    ("zone_type",            "zone_type",            _str),
    ("location_hub",         "location_hub",         _str),
    ("property_condition",   "property_condition",   _str),
    ("ownership_type",       "ownership_type",       _str),
    ("construction_status",  "construction_status",  _str),
    # Area & Pricing
    ("builtup_area",         "builtup_area",         _int),
    ("carpet_area",          "carpet_area",          _int),
    ("expected_rent",        "expected_rent",        _int),
    ("security_deposit",     "security_deposit",     _int),
    ("maintenance_charges",  "maintenance_charges",  _int),
    ("negotiable",           "negotiable",           _bool),
    ("brokerage",            "brokerage",            _str),
    ("brokerage_percentage", "brokerage_percentage", _str),
    ("manual_brokerage",     "manual_brokerage",     _str),
    # Utilities
    ("dg_ups_included",      "dg_ups_included",      _bool),
    ("electricity_included", "electricity_included", _bool),
    ("water_included",       "water_included",       _bool),
    ("lockin_period",        "lockin_period",        _int),
    ("rent_increase",        "rent_increase",        _float),
    # Building Details
    ("total_floors",         "total_floors",         _int),
    ("your_floor",           "your_floor",           _int),
    ("staircases",           "staircases",           _int),
    ("passenger_lifts",      "passenger_lifts",      _int),
    ("service_lifts",        "service_lifts",        _int),
    ("private_parking",      "private_parking",      _int),
    # Office Facilities
    ("min_seats",            "min_seats",            _int),
    ("max_seats",            "max_seats",            _int),
    ("cabins",               "cabins",               _int),
    ("meeting_rooms",        "meeting_rooms",        _int),
    ("private_washroom",     "private_washroom",     _int),
    ("public_washroom",      "public_washroom",      _int),
    ("flooring_type",        "flooring_type",        _str),
    # Nearby
    ("metro_station",        "metro_station",        _str),
    ("bus_stop",             "bus_stop",             _str),
    ("restaurants",          "restaurants",          _str),
    ("banks",                "banks",                _str),
    # Amenities
    ("parking",              "parking",              _bool),
    ("security",             "security",             _bool),
    ("ac",                   "ac",                   _bool),
    ("power_backup",         "power_backup",         _bool),
    ("cafeteria",            "cafeteria",            _bool),
    ("conference_room",      "conference_room",      _bool),
    ("fire_safety",          "fire_safety",          _bool),
    ("cctv",                 "cctv",                 _bool),
    # Owner
    ("owner_name",           "owner_name",           _str),
    ("contact_number",       "contact_number",       _str),
    ("email",                "email",                _str),
    ("alternate_contact",    "alternate_contact",    _str),
    # Uploaded By
    ("uploaded_by_name",     "uploaded_by_name",     _str),
    ("uploaded_by_email",    "uploaded_by_email",    _str),
    ("uploaded_by_contact",  "uploaded_by_contact",  _str),
    ("uploaded_by_role",     "uploaded_by_role",     _str),
]


# ─────────────────────────────────────────────
#  Commercial List View
# ─────────────────────────────────────────────

def commercial_list(request):
    session_id = request.session.get('Admin_id')
    if not session_id:
        return render(request, 'home_page/Adminlogin.html')

    admin_obj = Admin_Login.objects.get(id=session_id)
    search_query = request.GET.get('search', '').strip()

    properties = CommercialRentalProperty.objects.all().order_by('-id')

    if search_query:
        properties = properties.filter(
            Q(property_title__icontains=search_query) |
            Q(property_type__icontains=search_query) |
            Q(city__icontains=search_query) |
            Q(area_locality__icontains=search_query) |
            Q(owner_name__icontains=search_query) |
            Q(possession_status__icontains=search_query)
        )

    # CSV Download
    if request.GET.get('download') == 'csv':
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="commercial_rental_properties.csv"'
        writer = csv.writer(response)
        writer.writerow([cm[0] for cm in COMMERCIAL_COLUMN_MAP])
        for p in properties:
            writer.writerow([
                p.property_title, p.property_type, p.city, p.area_locality, p.property_address,
                p.building_name, p.possession_status,
                p.available_from.strftime('%d-%m-%Y') if p.available_from else '',
                p.age_of_property, p.zone_type, p.location_hub, p.property_condition,
                p.ownership_type, p.construction_status,
                p.builtup_area, p.carpet_area, p.expected_rent, p.security_deposit,
                p.maintenance_charges, p.negotiable, p.brokerage,
                p.brokerage_percentage, p.manual_brokerage,
                p.dg_ups_included, p.electricity_included, p.water_included,
                p.lockin_period, p.rent_increase,
                p.total_floors, p.your_floor, p.staircases, p.passenger_lifts,
                p.service_lifts, p.private_parking,
                p.min_seats, p.max_seats, p.cabins, p.meeting_rooms,
                p.private_washroom, p.public_washroom, p.flooring_type,
                p.metro_station, p.bus_stop, p.restaurants, p.banks,
                p.parking, p.security, p.ac, p.power_backup,
                p.cafeteria, p.conference_room, p.fire_safety, p.cctv,
                p.owner_name, p.contact_number, p.email, p.alternate_contact,
                p.uploaded_by_name, p.uploaded_by_email,
                p.uploaded_by_contact, p.uploaded_by_role,
            ])
        return response

    paginator = Paginator(properties, 10)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    context = {
        'admin_obj': admin_obj,
        'page_obj': page_obj,
        'search_query': search_query,
        'total_count': properties.count(),
    }
    return render(request, 'admin_user/Reports/Rental/commercial_list.html', context)


# ─────────────────────────────────────────────
#  Import Excel View
# ─────────────────────────────────────────────

@require_POST
def import_commercial_excel(request):
    excel_file = request.FILES.get("commercial_file")

    if not excel_file:
        return JsonResponse({"status": "error", "message": "No file uploaded."}, status=400)

    if not excel_file.name.endswith(".xlsx"):
        return JsonResponse({"status": "error", "message": "Only .xlsx files are accepted."}, status=400)

    try:
        wb = openpyxl.load_workbook(excel_file, read_only=True, data_only=True)
        ws = wb.active
    except Exception as e:
        return JsonResponse({"status": "error", "message": f"Could not open file: {e}"}, status=400)

    # Build header index map
    headers = {}
    for col_idx, cell in enumerate(next(ws.iter_rows(min_row=1, max_row=1)), 1):
        if cell.value:
            headers[str(cell.value).strip()] = col_idx

    # Check required columns exist
    missing = [cm[0] for cm in COMMERCIAL_COLUMN_MAP if cm[0] not in headers]
    if missing:
        return JsonResponse({
            "status": "error",
            "message": f"Missing columns: {', '.join(missing[:8])}{'...' if len(missing) > 8 else ''}"
        }, status=400)

    created_count = 0
    error_rows = []

    for row_idx, row in enumerate(ws.iter_rows(min_row=2, values_only=True), start=2):
        if all(v is None or str(v).strip() == "" for v in row):
            continue

        obj_fields = {}
        row_error = None

        for excel_col, model_field, converter in COMMERCIAL_COLUMN_MAP:
            col_idx = headers.get(excel_col)
            if col_idx is None:
                continue
            raw_val = row[col_idx - 1] if col_idx - 1 < len(row) else None
            try:
                obj_fields[model_field] = converter(raw_val)
            except Exception as e:
                row_error = f"Row {row_idx}, col '{excel_col}': {e}"
                break

        if row_error:
            error_rows.append(row_error)
            continue

        # Required field defaults to avoid DB NOT NULL errors
        obj_fields.setdefault('property_type', 'office-space')
        obj_fields.setdefault('city', '')
        obj_fields.setdefault('area_locality', '')
        obj_fields.setdefault('property_address', '')
        obj_fields.setdefault('building_name', '')
        obj_fields.setdefault('possession_status', 'ready-to-move')
        obj_fields.setdefault('age_of_property', '0-1')
        obj_fields.setdefault('property_condition', 'bare-shell')
        obj_fields.setdefault('ownership_type', 'freehold')
        obj_fields.setdefault('builtup_area', 0)
        obj_fields.setdefault('expected_rent', 0)
        obj_fields.setdefault('owner_name', '')
        obj_fields.setdefault('contact_number', '')
        obj_fields.setdefault('email', '')

        try:
            CommercialRentalProperty.objects.create(**obj_fields)
            created_count += 1
        except Exception as e:
            error_rows.append(f"Row {row_idx}: DB error — {e}")

    wb.close()

    return JsonResponse({
        "status": "success",
        "message": f"{created_count} record(s) imported successfully." + (
            f" {len(error_rows)} row(s) had errors." if error_rows else ""
        ),
        "created": created_count,
        "errors": error_rows,
        "error_count": len(error_rows),
    })


# ─────────────────────────────────────────────
#  Download Template View
# ─────────────────────────────────────────────

def download_commercial_template(request):
    from openpyxl import Workbook
    from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
    from openpyxl.utils import get_column_letter

    wb = Workbook()
    ws = wb.active
    ws.title = "Commercial Rental"

    columns = [cm[0] for cm in COMMERCIAL_COLUMN_MAP]

    header_fill = PatternFill("solid", start_color="DC2626", end_color="DC2626")
    header_font = Font(bold=True, color="FFFFFF", name="Arial", size=10)
    thin_border = Border(
        left=Side(style='thin', color='CCCCCC'),
        right=Side(style='thin', color='CCCCCC'),
        top=Side(style='thin', color='CCCCCC'),
        bottom=Side(style='thin', color='CCCCCC'),
    )

    for col_idx, col_name in enumerate(columns, 1):
        cell = ws.cell(row=1, column=col_idx, value=col_name)
        cell.font = header_font
        cell.fill = header_fill
        cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
        cell.border = thin_border
        ws.column_dimensions[get_column_letter(col_idx)].width = max(18, len(col_name) + 4)

    ws.row_dimensions[1].height = 35
    ws.freeze_panes = "A2"

    buffer = io.BytesIO()
    wb.save(buffer)
    buffer.seek(0)

    response = HttpResponse(
        buffer.getvalue(),
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
    response["Content-Disposition"] = 'attachment; filename="commercial_rental_import_template.xlsx"'
    return response
############### Views end for commercial property list ########################


######### Views start for pg co living rental list ########################



   


import csv
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, HttpResponse
from django.core.paginator import Paginator
from django.db.models import Q
from django.views.decorators.http import require_POST

from Admin_App.models import PGColivingProperty, Admin_Login  # ← update app name if needed


# ─────────────────────────────────────────────────────────────
# LIST VIEW
# ─────────────────────────────────────────────────────────────
def pg_list(request):
    session_id = request.session.get('Admin_id')
    if not session_id:
        return render(request, 'home_page/Adminlogin.html')

    try:
        admin_obj = Admin_Login.objects.get(id=session_id)
    except Admin_Login.DoesNotExist:
        return render(request, 'home_page/Adminlogin.html')

    search_query = request.GET.get('search', '').strip()
    pg_for_filter = request.GET.get('pg_for', '').strip()       # boys / girls / co-living
    city_filter   = request.GET.get('city', '').strip()

    # Base queryset — newest first
    properties = PGColivingProperty.objects.all().order_by('-id')

    # ── Search ────────────────────────────────────────────────
    if search_query:
        properties = properties.filter(
            Q(pg_name__icontains=search_query)       |
            Q(city__icontains=search_query)          |
            Q(locality__icontains=search_query)      |
            Q(building_name__icontains=search_query) |
            Q(owner_name__icontains=search_query)    |
            Q(contact_number__icontains=search_query)
        )

    # ── Filters ───────────────────────────────────────────────
    if pg_for_filter:
        properties = properties.filter(pg_for=pg_for_filter)

    if city_filter:
        properties = properties.filter(city__icontains=city_filter)

    total_count = properties.count()

    # ── CSV Download ──────────────────────────────────────────
    if request.GET.get('download') == 'csv':
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="pg_coliving_properties.csv"'
        writer = csv.writer(response)

        writer.writerow([
            'ID', 'PG Name', 'City', 'Locality', 'Building Name',
            'PG For', 'Furnishing', 'Room Type', 'Total Beds',
            'Rent', 'Security Deposit', 'Min Stay',
            'Meals Available', 'Owner Name', 'Contact', 'Email',
            'Added On',
        ])

        for p in properties:
            writer.writerow([
                p.id,
                p.pg_name,
                p.city,
                p.locality,
                p.building_name or '',
                p.get_pg_for_display(),
                p.get_furnishing_type_display(),
                p.get_room_type_display(),
                p.total_beds,
                p.rent,
                p.security_deposit,
                p.minimum_stay,
                'Yes' if p.meals_available else 'No',
                p.owner_name,
                p.contact_number,
                p.email,
                p.created_at.strftime('%d-%m-%Y') if p.created_at else '',
            ])

        return response

    # ── Pagination ────────────────────────────────────────────
    paginator   = Paginator(properties, 10)
    page_number = request.GET.get('page', 1)
    page_obj    = paginator.get_page(page_number)

    # Distinct cities for filter dropdown
    cities = (PGColivingProperty.objects
              .values_list('city', flat=True)
              .distinct()
              .order_by('city'))

    context = {
        'admin_obj':     admin_obj,
        'page_obj':      page_obj,
        'search_query':  search_query,
        'pg_for_filter': pg_for_filter,
        'city_filter':   city_filter,
        'total_count':   total_count,
        'cities':        cities,
    }
    return render(request, 'admin_user/Reports/Rental/pg_list.html', context)


# ─────────────────────────────────────────────────────────────
# DELETE VIEW  (POST only — called via JS fetch)
# ─────────────────────────────────────────────────────────────
@require_POST
def pg_delete(request, pk):
    session_id = request.session.get('Admin_id')
    if not session_id:
        return JsonResponse({'status': 'error', 'message': 'Unauthorized'}, status=401)

    prop = get_object_or_404(PGColivingProperty, pk=pk)
    prop.delete()
    return JsonResponse({'status': 'success', 'message': 'Property deleted successfully.'})

########### Views end for pg co living rental list ########################


def residential_resale(request):
    session_id = request.session.get('Admin_id')
    if session_id:
        admin_obj = Admin_Login.objects.get(id=session_id)

        ameneties_obj = Ameneties_Details.objects.all()
        facilities_obj = Facilities_Details.objects.all()

        context = {'admin_obj':admin_obj,'ameneties_obj':ameneties_obj,'facilities_obj':facilities_obj}
        return render(request,"admin_user/Resale/residential_resale.html",context)
    else:
        return render(request,'home_page/Adminlogin.html')
    

def commercial_resale(request):
    session_id = request.session.get('Admin_id')
    if session_id:
        admin_obj = Admin_Login.objects.get(id=session_id)

        ameneties_obj = Ameneties_Details.objects.all()
        facilities_obj = Facilities_Details.objects.all()

        context = {'admin_obj':admin_obj,'ameneties_obj':ameneties_obj,'facilities_obj':facilities_obj}
        return render(request,"admin_user/Resale/commercial_resale.html",context)
    else:
        return render(request,'home_page/Adminlogin.html')


def plot_resale(request):
    session_id = request.session.get('Admin_id')
    if session_id:
        admin_obj = Admin_Login.objects.get(id=session_id)
        context = {'admin_obj':admin_obj}
        return render(request,"admin_user/Resale/plot_resale.html",context)
    else:
        return render(request,'home_page/Adminlogin.html')


def industrial_resale(request):
    session_id = request.session.get('Admin_id')
    if session_id:
        admin_obj = Admin_Login.objects.get(id=session_id)
        context = {'admin_obj':admin_obj}
        return render(request,"admin_user/Resale/industrial_resale.html",context)
    else:
        return render(request,'home_page/Adminlogin.html')
    

def agricultural_resale(request):
    session_id = request.session.get('Admin_id')
    if session_id:
        admin_obj = Admin_Login.objects.get(id=session_id)
        context = {'admin_obj':admin_obj}
        return render(request,"admin_user/Resale/agricultural_resale.html",context)
    else:
        return render(request,'home_page/Adminlogin.html')


############# Views start for resale residential property list ###################


from django.db.models import Count



# ─────────────────────────────────────────────────────────
# LIST VIEW
# ─────────────────────────────────────────────────────────
def residential_resale_list(request):

    session_id = request.session.get('Admin_id')
    if not session_id:
        return render(request, 'home_page/Adminlogin.html')

    admin_obj = Admin_Login.objects.get(id=session_id)

    # ── Fetch all properties with images ──────────────
    properties = ResaleResidentialProperty.objects.prefetch_related('images').order_by('-created_at')

    # ── Attach first image as thumbnail ──────────────
    for prop in properties:
        prop.thumbnail = prop.images.first()

    # ── Stat card counts ──────────────────────────────
    total_negotiable  = properties.filter(is_negotiable='yes').count()
    total_furnished   = properties.filter(furnishing_type='fully').count()
    total_freehold    = properties.filter(ownership_type='freehold').count()
    total_with_images = sum(1 for p in properties if p.thumbnail)

    # ── Chart data ────────────────────────────────────

    # Property type distribution
    property_type_counts = dict(
        properties.values_list('property_type')
                  .annotate(count=Count('id'))
                  .values_list('property_type', 'count')
    )

    # BHK distribution
    bhk_counts = dict(
        properties.values_list('bhk')
                  .annotate(count=Count('id'))
                  .values_list('bhk', 'count')
    )

    # Furnishing breakdown (for doughnut)
    fully_furnished = properties.filter(furnishing_type='fully').count()
    semi_furnished  = properties.filter(furnishing_type='semi').count()
    unfurnished     = properties.filter(furnishing_type='unfurnished').count()

    # Zone distribution
    zone_counts = dict(
        properties.values_list('zone')
                  .annotate(count=Count('id'))
                  .values_list('zone', 'count')
    )

    context = {
        'admin_obj'           : admin_obj,
        'properties'          : properties,

        # Stat cards
        'total_negotiable'    : total_negotiable,
        'total_furnished'     : total_furnished,
        'total_freehold'      : total_freehold,
        'total_with_images'   : total_with_images,

        # Charts
        'property_type_counts': property_type_counts,
        'bhk_counts'          : bhk_counts,
        'fully_furnished'     : fully_furnished,
        'semi_furnished'      : semi_furnished,
        'unfurnished'         : unfurnished,
        'zone_counts'         : zone_counts,
    }
    return render(request, 'admin_user/Reports/Resale/residential_resale_list.html', context)









############ Views end for resale residential list #######################


########### Views start for resale commercial property list ######################



from django.shortcuts import render
from django.db.models import Count, Avg
from django.utils import timezone
import json

def commercial_resale_list(request):

    # ── Session check ─────────────────────────────────────
    admin_id = request.session.get('Admin_id')
    user_id  = request.session.get('User_id')

    if not admin_id and not user_id:
        return render(request, 'home_page/Adminlogin.html')

    # ── Get admin or user object ───────────────────────────
    admin_obj = None
    user_obj  = None

    if admin_id:
        try:
            admin_obj = Admin_Login.objects.get(id=admin_id)
        except Admin_Login.DoesNotExist:
            return render(request, 'home_page/Adminlogin.html')

    elif user_id:
        try:
            user_obj = User_Details.objects.get(id=user_id)
        except User_Details.DoesNotExist:
            return render(request, 'home_page/Adminlogin.html')

    # ── Queryset ───────────────────────────────────────────
    props = CommercialProperty.objects.all().order_by('-id')

    # ── Stat cards ─────────────────────────────────────────
    total_properties = props.count()

    office_count     = props.filter(property_type='office-space').count()
    shop_count       = props.filter(property_type='shop').count()
    warehouse_count  = props.filter(property_type='warehouse').count()
    industrial_count = props.filter(property_type='industrial').count()
    land_count       = props.filter(property_type='land').count()

    #  FIXED (use correct field)
    avg_price = props.aggregate(
        Avg('expected_rent')
    )['expected_rent__avg']

    # ── Chart 1: Property Type Pie ─────────────────────────
    type_map = {
        'office-space': 'Office Space',
        'shop'        : 'Shop/Showroom',
        'warehouse'   : 'Warehouse',
        'industrial'  : 'Industrial',
        'land'        : 'Land',
    }

    type_qs = props.values('property_type').annotate(count=Count('id'))

    type_labels = [
        type_map.get(x['property_type'], x['property_type'])
        for x in type_qs
    ]
    type_data = [x['count'] for x in type_qs]

    # ── Chart 2: Monthly Data (Current Year) ───────────────
    current_year = timezone.now().year
    monthly_data = [0] * 12

    monthly_qs = props.filter(
        created_at__year=current_year
    ).values('created_at__month').annotate(count=Count('id'))

    for x in monthly_qs:
        monthly_data[x['created_at__month'] - 1] = x['count']

    # ── Chart 3: Zone Distribution ─────────────────────────
    zone_map = {
        'industrial'      : 'Industrial',
        'commercial'      : 'Commercial',
        'residential'     : 'Residential',
        'special-economic': 'SEZ',
    }

    zone_qs = props.values('zone_type').annotate(count=Count('id'))

    zone_labels = [
        zone_map.get(x['zone_type'], x['zone_type'])
        for x in zone_qs
    ]
    zone_data = [x['count'] for x in zone_qs]

    # ── Context ────────────────────────────────────────────
    context = {
        # user/session
        'admin_obj': admin_obj,
        'user_obj' : user_obj,

        # table
        'commercial_list': props,

        # stats
        'total_properties': total_properties,
        'office_count'    : office_count,
        'shop_count'      : shop_count,
        'warehouse_count' : warehouse_count,
        'industrial_count': industrial_count,
        'land_count'      : land_count,
        'avg_price'       : avg_price,

        # charts
        'chart_type_labels' : json.dumps(type_labels),
        'chart_type_data'   : json.dumps(type_data),
        'chart_monthly_data': json.dumps(monthly_data),
        'chart_zone_labels' : json.dumps(zone_labels),
        'chart_zone_data'   : json.dumps(zone_data),
    }

    return render(request, 'admin_user/Reports/Resale/commercial_list.html', context)

############# Views end for resale commercial property list ############################


######## Views start for resale plot commercial property list ###################

def plot_resale_list(request):
    session_id = request.session.get('Admin_id')
    if session_id:
        admin_obj = Admin_Login.objects.get(id=session_id)
        context = {'admin_obj':admin_obj}
        return render(request,'admin_user/Reports/Resale/plot_list.html',context)
    else:
        return render(request,'home_page/Adminlogin.html')

############# Views end for resale plot commercial property list ########################


########## Views start for resale industrial property list ##################

def industrial_resale_list(request):
    session_id = request.session.get('Admin_id')
    if session_id:
        admin_obj = Admin_Login.objects.get(id=session_id)
        context = {'admin_obj':admin_obj}
        return render(request,'admin_user/Reports/Resale/industrial_list.html',context)
    else:
        return render(request,'home_page/Adminlogin.html')

############ Views end for resale industrial property list ######################


########## Views start for resale agricultural resale list ######################

def agricultural_resale_list(request):
    session_id = request.session.get('Admin_id')
    if session_id:
        admin_obj = Admin_Login.objects.get(id=session_id)
        context = {'admin_obj':admin_obj}
        return render(request,'admin_user/Reports/Resale/agricultural_list.html',context)
    else:
        return render(request,'home_page/Adminlogin.html')

######### Views end for agricultural resale list ############################


########### Views start for display rm list ##########################

def rm_list(request):
    session_id = request.session.get('Admin_id')
    if session_id:
        admin_obj = Admin_Login.objects.get(id=session_id)

        rm_obj = User_Details.objects.filter(user_role="Relationship Manager").order_by('-id')
        rm_obj_count = User_Details.objects.filter(user_role="Relationship Manager").count()

        rendered = render_to_string("admin_user/render_to_string/R_RM/r_t_s_rm.html",{'rm_obj':rm_obj,'rm_obj_count':rm_obj_count,'Role':'Relationship Manager'})

        context = {'admin_obj':admin_obj,'rm_list':rendered}
        return render(request,'admin_user/RM/rm_list.html',context)
    else:
        return render(request,'home_page/Adminlogin.html')

############ Views end for display rm list ###########################


############ Views start for add rm ############################

def Add_RM(request):
    session_id = request.session.get('Admin_id')
    if session_id:
        admin_obj = Admin_Login.objects.get(id=session_id)
        context = {'admin_obj':admin_obj}
        return render(request,'admin_user/RM/add_rm.html',context)
    else:
        return render(request,'home_page/Adminlogin.html')

################ Views end for add rm ###########################


########### Views start for data upload functtionality via excel ##############

@csrf_exempt
def Rm_Data(request):

    if request.method == 'POST':

        excel_file = request.FILES.get('rm_file')

        if not excel_file:
            return JsonResponse({"status": "0", "msg": "Excel file not found"})

        wb = load_workbook(excel_file)
        sheet = wb.active

        for row in sheet.iter_rows(min_row=2, values_only=True):

            user_name = row[0]
            user_email = row[1]
            user_phone = row[2]
            user_state = row[3]
            user_city = row[4]
            user_address = row[5]
            user_password = row[6]
            user_profile = row[7]
            user_role = row[8]

            if user_password is not None:
                user_password = str(user_password).split(".")[0]

            if user_phone is not None:
                user_phone = str(user_phone).split(".")[0]

            if not user_phone:
                continue

            User_Details.objects.update_or_create(
                user_phone=user_phone,
                user_role = user_role,   # unique identifier
                defaults={
                    "user_name": user_name,
                    "user_email": user_email,
                    "user_state": user_state,
                    "user_city": user_city,
                    "user_address": user_address,
                    "user_profile": user_profile,
                    "user_password": user_password,
                    "user_register_date": datetime.today(),
                    "user_register_time": datetime.now()
                }
            )

        return JsonResponse({
            "status": "1",
            "msg": "Data Uploaded / Updated Successfully..."
        })

    return JsonResponse({
        "status": "0",
        "msg": "Invalid Request"
    })

########## Views end for data upload functionality via excel #######################


########### Views start for delete rm details ######################

@csrf_exempt
def Delete_RM(request):
    try:
        try:
            rm_id = request.POST.get('rm_id')
            User_Details.objects.filter(id=rm_id).delete()
            return JsonResponse({'status':'1', 'msg':'RM details deleted successfully...'}) 
        except:
            traceback.print_exc()
            return JsonResponse({"status":"0", "msg" : "Something went wrong..."})
    except:
        traceback.print_exc()
        return JsonResponse({"status":"0", "msg" : "Something went wrong..."})

############ Views end for delete rm details #########################


########### Views start for update rm details #########################

def Update_RM(request,id):
    session_id = request.session.get('Admin_id')
    if session_id:
        admin_obj = Admin_Login.objects.get(id=session_id)
        rm = User_Details.objects.get(id=id)

        context = {'admin_obj':admin_obj,'rm':rm}
        return render(request,'admin_user/RM/update_rm.html',context)
    else:
        return render(request,'home_page/Adminlogin.html')

######### Views end for update rm details #############################


########## Views start for ajax for add/update rm functionality #################4

@csrf_exempt
def User_Ajax(request):
    data = request.POST.dict()

    # --- HANDLE NEW FIELDS ---
    # 1. Handle Checkboxes: .dict() fails on lists, so we use .getlist
    user_operational_scope = data.get('user_operational_scope')
    if user_operational_scope == 'all':
        data['selected_regions'] = "All Over India"
    else:
        # We sent it as a JSON string from AJAX
        regions_raw = request.POST.get('selected_regions')
        try:
            regions_list = json.loads(regions_raw)
            data['selected_regions'] = ", ".join(regions_list)
        except (json.JSONDecodeError, TypeError):
            data['selected_regions'] = ""

    if data.get('id') == "":
        data.pop("id", None)
        data['user_profile'] = request.FILES.get('user_profile')         
        data['user_register_date'] = datetime.today()
        data['user_register_time'] = datetime.now()
        if User_Details.objects.filter(user_role=data['user_role'],user_phone=data['user_phone']).exists():
            return JsonResponse({"status":"0", "msg" : f"User with this phone number already exists"})
        else:
            User_Details.objects.create(**data)
            return JsonResponse({"status":"1", "msg" : f"User Details added successfully"})

    # UPDATE MODE
    else:
        try:
            rm = User_Details.objects.get(id=data['id'])
        except User_Details.DoesNotExist:
            return JsonResponse({'status': '0', 'msg': 'User Details not found'})
        
        data['user_profile'] = request.FILES.get('user_profile')

        if request.FILES.get('user_profile'):
            data['user_profile'] = request.FILES.get('user_profile')
        else:
            data.pop('user_profile', None)


        # Update withdraw fields (unchanged)
        for key, value in data.items():
            setattr(rm, key, value)

        rm.save()
        return JsonResponse({"status":"1", "msg" : f"User Details updated successfully"})

########### Views end for ajax for add/update rm functionality ###################


########### Views start for display landlords list ###################

def Landlord_List(request):
    session_id = request.session.get('Admin_id')
    if session_id:
        admin_obj = Admin_Login.objects.get(id=session_id)

        landlord_obj = User_Details.objects.filter(user_role="Landlord").order_by('-id')
        landlord_obj_count = User_Details.objects.filter(user_role="Landlord").count()

        rendered = render_to_string("admin_user/render_to_string/R_Landlord/r_t_s_landlord.html",{'landlord_obj':landlord_obj,'landlord_obj_count':landlord_obj_count,'Role':'Landlord'})

        context = {'admin_obj':admin_obj,'landlords_list':rendered}

        return render(request,'admin_user/Landlord/landlord_list.html',context)
    else:
        return render(request,'home_page/Adminlogin.html')

############ Views end for display landlords list ######################


############ Views start for add landlords #####################

def Add_Landlord(request):
    session_id = request.session.get('Admin_id')
    if session_id:
        admin_obj = Admin_Login.objects.get(id=session_id)
        context = {'admin_obj':admin_obj}
        return render(request,'admin_user/Landlord/add_landlord.html',context)
    else:
        return render(request,'home_page/Adminlogin.html')

########### Views end for add landlords ########################


########### Views start for upload landlord data functionality via excel ###############

@csrf_exempt
def Landlord_Data(request):
    if request.method == 'POST':

        excel_file = request.FILES.get('landlord_file')

        if not excel_file:
            return JsonResponse({"status": "0", "msg": "Excel file not found"})

        wb = load_workbook(excel_file)
        sheet = wb.active

        for row in sheet.iter_rows(min_row=2, values_only=True):

            user_name = row[0]
            user_email = row[1]
            user_phone = row[2]
            user_state = row[3]
            user_city = row[4]
            user_address = row[5]
            user_password = row[6]
            user_profile = row[7]
            user_role = row[8]

            if user_password is not None:
                user_password = str(user_password).split(".")[0]

            if user_phone is not None:
                user_phone = str(user_phone).split(".")[0]

            if not user_phone:
                continue

            User_Details.objects.update_or_create(
                user_phone=user_phone, 
                user_role=user_role,  # unique identifier
                defaults={
                    "user_name": user_name,
                    "user_email": user_email,
                    "user_state": user_state,
                    "user_city": user_city,
                    "user_address": user_address,
                    "user_profile": user_profile,
                    "user_password": user_password,
                    "user_register_date": datetime.today(),
                    "user_register_time": datetime.now()
                }
            )

        return JsonResponse({
            "status": "1",
            "msg": "Data Uploaded / Updated Successfully..."
        })

    return JsonResponse({
        "status": "0",
        "msg": "Invalid Request"
    })

############ Views end for upload landlord data functionality via excel ##################


############ Views start for delete landlord details ########################

@csrf_exempt
def Delete_Landlord(request):
    try:
        try:
            landlord_id = request.POST.get('landlord_id')
            User_Details.objects.filter(id=landlord_id).delete()
            return JsonResponse({'status':'1', 'msg':'Landlord details deleted successfully...'}) 
        except:
            traceback.print_exc()
            return JsonResponse({"status":"0", "msg" : "Something went wrong..."})
    except:
        traceback.print_exc()
        return JsonResponse({"status":"0", "msg" : "Something went wrong..."})

########## Views end for delete landlord details ##############################


############### Views start for update landlord details #####################

def Update_Landlord(request,id):
    session_id = request.session.get('Admin_id')
    if session_id:
        admin_obj = Admin_Login.objects.get(id=session_id)

        landlord = User_Details.objects.get(id=id)

        context = {'admin_obj':admin_obj,'landlord':landlord}
        return render(request,'admin_user/Landlord/update_landlord.html',context)
    else:
        return render(request,'home_page/Adminlogin.html')

############## Views end for update landlord details ###########################


######### Views start for display tenants list #####################

def Tenant_List(request):
    session_id = request.session.get('Admin_id')
    if session_id:
        admin_obj = Admin_Login.objects.get(id=session_id)

        tenant_obj = User_Details.objects.filter(user_role="Tenant").order_by('-id')
        tenant_obj_count = User_Details.objects.filter(user_role="Tenant").count()

        rendered = render_to_string("admin_user/render_to_string/R_Tenant/r_t_s_tenant.html",{'tenant_obj':tenant_obj,'tenant_obj_count':tenant_obj_count,'Role':'Tenant'})


        context = {'admin_obj':admin_obj,'tenants_list':rendered}
        
        return render(request,'admin_user/Tenant/tenant_list.html',context)
    else:
        return render(request,'home_page/Adminlogin.html')

############ Views end for display tenants list ########################


############ Views start for add tenants ######################

def Add_Tenant(request):
    session_id = request.session.get('Admin_id')
    if session_id:
        admin_obj = Admin_Login.objects.get(id=session_id)
        context = {'admin_obj':admin_obj}
        return render(request,'admin_user/Tenant/add_tenant.html',context)
    else:
        return render(request,'home_page/Adminlogin.html')

######## Views end for add tenants ##########################


########## Views start for upload tenant data functionality via excel ##############

@csrf_exempt
def Tenant_Data(request):
    if request.method == 'POST':

        excel_file = request.FILES.get('tenant_file')

        if not excel_file:
            return JsonResponse({"status": "0", "msg": "Excel file not found"})

        wb = load_workbook(excel_file)
        sheet = wb.active

        for row in sheet.iter_rows(min_row=2, values_only=True):

            user_name = row[0]
            user_email = row[1]
            user_phone = row[2]
            user_state = row[3]
            user_city = row[4]
            user_address = row[5]
            user_password = row[6]
            user_profile = row[7]
            user_role = row[8]

            if user_password is not None:
                user_password = str(user_password).split(".")[0]

            if user_phone is not None:
                user_phone = str(user_phone).split(".")[0]

            if not user_phone:
                continue

            User_Details.objects.update_or_create(
                user_phone=user_phone, 
                user_role=user_role,  # unique identifier
                defaults={
                    "user_name": user_name,
                    "user_email": user_email,
                    "user_state": user_state,
                    "user_city": user_city,
                    "user_address": user_address,
                    "user_profile": user_profile,
                    "user_password": user_password,
                    "user_register_date": datetime.today(),
                    "user_register_time": datetime.now()
                }
            )

        return JsonResponse({
            "status": "1",
            "msg": "Data Uploaded / Updated Successfully..."
        })

    return JsonResponse({
        "status": "0",
        "msg": "Invalid Request"
    })

######### Views end for upload tenant data functionality via excel ####################


########### Views start for delete tenant details #######################

@csrf_exempt
def Delete_Tenant(request):
    try:
        try:
            tenant_id = request.POST.get('tenant_id')
            User_Details.objects.filter(id=tenant_id).delete()
            return JsonResponse({'status':'1', 'msg':'Tenant details deleted successfully...'}) 
        except:
            traceback.print_exc()
            return JsonResponse({"status":"0", "msg" : "Something went wrong..."})
    except:
        traceback.print_exc()

########### Views end for delete tenant details ############################


############ Views start for update tenant details ###################

def Update_Tenant(request,id):
    session_id = request.session.get('Admin_id')
    if session_id:
        admin_obj = Admin_Login.objects.get(id=session_id)

        tenant = User_Details.objects.get(id=id)

        context = {'admin_obj':admin_obj,'tenant':tenant}
        return render(request,'admin_user/Tenant/update_tenant.html',context)
    else:
        return render(request,'home_page/Adminlogin.html')


############### Views start for display buyers list ####################

def Buyer_List(request):
    session_id = request.session.get('Admin_id')
    if session_id:
        admin_obj = Admin_Login.objects.get(id=session_id)

        buyer_obj = User_Details.objects.filter(user_role="Buyer").order_by('-id')
        buyer_obj_count = User_Details.objects.filter(user_role="Buyer").count()

        rendered = render_to_string("admin_user/render_to_string/R_Buyer/r_t_s_buyer.html",{'buyer_obj':buyer_obj,'buyer_obj_count':buyer_obj_count,'Role':'Buyer'})

        context = {'admin_obj':admin_obj,'buyer_list':rendered}

        return render(request,'admin_user/Buyer/buyer_list.html',context)
    else:
        return render(request,'home_page/Adminlogin.html')

############## Views end for display buyers list #########################


############# Views start for add buyers ########################

def Add_Buyer(request):
    session_id = request.session.get('Admin_id')
    if session_id:
        admin_obj = Admin_Login.objects.get(id=session_id)
        context = {'admin_obj':admin_obj}
        return render(request,'admin_user/Buyer/add_buyer.html',context)
    else:
        return render(request,'home_page/Adminlogin.html')

############ Views end for add buyers ###############################


############# Views start for buyer data functionality via excel ####################

@csrf_exempt
def Buyer_Data(request):
    if request.method == 'POST':

        excel_file = request.FILES.get('buyer_file')

        if not excel_file:
            return JsonResponse({"status": "0", "msg": "Excel file not found"})

        wb = load_workbook(excel_file)
        sheet = wb.active

        for row in sheet.iter_rows(min_row=2, values_only=True):

            user_name = row[0]
            user_email = row[1]
            user_phone = row[2]
            user_state = row[3]
            user_city = row[4]
            user_address = row[5]
            user_password = row[6]
            user_profile = row[7]
            user_role = row[8]

            if user_password is not None:
                user_password = str(user_password).split(".")[0]

            if user_phone is not None:
                user_phone = str(user_phone).split(".")[0]

            if not user_phone:
                continue

            User_Details.objects.update_or_create(
                user_phone=user_phone, 
                user_role=user_role,  # unique identifier
                defaults={
                    "user_name": user_name,
                    "user_email": user_email,
                    "user_state": user_state,
                    "user_city": user_city,
                    "user_address": user_address,
                    "user_profile": user_profile,
                    "user_password": user_password,
                    "user_register_date": datetime.today(),
                    "user_register_time": datetime.now()
                }
            )

        return JsonResponse({
            "status": "1",
            "msg": "Data Uploaded / Updated Successfully..."
        })

    return JsonResponse({
        "status": "0",
        "msg": "Invalid Request"
    })

######### Views end for buyer data functionality via excel ###########################


############ Views start for delete buyer details #######################

@csrf_exempt
def Delete_Buyer(request):
    try:
        try:
            buyer_id = request.POST.get('buyer_id')
            User_Details.objects.filter(id=buyer_id).delete()
            return JsonResponse({'status':'1', 'msg':'Buyer details deleted successfully...'}) 
        except:
            traceback.print_exc()
            return JsonResponse({"status":"0", "msg" : "Something went wrong..."})
    except:
        traceback.print_exc()

########## Views end for delete buyer details ###########################


########### Views start for update buyer details ###########################

def Update_Buyer(request,id):
    session_id = request.session.get('Admin_id')
    if session_id:
        admin_obj = Admin_Login.objects.get(id=session_id)

        buyer = User_Details.objects.get(id=id)

        context = {'admin_obj':admin_obj,'buyer':buyer}
        
        return render(request,'admin_user/Buyer/update_buyer.html',context)
    else:
        return render(request,'home_page/Adminlogin.html')

############# Views end for update buyer details ###############################


######### Views start for display agents list ##################

def Agent_List(request):
    session_id = request.session.get('Admin_id')
    if session_id:
        admin_obj = Admin_Login.objects.get(id=session_id)

        agent_obj = User_Details.objects.filter(user_role="Agent").order_by('-id')
        agent_obj_count = User_Details.objects.filter(user_role="Agent").count()

        rendered = render_to_string("admin_user/render_to_string/R_Agent/r_t_s_agent.html",{'agent_obj':agent_obj,'agent_obj_count':agent_obj_count,'Role':'Agent'})


        context = {'admin_obj':admin_obj,'agent_list':rendered}
        return render(request,'admin_user/Agent/agent_list.html',context)
    else:
        return render(request,'home_page/Adminlogin.html')

############ Views end for display agents list #################


############ Views start for add agents #################

def Add_Agent(request):
    session_id = request.session.get('Admin_id')
    if session_id:
        admin_obj = Admin_Login.objects.get(id=session_id)
        context = {'admin_obj':admin_obj}
        return render(request,'admin_user/Agent/add_agent.html',context)
    else:
        return render(request,'home_page/Adminlogin.html')

############## Views end for add agents #######################


########## Views start for upload agent data functionality via excel ###############

@csrf_exempt
def Agent_Data(request):
    if request.method == 'POST':

        excel_file = request.FILES.get('agent_file')

        if not excel_file:
            return JsonResponse({"status": "0", "msg": "Excel file not found"})

        wb = load_workbook(excel_file)
        sheet = wb.active

        for row in sheet.iter_rows(min_row=2, values_only=True):

            user_name = row[0]
            user_email = row[1]
            user_phone = row[2]
            user_state = row[3]
            user_city = row[4]
            user_address = row[5]
            user_password = row[6]
            user_agency_name = row[7]
            user_license_number = row[8]
            user_profile = row[9]
            user_role = row[10]

            if user_password is not None:
                user_password = str(user_password).split(".")[0]

            if user_phone is not None:
                user_phone = str(user_phone).split(".")[0]

            if not user_phone:
                continue

            User_Details.objects.update_or_create(
                user_phone=user_phone, 
                user_role=user_role,  # unique identifier
                defaults={
                    "user_name": user_name,
                    "user_email": user_email,
                    "user_state": user_state,
                    "user_city": user_city,
                    "user_address": user_address,
                    "user_profile": user_profile,
                    "user_password": user_password,
                    "user_agency_name": user_agency_name,
                    "user_license_number": user_license_number,
                    "user_register_date": datetime.today(),
                    "user_register_time": datetime.now()
                }
            )

        return JsonResponse({
            "status": "1",
            "msg": "Data Uploaded / Updated Successfully..."
        })

    return JsonResponse({
        "status": "0",
        "msg": "Invalid Request"
    })

########### Views end for upload agent data functionaity via excel #####################


############# Views start for delete agent ##############################

@csrf_exempt
def Delete_Agent(request):
    try:
        try:
            agent_id = request.POST.get('agent_id')
            User_Details.objects.filter(id=agent_id).delete()
            return JsonResponse({'status':'1', 'msg':'Agent details deleted successfully...'}) 
        except:
            traceback.print_exc()
            return JsonResponse({"status":"0", "msg" : "Something went wrong..."})
    except:
        traceback.print_exc()

########## Views ennd for delete agent ###################################


########### Views start for update agent details ################

def Update_Agent(request,id):
    session_id = request.session.get('Admin_id')
    if session_id:
        admin_obj = Admin_Login.objects.get(id=session_id)

        agent = User_Details.objects.get(id=id)

        context = {'admin_obj':admin_obj,'agent':agent}

        return render(request,'admin_user/Agent/update_agent.html',context)
    else:
        return render(request,'home_page/Adminlogin.html')

########## Views end for update agent details #####################


########## Views start for display agency list #########################

def Agency_List(request):
    session_id = request.session.get('Admin_id')
    if session_id:
        admin_obj = Admin_Login.objects.get(id=session_id)

        agency_obj = User_Details.objects.filter(user_role="Agency/Builder").order_by('-id')
        agency_obj_count = User_Details.objects.filter(user_role="Agency/Builder").count()

        rendered = render_to_string("admin_user/render_to_string/R_Agency/r_t_s_agency.html",{'agency_obj':agency_obj,'agency_obj_count':agency_obj_count,'Role':'Agency'})

        context = {'admin_obj':admin_obj,'agency_list':rendered}
        return render(request,'admin_user/Agency/agency_list.html',context)
    else:
        return render(request,'home_page/Adminlogin.html')

############ Views end for display agency list ############################


############### Views start for add agency ########################

def Add_Agency(request):
    session_id = request.session.get('Admin_id')
    if session_id:
        admin_obj = Admin_Login.objects.get(id=session_id)
        context = {'admin_obj':admin_obj}
        return render(request,'admin_user/Agency/add_agency.html',context)
    else:
        return render(request,'home_page/Adminlogin.html')

############ Views end for add agency ##########################


########## Views start for upload agency data functionality via excel #################

@csrf_exempt
def Agency_Data(request):
    if request.method == 'POST':

        excel_file = request.FILES.get('agency_file')

        if not excel_file:
            return JsonResponse({"status": "0", "msg": "Excel file not found"})

        wb = load_workbook(excel_file)
        sheet = wb.active

        for row in sheet.iter_rows(min_row=2, values_only=True):

            user_name = row[0]
            user_email = row[1]
            user_phone = row[2]
            user_state = row[3]
            user_city = row[4]
            user_address = row[5]
            user_password = row[6]
            user_agency_name = row[7]
            user_license_number = row[8]
            user_profile = row[9]
            user_role = row[10]

            if user_password is not None:
                user_password = str(user_password).split(".")[0]

            if user_phone is not None:
                user_phone = str(user_phone).split(".")[0]

            if not user_phone:
                continue

            User_Details.objects.update_or_create(
                user_phone=user_phone, 
                user_role=user_role,  # unique identifier
                defaults={
                    "user_name": user_name,
                    "user_email": user_email,
                    "user_state": user_state,
                    "user_city": user_city,
                    "user_address": user_address,
                    "user_profile": user_profile,
                    "user_password": user_password,
                    "user_agency_name": user_agency_name,
                    "user_license_number": user_license_number,
                    "user_register_date": datetime.today(),
                    "user_register_time": datetime.now()
                }
            )

        return JsonResponse({
            "status": "1",
            "msg": "Data Uploaded / Updated Successfully..."
        })

    return JsonResponse({
        "status": "0",
        "msg": "Invalid Request"
    })

############# Views end for upload agency data functionality via excel ##################


############## Views start for delete agency ###########################

@csrf_exempt
def Delete_Agency(request):
    try:
        try:
            agency_id = request.POST.get('agency_id')
            User_Details.objects.filter(id=agency_id).delete()
            return JsonResponse({"status":"1", "msg" : "Agency Details Deleted Successfully..."}) 
        except:
            traceback.print_exc()
            return JsonResponse({"status":"0", "msg" : "Something went wrong..."})
    except:
        traceback.print_exc()

############ Views end for delete agency ################################


########### Views start for update agency ###########################

def Update_Agency(request,id):
    session_id = request.session.get('Admin_id')
    if session_id:
        admin_obj = Admin_Login.objects.get(id=session_id)

        agency = User_Details.objects.get(id=id)
        
        context = {'admin_obj':admin_obj,'agency':agency}

        return render(request,'admin_user/Agency/update_agency.html',context)
    else:
        return render(request,'home_page/Adminlogin.html')

######### Views end for update agency ###############################


########## Views start for display vendors list ##################

def Vendor_List(request):
    session_id = request.session.get('Admin_id')
    if session_id:
        admin_obj = Admin_Login.objects.get(id=session_id)

        vendor_obj = User_Details.objects.filter(user_role="Vendor").order_by('-id')
        vendor_obj_count = User_Details.objects.filter(user_role="Vendor").count()

        rendered = render_to_string("admin_user/render_to_string/R_Vendor/r_t_s_vendor.html",{'vendor_obj':vendor_obj,'vendor_obj_count':vendor_obj_count,'Role':'Vendor'})

        context = {'admin_obj':admin_obj,'vendors_list':rendered}

        return render(request,'admin_user/Vendor/vendor_list.html',context)
    else:
        return render(request,'home_page/Adminlogin.html')

######### Views end for display vendors list ######################


########### Views start for add vendor #####################

def Add_Vendor(request):
    session_id = request.session.get('Admin_id')
    if session_id:
        admin_obj = Admin_Login.objects.get(id=session_id)

        services_obj = Service_Type_Details.objects.all()

        context = {'admin_obj':admin_obj,'services_obj':services_obj}
        return render(request,'admin_user/Vendor/add_vendor.html',context)
    else:
        return render(request,'home_page/Adminlogin.html')

############### Views end for add vendor #######################


############# Views start for upload vendor data functionality via excel ###############

@csrf_exempt
def Vendor_Data(request):
    if request.method == 'POST':
        excel_file = request.FILES.get('vendor_file')

        if not excel_file:
            return JsonResponse({"status": "0", "msg": "Excel file not found"})

        wb = load_workbook(excel_file)
        sheet = wb.active

        # We start from row 2 to skip headers
        for row in sheet.iter_rows(min_row=2, values_only=True):
            # Basic Fields
            user_name = row[0]
            user_email = row[1]
            user_phone = row[2]
            user_state = row[3]
            user_city = row[4]
            user_address = row[5]
            user_password = row[6]
            # Confirm Password is row[7], we skip it
            
            # New Vendor Fields (Matching the Excel I generated)
            user_service_type = row[8]
            user_company_name = row[9]
            user_pan_number = row[10]
            user_gstin_number = row[11]
            user_role = row[12]
            operational_areas = row[13]

            # Cleaning numeric strings (Phone/Password often come as floats from Excel)
            if user_password is not None:
                user_password = str(user_password).split(".")[0]

            if user_phone is not None:
                user_phone = str(user_phone).split(".")[0]

            if not user_phone:
                continue

            # Update or Create Logic
            User_Details.objects.update_or_create(
                user_phone=user_phone, 
                user_role=user_role,
                defaults={
                    "user_name": user_name,
                    "user_email": user_email,
                    "user_state": user_state,
                    "user_city": user_city,
                    "user_address": user_address,
                    "user_password": user_password,
                    "user_service_type": user_service_type,
                    "user_company_name": user_company_name,
                    "user_pan_number": user_pan_number,
                    "user_gstin_number": user_gstin_number,
                    "user_operational_scope": 'all' if operational_areas == 'All Over India' else 'other',
                    "selected_regions": operational_areas,
                    "user_register_date": datetime.today(),
                    "user_register_time": datetime.now()
                }
            )

        return JsonResponse({
            "status": "1",
            "msg": "Vendor Data Uploaded / Updated Successfully..."
        })

    return JsonResponse({"status": "0", "msg": "Invalid Request"})


############ Views end for upload vendor data functionality via excel #################


########## Views start for delete vendor ##########################

@csrf_exempt
def Delete_Vendor(request):
    try:
        try:
            vendor_id = request.POST.get('vendor_id')
            User_Details.objects.filter(id=vendor_id).delete()
            return JsonResponse({'status':'1', 'msg':'Vendor details deleted successfully...'}) 
        except:
            traceback.print_exc()
            return JsonResponse({"status":"0", "msg" : "Something went wrong..."})
    except:
        traceback.print_exc()
        return JsonResponse({"status":"0", "msg" : "Something went wrong..."})

############# Views end for delete vendor ###########################


############## Views start for update vendor #######################

def Update_Vendor(request,id):
    session_id = request.session.get('Admin_id')
    if session_id:
        admin_obj = Admin_Login.objects.get(id=session_id)

        services_obj = Service_Type_Details.objects.all()
        vendor = User_Details.objects.get(id=id)

        context = {'admin_obj':admin_obj,'services_obj':services_obj,'vendor':vendor}

        return render(request,'admin_user/Vendor/update_vendor.html',context)
    else:
        return render(request,'home_page/Adminlogin.html')

######### Views end for update vendor ##########################



def broadcast_email(request):
    return render(request,"admin_user/broadcast_email.html")



def send_message(request):
    
   
    if request.method == 'POST':
        WhatsAppMessage.objects.create(
            phone_number=request.POST.get('phone_number'),
            template=request.POST.get('template'),
            message=request.POST.get('message')
        )
       # return redirect('whatsapp_message:message_list')

   # return render(request, 'whatsapp_message/message_form.html')
    return render(request,"admin_user/send_message.html")



def commision_release_cycle(request):
    return render(request,"admin_user/commision_release_cycle.html")





from django.core.files.images import get_image_dimensions

def hero_section(request):
    if request.method == "POST":
        title = request.POST.get("title")
        subtitle = request.POST.get("subtitle")
        title_font_size = request.POST.get("title_font_size")
        subtitle_font_size = request.POST.get("subtitle_font_size")
        text_color = request.POST.get("text_color")
        overlay_color = request.POST.get("overlay_color")
        is_active = True if request.POST.get("is_active") == "on" else False

        background_image = request.FILES.get("background_image")

        # Validate image
        if background_image:
            # File size (max 2MB)
            if background_image.size > 2 * 1024 * 1024:
                messages.error(request, "Image size must be under 2MB")
                return redirect("hero_section_form")

            # Resolution (min 1200x600)
            width, height = get_image_dimensions(background_image)
            if width < 1200 or height < 600:
                messages.error(request, "Image resolution must be at least 1200x600 pixels")
                return redirect("hero_section_form")

        # Save to DB
        HeroSection.objects.create(
            title=title,
            subtitle=subtitle,
            title_font_size=title_font_size,
            subtitle_font_size=subtitle_font_size,
            text_color=text_color,
            overlay_color=overlay_color,
            background_image=background_image,
            is_active=is_active
        )

        messages.success(request, "Hero section saved successfully!")
       # return redirect("home")

    return render(request, "admin_user/hero_section.html")



def hero_section_list(request):
    heros = HeroSection.objects.all().order_by("-id")
    return render(request, "admin_user/hero_section_list.html", {"heros": heros})


def hero_section_edit(request, pk):
    hero = get_object_or_404(HeroSection, pk=pk)

    if request.method == "POST":
        hero.title = request.POST.get("title")
        hero.subtitle = request.POST.get("subtitle")
        hero.title_font_size = request.POST.get("title_font_size")
        hero.subtitle_font_size = request.POST.get("subtitle_font_size")
        hero.text_color = request.POST.get("text_color")
        hero.overlay_color = request.POST.get("overlay_color")
        hero.is_active = True if request.POST.get("is_active") == "on" else False

        if "background_image" in request.FILES:
            hero.background_image = request.FILES["background_image"]

        hero.save()
        messages.success(request, "Hero section updated successfully!")
        return redirect("hero_section_list")

    return render(request, "admin_user/hero_section_edit.html", {"hero": hero})


def hero_section_delete(request, pk):
    hero = get_object_or_404(HeroSection, pk=pk)
    hero.delete()
    messages.success(request, "Hero section deleted successfully!")
    return redirect("hero_section_list")


def hero_section_toggle(request, pk):
    hero = get_object_or_404(HeroSection, pk=pk)
    hero.is_active = not hero.is_active
    hero.save()
    messages.success(request, f"{hero.title} status updated successfully.")
    return redirect("hero_section_list")



from django.utils.text import slugify



def add_blog(request):
    if request.method == "POST":
        blog = Blog.objects.create(
            title=request.POST.get("title"),
            category=request.POST.get("category"),
            reading_time=request.POST.get("reading_time"),
            content=request.POST.get("content"),
            featured_image=request.FILES.get("featured_image"),
            author=request.POST.get("author"),
        )
        return redirect("blog_list")

    return render(request, "admin_user/blog_add.html")






def blog_list(request):
    blogs = Blog.objects.all().order_by("-date_posted")
    return render(request, "admin_user/blog_list.html", {"blogs": blogs})


def blog_delete(request, id):
    blog = get_object_or_404(Blog, id=id)
    blog.delete()
    return redirect("blog_list")


def blog_edit(request, id):
    blog = get_object_or_404(Blog, id=id)
    if request.method == "POST":
        blog.title = request.POST.get("title")
        blog.category = request.POST.get("category")
        blog.reading_time = request.POST.get("reading_time")
        blog.content = request.POST.get("content")
        if request.FILES.get("featured_image"):
            blog.featured_image = request.FILES.get("featured_image")
        blog.author = request.POST.get("author")
        blog.slug = slugify(blog.title)
        blog.save()
        return redirect("blog_list")

    return render(request, "admin_user/blog_edit.html", {"blog": blog})



# services/views.py


def add_service(request):
    if request.method == "POST":
        title = request.POST.get("title")
        icon = request.POST.get("icon")
        short_description = request.POST.get("short_description")
        content = request.POST.get("content")   # CKEditor sends HTML
        featured_image = request.FILES.get("featured_image")
        active = bool(request.POST.get('is_active'))

        service = Service(
            title=title,
            icon=icon,
            short_description=short_description,
            content=content,
            featured_image=featured_image,
           # is_active=active
            #active = bool(request.POST.get('is_active'))
        )
        service.save()
       # return redirect("services_list")  # after save go to list page

    return render(request, "admin_user/add_service.html")


def delete_service(request, service_id):
    service = get_object_or_404(Service, id=service_id)
    service.delete()
    return redirect("services_list")




def services_list(request):
    services = Service.objects.all().order_by('-id')
    return render(request, 'admin_user/services_list.html', {'services': services})

# ADD view
def add_about(request):
    if request.method == "POST":
        title = request.POST.get("title")
        description = request.POST.get("description")
        intro_badge = request.POST.get("intro_badge")
        intro_heading = request.POST.get("intro_heading")
        intro_content = request.POST.get("intro_content")
        founder_name = request.POST.get("founder_name")
        founder_role = request.POST.get("founder_role")
        founder_quote = request.POST.get("founder_quote")

        founder_image = request.FILES.get("founder_image")
        main_image = request.FILES.get("main_image")
        overlay_image = request.FILES.get("overlay_image")

        AboutPage.objects.create(
            title=title,
            description=description,
            intro_badge=intro_badge,
            intro_heading=intro_heading,
            intro_content=intro_content,
            founder_name=founder_name,
            founder_role=founder_role,
            founder_quote=founder_quote,
            founder_image=founder_image,
            main_image=main_image,
            overlay_image=overlay_image,
            years_of_excellence=request.POST.get("years_of_excellence", 1),
        )
      #  return redirect("about")  # show frontend about page

    return render(request, "admin_user/add_about.html")


# EDIT view
def edit_about(request, pk):
    about = get_object_or_404(AboutPage, pk=pk)

    if request.method == "POST":
        about.title = request.POST.get("title")
        about.description = request.POST.get("description")
        about.intro_badge = request.POST.get("intro_badge")
        about.intro_heading = request.POST.get("intro_heading")
        about.intro_content = request.POST.get("intro_content")
        about.founder_name = request.POST.get("founder_name")
        about.founder_role = request.POST.get("founder_role")
        about.founder_quote = request.POST.get("founder_quote")
        about.years_of_excellence = request.POST.get("years_of_excellence", 1)

        if request.FILES.get("founder_image"):
            about.founder_image = request.FILES.get("founder_image")
        if request.FILES.get("main_image"):
            about.main_image = request.FILES.get("main_image")
        if request.FILES.get("overlay_image"):
            about.overlay_image = request.FILES.get("overlay_image")

        about.save()
        return redirect("about")

    return render(request, "edit_about.html", {"about": about})





def achievements_page(request):
    achievements = Achievement.objects.all()

    if request.method == "POST":
        pk = request.POST.get("pk")
        if pk:
            achievement = get_object_or_404(Achievement, pk=pk)
            achievement.icon_class = request.POST.get("icon_class")
            achievement.number = request.POST.get("number")
            achievement.suffix = request.POST.get("suffix")
            achievement.label = request.POST.get("label")
            achievement.order = request.POST.get("order", 0)
            achievement.save()
        else:
            Achievement.objects.create(
                icon_class=request.POST.get("icon_class"),
                number=request.POST.get("number"),
                suffix=request.POST.get("suffix"),
                label=request.POST.get("label"),
                order=request.POST.get("order", 0),
            )
        #return redirect("achievements_page")

    return render(request, "admin_user/achievements_page.html", {"achievements": achievements})





def faq_list_admin(request):
    faqs = FAQ.objects.all().order_by('-created_at')
    return render(request, 'faq_list_admin.html', {'faqs': faqs})

()
def faq_add(request):
    if request.method == 'POST':
        question = request.POST['question']
        answer = request.POST['answer']
        FAQ.objects.create(question=question, answer=answer)
       # return redirect('faq_list_admin')
    return render(request, 'admin_user/faq_add.html')


def faq_edit(request, faq_id):
    faq = get_object_or_404(FAQ, id=faq_id)
    if request.method == 'POST':
        faq.question = request.POST['question']
        faq.answer = request.POST['answer']
        faq.save()
        return redirect('faq_list_admin')
    return render(request, 'faq_edit.html', {'faq': faq})


def faq_delete(request, faq_id):
    faq = get_object_or_404(FAQ, id=faq_id)
    if request.method == 'POST':
        faq.delete()
        return redirect('faq_list_admin')
    return render(request, 'faq_delete.html', {'faq': faq})

def faq_list_public(request):
    faqs = FAQ.objects.all().order_by('-created_at')
    return render(request, 'faq_list_public.html', {'faqs': faqs})





def timeline_page(request):
    timeline_items = TimelineItem.objects.all

    if request.method == "POST":
        pk = request.POST.get("pk")
        if pk:
            timeline = get_object_or_404(TimelineItem, pk=pk)
            timeline.year = request.POST.get("year")
            timeline.title = request.POST.get("title")
            timeline.description = request.POST.get("description")
            timeline.order = request.POST.get("order", 0)
            timeline.save()
        else:
            TimelineItem.objects.create(
                year=request.POST.get("year"),
                title=request.POST.get("title"),
                description=request.POST.get("description"),
                order=request.POST.get("order", 0),
            )
        #return redirect("timeline_page")

    return render(request, "admin_user/timeline_page.html", {"timeline_items": timeline_items})




def add_ad(request):
    if request.method == "POST":
        title = request.POST.get("title")
        category = request.POST.get("category")
        image = request.FILES.get("image")
        short_description = request.POST.get("short_description")
        detail_content = request.POST.get("detail_content")
        badge_text = request.POST.get("badge_text")
        badge_icon = request.POST.get("badge_icon")
        special_offer_title = request.POST.get("special_offer_title")
        special_offer_description = request.POST.get("special_offer_description")
        text_size_heading = request.POST.get("text_size_heading")
        text_size_paragraph = request.POST.get("text_size_paragraph")
        slug = request.POST.get("slug")

        ad = Ad(
            title=title,
            category=category,
            image=image,
            short_description=short_description,
            detail_content=detail_content,
            badge_text=badge_text,
            badge_icon=badge_icon,
            special_offer_title=special_offer_title,
            special_offer_description=special_offer_description,
            text_size_heading=text_size_heading,
            text_size_paragraph=text_size_paragraph,
            slug=slug
        )
        ad.save()
     #   return redirect("ad_list")

    return render(request, "admin_user/add_ad.html")









# seo/views.py


def seo_list(request):
    seo_pages = LocationSEO.objects.all().order_by('-id')
    return render(request, "admin_user/seo_list.html", {"seo_pages": seo_pages})


def toggle_seo_status(request, pk):
    seo_page = get_object_or_404(LocationSEO, pk=pk)
    seo_page.is_active = not seo_page.is_active
    seo_page.save()
    return redirect("seo_list")


def delete_seo_page(request, pk):
    seo_page = get_object_or_404(LocationSEO, pk=pk)
    seo_page.delete()
    return redirect("seo_list")




def edit_seo_page(request, pk):
    seo_page = get_object_or_404(LocationSEO, pk=pk)
    
    if request.method == "POST":
        seo_page.meta_title = request.POST.get("meta_title")
        seo_page.meta_description = request.POST.get("meta_description")
        seo_page.primary_keyword = request.POST.get("primary_keyword")
        seo_page.secondary_keywords = request.POST.get("secondary_keywords")
        seo_page.intro_html = request.POST.get("intro_html")
        seo_page.noindex = "noindex" in request.POST
        seo_page.is_active = "is_active" in request.POST
        seo_page.save()
        return redirect("seo_list")

    return render(request, "admin_user/seo_edit.html", {"page": seo_page})


def services_list1(request):
    services = LocationSEO.objects.filter(page_type="service", is_active=True)
    return render(request, "admin_user/services_list1.html", {"services": services})




def plans_list(request):
    plans = Plan.objects.all().order_by('-id')
    return render(request, "admin_user/plans_list.html", {'plans': plans})

def plan_add(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        plan_type = request.POST.get('plan_type')
        desc = request.POST.get('description')
        base_price = request.POST.get('base_price') or 0
        roles_visible = request.POST.get('roles_visible') or ''
        is_active = bool(request.POST.get('is_active'))
        plan = Plan.objects.create(
            name=name, plan_type=plan_type, description=desc,
            base_price=Decimal(base_price), roles_visible=roles_visible, is_active=is_active
        )
        return redirect('plans_list')
    return render(request, 'admin_user/plan_add.html')

def plan_edit(request, pid):
    plan = get_object_or_404(Plan, id=pid)
    if request.method == 'POST':
        plan.name = request.POST.get('name')
        plan.plan_type = request.POST.get('plan_type')
        plan.description = request.POST.get('description')
        plan.base_price = Decimal(request.POST.get('base_price') or 0)
        plan.roles_visible = request.POST.get('roles_visible') or ''
        plan.is_active = bool(request.POST.get('is_active'))
        plan.save()
        return redirect('plans_list')
    return render(request, 'admin_user/plan_edit.html', {'plan': plan})




# --- Add-On Create View ---
def addon_create(request):
    if request.method == 'POST':
        name = request.POST['name']
        description = request.POST['description']
        price = request.POST['price']
        applicableroles = request.POST.get('applicableroles', '')
        isactive = 'isactive' in request.POST

        Addon.objects.create(
            name=name,
            description=description,
            price=price,
            applicableroles=applicableroles,
            isactive=isactive,
        )
        messages.success(request, "Add-On created successfully!")
        return redirect('addon_list')

    return render(request, 'admin_user/addon_create.html')


# --- Add-On List View ---


#######################

from django.http import JsonResponse
from django.shortcuts import render

def rental_residential_add(request):

    admin_id = request.session.get('Admin_id')
    user_id = request.session.get('User_id')

    admin_obj = None
    user_obj = None

    # Detect who logged in
    if admin_id:
        admin_obj = Admin_Login.objects.get(id=admin_id)

    if user_id:
        user_obj = User_Details.objects.get(id=user_id)

    # If nobody logged in
    if not admin_obj and not user_obj:
        return render(request, 'home_page/Adminlogin.html')

    if request.method == 'POST':

        try:

            def to_int(val):
                try:
                    v = str(val).strip()
                    return int(v) if v else None
                except:
                    return None

            def to_decimal(val):
                try:
                    v = str(val).strip()
                    return float(v) if v else None
                except:
                    return None

            # Amenities
            amenities_list = request.POST.getlist('amenities[]')
            amenities = ",".join(amenities_list)

            # ---------------------------------
            # Detect uploader automatically
            # ---------------------------------

            if admin_obj:

                uploader_name = admin_obj.admin_name
                uploader_email = admin_obj.email
                uploader_contact = admin_obj.admin_phone
                uploader_role = "Admin"

            elif user_obj:

                uploader_name = user_obj.user_name
                uploader_email = user_obj.user_email
                uploader_contact = user_obj.user_phone
                uploader_role = "User"

            # ---------------------------------

            prop = RentalResidentialProperty(

                # Basic Info
                property_title=request.POST.get('property_title'),
                property_purpose=request.POST.get('property_purpose'),
                property_type=request.POST.get('property_type'),
                bhk_type=request.POST.get('bhk_type'),
                renting_option=request.POST.get('renting_option'),
                furnishing_status=request.POST.get('furnishing_status'),
                available_for=request.POST.get('available_for'),

                built_up_area=to_decimal(request.POST.get('built_up_area')),
                bathrooms=to_int(request.POST.get('bathrooms')),
                balconies=to_int(request.POST.get('balconies')),
                floor_number=request.POST.get('floor_number'),
                total_floors=to_int(request.POST.get('total_floors')),
                facing=request.POST.get('facing'),

                # Property Details
                zone=request.POST.get('zone'),
                ownership_type=request.POST.get('ownership_type'),
                construction_status=request.POST.get('construction_status'),
                property_age=request.POST.get('property_age'),
                carpet_area=to_decimal(request.POST.get('carpet_area')),
                plot_area=to_decimal(request.POST.get('plot_area')),
                building_name=request.POST.get('building_name'),

                # Availability
                possession_status=request.POST.get('possession_status'),
                available_from=request.POST.get('available_from'),
                lease_duration=request.POST.get('lease_duration'),
                brokerage=request.POST.get('brokerage'),
                brokerage_percentage=request.POST.get('brokerage_percentage'),
                manual_brokerage=request.POST.get('manual_brokerage'),

                # Pricing
                monthly_rent=to_int(request.POST.get('monthly_rent')),
                security_deposit=to_int(request.POST.get('security_deposit')),
                maintenance_type=request.POST.get('maintenance_type'),
                maintenance_amount=to_int(request.POST.get('maintenance_amount')),
                expected_price=to_int(request.POST.get('expected_price')),

                # Location
                address=request.POST.get('address'),
                city=request.POST.get('city'),
                locality=request.POST.get('locality'),
                state=request.POST.get('state'),
                pincode=request.POST.get('pincode'),
                road_connectivity=request.POST.get('road_connectivity'),

                # Amenities
                amenities=amenities,

                # Description
                description=request.POST.get('description'),
                rent_residential_desc=request.POST.get('rent_residential_desc'),

                # Owner
                owner_name=request.POST.get('owner_name'),
                contact_number=request.POST.get('contact_number'),
                email=request.POST.get('email'),
                alternate_contact=request.POST.get('alternate_contact'),

                # Uploaded By (AUTO)
                uploaded_by_name=uploader_name,
                uploaded_by_email=uploader_email,
                uploaded_by_contact=uploader_contact,
                uploaded_by_role=uploader_role,
            )

            # Images
            images = request.FILES.getlist('property_images[]')

            image_fields = [
                'image1','image2','image3','image4','image5',
                'image6','image7','image8','image9','image10'
            ]

            for i, img in enumerate(images[:10]):
                setattr(prop, image_fields[i], img)

            prop.save()

            return JsonResponse({
                'status': 'success',
                'message': 'Property listed successfully!'
            })

        except Exception as e:
            import traceback
            print(traceback.format_exc())

            return JsonResponse({
                'status': 'error',
                'message': str(e)
            })

    context = {
        'admin_obj': admin_obj,
        'user_obj': user_obj
    }

    return render(request, 'admin_user/Reports/Rental/rental_list.html', context)



import csv
import json
from django.db.models import Count, Avg, Max, Min, Q
from django.core.paginator import Paginator
from django.shortcuts import render
from django.http import HttpResponse


def rental_list(request):

    session_id = request.session.get('Admin_id')
    if not session_id:
        return render(request, 'home_page/Adminlogin.html')

    admin_obj = Admin_Login.objects.get(id=session_id)
    search_query = request.GET.get('search', '').strip()

    # ── Base queryset ──
    try:
        properties = RentalResidentialProperty.objects.all().order_by('-id')
        print("STEP 1 - properties count:", properties.count())
    except Exception as e:
        print("STEP 1 FAILED:", e)
        properties = RentalResidentialProperty.objects.none()

    # ── Search filter ──
    if search_query:
        try:
            properties = properties.filter(
                Q(property_title__icontains=search_query) |
                Q(property_type__icontains=search_query) |
                Q(bhk_type__icontains=search_query) |
                Q(city__icontains=search_query) |
                Q(locality__icontains=search_query) |
                Q(owner_name__icontains=search_query) |
                Q(possession_status__icontains=search_query)
            )
            print(" STEP 2 - search filter ok:", properties.count())
        except Exception as e:
            print(" STEP 2 FAILED:", e)
            properties = RentalResidentialProperty.objects.none()

    # ── CSV Download ──
    if request.GET.get('download') == 'csv':
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="rental_properties.csv"'
        writer = csv.writer(response)
        writer.writerow([
            'ID', 'Property Title', 'Property Purpose', 'Property Type', 'BHK Type',
            'Renting Option', 'Furnishing Status', 'Available For',
            'Built Up Area', 'Carpet Area', 'Plot Area',
            'Bathrooms', 'Balconies', 'Floor Number', 'Total Floors', 'Facing',
            'Zone', 'Ownership Type', 'Construction Status', 'Property Age', 'Building Name',
            'Possession Status', 'Available From', 'Lease Duration',
            'Brokerage', 'Brokerage %', 'Manual Brokerage',
            'Monthly Rent', 'Security Deposit', 'Maintenance Type',
            'Maintenance Amount', 'Expected Price',
            'Address', 'City', 'Locality', 'State', 'Pincode', 'Road Connectivity',
            'Amenities', 'Description', 'Rent Description',
            'Owner Name', 'Contact Number', 'Email', 'Alternate Contact',
            'Uploaded By Name', 'Uploaded By Email',
            'Uploaded By Contact', 'Uploaded By Role',
        ])
        for p in properties:
            writer.writerow([
                p.id, p.property_title, p.property_purpose, p.property_type, p.bhk_type,
                p.renting_option, p.furnishing_status, p.available_for,
                p.built_up_area, p.carpet_area, p.plot_area,
                p.bathrooms, p.balconies, p.floor_number, p.total_floors, p.facing,
                p.zone, p.ownership_type, p.construction_status, p.property_age, p.building_name,
                p.possession_status,
                p.available_from.strftime('%d-%m-%Y') if p.available_from else '',
                p.lease_duration,
                p.brokerage, p.brokerage_percentage, p.manual_brokerage,
                p.monthly_rent, p.security_deposit, p.maintenance_type,
                p.maintenance_amount, p.expected_price,
                p.address, p.city, p.locality, p.state, p.pincode, p.road_connectivity,
                p.amenities, p.description, p.rent_residential_desc,
                p.owner_name, p.contact_number, p.email, p.alternate_contact,
                p.uploaded_by_name, p.uploaded_by_email,
                p.uploaded_by_contact, p.uploaded_by_role,
            ])
        return response

    # ── Pagination ──
    try:
        paginator = Paginator(properties, 10)
        page_number = request.GET.get('page', 1)
        page_obj = paginator.get_page(page_number)
        print(" STEP 3 - page_obj count:", page_obj.object_list.count())
    except Exception as e:
        print("STEP 3 FAILED:", e)
        page_obj = Paginator(RentalResidentialProperty.objects.none(), 10).get_page(1)

    total_count = properties.count()
    print(" STEP 4 - total_count:", total_count)

    # ════════════════════════════════════════════════
    # STATS — computed on the FULL unfiltered queryset
    # so cards/charts always show global numbers
    # ════════════════════════════════════════════════
    all_props = RentalResidentialProperty.objects.all()

    # ── Summary stat cards ──
    active_count = all_props.exclude(
        possession_status__isnull=True
    ).exclude(possession_status='').count()

    furnished_count = all_props.filter(
        furnishing_status__iexact='Furnished'
    ).count()

    available_count = all_props.filter(
        possession_status__iexact='Ready to Move'
    ).count()

    city_count = all_props.exclude(
        city__isnull=True
    ).exclude(city='').values('city').distinct().count()

    # ── Rent aggregates (ignore nulls) ──
    rent_stats = all_props.exclude(
        monthly_rent__isnull=True
    ).aggregate(
        avg_rent=Avg('monthly_rent'),
        max_rent=Max('monthly_rent'),
        min_rent=Min('monthly_rent'),
    )
    avg_rent   = rent_stats['avg_rent']
    max_rent   = rent_stats['max_rent']
    min_rent   = rent_stats['min_rent']

    # ── Deposit average ──
    deposit_stats = all_props.exclude(
        security_deposit__isnull=True
    ).aggregate(avg_deposit=Avg('security_deposit'))
    avg_deposit = deposit_stats['avg_deposit']

    # ── Average built-up area ──
    area_stats = all_props.exclude(
        built_up_area__isnull=True
    ).aggregate(avg_area=Avg('built_up_area'))
    avg_area = area_stats['avg_area']

    # ── With owner info ──
    with_owner_count = all_props.exclude(
        owner_name__isnull=True
    ).exclude(owner_name='').count()

    # ── With at least one image ──
    with_images_count = all_props.exclude(
        image1__isnull=True
    ).exclude(image1='').count()

    # ════════════════════════════════════════════════
    # CHART DATA
    # ════════════════════════════════════════════════

    # ── Chart 1: BHK Distribution (Doughnut) ──
    bhk_qs = (
        all_props
        .exclude(bhk_type__isnull=True)
        .exclude(bhk_type='')
        .values('bhk_type')
        .annotate(count=Count('id'))
        .order_by('-count')
    )
    bhk_labels = json.dumps([item['bhk_type'] for item in bhk_qs])
    bhk_data   = json.dumps([item['count']    for item in bhk_qs])

    # ── Chart 2: Rent Range Distribution (Bar) ──
    # Bucket properties into rent brackets
    rent_buckets = [
        ('Under ₹5k',    0,      5000),
        ('₹5k–10k',      5000,   10000),
        ('₹10k–20k',     10000,  20000),
        ('₹20k–30k',     20000,  30000),
        ('₹30k–50k',     30000,  50000),
        ('₹50k–1L',      50000,  100000),
        ('Above ₹1L',    100000, 999999999),
    ]
    rent_range_labels = json.dumps([b[0] for b in rent_buckets])
    rent_range_data   = json.dumps([
        all_props.filter(
            monthly_rent__gte=lo,
            monthly_rent__lt=hi
        ).count()
        for _, lo, hi in rent_buckets
    ])

    # ── Chart 3: Furnishing Status (Doughnut) ──
    furnish_qs = (
        all_props
        .exclude(furnishing_status__isnull=True)
        .exclude(furnishing_status='')
        .values('furnishing_status')
        .annotate(count=Count('id'))
        .order_by('-count')
    )
    furnishing_labels = json.dumps([item['furnishing_status'] for item in furnish_qs])
    furnishing_data   = json.dumps([item['count']             for item in furnish_qs])

    # ── Chart 4: Property Type (Bar) ──
    prop_type_qs = (
        all_props
        .exclude(property_type__isnull=True)
        .exclude(property_type='')
        .values('property_type')
        .annotate(count=Count('id'))
        .order_by('-count')
    )
    prop_type_labels = json.dumps([item['property_type'] for item in prop_type_qs])
    prop_type_data   = json.dumps([item['count']         for item in prop_type_qs])

    # ════════════════════════════════════════════════
    # CONTEXT
    # ════════════════════════════════════════════════
    context = {
        # Auth
        'admin_obj': admin_obj,

        # Table
        'page_obj': page_obj,
        'search_query': search_query,
        'total_count': total_count,

        # Stat cards
        'active_count':      active_count,
        'furnished_count':   furnished_count,
        'available_count':   available_count,
        'city_count':        city_count,
        'avg_rent':          avg_rent,
        'max_rent':          max_rent,
        'min_rent':          min_rent,
        'avg_deposit':       avg_deposit,
        'avg_area':          avg_area,
        'with_owner_count':  with_owner_count,
        'with_images_count': with_images_count,

        # Chart data (JSON strings — safe to dump into JS variables)
        'bhk_labels':         bhk_labels,
        'bhk_data':           bhk_data,
        'rent_range_labels':  rent_range_labels,
        'rent_range_data':    rent_range_data,
        'furnishing_labels':  furnishing_labels,
        'furnishing_data':    furnishing_data,
        'prop_type_labels':   prop_type_labels,
        'prop_type_data':     prop_type_data,
    }

    print(" STEP 5 - context keys:", list(context.keys()))
    return render(request, 'admin_user/Reports/Rental/rental_list.html', context)

import os
import io
from datetime import datetime, date

import openpyxl
from django.contrib import messages
from django.http import JsonResponse, HttpResponse, FileResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import redirect





# ─────────────────────────────────────────────
#  Helper: safe type conversions
# ─────────────────────────────────────────────



# ─────────────────────────────────────────────
#  Helper converters
# ─────────────────────────────────────────────

def _str(val):
    if val is None:
        return None
    s = str(val).strip()
    return s if s else None


def _int(val):
    try:
        return int(float(str(val).strip()))
    except (TypeError, ValueError):
        return None


def _decimal(val):
    try:
        cleaned = str(val).replace(",", "").replace("₹", "").strip()
        return Decimal(cleaned)
    except Exception:
        return None


def _bigint(val):
    try:
        cleaned = str(val).replace(",", "").replace("₹", "").strip()
        return int(float(cleaned))
    except (TypeError, ValueError):
        return None


def _date(val):
    if val is None:
        return None
    if isinstance(val, (date, datetime)):
        return val.date() if isinstance(val, datetime) else val
    for fmt in ("%Y-%m-%d", "%d-%m-%Y", "%d/%m/%Y"):
        try:
            return datetime.strptime(str(val).strip(), fmt).date()
        except ValueError:
            continue
    return None


# ─────────────────────────────────────────────
#  Column → model field mapping
# ─────────────────────────────────────────────

def _email(val):
    if val is None:
        return None
    s = str(val).strip()
    if not s or '@' not in s:
        return None
    return s




@csrf_exempt
@require_POST
def import_residential_excel(request):

    #  Defined INSIDE the function — PG COLUMN_MAP cannot override this
    RESIDENTIAL_COLUMN_MAP = [
        ("property_title", "property_title", _str),
        ("property_purpose", "property_purpose", _str),
        ("property_type", "property_type", _str),
        ("bhk_type", "bhk_type", _str),
        ("renting_option", "renting_option", _str),
        ("furnishing_status", "furnishing_status", _str),
        ("available_for", "available_for", _str),
        ("built_up_area", "built_up_area", _decimal),
        ("bathrooms", "bathrooms", _int),
        ("balconies", "balconies", _int),
        ("floor_number", "floor_number", _str),
        ("total_floors", "total_floors", _int),
        ("facing", "facing", _str),
        ("zone", "zone", _str),
        ("ownership_type", "ownership_type", _str),
        ("construction_status", "construction_status", _str),
        ("property_age", "property_age", _str),
        ("carpet_area", "carpet_area", _decimal),
        ("plot_area", "plot_area", _decimal),
        ("building_name", "building_name", _str),
        ("possession_status", "possession_status", _str),
        ("available_from", "available_from", _date),
        ("lease_duration", "lease_duration", _str),
        ("brokerage", "brokerage", _str),
        ("brokerage_percentage", "brokerage_percentage", _str),
        ("manual_brokerage", "manual_brokerage", _str),
        ("monthly_rent", "monthly_rent", _bigint),
        ("security_deposit", "security_deposit", _bigint),
        ("maintenance_type", "maintenance_type", _str),
        ("maintenance_amount", "maintenance_amount", _bigint),
        ("expected_price", "expected_price", _bigint),
        ("address", "address", _str),
        ("city", "city", _str),
        ("locality", "locality", _str),
        ("state", "state", _str),
        ("pincode", "pincode", _str),
        ("road_connectivity", "road_connectivity", _str),
        ("amenities", "amenities", _str),
        ("description", "description", _str),
        ("rent_residential_desc", "rent_residential_desc", _str),
        ("owner_name", "owner_name", _str),
        ("contact_number", "contact_number", _str),
        ("email", "email", _email),
        ("alternate_contact", "alternate_contact", _str),
        ("uploaded_by_name", "uploaded_by_name", _str),
        ("uploaded_by_email", "uploaded_by_email", _str),
        ("uploaded_by_contact", "uploaded_by_contact", _str),
        ("uploaded_by_role", "uploaded_by_role", _str),
    ]

    excel_file = request.FILES.get("rental_file")

    if not excel_file:
        return JsonResponse({"status": "error", "message": "No file uploaded."}, status=400)

    if not excel_file.name.endswith(".xlsx"):
        return JsonResponse({"status": "error", "message": "Only .xlsx files are accepted."}, status=400)

    try:
        wb = openpyxl.load_workbook(excel_file, read_only=True, data_only=True)
        ws = wb.active
    except Exception as e:
        return JsonResponse({"status": "error", "message": f"Could not open file: {e}"}, status=400)

    # ── Read headers ──
    headers = {}
    first_row = next(ws.iter_rows(min_row=1, max_row=1))
    for col_idx, cell in enumerate(first_row, 1):
        if cell.value is not None:
            key = str(cell.value).strip().lower().replace(" ", "_")
            headers[key] = col_idx

    print("=" * 60)
    print("HEADERS FROM EXCEL:", list(headers.keys()))
    missing = [cm[0] for cm in RESIDENTIAL_COLUMN_MAP if cm[0].lower() not in headers]
    print("MISSING COLUMNS   :", missing)
    print("=" * 60)

    if missing:
        return JsonResponse({
            "status": "error",
            "message": f"Missing columns: {', '.join(missing)}"
        }, status=400)

    created_count = 0
    error_rows = []

    for row_idx, row in enumerate(ws.iter_rows(min_row=2, values_only=True), start=2):

        if all(v is None or str(v).strip() == "" for v in row):
            continue

        obj_fields = {}
        row_error = None

        for excel_col, model_field, converter in RESIDENTIAL_COLUMN_MAP:
            col_idx = headers.get(excel_col.lower())
            raw_val = row[col_idx - 1] if (col_idx and col_idx - 1 < len(row)) else None
            try:
                obj_fields[model_field] = converter(raw_val)
            except Exception as e:
                row_error = f"Row {row_idx}, col '{excel_col}': {e}"
                break

        if row_error:
            error_rows.append(row_error)
            continue

        try:
            obj = RentalResidentialProperty(**obj_fields)
            obj.save()
            created_count += 1
        except Exception as e:
            print(f" DB ERROR ROW {row_idx}:", e)
            error_rows.append(f"Row {row_idx}: DB error — {e}")

    wb.close()

    return JsonResponse({
        "status": "success",
        "message": f"{created_count} records imported, {len(error_rows)} errors",
        "created": created_count,
        "error_count": len(error_rows),
        "errors": error_rows,
    })

from django.views.decorators.http import require_POST




def download_residential_template(request):
    import openpyxl
    from django.http import HttpResponse

    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Residential Properties"

    #  Exact headers matching COLUMN_MAP
    headers = [
        "property_title", "property_purpose", "property_type", "bhk_type",
        "renting_option", "furnishing_status", "available_for", "built_up_area",
        "bathrooms", "balconies", "floor_number", "total_floors", "facing",
        "zone", "ownership_type", "construction_status", "property_age",
        "carpet_area", "plot_area", "building_name", "possession_status",
        "available_from", "lease_duration", "brokerage", "brokerage_percentage",
        "manual_brokerage", "monthly_rent", "security_deposit", "maintenance_type",
        "maintenance_amount", "expected_price", "address", "city", "locality",
        "state", "pincode", "road_connectivity", "amenities", "description",
        "rent_residential_desc", "owner_name", "contact_number", "email",
        "alternate_contact", "uploaded_by_name", "uploaded_by_email",
        "uploaded_by_contact", "uploaded_by_role"
    ]

    from openpyxl.styles import Font, PatternFill, Alignment
    header_font = Font(name="Arial", bold=True, color="FFFFFF", size=10)
    header_fill = PatternFill("solid", start_color="4F46E5")
    header_align = Alignment(horizontal="center", vertical="center")

    for col_idx, header in enumerate(headers, 1):
        cell = ws.cell(row=1, column=col_idx, value=header)
        cell.font = header_font
        cell.fill = header_fill
        cell.alignment = header_align
        ws.column_dimensions[openpyxl.utils.get_column_letter(col_idx)].width = 20

    ws.freeze_panes = "A2"

    # ── Send as download ──
    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = 'attachment; filename="rental_residential_template.xlsx"'
    wb.save(response)
    return response



def rental_residential_view(request, pk):
    """View a single property detail."""
    prop = get_object_or_404(RentalResidentialProperty, pk=pk)
    return render(request, 'admin_user/Reports/Rental/rental_residential_detail.html', {'property': prop})



def rental_residential_edit(request, pk):
    """Edit an existing property (no forms.py)."""
    prop = get_object_or_404(RentalResidentialProperty, pk=pk)

    if request.method == 'POST':
        try:
            prop.property_title = request.POST.get('property_title')
            prop.property_type = request.POST.get('property_type')
            prop.bhk_type = request.POST.get('bhk_type')
            prop.furnishing_status = request.POST.get('furnishing_status')
            prop.property_age = request.POST.get('property_age') or None
            prop.floor_number = request.POST.get('floor_number') or None
            prop.total_floors = request.POST.get('total_floors') or None
            prop.builtup_area = request.POST.get('built_up_area')
            prop.carpet_area = request.POST.get('carpet_area') or None
            prop.balconies = request.POST.get('balconies') or None
            prop.bathrooms = request.POST.get('bathrooms') or None
            prop.facing = request.POST.get('facing') or None
            prop.availability_status = request.POST.get('possession_status', '')
            prop.available_from = request.POST.get('available_from') or None
            prop.monthly_rent = request.POST.get('monthly_rent')
            prop.security_deposit = request.POST.get('security_deposit') or None
            prop.maintenance_charges = request.POST.get('maintenance_amount') or None
            prop.brokerage = request.POST.get('brokerage') or None
            prop.brokerage_percentage = request.POST.get('brokerage_percentage') or None
            prop.manual_brokerage = request.POST.get('manual_brokerage') or None
            prop.preferred_tenant = request.POST.get('available_for') or None
            prop.city = request.POST.get('city')
            prop.locality = request.POST.get('locality')
            prop.address = request.POST.get('address')
            prop.pincode = request.POST.get('pincode') or None
            prop.property_description = request.POST.get('rent_residential_desc', '')
            prop.owner_name = request.POST.get('owner_name')
            prop.owner_contact = request.POST.get('contact_number')
            prop.owner_email = request.POST.get('email')
            prop.uploaded_by_name = request.POST.get('uploaded_by_name') or None
            prop.uploaded_by_email = request.POST.get('uploaded_by_email') or None
            prop.uploaded_by_contact = request.POST.get('uploaded_by_contact') or None

            # Handle new images if uploaded
            images = request.FILES.getlist('property_images[]')
            image_fields = ['image1','image2','image3','image4','image5','image6','image7','image8']
            for i, img in enumerate(images[:8]):
                setattr(prop, image_fields[i], img)

            prop.save()
            return JsonResponse({'status': 'success', 'message': 'Property updated successfully!'})

        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)

    return render(request, 'admin_user/rental_residential_edit.html', {'property': prop})







def commercial_rental_add(request):

    admin_id = request.session.get('Admin_id')
    user_id = request.session.get('User_id')

    admin_obj = None
    user_obj = None

    uploader_name = ""
    uploader_email = ""
    uploader_phone = ""
    uploader_role = ""

    # ADMIN LOGIN
    if admin_id:
        admin_obj = Admin_Login.objects.get(id=admin_id)

        uploader_name = admin_obj.user_name
        uploader_email = admin_obj.email
        uploader_phone = admin_obj.phone
        uploader_role = admin_obj.role

    # USER LOGIN
    elif user_id:
        user_obj = User_Details.objects.get(id=user_id)

        uploader_name = user_obj.user_name
        uploader_email = user_obj.user_email
        uploader_phone = user_obj.user_phone
        uploader_role = user_obj.user_role

    else:
        return redirect('login')


    if request.method == "POST":

        prop = CommercialRentalProperty(

            property_type=request.POST.get('property_type'),
            city=request.POST.get('city'),
            area_locality=request.POST.get('area_locality'),
            property_address=request.POST.get('property_address'),
            building_name=request.POST.get('building_name'),

            possession_status=request.POST.get('possession_status'),
            available_from=request.POST.get('available_from'),
            age_of_property=request.POST.get('age_of_property'),

            zone_type=request.POST.get('zone_type'),
            location_hub=request.POST.get('location_hub'),

            property_condition=request.POST.get('property_condition'),
            ownership_type=request.POST.get('ownership_type'),
            construction_status=request.POST.get('construction_status'),

            builtup_area=request.POST.get('builtup_area'),
            carpet_area=request.POST.get('carpet_area'),

            expected_rent=request.POST.get('expected_rent'),
            security_deposit=request.POST.get('security_deposit'),
            maintenance_charges=request.POST.get('maintenance_charges'),

            brokerage=request.POST.get('brokerage'),
            brokerage_percentage=request.POST.get('brokerage_percentage'),
            manual_brokerage=request.POST.get('manual_brokerage'),

            owner_name=request.POST.get('owner_name'),
            contact_number=request.POST.get('contact_number'),
            email=request.POST.get('email'),
            alternate_contact=request.POST.get('alternate_contact'),

            # AUTO FILLED
            uploaded_by_name=uploader_name,
            uploaded_by_email=uploader_email,
            uploaded_by_contact=uploader_phone,
            uploaded_by_role=uploader_role,
        )

        # IMAGES
        images = request.FILES.getlist('property_images[]')

        if images:
            prop.property_images = images[0]

        prop.save()

        return JsonResponse({
            "status": "success",
            "message": "Commercial Property Added Successfully"
        })


    context = {
        "admin_obj": admin_obj,
        "user_obj": user_obj,

        "uploader_name": uploader_name,
        "uploader_email": uploader_email,
        "uploader_phone": uploader_phone,
        "uploader_role": uploader_role,
    }

  #  return render(request, "admin_user/commercial_rent_add.html", context)
    return render(request, 'admin_user/Reports/Rental/commer_list.html', context)


    
    path('commercial/list/',           views.commercial_list,   name='commercial_list'),
    path('commercial/view/<int:pk>/',  views.commercial_view,   name='commercial_view'),
    path('commercial/edit/<int:pk>/',  views.commercial_edit,   name='commercial_edit'),
    path('commercial/delete/<int:pk>/',views.commercial_delete, name='commercial_delete'),


from datetime import datetime
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from Admin_App.models import CommercialRentalProperty, Admin_Login


# ─────────────────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────────────────
def _get_admin(request):
    sid = request.session.get('Admin_id')
    if not sid:
        return None, None
    try:
        return sid, Admin_Login.objects.get(id=sid)
    except Admin_Login.DoesNotExist:
        return None, None

def _to_int(val):
    try:   return int(val) if val not in (None, '') else None
    except: return None

def _to_float(val):
    try:   return float(val) if val not in (None, '') else None
    except: return None


# ─────────────────────────────────────────────────────────
# DETAIL / VIEW PAGE
# ─────────────────────────────────────────────────────────
def commercial_view(request, pk):
    sid, admin_obj = _get_admin(request)
    if not sid:
        return render(request, 'home_page/Adminlogin.html')

    prop = get_object_or_404(CommercialRentalProperty, pk=pk)
    return render(request, 'admin_user/Reports/Rental/commercial_detail.html', {
        'admin_obj': admin_obj,
        'prop': prop,
    })


# ─────────────────────────────────────────────────────────
# EDIT PAGE
# ─────────────────────────────────────────────────────────
def commercial_edit(request, pk):
    sid, admin_obj = _get_admin(request)
    if not sid:
        return render(request, 'home_page/Adminlogin.html')

    prop = get_object_or_404(CommercialRentalProperty, pk=pk)

    if request.method == 'POST':
        p = request.POST

        # Basic Info
        prop.property_title      = p.get('property_title') or None
        prop.property_type       = p.get('property_type') or 'office-space'
        prop.city                = p.get('city', '')
        prop.area_locality       = p.get('area_locality', '')
        prop.property_address    = p.get('property_address', '')
        prop.building_name       = p.get('building_name', '')
        prop.possession_status   = p.get('possession_status', 'ready-to-move')
        prop.age_of_property     = p.get('age_of_property', '0-1')
        prop.zone_type           = p.get('zone_type') or None
        prop.location_hub        = p.get('location_hub') or None
        prop.property_condition  = p.get('property_condition', 'bare-shell')
        prop.ownership_type      = p.get('ownership_type', 'freehold')
        prop.construction_status = p.get('construction_status') or None

        avail = p.get('available_from')
        if avail:
            try:    prop.available_from = datetime.strptime(avail, '%Y-%m-%d').date()
            except: prop.available_from = None
        else:
            prop.available_from = None

        # Area & Pricing
        prop.builtup_area         = _to_int(p.get('builtup_area')) or 0
        prop.carpet_area          = _to_int(p.get('carpet_area'))
        prop.expected_rent        = _to_int(p.get('expected_rent')) or 0
        prop.security_deposit     = _to_int(p.get('security_deposit'))
        prop.maintenance_charges  = _to_int(p.get('maintenance_charges'))
        prop.negotiable           = p.get('negotiable') == 'True'
        prop.brokerage            = p.get('brokerage') or None
        prop.brokerage_percentage = p.get('brokerage_percentage') or None
        prop.manual_brokerage     = p.get('manual_brokerage') or None

        # Utilities
        prop.dg_ups_included      = p.get('dg_ups_included') == 'True'
        prop.electricity_included = p.get('electricity_included') == 'True'
        prop.water_included       = p.get('water_included') == 'True'
        prop.lockin_period        = _to_int(p.get('lockin_period'))
        prop.rent_increase        = _to_float(p.get('rent_increase'))

        # Building Details
        prop.total_floors    = _to_int(p.get('total_floors'))
        prop.your_floor      = _to_int(p.get('your_floor'))
        prop.staircases      = _to_int(p.get('staircases'))
        prop.passenger_lifts = _to_int(p.get('passenger_lifts')) or 0
        prop.service_lifts   = _to_int(p.get('service_lifts')) or 0
        prop.private_parking = _to_int(p.get('private_parking')) or 0

        # Office Facilities
        prop.min_seats        = _to_int(p.get('min_seats'))
        prop.max_seats        = _to_int(p.get('max_seats'))
        prop.cabins           = _to_int(p.get('cabins'))
        prop.meeting_rooms    = _to_int(p.get('meeting_rooms'))
        prop.private_washroom = _to_int(p.get('private_washroom')) or 0
        prop.public_washroom  = _to_int(p.get('public_washroom')) or 0
        prop.flooring_type    = p.get('flooring_type') or None

        # Nearby
        prop.metro_station = p.get('metro_station') or None
        prop.bus_stop      = p.get('bus_stop') or None
        prop.restaurants   = p.get('restaurants') or None
        prop.banks         = p.get('banks') or None

        # Amenities
        prop.parking         = 'parking'         in p
        prop.security        = 'security'        in p
        prop.ac              = 'ac'              in p
        prop.power_backup    = 'power_backup'    in p
        prop.cafeteria       = 'cafeteria'       in p
        prop.conference_room = 'conference_room' in p
        prop.fire_safety     = 'fire_safety'     in p
        prop.cctv            = 'cctv'            in p

        # Owner
        prop.owner_name        = p.get('owner_name', '')
        prop.contact_number    = p.get('contact_number', '')
        prop.email             = p.get('email', '')
        prop.alternate_contact = p.get('alternate_contact') or None

        # Uploaded By
        prop.uploaded_by_name    = p.get('uploaded_by_name') or None
        prop.uploaded_by_email   = p.get('uploaded_by_email') or None
        prop.uploaded_by_contact = p.get('uploaded_by_contact') or None
        prop.uploaded_by_role    = p.get('uploaded_by_role') or None

        # Media
        if 'property_images' in request.FILES:
            prop.property_images = request.FILES['property_images']
        if 'floor_plan' in request.FILES:
            prop.floor_plan = request.FILES['floor_plan']
        if 'video' in request.FILES:
            prop.video = request.FILES['video']

        prop.save()
        return redirect('commercial_list')

    return render(request, 'admin_user/commercial_edit.html', {
        'admin_obj': admin_obj,
        'prop': prop,
    })


# ─────────────────────────────────────────────────────────
# DELETE  (POST only, returns JSON — called via JS fetch)
# ─────────────────────────────────────────────────────────
@require_POST
def commercial_delete(request, pk):
    sid, _ = _get_admin(request)
    if not sid:
        return JsonResponse({'status': 'error', 'message': 'Unauthorized'}, status=401)

    prop = get_object_or_404(CommercialRentalProperty, pk=pk)
    prop.delete()
    return JsonResponse({'status': 'success', 'message': 'Property deleted successfully.'})









import os
import io
from datetime import datetime, date

import openpyxl
from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt

from Admin_App.models import PGColivingProperty  # ← update app name if needed


# ─────────────────────────────────────────────────────────────
#  Type converters
# ─────────────────────────────────────────────────────────────

def _str(val):
    if val is None:
        return None
    s = str(val).strip()
    return s if s else None


def _int(val):
    try:
        return int(float(str(val).strip()))
    except (TypeError, ValueError):
        return None


def _bool(val):
    """Accepts True/False (Python bool from openpyxl) or strings 'True'/'False'/'1'/'0'."""
    if isinstance(val, bool):
        return val
    if val is None:
        return False
    s = str(val).strip().lower()
    return s in ("true", "1", "yes")


def _date(val):
    if val is None:
        return None
    if isinstance(val, (date, datetime)):
        return val.date() if isinstance(val, datetime) else val
    s = str(val).strip()
    for fmt in ("%Y-%m-%d", "%d-%m-%Y", "%d/%m/%Y"):
        try:
            return datetime.strptime(s, fmt).date()
        except ValueError:
            continue
    return None


# ─────────────────────────────────────────────────────────────
#  Column → model field mapping
#  Order MUST match the Excel template column order
# ─────────────────────────────────────────────────────────────
COLUMN_MAP = [
    # (excel_header,          model_field,             converter)

    # ── Basic ────────────────────────────────────────────────
    ("city",                  "city",                  _str),
    ("building_name",         "building_name",         _str),
    ("locality",              "locality",              _str),
    ("pg_name",               "pg_name",               _str),
    ("property_address",      "property_address",      _str),
    ("total_beds",            "total_beds",            _int),
    ("pg_for",                "pg_for",                _str),
    ("furnishing_type",       "furnishing_type",       _str),
    ("best_suited_for",       "best_suited_for",       _str),

    # ── Room Details ─────────────────────────────────────────
    ("room_type",             "room_type",             _str),
    ("room_total_beds",       "room_total_beds",       _int),
    ("rent",                  "rent",                  _int),
    ("security_deposit",      "security_deposit",      _int),
    ("brokerage",             "brokerage",             _bool),
    ("brokerage_percentage",  "brokerage_percentage",  _str),
    ("manual_brokerage",      "manual_brokerage",      _str),

    # ── Room Facilities ───────────────────────────────────────
    ("attached_bathroom",     "attached_bathroom",     _bool),
    ("balcony",               "balcony",               _bool),
    ("ac",                    "ac",                    _bool),
    ("wardrobe",              "wardrobe",              _bool),
    ("study_table",           "study_table",           _bool),
    ("wifi_room",             "wifi_room",             _bool),

    # ── Meals ─────────────────────────────────────────────────
    ("meals_available",       "meals_available",       _bool),
    ("meal_offerings",        "meal_offerings",        _str),
    ("meal_speciality",       "meal_speciality",       _str),

    # ── Stay Rules ────────────────────────────────────────────
    ("notice_period",         "notice_period",         _int),
    ("lockin_period",         "lockin_period",         _int),
    ("minimum_stay",          "minimum_stay",          _int),
    ("available_from",        "available_from",        _date),

    # ── Property Management ───────────────────────────────────
    ("property_managed_by",   "property_managed_by",   _str),
    ("manager_stays",         "manager_stays",         _bool),

    # ── Common Area ───────────────────────────────────────────
    ("tv",                    "tv",                    _bool),
    ("refrigerator",          "refrigerator",          _bool),
    ("washing_machine",       "washing_machine",       _bool),
    ("kitchen",               "kitchen",               _bool),
    ("lounge",                "lounge",                _bool),

    # ── PG Rules ─────────────────────────────────────────────
    ("non_veg_allowed",       "non_veg_allowed",       _bool),
    ("opposite_sex_allowed",  "opposite_sex_allowed",  _bool),
    ("any_time_allowed",      "any_time_allowed",      _bool),
    ("visitors_allowed",      "visitors_allowed",      _bool),
    ("guardian_allowed",      "guardian_allowed",      _bool),
    ("drinking_allowed",      "drinking_allowed",      _bool),
    ("smoking_allowed",       "smoking_allowed",       _bool),

    # ── Nearby Facilities ─────────────────────────────────────
    ("colleges_nearby",       "colleges_nearby",       _str),
    ("offices_nearby",        "offices_nearby",        _str),
    ("transport_nearby",      "transport_nearby",      _str),
    ("markets_nearby",        "markets_nearby",        _str),

    # ── Amenities ────────────────────────────────────────────
    ("security_24x7",         "security_24x7",         _bool),
    ("power_backup",          "power_backup",          _bool),
    ("parking",               "parking",               _bool),
    ("gym",                   "gym",                   _bool),
    ("laundry",               "laundry",               _bool),
    ("housekeeping",          "housekeeping",          _bool),
    ("wifi",                  "wifi",                  _bool),
    ("cctv",                  "cctv",                  _bool),

    # ── Owner Contact ─────────────────────────────────────────
    ("owner_name",            "owner_name",            _str),
    ("contact_number",        "contact_number",        _str),
    ("email",                 "email",                 _str),
    ("alternate_contact",     "alternate_contact",     _str),

    # ── Uploaded By ───────────────────────────────────────────
    ("uploaded_by_name",      "uploaded_by_name",      _str),
    ("uploaded_by_email",     "uploaded_by_email",     _str),
    ("uploaded_by_contact",   "uploaded_by_contact",   _str),
]

# Required fields (model will raise IntegrityError without these)
REQUIRED_FIELDS = {
    "city":           "",
    "locality":       "",
    "pg_name":        "Unnamed PG",
    "property_address": "",
    "total_beds":     1,
    "pg_for":         "co-living",
    "furnishing_type":"unfurnished",
    "room_type":      "single",
    "room_total_beds":1,
    "rent":           0,
    "security_deposit":0,
    "minimum_stay":   1,
    "available_from": date.today,   # callable → evaluated per row
    "owner_name":     "",
    "contact_number": "",
    "email":          "",
}


# ─────────────────────────────────────────────────────────────
#  IMPORT VIEW
# ─────────────────────────────────────────────────────────────

@csrf_exempt
@require_POST
def import_pg_excel(request):
    """
    POST  /Admin_App/pg/import-excel/
    Expects: multipart/form-data with key 'file' (.xlsx)
    Returns: JSON { status, imported, skipped, errors[] }
    """
    session_id = request.session.get('Admin_id')
    if not session_id:
        return JsonResponse({'status': 'error', 'message': 'Unauthorized'}, status=401)

    uploaded = request.FILES.get('file')
    if not uploaded:
        return JsonResponse({'status': 'error', 'message': 'No file uploaded.'}, status=400)

    if not uploaded.name.endswith('.xlsx'):
        return JsonResponse({'status': 'error', 'message': 'Only .xlsx files are accepted.'}, status=400)

    try:
        wb = openpyxl.load_workbook(io.BytesIO(uploaded.read()), data_only=True)
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': f'Could not read Excel file: {e}'}, status=400)

    # Support both sheet names
    sheet_name = None
    for candidate in ("PG_CoLiving_Data", "Sheet1", wb.sheetnames[0]):
        if candidate in wb.sheetnames:
            sheet_name = candidate
            break
    ws = wb[sheet_name]

    # Find header row (row with 'city' in column A or B)
    header_row_idx = None
    col_index_map = {}  # field_name → col index (0-based)

    for row_idx, row in enumerate(ws.iter_rows(min_row=1, max_row=5, values_only=True), start=1):
        row_vals = [str(c).strip().lower() if c else "" for c in row]
        if "city" in row_vals:
            header_row_idx = row_idx
            for col_name, model_field, _ in COLUMN_MAP:
                try:
                    col_index_map[model_field] = row_vals.index(col_name.lower())
                except ValueError:
                    pass  # column not present — skip
            break

    if header_row_idx is None:
        return JsonResponse({
            'status': 'error',
            'message': "Could not find header row. Make sure row contains 'city' column."
        }, status=400)

    imported = 0
    skipped  = 0
    errors   = []

    for row_num, row in enumerate(
        ws.iter_rows(min_row=header_row_idx + 1, values_only=True),
        start=header_row_idx + 1
    ):
        # Skip completely empty rows
        if all(c is None or str(c).strip() == "" for c in row):
            continue

        kwargs = {}

        # Apply COLUMN_MAP
        for col_name, model_field, converter in COLUMN_MAP:
            if model_field not in col_index_map:
                continue
            raw = row[col_index_map[model_field]]
            try:
                kwargs[model_field] = converter(raw)
            except Exception:
                kwargs[model_field] = None

        # Apply defaults for required fields
        for field, default in REQUIRED_FIELDS.items():
            if not kwargs.get(field):
                kwargs[field] = default() if callable(default) else default

        # Skip row if pg_name and city are both empty
        if not kwargs.get("pg_name") and not kwargs.get("city"):
            skipped += 1
            continue

        try:
            PGColivingProperty.objects.create(**kwargs)
            imported += 1
        except Exception as e:
            skipped += 1
            errors.append(f"Row {row_num}: {str(e)[:120]}")

    return JsonResponse({
        'status':   'success',
        'imported': imported,
        'skipped':  skipped,
        'errors':   errors[:20],  # cap at 20 error messages
        'message':  f'{imported} PG/Co-living records imported, {skipped} skipped.'
    })


# ─────────────────────────────────────────────────────────────
#  DOWNLOAD TEMPLATE VIEW
# ─────────────────────────────────────────────────────────────

def download_pg_template(request):
    """
    GET  /Admin_App/pg/download-template/
    Serves the pre-built .xlsx template file.
    """
    session_id = request.session.get('Admin_id')
    if not session_id:
        from django.shortcuts import render
        return render(request, 'home_page/Adminlogin.html')

    # Template file location — place pg_coliving_import_template.xlsx
    # in your Django project root or adjust path below.
    template_path = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        'static', 'templates', 'pg_coliving_import_template.xlsx'
    )

    if os.path.exists(template_path):
        with open(template_path, 'rb') as f:
            response = HttpResponse(
                f.read(),
                content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
            )
            response['Content-Disposition'] = 'attachment; filename="pg_coliving_import_template.xlsx"'
            return response

    # Fallback: generate on the fly
    return _generate_template_response()


def _generate_template_response():
    """Generate a minimal template on the fly if static file not found."""
    import openpyxl
    from openpyxl.styles import PatternFill, Font, Alignment

    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "PG_CoLiving_Data"

    headers = [col[0] for col in COLUMN_MAP]
    for i, h in enumerate(headers, start=1):
        cell = ws.cell(row=1, column=i, value=h)
        cell.fill = PatternFill("solid", fgColor="7C3AED")
        cell.font = Font(bold=True, color="FFFFFF", size=9)
        cell.alignment = Alignment(horizontal="center")

    buf = io.BytesIO()
    wb.save(buf)
    buf.seek(0)

    response = HttpResponse(
        buf.read(),
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = 'attachment; filename="pg_coliving_import_template.xlsx"'
    return response






def _get_uploader(request):
    admin_id = request.session.get('Admin_id')
    user_id  = request.session.get('User_id')

    admin_obj = None
    user_obj  = None

    uploader_name    = ""
    uploader_email   = ""
    uploader_phone   = ""
    uploader_role    = ""

    if admin_id:
        try:
            admin_obj        = Admin_Login.objects.get(id=admin_id)
            uploader_name    = admin_obj.name      # ← fixed (was user_name)
            uploader_email   = admin_obj.email
            uploader_phone   = admin_obj.phone
            uploader_role    = admin_obj.role
        except Admin_Login.DoesNotExist:
            return None

    elif user_id:
        try:
            user_obj         = User_Details.objects.get(id=user_id)
            uploader_name    = user_obj.user_name
            uploader_email   = user_obj.user_email
            uploader_phone   = user_obj.user_phone
            uploader_role    = user_obj.user_role
        except User_Details.DoesNotExist:
            return None
    else:
        return None  # not logged in at all

    return {
        "admin_obj"      : admin_obj,
        "user_obj"       : user_obj,
        "uploader_name"  : uploader_name,
        "uploader_email" : uploader_email,
        "uploader_phone" : uploader_phone,
        "uploader_role"  : uploader_role,
    }



# ─────────────────────────────────────────────────────────
# ADD
# ─────────────────────────────────────────────────────────
def resale_residential_add(request):

    # ── Session check ──────────────────────────────────
    uploader = _get_uploader(request)
    if uploader is None:
        return redirect('login')

    # ── Handle POST ────────────────────────────────────
    if request.method == "POST":

        prop = ResaleResidentialProperty(

            # Basic Information
            title            = request.POST.get('title'),
            property_type    = request.POST.get('property_type'),
            zone             = request.POST.get('zone'),
            society_type     = request.POST.get('society_type'),
            water_type       = request.POST.get('water_type'),
            furnishing_type  = request.POST.get('furnishing_type'),
            age_of_property  = request.POST.get('age_of_property'),
            facing           = request.POST.get('facing'),
            available_from   = request.POST.get('available_from') or None,

            # Property Configuration
            bhk              = request.POST.get('bhk'),
            bathrooms        = request.POST.get('bathrooms') or 1,
            balconies        = request.POST.get('balconies') or 0,
            covered_parking  = request.POST.get('covered_parking') or 0,
            open_parking     = request.POST.get('open_parking') or 0,

            # Measurements
            builtup_area     = request.POST.get('builtup_area'),
            carpet_area      = request.POST.get('carpet_area'),
            plot_area        = request.POST.get('plot_area') or None,
            floor_no         = request.POST.get('floor_no'),
            total_floors     = request.POST.get('total_floors'),

            # Ownership & Legal
            ownership_type     = request.POST.get('ownership_type'),
            num_owners         = request.POST.get('num_owners'),
            has_loan           = request.POST.get('has_loan') == 'yes',
            loan_amount        = request.POST.get('loan_amount') or None,
            has_tenants        = request.POST.get('has_tenants') == 'yes',
            tenant_details     = request.POST.get('tenant_details') or None,
            has_legal_dispute  = request.POST.get('has_legal_dispute') == 'yes',
            dispute_details    = request.POST.get('dispute_details') or None,
            has_tax_due        = request.POST.get('has_tax_due') == 'yes',
            pending_tax_amount = request.POST.get('pending_tax_amount') or None,

            # Pricing
            expected_price       = request.POST.get('expected_price'),
            price_per_sqft       = request.POST.get('price_per_sqft') or None,
            is_negotiable        = request.POST.get('is_negotiable'),
            brokerage            = request.POST.get('brokerage') or None,
            brokerage_percentage = request.POST.get('brokerage_percentage') or None,
            manual_brokerage     = request.POST.get('manual_brokerage') or None,
            description          = request.POST.get('description'),

            # Amenities & Facilities (checkboxes → comma separated)
            nearby_facilities = ','.join(request.POST.getlist('nearby_facilities')),
            amenities         = ','.join(request.POST.getlist('amenities')),

            # Address
            city             = request.POST.get('city'),
            locality         = request.POST.get('locality'),
            building_name    = request.POST.get('building_name') or None,
            complete_address = request.POST.get('complete_address'),

            # Owner Contact
            owner_name         = request.POST.get('owner_name'),
            owner_contact      = request.POST.get('owner_contact'),
            owner_email        = request.POST.get('owner_email'),
            residential_status = request.POST.get('residential_status'),

            # Single file fields
            floor_plan     = request.FILES.get('floor_plan') or None,
            property_video = request.FILES.get('property_video') or None,

            # ── Auto-filled from session (shown in "Listing Uploaded By") ──
            uploaded_by_name    = uploader['uploader_name'],
            uploaded_by_email   = uploader['uploader_email'],
            uploaded_by_contact = uploader['uploader_phone'],
            uploaded_by_role    = uploader['uploader_role'],
        )

        prop.save()  # save property first so FK can reference it

        # ── Save multiple images into ResalePropertyImage ──
        images = request.FILES.getlist('property_images')
        for image in images:
            ResalePropertyImage.objects.create(
                property=prop,
                image=image
            )

        return JsonResponse({
            "status" : "success",
            "message": "Resale Residential Property Added Successfully"
        })

    # ── GET — render form with uploader info pre-filled ──
    # These 4 variables fill the readonly "Listing Uploaded By" section
    context = {
        "admin_obj"      : uploader['admin_obj'],
        "user_obj"       : uploader['user_obj'],

        "uploader_name"  : uploader['uploader_name'],   # → value="{{ uploader_name }}"
        "uploader_email" : uploader['uploader_email'],  # → value="{{ uploader_email }}"
        "uploader_phone" : uploader['uploader_phone'],  # → value="{{ uploader_phone }}"
        "uploader_role"  : uploader['uploader_role'],   # → value="{{ uploader_role }}"
    }
    return render(request, 'admin_user/Reports/Resale/residential_resale_list.html', context)


# ─────────────────────────────────────────────────────────
# LIST
# ─────────────────────────────────────────────────────────


# ─────────────────────────────────────────────────────────
# VIEW DETAIL
# ─────────────────────────────────────────────────────────
def resale_residential_view(request, pk):

    uploader = _get_uploader(request)
    if uploader is None:
        return redirect('login')

    prop   = get_object_or_404(ResaleResidentialProperty, pk=pk)
    images = prop.images.all()  # all images for this property

    context = {
        "admin_obj": uploader['admin_obj'],
        "user_obj" : uploader['user_obj'],
        "prop"     : prop,
        "images"   : images,  # all images shown in detail page
    }
    return render(request, 'admin_user/resale_residential_detail.html', context)


# ─────────────────────────────────────────────────────────
# DELETE
# ─────────────────────────────────────────────────────────
def resale_residential_delete(request, pk):

    uploader = _get_uploader(request)
    if uploader is None:
        return redirect('login')

    prop = get_object_or_404(ResaleResidentialProperty, pk=pk)
    prop.delete()  # CASCADE automatically deletes all ResalePropertyImage rows too

    return JsonResponse({
        "status" : "success",
        "message": "Property deleted successfully"
    })
    
    
    
    
    



# ─────────────────────────────────────────────────────────
# LIST VIEW
# ─────────────────────────────────────────────────────────


# ─────────────────────────────────────────────────────────
# IMPORT EXCEL VIEW
# ─────────────────────────────────────────────────────────
def resale_residential_import_excel(request):

    session_id = request.session.get('Admin_id')
    if not session_id:
        return JsonResponse({'status': 'error', 'message': 'Not logged in'})

    if request.method != 'POST':
        return JsonResponse({'status': 'error', 'message': 'Invalid request'})

    excel_file = request.FILES.get('excel_file')
    if not excel_file:
        return JsonResponse({'status': 'error', 'message': 'No file uploaded'})

    if not excel_file.name.endswith('.xlsx'):
        return JsonResponse({'status': 'error', 'message': 'Only .xlsx files allowed'})

    try:
        wb = openpyxl.load_workbook(excel_file)
        ws = wb.active

        imported = 0
        skipped  = 0

        # Skip header row (row 1), start from row 2
        for row in ws.iter_rows(min_row=2, values_only=True):

            # Skip completely empty rows
            if not any(row):
                continue

            try:
                # Map columns to fields (must match sample Excel order)
                (
                    title, property_type, zone, society_type, water_type,
                    furnishing_type, age_of_property, facing, available_from,
                    bhk, bathrooms, balconies, covered_parking, open_parking,
                    builtup_area, carpet_area, plot_area, floor_no, total_floors,
                    ownership_type, num_owners,
                    expected_price, is_negotiable, description,
                    city, locality, building_name, complete_address,
                    owner_name, owner_contact, owner_email, residential_status
                ) = row[:32]

                # Required field check
                if not title or not city or not expected_price:
                    skipped += 1
                    continue

                ResaleResidentialProperty.objects.create(
                    title            = str(title).strip(),
                    property_type    = str(property_type).strip().lower() if property_type else '',
                    zone             = str(zone).strip().lower() if zone else '',
                    society_type     = str(society_type).strip().lower() if society_type else '',
                    water_type       = str(water_type).strip().lower() if water_type else '',
                    furnishing_type  = str(furnishing_type).strip().lower() if furnishing_type else '',
                    age_of_property  = str(age_of_property).strip() if age_of_property else '',
                    facing           = str(facing).strip() if facing else '',
                    available_from   = available_from if available_from else None,
                    bhk              = str(bhk).strip().lower() if bhk else '',
                    bathrooms        = int(bathrooms) if bathrooms else 1,
                    balconies        = int(balconies) if balconies else 0,
                    covered_parking  = int(covered_parking) if covered_parking else 0,
                    open_parking     = int(open_parking) if open_parking else 0,
                    builtup_area     = float(builtup_area) if builtup_area else 0,
                    carpet_area      = float(carpet_area) if carpet_area else 0,
                    plot_area        = float(plot_area) if plot_area else None,
                    floor_no         = int(floor_no) if floor_no else 0,
                    total_floors     = int(total_floors) if total_floors else 0,
                    ownership_type   = str(ownership_type).strip().lower() if ownership_type else '',
                    num_owners       = str(num_owners).strip() if num_owners else '1',
                    expected_price   = float(expected_price) if expected_price else 0,
                    is_negotiable    = str(is_negotiable).strip().lower() if is_negotiable else 'yes',
                    description      = str(description).strip() if description else '',
                    city             = str(city).strip(),
                    locality         = str(locality).strip() if locality else '',
                    building_name    = str(building_name).strip() if building_name else None,
                    complete_address = str(complete_address).strip() if complete_address else '',
                    owner_name       = str(owner_name).strip() if owner_name else '',
                    owner_contact    = str(owner_contact).strip() if owner_contact else '',
                    owner_email      = str(owner_email).strip() if owner_email else '',
                    residential_status = str(residential_status).strip().lower() if residential_status else 'resident',

                    # Auto-fill uploader from session
                    uploaded_by_name    = request.session.get('admin_name', ''),
                    uploaded_by_role    = 'admin',
                )
                imported += 1

            except Exception:
                skipped += 1
                continue

        return JsonResponse({
            'status'  : 'success',
            'imported': imported,
            'skipped' : skipped,
        })

    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)})


# ─────────────────────────────────────────────────────────
# DOWNLOAD SAMPLE EXCEL
# ─────────────────────────────────────────────────────────
def resale_residential_sample_excel(request):

    session_id = request.session.get('Admin_id')
    if not session_id:
        return redirect('login')

    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Resale Residential Sample"

    # Header row — must match import order exactly
    headers = [
        'title', 'property_type', 'zone', 'society_type', 'water_type',
        'furnishing_type', 'age_of_property', 'facing', 'available_from',
        'bhk', 'bathrooms', 'balconies', 'covered_parking', 'open_parking',
        'builtup_area', 'carpet_area', 'plot_area', 'floor_no', 'total_floors',
        'ownership_type', 'num_owners',
        'expected_price', 'is_negotiable', 'description',
        'city', 'locality', 'building_name', 'complete_address',
        'owner_name', 'owner_contact', 'owner_email', 'residential_status',
    ]
    ws.append(headers)

    # One sample data row
    sample = [
        '3BHK Apartment in Prime Location', 'apartment', 'north', 'gated', 'municipal',
        'semi', '1-3', 'North-East', '2026-06-01',
        '3bhk', 2, 1, 1, 0,
        1200, 950, None, 3, 10,
        'freehold', '1',
        5000000, 'yes', 'Beautiful apartment near schools and hospitals',
        'Nagpur', 'Dharampeth', 'Sunshine Society', '123, Dharampeth, Nagpur - 440010',
        'Rahul Sharma', '9876543210', 'rahul@example.com', 'resident',
    ]
    ws.append(sample)

    # Style header row
    from openpyxl.styles import Font, PatternFill
    for cell in ws[1]:
        cell.font = Font(bold=True, color="FFFFFF")
        cell.fill = PatternFill("solid", fgColor="667EEA")

    # Auto column width
    for col in ws.columns:
        max_len = max(len(str(cell.value)) if cell.value else 0 for cell in col)
        ws.column_dimensions[col[0].column_letter].width = max_len + 4

    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = 'attachment; filename="resale_residential_sample.xlsx"'
    wb.save(response)
    return response






 ####################Start  Views Section For Commercial Resale Property #######################################


def _get_uploader(request):
    admin_id = request.session.get('Admin_id')
    user_id  = request.session.get('User_id')

    admin_obj = None
    user_obj  = None

    uploader_name    = ""
    uploader_email   = ""
    uploader_phone   = ""
    uploader_role    = ""

    if admin_id:
        try:
            admin_obj        = Admin_Login.objects.get(id=admin_id)
            uploader_name    = admin_obj.name
            uploader_email   = admin_obj.email
            uploader_phone   = admin_obj.phone
            uploader_role    = admin_obj.role
        except Admin_Login.DoesNotExist:
            return None

    elif user_id:
        try:
            user_obj         = User_Details.objects.get(id=user_id)
            uploader_name    = user_obj.user_name
            uploader_email   = user_obj.user_email
            uploader_phone   = user_obj.user_phone
            uploader_role    = user_obj.user_role
        except User_Details.DoesNotExist:
            return None
    else:
        return None  # not logged in at all

    return {
        "admin_obj"      : admin_obj,
        "user_obj"       : user_obj,
        "uploader_name"  : uploader_name,
        "uploader_email" : uploader_email,
        "uploader_phone" : uploader_phone,
        "uploader_role"  : uploader_role,
    }


# ─────────────────────────────────────────────────────────
# ADD COMMERCIAL PROPERTY
# ─────────────────────────────────────────────────────────
def add_commercial_property(request):

    # ── Step 1: Session check — who is logged in? ──────
    uploader = _get_uploader(request)
    if uploader is None:
        return redirect('login')   # not logged in → redirect to login

    # ── Step 2: Handle POST (form submission) ──────────
    if request.method == "POST":

        prop = CommercialResaleProperty(

            # ── Basic Information ──────────────────────
            title               = request.POST.get('title'),
            property_type       = request.POST.get('property_type'),
            zone_type           = request.POST.get('zone_type'),
            location_hub        = request.POST.get('location_hub') or None,
            property_condition  = request.POST.get('property_condition'),
            ownership_type      = request.POST.get('ownership_type'),
            age_of_property     = request.POST.get('age_of_property'),
            available_from      = request.POST.get('available_from') or None,

            # ── Commercial Specifications ──────────────
            num_staircases      = request.POST.get('num_staircases') or None,
            passenger_lifts     = request.POST.get('passenger_lifts') or 0,
            service_lifts       = request.POST.get('service_lifts') or 0,
            num_cabins          = request.POST.get('num_cabins') or None,
            meeting_rooms       = request.POST.get('meeting_rooms') or None,
            min_seats           = request.POST.get('min_seats') or None,
            max_seats           = request.POST.get('max_seats') or None,
            private_parking     = request.POST.get('private_parking') or 0,
            public_parking      = request.POST.get('public_parking') or None,

            # ── Area & Pricing ─────────────────────────
            builtup_area        = request.POST.get('builtup_area'),
            carpet_area         = request.POST.get('carpet_area') or None,
            plot_area           = request.POST.get('plot_area') or None,
            brokerage           = request.POST.get('brokerage') or None,
            brokerage_percentage = request.POST.get('brokerage_percentage') or None,
            manual_brokerage    = request.POST.get('manual_brokerage') or None,
            expected_price      = request.POST.get('expected_price'),

            # ── Ownership & Legal ──────────────────────
            num_owners          = request.POST.get('num_owners'),
            loan_on_property    = request.POST.get('loan_on_property'),
            loan_amount         = request.POST.get('loan_amount') or None,
            existing_tenants    = request.POST.get('existing_tenants'),
            tenant_details      = request.POST.get('tenant_details') or None,
            legal_dispute       = request.POST.get('legal_dispute'),
            dispute_details     = request.POST.get('dispute_details') or None,
            tax_due             = request.POST.get('tax_due'),
            pending_tax_amount  = request.POST.get('pending_tax_amount') or None,
            fire_noc            = request.POST.get('fire_noc') or None,
            property_description = request.POST.get('property_description'),
            sanctioning_authority = request.POST.get('sanctioning_authority'),

            # ── Media ──────────────────────────────────
            floor_plan          = request.FILES.get('floor_plan') or None,
            property_video      = request.FILES.get('property_video') or None,

            # ── Amenities & Facilities (checkboxes) ────
            nearby_facilities   = ','.join(request.POST.getlist('nearby_facilities')),
            amenities           = ','.join(request.POST.getlist('amenities')),

            # ── Address ────────────────────────────────
            city                = request.POST.get('city'),
            locality            = request.POST.get('locality'),
            building_name       = request.POST.get('building_name') or None,
            property_address    = request.POST.get('property_address'),

            # ── Owner Contact ──────────────────────────
            owner_name          = request.POST.get('owner_name'),
            owner_contact       = request.POST.get('owner_contact'),
            owner_email         = request.POST.get('owner_email'),
            residential_status  = request.POST.get('residential_status'),

            # ── Listing Uploaded By (from session) ─────
            # These come from the readonly fields in the form
            # which are pre-filled from session via context below
            uploaded_by_name    = uploader['uploader_name'],
            uploaded_by_email   = uploader['uploader_email'],
            uploaded_by_contact = uploader['uploader_phone'],
            uploaded_by_role    = uploader['uploader_role'],
        )

        prop.save()  # save first so FK for images works

        # ── Save multiple property images ───────────────
        images = request.FILES.getlist('property_images')
        for image in images[:10]:    # max 10 images
            CommercialPropertyImage.objects.create(
                property=prop,
                image=image
            )

        return JsonResponse({
            "status" : "success",
            "message": "Commercial Property Added Successfully"
        })

    # ── Step 3: GET — render form with uploader pre-filled ──
    # uploader_name / uploader_email / uploader_phone / uploader_role
    # are passed to the template so the readonly "Listing Uploaded By"
    # section shows the correct logged-in Admin OR User data
    context = {
        "admin_obj"      : uploader['admin_obj'],   # None if user is logged in
        "user_obj"       : uploader['user_obj'],     # None if admin is logged in

        # These 4 fill the readonly inputs in the template:
        # value="{{ uploader_name }}"   → Admin: admin_obj.name   | User: user_obj.user_name
        # value="{{ uploader_email }}"  → Admin: admin_obj.email  | User: user_obj.user_email
        # value="{{ uploader_phone }}"  → Admin: admin_obj.phone  | User: user_obj.user_phone
        # value="{{ uploader_role }}"   → Admin: admin_obj.role   | User: user_obj.user_role
        "uploader_name"  : uploader['uploader_name'],
        "uploader_email" : uploader['uploader_email'],
        "uploader_phone" : uploader['uploader_phone'],
        "uploader_role"  : uploader['uploader_role'],
    }
    return render(request, 'admin_user/Reports/Resale/commercial_list.html', context)







# =====================================================
# views.py — Commercial List + Import Excel + Toggle + Delete
# =====================================================


from django.db.models import Avg, Count








import json
import openpyxl
from datetime import datetime
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Avg, Count
from .models import CommercialResaleProperty


# ── DEBUG TEST VIEW ──────────────────────────────────────────
# Visit /commercial/import/test/ to test plain form submit
def import_test_view(request):
    result = ''
    if request.method == 'POST':
        f = request.FILES.get('commercial_excel_file')
        if f:
            result = f'File received: {f.name}, size: {f.size} bytes'
        else:
            result = 'ERROR: No file in request.FILES — field name mismatch or form issue'
    return HttpResponse(f'''
        <h2>Import Debug Test</h2>
        <p style="color:green;font-size:18px;">{result}</p>
        <hr>
        <h3>Plain Form Test</h3>
        <form method="POST" enctype="multipart/form-data">
            <input type="hidden" name="csrfmiddlewaretoken" value="get-from-cookie">
            <input type="file" name="commercial_excel_file" accept=".xlsx">
            <button type="submit">Submit</button>
        </form>
    ''')


# ── IMPORT EXCEL ─────────────────────────────────────────────
@csrf_exempt
def import_commercial_data(request):

    print("=" * 60)
    print("import_commercial_data called")
    print("Method:", request.method)
    print("FILES:", request.FILES)
    print("POST keys:", list(request.POST.keys()))
    print("=" * 60)

    if request.method != 'POST':
        return JsonResponse({'status': '0', 'msg': 'Invalid request method. Must be POST.'})

    uploader   = _get_uploader(request)
    excel_file = request.FILES.get('commercial_excel_file')

    if not excel_file:
        print("ERROR: No file found in request.FILES")
        print("Available FILES keys:", list(request.FILES.keys()))
        return JsonResponse({
            'status': '0',
            'msg': f'No file received. Keys in FILES: {list(request.FILES.keys())}. Expected key: commercial_excel_file'
        })

    print(f"File received: {excel_file.name}, size: {excel_file.size}")

    # ── Helper functions ─────────────────────────────────
    def val(v, default=''):
        if v is None or str(v).strip() == '':
            return default
        return str(v).strip()

    def num(v, default=None):
        if v is None or str(v).strip() == '':
            return default
        try:
            return float(v)
        except (ValueError, TypeError):
            return default

    def pos_int(v, default=0):
        if v is None or str(v).strip() == '':
            return default
        try:
            return int(float(str(v)))
        except (ValueError, TypeError):
            return default

    def yn(v):
        if v is None:
            return 'no'
        return 'yes' if str(v).strip().lower() in ('yes', 'y', '1', 'true') else 'no'

    def parse_date(v):
        if v is None or str(v).strip() == '':
            return None
        try:
            if hasattr(v, 'date'):
                return v.date()
            return datetime.strptime(str(v).strip(), '%Y-%m-%d').date()
        except Exception:
            return None

    # ── Read Excel ───────────────────────────────────────
    try:
        wb   = openpyxl.load_workbook(excel_file, data_only=True)
        ws   = wb.active
        rows = list(ws.iter_rows(values_only=True))
        print(f"Excel read OK. Total rows (including header): {len(rows)}")
    except Exception as e:
        print(f"Excel read ERROR: {e}")
        return JsonResponse({'status': '0', 'msg': f'Cannot read Excel file: {str(e)}'})

    if len(rows) < 2:
        return JsonResponse({'status': '0', 'msg': 'Excel file has no data. Row 1 = header, Row 2+ = data.'})

    count  = 0
    errors = []

    for i, row in enumerate(rows[1:], start=2):

        # pad to 46
        row = list(row) + [None] * 50
        row = row[:46]

        # skip blank rows
        if all(c is None or str(c).strip() == '' for c in row):
            continue

        if not row[0] or not row[23]:
            errors.append(f'Row {i}: Skipped — title (col A) or expected_price (col X) empty.')
            continue

        try:
            CommercialResaleProperty.objects.create(
                title                 = val(row[0]),
                property_type         = val(row[1],  'office').lower(),
                zone_type             = val(row[2],  'commercial').lower(),
                location_hub          = val(row[3])  or None,
                property_condition    = val(row[4],  'good').lower(),
                ownership_type        = val(row[5],  'freehold').lower(),
                age_of_property       = val(row[6],  '0-1'),
                available_from        = parse_date(row[7]),
                num_staircases        = pos_int(row[8]),
                passenger_lifts       = pos_int(row[9]),
                service_lifts         = pos_int(row[10]),
                num_cabins            = pos_int(row[11]),
                meeting_rooms         = pos_int(row[12]),
                min_seats             = pos_int(row[13]) or None,
                max_seats             = pos_int(row[14]) or None,
                private_parking       = pos_int(row[15]),
                public_parking        = pos_int(row[16]) or None,
                builtup_area          = num(row[17], 0),
                carpet_area           = num(row[18]) or None,
                plot_area             = num(row[19]) or None,
                brokerage             = val(row[20]) or None,
                brokerage_percentage  = val(row[21]) or None,
                manual_brokerage      = val(row[22]) or None,
                expected_price        = num(row[23], 0),
                num_owners            = val(row[24], '1'),
                loan_on_property      = yn(row[25]),
                loan_amount           = num(row[26]) or None,
                existing_tenants      = yn(row[27]),
                tenant_details        = val(row[28]) or None,
                legal_dispute         = yn(row[29]),
                dispute_details       = val(row[30]) or None,
                tax_due               = yn(row[31]),
                pending_tax_amount    = num(row[32]) or None,
                fire_noc              = yn(row[33]),
                property_description  = val(row[34], val(row[0])),
                sanctioning_authority = val(row[35], 'N/A'),
                nearby_facilities     = val(row[36]) or None,
                amenities             = val(row[37]) or None,
                city                  = val(row[38]),
                locality              = val(row[39]),
                building_name         = val(row[40]) or None,
                property_address      = val(row[41]),
                owner_name            = val(row[42]),
                owner_contact         = val(row[43]),
                owner_email           = val(row[44]),
                residential_status    = val(row[45], 'resident').lower(),
                uploaded_by_name      = uploader['uploader_name']    if uploader else '',
                uploaded_by_email     = uploader['uploader_email']   if uploader else '',
                uploaded_by_contact   = uploader['uploader_phone']   if uploader else '',
                uploaded_by_role      = uploader['uploader_role']    if uploader else '',
                is_active             = True,
            )
            count += 1
            print(f"Row {i}: Saved OK — {val(row[0])}")

        except Exception as row_err:
            print(f"Row {i} ERROR: {row_err}")
            errors.append(f'Row {i}: {str(row_err)}')

    print(f"Import done. Saved: {count}, Errors: {len(errors)}")

    if count == 0 and errors:
        return JsonResponse({
            'status': '0',
            'msg': f'0 imported. First error: {errors[0]}'
        })

    msg = f'{count} properties imported successfully.'
    if errors:
        msg += f' ({len(errors)} row(s) skipped.)'

    return JsonResponse({'status': '1', 'msg': msg})


# ── LIST VIEW ────────────────────────────────────────────────



# ── TOGGLE ───────────────────────────────────────────────────
@csrf_exempt
def toggle_commercial_property(request):
    if request.method == 'POST':
        prop_id = request.POST.get('prop_id')
        try:
            prop = CommercialResaleProperty.objects.get(id=prop_id)
            prop.is_active = not prop.is_active
            prop.save()
            status = 'Active' if prop.is_active else 'Inactive'
            return JsonResponse({'status': '1', 'msg': f'Property marked as {status}.'})
        except CommercialResaleProperty.DoesNotExist:
            return JsonResponse({'status': '0', 'msg': 'Property not found.'})
    return JsonResponse({'status': '0', 'msg': 'Invalid request.'})


# ── DELETE ───────────────────────────────────────────────────
@csrf_exempt
def delete_commercial_property(request):
    if request.method == 'POST':
        prop_id = request.POST.get('prop_id')
        try:
            prop = CommercialResaleProperty.objects.get(id=prop_id)
            prop.delete()
            return JsonResponse({'status': '1', 'msg': 'Property deleted successfully.'})
        except CommercialResaleProperty.DoesNotExist:
            return JsonResponse({'status': '0', 'msg': 'Property not found.'})
    return JsonResponse({'status': '0', 'msg': 'Invalid request.'})


# ── DOWNLOAD SAMPLE EXCEL ────────────────────────────────────
def download_commercial_sample_excel(request):
    from openpyxl.styles import Font, PatternFill, Alignment
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = 'Commercial Properties'
    headers = [
        'title','property_type','zone_type','location_hub','property_condition',
        'ownership_type','age_of_property','available_from','num_staircases',
        'passenger_lifts','service_lifts','num_cabins','meeting_rooms','min_seats',
        'max_seats','private_parking','public_parking','builtup_area','carpet_area',
        'plot_area','brokerage','brokerage_percentage','manual_brokerage','expected_price',
        'num_owners','loan_on_property','loan_amount','existing_tenants','tenant_details',
        'legal_dispute','dispute_details','tax_due','pending_tax_amount','fire_noc',
        'property_description','sanctioning_authority','nearby_facilities','amenities',
        'city','locality','building_name','property_address',
        'owner_name','owner_contact','owner_email','residential_status',
    ]
    ws.append(headers)
    for cell in ws[1]:
        cell.font = Font(bold=True, color='FFFFFF')
        cell.fill = PatternFill(fill_type='solid', fgColor='667EEA')
    ws.append([
        'Prime Office Space BKC','office','commercial','business','excellent',
        'freehold','3-5','2025-06-01',2,3,1,10,2,20,50,5,20,
        2500,2000,3000,'Yes','2%','',15000000,
        '1','no','','no','','no','','no','','yes',
        'Prime office space in BKC with modern interiors.',
        'MCGM - Municipal Corporation of Greater Mumbai',
        'metro,bus,banks','parking,security,ac,cctv',
        'Mumbai','BKC','Platina Business Park',
        'Plot C-59, G Block, BKC, Mumbai - 400051',
        'Rajesh Sharma','9876543210','rajesh@example.com','resident',
    ])
    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = 'attachment; filename=commercial_sample.xlsx'
    wb.save(response)
    return response

# ─────────────────────────────────────────────────────────





 ####################End Views Section For Commercial Resale Property #######################################