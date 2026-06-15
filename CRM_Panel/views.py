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

        ################ Notifications Section ######################

        enquiry_obj_today = PropertyEnquiry.objects.filter(enquiry_date=datetime.today()).count()

        context = {'admin_obj':admin_obj,'enquiry_obj_today':enquiry_obj_today}
        return render(request,"crm/crm_dashboard.html",context) 
    else:
        return render(request,'home_page/Adminlogin.html')
    

############# Views start for today's property enquiry ######################

def today_property_enquiry(request):
    session_id = request.session.get('Admin_id')
    if session_id:
        admin_obj = Admin_Login.objects.get(id=session_id)

        enquiry_obj = PropertyEnquiry.objects.filter(enquiry_date=datetime.today()).order_by('-id')
        enquiry_obj_count = PropertyEnquiry.objects.filter(enquiry_date=datetime.today()).count()

        ############## Enquiries Stats By Source ##############################

        fb_obj_count = PropertyEnquiry.objects.filter(utm_link__utm_source="facebook",enquiry_date=datetime.today()).count()
        insta_obj_count = PropertyEnquiry.objects.filter(utm_link__utm_source="instagram",enquiry_date=datetime.today()).count()
        whatsapp_obj_count = PropertyEnquiry.objects.filter(utm_link__utm_source="whatsapp",enquiry_date=datetime.today()).count()
        google_obj_count = PropertyEnquiry.objects.filter(utm_link__utm_source="google",enquiry_date=datetime.today()).count()
        linkedin_obj_count = PropertyEnquiry.objects.filter(utm_link__utm_source="linkedin",enquiry_date=datetime.today()).count()
        twitter_obj_count = PropertyEnquiry.objects.filter(utm_link__utm_source="twitter",enquiry_date=datetime.today()).count()
        youtube_obj_count = PropertyEnquiry.objects.filter(utm_link__utm_source="youtube",enquiry_date=datetime.today()).count()
        referral_obj_count = PropertyEnquiry.objects.filter(utm_link__utm_source="referral",enquiry_date=datetime.today()).count()

        ########### Enquiry Stats by lead source ################################

        pending_obj_count = PropertyEnquiry.objects.filter(lead_status="Pending",enquiry_date=datetime.today()).count()
        progress_obj_count = PropertyEnquiry.objects.filter(lead_status="In Progress",enquiry_date=datetime.today()).count()
        hold_obj_count = PropertyEnquiry.objects.filter(lead_status="Hold",enquiry_date=datetime.today()).count()
        closed_obj_count = PropertyEnquiry.objects.filter(lead_status="Closed",enquiry_date=datetime.today()).count()
        cancelled_obj_count = PropertyEnquiry.objects.filter(lead_status="Cancelled",enquiry_date=datetime.today()).count()

        rendered = render_to_string("crm/render_to_string/R_Enquiry/r_t_s_enquiry.html",{'enquiry_obj':enquiry_obj,'enquiry_obj_count':enquiry_obj_count,'fb_obj_count':fb_obj_count,'insta_obj_count':insta_obj_count,'whatsapp_obj_count':whatsapp_obj_count,'google_obj_count':google_obj_count,'linkedin_obj_count':linkedin_obj_count,'twitter_obj_count':twitter_obj_count,'youtube_obj_count':youtube_obj_count,'referral_obj_count':referral_obj_count,'pending_obj_count':pending_obj_count,'progress_obj_count':progress_obj_count,'hold_obj_count':hold_obj_count,'closed_obj_count':closed_obj_count,'cancelled_obj_count':cancelled_obj_count})

        ################ Notifications Section ######################

        enquiry_obj_today = PropertyEnquiry.objects.filter(enquiry_date=datetime.today()).count()

        context = {'admin_obj':admin_obj,'property_enquiry_list':rendered,'enquiry_obj_today':enquiry_obj_today}
        
        return render(request,"crm/Property_Enquiry/today_enquiry.html",context) 
    else:
        return render(request,'home_page/Adminlogin.html')

############### Views end for today's property enquiry ########################


############## Views start for property enquiry status ########################

def property_enquiry_status(request):
    session_id = request.session.get('Admin_id')
    if session_id:
        admin_obj = Admin_Login.objects.get(id=session_id)

        ################ Notifications Section ######################

        enquiry_obj_today = PropertyEnquiry.objects.filter(enquiry_date=datetime.today()).count()

        context = {'admin_obj':admin_obj,'enquiry_obj_today':enquiry_obj_today}
        return render(request,"crm/Property_Enquiry/property_enquiry_status.html",context) 
    else:
        return render(request,'home_page/Adminlogin.html')

