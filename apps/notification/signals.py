from typing_extensions import Self
from django.dispatch import receiver
from django.db.models.signals import pre_save, post_save
from documents.models import Agreement
from payment.models import OtherPayment, PayRent, Transaction
from rentapp.models import Complaint
from users.models import Tenant
from .models import Notification
from documents.signals import deadline_approach, deadline_skipped

@receiver(post_save, sender = Complaint)
def post_complain(sender, instance, created, weak=False, *args, **kwargs):
    obj = Notification.objects.create(tenant=instance.tenant,
    target=instance.tenant.owner.owner,
    type='C',
    title=instance.title,
    is_read=False
    )
    obj.save()


# fetch all list, id lincha notification ko, then notification[type] j cha tei page ma lagdincha


@receiver(post_save, sender = Transaction)
def post_payment(sender, instance, created, weak=False, *args, **kwargs):
    obj = Notification.objects.create(tenant=instance.tenant,
        target=instance.tenant.owner.owner,
        type='P',
        title=str(instance.tenant.username) + ' has paid Rs. ' + str(instance.amount),
        is_read=False
        )
    obj.save()



@receiver(post_save, sender=OtherPayment)
def post_other_payment(sender, instance, created, weak=False, *args, **kwargs):
    if created:
        obj =  Notification.objects.create(
            tenant=instance.tenant,
            # amount=instance.amount,
            title=str(instance.tenant)+ 'pays' + str(instance.amount) + 'physically',
            target=instance.tenant.owner.owner,
            type='O',
            is_read=False)
        obj.save()


@receiver(deadline_approach)
def on_deadline_approach(sender, instance, weak=False, *args, **kwargs):

    obj =  Notification.objects.create(
        tenant=instance.tenant,
        title= 'Your deadline of rent payment is approaching',
        target=instance.tenant,
        type='D',
        is_read=False)
    obj.save()

@receiver(deadline_approach)
def on_deadline_approach(sender, instance, weak=False, *args, **kwargs):

    obj =  Notification.objects.create(
        tenant=instance.tenant,
        title= str(instance.tenant) + " 's deadline of rent payment is approaching",
        target=instance.tenant.owner.owner,
        type='D',
        is_read=False)
    obj.save()


@receiver(deadline_skipped)
def on_deadline_skipped(sender, instance, weak=False, *args, **kwargs):

    obj =  Notification.objects.create(
        tenant=instance.tenant,
        title= 'Your deadline of rent payment is skipped',
        target=instance.tenant,
        type='D',
        is_read=False)
    obj.save()

@receiver(deadline_skipped)
def on_deadline_skipped(sender, instance, weak=False, *args, **kwargs):

    obj =  Notification.objects.create(
        tenant=instance.tenant,
        title= str(instance.tenant) + " 's deadline of rent payment is skipped",
        target=instance.tenant.owner.owner,
        type='D',
        is_read=False)
    obj.save()


# also add a flag in rent paying record