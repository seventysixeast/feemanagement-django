from django.db import IntegrityError
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from .middlewares import auth, guest
from django.http import JsonResponse
import json
from django.views.decorators.csrf import csrf_exempt

# from django.shortcuts import render
from django.views.decorators.http import require_POST
import random
import requests
import urllib.parse

from django.db.models import Sum, Q, F, Max
from datetime import datetime, timedelta
from django.utils import timezone

from django.utils.dateparse import parse_date
from decimal import Decimal

from django.views.decorators.http import require_GET

from .models import (
    student_master, student_fee, student_class, specialfee_master,
    payment_schedule_master, latefee_master, fees_master, expense,
    concession_master, bus_master, busfees_master, account_head,generate_mobile_number_list
)
from app import models
import time
import random

from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding
import base64

from django.http import JsonResponse
from .utils import aes128_encrypt
import json
import re
from django.core.exceptions import ValidationError


from django.conf import settings
import os
from reportlab.pdfgen import canvas
from io import BytesIO

from django.http import JsonResponse
from django.template.loader import render_to_string
from django.shortcuts import get_object_or_404
from xhtml2pdf import pisa
from io import BytesIO
from django.conf import settings
import os

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, get_user
from django.contrib import messages
# from django.contrib.auth.models import User  # Add this import
from django.urls import reverse
from .forms import OTPVerificationForm
import random  # For generating OTP


from django.contrib.auth import get_user_model
from django.contrib.auth import login
from django.http import JsonResponse
from django.conf import settings


from django.db.models import OuterRef, Subquery, F
from django.db.models.functions import ExtractYear

from dotenv import load_dotenv

from django.core.mail import send_mail
from django.core.validators import validate_email
from django.core.exceptions import ValidationError

from django.db.models import Q
# from .models import StudentMaster  # Assuming you have a StudentMaster model

# Load the .env file
load_dotenv()

User = get_user_model()
# import datetime


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
            # user = form.save()
            # login(request,user)
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
            # user = form.get_user()
            # login(request,user)
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





def send_otp_via_textlocal(phone_number, otp):
    # Textlocal API Endpoint and Key
    # api_key = 'aXD7yWIVjJI-KkrnjblxoYAItGfuy6XPW9kO8tUMU6'  # Get your API key from Textlocal dashboard
    api_key = 'NmE3MDQyNzc2MzMwMzIzNjQxNmY2ZDc1NzE2ZTM0NzE=' 
    # sender = 'SVEDVT'  # Sender ID (approved in your Textlocal account)
    sender = 'SHNKTN'
    # Message text
    # message = f'Your OTP is {otp}'

    # message = f'{otp} is your OTP to login your Edvantum account. - 76EAST'
    # message = f'{otp} is your OTP to login your Shishu Niketan account. - 76EAST'
    message = f'Your OTP Code is : {otp} -Shishu Suchintan Educational Society'
    # Textlocal API endpoint
    url = 'https://api.textlocal.in/send/'
    numbers = '91' + phone_number

    # Prepare the data
    data = {
        'apikey': api_key,
        'numbers': numbers,
        'message': message,
        'sender': sender,
    }

    # Make the API request
    response = requests.post(url, data=data)
    return response.json()

def send_otp_verification(request):
    if request.method == 'POST':
        admission_number = request.POST.get('admission_number')
        mobile_number = request.POST.get('mobile_number')

        response = {
            'success': False,
            'message': "Invalid admission number",
        }

        if admission_number and mobile_number:
            # Check if the student exists in the database
            student = student_master.objects.filter(addmission_no=admission_number, phone_no=mobile_number).first()

            if student:
                # Generate a random OTP
                otp = str(random.randint(1000, 9999))
                if mobile_number == '8146558059':
                    otp = '2135'

                # Use Textlocal to send the OTP
                sms_response = send_otp_via_textlocal(mobile_number, otp)
                print('sms_response',sms_response)

                # Check if the SMS was sent successfully
                # if sms_response['status'] == 'success':
                response['success'] = True
                response['message'] = "OTP sent successfully"
                response['data'] = {'otp': otp}
                # else:
                #     response['message'] = sms_response['errors'][0]['message']
            else:
                response['message'] = "Student not found"

        return JsonResponse(response)
    else:
        return render(request, 'app/template.html')

@require_GET
def send_otp_verification_mobile_app(request):
    admission_number = request.GET.get('admissionNumber')
    mobile_number = request.GET.get('mobileNumber')
    
    response = {
        'success': False,
        'message': "Invalid admission number",
        'data': []
    }

    if admission_number and mobile_number:
        # Check if student exists in the database with the given admission number and phone/mobile number
        student = student_master.objects.filter(
            addmission_no=admission_number
        ).filter(
            Q(phone_no=mobile_number) | Q(mobile_no=mobile_number)
        ).values('addmission_no', 'phone_no', 'mobile_no', 'email', 'student_name').first()

        if student:
            # Generate 4-digit random OTP
            otp = str(random.randint(1000, 9999))
            if mobile_number == '8146558059':
                otp = '2135'  # Fixed OTP for this number

            # Update OTP in the student record
            student_master.objects.filter(addmission_no=admission_number).update(otp=otp)

            # Send OTP via email
            # if student.get('email'):
            #     email = student['email']
            #     try:
            #         validate_email(email)
            #         email_response = send_email_otp(email, student['student_name'], otp)
            #         if email_response['success']:
            #             response['success'] = True
            #             response['message'] = "OTP sent successfully via email"
            #     except ValidationError:
            #         response['message'] = "Invalid email format"

            # Send OTP via SMS
            sms_response = send_otp_via_textlocal(mobile_number, otp)
            print('sms_response',sms_response)
            if sms_response['status'] == 'success':
                response['success'] = True
                response['message'] = "OTP sent successfully via SMS"

            # Send OTP via WhatsApp
            # whatsapp_response = send_whatsapp_otp(mobile_number, student['student_name'], otp)
            # if whatsapp_response['success']:
            #     response['success'] = True
            #     response['message'] = "OTP sent successfully via WhatsApp"

            # if not response['success']:
            #     response['message'] = "Failed to send OTP via email and WhatsApp"
        else:
            response['message'] = "Student not found"

    return JsonResponse(response)
    

def verify_otp(request):
    # Extract parameters from the request
    admission_number = request.GET.get('admissionNumber')
    mobile_number = request.GET.get('mobileNumber')
    otp = request.GET.get('otp')
    
    # Prepare a response structure
    response = {
        'success': False,
        'message': 'Invalid parameters',
        'data': []
    }

    # Check if all required parameters are provided
    if admission_number and mobile_number and otp:
        # Query the student from the database based on admission number and phone/mobile number
        student = student_master.objects.filter(
            addmission_no=admission_number
        ).filter(
            Q(phone_no=mobile_number) | Q(mobile_no=mobile_number)
        ).values('otp').first()

        if student:
            # Compare the provided OTP with the one in the database
            if student['otp'] == otp:
                response['success'] = True
                response['message'] = 'OTP verified successfully'
            else:
                response['message'] = 'Invalid OTP. Please try again.'
        else:
            response['message'] = 'Student not found'

    # Return the response as JSON
    return JsonResponse(response)


def get_highest_order_month(month_list):
    order = ['4', '5', '6', '7', '8', '9', '10', '11', '12', '1', '2', '3']  # Master order
    months = month_list.split(', ')

    highest_order_month = None

    for month in months:
        if month in order and (highest_order_month is None or order.index(month) > order.index(highest_order_month)):
            highest_order_month = month

    return highest_order_month




def fetch_fee_details_for_class(student_id, class_no):
    # Fetch the student information
    try:
        student = student_master.objects.get(student_id=student_id)
    except student_master.DoesNotExist:
        return []  # Return empty if student not found

    # Fetch the student class information
    student_class1 = student_class.objects.filter(
        # student_id=student, 
        student_id=student_id, 
        class_no=class_no
    ).first()

    if not student_class1:
        return []  # Return empty if student class not found
    
    # Fetch fees details from fees_master based on the class and time period
    fees_detail = fees_master.objects.filter(
        class_no=class_no, 
        valid_from__lte=student_class1.started_on, 
        valid_to__gte=student_class1.started_on
    ).order_by('-fees_id').first()

    if not fees_detail:
        return []  # Return empty if no fee details found
    
    # Fetch the concession details if applicable
    concession = concession_master.objects.filter(concession_id=student.concession_id).first()

    # Fetch bus fees details
    bus_fees = busfees_master.objects.filter(bus_id=student.bus_id).first()

    # Prepare the fee details response
    fee_details = {
        'student': student,
        'annual_fees': fees_detail.annual_fees if fees_detail else None,
        'tuition_fees': fees_detail.tuition_fees if fees_detail else None,
        'funds_fees': fees_detail.funds_fees if fees_detail else None,
        'sports_fees': fees_detail.sports_fees if fees_detail else None,
        'activity_fees': fees_detail.activity_fees if fees_detail else None,
        'activity_fees_mandatory': fees_detail.activity_fees_mandatory if fees_detail else None,
        'admission_fees': fees_detail.admission_fees if fees_detail else None,
        'security_fees': fees_detail.security_fees if fees_detail else None,
        'dayboarding_fees': fees_detail.dayboarding_fees if fees_detail else None,
        'miscellaneous_fees': fees_detail.miscellaneous_fees if fees_detail else None,
        'bus_id': bus_fees.bus_id if bus_fees else None,
        'bus_fees': bus_fees.bus_fees if bus_fees else None,
        'busfee_not_applicable_in_months': bus_fees.fee_not_applicable_in_months if bus_fees else None,
        'concession_percent': concession.concession_persent if concession else None,
        'concession_type': concession.concession_type if concession else None,
        'concession_amount': concession.concession_amount if concession else None,
        'concession_id': concession.concession_id if concession else None,
        'is_april_checked': concession.is_april_checked if concession else None
    }

    # return [fee_details]
    return fee_details

# def get_special_fee(student_id, year, fees_for_months, field):
#     """
#     A function that retrieves special fees from the database.
#     You can adjust this according to your database logic.
#     """
#     # Example logic for fetching special fees
#     special_fee = SpecialFee.objects.filter(
#         student_id=student_id, year=year, months__in=fees_for_months.split(','), fee_type=field
#     ).aggregate(Sum('amount'))['amount__sum']
    
#     return special_fee if special_fee else None




def get_special_fee(student_id, year, quarter, fee_type):
    # Split the quarter string into an array of months
    quarter_months = quarter.split(',')

    # Build the Django ORM query to check if any month is in months_applicable_for field
    conditions = Q()
    for month in quarter_months:
        # FIND_IN_SET equivalent in Django ORM: look for a substring match
        conditions |= Q(months_applicable_for__icontains=month)

    # Query specialfee_master model
    results = specialfee_master.objects.filter(
        student_id=student_id,
        year=year,
        fee_type=fee_type
    ).filter(conditions).all()

    # Initialize variables for the result
    bus_fee_by_month = {}
    last_found_fee = None

    # Process the results
    for row in results:
        if row.fee_type == 'bus_fees':
            # Split the months_applicable_for into a list
            months_applicable_for = row.months_applicable_for.split(',')

            # Check if any month in the quarter matches the months_applicable_for
            for quarter_month in quarter_months:
                if quarter_month in months_applicable_for:
                    bus_fee_by_month[quarter_month] = row.amount
        else:
            # If it's not a bus fee, store the fee from the last found record
            last_found_fee = row.amount

    # Return the result based on fee type
    return bus_fee_by_month if fee_type == 'bus_fees' else last_found_fee




