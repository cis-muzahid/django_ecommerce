from .base import *
from dotenv import load_dotenv
import os

# Load environment variables from the .env_development file
load_dotenv(os.path.join(BASE_DIR, '../.env_development'))

# Set the SECRET_KEY from the environment variable
SECRET_KEY = os.environ.get("DJANGO_KEY")

# Development settings
DEBUG = True

ALLOWED_HOSTS = ['127.0.0.1', 'localhost', '0896-103-47-44-135.ngrok-free.app']

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "ecom2",
        "USER": "postgres",
        "PASSWORD": "postgres",
        "HOST": "127.0.0.1",
        "PORT": "5432",
    }
}

# Stripe
STRIPE_PUBLISHABLE_KEY = os.environ.get('STRIPE_PUBLISHABLE_KEY')
STRIPE_SECRET_KEY = os.environ.get('STRIPE_SECRET_KEY')
BACKEND_DOMAIN = os.environ.get("BACKEND_DOMAIN")
PAYMENT_SUCCESS_URL = os.environ.get("PAYMENT_SUCCESS_URL")
PAYMENT_CANCEL_URL = os.environ.get("PAYMENT_CANCEL_URL")
PAYPAL_CLIENT_ID = os.environ.get('PAYPAL_CLIENT_ID')
PAYPAL_SECRET = os.environ.get('PAYPAL_SECRET')
TRACKING_KEY = os.environ.get("TRACKING_SECRET")
STRIPE_WEBHOOK_KEY = os.environ.get("STRIPE_WEBHOOK_KEY")
PAYPAL_MODE = 'production'