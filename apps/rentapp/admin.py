from django.contrib import admin
from .models import  Complaint, Rent


@admin.register(Rent)
class RentAdmin(admin.ModelAdmin):
    list_display = (
        'tenant',
        'this_month_rent',
        'amount_to_be_paid',
        'amount_paid_this_month', 
        'due_amount',
        'status',
        'paid_at'  
    )
    fields = (
        'tenant',
        'this_month_rent',
        'amount_to_be_paid',
        'amount_paid_this_month', 
        'due_amount',
        'status',
        'paid_at'  
    )

    readonly_fields = ('paid_at', 'next_payment_schedule')
      

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




