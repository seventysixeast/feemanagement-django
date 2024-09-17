from django.db import models
from django.utils import timezone
from datetime import date
from django.core.validators import RegexValidator

# Validator that allows only digits
numeric_validator = RegexValidator(r'^\d+$', 'Enter a valid mobile number. Only digits are allowed.')

# Create your models here.

class account_head(models.Model):
  account_id = models.AutoField(primary_key=True)
  account_code = models.IntegerField(null=True, blank=True)
  parentaccount_id = models.IntegerField(null=True, blank=True)
  account_name = models.CharField(max_length=100, null=True, blank=True)
  account_desc = models.TextField(null=True, blank=True)

  class Meta:
    db_table = 'account_heads'  # Custom table name

  def __str__(self):
      return f"Account {self.account_id} - {self.account_name}"
  
class busfees_master(models.Model):
    bus_id = models.AutoField(primary_key=True)
    route = models.IntegerField(null=True, blank=True)  # Keeping it as IntegerField
    destination = models.CharField(max_length=100, null=True, blank=True)
    bus_fees = models.IntegerField(null=True, blank=True)
    fee_not_applicable_in_months = models.CharField(max_length=50, null=True, blank=True)

    class Meta:
        db_table = 'busfees_master'  # Custom table name

    def __str__(self):
        return f"Bus {self.bus_id} - Route {self.route} to {self.destination}"

    # Custom methods to fetch bus_driver and bus_attendant from bus_master
    @property
    def bus_driver(self):
        try:
            bus_master_instance = bus_master.objects.filter(bus_route=self.route).first()
            return bus_master_instance.bus_driver if bus_master_instance else None
        except bus_master.DoesNotExist:
            return None

    @property
    def bus_attendant(self):
        try:
            bus_master_instance = bus_master.objects.filter(bus_route=self.route).first()
            return bus_master_instance.bus_attendant if bus_master_instance else None
        except bus_master.DoesNotExist:
            return None
  
class bus_master(models.Model):
    BUS_CHOICES = [
      ('', 'Please Select Route'),
      (1, '1'),
      (2, '2'),
      (3, '3'),
      (4, '4'),
      (5, '5'),
      (6, '6'),
      (7, '7'),
      (8, '8'),
      (9, '9'),
      (10, '10'),
      (11, '11'),
      (12, '12'),
      (13, '13'),
      (14, '14'),
      (15, '15'),
      (16, '16'),
      (17, '17'),
      (18, '18'),
      (19, '19'),
      (20, '20'),
    ]
    INTERNAL_CHOICES = [
        ('', 'Select'),
        ('True', 'True'),
        ('False', 'False'),
    ]
    busdetail_id = models.AutoField(primary_key=True)
    bus_route = models.IntegerField(null=True, choices=BUS_CHOICES, default='',unique=True)
    internal = models.CharField(max_length=10, null=True, choices=INTERNAL_CHOICES)
    bus_driver = models.CharField(max_length=50, null=True)
    bus_conductor = models.CharField(max_length=50, null=True)
    bus_attendant = models.CharField(max_length=50, null=True)
    driver_phone = models.CharField(max_length=50, null=True)
    conductor_phone = models.CharField(max_length=50, null=True)
    attendant_phone = models.CharField(max_length=50, null=True)

    class Meta:
        db_table = 'bus_master'  # Custom table name

    def __str__(self):
        return f"BusDetail {self.busdetail_id} - Route {self.bus_route}"
  
class concession_master(models.Model):
  concession_id = models.AutoField(primary_key=True)
  concession_type = models.CharField(max_length=100)
  concession_persent = models.CharField(max_length=100)
  concession_amount = models.BigIntegerField(null=True, blank=True)
  is_april_checked = models.BooleanField(default=False)

  class Meta:
    db_table = 'concession_master'  # Custom table name

  def __str__(self):
      return f"Concession {self.concession_id}: {self.concession_type}"
  
