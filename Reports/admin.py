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




# class CollectionReportResource(resources.ModelResource):
#     class Meta:
#         model = collection_report
#         # Specify the fields you want to include, or leave it empty for all fields
#         fields = ('id', 'student_id', 'date_payment', 'total_amount', 'amount_paid', 'remarks', 'added_by', 'added_at', 'edited_by', 'edited_at')
#         # If you want to set up import/export options, you can define them here.

# class CollectionReportAdmin(ExportMixin, admin.ModelAdmin):
#     resource_class = CollectionReportResource
#     list_display = (
#         'student_class',
#         'student_section',
#         'fees_for_months',
#         'fees_period_month',
#         'year',
#         'date_payment',
#         'concession_applied',
#         'annual_fees_paid',
#         'tuition_fees_paid',
#         'funds_fees_paid',
#         'admission_fees_paid',
#         'dayboarding_fees_paid',
#         'miscellaneous_fees_paid',
#         'bus_fees_paid',
#         'activity_fees',
#         'total_amount',
#         'amount_paid',
#         'payment_mode',
#         'cheq_no',
#         'txn_id',
#         'bank_name',
#         'cheque_status',
#         'realized_date',
#         'added_by',
#         'txn_ref_number',
#         'branch_name',
#         'txn_response_code',
#         'txn_payment_mode',
#         'added_at',
#         'edited_by',
#         'edited_at',
#         'remarks',
#         'entry_date',
#     )

#     def has_add_permission(self, request):
#         return False

#     def has_change_permission(self, request, obj=None):
#         return False

#     def has_delete_permission(self, request, obj=None):
#         return False

#     def changelist_view(self, request, extra_context=None):
#         """
#         Custom changelist view to show only the search results.
#         """
#         # Extract filters from the request
#         datefrom = request.GET.get('datefrom')
#         dateto = request.GET.get('dateto')
#         paymentType = request.GET.get('paymentType')
#         deviceType = request.GET.get('deviceType')
#         radioval = request.GET.get('radioval')

#         # Convert date strings to date objects (if provided)
#         datefrom1 = datetime.strptime(datefrom, "%Y-%m-%d") if datefrom else None
#         dateto1 = datetime.strptime(dateto, "%Y-%m-%d") if dateto else None

#         # Base queryset
#         queryset = student_fee.objects.all()

#         # Apply filters based on GET parameters
#         if radioval == 'advancedfees':
#             current_year = datetime.now().year
#             from_date = f"{current_year - 1}-04-01"
#             to_date = f"{current_year}-03-31"
#             queryset = queryset.filter(year=current_year, date_payment__range=[from_date, to_date])
#         elif radioval == 'customfees':
#             if datefrom1 and dateto1:
#                 queryset = queryset.filter(date_payment__range=[datefrom1, dateto1])
#             else:
#                 # Default to filtering by the last day if no date range is provided
#                 yesterday = datetime.now() - timedelta(days=1)
#                 queryset = queryset.filter(added_at__gte=yesterday, added_at__lt=datetime.now())
        
#         if paymentType:
#             queryset = queryset.filter(payment_mode=paymentType)
#         if deviceType:
#             queryset = queryset.filter(request_source=deviceType)

#         # Pass the filtered queryset to the context to display in the template
#         extra_context = extra_context or {}
#         # extra_context['cl'] = self.get_changelist_instance(request, queryset=queryset)

#         return super().changelist_view(request, extra_context=extra_context)

#     change_list_template = "admin/collection_report/change_list.html"  # Specify your custom template


# admin.site.register(collection_report, CollectionReportAdmin)


# class CollectionReportResource(resources.ModelResource):
#     class Meta:
#         model = collection_report
#         fields = ('id', 'student_id', 'date_payment', 'total_amount', 'amount_paid', 'remarks', 'added_by', 'added_at', 'edited_by', 'edited_at')