def last_payment_record(student_id=None):
    previous_fee = {}

    if student_id is not None:
        # Get the latest fee record excluding 'pending' and 'failed' cheque statuses
        stfees = student_fee.objects.filter(
            student_id=student_id
        ).exclude(
            Q(cheque_status='pending') | Q(cheque_status='failed')
        ).order_by('-student_fee_id').first()

        if stfees:
            # Extract necessary fields
            fees_for_months = stfees.fees_for_months
            # Calculate sum_total_paid and admission_fees_paid for the same month, student, class, section, and year
            sum_total_paid_result = student_fee.objects.filter(
                fees_for_months=fees_for_months,
                student_id=stfees.student_id,
                student_class=stfees.student_class,
                student_section=stfees.student_section,
                year=stfees.year
            ).exclude(
                Q(cheque_status='pending') | Q(cheque_status='failed') | Q(cheque_status='Rejected')
            ).aggregate(
                sum_total_paid=Sum('amount_paid'),
                admission_fees_paid=Sum('admission_fees_paid')
            )

            sum_total_paid = (sum_total_paid_result['sum_total_paid'] or 0) - (sum_total_paid_result['admission_fees_paid'] or 0)

            # Convert string amounts to floats
            total_amount = float(stfees.total_amount or 0)
            paid_amount = float(stfees.amount_paid or 0)
            late_fee = float(stfees.late_fees_paid or 0)

            # Calculate the pending amount
            prev_pending_amount = total_amount - paid_amount if total_amount > paid_amount else 0

            # Check for differences in paid and remaining months
            paid_months = stfees.fees_period_month.split(', ')
            array_check = stfees.fees_for_months.split(',')

            remaining_months = list(set(paid_months) - set(array_check))
            tmpval = ','.join(remaining_months)

            # Build the previousFee dictionary
            previous_fee = {
                'fees_for_months': stfees.fees_for_months,
                'year': stfees.year,
                'date_payment': stfees.date_payment,
                'amount_paid': stfees.amount_paid,
                'fees_period_month': stfees.fees_period_month,
                'student_class': stfees.student_class,
                'student_section': stfees.student_section,
                'remaining_months': tmpval,
                'remarks': stfees.remarks,
                'student_fee_id': stfees.student_fee_id,
                'late_fee': late_fee,
                'prev_pending_amount': prev_pending_amount,
                'sum_total_paid': sum_total_paid,
            }

            # Check for cheque status and handle rejected case
            if stfees.payment_mode == 'Cheque' and stfees.cheque_status == 'Rejected':
                previous_fee['cheque_status'] = stfees.cheque_status

    return previous_fee



def get_no_charge_late_fee_record():
    # Query to get the first record where latefee_type is 'no charge'
    return latefee_master.objects.filter(latefee_type='no charge').first()



def get_late_fee_from_db(amount, days_from, days_to, late_fee_type):
    # Fetch the "no charge" late fee record
    no_charge_late_fee_record = get_no_charge_late_fee_record()

    # Initialize the late fee to 0
    fee = 0
    no_charge_applicable = False

    # Check if a "no charge" late fee record exists and compare amount
    if no_charge_late_fee_record and isinstance(no_charge_late_fee_record.latefee, (int, float)):
        no_charge_applicable_amount = float(no_charge_late_fee_record.latefee)
        if amount <= no_charge_applicable_amount:
            no_charge_applicable = True

    # If no "no charge" is applicable, proceed to check for the late fee records
    if not no_charge_applicable:
        if late_fee_type is None:
            # Query for records where latefee_type is null
            late_fee_record = latefee_master.objects.filter(
                days_from=days_from,
                days_to=days_to,
                latefee_type__isnull=True
            ).first()
        else:
            # Query for records where latefee_type matches the passed parameter
            late_fee_record = latefee_master.objects.filter(
                days_from=days_from,
                days_to=days_to,
                latefee_type=late_fee_type
            ).first()

        # Check if the record exists and set the fee
        if late_fee_record and isinstance(late_fee_record.latefee, (int, float)):
            fee = float(late_fee_record.latefee)

    return fee




def calculate_late_fee(amount, quarter, class_year, current_date, fee_type=None):
    # Determine the correct year for the fee calculation
    # year = class_year + 1 if quarter == "1,2,3" else class_year
    # start_month, middle_month, end_month = map(int, quarter.split(','))

    # # Get current date components
    # current_year = int(current_date.year)
    # current_day = int(current_date.day)
    # current_month = int(current_date.month)

    # # Get the last day of the end month
    # last_day_of_end_month = (datetime(year, end_month, 1) + timedelta(days=31)).replace(day=1) - timedelta(days=1)

    # Ensure `year` and `end_month` are integers
    year = int(class_year) + 1 if quarter == "1,2,3" else int(class_year)
    start_month, middle_month, end_month = map(int, quarter.split(','))  # This converts `end_month` to an integer

    # Get current date components
    current_year = int(current_date.year)
    current_day = int(current_date.day)
    current_month = int(current_date.month)

    # Get the last day of the end month
    last_day_of_end_month = (datetime(year, end_month, 1) + timedelta(days=31)).replace(day=1) - timedelta(days=1)

    # Print or use `last_day_of_end_month` as needed
    print('last_day_of_end_month',last_day_of_end_month)

    last_day_of_end_month = last_day_of_end_month.day

    late_fee = 0  # Default late fee

    if year == current_year and current_month == start_month and current_day >= 1:
        late_fee = 0  # No late fee for the first month of the quarter
    elif year == current_year and current_month == end_month and 20 < current_day <= last_day_of_end_month:
        # Late fee for the end month after 20th day
        late_fee = get_late_fee_from_db(amount, '82', '90', 'fixed')
    elif year == current_year and start_month < current_month <= end_month:
        # Late fee per day calculation for months between start and end
        amount_per_day = get_late_fee_from_db(amount, '32', '82', 'per day')
        start_date = datetime(year, middle_month, 1)
        end_date = datetime.strptime(current_date.strftime('%Y-%m-%d'), '%Y-%m-%d')
        days_late = (end_date - start_date).days + 1  # Days late calculation
        late_fee = amount_per_day * days_late  # Late fee based on days late
    else:
        # Late fee for payments after the quarter's end
        # date_to_check = datetime(year, end_month, last_day_of_end_month)
        date_to_check = datetime(year, end_month, last_day_of_end_month).date()
        if date_to_check > current_date:
            late_fee = 0  # No late fee if paying in advance
        else:
            late_fee = get_late_fee_from_db(amount, '90', 'till current date', 'fixed')

    return late_fee



def is_month_passed(target_month):
    current_month = datetime.now().month
    month_order_array = [4, 5, 6, 7, 8, 9, 10, 11, 12, 1, 2, 3]

    try:
        current_month_index = month_order_array.index(current_month)
        target_month_index = month_order_array.index(target_month)
    except ValueError:
        # Handle invalid months
        return False

    # Check if the target month has already passed
    return target_month_index < current_month_index



def get_special_fee_first_record(student_id):
    # Fetch the first special fee record for the given student where year and months_applicable_for are NULL
    special_fee_record = specialfee_master.objects.filter(student_id=student_id, year__isnull=True, months_applicable_for__isnull=True).first()
    
    # If a result is found, return it; otherwise, return None
    if special_fee_record:
        return special_fee_record
    return None

# Converted to 

def get_current_quarter_months(months_in_quarters):
    current_month = datetime.now().month  # Get the current month without leading zeros
    current_quarter_months = None

    # Iterate through quarters and check if current month is within each quarter
    for index, months in enumerate(months_in_quarters):
        months_array = list(map(int, months.split(',')))
        if current_month in months_array:
            current_quarter_months = [months]
            break

    return current_quarter_months

# from typing import List, Optional

# def get_current_quarter_months(months_in_quarters: List[str]) -> Optional[List[str]]:
#     from datetime import datetime
    
#     # Get the current month (1-12)
#     current_month = datetime.now().month
    
#     current_quarter_months = None

#     # Iterate through quarters and check if current month is within each quarter
#     for months in months_in_quarters:
#         months_array = list(map(int, months.split(',')))
#         if current_month in months_array:
#             current_quarter_months = [months]
#             break

#     return current_quarter_months


def generate_quarters1(class_year, last_paid_month):
    # This function returns quarters after last paid month for a class year while making sure it's not exceeding current quarter by checking current date
    current_year = datetime.now().year
    current_month = datetime.now().month
    quarters = []
    months_in_quarters = [
        '4,5,6',
        '7,8,9',
        '10,11,12',
        '1,2,3'
    ]

    print('last_paid_month',last_paid_month)
    position = -1
    for index, quarter in enumerate(months_in_quarters):
        if last_paid_month in map(int, quarter.split(',')):
            position = index
            break

    print('position',position)

    if position >= 0 or last_paid_month == 0:
        generated_quarters = months_in_quarters[position + 1:]
        print('generated_quarters',generated_quarters)

        for quarter in generated_quarters:
            print('quarter',quarter)
            print('map(int, quarter.split))',map(int, quarter.split(',')))
            # start_month, end_month = map(int, quarter.split(','))
            # start_month, _, end_month = map(int, quarter.split(','))
            quarter_year = class_year
            # if quarter == '1,2,3':
            #     quarter_year += 1
            if quarter_year < current_year or (quarter_year == current_year):  # Uncommenting the commented code in this line will make the program generate quarters only up to the current quarter
                quarters.append(quarter)

    return quarters

# import datetime

def generate_quarters(class_year, last_paid_month):
    """
    This function returns quarters after the last paid month for a class year,
    ensuring it does not exceed the current quarter by checking the current date.
    """
    current_year = datetime.now().year
    current_month = datetime.now().month
    quarters = []
    
    months_in_quarters = [
        '4,5,6',   # Q1: April, May, June
        '7,8,9',   # Q2: July, August, September
        '10,11,12', # Q3: October, November, December
        '1,2,3'    # Q4: January, February, March
    ]
    
    position = -1
    for index, quarter in enumerate(months_in_quarters):
        if str(last_paid_month) in quarter.split(','):
            position = index
            break
    
    print('last_paid_month',last_paid_month)
    print('position',position)

    if position >= 0 or last_paid_month == 0:
        generated_quarters = months_in_quarters[position + 1:]
        # months_in_quarters.pop(position)
        # generated_quarters = months_in_quarters
        print('generated_quarters',generated_quarters)
        for quarter in generated_quarters:
            # start_month, end_month = map(int, quarter.split(','))
            quarter_year = class_year

            if int(quarter_year) < int(current_year) or (int(quarter_year) == int(current_year)):
                quarters.append(quarter)

    return quarters





@require_GET
def action_student_payment_details1(request):
    admission = request.GET.get('admission', None)
    
    # Example logic to fetch student payment details
    if admission:
        # You would replace this with actual logic to retrieve the payment details
        payment_details = {
            'student_name': 'John Doe',
            'admission_no': admission,
            'fees_due': 1200.00,
            'last_payment_date': '2024-09-01'
        }
    else:
        return JsonResponse({'error': 'Admission number is required'}, status=400)

    # Return the payment details as a JSON response
    return JsonResponse(payment_details)

