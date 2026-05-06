import os
import secrets
import string

from django.contrib.auth.models import Group, Permission as AuthPermission
from django.core.management.base import BaseCommand
from django.db import transaction

from users.models import CustomUser, Role
from users.roles import RoleManager


ROLE_NAMES = ("admin", "supplier", "customer", "user")

DEFAULT_USERS = {
    "admin": {
        "email": "admin@example.com",
        "first_name": "Default",
        "last_name": "Admin",
        "mobile_no": "0000000000",
        "is_staff": True,
        "is_superuser": True,
    },
    "supplier": {
        "email": "supplier@example.com",
        "first_name": "Default",
        "last_name": "Supplier",
        "mobile_no": "0000000001",
    },
    "customer": {
        "email": "customer@example.com",
        "first_name": "Default",
        "last_name": "Customer",
        "mobile_no": "0000000002",
    },
    "user": {
        "email": "user@example.com",
        "first_name": "Default",
        "last_name": "User",
        "mobile_no": "0000000003",
    },
}


class Command(BaseCommand):
    help = "Create default roles, auth groups, and users for this ecommerce project."

    def add_arguments(self, parser):
        parser.add_argument(
            "--password",
            help=(
                "Password to set for newly created default users. If omitted, "
                "DEFAULT_USER_PASSWORD is used; otherwise a secure password is generated."
            ),
        )

    @transaction.atomic
    def handle(self, *args, **options):
        password = (
            options.get("password")
            or os.environ.get("DEFAULT_USER_PASSWORD")
            or self._generate_password()
        )
        generated_password = not (
            options.get("password") or os.environ.get("DEFAULT_USER_PASSWORD")
        )

        roles = self._create_roles()
        groups = self._create_groups()
        created_users = []
        existing_users = []

        for role_name, user_data in DEFAULT_USERS.items():
            role = roles[role_name]
            group = groups[role_name]
            defaults = {
                "first_name": user_data["first_name"],
                "last_name": user_data["last_name"],
                "mobile_no": user_data["mobile_no"],
                "user_role": role,
                "is_active": True,
                "is_staff": user_data.get("is_staff", False),
                "is_superuser": user_data.get("is_superuser", False),
            }

            user, created = CustomUser.objects.get_or_create(
                email=user_data["email"],
                defaults=defaults,
            )

            if created:
                user.set_password(password)
                user.save()
                created_users.append(user.email)
            else:
                changed = False
                if user.user_role_id is None:
                    user.user_role = role
                    changed = True
                if role_name == "admin":
                    if not user.is_staff:
                        user.is_staff = True
                        changed = True
                    if not user.is_superuser:
                        user.is_superuser = True
                        changed = True
                if changed:
                    user.save()
                existing_users.append(user.email)

            user.groups.add(group)

        self._write_summary(created_users, existing_users, password, generated_password)

    def _create_roles(self):
        roles = {}
        for role_name in ROLE_NAMES:
            role, _ = Role.objects.get_or_create(name=role_name)
            roles[role_name] = role
        return roles

    def _create_groups(self):
        groups = {}
        for role_name in ROLE_NAMES:
            RoleManager.create_permissions_for_role(role_name)
            group, _ = Group.objects.get_or_create(name=role_name)
            group.permissions.set(self._permissions_for_role(role_name))
            groups[role_name] = group
        return groups

    def _permissions_for_role(self, role_name):
        if role_name == "admin":
            return AuthPermission.objects.all()
        if role_name == "customer":
            return AuthPermission.objects.filter(codename="can_view_customer_dashboard")
        if role_name == "supplier":
            return AuthPermission.objects.filter(codename="can_view_supplier_dashboard")
        return AuthPermission.objects.none()

    def _generate_password(self):
        alphabet = string.ascii_letters + string.digits + "@$!%*?"
        while True:
            password = "".join(secrets.choice(alphabet) for _ in range(16))
            if (
                any(char.islower() for char in password)
                and any(char.isupper() for char in password)
                and any(char.isdigit() for char in password)
                and any(char in "@$!%*?" for char in password)
            ):
                return password

    def _write_summary(
        self, created_users, existing_users, password, generated_password
    ):
        for email in created_users:
            self.stdout.write(self.style.SUCCESS(f"Created default user: {email}"))

        for email in existing_users:
            self.stdout.write(f"Default user already exists: {email}")

        if created_users:
            self.stdout.write("")
            self.stdout.write("Password for newly created default users:")
            self.stdout.write(password)
            if generated_password:
                self.stdout.write(
                    self.style.WARNING(
                        "Store this generated password now; it will not be shown again."
                    )
                )
        else:
            self.stdout.write(self.style.SUCCESS("No default users needed creation."))
