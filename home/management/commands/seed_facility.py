from django.core.management.base import BaseCommand
from django.db import transaction

from home.models import Facility
from home.management.commands._seed_image_utils import save_seed_image


SEED_FACILITIES = [
    {
        "title": "Free Shipping",
        "image_file": "imggg.png",
        "image_dest": "imggg.png",
        "active": True,
    },
    {
        "title": "Secure Payment",
        "image_file": "imggg.png",
        "image_dest": "imggg.png",
        "active": True,
    },
    {
        "title": "Easy Returns",
        "image_file": "imggg.png",
        "image_dest": "imggg.png",
        "active": True,
    },
    {
        "title": "24/7 Customer Support",
        "image_file": "imggg.png",
        "image_dest": "imggg.png",
        "active": True,
    },
    {
        "title": "Quality Guarantee",
        "image_file": "imggg.png",
        "image_dest": "imggg.png",
        "active": True,
    },
]

SEED_SUBDIR = "facility"


class Command(BaseCommand):
    help = "Seed default facility entries (trust badges shown on the homepage)."

    def handle(self, *args, **options):
        created_count  = 0
        existing_count = 0
        image_warnings = 0

        for data in SEED_FACILITIES:
            existing = Facility.objects.filter(title=data["title"]).first()

            if existing:
                # ── UPDATE ────────────────────────────────────────────────
                with transaction.atomic():
                    existing.active = data["active"]
                    existing.save(update_fields=["active"])

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

                existing_count += 1
                self.stdout.write(f"  [=] Facility already exists: {existing.title}")

            else:
                # ── CREATE ────────────────────────────────────────────────
                # Step 1: insert the row with an empty image placeholder.
                with transaction.atomic():
                    facility = Facility.objects.create(
                        title=data["title"],
                        image="",  # placeholder — filled in step 2
                        active=data["active"],
                    )

                # Step 2: upload through Django's storage backend.
                ok = save_seed_image(
                    instance=facility,
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
                    self.style.SUCCESS(f"  [+] Created facility: {data['title']}")
                )

        # ── Summary ───────────────────────────────────────────────────────
        self.stdout.write("")
        self.stdout.write(
            self.style.SUCCESS(
                f"Facilities seeded: {created_count} created, "
                f"{existing_count} already existed."
            )
        )
        if image_warnings:
            self.stdout.write(
                self.style.WARNING(
                    f"  {image_warnings} facility item(s) had missing seed images. "
                    "Add the files to seed_assets/facility/ and re-run."
                )
            )
