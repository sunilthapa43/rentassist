from django.db import models
from django.contrib.auth import get_user_model

URGENCY_CHOICES =[
    ('H','High'),
    ('I', 'Intermediate'),
    ('L', 'Low')
]
ELECTRICITY_CHARGES = [
    ('Fixed', 'Fixed Charge'),
    ('Dynamic', 'Per Unit Charge')
]

NOTIFICATION_TYPES = [
    ('M', 'Maintainence'),
    ('D', 'Deadline Approach'),
    ('E','Deadline Skipped'),
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

User=get_user_model()


class Tenant(models.Model): 
    tenant = models.OneToOneField(User, verbose_name='tenant name', on_delete=models.CASCADE, related_name='tenant')
    owner = models.OneToOneField(User, verbose_name='owner', on_delete=models.CASCADE, related_name='owner', )
    is_tenant = models.BooleanField(default=True)
    def __str__(self):
        return self.tenant.username


class Complaint(models.Model):
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE,related_name='complaint')
    image = models.ImageField(upload_to='static/complains', blank=True)
    title = models.CharField(max_length=20)
    description =  models.TextField()
    date =  models.DateTimeField(auto_now_add=True)
    urgency_level = models.CharField(choices=URGENCY_CHOICES,max_length =255)


class Rent(models.Model):
    price = models.IntegerField(verbose_name='rent amount')
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name='rent')
    due_date =  models.DateField(verbose_name='due date')



class Deposit(models.Model):
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name='deposit')
    amount = models.DecimalField(decimal_places=2, max_digits=10)
    title =  models.CharField(max_length=30, verbose_name='deposit title')
    remarks = models.CharField(max_length=50)
    date =  models.DateTimeField(auto_now_add=True)

class Notification(models.Model):
    title= models.CharField(max_length=40)    
    device_id= models.CharField(max_length=50) # might need to change later
    user_id= models.PositiveIntegerField(auto_created=False, verbose_name='user id')
    description= models.TextField(max_length=255)
    deep_link= models.URLField(max_length=200)
    notification_type= models.CharField(choices=NOTIFICATION_TYPES, max_length=255 )

