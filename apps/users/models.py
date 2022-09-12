from django.db import models
from django.contrib.auth.models import AbstractUser
from  phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth import get_user_model
class CustomUser(AbstractUser):
    is_owner = models.BooleanField(default=False, verbose_name='Is owner?')
    phone_number = PhoneNumberField(null=False)
    image = models.ImageField(verbose_name=('image'), upload_to='static/user-images/', null=False)


User=get_user_model()


class Owner(models.Model):
    owner = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='owner user', related_name='owner_user')
    
    def __str__(self) -> str:
        return f'{self.owner.username}'


class Tenant(models.Model): 
    tenant = models.OneToOneField(User, verbose_name='tenant name', on_delete=models.CASCADE, related_name='tenant')
    owner = models.ForeignKey(Owner, verbose_name='owner', on_delete=models.CASCADE, related_name='owner_of_this_tenant',)
    def __str__(self):
        return self.tenant.username



class EmailVerification(models.Model):
    created = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='User', related_name='verify')
    token = models.CharField(max_length=6, verbose_name='verification code',null=False)