from django.contrib import admin
from .models import (
    teacher_master, student_master, student_fee, student_class, specialfee_master,
    payment_schedule_master, latefee_master, fees_master, expense,
    concession_master, bus_master, busfees_master, account_head,generate_mobile_number_list, cheque_status
)
from django.db.models import Max
from django import forms
# from datetime import date, timezone
from django.urls import path
from django.http import JsonResponse
from django.core.exceptions import ValidationError
from django.utils.safestring import mark_safe

# by amrit
from .forms import FeeNotApplicableForm
from django.shortcuts import render
from django.http import HttpResponseRedirect
from import_export import resources
from import_export.admin import ExportMixin
from import_export.fields import Field
from ckeditor.widgets import CKEditorWidget
from .widgets import ReadOnlyCKEditorWidget
from django.db.models import Q
from django.db.models import IntegerField, Value as V
from django.db.models.functions import Cast


from django.db.models import OuterRef, Subquery, Exists

import csv
from django.http import HttpResponse

from django.utils import timezone
from .forms import RealizedDateForm
from django.utils.dateformat import DateFormat
from . import views
# from django.utils.safestring import mark_safe
# vikas code

# from datetime import datetime
# from django.shortcuts import get_object_or_404
from django.http import JsonResponse, HttpResponse
# from datetime import datetime
from django.db import connection
from datetime import datetime
# from django.db.models.functions import Lower
from datetime import datetime, timedelta
from django.utils.dateparse import parse_date
from django.db.models import Sum, F, Q
import time
import logging

from .services import last_payment_record,fetch_fee_details_for_class,get_special_fee,calculate_late_fee

CLASS_CHOICES = [
        ('', 'Select the Class'),
        ('Play-way', 'Play-way'),
        ('Nursery', 'Nursery'),
        ('lkg', 'LKG'),
        ('ukg', 'UKG'),
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
        ('4', '4'),
        ('5', '5'),
        ('6', '6'),
        ('7', '7'),
        ('8', '8'),
        ('9', '9'),
        ('10', '10'),
        ('11', '11'),
        ('12', '12')
    ]
SECTION = [
        ('', 'Select the Section'),
        ('A', 'A'),
        ('B', 'B'),
        ('C', 'C'),
        ('D', 'D'),
        ('E', 'E'),
        ('F', 'F'),
        ('G', 'G'),
        ('H', 'H'),
        ('I', 'I'),
        ('J', 'J'),
    ]

PAYMENT_MODE_CHOICES = [
    ('Cash', 'Cash'),
    ('Cheque', 'Cheque'),
    ('Online', 'Online'),
]

CHEQUE_STATUS_CHOICES = [
    ('Open', 'Open'),
    ('Rejected', 'Rejected'),
    ('Realized', 'Realized'),
]

BANK_CHOICES = [
    (None, 'Select Bank'),
    ('ALLAHABAD BANK (ALB)', 'ALLAHABAD BANK (ALB)'),
    ('ANDHRA BANK (ANB)', 'ANDHRA BANK (ANB)'),
    ('AXIS BANK (AXS)', 'AXIS BANK (AXS)'),
    ('BOB', 'BOB'),
    ('BOI', 'BOI'),
    ('BOM', 'BOM'),
    ('CANARA BANK (CAB)', 'CANARA BANK (CAB)'),
    ('CBOI (CBI)', 'CBOI (CBI)'),
    ('CITY', 'CITY'),
    ('COOPERATION BANK', 'COOPERATION BANK'),
    ('COOPERATIVE BANK (COB)', 'COOPERATIVE BANK (COB)'),
    ('DENA BANK (DEB)', 'DENA BANK (DEB)'),
    ('DCB', 'DCB'),
    ('EQUITAS', 'EQUITAS'),
    ('FEDERAL BANK (FB)', 'FEDERAL BANK (FB)'),
    ('GPO FEDERAL BANK (GPO)', 'GPO FEDERAL BANK (GPO)'),
    ('HDFC (HDF)', 'HDFC (HDF)'),
    ('ICICI (ICI)', 'ICICI (ICI)'),
    ('IDBI (IDB)', 'IDBI (IDB)'),
    ('IDL', 'IDL'),
    ('INDIAN BANK (INB)', 'INDIAN BANK (INB)'),
    ('INDUSIND (IDS)', 'INDUSIND (IDS)'),
    ('IOB', 'IOB'),
    ('J&K BANK', 'J&K BANK'),
    ('KOTAK (KOT)', 'KOTAK (KOT)'),
    ('KARNATAKA BANK (KBL)', 'KARNATAKA BANK (KBL)'),
    ('OBOC', 'OBOC'),
    ('PGB', 'PGB'),
    ('PNB', 'PNB'),
    ('P&SB (PSB)', 'P&SB (PSB)'),
    ('OBOC (OBC)', 'OBOC (OBC)'),
    ('SBI', 'SBI'),
    ('STANDARD CHARTED', 'STANDARD CHARTED'),
    ('SYNDICATE BANK (SYB)', 'SYNDICATE BANK (SYB)'),
    ('SOUTH INDIAN', 'SOUTH INDIAN'),
    ('UBOI (UBI)', 'UBOI (UBI)'),
    ('UNI', 'UNI'),
    ('UCO', 'UCO'),
    ('VIJAYA BANK (VJB)', 'VIJAYA BANK (VJB)'),
    ('YES BANK', 'YES BANK'),
    ('YES PROPERTY', 'YES PROPERTY'),
    ('OTHER', 'OTHER'),
]

FEE_MONTHS_CHOICES = [
        ('4,5,6', '4,5,6'),
        ('7,8,9', '7,8,9'),
        ('10,11,12', '10,11,12'),
        ('1,2,3', '1,2,3')
    ]

# Register your models here.

class TeacherMasterForm(forms.ModelForm):
    role = forms.ChoiceField(choices=teacher_master.ROLES_CHOICES, required=True)

    class Meta:
        model = teacher_master
        fields = [
            "user_name", "email", "mobile","role"
        ]

# class UserDisplay(admin.ModelAdmin):
#     list_display = ("user_name", "email", "created_at",)

class UserDisplay(admin.ModelAdmin):
    form = TeacherMasterForm
    list_display = ("teacher_name", "email", "mobile", "role")
    search_fields = ("user_name", "email", "mobile", "role")
    list_filter = ("role",)

    def teacher_name(self, obj):
        return obj.user_name  # Assuming user_name is the field in the model
    
    teacher_name.short_description = 'Teacher Name'

    def get_queryset(self, request):
        # Get the original queryset
        queryset = super().get_queryset(request)

        # Retrieve the search terms from the GET parameters
        user_name = request.GET.get('user_name', '')
        email = request.GET.get('email', '')
        mobile = request.GET.get('mobile', '')
        role = request.GET.get('role', '')

        # Apply filters based on the search terms
        if user_name:
            queryset = queryset.filter(user_name__icontains=user_name)
        if email:
            queryset = queryset.filter(email__icontains=email)
        if mobile:
            queryset = queryset.filter(mobile__icontains=mobile)
        if role:
            queryset = queryset.filter(role__icontains=role)

        return queryset

class StudentMasterForm(forms.ModelForm):
    class_no = forms.ChoiceField(choices=student_class.CLASS_CHOICES, required=True)
    section = forms.ChoiceField(choices=student_class.SECTION, required=True)
    concession_id = forms.ModelChoiceField(
        queryset=concession_master.objects.all(),
        required=False,
        label='Concession Type',
        empty_label='Select Concession Type'
    )
    route = forms.ChoiceField(
        choices=[('', 'Select Route')] + [(route, route) for route in busfees_master.objects.values_list('route', flat=True).distinct()],
        required=False,
        label='Route',
    )
    destination = forms.ChoiceField(
        choices=[('', 'Select Destination')],
        required=False,
        label='Destination',
    )

    class Meta:
        model = student_master
        fields = [
            'addmission_no', 'student_name', 'class_no', 'section', 'father_name', 'mother_name', 'birth_date',
            'phone_no', 'mobile_no', 'aadhaar_no', 'email', 'address', 'city', 'route', 'destination',
            'gender', 'admission_date', 'concession_id', 'status', 'category', 'passedout_date',
            'remarks'
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['concession_id'].label_from_instance = lambda obj: obj.concession_type

        # Prepopulate route and destination if instance is being edited
        if self.instance and self.instance.pk:
            bus_id = self.instance.bus_id
            if bus_id:
                busfee_instance = busfees_master.objects.filter(bus_id=bus_id).first()
                if busfee_instance:
                    self.fields['route'].initial = busfee_instance.route
                    self.fields['destination'].choices = [(busfee_instance.destination, busfee_instance.destination)]
                    self.fields['destination'].initial = busfee_instance.destination

        # If a route is selected, populate the destination choices
        selected_route = self.data.get('route') or self.fields['route'].initial
        if selected_route:
            self.fields['destination'].choices = [
                (dest['destination'], dest['destination'])
                for dest in busfees_master.objects.filter(route=selected_route).values('destination')
            ]
                
        if self.instance and self.instance.pk is None:
            last_admission_no = student_master.objects.aggregate(Max('addmission_no'))['addmission_no__max']
            self.fields['addmission_no'].initial = (last_admission_no or 0) + 1
            if not self.fields['admission_date'].initial:
                self.fields['admission_date'].initial = date.today()
        else:
            student_class_instance = student_class.objects.filter(student_id=self.instance.student_id).order_by('-started_on').first()
            if student_class_instance:
                self.fields['class_no'].initial = student_class_instance.class_no
                self.fields['section'].initial = student_class_instance.section

    def clean_concession_id(self):
        concession = self.cleaned_data.get('concession_id')
        return concession.concession_id if concession else None



class StudentMasterAdmin(admin.ModelAdmin):
    form = StudentMasterForm
    list_display = ('student_id', 'student_name', 'get_class_no', 'get_section', 'addmission_no', 'gender', 'birth_date', 'category', 'status', 'admission_date', 'passedout_date')
    search_fields = ('student_name', 'addmission_no', 'aadhaar_no', 'email', 'city', 'birth_date')

    def get_class_no(self, obj):
        student_class_instance = student_class.objects.filter(student_id=obj.student_id).order_by('-started_on').first()
        return student_class_instance.class_no if student_class_instance else None
    get_class_no.short_description = 'Class'

    def get_section(self, obj):
        student_class_instance = student_class.objects.filter(student_id=obj.student_id).order_by('-started_on').first()
        return student_class_instance.section if student_class_instance else None
    get_section.short_description = 'Section'
    
    def save_model(self, request, obj, form, change):
        # Retrieve bus_id based on selected route and destination
        route = form.cleaned_data.get('route')
        destination = form.cleaned_data.get('destination')
        if route and destination:
            busfee_instance = busfees_master.objects.filter(route=route, destination=destination).first()
            if busfee_instance:
                obj.bus_id = busfee_instance.bus_id

        super().save_model(request, obj, form, change)

        if change:
            student_class_instance = student_class.objects.filter(student_id=obj.student_id).order_by('-started_on').first()
            if student_class_instance:
                student_class_instance.class_no = form.cleaned_data['class_no']
                student_class_instance.section = form.cleaned_data['section']
                student_class_instance.save()
            else:
                student_class.objects.create(
                    student_id=obj.student_id,
                    class_no=form.cleaned_data['class_no'],
                    section=form.cleaned_data['section']
                )
        else:
            if form.cleaned_data['class_no'] and form.cleaned_data['section']:
                student_class.objects.create(
                    student_id=obj.student_id,
                    class_no=form.cleaned_data['class_no'],
                    section=form.cleaned_data['section']
                )
        
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('ajax/load-destinations/', self.admin_site.admin_view(self.load_destinations), name='ajax_load_destinations'),
        ]
        return custom_urls + urls

    def load_destinations(self, request):
        route = request.GET.get('route')
        destinations = list(busfees_master.objects.filter(route=route).values('destination'))
        return JsonResponse(destinations, safe=False)

    class Media:
        js = ('app/js/student_master.js',)

# class StudentMasterAdmin(admin.ModelAdmin):
#     form = StudentMasterForm
#     list_display = ('student_id', 'student_name', 'get_class_no', 'get_section', 'addmission_no', 'gender', 'birth_date', 'category', 'status', 'admission_date', 'passedout_date')
#     search_fields = ('student_name', 'addmission_no', 'aadhaar_no', 'email', 'city', 'birth_date')

#     # Other methods...

#     def get_urls(self):
#         urls = super().get_urls()
#         custom_urls = [
#             path('mobile-number-list/', self.admin_site.admin_view(self.mobile_number_list_view), name='mobile_number_list'),
#             path('ajax/load-destinations/', self.admin_site.admin_view(self.load_destinations), name='ajax_load_destinations'),
#         ]
#         return custom_urls + urls

#     def mobile_number_list_view(self, request):
#         # Filter the student_master queryset
#         qs = student_master.objects.all()

#         class_no = request.GET.get('class_no')
#         section = request.GET.get('section')
#         admission_date = request.GET.get('admission_date')

#         if class_no:
#             qs = qs.filter(student_class__class_no=class_no)
#         if section:
#             qs = qs.filter(student_class__section=section)
#         if admission_date:
#             qs = qs.filter(admission_date=admission_date)

#         # Export filtered results to CSV
#         # if 'export' in request.GET:
#         #     response = HttpResponse(content_type='text/csv')
#         #     response['Content-Disposition'] = 'attachment; filename="mobile_number_list.csv"'

#         #     writer = csv.writer(response)
#         #     writer.writerow(['Admission No', 'Student Name', 'Class', 'Section', 'Mobile No'])
#         #     for student in qs:
#         #         writer.writerow([student.addmission_no, student.student_name, self.get_class_no(student), self.get_section(student), student.mobile_no])

#         #     return response

#         context = {
#             'students': qs,
#             'class_no': class_no,
#             'section': section,
#             'admission_date': admission_date,
#         }
#         return render(request, 'admin/mobile_number_list.html', context)

#     def get_class_no(self, obj):
#         student_class_instance = student_class.objects.filter(student_id=obj.student_id).order_by('-started_on').first()
#         return student_class_instance.class_no if student_class_instance else None
#     get_class_no.short_description = 'Class'

#     def get_section(self, obj):
#         student_class_instance = student_class.objects.filter(student_id=obj.student_id).order_by('-started_on').first()
#         return student_class_instance.section if student_class_instance else None
#     get_section.short_description = 'Section'

    
#     def save_model(self, request, obj, form, change):
#         # Retrieve bus_id based on selected route and destination
#         route = form.cleaned_data.get('route')
#         destination = form.cleaned_data.get('destination')
#         if route and destination:
#             busfee_instance = busfees_master.objects.filter(route=route, destination=destination).first()
#             if busfee_instance:
#                 obj.bus_id = busfee_instance.bus_id

