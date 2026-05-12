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
import csv
import json
from django.db.models import Count, Avg, Max, Min, Q
from django.core.paginator import Paginator
from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib import messages
from datetime import datetime

from django.shortcuts import render, redirect
from django.contrib import messages
from datetime import datetime
from datetime import datetime
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.views.decorators.http import require_POST

import csv
from datetime import datetime, date

import openpyxl
from django.contrib import messages
from django.http import HttpResponse, JsonResponse
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST
from openpyxl import Workbook
from django.db import transaction
import pandas as pd
import io
from django.urls import reverse,NoReverseMatch

from openpyxl.styles import Font, PatternFill
from datetime import timedelta

########### Crime Officer Views#######

def _float(val):
    try:
        return float(val) if val not in (None, '') else None
    except:
        return None
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


########## Views start for impersonation url for super admin ######################

@csrf_exempt
def Impersonate(request):
    if request.method == "POST" and request.session.get('user_type') == 'Admin':
        target_id = request.POST.get('target_user_id')

        
        
        if target_id:
            # 1. Save ID to session securely
            request.session['impersonate_id'] = target_id
            
            target_user = User_Details.objects.get(id=target_id)

            
            
            # 2. Determine the correct URL based on their role
            if target_user.user_role == 'Relationship Manager':
                url = reverse('rm_dashboard')
            elif target_user.user_role == 'Landlord':
                url = reverse('landlord_dashboard')
            elif target_user.user_role == 'Tenant':
                url = reverse('Tenant_App:tenant_Dashboard')
            elif target_user.user_role == 'Buyer':
                url = reverse('Buyer_Dashboard')
            elif target_user.user_role == 'Agent':
                url = reverse('agent_dashboard')
            elif target_user.user_role == 'Agency/Builder':
                url = reverse('Agency_Dashboard')
            elif target_user.user_role == 'Vendor':
                url = reverse('Vendors:vendors_Dashboard')            
            
            # 3. Send the URL back to the JavaScript
            return JsonResponse({'status': 'success', 'redirect_url': url})
            
    return JsonResponse({'status': 'error', 'msg': 'Unauthorized request'})

############ Views end for impersonation url for super admin ##########################


############ Views start for live statistical tracking #####################

def get_live_traffic(request):
    if request.session.get('user_type') != 'Admin':
        return JsonResponse({'error': 'Unauthorized'}, status=403)

    five_minutes_ago = now() - timedelta(minutes=5)
    
    # Clean up old users
    ActiveVisitor.objects.filter(last_seen__lt=five_minutes_ago).delete()

    # Count active users from SQL
    return JsonResponse({
        'desktop': ActiveVisitor.objects.filter(device_type='desktop').count(),
        'mobile': ActiveVisitor.objects.filter(device_type='mobile').count(),
        'tablet': ActiveVisitor.objects.filter(device_type='tablet').count()
    })

############# Production Version ##############################

# from django.core.cache import cache

# def get_live_traffic(request):
#     if request.session.get('user_type') != 'Admin':
#         return JsonResponse({'error': 'Unauthorized'}, status=403)

#     # Ask Redis for all active user keys
#     active_keys = cache.keys("active_user_*")
    
#     desktop_count, mobile_count, tablet_count = 0, 0, 0

#     # Tally them up from RAM
#     for key in active_keys:
#         device = cache.get(key)
#         if device == 'desktop': desktop_count += 1
#         elif device == 'mobile': mobile_count += 1
#         elif device == 'tablet': tablet_count += 1

#     return JsonResponse({
#         'desktop': desktop_count,
#         'mobile': mobile_count,
#         'tablet': tablet_count
#     })

############ Views end for live statistical tracking #############################


############# Views start for global search ########################

def global_search(request):
    query = request.GET.get('q', '')
    results_list = []

    if len(query) >= 2:
        
        property_tables = [
            {'model': RentalResidentialProperty, 'label': 'Residential (Rent)', 'url_name': 'residential_detail'},
            {'model': CommercialRentalProperty, 'label': 'Commercial (Rent)', 'url_name': 'commercial_detail'},
            # {'model': PGColivingProperty, 'label': 'PG / Co-living', 'url_name': 'pg_detail'},
            {'model': ResaleResidentialProperty, 'label': 'Residential (Resale)', 'url_name': 'residential_resale_detail'},
            {'model': ResaleResidentialProperty, 'label': 'Commercial (Resale)', 'url_name': 'commercial_resale_detail'},
            {'model': PlotSaleProperty, 'label': 'Plot / Land', 'url_name': 'plot_detail'},
            {'model': IndustrialResaleProperty, 'label': 'Industrial', 'url_name': 'industrial_detail'},
            {'model': AgriculturalResaleProperty, 'label': 'Agricultural', 'url_name': 'agricultural_detail'},
        ]

        # 🟢 1. SEARCH PROPERTIES (By Title, Location, Price, City, Status, etc.)
        for table in property_tables:
            ModelClass = table['model']
            
            matches = ModelClass.objects.filter(            # Search by City       # Search by Rent/Price amount
                Q(uploaded_by_name=query) |          # Search by Status (e.g., "Active")
                Q(uploaded_by_email=query) |           # Search by Status (e.g., "Active")
                Q(uploaded_by_contact=query)|            # Search by Status (e.g., "Active")
                Q(uploaded_by_role=query)            # Search by Status (e.g., "Active")
                # Add as many Q() | as you want here!
            )[:3] 
            
            for match in matches:
                results_list.append({
                    'title': f"{match.title} - {match.location}",
                    'type': table['label'],
                    'url': reverse(table['url_name'], args=[match.id]) 
                })
        
        # 🟢 2. SEARCH USERS (By Name, Email, Phone, Role, etc.)
        users = User_Details.objects.filter(
            Q(user_name__icontains=query) | 
            Q(user_email__icontains=query) |
            Q(user_phone__icontains=query) |       # Search Last Name  # Search Phone Number
            Q(user_state__icontains=query) |        # Search by Role (e.g., "Tenant")
            Q(user_city__icontains=query)  |       # Search by Role (e.g., "Tenant")
            Q(user_role__icontains=query)         # Search by Role (e.g., "Tenant")
        )[:5]
        
       # 🟢 Create a map that connects the exact database role to its URLs.py name
        role_url_map = {
            'Tenant': 'Update_Tenant',     # Replace 'tenant_detail' with actual url name
            'Landlord': 'Update_Landlord', # Replace 'landlord_detail' with actual url name
            'Buyer': 'Update_Buyer',
            'Agent': 'Update_Agent',
            'Agency': 'Update_Agency',
            'Vendor': 'Update_Vendor',
            'Relationship Manager': 'Update_RM',
        }

        for user in users:
            # 🟢 Look up the correct URL name based on the user's role
            url_name = role_url_map.get(user.user_role)
            
            # If the role exists in our map, generate the real link. 
            # If not, fall back to '#' so the server doesn't crash.
            if url_name:
                final_url = reverse(url_name, args=[user.id])
            else:
                final_url = '#'

            results_list.append({
                'title': f"{user.user_name} ({user.user_email})",
                'type': user.user_role, 
                'url': final_url 
            })

        results_list = results_list[:10]

    return JsonResponse({'results': results_list})

########## Views end for global search ########################


############## Views start for notifications ########################

def get_todays_notifications(request):
    today = datetime.today()
    master_feed = []

    # 🟢 1. Create the Map linking Roles to their specific URLs
    role_url_map = {
        'RM': 'Update_RM',             
        'Landlord': 'Update_Landlord', 
        'Tenant': 'Update_Tenant',     
        'Buyer': 'Update_Buyer',
        'Agent': 'Update_Agent',
        'Agency': 'Update_Agency',
        'Vendor': 'Update_Vendor',
    }

    # ==========================================
    # 2. FETCH NEW USERS
    # ==========================================
    recent_users = User_Details.objects.filter(user_register_date=today).order_by('-id')[:10]
    
    for user in recent_users:
        
        #  3. Look up the correct URL name based on the user's role
        url_name = role_url_map.get(user.user_role)
        user_url = '#' # Default fallback

        if url_name:
            try:
                user_url = reverse(url_name, args=[user.id])
            except NoReverseMatch:
                pass # If URL isn't built yet, it stays '#' safely

        master_feed.append({
            'category': 'user', 
            'title': f"New {user.user_role} Registered",
            'desc': user.user_email, # Or user_name, whichever you prefer
            'timestamp': user.user_register_date, 
            'time': user.user_register_time, 
            'url': user_url #  Plugs in the dynamic URL!
        })


    # ==========================================
    # 3. FETCH NEW SUBSCRIPTIONS (Optional)
    # ==========================================
    # recent_subs = Subscriptions.objects.filter(purchased_at__date=today).order_by('-purchased_at')[:10]
    # for sub in recent_subs:
    #     master_feed.append({
    #         'category': 'sub', 
    #         'title': "Plan Purchased",
    #         'desc': f"{sub.plan_name} by User ID {sub.user_id}",
    #         'timestamp': sub.purchased_at,
    #         'time': timezone.localtime(sub.purchased_at).strftime("%I:%M %p"),
    #         'url': '#' 
    #     })


    # ==========================================
    # 4. SORT AND FINALIZE
    # ==========================================
    master_feed.sort(key=lambda x: x['timestamp'], reverse=True)
    final_feed = master_feed[:10]

    return JsonResponse({
        'notifications': final_feed
    })

############# Views endd for notifications ###############################


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
    else:
        try:
            services = Service_Type_Details.objects.get(id=data['id'])
        except Service_Type_Details.DoesNotExist:
            return JsonResponse({'status': '0', 'msg': 'Service Type Details not found'})


        # Update withdraw fields (unchanged)
        for key, value in data.items():
            setattr(services, key, value)

        services.save()
        return JsonResponse({"status":"1", "msg" : f"Service Type Details updated successfully"})

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


########### Views start for delete vendor service details ##########################

@csrf_exempt
def Delete_Services(request):
    try:
        try:
            services_id = request.POST.get('services_id')
            Service_Type_Details.objects.filter(id=services_id).delete()
            return JsonResponse({'status':'1', 'msg':'Services type details deleted successfully...'})
        except:
            traceback.print_exc()
            return JsonResponse({"status":"0", "msg" : "Something went wrong..."})
    except:
        traceback.print_exc()
        return JsonResponse({"status":"0", "msg" : "Something went wrong..."})

############## Views end for delete vendor service details #########################


########## Views start for update service details ########################

def Update_Services(request,id):
    session_id = request.session.get('Admin_id')
    if session_id:
        admin_obj = Admin_Login.objects.get(id=session_id)

        service = Service_Type_Details.objects.get(id=id)
        context = {'service':service,'admin_obj':admin_obj}

        return render(request,"admin_user/Service_Type/update_service_type.html",context)
    else:
        return render(request,'home_page/Adminlogin.html')

############ Views end for update service details ######################

############## Views start for subscriptions list ##########################

def Subscriptions_List(request):
    session_id = request.session.get('Admin_id')
    if session_id:
        admin_obj = Admin_Login.objects.get(id=session_id)

        subscriptions_obj = Subscription_Details.objects.all().order_by('-id')
        subscriptions_obj_count = Subscription_Details.objects.all().count()

        rendered = render_to_string("admin_user/render_to_string/R_Subscription/r_t_s_subsciption.html",{'subscriptions_obj':subscriptions_obj,'subscriptions_obj_count':subscriptions_obj_count})

        context = {'admin_obj':admin_obj,'subscriptions_list':rendered}

        return render(request,"admin_user/Subscription/subscriptions_list.html",context)
    else:
        return render(request,'home_page/Adminlogin.html')

############## Views end for subscriptions list ##########################


############### Views start for add subscriptions ########################

def Add_Subscriptions(request):
    session_id = request.session.get('Admin_id')
    if session_id:
        admin_obj = Admin_Login.objects.get(id=session_id)

        context = {'admin_obj':admin_obj}
        return render(request,"admin_user/Subscription/add_subscription.html",context)
    else:
        return render(request,'home_page/Adminlogin.html')

############ Views end for add subscriptions ###########################


############ Views start for ajax for add/update subscriptions ################

@csrf_exempt
def Subscriptions_Ajax(request):
    data = request.POST.dict()

    if data.get('id') == "":
        data.pop("id", None)        
        data['plan_upload_date'] = datetime.today()
        data['plan_upload_time'] = datetime.now()
        Subscription_Details.objects.create(**data)
        return JsonResponse({"status":"1", "msg" : f"Subscription Details added successfully"})

    # UPDATE MODE
    else:
        try:
            subscriptions = Subscription_Details.objects.get(id=data['id'])
        except Subscription_Details.DoesNotExist:
            return JsonResponse({'status': '0', 'msg': 'Subscription Details not found'})


        # Update withdraw fields (unchanged)
        for key, value in data.items():
            setattr(subscriptions, key, value)

        subscriptions.save()
        return JsonResponse({"status":"1", "msg" : f"Subscriptions Details updated successfully"})

########### Views end for ajax for add/update subscriptions ######################


############## Views start for delete subscriptions #####################

@csrf_exempt
def Delete_Subscriptions(request):
    try:
        try:
            subscription_id = request.POST.get('subscription_id')
            Subscription_Details.objects.filter(id=subscription_id).delete()
            return JsonResponse({'status':'1', 'msg':'Subscription type details deleted successfully...'})
        except:
            traceback.print_exc()
            return JsonResponse({"status":"0", "msg" : "Something went wrong..."})
    except:
        traceback.print_exc()
        return JsonResponse({"status":"0", "msg" : "Something went wrong..."})

########### Views end for delete subscriptions ########################


############## Views start for update subscriptions #########################

def Update_Subscriptions(request,id):
    session_id = request.session.get('Admin_id')
    if session_id:
        admin_obj = Admin_Login.objects.get(id=session_id)

        subscription = Subscription_Details.objects.get(id=id)

        context = {'admin_obj':admin_obj,'subscription':subscription}
        return render(request,"admin_user/Subscription/update_subscription.html",context)
    else:
        return render(request,'home_page/Adminlogin.html')

############# Views end for update subscriptions ##########################


########### Views start for upload subscription details via excel ###############

@csrf_exempt
def Subscriptions_Data(request):
    if request.method == 'POST':
        excel_file = request.FILES.get('subscriptions_file')

        if not excel_file:
            return JsonResponse({
                "status": "0",
                "msg": "No file uploaded."
            })

        try:
            wb = load_workbook(excel_file)
            sheet = wb.active

            # Iterating through rows, skipping the header (min_row=2)
            for row in sheet.iter_rows(min_row=2, values_only=True):
                
                # Unpacking the exact columns from your generated dummy data
                package_name = row[0]
                plan_type = row[1]
                # row[2] is plan_duration which we combined into the package name/desc in the model
                plan_for = row[3]
                plan_base_price = row[4]
                plan_offer_price = row[5]
                plan_discount = row[6]
                plan_max_listings = row[7]
                plan_offer_start_date = row[8]
                plan_offer_end_date = row[9]
                plan_desc = row[10]

                # Skip empty rows where package_name is missing
                if not package_name:
                    continue
                    
                # Format the dates properly for Django DateField if they are strings
                if isinstance(plan_offer_start_date, str):
                    try:
                        plan_offer_start_date = datetime.strptime(plan_offer_start_date, '%Y-%m-%d').date()
                    except ValueError:
                        pass # Handle or log date parsing error
                        
                if isinstance(plan_offer_end_date, str):
                    try:
                        plan_offer_end_date = datetime.strptime(plan_offer_end_date, '%Y-%m-%d').date()
                    except ValueError:
                        pass # Handle or log date parsing error

                # Create or Update the subscription plan
                # Using package_name as the unique identifier to update existing ones
                Subscription_Details.objects.update_or_create(
                    package_name=package_name,  # condition to check existing
                    defaults={
                        "plan_type": plan_type,
                        "plan_for": plan_for,
                        "plan_base_price": plan_base_price,
                        "plan_offer_price": plan_offer_price,
                        "plan_discount": plan_discount,
                        "plan_max_listings": plan_max_listings,
                        "plan_offer_start_date": plan_offer_start_date,
                        "plan_offer_end_date": plan_offer_end_date,
                        "plan_desc": plan_desc,
                        "plan_upload_date":datetime.today()
                        # is_active and created_at/updated_at will be handled by model defaults
                    }
                )

            return JsonResponse({
                "status": "1",
                "msg": "Subscriptions Uploaded / Updated Successfully..."
            })

        except Exception as e:
            # It's good practice to log 'e' here in a real application
            return JsonResponse({
                "status": "0",
                "msg": f"An error occurred while processing the file: {str(e)}"
            })

    return JsonResponse({
        "status": "0",
        "msg": "Invalid request method."
    })

########### Views end for upload subscriptions data via excel ######################


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





def residential_resale_list(request):
    session_id = request.session.get('Admin_id')
    if not session_id:
        return render(request, 'home_page/Adminlogin.html')

    admin_obj = Admin_Login.objects.get(id=session_id)

    # ── Fetch properties ─────────────────────────────
    properties = ResaleResidentialProperty.objects.prefetch_related('images').order_by('-created_at')

    for prop in properties:
        # ✅ Thumbnail
        prop.thumbnail = prop.images.first()

        # ✅ Convert facilities & amenities to list
        prop.nearby_facilities_list = (
            [f.strip() for f in prop.nearby_facilities.split(',')]
            if prop.nearby_facilities else []
        )

        prop.amenities_list = (
            [a.strip() for a in prop.amenities.split(',')]
            if prop.amenities else []
        )

        # ✅ Image count
        prop.image_count = prop.images.count()
        
        # 🔥🔥 ADD THIS (MOST IMPORTANT FIX)
        prop.image_urls = [img.image.url for img in prop.images.all()]

    # ── Stats ────────────────────────────────────────
    total_negotiable  = properties.filter(is_negotiable='yes').count()
    total_furnished   = properties.filter(furnishing_type='fully').count()
    total_freehold    = properties.filter(ownership_type='freehold').count()
    total_with_images = sum(1 for p in properties if p.thumbnail)

    # ── Charts ───────────────────────────────────────
    property_type_counts = dict(
        properties.values_list('property_type')
        .annotate(count=Count('id'))
        .values_list('property_type', 'count')
    )

    bhk_counts = dict(
        properties.values_list('bhk')
        .annotate(count=Count('id'))
        .values_list('bhk', 'count')
    )

    fully_furnished = properties.filter(furnishing_type='fully').count()
    semi_furnished  = properties.filter(furnishing_type='semi').count()
    unfurnished     = properties.filter(furnishing_type='unfurnished').count()

    zone_counts = dict(
        properties.values_list('zone')
        .annotate(count=Count('id'))
        .values_list('zone', 'count')
    )

    # ── Fetch unique uploaded file names for the Bulk Delete modal ──
    try:
        # Note: Replace 'upload_file_name' with your actual model field name if different
        uploaded_files = properties.exclude(
            upload_file_name__isnull=True
        ).exclude(upload_file_name='').values_list('upload_file_name', flat=True).distinct()
    except Exception:
        uploaded_files = []

    context = {
        'admin_obj': admin_obj,
        'properties': properties,

        'total_negotiable': total_negotiable,
        'total_furnished': total_furnished,
        'total_freehold': total_freehold,
        'total_with_images': total_with_images,

        'property_type_counts': property_type_counts,
        'bhk_counts': bhk_counts,
        'fully_furnished': fully_furnished,
        'semi_furnished': semi_furnished,
        'unfurnished': unfurnished,
        'zone_counts': zone_counts,
        'uploaded_files': uploaded_files, # Passed files to template here
    }

    return render(request, 'admin_user/Reports/Resale/residential_resale_list.html', context)


def resale_residential_bulk_delete(request):
    """Handles Advanced Bulk Deletions for Resale Residential Properties."""
    if request.method != 'POST':
        return JsonResponse({'status': 'error', 'message': 'Invalid request method.'})
        
    session_id = request.session.get('Admin_id')
    if not session_id:
        return JsonResponse({'status': 'error', 'message': 'Unauthorized access.'})

    try:
        data = json.loads(request.body)
        delete_type = data.get('delete_type')
        properties = ResaleResidentialProperty.objects.all()
        
        if delete_type == 'delete_all':
            count = properties.count()
            properties.delete()
            return JsonResponse({'status': 'success', 'message': f'Successfully deleted ALL {count} resale properties.'})
            
        elif delete_type == 'current_page':
            page_ids = data.get('page_ids', [])
            target_props = properties.filter(id__in=page_ids) # Or pk__in
            count = target_props.count()
            target_props.delete()
            return JsonResponse({'status': 'success', 'message': f'Successfully deleted {count} resale properties from current page.'})
            
        elif delete_type == 'date_range':
            from_date = data.get('from_date')
            to_date = data.get('to_date')
            # Using created_at for accurate date ranges, change to available_from if needed
            target_props = properties.filter(created_at__range=[from_date, to_date])
            count = target_props.count()
            target_props.delete()
            return JsonResponse({'status': 'success', 'message': f'Successfully deleted {count} resale properties in date range.'})
            
        elif delete_type == 'latest_month':
            thirty_days_ago = timezone.now() - timedelta(days=30)
            target_props = properties.filter(created_at__gte=thirty_days_ago)
            count = target_props.count()
            target_props.delete()
            return JsonResponse({'status': 'success', 'message': f'Successfully deleted {count} resale properties from the last 30 days.'})
            
        elif delete_type == 'old_data':
            six_months_ago = timezone.now() - timedelta(days=180)
            target_props = properties.filter(created_at__lt=six_months_ago)
            count = target_props.count()
            target_props.delete()
            return JsonResponse({'status': 'success', 'message': f'Successfully deleted {count} older resale properties.'})
            
        elif delete_type == 'by_uploader':
            uploader = data.get('uploader_text', '')
            target_props = properties.filter(
                Q(uploaded_by_name__icontains=uploader) | 
                Q(uploaded_by_email__icontains=uploader) |
                Q(uploaded_by_role__icontains=uploader)
            )
            count = target_props.count()
            target_props.delete()
            return JsonResponse({'status': 'success', 'message': f'Successfully deleted {count} resale properties uploaded by {uploader}.'})

        elif delete_type == 'by_file':
            file_name = data.get('file_name', '')
            # Replace 'upload_file_name' with your exact database field name for tracking files
            target_props = properties.filter(upload_file_name=file_name) 
            count = target_props.count()
            if count == 0:
                return JsonResponse({'status': 'error', 'message': f'No properties found for file: {file_name}'})
            target_props.delete()
            return JsonResponse({'status': 'success', 'message': f'Successfully deleted {count} resale properties from {file_name}.'})
            
        else:
            return JsonResponse({'status': 'error', 'message': 'Unknown delete criteria.'})

    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)})






############ Views end for resale residential list #######################



########### Views start for display rm list ##########################

@csrf_exempt
def rm_list(request):

    if request.method=="POST":
        start_date= request.POST.get('start_date')
        end_date= request.POST.get('end_date')
        rm_obj = User_Details.objects.filter(user_register_date__gte=start_date,user_register_date__lte=end_date,user_role="Relationship Manager").order_by("-id")
        if User_Details.objects.filter(user_register_date__gte=start_date,user_register_date__lte=end_date,user_role="Relationship Manager").exists():
            rm_obj_count = User_Details.objects.filter(user_register_date__gte=start_date,user_register_date__lte=end_date,user_role="Relationship Manager").count()
            rendered = render_to_string("admin_user/render_to_string/R_RM/r_t_s_rm.html",{'rm_obj':rm_obj,'rm_obj_count':rm_obj_count,'Role':'Relationship Manager'})
            return HttpResponse(rendered)
        else:
            return HttpResponse("error")

            
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


############ Views start for ajax for delete bulk users #####################

