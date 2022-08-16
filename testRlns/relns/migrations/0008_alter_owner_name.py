# Generated by Django 4.0.4 on 2022-07-11 05:56

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('relns', '0007_remove_user_is_owner_remove_user_is_tenant'),
    ]

    operations = [
        migrations.AlterField(
            model_name='owner',
            name='name',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='owners', to=settings.AUTH_USER_MODEL),
        ),
    ]
