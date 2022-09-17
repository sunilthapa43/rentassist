from django.dispatch import receiver
from django.db.models.signals import pre_save, post_save
from documents.models import Agreement
from payment.models import OtherPayment, Transaction
from rentapp.models import Complaint
from .models import Notification
# from documents.signals import agreement_deadline_approach, agreement_deadline_skipped



@receiver(post_save, sender = Complaint)
def post_complain(sender, instance, created, weak=False, *args, **kwargs):
    obj = Notification.objects.create(tenant=instance.tenant,
    target=instance.tenant.owner.owner,
    type='C',
    title=instance.title,
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

# @receiver(pre_save, sender=Agreement)
# def pre_save_agreement(sender, instance, *args, **kwargs):
#     try:
#         if instance.id:
#             obj = Agreement.objects.get(id=instance.id)
#             print('===========================================')
#             print(id)
#             obj.price = instance.price,
#             obj.internet_price = instance.internet_price,
#             obj.water_usage_price = instance.water_usage_price,
#             obj.electricity_rate = instance.electricity_rate,
#             obj.deadline = instance.deadline
#             obj.save()

#             noti = Notification.objects.create(
#             tenant=instance.tenant,
#             title= 'Contract with ' +str(instance.tenant) + " has been extended till" + str(instance.deadline),
#             target=instance.tenant.owner.owner,
#             type='CE',
#             is_read=False)
#             noti.save() 

#             noti = Notification.objects.create(
#             tenant=instance.tenant,
#             title= 'Contract on rent has been extended',
#             target=instance.tenant,
#             type='A',
#             is_read=False)
             
#     except Exception as e:
#         print(e)
