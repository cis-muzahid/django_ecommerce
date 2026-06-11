from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .api_views import (
    OrderViewSet, CheckoutView, PaymentView, RazorpayWebhookView, PayPalWebhookView, PayPalPaymentCompleteView, ReturnAndReplaceViewSet,
    OrderTrackingView
)

# Create router for ViewSets
router = DefaultRouter()
router.register(r'orders', OrderViewSet, basename='order')
router.register(r'returns-replacements', ReturnAndReplaceViewSet, basename='return-replace')

urlpatterns = [
    # Checkout and payment endpoints
    path('checkout/', CheckoutView.as_view(), name='checkout'),
    path('payment/', PaymentView.as_view(), name='payment'),
    path('razorpay/webhook/', RazorpayWebhookView.as_view(), name='razorpay-webhook'),
    path('paypal/webhook/', PayPalWebhookView.as_view(), name='paypal-webhook'),
    path('paypal/complete/', PayPalPaymentCompleteView.as_view(), name='paypal-complete'),
    path('order-tracking/', OrderTrackingView.as_view(), name='order-tracking'),
    
    # Include router URLs
    path('', include(router.urls)),
]
