from django.contrib import admin
from .models import (
    transport, tuition_fees_defaulter,admission_report,collection_report,activity_fees_defaulter
)

from app.models import (
    student_master, student_fee, student_class, specialfee_master,
    payment_schedule_master, latefee_master, fees_master, expense,
    concession_master, bus_master, busfees_master, account_head,generate_mobile_number_list
)

from import_export import resources
from import_export.admin import ExportMixin
from import_export.fields import Field


from django.db.models import OuterRef, Subquery
from django.contrib import admin
from django.urls import path
from django.http import JsonResponse
from django.shortcuts import render

# from .models import TuitionFeesDefaulter, student_master, student_classes
from datetime import date
from django.db.models.functions import Concat

from django.db.models.expressions import RawSQL

# from django.db.models import F, Value, CharField, ExpressionWrapper, Q
from django.db.models.functions import Coalesce
from django.db.models import DecimalField

from django.db.models import Case, When, Value, F, Q, CharField, ExpressionWrapper, DecimalField

from django.utils.html import format_html
from django.utils import timezone
from datetime import datetime

from django.db.models import Subquery, OuterRef
from django.db.models import Exists, OuterRef

from django.db.models import Sum, Max
from datetime import datetime, timedelta
from django import forms
from django.template.response import TemplateResponse

import csv
from django.http import HttpResponse
from django.urls import path
from django.shortcuts import render

from django.db import connection
import pandas as pd
from io import BytesIO
from django.contrib import messages
from django.shortcuts import redirect
from MySQLdb.cursors import DictCursor


# from .forms import DefaultersReportForm


# from .models import transport, BusFeesMaster, BusMaster, StudentClasses

class BusRouteFilter(admin.SimpleListFilter):
    title = 'Bus Route'
    parameter_name = 'bus_route'

    def lookups(self, request, model_admin):
        return []

class DestinationFilter(admin.SimpleListFilter):
    title = 'Destination'
    parameter_name = 'destination'

    def lookups(self, request, model_admin):
        return []

class ClassFilter(admin.SimpleListFilter):
    title = 'Class'
    parameter_name = 'class_no'

    def lookups(self, request, model_admin):
        return []

# Define class choices
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

def get_months_array(year):
    start_date = date(year, 4, 1)
    end_date = date(year + 1, 3, 31)
    current_date = date.today()

    months = []
    time = start_date
    if current_date < end_date:
        end_date = current_date

    while time <= end_date:
        months.append(time.month)
        next_month = (time.month % 12) + 1
        next_year = time.year + (1 if next_month == 1 else 0)
        time = date(next_year, next_month, 1)

    return months

def calculate_unpaid_months(paid_months, months_array):
        # print('paid_months in calculate_unpaid_months', paid_months)
        # print('months_array in calculate_unpaid_months', months_array)
        if not paid_months:
            return ','.join(map(str, months_array))  # Return all months if no months are paid

        paid_months_list = list(map(int, paid_months.split(',')))
        unpaid_months = set(months_array) - set(paid_months_list)
        return ','.join(map(str, sorted(unpaid_months)))

class TransportMasterResource(resources.ModelResource):

    class Meta:
        model = transport
        fields = ('student_name', 'addmission_no', 'class_no', 'section', 'destination', 'route', 
        'father_name', 'phone_no', 'bus_driver', 'driver_phone', 'bus_conductor', 
        'conductor_phone', 'bus_attendant', 'attendant_phone')

    student_name = Field(attribute='student_name', column_name='Student Name')
    addmission_no = Field(attribute='addmission_no', column_name='Admission No')
    class_no = Field(attribute='class_no', column_name='Class')
    section = Field(attribute='section', column_name='Section')
    destination = Field(attribute='destination', column_name='Destination')

    route = Field(attribute='route', column_name='Route')
    father_name = Field(attribute='father_name', column_name='Father Name')
    phone_no = Field(attribute='phone_no', column_name='Phone No.')
    bus_driver = Field(attribute='bus_driver', column_name='Bus Driver')
    driver_phone = Field(attribute='driver_phone', column_name='Driver Phone')

    bus_conductor = Field(attribute='bus_conductor', column_name='Bus Conductor')
    conductor_phone = Field(attribute='conductor_phone', column_name='Conductor Phone')
    bus_attendant = Field(attribute='bus_attendant', column_name='Bus Attendant')
    attendant_phone = Field(attribute='attendant_phone', column_name='Attendant Phone')

    def dehydrate_class_no(self, obj):
        # Assuming 'bus_driver' is a related field on the model
        student_class_instance = student_class.objects.filter(student_id=obj.student_id).order_by('-started_on').first()
        return student_class_instance.class_no if student_class_instance else None
        # return obj.class_no if obj.class_no else ''

    
    def dehydrate_section(self, obj):
        student_class_instance = student_class.objects.filter(student_id=obj.student_id).order_by('-started_on').first()
        return student_class_instance.section if student_class_instance else None
    # get_section.short_description = 'Section'


    def dehydrate_route(self, obj):
        busfees_master_instance = busfees_master.objects.filter(bus_id=obj.bus_id).first()
        return busfees_master_instance.route if busfees_master_instance else None
        # return obj.route

    def dehydrate_destination(self, obj):
        busfees_master_instance = busfees_master.objects.filter(bus_id=obj.bus_id).first()
        return busfees_master_instance.destination if busfees_master_instance else None
        # return obj.destination


    def dehydrate_bus_driver(self, obj):
        busfees_master_instance = busfees_master.objects.filter(bus_id=obj.bus_id).first()
        bus_master_instance = bus_master.objects.filter(bus_route=busfees_master_instance.route).first() if busfees_master_instance else None
        return bus_master_instance.bus_driver if bus_master_instance else None
        # return obj.bus_driver
    
    def dehydrate_driver_phone(self, obj):
        busfees_master_instance = busfees_master.objects.filter(bus_id=obj.bus_id).first()
        bus_master_instance = bus_master.objects.filter(bus_route=busfees_master_instance.route).first() if busfees_master_instance else None
        return bus_master_instance.driver_phone if bus_master_instance else None

    def dehydrate_bus_conductor(self, obj):
        busfees_master_instance = busfees_master.objects.filter(bus_id=obj.bus_id).first()
        bus_master_instance = bus_master.objects.filter(bus_route=busfees_master_instance.route).first() if busfees_master_instance else None
        return bus_master_instance.bus_conductor if bus_master_instance else None
        # return obj.bus_conductor

    def dehydrate_conductor_phone(self, obj):
        busfees_master_instance = busfees_master.objects.filter(bus_id=obj.bus_id).first()
        bus_master_instance = bus_master.objects.filter(bus_route=busfees_master_instance.route).first() if busfees_master_instance else None
        return bus_master_instance.conductor_phone if bus_master_instance else None
        # return obj.conductor_phone

    def dehydrate_bus_attendant(self, obj):
        busfees_master_instance = busfees_master.objects.filter(bus_id=obj.bus_id).first()
        bus_master_instance = bus_master.objects.filter(bus_route=busfees_master_instance.route).first() if busfees_master_instance else None
        return bus_master_instance.bus_attendant if bus_master_instance else None
        # return obj.bus_attendant

    def dehydrate_attendant_phone(self, obj):
        busfees_master_instance = busfees_master.objects.filter(bus_id=obj.bus_id).first()
        bus_master_instance = bus_master.objects.filter(bus_route=busfees_master_instance.route).first() if busfees_master_instance else None
        return bus_master_instance.attendant_phone if bus_master_instance else None


