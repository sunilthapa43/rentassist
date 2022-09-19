from django.db import models


STATUS_CHOICES = [
        ('PENDING' , 'PENDING'),
        ('PROCESSING' , 'PROCESSING'),
        ('CANCELLED' , 'CANCELLED'),
        ('SUCCESS' , 'SUCCESS'),
]

MEDIUM_CHOICES = [
    ('O', 'Online Payment'),
    ('C', 'Cash Payment')
]
class Transaction(models.Model): #KHALTI
    initiator= models.ForeignKey('users.Tenant', on_delete=models.CASCADE, related_name='payment')
    payment_token = models.CharField(max_length=50,blank=False,null=False)
    paid_amount =  models.DecimalField(decimal_places=2, max_digits=10, blank=False, null=False)
    transaction_status = models.CharField(choices = STATUS_CHOICES, max_length=20)
    payment_response = models.JSONField(blank=True, null=True, verbose_name='Transaction response')
    
    def __str__(self):
        return f'{self.initiator} paid {self.paid_amount}'


class OtherPayment(models.Model):
    initiator = models.ForeignKey('users.Tenant', on_delete=models.CASCADE, verbose_name='Tenant', related_name='other_payment')
    amount = models.DecimalField(decimal_places=2, max_digits=10, blank=False, null=False)
    date = models.DateField(verbose_name='Paid At', auto_now=True)
    remarks = models.CharField(verbose_name='remarks', max_length=255, blank=False)
    

    def __str__(self):
        return f' {self.initiator} has paid Rs. {self.amount}'
    class Meta:
        ordering = ['date']



class AllTransaction(models.Model):
    initiator = models.ForeignKey('users.Tenant', verbose_name='Initiator', related_name='all_transactions',on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=8, decimal_places=2, blank=False)
    medium = models.CharField(max_length=32, blank=False, choices=MEDIUM_CHOICES)
    paid_at = models.DateTimeField(auto_now=True)
 

    def __str__(self):
        return f'{self.initiator} pays Rs. {self.amount} via {self.medium}'




