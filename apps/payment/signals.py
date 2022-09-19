from typing_extensions import Self
from django.dispatch import receiver
from .models import Transaction, AllTransaction, OtherPayment
from django.db.models.signals import post_save


@receiver(post_save, sender=Transaction)
def post_online_payment(sender, instance, created, weak=False, *args, **kwargs):
    if created:
        obj = AllTransaction.objects.create(initiator=instance.initiator,
                                      amount=instance.paid_amount,
                                      medium = 'O')
        obj.save()


@receiver(post_save, sender=OtherPayment)
def post_cash(sender, instance, created, weak=False, *args, **kwargs):
    if created:
        obj = AllTransaction.objects.create(initiator=instance.initiator,
                                      amount=instance.amount,
                                      medium = 'C')
        obj.save()
