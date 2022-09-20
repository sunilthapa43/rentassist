from django.contrib import admin
from .models import  Complaint, Rent
from .models import Room


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
        'urgency_level',
        'is_solved',
        'status'

    )
    fields = (
        'tenant',
        'title',
        'image',
        'description',
        'urgency_level',
        'is_solved',
        'status'

    )

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = (
        'owner',
        'price',
        'internet_price',
        'water_usage_price',
        'nagarpalika_fohr_price',
        'electricity_rate',
          
    )
    fields = (
        'owner',
        'price',
        'internet_price',
        'water_usage_price',
        'nagarpalika_fohr_price',
        'electricity_rate',
        
        
    )
    readonly_fields = ['created','updated']
