from django.contrib import admin
from .models import (
    student_master, student_fee, student_class, specialfee_master,
    payment_schedule_master, latefee_master, fees_master, expense,
    concession_master, bus_master, busfees_master, account_head,generate_mobile_number_list, 
)
from django.db.models import Max
from django import forms
from datetime import date
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
from datetime import datetime

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

from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _

import time
import logging

from django.utils.dateparse import parse_date
from datetime import datetime
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import get_object_or_404
# from multiselectfield import MultiSelectField

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
MONTHS = [
    ('', 'Please Select Month'),
    ('1', 'January'),
    ('2', 'February'),
    ('3', 'March'),
    ('4', 'April'),
    ('5', 'May'),
    ('6', 'June'),
    ('7', 'July'),
    ('8', 'August'),
    ('9', 'September'),
    ('10', 'October'),
    ('11', 'November'),
    ('12', 'December'),
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

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .forms import CustomUserCreationForm, CustomUserChangeForm
from django.http import HttpResponseRedirect 

class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm

    form = CustomUserChangeForm

    # list_display = ('email', 'username', 'first_name', 'is_staff')  # Use username as teacher_name
    list_display = ('email', 'get_teacher_name', 'get_mobile', 'get_role_display')
    search_fields = ('email', 'username')
    list_filter = ()

    # fieldsets = (
    #     (None, {'fields': ('email', 'username', 'first_name', 'password')}),
    #     ('Permissions', {'fields': ('is_staff', 'is_superuser', 'is_active')}),
    #     ('Important dates', {'fields': ('last_login', 'date_joined')}),
    # )
    # fieldsets = (
    #     (None, {'fields': ('email', 'username', 'first_name', 'role', 'password'),}),
    # )
    fieldsets = (
        (None, {'fields': ('email', 'username', 'first_name', 'role', 'password')}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'first_name', 'role', 'password'),
        }),
    )

    def get_teacher_name(self, obj):
        """ Return the username as Teacher Name. """
        return obj.username
    get_teacher_name.short_description = 'Teacher Name'  # Set column name

    def get_mobile(self, obj):
        """ Return the first_name as Mobile Number. """
        return obj.first_name
    get_mobile.short_description = 'Mobile'  # Set column name

    def get_role_display(self, obj):
        """ Return Admin or Super Admin based on is_superuser. """
        return 'Super Admin' if obj.is_superuser else 'Admin'
    get_role_display.short_description = 'Role'  # Set column name

    def response_add(self, request, obj, post_url_continue=None):
        """ Redirect to the user list page after successfully adding a user. """
        return HttpResponseRedirect("/school-admin/auth/user/") 

# Unregister the default UserAdmin and register the customized one
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)





# Define choices for months (1 to 12)
#MONTH_CHOICES = [(str(i), str(i)) for i in range(1, 13)]
# Register your models here.

# class TeacherMasterForm(forms.ModelForm):
#     # role = forms.ChoiceField(choices=teacher_master.ROLES_CHOICES, required=True)
#     role = forms.ChoiceField(choices=user.ROLES_CHOICES, required=True)

#     class Meta:
#         model = user
#         fields = [
#             "user_name", "email", "mobile","role"
#         ]


# class UserDisplay(admin.ModelAdmin):
#     form = TeacherMasterForm
#     list_display = ("teacher_name", "email", "mobile", "role")
#     search_fields = ("user_name", "email", "mobile", "role")
#     list_filter = ("role",)

#     def teacher_name(self, obj):
#         return obj.user_name  # Assuming user_name is the field in the model
    
#     teacher_name.short_description = 'Teacher Name'

#     def get_queryset(self, request):
#         # Get the original queryset
#         queryset = super().get_queryset(request)

#         # Retrieve the search terms from the GET parameters
#         user_name = request.GET.get('user_name', '')
#         email = request.GET.get('email', '')
#         mobile = request.GET.get('mobile', '')
#         role = request.GET.get('role', '')

#         # Apply filters based on the search terms
#         if user_name:
#             queryset = queryset.filter(user_name__icontains=user_name)
#         if email:
#             queryset = queryset.filter(email__icontains=email)
#         if mobile:
#             queryset = queryset.filter(mobile__icontains=mobile)
#         if role:
#             queryset = queryset.filter(role__icontains=role)

#         return queryset

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
    
# Custom filter for admission_no
class AdmissionNoFilter(admin.SimpleListFilter):
    title = 'Admission No'
    parameter_name = 'search_admission_no'

    def lookups(self, request, model_admin):
        return []

    # def queryset(self, request, queryset):
    #     search_admission_no = self.value()  # Get the value from the request
    #     if search_admission_no:
    #         return queryset.filter(addmission_no__icontains=search_admission_no)
    #     return queryset


# Custom filter for student_name
class StudentNameFilter(admin.SimpleListFilter):
    title = 'Student Name'
    parameter_name = 'search_student_name'

    def lookups(self, request, model_admin):
        return []

    # def queryset(self, request, queryset):
    #     search_student_name = self.value()  # Get the value from the request
    #     if search_student_name:
    #         return queryset.filter(student_name__icontains=search_student_name)
    #     return queryset


class ClassNoFilter(admin.SimpleListFilter):
    title = 'Class No'
    parameter_name = 'search_class_no'

    def lookups(self, request, model_admin):
        return []

class SectionFilter(admin.SimpleListFilter):
    title = 'Section'
    parameter_name = 'search_section'

    def lookups(self, request, model_admin):
        return []

class StudentMasterAdmin(admin.ModelAdmin):
    form = StudentMasterForm
    list_display = ('student_id', 'student_name', 'get_class_no', 'get_section', 'addmission_no', 'father_name', 'mother_name', 'gender', 'birth_date', 'category', 'status', 'admission_date', 'passedout_date')
    # search_fields = ('student_name', 'addmission_no', 'aadhaar_no', 'email', 'city', 'birth_date')

    # Add custom filters to the list filter
    list_filter = (AdmissionNoFilter, StudentNameFilter, ClassNoFilter, SectionFilter)

    def get_queryset(self, request):
        # Get the base queryset
        qs = super().get_queryset(request)

        # Store the request in the instance for later use
        self._request = request
        
        # Custom filtering for search_class_no
        search_class_no = request.GET.get('search_class_no', None)
        search_section = request.GET.get('search_section', None)

        if search_class_no and search_section:
            student_ids = student_class.objects.filter(class_no=search_class_no,section=search_section).values_list('student_id', flat=True)
            qs = qs.filter(student_id__in=student_ids)
        elif search_class_no:
            student_ids = student_class.objects.filter(class_no=search_class_no).values_list('student_id', flat=True)
            qs = qs.filter(student_id__in=student_ids)
        elif search_section:
            student_ids_by_section = student_class.objects.filter(section=search_section).values_list('student_id', flat=True)
            qs = qs.filter(student_id__in=student_ids_by_section)
                
        return qs

    # Override get_search_results to handle custom search logic
    def get_search_results(self, request, queryset, search_term):
        search_admission_no = request.GET.get('search_admission_no', None)
        search_student_name = request.GET.get('search_student_name', None)

        # Apply custom filters for admission_no and student_name
        if search_admission_no:
            queryset = queryset.filter(addmission_no__icontains=search_admission_no)
        if search_student_name:
            queryset = queryset.filter(student_name__icontains=search_student_name)

        # Return the modified queryset and a boolean for whether distinct is needed
        return queryset, False

    def changelist_view(self, request, extra_context=None):
        # Adding extra context for the search fields in the template
        extra_context = extra_context or {}
        extra_context['search_admission_no'] = request.GET.get('search_admission_no', '')
        extra_context['search_student_name'] = request.GET.get('search_student_name', '')
        extra_context['search_class_no'] = request.GET.get('search_class_no', '')
        extra_context['search_section'] = request.GET.get('search_section', '')
        
        return super().changelist_view(request, extra_context=extra_context)

    # Customize the changelist template to include custom search fields
    change_list_template = 'admin/student_master_changelist.html'

    def get_class_no(self, obj):
        search_class_no = self._request.GET.get('search_class_no', None)
        search_section = self._request.GET.get('search_section', None)

        # Filter by class_no and/or section if available
        if search_class_no and search_section:
            student_class_instance = student_class.objects.filter(student_id=obj.student_id, class_no=search_class_no, section=search_section).order_by('-started_on').first()
        elif search_class_no:
            student_class_instance = student_class.objects.filter(student_id=obj.student_id, class_no=search_class_no).order_by('-started_on').first()
        elif search_section:
            student_class_instance = student_class.objects.filter(student_id=obj.student_id, section=search_section).order_by('-started_on').first()
        else:
            student_class_instance = student_class.objects.filter(student_id=obj.student_id).order_by('-started_on').first()

        return student_class_instance.class_no if student_class_instance else None
    get_class_no.short_description = 'Class'

    def get_section(self, obj):
        search_class_no = self._request.GET.get('search_class_no', None)
        search_section = self._request.GET.get('search_section', None)

        # Filter by class_no and/or section if available
        if search_class_no and search_section:
            student_class_instance = student_class.objects.filter(student_id=obj.student_id, class_no=search_class_no, section=search_section).order_by('-started_on').first()
        elif search_class_no:
            student_class_instance = student_class.objects.filter(student_id=obj.student_id, class_no=search_class_no).order_by('-started_on').first()
        elif search_section:
            student_class_instance = student_class.objects.filter(student_id=obj.student_id, section=search_section).order_by('-started_on').first()
        else:
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

admin.site.register(student_master, StudentMasterAdmin)


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

class ClassNoFilter(admin.SimpleListFilter):
    title = 'Class No'
    parameter_name = 'search_class_no'

    def lookups(self, request, model_admin):
        return []

class AnnualFeesFilter(admin.SimpleListFilter):
    title = 'Annual Fees'
    parameter_name = 'search_annual_fees'

    def lookups(self, request, model_admin):
        return []

class TuitionFeesFilter(admin.SimpleListFilter):
    title = 'Tuition Fees'
    parameter_name = 'search_tuition_fees'

    def lookups(self, request, model_admin):
        return []

class FundsFeesFilter(admin.SimpleListFilter):
    title = 'Funds Fees'
    parameter_name = 'search_funds_fees'

    def lookups(self, request, model_admin):
        return []

class SportsFeesFilter(admin.SimpleListFilter):
    title = 'Sports Fees'
    parameter_name = 'search_sports_fees'

    def lookups(self, request, model_admin):
        return []

class ActivityFeesFilter(admin.SimpleListFilter):
    title = 'Activity Fees'
    parameter_name = 'search_activity_fees'

    def lookups(self, request, model_admin):
        return []

class AdmissionFeesFilter(admin.SimpleListFilter):
    title = 'Admission Fees'
    parameter_name = 'search_admission_fees'

    def lookups(self, request, model_admin):
        return []

class DayboardingFeesFilter(admin.SimpleListFilter):
    title = 'Dayboarding Fees'
    parameter_name = 'search_dayboarding_fees'

    def lookups(self, request, model_admin):
        return []

class MiscellaneousFeesFilter(admin.SimpleListFilter):
    title = 'Miscellaneous Fees'
    parameter_name = 'search_miscel_fees'

    def lookups(self, request, model_admin):
        return []

class FeesMasterAdmin(admin.ModelAdmin):
    form = FeesMasterForm
    list_display = ("fees_id", "class_no", "annual_fees", "tuition_fees", "funds_fees", "sports_fees", "activity_fees", "admission_fees", "dayboarding_fees", "miscellaneous_fees", "valid_from", "valid_to")
    list_filter = (ClassNoFilter, AnnualFeesFilter, TuitionFeesFilter, FundsFeesFilter, SportsFeesFilter, ActivityFeesFilter, AdmissionFeesFilter, DayboardingFeesFilter, MiscellaneousFeesFilter)

    def get_search_results(self, request, queryset, search_term):
        search_class_no = request.GET.get('search_class_no', None)
        search_annual_fees = request.GET.get('search_annual_fees', None)
        search_tuition_fees = request.GET.get('search_tuition_fees', None)
        search_funds_fees = request.GET.get('search_funds_fees', None)
        search_sports_fees = request.GET.get('search_sports_fees', None)
        search_activity_fees = request.GET.get('search_activity_fees', None)
        search_admission_fees = request.GET.get('search_admission_fees', None)
        search_dayboarding_fees = request.GET.get('search_dayboarding_fees', None)
        search_miscel_fees = request.GET.get('search_miscel_fees', None)


        # Apply custom filters for admission_no and student_name
        if search_class_no:
            queryset = queryset.filter(class_no=search_class_no)
        if search_annual_fees:
            queryset = queryset.filter(annual_fees=search_annual_fees)
        if search_tuition_fees:
            queryset = queryset.filter(tuition_fees=search_tuition_fees)
        if search_funds_fees:
            queryset = queryset.filter(funds_fees=search_funds_fees)
        if search_sports_fees:
            queryset = queryset.filter(sports_fees=search_sports_fees)
        if search_activity_fees:
            queryset = queryset.filter(activity_fees=search_activity_fees)
        if search_admission_fees:
            queryset = queryset.filter(admission_fees=search_admission_fees)
        if search_dayboarding_fees:
            queryset = queryset.filter(dayboarding_fees=search_dayboarding_fees)
        if search_miscel_fees:
            queryset = queryset.filter(miscellaneous_fees=search_miscel_fees)
        

        # Return the modified queryset and a boolean for whether distinct is needed
        return queryset, False

    def changelist_view(self, request, extra_context=None):
        # Adding extra context for the search fields in the template
        extra_context = extra_context or {}
        extra_context['search_class_no'] = request.GET.get('search_class_no', '')
        extra_context['search_annual_fees'] = request.GET.get('search_annual_fees', '')
        extra_context['search_tuition_fees'] = request.GET.get('search_tuition_fees', '')
        extra_context['search_funds_fees'] = request.GET.get('search_funds_fees', '')
        extra_context['search_sports_fees'] = request.GET.get('search_sports_fees', '')
        extra_context['search_activity_fees'] = request.GET.get('search_activity_fees', '')
        extra_context['search_admission_fees'] = request.GET.get('search_admission_fees', '')
        extra_context['search_dayboarding_fees'] = request.GET.get('search_dayboarding_fees', '')
        extra_context['search_miscel_fees'] = request.GET.get('search_miscel_fees', '')

        return super().changelist_view(request, extra_context=extra_context)

    change_list_template = 'admin/fees_master_changelist.html'

