from django.contrib import admin
from .models import Agreement, Document

@admin.register(Agreement)
class AgreementAdmin(admin.ModelAdmin):
    list_display = (
        'tenant',
        'created',
        'updated',
        'deadline',   
    )
    fields = (
        'tenant',
        'created',
        'updated',
        'deadline', 
    )


admin.site.register(Document)