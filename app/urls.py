from django.urls import path
from . import views
from .views import search_student
from .views import custom_login, otp_verification, resend_otp
from django.conf import settings
from django.conf.urls.static import static
# from .admin import section1_site, section2_site

urlpatterns = [
    # path('admin/app/student_class/search/', search_student, name='search_student'),
    # path('admin/app/search-student/', views.search_student, name='search_student'),
    # path('section1-admin/', section1_site.urls),
    # path('section2-admin/', section2_site.urls),
    # path('login/', views.custom_login, name='custom_login'),
    # path('resend-otp/', resend_otp, name='resend_otp'),
    path('otp_verification/', otp_verification, name='otp_verification'),
    path('send-otp/', views.send_otp_verification, name='send_otp_verification'),
    path('send-otp-verification/', views.send_otp_verification_mobile_app, name='send_otp_verification_mobile_app'),
    path('verify-otp/', views.verify_otp, name='verify_otp'),
    path('student-payment-details/', views.action_student_payment_details, name='student_payment_details'),
    path('get-fee-receipts/', views.get_fee_receipts, name='get_fee_receipts'),
    path('generate-payment-url/', views.generate_payment_url, name='generate_payment_url'),
    path('payment-response/', views.payment_response, name='payment_response'),
    path('process-payment/', views.process_payment, name='process_payment'),
    path('register/',views.register_view,name='register'),
    # path('login/',views.login_view,name='login'),
    path('logout/',views.logout_view,name='logout'),
    path('dashboard/',views.dashboard_view,name='dashboard'),


    path('send-otp-verification-from-admin/', views.send_otp_verification_from_admin, name='send_otp_verification_from_admin'),
    path('verify-otp-for-admin/', views.verify_otp_for_admin, name='verify_otp_for_admin'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