# admin.site.register(student_master,StudentMasterAdmin)
# admin.site.register(user, UserDisplay)
# admin.site.register(teacher_master, UserDisplay)
# admin.site.register(user, UserDisplay)
# admin.site.register(account_head)

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

    # Override delete_queryset to handle delete errors during confirmation
    def delete_queryset(self, request, queryset):
        try:
            with transaction.atomic():
                # Attempt to delete the selected objects inside a transaction block
                num_deleted = queryset.count()  # Check the count before attempting to delete
                queryset.delete()  # Attempt to delete
                if num_deleted > 0:
                    messages.success(request, _("Successfully deleted %d record(s)." % num_deleted))
        except IntegrityError:
            # If a foreign key constraint error occurs, show only the error message
            messages.error(request, _("Cannot delete some of the selected records as they are referenced by other data. Please remove the dependencies first."))

    # Optionally override the delete_model to handle individual deletion as well
    def delete_model(self, request, obj):
        try:
            obj.delete()
            # messages.success(request, _("Record deleted successfully!"))
        except IntegrityError:
            messages.error(request, _("Cannot delete the record because it is referenced by other data."))

    class Media:
        js = ('app/js/bus_master.js',)

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

from django.contrib import messages
from django.db import IntegrityError, transaction
from django.utils.translation import gettext_lazy as _

class BusMaster(ExportMixin, admin.ModelAdmin):
    resource_class = BusMasterResource
    list_display = ("bus_route", "bus_driver", "bus_conductor", "bus_attendant", "driver_phone", "conductor_phone", "attendant_phone")
    search_fields = ("bus_route", "bus_driver", "bus_conductor", "bus_attendant", "driver_phone", "conductor_phone", "attendant_phone")

    # Override delete_queryset to handle delete errors during confirmation
    def delete_queryset(self, request, queryset):
        try:
            with transaction.atomic():
                # Attempt to delete the selected objects inside a transaction block
                num_deleted = queryset.count()  # Check the count before attempting to delete
                queryset.delete()  # Attempt to delete
                if num_deleted > 0:
                    messages.success(request, _("Successfully deleted %d record(s)." % num_deleted))
        except IntegrityError:
            # If a foreign key constraint error occurs, show only the error message
            messages.error(request, _("Cannot delete some of the selected records as they are referenced by other data. Please remove the dependencies first."))

    # Optionally override the delete_model to handle individual deletion as well
    def delete_model(self, request, obj):
        try:
            obj.delete()
            # messages.success(request, _("Record deleted successfully!"))
        except IntegrityError:
            messages.error(request, _("Cannot delete the record because it is referenced by other data."))

    # Override the save_model method to catch IntegrityError
    def save_model(self, request, obj, form, change):
        try:
            with transaction.atomic():
                super().save_model(request, obj, form, change)
        except IntegrityError as e:
            if '1451' in str(e):  # Check if it's the specific foreign key error
                messages.error(request, _("Cannot update this bus route because it is referenced in the bus fees. Please update or remove the related records first."))
            else:
                messages.error(request, _("An error occurred while saving the record."))

    class Media:
        js = ('app/js/bus_master.js',)

admin.site.register(bus_master, BusMaster)




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
# admin.site.register(expense)

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
    )

    days_to = forms.ChoiceField(
        choices=Pay_In_Month_CHOICES,
    )

    Latefee_Type_CHOICES = [
        ('', 'Select Type'),
        ('fixed', 'Fixed'),
        ('per day', 'Per Day'),
        ('no charge', 'No Charge'),
    ]

    latefee_type = forms.ChoiceField(
        choices=Latefee_Type_CHOICES,
    )

    class Meta:
        model = latefee_master
        fields = '__all__'

    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Get the instance being edited
        instance = kwargs.get('instance')
        selected_days_from = int(instance.days_from) if instance and instance.days_from.isdigit() else None
        selected_days_to = int(instance.days_to) if instance and instance.days_to.isdigit() else None

        print('selected_days_from',selected_days_from)
        print('selected_days_to',selected_days_to)

        
        # Exclude non-numeric values and get existing ranges
        # existing_ranges = latefee_master.objects.exclude(days_from__in=['', None, 'till current date']).exclude(days_to__in=['', None, 'till current date']).values_list('days_from', 'days_to')

        existing_ranges = latefee_master.objects.exclude(days_from__in=['', None]).exclude(days_to__in=['', None]).values_list('days_from', 'days_to')

        print('existing_ranges',existing_ranges)
        
        excluded_days = set()
        
        # Calculate excluded days only for numeric values
        for days_from, days_to in existing_ranges:
            # if str(days_to) == "90":
            #     continue  # Keep "90" available
            try:
                excluded_days.update(range(int(days_from), int(days_to) + 1))
            except ValueError:
                continue  # Skip non-numeric values

        print('excluded_days',excluded_days)
        # Check if 'till current date' is present in either days_from or days_to
        is_till_current_date_present = any('till current date' in (days_from, days_to) for days_from, days_to in existing_ranges)


        # Define available numeric choices for the form fields
        if selected_days_from is not None and selected_days_to is not None:
            # If editing, restrict the choices to the selected range (days_from to days_to)
            numeric_choices = [(str(i), str(i)) for i in range(selected_days_from, selected_days_to + 1)]

            available_choices = [
                ('', 'Please Select Day'),
            ] + numeric_choices

        elif is_till_current_date_present:
            numeric_choices = [(str(i), str(i)) for i in range(1, 91) if i not in excluded_days]

            available_choices = [
                ('', 'Please Select Day'),
            ] + numeric_choices 

        elif 90 in excluded_days:
            numeric_choices = [(str(i), str(i)) for i in range(1, 91) if i not in excluded_days]

            available_choices = [
                ('', 'Please Select Day'),
            ] + numeric_choices + [
                ('90', '90'),('till current date', 'Till Current Date')
            ]
    
        else:
            # If not editing, exclude the existing ranges
            numeric_choices = [(str(i), str(i)) for i in range(1, 91) if i not in excluded_days]

            available_choices = [
                ('', 'Please Select Day'),
            ] + numeric_choices + [
                ('till current date', 'Till Current Date')
            ]
        
        self.fields['days_from'].choices = available_choices
        self.fields['days_from'].initial = str(selected_days_from) if selected_days_from else ''
        self.fields['days_from'].required = False  # Not required
        self.fields['days_to'].choices = available_choices
        self.fields['days_to'].initial = str(selected_days_to) if selected_days_to else ''
        self.fields['days_to'].required = False  # Not required

        # Generate the HTML table to display existing LateFeeMaster records
        records = latefee_master.objects.all()

        listing_html = """
            <h3>Existing Late Fees</h3>
            <table style='border: 1px solid #ddd; width: 100%; border-collapse: collapse;'>
                <thead>
                    <tr>
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


class LateFeeMasterDisplay(admin.ModelAdmin):
    form = LateFeeMasterForm
    list_display = ("days_from", "days_to", "latefee", "latefee_type", "latefee_desc")

admin.site.register(latefee_master, LateFeeMasterDisplay)

# class LateFeeMasterForm(forms.ModelForm):
#     listing = forms.CharField(widget=ReadOnlyCKEditorWidget(), required=False, label='')

#     # Pay_In_Month_CHOICES with "Till Current Date" option and numeric values
#     Pay_In_Month_CHOICES = [
#         ('', 'Please Select Day'),
#     ] + [(str(i), str(i)) for i in range(1, 91)] + [
#         ('till current date', 'Till Current Date')
#     ]

#     days_from = forms.ChoiceField(choices=Pay_In_Month_CHOICES)
#     days_to = forms.ChoiceField(choices=Pay_In_Month_CHOICES)
    
#     Latefee_Type_CHOICES = [
#         ('', 'Select Type'),
#         ('fixed', 'Fixed'),
#         ('per day', 'Per Day'),
#         ('no charge', 'No Charge'),
#     ]

#     latefee_type = forms.ChoiceField(choices=Latefee_Type_CHOICES)

#     class Meta:
#         model = latefee_master
#         fields = '__all__'

#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
        
#         # Get the instance being edited
#         instance = kwargs.get('instance')
#         selected_days_from = instance.days_from if instance else None
#         selected_days_to = instance.days_to if instance else None
        
#         # Exclude non-numeric values and get existing ranges
#         existing_ranges = latefee_master.objects.exclude(days_from__in=['', None, 'till current date']).exclude(days_to__in=['', None, 'till current date']).values_list('days_from', 'days_to')
        
#         excluded_days = set()
        
#         # Calculate excluded days only for numeric values, but keep "90" always available
#         for days_from, days_to in existing_ranges:
#             if str(days_to) == "90":
#                 continue  # Keep "90" available
#             try:
#                 excluded_days.update(range(int(days_from), int(days_to) + 1))
#             except ValueError:
#                 continue  # Skip non-numeric values

#         # Include the currently selected days_from and days_to in the choices
#         numeric_choices = [(str(i), str(i)) for i in range(1, 91) if i not in excluded_days or str(i) in (selected_days_from, selected_days_to)]
#         available_choices = [
#             ('', 'Please Select Day'),
#         ] + numeric_choices + [
#             ('till current date', 'Till Current Date')
#         ]

#         # Update choices for the form fields
#         self.fields['days_from'].choices = available_choices
#         self.fields['days_from'].initial = selected_days_from
#         self.fields['days_from'].required = False  # Not required

#         self.fields['days_to'].choices = available_choices
#         self.fields['days_to'].initial = selected_days_to
#         self.fields['days_to'].required = False  # Not required

#         # Display existing late fees in a table
#         listing_html = """
#             <h3>Existing Late Fees</h3>
#             <table style='border: 1px solid #ddd; width: 100%; border-collapse: collapse;'>
#                 <tr>
#                     <th>Days From</th>
#                     <th>Days To</th>
#                     <th>Late Fee</th>
#                     <th>Type</th>
#                     <th>Description</th>
#                 </tr>
#         """
#         # Query existing records for display in listing
#         for latefee in latefee_master.objects.all():
#             listing_html += f"""
#                 <tr>
#                     <td>{latefee.days_from}</td>
#                     <td>{latefee.days_to}</td>
#                     <td>{latefee.latefee}</td>
#                     <td>{latefee.latefee_type}</td>
#                     <td>{latefee.latefee_desc}</td>
#                 </tr>
#             """
        
#         listing_html += "</table>"

#         # Assign the marked-safe HTML to the custom form field
#         self.fields['listing'].initial = mark_safe(listing_html)


# class LateFeeMasterDisplay(admin.ModelAdmin):
#     form = LateFeeMasterForm
#     list_display = ("days_from", "days_to", "latefee", "latefee_type", "latefee_desc")

# admin.site.register(latefee_master, LateFeeMasterDisplay)



# class LateFeeMasterForm(forms.ModelForm):
#     listing = forms.CharField(widget=ReadOnlyCKEditorWidget(), required=False, label='')

#     # Pay_In_Month_CHOICES with "Till Current Date" option and numeric values
#     Pay_In_Month_CHOICES = [
#         ('', 'Please Select Day'),
#     ] + [(str(i), str(i)) for i in range(1, 91)] + [
#         ('till current date', 'Till Current Date')
#     ]

#     days_from = forms.ChoiceField(choices=Pay_In_Month_CHOICES)
#     days_to = forms.ChoiceField(choices=Pay_In_Month_CHOICES)

#     Latefee_Type_CHOICES = [
#         ('', 'Select Type'),
#         ('fixed', 'Fixed'),
#         ('per day', 'Per Day'),
#         ('no charge', 'No Charge'),
#     ]

#     latefee_type = forms.ChoiceField(choices=Latefee_Type_CHOICES)

#     class Meta:
#         model = latefee_master
#         fields = '__all__'

#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)

#         # Get the instance being edited
#         instance = kwargs.get('instance')
#         selected_days_from = int(instance.days_from) if instance and instance.days_from.isdigit() else None
#         selected_days_to = int(instance.days_to) if instance and instance.days_to.isdigit() else None

#         # Exclude non-numeric values and get existing ranges
#         existing_ranges = latefee_master.objects.exclude(days_from__in=['', None, 'till current date']).exclude(days_to__in=['', None, 'till current date']).values_list('days_from', 'days_to')

#         excluded_days = set()
        
#         # Calculate excluded days based on existing records' ranges
#         for days_from, days_to in existing_ranges:
#             if str(days_to) == "90":
#                 continue  # Keep "90" available
#             try:
#                 excluded_days.update(range(int(days_from), int(days_to) + 1))
#             except ValueError:
#                 continue  # Skip non-numeric values
        
#         # Include the currently selected range only for numeric choices
#         if selected_days_from is not None and selected_days_to is not None:
#             numeric_choices = [(str(i), str(i)) for i in range(selected_days_from, selected_days_to + 1) if i not in excluded_days or str(i) in (str(selected_days_from), str(selected_days_to))]
#         else:
#             numeric_choices = [(str(i), str(i)) for i in range(1, 91) if i not in excluded_days]

#         available_choices = [
#             ('', 'Please Select Day'),
#         ] + numeric_choices + [
#             ('till current date', 'Till Current Date')
#         ]

#         # Update choices for the form fields
#         self.fields['days_from'].choices = available_choices
#         self.fields['days_from'].initial = str(selected_days_from) if selected_days_from else ''
#         self.fields['days_from'].required = False  # Not required

#         self.fields['days_to'].choices = available_choices
#         self.fields['days_to'].initial = str(selected_days_to) if selected_days_to else ''
#         self.fields['days_to'].required = False  # Not required

#         # Display existing late fees in a table
#         listing_html = """
#             <h3>Existing Late Fees</h3>
#             <table style='border: 1px solid #ddd; width: 100%; border-collapse: collapse;'>
#                 <tr>
#                     <th>Days From</th>
#                     <th>Days To</th>
#                     <th>Late Fee</th>
#                     <th>Type</th>
#                     <th>Description</th>
#                 </tr>
#         """
#         # Query existing records for display in listing
#         for latefee in latefee_master.objects.all():
#             listing_html += f"""
#                 <tr>
#                     <td>{latefee.days_from}</td>
#                     <td>{latefee.days_to}</td>
#                     <td>{latefee.latefee}</td>
#                     <td>{latefee.latefee_type}</td>
#                     <td>{latefee.latefee_desc}</td>
#                 </tr>
#             """
        
