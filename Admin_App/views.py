from django.shortcuts import render,HttpResponse
from openpyxl.styles import PatternFill, Font, Alignment, Border, Side
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
from django.db import transaction  
from django.utils import timezone
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

from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter
import csv
import json
# I added 'Sum' to the end of this line:
from django.db.models import Q, Count, Avg, Max, Min, Sum
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect

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








# Assuming CommercialRentalProperty and Admin_Login are imported





def export_commercial_rent(request):
    """Dedicated view for exporting commercial properties to CSV or Excel."""
    
    # ── 1. Re-apply the same search filters so the export matches the screen ──
    try:
        properties = CommercialRentalProperty.objects.filter(is_deleted=False).order_by('-id')
    except Exception:
        properties = CommercialRentalProperty.objects.all().order_by('-id')

    search_query    = request.GET.get('search', '').strip()
    prop_type_query = request.GET.get('property_type', '').strip()
    city_query      = request.GET.get('city', '').strip()
    zone_query      = request.GET.get('zone_type', '').strip()
    possession_query= request.GET.get('possession', '').strip()
    listed_by_query = request.GET.get('listed_by', '').strip()
    budget_query    = request.GET.get('budget', '').strip()
    from_date       = request.GET.get('from_date', '').strip()
    to_date         = request.GET.get('to_date', '').strip()

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
    if from_date:
        properties = properties.filter(created_at__date__gte=from_date)
    if to_date:
        properties = properties.filter(created_at__date__lte=to_date)
    if budget_query and budget_query != 'All Budgets':
        if budget_query == 'under_25k': properties = properties.filter(expected_rent__lt=25000)
        elif budget_query == '25k_1L': properties = properties.filter(expected_rent__gte=25000, expected_rent__lte=100000)
        elif budget_query == '1L_5L': properties = properties.filter(expected_rent__gte=100000, expected_rent__lte=500000)
        elif budget_query == 'above_5L': properties = properties.filter(expected_rent__gt=500000)

    # ── 2. Exhaustive Field Mapping (Strictly following DB sequence) ──
    EXPORT_COLS = [
        ("System Data", "id", False, "Database ID"),
        ("System Data", "commercial_rental_id", False, "System Generated ID"),
        ("System Data", "property_title", False, "Auto Generated Title"),
        ("Basic Info", "property_type", True, "office-space / shop / warehouse / industrial / land"),
        ("Basic Info", "property_condition", True, "bare-shell / warm-shell / fitted / furnished"),
        ("Basic Info", "city", True, "City name"),
        ("Basic Info", "area_locality", True, "Area/locality"),
        ("Basic Info", "property_address", True, "Complete address"),
        ("Basic Info", "building_name", True, "Building/project name"),
        ("Basic Info", "possession_status", True, "ready-to-move / under-construction"),
        ("Basic Info", "available_from", False, "YYYY-MM-DD"),
        ("Basic Info", "age_of_property", True, "0-1 / 1-3 / 3-5 / 5-10 / 10+"),
        ("Basic Info", "zone_type", False, "industrial / commercial / residential / special-economic"),
        ("Basic Info", "location_hub", False, "it-park / business-district / mall / standalone"),
        ("Basic Info", "ownership_type", True, "freehold / leasehold / co-operative"),
        ("Basic Info", "construction_status", False, "new / resale"),
        ("Area & Pricing", "builtup_area", True, "Number in sq.ft"),
        ("Area & Pricing", "carpet_area", False, "Number in sq.ft"),
        ("Area & Pricing", "expected_rent", True, "Monthly rent in ₹"),
        ("Area & Pricing", "security_deposit", False, "Deposit in ₹"),
        ("Area & Pricing", "maintenance_charges", False, "Monthly maintenance in ₹"),
        ("Area & Pricing", "negotiable", False, "Yes / No"),
        ("Area & Pricing", "brokerage", False, "Yes / No"),
        ("Area & Pricing", "brokerage_percentage", False, "1% / 1.5% / 2% / Negotiable / Manual"),
        ("Area & Pricing", "manual_brokerage", False, "e.g. 2.5%"),
        ("Area & Pricing", "dg_ups_included", False, "true / false"),
        ("Area & Pricing", "electricity_included", False, "true / false"),
        ("Area & Pricing", "water_included", False, "true / false"),
        ("Area & Pricing", "lockin_period", False, "Lock-in months"),
        ("Area & Pricing", "rent_increase", False, "% per year"),
        ("Building", "total_floors", False, "Total floors"),
        ("Building", "your_floor", False, "Floor of property"),
        ("Building", "staircases", False, "Number of staircases"),
        ("Building", "passenger_lifts", False, "Number (0 if none)"),
        ("Building", "service_lifts", False, "Number (0 if none)"),
        ("Building", "private_parking", False, "Private parking spots"),
        ("Building", "min_seats", False, "Min seating"),
        ("Building", "max_seats", False, "Max seating"),
        ("Building", "cabins", False, "Number of cabins"),
        ("Building", "meeting_rooms", False, "Number of meeting rooms"),
        ("Building", "private_washroom", False, "Number (0 if none)"),
        ("Building", "public_washroom", False, "Number (0 if none)"),
        ("Building", "flooring_type", False, "marble / vitrified / granite / wooden / ceramic"),
        ("Amenities", "amenities", True, "Comma-separated"),
        ("Amenities", "nearby_facilities", True, "Comma-separated"),
        ("Amenities", "property_summary", False, "Short description"),
        ("Amenities", "property_description", False, "Detailed description"),
        ("Media & Contact", "video", False, "Video file path"),
        ("Media & Contact", "owner_name", True, "Full name"),
        ("Media & Contact", "contact_number", True, "+91 XXXXXXXXXX"),
        ("Media & Contact", "email", True, "email@example.com"),
        ("Media & Contact", "alternate_contact", False, "+91 XXXXXXXXXX"),
        ("Uploader Tracking", "uploaded_by_name", False, "Auto-filled"),
        ("Uploader Tracking", "uploaded_by_email", False, "Auto-filled"),
        ("Uploader Tracking", "uploaded_by_contact", False, "Auto-filled"),
        ("Uploader Tracking", "uploaded_by_role", False, "Auto-filled"),
        ("System Tracking", "created_at", False, "Datetime created"),
        ("System Tracking", "is_deleted", False, "True/False"),
        ("System Tracking", "deleted_at", False, "Datetime deleted"),
        ("System Tracking", "upload_file_name", False, "Bulk upload source"),
        ("System Tracking", "upload_file_hash", False, "File hash"),
        ("System Tracking", "deleted_by", False, "Deleted by user"),
    ]

    export_format = request.GET.get('format', 'excel')

    # ── 3. EXCEL EXPORT ──
    if export_format == 'excel':
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = "Commercial Rental"

        HDR_BG  = "667EEA"
        REQ_BG  = "FEF3C7"
        OPT_BG  = "F0FDF4"
        thin = Side(style="thin", color="CBD5E1")
        bdr  = Border(left=thin, right=thin, top=thin, bottom=thin)

        sec_spans = OrderedDict()
        for i, (sec, *_) in enumerate(EXPORT_COLS):
            sec_spans.setdefault(sec, []).append(i + 1)

        for sec, cols in sec_spans.items():
            c = ws.cell(row=1, column=cols[0], value=f"📋 {sec}")
            c.font = Font(bold=True, color="FFFFFF", name="Arial", size=11)
            c.fill = PatternFill("solid", fgColor=HDR_BG)
            c.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
            c.border = bdr
            if len(cols) > 1:
                ws.merge_cells(start_row=1, start_column=cols[0], end_row=1, end_column=cols[-1])

        for ci, (sec, field, req, hint) in enumerate(EXPORT_COLS, 1):
            lc = ws.cell(row=2, column=ci, value=field + (" *" if req else ""))
            lc.font, lc.fill, lc.border = Font(bold=True, size=9), PatternFill("solid", fgColor=REQ_BG if req else OPT_BG), bdr
            lc.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)

            hc = ws.cell(row=3, column=ci, value=hint)
            hc.font, hc.fill, hc.border = Font(italic=True, color="64748B", size=8), PatternFill("solid", fgColor="FFFFFF"), bdr
            hc.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
            ws.column_dimensions[get_column_letter(ci)].width = max(18, len(field) + 4)

        for row_idx, prop in enumerate(properties, start=4):
            for col_idx, (_, field_name, _, _) in enumerate(EXPORT_COLS, start=1):
                val = getattr(prop, field_name, "")
                
                # Try to format the value, catch empty file errors safely
                try:
                    if val is True: val = "Yes"
                    elif val is False: val = "No"
                    elif hasattr(val, 'strftime'): val = val.strftime('%Y-%m-%d %H:%M')
                    elif isinstance(val, list): val = ", ".join(map(str, val))
                    elif hasattr(val, 'url'): val = val.url if val else ""
                except ValueError:
                    val = "" # If Django panics about an empty video, just leave it blank
                
                cell = ws.cell(row=row_idx, column=col_idx, value=str(val) if val is not None else "")
                cell.alignment, cell.border = Alignment(vertical="center", wrap_text=True), bdr

        ws.row_dimensions[1].height, ws.row_dimensions[2].height, ws.row_dimensions[3].height = 28, 36, 42
        ws.freeze_panes = "A4"

        buf = io.BytesIO()
        wb.save(buf)
        buf.seek(0)
        response = HttpResponse(buf.getvalue(), content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
        response["Content-Disposition"] = 'attachment; filename="Commercial_Properties.xlsx"'
        return response

    # ── 4. CSV EXPORT ──
    elif export_format == 'csv':
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="Commercial_Properties.csv"'
        writer = csv.writer(response)
        
        writer.writerow([field for _, field, _, _ in EXPORT_COLS])
        
        for prop in properties:
            row_data = []
            for _, field_name, _, _ in EXPORT_COLS:
                val = getattr(prop, field_name, "")
                
                # Try to format the value, catch empty file errors safely
                try:
                    if val is True: val = "Yes"
                    elif val is False: val = "No"
                    elif hasattr(val, 'strftime'): val = val.strftime('%Y-%m-%d %H:%M')
                    elif isinstance(val, list): val = ", ".join(map(str, val))
                    elif hasattr(val, 'url'): val = val.url if val else ""
                except ValueError:
                    val = "" # Catch empty video/image files
                    
                row_data.append(str(val) if val is not None else "")
            writer.writerow(row_data)


# Make sure you import your models here!
# from .models import CommercialRentalProperty, Admin_Login

def commercial_list(request):
    session_id = request.session.get('Admin_id')
    if not session_id:
        return render(request, 'home_page/Adminlogin.html')

    try:
        admin_obj = Admin_Login.objects.get(id=session_id)
    except Admin_Login.DoesNotExist:
        return render(request, 'home_page/Adminlogin.html')


    print(">>> YES! THE VIEW IS RUNNING! <<<")
    print(f">>> THE DOWNLOAD PARAMETER IS: {request.GET.get('download')} <<<")

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

    if budget_query and budget_query != 'All Budgets':
        if budget_query == 'under_25k':
            properties = properties.filter(expected_rent__lt=25000)
        elif budget_query == '25k_1L':
            properties = properties.filter(expected_rent__gte=25000, expected_rent__lte=100000)
        elif budget_query == '1L_5L':
            properties = properties.filter(expected_rent__gte=100000, expected_rent__lte=500000)
        elif budget_query == 'above_5L':
            properties = properties.filter(expected_rent__gt=500000)

    # ── Exhaustive Field Definition for Exports ──
    EXPORT_COLS = [
        ("System Data", "id", False, "Database ID"),
        ("System Data", "commercial_rental_id", False, "System Generated ID"),
        ("System Data", "property_title", False, "Auto Generated Title"),
        
        ("Basic Info", "property_type", True, "office-space / shop / warehouse / industrial / land"),
        ("Basic Info", "property_condition", True, "bare-shell / warm-shell / fitted / furnished"),
        ("Basic Info", "city", True, "City name"),
        ("Basic Info", "area_locality", True, "Area/locality"),
        ("Basic Info", "property_address", True, "Complete address"),
        ("Basic Info", "building_name", True, "Building/project name"),
        ("Basic Info", "possession_status", True, "ready-to-move / under-construction"),
        ("Basic Info", "available_from", False, "YYYY-MM-DD"),
        ("Basic Info", "age_of_property", True, "0-1 / 1-3 / 3-5 / 5-10 / 10+"),
        ("Basic Info", "zone_type", False, "industrial / commercial / residential / special-economic"),
        ("Basic Info", "location_hub", False, "it-park / business-district / mall / standalone"),
        ("Basic Info", "ownership_type", True, "freehold / leasehold / co-operative"),
        ("Basic Info", "construction_status", False, "new / resale"),
        
        ("Area & Pricing", "builtup_area", True, "Number in sq.ft"),
        ("Area & Pricing", "carpet_area", False, "Number in sq.ft"),
        ("Area & Pricing", "expected_rent", True, "Monthly rent in ₹"),
        ("Area & Pricing", "security_deposit", False, "Deposit in ₹"),
        ("Area & Pricing", "maintenance_charges", False, "Monthly maintenance in ₹"),
        ("Area & Pricing", "negotiable", False, "Yes / No"),
        ("Area & Pricing", "brokerage", False, "Yes / No"),
        ("Area & Pricing", "brokerage_percentage", False, "1% / 1.5% / 2% / Negotiable / Manual"),
        ("Area & Pricing", "manual_brokerage", False, "e.g. 2.5%"),
        ("Area & Pricing", "dg_ups_included", False, "true / false"),
        ("Area & Pricing", "electricity_included", False, "true / false"),
        ("Area & Pricing", "water_included", False, "true / false"),
        ("Area & Pricing", "lockin_period", False, "Lock-in months"),
        ("Area & Pricing", "rent_increase", False, "% per year"),
        
        ("Building", "total_floors", False, "Total floors"),
        ("Building", "your_floor", False, "Floor of property"),
        ("Building", "staircases", False, "Number of staircases"),
        ("Building", "passenger_lifts", False, "Number (0 if none)"),
        ("Building", "service_lifts", False, "Number (0 if none)"),
        ("Building", "private_parking", False, "Private parking spots"),
        ("Building", "min_seats", False, "Min seating"),
        ("Building", "max_seats", False, "Max seating"),
        ("Building", "cabins", False, "Number of cabins"),
        ("Building", "meeting_rooms", False, "Number of meeting rooms"),
        ("Building", "private_washroom", False, "Number (0 if none)"),
        ("Building", "public_washroom", False, "Number (0 if none)"),
        ("Building", "flooring_type", False, "marble / vitrified / granite / wooden / ceramic"),
        
        ("Amenities", "amenities", True, "Comma-separated"),
        ("Amenities", "nearby_facilities", True, "Comma-separated"),
        ("Amenities", "property_summary", False, "Short description"),
        ("Amenities", "property_description", False, "Detailed description"),
        
        ("Media & Contact", "video", False, "Video file path"),
        ("Media & Contact", "owner_name", True, "Full name"),
        ("Media & Contact", "contact_number", True, "+91 XXXXXXXXXX"),
        ("Media & Contact", "email", True, "email@example.com"),
        ("Media & Contact", "alternate_contact", False, "+91 XXXXXXXXXX"),
        
        ("Uploader Tracking", "uploaded_by_name", False, "Auto-filled"),
        ("Uploader Tracking", "uploaded_by_email", False, "Auto-filled"),
        ("Uploader Tracking", "uploaded_by_contact", False, "Auto-filled"),
        ("Uploader Tracking", "uploaded_by_role", False, "Auto-filled"),
        
        ("System Tracking", "created_at", False, "Datetime created"),
        ("System Tracking", "is_deleted", False, "True/False"),
        ("System Tracking", "deleted_at", False, "Datetime deleted"),
        ("System Tracking", "upload_file_name", False, "Bulk upload source"),
        ("System Tracking", "upload_file_hash", False, "File hash"),
        ("System Tracking", "deleted_by", False, "Deleted by user"),
    ]

    # ════════════════════════════════════════════════
    # 🛑 ROBUST EXPORT LOGIC 🛑
    # ════════════════════════════════════════════════

    # ── Excel Download ──
    if request.GET.get('download') == 'excel':
        try:
            print("--- STARTING EXCEL GENERATION ---")
            wb = openpyxl.Workbook()
            ws = wb.active
            ws.title = "Commercial Rental"

            HDR_BG  = "667EEA"
            REQ_BG  = "FEF3C7"
            OPT_BG  = "F0FDF4"
            thin = Side(style="thin", color="CBD5E1")
            bdr  = Border(left=thin, right=thin, top=thin, bottom=thin)

            # Row 1: Section Banners
            sec_spans = OrderedDict()
            for i, (sec, *_) in enumerate(EXPORT_COLS):
                sec_spans.setdefault(sec, []).append(i + 1)

            for sec, cols in sec_spans.items():
                c = ws.cell(row=1, column=cols[0], value=f"📋 {sec}")
                c.font      = Font(bold=True, color="FFFFFF", name="Arial", size=11)
                c.fill      = PatternFill("solid", fgColor=HDR_BG)
                c.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
                c.border    = bdr
                if len(cols) > 1:
                    ws.merge_cells(start_row=1, start_column=cols[0], end_row=1, end_column=cols[-1])

            # Rows 2 & 3: Labels and Hints
            for ci, (sec, field, req, hint) in enumerate(EXPORT_COLS, 1):
                lc = ws.cell(row=2, column=ci, value=field + (" *" if req else ""))
                lc.font      = Font(bold=True, color="1E293B", name="Arial", size=9)
                lc.fill      = PatternFill("solid", fgColor=REQ_BG if req else OPT_BG)
                lc.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
                lc.border    = bdr

                hc = ws.cell(row=3, column=ci, value=hint)
                hc.font      = Font(italic=True, color="64748B", name="Arial", size=8)
                hc.fill      = PatternFill("solid", fgColor="FFFFFF")
                hc.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
                hc.border    = bdr

                ws.column_dimensions[get_column_letter(ci)].width = max(18, len(field) + 4)

            print(f"--- FETCHING DATA FOR EXCEL. ROWS FOUND: {properties.count()} ---")
            # Rows 4+: Database Data Injection
            for row_idx, prop in enumerate(properties, start=4):
                for col_idx, (_, field_name, _, _) in enumerate(EXPORT_COLS, start=1):
                    val = getattr(prop, field_name, "")
                    
                    if val is True: val = "Yes"
                    elif val is False: val = "No"
                    elif hasattr(val, 'strftime'): val = val.strftime('%Y-%m-%d %H:%M')
                    elif isinstance(val, list): val = ", ".join(map(str, val))
                    elif hasattr(val, 'url'): val = val.url if val else ""
                    
                    cell = ws.cell(row=row_idx, column=col_idx, value=str(val) if val is not None else "")
                    cell.alignment = Alignment(vertical="center", wrap_text=True)
                    cell.border = bdr

            ws.row_dimensions[1].height = 28
            ws.row_dimensions[2].height = 36
            ws.row_dimensions[3].height = 42
            ws.freeze_panes = "A4"

            print("--- EXCEL FILE BUILT, SENDING RESPONSE ---")
            buf = io.BytesIO()
            wb.save(buf)
            buf.seek(0)
            
            response = HttpResponse(
                buf.getvalue(),
                content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            )
            response["Content-Disposition"] = 'attachment; filename="Commercial_Rental_Export.xlsx"'
            return response

        except Exception as e:
            # THIS IS CRITICAL: If it fails, it will output the exact error to your browser screen!
            error_msg = f"ERROR GENERATING EXCEL:\n\n{str(e)}\n\n{traceback.format_exc()}"
            print(error_msg)
            return HttpResponse(f"<pre>{error_msg}</pre>", status=500)

    # ── CSV Download ──
    if request.GET.get('download') == 'csv':
        try:
            print("--- STARTING CSV GENERATION ---")
            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename="commercial_rental_properties.csv"'
            writer = csv.writer(response)
            
            writer.writerow([field for _, field, _, _ in EXPORT_COLS])
            
            print(f"--- FETCHING DATA FOR CSV. ROWS FOUND: {properties.count()} ---")
            for prop in properties:
                row_data = []
                for _, field_name, _, _ in EXPORT_COLS:
                    val = getattr(prop, field_name, "")
                    if val is True: val = "Yes"
                    elif val is False: val = "No"
                    elif hasattr(val, 'strftime'): val = val.strftime('%Y-%m-%d %H:%M')
                    elif isinstance(val, list): val = ", ".join(map(str, val))
                    elif hasattr(val, 'url'): val = val.url if val else ""
                    row_data.append(val if val is not None else "")
                writer.writerow(row_data)
            
            print("--- CSV FILE BUILT, SENDING RESPONSE ---")
            return response
            
        except Exception as e:
            error_msg = f"ERROR GENERATING CSV:\n\n{str(e)}\n\n{traceback.format_exc()}"
            print(error_msg)
            return HttpResponse(f"<pre>{error_msg}</pre>", status=500)


    # ════════════════════════════════════════════════
    # END EXPORT LOGIC
    # ════════════════════════════════════════════════

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

    prop_type_dist = list(
        all_props.exclude(property_type__isnull=True).exclude(property_type='')
        .values('property_type').annotate(cnt=Count('id')).order_by('-cnt')[:8]
    )
    prop_type_labels_json = json.dumps([x['property_type'] for x in prop_type_dist])
    prop_type_counts_json = json.dumps([x['cnt']           for x in prop_type_dist])

    rent_range_data = {
        'Under ₹25k':  all_props.filter(expected_rent__lt=25000).count(),
        '₹25k–1L':     all_props.filter(expected_rent__gte=25000,  expected_rent__lt=100000).count(),
        '₹1L–5L':      all_props.filter(expected_rent__gte=100000, expected_rent__lt=500000).count(),
        'Above ₹5L':   all_props.filter(expected_rent__gte=500000).count(),
    }
    rent_range_labels_json = json.dumps(list(rent_range_data.keys()))
    rent_range_counts_json = json.dumps(list(rent_range_data.values()))

    occupancy_json = json.dumps([occupied_count, vacant_count, max(0, total_count - occupied_count - vacant_count)])

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

    total_tenants    = occupied_count
    collection_rate  = 0
    pending_payments = 0
    maintenance_req  = 0

    context = {
        'admin_obj': admin_obj,
        'page_obj': page_obj,

        'search_query':     search_query,
        'prop_type_query':  prop_type_query,
        'city_query':       city_query,
        'zone_query':       zone_query,
        'possession_query': possession_query,
        'listed_by_query':  listed_by_query,
        'budget_query':     budget_query,
        'from_date':        from_date,
        'to_date':          to_date,

        'unique_property_types': unique_property_types,
        'unique_cities':         unique_cities,
        'unique_zones':          unique_zones,
        'unique_possession':     unique_possession,
        'unique_roles':          unique_roles,
        'uploaded_files':        uploaded_files,

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

        'total_tenants':    total_tenants,
        'collection_rate':  collection_rate,
        'pending_payments': pending_payments,
        'maintenance_req':  maintenance_req,

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





# ─────────────────────────────────────────────────────────────
# DELETE VIEW  (POST only — called via JS fetch)
# ─────────────────────────────────────────────────────────────

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





def calculate_retention(queryset):
    now = timezone.now()
    items = list(queryset)

    for item in items:
        if item.deleted_at:
            deleted_at = item.deleted_at
            # Safeguard against offset-naive vs offset-aware datetime comparison errors
            if timezone.is_naive(deleted_at):
                deleted_at = timezone.make_aware(deleted_at)
            expiry_date = deleted_at + timedelta(days=30)
            item.days_left = max((expiry_date - now).days, 0)
        else:
            item.days_left = 30
    return items

from django.db import transaction

# ── UNIFIED GLOBAL RECYCLE BIN VIEW ──────────────────────────────────────────
def global_recycle_bin(request):
    """Unified Recycle Bin displaying deleted items from all property modules."""
    session_id = request.session.get('Admin_id')
    if not session_id:
        return render(request, 'home_page/Adminlogin.html')

    rental_deleted = calculate_retention(RentalResidentialProperty.objects.filter(is_deleted=True).order_by('-deleted_at'))
    commercial_deleted = calculate_retention(CommercialRentalProperty.objects.filter(is_deleted=True).order_by('-deleted_at'))
    pg_deleted = calculate_retention(PGColivingProperty.objects.filter(is_deleted=True).order_by('-deleted_at'))
    resale_deleted = calculate_retention(ResaleResidentialProperty.objects.filter(is_deleted=True).order_by('-deleted_at'))
    commercial_resale_deleted = calculate_retention(CommercialResaleProperty.objects.filter(is_deleted=True).order_by('-deleted_at'))
    plot_sale_deleted = calculate_retention(PlotSaleProperty.objects.filter(is_deleted=True).order_by('-deleted_at'))
    industrial_resale_deleted = calculate_retention(IndustrialResaleProperty.objects.filter(is_deleted=True).order_by('-deleted_at'))
    agricultural_resale_deleted = calculate_retention(AgriculturalResaleProperty.objects.filter(is_deleted=True).order_by('-deleted_at'))

    context = {
        'rental_deleted': rental_deleted, 'rental_count': len(rental_deleted),
        'commercial_deleted': commercial_deleted, 'commercial_count': len(commercial_deleted),
        'pg_deleted': pg_deleted, 'pg_count': len(pg_deleted),
        'resale_deleted': resale_deleted, 'resale_count': len(resale_deleted),
        'commercial_resale_deleted': commercial_resale_deleted, 'commercial_resale_count': len(commercial_resale_deleted),
        'plot_sale_deleted': plot_sale_deleted, 'plot_sale_count': len(plot_sale_deleted),
        'industrial_resale_deleted': industrial_resale_deleted, 'industrial_resale_count': len(industrial_resale_deleted),
        'agricultural_resale_deleted': agricultural_resale_deleted, 'agricultural_resale_count': len(agricultural_resale_deleted),
        'total_deleted_all': (
            len(rental_deleted) + len(commercial_deleted) + len(pg_deleted) +
            len(resale_deleted) + len(commercial_resale_deleted) + len(plot_sale_deleted) +
            len(industrial_resale_deleted) + len(agricultural_resale_deleted)
        )
    }
    return render(request, 'admin_user/Reports/Rental/global_recycle_bin.html', context)

def system_audit_logs(request):
    """A completely separate view for tracking Deletion and Restore Audit Logs."""
    session_id = request.session.get('Admin_id')
    if not session_id:
        return render(request, 'home_page/Adminlogin.html')

    admin_obj = Admin_Login.objects.get(id=session_id)
    deletion_logs = []
    restore_logs = []

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

    def get_display_id(obj):
        # Look for custom model unique IDs before falling back to PK
        id_fields = [
            'rental_residential_id', 'commercial_rental_id', 'pg_property_id', 
            'property_id', 'commercial_id', 'plot_property_id', 
            'industrial_id', 'agri_property_id'
        ]
        for field in id_fields:
            if hasattr(obj, field) and getattr(obj, field):
                return getattr(obj, field)
        return obj.pk

    def get_display_title(obj):
        if hasattr(obj, 'property_title') and obj.property_title:
            return obj.property_title
        elif hasattr(obj, 'title') and obj.title:
            return obj.title
        elif hasattr(obj, 'plot_title') and obj.plot_title:
            return obj.plot_title
        return 'N/A'

    for module_name, model in models_map.items():
        # 1. Fetch Deletion Logs
        try:
            deleted_items = model.objects.filter(is_deleted=True).exclude(deleted_at__isnull=True)
            for p in deleted_items:
                deletion_logs.append({
                    'module': module_name,
                    'id': get_display_id(p),
                    'title': get_display_title(p),
                    'by': getattr(p, 'deleted_by', 'System Admin') or 'System Admin',
                    'date': p.deleted_at
                })
        except Exception:
            pass

        # 2. Fetch Restore Logs (if restored_at is later implemented in models)
        try:
            restored_items = model.objects.filter(restored_at__isnull=False)
            for p in restored_items:
                restore_logs.append({
                    'module': module_name,
                    'id': get_display_id(p),
                    'title': get_display_title(p),
                    'by': getattr(p, 'restored_by', 'System Admin') or 'System Admin',
                    'date': p.restored_at
                })
        except Exception:
            pass

    # Sort both lists by date (Newest logs first)
    deletion_logs.sort(key=lambda x: x['date'] if x['date'] else timezone.now(), reverse=True)
    restore_logs.sort(key=lambda x: x['date'] if x['date'] else timezone.now(), reverse=True)

    context = {
        'admin_obj': admin_obj,
        'deletion_logs': deletion_logs,
        'restore_logs': restore_logs,
        'deletion_count': len(deletion_logs),
        'restore_count': len(restore_logs),
        'total_logs': len(deletion_logs) + len(restore_logs)
    }

    return render(request, 'admin_user/Reports/Rental/audit_logs.html', context)





@csrf_exempt
@require_POST
def bulk_restore_route(request, property_type):
    """
    Unified bulk-restore engine. Reverses soft-deletion status across 
    all 8 real estate modules using efficient database batch updates.
    """
    admin_id = request.session.get('Admin_id')
    if not admin_id:
        return JsonResponse({'status': 'error', 'message': 'Unauthorized access.'}, status=401)

    try:
        # Complete dictionary mapping for all active property models
        model_map = {
            'rental-residential': RentalResidentialProperty,
            'commercial': CommercialRentalProperty,
            'pg-coliving': PGColivingProperty,
            'resale-residential': ResaleResidentialProperty,
            'commercial-resale': CommercialResaleProperty,
            'plot-sale': PlotSaleProperty,
            'industrial-resale': IndustrialResaleProperty,
            'agricultural-resale': AgriculturalResaleProperty,
        }

        # Guard against invalid module requests
        if property_type not in model_map:
            return JsonResponse({
                'status': 'error', 
                'message': f'Invalid property module selector: {property_type}'
            }, status=400)

        TargetModel = model_map[property_type]
        
        # Grab only the records currently marked as soft-deleted
        deleted_queryset = TargetModel.objects.filter(is_deleted=True)
        count = deleted_queryset.count()

        if count == 0:
            readable_name = property_type.replace("-", " ").title()
            return JsonResponse({
                'status': 'success', 
                'message': f'The bin for {readable_name} has no items to restore.'
            })

        # Perform a high-speed database batch update
        deleted_queryset.update(
            is_deleted=False,
            deleted_at=None,
            deleted_by=None
        )

        return JsonResponse({
            'status': 'success',
            'message': f'Successfully restored {count} properties back to active inventory status.'
        })

    except Exception as e:
        return JsonResponse({
            'status': 'error', 
            'message': f'Database operational failure during restoration: {str(e)}'
        }, status=500)


@csrf_exempt
@require_POST
def bulk_hard_delete_properties(request, property_type):

    """
    Unified hard-delete engine. Permanently deletes soft-deleted records 
    across all 8 real estate modules and purges attached media files from disk.
    """
    admin_id = request.session.get('Admin_id')
    if not admin_id:
        return JsonResponse({'status': 'error', 'message': 'Unauthorized access.'}, status=401)

    try:
        # 1. Map endpoint slugs to their respective Models
        model_map = {
            'rental-residential': RentalResidentialProperty,
            'commercial': CommercialRentalProperty,
            'pg-coliving': PGColivingProperty,
            'resale-residential': ResaleResidentialProperty,
            'commercial-resale': CommercialResaleProperty,
            'plot-sale': PlotSaleProperty,
            'industrial-resale': IndustrialResaleProperty,   
            'agricultural-resale': AgriculturalResaleProperty,
        }

        if property_type not in model_map:
            return JsonResponse({'status': 'error', 'message': f'Invalid property module context: {property_type}'}, status=400)

        TargetModel = model_map[property_type]
        
        # 2. Grab all items waiting in the recycle bin for this specific model
        deleted_queryset = TargetModel.objects.filter(is_deleted=True)
        count = deleted_queryset.count()

        if count == 0:
            return JsonResponse({
                'status': 'success', 
                'message': f'The bin for {property_type.replace("-", " ").title()} is already completely empty.'
            })

        # 3. Media Cleanup Loop (Prevents unlinked/orphaned images/videos from filling up the disk)
        for property_obj in deleted_queryset:
            # Drop related images if the model utilizes a related images manager
            if hasattr(property_obj, 'images'):
                try:
                    for img in property_obj.images.all():
                        if img.image:
                            img.image.delete(save=False)
                except Exception:
                    pass  # Fail gracefully if relationship structure differs

            # Drop standalone video files if present
            if hasattr(property_obj, 'video') and property_obj.video:
                try:
                    property_obj.video.delete(save=False)
                except Exception:
                    pass

            # Drop standalone image files if present (e.g., plot layouts, agri maps)
            if hasattr(property_obj, 'image') and property_obj.image:
                try:
                    property_obj.image.delete(save=False)
                except Exception:
                    pass

        # 4. Wipe rows from the database permanently
        deleted_queryset.delete()

        return JsonResponse({
            'status': 'success',
            'message': f'Permanently purged {count} records and all associated assets from the database.'
        })

    except Exception as e:
        return JsonResponse({'status': 'error', 'message': f'Database operational failure: {str(e)}'}, status=500)




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













@csrf_exempt
@require_POST
def import_residential_excel(request):
    excel_file = request.FILES.get("rental_file")
    if not excel_file:
        return JsonResponse({"status": "error", "message": "No file uploaded."}, status=400)
    
    if not excel_file.name.endswith(".xlsx"):
        return JsonResponse({"status": "error", "message": "Only .xlsx files allowed."}, status=400)

    # =========================================================
    # 1. ESTABLISH UPLOADER IDENTITY (Copied from manual add)
    # =========================================================
    admin_id = request.session.get('Admin_id')
    user_id = request.session.get('User_id')

    admin_obj = None
    user_obj = None

    if admin_id:
        admin_obj = Admin_Login.objects.filter(id=admin_id).first()
    if user_id:
        user_obj = User_Details.objects.filter(id=user_id).first()

    # Default fallbacks
    uploader_name = ""
    uploader_email = ""
    uploader_contact = ""
    uploader_role = "Automated Engine"
    user_identity = "Automated Engine"

    if admin_obj:
        uploader_name = getattr(admin_obj, 'name', '') or getattr(admin_obj, 'username', '')
        uploader_email = getattr(admin_obj, 'email', '')
        uploader_contact = getattr(admin_obj, 'phone', '') or getattr(admin_obj, 'mobile', '')
        uploader_role = "Admin"
        user_identity = uploader_email or uploader_name
    elif user_obj:
        uploader_name = user_obj.user_name
        uploader_email = user_obj.user_email
        uploader_contact = user_obj.user_phone
        uploader_role = "User"
        user_identity = uploader_email or uploader_name

    # =========================================================
    # 2. PARSE EXCEL FILE
    # =========================================================
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

    # =========================================================
    # 3. DUPLICATE & OVERLAP CHECKS
    # =========================================================
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

    # =========================================================
    # 4. DATABASE WRITE & UPLOADER INJECTION
    # =========================================================
    created, updated, skipped, errors = 0, 0, 0, []
    for item in parsed_rows:
        o_data = item['data']
        r_id = item['row_id']
        
        # ---> INJECT UPLOADER DETAILS INTO THE DICTIONARY HERE <---
        o_data["upload_file_name"] = excel_file.name
        o_data["uploaded_by_name"] = uploader_name
        o_data["uploaded_by_email"] = uploader_email
        o_data["uploaded_by_contact"] = uploader_contact
        o_data["uploaded_by_role"] = uploader_role

        try:
            # Update Existing
            if r_id and r_id != "None":
                prop = RentalResidentialProperty.objects.filter(rental_residential_id=r_id).first()
                if prop:
                    for key, val in o_data.items(): setattr(prop, key, val)
                    prop.save()
                    updated += 1
                    continue

            # Create New if not Duplicate
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
    # 5. AUDIT LOGIC: File-wise Workbook Log Creation Entry
    # =====================================================
    RentalActivityLog.objects.create(
        user_identity=user_identity,
        user_role=uploader_role, # Updated to use the resolved role!
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
    # Standard security session management protocol
    session_id = request.session.get('Admin_id')
    if not session_id:
        return render(request, 'home_page/Adminlogin.html')
        
    admin_obj = Admin_Login.objects.get(id=session_id)
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

    # ═══════════════════════════════════════
    # DYNAMIC SEARCH DROPDOWN & BUDGET POPULATORS
    # ═══════════════════════════════════════
    unfiltered_base = CommercialRentalProperty.objects.filter(is_deleted=False)
    
    unique_property_types = unfiltered_base.values_list('property_type', flat=True).distinct()
    unique_cities = unfiltered_base.values_list('city', flat=True).distinct()
    unique_zones = unfiltered_base.exclude(zone_type__isnull=True).exclude(zone_type='').values_list('zone_type', flat=True).distinct()
    unique_possession = unfiltered_base.values_list('possession_status', flat=True).distinct()
    unique_roles = unfiltered_base.exclude(uploaded_by_role__isnull=True).exclude(uploaded_by_role='').values_list('uploaded_by_role', flat=True).distinct()

    # Financial Aggregations & Dynamic Budget Tier Generation
    financials = unfiltered_base.aggregate(
        avg=Avg('expected_rent'), max_r=Max('expected_rent'), min_r=Min('expected_rent'),
        total_r=Sum('expected_rent'), deposit_total=Sum('security_deposit'), area_avg=Avg('builtup_area')
    )
    
    max_rent = financials['max_r'] or 0
    min_rent = financials['min_r'] or 0

    dynamic_budgets = []
    if max_rent > 0:
        interval = (max_rent - min_rent) / 4
        if interval == 0:
            dynamic_budgets.append({
                'value': 'tier_1', 
                'label': f"Up to ₹{int(max_rent):,}", 
                'min': 0, 'max': max_rent
            })
        else:
            b1 = min_rent + interval
            b2 = min_rent + (interval * 2)
            b3 = min_rent + (interval * 3)

            dynamic_budgets = [
                {'value': 'tier_1', 'label': f"Under ₹{int(b1):,}", 'min': 0, 'max': b1},
                {'value': 'tier_2', 'label': f"₹{int(b1):,} – ₹{int(b2):,}", 'min': b1, 'max': b2},
                {'value': 'tier_3', 'label': f"₹{int(b2):,} – ₹{int(b3):,}", 'min': b2, 'max': b3},
                {'value': 'tier_4', 'label': f"Above ₹{int(b3):,}", 'min': b3, 'max': max_rent * 10}
            ]

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

    # Dynamic Budget Range Filter Lookup Execution
    if budget_query and budget_query != "All Budgets":
        for bucket in dynamic_budgets:
            if budget_query == bucket['value']:
                properties = properties.filter(expected_rent__gte=bucket['min'], expected_rent__lte=bucket['max'])
                break

    # Created At Date Filter Ranges
    if from_date_str:
        f_date = parse_date(from_date_str)
        if f_date:
            properties = properties.filter(created_at__date__gte=f_date)

    if to_date_str:
        t_date = parse_date(to_date_str)
        if t_date:
            properties = properties.filter(created_at__date__lte=t_date)

    properties = properties.order_by('-id')

    # KPI Dashboards metrics logic
    total_properties = unfiltered_base.count()
    active_listings = unfiltered_base.count()
    occupied_count = unfiltered_base.filter(possession_status__icontains="occupied").count()
    vacant_count = unfiltered_base.filter(possession_status__icontains="ready").count()
    occupancy_rate = round((occupied_count / total_properties * 100), 1) if total_properties > 0 else 0
    vacancy_rate = round((vacant_count / total_properties * 100), 1) if total_properties > 0 else 0

    avg_rent = financials['avg'] or 0
    max_rent = financials['max_r'] or 0
    min_rent = financials['min_r'] or 0
    total_revenue = financials['total_r'] or 0
    total_security_deposit = financials['deposit_total'] or 0
    avg_area = financials['area_avg'] or 0

    ready_to_move_count = vacant_count
    premium_properties_count = unfiltered_base.filter(expected_rent__gte=100000).count()
    affordable_properties_count = unfiltered_base.filter(expected_rent__lt=25000).count()
    short_lease_count = unfiltered_base.filter(lockin_period__lte=6).count()
    long_lease_count = unfiltered_base.filter(lockin_period__gt=11).count()
    with_images_count = unfiltered_base.filter(images__isnull=False).distinct().count()
    with_owner_count = unfiltered_base.exclude(owner_name__isnull=True).exclude(owner_name='').count()
    image_pct = round((with_images_count / total_properties * 100), 1) if total_properties > 0 else 0
    verified_pct = round((with_owner_count / total_properties * 100), 1) if total_properties > 0 else 0

    total_tenants = occupied_count
    collection_rate = 98
    pending_payments = unfiltered_base.filter(possession_status__icontains="dispute").count()
    maintenance_req = unfiltered_base.filter(maintenance_charges__gt=0).count()

    # Chart Serialization Lookups
    pt_qs = unfiltered_base.values('property_type').annotate(count=Count('id')).order_by('-count')
    prop_type_labels_json = json.dumps([item['property_type'].replace('-', ' ').title() for item in pt_qs])
    prop_type_counts_json = json.dumps([item['count'] for item in pt_qs])

    city_qs = unfiltered_base.values('city').annotate(revenue=Sum('expected_rent')).order_by('-revenue')[:6]
    monthly_labels_json = json.dumps([item['city'] for item in city_qs])
    monthly_revenue_json = json.dumps([float(item['revenue'] or 0) for item in city_qs])
    occupancy_json = json.dumps([occupied_count, vacant_count, total_properties - (occupied_count + vacant_count)])

    rent_buckets = [
        ('Under 25k', unfiltered_base.filter(expected_rent__lt=25000).count()),
        ('25k - 1L', unfiltered_base.filter(expected_rent__gte=25000, expected_rent__lte=100000).count()),
        ('1L - 5L', unfiltered_base.filter(expected_rent__gte=100000, expected_rent__lte=500000).count()),
        ('Above 5L', unfiltered_base.filter(expected_rent__gt=500000).count()),
    ]
    rent_range_labels_json = json.dumps([b[0] for b in rent_buckets])
    rent_range_counts_json = json.dumps([b[1] for b in rent_buckets])

    try:
        uploaded_files = unfiltered_base.exclude(upload_file_name__isnull=True).exclude(upload_file_name='').values_list('upload_file_name', flat=True).distinct()
    except Exception:
        uploaded_files = []

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
        'dynamic_budgets': dynamic_budgets,  # Added Context

        # Metrics & KPI Bindings
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





# Make sure your models are imported
# from .models import PGColivingProperty, PGRoomDetail




def export_pg_coliving(request):
    """Dedicated view for exporting PG/Coliving properties to CSV or Excel with System Meta."""
    
    try:
        properties = PGColivingProperty.objects.filter(is_deleted=False).order_by('-created_at')
    except Exception:
        properties = PGColivingProperty.objects.all().order_by('-created_at')

    # ── Apply Search Filters ──
    search_query = request.GET.get('search', '').strip()
    city_query   = request.GET.get('city', '').strip()
    pg_for_query = request.GET.get('pg_for', '').strip()
    from_date    = request.GET.get('from_date', '').strip()
    to_date      = request.GET.get('to_date', '').strip()

    if search_query:
        properties = properties.filter(
            Q(property_title__icontains=search_query) |
            Q(building_name__icontains=search_query) |
            Q(locality__icontains=search_query) |
            Q(city__icontains=search_query) |
            Q(owner_name__icontains=search_query)
        )
    if city_query and city_query != 'All Cities':
        properties = properties.filter(city__icontains=city_query)
    if pg_for_query and pg_for_query != 'All Types':
        properties = properties.filter(pg_for__icontains=pg_for_query)
    if from_date:
        properties = properties.filter(created_at__date__gte=from_date)
    if to_date:
        properties = properties.filter(created_at__date__lte=to_date)

    # ── EXACT MATCH TO IMPORT SEQUENCE + SYSTEM META FOR AUDIT ──
    EXPORT_COLS = [
        ("⚙️ System Meta", "pg_property_id", False, "Auto Generated Property pg ID"),
        ("📋 Basic Info", "property_title", False, "Property Title/Auto Generated"),
        ("📋 Basic Info", "city", True, "city *"),
        ("📋 Basic Info", "building_name", False, "building / project name"),
        ("📋 Basic Info", "locality", True, "locality *"),
       
        ("📋 Basic Info", "property_address", True, "property address *"),
        ("📋 Basic Info", "total_beds", True, "total beds *"),
        ("📋 Basic Info", "pg_for", True, "pg for * (boys/girls/co_living)"),
        ("📋 Basic Info", "furnishing_type", True, "furnishing type * (fully-furnished/semi-furnished/unfurnished)"),
        ("📋 Basic Info", "sharing_type", False, "sharing type"),
        ("📋 Basic Info", "best_suited_for", False, "best suited for (students/working professionals/any)"),
      
        ("📋 Basic Info", "meals_available", False, "meals available? (true/false)"),
        ("📋 Basic Info", "meal_offerings", False, "meal offerings (breakfast,lunch,dinner)"),
        ("📋 Basic Info", "meal_speciality", False, "meal speciality (veg/non-veg/both)"),
    
        ("📋 Basic Info", "notice_period", False, "notice period (days)"),
        ("📋 Basic Info", "lockin_period", False, "lock-in period (days)"),
        ("📋 Basic Info", "minimum_stay", True, "minimum stay (months) *"),
        ("📋 Basic Info", "available_from", True, "available from * (yyyy-mm-dd)"),
        ("📋 Basic Info", "property_managed_by", False, "property managed by (owner/caretaker)"),
        ("📋 Basic Info", "manager_stays", False, "property manager stays at property? (true/false)"),
        

        ("🛏 Room 1", "room_type_1", True, "room_type_1 *"),
        ("🛏 Room 1", "room_beds_1", True, "room_beds_1 *"),
        ("🛏 Room 1", "room_rent_1", True, "room_rent_1 *"),
        ("🛏 Room 1", "room_deposit_1", True, "room_deposit_1 *"),
        ("🛏 Room 1", "room_brokerage_1", False, "room_brokerage_1"),
        ("🛏 Room 1", "room_brokerage_percent_1", False, "room_brokerage_percent_1"),
        ("🛏 Room 1", "room_manual_brokerage_1", False, "room_manual_brokerage_1"),
        ("🛏 Room 1", "room_facilities_1", False, "room_facilities_1"),

        ("🛏 Room 2", "room_type_2", False, "room_type_2"),
        ("🛏 Room 2", "room_beds_2", False, "room_beds_2"),
        ("🛏 Room 2", "room_rent_2", False, "room_rent_2"),
        ("🛏 Room 2", "room_deposit_2", False, "room_deposit_2"),
        ("🛏 Room 2", "room_brokerage_2", False, "room_brokerage_2"),
        ("🛏 Room 2", "room_brokerage_percent_2", False, "room_brokerage_percent_2"),
        ("🛏 Room 2", "room_manual_brokerage_2", False, "room_manual_brokerage_2"),
        ("🛏 Room 2", "room_facilities_2", False, "room_facilities_2"),

        

        ("📏 PG Regulations", "opposite_sex_allowed", False, "opposite sex allowed? (true/false)"),
        ("📏 PG Regulations", "any_time_allowed", False, "any time allowed? (true/false)"),
        ("📏 PG Regulations", "visitors_allowed", False, "visitors allowed? (true/false)"),
        ("📏 PG Regulations", "guardian_allowed", False, "guardian allowed? (true/false)"),
        ("📏 PG Regulations", "drinking_allowed", False, "drinking allowed? (true/false)"),
        ("📏 PG Regulations", "smoking_allowed", False, "smoking allowed? (true/false)"),

        ("🏷 Property Description & Amenties", "property_description", False, "property description"),
        ("🏷 Property Description & Amenties", "amenities", False, "amenities (wifi,cctv,geyser,...)"),
        ("🏷 Property Description & Amenties", "nearby_facilities", False, "nearby facilities (college,market,...)"),

        ("📞 Contact Info", "owner_name", True, "owner name *"),
        ("📞 Contact Info", "contact_number", True, "contact number *"),
        ("📞 Contact Info", "email", True, "email *"),
        ("📞 Contact Info", "alternate_contact", False, "alternate contact"),

        # 🛑 AUDIT LOG SYSTEM FIELDS 🛑
     
        ("⚙️ System Meta", "uploaded_by_name", False, "uploaded by (name)"),
        ("⚙️ System Meta", "uploaded_by_email", False, "uploaded by (email)"),
        ("⚙️ System Meta", "uploaded_by_role", False, "uploader role"),
        ("⚙️ System Meta", "uploaded_by_contact", False, "uploader contact"),
        ("⚙️ System Meta", "upload_file_name", False, "source file name"),
        ("⚙️ System Meta", "created_at", False, "record created at"),
        ("⚙️ System Meta", "updated_at", False, "record updated at"),
        ("⚙️ System Meta", "is_deleted", False, "is deleted? (true/false)"),
        ("⚙️ System Meta", "deleted_at", False, "deleted at timestamp"),
        ("⚙️ System Meta", "deleted_by", False, "deleted by user"),
    ]

    export_format = request.GET.get('format', 'excel')

    # ── EXCEL EXPORT ──
    if export_format == 'excel':
        try:
            wb = openpyxl.Workbook()
            ws = wb.active
            ws.title = "PG Listings Export"

            HDR_BG, ROOM1_BG, ROOM2_BG = "1F4E79", "2E75B6", "5B9BD5"
            META_BG = "475569"
            REQ_BG, OPT_BG = "FFD7D7", "DDEBF7"
            thin = Side(style="thin", color="BBBBBB")
            bdr  = Border(left=thin, right=thin, top=thin, bottom=thin)

            # Group column headers into contiguous chunks to separate System Meta sections cleanly
            contiguous_sections = []
            for i, (sec, *_) in enumerate(EXPORT_COLS):
                col_idx = i + 1
                if not contiguous_sections or contiguous_sections[-1]['sec'] != sec:
                    contiguous_sections.append({'sec': sec, 'start': col_idx, 'end': col_idx})
                else:
                    contiguous_sections[-1]['end'] = col_idx

            # Draw Banners
            for item in contiguous_sections:
                sec = item['sec']
                start_col = item['start']
                end_col = item['end']

                if "Room 1" in sec: 
                    fill_color = ROOM1_BG
                elif "Room 2" in sec: 
                    fill_color = ROOM2_BG
                elif "System Meta" in sec: 
                    fill_color = META_BG
                else: 
                    fill_color = HDR_BG

                # Style cells across the range first to avoid styling MergedCells safely
                for col in range(start_col, end_col + 1):
                    cell = ws.cell(row=1, column=col)
                    cell.fill = PatternFill("solid", fgColor=fill_color)
                    cell.border = bdr

                # Put text & configurations inside the main tracking cell
                top_cell = ws.cell(row=1, column=start_col)
                top_cell.value = sec
                top_cell.font = Font(bold=True, color="FFFFFF", size=10)
                top_cell.alignment = Alignment(horizontal="center", vertical="center")

                if start_col < end_col:
                    ws.merge_cells(start_row=1, start_column=start_col, end_row=1, end_column=end_col)

            # Draw Headers
            for ci, (sec, field, req, hint) in enumerate(EXPORT_COLS, 1):
                lc = ws.cell(row=2, column=ci, value=hint) 
                lc.font, lc.border = Font(bold=True, size=9), bdr
                lc.fill = PatternFill("solid", fgColor=REQ_BG if req else OPT_BG)
                lc.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
                ws.column_dimensions[get_column_letter(ci)].width = max(18, len(hint) * 0.9)

            # Process Data
            for row_idx, prop in enumerate(properties, start=3):
                rooms = list(prop.rooms.all().order_by('id'))
                room1 = rooms[0] if len(rooms) > 0 else None
                room2 = rooms[1] if len(rooms) > 1 else None

                for col_idx, (_, field_name, _, _) in enumerate(EXPORT_COLS, start=1):
                    val = ""
                    if field_name.endswith("_1") and room1: val = getattr(room1, field_name.replace("_1", ""), "")
                    elif field_name.endswith("_2") and room2: val = getattr(room2, field_name.replace("_2", ""), "")
                    elif hasattr(prop, field_name): val = getattr(prop, field_name, "")
                    
                    try:
                        if val is True: val = "True"
                        elif val is False: val = "False"
                        elif hasattr(val, 'strftime'): 
                            val = val.strftime('%Y-%m-%d %H:%M:%S') if "at" in field_name else val.strftime('%Y-%m-%d')
                        elif isinstance(val, list): val = ", ".join(map(str, val))
                        elif hasattr(val, 'url'): val = val.url if val else ""
                    except ValueError: val = ""
                    
                    cell = ws.cell(row=row_idx, column=col_idx, value=str(val) if val is not None else "")
                    cell.alignment, cell.border = Alignment(vertical="center", wrap_text=True), bdr

            ws.row_dimensions[1].height, ws.row_dimensions[2].height = 28, 36
            ws.freeze_panes = "A3"

            buf = io.BytesIO()
            wb.save(buf)
            buf.seek(0)
            response = HttpResponse(buf.getvalue(), content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
            response["Content-Disposition"] = 'attachment; filename="PG_Coliving_Export_With_Audit.xlsx"'
            return response
            
        except Exception as e:
            return HttpResponse(f"<pre>ERROR GENERATING EXCEL:\n{str(e)}\n{traceback.format_exc()}</pre>", status=500)

    # ── CSV EXPORT ──
    elif export_format == 'csv':
        try:
            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename="PG_Coliving_Export_With_Audit.csv"'
            writer = csv.writer(response)
            
            writer.writerow([hint for _, _, _, hint in EXPORT_COLS])
            
            for prop in properties:
                rooms = list(prop.rooms.all().order_by('id'))
                room1 = rooms[0] if len(rooms) > 0 else None
                room2 = rooms[1] if len(rooms) > 1 else None

                row_data = []
                for _, field_name, _, _ in EXPORT_COLS:
                    val = ""
                    if field_name.endswith("_1") and room1: val = getattr(room1, field_name.replace("_1", ""), "")
                    elif field_name.endswith("_2") and room2: val = getattr(room2, field_name.replace("_2", ""), "")
                    elif hasattr(prop, field_name): val = getattr(prop, field_name, "")
                    
                    try:
                        if val is True: val = "True"
                        elif val is False: val = "False"
                        elif hasattr(val, 'strftime'): 
                            val = val.strftime('%Y-%m-%d %H:%M:%S') if "at" in field_name else val.strftime('%Y-%m-%d')
                        elif isinstance(val, list): val = ", ".join(map(str, val))
                        elif hasattr(val, 'url'): val = val.url if val else ""
                    except ValueError: val = ""
                        
                    row_data.append(str(val) if val is not None else "")
                writer.writerow(row_data)
                
            return response
            
        except Exception as e:
            return HttpResponse(f"<pre>ERROR GENERATING CSV:\n{str(e)}\n{traceback.format_exc()}</pre>", status=500)

def pg_list(request):
    session_id = request.session.get('Admin_id')

    if not session_id:
        return render(request, 'home_page/Adminlogin.html')

    admin_obj = Admin_Login.objects.get(id=session_id)

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
    all_props  = PGColivingProperty.objects.filter(is_deleted=False)
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

    # ══════════════════════════════════════════════════════════════
    # EXPORT HELPERS  (shared by both Excel & CSV)
    # ══════════════════════════════════════════════════════════════
    EXPORT_HEADERS = [
        "pg_property_id", "property_title", "city", "building_name",
        "locality", "property_address", "total_beds", "pg_for",
        "furnishing_type", "sharing_type", "best_suited_for",
        # Room 1
        "room_type_1", "room_beds_1", "room_rent_1", "room_deposit_1",
        "room_brokerage_1", "room_brokerage_percent_1",
        "room_manual_brokerage_1", "room_facilities_1",
        # Room 2
        "room_type_2", "room_beds_2", "room_rent_2", "room_deposit_2",
        "room_brokerage_2", "room_brokerage_percent_2",
        "room_manual_brokerage_2", "room_facilities_2",
        # Meals
        "meals_available", "meal_offerings", "meal_speciality",
        # Rules
        "notice_period", "lockin_period", "minimum_stay",
        "available_from", "property_managed_by", "manager_stays",
        "opposite_sex_allowed", "any_time_allowed", "visitors_allowed",
        "guardian_allowed", "drinking_allowed", "smoking_allowed",
        # Amenities
        "property_description", "amenities", "nearby_facilities",
        # Contact
        "owner_name", "contact_number", "email", "alternate_contact",
        # Uploader
        "uploaded_by_name", "uploaded_by_email",
        "uploaded_by_contact", "uploaded_by_role",
        # Audit
        "upload_file_name", "created_at",
    ]

    def _room_slot(rooms_list, idx):
        """Return flat dict for a room slot (0-based idx)."""
        n = idx + 1
        r = rooms_list[idx] if idx < len(rooms_list) else None
        if r:
            return {
                f"room_type_{n}":              r.room_type,
                f"room_beds_{n}":              r.room_beds,
                f"room_rent_{n}":              r.room_rent,
                f"room_deposit_{n}":           r.room_deposit,
                f"room_brokerage_{n}":         r.room_brokerage,
                f"room_brokerage_percent_{n}": r.room_brokerage_percent or "",
                f"room_manual_brokerage_{n}":  r.room_manual_brokerage or "",
                f"room_facilities_{n}":        r.room_facilities or "",
            }
        return {f"room_type_{n}": "", f"room_beds_{n}": "", f"room_rent_{n}": "",
                f"room_deposit_{n}": "", f"room_brokerage_{n}": "",
                f"room_brokerage_percent_{n}": "", f"room_manual_brokerage_{n}": "",
                f"room_facilities_{n}": ""}

    def _build_export_rows(qs):
        """Build list-of-dicts for export from the given queryset."""
        rows = []
        for prop in qs.prefetch_related('rooms'):
            rooms_list = list(prop.rooms.all())
            row = {
                "pg_property_id":       prop.pg_property_id,
                "property_title":       prop.property_title or "",
                "city":                 prop.city,
                "building_name":        prop.building_name or "",
                "locality":             prop.locality,
                "property_address":     prop.property_address,
                "total_beds":           prop.total_beds,
                "pg_for":               prop.pg_for,
                "furnishing_type":      prop.furnishing_type,
                "sharing_type":         prop.sharing_type or "",
                "best_suited_for":      prop.best_suited_for or "",
                **_room_slot(rooms_list, 0),
                **_room_slot(rooms_list, 1),
                "meals_available":      prop.meals_available,
                "meal_offerings":       prop.meal_offerings or "",
                "meal_speciality":      prop.meal_speciality or "",
                "notice_period":        prop.notice_period or "",
                "lockin_period":        prop.lockin_period or "",
                "minimum_stay":         prop.minimum_stay,
                "available_from":       prop.available_from.strftime("%Y-%m-%d") if prop.available_from else "",
                "property_managed_by":  prop.property_managed_by or "",
                "manager_stays":        prop.manager_stays,
                "opposite_sex_allowed": prop.opposite_sex_allowed,
                "any_time_allowed":     prop.any_time_allowed,
                "visitors_allowed":     prop.visitors_allowed,
                "guardian_allowed":     prop.guardian_allowed,
                "drinking_allowed":     prop.drinking_allowed,
                "smoking_allowed":      prop.smoking_allowed,
                "property_description": prop.property_description or "",
                "amenities":            prop.amenities or "",
                "nearby_facilities":    prop.nearby_facilities or "",
                "owner_name":           prop.owner_name,
                "contact_number":       prop.contact_number,
                "email":                prop.email,
                "alternate_contact":    prop.alternate_contact or "",
                "uploaded_by_name":     prop.uploaded_by_name or "",
                "uploaded_by_email":    prop.uploaded_by_email or "",
                "uploaded_by_contact":  prop.uploaded_by_contact or "",
                "uploaded_by_role":     prop.uploaded_by_role or "",
                "upload_file_name":     prop.upload_file_name or "",
                "created_at":           prop.created_at.strftime("%Y-%m-%d %H:%M") if prop.created_at else "",
            }
            rows.append(row)
        return rows

    # ── EXCEL DOWNLOAD ────────────────────────────────────────────────────────
    if request.GET.get('download') == 'excel':
        from openpyxl.styles import Font, PatternFill, Alignment
        from openpyxl.utils import get_column_letter

        rows = _build_export_rows(properties)

        wb  = openpyxl.Workbook()
        ws  = wb.active
        ws.title = "PG Listings"

        HDR_FILL   = PatternFill("solid", start_color="1F4E79")
        ROOM1_FILL = PatternFill("solid", start_color="2E75B6")
        ROOM2_FILL = PatternFill("solid", start_color="5B9BD5")
        HDR_FONT   = Font(bold=True, color="FFFFFF", size=10)
        COL_FONT   = Font(bold=True, size=9)
        CENTER     = Alignment(horizontal="center", vertical="center", wrap_text=True)

        # Row 1 — section labels
        section_map = [
            (1,  11, "📋 Basic Info"),
            (12, 19, "🛏 Room 1"),
            (20, 27, "🛏 Room 2"),
            (28, 30, "🍽 Meals"),
            (31, 42, "📏 Rules"),
            (43, 45, "🏷 Amenities"),
            (46, 49, "📞 Contact"),
            (50, 53, "👤 Uploader"),
            (54, 55, "📁 Audit"),
        ]
        for sc, ec, label in section_map:
            ws.merge_cells(start_row=1, start_column=sc, end_row=1, end_column=ec)
            c = ws.cell(row=1, column=sc, value=label)
            c.fill = ROOM1_FILL if "Room 1" in label else ROOM2_FILL if "Room 2" in label else HDR_FILL
            c.font = HDR_FONT
            c.alignment = CENTER

        # Row 2 — column headers
        ROOM1_CI = set(range(12, 20))
        ROOM2_CI = set(range(20, 28))
        for ci, h in enumerate(EXPORT_HEADERS, 1):
            c = ws.cell(row=2, column=ci, value=h)
            c.font = COL_FONT
            c.alignment = CENTER
            if ci in ROOM1_CI:
                c.fill = PatternFill("solid", start_color="DDEEFF")
            elif ci in ROOM2_CI:
                c.fill = PatternFill("solid", start_color="EEE8FF")
            else:
                c.fill = PatternFill("solid", start_color="F0F4FF")

        # Data rows from row 3
        for row in rows:
            ws.append([row.get(h, "") for h in EXPORT_HEADERS])

        ws.row_dimensions[1].height = 20
        ws.row_dimensions[2].height = 30
        ws.freeze_panes = "A3"

        for ci, h in enumerate(EXPORT_HEADERS, 1):
            cl = get_column_letter(ci)
            if any(k in h for k in ("address", "description", "facilities")):
                ws.column_dimensions[cl].width = 30
            elif any(k in h for k in ("brokerage_percent", "manual_brokerage")):
                ws.column_dimensions[cl].width = 22
            else:
                ws.column_dimensions[cl].width = max(15, len(h) * 0.9)

        buf = io.BytesIO()
        wb.save(buf)
        buf.seek(0)
        response = HttpResponse(
            buf.read(),
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        response['Content-Disposition'] = 'attachment; filename="pg_listings_export.xlsx"'
        return response

    # ── CSV DOWNLOAD ──────────────────────────────────────────────────────────
    if request.GET.get('download') == 'csv':
        rows = _build_export_rows(properties)
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="pg_listings_export.csv"'
        writer = csv.writer(response)
        writer.writerow(EXPORT_HEADERS)
        for row in rows:
            writer.writerow([row.get(h, "") for h in EXPORT_HEADERS])
        return response

    # ── PAGINATION SYSTEM ──
    paginator = Paginator(properties, 10)
    page_obj  = paginator.get_page(request.GET.get('page', 1))

    # ── SUMMARY CARD KPI AGGREGATIONS ──
    total_count    = properties.count()
    boys_count     = properties.filter(pg_for__iexact='Boys').count()
    girls_count    = properties.filter(pg_for__iexact='Girls').count()
    coliving_count = properties.filter(pg_for__iexact='Co-living').count()
    total_beds     = properties.aggregate(t=Sum('total_beds'))['t'] or 0
    city_count     = properties.values('city').distinct().count()

    boys_pct     = round((boys_count    / total_count * 100), 1) if total_count else 0
    girls_pct    = round((girls_count   / total_count * 100), 1) if total_count else 0
    coliving_pct = round((coliving_count/ total_count * 100), 1) if total_count else 0

    rent_stats = PGRoomDetail.objects.filter(property__in=properties).aggregate(
        avg_rent=Avg('room_rent'), max_rent=Max('room_rent'), min_rent=Min('room_rent'),
        avg_dep=Avg('room_deposit'), tot_rev=Sum('room_rent'), tot_dep=Sum('room_deposit')
    )

    meals_available_count = properties.filter(meals_available=True).count()
    meals_pct     = round((meals_available_count / total_count * 100), 1) if total_count else 0
    furnished_count = properties.filter(furnishing_type__icontains='Fully').count()
    furnished_pct   = round((furnished_count / total_count * 100), 1) if total_count else 0
    single_room_count = properties.filter(rooms__room_type__iexact='single').distinct().count()
    shared_room_count = properties.filter(rooms__room_type__in=['double','triple','quad']).distinct().count()
    anytime_entry   = properties.filter(any_time_allowed=True).count()
    visitors_allowed= properties.filter(visitors_allowed=True).count()
    premium_pg_count= properties.filter(rooms__room_rent__gte=10000).distinct().count()
    budget_pg_count = properties.filter(rooms__room_rent__lt=5000).distinct().count()
    with_owner_count= properties.exclude(owner_name='').count()
    try:
        with_images_count = properties.filter(images__isnull=False).distinct().count()
    except Exception:
        with_images_count = 0

    uploaded_files = PGColivingProperty.objects.filter(
        is_deleted=False, upload_file_name__isnull=False
    ).exclude(upload_file_name='').values_list('upload_file_name', flat=True).distinct().order_by('upload_file_name')

    # ── CHARTS ──
    pg_for_qs     = properties.values('pg_for').annotate(c=Count('pg_property_id')).order_by('-c')
    pg_for_labels = json.dumps([i['pg_for'] for i in pg_for_qs])
    pg_for_data   = json.dumps([i['c']      for i in pg_for_qs])

    rent_buckets      = [('Under ₹3k',0,3000),('₹3k–5k',3000,5000),('₹5k–8k',5000,8000),('₹8k–12k',8000,12000),('Above ₹12k',12000,999999)]
    rent_range_labels = json.dumps([b[0] for b in rent_buckets])
    rent_range_data   = json.dumps([properties.filter(rooms__room_rent__gte=lo, rooms__room_rent__lt=hi).distinct().count() for _, lo, hi in rent_buckets])

    furnish_qs       = properties.values('furnishing_type').annotate(c=Count('pg_property_id')).order_by('-c')
    furnishing_labels= json.dumps([i['furnishing_type'] for i in furnish_qs])
    furnishing_data  = json.dumps([i['c']               for i in furnish_qs])

    city_qs     = properties.values('city').annotate(c=Count('pg_property_id')).order_by('-c')[:5]
    city_labels = json.dumps([i['city'] for i in city_qs])
    city_data   = json.dumps([i['c']    for i in city_qs])

    cities = all_props.values_list('city', flat=True).distinct().order_by('city')

    return render(request, 'admin_user/Reports/Rental/pg_list.html', {'admin_obj': admin_obj,
        'page_obj': page_obj, 'search_query': search_query, 'pg_for_filter': pg_for_filter,
        'city_filter': city_filter, 'furnish_filter': furnish_filter, 'meals_filter': meals_filter,
        'sharing_filter': sharing_filter, 'from_date': from_date, 'to_date': to_date, 'cities': cities,
        'total_count': total_count, 'city_count': city_count, 'boys_count': boys_count,
        'girls_count': girls_count, 'coliving_count': coliving_count, 'total_beds': total_beds,
        'boys_pct': boys_pct, 'girls_pct': girls_pct, 'coliving_pct': coliving_pct,
        'avg_rent': rent_stats['avg_rent'] or 0, 'max_rent': rent_stats['max_rent'] or 0,
        'min_rent': rent_stats['min_rent'] or 0, 'total_revenue': rent_stats['tot_rev'] or 0,
        'total_deposit': rent_stats['tot_dep'] or 0, 'avg_deposit': rent_stats['avg_dep'] or 0,
        'meals_available_count': meals_available_count, 'meals_pct': meals_pct,
        'furnished_count': furnished_count, 'furnished_pct': furnished_pct,
        'single_room_count': single_room_count, 'shared_room_count': shared_room_count,
        'non_veg_allowed': meals_available_count, 'with_images_count': with_images_count,
        'anytime_entry': anytime_entry, 'visitors_allowed': visitors_allowed,
        'premium_pg_count': premium_pg_count, 'budget_pg_count': budget_pg_count,
        'with_owner_count': with_owner_count, 'uploaded_files': uploaded_files,
        'pg_for_labels': pg_for_labels, 'pg_for_data': pg_for_data,
        'rent_range_labels': rent_range_labels, 'rent_range_data': rent_range_data,
        'furnishing_labels': furnishing_labels, 'furnishing_data': furnishing_data,
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









@csrf_exempt
@require_POST
def pg_bulk_delete(request):
    """Handles Dashboard side bulk deletion by transforming actions to secure SOFT DELETES."""
    # Assuming standard session check or your local _get_admin helper logic
    admin_id = request.session.get('Admin_id')
    if not admin_id:
        return JsonResponse({'status': 'error', 'message': 'Unauthorized access.'}, status=401)

    try:
        # Gracefully handle missing or empty payloads
        if not request.body:
            return JsonResponse({'status': 'error', 'message': 'Empty request body payload.'}, status=400)
            
        data = json.loads(request.body)
        delete_type = data.get('delete_type')
        
        # Target only active, live properties for dashboard actions
        properties = PGColivingProperty.objects.filter(is_deleted=False)
        target_props = properties.none()

        if delete_type == 'delete_all':
            target_props = properties

        elif delete_type == 'current_page':
            page_ids = data.get('page_ids', [])
            target_props = properties.filter(pg_property_id__in=page_ids)

        elif delete_type == 'date_range':
            from_date = data.get('from_date')
            to_date = data.get('to_date')
            target_props = properties.filter(created_at__date__range=[from_date, to_date])

        elif delete_type == 'latest_month':
            thirty_days_ago = timezone.now() - timedelta(days=30)
            target_props = properties.filter(created_at__gte=thirty_days_ago)

        elif delete_type == 'old_data':
            six_months_ago = timezone.now() - timedelta(days=180)
            target_props = properties.filter(created_at__lt=six_months_ago)

        elif delete_type == 'by_uploader':
            uploader = data.get('uploader_text', '')
            target_props = properties.filter(
                Q(uploaded_by_name__icontains=uploader) |
                Q(uploaded_by_email__icontains=uploader) |
                Q(uploaded_by_contact__icontains=uploader) |
                Q(owner_name__icontains=uploader)
            )

        elif delete_type == 'by_file':
            file_name = data.get('file_name', '')
            target_props = properties.filter(upload_file_name=file_name)
        else:
            return JsonResponse({'status': 'error', 'message': 'Unknown delete criteria.'}, status=400)

        count = target_props.count()
        if count == 0:
            return JsonResponse({'status': 'success', 'message': 'No matching active records found to process.'})

        # 🚀 FIX: Convert to Soft Delete so records actually land in your Global Recycle Bin
        target_props.update(
            is_deleted=True,
            deleted_at=timezone.now(),
            deleted_by=request.session.get('Admin_username', 'System Admin')
        )

        return JsonResponse({
            'status': 'success',
            'message': f'Successfully moved {count} PG properties to the Recycle Bin.'
        })

    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)





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
    ("pg name *",                                                           "property_title",       _str,  False),
    ("property address *",                                                  "property_address",     _str,  False),
    ("total beds *",                                                        "total_beds",           _int,  False),
    ("pg for * (boys/girls/co_living)",                                          "pg_for",               _str,  False),
    ("furnishing type * (fully-furnished/semi-furnished/unfurnished)",      "furnishing_type",      _str,  False),
    ("best suited for (students/working professionals/any)",                "best_suited_for",      _str,  False),
    ("property managed by (owner/caretaker)",                               "property_managed_by",  _str,  False),
    ("property manager stays at property? (true/false)",                    "manager_stays",        _bool, False),
    ("notice period (days)",                                                "notice_period",        _int,  False),
    ("lock-in period (days)",                                               "lockin_period",        _int,  False),
    ("minimum stay (months) *",                                             "minimum_stay",         _int,  False),
    ("available from * (yyyy-mm-dd)",                                       "available_from",       _date, False),
    # ── Room 1 columns ────────────────────────────────────────────────────────
    ("room_type_1 *",                                                       "__room_type_1__",      _str,  True),
    ("room_beds_1 *",                                                       "__room_beds_1__",      _int,  True),
    ("room_rent_1 *",                                                       "__room_rent_1__",      _str,  True),
    ("room_deposit_1 *",                                                    "__room_deposit_1__",   _str,  True),
    ("room_brokerage_1",                                                    "__room_brokerage_1__", _str,  True),
    ("room_brokerage_percent_1",                                            "__room_brokerage_percent_1__", _str, True),
    ("room_manual_brokerage_1",                                             "__room_manual_brokerage_1__",  _str, True),
    ("room_facilities_1",                                                   "__room_facilities_1__",_str,  True),
    # ── Room 2 columns ────────────────────────────────────────────────────────
    ("room_type_2",                                                         "__room_type_2__",      _str,  True),
    ("room_beds_2",                                                         "__room_beds_2__",      _int,  True),
    ("room_rent_2",                                                         "__room_rent_2__",      _str,  True),
    ("room_deposit_2",                                                      "__room_deposit_2__",   _str,  True),
    ("room_brokerage_2",                                                    "__room_brokerage_2__", _str,  True),
    ("room_brokerage_percent_2",                                            "__room_brokerage_percent_2__", _str, True),
    ("room_manual_brokerage_2",                                             "__room_manual_brokerage_2__",  _str, True),
    ("room_facilities_2",                                                   "__room_facilities_2__",_str,  True),
    # ── Rest of fields ─────────────────────────────────────────────────────────
    ("meals available? (true/false)",                                       "meals_available",      _bool, False),
    ("meal offerings (breakfast,lunch,dinner)",                             "meal_offerings",       _str,  False),
    ("meal speciality (veg/non-veg/both)",                                  "meal_speciality",      _str,  False),
    ("opposite sex allowed? (true/false)",                                  "opposite_sex_allowed", _bool, False),
    ("any time allowed? (true/false)",                                       "any_time_allowed",     _bool, False),
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
 
# Updated REQUIRED_HEADERS — room type 1 is now required
REQUIRED_HEADERS = {
    "city *",
    "locality *",
    "property address *",
    "total beds *",
    "pg for * (boys/girls/co_living)",
    "furnishing type * (fully-furnished/semi-furnished/unfurnished)",
    "minimum stay (months) *",
    "available from * (yyyy-mm-dd)",
    "room_type_1 *",
    "room_beds_1 *",
    "room_rent_1 *",
    "room_deposit_1 *",
    "owner name *",
    "contact number *",
    "email *",
}
 
# Number of room slots supported
ROOM_SLOTS = 2
# Required fields validated on model data dict
REQUIRED_FIELDS = [
    "city", "locality", "property_address",
    "total_beds", "pg_for", "furnishing_type",
    "minimum_stay", "available_from",
    "owner_name", "contact_number", "email",
]




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



@csrf_exempt
@require_POST
def import_pg_excel(request):
    if not request.session.get('Admin_id') and not request.session.get('User_id'):
        return JsonResponse({'status': 'error', 'message': 'Unauthorized'}, status=401)

    file = request.FILES.get('file')
    if not file:
        return JsonResponse({'status': 'error', 'message': 'No file uploaded'}, status=400)

    file_name = file.name.strip()

    try:
        wb = openpyxl.load_workbook(io.BytesIO(file.read()), data_only=True, read_only=True)
        ws = wb.active
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': f'Invalid Excel file: {e}'}, status=400)

    all_rows = list(ws.iter_rows(values_only=True))
    wb.close()

    if len(all_rows) < 2:
        return JsonResponse({'status': 'error', 'message': 'File is empty or missing headers.'}, status=400)

    row0 = [str(c).strip().lower() if c else "" for c in all_rows[0]]
    row1 = [str(c).strip().lower() if c else "" for c in all_rows[1]]

    if any("step" in v or "📋" in v or "room" in v for v in row0 if v):
        header_row = row1
        data_start = 2
        if len(all_rows) > 2:
            row2 = all_rows[2]
            non_empty = [c for c in row2 if c is not None and str(c).strip()]
            if len(non_empty) > 3 and all(
                isinstance(c, str) and len(c) > 10 for c in non_empty[:5]
            ):
                data_start = 3
    else:
        header_row = row0
        data_start = 1

    col_index = {h: i for i, h in enumerate(header_row) if h}

    missing_headers = REQUIRED_HEADERS - set(col_index.keys())
    if missing_headers:
        return JsonResponse({
            'status': 'error',
            'message': (
                f'Wrong template format — missing columns: {", ".join(sorted(missing_headers))}. '
                f'Please download the latest template.'
            )
        }, status=400)

    # ── Uploader identity ─────────────────────────────────────────────────────
    admin_id = request.session.get('Admin_id')
    user_id  = request.session.get('User_id')

    admin_obj = Admin_Login.objects.filter(id=admin_id).first() if admin_id else None
    user_obj  = User_Details.objects.filter(id=user_id).first()  if user_id  else None

    uploader_name    = ""
    uploader_email   = ""
    uploader_contact = ""
    uploader_role    = "Automated Engine"

    if admin_obj:
        uploader_name    = getattr(admin_obj, 'name', '') or getattr(admin_obj, 'username', '')
        uploader_email   = getattr(admin_obj, 'email', '')
        uploader_contact = getattr(admin_obj, 'phone', '') or getattr(admin_obj, 'mobile', '')
        uploader_role    = "Admin"
    elif user_obj:
        uploader_name    = user_obj.user_name
        uploader_email   = user_obj.user_email
        uploader_contact = user_obj.user_phone
        uploader_role    = "User"

    col_lookup   = {excel_key: (field, conv) for excel_key, field, conv, _ in COLUMN_MAP}
    model_fields = {f.name for f in PGColivingProperty._meta.get_fields() if hasattr(f, 'column')}
    meta_fields  = {
        "uploaded_by_name", "uploaded_by_email", "uploaded_by_contact",
        "uploaded_by_role", "upload_file_name"
    }

    # ── PRE-FETCH all fingerprints in ONE query (no per-row DB hits) ──────────
    existing_all = set(
        PGColivingProperty.objects.filter(is_deleted=False)
        .values_list('contact_number', 'email', 'property_address', 'locality')
    )
    same_file_same_user_fps = set(
        PGColivingProperty.objects.filter(
            upload_file_name=file_name,
            uploaded_by_email=uploader_email,
            is_deleted=False
        ).values_list('contact_number', 'email', 'property_address', 'locality')
    )
    same_file_all_fps = set(
        PGColivingProperty.objects.filter(
            upload_file_name=file_name,
            is_deleted=False
        ).values_list('contact_number', 'email', 'property_address', 'locality')
    )

    imported                    = 0
    skipped                     = 0
    errors                      = []
    same_file_same_user_skipped = 0
    same_file_diff_user_skipped = 0
    diff_file_same_data_skipped = 0

    pg_objects_to_create = []
    room_data_per_row    = []

    for row_num, row in enumerate(all_rows[data_start:], start=data_start + 1):

        if all(c is None or str(c).strip() == "" for c in row):
            continue

        data     = {}
        room_map = {}

        for excel_key, (model_field, conv) in col_lookup.items():
            idx = col_index.get(excel_key)
            if idx is None or idx >= len(row):
                continue
            raw = row[idx]

            if model_field.startswith("__room_") and model_field.endswith("__"):
                inner = model_field[2:-2]
                parts = inner.rsplit("_", 1)
                if len(parts) == 2 and parts[1].isdigit():
                    slot      = int(parts[1])
                    field_key = parts[0]
                    try:
                        val = conv(raw)
                    except Exception:
                        val = None
                    room_map.setdefault(slot, {})[field_key] = val
                continue

            if model_field in model_fields:
                try:
                    data[model_field] = conv(raw)
                except Exception:
                    data[model_field] = None

        # 🚀 AUTO GENERATE PROPERTY TITLE DURING EXCEL IMPORT LOOP IF EMPTY OR STR NULL/NAN
        incoming_title = str(data.get("property_title", "")).strip()
        if not data.get("property_title") or incoming_title in ["", "None", "nan", "NaN"]:
            city_val = str(data.get("city", "")).strip()
            locality_val = str(data.get("locality", "")).strip()
            building_val = str(data.get("building_name", "")).strip() if data.get("building_name") else ""
            pg_for_val = str(data.get("pg_for", "Co-Living")).strip()
            
            gender_target = pg_for_val if pg_for_val and pg_for_val not in ["None", "nan", "NaN"] else "Co-Living"
            b_name = f"{building_val} " if building_val and building_val not in ["None", "nan", "NaN"] else ""
            
            data["property_title"] = f"Premium {gender_target} PG at {b_name}{locality_val}".strip()

        missing = [f for f in REQUIRED_FIELDS if not data.get(f)]
        if missing:
            skipped += 1
            errors.append(f"Row {row_num}: Missing → {', '.join(missing)}")
            continue

        rooms = []
        for slot in range(1, ROOM_SLOTS + 1):
            rd = room_map.get(slot, {})
            if not rd.get("room_type") and not rd.get("room_rent"):
                continue
            rooms.append({
                "room_type":              rd.get("room_type") or "single",
                "room_beds":              rd.get("room_beds") or 1,
                "room_rent":              float(rd.get("room_rent") or 0),
                "room_deposit":           float(rd.get("room_deposit") or 0),
                "room_brokerage":         rd.get("room_brokerage") or "No",
                "room_brokerage_percent": rd.get("room_brokerage_percent") or "",
                "room_manual_brokerage":  rd.get("room_manual_brokerage") or "",
                "room_facilities":        rd.get("room_facilities") or "",
            })

        data["uploaded_by_name"]    = uploader_name
        data["uploaded_by_email"]   = uploader_email
        data["uploaded_by_contact"] = uploader_contact
        data["uploaded_by_role"]    = uploader_role
        data["upload_file_name"]    = file_name

        fingerprint = (
            data.get("contact_number", ""),
            data.get("email", ""),
            data.get("property_address", ""),
            data.get("locality", ""),
        )

        if fingerprint in same_file_same_user_fps:
            same_file_same_user_skipped += 1
            skipped += 1
            continue

        if fingerprint in same_file_all_fps and fingerprint not in same_file_same_user_fps:
            same_file_diff_user_skipped += 1
            skipped += 1
            errors.append(
                f"Row {row_num}: Already uploaded by a different user with the same file."
            )
            continue

        if fingerprint in existing_all and fingerprint not in same_file_all_fps:
            diff_file_same_data_skipped += 1
            skipped += 1
            errors.append(
                f"Row {row_num}: Duplicate — same property data already exists from a different file."
            )
            continue

        data = {k: v for k, v in data.items() if k in model_fields or k in meta_fields}

        pg_objects_to_create.append(PGColivingProperty(**data))
        room_data_per_row.append(rooms)

        existing_all.add(fingerprint)
        same_file_all_fps.add(fingerprint)
        same_file_same_user_fps.add(fingerprint)

    # ── BULK INSERT & DYNAMIC AUTO-FAQ EXECUTION ──────────────────────────────
    if pg_objects_to_create:
        try:
            created = PGColivingProperty.objects.bulk_create(
                pg_objects_to_create,
                batch_size=200,
            )
            imported = len(created)

            # 🚀 RUN BULK GENERATED AUTO-FAQ SEQUENCING FOR CREATED OBJECTS
            for pg_instance in created:
                pg_instance.generate_auto_faqs()

            room_objects = []
            for pg, rooms in zip(created, room_data_per_row):
                for room in rooms:
                    room_objects.append(PGRoomDetail(property=pg, **room))
            if room_objects:
                PGRoomDetail.objects.bulk_create(room_objects, batch_size=500)

        except Exception as e:
            # Re-init counter reset for fallback error validation loop block
            imported = 0 
            for pg_obj, rooms in zip(pg_objects_to_create, room_data_per_row):
                try:
                    pg_obj.save()
                    # 🚀 TRIGGER FAQ PROGRAMMATIC ASSIGNMENT DURING FALLBACK ROW SAVE
                    pg_obj.generate_auto_faqs()
                    
                    for room in rooms:
                        PGRoomDetail.objects.create(property=pg_obj, **room)
                    imported += 1
                except Exception as row_err:
                    skipped += 1
                    errors.append(f"Save error: {row_err}")

    return JsonResponse({
        "status":                        "success",
        "imported":                      imported,
        "skipped":                       skipped,
        "errors":                        errors[:10],
        "same_file_same_user_skipped":   same_file_same_user_skipped,
        "same_file_diff_user_skipped":   same_file_diff_user_skipped,
        "diff_file_same_data_skipped":   diff_file_same_data_skipped,
        "uploader_name":                 uploader_name,
        "file_name":                     file_name,
        "message":                       f"{imported} imported, {skipped} skipped",
    })
# ─── DOWNLOAD TEMPLATE VIEW ───────────────────────────────────────────────────
def download_pg_template(request):
    if not request.session.get('Admin_id'):
        from django.shortcuts import render
        return render(request, 'home_page/Adminlogin.html')
 
    import io
    import openpyxl
    from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
    from openpyxl.utils import get_column_letter
    from openpyxl.comments import Comment
    from django.http import HttpResponse
 
    wb  = openpyxl.Workbook()
    ws  = wb.active
    ws.title = "PG Listings"
 
    # ── Strict Sequence & Exact Lowercase Headers ─────────────────────────────
    sections = [
        ("📋 Basic Info", [
            ("property_title",     "Auto Generated By System",                                   False),
            ("city",               "city *",                                                      True),
            ("building_name",      "building / project name",                                     False),
            ("locality",           "locality *",                                                  True),
            
            ("property_address",   "property address *",                                          True),
            ("total_beds",         "total beds *",                                                True),
            ("pg_for",             "pg for * (boys/girls/co_living)",                             True),
            ("furnishing_type",    "furnishing type * (fully-furnished/semi-furnished/unfurnished)", True),
            ("sharing_type",       "sharing type",                                                False), # <-- Added missing field
            ("best_suited_for",    "best suited for (students/working professionals/any)",        False),
            ("meals_available",    "meals available? (true/false)",           False),
            ("meal_offerings",     "meal offerings (breakfast,lunch,dinner)", False),
            ("meal_speciality",    "meal speciality (veg/non-veg/both)",      False),
          
            ("notice_period",      "notice period (days)",                                        False),
            ("lockin_period",      "lock-in period (days)",                                       False),
            ("minimum_stay",       "minimum stay (months) *",                                     True),
            ("available_from",     "available from * (yyyy-mm-dd)",                               True),
            ("property_managed_by","property managed by (owner/caretaker)",                       False),
            ("manager_stays",      "property manager stays at property? (true/false)",            False),
        ]),
        ("🛏 Room 1", [
            ("room_type_1",              "room_type_1 *",              True),
            ("room_beds_1",              "room_beds_1 *",              True),
            ("room_rent_1",              "room_rent_1 *",              True),
            ("room_deposit_1",           "room_deposit_1 *",           True),
            ("room_brokerage_1",         "room_brokerage_1",           False),
            ("room_brokerage_percent_1", "room_brokerage_percent_1",   False),
            ("room_manual_brokerage_1",  "room_manual_brokerage_1",    False),
            ("room_facilities_1",        "room_facilities_1",          False),
        ]),
        ("🛏 Room 2", [
            ("room_type_2",              "room_type_2",                False),
            ("room_beds_2",              "room_beds_2",                False),
            ("room_rent_2",              "room_rent_2",                False),
            ("room_deposit_2",           "room_deposit_2",             False),
            ("room_brokerage_2",         "room_brokerage_2",           False),
            ("room_brokerage_percent_2", "room_brokerage_percent_2",   False),
            ("room_manual_brokerage_2",  "room_manual_brokerage_2",    False),
            ("room_facilities_2",        "room_facilities_2",          False),
        ]),
        
        ("📏 PG Regulations", [
            ("opposite_sex_allowed", "opposite sex allowed? (true/false)",   False),
            ("any_time_allowed",     "any time allowed? (true/false)",       False),
            ("visitors_allowed",     "visitors allowed? (true/false)",       False),
            ("guardian_allowed",     "guardian allowed? (true/false)",       False),
            ("drinking_allowed",     "drinking allowed? (true/false)",       False),
            ("smoking_allowed",      "smoking allowed? (true/false)",        False),
        ]),
        ("🏷  Property Description & Amenties/Nearby Facilities", [
            ("property_description", "property description",                   False),
            ("amenities",            "amenities (wifi,cctv,geyser,...)",       False),
            ("nearby_facilities",    "nearby facilities (college,market,...)", False),
            
        ]),
        ("📞 Contact Info", [
            ("owner_name",        "owner name *",      True),
            ("contact_number",    "contact number *",  True),
            ("email",             "email *",           True),
            ("alternate_contact", "alternate contact", False),
        ]),
    ]
 
    # ── Styles ────────────────────────────────────────────────────────────────
    SECTION_FILL  = PatternFill("solid", start_color="1F4E79")
    ROOM1_FILL    = PatternFill("solid", start_color="2E75B6")
    ROOM2_FILL    = PatternFill("solid", start_color="5B9BD5")
    SECTION_FONT  = Font(bold=True, color="FFFFFF", size=10)
    REQ_FILL      = PatternFill("solid", start_color="FFD7D7")
    OPT_FILL      = PatternFill("solid", start_color="DDEBF7")
    ROOM_REQ_FILL = PatternFill("solid", start_color="FFE4B5")
    ROOM_OPT_FILL = PatternFill("solid", start_color="E8F4FD")
    SAMPLE_FILL   = PatternFill("solid", start_color="F2F2F2")
    AUTOGEN_FILL  = PatternFill("solid", start_color="FFF3CD")
    HDR_FONT      = Font(bold=True, size=9)
    CENTER        = Alignment(horizontal="center", vertical="center", wrap_text=True)
    LEFT          = Alignment(horizontal="left",   vertical="center", wrap_text=True)
    thin          = Side(style="thin", color="BBBBBB")
    BORDER        = Border(left=thin, right=thin, top=thin, bottom=thin)
 
    all_cols      = []
    section_spans = []
 
    for sec_idx, (sec_label, fields) in enumerate(sections):
        sc = len(all_cols) + 1
        for fkey, fheader, req in fields:
            all_cols.append((fkey, fheader, req, sec_idx))
        section_spans.append((sec_label, sc, len(all_cols), sec_idx))
 
    # Row 1: Section headers
    for sec_label, sc, ec, sec_idx in section_spans:
        ws.merge_cells(start_row=1, start_column=sc, end_row=1, end_column=ec)
        c = ws.cell(row=1, column=sc, value=sec_label)
        if "Room 1" in sec_label: c.fill = ROOM1_FILL
        elif "Room 2" in sec_label: c.fill = ROOM2_FILL
        else: c.fill = SECTION_FILL
        c.font = SECTION_FONT
        c.alignment = CENTER
 
    # Row 2 & 3: Column headers and hints
    for ci, (fkey, fheader, req, sec_idx) in enumerate(all_cols, 1):
        # Header
        c = ws.cell(row=2, column=ci, value=fheader)
        is_room = fkey.startswith("room_")
        if fkey == "property_title": c.fill = AUTOGEN_FILL
        elif is_room and req: c.fill = ROOM_REQ_FILL
        elif is_room: c.fill = ROOM_OPT_FILL
        elif req: c.fill = REQ_FILL
        else: c.fill = OPT_FILL
        c.font, c.alignment, c.border = HDR_FONT, CENTER, BORDER

        # Hint
        hint = ""
        if fkey == "city": hint = "Text – name of city"
        elif fkey == "available_from": hint = "YYYY-MM-DD"
        elif fkey == "sharing_type": hint = "single / double / triple"
        c_hint = ws.cell(row=3, column=ci, value=hint)
        c_hint.font, c_hint.alignment, c_hint.border = Font(italic=True, color="777777", size=8), LEFT, BORDER
 
    # Row 4: Sample data
   # ── Row 4: sample data (Aligned with new sequence) ────────────────────────
    samples = {
        # 📋 Basic Info
        "property_title": "",  # Blank -> Auto-generated by system
        "city": "Nagpur",
        "building_name": "ABC Building",
        "locality": "Dharampeth",
        "property_address": "123, Near Metro Station, Dharampeth, Nagpur",
        "total_beds": 50,
        "pg_for": "boys",
        "furnishing_type": "fully-furnished",
        "sharing_type": "double",
        "best_suited_for": "students",
        "meals_available": "True",
        "meal_offerings": "Breakfast,Dinner",
        "meal_speciality": "Veg",
        "notice_period": 30,
        "lockin_period": 90,
        "minimum_stay": 3,
        "available_from": "2026-07-01",
        "property_managed_by": "owner",
        "manager_stays": "True",

        # 🛏 Room 1
        "room_type_1": "double",
        "room_beds_1": 2,
        "room_rent_1": 8000,
        "room_deposit_1": 15000,
        "room_brokerage_1": "Yes",
        "room_brokerage_percent_1": "1%",
        "room_manual_brokerage_1": "",
        "room_facilities_1": "AC,Wi-Fi,Attached Bathroom",

        # 🛏 Room 2
        "room_type_2": "single",
        "room_beds_2": 1,
        "room_rent_2": 12000,
        "room_deposit_2": 20000,
        "room_brokerage_2": "No",
        "room_brokerage_percent_2": "",
        "room_manual_brokerage_2": "",
        "room_facilities_2": "AC,Wardrobe",

        # 📏 PG Regulations
        "opposite_sex_allowed": "False",
        "any_time_allowed": "True",
        "visitors_allowed": "True",
        "guardian_allowed": "True",
        "drinking_allowed": "False",
        "smoking_allowed": "False",

        # 🏷 Property Description & Amenities
        "property_description": "Premium and secure PG with modern amenities, ideal for students and professionals.",
        "amenities": "WiFi,CCTV,Geyser,Washing Machine",
        "nearby_facilities": "College,Market,Hospital,Metro Station",

        # 📞 Contact Info
        "owner_name": "Mr. Sharma",
        "contact_number": "9876543210",
        "email": "sharma@email.com",
        "alternate_contact": "9999999999",
    }
 
    for ci, (fkey, fheader, _, sec_idx) in enumerate(all_cols, 1):
        val = samples.get(fkey, "")
        c = ws.cell(row=4, column=ci, value=val)
        if fkey == "property_title":
            c.font = Font(italic=True, color="999999", size=9)
            c.comment = Comment("Leave blank — auto-generated.", "System")
        c.fill, c.alignment, c.border = SAMPLE_FILL, LEFT, BORDER
 
    ws.merge_cells(start_row=5, start_column=1, end_row=5, end_column=len(all_cols))
    lc = ws.cell(row=5, column=1, value=("🔴 Red = Required | Row 3 = Hints | Row 4 = SAMPLE — delete before uploading"))
    lc.font, lc.alignment = Font(italic=True, color="555555", size=9), LEFT
 
    for ci, (fkey, fheader, _, __) in enumerate(all_cols, 1):
        ws.column_dimensions[get_column_letter(ci)].width = max(18, len(fheader) * 0.9)
 
    ws.row_dimensions[1].height, ws.row_dimensions[2].height = 22, 42
    ws.row_dimensions[3].height, ws.row_dimensions[4].height = 28, 18
    ws.freeze_panes = "A5"
 
    buf = io.BytesIO()
    wb.save(buf)
    buf.seek(0)
    response = HttpResponse(buf.read(), content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="pg_import_template.xlsx"'
    return response







# =========================================================
# EDIT PAGE VIEW
# =========================================================

def pg_edit_page(request, property_id):

    # =====================================================
    # ADMIN SESSION CHECK
    # =====================================================
    session_id = request.session.get('Admin_id')

    if not session_id:
        return render(
            request,
            'home_page/Adminlogin.html'
        )

    admin_obj = Admin_Login.objects.get(
        id=session_id
    )

    # =====================================================
    # FETCH PROPERTY
    # =====================================================
    pg = get_object_or_404(
        PGColivingProperty,
        pg_property_id=property_id
    )

    # =====================================================
    # AMENITIES DATA
    # =====================================================
    ameneties_obj = Ameneties_Details.objects.all()

    # =====================================================
    # FACILITIES DATA
    # =====================================================
    facilities_obj = Facilities_Details.objects.all()

    # =====================================================
    # SPLIT AMENITIES
    # =====================================================
    selected_amenities = []

    if pg.amenities:

        selected_amenities = [
            x.strip()
            for x in pg.amenities.split(",")
            if x.strip()
        ]

    # =====================================================
    # SPLIT FACILITIES
    # =====================================================
    selected_facilities = []

    if pg.nearby_facilities:

        selected_facilities = [
            x.strip()
            for x in pg.nearby_facilities.split(",")
            if x.strip()
        ]

    # =====================================================
    # ROOM FACILITIES SPLIT
    # =====================================================
    rooms = pg.rooms.all()

    for room in rooms:

        if room.room_facilities:

            room.facility_list = [
                x.strip()
                for x in room.room_facilities.split(",")
                if x.strip()
            ]

        else:
            room.facility_list = []

    # =====================================================
    # CONTEXT
    # =====================================================
    context = {

        # ADMIN
        "admin_obj": admin_obj,

        # PROPERTY
        "pg": pg,

        # AMENITIES
        "ameneties_obj": ameneties_obj,

        # FACILITIES
        "facilities_obj": facilities_obj,

        # SELECTED VALUES
        "selected_amenities": selected_amenities,
        "selected_facilities": selected_facilities,

        # ROOMS
        "rooms": rooms,
    }

    return render(
        request,
        "admin_user/Reports/Rental/pg_edit.html",
        context
    )

# =========================================================
# UPDATE PG PROPERTY

@require_POST
def pg_edit(request, property_id):

    # =====================================================
    # ADMIN SESSION CHECK
    # =====================================================
    session_id = request.session.get('Admin_id')

    if not session_id:
        return render(request, 'home_page/Adminlogin.html')

    admin_obj = Admin_Login.objects.get(id=session_id)

    try:

        print("========== POST DATA ==========")
        print(request.POST)

        print("========== FILES ==========")
        print(request.FILES)

        # =====================================================
        # FETCH PROPERTY
        # =====================================================
        pg = get_object_or_404(
            PGColivingProperty,
            pg_property_id=property_id
        )

        # =================================================
        # UPDATE ADMIN / UPLOADER DETAILS
        # =================================================
        pg.uploaded_by_name = admin_obj.name
        pg.uploaded_by_email = admin_obj.email
        pg.uploaded_by_contact = admin_obj.phone
        pg.uploaded_by_role = admin_obj.role

        # =================================================
        # MULTI SELECT LIST HELPER
        # =================================================
        def get_list(name):
            return ",".join(request.POST.getlist(name))

        with transaction.atomic():

            # =================================================
            # BASIC DETAILS
            # =================================================
            pg.property_title = request.POST.get(
                "property_title", ""
            )

            pg.city = request.POST.get(
                "city", ""
            )

            pg.building_name = request.POST.get(
                "building_name", ""
            )

            pg.locality = request.POST.get(
                "locality", ""
            )

            pg.property_address = request.POST.get(
                "property_address", ""
            )

            pg.total_beds = int(
                request.POST.get("total_beds") or 0
            )

            pg.pg_for = request.POST.get(
                "pg_for", ""
            )

            pg.furnishing_type = request.POST.get(
                "furnishing_type", ""
            )

            pg.sharing_type = request.POST.get(
                "sharing_type", ""
            )

            pg.best_suited_for = request.POST.get(
                "best_suited_for", ""
            )

            # =================================================
            # AMENITIES
            # =================================================
            pg.amenities = get_list("amenities[]")

            pg.nearby_facilities = get_list("facilities[]")

            # =================================================
            # MEALS
            # =================================================
            pg.meals_available = (
                request.POST.get("meals_available")
                in ["on", "true", "True", "1"]
            )

            if pg.meals_available:

                pg.meal_offerings = request.POST.get(
                    "meal_offerings", ""
                )

                pg.meal_speciality = request.POST.get(
                    "meal_speciality", ""
                )

            else:

                pg.meal_offerings = None
                pg.meal_speciality = None

            # =================================================
            # RULES
            # =================================================
            pg.notice_period = (
                request.POST.get("notice_period") or None
            )

            pg.lockin_period = (
                request.POST.get("lockin_period") or None
            )

            pg.minimum_stay = int(
                request.POST.get("minimum_stay") or 1
            )

            pg.available_from = request.POST.get(
                "available_from"
            )

            pg.property_managed_by = request.POST.get(
                "property_managed_by", ""
            )

            # =================================================
            # MANAGER STAYS — RADIO BUTTON FIX
            # =================================================
            pg.manager_stays = (
                request.POST.get("manager_stays") == "true"
            )

            # =================================================
            # BOOLEAN CHECKBOXES
            # =================================================
            pg.opposite_sex_allowed = (
                "opposite_sex_allowed" in request.POST
            )

            pg.any_time_allowed = (
                "any_time_allowed" in request.POST
            )

            pg.visitors_allowed = (
                "visitors_allowed" in request.POST
            )

            pg.guardian_allowed = (
                "guardian_allowed" in request.POST
            )

            pg.drinking_allowed = (
                "drinking_allowed" in request.POST
            )

            pg.smoking_allowed = (
                "smoking_allowed" in request.POST
            )

            # =================================================
            # DESCRIPTION
            # =================================================
            pg.property_description = request.POST.get(
                "property_description", ""
            )

            # =================================================
            # VIDEO
            # =================================================
            if request.FILES.get("video"):

                if pg.video:
                    pg.video.delete(save=False)

                pg.video = request.FILES.get("video")

            # =================================================
            # CONTACT
            # =================================================
            pg.owner_name = request.POST.get(
                "owner_name", ""
            )

            pg.contact_number = request.POST.get(
                "contact_number", ""
            )

            pg.email = request.POST.get(
                "email", ""
            )

            pg.alternate_contact = request.POST.get(
                "alternate_contact", ""
            )

            # =================================================
            # SAVE PROPERTY
            # =================================================
            pg.save()

            # =================================================
            # DELETE OLD ROOMS
            # =================================================
            pg.rooms.all().delete()

            # =================================================
            # ROOM ARRAYS
            # =================================================
            room_types = request.POST.getlist('room_type[]')

            room_beds = request.POST.getlist('room_beds[]')

            room_rents = request.POST.getlist('room_rent[]')

            room_deposits = request.POST.getlist('room_deposit[]')

            room_brokerages = request.POST.getlist('room_brokerage[]')

            room_brokerage_percents = request.POST.getlist(
                'room_brokerage_percent[]'
            )

            room_manual_brokerages = request.POST.getlist(
                'room_manual_brokerage[]'
            )

            # =================================================
            # CREATE NEW ROOMS
            # =================================================
            for idx in range(len(room_types)):

                facilities_key = f'room_facilities_{idx + 1}[]'

                room_facilities_str = ",".join(
                    request.POST.getlist(facilities_key)
                )

                PGRoomDetail.objects.create(
                    property=pg,

                    room_type=room_types[idx],

                    room_beds=int(
                        room_beds[idx] or 1
                    ),

                    room_rent=room_rents[idx] or 0,

                    room_deposit=room_deposits[idx] or 0,

                    room_brokerage=(
                        room_brokerages[idx]
                        if idx < len(room_brokerages)
                        else ''
                    ),

                    room_brokerage_percent=(
                        room_brokerage_percents[idx]
                        if idx < len(room_brokerage_percents)
                        else ''
                    ),

                    room_manual_brokerage=(
                        room_manual_brokerages[idx]
                        if idx < len(room_manual_brokerages)
                        else ''
                    ),

                    room_facilities=room_facilities_str
                )

            # =================================================
            # IMAGE UPLOAD
            # =================================================
            new_images = request.FILES.getlist("property_images[]")

            if new_images:

                current_total = pg.images.count()

                if current_total + len(new_images) > 10:

                    return JsonResponse({
                        "status": "error",
                        "message": (
                            f"Maximum 10 images allowed. "
                            f"Current images: {current_total}"
                        )
                    })

                for img in new_images:

                    PGPropertyImage.objects.create(
                        property=pg,
                        image=img
                    )

        # =====================================================
        # SUCCESS RESPONSE
        # =====================================================
        return JsonResponse({
            "status": "success",
            "message": "PG Property Updated Successfully.",
            "redirect_url": reverse('pg_list')
        })

    except Exception as e:

        print("========== ERROR ==========")
        print(str(e))

        return JsonResponse({
            "status": "error",
            "message": str(e)
        }) 




@require_POST
def pg_coliving_delete(request, pk):

    sid, _ = _get_admin(request)
    if not sid:
        return JsonResponse({
            'status': 'error',
            'message': 'Unauthorized'
        }, status=401)

    try:
        deleter_name = _get_deleter_name(request)

        # ✅ USING NEW PRIMARY KEY FIELD
        pg = get_object_or_404(
            PGColivingProperty,
            pg_property_id=pk
        )

        pg.is_deleted = True
        pg.deleted_at = timezone.now()
        pg.deleted_by = deleter_name
        pg.save()

        return JsonResponse({
            'status': 'success',
            'message': 'Moved to Recycle Bin successfully!'
        })

    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        })



@csrf_exempt
@require_POST
def pg_restore(request, id):
    admin_id = request.session.get('Admin_id')
    if not admin_id:
        return JsonResponse({'status': 'error', 'message': 'Unauthorized'}, status=401)

    PGColivingProperty.objects.filter(pg_property_id=id).update(
        is_deleted=False,
        deleted_at=None,
        deleted_by=None
    )
    return JsonResponse({'status': 'success', 'message': 'PG Property Restored Successfully!'})

# =========================================================
# HARD DELETE
# =========================================================
@csrf_exempt
@require_POST
def pg_hard_delete(request, id):
    admin_id = request.session.get('Admin_id')
    if not admin_id:
        return JsonResponse({'status': 'error', 'message': 'Unauthorized'}, status=401)

    try:
        pg = get_object_or_404(PGColivingProperty, pg_property_id=id)

        # Clean up related asset files safely
        for img in pg.images.all():
            if img.image:
                img.image.delete(save=False)
        if pg.video:
            pg.video.delete(save=False)

        pg.delete()
        return JsonResponse({'status': 'success', 'message': 'Permanently Deleted Successfully!'})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)





def pg_coliving_view(request, pk):
    # session_id = request.session.get('Admin_id')
    # admin_obj = Admin_Login.objects.get(id=session_id)
    # ^ Replace with your standard auth logic
    
    pg = get_object_or_404(PGColivingProperty, pk=pk)

    # 1. Safely query the new relational Room models
    parsed_rooms = pg.rooms.all()
    
    # Calculate sidebar pricing metrics dynamically
    rent_stats = parsed_rooms.aggregate(min_rent=Min('room_rent'), max_rent=Max('room_rent'))
    starting_rent = rent_stats['min_rent'] or 0

    # 2. Parse Comma-Separated Strings into Lists for HTML "Chips"
    def split_to_list(db_string):
        return [x.strip() for x in db_string.split(',') if x.strip()] if db_string else []

    context = {
        # 'admin_obj': admin_obj,
        'pg': pg,
        'parsed_rooms': parsed_rooms,
        'starting_rent': starting_rent, # Passed to the sidebar
        'pg_for_list': split_to_list(pg.pg_for),
        'sharing_type_list': split_to_list(pg.sharing_type),
        'best_suited_list': split_to_list(pg.best_suited_for),
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
    user_id  = request.session.get('User_id')

    if not admin_id and not user_id:
        return redirect('login')

    try:
        if admin_id:
            admin = Admin_Login.objects.get(id=admin_id)
            uploader_name, uploader_email, uploader_phone, uploader_role = (
                admin.name, admin.email, admin.phone, admin.role
            )
        else:
            user = User_Details.objects.get(id=user_id)
            uploader_name, uploader_email, uploader_phone, uploader_role = (
                user.name, user.email, user.phone, user.role
            )

        if request.method == "POST":
            prop = PlotSaleProperty.objects.create(
                # ── Step 1: Plot Specs ──────────────────────────────────
                plot_title            = request.POST.get('plot_title'),
                plot_area             = request.POST.get('plot_area') or 0,
                resale_plot_type      = request.POST.get('resale_plot_type'),
                plot_road_facing      = request.POST.get('plot_road_facing'),
                corner_plot           = request.POST.get('corner_plot', 'no'),       # ✅ was plot_corner
                sanctioning_authority = request.POST.get('sanctioning_authority'),   # ✅ was plot_authority
                plot_fencing          = request.POST.get('plot_fencing', 'no'),

                # ── Step 2: Pricing & Legal ─────────────────────────────
                plot_price            = request.POST.get('plot_price') or 0,
                brokerage             = request.POST.get('brokerage', 'No'),
                brokerage_percentage  = request.POST.get('brokerage_percentage'),
                ownership_type        = request.POST.get('ownership_type'),          # ✅ was plot_ownership
                loan_on_property      = request.POST.get('loan_on_property', 'no'), # ✅ was plot_loan
                plot_loan_amount      = request.POST.get('plot_loan_amount') or None,

                # ── Step 3: Media ───────────────────────────────────────
                encumbrance_cert      = request.FILES.get('encumbrance_cert'),
                social_video          = request.FILES.get('social_video'),

                # ── Step 4: Location & Owner ────────────────────────────
                plot_city             = request.POST.get('plot_city'),
                plot_locality         = request.POST.get('plot_locality'),
                plot_address          = request.POST.get('plot_address'),
                plot_owner_name       = request.POST.get('plot_owner_name'),
                plot_owner_contact    = request.POST.get('plot_owner_contact'),
                plot_owner_email      = request.POST.get('plot_owner_email'),
                plot_owner_role       = request.POST.get('plot_owner_role'),         # ✅ was missing

                # ── Uploader / Audit ────────────────────────────────────
                uploaded_by_name      = uploader_name,
                uploaded_by_email     = uploader_email,
                uploaded_by_contact   = uploader_phone,
                uploaded_by_role      = uploader_role,
            )

            images = request.FILES.getlist('property_images[]')
            for i, img in enumerate(images[:10]):
                PlotSaleImage.objects.create(property=prop, image=img)

            return JsonResponse({"status": "success", "message": "Plot Listing Added Successfully"})

    except Exception as e:
        print("ERROR:", str(e))
        traceback.print_exc()
        return JsonResponse({"status": "error", "message": str(e)})

    admin_obj = Admin_Login.objects.get(id=admin_id) if admin_id else User_Details.objects.get(id=user_id)
    return render(request, 'admin_user/Reports/Resale/plot_add.html', {'admin_obj': admin_obj})






def plot_sale_edit(request, plot_property_id):
    admin_id = request.session.get('Admin_id')
    user_id  = request.session.get('User_id')

    if not admin_id and not user_id:
        return redirect('login')

    prop = get_object_or_404(PlotSaleProperty, plot_property_id=plot_property_id)

    if request.method == "POST":
        try:
            # ── Step 1: Plot Specs ──────────────────────────────────
            prop.plot_title            = request.POST.get('plot_title')
            prop.plot_area             = request.POST.get('plot_area') or 0
            prop.resale_plot_type      = request.POST.get('resale_plot_type')
            prop.plot_road_facing      = request.POST.get('plot_road_facing')
            prop.corner_plot           = request.POST.get('corner_plot', 'no')        # ✅ was plot_corner
            prop.sanctioning_authority = request.POST.get('sanctioning_authority')    # ✅ was plot_authority
            prop.plot_fencing          = request.POST.get('plot_fencing', 'no')

            # ── Step 2: Pricing & Legal ─────────────────────────────
            prop.plot_price            = request.POST.get('plot_price') or 0
            prop.brokerage             = request.POST.get('brokerage', 'No')
            prop.brokerage_percentage  = request.POST.get('brokerage_percentage')
            prop.ownership_type        = request.POST.get('ownership_type')           # ✅ was plot_ownership
            prop.loan_on_property      = request.POST.get('loan_on_property', 'no')  # ✅ was plot_loan
            prop.plot_loan_amount      = request.POST.get('plot_loan_amount') or None

            # ── Step 3: Media (only update if new file uploaded) ────
            if request.FILES.get('encumbrance_cert'):
                prop.encumbrance_cert  = request.FILES.get('encumbrance_cert')
            if request.FILES.get('social_video'):
                prop.social_video      = request.FILES.get('social_video')

            # ── Step 4: Location & Owner ────────────────────────────
            prop.plot_city             = request.POST.get('plot_city')
            prop.plot_locality         = request.POST.get('plot_locality')
            prop.plot_address          = request.POST.get('plot_address')
            prop.plot_owner_name       = request.POST.get('plot_owner_name')
            prop.plot_owner_contact    = request.POST.get('plot_owner_contact')
            prop.plot_owner_email      = request.POST.get('plot_owner_email')
            prop.plot_owner_role       = request.POST.get('plot_owner_role')          # ✅ was missing

            # Wipe title so save() auto-regenerates it
            prop.property_title = ""
            prop.save()

            # Handle new images (respect 10 image cap)
            new_images        = request.FILES.getlist('property_images[]')
            current_count     = prop.images.count()
            for img in new_images:
                if current_count >= 10:
                    break
                PlotSaleImage.objects.create(property=prop, image=img)
                current_count += 1

            return JsonResponse({"status": "success", "message": "Plot Listing Updated Successfully"})

        except Exception as e:
            print("ERROR:", str(e))
            traceback.print_exc()
            return JsonResponse({"status": "error", "message": str(e)})

    context = {
        'prop': prop,
        'existing_images': prop.images.all()
    }
    return render(request, 'admin_user/Reports/Resale/plot_edit.html', context)

# ── 1. MAIN LIST VIEW ──



#


@require_POST
def plot_sale_bulk_delete(request):
    """
    Bulk Soft Delete Plot Sale Properties
    """

    admin_id = request.session.get('Admin_id')
    user_id = request.session.get('User_id')

    if not admin_id and not user_id:
        return JsonResponse({
            'status': 'error',
            'message': 'Unauthorized access.'
        })

    try:

        data = json.loads(request.body)

        delete_type = data.get('delete_type')

        deleter_name = _get_deleter_name(request)

        properties = PlotSaleProperty.objects.filter(
            is_deleted=False
        )

        # ====================================
        # Delete All
        # ====================================

        if delete_type == 'delete_all':

            count = properties.count()

            properties.update(
                is_deleted=True,
                deleted_at=timezone.now(),
                deleted_by=deleter_name
            )

            return JsonResponse({
                'status': 'success',
                'message': f'{count} plots moved to recycle bin.'
            })

        # ====================================
        # Current Page
        # ====================================

        elif delete_type == 'current_page':

            page_ids = data.get('page_ids', [])

            target_props = properties.filter(
                plot_property_id__in=page_ids
            )

            count = target_props.count()

            target_props.update(
                is_deleted=True,
                deleted_at=timezone.now(),
                deleted_by=deleter_name
            )

            return JsonResponse({
                'status': 'success',
                'message': f'{count} plots moved to recycle bin.'
            })

        # ====================================
        # Date Range
        # ====================================

        elif delete_type == 'date_range':

            from_date = data.get('from_date')
            to_date = data.get('to_date')

            if not from_date or not to_date:
                return JsonResponse({
                    'status': 'error',
                    'message': 'Please select both dates.'
                })

            target_props = properties.filter(
                created_at__date__range=[from_date, to_date]
            )

            count = target_props.count()

            target_props.update(
                is_deleted=True,
                deleted_at=timezone.now(),
                deleted_by=deleter_name
            )

            return JsonResponse({
                'status': 'success',
                'message': f'{count} plots deleted between {from_date} and {to_date}.'
            })

        # ====================================
        # Last 30 Days
        # ====================================

        elif delete_type == 'latest_month':

            thirty_days_ago = timezone.now() - timedelta(days=30)

            target_props = properties.filter(
                created_at__gte=thirty_days_ago
            )

            count = target_props.count()

            target_props.update(
                is_deleted=True,
                deleted_at=timezone.now(),
                deleted_by=deleter_name
            )

            return JsonResponse({
                'status': 'success',
                'message': f'{count} plots from last 30 days moved to recycle bin.'
            })

        # ====================================
        # Older Than 6 Months
        # ====================================

        elif delete_type == 'old_data':

            six_months_ago = timezone.now() - timedelta(days=180)

            target_props = properties.filter(
                created_at__lt=six_months_ago
            )

            count = target_props.count()

            target_props.update(
                is_deleted=True,
                deleted_at=timezone.now(),
                deleted_by=deleter_name
            )

            return JsonResponse({
                'status': 'success',
                'message': f'{count} old plots moved to recycle bin.'
            })

        # ====================================
        # By Uploader
        # ====================================

        elif delete_type == 'by_uploader':

            uploader = data.get('uploader_text', '').strip()

            if not uploader:
                return JsonResponse({
                    'status': 'error',
                    'message': 'Please enter uploader details.'
                })

            target_props = properties.filter(
                Q(uploaded_by_name__icontains=uploader) |
                Q(uploaded_by_email__icontains=uploader) |
                Q(uploaded_by_role__icontains=uploader) |
                Q(uploaded_by_contact__icontains=uploader)
            )

            count = target_props.count()

            target_props.update(
                is_deleted=True,
                deleted_at=timezone.now(),
                deleted_by=deleter_name
            )

            return JsonResponse({
                'status': 'success',
                'message': f'{count} plots uploaded by "{uploader}" moved to recycle bin.'
            })

        # ====================================
        # By Imported File
        # ====================================

        elif delete_type == 'by_file':

            file_name = data.get('file_name', '').strip()

            if not file_name:
                return JsonResponse({
                    'status': 'error',
                    'message': 'Please select file.'
                })

            target_props = properties.filter(
                upload_file_name=file_name
            )

            count = target_props.count()

            if count == 0:
                return JsonResponse({
                    'status': 'error',
                    'message': f'No records found for file "{file_name}".'
                })

            target_props.update(
                is_deleted=True,
                deleted_at=timezone.now(),
                deleted_by=deleter_name
            )

            return JsonResponse({
                'status': 'success',
                'message': f'{count} plots from file "{file_name}" moved to recycle bin.'
            })

        # ====================================
        # Unknown Type
        # ====================================

        return JsonResponse({
            'status': 'error',
            'message': 'Invalid delete type.'
        })

    except Exception as e:

        return JsonResponse({
            'status': 'error',
            'message': str(e)
        })


  



def safe_float(val):
    """Safely converts Excel cell values to float, handling strings, currencies, and spaces."""
    if val is None:
        return 0.0
    try:
        if isinstance(val, (int, float)):
            return float(val)
        clean_val = str(val).replace('₹', '').replace(',', '').strip()
        return float(clean_val)
    except (ValueError, TypeError):
        return 0.0





def safe_float(value):
    try:
        return float(str(value).replace(",", "").strip())
    except (ValueError, TypeError):
        return 0.0





from django.views.decorators.csrf import csrf_protect




def download_plot_resale_template(request):
    wb = Workbook()
    sheet = wb.active
    sheet.title = "Plot Resale"

    DARK_BG, WHITE, MID_BLUE = "1E293B", "FFFFFF", "3B82F6"
    LIGHT_BG, HINT_BG, SAMPLE_BG = "F8FAFC", "FEF9C3", "EFF6FF"
    HINT_FG, BORDER_COLOR = "92400E", "CBD5E1"

    thin   = Side(style="thin",   color=BORDER_COLOR)
    thick  = Side(style="medium", color="94A3B8")
    cborder = Border(left=thin, right=thin, top=thin, bottom=thin)
    hborder = Border(left=thick, right=thick, top=thick, bottom=thick)

    def hfill(h): return PatternFill("solid", fgColor=h)

    sections = [
        ("📋 Plot Details", [
            ("property_title",        "Property Title",                  "⚠️ AUTO GENERATED - Leave Empty"),
            ("plot_title",            "Plot Title *",                    "e.g. Green Valley Plots"),
            ("plot_area",             "Plot Area (sq.ft) *",             "e.g. 1500"),
            ("resale_plot_type",      "Resale Plot Type *",              "residential / commercial / agricultural"),
            ("plot_road_facing",      "Plot Road Facing *",              "main / east / west / north / south"),
            ("corner_plot",           "Corner Plot",                     "yes / no (default: no)"),
            ("sanctioning_authority", "Sanctioning Authority",           "e.g. NIT / NMRDA / PRIVATE"),
            ("plot_fencing",          "Plot Fencing",                    "yes / no (default: no)"),
        ]),
        ("📋 Pricing & Legal", [
            ("plot_price",           "Plot Price (₹) *",                 "e.g. 3500000"),
            ("price_per_sqft",       "Price Per Sqft",                   "🔄 AUTO CALCULATED - Leave Empty"),
            ("brokerage",            "Brokerage",                        "Yes / No (default: No)"),
            ("brokerage_percentage", "Brokerage %",                      "e.g. 1% or leave blank"),
            ("ownership_type",       "Ownership Type *",                 "freehold / leasehold"),
            ("loan_on_property",     "Loan on Property *",               "yes / no (default: no)"),
            ("plot_loan_amount",     "Plot Loan Amount (₹)",             "e.g. 2000000 (0 if no loan)"),
        ]),
        ("📋 Location", [
            ("plot_city",     "Plot City *",        "e.g. Nagpur"),
            ("plot_locality", "Plot Locality *",    "e.g. Besa"),
            ("plot_address",  "Plot Address *",     "Plot 12, Besa Road, Nagpur"),
        ]),
        ("📋 Owner Contact", [
            ("plot_owner_name",    "Plot Owner Name *",    "Full Name"),
            ("plot_owner_contact", "Plot Owner Contact *", "10-digit mobile"),
            ("plot_owner_email",   "Plot Owner Email *",   "email@example.com"),
            ("plot_owner_role",    "Plot Owner Role",      "Owner / Agent / Builder"),
        ]),
    ]

    all_db, all_disp, all_hints = [], [], []
    section_spans = []
    col = 1
    for label, fields in sections:
        s = col
        for db, disp, hint in fields:
            all_db.append(db); all_disp.append(disp); all_hints.append(hint)
            col += 1
        section_spans.append((label, s, col - 1))

    # Header Row 1
    for label, sc, ec in section_spans:
        c = sheet.cell(row=1, column=sc, value=label)
        c.font      = Font(name="Arial", bold=True, size=11, color=WHITE)
        c.fill      = hfill(DARK_BG)
        c.alignment = Alignment(horizontal="center", vertical="center")
        c.border    = hborder
        if sc != ec:
            sheet.merge_cells(start_row=1, start_column=sc, end_row=1, end_column=ec)
    sheet.row_dimensions[1].height = 30

    # Row 2 - Database Fields
    for i, db in enumerate(all_db, 1):
        c = sheet.cell(row=2, column=i, value=db)
        c.font = Font(name="Arial", bold=True, size=9, color="475569")
        c.fill = hfill("E2E8F0"); c.alignment = Alignment(horizontal="center", vertical="center"); c.border = cborder
    sheet.row_dimensions[2].height = 22

    # Row 3 - Display Names
    for i, disp in enumerate(all_disp, 1):
        c = sheet.cell(row=3, column=i, value=disp)
        c.font = Font(name="Arial", bold=True, size=10, color=("C0392B" if disp.endswith("*") else MID_BLUE))
        c.fill = hfill(LIGHT_BG); c.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True); c.border = cborder
    sheet.row_dimensions[3].height = 36

    # Row 4 - Hints
    for i, hint in enumerate(all_hints, 1):
        c = sheet.cell(row=4, column=i, value=hint)
        c.font = Font(name="Arial", italic=True, size=8, color=HINT_FG)
        c.fill = hfill(HINT_BG); c.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True); c.border = cborder
    sheet.row_dimensions[4].height = 30

    # Row 5 - SAMPLE DATA (Marked clearly as SAMPLE)
    sample_row_label = sheet.cell(row=5, column=1, value="🔴 DELETE THIS ROW BEFORE IMPORT 🔴")
    sample_row_label.font = Font(name="Arial", bold=True, size=10, color="FF0000")
    sample_row_label.fill = hfill("FFE5E5")
    sample_row_label.alignment = Alignment(horizontal="center", vertical="center")
    sample_row_label.border = cborder
    
    sample = [
        "",  # property_title
        "SAMPLE - Green Valley Plots",  # plot_title (clearly marked as SAMPLE)
        1500,  # plot_area
        "residential",  # resale_plot_type
        "main",  # plot_road_facing
        "no",  # corner_plot
        "NIT",  # sanctioning_authority
        "yes",  # plot_fencing
        3500000,  # plot_price
        "",  # price_per_sqft
        "No",  # brokerage
        "",  # brokerage_percentage
        "freehold",  # ownership_type
        "no",  # loan_on_property
        0,  # plot_loan_amount
        "Nagpur",  # plot_city
        "Besa",  # plot_locality
        "SAMPLE - Plot 12, Besa Road, Nagpur",  # plot_address
        "SAMPLE - Amit Patil",  # plot_owner_name
        "9999999999",  # plot_owner_contact (different from real data)
        "sample@example.com",  # plot_owner_email
        "Agent"  # plot_owner_role
    ]
    
    for i, val in enumerate(sample, 1):
        if i == 1: continue  # Skip column 1 as we already set it
        c = sheet.cell(row=5, column=i, value=val)
        c.font = Font(name="Arial", size=9, color="999999")
        c.fill = hfill("FFF3F3")
        c.alignment = Alignment(horizontal="center", vertical="center")
        c.border = cborder
    sheet.row_dimensions[5].height = 25

    # Row 6 - Empty template row for user data
    for i in range(1, 23):
        c = sheet.cell(row=6, column=i, value="")
        c.fill = hfill(SAMPLE_BG)
        c.border = cborder
    
    # Add instruction text
    instruction_cell = sheet.cell(row=7, column=1, value="👇 START YOUR DATA FROM ROW 6 👇")
    instruction_cell.font = Font(name="Arial", bold=True, size=11, color="0066CC")
    instruction_cell.fill = hfill("E5F3FF")
    sheet.merge_cells(start_row=7, start_column=1, end_row=7, end_column=22)
    instruction_cell.alignment = Alignment(horizontal="center", vertical="center")
    sheet.row_dimensions[7].height = 25

    # Column widths
    widths = [28, 20, 18, 18, 18, 12, 22, 12, 16, 16, 12, 16, 18, 18, 20, 15, 18, 32, 18, 18, 24, 15]
    for i, w in enumerate(widths, 1):
        sheet.column_dimensions[get_column_letter(i)].width = w

    sheet.freeze_panes = "A6"
    sheet.sheet_view.zoomScale = 90

    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="PropCRM_Plot_Resale_Template.xlsx"'
    wb.save(response)
    return response



@csrf_protect
def import_plot_resale_excel(request):
    if request.method != 'POST':
        return JsonResponse({'status': 'error', 'message': 'Invalid request method.'})

    session_id = request.session.get('Admin_id')
    if not session_id:
        return JsonResponse({'status': 'error', 'message': 'Session expired.'})

    try:
        admin_obj = Admin_Login.objects.get(id=session_id)
    except Admin_Login.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Invalid admin.'})

    excel_file = request.FILES.get('excel_file')
    if not excel_file:
        return JsonResponse({'status': 'error', 'message': 'Please upload Excel file.'})

    try:
        wb = openpyxl.load_workbook(excel_file, data_only=True)
        sheet = wb.active

        saved_count = 0
        skipped_count = 0
        row_logs = []

        def clean_s(v):
            """Clean string values"""
            if v is None: return ""
            s = str(v).strip()
            # Remove 'SAMPLE - ' prefix if present
            s = s.replace('SAMPLE - ', '')
            if s.endswith(".0"): s = s[:-2]
            return s

        def clean_f(v):
            """Clean float values"""
            try:
                if v in [None, ""]: return 0
                # Handle string numbers with commas
                if isinstance(v, str):
                    v = v.replace(",", "").strip()
                return float(v)
            except:
                return 0

        def is_sample_row(values):
            """Check if this is a sample/instruction row"""
            # Check for instruction rows (row 7 in template)
            if values[0] and "START YOUR DATA" in str(values[0]):
                return True
            
            # Check for sample row (marked with SAMPLE in title or owner name)
            plot_title = clean_s(values[1]) if len(values) > 1 else ""
            owner_name = clean_s(values[18]) if len(values) > 18 else ""
            owner_contact = clean_s(values[19]) if len(values) > 19 else ""
            
            if "SAMPLE" in plot_title or "SAMPLE" in owner_name:
                return True
            
            # Check for exact sample data match
            if owner_contact == "9999999999" and "SAMPLE" in owner_name:
                return True
                
            return False

        # Start from row 6 (after header and sample row)
        for row_idx in range(6, sheet.max_row + 1):
            values = []
            # Fetch 22 columns
            for col in range(1, 23):
                cell_value = sheet.cell(row=row_idx, column=col).value
                values.append(cell_value)

            # Skip completely empty rows
            if not any(values):
                continue

            # Skip sample/instruction rows
            if is_sample_row(values):
                skipped_count += 1
                row_logs.append(f"Row {row_idx}: Template instruction/sample row skipped.")
                continue

            # Extract values (all 22 columns)
            property_title       = clean_s(values[0]) if len(values) > 0 else ""
            plot_title           = clean_s(values[1]) if len(values) > 1 else ""
            plot_area            = clean_f(values[2]) if len(values) > 2 else 0
            resale_plot_type     = clean_s(values[3]) if len(values) > 3 else ""
            plot_road_facing     = clean_s(values[4]) if len(values) > 4 else ""
            corner_plot          = clean_s(values[5]) if len(values) > 5 else "no"
            sanctioning_authority= clean_s(values[6]) if len(values) > 6 else ""
            plot_fencing         = clean_s(values[7]) if len(values) > 7 else "no"
            plot_price           = clean_f(values[8]) if len(values) > 8 else 0
            price_per_sqft       = clean_f(values[9]) if len(values) > 9 else 0
            brokerage            = clean_s(values[10]) if len(values) > 10 else "No"
            brokerage_percentage = clean_s(values[11]) if len(values) > 11 else ""
            ownership_type       = clean_s(values[12]) if len(values) > 12 else ""
            loan_on_property     = clean_s(values[13]) if len(values) > 13 else "no"
            plot_loan_amount     = clean_f(values[14]) if len(values) > 14 else 0
            plot_city            = clean_s(values[15]) if len(values) > 15 else ""
            plot_locality        = clean_s(values[16]) if len(values) > 16 else ""
            plot_address         = clean_s(values[17]) if len(values) > 17 else ""
            plot_owner_name      = clean_s(values[18]) if len(values) > 18 else ""
            plot_owner_contact   = clean_s(values[19]) if len(values) > 19 else ""
            plot_owner_email     = clean_s(values[20]) if len(values) > 20 else ""
            plot_owner_role      = clean_s(values[21]) if len(values) > 21 else ""

            # REQUIRED FIELD VALIDATION
            missing = []
            if not plot_title: missing.append("Plot Title")
            if not plot_area or plot_area <= 0: missing.append("Plot Area (>0)")
            if not plot_price or plot_price <= 0: missing.append("Plot Price (>0)")
            if not plot_city: missing.append("City")
            if not plot_locality: missing.append("Locality")
            if not plot_address: missing.append("Address")
            if not plot_owner_contact: missing.append("Owner Contact")
            if not plot_owner_email: missing.append("Owner Email")
            if not resale_plot_type: missing.append("Resale Plot Type")
            if not plot_road_facing: missing.append("Plot Road Facing")
            if not ownership_type: missing.append("Ownership Type")

            if missing:
                skipped_count += 1
                row_logs.append(f"Row {row_idx}: ❌ Missing required fields - {', '.join(missing)}")
                continue

            # Validate field values
            if corner_plot.lower() not in ['yes', 'no']:
                corner_plot = 'no'
            if plot_fencing.lower() not in ['yes', 'no']:
                plot_fencing = 'no'
            if loan_on_property.lower() not in ['yes', 'no']:
                loan_on_property = 'no'
            if brokerage.lower() not in ['yes', 'no']:
                brokerage = 'No'

            # DUPLICATE CHECK
            duplicate = PlotSaleProperty.objects.filter(
                plot_city__iexact=plot_city,
                plot_locality__iexact=plot_locality,
                plot_address__iexact=plot_address,
                plot_owner_contact=plot_owner_contact,
                is_deleted=False
            ).exists()

            if duplicate:
                skipped_count += 1
                row_logs.append(f"Row {row_idx}: ⚠️ Duplicate record skipped (same location & owner contact)")
                continue

            # CREATE THE PROPERTY
            try:
                plot_property = PlotSaleProperty.objects.create(
                    property_title=property_title or plot_title,
                    plot_title=plot_title,
                    plot_area=plot_area,
                    resale_plot_type=resale_plot_type,
                    plot_road_facing=plot_road_facing,
                    corner_plot=corner_plot,
                    sanctioning_authority=sanctioning_authority if sanctioning_authority else None,
                    plot_fencing=plot_fencing,
                    plot_price=plot_price,
                    # price_per_sqft will be auto-calculated in save()
                    brokerage=brokerage,
                    brokerage_percentage=brokerage_percentage if brokerage_percentage else None,
                    ownership_type=ownership_type,
                    loan_on_property=loan_on_property,
                    plot_loan_amount=plot_loan_amount if plot_loan_amount > 0 else None,
                    plot_city=plot_city,
                    plot_locality=plot_locality,
                    plot_address=plot_address,
                    plot_owner_name=plot_owner_name,
                    plot_owner_contact=plot_owner_contact,
                    plot_owner_email=plot_owner_email,
                    plot_owner_role=plot_owner_role if plot_owner_role else None,
                    
                    upload_file_name=excel_file.name,
                    uploaded_by_name=getattr(admin_obj, 'name', 'Admin'),
                    uploaded_by_email=getattr(admin_obj, 'email', ''),
                    is_deleted=False
                )
                saved_count += 1
                row_logs.append(f"Row {row_idx}: ✅ Successfully imported - ID: {plot_property.plot_property_id}")
                
            except Exception as create_error:
                skipped_count += 1
                row_logs.append(f"Row {row_idx}: ❌ Creation failed - {str(create_error)}")

        # Prepare response
        response_data = {
            'status': 'success' if saved_count > 0 else 'warning',
            'saved': saved_count,
            'skipped': skipped_count,
            'total_rows_processed': saved_count + skipped_count,
            'message': f'✅ {saved_count} properties imported successfully. ⚠️ {skipped_count} rows skipped.',
            'logs': row_logs[-30:] if row_logs else []  # Return last 30 logs
        }
        
        if saved_count == 0:
            response_data['message'] = f'⚠️ No rows imported. {skipped_count} rows skipped. Please ensure you have added data starting from Row 6.'
            response_data['status'] = 'error'
            
        return JsonResponse(response_data)

    except Exception as e:
        import traceback
        return JsonResponse({
            'status': 'error', 
            'message': f'Error processing file: {str(e)}',
            'traceback': traceback.format_exc()
        })

def plot_resale_list(request):
    session_id = request.session.get('Admin_id')

    if not session_id:
        return render(request,'home_page/Adminlogin.html')

    try:
        admin_obj = Admin_Login.objects.get(id=session_id)
    except Admin_Login.DoesNotExist:
        return render(request,'home_page/Adminlogin.html')

    base_qs = PlotSaleProperty.objects.filter(is_deleted=False)
    total_properties = base_qs.count()
    properties = base_qs

    # Get filter parameters
    search = request.GET.get('search')
    city = request.GET.get('city')
    locality = request.GET.get('locality')
    plot_type = request.GET.get('plot_type')
    road_facing = request.GET.get('road_facing')
    corner_plot = request.GET.get('corner_plot')
    loan = request.GET.get('loan')
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    from_date = request.GET.get('from_date')
    to_date = request.GET.get('to_date')

    # Apply Filters
    if search:
        properties = properties.filter(
            Q(plot_property_id__icontains=search) |
            Q(property_title__icontains=search) |
            Q(plot_title__icontains=search) |
            Q(plot_city__icontains=search) |
            Q(plot_locality__icontains=search) |
            Q(plot_owner_name__icontains=search) |
            Q(plot_owner_contact__icontains=search)
        )

    if city:
        properties = properties.filter(plot_city__icontains=city)
    if locality:
        properties = properties.filter(plot_locality__icontains=locality)
    if plot_type:
        properties = properties.filter(resale_plot_type__icontains=plot_type)
    if road_facing:
        properties = properties.filter(plot_road_facing__icontains=road_facing)
    if corner_plot:
        properties = properties.filter(corner_plot__iexact=corner_plot) 
    if loan:
        properties = properties.filter(loan_on_property__iexact=loan) 
    if min_price:
        properties = properties.filter(plot_price__gte=min_price)
    if max_price:
        properties = properties.filter(plot_price__lte=max_price)
    if from_date:
        properties = properties.filter(created_at__date__gte=from_date)
    if to_date:
        properties = properties.filter(created_at__date__lte=to_date)

    properties = properties.order_by('-created_at')

    # Dashboard Statistics
    active_listings = base_qs.filter(plot_price__gt=0).count()
    residential_count = base_qs.filter(resale_plot_type__icontains='residential').count()
    commercial_count = base_qs.filter(resale_plot_type__icontains='commercial').count()
    agricultural_count = base_qs.filter(resale_plot_type__icontains='agricultural').count()
    finance_ready_count = base_qs.filter(loan_on_property__iexact='yes').count() 

    uploaded_files = list(
        base_qs.exclude(upload_file_name__isnull=True)
               .exclude(upload_file_name="")
               .values_list('upload_file_name', flat=True)
               .distinct()
    )

    context = {
        'admin_obj': admin_obj,
        'properties': properties,
        'total_properties': total_properties,
        'active_listings': active_listings,
        'residential_count': residential_count,
        'commercial_count': commercial_count,
        'agricultural_count': agricultural_count,
        'finance_ready_count': finance_ready_count,
        'uploaded_files': sorted(uploaded_files),
    }

    return render(request, 'admin_user/Reports/Resale/plot_list.html', context)


# ==========================================



 

def plot_sale_view(request, id):
    session_id = request.session.get('Admin_id')
    user_id    = request.session.get('User_id')
 
    if not session_id and not user_id:
        return redirect('login')
 
    prop = get_object_or_404(
        PlotSaleProperty.objects.prefetch_related('images', 'faqs'),
        plot_property_id=id
    )
 
    # Safety: regenerate FAQs if missing (old records before migration)
    if not prop.faqs.exists():
        prop.generate_auto_faqs()
 
    context = {
        'property': prop,  # Changed from 'prop' to 'property' to match the HTML
        'faqs': prop.faqs.all(),
    }
    return render(request, 'admin_user/Reports/Resale/plot_view.html', context)



@require_POST
def plot_sale_delete(request, id):

    try:

        deleter_name = _get_deleter_name(request)

        prop = get_object_or_404(
            PlotSaleProperty,
            plot_property_id=id,
            is_deleted=False
        )

        prop.is_deleted = True
        prop.deleted_at = timezone.now()
        prop.deleted_by = deleter_name
        prop.save()

        return JsonResponse({
            "status": "success",
            "message": f"{id} moved to recycle bin successfully."
        })

    except Exception as e:
        return JsonResponse({
            "status": "error",
            "message": str(e)
        })

@require_POST
def plot_sale_restore(request, id):

    updated = PlotSaleProperty.objects.filter(
        plot_property_id=id
    ).update(
        is_deleted=False,
        deleted_at=None,
        deleted_by=None
    )

    if updated:
        return JsonResponse({
            'status': 'success',
            'message': 'Plot restored successfully!'
        })

    return JsonResponse({
        'status': 'error',
        'message': 'Plot not found.'
    })

@require_POST
def plot_sale_hard_delete(request, id):

    deleted, _ = PlotSaleProperty.objects.filter(
        plot_property_id=id
    ).delete()

    if deleted:
        return JsonResponse({
            'status': 'success',
            'message': 'Property permanently deleted!'
        })

    return JsonResponse({
        'status': 'error',
        'message': 'Property not found.'
    })

    #####################END VIEW SECTION PLOT RESALE LISTING################


    ##############################START VIEW SECTION RESALE INDUSTRIAL LISTING#################

    

def safe_parse_date(date_str):
    if date_str:
        try:
            return datetime.strptime(date_str, '%Y-%m-%d').date()
        except ValueError:
            return None
    return None





def industrial_resale_add(request):
    admin_id = request.session.get('Admin_id')
    user_id = request.session.get('User_id')

    if not admin_id and not user_id:
        return redirect('login')

    try:
        # Resolve administrator identity profiles context
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

        if request.method == "POST":
            # Map string toggle parameters safely to systemic database booleans
            power_val = request.POST.get('power_supply') == 'True'
            crane_val = request.POST.get('crane_heavy_machinery') == 'True'
            housing_val = request.POST.get('worker_housing_nearby') == 'True'
            
            # Use your custom date parser or handle None safely
            
            
            # FIXED BOOLEANS TO MATCH MODEL
            loan_val = request.POST.get('loan_on_property') == 'True'
            tenants_val = request.POST.get('existing_tenants') == 'True'
            dispute_val = request.POST.get('legal_dispute') == 'True'
            tax_due_val = request.POST.get('government_tax_dues') == 'True'
            tax_cert_val = request.POST.get('tax_clearance_cert') == 'True'

            # Backend calculation for price per sqft (failsafe)
            try:
                price = float(request.POST.get('expected_price') or 0)
                area = float(request.POST.get('land_area') or 0)
                calc_price_per_sqft = round((price / area), 2) if area > 0 else None
            except ValueError:
                calc_price_per_sqft = None

            prop = IndustrialResaleProperty.objects.create(
                property_title=request.POST.get('property_title'),

                # Step 1: Specs
                property_type=request.POST.get('property_type'),
                land_area=request.POST.get('land_area') or 0,
                # Note: Make sure your model has an 'available_from' field. I added it to the dict based on your old view.
                power_supply=power_val,
                kva_capacity=request.POST.get('kva_capacity') or None,
                water_supply=request.POST.get('water_supply'),
                crane_heavy_machinery=crane_val,
                road_connectivity=request.POST.get('road_connectivity'),
                worker_housing_nearby=housing_val,

                # Step 2: Pricing & Legal
                expected_price=request.POST.get('expected_price') or None,
                price_per_sqft=request.POST.get('price_per_sqft') or calc_price_per_sqft,  # ADDED METRIC
                brokerage=request.POST.get('brokerage'),
                brokerage_percentage=request.POST.get('brokerage_percentage'),
                manual_brokerage=request.POST.get('manual_brokerage'),
                sanctioning_authority=request.POST.get('sanctioning_authority'),
                ownership_type=request.POST.get('ownership_type'),
                
                loan_on_property=loan_val,               # FIXED KEY
                loan_amount=request.POST.get('loan_amount') or None,
                existing_tenants=tenants_val,
                tenant_details=request.POST.get('tenant_details'),
                legal_dispute=dispute_val,
                dispute_details=request.POST.get('dispute_details'),
                government_tax_dues=tax_due_val,         # FIXED KEY
                tax_amount=request.POST.get('tax_amount') or None,
                tax_clearance_cert=tax_cert_val,
                property_description=request.POST.get('property_description'),

                # Step 3: File Document Streams
                compliance_docs=request.FILES.get('compliance_docs'),
                social_video=request.FILES.get('social_video'),

                # Step 4: Contact Information
                city=request.POST.get('city'),
                locality_area=request.POST.get('locality_area'),   # FIXED KEY
                Property_address=request.POST.get('Property_address'), # FIXED KEY
                owner_name=request.POST.get('owner_name'),
                owner_contact=request.POST.get('owner_contact'),
                owner_email=request.POST.get('owner_email'),
                owner_role=request.POST.get('owner_role'),
                residency_status=request.POST.get('residency_status'),

                # Audit Session Metadata Tracks
                uploaded_by_name=uploader_name,
                uploaded_by_email=uploader_email,
                uploaded_by_contact=uploader_phone,
                uploaded_by_role=uploader_role
            )

            # Saves multi-image selections
            images = request.FILES.getlist('property_images[]')
            for idx, img in enumerate(images):
                if idx >= 10:
                    break
                # Ensure you have an IndustrialResaleImage model ready
                IndustrialResaleImage.objects.create(property=prop, image=img)

            # Fire the FAQ generator logic
            prop.generate_auto_faqs()

            return JsonResponse({
                "status": "success",
                "message": f"Industrial Listing successfully built and posted live!"
            })

    except Exception as err:
        print("CRITICAL EXCEPTION ROUTED:", str(err))
        traceback.print_exc()
        return JsonResponse({"status": "error", "message": str(err)})

    context = {'admin_obj': admin if admin_id else user}
    return render(request, 'admin_user/industrial_resale.html', context)


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
            def parse_bool(val):
                return str(val).strip().lower() in ['yes', 'true', '1', 'on']

            # Update Step 1: Specs
            prop.property_type = request.POST.get('property_type')
            prop.land_area = request.POST.get('land_area') or 0.0
            
            prop.available_from = safe_parse_date(request.POST.get('available_from'))
          
            prop.power_supply = parse_bool(request.POST.get('power_supply'))
            prop.kva_capacity = request.POST.get('kva_capacity') or None
            prop.water_supply = request.POST.get('water_supply')
            prop.crane_heavy_machinery = parse_bool(request.POST.get('crane_heavy_machinery'))
            prop.road_connectivity = request.POST.get('road_connectivity')
            prop.worker_housing_nearby = parse_bool(request.POST.get('worker_housing_nearby'))

            # Update Step 2: Pricing & Legal
            prop.expected_price = request.POST.get('expected_price') or 0.0
            prop.brokerage = request.POST.get('brokerage')
            prop.brokerage_percentage = request.POST.get('brokerage_percentage')
            prop.manual_brokerage = request.POST.get('manual_brokerage')
            prop.sanctioning_authority = request.POST.get('sanctioning_authority')
            prop.ownership_type = request.POST.get('ownership_type')
            
            prop.has_loan = parse_bool(request.POST.get('has_loan'))
            prop.loan_amount = request.POST.get('loan_amount') or 0.0
            
            prop.existing_tenants = parse_bool(request.POST.get('existing_tenants'))
            prop.tenant_details = request.POST.get('tenant_details')
            
            prop.legal_dispute = parse_bool(request.POST.get('legal_dispute'))
            prop.dispute_details = request.POST.get('dispute_details')
            
            prop.tax_due = parse_bool(request.POST.get('tax_due'))
            prop.tax_amount = request.POST.get('tax_amount') or 0.0
            prop.tax_clearance_cert = parse_bool(request.POST.get('tax_clearance_cert'))
            
            prop.property_description = request.POST.get('property_description')

            # Update Step 3: Media & Files
            if 'compliance_docs' in request.FILES:
                prop.compliance_docs = request.FILES['compliance_docs']
            if 'social_video' in request.FILES:
                prop.social_video = request.FILES['social_video']

            # Update Step 4: Location & Contact
            prop.city = request.POST.get('city')
            prop.locality = request.POST.get('locality')
            prop.complete_address = request.POST.get('complete_address')
            prop.owner_name = request.POST.get('owner_name')
            prop.owner_contact = request.POST.get('owner_contact')
            prop.owner_email = request.POST.get('owner_email')
            prop.residency_status = request.POST.get('residency_status')

            # Save core property attributes
            prop.save()

            # Handle Deletion of Specific Old Images
            removed_image_ids = request.POST.getlist('removed_images[]')
            if removed_image_ids:
                from .models import IndustrialResaleImage  # Ensure imported
                IndustrialResaleImage.objects.filter(id__in=removed_image_ids, property=prop).delete()

            # Save New Images (Append up to 10 max)
            new_images = request.FILES.getlist('property_images[]')
            current_image_count = prop.images.count()

            for img in new_images:
                if current_image_count >= 10:
                    break
                from .models import IndustrialResaleImage
                IndustrialResaleImage.objects.create(property=prop, image=img)
                current_image_count += 1

            return JsonResponse({"status": "success", "message": "Industrial Property Updated Successfully"})

        except Exception as e:
            traceback.print_exc()
            return JsonResponse({"status": "error", "message": str(e)})

    # GET Request: Render edit template with pre-filled data
    context = {
        'prop': prop,
        # Determine uploader for display
        'admin_obj': Admin_Login.objects.filter(id=admin_id).first() if admin_id else None
    }
    return render(request, 'admin_user/Resale/industrial_edit.html', context)





def industrial_resale_list(request):
    session_id = request.session.get('Admin_id')
    if not session_id:
        return render(request, 'home_page/Adminlogin.html')
        
    admin_obj = Admin_Login.objects.get(id=session_id)
    base_qs = IndustrialResaleProperty.objects.filter(is_deleted=False)
    
    # ─── Filter Parameters ───
    search_query = request.GET.get('search', '').strip()
    city_query = request.GET.get('city', 'All Cities')
    prop_type_query = request.GET.get('property_type', 'All Types')
    power_query = request.GET.get('power_supply', 'Any Power Supply')
    legal_query = request.GET.get('legal_status', 'All')  # Newly added Legal filter
    from_date = request.GET.get('from_date', '')
    to_date = request.GET.get('to_date', '')

    # ─── Apply Filters ───
    if search_query:
        base_qs = base_qs.filter(
            Q(property_title__icontains=search_query) |
            Q(city__icontains=search_query) |
            Q(locality_area__icontains=search_query) |  # Aligned to new model
            Q(owner_name__icontains=search_query) |
            Q(id__icontains=search_query)
        )

    if city_query != 'All Cities':
        base_qs = base_qs.filter(city__iexact=city_query)
        
    if prop_type_query != 'All Types':
        base_qs = base_qs.filter(property_type__iexact=prop_type_query)
        
    if power_query == 'heavy':
        base_qs = base_qs.filter(power_supply=True, kva_capacity__gte=100)
    elif power_query == 'light':
        base_qs = base_qs.filter(power_supply=True, kva_capacity__lt=100)
        
    if legal_query == 'clear':
        # Must have no tax dues AND no legal disputes
        base_qs = base_qs.filter(government_tax_dues=False, legal_dispute=False)
    elif legal_query == 'dispute':
        # Has EITHER tax dues OR a legal dispute
        base_qs = base_qs.filter(Q(government_tax_dues=True) | Q(legal_dispute=True))
        
    if from_date and to_date:
        base_qs = base_qs.filter(created_at__date__gte=from_date, created_at__date__lte=to_date)

    # Sort listings chronologically
    properties_qs = base_qs.order_by('-created_at')

    # ─── EXPORT LOGIC (CSV / EXCEL) ───
    download_type = request.GET.get('download')
    if download_type in ['csv', 'excel']:
        # Exact headers matching the new model sequentially
        headers = [
            # System Control & Identification
            "ID", "Property Title", 
            # Step 1: Property Specs
            "Property Type", "Land Area", "Power Supply", "KVA Capacity", 
            "Water Supply", "Crane & Heavy Machinery", "Road Connectivity", "Worker Housing Nearby",
            # Step 2: Pricing & Legal
            "Expected Price", "Price Per Sqft", "Brokerage", "Brokerage Percentage", 
            "Manual Brokerage", "Sanctioning Authority", "Ownership Type", "Loan On Property", 
            "Loan Amount", "Existing Tenants", "Tenant Details", "Legal Dispute", 
            "Dispute Details", "Government Tax Dues", "Tax Amount", "Tax Clearance Cert", 
            "Property Description",
            # Step 3: Media & Compliance
            "Compliance Docs", "Social Video",
            # Step 4: Location & Contact
            "City", "Locality Area", "Property Address", "Owner Name", "Owner Contact", 
            "Owner Email", "Owner Role", "Residency Status",
            # Uploader Details
            "Uploaded By Name", "Uploaded By Role", "Uploaded By Email", "Uploaded By Contact", 
            "Upload File Name", 
            # Timestamp & Deletion Status
            "Created At", "Updated At", "Is Deleted", "Deleted At", "Deleted By"
        ]

        # Helper function to extract data sequentially for each property using exact model fields
        def get_row_data(prop):
            return [
                prop.id, prop.property_title,
                prop.property_type, prop.land_area,
                "Yes" if prop.power_supply else "No", prop.kva_capacity, prop.water_supply,
                "Yes" if prop.crane_heavy_machinery else "No", prop.road_connectivity,
                "Yes" if prop.worker_housing_nearby else "No", prop.expected_price, prop.price_per_sqft,
                prop.brokerage, prop.brokerage_percentage, prop.manual_brokerage,
                prop.sanctioning_authority, prop.ownership_type, "Yes" if prop.loan_on_property else "No",
                prop.loan_amount, "Yes" if prop.existing_tenants else "No", prop.tenant_details,
                "Yes" if prop.legal_dispute else "No", prop.dispute_details,
                "Yes" if prop.government_tax_dues else "No", prop.tax_amount,
                "Yes" if prop.tax_clearance_cert else "No", prop.property_description,
                prop.compliance_docs.name if prop.compliance_docs else "",
                prop.social_video.name if prop.social_video else "",
                prop.city, prop.locality_area, prop.Property_address, prop.owner_name,
                prop.owner_contact, prop.owner_email, prop.owner_role, prop.residency_status,
                prop.uploaded_by_name, prop.uploaded_by_role, prop.uploaded_by_email,
                prop.uploaded_by_contact, prop.upload_file_name,
                str(prop.created_at.replace(tzinfo=None)) if prop.created_at else "",
                str(prop.updated_at.replace(tzinfo=None)) if prop.updated_at else "",
                "Yes" if prop.is_deleted else "No",
                str(prop.deleted_at.replace(tzinfo=None)) if prop.deleted_at else "",
                prop.deleted_by
            ]

        if download_type == 'csv':
            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename="Industrial_Resale_Report.csv"'
            writer = csv.writer(response)
            writer.writerow(headers)
            for prop in properties_qs:
                writer.writerow(get_row_data(prop))
            return response

        elif download_type == 'excel':
            wb = openpyxl.Workbook()
            sheet = wb.active
            sheet.title = "Industrial Report Data"
            sheet.append(headers)
            for prop in properties_qs:
                sheet.append(get_row_data(prop))
            response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
            response['Content-Disposition'] = 'attachment; filename="Industrial_Resale_Report.xlsx"'
            wb.save(response)
            return response

    # ─── Pagination ───
    paginator = Paginator(properties_qs, 15)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # ─── Dynamic Statistical Compilations ───
    total_count = IndustrialResaleProperty.objects.filter(is_deleted=False).count()
    filtered_count = properties_qs.count()
    active_listings = properties_qs.filter(expected_price__gt=0).count()
    warehouse_count = properties_qs.filter(property_type__icontains='warehouse').count()
    compliance_passed = properties_qs.exclude(compliance_docs='').exclude(compliance_docs__isnull=True).count()

    # ─── Chart Data Aggregation ───
    small_cap = properties_qs.filter(land_area__lte=20000).count()
    mid_cap = properties_qs.filter(land_area__gt=20000, land_area__lte=80000).count()
    large_cap = properties_qs.filter(land_area__gt=80000).count()
    
    manufacturing = properties_qs.filter(property_type__icontains='manufacturing').count()
    cold_storage = properties_qs.filter(property_type__icontains='cold_storage').count()
    
    # Updated chart filters to match new model field definitions
    low_risk = properties_qs.filter(government_tax_dues=False, legal_dispute=False).count()
    medium_risk = properties_qs.filter(government_tax_dues=True, legal_dispute=False).count()
    high_risk = properties_qs.filter(legal_dispute=True).count()

    # Dropdown Options Pickers
    unique_cities = IndustrialResaleProperty.objects.filter(is_deleted=False).exclude(city__isnull=True).exclude(city='').values_list('city', flat=True).distinct()
    unique_property_types = IndustrialResaleProperty.objects.filter(is_deleted=False).exclude(property_type__isnull=True).exclude(property_type='').values_list('property_type', flat=True).distinct()
    uploaded_files = IndustrialResaleProperty.objects.filter(is_deleted=False).exclude(upload_file_name__isnull=True).exclude(upload_file_name='').values_list('upload_file_name', flat=True).distinct()

    context = {
        'admin_obj': admin_obj,
        'page_obj': page_obj,
        'properties': page_obj, 
        'total_properties': total_count, 
        'total_count': total_count,
        'filtered_count': filtered_count,
        'active_listings': active_listings,
        'warehouse_count': warehouse_count,
        'compliance_passed': compliance_passed,
        
        # Chart Data
        'capacity_labels': json.dumps(["Small (≤ 20k sqft)", "Mid (20-80k sqft)", "Large (80k+ sqft)"]),
        'capacity_data': json.dumps([small_cap, mid_cap, large_cap]),
        'type_labels': json.dumps(["Warehouse", "Manufacturing", "Cold Storage", "Other"]),
        'type_data': json.dumps([warehouse_count, manufacturing, cold_storage, filtered_count - (warehouse_count + manufacturing + cold_storage)]),
        'risk_labels': json.dumps(["Low Risk", "Medium Risk", "High Risk"]),
        'risk_data': json.dumps([low_risk, medium_risk, high_risk]),
        
        # Select Dropdowns
        'unique_cities': unique_cities,
        'unique_property_types': unique_property_types,
        'uploaded_files': uploaded_files,
        
        # Maintained Filter States (so they stay selected on page reload)
        'search_query': search_query,
        'city_query': city_query,
        'prop_type_query': prop_type_query,
        'power_query': power_query,
        'legal_query': legal_query,
    }
    return render(request, 'admin_user/Reports/Resale/industrial_list.html', context)



def industrial_resale_view(request, id):
    session_id = request.session.get('Admin_id')
    user_id    = request.session.get('User_id')

    if not session_id and not user_id:
        return redirect('login')

    # Fetch the property + prefetch related images and DB-stored FAQs
    prop = get_object_or_404(
        IndustrialResaleProperty.objects.prefetch_related('images', 'faqs'),
        id=id
    )

    # FAQs are now persisted in DB via generate_auto_faqs() called on save().
    # If for any reason they are missing (e.g. old record), regenerate on the fly.
    if not prop.faqs.exists():
        prop.generate_auto_faqs()

    context = {
        'prop': prop,
        'faqs': prop.faqs.all(),   # QuerySet from IndustrialResaleFAQ table
    }
    return render(request, 'admin_user/Resale/industrial_view.html', context)





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
        
        # Calling your existing helper function here
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
            uploader = data.get('uploader_text', '').strip()
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
            # Updated to match exact DB field name
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
def industrial_resale_hard_delete(request, id):
    """Permanently deletes the record from the database."""
    try:
        IndustrialResaleProperty.objects.filter(id=id).delete()
        return JsonResponse({'status': 'success', 'message': 'Permanently deleted!'})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)})


