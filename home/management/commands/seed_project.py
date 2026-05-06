"""
seed_project.py
---------------
Master seed command. Runs all individual seed commands in dependency order.

Usage
-----
    python manage.py seed_project
    python manage.py seed_project --password=MySecret123!

Safe to run multiple times — every individual command is idempotent.
"""

from django.core.management import call_command
from django.core.management.base import BaseCommand


# Ordered list: each tuple is (management_command_name, human_readable_label).
# Order matters — later commands depend on earlier ones.
SEED_PIPELINE = [
    ("create_default_users",    "Default roles, groups & users"),
    ("seed_categories",         "Product categories & sub-categories"),
    ("seed_products",           "Products"),
    ("seed_product_attributes", "Product attributes (colour, size, storage …)"),
    ("seed_banners",            "Homepage banners"),
    ("seed_blogs",              "Blog categories & posts"),
    ("seed_facility",           "Facility / trust-badge entries"),
]

DIVIDER = "=" * 62


class Command(BaseCommand):
    help = (
        "Run the full seed pipeline in dependency order. "
        "Idempotent — safe to run multiple times."
    )

    def add_arguments(self, parser):
        parser.add_argument(
            "--password",
            help=(
                "Password forwarded to 'create_default_users'. "
                "Falls back to the DEFAULT_USER_PASSWORD env var, "
                "then auto-generates a secure password."
            ),
        )

    def handle(self, *args, **options):
        self.stdout.write(self.style.MIGRATE_HEADING(DIVIDER))
        self.stdout.write(self.style.MIGRATE_HEADING("  Django Ecommerce — Full Seed Pipeline"))
        self.stdout.write(self.style.MIGRATE_HEADING(DIVIDER))
        self.stdout.write("")

        errors = []

        for command_name, label in SEED_PIPELINE:
            self.stdout.write(
                self.style.MIGRATE_HEADING(f"▶  {label}  ({command_name})")
            )
            self.stdout.write(self.style.MIGRATE_HEADING("-" * 62))

            try:
                kwargs = {"stdout": self.stdout, "stderr": self.stderr}

                # Forward --password only to the command that accepts it.
                if command_name == "create_default_users" and options.get("password"):
                    kwargs["password"] = options["password"]

                call_command(command_name, **kwargs)

            except Exception as exc:  # noqa: BLE001
                msg = f"[ERROR] '{command_name}' raised: {exc}"
                self.stdout.write(self.style.ERROR(msg))
                errors.append(msg)

            self.stdout.write("")

        # --- Final report ---
        self.stdout.write(self.style.MIGRATE_HEADING(DIVIDER))
        if errors:
            self.stdout.write(
                self.style.ERROR(
                    f"  Seed pipeline finished with {len(errors)} error(s):"
                )
            )
            for err in errors:
                self.stdout.write(self.style.ERROR(f"    {err}"))
        else:
            self.stdout.write(
                self.style.SUCCESS("  Seed pipeline completed successfully.")
            )
        self.stdout.write(self.style.MIGRATE_HEADING(DIVIDER))
