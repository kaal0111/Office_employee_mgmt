# Generated by Django 5.0.6 on 2024-06-17 15:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('emp_app', '0004_auto_20240606_1812'),
    ]

    operations = [
        migrations.AddField(
            model_name='attendance',
            name='days_present',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='attendance',
            name='status',
            field=models.CharField(choices=[('present', 'Present'), ('absent', 'Absent'), ('half day', 'Half Day'), ('leave', 'Leave')], default='not marked', max_length=10),
        ),
    ]