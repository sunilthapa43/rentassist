from django.dispatch import receiver
from django.db.models.signals import pre_save, post_save
from documents.models import Agreement
from payment.models import AllTransaction
from rentapp.models import Complaint
from .models import Notification
# from documents.signals import agreement_deadline_approach, agreement_deadline_skipped


from fcm_django.models import FCMDevice
from firebase_admin.messaging import Message as FirebaseMessage, Notification as FirebaseNotification

def switcher(type):
    to_subject = {
        'D': 'Deadline Approach',
        'S': 'Deadline Skipped',
        'C': 'Complaint',
        'T': 'Transaction',
        'O': 'Other Payment',
        'A': 'Agreement Formed',
        'CE': 'Contract Extended',
        'E': 'Contract Expiry',
        'CM': 'Configure Meter',
    }
    return to_subject.get(type)


@receiver(post_save, sender = Complaint)
def post_complain(sender, instance, created, weak=False, *args, **kwargs):
    if created:
        obj = Notification.objects.create(tenant=instance.tenant,
        target=instance.tenant.owner.owner,
        type='C',
        title='Complaint from '+ str(instance.tenant.tenant.first_name),
        deep_link = f'rentassist2021.herokuapp.com/api/complaints/{instance.id}',
        is_read=False
        )
        obj.save()
    else:
        obj = Notification.objects.create(tenant=instance.tenant,
        target=instance.tenant.tenant,
        type='C',
        title=f'Your complaint cmp{instance.id} has been addressed',
        deep_link = f'rentassist2021/api/complaints/{instance.id}',
        # str(instance.tenant.tenant.first_name) ,
        is_read=False
        )
        obj.save()



@receiver(post_save, sender=Agreement)
def post_saved_agreement(sender, instance, created, weak=False, *args, **kwargs):
    if created:
        obj =  Notification.objects.create(
            tenant=instance.tenant,
            title= 'Agreement formed with ' +str(instance.tenant.tenant.first_name) + " on rent",
            target=instance.tenant.owner.owner,
            type='A',
            is_read=False)
        obj.save()
        obj =  Notification.objects.create(
            tenant=instance.tenant,
            title= 'Agreement formed with ' +str(instance.tenant.owner.owner.first_name) + " on rent",
            target=instance.tenant.tenant,
            type='A',
            is_read=False)
        obj.save()        
    else:
        obj =  Notification.objects.create(
            tenant=instance.tenant,
            title= 'Agreement updated with ' +str(instance.tenant.tenant.first_name) + " on rent",
            target=instance.tenant.owner.owner,
            type='CE',
            is_read=False)
        obj.save()



@receiver(post_save, sender=Notification)
def fcm_push_notification(sender, instance, created, weak=False, *args, **kwargs):
    if created:
        id = instance.id
        type= switcher(instance.type)

        message = instance.title
        receiver = instance.target
        try:
          devices = FCMDevice.objects.filter(user = receiver, active=True).first()
          print(devices)
          fcm_message = FirebaseMessage(notification=FirebaseNotification(
            title='New Notification on ' + type,
            body = str(message), 
          ),
        #   topic='New Message'
          )
          devices.send_message(fcm_message)
          print('message is sent')

        except Exception as e:
            print(e)



@receiver(post_save, sender=AllTransaction)
def notify_transaction(sender, instance, created, weak=False, *args, **kwargs):
    if created:
        med = 'Online Payment'
        if instance.medium == 'C':
            med = 'Cash Payment'
        
        obj = Notification.objects.create(
            tenant=instance.initiator,
            title= str(instance.initiator.tenant.first_name) + ' has paid rs '+ str(instance.amount) + ' via ' + med,
            target=instance.initiator.owner.owner,
            type='T',
            is_read=False)
        obj.save()