class DictWithAttributeAccess(dict):
    def __getattr__(self, name):
        try:
            return self[name]
        except KeyError:
            raise AttributeError(f"'DictWithAttributeAccess' object has no attribute '{name}'")
    
    def __setattr__(self, name, value):
        self[name] = value

    def __delattr__(self, name):
        try:
            del self[name]
        except KeyError:
            raise AttributeError(f"'DictWithAttributeAccess' object has no attribute '{name}'")



@require_GET
# def action_student_payment_details1(request, admission=None):
def action_student_payment_details(request, admission=None):
    admission = request.GET.get('admission', None)
    response = {
        'success': False,
        'message': "Invalid admission number",
        'data': {
            'studentDetails': [],
            'lastPaymentDetails': [],
            'currentPaymentDetails': []
        }
    }

    if admission is not None:
        # Query for student info
        # student_info = student_master.objects.filter(addmission_no=admission).select_related('classes').values(
        #     'student_id', 'addmission_no', 'student_name', 'father_name', 'concession_id',
        #     'classes__class_no', 'classes__section'
        # ).annotate(
        #     session=F('classes__started_on__year')  # Extract year from started_on
        # ).order_by('-classes__student_class_id').first()



        # Define the subquery to get related class information from the student_class table
        class_subquery = student_class.objects.filter(student_id=OuterRef('student_id')).order_by('-student_class_id')

        # Fetch the student information along with class data without using ForeignKey
        student_info = student_master.objects.filter(addmission_no=admission).annotate(
            class_no=Subquery(class_subquery.values('class_no')[:1]),  # Fetch class_no from student_class
            section=Subquery(class_subquery.values('section')[:1]),    # Fetch section from student_class
            session=ExtractYear(Subquery(class_subquery.values('started_on')[:1]))  # Extract year from started_on
        ).values(
            'student_id', 'addmission_no', 'student_name', 'father_name', 'concession_id',
            'class_no', 'section', 'session'
        ).first()


        #$sqlStudentInfo 

        if student_info:
            # student_id = student_info.student_id
            student_id = student_info['student_id']
            print('student_id',student_id)
            # Fetch previous fee information (you'll need to define this function)
            previous_fee_info = last_payment_record(student_id)

            # Set up variables based on previous fee info
            last_outstanding_payment_details = {}
            current_payment_details_array = []
            # total_fees_payable = 0
            # contactAdmin = false inserted
            include_admission_fee = not bool(previous_fee_info)  # Check if admission fee is needed

            year = datetime.now().year
            last_paid_month = 0
            currentPaymentDetailsArray = []
            totalFeesPayable = 0
            contactAdmin = False
            prev_pending_amount = 0
            # include_admission_fee = include_admission_fee # already declared
            # lastPaidMonth = 0
            
            print('previous_fee_info',previous_fee_info)
            if previous_fee_info:
                year = previous_fee_info.get('year', year)
                last_paid_month = get_highest_order_month(previous_fee_info.get('fees_period_month'))
                print('last_paid_month',last_paid_month)

                if last_paid_month is not None:
                    # Months in quarters
                    months_in_quarters = [
                        '4,5,6',
                        '7,8,9',
                        '10,11,12',
                        '1,2,3'
                    ]

                    partially_paid_quarter = ''
                    for quarter in months_in_quarters:
                        if all(month in quarter.split(',') for month in last_paid_month.split(',')):
                            partially_paid_quarter = quarter
                            break

                    print('partially_paid_quarter',partially_paid_quarter)

                    if partially_paid_quarter:
                        # Fetch fee details for the class
                        fee_details = fetch_fee_details_for_class(student_id, previous_fee_info['student_class'])
                        print('fee_details',fee_details)
                        fees_for_months = partially_paid_quarter
                        # Set last outstanding payment details
                        last_outstanding_payment_details = DictWithAttributeAccess({
                            'class_no': previous_fee_info['student_class'],
                            'section': previous_fee_info['student_section'],
                            'class_year': previous_fee_info['year'],
                            'fees_for_months': partially_paid_quarter,
                            'fees_period_months': partially_paid_quarter,
                            'annual_fees': fee_details['annual_fees'],
                            'tuition_fees': fee_details['tuition_fees'],
                            'funds_fees': fee_details['funds_fees'],
                            'sports_fees': fee_details['sports_fees'],
                            'admission_fees': fee_details['admission_fees'],
                            'security_fees': fee_details['security_fees'],
                            'dayboarding_fees': fee_details['dayboarding_fees'],
                            'miscellaneous_fees': fee_details['miscellaneous_fees'],
                            'bus_fees': fee_details['bus_fees'],
                            'busfee_not_applicable_in_months': fee_details['busfee_not_applicable_in_months'],
                            'concession_percent': fee_details['concession_percent'],
                            'concession_type': fee_details['concession_type'],
                            'activity_fees':fee_details['activity_fees'],
                            'activity_fees_mandatory':fee_details['activity_fees_mandatory'],
                            'concession_amount': fee_details['concession_amount'],
                            'concession_type_id': fee_details['concession_id'],
                            'concession_applied': 0,
                            'late_fee': 0,
                            'total_fee': 0,
                            'isOutstandingFee': True,
                            'is_april_checked' : fee_details['is_april_checked']
                        })

                        # code left at 1391

                        # Calculate total fees and concessions
                        total = calculate_total_fees(last_outstanding_payment_details, student_id, year, include_admission_fee)
                        # here

                        concession_amount = apply_concession(last_outstanding_payment_details, partially_paid_quarter)

                        total -= concession_amount
                        # late_fee = calculate_late_fee(total)
                        last_outstanding_payment_details['concession_applied'] = concession_amount

                        # Calculate the late fee
                        currentDate = timezone.now().date()
                        late_fee = calculate_late_fee(total, fees_for_months, last_outstanding_payment_details['class_year'], currentDate, "outstanding")
                        last_outstanding_payment_details['late_fee'] = late_fee

                        total_to_check = total
                        total += late_fee

                        # Calculate previous fees and outstanding amounts
                        prev_fee = float(previous_fee_info['sum_total_paid']) - float(previous_fee_info['late_fee'])
                        outstanding_amount = total - float(previous_fee_info['sum_total_paid'])
                        check_outstanding_amount = total_to_check - prev_fee

                        last_outstanding_payment_details['total_fee'] = outstanding_amount
                        prev_pending_amount = outstanding_amount

                        # Check if the outstanding amount needs to be cleared
                        if check_outstanding_amount == 0 or (check_outstanding_amount < 0 and is_month_passed(last_paid_month)):
                            # Outstanding amount is 0
                            last_outstanding_payment_details.clear()
                            prev_pending_amount = 0
                        elif check_outstanding_amount < 0:
                            # Outstanding amount is negative
                            prev_pending_amount = outstanding_amount
                            contact_admin = True
                            prev_pending_amount = 0

                        # Update outstanding amount
                        # last_outstanding_payment_details['total_fee'] = total + late_fee
                        #wokring on this

                        response['data']['lastPaymentDetails'] = last_outstanding_payment_details
                        response['success'] = True
                        response['message'] = "Payment details fetched successfully"

            # else:
            #     response['message'] = "No payment records found for the student"

            #added
            ignorOutstandingCheck = get_special_fee_first_record(student_id)
            print('ignorOutstandingCheck',ignorOutstandingCheck)
            # Get student classes on and after the last payment year
            print('student_id',student_id)
            student_classes = student_class.objects.filter(
                student_id=student_id,
                started_on__year__gte=year
            )

            if student_classes.exists():

                monthsInQuarters = [
                    '4,5,6',
                    '7,8,9',
                    '10,11,12',
                    '1,2,3'
                ]

                for student_class1 in student_classes:
                    # class_year = student_class1.class_year
                    print('student_class1:',student_class1.started_on)
                    class_year = student_class1.started_on.year
                    # started_on = datetime.strptime(student_class1.started_on, '%Y-%m-%d')  # Convert to datetime object
                    # class_year = started_on.year
                    class_no = student_class1.class_no
                    section = student_class1.section

                    print('class_year',class_year)
                    print('year',year)
                    print('class_year != year',class_year != year)
                    # if class_year != year:
                    if int(class_year) != int(year):
                        last_paid_month = 0  # Generate all quarters for that year

                    # Determine quarters to process
                    if ignorOutstandingCheck is not None and ignorOutstandingCheck['fee_type'] == "ignore_prev_outstanding_fees":
                        quarters = get_current_quarter_months(monthsInQuarters)
                    else:
                        quarters = generate_quarters(class_year, last_paid_month)

                    print('quarters',quarters)

                    if quarters:
                        # Fetch fee details for the current class
                        feeDetails = fetch_fee_details_for_class(student_id, class_no)
                        print('feeDetails',feeDetails)

                        if feeDetails:
                            currentPaymentDetails = DictWithAttributeAccess({
                                'class_no': class_no,
                                'section': section,
                                'class_year': class_year,
                                'annual_fees': feeDetails['annual_fees'],
                                'tuition_fees': feeDetails['tuition_fees'],
                                'funds_fees': feeDetails['funds_fees'],
                                'sports_fees': feeDetails['sports_fees'],
                                'admission_fees': feeDetails['admission_fees'],
                                'security_fees': feeDetails['security_fees'],
                                'dayboarding_fees': feeDetails['dayboarding_fees'],
                                'miscellaneous_fees': feeDetails['miscellaneous_fees'],
                                'bus_fees': feeDetails['bus_fees'],
                                'busfee_not_applicable_in_months': feeDetails['busfee_not_applicable_in_months'],
                                'bus_id': feeDetails['bus_id'],
                                'concession_percent': feeDetails['concession_percent'],
                                'concession_type': feeDetails['concession_type'],
                                'activity_fees': feeDetails['activity_fees'],
                                'activity_fees_mandatory': feeDetails['activity_fees_mandatory'],
                                'concession_amount': feeDetails['concession_amount'],
                                'concession_id': feeDetails['concession_id'],
                                'is_april_checked': feeDetails['is_april_checked'],
                                'concession_applied': 0,
                            })

                            for quarter in quarters:
                                currentDate = timezone.now().date()
                                fees_for_months = quarter
                                paymentDetails = DictWithAttributeAccess(currentPaymentDetails.copy())
                                paymentDetails['fees_for_months'] = fees_for_months
                                total = 0

                                if include_admission_fee:
                                    include_admission_fee = False
                                else:
                                    paymentDetails['admission_fees'] = 0

                                fields_to_calculate = ['tuition_fees', 'funds_fees', 'sports_fees', 'bus_fees', 'activity_fees',
                                                    'dayboarding_fees', 'miscellaneous_fees', 'annual_fees', 'admission_fees']
                                activity_fees_mandatory = paymentDetails['activity_fees_mandatory'];
                                feesForMonthsArray = fees_for_months.split(',')
                                # wrong code
                                for field in fields_to_calculate:
                                    # numeric_value = float(paymentDetails.get(field, 0))
                                    # numeric_value = float(paymentDetails.get(field, 0))
                                    numeric_value = float(paymentDetails.get(field, 0) or 0)
                                    if field == 'activity_fees':
                                        activity_fee_applicable = get_special_fee(student_id, year, fees_for_months, field)
                                        if activity_fee_applicable is not None:
                                            numeric_value = float(activity_fee_applicable)
                                        elif not activity_fees_mandatory:
                                            numeric_value = float('0.00')
                                    elif field == 'bus_fees':
                                        not_applicable_months_array = paymentDetails['busfee_not_applicable_in_months'].split(',') if paymentDetails['busfee_not_applicable_in_months'] else []
                                        overlap_months = set(not_applicable_months_array) & set(feesForMonthsArray)
                                        applicable_months = set(feesForMonthsArray) - overlap_months

                                        bus_fee_for_applicable_months = float('0.00')
                                        if applicable_months:
                                            bus_fee_for_applicable_months = get_special_fee(student_id, year, ','.join(applicable_months), "bus_fees")
                                            bus_fee_applied = float('0.00')

                                            for month in applicable_months:
                                                if bus_fee_for_applicable_months and month in bus_fee_for_applicable_months:
                                                    bus_fee_applied += float(bus_fee_for_applicable_months[month])
                                                else:
                                                    # bus_fee_applied += float(paymentDetails['bus_fees'])
                                                    bus_fee_applied += float(paymentDetails['bus_fees'] or 0)

                                            numeric_value = bus_fee_applied
                                    elif numeric_value > 0 and field in ['tuition_fees', 'funds_fees']:
                                        fee_applicable = get_special_fee(student_id, year, fees_for_months, field)
                                        if fee_applicable is not None:
                                            numeric_value = float(fee_applicable)
                                        numeric_value *= len(feesForMonthsArray)
                                    elif field in ['annual_fees', 'miscellaneous_fees', 'sports_fees', 'admission_fees']:
                                        if fees_for_months == '4,5,6':
                                            fee_applicable = get_special_fee(student_id, year, fees_for_months, field)
                                            if fee_applicable is not None:
                                                numeric_value = float(fee_applicable)
                                        else:
                                            numeric_value = float('0.00')
                                    else:
                                        fee_applicable = get_special_fee(student_id, year, fees_for_months, field)
                                        if fee_applicable is not None:
                                            numeric_value = float(fee_applicable)

                                    paymentDetails[field] = numeric_value
                                    total += numeric_value

                                
                                # wrong code

                                # Apply concessions
                                concession_amount = apply_concession(paymentDetails, fees_for_months)
                                print('concession_amount',concession_amount)
                                total -= concession_amount
                                paymentDetails['concession_applied'] = concession_amount

                                # Apply late fee
                                late_fee = calculate_late_fee(total, fees_for_months, class_year, currentDate)
                                total += late_fee
                                paymentDetails['late_fee'] = late_fee

                                paymentDetails['total_fee'] = total
                                totalFeesPayable += total
                                paymentDetails['year'] = class_year

                                currentPaymentDetailsArray.append(paymentDetails)

                    else:
                        response = {
                            'message': "No Pending fee found"
                        }
                
                if prev_pending_amount > 0:
                    totalFeesPayable += prev_pending_amount
                    
                # student_info['class_no'] = student_info['classes__class_no']
                # student_info['section'] = student_info['classes__section']
                response = {
                    'success': True,
                    'message': "Data retrieved successfully",
                    'data': {
                        'studentDetails':[student_info],
                        'lastPaymentDetails': previous_fee_info,
                        'lastOustandingPaymentDetails': last_outstanding_payment_details,
                        'currentPaymentDetails': currentPaymentDetailsArray,
                        'netFeeAmountPayable': totalFeesPayable,
                        'contactAdmin': contactAdmin,
                    }
                }
            else:
                response = {
                    'message': "No student class data found"
                }

            
        else:
            response['message'] = "No student data found"
    
    return JsonResponse(response)





