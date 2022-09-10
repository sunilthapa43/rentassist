from django.contrib import admin
from .models import Agreement, Document

@admin.register(Agreement)
class AgreementAdmin(admin.ModelAdmin):
    list_display = (
        'tenant',
        'price',
        'internet_price',
        'water_usage_price',
        'nagarpalika_fohr_price',
        'electricity_rate',
        'deadline',   
    )
    fields = (
        'tenant',
        'price',
        'internet_price',
        'water_usage_price',
        'nagarpalika_fohr_price',
        'electricity_rate',
        'deadline', 
        
    )
    readonly_fields = ['created','updated']

admin.site.register(Document)