@require_POST
def industrial_resale_restore(request, id):
    """Restores the record from the Recycle Bin."""
    try:
        IndustrialResaleProperty.objects.filter(id=id).update(is_deleted=False, deleted_at=None, deleted_by=None)
        return JsonResponse({'status': 'success', 'message': 'Industrial property restored!'})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)})

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





# =========================================================================
# 1. TEMPLATE DOWNLOADER
# =========================================================================
def download_industrial_resale_template(request):
    wb = openpyxl.Workbook()
    sheet = wb.active
    sheet.title = "Industrial Resale"

    # --- STYLING DEFINITIONS ---
    section_fill = PatternFill(start_color="1E3A8A", end_color="1E3A8A", fill_type="solid")
    header_fill = PatternFill(start_color="DBEAFE", end_color="DBEAFE", fill_type="solid")
    required_fill = PatternFill(start_color="FEF08A", end_color="FEF08A", fill_type="solid")
    
    white_font_bold = Font(color="FFFFFF", bold=True, size=12)
    dark_font_bold = Font(color="1E293B", bold=True, size=11)
    
    center_align = Alignment(horizontal="center", vertical="center", wrap_text=True)
    thin_border = Border(
        left=Side(style='thin', color='CBD5E1'), right=Side(style='thin', color='CBD5E1'), 
        top=Side(style='thin', color='CBD5E1'), bottom=Side(style='thin', color='CBD5E1')
    )

    # Row 1: Section Headings spanning across cell ranges (Total 47 columns)
    section_headers = [""] * 47
    section_headers[0] = "📋 System & Identification"        # Cols 1-2
    section_headers[2] = "📋 Property Specs"                # Cols 3-10
    section_headers[10] = "📋 Pricing & Legal"              # Cols 11-27
    section_headers[27] = "📋 Media & Compliance"           # Cols 28-29
    section_headers[29] = "📋 Location & Contact"           # Cols 30-37
    section_headers[37] = "📋 Uploader Details"             # Cols 38-42
    section_headers[42] = "📋 System Timestamps & Log"      # Cols 43-47
    
    sheet.append(section_headers)
    
    # Merge Section Blocks precisely to match the exact field counts (Shifted left by 1)
    sheet.merge_cells('A1:B1')   # System (2)
    sheet.merge_cells('C1:J1')   # Specs (8) - Removed available_from
    sheet.merge_cells('K1:AA1')  # Pricing & Legal (17)
    sheet.merge_cells('AB1:AC1') # Media (2)
    sheet.merge_cells('AD1:AK1') # Location (8)
    sheet.merge_cells('AL1:AP1') # Uploader (5)
    sheet.merge_cells('AQ1:AU1') # Timestamps (5)

    # Apply Styling to Row 1
    for cell in sheet[1]:
        cell.fill = section_fill
        cell.font = white_font_bold
        cell.alignment = center_align
        cell.border = thin_border
    sheet.row_dimensions[1].height = 30

    # Row 2: Headers (available_from removed)
    headers = [
        # System Control (Cols 0-1)
        "id", "property_title",
        # Step 1: Specs (Cols 2-9)
        "property_type *", "land_area *", "power_supply",
        "kva_capacity", "water_supply", "crane_heavy_machinery", "road_connectivity *",
        "worker_housing_nearby", 
        # Step 2: Pricing & Legal (Cols 10-26)
        "expected_price *", "price_per_sqft", "brokerage", "brokerage_percentage",
        "manual_brokerage", "sanctioning_authority", "ownership_type *", "loan_on_property",
        "loan_amount", "existing_tenants", "tenant_details", "legal_dispute",
        "dispute_details", "government_tax_dues", "tax_amount", "tax_clearance_cert",
        "property_description *", 
        # Step 3: Media (Cols 27-28)
        "compliance_docs", "social_video",
        # Step 4: Location & Contact (Cols 29-36)
        "city *", "locality_area *", "Property_address *", "owner_name *", 
        "owner_contact *", "owner_email *", "owner_role *", "residency_status *",
        # Uploader Details (Cols 37-41)
        "uploaded_by_name", "uploaded_by_role", "uploaded_by_email", "uploaded_by_contact", 
        "upload_file_name",
        # Meta Timestamps (Cols 42-46)
        "created_at", "updated_at", "is_deleted", "deleted_at", "deleted_by"
    ]
    sheet.append(headers)

    # Apply Styling to Row 2
    for cell in sheet[2]:
        cell.font = dark_font_bold
        cell.alignment = center_align
        cell.border = thin_border
        cell.fill = required_fill if "*" in str(cell.value) else header_fill
        sheet.column_dimensions[cell.column_letter].width = len(str(cell.value)) + 8

    sheet.row_dimensions[2].height = 25

    # Row 3: Sample Data (available_from date removed)
    sample_data = [
        "", "",
        "warehouse", 5000, "yes",
        250, "corporation", "no", "highway",
        "yes", 
        15000000, 3000.00, "Yes", "2",
        "", "MIDC", "freehold", "no",
        0, "no", "", "no",
        "", "no", 0, "yes",
        "Good industrial shed near highway", 
        "", "",
        "Nagpur", "Hingna MIDC", "Plot 42, Phase 1", "Ramesh Verma", 
        "9876543210", "ramesh@example.com", "Owner", "resident",
        "Admin", "System Admin", "admin@example.com", "9999999999", 
        "bulk_upload_01.csv",
        "", "", "False", "", ""
    ]
    sheet.append(sample_data)
    
    for cell in sheet[3]:
        cell.border = thin_border
        cell.alignment = Alignment(horizontal="center", vertical="center")

    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="PropCRM_Industrial_Resale_Template.xlsx"'
    wb.save(response)
    return response


