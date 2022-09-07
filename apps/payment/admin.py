from django.contrib import admin

from .models import Transaction

# Register your models here.
@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = (
        'initiator',
        'amount',
        'payment_token',
        'transaction_status',
        'payment_response'

    )
    fields = ( 
        'initiator',
        'amount',
        'payment_token',
        'transaction_status',
        'payment_response'
    )

