# Generated by Django 4.2.14 on 2024-08-06 13:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0007_alter_student_master_birth_date'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='student_master',
            name='bus_id',
        ),
        migrations.AddField(
            model_name='student_master',
            name='bus',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='app.busfees_master'),
        ),
    ]