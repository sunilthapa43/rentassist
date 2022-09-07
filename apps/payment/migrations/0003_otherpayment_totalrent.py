# Generated by Django 4.0.5 on 2022-09-07 06:12

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('payment', '0002_transaction_delete_payment'),
    ]

    operations = [
        migrations.CreateModel(
            name='OtherPayment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('date', models.DateField(verbose_name='Paid At')),
                ('remarks', models.CharField(max_length=255, verbose_name='remarks')),
                ('initiator', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='other_payment', to=settings.AUTH_USER_MODEL, verbose_name='Other payment')),
            ],
            options={
                'ordering': ['date'],
            },
        ),
        migrations.CreateModel(
            name='TotalRent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total_amount', models.DecimalField(decimal_places=2, max_digits=7)),
                ('remaining_balance', models.DecimalField(decimal_places=2, max_digits=7)),
                ('online_payment_amount', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='payment.transaction')),
                ('other_payment_amount', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='payment.otherpayment')),
                ('tenant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='total_rent', to=settings.AUTH_USER_MODEL, verbose_name='total amount to be paid')),
            ],
        ),
    ]