class CollectionReportAdmin(ExportMixin, admin.ModelAdmin):
    # resource_class = CollectionReportResource
    list_display = (
        'student_class',
        'student_section',
        'fees_for_months',
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

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    # def changelist_view(self, request, extra_context=None):
    #     """
    #     Custom changelist view to show filtered results or an empty list initially.
    #     """
    #     extra_context = extra_context or {}
        
    #     # Get filters and search term from the request
    #     datefrom = request.GET.get('datefrom')
    #     dateto = request.GET.get('dateto')
    #     paymentType = request.GET.get('paymentType')
    #     deviceType = request.GET.get('deviceType')
    #     radioval = request.GET.get('radioval')
    #     search_term = request.GET.get('q', '')  # Get search term from the request

    #     # Base queryset is empty to prevent showing the list initially
    #     queryset = collection_report.objects.none()

    #     # Check if any filters or search terms have been applied
    #     if datefrom or dateto or paymentType or deviceType or radioval or search_term:
    #         # Convert date strings to date objects (if provided)
    #         datefrom1 = datetime.strptime(datefrom, "%Y-%m-%d") if datefrom else None
    #         dateto1 = datetime.strptime(dateto, "%Y-%m-%d") if dateto else None

    #         # Create the base queryset
    #         queryset = collection_report.objects.all()

    #         # Apply filters based on GET parameters
    #         if radioval == 'advancedfees':
    #             current_year = datetime.now().year
    #             from_date = f"{current_year - 1}-04-01"
    #             to_date = f"{current_year}-03-31"
    #             queryset = queryset.filter(year=current_year, date_payment__range=[from_date, to_date])
    #         elif radioval == 'customfees':
    #             if datefrom1 and dateto1:
    #                 queryset = queryset.filter(date_payment__range=[datefrom1, dateto1])
    #             else:
    #                 # Default to filtering by the last day if no date range is provided
    #                 yesterday = datetime.now() - timedelta(days=1)
    #                 queryset = queryset.filter(added_at__gte=yesterday, added_at__lt=datetime.now())

    #         if paymentType:
    #             queryset = queryset.filter(payment_mode=paymentType)
    #         if deviceType:
    #             queryset = queryset.filter(request_source=deviceType)

    #         # Search results
    #         if search_term:
    #             queryset = queryset.filter(
    #                 Q(student_id__icontains=search_term) |
    #                 Q(date_payment__icontains=search_term) |
    #                 Q(total_amount__icontains=search_term) |
    #                 Q(remarks__icontains=search_term) |
    #                 Q(added_by__icontains=search_term) |
    #                 Q(edited_by__icontains=search_term)
    #             ).distinct()

    #     # Pass the filtered queryset to the context to display in the template
    #     extra_context['filtered_queryset'] = queryset

    #     return super().changelist_view(request, extra_context=extra_context)


    # def changelist_view(self, request, extra_context=None):
    #     """
    #     Custom changelist view to show filtered results or an empty list initially.
    #     """
    #     extra_context = extra_context or {}
        
    #     # Get filters and search term from the request
    #     datefrom = request.GET.get('datefrom')
    #     dateto = request.GET.get('dateto')
    #     paymentType = request.GET.get('paymentType')
    #     deviceType = request.GET.get('deviceType')
    #     radioval = request.GET.get('radioval')
    #     search_term = request.GET.get('q', '')  # Get search term from the request

    #     # Base queryset is empty to prevent showing the list initially
    #     queryset = collection_report.objects.none()

    #     # Initialize date variables
    #     datefrom1 = datetime.strptime(datefrom, "%Y-%m-%d") if datefrom else None
    #     dateto1 = datetime.strptime(dateto, "%Y-%m-%d") if dateto else None
    #     current_year = datetime.now().year
    #     from_date = f"{current_year - 1}-04-01"
    #     to_date = f"{current_year}-03-31"

    #     # Check if any filters or search terms have been applied
    #     if datefrom or dateto or paymentType or deviceType or radioval or search_term:
    #         # Create the base queryset
    #         queryset = collection_report.objects.all()

    #         # Apply filters based on GET parameters
    #         if radioval == 'advancedfees':
    #             queryset = queryset.filter(year=current_year, date_payment__range=[from_date, to_date])
    #         elif radioval == 'customfees':
    #             if datefrom1 and dateto1:
    #                 queryset = queryset.filter(date_payment__range=[datefrom1, dateto1])
    #             else:
    #                 # Default to filtering by the last day if no date range is provided
    #                 yesterday = datetime.now() - timedelta(days=1)
    #                 queryset = queryset.filter(added_at__gte=yesterday, added_at__lt=datetime.now())

    #         if paymentType:
    #             queryset = queryset.filter(payment_mode=paymentType)
    #         if deviceType:
    #             queryset = queryset.filter(request_source=deviceType)

    #         # Search results
    #         if search_term:
    #             queryset = queryset.filter(
    #                 Q(student_id__icontains=search_term) |
    #                 Q(date_payment__icontains=search_term) |
    #                 Q(total_amount__icontains=search_term) |
    #                 Q(remarks__icontains=search_term) |
    #                 Q(added_by__icontains=search_term) |
    #                 Q(edited_by__icontains=search_term)
    #             ).distinct()

    #     # Pass the filtered queryset to the context to display in the template
    #     extra_context['filtered_queryset'] = queryset

    #     return super().changelist_view(request, extra_context=extra_context)


    def changelist_view(self, request, extra_context=None):
        """
        Custom changelist view to show filtered results based on the form submission.
        """
        extra_context = extra_context or {}

        # Start with an empty queryset
        queryset = collection_report.objects.none()  

        # Initialize current year for filter logic
        current_year = datetime.now().year

        # Create the base queryset if any form filters are present
        if request.GET:
            # Create the base queryset from `collection_report` (or the relevant model)
            queryset = collection_report.objects.all()

            # Check for the fee type radio button
            if 'feestype' in request.GET:
                fee_type = request.GET['feestype']
                if fee_type == 'advancedfees':
                    queryset = queryset.filter(year=current_year)
                elif fee_type == 'customfees':
                    datefrom = request.GET.get('date_from')
                    dateto = request.GET.get('date_to')
                    if datefrom and dateto:
                        # Convert dates to datetime objects
                        datefrom1 = datetime.strptime(datefrom, "%Y-%m-%d")
                        dateto1 = datetime.strptime(dateto, "%Y-%m-%d")
                        queryset = queryset.filter(date_payment__range=[datefrom1, dateto1])
                    else:
                        # Default to filtering by the last day if no date range is provided
                        yesterday = datetime.now() - timedelta(days=1)
                        queryset = queryset.filter(added_at__gte=yesterday, added_at__lt=datetime.now())

            # Additional filters (if provided in the request)
            if 'paymentType' in request.GET:
                paymentType = request.GET['paymentType']
                if paymentType:
                    queryset = queryset.filter(payment_mode=paymentType)

            if 'deviceType' in request.GET:
                deviceType = request.GET['deviceType']
                if deviceType:
                    queryset = queryset.filter(request_source=deviceType)

            # Search term filter
            search_term = request.GET.get('q', '')  # Default to empty string if not present
            if search_term:
                queryset = queryset.filter(
                    Q(student_id__icontains=search_term) |
                    Q(date_payment__icontains=search_term) |
                    Q(total_amount__icontains=search_term) |
                    Q(remarks__icontains=search_term) |
                    Q(added_by__icontains=search_term) |
                    Q(edited_by__icontains=search_term)
                ).distinct()

        # Pass the filtered queryset to the context to display in the template
        extra_context['filtered_queryset'] = queryset

        return super().changelist_view(request, extra_context=extra_context)

    def get_search_results(self, request, queryset, search_term):
        """
        Filter the queryset based on search parameters from the request.
        """
        # Get filters from the request
        date_from = request.GET.get('date_from')
        date_to = request.GET.get('date_to')
        payment_type = request.GET.get('paymentType')
        device_type = request.GET.get('deviceType')
        fee_type = request.GET.get('feestype')

        print(f"date_from-date_to-payment_type-fee_type -> {date_from}-{date_to}-{payment_type}-{fee_type}")

        # Convert date strings to date objects
        date_from = datetime.strptime(date_from, "%Y-%m-%d") if date_from else None
        date_to = datetime.strptime(date_to, "%Y-%m-%d") if date_to else None

        # Start with the base queryset
        if fee_type == 'advancedfees':
            current_year = timezone.now().year
            from_date = f"{current_year - 1}-04-01"
            to_date = f"{current_year}-03-31"
            queryset = queryset.filter(year=current_year, date_payment__range=[from_date, to_date])
        elif fee_type == 'customfees':
            if date_from and date_to:
                queryset = queryset.filter(date_payment__range=[date_from, date_to])
            else:
                # Default to filtering by the last day if no date range is provided
                yesterday = timezone.now() - timedelta(days=1)
                queryset = queryset.filter(added_at__gte=yesterday, added_at__lt=timezone.now())
        else:
            if date_from and date_to:
                queryset = queryset.filter(date_payment__range=[date_from, date_to])
            else:
                # Apply any default filtering logic if necessary
                queryset = queryset.none()  # Or another default behavior

        # Apply additional filters based on payment type and device type
        if payment_type:
            queryset = queryset.filter(payment_mode=payment_type)
        # if device_type:
        #     queryset = queryset.filter(request_source=device_type)

        # Apply search term filtering (if necessary)
        if search_term:
            queryset = queryset.filter(
                Q(student_id__icontains=search_term) |
                Q(date_payment__icontains=search_term) |
                Q(total_amount__icontains=search_term) |
                Q(remarks__icontains=search_term) |
                Q(added_by__icontains=search_term) |
                Q(edited_by__icontains=search_term)
            ).distinct()

        return queryset, True


    change_list_template = "admin/collection_report/change_list.html"  # Specify your custom template

admin.site.register(collection_report, CollectionReportAdmin)


class ActivityFeesDefaulterResource(resources.ModelResource):
    class Meta:
        model = student_fee  # Define your model here
        fields = (
            'student_id', 'student_class', 
            'activity_fees', 'year'
        )  # Specify fields for export

        # fields = (
        #     'student_id__addmission_no', 'student_id__student_name', 
        #     'student_class', 'fees_for_months', 'activity_fees_paid'
        # )  # Specify fields for export


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


class ActivityFeesDefaulterAdmin(ExportMixin, admin.ModelAdmin):
    resource_class = ActivityFeesDefaulterResource

    list_display = ('student_id', 'student_class', 'activity_fees', 'year')

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('activity-fees-defaulters/', self.admin_site.admin_view(self.activity_fees_defaulters_view)),
            path('activity-fees-defaulters/export/', self.admin_site.admin_view(self.export_defaulters_to_csv), name="export_defaulters_csv"),
        ]
        return custom_urls + urls
    
    def get_months_array(self, year):
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


    def changelist_view(self, request, extra_context=None):
        return self.activity_fees_defaulters_view(request)

    def activity_fees_defaulters_view(self, request):
        form = DefaultersReportForm(request.POST or None)
        results = None

        if request.method == 'POST' and form.is_valid():
            selected_class = form.cleaned_data.get('student_class', None)
            selected_year = form.cleaned_data.get('year', None)

            current_date = datetime.today().strftime('%Y-%m-%d')
            month_array = self.get_months_array(int(selected_year)) if selected_year else []
            months = ",".join(month_array)

            # Query for unpaid and non-paid students
            base_query = student_fee.objects.filter(
                year=selected_year,
                activity_fees__gt=0
            ).annotate(
                months_paid=F('fees_period_month')
            ).values(
                'student_id',
                'student_class',
                'student_id__addmission_no',
                'student_id__admission_date',    # Contains date field
                'student_id__passedout_date',    # Contains date field
                'student_id__student_name',
            ).order_by('student_class', 'student_id__addmission_no')

            if selected_class:
                base_query = base_query.filter(student_class=selected_class)

            unpaid_students_query = base_query.filter(~Q(months_paid=months))

            non_paid_students_query = student_master.objects.filter(
                ~Q(student_id__in=student_fee.objects.filter(year=selected_year).values('student_id'))
            ).values(
                'student_id',
                'student_name',
                'addmission_no',
                'admission_date',  # Contains date field
                'passedout_date',  # Contains date field
            )

            from itertools import chain
            results = list(chain(unpaid_students_query, non_paid_students_query))

            # Convert date fields to strings before saving in the session
            def convert_dates(result):
                if 'student_id__admission_date' in result and result['student_id__admission_date']:
                    result['student_id__admission_date'] = result['student_id__admission_date'].strftime('%Y-%m-%d')
                if 'student_id__passedout_date' in result and result['student_id__passedout_date']:
                    result['student_id__passedout_date'] = result['student_id__passedout_date'].strftime('%Y-%m-%d')
                if 'admission_date' in result and result['admission_date']:
                    result['admission_date'] = result['admission_date'].strftime('%Y-%m-%d')
                if 'passedout_date' in result and result['passedout_date']:
                    result['passedout_date'] = result['passedout_date'].strftime('%Y-%m-%d')
                return result

            results = [convert_dates(r) for r in results]

            # Store results in session
            request.session['defaulters_report_results'] = results

        context = dict(
            self.admin_site.each_context(request),
            form=form,
            results=results,
            title="Activity Fees Defaulters Report",
        )
        return TemplateResponse(request, "admin/activity_fees_defaulter/change_list.html", context)

    def export_defaulters_to_csv(self, request):
        # Fetch the results from the session (which were saved during the report generation)
        results = request.session.get('defaulters_report_results', None)
        
        if results is None:
            return HttpResponse("No data available for export", status=400)

        # Ensure `month_array` is retrieved or reconstructed from the session
        selected_year = 2024 #request.session.get('selected_year', None)
        if selected_year:
            month_array = self.get_months_array(int(selected_year))  # Assuming this is already defined elsewhere
        else:
            return HttpResponse("No year selected", status=400)
        
        # Create CSV response
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="defaulters_report.csv"'

        writer = csv.writer(response)
        writer.writerow(['Admission No', 'Student Name', 'Class', 'Unpaid Months'])

        # Write the rows from the results stored in the session
        for result in results:
            mp = result.get('months_paid', '')
            unpaid_months = list(set(month_array) - set(mp.split(','))) if mp else month_array
            writer.writerow([
                result['student_id__addmission_no'],
                result['student_id__student_name'],
                result['student_class'],
                ",".join(unpaid_months) if unpaid_months else 'All Months Paid'
            ])

        return response