#         super().save_model(request, obj, form, change)

#         if change:
#             student_class_instance = student_class.objects.filter(student_id=obj.student_id).order_by('-started_on').first()
#             if student_class_instance:
#                 student_class_instance.class_no = form.cleaned_data['class_no']
#                 student_class_instance.section = form.cleaned_data['section']
#                 student_class_instance.save()
#             else:
#                 student_class.objects.create(
#                     student_id=obj.student_id,
#                     class_no=form.cleaned_data['class_no'],
#                     section=form.cleaned_data['section']
#                 )
#         else:
#             if form.cleaned_data['class_no'] and form.cleaned_data['section']:
#                 student_class.objects.create(
#                     student_id=obj.student_id,
#                     class_no=form.cleaned_data['class_no'],
#                     section=form.cleaned_data['section']
#                 )


#     def load_destinations(self, request):
#         route = request.GET.get('route')
#         destinations = list(busfees_master.objects.filter(route=route).values('destination'))
#         return JsonResponse(destinations, safe=False)

#     class Media:
#         js = ('app/js/student_master.js',)

    # Existing methods...

# admin.site.register(student_master, StudentMasterAdmin)


class FeesMasterForm(forms.ModelForm):
    class Meta:
        model = fees_master
        fields = [
            'class_no', 'annual_fees', 'tuition_fees', 'funds_fees', 'sports_fees', 'activity_fees',
            'activity_fees_mandatory', 'admission_fees', 'dayboarding_fees', 'miscellaneous_fees',
            'valid_from', 'valid_to'
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        current_year = date.today().year
        if not self.instance.pk:  # Check if the form is for creating a new instance
            self.fields['valid_from'].initial = date(current_year, 4, 1)
            self.fields['valid_to'].initial = date(current_year + 1, 3, 31)

    def clean(self):
        cleaned_data = super().clean()
        activity_fees_mandatory = cleaned_data.get('activity_fees_mandatory')
        activity_fees = cleaned_data.get('activity_fees')
        class_no = cleaned_data.get('class_no')
        valid_from = cleaned_data.get('valid_from')
        valid_to = cleaned_data.get('valid_to')

        # Check if the combination of class_no, valid_from, and valid_to already exists
        if not self.instance.pk:  # Only check for new instances
            if fees_master.objects.filter(class_no=class_no, valid_from=valid_from, valid_to=valid_to).exists():
                raise ValidationError("Fees already exists for this class and session.")

        if activity_fees_mandatory and (activity_fees is None or activity_fees == ''):
            self.add_error('activity_fees', 'This field is required when Activity Fees Mandatory is checked.')

        return cleaned_data

class FeesMasterAdmin(admin.ModelAdmin):
    form = FeesMasterForm
    list_display = ("fees_id", "class_no", "annual_fees", "tuition_fees", "funds_fees", "sports_fees", "activity_fees", "admission_fees", "dayboarding_fees", "miscellaneous_fees", "valid_from", "valid_to")

admin.site.register(student_master,StudentMasterAdmin)
# admin.site.register(user, UserDisplay)
admin.site.register(teacher_master, UserDisplay)
admin.site.register(account_head)

# class BusFeesMaster(admin.ModelAdmin):
#     list_display = ("bus_id", "route", "destination", "bus_fees", "fee_not_applicable_in_months")
#     search_fields = ['route']
    

class BusFeesMasterResource(resources.ModelResource):
    # Custom fields for Bus Driver and Bus Attendant
    route = Field(attribute='route', column_name='Bus Route')
    destination = Field(attribute='destination', column_name='Destination')
    bus_fees = Field(attribute='bus_fees', column_name='Bus Fees')
    bus_driver = Field(attribute='bus_driver', column_name='Bus Driver')
    bus_attendant = Field(attribute='bus_attendant', column_name='Bus Attendant')

    class Meta:
        model = busfees_master
        fields = ('route', 'destination', 'bus_fees', 'bus_driver', 'bus_attendant')
        export_order = ('route', 'destination', 'bus_fees', 'bus_driver', 'bus_attendant')

    def dehydrate_bus_driver(self, obj):
        # Assuming 'bus_driver' is a related field on the model
        return obj.bus_driver if obj.bus_driver else 'N/A'

    def dehydrate_bus_attendant(self, obj):
        # Assuming 'bus_attendant' is a related field on the model
        return obj.bus_attendant if obj.bus_attendant else 'N/A'


class BusFeesMasterForm(forms.ModelForm):    
    route = forms.ChoiceField(
        choices=[('', 'Select Route')] + [(route, route) for route in bus_master.objects.values_list('bus_route', flat=True)],
        required=False,
        label='Route',
    )

    class Meta:
        model = busfees_master
        fields = [
            "route", "destination", "bus_fees"
        ]


class BusFeesMaster(ExportMixin, admin.ModelAdmin):
    form = BusFeesMasterForm
    list_display = ( "route", "destination", "bus_fees", "get_bus_driver", "get_bus_attendant")
    search_fields = ['route']
    resource_class = BusFeesMasterResource
    # Custom method to retrieve bus_driver from the related BusMaster model
    def get_bus_driver(self, obj):
        return obj.bus_driver
    get_bus_driver.short_description = 'Bus Driver'

    # Custom method to retrieve bus_attendant from the related BusMaster model
    def get_bus_attendant(self, obj):
        return obj.bus_attendant
    get_bus_attendant.short_description = 'Bus Attendant'

    def submit_fee_data(self, request, queryset=None):
        if request.method == 'POST':
            form = FeeNotApplicableForm(request.POST)

            # Debugging: Print the POST data
            print("POST data:", request)

            if form.is_valid():
                fee_not_applicable_in_months = form.cleaned_data['fee_not_applicable_in_months']

                # Update all records with the selected month
                busfees_master.objects.all().update(fee_not_applicable_in_months=fee_not_applicable_in_months)
                self.message_user(request, "Fee data submitted successfully for all records.")
                return HttpResponseRedirect(request.get_full_path())
            else:
                # Debugging: Print form errors
                print("Form errors:", form.errors)
        else:
            form = FeeNotApplicableForm()

        return render(request, 'admin/submit_fee_form.html', {'form': form})




    submit_fee_data.short_description = "Submit Fee Data for All Records"

    actions = ['submit_fee_data']

admin.site.register(busfees_master, BusFeesMaster)

class BusMasterResource(resources.ModelResource):

    class Meta:
        model = bus_master
        fields = ("bus_route", "bus_driver", "bus_conductor","bus_attendant", "internal")
        export_order = ("bus_route", "bus_driver", "bus_conductor", "bus_conductor", "bus_attendant", "internal")

    bus_route = Field(attribute='bus_route', column_name='Bus Route')
    bus_driver = Field(attribute='bus_driver', column_name='Driver')
    bus_conductor = Field(attribute='bus_conductor', column_name='Conductor')
    bus_attendant = Field(attribute='bus_attendant', column_name='Attendant')
    internal = Field(attribute='internal', column_name='Internal/External')

    def dehydrate_internal(self, obj):
        # Custom logic for displaying "Internal" or "External"
        return "Internal" if str(obj.internal).upper() == "TRUE" else "External"


class BusMaster(ExportMixin, admin.ModelAdmin):
    # list_display = ("busdetail_id", "bus_route", "bus_driver", "bus_conductor", "bus_attendant", "driver_phone", "conductor_phone", "attendant_phone")
    resource_class = BusMasterResource
    list_display = ("bus_route", "bus_driver", "bus_conductor", "bus_attendant", "driver_phone", "conductor_phone", "attendant_phone")
    search_fields = ("bus_route", "bus_driver", "bus_conductor", "bus_attendant", "driver_phone", "conductor_phone", "attendant_phone")

admin.site.register(bus_master,BusMaster)


class ConcessionMasterForm(forms.ModelForm):
    PERCENTAGE_CHOICES = [
        ('percentage', 'Percentage'),
        ('amount', 'Amount'),
    ]
    concession_type = forms.CharField(
        label="Concession Type *",
        max_length=100,
    )
    concession_persent = forms.ChoiceField(
        choices=PERCENTAGE_CHOICES,
        widget=forms.RadioSelect,
        label="Concession Persent *",
    )
    is_april_checked = forms.BooleanField(
        label="April Concession",
        required=False
    )

    class Meta:
        model = concession_master
        fields = '__all__'

class ConcessionMasterAdmin(admin.ModelAdmin):
    list_display = ("concession_id", "concession_type", "concession_persent", "concession_amount", "is_april_checked")
    form = ConcessionMasterForm

admin.site.register(concession_master, ConcessionMasterAdmin)
admin.site.register(expense)

class FeesMasterDisplay(admin.ModelAdmin):
    list_display = ("fees_id", "class_no", "annual_fees", "tuition_fees", "funds_fees", "sports_fees", "activity_fees", "admission_fees", "dayboarding_fees", "miscellaneous_fees", "valid_from", "valid_to")

admin.site.register(fees_master,FeesMasterAdmin)


class LateFeeMasterForm(forms.ModelForm):
    listing = forms.CharField(widget=ReadOnlyCKEditorWidget(), required=False, label='')
    # Pay_In_Month_CHOICES = [(str(i), str(i)) for i in range(1, 91)]
    Pay_In_Month_CHOICES = [
        ('', 'Please Select Day'),  # Default option
    ] + [(str(i), str(i)) for i in range(1, 91)] + [
        ('till current date', 'Till Current Date')  # Custom option
    ]

    days_from = forms.ChoiceField(
        choices=Pay_In_Month_CHOICES,
        # label="Concession Persent *",
    )

    days_to = forms.ChoiceField(
        choices=Pay_In_Month_CHOICES,
        # label="Concession Persent *",
    )

    Latefee_Type_CHOICES = [
        ('', 'Select Type'),
        ('fixed', 'Fixed'),
        ('per day', 'Per Day'),
        ('no charge', 'No Charge'),
    ]

    latefee_type = forms.ChoiceField(
        choices=Latefee_Type_CHOICES,
        # widget=forms.RadioSelect,
        # label="Concession Persent *",
    )

    class Meta:
        model = latefee_master
        fields = '__all__'

    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Exclude non-numeric values and get existing ranges
        existing_ranges = latefee_master.objects.exclude(days_from__in=['', None, 'till current date']).exclude(days_to__in=['', None, 'till current date']).values_list('days_from', 'days_to')
        
        excluded_days = set()
        
        # Calculate excluded days only for numeric values
        for days_from, days_to in existing_ranges:
            try:
                excluded_days.update(range(int(days_from), int(days_to) + 1))
            except ValueError:
                continue  # Skip non-numeric values

        # Filter numeric choices and include custom options
        numeric_choices = [(str(i), str(i)) for i in range(1, 91) if i not in excluded_days]
        available_choices = [
            ('', 'Please Select Day'),
        ] + numeric_choices + [
            ('till current date', 'Till Current Date')
        ]
        
        self.fields['days_from'].choices = available_choices
        self.fields['days_from'].required = False  # Not required
        self.fields['days_to'].choices = available_choices
        self.fields['days_to'].required = False  # Not required

        # Generate the HTML table to display existing LateFeeMaster records
        records = latefee_master.objects.all()

        listing_html = """
            <h3>Existing Late Fees</h3>
            <table style='border: 1px solid #ddd; width: 100%; border-collapse: collapse;'>
                <thead>
                    <tr>
                        <th style='border: 1px solid #ddd; padding: 8px;'>Late Fee ID</th>
                        <th style='border: 1px solid #ddd; padding: 8px;'>Days From</th>
                        <th style='border: 1px solid #ddd; padding: 8px;'>Days To</th>
                        <th style='border: 1px solid #ddd; padding: 8px;'>Late Fee</th>
                        <th style='border: 1px solid #ddd; padding: 8px;'>Late Fee Type</th>
                        <th style='border: 1px solid #ddd; padding: 8px;'>Description</th>
                    </tr>
                </thead>
                <tbody>
        """
        
        for record in records:
            listing_html += f"""
                <tr>
                    <td style='border: 1px solid #ddd; padding: 8px;'>{record.latefee_id}</td>
                    <td style='border: 1px solid #ddd; padding: 8px;'>{record.days_from}</td>
                    <td style='border: 1px solid #ddd; padding: 8px;'>{record.days_to}</td>
                    <td style='border: 1px solid #ddd; padding: 8px;'>{record.latefee}</td>
                    <td style='border: 1px solid #ddd; padding: 8px;'>{record.latefee_type}</td>
                    <td style='border: 1px solid #ddd; padding: 8px;'>{record.latefee_desc}</td>
                </tr>
            """

        listing_html += """
                </tbody>
            </table>
        """

        # Assign the marked-safe HTML to the custom form field
        self.fields['listing'].initial = mark_safe(listing_html)

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
        
    #     # Get all existing ranges as integers, ignoring non-numeric values
    #     existing_ranges = latefee_master.objects.exclude(days_from='').exclude(days_from=None).exclude(days_to='').exclude(days_to=None).values_list('days_from', 'days_to')
    #     excluded_days = set()
        
    #     # Calculate excluded days only for numeric values
    #     for r in existing_ranges:
    #         try:
    #             days_from = int(r[0])
    #             days_to = int(r[1])
    #             excluded_days.update(range(days_from, days_to + 1))
    #         except ValueError:
    #             # Skip non-numeric values
    #             continue
        
    #     # Filter choices and convert to strings
    #     available_choices = [(str(i), str(i)) for i in range(1, 91) if i not in excluded_days]
        
    #     self.fields['days_from'].choices = available_choices
    #     self.fields['days_to'].choices = available_choices

class LateFeeMasterDisplay(admin.ModelAdmin):
    form = LateFeeMasterForm
    list_display = ("days_from", "days_to", "latefee", "latefee_type", "latefee_desc")

admin.site.register(latefee_master, LateFeeMasterDisplay)


# admin.site.register(latefee_master)


class PaymentScheduleMasterForm(forms.ModelForm):

    schedule_list = forms.CharField(widget=ReadOnlyCKEditorWidget(), required=False, label='Existing Payment Schedules')
    
    fees_for_months = forms.MultipleChoiceField(
        choices=payment_schedule_master.Fees_For_Month_CHOICES,
    )

    Pay_In_Month_CHOICES = [
        ('', 'Choose The Month'),
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
        ('4', '4'),
        ('5', '5'),
        ('6', '6'),
        ('7', '7'),
        ('8', '8'),
        ('9', '9'),
        ('10', '10'),
        ('11', '11'),
        ('12', '12')
    ]
   
    pay_in_month = forms.ChoiceField(
        choices=Pay_In_Month_CHOICES,
        # widget=forms.RadioSelect,
        label="Pay In Month *",
    )

    Payment_Date_CHOICES = [
        ('', 'Choose The Date'),
        ('01', '01'),
        ('02', '02'),
        ('03', '03'),
        ('04', '04'),
        ('05', '05'),
        ('06', '06'),
        ('07', '07'),
        ('08', '08'),
        ('09', '09'),
        ('10', '10'),
        ('11', '11'),
        ('12', '12'),
        ('13', '13'),
        ('14', '14'),
        ('15', '15'),
        ('16', '16'),
        ('17', '17'),
        ('18', '18'),
        ('19', '19'),
        ('20', '20'),
        ('21', '21'),
        ('22', '22'),
        ('23', '23'),
        ('24', '24'),
        ('25', '25'),
        ('26', '26'),
        ('27', '27'),
        ('28', '28'),
        ('29', '29'),
        ('30', '30'),
        ('31', '31'),
    ]
   
    payment_date = forms.ChoiceField(
        choices=Payment_Date_CHOICES,
        # widget=forms.RadioSelect,
        label="Payment Date *",
    )

   

    class Meta:
        model = payment_schedule_master
        fields = '__all__'


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        instance = kwargs.get('instance')

        schedules = payment_schedule_master.objects.all()
        schedule_list_html = """
            <h3>Existing Payment Schedules</h3>
            <table style='border: 1px solid #ddd; width: 100%; border-collapse: collapse;'>
                <thead>
                    <tr>
                        <th style='border: 1px solid #ddd; padding: 8px;'>Schedule ID</th>
                        <th style='border: 1px solid #ddd; padding: 8px;'>Fees for Months</th>
                        <th style='border: 1px solid #ddd; padding: 8px;'>Pay in Month</th>
                        <th style='border: 1px solid #ddd; padding: 8px;'>Payment Date</th>
                    </tr>
                </thead>
                <tbody>
        """
        
        for schedule in schedules:
            schedule_list_html += f"""
                <tr>
                    <td style='border: 1px solid #ddd; padding: 8px;'>{schedule.schedule_id}</td>
                    <td style='border: 1px solid #ddd; padding: 8px;'>{schedule.fees_for_months}</td>
                    <td style='border: 1px solid #ddd; padding: 8px;'>{schedule.pay_in_month}</td>
                    <td style='border: 1px solid #ddd; padding: 8px;'>{schedule.payment_date}</td>
                </tr>
            """

        schedule_list_html += """
                </tbody>
            </table>
        """

        # Assign the marked-safe HTML to the custom form field
        self.fields['schedule_list'].initial = mark_safe(schedule_list_html)

        # Gather all used months from other records
        used_months = set()
        all_schedules = payment_schedule_master.objects.all()

        if instance:
            all_schedules = all_schedules.exclude(pk=instance.pk)
            # Add the selected months of the current instance to the used months set
            current_months = set(instance.fees_for_months.split(','))
        else:
            current_months = set()

        for schedule in all_schedules:
            used_months.update(schedule.fees_for_months.split(','))

        # The available choices should include the months used by this instance + months not used by other records
        available_choices = [
            (value, label) for value, label in self.fields['fees_for_months'].choices 
            if value in current_months or value not in used_months
        ]
        self.fields['fees_for_months'].choices = available_choices
    
    def clean_fees_for_months(self):
        selected_months = self.cleaned_data['fees_for_months']
        # Convert the list of selected months into a comma-separated string
        return ','.join(selected_months)
    
    

class PaymentScheduleMasterAdmin(admin.ModelAdmin):
    form = PaymentScheduleMasterForm
    list_display = ("fees_for_months", "pay_in_month", "payment_date")
    search_fields = ("fees_for_months", "pay_in_month", "payment_date")
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        return form

    



admin.site.register(payment_schedule_master, PaymentScheduleMasterAdmin)

# admin.site.register(payment_schedule_master)
admin.site.register(specialfee_master)
    
class ButtonWidget(forms.Widget):
    def render(self, name, value, attrs=None, renderer=None):
        return mark_safe(f'<button type="button" id="search-button">Search</button>')

class StudentClassAdminForm(forms.ModelForm):
    student_name = forms.CharField(required=False, label="Student Name")
    admission_no = forms.IntegerField(required=False, label="Admission")
    search_button = forms.CharField(widget=ButtonWidget(), required=False)
    search_results = forms.ModelChoiceField(queryset=student_master.objects.none(), required=False,blank=True, label="Select Student")
    display_admission_no = forms.IntegerField(required=False, label="Admission No")
    display_student_name = forms.CharField(required=False, label="Student Name")

    class Meta:
        model = student_class
        fields = ['student_name', 'admission_no', 'search_button', 'search_results', 'student_id', 'display_admission_no', 'display_student_name', 'class_no', 'section', 'started_on', 'ended_on']

    class Media:
        js = ('app/js/student_class.js',)
        css = {
            'all': ('app/css/custom_admin.css',)  # Add your custom CSS file here
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['search_results'].queryset = student_master.objects.none()
        # self.fields['student_id'].widget.attrs['disabled'] = True
        self.fields['display_admission_no'].widget.attrs['disabled'] = True
        self.fields['display_student_name'].widget.attrs['disabled'] = True

        if self.instance and self.instance.pk:
            # Editing existing instance, hide search fields
            self.fields['student_name'].widget = forms.HiddenInput()
            self.fields['admission_no'].widget = forms.HiddenInput()
            self.fields['search_button'].widget = forms.HiddenInput()
            self.fields['search_results'].widget = forms.HiddenInput()
            # Get the related student_id
            student_id = self.instance.student_id
            if student_id:
                # Fetch the related student_master instance
                student = student_master.objects.get(student_id=student_id)
                # Populate the fields with the related student's details
                self.fields['display_admission_no'].initial = student.addmission_no
                self.fields['display_student_name'].initial = student.student_name
                # self.fields['search_results'].queryset = student_master.objects.filter(student_id=student_id)
                # self.fields['search_results'].initial = student_id  # Set initial value for dropdown

        if self.is_bound and self.data.get('search_results'):
            student_id = self.data.get('search_results')
            if student_id:
                self.fields['search_results'].queryset = student_master.objects.filter(student_id=student_id)

class StudentClassAdmin(admin.ModelAdmin):
    list_display = ("student_class_id", "student_id", "class_no", "section", "started_on", "ended_on")
    search_fields = ('student_id', 'class_no', 'section')
    form = StudentClassAdminForm

    # def save_model(self, request, obj, form, change):
    #     if 'student_id' in form.cleaned_data:
    #         # Ensure the student_id is retained even if the field is readonly
    #         obj.student_id = form.cleaned_data['student_id']
    #     super().save_model(request, obj, form, change)

    def get_fieldsets(self, request, obj=None):
        if obj:  # Editing an existing student_class
            return [
                (None, {
                    'fields': ('student_id', 'display_admission_no', 'display_student_name', 'class_no', 'section', 'started_on', 'ended_on'),
                }),
            ]
        else:  # Adding a new student_class
            return [
                ('Student Search', {
                    'classes': ('box',),  # Custom class to style the box
                    'fields': ('student_name', 'admission_no', 'search_button', 'search_results'),
                }),
                (None, {
                    'fields': ('student_id', 'display_admission_no', 'display_student_name', 'class_no', 'section', 'started_on', 'ended_on'),
                }),
            ]

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('ajax/load-students/', self.admin_site.admin_view(self.load_students), name='ajax_load_students'),
            path('ajax/get-student/', self.admin_site.admin_view(self.get_student), name='ajax_get_student'),
        ]
        return custom_urls + urls
    
    def get_student(self, request):
        student_id = request.GET.get('student_id', '')
        print("++++++ student_id +++++++++", student_id)
        if student_id:
            student = student_master.objects.get(student_id=student_id)
            return JsonResponse({'student_id': student.student_id,'student_name':student.student_name,'admission_no':student.addmission_no})
        return JsonResponse({'error': 'Student not found'}, status=404)

    def load_students(self, request):
        student_name = request.GET.get('student_name', '')
        admission_no = request.GET.get('admission_no', '')
        queryset = student_master.objects.all()

        if student_name:
            queryset = queryset.filter(student_name__icontains=student_name)
        if admission_no:
            queryset = queryset.filter(addmission_no=admission_no)
        results = list(queryset.values('student_id', 'student_name', 'addmission_no'))
        return JsonResponse(results, safe=False)

    class Media:
        js = ('app/js/student_class.js',)


admin.site.register(student_class,StudentClassAdmin)


class StudentFeesAdminForm(forms.ModelForm):

    class Meta:
        model = student_fee
        fields = '__all__'

    # student_id = forms.ModelChoiceField(queryset=student_master.objects.all())
    # Define current year at the top
    current_year = datetime.now().year

    # Existing fields
    student_name = forms.CharField(label="Student Name", required=False)
    admission_no = forms.CharField(label="Admission Number", required=False)
    class_no = forms.ChoiceField(choices=CLASS_CHOICES, required=False, label="Class")
    section = forms.ChoiceField(choices=SECTION, required=False, label="Section")
    search_button = forms.CharField(widget=forms.TextInput(attrs={'type': 'button', 'value': 'Find Student'}), label='', required=False)
    search_results = forms.ModelChoiceField(queryset=student_master.objects.none(), required=False, blank=True, label="Select Student")
    
    # Student detail fields
    student_id = forms.IntegerField(widget=forms.HiddenInput(), required=False)
    display_admission_no = forms.CharField(required=False, label="Admission No", widget=forms.TextInput(attrs={'readonly': 'readonly'}))
    display_student_name = forms.CharField(required=False, label="Student Name", widget=forms.TextInput(attrs={'readonly': 'readonly'}))
    display_father_name = forms.CharField(required=False, label="Father Name", widget=forms.TextInput(attrs={'readonly': 'readonly'}))
    display_student_class = forms.CharField(required=False, label="Student Class", widget=forms.TextInput(attrs={'readonly': 'readonly'}))
    display_student_section = forms.CharField(required=False, label="Student Section", widget=forms.TextInput(attrs={'readonly': 'readonly'}))
    display_year = forms.ChoiceField(
        choices=[(str(year), str(year)) for year in range(current_year - 1, current_year + 2)],
        required=False, 
        label="Year", 
        widget=forms.Select()
    )

    # Fees section fields
    # fees_for_months = forms.CharField(label="Fees For Months", required=False)
    # fees_period_month = forms.CharField(label="Fees Period Month", required=False)
    # Define the multiple choice fields for fees_for_months and fees_period_month
    fees_for_months = forms.MultipleChoiceField(
        choices=FEE_MONTHS_CHOICES,  # Populate with dynamic data if needed
        required=False,
        label="Fees for Months",
        widget=forms.SelectMultiple(attrs={'style': 'width:165px', 'id': 'id_fees_for_months'})
    )
    
    fees_period_month = forms.MultipleChoiceField(
        choices=[],  # Initially empty, will be populated by JavaScript
        required=False,
        label="Fees Period Month",
        widget=forms.SelectMultiple(attrs={'style': 'width:160px; height:50px','id': 'id_fees_period_month'})
    )
    annual_fees_paid = forms.DecimalField(label="Annual Fees Paid", required=False)
    tuition_fees_paid = forms.DecimalField(label="Tuition Fees Paid", required=False)
    funds_fees_paid = forms.DecimalField(label="Funds Fees Paid", required=False)
    sports_fees_paid = forms.DecimalField(label="Sports Fees Paid", required=False)
    activity_fees = forms.DecimalField(label="Activity Fees", required=False)
    admission_fees_paid = forms.DecimalField(label="Admission Fees Paid", required=False)
    miscellaneous_fees_paid = forms.DecimalField(label="Miscellaneous Fees Paid", required=False)
    late_fees_paid = forms.DecimalField(label="Late Fees Paid", required=False)
    dayboarding_fees_paid = forms.DecimalField(label="Dayboarding Fees Paid", required=False)
    bus_fees_paid = forms.DecimalField(label="Bus Fees Paid", required=False)
    concession_type = forms.CharField(label="Concession Type", required=False)
    concession_applied = forms.DecimalField(label="Concession Applied", required=False)
    total_amount = forms.DecimalField(label="Total Amount", required=False)


    # Payment Section
    date_payment = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), label="Date Payment", required=False)
    payment_mode = forms.ChoiceField(choices=PAYMENT_MODE_CHOICES, label="Payment Mode", required=False)
    cheque_no = forms.CharField(label="Cheque No", required=False)
    bank_name = forms.ChoiceField(choices=BANK_CHOICES, label="Bank Name", required=False)
    branch_name = forms.CharField(label="Branch Name", required=False)
    amount_paid = forms.DecimalField(label="Amount Paid", required=False)
    realized_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), label="Realized Date", required=False)
    cheque_status = forms.ChoiceField(choices=CHEQUE_STATUS_CHOICES, label="Cheque Status", required=False)
    remarks = forms.CharField(widget=forms.Textarea, label="Remarks", required=False)

     # Previous Fees Record
    previous_fees_record = forms.CharField(widget=forms.HiddenInput(), required=False)  # This can be a hidden input for custom HTML rendering

    class Media:
        js = ('app/js/student_fees.js',)  # Adjust the path as necessary
        css = {
            'all': ('app/css/custom_admin.css',)  # Add your custom CSS file here
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        print("======= I'M HERE ===========")

        self.fields['search_results'].queryset = student_master.objects.none()

        # Calculate the current quarter based on the current month
        current_month = datetime.now().month
        if 4 <= current_month <= 6:
            default_quarter = '4,5,6'  # April - June
        elif 7 <= current_month <= 9:
            default_quarter = '7,8,9'  # July - September
        elif 10 <= current_month <= 12:
            default_quarter = '10,11,12'  # October - December
        else:
            default_quarter = '1,2,3'  # January - March

        # Set the default value for fees_for_months
        self.fields['fees_for_months'].initial = default_quarter

        
        if self.instance and self.instance.pk:

            # Assuming 'student_id' is being passed in the form data
            student_id  = student_master.objects.get(pk=student_id)

            # Print the value and type of student_id
            # logger.debug(f"Student ID: {student_id}, Type: {type(student_id)}")

            self.fields['student_name'].widget = forms.HiddenInput()
            self.fields['admission_no'].widget = forms.HiddenInput()
            self.fields['class_no'].widget = forms.HiddenInput()
            self.fields['section'].widget = forms.HiddenInput()
            self.fields['search_results'].widget = forms.HiddenInput()

            
            if student_id:

                student = student_master.objects.get(student_id=student_id)
                self.fields['display_admission_no'].initial = student.admission_no
                self.fields['display_student_name'].initial = student.student_name
                self.fields['display_father_name'].initial = student.father_name
                self.fields['display_student_class'].initial = student.student_class
                self.fields['display_student_section'].initial = student.student_section
                self.fields['display_year'].initial = student.selected_year

                # Set hidden student_id value
                self.fields['student_id'].initial = student_id

                

        if self.is_bound and self.data.get('search_results'):
            student_id = self.data.get('search_results')
            if student_id:
                self.fields['search_results'].queryset = student_master.objects.filter(student_id=student_id)

class StudentFeesAdmin(admin.ModelAdmin):

    
    
    form = StudentFeesAdminForm

    fieldsets = (
        ('Search Student', {
            'fields': (
                'student_name',
                'admission_no',
                'class_no',
                'section',
                'search_button',
            ),
            'classes': ('half-width-container',),  # Custom CSS class
        }),
        ('Previous Fees Record', {
            'fields': ('previous_fees_record',),
            'classes': ('collapse',),  # Optional: to initially collapse the section
        }),
        ('Selected Student Details', {
            'fields': (
                'display_admission_no',
                'display_student_name',
                'display_father_name',
                'display_student_class',
                'display_student_section',
                'display_year',
                'student_id',
            ),
            'classes': ('half-width-container',),  # Custom CSS class
        }),
         ('Fees Section', {
            'fields': ('fees_for_months', 'fees_period_month', 'annual_fees_paid', 'tuition_fees_paid', 'funds_fees_paid', 'sports_fees_paid', 'activity_fees', 'admission_fees_paid', 'miscellaneous_fees_paid', 'late_fees_paid', 'dayboarding_fees_paid', 'bus_fees_paid', 'concession_type', 'concession_applied', 'total_amount'),
        }),
        ('Payment Section', {
            'fields': ('date_payment', 'payment_mode', 'cheque_no', 'bank_name', 'branch_name', 'amount_paid', 'realized_date', 'cheque_status', 'remarks')
        }),
         
    )

    # change_form_template = 'admin/student_fee/change_form.html'

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('ajax/load-students/', self.admin_site.admin_view(self.load_students), name='ajax_load_students'),
            path('ajax/get-student/', self.admin_site.admin_view(self.get_student), name='ajax_get_student'),
            path('ajax/prev-fees/', self.admin_site.admin_view(self.prev_fees), name='ajax_prev_fees'),
            path('ajax/calculate-fees/', self.admin_site.admin_view(self.calculate_fees), name='ajax_calculate_fees'),
            path('ajax/pay-fees/', self.admin_site.admin_view(self.action_payfees), name='ajax_action_payfees'),
        ]
        return custom_urls + urls
    

    def load_students(self, request):
        if request.method == 'GET':
            admission_no = request.GET.get('admission_no')
            class_no = request.GET.get('class_no')
            section = request.GET.get('section')
            student_name = request.GET.get('student_name')
            
            # Base query
            students = student_master.objects.distinct()

            # Apply filters based on the provided parameters
            if admission_no:
                students = students.filter(addmission_no=admission_no)
            if student_name:
                students = students.filter(student_name__istartswith=student_name)

            # Create the final response
            student_data = []
            for student in students:
                # Filter related student classes
                latest_class = student_class.objects.filter(
                    student_id=student.student_id
                ).order_by('-student_class_id').first()

                if latest_class and (not class_no or latest_class.class_no == class_no):
                    student_data.append({
                        'student_id': student.student_id,
                        'student_name': student.student_name,
                        'class_no': latest_class.class_no
                    })

            # Convert the student_data list into the desired format
            formatted_data = ','.join([f"{d['student_id']}${d['student_name']}:{d['class_no']}" for d in student_data])

            return JsonResponse({'data': formatted_data})
        
        return JsonResponse({'error': 'Bad Request'}, status=400)

    # Get student
    def get_student(self, request):
        if request.method == 'GET':
            student_id = request.GET.get('student_id')
            if not student_id:
                return JsonResponse({'error': 'Student ID not provided'}, status=400)

            with connection.cursor() as cursor:
                # Query 1: Get the maximum student_class_id
                cursor.execute("""
                    SELECT MAX(student_class_id)
                    FROM student_classes
                    WHERE student_id = %s
                """, [student_id])
                row1 = cursor.fetchone()
                if row1:
                    stuclsid = row1[0]
                else:
                    return JsonResponse({'error': 'Student class not found'}, status=404)

                # Query 2: Get class_no, section, and started_on based on student_class_id
                cursor.execute("""
                    SELECT class_no, section, started_on
                    FROM student_classes
                    WHERE student_class_id = %s
                """, [stuclsid])
                row2 = cursor.fetchone()
                if row2:
                    stucls, section, started_on = row2
                else:
                    return JsonResponse({'error': 'Student class details not found'}, status=404)

                # Query 3: Get student details
                cursor.execute("""
                    SELECT addmission_no, student_id, student_name, father_name
                    FROM student_master
                    WHERE student_id = %s
                """, [student_id])
                row3 = cursor.fetchone()
                if row3:
                    stuadm, stuid, stuname, stufather = row3
                else:
                    return JsonResponse({'error': 'Student details not found'}, status=404)

                # Format the details including started_on
                details = f"{stuid}${stucls}${stuname}${section}${stufather}${stuadm}${started_on}"

                #return HttpResponse(details)
                return JsonResponse({'data': details})
        else:
            return HttpResponse(status=400)

    # Previous fees 
    def prev_fees(self, request):
        if request.method == 'GET':
            student_id = request.GET.get('student_id')
            if not student_id:
                return JsonResponse({'error': 'Student ID not provided'}, status=400)
            # Get the max class ID for the student
            max_class_id = student_class.objects.filter(student_id=student_id).aggregate(Max('student_class_id'))['student_class_id__max']

            # Get the current class number
            current_class = student_class.objects.filter(student_class_id=max_class_id).values_list('class_no', flat=True).first()

            # Fetch all previous fees for the student, ordered by payment date
            previous_fees = student_fee.objects.filter(student_id=student_id).order_by('-date_payment')

            # Prepare the response
            fees_data = []
            for fee in previous_fees:
                fees_data.append(f"{fee.fees_for_months}${fee.date_payment}${fee.amount_paid}${fee.fees_period_month}${fee.student_class}")

            # Return the data as a JSON response
            return JsonResponse({
                'success': True,
                'data': '&'.join(fees_data),
            })
        else:
            return JsonResponse({'success': False, 'message': 'Invalid request method'})
    
    # Calculate fees
    def calculate_fees(self, request):
        if request.method == "GET":
            sid = request.GET.get("sid")
            cls = request.GET.get("cls")
            mf = request.GET.get("mf")
            yr = request.GET.get("yr")

        # Validate that required parameters are provided
        if not sid:
            return JsonResponse({"error": "Student ID not provided"}, status=400)
        if not cls:
            return JsonResponse({"error": "Class not provided"}, status=400)
        if not mf:
            return JsonResponse({"error": "Month not provided"}, status=400)
        if not yr:
            return JsonResponse({"error": "Year not provided"}, status=400)

        # Fetch previous payment record
        previous_fee_info = last_payment_record(sid)
        include_admission_fee = (
            previous_fee_info is None
        )  # Include admission fee if no previous record exists
        pay_months = mf
        months_in_quarters = ["4,5,6", "7,8,9", "10,11,12", "1,2,3"]

        target_months = pay_months
        target_months_array = target_months.split(",")
        quarters = []

        for quarter in months_in_quarters:
            quarter_months = quarter.split(",")
            intersection = list(set(quarter_months) & set(target_months_array))

            if intersection:
                quarters.append(
                    {
                        "quarter": quarter,
                        "months_paid": ",".join(intersection),
                    }
                )

        student_id = sid
        class_no = cls
        year = yr
        total_fees_payable = 0

        fee_details = fetch_fee_details_for_class(student_id, class_no)
        current_payment_details_array = []

        if fee_details:
            current_payment_details = {
                "class_no": class_no,
                "annual_fees": fee_details['annual_fees'],
                "tuition_fees": fee_details['tuition_fees'],
                "funds_fees": fee_details['funds_fees'],
                "sports_fees": fee_details['sports_fees'],
                "admission_fees": fee_details['admission_fees'],
                "security_fees": fee_details['security_fees'],
                "dayboarding_fees": fee_details['dayboarding_fees'],
                "miscellaneous_fees": fee_details['miscellaneous_fees'],
                "bus_fees": fee_details['bus_fees'],
                "busfee_not_applicable_in_months": fee_details['busfee_not_applicable_in_months'],
                "bus_id": fee_details['bus_id'],
                "concession_percent": fee_details['concession_percent'],
                "concession_type": fee_details['concession_type'],
                "activity_fees": fee_details['activity_fees'],
                "activity_fees_mandatory": fee_details['activity_fees_mandatory'],
                "concession_amount": fee_details['concession_amount'],
                "concession_id": fee_details['concession_id'],
                "is_april_checked": fee_details['is_april_checked'],
                "concession_applied": 0,
            }

            for quarter in quarters:
                current_date = datetime.now().strftime("%Y-%m-%d")  # Example current date
                fees_for_months = quarter["quarter"]
                months_paid_for = quarter["months_paid"]
                payment_details = current_payment_details.copy()
                payment_details["fees_for_months"] = fees_for_months
                payment_details["fees_period_month"] = months_paid_for

                total = 0
                if include_admission_fee:
                    # total = payment_details['admission_fees']
                    include_admission_fee = False
                else:
                    payment_details["admission_fees"] = 0

                fields_to_calculate = [
                    "tuition_fees",
                    "funds_fees",
                    "sports_fees",
                    "bus_fees",
                    "activity_fees",
                    "dayboarding_fees",
                    "miscellaneous_fees",
                    "annual_fees",
                    "admission_fees",
                ]

                activity_fees_mandatory = payment_details["activity_fees_mandatory"]
                fees_for_months_array = payment_details["fees_period_month"].split(",")

                for field in fields_to_calculate:
                    numeric_value = (
                        float(payment_details[field])
                        if isinstance(payment_details[field], (int, float))
                        else 0
                    )

                    if field == "activity_fees":
                        activity_fee_applicable = get_special_fee(
                            student_id, year, payment_details["fees_period_month"], field
                        )
                        if activity_fee_applicable is not None:
                            numeric_value = activity_fee_applicable
                        elif activity_fees_mandatory != 1:
                            numeric_value = 0
                    elif field == "bus_fees":
                        not_applicable_months_array = (
                            payment_details["busfee_not_applicable_in_months"].split(",")
                            if payment_details["busfee_not_applicable_in_months"]
                            else []
                        )
                        overlap_months = list(
                            set(not_applicable_months_array) & set(fees_for_months_array)
                        )
                        applicable_months = list(
                            set(fees_for_months_array) - set(overlap_months)
                        )
                        bus_fee_applied = 0
                        if applicable_months:
                            bus_fee_for_applicable_months = get_special_fee(
                                student_id, year, ",".join(applicable_months), "bus_fees"
                            )
                            for month in applicable_months:
                                bus_fees_value = payment_details.get("bus_fees", 0)  # Default to 0 if not present
                                if bus_fees_value is None:  # Explicitly check for None
                                    bus_fees_value = 0
                                bus_fee_applied += bus_fee_for_applicable_months.get(month, int(bus_fees_value))
                            numeric_value = bus_fee_applied

                    elif numeric_value > 0 and field in ["tuition_fees", "funds_fees"]:
                        fee_applicable = get_special_fee(
                            student_id, year, payment_details["fees_for_months"], field
                        )
                        if fee_applicable:
                            numeric_value = float(fee_applicable)
                        numeric_value *= len(fees_for_months_array)
                    elif field in [
                        "annual_fees",
                        "miscellaneous_fees",
                        "sports_fees",
                        "admission_fees",
                    ]:
                        if fees_for_months == "4,5,6":
                            fee_applicable = get_special_fee(
                                student_id, year, payment_details["fees_for_months"], field
                            )
                            if fee_applicable:
                                numeric_value = float(fee_applicable)
                        else:
                            numeric_value = 0

                    payment_details[field] = numeric_value
                    total += numeric_value

                concession_amount = 0
                if payment_details["concession_percent"] == "percentage":
                    concession_percent = float(payment_details["concession_amount"])
                    tuition_fees = float(payment_details["tuition_fees"])
                    concession_amount = (tuition_fees * concession_percent) / 100
                elif payment_details["concession_percent"] == "amount":
                    concession_amount = float(payment_details["concession_amount"])

                if (
                    "4" in fees_for_months_array
                    and concession_amount > 0
                    and payment_details["is_april_checked"] == 0
                ):
                    concession_amount = (concession_amount / len(fees_for_months_array)) * (
                        len(fees_for_months_array) - 1
                    )
                    concession_amount = round(concession_amount)

                total -= concession_amount
                payment_details["concession_applied"] = concession_amount

                late_fee = calculate_late_fee(total, fees_for_months, year, current_date)
                payment_details["late_fee"] = late_fee
                total += late_fee
                payment_details["total_fee"] = total
                payment_details["year"] = year
                total_fees_payable += total

                current_payment_details_array.append(payment_details)

        sum_dict = {
            "annual_fees": 0,
            "tuition_fees": 0,
            "funds_fees": 0,
            "sports_fees": 0,
            "activity_fees": 0,
            "admission_fees": 0,
            "security_fees": 0,
            "dayboarding_fees": 0,
            "miscellaneous_fees": 0,
            "bus_fees": 0,
            "concession_amount": 0,
            "concession_applied": 0,
            "concession_percent": "",
            "concession_type_id": "",
            "concession_type": "",
            "late_fee": 0,
            "total_fee": 0,
        }

        sum_keys = [
            "annual_fees",
            "tuition_fees",
            "funds_fees",
            "sports_fees",
            "activity_fees",
            "admission_fees",
            "security_fees",
            "dayboarding_fees",
            "miscellaneous_fees",
            "bus_fees",
            "concession_applied",
            "late_fee",
            "total_fee",
        ]

        excluded_keys = [
            "concession_amount",
            "concession_percent",
            "concession_id",
            "concession_type",
        ]

        for details in current_payment_details_array:
            for key in sum_keys:
                sum_dict[key] += details[key]
                print(f"Updated {key}: {sum_dict[key]}")

            for key in excluded_keys:
                sum_dict[key] = details[key]
                print(f"Set {key}: {sum_dict[key]}")

        response_data = "|".join([str(sum_dict[key]) for key in sum_keys])

        # return JsonResponse(response_data, safe=False)
        return JsonResponse({
                'success': True,
                'data': response_data,
            })

    def action_payfees(self, request):
        fm = request.GET.get('fm')
        sid = request.GET.get('sid')
        today = datetime.today().strftime("%Y-%m-%d")
        date = today.split("-")

        with connection.cursor() as cursor:
            # Query 1: Get payment schedule master data
            cursor.execute("SELECT * FROM payment_schedule_master WHERE fees_for_months = %s", [fm])
            query = cursor.fetchone()
            if query:
                # Constructing the data string as you expect
                data = f"{query[1]}${query[2]}${query[3]}"
                payment_date = f"{date[0]}-{query[2]}-{query[3]}"
            
                # Calculate the date difference in days
                now = int(time.mktime(datetime.today().timetuple()))
                your_date = int(time.mktime(datetime.strptime(payment_date, "%Y-%m-%d").timetuple()))
                days = (now - your_date) // (60 * 60 * 24)

                # Query 2: Get late fee
                cursor.execute("SELECT * FROM latefee_master WHERE days_from <= %s AND days_to >= %s", [days, days])
                query1 = cursor.fetchone()
                lf = days * query1[3] if query1 else 0

                # Query 3: Get student data and concession details
                cursor.execute("""
                    SELECT a.*, c.cp, c.ct, c.ca FROM student_master a
                    LEFT JOIN (
                        SELECT concession_id, concession_type as ct, concession_persent as cp, concession_amount as ca 
                        FROM concession_master
                    ) as c ON a.concession_id = c.concession_id
                    WHERE a.student_id = %s
                """, [sid])
                query2 = cursor.fetchone()

                if query2:
                    # Constructing the expected output string
                    concession_percent = query2[18] if query2[18] is not None else "None"
                    concession_amount = query2[20] if query2[20] is not None else "None"
                    
                    detail = f"{data}&{lf}&{concession_percent}&{concession_amount}&"
                    # return JsonResponse(detail, safe=False)  # Returning as a string
                    return JsonResponse({
                        'success': True,
                        'data': detail,
                    })
                else:
                    return JsonResponse({"error": "Student not found"}, status=404)
            else:
                return JsonResponse({"error": "Payment schedule not found"}, status=404)


    # def save_model(self, request, obj, form, change):
    #     if not change:  # Only on creation
    #         student_id = form.cleaned_data.get('student_id')
    #         if student_id:
    #             try:
    #                 student = student_master.objects.get(pk=student_id)
    #                 obj.student_id = student
    #             except student_master.DoesNotExist:
    #                 raise ValueError("Student does not exist.")
    #     super().save_model(request, obj, form, change)

    def save_model(self, request, obj, form, change):
        if not change:  # Only on creation
            # Example of setting additional fields
            obj.added_by = request.user.username
            obj.entry_date = timezone.now()
        super().save_model(request, obj, form, change)

    class Media:
        
        js = ('app/js/student_fees.js',)

