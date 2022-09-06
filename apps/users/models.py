from django.db import models
from django.contrib.auth.models import AbstractUser
from  phonenumber_field.modelfields import PhoneNumberField

class CustomUser(AbstractUser):
    is_owner = models.BooleanField(default=False, verbose_name='Is owner?')
    phone_number = PhoneNumberField(null=False)
    image = models.ImageField(verbose_name=('image'), upload_to='static/images/', null=False)
