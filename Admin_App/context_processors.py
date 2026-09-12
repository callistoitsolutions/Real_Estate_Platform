from datetime import date
from datetime import datetime
from Admin_App.models import *


def admin_alerts(request):

    rental_count_alert = RentalResidentialProperty.objects.filter(is_deleted=False,approval_status="Pending").count()
    commercial_count_alert = CommercialRentalProperty.objects.filter(is_deleted=False,approval_status="Pending").count()
    pg_count_alert = PGColivingProperty.objects.filter(is_deleted=False,approval_status="Pending").count()
    resale_count_alert = ResaleResidentialProperty.objects.filter(is_deleted=False,approval_status="Pending").count()
    commercial_resale_count_alert = CommercialResaleProperty.objects.filter(is_deleted=False,approval_status="Pending").count()
        
    industrial_resale_count_alert = IndustrialResaleProperty.objects.filter(is_deleted=False,approval_status="Pending").count()
    agricultural_resale_count_alert = AgriculturalResaleProperty.objects.filter(is_deleted=False,approval_status="Pending").count()
        
    # ── NEW: Plot Resale modules (Residential Plot/ Commercial Plot/ Industrial Plot / Agricultural Plot) ──

    residential_plot_count_alert = ResidentialPlotResaleProperty.objects.filter(is_deleted=False,approval_status="Pending").count()
    commercial_plot_count_alert = CommercialPlotResaleProperty.objects.filter(is_deleted=False,approval_status="Pending").count()
    industrial_plot_count_alert = IndustrialPlotResaleProperty.objects.filter(is_deleted=False,approval_status="Pending").count()
    agricultural_plot_count_alert = AgriculturalPlotResaleProperty.objects.filter(is_deleted=False,approval_status="Pending").count()


    total_count_alert = rental_count_alert + commercial_count_alert + pg_count_alert + resale_count_alert +   commercial_resale_count_alert + industrial_resale_count_alert + agricultural_resale_count_alert + residential_plot_count_alert + commercial_plot_count_alert + industrial_plot_count_alert + agricultural_plot_count_alert

    landlord_count = Subscription_Purchase_Details.objects.filter(fk_user__user_role="Landlord",plan_status="Pending").count()
    agent_count = Subscription_Purchase_Details.objects.filter(fk_user__user_role="Agent",plan_status="Pending").count()
    agency_count = Subscription_Purchase_Details.objects.filter(fk_user__user_role="Agency/Builder",plan_status="Pending").count()
    tenant_count = Subscription_Purchase_Details.objects.filter(fk_user__user_role="Tenant",plan_status="Pending").count()
    buyer_count = Subscription_Purchase_Details.objects.filter(fk_user__user_role="Buyer",plan_status="Pending").count()
    vendor_count = Subscription_Purchase_Details.objects.filter(fk_user__user_role="Vendor",plan_status="Pending").count()

    total_pending_count = landlord_count + agent_count + agency_count + tenant_count + buyer_count + vendor_count


    return {
        'total_count':total_count_alert,
        'total_pending_count':total_pending_count
    }


