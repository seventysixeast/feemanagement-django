"""
URL configuration for feemanagement project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path, include
from django.contrib import admin
from django.urls import path
from app.views import custom_login, otp_verification
# from app.admin import section1_site, section2_site
# from app.admin import custom_admin_site  # Import the custom admin site
# import custom_ad

# urlpatterns = [
#     # Use the custom admin site
#     path('admin/', custom_admin_site.urls),
# ]


urlpatterns = [
    path('school-admin/login/', custom_login, name='custom_login'),
    # path('otp_verification/', otp_verification, name='otp_verification'),
    path('school-admin/', admin.site.urls),
    # path('school-admin/login/', custom_login, name='admin_login'),
    # path('school-admin/', section1_site.urls),
    # path('section2-admin/', section2_site.urls),
    # path('school-admin/', custom_admin_site.urls),
    # path('auth/', include('app.urls')),
    path('fees-section/', include('Fees_Section.urls')),
    path('reports/', include('Reports.urls')),
    path('', include('app.urls')),
]

admin.site.login = custom_login