@csrf_exempt
def Users_Bulk_Delete(request):
    try:
        data = json.loads(request.body)
        delete_type = data.get('delete_type')
        
        #  BUG FIX 1: This was incorrectly pulling 'delete_type' before
        role = data.get('role') 
        
        # Base query: Get all users of the selected role
        users = User_Details.objects.filter(user_role=role)

        print(f"--- Bulk Delete Request: Type={delete_type}, Role={role} ---")
        
        if delete_type == 'delete_all':
            count = users.count()
            users.delete()
            return JsonResponse({'status': 'success', 'message': f'Successfully deleted ALL {count} users ({role}).'})

            
        elif delete_type == 'date_range':
            from_date = data.get('from_date')
            to_date = data.get('to_date')
            # Assuming your date field is 'user_register_date'. Adjust if necessary.
            target_users = users.filter(user_register_date__range=[from_date, to_date])
            count = target_users.count()
            target_users.delete()
            return JsonResponse({'status': 'success', 'message': f'Successfully deleted {count} users ({role}) in date range.'})
            
            
        elif delete_type == 'latest_month':
            thirty_days_ago = timezone.now() - timedelta(days=30)
            #  BUG FIX 2 & 3: Used the base 'users' queryset so it respects the role filter
            target_users = users.filter(user_register_date__gte=thirty_days_ago)
            count = target_users.count()
            target_users.delete()
            return JsonResponse({'status': 'success', 'message': f'Successfully deleted {count} users ({role}) from the last 30 days.'})
            
            
        elif delete_type == 'old_data':
            six_months_ago = timezone.now() - timedelta(days=180)
            #  BUG FIX 2 & 3: Used the base 'users' queryset so it respects the role filter
            target_users = users.filter(user_register_date__lt=six_months_ago)
            count = target_users.count()
            target_users.delete()
            return JsonResponse({'status': 'success', 'message': f'Successfully deleted {count} older users ({role}).'})
            

        elif delete_type == 'current_page':
            # This handles the front-end 'current_page' logic if you pass page_ids
            page_ids = data.get('page_ids', [])
            target_users = users.filter(id__in=page_ids)
            count = target_users.count()
            target_users.delete()
            return JsonResponse({'status': 'success', 'message': f'Successfully deleted {count} users ({role}) from the current page.'})

            
        else:
            return JsonResponse({'status': 'error', 'message': 'Unknown delete criteria.'})

    except Exception as e:
        return JsonResponse({'status': 'error', 'message': f'Server error: {str(e)}'})

############# Views end for ajax for delete bulk users #######################


########### Views start for display landlords list ###################

@csrf_exempt
def Landlord_List(request):

    if request.method=="POST":
        start_date= request.POST.get('start_date')
        end_date= request.POST.get('end_date')
        landlord_obj = User_Details.objects.filter(user_register_date__gte=start_date,user_register_date__lte=end_date,user_role="Landlord").order_by("-id")
        if User_Details.objects.filter(user_register_date__gte=start_date,user_register_date__lte=end_date,user_role="Landlord").exists():
            landlord_obj_count = User_Details.objects.filter(user_register_date__gte=start_date,user_register_date__lte=end_date,user_role="Landlord").count()
            rendered = render_to_string("admin_user/render_to_string/R_Landlord/r_t_s_landlord.html",{'landlord_obj':landlord_obj,'landlord_obj_count':landlord_obj_count,'Role':'Landlord'})

            return HttpResponse(rendered)
        else:
            return HttpResponse("error")


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

@csrf_exempt
def Tenant_List(request):

    if request.method=="POST":
        start_date= request.POST.get('start_date')
        end_date= request.POST.get('end_date')
        tenant_obj = User_Details.objects.filter(user_register_date__gte=start_date,user_register_date__lte=end_date,user_role="Tenant").order_by("-id")
        if User_Details.objects.filter(user_register_date__gte=start_date,user_register_date__lte=end_date,user_role="Tenant").exists():
            tenant_obj_count = User_Details.objects.filter(user_register_date__gte=start_date,user_register_date__lte=end_date,user_role="Tenant").count()

            rendered = render_to_string("admin_user/render_to_string/R_Tenant/r_t_s_tenant.html",{'tenant_obj':tenant_obj,'tenant_obj_count':tenant_obj_count,'Role':'Tenant'})
            
            return HttpResponse(rendered)
        else:
            return HttpResponse("error")


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

@csrf_exempt
def Buyer_List(request):

    if request.method=="POST":
        start_date= request.POST.get('start_date')
        end_date= request.POST.get('end_date')
        buyer_obj = User_Details.objects.filter(user_register_date__gte=start_date,user_register_date__lte=end_date,user_role="Buyer").order_by("-id")
        if User_Details.objects.filter(user_register_date__gte=start_date,user_register_date__lte=end_date,user_role="Buyer").exists():
            buyer_obj_count = User_Details.objects.filter(user_register_date__gte=start_date,user_register_date__lte=end_date,user_role="Buyer").count()

            rendered = render_to_string("admin_user/render_to_string/R_Buyer/r_t_s_buyer.html",{'buyer_obj':buyer_obj,'buyer_obj_count':buyer_obj_count,'Role':'Buyer'})

            return HttpResponse(rendered)
        else:
            return HttpResponse("error")


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

@csrf_exempt
def Agent_List(request):

    if request.method=="POST":
        start_date= request.POST.get('start_date')
        end_date= request.POST.get('end_date')
        agent_obj = User_Details.objects.filter(user_register_date__gte=start_date,user_register_date__lte=end_date,user_role="Agent").order_by("-id")
        if User_Details.objects.filter(user_register_date__gte=start_date,user_register_date__lte=end_date,user_role="Agent").exists():
            agent_obj_count = User_Details.objects.filter(user_register_date__gte=start_date,user_register_date__lte=end_date,user_role="Agent").count()

            rendered = render_to_string("admin_user/render_to_string/R_Agent/r_t_s_agent.html",{'agent_obj':agent_obj,'agent_obj_count':agent_obj_count,'Role':'Agent'})

            return HttpResponse(rendered)
        else:
            return HttpResponse("error")
        
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

@csrf_exempt
def Agency_List(request):

    if request.method=="POST":
        start_date= request.POST.get('start_date')
        end_date= request.POST.get('end_date')
        agency_obj = User_Details.objects.filter(user_register_date__gte=start_date,user_register_date__lte=end_date,user_role="Agency/Builder").order_by("-id")
        if User_Details.objects.filter(user_register_date__gte=start_date,user_register_date__lte=end_date,user_role="Agency/Builder").exists():
            agency_obj_count = User_Details.objects.filter(user_register_date__gte=start_date,user_register_date__lte=end_date,user_role="Agency/Builder").count()

            rendered = render_to_string("admin_user/render_to_string/R_Agency/r_t_s_agency.html",{'agency_obj':agency_obj,'agency_obj_count':agency_obj_count,'Role':'Agency'})

            return HttpResponse(rendered)
        else:
            return HttpResponse("error")


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

@csrf_exempt
def Vendor_List(request):


    if request.method=="POST":
        start_date= request.POST.get('start_date')
        end_date= request.POST.get('end_date')
        vendor_obj = User_Details.objects.filter(user_register_date__gte=start_date,user_register_date__lte=end_date,user_role="Vendor").order_by("-id")
        if User_Details.objects.filter(user_register_date__gte=start_date,user_register_date__lte=end_date,user_role="Vendor").exists():
            vendor_obj_count = User_Details.objects.filter(user_register_date__gte=start_date,user_register_date__lte=end_date,user_role="Vendor").count()

            rendered = render_to_string("admin_user/render_to_string/R_Vendor/r_t_s_vendor.html",{'vendor_obj':vendor_obj,'vendor_obj_count':vendor_obj_count,'Role':'Vendor'})

            return HttpResponse(rendered)
        else:
            return HttpResponse("error")


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

        for row in sheet.iter_rows(min_row=2, values_only=True):
            # 1. ADD SAFETY CHECK: Ensure the row has at least 14 columns
            if len(row) < 14:
                continue  # Skip rows that don't have all the new vendor fields

            user_name = row[0]
            user_email = row[1]
            user_phone = row[2]
            user_state = row[3]
            user_city = row[4]
            user_address = row[5]
            user_password = row[6]
           
            # New Vendor Fields
            user_service_type = row[8]
            user_company_name = row[9]
            user_pan_number = row[10]
            user_gstin_number = row[11]
            user_role = row[12]
            operational_areas = row[13]

            # Cleaning numeric strings
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


############ Views start for update profile page ########################

def Update_Profile_Admin(request):
    session_id = request.session.get('Admin_id')
    if session_id:
        admin_obj = Admin_Login.objects.get(id=session_id)

        context = {'admin_obj':admin_obj}

        return render(request,'admin_user/Profile/profile_admin.html',context)
    else:
        return render(request,'home_page/Adminlogin.html')

############# Views end for update profile page ###########################


############ Views start for ajax for update profile #######################

@csrf_exempt
def Admin_Profile_Ajax(request):
    data=request.POST.dict()
    try:
        Admin_Login.objects.get(id=data['id'])
        Admin_Login.objects.filter(id=data['id']).update(**data)
        return JsonResponse({"status":"1", "msg" : f"Profile updated successfully"})
    except:
        traceback.print_exc()
        return JsonResponse({"status":"0", "msg" : "Something went wrong..."})

############## Views end for ajax for update profile ##########################



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





# services/views.py



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








 

##################################RESIDENTIAL RENTAL LISTING VEIW SECTION START##############################




def rental_residential_add(request):

    admin_id = request.session.get('Admin_id')
    user_id = request.session.get('User_id')

    admin_obj = None
    user_obj = None

    # Safe fetch (NO crash)
    if admin_id:
        admin_obj = Admin_Login.objects.filter(id=admin_id).first()

    if user_id:
        user_obj = User_Details.objects.filter(id=user_id).first()

    # If not logged in
    if not admin_obj and not user_obj:
        return render(request, 'home_page/Adminlogin.html')

    if request.method == 'POST':
        try:

            # ---------- HELPERS ----------
            def to_int(val):
                try:
                    return int(val) if val else None
                except:
                    return None

            def to_decimal(val):
                try:
                    return float(val) if val else None
                except:
                    return None

            # ---------- DATE FIX ----------
            date_val = request.POST.get('available_from')
            if date_val:
                try:
                    available_from = datetime.strptime(date_val, "%Y-%m-%d").date()
                except:
                    available_from = None
            else:
                available_from = None

            # ---------- AMENITIES ----------
            amenities = ",".join(request.POST.getlist('amenities[]'))
            facilities = ",".join(request.POST.getlist('facilities[]'))

            # ---------- UPLOADER (FIXED) ----------
            if admin_obj:
                uploader_name = getattr(admin_obj, 'name', '') or getattr(admin_obj, 'username', '')
                uploader_email = getattr(admin_obj, 'email', '')
                uploader_contact = getattr(admin_obj, 'phone', '') or getattr(admin_obj, 'mobile', '')
                uploader_role = "Admin"

            elif user_obj:
                uploader_name = user_obj.user_name
                uploader_email = user_obj.user_email
                uploader_contact = user_obj.user_phone
                uploader_role = "User"

            # ---------- CREATE OBJECT ----------
            prop = RentalResidentialProperty.objects.create(

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

                zone=request.POST.get('zone'),
                ownership_type=request.POST.get('ownership_type'),
                construction_status=request.POST.get('construction_status'),
                property_age=request.POST.get('property_age'),
                carpet_area=to_decimal(request.POST.get('carpet_area')),
                plot_area=to_decimal(request.POST.get('plot_area')),
                building_name=request.POST.get('building_name'),

                possession_status=request.POST.get('possession_status'),
                available_from=available_from,
                lease_duration=request.POST.get('lease_duration'),
                brokerage=request.POST.get('brokerage'),
                brokerage_percentage=request.POST.get('brokerage_percentage'),
                manual_brokerage=request.POST.get('manual_brokerage'),

                monthly_rent=to_int(request.POST.get('monthly_rent')),
                security_deposit=to_int(request.POST.get('security_deposit')),
                maintenance_type=request.POST.get('maintenance_type'),
                maintenance_amount=to_int(request.POST.get('maintenance_amount')),

                address=request.POST.get('address'),
                city=request.POST.get('city'),
                locality=request.POST.get('locality'),
                state=request.POST.get('state'),
                pincode=request.POST.get('pincode'),
                road_connectivity=request.POST.get('road_connectivity'),

                amenities=amenities,
                facilities=facilities,

                description=request.POST.get('description'),
                rent_residential_desc=request.POST.get('rent_residential_desc'),

                owner_name=request.POST.get('owner_name'),
                contact_number=request.POST.get('contact_number'),
                email=request.POST.get('email'),
                alternate_contact=request.POST.get('alternate_contact'),

                uploaded_by_name=uploader_name,
                uploaded_by_email=uploader_email,
                uploaded_by_contact=uploader_contact,
                uploaded_by_role=uploader_role,
            )

            # ---------- ✅ NEW IMAGE UPLOAD LOGIC ----------
            images = request.FILES.getlist('property_images[]')

            # Loop through the files (up to 10) and save them to the new Image model
            for img in images[:10]:
                RentalResidentialImage.objects.create(
                    property=prop, 
                    image=img
                )
            # -----------------------------------------------

            messages.success(request, "Property Added Successfully ✅")
            return redirect('rental_residential_add')

        except Exception as e:
            print("ERROR:", str(e))
            messages.error(request, f"Error: {str(e)}")
            return redirect('rental_residential_add')

    # ---------- GET ----------
    return render(request, 'admin_user/Reports/Rental/rental_list.html', {
        'admin_obj': admin_obj,
        'user_obj': user_obj,
        'ameneties_obj': Ameneties_Details.objects.all(),
        'facilities_obj': Facilities_Details.objects.all()
    })










def rental_list(request):
    session_id = request.session.get('Admin_id')
    if not session_id:
        return render(request, 'home_page/Adminlogin.html')

    admin_obj = Admin_Login.objects.get(id=session_id)
    search_query = request.GET.get('search', '').strip()

    # ── Base queryset ──
    try:
        properties = RentalResidentialProperty.objects.all().order_by('-id')
    except Exception as e:
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
        except Exception as e:
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
    except Exception as e:
        page_obj = Paginator(RentalResidentialProperty.objects.none(), 10).get_page(1)

    total_count = properties.count()

    # ════════════════════════════════════════════════
    # STATS — computed on the FULL unfiltered queryset
    # ════════════════════════════════════════════════
    all_props = RentalResidentialProperty.objects.all()

    active_count = all_props.exclude(possession_status__isnull=True).exclude(possession_status='').count()
    furnished_count = all_props.filter(furnishing_status__iexact='Furnished').count()
    available_count = all_props.filter(possession_status__iexact='Ready to Move').count()
    city_count = all_props.exclude(city__isnull=True).exclude(city='').values('city').distinct().count()

    rent_stats = all_props.exclude(monthly_rent__isnull=True).aggregate(
        avg_rent=Avg('monthly_rent'),
        max_rent=Max('monthly_rent'),
        min_rent=Min('monthly_rent'),
    )
    avg_rent = rent_stats['avg_rent']
    max_rent = rent_stats['max_rent']
    min_rent = rent_stats['min_rent']

    deposit_stats = all_props.exclude(security_deposit__isnull=True).aggregate(avg_deposit=Avg('security_deposit'))
    avg_deposit = deposit_stats['avg_deposit']

    area_stats = all_props.exclude(built_up_area__isnull=True).aggregate(avg_area=Avg('built_up_area'))
    avg_area = area_stats['avg_area']

    with_owner_count = all_props.exclude(owner_name__isnull=True).exclude(owner_name='').count()
    with_images_count = all_props.filter(images__isnull=False).distinct().count()

    # ── Fetch unique uploaded file names for the Bulk Delete modal ──
    try:
        # Note: Replace 'upload_file_name' with your actual model field name if different
        uploaded_files = all_props.exclude(
            upload_file_name__isnull=True
        ).exclude(upload_file_name='').values_list('upload_file_name', flat=True).distinct()
    except Exception:
        uploaded_files = []

    # ════════════════════════════════════════════════
    # CHART DATA
    # ════════════════════════════════════════════════
    bhk_qs = all_props.exclude(bhk_type__isnull=True).exclude(bhk_type='').values('bhk_type').annotate(count=Count('id')).order_by('-count')
    bhk_labels = json.dumps([item['bhk_type'] for item in bhk_qs])
    bhk_data   = json.dumps([item['count']    for item in bhk_qs])

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
        all_props.filter(monthly_rent__gte=lo, monthly_rent__lt=hi).count()
        for _, lo, hi in rent_buckets
    ])

    furnish_qs = all_props.exclude(furnishing_status__isnull=True).exclude(furnishing_status='').values('furnishing_status').annotate(count=Count('id')).order_by('-count')
    furnishing_labels = json.dumps([item['furnishing_status'] for item in furnish_qs])
    furnishing_data   = json.dumps([item['count']             for item in furnish_qs])

    prop_type_qs = all_props.exclude(property_type__isnull=True).exclude(property_type='').values('property_type').annotate(count=Count('id')).order_by('-count')
    prop_type_labels = json.dumps([item['property_type'] for item in prop_type_qs])
    prop_type_data   = json.dumps([item['count']         for item in prop_type_qs])

    # ════════════════════════════════════════════════
    # CONTEXT
    # ════════════════════════════════════════════════
    context = {
        'admin_obj': admin_obj,
        'page_obj': page_obj,
        'search_query': search_query,
        'total_count': total_count,
        'active_count': active_count,
        'furnished_count': furnished_count,
        'available_count': available_count,
        'city_count': city_count,
        'avg_rent': avg_rent,
        'max_rent': max_rent,
        'min_rent': min_rent,
        'avg_deposit': avg_deposit,
        'avg_area': avg_area,
        'with_owner_count': with_owner_count,
        'with_images_count': with_images_count,
        'uploaded_files': uploaded_files, # Added the files here
        'bhk_labels': bhk_labels,
        'bhk_data': bhk_data,
        'rent_range_labels': rent_range_labels,
        'rent_range_data': rent_range_data,
        'furnishing_labels': furnishing_labels,
        'furnishing_data': furnishing_data,
        'prop_type_labels': prop_type_labels,
        'prop_type_data': prop_type_data,
    }

    return render(request, 'admin_user/Reports/Rental/rental_list.html', context)


def rental_bulk_delete(request):
    """Handles Advanced Bulk Deletions for Rental Properties."""
    if request.method != 'POST':
        return JsonResponse({'status': 'error', 'message': 'Invalid request method.'})
        
    session_id = request.session.get('Admin_id')
    if not session_id:
        return JsonResponse({'status': 'error', 'message': 'Unauthorized access.'})

    try:
        data = json.loads(request.body)
        delete_type = data.get('delete_type')
        properties = RentalResidentialProperty.objects.all()
        
        if delete_type == 'delete_all':
            count = properties.count()
            properties.delete()
            return JsonResponse({'status': 'success', 'message': f'Successfully deleted ALL {count} properties.'})
            
        elif delete_type == 'current_page':
            page_ids = data.get('page_ids', [])
            target_props = properties.filter(id__in=page_ids)
            count = target_props.count()
            target_props.delete()
            return JsonResponse({'status': 'success', 'message': f'Successfully deleted {count} properties from current page.'})
            
        elif delete_type == 'date_range':
            from_date = data.get('from_date')
            to_date = data.get('to_date')
            target_props = properties.filter(available_from__range=[from_date, to_date])
            count = target_props.count()
            target_props.delete()
            return JsonResponse({'status': 'success', 'message': f'Successfully deleted {count} properties in date range.'})
            
        elif delete_type == 'latest_month':
            thirty_days_ago = timezone.now() - timedelta(days=30)
            target_props = properties.filter(available_from__gte=thirty_days_ago)
            count = target_props.count()
            target_props.delete()
            return JsonResponse({'status': 'success', 'message': f'Successfully deleted {count} properties from the last 30 days.'})
            
        elif delete_type == 'old_data':
            six_months_ago = timezone.now() - timedelta(days=180)
            target_props = properties.filter(available_from__lt=six_months_ago)
            count = target_props.count()
            target_props.delete()
            return JsonResponse({'status': 'success', 'message': f'Successfully deleted {count} older properties.'})
            
        elif delete_type == 'by_uploader':
            uploader = data.get('uploader_text', '')
            target_props = properties.filter(
                Q(uploaded_by_name__icontains=uploader) | 
                Q(uploaded_by_email__icontains=uploader) |
                Q(uploaded_by_role__icontains=uploader)
            )
            count = target_props.count()
            target_props.delete()
            return JsonResponse({'status': 'success', 'message': f'Successfully deleted {count} properties uploaded by {uploader}.'})

        elif delete_type == 'by_file':
            file_name = data.get('file_name', '')
            # Replace 'upload_file_name' with your exact database field name for tracking files
            target_props = properties.filter(upload_file_name=file_name) 
            count = target_props.count()
            if count == 0:
                return JsonResponse({'status': 'error', 'message': f'No properties found for file: {file_name}'})
            target_props.delete()
            return JsonResponse({'status': 'success', 'message': f'Successfully deleted {count} properties from {file_name}.'})
            
        else:
            return JsonResponse({'status': 'error', 'message': 'Unknown delete criteria.'})

    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)})




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

    # -------------------------------
    # COLUMN MAP (MATCHES DB EXACTLY)
    # -------------------------------
    RESIDENTIAL_COLUMN_MAP = [
        # Basic Information
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

        # Property Details
        ("zone", "zone", _str),
        ("ownership_type", "ownership_type", _str),
        ("construction_status", "construction_status", _str),
        ("property_age", "property_age", _str),
        ("carpet_area", "carpet_area", _decimal),
        ("plot_area", "plot_area", _decimal),
        ("building_name", "building_name", _str),

        # Availability
        ("possession_status", "possession_status", _str),
        ("available_from", "available_from", _date),
        ("lease_duration", "lease_duration", _str),
        ("brokerage", "brokerage", _str),
        ("brokerage_percentage", "brokerage_percentage", _str),
        ("manual_brokerage", "manual_brokerage", _str),

        # Pricing
        ("monthly_rent", "monthly_rent", _bigint),
        ("security_deposit", "security_deposit", _bigint),
        ("maintenance_type", "maintenance_type", _str),
        ("maintenance_amount", "maintenance_amount", _bigint),
        ("expected_price", "expected_price", _bigint),

        # Location
        ("address", "address", _str),
        ("city", "city", _str),
        ("locality", "locality", _str),
        ("state", "state", _str),
        ("pincode", "pincode", _str),
        ("road_connectivity", "road_connectivity", _str),

        # Amenities & Facilities
        ("amenities", "amenities", _str),
        ("facilities", "facilities", _str),

        # Description
        ("description", "description", _str),
        ("rent_residential_desc", "rent_residential_desc", _str),

        # Owner Details
        ("owner_name", "owner_name", _str),
        ("contact_number", "contact_number", _str),
        ("email", "email", _email),
        ("alternate_contact", "alternate_contact", _str),

        # Uploaded By
        ("uploaded_by_name", "uploaded_by_name", _str),
        ("uploaded_by_email", "uploaded_by_email", _str),
        ("uploaded_by_contact", "uploaded_by_contact", _str),
        ("uploaded_by_role", "uploaded_by_role", _str),
    ]

    # -------------------------------
    # FILE CHECK
    # -------------------------------
    excel_file = request.FILES.get("rental_file")

    if not excel_file:
        return JsonResponse({"status": "error", "message": "No file uploaded."}, status=400)

    if not excel_file.name.endswith(".xlsx"):
        return JsonResponse({"status": "error", "message": "Only .xlsx files allowed."}, status=400)

    # -------------------------------
    # LOAD EXCEL
    # -------------------------------
    try:
        wb = openpyxl.load_workbook(excel_file, read_only=True, data_only=True)
        ws = wb.active
    except Exception as e:
        return JsonResponse({"status": "error", "message": f"Error opening file: {str(e)}"}, status=400)

    # -------------------------------
    # READ HEADERS
    # -------------------------------
    headers = {}
    first_row = next(ws.iter_rows(min_row=1, max_row=1))

    for col_idx, cell in enumerate(first_row, 1):
        if cell.value:
            key = str(cell.value).strip().lower().replace(" ", "_")
            headers[key] = col_idx

    # -------------------------------
    # CHECK MISSING COLUMNS
    # -------------------------------
    missing = [col[0] for col in RESIDENTIAL_COLUMN_MAP if col[0] not in headers]

    if missing:
        return JsonResponse({
            "status": "error",
            "message": f"Missing columns: {', '.join(missing)}"
        }, status=400)

    # -------------------------------
    # PROCESS DATA
    # -------------------------------
    created_count = 0
    error_rows = []

    for row_idx, row in enumerate(ws.iter_rows(min_row=2, values_only=True), start=2):

        if all(v is None or str(v).strip() == "" for v in row):
            continue

        obj_data = {}
        row_error = None

        for excel_col, model_field, converter in RESIDENTIAL_COLUMN_MAP:
            col_index = headers.get(excel_col)

            raw_val = None
            if col_index and col_index - 1 < len(row):
                raw_val = row[col_index - 1]

            try:
                obj_data[model_field] = converter(raw_val)
            except Exception as e:
                row_error = f"Row {row_idx}, Column '{excel_col}': {str(e)}"
                break

        if row_error:
            error_rows.append(row_error)
            continue

        try:
            RentalResidentialProperty.objects.create(**obj_data)
            created_count += 1
        except Exception as e:
            error_rows.append(f"Row {row_idx}: DB Error - {str(e)}")

    wb.close()

    # -------------------------------
    # RESPONSE
    # -------------------------------
    return JsonResponse({
        "status": "success",
        "message": f"{created_count} records imported",
        "created": created_count,
        "error_count": len(error_rows),
        "errors": error_rows,
    })


