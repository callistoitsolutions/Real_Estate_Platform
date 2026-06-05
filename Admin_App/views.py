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
import io
from collections import OrderedDict
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter
from django.http import HttpResponse

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
from django.utils import timezone


import csv
import json
# I added 'Sum' to the end of this line:
from django.db.models import Q, Count, Avg, Max, Min, Sum
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import render

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
    if request.method == "POST":
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
        'Relationship Manager': 'Update_RM',             
        'Landlord': 'Update_Landlord', 
        'Tenant': 'Update_Tenant',     
        'Buyer': 'Update_Buyer',
        'Agent': 'Update_Agent',
        'Agency/Builder': 'Update_Agency',
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
    # 3. FETCH NEW CONTACTS ENQUIRIES 
    # ==========================================
    recent_contacts = Contact_Enquiry.objects.filter(contact_enquiry_date=today).order_by('-contact_enquiry_date')[:10]
    for con in recent_contacts:

        contact_url = reverse("View_Contact_Enquiry", args=[con.id])
        
        master_feed.append({
            'category': 'contact', 
            'title': "New Contact Enquiry",
            'desc': f"{con.contact_name} and contact {con.contact_phone}",
            'timestamp': con.contact_enquiry_date,
            'time': con.contact_enquiry_time,
            'url': contact_url 
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


############### Views start for contact enquiries list #####################

def Contact_Enquiries_List(request):
    session_id = request.session.get('Admin_id')
    if session_id:
        admin_obj = Admin_Login.objects.get(id=session_id)

        contacts_en_obj = Contact_Enquiry.objects.all().order_by('-id')
        contacts_en_obj_count = Contact_Enquiry.objects.all().count()

        rendered = render_to_string("admin_user/render_to_string/R_Contact/r_t_s_enquiry.html",{'contacts_en_obj':contacts_en_obj,'contacts_en_obj_count':contacts_en_obj_count})

        context = {'admin_obj':admin_obj,'contact_enquiries_list':rendered}

        return render(request,"admin_user/Contact_Enquiry/contact_enquiry.html",context)
    else:
        return render(request,'home_page/Adminlogin.html')

############ Views end for contact enquiries list ###########################


############ Views start for delete contact enquiry ######################

@csrf_exempt
def Delete_Contact_Enquiry(request):
    try:
        try:
            enquiry_id = request.POST.get('enquiry_id')
            Contact_Enquiry.objects.filter(id=enquiry_id).delete()
            return JsonResponse({'status':'1', 'msg':'Contact enquiry details deleted successfully...'})
        except:
            traceback.print_exc()
            return JsonResponse({"status":"0", "msg" : "Something went wrong..."})
    except:
        traceback.print_exc()
        return JsonResponse({"status":"0", "msg" : "Something went wrong..."})



############## Views end for delete contact enquiry ######################


############ Views start for view contact enquiries ####################

def  View_Contact_Enquiry(request,id):
    session_id = request.session.get('Admin_id')
    if session_id:
        admin_obj = Admin_Login.objects.get(id=session_id)

        contact = Contact_Enquiry.objects.get(id=id)

        context = {'admin_obj':admin_obj,'contact':contact}

        return render(request,"admin_user/Contact_Enquiry/view_enquiry.html",context)
    else:
        return render(request,'home_page/Adminlogin.html')

############## Views end for view contact enquiries ######################
   

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


############## Views start for normal faqs list ######################

def Faqs_List(request):
    session_id = request.session.get('Admin_id')
    if session_id:
        admin_obj = Admin_Login.objects.get(id=session_id)

        faqs_obj = NormalFAQ.objects.all().order_by('-id')
        faqs_obj_count = NormalFAQ.objects.all().count()

        rendered = render_to_string("admin_user/render_to_string/R_FAQ/r_t_s_faq.html",{'faqs_obj':faqs_obj,'faqs_obj_count':faqs_obj_count})

        context = {'admin_obj':admin_obj,'faqs_list':rendered}

        return render(request,"admin_user/FAQ/display_faq.html",context)
    else:
        return render(request,'home_page/Adminlogin.html')

######### Views end for normal faqs list ###############################


########### Views start for add normal faq #############################

def Add_FAQ(request):
    session_id = request.session.get('Admin_id')
    if session_id:
        admin_obj = Admin_Login.objects.get(id=session_id)

        context = {'admin_obj':admin_obj}

        return render(request,"admin_user/FAQ/add_faq.html",context)
    else:
        return render(request,'home_page/Adminlogin.html')

############## Views end for add normal faq #########################


############## Views start for ajax for normal faq ####################

@csrf_exempt
def Faq_Ajax(request):
    data = request.POST.dict()

    if data.get('id') == "":
        data.pop("id", None)        
        data['faq_date'] = datetime.today()
        data['faq_time'] = datetime.now()
        NormalFAQ.objects.create(**data)
        return JsonResponse({"status":"1", "msg" : f"FAQ Details added successfully"})

    # UPDATE MODE
    else:
        try:
            faqs = NormalFAQ.objects.get(id=data['id'])
        except NormalFAQ.DoesNotExist:
            return JsonResponse({'status': '0', 'msg': 'FAQ Details not found'})


        # Update withdraw fields (unchanged)
        for key, value in data.items():
            setattr(faqs, key, value)

        faqs.save()
        return JsonResponse({"status":"1", "msg" : f"FAQ Details updated successfully"})

############ Views end for ajax for normal faq ##########################


############## Views start for delete faqs #########################

@csrf_exempt
def Delete_Faqs(request):
    try:
        try:
            faq_id = request.POST.get('faq_id')
            NormalFAQ.objects.filter(id=faq_id).delete()
            return JsonResponse({'status':'1', 'msg':'FAQ details deleted successfully...'})
        except:
            traceback.print_exc()
            return JsonResponse({"status":"0", "msg" : "Something went wrong..."})
    except:
        traceback.print_exc()
        return JsonResponse({"status":"0", "msg" : "Something went wrong..."})

############# Views end for delete faqs ###############################


############## Views start for update faqs #######################

def Update_Faqs(request,id):
    session_id = request.session.get('Admin_id')
    if session_id:
        admin_obj = Admin_Login.objects.get(id=session_id)

        faq = NormalFAQ.objects.get(id=id)

        context = {'admin_obj':admin_obj,'faq':faq}

        return render(request,"admin_user/FAQ/update_faq.html",context)
    else:
        return render(request,'home_page/Adminlogin.html')

############## Views end for update faqs ############################


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



# ─────────────────────────────────────────────
#  Commercial List View
# ─────────────────────────────────────────────







def commercial_list(request):
    session_id = request.session.get('Admin_id')
    if not session_id:
        return render(request, 'home_page/Adminlogin.html')

    admin_obj = Admin_Login.objects.get(id=session_id)

    # ── 1. GET ALL SEARCH PARAMS ──
    search_query    = request.GET.get('search', '').strip()
    prop_type_query = request.GET.get('property_type', '').strip()
    city_query      = request.GET.get('city', '').strip()
    zone_query      = request.GET.get('zone_type', '').strip()
    possession_query= request.GET.get('possession', '').strip()
    listed_by_query = request.GET.get('listed_by', '').strip()
    budget_query    = request.GET.get('budget', '').strip()
    from_date       = request.GET.get('from_date', '').strip()
    to_date         = request.GET.get('to_date', '').strip()

    # ── Base queryset ──
    try:
        properties = CommercialRentalProperty.objects.filter(is_deleted=False).order_by('-id')
    except Exception:
        properties = CommercialRentalProperty.objects.all().order_by('-id')

    # ── 2. APPLY FILTERS ──
    if search_query:
        properties = properties.filter(
            Q(property_title__icontains=search_query) |
            Q(building_name__icontains=search_query) |
            Q(city__icontains=search_query) |
            Q(area_locality__icontains=search_query) |
            Q(owner_name__icontains=search_query)
        )

    if prop_type_query and prop_type_query != 'All Types':
        properties = properties.filter(property_type__icontains=prop_type_query)
    if city_query and city_query != 'All Cities':
        properties = properties.filter(city__icontains=city_query)
    if zone_query and zone_query != 'All Zones':
        properties = properties.filter(zone_type__icontains=zone_query)
    if possession_query and possession_query != 'All Status':
        properties = properties.filter(possession_status__icontains=possession_query)
    if listed_by_query and listed_by_query != 'All Roles':
        properties = properties.filter(uploaded_by_role__icontains=listed_by_query)

    # Date range filter
    if from_date:
        try:
            properties = properties.filter(created_at__date__gte=from_date)
        except Exception:
            pass
    if to_date:
        try:
            properties = properties.filter(created_at__date__lte=to_date)
        except Exception:
            pass

    # Budget ranges
    if budget_query and budget_query != 'All Budgets':
        if budget_query == 'under_25k':
            properties = properties.filter(expected_rent__lt=25000)
        elif budget_query == '25k_1L':
            properties = properties.filter(expected_rent__gte=25000, expected_rent__lte=100000)
        elif budget_query == '1L_5L':
            properties = properties.filter(expected_rent__gte=100000, expected_rent__lte=500000)
        elif budget_query == 'above_5L':
            properties = properties.filter(expected_rent__gt=500000)

    # ── CSV Download ──
    if request.GET.get('download') == 'csv':
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="commercial_rental_properties.csv"'
        writer = csv.writer(response)
        writer.writerow([
            'Property Title', 'Property Type', 'City', 'Area/Locality', 'Address',
            'Building Name', 'Possession Status', 'Available From', 'Age', 'Zone Type',
            'Location Hub', 'Condition', 'Ownership Type', 'Construction Status',
            'Builtup Area', 'Carpet Area', 'Expected Rent', 'Security Deposit',
            'Maintenance', 'Negotiable', 'Brokerage', 'Brokerage %', 'Manual Brokerage',
            'DG/UPS', 'Electricity', 'Water', 'Lock-in Period', 'Rent Increase',
            'Total Floors', 'Your Floor', 'Staircases', 'Passenger Lifts', 'Service Lifts',
            'Private Parking', 'Min Seats', 'Max Seats', 'Cabins', 'Meeting Rooms',
            'Private Washroom', 'Public Washroom', 'Flooring',
            'Owner Name', 'Contact Number', 'Email', 'Alternate Contact',
            'Uploaded By Name', 'Uploaded By Email', 'Uploaded By Contact', 'Uploaded By Role',
            'Created At',
        ])
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
                p.owner_name, p.contact_number, p.email, p.alternate_contact,
                p.uploaded_by_name, p.uploaded_by_email,
                p.uploaded_by_contact, p.uploaded_by_role,
                p.created_at.strftime('%d-%m-%Y') if p.created_at else '',
            ])
        return response

    # ── Pagination ──
    paginator    = Paginator(properties, 10)
    page_number  = request.GET.get('page', 1)
    page_obj     = paginator.get_page(page_number)
    filtered_count = properties.count()

    # ════════════════════════════════════════════════
    # ALL-PROPS STATS (always on unfiltered dataset)
    # ════════════════════════════════════════════════
    try:
        all_props = CommercialRentalProperty.objects.filter(is_deleted=False)
    except Exception:
        all_props = CommercialRentalProperty.objects.all()

    total_count = all_props.count()

    # ── Dropdown unique values ──
    unique_property_types = (all_props
        .exclude(property_type__isnull=True).exclude(property_type='')
        .values_list('property_type', flat=True).distinct().order_by('property_type'))
    unique_cities = (all_props
        .exclude(city__isnull=True).exclude(city='')
        .values_list('city', flat=True).distinct().order_by('city'))
    unique_zones = (all_props
        .exclude(zone_type__isnull=True).exclude(zone_type='')
        .values_list('zone_type', flat=True).distinct().order_by('zone_type'))
    unique_possession = (all_props
        .exclude(possession_status__isnull=True).exclude(possession_status='')
        .values_list('possession_status', flat=True).distinct())
    unique_roles = (all_props
        .exclude(uploaded_by_role__isnull=True).exclude(uploaded_by_role='')
        .values_list('uploaded_by_role', flat=True).distinct())

    # ── Occupancy KPIs ──
    active_count   = all_props.exclude(possession_status__isnull=True).exclude(possession_status='').count()
    occupied_count = all_props.filter(possession_status__iexact='Occupied').count()
    vacant_count   = all_props.filter(possession_status__iexact='Ready to Move').count()
    occupancy_rate = round((occupied_count / total_count * 100)) if total_count > 0 else 0
    vacancy_rate   = round((vacant_count   / total_count * 100)) if total_count > 0 else 0

    # ── Revenue KPIs ──
    rent_stats = all_props.exclude(expected_rent__isnull=True).aggregate(
        avg_rent=Avg('expected_rent'),
        max_rent=Max('expected_rent'),
        min_rent=Min('expected_rent'),
    )
    avg_rent = rent_stats['avg_rent'] or 0
    max_rent = rent_stats['max_rent'] or 0
    min_rent = rent_stats['min_rent'] or 0
    total_revenue          = all_props.aggregate(total=Sum('expected_rent'))['total'] or 0
    total_security_deposit = all_props.aggregate(total=Sum('security_deposit'))['total'] or 0
    avg_deposit = (all_props.exclude(security_deposit__isnull=True)
                   .aggregate(avg=Avg('security_deposit'))['avg'] or 0)

    try:
        avg_area = (all_props.exclude(builtup_area__isnull=True)
                    .aggregate(avg=Avg('builtup_area'))['avg'] or 0)
    except Exception:
        avg_area = 0

    # ── Business KPIs ──
    premium_properties_count    = all_props.filter(expected_rent__gte=100000).count()
    affordable_properties_count = all_props.filter(expected_rent__lt=25000).count()
    short_lease_count           = all_props.filter(lockin_period__icontains='6').count()
    long_lease_count            = all_props.filter(lockin_period__icontains='12').count()
    with_owner_count            = all_props.exclude(owner_name__isnull=True).exclude(owner_name='').count()
    city_count                  = (all_props.exclude(city__isnull=True).exclude(city='')
                                   .values('city').distinct().count())
    try:
        with_images_count = all_props.filter(images__isnull=False).distinct().count()
    except Exception:
        with_images_count = 0

    # ── Percentages ──
    verified_pct = round((with_owner_count     / total_count * 100)) if total_count > 0 else 0
    image_pct    = round((with_images_count    / total_count * 100)) if total_count > 0 else 0
    premium_pct  = round((premium_properties_count / total_count * 100)) if total_count > 0 else 0

    # ── Uploaded file names (for bulk delete) ──
    try:
        uploaded_files = (all_props.exclude(upload_file_name__isnull=True)
                          .exclude(upload_file_name='')
                          .values_list('upload_file_name', flat=True).distinct())
    except Exception:
        uploaded_files = []

    # ════════════════════════════════════════════
    # CHART DATA  (JSON → template → JS)
    # ════════════════════════════════════════════

    # 1. Property-type pie
    prop_type_dist = list(
        all_props.exclude(property_type__isnull=True).exclude(property_type='')
        .values('property_type').annotate(cnt=Count('id')).order_by('-cnt')[:8]
    )
    prop_type_labels_json = json.dumps([x['property_type'] for x in prop_type_dist])
    prop_type_counts_json = json.dumps([x['cnt']           for x in prop_type_dist])

    # 2. Rent-range bar
    rent_range_data = {
        'Under ₹25k':  all_props.filter(expected_rent__lt=25000).count(),
        '₹25k–1L':     all_props.filter(expected_rent__gte=25000,  expected_rent__lt=100000).count(),
        '₹1L–5L':      all_props.filter(expected_rent__gte=100000, expected_rent__lt=500000).count(),
        'Above ₹5L':   all_props.filter(expected_rent__gte=500000).count(),
    }
    rent_range_labels_json = json.dumps(list(rent_range_data.keys()))
    rent_range_counts_json = json.dumps(list(rent_range_data.values()))

    # 3. Occupancy doughnut
    occupancy_json = json.dumps([occupied_count, vacant_count, max(0, total_count - occupied_count - vacant_count)])

    # 4. Monthly listed count + expected revenue (last 6 months)
    six_months_ago = timezone.now() - timedelta(days=180)
    monthly_qs = (
        all_props.filter(created_at__gte=six_months_ago)
        .annotate(month=TruncMonth('created_at'))
        .values('month')
        .annotate(revenue=Sum('expected_rent'), cnt=Count('id'))
        .order_by('month')
    )
    monthly_labels_json  = json.dumps([x['month'].strftime('%b %Y') for x in monthly_qs])
    monthly_revenue_json = json.dumps([float(x['revenue'] or 0) for x in monthly_qs])

    # ── Placeholder quick stats (replace with real models if available) ──
    total_tenants    = occupied_count
    collection_rate  = 0
    pending_payments = 0
    maintenance_req  = 0

    context = {
        'admin_obj': admin_obj,
        'page_obj': page_obj,

        # Search params
        'search_query':     search_query,
        'prop_type_query':  prop_type_query,
        'city_query':       city_query,
        'zone_query':       zone_query,
        'possession_query': possession_query,
        'listed_by_query':  listed_by_query,
        'budget_query':     budget_query,
        'from_date':        from_date,
        'to_date':          to_date,

        # Dropdown options
        'unique_property_types': unique_property_types,
        'unique_cities':         unique_cities,
        'unique_zones':          unique_zones,
        'unique_possession':     unique_possession,
        'unique_roles':          unique_roles,
        'uploaded_files':        uploaded_files,

        # KPI numbers
        'filtered_count':            filtered_count,
        'total_count':               total_count,
        'active_count':              active_count,
        'occupied_count':            occupied_count,
        'vacant_count':              vacant_count,
        'occupancy_rate':            occupancy_rate,
        'vacancy_rate':              vacancy_rate,
        'avg_rent':                  avg_rent,
        'max_rent':                  max_rent,
        'min_rent':                  min_rent,
        'total_revenue':             total_revenue,
        'total_security_deposit':    total_security_deposit,
        'avg_deposit':               avg_deposit,
        'avg_area':                  avg_area,
        'premium_properties_count':  premium_properties_count,
        'affordable_properties_count': affordable_properties_count,
        'ready_to_move_count':       vacant_count,
        'short_lease_count':         short_lease_count,
        'long_lease_count':          long_lease_count,
        'with_owner_count':          with_owner_count,
        'with_images_count':         with_images_count,
        'city_count':                city_count,
        'verified_pct':              verified_pct,
        'image_pct':                 image_pct,
        'premium_pct':               premium_pct,

        # Quick-stat placeholders
        'total_tenants':    total_tenants,
        'collection_rate':  collection_rate,
        'pending_payments': pending_payments,
        'maintenance_req':  maintenance_req,

        # Chart JSON
        'prop_type_labels_json':  prop_type_labels_json,
        'prop_type_counts_json':  prop_type_counts_json,
        'rent_range_labels_json': rent_range_labels_json,
        'rent_range_counts_json': rent_range_counts_json,
        'occupancy_json':         occupancy_json,
        'monthly_labels_json':    monthly_labels_json,
        'monthly_revenue_json':   monthly_revenue_json,
    }
    return render(request, 'admin_user/Reports/Rental/commercial_list.html', context)

# ─────────────────────────────────────────────
#  Import Excel View
# ─────────────────────────────────────────────

def _decimal(v):
    if v is None or str(v).strip() == '': return None
    try: return float(str(v))
    except: return None


def _email(v):
    return _str(v)




COMMERCIAL_RENTAL_COLUMN_MAP = [
    ("property_type",         "property_type",         _str),
    ("property_condition",    "property_condition",    _str),
    ("city",                  "city",                  _str),
    ("area_locality",         "area_locality",         _str),
    ("property_address",      "property_address",      _str),
    ("building_name",         "building_name",         _str),
    ("possession_status",     "possession_status",     _str),
    ("available_from",        "available_from",        _date),
    ("age_of_property",       "age_of_property",       _str),
    ("zone_type",             "zone_type",             _str),
    ("location_hub",          "location_hub",          _str),
    ("ownership_type",        "ownership_type",        _str),
    ("construction_status",   "construction_status",   _str),
    ("builtup_area",          "builtup_area",          _int),
    ("carpet_area",           "carpet_area",           _int),
    ("expected_rent",         "expected_rent",         _int),
    ("security_deposit",      "security_deposit",      _int),
    ("maintenance_charges",   "maintenance_charges",   _int),
    ("negotiable",            "negotiable",            _bool),
    ("brokerage",             "brokerage",             _str),
    ("brokerage_percentage",  "brokerage_percentage",  _str),
    ("manual_brokerage",      "manual_brokerage",      _str),
    ("dg_ups_included",       "dg_ups_included",       _bool),
    ("electricity_included",  "electricity_included",  _bool),
    ("water_included",        "water_included",        _bool),
    ("lockin_period",         "lockin_period",         _int),
    ("rent_increase",         "rent_increase",         _decimal),
    ("total_floors",          "total_floors",          _int),
    ("your_floor",            "your_floor",            _int),
    ("staircases",            "staircases",            _int),
    ("passenger_lifts",       "passenger_lifts",       _int),
    ("service_lifts",         "service_lifts",         _int),
    ("private_parking",       "private_parking",       _int),
    ("min_seats",             "min_seats",             _int),
    ("max_seats",             "max_seats",             _int),
    ("cabins",                "cabins",                _int),
    ("meeting_rooms",         "meeting_rooms",         _int),
    ("private_washroom",      "private_washroom",      _int),
    ("public_washroom",       "public_washroom",       _int),
    ("flooring_type",         "flooring_type",         _str),
    ("amenities",             "amenities",             _str),
    ("nearby_facilities",     "nearby_facilities",     _str),
    ("property_summary",      "property_summary",      _str),
    ("owner_name",            "owner_name",            _str),
    ("contact_number",        "contact_number",        _str),
    ("email",                 "email",                 _email),
    ("alternate_contact",     "alternate_contact",     _str),
    ("uploaded_by_name",      "uploaded_by_name",      _str),
    ("uploaded_by_email",     "uploaded_by_email",     _str),
    ("uploaded_by_contact",   "uploaded_by_contact",   _str),
    ("uploaded_by_role",      "uploaded_by_role",      _str),
]

COMMERCIAL_RENTAL_REQUIRED_DEFAULTS = {
    'property_type': 'office-space', 'city': '', 'area_locality': '',
    'property_address': '', 'building_name': '', 'possession_status': 'ready-to-move',
    'age_of_property': '0-1', 'property_condition': 'bare-shell',
    'ownership_type': 'freehold', 'builtup_area': 0, 'expected_rent': 0,
    'owner_name': '', 'contact_number': '', 'email': '',
}


@require_POST
def import_commercial_excel(request):
    excel_file = request.FILES.get("commercial_file")
    if not excel_file:
        return JsonResponse({"status": "error", "message": "No file uploaded."}, status=400)
    if not excel_file.name.endswith(".xlsx"):
        return JsonResponse({"status": "error", "message": "Only .xlsx files accepted."}, status=400)

    try:
        wb, ws, headers = _load_new_excel(excel_file)
    except Exception as e:
        return JsonResponse({"status": "error", "message": f"Cannot open file: {e}"}, status=400)

    created, errors = 0, []
    file_name = excel_file.name

    for row_idx, row in enumerate(ws.iter_rows(min_row=4, values_only=True), start=4):
        if all(v is None or str(v).strip() == "" for v in row):
            continue

        obj_data = {**COMMERCIAL_RENTAL_REQUIRED_DEFAULTS, "upload_file_name": file_name}
        row_error = None

        for excel_col, model_field, converter in COMMERCIAL_RENTAL_COLUMN_MAP:
            raw = _get_cell(row, headers.get(excel_col))
            try:
                val = converter(raw)
                if val is not None:
                    obj_data[model_field] = val
            except Exception as e:
                row_error = f"Row {row_idx} '{excel_col}': {e}"
                break

        if row_error:
            errors.append(row_error)
            continue

        # amenities / nearby_facilities are JSONField — convert comma-sep string → list
        for fld in ('amenities', 'nearby_facilities'):
            raw_str = obj_data.get(fld)
            if isinstance(raw_str, str) and raw_str:
                obj_data[fld] = [x.strip() for x in raw_str.split(',') if x.strip()]
            else:
                obj_data[fld] = []

        try:
            CommercialRentalProperty.objects.create(**obj_data)
            created += 1
        except Exception as e:
            errors.append(f"Row {row_idx} DB: {e}")

    wb.close()
    return JsonResponse({
        "status": "success",
        "message": f"{created} record(s) imported. {len(errors)} error(s).",
        "created": created, "error_count": len(errors), "errors": errors[:20],
    })


def download_commercial_template(request):
    """New-style Commercial Rental template: Row1=banners, Row2=labels, Row3=hints, Row4=sample."""
   

    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Commercial Rental"

    HDR_BG  = "667EEA"   # section banner – indigo
    REQ_BG  = "FEF3C7"   # required field – amber
    OPT_BG  = "F0FDF4"   # optional field – green-tint
    SAMP_BG = "ECFDF5"   # sample row – mint

    thin = Side(style="thin", color="CBD5E1")
    bdr  = Border(left=thin, right=thin, top=thin, bottom=thin)

    # (section, excel_col, required, hint, sample)
    COLS = [
        # ── Basic Info ────────────────────────────────────────────────────────
        ("Basic Info", "property_type",       True,  "office-space / shop / warehouse / industrial / land",          "office-space"),
        ("Basic Info", "property_condition",  True,  "bare-shell / warm-shell / fitted / furnished",                 "bare-shell"),
        ("Basic Info", "city",                True,  "City name",                                                     "Mumbai"),
        ("Basic Info", "area_locality",       True,  "Area/locality",                                                 "BKC"),
        ("Basic Info", "property_address",    True,  "Complete address",                                              "Tower A, BKC, Mumbai"),
        ("Basic Info", "building_name",       True,  "Building/project name",                                         "Platina Tower"),
        ("Basic Info", "possession_status",   True,  "ready-to-move / under-construction",                           "ready-to-move"),
        ("Basic Info", "available_from",      False, "YYYY-MM-DD",                                                    "2025-08-01"),
        ("Basic Info", "age_of_property",     True,  "0-1 / 1-3 / 3-5 / 5-10 / 10+",                               "1-3"),
        ("Basic Info", "zone_type",           False, "industrial / commercial / residential / special-economic",      "commercial"),
        ("Basic Info", "location_hub",        False, "it-park / business-district / mall / standalone",              "business-district"),
        ("Basic Info", "ownership_type",      True,  "freehold / leasehold / co-operative",                          "freehold"),
        ("Basic Info", "construction_status", False, "new / resale",                                                  "resale"),
        # ── Area & Pricing ────────────────────────────────────────────────────
        ("Area & Pricing", "builtup_area",         True,  "Number in sq.ft",                                         "2000"),
        ("Area & Pricing", "carpet_area",          False, "Number in sq.ft",                                         "1700"),
        ("Area & Pricing", "expected_rent",        True,  "Monthly rent in ₹",                                      "85000"),
        ("Area & Pricing", "security_deposit",     False, "Deposit in ₹",                                           "500000"),
        ("Area & Pricing", "maintenance_charges",  False, "Monthly maintenance in ₹",                               "5000"),
        ("Area & Pricing", "negotiable",           False, "Yes / No",                                                "Yes"),
        ("Area & Pricing", "brokerage",            False, "Yes / No",                                                "No"),
        ("Area & Pricing", "brokerage_percentage", False, "1% / 1.5% / 2% / Negotiable / Manual",                   ""),
        ("Area & Pricing", "manual_brokerage",     False, "e.g. 2.5% (if Manual)",                                  ""),
        ("Area & Pricing", "dg_ups_included",      False, "true / false",                                           "false"),
        ("Area & Pricing", "electricity_included", False, "true / false",                                           "false"),
        ("Area & Pricing", "water_included",       False, "true / false",                                           "false"),
        ("Area & Pricing", "lockin_period",        False, "Lock-in months",                                         "6"),
        ("Area & Pricing", "rent_increase",        False, "% per year e.g. 5",                                      "5"),
        # ── Building ──────────────────────────────────────────────────────────
        ("Building", "total_floors",     False, "Total floors in building",        "10"),
        ("Building", "your_floor",       False, "Floor of this property",          "4"),
        ("Building", "staircases",       False, "Number of staircases",            "2"),
        ("Building", "passenger_lifts",  False, "Number (use 0 if none)",          "2"),
        ("Building", "service_lifts",    False, "Number (use 0 if none)",          "1"),
        ("Building", "private_parking",  False, "Number of private parking spots", "2"),
        ("Building", "min_seats",        False, "Minimum seating capacity",        "20"),
        ("Building", "max_seats",        False, "Maximum seating capacity",        "50"),
        ("Building", "cabins",           False, "Number of cabins",                "5"),
        ("Building", "meeting_rooms",    False, "Number of meeting rooms",         "2"),
        ("Building", "private_washroom", False, "Number (use 0)",                  "1"),
        ("Building", "public_washroom",  False, "Number (use 0)",                  "2"),
        ("Building", "flooring_type",    False, "marble / vitrified / granite / wooden / ceramic", "vitrified"),
        # ── Amenities ─────────────────────────────────────────────────────────
        ("Amenities", "amenities",          True,  "Comma-sep e.g. Wi-Fi,AC,CCTV,Generator",  "Wi-Fi,AC,CCTV"),
        ("Amenities", "nearby_facilities",  True,  "Comma-sep e.g. Metro,Bank,Parking",        "Metro,Bank"),
        ("Amenities", "property_summary",   False, "Short plain-text description",              "Prime BKC office with fit-out."),
        # ── Contact ───────────────────────────────────────────────────────────
        ("Contact", "owner_name",        True,  "Full name",           "Rahul Mehta"),
        ("Contact", "contact_number",    True,  "+91 XXXXXXXXXX",      "9876543210"),
        ("Contact", "email",             True,  "email@example.com",   "rahul@email.com"),
        ("Contact", "alternate_contact", False, "+91 XXXXXXXXXX",      ""),
        ("Contact", "uploaded_by_name",  False, "Auto-filled",         ""),
        ("Contact", "uploaded_by_email", False, "Auto-filled",         ""),
        ("Contact", "uploaded_by_contact",False,"Auto-filled",         ""),
        ("Contact", "uploaded_by_role",  False, "Auto-filled",         ""),
    ]

    # ── Row 1: section banners ────────────────────────────────────────────────
    sec_spans = OrderedDict()
    for i, (sec, *_) in enumerate(COLS):
        sec_spans.setdefault(sec, []).append(i + 1)

    for sec, cols in sec_spans.items():
        c = ws.cell(row=1, column=cols[0], value=f"📋 {sec}")
        c.font      = Font(bold=True, color="FFFFFF", name="Arial", size=11)
        c.fill      = PatternFill("solid", fgColor=HDR_BG)
        c.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
        c.border    = bdr
        if len(cols) > 1:
            ws.merge_cells(start_row=1, start_column=cols[0],
                           end_row=1,   end_column=cols[-1])

    # ── Rows 2 / 3 / 4 ───────────────────────────────────────────────────────
    for ci, (sec, field, req, hint, sample) in enumerate(COLS, 1):
        # Row 2 – label
        lc = ws.cell(row=2, column=ci, value=field + (" *" if req else ""))
        lc.font      = Font(bold=True, color="1E293B", name="Arial", size=9)
        lc.fill      = PatternFill("solid", fgColor=REQ_BG if req else OPT_BG)
        lc.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
        lc.border    = bdr

        # Row 3 – hint
        hc = ws.cell(row=3, column=ci, value=hint)
        hc.font      = Font(italic=True, color="64748B", name="Arial", size=8)
        hc.fill      = PatternFill("solid", fgColor="FFFFFF")
        hc.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
        hc.border    = bdr

        # Row 4 – sample
        sc = ws.cell(row=4, column=ci, value=sample)
        sc.font      = Font(name="Arial", size=9, color="065F46")
        sc.fill      = PatternFill("solid", fgColor=SAMP_BG)
        sc.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
        sc.border    = bdr

        ws.column_dimensions[get_column_letter(ci)].width = max(18, len(field) + 4)

    ws.row_dimensions[1].height = 28
    ws.row_dimensions[2].height = 36
    ws.row_dimensions[3].height = 42
    ws.row_dimensions[4].height = 26
    ws.freeze_panes = "A5"

    buf = io.BytesIO()
    wb.save(buf)
    buf.seek(0)
    response = HttpResponse(
        buf.getvalue(),
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )
    response["Content-Disposition"] = 'attachment; filename="Commercial_Rental_Template.xlsx"'
    return response