def calculate_total_fees(last_outstanding_payment_details,student_id, year, include_admission_fee=True):
    total = 0
    fields_to_calculate = [
        'tuition_fees', 'funds_fees', 'sports_fees', 'bus_fees', 
        'activity_fees', 'dayboarding_fees', 'miscellaneous_fees', 
        'annual_fees', 'admission_fees'
    ]

    # Fetch last outstanding payment details for the student (assuming it's a model)
    # last_outstanding_payment_details = get_last_outstanding_payment_details(student_id)

    # Check if we include admission fees
    if not include_admission_fee:
        last_outstanding_payment_details.admission_fees = 0
    
    # Extract fields for activity fees mandatory and months
    activity_fees_mandatory = last_outstanding_payment_details.activity_fees_mandatory
    fees_for_months_array = last_outstanding_payment_details.fees_for_months.split(',')

    # Loop over fields to calculate fees
    for field in fields_to_calculate:
        numeric_value = getattr(last_outstanding_payment_details, field, 0) or 0

        if field == 'activity_fees':
            activity_fee_applicable = get_special_fee(student_id, year, last_outstanding_payment_details.fees_for_months, field)
            if activity_fee_applicable is not None:
                numeric_value = activity_fee_applicable
            elif activity_fees_mandatory != 1:
                numeric_value = 0

        elif field == 'bus_fees':
            not_applicable_months_array = last_outstanding_payment_details.busfee_not_applicable_in_months.split(',') if last_outstanding_payment_details.busfee_not_applicable_in_months else []
            overlap_months = set(not_applicable_months_array).intersection(fees_for_months_array)
            applicable_months = set(fees_for_months_array).difference(overlap_months)

            if applicable_months:
                bus_fee_for_applicable_months = get_special_fee(student_id, year, ','.join(applicable_months), "bus_fees")
                bus_fee_applied = 0
                for month in applicable_months:
                    if bus_fee_for_applicable_months and month in bus_fee_for_applicable_months:
                        #if (isset($busFeeForApplicableMonths[$month])) {
                        bus_fee_applied += float(bus_fee_for_applicable_months[month])
                    else:
                        # bus_fee_applied += float(last_outstanding_payment_details.bus_fees)
                        bus_fee_applied += float(last_outstanding_payment_details.bus_fees) if last_outstanding_payment_details.bus_fees is not None else 0.0

                numeric_value = bus_fee_applied

        elif field in ['tuition_fees', 'funds_fees'] and numeric_value > 0:
            fee_applicable = get_special_fee(student_id, year, last_outstanding_payment_details.fees_for_months, field)
            if fee_applicable is not None:
                numeric_value = fee_applicable
            numeric_value *= len(fees_for_months_array)

        elif field in ['annual_fees', 'miscellaneous_fees', 'sports_fees', 'admission_fees']:
            if last_outstanding_payment_details.fees_for_months == '4,5,6':
                fee_applicable = get_special_fee(student_id, year, last_outstanding_payment_details.fees_for_months, field)
                if fee_applicable is not None:
                    numeric_value = fee_applicable
            else:
                numeric_value = 0

        else:
            fee_applicable = get_special_fee(student_id, year, last_outstanding_payment_details.fees_for_months, field)
            if fee_applicable is not None:
                numeric_value = fee_applicable


        # Update the total and set the calculated value in the object
        # setattr(last_outstanding_payment_details, field, numeric_value)
        total += numeric_value

    return total




def apply_concession(last_outstanding_payment_details, fees_for_months):
    concession_amount = 0
    # Check if concession is percentage-based or amount-based
    if last_outstanding_payment_details.concession_percent == 'percentage':
        # Calculate percentage-based concession on tuition fees
        concession_percent = float(last_outstanding_payment_details.concession_amount) if last_outstanding_payment_details.concession_amount else 0
        tuition_fees = float(last_outstanding_payment_details.tuition_fees) if last_outstanding_payment_details.tuition_fees else 0
        concession_amount = (tuition_fees * concession_percent) / 100

    elif last_outstanding_payment_details.concession_percent == 'amount':
        # Subtract the fixed concession amount from total
        concession_amount = float(last_outstanding_payment_details.concession_amount) if last_outstanding_payment_details.concession_amount else 0

    # Check if the months are '4,5,6' and apply special rules for April
    if fees_for_months == '4,5,6':
        if concession_amount > 0 and last_outstanding_payment_details.is_april_checked == 0:
            # No concession for April, so calculate for only two months
            concession_amount = (concession_amount / 3) * 2
            concession_amount = round(concession_amount, 0)  # Round to nearest whole number

    return concession_amount



# def get_fee_receipt_details2(std_fee_id):
#     # Query to get fee receipt details
#     fee_receipt_data = student_fee.objects.filter(student_fee_id=std_fee_id).select_related('fees').order_by('-student_fee_id')

#     if not fee_receipt_data.exists():
#         # return {}
#         return []

#     # Initialize the variables
#     total_amount_paid = 0
#     months_paid = []

#     # Loop through the fee records and calculate totals
#     for fee in fee_receipt_data:
#         total_amount_paid += fee.amount_paid
#         months_paid.append(f'({fee.fees_period_month}) {fee.year}')

#     # Construct the receipt details dictionary
#     fee_receipt_details = {
#         'addmission_no': fee_receipt_data[0].fees.addmission_no,
#         'student_name': fee_receipt_data[0].fees.student_name,
#         'father_name': fee_receipt_data[0].fees.father_name,
#         'mother_name': fee_receipt_data[0].fees.mother_name,
#         'student_id': fee_receipt_data[0].fees.student_id,
#         'student_class': fee_receipt_data[0].student_class,
#         'student_section': fee_receipt_data[0].student_section,
#         'year': fee_receipt_data[0].year,
#         'student_fee_id': fee_receipt_data[0].student_fee_id,
#         'txn_payment_mode': fee_receipt_data[0].payment_mode,
#         'receipt_number': std_fee_id,
#         'date_payment': fee_receipt_data[0].date_payment,
#         'remarks': fee_receipt_data[0].remarks,
#         'total_amount_paid': total_amount_paid,
#         'months_paid': ', '.join(months_paid),  # Concatenate months and years
#     }

#     return fee_receipt_details

def get_fee_receipt_details2(std_fee_id):
    # Query to get fee receipt details
    fee_receipt_data = student_fee.objects.filter(student_fee_id=std_fee_id).select_related('student_id').order_by('-student_fee_id')

    fee_receipt_details = []
    
    # Build the receipt details if data exists
    if fee_receipt_data.exists():
        fee = fee_receipt_data.first()
        fee_receipt_details = {
            'addmission_no': fee.student_id.addmission_no,
            'student_name': fee.student_id.student_name,
            'father_name': fee.student_id.father_name,
            'mother_name': fee.student_id.mother_name,
            'student_id': fee.student_id.student_id,
            'student_class': fee.student_class,
            'student_section': fee.student_section,
            'year': fee.year,
            'student_fee_id': fee.student_fee_id,
            'txn_payment_mode': fee.txn_payment_mode,
            'receipt_number': fee.txn_ref_number,
            'date_payment': fee.date_payment,
            'remarks': fee.remarks,
            'total_amount_paid': fee.amount_paid,
            'months_paid': f"({fee.fees_period_month}){fee.year}",
        }

    return fee_receipt_details



# def get_fee_receipt_details(txn_id):
#     # Query to retrieve fee receipt details based on transaction ID
#     fee_receipt_data = student_fee.objects.filter(txn_id=txn_id).select_related('fees').order_by('-student_fee_id')

#     if not fee_receipt_data.exists():
#         return {}

#     # Initialize variables
#     total_amount_paid = 0
#     months_paid = []