# =========================================================================
# 2. BULK EXCEL IMPORTER
# =========================================================================
def import_industrial_resale_excel(request):
    session_id = request.session.get('Admin_id')
    user_id = request.session.get('User_id')

    if not session_id and not user_id:
        return JsonResponse({"status": "error", "message": "Unauthorized access"})

    if request.method == "POST" and request.FILES.get('industrial_file'):
        try:
            if session_id:
                uploader = Admin_Login.objects.get(id=session_id)
                u_name, u_email, u_phone, u_role = uploader.name, uploader.email, uploader.phone, "Admin"
            else:
                uploader = User_Details.objects.get(id=user_id)
                u_name, u_email, u_phone, u_role = uploader.name, uploader.email, uploader.phone, uploader.role

            excel_file = request.FILES['industrial_file']
            file_name_str = excel_file.name

            if IndustrialResaleProperty.objects.filter(upload_file_name=file_name_str, is_deleted=False).exists():
                return JsonResponse({"status": "duplicate_filename_and_data", "message": f"A file named '{file_name_str}' has already been processed."})

            wb = openpyxl.load_workbook(excel_file, data_only=True)
            sheet = wb.active

            if sheet.max_row < 3:
                return JsonResponse({"status": "error", "message": "Uploaded spreadsheet lacks data rows."})

            row2_values = [str(cell.value).strip() if cell.value else "" for cell in sheet[2]]
            
            # Expected Headers (47 columns)
            expected_headers = [
                "id", "property_title",
                "property_type *", "land_area *", "power_supply",
                "kva_capacity", "water_supply", "crane_heavy_machinery", "road_connectivity *",
                "worker_housing_nearby", "expected_price *", "price_per_sqft", "brokerage", "brokerage_percentage",
                "manual_brokerage", "sanctioning_authority", "ownership_type *", "loan_on_property",
                "loan_amount", "existing_tenants", "tenant_details", "legal_dispute",
                "dispute_details", "government_tax_dues", "tax_amount", "tax_clearance_cert",
                "property_description *", "compliance_docs", "social_video",
                "city *", "locality_area *", "Property_address *", "owner_name *", 
                "owner_contact *", "owner_email *", "owner_role *", "residency_status *",
                "uploaded_by_name", "uploaded_by_role", "uploaded_by_email", "uploaded_by_contact", 
                "upload_file_name", "created_at", "updated_at", "is_deleted", "deleted_at", "deleted_by"
            ]

            for idx, key in enumerate(expected_headers):
                if idx >= len(row2_values) or row2_values[idx].lower() != key.lower():
                    return JsonResponse({"status": "error", "message": f"Column structure mismatch at Column {idx+1}. Expected '{key}'."})

            def parse_bool(val):
                return str(val).strip().lower() in ['yes', 'true', '1']

            def safe_float(val):
                try: return float(val) if val else 0.0
                except ValueError: return 0.0

            all_rows_data_str = ""
            records_to_create = []

            for row_idx, row in enumerate(sheet.iter_rows(min_row=3, values_only=True), start=3):
                if not row or not any(row): continue

                # Validation Indices Shifted
                required_indices = [
                    2,   # property_type
                    3,   # land_area
                    8,   # road_connectivity
                    10,  # expected_price
                    16,  # ownership_type
                    26,  # property_description
                    29,  # city
                    30,  # locality_area
                    31,  # Property_address
                    32,  # owner_name
                    33,  # owner_contact
                    34,  # owner_email
                    35,  # owner_role
                    36   # residency_status
                ]
                
                for ri in required_indices:
                    if row[ri] is None or str(row[ri]).strip() == "":
                        return JsonResponse({"status": "error", "message": f"Data Validation Error at Row {row_idx}: Column '{expected_headers[ri]}' cannot be blank."})

                all_rows_data_str += "".join([str(val) for val in row])

                # Mapped with shifted indices
                records_to_create.append({
                    "property_type": str(row[2]).strip(),
                    "land_area": safe_float(row[3]),
                    "power_supply": parse_bool(row[4]),
                    "kva_capacity": row[5] or None,
                    "water_supply": str(row[6]).strip() if row[6] else None,
                    "crane_heavy_machinery": parse_bool(row[7]),
                    "road_connectivity": str(row[8]).strip(),
                    "worker_housing_nearby": parse_bool(row[9]),
                    "expected_price": safe_float(row[10]),
                    "price_per_sqft": safe_float(row[11]),
                    "brokerage": str(row[12]).strip() if row[12] else "No",
                    "brokerage_percentage": str(row[13]).strip() if row[13] else None,
                    "manual_brokerage": str(row[14]).strip() if row[14] else None,
                    "sanctioning_authority": str(row[15]).strip() if row[15] else None,
                    "ownership_type": str(row[16]).strip(),
                    "loan_on_property": parse_bool(row[17]),
                    "loan_amount": safe_float(row[18]),
                    "existing_tenants": parse_bool(row[19]),
                    "tenant_details": str(row[20]).strip() if row[20] else None,
                    "legal_dispute": parse_bool(row[21]),
                    "dispute_details": str(row[22]).strip() if row[22] else None,
                    "government_tax_dues": parse_bool(row[23]),
                    "tax_amount": safe_float(row[24]),
                    "tax_clearance_cert": parse_bool(row[25]),
                    "property_description": str(row[26]).strip(),
                    "city": str(row[29]).strip(),
                    "locality_area": str(row[30]).strip(),
                    "Property_address": str(row[31]).strip(),
                    "owner_name": str(row[32]).strip(),
                    "owner_contact": str(row[33]).strip(),
                    "owner_email": str(row[34]).strip(),
                    "owner_role": str(row[35]).strip(),
                    "residency_status": str(row[36]).strip(),
                })

            combined_hash_fingerprint = hashlib.md5(all_rows_data_str.encode('utf-8')).hexdigest()
            if IndustrialResaleProperty.objects.filter(property_description__icontains=f"[MD5:{combined_hash_fingerprint}]", is_deleted=False).exists():
                return JsonResponse({"status": "duplicate_data_different_filename", "message": "Duplicate Content Rejected: This exact data matrix has already been imported."})

            for r in records_to_create:
                IndustrialResaleProperty.objects.create(
                    property_type=r["property_type"],
                    land_area=r["land_area"],
                    power_supply=r["power_supply"],
                    kva_capacity=r["kva_capacity"],
                    water_supply=r["water_supply"],
                    crane_heavy_machinery=r["crane_heavy_machinery"],
                    road_connectivity=r["road_connectivity"],
                    worker_housing_nearby=r["worker_housing_nearby"],
                    expected_price=r["expected_price"],
                    price_per_sqft=r["price_per_sqft"],
                    brokerage=r["brokerage"],
                    brokerage_percentage=r["brokerage_percentage"],
                    manual_brokerage=r["manual_brokerage"],
                    sanctioning_authority=r["sanctioning_authority"],
                    ownership_type=r["ownership_type"],
                    loan_on_property=r["loan_on_property"],
                    loan_amount=r["loan_amount"],
                    existing_tenants=r["existing_tenants"],
                    tenant_details=r["tenant_details"],
                    legal_dispute=r["legal_dispute"],
                    dispute_details=r["dispute_details"],
                    government_tax_dues=r["government_tax_dues"],
                    tax_amount=r["tax_amount"],
                    tax_clearance_cert=r["tax_clearance_cert"],
                    property_description=f"{r['property_description']} [MD5:{combined_hash_fingerprint}]",
                    city=r["city"],
                    locality_area=r["locality_area"],
                    Property_address=r["Property_address"],
                    owner_name=r["owner_name"],
                    owner_contact=r["owner_contact"],
                    owner_email=r["owner_email"],
                    owner_role=r["owner_role"],
                    residency_status=r["residency_status"],
                    upload_file_name=file_name_str,
                    uploaded_by_name=u_name,
                    uploaded_by_email=u_email,
                    uploaded_by_contact=u_phone,
                    uploaded_by_role=u_role
                )

            return JsonResponse({"status": "success", "message": f"Successfully parsed and saved {len(records_to_create)} industrial rows."})

        except Exception as e:
            traceback.print_exc()
            return JsonResponse({"status": "error", "message": f"Parsing Error encountered: {str(e)}"})

    return JsonResponse({"status": "error", "message": "Invalid parameters submitted."})


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
        
        # --- A. Safely convert primary configuration metrics ---
        try:
            builtup_val = float(request.POST.get('builtup_area') or 0.0)
        except ValueError:
            builtup_val = 0.0

        try:
            carpet_val = float(request.POST.get('carpet_area') or 0.0)
        except ValueError:
            carpet_val = 0.0

        try:
            price_val = float(request.POST.get('expected_price') or 0.0)
        except ValueError:
            price_val = 0.0

        # --- B. Safely handle optional/conditional numerical fields ---
        try:
            plot_area_raw = request.POST.get('plot_area')
            plot_area_val = float(plot_area_raw) if plot_area_raw and plot_area_raw.strip() else None
        except ValueError:
            plot_area_val = None

        try:
            loan_amount_raw = request.POST.get('loan_amount')
            loan_amount_val = float(loan_amount_raw) if loan_amount_raw and loan_amount_raw.strip() else None
        except ValueError:
            loan_amount_val = None

        try:
            pending_tax_raw = request.POST.get('pending_tax_amount')
            pending_tax_val = float(pending_tax_raw) if pending_tax_raw and pending_tax_raw.strip() else None
        except ValueError:
            pending_tax_val = None

        # ─── C. Create the Property Object ───────────────────
        prop = ResaleResidentialProperty(
            # Basic Information
            property_title   = request.POST.get('title') or None, 
            property_type    = request.POST.get('property_type'),
            zone             = request.POST.get('zone'),
            society_type     = request.POST.get('society_type'),
            water_type       = request.POST.get('water_type'),
            furnishing_type  = request.POST.get('furnishing_type'),
            age_of_property  = request.POST.get('age_of_property'),
            facing_direction = request.POST.get('facing_direction'), 

            # Property Configuration
            bhk              = request.POST.get('bhk'),
            bathrooms        = int(request.POST.get('bathrooms') or 1),
            balconies        = int(request.POST.get('balconies') or 0),
            covered_parking  = int(request.POST.get('covered_parking') or 0),
            open_parking     = int(request.POST.get('open_parking') or 0),

            # Measurements
            builtup_area     = builtup_val,
            carpet_area      = carpet_val,
            plot_area        = plot_area_val,
            floor_no         = int(request.POST.get('floor_no') or 0),
            total_floors     = int(request.POST.get('total_floors') or 0),

            # Ownership & Legal
            ownership_type      = request.POST.get('ownership_type'),
            num_owners          = request.POST.get('num_owners'),
            loan_on_property    = request.POST.get('loan_on_property', 'no'), 
            loan_amount         = loan_amount_val,
            existing_tenants    = request.POST.get('existing_tenants', 'no'), 
            tenant_details      = request.POST.get('tenant_details') or None,
            any_legal_dispute   = request.POST.get('any_legal_dispute', 'no'), 
            dispute_details     = request.POST.get('dispute_details') or None,
            government_tax_dues = request.POST.get('government_tax_dues', 'no'), 
            pending_tax_amount  = pending_tax_val,

            # Pricing & Description (FIXED: Linked directly to matching HTML input name properties)
            expected_price       = price_val,
            price_negotiable     = request.POST.get('is_negotiable', 'yes'), 
            brokerage            = request.POST.get('brokerage') or None,
            brokerage_percentage = request.POST.get('brokerage_percentage') or None,
            manual_brokerage     = request.POST.get('manual_brokerage') or None,
            property_description = request.POST.get('property_description'), 

            # Amenities & Facilities 
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
            owner_role         = request.POST.get('owner_role'), 
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

        # --- E. Return valid JSON for your SweetAlert success box ---
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
        properties = properties.filter(price_negotiable=negotiable) # Synced field name

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
    # KPI STATS (Calculated using correct DB layout keys)
    # ════════════════════════════════════════════════════════════════════════
    total_count = all_properties.count()

    # ── Row 1 — Inventory ────────────────────────────────────────────────────
    total_negotiable  = all_properties.filter(price_negotiable='yes').count() # Synced
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
    total_with_loan = all_properties.filter(loan_on_property='yes').count() # Synced

    # ── Row 3 — Legal & Status ───────────────────────────────────────────────
    no_dispute_count  = all_properties.filter(any_legal_dispute='no').count() # Synced
    dispute_count     = all_properties.filter(any_legal_dispute='yes').count() # Synced
    tax_pending_count = all_properties.filter(government_tax_dues='yes').count() # Synced
    tenant_occupied   = all_properties.filter(existing_tenants='yes').count() # Synced
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

    return render(request, 'admin_user/Reports/Resale/residential_resale_list.html', context)




def resale_residential_edit(request, id):
    # ── 1. Session Check ──────────────────────────────────
    uploader = _get_uploader(request)
    if uploader is None:
        return redirect('login')

    # ── 2. Get Property Instance ──────────────────────────
    prop = get_object_or_404(ResaleResidentialProperty, id=id)

    # ── 3. Handle POST (UPDATE DATA) ──────────────────────
    if request.method == "POST":
        # --- A. Safe Numeric Conversion & Validation ---
        try: builtup_val = float(request.POST.get('builtup_area') or 0.0)
        except ValueError: builtup_val = 0.0

        try: carpet_val = float(request.POST.get('carpet_area') or 0.0)
        except ValueError: carpet_val = 0.0

        try: price_val = float(request.POST.get('expected_price') or 0.0)
        except ValueError: price_val = 0.0

        try:
            plot_raw = request.POST.get('plot_area')
            plot_val = float(plot_raw) if plot_raw and plot_raw.strip() else None
        except ValueError: plot_val = None

        try:
            loan_raw = request.POST.get('loan_amount')
            loan_val = float(loan_raw) if loan_raw and loan_raw.strip() else None
        except ValueError: loan_val = None

        try:
            tax_raw = request.POST.get('pending_tax_amount')
            tax_val = float(tax_raw) if tax_raw and tax_raw.strip() else None
        except ValueError: tax_val = None

        # --- B. Map Fields Sequentially as per Database Model Layout ---
        # Basic Information
        prop.property_title   = request.POST.get('property_title') or None  # Empty allows fallback title builder
        prop.property_type    = request.POST.get('property_type')
        prop.zone             = request.POST.get('zone')
        prop.society_type     = request.POST.get('society_type')
        prop.water_type       = request.POST.get('water_type')
        prop.furnishing_type  = request.POST.get('furnishing_type')
        prop.age_of_property  = request.POST.get('age_of_property')
        prop.facing_direction = request.POST.get('facing_direction')

        # Property Configuration
        prop.bhk             = request.POST.get('bhk')
        prop.bathrooms       = int(request.POST.get('bathrooms') or 1)
        prop.balconies       = int(request.POST.get('balconies') or 0)
        prop.covered_parking = int(request.POST.get('covered_parking') or 0)
        prop.open_parking    = int(request.POST.get('open_parking') or 0)

        # Measurements
        prop.builtup_area = builtup_val
        prop.carpet_area  = carpet_val
        prop.plot_area    = plot_val
        prop.floor_no     = int(request.POST.get('floor_no') or 0)
        prop.total_floors = int(request.POST.get('total_floors') or 0)

        # Ownership & Legal
        prop.ownership_type      = request.POST.get('ownership_type')
        prop.num_owners          = request.POST.get('num_owners')
        prop.loan_on_property    = request.POST.get('loan_on_property', 'no')
        prop.loan_amount         = loan_val if prop.loan_on_property == 'yes' else None
        prop.existing_tenants    = request.POST.get('existing_tenants', 'no')
        prop.tenant_details      = request.POST.get('tenant_details') if prop.existing_tenants == 'yes' else None
        prop.any_legal_dispute   = request.POST.get('any_legal_dispute', 'no')
        prop.dispute_details     = request.POST.get('dispute_details') if prop.any_legal_dispute == 'yes' else None
        prop.government_tax_dues = request.POST.get('government_tax_dues', 'no')
        prop.pending_tax_amount  = tax_val if prop.government_tax_dues == 'yes' else None

        # Pricing & Description
        prop.expected_price       = price_val
        prop.price_negotiable     = request.POST.get('price_negotiable', 'yes')
        prop.brokerage            = request.POST.get('brokerage') or None
        prop.brokerage_percentage = request.POST.get('brokerage_percentage') or None
        prop.manual_brokerage     = request.POST.get('manual_brokerage') or None
        prop.property_description = request.POST.get('property_description')

        # Amenities & Facilities
        prop.nearby_facilities = ', '.join(request.POST.getlist('facilities[]'))
        prop.amenities         = ', '.join(request.POST.getlist('amenities[]'))

        # Address
        prop.city             = request.POST.get('city')
        prop.locality         = request.POST.get('locality')
        prop.building_name    = request.POST.get('building_name') or None
        prop.complete_address = request.POST.get('complete_address')

        # Owner Contact Info
        prop.owner_name         = request.POST.get('owner_name')
        prop.owner_contact      = request.POST.get('owner_contact')
        prop.owner_email        = request.POST.get('owner_email')
        prop.owner_role         = request.POST.get('owner_role')
        prop.residential_status = request.POST.get('residential_status')

        # File Upload Fields
        if request.FILES.get('floor_plan'):
            prop.floor_plan = request.FILES.get('floor_plan')
        if request.FILES.get('property_video'):
            prop.property_video = request.FILES.get('property_video')

        # Save updates safely (executes system automated formulas for title, price/sqft, and programmatic FAQs)
        prop.save()

        # --- C. Handle Dynamic Image Deletion Array ---
        deleted_images = request.POST.getlist('deleted_images[]')
        if deleted_images:
            ResalePropertyImage.objects.filter(id__in=deleted_images, property=prop).delete()

        # --- D. Handle New Image Queue Processing Array ---
        new_images = request.FILES.getlist('property_images')
        for img in new_images:
            ResalePropertyImage.objects.create(property=prop, image=img)

        return JsonResponse({
            "status": "success",
            "message": "Resale Residential Property Updated Successfully"
        })

    # ── 4. Handle GET (LOAD EDIT FORM) ───────────────────
    # Stored string splitters mapping tags back to array lists for template rendering checks
    prop_facilities_list = [f.strip() for f in prop.nearby_facilities.split(',')] if prop.nearby_facilities else []
    prop_amenities_list = [a.strip() for a in prop.amenities.split(',')] if prop.amenities else []
    existing_images = prop.images.all()

    context = {
        "prop": prop,
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

    # Fetch Resale Residential Object via PK
    prop = get_object_or_404(ResaleResidentialProperty, pk=pk)

    # Convert comma-separated string datasets into lists for badge generation loop arrays
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


# ═════════════════════════════════════════════════════════════
# SINGLE SOFT DELETE
# ═════════════════════════════════════════════════════════════
@require_POST
def resale_residential_delete(request, pk):
    uploader = _get_uploader(request)
    if uploader is None:
        return redirect('login')

    deleter_name = _get_deleter_name(request)

    prop = get_object_or_404(
        ResaleResidentialProperty,
        pk=pk,
        is_deleted=False
    )

    prop.is_deleted = True
    prop.deleted_at = timezone.now()
    prop.deleted_by = deleter_name
    prop.save(update_fields=['is_deleted', 'deleted_at', 'deleted_by'])

    return JsonResponse({
        "status": "success",
        "message": f"{prop.property_id} moved to Recycle Bin successfully!"
    })


# ═════════════════════════════════════════════════════════════
# RESTORE SINGLE PROPERTY
# ═════════════════════════════════════════════════════════════
@require_POST
def resale_restore(request, id):

    uploader = _get_uploader(request)
    if uploader is None:
        return JsonResponse({
            'status': 'error',
            'message': 'Unauthorized access.'
        })

    prop = get_object_or_404(
        ResaleResidentialProperty,
        id=id
    )

    prop.is_deleted = False
    prop.deleted_at = None
    prop.deleted_by = None
    prop.save(update_fields=['is_deleted', 'deleted_at', 'deleted_by'])

    return JsonResponse({
        'status': 'success',
        'message': f'{prop.property_id} restored successfully!'
    })


# ═════════════════════════════════════════════════════════════
# HARD DELETE SINGLE PROPERTY
# ═════════════════════════════════════════════════════════════
@require_POST
def resale_hard_delete(request, id):

    uploader = _get_uploader(request)
    if uploader is None:
        return JsonResponse({
            'status': 'error',
            'message': 'Unauthorized access.'
        })

    prop = get_object_or_404(
        ResaleResidentialProperty,
        id=id
    )

    property_id = prop.property_id

    # Delete related images automatically
    prop.images.all().delete()

    # Delete property
    prop.delete()

    return JsonResponse({
        'status': 'success',
        'message': f'{property_id} permanently deleted!'
    })


# ═════════════════════════════════════════════════════════════
# BULK DELETE / RECYCLE BIN SYSTEM
# ═════════════════════════════════════════════════════════════
@require_POST
def resale_residential_bulk_delete(request):

    uploader = _get_uploader(request)
    if uploader is None:
        return JsonResponse({
            'status': 'error',
            'message': 'Unauthorized access.'
        })

    deleter_name = _get_deleter_name(request)

    try:
        data = json.loads(request.body)

        delete_type = data.get('delete_type')

        # Only active records
        properties = ResaleResidentialProperty.objects.filter(
            is_deleted=False
        )

        # ═══════════════════════════════════════
        # DELETE ALL
        # ═══════════════════════════════════════
        if delete_type == 'delete_all':

            count = properties.count()

            properties.update(
                is_deleted=True,
                deleted_at=timezone.now(),
                deleted_by=deleter_name
            )

            return JsonResponse({
                'status': 'success',
                'message': f'{count} resale properties moved to recycle bin.'
            })

        # ═══════════════════════════════════════
        # CURRENT PAGE DELETE
        # ═══════════════════════════════════════
        elif delete_type == 'current_page':

            page_ids = data.get('page_ids', [])

            target_props = properties.filter(id__in=page_ids)

            count = target_props.count()

            target_props.update(
                is_deleted=True,
                deleted_at=timezone.now(),
                deleted_by=deleter_name
            )

            return JsonResponse({
                'status': 'success',
                'message': f'{count} resale properties moved to recycle bin.'
            })

        # ═══════════════════════════════════════
        # DATE RANGE DELETE
        # ═══════════════════════════════════════
        elif delete_type == 'date_range':

            from_date = data.get('from_date')
            to_date = data.get('to_date')

            if not from_date or not to_date:
                return JsonResponse({
                    'status': 'error',
                    'message': 'From date and To date are required.'
                })

            target_props = properties.filter(
                created_at__date__range=[from_date, to_date]
            )

            count = target_props.count()

            target_props.update(
                is_deleted=True,
                deleted_at=timezone.now(),
                deleted_by=deleter_name
            )

            return JsonResponse({
                'status': 'success',
                'message': f'{count} resale properties deleted between selected dates.'
            })

        # ═══════════════════════════════════════
        # LAST 30 DAYS
        # ═══════════════════════════════════════
        elif delete_type == 'latest_month':

            thirty_days_ago = timezone.now() - timedelta(days=30)

            target_props = properties.filter(
                created_at__gte=thirty_days_ago
            )

            count = target_props.count()

            target_props.update(
                is_deleted=True,
                deleted_at=timezone.now(),
                deleted_by=deleter_name
            )

            return JsonResponse({
                'status': 'success',
                'message': f'{count} recent resale properties moved to recycle bin.'
            })

        # ═══════════════════════════════════════
        # OLD DATA
        # ═══════════════════════════════════════
        elif delete_type == 'old_data':

            six_months_ago = timezone.now() - timedelta(days=180)

            target_props = properties.filter(
                created_at__lt=six_months_ago
            )

            count = target_props.count()

            target_props.update(
                is_deleted=True,
                deleted_at=timezone.now(),
                deleted_by=deleter_name
            )

            return JsonResponse({
                'status': 'success',
                'message': f'{count} old resale properties moved to recycle bin.'
            })

        # ═══════════════════════════════════════
        # DELETE BY UPLOADER
        # ═══════════════════════════════════════
        elif delete_type == 'by_uploader':

            uploader_text = data.get('uploader_text', '').strip()

            if not uploader_text:
                return JsonResponse({
                    'status': 'error',
                    'message': 'Uploader name is required.'
                })

            target_props = properties.filter(
                Q(uploaded_by_name__icontains=uploader_text) |
                Q(uploaded_by_email__icontains=uploader_text) |
                Q(uploaded_by_role__icontains=uploader_text) |
                Q(uploaded_by_contact__icontains=uploader_text)
            )

            count = target_props.count()

            target_props.update(
                is_deleted=True,
                deleted_at=timezone.now(),
                deleted_by=deleter_name
            )

            return JsonResponse({
                'status': 'success',
                'message': f'{count} resale properties moved to recycle bin.'
            })

        # ═══════════════════════════════════════
        # DELETE BY FILE
        # ═══════════════════════════════════════
        elif delete_type == 'by_file':

            file_name = data.get('file_name', '').strip()

            if not file_name:
                return JsonResponse({
                    'status': 'error',
                    'message': 'File name is required.'
                })

            target_props = properties.filter(
                upload_file_name__iexact=file_name
            )

            count = target_props.count()

            if count == 0:
                return JsonResponse({
                    'status': 'error',
                    'message': f'No properties found for file: {file_name}'
                })

            target_props.update(
                is_deleted=True,
                deleted_at=timezone.now(),
                deleted_by=deleter_name
            )

            return JsonResponse({
                'status': 'success',
                'message': f'{count} resale properties moved to recycle bin.'
            })

        # ═══════════════════════════════════════
        # PERMANENT DELETE RECYCLE BIN
        # ═══════════════════════════════════════
        elif delete_type == 'permanent_deleted':

            deleted_props = ResaleResidentialProperty.objects.filter(
                is_deleted=True
            )

            count = deleted_props.count()

            # Delete related images first
            for prop in deleted_props:
                prop.images.all().delete()

            deleted_props.delete()

            return JsonResponse({
                'status': 'success',
                'message': f'{count} properties permanently deleted.'
            })

        else:
            return JsonResponse({
                'status': 'error',
                'message': 'Unknown delete criteria.'
            })

    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        })




