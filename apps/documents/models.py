from django.db import models
from django.contrib.auth import get_user_model


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
    deadline =  models.DateField()

    def __str__(self) -> str:
        return f'Agreement on rent between {self.tenant} and {self.tenant.owner.owner.username}'

    def total_price(self, electricity_unit):
        price = self.price + self.internet_price + self.water_usage_price + self.nagarpalika_fohr_price + self.electricity_rate*electricity_unit
        return price