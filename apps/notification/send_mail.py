from django.dispatch import receiver
from django.db.models.signals import pre_save, post_save

from rentassist.settings import EMAIL_HOST_USER
from .models import Notification
from django.core.mail import send_mail


mail_sender = 'me'
def switcher(type):
    to_subject = {
        'D':'Deadline Approach',
        'S':'Deadline Skipped',
        'C':'Complaint',
        'P':'Online Payment',
        'O':'Other Payment',
        'A':'Agreement Formed or Updated'
    }
    return to_subject.get(type)

@receiver(post_save, sender=Notification)
def send_email(sender, instance, created, weak=False, *args, **kwargs):
    type =instance.type
    subject = switcher(type)
    send_mail(
        subject,
        instance.title,
        EMAIL_HOST_USER,
        [instance.target.email]
    )