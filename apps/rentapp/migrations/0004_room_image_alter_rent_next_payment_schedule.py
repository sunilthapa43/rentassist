# Generated by Django 4.0.5 on 2022-09-21 09:02

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rentapp', '0003_alter_complaint_status_alter_complaint_title'),
    ]

    operations = [
        migrations.AddField(
            model_name='room',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='static/agreements', verbose_name='Dummy Agreement Image'),
        ),
        migrations.AlterField(
            model_name='rent',
            name='next_payment_schedule',
            field=models.DateField(default=datetime.date(2022, 10, 21), verbose_name='next payment schedule'),
        ),
    ]
