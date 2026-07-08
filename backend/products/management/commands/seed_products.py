from django.core.management.base import BaseCommand
from django.db import transaction

from products.models import Category, Product
from users.models import CustomUser


# ---------------------------------------------------------------------------
# Seed data
# Each entry maps to a Product row.
# Fields: name, description, price, weight, length, width, height,
#         tag, category_name, slug
# ---------------------------------------------------------------------------

SEED_PRODUCTS = [
    {
        "name": "iPhone 15 Pro",
        "description": (
            "Apple iPhone 15 Pro with A17 Pro chip, titanium design, "
            "48 MP main camera, and USB-C connectivity."
        ),
        "price": "999.99",
        "weight": "0.19",
        "length": "14.67",
        "width": "7.09",
        "height": "0.83",
        "tag": "apple,iphone,smartphone,mobile",
        "category_name": "Mobile Phones",
        "slug": "iphone-15-pro",
    },
    {
        "name": "Samsung Galaxy S24 Ultra",
        "description": (
            "Samsung Galaxy S24 Ultra with Snapdragon 8 Gen 3, "
            "200 MP camera, built-in S Pen, and 5000 mAh battery."
        ),
        "price": "1199.99",
        "weight": "0.23",
        "length": "16.28",
        "width": "7.92",
        "height": "0.86",
        "tag": "samsung,galaxy,android,smartphone",
        "category_name": "Mobile Phones",
        "slug": "samsung-galaxy-s24-ultra",
    },
    {
        "name": "Dell XPS 15 Laptop",
        "description": (
            "Dell XPS 15 with Intel Core i7, 16 GB RAM, 512 GB SSD, "
            "OLED display, and NVIDIA GeForce RTX 4060."
        ),
        "price": "1799.99",
        "weight": "1.86",
        "length": "34.40",
        "width": "23.00",
        "height": "1.80",
        "tag": "dell,laptop,xps,windows",
        "category_name": "Laptops & Computers",
        "slug": "dell-xps-15-laptop",
    },
    {
        "name": "Sony WH-1000XM5 Headphones",
        "description": (
            "Industry-leading noise cancelling wireless headphones with "
            "30-hour battery life and multipoint connection."
        ),
        "price": "349.99",
        "weight": "0.25",
        "length": "19.00",
        "width": "17.00",
        "height": "7.50",
        "tag": "sony,headphones,wireless,noise-cancelling",
        "category_name": "Audio & Headphones",
        "slug": "sony-wh-1000xm5-headphones",
    },
    {
        "name": "Canon EOS R6 Mark II",
        "description": (
            "Full-frame mirrorless camera with 40 fps burst shooting, "
            "6K RAW video, and advanced subject tracking."
        ),
        "price": "2499.99",
        "weight": "0.67",
        "length": "13.83",
        "width": "9.80",
        "height": "8.28",
        "tag": "canon,camera,mirrorless,photography",
        "category_name": "Cameras & Photography",
        "slug": "canon-eos-r6-mark-ii",
    },
    {
        "name": "Men's Classic Fit T-Shirt",
        "description": (
            "100% cotton classic fit crew-neck t-shirt, available in "
            "multiple colours. Machine washable."
        ),
        "price": "19.99",
        "weight": "0.20",
        "length": "70.00",
        "width": "50.00",
        "height": "0.50",
        "tag": "tshirt,men,cotton,casual",
        "category_name": "Men's Clothing",
        "slug": "mens-classic-fit-tshirt",
    },
    {
        "name": "Women's Running Shoes",
        "description": (
            "Lightweight and breathable running shoes with responsive "
            "cushioning and durable rubber outsole."
        ),
        "price": "89.99",
        "weight": "0.30",
        "length": "28.00",
        "width": "10.00",
        "height": "4.00",
        "tag": "shoes,women,running,sports",
        "category_name": "Footwear",
        "slug": "womens-running-shoes",
    },
    {
        "name": "Yoga Mat Premium",
        "description": (
            "Non-slip 6 mm thick yoga mat with alignment lines, "
            "eco-friendly TPE material, includes carry strap."
        ),
        "price": "45.99",
        "weight": "1.20",
        "length": "183.00",
        "width": "61.00",
        "height": "0.60",
        "tag": "yoga,fitness,mat,exercise",
        "category_name": "Exercise & Fitness",
        "slug": "yoga-mat-premium",
    },
    {
        "name": "Organic Green Tea (100g)",
        "description": (
            "Premium organic green tea leaves sourced from certified "
            "farms. Rich in antioxidants, smooth flavour."
        ),
        "price": "12.99",
        "weight": "0.10",
        "length": "10.00",
        "width": "7.00",
        "height": "5.00",
        "tag": "tea,organic,green-tea,health",
        "category_name": "Organic & Natural",
        "slug": "organic-green-tea-100g",
    },
    {
        "name": "LEGO Classic Creative Bricks",
        "description": (
            "900-piece LEGO classic set with a wide range of bricks "
            "in 33 colours. Suitable for ages 4 and up."
        ),
        "price": "59.99",
        "weight": "1.10",
        "length": "37.80",
        "width": "26.20",
        "height": "9.40",
        "tag": "lego,toys,kids,creative",
        "category_name": "Toys & Games",
        "slug": "lego-classic-creative-bricks",
    },
    {
        "name": "Fresh Organic Apples (1kg)",
        "description": (
            "Crisp and juicy organic apples packed fresh for daily snacking "
            "and healthy meals."
        ),
        "price": "4.99",
        "weight": "1.00",
        "length": "10.00",
        "width": "10.00",
        "height": "10.00",
        "tag": "apples,organic,fruit,groceries",
        "category_name": "Fresh Produce",
        "slug": "fresh-organic-apples-1kg",
    },
    {
        "name": "Classic Peanut Butter 500g",
        "description": (
            "Smooth peanut butter made from roasted peanuts with a rich "
            "and creamy texture for sandwiches and baking."
        ),
        "price": "3.49",
        "weight": "0.50",
        "length": "8.00",
        "width": "6.00",
        "height": "12.00",
        "tag": "peanut-butter,spread,grocery,food",
        "category_name": "Snacks & Beverages",
        "slug": "classic-peanut-butter-500g",
    },
]


