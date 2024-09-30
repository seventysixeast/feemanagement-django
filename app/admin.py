from django.contrib import admin
from .models import (
    student_master, student_fee, student_class, specialfee_master,
    payment_schedule_master, latefee_master, fees_master, expense,
    concession_master, bus_master, busfees_master, account_head,generate_mobile_number_list, 
)
from django.db.models import Max
from django import forms
from datetime import date, timezone
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
from django.utils.html import format_html


from django.utils.dateparse import parse_date
from datetime import datetime
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import get_object_or_404
# from multiselectfield import MultiSelectField

from django.contrib import messages
from django.db import IntegrityError, transaction
from django.utils.translation import gettext_lazy as _

from .services import last_payment_record,fetch_fee_details_for_class,get_special_fee,calculate_late_fee,generate_pdf2,get_months_array

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
            
        # print("======= I'M HERE ===========")

    class Media:
        js = ('app/js/student_fees.js',)  # Adjust the path as necessary
        css = {
            'all': ('app/css/custom_admin.css',)  # Add your custom CSS file here
        }


class StudentFeesAdmin(admin.ModelAdmin):

    form = StudentFeesAdminForm

    change_form_template = 'admin/student_fee/change_form.html'

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
        'download_link',  # Add the custom download link method
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

    def download_link(self, obj):
        """Generate a clickable link for the receipt URL."""
        if obj.receipt_url:
            return format_html(
                '<a href="{}" download>{}</a>',
                obj.receipt_url,
                'Download Receipt'  # The link text
            )
        return "-"
        # """Generate a download link for the receipt URL."""
        # if obj.receipt_url:
        #     return format_html(
        #         '<a href="{}" download><img src="{}" alt="Download" style="width: 20px; height: 20px;"/></a>',
        #         obj.receipt_url,
        #         'path/to/download_icon.png'  # Replace with your actual icon path
        #     )
        # return "-"
    
    download_link.short_description = 'Download Receipt'  # Column name in admin

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
        
        previous_fee_info = last_payment_record(sid)

        print(f" +++++++ previous_fee_info +++++++ {previous_fee_info}")

        include_admission_fee = not previous_fee_info  # Include admission fee if no previous fee record
        pay_months = mf
        months_in_quarters = [
            '4,5,6',
            '7,8,9',
            '10,11,12',
            '1,2,3'
        ]

        target_months = pay_months
        target_months_array = target_months.split(',')
        quarters = []

        for quarter in months_in_quarters:
            quarter_months = quarter.split(',')
            intersection = list(set(quarter_months) & set(target_months_array))
            if intersection:
                quarters.append({
                    'quarter': quarter,
                    'months_paid': ','.join(intersection),
                })

        student_id = sid
        class_no = cls
        year = yr
        class_year = yr
        total_fees_payable = 0
        fee_details = fetch_fee_details_for_class(student_id, class_no)

        print(f" +++++++ fee_details +++++++ {fee_details}")

        if fee_details:
            current_payment_details = {
                'class_no': class_no,
                'annual_fees': fee_details.get('annual_fees', 0),
                'tuition_fees': fee_details.get('tuition_fees', 0),
                'funds_fees': fee_details.get('funds_fees', 0),
                'sports_fees': fee_details.get('sports_fees', 0),
                'admission_fees': fee_details.get('admission_fees', 0),
                'security_fees': fee_details.get('security_fees', 0),
                'dayboarding_fees': fee_details.get('dayboarding_fees', 0),
                'miscellaneous_fees': fee_details.get('miscellaneous_fees', 0),
                'bus_fees': fee_details.get('bus_fees', 0),
                'busfee_not_applicable_in_months': fee_details.get('busfee_not_applicable_in_months', ''),
                'bus_id': fee_details.get('bus_id', 0),
                'concession_percent': fee_details.get('concession_percent', ''),
                'concession_type': fee_details.get('concession_type', ''),
                'activity_fees': fee_details.get('activity_fees', 0),
                'activity_fees_mandatory': fee_details.get('activity_fees_mandatory', 0),
                'concession_amount': fee_details.get('concession_amount', 0),
                'concession_id': fee_details.get('concession_id', 0),
                'is_april_checked': fee_details.get('is_april_checked', 0),
                'concession_applied': 0
            }

            current_payment_details_array = []

            for quarter in quarters:
                current_date = datetime.now().strftime("%Y-%m-%d")  # Example current date
                fees_for_months = quarter['quarter']
                months_paid_for = quarter['months_paid']

                # Clone current payment details to modify and calculate total
                payment_details = current_payment_details.copy()
                payment_details['fees_for_months'] = fees_for_months
                payment_details['fees_period_month'] = months_paid_for

                total = 0
                if include_admission_fee:
                    include_admission_fee = False
                else:
                    payment_details['admission_fees'] = 0

                fields_to_calculate = [
                    'tuition_fees', 'funds_fees', 'sports_fees', 'bus_fees', 'activity_fees', 
                    'dayboarding_fees', 'miscellaneous_fees', 'annual_fees', 'admission_fees'
                ]

                activity_fees_mandatory = payment_details['activity_fees_mandatory']
                fees_for_months_array = payment_details['fees_period_month'].split(',')

                for field in fields_to_calculate:
                    numeric_value = float(payment_details.get(field, 0) or 0)

                    if field == 'activity_fees':
                        activity_fee_applicable = get_special_fee(student_id, year, payment_details['fees_period_month'], field)
                        if activity_fee_applicable is not None:
                            numeric_value = activity_fee_applicable
                        elif activity_fees_mandatory != 1:
                            numeric_value = 0

                    elif field == 'bus_fees':
                        not_applicable_months_array = (payment_details.get('busfee_not_applicable_in_months') or '').split(',')

                        overlap_months = set(not_applicable_months_array) & set(fees_for_months_array)
                        applicable_months = set(fees_for_months_array) - overlap_months
                        bus_fee_applied = 0

                        if applicable_months:
                            bus_fee_for_applicable_months = get_special_fee(student_id, year, ','.join(applicable_months), 'bus_fees')
                            for month in applicable_months:
                                bus_fee_applied += bus_fee_for_applicable_months.get(month, numeric_value)

                            numeric_value = bus_fee_applied

                    elif numeric_value > 0 and field in ['tuition_fees', 'funds_fees']:
                        fee_applicable = get_special_fee(student_id, year, payment_details['fees_for_months'], field)
                        if fee_applicable is not None:
                            numeric_value = float(fee_applicable)
                        numeric_value *= len(fees_for_months_array)

                    elif field in ['annual_fees', 'miscellaneous_fees', 'sports_fees', 'admission_fees']:
                        if fees_for_months == '4,5,6':
                            fee_applicable = get_special_fee(student_id, year, payment_details['fees_for_months'], field)
                            if fee_applicable is not None:
                                numeric_value = float(fee_applicable)
                        else:
                            numeric_value = 0

                    total += numeric_value
                    payment_details[field] = numeric_value

                # Apply concession
                concession_amount = 0
                if payment_details['concession_percent'] == 'percentage':
                    concession_amount = (float(payment_details['tuition_fees']) * float(payment_details['concession_amount'])) / 100
                elif payment_details['concession_percent'] == 'amount':
                    concession_amount = float(payment_details['concession_amount'])

                if '4' in fees_for_months_array and payment_details['is_april_checked'] == 0:
                    concession_amount = round(concession_amount / len(fees_for_months_array) * (len(fees_for_months_array) - 1), 0)

                total -= concession_amount
                payment_details['concession_applied'] = concession_amount

                # Calculate late fee
                late_fee = calculate_late_fee(total, fees_for_months, class_year, current_date, None)
                payment_details['late_fee'] = late_fee
                total += late_fee

                payment_details['total_fee'] = total
                total_fees_payable += total

                current_payment_details_array.append(payment_details)

                fee_details

            sum_dict = {
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
            'concession_applied': 0,
            'late_fee': 0,
            'total_fee': 0,
        }

        excluded_keys = ['concession_amount', 'concession_percent', 'concession_id', 'concession_type']

        for details in current_payment_details_array:
            for key in sum_dict:
                sum_dict[key] += details.get(key, 0)
            for key in excluded_keys:
                sum_dict[key] = details.get(key)

            # return JsonResponse(sum_dict)
            response_data = "|".join([str(sum_dict[key]) for key in sum_dict])

            # return JsonResponse(sum_fees)
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
            montharray = get_months_array(year)
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
            generate_pdf2(request,obj.student_fee_id)

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
            montharray = get_months_array(year)
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
            generate_pdf2(request,obj.student_fee_id)

            self.message_user(request, "Student fee record updated successfully.")
            return HttpResponseRedirect(reverse('admin:app_student_fee_changelist'))

        return super().change_view(request, object_id, form_url, extra_context)

    class Media:
        
        js = ('app/js/student_fees.js',)

