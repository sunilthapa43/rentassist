from django.dispatch import receiver
from django.db.models.signals import pre_save, post_save
from documents.models import Agreement
from rentapp.models import Complaint
from .models import Notification
# from documents.signals import agreement_deadline_approach, agreement_deadline_skipped



@receiver(post_save, sender = Complaint)
def post_complain(sender, instance, created, weak=False, *args, **kwargs):
    obj = Notification.objects.create(tenant=instance.tenant,
    target=instance.tenant.owner.owner,
    type='C',
    title='you received a compalint: ' + str(instance.title) + 'from ' + str(instance.tenant) ,
    is_read=False
    )
    obj.save()



@receiver(post_save, sender=Agreement)
def post_saved_agreement(sender, instance, created, weak=False, *args, **kwargs):
    if created:
        obj =  Notification.objects.update_or_create(
            tenant=instance.tenant,
            title= 'Agreement formed with ' +str(instance.tenant) + " on rent",
            target=instance.tenant.owner.owner,
            type='A',
            is_read=False)
         
    else:
        pass  