def download_residential_template(request):
    
    wb = openpyxl.Workbook()
    ws = wb.active

    # EXACT DB SEQUENCE
    headers = [
        "property_title", "property_purpose", "property_type", "bhk_type", 
        "renting_option", "furnishing_status", "available_for", "built_up_area",
        "bathrooms", "balconies", "floor_number", "total_floors", "facing",
        
        "zone", "ownership_type", "construction_status", "property_age",
        "carpet_area", "plot_area", "building_name",
        
        "possession_status", "available_from", "lease_duration", "brokerage",
        "brokerage_percentage", "manual_brokerage",
        
        "monthly_rent", "security_deposit", "maintenance_type", "maintenance_amount", "expected_price",
        
        "address", "city", "locality", "state", "pincode", "road_connectivity",
        
        "amenities", "facilities",
        
        "description", "rent_residential_desc",
        
        "owner_name", "contact_number", "email", "alternate_contact",
        
        "uploaded_by_name", "uploaded_by_email", "uploaded_by_contact", "uploaded_by_role"
    ]

    # ✅ ADDED SAMPLE DATA EXACTLY MATCHING THE HEADERS
    sample_data = [
        "Beautiful 3BHK for Rent", "Rent", "Apartment", "3 BHK", 
        "Full Property", "Semi-Furnished", "Family", 1500.50,
        3, 2, "4th Floor", 10, "East",
        
        "North", "Freehold", "Ready to Move", "1-5 Years",
        1200.00, 1600.00, "Green Valley Heights",
        
        "Ready to Move", "2024-05-01", "11 Months", "Yes",
        "1 Month Rent", "None",
        
        25000, 50000, "Extra", 2500, 25000,
        
        "Flat 402, Green Valley", "Nagpur", "Dharampeth", "Maharashtra", "440010", "Highway Access",
        
        "Gym, Swimming Pool, Parking", "Hospital, School, Market",
        
        "Spacious and well-ventilated apartment.", "Newly painted, modular kitchen included.",
        
        "Rajesh Sharma", "9876543210", "rajesh@example.com", "9123456780",
        
        "Admin User", "admin@site.com", "1234567890", "SuperAdmin"
    ]

    # Write Headers (Row 1)
    for col, header in enumerate(headers, 1):
        cell = ws.cell(row=1, column=col, value=header)
        cell.font = Font(bold=True)

    # Write Sample Data (Row 2)
    for col, data in enumerate(sample_data, 1):
        ws.cell(row=2, column=col, value=data)

    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = 'attachment; filename="residential_template.xlsx"'
    wb.save(response)
    return response


def rental_residential_view(request, pk):
    """View a single property detail."""
    prop = get_object_or_404(RentalResidentialProperty, pk=pk)
    return render(request, 'admin_user/Reports/Rental/rental_residential_detail.html', {'property': prop})





def rental_residential_edit(request, pk):
    prop = get_object_or_404(RentalResidentialProperty, pk=pk)

    if request.method == 'POST':
        try:
            # ---------------- BASIC ----------------
            prop.property_title = request.POST.get('property_title')
            prop.property_purpose = request.POST.get('property_purpose')
            prop.property_type = request.POST.get('property_type')
            prop.bhk_type = request.POST.get('bhk_type')
            prop.renting_option = request.POST.get('renting_option')
            prop.furnishing_status = request.POST.get('furnishing_status')
            prop.available_for = request.POST.get('available_for')

            prop.built_up_area = request.POST.get('built_up_area') or None
            prop.carpet_area = request.POST.get('carpet_area') or None
            prop.plot_area = request.POST.get('plot_area') or None

            prop.bathrooms = request.POST.get('bathrooms') or None
            prop.balconies = request.POST.get('balconies') or None

            prop.floor_number = request.POST.get('floor_number')
            prop.total_floors = request.POST.get('total_floors') or None
            prop.facing = request.POST.get('facing')

            # ---------------- DETAILS ----------------
            prop.zone = request.POST.get('zone')
            prop.ownership_type = request.POST.get('ownership_type')
            prop.construction_status = request.POST.get('construction_status')
            prop.property_age = request.POST.get('property_age')
            prop.building_name = request.POST.get('building_name')

            # ---------------- AVAILABILITY ----------------
            prop.possession_status = request.POST.get('possession_status')
            prop.available_from = request.POST.get('available_from') or None
            prop.lease_duration = request.POST.get('lease_duration')

            prop.brokerage = request.POST.get('brokerage')
            prop.brokerage_percentage = request.POST.get('brokerage_percentage')
            prop.manual_brokerage = request.POST.get('manual_brokerage')

            # ---------------- PRICING ----------------
            prop.monthly_rent = request.POST.get('monthly_rent') or None
            prop.security_deposit = request.POST.get('security_deposit') or None
            prop.maintenance_type = request.POST.get('maintenance_type')
            prop.maintenance_amount = request.POST.get('maintenance_amount') or None
            prop.expected_price = request.POST.get('expected_price') or None

            # ---------------- LOCATION ----------------
            prop.address = request.POST.get('address')
            prop.city = request.POST.get('city')
            prop.locality = request.POST.get('locality')
            prop.state = request.POST.get('state')
            prop.pincode = request.POST.get('pincode')
            prop.road_connectivity = request.POST.get('road_connectivity')

            # ---------------- AMENITIES & FACILITIES (FIXED) ----------------
            prop.amenities = ",".join(request.POST.getlist('amenities[]'))
            prop.facilities = ",".join(request.POST.getlist('facilities[]'))

            # ---------------- DESCRIPTION ----------------
            prop.description = request.POST.get('description')
            prop.rent_residential_desc = request.POST.get('rent_residential_desc')

            # ---------------- OWNER ----------------
            prop.owner_name = request.POST.get('owner_name')
            prop.contact_number = request.POST.get('contact_number')
            prop.email = request.POST.get('email')
            prop.alternate_contact = request.POST.get('alternate_contact')

            # ---------------- UPLOADED BY ----------------
            # Usually you don't overwrite who originally uploaded it during an edit, 
            # but if you need to, keep these. Otherwise, remove them.
            prop.uploaded_by_name = request.POST.get('uploaded_by_name', prop.uploaded_by_name)
            prop.uploaded_by_email = request.POST.get('uploaded_by_email', prop.uploaded_by_email)
            prop.uploaded_by_contact = request.POST.get('uploaded_by_contact', prop.uploaded_by_contact)
            prop.uploaded_by_role = request.POST.get('uploaded_by_role', prop.uploaded_by_role)

            prop.save()

            # ---------------- IMAGE UPDATE (FIXED FOR NEW MODEL) ----------------
            images = request.FILES.getlist('property_images[]')
            current_count = prop.images.count()

            for img in images:
                if current_count < 10:
                    RentalResidentialImage.objects.create(property=prop, image=img)
                    current_count += 1

            return JsonResponse({
                'status': 'success',
                'message': 'Property updated successfully!',
                'redirect_url': reverse('rental_list') # Ensure this matches your list URL name
            })

        except Exception as e:
            return JsonResponse({
                'status': 'error',
                'message': str(e)
            }, status=400)

    # ---------- GET ----------
    return render(request, 'admin_user/rental_residential_edit.html', {
        'property': prop,
        # YOU MUST PASS THESE SO THE CHECKBOXES RENDER!
        'ameneties_obj': Ameneties_Details.objects.all(),
        'facilities_obj': Facilities_Details.objects.all()
    })




@require_POST # Security practice: only allow POST requests to delete data
def rental_residential_delete(request, pk):
    try:
        # Find the property
        prop = get_object_or_404(RentalResidentialProperty, pk=pk)
        
        # Delete it (this automatically deletes related images due to CASCADE)
        prop.delete()
        
        return JsonResponse({
            'status': 'success',
            'message': 'Property deleted successfully!'
        })
        
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=400)


##################################RESIDENTIAL RENTAL LISTING VEIW SECTION END##############################

 ######################START VIEW SECTION OF RENTAL COMMERCIAL VIEW SECTION####################################



def commercial_rental_add(request):

    admin_id = request.session.get('Admin_id')
    user_id = request.session.get('User_id')

    if not admin_id and not user_id:
        return redirect('login')

    try:
        # =============================
        # GET USER DETAILS
        # =============================
        if admin_id:
            admin = Admin_Login.objects.get(id=admin_id)
            uploader_name = admin.name
            uploader_email = admin.email
            uploader_phone = admin.phone
            uploader_role = admin.role

        else:
            user = User_Details.objects.get(id=user_id)
            uploader_name = user.name
            uploader_email = user.email
            uploader_phone = user.phone
            uploader_role = user.role

        # =============================
        # HANDLE POST
        # =============================
        if request.method == "POST":

            # ✅ FIXED: Now grabbing nearby_facilities[] to match the HTML update and DB model
            amenities_list = request.POST.getlist('amenities[]')
            facilities_list = request.POST.getlist('nearby_facilities[]')

            # DEBUG (optional)
            # print("POST:", request.POST)
            # print("FILES:", request.FILES)

            prop = CommercialRentalProperty.objects.create(

                property_type=request.POST.get('property_type'),
                city=request.POST.get('city'),
                area_locality=request.POST.get('area_locality'),
                property_address=request.POST.get('property_address'),
                building_name=request.POST.get('building_name'),

                possession_status=request.POST.get('possession_status'),
                available_from=request.POST.get('available_from') or None,
                age_of_property=request.POST.get('age_of_property'),

                zone_type=request.POST.get('zone_type'),
                location_hub=request.POST.get('location_hub'),

                property_condition=request.POST.get('property_condition'),
                ownership_type=request.POST.get('ownership_type'),
                construction_status=request.POST.get('construction_status'),

                builtup_area=request.POST.get('builtup_area') or 0,
                carpet_area=request.POST.get('carpet_area') or None,
                expected_rent=request.POST.get('expected_rent') or 0,

                security_deposit=request.POST.get('security_deposit') or None,
                maintenance_charges=request.POST.get('maintenance_charges') or None,

                # ✅ FIXED: Explicitly handle the 'Yes'/'No' Radio buttons from the form
                negotiable=True if request.POST.get('negotiable') == 'Yes' else False,

                brokerage=request.POST.get('brokerage'),
                brokerage_percentage=request.POST.get('brokerage_percentage'),
                manual_brokerage=request.POST.get('manual_brokerage'),

                # ✅ FIXED: HTML checkboxes send 'on' if checked, None if unchecked
                dg_ups_included=True if request.POST.get('dg_ups_included') == 'on' else False,
                electricity_included=True if request.POST.get('electricity_included') == 'on' else False,
                water_included=True if request.POST.get('water_included') == 'on' else False,

                lockin_period=request.POST.get('lockin_period') or None,
                rent_increase=request.POST.get('rent_increase') or None,

                total_floors=request.POST.get('total_floors') or None,
                your_floor=request.POST.get('your_floor') or None,
                staircases=request.POST.get('staircases') or None,

                passenger_lifts=request.POST.get('passenger_lifts') or 0,
                service_lifts=request.POST.get('service_lifts') or 0,
                private_parking=request.POST.get('private_parking') or 0,

                min_seats=request.POST.get('min_seats') or None,
                max_seats=request.POST.get('max_seats') or None,
                cabins=request.POST.get('cabins') or None,
                meeting_rooms=request.POST.get('meeting_rooms') or None,

                private_washroom=request.POST.get('private_washroom') or 0,
                public_washroom=request.POST.get('public_washroom') or 0,

                flooring_type=request.POST.get('flooring_type'),

                # Assign the properly fetched JSON arrays
                amenities=amenities_list,
                nearby_facilities=facilities_list,

                floor_plan=request.FILES.get('floor_plan'),
                video=request.FILES.get('video'),

                owner_name=request.POST.get('owner_name'),
                contact_number=request.POST.get('contact_number'),
                email=request.POST.get('email'),
                alternate_contact=request.POST.get('alternate_contact'),

                uploaded_by_name=uploader_name,
                uploaded_by_email=uploader_email,
                uploaded_by_contact=uploader_phone,
                uploaded_by_role=uploader_role,
            )

            # =============================
            # SAVE IMAGES
            # =============================
            images = request.FILES.getlist('property_images[]')

            for i, img in enumerate(images):
                if i >= 10:
                    break

                CommercialRentalPropertyImage.objects.create(
                    property=prop,
                    image=img
                )

            return JsonResponse({
                "status": "success",
                "message": "Commercial Property Added Successfully"
            })

    except Exception as e:
        print("ERROR:", str(e))
        traceback.print_exc()

        return JsonResponse({
            "status": "error",
            "message": str(e)
        })

    return render(request, 'admin_user/Reports/Rental/commercial_list.html')


def _get_admin(request):
    sid = request.session.get('Admin_id')
    if not sid:
        return None, None
    try:
        return sid, Admin_Login.objects.get(id=sid)
    except Admin_Login.DoesNotExist:
        return None, None

def _to_int(val):
    try:
        return int(val) if val not in (None, '') else None
    except:
        return None

def _to_float(val):
    try:
        return float(val) if val not in (None, '') else None
    except:
        return None

def _to_bool(val):
    return str(val).lower() in ['true', '1', 'yes']

def _to_date(val):
    if not val:
        return None
    try:
        return datetime.strptime(val, "%Y-%m-%d").date()
    except:
        return None

# ─────────────────────────────
# VIEW PROPERTY
def commercial_view(request, pk):
    sid, admin_obj = _get_admin(request)
    if not sid:
        return render(request, 'home_page/Adminlogin.html')

    prop = get_object_or_404(CommercialRentalProperty, pk=pk)

    return render(request, 'admin_user/Reports/Rental/commercial_detail.html', {
        'admin_obj': admin_obj,
        'prop': prop,
    })
# ─────────────────────────────




def commercial_edit(request, pk):
    sid, admin_obj = _get_admin(request)
    if not sid:
        return render(request, 'home_page/Adminlogin.html')

    prop = get_object_or_404(CommercialRentalProperty, pk=pk)

    if request.method == 'POST':
        try:
            p = request.POST

            # BASIC
            prop.property_type = p.get('property_type')
            prop.city = p.get('city')
            prop.area_locality = p.get('area_locality')
            prop.property_address = p.get('property_address')
            prop.building_name = p.get('building_name')

            prop.possession_status = p.get('possession_status')
            prop.available_from = _to_date(p.get('available_from'))
            prop.age_of_property = p.get('age_of_property')

            prop.zone_type = p.get('zone_type')
            prop.location_hub = p.get('location_hub')

            prop.property_condition = p.get('property_condition')
            prop.ownership_type = p.get('ownership_type')
            prop.construction_status = p.get('construction_status') # Added missing field

            # AREA
            prop.builtup_area = _to_int(p.get('builtup_area')) or 0
            prop.carpet_area = _to_int(p.get('carpet_area'))
            prop.expected_rent = _to_int(p.get('expected_rent')) or 0

            prop.security_deposit = _to_int(p.get('security_deposit'))
            prop.maintenance_charges = _to_int(p.get('maintenance_charges'))

            # ✅ FIXED: Radio buttons send 'Yes' or 'No'
            prop.negotiable = True if p.get('negotiable') == 'Yes' else False

            # BROKERAGE
            prop.brokerage = p.get('brokerage')
            prop.brokerage_percentage = p.get('brokerage_percentage')
            prop.manual_brokerage = p.get('manual_brokerage')

            # UTILITIES - ✅ FIXED: Toggle switches send 'on' or None
            prop.dg_ups_included = True if p.get('dg_ups_included') == 'on' else False
            prop.electricity_included = True if p.get('electricity_included') == 'on' else False
            prop.water_included = True if p.get('water_included') == 'on' else False

            prop.lockin_period = _to_int(p.get('lockin_period'))
            prop.rent_increase = _to_float(p.get('rent_increase'))

            # BUILDING
            prop.total_floors = _to_int(p.get('total_floors'))
            prop.your_floor = _to_int(p.get('your_floor'))
            prop.staircases = _to_int(p.get('staircases'))

            prop.passenger_lifts = _to_int(p.get('passenger_lifts')) or 0
            prop.service_lifts = _to_int(p.get('service_lifts')) or 0
            prop.private_parking = _to_int(p.get('private_parking')) or 0

            # OFFICE
            prop.min_seats = _to_int(p.get('min_seats'))
            prop.max_seats = _to_int(p.get('max_seats'))
            prop.cabins = _to_int(p.get('cabins'))
            prop.meeting_rooms = _to_int(p.get('meeting_rooms'))

            prop.private_washroom = _to_int(p.get('private_washroom')) or 0
            prop.public_washroom = _to_int(p.get('public_washroom')) or 0

            prop.flooring_type = p.get('flooring_type')

            # ✅ JSON FIELDS (FIXED names to match HTML)
            prop.amenities = request.POST.getlist('amenities[]')
            prop.nearby_facilities = request.POST.getlist('nearby_facilities[]')

            # OWNER
            prop.owner_name = p.get('owner_name')
            prop.contact_number = p.get('contact_number')
            prop.email = p.get('email')
            prop.alternate_contact = p.get('alternate_contact')

            # UPLOADER (Usually kept unchanged on edit, but updating if provided)
            prop.uploaded_by_name = p.get('uploaded_by_name', prop.uploaded_by_name)
            prop.uploaded_by_email = p.get('uploaded_by_email', prop.uploaded_by_email)
            prop.uploaded_by_contact = p.get('uploaded_by_contact', prop.uploaded_by_contact)
            prop.uploaded_by_role = p.get('uploaded_by_role', prop.uploaded_by_role)

            # MEDIA
            if 'floor_plan' in request.FILES:
                prop.floor_plan = request.FILES['floor_plan']

            if 'video' in request.FILES:
                prop.video = request.FILES['video']

            prop.save()

            # ✅ MULTIPLE IMAGES SAVE (FIXED name to match HTML)
            images = request.FILES.getlist('property_images[]')
            
            # Count existing images to prevent going over 10
            current_count = prop.images.count()
            
            for img in images:
                if current_count < 10:
                    CommercialRentalPropertyImage.objects.create(
                        property=prop,
                        image=img
                    )
                    current_count += 1

            # ✅ FIXED: Return JsonResponse for SweetAlert2
            return JsonResponse({
                'status': 'success',
                'message': 'Property updated successfully!',
                'redirect_url': reverse('commercial_list') # Redirects safely via JS
            })

        except Exception as e:
            return JsonResponse({
                'status': 'error',
                'message': str(e)
            }, status=400)

    # ---------- GET REQUEST ----------
    return render(request, 'admin_user/commercial_edit.html', {
        'admin_obj': admin_obj,
        'prop': prop,
        # ✅ VERY IMPORTANT: You must pass these so the checkboxes render!
        'ameneties_obj': Ameneties_Details.objects.all(),
        'facilities_obj': Facilities_Details.objects.all()
    })



# ─────────────────────────────
# DELETE
@require_POST
def commercial_delete(request, pk):
    sid, _ = _get_admin(request)
    if not sid:
        return JsonResponse({'status': 'error'}, status=401)

    prop = get_object_or_404(CommercialRentalProperty, pk=pk)
    prop.delete()

    return JsonResponse({'status': 'success'})











def _bool(val):
    # Converts "Yes", "True", "1" from Excel to Python True
    if str(val).strip().lower() in ['yes', 'true', '1', 'y']:
        return True
    return False

# ==========================================
# 2. EXACT DB SEQUENCE MAPPING (50 FIELDS)
# ==========================================
COMMERCIAL_COLUMN_MAP = [
    # BASIC (1-5)
    ("property_type", "property_type", _str),
    ("city", "city", _str),
    ("area_locality", "area_locality", _str),
    ("property_address", "property_address", _str),
    ("building_name", "building_name", _str),

    # AVAILABILITY & CONDITION (6-13)
    ("possession_status", "possession_status", _str),
    ("available_from", "available_from", _date),
    ("age_of_property", "age_of_property", _str),
    ("zone_type", "zone_type", _str),
    ("location_hub", "location_hub", _str),
    ("property_condition", "property_condition", _str),
    ("ownership_type", "ownership_type", _str),
    ("construction_status", "construction_status", _str),

    # AREA & PRICING (14-18)
    ("builtup_area", "builtup_area", _int),
    ("carpet_area", "carpet_area", _int),
    ("expected_rent", "expected_rent", _int),
    ("security_deposit", "security_deposit", _int),
    ("maintenance_charges", "maintenance_charges", _int),

    # NEGOTIABLE & BROKERAGE (19-22) - ✅ Fixed with _bool
    ("negotiable", "negotiable", _bool),
    ("brokerage", "brokerage", _str),
    ("brokerage_percentage", "brokerage_percentage", _str),
    ("manual_brokerage", "manual_brokerage", _str),

    # UTILITIES (23-27) - ✅ Fixed with _bool
    ("dg_ups_included", "dg_ups_included", _bool),
    ("electricity_included", "electricity_included", _bool),
    ("water_included", "water_included", _bool),
    ("lockin_period", "lockin_period", _int),
    ("rent_increase", "rent_increase", _float),

    # BUILDING DETAILS (28-33)
    ("total_floors", "total_floors", _int),
    ("your_floor", "your_floor", _int),
    ("staircases", "staircases", _int),
    ("passenger_lifts", "passenger_lifts", _int),
    ("service_lifts", "service_lifts", _int),
    ("private_parking", "private_parking", _int),

    # OFFICE DETAILS (34-40)
    ("min_seats", "min_seats", _int),
    ("max_seats", "max_seats", _int),
    ("cabins", "cabins", _int),
    ("meeting_rooms", "meeting_rooms", _int),
    ("private_washroom", "private_washroom", _int),
    ("public_washroom", "public_washroom", _int),
    ("flooring_type", "flooring_type", _str),

    # JSON LISTS (41-42)
    ("amenities", "amenities", lambda v: [x.strip() for x in str(v).split(",")] if v else []),
    ("nearby_facilities", "nearby_facilities", lambda v: [x.strip() for x in str(v).split(",")] if v else []),

    # OWNER DETAILS (43-46)
    ("owner_name", "owner_name", _str),
    ("contact_number", "contact_number", _str),
    ("email", "email", _str),
    ("alternate_contact", "alternate_contact", _str),

    # UPLOADER DETAILS (47-50)
    ("uploaded_by_name", "uploaded_by_name", _str),
    ("uploaded_by_email", "uploaded_by_email", _str),
    ("uploaded_by_contact", "uploaded_by_contact", _str),
    ("uploaded_by_role", "uploaded_by_role", _str),
]