#         listing_html += "</table>"

#         # Assign the marked-safe HTML to the custom form field
#         self.fields['listing'].initial = mark_safe(listing_html)


# class LateFeeMasterDisplay(admin.ModelAdmin):
#     form = LateFeeMasterForm
#     list_display = ("days_from", "days_to", "latefee", "latefee_type", "latefee_desc")

# admin.site.register(latefee_master, LateFeeMasterDisplay)



# class LateFeeMasterForm(forms.ModelForm):
#     listing = forms.CharField(widget=ReadOnlyCKEditorWidget(), required=False, label='')

#     # Pay_In_Month_CHOICES with "Till Current Date" option and numeric values
#     Pay_In_Month_CHOICES = [
#         ('', 'Please Select Day'),
#     ] + [(str(i), str(i)) for i in range(1, 91)] + [
#         ('till current date', 'Till Current Date')
#     ]

#     days_from = forms.ChoiceField(choices=Pay_In_Month_CHOICES)
#     days_to = forms.ChoiceField(choices=Pay_In_Month_CHOICES)

#     Latefee_Type_CHOICES = [
#         ('', 'Select Type'),
#         ('fixed', 'Fixed'),
#         ('per day', 'Per Day'),
#         ('no charge', 'No Charge'),
#     ]

#     latefee_type = forms.ChoiceField(choices=Latefee_Type_CHOICES)

#     class Meta:
#         model = latefee_master
#         fields = '__all__'

#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)

#         # Get the instance being edited
#         instance = kwargs.get('instance')
#         selected_days_from = int(instance.days_from) if instance and instance.days_from.isdigit() else None
#         selected_days_to = int(instance.days_to) if instance and instance.days_to.isdigit() else None

#         # Exclude non-numeric values and get existing ranges
#         existing_ranges = latefee_master.objects.exclude(
#             days_from__in=['', None, 'till current date']
#         ).exclude(
#             days_to__in=['', None, 'till current date']
#         ).values_list('days_from', 'days_to')

#         excluded_days = set()

#         # Calculate excluded days based on existing records' ranges
#         for days_from, days_to in existing_ranges:
#             if str(days_to) == "90":
#                 continue  # Keep "90" available
#             try:
#                 excluded_days.update(range(int(days_from), int(days_to) + 1))
#             except ValueError:
#                 continue  # Skip non-numeric values

#         # Define available numeric choices for the form fields
#         if selected_days_from is not None and selected_days_to is not None:
#             # If editing, restrict the choices to the selected range (days_from to days_to)
#             numeric_choices = [(str(i), str(i)) for i in range(selected_days_from, selected_days_to + 1)]

#             available_choices = [
#                 ('', 'Please Select Day'),
#             ] + numeric_choices

#         else:
#             # If not editing, exclude the existing ranges
#             numeric_choices = [(str(i), str(i)) for i in range(1, 91) if i not in excluded_days]

#             available_choices = [
#                 ('', 'Please Select Day'),
#             ] + numeric_choices + [
#                 ('till current date', 'Till Current Date')
#             ]

#         # Update choices for the form fields
#         self.fields['days_from'].choices = available_choices
#         self.fields['days_from'].initial = str(selected_days_from) if selected_days_from else ''
#         self.fields['days_from'].required = False  # Not required

#         self.fields['days_to'].choices = available_choices
#         self.fields['days_to'].initial = str(selected_days_to) if selected_days_to else ''
#         self.fields['days_to'].required = False  # Not required

#         # Display existing late fees in a table
#         listing_html = """
#             <h3>Existing Late Fees</h3>
#             <table style='border: 1px solid #ddd; width: 100%; border-collapse: collapse;'>
#                 <tr>
#                     <th>Days From</th>
#                     <th>Days To</th>
#                     <th>Late Fee</th>
#                     <th>Type</th>
#                     <th>Description</th>
#                 </tr>
#         """
#         # Query existing records for display in listing
#         for latefee in latefee_master.objects.all():
#             listing_html += f"""
#                 <tr>
#                     <td>{latefee.days_from}</td>
#                     <td>{latefee.days_to}</td>
#                     <td>{latefee.latefee}</td>
#                     <td>{latefee.latefee_type}</td>
#                     <td>{latefee.latefee_desc}</td>
#                 </tr>
#             """
        
#         listing_html += "</table>"

#         # Assign the marked-safe HTML to the custom form field
#         self.fields['listing'].initial = mark_safe(listing_html)


# class LateFeeMasterDisplay(admin.ModelAdmin):
#     form = LateFeeMasterForm
#     list_display = ("days_from", "days_to", "latefee", "latefee_type", "latefee_desc")

# admin.site.register(latefee_master, LateFeeMasterDisplay)



# class LateFeeMasterForm(forms.ModelForm):
#     listing = forms.CharField(widget=ReadOnlyCKEditorWidget(), required=False, label='')

#     # Pay_In_Month_CHOICES with "Till Current Date" option and numeric values
#     Pay_In_Month_CHOICES = [
#         ('', 'Please Select Day'),
#     ] + [(str(i), str(i)) for i in range(1, 91)] + [
#         ('till current date', 'Till Current Date')
#     ]

#     days_from = forms.ChoiceField(choices=Pay_In_Month_CHOICES)
#     days_to = forms.ChoiceField(choices=Pay_In_Month_CHOICES)

#     Latefee_Type_CHOICES = [
#         ('', 'Select Type'),
#         ('fixed', 'Fixed'),
#         ('per day', 'Per Day'),
#         ('no charge', 'No Charge'),
#     ]

#     latefee_type = forms.ChoiceField(choices=Latefee_Type_CHOICES)

#     class Meta:
#         model = latefee_master
#         fields = '__all__'

#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)

#         # Get the instance being edited
#         instance = kwargs.get('instance')
#         selected_days_from = int(instance.days_from) if instance and instance.days_from.isdigit() else None
#         selected_days_to = int(instance.days_to) if instance and instance.days_to.isdigit() else None

#         # Exclude non-numeric values and get existing ranges
#         existing_ranges = latefee_master.objects.exclude(
#             days_from__in=['', None, 'till current date']
#         ).exclude(
#             days_to__in=['', None, 'till current date']
#         ).values_list('days_from', 'days_to')

#         excluded_days = set()

#         # Calculate excluded days based on existing records' ranges
#         for days_from, days_to in existing_ranges:
#             if str(days_to) == "90":
#                 continue  # Always allow 90 and "Till Current Date" to be available
#             try:
#                 excluded_days.update(range(int(days_from), int(days_to) + 1))
#             except ValueError:
#                 continue  # Skip non-numeric values

#         # Define available numeric choices for the form fields
#         if selected_days_from is not None and selected_days_to is not None:
#             # If editing, restrict the choices to the selected range (days_from to days_to)
#             numeric_choices = [(str(i), str(i)) for i in range(selected_days_from, selected_days_to + 1)]
#         else:
#             # If not editing, exclude the existing ranges but keep "90" and "Till Current Date" available
#             numeric_choices = [(str(i), str(i)) for i in range(1, 91) if i not in excluded_days or i == 90]

#         available_choices = [
#             ('', 'Please Select Day'),
#         ] + numeric_choices + [
#             ('till current date', 'Till Current Date')
#         ]

#         # Update choices for the form fields
#         self.fields['days_from'].choices = available_choices
#         self.fields['days_from'].initial = str(selected_days_from) if selected_days_from else ''
#         self.fields['days_from'].required = False  # Not required

#         self.fields['days_to'].choices = available_choices
#         self.fields['days_to'].initial = str(selected_days_to) if selected_days_to else ''
#         self.fields['days_to'].required = False  # Not required

#         # Display existing late fees in a table
#         listing_html = """
#             <h3>Existing Late Fees</h3>
#             <table style='border: 1px solid #ddd; width: 100%; border-collapse: collapse;'>
#                 <tr>
#                     <th>Days From</th>
#                     <th>Days To</th>
#                     <th>Late Fee</th>
#                     <th>Type</th>
#                     <th>Description</th>
#                 </tr>
#         """
#         # Query existing records for display in listing
#         for latefee in latefee_master.objects.all():
#             listing_html += f"""
#                 <tr>
#                     <td>{latefee.days_from}</td>
#                     <td>{latefee.days_to}</td>
#                     <td>{latefee.latefee}</td>
#                     <td>{latefee.latefee_type}</td>
#                     <td>{latefee.latefee_desc}</td>
#                 </tr>
#             """
        
#         listing_html += "</table>"

#         # Assign the marked-safe HTML to the custom form field
#         self.fields['listing'].initial = mark_safe(listing_html)


# class LateFeeMasterDisplay(admin.ModelAdmin):
#     form = LateFeeMasterForm
#     list_display = ("days_from", "days_to", "latefee", "latefee_type", "latefee_desc")

# admin.site.register(latefee_master, LateFeeMasterDisplay)



# admin.site.register(latefee_master)


# class PaymentScheduleMasterForm(forms.ModelForm):

#     schedule_list = forms.CharField(widget=ReadOnlyCKEditorWidget(), required=False, label='')
    
#     fees_for_months = forms.MultipleChoiceField(
#         choices=payment_schedule_master.Fees_For_Month_CHOICES,
#     )

#     Pay_In_Month_CHOICES = [
#         ('', 'Choose The Month'),
#         ('1', '1'),
#         ('2', '2'),
#         ('3', '3'),
#         ('4', '4'),
#         ('5', '5'),
#         ('6', '6'),
#         ('7', '7'),
#         ('8', '8'),
#         ('9', '9'),
#         ('10', '10'),
#         ('11', '11'),
#         ('12', '12')
#     ]
   
#     pay_in_month = forms.ChoiceField(
#         choices=Pay_In_Month_CHOICES,
#         # widget=forms.RadioSelect,
#         label="Pay In Month *",
#     )

#     Payment_Date_CHOICES = [
#         ('', 'Choose The Date'),
#         ('01', '01'),
#         ('02', '02'),
#         ('03', '03'),
#         ('04', '04'),
#         ('05', '05'),
#         ('06', '06'),
#         ('07', '07'),
#         ('08', '08'),
#         ('09', '09'),
#         ('10', '10'),
#         ('11', '11'),
#         ('12', '12'),
#         ('13', '13'),
#         ('14', '14'),
#         ('15', '15'),
#         ('16', '16'),
#         ('17', '17'),
#         ('18', '18'),
#         ('19', '19'),
#         ('20', '20'),
#         ('21', '21'),
#         ('22', '22'),
#         ('23', '23'),
#         ('24', '24'),
#         ('25', '25'),
#         ('26', '26'),
#         ('27', '27'),
#         ('28', '28'),
#         ('29', '29'),
#         ('30', '30'),
#         ('31', '31'),
#     ]
   
#     payment_date = forms.ChoiceField(
#         choices=Payment_Date_CHOICES,
#         # widget=forms.RadioSelect,
#         label="Payment Date *",
#     )

   

#     class Meta:
#         model = payment_schedule_master
#         fields = '__all__'


#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         instance = kwargs.get('instance')

#         schedules = payment_schedule_master.objects.all()
#         schedule_list_html = """
#             <h3>Existing Payment Schedules</h3>
#             <table style='border: 1px solid #ddd; width: 100%; border-collapse: collapse;'>
#                 <thead>
#                     <tr>
#                         <th style='border: 1px solid #ddd; padding: 8px;'>Schedule ID</th>
#                         <th style='border: 1px solid #ddd; padding: 8px;'>Fees for Months</th>
#                         <th style='border: 1px solid #ddd; padding: 8px;'>Pay in Month</th>
#                         <th style='border: 1px solid #ddd; padding: 8px;'>Payment Date</th>
#                     </tr>
#                 </thead>
#                 <tbody>
#         """
        
#         for schedule in schedules:
#             schedule_list_html += f"""
#                 <tr>
#                     <td style='border: 1px solid #ddd; padding: 8px;'>{schedule.schedule_id}</td>
#                     <td style='border: 1px solid #ddd; padding: 8px;'>{schedule.fees_for_months}</td>
#                     <td style='border: 1px solid #ddd; padding: 8px;'>{schedule.pay_in_month}</td>
#                     <td style='border: 1px solid #ddd; padding: 8px;'>{schedule.payment_date}</td>
#                 </tr>
#             """

#         schedule_list_html += """
#                 </tbody>
#             </table>
#         """

#         # Assign the marked-safe HTML to the custom form field
#         self.fields['schedule_list'].initial = mark_safe(schedule_list_html)

#         # Gather all used months from other records
#         used_months = set()
#         all_schedules = payment_schedule_master.objects.all()

#         if instance:
#             all_schedules = all_schedules.exclude(pk=instance.pk)
#             # Add the selected months of the current instance to the used months set
#             current_months = set(instance.fees_for_months.split(','))
#         else:
#             current_months = set()

#         for schedule in all_schedules:
#             used_months.update(schedule.fees_for_months.split(','))

#         # The available choices should include the months used by this instance + months not used by other records
#         available_choices = [
#             (value, label) for value, label in self.fields['fees_for_months'].choices 
#             if value in current_months or value not in used_months
#         ]
#         self.fields['fees_for_months'].choices = available_choices
#         self.fields['fees_for_months'].initial = list(current_months)
    
#     def clean_fees_for_months(self):
#         selected_months = self.cleaned_data['fees_for_months']
#         # Convert the list of selected months into a comma-separated string
#         return ','.join(selected_months)
    
    

# class PaymentScheduleMasterAdmin(admin.ModelAdmin):
#     form = PaymentScheduleMasterForm
#     list_display = ("fees_for_months", "pay_in_month", "payment_date")
#     search_fields = ("fees_for_months", "pay_in_month", "payment_date")
#     def get_form(self, request, obj=None, **kwargs):
#         form = super().get_form(request, obj, **kwargs)
#         return form


# admin.site.register(payment_schedule_master, PaymentScheduleMasterAdmin)

# another method

# class PaymentScheduleMasterForm(forms.ModelForm):
#     schedule_list = forms.CharField(widget=ReadOnlyCKEditorWidget(), required=False, label='')
    