############ Views end for property enquiry status ############################
    


############## Views start for display utm links ###########################

def utm_links_crm(request):
    session_id = request.session.get('Admin_id')
    if session_id:
        admin_obj = Admin_Login.objects.get(id=session_id)

        utm_obj = UTMLink.objects.all().order_by('-id')
        utm_obj_count = UTMLink.objects.all().count()

        rendered = render_to_string("crm/render_to_string/R_Utm/r_t_s_utm.html",{'utm_obj':utm_obj,'utm_obj_count':utm_obj_count})

        ################ Notifications Section ######################

        enquiry_obj_today = PropertyEnquiry.objects.filter(enquiry_date=datetime.today()).count()

        context = {'admin_obj':admin_obj,'utm_lists':rendered,'enquiry_obj_today':enquiry_obj_today}
        
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

        ################ Notifications Section ######################

        enquiry_obj_today = PropertyEnquiry.objects.filter(enquiry_date=datetime.today()).count()

        context = {'admin_obj':admin_obj,'properties':properties,'enquiry_obj_today':enquiry_obj_today}

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

        ############## Enquiries Stats By Source ##############################

        fb_obj_count = PropertyEnquiry.objects.filter(utm_link__utm_source="facebook").count()
        insta_obj_count = PropertyEnquiry.objects.filter(utm_link__utm_source="instagram").count()
        whatsapp_obj_count = PropertyEnquiry.objects.filter(utm_link__utm_source="whatsapp").count()
        google_obj_count = PropertyEnquiry.objects.filter(utm_link__utm_source="google").count()
        linkedin_obj_count = PropertyEnquiry.objects.filter(utm_link__utm_source="linkedin").count()
        twitter_obj_count = PropertyEnquiry.objects.filter(utm_link__utm_source="twitter").count()
        youtube_obj_count = PropertyEnquiry.objects.filter(utm_link__utm_source="youtube").count()
        referral_obj_count = PropertyEnquiry.objects.filter(utm_link__utm_source="referral").count()

        ########### Enquiry Stats by lead source ################################

        pending_obj_count = PropertyEnquiry.objects.filter(lead_status="Pending").count()
        progress_obj_count = PropertyEnquiry.objects.filter(lead_status="In Progress").count()
        hold_obj_count = PropertyEnquiry.objects.filter(lead_status="Hold").count()
        closed_obj_count = PropertyEnquiry.objects.filter(lead_status="Closed").count()
        cancelled_obj_count = PropertyEnquiry.objects.filter(lead_status="Cancelled").count()

        rendered = render_to_string("crm/render_to_string/R_Enquiry/r_t_s_enquiry.html",{'enquiry_obj':enquiry_obj,'enquiry_obj_count':enquiry_obj_count,'fb_obj_count':fb_obj_count,'insta_obj_count':insta_obj_count,'whatsapp_obj_count':whatsapp_obj_count,'google_obj_count':google_obj_count,'linkedin_obj_count':linkedin_obj_count,'twitter_obj_count':twitter_obj_count,'youtube_obj_count':youtube_obj_count,'referral_obj_count':referral_obj_count,'pending_obj_count':pending_obj_count,'progress_obj_count':progress_obj_count,'hold_obj_count':hold_obj_count,'closed_obj_count':closed_obj_count,'cancelled_obj_count':cancelled_obj_count})

        ################ Notifications Section ######################

        enquiry_obj_today = PropertyEnquiry.objects.filter(enquiry_date=datetime.today()).count()

        context = {'admin_obj':admin_obj,'property_enquiry_list':rendered,'enquiry_obj_today':enquiry_obj_today}

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

        ################ Notifications Section ######################

        enquiry_obj_today = PropertyEnquiry.objects.filter(enquiry_date=datetime.today()).count()

        context = {'admin_obj':admin_obj,'enquiry':enquiry,'user_obj':user_obj,'enquiry_obj_today':enquiry_obj_today}

        return render(request,"crm/Property_Enquiry/update_enquiry.html",context) 
    else:
        return render(request,'home_page/Adminlogin.html')

############# Views end for update property enquiry ############################


############## Views start Helper function to check validity to assign rm ################

