from django.db import models
from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField


# Create your models here.

#class MyUserManager(BaseUserManager):
#
#
#    def create_user(self, email, name, password = None ):
#        """Create a user with given email, name and pw"""
#
#        if not email:
#            raise ValueError('User must provide an email address')
#
#        user = self.model(
#            email = self.normalize_email(email),
#            name = name
#        )
#
#        user.set_password(password)
#        user.save(using = self._db)
#        return user
#
#    def create_superuser(self, email, name, password =None):
#        """create a superuser, here we define what is reqd to create a superuser"""
#        #name is not necessary; modify later
#
#        user = self.create_user(
#            email, 
#            password= password,
#            name =  name
#        )
#        user.is_admin = True
#        user.save(using = self._db)
#        return user
#
#
#
#
#class User(AbstractBaseUser):
#    email = models.EmailField(
#        verbose_name= 'email address',
#        max_length=255,
#        unique= True
#    )
#
#    name = models.CharField(max_length=255)
#    is_active = models.BooleanField(default= True)
#    is_admin = models.BooleanField(default=False)
#
#    objects = MyUserManager()
#
#    USERNAME_FIELD = 'email'
#    REQUIRED_FIELDS = ['date_of_birth']
#
#    def __str__(self):
#        return self.email
#
#    def has_perm(self, perm, obj=None):
#        "Does the user have a specific permission?"
#        # Simplest possible answer: Yes, always
#        return True
#
#    def has_module_perms(self, app_label):
#        "Does the user have permissions to view the app `app_label`?"
#        # Simplest possible answer: Yes, always
#        return True
#
#    @property
#    def is_staff(self):
#        "Is the user a member of staff?"
#        # Simplest possible answer: All admins are staff
#        return self.is_admin

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

class Owner(models.Model):
    owner = models.ForeignKey(User, on_delete= models.CASCADE)
    email = models.EmailField(verbose_name= 'email address', blank= False,max_length=40)
    phone_number = PhoneNumberField()
    balance = models.CharField(max_length=11) #modify to transactions table
    image = models.ImageField(verbose_name= 'image', null = True,  blank =True, upload_to = 'static/owner-images/', default ='static/me.jpg' )
    address = models.CharField(max_length= 255, blank= False)
    

    def __str__(self):
        return self.owner.username

class Tenant(models.Model):
    tenant = models.ForeignKey(User, on_delete=models.CASCADE , default= None)
    owner = models.ForeignKey(Owner, on_delete=models.CASCADE)
    image =  models.ImageField(verbose_name= 'tenant-image', null = True, upload_to= 'static/tenant-images/', default = 'static/me.jpg')
    balance =  models.CharField(max_length=11)
    phone_number =  PhoneNumberField()
    
    def __str__(self):
        return self.tenant.username

class Agreement(models.Model):
    owner =  models.ForeignKey(Owner, on_delete= models.CASCADE)
    tenant = models.ForeignKey(Tenant, on_delete= models.CASCADE)
    created =  models.DateField(auto_now= True)
    updated = models.DateTimeField(auto_now_add= True)
    deadline =  models.DateField()


class Document(models.Model):
    tenant =  models.ForeignKey(Tenant, on_delete=models.CASCADE)
    document = models.FileField(upload_to='static/docs')


class Complaint(models.Model):
    tenant = models.ForeignKey(Tenant, on_delete= models.CASCADE)
    owner = models.ForeignKey(Owner, on_delete= models.CASCADE)
    image = models.ImageField(upload_to = 'static/complains', blank = True)
    title = models.CharField(max_length= 20)
    description =  models.TextField()
    date =  models.DateTimeField(auto_now_add= True)
    urgency_level = models.CharField(choices= URGENCY_CHOICES,max_length =255)


class Electricity(models.Model):
    charge_type =  models.CharField(choices = ELECTRICITY_CHARGES,max_length =255)
    units_total = models.DecimalField(max_digits= 6, decimal_places= 2)
    amount_total = models.DecimalField(max_digits=7, decimal_places= 2)

class Rent(models.Model):
    price = models.IntegerField(verbose_name= ' rent amount')
    tenant = models.ForeignKey(Tenant, on_delete= models.CASCADE)
    owner = models.ForeignKey(Owner, on_delete=models.CASCADE)
    due_date =  models.DateField(verbose_name='due date')

class OtherPayment(models.Model):
    title = models.CharField(max_length= 50)
    description =  models.TextField(max_length=250)
    paid_by = models.ForeignKey(Tenant, on_delete= models.CASCADE)
    amount = models.IntegerField(verbose_name= 'other payments')


class Deposit(models.Model):
    owner = models.ForeignKey(Owner, on_delete= models.CASCADE)
    tenant = models.ForeignKey(Tenant, on_delete = models.CASCADE)
    amount = models.DecimalField(decimal_places=2, max_digits=10)
    title =  models.CharField(max_length=30, verbose_name='deposit title')
    remarks = models.CharField(max_length=50)
    date =  models.DateTimeField(auto_now_add= True)

class Notification(models.Model):
    title= models.CharField(max_length= 40)    
    device_id= models.CharField(max_length=50) # might need to change later
    user_id= models.PositiveIntegerField(auto_created= False, verbose_name = ' user id')
    description= models.TextField(max_length=255)
    deep_link= models.URLField(max_length=200)
    notification_type= models.CharField(choices= NOTIFICATION_TYPES,max_length =255 )

class Transaction(models.Model):
    owner = models.ForeignKey(Owner,verbose_name= 'owner' , on_delete= models.CASCADE)
    tenant= models.ForeignKey(Tenant,verbose_name= 'tenant' , on_delete= models.CASCADE)
    total= models.DecimalField(max_digits=7, decimal_places= 2)
    status = models.CharField(choices = BILL_STATUS,max_length =255 )
    payment_method= models.CharField(choices = PAYMENT_TYPE,max_length =255)
    date_created   = models.DateField(auto_now_add= True)
    
class Chat(models.Model): 
    message = models.CharField(max_length=10000)
    time = models.DateTimeField(auto_now_add=True)