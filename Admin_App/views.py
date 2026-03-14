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
        context = {'admin_obj':admin_obj}
        return render(request,"admin_user/residential.html",context)
    else:
        return render(request,'home_page/Adminlogin.html')


def commercial(request):
    session_id = request.session.get('Admin_id')
    if session_id:
        admin_obj = Admin_Login.objects.get(id=session_id)
        context = {'admin_obj':admin_obj}
        return render(request,"admin_user/commercial.html",context)
    else:
        return render(request,'home_page/Adminlogin.html')


def pg_coliving(request):
    session_id = request.session.get('Admin_id')
    if session_id:
        admin_obj = Admin_Login.objects.get(id=session_id)
        context = {'admin_obj':admin_obj}
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
        context = {'admin_obj':admin_obj}
        return render(request,"admin_user/Resale/residential_resale.html",context)
    else:
        return render(request,'home_page/Adminlogin.html')
    

def commercial_resale(request):
    session_id = request.session.get('Admin_id')
    if session_id:
        admin_obj = Admin_Login.objects.get(id=session_id)
        context = {'admin_obj':admin_obj}
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

def residential_resale_list(request):
    session_id = request.session.get('Admin_id')
    if session_id:
        admin_obj = Admin_Login.objects.get(id=session_id)
        context = {'admin_obj':admin_obj}
        return render(request,'admin_user/Reports/Resale/residential_list.html',context)
    else:
        return render(request,'home_page/Adminlogin.html')

############ Views end for resale residential list #######################


########### Views start for resale commercial property list ######################

def commercial_resale_list(request):
    session_id = request.session.get('Admin_id')
    if session_id:
        admin_obj = Admin_Login.objects.get(id=session_id)
        context = {'admin_obj':admin_obj}
        return render(request,'admin_user/Reports/Resale/commercial_list.html',context)
    else:
        return render(request,'home_page/Adminlogin.html')

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



from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.db.models import Q
from django.core.paginator import Paginator  # ← ADD THIS
import csv

def rental_list(request):

    session_id = request.session.get('Admin_id')
    if not session_id:
        return render(request, 'home_page/Adminlogin.html')

    admin_obj = Admin_Login.objects.get(id=session_id)
    search_query = request.GET.get('search', '').strip()

    try:
        properties = RentalResidentialProperty.objects.all().order_by('-id')
        print("✅ STEP 1 - properties count:", properties.count())
    except Exception as e:
        print("❌ STEP 1 FAILED:", e)
        properties = RentalResidentialProperty.objects.none()

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
            print("✅ STEP 2 - search filter ok:", properties.count())
        except Exception as e:
            print("❌ STEP 2 FAILED:", e)
            properties = RentalResidentialProperty.objects.none()

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

    try:
        paginator = Paginator(properties, 10)
        page_number = request.GET.get('page', 1)
        page_obj = paginator.get_page(page_number)
        print("✅ STEP 3 - page_obj count:", page_obj.object_list.count())
    except Exception as e:
        print("❌ STEP 3 FAILED:", e)
        page_obj = Paginator(RentalResidentialProperty.objects.none(), 10).get_page(1)

    total_count = properties.count()
    print("✅ STEP 4 - total_count:", total_count)
    print("✅ STEP 5 - rendering template with page_obj:", page_obj)

    context = {
        'admin_obj': admin_obj,
        'page_obj': page_obj,
        'search_query': search_query,
        'total_count': total_count,
    }

    print("✅ STEP 6 - context keys:", list(context.keys()))
    print("✅ STEP 7 - page_obj in context:", context['page_obj'])

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

def _str(val):
    if val is None:
        return None
    s = str(val).strip()
    return s if s else None


def _int(val):
    try:
        return int(val)
    except (TypeError, ValueError):
        return None


def _decimal(val):
    try:
        from decimal import Decimal
        return Decimal(str(val).strip())
    except Exception:
        return None


