
from datetime import datetime
from django.db import models
from django.db.models.signals import post_save

from django.contrib.auth.models import User, AbstractUser
from django.dispatch import receiver
# Create your models here.

class User(AbstractUser):
    user_type_choice = ((1, 'Owner'), (2, 'Tenant'))
    user_type = models.CharField(default= 1, choices= user_type_choice, max_length=10)


class Owner(models.Model):
    name = models.OneToOneField(User, on_delete= models.CASCADE)
    

    def __str__(self):
        return self.name.username
    


    
class Tenant(models.Model):
    fname = models.CharField(max_length=25)
    lname = models.CharField(max_length=25)
    identity = models.OneToOneField(User, on_delete= models.CASCADE, )
    owner =  models.ForeignKey(Owner, on_delete=models.CASCADE, related_name= 'owner')
    
    def __str__(self):
        return f'{self.fname} {self.lname}'
    
    


    
        


class Chat(models.Model):
    sender = models.ForeignKey(User, on_delete= models.CASCADE,verbose_name='sender',related_name= 'sender')
    receiver = models.ForeignKey(User, on_delete= models.CASCADE, verbose_name= 'receiver', related_name= 'receiver')
    timestamp = models.DateTimeField(auto_now_add= True) 
    message = models.TextField(max_length=10000, )
    seen_status =  models.BooleanField(default= False)

    def __str__(self):
        return self.message
    
    class Meta:
        ordering = ('timestamp',

    
    
    # if sender is Owner:
    #  def sendmessage(self, message, receiver, sender):
    #     message = self.message
    #     sender = self.sender.username
    #     receiver = self.receiver
        

    )
    



@receiver(post_save,sender=User)
def create_user_profile(sender,instance,created,**kwargs):
    if created:
        
        if instance.user_type==1:
            Owner.__setattr__(owner =instance)
        if instance.user_type==2:
            Tenant.objects.create(identity =instance)

@receiver(post_save,sender=User)
def save_user_profile(sender,instance,**kwargs):
    if instance.user_type==1:
        instance.owner.save()
    if instance.user_type==2:
        instance.tenant.save()
  