############### Views end for commercial property list ########################


######### Views start for pg co living rental list ########################



   





# ─────────────────────────────────────────────────────────────
# LIST VIEW
# ─────────────────────────────────────────────────────────────
<<<<<<< HEAD



=======
# def pg_list(request):
#     session_id = request.session.get('Admin_id')
#     if not session_id:
#         return render(request, 'home_page/Adminlogin.html')

#     try:
#         admin_obj = Admin_Login.objects.get(id=session_id)
#     except Admin_Login.DoesNotExist:
#         return render(request, 'home_page/Adminlogin.html')

#     search_query = request.GET.get('search', '').strip()
#     pg_for_filter = request.GET.get('pg_for', '').strip()       # boys / girls / co-living
#     city_filter   = request.GET.get('city', '').strip()

#     # Base queryset — newest first
#     properties = PGColivingProperty.objects.all().order_by('-id')

#     # ── Search ────────────────────────────────────────────────
#     if search_query:
#         properties = properties.filter(
#             Q(pg_name__icontains=search_query)       |
#             Q(city__icontains=search_query)          |
#             Q(locality__icontains=search_query)      |
#             Q(building_name__icontains=search_query) |
#             Q(owner_name__icontains=search_query)    |
#             Q(contact_number__icontains=search_query)
#         )

#     # ── Filters ───────────────────────────────────────────────
#     if pg_for_filter:
#         properties = properties.filter(pg_for=pg_for_filter)

#     if city_filter:
#         properties = properties.filter(city__icontains=city_filter)

#     total_count = properties.count()

#     # ── CSV Download ──────────────────────────────────────────
#     if request.GET.get('download') == 'csv':
#         response = HttpResponse(content_type='text/csv')
#         response['Content-Disposition'] = 'attachment; filename="pg_coliving_properties.csv"'
#         writer = csv.writer(response)

#         writer.writerow([
#             'ID', 'PG Name', 'City', 'Locality', 'Building Name',
#             'PG For', 'Furnishing', 'Room Type', 'Total Beds',
#             'Rent', 'Security Deposit', 'Min Stay',
#             'Meals Available', 'Owner Name', 'Contact', 'Email',
#             'Added On',
#         ])

#         for p in properties:
#             writer.writerow([
#                 p.id,
#                 p.pg_name,
#                 p.city,
#                 p.locality,
#                 p.building_name or '',
#                 p.get_pg_for_display(),
#                 p.get_furnishing_type_display(),
#                 p.get_room_type_display(),
#                 p.total_beds,
#                 p.rent,
#                 p.security_deposit,
#                 p.minimum_stay,
#                 'Yes' if p.meals_available else 'No',
#                 p.owner_name,
#                 p.contact_number,
#                 p.email,
#                 p.created_at.strftime('%d-%m-%Y') if p.created_at else '',
#             ])

#         return response

#     # ── Pagination ────────────────────────────────────────────
#     paginator   = Paginator(properties, 10)
#     page_number = request.GET.get('page', 1)
#     page_obj    = paginator.get_page(page_number)

#     # Distinct cities for filter dropdown
#     cities = (PGColivingProperty.objects
#               .values_list('city', flat=True)
#               .distinct()
#               .order_by('city'))

#     print("----------------------------",admin_obj)

#     context = {
#         'admin_obj':     admin_obj,
#         'page_obj':      page_obj,
#         'search_query':  search_query,
#         'pg_for_filter': pg_for_filter,
#         'city_filter':   city_filter,
#         'total_count':   total_count,
#         'cities':        cities,
#     }
#     return render(request, 'admin_user/Reports/Rental/pg_list.html', context)
>>>>>>> d0f149b2c74d1fc5cd4a07f46e5105a392471ff5


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
        if User_Details.objects.filter(user_phone=data['user_phone']).exists():
            return JsonResponse({"status":"0", "msg" : f"User with this phone number already exists"})
        elif User_Details.objects.filter(user_email=data['user_email']).exists():
            return JsonResponse({"status":"0", "msg" : f"User with this email address already exists"})
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






def rental_residential_logs_view(request):
    # Base query initialization
    logs = RentalActivityLog.objects.all()

    # Capture URL GET search query parameters
    user_query = request.GET.get('user_query', '').strip()
    file_query = request.GET.get('file_query', '').strip()
    location_query = request.GET.get('location_query', '').strip()
    property_type = request.GET.get('property_type', '').strip()
    bhk_type = request.GET.get('bhk_type', '').strip()
    min_budget = request.GET.get('min_budget', '').strip()
    max_budget = request.GET.get('max_budget', '').strip()
    field_target = request.GET.get('field_target', '').strip()
    action_type = request.GET.get('action_type', '').strip()
    month_filter = request.GET.get('month_filter', '').strip()
    
    start_date_str = request.GET.get('start_date', '').strip()
    end_date_str = request.GET.get('end_date', '').strip()
    start_time_str = request.GET.get('start_time', '').strip()
    end_time_str = request.GET.get('end_time', '').strip()

    # 1. Build Property Specifications Pool Filter First
    property_pool = RentalResidentialProperty.objects.filter(is_deleted=False)
    has_property_filter = False

    if property_type:
        property_pool = property_pool.filter(property_type__icontains=property_type)
        has_property_filter = True
    if bhk_type:
        property_pool = property_pool.filter(bhk_type__icontains=bhk_type)
        has_property_filter = True
    if location_query:
        property_pool = property_pool.filter(
            Q(city__icontains=location_query) | 
            Q(locality__icontains=location_query) | 
            Q(address__icontains=location_query)
        )
        has_property_filter = True
    if min_budget and min_budget.isdigit():
        property_pool = property_pool.filter(monthly_rent__gte=int(min_budget))
        has_property_filter = True
    if max_budget and max_budget.isdigit():
        property_pool = property_pool.filter(monthly_rent__lte=int(max_budget))
        has_property_filter = True

    matched_property_ids = list(property_pool.values_list('rental_residential_id', flat=True))

    # 2. Apply Filters Across the Audit Logs Queryset
    log_conditions = Q()

    if user_query:
        log_conditions &= (Q(user_identity__icontains=user_query) | Q(user_role__icontains=user_query))
    if file_query:
        clean_file = file_query.replace('.xlsx', '').replace('.xls', '').strip()
        log_conditions &= Q(associated_file__icontains=clean_file)
    if action_type:
        log_conditions &= Q(action_type__iexact=action_type)
    if month_filter and month_filter.isdigit():
        log_conditions &= Q(timestamp__month=int(month_filter))
    if field_target:
        if field_target == 'city_locality':
            log_conditions &= (Q(targeted_fields__icontains='city') | Q(targeted_fields__icontains='locality'))
        elif field_target == 'owner_contact':
            log_conditions &= (Q(targeted_fields__icontains='owner') | Q(targeted_fields__icontains='contact'))
        else:
            log_conditions &= Q(targeted_fields__icontains=field_target)

    # Date-wise & Time-wise Precision Datetime Combiner Lookups
    if start_date_str:
        try:
            start_date_parsed = datetime.strptime(start_date_str, "%Y-%m-%d").date()
            if start_time_str:
                start_time_parsed = datetime.strptime(start_time_str, "%H:%M").time()
                log_conditions &= Q(timestamp__gte=datetime.combine(start_date_parsed, start_time_parsed))
            else:
                log_conditions &= Q(timestamp__date__gte=start_date_parsed)
        except ValueError:
            pass

    if end_date_str:
        try:
            end_date_parsed = datetime.strptime(end_date_str, "%Y-%m-%d").date()
            if end_time_str:
                end_time_parsed = datetime.strptime(end_time_str, "%H:%M").time()
                log_conditions &= Q(timestamp__lte=datetime.combine(end_date_parsed, end_time_parsed))
            else:
                log_conditions &= Q(timestamp__date__lte=end_date_parsed)
        except ValueError:
            pass

    # Merge search targets dynamically
    if has_property_filter:
        payload_q = Q(property_id__in=matched_property_ids)
        if bhk_type: payload_q |= Q(action_payload__icontains=bhk_type)
        if property_type: payload_q |= Q(action_payload__icontains=property_type)
        if location_query: payload_q |= Q(action_payload__icontains=location_query)
        log_conditions &= payload_q

    filtered_logs = logs.filter(log_conditions)

    # 3. Compile the Comprehensive Final Properties Presentation Array
    logs_property_ids = filtered_logs.exclude(property_id="Multiple / Sheet Records").values_list('property_id', flat=True).distinct()
    
    final_properties_queryset = RentalResidentialProperty.objects.filter(
        Q(rental_residential_id__in=logs_property_ids) | Q(rental_residential_id__in=matched_property_ids),
        is_deleted=False
    ).prefetch_related('images').distinct()

    # Calculate real-time totals for the Property Counter Badge
    properties_filtered_count = final_properties_queryset.count()
    properties_total_count = RentalResidentialProperty.objects.filter(is_deleted=False).count()

    # 4. Compute Metrics for the Top KPI Cards Block
    total_logs_count = filtered_logs.count()
    update_logs_count = filtered_logs.filter(action_type__iexact='UPDATE').count()
    delete_logs_count = filtered_logs.filter(action_type__iexact='DELETE').count()
    import_logs_count = filtered_logs.filter(action_type__iexact='EXCEL_IMPORT').count()

    # 5. LIVE EXPORT LOGIC FOR CSV AND EXCEL TRANSFERS
    download_format = request.GET.get('download', '').strip()
    if download_format in ['csv', 'excel']:
        filename_stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        if download_format == 'csv':
            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = f'attachment; filename="filtered_activity_logs_{filename_stamp}.csv"'
            writer = csv.writer(response)
            writer.writerow(['Sr.No', 'Timestamp', 'Property ID', 'Operator Identity', 'User System Role', 'Action', 'Changed Fields', 'Associated Excel File', 'Client IP Address', 'Execution Status'])
            for idx, item in enumerate(filtered_logs, 1):
                writer.writerow([idx, item.timestamp.strftime("%Y-%m-%d %H:%M"), item.property_id, item.user_identity, item.user_role, item.action_type, item.targeted_fields, item.associated_file, item.ip_address, item.status])
            return response
            
        elif download_format == 'excel':
            response = HttpResponse(content_type='application/ms-excel')
            response['Content-Disposition'] = f'attachment; filename="filtered_properties_matrix_{filename_stamp}.xls"'
            writer = csv.writer(response, delimiter='\t')
            writer.writerow(['Property ID', 'Property Title', 'Property Type', 'BHK Config Type', 'Monthly Rent', 'Security Deposit', 'City', 'Locality', 'Uploaded By', 'Source File Name'])
            for item in final_properties_queryset:
                writer.writerow([item.rental_residential_id, item.property_title, item.property_type, item.bhk_type, item.monthly_rent, item.security_deposit, item.city, item.locality, item.uploaded_by_name, item.upload_file_name])
            return response

    # 6. Pagination System Engine Layout Slices
    log_paginator = Paginator(filtered_logs, 15)
    log_records_list = log_paginator.get_page(request.GET.get('log_page', 1))

    prop_paginator = Paginator(final_properties_queryset, 10)
    page_obj = prop_paginator.get_page(request.GET.get('prop_page', 1))

    context = {
        'log_records_list': log_records_list,
        'page_obj': page_obj,
        'properties_filtered_count': properties_filtered_count,
        'properties_total_count': properties_total_count,
        'total_logs_count': total_logs_count,
        'update_logs_count': update_logs_count,
        'delete_logs_count': delete_logs_count,
        'import_logs_count': import_logs_count,
    }
    return render(request, "admin_user/Reports/Rental/rental_residential_activity_logs.html", context)





def _get_client_ip(request):
    """Helper to safely fetch client IP address reference."""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        return x_forwarded_for.split(',')[0].strip()
    return request.META.get('REMOTE_ADDR', '127.0.0.1')


def _get_deleter_name(request):
    """Helper function to get the name of the person deleting the property."""
    admin_id = request.session.get('Admin_id')
    user_id = request.session.get('User_id')

    if admin_id:
        try:
            admin = Admin_Login.objects.get(id=admin_id)
            return f"{admin.name} (Admin)"
        except Admin_Login.DoesNotExist:
            return "Unknown Admin"
            
    elif user_id:
        try:
            user = User_Details.objects.get(id=user_id)
            return f"{user.user_name} (User)"
        except User_Details.DoesNotExist:
            return "Unknown User"
            
    return "System"




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

            # ---------- AMENITIES & FACILITIES ----------
            amenities = ",".join(request.POST.getlist('amenities[]'))
            facilities = ",".join(request.POST.getlist('facilities[]'))

            # ---------- UPLOADER IDENTIFICATION ----------
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
            else:
                uploader_name, uploader_email, uploader_contact, uploader_role = "", "", "", ""

            # ---------- CREATE DATABASE OBJECT ----------
            prop = RentalResidentialProperty.objects.create(
                # BASIC INFORMATION
                property_title=request.POST.get('property_title'),
                # property_purpose is commented out in your model, so it is omitted here to prevent a crash
                property_type=request.POST.get('property_type'),
                bhk_type=request.POST.get('bhk_type'),
                renting_option=request.POST.get('renting_option'),
                built_up_area=to_decimal(request.POST.get('built_up_area')),
                bathrooms=to_int(request.POST.get('bathrooms')),
                balconies=to_int(request.POST.get('balconies')),
                floor_number=request.POST.get('floor_number'),
                total_floors=to_int(request.POST.get('total_floors')),
                facing=request.POST.get('facing'),
                furnishing_status=request.POST.get('furnishing_status'),
                available_for=request.POST.get('available_for'),

                # PROPERTY DETAILS
                zone=request.POST.get('zone'),
                ownership_type=request.POST.get('ownership_type'),
                construction_status=request.POST.get('construction_status'),
                property_age=request.POST.get('property_age'),
                carpet_area=to_decimal(request.POST.get('carpet_area')),
                plot_area=to_decimal(request.POST.get('plot_area')),
                building_name=request.POST.get('building_name'),

                # AVAILABILITY DETAILS
                possession_status=request.POST.get('possession_status'),
                available_from=available_from,
                lease_duration=request.POST.get('lease_duration'),
                brokerage=request.POST.get('brokerage'),
                brokerage_percentage=request.POST.get('brokerage_percentage'),
                manual_brokerage=request.POST.get('manual_brokerage'),

                # PRICING DETAILS
                monthly_rent=to_int(request.POST.get('monthly_rent')),
                security_deposit=to_int(request.POST.get('security_deposit')),
                maintenance_type=request.POST.get('maintenance_type'),
                maintenance_amount=to_int(request.POST.get('maintenance_amount')),

                # LOCATION DETAILS
                address=request.POST.get('address'),
                city=request.POST.get('city'),
                locality=request.POST.get('locality'),
                state=request.POST.get('state'),
                pincode=request.POST.get('pincode'),
                road_connectivity=request.POST.get('road_connectivity'),

                # AMENITIES & FACILITIES
                amenities=amenities,
                facilities=facilities,

                # DESCRIPTION
                description=request.POST.get('description'),
                rent_residential_desc=request.POST.get('rent_residential_desc'),

                # OWNER DETAILS
                owner_name=request.POST.get('owner_name'),
                contact_number=request.POST.get('contact_number'),
                email=request.POST.get('email'),
                alternate_contact=request.POST.get('alternate_contact'),

                # UPLOADED BY SYSTEM META-DATA
                uploaded_by_name=uploader_name,
                uploaded_by_email=uploader_email,
                uploaded_by_contact=uploader_contact,
                uploaded_by_role=uploader_role,
                upload_file_name=None # Explicitly handled for online UI submissions
            )

            # ---------- IMAGES MULTI-UPLOAD LOGIC ----------
            images = request.FILES.getlist('property_images[]')
            for img in images[:10]:
                RentalResidentialImage.objects.create(
                    property=prop, 
                    image=img
                )

            messages.success(request, "Property Added Successfully ✅")
            return redirect('residential_list')

        except Exception as e:
            print("ERROR DETECTED:", str(e))
            messages.error(request, f"Error while saving listing: {str(e)}")
            return redirect('rental_residential_add')


        print("Property Saved Successfully")
        print("description")
       

    # ---------- GET METHOD RENDER ----------
    return render(request, 'admin_user/Reports/Rental/rental_list.html', {
        'admin_obj': admin_obj,
        'user_obj': user_obj,
        'ameneties_obj': Ameneties_Details.objects.all(),
        'facilities_obj': Facilities_Details.objects.all()
    })








from django.utils.dateparse import parse_date


def rental_list(request):

    session_id = request.session.get('Admin_id')

    if not session_id:
        return render(request, 'home_page/Adminlogin.html')

    admin_obj = Admin_Login.objects.get(id=session_id)

    # ═══════════════════════════════════════
    # SEARCH FILTERS
    # ═══════════════════════════════════════

    search_query = request.GET.get('search', '').strip()
    bhk_query = request.GET.get('bhk_type', '').strip()
    city_query = request.GET.get('city', '').strip()
    furnish_query = request.GET.get('furnishing', '').strip()
    possession_query = request.GET.get('possession', '').strip()

    from_date_str = request.GET.get('from_date', '').strip()
    to_date_str = request.GET.get('to_date', '').strip()

    # ═══════════════════════════════════════
    # BASE QUERYSET
    # ═══════════════════════════════════════

    properties = RentalResidentialProperty.objects.filter(
        is_deleted=False
    ).order_by('-rental_residential_id')

    # ═══════════════════════════════════════
    # SEARCH FILTER
    # ═══════════════════════════════════════

    if search_query:
        properties = properties.filter(
            Q(property_title__icontains=search_query) |
            Q(property_type__icontains=search_query) |
            Q(bhk_type__icontains=search_query) |
            Q(city__icontains=search_query) |
            Q(locality__icontains=search_query) |
            Q(owner_name__icontains=search_query) |
            Q(possession_status__icontains=search_query)
        )

    # ═══════════════════════════════════════
    # ADVANCED FILTERS
    # ═══════════════════════════════════════

    if bhk_query and bhk_query != 'All BHK':
        properties = properties.filter(
            bhk_type__iexact=bhk_query
        )

    if city_query and city_query != 'All Cities':
        properties = properties.filter(
            city__iexact=city_query
        )

    if furnish_query and furnish_query != 'All':
        properties = properties.filter(
            furnishing_status__iexact=furnish_query
        )

    if possession_query and possession_query != 'All Status':
        properties = properties.filter(
            possession_status__iexact=possession_query
        )


    if from_date_str:
        from_date = parse_date(from_date_str)
        if from_date:
            properties = properties.filter(created_at__date__gte=from_date)

    if to_date_str:
        to_date = parse_date(to_date_str)
        if to_date:
            properties = properties.filter(created_at__date__lte=to_date)
    

    # ═══════════════════════════════════════
    # FLAT EXPORT HEADERS
    # ═══════════════════════════════════════
    # ═══════════════════════════════════════
    # EXPORT DOWNLOAD (TEMPLATE STYLE WITH ID & TRACKING)
    # ═══════════════════════════════════════
    if request.GET.get('download') in ['excel', 'csv']:
        import openpyxl
        from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
        from openpyxl.utils import get_column_letter
        from collections import OrderedDict
        import csv

        # ALL fields including ID and Uploader tracking
        sections = {
            "Basic Info": [
                "rental_residential_id", "property_title", "property_type", "bhk_type", 
                "renting_option", "built_up_area", "bathrooms", "balconies", 
                "floor_number", "total_floors", "facing", "furnishing_status", "available_for"
            ],
            "Property Details": [
                "zone", "ownership_type", "construction_status", "property_age", 
                "carpet_area", "plot_area", "building_name"
            ],
            "Availability": [
                "possession_status", "available_from", "lease_duration", 
                "brokerage", "brokerage_percentage", "manual_brokerage"
            ],
            "Pricing": [
                "monthly_rent", "security_deposit", "maintenance_type", "maintenance_amount"
            ],
            "Location": [
                "address", "city", "locality", "state", "pincode", "road_connectivity"
            ],
            "Description & Features": [
                "amenities", "facilities", "description", "rent_residential_desc"
            ],
            "Owner Info": [
                "owner_name", "contact_number", "email", "alternate_contact"
            ],
            "System Data": [
                 "uploaded_by_name", "uploaded_by_email", 
                "uploaded_by_contact", "uploaded_by_role", "upload_file_name", "created_at"
            ],
        }

        HINTS = {
            "rental_residential_id": "Auto-Generated ID",
            "property_title": "Auto_Generated Title", "property_type": "Apartment",
            "bhk_type": "1 BHK/2 BHK", "renting_option": "Full Property", "built_up_area": "sq.ft",
            "bathrooms": "Number", "balconies": "Number", "floor_number": "e.g. 5th Floor",
            "total_floors": "Number", "facing": "North/East", "furnishing_status": "Semi Furnished",
            "available_for": "Family/Bachelor", "zone": "North/South", "ownership_type": "Freehold",
            "construction_status": "Resale", "property_age": "1-3 Years", "carpet_area": "sq.ft",
            "plot_area": "sq.ft", "building_name": "Text", "possession_status": "Ready to Move",
            "available_from": "YYYY-MM-DD", "lease_duration": "11 Months", "brokerage": "Yes/No",
            "brokerage_percentage": "1%/Manual", "manual_brokerage": "e.g. 2.5%", "monthly_rent": "₹",
            "security_deposit": "₹", "maintenance_type": "Included in Rent/Extra", "maintenance_amount": "₹",
            "address": "Full Address", "city": "Text", "locality": "Text", "state": "e.g. Maharashtra",
            "pincode": "6-digit", "road_connectivity": "Optional", "amenities": "Comma-sep", 
            "facilities": "Comma-sep", "description": "Short Summary", "rent_residential_desc": "Long Rich Text",
            "owner_name": "Full Name", "contact_number": "10 Digits", "email": "email@example.com",
            "alternate_contact": "Optional", "uploaded_by_name": "Admin Name", "uploaded_by_email": "Admin Email",
            "uploaded_by_contact": "Admin Contact", "uploaded_by_role": "Admin Role", "upload_file_name": "File Name", "created_at": "YYYY-MM-DD"
        }

        REQUIRED = {
            "property_type", "bhk_type", "renting_option", 
            "built_up_area", "bathrooms", "floor_number", "furnishing_status", 
            "available_for", "monthly_rent", "security_deposit", "address", 
            "city", "locality", "state", "pincode", "owner_name", "contact_number", "email"
        }

        all_cols = []
        for sec, fields in sections.items():
            all_cols.extend([(sec, f) for f in fields])

        # ------------- EXCEL GENERATION -------------
        if request.GET.get('download') == 'excel':
            wb = openpyxl.Workbook()
            ws = wb.active
            ws.title = "Rental Residential"

            HDR_BG, REQ_BG, OPT_BG = "667EEA", "FEF3C7", "F0FDF4"
            thin = Side(style="thin", color="CBD5E1")
            bdr = Border(left=thin, right=thin, top=thin, bottom=thin)

            sec_spans = OrderedDict()
            for i, (sec, _) in enumerate(all_cols):
                sec_spans.setdefault(sec, []).append(i + 1)

            # Row 1: Banners
            for sec, cols in sec_spans.items():
                c = ws.cell(row=1, column=cols[0], value=f"📋 {sec}")
                c.font = Font(bold=True, color="FFFFFF", name="Arial", size=11)
                c.fill = PatternFill("solid", fgColor=HDR_BG)
                c.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
                c.border = bdr
                if len(cols) > 1:
                    ws.merge_cells(start_row=1, start_column=cols[0], end_row=1, end_column=cols[-1])

            # Row 2 & 3: Fields and Hints
            for ci, (sec, field) in enumerate(all_cols, 1):
                req = field in REQUIRED
                lc = ws.cell(row=2, column=ci, value=field + (" *" if req else ""))
                lc.font = Font(bold=True, color="1E293B", name="Arial", size=9)
                lc.fill = PatternFill("solid", fgColor=REQ_BG if req else OPT_BG)
                lc.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
                lc.border = bdr

                hc = ws.cell(row=3, column=ci, value=HINTS.get(field, ""))
                hc.font = Font(italic=True, color="64748B", name="Arial", size=8)
                hc.fill = PatternFill("solid", fgColor="FFFFFF")
                hc.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
                hc.border = bdr

                ws.column_dimensions[get_column_letter(ci)].width = max(16, len(field) + 4)

            ws.row_dimensions[1].height = 28
            ws.row_dimensions[2].height = 36
            ws.row_dimensions[3].height = 42
            ws.freeze_panes = "A4"

            # Row 4+: Actual Database Data (Automatically fills ID and Uploader Info)
            for row_idx, p in enumerate(properties, start=4):
                for col_idx, (sec, field) in enumerate(all_cols, 1):
                    val = getattr(p, field, "")
                    if field in ['available_from', 'created_at'] and val:
                        val = val.strftime('%Y-%m-%d')
                    
                    c = ws.cell(row=row_idx, column=col_idx, value=val)
                    c.alignment = Alignment(horizontal="center", vertical="center")
                    c.border = bdr

            response = HttpResponse(content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
            response["Content-Disposition"] = 'attachment; filename="Rental_Properties_Data.xlsx"'
            wb.save(response)
            return response

        # ------------- CSV GENERATION -------------
        elif request.GET.get('download') == 'csv':
            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename="Rental_Properties_Data.csv"'
            writer = csv.writer(response)

            # Build Row 1 (Banners) for CSV
            row1 = []
            current_sec = ""
            for sec, _ in all_cols:
                if sec != current_sec:
                    row1.append(f"📋 {sec}")
                    current_sec = sec
                else:
                    row1.append("") # Empty cell to simulate merge in CSV
            writer.writerow(row1)

            # Row 2 & 3 (Fields and Hints)
            writer.writerow([field + (" *" if field in REQUIRED else "") for _, field in all_cols])
            writer.writerow([HINTS.get(field, "") for _, field in all_cols])

            # Row 4+: Actual Database Data (Automatically fills ID and Uploader Info)
            for p in properties:
                data_row = []
                for _, field in all_cols:
                    val = getattr(p, field, "")
                    if field in ['available_from', 'created_at'] and val:
                        val = val.strftime('%Y-%m-%d')
                    data_row.append(val)
                writer.writerow(data_row)
                
            return response
    # ═══════════════════════════════════════
    # PAGINATION
    # ═══════════════════════════════════════

    paginator = Paginator(properties, 10)

    page_number = request.GET.get('page')

    page_obj = paginator.get_page(page_number)

    filtered_count = properties.count()

    # ═══════════════════════════════════════
    # STATS
    # ═══════════════════════════════════════

    all_props = RentalResidentialProperty.objects.filter(
        is_deleted=False
    )

    total_count = all_props.count()

    unique_bhk = all_props.exclude(
        bhk_type__isnull=True
    ).exclude(
        bhk_type=''
    ).values_list(
        'bhk_type',
        flat=True
    ).distinct()

    unique_cities = all_props.exclude(
        city__isnull=True
    ).exclude(
        city=''
    ).values_list(
        'city',
        flat=True
    ).distinct()

    unique_furnish = all_props.exclude(
        furnishing_status__isnull=True
    ).exclude(
        furnishing_status=''
    ).values_list(
        'furnishing_status',
        flat=True
    ).distinct()

    unique_possession = all_props.exclude(
        possession_status__isnull=True
    ).exclude(
        possession_status=''
    ).values_list(
        'possession_status',
        flat=True
    ).distinct()

    active_count = all_props.exclude(
        possession_status__isnull=True
    ).exclude(
        possession_status=''
    ).count()

    furnished_count = all_props.filter(
        furnishing_status__iexact='Furnished'
    ).count()

    available_count = all_props.filter(
        possession_status__iexact='Ready to Move'
    ).count()

    city_count = all_props.exclude(
        city__isnull=True
    ).exclude(
        city=''
    ).values(
        'city'
    ).distinct().count()

    # ═══════════════════════════════════════
    # RENT STATS
    # ═══════════════════════════════════════

    rent_stats = all_props.exclude(
        monthly_rent__isnull=True
    ).aggregate(
        avg_rent=Avg('monthly_rent'),
        max_rent=Max('monthly_rent'),
        min_rent=Min('monthly_rent'),
    )

    avg_rent = rent_stats['avg_rent']
    max_rent = rent_stats['max_rent']
    min_rent = rent_stats['min_rent']

    deposit_stats = all_props.exclude(
        security_deposit__isnull=True
    ).aggregate(
        avg_deposit=Avg('security_deposit')
    )

    avg_deposit = deposit_stats['avg_deposit']

    area_stats = all_props.exclude(
        built_up_area__isnull=True
    ).aggregate(
        avg_area=Avg('built_up_area')
    )

    avg_area = area_stats['avg_area']

    with_owner_count = all_props.exclude(
        owner_name__isnull=True
    ).exclude(
        owner_name=''
    ).count()

    with_images_count = all_props.filter(
        images__isnull=False
    ).distinct().count()

    uploaded_files = all_props.exclude(
        upload_file_name__isnull=True
    ).exclude(
        upload_file_name=''
    ).values_list(
        'upload_file_name',
        flat=True
    ).distinct()

    # ═══════════════════════════════════════
    # CHARTS
    # ═══════════════════════════════════════

    bhk_qs = all_props.exclude(
        bhk_type__isnull=True
    ).exclude(
        bhk_type=''
    ).values(
        'bhk_type'
    ).annotate(
        count=Count('rental_residential_id')
    ).order_by('-count')

    bhk_labels = json.dumps([
        item['bhk_type'] for item in bhk_qs
    ])

    bhk_data = json.dumps([
        item['count'] for item in bhk_qs
    ])

    rent_buckets = [
        ('Under ₹5k', 0, 5000),
        ('₹5k–10k', 5000, 10000),
        ('₹10k–20k', 10000, 20000),
        ('₹20k–30k', 20000, 30000),
        ('₹30k–50k', 30000, 50000),
        ('₹50k–1L', 50000, 100000),
        ('Above ₹1L', 100000, 999999999),
    ]

    rent_range_labels = json.dumps([
        b[0] for b in rent_buckets
    ])

    rent_range_data = json.dumps([
        all_props.filter(
            monthly_rent__gte=lo,
            monthly_rent__lt=hi
        ).count()
        for _, lo, hi in rent_buckets
    ])

    furnish_qs = all_props.exclude(
        furnishing_status__isnull=True
    ).exclude(
        furnishing_status=''
    ).values(
        'furnishing_status'
    ).annotate(
        count=Count('rental_residential_id')
    ).order_by('-count')

    furnishing_labels = json.dumps([
        item['furnishing_status'] for item in furnish_qs
    ])

    furnishing_data = json.dumps([
        item['count'] for item in furnish_qs
    ])

    prop_type_qs = all_props.exclude(
        property_type__isnull=True
    ).exclude(
        property_type=''
    ).values(
        'property_type'
    ).annotate(
        count=Count('rental_residential_id')
    ).order_by('-count')

    prop_type_labels = json.dumps([
        item['property_type'] for item in prop_type_qs
    ])

    prop_type_data = json.dumps([
        item['count'] for item in prop_type_qs
    ])

    # ═══════════════════════════════════════
    # KPI
    # ═══════════════════════════════════════

    occupied_count = all_props.filter(
        possession_status__iexact='Occupied'
    ).count()

    vacant_count = all_props.filter(
        possession_status__iexact='Ready to Move'
    ).count()

    occupancy_rate = round(
        (occupied_count / total_count * 100), 1
    ) if total_count > 0 else 0

    vacancy_rate = round(
        (vacant_count / total_count * 100), 1
    ) if total_count > 0 else 0

    total_revenue = all_props.aggregate(
        total=Sum('monthly_rent')
    )['total'] or 0

    total_security_deposit = all_props.aggregate(
        total=Sum('security_deposit')
    )['total'] or 0

    ready_to_move_count = all_props.filter(
        possession_status__iexact='Ready to Move'
    ).count()

    short_lease_count = all_props.filter(
        lease_duration__icontains='6'
    ).count()

    long_lease_count = all_props.filter(
        lease_duration__icontains='12'
    ).count()

    new_property_count = all_props.filter(
        property_age__icontains='New'
    ).count()

    old_property_count = all_props.exclude(
        property_age__icontains='New'
    ).count()

    premium_properties_count = all_props.filter(
        monthly_rent__gte=50000
    ).count()

    affordable_properties_count = all_props.filter(
        monthly_rent__lt=15000
    ).count()

    # ═══════════════════════════════════════
    # CONTEXT
    # ═══════════════════════════════════════

    context = {

        'admin_obj': admin_obj,
        'page_obj': page_obj,

        'search_query': search_query,
        'bhk_query': bhk_query,
        'city_query': city_query,
        'furnish_query': furnish_query,
        'possession_query': possession_query,

        'unique_bhk': unique_bhk,
        'unique_cities': unique_cities,
        'unique_furnish': unique_furnish,
        'unique_possession': unique_possession,

        'filtered_count': filtered_count,

        'total_count': total_count,
        'active_count': active_count,
        'furnished_count': furnished_count,
        'available_count': available_count,
        'city_count': city_count,

        'from_date': from_date_str,
        'to_date': to_date_str,

        'avg_rent': avg_rent,
        'max_rent': max_rent,
        'min_rent': min_rent,

        'avg_deposit': avg_deposit,
        'avg_area': avg_area,

        'with_owner_count': with_owner_count,
        'with_images_count': with_images_count,

        'uploaded_files': uploaded_files,

        'bhk_labels': bhk_labels,
        'bhk_data': bhk_data,

        'rent_range_labels': rent_range_labels,
        'rent_range_data': rent_range_data,

        'furnishing_labels': furnishing_labels,
        'furnishing_data': furnishing_data,

        'prop_type_labels': prop_type_labels,
        'prop_type_data': prop_type_data,

        'occupied_count': occupied_count,
        'vacant_count': vacant_count,

        'occupancy_rate': occupancy_rate,
        'vacancy_rate': vacancy_rate,

        'total_revenue': total_revenue,
        'total_security_deposit': total_security_deposit,

        'ready_to_move_count': ready_to_move_count,
        'short_lease_count': short_lease_count,
        'long_lease_count': long_lease_count,

        'new_property_count': new_property_count,
        'old_property_count': old_property_count,

        'premium_properties_count': premium_properties_count,
        'affordable_properties_count': affordable_properties_count,
    }

    return render(
        request,
        'admin_user/Reports/Rental/rental_list.html',
        context
    )




def rental_bulk_delete(request):
    """Handles Advanced Bulk Deletions for Rental Properties (Soft Delete)."""
    if request.method != 'POST':
        return JsonResponse({'status': 'error', 'message': 'Invalid request method.'})
        
    admin_id = request.session.get('Admin_id')
    user_id = request.session.get('User_id')
    
    if not admin_id and not user_id:
        return JsonResponse({'status': 'error', 'message': 'Unauthorized access.'})

    try:
        data = json.loads(request.body)
        delete_type = data.get('delete_type')
        
        # 👈 1. Get the deleter's name
        deleter_name = _get_deleter_name(request)
        
        # IMPORTANT: Only target properties that are NOT currently in the Recycle Bin
        properties = RentalResidentialProperty.objects.filter(is_deleted=False)
        
        if delete_type == 'delete_all':
            count = properties.count()
            # 👈 2. Add deleted_by=deleter_name to the update query
            properties.update(is_deleted=True, deleted_at=timezone.now(), deleted_by=deleter_name)
            return JsonResponse({'status': 'success', 'message': f'Successfully moved ALL {count} properties to Recycle Bin.'})
            
        elif delete_type == 'current_page':
            page_ids = data.get('page_ids', [])
            target_props = properties.filter(rental_residential_id__in=page_ids)
            count = target_props.count()
            target_props.update(is_deleted=True, deleted_at=timezone.now(), deleted_by=deleter_name)
            return JsonResponse({'status': 'success', 'message': f'Successfully moved {count} properties from current page to Recycle Bin.'})
            
        elif delete_type == 'date_range':
            from_date = data.get('from_date')
            to_date = data.get('to_date')
            target_props = properties.filter(available_from__range=[from_date, to_date])
            count = target_props.count()
            target_props.update(is_deleted=True, deleted_at=timezone.now(), deleted_by=deleter_name)
            return JsonResponse({'status': 'success', 'message': f'Successfully moved {count} properties in date range to Recycle Bin.'})
            
        elif delete_type == 'latest_month':
            thirty_days_ago = timezone.now() - timedelta(days=30)
            target_props = properties.filter(available_from__gte=thirty_days_ago)
            count = target_props.count()
            target_props.update(is_deleted=True, deleted_at=timezone.now(), deleted_by=deleter_name)
            return JsonResponse({'status': 'success', 'message': f'Successfully moved {count} properties from the last 30 days to Recycle Bin.'})
            
        elif delete_type == 'old_data':
            six_months_ago = timezone.now() - timedelta(days=180)
            target_props = properties.filter(available_from__lt=six_months_ago)
            count = target_props.count()
            target_props.update(is_deleted=True, deleted_at=timezone.now(), deleted_by=deleter_name)
            return JsonResponse({'status': 'success', 'message': f'Successfully moved {count} older properties to Recycle Bin.'})
            
        elif delete_type == 'by_uploader':
            uploader = data.get('uploader_text', '')
            target_props = properties.filter(
                Q(uploaded_by_name__icontains=uploader) | 
                Q(uploaded_by_email__icontains=uploader) |
                Q(uploaded_by_role__icontains=uploader)
            )
            count = target_props.count()
            target_props.update(is_deleted=True, deleted_at=timezone.now(), deleted_by=deleter_name)
            return JsonResponse({'status': 'success', 'message': f'Successfully moved {count} properties uploaded by {uploader} to Recycle Bin.'})

        elif delete_type == 'by_file':
            file_name = data.get('file_name', '')
            target_props = properties.filter(upload_file_name=file_name) 
            count = target_props.count()
            if count == 0:
                return JsonResponse({'status': 'error', 'message': f'No properties found for file: {file_name}'})
            target_props.update(is_deleted=True, deleted_at=timezone.now(), deleted_by=deleter_name)
            return JsonResponse({'status': 'success', 'message': f'Successfully moved {count} properties from {file_name} to Recycle Bin.'})
            
        else:
            return JsonResponse({'status': 'error', 'message': 'Unknown delete criteria.'})

    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)})





