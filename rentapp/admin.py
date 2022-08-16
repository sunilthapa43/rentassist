from django.contrib import admin
from .models import Notification, OtherPayment, Owner, Tenant, Transaction, Rent, Agreement, Complaint, Document, Deposit, Electricity, Chat


# Register your models here.


@admin.register(Owner)
class RatingAdmin(admin.ModelAdmin):
    list_display = (
        'owner',
        'email',
        'phone_number',
        'balance'
        
    )
    fields = (
        'owner',
        'email',
        'phone_number',
        'balance'
    )
admin.site.register(Tenant)
admin.site.register(Transaction)
admin.site.register(Rent)
admin.site.register(Deposit)
admin.site.register(Chat)
admin.site.register(Complaint)
admin.site.register(Notification)
admin.site.register(Electricity)
admin.site.register(Agreement)
admin.site.register(Document)
admin.site.register(OtherPayment)
