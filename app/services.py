from django.contrib import admin
from .models import (
    student_master, student_fee, student_class, specialfee_master,
    payment_schedule_master, latefee_master, fees_master, expense,
    concession_master, bus_master, busfees_master, account_head
)

from datetime import datetime
from django.shortcuts import get_object_or_404
from django.http import JsonResponse, HttpResponse
from datetime import datetime
from django.db import connection
from datetime import datetime
from django.db.models.functions import Lower
from datetime import datetime, timedelta
from django.utils.dateparse import parse_date
from django.db.models import Sum, F, Q

def last_payment_record( student_id=None):
    previous_fee = {}

    if student_id is not None:
        # Get the latest fee record excluding 'pending' and 'failed' cheque statuses
        stfees = (
            student_fee.objects.filter(student_id=student_id)
            .exclude(Q(cheque_status="pending") | Q(cheque_status="failed"))
            .order_by("-student_fee_id")
            .first()
        )

        if stfees:
            # Extract necessary fields
            fees_for_months = stfees.fees_for_months

            # Calculate sum_total_paid and admission_fees_paid for the same month, student, class, section, and year
            sum_total_paid_result = (
                student_fee.objects.filter(
                    fees_for_months=fees_for_months,
                    student_id=stfees.student_id,
                    student_class=stfees.student_class,
                    student_section=stfees.student_section,
                    year=stfees.year,
                )
                .exclude(
                    Q(cheque_status="pending")
                    | Q(cheque_status="failed")
                    | Q(cheque_status="Rejected")
                )
                .aggregate(
                    sum_total_paid=Sum("amount_paid"),
                    admission_fees_paid=Sum("admission_fees_paid"),
                )
            )

            sum_total_paid = (sum_total_paid_result["sum_total_paid"] or 0) - (
                sum_total_paid_result["admission_fees_paid"] or 0
            )

            # Convert string amounts to floats
            total_amount = float(stfees.total_amount or 0)
            paid_amount = float(stfees.amount_paid or 0)
            late_fee = float(stfees.late_fees_paid or 0)

            # Calculate the pending amount
            prev_pending_amount = (
                total_amount - paid_amount if total_amount > paid_amount else 0
            )

            # Check for differences in paid and remaining months
            paid_months = stfees.fees_period_month.split(", ")
            array_check = stfees.fees_for_months.split(",")

            remaining_months = list(set(paid_months) - set(array_check))
            tmpval = ",".join(remaining_months)

            # Build the previousFee dictionary
            previous_fee = {
                "fees_for_months": stfees.fees_for_months,
                "year": stfees.year,
                "date_payment": stfees.date_payment,
                "amount_paid": stfees.amount_paid,
                "fees_period_month": stfees.fees_period_month,
                "student_class": stfees.student_class,
                "student_section": stfees.student_section,
                "remaining_months": tmpval,
                "remarks": stfees.remarks,
                "student_fee_id": stfees.student_fee_id,
                "late_fee": late_fee,
                "prev_pending_amount": prev_pending_amount,
                "sum_total_paid": sum_total_paid,
            }

            # Check for cheque status and handle rejected case
            if stfees.payment_mode == "Cheque" and stfees.cheque_status == "Rejected":
                previous_fee["cheque_status"] = stfees.cheque_status

    return previous_fee


def fetch_fee_details_for_class( student_id, class_no):
    # Fetch the student information
    try:
        student = student_master.objects.get(student_id=student_id)
    except student_master.DoesNotExist:
        return []  # Return empty if student not found

    # Fetch the student class information
    student_class1 = student_class.objects.filter(
        student_id=student.student_id, class_no=class_no
    ).first()

    if not student_class1:
        return []  # Return empty if student class not found

    # Fetch fees details from fees_master based on the class and time period
    fees_detail = (
        fees_master.objects.filter(
            class_no=class_no,
            valid_from__lte=student_class1.started_on,
            valid_to__gte=student_class1.started_on,
        )
        .order_by("-fees_id")
        .first()
    )

    if not fees_detail:
        return []  # Return empty if no fee details found

    # Fetch the concession details if applicable
    concession = concession_master.objects.filter(
        concession_id=student.concession_id
    ).first()

    # Fetch bus fees details
    bus_fees = busfees_master.objects.filter(bus_id=student.bus_id).first()

    # Prepare the fee details response
    fee_details = {
        "student": student,
        "annual_fees": fees_detail.annual_fees if fees_detail else None,
        "tuition_fees": fees_detail.tuition_fees if fees_detail else None,
        "funds_fees": fees_detail.funds_fees if fees_detail else None,
        "sports_fees": fees_detail.sports_fees if fees_detail else None,
        "activity_fees": fees_detail.activity_fees if fees_detail else None,
        "activity_fees_mandatory": fees_detail.activity_fees_mandatory
        if fees_detail
        else None,
        "admission_fees": fees_detail.admission_fees if fees_detail else None,
        "security_fees": fees_detail.security_fees if fees_detail else None,
        "dayboarding_fees": fees_detail.dayboarding_fees if fees_detail else None,
        "miscellaneous_fees": fees_detail.miscellaneous_fees if fees_detail else None,
        "bus_id": bus_fees.bus_id if bus_fees else None,
        "bus_fees": bus_fees.bus_fees if bus_fees else None,
        "busfee_not_applicable_in_months": bus_fees.fee_not_applicable_in_months
        if bus_fees
        else None,
        "concession_percent": concession.concession_persent if concession else None,
        "concession_type": concession.concession_type if concession else None,
        "concession_amount": concession.concession_amount if concession else None,
        "concession_id": concession.concession_id if concession else None,
        "is_april_checked": concession.is_april_checked if concession else None,
    }

    # return [fee_details]
    return fee_details


