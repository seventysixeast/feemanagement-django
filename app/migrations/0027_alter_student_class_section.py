# Generated by Django 4.2.14 on 2024-08-22 12:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0026_alter_fees_master_security_fees'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student_class',
            name='section',
            field=models.CharField(choices=[('', 'Select the Section'), ('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D'), ('E', 'E'), ('F', 'F'), ('G', 'G'), ('H', 'H'), ('I', 'I'), ('J', 'J')], default='', max_length=50),
        ),
    ]