admin.site.register(student_fee,StudentFeesAdmin)
# admin.site.register(student_fee)





class ClassFilter(admin.SimpleListFilter):
    title = 'Class'
    parameter_name = 'class_no'

    def lookups(self, request, model_admin):
        return []

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
        return []

    # def lookups(self, request, model_admin):
    #     # Get all distinct section values from student_class and order them alphabetically
    #     sections = student_class.objects.values_list('section', flat=True).distinct().order_by('section')

    #     # Return as tuples for lookups
    #     return [(section, section) for section in sections]

    # def queryset(self, request, queryset):
    #     return queryset  # We handle filtering in get_queryset()


class YearFilter(admin.SimpleListFilter):
    title = 'Year'
    parameter_name = 'year'

    def lookups(self, request, model_admin):
        return []

    # def lookups(self, request, model_admin):
    #     # Create a list of years from 2024 to 2018
    #     years = [(str(year), str(year)) for year in range(2024, 2017, -1)]
    #     return years

    # def queryset(self, request, queryset):
    #     # Return the queryset unchanged since this filter is not used for filtering
    #     return queryset


class GenerateMobileNumbersListAdmin(admin.ModelAdmin):
    list_display = ('addmission_no', 'student_name', 'get_class_no', 'get_section', 'mobile_no')
    list_filter = (ClassFilter, SectionFilter, YearFilter)
    # change_list_template = 'admin/generate_mobile_number_changelist.html'  # Specify your custom template here

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def get_class_no(self, obj):
        # student_class_instance = student_class.objects.filter(student_id=obj.student_id).order_by('-started_on').first()
        # return student_class_instance.class_no if student_class_instance else None
        search_class_no = self._request.GET.get('class_no', None)

        # Filter by class_no and/or section if available
        if search_class_no:
            student_class_instance = student_class.objects.filter(student_id=obj.student_id, class_no=search_class_no).order_by('-started_on').first()
        else:
            student_class_instance = student_class.objects.filter(student_id=obj.student_id).order_by('-started_on').first()

        return student_class_instance.class_no if student_class_instance else None

    get_class_no.short_description = 'Class'

    def get_section(self, obj):
        # student_class_instance = student_class.objects.filter(student_id=obj.student_id).order_by('-started_on').first()
        # return student_class_instance.section if student_class_instance else None

        search_class_no = self._request.GET.get('class_no', None)

        # Filter by class_no and/or section if available
        if search_class_no:
            student_class_instance = student_class.objects.filter(student_id=obj.student_id, class_no=search_class_no).order_by('-started_on').first()
        else:
            student_class_instance = student_class.objects.filter(student_id=obj.student_id).order_by('-started_on').first()

        return student_class_instance.section if student_class_instance else None
    
    get_section.short_description = 'Section'

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        
        # Add filter values to the context
        # extra_context['class_numbers'] = student_class.objects.values_list('class_no', flat=True).distinct()
        extra_context['class_numbers'] = CLASS_CHOICES
        # extra_context['sections'] = student_class.objects.values_list('section', flat=True).distinct()

        # sections = student_class.objects.values_list('section', flat=True).distinct().order_by('section')
        sections = student_class.objects.values_list('section', flat=True).exclude(section='').distinct().order_by('section')


        # Return as tuples for lookups
        extra_context['sections'] = [(section, section) for section in sections]
        # extra_context['years'] = student_class.objects.values_list('started_on__year', flat=True).distinct()
        # extra_context['years'] = [str(year) for year in range(2024, 2017, -1)]
        year_choices = [str(year) for year in range(2024, 2017, -1)]
        extra_context['year_choices'] = year_choices
        self._request = request
        return super().changelist_view(request, extra_context=extra_context)

    change_list_template = 'admin/generate_mobile_number_changelist.html'

    def get_search_results(self, request, queryset, search_term):
        """
        Overrides get_search_results to handle search and filtering with class_no, section, and year.
        """
        # Get the default queryset (with search fields applied)
        queryset, use_distinct = super().get_search_results(request, queryset, search_term)

        # Retrieve filters from the request
        requested_class_no = request.GET.get('class_no')
        requested_section = request.GET.get('section')
        year_filter_selected = request.GET.get('year')

        # Apply class and section filters if provided
        if requested_class_no or requested_section:
            # Get student IDs that match the class and section filters
            student_ids = set()

            if requested_class_no:
                student_ids.update(
                    student_class.objects.filter(class_no=requested_class_no).values_list('student_id', flat=True)
                )

            if requested_section:
                student_ids.update(
                    student_class.objects.filter(section=requested_section).values_list('student_id', flat=True)
                )

            # Filter the queryset based on student IDs
            queryset = queryset.filter(student_id__in=student_ids)

        # Apply year filter if selected
        if year_filter_selected:
            # queryset = queryset.filter(some_year_field=year_filter_selected)  # Customize this to your year field
            # Optionally handle year filter logic here
            pass

        return queryset, use_distinct


    def export_as_csv(self, request, queryset):
        meta = self.model._meta
        # field_names = ['addmission_no', 'student_name', 'Class', 'Section', 'mobile_no']
        field_names = ['Addmission no', 'Student Name', 'Class', 'Section', 'Mobile No']

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


admin.site.register(generate_mobile_number_list,GenerateMobileNumbersListAdmin)








   
    








