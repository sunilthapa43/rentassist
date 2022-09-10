# Generated by Django 4.0.5 on 2022-09-09 05:20

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
            name='Message',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.TextField()),
                ('is_read', models.BooleanField(default=False, verbose_name='is read')),
                ('sent_at', models.DateTimeField(auto_now_add=True)),
                ('receiver', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='msg_receiver', to=settings.AUTH_USER_MODEL, verbose_name='receiver')),
                ('sender', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='msg_sender', to=settings.AUTH_USER_MODEL, verbose_name='sender')),
            ],
            options={
                'verbose_name': 'Message',
                'verbose_name_plural': 'Messages',
                'ordering': ['sent_at'],
            },
        ),
    ]
