from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()
class Document(models.Model):
    user =  models.ForeignKey(User, on_delete=models.CASCADE,related_name='document')
    citizenship = models.FileField(upload_to='static/docs', verbose_name="citizenship", blank=False, null=False)


class Agreement(models.Model):
    tenant = models.ForeignKey('users.Tenant', on_delete=models.CASCADE, related_name='agreement')
    created =  models.DateField(auto_now= True)
    updated = models.DateField()# auto now add
    deadline =  models.DateField()