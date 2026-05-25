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
        context = {'admin_obj':admin_obj}
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

############## Views start for property enquiries section #####################

def property_enquiry_crm(request):
    session_id = request.session.get('Admin_id')
    if session_id:
        admin_obj = Admin_Login.objects.get(id=session_id)
        context = {'admin_obj':admin_obj}
        return render(request,"crm/Property_Enquiry/property_enquiry.html",context) 
    else:
        return render(request,'home_page/Adminlogin.html')

############# Views end for property enquiry section ###########################




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


