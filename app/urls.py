from django.urls import path
from . import views
from .views import search_student

urlpatterns = [
    # path('admin/app/student_class/search/', search_student, name='search_student'),
    # path('admin/app/search-student/', views.search_student, name='search_student'),
    path('register/',views.register_view,name='register'),
    path('login/',views.login_view,name='login'),
    path('logout/',views.logout_view,name='logout'),
    path('dashboard/',views.dashboard_view,name='dashboard')
]