from django.db import models
from django.contrib.auth import get_user_model

from rentapp.models import Tenant

User = get_user_model()
class Document(models.Model):
    user =  models.ForeignKey(User, on_delete=models.CASCADE,related_name='document')
    citizenship = models.FileField(upload_to='static/docs', verbose_name="citizenship")


class Agreement(models.Model):
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name='agreement')
    created =  models.DateField(auto_now= True)
    updated = models.DateTimeField(auto_now_add= True)
    deadline =  models.DateField()