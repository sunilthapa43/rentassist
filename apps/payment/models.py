from http.client import PROCESSING
from pyexpat import model
from secrets import choice
from tabnanny import verbose
from django.db import models
from django.contrib.auth import get_user_model

from rentapp.models import Rent
User= get_user_model()
# Create your models here.

STATUS_CHOICES = [
        ('PENDING' , 'PENDING'),
        ('PROCESSING' , 'PROCESSING'),
        ('CANCELLED' , 'CANCELLED'),
        ('SUCCESS' , 'SUCCESS'),
]
class Transaction(models.Model):
    initiator= models.ForeignKey(User, on_delete=models.PROTECT, related_name='payment')
    payment_token = models.CharField(max_length=50,blank=False,null=False)
    amount =  models.DecimalField(decimal_places=2, max_digits=10, blank=False, null=False)
    transaction_status = models.CharField(choices = STATUS_CHOICES, max_length=20)
    payment_response = models.JSONField(blank=True, null=True, verbose_name='Transaction response')
    
    def __str__(self):
        return f'{self.initiator} paid {self.amount}'


class OtherPayment(models.Model):
    initiator = models.ForeignKey(User, on_delete=models.PROTECT, verbose_name='Other payment', related_name='other_payment')
    amount = models.DecimalField(decimal_places=2, max_digits=10, blank=False, null=False)
    date = models.DateField(verbose_name='Paid At')
    remarks = models.CharField(verbose_name='remarks', max_length=255, blank=False)
    
    def __str__(self):
        return f'{self.initiator.username} has paid Rs. { self.amount}'
    class Meta:
        ordering = ['date']


class TotalRent(models.Model):
    tenant = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='total amount to be paid', related_name='total_rent')
    total_amount = models.DecimalField(max_digits=7, decimal_places=2) #Electricity, 
    online_payment_amount = models.ForeignKey(Transaction, on_delete=models.PROTECT, null=True, blank=True)
    other_payment_amount = models.ForeignKey(OtherPayment, on_delete=models.CASCADE, null=True, blank=True)
    remaining_balance = models.DecimalField(max_digits=7, decimal_places=2)
    
