from django.shortcuts import render

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



def auto_lead_create(request):
    if request.method == 'POST':
        AutoLeadCapture.objects.create(
            name=request.POST.get('name'),
            property_id=request.POST.get('property_id'),
            source=request.POST.get('source'),
            inquiry_date=request.POST.get('inquiry_date'),
            contact=request.POST.get('contact')
        )
        return redirect('auto_lead_list')
    return render(request, 'crm/auto_capture.html')



from django.contrib import messages

def auto_lead_edit(request, pk):
    lead = get_object_or_404(AutoLeadCapture, pk=pk)

    if request.method == 'POST':
        lead.name = request.POST.get('name')
        lead.property_id = request.POST.get('property_id')
        lead.source = request.POST.get('source')
        lead.inquiry_date = request.POST.get('inquiry_date')
        lead.contact = request.POST.get('contact')
        lead.save()

        messages.success(request, "Lead updated successfully!")
        return redirect('auto_lead_edit', pk=lead.pk)  # stay on edit page to show alert

    return render(request, 'crm/auto_capture_edit.html', {'lead': lead})


def auto_lead_delete(request, pk):
    lead = get_object_or_404(AutoLeadCapture, pk=pk)
    lead.delete()
    return redirect('auto_lead_list')

 
def auto_lead_list(request):
    leads = AutoLeadCapture.objects.all()
    return render(request, 'crm/auto_lead_list.html', {'leads': leads})


def crm_dashboard(request):
    session_id = request.session.get('Admin_id')
    if session_id:
        admin_obj = Admin_Login.objects.get(id=session_id)
        context = {'admin_obj':admin_obj}
        return render(request,"crm/crm_dashboard.html",context) 
    else:
        return render(request,'home_page/Adminlogin.html')


def manual_lead_list(request):
    leads = ManualLeadEntry.objects.all().order_by("-created_at")
    return render(request, "crm/manual_lead_list.html", {"leads": leads})


def manual_lead_create(request):
    if request.method == "POST":
        ManualLeadEntry.objects.create(
            name=request.POST.get("name"),
            requirement_type=request.POST.get("requirement_type"),
            budget=request.POST.get("budget"),
            location=request.POST.get("location"),
            source=request.POST.get("source"),
            contact=request.POST.get("contact")
        )
       # return redirect("manual_lead_list")  # redirect to list after save
    
    return render(request, "crm/manual_entry.html")


    
    
    
def lead_status_create(request):
    if request.method == "POST":
        LeadStatusUpdate.objects.create(
            lead_id=request.POST.get("lead_id"),
            status=request.POST.get("status"),
            next_action=request.POST.get("next_action"),
            remarks=request.POST.get("remarks")
        )
        #return redirect("lead_status_list")  # redirect to list page
    
    return render(request, "crm/Lead_Status_Update_crm.html")
  #  return render(request,"crm/Lead_Status_Update_crm.html")
  
  
def lead_status_list(request):
    updates = LeadStatusUpdate.objects.all().order_by("-created_at")
    return render(request, "crm/lead_status_list.html", {"updates": updates})  

def Lead_Assignment_crm(request):
    return render(request,"crm/Lead_Assignment_crm.html")

def Lead_Assignment_crm(request):
    return render(request,"crm/Lead_Assignment_crm.html")


# Create new Lead Age Analysis entry
def lead_age_analysis_create(request):
    if request.method == "POST":
        LeadAgeAnalysis.objects.create(
            lead_id=request.POST.get("lead_id"),
            created_date=request.POST.get("created_date"),
            last_update=request.POST.get("last_update"),
            days_old=request.POST.get("days_old"),
        )
        return redirect("lead_age_analysis_list")
    return render(request, "crm/Lead_Age_Analysis.html")

# List all entries
def lead_age_analysis_list(request):
    analyses = LeadAgeAnalysis.objects.all().order_by("-created_at")
    return render(request, "crm/lead_age_analysis_list.html", {"analyses": analyses})


def wallet_transaction_create(request):
    if request.method == "POST":
        WalletTransaction.objects.create(
            user_id=request.POST.get("user_id"),
            transaction_type=request.POST.get("transaction_type"),
            amount=request.POST.get("amount"),
            reason=request.POST.get("reason"),
            balance=request.POST.get("balance"),
        )
        return redirect("wallet_transaction_list")
    return render(request, "crm/Wallet_Transaction.html")

# List Wallet Transactions
def wallet_transaction_list(request):
    transactions = WalletTransaction.objects.all().order_by("-created_at")
    return render(request, "crm/wallet_transaction_list.html", {"transactions": transactions})




# Create Wallet Recharge
def wallet_recharge_create(request):
    if request.method == "POST":
        WalletRecharge.objects.create(
            user_id=request.POST.get("user_id"),
            payment_mode=request.POST.get("payment_mode"),
            amount=request.POST.get("amount"),
            transaction_id=request.POST.get("transaction_id"),
        )
        return redirect("wallet_recharge_list")
    return render(request, "crm/Wallet_Recharge.html")

# List Wallet Recharges
def wallet_recharge_list(request):
    recharges = WalletRecharge.objects.all().order_by("-created_at")
    return render(request, "crm/wallet_recharge_list.html", {"recharges": recharges})




# Create Lead Buy Request
def lead_buy_request_create(request):
    if request.method == "POST":
        LeadBuyRequest.objects.create(
            lead_id=request.POST.get("lead_id"),
            agent_id=request.POST.get("agent_id"),
            wallet_deduction=request.POST.get("wallet_deduction"),
            status=request.POST.get("status"),
        )
        return redirect("lead_buy_request_list")
    return render(request, "crm/Lead_Buy_Request.html")

# List Lead Buy Requests
def lead_buy_request_list(request):
    requests = LeadBuyRequest.objects.all().order_by("-created_at")
    return render(request, "crm/lead_buy_request_list.html", {"requests": requests})





def Lead_History(request):
    return render(request,"crm/Lead_History.html")

def Bulk_Lead_Upload(request):
    return render(request,"crm/Bulk_Lead_Upload.html")