#     fees_for_months = forms.MultipleChoiceField(
#         choices=payment_schedule_master.Fees_For_Month_CHOICES,
#     )

#     Pay_In_Month_CHOICES = [
#         ('', 'Choose The Month'),
#         ('1', '1'),
#     ]
   
#     pay_in_month = forms.ChoiceField(
#         choices=Pay_In_Month_CHOICES,
#         label="Pay In Month *",
#     )

#     Payment_Date_CHOICES = [
#         ('', 'Choose The Date'),
#         ('01', '01'),
#     ]
   
#     payment_date = forms.ChoiceField(
#         choices=Payment_Date_CHOICES,
#         label="Payment Date *",
#     )

#     class Meta:
#         model = payment_schedule_master
#         fields = '__all__'

#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         instance = kwargs.get('instance')

#         # Display a custom HTML block for the schedule list
#         schedule_list_html = """
#             <h3>Existing Payment Schedules</h3>
#         """
#         self.fields['schedule_list'].initial = mark_safe(schedule_list_html)

#         # Gather all used months from other records (excluding the current record if in edit mode)
#         used_months = set()
#         all_schedules = payment_schedule_master.objects.all()

#         # If in edit mode, exclude the current instance from the used months
#         current_months = set()
#         if instance:
#             all_schedules = all_schedules.exclude(pk=instance.pk)
#             current_months = set(instance.fees_for_months.split(','))

#         # Collect months used by other records
#         for schedule in all_schedules:
#             used_months.update(schedule.fees_for_months.split(','))

#         # The available choices should include the months used by this instance + months not used by other records
#         available_choices = [
#             (value, label) for value, label in self.fields['fees_for_months'].choices
#             if value in current_months or value not in used_months
#         ]

#         # Set the available choices for the 'fees_for_months' field
#         self.fields['fees_for_months'].choices = available_choices
#         self.fields['fees_for_months'].initial = list(current_months)  # Set initial value to the current record's months

#     def clean_fees_for_months(self):
#         selected_months = self.cleaned_data['fees_for_months']
#         # Convert the list of selected months into a comma-separated string for storage
#         return ','.join(selected_months)
    
class PaymentScheduleMasterForm(forms.ModelForm):
    schedule_list = forms.CharField(widget=ReadOnlyCKEditorWidget(), required=False, label='')

    fees_for_months = forms.MultipleChoiceField(
        choices=payment_schedule_master.Fees_For_Month_CHOICES,
    )
    # fees_for_months = forms.CharField(
    #     widget=forms.CheckboxSelectMultiple(choices=payment_schedule_master.Fees_For_Month_CHOICES),
    #     required=False,
    # )
    # fees_for_months = forms.MultipleChoiceField(
    #     choices=payment_schedule_master.Fees_For_Month_CHOICES,
    #     widget=forms.CheckboxSelectMultiple,  # Use CheckboxSelectMultiple widget
    #     required=False,
    # )


    Pay_In_Month_CHOICES = [
        ('', 'Choose The Month'),
        ('1', '1'),
    ]
   
    pay_in_month = forms.ChoiceField(
        choices=Pay_In_Month_CHOICES,
        label="Pay In Month *",
    )

    Payment_Date_CHOICES = [
        ('', 'Choose The Date'),
        ('01', '01'),
    ]
   
    payment_date = forms.ChoiceField(
        choices=Payment_Date_CHOICES,
        label="Payment Date *",
    )

    class Meta:
        model = payment_schedule_master
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        instance = kwargs.get('instance')

        # Display a custom HTML block for the schedule list
        schedule_list_html = """
            <h3>Existing Payment Schedules</h3>
        """
        self.fields['schedule_list'].initial = mark_safe(schedule_list_html)

        # Gather all months used by other records (excluding the current instance's months)
        used_months = set()
        current_months = set()

        # Collect months used by other records
        all_schedules = payment_schedule_master.objects.all()
        # print('instance.fees_for_months',type(instance.fees_for_months))
        if instance:
            # Exclude the current instance if in edit mode
            all_schedules = all_schedules.exclude(pk=instance.pk)
            # Include the current record's months to keep them selectable
            current_months = set(instance.fees_for_months.split(','))
            # current_months = ','.join(current_months)
             # Sort the current months in ascending order
            current_months = sorted(current_months, key=lambda x: int(x))

        print('current_months',(current_months))

        # Collect months from all other records
        for schedule in all_schedules:
            used_months.update(schedule.fees_for_months.split(','))

        # Ensure the current record's months remain in the selectable list and filter out used months
        available_choices = [
            (value, label) for value, label in self.fields['fees_for_months'].choices
            if value in current_months or value not in used_months
        ]

        # Set the available choices for the 'fees_for_months' field
        self.fields['fees_for_months'].choices = available_choices

        # Set the initial values for 'fees_for_months' to the current record's months
        self.fields['fees_for_months'].initial = (current_months)

    def clean_fees_for_months(self):
        selected_months = self.cleaned_data['fees_for_months']
        # Convert the list of selected months into a comma-separated string for storage
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

class FeeTypeFilter(admin.SimpleListFilter):
    title = 'Fee Type'
    parameter_name = 'search_fee_type'

    def lookups(self, request, model_admin):
        return []

class MonthsApplFilter(admin.SimpleListFilter):
    title = 'Months Applicable'
    parameter_name = 'search_months_appl'

    def lookups(self, request, model_admin):
        return []

class SpecialFeeMasterForm(forms.ModelForm):
    class_no = forms.ChoiceField(choices=CLASS_CHOICES, required=True)
    student_name = forms.ChoiceField(choices=[('', 'Select Student')], required=False, label="Student Name*")
    student_id = forms.CharField(widget=forms.HiddenInput())
    student_class_id = forms.CharField(widget=forms.HiddenInput())
    # added_by = forms.CharField(widget=forms.HiddenInput())
    # updated_by = forms.CharField(widget=forms.HiddenInput())
    months_applicable_for = forms.MultipleChoiceField(
        widget=forms.SelectMultiple,  # Use SelectMultiple for a multi-select dropdown
        required=False
    )

    # Generate year choices dynamically
    current_year = datetime.now().year
    year_choices = [(str(year), str(year)) for year in range(current_year + 1, current_year - 4, -1)]
    year = forms.ChoiceField(choices=year_choices, required=True)

    class Meta:
        model = specialfee_master
        # fields = ['class_no', 'student_name', 'fee_type', 'months_applicable_for', 'year', 'amount', 'added_by', 'updated_by']
        fields = ['class_no', 'student_name', 'fee_type', 'months_applicable_for', 'year', 'amount']

    class Media:
        js = ('app/js/specialfee_master.js',)

    MONTHS = [
        ('', 'Please Select Month'),
        ('1', 'January'),
        ('2', 'February'),
        ('3', 'March'),
        ('4', 'April'),
        ('5', 'May'),
        ('6', 'June'),
        ('7', 'July'),
        ('8', 'August'),
        ('9', 'September'),
        ('10', 'October'),
        ('11', 'November'),
        ('12', 'December')
    ]

    def __init__(self, *args, **kwargs):
        super(SpecialFeeMasterForm, self).__init__(*args, **kwargs)

        # Fetch all months (comma-separated groups) from payment_schedule_master
        months_choices = payment_schedule_master.objects.values_list('fees_for_months', 'fees_for_months')
        # Set the choices for the months_applicable_for field
        self.fields['months_applicable_for'].choices = months_choices

        # Handle initial value for edit case
        if self.instance and self.instance.pk:
            stored_months = self.instance.months_applicable_for
            if stored_months:
                print('+++ stored_months ++++', stored_months)
                # Split the stored comma-separated string into a list of strings
                self.fields['months_applicable_for'].initial = stored_months.split(',')
            else:
                self.fields['months_applicable_for'].initial = []
        
        # Set the choices for months_applicable_for based on the initial fee_type
        self.update_months_choices()

        if 'class_no' in self.data and not self.instance.pk:  # Only validate class_no if it's a new instance
            try:
                class_no = int(self.data.get('class_no'))
                current_year = datetime.now().year

                # Get student_classes and filter students
                student_classes = student_class.objects.filter(class_no=class_no).values('student_class_id', 'student_id', 'class_no', 'section')
                student_ids = [sc['student_id'] for sc in student_classes]
                students = student_master.objects.filter(student_id__in=student_ids, admission_date__year=current_year)

                # Prepare choices for the student_name field
                student_choices = [(f"{student.student_id}-{sc['student_class_id']}", f"{sc['class_no']} {sc['section']} {student.student_name}") 
                                   for student in students 
                                   for sc in student_classes 
                                   if sc['student_id'] == student.student_id]

                # Update the choices dynamically
                self.fields['student_name'].choices = student_choices

            except (ValueError, TypeError):
                pass  # Invalid input; ignore and leave choices empty
        elif self.instance.pk:  # Edit case
            # pass
            # Hide the class_no and student_name fields when editing
            self.fields['months_applicable_for'].required = False
            self.fields['class_no'].required = False
            self.fields['class_no'].widget = forms.HiddenInput()
            self.fields['student_name'].required = False
            self.fields['student_name'].widget = forms.HiddenInput()

            # Populate the student_name choices for existing instances
            # self.fields['student_name'].choices = [(f"{self.instance.student_id}-{self.instance.student_class_id}", 
            #                                         f"{self.instance.student_id} - {self.instance.student_class_id}")]

    def update_months_choices(self):
        months_choices = payment_schedule_master.objects.values_list('fees_for_months', 'fees_for_months')
        fee_type = self.initial.get('fee_type', self.data.get('fee_type'))
        if fee_type == 'bus_fees':
            print("++++++++++++")
            self.fields['months_applicable_for'].choices = self.MONTHS
            # self.fields['months_applicable_for'].required = True
        elif fee_type == 'ignore_prev_outstanding_fees':
            print("############")
            self.fields['months_applicable_for'].choices = []
            self.fields['months_applicable_for'].required = False
        else:
            print("&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&")
            self.fields['months_applicable_for'].choices = months_choices
            # self.fields['months_applicable_for'].required = True

    def clean_months_applicable_for(self):
        months = self.cleaned_data.get('months_applicable_for', [])
        # Join the list into a comma-separated string
        return ','.join(months)

        # months = self.cleaned_data.get('months_applicable_for', None)
        # print('+++++ months ++++++++', months)
        # # If no months were selected, keep the existing value
        # if not months:
        #     return self.instance.months_applicable_for
        # # Otherwise, join the selected months into a comma-separated string
        # return ','.join(months)


class SpecialFeeMasterAdmin(admin.ModelAdmin):
    list_display = ("student_charge_id", "student_id", "student_class_id", "fee_type", "months_applicable_for", "year", "amount", "added_at", "updated_at")
    # search_fields = ("student_charge_id", "student_id", "student_class_id", "fee_type", "months_applicable_for", "year", "amount", "added_at", "updated_at")
    list_filter = (FeeTypeFilter, MonthsApplFilter)

    form = SpecialFeeMasterForm

    def get_search_results(self, request, queryset, search_term):
        search_fee_type = request.GET.get('search_fee_type', None)
        search_months_appl = request.GET.get('search_months_appl', None)

        # Apply custom filters for admission_no and student_name
        if search_fee_type:
            queryset = queryset.filter(fee_type__icontains=search_fee_type)
        if search_months_appl:
            queryset = queryset.filter(months_applicable_for__icontains=search_months_appl)

        # Return the modified queryset and a boolean for whether distinct is needed
        return queryset, False

    def changelist_view(self, request, extra_context=None):
        # Adding extra context for the search fields in the template
        extra_context = extra_context or {}
        extra_context['search_fee_type'] = request.GET.get('search_fee_type', '')
        extra_context['search_months_appl'] = request.GET.get('search_months_appl', '')

        return super().changelist_view(request, extra_context=extra_context)

    change_list_template = 'admin/specialfee_changelist.html'

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('ajax/get-students/', self.admin_site.admin_view(self.get_students), name='ajax_get_students'),
        ]
        return custom_urls + urls

    def get_students(self, request):
        class_no = request.GET.get('class_no', '')
        if class_no:
            current_year = datetime.now().year

            # Get the student_id, class_no, and section from the student_class model
            student_classes = student_class.objects.filter(class_no=class_no).values('student_class_id', 'student_id', 'class_no', 'section')

            # Extract student_ids
            student_ids = [sc['student_id'] for sc in student_classes]

            # Filter students from the student_master model
            students = student_master.objects.filter(student_id__in=student_ids, admission_date__year=current_year)
            
            # Combine the student data with class_no and section
            results = []
            for student in students:
                student_info = {
                    'student_id': student.student_id,
                    'student_name': student.student_name,
                    'admission_no': student.addmission_no,
                }
                # Add class_no and section from the student_classes data
                student_class_info = next(sc for sc in student_classes if sc['student_id'] == student.student_id)
                student_info['class_id'] = student_class_info['student_class_id']
                student_info['class_no'] = student_class_info['class_no']
                student_info['section'] = student_class_info['section']
                results.append(student_info)

            return JsonResponse(results, safe=False)

        return JsonResponse({'error': 'Student not found'}, status=404)



admin.site.register(specialfee_master,SpecialFeeMasterAdmin)

    
class ButtonWidget(forms.Widget):
    def render(self, name, value, attrs=None, renderer=None):
        return mark_safe(f'<button type="button" id="search-button">Search</button>')

class StudentClassAdminForm(forms.ModelForm):
    student_name = forms.CharField(required=False, label="Student Name")
    admission_no = forms.IntegerField(required=False, label="Admission")
    display_class_no = forms.ChoiceField(choices=CLASS_CHOICES, required=False, label="Class")
    dispaly_section = forms.ChoiceField(choices=SECTION, required=False, label="Section")
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

class ClassNoFilter(admin.SimpleListFilter):
    title = 'Class No'
    parameter_name = 'search_class'

    def lookups(self, request, model_admin):
        return []

class SectionFilter(admin.SimpleListFilter):
    title = 'Section'
    parameter_name = 'search_section'

    def lookups(self, request, model_admin):
        return []

class StudentNameFilter(admin.SimpleListFilter):
    title = 'Student Name'
    parameter_name = 'search_student'

    def lookups(self, request, model_admin):
        return []