admin.site.register(student_fee,StudentFeesAdmin)
# admin.site.register(student_fee)


# class ClassFilter(admin.SimpleListFilter):
#     title = 'Class'
#     parameter_name = 'class_no'

#     def lookups(self, request, model_admin):
#         classes = student_class.objects.values_list('class_no', flat=True).distinct()
#         return [(class_no, class_no) for class_no in classes]

#     def queryset(self, request, queryset):
#         if self.value():
#             return queryset.filter(student_id__in=student_class.objects.filter(class_no=self.value()).values('student_id'))
#         return queryset


# class SectionFilter(admin.SimpleListFilter):
#     title = 'Section'
#     parameter_name = 'section'

#     def lookups(self, request, model_admin):
#         sections = student_class.objects.values_list('section', flat=True).distinct()
#         return [(section, section) for section in sections]

#     def queryset(self, request, queryset):
#         if self.value():
#             return queryset.filter(student_id__in=student_class.objects.filter(section=self.value()).values('student_id'))
#         return queryset


# class GenerateMobileNumbersListAdmin(admin.ModelAdmin):
#     list_display = ('addmission_no', 'student_name', 'get_class_no', 'get_section', 'mobile_no')
#     list_filter = (ClassFilter, SectionFilter)  # Custom filters for class and section

