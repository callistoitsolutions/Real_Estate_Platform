"""
URL configuration for Real_Estate project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from django.conf.urls.static import static
from django.conf import settings
# finance.api import router as finance_router

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('Main_App.urls')),
       
    path('Admin_App/',include('Admin_App.urls')),
    #path('Tenant_App/',include('Tenant_App.urls')),
    #path('Tenant_Panel/',include('Tenant_Panel.urls')),
    path('Landlord_Panel/',include('Landlord_Panel.urls')),
    path('CRM_Panel/',include('CRM_Panel.urls')),
    path('Agent_Dashboard/',include('Agent_Dashboard.urls')),
    path('RM_Dashboard/',include('RM_Dashboard.urls')),
    path('Vendors/',include('Vendors.urls')),
    path('Tenant_Panel/',include('Tenant_App.urls')),
    path('Buyer_Panel/',include('Buyer_App.urls')),
    path('seo/',include('seo.urls')),
    path('captcha/', include('captcha.urls')),
#path('api/', include(finance_router.urls)),
    #path('finance/', include('finance.urls')),
    path('oauth/', include('social_django.urls', namespace='social')),
   
   # path('',include('Admin_App.urls')),
   # path('Tenant_App/',include('Tenant_App.urls')),
   # path('Tenant_Panel/',include('Tenant_Panel.urls')),
   # path('Landlord_Panel/',include('Landlord_Panel.urls')),
   # path('CRM_Panel/',include('CRM_Panel.urls')),
   # path('Agent_Dashboard/',include('Agent_Dashboard.urls')),
   # path('RM_Dashboard/',include('RM_Dashboard.urls')),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)