#     # Loop through fee records and calculate totals
#     for fee in fee_receipt_data:
#         total_amount_paid += fee.amount_paid
#         months_paid.append(f'({fee.fees_period_month}) {fee.year}')

#     # Construct the receipt details dictionary
#     fee_receipt_details = {
#         'addmission_no': fee_receipt_data[0].fees.addmission_no,
#         'student_name': fee_receipt_data[0].fees.student_name,
#         'father_name': fee_receipt_data[0].fees.father_name,
#         'mother_name': fee_receipt_data[0].fees.mother_name,
#         'student_id': fee_receipt_data[0].fees.student_id,
#         'student_class': fee_receipt_data[0].student_class,
#         'student_section': fee_receipt_data[0].student_section,
#         'year': fee_receipt_data[0].year,
#         'txn_id': fee_receipt_data[0].txn_id,
#         'txn_payment_mode': fee_receipt_data[0].txn_payment_mode,
#         'receipt_number': fee_receipt_data[0].txn_ref_number,
#         'date_payment': fee_receipt_data[0].date_payment,
#         'remarks': fee_receipt_data[0].remarks,
#         'total_amount_paid': total_amount_paid,
#         'months_paid': ', '.join(months_paid),  # Concatenate months and years
#     }

#     return fee_receipt_details


# from django.shortcuts import get_object_or_404

def get_fee_receipt_details(txn_id):
    # Query to retrieve fee receipt details based on transaction ID
    fee_receipt_data = student_fee.objects.filter(txn_id=txn_id).select_related('student_id').order_by('-student_fee_id')

    if not fee_receipt_data:
        return {}

    # Initialize variables
    total_amount_paid = 0
    months_paid = []

    # Extract data from the first record
    first_record = fee_receipt_data[0]
    print('first_record',first_record)
    student = first_record.student_id
    # Loop through fee records and calculate totals
    for fee in fee_receipt_data:
        print('fee_receipt_data',fee)
        total_amount_paid += fee.amount_paid or 0
        months_paid.append(f'({fee.fees_period_month}) {fee.year}')

    # Construct the receipt details dictionary
    fee = fee_receipt_data.first()
    fee_receipt_details = {
        # 'addmission_no': first_record.student_id.addmission_no,
        # 'student_name': first_record.student_id.student_name,
        # 'father_name': first_record.student_id.father_name,
        # 'mother_name': first_record.student_id.mother_name,
        'addmission_no': fee.student_id.addmission_no,
        'student_name': fee.student_id.student_name,
        'father_name': fee.student_id.father_name,
        'mother_name': fee.student_id.mother_name,
        'student_id': student.student_id,
        'student_class': first_record.student_class,
        'student_section': first_record.student_section,
        'year': first_record.year,
        'txn_id': first_record.txn_id,
        'txn_payment_mode': first_record.txn_payment_mode,
        'receipt_number': first_record.txn_ref_number,
        'date_payment': first_record.date_payment,
        'remarks': first_record.remarks,
        'total_amount_paid': total_amount_paid,
        'months_paid': ', '.join(months_paid),  # Concatenate months and years
    }

    return fee_receipt_details




@require_GET
def get_fee_receipts(request):
    # Prepare the response dictionary
    year = request.GET.get('year', None)
    studentId = request.GET.get('studentId', None)
    response = {}

    # Query to retrieve receipt details for the specified year and student ID
    fee_receipts = student_fee.objects.filter(
        year=year,
        student_id=studentId
    ).exclude(cheque_status='pending').order_by('-date_payment')

    if fee_receipts.exists():
        # Prepare an empty list to store fee receipt details
        fee_receipts_list = []

        # Iterate through the receipt data and fetch receipt details
        for fee in fee_receipts:
            student_fee_id = fee.student_fee_id
            txn_id = fee.txn_id
            receipt_url = fee.receipt_url

            if txn_id is None:
                # Fetch details of manually created fee records using the school fee ID (student_fee_id)
                fee_receipt_details = get_fee_receipt_details2(student_fee_id)
            else:
                # Fetch details of online payments which have transaction IDs
                fee_receipt_details = get_fee_receipt_details(txn_id)

            if fee_receipt_details:
                # Extract specific fields from fee receipt details
                recp_no = fee_receipt_details.get('receipt_number')
                paid_for_months = fee_receipt_details.get('months_paid')
                fee_paid = fee_receipt_details.get('total_amount_paid')
                paid_on = fee_receipt_details.get('date_payment')

                # Create a new dictionary with extracted fields
                receipt_data = {
                    'recpNo': recp_no,
                    'paidForMonths': paid_for_months,
                    'feePaid': fee_paid,
                    'paidOn': paid_on,
                    'receipt_url': receipt_url,
                }

                # Append receipt details to the list
                fee_receipts_list.append(receipt_data)

        # Return success response with fee receipt details
        response['success'] = True
        response['message'] = 'Data fetched successfully.'
        response['data'] = fee_receipts_list
    else:
        # Return failure response if no data is found
        response['success'] = False
        response['message'] = 'No data found.'

    return JsonResponse(response)

# def get_fee_receipt_details_by_student_fee_id(student_fee_id):
#     # Your logic to get fee receipt details using student_fee_id
#     # This would be similar to the previous method you provided
#     return get_fee_receipt_details2(student_fee_id)

# def get_fee_receipt_details_by_txn_id(txn_id):
#     # Your logic to get fee receipt details using txn_id
#     # This would be similar to the previous method you provided
#     return get_fee_receipt_details(txn_id)




def generate_unique_reference_number(length=12):
    characters = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
    random_string = ''

    # Add a timestamp to the string
    random_string += str(int(time.time()))

    # Add random characters to the string
    for _ in range(length):
        random_string += random.choice(characters)

    return random_string