class TransportAdmin(ExportMixin,admin.ModelAdmin):
    resource_class = TransportMasterResource
    list_display = (
        'student_name', 'addmission_no', 'class_no', 'section', 'destination', 'route', 
        'father_name', 'phone_no', 'bus_driver', 'driver_phone', 'bus_conductor', 
        'conductor_phone', 'bus_attendant', 'attendant_phone'
    )

   

    list_filter = (BusRouteFilter, DestinationFilter, ClassFilter)

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

        # Override get_search_results to handle custom filtering
    def get_search_results(self, request, queryset, search_term):
        bus_route = request.GET.get('bus_route', None)
        destination = request.GET.get('destination', None)
        class_no = request.GET.get('class_no', None)
        print('bus_route',bus_route)

         # If no filters are selected, return an empty queryset
        if not bus_route and not destination and not class_no:
            return queryset.none(), False

        # Annotate the queryset with related fields
        # latest_student_class = student_class.objects.filter(
        #     student_id=OuterRef('student_id')
        # ).order_by('-student_class_id')

        # bus_route_subquery = busfees_master.objects.filter(
        #     bus_id=OuterRef('bus_id')
        # ).values('route')[:1]

        # bus_destination_subquery = busfees_master.objects.filter(
        #     bus_id=OuterRef('bus_id')
        # ).values('destination')[:1]

        
        # bus_driver_subquery = bus_master.objects.filter(
        #     bus_route=OuterRef('route')
        # ).values('bus_driver')[:1]

        
        # driver_phone_subquery = bus_master.objects.filter(
        #     bus_route=OuterRef('route')
        # ).values('driver_phone')[:1]

        # bus_conductor_subquery = bus_master.objects.filter(
        #     bus_route=OuterRef('route')
        # ).values('bus_conductor')[:1]

        # conductor_phone_subquery = bus_master.objects.filter(
        #     bus_route=OuterRef('route')
        # ).values('conductor_phone')[:1]

        # bus_attendant_subquery = bus_master.objects.filter(
        #     bus_route=OuterRef('route')
        # ).values('bus_attendant')[:1]

        # attendant_phone_subquery = bus_master.objects.filter(
        #     bus_route=OuterRef('route')
        # ).values('attendant_phone')[:1]

        # queryset = queryset.annotate(
        #     class_no=Subquery(latest_student_class.values('class_no')[:1]),
        #     section=Subquery(latest_student_class.values('section')[:1]),
        #     route=Subquery(bus_route_subquery),
        #     destination=Subquery(bus_destination_subquery),
        #     bus_driver=Subquery(bus_driver_subquery),
        #     driver_phone=Subquery(driver_phone_subquery),
        #     bus_conductor=Subquery(bus_conductor_subquery),
        #     conductor_phone=Subquery(conductor_phone_subquery),
        #     bus_attendant=Subquery(bus_attendant_subquery),
        #     attendant_phone=Subquery(attendant_phone_subquery)
        # )

        # Filtering logic based on query parameters
        if bus_route:
            bus_ids = busfees_master.objects.filter(route=bus_route).values_list('bus_id', flat=True)
            queryset = queryset.filter(bus_id__in=bus_ids)
        if destination:
            bus_ids1 = busfees_master.objects.filter(destination=destination).values_list('bus_id', flat=True)
            # queryset = queryset.filter(destination=destination)
            queryset = queryset.filter(bus_id__in=bus_ids1)
        if class_no:
            student_ids = student_class.objects.filter(class_no=class_no).values_list('student_id', flat=True)
            queryset = queryset.filter(student_id__in=student_ids)
            # queryset = queryset.filter(class_no=class_no)

        return queryset, False


    # Override changelist_view to customize filters
    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}

        # Extract filter parameters from the request
        bus_route = request.GET.get('bus_route', '')
        destination = request.GET.get('destination', '')
        class_no = request.GET.get('class_no', '')

        # Add filter data to context for rendering the filters
        extra_context['bus_route_filter'] = range(1, 21)
        extra_context['class_filter'] = CLASS_CHOICES
        extra_context['destination_filter'] = busfees_master.objects.values_list('destination', flat=True).distinct()

        # Attach the filtered queryset to the changelist view
        response = super().changelist_view(request, extra_context=extra_context)
        
        return response


    # Customize the changelist template to include custom search fields
    change_list_template = 'admin/transport_changelist.html'

    # Custom URLs for AJAX
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('ajax/load-destinations/', self.admin_site.admin_view(self.load_destinations), name='ajax_load_destinations'),
        ]
        return custom_urls + urls

    # AJAX method to dynamically load destinations based on bus route
    def load_destinations(self, request):
        route = request.GET.get('route')
        destinations = list(busfees_master.objects.filter(route=route).values('destination').distinct())
        return JsonResponse(destinations, safe=False)

    # Custom JS for dynamic loading of destinations
    class Media:
        js = ('app/js/transport_filters.js',)

    # Define the remaining list_display methods (e.g., class_no, section)
    # def class_no(self, obj):
    #     return obj.class_no

    # def section(self, obj):
    #     return obj.section
    
    def class_no(self, obj):
        student_class_instance = student_class.objects.filter(student_id=obj.student_id).order_by('-started_on').first()
        return student_class_instance.class_no if student_class_instance else None
    # get_class_no.short_description = 'Class'

    def section(self, obj):
        student_class_instance = student_class.objects.filter(student_id=obj.student_id).order_by('-started_on').first()
        return student_class_instance.section if student_class_instance else None
    # get_section.short_description = 'Section'

    

    # def route(self, obj):
    #     return obj.route

    # def destination(self, obj):
    #     return obj.destination

    def route(self, obj):
        busfees_master_instance = busfees_master.objects.filter(bus_id=obj.bus_id).first()
        return busfees_master_instance.route if busfees_master_instance else None
        # return obj.route

    def destination(self, obj):
        busfees_master_instance = busfees_master.objects.filter(bus_id=obj.bus_id).first()
        return busfees_master_instance.destination if busfees_master_instance else None
        # return obj.destination

    # def bus_driver(self, obj):
    #     return obj.bus_driver
    
    # def driver_phone(self, obj):
    #     return obj.driver_phone

    def bus_driver(self, obj):
        busfees_master_instance = busfees_master.objects.filter(bus_id=obj.bus_id).first()
        bus_master_instance = bus_master.objects.filter(bus_route=busfees_master_instance.route).first() if busfees_master_instance else None
        return bus_master_instance.bus_driver if bus_master_instance else None
        # return obj.bus_driver
    
    def driver_phone(self, obj):
        busfees_master_instance = busfees_master.objects.filter(bus_id=obj.bus_id).first()
        bus_master_instance = bus_master.objects.filter(bus_route=busfees_master_instance.route).first() if busfees_master_instance else None
        return bus_master_instance.driver_phone if bus_master_instance else None

        # return obj.driver_phone

    # def bus_conductor(self, obj):
    #     return obj.bus_conductor

    # def conductor_phone(self, obj):
    #     return obj.conductor_phone

    # def bus_attendant(self, obj):
    #     return obj.bus_attendant

    # def attendant_phone(self, obj):
    #     return obj.attendant_phone

    def bus_conductor(self, obj):
        busfees_master_instance = busfees_master.objects.filter(bus_id=obj.bus_id).first()
        bus_master_instance = bus_master.objects.filter(bus_route=busfees_master_instance.route).first() if busfees_master_instance else None
        return bus_master_instance.bus_conductor if bus_master_instance else None
        # return obj.bus_conductor

    def conductor_phone(self, obj):
        busfees_master_instance = busfees_master.objects.filter(bus_id=obj.bus_id).first()
        bus_master_instance = bus_master.objects.filter(bus_route=busfees_master_instance.route).first() if busfees_master_instance else None
        return bus_master_instance.conductor_phone if bus_master_instance else None
        # return obj.conductor_phone

    def bus_attendant(self, obj):
        busfees_master_instance = busfees_master.objects.filter(bus_id=obj.bus_id).first()
        bus_master_instance = bus_master.objects.filter(bus_route=busfees_master_instance.route).first() if busfees_master_instance else None
        return bus_master_instance.bus_attendant if bus_master_instance else None
        # return obj.bus_attendant

    def attendant_phone(self, obj):
        busfees_master_instance = busfees_master.objects.filter(bus_id=obj.bus_id).first()
        bus_master_instance = bus_master.objects.filter(bus_route=busfees_master_instance.route).first() if busfees_master_instance else None
        return bus_master_instance.attendant_phone if bus_master_instance else None
        # return obj.attendant_phone

    class_no.short_description = 'Class No'
    section.short_description = 'Section'
    route.short_description = 'Route'
    destination.short_description = 'Destination'
    bus_driver.short_description = 'Bus Driver'
    driver_phone.short_description = 'Driver Phone'
    bus_conductor.short_description = 'Bus Conductor'
    conductor_phone.short_description = 'Conductor Phone'
    bus_attendant.short_description = 'Bus Attendant'
    attendant_phone.short_description = 'Attendant Phone'