def generate_row_hash(row_values):
    """Generates a secure MD5 signature unique to the actual structural data values inside a row."""
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

    file_name_string = str(excel_file.name).strip()
    if not file_name_string.endswith('.xlsx'):
        return JsonResponse({'status': 'error', 'message': 'Invalid format. Only .xlsx extensions allowed.'})

    try:
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

        # Strict sequential sequence mapping array matching your database schema layout
        expected_headers = [
            'property_title', 'property_type', 'zone', 'society_type', 'water_type', 'furnishing_type', 
            'age_of_property', 'facing_direction', 'bhk', 'bathrooms', 'balconies', 
            'covered_parking', 'open_parking', 'builtup_area', 'carpet_area', 'plot_area', 
            'floor_no', 'total_floors', 'ownership_type', 'num_owners', 'loan_on_property', 
            'loan_amount', 'existing_tenants', 'tenant_details', 'any_legal_dispute', 
            'dispute_details', 'government_tax_dues', 'pending_tax_amount', 'expected_price', 
            'price_per_sqft', 'price_negotiable', 'brokerage', 'brokerage_percentage', 
            'manual_brokerage', 'property_description', 'nearby_facilities', 'amenities', 
            'city', 'locality', 'building_name', 'complete_address', 'owner_name', 
            'owner_contact', 'owner_email', 'owner_role', 'residential_status'
        ]

        # FIXED: Look at Row 2 (ws[2]) for headers because Row 1 contains the merged Section titles!
        file_headers = [str(cell.value).strip().lower() for cell in ws[2] if cell.value is not None]

        missing_fields = [f for f in expected_headers if f not in file_headers]
        if missing_fields:
            return JsonResponse({
                'status': 'error',
                'message': f'Required column headers missing in Row 2: {", ".join(missing_fields)}'
            })

        # FIXED: Map column indexes based on Row 2 fields
        header_map = {str(cell.value).strip().lower(): idx for idx, cell in enumerate(ws[2]) if cell.value is not None}

        file_signature_match = ResaleResidentialProperty.objects.filter(
            uploaded_by_email=current_uploader_email,
            upload_file_name=file_name_string
        ).exists()

        imported = 0
        skipped = 0
        duplicate_records_skipped = 0

        # FIXED: Changed min_row=3 because actual row property details start on Row 3
        for row_idx, row in enumerate(ws.iter_rows(min_row=3, values_only=True), start=3):
            if not any(row):
                continue

            try:
                # Direct safe indexing assignment through map positions
                p_title      = row[header_map['property_title']]
                p_type       = row[header_map['property_type']]
                zone         = row[header_map['zone']]
                soc_type     = row[header_map['society_type']]
                wat_type     = row[header_map['water_type']]
                furnish      = row[header_map['furnishing_type']]
                age          = row[header_map['age_of_property']]
                facing_dir   = row[header_map['facing_direction']]
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
                loan_on_prop = row[header_map['loan_on_property']]
                loan_amt     = row[header_map['loan_amount']]
                tenants      = row[header_map['existing_tenants']]
                ten_details  = row[header_map['tenant_details']]
                dispute      = row[header_map['any_legal_dispute']]
                disp_details = row[header_map['dispute_details']]
                tax_dues     = row[header_map['government_tax_dues']]
                tax_amt      = row[header_map['pending_tax_amount']]
                price        = row[header_map['expected_price']]
                price_sqft   = row[header_map['price_per_sqft']]
                negotiable   = row[header_map['price_negotiable']]
                brokerage    = row[header_map['brokerage']]
                brok_pct     = row[header_map['brokerage_percentage']]
                man_brok     = row[header_map['manual_brokerage']]
                description  = row[header_map['property_description']]
                facilities   = row[header_map['nearby_facilities']]
                amenities    = row[header_map['amenities']]
                city         = row[header_map['city']]
                locality     = row[header_map['locality']]
                bld_name     = row[header_map['building_name']]
                address      = row[header_map['complete_address']]
                own_name     = row[header_map['owner_name']]
                own_cont     = row[header_map['owner_contact']]
                own_email    = row[header_map['owner_email']]
                own_role     = row[header_map['owner_role']]
                res_status   = row[header_map['residential_status']]

                # Strict mandatory field checks
                if not all([p_type, bhk, builtup, price, city, locality, address, own_name, own_cont, own_email]):
                    skipped += 1
                    continue

                # Fallback decimal casting wrappers to isolate data type validation anomalies
                try: builtup_val = float(builtup)
                except (ValueError, TypeError): builtup_val = 0.0

                try: carpet_val = float(carpet) if carpet else 0.0
                except (ValueError, TypeError): carpet_val = 0.0

                try: price_val = float(price)
                except (ValueError, TypeError): price_val = 0.0

                try: plot_val = float(plot) if plot else None
                except (ValueError, TypeError): plot_val = None

                try: loan_val = float(loan_amt) if loan_amt else None
                except (ValueError, TypeError): loan_val = None

                try: tax_val = float(tax_amt) if tax_amt else None
                except (ValueError, TypeError): tax_val = None

                try: price_sqft_val = float(price_sqft) if price_sqft else None
                except (ValueError, TypeError): price_sqft_val = None

                # Duplication guard trace
                is_row_duplicate = ResaleResidentialProperty.objects.filter(
                    property_type=str(p_type).strip().lower(),
                    bhk=str(bhk).strip().lower(),
                    builtup_area=builtup_val,
                    expected_price=price_val,
                    locality=str(locality).strip(),
                    owner_contact=str(own_cont).strip()
                ).exists()

                if is_row_duplicate:
                    duplicate_records_skipped += 1
                    continue

                # Build instance model properties matching your structural database schema constraints
                prop = ResaleResidentialProperty(
                    property_title=str(p_title).strip() if p_title and str(p_title).strip().lower() != 'auto generated by system' else None,
                    property_type=str(p_type).strip().lower(),
                    zone=str(zone).strip().lower() if zone else '',
                    society_type=str(soc_type).strip().lower() if soc_type else '',
                    water_type=str(wat_type).strip().lower() if wat_type else '',
                    furnishing_type=str(furnish).strip().lower() if furnish else '',
                    age_of_property=str(age).strip() if age else '',
                    facing_direction=str(facing_dir).strip() if facing_dir else '',
                    bhk=str(bhk).strip().lower(),
                    bathrooms=int(baths) if baths else 1,
                    balconies=int(balconies) if balconies else 0,
                    covered_parking=int(cov_parking) if cov_parking else 0,
                    open_parking=int(op_parking) if op_parking else 0,
                    builtup_area=builtup_val,
                    carpet_area=carpet_val,
                    plot_area=plot_val,
                    floor_no=int(floor_no) if floor_no else 0,
                    total_floors=int(tot_floors) if tot_floors else 1,
                    ownership_type=str(ownership).strip().lower() if ownership else 'freehold',
                    num_owners=str(num_owners).strip() if num_owners else '1',
                    loan_on_property=str(loan_on_prop).strip().lower() if loan_on_prop else 'no',
                    loan_amount=loan_val,
                    existing_tenants=str(tenants).strip().lower() if tenants else 'no',
                    tenant_details=str(ten_details).strip() if ten_details else None,
                    any_legal_dispute=str(dispute).strip().lower() if dispute else 'no',
                    dispute_details=str(disp_details).strip() if disp_details else None,
                    government_tax_dues=str(tax_dues).strip().lower() if tax_dues else 'no',
                    pending_tax_amount=tax_val,
                    expected_price=price_val,
                    price_per_sqft=price_sqft_val,
                    price_negotiable=str(negotiable).strip().lower() if negotiable else 'yes',
                    brokerage=str(brokerage).strip() if brokerage else None,
                    brokerage_percentage=str(brok_pct).strip() if brok_pct else None,
                    manual_brokerage=str(man_brok).strip() if man_brok else None,
                    property_description=str(description).strip() if description else '',
                    nearby_facilities=str(facilities).strip() if facilities else '',
                    amenities=str(amenities).strip() if amenities else '',
                    city=str(city).strip(),
                    locality=str(locality).strip(),
                    building_name=str(bld_name).strip() if bld_name else None,
                    complete_address=str(address).strip(),
                    owner_name=str(own_name).strip(),
                    owner_contact=str(own_cont).strip(),
                    owner_email=str(own_email).strip(),
                    owner_role=str(own_role).strip() if own_role else 'Owner',
                    residential_status=str(res_status).strip().lower() if res_status else 'resident',
                    
                    # Systemic session context metadata strings
                    uploaded_by_name=current_uploader_name,
                    uploaded_by_email=current_uploader_email,
                    uploaded_by_contact=current_uploader_contact,
                    uploaded_by_role=current_uploader_role,
                    upload_file_name=file_name_string
                )

                prop.save()
                imported += 1

            except Exception as e:
                skipped += 1
                continue

        if imported == 0 and file_signature_match:
            return JsonResponse({
                'status': 'duplicate', 
                'message': f'The file "{file_name_string}" was already processed by your user account context. No new records have been appended.'
            })

        return JsonResponse({
            'status': 'success',
            'imported': imported,
            'skipped': skipped,
            'duplicates': duplicate_records_skipped
        })

    except Exception as e:
        return JsonResponse({'status': 'error', 'message': f'Process Error: {str(e)}'})