def get_special_fee( student_id, year, quarter, fee_type):
    # Split the quarter string into an array of months
    quarter_months = quarter.split(",")

    # Build the Django ORM query to check if any month is in months_applicable_for field
    conditions = Q()
    for month in quarter_months:
        # FIND_IN_SET equivalent in Django ORM: look for a substring match
        conditions |= Q(months_applicable_for__icontains=month)

    # Query specialfee_master model
    results = (
        specialfee_master.objects.filter(
            student_id=student_id, year=year, fee_type=fee_type
        )
        .filter(conditions)
        .all()
    )

    # Initialize variables for the result
    bus_fee_by_month = {}
    last_found_fee = None

    # Process the results
    for row in results:
        if row.fee_type == "bus_fees":
            # Split the months_applicable_for into a list
            months_applicable_for = row.months_applicable_for.split(",")

            # Check if any month in the quarter matches the months_applicable_for
            for quarter_month in quarter_months:
                if quarter_month in months_applicable_for:
                    bus_fee_by_month[quarter_month] = row.amount
        else:
            # If it's not a bus fee, store the fee from the last found record
            last_found_fee = row.amount

    # Return the result based on fee type
    return bus_fee_by_month if fee_type == "bus_fees" else last_found_fee


def calculate_late_fee( amount, quarter, class_year, current_date, fee_type=None):
    # Convert current_date from string to datetime if it's a string
    if isinstance(current_date, str):
        current_date = datetime.strptime(current_date, "%Y-%m-%d")

    # Determine the correct year for the fee calculation
    year = int(class_year) + 1 if quarter == "1,2,3" else int(class_year)
    start_month, middle_month, end_month = map(
        int, quarter.split(",")
    )  # This converts `end_month` to an integer

    # Get current date components
    current_year = int(current_date.year)
    current_day = int(current_date.day)
    current_month = int(current_date.month)

    # Get the last day of the end month
    last_day_of_end_month = (datetime(year, end_month, 1) + timedelta(days=31)).replace(
        day=1
    ) - timedelta(days=1)

    # Print or use `last_day_of_end_month` as needed
    print("last_day_of_end_month", last_day_of_end_month)

    last_day_of_end_month = last_day_of_end_month.day

    late_fee = 0  # Default late fee

    if year == current_year and current_month == start_month and current_day >= 1:
        late_fee = 0  # No late fee for the first month of the quarter
    elif (
        year == current_year
        and current_month == end_month
        and 20 < current_day <= last_day_of_end_month
    ):
        # Late fee for the end month after 20th day
        late_fee = get_late_fee_from_db(amount, "82", "90", "fixed")
    elif year == current_year and start_month < current_month <= end_month:
        # Late fee per day calculation for months between start and end
        amount_per_day = get_late_fee_from_db(amount, "32", "82", "per day")
        start_date = datetime(year, middle_month, 1)
        end_date = datetime.strptime(current_date.strftime("%Y-%m-%d"), "%Y-%m-%d")
        days_late = (end_date - start_date).days + 1  # Days late calculation
        late_fee = amount_per_day * days_late  # Late fee based on days late
    else:
        # Late fee for payments after the quarter's end
        date_to_check = datetime(year, end_month, last_day_of_end_month).date()
        if date_to_check > current_date.date():
            late_fee = 0  # No late fee if paying in advance
        else:
            late_fee = get_late_fee_from_db(
                amount, "90", "till current date", "fixed"
            )

    return late_fee


def get_late_fee_from_db( amount, days_from, days_to, late_fee_type):
    # Fetch the "no charge" late fee record
    no_charge_late_fee_record = get_no_charge_late_fee_record()

    # Initialize the late fee to 0
    fee = 0
    no_charge_applicable = False

    # Check if a "no charge" late fee record exists and compare amount
    if no_charge_late_fee_record and isinstance(
        no_charge_late_fee_record.latefee, (int, float)
    ):
        no_charge_applicable_amount = float(no_charge_late_fee_record.latefee)
        if amount <= no_charge_applicable_amount:
            no_charge_applicable = True

    # If no "no charge" is applicable, proceed to check for the late fee records
    if not no_charge_applicable:
        if late_fee_type is None:
            # Query for records where latefee_type is null
            late_fee_record = latefee_master.objects.filter(
                days_from=days_from, days_to=days_to, latefee_type__isnull=True
            ).first()
        else:
            # Query for records where latefee_type matches the passed parameter
            late_fee_record = latefee_master.objects.filter(
                days_from=days_from, days_to=days_to, latefee_type=late_fee_type
            ).first()

        # Check if the record exists and set the fee
        if late_fee_record and isinstance(late_fee_record.latefee, (int, float)):
            fee = float(late_fee_record.latefee)

    return fee


def get_no_charge_late_fee_record():
    # Query to get the first record where latefee_type is 'no charge'
    return latefee_master.objects.filter(latefee_type="no charge").first()