admin.site.register(transport, TransportAdmin)

class PassedOutFilter(admin.SimpleListFilter):
    title = 'PassedOut'
    parameter_name = 'radioval'

    def lookups(self, request, model_admin):
        return []

class YearFilter(admin.SimpleListFilter):
    title = 'Year'
    parameter_name = 'year'

    def lookups(self, request, model_admin):
        return []
    

class TuitionFeesDefaulterResource(resources.ModelResource):

    class Meta:
        model = tuition_fees_defaulter
        fields = ('student_name', 'admission_no', 'class_no', 'section', 'tmpval')

    student_name = Field(attribute='student_name', column_name='Student Name')
    addmission_no = Field(attribute='addmission_no', column_name='Admission No')
    class_no = Field(attribute='class_no', column_name='Class')
    section = Field(attribute='section', column_name='Section')
    tmpval = Field(attribute='tmpval', column_name='Tution Fees unpaid for months')

    def dehydrate_class_no(self, obj):
        # Assuming 'bus_driver' is a related field on the model
        student_class_instance = student_class.objects.filter(student_id=obj.student_id.student_id).order_by('-started_on').first()
        return student_class_instance.class_no if student_class_instance else None

    
    def dehydrate_section(self, obj):
        student_class_instance = student_class.objects.filter(student_id=obj.student_id.student_id).order_by('-started_on').first()
        return student_class_instance.section if student_class_instance else None

    def dehydrate_tmpval(self, obj):
        # Get the year from the object
        year = int(obj.year)
        month_array = get_months_array(year)

        # Calculate the unpaid months
        unpaid_months = calculate_unpaid_months(obj.months_paid, month_array)

        # If unpaid_months is an empty string, return None to exclude it from display
        if not unpaid_months:
            return None  # or you can return '' if you prefer an empty string to be displayed
        
        return unpaid_months


    



class TuitionFeesDefaulterAdmin(ExportMixin,admin.ModelAdmin):
    resource_class = TuitionFeesDefaulterResource
    list_display = ('student_name', 'admission_no', 'class_no', 'section', 'tmpval')
    list_filter = (PassedOutFilter, ClassFilter, YearFilter)

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
    
    def get_year(self, request):
        current_month = date.today().month
        return date.today().year if current_month >= 4 else date.today().year - 1


    def changelist_view(self, request, extra_context=None):
        year_choices = [str(year) for year in range(2024, 2017, -1)]
        extra_context = extra_context or {}
        extra_context['class_choices'] = CLASS_CHOICES
        extra_context['year_choices'] = year_choices
        return super().changelist_view(request, extra_context=extra_context)

    change_list_template = 'admin/tuitionfeesdefaulter_change_list.html'

    def get_search_results(self, request, queryset, search_term):
        radioval = request.GET.get('radioval', None)
        year1 = request.GET.get('year', None)
        class_no = request.GET.get('class_no', None)

        year = int(year1) if year1 else self.get_year(request)
        month_array = get_months_array(year)
        months_str = ','.join(map(str, month_array))

        if not radioval and not year1 and not class_no:
            return queryset.none(), False

        total_fees_paid = ExpressionWrapper(
            Coalesce(F('tuition_fees_paid'), 0) +
            Coalesce(F('funds_fees_paid'), 0) +
            Coalesce(F('sports_fees_paid'), 0),
            output_field=DecimalField()
        )

        queryset = queryset.annotate(
            total_fees_paid=total_fees_paid
        ).filter(
            year=year,
            total_fees_paid__gt=0
        ).annotate(
            months_paid=RawSQL(
                """
                SELECT GROUP_CONCAT(DISTINCT TRIM(sf.fees_period_month) 
                ORDER BY sf.fees_period_month+0 SEPARATOR ', ')
                FROM student_fees AS sf
                WHERE sf.student_id = student_fees.student_id
                AND sf.year = %s
                """, (year,)
            ),
            student_name=F('student_id__student_name'),
            admission_no=F('student_id__addmission_no'),
            class_no=F('student_class'),
            section=F('student_section'),
            passedout_date=F('student_id__passedout_date'),
            tmpval=Value('', output_field=CharField())  # Placeholder for tmpval logic
        ).exclude(
            months_paid=months_str
        )

        if class_no:
            queryset = queryset.filter(class_no=class_no)

        queryset = self.filter_passed_out_students(queryset, radioval)
        for obj in queryset:
            obj.tmpval = calculate_unpaid_months(obj.months_paid, month_array)

        # Filter out objects where `tmpval` is empty
        filtered_queryset = [obj.student_fee_id for obj in queryset if obj.tmpval == '']

        queryset = queryset.exclude(student_fee_id__in=filtered_queryset)

        return queryset, False

    # def get_months_array(self, year):
    #     start_date = date(year, 4, 1)
    #     end_date = date(year + 1, 3, 31)
    #     current_date = date.today()

    #     months = []
    #     time = start_date
    #     if current_date < end_date:
    #         end_date = current_date

    #     while time <= end_date:
    #         months.append(time.month)
    #         next_month = (time.month % 12) + 1
    #         next_year = time.year + (1 if next_month == 1 else 0)
    #         time = date(next_year, next_month, 1)

    #     return months

    # def calculate_unpaid_months(self, paid_months, months_array):
    #     print('paid_months in calculate_unpaid_months', paid_months)
    #     print('months_array in calculate_unpaid_months', months_array)
    #     if not paid_months:
    #         return ','.join(map(str, months_array))  # Return all months if no months are paid

    #     paid_months_list = list(map(int, paid_months.split(',')))
    #     unpaid_months = set(months_array) - set(paid_months_list)
    #     return ','.join(map(str, sorted(unpaid_months)))

    def filter_passed_out_students(self, queryset, radioval):
        current_date = date.today()
        if radioval != 'withpassedout':
            queryset = queryset.exclude(passedout_date__lt=current_date)
        return queryset
    
    
#     # Display functions for fields
    def student_name(self, obj):
        return obj.student_name

    def admission_no(self, obj):
        return obj.admission_no

    def class_no(self, obj):
        return obj.class_no

    def section(self, obj):
        return obj.section

    def tmpval(self, obj):
        # Get the year from the object
        year = int(obj.year)
        month_array = get_months_array(year)

        # Calculate the unpaid months
        unpaid_months = calculate_unpaid_months(obj.months_paid, month_array)

        # If unpaid_months is an empty string, return None to exclude it from display
        if not unpaid_months:
            return None  # or you can return '' if you prefer an empty string to be displayed
        
        obj.tmpval = unpaid_months 
        return unpaid_months
    tmpval.short_description = 'Tuition Fees Unpaid for Months'


admin.site.register(tuition_fees_defaulter, TuitionFeesDefaulterAdmin)

# Custom Filter for Class No
class ClassNoFilter1(admin.SimpleListFilter):
    title = 'Class'
    parameter_name = 'class_no'

    def lookups(self, request, model_admin):
        # Define class choices as per your requirements
        return CLASS_CHOICES

    def queryset(self, request, queryset):
        cls = self.value()
        if cls:
            subquery = student_class.objects.filter(
                student_id=OuterRef('student_id'),
                class_no=cls
            ).order_by('-student_class_id').values('student_class_id')[:1]
            return queryset.filter(
                student_id__in=Subquery(subquery)
            )
        return queryset


    
# Custom Filter for Admission Date From
class DateFromFilter(admin.SimpleListFilter):
    title = 'Admission Date From'
    parameter_name = 'date_from'

    def lookups(self, request, model_admin):
        # return ()
        return []

    # def queryset(self, request, queryset):
    #     date_from = request.GET.get('date_from')
    #     if date_from:
    #         return queryset.filter(admission_date__gte=date_from)
    #     return queryset

    # def choices(self, changelist):
    #     # Override to remove the 'All' option
    #     return []

