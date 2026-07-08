from django.core.management.base import BaseCommand
from django.db import transaction

from home.management.commands._seed_image_utils import save_seed_image
from products.models import Product, ProductAttribute


# ---------------------------------------------------------------------------
# Seed data
#
# product_slug -> list of attribute dicts
# Fields:
#   title        : attribute name  (e.g. "color", "size", "storage", "RAM")
#   value        : attribute value (e.g. "Blue", "128 GB")
#   image_file   : filename inside seed_assets/products/  (empty string = no image)
#   image_dest   : storage path passed to FieldFile.save()
#   out_of_stoke : bool
#   is_display   : bool
# ---------------------------------------------------------------------------

SEED_ATTRIBUTES = {
    "iphone-15-pro": [
        {
            "title": "color",
            "value": "Natural Titanium",
            "image_file": "1887.jpeg",
            "image_dest": "1887.jpeg",
            "out_of_stoke": False,
            "is_display": True,
        },
        {
            "title": "color",
            "value": "Black Titanium",
            "image_file": "1887_f7aIwQ8.jpeg",
            "image_dest": "1887_f7aIwQ8.jpeg",
            "out_of_stoke": False,
            "is_display": True,
        },
        {
            "title": "storage",
            "value": "128 GB",
            "image_file": "",
            "image_dest": "",
            "out_of_stoke": False,
            "is_display": True,
        },
        {
            "title": "storage",
            "value": "256 GB",
            "image_file": "",
            "image_dest": "",
            "out_of_stoke": False,
            "is_display": True,
        },
        {
            "title": "storage",
            "value": "512 GB",
            "image_file": "",
            "image_dest": "",
            "out_of_stoke": True,
            "is_display": True,
        },
    ],
    "samsung-galaxy-s24-ultra": [
        {
            "title": "color",
            "value": "Titanium Black",
            "image_file": "images.jpeg",
            "image_dest": "images.jpeg",
            "out_of_stoke": False,
            "is_display": True,
        },
        {
            "title": "color",
            "value": "Titanium Gray",
            "image_file": "images.jpeg",
            "image_dest": "images.jpeg",
            "out_of_stoke": False,
            "is_display": True,
        },
        {
            "title": "storage",
            "value": "256 GB",
            "image_file": "",
            "image_dest": "",
            "out_of_stoke": False,
            "is_display": True,
        },
        {
            "title": "storage",
            "value": "512 GB",
            "image_file": "",
            "image_dest": "",
            "out_of_stoke": False,
            "is_display": True,
        },
    ],
    "dell-xps-15-laptop": [
        {
            "title": "color",
            "value": "Platinum Silver",
            "image_file": "laptop.jpg",
            "image_dest": "laptop.jpg",
            "out_of_stoke": False,
            "is_display": True,
        },
        {
            "title": "RAM",
            "value": "16 GB",
            "image_file": "",
            "image_dest": "",
            "out_of_stoke": False,
            "is_display": True,
        },
        {
            "title": "RAM",
            "value": "32 GB",
            "image_file": "",
            "image_dest": "",
            "out_of_stoke": False,
            "is_display": True,
        },
        {
            "title": "storage",
            "value": "512 GB SSD",
            "image_file": "",
            "image_dest": "",
            "out_of_stoke": False,
            "is_display": True,
        },
        {
            "title": "storage",
            "value": "1 TB SSD",
            "image_file": "",
            "image_dest": "",
            "out_of_stoke": True,
            "is_display": True,
        },
    ],
    "sony-wh-1000xm5-headphones": [
        {
            "title": "color",
            "value": "Black",
            "image_file": "images.jpeg",
            "image_dest": "images.jpeg",
            "out_of_stoke": False,
            "is_display": True,
        },
        {
            "title": "color",
            "value": "Silver",
            "image_file": "images.jpeg",
            "image_dest": "images.jpeg",
            "out_of_stoke": False,
            "is_display": True,
        },
    ],
    "mens-classic-fit-tshirt": [
        {
            "title": "color",
            "value": "White",
            "image_file": "nature.jpg",
            "image_dest": "nature.jpg",
            "out_of_stoke": False,
            "is_display": True,
        },
        {
            "title": "color",
            "value": "Black",
            "image_file": "nature.jpg",
            "image_dest": "nature.jpg",
            "out_of_stoke": False,
            "is_display": True,
        },
        {
            "title": "color",
            "value": "Navy Blue",
            "image_file": "nature.jpg",
            "image_dest": "nature.jpg",
            "out_of_stoke": False,
            "is_display": True,
        },
        {
            "title": "size",
            "value": "S",
            "image_file": "",
            "image_dest": "",
            "out_of_stoke": False,
            "is_display": True,
        },
        {
            "title": "size",
            "value": "M",
            "image_file": "",
            "image_dest": "",
            "out_of_stoke": False,
            "is_display": True,
        },
        {
            "title": "size",
            "value": "L",
            "image_file": "",
            "image_dest": "",
            "out_of_stoke": False,
            "is_display": True,
        },
        {
            "title": "size",
            "value": "XL",
            "image_file": "",
            "image_dest": "",
            "out_of_stoke": True,
            "is_display": True,
        },
    ],
    "womens-running-shoes": [
        {
            "title": "color",
            "value": "Pink",
            "image_file": "nature.jpg",
            "image_dest": "nature.jpg",
            "out_of_stoke": False,
            "is_display": True,
        },
        {
            "title": "color",
            "value": "White",
            "image_file": "nature.jpg",
            "image_dest": "nature.jpg",
            "out_of_stoke": False,
            "is_display": True,
        },
        {
            "title": "size",
            "value": "UK 5",
            "image_file": "",
            "image_dest": "",
            "out_of_stoke": False,
            "is_display": True,
        },
        {
            "title": "size",
            "value": "UK 6",
            "image_file": "",
            "image_dest": "",
            "out_of_stoke": False,
            "is_display": True,
        },
        {
            "title": "size",
            "value": "UK 7",
            "image_file": "",
            "image_dest": "",
            "out_of_stoke": False,
            "is_display": True,
        },
    ],
    "yoga-mat-premium": [
        {
            "title": "color",
            "value": "Purple",
            "image_file": "nature.jpg",
            "image_dest": "nature.jpg",
            "out_of_stoke": False,
            "is_display": True,
        },
        {
            "title": "color",
            "value": "Blue",
            "image_file": "nature.jpg",
            "image_dest": "nature.jpg",
            "out_of_stoke": False,
            "is_display": True,
        },
        {
            "title": "color",
            "value": "Black",
            "image_file": "nature.jpg",
            "image_dest": "nature.jpg",
            "out_of_stoke": False,
            "is_display": True,
        },
    ],
    "canon-eos-r6-mark-ii": [
        {
            "title": "color",
            "value": "Black",
            "image_file": "images.jpeg",
            "image_dest": "canon-eos-r6-mark-ii-black.jpeg",
            "out_of_stoke": False,
            "is_display": True,
        }
    ],
    "organic-green-tea-100g": [
        {
            "title": "variant",
            "value": "Classic",
            "image_file": "nature.jpg",
            "image_dest": "organic-green-tea-classic.jpeg",
            "out_of_stoke": False,
            "is_display": True,
        }
    ],
    "lego-classic-creative-bricks": [
        {
            "title": "color",
            "value": "Multicolor",
            "image_file": "images.jpeg",
            "image_dest": "lego-classic-creative-bricks-multicolor.jpeg",
            "out_of_stoke": False,
            "is_display": True,
        }
    ],
    "fresh-organic-apples-1kg": [
        {
            "title": "variant",
            "value": "1kg Bag",
            "image_file": "dairyegg.jpg",
            "image_dest": "fresh-organic-apples-1kg.jpg",
            "out_of_stoke": False,
            "is_display": True,
        }
    ],
    "classic-peanut-butter-500g": [
        {
            "title": "variant",
            "value": "500g Jar",
            "image_file": "snack.jpg",
            "image_dest": "classic-peanut-butter-500g.jpg",
            "out_of_stoke": False,
            "is_display": True,
        }
    ],
}

