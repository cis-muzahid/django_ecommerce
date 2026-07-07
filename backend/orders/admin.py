from django.contrib import admin

from .models import Order, OrderItem, ReturnAndReplaceOrder, PaymentEvent


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'status', 'payment_method', 'payment_status', 'total_amount', 'created_at')
    list_filter = ('status', 'payment_method', 'payment_status', 'created_at')
    search_fields = ('user__email', 'payment_id', 'address')
    readonly_fields = ('created_at', 'updated_at')


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'order', 'cart', 'active')
    list_filter = ('active',)
    search_fields = ('order__id', 'cart__product__name')


@admin.register(ReturnAndReplaceOrder)
class ReturnAndReplaceOrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'order', 'action', 'requested', 'approved', 'active', 'created_at')
    list_filter = ('action', 'requested', 'approved', 'active', 'created_at')
    search_fields = ('user__email', 'order__id', 'reason')


@admin.register(PaymentEvent)
class PaymentEventAdmin(admin.ModelAdmin):
    list_display = ('id', 'event_type', 'order', 'payment_intent_id', 'payment_status', 'amount', 'currency', 'created_at')
    list_filter = ('event_type', 'payment_status', 'currency', 'created_at')
    search_fields = ('razorpay_payment_id', 'payment_intent_id', 'order__id')
    readonly_fields = ('created_at', 'payload')
