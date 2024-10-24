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
from django.template.loader import render_to_string
import os
from io import BytesIO
from django.conf import settings
from reportlab.pdfgen import canvas
from xhtml2pdf import pisa


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

def get_months_array(year):
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



# def generate_pdf(request, txn_id):
#     receipt_data = get_fee_receipt_details_common('txn_id', txn_id, is_txn=True)
#     return generate_pdf_common(receipt_data, txn_id, 'txn_id')


def generate_pdf2(request, student_fee_id):
    receipt_data = get_fee_receipt_details_common('student_fee_id', student_fee_id, is_txn=False)
    return generate_pdf_common(request,receipt_data, student_fee_id, 'student_fee_id')

def get_fee_receipt_details_common(identifier_type, identifier_value, is_txn):
    # Set up the filter depending on whether we are using txn_id or student_fee_id
    if identifier_type == 'txn_id':
        filter_params = {'txn_id': identifier_value}
    elif identifier_type == 'student_fee_id':
        filter_params = {'student_fee_id': identifier_value}  # 'id' is the Django ORM field name for primary key
    else:
        return {}

    # Query the database to get the relevant records
    fee_receipt_data = student_fee.objects.filter(**filter_params).select_related('student_id').order_by('-student_fee_id')

    # Check if we got any results
    if not fee_receipt_data.exists():
        return {}

    # Initialize the variables
    total_amount_paid = fee_receipt_data.aggregate(Sum('amount_paid'))['amount_paid__sum'] or 0
    months_paid = ['({}) {}'.format(fee.fees_period_month, fee.year) for fee in fee_receipt_data]

    # Take the first result to populate general student info
    first_receipt = fee_receipt_data.first()
    
    # Construct the receipt details
    fee_receipt_details = {
        'addmission_no': first_receipt.student_id.addmission_no,
        'student_name': first_receipt.student_id.student_name,
        'father_name': first_receipt.student_id.father_name,
        'mother_name': first_receipt.student_id.mother_name,
        'student_id': first_receipt.student_id.student_id,
        'student_class': first_receipt.student_class,
        'student_section': first_receipt.student_section,
        'year': first_receipt.year,
        'student_fee_id': first_receipt.student_fee_id,
        'txn_payment_mode': first_receipt.payment_mode,
        'receipt_number': first_receipt.txn_ref_number if is_txn else first_receipt.student_fee_id,
        'date_payment': first_receipt.date_payment,
        'remarks': first_receipt.remarks,
        'total_amount_paid': total_amount_paid,
        'months_paid': ', '.join(months_paid)  # Concatenate months and years
    }

    return fee_receipt_details


def generate_pdf_common(request,receipt_data, record_id, id_field):
    """
    Generates a PDF for the given record ID (either txn_id or student_fee_id) and updates the receipt URL in the database.
    
    Args:
        receipt_data (dict): Data to be included in the PDF.
        record_id (str/int): ID of the record (either txn_id or student_fee_id).
        id_field (str): Field name to filter the database records ('txn_id' or 'student_fee_id').
    
    Returns:
        JsonResponse: A response containing the success status and message.
    """
    response_data = {
        'success': False,
        'message': 'No records found for the given ID'
    }

    if receipt_data:
        # Prepare HTML content with the receipt data
        html_content = render_to_string('fee_receipt.html', receipt_data)

        # Create a BytesIO stream to hold the generated PDF
        pdf_file = BytesIO()
        pisa_status = pisa.CreatePDF(html_content, dest=pdf_file)

        if pisa_status.err:
            return JsonResponse({'success': False, 'message': 'Error generating PDF'})

        # Define the folder path where you want to store PDFs
        pdf_folder = os.path.join(settings.MEDIA_ROOT, 'pdfs')
        os.makedirs(pdf_folder, exist_ok=True)

        # File name and path
        pdf_filename = f'invoice_{record_id}.pdf'
        pdf_file_path = os.path.join(pdf_folder, pdf_filename)

        # Write the generated PDF to the file system
        with open(pdf_file_path, 'wb') as f:
            f.write(pdf_file.getvalue())

        # Generate the public URL to the PDF file
        pdf_url = f"{settings.MEDIA_URL}pdfs/{pdf_filename}"
        host_info = request.build_absolute_uri(settings.MEDIA_URL)

        # Update the `receipt_url` field in the database based on the id_field
        filter_params = {id_field: record_id}
        student_fees = student_fee.objects.filter(**filter_params)

        if student_fees.exists():
            student_fees.update(receipt_url=pdf_url)

            response_data = {
                'success': True,
                'receiptUrl': host_info + f'pdfs/{pdf_filename}',
                'message': f"Receipt URL updated successfully for {id_field}: {record_id}"
            }
        else:
            response_data = {
                'success': False,
                'message': f"No records found for {id_field}: {record_id}"
            }

    return JsonResponse(response_data)


# def generate_pdf_common(receipt_data, record_id, id_field):
#     """
#     Generates a PDF for the given record ID (either txn_id or student_fee_id) and updates the receipt URL in the database.
    
#     Args:
#         receipt_data (dict): Data to be included in the PDF.
#         record_id (str/int): ID of the record (either txn_id or student_fee_id).
#         id_field (str): Field name to filter the database records ('txn_id' or 'student_fee_id').
    
#     Returns:
#         JsonResponse: A response containing the success status and message.
#     """
#     response_data = {
#         'success': False,
#         'message': 'No records found for the given ID'
#     }

#     if receipt_data:
#         # Create a new PDF in memory
#         buffer = BytesIO()
#         pdf = canvas.Canvas(buffer)

#         # Set PDF meta-data
#         pdf.setTitle('Invoice')

