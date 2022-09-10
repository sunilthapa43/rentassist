from django.db import models
from rentapp.models import Rent


STATUS_CHOICES = [
        ('PENDING' , 'PENDING'),
        ('PROCESSING' , 'PROCESSING'),
        ('CANCELLED' , 'CANCELLED'),
        ('SUCCESS' , 'SUCCESS'),
]
class Transaction(models.Model):
    initiator= models.ForeignKey('users.Tenant', on_delete=models.PROTECT, related_name='payment')
    payment_token = models.CharField(max_length=50,blank=False,null=False)
    paid_amount =  models.DecimalField(decimal_places=2, max_digits=10, blank=False, null=False)
    transaction_status = models.CharField(choices = STATUS_CHOICES, max_length=20)
    payment_response = models.JSONField(blank=True, null=True, verbose_name='Transaction response')
    
    def __str__(self):
        return f'{self.initiator} paid {self.amount}'


class OtherPayment(models.Model):
    initiator = models.ForeignKey('users.Tenant', on_delete=models.PROTECT, verbose_name='Other payment', related_name='other_payment')
    amount = models.DecimalField(decimal_places=2, max_digits=10, blank=False, null=False)
    date = models.DateField(verbose_name='Paid At')
    remarks = models.CharField(verbose_name='remarks', max_length=255, blank=False)
    

    def __str__(self):
        return f'{self.initiator} has paid Rs. {self.amount}'
    class Meta:
        ordering = ['date']


class PayRent(models.Model):
    class Status(models.TextChoices):
        FULLLY_PAID = 'FULL', ('Fully Paid')
        PARTIALLY_PAID = 'PARTIAL', ('Partially Paid')

    
    rent = models.ForeignKey(Rent, on_delete=models.CASCADE, verbose_name='Rent', related_name="total_rent")
    online_payment_amount = models.ForeignKey(Transaction, on_delete=models.PROTECT, null=True, blank=True)
    other_payment_amount = models.ForeignKey(OtherPayment, on_delete=models.PROTECT, null=True, blank=True)
    remaining_balance = models.DecimalField(max_digits=7, decimal_places=2)
    status = models.CharField(max_length=25, verbose_name='payment status', choices=Status.choices)

    def __str__(self) -> str:
        if self.online_payment_amount and self.online_payment_amount.amount >= self.rent.total_rent:
            msg = f'{self.rent.tenant} has {self.status} paid {self.online_payment_amount}'
        elif self.other_payment_amount and self.other_payment_amount.amount >= self.rent.total_rent:
            msg = f'{self.rent.tenant} has {self.status} paid {self.online_payment_amount}'
        return msg
    
