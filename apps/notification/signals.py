from django.dispatch import receiver
from django.db.models.signals import pre_save, post_save
from documents.models import Agreement
from payment.models import OtherPayment, Transaction
from rentapp.models import Complaint
from .models import Notification
from documents.signals import agreement_deadline_approach, agreement_deadline_skipped
# deac


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
    obj = Notification.objects.create(tenant=instance.initiator,
        target=instance.initiator.owner.owner,
        type='P',
        title=str(instance.initiator) + ' has paid Rs. ' + str(instance.paid_amount),
        is_read=False
        )
    obj.save()



@receiver(post_save, sender=OtherPayment)
def post_other_payment(sender, instance, created, weak=False, *args, **kwargs):
    if created:
        obj =  Notification.objects.create(
            tenant=instance.initiator,
            # amount=instance.amount,
            title=str(instance.initiator)+ 'pays' + str(instance.amount) + 'physically',
            target=instance.initiator.owner.owner,
            type='O',
            is_read=False)
        obj.save()


@receiver(agreement_deadline_approach)
def on_deadline_approach(sender, instance, weak=False, *args, **kwargs):

    obj =  Notification.objects.create(
        tenant=instance.tenant,
        title= 'Your deadline of rent payment is approaching',
        target=instance.tenant,
        type='D',
        is_read=False)
    obj.save()

@receiver(agreement_deadline_approach)
def on_deadline_approach(sender, instance, weak=False, *args, **kwargs):

    obj =  Notification.objects.create(
        tenant=instance.tenant,
        title= str(instance.tenant) + " 's deadline of rent payment is approaching",
        target=instance.tenant.owner.owner,
        type='D',
        is_read=False)
    obj.save()


@receiver(agreement_deadline_skipped)
def on_agreement_deadline_skipped(sender, instance, weak=False, *args, **kwargs):

    obj =  Notification.objects.create(
        tenant=instance.tenant,
        title= 'Your deadline of rent payment is skipped',
        target=instance.tenant,
        type='D',
        is_read=False)
    obj.save()

@receiver(agreement_deadline_skipped)
def on_deadline_skipped(sender, instance, weak=False, *args, **kwargs):

    obj =  Notification.objects.create(
        tenant=instance.tenant,
        title= str(instance.tenant) + " 's deadline of rent payment is skipped",
        target=instance.tenant.owner.owner,
        type='D',
        is_read=False)
    obj.save()


# also add a flag in rent paying record

@receiver(post_save, sender=Agreement)
def post_saved_agreement(sender, instance, created, weak=False, *args, **kwargs):
    if created:
        obj =  Notification.objects.update_or_create(
            tenant=instance.tenant,
            title= 'Agreement formed with ' +str(instance.tenant) + "on rent",
            target=instance.tenant.owner.owner,
            type='A',
            is_read=False)
        obj.save()  
    else:
        pass  

@receiver(pre_save, sender=Agreement)
def pre_save_agreement(sender, instance, *args, **kwargs):
    try:
        if instance.id:
            obj = Agreement.objects.get(id=instance.id)
            obj.updated = instance.updated
            obj.price = instance.price,
            obj.internet_price = instance.internet_price,
            obj.water_usage_price = instance.water_usage_price,
            obj.electricity_rate = instance.electricity_rate,
            obj.deadline = instance.deadline
            obj.save()

            noti = Notification.objects.create(
            tenant=instance.tenant,
            title= 'Contract with ' +str(instance.tenant) + "has been extended",
            target=instance.tenant.owner.owner,
            type='A',
            is_read=False)
            noti.save() 

            noti = Notification.objects.create(
            tenant=instance.tenant,
            title= 'Contract on rent has been extended',
            target=instance.tenant,
            type='A',
            is_read=False)
            noti.save()  
    except Exception as e:
        print(e)



@receiver(post_save, sender= Notification)
def send_mail(sender, instance, weak=False, *args, **kwargs):
    print('send mail')