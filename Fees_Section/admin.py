from django.contrib import admin
from .models import (
    cheque_status
)

from app.models import (
    student_master, student_fee, student_class, specialfee_master,
    payment_schedule_master, latefee_master, fees_master, expense,
    concession_master, bus_master, busfees_master, account_head,generate_mobile_number_list
)

from django.utils.dateformat import DateFormat

from django.utils import timezone
# Register your models here.

# admin.site.register(cheque_status)
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

admin.site.register(cheque_status, ChequeStatusListAdmin)

# admin.site.register(transport)
