from django.contrib import admin
from .models import CustomUser

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