# class ActivityFeesDefaulterAdmin(ExportMixin, admin.ModelAdmin):

#     resource_class = ActivityFeesDefaulterResource  # Assign the resource class for export

#     list_display = ('student_id', 'student_class', 'activity_fees', 'year')

#     def get_urls(self):
#         urls = super().get_urls()
#         custom_urls = [
#             path('activity-fees-defaulters/', self.admin_site.admin_view(self.activity_fees_defaulters_view)),
#         ]
#         return custom_urls + urls

#     def changelist_view(self, request, extra_context=None):
#         """
#         Override the default changelist view to use the custom defaulters report view.
#         """
#         return self.activity_fees_defaulters_view(request)

#     """ def get_months_array(self, year):
#         # Logic to generate the months array based on the year, similar to the PHP function get_months_array
#         start_month = 4  # Assume the financial year starts in April
#         months_array = [str(month) for month in range(start_month, start_month + 12)]
#         return months_array """
    
#     def get_months_array(self, year):
#         # Define the start and end of the financial year
#         datefrom = f"{year}0401"  # First date of the financial year (April 1st)
#         dateto = f"{year + 1}0331"  # Last date of the financial year (March 31st of the next year)

#         # Convert to actual date format (Y-m-d)
#         datefrom1 = datetime.strptime(datefrom, "%Y%m%d").date()
#         dateto1 = datetime.strptime(dateto, "%Y%m%d").date()

