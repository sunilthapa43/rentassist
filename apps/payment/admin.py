from django.contrib import admin

from .models import AllTransaction, Deposit, OtherPayment, Transaction

# Register your models here.
@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = (
        'initiator',
        'paid_amount',
        'payment_token',
        'transaction_status',
        'payment_response'

    )
    fields = ( 
        'initiator',
        'paid_amount',
        'payment_token',
        'transaction_status',
        'payment_response'
    )

@admin.register(OtherPayment)
class OtherPaymentAdmin(admin.ModelAdmin):
    list_display = (
        'initiator',
        'amount',
        'remarks',

    )
    fields = ( 
        'initiator',
        'amount',
        'remarks',
    )

@admin.register(AllTransaction)
class AllTransactionAdmin(admin.ModelAdmin):
    list_display = (
        'initiator',
        'amount',
        'medium',

    )
    fields = ( 
        'initiator',
        'amount',
        'medium',
    )

@admin.register(Deposit)
class DepositAdmin(admin.ModelAdmin):
    list_display = (
        'owner',
        'amount'
    )