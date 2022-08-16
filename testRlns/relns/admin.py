from django.contrib.auth.admin import UserAdmin
from django.contrib import admin
from .models import Chat, Owner, Tenant, User
# Register your models here.


class UserModel(UserAdmin):
    pass

admin.site.register(User, UserModel)
admin.site.register(Owner)
admin.site.register(Tenant)
admin.site.register(Chat)