class Command(BaseCommand):
    help = "Seed default products into the database."

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

        created_count = 0
        updated_count = 0
        skipped_count = 0

        for data in SEED_PRODUCTS:
            category = self._resolve_category(data["category_name"], admin_user)
            if category is None:
                self.stdout.write(
                    self.style.WARNING(
                        f"  [!] Category '{data['category_name']}' not found — "
                        f"skipping product '{data['name']}'. "
                        "Run 'seed_categories' first."
                    )
                )
                skipped_count += 1
                continue

            defaults = {
                "name": data["name"],
                "description": data["description"],
                "price": data["price"],
                "weight": data["weight"],
                "length": data["length"],
                "width": data["width"],
                "height": data["height"],
                "tag": data["tag"],
                "category": category,
                "user": admin_user,
                "is_delete": False,
            }

            product, created = Product.objects.update_or_create(
                slug=data["slug"],
                defaults=defaults,
            )

            if created:
                created_count += 1
                self.stdout.write(
                    self.style.SUCCESS(f"  [+] Created product: {product.name}")
                )
            else:
                updated_count += 1
                self.stdout.write(f"  [=] Updated product: {product.name}")

        # --- Summary ---
        self.stdout.write("")
        self.stdout.write(
            self.style.SUCCESS(
                f"Products seeded: {created_count} created, "
                f"{updated_count} updated, {skipped_count} skipped."
            )
        )

    # -----------------------------------------------------------------------
    # Helpers
    # -----------------------------------------------------------------------

    def _get_admin_user(self):
        user = CustomUser.objects.filter(is_superuser=True).first()
        if user is None:
            user = CustomUser.objects.filter(is_staff=True).first()
        return user

    def _resolve_category(self, name, admin_user):
        """Return existing Category by name, or create it as a top-level category."""
        category, _ = Category.objects.get_or_create(
            name=name,
            defaults={"parent_category": None, "user": admin_user, "is_delete": False},
        )
        return category
