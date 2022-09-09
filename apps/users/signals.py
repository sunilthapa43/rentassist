from django.dispatch import receiver

from django.db.models.signals import post_save, pre_save
from .models import CustomUser, Owner, Tenant

@receiver(post_save, sender = CustomUser)
def post_save_user(sender, instance, created, weak=False, *args, **kwargs):
    if created and instance.is_owner == True:
        obj = Owner.objects.create(owner=instance)
        obj.save()
        print('successful')
    
    else:
      pass