def can_assign_lead_to_rm(rm_user, exclude_enquiry_id=None, max_leads=4):
    """
    Check if an RM can be assigned a new lead.
    
    Args:
        rm_user: User_Details object of the RM
        exclude_enquiry_id: ID of the current enquiry to exclude from count (for updates)
        max_leads: Maximum allowed leads (default: 4)
    
    Returns:
        tuple: (can_assign, current_count, message)
    """
    
    # Base queryset
    queryset = PropertyEnquiry.objects.filter(
        assigned_to=rm_user,
        lead_status__in=['Pending', 'In Progress', 'Hold']
    )
    
    # Exclude current enquiry if provided (for update operations)
    if exclude_enquiry_id:
        queryset = queryset.exclude(id=exclude_enquiry_id)
    
    current_count = queryset.count()
    can_assign = current_count < max_leads
    
    if can_assign:
        message = f"{rm_user.user_name} can be assigned. Current active leads: {current_count}/{max_leads}"
    else:
        message = f"{rm_user.user_name} already has {current_count} active leads. Maximum allowed is {max_leads}."
    
    return can_assign, current_count, message


############# Views end for helper function to assign rm validation #####################



############ Views start for ajax for update property enquiry ######################3

@csrf_exempt
def property_enquiry_ajax(request):
    data = request.POST.dict()

    try:
        enquiry = PropertyEnquiry.objects.get(id=data['id'])
    except PropertyEnquiry.DoesNotExist:
        return JsonResponse({'status': '0', 'msg': 'Property Enquiry Details not found'})

    try:
        assigned_user = User_Details.objects.get(id=data['user'])
    except User_Details.DoesNotExist:
        return JsonResponse({'status': '0', 'msg': 'User not found'})

    MAX_LEADS = 4
    
    # Check if assignment is changing (different RM)
    if str(enquiry.assigned_to_id) != str(data['user']):
        can_assign, current_count, message = can_assign_lead_to_rm(
            assigned_user, 
            exclude_enquiry_id=enquiry.id, 
            max_leads=MAX_LEADS
        )
        
        if not can_assign:
            return JsonResponse({
                'status': '0',
                'msg': message,
                'current_count': current_count,
                'max_allowed': MAX_LEADS
            })
    
    # Set closed date
    if data['lead_status'] in ["Closed", "Cancelled"]:
        closed_date = datetime.today()
    else:
        closed_date = None
    
    # Update enquiry
    PropertyEnquiry.objects.filter(id=data['id']).update(
        lead_status=data['lead_status'],
        assigned_to=assigned_user,
        closed_date=closed_date,
        followup_notes=data['followup_notes']
    )
    
    # Get final count for response
    final_count = PropertyEnquiry.objects.filter(
        assigned_to=assigned_user,
        lead_status__in=['Pending', 'In Progress', 'Hold']
    ).count()
    
    return JsonResponse({
        "status": "1",
        "msg": f"Enquiry updated successfully!\n\n{assigned_user.user_name} now has {final_count}/{MAX_LEADS} active leads.",
        "active_leads_count": final_count,
        "max_allowed": MAX_LEADS,
        "remaining_slots": MAX_LEADS - final_count
    })

############# Views end for ajax for update property enquiry ####################


############ Views start for ajax for filter by source ########################

@csrf_exempt
def filter_source(request):
    par = request.POST.get('par')


    enquiry_obj = PropertyEnquiry.objects.filter(utm_link__utm_source=par).order_by('-id')
    enquiry_obj_count = PropertyEnquiry.objects.filter(utm_link__utm_source=par).count()

    ############## Enquiries Stats By Source ##############################

    fb_obj_count = PropertyEnquiry.objects.filter(utm_link__utm_source="facebook").count()
    insta_obj_count = PropertyEnquiry.objects.filter(utm_link__utm_source="instagram").count()
    whatsapp_obj_count = PropertyEnquiry.objects.filter(utm_link__utm_source="whatsapp").count()
    google_obj_count = PropertyEnquiry.objects.filter(utm_link__utm_source="google").count()
    linkedin_obj_count = PropertyEnquiry.objects.filter(utm_link__utm_source="linkedin").count()
    twitter_obj_count = PropertyEnquiry.objects.filter(utm_link__utm_source="twitter").count()
    youtube_obj_count = PropertyEnquiry.objects.filter(utm_link__utm_source="youtube").count()
    referral_obj_count = PropertyEnquiry.objects.filter(utm_link__utm_source="referral").count()

    ########### Enquiry Stats by lead source ################################

    pending_obj_count = PropertyEnquiry.objects.filter(lead_status="Pending").count()
    progress_obj_count = PropertyEnquiry.objects.filter(lead_status="In Progress").count()
    hold_obj_count = PropertyEnquiry.objects.filter(lead_status="Hold").count()
    closed_obj_count = PropertyEnquiry.objects.filter(lead_status="Closed").count()
    cancelled_obj_count = PropertyEnquiry.objects.filter(lead_status="Cancelled").count()

    rendered = render_to_string("crm/render_to_string/R_Enquiry/r_t_s_enquiry.html",{'enquiry_obj':enquiry_obj,'enquiry_obj_count':enquiry_obj_count,'fb_obj_count':fb_obj_count,'insta_obj_count':insta_obj_count,'whatsapp_obj_count':whatsapp_obj_count,'google_obj_count':google_obj_count,'linkedin_obj_count':linkedin_obj_count,'twitter_obj_count':twitter_obj_count,'youtube_obj_count':youtube_obj_count,'referral_obj_count':referral_obj_count,'pending_obj_count':pending_obj_count,'progress_obj_count':progress_obj_count,'hold_obj_count':hold_obj_count,'closed_obj_count':closed_obj_count,'cancelled_obj_count':cancelled_obj_count})

    return HttpResponse(rendered)

