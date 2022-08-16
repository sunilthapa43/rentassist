from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Owner(models.Model):
    owner = models.ForeignKey(User, on_delete= models.CASCADE)
    uname =  models.CharField(max_length=255)

    def __str__(self):
        return self.uname


class Tenant(models.Model):
    owner = models.ForeignKey(Owner, on_delete= models.CASCADE)
    fullname = models.CharField(max_length=35)
   

    def __str__(self):
        return self.fullname