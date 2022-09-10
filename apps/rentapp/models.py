from django.db import models

from users.models import Tenant

URGENCY_CHOICES =[
    ('H','High'),
    ('I', 'Intermediate'),
    ('L', 'Low')
]
ELECTRICITY_CHARGES = [
    ('Fixed', 'Fixed Charge'),
    ('Dynamic', 'Per Unit Charge')
]


BILL_STATUS=  [
    ('C', 'Cleared'),
    ('P', 'Partially paid'),
    ('U', 'Unpaid')
      
]
PAYMENT_TYPE = [
    ('C', 'Cash'),
    ('E', 'Online Payment')
]

class Complaint(models.Model):
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE,related_name='complaint')
    image = models.ImageField(upload_to='static/complains', blank=True, null=True)
    title = models.CharField(max_length=20)
    description =  models.TextField()
    date =  models.DateTimeField(auto_now_add=True)
    urgency_level = models.CharField(choices=URGENCY_CHOICES,max_length =255)

    def __str__(self) -> str:
        return f'{self.tenant} complains on {self.title}'
class Rent(models.Model):
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name='rent')
    price = models.IntegerField(verbose_name='rent amount', null=False, blank=False)
    internet_price = models.DecimalField(max_digits=4, decimal_places=2, blank = True, null=True)
    water_usage_price = models.DecimalField(max_digits=4, decimal_places=2, blank = True, null=True)
    electricity_rate = models.DecimalField(max_digits=3, decimal_places=2, verbose_name='electricity charge per unit')
    
    def __str__(self) -> str:
        return f'{self.tenant} has room rent of Rs. {self.price}'       


class Deposit(models.Model):
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name='deposit')
    amount = models.DecimalField(decimal_places=2, max_digits=10)
    title =  models.CharField(max_length=30, verbose_name='deposit title')
    remarks = models.CharField(max_length=50)
    date =  models.DateTimeField(auto_now_add=True)


# have owner add rooms or flats, its image when tenant comes and takes one the owner assigns a room while adding the tenant,
#  this way it is easier if same tenant buys 2 different rooms or apartments