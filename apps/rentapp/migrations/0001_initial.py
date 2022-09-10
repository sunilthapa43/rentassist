# Generated by Django 4.0.5 on 2022-09-09 07:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Rent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.IntegerField(verbose_name='rent amount')),
                ('internet_price', models.DecimalField(blank=True, decimal_places=2, max_digits=4, null=True)),
                ('water_usage_price', models.DecimalField(blank=True, decimal_places=2, max_digits=4, null=True)),
                ('electricity_rate', models.DecimalField(decimal_places=2, max_digits=3, verbose_name='electricity charge per unit')),
                ('tenant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='rent', to='users.tenant')),
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
                ('tenant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='deposit', to='users.tenant')),
            ],
        ),
        migrations.CreateModel(
            name='Complaint',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(blank=True, null=True, upload_to='static/complains')),
                ('title', models.CharField(max_length=20)),
                ('description', models.TextField()),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('urgency_level', models.CharField(choices=[('H', 'High'), ('I', 'Intermediate'), ('L', 'Low')], max_length=255)),
                ('tenant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='complaint', to='users.tenant')),
            ],
        ),
    ]
