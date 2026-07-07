# seed_assets/

This directory contains **default images committed to version control** that are
used exclusively by the Django management seed commands.

## Why this exists

Django `ImageField` / `FileField` values must be saved through Django's storage
backend (local filesystem, S3, GCP, Azure, etc.) using `FieldFile.save()`.
Simply writing a string path into the database field bypasses the storage layer
and breaks on any environment where `media/` is not pre-populated.

`seed_assets/` solves this by:

1. Committing a small set of representative images to git.
2. Having seed commands open those files and call `field.save(name, File(f))`
   so Django's storage backend handles the write correctly on every environment.

## Structure

```
seed_assets/
├── banner/          # Images for Banner model (home app)
├── blogs/           # Images for Blog model (blog app)
├── facility/        # Images for Facility model (home app)
└── products/        # Images for ProductAttribute model (products app)
```

## Rules

- **Do NOT** put user-uploaded or runtime-generated files here.
- **Do NOT** reference `media/` paths directly in seed commands.
- `media/` is git-ignored and managed entirely by Django's storage backend.
- Add new seed images here when adding new seed data that requires images.