# Custom Filter for Admission Date To
class DateToFilter(admin.SimpleListFilter):
    title = 'Admission Date To'
    parameter_name = 'date_to'

    def lookups(self, request, model_admin):
        # return ()
        return []

    # def queryset(self, request, queryset):
    #     date_to = request.GET.get('date_to')
    #     if date_to:
    #         return queryset.filter(admission_date__lte=date_to)
    #     return queryset

    # def choices(self, changelist):
    #     # Override to remove the 'All' option
    #   
    # 

# class AdmissionReportResource(resources.ModelResource):

#     class Meta:
#         model = admission_report
#         fields = ('addmission_no', 'admission_date', 'student_name', 'birth_date',
#         'class_no', 'section', 'father_name', 'mother_name', 'address')

#     student_name = Field(attribute='student_name', column_name='Student Name')
#     addmission_no = Field(attribute='addmission_no', column_name='Admission No')
#     admission_date = Field(attribute='admission_date', column_name='Admission Date')
#     class_no = Field(attribute='class_no', column_name='Class')
#     section = Field(attribute='section', column_name='Section')

#     father_name = Field(attribute='father_name', column_name='Father Name')
#     mother_name = Field(attribute='phone_no', column_name='Mother Name')
#     address = Field(attribute='address', column_name='Address')
#     birth_date = Field(attribute='birth_date', column_name='Birth Date')


#     def dehydrate_class_no(self, obj):
#         # Assuming 'bus_driver' is a related field on the model
#         student_class_instance = student_class.objects.filter(student_id=obj.student_id).order_by('-started_on').first()
#         return student_class_instance.class_no if student_class_instance else None
#         # return obj.class_no if obj.class_no else ''

    
#     def dehydrate_section(self, obj):
#         student_class_instance = student_class.objects.filter(student_id=obj.student_id).order_by('-started_on').first()
#         return student_class_instance.section if student_class_instance else None
    
#     # def dehydrate_class_no(self, obj):
#     #     # Subquery to fetch class_no from student_class without foreign key
#     #     # subquery = student_class.objects.filter(
#     #     #     student_id=obj.student_id
#     #     # ).order_by('-student_class_id').values('class_no')[:1]
#     #     # result = subquery.first()
#     #     # return result.get('class_no') if result else None
#     #     search_class_no = self._request.GET.get('class_no', None)

#     #     # Filter by class_no and/or section if available
#     #     if search_class_no:
#     #         student_class_instance = student_class.objects.filter(student_id=obj.student_id, class_no=search_class_no).order_by('-started_on').first()
#     #     else:
#     #         student_class_instance = student_class.objects.filter(student_id=obj.student_id).order_by('-started_on').first()

#     #     return student_class_instance.class_no if student_class_instance else None

#     # def dehydrate_section(self, obj):
#     #     # Subquery to fetch section from student_class without foreign key
#     #     # subquery = student_class.objects.filter(
#     #     #     student_id=obj.student_id
#     #     # ).order_by('-student_class_id').values('section')[:1]
#     #     # result = subquery.first()
#     #     # return result.get('section') if result else None
#     #     search_class_no = self._request.GET.get('class_no', None)

#     #     # Filter by class_no and/or section if available
#     #     if search_class_no:
#     #         student_class_instance = student_class.objects.filter(student_id=obj.student_id, class_no=search_class_no).order_by('-started_on').first()
#     #     else:
#     #         student_class_instance = student_class.objects.filter(student_id=obj.student_id).order_by('-started_on').first()

#     #     return student_class_instance.section if student_class_instance else None

#     # # get_section.short_description = 'Section'


  
#         # return obj.bus_driver
    
# class AdmissionReportResource(resources.ModelResource):
#     def __init__(self, request=None):
#         super().__init__()
#         self._request = request

#     class Meta:
#         model = admission_report
#         fields = ('addmission_no', 'admission_date', 'student_name', 'birth_date',
#                   'class_no', 'section', 'father_name', 'mother_name', 'address')

#     # Define fields
#     student_name = Field(attribute='student_name', column_name='Student Name')
#     addmission_no = Field(attribute='addmission_no', column_name='Admission No')
#     admission_date = Field(attribute='admission_date', column_name='Admission Date')
#     class_no = Field(attribute='class_no', column_name='Class')
#     section = Field(attribute='section', column_name='Section')
#     father_name = Field(attribute='father_name', column_name='Father Name')
#     mother_name = Field(attribute='phone_no', column_name='Mother Name')
#     address = Field(attribute='address', column_name='Address')
#     birth_date = Field(attribute='birth_date', column_name='Birth Date')

#     # Custom dehydrate methods
#     def dehydrate_class_no(self, obj):
#         search_class_no = self._request.GET.get('class_no', None) if self._request else None

#         if search_class_no:
#             student_class_instance = student_class.objects.filter(
#                 student_id=obj.student_id, class_no=search_class_no).order_by('-started_on').first()
#         else:
#             student_class_instance = student_class.objects.filter(
#                 student_id=obj.student_id).order_by('-started_on').first()

#         return student_class_instance.class_no if student_class_instance else None

#     def dehydrate_section(self, obj):
#         search_class_no = self._request.GET.get('class_no', None) if self._request else None

#         if search_class_no:
#             student_class_instance = student_class.objects.filter(
#                 student_id=obj.student_id, class_no=search_class_no).order_by('-started_on').first()
#         else:
#             student_class_instance = student_class.objects.filter(
#                 student_id=obj.student_id).order_by('-started_on').first()

#         return student_class_instance.section if student_class_instance else None

# class AdmissionReportResource(resources.ModelResource):
#     def __init__(self, request=None):
#         super().__init__()
#         self._request = request  # Store the request passed from the Admin class

#     class Meta:
#         model = admission_report
#         fields = ('addmission_no', 'admission_date', 'student_name', 'birth_date',
#                   'class_no', 'section', 'father_name', 'mother_name', 'address')

#     # Define fields
#     student_name = Field(attribute='student_name', column_name='Student Name')
#     addmission_no = Field(attribute='addmission_no', column_name='Admission No')
#     admission_date = Field(attribute='admission_date', column_name='Admission Date')
#     class_no = Field(attribute='class_no', column_name='Class')
#     section = Field(attribute='section', column_name='Section')
#     father_name = Field(attribute='father_name', column_name='Father Name')
#     mother_name = Field(attribute='phone_no', column_name='Mother Name')
#     address = Field(attribute='address', column_name='Address')
#     birth_date = Field(attribute='birth_date', column_name='Birth Date')

#     # Custom dehydrate methods
#     def dehydrate_class_no(self, obj):
#         search_class_no = self._request.GET.get('class_no', None) if self._request else None

#         if search_class_no:
#             student_class_instance = student_class.objects.filter(
#                 student_id=obj.student_id, class_no=search_class_no).order_by('-started_on').first()
#         else:
#             student_class_instance = student_class.objects.filter(
#                 student_id=obj.student_id).order_by('-started_on').first()

#         return student_class_instance.class_no if student_class_instance else None

#     def dehydrate_section(self, obj):
#         search_class_no = self._request.GET.get('class_no', None) if self._request else None

#         if search_class_no:
#             student_class_instance = student_class.objects.filter(
#                 student_id=obj.student_id, class_no=search_class_no).order_by('-started_on').first()
#         else:
#             student_class_instance = student_class.objects.filter(
#                 student_id=obj.student_id).order_by('-started_on').first()

#         return student_class_instance.section if student_class_instance else None

# class AdmissionReportResource(resources.ModelResource):
#     def __init__(self, request=None, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self._request = request  # Store the request passed from the Admin class
#         # Handle other keyword arguments like 'encoding'
#         self.extra_args = kwargs

#     class Meta:
#         model = admission_report
#         fields = ('addmission_no', 'admission_date', 'student_name', 'birth_date',
#                   'class_no', 'section', 'father_name', 'mother_name', 'address')