def _bigint(val):
    try:
        return int(float(str(val).strip()))
    except (TypeError, ValueError):
        return None


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
#  Column → model field mapping
#  Order must match the Excel template columns
# ─────────────────────────────────────────────

COLUMN_MAP = [
    # (excel_col_name,          model_field,            converter)
    ("property_title",          "property_title",       _str),
    ("property_purpose",        "property_purpose",     _str),
    ("property_type",           "property_type",        _str),
    ("bhk_type",                "bhk_type",             _str),
    ("renting_option",          "renting_option",       _str),
    ("furnishing_status",       "furnishing_status",    _str),
    ("available_for",           "available_for",        _str),
    ("built_up_area",           "built_up_area",        _decimal),
    ("bathrooms",               "bathrooms",            _int),
    ("balconies",               "balconies",            _int),
    ("floor_number",            "floor_number",         _str),
    ("total_floors",            "total_floors",         _int),
    ("facing",                  "facing",               _str),
    ("zone",                    "zone",                 _str),
    ("ownership_type",          "ownership_type",       _str),
    ("construction_status",     "construction_status",  _str),
    ("property_age",            "property_age",         _str),
    ("carpet_area",             "carpet_area",          _decimal),
    ("plot_area",               "plot_area",            _decimal),
    ("building_name",           "building_name",        _str),
    ("possession_status",       "possession_status",    _str),
    ("available_from",          "available_from",       _date),
    ("lease_duration",          "lease_duration",       _str),
    ("brokerage",               "brokerage",            _str),
    ("brokerage_percentage",    "brokerage_percentage", _str),
    ("manual_brokerage",        "manual_brokerage",     _str),
    ("monthly_rent",            "monthly_rent",         _bigint),
    ("security_deposit",        "security_deposit",     _bigint),
    ("maintenance_type",        "maintenance_type",     _str),
    ("maintenance_amount",      "maintenance_amount",   _bigint),
    ("expected_price",          "expected_price",       _bigint),
    ("address",                 "address",              _str),
    ("city",                    "city",                 _str),
    ("locality",                "locality",             _str),
    ("state",                   "state",                _str),
    ("pincode",                 "pincode",              _str),
    ("road_connectivity",       "road_connectivity",    _str),
    ("amenities",               "amenities",            _str),
    ("description",             "description",          _str),
    ("rent_residential_desc",   "rent_residential_desc",_str),
    ("owner_name",              "owner_name",           _str),
    ("contact_number",          "contact_number",       _str),
    ("email",                   "email",                _str),
    ("alternate_contact",       "alternate_contact",    _str),
    ("uploaded_by_name",        "uploaded_by_name",     _str),
    ("uploaded_by_email",       "uploaded_by_email",    _str),
    ("uploaded_by_contact",     "uploaded_by_contact",  _str),
    ("uploaded_by_role",        "uploaded_by_role",     _str),
]


# ─────────────────────────────────────────────
#  Main import view
# ─────────────────────────────────────────────

@require_POST
def import_residential_excel(request):
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

    # Build header → column-index map from row 1
    headers = {}
    for col_idx, cell in enumerate(next(ws.iter_rows(min_row=1, max_row=1)), 1):
        if cell.value:
            headers[str(cell.value).strip()] = col_idx

    # Validate that required columns exist
    missing = [cm[0] for cm in COLUMN_MAP if cm[0] not in headers]
    if missing:
        return JsonResponse({
            "status": "error",
            "message": f"Missing columns in Excel: {', '.join(missing[:10])}{'...' if len(missing) > 10 else ''}"
        }, status=400)

    created_count = 0
    error_rows = []

    for row_idx, row in enumerate(ws.iter_rows(min_row=2, values_only=True), start=2):
        # Skip completely empty rows
        if all(v is None or str(v).strip() == "" for v in row):
            continue

        obj_fields = {}
        row_error = None

        for excel_col, model_field, converter in COLUMN_MAP:
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

        try:
            RentalResidentialProperty.objects.create(**obj_fields)
            created_count += 1
        except Exception as e:
            error_rows.append(f"Row {row_idx}: DB error — {e}")

    wb.close()

    response_data = {
        "status": "success",
        "message": f"Import complete. {created_count} record(s) imported successfully.",
        "created": created_count,
        "errors": error_rows,
        "error_count": len(error_rows),
    }

    if error_rows:
        response_data["message"] += f" {len(error_rows)} row(s) had errors (see 'errors' list)."

    return JsonResponse(response_data)


