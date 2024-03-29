# Generated by Django 4.0.5 on 2022-09-20 07:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ocr', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Ocr',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='static/meter-reader-images/', verbose_name='meter image')),
                ('image_name', models.CharField(max_length=50)),
                ('extracted_digits', models.DecimalField(decimal_places=2, default=123456.24, max_digits=8)),
            ],
        ),
        migrations.RemoveField(
            model_name='electricityunit',
            name='image',
        ),
    ]
