from datetime import datetime, timedelta
from django.db import models
from notification.models import Notification

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
    tenant = models.ForeignKey('users.Tenant', on_delete=models.CASCADE,related_name='complaint')
    image = models.ImageField(upload_to='static/complains', blank=True, null=True)
    title = models.CharField(max_length=20)
    description =  models.TextField()
    date =  models.DateTimeField(auto_now_add=True)
    urgency_level = models.CharField(choices=URGENCY_CHOICES,max_length =255)

    def __str__(self) -> str:
        return f'{self.tenant} complains on {self.title}'
        

class Rent(models.Model):
    class Status(models.TextChoices):
        FULLLY_PAID = 'F', ('Fully Paid')
        PARTIALLY_PAID = 'P', ('Partially Paid')
        UNPAID = 'U', ('Unpaid')
    
    tenant = models.ForeignKey('users.Tenant', on_delete=models.CASCADE, verbose_name='who pays the rent', related_name='rent_payer')
    this_month_rent = models.DecimalField(max_digits=8, decimal_places=2)
    amount_to_be_paid = models.DecimalField(max_digits=8, decimal_places=2) #this_month_rent + due_amount
    amount_paid_this_month = models.DecimalField(max_digits=8, decimal_places=2)
    due_amount = models.DecimalField(max_digits=8, decimal_places=2, verbose_name='remaining amount')
    status = models.CharField(max_length=25, verbose_name='payment status', choices=Status.choices)
    paid_at = models.DateField(auto_now=True)
    next_payment_schedule = models.DateField(default=datetime.now().date() + timedelta(days=30), verbose_name='next payment schedule')


    def total_amount(self):
        total = self.this_month_rent + self.due_amount
        return total

    def schedule_deadline(self, days):
        schedule =  datetime.now().date() + timedelta(days=days)
        return schedule
    
    def calculate_due(self):
        due = self.amount_to_be_paid - self.amount_paid_this_month
        return due

    def create_notification(self, days, flag):
        if days == -1 and flag == 1:
            type = 'S'
            target = self.tenant.owner.owner
            title = f'The rent paying deadline for {self.tenant} has been skipped'
        if days == 1 and flag == 0:
            type = 'D'
            target = self.tenant.tenant
            title = f'Your rent paying deadline is tomorrow' 
        elif days == 1 and flag == 1:
            type = 'D'
            target = self.tenant.owner.owner
            title = f'The rent paying deadline for {self.tenant} is tomorrow'
        elif days == 0 and flag == 0:
            type = 'D'
            target = self.tenant.tenant
            title = f'Today is your scheduled rent paying date'
    
        elif days == 0 and flag == 1:
            type = 'D'
            target = self.tenant.owner.owner
            title = f'The rent paying deadline for {self.tenant} is today'
        
        
    
        elif days == -1 and flag == 0:
            type = 'S'
            target = self.tenant.tenant
            title = f'The deadline for rent payment has been skipped'
        

        
        else:
            pass
        type = type or 'S'
        obj = Notification.objects.create(
            tenant = self.tenant,
            is_read = False,
            title = title,
            type = type ,
            target = target
        )
        obj.save()



class Room(models.Model):
    name = models.CharField(max_length=50, blank=True, default = 'great room', verbose_name='Room')
    owner = models.ForeignKey('users.Owner', on_delete=models.CASCADE, related_name='room_owner', verbose_name='owner user')
    price = models.IntegerField(verbose_name='rent amount', null=False, blank=False)
    internet_price = models.IntegerField(verbose_name = 'Internet Price', default=0)
    water_usage_price = models.IntegerField( null=False, verbose_name = 'water_usage_price')
    nagarpalika_fohr_price = models.IntegerField( null=False, blank=False, verbose_name = 'Nagarpalika Fohr Price',)
    electricity_rate = models.IntegerField( verbose_name='electricity charge per unit')
    created =  models.DateField(auto_now= True)
    updated = models.DateField(auto_now_add=True)

    def __str__(self) -> str:
        return f'{self.id}'