class expense(models.Model):
  expense_id = models.AutoField(primary_key=True)
  account_id = models.IntegerField(null=True, blank=True)
  expense_desc = models.TextField(null=True, blank=True)
  expense_date = models.DateField(null=True, blank=True)
  amount = models.BigIntegerField(null=True, blank=True)
  paid_to = models.CharField(max_length=100, null=True, blank=True)

  class Meta:
    db_table = 'expenses'  # Custom table name

  def __str__(self):
      return f"Expense {self.expense_id}: {self.expense_desc or 'No Description'}"
  
class fees_master(models.Model):
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
  fees_id = models.AutoField(primary_key=True)
  class_no = models.CharField(max_length=50, choices=CLASS_CHOICES,default='')
  annual_fees = models.IntegerField()
  tuition_fees = models.IntegerField()
  funds_fees = models.IntegerField()
  sports_fees = models.IntegerField()
  activity_fees = models.IntegerField(null=True, blank=True)
  activity_fees_mandatory = models.BooleanField()
  admission_fees = models.IntegerField()
  security_fees = models.IntegerField(null=True, blank=True)
  dayboarding_fees = models.IntegerField()
  miscellaneous_fees = models.IntegerField(null=True, blank=True)
  valid_from = models.DateField(null=True, blank=True)
  valid_to = models.DateField(null=True, blank=True)

  class Meta:
    db_table = 'fees_master'  # Custom table name

  # def clean(self):
  #       super().clean()
  #       if fees_master.objects.filter(class_no=self.class_no, valid_from=self.valid_from, valid_to=self.valid_to).exists():
  #           raise ValidationError('A record with this class_no, valid_from, and valid_to already exists.')

  def save(self, *args, **kwargs):
    if not self.security_fees:
      self.security_fees = 0

    # self.clean()
    # super().save(*args, **kwargs)

class latefee_master(models.Model):
  latefee_id = models.BigAutoField(primary_key=True)
  days_from = models.CharField(max_length=20, null=True, blank=True)
  days_to = models.CharField(max_length=20, null=True, blank=True)
  latefee = models.IntegerField()
  latefee_type = models.CharField(max_length=50, null=True, blank=True)
  latefee_desc = models.CharField(max_length=200, null=True, blank=True)

  class Meta:
    db_table = 'latefee_master'  # Custom table name

  def __str__(self):
      return f"LateFee {self.latefee_id}: {self.latefee_desc}" 

