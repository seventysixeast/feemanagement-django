# Generated by Django 4.2.14 on 2024-08-07 11:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0012_remove_student_class_student_master'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student_class',
            name='class_no',
            field=models.CharField(default='', max_length=50),
        ),
        migrations.AlterField(
            model_name='student_class',
            name='section',
            field=models.CharField(default='', max_length=50),
        ),
    ]