# ─────────────────────────────────────────────
#  Download blank template view
# ─────────────────────────────────────────────

def download_residential_template(request):
    """
    Serves the blank Excel template for users to fill in.
    Place the template file at: your_app/static/templates/rental_residential_import_template.xlsx
    OR generate it on-the-fly (code below generates it dynamically).
    """
    from openpyxl import Workbook
    from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
    from openpyxl.utils import get_column_letter

    wb = Workbook()
    ws = wb.active
    ws.title = "Rental Residential"

    columns = [cm[0] for cm in COLUMN_MAP]

    header_fill = PatternFill("solid", start_color="4F46E5", end_color="4F46E5")
    header_font = Font(bold=True, color="FFFFFF", name="Arial", size=10)
    header_align = Alignment(horizontal="center", vertical="center", wrap_text=True)
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
        cell.alignment = header_align
        cell.border = thin_border
        ws.column_dimensions[get_column_letter(col_idx)].width = max(18, len(col_name) + 4)

    ws.row_dimensions[1].height = 35
    ws.freeze_panes = "A2"

    # Instructions sheet
    ws2 = wb.create_sheet("Instructions")
    ws2.column_dimensions["A"].width = 28
    ws2.column_dimensions["B"].width = 60
    ws2.column_dimensions["C"].width = 20

    notes = {
        "property_type": "Apartment / Independent House / Villa / Flat / Studio",
        "bhk_type": "1 BHK / 2 BHK / 3 BHK / 4 BHK / Studio",
        "furnishing_status": "Fully Furnished / Semi Furnished / Unfurnished",
        "available_for": "Family / Bachelor / Any",
        "facing": "North / South / East / West / North-East / South-West etc.",
        "property_purpose": "Rent / Lease",
        "brokerage": "Yes / No",
        "maintenance_type": "Monthly / Quarterly / Yearly / None",
        "available_from": "YYYY-MM-DD (e.g. 2025-04-01)",
        "built_up_area": "Numeric sq.ft",
        "monthly_rent": "Numeric INR (e.g. 15000)",
    }
    type_map = {
        "built_up_area": "Decimal", "carpet_area": "Decimal", "plot_area": "Decimal",
        "monthly_rent": "Integer", "security_deposit": "Integer",
        "maintenance_amount": "Integer", "expected_price": "Integer",
        "bathrooms": "Integer", "balconies": "Integer",
        "total_floors": "Integer", "available_from": "Date (YYYY-MM-DD)",
    }

    ws2.cell(row=1, column=1, value="Column Instructions").font = Font(bold=True, size=13, color="4F46E5")
    for ci, h in enumerate(["Column Name", "Valid Values / Notes", "Data Type"], 1):
        c = ws2.cell(row=2, column=ci, value=h)
        c.font = Font(bold=True, color="FFFFFF", name="Arial")
        c.fill = PatternFill("solid", start_color="4F46E5", end_color="4F46E5")

    for ri, col_name in enumerate(columns, 3):
        ws2.cell(row=ri, column=1, value=col_name).font = Font(bold=True, size=9)
        ws2.cell(row=ri, column=2, value=notes.get(col_name, "Free text"))
        ws2.cell(row=ri, column=3, value=type_map.get(col_name, "Text"))

    ws2.freeze_panes = "A3"

    buffer = io.BytesIO()
    wb.save(buffer)
    buffer.seek(0)

    response = HttpResponse(
        buffer.getvalue(),
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
    response["Content-Disposition"] = 'attachment; filename="rental_residential_import_template.xlsx"'
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