#     # Define fields
#     student_name = Field(attribute='student_name', column_name='Student Name')
#     addmission_no = Field(attribute='addmission_no', column_name='Admission No')
#     admission_date = Field(attribute='admission_date', column_name='Admission Date')
#     class_no = Field(attribute='class_no', column_name='Class')
#     section = Field(attribute='section', column_name='Section')
#     father_name = Field(attribute='father_name', column_name='Father Name')
#     mother_name = Field(attribute='phone_no', column_name='Mother Name')
#     address = Field(attribute='address', column_name='Address')
#     birth_date = Field(attribute='birth_date', column_name='Birth Date')

#     # Custom dehydrate methods
#     def dehydrate_class_no(self, obj):
#         search_class_no = self._request.GET.get('class_no', None) if self._request else None
#         print('search_class_no',search_class_no)
#         if search_class_no:
#             student_class_instance = student_class.objects.filter(
#                 student_id=obj.student_id, class_no=search_class_no).order_by('-started_on').first()
#         else:
#             student_class_instance = student_class.objects.filter(
#                 student_id=obj.student_id).order_by('-started_on').first()

#         return student_class_instance.class_no if student_class_instance else None

#     def dehydrate_section(self, obj):
#         search_class_no = self._request.GET.get('class_no', None) if self._request else None

#         if search_class_no:
#             student_class_instance = student_class.objects.filter(
#                 student_id=obj.student_id, class_no=search_class_no).order_by('-started_on').first()
#         else:
#             student_class_instance = student_class.objects.filter(
#                 student_id=obj.student_id).order_by('-started_on').first()

#         return student_class_instance.section if student_class_instance else None

class AdmissionReportResource(resources.ModelResource):
    # def __init__(self, request=None, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self._request = request  # Store the request passed from the Admin class
    #     # Handle other keyword arguments like 'encoding'
    #     # self.extra_args = kwargs

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._request = None  # Default to None; it will be set later if passed
    

    class Meta:
        model = admission_report
        fields = ('addmission_no', 'admission_date', 'student_name', 'birth_date',
                  'class_no', 'section', 'father_name', 'mother_name', 'address')

    # Define fields
    student_name = Field(attribute='student_name', column_name='Student Name')
    addmission_no = Field(attribute='addmission_no', column_name='Admission No')
    admission_date = Field(attribute='admission_date', column_name='Admission Date')
    class_no = Field(attribute='class_no', column_name='Class')
    section = Field(attribute='section', column_name='Section')
    father_name = Field(attribute='father_name', column_name='Father Name')
    mother_name = Field(attribute='phone_no', column_name='Mother Name')
    address = Field(attribute='address', column_name='Address')
    birth_date = Field(attribute='birth_date', column_name='Birth Date')

    # Custom dehydrate methods
    # def dehydrate_class_no(self, obj):
    #     search_class_no = self._request.GET.get('class_no', None) if self._request else None
    #     print('search_class_no',search_class_no)
    #     if search_class_no:
    #         student_class_instance = student_class.objects.filter(
    #             student_id=obj.student_id, class_no=search_class_no).order_by('-started_on').first()
    #     else:
    #         student_class_instance = student_class.objects.filter(
    #             student_id=obj.student_id).order_by('-started_on').first()

    #     return student_class_instance.class_no if student_class_instance else None

    # def dehydrate_section(self, obj):
    #     search_class_no = self._request.GET.get('class_no', None) if self._request else None

    #     if search_class_no:
    #         student_class_instance = student_class.objects.filter(
    #             student_id=obj.student_id, class_no=search_class_no).order_by('-started_on').first()
    #     else:
    #         student_class_instance = student_class.objects.filter(
    #             student_id=obj.student_id).order_by('-started_on').first()

    #     return student_class_instance.section if student_class_instance else None


    def dehydrate_class_no(self, obj):
        # Check if request is available
        if self._request:
            search_class_no = self._request.GET.get('class_no', None)
        else:
            search_class_no = None

        # Filter by class_no if available
        if search_class_no:
            student_class_instance = student_class.objects.filter(
                student_id=obj.student_id, class_no=search_class_no).order_by('-started_on').first()
        else:
            student_class_instance = student_class.objects.filter(
                student_id=obj.student_id).order_by('-started_on').first()

        return student_class_instance.class_no if student_class_instance else None

    def dehydrate_section(self, obj):
        # Check if request is available
        if self._request:
            search_class_no = self._request.GET.get('class_no', None)
        else:
            search_class_no = None

        # Filter by class_no and return section if available
        if search_class_no:
            student_class_instance = student_class.objects.filter(
                student_id=obj.student_id, class_no=search_class_no).order_by('-started_on').first()
        else:
            student_class_instance = student_class.objects.filter(
                student_id=obj.student_id).order_by('-started_on').first()

        return student_class_instance.section if student_class_instance else None