#     def get_class_no(self, obj):
#         student_class_instance = student_class.objects.filter(student_id=obj.student_id).order_by('-started_on').first()
#         return student_class_instance.class_no if student_class_instance else None
#     get_class_no.short_description = 'Class'

#     def get_section(self, obj):
#         student_class_instance = student_class.objects.filter(student_id=obj.student_id).order_by('-started_on').first()
#         return student_class_instance.section if student_class_instance else None
#     get_section.short_description = 'Section'

# class ClassFilter(admin.SimpleListFilter):
#     title = 'Class'
#     parameter_name = 'class_no'

#     def lookups(self, request, model_admin):
#         classes = student_class.objects.values_list('class_no', flat=True).distinct()
#         return [(class_no, class_no) for class_no in classes]

#     def queryset(self, request, queryset):
#         if self.value():
#             return queryset.filter(student_id__in=student_class.objects.filter(class_no=self.value()).values('student_id'))
#         return queryset  # Return original queryset, but it will be handled by SectionFilter


# class SectionFilter(admin.SimpleListFilter):
#     title = 'Section'
#     parameter_name = 'section'

#     def lookups(self, request, model_admin):
#         sections = student_class.objects.values_list('section', flat=True).distinct()
#         return [(section, section) for section in sections]

#     def queryset(self, request, queryset):
#         if self.value():
#             return queryset.filter(student_id__in=student_class.objects.filter(section=self.value()).values('student_id'))
#         return queryset  # Return original queryset, but it will be handled by ClassFilter


