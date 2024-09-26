# Generated by Django 4.2.14 on 2024-08-07 13:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0014_student_class_student_id_student_master_class_no_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='student_class',
            name='student_id',
        ),
        migrations.RemoveField(
            model_name='student_master',
            name='class_no',
        ),
        migrations.RemoveField(
            model_name='student_master',
            name='section',
        ),
        migrations.AlterField(
            model_name='student_class',
            name='class_no',
            field=models.CharField(choices=[('', 'Select the Class'), ('Play-way', 'Play-way'), ('Nursery', 'Nursery'), ('lkg', 'LKG'), ('ukg', 'UKG'), ('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5'), ('6', '6'), ('7', '7'), ('8', '8'), ('9', '9'), ('10', '10'), ('11', '11'), ('12', '12')], default=6, max_length=50),
        ),
        migrations.AlterField(
            model_name='student_class',
            name='section',
            field=models.CharField(choices=[('', 'Select the Section'), ('a', 'A'), ('b', 'B'), ('c', 'C'), ('d', 'D'), ('e', 'E'), ('f', 'F'), ('g', 'G'), ('h', 'H'), ('i', 'I'), ('j', 'J')], default='A', max_length=50),
        ),
    ]