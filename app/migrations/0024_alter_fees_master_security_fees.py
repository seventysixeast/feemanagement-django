# Generated by Django 4.2.14 on 2024-08-12 05:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0023_alter_fees_master_security_fees'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fees_master',
            name='security_fees',
            field=models.IntegerField(blank=True, default=0),
        ),
    ]