@require_POST
def rental_residential_delete(request, pk):
    """Soft delete a single property."""
    try:
        session_id = request.session.get('Admin_id')
        user_identity = "Unknown Admin"
        if session_id:
            try:
                admin_obj = Admin_Login.objects.get(id=session_id)
                user_identity = admin_obj.email or admin_obj.username
            except Admin_Login.DoesNotExist:
                pass

        prop = RentalResidentialProperty.objects.get(rental_residential_id=pk)

        # Snapshot file source metadata before deletion mapping executions
        associated_origin_file = prop.upload_file_name or "Web UI Form"
        property_title_ref = prop.property_title or "—"

        prop.is_deleted = True
        prop.deleted_at = timezone.now()
        if hasattr(prop, 'deleted_by'):
            prop.deleted_by = user_identity

        prop.save()

        # =====================================================
        # AUDIT LOGIC: Operational Deletion Trace Serialization
        # =====================================================
        RentalActivityLog.objects.create(
            user_identity=user_identity,
            user_role="Admin",
            action_type='DELETE',
            property_id=pk,
            targeted_fields="Entire Record Purged",
            associated_file=associated_origin_file,
            action_payload=json.dumps({
                "deleted_property_id": pk,
                "property_title": property_title_ref,
                "action": "soft_delete_to_recycle_bin"
            }),
            ip_address=_get_client_ip(request),
            status='SUCCESS'
        )

        return JsonResponse({
            'status': 'success',
            'message': 'Moved to Recycle Bin successfully!'
        })

    except RentalResidentialProperty.DoesNotExist:
        return JsonResponse({
            'status': 'error',
            'message': 'Property not found.'
        })
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        })



def system_audit_logs(request):
    """A completely separate view for tracking Deletion and Restore Audit Logs."""
    session_id = request.session.get('Admin_id')
    if not session_id:
        return render(request, 'home_page/Adminlogin.html')

    admin_obj = Admin_Login.objects.get(id=session_id)

    deletion_logs = []
    restore_logs = []

    # Map all your 8 models
    models_map = {
        'Rental Residential': RentalResidentialProperty,
        'Commercial Rental': CommercialRentalProperty,
        'PG / Co-living': PGColivingProperty,
        'Resale Residential': ResaleResidentialProperty,
        'Commercial Resale': CommercialResaleProperty,
        'Plot/Land': PlotSaleProperty,
        'Industrial Resale': IndustrialResaleProperty,
        'Agricultural Resale': AgriculturalResaleProperty,
    }

    for module_name, model in models_map.items():
        # 1. Fetch Deletion Logs
        try:
            deleted_items = model.objects.filter(is_deleted=True).exclude(deleted_at__isnull=True)
            for p in deleted_items:
                # Dynamically find the title/name field since different models use different names
                title = getattr(p, 'property_title', getattr(p, 'building_name', getattr(p, 'pg_name', getattr(p, 'title', getattr(p, 'plot_title', getattr(p, 'property_type', 'N/A'))))))
                
                deletion_logs.append({
                    'module': module_name,
                    'id': p.id,
                    'title': title,
                    'by': getattr(p, 'deleted_by', 'System Admin'),
                    'date': p.deleted_at
                })
        except Exception:
            pass

        # 2. Fetch Restore Logs
        try:
            # Assumes you added restored_at and restored_by to your models!
            restored_items = model.objects.filter(restored_at__isnull=False)
            for p in restored_items:
                title = getattr(p, 'property_title', getattr(p, 'building_name', getattr(p, 'pg_name', getattr(p, 'title', getattr(p, 'plot_title', getattr(p, 'property_type', 'N/A'))))))
                
                restore_logs.append({
                    'module': module_name,
                    'id': p.id,
                    'title': title,
                    'by': getattr(p, 'restored_by', 'System Admin'),
                    'date': p.restored_at
                })
        except Exception:
            pass

    # Sort both lists by date (Newest logs first)
    deletion_logs.sort(key=lambda x: x['date'] if x['date'] else timezone.now(), reverse=True)
    restore_logs.sort(key=lambda x: x['date'] if x['date'] else timezone.now(), reverse=True)

    context = {
        'admin_obj':admin_obj,
        'deletion_logs': deletion_logs,
        'restore_logs': restore_logs,
        'deletion_count': len(deletion_logs),
        'restore_count': len(restore_logs),
        'total_logs': len(deletion_logs) + len(restore_logs)
    }

    return render(request, 'admin_user/Reports/Rental/audit_logs.html', context)





def global_recycle_bin(request):
    """Unified Recycle Bin displaying deleted items from all property modules."""

    session_id = request.session.get('Admin_id')
    if not session_id:
        return render(request, 'home_page/Adminlogin.html')

<<<<<<< HEAD
=======
    admin_obj = Admin_Login.objects.get(id=session_id)

    # Helper function to calculate auto-delete countdown (30 days)
>>>>>>> d0f149b2c74d1fc5cd4a07f46e5105a392471ff5
    def calculate_retention(queryset):
        now = timezone.now()

        items = list(queryset)

        for item in items:
            if item.deleted_at:
                expiry_date = item.deleted_at + timedelta(days=30)
                item.days_left = max((expiry_date - now).days, 0)
            else:
                item.days_left = 30

        return items

    rental_deleted = calculate_retention(
        RentalResidentialProperty.objects.filter(
            is_deleted=True
        ).order_by('-deleted_at')
    )

    commercial_deleted = calculate_retention(
        CommercialRentalProperty.objects.filter(
            is_deleted=True
        ).order_by('-deleted_at')
    )

    pg_deleted = calculate_retention(
        PGColivingProperty.objects.filter(
            is_deleted=True
        ).order_by('-deleted_at')
    )

    resale_deleted = calculate_retention(
        ResaleResidentialProperty.objects.filter(
            is_deleted=True
        ).order_by('-deleted_at')
    )

    commercial_resale_deleted = calculate_retention(
        CommercialResaleProperty.objects.filter(
            is_deleted=True
        ).order_by('-deleted_at')
    )

    plot_sale_deleted = calculate_retention(
        PlotSaleProperty.objects.filter(
            is_deleted=True
        ).order_by('-deleted_at')
    )

    industrial_resale_deleted = calculate_retention(
        IndustrialResaleProperty.objects.filter(
            is_deleted=True
        ).order_by('-deleted_at')
    )

    agricultural_resale_deleted = calculate_retention(
        AgriculturalResaleProperty.objects.filter(
            is_deleted=True
        ).order_by('-deleted_at')
    )

    context = {
<<<<<<< HEAD
        'rental_deleted': rental_deleted,
        'rental_count': len(rental_deleted),

        'commercial_deleted': commercial_deleted,
        'commercial_count': len(commercial_deleted),

        'pg_deleted': pg_deleted,
        'pg_count': len(pg_deleted),

        'resale_deleted': resale_deleted,
        'resale_count': len(resale_deleted),

        'commercial_resale_deleted': commercial_resale_deleted,
        'commercial_resale_count': len(commercial_resale_deleted),

        'plot_sale_deleted': plot_sale_deleted,
        'plot_sale_count': len(plot_sale_deleted),

        'industrial_resale_deleted': industrial_resale_deleted,
        'industrial_resale_count': len(industrial_resale_deleted),

        'agricultural_resale_deleted': agricultural_resale_deleted,
        'agricultural_resale_count': len(agricultural_resale_deleted),

=======
        'admin_obj':admin_obj,
        'rental_deleted': rental_deleted, 'rental_count': len(rental_deleted),
        'commercial_deleted': commercial_deleted, 'commercial_count': len(commercial_deleted),
        'pg_deleted': pg_deleted, 'pg_count': len(pg_deleted),
        'resale_deleted': resale_deleted, 'resale_count': len(resale_deleted),
        'commercial_resale_deleted': commercial_resale_deleted, 'commercial_resale_count': len(commercial_resale_deleted),
        'plot_sale_deleted': plot_sale_deleted, 'plot_sale_count': len(plot_sale_deleted),
        'industrial_resale_deleted': industrial_resale_deleted, 'industrial_resale_count': len(industrial_resale_deleted),
        'agricultural_resale_deleted': agricultural_resale_deleted, 'agricultural_resale_count': len(agricultural_resale_deleted),
        
>>>>>>> d0f149b2c74d1fc5cd4a07f46e5105a392471ff5
        'total_deleted_all': (
            len(rental_deleted)
            + len(commercial_deleted)
            + len(pg_deleted)
            + len(resale_deleted)
            + len(commercial_resale_deleted)
            + len(plot_sale_deleted)
            + len(industrial_resale_deleted)
            + len(agricultural_resale_deleted)
        )
    }

    return render(
        request,
        'admin_user/Reports/Rental/global_recycle_bin.html',
        context
    )



@require_POST
def bulk_hard_delete_properties(request, property_type):
    """Permanently deletes all soft-deleted items for a specific property type."""
    session_id = request.session.get('Admin_id')
    if not session_id:
        return JsonResponse({'status': 'error', 'message': 'Unauthorized entry.'}, status=403)
    
    # Map property type slugs to corresponding models
    model_mapping = {
        'rental-residential': RentalResidentialProperty,
        'commercial': CommercialRentalProperty,
        'pg-coliving': PGColivingProperty,
        'resale-residential': ResaleResidentialProperty,
        'commercial-resale': CommercialResaleProperty,
        'plot-sale': PlotSaleProperty,
        'industrial-resale': IndustrialResaleProperty,
        'agricultural-resale': AgriculturalResaleProperty,
    }
    
    model = model_mapping.get(property_type)
    if not model:
        return JsonResponse({'status': 'error', 'message': 'Invalid property module type.'})
    
    try:
        # Perform permanent hard delete on all items marked as is_deleted=True
        deleted_count, _ = model.objects.filter(is_deleted=True).delete()
        return JsonResponse({
            'status': 'success',
            'message': f'Permanently wiped all {deleted_count} items from this bin context.'
        })
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)})




@require_POST
def rental_restore(request, pk):
    """Restore property from recycle bin."""

    try:
        prop = RentalResidentialProperty.objects.get(
            rental_residential_id=pk,
            is_deleted=True
        )

        prop.is_deleted = False
        prop.deleted_at = None

        if hasattr(prop, 'deleted_by'):
            prop.deleted_by = None

        prop.save()

        return JsonResponse({
            'status': 'success',
            'message': 'Property successfully restored!'
        })

    except RentalResidentialProperty.DoesNotExist:
        return JsonResponse({
            'status': 'error',
            'message': 'Property not found.'
        })

    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        })


@require_POST
def rental_hard_delete(request, pk):
    print("PK RECEIVED:", pk)

    try:
        prop = RentalResidentialProperty.objects.get(
            rental_residential_id=pk,
            is_deleted=True
        )

        print("FOUND PROPERTY:", prop.rental_residential_id)

        prop.delete()

        return JsonResponse({
            'status': 'success',
            'message': 'Property permanently deleted.'
        })

    except RentalResidentialProperty.DoesNotExist:
        print("PROPERTY NOT FOUND:", pk)

        return JsonResponse({
            'status': 'error',
            'message': 'Property not found.'
        })
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



def _load_new_excel(excel_file):
    """
    Returns (ws, headers_dict) where headers_dict maps clean_col_name → col_index (1-based).
    Caller iterates ws.iter_rows(min_row=4, values_only=True) for data.
    """
    wb = openpyxl.load_workbook(excel_file, read_only=True, data_only=True)
    ws = wb.active
 
    headers = {}
    header_row = list(ws.iter_rows(min_row=2, max_row=2, values_only=True))[0]
    for col_idx, cell_val in enumerate(header_row, 1):
        if cell_val:
            key = str(cell_val).strip().rstrip(' *').strip().lower()
            headers[key] = col_idx
    return wb, ws, headers
 
 
def _get_cell(row, col_idx):
    """Safe cell fetch from a values_only row tuple."""
    if col_idx and col_idx - 1 < len(row):
        return row[col_idx - 1]
    return None
 
 
# =============================================================================
# 1. RENTAL RESIDENTIAL
# =============================================================================
 
RENTAL_RES_COLUMN_MAP = [
    # ==========================================
    # BASIC INFO
    # ==========================================
    
   
    ("property_type",        "property_type",        _str),
    ("bhk_type",             "bhk_type",             _str),
    ("renting_option",       "renting_option",       _str),
    ("built_up_area",        "built_up_area",        _decimal),
    ("bathrooms",            "bathrooms",            _int),
    ("balconies",            "balconies",            _int),
    ("floor_number",         "floor_number",         _str),
    ("total_floors",         "total_floors",         _int),
    ("facing",               "facing",               _str),
    ("furnishing_status",    "furnishing_status",    _str),
    ("available_for",        "available_for",        _str),

    # ==========================================
    # PROPERTY DETAILS
    # ==========================================
    ("zone",                 "zone",                 _str),
    ("ownership_type",       "ownership_type",       _str),
    ("construction_status",  "construction_status",  _str),
    ("property_age",         "property_age",         _str),
    ("carpet_area",          "carpet_area",          _decimal),
    ("plot_area",            "plot_area",            _decimal),
    ("building_name",        "building_name",        _str),

    # ==========================================
    # AVAILABILITY DETAILS
    # ==========================================
    ("possession_status",    "possession_status",    _str),
    ("available_from",       "available_from",       _date),
    ("lease_duration",       "lease_duration",       _str),
    ("brokerage",            "brokerage",            _str),
    ("brokerage_percentage", "brokerage_percentage", _str),
    ("manual_brokerage",     "manual_brokerage",     _str),

    # ==========================================
    # PRICING DETAILS
    # ==========================================
    ("monthly_rent",         "monthly_rent",         _bigint),
    ("security_deposit",     "security_deposit",     _bigint),
    ("maintenance_type",     "maintenance_type",     _str),
    ("maintenance_amount",   "maintenance_amount",   _bigint),

    # ==========================================
    # LOCATION DETAILS
    # ==========================================
    ("address",              "address",              _str),
    ("city",                 "city",                 _str),
    ("locality",             "locality",             _str),
    ("state",                "state",                _str),
    ("pincode",              "pincode",              _str),
    ("road_connectivity",    "road_connectivity",    _str),

    # ==========================================
    # AMENITIES & DESCRIPTION
    # ==========================================
    ("amenities",            "amenities",            _str),
    ("facilities",           "facilities",           _str),
    ("description",          "description",          _str),
    ("rent_residential_desc","rent_residential_desc",_str),

    # ==========================================
    # OWNER DETAILS
    # ==========================================
    ("owner_name",           "owner_name",           _str),
    ("contact_number",       "contact_number",       _str),
    ("email",                "email",                _email),
    ("alternate_contact",    "alternate_contact",    _str),

    # ==========================================
    # SYSTEM / TRACKING (Optional for Excel Upload)
    # ==========================================
    ("uploaded_by_name",     "uploaded_by_name",     _str),
    ("uploaded_by_email",    "uploaded_by_email",    _str),
    ("uploaded_by_contact",  "uploaded_by_contact",  _str),
    ("uploaded_by_role",     "uploaded_by_role",     _str),
    ("created_at",           "created_at",           _date), 
]






from datetime import datetime
from decimal import Decimal, InvalidOperation






@csrf_exempt
@require_POST
def import_residential_excel(request):
    excel_file = request.FILES.get("rental_file")
    if not excel_file:
        return JsonResponse({"status": "error", "message": "No file uploaded."}, status=400)
    
    if not excel_file.name.endswith(".xlsx"):
        return JsonResponse({"status": "error", "message": "Only .xlsx files allowed."}, status=400)

    # Establish operator system identities tracking maps
    session_id = request.session.get('Admin_id')
    user_identity = "Automated Engine"
    if session_id:
        try:
            admin_obj = Admin_Login.objects.get(id=session_id)
            user_identity = admin_obj.email or admin_obj.username
        except Admin_Login.DoesNotExist:
            pass

    try:
        wb = openpyxl.load_workbook(excel_file, data_only=True)
        ws = wb.active
    except Exception as e:
        return JsonResponse({"status": "error", "message": f"Cannot open file: {e}"}, status=400)

    row1_vals = [str(cell.value or "").strip().replace(" *", "") for cell in ws[1]]
    row2_vals = [str(cell.value or "").strip().replace(" *", "") for cell in ws[2]] if ws.max_row >= 2 else []

    if "property_purpose" in row2_vals or "property_title" in row2_vals:
        headers = [val if val else None for val in row2_vals]
        data_start_row = 4
    else:
        headers = [val if val else None for val in row1_vals]
        data_start_row = 2

    parsed_rows = []
    for row_idx, row in enumerate(ws.iter_rows(min_row=data_start_row, values_only=True), start=data_start_row):
        if all(v is None or str(v).strip() == "" for v in row): continue  
        
        obj_data = {}
        row_id = None
        for col_idx, col_name in enumerate(headers):
            if col_name:
                val = row[col_idx]
                if col_name == 'rental_residential_id': row_id = str(val).strip() if val else None
                elif col_name not in ['created_at', 'deleted_at', 'is_deleted']:
                    if val is not None and str(val).strip() != "": obj_data[col_name] = val

        if 'available_from' in obj_data and obj_data['available_from']:
            d_val = obj_data['available_from']
            if isinstance(d_val, str):
                c_str = d_val.strip().split(" ")[0]
                try: obj_data['available_from'] = datetime.strptime(c_str, "%Y-%m-%d").date()
                except:
                    try: obj_data['available_from'] = datetime.strptime(c_str, "%d-%m-%Y").date()
                    except: obj_data['available_from'] = None
            elif isinstance(d_val, datetime):
                obj_data['available_from'] = d_val.date()

        for f in ['monthly_rent', 'security_deposit', 'maintenance_amount', 'bathrooms', 'balconies', 'total_floors']:
            if f in obj_data and obj_data[f] is not None:
                try: obj_data[f] = int(float(str(obj_data[f]).replace(",", "").strip()))
                except: obj_data[f] = None

        for f in ['built_up_area', 'carpet_area', 'plot_area']:
            if f in obj_data and obj_data[f] is not None:
                try: obj_data[f] = Decimal(str(obj_data[f]).replace(",", "").strip())
                except: obj_data[f] = None

        parsed_rows.append({'row_idx': row_idx, 'row_id': row_id, 'data': obj_data})

    wb.close()

    file_name_exists = RentalResidentialProperty.objects.filter(upload_file_name=excel_file.name).exists()
    total_scanned_rows = len(parsed_rows)
    different_file_rows = 0
    duplicate_data_different_name_count = 0

    for item in parsed_rows:
        o_data = item['data']
        r_id = item['row_id']

        dup_match = RentalResidentialProperty.objects.filter(
            property_title=o_data.get('property_title'),
            address=o_data.get('address'),
            owner_name=o_data.get('owner_name'),
            contact_number=o_data.get('contact_number')
        ).first()

        if dup_match and dup_match.upload_file_name != excel_file.name:
            duplicate_data_different_name_count += 1

        if r_id and r_id != "None":
            existing = RentalResidentialProperty.objects.filter(rental_residential_id=r_id).first()
            if existing:
                has_changed = False
                for k, v in o_data.items():
                    if str(getattr(existing, k, None)).strip() != str(v).strip():
                        has_changed = True
                        break
                if has_changed: different_file_rows += 1

    if file_name_exists and different_file_rows == 0 and total_scanned_rows > 0:
        return JsonResponse({
            "status": "duplicate_filename_and_data",
            "message": f"Upload Denied: A file named '{excel_file.name}' has already been processed with identical rows."
        })

    if not file_name_exists and duplicate_data_different_name_count == total_scanned_rows and total_scanned_rows > 0:
        return JsonResponse({
            "status": "duplicate_data_different_filename",
            "message": "Data Overlap Alert: The property rows inside this workbook already exist verbatim in the system under another filename."
        })

    # Process workbook writes to dataset matrices safely
    created, updated, skipped, errors = 0, 0, 0, []
    for item in parsed_rows:
        o_data = item['data']
        r_id = item['row_id']
        o_data["upload_file_name"] = excel_file.name

        try:
            if r_id and r_id != "None":
                prop = RentalResidentialProperty.objects.filter(rental_residential_id=r_id).first()
                if prop:
                    for key, val in o_data.items(): setattr(prop, key, val)
                    prop.save()
                    updated += 1
                    continue

            dup_exists = RentalResidentialProperty.objects.filter(
                property_title=o_data.get('property_title'),
                address=o_data.get('address'),
                owner_name=o_data.get('owner_name'),
                contact_number=o_data.get('contact_number')
            ).exists()

            if dup_exists:
                skipped += 1
            else:
                RentalResidentialProperty.objects.create(**o_data)
                created += 1
        except Exception as e:
            errors.append(f"Row {item['row_idx']} processing failure: {str(e)}")

    # =====================================================
    # AUDIT LOGIC: File-wise Workbook Log Creation Entry
    # =====================================================
    RentalActivityLog.objects.create(
        user_identity=user_identity,
        user_role="Admin",
        action_type='EXCEL_IMPORT',
        property_id="Multiple / Sheet Records",
        targeted_fields="bulk_action",
        associated_file=excel_file.name,
        action_payload=json.dumps({
            "filename": excel_file.name,
            "records_created": created,
            "records_updated": updated,
            "records_skipped": skipped,
            "errors_encountered": len(errors)
        }),
        ip_address=_get_client_ip(request),
        status='SUCCESS' if not errors else 'PARTIAL'
    )

    return JsonResponse({
        "status": "success" if not errors else "partial_error",
        "message": f"{created} Created | {updated} Updated | {skipped} Skipped due to system rules.",
        "created": created, "updated": updated, "skipped": skipped, "error_count": len(errors), "errors": errors
    })


 
