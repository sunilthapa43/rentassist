from django.db import models


from django.contrib.auth import get_user_model
User = get_user_model()
class ElectricityUnit(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=('User'), related_name='ImageToText')
    image =  models.ImageField(upload_to='static/meter-reader-images/', verbose_name=('meter image'), null=False)
    current_reading = models.DecimalField(verbose_name=('current meter reading'), decimal_places=1, max_digits=6, null = True, blank=True)
    current_units = models.DecimalField(verbose_name=('current units'), decimal_places=1, max_digits=6, null = True, blank=True)
    previous_month_reading = models.DecimalField(verbose_name=('previous meter reading'), decimal_places=1, max_digits=6, null = True, blank=True)
    previous_month_units = models.DecimalField(verbose_name=('previous month units'), decimal_places=1, max_digits=6, null = True, blank=True)
    

    payment_status = models.BooleanField(default=False)
    # if not paid add the previous month units to current units
    total_payable_units = models.DecimalField(decimal_places=1,max_digits=5, blank=True)

    def __str__(self):
        return self.user.username
    
    # todo migrations ocr