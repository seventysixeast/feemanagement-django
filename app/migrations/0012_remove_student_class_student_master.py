# Generated by Django 4.2.14 on 2024-08-07 06:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0011_student_class_student_master'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='student_class',
            name='student_master',
        ),
    ]