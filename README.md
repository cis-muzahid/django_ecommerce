# Django E-commerce Web Application

## Overview

A full-stack e-commerce platform built with Django and React. The backend is a Django monorepo under `backend/`, while the storefront is a React + Vite app in `frontend/`.

---

## Features

- **React storefront** — fast, SPA-style customer experience
- **Django admin** — manage products, orders, users, banners, blogs, and settings
- **Role-based access** — admin, supplier, customer, and regular user roles
- **Product variants** — colour, size, storage options with separate images
- **Blog** — categories, posts, and comments
- **Banners and facility badges** — homepage marketing sections and trust icons
- **Cart & wishlist** — per-user cart and wishlist handling
- **Orders** — order creation, tracking, and return/replace flows
- **Payment integration** — Stripe, PayPal, and Razorpay-ready
- **Docker-friendly** — preconfigured `docker-compose.yml`

---

## Tech Stack

| Layer | Technology |
|---|---|
| Backend | Django |
| API | Django REST Framework |
| Frontend | React, Vite |
| Styling | CSS, React UI components |
| Database | SQLite (local) / PostgreSQL (production) |
| Payments | Stripe, PayPal, Razorpay |
| Containerisation | Docker, Docker Compose |

---

## Repository Structure

```
django_ecommerce/
├── backend/                 # Django backend app
│   ├── ecom/                # Django project settings, URLs, ASGI/WGSI
│   ├── users/               # User, roles, permissions, user profiles
│   ├── products/            # Product, category, product attribute models
│   ├── cart/                # Cart and wishlist logic
│   ├── orders/              # Order models, payment helpers, tracking
│   ├── home/                # Banner, facility, homepage seed commands
│   ├── blog/                # Blog and blog category models
│   ├── category/            # Category APIs and serializers
│   ├── seed_assets/         # Committed source images used by seed commands
│   ├── static/              # Backend static files
│   ├── templates/           # Django templates and admin pages
│   ├── manage.py
│   └── requirements.txt
├── frontend/                # React + Vite frontend
│   ├── public/
│   ├── src/
│   ├── package.json
│   ├── package-lock.json
│   └── vite.config.js
├── docker-compose.yml
├── README.md
└── .gitignore
```

---

## Local Development Setup

### Backend setup

1. Change into the project root:

```bash
cd django_ecommerce
```

2. Create and activate a Python virtual environment:

```bash
python -m venv venv
source venv/bin/activate
```

3. Install backend dependencies:

```bash
pip install -r backend/requirements.txt
```

4. Create a `.env` file in `django_ecommerce/` and add required environment variables.

If you have an example env file, copy it first. Otherwise create `.env` manually.

Minimum variables:

```env
DJANGO_KEY=your-secret-key-here
DEFAULT_USER_PASSWORD=Admin@123
```

5. Run database migrations from the backend directory:

```bash
cd backend
python manage.py migrate
```

6. Seed initial data:

```bash
python manage.py seed_project
```

7. Start the backend server:

```bash
python manage.py runserver
```

Backend URLs:

- Storefront API: http://localhost:8000/
- Admin panel: http://localhost:8000/admin/

---

### Frontend setup

1. Install frontend dependencies:

```bash
cd ../frontend
npm install
```

2. Start the Vite development server:

```bash
npm run dev
```

3. Open the frontend in your browser at:

```text
http://localhost:5173/
```

If the frontend calls the backend API, verify `VITE_API_BASE_URL` in `frontend/src/services/apiClient.js` or set it in a `.env` file inside `frontend/`.

---

## Docker Setup

The Docker Compose file builds the backend from `backend/` and exposes port `8000`.

Run:

```bash
docker-compose up --build
```

Then migrate and seed inside the container:

```bash
docker-compose exec backend python manage.py migrate
docker-compose exec backend python manage.py seed_project
```

If your service name differs, replace `backend` with the actual Docker service name.

---

## Seed Commands

Available seed commands for the Django backend:

```bash
cd backend
python manage.py seed_project
python manage.py seed_categories
python manage.py seed_products
python manage.py seed_product_attributes
python manage.py seed_banners
python manage.py seed_blogs
python manage.py seed_facility
```

These commands are intended to be idempotent and safe to run multiple times.

---

## Default Users

The seeded users are typically created by `seed_project`.

| Role | Email | Notes |
|------|-------|-------|
| Admin | `admin@example.com` | `is_staff=True`, `is_superuser=True` |
| Supplier | `supplier@example.com` | |
| Customer | `customer@example.com` | |
| User | `user@example.com` | |

The seeded password comes from the `--password` flag or the `DEFAULT_USER_PASSWORD` environment variable.

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

## Notes

- Backend code lives under `backend/`.
- Frontend code lives under `frontend/`.
- `seed_assets/` contains committed seed images used by backend seed commands.
- `media/` is runtime upload storage and should remain gitignored.

---

## Contributing

Pull requests are welcome. For major changes, open an issue first to discuss your proposed work.

---

## License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.