# ==========================================
# 3. IMPORT VIEW
# ==========================================
@require_POST
def import_commercial_excel(request):
    file = request.FILES.get("commercial_file")

    if not file:
        return JsonResponse({"status": "error", "message": "No file uploaded"}, status=400)

    wb = openpyxl.load_workbook(file, data_only=True)
    ws = wb.active

    headers = {}
    for i, cell in enumerate(ws[1], 1):
        if cell.value:
            headers[str(cell.value).strip()] = i

    missing = [col[0] for col in COMMERCIAL_COLUMN_MAP if col[0] not in headers]
    if missing:
        return JsonResponse({"status": "error", "message": f"Missing: {', '.join(missing)}"})

    created = 0
    errors = []

    for row_idx, row in enumerate(ws.iter_rows(min_row=2, values_only=True), start=2):
        if not any(row):
            continue

        data = {}

        for excel_col, model_field, converter in COMMERCIAL_COLUMN_MAP:
            idx = headers[excel_col] - 1
            raw = row[idx] if idx < len(row) else None

            try:
                data[model_field] = converter(raw)
            except Exception as e:
                errors.append(f"Row {row_idx} {excel_col}: {e}")

        # REQUIRED DEFAULTS
        data.setdefault("property_type", "office-space")
        data.setdefault("city", "")
        data.setdefault("area_locality", "")
        data.setdefault("property_address", "")
        data.setdefault("building_name", "")
        data.setdefault("possession_status", "ready-to-move")
        data.setdefault("age_of_property", "0-1")
        data.setdefault("property_condition", "bare-shell")
        data.setdefault("ownership_type", "freehold")
        data.setdefault("builtup_area", 0)
        data.setdefault("expected_rent", 0)
        data.setdefault("owner_name", "")
        data.setdefault("contact_number", "")
        data.setdefault("email", "")

        try:
            CommercialRentalProperty.objects.create(**data)
            created += 1
        except Exception as e:
            errors.append(f"Row {row_idx}: {e}")

    wb.close()

    return JsonResponse({
        "status": "success",
        "message": f"{created} records imported",
        "errors": errors
    })


# ==========================================
# 4. DOWNLOAD TEMPLATE VIEW
# ==========================================
def download_commercial_rental__template(request):
    wb = Workbook()
    ws = wb.active
    ws.title = "Commercial"

    columns = [col[0] for col in COMMERCIAL_COLUMN_MAP]

    # HEADER
    for i, col in enumerate(columns, 1):
        ws.cell(row=1, column=i, value=col)

    # EXACT SAMPLE DATA - MUST MATCH THE 50 COLUMNS ABOVE
    sample = [
        # BASIC
        "office-space", "Nagpur", "Sitabuldi", "Main Road", "ABC Tower",
        # AVAILABILITY
        "ready-to-move", "2026-01-01", "0-1", "commercial", "IT Hub", "furnished", "freehold", "completed",
        # AREA & PRICING
        1200, 1000, 50000, 200000, 5000,
        # NEGOTIABLE & BROKERAGE
        "Yes", "Yes", "2%", "",
        # UTILITIES & LOCKIN
        "Yes", "Yes", "Yes", 12, 5.0,
        # BUILDING
        10, 3, 2, 2, 1, 3,
        # OFFICE
        10, 50, 5, 2, 2, 3, "vitrified tiles",
        # JSON ARRAYS
        "parking,ac,cctv,wifi", "metro,bus stop,bank",
        # OWNER
        "John Doe", "9876543210", "john@mail.com", "",
        # UPLOADER
        "Admin", "admin@mail.com", "9999999999", "Manager"
    ]

    # Write sample row 2
    for i, val in enumerate(sample, 1):
        ws.cell(row=2, column=i, value=val)

    # Bold headers
    for col in range(1, len(columns) + 1):
        ws.cell(row=1, column=col).font = Font(bold=True)

    buffer = io.BytesIO()
    wb.save(buffer)
    buffer.seek(0)

    return HttpResponse(
        buffer,
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={'Content-Disposition': 'attachment; filename="commercial_template.xlsx"'}
    )


from django.db.models import Sum, Count





def commercial_list(request):
    session_id = request.session.get('Admin_id')
    if not session_id:
        return render(request, 'home_page/Adminlogin.html')

    admin_obj = Admin_Login.objects.get(id=session_id)
    search_query = request.GET.get('search', '').strip()

    properties = CommercialRentalProperty.objects.all().order_by('-id')

    # SEARCH
    if search_query:
        properties = properties.filter(
            Q(property_type__icontains=search_query) |
            Q(city__icontains=search_query) |
            Q(area_locality__icontains=search_query) |
            Q(owner_name__icontains=search_query) |
            Q(possession_status__icontains=search_query)
        )

    # =========================
    # 📊 DASHBOARD STATS
    # =========================
    total_properties = properties.count()

    residential_count = properties.filter(property_type__icontains="residential").count()
    commercial_count = properties.filter(property_type__icontains="commercial").count()
    pg_count = properties.filter(property_type__icontains="pg").count()

    active_listings = properties.filter(possession_status__icontains="available").count()

    monthly_revenue = properties.aggregate(
        total=Sum('expected_rent')
    )['total'] or 0

    total_tenants = properties.count() * 1  # (placeholder logic)

    collection_rate = 95  # you can replace with payment model later
    pending_payments = 3

    maintenance_req = properties.filter(maintenance_charges__gt=0).count()

    # PIE CHART DATA
    pie_data = {
        "Residential": residential_count,
        "Commercial": commercial_count,
        "PG/Co-living": pg_count
    }

    # ── Fetch unique uploaded file names for the Bulk Delete modal ──
    try:
        # Note: Replace 'upload_file_name' with your actual model field name if different
        uploaded_files = properties.exclude(
            upload_file_name__isnull=True
        ).exclude(upload_file_name='').values_list('upload_file_name', flat=True).distinct()
    except Exception:
        uploaded_files = []

    paginator = Paginator(properties, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'admin_user/Reports/Rental/commercial_list.html', {
        'admin_obj': admin_obj,
        'page_obj': page_obj,
        'search_query': search_query,
        'total_count': total_properties,

        # ✅ STATS
        'total_properties': total_properties,
        'residential_count': residential_count,
        'commercial_count': commercial_count,
        'pg_count': pg_count,
        'active_listings': active_listings,
        'monthly_revenue': monthly_revenue,
        'total_tenants': total_tenants,
        'collection_rate': collection_rate,
        'pending_payments': pending_payments,
        'maintenance_req': maintenance_req,
        'pie_data': pie_data,
        'uploaded_files': uploaded_files, # Passed files to template here
    })


def commercial_bulk_delete(request):
    """Handles Advanced Bulk Deletions for Commercial Properties."""
    if request.method != 'POST':
        return JsonResponse({'status': 'error', 'message': 'Invalid request method.'})
        
    session_id = request.session.get('Admin_id')
    if not session_id:
        return JsonResponse({'status': 'error', 'message': 'Unauthorized access.'})

    try:
        data = json.loads(request.body)
        delete_type = data.get('delete_type')
        properties = CommercialRentalProperty.objects.all()
        
        if delete_type == 'delete_all':
            count = properties.count()
            properties.delete()
            return JsonResponse({'status': 'success', 'message': f'Successfully deleted ALL {count} properties.'})
            
        elif delete_type == 'current_page':
            page_ids = data.get('page_ids', [])
            target_props = properties.filter(id__in=page_ids)
            count = target_props.count()
            target_props.delete()
            return JsonResponse({'status': 'success', 'message': f'Successfully deleted {count} properties from current page.'})
            
        elif delete_type == 'date_range':
            from_date = data.get('from_date')
            to_date = data.get('to_date')
            # Using created_at for accurate date ranges, change to available_from if needed
            target_props = properties.filter(created_at__range=[from_date, to_date])
            count = target_props.count()
            target_props.delete()
            return JsonResponse({'status': 'success', 'message': f'Successfully deleted {count} properties in date range.'})
            
        elif delete_type == 'latest_month':
            thirty_days_ago = timezone.now() - timedelta(days=30)
            target_props = properties.filter(created_at__gte=thirty_days_ago)
            count = target_props.count()
            target_props.delete()
            return JsonResponse({'status': 'success', 'message': f'Successfully deleted {count} properties from the last 30 days.'})
            
        elif delete_type == 'old_data':
            six_months_ago = timezone.now() - timedelta(days=180)
            target_props = properties.filter(created_at__lt=six_months_ago)
            count = target_props.count()
            target_props.delete()
            return JsonResponse({'status': 'success', 'message': f'Successfully deleted {count} older properties.'})
            
        elif delete_type == 'by_uploader':
            uploader = data.get('uploader_text', '')
            target_props = properties.filter(
                Q(uploaded_by_name__icontains=uploader) | 
                Q(uploaded_by_email__icontains=uploader) |
                Q(uploaded_by_role__icontains=uploader)
            )
            count = target_props.count()
            target_props.delete()
            return JsonResponse({'status': 'success', 'message': f'Successfully deleted {count} properties uploaded by {uploader}.'})

        elif delete_type == 'by_file':
            file_name = data.get('file_name', '')
            # Replace 'upload_file_name' with your exact database field name for tracking files
            target_props = properties.filter(upload_file_name=file_name) 
            count = target_props.count()
            if count == 0:
                return JsonResponse({'status': 'error', 'message': f'No properties found for file: {file_name}'})
            target_props.delete()
            return JsonResponse({'status': 'success', 'message': f'Successfully deleted {count} properties from {file_name}.'})
            
        else:
            return JsonResponse({'status': 'error', 'message': 'Unknown delete criteria.'})

    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)})

#######################END VIEW SECTION RENTAL COMMERCIAL PROPERTY##################################



###############################START VIEW SECTION OF RENTAL PG_COLIVING PROPERTY###############################



@csrf_exempt
def add_pg(request):
    if request.method == "POST":

        def get_list(name):
            return ",".join(request.POST.getlist(name))

        # ✅ ROOM LOGIC (MULTIPLE → TEXT)
        room_types = request.POST.getlist("room_type[]")
        beds = request.POST.getlist("room_beds[]")
        rents = request.POST.getlist("room_rent[]")
        deposits = request.POST.getlist("room_deposit[]")
        brokerages = request.POST.getlist("room_brokerage[]")
        brokerage_percents = request.POST.getlist("room_brokerage_percent[]")
        manual_brokerages = request.POST.getlist("room_manual_brokerage[]")

        room_data = []

        for i in range(len(room_types)):
            room_data.append(
                f"{room_types[i]}|{beds[i]}|{rents[i]}|{deposits[i]}|"
                f"{brokerages[i] if i < len(brokerages) else ''}|"
                f"{brokerage_percents[i] if i < len(brokerage_percents) else ''}|"
                f"{manual_brokerages[i] if i < len(manual_brokerages) else ''}"
            )

        room_details = ",".join(room_data)

        # ✅ CREATE PROPERTY
        pg = PGColivingProperty.objects.create(

            # BASIC
            city=request.POST.get("city"),
            building_name=request.POST.get("building_name"),   # ✅ FIXED
            locality=request.POST.get("locality"),
            pg_name=request.POST.get("pg_name"),
            property_address=request.POST.get("property_address"),  # ✅ FIXED

            total_beds=request.POST.get("total_beds"),

            pg_for=request.POST.get("pg_for"),
            furnishing_type=request.POST.get("furnishing_type"),
            sharing_type=request.POST.get("sharing_type"),
            best_suited_for=request.POST.get("best_suited_for"),

            # ✅ ROOM STORED AS TEXT
            room_details=room_details,

            # FACILITIES
            common_area=get_list("common_area[]"),
            amenities=get_list("amenities[]"),
            nearby_facilities=get_list("facilities[]"),

            # MEALS
            meals_available=True if request.POST.get("meals_available") else False,
            meal_offerings=request.POST.get("meal_offerings"),
            meal_speciality=request.POST.get("meal_speciality"),

            # RULES
            notice_period=request.POST.get("notice_period") or None,
            lockin_period=request.POST.get("lockin_period") or None,
            minimum_stay=request.POST.get("minimum_stay"),   # ✅ FIXED
            available_from=request.POST.get("available_from"),

            property_managed_by=request.POST.get("property_managed_by"),  # ✅ FIXED
            manager_stays=True if request.POST.get("manager_stays") == "true" else False,  # ✅ FIXED

            non_veg_allowed=True if request.POST.get("non_veg_allowed") else False,  # ✅ FIXED
            opposite_sex_allowed=True if request.POST.get("opposite_sex_allowed") else False,
            any_time_allowed=True if request.POST.get("any_time_allowed") else False,  # ✅ FIXED
            visitors_allowed=True if request.POST.get("visitors_allowed") else False,
            guardian_allowed=True if request.POST.get("guardian_allowed") else False,
            drinking_allowed=True if request.POST.get("drinking_allowed") else False,
            smoking_allowed=True if request.POST.get("smoking_allowed") else False,

            # MEDIA
            floor_plan=request.FILES.get("floor_plan"),
            video=request.FILES.get("video"),  # ✅ FIXED

            # CONTACT
            owner_name=request.POST.get("owner_name"),
            contact_number=request.POST.get("contact_number"),
            email=request.POST.get("email"),
            alternate_contact=request.POST.get("alternate_contact"),

            uploaded_by_name=request.POST.get("uploaded_by_name"),
            uploaded_by_email=request.POST.get("uploaded_by_email"),
            uploaded_by_contact=request.POST.get("uploaded_by_contact"),
            uploaded_by_role=request.POST.get("uploaded_by_role"),
        )

        # ✅ IMAGE SAVE (MIN 3 MAX 10)
        images = request.FILES.getlist("property_images[]")

        if len(images) < 3 or len(images) > 10:
            return JsonResponse({
                "status": "error",
                "message": "Upload minimum 3 and maximum 10 images"
            })

        for img in images:
            PGPropertyImage.objects.create(property=pg, image=img)

        return JsonResponse({
            "status": "success",
            "message": "PG Added Successfully"
        })




def _str(val):
    if val is None:
        return None
    s = str(val).strip()
    return s if s else None

def _int(val):
    try:
        return int(float(str(val).strip()))
    except:
        return None

def _bool(val):
    if isinstance(val, bool):
        return val
    if val is None:
        return False
    return str(val).strip().lower() in ("true","1","yes")

def _date(val):
    if val is None:
        return None
    if isinstance(val, (date, datetime)):
        return val.date() if isinstance(val, datetime) else val
    for fmt in ("%Y-%m-%d","%d-%m-%Y","%d/%m/%Y"):
        try:
            return datetime.strptime(str(val).strip(), fmt).date()
        except:
            continue
    return None




def pg_list(request):
    session_id = request.session.get('Admin_id')
    if not session_id:
        return render(request, 'home_page/Adminlogin.html')

    search = request.GET.get('search', '')
    qs = PGColivingProperty.objects.all().order_by('-id')

    if search:
        qs = qs.filter(
            Q(pg_name__icontains=search) |
            Q(city__icontains=search) |
            Q(locality__icontains=search) |
            Q(owner_name__icontains=search)
        )

    if request.GET.get('download') == 'csv':
        res = HttpResponse(content_type='text/csv')
        res['Content-Disposition'] = 'attachment; filename="pg.csv"'
        w = csv.writer(res)
        w.writerow(["PG", "City", "Total Beds", "Owner", "Contact"])
        for p in qs:
            w.writerow([p.pg_name, p.city, p.total_beds, p.owner_name, p.contact_number])
        return res

    # ── Fetch unique uploaded file names for the Bulk Delete modal ──
    try:
        # Note: Replace 'upload_file_name' with your actual model field name if different
        uploaded_files = PGColivingProperty.objects.exclude(
            upload_file_name__isnull=True
        ).exclude(upload_file_name='').values_list('upload_file_name', flat=True).distinct()
    except Exception:
        uploaded_files = []

    paginator = Paginator(qs, 10)
    page = paginator.get_page(request.GET.get('page'))

    # ==========================================
    # DASHBOARD AGGREGATION LOGIC
    # ==========================================
    
    # 1. Get counts for property types
    pg_count = PGColivingProperty.objects.count()
    
    try:
        # Assuming you have these models imported
        commercial_count = CommercialRentalProperty.objects.count()
        # residential_count = ResidentialRentalProperty.objects.count() # Update with your actual model name
        residential_count = 32 # Placeholder: replace with actual query
    except NameError:
        commercial_count = 0
        residential_count = 0

    total_properties = pg_count + commercial_count + residential_count

    # 2. Get PG Specific Stats
    total_pg_beds = PGColivingProperty.objects.aggregate(total=Sum('total_beds'))['total'] or 0
    
    # Pack data for charts (Converting to JSON for safe Javascript usage)
    chart_data = {
        "property_distribution": [residential_count, commercial_count, pg_count],
        "months": ["Jan", "Feb", "Mar", "Apr", "May", "Jun"],
        "rental_income": [120000, 150000, 180000, 210000, 250000, 300000], # Mock data: replace with real monthly aggregation
    }

    return render(request, 'admin_user/Reports/Rental/pg_list.html', {
        "page_obj": page,
        "search": search,
        
        # Pass Stats to template
        "total_properties": total_properties,
        "residential_count": residential_count,
        "commercial_count": commercial_count,
        "pg_count": pg_count,
        "total_pg_beds": total_pg_beds,
        "active_listings": total_properties, # Assuming all are active for now
        "chart_data_json": json.dumps(chart_data), # Send secure JSON to JS
        "uploaded_files": uploaded_files, # Passed files to template here
    })


def pg_bulk_delete(request):
    """Handles Advanced Bulk Deletions for PG / Co-living Properties."""
    if request.method != 'POST':
        return JsonResponse({'status': 'error', 'message': 'Invalid request method.'})
        
    session_id = request.session.get('Admin_id')
    if not session_id:
        return JsonResponse({'status': 'error', 'message': 'Unauthorized access.'})

    try:
        data = json.loads(request.body)
        delete_type = data.get('delete_type')
        properties = PGColivingProperty.objects.all()
        
        if delete_type == 'delete_all':
            count = properties.count()
            properties.delete()
            return JsonResponse({'status': 'success', 'message': f'Successfully deleted ALL {count} PG properties.'})
            
        elif delete_type == 'current_page':
            page_ids = data.get('page_ids', [])
            target_props = properties.filter(id__in=page_ids)
            count = target_props.count()
            target_props.delete()
            return JsonResponse({'status': 'success', 'message': f'Successfully deleted {count} PG properties from current page.'})
            
        elif delete_type == 'date_range':
            from_date = data.get('from_date')
            to_date = data.get('to_date')
            # Adjust 'created_at' if your model uses a different date field
            target_props = properties.filter(created_at__range=[from_date, to_date])
            count = target_props.count()
            target_props.delete()
            return JsonResponse({'status': 'success', 'message': f'Successfully deleted {count} PG properties in date range.'})
            
        elif delete_type == 'latest_month':
            thirty_days_ago = timezone.now() - timedelta(days=30)
            target_props = properties.filter(created_at__gte=thirty_days_ago)
            count = target_props.count()
            target_props.delete()
            return JsonResponse({'status': 'success', 'message': f'Successfully deleted {count} PG properties from the last 30 days.'})
            
        elif delete_type == 'old_data':
            six_months_ago = timezone.now() - timedelta(days=180)
            target_props = properties.filter(created_at__lt=six_months_ago)
            count = target_props.count()
            target_props.delete()
            return JsonResponse({'status': 'success', 'message': f'Successfully deleted {count} older PG properties.'})
            
        elif delete_type == 'by_uploader':
            uploader = data.get('uploader_text', '')
            target_props = properties.filter(
                Q(owner_name__icontains=uploader) | # Using owner_name as fallback if uploaded_by isn't present
                Q(email__icontains=uploader) 
                # Add Q(uploaded_by_name__icontains=uploader) if your PG model has this field
            )
            count = target_props.count()
            target_props.delete()
            return JsonResponse({'status': 'success', 'message': f'Successfully deleted {count} PG properties uploaded by {uploader}.'})

        elif delete_type == 'by_file':
            file_name = data.get('file_name', '')
            # Replace 'upload_file_name' with your exact database field name
            target_props = properties.filter(upload_file_name=file_name) 
            count = target_props.count()
            if count == 0:
                return JsonResponse({'status': 'error', 'message': f'No properties found for file: {file_name}'})
            target_props.delete()
            return JsonResponse({'status': 'success', 'message': f'Successfully deleted {count} PG properties from {file_name}.'})
            
        else:
            return JsonResponse({'status': 'error', 'message': 'Unknown delete criteria.'})

    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)})





COLUMN_MAP = [

    ("city","city",_str),
    ("building_name","building_name",_str),
    ("locality","locality",_str),
    ("pg_name","pg_name",_str),
    ("property_address","property_address",_str),
    ("total_beds","total_beds",_int),
    ("pg_for","pg_for",_str),
    ("furnishing_type","furnishing_type",_str),
    ("best_suited_for","best_suited_for",_str),

    ("room_details","room_details",_str),

    ("common_area","common_area",_str),
    ("amenities","amenities",_str),
    ("nearby_facilities","nearby_facilities",_str),

    ("meals_available","meals_available",_bool),
    ("meal_offerings","meal_offerings",_str),
    ("meal_speciality","meal_speciality",_str),

    ("notice_period","notice_period",_int),
    ("lockin_period","lockin_period",_int),
    ("minimum_stay","minimum_stay",_int),
    ("available_from","available_from",_date),

    ("property_managed_by","property_managed_by",_str),
    ("manager_stays","manager_stays",_bool),

    ("non_veg_allowed","non_veg_allowed",_bool),
    ("opposite_sex_allowed","opposite_sex_allowed",_bool),
    ("any_time_allowed","any_time_allowed",_bool),
    ("visitors_allowed","visitors_allowed",_bool),
    ("guardian_allowed","guardian_allowed",_bool),
    ("drinking_allowed","drinking_allowed",_bool),
    ("smoking_allowed","smoking_allowed",_bool),

    ("owner_name","owner_name",_str),
    ("contact_number","contact_number",_str),
    ("email","email",_str),
    ("alternate_contact","alternate_contact",_str),
]

