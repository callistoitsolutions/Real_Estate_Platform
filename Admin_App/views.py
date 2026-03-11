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
        print("-------------------------------")
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


############  Views start for rental property list ########################

def residential_list(request):
    session_id = request.session.get('Admin_id')
    if session_id:
        admin_obj = Admin_Login.objects.get(id=session_id)
        context = {'admin_obj':admin_obj}
        return render(request,'admin_user/Reports/Rental/rental_list.html',context)
    else:
        return render(request,'home_page/Adminlogin.html')

############ Views end for rental property list ###########################


########### Views start for commercial property list ###################

def commercial_list(request):
    session_id = request.session.get('Admin_id')
    if session_id:
        admin_obj = Admin_Login.objects.get(id=session_id)
        context = {'admin_obj':admin_obj}
        return render(request,'admin_user/Reports/Rental/commercial_list.html',context)
    else:
        return render(request,'home_page/Adminlogin.html')

############### Views end for commercial property list ########################


######### Views start for pg co living rental list ########################

def pg_list(request):
    session_id = request.session.get('Admin_id')
    if session_id:
        admin_obj = Admin_Login.objects.get(id=session_id)
        context = {'admin_obj':admin_obj}
        return render(request,'admin_user/Reports/Rental/pg_list.html',context)
    else:
        return render(request,'home_page/Adminlogin.html')

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
        context = {'admin_obj':admin_obj}
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


########## Views start for display vendors list ##################

def Vendor_List(request):
    session_id = request.session.get('Admin_id')
    if session_id:
        admin_obj = Admin_Login.objects.get(id=session_id)
        context = {'admin_obj':admin_obj}
        return render(request,'admin_user/Vendor/vendor_list.html',context)
    else:
        return render(request,'home_page/Adminlogin.html')

######### Views end for display vendors list ######################


########### Views start for add vendor #####################

def Add_Vendor(request):
    session_id = request.session.get('Admin_id')
    if session_id:
        admin_obj = Admin_Login.objects.get(id=session_id)
        context = {'admin_obj':admin_obj}
        return render(request,'admin_user/Vendor/add_vendor.html',context)
    else:
        return render(request,'home_page/Adminlogin.html')

############### Views end for add vendor #######################



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