def download_residential_template(request):
    """Download new-style template aligned exactly with the RentalResidentialProperty model."""
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Rental Residential"

    from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
    from openpyxl.utils import get_column_letter

    HDR_BG, REQ_BG, OPT_BG, SAMP_BG = "667EEA", "FEF3C7", "F0FDF4", "ECFDF5"
    thin = Side(style="thin", color="CBD5E1")
    bdr = Border(left=thin, right=thin, top=thin, bottom=thin)

    # EXACT DB SEQUENCE
    sections = {
        "Basic Info": [
            "property_title","property_type", "bhk_type", 
            "renting_option", "built_up_area", "bathrooms", "balconies", 
            "floor_number", "total_floors", "facing", "furnishing_status", "available_for"
        ],
        "Property Details": [
            "zone", "ownership_type", "construction_status", "property_age", 
            "carpet_area", "plot_area", "building_name"
        ],
        "Availability": [
            "possession_status", "available_from", "lease_duration", 
            "brokerage", "brokerage_percentage", "manual_brokerage"
        ],
        "Pricing": [
            "monthly_rent", "security_deposit", "maintenance_type", "maintenance_amount"
        ],
        "Location": [
            "address", "city", "locality", "state", "pincode", "road_connectivity"
        ],
        "Description & Features": [
            "amenities", "facilities", "description", "rent_residential_desc"
        ],
        "Owner Info": [
            "owner_name", "contact_number", "email", "alternate_contact"
        ],
        "System Data": [
            "uploaded_by_name", "uploaded_by_email", "uploaded_by_contact", 
            "uploaded_by_role", "created_at"
        ],
    }

    HINTS = {
        "property_title": "Auto Generated Title By System", "property_type": "Apartment",
        "bhk_type": "1 BHK/2 BHK", "renting_option": "Full Property", "built_up_area": "sq.ft",
        "bathrooms": "Number", "balconies": "Number", "floor_number": "e.g. 5th Floor",
        "total_floors": "Number", "facing": "North/East", "furnishing_status": "Semi Furnished",
        "available_for": "Family/Bachelor", "zone": "North/South", "ownership_type": "Freehold",
        "construction_status": "Resale", "property_age": "1-3 Years", "carpet_area": "sq.ft",
        "plot_area": "sq.ft", "building_name": "Text", "possession_status": "Ready to Move",
        "available_from": "YYYY-MM-DD", "lease_duration": "11 Months", "brokerage": "Yes/No",
        "brokerage_percentage": "1%/Manual", "manual_brokerage": "e.g. 2.5%", "monthly_rent": "₹",
        "security_deposit": "₹", "maintenance_type": "Included in Rent/Extra", "maintenance_amount": "₹",
        "address": "Full Address", "city": "Text", "locality": "Text", "state": "e.g. Maharashtra",
        "pincode": "6-digit", "road_connectivity": "Optional", "amenities": "Comma-sep", 
        "facilities": "Comma-sep", "description": "Short Summary", "rent_residential_desc": "Long Rich Text",
        "owner_name": "Full Name", "contact_number": "10 Digits", "email": "email@example.com",
        "alternate_contact": "Optional", "uploaded_by_name": "Auto", "uploaded_by_email": "Auto",
        "uploaded_by_contact": "Auto", "uploaded_by_role": "Auto", "created_at": "YYYY-MM-DD (Auto)"
    }

    REQUIRED = {
        "property_type", "bhk_type", "renting_option", 
        "built_up_area", "bathrooms", "floor_number", "furnishing_status", 
        "available_for", "monthly_rent", "security_deposit", "address", 
        "city", "locality", "state", "pincode", "owner_name", "contact_number", "email"
    }

    SAMPLE = {
        "property_purpose": "rent", "property_type": "Apartment",
        "bhk_type": "2 BHK", "renting_option": "Full Property", "built_up_area": "1200",
        "bathrooms": "2", "balconies": "1", "floor_number": "5th Floor", "total_floors": "10",
        "facing": "East", "furnishing_status": "Semi Furnished", "available_for": "Family",
        "zone": "West", "ownership_type": "Freehold", "construction_status": "Resale",
        "property_age": "1-3 Years", "carpet_area": "950", "plot_area": "", "building_name": "Green Valley",
        "possession_status": "Ready to Move", "available_from": "2026-06-01", "lease_duration": "11 Months",
        "brokerage": "No", "brokerage_percentage": "", "manual_brokerage": "", "monthly_rent": "25000",
        "security_deposit": "50000", "maintenance_type": "Included in Rent", "maintenance_amount": "",
        "address": "Flat 402, Green Valley", "city": "Pune", "locality": "Kharadi", "state": "Maharashtra",
        "pincode": "411014", "road_connectivity": "Highway 1km", "amenities": "Wi-Fi, AC",
        "facilities": "Metro, Hospital", "description": "Great flat", "rent_residential_desc": "Full detailed html description...",
        "owner_name": "Rahul Sharma", "contact_number": "9876543210", "email": "rahul@test.com"
    }

    all_cols = []
    for sec, fields in sections.items():
        all_cols.extend([(sec, f) for f in fields])

    from collections import OrderedDict
    sec_spans = OrderedDict()
    for i, (sec, _) in enumerate(all_cols):
        sec_spans.setdefault(sec, []).append(i + 1)

    for sec, cols in sec_spans.items():
        c = ws.cell(row=1, column=cols[0], value=f"📋 {sec}")
        c.font = Font(bold=True, color="FFFFFF", name="Arial", size=11)
        c.fill = PatternFill("solid", fgColor=HDR_BG)
        c.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
        c.border = bdr
        if len(cols) > 1:
            ws.merge_cells(start_row=1, start_column=cols[0], end_row=1, end_column=cols[-1])

    for ci, (sec, field) in enumerate(all_cols, 1):
        req = field in REQUIRED
        lc = ws.cell(row=2, column=ci, value=field + (" *" if req else ""))
        lc.font = Font(bold=True, color="1E293B", name="Arial", size=9)
        lc.fill = PatternFill("solid", fgColor=REQ_BG if req else OPT_BG)
        lc.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
        lc.border = bdr

        hc = ws.cell(row=3, column=ci, value=HINTS.get(field, ""))
        hc.font = Font(italic=True, color="64748B", name="Arial", size=8)
        hc.fill = PatternFill("solid", fgColor="FFFFFF")
        hc.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
        hc.border = bdr

        sc = ws.cell(row=4, column=ci, value=SAMPLE.get(field, ""))
        sc.font = Font(name="Arial", size=9, color="065F46")
        sc.fill = PatternFill("solid", fgColor=SAMP_BG)
        sc.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
        sc.border = bdr

        ws.column_dimensions[get_column_letter(ci)].width = max(16, len(field) + 4)

    ws.row_dimensions[1].height = 28
    ws.row_dimensions[2].height = 36
    ws.row_dimensions[3].height = 42
    ws.row_dimensions[4].height = 26
    ws.freeze_panes = "A5"

    response = HttpResponse(content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    response["Content-Disposition"] = 'attachment; filename="Rental_Residential_Template.xlsx"'
    wb.save(response)
    return response





def rental_residential_view(request, pk):
    session_id = request.session.get('Admin_id')
    if not session_id:
        return render(request, 'home_page/Adminlogin.html')

    # Prefetch core and related assets for the current listing
    prop = get_object_or_404(
        RentalResidentialProperty.objects.prefetch_related('images', 'faqs'), 
        pk=pk
    )
    
    # Context cross-linking: Pull the latest uploaded properties along with their dynamic FAQs
    latest_properties = RentalResidentialProperty.objects.filter(
        is_deleted=False
    ).exclude(
        rental_residential_id=prop.rental_residential_id
    ).prefetch_related('faqs').order_by('-created_at')[:4]

    # Convert comma-separated string arrays smoothly
    amenities_list = [x.strip() for x in prop.amenities.split(',')] if prop.amenities else []
    facilities_list = [x.strip() for x in prop.facilities.split(',')] if prop.facilities else []

    context = {
        'property': prop,
        'images': prop.images.all(),
        'faqs': prop.faqs.all(), # Dynamic property FAQs
        'amenities_list': amenities_list,
        'facilities_list': facilities_list,
        'latest_properties': latest_properties, # Direct cross-linking hook
    }
    return render(request, 'admin_user/Reports/Rental/rental_residential_detail.html', context)



def _get_client_ip(request):
    """Helper to safely fetch client IP address reference."""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        return x_forwarded_for.split(',')[0].strip()
    return request.META.get('REMOTE_ADDR', '127.0.0.1')


def rental_residential_edit(request, pk):
    # Retrieve the property using the custom primary key
    prop = get_object_or_404(RentalResidentialProperty, rental_residential_id=pk)
    
    session_id = request.session.get('Admin_id')
    if not session_id:
        return render(request, 'home_page/Adminlogin.html')

    admin_obj = Admin_Login.objects.get(id=session_id)
    
    if request.method == 'POST':
        try:
            # =====================================================
            # AUDIT LOGIC: Snapshot current state BEFORE modification
            # =====================================================
            tracked_fields_list = [
                'property_title', 'property_type', 'bhk_type', 'renting_option',
                'built_up_area', 'bathrooms', 'balconies', 'floor_number', 'total_floors',
                'facing', 'furnishing_status', 'available_for', 'zone', 'ownership_type',
                'construction_status', 'property_age', 'carpet_area', 'plot_area',
                'building_name', 'possession_status', 'available_from', 'lease_duration',
                'brokerage', 'brokerage_percentage', 'manual_brokerage', 'monthly_rent',
                'security_deposit', 'maintenance_type', 'maintenance_amount', 'address',
                'city', 'locality', 'state', 'pincode', 'owner_name', 'contact_number', 'email'
            ]
            old_state_snapshot = {field: str(getattr(prop, field, '')) for field in tracked_fields_list}

            # =====================================================
            # 1. BASIC INFORMATION
            # =====================================================
            prop.property_title = request.POST.get('property_title')
            prop.property_type = request.POST.get('property_type')
            prop.bhk_type = request.POST.get('bhk_type')
            prop.renting_option = request.POST.get('renting_option')
            
            prop.built_up_area = request.POST.get('built_up_area') or None
            prop.bathrooms = request.POST.get('bathrooms') or None
            prop.balconies = request.POST.get('balconies') or None
            
            prop.floor_number = request.POST.get('floor_number')
            prop.total_floors = request.POST.get('total_floors') or None
            prop.facing = request.POST.get('facing')
            prop.furnishing_status = request.POST.get('furnishing_status')
            prop.available_for = request.POST.get('available_for')

            # =====================================================
            # 2. PROPERTY DETAILS
            # =====================================================
            prop.zone = request.POST.get('zone')
            prop.ownership_type = request.POST.get('ownership_type')
            prop.construction_status = request.POST.get('construction_status')
            prop.property_age = request.POST.get('property_age')
            
            prop.carpet_area = request.POST.get('carpet_area') or None
            prop.plot_area = request.POST.get('plot_area') or None
            prop.building_name = request.POST.get('building_name')

            # =====================================================
            # 3. AVAILABILITY DETAILS
            # =====================================================
            prop.possession_status = request.POST.get('possession_status')
            
            available_from_raw = request.POST.get('available_from')
            if available_from_raw and available_from_raw.strip():
                try:
                    prop.available_from = datetime.strptime(available_from_raw.strip(), "%Y-%m-%d").date()
                except ValueError:
                    prop.available_from = None
            else:
                prop.available_from = None
                
            prop.lease_duration = request.POST.get('lease_duration')
            prop.brokerage = request.POST.get('brokerage')
            prop.brokerage_percentage = request.POST.get('brokerage_percentage')
            prop.manual_brokerage = request.POST.get('manual_brokerage')

            # =====================================================
            # 4. PRICING DETAILS
            # =====================================================
            monthly_rent_raw = request.POST.get('monthly_rent')
            prop.monthly_rent = int(monthly_rent_raw) if monthly_rent_raw and monthly_rent_raw.isdigit() else None

            security_deposit_raw = request.POST.get('security_deposit')
            prop.security_deposit = int(security_deposit_raw) if security_deposit_raw and security_deposit_raw.isdigit() else None

            prop.maintenance_type = request.POST.get('maintenance_type')

            maintenance_amount_raw = request.POST.get('maintenance_amount')
            prop.maintenance_amount = int(maintenance_amount_raw) if maintenance_amount_raw and maintenance_amount_raw.isdigit() else None

            # =====================================================
            # 5. LOCATION DETAILS
            # =====================================================
            prop.address = request.POST.get('address')
            prop.city = request.POST.get('city')
            prop.locality = request.POST.get('locality')
            prop.state = request.POST.get('state')
            prop.pincode = request.POST.get('pincode')
            prop.road_connectivity = request.POST.get('road_connectivity')

            # =====================================================
            # 6. AMENITIES & FACILITIES
            # =====================================================
            prop.amenities = ",".join(request.POST.getlist('amenities[]'))
            prop.facilities = ",".join(request.POST.getlist('facilities[]'))

            # =====================================================
            # 7. DESCRIPTION
            # =====================================================
            prop.description = request.POST.get('description')
            prop.rent_residential_desc = request.POST.get('rent_residential_desc')

            # =====================================================
            # 8. OWNER DETAILS
            # =====================================================
            prop.owner_name = request.POST.get('owner_name')
            prop.contact_number = request.POST.get('contact_number')
            prop.email = request.POST.get('email')
            prop.alternate_contact = request.POST.get('alternate_contact')

            # =====================================================
            # 9. UPLOADED BY DETAILS & SYSTEM FILES
            # =====================================================
            prop.uploaded_by_name = request.POST.get('uploaded_by_name', prop.uploaded_by_name)
            prop.uploaded_by_email = request.POST.get('uploaded_by_email', prop.uploaded_by_email)
            prop.uploaded_by_contact = request.POST.get('uploaded_by_contact', prop.uploaded_by_contact)
            prop.uploaded_by_role = request.POST.get('uploaded_by_role', prop.uploaded_by_role)
            prop.upload_file_name = request.POST.get('upload_file_name', prop.upload_file_name)

            # Save core instance data changes
            prop.save()

            # =====================================================
            # 10. IMAGE UPLOAD & SEQUENCE LOGIC
            # =====================================================
            images = request.FILES.getlist('property_images[]')
            current_count = prop.images.count()

            for img in images:
                if current_count < 10:
                    RentalResidentialImage.objects.create(property=prop, image=img)
                    current_count += 1

            # =====================================================
            # AUDIT LOGIC: Generate field modifications diff dictionary
            # =====================================================
            modifications_diff = {}
            modified_fields_summary = []
            
            for field in tracked_fields_list:
                new_val = str(getattr(prop, field, ''))
                if old_state_snapshot[field] != new_val:
                    modifications_diff[field] = {
                        "old_value": old_state_snapshot[field],
                        "new_value": new_val
                    }
                    modified_fields_summary.append(field)

            # Save the structural field adjustments to the activity stream
            if modified_fields_summary:
                RentalActivityLog.objects.create(
                    user_identity=admin_obj.email or admin_obj.username,
                    user_role="Admin",
                    action_type='UPDATE',
                    property_id=prop.rental_residential_id,
                    targeted_fields=", ".join(modified_fields_summary[:4]) + ("..." if len(modified_fields_summary) > 4 else ""),
                    associated_file=prop.upload_file_name or "Web UI Form",
                    action_payload=json.dumps(modifications_diff),
                    ip_address=_get_client_ip(request),
                    status='SUCCESS'
                )

            return JsonResponse({
                'status': 'success',
                'message': 'Property updated successfully!',
                'redirect_url': reverse('residential_list')
            })

        except Exception as e:
            # Audit log execution error tracks
            RentalActivityLog.objects.create(
                user_identity=admin_obj.email if 'admin_obj' in locals() else "Unknown Session",
                user_role="Admin",
                action_type='UPDATE',
                property_id=pk,
                targeted_fields="System Errors",
                action_payload=f"Failed modification update runtime sequence execution target: {str(e)}",
                ip_address=_get_client_ip(request),
                status='FAILED'
            )
            return JsonResponse({
                'status': 'error',
                'message': f"Failed to save data: {str(e)}"
            }, status=400)

    # ---------- GET METHOD: RENDER FORM ----------
    return render(request, 'admin_user/rental_residential_edit.html', {
        'property': prop,
        'admin_obj': admin_obj,
        'ameneties_obj': Ameneties_Details.objects.all(),
        'facilities_obj': Facilities_Details.objects.all()
    })





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

            amenities_list = request.POST.getlist('amenities[]')
            facilities_list = request.POST.getlist('nearby_facilities[]')

            prop = CommercialRentalProperty.objects.create(
                # ✅ Added the newly auto-generated property title field
                property_title=request.POST.get('property_title'), 
                
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

                # ✅ Fixed: Now saves directly as a string to match the updated CharField model
                negotiable=request.POST.get('negotiable'),

                brokerage=request.POST.get('brokerage'),
                brokerage_percentage=request.POST.get('brokerage_percentage'),
                manual_brokerage=request.POST.get('manual_brokerage'),

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

                amenities=amenities_list,
                nearby_facilities=facilities_list,

                property_summary=request.POST.get('property_summary'),
                property_description=request.POST.get('property_description'),

               
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
            
            # The enumerate(images) loop automatically reads them in the sequence they were dragged/dropped!
            for i, img in enumerate(images):
                if i >= 10:
                    break
                CommercialRentalPropertyImage.objects.create(
                    property=prop,
                    image=img
                    # display_order=i  <-- Uncomment this if you added a display_order field to your image model
                )

            return JsonResponse({
                "status": "success",
                "message": "Commercial Rental Property Added Successfully"
            })

    except Exception as e:
        print("ERROR:", str(e))
        traceback.print_exc()
        return JsonResponse({
            "status": "error",
            "message": str(e)
        })

    return render(request, 'admin_user/Reports/Rental/commercial_list.html')




# ─────────────────────────────
# VIEW PROPERTY






def _get_admin(request):
    sid = request.session.get('Admin_id')
    admin_obj = None
    if sid:
        try:
            admin_obj = Admin_Login.objects.get(id=sid)
        except Admin_Login.DoesNotExist:
            sid = None
    return sid, admin_obj

def _to_int(val):
    if not val: return None
    try: return int(val)
    except ValueError: return None

def _to_float(val):
    if not val: return None
    try: return float(val)
    except ValueError: return None

def _to_date(val):
    return val if val else None

# ═══════════════════════════════════════
# COMMERCIAL DETAILS VIEW
# ═══════════════════════════════════════
def commercial_view(request, pk):
    sid, admin_obj = _get_admin(request)
    if not sid:
        return render(request, 'home_page/Adminlogin.html')

    prop = get_object_or_404(CommercialRentalProperty, pk=pk)

    return render(request, 'admin_user/Reports/Rental/commercial_detail.html', {
        'admin_obj': admin_obj,
        'prop': prop,
    })

# ═══════════════════════════════════════
# COMMERCIAL EDIT/UPDATE VIEW
# ═══════════════════════════════════════
def commercial_edit(request, pk):
    sid, admin_obj = _get_admin(request)
    if not sid:
        return render(request, 'home_page/Adminlogin.html')

    prop = get_object_or_404(CommercialRentalProperty, pk=pk)

    if request.method == 'POST':
        try:
            p = request.POST

            # STEP 1: Basic Info Parameter Processing
            prop.property_title = p.get('property_title')
            prop.property_type = p.get('property_type')
            prop.property_condition = p.get('property_condition')
            prop.city = p.get('city')
            prop.area_locality = p.get('area_locality')
            prop.property_address = p.get('property_address')
            prop.building_name = p.get('building_name')
            prop.possession_status = p.get('possession_status')
            prop.available_from = _to_date(p.get('available_from'))
            prop.age_of_property = p.get('age_of_property')
            prop.zone_type = p.get('zone_type')
            prop.location_hub = p.get('location_hub')
            prop.ownership_type = p.get('ownership_type')
            prop.construction_status = p.get('construction_status')

            # STEP 2: Area, Pricing & Building Specifications
            prop.builtup_area = _to_int(p.get('builtup_area')) or 0
            prop.carpet_area = _to_int(p.get('carpet_area'))
            prop.expected_rent = _to_int(p.get('expected_rent')) or 0
            prop.security_deposit = _to_int(p.get('security_deposit'))
            prop.maintenance_charges = _to_int(p.get('maintenance_charges'))
            
            # Form saves radio values directly as matching CharField string format ('Yes'/'No')
            prop.negotiable = p.get('negotiable')

            prop.brokerage = p.get('brokerage')
            prop.brokerage_percentage = p.get('brokerage_percentage')
            prop.manual_brokerage = p.get('manual_brokerage')

            prop.dg_ups_included = True if p.get('dg_ups_included') == 'on' else False
            prop.electricity_included = True if p.get('electricity_included') == 'on' else False
            prop.water_included = True if p.get('water_included') == 'on' else False

            prop.lockin_period = _to_int(p.get('lockin_period'))
            prop.rent_increase = _to_float(p.get('rent_increase'))
            prop.total_floors = _to_int(p.get('total_floors'))
            prop.your_floor = _to_int(p.get('your_floor'))
            prop.staircases = _to_int(p.get('staircases'))
            prop.passenger_lifts = _to_int(p.get('passenger_lifts')) or 0
            prop.service_lifts = _to_int(p.get('service_lifts')) or 0
            prop.private_parking = _to_int(p.get('private_parking')) or 0
            prop.min_seats = _to_int(p.get('min_seats'))
            prop.max_seats = _to_int(p.get('max_seats'))
            prop.cabins = _to_int(p.get('cabins'))
            prop.meeting_rooms = _to_int(p.get('meeting_rooms'))
            prop.private_washroom = _to_int(p.get('private_washroom')) or 0
            prop.public_washroom = _to_int(p.get('public_washroom')) or 0
            prop.flooring_type = p.get('flooring_type')

            # STEP 3: Amenities & Summary Overwrites
            prop.amenities = request.POST.getlist('amenities[]')
            prop.nearby_facilities = request.POST.getlist('nearby_facilities[]')
            prop.property_summary = p.get('property_summary')
            prop.property_description = p.get('property_description')

            # STEP 4: Owner Verification Registry Mapping
            prop.owner_name = p.get('owner_name')
            prop.contact_number = p.get('contact_number')
            prop.email = p.get('email')
            prop.alternate_contact = p.get('alternate_contact')

            # Core media attachments upload logic handlers
            if 'floor_plan' in request.FILES:
                prop.floor_plan = request.FILES['floor_plan']
            if 'video' in request.FILES:
                prop.video = request.FILES['video']

            prop.save()

            # Multiple additional imagery append processing loops
            images = request.FILES.getlist('property_images[]')
            current_count = prop.images.count()
            
            for img in images:
                if current_count < 10:
                    CommercialRentalPropertyImage.objects.create(
                        property=prop,
                        image=img
                    )
                    current_count += 1

            return JsonResponse({
                'status': 'success',
                'message': 'Property registry updated successfully!',
                'redirect_url': reverse('commercial_list')
            })

        except Exception as e:
            traceback.print_exc()
            return JsonResponse({
                'status': 'error',
                'message': f"Update operation failure: {str(e)}"
            }, status=400)

    # ---------- GET REQUEST PROCESSING ----------
    return render(request, 'admin_user/commercial_edit.html', {
        'admin_obj': admin_obj,
        'prop': prop,
        'ameneties_obj': Ameneties_Details.objects.all(),
        'facilities_obj': Facilities_Details.objects.all()
    })

# ─────────────────────────────
# DELETE
@require_POST
def commercial_delete(request, pk):
    # Auth check
    sid, _ = _get_admin(request)
    if not sid:
        return JsonResponse({'status': 'error'}, status=401)

    # Grab the deleter's name using our helper!
    deleter_name = _get_deleter_name(request)

    prop = get_object_or_404(CommercialRentalProperty, pk=pk)
    prop.is_deleted = True
    prop.deleted_at = timezone.now()
    prop.deleted_by = deleter_name # 👈 SAVE THE NAME HERE
    prop.save()

    return JsonResponse({'status': 'success', 'message': 'Moved to Recycle Bin successfully!'})


@require_POST
def commercial_restore(request, id):
    CommercialRentalProperty.objects.filter(id=id).update(is_deleted=False, deleted_at=None, deleted_by=None)
    return JsonResponse({'status': 'success', 'message': 'Commercial property restored!'})

@require_POST
def commercial_hard_delete(request, id):
    CommercialRentalProperty.objects.filter(id=id).delete()
    return JsonResponse({'status': 'success', 'message': 'Permanently deleted!'})



def _bool(val):
    # Converts "Yes", "True", "1" from Excel to Python True
    if str(val).strip().lower() in ['yes', 'true', '1', 'y']:
        return True
    return False




import io
import openpyxl
from collections import OrderedDict
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter
from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_POST
# Ensure your CommercialRentalProperty model is imported
# from .models import CommercialRentalProperty





import hashlib

# --- EXCEL HELPER CONVERTERS ---
def _str(v): return str(v).strip() if v is not None else ""
def _int(v): return int(float(v)) if v else None
def _float(v): return float(v) if v else None
def _bool(v): return str(v).strip().lower() in ['true', 'yes', '1', 'on'] if v else False
def _date(v): 
    if not v: return None
    if hasattr(v, 'date'): return v.date()
    return str(v).strip()[:10]

def _get_cell(row, col_idx):
    if col_idx is None or col_idx >= len(row): return None
    return row[col_idx]

def _load_new_excel(excel_file):
    wb = openpyxl.load_workbook(excel_file, data_only=True)
    ws = wb.active
    # Row 2 contains the database field names (labels)
    headers = {str(cell.value).replace(' *', '').strip(): idx for idx, cell in enumerate(ws[2]) if cell.value}
    return wb, ws, headers

# --- EXCEL TO MODEL FIELD MAPPING ---
COMMERCIAL_RENTAL_COLUMN_MAP = [
    ("property_type", "property_type", _str), ("property_condition", "property_condition", _str),
    ("city", "city", _str), ("area_locality", "area_locality", _str),
    ("property_address", "property_address", _str), ("building_name", "building_name", _str),
    ("possession_status", "possession_status", _str), ("available_from", "available_from", _date),
    ("age_of_property", "age_of_property", _str), ("zone_type", "zone_type", _str),
    ("location_hub", "location_hub", _str), ("ownership_type", "ownership_type", _str),
    ("construction_status", "construction_status", _str), ("builtup_area", "builtup_area", _int),
    ("carpet_area", "carpet_area", _int), ("expected_rent", "expected_rent", _int),
    ("security_deposit", "security_deposit", _int), ("maintenance_charges", "maintenance_charges", _int),
    ("negotiable", "negotiable", _str), ("brokerage", "brokerage", _str),
    ("brokerage_percentage", "brokerage_percentage", _str), ("manual_brokerage", "manual_brokerage", _str),
    ("dg_ups_included", "dg_ups_included", _bool), ("electricity_included", "electricity_included", _bool),
    ("water_included", "water_included", _bool), ("lockin_period", "lockin_period", _int),
    ("rent_increase", "rent_increase", _float), ("total_floors", "total_floors", _int),
    ("your_floor", "your_floor", _int), ("staircases", "staircases", _int),
    ("passenger_lifts", "passenger_lifts", _int), ("service_lifts", "service_lifts", _int),
    ("private_parking", "private_parking", _int), ("min_seats", "min_seats", _int),
    ("max_seats", "max_seats", _int), ("cabins", "cabins", _int),
    ("meeting_rooms", "meeting_rooms", _int), ("private_washroom", "private_washroom", _int),
    ("public_washroom", "public_washroom", _int), ("flooring_type", "flooring_type", _str),
    ("amenities", "amenities", _str), ("nearby_facilities", "nearby_facilities", _str),
    ("property_summary", "property_summary", _str), ("property_description", "property_description", _str),
    ("owner_name", "owner_name", _str), ("contact_number", "contact_number", _str),
    ("email", "email", _str), ("alternate_contact", "alternate_contact", _str),
]



@require_POST
def import_commercial_rental_excel(request):
    excel_file = request.FILES.get("commercial_file")
    
    if not excel_file:
        return JsonResponse({"status": "error", "message": "No file uploaded."}, status=400)
    if not excel_file.name.endswith(".xlsx"):
        return JsonResponse({"status": "error", "message": "Only .xlsx files accepted."}, status=400)

    # ==========================================
    # 0. GET UPLOADER DETAILS (Like your Add form)
    # ==========================================
    admin_id = request.session.get('Admin_id')
    user_id = request.session.get('User_id')

    uploader_name = ""
    uploader_email = ""
    uploader_phone = ""
    uploader_role = ""

    if admin_id:
        admin = Admin_Login.objects.filter(id=admin_id).first()
        if admin:
            uploader_name, uploader_email, uploader_phone, uploader_role = admin.name, admin.email, admin.phone, admin.role
    elif user_id:
        user = User_Details.objects.filter(id=user_id).first()
        if user:
            uploader_name, uploader_email, uploader_phone, uploader_role = user.name, user.email, user.phone, user.role

    # ==========================================
    # 1. SMART DUPLICATE FILE DETECTION
    # ==========================================
    file_content = excel_file.read()
    file_hash = hashlib.sha256(file_content).hexdigest()
    excel_file.seek(0) # IMPORTANT: Reset file pointer so openpyxl can read it!

    # Validates by content hash: Rejects duplicate content regardless of file name.
    if CommercialRentalProperty.objects.filter(upload_file_hash=file_hash).exists():
        return JsonResponse({
            "status": "error", 
            "message": "Duplicate Data Detected! This exact file content has already been uploaded."
        }, status=400)

    try:
        wb, ws, headers = _load_new_excel(excel_file)
    except Exception as e:
        return JsonResponse({"status": "error", "message": f"Cannot open Excel file: {str(e)}"}, status=400)

    # ==========================================
    # 2. REQUIRED COLUMNS VALIDATION
    # ==========================================
    REQUIRED_EXCEL_COLUMNS = [
        "property_type", "property_condition", "city", "area_locality", 
        "property_address", "building_name", "possession_status", 
        "age_of_property", "ownership_type", "builtup_area", 
        "expected_rent", "owner_name", "contact_number", "email"
    ]
    
    missing_cols = [col for col in REQUIRED_EXCEL_COLUMNS if col not in headers]
    if missing_cols:
        return JsonResponse({
            "status": "error", 
            "message": f"Missing required columns in your Excel file:\n{', '.join(missing_cols)}"
        }, status=400)

    created = 0
    errors = []
    file_name = excel_file.name

    # ==========================================
    # 3. ROW VALIDATION & ATOMIC SAVE
    # ==========================================
    try:
        with transaction.atomic():
            
            for row_idx, row in enumerate(ws.iter_rows(min_row=4, values_only=True), start=4):
                
                # Skip entirely empty rows
                if all(v is None or str(v).strip() == "" for v in row):
                    continue

                # A. Check missing required cells
                row_missing_data = []
                for req_col in REQUIRED_EXCEL_COLUMNS:
                    val = _get_cell(row, headers.get(req_col))
                    if val is None or str(val).strip() == "":
                        row_missing_data.append(req_col)
                
                if row_missing_data:
                    errors.append(f"Row {row_idx}: Missing required data -> {', '.join(row_missing_data)}")
                    continue 

                # B. Map Data
                obj_data = {
                    "upload_file_name": file_name, 
                    "upload_file_hash": file_hash,
                    "uploaded_by_name": uploader_name,
                    "uploaded_by_email": uploader_email,
                    "uploaded_by_contact": uploader_phone,
                    "uploaded_by_role": uploader_role,
                }
                
                has_format_error = False
                for excel_col, model_field, converter in COMMERCIAL_RENTAL_COLUMN_MAP:
                    raw = _get_cell(row, headers.get(excel_col))
                    try:
                        val = converter(raw)
                        if val is not None and val != "":
                            obj_data[model_field] = val
                    except Exception as e:
                        errors.append(f"Row {row_idx}: Invalid format in '{excel_col}'")
                        has_format_error = True
                        break

                if has_format_error:
                    continue

                # C. Format JSON Lists
                for fld in ('amenities', 'nearby_facilities'):
                    raw_str = obj_data.get(fld)
                    if isinstance(raw_str, str) and raw_str:
                        obj_data[fld] = [x.strip() for x in raw_str.split(',') if x.strip()]
                    else:
                        obj_data[fld] = []

                # D. Attempt Database Save (Catches Database Integrity Errors safely)
                try:
                    CommercialRentalProperty.objects.create(**obj_data)
                    created += 1
                except Exception as db_e:
                    errors.append(f"Row {row_idx} Database Error: Check data lengths and types.")

            # If ANY errors were collected across all rows, abort the transaction!
            if errors:
                raise Exception("Data Validation Failed")

    except Exception as e:
        if str(e) == "Data Validation Failed":
            error_list = "\n".join(errors[:8]) 
            if len(errors) > 8:
                error_list += f"\n\n...and {len(errors) - 8} more errors."
                
            return JsonResponse({
                "status": "error",
                "message": "Upload Failed! Please fix these rows and try again:\n\n" + error_list
            }, status=400)
        else:
            return JsonResponse({"status": "error", "message": f"Server Error: {str(e)}"}, status=500)

    wb.close()
    
    if created == 0 and not errors:
        return JsonResponse({"status": "error", "message": "The uploaded file contained no valid data rows to import."}, status=400)

    return JsonResponse({
        "status": "success",
        "message": f"Successfully imported {created} properties!"
    })

# ═══════════════════════════════════════
# DOWNLOAD TEMPLATE FUNCTION
# ═══════════════════════════════════════
def download_commercial_rental12__template(request):
    """New-style Commercial Rental template: Row1=banners, Row2=labels, Row3=hints, Row4=sample."""

    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Commercial Rental"

    HDR_BG  = "667EEA"   # section banner – indigo
    REQ_BG  = "FEF3C7"   # required field – amber
    OPT_BG  = "F0FDF4"   # optional field – green-tint
    SAMP_BG = "ECFDF5"   # sample row – mint

    thin = Side(style="thin", color="CBD5E1")
    bdr  = Border(left=thin, right=thin, top=thin, bottom=thin)

    # Ordered exactly as per your database model
    # Format: (Section, Column Name, isRequired, Hint Text, Sample Data)
    COLS = [
        # ── Basic Info ────────────────────────────────────────────────────────
        ("Basic Info", "property_title",      False,  "Auto Generated By System",          ""),
        ("Basic Info", "property_type",       True,  "office-space / shop / warehouse / industrial / land",          "office-space"),
        ("Basic Info", "property_condition",  True,  "bare-shell / warm-shell / fitted / furnished",                 "bare-shell"),
        ("Basic Info", "city",                True,  "City name",                                                    "Pune"),
        ("Basic Info", "area_locality",       True,  "Area/locality",                                                "Viman Nagar"),
        ("Basic Info", "property_address",    True,  "Complete address",                                             "Tower A, Viman Nagar, Pune"),
        ("Basic Info", "building_name",       True,  "Building/project name",                                        "Alpha Tower"),
        ("Basic Info", "possession_status",   True,  "ready-to-move / under-construction",                           "ready-to-move"),
        ("Basic Info", "available_from",      False, "YYYY-MM-DD",                                                   "2026-08-01"),
        ("Basic Info", "age_of_property",     True,  "0-1 / 1-3 / 3-5 / 5-10 / 10+",                                 "1-3"),
        ("Basic Info", "zone_type",           False, "industrial / commercial / residential / special-economic",     "commercial"),
        ("Basic Info", "location_hub",        False, "it-park / business-district / mall / standalone",              "it-park"),
        ("Basic Info", "ownership_type",      True,  "freehold / leasehold / co-operative",                          "freehold"),
        ("Basic Info", "construction_status", False, "new / resale",                                                 "resale"),
        
        # ── Area, Pricing & Building ──────────────────────────────────────────
        ("Area, Pricing & Building", "builtup_area",         True,  "Number in sq.ft",                        "2000"),
        ("Area, Pricing & Building", "carpet_area",          False, "Number in sq.ft",                        "1700"),
        ("Area, Pricing & Building", "expected_rent",        True,  "Monthly rent in ₹",                      "85000"),
        ("Area, Pricing & Building", "security_deposit",     False, "Deposit in ₹",                           "500000"),
        ("Area, Pricing & Building", "maintenance_charges",  False, "Monthly maintenance in ₹",               "5000"),
        ("Area, Pricing & Building", "negotiable",           False, "Yes / No",                               "Yes"),
        ("Area, Pricing & Building", "brokerage",            False, "Yes / No",                               "No"),
        ("Area, Pricing & Building", "brokerage_percentage", False, "1% / 1.5% / 2% / Negotiable / Manual",   ""),
        ("Area, Pricing & Building", "manual_brokerage",     False, "e.g. 2.5% (if Manual)",                  ""),
        ("Area, Pricing & Building", "dg_ups_included",      False, "true / false",                           "true"),
        ("Area, Pricing & Building", "electricity_included", False, "true / false",                           "false"),
        ("Area, Pricing & Building", "water_included",       False, "true / false",                           "false"),
        ("Area, Pricing & Building", "lockin_period",        False, "Lock-in months",                         "6"),
        ("Area, Pricing & Building", "rent_increase",        False, "% per year e.g. 5",                      "5"),
        ("Area, Pricing & Building", "total_floors",         False, "Total floors in building",               "10"),
        ("Area, Pricing & Building", "your_floor",           False, "Floor of this property",                 "4"),
        ("Area, Pricing & Building", "staircases",           False, "Number of staircases",                   "2"),
        ("Area, Pricing & Building", "passenger_lifts",      False, "Number (use 0 if none)",                 "2"),
        ("Area, Pricing & Building", "service_lifts",        False, "Number (use 0 if none)",                 "1"),
        ("Area, Pricing & Building", "private_parking",      False, "Number of private parking spots",        "2"),
        ("Area, Pricing & Building", "min_seats",            False, "Minimum seating capacity",               "20"),
        ("Area, Pricing & Building", "max_seats",            False, "Maximum seating capacity",               "50"),
        ("Area, Pricing & Building", "cabins",               False, "Number of cabins",                       "5"),
        ("Area, Pricing & Building", "meeting_rooms",        False, "Number of meeting rooms",                "2"),
        ("Area, Pricing & Building", "private_washroom",     False, "Number (use 0 if none)",                 "1"),
        ("Area, Pricing & Building", "public_washroom",      False, "Number (use 0 if none)",                 "2"),
        ("Area, Pricing & Building", "flooring_type",        False, "marble / vitrified / granite / wooden / ceramic", "vitrified"),
        
        # ── Amenities & Facilities ────────────────────────────────────────────
        ("Amenities & Facilities", "amenities",            False,  "Comma-sep e.g. Wi-Fi,AC,CCTV,Generator",  "Wi-Fi,AC,CCTV"),
        ("Amenities & Facilities", "nearby_facilities",    False,  "Comma-sep e.g. Metro,Bank,Parking",       "Metro,Bank"),
        ("Amenities & Facilities", "property_summary",     False,  "Short plain-text description",            "Prime office space with fit-out."),
        ("Amenities & Facilities", "property_description", False,  "Full Detailed Description",               "Elevate your business presence..."),
        
        # ── Contact Info ──────────────────────────────────────────────────────
        ("Contact Info", "owner_name",          True,  "Full name",              "Rahul Mehta"),
        ("Contact Info", "contact_number",      True,  "10 Digits",              "9876543210"),
        ("Contact Info", "email",               True,  "email@example.com",      "rahul@email.com"),
        ("Contact Info", "alternate_contact",   False, "10 Digits",              ""),
        ("Contact Info", "uploaded_by_name",    False, "Auto-filled (Optional)", ""),
        ("Contact Info", "uploaded_by_email",   False, "Auto-filled (Optional)", ""),
        ("Contact Info", "uploaded_by_contact", False, "Auto-filled (Optional)", ""),
        ("Contact Info", "uploaded_by_role",    False, "Auto-filled (Optional)", ""),
    ]

    # ── Row 1: Section Banners ────────────────────────────────────────────────
    sec_spans = OrderedDict()
    for i, (sec, *_) in enumerate(COLS):
        sec_spans.setdefault(sec, []).append(i + 1)

    for sec, cols in sec_spans.items():
        c = ws.cell(row=1, column=cols[0], value=f"📋 {sec}")
        c.font      = Font(bold=True, color="FFFFFF", name="Arial", size=11)
        c.fill      = PatternFill("solid", fgColor=HDR_BG)
        c.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
        c.border    = bdr
        if len(cols) > 1:
            ws.merge_cells(start_row=1, start_column=cols[0],
                           end_row=1,   end_column=cols[-1])

    # ── Rows 2 / 3 / 4 ───────────────────────────────────────────────────────
    for ci, (sec, field, req, hint, sample) in enumerate(COLS, 1):
        # Row 2 – label
        lc = ws.cell(row=2, column=ci, value=field + (" *" if req else ""))
        lc.font      = Font(bold=True, color="1E293B", name="Arial", size=9)
        lc.fill      = PatternFill("solid", fgColor=REQ_BG if req else OPT_BG)
        lc.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
        lc.border    = bdr

        # Row 3 – hint
        hc = ws.cell(row=3, column=ci, value=hint)
        hc.font      = Font(italic=True, color="64748B", name="Arial", size=8)
        hc.fill      = PatternFill("solid", fgColor="FFFFFF")
        hc.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
        hc.border    = bdr

        # Row 4 – sample
        sc = ws.cell(row=4, column=ci, value=sample)
        sc.font      = Font(name="Arial", size=9, color="065F46")
        sc.fill      = PatternFill("solid", fgColor=SAMP_BG)
        sc.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
        sc.border    = bdr

        # Adjust column width based on field name length
        ws.column_dimensions[get_column_letter(ci)].width = max(18, len(field) + 4)

    ws.row_dimensions[1].height = 28
    ws.row_dimensions[2].height = 36
    ws.row_dimensions[3].height = 42
    ws.row_dimensions[4].height = 26
    ws.freeze_panes = "A5"

    buf = io.BytesIO()
    wb.save(buf)
    buf.seek(0)
    response = HttpResponse(
        buf.getvalue(),
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )
    response["Content-Disposition"] = 'attachment; filename="Commercial_Rental_Template.xlsx"'
    return response



from django.db.models import Sum, Count







def commercial_list(request):
    session_id = request.session.get('Admin_id')
    if not session_id:
        return render(request, 'home_page/Adminlogin.html')

    admin_obj = Admin_Login.objects.get(id=session_id)

    # ═══════════════════════════════════════
    # CAPTURE ADVANCED FILTER QUERY PARAMS
    # ═══════════════════════════════════════
    search_query = request.GET.get('search', '').strip()
    prop_type_query = request.GET.get('property_type', '').strip()
    city_query = request.GET.get('city', '').strip()
    zone_query = request.GET.get('zone_type', '').strip()
    possession_query = request.GET.get('possession', '').strip()
    listed_by_query = request.GET.get('listed_by', '').strip()
    budget_query = request.GET.get('budget', '').strip()
    from_date_str = request.GET.get('from_date', '').strip()
    to_date_str = request.GET.get('to_date', '').strip()

    # Base Active Queryset 
    properties = CommercialRentalProperty.objects.filter(is_deleted=False)

    # ═══════════════════════════════════════
    # EXECUTE DYNAMIC ADVANCED FILTERS
    # ═══════════════════════════════════════
    if search_query:
        properties = properties.filter(
            Q(property_title__icontains=search_query) |
            Q(city__icontains=search_query) |
            Q(area_locality__icontains=search_query) |
            Q(building_name__icontains=search_query) |
            Q(owner_name__icontains=search_query)
        )

    if prop_type_query and prop_type_query != "All Types":
        properties = properties.filter(property_type__iexact=prop_type_query)

    if city_query and city_query != "All Cities":
        properties = properties.filter(city__iexact=city_query)

    if zone_query and zone_query != "All Zones":
        properties = properties.filter(zone_type__iexact=zone_query)

    if possession_query and possession_query != "All Status":
        properties = properties.filter(possession_status__iexact=possession_query)

    if listed_by_query and listed_by_query != "All Roles":
        properties = properties.filter(uploaded_by_role__iexact=listed_by_query)

    # Budget Range Lookup Filter
    if budget_query and budget_query != "All Budgets":
        if budget_query == "under_25k":
            properties = properties.filter(expected_rent__lt=25000)
        elif budget_query == "25k_1L":
            properties = properties.filter(expected_rent__gte=25000, expected_rent__lte=100000)
        elif budget_query == "1L_5L":
            properties = properties.filter(expected_rent__gte=100000, expected_rent__lte=500000)
        elif budget_query == "above_5L":
            properties = properties.filter(expected_rent__gt=500000)

    # Created At Date Filter Ranges
    if from_date_str:
        f_date = parse_date(from_date_str)
        if f_date:
            properties = properties.filter(created_at__date__gte=f_date)

    if to_date_str:
        t_date = parse_date(to_date_str)
        if t_date:
            properties = properties.filter(created_at__date__lte=t_date)

    # Order parameters sorting to top view
    properties = properties.order_by('-id')

    # ═══════════════════════════════════════
    # DYNAMIC SEARCH DROPDOWN POPULATORS
    # ═══════════════════════════════════════
    unfiltered_base = CommercialRentalProperty.objects.filter(is_deleted=False)
    
    unique_property_types = unfiltered_base.values_list('property_type', flat=True).distinct()
    unique_cities = unfiltered_base.values_list('city', flat=True).distinct()
    unique_zones = unfiltered_base.exclude(zone_type__isnull=True).exclude(zone_type='').values_list('zone_type', flat=True).distinct()
    unique_possession = unfiltered_base.values_list('possession_status', flat=True).distinct()
    unique_roles = unfiltered_base.exclude(uploaded_by_role__isnull=True).exclude(uploaded_by_role='').values_list('uploaded_by_role', flat=True).distinct()

    # ═══════════════════════════════════════
    # 📊 KPI DASHBOARD DATA CALCULATIONS
    # ═══════════════════════════════════════
    total_properties = unfiltered_base.count()
    active_listings = unfiltered_base.count() # Base live listings counter
    
    occupied_count = unfiltered_base.filter(possession_status__icontains="occupied").count()
    vacant_count = unfiltered_base.filter(possession_status__icontains="ready").count()

    occupancy_rate = round((occupied_count / total_properties * 100), 1) if total_properties > 0 else 0
    vacancy_rate = round((vacant_count / total_properties * 100), 1) if total_properties > 0 else 0

    # Financial Aggregations
    financials = unfiltered_base.aggregate(
        avg=Avg('expected_rent'), max_r=Max('expected_rent'), min_r=Min('expected_rent'),
        total_r=Sum('expected_rent'), deposit_total=Sum('security_deposit'), area_avg=Avg('builtup_area')
    )
    
    avg_rent = financials['avg'] or 0
    max_rent = financials['max_r'] or 0
    min_rent = financials['min_r'] or 0
    total_revenue = financials['total_r'] or 0
    total_security_deposit = financials['deposit_total'] or 0
    avg_area = financials['area_avg'] or 0

    # Business Quality Specs
    ready_to_move_count = vacant_count
    premium_properties_count = unfiltered_base.filter(expected_rent__gte=100000).count()
    affordable_properties_count = unfiltered_base.filter(expected_rent__lt=25000).count()
    
    short_lease_count = unfiltered_base.filter(lockin_period__lte=6).count()
    long_lease_count = unfiltered_base.filter(lockin_period__gt=11).count()
    
    with_images_count = unfiltered_base.filter(images__isnull=False).distinct().count()
    with_owner_count = unfiltered_base.exclude(owner_name__isnull=True).exclude(owner_name='').count()

    image_pct = round((with_images_count / total_properties * 100), 1) if total_properties > 0 else 0
    verified_pct = round((with_owner_count / total_properties * 100), 1) if total_properties > 0 else 0

    # Placeholders for Quick Stats Segment
    total_tenants = occupied_count
    collection_rate = 98
    pending_payments = unfiltered_base.filter(possession_status__icontains="dispute").count()
    maintenance_req = unfiltered_base.filter(maintenance_charges__gt=0).count()

    # ═══════════════════════════════════════
    # 📉 CHART AGGREGATIONS (JSON)
    # ═══════════════════════════════════════
    # 4a. Property Type Distribution
    pt_qs = unfiltered_base.values('property_type').annotate(count=Count('id')).order_by('-count')
    prop_type_labels_json = json.dumps([item['property_type'].replace('-', ' ').title() for item in pt_qs])
    prop_type_counts_json = json.dumps([item['count'] for item in pt_qs])

    # 4b. Monthly Distribution (Grouped by City for visual split)
    city_qs = unfiltered_base.values('city').annotate(revenue=Sum('expected_rent')).order_by('-revenue')[:6]
    monthly_labels_json = json.dumps([item['city'] for item in city_qs])
    monthly_revenue_json = json.dumps([float(item['revenue'] or 0) for item in city_qs])

    # 4c. Occupancy Array Data
    occupancy_json = json.dumps([occupied_count, vacant_count, total_properties - (occupied_count + vacant_count)])

    # 4d. Rent Ranges
    rent_buckets = [
        ('Under 25k', unfiltered_base.filter(expected_rent__lt=25000).count()),
        ('25k - 1L', unfiltered_base.filter(expected_rent__gte=25000, expected_rent__lte=100000).count()),
        ('1L - 5L', unfiltered_base.filter(expected_rent__gte=100000, expected_rent__lte=500000).count()),
        ('Above 5L', unfiltered_base.filter(expected_rent__gt=500000).count()),
    ]
    rent_range_labels_json = json.dumps([b[0] for b in rent_buckets])
    rent_range_counts_json = json.dumps([b[1] for b in rent_buckets])

    # Bulk Delete Selector Queries
    try:
        uploaded_files = unfiltered_base.exclude(upload_file_name__isnull=True).exclude(upload_file_name='').values_list('upload_file_name', flat=True).distinct()
    except Exception:
        uploaded_files = []

    # Pagination execution Engine
    paginator = Paginator(properties, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'admin_user/Reports/Rental/commercial_list.html', {
        'admin_obj': admin_obj,
        'page_obj': page_obj,
        
        # Filter Retention Tags State
        'search_query': search_query,
        'prop_type_query': prop_type_query,
        'city_query': city_query,
        'zone_query': zone_query,
        'possession_query': possession_query,
        'listed_by_query': listed_by_query,
        'budget_query': budget_query,
        'from_date': from_date_str,
        'to_date': to_date_str,
        'filtered_count': properties.count(),

        # Dropdown Lists Populators
        'unique_property_types': unique_property_types,
        'unique_cities': unique_cities,
        'unique_zones': unique_zones,
        'unique_possession': unique_possession,
        'unique_roles': unique_roles,
        'uploaded_files': uploaded_files,

        # Metrics & KPI Metrics Bindings
        'total_count': total_properties,
        'active_count': active_listings,
        'occupied_count': occupied_count,
        'vacant_count': vacant_count,
        'occupancy_rate': occupancy_rate,
        'vacancy_rate': vacancy_rate,
        'avg_rent': avg_rent,
        'max_rent': max_rent,
        'min_rent': min_rent,
        'total_revenue': total_revenue,
        'total_security_deposit': total_security_deposit,
        'avg_area': avg_area,
        'ready_to_move_count': ready_to_move_count,
        'premium_properties_count': premium_properties_count,
        'affordable_properties_count': affordable_properties_count,
        'short_lease_count': short_lease_count,
        'long_lease_count': long_lease_count,
        'with_images_count': with_images_count,
        'with_owner_count': with_owner_count,
        'image_pct': image_pct,
        'verified_pct': verified_pct,
        'total_tenants': total_tenants,
        'collection_rate': collection_rate,
        'pending_payments': pending_payments,
        'maintenance_req': maintenance_req,

        # Charts Context Variables Serialization
        'prop_type_labels_json': prop_type_labels_json,
        'prop_type_counts_json': prop_type_counts_json,
        'monthly_labels_json': monthly_labels_json,
        'monthly_revenue_json': monthly_revenue_json,
        'occupancy_json': occupancy_json,
        'rent_range_labels_json': rent_range_labels_json,
        'rent_range_counts_json': rent_range_counts_json,
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




def pg_list(request):
    session_id = request.session.get('Admin_id')
    if not session_id:
        return render(request, 'home_page/Adminlogin.html')

    # ── READ FILTER STRINGS ──
    search_query   = request.GET.get('search', '').strip()
    pg_for_filter  = request.GET.get('pg_for', '').strip()
    city_filter    = request.GET.get('city', '').strip()
    furnish_filter = request.GET.get('furnish', '').strip()
    meals_filter   = request.GET.get('meals', '').strip()
    sharing_filter = request.GET.get('sharing', '').strip()
    from_date      = request.GET.get('from_date', '').strip()
    to_date        = request.GET.get('to_date', '').strip()

    # ── FILTER SOFT DELETIONS ──
    all_props = PGColivingProperty.objects.filter(is_deleted=False)
    properties = all_props.order_by('-created_at')

    if search_query:
        properties = properties.filter(
            Q(property_title__icontains=search_query) | Q(city__icontains=search_query) |
            Q(locality__icontains=search_query) | Q(building_name__icontains=search_query) |
            Q(owner_name__icontains=search_query) | Q(contact_number__icontains=search_query) |
            Q(pg_property_id__icontains=search_query)
        )
    if pg_for_filter:
        properties = properties.filter(pg_for__iexact=pg_for_filter)
    if city_filter:
        properties = properties.filter(city__icontains=city_filter)
    if furnish_filter:
        properties = properties.filter(furnishing_type__iexact=furnish_filter)
    if meals_filter == 'Yes':
        properties = properties.filter(meals_available=True)
    elif meals_filter == 'No':
        properties = properties.filter(meals_available=False)
    if sharing_filter:
        properties = properties.filter(rooms__room_type__iexact=sharing_filter).distinct()
    if from_date:
        properties = properties.filter(created_at__date__gte=from_date)
    if to_date:
        properties = properties.filter(created_at__date__lte=to_date)

    # ── CSV DOWNLOAD ENGINE ──
    if request.GET.get('download') == 'csv':
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="pg_listings.csv"'
        writer = csv.writer(response)
        writer.writerow(['Property ID', 'Title', 'City', 'Locality', 'Building', 'Beds', 'PG For', 'Furnishing', 'Meals', 'Owner', 'Contact', 'Created At'])
        for p in properties:
            writer.writerow([p.pg_property_id, p.property_title, p.city, p.locality, p.building_name or '', p.total_beds, p.pg_for, p.furnishing_type, p.meals_available, p.owner_name, p.contact_number, p.created_at.strftime('%Y-%m-%d')])
        return response

    # ── PAGINATION SYSTEM ──
    paginator = Paginator(properties, 10)
    page_obj = paginator.get_page(request.GET.get('page', 1))

    # ── SUMMARY CARD KPI AGGREGATIONS ──
    total_count = properties.count()
    boys_count = properties.filter(pg_for__iexact='Boys').count()
    girls_count = properties.filter(pg_for__iexact='Girls').count()
    coliving_count = properties.filter(pg_for__iexact='Co-living').count()
    total_beds = properties.aggregate(t=Sum('total_beds'))['t'] or 0
    city_count = properties.values('city').distinct().count()

    boys_pct = round((boys_count / total_count * 100), 1) if total_count else 0
    girls_pct = round((girls_count / total_count * 100), 1) if total_count else 0
    coliving_pct = round((coliving_count / total_count * 100), 1) if total_count else 0

    # Financial operations aggregations using PGRoomDetail relational inner joins
    rent_stats = PGRoomDetail.objects.filter(property__in=properties).aggregate(avg_rent=Avg('room_rent'), max_rent=Max('room_rent'), min_rent=Min('room_rent'), avg_dep=Avg('room_deposit'), tot_rev=Sum('room_rent'), tot_dep=Sum('room_deposit'))
    
    # Extra Dashboard count maps
    meals_available_count = properties.filter(meals_available=True).count()
    meals_pct = round((meals_available_count / total_count * 100), 1) if total_count else 0
    furnished_count = properties.filter(furnishing_type__icontains='Fully').count()
    furnished_pct = round((furnished_count / total_count * 100), 1) if total_count else 0
    single_room_count = properties.filter(rooms__room_type__iexact='single').distinct().count()
    shared_room_count = properties.filter(rooms__room_type__in=['double', 'triple', 'quad']).distinct().count()
    anytime_entry = properties.filter(any_time_allowed=True).count()
    visitors_allowed = properties.filter(visitors_allowed=True).count()
    premium_pg_count = properties.filter(rooms__room_rent__gte=10000).distinct().count()
    budget_pg_count = properties.filter(rooms__room_rent__lt=5000).distinct().count()
    with_owner_count = properties.exclude(owner_name='').count()
    try: with_images_count = properties.filter(images__isnull=False).distinct().count()
    except Exception: with_images_count = 0

    # ── CHARTS STRUCTURAL JSON OBJECTS ──
    pg_for_qs = properties.values('pg_for').annotate(c=Count('pg_property_id')).order_by('-c')
    pg_for_labels = json.dumps([i['pg_for'] for i in pg_for_qs])
    pg_for_data = json.dumps([i['c'] for i in pg_for_qs])

    rent_buckets = [('Under ₹3k', 0, 3000), ('₹3k–5k', 3000, 5000), ('₹5k–8k', 5000, 8000), ('₹8k–12k', 8000, 12000), ('Above ₹12k', 12000, 999999)]
    rent_range_labels = json.dumps([b[0] for b in rent_buckets])
    rent_range_data = json.dumps([properties.filter(rooms__room_rent__gte=lo, rooms__room_rent__lt=hi).distinct().count() for _, lo, hi in rent_buckets])

    furnish_qs = properties.values('furnishing_type').annotate(c=Count('pg_property_id')).order_by('-c')
    furnishing_labels = json.dumps([i['furnishing_type'] for i in furnish_qs])
    furnishing_data = json.dumps([i['c'] for i in furnish_qs])

    city_qs = properties.values('city').annotate(c=Count('pg_property_id')).order_by('-c')[:5]
    city_labels = json.dumps([i['city'] for i in city_qs])
    city_data = json.dumps([i['c'] for i in city_qs])
    
    cities = all_props.values_list('city', flat=True).distinct().order_by('city')

    return render(request, 'admin_user/Reports/Rental/pg_list.html', {
        'page_obj': page_obj, 'search_query': search_query, 'pg_for_filter': pg_for_filter,
        'city_filter': city_filter, 'furnish_filter': furnish_filter, 'meals_filter': meals_filter,
        'sharing_filter': sharing_filter, 'from_date': from_date, 'to_date': to_date, 'cities': cities,
        'total_count': total_count, 'city_count': city_count, 'boys_count': boys_count, 'girls_count': girls_count,
        'coliving_count': coliving_count, 'total_beds': total_beds, 'boys_pct': boys_pct, 'girls_pct': girls_pct,
        'coliving_pct': coliving_pct, 'avg_rent': rent_stats['avg_rent'] or 0, 'max_rent': rent_stats['max_rent'] or 0,
        'min_rent': rent_stats['min_rent'] or 0, 'total_revenue': rent_stats['tot_rev'] or 0, 'total_deposit': rent_stats['tot_dep'] or 0,
        'avg_deposit': rent_stats['avg_dep'] or 0, 'meals_available_count': meals_available_count, 'meals_pct': meals_pct,
        'furnished_count': furnished_count, 'furnished_pct': furnished_pct, 'single_room_count': single_room_count,
        'shared_room_count': shared_room_count, 'non_veg_allowed': meals_available_count, 'with_images_count': with_images_count,
        'anytime_entry': anytime_entry, 'visitors_allowed': visitors_allowed, 'premium_pg_count': premium_pg_count,
        'budget_pg_count': budget_pg_count, 'with_owner_count': with_owner_count,
        'pg_for_labels': pg_for_labels, 'pg_for_data': pg_for_data, 'rent_range_labels': rent_range_labels,
        'rent_range_data': rent_range_data, 'furnishing_labels': furnishing_labels, 'furnishing_data': furnishing_data,
        'city_labels': city_labels, 'city_data': city_data,
    })




@csrf_exempt
def add_pg(request):
    if request.method != "POST":
        return JsonResponse({
            "status": "error",
            "message": "Invalid Request"
        })

    try:

        def get_list(name):
            return ",".join(request.POST.getlist(name))

        images = request.FILES.getlist("property_images[]")

        if len(images) < 3 or len(images) > 10:
            return JsonResponse({
                "status": "error",
                "message": "Upload minimum 3 and maximum 10 images"
            })

        with transaction.atomic():

            pg = PGColivingProperty.objects.create(

                # BASIC INFO
                property_title=request.POST.get("property_title"),  # FIXED
                city=request.POST.get("city"),
                building_name=request.POST.get("building_name"),
                locality=request.POST.get("locality"),
                property_address=request.POST.get("property_address"),

                total_beds=int(request.POST.get("total_beds") or 0),

                pg_for=request.POST.get("pg_for"),
                furnishing_type=request.POST.get("furnishing_type"),
                sharing_type=request.POST.get("sharing_type"),
                best_suited_for=request.POST.get("best_suited_for"),

                amenities=get_list("amenities[]"),
                nearby_facilities=get_list("facilities[]"),

                # MEALS
                meals_available=bool(request.POST.get("meals_available")),
                meal_offerings=request.POST.get("meal_offerings"),
                meal_speciality=request.POST.get("meal_speciality"),

                # RULES
                notice_period=request.POST.get("notice_period") or None,
                lockin_period=request.POST.get("lockin_period") or None,
                minimum_stay=int(request.POST.get("minimum_stay") or 1),
                available_from=request.POST.get("available_from"),

                property_managed_by=request.POST.get("property_managed_by"),

                manager_stays=bool(request.POST.get("manager_stays")),

                opposite_sex_allowed=bool(request.POST.get("opposite_sex_allowed")),
                any_time_allowed=bool(request.POST.get("any_time_allowed")),
                visitors_allowed=bool(request.POST.get("visitors_allowed")),
                guardian_allowed=bool(request.POST.get("guardian_allowed")),
                drinking_allowed=bool(request.POST.get("drinking_allowed")),
                smoking_allowed=bool(request.POST.get("smoking_allowed")),

                property_description=request.POST.get("property_description"),

                # MEDIA
                video=request.FILES.get("video"),

                # CONTACT
                owner_name=request.POST.get("owner_name"),
                contact_number=request.POST.get("contact_number"),
                email=request.POST.get("email"),
                alternate_contact=request.POST.get("alternate_contact"),

                # UPLOAD INFO
                upload_file_name=request.POST.get("uploaded_file_name"),
                uploaded_by_name=request.POST.get("uploaded_by_name"),
                uploaded_by_email=request.POST.get("uploaded_by_email"),
                uploaded_by_contact=request.POST.get("uploaded_by_contact"),
                uploaded_by_role=request.POST.get("uploaded_by_role"),
            )

            # ROOMS
            room_types = request.POST.getlist('room_type[]')
            room_beds = request.POST.getlist('room_beds[]')
            room_rents = request.POST.getlist('room_rent[]')
            room_deposits = request.POST.getlist('room_deposit[]')
            room_brokerages = request.POST.getlist('room_brokerage[]')
            room_brokerage_percents = request.POST.getlist('room_brokerage_percent[]')
            room_manual_brokerages = request.POST.getlist('room_manual_brokerage[]')

            for idx in range(len(room_types)):

                facilities_key = f'room_facilities_{idx + 1}[]'
                room_facilities = ",".join(
                    request.POST.getlist(facilities_key)
                )

                PGRoomDetail.objects.create(
                    property=pg,
                    room_type=room_types[idx],
                    room_beds=int(room_beds[idx] or 1),
                    room_rent=room_rents[idx] or 0,
                    room_deposit=room_deposits[idx] or 0,
                    room_brokerage=room_brokerages[idx] if idx < len(room_brokerages) else '',
                    room_brokerage_percent=room_brokerage_percents[idx] if idx < len(room_brokerage_percents) else '',
                    room_manual_brokerage=room_manual_brokerages[idx] if idx < len(room_manual_brokerages) else '',
                    room_facilities=room_facilities
                )

            # IMAGES
            for img in images:
                PGPropertyImage.objects.create(
                    property=pg,
                    image=img
                )

        return JsonResponse({
            "status": "success",
            "message": "PG Added Successfully"
        })

    except Exception as e:
        print("PG SAVE ERROR:", str(e))
        import traceback
        traceback.print_exc()

        return JsonResponse({
            "status": "error",
            "message": str(e)
        })





<<<<<<< HEAD
=======
    admin_obj = Admin_Login.objects.get(id=session_id)

    search = request.GET.get('search', '')
    qs = PGColivingProperty.objects.all().order_by('-id')
>>>>>>> d0f149b2c74d1fc5cd4a07f46e5105a392471ff5


<<<<<<< HEAD
=======
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
        'admin_obj':admin_obj,
        
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
>>>>>>> d0f149b2c74d1fc5cd4a07f46e5105a392471ff5


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






# ─── Converters ───────────────────────────────────────────────────────────────
def _bool(v):
    if isinstance(v, bool): return v
    return str(v).strip().lower() in ("true", "yes", "1")

def _int(v):
    try: return int(float(str(v).strip()))
    except: return None

def _str(v):
    return str(v).strip() if v not in (None, "") else ""

def _date(v):
    if v is None: return None
    from datetime import date, datetime
    if isinstance(v, (date, datetime)): return v
    from django.utils.dateparse import parse_date
    return parse_date(str(v).strip())


# ─── Column map: keys EXACTLY match lowercased row-2 headers in template ──────
#     (excel_header_lowercase,   model_field,            converter,  is_room_col)
COLUMN_MAP = [
    ("city *",                                                              "city",                 _str,  False),
    ("building / project name",                                             "building_name",        _str,  False),
    ("locality *",                                                          "locality",             _str,  False),
    ("pg name *",                                                           "property_title",       _str,  False),  # auto-gen if blank, but we still pass it
    ("property address *",                                                  "property_address",     _str,  False),
    ("total beds *",                                                        "total_beds",           _int,  False),
    ("pg for * (boys/girls/both)",                                          "pg_for",               _str,  False),
    ("furnishing type * (fully-furnished/semi-furnished/unfurnished)",      "furnishing_type",      _str,  False),
    ("best suited for (students/working professionals/any)",                "best_suited_for",      _str,  False),
    ("property managed by (owner/caretaker)",                               "property_managed_by",  _str,  False),
    ("manager stays? (true/false)",                                         "manager_stays",        _bool, False),
    ("notice period (days)",                                                "notice_period",        _int,  False),
    ("lock-in period (days)",                                               "lockin_period",        _int,  False),
    ("minimum stay (months) *",                                             "minimum_stay",         _int,  False),
    ("available from * (yyyy-mm-dd)",                                       "available_from",       _date, False),
    # room col — value is the pipe-string; handled separately
    ("single|1|8000|16000|yes|1%||,double|2|6000|12000|no||",              "__room_details__",     _str,  True),
    ("meals available? (true/false)",                                       "meals_available",      _bool, False),
    ("meal offerings (breakfast,lunch,dinner)",                             "meal_offerings",       _str,  False),
    ("meal speciality (veg/non-veg/both)",                                  "meal_speciality",      _str,  False),
    # non_veg_allowed not in model — skip
    ("opposite sex allowed? (true/false)",                                  "opposite_sex_allowed", _bool, False),
    ("any time entry allowed? (true/false)",                                "any_time_allowed",     _bool, False),
    ("visitors allowed? (true/false)",                                      "visitors_allowed",     _bool, False),
    ("guardian allowed? (true/false)",                                      "guardian_allowed",     _bool, False),
    ("drinking allowed? (true/false)",                                      "drinking_allowed",     _bool, False),
    ("smoking allowed? (true/false)",                                       "smoking_allowed",      _bool, False),
    ("amenities (wifi,cctv,geyser,...)",                                    "amenities",            _str,  False),
    ("nearby facilities (college,market,...)",                               "nearby_facilities",    _str,  False),
    ("property description",                                                "property_description", _str,  False),
    ("owner name *",                                                        "owner_name",           _str,  False),
    ("contact number *",                                                    "contact_number",       _str,  False),
    ("email *",                                                             "email",                _str,  False),
    ("alternate contact",                                                   "alternate_contact",    _str,  False),
]

# Required fields validated on model data dict
REQUIRED_FIELDS = [
    "city", "locality", "property_address",
    "total_beds", "pg_for", "furnishing_type",
    "minimum_stay", "available_from",
    "owner_name", "contact_number", "email",
]

# Minimum required headers (lowercased) that MUST appear in the uploaded file
REQUIRED_HEADERS = {
    "city *",
    "locality *",
    "property address *",
    "total beds *",
    "pg for * (boys/girls/both)",
    "furnishing type * (fully-furnished/semi-furnished/unfurnished)",
    "minimum stay (months) *",
    "available from * (yyyy-mm-dd)",
    "owner name *",
    "contact number *",
    "email *",
}


# ─── Room detail parser ───────────────────────────────────────────────────────
def _parse_room_details(raw):
    rooms = []
    if not raw:
        return rooms
    for chunk in str(raw).split(","):
        parts = [p.strip() for p in chunk.split("|")]
        if len(parts) < 4 or not parts[0]:
            continue
        def _s(i, d=""): return parts[i].strip() if i < len(parts) else d
        try:
            rooms.append({
                "room_type":              _s(0) or "single",
                "room_beds":              _int(_s(1, "1")) or 1,
                "room_rent":              float(_s(2, "0") or 0),
                "room_deposit":           float(_s(3, "0") or 0),
                "room_brokerage":         _s(4, "No"),
                "room_brokerage_percent": _s(5, ""),
                "room_manual_brokerage":  _s(6, ""),
            })
        except Exception:
            continue
    return rooms


# ─── IMPORT VIEW ──────────────────────────────────────────────────────────────
@csrf_exempt
@require_POST
def import_pg_excel(request):

    if not request.session.get('Admin_id'):
        return JsonResponse({'status': 'error', 'message': 'Unauthorized'}, status=401)

    file = request.FILES.get('file')
    if not file:
        return JsonResponse({'status': 'error', 'message': 'No file uploaded'}, status=400)

    file_name = file.name.strip()

    try:
        wb = openpyxl.load_workbook(io.BytesIO(file.read()), data_only=True)
        ws = wb.active
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': f'Invalid Excel file: {e}'}, status=400)

    all_rows = list(ws.iter_rows(values_only=True))
    if len(all_rows) < 2:
        return JsonResponse({'status': 'error', 'message': 'File is empty or missing headers.'}, status=400)

    # Detect header row: row 1 = section titles (merged), row 2 = real col headers
    # If row 0 cells are all None except merged starts → row 1 is section row, row 1 (index 1) is headers
    row0 = [str(c).strip().lower() if c else "" for c in all_rows[0]]
    row1 = [str(c).strip().lower() if c else "" for c in all_rows[1]]

    # If row0 contains "step" clues → headers are in row1
    if any("step" in v or "📋" in v for v in row0 if v):
        header_row = row1
        data_start  = 2   # data begins at index 2
    else:
        header_row = row0
        data_start  = 1

    col_index = {h: i for i, h in enumerate(header_row) if h}

    # ── Validate template format ──────────────────────────────────────────────
    missing_headers = REQUIRED_HEADERS - set(col_index.keys())
    if missing_headers:
        return JsonResponse({
            'status': 'error',
            'message': (
                f'Wrong template format — missing columns: {", ".join(sorted(missing_headers))}. '
                f'Please download the latest template.'
            )
        }, status=400)

    # ── Find room_details column index (its header is the sample pipe-string) ─
    room_col_idx = None
    for h, idx in col_index.items():
        if "|" in h and ("single" in h or "double" in h):
            room_col_idx = idx
            break

    # ── Same-file check ───────────────────────────────────────────────────────
    file_already_exists = PGColivingProperty.objects.filter(
        upload_file_name=file_name, is_deleted=False
    ).exists()

    uploader_name = request.session.get(
    "Admin_name",
    request.session.get("User_name", "Admin")
    )

    uploader_email = request.session.get(
    "Admin_email",
    request.session.get("User_email", "")
    )

    uploader_contact = request.session.get(
    "Admin_contact",
    request.session.get("User_contact", "")
    )

    uploader_role = (
    "Admin"
    if request.session.get("Admin_id")
    else "User"
    )

    # Build lookup from COLUMN_MAP: excel_key → (model_field, converter)
    col_lookup = {excel_key: (field, conv) for excel_key, field, conv, _ in COLUMN_MAP}

    imported          = 0
    skipped           = 0
    errors            = []
    same_file_skipped = 0

    model_fields = {f.name for f in PGColivingProperty._meta.get_fields() if hasattr(f, 'column')}

    for row_num, row in enumerate(all_rows[data_start:], start=data_start + 1):

        if all(c is None or str(c).strip() == "" for c in row):
            continue

        data         = {}
        room_raw     = ""

        # Map each column
        for excel_key, (model_field, conv) in col_lookup.items():
            if model_field == "__room_details__":
                continue
            idx = col_index.get(excel_key)
            if idx is not None and idx < len(row):
                try:
                    val = conv(row[idx])
                    if model_field in model_fields:
                        data[model_field] = val
                except Exception:
                    data[model_field] = None

        # property_title: leave blank → model.save() auto-generates it
        # If user typed a PG name, keep it; otherwise let save() build it
        if not data.get("property_title"):
            data.pop("property_title", None)   # let model handle it

        # Room details
        if room_col_idx is not None and room_col_idx < len(row):
            room_raw = str(row[room_col_idx] or "").strip()

        # ── Required field check ──────────────────────────────────────────────
        missing = [f for f in REQUIRED_FIELDS if not data.get(f)]
        if missing:
            skipped += 1
            errors.append(f"Row {row_num}: Missing → {', '.join(missing)}")
            continue

        # ── Uploader ──────────────────────────────────────────────────────────
        # Ignore uploader values from Excel
        data.pop("uploaded_by_name", None)
        data.pop("uploaded_by_email", None)
        data.pop("uploaded_by_contact", None)
        data.pop("uploaded_by_role", None)

# Save actual logged-in user details
        data["uploaded_by_name"] = uploader_name
        data["uploaded_by_email"] = uploader_email
        data["uploaded_by_contact"] = uploader_contact
        data["uploaded_by_role"] = uploader_role
        data["upload_file_name"] = file_name

        # ── Duplicate: same file, same core fields → skip ─────────────────────
        if file_already_exists:
            dupe = PGColivingProperty.objects.filter(
                upload_file_name=file_name,
                contact_number=data.get("contact_number", ""),
                email=data.get("email", ""),
                property_address=data.get("property_address", ""),
                is_deleted=False,
            ).exists()
            if dupe:
                same_file_skipped += 1
                skipped += 1
                continue

        # ── Duplicate: different file, same property ──────────────────────────
        dupe_diff_file = PGColivingProperty.objects.filter(
            contact_number=data.get("contact_number", ""),
            email=data.get("email", ""),
            property_address=data.get("property_address", ""),
            locality=data.get("locality", ""),
            is_deleted=False,
        ).exclude(upload_file_name=file_name).exists()

        if dupe_diff_file:
            skipped += 1
            errors.append(f"Row {row_num}: Duplicate — same property already exists from a different file.")
            continue

        # ── Strip unknown keys ────────────────────────────────────────────────
        data = {k: v for k, v in data.items() if k in model_fields}

        # ── Save ──────────────────────────────────────────────────────────────
        try:
            pg = PGColivingProperty.objects.create(**data)
            for room in _parse_room_details(room_raw):
                PGRoomDetail.objects.create(property=pg, **room)
            imported += 1
        except Exception as e:
            skipped += 1
            errors.append(f"Row {row_num}: {e}")

    same_file_flag = same_file_skipped > 0 and imported == 0

    return JsonResponse({
        "status":          "success",
        "imported":        imported,
        "skipped":         skipped,
        "errors":          errors[:10],
        "same_file":       same_file_flag,
        "same_file_count": same_file_skipped,
        "message":         f"{imported} imported, {skipped} skipped",
    })


# ─── DOWNLOAD TEMPLATE VIEW ───────────────────────────────────────────────────
def download_pg_template(request):

    if not request.session.get('Admin_id'):
        from django.shortcuts import render
        return render(request, 'home_page/Adminlogin.html')

    from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
    from openpyxl.utils import get_column_letter

    wb  = openpyxl.Workbook()
    ws  = wb.active
    ws.title = "PG Import"

    sections = [
        ("📋 Step 1: Basic Info", [
            ("city",               "City *",                                                              True),
            ("building_name",      "Building / Project Name",                                             False),
            ("locality",           "Locality *",                                                          True),
            ("property_title",     "PG Name *",                                                          True),
            ("property_address",   "Property Address *",                                                  True),
            ("total_beds",         "Total Beds *",                                                        True),
            ("pg_for",             "PG For * (boys/girls/both)",                                          True),
            ("furnishing_type",    "Furnishing Type * (fully-furnished/semi-furnished/unfurnished)",       True),
            ("best_suited_for",    "Best Suited For (students/working professionals/any)",                 False),
            ("property_managed_by","Property Managed By (owner/caretaker)",                               False),
            ("manager_stays",      "Manager Stays? (True/False)",                                         False),
            ("notice_period",      "Notice Period (Days)",                                                False),
            ("lockin_period",      "Lock-in Period (Days)",                                               False),
            ("minimum_stay",       "Minimum Stay (Months) *",                                             True),
            ("available_from",     "Available From * (YYYY-MM-DD)",                                       True),
        ]),
        ("📋 Step 2: Room Details  ▶  Format: type|beds|rent|deposit|brokerage(Yes/No)|brokerage%|manual_brokerage  — separate room types with comma", [
            ("room_details", "single|1|8000|16000|Yes|1%||,double|2|6000|12000|No||", False),
        ]),
        ("📋 Step 3: Meals", [
            ("meals_available", "Meals Available? (True/False)",           False),
            ("meal_offerings",  "Meal Offerings (Breakfast,Lunch,Dinner)", False),
            ("meal_speciality", "Meal Speciality (Veg/Non-Veg/Both)",      False),
        ]),
        ("📋 Step 4: Rules", [
            ("opposite_sex_allowed", "Opposite Sex Allowed? (True/False)",   False),
            ("any_time_allowed",     "Any Time Entry Allowed? (True/False)", False),
            ("visitors_allowed",     "Visitors Allowed? (True/False)",       False),
            ("guardian_allowed",     "Guardian Allowed? (True/False)",       False),
            ("drinking_allowed",     "Drinking Allowed? (True/False)",       False),
            ("smoking_allowed",      "Smoking Allowed? (True/False)",        False),
        ]),
        ("📋 Step 5: Amenities & Description", [
            ("amenities",            "Amenities (WiFi,CCTV,Geyser,...)",        False),
            ("nearby_facilities",    "Nearby Facilities (College,Market,...)",   False),
            ("property_description", "Property Description",                    False),
        ]),
        ("📋 Step 6: Contact Info", [
            ("owner_name",       "Owner Name *",      True),
            ("contact_number",   "Contact Number *",  True),
            ("email",            "Email *",           True),
            ("alternate_contact","Alternate Contact", False),
        ]),
    ]

    SECTION_FILL = PatternFill("solid", start_color="1F4E79")
    SECTION_FONT = Font(bold=True, color="FFFFFF", size=10)
    REQ_FILL     = PatternFill("solid", start_color="FFD7D7")
    OPT_FILL     = PatternFill("solid", start_color="DDEBF7")
    SAMPLE_FILL  = PatternFill("solid", start_color="F2F2F2")
    HDR_FONT     = Font(bold=True, size=9)
    AUTOGEN_FILL = PatternFill("solid", start_color="FFF3CD")   # yellow = auto-generated
    CENTER       = Alignment(horizontal="center", vertical="center", wrap_text=True)
    LEFT         = Alignment(horizontal="left",   vertical="center", wrap_text=True)
    thin         = Side(style="thin", color="BBBBBB")
    BORDER       = Border(left=thin, right=thin, top=thin, bottom=thin)

    all_cols      = []
    section_spans = []
    for sec_label, fields in sections:
        sc = len(all_cols) + 1
        for fkey, fheader, req in fields:
            all_cols.append((fkey, fheader, req))
        section_spans.append((sec_label, sc, len(all_cols)))

    # Row 1 — section headers
    for sec_label, sc, ec in section_spans:
        ws.merge_cells(start_row=1, start_column=sc, end_row=1, end_column=ec)
        c = ws.cell(row=1, column=sc, value=sec_label)
        c.fill = SECTION_FILL; c.font = SECTION_FONT; c.alignment = CENTER

    # Row 2 — column headers
    for ci, (fkey, fheader, req) in enumerate(all_cols, 1):
        c = ws.cell(row=2, column=ci, value=fheader)
        if fkey == "property_title":
            c.fill = AUTOGEN_FILL   # yellow = auto-generated if blank
        else:
            c.fill = REQ_FILL if req else OPT_FILL
        c.font = HDR_FONT; c.alignment = CENTER; c.border = BORDER

    # Row 3 — sample data  (property_title intentionally blank → auto-gen)
    samples = {
        "city": "Nagpur",
        "building_name": "ABC Building",
        "locality": "Dharampeth",
        "property_title": "",    # ← blank: model.save() will auto-generate
        "property_address": "123, Near Metro, Dharampeth, Nagpur",
        "total_beds": 50,
        "pg_for": "boys",
        "furnishing_type": "fully-furnished",
        "best_suited_for": "students",
        "property_managed_by": "owner",
        "manager_stays": "True",
        "notice_period": 30,
        "lockin_period": 90,
        "minimum_stay": 3,
        "available_from": "2026-07-01",
        "room_details": "single|1|8000|16000|Yes|1%||,double|2|6000|12000|No||",
        "meals_available": "True",
        "meal_offerings": "Breakfast,Dinner",
        "meal_speciality": "Veg",
        "opposite_sex_allowed": "False",
        "any_time_allowed": "True",
        "visitors_allowed": "True",
        "guardian_allowed": "True",
        "drinking_allowed": "False",
        "smoking_allowed": "False",
        "amenities": "WiFi,CCTV,Geyser",
        "nearby_facilities": "College,Market,Hospital",
        "property_description": "Well-managed PG with modern amenities.",
        "owner_name": "Mr. Sharma",
        "contact_number": "9876543210",
        "email": "sharma@email.com",
        "alternate_contact": "9999999999",
    }
    for ci, (fkey, fheader, _) in enumerate(all_cols, 1):
        val = samples.get(fkey, "")
        c = ws.cell(row=3, column=ci, value=val)
        if fkey == "property_title":
            c.value = ""    # keep blank to show auto-gen behaviour
            c.font = Font(italic=True, color="999999", size=9)
            # add comment hint
            from openpyxl.comments import Comment
            comment = Comment("Leave blank — auto-generated as:\n'Premium boys PG at ABC Building Dharampeth'", "System")
            c.comment = comment
        c.fill = SAMPLE_FILL; c.alignment = LEFT; c.border = BORDER

    # Row 4 — legend
    ws.merge_cells(start_row=4, start_column=1, end_row=4, end_column=len(all_cols))
    lc = ws.cell(row=4, column=1,
        value="🔴 Red = Required  |  🔵 Blue = Optional  |  🟡 Yellow = Auto-generated (leave blank)  |  Row 3 = SAMPLE — delete before uploading  |  Do NOT rename headers")
    lc.font = Font(italic=True, color="555555", size=9)
    lc.alignment = LEFT

    for ci, (fkey, fheader, _) in enumerate(all_cols, 1):
        cl = get_column_letter(ci)
        if fkey == "room_details":                   ws.column_dimensions[cl].width = 65
        elif fkey in ("property_address", "property_description"): ws.column_dimensions[cl].width = 32
        else: ws.column_dimensions[cl].width = max(18, len(fheader) * 0.85)

    ws.row_dimensions[1].height = 24
    ws.row_dimensions[2].height = 48
    ws.row_dimensions[3].height = 20
    ws.freeze_panes = "A3"

    buf = io.BytesIO()
    wb.save(buf)
    buf.seek(0)

    response = HttpResponse(
        buf.read(),
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = 'attachment; filename="pg_import_template.xlsx"'
    return response








def pg_edit_page(request, property_id):
    """Renders the multi-step edit interface form filled with existing asset data."""
    pg = get_object_or_404(PGColivingProperty, pg_property_id=property_id)
    
    # Static data configurations matching your form expectations
    ameneties_obj = [
        {"amenties_name": "Wi-Fi High Speed", "amenties_icon": "fas fa-wifi"},
        {"amenties_name": "Power Backup", "amenties_icon": "fas fa-plug"},
        {"amenties_name": "RO Water Filtration", "amenties_icon": "fas fa-tint"},
        {"amenties_name": "Housekeeping Service", "amenties_icon": "fas fa-broom"},
        {"amenties_name": "CCTV Surveillance", "amenties_icon": "fas fa-shield-alt"},
        {"amenties_name": "Washing Machine", "amenties_icon": "fas fa-tshirt"}
    ]
    facilities_obj = [
        {"facilities_name": "Metro Station", "facilities_icon": "fas fa-subway"},
        {"facilities_name": "Food Court / Market", "facilities_icon": "fas fa-shopping-basket"},
        {"facilities_name": "Hospital / Clinic", "facilities_icon": "fas fa-hospital"},
        {"facilities_name": "IT Hub / Business Park", "facilities_icon": "fas fa-building"}
    ]
    
    # Split comma-separated database string metrics into lists for template checkboxes
    selected_amenities = pg.amenities.split(",") if pg.amenities else []
    selected_facilities = pg.nearby_facilities.split(",") if pg.nearby_facilities else []

    return render(request, "admin_user/Reports/Rental/pg_edit.html", {
        "pg": pg,
        "ameneties_obj": ameneties_obj,
        "facilities_obj": facilities_obj,
        "selected_amenities": selected_amenities,
        "selected_facilities": selected_facilities,
    })


@csrf_exempt
def pg_edit(request, property_id):
    """Processes the asynchronous multi-part POST payload to update data records."""
    if request.method != "POST":
        return JsonResponse({
            "status": "error", 
            "message": f"Invalid Request Protocol: Expected POST, received {request.method}."
        })

    try:
        pg = get_object_or_404(PGColivingProperty, pg_property_id=property_id)

        def get_list(name):
            return ",".join(request.POST.getlist(name))

        with transaction.atomic():
            # ✅ 1. UPDATE CORE RECORD PROPERTIES
            pg.property_title = request.POST.get("property_title")
            pg.city = request.POST.get("city")
            pg.building_name = request.POST.get("building_name")
            pg.locality = request.POST.get("locality")
            pg.property_address = request.POST.get("property_address")
            pg.total_beds = int(request.POST.get("total_beds") or 0)
            pg.pg_for = request.POST.get("pg_for")
            pg.furnishing_type = request.POST.get("furnishing_type")
            pg.sharing_type = request.POST.get("sharing_type")
            pg.best_suited_for = request.POST.get("best_suited_for")

            pg.amenities = get_list("amenities[]")
            pg.nearby_facilities = get_list("facilities[]")

            # MEALS HANDLERS
            pg.meals_available = True if request.POST.get("meals_available") in ["on", "true"] else False
            pg.meal_offerings = request.POST.get("meal_offerings") if pg.meals_available else None
            pg.meal_speciality = request.POST.get("meal_speciality") if pg.meals_available else None

            # RULES & POLICIES
            pg.notice_period = request.POST.get("notice_period") or None
            pg.lockin_period = request.POST.get("lockin_period") or None
            pg.minimum_stay = int(request.POST.get("minimum_stay") or 1)
            pg.available_from = request.POST.get("available_from")
            pg.property_managed_by = request.POST.get("property_managed_by")
            pg.manager_stays = True if request.POST.get("manager_stays") == "true" else False
            
            # TOGGLE SWITCH PROTOCOLS
            pg.opposite_sex_allowed = 'opposite_sex_allowed' in request.POST
            pg.any_time_allowed = 'any_time_allowed' in request.POST
            pg.visitors_allowed = 'visitors_allowed' in request.POST
            pg.guardian_allowed = 'guardian_allowed' in request.POST
            pg.drinking_allowed = 'drinking_allowed' in request.POST
            pg.smoking_allowed = 'smoking_allowed' in request.POST
            
            pg.property_description = request.POST.get("property_description")

            # MEDIA TOUR FILE INTERACTION
            if request.FILES.get("video"):
                pg.video = request.FILES.get("video")

            # CONTACT STRINGS
            pg.owner_name = request.POST.get("owner_name")
            pg.contact_number = request.POST.get("contact_number")
            pg.email = request.POST.get("email")
            pg.alternate_contact = request.POST.get("alternate_contact")

            pg.save()

            # ✅ 2. ATOMIC RESET & FLUSH RELATIONAL CHILD variant lines (PGRoomDetail)
            pg.rooms.all().delete()

            room_types = request.POST.getlist('room_type[]')
            room_beds = request.POST.getlist('room_beds[]')
            room_rents = request.POST.getlist('room_rent[]')
            room_deposits = request.POST.getlist('room_deposit[]')
            room_brokerages = request.POST.getlist('room_brokerage[]')
            room_brokerage_percents = request.POST.getlist('room_brokerage_percent[]')
            room_manual_brokerages = request.POST.getlist('room_manual_brokerage[]')

            for idx in range(len(room_types)):
                facilities_key = f'room_facilities_{idx + 1}[]'
                room_facilities_str = ",".join(request.POST.getlist(facilities_key))

                PGRoomDetail.objects.create(
                    property=pg,
                    room_type=room_types[idx],
                    room_beds=int(room_beds[idx] or 1),
                    room_rent=room_rents[idx] or 0.00,
                    room_deposit=room_deposits[idx] or 0.00,
                    room_brokerage=room_brokerages[idx] if idx < len(room_brokerages) else '',
                    room_brokerage_percent=room_brokerage_percents[idx] if idx < len(room_brokerage_percents) else '',
                    room_manual_brokerage=room_manual_brokerages[idx] if idx < len(room_manual_brokerages) else '',
                    room_facilities=room_facilities_str
                )

            # ✅ 3. DYNAMIC IMAGE APPEND PIPELINE
            new_images = request.FILES.getlist("property_images[]")
            if new_images:
                current_total = pg.images.count()
                if current_total + len(new_images) > 10:
                    return JsonResponse({
                        "status": "error", 
                        "message": f"Gallery limits hit. Maximum limit is 10 images. You have {current_total} active images."
                    })
                for img in new_images:
                    PGPropertyImage.objects.create(property=pg, image=img)

        return JsonResponse({
            "status": "success", 
            "message": "PG Record Suite Modifications Deployed Successfully.",
            "redirect_url": "/Admin_App/pg_list/"  # Adjust this redirect target to match your dashboard page
        })

    except Exception as e:
        return JsonResponse({"status": "error", "message": f"System Interruption: {str(e)}"})





@require_POST
def pg_coliving_delete(request, pk):
    sid, _ = _get_admin(request)
    if not sid:
        return JsonResponse({'status': 'error', 'message': 'Unauthorized'}, status=401)

    try:
        deleter_name = _get_deleter_name(request)

        pg = get_object_or_404(PGColivingProperty, pk=pk)
        pg.is_deleted = True
        pg.deleted_at = timezone.now()
        pg.deleted_by = deleter_name # 👈 SAVE THE NAME HERE
        pg.save()
        
        return JsonResponse({'status': 'success', 'message': 'Moved to Recycle Bin successfully!'})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)})

@require_POST
def pg_restore(request, id):
    PGColivingProperty.objects.filter(id=id).update(is_deleted=False, deleted_at=None, deleted_by=None)
    return JsonResponse({'status': 'success', 'message': 'PG property restored!'})



@require_POST
def pg_hard_delete(request, id):
    PGColivingProperty.objects.filter(id=id).delete()
    return JsonResponse({'status': 'success', 'message': 'Permanently deleted!'})



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





# ── 1. MAIN LIST VIEW ──
def plot_resale_list(request):
    session_id = request.session.get('Admin_id')
    if not session_id:
        return render(request, 'home_page/Adminlogin.html')
        
    admin_obj = Admin_Login.objects.get(id=session_id)
    
    # 👈 1. Filter out deleted properties!
    base_qs = PlotSaleProperty.objects.filter(is_deleted=False)
    
    # Fetch properties newest first
    properties = PlotSaleProperty.objects.filter(is_deleted=False).order_by('-created_at')
    
    # Calculate stats
    total_properties = base_qs.count()
    active_listings = base_qs.filter(plot_price__gt=0).count()
    
    # 👈 2. Fetch unique uploaded file names for the Bulk Delete modal
    try:
        uploaded_files = base_qs.exclude(
            upload_file_name__isnull=True
        ).exclude(upload_file_name='').values_list('upload_file_name', flat=True).distinct()
    except Exception:
        uploaded_files = []
    
    context = {
        'admin_obj': admin_obj,
        'properties': properties,
        'total_properties': total_properties,
        'active_listings': active_listings,
        'uploaded_files': uploaded_files # 👈 Passed to template here
    }
    return render(request, 'admin_user/Reports/Resale/plot_list.html', context)


# ── 2. BULK DELETE VIEW (Soft Delete) ──
@require_POST
def plot_sale_bulk_delete(request):
    """Handles Advanced Bulk Deletions for Plot/Land Properties."""
    admin_id = request.session.get('Admin_id')
    user_id = request.session.get('User_id')
    
    if not admin_id and not user_id:
        return JsonResponse({'status': 'error', 'message': 'Unauthorized access.'})

    try:
        data = json.loads(request.body)
        delete_type = data.get('delete_type')
        deleter_name = _get_deleter_name(request) # Using the helper we made earlier
        
        properties = PlotSaleProperty.objects.filter(is_deleted=False)
        
        if delete_type == 'delete_all':
            count = properties.count()
            properties.update(is_deleted=True, deleted_at=timezone.now(), deleted_by=deleter_name)
            return JsonResponse({'status': 'success', 'message': f'Successfully moved ALL {count} plots to Recycle Bin.'})
            
        elif delete_type == 'current_page':
            page_ids = data.get('page_ids', [])
            target_props = properties.filter(id__in=page_ids)
            count = target_props.count()
            target_props.update(is_deleted=True, deleted_at=timezone.now(), deleted_by=deleter_name)
            return JsonResponse({'status': 'success', 'message': f'Successfully moved {count} plots from current page to Recycle Bin.'})
            
        elif delete_type == 'date_range':
            from_date = data.get('from_date')
            to_date = data.get('to_date')
            target_props = properties.filter(created_at__date__range=[from_date, to_date])
            count = target_props.count()
            target_props.update(is_deleted=True, deleted_at=timezone.now(), deleted_by=deleter_name)
            return JsonResponse({'status': 'success', 'message': f'Successfully moved {count} plots in date range to Recycle Bin.'})
            
        elif delete_type == 'latest_month':
            thirty_days_ago = timezone.now() - timedelta(days=30)
            target_props = properties.filter(created_at__gte=thirty_days_ago)
            count = target_props.count()
            target_props.update(is_deleted=True, deleted_at=timezone.now(), deleted_by=deleter_name)
            return JsonResponse({'status': 'success', 'message': f'Successfully moved {count} plots from the last 30 days to Recycle Bin.'})
            
        elif delete_type == 'old_data':
            six_months_ago = timezone.now() - timedelta(days=180)
            target_props = properties.filter(created_at__lt=six_months_ago)
            count = target_props.count()
            target_props.update(is_deleted=True, deleted_at=timezone.now(), deleted_by=deleter_name)
            return JsonResponse({'status': 'success', 'message': f'Successfully moved {count} older plots to Recycle Bin.'})
            
        elif delete_type == 'by_uploader':
            uploader = data.get('uploader_text', '')
            target_props = properties.filter(
                Q(uploaded_by_name__icontains=uploader) | 
                Q(uploaded_by_email__icontains=uploader) |
                Q(uploaded_by_role__icontains=uploader)
            )
            count = target_props.count()
            target_props.update(is_deleted=True, deleted_at=timezone.now(), deleted_by=deleter_name)
            return JsonResponse({'status': 'success', 'message': f'Successfully moved {count} plots uploaded by {uploader} to Recycle Bin.'})

        elif delete_type == 'by_file':
            file_name = data.get('file_name', '')
            target_props = properties.filter(upload_file_name=file_name) 
            count = target_props.count()
            if count == 0:
                return JsonResponse({'status': 'error', 'message': f'No properties found for file: {file_name}'})
            target_props.update(is_deleted=True, deleted_at=timezone.now(), deleted_by=deleter_name)
            return JsonResponse({'status': 'success', 'message': f'Successfully moved {count} plots from {file_name} to Recycle Bin.'})
            
        else:
            return JsonResponse({'status': 'error', 'message': 'Unknown delete criteria.'})

    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)})





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