@csrf_exempt
@require_POST
def import_pg_excel(request):

    if not request.session.get('Admin_id'):
        return JsonResponse({'status':'error','message':'Unauthorized'}, status=401)

    file = request.FILES.get('file')
    if not file:
        return JsonResponse({'status':'error','message':'No file uploaded'}, status=400)

    try:
        wb = openpyxl.load_workbook(io.BytesIO(file.read()), data_only=True)
        ws = wb.active
    except Exception as e:
        return JsonResponse({'status':'error','message':f'Invalid Excel file: {e}'}, status=400)

    headers = [str(c).strip().lower() if c else "" for c in next(ws.iter_rows(values_only=True))]
    col_index = {h:i for i,h in enumerate(headers)}

    REQUIRED_FIELDS = [
        "city","locality","pg_name","property_address",
        "total_beds","pg_for","furnishing_type",
        "room_details",
        "minimum_stay","available_from",
        "owner_name","contact_number","email"
    ]

    imported = 0
    skipped = 0
    errors = []

    # ✅ AUTO USER (IMPORTANT)
    uploader_name = request.session.get("Admin_name", "Admin")
    uploader_email = request.session.get("Admin_email", "")
    uploader_contact = request.session.get("Admin_contact", "")
    uploader_role = "Admin"

    for row_num, row in enumerate(ws.iter_rows(min_row=2, values_only=True), start=2):

        if all(c is None or str(c).strip() == "" for c in row):
            continue

        data = {}

        for excel, field, conv in COLUMN_MAP:
            idx = col_index.get(excel)
            if idx is not None:
                try:
                    data[field] = conv(row[idx])
                except:
                    data[field] = None

        data["room_details"] = data.get("room_details") or ""

        missing_fields = [f for f in REQUIRED_FIELDS if not data.get(f)]

        if missing_fields:
            skipped += 1
            errors.append(f"Row {row_num}: Missing → {', '.join(missing_fields)}")
            continue

        try:
            pg = PGColivingProperty.objects.create(**data)

            # ✅ HERE YOU CAN SAVE UPLOADER IN SEPARATE MODEL (OPTIONAL)
            # PGUploader.objects.create(
            #     property=pg,
            #     name=uploader_name,
            #     email=uploader_email,
            #     contact=uploader_contact,
            #     role=uploader_role
            # )

            imported += 1

        except Exception as e:
            skipped += 1
            errors.append(f"Row {row_num}: {str(e)}")

    return JsonResponse({
        "status": "success",
        "imported": imported,
        "skipped": skipped,
        "errors": errors[:10],
        "message": f"{imported} imported, {skipped} skipped"
    })



def download_pg_template(request):

    if not request.session.get('Admin_id'):
        from django.shortcuts import render
        return render(request, 'home_page/Adminlogin.html')

    wb = openpyxl.Workbook()
    ws = wb.active

    headers = [
        "city","building_name","locality","pg_name","property_address",
        "total_beds","pg_for","furnishing_type","best_suited_for",
        "room_details",
        "common_area","amenities","nearby_facilities",
        "meals_available","meal_offerings","meal_speciality",
        "notice_period","lockin_period","minimum_stay","available_from",
        "property_managed_by","manager_stays",
        "non_veg_allowed","opposite_sex_allowed","any_time_allowed",
        "visitors_allowed","guardian_allowed","drinking_allowed","smoking_allowed",
        "owner_name","contact_number","email","alternate_contact",

        # KEEP BUT NOT USED
        "uploaded_by_name","uploaded_by_email","uploaded_by_contact","uploaded_by_role",
    ]

    for col, header in enumerate(headers, 1):
        ws.cell(row=1, column=col, value=header)

    sample = [
        "Nagpur","ABC Building","Dharampeth","Sunrise PG","Near Metro",
        50,"boys","fully-furnished","students",

        "single|2|5000|10000|Yes|10%|,double|4|8000|15000|No||",

        "TV,Fridge",
        "WiFi,CCTV",
        "College,Market",

        True,"Breakfast,Dinner","Veg",

        30,90,3,"2026-05-01",
        "owner",True,

        True,True,True,True,False,False,False,

        "Mr Sharma","9876543210","test@gmail.com","9999999999",

        "", "", "", ""   # ✅ EMPTY uploader fields
    ]

    for col, val in enumerate(sample, 1):
        ws.cell(row=2, column=col, value=val)

    buffer = io.BytesIO()
    wb.save(buffer)
    buffer.seek(0)

    response = HttpResponse(
        buffer.read(),
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = 'attachment; filename="pg_template.xlsx"'

    return response



@csrf_exempt
def pg_edit(request, pk):
    sid, admin_obj = _get_admin(request) # Use your standard auth check
    if not sid:
        return redirect('login') # Or your login route

    pg = get_object_or_404(PGColivingProperty, pk=pk)

    if request.method == "POST":
        try:
            def get_list(name):
                return ",".join(request.POST.getlist(name))

            # ✅ 1. ROOM LOGIC (MULTIPLE → TEXT)
            room_types = request.POST.getlist("room_type[]")
            beds = request.POST.getlist("room_beds[]")
            rents = request.POST.getlist("room_rent[]")
            deposits = request.POST.getlist("room_deposit[]")
            brokerages = request.POST.getlist("room_brokerage[]")
            brokerage_percents = request.POST.getlist("room_brokerage_percent[]")
            manual_brokerages = request.POST.getlist("room_manual_brokerage[]")

            room_data = []
            for i in range(len(room_types)):
                room_data.append(
                    f"{room_types[i]}|{beds[i]}|{rents[i]}|{deposits[i]}|"
                    f"{brokerages[i] if i < len(brokerages) else ''}|"
                    f"{brokerage_percents[i] if i < len(brokerage_percents) else ''}|"
                    f"{manual_brokerages[i] if i < len(manual_brokerages) else ''}"
                )

            pg.room_details = ",".join(room_data)

            # ✅ 2. BASIC
            pg.city = request.POST.get("city")
            pg.building_name = request.POST.get("building_name")
            pg.locality = request.POST.get("locality")
            pg.pg_name = request.POST.get("pg_name")
            pg.property_address = request.POST.get("property_address")
            pg.total_beds = request.POST.get("total_beds")

            pg.pg_for = request.POST.get("pg_for")
            pg.furnishing_type = request.POST.get("furnishing_type")
            pg.sharing_type = request.POST.get("sharing_type")
            pg.best_suited_for = request.POST.get("best_suited_for")

            # ✅ 3. FACILITIES (Lists)
            pg.common_area = get_list("common_area[]")
            pg.amenities = get_list("amenities[]")
            pg.nearby_facilities = get_list("facilities[]")

            # ✅ 4. MEALS & RULES (Booleans & Toggles)
            pg.meals_available = True if request.POST.get("meals_available") else False
            pg.meal_offerings = request.POST.get("meal_offerings")
            pg.meal_speciality = request.POST.get("meal_speciality")

            pg.notice_period = request.POST.get("notice_period") or None
            pg.lockin_period = request.POST.get("lockin_period") or None
            pg.minimum_stay = request.POST.get("minimum_stay")
            pg.available_from = request.POST.get("available_from")

            pg.property_managed_by = request.POST.get("property_managed_by")
            pg.manager_stays = True if request.POST.get("manager_stays") == "true" else False

            pg.non_veg_allowed = True if request.POST.get("non_veg_allowed") else False
            pg.opposite_sex_allowed = True if request.POST.get("opposite_sex_allowed") else False
            pg.any_time_allowed = True if request.POST.get("any_time_allowed") else False
            pg.visitors_allowed = True if request.POST.get("visitors_allowed") else False
            pg.guardian_allowed = True if request.POST.get("guardian_allowed") else False
            pg.drinking_allowed = True if request.POST.get("drinking_allowed") else False
            pg.smoking_allowed = True if request.POST.get("smoking_allowed") else False

            # ✅ 5. CONTACT
            pg.owner_name = request.POST.get("owner_name")
            pg.contact_number = request.POST.get("contact_number")
            pg.email = request.POST.get("email")
            pg.alternate_contact = request.POST.get("alternate_contact")

            # REMOVED UPLOADER FIELDS AS THEY DO NOT EXIST IN THE PG MODEL

            # ✅ 6. MEDIA
            if "floor_plan" in request.FILES:
                pg.floor_plan = request.FILES["floor_plan"]
            if "video" in request.FILES:
                pg.video = request.FILES["video"]

            pg.save()

            # ✅ 7. MULTIPLE IMAGES SAVE
            images = request.FILES.getlist("property_images[]")
            current_image_count = PGPropertyImage.objects.filter(property=pg).count()
            
            for img in images:
                if current_image_count < 10:
                    PGPropertyImage.objects.create(property=pg, image=img)
                    current_image_count += 1

            return JsonResponse({
                "status": "success",
                "message": "PG Updated Successfully",
                "redirect_url": reverse('pg_list') # Ensure 'pg_list' matches your urls.py
            })

        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)})

    # ========== GET REQUEST (LOAD FORM) ==========
    
    # Parse the custom room_details string into a list of dictionaries for the template
    parsed_rooms = []
    if pg.room_details:
        room_strings = pg.room_details.split(',')
        for rs in room_strings:
            parts = rs.split('|')
            if len(parts) >= 4:
                parsed_rooms.append({
                    'type': parts[0],
                    'beds': parts[1],
                    'rent': parts[2],
                    'deposit': parts[3],
                    'brokerage': parts[4] if len(parts) > 4 else '',
                    'brokerage_percent': parts[5] if len(parts) > 5 else '',
                    'manual_brokerage': parts[6] if len(parts) > 6 else '',
                })

    return render(request, "admin_user/Reports/Rental/pg_edit.html", {
        "admin_obj": admin_obj,
        "pg": pg,
        "parsed_rooms": parsed_rooms,
        "ameneties_obj": Ameneties_Details.objects.all(),
        "facilities_obj": Facilities_Details.objects.all(),
    })





@require_POST
def pg_coliving_delete(request, pk):
    # Check if admin/user is logged in (using your standard auth logic)
    sid, _ = _get_admin(request)
    if not sid:
        return JsonResponse({'status': 'error', 'message': 'Unauthorized'}, status=401)

    try:
        # Find the PG and delete it
        pg = get_object_or_404(PGColivingProperty, pk=pk)
        pg.delete()
        
        return JsonResponse({'status': 'success'})
        
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)})




def pg_coliving_view(request, pk):
    sid, admin_obj = _get_admin(request) # Use your standard auth check
    if not sid:
        return redirect('login')

    pg = get_object_or_404(PGColivingProperty, pk=pk)

    # 1. Parse Room Details
    parsed_rooms = []
    if pg.room_details:
        room_strings = pg.room_details.split(',')
        for rs in room_strings:
            parts = rs.split('|')
            if len(parts) >= 4:
                parsed_rooms.append({
                    'type': parts[0].title(),
                    'beds': parts[1],
                    'rent': parts[2],
                    'deposit': parts[3],
                    'brokerage': parts[4] if len(parts) > 4 else '',
                    'brokerage_percent': parts[5] if len(parts) > 5 else '',
                    'manual_brokerage': parts[6] if len(parts) > 6 else '',
                })

    # 2. Parse Comma-Separated Strings into Lists for "Chip" styling in HTML
    def split_to_list(db_string):
        return [x.strip() for x in db_string.split(',')] if db_string else []

    context = {
        'admin_obj': admin_obj,
        'pg': pg,
        'parsed_rooms': parsed_rooms,
        'pg_for_list': split_to_list(pg.pg_for),
        'sharing_type_list': split_to_list(pg.sharing_type),
        'best_suited_list': split_to_list(pg.best_suited_for),
        'common_area_list': split_to_list(pg.common_area),
        'amenities_list': split_to_list(pg.amenities),
        'facilities_list': split_to_list(pg.nearby_facilities),
        'meal_offerings_list': split_to_list(pg.meal_offerings),
        'meal_speciality_list': split_to_list(pg.meal_speciality),
    }

    return render(request, "admin_user/Reports/Rental/pg_coliving_view.html", context)

###############################END VIEW SECTION OF RENTAL PG_COLIVING PROPERTY###############################



###################START VIEW SECTION RESALE PLOT LISTING###########################



def plot_sale_add(request):
    admin_id = request.session.get('Admin_id')
    user_id = request.session.get('User_id')

    if not admin_id and not user_id:
        return redirect('login')

    try:
        # =============================
        # GET USER DETAILS
        # =============================
        if admin_id:
            admin = Admin_Login.objects.get(id=admin_id)
            uploader_name = admin.name
            uploader_email = admin.email
            uploader_phone = admin.phone
            uploader_role = admin.role
        else:
            user = User_Details.objects.get(id=user_id)
            uploader_name = user.name
            uploader_email = user.email
            uploader_phone = user.phone
            uploader_role = user.role

        # =============================
        # HANDLE POST
        # =============================
        if request.method == "POST":
            # Safely parse boolean choices
            plot_corner_val = True if request.POST.get('plot_corner') == 'yes' else False
            plot_fencing_val = True if request.POST.get('plot_fencing') == 'yes' else False
            plot_loan_val = True if request.POST.get('plot_loan') == 'yes' else False

            # Create the main property listing
            prop = PlotSaleProperty.objects.create(
                # Step 1
                plot_title=request.POST.get('plot_title'),
                plot_area=request.POST.get('plot_area') or 0,
                resale_plot_type=request.POST.get('resale_plot_type'),
                plot_road_facing=request.POST.get('plot_road_facing'),
                plot_corner=plot_corner_val,
                available_from=request.POST.get('available_from') or None,
                plot_authority=request.POST.get('plot_authority'),
                plot_fencing=plot_fencing_val,

                # Step 2
                plot_price=request.POST.get('plot_price') or 0,
                brokerage=request.POST.get('brokerage'),
                brokerage_percentage=request.POST.get('brokerage_percentage'),
                plot_ownership=request.POST.get('plot_ownership'),
                plot_loan=plot_loan_val,
                plot_loan_amount=request.POST.get('plot_loan_amount') or None,

                # Step 3
                encumbrance_cert=request.FILES.get('encumbrance_cert'),
                social_video=request.FILES.get('social_video'),

                # Step 4
                plot_city=request.POST.get('plot_city'),
                plot_locality=request.POST.get('plot_locality'),
                plot_address=request.POST.get('plot_address'),
                plot_owner_name=request.POST.get('plot_owner_name'),
                plot_owner_contact=request.POST.get('plot_owner_contact'),
                plot_owner_email=request.POST.get('plot_owner_email'),

                # Uploaded By details
                uploaded_by_name=uploader_name,
                uploaded_by_email=uploader_email,
                uploaded_by_contact=uploader_phone,
                uploaded_by_role=uploader_role,
            )

            # =============================
            # SAVE IMAGES (Max 10)
            # =============================
            images = request.FILES.getlist('property_images[]')

            for i, img in enumerate(images):
                if i >= 10:
                    break  # Stop if the user somehow bypassed the frontend limit
                
                PlotSaleImage.objects.create(
                    property=prop,
                    image=img
                )

            return JsonResponse({
                "status": "success",
                "message": "Plot Listing Added Successfully"
            })

    except Exception as e:
        print("ERROR:", str(e))
        traceback.print_exc()

        return JsonResponse({
            "status": "error",
            "message": str(e)
        })

    # Render your form page for GET requests
    return render(request, 'admin_user/Reports/Resale/plot_list.html')




def plot_sale_edit(request, id):
    admin_id = request.session.get('Admin_id')
    user_id = request.session.get('User_id')

    if not admin_id and not user_id:
        return redirect('login')

    # Fetch the existing property
    prop = get_object_or_404(PlotSaleProperty, id=id)

    if request.method == "POST":
        try:
            # Safely parse boolean choices
            plot_corner_val = True if request.POST.get('plot_corner') == 'yes' else False
            plot_fencing_val = True if request.POST.get('plot_fencing') == 'yes' else False
            plot_loan_val = True if request.POST.get('plot_loan') == 'yes' else False

            # Update the main property listing
            prop.plot_title = request.POST.get('plot_title')
            prop.plot_area = request.POST.get('plot_area') or 0
            prop.resale_plot_type = request.POST.get('resale_plot_type')
            prop.plot_road_facing = request.POST.get('plot_road_facing')
            prop.plot_corner = plot_corner_val
            prop.available_from = request.POST.get('available_from') or None
            prop.plot_authority = request.POST.get('plot_authority')
            prop.plot_fencing = plot_fencing_val

            prop.plot_price = request.POST.get('plot_price') or 0
            prop.brokerage = request.POST.get('brokerage')
            prop.brokerage_percentage = request.POST.get('brokerage_percentage')
            prop.plot_ownership = request.POST.get('plot_ownership')
            prop.plot_loan = plot_loan_val
            prop.plot_loan_amount = request.POST.get('plot_loan_amount') or None

            prop.plot_city = request.POST.get('plot_city')
            prop.plot_locality = request.POST.get('plot_locality')
            prop.plot_address = request.POST.get('plot_address')
            prop.plot_owner_name = request.POST.get('plot_owner_name')
            prop.plot_owner_contact = request.POST.get('plot_owner_contact')
            prop.plot_owner_email = request.POST.get('plot_owner_email')

            # Update files ONLY if new ones are uploaded
            if request.FILES.get('encumbrance_cert'):
                prop.encumbrance_cert = request.FILES.get('encumbrance_cert')
            if request.FILES.get('social_video'):
                prop.social_video = request.FILES.get('social_video')

            prop.save()

            # =============================
            # SAVE NEW IMAGES (Append up to 10 max)
            # =============================
            new_images = request.FILES.getlist('property_images[]')
            current_image_count = prop.images.count() # Using the related_name 'images'

            for img in new_images:
                if current_image_count >= 10:
                    break # Stop adding if we hit the 10 image limit
                PlotSaleImage.objects.create(property=prop, image=img)
                current_image_count += 1

            return JsonResponse({
                "status": "success",
                "message": "Plot Listing Updated Successfully"
            })

        except Exception as e:
            print("ERROR:", str(e))
            traceback.print_exc()
            return JsonResponse({
                "status": "error",
                "message": str(e)
            })

    # For GET requests, render the template with the existing property data
    context = {
        'prop': prop,
        # Fetching session details just for the footer 'Uploaded By' visual if needed, 
        # though you might want to show the original uploader's data. We'll pass the prop.
    }
    return render(request, 'admin_user/Reports/Resale/plot_edit.html', context)





# 1. UPDATED LIST VIEW
def plot_resale_list(request):
    session_id = request.session.get('Admin_id')
    if session_id:
        admin_obj = Admin_Login.objects.get(id=session_id)
        
        # Fetch properties newest first
        properties = PlotSaleProperty.objects.all().order_by('-created_at')
        
        # Calculate stats (optional but good for your top cards)
        total_properties = properties.count()
        active_listings = properties.filter(plot_price__gt=0).count()
        
        context = {
            'admin_obj': admin_obj,
            'properties': properties,
            'total_properties': total_properties,
            'active_listings': active_listings
        }
        return render(request, 'admin_user/Reports/Resale/plot_list.html', context)
    else:
        return render(request, 'home_page/Adminlogin.html')

# 2. GENERATE SAMPLE EXCEL TEMPLATE
def download_plot_resale_template(request):
    workbook = openpyxl.Workbook()
    sheet = workbook.active
    sheet.title = "Plot Import Template"

    # Sequence exactly matching your PlotSaleProperty model fields
    headers = [
        "Project Name",             # 0: plot_title
        "Plot Area (sq.ft)",        # 1: plot_area
        "Plot Type",                # 2: resale_plot_type (open_plot/residential_plot/commercial_plot)
        "Road Facing",              # 3: plot_road_facing (main/internal/corner)
        "Corner Plot (yes/no)",     # 4: plot_corner
        "Available From",           # 5: available_from (YYYY-MM-DD)
        "Sanctioning Authority",    # 6: plot_authority
        "Fencing Done (yes/no)",    # 7: plot_fencing
        "Expected Price",           # 8: plot_price
        "Brokerage (Yes/No)",       # 9: brokerage
        "Brokerage %",              # 10: brokerage_percentage
        "Ownership Type",           # 11: plot_ownership (freehold/leasehold)
        "Loan on Property (yes/no)",# 12: plot_loan
        "Loan Amount",              # 13: plot_loan_amount
        "City",                     # 14: plot_city
        "Locality",                 # 15: plot_locality
        "Complete Address",         # 16: plot_address
        "Owner Name",               # 17: plot_owner_name
        "Owner Contact",            # 18: plot_owner_contact
        "Owner Email"               # 19: plot_owner_email
    ]
    sheet.append(headers)

    # Sample Data Row
    sample_data = [
        "Green Valley Plots", 1500, "residential_plot", "main", "yes", "2026-06-01", 
        "NIT", "yes", 3500000, "No", "", "freehold", "no", 0, 
        "Nagpur", "Besa", "Plot 12, Besa Road", "Amit Patil", "9876543210", "amit@example.com"
    ]
    sheet.append(sample_data)

    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="Plot_Resale_Template.xlsx"'
    workbook.save(response)
    return response

# 3. IMPORT EXCEL DATA
def import_plot_resale_excel(request):
    session_id = request.session.get('Admin_id')
    if not session_id:
        return JsonResponse({"status": "error", "message": "Unauthorized access"})

    if request.method == "POST" and request.FILES.get('excel_file'):
        try:
            admin_obj = Admin_Login.objects.get(id=session_id)
            
            excel_file = request.FILES['excel_file']
            wb = openpyxl.load_workbook(excel_file, data_only=True)
            sheet = wb.active

            # Iterate through rows, skipping header (min_row=2)
            for row in sheet.iter_rows(min_row=2, values_only=True):
                # Skip row if Project Name (column 0) is empty
                if not row[0]:
                    continue
                
                # Safely parse booleans
                is_corner = True if str(row[4]).strip().lower() == 'yes' else False
                is_fenced = True if str(row[7]).strip().lower() == 'yes' else False
                has_loan = True if str(row[12]).strip().lower() == 'yes' else False

                # Handle potential date parsing from excel (if it's a datetime object, extract date)
                avail_date = row[5]
                if avail_date and hasattr(avail_date, 'date'):
                    avail_date = avail_date.date()

                PlotSaleProperty.objects.create(
                    plot_title=row[0],
                    plot_area=row[1] or 0,
                    resale_plot_type=row[2],
                    plot_road_facing=row[3],
                    plot_corner=is_corner,
                    available_from=avail_date or None,
                    plot_authority=row[6],
                    plot_fencing=is_fenced,
                    plot_price=row[8] or 0,
                    brokerage=row[9],
                    brokerage_percentage=row[10],
                    plot_ownership=row[11],
                    plot_loan=has_loan,
                    plot_loan_amount=row[13] or 0,
                    plot_city=row[14],
                    plot_locality=row[15],
                    plot_address=row[16],
                    plot_owner_name=row[17],
                    plot_owner_contact=row[18],
                    plot_owner_email=row[19],
                    
                    # Store Uploader Details
                    uploaded_by_name=admin_obj.name,
                    uploaded_by_email=admin_obj.email,
                    uploaded_by_contact=admin_obj.phone,
                    uploaded_by_role=admin_obj.role
                )
            
            return JsonResponse({"status": "success", "message": "Excel data imported successfully!"})

        except Exception as e:
            traceback.print_exc()
            return JsonResponse({"status": "error", "message": f"Format Error: Ensure data matches template. Details: {str(e)}"})

    return JsonResponse({"status": "error", "message": "Invalid Request. File missing."})





# ==========================================
# 1. DETAILS VIEW PAGE
# ==========================================
def plot_sale_view(request, id):
    session_id = request.session.get('Admin_id')
    user_id = request.session.get('User_id')

    if not session_id and not user_id:
        return redirect('login')

    # Fetch the specific property
    prop = get_object_or_404(PlotSaleProperty, id=id)
    
    context = {
        'prop': prop
    }
    return render(request, 'admin_user/Reports/Resale/plot_view.html', context)


# ==========================================
# 2. DELETE FUNCTION (AJAX)
# ==========================================
def plot_sale_delete(request, id):
    # Ensure it's a POST request for security
    if request.method == "POST":
        try:
            prop = get_object_or_404(PlotSaleProperty, id=id)
            prop.delete() # This will automatically delete related images due to on_delete=models.CASCADE
            return JsonResponse({"status": "success", "message": "Property deleted successfully."})
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)})
            
    return JsonResponse({"status": "error", "message": "Invalid Request Method."})

    #####################END VIEW SECTION PLOT RESALE LISTING################


    ##############################START VIEW SECTION RESALE INDUSTRIAL LISTING#################

    
