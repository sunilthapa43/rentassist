from django.dispatch import receiver
from django.core.mail import send_mail
from django.db.models.signals import post_save, pre_save

from rentassist.settings import EMAIL_HOST_USER
from .models import CustomUser, Owner, Tenant


def generate_otp():
    pass


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
    if instance.email != '':
        generate_otp()
        send_mail(
            'Account Verification',
            'Thanks for signing up with us. Your email needs to be verified. Your otp code is',
            EMAIL_HOST_USER,
            [instance.email]
        )
    