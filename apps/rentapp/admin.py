from django.contrib import admin
from .models import  Complaint, Deposit


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

@admin.register(Complaint)
class ComplaintAdmin(admin.ModelAdmin):
    list_display = (
        'tenant',
        'title',
        'image',
        'description', 
        'urgency_level'  
    )
    fields = (
        'tenant',
        'title',
        'image',
        'description',
        'urgency_level' 
    )




