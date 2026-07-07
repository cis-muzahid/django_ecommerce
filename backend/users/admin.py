from django.contrib import admin

from .models import *


class AdminRole(admin.ModelAdmin):
    fields = ['name', 'permissions']

class AdminPersmission(admin.ModelAdmin):
    fields = ['name']

class AdminUserAdress(admin.ModelAdmin):
    fields = ['city']

admin.site.register(Role, AdminRole)
admin.site.register(Permission, AdminPersmission)
admin.site.register(UserAddress, AdminUserAdress)
