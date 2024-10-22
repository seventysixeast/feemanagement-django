from django.contrib import admin
from .models import (
    transport, tuition_fees_defaulter,admission_report, final_fees_report, transport_defaulter, cheque_deposit
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

from django.db.models import Subquery, OuterRef
from django.db.models import Exists, OuterRef

from django.db.models import Sum

from datetime import datetime, timedelta
from django.db.models import F, Q, Value, CharField


    
from django.db.models import Sum, F
from django.db.models import CharField, Value as V

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

# def get_months_array(year):
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

from datetime import datetime, timedelta

def get_months_array(year):
    # Define the start and end dates of the financial year
    datefrom = datetime(year, 4, 1)  # April 1st of the selected year
    dateto = datetime(year + 1, 3, 31)  # March 31st of the next year
    
    # Get current date
    currentdate = datetime.today()

    montharray = []

    # If the current date is before the financial year end
    if currentdate < dateto:
        # Adjust the end date to today's date
        dateto = currentdate

        # Generate months from datefrom to dateto
        cur_date = datefrom
        while cur_date <= dateto:
            # Append the month number without leading zero
            montharray.append(cur_date.month)
            # Move to the next month
            cur_date = (cur_date.replace(day=28) + timedelta(days=4)).replace(day=1)
        
        # Sort the array to ensure months are in ascending order
        montharray.sort()
    else:
        # If the current date is after the financial year end, return all months
        montharray = list(range(1, 13))  # Months 1 to 12

    return montharray


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
    list_display = ('admission_no', 'student_name', 'class_no', 'section', 'tmpval')
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


 # Use obj as a dict because values() returns a dict


# class FinalFeesReportAdmin(admin.ModelAdmin):
#     model = final_fees_report

#     list_display = (
#         'student_class', 'total_annual_fees'
#     )

#     def has_add_permission(self, request):
#         return False

#     def has_change_permission(self, request, obj=None):
#         return False

#     def has_delete_permission(self, request, obj=None):
#         return False
    
#     class MoneySerializer(serializers.ModelSerializer):
#     total_annual_fees = serializers.IntegerField()

#     class Meta:
#         model =  final_fees_report
#         fields = ('student_class', 'total_annual_fees')

#     def get_queryset(self, request):
#         # Extract parameters from request (you can modify this part as needed)
#         year = "2024"  # Hardcoded for testing, adjust dynamically if needed

#         try:
#             year = int(year)
#         except ValueError:
#             year = datetime.now().year  # Fallback to current year if invalid

#         # Calculate date range for the academic year
#         from_year = f"{year}-04-01"
#         to_year = f"{year + 1}-03-31"

#         # Perform aggregation but still return the queryset as model instances
#         queryset = student_fee.objects.filter(
#             date_payment__range=[from_year, to_year]
#         ).values('student_class').annotate(
#             total_annual_fees=Sum('annual_fees_paid'),
#             # total_tuition_fees=Sum('tuition_fees_paid'),
#             # total_funds_fees=Sum('funds_fees_paid'),
#             # total_sports_fees=Sum('sports_fees_paid'),
#             # total_activity_fees=Sum('activity_fees'),
#             # total_admission_fees=Sum('admission_fees_paid'),
#             # total_security_fees=Sum('security_paid'),
#             # total_late_fees=Sum('late_fees_paid'),
#             # total_dayboarding_fees=Sum('dayboarding_fees_paid'),
#             # total_bus_fees=Sum('bus_fees_paid'),
#             # total_fees_amount=Sum('total_amount'),
#             # total_amount_paid=Sum('amount_paid')
#         ).order_by('student_class')

#         return queryset

    # Display method for total annual fees
    # def total_annual_fees_display(self, obj):
    #     return obj.total_annual_fees  # Access the annotated field directly


from rest_framework import serializers  # Importing serializers for the MoneySerializer

# Serializer for handling data representation (useful for APIs or exporting data)
# class MoneySerializer(serializers.ModelSerializer):
#     total_annual_fees = serializers.IntegerField()

#     class Meta:
#         model = final_fees_report
#         fields = ('student_class', 'total_annual_fees')

# Django Admin class for displaying the data
# class FinalFeesReportAdmin(admin.ModelAdmin):
#     model = final_fees_report

#     list_display = (
#         'student_class','total_annual_fees_display',
#     )

#     def has_add_permission(self, request):
#         return False

#     def has_change_permission(self, request, obj=None):
#         return False

#     def has_delete_permission(self, request, obj=None):
#         return False

#     def get_queryset(self, request):
#         # Extract parameters from request or hardcode for testing
#         year = "2024"  # You can replace this with dynamic extraction from request if needed

#         try:
#             year = int(year)
#         except ValueError:
#             year = datetime.now().year  # Fallback to current year if the value is invalid

#         # Calculate date range for the academic year
#         from_year = f"{year}-04-01"
#         to_year = f"{year + 1}-03-31"

#         # Perform aggregation but return the queryset as model instances
#         queryset = student_fee.objects.filter(
#             date_payment__range=[from_year, to_year]
#         ).values('student_class').annotate(
#             total_annual_fees=Sum('annual_fees_paid'),
#         ).order_by('student_class')

#         print('queryset',queryset)

#         # return queryset
#         return list(queryset)
    
#     # Custom display for total_annual_fees in list_display
#     def total_annual_fees_display(self, obj):
#         # Access the 'total_annual_fees' from the dictionary returned by get_queryset
#         return obj.get('total_annual_fees', 0)

#     total_annual_fees_display.short_description = "Total Annual Fees"

#     # Display the student class in the list
#     def student_class(self, obj):
#         return obj.get('student_class', 'Unknown')

#     student_class.short_description = "Student Class"

    # Custom display for total_annual_fees
    # def total_annual_fees_display(self, obj):
    #     print('Full object:', obj.__dict__)
    #     return obj.student_class if obj.student_class else 0

    # total_annual_fees_display.short_description = "Total Annual Fees"

# Register the admin class with the model
# admin.site.register(final_fees_report, FinalFeesReportAdmin)


# Register the admin

# from django.contrib import admin
# from django.db.models import Sum
# from .models import student_fee  # Ensure you import your model
# working fine
# class FinalFeesReportAdmin(admin.ModelAdmin):
#     model = final_fees_report
#     list_display = (
#         'student_class', 'total_annual_fees_display',  # Add the display method for total fees
#     )

#     def has_add_permission(self, request):
#         return False

#     def has_change_permission(self, request, obj=None):
#         return False

#     def has_delete_permission(self, request, obj=None):
#         return False

#     def get_queryset(self, request):
#         # Extract parameters from request or hardcode for testing
#         year = "2024"  # You can replace this with dynamic extraction from request if needed

#         try:
#             year = int(year)
#         except ValueError:
#             year = datetime.now().year  # Fallback to current year if the value is invalid

#         # Calculate date range for the academic year
#         from_year = f"{year}-04-01"
#         to_year = f"{year + 1}-03-31"

#         # Perform aggregation
#         queryset = student_fee.objects.filter(
#             date_payment__range=[from_year, to_year]
#         ).values('student_class').annotate(
#             total_annual_fees=Sum('annual_fees_paid'),
#             total_tuition_fees=Sum('tuition_fees_paid'),
#             total_funds_fees=Sum('funds_fees_paid'),
#             total_sports_fees=Sum('sports_fees_paid'),
#             total_activity_fees=Sum('activity_fees'),
#             total_admission_fees=Sum('admission_fees_paid'),
#             total_security_fees=Sum('security_paid'),
#             total_late_fees=Sum('late_fees_paid'),
#             total_dayboarding_fees=Sum('dayboarding_fees_paid'),
#             total_bus_fees=Sum('bus_fees_paid'),
#             total_fees_amount=Sum('total_amount'),
#             total_amount_paid=Sum('amount_paid')
#         ).order_by('student_class')

#         # Use list() to convert to a list of dictionaries
#         return (queryset)

#     # Custom display for total_annual_fees in list_display
#     def total_annual_fees_display(self, obj):
#         # Access the 'total_annual_fees' from the dictionary returned by get_queryset
#         return obj.get('total_annual_fees', 0)

#     total_annual_fees_display.short_description = "Total Annual Fees"

#     # Display the student class in the list
#     def student_class(self, obj):
#         return obj.get('student_class', 'Unknown')

#     student_class.short_description = "Student Class"
# working fine


# class FinalFeesReportAdmin(admin.ModelAdmin):
#     model = final_fees_report

#     list_display = (
#         'student_class',
#     )

#     def has_add_permission(self, request):
#         return False

#     def has_change_permission(self, request, obj=None):
#         return False

#     def has_delete_permission(self, request, obj=None):
#         return False

#     def get_search_results(self, request, queryset, search_term):
#         # Extract parameters from request
#         reporttype = request.GET.get('reporttype')
#         year = request.GET.get('year')

#         if reporttype == "summaryreport" and year:
#             try:
#                 year = int(year)
#             except ValueError:
#                 year = datetime.now().year  # Fallback to current year if invalid

#             # Calculate date range from the year
#             from_year = f"{year}-04-01"
#             to_year = f"{year + 1}-03-31"

#             # Aggregate the data based on the class
#             queryset = student_fee.objects.filter(
#                 date_payment__range=[from_year, to_year]
#             ).values('student_class').annotate(
#                 total_annual_fees=Sum('annual_fees_paid'),
#                 total_tuition_fees=Sum('tuition_fees_paid'),
#                 total_funds_fees=Sum('funds_fees_paid'),
#                 total_sports_fees=Sum('sports_fees_paid'),
#                 total_activity_fees=Sum('activity_fees'),
#                 total_admission_fees=Sum('admission_fees_paid'),
#                 total_security_fees=Sum('security_paid'),
#                 total_late_fees=Sum('late_fees_paid'),
#                 total_dayboarding_fees=Sum('dayboarding_fees_paid'),
#                 total_bus_fees=Sum('bus_fees_paid'),
#                 total_amount=Sum('Total_amount'),
#                 total_amount_paid=Sum('amount_paid'),
#             ).order_by('student_class')

#         return queryset, False

# Register the admin
# admin.site.register(final_fees_report, FinalFeesReportAdmin)

from django.shortcuts import render
from django.template.response import TemplateResponse
from django.utils.datetime_safe import datetime

class FinalFeesReportAdmin(admin.ModelAdmin):
    model = student_fee
    change_list_template = "admin/final_fees_report_change_list.html"  # Custom template
    
    list_display = ('student_class',)
    
    # Permissions removed
    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def changelist_view(self, request, extra_context=None):
        reporttype = request.GET.get('reporttype', 'summaryreport')  # Default to 'summaryreport'
        year = request.GET.get('year', datetime.now().year)  # Default to current year

        # Ensure year is valid
        try:
            year = int(year)
        except ValueError:
            year = datetime.now().year

        queryset = self.get_filtered_queryset(reporttype, year)

        extra_context = extra_context or {}
        extra_context['reporttype'] = reporttype
        extra_context['year'] = year
        extra_context['years'] = list(range(2000, 2026))  # Populate years 2000-2025
        extra_context['report_types'] = ["Summary report", "Advance report"]  # Populate report types
        extra_context['opts'] = self.model._meta

        return super().changelist_view(request, extra_context=extra_context)


    def get_filtered_queryset(self, reporttype, year):
        """
        Return a filtered queryset based on report type and year.
        """
        from_year = f"{year}-04-01"
        to_year = f"{year + 1}-03-31"

        # Modify queryset based on reporttype
        if reporttype == "summaryreport":
            queryset = student_fee.objects.filter(
                date_payment__range=[from_year, to_year]
            ).values(
                'student_class'
            ).annotate(
                total_annual_fees=Sum('annual_fees_paid'),
                total_tuition_fees=Sum('tuition_fees_paid'),
                total_funds_fees=Sum('funds_fees_paid'),
                total_sports_fees=Sum('sports_fees_paid'),
                total_activity_fees=Sum('activity_fees'),
                total_admission_fees=Sum('admission_fees_paid'),
                total_security_fees=Sum('security_paid'),
                total_late_fees=Sum('late_fees_paid'),
                total_dayboarding_fees=Sum('dayboarding_fees_paid'),
                total_bus_fees=Sum('bus_fees_paid'),
                total_fees_amount=Sum('total_amount'),
                total_amount_paid=Sum('amount_paid'),
            ).order_by('student_class')

            print("queryset",queryset)
        else:
            # Handle "Advance report" or any other type if needed
            queryset = student_fee.objects.filter(
                date_payment__range=[from_year, to_year]
            ).values(
                'student_class'
            ).distinct().order_by('student_class')

        return list(queryset)



# from django.db.models import Sum
# from django.utils.html import format_html
# from django.db.models import Sum
# from django.db.models import Sum

# class FinalFeesReportAdmin(admin.ModelAdmin):
#     model = student_fee  # Ensure this is the correct model

#     # Display the student class and total fees
#     list_display = ('student_class', 'total_annual_fees')

#     def has_add_permission(self, request):
#         return False

#     def has_change_permission(self, request, obj=None):
#         return False

#     def has_delete_permission(self, request, obj=None):
#         return False

#     def get_queryset(self, request):
#         """
#         Return the normal queryset with all model instances.
#         We'll handle aggregation separately to keep model instances in the admin.
#         """
#         year = "2024"  # Static for now, but you can dynamically adjust
#         try:
#             year = int(year)
#         except ValueError:
#             year = datetime.now().year

#         # Define date range for the academic year
#         from_year = f"{year}-04-01"
#         to_year = f"{year + 1}-03-31"

#         # Return the standard model instances queryset
#         return student_fee.objects.filter(date_payment__range=[from_year, to_year]).order_by('student_class').order_by('student_class').distinct()

#     def total_annual_fees(self, obj):
#         """
#         Calculate the total annual fees for each student_class and return.
#         This method performs aggregation on model instances.
#         """
#         year = "2024"  # Ensure year matches, or make this dynamic based on user input
#         try:
#             year = int(year)
#         except ValueError:
#             year = datetime.now().year

#         # Calculate date range for the academic year
#         from_year = f"{year}-04-01"
#         to_year = f"{year + 1}-03-31"

#         # Aggregate total fees paid for this specific student class
#         total_fees = student_fee.objects.filter(
#             date_payment__range=[from_year, to_year],
#             student_class=obj.student_class
#         ).aggregate(total_annual_fees=Sum('annual_fees_paid'))['total_annual_fees']

#         # Return the calculated total fees, or 0 if there's no data
#         return total_fees or 0

#     # Set the display name for the custom method in the list display
#     total_annual_fees.short_description = 'Total Annual Fees'

# from django.db.models import Sum

# class FinalFeesReportAdmin(admin.ModelAdmin):
#     model = student_fee  # Make sure this is the correct model

#     # Display the student class and total fees
#     list_display = ('student_class_display', 'total_annual_fees_display')

#     def has_add_permission(self, request):
#         return False

#     def has_change_permission(self, request, obj=None):
#         return False

#     def has_delete_permission(self, request, obj=None):
#         return False

#     # def get_queryset(self, request):
#     #     """
#     #     Return a queryset with distinct student_class and annotate the total fees.
#     #     """
#     #     year = "2024"  # Static for now, adjust dynamically if needed
#     #     try:
#     #         year = int(year)
#     #     except ValueError:
#     #         year = datetime.now().year

#     #     # Define date range for the academic year
#     #     from_year = f"{year}-04-01"
#     #     to_year = f"{year + 1}-03-31"

#     #     # Perform aggregation while returning model instances
#     #     queryset = student_fee.objects.filter(
#     #         date_payment__range=[from_year, to_year]
#     #     ).values(
#     #         'student_class'
#     #     ).annotate(
#     #         total_annual_fees=Sum('annual_fees_paid')
#     #     ).order_by('student_class')

#     #     # Convert the values() queryset into a list of model instances
#     #     # using distinct values for 'student_class' and returning model instances
#     #     return student_fee.objects.values(
#     #         'student_class'
#     #     ).distinct()

#     def get_queryset(self, request):
#         """
#         Return a queryset with distinct student_class values without aggregation.
#         """
#         year = "2024"  # Static for now, adjust dynamically if needed
#         try:
#             year = int(year)
#         except ValueError:
#             year = datetime.now().year

#         # Define date range for the academic year
#         from_year = f"{year}-04-01"
#         to_year = f"{year + 1}-03-31"

#         # Fetch distinct student_class values without aggregation
#         queryset = student_fee.objects.filter(
#             date_payment__range=[from_year, to_year]
#         ).values(
#             'student_class'
#         ).distinct().order_by('student_class')  # Ensure distinct and ordered by student_class

#         return queryset
    
#     def total_annual_fees_display(self, obj):
#         """
#         Calculate total fees for the given student class.
#         """
#         year = "2024"  # Static, adjust dynamically if needed
#         try:
#             year = int(year)
#         except ValueError:
#             year = datetime.now().year

#         # Define date range for the academic year
#         from_year = f"{year}-04-01"
#         to_year = f"{year + 1}-03-31"

#         # Calculate total fees for each student_class
#         total_fees = student_fee.objects.filter(
#             date_payment__range=[from_year, to_year],
#             student_class=obj['student_class']
#         ).aggregate(total_fees=Sum('annual_fees_paid'))['total_fees']

#         return total_fees or 0  # Return total fees, or 0 if none

#     def student_class_display(self, obj):
#         return obj['student_class']

#     # def total_annual_fees_display(self, obj):
#     #     """
#     #     Display total annual fees for each student_class by aggregating in the queryset.
#     #     """
#     #     year = "2024"  # Make this dynamic as necessary
#     #     try:
#     #         year = int(year)
#     #     except ValueError:
#     #         year = datetime.now().year

#     #     # Define date range for the academic year
#     #     from_year = f"{year}-04-01"
#     #     to_year = f"{year + 1}-03-31"

#     #     # Calculate total fees for each student_class
#     #     total_fees = student_fee.objects.filter(
#     #         date_payment__range=[from_year, to_year],
#     #         student_class=obj.student_class
#     #     ).aggregate(total_annual_fees=Sum('annual_fees_paid'))['total_annual_fees']

#     #     return total_fees or 0

#     # # Set the display name for the custom method in the list display
#     # total_annual_fees_display.short_description = 'Total Annual Fees'




# Register the admin class with the model
# admin.site.register(student_fee, FinalFeesReportAdmin)

# admin.site.register(final_fees_report, FinalFeesReportAdmin)


admin.site.register(final_fees_report, FinalFeesReportAdmin)




class TransportDefaulterResource(resources.ModelResource):

    class Meta:
        model = transport_defaulter
        fields = ('addmission_no','student_name', 'student_class', 'student_section', 
        'route', 'destination', 'unpaid_months')

    addmission_no = Field(attribute='addmission_no', column_name='Admission No')
    student_name = Field(attribute='student_name', column_name='Student Name')
    student_class = Field(attribute='student_class', column_name='Class')
    student_section = Field(attribute='student_section', column_name='Section')
    route = Field(attribute='route', column_name='Route')
    destination = Field(attribute='destination', column_name='Destination')
    unpaid_months = Field(attribute='unpaid_months', column_name='Busfees unpaid for months')

    def dehydrate_student_name(self, obj):
        return obj.student_id.student_name

    
    def dehydrate_addmission_no(self, obj):
        return obj.student_id.addmission_no
    
    def dehydrate_unpaid_months(self, obj):
        # Get the year from the object
        year = int(obj.year)
        current_date = datetime.now().date()
        # year = self.get_year()
        montharray = get_months_array(year)

        months_paid = obj.months_paid
        passedout_date = obj.student_id.passedout_date

        if not months_paid:
            months_paid_list = []
        else:
            try:
                # Remove duplicates and convert months_paid_list to integers
                months_paid_list = list(map(int, set(map(str.strip, months_paid.split(',')))))
            except ValueError as e:
                print(f"Error converting months_paid to integers: {e}")
                months_paid_list = []

        # Calculate unpaid months
        unpaid_months = list(set(montharray) - set(months_paid_list))

        # Only show unpaid months if student hasn't passed out
        if unpaid_months and (not passedout_date or passedout_date >= current_date):
            return ",".join(map(str, unpaid_months))
        else:
            return "No unpaid months"



class TransportDefaulterReportAdmin(ExportMixin, admin.ModelAdmin):
    resource_class = TransportDefaulterResource
    # Define the fields to display in the admin list
    list_display = (
        'admission_no','student_name', 'class_no', 'section', 
        'route', 'destination', 'unpaid_months'
    )
    
    list_filter = (ClassFilter, YearFilter, BusRouteFilter, DestinationFilter)
    
    # Disable add, change, and delete permissions
    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    # Custom method to show the student's name
    def student_name(self, obj):
        return obj.student_id.student_name

    # Custom method to show the student's admission number
    def admission_no(self, obj):
        return obj.student_id.addmission_no

    # Custom method to show the student's class
    def class_no(self, obj):
        return obj.student_class

    # Custom method to show the student's section
    def section(self, obj):
        return obj.student_section

    # Custom method to show the route
    def route(self, obj):
        return obj.route

    # Custom method to show the destination
    def destination(self, obj):
        return obj.destination

    # # Custom method to show unpaid months
    def unpaid_months(self, obj):
        # Calculate the unpaid months
        current_date = datetime.now().date()
        year = self.get_year()
        montharray = get_months_array(year)

        months_paid = obj.months_paid
        passedout_date = obj.student_id.passedout_date

        if not months_paid:
            months_paid_list = []
        else:
            try:
                # Remove duplicates and convert months_paid_list to integers
                months_paid_list = list(map(int, set(map(str.strip, months_paid.split(',')))))
            except ValueError as e:
                print(f"Error converting months_paid to integers: {e}")
                months_paid_list = []

        # Calculate unpaid months
        unpaid_months = list(set(montharray) - set(months_paid_list))

        # Only show unpaid months if student hasn't passed out
        if unpaid_months and (not passedout_date or passedout_date >= current_date):
            return ",".join(map(str, unpaid_months))
        else:
            return "No unpaid months"

    
    # def changelist_view(self, request, extra_context=None):
    #     bus_route = request.GET.get('bus_route', '')
    #     destination = request.GET.get('destination', '')
    #     class_no = request.GET.get('class_no', '')

    #     year_choices = [str(year) for year in range(2024, 2017, -1)]
    #     extra_context = extra_context or {}
    #     extra_context['class_choices'] = CLASS_CHOICES
    #     extra_context['year_choices'] = year_choices
    #     extra_context['bus_route_choices'] = range(1, 21)
    #     extra_context['destination_choices'] = busfees_master.objects.values_list('destination', flat=True).distinct()
    #     extra_context['selected_bus_route'] = bus_route
    #     extra_context['selected_destination'] = destination
    #     extra_context['selected_class_no'] = class_no
      

    #     return super().changelist_view(request, extra_context=extra_context)
    # Override changelist_view to provide extra context for filters
    def changelist_view(self, request, extra_context=None):
        bus_route = request.GET.get('bus_route', '')
        destination = request.GET.get('destination', '')
        class_no = request.GET.get('class_no', '')
        year = request.GET.get('year', None)
        if year is None:
            year = self.get_year()

        year_choices = [str(year) for year in range(2024, 2017, -1)]
        extra_context = extra_context or {}
        extra_context['class_choices'] = CLASS_CHOICES
        extra_context['year_choices'] = year_choices
        extra_context['bus_route_choices'] = range(1, 21)
        extra_context['destination_choices'] = busfees_master.objects.values_list('destination', flat=True).distinct()
        extra_context['selected_bus_route'] = bus_route
        extra_context['selected_destination'] = destination
        extra_context['selected_class_no'] = class_no
        extra_context['selected_year'] = year
       

        return super().changelist_view(request, extra_context=extra_context)

    change_list_template = 'admin/transportdefaulter_change_list.html'

    def get_year(self):
        current_month = date.today().month
        return date.today().year if current_month >= 4 else date.today().year - 1
    
    # Modify get_search_results to return unique student IDs
    def get_search_results(self, request, queryset, search_term):
        year1 = request.GET.get('year', None)

        busno = request.GET.get('bus_route', None)
        destination = request.GET.get('destination', None)
        student_class = request.GET.get('class_no', None)
        if not busno and not year1 and not destination and not student_class:
            return queryset.none(), False
        year = int(year1) if year1 else self.get_year()
        current_date = datetime.now().date()
          # Get list of months for the year
        montharray = get_months_array(year)
        query = queryset.filter(
            year=year,
            bus_fees_paid__gt=0,
            student_id__bus_id__isnull=False
        )

        # print('query',query)

        route_subquery = RawSQL(
            "(SELECT route FROM busfees_master WHERE busfees_master.bus_id = student_master.bus_id)", []
        )

        destination_subquery = RawSQL(
            "(SELECT destination FROM busfees_master WHERE busfees_master.bus_id = student_master.bus_id)", []
        )

      
        query = query.annotate(
            route=RawSQL(
                "(SELECT route FROM busfees_master WHERE busfees_master.bus_id = student_master.bus_id)", []
            ),
            destination=RawSQL(
                "(SELECT destination FROM busfees_master WHERE busfees_master.bus_id = student_master.bus_id)", []
            ),
            # Avoid using GROUP_CONCAT in SQL here, as it might aggregate incorrectly
            months_paid=RawSQL(
                "(SELECT GROUP_CONCAT(TRIM(fees_period_month) ORDER BY CAST(fees_period_month AS UNSIGNED)) FROM student_fees WHERE student_fees.student_id = student_master.student_id AND student_fees.year = %s)",
                [year]
            )
        )


        if busno:
            query = query.filter(route=busno)

        if destination:
            query = query.filter(destination=destination)

        if student_class:
            query = query.filter(student_class=student_class)

        # Filter only students with unpaid months
        fees_records = []
        for data in query:
            months_paid = data.months_paid
            passedout_date = data.student_id.passedout_date

            if not months_paid:
                months_paid_list = []
            else:
                try:
                    months_paid_list = list(map(int, set(map(str.strip, months_paid.split(',')))))
                except ValueError:
                    months_paid_list = []

            unpaid_months = list(set(montharray) - set(months_paid_list))

            if unpaid_months and (not passedout_date or passedout_date >= current_date):
                fees_records.append(data.student_id.student_id)


        final_query = query.filter(student_id__in=fees_records).distinct()
        return final_query, False
    

admin.site.register(transport_defaulter, TransportDefaulterReportAdmin)


# class chequedepositreportAdmin(admin.ModelAdmin):

#     def get_search_results(self, request, queryset, search_term):
#         # Parse date range from user inputs
#         datefrom = request.GET.get('datefrom')
#         dateto = request.GET.get('dateto')

#         # Convert dates if they exist
#         if datefrom:
#             datefrom1 = datefrom  # Expecting date format: 'Y-m-d'
#         if dateto:
#             dateto1 = dateto

#         # Current year and session start (April 1st of the current year)
#         current_year = date.today().year
#         session_start = f"{current_year}-04-01"

#         # Filter queryset for cheque payments that are open and between the date range
#         queryset = queryset.filter(
#             payment_mode='cheque',
#             cheque_status='open',
#             date_payment__range=[datefrom1, dateto1]
#         ).values(
#             'bank_name', 'branch_name', 'cheq_no'
#         ).annotate(
#             amount_paid=Sum('amount_paid'),
#             student_name=Concat('student__student_name', output_field=CharField()),
#             mobile_no=F('student__mobile_no'),
#             admission_no=Concat('student__admission_no', output_field=CharField()),
#             student_class=Concat('student_class', output_field=CharField()),
#             student_section=Concat('student_section', output_field=CharField())
#         )

#         total_amount = 0
#         for chq in queryset:
#             total_amount += chq['amount_paid']

#         return queryset, total_amount
    
# from datetime import date
# from django.db.models import Sum, F
# from django.db.models.functions import Concat
# from django.db.models import CharField

# class chequedepositreportAdmin(admin.ModelAdmin):

#     def get_search_results(self, request, queryset, search_term):
#         # Parse date range from user inputs
#         datefrom = request.GET.get('datefrom')
#         dateto = request.GET.get('dateto')

#         # Set default values for date range if not provided
#         if datefrom:
#             datefrom1 = datefrom  # Expecting date format: 'Y-m-d'
#         else:
#             datefrom1 = '2024-04-01'  # Default start date (adjust as needed)

#         if dateto:
#             dateto1 = dateto
#         else:
#             dateto1 = date.today().strftime('%Y-%m-%d')  # Default end date is today

#         # Current year and session start (April 1st of the current year)
#         current_year = date.today().year
#         session_start = f"{current_year}-04-01"

#         # Filter queryset for cheque payments that are open and between the date range
#         queryset = queryset.filter(
#             payment_mode='cheque',
#             cheque_status='open',
#             date_payment__range=[datefrom1, dateto1]
#         ).values(
#             'bank_name', 'branch_name', 'cheq_no'
#         ).annotate(
#             amount_paid=Sum('amount_paid'),
#             student_name=Concat('student_id__student_name', output_field=CharField()),
#             mobile_no=F('student_id__mobile_no'),
#             admission_no=Concat('student_id__admission_no', output_field=CharField()),
#             student_class=Concat('student_class', output_field=CharField()),
#             student_section=Concat('student_section', output_field=CharField())
#         )

#         total_amount = 0
#         for chq in queryset:
#             total_amount += chq['amount_paid']

#         return queryset, total_amount


# from django.db.models import Sum, F
# from django.db.models import CharField

# class chequedepositreportAdmin(admin.ModelAdmin):

#     def get_search_results(self, request, queryset, search_term):
#         # Parse date range from user inputs
#         datefrom = request.GET.get('datefrom')
#         dateto = request.GET.get('dateto')

#         # Set default values for date range if not provided
#         if datefrom:
#             datefrom1 = datefrom  # Expecting date format: 'Y-m-d'
#         else:
#             datefrom1 = '2024-04-01'  # Default start date (adjust as needed)

#         if dateto:
#             dateto1 = dateto
#         else:
#             dateto1 = date.today().strftime('%Y-%m-%d')  # Default end date is today

#         # Current year and session start (April 1st of the current year)
#         current_year = date.today().year
#         session_start = f"{current_year}-04-01"

#         # Filter queryset for cheque payments that are open and between the date range
#         queryset = queryset.filter(
#             payment_mode='cheque',
#             cheque_status='open',
#             date_payment__range=[datefrom1, dateto1]
#         ).values(
#             'bank_name', 'branch_name', 'cheq_no'
#         ).annotate(
#             amount_paid=Sum('amount_paid'),
#             student_name=F('student_id__student_name'),  # Fetch student name without Concat
#             mobile_no=F('student_id__mobile_no'),
#             admission_no=F('student_id__addmission_no'),
#             student_class=F('student_class'),
#             student_section=F('student_section')
#         )

#         total_amount = 0
#         for chq in queryset:
#             print("chq['amount_paid']",chq['amount_paid'])
#             total_amount += int(chq['amount_paid'])

#         return queryset, total_amount
    
from datetime import date
from django.utils.html import format_html
# from django.contrib.postgres.aggregates import ArrayAgg
from django.db.models import Sum, F, Value, CharField, IntegerField
from django.db.models.functions import Concat, Coalesce
from collections import defaultdict


class chequedepositreportAdmin(admin.ModelAdmin):

    list_display = (
        'student_name','admission_no','student_class','student_section','phone_no','bank_name', 'branch_name', 'cheq_no','total_collection'
    )
    list_filter = ( DateFromFilter, DateToFilter)
     # Add your list display fields here
    # list_display = ('bank_name', 'branch_name', 'cheq_no', 'student_name', 'mobile_no', 'admission_no', 'student_class', 'student_section', 'cheque_status', 'amount_paid')
    
    # Specify which fields to link to change views
    # list_display_links = ('student_class',)

    # Add other relevant configurations
    # list_filter = ('bank_name', 'branch_name', 'cheque_status')
    # search_fields = ('student__student_name', 'student__mobile_no', 'cheq_no')
    change_list_template = "admin/chequedepositreport_change_list.html"  # Custom template for the change list

    # def get_search_results(self, request, queryset, search_term):
    #     # Parse date range from user inputs
    #     datefrom = request.GET.get('datefrom')
    #     dateto = request.GET.get('dateto')

    #     # Set default values for date range if not provided
    #     if datefrom:
    #         datefrom1 = datefrom  # Expecting date format: 'Y-m-d'
    #     else:
    #         datefrom1 = '2024-04-01'  # Default start date (adjust as needed)

    #     if dateto:
    #         dateto1 = dateto
    #     else:
    #         dateto1 = date.today().strftime('%Y-%m-%d')  # Default end date is today

    #     # Filter queryset for cheque payments that are open and between the date range
    #     # queryset = queryset.filter(
    #     #     payment_mode='cheque',
    #     #     cheque_status='open',
    #     #     date_payment__range=[datefrom1, dateto1]
    #     # ).values(
    #     #     'bank_name', 'branch_name', 'cheq_no'
    #     # ).annotate(
    #     #     # Safely aggregate numeric values, using Coalesce to handle nulls if necessary
    #     #     # amount_paid=Coalesce(Sum('amount_paid'), 0),
    #     #     amount_paid=Sum('amount_paid'),
    #     #     student_name=F('student_id__student_name'),
    #     #     mobile_no=F('student_id__mobile_no'),
    #     #     admission_no=F('student_id__addmission_no'),
    #     #     student_class=F('student_class'),
    #     #     student_section=F('student_section')
    #     # )

    #     queryset = queryset.filter(
    #         payment_mode='cheque',
    #         cheque_status='open',
    #         date_payment__range=[datefrom1, dateto1]
    #     ).values(
    #         'bank_name', 'branch_name', 'cheq_no'
    #     ).annotate(
    #         # Concatenate distinct student names
    #         student_names=ArrayAgg(
    #             F('student_id__student_name'), distinct=True, ordering=F('student_id__student_name').asc()
    #         ),
    #         # Aggregating and concatenating admission numbers
    #         admission_no=ArrayAgg(
    #             F('student_id__addmission_no'), distinct=True, ordering=F('student_id__addmission_no').asc()
    #         ),
    #         # Concatenate class and section without duplicates
    #         student_class=ArrayAgg(
    #             F('student_class'), distinct=True, ordering=F('student_class').asc()
    #         ),
    #         student_section=ArrayAgg(
    #             F('student_section'), distinct=True, ordering=F('student_section').asc()
    #         ),
    #         # Safely aggregate numeric values, using Coalesce to handle nulls if necessary
    #         amount_paid=Sum('amount_paid'),
    #         mobile_no=F('student_id__mobile_no')
    #     )

    #     # Calculate total amount
    #     # total_amount = queryset.aggregate(total=Coalesce(Sum('amount_paid'), 0))['total']
    #     total_amount = 0
    #     for chq in queryset:
    #         # print("chq['amount_paid']",chq['amount_paid'])
    #         total_amount += int(chq['amount_paid'])

    #     # Returning queryset and total amount for further rendering
    #     return queryset, total_amount

    def get_search_results(self, request, queryset, search_term):
        # Parse date range from user inputs
        datefrom = request.GET.get('datefrom')
        dateto = request.GET.get('dateto')

        # Set default values for date range if not provided
        if datefrom:
            datefrom1 = datefrom  # Expecting date format: 'Y-m-d'
        else:
            datefrom1 = '2024-04-01'  # Default start date (adjust as needed)

        if dateto:
            dateto1 = dateto
        else:
            dateto1 = date.today().strftime('%Y-%m-%d')  # Default end date is today

        # Filter queryset for cheque payments that are open and between the date range
        queryset = queryset.filter(
            payment_mode='cheque',
            cheque_status='open',
            date_payment__range=[datefrom1, dateto1]
        ).values(
            'bank_name', 'branch_name', 'cheq_no'
        ).annotate(
            # Concatenate admission numbers and student names
            admission_no=F('student_id__addmission_no'),
            student_name=F('student_id__student_name'),
            mobile_no=F('student_id__mobile_no'),
            student_class=F('student_class'),
            student_section=F('student_section'),
            # amount_paid=Sum('amount_paid')
            amount_paid=Sum(F('amount_paid'), output_field=IntegerField())
        )

        # Grouping using the same cheque number, bank, and branch, while concatenating student names
        queryset = queryset.annotate(
            student_names=Concat(
                F('student_name'),
                Value(', '),
                output_field=CharField()
            ),
            admission_nos=Concat(
                F('admission_no'),
                Value(', '),
                output_field=CharField()
            )
        )

        total_amount = queryset.aggregate(total_amount=Sum('amount_paid', output_field=IntegerField()))['total_amount']

        return queryset, total_amount
    

    def changelist_view(self, request, extra_context=None):
        # Call the parent method to get the default changelist view
        queryset, total_amount = self.get_search_results(request, self.model.objects.all(), search_term='')

        # context = {
        #     'cl': self.get_changelist(request)(self.model, self.admin_site),
        #     'total_amount': total_amount,
        # }
        extra_context = extra_context or {}
        # Store the request object in the instance
        
        # Get the filter values from GET parameters
        date_from = request.GET.get('date_from', '')
        date_to = request.GET.get('date_to', timezone.now().strftime('%Y-%m-%d'))

        # Pass filter values to the template to retain them
        extra_context['date_from'] = date_from
        extra_context['date_to'] = date_to
        extra_context['total_amount'] = total_amount
        return super().changelist_view(request, extra_context=extra_context)

    def total_collection(self, obj):
        # return format_html('<strong>{}</strong>', obj.amount_paid)
        return obj.amount_paid

    total_collection.short_description = 'Total Collection'

    def student_name(self, obj):
        # return format_html('<strong>{}</strong>', obj.amount_paid)
        return obj.student_id.student_name
    
    def admission_no(self, obj):
        # return format_html('<strong>{}</strong>', obj.amount_paid)
        return obj.student_id.addmission_no
    
    def phone_no(self, obj):
        # return format_html('<strong>{}</strong>', obj.amount_paid)
        return obj.student_id.mobile_no


admin.site.register(cheque_deposit, chequedepositreportAdmin)










