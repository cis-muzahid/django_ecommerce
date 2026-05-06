"""
_seed_image_utils.py
--------------------
Shared helper for saving seed images through Django's storage backend.

The ONLY correct way to attach a seed image to an ImageField is:

    instance.save()                          # get a PK first
    instance.<field>.save(name, File(f))     # let Django storage handle the write

Assigning a raw File / absolute path directly to the field triggers Django's
path-traversal protection ("Detected path traversal attempt") because the
File's .name attribute is an absolute filesystem path outside MEDIA_ROOT.

Usage
-----
    from home.management.commands._seed_image_utils import save_seed_image

    # 1. Save the instance without the image first.
    obj = MyModel(title="...", ...)
    obj.save()

    # 2. Upload the image through Django's storage backend.
    ok = save_seed_image(
        instance=obj,
        field_name="image",
        seed_subdir="banner",       # folder inside seed_assets/
        filename="ele.jpeg",        # file inside that folder
        storage_upload_to="ele.jpeg",
        stdout=self.stdout,
        style=self.style,
    )
"""

import os

from django.conf import settings
from django.core.files import File


# Absolute path to the committed seed images root.
SEED_ASSETS_ROOT = os.path.abspath(os.path.join(settings.BASE_DIR, "seed_assets"))


def seed_asset_path(seed_subdir: str, filename: str) -> str:
    """
    Return the safe absolute filesystem path for a seed asset.
    Raises ValueError on path-traversal attempts.
    """
    abs_path = os.path.abspath(os.path.join(SEED_ASSETS_ROOT, seed_subdir, filename))
    if not abs_path.startswith(SEED_ASSETS_ROOT + os.sep) and abs_path != SEED_ASSETS_ROOT:
        raise ValueError(f"Unsafe seed asset path detected: {abs_path}")
    return abs_path


def save_seed_image(
    instance,
    field_name: str,
    seed_subdir: str,
    filename: str,
    storage_upload_to: str,
    stdout=None,
    style=None,
    force: bool = False,
) -> bool:
    """
    Upload a seed image to an ImageField via Django's storage backend.

    The instance MUST already have a PK (i.e. .save() called at least once).
    Django's FieldFile.save(name, File(f)) is the only safe way to write to
    an ImageField — it routes through the configured storage backend
    (local filesystem, S3, GCP, Azure, etc.) without triggering path-traversal
    protection.

    Parameters
    ----------
    instance          : Saved Django model instance (must have a PK).
    field_name        : Name of the ImageField, e.g. "image".
    seed_subdir       : Sub-directory inside seed_assets/, e.g. "banner".
    filename          : Filename inside that sub-directory, e.g. "ele.jpeg".
    storage_upload_to : Destination name passed to FieldFile.save().
                        Django prepends the model's upload_to automatically.
                        Pass only the leaf filename, e.g. "ele.jpeg".
    stdout            : Management command stdout (optional).
    style             : Management command style (optional).
    force             : Re-upload even if the field already has a value.

    Returns
    -------
    True  — image uploaded successfully, or already existed (skipped).
    False — seed asset file not found on disk; warning printed.
    """
    field = getattr(instance, field_name)

    # Idempotent: skip if already populated and not forced.
    if field and field.name and not force:
        _log(stdout, f"  [~] Image already set for {instance} — skipping.")
        return True

    abs_path = seed_asset_path(seed_subdir, filename)

    if not os.path.isfile(abs_path):
        msg = (
            f"  [!] Seed asset not found: {abs_path}\n"
            f"      Add the file and re-run the seed command.\n"
            f"      '{instance}' will remain without an image."
        )
        if stdout and style:
            stdout.write(style.WARNING(msg))
        else:
            print(msg)
        return False

    # Open the file and let Django's storage backend handle the write.
    # FieldFile.save() accepts a plain filename (no path) as the first arg;
    # the model's upload_to is prepended automatically by the storage layer.
    with open(abs_path, "rb") as f:
        field.save(storage_upload_to, File(f), save=True)

    _log(stdout, f"  [~] Uploaded image for {instance}: {storage_upload_to}")
    return True


def _log(stdout, message: str, style=None, success: bool = False) -> None:
    if stdout is None:
        print(message)
        return
    if success and style:
        stdout.write(style.SUCCESS(message))
    else:
        stdout.write(message)
