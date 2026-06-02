from django.shortcuts import render,HttpResponse

# Create your views here.
from django.shortcuts import render, get_object_or_404,redirect

# Create your views here.
from django.shortcuts import render



# Create your views here.
from django.shortcuts import render
from django.contrib import messages
from django.shortcuts import render,redirect
from CRM_Panel .models import *
from Admin_App.models import *
from django.template.loader import render_to_string
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import traceback
from django.db.models import Case, When, Value, IntegerField
from datetime import datetime

# Create your views here.

########### Crime Officer Views#######




def crm_dashboard(request):
    session_id = request.session.get('Admin_id')
    if session_id:
        admin_obj = Admin_Login.objects.get(id=session_id)
        context = {'admin_obj':admin_obj}
        return render(request,"crm/crm_dashboard.html",context) 
    else:
        return render(request,'home_page/Adminlogin.html')
    


############## Views start for display utm links ###########################

def utm_links_crm(request):
    session_id = request.session.get('Admin_id')
    if session_id:
        admin_obj = Admin_Login.objects.get(id=session_id)

        utm_obj = UTMLink.objects.all().order_by('-id')
        utm_obj_count = UTMLink.objects.all().count()

        rendered = render_to_string("crm/render_to_string/R_Utm/r_t_s_utm.html",{'utm_obj':utm_obj,'utm_obj_count':utm_obj_count})


        context = {'admin_obj':admin_obj,'utm_lists':rendered}
        
        return render(request,"crm/UTM/utm_links.html",context) 
    else:
        return render(request,'home_page/Adminlogin.html')

############# Views end for display utm links #############################


########### Views start for create utm link ##########################

def create_utm_crm(request):
    session_id = request.session.get('Admin_id')
    if session_id:
        admin_obj = Admin_Login.objects.get(id=session_id)

        properties = []

        for model in [RentalResidentialProperty, CommercialRentalProperty, PGColivingProperty,ResaleResidentialProperty,CommercialResaleProperty,PlotSaleProperty,IndustrialResaleProperty,AgriculturalResaleProperty]:  # Add all 8
            for prop in model.objects.all()[:50]:
                properties.append({
                    'id': prop.id,
                    # 'title': prop.property_title,
                    # 'url': prop.get_absolute_url(),
                    # 'type': prop.listing_type
                })

        context = {'admin_obj':admin_obj,'properties':properties}
        return render(request,"crm/UTM/create_utm_link.html",context) 
    else:
        return render(request,'home_page/Adminlogin.html')

############ Views end for create utm link ###########################


############# Views start for delete utm link ########################

@csrf_exempt
def delete_utm_crm(request):
    try:
        try:
            utm_id = request.POST.get('utm_id')
            UTMLink.objects.filter(id=utm_id).delete()
            return JsonResponse({'status':'1', 'msg':'Utm link details deleted successfully...'})
        except:
            traceback.print_exc()
            return JsonResponse({"status":"0", "msg" : "Something went wrong..."})
    except:
        traceback.print_exc()
        return JsonResponse({"status":"0", "msg" : "Something went wrong..."})

############# Views end for delete utm link ##########################

############## Views start for property enquiries section #####################

def property_enquiry_crm(request):
    session_id = request.session.get('Admin_id')
    if session_id:
        admin_obj = Admin_Login.objects.get(id=session_id)

        enquiry_obj = PropertyEnquiry.objects.all().order_by('-id')
        enquiry_obj_count = PropertyEnquiry.objects.all().count()

        rendered = render_to_string("crm/render_to_string/R_Enquiry/r_t_s_enquiry.html",{'enquiry_obj':enquiry_obj,'enquiry_obj_count':enquiry_obj_count})


        context = {'admin_obj':admin_obj,'property_enquiry_list':rendered}

        return render(request,"crm/Property_Enquiry/property_enquiry.html",context) 
    else:
        return render(request,'home_page/Adminlogin.html')

############# Views end for property enquiry section ###########################


############ Views start for delete property enquiry ########################

@csrf_exempt
def delete_property_enquiry(request):
    try:
        enquiry_id = request.POST.get('enquiry_id')
        
        # Get the enquiry first to access its utm_link
        enquiry = PropertyEnquiry.objects.filter(id=enquiry_id).first()
        
        if not enquiry:
            return JsonResponse({"status": "0", "msg": "Enquiry not found."})
        
        # Get the UTM link before deleting the enquiry
        utm_link = enquiry.utm_link
        
        # Delete the enquiry
        enquiry.delete()
        
        #  Decrement the total_enquiries count in UTMLink
        if utm_link:
            utm_link.total_enquiries = models.F('total_enquiries') - 1
            utm_link.save()
            utm_link.refresh_from_db()
            print(f"Decremented UTMLink enquiries for {utm_link.utm_source}: {utm_link.total_enquiries}")
        
        return JsonResponse({
            'status': '1', 
            'msg': 'Property Enquiry details deleted successfully.'
        })
        
    except Exception as e:
        import traceback
        traceback.print_exc()
        return JsonResponse({
            "status": "0", 
            "msg": f"Something went wrong: {str(e)}"
        })

########## Views end for delete property enquiry #########################


########### Views start for update property enquiry ##########################

def update_property_enquiry(request,id):
    session_id = request.session.get('Admin_id')
    if session_id:
        admin_obj = Admin_Login.objects.get(id=session_id)

        enquiry = PropertyEnquiry.objects.get(id=id)

        user_obj = User_Details.objects.filter(
                user_role__in=['Relationship Manager', 'Agent', 'Agency/Builder']
        ).annotate(
            sort_order=Case(
                When(user_role='Relationship Manager', then=Value(1)),         
                default=Value(2),   
                output_field=IntegerField(),
            )
        ).order_by('sort_order', '-id','user_role')

        context = {'admin_obj':admin_obj,'enquiry':enquiry,'user_obj':user_obj}

        return render(request,"crm/Property_Enquiry/update_enquiry.html",context) 
    else:
        return render(request,'home_page/Adminlogin.html')

############# Views end for update property enquiry ############################


############ Views start for ajax for update property enquiry ######################3

@csrf_exempt
def property_enquiry_ajax(request):
    data = request.POST.dict()

    try:
        enquiry = PropertyEnquiry.objects.get(id=data['id'])
    except PropertyEnquiry.DoesNotExist:
        return JsonResponse({'status': '0', 'msg': 'Propertyy Enquiry Details not found'})


    user = User_Details.objects.get(id=data['user'])

 
    if data['lead_status'] == "Closed" or data['lead_status'] == "Cancelled":
        closed_date = datetime.today()
    else:
        closed_date=None

    PropertyEnquiry.objects.filter(id=data['id']).update(lead_status=data['lead_status'],assigned_to=user,closed_date=closed_date,followup_notes=data['followup_notes'])

    return JsonResponse({"status":"1", "msg" : f"Property Enquiry Details updated successfully"})

############# Views end for ajax for update property enquiry ####################

def lead_report(request):
    session_id = request.session.get('Admin_id')
    if not session_id:
        return render(request, 'home_page/Adminlogin.html')

    admin_obj = Admin_Login.objects.get(id=session_id)
    
    lead = PropertyEnquiry.objects.all()

   
    

   
 
    context = {
        'admin_obj': admin_obj,
        'lead': lead,
       }

    return render(request, 'crm/lead_report.html', context)


