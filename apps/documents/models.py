from datetime import datetime, timedelta
from django.db import models
from django.contrib.auth import get_user_model

from notification.models import Notification


User = get_user_model()
class Document(models.Model):
    user =  models.ForeignKey(User, on_delete=models.CASCADE,related_name='document')
    citizenship = models.FileField(upload_to='static/docs', verbose_name="citizenship", blank=False, null=False)


class Agreement(models.Model):
    tenant = models.ForeignKey('users.Tenant', on_delete=models.CASCADE, related_name='agreement', verbose_name='tenant_user')
    price = models.IntegerField(verbose_name='rent amount', null=False, blank=False)
    internet_price = models.IntegerField(verbose_name = 'Internet Price', default=0)
    water_usage_price = models.IntegerField( null=False, verbose_name = 'water_usage_price')
    nagarpalika_fohr_price = models.IntegerField( null=False, blank=False, verbose_name = 'Nagarpalika Fohr Price',)
    electricity_rate = models.IntegerField( verbose_name='electricity charge per unit')
    created =  models.DateField(auto_now= True)
    updated = models.DateField(auto_now_add=True)# auto now add
    deadline =  models.DateField(default=datetime.now().date()+timedelta(days=30))

    def __str__(self) -> str:
        return f'Agreement on rent between {self.tenant} and {self.tenant.owner.owner.username}'

    def total_price(self, electricity_unit):
        price = self.price + self.internet_price + self.water_usage_price + self.nagarpalika_fohr_price + self.electricity_rate*electricity_unit
        return price

    def create_notification(self, days, flag):
        if days == -1 and flag == 1:
            type = 'C'
            target = self.tenant.owner.owner
            title = f'The rental Contract with {self.tenant} been expired yesterday'
        if days == -1 and flag == 0:
            type = 'C'
            target = self.tenant.tenant
            title = f'Your rental contract has been ended yesterday' 
        elif days == 0 and flag == 1:
            type = 'C'
            target = self.tenant.owner.owner
            title = f'The rental contract of {self.tenant} expires today'
        elif days == 0 and flag == 0:
            type = 'C'
            target = self.tenant.tenant
            title = f'Your rental contract expires today'
        type = type 
        obj = Notification.objects.create(
            tenant = self.tenant,
            is_read = False,
            title = title,
            type = type ,
            target = target
        )
        obj.save()