@require_POST
def plot_sale_delete(request, id):
    try:
        deleter_name = _get_deleter_name(request)
        
        prop = get_object_or_404(PlotSaleProperty, id=id)
        prop.is_deleted = True
        prop.deleted_at = timezone.now()
        prop.deleted_by = deleter_name # 👈 SAVE THE NAME HERE
        prop.save() 
        return JsonResponse({"status": "success", "message": "Moved to Recycle Bin successfully!"})
    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)})


@require_POST
def plot_sale_restore(request, id):
    PlotSaleProperty.objects.filter(id=id).update(is_deleted=False, deleted_at=None, deleted_by=None)
    return JsonResponse({'status': 'success', 'message': 'Plot restored!'})

@require_POST
def plot_sale_hard_delete(request, id):
    PlotSaleProperty.objects.filter(id=id).delete()
    return JsonResponse({'status': 'success', 'message': 'Permanently deleted!'})

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
        properties = IndustrialResaleProperty.objects.filter(is_deleted=False).order_by('-created_at')
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


@require_POST
def industrial_resale_hard_delete(request, id):
    IndustrialResaleProperty.objects.filter(id=id).delete()
    return JsonResponse({'status': 'success', 'message': 'Permanently deleted!'})

@require_POST
def industrial_resale_restore(request, id):
    IndustrialResaleProperty.objects.filter(id=id).update(is_deleted=False, deleted_at=None, deleted_by=None)
    return JsonResponse({'status': 'success', 'message': 'Industrial property restored!'})