def resale_residential_sample_excel(request):
    session_id = request.session.get('Admin_id')
    if not session_id:
        return redirect('login')

    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Resale Template"
    
    # Ensure grid lines show up clearly
    ws.views.sheetView[0].showGridLines = True

    # ── STYLING ENGINE DEFINITIONS ────────────────────────────────────────
    font_family = "Segoe UI"
    
    # Fonts
    section_font = Font(name=font_family, size=11, bold=True, color="FFFFFF")
    header_font = Font(name=font_family, size=10, bold=True, color="1E293B")
    data_font = Font(name=font_family, size=11, bold=False, color="000000")
    
    # Fills
    section_fill = PatternFill(start_color="4F46E5", end_color="4F46E5", fill_type="solid") # Corporate Indigo Block
    header_fill = PatternFill(start_color="F1F5F9", end_color="F1F5F9", fill_type="solid")  # Light Slate Header Row
    
    # Borders
    thin_border = Side(border_style="thin", color="CBD5E1")
    cell_border = Border(left=thin_border, right=thin_border, top=thin_border, bottom=thin_border)
    
    # Alignments
    center_align = Alignment(horizontal="center", vertical="center", wrap_text=True)
    left_align = Alignment(horizontal="left", vertical="center", wrap_text=True)

    # ── HARDCODED HORIZONTAL BLOCKS (Synchronized with DB layout) ──────────
    # Arranged precisely sequentially side-by-side matching your database model structure
    sections_config = [
        {
            "title": "STEP 1: BASIC INFO & CONFIGURATION",
            "fields": [
                ('property_title', 'Auto Generated By System'), ('property_type', 'apartment'), ('zone', 'north'), ('society_type', 'gated community'),
                ('water_type', 'municipal'), ('furnishing_type', 'semi-furnished'), ('age_of_property', '1-3 years'),
                ('facing_direction', 'North-East'), ('bhk', '3 BHK'), ('bathrooms', 2), ('balconies', 1),
                ('covered_parking', 1), ('open_parking', 0), ('builtup_area', 1450.00), ('carpet_area', 1120.00),
                ('plot_area', ''), ('floor_no', 4), ('total_floors', 12)
            ]
        },
        {
            "title": "STEP 2: LEGAL & PRICING DETAILS",
            "fields": [
                ('ownership_type', 'freehold'), ('num_owners', '1'), ('loan_on_property', 'no'),
                ('loan_amount', ''), ('existing_tenants', 'no'), ('tenant_details', ''),
                ('any_legal_dispute', 'no'), ('dispute_details', ''), ('government_tax_dues', 'no'),
                ('pending_tax_amount', ''), ('expected_price', 7500000.00), ('price_per_sqft', 5172.41),
                ('price_negotiable', 'yes'), ('brokerage', 'no'), ('brokerage_percentage', ''),
                ('manual_brokerage', ''), ('property_description', 'Spacious apartment layout.')
            ]
        },
        {
            "title": "STEP 3: AMENITIES & LOCATION",
            "fields": [
                ('nearby_facilities', 'School, Metro'), ('amenities', 'Lift, Security, Gym'), ('city', 'Nagpur'),
                ('locality', 'Dharampeth'), ('building_name', 'Sunshine Towers'),
                ('complete_address', 'Flat 402, Sunshine Towers, Dharampeth, Nagpur'), ('owner_name', 'Rahul Sharma'),
                ('owner_contact', '9876543210'), ('owner_email', 'rahul.sharma@example.com'),
                ('owner_role', 'Owner'), ('residential_status', 'resident')
            ]
        }
    ]

    # Flatten out arrays to compute complete ranges
    total_columns = sum(len(sec["fields"]) for sec in sections_config)
    
    # ── GENERATE ROW 1: MERGED SECTION BANNERS ────────────────────────────
    current_col = 1
    for sec in sections_config:
        sec_length = len(sec["fields"])
        start_cell = ws.cell(row=1, column=current_col)
        end_col_idx = current_col + sec_length - 1
        
        ws.merge_cells(start_row=1, start_column=current_col, end_row=1, end_column=end_col_idx)
        
        start_cell.value = sec["title"]
        start_cell.font = section_font
        start_cell.fill = section_fill
        start_cell.alignment = Alignment(horizontal="center", vertical="center")
        
        # Apply borders across merged blocks cleanly
        for col in range(current_col, end_col_idx + 1):
            ws.cell(row=1, column=col).border = cell_border
            
        current_col += sec_length
    ws.row_dimensions[1].height = 30

    # ── GENERATE ROW 2 & 3: DB FIELD HEADERS & SAMPLE DATA ────────────────
    current_col = 1
    for sec in sections_config:
        for field_name, sample_val in sec["fields"]:
            # Row 2: Database Headers
            header_cell = ws.cell(row=2, column=current_col, value=field_name)
            header_cell.font = header_font
            header_cell.fill = header_fill
            header_cell.alignment = center_align
            header_cell.border = cell_border
            
            # Row 3: Sample Values
            data_cell = ws.cell(row=3, column=current_col, value=sample_val)
            data_cell.font = data_font
            data_cell.alignment = center_align if isinstance(sample_val, (int, float)) else left_align
            data_cell.border = cell_border
            
            current_col += 1
            
    ws.row_dimensions[2].height = 25
    ws.row_dimensions[3].height = 22

    # Auto-fit column widths dynamically to prevent text truncation
    for col in ws.columns:
        max_len = max(len(str(cell.value or '')) for cell in col)
        col_letter = get_column_letter(col[0].column)
        ws.column_dimensions[col_letter].width = max(max_len + 5, 18)

    # ── TRANSMIT ATTACHMENT RESPONSE ──────────────────────────────────────
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="resale_residential_listing_template.xlsx"'
    wb.save(response)
    return response