# class GenerateMobileNumbersListAdmin(admin.ModelAdmin):
#     list_display = ('addmission_no', 'student_name', 'get_class_no', 'get_section', 'mobile_no')
#     list_filter = (ClassFilter, SectionFilter)  # Custom filters for class and section

#     def get_class_no(self, obj):
#         student_class_instance = student_class.objects.filter(student_id=obj.student_id).order_by('-started_on').first()
#         return student_class_instance.class_no if student_class_instance else None
#     get_class_no.short_description = 'Class'

#     def get_section(self, obj):
#         student_class_instance = student_class.objects.filter(student_id=obj.student_id).order_by('-started_on').first()
#         return student_class_instance.section if student_class_instance else None
#     get_section.short_description = 'Section'

#     def get_queryset(self, request):
#         queryset = super().get_queryset(request)
#         # Get filter values
#         class_no = request.GET.get('class_no')
#         section = request.GET.get('section')
        
#         if not class_no and not section:
#             # Return empty queryset if no filters are selected
#             return queryset.none()

#         # Apply filters if any are selected
#         if class_no:
#             queryset = queryset.filter(student_id__in=student_class.objects.filter(class_no=class_no).values('student_id'))
#         if section:
#             queryset = queryset.filter(student_id__in=student_class.objects.filter(section=section).values('student_id'))
        
#         return queryset

# from django.contrib import admin

# class ClassFilter(admin.SimpleListFilter):
#     title = 'Class'
#     parameter_name = 'class_no'

#     def lookups(self, request, model_admin):
#         classes = student_class.objects.values_list('class_no', flat=True).distinct()
#         return [(class_no, class_no) for class_no in classes]

#     def queryset(self, request, queryset):
#         if self.value():
#             return queryset.filter(student_id__in=student_class.objects.filter(class_no=self.value()).values('student_id'))
#         return queryset  # Pass through the queryset if no filter is selected


# class SectionFilter(admin.SimpleListFilter):
#     title = 'Section'
#     parameter_name = 'section'

#     def lookups(self, request, model_admin):
#         sections = student_class.objects.values_list('section', flat=True).distinct()
#         return [(section, section) for section in sections]

#     def queryset(self, request, queryset):
#         if self.value():
#             return queryset.filter(student_id__in=student_class.objects.filter(section=self.value()).values('student_id'))
#         return queryset  # Pass through the queryset if no filter is selected


# class GenerateMobileNumbersListAdmin(admin.ModelAdmin):
#     list_display = ('addmission_no', 'student_name', 'get_class_no', 'get_section', 'mobile_no')
#     list_filter = (ClassFilter, SectionFilter)  # Custom filters for class and section

#     def get_class_no(self, obj):
#         student_class_instance = student_class.objects.filter(student_id=obj.student_id).order_by('-started_on').first()
#         return student_class_instance.class_no if student_class_instance else None
#     get_class_no.short_description = 'Class'

#     def get_section(self, obj):
#         student_class_instance = student_class.objects.filter(student_id=obj.student_id).order_by('-started_on').first()
#         return student_class_instance.section if student_class_instance else None
#     get_section.short_description = 'Section'

#     def get_queryset(self, request):
#         queryset = super().get_queryset(request)
#         # Get filter values
#         class_no = request.GET.get('class_no')
#         section = request.GET.get('section')
        
#         # If no filters are selected, return an empty queryset
#         if not class_no and not section:
#             return queryset.none()

#         # Apply filters based on selected criteria
#         if class_no:
#             queryset = queryset.filter(student_id__in=student_class.objects.filter(class_no=class_no).values('student_id'))
#         if section:
#             queryset = queryset.filter(student_id__in=student_class.objects.filter(section=section).values('student_id'))
        
#         return queryset

# from django.contrib import admin

#required
# class ClassFilter(admin.SimpleListFilter):
#     title = 'Class'
#     parameter_name = 'class_no'

#     def lookups(self, request, model_admin):
#         classes = student_class.objects.values_list('class_no', flat=True).distinct()
#         return [(class_no, class_no) for class_no in classes]

#     def queryset(self, request, queryset):
#         if self.value():
#             return queryset.filter(student_id__in=student_class.objects.filter(class_no=self.value()).values('student_id'))
#         return queryset


# class SectionFilter(admin.SimpleListFilter):
#     title = 'Section'
#     parameter_name = 'section'

#     def lookups(self, request, model_admin):
#         sections = student_class.objects.values_list('section', flat=True).distinct()
#         return [(section, section) for section in sections]

#     def queryset(self, request, queryset):
#         if self.value():
#             print("seld",type(self.value()))
#             # print("student_id",student_class.objects.filter(section=self.value()).values('student_id'))
#             return queryset.filter(student_id__in=student_class.objects.filter(section=self.value()).values('student_id'))
#         return queryset


# class GenerateMobileNumbersListAdmin(admin.ModelAdmin):
#     list_display = ('addmission_no', 'student_name', 'get_class_no', 'get_section', 'mobile_no')
#     search_fields = ("addmission_no",)
#     list_filter = (ClassFilter, SectionFilter)  # Custom filters for class and section

#     def get_class_no(self, obj):
#         # student_class_instance = student_class.objects.filter(student_id=obj.student_id).order_by('-started_on').first()
#         student_class_instance = student_class.objects.filter(student_id=obj.student_id).order_by('started_on').first()
#         return student_class_instance.class_no if student_class_instance else None
#     get_class_no.short_description = 'Class'

#     def get_section(self, obj):
#         # student_class_instance = student_class.objects.filter(student_id=obj.student_id).order_by('-started_on').first()
#         student_class_instance = student_class.objects.filter(student_id=obj.student_id).order_by('started_on').first()
#         return student_class_instance.section if student_class_instance else None
#     get_section.short_description = 'Section'

#     def get_queryset(self, request):
#         queryset = super().get_queryset(request)
        
#         # Get filter values
#         class_no = request.GET.get('class_no')
#         section = request.GET.get('section')

#         # If no filters are selected, return an empty queryset
#         if not class_no and not section:
#             return queryset.none()

#         # Apply filters based on selected criteria
#         if class_no and section:
#             # Both filters applied, must match both class and section
#             print("class_no and section",type(section))
#             queryset = queryset.filter(
#                 student_id__in=student_class.objects.filter(class_no=class_no, section=section).values('student_id')
#             )
#         elif class_no:
#             # Only class filter applied
#             print("class_no",type(class_no))
#             queryset = queryset.filter(
#                 student_id__in=student_class.objects.filter(class_no=class_no).values('student_id')
#             )
#         elif section:
#             print(" section",type(section))
#             print(" student_class.objects.filter(section=section)",student_class.objects.filter(section=section))
#             student_class.objects.filter(section=section)
#             # Only section filter applied
#             queryset = queryset.filter(
#                 student_id__in=student_class.objects.filter(section=section).values('student_id')
#             )
        
#         return queryset



# to much improved
# class ClassFilter(admin.SimpleListFilter):
#     title = 'Class'
#     parameter_name = 'class_no'

#     def lookups(self, request, model_admin):
#         classes = student_class.objects.values_list('class_no', flat=True).distinct()
#         return [(class_no, class_no) for class_no in classes]

#     def queryset(self, request, queryset):
#         if self.value():
#             return queryset.filter(student_id__in=student_class.objects.filter(class_no=self.value()).values('student_id'))
#         return queryset


# class SectionFilter(admin.SimpleListFilter):
#     title = 'Section'
#     parameter_name = 'section'

#     def lookups(self, request, model_admin):
#         sections = student_class.objects.values_list('section', flat=True).distinct()
#         return [(section, section) for section in sections]

#     def queryset(self, request, queryset):
#         if self.value():
#             return queryset.filter(student_id__in=student_class.objects.filter(section=self.value()).values('student_id'))
#         return queryset


# class GenerateMobileNumbersListAdmin(admin.ModelAdmin):
#     list_display = ('addmission_no', 'student_name', 'get_class_no', 'get_section', 'mobile_no')
#     list_filter = (ClassFilter, SectionFilter)  # Custom filters for class and section

#     def get_class_no(self, obj):
#         student_class_instance = student_class.objects.filter(student_id=obj.student_id).order_by('-started_on').first()
#         return student_class_instance.class_no if student_class_instance else None
#     get_class_no.short_description = 'Class'

#     def get_section(self, obj):
#         student_class_instance = student_class.objects.filter(student_id=obj.student_id).order_by('-started_on').first()
#         return student_class_instance.section if student_class_instance else None
#     get_section.short_description = 'Section'

#     def get_queryset(self, request):
#         queryset = super().get_queryset(request)

#         # Get filter values
#         class_no = request.GET.get('class_no')
#         section = request.GET.get('section')

#         # If no filters are selected, return an empty queryset
#         if not class_no and not section:
#             return queryset.none()

#         # Subquery to get the latest valid entry for each student based on filter criteria
#         subquery = student_class.objects.filter(
#             student_id=OuterRef('student_id'),
#             started_on=Subquery(
#                 student_class.objects.filter(
#                     student_id=OuterRef('student_id')
#                 ).values('student_id').annotate(
#                     max_started_on=Max('started_on')
#                 ).values('max_started_on')
#             )
#         ).values('student_id')

