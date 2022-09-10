from django.db import models


class ElectricityUnit(models.Model):
    tenant = models.ForeignKey('users.Tenant', on_delete=models.PROTECT, verbose_name='tenant')
    image = models.ImageField(upload_to='static/meter-reader-images/', verbose_name=('meter image'), null=False)
    current_reading = models.DecimalField(verbose_name=('current meter reading'), decimal_places=1, max_digits=6, null = True, blank=True)
    current_units = models.DecimalField(verbose_name=('current units'), decimal_places=1, max_digits=6, null = True, blank=True)
    previous_month_reading = models.DecimalField(verbose_name=('previous meter reading'), decimal_places=1, max_digits=6, null = True, blank=True)
    previous_month_units = models.DecimalField(verbose_name=('previous month units'), decimal_places=1, max_digits=6, null = True, blank=True)

    def __str__(self):
        return f'{self.tenant} used {self.current_units} units this month'

    
    