# ── MASTER DATA CONFIGURATION MATRIX (DEFINED ONCE) ──────────────────
EXPORT_COLUMNS_BLUEPRINT = [
    # System Control Section
    {'field': 'property_id', 'section_name': 'SYSTEM CONTROL & IDENTIFICATION'},
    {'field': 'property_title', 'section_name': 'SYSTEM CONTROL & IDENTIFICATION'},
    
    # Step 1 Section
    {'field': 'property_type', 'section_name': 'STEP 1: BASIC INFO & CONFIGURATION'},
    {'field': 'zone', 'section_name': 'STEP 1: BASIC INFO & CONFIGURATION'},
    {'field': 'society_type', 'section_name': 'STEP 1: BASIC INFO & CONFIGURATION'},
    {'field': 'water_type', 'section_name': 'STEP 1: BASIC INFO & CONFIGURATION'},
    {'field': 'furnishing_type', 'section_name': 'STEP 1: BASIC INFO & CONFIGURATION'},
    {'field': 'age_of_property', 'section_name': 'STEP 1: BASIC INFO & CONFIGURATION'},
    {'field': 'facing_direction', 'section_name': 'STEP 1: BASIC INFO & CONFIGURATION'},
    {'field': 'bhk', 'section_name': 'STEP 1: BASIC INFO & CONFIGURATION'},
    {'field': 'bathrooms', 'section_name': 'STEP 1: BASIC INFO & CONFIGURATION'},
    {'field': 'balconies', 'section_name': 'STEP 1: BASIC INFO & CONFIGURATION'},
    {'field': 'covered_parking', 'section_name': 'STEP 1: BASIC INFO & CONFIGURATION'},
    {'field': 'open_parking', 'section_name': 'STEP 1: BASIC INFO & CONFIGURATION'},
    {'field': 'builtup_area', 'section_name': 'STEP 1: BASIC INFO & CONFIGURATION'},
    {'field': 'carpet_area', 'section_name': 'STEP 1: BASIC INFO & CONFIGURATION'},
    {'field': 'plot_area', 'section_name': 'STEP 1: BASIC INFO & CONFIGURATION'},
    {'field': 'floor_no', 'section_name': 'STEP 1: BASIC INFO & CONFIGURATION'},
    {'field': 'total_floors', 'section_name': 'STEP 1: BASIC INFO & CONFIGURATION'},
    
    # Step 2 Section
    {'field': 'ownership_type', 'section_name': 'STEP 2: LEGAL & PRICING DETAILS'},
    {'field': 'num_owners', 'section_name': 'STEP 2: LEGAL & PRICING DETAILS'},
    {'field': 'loan_on_property', 'section_name': 'STEP 2: LEGAL & PRICING DETAILS'},
    {'field': 'loan_amount', 'section_name': 'STEP 2: LEGAL & PRICING DETAILS'},
    {'field': 'existing_tenants', 'section_name': 'STEP 2: LEGAL & PRICING DETAILS'},
    {'field': 'tenant_details', 'section_name': 'STEP 2: LEGAL & PRICING DETAILS'},
    {'field': 'any_legal_dispute', 'section_name': 'STEP 2: LEGAL & PRICING DETAILS'},
    {'field': 'dispute_details', 'section_name': 'STEP 2: LEGAL & PRICING DETAILS'},
    {'field': 'government_tax_dues', 'section_name': 'STEP 2: LEGAL & PRICING DETAILS'},
    {'field': 'pending_tax_amount', 'section_name': 'STEP 2: LEGAL & PRICING DETAILS'},
    {'field': 'expected_price', 'section_name': 'STEP 2: LEGAL & PRICING DETAILS'},
    {'field': 'price_per_sqft', 'section_name': 'STEP 2: LEGAL & PRICING DETAILS'},
    {'field': 'price_negotiable', 'section_name': 'STEP 2: LEGAL & PRICING DETAILS'},
    {'field': 'brokerage', 'section_name': 'STEP 2: LEGAL & PRICING DETAILS'},
    {'field': 'brokerage_percentage', 'section_name': 'STEP 2: LEGAL & PRICING DETAILS'},
    {'field': 'manual_brokerage', 'section_name': 'STEP 2: LEGAL & PRICING DETAILS'},
    {'field': 'property_description', 'section_name': 'STEP 2: LEGAL & PRICING DETAILS'},
    
    # Step 3 Section
    {'field': 'nearby_facilities', 'section_name': 'STEP 3: AMENITIES & LOCATION'},
    {'field': 'amenities', 'section_name': 'STEP 3: AMENITIES & LOCATION'},
    {'field': 'city', 'section_name': 'STEP 3: AMENITIES & LOCATION'},
    {'field': 'locality', 'section_name': 'STEP 3: AMENITIES & LOCATION'},
    {'field': 'building_name', 'section_name': 'STEP 3: AMENITIES & LOCATION'},
    {'field': 'complete_address', 'section_name': 'STEP 3: AMENITIES & LOCATION'},
    {'field': 'owner_name', 'section_name': 'STEP 3: AMENITIES & LOCATION'},
    {'field': 'owner_contact', 'section_name': 'STEP 3: AMENITIES & LOCATION'},
    {'field': 'owner_email', 'section_name': 'STEP 3: AMENITIES & LOCATION'},
    {'field': 'owner_role', 'section_name': 'STEP 3: AMENITIES & LOCATION'},
    {'field': 'residential_status', 'section_name': 'STEP 3: AMENITIES & LOCATION'},

    # Step 4 Auditing Meta
    {'field': 'uploaded_by_name', 'section_name': 'STEP 4: PHOTOS & PUBLISH SYSTEM'},
    {'field': 'uploaded_by_email', 'section_name': 'STEP 4: PHOTOS & PUBLISH SYSTEM'},
    {'field': 'uploaded_by_contact', 'section_name': 'STEP 4: PHOTOS & PUBLISH SYSTEM'},
    {'field': 'uploaded_by_role', 'section_name': 'STEP 4: PHOTOS & PUBLISH SYSTEM'},
    {'field': 'upload_file_name', 'section_name': 'STEP 4: PHOTOS & PUBLISH SYSTEM'},
    {'field': 'created_at', 'section_name': 'STEP 4: PHOTOS & PUBLISH SYSTEM'},
    {'field': 'updated_at', 'section_name': 'STEP 4: PHOTOS & PUBLISH SYSTEM'},
    {'field': 'is_deleted', 'section_name': 'STEP 4: PHOTOS & PUBLISH SYSTEM'},
    {'field': 'deleted_at', 'section_name': 'STEP 4: PHOTOS & PUBLISH SYSTEM'},
    {'field': 'deleted_by', 'section_name': 'STEP 4: PHOTOS & PUBLISH SYSTEM'}
]


def export_resale_csv(request):
    """
    Exports all Resale Residential properties to CSV pulling directly from the master matrix sequence.
    """
    uploader = _get_uploader(request)
    if uploader is None:
        return redirect('login')

    response = HttpResponse(content_type='text/csv; charset=utf-8')
    response['Content-Disposition'] = 'attachment; filename="resale_residential_complete_database.csv"'

    writer = csv.writer(response)
    
    # Extract headers straight out of the master dictionary array
    headers = [item['field'] for item in EXPORT_COLUMNS_BLUEPRINT]
    writer.writerow(headers)

    queryset = ResaleResidentialProperty.objects.all()
    for prop in queryset:
        row = []
        for item in EXPORT_COLUMNS_BLUEPRINT:
            val = getattr(prop, item['field'], '')
            if val is None:
                val = ''
            elif isinstance(val, Decimal):
                val = float(val)
            elif hasattr(val, 'strftime'):
                val = val.strftime('%Y-%m-%d %H:%M:%S')
            row.append(val)
        writer.writerow(row)

    return response