#         if class_no:
#             subquery = subquery.filter(class_no=class_no)
#         if section:
#             subquery = subquery.filter(section=section)

#         # Filter queryset based on the subquery
#         queryset = queryset.filter(student_id__in=Subquery(subquery))

#         return queryset



# class ClassFilter(admin.SimpleListFilter):
#     title = 'Class'
#     parameter_name = 'class_no'

#     def lookups(self, request, model_admin):
#         predefined_classes = ['Play-way', 'pre-nursery', 'nursery', 'LKG', 'UKG']
        
#         # Get all distinct class_no values from student_class, excluding predefined classes and 0
#         class_numbers = student_class.objects.exclude(class_no__in=predefined_classes).exclude(class_no='0')

#         # Convert numeric values to integers for sorting, and then sort them
#         class_numbers = sorted(
#             class_numbers.annotate(
#                 numeric_class=Cast('class_no', IntegerField())
#             ).values_list('numeric_class', flat=True)
#         )

#         # Combine predefined classes with sorted numeric classes
#         class_list = predefined_classes + [str(num) for num in class_numbers]

#         # Return as tuples for lookups
#         return [(class_no, class_no) for class_no in class_list]

#     def queryset(self, request, queryset):
#         return queryset  # We handle filtering in get_queryset()


# this is required

class ClassFilter(admin.SimpleListFilter):
    title = 'Class'
    parameter_name = 'class_no'

    def lookups(self, request, model_admin):
        predefined_classes = ['Play-way', 'pre-nursery', 'nursery', 'LKG', 'UKG']
        # Get all distinct class_no values from student_class
        class_numbers = student_class.objects.exclude(class_no__in=predefined_classes).values_list('class_no', flat=True).distinct()
        
        # Convert numeric values to integers for sorting
        class_numbers = sorted(
            class_numbers.annotate(
                numeric_class=Cast('class_no', IntegerField())
            ).values_list('numeric_class', flat=True)
        )

        # Combine predefined classes with sorted numeric classes
        # class_list = predefined_classes + [str(num) for num in class_numbers]
        class_list = predefined_classes + [str(i) for i in range(1, 13)]
        
        # Return as tuples for lookups
        return [(class_no, class_no) for class_no in class_list]

    def queryset(self, request, queryset):
        return queryset  # We handle filtering in get_queryset()


# class ClassFilter(admin.SimpleListFilter):
#     title = 'Class'
#     parameter_name = 'class_no'

#     def lookups(self, request, model_admin):
#         classes = student_class.objects.values_list('class_no', flat=True).distinct()
#         return [(class_no, class_no) for class_no in classes]

#     def queryset(self, request, queryset):
#         return queryset  # We handle filtering in get_queryset()


class SectionFilter(admin.SimpleListFilter):
    title = 'Section'
    parameter_name = 'section'

    def lookups(self, request, model_admin):
        # Get all distinct section values from student_class and order them alphabetically
        sections = student_class.objects.values_list('section', flat=True).distinct().order_by('section')

        # Return as tuples for lookups
        return [(section, section) for section in sections]

    def queryset(self, request, queryset):
        return queryset  # We handle filtering in get_queryset()


class YearFilter(admin.SimpleListFilter):
    title = 'Year'
    parameter_name = 'year'

    def lookups(self, request, model_admin):
        # Create a list of years from 2024 to 2018
        years = [(str(year), str(year)) for year in range(2024, 2017, -1)]
        return years

    def queryset(self, request, queryset):
        # Return the queryset unchanged since this filter is not used for filtering
        return queryset


class GenerateMobileNumbersListAdmin(admin.ModelAdmin):
    list_display = ('addmission_no', 'student_name', 'get_class_no', 'get_section', 'mobile_no')
    list_filter = (ClassFilter, SectionFilter, YearFilter)

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def get_class_no(self, obj):
        return self.class_section_map.get(obj.student_id, {}).get('class_no')
    get_class_no.short_description = 'Class'

    def get_section(self, obj):
        return self.class_section_map.get(obj.student_id, {}).get('section')
    get_section.short_description = 'Section'

    def get_queryset(self, request):
        self.requested_class_no = request.GET.get('class_no')
        self.requested_section = request.GET.get('section')
        self.requested_year = request.GET.get('year')

        queryset = super().get_queryset(request)

        # If no filters are selected, return an empty queryset
        if not self.requested_class_no and not self.requested_section and not self.requested_year:
            return queryset.none()

        # Filter `student_class` records based on selected class_no and section
        student_class_queryset = student_class.objects.all()



        if self.requested_class_no:
            student_class_queryset = student_class_queryset.filter(class_no=self.requested_class_no)

        if self.requested_section:
            student_class_queryset = student_class_queryset.filter(section=self.requested_section)

        # Create a map of student_id to their class and section
        self.class_section_map = {}
        for sc in student_class_queryset:
            self.class_section_map[sc.student_id.student_id] = {
                'class_no': sc.class_no,
                'section': sc.section
            }

        # Filter the queryset based on student IDs that match the class_section_map
        queryset = queryset.filter(student_id__in=self.class_section_map.keys())

        return queryset
    
    
    def export_as_csv(self, request, queryset):
        meta = self.model._meta
        field_names = ['addmission_no', 'student_name', 'Class', 'Section', 'mobile_no']

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename={meta}.csv'
        writer = csv.writer(response)

        writer.writerow(field_names)
        for obj in queryset:
            row = [
                getattr(obj, 'addmission_no'),
                getattr(obj, 'student_name'),
                self.get_class_no(obj),
                self.get_section(obj),
                getattr(obj, 'mobile_no')
            ]
            writer.writerow(row)

        return response

    export_as_csv.short_description = "Export Selected to CSV"
    actions = [export_as_csv]



# class GenerateMobileNumbersListAdmin(admin.ModelAdmin):
#     list_display = ('addmission_no', 'student_name', 'get_class_no', 'get_section', 'mobile_no')
#     list_filter = (ClassFilter, SectionFilter, YearFilter)

#     def has_add_permission(self, request):
#         return False

#     def has_change_permission(self, request, obj=None):
#         return False

#     def has_delete_permission(self, request, obj=None):
#         return False

#     def get_class_no(self, obj):
#         student_class_instance = student_class.objects.filter(student_id=obj.student_id).order_by('-started_on').first()
#         return student_class_instance.class_no if student_class_instance else None
#     get_class_no.short_description = 'Class'

#     def get_section(self, obj):
#         student_class_instance = student_class.objects.filter(student_id=obj.student_id).order_by('-started_on').first()
#         return student_class_instance.section if student_class_instance else None
#     get_section.short_description = 'Section'

#     def get_queryset(self, request):
#         queryset = super().get_queryset(request)

#         # Retrieve filters from the request
#         requested_class_no = request.GET.get('class_no')
#         requested_section = request.GET.get('section')
#         year_filter_selected = request.GET.get('year')

#         # If a year filter is selected, show all records
#         # if year_filter_selected:
#         #     return queryset

#         # Apply class and section filters if provided
#         if requested_class_no or requested_section:
#             # Get student IDs that match the class and section filters
#             student_ids = set()

#             if requested_class_no:
#                 student_ids.update(
#                     student_class.objects.filter(class_no=requested_class_no).values_list('student_id', flat=True)
#                 )

#             if requested_section:
#                 student_ids.update(
#                     student_class.objects.filter(section=requested_section).values_list('student_id', flat=True)
#                 )

#             # Filter the queryset based on student IDs
#             queryset = queryset.filter(student_id__in=student_ids)

#         elif year_filter_selected:
#             return queryset
#         else:
#             # If no filters are selected, return an empty queryset
#             return queryset.none()

#         return queryset

#     def export_as_csv(self, request, queryset):
#         meta = self.model._meta
#         field_names = ['addmission_no', 'student_name', 'Class', 'Section', 'mobile_no']

#         response = HttpResponse(content_type='text/csv')
#         response['Content-Disposition'] = f'attachment; filename={meta}.csv'
#         writer = csv.writer(response)

#         writer.writerow(field_names)
#         for obj in queryset:
#             row = [
#                 getattr(obj, 'addmission_no'),
#                 getattr(obj, 'student_name'),
#                 self.get_class_no(obj),
#                 self.get_section(obj),
#                 getattr(obj, 'mobile_no')
#             ]
#             writer.writerow(row)

#         return response

#     export_as_csv.short_description = "Export Selected to CSV"
#     actions = [export_as_csv]



    



# class GenerateMobileNumbersListAdmin(admin.ModelAdmin):
#     list_display = ('addmission_no', 'student_name', 'Class', 'Section', 'mobile_no')
#     list_filter = ('get_class_no', 'get_section')

#     def has_add_permission(self, request):
#         return False

#     def has_change_permission(self, request, obj=None):
#         return False

#     def has_delete_permission(self, request, obj=None):
#         return False

#     def Class(self, obj):
#         student_class_instance = student_class.objects.filter(student_id=obj.student_id).order_by('-started_on').first()
#         return student_class_instance.class_no if student_class_instance else None
#     Class.short_description = 'Class'

#     def Section(self, obj):
#         student_class_instance = student_class.objects.filter(student_id=obj.student_id).order_by('-started_on').first()
#         return student_class_instance.section if student_class_instance else None
#     Section.short_description = 'Section'

#     def export_as_csv(self, request, queryset):
#         meta = self.model._meta
#         field_names = ['addmission_no', 'student_name', 'Class', 'Section', 'mobile_no']

#         response = HttpResponse(content_type='text/csv')
#         response['Content-Disposition'] = f'attachment; filename={meta}.csv'
#         writer = csv.writer(response)

#         writer.writerow(field_names)
#         for obj in queryset:
#             row = [
#                 getattr(obj, 'addmission_no'),
#                 getattr(obj, 'student_name'),
#                 self.Class(obj),
#                 self.Section(obj),
#                 getattr(obj, 'mobile_no')
#             ]
#             writer.writerow(row)

#         return response

#     export_as_csv.short_description = "Export Selected to CSV"
#     actions = [export_as_csv]





admin.site.register(generate_mobile_number_list,GenerateMobileNumbersListAdmin)


# class ChequeStatusListAdmin(admin.ModelAdmin):
#     list_display = ('addmission_no', 'Class', 'Section','student_name', 'FeesPeriod')
#     search_fields = ['addmission_no', 'student_class', 'student_section','student_name', 'FeesPeriod']

#     def has_add_permission(self, request):
#         return False

#     def has_change_permission(self, request, obj=None):
#         return False

#     def has_delete_permission(self, request, obj=None):
#         return False

#     def Class(self, obj):
#         student_class_instance = student_fee.objects.filter(student_id=obj.student_id).order_by('-added_at').first()
#         return student_class_instance.student_class  if student_class_instance else None
#     Class.short_description = 'Class'

#     def Section(self, obj):
#         student_class_instance = student_fee.objects.filter(student_id=obj.student_id).order_by('-added_at').first()
#         return student_class_instance.student_section if student_class_instance else None
#     Section.short_description = 'Section'

#     def FeesPeriod(self, obj):
#         student_class_instance = student_fee.objects.filter(student_id=obj.student_id).order_by('-added_at').first()
#         return student_class_instance.fees_period_month if student_class_instance else None
#     FeesPeriod.short_description = 'Fees Period Month'

# class ChequeStatusListAdmin(admin.ModelAdmin):
#     list_display = ('addmission_no', 'Class', 'Section', 'Student Name', 'FeesPeriod')
#     search_fields = ['addmission_no', 'student_name']  # Only fields in student_master

#     def has_add_permission(self, request):
#         return False

#     def has_change_permission(self, request, obj=None):
#         return False

#     def has_delete_permission(self, request, obj=None):
#         return False

#     def Class(self, obj):
#         student_class_instance = student_fee.objects.filter(student_id=obj.student_id).order_by('-added_at').first()
#         return student_class_instance.student_class if student_class_instance else None
#     Class.short_description = 'Student Class'

#     def Section(self, obj):
#         student_class_instance = student_fee.objects.filter(student_id=obj.student_id).order_by('-added_at').first()
#         return student_class_instance.student_section if student_class_instance else None
#     Section.short_description = 'Student Section'

#     def FeesPeriod(self, obj):
#         student_class_instance = student_fee.objects.filter(student_id=obj.student_id).order_by('-added_at').first()
#         return student_class_instance.fees_period_month if student_class_instance else None
#     FeesPeriod.short_description = 'Fees Period Month'

#     # Custom search method
#     def get_search_results(self, request, queryset, search_term):
#         queryset, use_distinct = super().get_search_results(request, queryset, search_term)
#         if search_term:
#             queryset = queryset.filter(
#                 student_id__in=student_fee.objects.filter(
#                     student_class__icontains=search_term
#                 ).values('student_id')
#             ) | queryset.filter(
#                 student_id__in=student_fee.objects.filter(
#                     student_section__icontains=search_term
#                 ).values('student_id')
#             )
#         return queryset, use_distinct
    
# class ChequeStatusListAdmin(admin.ModelAdmin):
#     list_display = (
#         'addmission_no', 'Class', 'Section', 'student_name', 'FeesPeriod', 'Year', 'DatePayment',
#         'ChequeStatus', 'CheqNo', 'BankName', 'BranchName', 'TotalAmount', 'AmountPaid',
#         'DateEntry'
#     )
#     search_fields = [
#         'addmission_no', 'student_name', 'student_fee__year', 'student_fee__date_payment',
#         'student_fee__cheque_status', 'student_fee__cheq_no', 'student_fee__bank_name',
#         'student_fee__branch_name', 'student_fee__total_amount', 'student_fee__amount_paid',
#         'student_fee__entry_date'
#     ]

#     def has_add_permission(self, request):
#         return False

#     def has_change_permission(self, request, obj=None):
#         return False

#     def has_delete_permission(self, request, obj=None):
#         return False

#     def Class(self, obj):
#         student_class_instance = student_fee.objects.filter(student_id=obj.student_id).order_by('-added_at').first()
#         return student_class_instance.student_class if student_class_instance else None
#     Class.short_description = 'Class'

#     def Section(self, obj):
#         student_class_instance = student_fee.objects.filter(student_id=obj.student_id).order_by('-added_at').first()
#         return student_class_instance.student_section if student_class_instance else None
#     Section.short_description = 'Section'

#     def FeesPeriod(self, obj):
#         student_class_instance = student_fee.objects.filter(student_id=obj.student_id).order_by('-added_at').first()
#         return student_class_instance.fees_period_month if student_class_instance else None
#     FeesPeriod.short_description = 'Fees Period Month'