# seed_assets sub-directory that holds product attribute images.
SEED_SUBDIR = "products"


class Command(BaseCommand):
    help = "Seed default product attributes (colour, size, storage, etc.)."

    def handle(self, *args, **options):
        created_count = 0
        skipped_count = 0
        image_warnings = 0
        missing_products = []

        for slug, attributes in SEED_ATTRIBUTES.items():
            try:
                product = Product.objects.get(slug=slug, is_delete=False)
            except Product.DoesNotExist:
                self.stdout.write(
                    self.style.WARNING(
                        f"  [!] Product with slug '{slug}' not found — "
                        "skipping its attributes. Run 'seed_products' first."
                    )
                )
                missing_products.append(slug)
                continue

            for attr_data in attributes:
                # ------------------------------------------------------------
                # 1. Create the attribute row (without the image field).
                #    Use (product, title, value) as the natural unique key.
                # ------------------------------------------------------------
                with transaction.atomic():
                    attr, created = ProductAttribute.objects.get_or_create(
                        product=product,
                        title=attr_data["title"],
                        value=attr_data["value"],
                        defaults={
                            "out_of_stoke": attr_data.get("out_of_stoke", False),
                            "is_display": attr_data.get("is_display", True),
                            "is_delete": False,
                        },
                    )

                # ------------------------------------------------------------
                # 2. Upload the image through Django's storage backend only
                #    when an image_file is specified for this attribute.
                # ------------------------------------------------------------
                if attr_data.get("image_file"):
                    image_saved = save_seed_image(
                        instance=attr,
                        field_name="product_image",
                        seed_subdir=SEED_SUBDIR,
                        filename=attr_data["image_file"],
                        storage_upload_to=attr_data["image_dest"],
                        stdout=self.stdout,
                        style=self.style,
                    )
                    if not image_saved:
                        image_warnings += 1

                if created:
                    created_count += 1
                    self.stdout.write(
                        self.style.SUCCESS(
                            f"  [+] {product.name} — {attr.title}: {attr.value}"
                        )
                    )
                else:
                    skipped_count += 1
                    self.stdout.write(
                        f"  [=] Already exists — {product.name} — "
                        f"{attr.title}: {attr.value}"
                    )

        # --- Summary ---
        self.stdout.write("")
        self.stdout.write(
            self.style.SUCCESS(
                f"Product attributes seeded: {created_count} created, "
                f"{skipped_count} already existed."
            )
        )
        if missing_products:
            self.stdout.write(
                self.style.WARNING(
                    f"  Skipped {len(missing_products)} product(s) not found in DB: "
                    + ", ".join(missing_products)
                )
            )
        if image_warnings:
            self.stdout.write(
                self.style.WARNING(
                    f"  {image_warnings} attribute(s) are missing seed images. "
                    "Add the files to seed_assets/products/ and re-run."
                )
            )
