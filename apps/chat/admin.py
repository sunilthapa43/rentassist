from django.contrib import admin
from .models import Message
@admin.register(Message)
class ChatAdmin(admin.ModelAdmin):
    list_display = (
        'sender',
        'receiver',
        'message',
        'is_read', 
         
    )
    fields = (
        'sender',
        'receiver',
        'message',
        'is_read' 
    )
