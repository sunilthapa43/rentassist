
from django.dispatch import Signal, receiver
from ocr.models import ElectricityUnit
from django.db.models.signals import post_save
from documents.models import Agreement
from payment.models import OtherPayment, Transaction
from rentapp.models import Rent

@receiver(post_save, sender = ElectricityUnit)
def post_save_electricity(sender, instance, created, weak=False, *args, **kwargs):
    """ When an electricity(ocr) is updated, the rent amount that is to be paid by the user is calculated by the help of signals"""
    if not instance.current_reading == 0.0:
        
        a = Agreement.objects.get(tenant=instance.tenant)
        current_units = instance.current_units
        total_payable_amount = a.total_price(electricity_unit=current_units)
        try:
           b = Rent.objects.get(tenant = instance.tenant)
    
           if b:
            print('found b')
            b.this_month_rent = total_payable_amount
            b.amount_to_be_paid = b.total_amount()
            b.save()
    
           else:
            a = Rent.objects.create(tenant=instance.tenant,
                                    this_month_rent = total_payable_amount,
                                    amount_to_be_paid = total_payable_amount,
                                    amount_paid_this_month = 0,
                                    due_amount = 0,
                                    status = 'U',
                                    )
            a.save()

        except Exception as e:
            print(e)
            

@receiver(post_save, sender = Transaction)
def post_payment(sender, instance, created, weak=False, *args, **kwargs):
    if created:
        obj = Rent.objects.get(tenant=instance.initiator)
        total_payable_amount = obj.total_amount()
        if instance.paid_amount == 0:
            obj.status = 'U'
        if instance.paid_amount >= total_payable_amount:
            obj.status = 'F'
            
        else:
            obj.status = 'P'
            
        obj.amount_paid_this_month = instance.paid_amount
        obj.due_amount = obj.calculate_due()
        
        obj.save()


@receiver(post_save, sender = OtherPayment)
def post_payment(sender, instance, created, weak=False, *args, **kwargs):
    if created:
        obj = Rent.objects.get(tenant=instance.initiator)
        total_payable_amount = obj.total_amount()
        if instance.amount == 0:
            obj.status = 'U'
        if instance.amount >= total_payable_amount:
            obj.status = 'F'
            
        else:
            obj.status = 'P'
            
        obj.amount_paid_this_month = instance.amount
        obj.due_amount = obj.calculate_due()
        
        obj.save()