def export_resale_excel(request):
    """
    Generates a stylized Excel sheet pulling from the master configuration blueprint array.
    """
    uploader = _get_uploader(request)
    if uploader is None:
        return redirect('login')

    wb = Workbook()
    ws = wb.active
    ws.title = "Resale Template"
    ws.views.sheetView[0].showGridLines = True

    # ── SYSTEM PALETTE CONFIGURATIONS ──
    sys_control_fill = PatternFill(start_color="1F2937", end_color="1F2937", fill_type="solid") # Dark Slate
    step1_fill = PatternFill(start_color="374151", end_color="374151", fill_type="solid")       # Dark Gray
    step2_fill = PatternFill(start_color="764BA2", end_color="764BA2", fill_type="solid")       # Deep Purple
    step3_fill = PatternFill(start_color="0F172A", end_color="0F172A", fill_type="solid")       # Slate Midnight
    meta_audit_fill = PatternFill(start_color="4B5563", end_color="4B5563", fill_type="solid")    # Mid Gray

    zebra_even_fill = PatternFill(start_color="F9FAFB", end_color="F9FAFB", fill_type="solid")
    white_fill = PatternFill(start_color="FFFFFF", end_color="FFFFFF", fill_type="solid")

    font_step_title = Font(name="Segoe UI", size=11, bold=True, color="FFFFFF")
    font_db_field = Font(name="Segoe UI", size=10, bold=True, color="FFFFFF")
    font_data_row = Font(name="Segoe UI", size=10, bold=False, color="111827")

    thin_border_side = Side(border_style="thin", color="E5E7EB")
    grid_border = Border(left=thin_border_side, right=thin_border_side, top=thin_border_side, bottom=thin_border_side)

    center_alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
    left_alignment = Alignment(horizontal="left", vertical="center")

    # ── RENDER HEADERS FROM THE SINGLE MASTER BLUEPRINT MATRIX ──
    for col_idx, column_meta in enumerate(EXPORT_COLUMNS_BLUEPRINT, start=1):
        # Render Row 1 Section Group Block
        cell_step = ws.cell(row=1, column=col_idx, value=column_meta['section_name'])
        cell_step.font = font_step_title
        cell_step.alignment = center_alignment
        cell_step.border = grid_border
        
        # Style sections dynamically based on identity mapping
        if "SYSTEM CONTROL" in column_meta['section_name']:
            cell_step.fill = sys_control_fill
        elif "STEP 1" in column_meta['section_name']:
            cell_step.fill = step1_fill
        elif "STEP 2" in column_meta['section_name']:
            cell_step.fill = step2_fill
        elif "STEP 3" in column_meta['section_name']:
            cell_step.fill = step3_fill
        else:
            cell_step.fill = meta_audit_fill

        # Render Row 2 Property Column Names
        cell_field = ws.cell(row=2, column=col_idx, value=column_meta['field'])
        cell_field.font = font_db_field
        cell_field.alignment = left_alignment
        cell_field.fill = meta_audit_fill
        cell_field.border = grid_border

    # ── INJECT RETRIEVED ROW DATA VALUES ──
    all_properties = ResaleResidentialProperty.objects.all()
    
    for row_idx, property_obj in enumerate(all_properties, start=3):
        for col_idx, column_meta in enumerate(EXPORT_COLUMNS_BLUEPRINT, start=1):
            cell_value = getattr(property_obj, column_meta['field'], '')
            if cell_value is None:
                cell_value = ''
                
            cell = ws.cell(row=row_idx, column=col_idx)
            
            # Formatting checks
            if isinstance(cell_value, (int, float, Decimal)):
                cell.value = float(cell_value)
                if any(kw in column_meta['field'] for kw in ['price', 'amount', 'due']):
                    cell.number_format = '₹#,##,##0.00'
                cell.alignment = Alignment(horizontal="right", vertical="center")
            elif hasattr(cell_value, 'strftime'):
                cell.value = cell_value.strftime('%Y-%m-%d %H:%M:%S')
                cell.alignment = left_alignment
            else:
                cell.value = str(cell_value)
                cell.alignment = left_alignment

            cell.font = font_data_row
            cell.border = grid_border
            cell.fill = zebra_even_fill if row_idx % 2 == 0 else white_fill

    ws.row_dimensions[1].height = 28
    ws.row_dimensions[2].height = 22

    # ── COLUMN AUTO-FIT LAYOUT CALCULATION ──
    for col in ws.columns:
        max_string_len = 0
        column_alpha_key = get_column_letter(col[0].column)
        for cell in col:
            if cell.row == 1:
                continue
            if cell.value is not None:
                max_string_len = max(max_string_len, len(str(cell.value)))
        ws.column_dimensions[column_alpha_key].width = max(max_string_len + 4, 16)

    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="resale_residential_Export.xlsx"'
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

    # ── Base Queryset ──────────────────────────────────────
    props = CommercialResaleProperty.objects.filter(is_deleted=False)

    # ── Advanced Real-Time Extraction Filters ──────────────
    search_query = request.GET.get('search_query', '').strip()
    property_type = request.GET.get('property_type', '').strip()
    zone_type = request.GET.get('zone_type', '').strip()
    city = request.GET.get('city', '').strip()
    property_condition = request.GET.get('property_condition', '').strip()
    ownership_type = request.GET.get('ownership_type', '').strip()
    status_filter = request.GET.get('status_filter', '').strip()
    
    start_date_str = request.GET.get('start_date', '').strip()
    end_date_str = request.GET.get('end_date', '').strip()

    # 1. Global text lookup matching primary data vectors
    if search_query:
        props = props.filter(
            Q(property_title__icontains=search_query) |
            Q(area_locality__icontains=search_query) |
            Q(building_name__icontains=search_query) |
            Q(owner_name__icontains=search_query)
        )

    # 2. Dropdown exact match filters
    if property_type:
        props = props.filter(property_type=property_type)
    if zone_type:
        props = props.filter(zone_type=zone_type)
    if city:
        props = props.filter(city__iexact=city)
    if property_condition:
        props = props.filter(property_condition=property_condition)
    if ownership_type:
        props = props.filter(ownership_type=ownership_type)
        
    # 3. Active/Inactive Status toggle matches
    if status_filter:
        if status_filter == 'active':
            props = props.filter(is_active=True)
        elif status_filter == 'inactive':
            props = props.filter(is_active=False)

    # 4. Strict Date-Range queries with automated datetime conversions
    if start_date_str:
        try:
            start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
            props = props.filter(created_at__gte=start_date)
        except ValueError:
            pass
            
    if end_date_str:
        try:
            # Append 23:59:59 to capture the entire final calendar day
            end_date = datetime.strptime(end_date_str + ' 23:59:59', '%Y-%m-%d %H:%M:%S')
            props = props.filter(created_at__lte=end_date)
        except ValueError:
            pass

    # ── ORDERING FIX ───────────────────────────────────────
    # Order results matching historical sequence trends
    # Changed from '-id' to '-created_at' due to the new UUID string format
    props = props.order_by('-created_at')

    # ── Dynamic Metric Aggregations (Reflects Filtered Querysets) ──
    # SECTION 1: Portfolio Quantities
    total_properties = props.count()
    active_properties = props.filter(is_active=True).count()
    inactive_properties = props.filter(is_active=False).count()

    # SECTION 2: Financial Aggregations & Capital Under Management
    avg_price = props.aggregate(Avg('expected_price'))['expected_price__avg'] or 0
    avg_price_per_sqft = props.aggregate(Avg('price_per_sqft'))['price_per_sqft__avg'] or 0
    
    raw_portfolio_sum = props.aggregate(Sum('expected_price'))['expected_price__sum'] or 0
    
    # Elegant short notation scale conversion formatting for large asset valuations (Crores / Lakhs)
    if raw_portfolio_sum >= 10000000:
        total_portfolio_value = f"{round(raw_portfolio_sum / 10000000, 2)} Cr"
    elif raw_portfolio_sum >= 100000:
        total_portfolio_value = f"{round(raw_portfolio_sum / 100000, 2)} L"
    else:
        total_portfolio_value = f"₹{raw_portfolio_sum:,}"

    # Brokerage Performance Metrics tracking
    brokered_deals_count = props.filter(brokerage__iexact='yes').count()
    brokerage_with_fees_count = props.filter(brokerage__iexact='yes').exclude(brokerage_percentage='').count()

    # SECTION 3: Property Mix Distribution
    office_count     = props.filter(property_type='office').count()
    shop_count       = props.filter(property_type='shop').count()
    warehouse_count  = props.filter(property_type='warehouse').count()
    industrial_count = props.filter(property_type='industrial').count()
    land_count       = props.filter(property_type='land').count()

    # Extract dynamic list arrays for autocomplete filter options lookups
    distinct_cities = CommercialResaleProperty.objects.filter(is_deleted=False).values_list('city', flat=True).distinct()
    
    # Uploaded Excel Files for Bulk Delete Dropdown
    # ── FIX APPLIED: Changed uploaded_file_name to upload_file_name ──
    uploaded_files = (
        CommercialResaleProperty.objects
        .filter(is_deleted=False)
        .exclude(upload_file_name__isnull=True)
        .exclude(upload_file_name='')
        .values_list('upload_file_name', flat=True)
        .distinct()
        .order_by('upload_file_name')
    )

    # ── Chart Data 1: Property Type Pie ────────────────────
    type_map = {
        'office': 'Office Space',
        'shop': 'Shop/Showroom',
        'warehouse': 'Warehouse',
        'industrial': 'Industrial',
        'land': 'Commercial Land',
    }
    type_qs = props.values('property_type').annotate(count=Count('id'))
    type_labels = [type_map.get(x['property_type'], x['property_type'].upper()) for x in type_qs]
    type_data = [x['count'] for x in type_qs]

    # ── Chart Data 2: Monthly Timeline (Current Year) ──────
    current_year = timezone.now().year
    monthly_data = [0] * 12
    monthly_qs = props.filter(created_at__year=current_year).values('created_at__month').annotate(count=Count('id'))
    for x in monthly_qs:
        monthly_data[x['created_at__month'] - 1] = x['count']

    # ── Chart Data 3: Zone Distribution ────────────────────
    zone_map = {
        'industrial': 'Industrial',
        'commercial': 'Commercial',
        'residential': 'Residential',
        'sez': 'SEZ',
    }
    zone_qs = props.values('zone_type').annotate(count=Count('id'))
    zone_labels = [zone_map.get(x['zone_type'], x['zone_type'].upper()) for x in zone_qs]
    zone_data = [x['count'] for x in zone_qs]

    context = {
        'admin_obj': admin_obj,
        'user_obj' : user_obj,
        'commercial_list': props,

        'uploaded_files': uploaded_files,
        # Metrics values (Reflecting custom grouped updates)
        'total_properties': total_properties,
        'active_properties': active_properties,
        'inactive_properties': inactive_properties,
        
        'avg_price': avg_price,
        'avg_price_per_sqft': avg_price_per_sqft,
        'total_portfolio_value': total_portfolio_value,
        'brokered_deals_count': brokered_deals_count,
        'brokerage_with_fees_count': brokerage_with_fees_count,
        
        'office_count'    : office_count,
        'shop_count'      : shop_count,
        'warehouse_count' : warehouse_count,
        'industrial_count': industrial_count,
        'land_count'      : land_count,
        'distinct_cities': distinct_cities,

        # Retained Filter Form States
        'search_query': search_query,
        'property_type': property_type,
        'zone_type': zone_type,
        'city_selected': city,
        'property_condition': property_condition,
        'ownership_type': ownership_type,
        'status_filter': status_filter,
        'start_date': start_date_str,
        'end_date': end_date_str,

        # Structured Analytics
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
    uploader = _get_uploader(request)
    if uploader is None:
        return redirect('login')

    if request.method == "POST":
        try:
            prop = CommercialResaleProperty(
                # ── Step 1: Basic Info & Specifications ────────────────
                property_type      = request.POST.get('property_type'),
                zone_type          = request.POST.get('zone_type'),
                location_hub       = request.POST.get('location_hub') or None,
                property_condition = request.POST.get('property_condition'),
                ownership_type     = request.POST.get('ownership_type'),
                age_of_property    = request.POST.get('age_of_property'),

                # Commercial Specifications
                num_staircases  = request.POST.get('num_staircases') or 0,
                passenger_lifts = request.POST.get('passenger_lifts') or 0,
                service_lifts   = request.POST.get('service_lifts') or 0,
                num_cabins      = request.POST.get('num_cabins') or 0,
                meeting_rooms   = request.POST.get('meeting_rooms') or 0,
                min_seats       = request.POST.get('min_seats') or None,
                max_seats       = request.POST.get('max_seats') or None,
                private_parking = request.POST.get('private_parking') or 0,
                public_parking  = request.POST.get('public_parking') or 0,

                # Area Measurements
                builtup_area = request.POST.get('builtup_area'),
                carpet_area  = request.POST.get('carpet_area') or None,
                plot_area    = request.POST.get('plot_area') or None,

                # ── Step 2: Legal & Pricing ─────────────────────────
                num_owners              = request.POST.get('num_owners'),
                loan_on_property        = request.POST.get('loan_on_property', 'no'),
                loan_amount             = request.POST.get('loan_amount') or None,
                existing_tenants        = request.POST.get('existing_tenants', 'no'),
                tenant_details          = request.POST.get('tenant_details') or None,
                any_legal_dispute       = request.POST.get('any_legal_dispute', 'no'),
                dispute_details         = request.POST.get('dispute_details') or None,
                government_tax_dues     = request.POST.get('government_tax_dues', 'no'),
                pending_tax_amount      = request.POST.get('pending_tax_amount') or None,
                fire_safety_noc_available = request.POST.get('fire_safety_noc_available') or None,

                # Pricing
                # NOTE: price_per_sqft is intentionally NOT taken from the form —
                # it is auto-calculated inside CommercialResaleProperty.save()
                # from expected_price / builtup_area. The frontend display value
                # (formatted string like "₹1,234 / sqft") must never be stored directly.
                brokerage             = request.POST.get('brokerage') or None,
                brokerage_percentage  = request.POST.get('brokerage_percentage') or None,
                manual_brokerage      = request.POST.get('manual_brokerage') or None,
                expected_price        = request.POST.get('expected_price'),
                property_description  = request.POST.get('property_description'),
                sanctioning_authority = request.POST.get('sanctioning_authority'),

                # ── Step 3: Amenities & Location ───────────────────
                nearby_facilities = ','.join(request.POST.getlist('nearby_facilities')),
                amenities         = ','.join(request.POST.getlist('amenities')),

                city             = request.POST.get('city'),
                area_locality    = request.POST.get('area_locality'),
                building_name    = request.POST.get('building_name') or None,
                property_address = request.POST.get('property_address'),

                owner_name         = request.POST.get('owner_name'),
                owner_contact      = request.POST.get('owner_contact'),
                owner_email        = request.POST.get('owner_email'),
                owner_role         = request.POST.get('owner_role') or None,  # ✅ ADDED — matches form name="owner_role"
                residential_status = request.POST.get('residential_status'),

                # ── Step 4: Media ───────────────────────────────────
                floor_plan     = request.FILES.get('floor_plan') or None,
                property_video = request.FILES.get('property_video') or None,

                # ── Uploader ────────────────────────────────────────
                uploaded_by_name    = uploader.get('uploader_name'),
                uploaded_by_email   = uploader.get('uploader_email'),
                uploaded_by_contact = uploader.get('uploader_phone'),
                uploaded_by_role    = uploader.get('uploader_role'),
            )

            prop.save()

            # Save up to 10 property images
            images = request.FILES.getlist('property_images')
            for image in images[:10]:
                CommercialPropertyImage.objects.create(property=prop, image=image)

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

    context = {
        "admin_obj"     : uploader.get('admin_obj'),
        "user_obj"      : uploader.get('user_obj'),
        "uploader_name" : uploader.get('uploader_name'),
        "uploader_email": uploader.get('uploader_email'),
        "uploader_phone": uploader.get('uploader_phone'),
        "uploader_role" : uploader.get('uploader_role'),
        "facilities_obj": Facilities_Details.objects.all() if 'Facilities_Details' in globals() else [],
        "ameneties_obj" : Ameneties_Details.objects.all() if 'Ameneties_Details' in globals() else [],
    }
    return render(request, 'admin_user/Reports/Resale/commercial_resale.html', context)



def commercial_resale_edit(request, id):
    uploader = _get_uploader(request)
    if uploader is None:
        return redirect('login')

    prop = get_object_or_404(CommercialResaleProperty, id=id)

    if request.method == "POST":
        def safe_float(val):
            try: return float(val) if val else 0.0
            except ValueError: return 0.0
            
        def safe_int(val):
            try: return int(float(val)) if val else 0
            except ValueError: return 0

        # ── Basic Information ──────────────────────────────
        prop.property_title = request.POST.get('property_title') or None  # Updates the title sequence fallback
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
        
        prop.any_legal_dispute = request.POST.get('any_legal_dispute', 'no') # Updated key
        prop.dispute_details = request.POST.get('dispute_details') if prop.any_legal_dispute == 'yes' else None
        
        prop.government_tax_dues = request.POST.get('government_tax_dues', 'no') # Updated key
        prop.pending_tax_amount = safe_float(request.POST.get('pending_tax_amount')) if prop.government_tax_dues == 'yes' else None
        
        prop.fire_safety_noc_available = request.POST.get('fire_safety_noc_available', 'no') # Updated key
        prop.property_description = request.POST.get('property_description')
        prop.sanctioning_authority = request.POST.get('sanctioning_authority')

        # ── Nearby Facilities & Amenities ──────────────────
        prop.nearby_facilities = ', '.join(request.POST.getlist('nearby_facilities'))
        prop.amenities = ', '.join(request.POST.getlist('amenities'))

        # ── Address ────────────────────────────────────────
        prop.city = request.POST.get('city')
        prop.area_locality = request.POST.get('area_locality') # Updated key
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

        # Handle Image Gallery (Delete marked records)
        deleted_images = request.POST.getlist('deleted_images[]')
        if deleted_images:
            CommercialPropertyImage.objects.filter(id__in=deleted_images, property=prop).delete()

        # Append additional attachments if space remains under current session bounds
        current_images_count = prop.images.count()
        new_files = request.FILES.getlist('property_images')
        available_slots = 10 - current_images_count
        
        for img in new_files[:available_slots]:
            CommercialPropertyImage.objects.create(property=prop, image=img)

        return JsonResponse({"status": "success", "message": "Commercial Property Updated Successfully"})

    # --- GET REQUEST Context ---
    ameneties_obj = Ameneties_Details.objects.all() if 'Ameneties_Details' in globals() else []
    facilities_obj = Facilities_Details.objects.all() if 'Facilities_Details' in globals() else []
    
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




from openpyxl.worksheet.datavalidation import DataValidation






def get_filtered_properties(request):
    """Internal helper to capture the identical data arrays currently viewed inside the frontend lists."""
    props = CommercialResaleProperty.objects.filter(is_deleted=False)
    
    search_query = request.GET.get('search_query', '').strip()
    property_type = request.GET.get('property_type', '').strip()
    zone_type = request.GET.get('zone_type', '').strip()
    city = request.GET.get('city', '').strip()
    property_condition = request.GET.get('property_condition', '').strip()
    ownership_type = request.GET.get('ownership_type', '').strip()
    status_filter = request.GET.get('status_filter', '').strip()
    start_date_str = request.GET.get('start_date', '').strip()
    end_date_str = request.GET.get('end_date', '').strip()

    if search_query:
        props = props.filter(
            Q(property_title__icontains=search_query) |
            Q(area_locality__icontains=search_query) |
            Q(building_name__icontains=search_query) |
            Q(owner_name__icontains=search_query)
        )
    if property_type:
        props = props.filter(property_type=property_type)
    if zone_type:
        props = props.filter(zone_type=zone_type)
    if city:
        props = props.filter(city__iexact=city)
    if property_condition:
        props = props.filter(property_condition=property_condition)
    if ownership_type:
        props = props.filter(ownership_type=ownership_type)
    if status_filter:
        if status_filter == 'active':
            props = props.filter(is_active=True)
        elif status_filter == 'inactive':
            props = props.filter(is_active=False)
            
    if start_date_str:
        try:
            props = props.filter(created_at__gte=datetime.strptime(start_date_str, '%Y-%m-%d'))
        except ValueError: pass
    if end_date_str:
        try:
            props = props.filter(created_at__lte=datetime.strptime(end_date_str + ' 23:59:59', '%Y-%m-%d %H:%M:%S'))
        except ValueError: pass

    return props.order_by('-id')





@transaction.atomic
def import_commercial_data(request):
    """
    Ingests sectioned double-header master sheets cleanly.
    Guarantees exact mapping indices to align database content profiles perfectly.
    """
    # ── IDENTIFY SESSION OWNER INGESTION AUDITS ─────────────────
    admin_id = request.session.get('Admin_id')
    user_id  = request.session.get('User_id')

    if not admin_id and not user_id:
        return JsonResponse({'status': '0', 'msg': 'Session Expired. Please log in again to perform uploads.'})

    uploader_name, uploader_email, uploader_contact, uploader_role = "System Bulk Import", "", "", "Staff"

    if admin_id:
        try:
            admin_obj = Admin_Login.objects.get(id=admin_id)
            uploader_name = getattr(admin_obj, 'name', 'Admin')
            uploader_email = getattr(admin_obj, 'email', '')
            uploader_contact = getattr(admin_obj, 'phone', '')
            uploader_role = getattr(admin_obj, 'role', 'Admin')
        except Admin_Login.DoesNotExist: pass
    elif user_id:
        try:
            user_obj = User_Details.objects.get(id=user_id)
            uploader_name = getattr(user_obj, 'name', 'User')
            uploader_email = getattr(user_obj, 'email', '')
            uploader_contact = getattr(user_obj, 'phone', '')
            uploader_role = "User"
        except User_Details.DoesNotExist: pass

    if request.method != 'POST' or not request.FILES.get('commercial_excel_file'):
        return JsonResponse({'status': '0', 'msg': 'Missing transactional multipart form document.'})
        
    excel_file = request.FILES['commercial_excel_file']
    filename = excel_file.name

    if not filename.endswith('.xlsx'):
        return JsonResponse({'status': '0', 'msg': 'Invalid file layout format. Please drop a valid .xlsx file.'})

    try:
        wb = openpyxl.load_workbook(excel_file, data_only=True)
        ws = wb.active
        
        # min_row=3 explicitly bypasses Row 1 (Visual Sections) and Row 2 (Column Headers)
        rows = list(ws.iter_rows(min_row=3, values_only=True))
        
        if not rows or all(all(cell is None for cell in row) for row in rows):
            return JsonResponse({'status': '0', 'msg': 'The processed workbook contains no usable data records.'})

        filename_exists = CommercialResaleProperty.objects.filter(upload_file_name=filename).exists()
        success_count = 0
        duplicate_count = 0

        def clean_str(val):
            return str(val).strip() if val is not None else ""

        def clean_num(val, is_float=False):
            if val is None or str(val).strip() == '':
                return 0.0 if is_float else 0
            try:
                cleaned_val = str(val).replace('₹', '').replace(',', '').strip()
                return float(cleaned_val) if is_float else int(float(cleaned_val))
            except (ValueError, TypeError):
                return 0.0 if is_float else 0

        # ── ITERATE CELLS POPULATED LAYERS ─────────────────────────
        for index, row in enumerate(rows, start=3):
            p_type_raw = clean_str(row[2]).lower()  # Property Type is locked at column index 2 (C)
            if not p_type_raw:  # Gracefully skip empty bottom trailing lines
                continue

            # --- CORRECTION SYNC FIELD MANDATORY VALIDATIONS MATRIX ---
            required_fields = {
                "Property Type": row[2],
                "Zone Type": row[3],
                "Property Condition": row[5],
                "Ownership Type": row[6],
                "Age of Property": row[7],
                "Private Parking": row[15],
                "Built-up Area (sq.ft)": row[17],
                "No. of Owners": row[20],
                "Loan on Property?": row[21],
                "Existing Tenants?": row[23],
                "Any Legal Dispute?": row[25],
                "Government Tax Dues?": row[27],
                "Expected Price (₹)": row[33],
                "Property Description": row[35],
                "Sanctioning Authority": row[36],
                "City": row[39],
                "Area/Locality": row[40],
                "Property Address": row[42],
                "Owner Name": row[43],
                "Owner Contact": row[44],
                "Owner Email": row[45],
                "Residential Status": row[47],
            }

            missing_fields = [field for field, val in required_fields.items() if val is None or str(val).strip() == '']
            if missing_fields:
                return JsonResponse({
                    'status': '0', 
                    'msg': f'Row {index} Stop: The following mandatory attributes are missing/blank: [{", ".join(missing_fields)}]'
                })

            city = clean_str(row[39])
            locality = clean_str(row[40])
            expected_price = clean_num(row[33], is_float=True)
            builtup_area_val = clean_num(row[17], is_float=True)

            # --- DYNAMIC AND UNIFORM AUTO PROPERTY TITLE GENERATOR ---
            type_clean_map = {
                'office': 'Office Space', 'shop': 'Shop / Showroom', 'warehouse': 'Warehouse',
                'industrial': 'Industrial Plant', 'land': 'Commercial Plot Land'
            }
            display_type = type_clean_map.get(p_type_raw, p_type_raw.title())
            generated_title = f"Premium {int(builtup_area_val)} Sqft {display_type}"
            building_val = clean_str(row[41])
            if building_val and building_val != "—" and building_val != "":
                generated_title += f" in {building_val}"
            generated_title += f" at {locality}, {city}"

            # --- STRUCTURAL ENFORCED DATA DUPLICATE security checks ---
            is_data_duplicate = CommercialResaleProperty.objects.filter(
                property_title=generated_title,
                property_type=p_type_raw,
                city=city,
                expected_price=expected_price,
                is_deleted=False
            ).exists()

            if is_data_duplicate:
                duplicate_count += 1
                if filename_exists:
                    return JsonResponse({
                        'status': '0',
                        'msg': f'Duplicate Halted: The upload package "{filename}" has already been processed and contains matching rows at index line {index}.'
                    })
                continue

            price_per_sqft_calc = round(expected_price / builtup_area_val, 2) if builtup_area_val > 0 else 0.0

            # --- EXECUTE STAGE RECORD COMMITMENT POOLS ---
            CommercialResaleProperty.objects.create(
                property_title=generated_title,
                
                # 📋 STEP 1: BASIC INFO & SPECIFICATIONS
                property_type=p_type_raw,
                zone_type=clean_str(row[3]).lower(),
                location_hub=clean_str(row[4]).lower() if row[4] else None,
                property_condition=clean_str(row[5]).lower(),
                ownership_type=clean_str(row[6]).lower(),
                age_of_property=clean_str(row[7]),
                
                num_staircases=clean_num(row[8]),
                passenger_lifts=clean_num(row[9]),
                service_lifts=clean_num(row[10]),
                num_cabins=clean_num(row[11]),
                meeting_rooms=clean_num(row[12]),
                min_seats=clean_num(row[13]) if row[13] is not None else None,
                max_seats=clean_num(row[14]) if row[14] is not None else None,
                private_parking=clean_num(row[15]),
                public_parking=clean_num(row[16]) if row[16] is not None else 0,
                
                builtup_area=builtup_area_val,
                carpet_area=clean_num(row[18], is_float=True) if row[18] else None,
                plot_area=clean_num(row[19], is_float=True) if row[19] else None,
                
                # 📋 STEP 2: LEGAL & PRICING DETAILS
                num_owners=clean_str(row[20]),
                loan_on_property=clean_str(row[21]).lower(),
                loan_amount=clean_num(row[22], is_float=True) if row[22] else None,
                existing_tenants=clean_str(row[23]).lower(),
                tenant_details=clean_str(row[24]) if row[24] else None,
                any_legal_dispute=clean_str(row[25]).lower(),
                dispute_details=clean_str(row[26]) if row[26] else None,
                government_tax_dues=clean_str(row[27]).lower(),
                pending_tax_amount=clean_num(row[28], is_float=True) if row[28] else None,
                fire_safety_noc_available=clean_str(row[29]).lower(),
                
                brokerage=clean_str(row[30]).lower(),
                brokerage_percentage=clean_str(row[31]) if row[31] else None,
                manual_brokerage=clean_str(row[32]) if row[32] else None,
                expected_price=expected_price,
                price_per_sqft=price_per_sqft_calc,
                property_description=clean_str(row[35]),
                sanctioning_authority=clean_str(row[36]),
                
                # 📋 STEP 3: AMENITIES & LOCATION
                nearby_facilities=clean_str(row[37]) if row[37] else None,
                amenities=clean_str(row[38]) if row[38] else None,
                city=city,
                area_locality=locality,
                building_name=building_val if building_val else None,
                property_address=clean_str(row[42]),
                
                # CONTACT SEQUENCE DETAILED TRACKING MAPS
                owner_name=clean_str(row[43]),
                owner_contact=clean_str(row[44]),
                owner_email=clean_str(row[45]),
                residential_status=clean_str(row[47]).lower(),
                
                # 📋 STEP 4: META TRACKING SYSTEMS AUDIT CONTROL LOGS
                uploaded_by_name=uploader_name,
                uploaded_by_email=uploader_email,
                uploaded_by_contact=uploader_contact,
                uploaded_by_role=uploader_role,
                upload_file_name=filename,
                is_active=True
            )
            success_count += 1

        if success_count > 0:
            msg = f'Import Process Completed! Successfully persisted {success_count} real-estate assets records.'
            if duplicate_count > 0:
                msg += f' ({duplicate_count} rows filtered out as safe database duplicates).'
            return JsonResponse({'status': '1', 'msg': msg})
        else:
            return JsonResponse({'status': '0', 'msg': 'All spreadsheet line profiles match current records. Zero mutations committed.'})

    except Exception as e:
        return JsonResponse({'status': '0', 'msg': f'Critical runtime exception encountered inside workbook sheets: {str(e)}'})




def download_commercial_sample_excel(request):
    """
    Generates a beautifully colored template matching the structural layout setup.
    Column index 0 is reserved for read-only title generation preview states.
    """
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Commercial Resale"
    ws.views.sheetView[0].showGridLines = True

    primary_purple = "667EEA"
    dark_section_slate = "475569"
    text_white = "FFFFFF"

    section_font = Font(name="Poppins", size=12, bold=True, color=text_white)
    header_font = Font(name="Poppins", size=10, bold=True, color=text_white)
    cell_alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)

    ws.row_dimensions[1].height = 32
    ws.row_dimensions[2].height = 54

    # --- ROW 1: RENDER COMPACT SECTION MASTER WRAPPERS BLOCK ---
    sections = [
        ("📋 Basic Info & Specs", 1, 15, dark_section_slate),
        ("📋 Area, Pricing & Building Details", 16, 37, primary_purple),
        ("📋 Amenities & Facilities", 38, 42, dark_section_slate),
        ("📋 Contact Info & System Logs", 43, 55, primary_purple)
    ]

    for title, start_col, end_col, color in sections:
        cell = ws.cell(row=1, column=start_col, value=title)
        cell.font = section_font
        cell.alignment = cell_alignment
        cell.fill = PatternFill(start_color=color, end_color=color, fill_type="solid")
        ws.merge_cells(start_row=1, start_column=start_col, end_row=1, end_column=end_col)
        for col in range(start_col + 1, end_col + 1):
            ws.cell(row=1, column=col).fill = PatternFill(start_color=color, end_color=color, fill_type="solid")

    # --- ROW 2: ENFORCE COMPLETE 55-COLUMN LABEL ARRANGEMENT ---
    headers = [
        "Property Id (Leave Blank - System Generated)", "Property Title (Leave Blank - System Generated)", 
        "Property Type (office/shop/warehouse/industrial/land) *", "Zone Type (industrial/commercial/residential/sez) *",
        "Location Hub", "Property Condition (new/excellent/good/renovation) *", "Ownership Type (freehold/leasehold/cooperative) *", 
        "Age Of The Property (0-1/1-3/3-5/5-10/10+) *", "No.Of.Staircases", "Passenger Lifts", "Service Lifts", 
        "No.Of.Cabins", "Meeting Rooms", "Min Seats", "Max Seats", "Private Parking *", "Public Parking", "Builtup Area *", 
        "Carpet Area", "Plot Area", "No.of Owners *",   
        "Loan on Property (yes/no) *", "Loan Amount", "Existing Tenants (yes/no) *", "Tenant Details", "Any Legal Dispute (yes/no) *", 
        "Dispute Details", "Government Tax Dues? (yes/no) *", "Pending Tax Amount", "Fire Safety NOC Available? (yes/no) *","Brokerage (yes/no)", "Brokerage Percentage","Manual_Brokarage","Expected Price *","Price Per Sqft/Auto Generated", "Property Description *", 
        "Sanctioning Authority *", "Nearby Facilities (comma separated)", "Amenities (comma separated)", "City *", 
        "Area/Locality *", "Building / Project / Society", "Property Address *", "Owner Name *", "Owner Contact *", "Owner Email *","Owner Role",
        "Residential Status (resident/nri/pio) *", "Uploaded By Name", "Uploaded By Email", "Uploaded By Contact", "Uploaded By Role", "Source File Name", "Created At", "Updated At"
    ]

    for col_index, header in enumerate(headers, start=1):
        cell = ws.cell(row=2, column=col_index, value=header)
        cell.font = header_font
        cell.alignment = cell_alignment
        bg_color = "5A67D8" if col_index in range(16, 38) or col_index in range(43, 56) else "334155"
        cell.fill = PatternFill(start_color=bg_color, end_color=bg_color, fill_type="solid")
        ws.column_dimensions[openpyxl.utils.get_column_letter(col_index)].width = 24

    # --- ROW 3: RE-ALIGNED SAMPLE PROTO PLATFORM INVENTORIES (55 ELEMENTS) ---
    sample_data = [
        "", "", "office", "commercial", "it", "excellent", "freehold", "1-3",
        2, 4, 1, 5, 2, 50, 100, 5, 10, 5000, 4500, 0, "1",
        "no", 0, "no", "", "no", "", "no", 0, "yes",
        "yes", "2%", "", 15000000, "", 
        "Fully furnished premium office space with modern workstation infrastructure.",
        "NMC", "Metro Station, Bus Stop, Mall, Hospital", 
        "CCTV Security, 100% Power Backup, Cafeteria, Central Gym", 
        "Nagpur", "Sitabuldi", "Tech Tower", "Floor 4, Tech Tower, Main Wardha Road, Sitabuldi",
        "Rajesh Kumar", "9876543210", "rajesh@example.com", "Owner", "resident",
        "System Template", "—", "—", "—", "—", "—", "—"
    ]
    ws.append(sample_data)

    def create_dropdown(options, cell_range):
        dv = DataValidation(type="list", formula1=f'"{",".join(options)}"', allow_blank=True)
        ws.add_data_validation(dv)
        dv.add(cell_range)

    # Re-indexedDropdown targets seamlessly link with explicit column indices
    create_dropdown(["office", "shop", "warehouse", "industrial", "land"], "C3:C100")
    create_dropdown(["industrial", "commercial", "residential", "sez"], "D3:D100")
    create_dropdown(["it", "business", "mall", "standalone"], "E3:E100")
    create_dropdown(["new", "excellent", "good", "renovation"], "F3:F100")
    create_dropdown(["freehold", "leasehold", "cooperative"], "G3:G100")
    create_dropdown(["0-1", "1-3", "3-5", "5-10", "10+"], "H3:H100")
    create_dropdown(["1", "2", "3", "4+"], "U3:U100")
    create_dropdown(["resident", "nri", "pio"], "AV3:AV100")
    
    for col_letter in ["V", "X", "Z", "AB", "AD", "AE"]:
        create_dropdown(["yes", "no"], f"{col_letter}3:{col_letter}100")

    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="Commercial_Resale_Sample_Master.xlsx"'
    wb.save(response)
    return response



def export_commercial_resale_excel(request):
    """
    Generates the master live database inventory extract.
    Maintains exact 55-column alignments to protect cell arrays from index shifts.
    """
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Live Database Extract"
    ws.views.sheetView[0].showGridLines = True

    primary_purple = "667EEA"
    dark_section_slate = "475569"
    text_white = "FFFFFF"

    section_font = Font(name="Poppins", size=12, bold=True, color=text_white)
    header_font = Font(name="Poppins", size=10, bold=True, color=text_white)
    cell_alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)

    ws.row_dimensions[1].height = 32
    ws.row_dimensions[2].height = 54

    sections = [
        ("📋 Basic Info & Specs", 1, 15, dark_section_slate),
        ("📋 Area, Pricing & Building Details", 16, 37, primary_purple),
        ("📋 Amenities & Facilities", 38, 42, dark_section_slate),
        ("📋 Contact Info & System Logs", 43, 55, primary_purple)
    ]

    for title, start_col, end_col, color in sections:
        cell = ws.cell(row=1, column=start_col, value=title)
        cell.font = section_font
        cell.alignment = cell_alignment
        cell.fill = PatternFill(start_color=color, end_color=color, fill_type="solid")
        ws.merge_cells(start_row=1, start_column=start_col, end_row=1, end_column=end_col)
        for col in range(start_col + 1, end_col + 1):
            ws.cell(row=1, column=col).fill = PatternFill(start_color=color, end_color=color, fill_type="solid")

    headers = [
        "Property Id","Property Title", "Property Type (office/shop/warehouse/industrial/land) *", "Zone Type (industrial/commercial/residential/sez) *",
        "Location Hub", "Property Condition (new/excellent/good/renovation) *", "Ownership Type (freehold/leasehold/cooperative) *", 
        "Age Of The Property (0-1/1-3/3-5/5-10/10+) *", "No.Of.Staircases", "Passenger Lifts", "Service Lifts", 
        "No.Of.Cabins", "Meeting Rooms", "Min Seats", "Max Seats", "Private Parking *", "Public Parking", "Builtup Area *", 
        "Carpet Area", "Plot Area", "No.of Owners *",   
        "Loan on Property (yes/no) *", "Loan Amount", "Existing Tenants (yes/no) *", "Tenant Details", "Any Legal Dispute (yes/no) *", 
        "Dispute Details", "Government Tax Dues? (yes/no) *", "Pending Tax Amount", "Fire Safety NOC Available? (yes/no) *","Brokerage (yes/no)", "Brokerage Percentage","Manual_Brokarage","Expected Price *","Price Per Sqft/Auto Generated", "Property Description *", 
        "Sanctioning Authority *", "Nearby Facilities (comma separated)", "Amenities (comma separated)", "City *", 
        "Area/Locality *", "Building / Project / Society", "Property Address *", "Owner Name *", "Owner Contact *", "Owner Email *","Owner Role",
        "Residential Status (resident/nri/pio) *", "Uploaded By Name", "Uploaded By Email", "Uploaded By Contact", "Uploaded By Role", "Source File Name", "Created At", "Updated At"
    ]

    for col_index, header in enumerate(headers, start=1):
        cell = ws.cell(row=2, column=col_index, value=header)
        cell.font = header_font
        cell.alignment = cell_alignment
        bg_color = "5A67D8" if col_index in range(16, 38) or col_index in range(43, 56) else "334155"
        cell.fill = PatternFill(start_color=bg_color, end_color=bg_color, fill_type="solid")
        ws.column_dimensions[openpyxl.utils.get_column_letter(col_index)].width = 24

    properties = get_filtered_properties(request)

    for prop in properties:
        data_row = [
           
            prop.id or "—",
            prop.property_title or "—",
            prop.property_type,
            prop.zone_type,
            prop.location_hub or "—",
            prop.property_condition,
            prop.ownership_type,
            prop.age_of_property,
            prop.num_staircases or 0,
            prop.passenger_lifts or 0,
            prop.service_lifts or 0,
            prop.num_cabins or 0,
            prop.meeting_rooms or 0,
            prop.min_seats or "—",
            prop.max_seats or "—",
            prop.private_parking or 0,
            prop.public_parking or 0,
            float(prop.builtup_area),
            float(prop.carpet_area) if prop.carpet_area else "—",
            float(prop.plot_area) if prop.plot_area else "—",
            prop.num_owners or "1",
            prop.loan_on_property,
            float(prop.loan_amount) if prop.loan_amount else 0,
            prop.existing_tenants,
            prop.tenant_details or "",
            prop.any_legal_dispute,
            prop.dispute_details or "",
            prop.government_tax_dues,
            float(prop.pending_tax_amount) if prop.pending_tax_amount else 0,
            prop.fire_safety_noc_available or "no",
            prop.brokerage or "no",
            prop.brokerage_percentage or "",
            prop.manual_brokerage or "",
            float(prop.expected_price),
            float(prop.price_per_sqft) if prop.price_per_sqft else 0,
            prop.property_description,
            prop.sanctioning_authority,
            prop.nearby_facilities or "",
            prop.amenities or "",
            prop.city,
            prop.area_locality,
            prop.building_name or "",
            prop.property_address,
            prop.owner_name,
            prop.owner_contact,
            prop.owner_email,
            prop.uploaded_by_role or "Owner",
            prop.residential_status,
            prop.uploaded_by_name or "Portal Direct",
            prop.uploaded_by_email or "—",
            prop.uploaded_by_contact or "—",
            prop.uploaded_by_role or "—",
            prop.upload_file_name or "Web Input Form",
            prop.created_at.strftime("%Y-%m-%d %H:%M") if prop.created_at else "—",
            prop.updated_at.strftime("%Y-%m-%d %H:%M") if prop.updated_at else "—"
        ]
        ws.append(data_row)

    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = f'attachment; filename="Commercial_Resale_Export_{datetime.now().strftime("%Y%m%d")}.xlsx"'
    wb.save(response)
    return response






def export_commercial_resale_csv(request):
    """
    Flat CSV layout exporter matching the same sequential blueprint matrix.
    Includes Property Title as index 0 to eliminate data parsing drift.
    """
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="Commercial_Resale_Export_{datetime.now().strftime("%Y%m%d")}.csv"'
    
    writer = csv.writer(response)
    
    # ── EXACT 54-COLUMN SEQUENCE MAPPING FROM INDEX 0 TO 53 ──
    writer.writerow([
        "Property Id","Property Title","Property Type (office/shop/warehouse/industrial/land) *", 
        "Zone Type (industrial/commercial/residential/sez) *", "Location Hub", 
        "Property Condition (new/excellent/good/renovation) *", "Ownership Type (freehold/leasehold/cooperative) *", 
        "Age Of The Property (0-1/1-3/3-5/5-10/10+) *", "No.Of.Staircases", "Passenger Lifts", 
        "Service Lifts", "No.Of.Cabins", "Meeting Rooms", "Min Seats", "Max Seats", 
        "Private Parking *", "Public Parking", "Builtup Area *", "Carpet Area", "Plot Area", "No.of Owners *",   
        "Loan on Property (yes/no) *", "Loan Amount", "Existing Tenants (yes/no) *", "Tenant Details", 
        "Any Legal Dispute (yes/no) *", "Dispute Details", "Government Tax Dues? (yes/no) *", "Pending Tax Amount", 
        "Fire Safety NOC Available? (yes/no) *", "Brokerage (yes/no)", "Brokerage Percentage", "Manual_Brokarage", 
        "Expected Price *", "Price Per Sqft/Auto Generated", "Property Description *", "Sanctioning Authority *", 
        "Nearby Facilities (comma separated)", "Amenities (comma separated)", "City *", "Area/Locality *", 
        "Building / Project / Society", "Property Address *", "Owner Name *", "Owner Contact *", "Owner Email *", 
        "Owner Role", "Residential Status (resident/nri/pio) *", "Uploaded By Name", "Uploaded By Email", 
        "Uploaded By Contact", "Uploaded By Role", "Source File Name", "Created At", "Updated At"
    ])
    
    # Pull identical data entries matching active dashboard panel query parameters
    properties = get_filtered_properties(request)
    
    for prop in properties:
        # Dynamic calculation check fallback if field database values are unpopulated
        calculated_price_per_sqft = prop.price_per_sqft
        if not calculated_price_per_sqft and prop.builtup_area > 0:
            calculated_price_per_sqft = round(float(prop.expected_price) / float(prop.builtup_area), 2)

        writer.writerow([

            prop.commercial_id or "—", 
            prop.property_title or "—",                         # [0] Property Title
                                  # [1] Property Id
            prop.property_type,                                  # [2] Property Type
            prop.zone_type,                                      # [3] Zone Type
            prop.location_hub or "—",                            # [4] Location Hub
            prop.property_condition,                             # [5] Property Condition
            prop.ownership_type,                                 # [6] Ownership Type
            prop.age_of_property,                                # [7] Age Of The Property
            prop.num_staircases or 0,                            # [8] No.Of.Staircases
            prop.passenger_lifts or 0,                           # [9] Passenger Lifts
            prop.service_lifts or 0,                             # [10] Service Lifts
            prop.num_cabins or 0,                                # [11] No.Of.Cabins
            prop.meeting_rooms or 0,                             # [12] Meeting Rooms
            prop.min_seats or "—",                               # [13] Min Seats
            prop.max_seats or "—",                               # [14] Max Seats
            prop.private_parking or 0,                           # [15] Private Parking
            prop.public_parking or 0,                            # [16] Public Parking
            float(prop.builtup_area),                            # [17] Builtup Area
            float(prop.carpet_area) if prop.carpet_area else "—", # [18] Carpet Area
            float(prop.plot_area) if prop.plot_area else "—",     # [19] Plot Area
            prop.num_owners or "1",                              # [20] No.of Owners
            prop.loan_on_property,                               # [21] Loan on Property (yes/no)
            float(prop.loan_amount) if prop.loan_amount else 0,  # [22] Loan Amount
            prop.existing_tenants,                               # [23] Existing Tenants (yes/no)
            prop.tenant_details or "",                           # [24] Tenant Details
            prop.any_legal_dispute,                              # [25] Any Legal Dispute (yes/no)
            prop.dispute_details or "",                          # [26] Dispute Details
            prop.government_tax_dues,                            # [27] Government Tax Dues? (yes/no)
            float(prop.pending_tax_amount) if prop.pending_tax_amount else 0, # [28] Pending Tax Amount
            prop.fire_safety_noc_available or "no",              # [29] Fire Safety NOC Available? (yes/no)
            prop.brokerage or "no",                              # [30] Brokerage (yes/no)
            prop.brokerage_percentage or "",                     # [31] Brokerage Percentage
            prop.manual_brokerage or "",                         # [32] Manual_Brokarage
            float(prop.expected_price),                          # [33] Expected Price
            float(calculated_price_per_sqft) if calculated_price_per_sqft else 0, # [34] Price Per Sqft
            prop.property_description,                           # [35] Property Description
            prop.sanctioning_authority,                          # [36] Sanctioning Authority
            prop.nearby_facilities or "",                        # [37] Nearby Facilities
            prop.amenities or "",                                # [38] Amenities
            prop.city,                                           # [39] City
            prop.area_locality,                                  # [40] Area/Locality
            prop.building_name or "",                            # [41] Building / Project / Society
            prop.property_address,                               # [42] Property Address
            prop.owner_name,                                     # [43] Owner Name
            prop.owner_contact,                                  # [44] Owner Contact
            prop.owner_email,                                    # [45] Owner Email
            prop.uploaded_by_role or "Owner",                    # [46] Owner Role
            prop.residential_status,                             # [47] Residential Status
            prop.uploaded_by_name or "Portal Direct",            # [48] Uploaded By Name
            prop.uploaded_by_email or "—",                       # [49] Uploaded By Email
            prop.uploaded_by_contact or "—",                     # [50] Uploaded By Contact
            prop.uploaded_by_role or "—",                        # [51] Uploaded By Role
            prop.upload_file_name or "Web Form Direct",          # [52] Source File Name
            prop.created_at.strftime("%Y-%m-%d %H:%M") if prop.created_at else "—", # [53] Created At
            prop.updated_at.strftime("%Y-%m-%d %H:%M") if prop.updated_at else "—"  # [54] Updated At
        ])
        
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




# Ensure _get_deleter_name and CommercialResaleProperty are imported