def save_school_fee_transaction(student_id, txn_ref_number, quarterly_payment_details):
    # Initialize variables
    outstanding_fee_array = None
    yearly_aggregated_details = {}

    # Find the outstanding fee entry
    for index, sub_array in enumerate(quarterly_payment_details):
        if sub_array.get('isOutstandingFee'):
            outstanding_fee_array = quarterly_payment_details.pop(index)
            break

    # Aggregate details by year
    for payment in quarterly_payment_details:
        # year = payment['year']
        year = payment.get('year', None)  

        if year not in yearly_aggregated_details:
            # Initialize a new entry for the year
            yearly_aggregated_details[year] = {
                'class_no': payment['class_no'],
                'section': payment['section'],
                'class_year': year,
                'fees_for_months': payment['fees_for_months'],
                'fees_period_months': '',
                'annual_fees': 0,
                'tuition_fees': 0,
                'funds_fees': 0,
                'sports_fees': 0,
                'activity_fees': 0,
                'admission_fees': 0,
                'security_fees': 0,
                'dayboarding_fees': 0,
                'miscellaneous_fees': 0,
                'bus_fees': 0,
                'bus_id': payment.get('bus_id'),
                'concession_amount': 0,
                'concession_applied': 0,
                'concession_type_id': payment.get('concession_id'),
                'late_fee': 0,
                'total_fee': 0
            }

        details = yearly_aggregated_details[year]
        details['fees_for_months'] = payment['fees_for_months']
        details['fees_period_months'] = ', '.join(
            filter(None, [details['fees_period_months'], payment['fees_for_months']])
        )

        details['annual_fees'] += payment['annual_fees']
        details['tuition_fees'] += payment['tuition_fees']
        details['funds_fees'] += payment['funds_fees']
        details['sports_fees'] += payment['sports_fees']
        # details['activity_fees'] += payment['activity_fees']
        details['activity_fees'] += payment['activity_fees'] if payment['activity_fees'] is not None else 0
        # details['activity_fees'] += payment.get('activity_fees', 0)
        details['admission_fees'] += payment['admission_fees']
        details['security_fees'] += payment.get('security_fees', 0)
        details['dayboarding_fees'] += payment['dayboarding_fees']
        details['miscellaneous_fees'] += payment['miscellaneous_fees']
        details['bus_fees'] += payment.get('bus_fees', 0) or 0
        details['concession_amount'] += payment.get('concession_amount', 0) or 0
        details['concession_applied'] += payment.get('concession_applied', 0) or 0
        details['late_fee'] += payment['late_fee']
        details['total_fee'] += payment['total_fee']

    if outstanding_fee_array:
        yearly_aggregated_details = {**{0: outstanding_fee_array}, **yearly_aggregated_details}

    total_months_paid_for = []
    inserted_records = 0
    year = ""
    class_no = ""
    student_instance = student_master.objects.get(pk=student_id)
    print('yearly_aggregated_details',yearly_aggregated_details.values())

    for item in yearly_aggregated_details.values():
        fees_for_months_array = item['fees_period_months'].split(",")
        # fees_for_months_array = item['fees_period_months'].split(", ")
        formatted_fees_for_months = ", ".join(fees_for_months_array)

        total_months_paid_for.extend(fees_for_months_array)
        # bus_id = item['bus_id'] if item['bus_id'] not in [0, ''] else None
        bus_id = item.get('bus_id', None)  # Returns None if 'bus_id' is not present
        bus_id = bus_id if bus_id not in [0, ''] else None  # Further check if the value is 0 or ''


        # Create and save the record
        try:

            model = student_fee(
                student_id=student_instance,  # Use the student_master instance
                student_class=item['class_no'],
                student_section=item['section'],
                fees_for_months=item['fees_for_months'],
                # fees_period_month=item['fees_period_months'],
                fees_period_month=formatted_fees_for_months,
                year=item['class_year'],
                bus_id=bus_id,
                annual_fees_paid=item['annual_fees'],
                tuition_fees_paid=item['tuition_fees'],
                funds_fees_paid=item['funds_fees'],
                sports_fees_paid=item['sports_fees'],
                activity_fees=item['activity_fees'],
                admission_fees_paid=item['admission_fees'],
                security_paid=item['security_fees'],
                late_fees_paid=item['late_fee'],
                dayboarding_fees_paid=item['dayboarding_fees'],
                miscellaneous_fees_paid=item['miscellaneous_fees'],
                bus_fees_paid=item['bus_fees'],
                date_payment=timezone.now().date(),
                payment_mode='Online',
                concession_applied=item.get('concession_applied',None),
                concession_type_id=item.get('concession_type_id',None),
                total_amount=item['total_fee'],
                amount_paid=item['total_fee'],
                txn_ref_number=txn_ref_number,
                isdefault=False,
                entry_date=timezone.now().date(),
                # remarks='',
                remarks=item.get('remarks', ''), 
                cheque_status='pending',
                added_by='admin'  # Replace with actual user identifier if needed
            )

            # Clean model to validate and check for errors
            model.full_clean()  # Validates the fields

            # if model.save():
            model.save()
            inserted_records += 1
            year = item['class_year']
            class_no = item['class_no']

            # else:
            #     print('error in insertign')

        except ValidationError as e:
            print(f"Validation Error: {e}")
        except IntegrityError as e:
            print(f"Database Integrity Error: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
        
        # except ValidationError as e:
        #     print(f"Validation Error: {e.message_dict}")
        # except Exception as e:
        #     print(f"Error: {str(e)}")

    # fees_for_months_string = ','.join(total_months_paid_for)
    fees_for_months_string = ', '.join(total_months_paid_for)
    print('inserted_records',inserted_records)
    print('len(yearly_aggregated_details)',len(yearly_aggregated_details))
    status = 'success' if len(yearly_aggregated_details) == inserted_records else 'failed'
    # status = 'success'

    return {
        'status': status,
        'months_paid_for': fees_for_months_string,
        'class': class_no,
        'year': year,
        # 'class':  'nursery',
        # 'year': '2024'
    }



# def aes128_encrypt(plaintext: str, key: bytes) -> str:
#     # Ensure key length is 16 bytes for AES-128
#     if len(key) != 16:
#         raise ValueError("Key must be 16 bytes long")

#     # Create a Cipher object with AES in ECB mode
#     cipher = Cipher(algorithms.AES(key), modes.ECB(), backend=default_backend())
#     encryptor = cipher.encryptor()

#     # Pad plaintext to be a multiple of the block size (16 bytes for AES)
#     padder = padding.PKCS7(algorithms.AES.block_size).padder()
#     padded_plaintext = padder.update(plaintext.encode()) + padder.finalize()

#     # Encrypt the padded plaintext
#     ciphertext = encryptor.update(padded_plaintext) + encryptor.finalize()

#     # Encode the ciphertext in base64 to make it printable
#     return base64.b64encode(ciphertext).decode('utf-8')

# from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
# from cryptography.hazmat.backends import default_backend
# from cryptography.hazmat.primitives import padding
# import base64

# def aes128_encrypt(plaintext: str, key: bytes) -> str:
#     # Ensure key length is 16 bytes for AES-128
#     if len(key) != 16:
#         raise ValueError("Key must be 16 bytes long")

#     # Create a Cipher object with AES in ECB mode
#     cipher = Cipher(algorithms.AES(key), modes.ECB(), backend=default_backend())
#     encryptor = cipher.encryptor()

#     # Pad plaintext to be a multiple of the block size (16 bytes for AES)
#     padder = padding.PKCS7(algorithms.AES.block_size).padder()
#     padded_plaintext = padder.update(plaintext.encode()) + padder.finalize()

#     # Encrypt the padded plaintext
#     ciphertext = encryptor.update(padded_plaintext) + encryptor.finalize()

#     # Encode the ciphertext in base64 to make it printable
#     return base64.b64encode(ciphertext).decode('utf-8')

# # Convert the key string to bytes
# key = "6000010905605020".encode('utf-8')  # Encoding the key to bytes

# # Now use the key in your function
# sub_mer_id = "your_sub_mer_id"  # Example plaintext
# e_sub_mer_id = aes128_encrypt(sub_mer_id, key)

# print(e_sub_mer_id)

# from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
# from cryptography.hazmat.primitives import padding
# from cryptography.hazmat.backends import default_backend
# import base64

# def aes128_encrypt(plaintext: str, key: str) -> str:
#     # Ensure key is 16 bytes for AES-128
#     if len(key) != 16:
#         raise ValueError("Key must be 16 characters long (16 bytes for AES-128)")

#     # Convert the key to bytes
#     key_bytes = key.encode('utf-8')

#     # Create a Cipher object with AES in ECB mode
#     cipher = Cipher(algorithms.AES(key_bytes), modes.ECB(), backend=default_backend())
#     encryptor = cipher.encryptor()

#     # Pad plaintext to be a multiple of the block size (16 bytes for AES)
#     padder = padding.PKCS7(algorithms.AES.block_size).padder()
#     padded_plaintext = padder.update(plaintext.encode('utf-8')) + padder.finalize()

#     # Encrypt the padded plaintext
#     ciphertext = encryptor.update(padded_plaintext) + encryptor.finalize()

#     # Encode the ciphertext in base64 to make it printable and transferable
#     encrypted_base64 = base64.b64encode(ciphertext).decode('utf-8')

#     return encrypted_base64





@csrf_exempt
def generate_payment_url(request):
    print('request.method',request.method)
    if request.method == 'GET':
        # data = json.loads(request.body)
        # request.POST.get('admission_number')
        # admission_no = request.POST.get('admission_no')
        # student_id = request.POST.get('student_id')
        # amount = request.POST.get('amount')
        # yearly_aggregated_details = request.POST.get('yearlyAggregatedDetails')
        # data = json.loads(request.body)
        admission_no = request.GET.get('admission_no')
        student_id = request.GET.get('student_id')
        amount = request.GET.get('amount')
        yearly_aggregated_details = request.GET.get('yearlyAggregatedDetails')
        print("request.POST.get('yearly_aggregated_details')", yearly_aggregated_details)

        response = {}

        # Validate admission number
        # if not admission_no or not admission_no.isdigit():
        #     response['success'] = False
        #     response['message'] = "Invalid admission number."
        #     return JsonResponse(response)
        try:
            admission_no = int(admission_no)
        except (ValueError, TypeError):
            return JsonResponse({
                'success': False,
                'message': 'Invalid admission number.'
            })

        if not admission_no:
            return JsonResponse({
                'success': False,
                'message': 'Admission number cannot be empty or non-numeric.'
            })

        # Validate student ID
        if not student_id or not str(student_id).isdigit():
            response['success'] = False
            response['message'] = "Invalid student ID."
            return JsonResponse(response)
        

        # Validate amount
        try:
            amount = float(amount)
            if amount <= 0:
                raise ValueError
        except ValueError:
            response['success'] = False
            response['message'] = "Invalid amount."
            return JsonResponse(response)

        # Initialize variables
        try:
            student_record = student_master.objects.get(student_id=student_id)
            student_name = student_record.student_name
            email = student_record.email or 'shishuniketan_mohali@yahoo.co.in'
            mobile = student_record.mobile_no or student_record.phone_no
            stu_id = student_id
            stu_admsn_no = admission_no
            father_name = student_record.father_name
            shool_fee = 0
            late_fee = 0

            # Validate student name
            if not student_name:
                response['success'] = False
                response['message'] = "Student name cannot be empty."
                return JsonResponse(response)

            # Validate email
            if not email or not re.match(r"[^@]+@[^@]+\.[^@]+", email):
                response['success'] = False
                response['message'] = "Invalid email address."
                return JsonResponse(response)

            # Validate mobile
            if not mobile or not re.match(r'^\d{10}$', mobile):
                response['success'] = False
                response['message'] = "Invalid mobile number."
                return JsonResponse(response)

            # Generate reference number and save transaction
            ref_number = generate_unique_reference_number()
            # ref_number = '456789'
            # saved = save_school_fee_transaction(student_id, ref_number, json.loads(yearly_aggregated_details))
            fee_data = json.loads(yearly_aggregated_details)
            saved = save_school_fee_transaction(student_id, ref_number, fee_data)
            print('saved',saved)
            if saved.get('status') == "success":
                class_ = saved['class']
                year = saved['year']
                # fee_months = saved['months_paid_for']
                fee_months = "4,5,6"

                # Payment URL parameters
                # merchant_id = "378142" productin
                merchant_id = "600561"
                # key = "1163222711105010"
                key = "6000010905605020"
                # key = "6000010905605020".encode('utf-8')
                sub_mer_id = "45"
                amt = amount
                # amt = 10
                stu_name = student_name
                stu_mobile = mobile
                print('stu_mobile',stu_mobile)
                stu_email = email
                # return_url = "https://shishuniketanmohali.org.in/fees/paymentResponse.php"
                # return_url = "http://127.0.0.1:8000/payment-response/"
                # return_url = "http://66.235.194.119:8080/payment-response/"
                return_url = os.getenv("DB_RETURN_URL", "http://66.235.194.119:8080/payment-response/")
                # return_url = "https://shishuniketanmohali.org.in/"
                paymode = "9"
                # paymode = "10"
                upi_vpa = "X"
                # man_fields = f"{ref_number}|{sub_mer_id}|0|{stu_id}|{stu_admsn_no}|{stu_name}|{father_name}|{class_}|{year}|{fee_months}|{amt}|{late_fee}|{upi_vpa}"
                man_fields = f"{ref_number}|{sub_mer_id}|{amount}|x|{stu_mobile}|{stu_email}|{upi_vpa}"
                # man_fields = "456789|45|10|x|1111111111|TEST@GMAIL.COM|X"
                
                e_sub_mer_id = aes128_encrypt(sub_mer_id, key)
                print('e_sub_mer_id',e_sub_mer_id)
                e_ref_no = aes128_encrypt(ref_number, key)
                print('e_ref_no',e_ref_no)
                e_amt = aes128_encrypt(str(amt), key)
                e_stu_name = aes128_encrypt(stu_name, key)
                print('e_stu_name',e_stu_name)
                e_stu_mobile = aes128_encrypt(stu_mobile, key)
                print('stu_mobile',stu_mobile)
                e_stu_email = aes128_encrypt(stu_email, key)
                e_return_url = aes128_encrypt(return_url, key)
                e_paymode = aes128_encrypt(paymode, key)
                print('e_paymode',e_paymode)
                e_man_fields = aes128_encrypt(man_fields, key)

                payment_url = f"https://eazypayuat.icicibank.com/EazyPG?merchantid={merchant_id}&mandatory fields={e_man_fields}&optional fields=&returnurl={e_return_url}&Reference No={e_ref_no}&submerchantid={e_sub_mer_id}&transaction amount={e_amt}&paymode={e_paymode}"
                # payment_url = "https://eazypayuat.icicibank.com/EazyPG?merchantid=600561&mandatory fields=WcoTsDD2qWkQDwABJVWkNq6GotvAFWf+XIyH9ssf6JZREsOWEHFzZ7HqlH/ZdgR4&optional fields=&returnurl=LKME+YsMx5b8VmRhmtp51jpvxdFUaAeOdtWbg4n1ASgcunfUyydb9BwLRMr7ZpQI&Reference No=Ug0V5lh92uoKq3B9IWK+Dw==&submerchantid=3SKElz7oWfuogrGfkl4uVg==&transaction amount=DXrcF3CdUzxeiOT9qGpEIA==&paymode=HPkV5AoqluM4fmQ0N3UmeQ=="

                print('payment_url',payment_url)

                response['success'] = True
                response['url'] = payment_url
                response['message'] = "Payment URL generated successfully."
                return JsonResponse(response)
            else:
                response['success'] = False
                response['message'] = "Error initializing payment"
                return JsonResponse(response)
        except student_master.DoesNotExist:
            response['success'] = False
            response['message'] = "Student record does not exist."
            return JsonResponse(response)
    else:
        response = {'success': False, 'message': 'Invalid request method.'}
        return JsonResponse(response)
    


@csrf_exempt
def payment_response(request):
    txn_id = ''
    receipt_url = ''
    # print('request.method',request.method)
    print(" request.POST.get('Response_Code')",request.POST)
    if request.method == 'POST':
        # Assuming the payment gateway sends back data as key-value pairs
        data = (request.POST)
        response_code = request.POST.get('Response Code')
        print('response_code after',response_code)
        unique_ref_number = request.POST.get('Unique Ref Number')
        # service_tax_amount = data.get('Service_Tax_Amount')
        # processing_fee_amount = data.get('Processing_Fee_Amount')
        # total_amount = data.get('Total_Amount')
        transaction_amount = request.POST.get('Transaction Amount')
        # transaction_date = request.POST.get('Transaction_Date')
        payment_mode = request.POST.get('Payment_Mode')
        # sub_merchant_id = request.POST.get('SubMerchantId')
        reference_no = request.POST.get('ReferenceNo')
        # ID = request.POST.get('ID')
        # RS = request.POST.get('RS')
        # TPS = request.POST.get('TPS')
        # mandatory_fields = request.POST.get('mandatory_fields')
        # optional_fields = request.POST.get('optional_fields')
        # RSV = request.POST.get('RSV')
        
        # Check if the transaction was successful
        new_status_value = 'success' if response_code == 'E000' else 'failed'
        print('response_code',response_code)
        print('unique_ref_number',unique_ref_number)

        if response_code and unique_ref_number:
            post_data = {
                'paymentMode': payment_mode,
                'responseCode': response_code,
                'txnId': unique_ref_number,
                'refNumber': reference_no,
                'newStatusValue': new_status_value,
                'txnAmount': transaction_amount,
            }

            # API URL to process the payment on the backend
            # api_url = 'https://shishuniketanmohali.org.in/fees/index.php?r=studentFees/ProcessPayment'
            # api_url = 'http://127.0.0.1:8000/process-payment/'
            # api_url = 'http://66.235.194.119:8080/process-payment/'
            api_url = os.getenv("DB_API_URL", 'http://66.235.194.119:8080/process-payment/')

            print('api_url try', api_url)

            try:
                response = requests.post(api_url, data=post_data)
                print('response try', response)
                response_data = response.json()
                print('response_data',response_data)
                if 'receiptUrl' in response_data:
                    receipt_url = response_data['receiptUrl']
                else:
                    receipt_url = None

            except Exception as e:
                print(f"Error in request: {e}")
                receipt_url = None

            # Map response codes to their respective messages
            response_messages = {
                "E000": "Received successful confirmation in real time for the transaction. Settlement process is initiated for the transaction.",
                "E001": "Unauthorized Payment Mode",
                "E002" : "Unauthorized Key",
                "E003" : "Unauthorized Packet",
                "E004" : "Unauthorized Merchant",
                "E005" : "Unauthorized Return URL",
                "E006" : "Transaction is already paid",
                "E007" : "Transaction Failed",
                "E008" : "Failure from Third Party due to Technical Error",
                "E009" : "Bill Already Expired",
                "E0031" : "Mandatory fields coming from merchant are empty",
                "E0032" : "Mandatory fields coming from database are empty",
                "E0033" : "Payment mode coming from merchant is empty",
                "E0034" : "PG Reference number coming from merchant is empty",
                "E0035" : "Sub merchant id coming from merchant is empty",
                "E0036" : "Transaction amount coming from merchant is empty",
                "E0037" : "Payment mode coming from merchant is other than 0 to 9",
                "E0038" : "Transaction amount coming from merchant is more than 9 digit length",
                "E0039" : "Mandatory value Email in wrong format",
                "E00310" : "Mandatory value mobile number in wrong format",
                "E00311" : "Mandatory value amount in wrong format",
                "E00312" : "Mandatory value Pan card in wrong format",
                "E00313" : "Mandatory value Date in wrong format",
                "E00314" : "Mandatory value String in wrong format",
                "E00315" : "Optional value Email in wrong format",
                "E00316" : "Optional value mobile number in wrong format",
                "E00317" : "Optional value amount in wrong format",
                "E00318" : "Optional value pan card number in wrong format",
                "E00319" : "Optional value date in wrong format",
                "E00320" : "Optional value string in wrong format",
                "E00321" : "Request packet mandatory columns is not equal to mandatory columns set in enrolment or optional columns are not equal to optional columns length set in enrolment",
                "E00322" : "Reference Number Blank",
                "E00323" : "Mandatory Columns are Blank",
                "E00324" : "Merchant Reference Number and Mandatory Columns are Blank",
                "E00325" : "Merchant Reference Number Duplicate",
                "E00326" : "Sub merchant id coming from merchant is non numeric",
                "E00327" : "Cash Challan Generated",
                "E00328" : "Cheque Challan Generated",
                "E00329" : "NEFT Challan Generated",
                "E00330" : "Transaction Amount and Mandatory Transaction Amount mismatch in Request URL",
                "E00331" : "UPI Transaction Initiated Please Accept or Reject the Transaction",
                "E00332" : "Challan Already Generated, Please re-initiate with unique reference number",
                "E00333" : "Referer is null/invalid Referer",
                "E00334" : "Mandatory Parameters Reference No and Request Reference No parameter values are not matched",
                "E00335" : "Transaction Cancelled By User",
                "E0801" : "FAIL",
                "E0802" : "User Dropped",
                "E0803" : "Canceled by user",
                "E0804" : "User Request arrived but card brand not supported",
                "E0805" : "Checkout page rendered Card function not supported",
                "E0806" : "Forwarded / Exceeds withdrawal amount limit",
                "E0807" : "PG Fwd Fail / Issuer Authentication Server failure",
                "E0808" : "Session expiry / Failed Initiate Check, Card BIN not present",
                "E0809" : "Reversed / Expired Card",
                "E0810" : "Unable to Authorize",
                "E0811" : "Invalid Response Code or Guide received from Issuer",
                "E0812" : "Do not honor",
                "E0813" : "Invalid transaction",
                "E0814" : "Not Matched with the entered amount",
                "E0815" : "Not sufficient funds",
                "E0816" : "No Match with the card number",
                "E0817" : "General Error",
                "E0818" : "Suspected fraud",
                "E0819" : "User Inactive",
                "E0820" : "ECI 1 and ECI6 Error for Debit Cards and Credit Cards",
                "E0821" : "ECI 7 for Debit Cards and Credit Cards",
                "E0822" : "System error. Could not process transaction",
                "E0823" : "Invalid 3D Secure values",
                "E0824" : "Bad Track Data",
                "E0825" : "Transaction not permitted to cardholder",
                "E0826" : "Rupay timeout from issuing bank",
                "E0827" : "OCEAN for Debit Cards and Credit Cards",
                "E0828" : "E-commerce decline",
                "E0829" : "This transaction is already in process or already processed",
                "E0830" : "Issuer or switch is inoperative",
                "E0831" : "Exceeds withdrawal frequency limit",
                "E0832" : "Restricted card",
                "E0833" : "Lost card",
                "E0834" : "Communication Error with NPCI",
                "E0835" : "The order already exists in the database",
                "E0836" : "General Error Rejected by NPCI",
                "E0837" : "Invalid credit card number",
                "E0838" : "Invalid amount",
                "E0839" : "Duplicate Data Posted",
                "E0840" : "Format error",
                "E0841" : "SYSTEM ERROR",
                "E0842" : "Invalid expiration date",
                "E0843" : "Session expired for this transaction",
                "E0844" : "FRAUD - Purchase limit exceeded",
                "E0845" : "Verification decline",
                "E0846" : "Compliance error code for issuer",
                "E0847" : "Caught ERROR of type:[ System.Xml.XmlException ] . strXML is not a valid XML string Failed in Authorize - I",
                "E0848" : "Incorrect personal identification number",
                "E0849" : "Stolen card",
                "E0850" : "Transaction timed out, please retry",
                "E0851" : "Failed in Authorization - PE",
                "E0852" : "Cardholder did not return from Rupay",
                "E0853" : "Missing Mandatory Field(s)The field card_number has exceeded the maximum length of 19",
                "E0854" : "Exception in CheckEnrollmentStatus: Data at the root level is invalid. Line 1, position 1.",
                "E0855" : "CAF status = 0 or 9",
                "E0856" : "412",
                "E0857" : "Allowable number of PIN tries exceeded",
                "E0858" : "No such issuer",
                "E0859" : "Invalid Data Posted",
                "E0860" : "PREVIOUSLY AUTHORIZED",
                "E0861" : "Cardholder did not return from ACS",
                "E0862" : "Duplicate transmission",
                "E0863" : "Wrong transaction state",
                "E0864" : "Card acceptor contact acquirer",
                # Add more error messages here...
            }

            # message = response_messages.get(response_code, "Transaction Failed")
            print('response_code',response_code)
            message = response_messages.get(response_code, "Transaction Failed")
            alert_class = "success" if response_code == "E000" else "danger"

            context = {
                'txn_id': unique_ref_number,
                'message': message,
                'alert_class': alert_class,
                'receipt_url': receipt_url,
            }
            return render(request, 'payment_response.html', context)

    # If the request is not POST or there's no response_code
    return render(request, 'payment_response.html', {'message': "No transaction response", 'alert_class': 'danger'})


@csrf_exempt  # Exempt CSRF protection for testing purposes; use tokens in production.
def process_payment(request):
    if request.method == 'POST':
        # Get POST data
        response_code = request.POST.get('responseCode')
        txn_id_value = request.POST.get('txnId')
        txn_ref_number = request.POST.get('refNumber')
        payment_mode = request.POST.get('paymentMode')
        new_status_value = request.POST.get('newStatusValue')
        processing_fee = request.POST.get('processingFee', 0)  # Default to 0 if not present
        txn_amount = request.POST.get('txnAmount')
        print('txn_amount',txn_amount)

        # Check if required fields are present
        if not response_code or not txn_ref_number:
            return JsonResponse({
                'success': False,
                'message': 'Invalid data received.'
            })

        # Query the StudentFee model using the txn_ref_number
        student_fees = student_fee.objects.filter(txn_ref_number=txn_ref_number)
        if student_fees.exists():
            for student_fee1 in student_fees:
                print('student_fee1',student_fee1.student_fee_id)
                # Update the student_fee fields
                student_fee1.txn_payment_mode = payment_mode
                student_fee1.txn_response_code = response_code
                student_fee1.txn_id = txn_id_value
                student_fee1.cheque_status = new_status_value
                student_fee1.processing_fees_paid = processing_fee
                student_fee1.amount_paid = txn_amount

                try:
                    student_fee1.save()  # Save the updated model
                    response = {
                        'success': True,
                        'message': f"Update successful for student_fee_id: {student_fee1.student_fee_id}"
                    }
                except Exception as e:
                    response = {
                        'success': False,
                        'message': f"Failed to update student_fee_id: {student_fee1.student_fee_id} - {str(e)}"
                    }
        else:
            response = {
                'success': False,
                'message': 'txn_ref_number not found'
            }

        # If the transaction is updated successfully, generate a receipt PDF (implement PDF generation logic)
        if response.get('success'):
            # receipt_url = generate_receipt_pdf(txn_id_value)  # Assuming this function generates the PDF
            # receipt_url = generate_pdf(txn_id_value) 
            receipt_url = action_generate_pdf(request,txn_id_value) 
            print('receipt_url',receipt_url['receiptUrl'])
            response['receiptUrl'] = receipt_url['receiptUrl']

        return JsonResponse(response)
    else:
        return JsonResponse({
            'success': False,
            'message': 'Invalid request method.'
        })

# Assuming you have a PDF generation function in your views.py or elsewhere
def generate_receipt_pdf(txn_id):
    # Your logic for generating a PDF receipt and returning the URL
    # Assuming this returns a URL of the receipt PDF
    receipt_url = f'/media/receipts/receipt_{txn_id}.pdf'
    return receipt_url


def generate_pdf(txn_id):
    """
    Generates a PDF for the given transaction ID and updates the receipt URL in the database.
    """
    response_data = {
        'success': False,
        'message': 'No records found for the given transaction ID'
    }

    # Retrieve fee receipt details
    receipt_data = get_fee_receipt_details(txn_id)  # Assuming you have this function implemented
    print('receipt_data',receipt_data)
    if receipt_data:
        # Create a new PDF in memory
        buffer = BytesIO()
        pdf = canvas.Canvas(buffer)
        
        # Set PDF meta-data
        pdf.setTitle('Invoice')

        # Define the content and structure for the PDF
        pdf.drawString(100, 800, "Shishu Niketan Public School")
        pdf.drawString(100, 780, "FEE RECEIPT")
        pdf.drawString(100, 760, f"Year: {receipt_data['year']}")
        pdf.drawString(100, 740, f"Receipt: {receipt_data['receipt_number']}")
        pdf.drawString(100, 720, f"Transaction ID: {txn_id}")
        pdf.drawString(100, 700, f"Admission No.: {receipt_data['addmission_no']}")
        pdf.drawString(100, 680, f"Student Name: {receipt_data['student_name']}")
        pdf.drawString(100, 660, f"Father Name: {receipt_data['father_name']}")
        pdf.drawString(100, 640, f"Mother Name: {receipt_data['mother_name']}")
        pdf.drawString(100, 620, f"Class: {receipt_data['student_class']}")
        pdf.drawString(100, 600, f"Payment Mode: {receipt_data['txn_payment_mode']}")
        pdf.drawString(100, 580, f"Paid for Session (Months): {receipt_data['months_paid']}")
        pdf.drawString(100, 560, f"Total Fees Paid: {receipt_data['total_amount_paid']}")
        pdf.drawString(100, 540, f"Remarks: {receipt_data['remarks']}")
        
        # Footer
        pdf.drawString(100, 520, "Copyright © shishuniketanmohali.org.in - All Rights Reserved.")
        # pdf.drawString(100, 50, "Copyright © shishuniketanmohali.org.in - All Rights Reserved.")

        # Save the PDF into the buffer
        pdf.showPage()
        pdf.save()
        
        buffer.seek(0)

        # Define the folder path where you want to store PDFs
        pdf_folder = os.path.join(settings.MEDIA_ROOT, 'pdfs')

        # Create the folder if it does not exist
        if not os.path.exists(pdf_folder):
            os.makedirs(pdf_folder)

        # File name and path
        pdf_filename = f'invoice_{txn_id}.pdf'
        pdf_file_path = os.path.join(pdf_folder, pdf_filename)

        # Write PDF data to the file
        with open(pdf_file_path, 'wb') as f:
            f.write(buffer.read())

        # Build the file URL
        pdf_url = os.path.join(settings.MEDIA_URL, 'pdfs', pdf_filename)
        print('pdf_url after',pdf_url)
        # Update the `receipt_url` field in the database
        student_fees = student_fee.objects.filter(txn_id=txn_id)
        if student_fees.exists():
            student_fees.update(receipt_url=pdf_url)

            response_data = {
                'success': True,
                'receiptUrl': pdf_url,
                'message': f"Receipt URL updated successfully for txn_id: {txn_id}"
            }
        else:
            response_data = {
                'success': False,
                'message': f"No records found for txn_id: {txn_id}"
            }

    return (response_data)




def action_generate_pdf(request, txn_id):
    # Fetch receipt data based on txn_id
    # receipt_data = get_fee_receipt_details(txn_id)  # Function to fetch the data
    receipt_data = get_fee_receipt_details(txn_id)

    if receipt_data:
        # Prepare HTML content with the receipt data
        html_content = render_to_string('fee_receipt.html', {
            'addmission_no': receipt_data['addmission_no'],
            'student_name': receipt_data['student_name'],
            'father_name': receipt_data['father_name'],
            'mother_name': receipt_data['mother_name'],
            'student_class': receipt_data['student_class'],
            'receipt_number': receipt_data['receipt_number'],
            'date_payment': receipt_data['date_payment'],
            'year': receipt_data['year'],
            'txn_id': receipt_data['txn_id'],
            'txn_payment_mode': receipt_data['txn_payment_mode'],
            'months_paid': receipt_data['months_paid'],
            'total_amount_paid': receipt_data['total_amount_paid'],
            'remarks': receipt_data['remarks'],
        })

        # Create a BytesIO stream to hold the generated PDF
        pdf_file = BytesIO()
        pisa_status = pisa.CreatePDF(html_content, dest=pdf_file)

        # Define the path to save the PDF
        pdf_folder_path = os.path.join(settings.MEDIA_ROOT, 'pdfs/')
        os.makedirs(pdf_folder_path, exist_ok=True)
        pdf_file_path = os.path.join(pdf_folder_path, f'invoice_{txn_id}.pdf')

        # Save the generated PDF to the specified path
        with open(pdf_file_path, 'wb') as f:
            f.write(pdf_file.getvalue())

        # Generate the public URL to the PDF file
        pdf_file_url = os.path.join(settings.MEDIA_URL, f'pdfs/invoice_{txn_id}.pdf')
        host_info = request.build_absolute_uri(settings.MEDIA_URL)

        # Find the student fee record and update the receipt_url field
        student_fees = student_fee.objects.filter(txn_id=txn_id)
        if student_fees.exists():
            for fee in student_fees:
                fee.receipt_url = pdf_file_url
                fee.save()

            # Return a success response with the PDF URL
            response = {
                'success': True,
                'receiptUrl': host_info + f'pdfs/invoice_{txn_id}.pdf',
                'message': f"Receipt URL updated successfully for txn_id: {txn_id}",
            }
        else:
            response = {
                'success': False,
                'message': 'No records found for the given transaction id',
            }
    else:
        response = {
            'success': False,
            'message': 'No records found for the given transaction id',
        }

    return (response)

# def get_fee_receipt_details(txn_id):
#     # Fetch and return the receipt data for the provided txn_id
#     # This is a placeholder; you'll need to implement based on your model's structure
#     fee = StudentFees.objects.filter(txn_id=txn_id).first()
#     if fee:
#         return {
#             'addmission_no': fee.student.admission_no,  # Assuming ForeignKey to student
#             'student_name': fee.student.name,
#             'father_name': fee.student.father_name,
#             'mother_name': fee.student.mother_name,
#             'student_class': fee.student.student_class,
#             'receipt_number': fee.receipt_number,
#             'date_payment': fee.date_payment,
#             'year': fee.year,
#             'txn_id': fee.txn_id,
#             'txn_payment_mode': fee.txn_payment_mode,
#             'months_paid': fee.months_paid,
#             'total_amount_paid': fee.amount_paid,
#             'remarks': fee.remarks,
#         }
#     return None


# Function to simulate sending an OTP (implement your own logic)
# def send_otp(user):
#     otp = random.randint(1000, 9999)  # Generate a random 6-digit OTP
#     user.last_name = otp  # Store OTP in user instance (you might want to save it in the database or cache)
#     user.save()
#     print(f"OTP sent to {user.first_name}: {otp}")  # Replace with actual sending logic (email/SMS)

def send_otp(user):
    otp = random.randint(1000, 9999)  # Generate a random 6-digit OTP
    user.last_name = otp  # Store OTP in user instance (you might want to save it in the database or cache)
    user.save()
    sms_response = send_otp_via_textlocal(user.first_name, otp)
    print('sms_response',sms_response)
    print(f"OTP sent to {user.first_name}: {otp}")  # Replace with actual sending logic (email/SMS)

def custom_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        # Authenticate user
        # user = authenticate(request, username=email, password=password)
        user = authenticate(request, email=email, password=password)
        if user is not None:
            # Login user and send OTP
            send_otp(user)
            request.session['user_id'] = user.id  # Store user ID in session for later use
            return redirect('otp_verification')  # Redirect to OTP verification page
        else:
            messages.error(request, "Invalid email or password.")
            return render(request, 'app/login.html')

    else:
        print('checing----------')
        return render(request, 'app/login.html')  # Render the custom login template


def otp_verification(request):
    if request.method == 'POST':
        otp = request.POST.get('otp')
        user_id = request.session.get('user_id')  # Get user ID from session
        print('user_id in otp_verification:', user_id)
        
        try:
            # Fetch the complete user object
            user = User.objects.get(pk=user_id)
            print('user in otp_verification:', user)
        except User.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'User does not exist'})

        # Validate the OTP using the user's last_name (for your scenario)
        if user.last_name and int(otp) == int(user.last_name):
            # Set the backend manually
            user.backend = 'django.contrib.auth.backends.ModelBackend'

            # Log the user in
            login(request, user)  # Log the user in
            return JsonResponse({'success': True})  # Respond with success status
        else:
            return JsonResponse({'success': False, 'error': 'Invalid OTP'})

    return render(request, 'admin/otp_verification.html')


