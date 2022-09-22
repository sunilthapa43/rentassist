from typing_extensions import Self
from django.dispatch import receiver
from .models import Deposit, Transaction, AllTransaction, OtherPayment
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



@receiver(post_save, sender=Transaction)
def deposit(sender, instance, created, weak=False, *args, **kwargs):
    if created:
        owner = instance.initiator.owner
        print(owner)
        obj = Deposit.objects.filter(owner = owner)
        print(obj)
        if obj.count() == 1:
            obj = Deposit.objects.get(owner=owner)
            obj.amount = obj.amount + instance.paid_amount
            obj.save()
        else:
            print("created new")
            obj = Deposit.objects.create(
                owner = instance.initiator.owner,
                amount = instance.paid_amount
            )
            obj.save()