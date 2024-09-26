# Generated by Django 4.2.14 on 2024-08-07 13:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0013_alter_student_class_class_no_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='student_class',
            name='student_id',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='student_master',
            name='class_no',
            field=models.CharField(default='', max_length=50),
        ),
        migrations.AddField(
            model_name='student_master',
            name='section',
            field=models.CharField(default='', max_length=50),
        ),
    ]