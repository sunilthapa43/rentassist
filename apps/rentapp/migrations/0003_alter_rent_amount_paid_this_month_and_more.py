# Generated by Django 4.0.5 on 2022-09-10 04:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rentapp', '0002_remove_rent_electricity_rate_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rent',
            name='amount_paid_this_month',
            field=models.DecimalField(decimal_places=2, max_digits=8),
        ),
        migrations.AlterField(
            model_name='rent',
            name='amount_to_be_paid',
            field=models.DecimalField(decimal_places=2, max_digits=8),
        ),
        migrations.AlterField(
            model_name='rent',
            name='due_amount',
            field=models.DecimalField(decimal_places=2, max_digits=8, verbose_name='remaining amount'),
        ),
        migrations.AlterField(
            model_name='rent',
            name='this_month_rent',
            field=models.DecimalField(decimal_places=2, max_digits=8),
        ),
    ]
