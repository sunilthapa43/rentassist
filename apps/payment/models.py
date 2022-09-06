from http.client import PROCESSING
from secrets import choice
from django.db import models
from django.contrib.auth import get_user_model
User= get_user_model()
# Create your models here.
class Transaction(models.Model):
    class Status(models.TextChoices):
        PENDING = 'PENDING'
        PROCESSING = 'PROCESSING'
        CANCELLED = 'CANCELLED'
        SUCCESS = 'SUCCESS'

    
    initiator= models.ForeignKey(User, on_delete=models.PROTECT, related_name='payment')
    payment_token = models.CharField(max_length=50,blank=False,null=False)
    amount =  models.DecimalField(decimal_places=2, max_digits=10, blank=False, null=False)
    transaction_status = models.CharField(choices = Status, default=Status.PENDING)
    payment_response = models.JSONField(blank=True, null=True, verbose_name='Transaction response')
    def __str__(self):
        return f'{self.initiator} paid {self.amount}'
