from django.contrib import admin
from .models import (
    transport, tuition_fees_defaulter
)

from app.models import (
    user, student_master, student_fee, student_class, specialfee_master,
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

from django.db.models import F, Value, CharField, ExpressionWrapper, Q
from django.db.models.functions import Coalesce
from django.db.models import DecimalField

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
        extra_context['class_filter'] = self.CLASS_CHOICES
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

# from django.contrib import admin
# from .models import TuitionFeesDefaulter, student_master, student_classes
# from datetime import date
# from django.db.models import F, Value, CharField
# from django.db.models.functions import Concat

# class TuitionFeesDefaulterAdmin(admin.ModelAdmin):
#     list_display = ('student_name', 'admission_no', 'class_no', 'section', 'tmpval')
    
#     def get_year(self):
#         current_month = date.today().month
#         return date.today().year if current_month >= 4 else date.today().year - 1

#     def get_queryset(self, request):
#         # Current year
#         year = self.get_year()
#         # Get months for the year
#         montharray = self.get_months_array(year)
#         months_str = ','.join(map(str, montharray))

#         # Build the queryset based on the logic in the PHP code
#         queryset = super().get_queryset(request)
#         queryset = queryset.filter(year=year).annotate(
#             months_paid=Concat(
#                 'fees_period_month', output_field=CharField()
#             ),
#             tmpval=Value('', output_field=CharField())  # Placeholder for tmpval logic
#         )
        
#         # Filter queryset
#         queryset = queryset.annotate(
#             months_diff=Value(months_str, output_field=CharField())
#         ).filter(
#             # Apply filtering logic for defaulters
#             tuition_fees_paid__gt=0,
#             funds_fees_paid__gt=0,
#             sports_fees_paid__gt=0,
#         ).exclude(
#             months_paid=F('months_diff')
#         )

#         return queryset

#     # def get_months_array(self, year):
#     #     # Returns months array similar to PHP function
#     #     month_array = []
#     #     current_month = date.today().month
#     #     current_year = date.today().year

#     #     for i in range(1, 13):
#     #         if current_year == year and i > current_month:
#     #             break
#     #         month_array.append(i)
        
#     #     return month_array
    
#     def get_months_array(self, year):
#         start_date = date(year, 4, 1)
#         end_date = date(year + 1, 3, 31)
#         current_date = date.today()

#         months = []
#         time = start_date

#         if current_date < end_date:
#             end_date = current_date

#         while time <= end_date:
#             months.append(time.month)
#             next_month = (time.month % 12) + 1
#             next_year = time.year + (1 if next_month == 1 else 0)
#             time = date(next_year, next_month, 1)

#         return months

#     def student_name(self, obj):
#         return obj.student_master.student_name

#     def admission_no(self, obj):
#         return obj.student_master.admission_no

#     def class_no(self, obj):
#         return obj.student_class.class_no

#     def section(self, obj):
#         return obj.student_class.section

#     def tmpval(self, obj):
#         # Placeholder for tmpval logic, to be implemented based on months diff
#         # You can compute the missing months logic here
#         return obj.tmpval






class TuitionFeesDefaulterAdmin(admin.ModelAdmin):
    list_display = ('student_name', 'admission_no', 'class_no', 'section', 'tmpval')
    
    def get_year(self, request):
        # Determine the current financial year based on today's date
        current_month = date.today().month
        return date.today().year if current_month >= 4 else date.today().year - 1
    

    change_list_template = 'admin/tuitionfeesdefaulter_change_list.html'

    # Pass context to the changelist view to include class choices and year range
    def changelist_view(self, request, extra_context=None):
        # Define year choices from 2024 to 2018
        year_choices = [str(year) for year in range(2024, 2017, -1)]
        
        # Provide class choices and year choices to the template context
        extra_context = extra_context or {}
        extra_context['class_choices'] = CLASS_CHOICES
        extra_context['year_choices'] = year_choices
        
        return super().changelist_view(request, extra_context=extra_context)


    def get_queryset(self, request):
        # Get the current year and month array
        year = self.get_year(request)
        month_array = self.get_months_array(year)
        months_str = ','.join(map(str, month_array))
        print('months_str',months_str)
        # Build the queryset based on the logic in the PHP code
        queryset = super().get_queryset(request)

        # Using ExpressionWrapper to handle combined fees check
        total_fees_paid = ExpressionWrapper(
            Coalesce(F('tuition_fees_paid'), 0) +
            Coalesce(F('funds_fees_paid'), 0) +
            Coalesce(F('sports_fees_paid'), 0),
            output_field=DecimalField()
        )

        queryset = queryset.annotate(
            total_fees_paid=total_fees_paid,  # Annotate the total fees paid
        ).filter(
            year=year
        ).filter(
            Q(total_fees_paid__gt=0)  # Only include students who have paid fees greater than 0
        )

        # Annotate the months_paid using GROUP_CONCAT
        # Ensure GROUP_CONCAT is used properly in the RawSQL and align with MySQL's requirements
        queryset = queryset.annotate(
            # months_paid=RawSQL(
            #     """
            #     SELECT GROUP_CONCAT(DISTINCT fees_period_month ORDER BY fees_period_month SEPARATOR ', ')
            #     FROM student_fees AS sf
            #     WHERE sf.student_id = student_fees.student_id
            #     AND sf.year = %s
            #     """, (year,)
            # ),
            months_paid=RawSQL(
                """
                SELECT GROUP_CONCAT(DISTINCT TRIM(sf.fees_period_month) ORDER BY sf.fees_period_month+0 SEPARATOR ', ')
                FROM student_fees AS sf
                WHERE sf.student_id = student_fees.student_id
                AND sf.year = %s
                """, (year,)
            ),
            # Assuming the foreign key is student_id, use double underscore to access related fields
            student_name=F('student_id__student_name'),  
            admission_no=F('student_id__addmission_no'),  
            class_no=F('student_class'),  # Since student_class is a CharField, reference it directly
            section=F('student_section'),  # student_section field assumed as CharField or directly from the model
            passedout_date=F('student_id__passedout_date'),  # Assuming this comes from a related model
            tmpval=Value('', output_field=CharField())  # Placeholder for tmpval logic
        ).exclude(
            months_paid=months_str  # Exclude students who have paid for all months
        )

        # Optionally filter by class if a class is selected
        class_no = request.GET.get('class_no')
        if class_no:
            queryset = queryset.filter(class_no=class_no)

        # Filter passed-out students if needed (assuming radioval is passed as a query parameter)
        radioval = request.GET.get('radioval', 'withpassedout')
        queryset = self.filter_passed_out_students(queryset, radioval)

        # Update tmpval for each student
        for obj in queryset:
            # print('obj.months_paid',obj.months_paid)
            obj.tmpval = self.calculate_unpaid_months(obj.months_paid, month_array)
            # print('obj.tmpval',obj.tmpval)

        return queryset
        # filtered_queryset = []
        # for obj in queryset:
        #     obj.tmpval = self.calculate_unpaid_months(obj.months_paid, month_array)
        #     if obj.tmpval:  # Only include objects where tmpval is not an empty string
        #         filtered_queryset.append(obj)

        # return filtered_queryset

    def get_months_array(self, year):
        # Create an array of months based on the year
        start_date = date(year, 4, 1)  # Start from April 1st of the financial year
        end_date = date(year + 1, 3, 31)  # Till March 31st of the next year
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

    def calculate_unpaid_months(self, paid_months, months_array):
        # Calculate unpaid months by comparing paid months with the full year/month array
        paid_months_list = list(map(int, paid_months.split(',')))
        # print('paid_months_list',paid_months_list)
        unpaid_months = set(months_array) - set(paid_months_list)
        # print('unpaid_months',unpaid_months)
        return ','.join(map(str, sorted(unpaid_months)))

    def filter_passed_out_students(self, queryset, radioval):
        # Filter passed-out students if required
        current_date = date.today()
        if radioval != 'withpassedout':
            queryset = queryset.exclude(passedout_date__lt=current_date)
        return queryset

    # Display functions for fields
    def student_name(self, obj):
        return obj.student_name

    def admission_no(self, obj):
        return obj.admission_no

    def class_no(self, obj):
        return obj.class_no

    def section(self, obj):
        return obj.section

    def tmpval(self, obj):
        return obj.tmpval


admin.site.register(tuition_fees_defaulter, TuitionFeesDefaulterAdmin)

# admin.site.register(tuition_fees_defaulter, TuitionFeesDefaulterAdmin)


# admin.site.register(tuition_fees_defaulter)