class AdmissionReportAdmin(ExportMixin, admin.ModelAdmin):

    resource_class = AdmissionReportResource
    list_display = (
        'addmission_no', 'formatted_admission_date', 'student_name', 'birth_date',
        'class_no', 'section', 'father_name', 'mother_name', 'address'
    )
    # search_fields = ('student_name', 'admission_no')
    list_filter = (ClassFilter, DateFromFilter, DateToFilter)

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
    
    

    def changelist_view(self, request, extra_context=None):
        """
        Handle the custom filters and pass them to the context for rendering the change list view.
        """
        extra_context = extra_context or {}
        # Store the request object in the instance
        
        # Get the filter values from GET parameters
        class_no = request.GET.get('class_no', '')
        date_from = request.GET.get('date_from', '')
        date_to = request.GET.get('date_to', timezone.now().strftime('%Y-%m-%d'))

        # Pass filter values to the template to retain them
        extra_context['class_no'] = class_no
        extra_context['date_from'] = date_from
        extra_context['date_to'] = date_to

        # Retrieve distinct class numbers from student_class to populate the filter options
        distinct_classes = student_class.objects.values_list('class_no', flat=True).distinct()
        # extra_context['class_choices'] = [(cls, cls) for cls in distinct_classes]
        extra_context['class_choices'] = CLASS_CHOICES
        self._request = request
        # Call the default changelist_view with the extra context
        return super().changelist_view(request, extra_context=extra_context)
    
    change_list_template = 'admin/admissionreport_change_list.html'

    # def get_export_resource_class(self):
    #     """
    #     Pass the stored request object to the ModelResource class constructor.
    #     """
    #     # Return an instance of the resource class with request passed
    #     return self.resource_class

    # def get_export_resource_instance(self):
    #     """
    #     Pass the stored request object when instantiating the resource class.
    #     """
    #     # Debugging: Log the request being passed
    #     print("Passing request to resource:", self._request.GET)  
    #     return self.resource_class(request=self._request)  
    def get_export_resource_instance(self):
        """
        Pass the stored request object when instantiating the resource class.
        """
        resource = self.resource_class()  # Create an instance of the resource class
        # Inject the request into the resource class
        if hasattr(self, '_request'):
            resource._request = self._request  # Set the _request attribute
        return resource
    # def get_search_results(self, request, queryset, search_term):
    #     """
    #     Override get_search_results to filter by class_no and date range.
    #     """
    #     queryset, use_distinct = super().get_search_results(request, queryset, search_term)

    #     # Get custom filter parameters from the request
    #     class_no = request.GET.get('class_no', '')
    #     date_from = request.GET.get('date_from', '')
    #     date_to = request.GET.get('date_to', timezone.now().strftime('%Y-%m-%d'))

    #     # Apply class_no filter if provided
    #     if class_no:
    #         subquery = student_class.objects.filter(
    #             student_id=OuterRef('student_id'),
    #             class_no=class_no
    #         ).order_by('-student_class_id').values('student_class_id')[:1]
    #         queryset = queryset.filter(student_id__in=Subquery(subquery))

    #     # Apply date filters if provided
    #     if date_from:
    #         queryset = queryset.filter(admission_date__gte=date_from)
    #     if date_to:
    #         queryset = queryset.filter(admission_date__lte=date_to)

    #     return queryset, use_distinct


    # def get_search_results(self, request, queryset, search_term):
    #     """
    #     Override get_search_results to filter by class_no and date range.
    #     """
    #     queryset, use_distinct = super().get_search_results(request, queryset, search_term)

    #     # Get custom filter parameters from the request
    #     class_no = request.GET.get('class_no', '')
    #     date_from = request.GET.get('date_from', '')
    #     date_to = request.GET.get('date_to', timezone.now().strftime('%Y-%m-%d'))

    #     # Apply class_no filter if provided using Exists() instead of Subquery
    #     if class_no:
    #         student_class_qs = student_class.objects.filter(
    #             student_id=OuterRef('student_id'),
    #             class_no=class_no
    #         ).order_by('-student_class_id')

    #         queryset = queryset.annotate(class_exists=Exists(student_class_qs)).filter(class_exists=True)

    #     # Apply date filters if provided
    #     if date_from:
    #         queryset = queryset.filter(admission_date__gte=date_from)
    #     if date_to:
    #         queryset = queryset.filter(admission_date__lte=date_to)

    #     return queryset, use_distinct


    def get_search_results(self, request, queryset, search_term):
        """
        Override get_search_results to filter by class_no and date range.
        """
        queryset, use_distinct = super().get_search_results(request, queryset, search_term)

        # Get custom filter parameters from the request
        class_no = request.GET.get('class_no', '')
        date_from = request.GET.get('date_from', '')
        date_to = request.GET.get('date_to', timezone.now().strftime('%Y-%m-%d'))

        if not class_no and not date_from:
            return queryset.none(), use_distinct

        # Apply strict class_no filter if provided using Exists() with exact class_no match
        if class_no:
            student_class_qs = student_class.objects.filter(
                student_id=OuterRef('student_id'),
                class_no=class_no
            ).order_by('-student_class_id')  # Ensure you're checking the latest class

            queryset = queryset.annotate(class_exists=Exists(student_class_qs)).filter(class_exists=True)

        # Apply date filters if provided
        if date_from:
            queryset = queryset.filter(admission_date__gte=date_from)
        if date_to:
            queryset = queryset.filter(admission_date__lte=date_to)

        return queryset, use_distinct

    def formatted_admission_date(self, obj):
        # Format the admission date in dd-mm-yyyy
        return obj.admission_date.strftime('%d-%m-%Y')
    formatted_admission_date.short_description = 'Admission Date'

    def class_no(self, obj):
        # Subquery to fetch class_no from student_class without foreign key
        # subquery = student_class.objects.filter(
        #     student_id=obj.student_id
        # ).order_by('-student_class_id').values('class_no')[:1]
        # result = subquery.first()
        # return result.get('class_no') if result else None
        search_class_no = self._request.GET.get('class_no', None)

        # Filter by class_no and/or section if available
        if search_class_no:
            student_class_instance = student_class.objects.filter(student_id=obj.student_id, class_no=search_class_no).order_by('-started_on').first()
        else:
            student_class_instance = student_class.objects.filter(student_id=obj.student_id).order_by('-started_on').first()

        return student_class_instance.class_no if student_class_instance else None

    def section(self, obj):
        # Subquery to fetch section from student_class without foreign key
        # subquery = student_class.objects.filter(
        #     student_id=obj.student_id
        # ).order_by('-student_class_id').values('section')[:1]
        # result = subquery.first()
        # return result.get('section') if result else None
        search_class_no = self._request.GET.get('class_no', None)

        # Filter by class_no and/or section if available
        if search_class_no:
            student_class_instance = student_class.objects.filter(student_id=obj.student_id, class_no=search_class_no).order_by('-started_on').first()
        else:
            student_class_instance = student_class.objects.filter(student_id=obj.student_id).order_by('-started_on').first()

        return student_class_instance.section if student_class_instance else None

# Register the AdmissionReport proxy model with the custom admin
admin.site.register(admission_report, AdmissionReportAdmin)

# admin.site.register(tuition_fees_defaulter, TuitionFeesDefaulterAdmin)



class CollectionReportForm(forms.Form):
    FEE_TYPE_CHOICES = [
        ('advancedfees', 'Advanced fees'),
        ('totalfees', 'Total fees'),
        ('customfees', 'LastDay fees'),
    ]

    PAYMENT_TYPE_CHOICES = [
        ('', 'Payment'),
        ('Online', 'Online'),
        ('Cash', 'Cash'),
        ('Cheque', 'Cheque'),
    ]

    DEVICE_TYPE_CHOICES = [
        ('', 'Device'),
        ('WEB', 'WEB'),
        ('MOBILE', 'MOBILE'),
    ]

    feestype = forms.ChoiceField(
        choices=FEE_TYPE_CHOICES, 
        widget=forms.RadioSelect,
        label='Fee Type'
    )
    
    paymentType = forms.ChoiceField(
        choices=PAYMENT_TYPE_CHOICES,
        required=False,
        label='Payment Type',
        widget=forms.Select(attrs={'id': 'paymentType'})
    )
    
    deviceType = forms.ChoiceField(
        choices=DEVICE_TYPE_CHOICES,
        required=False,
        label='Device Type',
        widget=forms.Select(attrs={'id': 'deviceType'})
    )
    
    date_from = forms.DateField(
        required=False,
        label='Date From',
        widget=forms.DateInput(attrs={'id': 'id_date_from', 'type': 'date'})
    )
    
    date_to = forms.DateField(
        required=False,
        label='Date To',
        widget=forms.DateInput(attrs={'id': 'id_date_to', 'type': 'date'})
    )

    filter_button = forms.CharField(
        widget=forms.TextInput(attrs={'type': 'submit', 'value': 'Filter'}),
        label='',
        required=False
    )