# ── 1. SINGLE DELETE VIEW (Soft Delete) ──
@require_POST
def industrial_resale_delete(request, id):
    try:
        # Get the name of the user/admin deleting the property
        deleter_name = _get_deleter_name(request)
        
        # Fetch the property
        prop = get_object_or_404(IndustrialResaleProperty, id=id)
        
        # Soft Delete
        prop.is_deleted = True
        prop.deleted_at = timezone.now()
        prop.deleted_by = deleter_name
        prop.save() 
        
        return JsonResponse({
            "status": "success", 
            "message": "Moved to Recycle Bin successfully."
        })
        
    except Exception as e:
        return JsonResponse({
            "status": "error", 
            "message": f"Failed to delete: {str(e)}"
        })


# ── 2. BULK DELETE VIEW (Soft Delete) ──
@require_POST
def industrial_bulk_delete(request):
    """Handles Advanced Bulk Deletions for Industrial Properties."""
    admin_id = request.session.get('Admin_id')
    user_id = request.session.get('User_id')
    
    if not admin_id and not user_id:
        return JsonResponse({'status': 'error', 'message': 'Unauthorized access.'})

    try:
        data = json.loads(request.body)
        delete_type = data.get('delete_type')
        deleter_name = _get_deleter_name(request)
        
        # Target only properties not currently in the Recycle Bin
        properties = IndustrialResaleProperty.objects.filter(is_deleted=False)
        
        if delete_type == 'delete_all':
            count = properties.count()
            properties.update(is_deleted=True, deleted_at=timezone.now(), deleted_by=deleter_name)
            return JsonResponse({'status': 'success', 'message': f'Successfully moved ALL {count} properties to Recycle Bin.'})
            
        elif delete_type == 'current_page':
            page_ids = data.get('page_ids', [])
            target_props = properties.filter(id__in=page_ids)
            count = target_props.count()
            target_props.update(is_deleted=True, deleted_at=timezone.now(), deleted_by=deleter_name)
            return JsonResponse({'status': 'success', 'message': f'Successfully moved {count} properties from current page to Recycle Bin.'})
            
        elif delete_type == 'date_range':
            from_date = data.get('from_date')
            to_date = data.get('to_date')
            target_props = properties.filter(created_at__date__range=[from_date, to_date])
            count = target_props.count()
            target_props.update(is_deleted=True, deleted_at=timezone.now(), deleted_by=deleter_name)
            return JsonResponse({'status': 'success', 'message': f'Successfully moved {count} properties in date range to Recycle Bin.'})
            
        elif delete_type == 'latest_month':
            thirty_days_ago = timezone.now() - timedelta(days=30)
            target_props = properties.filter(created_at__gte=thirty_days_ago)
            count = target_props.count()
            target_props.update(is_deleted=True, deleted_at=timezone.now(), deleted_by=deleter_name)
            return JsonResponse({'status': 'success', 'message': f'Successfully moved {count} properties from the last 30 days to Recycle Bin.'})
            
        elif delete_type == 'old_data':
            six_months_ago = timezone.now() - timedelta(days=180)
            target_props = properties.filter(created_at__lt=six_months_ago)
            count = target_props.count()
            target_props.update(is_deleted=True, deleted_at=timezone.now(), deleted_by=deleter_name)
            return JsonResponse({'status': 'success', 'message': f'Successfully moved {count} older properties to Recycle Bin.'})
            
        elif delete_type == 'by_uploader':
            uploader = data.get('uploader_text', '')
            target_props = properties.filter(
                Q(uploaded_by_name__icontains=uploader) | 
                Q(uploaded_by_email__icontains=uploader) |
                Q(uploaded_by_role__icontains=uploader)
            )
            count = target_props.count()
            target_props.update(is_deleted=True, deleted_at=timezone.now(), deleted_by=deleter_name)
            return JsonResponse({'status': 'success', 'message': f'Successfully moved {count} properties uploaded by {uploader} to Recycle Bin.'})

        elif delete_type == 'by_file':
            file_name = data.get('file_name', '')
            # Replace 'upload_file_name' with your exact DB field name
            target_props = properties.filter(upload_file_name=file_name) 
            count = target_props.count()
            if count == 0:
                return JsonResponse({'status': 'error', 'message': f'No properties found for file: {file_name}'})
            target_props.update(is_deleted=True, deleted_at=timezone.now(), deleted_by=deleter_name)
            return JsonResponse({'status': 'success', 'message': f'Successfully moved {count} properties from {file_name} to Recycle Bin.'})
            
        else:
            return JsonResponse({'status': 'error', 'message': 'Unknown delete criteria.'})

    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)})


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
            file_name = excel_file.name # 👈 1. GRAB THE FILE NAME HERE

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

                    # ✅ Uploader fields 
                    uploaded_by_name=uploader_name,
                    uploaded_by_email=uploader_email,
                    uploaded_by_contact=uploader_contact,
                    uploaded_by_role=uploader_role,
                    
                    # 👈 2. SAVE THE EXCEL FILE NAME IN THE DATABASE
                    upload_file_name=file_name
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
        # FIXED: Changed 'title=' to 'property_title=' to match your database schema
        prop = ResaleResidentialProperty(
            # Basic Information
            property_title    = generated_title,
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

            # Amenities & Facilities (Joining checkbox arrays into a string safely)
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

        # Save the main property object safely (this runs your model's custom save calculations)
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


def residential_resale_list(request):
    session_id = request.session.get('Admin_id')
    if not session_id:
        return render(request, 'home_page/Adminlogin.html')

    admin_obj = Admin_Login.objects.get(id=session_id)

    # ── Fetch ALL properties (used for KPI stats & chart data) ───────────────
    all_properties = (
        ResaleResidentialProperty.objects
        .prefetch_related('images')
        .order_by('-created_at')
    )

    # ── Read query params ────────────────────────────────────────────────────
    search_query    = request.GET.get('search', '').strip()
    prop_type       = request.GET.get('prop_type', '').strip()
    bhk_filter      = request.GET.get('bhk', '').strip()
    furnish         = request.GET.get('furnish', '').strip()
    zone_filter     = request.GET.get('zone', '').strip()
    ownership       = request.GET.get('ownership', '').strip()
    negotiable      = request.GET.get('negotiable', '').strip()
    from_date       = request.GET.get('from_date', '').strip()
    to_date         = request.GET.get('to_date', '').strip()

    # ── Apply filters ────────────────────────────────────────────────────────
    properties = all_properties

    # FIXED: Updated queries to map to 'property_title__icontains' to match schema
    if search_query:
        properties = properties.filter(
            Q(property_title__icontains=search_query)  |
            Q(city__icontains=search_query)           |
            Q(locality__icontains=search_query)       |
            Q(owner_name__icontains=search_query)     |
            Q(bhk__icontains=search_query)            |
            Q(building_name__icontains=search_query)
        )

    if prop_type:
        properties = properties.filter(property_type=prop_type)

    if bhk_filter:
        properties = properties.filter(bhk=bhk_filter)

    if furnish:
        properties = properties.filter(furnishing_type=furnish)

    if zone_filter:
        properties = properties.filter(zone=zone_filter)

    if ownership:
        properties = properties.filter(ownership_type=ownership)

    if negotiable:
        properties = properties.filter(is_negotiable=negotiable)

    if from_date:
        properties = properties.filter(created_at__date__gte=from_date)

    if to_date:
        properties = properties.filter(created_at__date__lte=to_date)

    # ── Thumbnail + helper attributes for each filtered property ─────────────
    for prop in properties:
        prop.thumbnail = prop.images.first()

        prop.nearby_facilities_list = (
            [f.strip() for f in prop.nearby_facilities.split(',')]
            if prop.nearby_facilities else []
        )
        prop.amenities_list = (
            [a.strip() for a in prop.amenities.split(',')]
            if prop.amenities else []
        )
        prop.image_count = prop.images.count()
        prop.image_urls  = [img.image.url for img in prop.images.all()]

    # ════════════════════════════════════════════════════════════════════════
    # KPI STATS
    # ════════════════════════════════════════════════════════════════════════
    total_count = all_properties.count()

    # ── Row 1 — Inventory ────────────────────────────────────────────────────
    total_negotiable  = all_properties.filter(is_negotiable='yes').count()
    total_furnished   = all_properties.filter(furnishing_type='fully').count()
    total_freehold    = all_properties.filter(ownership_type='freehold').count()
    total_with_images = all_properties.filter(images__isnull=False).distinct().count()

    def pct(part, whole):
        return round(part / whole * 100) if whole else 0

    negotiable_pct = pct(total_negotiable,  total_count)
    furnished_pct  = pct(total_furnished,   total_count)
    freehold_pct   = pct(total_freehold,    total_count)
    images_pct     = pct(total_with_images, total_count)

    # ── Row 2 — Pricing ──────────────────────────────────────────────────────
    price_agg = all_properties.aggregate(
        avg      = Avg('expected_price'),
        max_val  = Max('expected_price'),
        min_val  = Min('expected_price'),
        avg_sqft = Avg('price_per_sqft'),
        avg_area = Avg('builtup_area'),
    )
    avg_price      = price_agg['avg']
    max_price      = price_agg['max_val']
    min_price      = price_agg['min_val']
    avg_price_sqft = price_agg['avg_sqft']
    avg_builtup    = price_agg['avg_area']
    total_with_loan = all_properties.filter(has_loan='yes').count()

    # ── Row 3 — Legal & Status ───────────────────────────────────────────────
    no_dispute_count  = all_properties.filter(has_legal_dispute='no').count()
    dispute_count     = all_properties.filter(has_legal_dispute='yes').count()
    tax_pending_count = all_properties.filter(has_tax_due='yes').count()
    tenant_occupied   = all_properties.filter(has_tenants='yes').count()
    premium_count     = all_properties.filter(expected_price__gte=10000000).count()   # >= 1 Cr

    # ── Row 4 — Listing Quality ──────────────────────────────────────────────
    with_video_count = (
        all_properties
        .exclude(property_video__isnull=True)
        .exclude(property_video='')
        .count()
    )
    with_floor_plan = (
        all_properties
        .exclude(floor_plan__isnull=True)
        .exclude(floor_plan='')
        .count()
    )
    with_owner_count = (
        all_properties
        .exclude(owner_name__isnull=True)
        .exclude(owner_name='')
        .count()
    )
    budget_count = all_properties.filter(expected_price__lt=3000000).count()          # < 30 L

    # ── Charts ───────────────────────────────────────────────────────────────
    property_type_counts = dict(
        all_properties.values('property_type')
        .annotate(count=Count('id'))
        .values_list('property_type', 'count')
    )
    bhk_counts = dict(
        all_properties.values('bhk')
        .annotate(count=Count('id'))
        .values_list('bhk', 'count')
    )
    fully_furnished = all_properties.filter(furnishing_type='fully').count()
    semi_furnished  = all_properties.filter(furnishing_type='semi').count()
    unfurnished     = all_properties.filter(furnishing_type='unfurnished').count()

    zone_counts = dict(
        all_properties.values('zone')
        .annotate(count=Count('id'))
        .values_list('zone', 'count')
    )

    # ── Unique values for Select2 searchable dropdowns ───────────────────────
    unique_prop_types  = list(
        all_properties.values_list('property_type', flat=True)
        .distinct().order_by('property_type')
    )
    unique_bhk_values  = list(
        all_properties.values_list('bhk', flat=True)
        .distinct().order_by('bhk')
    )
    unique_zones       = list(
        all_properties.values_list('zone', flat=True)
        .distinct().order_by('zone')
    )
    unique_cities      = list(
        all_properties.values_list('city', flat=True)
        .distinct().order_by('city')
    )

    # ── Bulk-delete file list ────────────────────────────────────────────────
    try:
        uploaded_files = (
            all_properties
            .exclude(upload_file_name__isnull=True)
            .exclude(upload_file_name='')
            .values_list('upload_file_name', flat=True)
            .distinct()
        )
    except Exception:
        uploaded_files = []

    # ── Context ──────────────────────────────────────────────────────────────
    context = {
        'admin_obj'  : admin_obj,
        'properties' : properties,

        # Counts
        'filtered_count' : properties.count(),
        'total_count'    : total_count,

        # Active search params
        'search_query'   : search_query,
        'prop_type_query': prop_type,
        'bhk_query'      : bhk_filter,
        'furnish_query'  : furnish,
        'zone_query'     : zone_filter,
        'ownership_query': ownership,
        'negotiable_query': negotiable,
        'from_date'      : from_date,
        'to_date'        : to_date,

        # Row 1 — Inventory
        'total_negotiable' : total_negotiable,
        'total_furnished'  : total_furnished,
        'total_freehold'   : total_freehold,
        'total_with_images': total_with_images,
        'negotiable_pct'   : negotiable_pct,
        'furnished_pct'    : furnished_pct,
        'freehold_pct'     : freehold_pct,
        'images_pct'       : images_pct,

        # Row 2 — Pricing
        'avg_price'       : avg_price,
        'max_price'       : max_price,
        'min_price'       : min_price,
        'avg_price_sqft'  : avg_price_sqft,
        'total_with_loan' : total_with_loan,

        # Row 3 — Legal
        'no_dispute_count' : no_dispute_count,
        'dispute_count'    : dispute_count,
        'tax_pending_count': tax_pending_count,
        'tenant_occupied'  : tenant_occupied,
        'avg_builtup'      : avg_builtup,
        'premium_count'    : premium_count,

        # Row 4 — Quality
        'with_video_count': with_video_count,
        'with_floor_plan' : with_floor_plan,
        'with_owner_count': with_owner_count,
        'budget_count'    : budget_count,

        # Charts
        'property_type_counts': property_type_counts,
        'bhk_counts'          : bhk_counts,
        'fully_furnished'     : fully_furnished,
        'semi_furnished'      : semi_furnished,
        'unfurnished'         : unfurnished,
        'zone_counts'         : zone_counts,

        # Select2 unique options
        'unique_prop_types' : unique_prop_types,
        'unique_bhk_values' : unique_bhk_values,
        'unique_zones'      : unique_zones,
        'unique_cities'     : unique_cities,

        'uploaded_files': uploaded_files,
    }

    return render(
        request,
        'admin_user/Reports/Resale/residential_resale_list.html',
        context,
    )



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

@require_POST
def resale_residential_delete(request, pk):
    uploader = _get_uploader(request)
    if uploader is None:
        return redirect('login')
        
    deleter_name = _get_deleter_name(request)

    prop = get_object_or_404(ResaleResidentialProperty, pk=pk)
    prop.is_deleted = True
    prop.deleted_at = timezone.now()
    prop.deleted_by = deleter_name # 👈 SAVE THE NAME HERE
    prop.save()

    return JsonResponse({"status" : "success", "message": "Moved to Recycle Bin successfully!"})
   

   
@require_POST
def resale_restore(request, id):
    ResaleResidentialProperty.objects.filter(id=id).update(is_deleted=False, deleted_at=None, deleted_by=None)
    return JsonResponse({'status': 'success', 'message': 'Resale property restored!'})

@require_POST
def resale_hard_delete(request, id):
    ResaleResidentialProperty.objects.filter(id=id).delete()
    return JsonResponse({'status': 'success', 'message': 'Permanently deleted!'})
   



def generate_row_hash(row_values):
    """Generates a secure MD5 signature unique to the actual data values inside a row."""
    data_string = "|".join([str(v).strip().lower() for v in row_values if v is not None])
    return hashlib.md5(data_string.encode('utf-8')).hexdigest()

def resale_residential_import_excel(request):
    session_id = request.session.get('Admin_id')
    if not session_id:
        return JsonResponse({'status': 'error', 'message': 'Session expired. Please log in again.'})

    if request.method != 'POST':
        return JsonResponse({'status': 'error', 'message': 'Invalid operational request method.'})

    excel_file = request.FILES.get('excel_file')
    if not excel_file:
        return JsonResponse({'status': 'error', 'message': 'No file uploaded. Please select a valid sheet.'})

    if not excel_file.name.endswith('.xlsx'):
        return JsonResponse({'status': 'error', 'message': 'Invalid format. Only .xlsx extensions allowed.'})

    try:
        # Fetch current uploader meta profiles cleanly from active backend entities
        uploader_obj = Admin_Login.objects.get(id=session_id)
        current_uploader_name = getattr(uploader_obj, 'name', 'System Admin')
        current_uploader_email = getattr(uploader_obj, 'email', 'admin@crm.com')
        current_uploader_contact = getattr(uploader_obj, 'phone', '0000000000')
        current_uploader_role = getattr(uploader_obj, 'role', 'admin')
    except Exception:
        current_uploader_name = "System Admin"
        current_uploader_email = "admin@crm.com"
        current_uploader_contact = "0000000000"
        current_uploader_role = "admin"

    try:
        wb = openpyxl.load_workbook(excel_file, data_only=True)
        ws = wb.active

        # Define explicit model order sequences matching column indexes exactly
        # Skipping 'property_id' and 'property_title' as they automate dynamically downstream!
        expected_headers = [
            'property_type', 'zone', 'society_type', 'water_type', 'furnishing_type', 
            'age_of_property', 'facing', 'available_from', 'bhk', 'bathrooms', 
            'balconies', 'covered_parking', 'open_parking', 'builtup_area', 'carpet_area', 
            'plot_area', 'floor_no', 'total_floors', 'ownership_type', 'num_owners', 
            'has_loan', 'loan_amount', 'has_tenants', 'tenant_details', 'has_legal_dispute', 
            'dispute_details', 'has_tax_due', 'pending_tax_amount', 'expected_price', 
            'price_per_sqft', 'is_negotiable', 'brokerage', 'brokerage_percentage', 
            'manual_brokerage', 'description', 'nearby_facilities', 'amenities', 
            'city', 'locality', 'building_name', 'complete_address', 'owner_name', 
            'owner_contact', 'owner_email', 'residential_status'
        ]

        # Extract actual file header row values cleanly
        file_headers = [str(cell.value).strip().lower() for cell in ws[1] if cell.value is not None]

        # Check for mandatory missing field layouts
        missing_fields = [f for f in expected_headers if f not in file_headers]
        if missing_fields:
            return JsonResponse({
                'status': 'error',
                'message': f'Required structural headers missing: {", ".join(missing_fields)}'
            })

        # Map dynamic positions to avoid tracking offsets manually
        header_map = {str(cell.value).strip().lower(): idx for idx, cell in enumerate(ws[1]) if cell.value is not None}

        imported = 0
        skipped = 0
        duplicate_files_detected = 0

        for row_idx, row in enumerate(ws.iter_rows(min_row=2, values_only=True), start=2):
            if not any(row):
                continue

            try:
                # Direct assignment through verified mapping matrices
                p_type       = row[header_map['property_type']]
                zone         = row[header_map['zone']]
                soc_type     = row[header_map['society_type']]
                wat_type     = row[header_map['water_type']]
                furnish      = row[header_map['furnishing_type']]
                age          = row[header_map['age_of_property']]
                facing       = row[header_map['facing']]
                avail_from   = row[header_map['available_from']]
                bhk          = row[header_map['bhk']]
                baths        = row[header_map['bathrooms']]
                balconies    = row[header_map['balconies']]
                cov_parking  = row[header_map['covered_parking']]
                op_parking   = row[header_map['open_parking']]
                builtup      = row[header_map['builtup_area']]
                carpet       = row[header_map['carpet_area']]
                plot         = row[header_map['plot_area']]
                floor_no     = row[header_map['floor_no']]
                tot_floors   = row[header_map['total_floors']]
                ownership    = row[header_map['ownership_type']]
                num_owners   = row[header_map['num_owners']]
                has_loan     = row[header_map['has_loan']]
                loan_amt     = row[header_map['loan_amount']]
                has_tenants  = row[header_map['has_tenants']]
                ten_details  = row[header_map['tenant_details']]
                has_dispute  = row[header_map['has_legal_dispute']]
                disp_details = row[header_map['dispute_details']]
                has_tax      = row[header_map['has_tax_due']]
                tax_amt      = row[header_map['pending_tax_amount']]
                price        = row[header_map['expected_price']]
                price_sqft   = row[header_map['price_per_sqft']]
                negotiable   = row[header_map['is_negotiable']]
                brokerage    = row[header_map['brokerage']]
                brok_pct     = row[header_map['brokerage_percentage']]
                man_brok     = row[header_map['manual_brokerage']]
                desc         = row[header_map['description']]
                facilities   = row[header_map['nearby_facilities']]
                amenities    = row[header_map['amenities']]
                city         = row[header_map['city']]
                locality     = row[header_map['locality']]
                bld_name     = row[header_map['building_name']]
                address      = row[header_map['complete_address']]
                own_name     = row[header_map['owner_name']]
                own_cont     = row[header_map['owner_contact']]
                own_email    = row[header_map['owner_email']]
                res_status   = row[header_map['residential_status']]

                # Mandatory row level validation triggers
                if not all([p_type, bhk, builtup, price, city, locality, address, own_name, own_cont]):
                    skipped += 1
                    continue

                # Content-duplicate checks using hashes
                current_row_hash = generate_row_hash(row)
                
                # Check for historical duplication bounds
                is_duplicate = ResaleResidentialProperty.objects.filter(
                    property_type=str(p_type).strip().lower(),
                    bhk=str(bhk).strip().lower(),
                    builtup_area=float(builtup),
                    expected_price=float(price),
                    locality=str(locality).strip(),
                    owner_contact=str(own_cont).strip()
                ).exists()

                if is_duplicate:
                    duplicate_files_detected += 1
                    continue

                # Process parsed data into DB entry fields safely
                prop = ResaleResidentialProperty(
                    property_type=str(p_type).strip().lower(),
                    zone=str(zone).strip().lower() if zone else '',
                    society_type=str(soc_type).strip().lower() if soc_type else '',
                    water_type=str(wat_type).strip().lower() if wat_type else '',
                    furnishing_type=str(furnish).strip().lower() if furnish else '',
                    age_of_property=str(age).strip() if age else '',
                    facing=str(facing).strip() if facing else '',
                    bhk=str(bhk).strip().lower(),
                    bathrooms=int(baths) if baths else 1,
                    balconies=int(balconies) if balconies else 0,
                    covered_parking=int(cov_parking) if cov_parking else 0,
                    open_parking=int(op_parking) if op_parking else 0,
                    builtup_area=float(builtup),
                    carpet_area=float(carpet) if carpet else 0,
                    plot_area=float(plot) if plot else None,
                    floor_no=int(floor_no) if floor_no else 0,
                    total_floors=int(tot_floors) if tot_floors else 1,
                    ownership_type=str(ownership).strip().lower() if ownership else 'freehold',
                    num_owners=str(num_owners).strip() if num_owners else '1',
                    has_loan=str(has_loan).strip().lower() if has_loan else 'no',
                    loan_amount=float(loan_amt) if loan_amt else None,
                    has_tenants=str(has_tenants).strip().lower() if has_tenants else 'no',
                    tenant_details=str(ten_details).strip() if ten_details else None,
                    has_legal_dispute=str(has_dispute).strip().lower() if has_dispute else 'no',
                    dispute_details=str(disp_details).strip() if disp_details else None,
                    has_tax_due=str(has_tax).strip().lower() if has_tax else 'no',
                    pending_tax_amount=float(tax_amt) if tax_amt else None,
                    expected_price=float(price),
                    price_per_sqft=float(price_sqft) if price_sqft else None,
                    is_negotiable=str(negotiable).strip().lower() if negotiable else 'yes',
                    brokerage=str(brokerage).strip() if brokerage else None,
                    brokerage_percentage=str(brok_pct).strip() if brok_pct else None,
                    manual_brokerage=str(man_brok).strip() if man_brok else None,
                    description=str(desc).strip() if desc else '',
                    nearby_facilities=str(facilities).strip() if facilities else '',
                    amenities=str(amenities).strip() if amenities else '',
                    city=str(city).strip(),
                    locality=str(locality).strip(),
                    building_name=str(bld_name).strip() if bld_name else None,
                    complete_address=str(address).strip(),
                    owner_name=str(own_name).strip(),
                    owner_contact=str(own_cont).strip(),
                    owner_email=str(own_email).strip() if own_email else '',
                    residential_status=str(res_status).strip().lower() if res_status else 'resident',
                    
                    # Core systemic metrics overrule spreadsheet columns safely
                    uploaded_by_name=current_uploader_name,
                    uploaded_by_email=current_uploader_email,
                    uploaded_by_contact=current_uploader_contact,
                    uploaded_by_role=current_uploader_role
                )

                # Process specific date formats safely
                if avail_from:
                    if isinstance(avail_from, datetime):
                        prop.available_from = avail_from.date()
                    else:
                        try:
                            prop.available_from = datetime.strptime(str(avail_from).strip(), '%Y-%m-%d').date()
                        except ValueError:
                            pass

                prop.save()
                imported += 1

            except Exception as e:
                print(f"Skipped row structure execution context anomaly on index line {row_idx}: {e}")
                skipped += 1

        # Return comprehensive statistical metrics for frontend SweetAlert parsing
        if imported == 0 and duplicate_files_detected > 0:
            return JsonResponse({
                'status': 'duplicate', 
                'message': 'No entries saved. All row records inside this file already exist in the system database matching data arrays.'
            })

        return JsonResponse({
            'status': 'success',
            'imported': imported,
            'skipped': skipped,
            'duplicates': duplicate_files_detected
        })

    except Exception as e:
        return JsonResponse({'status': 'error', 'message': f'Process Error: {str(e)}'})


def resale_residential_sample_excel(request):
    session_id = request.session.get('Admin_id')
    if not session_id:
        return redirect('login')

    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Resale Structural Template"

    # Define strict segmented layout arrays directly representing your technical model
    sections = [
        # SECTION 1: BASIC INFORMATION
        ('property_type', 'apartment'), ('zone', 'north'), ('society_type', 'gated'), 
        ('water_type', 'municipal'), ('furnishing_type', 'semi'), ('age_of_property', '1-3'), 
        ('facing', 'North-East'), ('available_from', '2026-06-01'),
        # SECTION 2: CONFIGURATION
        ('bhk', '3bhk'), ('bathrooms', 2), ('balconies', 1), ('covered_parking', 1), ('open_parking', 0),
        # SECTION 3: MEASUREMENTS
        ('builtup_area', 1200), ('carpet_area', 950), ('plot_area', ''), ('floor_no', 3), ('total_floors', 10),
        # SECTION 4: LEGAL & OWNERSHIP
        ('ownership_type', 'freehold'), ('num_owners', '1'), ('has_loan', 'yes'), ('loan_amount', 2000000), 
        ('has_tenants', 'no'), ('tenant_details', ''), ('has_legal_dispute', 'no'), ('dispute_details', ''), 
        ('has_tax_due', 'no'), ('pending_tax_amount', ''),
        # SECTION 5: PRICING METRICS
        ('expected_price', 5000000), ('price_per_sqft', 4166.67), ('is_negotiable', 'yes'), 
        ('brokerage', 'yes'), ('brokerage_percentage', '2%'), ('manual_brokerage', ''), 
        ('description', 'Luxurious residential flat with modular kitchen modules near arterial transit routes.'),
        # SECTION 6: AMENITIES & SPATIAL LOCATION
        ('nearby_facilities', 'school, hospital, metro'), ('amenities', 'lift, parking, security, gym'), 
        ('city', 'Nagpur'), ('locality', 'Dharampeth'), ('building_name', 'Sunshine Heights'), 
        ('complete_address', 'Flat 302, Sunshine Heights, Dharampeth, Nagpur'),
        # SECTION 7: VERIFIED OWNER FIELDS
        ('owner_name', 'Rahul Sharma'), ('owner_contact', '9876543210'), 
        ('owner_email', 'rahul.sharma@example.com'), ('residential_status', 'resident')
    ]

    headers = [item[0] for item in sections]
    sample_row = [item[1] for item in sections]

    ws.append(headers)
    ws.append(sample_row)

    # Apply corporate formatting styles to header structures
    header_font = Font(name='Poppins', size=11, bold=True, color='FFFFFF')
    header_fill = PatternFill(start_color='667EEA', end_color='667EEA', fill_type='solid')

    for col_idx, cell in enumerate(ws[1], start=1):
        cell.font = header_font
        cell.fill = header_fill

    # Adapt individual column width profiles dynamically to match strings
    for col in ws.columns:
        max_len = max(len(str(cell.value or '')) for cell in col)
        col_letter = openpyxl.utils.get_column_letter(col[0].column)
        ws.column_dimensions[col_letter].width = max(max_len + 4, 15)

    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = 'attachment; filename="resale_residential_template.xlsx"'
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
    props = CommercialResaleProperty.objects.filter(is_deleted=False).order_by('-id')

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


import os


def add_commercial_property(request):
    # ── Step 1: Session check — who is logged in? ──────
    uploader = _get_uploader(request)
    if uploader is None:
        return redirect('login')   # not logged in → redirect to login

    # ── Step 2: Handle POST (form submission) ──────────
    if request.method == "POST":
        try:
            prop = CommercialResaleProperty(
                # ── Basic Information ──────────────────────
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
                loan_on_property    = request.POST.get('loan_on_property', 'no'),
                loan_amount         = request.POST.get('loan_amount') or None,
                existing_tenants    = request.POST.get('existing_tenants', 'no'),
                tenant_details      = request.POST.get('tenant_details') or None,
                legal_dispute       = request.POST.get('legal_dispute', 'no'),
                dispute_details     = request.POST.get('dispute_details') or None,
                tax_due             = request.POST.get('tax_due', 'no'),
                pending_tax_amount  = request.POST.get('pending_tax_amount') or None,
                fire_noc            = request.POST.get('fire_noc') or None,
                property_description = request.POST.get('property_description'),
                sanctioning_authority = request.POST.get('sanctioning_authority'),

                # ── Media ──────────────────────────────────
                floor_plan          = request.FILES.get('floor_plan') or None,
                property_video      = request.FILES.get('property_video') or None,

                # ── Amenities & Facilities (checkbox arrays matched with form POST name) ────
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

                # ── Listing Uploaded By (Pre-filled variables) ─────
                uploaded_by_name    = uploader.get('uploader_name'),
                uploaded_by_email   = uploader.get('uploader_email'),
                uploaded_by_contact = uploader.get('uploader_phone'),
                uploaded_by_role    = uploader.get('uploader_role'),
            )

            # Invokes save() to compute price_per_sqft and write automated property_title
            prop.save()  

            # ── Save multiple property images ───────────────
            images = request.FILES.getlist('property_images')
            for image in images[:10]:    
                CommercialPropertyImage.objects.create(
                    property=prop,
                    image=image
                )

            return JsonResponse({
                "status": "success",
                "message": "Commercial Property Added Successfully",
                "generated_title": prop.property_title
            })
            
        except Exception as e:
            return JsonResponse({
                "status": "error",
                "message": f"Database transaction failed: {str(e)}"
            }, status=400)

    # ── Step 3: GET — render form with context objects ──
    context = {
        "admin_obj"       : uploader.get('admin_obj'), 
        "user_obj"        : uploader.get('user_obj'), 
        "uploader_name"   : uploader.get('uploader_name'),
        "uploader_email"  : uploader.get('uploader_email'),
        "uploader_phone"  : uploader.get('uploader_phone'),
        "uploader_role"   : uploader.get('uploader_role'),
        # Ensure your standard seed querysets are sent down for selection loop structures:
        "facilities_obj"  : FacilitiesModel.objects.all() if 'FacilitiesModel' in globals() else [],
        "ameneties_obj"   : AmenitiesModel.objects.all() if 'AmenitiesModel' in globals() else [],
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
            deleter_name = _get_deleter_name(request)
            
            prop = CommercialResaleProperty.objects.get(id=prop_id)
            prop.is_deleted = True
            prop.deleted_at = timezone.now()
            prop.deleted_by = deleter_name # 👈 SAVE THE NAME HERE
            prop.save()
            
            return JsonResponse({'status': 'success', '1': '1', 'msg': 'Moved to Recycle Bin successfully.'})
        except CommercialResaleProperty.DoesNotExist:
            return JsonResponse({'status': 'error', '0': '0', 'msg': 'Property not found.'})
    return JsonResponse({'status': 'error', 'msg': 'Invalid request.'})



@require_POST
def commercial_resale_bulk_delete(request):
    """Handles Advanced Bulk Deletions for Commercial Resale Properties."""
    admin_id = request.session.get('Admin_id')
    user_id = request.session.get('User_id')
    
    if not admin_id and not user_id:
        return JsonResponse({'status': 'error', 'message': 'Unauthorized access.'})

    try:
        data = json.loads(request.body)
        delete_type = data.get('delete_type')
        deleter_name = _get_deleter_name(request)
        
        # Target only properties not currently in the Recycle Bin
        properties = CommercialResaleProperty.objects.filter(is_deleted=False)
        
        if delete_type == 'delete_all':
            count = properties.count()
            properties.update(is_deleted=True, deleted_at=timezone.now(), deleted_by=deleter_name)
            return JsonResponse({'status': 'success', 'message': f'Successfully moved ALL {count} properties to Recycle Bin.'})
            
        elif delete_type == 'current_page':
            page_ids = data.get('page_ids', [])
            target_props = properties.filter(id__in=page_ids)
            count = target_props.count()
            target_props.update(is_deleted=True, deleted_at=timezone.now(), deleted_by=deleter_name)
            return JsonResponse({'status': 'success', 'message': f'Successfully moved {count} properties from current page to Recycle Bin.'})
            
        elif delete_type == 'date_range':
            from_date = data.get('from_date')
            to_date = data.get('to_date')
            target_props = properties.filter(created_at__date__range=[from_date, to_date])
            count = target_props.count()
            target_props.update(is_deleted=True, deleted_at=timezone.now(), deleted_by=deleter_name)
            return JsonResponse({'status': 'success', 'message': f'Successfully moved {count} properties in date range to Recycle Bin.'})
            
        elif delete_type == 'latest_month':
            thirty_days_ago = timezone.now() - timedelta(days=30)
            target_props = properties.filter(created_at__gte=thirty_days_ago)
            count = target_props.count()
            target_props.update(is_deleted=True, deleted_at=timezone.now(), deleted_by=deleter_name)
            return JsonResponse({'status': 'success', 'message': f'Successfully moved {count} properties from the last 30 days to Recycle Bin.'})
            
        elif delete_type == 'old_data':
            six_months_ago = timezone.now() - timedelta(days=180)
            target_props = properties.filter(created_at__lt=six_months_ago)
            count = target_props.count()
            target_props.update(is_deleted=True, deleted_at=timezone.now(), deleted_by=deleter_name)
            return JsonResponse({'status': 'success', 'message': f'Successfully moved {count} older properties to Recycle Bin.'})
            
        elif delete_type == 'by_uploader':
            uploader = data.get('uploader_text', '')
            target_props = properties.filter(
                Q(uploaded_by_name__icontains=uploader) | 
                Q(uploaded_by_email__icontains=uploader) |
                Q(uploaded_by_role__icontains=uploader)
            )
            count = target_props.count()
            target_props.update(is_deleted=True, deleted_at=timezone.now(), deleted_by=deleter_name)
            return JsonResponse({'status': 'success', 'message': f'Successfully moved {count} properties uploaded by {uploader} to Recycle Bin.'})

        elif delete_type == 'by_file':
            file_name = data.get('file_name', '')
            target_props = properties.filter(upload_file_name=file_name) 
            count = target_props.count()
            if count == 0:
                return JsonResponse({'status': 'error', 'message': f'No properties found for file: {file_name}'})
            target_props.update(is_deleted=True, deleted_at=timezone.now(), deleted_by=deleter_name)
            return JsonResponse({'status': 'success', 'message': f'Successfully moved {count} properties from {file_name} to Recycle Bin.'})
            
        else:
            return JsonResponse({'status': 'error', 'message': 'Unknown delete criteria.'})

    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)})


