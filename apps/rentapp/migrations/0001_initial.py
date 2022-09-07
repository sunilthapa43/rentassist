# Generated by Django 4.0.5 on 2022-08-25 05:55

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=40)),
                ('device_id', models.CharField(max_length=50)),
                ('user_id', models.PositiveIntegerField(verbose_name='user id')),
                ('description', models.TextField(max_length=255)),
                ('deep_link', models.URLField()),
                ('notification_type', models.CharField(choices=[('M', 'Maintainence'), ('D', 'Deadline Approach'), ('E', 'Deadline Skipped')], max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Tenant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_tenant', models.BooleanField(default=True)),
                ('owner', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='owner', to=settings.AUTH_USER_MODEL, verbose_name='owner')),
                ('tenant', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='tenant', to=settings.AUTH_USER_MODEL, verbose_name='tenant name')),
            ],
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total', models.DecimalField(decimal_places=2, max_digits=7)),
                ('status', models.CharField(choices=[('C', 'Cleared'), ('P', 'Partially paid'), ('U', 'Unpaid')], max_length=255)),
                ('payment_method', models.CharField(choices=[('C', 'Cash'), ('E', 'Online Payment')], max_length=255)),
                ('date_created', models.DateField(auto_now_add=True)),
                ('tenant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='transactions', to='rentapp.tenant', verbose_name='tenant')),
            ],
        ),
        migrations.CreateModel(
            name='Rent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.IntegerField(verbose_name='rent amount')),
                ('due_date', models.DateField(verbose_name='due date')),
                ('tenant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='rent', to='rentapp.tenant')),
            ],
        ),
        migrations.CreateModel(
            name='OtherPayment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('description', models.TextField(max_length=250)),
                ('amount', models.IntegerField(verbose_name='other payments')),
                ('paid_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='payment', to='rentapp.tenant')),
            ],
        ),
        migrations.CreateModel(
            name='Electricity',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('charge_type', models.CharField(choices=[('Fixed', 'Fixed Charge'), ('Dynamic', 'Per Unit Charge')], max_length=255)),
                ('units_total', models.DecimalField(decimal_places=2, max_digits=6)),
                ('amount_total', models.DecimalField(decimal_places=2, max_digits=7)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Electricity', to='rentapp.tenant', verbose_name='tenant')),
            ],
        ),
        migrations.CreateModel(
            name='Document',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('document', models.FileField(upload_to='static/docs')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='document', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Deposit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('title', models.CharField(max_length=30, verbose_name='deposit title')),
                ('remarks', models.CharField(max_length=50)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('tenant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='deposit', to='rentapp.tenant')),
            ],
        ),
        migrations.CreateModel(
            name='Complaint',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(blank=True, upload_to='static/complains')),
                ('title', models.CharField(max_length=20)),
                ('description', models.TextField()),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('urgency_level', models.CharField(choices=[('H', 'High'), ('I', 'Intermediate'), ('L', 'Low')], max_length=255)),
                ('tenant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='complaint', to='rentapp.tenant')),
            ],
        ),
        migrations.CreateModel(
            name='Chat',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.CharField(max_length=10000)),
                ('time', models.DateTimeField(auto_now_add=True)),
                ('read', models.BooleanField(default=False)),
                ('receiver', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='Messaging', to=settings.AUTH_USER_MODEL)),
                ('sender', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='Chat', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Agreement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateField(auto_now=True)),
                ('updated', models.DateTimeField(auto_now_add=True)),
                ('deadline', models.DateField()),
                ('tenant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='agreement', to='rentapp.tenant')),
            ],
        ),
    ]
