from django.contrib import admin
from .models import CustomUser, Tenant, Owner

@admin.register(CustomUser)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        'username',
        'email',
        'is_owner',
        'phone_number',
        'image'
    )
    
    fields = (
        'username',
        'email',
        'is_owner',
        'phone_number',
        'image'       
    )

@admin.register(Tenant)
class TenantAdmin(admin.ModelAdmin):
    list_display = (

        'tenant',
        'owner',
        )
    fields = (

        'tenant',
        'owner',
        )

admin.site.register(Owner)