#     def Year(self, obj):
#         student_class_instance = student_fee.objects.filter(student_id=obj.student_id).order_by('-added_at').first()
#         return student_class_instance.year if student_class_instance else None
#     Year.short_description = 'Year'

#     def DatePayment(self, obj):
#         student_class_instance = student_fee.objects.filter(student_id=obj.student_id).order_by('-added_at').first()
#         return student_class_instance.date_payment if student_class_instance else None
#     DatePayment.short_description = 'Date Payment'

#     def ChequeStatus(self, obj):
#         student_class_instance = student_fee.objects.filter(student_id=obj.student_id).order_by('-added_at').first()
#         return student_class_instance.cheque_status if student_class_instance else None
#     ChequeStatus.short_description = 'Cheque Status'

#     def CheqNo(self, obj):
#         student_class_instance = student_fee.objects.filter(student_id=obj.student_id).order_by('-added_at').first()
#         return student_class_instance.cheq_no if student_class_instance else None
#     CheqNo.short_description = 'Cheque No'

#     def BankName(self, obj):
#         student_class_instance = student_fee.objects.filter(student_id=obj.student_id).order_by('-added_at').first()
#         return student_class_instance.bank_name if student_class_instance else None
#     BankName.short_description = 'Bank Name'

#     def BranchName(self, obj):
#         student_class_instance = student_fee.objects.filter(student_id=obj.student_id).order_by('-added_at').first()
#         return student_class_instance.branch_name if student_class_instance else None
#     BranchName.short_description = 'Branch Name'

#     def TotalAmount(self, obj):
#         student_class_instance = student_fee.objects.filter(student_id=obj.student_id).order_by('-added_at').first()
#         return student_class_instance.total_amount if student_class_instance else None
#     TotalAmount.short_description = 'Total Amount'

#     def AmountPaid(self, obj):
#         student_class_instance = student_fee.objects.filter(student_id=obj.student_id).order_by('-added_at').first()
#         return student_class_instance.amount_paid if student_class_instance else None
#     AmountPaid.short_description = 'Amount Paid'

#     def DateEntry(self, obj):
#         student_class_instance = student_fee.objects.filter(student_id=obj.student_id).order_by('-added_at').first()
#         return student_class_instance.entry_date if student_class_instance else None
#     DateEntry.short_description = 'Date of Entry'

#     # def RealizedDate(self, obj):
#     #     student_class_instance = student_fee.objects.filter(student_id=obj.student_id).order_by('-added_at').first()
#     #     return student_class_instance.realized_date if student_class_instance else None
#     # RealizedDate.short_description = 'Realized Date'

#     actions = ['mark_as_realized', 'mark_as_rejected']

#     def mark_as_realized(self, request, queryset):
#         for obj in queryset:
#             student_class_instance = student_fee.objects.filter(student_id=obj.student_id).order_by('-added_at').first()
#             if student_class_instance:
#                 student_class_instance.cheque_status = 'Realized'
#                 student_class_instance.realized_date = timezone.now()  # Update the realized date
#                 student_class_instance.save()
#     mark_as_realized.short_description = "Mark selected cheques as Realized"

#     def mark_as_rejected(self, request, queryset):
#         for obj in queryset:
#             student_class_instance = student_fee.objects.filter(student_id=obj.student_id).order_by('-added_at').first()
#             if student_class_instance:
#                 student_class_instance.cheque_status = 'Rejected'
#                 student_class_instance.realized_date = None  # Clear the realized date
#                 student_class_instance.save()
#     mark_as_rejected.short_description = "Mark selected cheques as Rejected"

#     def get_queryset(self, request):
#         # Filter records where cheque_status is 'Open'
#         queryset = super().get_queryset(request)
#         open_student_ids = student_fee.objects.filter(cheque_status='Open').values_list('student_id', flat=True)
#         return queryset.filter(student_id__in=open_student_ids)

#     def get_search_results(self, request, queryset, search_term):
#         queryset, use_distinct = super().get_search_results(request, queryset, search_term)
#         if search_term:
#             queryset = queryset.filter(
#                 student_id__in=student_fee.objects.filter(
#                     student_class__icontains=search_term
#                 ).values('student_id')
#             ) | queryset.filter(
#                 student_id__in=student_fee.objects.filter(
#                     student_section__icontains=search_term
#                 ).values('student_id')
#             )
#         return queryset, use_distinct


class ChequeStatusListAdmin(admin.ModelAdmin):
    list_display = (
        'addmission_no', 'Class', 'Section', 'student_name', 'FeesPeriod', 'Year', 'DatePayment',
        'ChequeStatus', 'CheqNo', 'BankName', 'BranchName', 'TotalAmount', 'AmountPaid',
        'DateEntry'
    )
    search_fields = [
        'addmission_no', 'student_name', 'student_fee__year', 'student_fee__date_payment',
        'student_fee__cheque_status', 'student_fee__cheq_no', 'student_fee__bank_name',
        'student_fee__branch_name', 'student_fee__total_amount', 'student_fee__amount_paid',
        'student_fee__entry_date'
    ]

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
    
    def format_date(self, date):
        return DateFormat(date).format('Y-m-d') if date else None

    def Class(self, obj):
        student_class_instance = student_fee.objects.filter(student_id=obj.student_id).order_by('-added_at').first()
        return student_class_instance.student_class if student_class_instance else None
    Class.short_description = 'Class'

    def Section(self, obj):
        student_class_instance = student_fee.objects.filter(student_id=obj.student_id).order_by('-added_at').first()
        return student_class_instance.student_section if student_class_instance else None
    Section.short_description = 'Section'

    def FeesPeriod(self, obj):
        student_class_instance = student_fee.objects.filter(student_id=obj.student_id).order_by('-added_at').first()
        return student_class_instance.fees_period_month if student_class_instance else None
    FeesPeriod.short_description = 'Fees Period Month'

    def Year(self, obj):
        student_class_instance = student_fee.objects.filter(student_id=obj.student_id).order_by('-added_at').first()
        return student_class_instance.year if student_class_instance else None
    Year.short_description = 'Year'

    def DatePayment(self, obj):
        student_class_instance = student_fee.objects.filter(student_id=obj.student_id).order_by('-added_at').first()
        # return student_class_instance.date_payment if student_class_instance else None
        return self.format_date(student_class_instance.date_payment) if student_class_instance else None
    DatePayment.short_description = 'Date Payment'

    def ChequeStatus(self, obj):
        student_class_instance = student_fee.objects.filter(student_id=obj.student_id).order_by('-added_at').first()
        return student_class_instance.cheque_status if student_class_instance else None
    ChequeStatus.short_description = 'Cheque Status'

    def CheqNo(self, obj):
        student_class_instance = student_fee.objects.filter(student_id=obj.student_id).order_by('-added_at').first()
        return student_class_instance.cheq_no if student_class_instance else None
    CheqNo.short_description = 'Cheque No'

    def BankName(self, obj):
        student_class_instance = student_fee.objects.filter(student_id=obj.student_id).order_by('-added_at').first()
        return student_class_instance.bank_name if student_class_instance else None
    BankName.short_description = 'Bank Name'

    def BranchName(self, obj):
        student_class_instance = student_fee.objects.filter(student_id=obj.student_id).order_by('-added_at').first()
        return student_class_instance.branch_name if student_class_instance else None
    BranchName.short_description = 'Branch Name'

    def TotalAmount(self, obj):
        student_class_instance = student_fee.objects.filter(student_id=obj.student_id).order_by('-added_at').first()
        return student_class_instance.total_amount if student_class_instance else None
    TotalAmount.short_description = 'Total Amount'

    def AmountPaid(self, obj):
        student_class_instance = student_fee.objects.filter(student_id=obj.student_id).order_by('-added_at').first()
        return student_class_instance.amount_paid if student_class_instance else None
    AmountPaid.short_description = 'Amount Paid'

    def DateEntry(self, obj):
        student_class_instance = student_fee.objects.filter(student_id=obj.student_id).order_by('-added_at').first()
        # return student_class_instance.entry_date if student_class_instance else None
        return self.format_date(student_class_instance.entry_date if student_class_instance else None)
    DateEntry.short_description = 'Date of Entry'

    def RealizedDate(self, obj):
        student_class_instance = student_fee.objects.filter(student_id=obj.student_id).order_by('-added_at').first()
        return student_class_instance.realized_date if student_class_instance else None
    RealizedDate.short_description = 'Realized Date'

    actions = ['mark_as_realized', 'mark_as_rejected']

    def mark_as_realized(self, request, queryset):
        for obj in queryset:
            student_class_instance = student_fee.objects.filter(student_id=obj.student_id).order_by('-added_at').first()
            if student_class_instance:
                student_class_instance.cheque_status = 'Realized'
                student_class_instance.realized_date = timezone.now()  # Update the realized date
                student_class_instance.save()
    mark_as_realized.short_description = "Mark selected cheques as Realized"

    def mark_as_rejected(self, request, queryset):
        for obj in queryset:
            student_class_instance = student_fee.objects.filter(student_id=obj.student_id).order_by('-added_at').first()
            if student_class_instance:
                student_class_instance.cheque_status = 'Rejected'
                student_class_instance.realized_date = None  # Clear the realized date
                student_class_instance.save()
    mark_as_rejected.short_description = "Mark selected cheques as Rejected"

    def get_queryset(self, request):
        # Filter the `student_fee` records where `cheque_status` is 'Open'
        student_ids_with_open_cheque = student_fee.objects.filter(cheque_status='Open').values_list('student_id', flat=True)
        # Filter the queryset of `cheque_status` to include only those student_ids
        queryset = super().get_queryset(request)
        return queryset.filter(student_id__in=student_ids_with_open_cheque)

# this is working

# class ChequeStatusListForm(forms.Form):
#     realized_date = forms.DateField(
#         widget=forms.TextInput(attrs={'type': 'date'}),
#         required=False,
#         label="Realized Date"
#     )

# class ChequeStatusListAdmin(admin.ModelAdmin):
#     list_display = (
#         'addmission_no', 'Class', 'Section', 'student_name', 'FeesPeriod', 'Year', 'DatePayment',
#         'ChequeStatus', 'CheqNo', 'BankName', 'BranchName', 'TotalAmount', 'AmountPaid', 'DateEntry'
#     )
#     search_fields = [
#         'addmission_no', 'student_name', 'student_fee__year', 'student_fee__date_payment',
#         'student_fee__cheque_status', 'student_fee__cheq_no', 'student_fee__bank_name',
#         'student_fee__branch_name', 'student_fee__total_amount', 'student_fee__amount_paid',
#         'student_fee__entry_date'
#     ]

#     actions = ['mark_as_realized', 'mark_as_rejected']

#     def get_queryset(self, request):
#         student_ids_with_open_cheque = student_fee.objects.filter(cheque_status='Open').values_list('student_id', flat=True)
#         queryset = super().get_queryset(request)
#         return queryset.filter(student_id__in=student_ids_with_open_cheque)

#     def get_changelist_form(self, request, **kwargs):
#         return ChequeStatusListForm

#     def changelist_view(self, request, extra_context=None):
#         if request.method == 'POST':
#             form = ChequeStatusListForm(request.POST)
#             if form.is_valid():
#                 request.session['realized_date'] = form.cleaned_data['realized_date']
#         else:
#             form = ChequeStatusListForm()

#         extra_context = extra_context or {}
#         extra_context['changelist_form'] = form
#         return super().changelist_view(request, extra_context=extra_context)

#     def mark_as_realized(self, request, queryset):
#         realized_date = request.session.get('realized_date', timezone.now().date())
#         for obj in queryset:
#             student_class_instance = student_fee.objects.filter(student_id=obj.student_id).order_by('-added_at').first()
#             if student_class_instance:
#                 student_class_instance.cheque_status = 'Realized'
#                 student_class_instance.realized_date = realized_date
#                 student_class_instance.save()
#     mark_as_realized.short_description = "Mark selected cheques as Realized"

#     def mark_as_rejected(self, request, queryset):
#         realized_date = request.session.get('realized_date', None)
#         for obj in queryset:
#             student_class_instance = student_fee.objects.filter(student_id=obj.student_id).order_by('-added_at').first()
#             if student_class_instance:
#                 student_class_instance.cheque_status = 'Rejected'
#                 student_class_instance.realized_date = realized_date
#                 student_class_instance.save()
#     mark_as_rejected.short_description = "Mark selected cheques as Rejected"

# admin.site.register(cheque_status, ChequeStatusListAdmin)
# this is working


# class ChequeStatusListAdmin(admin.ModelAdmin):
#     list_display = (
#         'addmission_no', 'get_class', 'get_section', 'student_name', 'get_fees_period', 'get_year', 
#         'get_date_payment', 'get_cheque_status', 'get_cheq_no', 'get_bank_name', 
#         'get_branch_name', 'get_total_amount', 'get_amount_paid', 'get_date_entry'
#     )
#     search_fields = [
#         'addmission_no', 'student_name', 'student_fee__year', 'student_fee__date_payment',
#         'student_fee__cheque_status', 'student_fee__cheq_no', 'student_fee__bank_name',
#         'student_fee__branch_name', 'student_fee__total_amount', 'student_fee__amount_paid',
#         'student_fee__entry_date'
#     ]

#     actions = ['mark_as_realized', 'mark_as_rejected']

    
#     def has_add_permission(self, request):
#         return False

#     def has_change_permission(self, request, obj=None):
#         return False

#     def has_delete_permission(self, request, obj=None):
#         return False

#     # Define the methods for each custom field
#     def get_class(self, obj):
#         student_class_instance = student_fee.objects.filter(student_id=obj.student_id).order_by('-added_at').first()
#         return student_class_instance.student_class if student_class_instance else None
#     get_class.short_description = 'Class'

#     def get_section(self, obj):
#         student_class_instance = student_fee.objects.filter(student_id=obj.student_id).order_by('-added_at').first()
#         return student_class_instance.student_section if student_class_instance else None
#     get_section.short_description = 'Section'

#     def get_fees_period(self, obj):
#         student_class_instance = student_fee.objects.filter(student_id=obj.student_id).order_by('-added_at').first()
#         return student_class_instance.fees_period_month if student_class_instance else None
#     get_fees_period.short_description = 'Fees Period Month'

#     def get_year(self, obj):
#         student_class_instance = student_fee.objects.filter(student_id=obj.student_id).order_by('-added_at').first()
#         return student_class_instance.year if student_class_instance else None
#     get_year.short_description = 'Year'

#     def get_date_payment(self, obj):
#         student_class_instance = student_fee.objects.filter(student_id=obj.student_id).order_by('-added_at').first()
#         return student_class_instance.date_payment if student_class_instance else None
#     get_date_payment.short_description = 'Date Payment'