#         # Get the current date
#         currentdate = datetime.now().date()

#         # If the financial year is not over yet, set `dateto1` to today
#         if currentdate < dateto1:
#             dateto1 = currentdate

#         # Initialize the month array
#         month_array = []
        
#         # Create a timestamp starting from `datefrom1`
#         time = datefrom1
#         to_month = dateto1.month

#         # Iterate for a maximum of 12 months
#         for i in range(12):
#             # Get the current month
#             cur_month = time.month
            
#             # Stop if the last month (current month) is reached
#             if cur_month == to_month:
#                 break

#             # Add the month number to the array, stripping leading zeroes
#             month_array.append(str(cur_month).lstrip('0'))
            
#             # Move to the next month
#             time = time + timedelta(days=31)
#             time = time.replace(day=1)  # Ensure to set the day to the 1st of the next month

#         # If all months have passed, return a full array from 1 to 12
#         if not month_array:
#             month_array = [str(i) for i in range(1, 13)]

#         # Sort the month array to ensure the months are in ascending order
#         month_array.sort(key=int)

#         return month_array

#     def activity_fees_defaulters_view(self, request):
#         form = DefaultersReportForm(request.POST or None)
#         results = None

#         if request.method == 'POST' and form.is_valid():
#             selected_class = form.cleaned_data.get('student_class', None)
#             selected_year = form.cleaned_data.get('year', None)