@require_POST
def commercial_resale_restore(request, id):
    try:
        # Reset the flags to put it back in the main active list
        CommercialResaleProperty.objects.filter(id=id).update(
            is_deleted=False, 
            deleted_at=None, 
            deleted_by=None
        )
        return JsonResponse({'status': 'success', 'message': 'Commercial Resale property restored successfully!'})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)})

# ── 2. HARD DELETE COMMERCIAL RESALE ──
@require_POST
def commercial_resale_hard_delete(request, id):
    try:
        # Fetch the property and permanently delete it from the database
        prop = CommercialResaleProperty.objects.get(id=id)
        prop.delete() # This will also delete associated images if cascading is set up
        
        return JsonResponse({'status': 'success', 'message': 'Property permanently deleted!'})
    except CommercialResaleProperty.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Property not found.'})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)})

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
    """
    Handles the 4-step agricultural property listing form submission.
    Field mapping follows the exact DB model column sequence.
    """
    if request.method == 'POST':
        try:
            def get_decimal(val):
                """Returns cleaned decimal value or None if blank."""
                return val if val and str(val).strip() != "" else None

            with transaction.atomic():

                property_obj = AgriculturalResaleProperty.objects.create(

                    # ── STEP 1: LAND DETAILS ─────────────────────────────────
                    # DB sequence: agriculture_property_type → village → taluka →
                    #              district → land_area → soil_type →
                    #              irrigation_facility → water_source →
                    #              previous_crops → fertility_status

                    agriculture_property_type = request.POST.get('agriculture_property_type', ''),
                    village                   = request.POST.get('village', ''),
                    taluka                    = request.POST.get('taluka', ''),
                    district                  = request.POST.get('district', ''),
                    land_area                 = get_decimal(request.POST.get('land_area')),
                    soil_type                 = request.POST.get('soil_type') or None,
                    irrigation_facility       = request.POST.get('irrigation_facility', 'no'),
                    water_source              = request.POST.get('water_source') or None,
                    previous_crops            = request.POST.get('previous_crops') or None,
                    fertility_status          = request.POST.get('fertility_status') or None,

                    # ── STEP 2: PRICING & LEGAL ──────────────────────────────
                    # DB sequence: expected_price → brokerage → brokerage_percentage →
                    #              manual_brokerage → ownership_type →
                    #              agri_loan → loan_amount →
                    #              agri_tenants → tenant_details →
                    #              agri_dispute → dispute_details →
                    #              agri_tax_due → pending_tax_amount →
                    #              resale_agricultural_desc

                    expected_price            = get_decimal(request.POST.get('expected_price')),
                    brokerage                 = request.POST.get('brokerage') or None,
                    brokerage_percentage      = request.POST.get('brokerage_percentage') or None,
                    manual_brokerage          = request.POST.get('manual_brokerage') or None,

                    ownership_type            = request.POST.get('ownership_type', ''),

                    agri_loan                 = request.POST.get('agri_loan', 'no'),
                    loan_amount               = (
                        get_decimal(request.POST.get('loan_amount'))
                        if request.POST.get('agri_loan') == 'yes'
                        else None
                    ),

                    agri_tenants              = request.POST.get('agri_tenants', 'no'),
                    tenant_details            = (
                        request.POST.get('tenant_details') or None
                        if request.POST.get('agri_tenants') == 'yes'
                        else None
                    ),

                    agri_dispute              = request.POST.get('agri_dispute', 'no'),
                    dispute_details           = (
                        request.POST.get('dispute_details') or None
                        if request.POST.get('agri_dispute') == 'yes'
                        else None
                    ),

                    agri_tax_due              = request.POST.get('agri_tax_due', 'no'),
                    pending_tax_amount        = (
                        get_decimal(request.POST.get('pending_tax_amount'))
                        if request.POST.get('agri_tax_due') == 'yes'
                        else None
                    ),

                    resale_agricultural_desc  = request.POST.get('resale_agricultural_desc', ''),

                    # ── STEP 3: LOCATION & OWNER ─────────────────────────────
                    # DB sequence: city → state → locality → address →
                    #              owner_name → owner_contact → owner_email →
                    #              comm_residency

                    city                      = request.POST.get('city', ''),
                    state                     = request.POST.get('state', ''),
                    locality                  = request.POST.get('locality', ''),
                    address                   = request.POST.get('address', ''),

                    owner_name                = request.POST.get('owner_name', ''),
                    owner_contact             = request.POST.get('owner_contact', ''),
                    owner_email               = request.POST.get('owner_email', ''),
                    comm_residency            = request.POST.get('comm_residency', 'resident'),

                    # ── STEP 4: UPLOADER AUDIT FIELDS ────────────────────────
                    # Note: property_images[] and encumbrance_cert are handled
                    #       separately below (file fields).

                    uploaded_by_name          = request.POST.get('uploaded_by_name') or None,
                    uploaded_by_email         = request.POST.get('uploaded_by_email') or None,
                    uploaded_by_contact       = request.POST.get('uploaded_by_contact') or None,
                    uploaded_by_role          = request.POST.get('uploaded_by_role') or None,
                )

                # ── FILE FIELDS ──────────────────────────────────────────────
                # encumbrance_cert  — required document
                if 'encumbrance_cert' in request.FILES:
                    property_obj.encumbrance_cert = request.FILES['encumbrance_cert']

                # property_video — optional media
                if 'property_video' in request.FILES:
                    property_obj.property_video = request.FILES['property_video']

                # Persist file field changes (title auto-generation happens in save())
                property_obj.save()

                # ── MULTIPLE IMAGES — child model (max 10) ───────────────────
                images = request.FILES.getlist('property_images[]')
                for img in images[:10]:
                    AgriculturalResaleImage.objects.create(
                        property=property_obj,
                        image=img
                    )

            return JsonResponse({
                'status': 'success',
                'message': f'Property "{property_obj.title}" listed successfully!',
                # Uncomment and set your redirect URL:
                # 'redirect_url': '/admin/agricultural-properties/',
            })

        except Exception as e:
            import traceback
            return JsonResponse({
                'status': 'error',
                'message': str(e),
                # Remove in production:
                'trace': traceback.format_exc(),
            }, status=400)

    # GET — render the form (pass admin context for uploader fields)
    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'}, status=405)


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
        file_name = excel_file.name  # 👈 1. Grab the file name here

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

                # DUPLICATE CHECK
                exists = AgriculturalResaleProperty.objects.filter(
                    village=get_string(row.get('village')),
                    city=get_string(row.get('city')),
                    owner_contact=get_string(row.get('owner_contact')),
                    address=get_string(row.get('address'))
                ).exists()

                if exists:
                    skipped_count += 1
                    continue

                # CREATE OBJECT
                AgriculturalResaleProperty.objects.create(
                    # STEP 1
                    title=get_string(row.get('title'), 'Agricultural Land Listing'),
                    agriculture_property_type=get_string(row.get('agriculture_property_type'), 'agriculture_land'),

                    land_area=(
                        get_decimal(row.get('land_area'))
                        or get_decimal(row.get('area'))
                        or 0
                    ),

                    state=get_string(row.get('state')),
                    city=get_string(row.get('city')),
                    district=get_string(row.get('district')),
                    taluka=get_string(row.get('taluka')),
                    village=get_string(row.get('village')),
                    address=(
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
                    
                    # 👈 2. Save the filename so the Bulk Delete Dropdown works!
                    upload_file_name=file_name 
                )

                added_count += 1

            # MESSAGES
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
    
    # 👈 3. Filter out deleted items from the main query
    base_qs = AgriculturalResaleProperty.objects.filter(is_deleted=False)
    
    properties = base_qs.order_by('-created_at')
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

    # 👈 4. Ensure stats only calculate active (non-deleted) items
    total_properties = base_qs.count()
    agri_land_count = base_qs.filter(agriculture_property_type='agriculture_land').count()
    farm_land_count = base_qs.filter(agriculture_property_type='farm_land').count()
    orchard_land_count = base_qs.filter(agriculture_property_type='orchard_land').count()

    total_value = base_qs.aggregate(
        Sum('expected_price')
    )['expected_price__sum'] or 0

    # 👈 5. Fetch unique uploaded file names for the Bulk Delete modal
    try:
        # Check if upload_file_name exists on this model. If not, this returns empty list safely.
        uploaded_files = base_qs.exclude(
            upload_file_name__isnull=True
        ).exclude(upload_file_name='').values_list('upload_file_name', flat=True).distinct()
    except Exception:
        uploaded_files = []

    context = {
        'admin_obj': admin_obj,
        'page_obj': page_obj,
        'search_query': search_query,
        'uploaded_files': uploaded_files, # 👈 Passed to template here
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


@require_POST
def agricultural_resale_restore(request, id):
    AgriculturalResaleProperty.objects.filter(id=id).update(is_deleted=False, deleted_at=None, deleted_by=None)
    return JsonResponse({'status': 'success', 'message': 'Agricultural property restored!'})

@require_POST
def agricultural_resale_hard_delete(request, id):
    AgriculturalResaleProperty.objects.filter(id=id).delete()
    return JsonResponse({'status': 'success', 'message': 'Permanently deleted!'})


# ── 1. SINGLE DELETE VIEW (Soft Delete) ──
@require_POST
def delete_agricultural_property(request, pk):
    try:
        # Get the name of the user/admin deleting the property
        deleter_name = _get_deleter_name(request)
        
        property_obj = get_object_or_404(AgriculturalResaleProperty, pk=pk)
        
        # Soft Delete
        property_obj.is_deleted = True
        property_obj.deleted_at = timezone.now()
        property_obj.deleted_by = deleter_name
        property_obj.save()
        
        return JsonResponse({
            'status': 'success', 
            'message': 'Moved to Recycle Bin successfully.'
        })
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)})


