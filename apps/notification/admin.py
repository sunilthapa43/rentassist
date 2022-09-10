from django.contrib import admin

from .models import Notification

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = (
        'created',
        'tenant',
        'is_read',
        'title' ,
        'type',
        'target'
    )

   
    fields= (
        'created', 
        'tenant',
        'is_read',
        'title' ,
        'type',
        'target',
    )
    readonly_fields = ('created',)