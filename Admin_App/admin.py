from django.contrib import admin
from Admin_App.models import *
# Register your models here.


# Register your models here.

admin.site.register(Admin_Login)

############## Register Active Visitors Modal #######################

admin.site.register(ActiveVisitor)

######### Register Ameneties Details Model #####################

admin.site.register(Ameneties_Details)

############## Register Facilities Details Modal ###################

admin.site.register(Facilities_Details)

########### Register Service Type Details Model ##################

admin.site.register(Service_Type_Details)

########### Register User Details Table/Modal ###############

admin.site.register(User_Details)

############ Register Subscription Package Details Table/Modal #################

#admin.site.register(Package_Details)

########### Register Subscription Plan Details Table/Modal ###################

#admin.site.register(Plan_Details)

############# Register Subscription Details Table/Modal ####################

admin.site.register(Subscription_Details)

########### Register  RentalResidentialProperty Table/Modal ###############

admin.site.register(RentalResidentialProperty)


########### Register  RentalResidentialVideo Table/Modal ###############

admin.site.register(RentalResidentialVideo)


########### Register  RentalResidentialImages Table/Modal ###############

admin.site.register(RentalResidentialImage)

########### Register RentalActivityLog Table/Modal ###############

admin.site.register(RentalActivityLog)

########### Register  CommercialRentalProperty Table/Modal ###############

admin.site.register(CommercialRentalProperty)

########### Register  PGRentalProperty Table/Modal ###############


admin.site.register(PGColivingProperty)


########### Register  PGRentalVideoProperty Table/Modal ###############


admin.site.register(PGColivingVideo)

########### Register  CommercialRentalImageProperty Table/Modal ###############


admin.site.register(CommercialRentalPropertyImage)

########### Register ResaleResidentialProperty Table/Modal ###############

admin.site.register(CommercialRentalVideo)

########### Register ResaleResidentialProperty Table/Modal ###############

admin.site.register(ResaleResidentialProperty)
admin.site.register(ResaleResidentialFAQ)
admin.site.register(ResalePropertyImage)
admin.site.register(ResaleResidentialVideo)


########### Register CommercialResaleProperty Table/Modal ###############

admin.site.register(CommercialResaleProperty)

############# Register Plot Resale Property Table/Modal ###############

admin.site.register(PlotSaleProperty)

############### Register Industrial Resale Property Table/Modal #################

admin.site.register(IndustrialResaleProperty)

############ Register Agicultural Resale Property Table/Modal ##################3

admin.site.register(AgriculturalResaleProperty)


############ Register Industrial Plot Resale Property Table/Modal ##################3

admin.site.register(IndustrialPlotResaleProperty)


############ Register Industrial Plot Resale Video Property Table/Modal ##################3

admin.site.register(IndustrialPlotResaleVideo)


############ Register Agriculture Plot Resale Property Table/Modal ##################3

admin.site.register(AgriculturalPlotResaleProperty)


############ Register Agriculture Plot Resale Video Property Table/Modal ##################3

admin.site.register(AgriculturalPlotResaleVideo)