def industrial_resale_add(request):
    admin_id = request.session.get('Admin_id')
    user_id = request.session.get('User_id')

    if not admin_id and not user_id:
        return redirect('login')

    try:
        # =============================
        # GET USER DETAILS
        # =============================
        if admin_id:
            admin = Admin_Login.objects.get(id=admin_id)
            uploader_name = admin.name
            uploader_email = admin.email
            uploader_phone = admin.phone
            uploader_role = admin.role
        else:
            user = User_Details.objects.get(id=user_id)
            uploader_name = user.name
            uploader_email = user.email
            uploader_phone = user.phone
            uploader_role = user.role

        # =============================
        # HANDLE POST
        # =============================
        if request.method == "POST":
            # Safely parse boolean choices
            power_val = True if request.POST.get('ind_power') == 'yes' else False
            crane_val = True if request.POST.get('ind_crane') == 'yes' else False
            housing_val = True if request.POST.get('ind_housing') == 'yes' else False
            
            loan_val = True if request.POST.get('ind_loan') == 'yes' else False
            tenants_val = True if request.POST.get('ind_tenants') == 'yes' else False
            dispute_val = True if request.POST.get('ind_dispute') == 'yes' else False
            tax_due_val = True if request.POST.get('ind_tax_due') == 'yes' else False
            tax_cert_val = True if request.POST.get('ind_tax_cert') == 'yes' else False

            prop = IndustrialResaleProperty.objects.create(
                # Step 1
                property_type=request.POST.get('industrial_property_type'),
                land_area=request.POST.get('ind_area') or 0,
                available_from=request.POST.get('available_from') or None,
                power_supply=power_val,
                kva_capacity=request.POST.get('ind_kva') or None,
                water_supply=request.POST.get('ind_water'),
                crane_heavy_machinery=crane_val,
                road_connectivity=request.POST.get('ind_road'),
                worker_housing_nearby=housing_val,

                # Step 2
                expected_price=request.POST.get('ind_price') or 0,
                brokerage=request.POST.get('brokerage'),
                brokerage_percentage=request.POST.get('brokerage_percentage'),
                manual_brokerage=request.POST.get('manual_brokerage'),
                sanctioning_authority=request.POST.get('ind_authority'),
                ownership_type=request.POST.get('ind_ownership'),
                
                has_loan=loan_val,
                loan_amount=request.POST.get('ind_loan_amount') or None,
                
                existing_tenants=tenants_val,
                tenant_details=request.POST.get('ind_tenant_details'),
                
                legal_dispute=dispute_val,
                dispute_details=request.POST.get('ind_dispute_details'),
                
                tax_due=tax_due_val,
                tax_amount=request.POST.get('ind_tax_amount') or None,
                tax_clearance_cert=tax_cert_val,
                
                property_description=request.POST.get('resale_industrial_desc'),

                # Step 3
                compliance_docs=request.FILES.get('ind_compliance'),
                social_video=request.FILES.get('ind_video'),

                # Step 4
                city=request.POST.get('ind_city'),
                locality=request.POST.get('ind_locality'),
                complete_address=request.POST.get('ind_address'),
                owner_name=request.POST.get('ind_owner_name'),
                owner_contact=request.POST.get('ind_owner_contact'),
                owner_email=request.POST.get('ind_owner_email'),
                residency_status=request.POST.get('ind_residency'),

                # Uploader Info
                uploaded_by_name=uploader_name,
                uploaded_by_email=uploader_email,
                uploaded_by_contact=uploader_phone,
                uploaded_by_role=uploader_role,
            )

            # =============================
            # SAVE IMAGES (Min 1 handled in JS, Max 10 handled here and JS)
            # =============================
            images = request.FILES.getlist('property_images[]')

            for i, img in enumerate(images):
                if i >= 10:
                    break  # Stop at 10 images
                IndustrialResaleImage.objects.create(
                    property=prop,
                    image=img
                )

            return JsonResponse({
                "status": "success",
                "message": "Industrial Property Added Successfully"
            })

    except Exception as e:
        print("ERROR:", str(e))
        traceback.print_exc()
        return JsonResponse({
            "status": "error",
            "message": str(e)
        })

    # For GET requests
    context = {'admin_obj': admin if admin_id else user}
    return render(request, 'admin_user/Reports/Resale/industrial_list.html', context)





def industrial_resale_edit(request, id):
    admin_id = request.session.get('Admin_id')
    user_id = request.session.get('User_id')

    if not admin_id and not user_id:
        return redirect('login')

    # Fetch the existing property
    prop = get_object_or_404(IndustrialResaleProperty, id=id)

    if request.method == "POST":
        try:
            # Safely parse boolean choices
            prop.power_supply = True if request.POST.get('ind_power') == 'yes' else False
            prop.crane_heavy_machinery = True if request.POST.get('ind_crane') == 'yes' else False
            prop.worker_housing_nearby = True if request.POST.get('ind_housing') == 'yes' else False
            
            prop.has_loan = True if request.POST.get('ind_loan') == 'yes' else False
            prop.existing_tenants = True if request.POST.get('ind_tenants') == 'yes' else False
            prop.legal_dispute = True if request.POST.get('ind_dispute') == 'yes' else False
            prop.tax_due = True if request.POST.get('ind_tax_due') == 'yes' else False
            prop.tax_clearance_cert = True if request.POST.get('ind_tax_cert') == 'yes' else False

            # Update Step 1
            prop.property_type = request.POST.get('industrial_property_type')
            prop.land_area = request.POST.get('ind_area') or 0
            prop.available_from = request.POST.get('available_from') or None
            prop.kva_capacity = request.POST.get('ind_kva') or None
            prop.water_supply = request.POST.get('ind_water')
            prop.road_connectivity = request.POST.get('ind_road')

            # Update Step 2
            prop.expected_price = request.POST.get('ind_price') or 0
            prop.brokerage = request.POST.get('brokerage')
            prop.brokerage_percentage = request.POST.get('brokerage_percentage')
            prop.manual_brokerage = request.POST.get('manual_brokerage')
            prop.sanctioning_authority = request.POST.get('ind_authority')
            prop.ownership_type = request.POST.get('ind_ownership')
            prop.loan_amount = request.POST.get('ind_loan_amount') or None
            prop.tenant_details = request.POST.get('ind_tenant_details')
            prop.dispute_details = request.POST.get('ind_dispute_details')
            prop.tax_amount = request.POST.get('ind_tax_amount') or None
            prop.property_description = request.POST.get('resale_industrial_desc')

            # Update Step 3 (Files - only update if new file is uploaded)
            if request.FILES.get('ind_compliance'):
                prop.compliance_docs = request.FILES.get('ind_compliance')
            if request.FILES.get('ind_video'):
                prop.social_video = request.FILES.get('ind_video')

            # Update Step 4
            prop.city = request.POST.get('ind_city')
            prop.locality = request.POST.get('ind_locality')
            prop.complete_address = request.POST.get('ind_address')
            prop.owner_name = request.POST.get('ind_owner_name')
            prop.owner_contact = request.POST.get('ind_owner_contact')
            prop.owner_email = request.POST.get('ind_owner_email')
            prop.residency_status = request.POST.get('ind_residency')

            prop.save()

            # Save New Images (Append up to 10 max)
            new_images = request.FILES.getlist('property_images[]')
            current_image_count = prop.images.count()

            for img in new_images:
                if current_image_count >= 10:
                    break
                IndustrialResaleImage.objects.create(property=prop, image=img)
                current_image_count += 1

            return JsonResponse({"status": "success", "message": "Industrial Property Updated Successfully"})

        except Exception as e:
            print("ERROR:", str(e))
            traceback.print_exc()
            return JsonResponse({"status": "error", "message": str(e)})

    # Render template for GET request
    context = {'prop': prop}
    return render(request, 'admin_user/Resale/industrial_edit.html', context)





def industrial_resale_list(request):
    session_id = request.session.get('Admin_id')
    if session_id:
        admin_obj = Admin_Login.objects.get(id=session_id)
        
        # Fetch all properties in descending order (newest first)
        properties = IndustrialResaleProperty.objects.all().order_by('-created_at')
        
        context = {
            'admin_obj': admin_obj,
            'properties': properties
        }
        return render(request, 'admin_user/Reports/Resale/industrial_list.html', context)
    else:
        return render(request, 'home_page/Adminlogin.html')





def industrial_resale_view(request, id):
    session_id = request.session.get('Admin_id')
    user_id = request.session.get('User_id')

    if not session_id and not user_id:
        return redirect('login')

    # Fetch the specific industrial property
    prop = get_object_or_404(IndustrialResaleProperty, id=id)
    
    context = {
        'prop': prop
    }
    return render(request, 'admin_user/Resale/industrial_view.html', context)



# ==========================================
def industrial_resale_delete(request, id):
    # Security check: Ensure it's a POST request triggered by our frontend JS
    if request.method == "POST":
        try:
            # Fetch the property
            prop = get_object_or_404(IndustrialResaleProperty, id=id)
            
            # Delete it (Cascades to related images)
            prop.delete() 
            
            return JsonResponse({
                "status": "success", 
                "message": "Industrial Property deleted successfully."
            })
            
        except Exception as e:
            return JsonResponse({
                "status": "error", 
                "message": f"Failed to delete: {str(e)}"
            })
            
    # Fallback for non-POST requests
    return JsonResponse({
        "status": "error", 
        "message": "Invalid Request Method. Must use POST."
    })



def download_industrial_resale_template(request):
    import openpyxl
    from django.http import HttpResponse

    wb = openpyxl.Workbook()
    sheet = wb.active
    sheet.title = "Industrial Template"

    # ✅ Headers (MATCH DB SEQUENCE EXACTLY)
    headers = [
        "Property Type", "Land Area", "Available From (YYYY-MM-DD)", "Power Supply (yes/no)",
        "KVA Capacity", "Water Supply", "Crane/Heavy Machinery (yes/no)", "Road Connectivity",
        "Worker Housing Nearby (yes/no)", "Expected Price", "Brokerage (Yes/No)", "Brokerage %",
        "Manual Brokerage", "Sanctioning Authority", "Ownership Type", "Has Loan (yes/no)",
        "Loan Amount", "Existing Tenants (yes/no)", "Tenant Details", "Legal Dispute (yes/no)",
        "Dispute Details", "Tax Due (yes/no)", "Tax Amount", "Tax Clearance Cert (yes/no)",
        "Property Description", "City", "Locality", "Complete Address",
        "Owner Name", "Owner Contact", "Owner Email", "Residency Status"
    ]

    sheet.append(headers)

    # ✅ Sample Row (CLEAN + SAFE DATA)
    sample_data = [
        "warehouse",                  # property_type
        5000,                         # land_area
        "2026-06-01",                 # available_from
        "yes",                        # power_supply
        250,                          # kva_capacity
        "corporation",                # water_supply
        "no",                         # crane
        "highway",                    # road
        "yes",                        # worker housing
        15000000,                     # expected_price
        "Yes",                        # brokerage
        "2",                          # brokerage % (no % sign)
        "",                           # manual brokerage
        "MIDC",                       # authority
        "freehold",                   # ownership
        "no",                         # loan
        0,                            # loan amount
        "no",                         # tenants
        "",                           # tenant details
        "no",                         # dispute
        "",                           # dispute details
        "no",                         # tax due
        0,                            # tax amount
        "yes",                        # tax clearance
        "Good industrial shed near highway",  # description
        "Nagpur",                     # city
        "Hingna MIDC",                # locality
        "Plot 42, Phase 1",           # address
        "Ramesh Verma",               # owner
        "9876543210",                 # contact
        "ramesh@example.com",         # email
        "resident"                    # residency
    ]

    sheet.append(sample_data)

    # ✅ Response
    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = 'attachment; filename="Industrial_Resale_Template.xlsx"'

    wb.save(response)
    return response

def import_industrial_resale_excel(request):
    session_id = request.session.get('Admin_id')
    user_id = request.session.get('User_id')

    if not session_id and not user_id:
        return JsonResponse({"status": "error", "message": "Unauthorized access"})

    if request.method == "POST" and request.FILES.get('excel_file'):
        try:
            # ✅ Get uploader (from session)
            if session_id:
                uploader = Admin_Login.objects.get(id=session_id)
                uploader_name = uploader.name
                uploader_email = uploader.email
                uploader_contact = uploader.phone
                uploader_role = "Admin"
            else:
                uploader = User_Details.objects.get(id=user_id)
                uploader_name = uploader.name
                uploader_email = uploader.email
                uploader_contact = uploader.phone
                uploader_role = uploader.role

            excel_file = request.FILES['excel_file']
            wb = openpyxl.load_workbook(excel_file, data_only=True)
            sheet = wb.active

            added_count = 0
            skipped_count = 0

            def parse_bool(val):
                return str(val).strip().lower() == 'yes'

            for row in sheet.iter_rows(min_row=2, values_only=True):

                if not row[0]:
                    continue

                # ✅ Clean values
                property_type = str(row[0]).strip() if row[0] else None
                city = str(row[25]).strip() if row[25] else None
                address = str(row[27]).strip() if row[27] else None
                owner_contact = str(row[29]).strip() if row[29] else None

                # ✅ Duplicate check
                if IndustrialResaleProperty.objects.filter(
                    property_type=property_type,
                    city=city,
                    complete_address=address,
                    owner_contact=owner_contact
                ).exists():
                    skipped_count += 1
                    continue

                # ✅ Date handling
                avail_date = row[2]
                if hasattr(avail_date, 'date'):
                    avail_date = avail_date.date()

                # ✅ Create object
                IndustrialResaleProperty.objects.create(
                    property_type=property_type,
                    land_area=float(row[1]) if row[1] else None,
                    available_from=avail_date,

                    power_supply=parse_bool(row[3]),
                    kva_capacity=row[4] or None,
                    water_supply=row[5],
                    crane_heavy_machinery=parse_bool(row[6]),
                    road_connectivity=row[7],
                    worker_housing_nearby=parse_bool(row[8]),

                    expected_price=float(row[9]) if row[9] else None,
                    brokerage=row[10],
                    brokerage_percentage=row[11],
                    manual_brokerage=row[12],

                    sanctioning_authority=row[13],
                    ownership_type=row[14],

                    has_loan=parse_bool(row[15]),
                    loan_amount=float(row[16]) if row[16] else None,

                    existing_tenants=parse_bool(row[17]),
                    tenant_details=row[18],

                    legal_dispute=parse_bool(row[19]),
                    dispute_details=row[20],

                    tax_due=parse_bool(row[21]),
                    tax_amount=float(row[22]) if row[22] else None,
                    tax_clearance_cert=parse_bool(row[23]),

                    property_description=row[24],

                    city=city,
                    locality=row[26],
                    complete_address=address,

                    owner_name=row[28],
                    owner_contact=owner_contact,
                    owner_email=row[30],
                    residency_status=row[31],

                    # ✅ Uploader fields (CORRECT)
                    uploaded_by_name=uploader_name,
                    uploaded_by_email=uploader_email,
                    uploaded_by_contact=uploader_contact,
                    uploaded_by_role=uploader_role
                )

                added_count += 1

            # ✅ Response
            if added_count > 0 and skipped_count == 0:
                return JsonResponse({"status": "success", "message": f"{added_count} properties imported successfully!"})
            elif added_count > 0 and skipped_count > 0:
                return JsonResponse({"status": "warning", "message": f"{added_count} imported, {skipped_count} skipped (duplicates)."})
            elif skipped_count > 0:
                return JsonResponse({"status": "info", "message": f"All {skipped_count} records already exist."})
            else:
                return JsonResponse({"status": "error", "message": "No valid data found."})

        except Exception as e:
            traceback.print_exc()
            return JsonResponse({"status": "error", "message": str(e)})

    return JsonResponse({"status": "error", "message": "Invalid request"})

    #####################END VIEW SECTION RESALE INDUSTRIL LISTING########################################


#####################START VIEW SECTION OF RESIDENTIAL RESALE LISTING###########################

def get_property_images(request, id):
    prop = ResaleResidentialProperty.objects.get(id=id)
    images = [img.image.url for img in prop.images.all()]
    return JsonResponse({'images': images})

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





def resale_residential_add(request):
    # ── 1. Session Check ──────────────────────────────────
    uploader = _get_uploader(request)
    if uploader is None:
        return redirect('login')

    # ── 2. Handle POST Request ────────────────────────────
    if request.method == "POST":
        
        # --- A. Auto-generate title if it's empty ---
        raw_title = request.POST.get('title')
        bhk = request.POST.get('bhk', '')
        locality = request.POST.get('locality', '')
        generated_title = raw_title if raw_title else f"{bhk.upper()} Property in {locality}"

        # --- B. Safely convert numeric strings to floats to prevent TypeErrors ---
        try:
            builtup_val = float(request.POST.get('builtup_area') or 0.0)
        except ValueError:
            builtup_val = 0.0

        try:
            price_val = float(request.POST.get('expected_price') or 0.0)
        except ValueError:
            price_val = 0.0

        # --- C. Create the Property Object ---
        prop = ResaleResidentialProperty(
            # Basic Information
            title            = generated_title,
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

            # Measurements (Using our safely converted numbers here)
            builtup_area     = builtup_val,
            expected_price   = price_val,
            
            carpet_area      = request.POST.get('carpet_area') or 0,
            plot_area        = request.POST.get('plot_area') or None,
            floor_no         = request.POST.get('floor_no') or 0,
            total_floors     = request.POST.get('total_floors') or 0,

            # Ownership & Legal
            ownership_type     = request.POST.get('ownership_type'),
            num_owners         = request.POST.get('num_owners'),
            has_loan           = request.POST.get('has_loan', 'no'),
            loan_amount        = request.POST.get('loan_amount') or None,
            has_tenants        = request.POST.get('has_tenants', 'no'),
            tenant_details     = request.POST.get('tenant_details') or None,
            has_legal_dispute  = request.POST.get('has_legal_dispute', 'no'),
            dispute_details    = request.POST.get('dispute_details') or None,
            has_tax_due        = request.POST.get('has_tax_due', 'no'),
            pending_tax_amount = request.POST.get('pending_tax_amount') or None,

            # Pricing & Description
            price_per_sqft       = request.POST.get('price_per_sqft') or None,
            is_negotiable        = request.POST.get('is_negotiable', 'yes'),
            brokerage            = request.POST.get('brokerage') or None,
            brokerage_percentage = request.POST.get('brokerage_percentage') or None,
            manual_brokerage     = request.POST.get('manual_brokerage') or None,
            description          = request.POST.get('description'),

            # Amenities & Facilities (Joining checkbox arrays into a string)
            nearby_facilities = ', '.join(request.POST.getlist('facilities[]')),
            amenities         = ', '.join(request.POST.getlist('amenities[]')),

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

            # Auto-filled from session
            uploaded_by_name    = uploader['uploader_name'],
            uploaded_by_email   = uploader['uploader_email'],
            uploaded_by_contact = uploader['uploader_phone'],
            uploaded_by_role    = uploader['uploader_role'],
        )

        # Save the main property object safely
        prop.save()  

        # --- D. Save multiple images into ResalePropertyImage ---
        images = request.FILES.getlist('property_images')
        for image in images:
            ResalePropertyImage.objects.create(
                property=prop,
                image=image
            )

        # --- E. Return JSON for the SweetAlert ---
        return JsonResponse({
            "status" : "success",
            "message": "Resale Residential Property Added Successfully"
        })

    # ── 3. Handle GET Request (Render Form) ───────────────────
    context = {
        "admin_obj"      : uploader['admin_obj'],
        "user_obj"       : uploader['user_obj'],
        "uploader_name"  : uploader['uploader_name'],  
        "uploader_email" : uploader['uploader_email'], 
        "uploader_phone" : uploader['uploader_phone'], 
        "uploader_role"  : uploader['uploader_role'],  
    }
    
    # Check that this template path matches your project structure!
    return render(request, 'admin_user/Reports/Resale/residential_resale_list.html', context)




def resale_residential_edit(request, id):
    # ── 1. Session Check ──────────────────────────────────
    uploader = _get_uploader(request)
    if uploader is None:
        return redirect('login')

    # ── 2. Get Property ───────────────────────────────────
    prop = get_object_or_404(ResaleResidentialProperty, id=id)

    # ── 3. Handle POST (UPDATE DATA) ──────────────────────
    if request.method == "POST":

        # --- A. Title Logic ---
        raw_title = request.POST.get('title')
        bhk = request.POST.get('bhk', '')
        locality = request.POST.get('locality', '')
        # If title is empty, auto-generate it for the table display
        prop.title = raw_title if raw_title else f"{bhk.upper()} Property in {locality}"

        # --- B. Safe Numeric Conversion & Auto-Calculation ---
        try:
            builtup = float(request.POST.get('builtup_area') or 0)
            expected_price = float(request.POST.get('expected_price') or 0)
            
            prop.builtup_area = builtup
            prop.expected_price = expected_price

            # Auto-calculate Price/sqft if not manually provided, to keep table data healthy
            manual_price_sqft = request.POST.get('price_per_sqft')
            if not manual_price_sqft and builtup > 0:
                prop.price_per_sqft = round(expected_price / builtup, 2)
            else:
                prop.price_per_sqft = manual_price_sqft
        except (ValueError, TypeError):
            pass

        # --- C. Basic Fields ---
        prop.property_type = request.POST.get('property_type')
        prop.zone = request.POST.get('zone')
        prop.society_type = request.POST.get('society_type')
        prop.water_type = request.POST.get('water_type')
        prop.furnishing_type = request.POST.get('furnishing_type')
        prop.age_of_property = request.POST.get('age_of_property')
        prop.facing = request.POST.get('facing')
        
        # Handle empty date string
        avail_date = request.POST.get('available_from')
        prop.available_from = avail_date if avail_date else None

        prop.bhk = request.POST.get('bhk')
        prop.bathrooms = request.POST.get('bathrooms') or 1
        prop.balconies = request.POST.get('balconies') or 0
        prop.covered_parking = request.POST.get('covered_parking') or 0
        prop.open_parking = request.POST.get('open_parking') or 0

        prop.carpet_area = request.POST.get('carpet_area') or 0
        prop.plot_area = request.POST.get('plot_area') or None
        prop.floor_no = request.POST.get('floor_no') or 0
        prop.total_floors = request.POST.get('total_floors') or 0

        # --- Legal ---
        prop.ownership_type = request.POST.get('ownership_type')
        prop.num_owners = request.POST.get('num_owners')

        prop.has_loan = request.POST.get('has_loan', 'no')
        prop.loan_amount = request.POST.get('loan_amount') if prop.has_loan == 'yes' else None

        prop.has_tenants = request.POST.get('has_tenants', 'no')
        prop.tenant_details = request.POST.get('tenant_details') if prop.has_tenants == 'yes' else None

        prop.has_legal_dispute = request.POST.get('has_legal_dispute', 'no')
        prop.dispute_details = request.POST.get('dispute_details') if prop.has_legal_dispute == 'yes' else None

        prop.has_tax_due = request.POST.get('has_tax_due', 'no')
        prop.pending_tax_amount = request.POST.get('pending_tax_amount') if prop.has_tax_due == 'yes' else None

        # --- Pricing ---
        prop.is_negotiable = request.POST.get('is_negotiable', 'yes')
        prop.brokerage = request.POST.get('brokerage') or None
        prop.brokerage_percentage = request.POST.get('brokerage_percentage') or None
        prop.manual_brokerage = request.POST.get('manual_brokerage') or None
        prop.description = request.POST.get('description')

        # --- Amenities & Facilities (Matching table badge logic) ---
        # Storing as comma-separated strings so prop.amenities_list works in the table
        prop.nearby_facilities = ', '.join(request.POST.getlist('facilities[]'))
        prop.amenities = ', '.join(request.POST.getlist('amenities[]'))

        # --- Address ---
        prop.city = request.POST.get('city')
        prop.locality = request.POST.get('locality')
        prop.building_name = request.POST.get('building_name') or None
        prop.complete_address = request.POST.get('complete_address')

        # --- Owner ---
        prop.owner_name = request.POST.get('owner_name')
        prop.owner_contact = request.POST.get('owner_contact')
        prop.owner_email = request.POST.get('owner_email')
        prop.residential_status = request.POST.get('residential_status')

        # --- Files ---
        if request.FILES.get('floor_plan'):
            prop.floor_plan = request.FILES.get('floor_plan')

        if request.FILES.get('property_video'):
            prop.property_video = request.FILES.get('property_video')

        prop.save()

        # --- Delete Old Images ---
        deleted_images = request.POST.getlist('deleted_images[]')
        if deleted_images:
            ResalePropertyImage.objects.filter(
                id__in=deleted_images,
                property=prop
            ).delete()

        # --- Add New Images ---
        new_images = request.FILES.getlist('property_images')
        for img in new_images:
            ResalePropertyImage.objects.create(property=prop, image=img)

        return JsonResponse({
            "status": "success",
            "message": "Property Updated Successfully"
        })

    # ── 4. Handle GET (LOAD EDIT FORM) ───────────────────
    ameneties_obj = Ameneties_Details.objects.all()
    facilities_obj = Facilities_Details.objects.all()

    # Convert stored string → list for checkbox checking
    prop_facilities_list = [f.strip() for f in prop.nearby_facilities.split(',')] if prop.nearby_facilities else []
    prop_amenities_list = [a.strip() for a in prop.amenities.split(',')] if prop.amenities else []

    existing_images = prop.images.all() 

    context = {
        "prop": prop,
        "ameneties_obj": ameneties_obj,
        "facilities_obj": facilities_obj,
        "prop_facilities_list": prop_facilities_list,
        "prop_amenities_list": prop_amenities_list,
        "existing_images": existing_images,
        "admin_obj": uploader['admin_obj'],
        "user_obj": uploader['user_obj'],
    }

    return render(request, 'admin_user/Reports/Resale/residential_resale_edit.html', context)