@require_POST
def commercial_resale_bulk_delete(request):
    """Handles Advanced Bulk Deletions for Commercial Resale Properties."""
    
    admin_id = request.session.get('Admin_id')
    user_id = request.session.get('User_id')

    if not admin_id and not user_id:
        return JsonResponse({
            'status': 'error',
            'message': 'Unauthorized access.'
        })

    try:
        data = json.loads(request.body)
        delete_type = data.get('delete_type')
        deleter_name = _get_deleter_name(request)

        properties = CommercialResaleProperty.objects.filter(
            is_deleted=False
        )

        # Delete All
        if delete_type == 'delete_all':
            count = properties.count()

            properties.update(
                is_deleted=True,
                deleted_at=timezone.now(),
                deleted_by=deleter_name
            )

            return JsonResponse({
                'status': 'success',
                'message': f'Successfully moved ALL {count} properties to Recycle Bin.'
            })

        # Current Page
        elif delete_type == 'current_page':
            page_ids = data.get('page_ids', [])

            target_props = properties.filter(id__in=page_ids)
            count = target_props.count()

            target_props.update(
                is_deleted=True,
                deleted_at=timezone.now(),
                deleted_by=deleter_name
            )

            return JsonResponse({
                'status': 'success',
                'message': f'Successfully moved {count} properties from current page to Recycle Bin.'
            })

        # Date Range
        elif delete_type == 'date_range':
            from_date = data.get('from_date')
            to_date = data.get('to_date')

            target_props = properties.filter(
                created_at__date__range=[from_date, to_date]
            )

            count = target_props.count()

            target_props.update(
                is_deleted=True,
                deleted_at=timezone.now(),
                deleted_by=deleter_name
            )

            return JsonResponse({
                'status': 'success',
                'message': f'Successfully moved {count} properties in date range to Recycle Bin.'
            })

        # Latest Month
        elif delete_type == 'latest_month':
            thirty_days_ago = timezone.now() - timedelta(days=30)

            target_props = properties.filter(
                created_at__gte=thirty_days_ago
            )

            count = target_props.count()

            target_props.update(
                is_deleted=True,
                deleted_at=timezone.now(),
                deleted_by=deleter_name
            )

            return JsonResponse({
                'status': 'success',
                'message': f'Successfully moved {count} properties from the last 30 days to Recycle Bin.'
            })

        # Old Data
        elif delete_type == 'old_data':
            six_months_ago = timezone.now() - timedelta(days=180)

            target_props = properties.filter(
                created_at__lt=six_months_ago
            )

            count = target_props.count()

            target_props.update(
                is_deleted=True,
                deleted_at=timezone.now(),
                deleted_by=deleter_name
            )

            return JsonResponse({
                'status': 'success',
                'message': f'Successfully moved {count} older properties to Recycle Bin.'
            })

        # By Uploader
        elif delete_type == 'by_uploader':
            uploader = data.get('uploader_text', '').strip()

            target_props = properties.filter(
                Q(uploaded_by_name__icontains=uploader) |
                Q(uploaded_by_email__icontains=uploader) |
                Q(uploaded_by_role__icontains=uploader)
            )

            count = target_props.count()

            target_props.update(
                is_deleted=True,
                deleted_at=timezone.now(),
                deleted_by=deleter_name
            )

            return JsonResponse({
                'status': 'success',
                'message': f'Successfully moved {count} properties uploaded by "{uploader}" to Recycle Bin.'
            })

        # By File Name
        elif delete_type == 'by_file':
            file_name = data.get('file_name', '').strip()

            if not file_name:
                return JsonResponse({
                    'status': 'error',
                    'message': 'Please select a file name.'
                })

            # ── FIX APPLIED HERE: Changed uploaded_file_name to upload_file_name ──
            target_props = properties.filter(
                upload_file_name__iexact=file_name 
            )

            count = target_props.count()

            if count == 0:
                # ── FIX APPLIED HERE ALSO ──
                available_files = list(
                    CommercialResaleProperty.objects.filter(
                        is_deleted=False
                    )
                    .exclude(upload_file_name__isnull=True)
                    .exclude(upload_file_name='')
                    .values_list('upload_file_name', flat=True)
                    .distinct()
                )

                return JsonResponse({
                    'status': 'error',
                    'message': f'No properties found for file: {file_name}',
                    'available_files': available_files
                })

            target_props.update(
                is_deleted=True,
                deleted_at=timezone.now(),
                deleted_by=deleter_name
            )

            return JsonResponse({
                'status': 'success',
                'message': f'Successfully moved {count} properties imported from "{file_name}" to Recycle Bin.'
            })

    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        })


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
    prop = get_object_or_404(CommercialResaleProperty, id=id)
    images = prop.images.all()
    
    # Split strings for nice badge rendering in HTML
    facilities_list = [f.strip() for f in prop.nearby_facilities.split(',')] if prop.nearby_facilities else []
    amenities_list = [a.strip() for a in prop.amenities.split(',')] if prop.amenities else []

    context = {
        'admin_obj': admin_obj,
        'user_obj': user_obj,
        'prop': prop,
        'images': images,
        'facilities_list': facilities_list,
        'amenities_list': amenities_list
    }
    return render(request, 'admin_user/Reports/Resale/commercial_resale_view.html', context)







####################End Views Section For Commercial Resale Property #######################################



####################START Views Section For AGRICULTURAL Resale Property #######################################





def add_agricultural_property(request):
    """
    Handles the 4-step agricultural property listing form submission.
    Field mapping follows the exact sequential form model schema context.
    """
    admin_id = request.session.get('Admin_id')
    user_id = request.session.get('User_id')

    if not admin_id and not user_id:
        return redirect('login')

    try:
        # Resolve administrative audit details safely out of current active session structures
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

        if request.method == 'POST':
            def get_decimal(val):
                """Returns cleaned decimal value or None if blank."""
                return val if val and str(val).strip() != "" else None

            with transaction.atomic():
                # Correctly assign the frontend auto-generated read-only property title
                property_obj = AgriculturalResaleProperty.objects.create(
                    title=request.POST.get('property_title'),

                    # ── STEP 1: LAND DETAILS ─────────────────────────────────
                    # DB sequence match
                    agriculture_property_type=request.POST.get('agriculture_property_type', ''),
                    village=request.POST.get('village', ''),
                    taluka=request.POST.get('taluka', ''),
                    district=request.POST.get('district', ''),
                    land_area=get_decimal(request.POST.get('land_area')),
                    soil_type=request.POST.get('soil_type') or None,
                    irrigation_facility=request.POST.get('irrigation_facility', 'no'),
                    water_source=request.POST.get('water_source') or None,
                    previous_crops=request.POST.get('previous_crops') or None,
                    fertility_status=request.POST.get('fertility_status') or None,

                    # ── STEP 2: PRICING & LEGAL ──────────────────────────────
                    # DB sequence match
                    expected_price=get_decimal(request.POST.get('expected_price')),
                    brokerage=request.POST.get('brokerage') or None,
                    brokerage_percentage=request.POST.get('brokerage_percentage') or None,
                    manual_brokerage=request.POST.get('manual_brokerage') or None,
                    ownership_type=request.POST.get('ownership_type', ''),
                    
                    agri_loan=request.POST.get('agri_loan', 'no'),
                    loan_amount=get_decimal(request.POST.get('loan_amount')) if request.POST.get('agri_loan') == 'yes' else None,
                    
                    agri_tenants=request.POST.get('agri_tenants', 'no'),
                    tenant_details=request.POST.get('tenant_details') if request.POST.get('agri_tenants') == 'yes' else None,
                    
                    agri_dispute=request.POST.get('agri_dispute', 'no'),
                    dispute_details=request.POST.get('dispute_details') if request.POST.get('agri_dispute') == 'yes' else None,
                    
                    agri_tax_due=request.POST.get('agri_tax_due', 'no'),
                    pending_tax_amount=get_decimal(request.POST.get('pending_tax_amount')) if request.POST.get('agri_tax_due') == 'yes' else None,
                    
                    resale_agricultural_desc=request.POST.get('resale_agricultural_desc', ''),

                    # ── STEP 3: LOCATION & OWNER ─────────────────────────────
                    # DB sequence match
                    city=request.POST.get('city', ''),
                    state=request.POST.get('state', ''),
                    locality=request.POST.get('locality', ''),
                    address=request.POST.get('address', ''),
                    
                    owner_name=request.POST.get('owner_name', ''),
                    owner_contact=request.POST.get('owner_contact', ''),
                    owner_email=request.POST.get('owner_email', ''),
                    comm_residency=request.POST.get('comm_residency', 'resident'),

                    # ── STEP 4: UPLOADER AUDIT FIELDS ────────────────────────
                    uploaded_by_name=uploader_name,
                    uploaded_by_email=uploader_email,
                    uploaded_by_contact=uploader_phone,
                    uploaded_by_role=uploader_role,
                )

                # ── FILE FIELDS HANDLING ─────────────────────────────────
                if 'encumbrance_cert' in request.FILES:
                    property_obj.encumbrance_cert = request.FILES['encumbrance_cert']

                if 'property_video' in request.FILES:
                    property_obj.property_video = request.FILES['property_video']

                property_obj.save()

                # ── USER-ORDERED IMAGES INJECTION ────────────────────────
                # Receives files array in the exact visual sort order dictated by frontend Sortable list arrays
                images = request.FILES.getlist('property_images[]')
                for img in images[:10]:
                    AgriculturalResaleImage.objects.create(
                        property=property_obj,
                        image=img
                    )

            return JsonResponse({
                'status': 'success',
                'message': f'Agricultural Property "{property_obj.title}" published successfully to directories!'
            })

    except Exception as e:
        print("ERROR:", str(e))
        traceback.print_exc()
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=400)

    # Context binding fallbacks for rendering standard baseline structural get requests layouts
    context = {'admin_obj': admin if admin_id else user}
    return render(request, 'admin_user/Reports/Resale/agricultural_list.html', context)









def edit_agricultural_property(request, pk):
    property_obj = get_object_or_404(AgriculturalResaleProperty, pk=pk)

    if request.method == 'POST':
        try:
            def get_decimal(value):
                if value is None or str(value).strip() == "":
                    return None
                return float(value)

            def clean_yes_no(val):
                return str(val).strip().lower() if val else 'no'

            with transaction.atomic():
                # ── STEP 1: LAND DETAILS ──────────────────────────────────
                property_obj.agriculture_property_type = request.POST.get('agriculture_property_type')
                property_obj.village = request.POST.get('village')
                property_obj.taluka = request.POST.get('taluka')
                property_obj.district = request.POST.get('district')
                property_obj.land_area = get_decimal(request.POST.get('land_area') or request.POST.get('area'))
                property_obj.soil_type = request.POST.get('soil_type')
                property_obj.irrigation_facility = clean_yes_no(request.POST.get('irrigation_facility'))
                property_obj.water_source = request.POST.get('water_source')
                property_obj.previous_crops = request.POST.get('previous_crops')
                property_obj.fertility_status = request.POST.get('fertility_status')

                # ── STEP 2: PRICING & LEGAL ───────────────────────────────
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
                
                property_obj.resale_agricultural_desc = request.POST.get('resale_agricultural_desc')

                # ── STEP 3: LOCATION & OWNER ─────────────────────────────
                property_obj.city = request.POST.get('city')
                property_obj.state = request.POST.get('state')
                property_obj.locality = request.POST.get('locality')
                property_obj.address = request.POST.get('address') or request.POST.get('property_address')
                
                property_obj.owner_name = request.POST.get('owner_name')
                property_obj.owner_contact = request.POST.get('owner_contact')
                property_obj.owner_email = request.POST.get('owner_email')
                property_obj.comm_residency = request.POST.get('comm_residency', 'resident')

                # ── STEP 4: DOCUMENTS & PHOTOS ────────────────────────────
                if 'encumbrance_cert' in request.FILES:
                    property_obj.encumbrance_cert = request.FILES['encumbrance_cert']

                if 'property_video' in request.FILES:
                    property_obj.property_video = request.FILES['property_video']

                # Force automated title re-generation logic on update
                property_obj.title = None 
                property_obj.save()

                # Multiple Portfolio Image Upload Handling Loops
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
                'message': 'Agricultural listing alterations updated successfully!',
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




# =========================================================================
# 1. DOWNLOAD TEMPLATE
# =========================================================================
def download_agri_sample_excel(request):
    from openpyxl import Workbook
    from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
    from openpyxl.utils import get_column_letter

    wb = Workbook()
    sheet = wb.active
    sheet.title = "Agricultural Resale"

    DARK_BG, WHITE, MID_BLUE = "1E293B", "FFFFFF", "3B82F6"
    LIGHT_BG, HINT_BG, SAMPLE_BG = "F8FAFC", "FEF9C3", "EFF6FF"
    HINT_FG, BORDER_COLOR = "92400E", "CBD5E1"
    thin  = Side(style="thin",   color=BORDER_COLOR)
    thick = Side(style="medium", color="94A3B8")
    cb = Border(left=thin, right=thin, top=thin, bottom=thin)
    hb = Border(left=thick, right=thick, top=thick, bottom=thick)
    def hfill(h): return PatternFill("solid", fgColor=h)

    sections = [
        ("📋 Land Details", [
            ("agriculture_property_type *", "Property Type *",        "agriculture_land / farm_land / orchard_land"),
            ("village *",                  "Village *",               "e.g. Warud"),
            ("taluka *",                   "Taluka *",                "e.g. Warud"),
            ("district *",                 "District *",              "e.g. Amravati"),
            ("land_area *",                "Land Area (Acres) *",     "e.g. 5.5"),
            ("soil_type",                  "Soil Type",               "black / red / alluvial / sandy / loamy"),
            ("irrigation_facility",        "Irrigation Facility",     "yes / no"),
            ("water_source",               "Water Source",            "well / borewell / canal / river / none"),
            ("previous_crops",             "Previous Crops",          "e.g. Wheat, Cotton"),
            ("fertility_status",           "Fertility Status",        "high / medium / low"),
        ]),
        ("📋 Pricing", [
            ("expected_price *",    "Expected Price (₹) *", "e.g. 5000000"),
            ("brokerage",           "Brokerage",            "Yes / No"),
            ("brokerage_percentage","Brokerage %",          "e.g. 2% or leave blank"),
            ("manual_brokerage",    "Manual Brokerage",     "e.g. 50000 or leave blank"),
        ]),
        ("📋 Ownership & Legal", [
            ("ownership_type *",         "Ownership Type *",      "freehold / leasehold"),
            ("agri_loan *",              "Loan Available *",      "yes / no"),
            ("loan_amount",              "Loan Amount (₹)",       "e.g. 200000 (0 if no loan)"),
            ("agri_tenants *",           "Tenants? *",            "yes / no"),
            ("tenant_details",           "Tenant Details",        "Enter if tenants=yes else leave blank"),
            ("agri_dispute *",           "Dispute? *",            "yes / no"),
            ("dispute_details",          "Dispute Details",       "Enter if dispute=yes else leave blank"),
            ("agri_tax_due *",           "Tax Due? *",            "yes / no"),
            ("pending_tax_amount",       "Pending Tax (₹)",       "0 if no tax due"),
            ("resale_agricultural_desc *","Description *",        "Short summary of the land"),
        ]),
        ("📋 Address", [
            ("city *",     "City *",     "e.g. Nagpur"),
            ("state *",    "State *",    "e.g. Maharashtra"),
            ("locality *", "Locality *", "e.g. Besa Rural"),
            ("address *",  "Address *",  "Near highway bridge, Ward No 4"),
        ]),
        ("📋 Owner Contact", [
            ("owner_name *",    "Owner Name *",    "Full Name"),
            ("owner_contact *", "Owner Contact *", "10-digit mobile"),
            ("owner_email *",   "Owner Email *",   "email@example.com"),
            ("comm_residency *","Comm/Residency *","resident / non_resident / commercial"),
        ]),
    ]

    all_db, all_disp, all_hints, section_spans = [], [], [], []
    col = 1
    for label, fields in sections:
        s = col
        for db, disp, hint in fields:
            all_db.append(db); all_disp.append(disp); all_hints.append(hint); col += 1
        section_spans.append((label, s, col-1))

    # Row 1 – Section headers
    for label, sc, ec in section_spans:
        c = sheet.cell(row=1, column=sc, value=label)
        c.font=Font(name="Arial",bold=True,size=11,color=WHITE); c.fill=hfill(DARK_BG)
        c.alignment=Alignment(horizontal="center",vertical="center"); c.border=hb
        if sc != ec: sheet.merge_cells(start_row=1,start_column=sc,end_row=1,end_column=ec)
    sheet.row_dimensions[1].height = 30

    # Row 2 – DB fields
    for i,db in enumerate(all_db,1):
        c=sheet.cell(row=2,column=i,value=db)
        c.font=Font(name="Arial",bold=True,size=9,color="475569"); c.fill=hfill("E2E8F0")
        c.alignment=Alignment(horizontal="center",vertical="center"); c.border=cb
    sheet.row_dimensions[2].height = 22

    # Row 3 – Display headers
    for i,disp in enumerate(all_disp,1):
        c=sheet.cell(row=3,column=i,value=disp)
        c.font=Font(name="Arial",bold=True,size=10,color=("C0392B" if disp.endswith("*") else MID_BLUE))
        c.fill=hfill(LIGHT_BG); c.alignment=Alignment(horizontal="center",vertical="center",wrap_text=True); c.border=cb
    sheet.row_dimensions[3].height = 36

    # Row 4 – Hints
    for i,hint in enumerate(all_hints,1):
        c=sheet.cell(row=4,column=i,value=hint)
        c.font=Font(name="Arial",italic=True,size=8,color=HINT_FG); c.fill=hfill(HINT_BG)
        c.alignment=Alignment(horizontal="center",vertical="center",wrap_text=True); c.border=cb
    sheet.row_dimensions[4].height = 30

    # Row 5 – Sample
    sample = [
        "agriculture_land","Warud","Warud","Amravati",5.5,"black","yes","well","Wheat","high",
        5000000,"Yes","2%","","freehold","yes",200000,"no","","no","","no",0,
        "Excellent land for farming close to arterial link pathways.",
        "Nagpur","Maharashtra","Besa Rural","Near highway bridge, Ward No 4",
        "Ramesh Patil","9876543210","ramesh@example.com","resident",
    ]
    for i,val in enumerate(sample,1):
        c=sheet.cell(row=5,column=i,value=val)
        c.font=Font(name="Arial",size=9,color="1E3A5F"); c.fill=hfill(SAMPLE_BG)
        c.alignment=Alignment(horizontal="center",vertical="center"); c.border=cb
    sheet.row_dimensions[5].height = 22

    widths=[22,14,14,14,14,14,14,14,18,12,16,12,14,16,16,12,16,12,20,12,20,12,16,28,14,16,16,28,18,18,24,18]
    for i,w in enumerate(widths,1): sheet.column_dimensions[get_column_letter(i)].width=w
    sheet.freeze_panes="A6"; sheet.sheet_view.zoomScale=90

    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="PropCRM_Agricultural_Template.xlsx"'
    wb.save(response)
    return response






def safe_float(val):
    """Safely converts Excel cell values to float, handling strings, currencies, and spaces."""
    if val is None:
        return 0.0
    try:
        if isinstance(val, (int, float)):
            return float(val)
        clean_val = str(val).replace('₹', '').replace(',', '').strip()
        return float(clean_val)
    except (ValueError, TypeError):
        return 0.0

def import_agricultural_resale_excel(request):
    session_id = request.session.get('Admin_id')
    if not session_id:
        return JsonResponse({"status": "error", "message": "Unauthorized access"})

    if request.method == "POST" and request.FILES.get('excel_file'):
        try:
            admin_obj = Admin_Login.objects.get(id=session_id)
            excel_file = request.FILES['excel_file']
            file_name_str = excel_file.name

            # Load the uploaded file safely from memory stream boundary
            excel_file.seek(0)
            wb = openpyxl.load_workbook(excel_file, data_only=True)
            sheet = wb.active

            if sheet.max_row < 3:
                return JsonResponse({"status": "error", "message": "Empty file uploaded."})

            # 1. Validate Row 3 Display Headers match what was downloaded
            row3 = [str(cell.value).strip() if cell.value else "" for cell in sheet[3]]
            expected = [
                "Property Type *","Village *","Taluka *","District *","Land Area (Acres) *",
                "Soil Type","Irrigation Facility","Water Source","Previous Crops","Fertility Status",
                "Expected Price (₹) *","Brokerage","Brokerage %","Manual Brokerage",
                "Ownership Type *","Loan Available *","Loan Amount (₹)","Tenants? *","Tenant Details",
                "Dispute? *","Dispute Details","Tax Due? *","Pending Tax (₹)","Description *",
                "City *","State *","Locality *","Address *",
                "Owner Name *","Owner Contact *","Owner Email *","Comm/Residency *",
            ]
            
            for idx, key in enumerate(expected):
                if idx >= len(row3) or row3[idx].lower() != key.lower():
                    return JsonResponse({
                        "status": "error",
                        "message": f"Column mismatch at {idx+1}. Expected '{key}', found '{row3[idx] if idx<len(row3) else 'Missing'}'."
                    })

            # Formatting helper wrappers
            def cs(v): return str(v).strip() if v is not None else ""
            def yn(v): return cs(v).lower() if v else "no"

            records = []
            # Index structural mapping of required spreadsheet inputs
            required_idx = [0, 1, 2, 3, 4, 10, 14, 15, 17, 19, 21, 23, 24, 25, 26, 27, 28, 29, 30, 31]

            # Start reading from Row 5 (The sample record data row generated by your system)
            DATA_START_ROW = 5 

            for row_idx, row in enumerate(sheet.iter_rows(min_row=DATA_START_ROW, values_only=True), start=DATA_START_ROW):
                # A. Skip entirely empty rows or whitespace padding rows
                if not row or not any(v is not None and str(v).strip() != "" for v in row): 
                    continue
                
                # B. Skip Row 4 hint text if it somehow gets included, or rows with clear instruction patterns
                if row[0] and ("agriculture_land /" in str(row[0]).lower() or str(row[0]).strip().lower().startswith("e.g.")):
                    continue

                # Fallback check for structural stability
                if len(row) < len(expected):
                    return JsonResponse({"status": "error", "message": f"Row {row_idx} does not have enough columns to process."})

                # C. Check mandatory field validations
                for ri in required_idx:
                    if row[ri] is None or str(row[ri]).strip() == "":
                        return JsonResponse({"status": "error", "message": f"Row {row_idx}: Required field '{expected[ri]}' is missing."})
                
                # D. Generate an isolated row unique fingerprint to check for duplicates
                row_raw_string = f"{row[28]}_{row[29]}_{row[1]}_{row[4]}_{row[10]}"  # Owner Name + Contact + Village + Area + Price
                row_fp = hashlib.md5(row_raw_string.encode()).hexdigest()

                # E. Individual item duplication check
                if AgriculturalResaleProperty.objects.filter(resale_agricultural_desc__icontains=f"[ROW-MD5:{row_fp}]", is_deleted=False).exists():
                    continue  # Skip safely if this exact row is already processed and saved in the database

                records.append({
                    "agriculture_property_type": cs(row[0]),
                    "village": cs(row[1]), "taluka": cs(row[2]), "district": cs(row[3]),
                    "land_area": safe_float(row[4]),
                    "soil_type": cs(row[5]), "irrigation_facility": yn(row[6]),
                    "water_source": cs(row[7]), "previous_crops": cs(row[8]),
                    "fertility_status": cs(row[9]),
                    "expected_price": safe_float(row[10]),
                    "brokerage": cs(row[11]) if row[11] else "No",
                    "brokerage_percentage": cs(row[12]), "manual_brokerage": cs(row[13]),
                    "ownership_type": cs(row[14]), "agri_loan": yn(row[15]),
                    "loan_amount": safe_float(row[16]) if yn(row[15]) == "yes" else 0.0,
                    "agri_tenants": yn(row[17]),
                    "tenant_details": cs(row[18]) if yn(row[17]) == "yes" else "",
                    "agri_dispute": yn(row[19]),
                    "dispute_details": cs(row[20]) if yn(row[19]) == "yes" else "",
                    "agri_tax_due": yn(row[21]),
                    "pending_tax_amount": safe_float(row[22]) if yn(row[21]) == "yes" else 0.0,
                    "resale_agricultural_desc": cs(row[23]),
                    "city": cs(row[24]), "state": cs(row[25]),
                    "locality": cs(row[26]), "address": cs(row[27]),
                    "owner_name": cs(row[28]), "owner_contact": cs(row[29]),
                    "owner_email": cs(row[30]), "comm_residency": cs(row[31]),
                    "row_fingerprint": row_fp
                })

            if not records:
                return JsonResponse({
                    "status": "error", 
                    "message": "No new or valid asset records found to import. Rows are either empty or already exist in the system."
                })

            # 2. Database Creation Loop
            imported_count = 0
            for r in records:
                AgriculturalResaleProperty.objects.create(
                    agriculture_property_type=r["agriculture_property_type"],
                    village=r["village"], taluka=r["taluka"], district=r["district"],
                    land_area=r["land_area"], soil_type=r["soil_type"],
                    irrigation_facility=r["irrigation_facility"], water_source=r["water_source"],
                    previous_crops=r["previous_crops"], fertility_status=r["fertility_status"],
                    expected_price=r["expected_price"], brokerage=r["brokerage"],
                    brokerage_percentage=r["brokerage_percentage"], manual_brokerage=r["manual_brokerage"],
                    ownership_type=r["ownership_type"], agri_loan=r["agri_loan"],
                    loan_amount=r["loan_amount"], agri_tenants=r["agri_tenants"],
                    tenant_details=r["tenant_details"], agri_dispute=r["agri_dispute"],
                    dispute_details=r["dispute_details"], agri_tax_due=r["agri_tax_due"],
                    pending_tax_amount=r["pending_tax_amount"],
                    resale_agricultural_desc=f"{r['resale_agricultural_desc']} [FILE:{file_name_str}] [ROW-MD5:{r['row_fingerprint']}]",
                    city=r["city"], state=r["state"], locality=r["locality"], address=r["address"],
                    owner_name=r["owner_name"], owner_contact=r["owner_contact"],
                    owner_email=r["owner_email"], comm_residency=r["comm_residency"],
                    uploaded_by_name=admin_obj.name, uploaded_by_email=admin_obj.email,
                    uploaded_by_contact=admin_obj.phone, uploaded_by_role=admin_obj.role,
                    upload_file_name=file_name_str
                )
                imported_count += 1

            return JsonResponse({"status": "success", "message": f"Successfully imported {imported_count} records from {file_name_str}."})

        except Exception as e:
            traceback.print_exc()
            return JsonResponse({"status": "error", "message": f"System Error: {str(e)}"})

    return JsonResponse({"status": "error", "message": "Invalid request parameters."})

# 3. LIST VIEW
# =========================================================================
import re


def agricultural_resale_list(request):
    session_id = request.session.get('Admin_id')
    if not session_id:
        return render(request, 'home_page/Adminlogin.html')

    try:
        admin_obj = Admin_Login.objects.get(id=session_id)
    except Admin_Login.DoesNotExist:
        return render(request, 'home_page/Adminlogin.html')

    # Base Active Dataset
    base_qs = AgriculturalResaleProperty.objects.filter(is_deleted=False)
    
    # ── FIXED SEARCH FILTER LOGIC ──────────────────────────────────────
    search_query = request.GET.get('search', '').strip()
    properties = base_qs

    if search_query:
        # Normalize spaces to underscores if a user types "farm land" instead of "farm_land"
        normalized_query = search_query.replace(' ', '_')
        
        properties = properties.filter(
            Q(village__icontains=search_query) | 
            Q(district__icontains=search_query) |
            Q(taluka__icontains=search_query) |
            Q(city__icontains=search_query) | 
            Q(state__icontains=search_query) |
            Q(owner_name__icontains=search_query) | 
            Q(owner_contact__icontains=search_query) |
            Q(agriculture_property_type__icontains=search_query) |
            Q(agriculture_property_type__icontains=normalized_query)
        )

    # Apply sorting safely AFTER filtering
    properties = properties.order_by('-created_at')

    # Pagination setup
    paginator = Paginator(properties, 25)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    total_value = base_qs.aggregate(Sum('expected_price'))['expected_price__sum'] or 0

    # Extract historical uploaded filenames from property description footprint strings
    uploaded_files = set()
    for desc in base_qs.exclude(resale_agricultural_desc__isnull=True).values_list('resale_agricultural_desc', flat=True):
        m = re.search(r'\[FILE:(.+?)\]', desc or '')
        if m: 
            uploaded_files.add(m.group(1))

    context = {
        'admin_obj': admin_obj,
        'page_obj': page_obj,
        'search_query': search_query,
        'uploaded_files': sorted(uploaded_files),
        'stats': {
            'total': base_qs.count(),
            'agri_land': base_qs.filter(agriculture_property_type='agriculture_land').count(),
            'farm_land': base_qs.filter(agriculture_property_type='farm_land').count(),
            'orchard': base_qs.filter(agriculture_property_type='orchard_land').count(),
            'total_value': total_value,
        }
    }
    return render(request, 'admin_user/Reports/Resale/agricultural_list.html', context)





# Helper layout structural definition matching the standard format sequence
EXPORT_SECTIONS = [
    ("📋 Land Details", [
        ("agriculture_property_type", "Property Type *", "agriculture_land / farm_land / orchard_land"),
        ("village", "Village *", "e.g. Warud"),
        ("taluka", "Taluka *", "e.g. Warud"),
        ("district", "District *", "e.g. Amravati"),
        ("land_area", "Land Area (Acres) *", "e.g. 5.5"),
        ("soil_type", "Soil Type", "black / red / alluvial / sandy / loamy"),
        ("irrigation_facility", "Irrigation Facility", "yes / no"),
        ("water_source", "Water Source", "well / borewell / canal / river / none"),
        ("previous_crops", "Previous Crops", "e.g. Wheat, Cotton"),
        ("fertility_status", "Fertility Status", "high / medium / low"),
    ]),
    ("📋 Pricing", [
        ("expected_price", "Expected Price (₹) *", "e.g. 5000000"),
        ("brokerage", "Brokerage", "Yes / No"),
        ("brokerage_percentage", "Brokerage %", "e.g. 2% or leave blank"),
        ("manual_brokerage", "Manual Brokerage", "e.g. 50000 or leave blank"),
    ]),
    ("📋 Ownership & Legal", [
        ("ownership_type", "Ownership Type *", "freehold / leasehold"),
        ("agri_loan", "Loan Available *", "yes / no"),
        ("loan_amount", "Loan Amount (₹)", "e.g. 200000 (0 if no loan)"),
        ("agri_tenants", "Tenants? *", "yes / no"),
        ("tenant_details", "Tenant Details", "Enter if tenants=yes else leave blank"),
        ("agri_dispute", "Dispute? *", "yes / no"),
        ("dispute_details", "Dispute Details", "Enter if dispute=yes else leave blank"),
        ("agri_tax_due", "Tax Due? *", "yes / no"),
        ("pending_tax_amount", "Pending Tax (₹)", "0 if no tax due"),
        ("resale_agricultural_desc", "Description *", "Short summary of the land"),
    ]),
    ("📋 Address", [
        ("city", "City *", "e.g. Nagpur"),
        ("state", "State *", "e.g. Maharashtra"),
        ("locality", "Locality *", "e.g. Besa Rural"),
        ("address", "Address *", "Near highway bridge, Ward No 4"),
    ]),
    ("📋 Owner Contact", [
        ("owner_name", "Owner Name *", "Full Name"),
        ("owner_contact", "Owner Contact *", "10-digit mobile"),
        ("owner_email", "Owner Email *", "email@example.com"),
        ("comm_residency", "Comm/Residency *", "resident / non_resident / commercial"),
    ]),
]

def export_agricultural_resale_excel(request):
    """Generates an Excel data dump built inside the exact import layout format schema."""
    # Apply identical search parameters from list filter to the export view
    search_query = request.GET.get('search', '').strip()
    queryset = AgriculturalResaleProperty.objects.filter(is_deleted=False)
    if search_query:
        normalized = search_query.replace(' ', '_')
        queryset = queryset.filter(
            Q(village__icontains=search_query) | Q(district__icontains=search_query) |
            Q(taluka__icontains=search_query) | Q(city__icontains=search_query) |
            Q(owner_name__icontains=search_query) | Q(agriculture_property_type__icontains=search_query) |
            Q(agriculture_property_type__icontains=normalized)
        )
    queryset = queryset.order_by('-created_at')

    wb = openpyxl.Workbook()
    sheet = wb.active
    sheet.title = "Agricultural Export Data"

    # Styling Assets
    DARK_BG, WHITE, MID_BLUE = "1E293B", "FFFFFF", "3B82F6"
    LIGHT_BG, HINT_BG = "F8FAFC", "FEF9C3"
    thin = Side(style="thin", color="CBD5E1")
    thick = Side(style="medium", color="94A3B8")
    cb = Border(left=thin, right=thin, top=thin, bottom=thin)
    hb = Border(left=thick, right=thick, top=thick, bottom=thick)
    def hfill(h): return PatternFill("solid", fgColor=h)

    all_db, all_disp, all_hints, section_spans = [], [], [], []
    col = 1
    for label, fields in EXPORT_SECTIONS:
        s = col
        for db, disp, hint in fields:
            all_db.append(db); all_disp.append(disp); all_hints.append(hint); col += 1
        section_spans.append((label, s, col-1))

    # Row 1 – Section banners
    for label, sc, ec in section_spans:
        c = sheet.cell(row=1, column=sc, value=label)
        c.font = Font(name="Arial", bold=True, size=11, color=WHITE)
        c.fill = hfill(DARK_BG)
        c.alignment = Alignment(horizontal="center", vertical="center")
        c.border = hb
        if sc != ec: 
            sheet.merge_cells(start_row=1, start_column=sc, end_row=1, end_column=ec)
    sheet.row_dimensions[1].height = 30

    # Row 2 – System keys
    for i, db in enumerate(all_db, 1):
        c = sheet.cell(row=2, column=i, value=f"{db} *") if i in [1,2,3,4,5,11,15,16,18,20,22,24,25,26,27,28,29,30,31] else sheet.cell(row=2, column=i, value=db)
        c.font = Font(name="Arial", bold=True, size=9, color="475569")
        c.fill = hfill("E2E8F0")
        c.alignment = Alignment(horizontal="center", vertical="center")
        c.border = cb
    sheet.row_dimensions[2].height = 22

    # Row 3 – Display Titles
    for i, disp in enumerate(all_disp, 1):
        c = sheet.cell(row=3, column=i, value=disp)
        c.font = Font(name="Arial", bold=True, size=10, color=("C0392B" if disp.endswith("*") else MID_BLUE))
        c.fill = hfill(LIGHT_BG)
        c.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
        c.border = cb
    sheet.row_dimensions[3].height = 36

    # Row 4 – Instruction Hints
    for i, hint in enumerate(all_hints, 1):
        c = sheet.cell(row=4, column=i, value=hint)
        c.font = Font(name="Arial", italic=True, size=8, color="92400E")
        c.fill = hfill(HINT_BG)
        c.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
        c.border = cb
    sheet.row_dimensions[4].height = 30

    # Row 5 onwards – Database Records Injection
    current_row = 5
    for item in queryset:
        for idx, db_field in enumerate(all_db, 1):
            val = getattr(item, db_field, "")
            
            # Clean dynamic descriptions so raw tags aren't visible
            if db_field == "resale_agricultural_desc" and val:
                val = re.sub(r'\[FILE:.+?\]|\[ROW-MD5:.+?\]', '', str(val)).strip()

            c = sheet.cell(row=current_row, column=idx, value=val)
            c.font = Font(name="Arial", size=10)
            c.border = cb
            c.alignment = Alignment(horizontal="left", vertical="center")
        sheet.row_dimensions[current_row].height = 20
        current_row += 1

    widths = [22,14,14,14,14,14,14,14,18,12,16,12,14,16,16,12,16,12,20,12,20,12,16,28,14,16,16,28,18,18,24,18]
    for i, w in enumerate(widths, 1): 
        sheet.column_dimensions[get_column_letter(i)].width = w
    sheet.freeze_panes = "A5"

    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="Agricultural_Properties_Export.xlsx"'
    wb.save(response)
    return response

def export_agricultural_resale_csv(request):
    """Generates a plain-text CSV export preserving identical structural row indexing maps."""
    search_query = request.GET.get('search', '').strip()
    queryset = AgriculturalResaleProperty.objects.filter(is_deleted=False)
    if search_query:
        normalized = search_query.replace(' ', '_')
        queryset = queryset.filter(
            Q(village__icontains=search_query) | Q(district__icontains=search_query) |
            Q(taluka__icontains=search_query) | Q(city__icontains=search_query) |
            Q(owner_name__icontains=search_query) | Q(agriculture_property_type__icontains=search_query) |
            Q(agriculture_property_type__icontains=normalized)
        )
    queryset = queryset.order_by('-created_at')

    response = HttpResponse(content_type='text/csv; charset=utf-8')
    response['Content-Disposition'] = 'attachment; filename="Agricultural_Properties_Export.csv"'
    
    writer = csv.writer(response)

    all_db, all_disp, all_hints = [], [], []
    for label, fields in EXPORT_SECTIONS:
        for db, disp, hint in fields:
            all_db.append(db); all_disp.append(disp); all_hints.append(hint)

    # Re-build matching row headers matrix
    # Note: Row 1 section names can't easily be merged in flat CSV files, so we pass blank pads
    section_row = []
    for label, fields in EXPORT_SECTIONS:
        section_row.append(label)
        section_row.extend([""] * (len(fields) - 1))
        
    writer.writerow(section_row) # Row 1
    
    # Process Row 2 updated required asterisks mapping keys
    db_row_final = []
    for i, db in enumerate(all_db, 1):
        if i in [1,2,3,4,5,11,15,16,18,20,22,24,25,26,27,28,29,30,31]:
            db_row_final.append(f"{db} *")
        else:
            db_row_final.append(db)
    writer.writerow(db_row_final) # Row 2
    
    writer.writerow(all_disp)     # Row 3
    writer.writerow(all_hints)    # Row 4

    # Inject data loops
    for item in queryset:
        row_data = []
        for db_field in all_db:
            val = getattr(item, db_field, "")
            if db_field == "resale_agricultural_desc" and val:
                val = re.sub(r'\[FILE:.+?\]|\[ROW-MD5:.+?\]', '', str(val)).strip()
            row_data.append(val)
        writer.writerow(row_data)

    return response

def view_agricultural_property(request, pk):
    session_id = request.session.get('Admin_id')
    user_id    = request.session.get('User_id')

    if not session_id and not user_id:
        return redirect('admin_login_url_name')

    property_obj = get_object_or_404(
        AgriculturalResaleProperty.objects.prefetch_related('images', 'faqs'),
        pk=pk
    )

    # Safety: regenerate FAQs if missing (old records before migration)
    if not property_obj.faqs.exists():
        property_obj.generate_auto_faqs()

    context = {
        'property': property_obj,
        'faqs': property_obj.faqs.all(),
    }
    return render(request, 'admin_user/Resale/view_agricultural_resale.html', context)


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