class payment_schedule_master(models.Model):

  Fees_For_Month_CHOICES = [
        ('', 'Select Months'),
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
  fees_for_months = models.CharField(max_length=100)
  schedule_id = models.AutoField(primary_key=True)
  pay_in_month = models.CharField(max_length=50)
  payment_date = models.CharField(max_length=50)

  class Meta:
    db_table = 'payment_schedule_master'  # Custom table name

  def __str__(self):
      return f"Schedule {self.schedule_id} for {self.fees_for_months}"

class specialfee_master(models.Model):
  FEE_TYPE_CHOICES = [
    ('activity_fees', 'Activity Fees'),
    ('admission_fees', 'Admission Fees'),
    ('annual_fees', 'Annual Fees'),
    ('bus_fees', 'Bus Fees'),
    ('dayboarding_fees', 'Dayboarding Fees'),
    ('funds_fees', 'Funds Fees'),
    ('miscellaneous_fees', 'Miscellaneous Fees'),
    ('sports_fees', 'Sports Fees'),
    ('tuition_fees', 'Tuition Fees'),
    ('ignore_prev_outstanding_fees', 'Ignore Previous Outstanding Fees')
  ]
  student_charge_id = models.AutoField(primary_key=True)
  student_id = models.IntegerField()
  student_class_id = models.IntegerField()
  late_fee_applicable = models.BooleanField(default=False)
  fee_type = models.CharField(max_length=50, choices=FEE_TYPE_CHOICES, default='activity_fees')
  months_applicable_for = models.CharField(max_length=100, null=True)
  year = models.CharField(max_length=4, null=True, blank=True)
  amount = models.IntegerField(default=0)
  status = models.CharField(max_length=50, default='enabled')
  added_by = models.CharField(max_length=100, null=True, blank=True)
  added_at = models.DateTimeField(auto_now_add=True)
  updated_by = models.CharField(max_length=255, null=True, blank=True)
  updated_at = models.DateTimeField(auto_now=True)

  class Meta:
    db_table = 'specialfee_master'  # Custom table name

  def __str__(self):
      return f"Charge {self.student_charge_id} for Student ID {self.student_id}"
  

  
class student_master(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]
    CATEGORY_CHOICES = [
        ('ews', 'EWS'),
        ('obc', 'OBC'),
        ('general', 'General'),
        ('sc', 'SC'),
    ]
    STATUS_CHOICES = [
        ('current', 'Current'),
        ('passedout', 'Passed Out'),
    ]

    student_id = models.AutoField(primary_key=True)
    addmission_no = models.IntegerField(unique=True)
    student_name = models.CharField(max_length=50)
    father_name = models.CharField(max_length=50, null=True, blank=True)
    mother_name = models.CharField(max_length=50, null=True, blank=True)
    birth_date = models.DateField(null=True, blank=True,default=None)
    phone_no = models.CharField(max_length=50, null=True, blank=True)
    mobile_no = models.CharField(max_length=50, null=True, blank=True)
    aadhaar_no = models.CharField(max_length=50, null=True, blank=True)
    email = models.EmailField(max_length=50, null=True, blank=True)
    address = models.CharField(max_length=50, null=True, blank=True)
    city = models.CharField(max_length=50, null=True, blank=True)
    bus_id = models.IntegerField(null=True, blank=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True)
    admission_date = models.DateField(default=timezone.now)
    concession_id = models.IntegerField(null=True, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='current')
    category = models.CharField(max_length=7, choices=CATEGORY_CHOICES, default='general')
    passedout_date = models.DateField(null=True, blank=True)
    remarks = models.CharField(max_length=50, null=True, blank=True)

    class Meta:
        db_table = 'student_master'
        # abstract = True

    def __str__(self):
        return f"{self.student_name} ({self.addmission_no})"

    def save(self, *args, **kwargs):
        creating = self.pk is None
        super().save(*args, **kwargs)

class student_fee(models.Model):
  student_fee_id = models.BigAutoField(primary_key=True)
  # student_id = models.IntegerField()
  student_id = models.ForeignKey(student_master, on_delete=models.CASCADE, related_name='fees',db_column='student_id')
  student_class = models.CharField(max_length=20)
  student_section = models.CharField(max_length=1, null=True, blank=True)
  fees_for_months = models.CharField(max_length=20)
  fees_period_month = models.CharField(max_length=100)
  year = models.CharField(max_length=4, null=True, blank=True)
  bus_id = models.IntegerField(null=True, blank=True)
  annual_fees_paid = models.IntegerField(null=True, blank=True)
  tuition_fees_paid = models.IntegerField(null=True, blank=True)
  funds_fees_paid = models.IntegerField(null=True, blank=True)
  sports_fees_paid = models.IntegerField(null=True, blank=True)
  activity_fees = models.IntegerField(null=True, blank=True)
  admission_fees_paid = models.IntegerField(null=True, blank=True)
  security_paid = models.IntegerField(null=True, blank=True)
  late_fees_paid = models.IntegerField(null=True, blank=True)
  dayboarding_fees_paid = models.IntegerField(null=True, blank=True)
  miscellaneous_fees_paid = models.IntegerField(null=True, blank=True)
  bus_fees_paid = models.IntegerField(null=True, blank=True)
  date_payment = models.DateField(null=True, blank=True)
  payment_mode = models.CharField(max_length=50, null=True, blank=True)
  cheq_no = models.CharField(max_length=20, null=True, blank=True)
  bank_name = models.CharField(max_length=30, null=True, blank=True)
  concession_applied = models.FloatField(null=True, blank=True)
  concession_type_id = models.IntegerField(null=True, blank=True)
  total_amount = models.FloatField(null=True, blank=True)
  amount_paid = models.FloatField(null=True, blank=True)
  processing_fees_paid = models.FloatField(null=True, blank=True)
  txn_ref_number = models.CharField(max_length=50, null=True, blank=True)
  isdefault = models.CharField(max_length=10, null=True, blank=True)
  entry_date = models.DateField(null=True, blank=True)
  cheque_status = models.CharField(max_length=10, null=True, blank=True)
  realized_date = models.DateField(null=True, blank=True)
  branch_name = models.CharField(max_length=50, null=True, blank=True)
  # remarks = models.CharField(max_length=50)
  remarks = models.CharField(max_length=255, blank=True, null=True)
  txn_id = models.CharField(max_length=50, null=True, blank=True)
  txn_response_code = models.CharField(max_length=20, null=True, blank=True)
  txn_payment_mode = models.CharField(max_length=50, null=True, blank=True)
  # txn_status = models.CharField(max_length=10, null=True, blank=True)
  receipt_url = models.CharField(max_length=100, null=True, blank=True)
  added_by = models.CharField(max_length=255, null=True, blank=True)
  added_at = models.DateTimeField(auto_now_add=True)
  edited_by = models.CharField(max_length=255, null=True, blank=True)
  edited_at = models.DateTimeField(auto_now=True)

  class Meta:
    db_table = 'student_fees'  # Custom table name

  def __str__(self):
      return f"StudentFee {self.student_fee_id} for Student {self.student_id}"
  

  def get_student_name(self):
        return self.student_id.student_name  # assuming student_id is a ForeignKey to student_master

  get_student_name.short_description = 'Student Name'  # Set the column name in the admin view
  

  def get_addmission_no(self):
      return self.student_id.addmission_no  # Assuming `student_id` is a ForeignKey to student_master

  get_addmission_no.short_description = 'Admission No'  # Set the column name in the admin view

  # def save(self, *args, **kwargs):
  #       creating = self.pk is None
  #       super().save(*args, **kwargs)
  


class student_class(models.Model):
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

    student_class_id = models.AutoField(primary_key=True)
    student_id = models.IntegerField(null=True)
    # student_id = models.ForeignKey(student_master, on_delete=models.CASCADE, related_name='classes',db_column='student_id')
    # student = models.ForeignKey(student_master, on_delete=models.CASCADE, related_name='classes')
    class_no = models.CharField(max_length=50, choices=CLASS_CHOICES,default='')
    section = models.CharField(max_length=50, choices=SECTION,default='')
    started_on = models.DateField(null=True, blank=True)
    ended_on = models.DateField(null=True, blank=True)

    class Meta:
        db_table = 'student_classes'  # Custom table name

    def __str__(self):
        return f"Class {self.class_no} Section {self.section}"

# class user(models.Model):
class teacher_master(models.Model):
  ROLES_CHOICES = [
      ('', 'Select Type'),
      ('admin', 'Admin'),
      ('superadmin', 'Super Admin'),
  ]
  user_id = models.AutoField(primary_key=True)
  user_name = models.CharField(max_length=200)
  email = models.EmailField(max_length=200, unique=True)
  mobile = models.CharField(max_length=15, validators=[numeric_validator])
  # mobile = models.IntegerField(max_length=15)
  
  # password = models.CharField(max_length=255)
  role = models.CharField(max_length=50, choices=ROLES_CHOICES,default='')
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)
  otp = models.CharField(max_length=255, null=True, blank=True)
  otp_created_at = models.DateTimeField(null=True, blank=True)
  otp_verified = models.BooleanField(default=False)

  class Meta:
    db_table = 'users'  # Custom table name

  def __str__(self):
      return self.user_name
  
class generate_mobile_number_list(student_master):
  class Meta:
      proxy = True  # Use this model as a proxy for the original model


class cheque_status(student_master):
  class Meta:
      proxy = True  # Use this model as a proxy for the original model
