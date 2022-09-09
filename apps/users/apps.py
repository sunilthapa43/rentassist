from django.apps import AppConfig
from django.db.models.signals import post_save, pre_save
from django.core.signals import request_finished
class UsersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'users'

    def ready(self):
        from . import signals
        
        

