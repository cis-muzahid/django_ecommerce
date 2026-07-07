from django.core.management.base import BaseCommand
from django.db import transaction

from products.models import Category
from users.models import CustomUser


# ---------------------------------------------------------------------------
# Seed data
# ---------------------------------------------------------------------------

# Top-level categories (no parent)
TOP_LEVEL_CATEGORIES = [
    "Electronics",
    "Clothing & Apparel",
    "Home & Garden",
    "Sports & Outdoors",
    "Books & Media",
    "Health & Beauty",
    "Toys & Games",
    "Food & Groceries",
]

# Sub-categories: {parent_name: [child_name, ...]}
SUB_CATEGORIES = {
    "Electronics": [
        "Mobile Phones",
        "Laptops & Computers",
        "Cameras & Photography",
        "Audio & Headphones",
        "TV & Home Theatre",
    ],
    "Clothing & Apparel": [
        "Men's Clothing",
        "Women's Clothing",
        "Kids' Clothing",
        "Footwear",
        "Accessories",
    ],
    "Home & Garden": [
        "Furniture",
        "Kitchen & Dining",
        "Bedding & Bath",
        "Garden & Outdoor",
        "Home Decor",
    ],
    "Sports & Outdoors": [
        "Exercise & Fitness",
        "Outdoor Recreation",
        "Team Sports",
        "Water Sports",
    ],
    "Books & Media": [
        "Books",
        "Music",
        "Movies & TV",
        "Video Games",
    ],
    "Health & Beauty": [
        "Skincare",
        "Hair Care",
        "Vitamins & Supplements",
        "Personal Care",
    ],
    "Toys & Games": [
        "Action Figures",
        "Board Games",
        "Educational Toys",
        "Outdoor Play",
    ],
    "Food & Groceries": [
        "Fresh Produce",
        "Dairy & Eggs",
        "Snacks & Beverages",
        "Organic & Natural",
    ],
}


class Command(BaseCommand):
    help = "Seed default product categories and sub-categories."

    @transaction.atomic
    def handle(self, *args, **options):
        admin_user = self._get_admin_user()
        if admin_user is None:
            self.stdout.write(
                self.style.ERROR(
                    "No admin user found. Run 'create_default_users' first."
                )
            )
            return

        created_top = 0
        existing_top = 0
        created_sub = 0
        existing_sub = 0

        # --- Top-level categories ---
        parent_map = {}
        for name in TOP_LEVEL_CATEGORIES:
            category, created = Category.objects.get_or_create(
                name=name,
                defaults={"parent_category": None, "user": admin_user, "is_delete": False},
            )
            parent_map[name] = category
            if created:
                created_top += 1
                self.stdout.write(self.style.SUCCESS(f"  [+] Created category: {name}"))
            else:
                existing_top += 1
                self.stdout.write(f"  [=] Category already exists: {name}")

        # --- Sub-categories ---
        for parent_name, children in SUB_CATEGORIES.items():
            parent = parent_map.get(parent_name)
            if parent is None:
                self.stdout.write(
                    self.style.WARNING(f"  [!] Parent category not found: {parent_name}")
                )
                continue

            for child_name in children:
                child, created = Category.objects.get_or_create(
                    name=child_name,
                    defaults={
                        "parent_category": parent,
                        "user": admin_user,
                        "is_delete": False,
                    },
                )
                if created:
                    created_sub += 1
                    self.stdout.write(
                        self.style.SUCCESS(f"    [+] Created sub-category: {child_name} -> {parent_name}")
                    )
                else:
                    existing_sub += 1
                    self.stdout.write(f"    [=] Sub-category already exists: {child_name}")

        # --- Summary ---
        self.stdout.write("")
        self.stdout.write(
            self.style.SUCCESS(
                f"Categories seeded: {created_top} top-level created, "
                f"{existing_top} already existed."
            )
        )
        self.stdout.write(
            self.style.SUCCESS(
                f"Sub-categories seeded: {created_sub} created, "
                f"{existing_sub} already existed."
            )
        )

    # -----------------------------------------------------------------------
    # Helpers
    # -----------------------------------------------------------------------

    def _get_admin_user(self):
        """Return the first superuser, or the first staff user, or None."""
        user = CustomUser.objects.filter(is_superuser=True).first()
        if user is None:
            user = CustomUser.objects.filter(is_staff=True).first()
        return user