#             # Get current date and month array based on the selected year
#             current_date = datetime.today().strftime('%Y-%m-%d')
#             month_array = self.get_months_array(int(selected_year)) if selected_year else []
#             months = ",".join(month_array)

#             # Base query for students who have paid some fees
#             base_query = student_fee.objects.filter(
#                 year=selected_year,
#                 activity_fees__gt=0  # activity_fees > 0
#             ).annotate(
#                 months_paid=F('fees_period_month')
#             ).values(
#                 'student_id',
#                 'student_class',
#                 'student_id__addmission_no',
#                 'student_id__admission_date',
#                 'student_id__passedout_date',
#                 'student_id__student_name',
#             ).order_by(
#                 'student_class', 'student_id__addmission_no'
#             )

#             # Apply class filter if selected
#             if selected_class:
#                 base_query = base_query.filter(student_class=selected_class)

#             # Query for students who haven't paid for all months
#             unpaid_students_query = base_query.filter(~Q(months_paid=months))

#             # Query for students who haven't paid any fees (no record in `student_fee`)
#             non_paid_students_query = student_master.objects.filter(
#                 ~Q(student_id__in=student_fee.objects.filter(year=selected_year).values('student_id')),
#             ).values(
#                 'student_id',
#                 'student_name',
#                 'addmission_no',
#                 'admission_date',
#                 'passedout_date',
#             )

