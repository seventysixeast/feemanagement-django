# Generated by Django 4.2.14 on 2024-08-01 13:14

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='account_head',
            fields=[
                ('account_id', models.AutoField(primary_key=True, serialize=False)),
                ('account_code', models.IntegerField(blank=True, null=True)),
                ('parentaccount_id', models.IntegerField(blank=True, null=True)),
                ('account_name', models.CharField(blank=True, max_length=100, null=True)),
                ('account_desc', models.TextField(blank=True, null=True)),
            ],
            options={
                'db_table': 'account_heads',
            },
        ),
        migrations.CreateModel(
            name='bus_master',
            fields=[
                ('busdetail_id', models.AutoField(primary_key=True, serialize=False)),
                ('bus_route', models.IntegerField(blank=True, null=True)),
                ('bus_driver', models.CharField(blank=True, max_length=50, null=True)),
                ('bus_conductor', models.CharField(blank=True, max_length=50, null=True)),
                ('bus_attendant', models.CharField(blank=True, max_length=50, null=True)),
                ('driver_phone', models.CharField(blank=True, max_length=50, null=True)),
                ('conductor_phone', models.CharField(blank=True, max_length=50, null=True)),
                ('attendant_phone', models.CharField(blank=True, max_length=50, null=True)),
                ('internal', models.CharField(blank=True, max_length=10, null=True)),
            ],
            options={
                'db_table': 'bus_master',
            },
        ),
        migrations.CreateModel(
            name='busfees_master',
            fields=[
                ('bus_id', models.AutoField(primary_key=True, serialize=False)),
                ('route', models.IntegerField(blank=True, null=True)),
                ('destination', models.CharField(blank=True, max_length=50, null=True)),
                ('bus_fees', models.IntegerField(blank=True, null=True)),
                ('fee_not_applicable_in_months', models.CharField(blank=True, max_length=50, null=True)),
            ],
            options={
                'db_table': 'busfees_master',
            },
        ),
        migrations.CreateModel(
            name='concession_master',
            fields=[
                ('concession_id', models.AutoField(primary_key=True, serialize=False)),
                ('concession_type', models.CharField(max_length=100)),
                ('concession_persent', models.CharField(max_length=100)),
                ('concession_amount', models.BigIntegerField(blank=True, null=True)),
                ('is_april_checked', models.BooleanField(default=False)),
            ],
            options={
                'db_table': 'concession_master',
            },
        ),
        migrations.CreateModel(
            name='expense',
            fields=[
                ('expense_id', models.AutoField(primary_key=True, serialize=False)),
                ('account_id', models.IntegerField(blank=True, null=True)),
                ('expense_desc', models.TextField(blank=True, null=True)),
                ('expense_date', models.DateField(blank=True, null=True)),
                ('amount', models.BigIntegerField(blank=True, null=True)),
                ('paid_to', models.CharField(blank=True, max_length=100, null=True)),
            ],
            options={
                'db_table': 'expenses',
            },
        ),
        migrations.CreateModel(
            name='fees_master',
            fields=[
                ('fees_id', models.AutoField(primary_key=True, serialize=False)),
                ('class_no', models.CharField(max_length=11)),
                ('annual_fees', models.IntegerField()),
                ('tuition_fees', models.IntegerField()),
                ('funds_fees', models.IntegerField()),
                ('sports_fees', models.IntegerField()),
                ('activity_fees', models.IntegerField(blank=True, null=True)),
                ('activity_fees_mandatory', models.BooleanField()),
                ('admission_fees', models.IntegerField()),
                ('security_fees', models.IntegerField()),
                ('dayboarding_fees', models.IntegerField()),
                ('miscellaneous_fees', models.IntegerField(blank=True, null=True)),
                ('valid_from', models.DateField(blank=True, null=True)),
                ('valid_to', models.DateField(blank=True, null=True)),
            ],
            options={
                'db_table': 'fees_master',
            },
        ),
        migrations.CreateModel(
            name='latefee_master',
            fields=[
                ('latefee_id', models.BigAutoField(primary_key=True, serialize=False)),
                ('days_from', models.CharField(blank=True, max_length=20, null=True)),
                ('days_to', models.CharField(blank=True, max_length=20, null=True)),
                ('latefee', models.IntegerField()),
                ('latefee_type', models.CharField(blank=True, max_length=50, null=True)),
                ('latefee_desc', models.CharField(blank=True, max_length=200, null=True)),
            ],
            options={
                'db_table': 'latefee_master',
            },
        ),
        migrations.CreateModel(
            name='payment_schedule_master',
            fields=[
                ('schedule_id', models.AutoField(primary_key=True, serialize=False)),
                ('fees_for_months', models.CharField(max_length=100)),
                ('pay_in_month', models.CharField(max_length=50)),
                ('payment_date', models.CharField(max_length=50)),
            ],
            options={
                'db_table': 'payment_schedule_master',
            },
        ),
        migrations.CreateModel(
            name='specialfee_master',
            fields=[
                ('student_charge_id', models.AutoField(primary_key=True, serialize=False)),
                ('student_id', models.IntegerField()),
                ('student_class_id', models.IntegerField()),
                ('late_fee_applicable', models.BooleanField(default=False)),
                ('fee_type', models.CharField(blank=True, max_length=50, null=True)),
                ('months_applicable_for', models.CharField(blank=True, max_length=100, null=True)),
                ('year', models.CharField(blank=True, max_length=4, null=True)),
                ('amount', models.IntegerField(default=0)),
                ('status', models.CharField(default='enabled', max_length=50)),
                ('added_by', models.CharField(blank=True, max_length=100, null=True)),
                ('added_at', models.DateTimeField(auto_now_add=True)),
                ('updated_by', models.CharField(blank=True, max_length=255, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'specialfee_master',
            },
        ),
        migrations.CreateModel(
            name='student_class',
            fields=[
                ('student_class_id', models.AutoField(primary_key=True, serialize=False)),
                ('student_id', models.IntegerField(blank=True, null=True)),
                ('class_no', models.CharField(blank=True, max_length=50, null=True)),
                ('section', models.CharField(blank=True, max_length=50, null=True)),
                ('started_on', models.DateField(blank=True, null=True)),
                ('ended_on', models.DateField(blank=True, null=True)),
            ],
            options={
                'db_table': 'student_classes',
            },
        ),
        migrations.CreateModel(
            name='student_fee',
            fields=[
                ('student_fee_id', models.BigAutoField(primary_key=True, serialize=False)),
                ('student_id', models.IntegerField()),
                ('student_class', models.CharField(max_length=20)),
                ('student_section', models.CharField(blank=True, max_length=1, null=True)),
                ('fees_for_months', models.CharField(max_length=20)),
                ('fees_period_month', models.CharField(max_length=50)),
                ('year', models.CharField(blank=True, max_length=4, null=True)),
                ('bus_id', models.IntegerField(blank=True, null=True)),
                ('annual_fees_paid', models.IntegerField(blank=True, null=True)),
                ('tuition_fees_paid', models.IntegerField(blank=True, null=True)),
                ('funds_fees_paid', models.IntegerField(blank=True, null=True)),
                ('sports_fees_paid', models.IntegerField(blank=True, null=True)),
                ('activity_fees', models.IntegerField(blank=True, null=True)),
                ('admission_fees_paid', models.IntegerField(blank=True, null=True)),
                ('security_paid', models.IntegerField(blank=True, null=True)),
                ('late_fees_paid', models.IntegerField(blank=True, null=True)),
                ('dayboarding_fees_paid', models.IntegerField(blank=True, null=True)),
                ('miscellaneous_fees_paid', models.IntegerField(blank=True, null=True)),
                ('bus_fees_paid', models.IntegerField(blank=True, null=True)),
                ('date_payment', models.DateField(blank=True, null=True)),
                ('payment_mode', models.CharField(blank=True, max_length=50, null=True)),
                ('cheq_no', models.CharField(blank=True, max_length=20, null=True)),
                ('bank_name', models.CharField(blank=True, max_length=30, null=True)),
                ('concession_applied', models.FloatField(blank=True, null=True)),
                ('concession_type_id', models.IntegerField(blank=True, null=True)),
                ('total_amount', models.FloatField(blank=True, null=True)),
                ('amount_paid', models.FloatField(blank=True, null=True)),
                ('processing_fees_paid', models.FloatField(blank=True, null=True)),
                ('txn_ref_number', models.CharField(blank=True, max_length=50, null=True)),
                ('isdefault', models.CharField(blank=True, max_length=10, null=True)),
                ('entry_date', models.DateField(blank=True, null=True)),
                ('cheque_status', models.CharField(blank=True, max_length=10, null=True)),
                ('realized_date', models.DateField(blank=True, null=True)),
                ('branch_name', models.CharField(blank=True, max_length=50, null=True)),
                ('remarks', models.CharField(max_length=50)),
                ('txn_id', models.CharField(blank=True, max_length=50, null=True)),
                ('txn_response_code', models.CharField(blank=True, max_length=20, null=True)),
                ('txn_payment_mode', models.CharField(blank=True, max_length=50, null=True)),
                ('receipt_url', models.CharField(blank=True, max_length=100, null=True)),
                ('added_by', models.CharField(blank=True, max_length=255, null=True)),
                ('added_at', models.DateTimeField(auto_now_add=True)),
                ('edited_by', models.CharField(blank=True, max_length=255, null=True)),
                ('edited_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'student_fees',
            },
        ),
        migrations.CreateModel(
            name='student_master',
            fields=[
                ('student_id', models.AutoField(primary_key=True, serialize=False)),
                ('addmission_no', models.IntegerField()),
                ('student_name', models.CharField(max_length=50)),
                ('father_name', models.CharField(max_length=50)),
                ('mother_name', models.CharField(max_length=50)),
                ('birth_date', models.DateField(blank=True, null=True)),
                ('phone_no', models.CharField(blank=True, max_length=50, null=True)),
                ('mobile_no', models.CharField(blank=True, max_length=50, null=True)),
                ('aadhaar_no', models.CharField(blank=True, max_length=50, null=True)),
                ('email', models.EmailField(blank=True, max_length=50, null=True)),
                ('address', models.CharField(blank=True, max_length=50, null=True)),
                ('city', models.CharField(blank=True, max_length=50, null=True)),
                ('bus_id', models.IntegerField(blank=True, null=True)),
                ('gender', models.CharField(choices=[('M', 'Male'), ('F', 'Female'), ('O', 'Other')], max_length=1)),
                ('admission_date', models.DateField()),
                ('concession_id', models.IntegerField(blank=True, null=True)),
                ('status', models.CharField(choices=[('current', 'Current'), ('alumni', 'Alumni'), ('dropped', 'Dropped')], default='current', max_length=7)),
                ('category', models.CharField(choices=[('general', 'General'), ('obc', 'OBC'), ('sc', 'SC'), ('st', 'ST')], default='general', max_length=7)),
                ('passedout_date', models.DateField(blank=True, null=True)),
                ('remarks', models.CharField(blank=True, max_length=50, null=True)),
            ],
            options={
                'db_table': 'student_master',
            },
        ),
        migrations.CreateModel(
            name='user',
            fields=[
                ('user_id', models.AutoField(primary_key=True, serialize=False)),
                ('user_name', models.CharField(max_length=200)),
                ('email', models.EmailField(max_length=200, unique=True)),
                ('mobile', models.CharField(max_length=15)),
                ('password', models.CharField(max_length=255)),
                ('role', models.CharField(max_length=50)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('otp', models.CharField(blank=True, max_length=255, null=True)),
                ('otp_created_at', models.DateTimeField(blank=True, null=True)),
                ('otp_verified', models.BooleanField(default=False)),
            ],
            options={
                'db_table': 'users',
            },
        ),
    ]
