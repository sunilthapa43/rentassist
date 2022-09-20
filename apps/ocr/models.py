from django.db import models


class ElectricityUnit(models.Model):
    tenant = models.ForeignKey('users.Tenant', on_delete=models.CASCADE, verbose_name='tenant')
   
    current_reading = models.DecimalField(verbose_name=('current meter reading'), decimal_places=1, max_digits=6, null = True, blank=True)
    current_units = models.DecimalField(verbose_name=('current units'), decimal_places=1, max_digits=6, null = True, blank=True)
    previous_month_reading = models.DecimalField(verbose_name=('previous meter reading'), decimal_places=1, max_digits=6, null = True, blank=True)
    previous_month_units = models.DecimalField(verbose_name=('previous month units'), decimal_places=1, max_digits=6, null = True, blank=True)

    def __str__(self):
        units = self.current_units or 0
        return f'{self.tenant} used {units} units this month'

    

class Ocr(models.Model):
    image = models.ImageField(upload_to='static/meter-reader-images/', verbose_name=('meter image'), null=False)
    image_name = models.CharField(blank=False, max_length=50)
    extracted_digits = models.DecimalField(max_digits=7, decimal_places=1, default=12345.4)





