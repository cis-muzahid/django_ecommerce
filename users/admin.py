from django.contrib import admin

from .models import *


class AdminRole(admin.ModelAdmin):
    fields = ['name', 'permissions']

class AdminPersmission(admin.ModelAdmin):
    fields = ['name']


admin.site.register(Role, AdminRole)
admin.site.register(Permission, AdminPersmission)