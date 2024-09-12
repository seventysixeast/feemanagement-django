from django.urls import path
from . import views
from .views import search_student
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # path('admin/app/student_class/search/', search_student, name='search_student'),
    # path('admin/app/search-student/', views.search_student, name='search_student'),
    path('send-otp/', views.send_otp_verification, name='send_otp_verification'),
    path('student-payment-details/', views.action_student_payment_details, name='student_payment_details'),
    path('get-fee-receipts/', views.get_fee_receipts, name='get_fee_receipts'),
    path('generate-payment-url/', views.generate_payment_url, name='generate_payment_url'),
    path('payment-response/', views.payment_response, name='payment_response'),
    path('process-payment/', views.process_payment, name='process_payment'),
    path('register/',views.register_view,name='register'),
    path('login/',views.login_view,name='login'),
    path('logout/',views.logout_view,name='logout'),
    path('dashboard/',views.dashboard_view,name='dashboard')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)