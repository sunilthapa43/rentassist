# Generated by Django 4.0.5 on 2022-09-10 04:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('documents', '0002_alter_agreement_tenant'),
    ]

    operations = [
        migrations.AlterField(
            model_name='agreement',
            name='electricity_rate',
            field=models.DecimalField(decimal_places=2, max_digits=4, verbose_name='electricity charge per unit'),
        ),
    ]