def resale_residential_view(request, pk):
    # ── Session Check ──
    uploader = _get_uploader(request)
    if uploader is None:
        return redirect('login')

    # 2. CHANGED 'id=id' to 'pk=pk' right here 👇
    prop = get_object_or_404(ResaleResidentialProperty, pk=pk)

    # Convert comma-separated strings to lists for nice badge rendering
    facilities_list = [f.strip() for f in prop.nearby_facilities.split(',')] if prop.nearby_facilities else []
    amenities_list = [a.strip() for a in prop.amenities.split(',')] if prop.amenities else []

    context = {
        "prop": prop,
        "images": prop.images.all(),
        "facilities_list": facilities_list,
        "amenities_list": amenities_list,
        "admin_obj": uploader['admin_obj'],
        "user_obj": uploader['user_obj'],
    }
    
    return render(request, 'admin_user/Reports/Resale/residential_resale_view.html', context)

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

    import openpyxl

    try:
        wb = openpyxl.load_workbook(excel_file)
        ws = wb.active

        imported = 0
        skipped  = 0

        for row in ws.iter_rows(min_row=2, values_only=True):

            if not any(row):
                continue

            try:
                (
                    title, property_type, zone, society_type, water_type,
                    furnishing_type, age_of_property, facing, available_from,

                    bhk, bathrooms, balconies, covered_parking, open_parking,

                    builtup_area, carpet_area, plot_area, floor_no, total_floors,

                    ownership_type, num_owners,

                    has_loan, loan_amount,
                    has_tenants, tenant_details,
                    has_legal_dispute, dispute_details,
                    has_tax_due, pending_tax_amount,

                    expected_price, price_per_sqft, is_negotiable,
                    brokerage, brokerage_percentage, manual_brokerage,

                    description,

                    nearby_facilities, amenities,

                    city, locality, building_name, complete_address,

                    owner_name, owner_contact, owner_email, residential_status

                ) = row[:46]   # ✅ EXACT correct count

                # ✅ Minimal validation
                if not title:
                    skipped += 1
                    continue

                ResaleResidentialProperty.objects.create(

                    title=str(title).strip(),
                    property_type=str(property_type).lower() if property_type else '',
                    zone=str(zone).lower() if zone else '',
                    society_type=str(society_type).lower() if society_type else '',
                    water_type=str(water_type).lower() if water_type else '',
                    furnishing_type=str(furnishing_type).lower() if furnishing_type else '',
                    age_of_property=str(age_of_property) if age_of_property else '',
                    facing=str(facing) if facing else '',
                    available_from=available_from if available_from else None,

                    bhk=str(bhk).lower() if bhk else '',
                    bathrooms=int(bathrooms) if bathrooms else 1,
                    balconies=int(balconies) if balconies else 0,
                    covered_parking=int(covered_parking) if covered_parking else 0,
                    open_parking=int(open_parking) if open_parking else 0,

                    builtup_area=float(builtup_area) if builtup_area else 0,
                    carpet_area=float(carpet_area) if carpet_area else 0,
                    plot_area=float(plot_area) if plot_area else None,
                    floor_no=int(floor_no) if floor_no else 0,
                    total_floors=int(total_floors) if total_floors else 0,

                    ownership_type=str(ownership_type).lower() if ownership_type else '',
                    num_owners=str(num_owners) if num_owners else '1',

                    has_loan=str(has_loan).lower() if has_loan else 'no',
                    loan_amount=float(loan_amount) if loan_amount else None,

                    has_tenants=str(has_tenants).lower() if has_tenants else 'no',
                    tenant_details=str(tenant_details) if tenant_details else None,

                    has_legal_dispute=str(has_legal_dispute).lower() if has_legal_dispute else 'no',
                    dispute_details=str(dispute_details) if dispute_details else None,

                    has_tax_due=str(has_tax_due).lower() if has_tax_due else 'no',
                    pending_tax_amount=float(pending_tax_amount) if pending_tax_amount else None,

                    expected_price=float(expected_price) if expected_price else 0,
                    price_per_sqft=float(price_per_sqft) if price_per_sqft else None,
                    is_negotiable=str(is_negotiable).lower() if is_negotiable else 'yes',

                    brokerage=str(brokerage) if brokerage else None,
                    brokerage_percentage=str(brokerage_percentage) if brokerage_percentage else None,
                    manual_brokerage=str(manual_brokerage) if manual_brokerage else None,

                    description=str(description) if description else '',

                    nearby_facilities=str(nearby_facilities) if nearby_facilities else '',
                    amenities=str(amenities) if amenities else '',

                    city=str(city) if city else '',
                    locality=str(locality) if locality else '',
                    building_name=str(building_name) if building_name else None,
                    complete_address=str(complete_address) if complete_address else '',

                    owner_name=str(owner_name) if owner_name else '',
                    owner_contact=str(owner_contact) if owner_contact else '',
                    owner_email=str(owner_email) if owner_email else '',
                    residential_status=str(residential_status).lower() if residential_status else 'resident',

                    # ✅ Always from session
                    uploaded_by_name=request.session.get('admin_name', ''),
                    uploaded_by_email=request.session.get('admin_email', ''),
                    uploaded_by_contact=request.session.get('admin_contact', ''),
                    uploaded_by_role='admin',
                )

                imported += 1

            except Exception as e:
                print("ROW ERROR:", e)   # 🔥 IMPORTANT DEBUG
                skipped += 1

        return JsonResponse({
            'status': 'success',
            'imported': imported,
            'skipped': skipped,
        })

    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)})


def resale_residential_sample_excel(request):

    session_id = request.session.get('Admin_id')
    if not session_id:
        return redirect('login')

   

    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Resale Residential Sample"

    # ✅ ALL FIELDS (NO SKIP — EXACT MODEL ORDER)
    headers = [
        'title', 'property_type', 'zone', 'society_type', 'water_type',
        'furnishing_type', 'age_of_property', 'facing', 'available_from',

        'bhk', 'bathrooms', 'balconies', 'covered_parking', 'open_parking',

        'builtup_area', 'carpet_area', 'plot_area', 'floor_no', 'total_floors',

        'ownership_type', 'num_owners',

        'has_loan', 'loan_amount',
        'has_tenants', 'tenant_details',
        'has_legal_dispute', 'dispute_details',
        'has_tax_due', 'pending_tax_amount',

        'expected_price', 'price_per_sqft', 'is_negotiable',
        'brokerage', 'brokerage_percentage', 'manual_brokerage',

        'description',

        'nearby_facilities', 'amenities',

        'city', 'locality', 'building_name', 'complete_address',

        'owner_name', 'owner_contact', 'owner_email', 'residential_status',

        'uploaded_by_name', 'uploaded_by_email', 'uploaded_by_contact', 'uploaded_by_role',

        'floor_plan', 'property_video'
    ]

    ws.append(headers)

    # ✅ FULL SAMPLE DATA (MATCHING ALL FIELDS)
    sample = [
        '3BHK Apartment in Prime Location',  # title
        'apartment',                        # property_type
        'north',                            # zone
        'gated',                            # society_type
        'municipal',                        # water_type
        'semi',                             # furnishing_type
        '1-3',                              # age_of_property
        'North-East',                       # facing
        '2026-06-01',                       # available_from

        '3bhk', 2, 1, 1, 0,                 # bhk, bath, balcony, parking

        1200, 950, '', 3, 10,               # area details

        'freehold', '1',                    # ownership

        'yes', 2000000,                     # loan
        'no', '',                           # tenants
        'no', '',                           # dispute
        'no', '',                           # tax

        5000000, '', 'yes',                 # price

        'yes', '2%', '',                    # brokerage

        'Beautiful apartment near schools, hospitals and metro station',  # desc

        'school, hospital, metro',          # facilities
        'lift, parking, security',          # amenities

        'Nagpur', 'Dharampeth', 'Sunshine Society', '123 Dharampeth Nagpur',

        'Rahul Sharma', '9876543210', 'rahul@example.com', 'resident',

        'Admin User', 'admin@mail.com', '9999999999', 'admin',

        '', ''                              # floor_plan, video
    ]

    ws.append(sample)

    # ✅ HEADER STYLE
    for cell in ws[1]:
        cell.font = Font(bold=True, color="FFFFFF")
        cell.fill = PatternFill("solid", fgColor="667EEA")

    # ✅ AUTO WIDTH
    for col in ws.columns:
        max_len = max(len(str(cell.value)) if cell.value else 0 for cell in col)
        ws.column_dimensions[col[0].column_letter].width = max_len + 4

    # ✅ RESPONSE
    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = 'attachment; filename="resale_residential_sample.xlsx"'

    wb.save(response)
    return response



#####################END VIEW SECTION OF RESIDENTIAL RESALE LISTING###########################






####################Start  Views Section For Commercial Resale Property #######################################



def commercial_resale_list(request):
    # ── Session check ─────────────────────────────────────
    admin_id = request.session.get('Admin_id')
    user_id  = request.session.get('User_id')

    if not admin_id and not user_id:
        return render(request, 'home_page/Adminlogin.html')

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
    props = CommercialResaleProperty.objects.all().order_by('-id')

    # ── Stat cards ─────────────────────────────────────────
    total_properties = props.count()
    active_properties = props.filter(is_active=True).count()
    inactive_properties = props.filter(is_active=False).count()

    office_count     = props.filter(property_type='office').count()
    shop_count       = props.filter(property_type='shop').count()
    warehouse_count  = props.filter(property_type='warehouse').count()
    industrial_count = props.filter(property_type='industrial').count()
    land_count       = props.filter(property_type='land').count()

    # Avg expected price
    avg_price = props.aggregate(Avg('expected_price'))['expected_price__avg'] or 0

    # ── Chart 1: Property Type Pie ─────────────────────────
    type_map = {
        'office': 'Office Space',
        'shop': 'Shop/Showroom',
        'warehouse': 'Warehouse',
        'industrial': 'Industrial',
        'land': 'Commercial Land',
    }
    type_qs = props.values('property_type').annotate(count=Count('id'))
    type_labels = [type_map.get(x['property_type'], x['property_type']) for x in type_qs]
    type_data = [x['count'] for x in type_qs]

    # ── Chart 2: Monthly Data (Current Year) ───────────────
    current_year = timezone.now().year
    monthly_data = [0] * 12
    monthly_qs = props.filter(created_at__year=current_year).values('created_at__month').annotate(count=Count('id'))
    for x in monthly_qs:
        monthly_data[x['created_at__month'] - 1] = x['count']

    # ── Chart 3: Zone Distribution ─────────────────────────
    zone_map = {
        'industrial': 'Industrial',
        'commercial': 'Commercial',
        'residential': 'Residential',
        'sez': 'SEZ',
    }
    zone_qs = props.values('zone_type').annotate(count=Count('id'))
    zone_labels = [zone_map.get(x['zone_type'], x['zone_type']) for x in zone_qs]
    zone_data = [x['count'] for x in zone_qs]

    context = {
        'admin_obj': admin_obj,
        'user_obj' : user_obj,
        'commercial_list': props,

        'total_properties': total_properties,
        'active_properties': active_properties,
        'inactive_properties': inactive_properties,
        'office_count'    : office_count,
        'shop_count'      : shop_count,
        'warehouse_count' : warehouse_count,
        'industrial_count': industrial_count,
        'land_count'      : land_count,
        'avg_price'       : avg_price,

        'chart_type_labels' : json.dumps(type_labels),
        'chart_type_data'   : json.dumps(type_data),
        'chart_monthly_data': json.dumps(monthly_data),
        'chart_zone_labels' : json.dumps(zone_labels),
        'chart_zone_data'   : json.dumps(zone_data),
    }

    return render(request, 'admin_user/Reports/Resale/commercial_list.html', context)



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



@transaction.atomic
def import_commercial_data(request):
    if request.method == 'POST' and request.FILES.get('commercial_excel_file'):
        excel_file = request.FILES['commercial_excel_file']
        
        if not excel_file.name.endswith('.xlsx'):
            return JsonResponse({'status': '0', 'msg': 'Invalid file format. Please upload a .xlsx file.'})

        try:
            wb = openpyxl.load_workbook(excel_file)
            ws = wb.active

            success_count = 0
            duplicate_count = 0

            # Helper function for safe numbers
            def safe_num(val, is_float=False):
                if val is None or str(val).strip() == '':
                    return 0.0 if is_float else 0
                try:
                    return float(val) if is_float else int(float(val))
                except ValueError:
                    return 0.0 if is_float else 0

            # Helper function for dates
            def safe_date(val):
                if not val:
                    return None
                if isinstance(val, datetime):
                    return val.date()
                try:
                    return datetime.strptime(str(val).strip(), "%Y-%m-%d").date()
                except ValueError:
                    return None

            # Iterate starting from row 2 (skipping headers)
            for row in ws.iter_rows(min_row=2, values_only=True):
                title = str(row[0] or '').strip()
                if not title: # Skip totally empty rows
                    continue
                
                property_type = str(row[1] or '').strip().lower()
                city = str(row[37] or '').strip()
                expected_price = safe_num(row[22], True)

                # --- DUPLICATE CHECK ---
                # Check if a property with the same Title, Type, City, and Price already exists
                is_duplicate = CommercialResaleProperty.objects.filter(
                    title=title,
                    property_type=property_type,
                    city=city,
                    expected_price=expected_price
                ).exists()

                if is_duplicate:
                    duplicate_count += 1
                    continue # Skip this row and move to the next

                # --- CREATE NEW PROPERTY ---
                CommercialResaleProperty.objects.create(
                    title=title,
                    property_type=property_type,
                    zone_type=str(row[2] or '').lower(),
                    location_hub=str(row[3] or '').lower(),
                    property_condition=str(row[4] or '').lower(),
                    ownership_type=str(row[5] or '').lower(),
                    age_of_property=str(row[6] or ''),
                    available_from=safe_date(row[7]),

                    num_staircases=safe_num(row[8]),
                    passenger_lifts=safe_num(row[9]),
                    service_lifts=safe_num(row[10]),
                    num_cabins=safe_num(row[11]),
                    meeting_rooms=safe_num(row[12]),
                    min_seats=safe_num(row[13]),
                    max_seats=safe_num(row[14]),
                    private_parking=safe_num(row[15]),
                    public_parking=safe_num(row[16]),

                    builtup_area=safe_num(row[17], True),
                    carpet_area=safe_num(row[18], True),
                    plot_area=safe_num(row[19], True),
                    brokerage=str(row[20] or '').lower(),
                    brokerage_percentage=str(row[21] or ''),
                    expected_price=expected_price,

                    num_owners=str(row[23] or '1'),
                    loan_on_property=str(row[24] or 'no').lower(),
                    loan_amount=safe_num(row[25], True),
                    existing_tenants=str(row[26] or 'no').lower(),
                    tenant_details=str(row[27] or ''),
                    legal_dispute=str(row[28] or 'no').lower(),
                    dispute_details=str(row[29] or ''),
                    tax_due=str(row[30] or 'no').lower(),
                    pending_tax_amount=safe_num(row[31], True),
                    fire_noc=str(row[32] or 'no').lower(),

                    property_description=str(row[33] or ''),
                    sanctioning_authority=str(row[34] or ''),
                    nearby_facilities=str(row[35] or ''),
                    amenities=str(row[36] or ''),

                    city=city,
                    locality=str(row[38] or ''),
                    building_name=str(row[39] or ''),
                    property_address=str(row[40] or ''),

                    owner_name=str(row[41] or ''),
                    owner_contact=str(row[42] or ''),
                    owner_email=str(row[43] or ''),
                    residential_status=str(row[44] or 'resident').lower(),

                    uploaded_by_name="Admin Upload",
                    is_active=True
                )
                success_count += 1

            # Prepare the response message
            if success_count > 0 and duplicate_count == 0:
                msg = f'{success_count} properties imported successfully!'
            elif success_count > 0 and duplicate_count > 0:
                msg = f'{success_count} properties imported. {duplicate_count} duplicate rows were skipped.'
            elif success_count == 0 and duplicate_count > 0:
                msg = f'No new properties imported. All {duplicate_count} rows already exist in the database.'
            else:
                msg = 'No valid data found in the file to import.'

            return JsonResponse({'status': '1', 'msg': msg})

        except Exception as e:
            return JsonResponse({'status': '0', 'msg': f'Error processing file: {str(e)}'})

    return JsonResponse({'status': '0', 'msg': 'Invalid request or missing file.'})


def download_commercial_sample_excel(request):
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Commercial Properties"

    # Exact Sequence of the Model (0 to 44 = 45 Columns)
    headers = [
        "Title", "Property Type (office/shop/warehouse/industrial/land)", "Zone Type (industrial/commercial/residential/sez)",
        "Location Hub", "Condition (new/excellent/good/renovation)", "Ownership (freehold/leasehold/cooperative)", 
        "Age (0-1/1-3/3-5/5-10/10+)", "Available From (YYYY-MM-DD)", "Staircases", "Passenger Lifts", "Service Lifts", 
        "Cabins", "Meeting Rooms", "Min Seats", "Max Seats", "Private Parking", "Public Parking", "Builtup Area", 
        "Carpet Area", "Plot Area", "Brokerage (yes/no)", "Brokerage Percentage", "Expected Price", "Num Owners", 
        "Loan on Property (yes/no)", "Loan Amount", "Existing Tenants (yes/no)", "Tenant Details", "Legal Dispute (yes/no)", 
        "Dispute Details", "Tax Due (yes/no)", "Pending Tax Amount", "Fire NOC (yes/no)", "Property Description", 
        "Sanctioning Authority", "Nearby Facilities (comma separated)", "Amenities (comma separated)", "City", 
        "Locality", "Building Name", "Property Address", "Owner Name", "Owner Contact", "Owner Email", 
        "Residential Status (resident/nri/pio)"
    ]
    
    ws.append(headers)

    # Add 1 Sample Row
    sample_data = [
        "Prime IT Park Office", "office", "commercial", "it", "excellent", "freehold", "1-3", "2026-05-01",
        2, 4, 1, 5, 2, 50, 100, 5, 10, 5000, 4500, 0, "yes", "2%", 15000000, "1", "no", 0, "no", "",
        "no", "", "no", 0, "yes", "Fully furnished premium office space.", "NMC", "Metro, Mall, Hospital", 
        "CCTV, Power Backup, Gym", "Nagpur", "Sitabuldi", "Tech Tower", "Floor 4, Tech Tower, Sitabuldi",
        "Rajesh Kumar", "9876543210", "rajesh@example.com", "resident"
    ]
    ws.append(sample_data)

    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="Commercial_Resale_Sample.xlsx"'
    wb.save(response)
    return response

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





# --- 1. COMMERCIAL VIEW PAGE ---
def commercial_resale_view(request, id):
    prop = get_object_or_404(CommercialResaleProperty, id=id)
    images = prop.images.all()
    
    # Split strings for nice badge rendering in HTML
    facilities_list = [f.strip() for f in prop.nearby_facilities.split(',')] if prop.nearby_facilities else []
    amenities_list = [a.strip() for a in prop.amenities.split(',')] if prop.amenities else []

    context = {
        'prop': prop,
        'images': images,
        'facilities_list': facilities_list,
        'amenities_list': amenities_list
    }
    return render(request, 'admin_user/Reports/Resale/commercial_resale_view.html', context)





