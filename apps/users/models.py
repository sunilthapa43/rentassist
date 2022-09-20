from django.db import models
from django.contrib.auth.models import AbstractUser
from  phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth import get_user_model



class CustomUser(AbstractUser):
    is_owner = models.BooleanField(default=False, verbose_name='Is owner?')
    phone_number = PhoneNumberField(null=False)
    first_name = models.CharField(max_length=50, null=False, blank=False, verbose_name='First Name')
    last_name = models.CharField(max_length=50, null=False, blank=False, verbose_name='Last Name')
    image = models.ImageField(verbose_name=('image'), upload_to='static/user-images/', null=False)


User=get_user_model()


class Owner(models.Model):
    owner = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='owner name', related_name='owner_user')
    
    def __str__(self) -> str:
        return f'{self.owner.username}'


class Tenant(models.Model): 
    tenant = models.OneToOneField(User, verbose_name='tenant name', on_delete=models.CASCADE, related_name='tenant')
    owner = models.ForeignKey(Owner, verbose_name='owner', on_delete=models.CASCADE, related_name='owner_of_this_tenant')
    

class EmailVerification(models.Model):
    created = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='User', related_name='verify')
    token = models.CharField(max_length=6, verbose_name='verification code',null=False)



# Cannot resolve keyword 'user' into field. Choices are: auth_token, date_joined, document, email, emailaddress, first_name, groups, id, image, is_active, is_owner, is_staff, is_superuser, last_login, last_name, logentry, msg_receiver, msg_sender, notification, owner_user, password, phone_number, socialaccount, tenant, user_permissions, username, verify