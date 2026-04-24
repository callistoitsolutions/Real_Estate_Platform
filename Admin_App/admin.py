from django.contrib import admin
from Admin_App.models import *
# Register your models here.


# Register your models here.

admin.site.register(Admin_Login)


######### Register Ameneties Details Model #####################

admin.site.register(Ameneties_Details)

############## Register Facilities Details Modal ###################

admin.site.register(Facilities_Details)

########### Register Service Type Details Model ##################

admin.site.register(Service_Type_Details)

########### Register User Details Table/Modal ###############

admin.site.register(User_Details)


########### Register  RentalResidentialProperty Table/Modal ###############

admin.site.register(RentalResidentialProperty)


########### Register  CommercialRentalProperty Table/Modal ###############

admin.site.register(CommercialRentalProperty)


########### Register ResaleResidentialProperty Table/Modal ###############

admin.site.register(ResaleResidentialProperty)


########### Register CommercialResaleProperty Table/Modal ###############

admin.site.register(CommercialResaleProperty)


############ Regiister Open Plot/Land Property Table/Modal ######################

admin.site.register(ResalePlotProperty)

############## Register Industrial Property Table/Modal ########################

admin.site.register(ResaleIndustrialProperty)

################ Register Agricultural Property Table/Modal ######################

admin.site.register(ResaleAgriculturalProperty)