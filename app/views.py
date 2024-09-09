from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from .middlewares import auth, guest
from django.http import JsonResponse
import json
from .models import student_master
from django.views.decorators.csrf import csrf_exempt


# # Create your views here.
# @csrf_exempt  # Allow POST requests without CSRF validation (for testing)
# def search_student(request):
#     print("++++++++++++++++++++++++++++++post+++++++++")
#     if request.method == 'POST':
#         data = json.loads(request.body)
#         student_name = data.get('student_name', '')
#         admission_no = data.get('admission_no', '')

#         # Query the student_master model
#         students = student_master.objects.filter(
#             student_name__icontains=student_name,
#             addmission_no=admission_no
#         )

#         # Serialize the results
#         results = [
#             {
#                 'id': student.student_id,
#                 'name': student.student_name,
#                 'admission_no': student.addmission_no,
#             }
#             for student in students
#         ]

#         return JsonResponse({'results': results})

#     return JsonResponse({'results': []})

@csrf_exempt
def search_student(request):
    print("+++++++++++++++++++++++++++++++++++++++")
    if request.method == 'POST':
        data = json.loads(request.body)
        student_name = data.get('student_name', '').strip()
        admission_no = data.get('admission_no', None)

        search_results = student_master.objects.all()

        if student_name:
            search_results = search_results.filter(student_name__icontains=student_name)
        if admission_no:
            search_results = search_results.filter(addmission_no=admission_no)

        students = list(search_results.values('pk', 'student_name', 'addmission_no', 'class_no', 'section'))
        return JsonResponse(students, safe=False)

    return JsonResponse({"error": "Invalid request"}, status=400)

@guest
def register_view(request):
    if request.method =='POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request,user)
            return redirect('dashboard')
    else:
        initial_data = { 'username':'', 'password1':'', 'password2':''}
        form = UserCreationForm(initial=initial_data)
    return render(request, 'auth/register.html',{'form':form})    

@guest
def login_view(request):
    if request.method =='POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request,user)
            return redirect('dashboard')
    else:
        initial_data = { 'username':'', 'password':''}
        form = AuthenticationForm(initial=initial_data)
    return render(request, 'auth/login.html',{'form':form}) 

@auth
def dashboard_view(request):
    return render(request, 'dashboard.html')

def logout_view(request):
    logout(request)
    return redirect('login')