class CollectionReportAdmin(admin.ModelAdmin):
   
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('collection_report/', self.admin_site.admin_view(self.changelist_view)),
           
        ]
        return custom_urls + urls

    # def changelist_view(self, request, extra_context=None):
    #     extra_context = extra_context or {}
    #     form = CollectionReportForm(request.POST or None)  # Initialize form with POST data

    #     results = []
    #     if request.method == 'POST' and form.is_valid():
    #         # selected_class = form.cleaned_data.get('student_class')
    #         # selected_year = form.cleaned_data.get('year')
    #         feestype = form.cleaned_data.get['feestype']
    #         payment_type = form.cleaned_data.get['paymentType']
    #         device_type = form.cleaned_data.get['deviceType']
    #         date_from = form.cleaned_data.get['date_from']
    #         date_to = form.cleaned_data.get['date_to']


    #     extra_context['form'] = form  # Add the form to extra_context
    #     extra_context['results'] = results  # Pass results to the template

    #     return super().changelist_view(request, extra_context=extra_context)

    def changelist_view(self, request, extra_context=None):
        # Assuming defaulters_list is populated with your required data
        collection_list = []
        extra_context = extra_context or {}
        form = CollectionReportForm(request.POST or None)  # Initialize form with POST data

        results = []
        total_fees = {
            "amount": 0,
            "annual_fees": 0,
            "tuition_fees": 0,
            "fund_fees": 0,
            "sports_fees": 0,
            "activity_fees": 0,
            "admission_fees": 0,
            "security_fees": 0,
            "late_fees": 0,
            "dayboarding_fees": 0,
            "bus_fees": 0,
            "total_fees": 0,
            "concession": 0
        }

        if request.method == 'POST' and form.is_valid():
            # Access cleaned_data properly
            feestype = form.cleaned_data.get('feestype')
            payment_type = form.cleaned_data.get('paymentType')
            device_type = form.cleaned_data.get('deviceType')
            date_from = form.cleaned_data.get('date_from')
            date_to = form.cleaned_data.get('date_to')

            # Set default values for dates
            current_year = date.today().year
            session_start = f"{current_year}-04-01"
            year = current_year - 1
            toyear = year + 1
            from_date = f"{year}-04-01"
            to_date = f"{toyear}-03-31"

            q = ""
            params = []

            # Construct SQL query based on fee type
            if feestype == 'advancedfees':
                q = """
                    SELECT 
                        sf.*, 
                        sf.student_class as class_no, 
                        sf.student_section as section, 
                        sm.addmission_no, 
                        sm.student_name, 
                        con.concession_type 
                    FROM 
                        student_fees sf
                    INNER JOIN 
                        student_master sm ON sm.student_id = sf.student_id 
                    LEFT JOIN 
                        concession_master con ON con.concession_id = sf.concession_type_id 
                    WHERE 
                        sf.year = %s 
                        AND sf.date_payment BETWEEN %s AND %s 
                """
                params = [current_year, from_date, to_date]

                if payment_type:
                    q += " AND sf.payment_mode = %s"
                    params.append(payment_type)

                if device_type:
                    q += " AND sf.request_source = %s"
                    params.append(device_type)

                q += " ORDER BY sf.date_payment DESC, sm.addmission_no;"

            elif feestype == 'customfees':
                q = """
                    SELECT sf.*, cls.*, sm.addmission_no, sm.student_name, con.concession_type 
                    FROM student_fees sf 
                    LEFT JOIN student_master sm ON sm.student_id = sf.student_id 
                    LEFT JOIN concession_master con ON con.concession_id = sf.concession_type_id 
                    LEFT OUTER JOIN (
                        SELECT * FROM student_classes WHERE (student_id, started_on) IN (
                            SELECT student_id, MAX(started_on) FROM student_classes GROUP BY student_id
                        )
                    ) AS cls ON sm.student_id = cls.student_id 
                """

                if date_from and date_to:
                    q += " WHERE sf.date_payment BETWEEN %s AND %s"
                    params += [date_from, date_to]
                else:
                    yesterday = date.today() - timedelta(days=1)
                    q += " WHERE (sf.added_at >= %s AND sf.added_at < %s)"
                    params += [yesterday, date.today()]

                if device_type:
                    q += " AND sf.request_source = %s"
                    params.append(device_type)

                if payment_type:
                    q += " AND sf.payment_mode = %s"
                    params.append(payment_type)

                q += " ORDER BY sf.added_at DESC, sm.addmission_no"

            else:
                q = """
                    SELECT a.*, cls.*, sm.addmission_no, sm.student_name, con.concession_type 
                    FROM student_fees a 
                    LEFT JOIN student_master sm ON sm.student_id = a.student_id 
                    LEFT JOIN concession_master con ON con.concession_id = a.concession_type_id 
                    LEFT OUTER JOIN student_classes AS cls ON sm.student_id = cls.student_id 
                    WHERE a.date_payment BETWEEN %s AND %s 
                    AND cls.student_class_id = (SELECT MAX(student_class_id) 
                                                FROM student_classes 
                                                WHERE student_id = sm.student_id)
                """
                params = [date_from, date_to]

                if payment_type:
                    q += " AND a.payment_mode = %s"
                    params.append(payment_type)

                if device_type:
                    q += " AND a.request_source = %s"
                    params.append(device_type)

                q += " ORDER BY a.date_payment DESC, sm.addmission_no"

            # Execute the query
            with connection.cursor() as cursor:
                cursor.execute(q, params)
                fee_records = cursor.fetchall()
                print(f"fee_records==={fee_records}")

            # Process fee records and calculate totals
            for entry in fee_records:

                # Create a dictionary for each record
                # Check the length of the tuple to avoid out of range errors
                if len(entry) >= 49:  # Ensure there are at least 49 elements in the tuple
                    collection_record = {
                        'addmission_no': entry[0],           # Admission no
                        'student_name': entry[48],           # Student Name
                        'class_no': entry[2],                # Class
                        'section': entry[3],                 # Section
                        'fees_for_months': entry[4],         # Fees for months
                        'fees_period_month': entry[5],       # Fees paid for months
                        'annual_fees_paid': entry[8],        # Annual fees
                        'tuition_fees_paid': entry[9],       # Tuition fees
                        'concession_applied': entry[10],     # Concession applied
                        'net_tuition_fees': entry[11],       # Net tuition fees
                        'funds_fees_paid': entry[12],        # Fund fees
                        'sports_fees_paid': entry[13],       # Sports fees
                        'activity_fees': entry[14],          # Activity fees
                        'admission_fees_paid': entry[15],    # Admission fees
                        'security_paid': entry[16],          # Security fees
                        'late_fees_paid': entry[17],         # Late fees
                        'miscellaneous_fees': entry[18],     # Miscellaneous fees
                        'bus_fees_paid': entry[19],          # Bus fees
                        'date_payment': entry[20],           # Payment date
                        'payment_mode': entry[21],           # Payment mode
                        'cheq_no': entry[22],                # Cheque no.
                        'bank_name': entry[23],              # Bank name
                        'concession_type': entry[24],        # Concession type
                        'Total_amount': entry[25],           # Total amount
                        'amount_paid': entry[26],            # Amount paid
                        'cheque_status': entry[28],          # Cheque status
                        'realized_date': entry[29],          # Realized date
                        'remarks': entry[31],                # Remarks
                        'request_source': entry[37],         # User Agent (Request source)
                    }
                    collection_list.append(collection_record)

                # Save results to session for later export
                request.session['collection_list'] = collection_list

                results = collection_list

                # results.append(fee)  # Collect each fee record to be displayed in the template

                # total_fees['amount'] += fee['amount_paid']
                # total_fees['annual_fees'] += fee['annual_fees_paid']
                # total_fees['tuition_fees'] += fee['tuition_fees_paid']
                # total_fees['fund_fees'] += fee['funds_fees_paid']
                # total_fees['sports_fees'] += fee['sports_fees_paid']
                # total_fees['activity_fees'] += fee['activity_fees']
                # total_fees['admission_fees'] += fee['admission_fees_paid']
                # total_fees['security_fees'] += fee['security_paid']
                # total_fees['late_fees'] += fee['late_fees_paid']
                # total_fees['dayboarding_fees'] += fee['dayboarding_fees_paid']
                # total_fees['bus_fees'] += fee['bus_fees_paid']
                # total_fees['total_fees'] += fee['Total_amount']
                # total_fees['concession'] += fee['concession_applied'] if isinstance(fee['concession_applied'], (int, float)) else 0

        # Add form, results, and totals to extra_context
        extra_context['form'] = form
        extra_context['results'] = results  # Contains the processed fee records
        extra_context['total_fees'] = total_fees  # Contains the summary of fees

        return super().changelist_view(request, extra_context=extra_context)

    change_list_template = "admin/collection_report/change_list.html"  # Specify your custom template

admin.site.register(collection_report, CollectionReportAdmin)

class DefaultersReportForm(forms.Form):
    CLASS_CHOICES = [
        ('', 'Select Class'),
        ('nursery', 'Nursery'),
        ('LKG', 'LKG'),
        ('UKG', 'UKG'),
        ('1', '1st Grade'),
        ('2', '2nd Grade'),
        # Add other classes as needed
    ]

    current_year = datetime.now().year
    YEAR_CHOICES = [(str(year), str(year)) for year in range(current_year, current_year - 6, -1)]

    student_class = forms.ChoiceField(choices=CLASS_CHOICES, required=True, label="Class", widget=forms.Select(attrs={'id': 'id_student_class'}))
    year = forms.ChoiceField(choices=YEAR_CHOICES, required=True, label="Year",widget=forms.Select(attrs={'id': 'id_year'}))

    # Search button with jQuery to trigger a student search
    search_button = forms.CharField(
        widget=forms.TextInput(attrs={'type': 'submit', 'value': 'Search'}),
        label='',
        required=False
    )