class AdmissionNoFilter(admin.SimpleListFilter):
    title = 'Admission Number'
    parameter_name = 'search_admission_no'

    def lookups(self, request, model_admin):
        return []

class StudentClassAdmin(admin.ModelAdmin):
    list_display = ("get_admission_no", "get_student_name", "class_no", "section", "started_on", "ended_on")
    list_filter = (ClassNoFilter, StudentNameFilter, AdmissionNoFilter, SectionFilter)

    form = StudentClassAdminForm

    # def save_model(self, request, obj, form, change):
    #     if 'student_id' in form.cleaned_data:
    #         # Ensure the student_id is retained even if the field is readonly
    #         obj.student_id = form.cleaned_data['student_id']
    #     super().save_model(request, obj, form, change)

    def get_search_results(self, request, queryset, search_term):
        search_class = request.GET.get('search_class', None)
        search_section = request.GET.get('search_section', None)
        search_student = request.GET.get('search_student', None)
        search_admission_no = request.GET.get('search_admission_no', None)

        # Apply custom filters for admission_no and student_name
        if search_class:
            queryset = queryset.filter(class_no=search_class)
        if search_section:
            queryset = queryset.filter(section=search_section)
        if search_student:
            student_ids = student_master.objects.filter(student_name__icontains=search_student).values_list('student_id', flat=True)
            queryset = queryset.filter(student_id__in=student_ids)
        if search_admission_no:
            student_ids = student_master.objects.filter(addmission_no__icontains=search_admission_no).values_list('student_id', flat=True)
            queryset = queryset.filter(student_id__in=student_ids)

        # Return the modified queryset and a boolean for whether distinct is needed
        return queryset, False

    def changelist_view(self, request, extra_context=None):
        # Adding extra context for the search fields in the template
        extra_context = extra_context or {}
        extra_context['search_class'] = request.GET.get('search_class', '')
        extra_context['search_section'] = request.GET.get('search_section', '')
        extra_context['search_student'] = request.GET.get('search_student', '')
        extra_context['search_admission_no'] = request.GET.get('search_admission_no', '')
        
        return super().changelist_view(request, extra_context=extra_context)

    change_list_template = 'admin/student_class_changelist.html'

    def get_student_name(self, obj):
        student_master_instance = student_master.objects.filter(student_id=obj.student_id).order_by('-addmission_no').first()
        return student_master_instance.student_name if student_master_instance else None
    get_student_name.short_description = 'Student Name'

    def get_admission_no(self, obj):
        student_master_instance = student_master.objects.filter(student_id=obj.student_id).order_by('-addmission_no').first()
        return student_master_instance.addmission_no if student_master_instance else None
    get_admission_no.short_description = 'Admission Number'

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
                    'fields': ('student_name', 'admission_no', 'display_class_no', 'dispaly_section', 'search_button', 'search_results'),
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
        if student_id:
            student = student_master.objects.get(student_id=student_id)
            return JsonResponse({'student_id': student.student_id,'student_name':student.student_name,'admission_no':student.addmission_no})
        return JsonResponse({'error': 'Student not found'}, status=404)

    def load_students(self, request):
        student_name = request.GET.get('student_name', '')
        admission_no = request.GET.get('admission_no', '')
        class_no = request.GET.get('class_no', '')
        section = request.GET.get('section', '')
        
        queryset = student_master.objects.all()

        if student_name:
            queryset = queryset.filter(student_name__icontains=student_name)
        if admission_no:
            queryset = queryset.filter(addmission_no=admission_no)
        if class_no:
            student_ids = student_class.objects.filter(class_no=class_no).values_list('student_id', flat=True)
            queryset = queryset.filter(student_id__in=student_ids)
        if section:
            student_ids = student_class.objects.filter(section=section).values_list('student_id', flat=True)
            queryset = queryset.filter(student_id__in=student_ids)
        results = list(queryset.values('student_id', 'student_name', 'addmission_no'))
        return JsonResponse(results, safe=False)

    class Media:
        js = ('app/js/student_class.js',)


admin.site.register(student_class,StudentClassAdmin)


def get_default_quarter():
    current_month = datetime.now().month
    if 4 <= current_month <= 6:
        return '4,5,6'  # April - June
    elif 7 <= current_month <= 9:
        return '7,8,9'  # July - September
    elif 10 <= current_month <= 12:
        return '10,11,12'  # October - December
    return '1,2,3'  # January - March


class StudentFeeClassNoFilter(admin.SimpleListFilter):
    title = 'Class No'
    parameter_name = 'search_class'

    def lookups(self, request, model_admin):
        return []

class StudentFeeSectionFilter(admin.SimpleListFilter):
    title = 'Section'
    parameter_name = 'search_section'

    def lookups(self, request, model_admin):
        return []

class StudentFeeStudentNameFilter(admin.SimpleListFilter):
    title = 'Student Name'
    parameter_name = 'search_student'

    def lookups(self, request, model_admin):
        return []

