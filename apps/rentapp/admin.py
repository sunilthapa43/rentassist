from django.contrib import admin
from .models import Notification, Tenant, Complaint, Deposit


@admin.register(Tenant)
class TenantAdmin(admin.ModelAdmin):
    list_display = (
        
        'tenant',
        'owner',
        'is_tenant'
   
    )
    fields = (
        
        'tenant',
        'owner',
        'is_tenant'
    
    )




@admin.register(Deposit)
class DepositAdmin(admin.ModelAdmin):
    list_display = (
        'tenant',
        'amount',
        'title',
        'remarks', 
        'date'  
    )
    fields = (
        'tenant',
        'amount',
        'title',
        'remarks',
        'date' 
    )

admin.site.register(Complaint)
admin.site.register(Notification)