class ActivityFeesDefaulterAdmin(admin.ModelAdmin):

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('activity-fees-defaulters/', self.admin_site.admin_view(self.changelist_view)),
            path('activity-fees-defaulters/export/', self.admin_site.admin_view(self.export_defaulters_to_excel), name="export_defaulters_csv")
        ]
        return custom_urls + urls

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def get_months_array(self, year):
        # Convert year to an integer for arithmetic operations
        year = int(year)

        # Define the start and end of the financial year
        datefrom = f"{year}0401"  # First date of the financial year (April 1st)
        dateto = f"{year + 1}0331"  # Last date of the financial year (March 31st of the next year)

        # Convert to actual date format (Y-m-d)
        datefrom1 = datetime.strptime(datefrom, "%Y%m%d").date()
        dateto1 = datetime.strptime(dateto, "%Y%m%d").date()

        # Get the current date
        currentdate = datetime.now().date()

        # If the financial year is not over yet, set `dateto1` to today
        if currentdate < dateto1:
            dateto1 = currentdate

        # Initialize the month array
        month_array = []
        
        # Create a timestamp starting from `datefrom1`
        time = datefrom1
        to_month = dateto1.month

        # Iterate for a maximum of 12 months
        for i in range(12):
            # Get the current month
            cur_month = time.month
            
            # Stop if the last month (current month) is reached
            if cur_month == to_month:
                break

            # Add the month number to the array, stripping leading zeroes
            month_array.append(str(cur_month).lstrip('0'))
            
            # Move to the next month
            time = time + timedelta(days=31)
            time = time.replace(day=1)  # Ensure to set the day to the 1st of the next month

        # If all months have passed, return a full array from 1 to 12
        if not month_array:
            month_array = [str(i) for i in range(1, 13)]

        # Sort the month array to ensure the months are in ascending order
        month_array.sort(key=int)

        return month_array


    def export_defaulters_to_excel(self, request):
        # Retrieve data to export, typically from a session or request
        defaulters_list = request.session.get('defaulters_list', [])
        
        if not defaulters_list:
            # Handle the case where there is no data to export
            messages.error(request, "No data available to export.")
            return redirect('admin:activity_fees_defaulter_changelist')

        # Define the column headers
        headers = ['Admission No', 'Student Name', 'Class', 'Section', 'Unpaid Months']

        # Convert defaulters_list to DataFrame for export
        df = pd.DataFrame(defaulters_list)

        # Rename the columns to match the desired headers
        df.columns = headers

        # Create a BytesIO stream to hold the Excel data
        excel_file = BytesIO()
        with pd.ExcelWriter(excel_file, engine='openpyxl') as writer:
            df.to_excel(writer, index=False, sheet_name='Defaulters')

        # Rewind the buffer
        excel_file.seek(0)

        # Create the HTTP response to download the file
        response = HttpResponse(
            excel_file.read(),
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        response['Content-Disposition'] = 'attachment; filename=defaulters_report.xlsx'
        
        return response

    def changelist_view(self, request, extra_context=None):

        # Assuming defaulters_list is populated with your required data
        defaulters_list = []  # Your existing logic for populating this

        # Export to Excel
        if request.POST.get('export_to_excel'):  # Check if export button was pressed
            df = pd.DataFrame(defaulters_list)  # Convert the list of dictionaries to a DataFrame

            # Create an Excel file in memory
            excel_file = pd.ExcelWriter('defaulters_report.xlsx', engine='openpyxl')
            df.to_excel(excel_file, index=False, sheet_name='Defaulters')  # Write DataFrame to the Excel file

            # Save the file
            excel_file.save()
            excel_file.close()

            # Send the file to the user
            response = HttpResponse(
                content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
            )
            response['Content-Disposition'] = 'attachment; filename=defaulters_report.xlsx'
            response.write(excel_file)
            return response  # Return the response to download the file


        extra_context = extra_context or {}
        form = DefaultersReportForm(request.POST or None)  # Initialize form with POST data

        results = []
        if request.method == 'POST' and form.is_valid():
            selected_class = form.cleaned_data.get('student_class')
            selected_year = form.cleaned_data.get('year')

            # print(f"selected_class-----{selected_class}")
            # print(f"selected_year-----{selected_year}")

            if selected_year is None:
                current_year = date.today().year
                selected_year = current_year - 1 if date.today().month < 4 else current_year

            # Prepare data for queries
            current_date = date.today()
            month_array = self.get_months_array(selected_year)
            months_paid_str = ",".join(month_array)

            # print(f"current_date-----{current_date}")
            # print(f"month_array-----{month_array}")
            # print(f"months_paid_str-----{months_paid_str}")

            # class_string = "'nursery', 'pre-nursery', 'kg', '1', '2'"  # Add other classes as needed
            class_string = 'nursery,pre-nursery,kg,1,2'

            # Query to fetch students who have paid but not fully
            query = f"""
            SELECT student_fees.student_id, 
                GROUP_CONCAT(TRIM(student_fees.fees_period_month) ORDER BY CAST(student_fees.fees_period_month AS UNSIGNED)) AS months_paid,
                student_fees.student_class AS class_no,
                student_master.addmission_no, 
                student_master.admission_date,
                student_master.passedout_date, 
                student_master.student_name, 
                student_classes.section
            FROM student_fees
            LEFT JOIN student_master ON student_fees.student_id = student_master.student_id
            LEFT JOIN student_classes ON student_fees.student_id = student_classes.student_id 
                                    AND student_classes.class_no = student_fees.student_class
            WHERE student_fees.year = %s 
            AND COALESCE(student_fees.activity_fees, 0) > 0
            AND FIND_IN_SET(student_fees.student_class, %s)
            """

            if selected_class:
                query += f" AND student_fees.student_class = '{selected_class}' "

            query += f"""
            GROUP BY student_fees.student_id
            HAVING months_paid != '{months_paid_str}'
            """

            # Query to fetch students who haven't paid at all
            query_union = f"""
            SELECT student_master.student_id, 
                '' AS months_paid, 
                student_classes.class_no, 
                student_master.addmission_no,
                student_master.admission_date, 
                student_master.passedout_date, 
                student_master.student_name, 
                student_classes.section
            FROM student_master
            INNER JOIN student_classes ON student_master.student_id = student_classes.student_id
            WHERE student_master.student_id NOT IN (
                SELECT student_id FROM student_fees WHERE year = %s
            )
            AND FIND_IN_SET(student_classes.class_no, %s)
            """

            if selected_class:
                query_union += f" AND student_classes.class_no = '{selected_class}' "

            query_union += " GROUP BY student_classes.student_id HAVING MAX(student_classes.class_no)"

            # print(f"query-----{query}")
            # print(f"query_union-----{query_union}")

            # Combine both queries
            final_query = f"SELECT * FROM ({query} UNION {query_union}) AS combined ORDER BY class_no, section, addmission_no"

            

            # Execute the query using Django's raw SQL execution
            with connection.cursor() as cursor:
                # Manually format the query with actual parameter values for logging
                formatted_query = final_query % (selected_year, class_string, selected_year, class_string)

                # Print the formatted query to the console
                # print(f"final_query-----{formatted_query}")

                # Execute the query using the parameters
                cursor.execute(final_query, [selected_year, class_string, selected_year, class_string])

                # Fetch and print the results
                query_results = cursor.fetchall()
                # print(f"query_results-----{query_results}")

            # with connection.cursor() as cursor:
            #     cursor.execute(final_query, [selected_year, class_string, selected_year, class_string])
            #     print(f"final_query-----{final_query}")
            #     query_results = cursor.fetchall()
            #     print(f"query_results-----{query_results}")

            # Process results to identify unpaid months and defaulters
            defaulters_list = []
            for data in query_results:
                months_paid = data[1]
                passedout_date = data[5]
                months_paid_cleaned = [month.strip() for month in months_paid.split(',') if month]
                months_unpaid = sorted(list(set(month_array) - set(months_paid_cleaned)), key=lambda x: int(x))
                # months_unpaid = list(set(month_array) - set(months_paid_cleaned))

                # Only include students who have unpaid months and haven't passed out
                # if months_unpaid and (not passedout_date or passedout_date >= str(current_date)):
                if months_unpaid and (not passedout_date or passedout_date >= current_date):
                    defaulter_record = {
                        'addmission_no': data[3],
                        'student_name': data[6],
                        'class_no': data[2],
                        'section': data[7],
                        'unpaid_months': ",".join(months_unpaid)
                    }
                    defaulters_list.append(defaulter_record)

            # Save results to session for later export
            request.session['defaulters_list'] = defaulters_list

            results = defaulters_list

        # Add form and results to extra_context
        extra_context['form'] = form
        extra_context['results'] = results

        return super().changelist_view(request, extra_context=extra_context)

    change_list_template = 'admin/activity_fees_defaulter/change_list.html'

admin.site.register(activity_fees_defaulter, ActivityFeesDefaulterAdmin)
