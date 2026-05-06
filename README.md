# Django E-commerce Web Application

## Overview

A full-featured e-commerce platform built with Django. It covers product management, order processing, delivery tracking, payment gateway integration (Stripe & PayPal), a blog, and a role-based admin dashboard.

---

## Features

- **User-Friendly Storefront** — intuitive shopping experience for customers
- **Admin Dashboard** — manage products, orders, users, banners, and blogs
- **Role-Based Access Control** — admin, supplier, customer, and user roles with granular permissions
- **Product Attributes** — colour, size, storage variants per product with individual images
- **Blog** — categorised blog posts with comments
- **Banners** — header, middle, and lower homepage banners
- **Facility Badges** — trust icons (free shipping, secure payment, etc.)
- **Cart & Wishlist** — per-user cart and wishlist management
- **Orders** — full order lifecycle with return/replace support
- **Payment Gateways** — Stripe and PayPal integration
- **Docker Ready** — `Dockerfile` and `docker-compose.yml` included

---

## Tech Stack

| Layer | Technology |
|---|---|
| Backend | Django 5 |
| Frontend | HTML, CSS, JavaScript, Bootstrap |
| Database | SQLite (local) / PostgreSQL (production) |
| Payments | Stripe, PayPal |
| Storage | Local filesystem (dev) / S3 or GCP (production) |
| Containerisation | Docker, Docker Compose |

---

## Project Structure (key parts)

```
django_ecommerce/
├── ecom/                  # Django project settings & root URLs
├── users/                 # CustomUser, Role, Permission, UserAddress
├── products/              # Category, Product, ProductAttribute, ProductSpecification
├── home/                  # Banner, Facility
├── blog/                  # Blog, BlogCategory, Comment
├── cart/                  # Cart, Wishlist
├── orders/                # Order, OrderItem, ReturnAndReplaceOrder
├── seed_assets/           # ✅ Committed seed images (used by seed commands)
│   ├── banner/
│   ├── blogs/
│   ├── facility/
│   └── products/
├── media/                 # ⛔ Git-ignored — runtime uploads only
├── static/                # Static files (CSS, JS, images)
└── manage.py
```

---

## Local Development Setup

### 1. Clone the repository

```bash
git clone https://github.com/cis-muzahid/django_ecommerce.git
cd django_ecommerce
```

### 2. Create and activate a virtual environment

```bash
python -m venv venv
source venv/bin/activate        # Linux / macOS
venv\Scripts\activate           # Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Copy the example env file and fill in your values:

```bash
cp .env.example .env
```

Minimum required variables:

```env
DJANGO_KEY=your-secret-key-here
DEFAULT_USER_PASSWORD=Admin@123
```

### 5. Run database migrations

```bash
python manage.py migrate
```

### 6. Seed the database (one command does everything)

```bash
python manage.py seed_project
```

This single command runs the full seed pipeline in the correct dependency order:

| Step | Command | What it creates |
|------|---------|-----------------|
| 1 | `create_default_users` | Roles, auth groups, and 4 default users |
| 2 | `seed_categories` | 8 top-level categories + 32 sub-categories |
| 3 | `seed_products` | 10 default products |
| 4 | `seed_product_attributes` | Colour / size / storage variants with images |
| 5 | `seed_banners` | 6 homepage banners (header, middle, lower) |
| 6 | `seed_blogs` | 6 blog categories + 8 blog posts |
| 7 | `seed_facility` | 5 facility / trust-badge entries |

**Images are handled automatically.** Seed commands open files from `seed_assets/`
and save them through Django's storage backend (`FieldFile.save()`), so they work
correctly on local filesystem, S3, GCP, or any other configured storage — no manual
file copying required.

To set a specific password for the default users:

```bash
python manage.py seed_project --password "YourStrongPassword123!"
```

Or set it via environment variable before running:

```bash
DEFAULT_USER_PASSWORD=YourStrongPassword123! python manage.py seed_project
```

The entire pipeline is **idempotent** — safe to run multiple times without
creating duplicates.

### 7. Start the development server

```bash
python manage.py runserver
```

- Storefront: [http://localhost:8000/](http://localhost:8000/)
- Admin panel: [http://localhost:8000/admin/](http://localhost:8000/admin/)

---

## Default Users

Created automatically by `seed_project` (or `create_default_users`):

| Role | Email | Notes |
|------|-------|-------|
| Admin | `admin@example.com` | `is_staff=True`, `is_superuser=True` |
| Supplier | `supplier@example.com` | |
| Customer | `customer@example.com` | |
| User | `user@example.com` | |

Password is taken from `--password` flag → `DEFAULT_USER_PASSWORD` env var →
auto-generated secure password (printed once to stdout).

---

## Docker Setup

```bash
docker-compose up --build
```

Then in a separate terminal (or add to your entrypoint):

```bash
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py seed_project
```

---

## Running Individual Seed Commands

Each seed command can be run independently:

```bash
python manage.py seed_categories
python manage.py seed_products
python manage.py seed_product_attributes
python manage.py seed_banners
python manage.py seed_blogs
python manage.py seed_facility
```

All commands are idempotent and use `get_or_create` / `update_or_create`
internally, so re-running them is always safe.

---

## How Seed Images Work

```
seed_assets/          ← committed to git, travels with the code
    banner/           ← source images for Banner model
    blogs/            ← source images for Blog model
    facility/         ← source images for Facility model
    products/         ← source images for ProductAttribute model

media/                ← git-ignored, managed by Django storage backend
```

When a seed command runs, it:

1. Opens the source file from `seed_assets/<subdir>/<filename>`
2. Calls `instance.image.save(dest_name, File(f), save=True)`
3. Django's storage backend writes the file to `media/` (local) or uploads
   it to S3/GCP (production)

This means images work correctly on **every environment** without any manual
file copying.

To add a new seed image:

1. Place the file in the appropriate `seed_assets/` sub-directory
2. Reference it in the relevant seed command using `image_file` / `image_dest`
3. Commit both the image and the updated seed command

---

## Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `DJANGO_KEY` | ✅ | Django secret key |
| `DEFAULT_USER_PASSWORD` | optional | Password for seeded default users |
| `STRIPE_PUBLISHABLE_KEY` | optional | Stripe public key |
| `STRIPE_SECRET_KEY` | optional | Stripe secret key |
| `PAYPAL_CLIENT_ID` | optional | PayPal client ID |
| `PAYPAL_SECRET` | optional | PayPal secret |
| `BACKEND_DOMAIN` | optional | Backend domain for payment callbacks |
| `PAYMENT_SUCCESS_URL` | optional | Redirect URL after successful payment |
| `PAYMENT_CANCEL_URL` | optional | Redirect URL after cancelled payment |
| `TRACKING_SECRET` | optional | Delivery tracking key |

---

## Contributing

Pull requests are welcome. For major changes, open an issue first to discuss
what you would like to change.

---

## License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.