#         # Define the content and structure for the PDF
#         pdf.drawString(100, 800, "Shishu Niketan Public School")
#         pdf.drawString(100, 780, "FEE RECEIPT")
#         pdf.drawString(100, 760, f"Year: {receipt_data['year']}")
#         pdf.drawString(100, 740, f"Receipt: {receipt_data['receipt_number']}")
#         pdf.drawString(100, 720, f"Transaction ID: {record_id}")
#         pdf.drawString(100, 700, f"Admission No.: {receipt_data['addmission_no']}")
#         pdf.drawString(100, 680, f"Student Name: {receipt_data['student_name']}")
#         pdf.drawString(100, 660, f"Father's Name: {receipt_data['father_name']}")
#         pdf.drawString(100, 640, f"Mother's Name: {receipt_data['mother_name']}")
#         pdf.drawString(100, 620, f"Class: {receipt_data['student_class']}")
#         pdf.drawString(100, 600, f"Payment Mode: {receipt_data['txn_payment_mode']}")
#         pdf.drawString(100, 580, f"Paid for Session (Months): {receipt_data['months_paid']}")
#         pdf.drawString(100, 560, f"Total Fees Paid: {receipt_data['total_amount_paid']}")
#         pdf.drawString(100, 540, f"Remarks: {receipt_data['remarks']}")

#         # Footer
#         pdf.drawString(100, 520, "Copyright © shishuniketanmohali.org.in - All Rights Reserved.")

#         # Save the PDF into the buffer
#         pdf.showPage()
#         pdf.save()

#         # Move buffer to the beginning
#         buffer.seek(0)

#         # Define the folder path where you want to store PDFs
#         pdf_folder = os.path.join(settings.MEDIA_ROOT, 'pdfs')

#         # Create the folder if it does not exist
#         if not os.path.exists(pdf_folder):
#             os.makedirs(pdf_folder)

#         # File name and path
#         pdf_filename = f'invoice_{record_id}.pdf'
#         pdf_file_path = os.path.join(pdf_folder, pdf_filename)

#         # Write PDF data to the file
#         with open(pdf_file_path, 'wb') as f:
#             f.write(buffer.read())

#         # Build the file URL (using MEDIA_URL for serving static media)
#         pdf_url = f"{settings.MEDIA_URL}pdfs/{pdf_filename}"

#         # Update the `receipt_url` field in the database based on the id_field
#         filter_params = {id_field: record_id}
#         student_fees = student_fee.objects.filter(**filter_params)

#         if student_fees.exists():
#             student_fees.update(receipt_url=pdf_url)

#             response_data = {
#                 'success': True,
#                 'receiptUrl': pdf_url,
#                 'message': f"Receipt URL updated successfully for {id_field}: {record_id}"
#             }
#         else:
#             response_data = {
#                 'success': False,
#                 'message': f"No records found for {id_field}: {record_id}"
#             }

#     return JsonResponse(response_data)




# def action_generate_pdf(request, txn_id):
#     # Fetch receipt data based on txn_id
#     # receipt_data = get_fee_receipt_details(txn_id)  # Function to fetch the data
#     receipt_data = get_fee_receipt_details(txn_id)

#     if receipt_data:
#         # Prepare HTML content with the receipt data
#         html_content = render_to_string('fee_receipt.html', {
#             'addmission_no': receipt_data['addmission_no'],
#             'student_name': receipt_data['student_name'],
#             'father_name': receipt_data['father_name'],
#             'mother_name': receipt_data['mother_name'],
#             'student_class': receipt_data['student_class'],
#             'receipt_number': receipt_data['receipt_number'],
#             'date_payment': receipt_data['date_payment'],
#             'year': receipt_data['year'],
#             'txn_id': receipt_data['txn_id'],
#             'txn_payment_mode': receipt_data['txn_payment_mode'],
#             'months_paid': receipt_data['months_paid'],
#             'total_amount_paid': receipt_data['total_amount_paid'],
#             'remarks': receipt_data['remarks'],
#         })

#         # Create a BytesIO stream to hold the generated PDF
#         pdf_file = BytesIO()
#         pisa_status = pisa.CreatePDF(html_content, dest=pdf_file)

#         # Define the path to save the PDF
#         pdf_folder_path = os.path.join(settings.MEDIA_ROOT, 'pdfs/')
#         os.makedirs(pdf_folder_path, exist_ok=True)
#         pdf_file_path = os.path.join(pdf_folder_path, f'invoice_{txn_id}.pdf')

#         # Save the generated PDF to the specified path
#         with open(pdf_file_path, 'wb') as f:
#             f.write(pdf_file.getvalue())

#         # Generate the public URL to the PDF file
#         pdf_file_url = os.path.join(settings.MEDIA_URL, f'pdfs/invoice_{txn_id}.pdf')
#         host_info = request.build_absolute_uri(settings.MEDIA_URL)

#         # Find the student fee record and update the receipt_url field
#         student_fees = student_fee.objects.filter(txn_id=txn_id)
#         if student_fees.exists():
#             for fee in student_fees:
#                 fee.receipt_url = pdf_file_url
#                 fee.save()

#             # Return a success response with the PDF URL
#             response = {
#                 'success': True,
#                 'receiptUrl': host_info + f'pdfs/invoice_{txn_id}.pdf',
#                 'message': f"Receipt URL updated successfully for txn_id: {txn_id}",
#             }
#         else:
#             response = {
#                 'success': False,
#                 'message': 'No records found for the given transaction id',
#             }
#     else:
#         response = {
#             'success': False,
#             'message': 'No records found for the given transaction id',
#         }

#     return (response)