# ── 2. BULK DELETE VIEW (Soft Delete) ──
@require_POST
def agricultural_bulk_delete(request):
    """Handles Advanced Bulk Deletions for Agricultural Properties."""
    admin_id = request.session.get('Admin_id')
    user_id = request.session.get('User_id')
    
    if not admin_id and not user_id:
        return JsonResponse({'status': 'error', 'message': 'Unauthorized access.'})

    try:
        data = json.loads(request.body)
        delete_type = data.get('delete_type')
        deleter_name = _get_deleter_name(request)
        
        # Target only properties not currently in the Recycle Bin
        properties = AgriculturalResaleProperty.objects.filter(is_deleted=False)
        
        if delete_type == 'delete_all':
            count = properties.count()
            properties.update(is_deleted=True, deleted_at=timezone.now(), deleted_by=deleter_name)
            return JsonResponse({'status': 'success', 'message': f'Successfully moved ALL {count} properties to Recycle Bin.'})
            
        elif delete_type == 'current_page':
            page_ids = data.get('page_ids', [])
            target_props = properties.filter(id__in=page_ids)
            count = target_props.count()
            target_props.update(is_deleted=True, deleted_at=timezone.now(), deleted_by=deleter_name)
            return JsonResponse({'status': 'success', 'message': f'Successfully moved {count} properties from current page to Recycle Bin.'})
            
        elif delete_type == 'date_range':
            from_date = data.get('from_date')
            to_date = data.get('to_date')
            # Assuming you want to filter by the created date
            target_props = properties.filter(created_at__date__range=[from_date, to_date])
            count = target_props.count()
            target_props.update(is_deleted=True, deleted_at=timezone.now(), deleted_by=deleter_name)
            return JsonResponse({'status': 'success', 'message': f'Successfully moved {count} properties in date range to Recycle Bin.'})
            
        elif delete_type == 'latest_month':
            thirty_days_ago = timezone.now() - timedelta(days=30)
            target_props = properties.filter(created_at__gte=thirty_days_ago)
            count = target_props.count()
            target_props.update(is_deleted=True, deleted_at=timezone.now(), deleted_by=deleter_name)
            return JsonResponse({'status': 'success', 'message': f'Successfully moved {count} properties from the last 30 days to Recycle Bin.'})
            
        elif delete_type == 'old_data':
            six_months_ago = timezone.now() - timedelta(days=180)
            target_props = properties.filter(created_at__lt=six_months_ago)
            count = target_props.count()
            target_props.update(is_deleted=True, deleted_at=timezone.now(), deleted_by=deleter_name)
            return JsonResponse({'status': 'success', 'message': f'Successfully moved {count} older properties to Recycle Bin.'})
            
        elif delete_type == 'by_uploader':
            uploader = data.get('uploader_text', '')
            target_props = properties.filter(
                Q(uploaded_by_name__icontains=uploader) | 
                Q(uploaded_by_email__icontains=uploader) |
                Q(uploaded_by_role__icontains=uploader)
            )
            count = target_props.count()
            target_props.update(is_deleted=True, deleted_at=timezone.now(), deleted_by=deleter_name)
            return JsonResponse({'status': 'success', 'message': f'Successfully moved {count} properties uploaded by {uploader} to Recycle Bin.'})

        elif delete_type == 'by_file':
            file_name = data.get('file_name', '')
            # Replace 'upload_file_name' with your exact DB field name
            target_props = properties.filter(upload_file_name=file_name) 
            count = target_props.count()
            if count == 0:
                return JsonResponse({'status': 'error', 'message': f'No properties found for file: {file_name}'})
            target_props.update(is_deleted=True, deleted_at=timezone.now(), deleted_by=deleter_name)
            return JsonResponse({'status': 'success', 'message': f'Successfully moved {count} properties from {file_name} to Recycle Bin.'})
            
        else:
            return JsonResponse({'status': 'error', 'message': 'Unknown delete criteria.'})

    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)})




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
    # --- Handle Bulk Action Logic ---
    if request.method == 'POST' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        selected_ids = request.POST.getlist('ids[]')
        action = request.POST.get('action')
        
        if action == 'active':
            LocationSEO.objects.filter(id__in=selected_ids).update(is_active=True)
        elif action == 'pause':
            LocationSEO.objects.filter(id__in=selected_ids).update(is_active=False)
            
        return JsonResponse({'status': 'success', 'message': f'Items updated to {action}'})

    session_id = request.session.get('Admin_id')
    if not session_id:
        return render(request, 'home_page/Adminlogin.html')
    
    # --- Regular List Logic ---
    # Retrieve all pages ordered by type for consistent grouping

    seo_pages = LocationSEO.objects.all().order_by('pagetype', '-id')

    # Get distinct page types and their counts for the menu/cards
    type_counts = LocationSEO.objects.values('pagetype').annotate(total=Count('id')).order_by('pagetype')

    

    admin_obj = Admin_Login.objects.get(id=session_id)

    context = {
        "seo_pages": seo_pages,
        "type_counts": type_counts,
        'admin_obj':admin_obj
    }
    return render(request, "admin_user/Seo_Module/seo_list.html", context)


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

    session_id = request.session.get('Admin_id')
    if not session_id:
        return render(request, 'home_page/Adminlogin.html')

    admin_obj = Admin_Login.objects.get(id=session_id)

    context = {'admin_obj':admin_obj}

    return render(request, "admin_user/Seo_Module/Blog_Pages/blog_add.html",context)






def blog_list(request):

    session_id = request.session.get('Admin_id')
    if not session_id:
        return render(request, 'home_page/Adminlogin.html')
    
    admin_obj = Admin_Login.objects.get(id=session_id)
    
    blogs = Blog.objects.all().order_by("-date_posted")
    return render(request, "admin_user/Seo_Module/Blog_Pages/blog_list.html", {"blogs": blogs,'admin_obj':admin_obj})


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

    session_id = request.session.get('Admin_id')
    if not session_id:
        return render(request, 'home_page/Adminlogin.html')

    admin_obj = Admin_Login.objects.get(id=session_id)

    return render(request, "admin_user/Seo_Module/Blog_Pages/blog_edit.html", {"blog": blog,'admin_obj':admin_obj})



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

    session_id = request.session.get('Admin_id')
    if not session_id:
        return render(request, 'home_page/Adminlogin.html')

    admin_obj = Admin_Login.objects.get(id=session_id)

    context = {'admin_obj':admin_obj}

    return render(request, "admin_user/Seo_Module/Services_Pages/add_service.html",context)


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

    session_id = request.session.get('Admin_id')
    if not session_id:
        return render(request, 'home_page/Adminlogin.html')

    admin_obj = Admin_Login.objects.get(id=session_id)

    # For a GET request, pass the service object to the template
    context = {
        'service': service,
        'admin_obj':admin_obj
    }
    return render(request, "admin_user/Seo_Module/Services_Pages/edit_service.html", context)


def services_list(request):
    services = Service.objects.all().order_by('-id')

    session_id = request.session.get('Admin_id')
    if not session_id:
        return render(request, 'home_page/Adminlogin.html')

    admin_obj = Admin_Login.objects.get(id=session_id)

    return render(request, 'admin_user/Seo_Module/Services_Pages/services_list.html', {'services': services,'admin_obj':admin_obj})





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