#     def get_cheque_status(self, obj):
#         student_class_instance = student_fee.objects.filter(student_id=obj.student_id).order_by('-added_at').first()
#         return student_class_instance.cheque_status if student_class_instance else None
#     get_cheque_status.short_description = 'Cheque Status'

#     def get_cheq_no(self, obj):
#         student_class_instance = student_fee.objects.filter(student_id=obj.student_id).order_by('-added_at').first()
#         return student_class_instance.cheq_no if student_class_instance else None
#     get_cheq_no.short_description = 'Cheque No'

#     def get_bank_name(self, obj):
#         student_class_instance = student_fee.objects.filter(student_id=obj.student_id).order_by('-added_at').first()
#         return student_class_instance.bank_name if student_class_instance else None
#     get_bank_name.short_description = 'Bank Name'

#     def get_branch_name(self, obj):
#         student_class_instance = student_fee.objects.filter(student_id=obj.student_id).order_by('-added_at').first()
#         return student_class_instance.branch_name if student_class_instance else None
#     get_branch_name.short_description = 'Branch Name'

#     def get_total_amount(self, obj):
#         student_class_instance = student_fee.objects.filter(student_id=obj.student_id).order_by('-added_at').first()
#         return student_class_instance.total_amount if student_class_instance else None
#     get_total_amount.short_description = 'Total Amount'

#     def get_amount_paid(self, obj):
#         student_class_instance = student_fee.objects.filter(student_id=obj.student_id).order_by('-added_at').first()
#         return student_class_instance.amount_paid if student_class_instance else None
#     get_amount_paid.short_description = 'Amount Paid'

#     def get_date_entry(self, obj):
#         student_class_instance = student_fee.objects.filter(student_id=obj.student_id).order_by('-added_at').first()
#         return student_class_instance.entry_date if student_class_instance else None
#     get_date_entry.short_description = 'Date of Entry'

#     def get_queryset(self, request):
#         student_ids_with_open_cheque = student_fee.objects.filter(cheque_status='Open').values_list('student_id', flat=True)
#         queryset = super().get_queryset(request)
#         return queryset.filter(student_id__in=student_ids_with_open_cheque)
    


#     def changelist_view(self, request, extra_context=None):
#         if request.method == 'POST' and 'apply' in request.POST:
#             realized_date_form = RealizedDateForm(request.POST)
#             if realized_date_form.is_valid():
#                 realized_date = realized_date_form.cleaned_data['realized_date']
#                 # Store the realized_date in the session to use in actions
#                 request.session['realized_date'] = str(realized_date)
#         else:
#             realized_date_form = RealizedDateForm()

#         extra_context = extra_context or {}
#         extra_context['realized_date_form'] = realized_date_form

#         return super().changelist_view(request, extra_context=extra_context)

#     def mark_as_realized(self, request, queryset):
#         realized_date = request.session.get('realized_date')
#         if realized_date:
#             queryset.update(cheque_status='Realized', realized_date=realized_date)
#         self.message_user(request, "Selected records marked as Realized.")
    
#     mark_as_realized.short_description = "Mark selected as Realized"

#     def mark_as_rejected(self, request, queryset):
#         realized_date = request.session.get('realized_date')
#         if realized_date:
#             queryset.update(cheque_status='Rejected', realized_date=realized_date)
#         self.message_user(request, "Selected records marked as Rejected.")
    
#     mark_as_rejected.short_description = "Mark selected as Rejected"
    
    
# from django.contrib import admin
# from django.utils.dateformat import DateFormat
# from .models import cheque_status, student_fee
# from .forms import RealizedDateForm

# class ChequeStatusListAdmin(admin.ModelAdmin):
#     list_display = (
#         'addmission_no', 'get_class', 'get_section', 'student_name', 'get_fees_period', 'get_year', 
#         'get_date_payment', 'get_cheque_status', 'get_cheq_no', 'get_bank_name', 
#         'get_branch_name', 'get_total_amount', 'get_amount_paid', 'get_date_entry'
#     )
#     search_fields = [
#         'addmission_no', 'student_name', 'student_fee__year', 'student_fee__date_payment',
#         'student_fee__cheque_status', 'student_fee__cheq_no', 'student_fee__bank_name',
#         'student_fee__branch_name', 'student_fee__total_amount', 'student_fee__amount_paid',
#         'student_fee__entry_date'
#     ]

#     actions = ['mark_as_realized', 'mark_as_rejected']

#     def has_add_permission(self, request):
#         return False

#     def has_change_permission(self, request, obj=None):
#         return False

#     def has_delete_permission(self, request, obj=None):
#         return False

#     def format_date(self, date):
#         return DateFormat(date).format('Y-m-d') if date else None

#     def get_class(self, obj):
#         student_class_instance = student_fee.objects.filter(student_id=obj.student_id).order_by('-added_at').first()
#         return student_class_instance.student_class if student_class_instance else None
#     get_class.short_description = 'Class'

#     def get_section(self, obj):
#         student_class_instance = student_fee.objects.filter(student_id=obj.student_id).order_by('-added_at').first()
#         return student_class_instance.student_section if student_class_instance else None
#     get_section.short_description = 'Section'

#     def get_fees_period(self, obj):
#         student_class_instance = student_fee.objects.filter(student_id=obj.student_id).order_by('-added_at').first()
#         return student_class_instance.fees_period_month if student_class_instance else None
#     get_fees_period.short_description = 'Fees Period Month'

#     def get_year(self, obj):
#         student_class_instance = student_fee.objects.filter(student_id=obj.student_id).order_by('-added_at').first()
#         return student_class_instance.year if student_class_instance else None
#     get_year.short_description = 'Year'

#     def get_date_payment(self, obj):
#         student_class_instance = student_fee.objects.filter(student_id=obj.student_id).order_by('-added_at').first()
#         return self.format_date(student_class_instance.date_payment) if student_class_instance else None
#     get_date_payment.short_description = 'Date Payment'

#     def get_cheque_status(self, obj):
#         student_class_instance = student_fee.objects.filter(student_id=obj.student_id).order_by('-added_at').first()
#         return student_class_instance.cheque_status if student_class_instance else None
#     get_cheque_status.short_description = 'Cheque Status'

#     def get_cheq_no(self, obj):
#         student_class_instance = student_fee.objects.filter(student_id=obj.student_id).order_by('-added_at').first()
#         return student_class_instance.cheq_no if student_class_instance else None
#     get_cheq_no.short_description = 'Cheque No'

#     def get_bank_name(self, obj):
#         student_class_instance = student_fee.objects.filter(student_id=obj.student_id).order_by('-added_at').first()
#         return student_class_instance.bank_name if student_class_instance else None
#     get_bank_name.short_description = 'Bank Name'

#     def get_branch_name(self, obj):
#         student_class_instance = student_fee.objects.filter(student_id=obj.student_id).order_by('-added_at').first()
#         return student_class_instance.branch_name if student_class_instance else None
#     get_branch_name.short_description = 'Branch Name'

#     def get_total_amount(self, obj):
#         student_class_instance = student_fee.objects.filter(student_id=obj.student_id).order_by('-added_at').first()
#         return student_class_instance.total_amount if student_class_instance else None
#     get_total_amount.short_description = 'Total Amount'

#     def get_amount_paid(self, obj):
#         student_class_instance = student_fee.objects.filter(student_id=obj.student_id).order_by('-added_at').first()
#         return student_class_instance.amount_paid if student_class_instance else None
#     get_amount_paid.short_description = 'Amount Paid'

#     def get_date_entry(self, obj):
#         student_class_instance = student_fee.objects.filter(student_id=obj.student_id).order_by('-added_at').first()
#         return self.format_date(student_class_instance.entry_date) if student_class_instance else None
#     get_date_entry.short_description = 'Date of Entry'

#     def get_queryset(self, request):
#         student_ids_with_open_cheque = student_fee.objects.filter(cheque_status='Open').values_list('student_id', flat=True)
#         queryset = super().get_queryset(request)
#         return queryset.filter(student_id__in=student_ids_with_open_cheque)
    
#     # def changelist_view(self, request, extra_context=None):
#     #     if request.method == 'POST' and 'apply' in request.POST:
#     #         realized_date_form = RealizedDateForm(request.POST)
#     #         if realized_date_form.is_valid():
#     #             realized_date = realized_date_form.cleaned_data['realized_date']
#     #             request.session['realized_date'] = str(realized_date)
#     #     else:
#     #         realized_date_form = RealizedDateForm()

#     #     extra_context = extra_context or {}
#     #     extra_context['realized_date_form'] = realized_date_form

#     #     return super().changelist_view(request, extra_context=extra_context)

#     def mark_as_realized(self, request, queryset):
#         realized_date = request.session.get('realized_date')
#         if realized_date:
#             queryset.update(cheque_status='Realized', realized_date=realized_date)
#         self.message_user(request, "Selected records marked as Realized.")
    
#     mark_as_realized.short_description = "Mark selected as Realized"

#     def mark_as_rejected(self, request, queryset):
#         realized_date = request.session.get('realized_date')
#         if realized_date:
#             queryset.update(cheque_status='Rejected', realized_date=realized_date)
#         self.message_user(request, "Selected records marked as Rejected.")
    
#     mark_as_rejected.short_description = "Mark selected as Rejected"

# admin.site.register(cheque_status, ChequeStatusListAdmin)


# class ChequeStatusListAdmin(admin.ModelAdmin):
#     list_display = (
#         'addmission_no', 'Class', 'Section', 'student_name', 'FeesPeriod',
#         'Year', 'DatePayment', 'ChequeStatus', 'CheqNo', 'BankName',
#         'BranchName', 'TotalAmount', 'AmountPaid', 'DateEntry'
#     )
#     search_fields = [
#         'addmission_no', 'student_name', 'student_fee__year', 
#         'student_fee__date_payment', 'student_fee__cheque_status', 
#         'student_fee__cheq_no', 'student_fee__bank_name', 
#         'student_fee__branch_name', 'student_fee__total_amount', 
#         'student_fee__amount_paid', 'student_fee__entry_date'
#     ]
#     actions = ['mark_as_realized', 'mark_as_rejected']

    
#     def get_class(self, obj):
#         student_class_instance = student_fee.objects.filter(student_id=obj.student_id).order_by('-added_at').first()
#         return student_class_instance.student_class if student_class_instance else None
#     get_class.short_description = 'Class'

#     def get_section(self, obj):
#         student_class_instance = student_fee.objects.filter(student_id=obj.student_id).order_by('-added_at').first()
#         return student_class_instance.student_section if student_class_instance else None
#     get_section.short_description = 'Section'

#     def get_fees_period(self, obj):
#         student_class_instance = student_fee.objects.filter(student_id=obj.student_id).order_by('-added_at').first()
#         return student_class_instance.fees_period_month if student_class_instance else None
#     get_fees_period.short_description = 'Fees Period Month'

#     def get_year(self, obj):
#         student_class_instance = student_fee.objects.filter(student_id=obj.student_id).order_by('-added_at').first()
#         return student_class_instance.year if student_class_instance else None
#     get_year.short_description = 'Year'

#     def get_date_payment(self, obj):
#         student_class_instance = student_fee.objects.filter(student_id=obj.student_id).order_by('-added_at').first()
#         return student_class_instance.date_payment if student_class_instance else None
#     get_date_payment.short_description = 'Date Payment'

#     def get_cheque_status(self, obj):
#         student_class_instance = student_fee.objects.filter(student_id=obj.student_id).order_by('-added_at').first()
#         return student_class_instance.cheque_status if student_class_instance else None
#     get_cheque_status.short_description = 'Cheque Status'

#     def get_cheq_no(self, obj):
#         student_class_instance = student_fee.objects.filter(student_id=obj.student_id).order_by('-added_at').first()
#         return student_class_instance.cheq_no if student_class_instance else None
#     get_cheq_no.short_description = 'Cheque No'

#     def get_bank_name(self, obj):
#         student_class_instance = student_fee.objects.filter(student_id=obj.student_id).order_by('-added_at').first()
#         return student_class_instance.bank_name if student_class_instance else None
#     get_bank_name.short_description = 'Bank Name'

#     def get_branch_name(self, obj):
#         student_class_instance = student_fee.objects.filter(student_id=obj.student_id).order_by('-added_at').first()
#         return student_class_instance.branch_name if student_class_instance else None
#     get_branch_name.short_description = 'Branch Name'

#     def get_total_amount(self, obj):
#         student_class_instance = student_fee.objects.filter(student_id=obj.student_id).order_by('-added_at').first()
#         return student_class_instance.total_amount if student_class_instance else None
#     get_total_amount.short_description = 'Total Amount'

#     def get_amount_paid(self, obj):
#         student_class_instance = student_fee.objects.filter(student_id=obj.student_id).order_by('-added_at').first()
#         return student_class_instance.amount_paid if student_class_instance else None
#     get_amount_paid.short_description = 'Amount Paid'

#     def get_date_entry(self, obj):
#         student_class_instance = student_fee.objects.filter(student_id=obj.student_id).order_by('-added_at').first()
#         return student_class_instance.entry_date if student_class_instance else None
#     get_date_entry.short_description = 'Date of Entry'

#     def get_queryset(self, request):
#         student_ids_with_open_cheque = student_fee.objects.filter(cheque_status='Open').values_list('student_id', flat=True)
#         queryset = super().get_queryset(request)
#         return queryset.filter(student_id__in=student_ids_with_open_cheque)

#     def changelist_view(self, request, extra_context=None):
#         if request.method == 'POST' and 'apply' in request.POST:
#             realized_date_form = RealizedDateForm(request.POST)
#             if realized_date_form.is_valid():
#                 realized_date = realized_date_form.cleaned_data['realized_date']
#                 # Store the realized_date in the session to use in actions
#                 request.session['realized_date'] = str(realized_date)
#         else:
#             realized_date_form = RealizedDateForm()

#         extra_context = extra_context or {}
#         extra_context['realized_date_form'] = realized_date_form

#         return super().changelist_view(request, extra_context=extra_context)

#     def mark_as_realized(self, request, queryset):
#         realized_date = request.session.get('realized_date')
#         if realized_date:
#             queryset.update(cheque_status='Realized', realized_date=realized_date)
#         self.message_user(request, "Selected records marked as Realized.")
    
#     mark_as_realized.short_description = "Mark selected as Realized"

#     def mark_as_rejected(self, request, queryset):
#         realized_date = request.session.get('realized_date')
#         if realized_date:
#             queryset.update(cheque_status='Rejected', realized_date=realized_date)
#         self.message_user(request, "Selected records marked as Rejected.")
    
#     mark_as_rejected.short_description = "Mark selected as Rejected"


admin.site.register(cheque_status, ChequeStatusListAdmin)







