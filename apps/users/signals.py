from django.dispatch import receiver
from django.core.mail import send_mail
from django.db.models.signals import post_save, pre_save

from rentassist.settings import EMAIL_HOST_USER
from .models import CustomUser, EmailVerification, Owner, Tenant
import math, random


    
 
# function to 6-digit generate OTP
def generate_otp() :
 
    # Declare a digits variable 
    # which stores all digits
    digits = "0123456789"
    OTP = ""
 
   
   # by changing value in range
    for i in range(6) :
        OTP += digits[math.floor(random.random() * 10)]
 
    return OTP


@receiver(post_save, sender = CustomUser)
def post_save_user(sender, instance, created, weak=False, *args, **kwargs):
    if created and instance.is_owner == True:
        obj = Owner.objects.create(owner=instance)
        obj.save()
        print('successful')
    
    else:
      pass


@receiver(post_save, sender=CustomUser)
def verification(sender, instance, created, weak=False, *args, **kwargs):
    otp = generate_otp()
    if instance.email != '' and instance.is_active ==True:
        send_mail(
            'Account Verification',
            'Thanks for signing up with us. Your email needs to be verified. Your otp code is: ' + otp ,
            EMAIL_HOST_USER,
            [instance.email]
        )

    obj = EmailVerification.objects.create(user=instance, token = otp)
    obj.save()

