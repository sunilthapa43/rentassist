from django.db import models
from django.contrib.auth import get_user_model
from phonenumber_field.modelfields import PhoneNumberField


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

User= get_user_model()
class Owner(models.Model):
    owner = models.OneToOneField(User, on_delete=models.CASCADE,max_length=35, verbose_name='owner name', related_name='owner')
    email = models.EmailField(verbose_name='User email address', null=False)
    phone_number = PhoneNumberField()
    balance = models.CharField(max_length=11) #modify to transactions table
    image = models.ImageField(verbose_name='image', null=True, blank=True, upload_to='static/owner-images/', default='static/me.jpg' )
    address = models.CharField(max_length=255, blank=False)
    
    def __str__(self):
        return self.owner.username
    
    

# no fk user, add name instead
class Tenant(models.Model): 
    tenant = models.OneToOneField(User, max_length=35, verbose_name='tenant name', on_delete=models.CASCADE, related_name='tenant') 
    owner = models.ForeignKey(Owner, on_delete=models.CASCADE)
    image =  models.ImageField(verbose_name='photo', null=True, upload_to='static/tenant-images/', default='static/me.jpg')
    balance =  models.CharField(max_length=11)
    phone_number =  PhoneNumberField()
    
    def __str__(self):
        return self.tenant.username

class Agreement(models.Model):
    owner =  models.ForeignKey(Owner, on_delete=models.CASCADE,related_name='agreement')
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name='agreement')
    created =  models.DateField(auto_now= True)
    updated = models.DateTimeField(auto_now_add= True)
    deadline =  models.DateField()


class Document(models.Model):
    tenant =  models.ForeignKey(Tenant, on_delete=models.CASCADE,related_name='document')
    document = models.FileField(upload_to='static/docs')


class Complaint(models.Model):
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE,related_name='complaint')
    owner = models.ForeignKey(Owner, on_delete=models.CASCADE, related_name='complaint')
    image = models.ImageField(upload_to='static/complains', blank=True)
    title = models.CharField(max_length=20)
    description =  models.TextField()
    date =  models.DateTimeField(auto_now_add=True)
    urgency_level = models.CharField(choices=URGENCY_CHOICES,max_length =255)


class Electricity(models.Model):
    charge_type =  models.CharField(choices=ELECTRICITY_CHARGES,max_length=255)
    units_total = models.DecimalField(max_digits=6, decimal_places=2)
    amount_total = models.DecimalField(max_digits=7, decimal_places=2)

class Rent(models.Model):
    price = models.IntegerField(verbose_name='rent amount')
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name='rent')
    owner = models.ForeignKey(Owner, on_delete=models.CASCADE)
    due_date =  models.DateField(verbose_name='due date')

class OtherPayment(models.Model):
    title = models.CharField(max_length=50)
    description =  models.TextField(max_length=250)
    paid_by = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name='payment')
    amount = models.IntegerField(verbose_name='other payments')


class Deposit(models.Model):
    owner = models.ForeignKey(Owner, on_delete=models.CASCADE,related_name='deposit')
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

class Transaction(models.Model):
    owner = models.ForeignKey(Owner,verbose_name='owner' , on_delete=models.CASCADE, related_name='transactions')
    tenant= models.ForeignKey(Tenant,verbose_name='tenant' , on_delete=models.CASCADE, related_name='transactions')
    total= models.DecimalField(max_digits=7, decimal_places=2)
    status = models.CharField(choices=BILL_STATUS,max_length=255 )
    payment_method= models.CharField(choices=PAYMENT_TYPE,max_length=255)
    date_created = models.DateField(auto_now_add=True)
    
class Chat(models.Model): 
    message = models.CharField(max_length=10000)
    time = models.DateTimeField(auto_now_add=True)