############ Views end for ajax for filter by source ###############################


############# Views start for ajax for filter by lead status #######################

@csrf_exempt
def filter_status(request):
    par = request.POST.get('par')

    if par == "all":
        enquiry_obj = PropertyEnquiry.objects.all().order_by('-id')
        enquiry_obj_count = PropertyEnquiry.objects.all().count()
    else:
        enquiry_obj = PropertyEnquiry.objects.filter(lead_status=par).order_by('-id')
        enquiry_obj_count = PropertyEnquiry.objects.filter(lead_status=par).count()

    ############## Enquiries Stats By Source ##############################

    fb_obj_count = PropertyEnquiry.objects.filter(utm_link__utm_source="facebook").count()
    insta_obj_count = PropertyEnquiry.objects.filter(utm_link__utm_source="instagram").count()
    whatsapp_obj_count = PropertyEnquiry.objects.filter(utm_link__utm_source="whatsapp").count()
    google_obj_count = PropertyEnquiry.objects.filter(utm_link__utm_source="google").count()
    linkedin_obj_count = PropertyEnquiry.objects.filter(utm_link__utm_source="linkedin").count()
    twitter_obj_count = PropertyEnquiry.objects.filter(utm_link__utm_source="twitter").count()
    youtube_obj_count = PropertyEnquiry.objects.filter(utm_link__utm_source="youtube").count()
    referral_obj_count = PropertyEnquiry.objects.filter(utm_link__utm_source="referral").count()

    ########### Enquiry Stats by lead source ################################

    pending_obj_count = PropertyEnquiry.objects.filter(lead_status="Pending").count()
    progress_obj_count = PropertyEnquiry.objects.filter(lead_status="In Progress").count()
    hold_obj_count = PropertyEnquiry.objects.filter(lead_status="Hold").count()
    closed_obj_count = PropertyEnquiry.objects.filter(lead_status="Closed").count()
    cancelled_obj_count = PropertyEnquiry.objects.filter(lead_status="Cancelled").count()

    rendered = render_to_string("crm/render_to_string/R_Enquiry/r_t_s_enquiry.html",{'enquiry_obj':enquiry_obj,'enquiry_obj_count':enquiry_obj_count,'fb_obj_count':fb_obj_count,'insta_obj_count':insta_obj_count,'whatsapp_obj_count':whatsapp_obj_count,'google_obj_count':google_obj_count,'linkedin_obj_count':linkedin_obj_count,'twitter_obj_count':twitter_obj_count,'youtube_obj_count':youtube_obj_count,'referral_obj_count':referral_obj_count,'pending_obj_count':pending_obj_count,'progress_obj_count':progress_obj_count,'hold_obj_count':hold_obj_count,'closed_obj_count':closed_obj_count,'cancelled_obj_count':cancelled_obj_count})

    return HttpResponse(rendered)

############# Views end for ajax for filter by lead status ##########################


############# Views start for ajax for datewise filter #############################

