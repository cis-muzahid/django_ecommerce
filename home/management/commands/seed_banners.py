from django.core.management.base import BaseCommand
from django.db import transaction

from home.models import Banner
from home.management.commands._seed_image_utils import save_seed_image
from products.models import Category
from users.models import CustomUser


BANNER_TYPE_HEADER = "header"
BANNER_TYPE_MIDDLE = "middle"
BANNER_TYPE_LOWER  = "lower"

# image_dest is the leaf filename passed to FieldFile.save().
# Django prepends Banner.image upload_to='banner/images/' automatically,
# so the final stored path becomes  banner/images/<image_dest>.
SEED_BANNERS = [
    {
        "title": "Summer Sale — Up to 50% Off",
        "subtitle": "Shop the hottest deals of the season",
        "description": (
            "Discover incredible savings across electronics, clothing, and more. "
            "Limited time offer — don't miss out!"
        ),
        "image_file": "ele.jpeg",
        "image_dest": "ele.jpeg",
        "category_name": "Electronics",
        "type": BANNER_TYPE_HEADER,
        "active": True,
    },
    {
        "title": "New Arrivals in Electronics",
        "subtitle": "The latest gadgets are here",
        "description": (
            "Explore our newest collection of smartphones, laptops, and accessories. "
            "Be the first to own the latest tech."
        ),
        "image_file": "ele_7Oylm9R.jpeg",
        "image_dest": "ele_7Oylm9R.jpeg",
        "category_name": "Electronics",
        "type": BANNER_TYPE_HEADER,
        "active": True,
    },
    {
        "title": "Fresh Fashion for Every Season",
        "subtitle": "Style that speaks for itself",
        "description": (
            "Browse our curated clothing collection for men, women, and kids. "
            "Quality fabrics, timeless designs."
        ),
        "image_file": "plantb.jpeg",
        "image_dest": "plantb.jpeg",
        "category_name": "Clothing & Apparel",
        "type": BANNER_TYPE_MIDDLE,
        "active": True,
    },
    {
        "title": "Transform Your Home",
        "subtitle": "Beautiful furniture & decor",
        "description": (
            "Upgrade your living space with our premium home and garden collection. "
            "Free delivery on orders over $100."
        ),
        "image_file": "plantb_Kfw5aCz.jpeg",
        "image_dest": "plantb_Kfw5aCz.jpeg",
        "category_name": "Home & Garden",
        "type": BANNER_TYPE_MIDDLE,
        "active": True,
    },
    {
        "title": "Health & Wellness Essentials",
        "subtitle": "Live better every day",
        "description": (
            "Stock up on vitamins, skincare, and personal care products. "
            "Your wellbeing is our priority."
        ),
        "image_file": "product.jpeg",
        "image_dest": "product.jpeg",
        "category_name": "Health & Beauty",
        "type": BANNER_TYPE_LOWER,
        "active": True,
    },
    {
        "title": "Weekend Flash Sale",
        "subtitle": "48 hours only — massive discounts",
        "description": (
            "Shop across all categories and save big this weekend. "
            "Deals refresh every hour."
        ),
        "image_file": "plantb_NhlayfP.jpeg",
        "image_dest": "plantb_NhlayfP.jpeg",
        "category_name": None,
        "type": BANNER_TYPE_LOWER,
        "active": True,
    },
]

SEED_SUBDIR = "banner"


class Command(BaseCommand):
    help = "Seed default banners (header, middle, lower) for the homepage."

    def handle(self, *args, **options):
        admin_user = self._get_admin_user()
        if admin_user is None:
            self.stdout.write(
                self.style.ERROR(
                    "No admin user found. Run 'create_default_users' first."
                )
            )
            return

        created_count  = 0
        updated_count  = 0
        image_warnings = 0

        for data in SEED_BANNERS:
            category = self._resolve_category(data["category_name"])
            existing = Banner.objects.filter(title=data["title"]).first()

            if existing:
                # ── UPDATE ────────────────────────────────────────────────
                # Sync non-image fields; re-upload image only if missing.
                with transaction.atomic():
                    existing.subtitle    = data["subtitle"]
                    existing.description = data["description"]
                    existing.category    = category
                    existing.type        = data["type"]
                    existing.active      = data["active"]
                    existing.save(update_fields=[
                        "subtitle", "description", "category", "type", "active"
                    ])

                if not (existing.image and existing.image.name):
                    ok = save_seed_image(
                        instance=existing,
                        field_name="image",
                        seed_subdir=SEED_SUBDIR,
                        filename=data["image_file"],
                        storage_upload_to=data["image_dest"],
                        stdout=self.stdout,
                        style=self.style,
                    )
                    if not ok:
                        image_warnings += 1

                updated_count += 1
                self.stdout.write(
                    f"  [=] Updated banner [{data['type']}]: {existing.title}"
                )

            else:
                # ── CREATE ────────────────────────────────────────────────
                # Step 1: insert the row without the image.
                # ImageField stores a varchar; an empty string is valid at the
                # DB level and lets us get a PK before calling FieldFile.save().
                with transaction.atomic():
                    banner = Banner.objects.create(
                        title=data["title"],
                        subtitle=data["subtitle"],
                        description=data["description"],
                        image="",           # placeholder — filled in step 2
                        user=admin_user,
                        category=category,
                        type=data["type"],
                        active=data["active"],
                    )

                # Step 2: upload through Django's storage backend.
                # FieldFile.save() is the only safe API — it never triggers
                # the path-traversal check that raw File assignment does.
                ok = save_seed_image(
                    instance=banner,
                    field_name="image",
                    seed_subdir=SEED_SUBDIR,
                    filename=data["image_file"],
                    storage_upload_to=data["image_dest"],
                    stdout=self.stdout,
                    style=self.style,
                )
                if not ok:
                    image_warnings += 1

                created_count += 1
                self.stdout.write(
                    self.style.SUCCESS(
                        f"  [+] Created banner [{data['type']}]: {data['title']}"
                    )
                )

        # ── Summary ───────────────────────────────────────────────────────
        self.stdout.write("")
        self.stdout.write(
            self.style.SUCCESS(
                f"Banners seeded: {created_count} created, {updated_count} updated."
            )
        )
        if image_warnings:
            self.stdout.write(
                self.style.WARNING(
                    f"  {image_warnings} banner(s) had missing seed images. "
                    "Add the files to seed_assets/banner/ and re-run."
                )
            )

    def _get_admin_user(self):
        user = CustomUser.objects.filter(is_superuser=True).first()
        if user is None:
            user = CustomUser.objects.filter(is_staff=True).first()
        return user

    def _resolve_category(self, name):
        if not name:
            return None
        return Category.objects.filter(name=name, is_delete=False).first()
