from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Message
from fcm_django.models import FCMDevice
from firebase_admin.messaging import Message as FirebaseMessage, Notification as FirebaseNotification

@receiver(post_save, sender=Message)
def fcm_push_notification(sender, instance, created, weak=False, *args, **kwargs):
    if created:
        id = instance.id
        sender = instance.sender.first_name
        message = instance.message
        receiver = instance.receiver
        try:
          devices = FCMDevice.objects.filter(user = receiver, active=True).first()
          fcm_message = FirebaseMessage(notification=FirebaseNotification(
            title='New Message From ' + str(sender),
            body = str(message), 
          ),
        #   topic='New Message'
          )
          devices.send_message(fcm_message)
          print('message is sent')

        except Exception as e:
            print(e)
