from datetime import date
from datetime import datetime
from Admin_App.models import *


def admin_alerts(request):

    rental_count = RentalResidentialProperty.objects.filter(is_deleted=False,approval_status="Pending").count()
    commercial_count = CommercialRentalProperty.objects.filter(is_deleted=False,approval_status="Pending").count()
    pg_count= PGColivingProperty.objects.filter(is_deleted=False,approval_status="Pending").count()
    resale_count = ResaleResidentialProperty.objects.filter(is_deleted=False,approval_status="Pending").count()
    commercial_resale_count = CommercialResaleProperty.objects.filter(is_deleted=False,approval_status="Pending").count()
        
    industrial_resale_count = IndustrialResaleProperty.objects.filter(is_deleted=False,approval_status="Pending").count()
    agricultural_resale_count = AgriculturalResaleProperty.objects.filter(is_deleted=False,approval_status="Pending").count()
        
    # ── NEW: Plot Resale modules (Residential Plot/ Commercial Plot/ Industrial Plot / Agricultural Plot) ──

    residential_plot_count = ResidentialPlotResaleProperty.objects.filter(is_deleted=False,approval_status="Pending").count()
    commercial_plot_count = CommercialPlotResaleProperty.objects.filter(is_deleted=False,approval_status="Pending").count()
    industrial_plot_count = IndustrialPlotResaleProperty.objects.filter(is_deleted=False,approval_status="Pending").count()
    agricultural_plot_count = AgriculturalPlotResaleProperty.objects.filter(is_deleted=False,approval_status="Pending").count()


    total_count = rental_count + commercial_count + pg_count + resale_count +   commercial_resale_count + industrial_resale_count + agricultural_resale_count + residential_plot_count + commercial_plot_count + industrial_plot_count + agricultural_plot_count

    landlord_count = Subscription_Purchase_Details.objects.filter(fk_user__user_role="Landlord",plan_status="Pending").count()
    agent_count = Subscription_Purchase_Details.objects.filter(fk_user__user_role="Agent",plan_status="Pending").count()
    agency_count = Subscription_Purchase_Details.objects.filter(fk_user__user_role="Agency/Builder",plan_status="Pending").count()
    tenant_count = Subscription_Purchase_Details.objects.filter(fk_user__user_role="Tenant",plan_status="Pending").count()
    buyer_count = Subscription_Purchase_Details.objects.filter(fk_user__user_role="Buyer",plan_status="Pending").count()
    vendor_count = Subscription_Purchase_Details.objects.filter(fk_user__user_role="Vendor",plan_status="Pending").count()

    total_pending_count = landlord_count + agent_count + agency_count + tenant_count + buyer_count + vendor_count


    return {
        'total_count':total_count,
        'total_pending_count':total_pending_count
    }