def commercial_resale_edit(request, id):
    uploader = _get_uploader(request)
    if uploader is None:
        return redirect('login')

    prop = get_object_or_404(CommercialResaleProperty, id=id)

    if request.method == "POST":
        # Safe Converters
        def safe_float(val):
            try: return float(val) if val else 0.0
            except ValueError: return 0.0
            
        def safe_int(val):
            try: return int(float(val)) if val else 0
            except ValueError: return 0

        # ── Basic Information ──────────────────────────────
        prop.title = request.POST.get('title')
        prop.property_type = request.POST.get('property_type')
        prop.zone_type = request.POST.get('zone_type')
        prop.location_hub = request.POST.get('location_hub') or None
        prop.property_condition = request.POST.get('property_condition')
        prop.ownership_type = request.POST.get('ownership_type')
        prop.age_of_property = request.POST.get('age_of_property')
        prop.available_from = request.POST.get('available_from') or None

        # ── Commercial Specifications ──────────────────────
        prop.num_staircases = safe_int(request.POST.get('num_staircases'))
        prop.passenger_lifts = safe_int(request.POST.get('passenger_lifts'))
        prop.service_lifts = safe_int(request.POST.get('service_lifts'))
        prop.num_cabins = safe_int(request.POST.get('num_cabins'))
        prop.meeting_rooms = safe_int(request.POST.get('meeting_rooms'))
        prop.min_seats = safe_int(request.POST.get('min_seats')) if request.POST.get('min_seats') else None
        prop.max_seats = safe_int(request.POST.get('max_seats')) if request.POST.get('max_seats') else None
        prop.private_parking = safe_int(request.POST.get('private_parking'))
        prop.public_parking = safe_int(request.POST.get('public_parking'))

        # ── Area & Pricing ─────────────────────────────────
        prop.builtup_area = safe_float(request.POST.get('builtup_area'))
        prop.carpet_area = safe_float(request.POST.get('carpet_area')) if request.POST.get('carpet_area') else None
        prop.plot_area = safe_float(request.POST.get('plot_area')) if request.POST.get('plot_area') else None
        
        prop.brokerage = request.POST.get('brokerage') or None
        prop.brokerage_percentage = request.POST.get('brokerage_percentage') or None
        prop.manual_brokerage = request.POST.get('manual_brokerage') or None
        prop.expected_price = safe_float(request.POST.get('expected_price'))

        # ── Ownership & Legal ──────────────────────────────
        prop.num_owners = request.POST.get('num_owners', '1')
        
        prop.loan_on_property = request.POST.get('loan_on_property', 'no')
        prop.loan_amount = safe_float(request.POST.get('loan_amount')) if prop.loan_on_property == 'yes' else None
        
        prop.existing_tenants = request.POST.get('existing_tenants', 'no')
        prop.tenant_details = request.POST.get('tenant_details') if prop.existing_tenants == 'yes' else None
        
        prop.legal_dispute = request.POST.get('legal_dispute', 'no')
        prop.dispute_details = request.POST.get('dispute_details') if prop.legal_dispute == 'yes' else None
        
        prop.tax_due = request.POST.get('tax_due', 'no')
        prop.pending_tax_amount = safe_float(request.POST.get('pending_tax_amount')) if prop.tax_due == 'yes' else None
        
        prop.fire_noc = request.POST.get('fire_noc', 'no')
        prop.property_description = request.POST.get('property_description')
        prop.sanctioning_authority = request.POST.get('sanctioning_authority')

        # ── Nearby Facilities & Amenities ──────────────────
        prop.nearby_facilities = ', '.join(request.POST.getlist('facilities[]'))
        prop.amenities = ', '.join(request.POST.getlist('amenities[]'))

        # ── Address ────────────────────────────────────────
        prop.city = request.POST.get('city')
        prop.locality = request.POST.get('locality')
        prop.building_name = request.POST.get('building_name') or None
        prop.property_address = request.POST.get('property_address')

        # ── Owner Contact ──────────────────────────────────
        prop.owner_name = request.POST.get('owner_name')
        prop.owner_contact = request.POST.get('owner_contact')
        prop.owner_email = request.POST.get('owner_email')
        prop.residential_status = request.POST.get('residential_status')

        # ── Media ──────────────────────────────────────────
        if request.FILES.get('floor_plan'):
            prop.floor_plan = request.FILES.get('floor_plan')
        if request.FILES.get('property_video'):
            prop.property_video = request.FILES.get('property_video')

        prop.save()

        # Handle Image Gallery (Delete checked ones)
        deleted_images = request.POST.getlist('deleted_images[]')
        if deleted_images:
            CommercialPropertyImage.objects.filter(id__in=deleted_images, property=prop).delete()

        # Add New Images
        for img in request.FILES.getlist('property_images'):
            CommercialPropertyImage.objects.create(property=prop, image=img)

        return JsonResponse({"status": "success", "message": "Commercial Property Updated Successfully"})

    # --- GET REQUEST Context ---
    ameneties_obj = Ameneties_Details.objects.all()
    facilities_obj = Facilities_Details.objects.all()
    
    prop_facilities_list = [f.strip() for f in prop.nearby_facilities.split(',')] if prop.nearby_facilities else []
    prop_amenities_list = [a.strip() for a in prop.amenities.split(',')] if prop.amenities else []
    
    existing_images = prop.images.all() 

    context = {
        "prop": prop,
        "ameneties_obj": ameneties_obj,
        "facilities_obj": facilities_obj,
        "prop_facilities_list": prop_facilities_list,
        "prop_amenities_list": prop_amenities_list,
        "existing_images": existing_images,
    }
    return render(request, 'admin_user/Reports/Resale/commercial_resale_edit.html', context)

####################End Views Section For Commercial Resale Property #######################################



####################START Views Section For AGRICULTURAL Resale Property #######################################


def add_agricultural_property(request):
    if request.method == 'POST':
        try:
            def get_decimal(val):
                return val if val and str(val).strip() != "" else None

            with transaction.atomic():

                property_obj = AgriculturalResaleProperty.objects.create(

                    # STEP 1
                    title=request.POST.get('title', 'Agricultural Land Listing'),
                    agriculture_property_type=request.POST.get('agriculture_property_type'),
                    land_area=get_decimal(request.POST.get('land_area')),
                    state=request.POST.get('state'),
                    city=request.POST.get('city'),
                    district=request.POST.get('district'),
                    taluka=request.POST.get('taluka'),
                    village=request.POST.get('village'),
                    address=request.POST.get('address'),

                    # STEP 2
                    soil_type=request.POST.get('soil_type'),
                    water_source=request.POST.get('water_source'),
                    irrigation_facility=request.POST.get('irrigation_facility', 'no'),
                    fertility_status=request.POST.get('fertility_status'),
                    previous_crops=request.POST.get('previous_crops'),
                    resale_agricultural_desc=request.POST.get('resale_agricultural_desc'),

                    # STEP 3
                    expected_price=get_decimal(request.POST.get('expected_price')),
                    brokerage=request.POST.get('brokerage'),
                    brokerage_percentage=request.POST.get('brokerage_percentage'),
                    manual_brokerage=request.POST.get('manual_brokerage'),
                    ownership_type=request.POST.get('ownership_type'),

                    agri_loan=request.POST.get('agri_loan', 'no'),
                    loan_amount=get_decimal(request.POST.get('loan_amount')) if request.POST.get('agri_loan') == 'yes' else None,

                    agri_tenants=request.POST.get('agri_tenants', 'no'),
                    tenant_details=request.POST.get('tenant_details'),

                    agri_dispute=request.POST.get('agri_dispute', 'no'),
                    dispute_details=request.POST.get('dispute_details'),

                    agri_tax_due=request.POST.get('agri_tax_due', 'no'),
                    pending_tax_amount=get_decimal(request.POST.get('pending_tax_amount')),

                    # STEP 4
                    owner_name=request.POST.get('owner_name'),
                    owner_contact=request.POST.get('owner_contact'),
                    owner_email=request.POST.get('owner_email'),
                    comm_residency=request.POST.get('comm_residency'),

                    # UPLOADER
                    uploaded_by_name=request.POST.get('uploaded_by_name'),
                    uploaded_by_email=request.POST.get('uploaded_by_email'),
                    uploaded_by_contact=request.POST.get('uploaded_by_contact'),
                    uploaded_by_role=request.POST.get('uploaded_by_role'),
                )

                # FILES (FIXED NAME ❗)
                if 'encumbrance_cert' in request.FILES:
                    property_obj.encumbrance_cert = request.FILES['encumbrance_cert']

                if 'property_video' in request.FILES:
                    property_obj.property_video = request.FILES['property_video']

                property_obj.save()

                # MULTIPLE IMAGES
                images = request.FILES.getlist('property_images[]')
                for img in images[:10]:
                    AgriculturalResaleImage.objects.create(property=property_obj, image=img)

            return JsonResponse({'status': 'success', 'message': 'Saved successfully'})

        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
    



def agricultural_resale_list(request):
    session_id = request.session.get('Admin_id')
    if not session_id:
        return render(request, 'home_page/Adminlogin.html')

    admin_obj = Admin_Login.objects.get(id=session_id)

    # ============================
    # EXCEL IMPORT
    # ============================
    if request.method == 'POST' and 'excel_file' in request.FILES:
        excel_file = request.FILES['excel_file']

        try:
            df = pd.read_excel(excel_file)

            def get_decimal(val):
                if pd.isna(val) or str(val).strip() == "":
                    return None
                return float(val)

            def get_string(val, default=""):
                if pd.isna(val):
                    return default
                return str(val).strip()

            def clean_yes_no(val):
                return get_string(val, 'no').lower()

            added_count = 0
            skipped_count = 0

            for index, row in df.iterrows():

                # ============================
                # DUPLICATE CHECK (FIXED)
                # ============================
                exists = AgriculturalResaleProperty.objects.filter(
                    village=get_string(row.get('village')),
                    city=get_string(row.get('city')),
                    owner_contact=get_string(row.get('owner_contact')),
                    address=get_string(row.get('address'))   # FIXED
                ).exists()

                if exists:
                    skipped_count += 1
                    continue

                # ============================
                # CREATE OBJECT
                # ============================
                AgriculturalResaleProperty.objects.create(

                    # STEP 1
                    title=get_string(row.get('title'), 'Agricultural Land Listing'),
                    agriculture_property_type=get_string(row.get('agriculture_property_type'), 'agriculture_land'),

                    land_area = (
                    get_decimal(row.get('land_area'))
                    or get_decimal(row.get('area'))
                    or 0
                    ),

                    state=get_string(row.get('state')),
                    city=get_string(row.get('city')),
                    district=get_string(row.get('district')),
                    taluka=get_string(row.get('taluka')),
                    village=get_string(row.get('village')),
                    address = (
    get_string(row.get('address'))
    or get_string(row.get('property_address'))
),

                    # STEP 2
                    soil_type=get_string(row.get('soil_type')),
                    water_source=get_string(row.get('water_source')),
                    irrigation_facility=clean_yes_no(row.get('irrigation_facility')),
                    fertility_status=get_string(row.get('fertility_status')),
                    previous_crops=get_string(row.get('previous_crops')),
                    resale_agricultural_desc=get_string(row.get('resale_agricultural_desc')),

                    # STEP 3
                    expected_price=get_decimal(row.get('expected_price')) or 0,
                    brokerage=get_string(row.get('brokerage'), 'No'),
                    brokerage_percentage=get_string(row.get('brokerage_percentage')),
                    manual_brokerage=get_string(row.get('manual_brokerage')),
                    ownership_type=get_string(row.get('ownership_type'), 'freehold'),

                    agri_loan=clean_yes_no(row.get('agri_loan')),
                    loan_amount=get_decimal(row.get('loan_amount')) if clean_yes_no(row.get('agri_loan')) == 'yes' else None,

                    agri_tenants=clean_yes_no(row.get('agri_tenants')),
                    tenant_details=get_string(row.get('tenant_details')) if clean_yes_no(row.get('agri_tenants')) == 'yes' else "",

                    agri_dispute=clean_yes_no(row.get('agri_dispute')),
                    dispute_details=get_string(row.get('dispute_details')) if clean_yes_no(row.get('agri_dispute')) == 'yes' else "",

                    agri_tax_due=clean_yes_no(row.get('agri_tax_due')),
                    pending_tax_amount=get_decimal(row.get('pending_tax_amount')) if clean_yes_no(row.get('agri_tax_due')) == 'yes' else None,

                    # STEP 4
                    owner_name=get_string(row.get('owner_name')),
                    owner_contact=get_string(row.get('owner_contact')),
                    owner_email=get_string(row.get('owner_email')),
                    comm_residency=get_string(row.get('comm_residency'), 'resident'),

                    # UPLOADER
                    uploaded_by_name=get_string(row.get('uploaded_by_name')) or admin_obj.name,
                    uploaded_by_email=get_string(row.get('uploaded_by_email')) or admin_obj.email,
                    uploaded_by_contact=get_string(row.get('uploaded_by_contact')) or admin_obj.phone,
                    uploaded_by_role=get_string(row.get('uploaded_by_role')) or admin_obj.role,
                )

                added_count += 1

            # ============================
            # MESSAGES
            # ============================
            if added_count > 0 and skipped_count == 0:
                messages.success(request, f"{added_count} records imported successfully!")
            elif added_count > 0 and skipped_count > 0:
                messages.warning(request, f"{added_count} added, {skipped_count} skipped (duplicates).")
            elif skipped_count > 0:
                messages.info(request, f"All {skipped_count} records already exist.")
            else:
                messages.error(request, "No valid data found.")

        except Exception as e:
            messages.error(request, f"Import Error: {str(e)}")

        return redirect('agricultural_resale_list')

    # ============================
    # LIST + SEARCH + PAGINATION
    # ============================
    properties = AgriculturalResaleProperty.objects.all().order_by('-created_at')
    search_query = request.GET.get('search', '')

    if search_query:
        properties = properties.filter(
            Q(village__icontains=search_query) |
            Q(district__icontains=search_query) |
            Q(owner_name__icontains=search_query) |
            Q(agriculture_property_type__icontains=search_query)
        )

    paginator = Paginator(properties, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    total_properties = AgriculturalResaleProperty.objects.count()
    agri_land_count = AgriculturalResaleProperty.objects.filter(agriculture_property_type='agriculture_land').count()
    farm_land_count = AgriculturalResaleProperty.objects.filter(agriculture_property_type='farm_land').count()
    orchard_land_count = AgriculturalResaleProperty.objects.filter(agriculture_property_type='orchard_land').count()

    total_value = AgriculturalResaleProperty.objects.aggregate(
        Sum('expected_price')
    )['expected_price__sum'] or 0

    context = {
        'admin_obj': admin_obj,
        'page_obj': page_obj,
        'search_query': search_query,
        'stats': {
            'total': total_properties,
            'agri_land': agri_land_count,
            'farm_land': farm_land_count,
            'orchard': orchard_land_count,
            'total_value': total_value
        }
    }

    return render(request, 'admin_user/Reports/Resale/agricultural_list.html', context)







def edit_agricultural_property(request, pk):
    property_obj = get_object_or_404(AgriculturalResaleProperty, pk=pk)

    if request.method == 'POST':
        try:
            # =========================
            # SAFE HELPERS
            # =========================
            def get_decimal(value):
                if value is None or str(value).strip() == "":
                    return None
                return float(value)

            def clean_yes_no(val):
                return str(val).strip().lower() if val else 'no'

            with transaction.atomic():
                # =========================
                # STEP 1: BASIC INFO
                # =========================
                property_obj.title = request.POST.get('title', 'Agricultural Land Listing')
                property_obj.agriculture_property_type = request.POST.get('agriculture_property_type')

                property_obj.land_area = get_decimal(
                    request.POST.get('land_area') or request.POST.get('area')
                )

                property_obj.state = request.POST.get('state')
                property_obj.city = request.POST.get('city')
                property_obj.district = request.POST.get('district')
                property_obj.taluka = request.POST.get('taluka')
                property_obj.village = request.POST.get('village')

                # ✅ FIXED: Handle both 'address' and 'property_address' just in case
                property_obj.address = request.POST.get('address') or request.POST.get('property_address')

                # =========================
                # STEP 2: LAND DETAILS
                # =========================
                property_obj.soil_type = request.POST.get('soil_type')
                property_obj.water_source = request.POST.get('water_source')
                property_obj.irrigation_facility = clean_yes_no(request.POST.get('irrigation_facility'))
                property_obj.fertility_status = request.POST.get('fertility_status')
                property_obj.previous_crops = request.POST.get('previous_crops')
                property_obj.resale_agricultural_desc = request.POST.get('resale_agricultural_desc')

                # =========================
                # STEP 3: PRICING & LEGAL
                # =========================
                property_obj.expected_price = get_decimal(request.POST.get('expected_price'))
                property_obj.brokerage = request.POST.get('brokerage')
                property_obj.brokerage_percentage = request.POST.get('brokerage_percentage')
                property_obj.manual_brokerage = request.POST.get('manual_brokerage')

                property_obj.ownership_type = request.POST.get('ownership_type')

                property_obj.agri_loan = clean_yes_no(request.POST.get('agri_loan'))
                property_obj.loan_amount = (
                    get_decimal(request.POST.get('loan_amount'))
                    if property_obj.agri_loan == 'yes' else None
                )

                property_obj.agri_tenants = clean_yes_no(request.POST.get('agri_tenants'))
                property_obj.tenant_details = (
                    request.POST.get('tenant_details')
                    if property_obj.agri_tenants == 'yes' else ""
                )

                property_obj.agri_dispute = clean_yes_no(request.POST.get('agri_dispute'))
                property_obj.dispute_details = (
                    request.POST.get('dispute_details')
                    if property_obj.agri_dispute == 'yes' else ""
                )

                property_obj.agri_tax_due = clean_yes_no(request.POST.get('agri_tax_due'))
                property_obj.pending_tax_amount = (
                    get_decimal(request.POST.get('pending_tax_amount'))
                    if property_obj.agri_tax_due == 'yes' else None
                )

                # =========================
                # STEP 4: OWNER DETAILS
                # =========================
                property_obj.owner_name = request.POST.get('owner_name')
                property_obj.owner_contact = request.POST.get('owner_contact')
                property_obj.owner_email = request.POST.get('owner_email')
                property_obj.comm_residency = request.POST.get('comm_residency', 'resident')

                # =========================
                # FILE UPLOADS
                # =========================
                if 'encumbrance_cert' in request.FILES:
                    property_obj.encumbrance_cert = request.FILES['encumbrance_cert']

                if 'property_video' in request.FILES:
                    property_obj.property_video = request.FILES['property_video']

                property_obj.save()

                # =========================
                # MULTIPLE IMAGES
                # =========================
                images = request.FILES.getlist('property_images[]')
                current_count = property_obj.images.count()

                for img in images:
                    if current_count < 10:
                        AgriculturalResaleImage.objects.create(
                            property=property_obj,
                            image=img
                        )
                        current_count += 1

            return JsonResponse({
                'status': 'success',
                'message': 'Property updated successfully!',
                # ✅ FIXED: Resolve the URL properly for the JS redirect
                'redirect_url': reverse('agricultural_resale_list')
            })

        except Exception as e:
            return JsonResponse({
                'status': 'error',
                'message': str(e)
            })

    return render(
        request,
        'admin_user/Resale/edit_agricultural_resale.html',
        {'property': property_obj}
    )


def download_agri_sample_excel(request):
    # EXACT MATCH WITH FORM + MODEL (NO EXTRA URL FIELDS)
    columns = [
        # STEP 1 (Form + DB)
        "title", "agriculture_property_type", "area", "state", "city",
        "district", "taluka", "village", "property_address",

        # STEP 2
        "soil_type", "water_source", "irrigation_facility", "fertility_status",
        "previous_crops", "resale_agricultural_desc",

        # STEP 3
        "expected_price", "brokerage", "brokerage_percentage", "manual_brokerage",
        "ownership_type", "agri_loan", "loan_amount",
        "agri_tenants", "tenant_details",
        "agri_dispute", "dispute_details",
        "agri_tax_due", "pending_tax_amount",

        # STEP 4 (Owner)
        "owner_name", "owner_contact", "owner_email", "comm_residency",

        # UPLOADER (IMPORTANT)
        "uploaded_by_name", "uploaded_by_email", "uploaded_by_contact", "uploaded_by_role"
    ]

    data = [[
        # STEP 1
        "Fertile Agricultural Land", "agriculture_land", 5.5, "Maharashtra", "Nagpur",
        "Nagpur", "Nagpur Rural", "Besa", "Near highway bridge",

        # STEP 2
        "black", "well", "yes", "high",
        "Wheat", "Excellent land for farming",

        # STEP 3
        5000000, "Yes", "2%", "",
        "freehold", "yes", 200000,
        "no", "",
        "no", "",
        "no", "",

        # STEP 4
        "Ramesh Patil", "9876543210", "ramesh@example.com", "resident",

        # UPLOADER (for reference only, NOT used in import)
        "Admin Name", "admin@mail.com", "9999999999", "Admin"
    ]]

    df = pd.DataFrame(data, columns=columns)

    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Template')

    output.seek(0)
    response = HttpResponse(
        output.read(),
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = 'attachment; filename="Agricultural_Template.xlsx"'
    return response

def delete_agricultural_property(request, pk):
    if request.method == 'POST':
        try:
            property_obj = get_object_or_404(AgriculturalResaleProperty, pk=pk)
            property_obj.delete()
            
            return JsonResponse({
                'status': 'success', 
                'message': 'Property has been permanently deleted.'
            })
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
            
    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'})




def view_agricultural_property(request, pk):
    # Ensure admin is logged in (optional, based on your session logic)
    session_id = request.session.get('Admin_id')
    if not session_id:
        return redirect('admin_login_url_name') # Change to your login URL name

    # Fetch the property
    property_obj = get_object_or_404(AgriculturalResaleProperty, pk=pk)
    
    context = {
        'property': property_obj
    }
    return render(request, 'admin_user/Resale//view_agricultural_resale.html', context)

####################END Views Section For AGRICULTURAL Resale Property #######################################



#######################Start View SEO MODULE SECTION###################################

def seo_list(request):
    seo_pages = LocationSEO.objects.all().order_by('-id')
    return render(request, "admin_user/Seo_Module/seo_list.html", {"seo_pages": seo_pages})




#######################End View SEO MODULE SECTION###################################



#######################Start View BLOG MODULE SECTION###################################


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

    return render(request, "admin_user/Seo_Module/Blog_Pages/blog_add.html")






def blog_list(request):
    blogs = Blog.objects.all().order_by("-date_posted")
    return render(request, "admin_user/Seo_Module/Blog_Pages/blog_list.html", {"blogs": blogs})


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

    return render(request, "admin_user/Seo_Module/Blog_Pages/blog_edit.html", {"blog": blog})



def import_blog_excel(request):
    if request.method == 'POST':
        excel_file = request.FILES.get('file')
        
        # Validation
        if not excel_file or not excel_file.name.endswith('.xlsx'):
            return JsonResponse({'status': 'error', 'message': 'Please upload a valid .xlsx file.'})

        try:
            wb = openpyxl.load_workbook(excel_file)
            sheet = wb.active
            
            # Assuming Excel columns are: [Title, Category, Author, Reading Time, Content]
            imported_count = 0
            for row in sheet.iter_rows(min_row=2, values_only=True): # Start from row 2 to skip headers
                if len(row) >= 5:
                    title = row[0]
                    category = row[1] if row[1] else ""
                    author = row[2] if row[2] else ""
                    reading_time = str(row[3]) if row[3] else ""
                    content = row[4] if row[4] else ""
                    
                    if title: # Only save if title exists
                        Blog.objects.create(
                            title=title,
                            category=category,
                            author=author,
                            reading_time=reading_time,
                            content=content
                        )
                        imported_count += 1
            
            return JsonResponse({'status': 'success', 'imported': imported_count})
            
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})

    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'})

#######################END View BLOG MODULE SECTION###################################


#######################START View SERVICES LANDING PAGE  MODULE SECTION###################################

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

    return render(request, "admin_user/Seo_Module/Services_Pages/add_service.html")


def delete_service(request, service_id):
    service = get_object_or_404(Service, id=service_id)
    service.delete()
    return redirect("services_list")



def edit_service(request, id):
    # Fetch the existing service using its ID
    service = get_object_or_404(Service, id=id)

    if request.method == "POST":
        # Get data from the form
        title = request.POST.get("title")
        icon = request.POST.get("icon")
        short_description = request.POST.get("short_description")
        content = request.POST.get("content")
        featured_image = request.FILES.get("featured_image")
        
        # Update the object
        service.title = title
        service.icon = icon
        service.short_description = short_description
        service.content = content
        
        # Only update the image if a new one was uploaded
        if featured_image:
            service.featured_image = featured_image
            
        # service.is_active = bool(request.POST.get('is_active')) # Uncomment if using active status

        # Save to database
        service.save()
        
        # Redirect back to the services list
        return redirect("services_list")

    # For a GET request, pass the service object to the template
    context = {
        'service': service
    }
    return render(request, "admin_user/Seo_Module/Services_Pages/edit_service.html", context)


def services_list(request):
    services = Service.objects.all().order_by('-id')
    return render(request, 'admin_user/Seo_Module/Services_Pages/services_list.html', {'services': services})





def import_services_excel(request):
    if request.method == 'POST':
        excel_file = request.FILES.get('file')
        
        # Validation
        if not excel_file or not excel_file.name.endswith('.xlsx'):
            return JsonResponse({'status': 'error', 'message': 'Please upload a valid .xlsx file.'})

        try:
            wb = openpyxl.load_workbook(excel_file)
            sheet = wb.active
            
            # Assuming Excel columns are: [Title, Icon, Short Description, Content]
            imported_count = 0
            for row in sheet.iter_rows(min_row=2, values_only=True): # Start from row 2 to skip headers
                if len(row) >= 4:
                    title = row[0]
                    icon = row[1] if row[1] else "bi bi-check-circle" # Default icon fallback
                    short_description = row[2] if row[2] else ""
                    content = row[3] if row[3] else ""
                    
                    if title: # Only save if title exists
                        Service.objects.create(
                            title=title,
                            icon=icon,
                            short_description=short_description,
                            content=content
                        )
                        imported_count += 1
            
            return JsonResponse({'status': 'success', 'imported': imported_count})
            
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})

    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'})





#######################END View SERVICES LANDING PAGE  MODULE SECTION###################################