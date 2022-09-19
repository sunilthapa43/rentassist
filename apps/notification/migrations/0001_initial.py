# Generated by Django 4.0.5 on 2022-09-19 09:44

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('users', '__first__'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now=True)),
                ('is_read', models.BooleanField(default=False)),
                ('title', models.CharField(max_length=50, verbose_name='Title')),
                ('type', models.CharField(choices=[('D', 'Deadline Approach'), ('S', 'Deadline Skipped'), ('C', 'Complaint'), ('P', 'Payment'), ('O', 'Other Payment'), ('A', 'Agreement Formed'), ('CE', 'Contract Extended'), ('C', 'Contract Expiry')], max_length=30, verbose_name='type of notification')),
                ('target', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Notification target')),
                ('tenant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='notification', to='users.tenant', verbose_name='Tenant')),
            ],
        ),
    ]
