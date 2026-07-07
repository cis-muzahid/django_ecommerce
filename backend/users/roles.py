# roles.py

from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from users.models import CustomUser  # Import your CustomUser model
from products.models import Product  # Import your Product model


class RoleManager:
    @staticmethod
    def create_permissions_for_role(role):
        permissions = []

        if role == 'admin':
            permissions = Permission.objects.all()
        elif role == 'customer':
            permissions = Permission.objects.filter(codename='can_view_customer_dashboard')
        elif role == 'supplier':
            permissions = Permission.objects.filter(codename='can_view_supplier_dashboard')

        for permission in permissions:
            RoleManager.create_or_update_permission(permission.codename, permission.name)

    @staticmethod
    def create_or_update_permission(codename, name):
        content_types = ContentType.objects.filter(app_label__in=['users', 'products', 'home'])
        
        for content_type in content_types:
            permission, created = Permission.objects.get_or_create(
                codename=codename,
                name=name,
                content_type=content_type,
            )

    @staticmethod
    def create_content_type(app_label, model):
        content_type, created = ContentType.objects.get_or_create(
            app_label=app_label,
            model=model,
        )
        return content_type