#             # Combine the two querysets
#             from itertools import chain
#             results = list(chain(unpaid_students_query, non_paid_students_query))

#         # Pass the form and results to the template for rendering
#         context = dict(
#             self.admin_site.each_context(request),
#             form=form,
#             results=results,
#             title="Activity Fees Defaulters Report",
#         )
#         return TemplateResponse(request, "admin/activity_fees_defaulter/change_list.html", context)


#     # def activity_fees_defaulters_view(self, request):
#     #     form = DefaultersReportForm(request.POST or None)
#     #     results = None

#     #     if request.method == 'POST' and form.is_valid():
#     #         selected_class = form.cleaned_data.get('student_class', None)
#     #         selected_year = form.cleaned_data.get('year', None)

#     #         # Get current date and month array based on the selected year
#     #         current_date = datetime.today().strftime('%Y-%m-%d')
#     #         month_array = self.get_months_array(int(selected_year)) if selected_year else []
#     #         months = ",".join(month_array)

#     #         print(f"months -------:{months}")

#     #         # Create base query for students who have paid
#     #         base_query = student_fee.objects.filter(
#     #             year=selected_year,
#     #             activity_fees__gt=0  # activity_fees > 0
#     #         ).annotate(
#     #             months_paid=F('fees_period_month'),  # group_concat equivalent
#     #         ).values(
#     #             'student_id',
#     #             'student_class',
#     #             'student_id__addmission_no',
#     #             'student_id__admission_date',
#     #             'student_id__passedout_date',
#     #             'student_id__student_name',
#     #             # 'student_class__section',
#     #         ).order_by(
#     #             'student_class', 'student_id__addmission_no'
#     #         )