@csrf_exempt
def date_property_filter(request):
    if request.method=="POST":
        start_date= request.POST.get('start_date')
        end_date= request.POST.get('end_date')
        lead_source = request.POST.get('lead_source')
        lead_status = request.POST.get('lead_status')

        if lead_source != "All" and lead_status != "All":
            # Case 1: Both filters applied
            enquiry_obj = PropertyEnquiry.objects.filter(
                enquiry_date__gte=start_date,
                enquiry_date__lte=end_date,
                utm_link__utm_source=lead_source,
                lead_status=lead_status
            ).order_by('-id')
            enquiry_obj_count= PropertyEnquiry.objects.filter(
                enquiry_date__gte=start_date,
                enquiry_date__lte=end_date,
                utm_link__utm_source=lead_source,
                lead_status=lead_status
            ).count()
        
        elif lead_source != "All" and lead_status == "All":
            # Case 2: Only source filter, all statuses
            enquiry_obj = PropertyEnquiry.objects.filter(
                enquiry_date__gte=start_date,
                enquiry_date__lte=end_date,
                utm_link__utm_source=lead_source
            ).order_by('-id')
            enquiry_obj_count = PropertyEnquiry.objects.filter(
                enquiry_date__gte=start_date,
                enquiry_date__lte=end_date,
                utm_link__utm_source=lead_source
            ).count()
        
        elif lead_source == "All" and lead_status != "All":
            # Case 3: Only status filter, all sources
            enquiry_obj = PropertyEnquiry.objects.filter(
                enquiry_date__gte=start_date,
                enquiry_date__lte=end_date,
                lead_status=lead_status
            ).order_by('-id')
            enquiry_obj_count = PropertyEnquiry.objects.filter(
                enquiry_date__gte=start_date,
                enquiry_date__lte=end_date,
                lead_status=lead_status
            ).count()
        
        else:
            # Case 4: No filters (All sources, All statuses)
            enquiry_obj = PropertyEnquiry.objects.filter(
                enquiry_date__gte=start_date,
                enquiry_date__lte=end_date
            ).order_by('-id')
            enquiry_obj_count = PropertyEnquiry.objects.filter(
                enquiry_date__gte=start_date,
                enquiry_date__lte=end_date
            ).count()


    ############## Enquiries Stats By Source ##############################

    fb_obj_count = PropertyEnquiry.objects.filter(enquiry_date__gte=start_date,
                enquiry_date__lte=end_date,utm_link__utm_source="facebook").count()
    insta_obj_count = PropertyEnquiry.objects.filter(enquiry_date__gte=start_date,
                enquiry_date__lte=end_date,utm_link__utm_source="instagram").count()
    whatsapp_obj_count = PropertyEnquiry.objects.filter(enquiry_date__gte=start_date,
                enquiry_date__lte=end_date,utm_link__utm_source="whatsapp").count()
    google_obj_count = PropertyEnquiry.objects.filter(enquiry_date__gte=start_date,
                enquiry_date__lte=end_date,utm_link__utm_source="google").count()
    linkedin_obj_count = PropertyEnquiry.objects.filter(enquiry_date__gte=start_date,
                enquiry_date__lte=end_date,utm_link__utm_source="linkedin").count()
    twitter_obj_count = PropertyEnquiry.objects.filter(enquiry_date__gte=start_date,
                enquiry_date__lte=end_date,utm_link__utm_source="twitter").count()
    youtube_obj_count = PropertyEnquiry.objects.filter(enquiry_date__gte=start_date,
                enquiry_date__lte=end_date,utm_link__utm_source="youtube").count()
    referral_obj_count = PropertyEnquiry.objects.filter(enquiry_date__gte=start_date,
                enquiry_date__lte=end_date,utm_link__utm_source="referral").count()

    ########### Enquiry Stats by lead source ################################

    pending_obj_count = PropertyEnquiry.objects.filter(enquiry_date__gte=start_date,
                enquiry_date__lte=end_date,lead_status="Pending").count()
    progress_obj_count = PropertyEnquiry.objects.filter(enquiry_date__gte=start_date,
                enquiry_date__lte=end_date,lead_status="In Progress").count()
    hold_obj_count = PropertyEnquiry.objects.filter(enquiry_date__gte=start_date,
                enquiry_date__lte=end_date,lead_status="Hold").count()
    closed_obj_count = PropertyEnquiry.objects.filter(enquiry_date__gte=start_date,
                enquiry_date__lte=end_date,lead_status="Closed").count()
    cancelled_obj_count = PropertyEnquiry.objects.filter(enquiry_date__gte=start_date,
                enquiry_date__lte=end_date,lead_status="Cancelled").count()

    rendered = render_to_string("crm/render_to_string/R_Enquiry/r_t_s_enquiry.html",{'enquiry_obj':enquiry_obj,'enquiry_obj_count':enquiry_obj_count,'fb_obj_count':fb_obj_count,'insta_obj_count':insta_obj_count,'whatsapp_obj_count':whatsapp_obj_count,'google_obj_count':google_obj_count,'linkedin_obj_count':linkedin_obj_count,'twitter_obj_count':twitter_obj_count,'youtube_obj_count':youtube_obj_count,'referral_obj_count':referral_obj_count,'pending_obj_count':pending_obj_count,'progress_obj_count':progress_obj_count,'hold_obj_count':hold_obj_count,'closed_obj_count':closed_obj_count,'cancelled_obj_count':cancelled_obj_count})

    return HttpResponse(rendered)   
    


############# Views end ffor ajax for datewise filter ###########################

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