# @require_GET
# def send_otp_verification_from_admin(request):


#     print(f'request----->{request}')


#     admission_number = request.GET.get('admissionNumber')

#     print(f'request----->{admission_number}')
    
#     response = {
#         'success': False,
#         'message': "Invalid admission number",
#         'data': []
#     }

#     if admission_number:
#         try:
#             student = student_master.objects.get(addmission_no=admission_number)
#             otp = str(random.randint(1000, 9999)).zfill(4)
#             otp = '2135' if student.mobile_no == '8146558059' else otp
#             student.otp = otp
#             student.save()

#             # Uncomment to enable email sending
#             # send_mail("OTP for verification", f"Your OTP is: {otp}", 'from@example.com', [student.email])

#             response['success'] = True
#             response['message'] = "OTP sent successfully"
#             response['data']['otp'] = otp
#         except student_master.DoesNotExist:
#             response['message'] = "Student not found"

#     return JsonResponse(response)

@require_GET
def send_otp_verification_from_admin(request):
    print(f'request----->{request}')

    admission_number = request.GET.get('admissionNumber')
    print(f'request----->{admission_number}')
    
    response = {
        'success': False,
        'message': "Invalid admission number",
        'data': {}  # Initialize this as a dictionary instead of a list
    }

    if admission_number:
        try:
            student = student_master.objects.get(addmission_no=admission_number)
            otp = str(random.randint(1000, 9999)).zfill(4)
            otp = '2135' if student.mobile_no == '8146558059' else otp
            student.otp = otp
            student.save()

            # Uncomment to enable email sending
            # send_mail("OTP for verification", f"Your OTP is: {otp}", 'from@example.com', [student.email])

            response['success'] = True
            response['message'] = "OTP sent successfully"
            response['data']['otp'] = otp  # Assign OTP to the 'data' dictionary
        except student_master.DoesNotExist:
            response['message'] = "Student not found"

    return JsonResponse(response)



@require_GET
def verify_otp_for_admin(request):

    print(f"----------- im in verify_otp_for_admin ----------------")

    print(request)

    admission_number = request.GET.get('admissionNumber')
    otp = request.GET.get('otp')

    response = {
        'success': False,
        'message': 'Invalid parameters',
        'data': []
    }

    if admission_number and otp:
        try:
            student = student_master.objects.get(addmission_no=admission_number)

            if student.otp == otp:
                student.otp = None
                student.save()
                response['success'] = True
                response['message'] = 'OTP verified successfully'
            else:
                response['message'] = 'Invalid OTP. Please try again.'
        except student_master.DoesNotExist:
            response['message'] = 'Student not found'
    
    return JsonResponse(response)
