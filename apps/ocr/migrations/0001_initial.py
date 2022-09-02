# Generated by Django 4.0.5 on 2022-08-25 04:54

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
            name='ImageToText',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='static/meter-reader-images/', verbose_name='meter image')),
                ('extracted_reading', models.DecimalField(decimal_places=2, max_digits=7, verbose_name='meter reading')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ImageToText', to=settings.AUTH_USER_MODEL, verbose_name='User')),
            ],
        ),
    ]