#     #         # print(f"resubase_query 1-------:{base_query}")


#     #         # Apply class filter if selected
#     #         if selected_class:
#     #             base_query = base_query.filter(student_class=selected_class)
#     #             # print(f"base_query 2-------:{base_query}")

            

#     #         # Query students who haven't paid for all months
#     #         unpaid_students_query = base_query.filter(~Q(months_paid=months))

#     #         print(f"unpaid_students_query 1-------:{unpaid_students_query}")

#     #        # Query students who haven't paid at all (no fees record)
#     #         non_paid_students_query = student_master.objects.filter(
#     #             ~Q(student_id__in=student_fee.objects.filter(year=selected_year).values('student_id')),
#     #         ).values(
#     #             'student_id',  # Correctly reference student_id
#     #             'student_name',  # Assuming you want to keep this
#     #             'addmission_no',  # Correctly reference addmission_no
#     #             'admission_date',  # Correctly reference admission_date
#     #             'passedout_date',  # Correctly reference passedout_date
#     #             # 'student_class__section',  # Uncomment if needed and ensure it's referenced correctly
#     #         )

#     #         print(f"non_paid_students_query 1-------:{non_paid_students_query}")

#     #         # Combine the two querysets using Django's chain function
#     #         from itertools import chain
#     #         results = list(chain(unpaid_students_query, non_paid_students_query))

#     #         # print(f"results-------:{results}")

#     #         # Handle AJAX request to return the result in JSON format
#     #         # Handle AJAX request to return the result in JSON format
#     #         if request.headers.get('x-requested-with') == 'XMLHttpRequest':
#     #             data = []
#     #             for fee in results:
#     #                 """ mp = fee['fees_period_month']
#     #                 passedout_date = fee['student_id__passedout_date']
#     #                 mp2 = [month.strip() for month in mp.split(',')] if mp else []
#     #                 unpaid_months = list(set(month_array) - set(mp2))

#     #                 if not unpaid_months or (passedout_date and passedout_date < current_date):
#     #                     # Skip the students who have paid all fees or have passed out
#     #                     continue

#     #                 data.append({
#     #                     'admission_no': fee['student_id__addmission_no'],
#     #                     'student_name': fee['student_id__student_name'],
#     #                     'student_class': fee['student_class'],
#     #                     # 'student_section': fee['student_class__section'],
#     #                     'unpaid_months': ",".join(unpaid_months),
#     #                 }) """


                    

#     #             return JsonResponse({'results': "ok"})

#     #         """ if request.is_ajax():
#     #             data = []
#     #             for fee in results:
#     #                 mp = fee['months_paid']
#     #                 passedout_date = fee['student_id__passedout_date']
#     #                 mp2 = [month.strip() for month in mp.split(',')] if mp else []
#     #                 unpaid_months = list(set(month_array) - set(mp2))

#     #                 if not unpaid_months or (passedout_date and passedout_date < current_date):
#     #                     # Skip the students who have paid all fees or have passed out
#     #                     continue

#     #                 data.append({
#     #                     'admission_no': fee['student_id__addmission_no'],
#     #                     'student_name': fee['student_id__student_name'],
#     #                     'student_class': fee['student_class'],
#     #                     # 'student_section': fee['student_class__section'],
#     #                     'unpaid_months': ",".join(unpaid_months),
#     #                 })

#     #             return JsonResponse({'results': data}) """

#     #     # Pass data to the template
#     #     context = dict(
#     #         self.admin_site.each_context(request),
#     #         form=form,
#     #         results=results,
#     #         title="Activity Fees Defaulters Report",
#     #     )
#     #     return TemplateResponse(request, "admin/activity_fees_defaulter/change_list.html", context)


