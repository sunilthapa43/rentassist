# Generated by Django 4.0.5 on 2022-09-22 04:11

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('documents', '0002_alter_agreement_deadline'),
    ]

    operations = [
        migrations.AlterField(
            model_name='agreement',
            name='deadline',
            field=models.DateField(default=datetime.date(2022, 12, 21)),
        ),
    ]
