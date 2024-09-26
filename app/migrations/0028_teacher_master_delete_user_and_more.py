# Generated by Django 4.2.14 on 2024-08-28 12:39

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0027_alter_student_class_section'),
    ]

    operations = [
        migrations.CreateModel(
            name='teacher_master',
            fields=[
                ('user_id', models.AutoField(primary_key=True, serialize=False)),
                ('user_name', models.CharField(max_length=200)),
                ('email', models.EmailField(max_length=200, unique=True)),
                ('mobile', models.CharField(max_length=15, validators=[django.core.validators.RegexValidator('^\\d+$', 'Enter a valid mobile number. Only digits are allowed.')])),
                ('role', models.CharField(choices=[('', 'Select Type'), ('admin', 'Admin'), ('superadmin', 'Super Admin')], default='', max_length=50)),
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
        migrations.DeleteModel(
            name='user',
        ),
        migrations.AlterField(
            model_name='bus_master',
            name='attendant_phone',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='bus_master',
            name='bus_attendant',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='bus_master',
            name='bus_conductor',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='bus_master',
            name='bus_driver',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='bus_master',
            name='bus_route',
            field=models.IntegerField(choices=[('', 'Please Select Route'), (1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5'), (6, '6'), (7, '7'), (8, '8'), (9, '9'), (10, '10'), (11, '11'), (12, '12'), (13, '13'), (14, '14'), (15, '15'), (16, '16'), (17, '17'), (18, '18'), (19, '19'), (20, '20')], default='', null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='bus_master',
            name='conductor_phone',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='bus_master',
            name='driver_phone',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='bus_master',
            name='internal',
            field=models.CharField(choices=[('', 'Select'), ('True', 'True'), ('False', 'False')], max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='student_class',
            name='student_id',
            field=models.IntegerField(null=True),
        ),
    ]