class StudentFeeAdmissionNoFilter(admin.SimpleListFilter):
    title = 'Admission Number'
    parameter_name = 'search_admission_no'

    def lookups(self, request, model_admin):
        return []


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
    # search_results = forms.ModelChoiceField(queryset=student_master.objects.none(), required=False,blank=True, label="Select Student")
    search_results = forms.ModelChoiceField(
        queryset=student_master.objects.none(),
        required=False,
        blank=True,
        label="Select Student",
        widget=forms.Select(attrs={'id': 'student-dropdown'})  # Adding the id attribute
    )

    student_id = forms.IntegerField(widget=forms.HiddenInput(attrs={'readonly': 'readonly', 'id': 'id_student_id'}), required=False)

    display_admission_no = forms.CharField(
        required=False, 
        label="Admission No", 
        widget=forms.TextInput(attrs={'readonly': 'readonly', 'id': 'id_display_admission_no'})
    )

    display_student_name = forms.CharField(
        required=False, 
        label="Student Name", 
        widget=forms.TextInput(attrs={'readonly': 'readonly', 'id': 'id_display_student_name'})
    )

    display_father_name = forms.CharField(
        required=False, 
        label="Father Name", 
        widget=forms.TextInput(attrs={'readonly': 'readonly', 'id': 'id_display_father_name'})
    )

    display_student_class = forms.CharField(
        required=False, 
        label="Student Class", 
        widget=forms.TextInput(attrs={'readonly': 'readonly', 'id': 'id_display_student_class'})
    )

    display_student_section = forms.CharField(
        required=False, 
        label="Student Section", 
        widget=forms.TextInput(attrs={'readonly': 'readonly', 'id': 'id_display_student_section'})
    )

    started_on = forms.ChoiceField(
        choices=[(str(year), str(year)) for year in range(current_year - 1, current_year + 2)],
        required=False, 
        label="Year", 
        widget=forms.Select(attrs={'id': 'id_started_on'})
    )


    # Fees section fields
    # fees_for_months = forms.CharField(label="Fees For Months", required=False)
    # fees_period_month = forms.CharField(label="Fees Period Month", required=False)
    # Define the multiple choice fields for fees_for_months and fees_period_month
    fees_for_months = forms.MultipleChoiceField(
        choices=FEE_MONTHS_CHOICES,  # Populate with dynamic data if needed
        required=False,
        label="Fees for Months",
        widget=forms.SelectMultiple(attrs={'style': 'width:150px', 'id': 'id_fees_for_months'})
    )

    # fees_for_months = MultiSelectField(choices=FEE_MONTHS_CHOICES, max_choices=4, max_length=100)

    

    Month_CHOICES = [
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
    fees_period_month = forms.MultipleChoiceField(
        choices=[(int(month[0]), int(month[1])) for month in Month_CHOICES],
        required=False,
        label="Fees Period Month",
        widget=forms.SelectMultiple(attrs={'style': 'width:150px;','id': 'id_fees_period_month'})
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
    previous_fees_record = forms.CharField(widget=forms.HiddenInput(), required=False)  # Hidden input to store previous fees data

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        print("======= I'M HERE ===========")

        # Fetch the initial data for update case
        # if self.instance and self.instance.fees_period_month:
        #     selected_months = self.instance.fees_period_month.split(', ')
        #     self.fields['fees_period_month'].initial = selected_months
        # print("======= I'M HERE ===========")

        # Calculate the current quarter based on the current month
        # current_month = datetime.now().month
        # if 4 <= current_month <= 6:
        #     default_quarter = '4,5,6'  # April - June
        # elif 7 <= current_month <= 9:
        #     default_quarter = '7,8,9'  # July - September
        # elif 10 <= current_month <= 12:
        #     default_quarter = '10,11,12'  # October - December
        # else:
        #     default_quarter = '1,2,3'  # January - March

        # # Set the default value for fees_for_months
        # self.fields['fees_for_months'].initial = default_quarter
        # print("======= I'M HERE ===========")

        # Call this in __init__
        self.fields['fees_for_months'].initial = get_default_quarter()

        if self.instance and self.instance.pk:
            
            self.fields['student_name'].widget = forms.HiddenInput()
            self.fields['admission_no'].widget = forms.HiddenInput()
            self.fields['class_no'].widget = forms.HiddenInput()
            self.fields['section'].widget = forms.HiddenInput()
            self.fields['search_results'].widget = forms.HiddenInput()

            student = self.instance.student_id
            # print(student)
            # print(f"Student ID: {student.student_id}, Name: {student.student_name}")

            if student.student_id:
                try:

                    # Fetch and render previous fees data
                    # previous_fees_html = self.get_previous_fees_data(student.student_id)
                    # self.fields['previous_fees_record'].initial = mark_safe(previous_fees_html)

                    # print("Testing for student id error.")
                    student = student_master.objects.get(student_id=student.student_id)
                    student_classes = student_class.objects.filter(student_id=student.student_id).order_by('-started_on').first()

                    self.fields['display_admission_no'].initial = student.addmission_no
                    self.fields['display_student_name'].initial = student.student_name
                    self.fields['display_father_name'].initial = student.father_name

                    if student_classes:
                        self.fields['display_student_class'].initial = student_classes.class_no
                        self.fields['display_student_section'].initial = student_classes.section
                        if student_classes.started_on:
                            self.fields['started_on'].initial = student_classes.started_on.strftime('%Y')

                    # Set hidden student_id value
                    self.fields['student_id'].initial = student.student_id
                except student_master.DoesNotExist:
                    print(f"Student with ID {student.student_id} does not exist.")
            
        print("======= I'M HERE ===========")
    
        # # Populate pre-selected values when the form is submitted
        # if self.is_bound:
        #     submitted_fees_period_month = self.data.getlist('fees_period_month')
        #     print("submitted_fees_period_month", submitted_fees_period_month)
        #     self.fields['fees_period_month'].initial = submitted_fees_period_month  # Ensure submitted values are used

        # if self.is_bound and self.data.get('search_results'):
        #     print(self.data.get('search_results'))
        #     student_id = self.data.get('search_results')
        #     if student_id:
        #         self.fields['search_results'].queryset = student_master.objects.filter(student_id=student_id)

    class Media:
        js = ('app/js/student_fees.js',)  # Adjust the path as necessary
        css = {
            'all': ('app/css/custom_admin.css',)  # Add your custom CSS file here
        }



    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)

    #     print("======= I'M HERE ===========")

    #     # Set the field to not required if needed
    #     # self.fields['fees_period_month'].required = False  # Ensure the field is optional
    #     # Populate fees_period_month with dynamic choices if needed
    #     # self.fields['fees_period_month'].choices = MONTH_CHOICES

    #     # Fetch the initial data for update case
    #     selected_months = self.instance.fees_period_month.split(', ')
    #     self.fields['fees_period_month'].initial = selected_months
    

    #     # Calculate the current quarter based on the current month
    #     current_month = datetime.now().month
    #     if 4 <= current_month <= 6:
    #         default_quarter = '4,5,6'  # April - June
    #     elif 7 <= current_month <= 9:
    #         default_quarter = '7,8,9'  # July - September
    #     elif 10 <= current_month <= 12:
    #         default_quarter = '10,11,12'  # October - December
    #     else:
    #         default_quarter = '1,2,3'  # January - March

    #      # Set the default value for fees_for_months
    #     self.fields['fees_for_months'].initial = default_quarter
    #     print(default_quarter)

    #     initial_values = self.instance.fees_period_month.split(', ') if self.instance.fees_period_month else []
    #     self.fields['fees_period_month'].initial = [10]
    #     print(initial_values)


    #     if self.instance and self.instance.pk:

    #         # Assuming 'student_id' is being passed in the form data
    #         student_id = self.instance.student_id

    #         # Print the value and type of student_id
    #         # logger.debug(f"Student ID: {student_id}, Type: {type(student_id)}")

    #         self.fields['student_name'].widget = forms.HiddenInput()
    #         self.fields['admission_no'].widget = forms.HiddenInput()
    #         self.fields['class_no'].widget = forms.HiddenInput()
    #         self.fields['section'].widget = forms.HiddenInput()
    #         self.fields['search_results'].widget = forms.HiddenInput()

    #         # Pre-select the values in fees_period_month
    #         if self.instance.fees_period_month:
    #             initial_values = self.instance.fees_period_month.split(', ')  # Split by comma
    #             print("initial_values", initial_values)
    #             self.fields['fees_period_month'].initial = initial_values  # Set the initial values
            
    #         if student_id:
                
    #             student = student_master.objects.get(student_id=student_id)
    #             student_classes = student_class.objects.filter(student_id=student_id).order_by('-started_on').first()
    #             self.fields['display_admission_no'].initial = student.addmission_no
    #             self.fields['display_student_name'].initial = student.student_name
    #             self.fields['display_father_name'].initial = student.father_name
    #             self.fields['display_student_class'].initial = student_classes.class_no
    #             self.fields['display_student_section'].initial = student_classes.section
    #             self.fields['started_on'].initial = student_classes.started_on.strftime('%Y')

    #             # Set hidden student_id value
    #             self.fields['student_id'].initial = student_id

    #     # Populate pre-selected values when the form is submitted
    #     if self.is_bound:
    #         submitted_fees_period_month = self.data.getlist('fees_period_month')
    #         print("submitted_fees_period_month", submitted_fees_period_month)
    #         self.fields['fees_period_month'].initial = submitted_fees_period_month  # Ensure submitted values are used      

    #     if self.is_bound and self.data.get('search_results'):
    #         student_id = self.data.get('search_results')
    #         if student_id:
    #             self.fields['search_results'].queryset = student_master.objects.filter(student_id=student_id)

    # class Media:
    #     js = ('app/js/student_fees.js',)  # Adjust the path as necessary
    #     css = {
    #         'all': ('app/css/custom_admin.css',)  # Add your custom CSS file here
    #     }

class StudentFeesAdmin(admin.ModelAdmin):

    form = StudentFeesAdminForm

    change_form_template = 'admin/student_fee/change_form.html'
    # change_form_template = 'admin/student_fee/change_form.html'

    # Fields to display in the list view
    list_display = (
        'get_addmission_no',  # Display student name
        'student_class',
        'student_section',
        'get_student_name',  # Display student name
        'fees_period_month',
        'year',
        'date_payment',
        'concession_applied',
        'annual_fees_paid',
        'tuition_fees_paid',
        'funds_fees_paid',
        'admission_fees_paid',
        'dayboarding_fees_paid',
        'miscellaneous_fees_paid',
        'bus_fees_paid',
        'activity_fees',
        'total_amount',
        'amount_paid',
        'payment_mode',
        'cheq_no',
        'txn_id',
        'bank_name',
        'cheque_status',
        'realized_date',
        'receipt_url',
        'added_by',
        'txn_ref_number',
        'branch_name',
        'txn_response_code',
        'txn_payment_mode',
        'added_at',
        'edited_by',
        'edited_at',
        'remarks',
        'entry_date',
       
    )
    
    # Fields to search in the search bar
    list_filter = (StudentFeeClassNoFilter, StudentFeeSectionFilter, StudentFeeStudentNameFilter,StudentFeeAdmissionNoFilter)

    # list_filter = (
    #     'student_class',           # Direct field on StudentFee model
    #     'student_section',         # Direct field on StudentFee model
    #     'student_id__student_name', # ForeignKey to student_master, filtering by student name
    #     'student_id__addmission_no' # ForeignKey to student_master, filtering by admission number
    # )
    # search_fields = (
    #     'student_class',
    #     'fees_for_months',
    #     'fees_period_month',
    #     'year',
    #     'date_payment',
    #     'total_amount',
    #     'amount_paid',
    #     'receipt_url',
    #     'added_by'
    # )

    def get_fieldsets(self, request, obj=None):
        if obj:  # Editing an existing student_class
            return [
                ('Previous Fees Record', {
                    'fields': (),
                    'classes': ('collapse',),  # Optional: initially collapsed
                }),

                # Section 2: Student Details, Fees, and Payment
                ('Selected Student Details', {
                    'fields': (
                        'display_admission_no',
                        'display_student_name',
                        'display_father_name',
                        'display_student_class',
                        'display_student_section',
                        'started_on',
                        'student_id',
                    ),
                    'classes': ('half-width-container',),  # Custom CSS class for layout
                }),
                ('Fees Section', {
                    'fields': (
                        'fees_for_months',
                        'fees_period_month',
                        'annual_fees_paid',
                        'tuition_fees_paid',
                        'funds_fees_paid',
                        'sports_fees_paid',
                        'activity_fees',
                        'admission_fees_paid',
                        'miscellaneous_fees_paid',
                        'late_fees_paid',
                        'dayboarding_fees_paid',
                        'bus_fees_paid',
                        'concession_type',
                        'concession_applied',
                        'total_amount',
                    ),
                }),
                ('Payment Section', {
                    'fields': (
                        'date_payment',
                        'payment_mode',
                        'cheque_no',
                        'bank_name',
                        'branch_name',
                        'amount_paid',
                        'realized_date',
                        'cheque_status',
                        'remarks',
                    ),
                }),

            ]
        else:  # Adding a new student_class
            return [
                ('Search Student', {
            'fields': (
                'student_name',
                'admission_no',
                'class_no',
                'section',
                'search_button',
            ),
            'classes': ('half-width-container',),  # Custom CSS class for layout
        }),
        ('Select Student', {
            'fields': ( 'search_results',),
            # 'classes': ('collapse',),  # Optional: initially collapsed
        }),

        # Section 2: Student Details, Fees, and Payment
        ('Selected Student Details', {
            'fields': (
                'display_admission_no',
                'display_student_name',
                'display_father_name',
                'display_student_class',
                'display_student_section',
                'started_on',
                'student_id',
            ),
            'classes': ('half-width-container',),  # Custom CSS class for layout
        }),
        ('Fees Section', {
            'fields': (
                'fees_for_months',
                'fees_period_month',
                'annual_fees_paid',
                'tuition_fees_paid',
                'funds_fees_paid',
                'sports_fees_paid',
                'activity_fees',
                'admission_fees_paid',
                'miscellaneous_fees_paid',
                'late_fees_paid',
                'dayboarding_fees_paid',
                'bus_fees_paid',
                'concession_type',
                'concession_applied',
                'total_amount',
            ),
        }),
        ('Payment Section', {
            'fields': (
                'date_payment',
                'payment_mode',
                'cheque_no',
                'bank_name',
                'branch_name',
                'amount_paid',
                'realized_date',
                'cheque_status',
                'remarks',
            ),
        }),
    
            ]



    def get_search_results(self, request, queryset, search_term):
        search_class = request.GET.get('search_class', None)
        search_section = request.GET.get('search_section', None)
        search_student = request.GET.get('search_student', None)
        search_admission_no = request.GET.get('search_admission_no', None)

        # Apply custom filters for admission_no and student_name
        if search_class:
            queryset = queryset.filter(student_class=search_class)
        if search_section:
            queryset = queryset.filter(student_section=search_section)
        if search_student:
            student_ids = student_master.objects.filter(student_name__icontains=search_student).values_list('student_id', flat=True)
            queryset = queryset.filter(student_id__in=student_ids)
        if search_admission_no:
            student_ids = student_master.objects.filter(addmission_no__icontains=search_admission_no).values_list('student_id', flat=True)
            queryset = queryset.filter(student_id__in=student_ids)

        # Return the modified queryset and a boolean for whether distinct is needed
        return queryset, False

    def changelist_view(self, request, extra_context=None):
        # Adding extra context for the search fields in the template
        extra_context = extra_context or {}
        extra_context['search_class'] = request.GET.get('search_class', '')
        extra_context['search_section'] = request.GET.get('search_section', '')
        extra_context['search_student'] = request.GET.get('search_student', '')
        extra_context['search_admission_no'] = request.GET.get('search_admission_no', '')
        
        return super().changelist_view(request, extra_context=extra_context)

    change_list_template = 'admin/student_fee/student_fees_changelist.html'

    # def get_student_name(self, obj):
    #     student_master_instance = student_master.objects.filter(student_id=obj.student_id).order_by('-addmission_no').first()
    #     return student_master_instance.student_name if student_master_instance else None
    # get_student_name.short_description = 'Student Name'

    # def get_admission_no(self, obj):
    #     student_master_instance = student_master.objects.filter(student_id=obj.student_id).order_by('-addmission_no').first()
    #     return student_master_instance.addmission_no if student_master_instance else None
    # get_admission_no.short_description = 'Admission Number'



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
    
    # def load_students(self, request):
    #     if request.method == 'GET':
    #         admission_no = request.GET.get('admission_no')
    #         class_no = request.GET.get('class_no')
    #         section = request.GET.get('section')
    #         student_name = request.GET.get('student_name')
            
    #         # Base query with distinct students
    #         students = student_master.objects.distinct()

    #         print(f'students==={students}')
            

    #         # Apply filters based on the provided parameters
    #         if admission_no:
    #             students = students.filter(addmission_no=admission_no)
    #         if student_name:
    #             students = students.filter(student_name__istartswith=student_name)

    #         # Prefetch related student classes to avoid querying in a loop
    #         students = students.prefetch_related('classes') 

    #         print(f'studentsssss==={students}')

    #         # Create the final response
    #         student_data = []
    #         for student in students:
    #             # Filter related student classes and get the latest with class_no and section filtering
    #             # latest_class = student_class.objects.filter(
    #             #     student_id=student.student_id,
    #             #     class_no=class_no if class_no else None,  # Filter by class_no if provided
    #             #     section=section if section else None  # Filter by section if provided
    #             # ).order_by('-student_class_id').first()

    #             latest_class = student_class.objects.filter(
    #                 student_id=student.student_id,
                    
    #             ).order_by('-student_class_id').first()

    #             print(f'latest_class----{latest_class}')

    #             # If latest_class exists, add it to the student_data
    #             if latest_class:
    #                 student_data.append({
    #                     'student_id': student.student_id,
    #                     'student_name': student.student_name,
    #                     'class_no': latest_class.class_no,
    #                     'section': latest_class.section
    #                 })

    #         # Convert the student_data list into the desired format
    #         formatted_data = ','.join([f"{d['student_id']}${d['student_name']}:{d['class_no']}-{d['section']}" for d in student_data])

    #         return JsonResponse({'data': formatted_data})
        
    #     return JsonResponse({'error': 'Bad Request'}, status=400)

    def load_students(self, request):
        if request.method == 'GET':
            # Extract query parameters from the GET request
            admission_no = request.GET.get('admission_no')
            class_no = request.GET.get('class_no')
            section = request.GET.get('section')
            student_name = request.GET.get('student_name')

            # Base query: Get distinct students and join with student_classes
            students = student_master.objects.all().distinct()

            # Apply filters based on the provided parameters
            if admission_no:
                students = students.filter(addmission_no=admission_no)
            if student_name:
                students = students.filter(student_name__istartswith=student_name)

            # Filter student_classes based on class_no and section if provided
            student_data = []
            for student in students:
                # Fetch the latest student_class for each student
                latest_class_query = student_class.objects.filter(
                    student_id=student.student_id
                ).order_by('-student_class_id')

                # Apply filters for class_no and section if they are provided
                if class_no:
                    latest_class_query = latest_class_query.filter(class_no=class_no)
                if section:
                    latest_class_query = latest_class_query.filter(section=section)

                latest_class = latest_class_query.first()

                # If latest_class exists, add the student and class details to student_data
                if latest_class:
                    student_data.append({
                        'student_id': student.student_id,
                        'student_name': student.student_name,
                        'class_no': latest_class.class_no,
                        'section': latest_class.section
                    })

            # Convert the student_data list into the desired output format
            formatted_data = ','.join([
                f"{d['student_id']}${d['student_name']}:{d['class_no']}-{d['section']}"
                for d in student_data
            ])

            # Return the response in JSON format
            return JsonResponse({'data': formatted_data})
        
        # If the request method is not GET, return a 400 Bad Request error
        return JsonResponse({'error': 'Bad Request'}, status=400)


    # def load_students(self, request):
    #     if request.method == 'GET':
    #         admission_no = request.GET.get('admission_no')
    #         class_no = request.GET.get('class_no')
    #         section = request.GET.get('section')
    #         student_name = request.GET.get('student_name')
            
    #         # Base query
    #         students = student_master.objects.distinct()

    #         # Apply filters based on the provided parameters
    #         if admission_no:
    #             students = students.filter(addmission_no=admission_no)
    #         if student_name:
    #             students = students.filter(student_name__istartswith=student_name)

    #         # Create the final response
    #         student_data = []
    #         for student in students:
    #             # Filter related student classes
    #             latest_class = student_class.objects.filter(
    #                 student_id=student.student_id
    #             ).order_by('-student_class_id').first()

    #             if latest_class and (not class_no or latest_class.class_no == class_no):
    #                 student_data.append({
    #                     'student_id': student.student_id,
    #                     'student_name': student.student_name,
    #                     'class_no': latest_class.class_no
    #                 })

    #         # Convert the student_data list into the desired format
    #         formatted_data = ','.join([f"{d['student_id']}${d['student_name']}:{d['class_no']}" for d in student_data])

    #         return JsonResponse({'data': formatted_data})
        
    #     return JsonResponse({'error': 'Bad Request'}, status=400)

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
        today = datetime.now().strftime("%Y-%m-%d")
        date = today.split("-")

        with connection.cursor() as cursor:
            # Query 1: Get payment schedule master data
            cursor.execute("SELECT * FROM payment_schedule_master WHERE fees_for_months = %s", [fm])
            if not (query := cursor.fetchone()):
                return JsonResponse({"error": "Payment schedule not found"}, status=404)
            # Constructing the data string as you expect
            data = f"{query[1]}${query[2]}${query[3]}"
            payment_date = f"{date[0]}-{query[2]}-{query[3]}"

                # Calculate the date difference in days
            now = int(time.mktime(datetime.now().timetuple()))
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
            if query2 := cursor.fetchone():
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

    # def save_model(self, request, obj, form, change):
    #     if request.method == 'POST':
    #         print("testing")
    #         print(request.POST)
    #     # Fetch the student ID from the POST data
    #         student_id = request.POST.get('student_id')
    #         print(f"request.POST.get('student_id') :{student_id}")

    #         if student_id:
    #             # Get the student_master instance using the student_id
    #             try:
    #                 student_instance = student_master.objects.get(pk=student_id)
    #                 obj.student_id = student_instance  # Assign the student_master instance to the student_fee object
    #             except student_master.DoesNotExist:
    #                 raise ValueError(f"Student with ID {student_id} does not exist")

    #         # Proceed with the rest of the save operation
    #         super().save_model(request, obj, form, change)



    def add_view(self, request, form_url='', extra_context=None):
        if request.method == 'POST':
            # Custom saving logic starts here

            # Fetch the student ID from the POST data
            stuid = request.POST.get('student_id')
            
            # Fetch the student_master instance using the primary key (stuid)
            try:
                student_instance = student_master.objects.get(student_id=stuid)
            except student_master.DoesNotExist:
                raise ValueError(f"Student with ID {stuid} does not exist")
            
            # Create a new student_fee instance
            obj = student_fee()
            
            # Now assign the student_master instance to obj.student_id
            obj.student_id = student_instance

            # Custom logic before saving the object
            today = datetime.now()  
            year = int(request.POST.get('started_on'))

            if today.month < 4:
                year -= 1

            student_class = request.POST.get('display_student_class', '')
            montharray = self.get_months_array(year)
            months = ','.join(map(str, montharray))

            if student_class:
                months_paid = student_fee.objects.filter(
                    student_id=stuid,
                    student_class=student_class,
                    year=year
                ).values_list('fees_for_months', flat=True).distinct()
            else:
                months_paid = student_fee.objects.filter(
                    student_id=stuid,
                    student_class='',
                    year=year
                ).values_list('fees_for_months', flat=True).distinct()

            months_paid = set(map(str.strip, ','.join(months_paid).split(',')))
            tmp = set(montharray) - months_paid
            tmpval = ','.join(map(str, tmp))

            if tmpval:
                alert_message = f'Fee pending for {tmpval} month '
                # Optionally use this alert message for feedback

            # Setting model attributes from the form data
            obj.payment_mode = request.POST.get('payment_mode')
            if obj.payment_mode == 'Cheque' and not obj.cheque_status:
                obj.cheque_status = 'Open'

            obj.date_payment = parse_date(request.POST.get('date_payment'))
            if obj.payment_mode != 'Cheque':
                obj.realized_date = obj.date_payment

            obj.entry_date = parse_date(request.POST.get('date_payment'))
            obj.student_class = request.POST.get('display_student_class')
            obj.student_section = request.POST.get('display_student_section')
            obj.fees_for_months = request.POST.get('fees_for_months')

            # Get the list of selected months
            fees_period_month_list = request.POST.getlist('fees_period_month')
            obj.fees_period_month = ', '.join(fees_period_month_list)

            obj.year = request.POST.get('started_on')
            obj.total_amount = float(request.POST.get('total_amount', 0))
            obj.amount_paid = float(request.POST.get('amount_paid', 0))

            # Handle concessions
            if request.POST.get('concession_applied') and float(request.POST.get('concession_applied')) > 0:
                obj.concession_applied = float(request.POST.get('concession_applied'))
                obj.concession_type_id = request.POST.get('concession_type')
            else:
                obj.concession_type_id = None
                obj.concession_applied = None

            # Handle other fees-related attributes
            obj.bus_fees_paid = float(request.POST.get('bus_fees_paid', 0))
            obj.dayboarding_fees_paid = float(request.POST.get('dayboarding_fees_paid', 0))
            obj.miscellaneous_fees_paid = float(request.POST.get('miscellaneous_fees_paid', 0))
            obj.late_fees_paid = float(request.POST.get('late_fees_paid', 0))
            obj.security_paid = float(request.POST.get('security_paid', 0))
            obj.admission_fees_paid = float(request.POST.get('admission_fees_paid', 0))
            obj.activity_fees = float(request.POST.get('activity_fees', 0))
            obj.sports_fees_paid = float(request.POST.get('sports_fees_paid', 0))
            obj.funds_fees_paid = float(request.POST.get('funds_fees_paid', 0))
            obj.tuition_fees_paid = float(request.POST.get('tuition_fees_paid', 0))
            obj.annual_fees_paid = float(request.POST.get('annual_fees_paid', 0))
            obj.isdefault = request.POST.get('isdefault')
            obj.remarks = request.POST.get('remarks')
            obj.added_by = request.user.username

            # Save the student_fee instance
            obj.save()

            # Generate the PDF for the fee record
            self.generate_pdf(obj.student_fee_id)

            # Redirect to the change page or list page
            self.message_user(request, "Student fee record saved successfully.")
            return HttpResponseRedirect(reverse('admin:app_student_fee_changelist'))

        return super().add_view(request, form_url, extra_context)


    def change_view(self, request, object_id, form_url='', extra_context=None):
        # Fetch the student_fee instance
        obj = get_object_or_404(student_fee, pk=object_id)
        
        if request.method == 'POST':
            # Custom logic for updating the object
            stuid = request.POST.get('student_id')
            
            try:
                student_instance = student_master.objects.get(student_id=stuid)
            except student_master.DoesNotExist:
                raise ValueError(f"Student with ID {stuid} does not exist")
            
            # Assign the student_master instance to obj.student_id
            obj.student_id = student_instance

            # Custom logic before saving the object
            today = datetime.now()
            year = int(request.POST.get('started_on'))

            if today.month < 4:
                year -= 1

            student_class = request.POST.get('display_student_class', '')
            montharray = self.get_months_array(year)
            months = ','.join(map(str, montharray))

            if student_class:
                months_paid = student_fee.objects.filter(
                    student_id=stuid,
                    student_class=student_class,
                    year=year
                ).values_list('fees_for_months', flat=True).distinct()
            else:
                months_paid = student_fee.objects.filter(
                    student_id=stuid,
                    student_class='',
                    year=year
                ).values_list('fees_for_months', flat=True).distinct()

            months_paid = set(map(str.strip, ','.join(months_paid).split(',')))
            tmp = set(montharray) - months_paid
            tmpval = ','.join(map(str, tmp))

            if tmpval:
                alert_message = f'Fee pending for {tmpval} month '

            # Setting model attributes from the form data
            obj.payment_mode = request.POST.get('payment_mode')
            if obj.payment_mode == 'Cheque' and not obj.cheque_status:
                obj.cheque_status = 'Open'

            obj.date_payment = parse_date(request.POST.get('date_payment'))
            if obj.payment_mode != 'Cheque':
                obj.realized_date = obj.date_payment

            obj.entry_date = parse_date(request.POST.get('date_payment'))
            obj.student_class = request.POST.get('display_student_class')
            obj.student_section = request.POST.get('display_student_section')
            obj.fees_for_months = request.POST.get('fees_for_months')

            fees_period_month_list = request.POST.getlist('fees_period_month')
            obj.fees_period_month = ', '.join(fees_period_month_list)

            obj.year = request.POST.get('started_on')
            obj.total_amount = float(request.POST.get('total_amount', 0))
            obj.amount_paid = float(request.POST.get('amount_paid', 0))

            if request.POST.get('concession_applied') and float(request.POST.get('concession_applied')) > 0:
                obj.concession_applied = float(request.POST.get('concession_applied'))
                obj.concession_type_id = request.POST.get('concession_type')
            else:
                obj.concession_type_id = None
                obj.concession_applied = None

            obj.bus_fees_paid = float(request.POST.get('bus_fees_paid', 0))
            obj.dayboarding_fees_paid = float(request.POST.get('dayboarding_fees_paid', 0))
            obj.miscellaneous_fees_paid = float(request.POST.get('miscellaneous_fees_paid', 0))
            obj.late_fees_paid = float(request.POST.get('late_fees_paid', 0))
            obj.security_paid = float(request.POST.get('security_paid', 0))
            obj.admission_fees_paid = float(request.POST.get('admission_fees_paid', 0))
            obj.activity_fees = float(request.POST.get('activity_fees', 0))
            obj.sports_fees_paid = float(request.POST.get('sports_fees_paid', 0))
            obj.funds_fees_paid = float(request.POST.get('funds_fees_paid', 0))
            obj.tuition_fees_paid = float(request.POST.get('tuition_fees_paid', 0))
            obj.annual_fees_paid = float(request.POST.get('annual_fees_paid', 0))
            obj.isdefault = request.POST.get('isdefault')
            obj.remarks = request.POST.get('remarks')
            obj.added_by = request.user.username

            # Save the updated object
            obj.save()
            
            # Generate the PDF for the fee record
            self.generate_pdf(obj.student_fee_id)

            self.message_user(request, "Student fee record updated successfully.")
            return HttpResponseRedirect(reverse('admin:app_student_fee_changelist'))

        return super().change_view(request, object_id, form_url, extra_context)


    # def save_model(self, request, obj, form, change):


    #     # Fetch the student ID from the POST data
    #     stuid = request.POST.get('student_id')
    #     # print(f"request.POST.get('student_id') :{request.POST.get('student_id')}")

    #     # Fetch the student_master instance using the primary key (stuid)
    #     try:
    #         #student_instance = student_master.objects.get(pk=stuid)
    #         student_instance = student_master.objects.get(student_id=stuid)
    #     except student_master.DoesNotExist:
    #         # Handle the case where the student does not exist
    #         raise ValueError(f"Student with ID {stuid} does not exist")

    #     # Now assign the student_master instance to obj.student_id
    #     obj.student_id = student_instance

    #     # Custom logic before saving the object
    #     today = datetime.now()  # Do not convert to string here
    #     year = int(request.POST.get('started_on'))

    #     # Now, you can access 'today.month' without issues
    #     if today.month < 4:
    #         year -= 1

    #     print(f"student_instance {student_instance}")

    #     print(f"Student ID: {student_instance.student_id}, Name: {student_instance.student_name}")

    #     # Assign the instance to the ForeignKey field
    #     # obj.student_id = student_instance

    #     student_class = request.POST.get('display_student_class', '')
    #     montharray = self.get_months_array(year)
    #     months = ','.join(map(str, montharray))

    #     if student_class:
    #         months_paid = student_fee.objects.filter(
    #             student_id=stuid,
    #             student_class=student_class,
    #             year=year
    #         ).values_list('fees_for_months', flat=True).distinct()
    #     else:
    #         months_paid = student_fee.objects.filter(
    #             student_id=stuid,
    #             student_class='',
    #             year=year
    #         ).values_list('fees_for_months', flat=True).distinct()

    #     months_paid = set(map(str.strip, ','.join(months_paid).split(',')))
    #     tmp = set(montharray) - months_paid
    #     tmpval = ','.join(map(str, tmp))

    #     if tmpval:
    #         alert_message = f'Fee pending for {tmpval} month '
    #         # Optionally use this alert message

    #     # Setting model attributes
    #     obj.payment_mode = request.POST.get('payment_mode')
    #     if obj.payment_mode == 'Cheque' and not obj.cheque_status:
    #         obj.cheque_status = 'Open'

    #     obj.date_payment = parse_date(request.POST.get('date_payment'))
    #     if obj.payment_mode != 'Cheque':
    #         obj.realized_date = obj.date_payment

    #     obj.entry_date = parse_date(request.POST.get('date_payment'))
    #     obj.student_class = request.POST.get('display_student_class')
    #     obj.student_section = request.POST.get('display_student_section')
    #     obj.fees_for_months = request.POST.get('fees_for_months')

    #     fees_period_month_list = request.POST.getlist('fees_period_month')  # Get the list of selected months
    #     obj.fees_period_month = ', '.join(fees_period_month_list)  # Join them as a string (e.g., '1, 2, 3')
    #     # request.POST.getlist('fees_period_month')

    #     obj.year = request.POST.get('started_on')
    #     obj.total_amount = float(request.POST.get('total_amount', 0))
    #     obj.amount_paid = float(request.POST.get('amount_paid', 0))

    #     # Handle concessions
    #     if request.POST.get('concession_applied') and float(request.POST.get('concession_applied')) > 0:
    #         obj.concession_applied = float(request.POST.get('concession_applied'))
    #         obj.concession_type_id = request.POST.get('concession_type')
    #     else:
    #         obj.concession_type_id = None
    #         obj.concession_applied = None

    #     # Setting other attributes
    #     # obj.bank_name = request.POST.get('bankname')
    #     # obj.branch_name = request.POST.get('branchname')
    #     # obj.cheq_no = request.POST.get('cheqno')
    #     obj.bus_fees_paid = float(request.POST.get('bus_fees_paid', 0))
    #     obj.dayboarding_fees_paid = float(request.POST.get('dayboarding_fees_paid', 0))
    #     obj.miscellaneous_fees_paid = float(request.POST.get('miscellaneous_fees_paid', 0))
    #     obj.late_fees_paid = float(request.POST.get('late_fees_paid', 0))
    #     obj.security_paid = float(request.POST.get('security_paid', 0))
    #     obj.admission_fees_paid = float(request.POST.get('admission_fees_paid', 0))
    #     obj.activity_fees = float(request.POST.get('activity_fees', 0))
    #     obj.sports_fees_paid = float(request.POST.get('sports_fees_paid', 0))
    #     obj.funds_fees_paid = float(request.POST.get('funds_fees_paid', 0))
    #     obj.tuition_fees_paid = float(request.POST.get('tuition_fees_paid', 0))
    #     obj.annual_fees_paid = float(request.POST.get('annual_fees_paid', 0))
    #     obj.isdefault = request.POST.get('isdefault')
    #     obj.remarks = request.POST.get('remarks')
    #     obj.added_by = request.user.username

    #     obj.save()
    #     self.generate_pdf(obj.student_fee_id)
        # self.message_user(request, "Student fee record saved successfully.")

    def get_months_array(self, year):
        # Format the start and end date for the financial year
        date_from = datetime(year, 4, 1)  # April 1st of the given year
        date_to = datetime(year + 1, 3, 31)  # March 31st of the next year

        # Convert the dates into string format if necessary
        current_date = datetime.now()

        # If the financial year is not over, adjust the end date to today
        if current_date < date_to:
            date_to = current_date

        # Create an array for storing the months
        month_array = []

        # Initialize a timestamp for the start date
        time = date_from

        # Loop through the months of the financial year
        while time <= date_to:
            # Get the current month number and strip leading zeroes
            cur_month = time.month

            # Append the current month to the array
            month_array.append(cur_month)

            # Move to the next month
            time += timedelta(days=32)
            time = time.replace(day=1)  # Set the day to 1 to handle month transitions

        # Sort the month array in ascending order
        month_array.sort()

        # If the financial year is over, return an array of all 12 months
        if current_date >= datetime(year + 1, 3, 31):
            month_array = list(range(1, 13))

        return month_array

    def generate_pdf(self, student_fee_id):
        # Your implementation for generating PDF
        pass


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





# admin.site.register(generate_mobile_number_list,GenerateMobileNumbersListAdmin)


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


# admin.site.register(cheque_status, ChequeStatusListAdmin)

# # admin.site.register(transport)
# from django.contrib import admin
# from .models import transport, StudentMaster

# Custom admin class for the transport model
# from django.contrib import admin
# from .models import transport, StudentMaster, StudentClass, BusFeesMaster, BusMaster
# from django.db.models import OuterRef, Subquery

# class TransportAdmin(admin.ModelAdmin):
#     list_display = ('student_id', 'student_name', 'admission_no', 'bus_id', 'status')
#     search_fields = ('student_name', 'admission_no', 'bus_id')
#     list_filter = ('status',)

#     def get_queryset(self, request):
#         # Get filter parameters from the request
#         busno = request.GET.get('busno', None)
#         c = request.GET.get('class', None)  # 'class' might be a reserved keyword, use 'class_no'
#         d = request.GET.get('destination', None)

#         # Build the route and destination conditions
#         busfees_filter = {}
#         if busno:
#             busfees_filter['route'] = busno
#         if d:
#             busfees_filter['destination'] = d

#         # Filter students who are not "passed out"
#         student_filter = {'status__ne': 'passed out'}

#         # Get the latest student_class_id for each student (subquery)
#         subquery = StudentClass.objects.filter(student_id=OuterRef('student_id')).order_by('-student_class_id').values('student_class_id')[:1]
        

#         # Filter based on bus route and destination
#         bus_fees = BusFeesMaster.objects.filter(**busfees_filter)

#         # Filter students manually based on conditions
#         queryset = StudentMaster.objects.filter(
#             student_id__in=Subquery(
#                 StudentClass.objects.filter(student_class_id=subquery).values('student_id')
#             ),
#             bus_id__in=bus_fees.values('bus_id'),
#             **student_filter
#         )

#         # Apply class filter if provided
#         if c:
#             queryset = queryset.filter(
#                 student_id__in=StudentClass.objects.filter(class_no=c).values('student_id')
#             )

#     #         # Now get the bus details from BusMaster
#         bus_routes = BusMaster.objects.filter(bus_route__in=bus_fees.values('route'))

#         # Build the transport details
#         trdetails = ""

#         for student in students:
#             student_class = StudentClass.objects.filter(student_id=student.student_id).first()
#             bus_fees_record = bus_fees.filter(bus_id=student.bus_id).first()
#             bus_route_record = bus_routes.filter(bus_route=bus_fees_record.route).first()

#             trdetails += f"{student.student_id}*{student.student_name}*" \
#                         f"{student.admission_no}*{student_class.class_no}*" \
#                         f"{student_class.section}*{bus_fees_record.destination}*" \
#                         f"{bus_fees_record.route}*{student.father_name}*" \
#                         f"{student.phone_no}*{bus_route_record.bus_driver}*" \
#                         f"{bus_route_record.driver_phone}*{bus_route_record.bus_conductor}*" \
#                         f"{bus_route_record.conductor_phone}*" \
#                         f"{bus_route_record.bus_attendant}*{bus_route_record.attendant_phone}&"



#         return queryset

# Register the transport model with the custom admin class
# admin.site.register(transport, TransportAdmin)
# from django.contrib import admin
# from .models import transport, StudentMaster, StudentClass, BusFeesMaster, BusMaster
# from django.db.models import OuterRef, Subquery
# from collections import namedtuple

# class TransportAdmin(admin.ModelAdmin):
#     list_display = ('student_id', 'student_name', 'admission_no', 'class_no', 'section', 'destination', 'route', 'father_name', 'phone_no', 'bus_driver', 'driver_phone', 'bus_conductor', 'conductor_phone', 'bus_attendant', 'attendant_phone')
#     search_fields = ('student_name', 'admission_no', 'bus_id')
#     list_filter = ('status',)

#     def get_queryset(self, request):
#         # Get filter parameters from the request
#         busno = request.GET.get('busno', None)
#         c = request.GET.get('class', None)
#         d = request.GET.get('destination', None)

#         # Build the route and destination conditions
#         busfees_filter = {}
#         if busno:
#             busfees_filter['route'] = busno
#         if d:
#             busfees_filter['destination'] = d

#         # Filter students who are not "passed out"
#         student_filter = {'status__ne': 'passed out'}

#         # Get the latest student_class_id for each student (subquery)
#         subquery = student_class.objects.filter(student_id=OuterRef('student_id')).order_by('-student_class_id').values('student_class_id')[:1]

#         # Filter based on bus route and destination
#         bus_fees = BusFeesMaster.objects.filter(**busfees_filter)

#         # Filter students manually based on conditions
#         queryset = student_master.objects.filter(
#             student_id__in=Subquery(
#                 student_class.objects.filter(student_class_id=subquery).values('student_id')
#             ),
#             bus_id__in=bus_fees.values('bus_id'),
#             **student_filter
#         )

#         # Apply class filter if provided
#         if c:
#             queryset = queryset.filter(
#                 student_id__in=student_class.objects.filter(class_no=c).values('student_id')
#             )

#         # Fetch bus route details from BusMaster
#         bus_routes = BusMaster.objects.filter(bus_route__in=bus_fees.values('route'))

#         # Define a named tuple to represent the custom fields
#         TransportDetails = namedtuple('TransportDetails', [
#             'student_id', 'student_name', 'admission_no', 'class_no', 'section', 'destination', 
#             'route', 'father_name', 'phone_no', 'bus_driver', 'driver_phone', 
#             'bus_conductor', 'conductor_phone', 'bus_attendant', 'attendant_phone'
#         ])

#         # Build a list of custom objects with transport details
#         custom_queryset = []
#         for student in queryset:
#             student_class1 = student_class.objects.filter(student_id=student.student_id).first()
#             bus_fees_record = bus_fees.filter(bus_id=student.bus_id).first()
#             bus_route_record = bus_routes.filter(bus_route=bus_fees_record.route).first()

#             # Create an object for each student with the desired fields
#             transport_detail = TransportDetails(
#                 student_id=student.student_id,
#                 student_name=student.student_name,
#                 admission_no=student.admission_no,
#                 class_no=student_class1.class_no if student_class1 else None,
#                 section=student_class1.section if student_class1 else None,
#                 destination=bus_fees_record.destination if bus_fees_record else None,
#                 route=bus_fees_record.route if bus_fees_record else None,
#                 father_name=student.father_name,
#                 phone_no=student.phone_no,
#                 bus_driver=bus_route_record.bus_driver if bus_route_record else None,
#                 driver_phone=bus_route_record.driver_phone if bus_route_record else None,
#                 bus_conductor=bus_route_record.bus_conductor if bus_route_record else None,
#                 conductor_phone=bus_route_record.conductor_phone if bus_route_record else None,
#                 bus_attendant=bus_route_record.bus_attendant if bus_route_record else None,
#                 attendant_phone=bus_route_record.attendant_phone if bus_route_record else None
#             )

#             # Append the transport detail object to the custom queryset
#             custom_queryset.append(transport_detail)

#         # Return the custom queryset (a list of TransportDetails named tuples)
#         return custom_queryset

# # Register the transport model with the custom admin class
# admin.site.register(transport, TransportAdmin)

# from django.contrib import admin
# from .models import transport, StudentMaster, StudentClass, BusFeesMaster, BusMaster
from django.db.models import OuterRef, Subquery
from collections import namedtuple

class TransportAdmin(admin.ModelAdmin):
    # Define methods to display custom fields in the list display
    list_display = (
        'get_student_id', 'get_student_name', 'get_admission_no', 'get_class_no', 
        'get_section', 'get_destination', 'get_route', 'get_father_name', 
        'get_phone_no', 'get_bus_driver', 'get_driver_phone', 'get_bus_conductor', 
        'get_conductor_phone', 'get_bus_attendant', 'get_attendant_phone'
    )
    # search_fields = ('student_name', 'admission_no', 'bus_id')
    # list_filter = ('status',)

    def get_queryset(self, request):
        # Get filter parameters from the request
        busno = request.GET.get('busno', None)
        c = request.GET.get('class', None)
        d = request.GET.get('destination', None)

        # Build the route and destination conditions
        busfees_filter = {}
        if busno:
            busfees_filter['route'] = busno
        if d:
            busfees_filter['destination'] = d

        # Filter students who are not "passed out"
        # student_filter = {'status__ne': 'passed out'}
        student_filter = {'status': 'passed out'}


        # Get the latest student_class_id for each student (subquery)
        subquery = student_class.objects.filter(student_id=OuterRef('student_id')).order_by('-student_class_id').values('student_class_id')[:1]

        # Filter based on bus route and destination
        bus_fees = busfees_master.objects.filter(**busfees_filter)

        # Filter students manually based on conditions
        # queryset = student_master.objects.filter(
        #     student_id__in=Subquery(
        #         student_class.objects.filter(student_class_id=subquery).values('student_id')
        #     ),
        #     bus_id__in=bus_fees.values('bus_id'),
        #     **student_filter
        # )

        queryset = student_master.objects.filter(
            student_id__in=Subquery(
                student_class.objects.filter(student_class_id=subquery).values('student_id')
            ),
            bus_id__in=bus_fees.values('bus_id')
        ).exclude(**student_filter)


        # Apply class filter if provided
        if c:
            queryset = queryset.filter(
                student_id__in=student_class.objects.filter(class_no=c).values('student_id')
            )

        # Fetch bus route details from BusMaster
        bus_routes = bus_master.objects.filter(bus_route__in=bus_fees.values('route'))

        # Define a named tuple to represent the custom fields
        TransportDetails = namedtuple('TransportDetails', [
            'student_id', 'student_name', 'admission_no', 'class_no', 'section', 'destination', 
            'route', 'father_name', 'phone_no', 'bus_driver', 'driver_phone', 
            'bus_conductor', 'conductor_phone', 'bus_attendant', 'attendant_phone'
        ])

        # Build a list of custom objects with transport details
        self.custom_queryset = []
        for student in queryset:
            student_class1 = student_class.objects.filter(student_id=student.student_id).first()
            bus_fees_record = bus_fees.filter(bus_id=student.bus_id).first()
            bus_route_record = bus_routes.filter(bus_route=bus_fees_record.route).first()

            # Create an object for each student with the desired fields
            transport_detail = views.DictWithAttributeAccess({
                "student_id":student.student_id,
                "student_name":student.student_name,
                "admission_no":student.addmission_no,
                "class_no":student_class1.class_no if student_class1 else None,
                "section":student_class1.section if student_class1 else None,
                "destination":bus_fees_record.destination if bus_fees_record else None,
                "route":bus_fees_record.route if bus_fees_record else None,
                "father_name":student.father_name,
                "phone_no":student.phone_no,
                "bus_driver":bus_route_record.bus_driver if bus_route_record else None,
                "driver_phone":bus_route_record.driver_phone if bus_route_record else None,
                "bus_conductor":bus_route_record.bus_conductor if bus_route_record else None,
                "conductor_phone":bus_route_record.conductor_phone if bus_route_record else None,
                "bus_attendant":bus_route_record.bus_attendant if bus_route_record else None,
                "attendant_phone":bus_route_record.attendant_phone if bus_route_record else None
            })

            # Append the transport detail object to the custom queryset
            self.custom_queryset.append(transport_detail)

        # Return the custom queryset (a list of TransportDetails named tuples)
        return self.custom_queryset

    # Define methods for each field to display in list_display
    def get_student_id(self, obj):
        return obj.student_id

    def get_student_name(self, obj):
        return obj.student_name

    def get_admission_no(self, obj):
        return obj.admission_no

    def get_class_no(self, obj):
        return obj.class_no

    def get_section(self, obj):
        return obj.section

    def get_destination(self, obj):
        return obj.destination

    def get_route(self, obj):
        return obj.route

    def get_father_name(self, obj):
        return obj.father_name

    def get_phone_no(self, obj):
        return obj.phone_no

    def get_bus_driver(self, obj):
        return obj.bus_driver

    def get_driver_phone(self, obj):
        return obj.driver_phone

    def get_bus_conductor(self, obj):
        return obj.bus_conductor

    def get_conductor_phone(self, obj):
        return obj.conductor_phone

    def get_bus_attendant(self, obj):
        return obj.bus_attendant

    def get_attendant_phone(self, obj):
        return obj.attendant_phone

    # Set short descriptions for admin display
    get_student_id.short_description = 'Student ID'
    get_student_name.short_description = 'Student Name'
    get_admission_no.short_description = 'Admission No'
    get_class_no.short_description = 'Class No'
    get_section.short_description = 'Section'
    get_destination.short_description = 'Destination'
    get_route.short_description = 'Route'
    get_father_name.short_description = 'Father Name'
    get_phone_no.short_description = 'Phone No'
    get_bus_driver.short_description = 'Bus Driver'
    get_driver_phone.short_description = 'Driver Phone'
    get_bus_conductor.short_description = 'Bus Conductor'
    get_conductor_phone.short_description = 'Conductor Phone'
    get_bus_attendant.short_description = 'Bus Attendant'
    get_attendant_phone.short_description = 'Attendant Phone'

# Register the transport model with the custom admin class
# admin.site.register(transport, TransportAdmin)


# class CustomAdminSite(admin.AdminSite):
#     site_header = "School Admin"
#     site_title = "Admin Portal"
#     index_title = "Welcome to School Admin"

# # Create a custom admin site instance
# custom_admin_site = CustomAdminSite(name='custom_admin')

# # Register models under custom sections
# custom_admin_site.register(student_master, StudentMasterAdmin)
# custom_admin_site.register(student_fee, StudentFeesAdmin)

# custom_admin_site.register(cheque_status, ChequeStatusListAdmin)

# custom_admin_site.register(transport, TransportAdmin)

# try:
#     admin.site.unregister(student_master)
#     admin.site.unregister(student_fee)
#     admin.site.unregister(cheque_status)
#     admin.site.unregister(transport)
# except admin.sites.NotRegistered:
#     pass



# from django.contrib import admin
# from django.contrib import admin
# from .models import (
#     user, student_master, student_fee, student_class, specialfee_master,
#     payment_schedule_master, latefee_master, fees_master, expense,
#     concession_master, bus_master, busfees_master, account_head,generate_mobile_number_list, cheque_status, transport
# )

# class CustomAdminSite(admin.AdminSite):
#     site_header = "School Admin"
#     site_title = "Admin Portal"
#     index_title = "Welcome to School Admin"

# # Create an instance of the custom admin site
# custom_admin_site = CustomAdminSite(name='custom_admin')

# # Register models to the custom admin site
# custom_admin_site.register(student_master)
# custom_admin_site.register(student_fee)
# custom_admin_site.register(cheque_status)
# custom_admin_site.register(transport)

# # Optionally, unregister these models from the default admin site
# try:
#     admin.site.unregister(student_master)
#     admin.site.unregister(student_fee)
#     admin.site.unregister(cheque_status)
#     admin.site.unregister(transport)
# except admin.sites.NotRegistered:
#     pass

# print(custom_admin_site._registry)

# admin.site.register(student_master)
# admin.site.register(student_fee)

# # Register Group 2 models
# admin.site.register(cheque_status)
# admin.site.register(transport)








   
    