admin.site.register(activity_fees_defaulter, ActivityFeesDefaulterAdmin)

    # def activity_fees_defaulters_view(self, request):
    #     form = DefaultersReportForm(request.POST or None)
    #     results = None

    #     if request.method == 'POST' and form.is_valid():
    #         selected_class = form.cleaned_data['student_class']
    #         selected_year = form.cleaned_data['year']

    #         # Query students with unpaid activity fees
    #         results = student_fee.objects.filter(
    #             student_class=selected_class,
    #             year=selected_year,
    #             activity_fees_paid__isnull=True
    #         )

    #         # Handle AJAX request
    #         if request.is_ajax():
    #             data = []
    #             for fee in results:
    #                 data.append({
    #                     'admission_no': fee.student_id.admission_no,
    #                     'student_name': fee.student_id.student_name,
    #                     'student_class': fee.student_class,
    #                     'student_section': fee.student_section,
    #                     'fees_for_months': fee.fees_for_months,
    #                 })
    #             return JsonResponse({'results': data})

    #     # Use admin_site.each_context(request) to get the correct context
    #     context = dict(
    #         self.admin_site.each_context(request),
    #         form=form,
    #         results=results,
    #         title="Activity Fees Defaulters Report",
    #     )
    #     return TemplateResponse(request, "admin/activity_fees_defaulter/change_list.html", context)


# class ActivityFeesDefaulterAdmin(admin.ModelAdmin):
#     # list_display = ('student', 'class_no', 'section', 'activity_fees_due', 'last_payment_date', 'is_defaulter')
#     # list_filter = ('class_no', 'section', 'is_defaulter')
#     # search_fields = ('student__student_name', 'class_no')

#     def has_add_permission(self, request):
#         return False  # You may want to disallow adding defaulters manually

#     def has_change_permission(self, request, obj=None):
#         return False  # Disallow changing defaulters

#     def has_delete_permission(self, request, obj=None):
#         return False  # Disallow deleting defaulters
    
#     def get_urls(self):
#         urls = super().get_urls()
#         custom_urls = [
#             path('activity-fees-defaulters/', self.admin_site.admin_view(self.activity_fees_defaulters_view)),
#             # path('ajax/get-students/', self.admin_site.admin_view(self.get_students), name='ajax_get_students'),
#         ]
#         return custom_urls + urls

#     def activity_fees_defaulters_view(self, request):
#         form = DefaultersReportForm(request.POST or None)
        
#         if request.method == 'POST' and form.is_valid():
#             selected_class = form.cleaned_data['student_class']
#             selected_year = form.cleaned_data['year']

#             # Query students with unpaid activity fees
#             results = student_fee.objects.filter(
#                 student_class=selected_class,
#                 year=selected_year,
#                 activity_fees_paid__isnull=True
#             )

#             # Handle AJAX request
#             if request.is_ajax():
#                 data = []
#                 for fee in results:
#                     data.append({
#                         'admission_no': fee.student_id.admission_no,
#                         'student_name': fee.student_id.student_name,
#                         'student_class': fee.student_class,
#                         'student_section': fee.student_section,
#                         'fees_for_months': fee.fees_for_months,
#                     })
#                 return JsonResponse({'results': data})

#         # Render standard template for non-AJAX requests
#         context = dict(
#             self.each_context(request),
#             form=form,
#             results=results if not request.is_ajax() else None,
#             title="Activity Fees Defaulters Report",
#         )
#         return TemplateResponse(request, "admin/activity_fees_defaulter/change_list.html", context)

#     """ def activity_fees_defaulters_view(self, request):
#         form = DefaultersReportForm(request.POST or None)
#         results = None

#         if request.method == 'POST' and form.is_valid():
#             selected_class = form.cleaned_data['student_class']
#             selected_year = form.cleaned_data['year']

#             # Query students with unpaid activity fees
#             results = student_fee.objects.filter(
#                 student_class=selected_class,
#                 year=selected_year,
#                 activity_fees_paid__isnull=True
#             )

#         context = dict(
#             self.each_context(request),
#             form=form,
#             results=results,
#             title="Activity Fees Defaulters Report",
#         )
#         return TemplateResponse(request, "admin/activity_fees_defaulter/change_list.html", context) """



