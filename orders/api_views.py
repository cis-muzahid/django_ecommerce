from rest_framework import status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from django.shortcuts import get_object_or_404
from django.db.models import Sum, Count, Q
from datetime import datetime, timedelta
from django.utils import timezone
from decimal import Decimal
import razorpay
import paypalrestsdk
import hmac
import hashlib
import json
from django.conf import settings

from .models import Order, OrderItem, ReturnAndReplaceOrder, PaymentEvent
from cart.models import Cart
from users.models import UserAddress
from .serializers import (
    OrderSerializer, OrderCreateSerializer, OrderItemSerializer,
    ReturnAndReplaceOrderSerializer, ReturnAndReplaceCreateSerializer,
    OrderStatusUpdateSerializer, PaymentIntentSerializer,
    OrderTrackingSerializer, OrderSummarySerializer
)
from .utilities import (
    order_cart_item, check_default_address, fetch_user_address,
    finalize_order_carts, cancel_unpaid_order, PAID_PAYMENT_STATUSES,
)
from .paypal_service import (
    PayPalAPIError,
    paypal_configured as paypal_service_configured,
    paypal_currency as paypal_service_currency,
    create_checkout_order_from_store_amount,
    capture_checkout_order,
    get_checkout_order,
)

# Initialize Razorpay client
if settings.RAZORPAY_KEY_ID and settings.RAZORPAY_KEY_SECRET:
    razorpay_client = razorpay.Client(
        auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET)
    )
else:
    razorpay_client = None

# Initialize legacy PayPal SDK (webhook signature verification only)
paypal_configured = paypal_service_configured()
if paypal_configured:
    paypalrestsdk.configure({
        'mode': getattr(settings, 'PAYPAL_MODE', 'sandbox'),
        'client_id': settings.PAYPAL_CLIENT_ID,
        'client_secret': settings.PAYPAL_CLIENT_SECRET,
    })


def _paypal_redirect_urls():
    return {
        'return_url': settings.PAYMENT_SUCCESS_URL,
        'cancel_url': settings.PAYMENT_CANCEL_URL,
    }


def _paypal_currency():
    return paypal_service_currency()


def _mark_paypal_order_paid(order, paypal_order_id, payload, event_type='payment_captured'):
    order.payment_id = paypal_order_id
    order.payment_status = 'succeeded'
    if order.status == 'initial':
        order.status = 'in_process'
    order.save(update_fields=['payment_id', 'payment_status', 'status', 'updated_at'])
    finalize_order_carts(order)
    _record_payment_event(
        order=order,
        event_id=paypal_order_id,
        event_type=event_type,
        payment_intent_id=paypal_order_id,
        payment_status='succeeded',
        currency=_paypal_currency(),
        payment_gateway='paypal',
        payload=payload,
    )


def _paypal_webhook_headers(request):
    return {
        'PAYPAL-TRANSMISSION-ID': request.META.get('HTTP_PAYPAL_TRANSMISSION_ID', ''),
        'PAYPAL-TRANSMISSION-TIME': request.META.get('HTTP_PAYPAL_TRANSMISSION_TIME', ''),
        'PAYPAL-TRANSMISSION-SIG': request.META.get('HTTP_PAYPAL_TRANSMISSION_SIG', ''),
        'PAYPAL-CERT-URL': request.META.get('HTTP_PAYPAL_CERT_URL', ''),
        'PAYPAL-AUTH-ALGO': request.META.get('HTTP_PAYPAL_AUTH_ALGO', ''),
    }


def _parse_paypal_webhook_event(request):
    body = request.body.decode('utf-8') if isinstance(request.body, bytes) else request.body
    webhook_id = getattr(settings, 'PAYPAL_WEBHOOK_ID', None)

    if webhook_id:
        headers = _paypal_webhook_headers(request)
        verified = paypalrestsdk.WebhookEvent.verify(body, headers, webhook_id)
        if not verified:
            return None
        return json.loads(body) if isinstance(body, str) else verified

    return json.loads(body)


def _paypal_event_already_processed(event_id):
    if not event_id:
        return False
    return PaymentEvent.objects.filter(
        event_type__startswith='PAYMENT.',
        payload__id=event_id,
        payment_gateway='paypal',
    ).exists()


def _find_paypal_order(payment_id, custom_order_id=None):
    order = None
    if custom_order_id:
        try:
            order = Order.objects.get(id=custom_order_id)
        except (Order.DoesNotExist, ValueError, TypeError):
            order = None
    if order is None and payment_id:
        order = Order.objects.filter(payment_id=payment_id).first()
    return order


def _record_payment_event(*, order=None, event_id, event_type, payload, payment_intent_id='', payment_status='', amount=None, currency='INR', payment_gateway='razorpay', razorpay_payment_id='', paypal_transaction_id=''):
    try:
        return PaymentEvent.objects.create(
            order=order,
            stripe_event_id=event_id if payment_gateway == 'stripe' else None,
            razorpay_payment_id=razorpay_payment_id or event_id if payment_gateway == 'razorpay' else None,
            event_type=event_type,
            payment_intent_id=payment_intent_id or '',
            payment_status=payment_status or '',
            amount=amount,
            currency=currency or 'INR',
            payment_gateway=payment_gateway,
            payload=payload or {},
        )
    except Exception:
        return None


def _find_order_from_payment_payload(payment_object):
    """Helper function to find order from payment payload - kept for backward compatibility"""
    metadata = payment_object.get('metadata') or {}
    order_id = metadata.get('order_id')
    order = None
    if order_id:
        try:
            order = Order.objects.select_related('user').get(id=order_id)
        except Order.DoesNotExist:
            order = None
    if order is None:
        payment_intent_id = payment_object.get('id') or ''
        order = Order.objects.select_related('user').filter(payment_id=payment_intent_id).first()
    return order


class OrderViewSet(ModelViewSet):
    """ViewSet for Order management"""
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['status', 'payment_method', 'payment_status']
    ordering_fields = ['created_at', 'total_amount']
    ordering = ['-created_at']
    
    def get_queryset(self):
        """Users can only access their own orders"""
        user = self.request.user
        if self.action == 'cancel':
            queryset = Order.objects.filter(user=user)
        else:
            queryset = Order.objects.filter(user=user, active=True)
        
        # Admin and suppliers can see all orders
        if hasattr(user, 'user_role') and user.user_role:
            if user.user_role.name in ['admin'] or user.is_superuser:
                queryset = Order.objects.all()
            elif user.user_role.name == 'supplier':
                # Suppliers can see orders for their products
                queryset = Order.objects.filter(
                    orderitem__cart__product__user=user
                ).distinct()
        
        return queryset
    
    def get_serializer_class(self):
        if self.action == 'create':
            return OrderCreateSerializer
        return OrderSerializer
    
    def create(self, request, *args, **kwargs):
        """Create a new order"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        try:
            order = serializer.save()
            order_serializer = OrderSerializer(order, context={'request': request})
            
            return Response({
                'message': 'Order created successfully',
                'order': order_serializer.data
            }, status=status.HTTP_201_CREATED)
            
        except Exception as e:
            return Response({
                'error': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        """Cancel an order"""
        order = self.get_object()
        
        if order.user != request.user:
            return Response(
                {'error': 'You can only cancel your own orders'}, 
                status=status.HTTP_403_FORBIDDEN
            )
        
        if order.status in ['deliverd', 'cancelled']:
            return Response(
                {'error': 'Cannot cancel this order'}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        if order.payment_status not in PAID_PAYMENT_STATUSES:
            cancel_unpaid_order(order)
            return Response({
                'message': 'Order cancelled successfully'
            }, status=status.HTTP_200_OK)
        
        # Cancel order items
        OrderItem.objects.filter(order=order).update(active=False)
        order.status = 'cancelled'
        order.save()
        
        # Process refund if payment was made
        if order.payment_id and order.payment_status in ['succeeded', 'processing', 'authorized']:
            try:
                if order.payment_method == 'razorpay' and razorpay_client:
                    refund = razorpay_client.payment.refund(
                        order.payment_id,
                        {'amount': int(order.total_amount * 100)}
                    )
                    order.payment_status = 'refunded'
                    order.save(update_fields=['payment_status', 'updated_at'])
                    _record_payment_event(
                        order=order,
                        event_id=refund['id'],
                        event_type='manual_refund',
                        payment_intent_id=order.payment_id,
                        payment_status='refunded',
                        amount=order.total_amount,
                        payment_gateway='razorpay',
                        razorpay_payment_id=refund['id'],
                        payload={'refund_id': refund['id'], 'status': refund.get('status'), 'source': 'order_cancel'},
                    )
                    return Response({
                        'message': 'Order cancelled and refund processed successfully'
                    }, status=status.HTTP_200_OK)
            except Exception as e:
                return Response({
                    'message': 'Order cancelled but refund failed',
                    'error': str(e)
                }, status=status.HTTP_200_OK)
        
        return Response({
            'message': 'Order cancelled successfully'
        }, status=status.HTTP_200_OK)
    
    @action(detail=True, methods=['post'])
    def update_status(self, request, pk=None):
        """Update order status (Admin/Supplier only)"""
        order = self.get_object()
        
        # Check permissions
        if not (hasattr(request.user, 'user_role') and request.user.user_role):
            return Response(
                {'error': 'Permission denied'}, 
                status=status.HTTP_403_FORBIDDEN
            )
        
        if request.user.user_role.name not in ['admin', 'supplier'] and not request.user.is_superuser:
            return Response(
                {'error': 'Permission denied'}, 
                status=status.HTTP_403_FORBIDDEN
            )
        
        serializer = OrderStatusUpdateSerializer(data=request.data)
        if serializer.is_valid():
            order.status = serializer.validated_data['status']
            order.save()
            
            return Response({
                'message': 'Order status updated successfully',
                'order': OrderSerializer(order, context={'request': request}).data
            })
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['get'])
    def summary(self, request):
        """Get order summary for the user"""
        user = request.user
        orders = Order.objects.filter(user=user)
        
        summary_data = {
            'total_orders': orders.count(),
            'pending_orders': orders.filter(status='initial').count(),
            'delivered_orders': orders.filter(status='deliverd').count(),
            'cancelled_orders': orders.filter(status='cancelled').count(),
            'total_amount_spent': orders.aggregate(
                total=Sum('total_amount')
            )['total'] or 0
        }
        
        serializer = OrderSummarySerializer(summary_data)
        return Response(serializer.data)


class CheckoutView(APIView):
    """API view for checkout process"""
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        """Get checkout information"""
        user = request.user
        
        # Get cart items
        cart_items = Cart.objects.filter(user=user, active=True)
        if not cart_items.exists():
            return Response({
                'error': 'Cart is empty'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Calculate totals
        total_amount = sum(
            item.product.price * item.quantity for item in cart_items
        )
        
        # Get addresses
        addresses = fetch_user_address(user)
        default_address = check_default_address(user)
        
        from cart.serializers import CartSerializer
        return Response({
            'cart_items': CartSerializer(cart_items, many=True, context={'request': request}).data,
            'total_amount': float(total_amount),
            'addresses': [
                {
                    'id': addr.id,
                    'street': addr.street,
                    'city': addr.city,
                    'state': addr.state,
                    'postal_code': addr.postal_code,
                    'country': addr.country,
                    'is_default': addr.is_default
                } for addr in addresses
            ] if addresses else [],
            'default_address': {
                'id': default_address.id,
                'street': default_address.street,
                'city': default_address.city,
                'state': default_address.state,
                'postal_code': default_address.postal_code,
                'country': default_address.country,
            } if default_address else None
        })
    
    def post(self, request):
        """Process checkout and create order"""
        serializer = OrderCreateSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            try:
                order = serializer.save()
                order_serializer = OrderSerializer(order, context={'request': request})
                
                return Response({
                    'message': 'Order created successfully',
                    'order': order_serializer.data
                }, status=status.HTTP_201_CREATED)
                
            except Exception as e:
                return Response({
                    'error': str(e)
                }, status=status.HTTP_400_BAD_REQUEST)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PaymentView(APIView):
    """API view for payment processing using Razorpay or PayPal"""
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request):
        """Create payment order (Razorpay or PayPal)"""
        serializer = PaymentIntentSerializer(data=request.data)
        if serializer.is_valid():
            user = request.user
            payment_method = serializer.validated_data['payment_method']
            order_id = serializer.validated_data.get('order_id')

            # Support both razorpay and paypal
            if payment_method not in ['razorpay', 'paypal']:
                return Response({
                    'error': 'Unsupported payment method'
                }, status=status.HTTP_400_BAD_REQUEST)

            if order_id:
                order = get_object_or_404(Order, id=order_id, user=user)
                total_amount = order.total_amount
            else:
                # Get cart items and calculate total before an order has been created.
                cart_items = Cart.objects.filter(user=user, active=True)
                if not cart_items.exists():
                    return Response({
                        'error': 'Cart is empty'
                    }, status=status.HTTP_400_BAD_REQUEST)

                total_amount = sum(
                    item.product.price * item.quantity for item in cart_items
                )
                order = None

            try:
                if payment_method == 'razorpay':
                    if not razorpay_client:
                        return Response({
                            'error': 'Razorpay is not configured'
                        }, status=status.HTTP_503_SERVICE_UNAVAILABLE)
                    
                    # Create Razorpay order
                    razorpay_order = razorpay_client.order.create(
                        {
                            'amount': int(total_amount * 100),  # Amount in paise
                            'currency': 'INR',
                            'receipt': f'order_{order_id or "cart"}_{user.id}',
                            'notes': {
                                'user_id': str(user.id),
                                'user_email': user.email,
                                'order_id': str(order_id or ''),
                            }
                        }
                    )

                    if order:
                        order.payment_id = razorpay_order['id']
                        order.payment_method = 'razorpay'
                        order.payment_status = 'pending'
                        if order.status == 'initial':
                            order.status = 'in_process'
                        order.save(update_fields=['payment_id', 'payment_method', 'payment_status', 'status', 'updated_at'])
                        _record_payment_event(
                            order=order,
                            event_id=razorpay_order['id'],
                            event_type='order_created',
                            payment_intent_id=razorpay_order['id'],
                            payment_status='pending',
                            amount=total_amount,
                            payment_gateway='razorpay',
                            razorpay_payment_id=razorpay_order['id'],
                            payload=razorpay_order,
                        )

                    return Response({
                        'razorpay_order_id': razorpay_order['id'],
                        'amount': float(total_amount),
                        'currency': 'INR',
                        'payment_status': 'pending',
                        'key_id': settings.RAZORPAY_KEY_ID,
                        'order_id': order.id if order else order_id,
                    })
                
                elif payment_method == 'paypal':
                    if not paypal_configured:
                        return Response({
                            'error': 'PayPal is not configured'
                        }, status=status.HTTP_503_SERVICE_UNAVAILABLE)

                    redirect_urls = _paypal_redirect_urls()
                    checkout_order = create_checkout_order_from_store_amount(
                        store_amount=total_amount,
                        custom_id=order.id if order else order_id,
                        return_url=redirect_urls['return_url'],
                        cancel_url=redirect_urls['cancel_url'],
                        description=f'Order #{order_id or "pending"} - {user.email}',
                    )
                    currency_code = checkout_order.get('currency') or _paypal_currency()
                    conversion = checkout_order.get('conversion', {})

                    if order:
                        order.payment_id = checkout_order['id']
                        order.payment_method = 'paypal'
                        order.payment_status = 'pending'
                        if order.status == 'initial':
                            order.status = 'in_process'
                        order.save(update_fields=['payment_id', 'payment_method', 'payment_status', 'status', 'updated_at'])
                        _record_payment_event(
                            order=order,
                            event_id=checkout_order['id'],
                            event_type='order_created',
                            payment_intent_id=checkout_order['id'],
                            payment_status='pending',
                            amount=total_amount,
                            currency=currency_code,
                            payment_gateway='paypal',
                            payload={**checkout_order['raw'], 'conversion': conversion},
                        )

                    return Response({
                        'payment_id': checkout_order['id'],
                        'paypal_order_id': checkout_order['id'],
                        'approval_url': checkout_order['approval_url'],
                        'amount': float(total_amount),
                        'currency': currency_code,
                        'store_amount': conversion.get('store_amount', float(total_amount)),
                        'store_currency': conversion.get('store_currency', 'INR'),
                        'paypal_amount': conversion.get('paypal_amount'),
                        'payment_status': 'pending',
                        'order_id': order.id if order else order_id,
                    })

            except PayPalAPIError as e:
                return Response({
                    'error': str(e)
                }, status=status.HTTP_400_BAD_REQUEST)
            except Exception as e:
                return Response({
                    'error': str(e)
                }, status=status.HTTP_400_BAD_REQUEST)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RazorpayWebhookView(APIView):
    """Razorpay webhook endpoint for asynchronous payment status updates"""
    authentication_classes = []
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        """Handle Razorpay webhook events"""
        if not settings.RAZORPAY_KEY_SECRET:
            return Response(
                {'error': 'Razorpay webhook secret is not configured'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        try:
            payload = json.loads(request.body)
            signature = request.META.get('HTTP_X_RAZORPAY_SIGNATURE')
            
            if not signature:
                return Response({'error': 'Invalid signature'}, status=status.HTTP_400_BAD_REQUEST)

            # Verify webhook signature
            body = request.body.decode('utf-8') if isinstance(request.body, bytes) else request.body
            expected_signature = hmac.new(
                settings.RAZORPAY_KEY_SECRET.encode(),
                body.encode(),
                hashlib.sha256
            ).hexdigest()

            if signature != expected_signature:
                return Response({'error': 'Invalid signature'}, status=status.HTTP_400_BAD_REQUEST)

        except (ValueError, KeyError):
            return Response({'error': 'Invalid payload'}, status=status.HTTP_400_BAD_REQUEST)

        event_type = payload.get('event')
        data = payload.get('payload', {})
        
        # Handle payment authorization events
        if event_type == 'payment.authorized':
            payment_data = data.get('payment', {})
            payment_id = payment_data.get('entity', {}).get('id', '')
            order_id = payment_data.get('entity', {}).get('notes', {}).get('order_id', '')
            
            order = None
            if order_id:
                try:
                    order = Order.objects.get(id=order_id)
                except Order.DoesNotExist:
                    pass
            
            if not order and payment_id:
                order = Order.objects.filter(payment_id=payment_id).first()
            
            if order:
                order.payment_id = payment_id or order.payment_id
                order.payment_status = 'authorized'
                if order.status == 'initial':
                    order.status = 'in_process'
                order.save(update_fields=['payment_id', 'payment_status', 'status', 'updated_at'])
                finalize_order_carts(order)
                
                _record_payment_event(
                    order=order,
                    event_id=payload.get('id', ''),
                    event_type=event_type,
                    payment_intent_id=payment_id,
                    payment_status='authorized',
                    amount=Decimal(str(payment_data.get('entity', {}).get('amount', 0))) / 100,
                    payment_gateway='razorpay',
                    razorpay_payment_id=payment_id,
                    payload=payload,
                )
        
        elif event_type == 'payment.failed':
            payment_data = data.get('payment', {})
            payment_id = payment_data.get('entity', {}).get('id', '')
            order_id = payment_data.get('entity', {}).get('notes', {}).get('order_id', '')
            
            order = None
            if order_id:
                try:
                    order = Order.objects.get(id=order_id)
                except Order.DoesNotExist:
                    pass
            
            if not order and payment_id:
                order = Order.objects.filter(payment_id=payment_id).first()
            
            if order:
                order.payment_id = payment_id or order.payment_id
                order.save(update_fields=['payment_id', 'updated_at'])
                cancel_unpaid_order(order)
                
                _record_payment_event(
                    order=order,
                    event_id=payload.get('id', ''),
                    event_type=event_type,
                    payment_intent_id=payment_id,
                    payment_status='failed',
                    amount=Decimal(str(payment_data.get('entity', {}).get('amount', 0))) / 100,
                    payment_gateway='razorpay',
                    razorpay_payment_id=payment_id,
                    payload=payload,
                )
        
        elif event_type == 'refund.created':
            refund_data = data.get('refund', {})
            payment_id = refund_data.get('entity', {}).get('payment_id', '')
            
            order = None
            if payment_id:
                order = Order.objects.filter(payment_id=payment_id).first()
            
            if order:
                refund_amount = Decimal(str(refund_data.get('entity', {}).get('amount', 0))) / 100
                order.payment_status = 'refunded'
                if refund_amount < order.total_amount:
                    order.payment_status = 'partially_refunded'
                order.save(update_fields=['payment_status', 'updated_at'])
                
                _record_payment_event(
                    order=order,
                    event_id=refund_data.get('entity', {}).get('id', ''),
                    event_type=event_type,
                    payment_intent_id=payment_id,
                    payment_status=order.payment_status,
                    amount=refund_amount,
                    payment_gateway='razorpay',
                    razorpay_payment_id=refund_data.get('entity', {}).get('id', ''),
                    payload=payload,
                )

        return Response({'received': True}, status=status.HTTP_200_OK)


class PayPalWebhookView(APIView):
    """PayPal REST webhook endpoint for asynchronous payment status updates"""
    authentication_classes = []
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        """Handle PayPal webhook events"""
        if not paypal_configured:
            return Response(
                {'error': 'PayPal is not configured'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        try:
            webhook_event = _parse_paypal_webhook_event(request)
            if not webhook_event:
                return Response({'error': 'Invalid webhook signature'}, status=status.HTTP_400_BAD_REQUEST)

            event_id = webhook_event.get('id', '')
            if _paypal_event_already_processed(event_id):
                return Response({'received': True}, status=status.HTTP_200_OK)

            event_type = webhook_event.get('event_type', '')
            resource = webhook_event.get('resource', {}) or {}
            payment_id = (
                resource.get('parent_payment')
                or resource.get('id')
                or ''
            )
            custom_order_id = resource.get('custom') or webhook_event.get('custom')

            if event_type == 'PAYMENT.CAPTURE.COMPLETED':
                resource = webhook_event.get('resource', {}) or {}
                paypal_order_id = resource.get('supplementary_data', {}).get('related_ids', {}).get('order_id', '')
                custom_order_id = resource.get('custom_id')
                order = _find_paypal_order(paypal_order_id, custom_order_id)

                if order and resource.get('status') == 'COMPLETED':
                    _mark_paypal_order_paid(
                        order,
                        paypal_order_id or order.payment_id,
                        webhook_event,
                        event_type=event_type,
                    )

            elif event_type == 'PAYMENT.SALE.COMPLETED':
                state = resource.get('state', '')
                amount = resource.get('amount', {}).get('total', '0')
                order = _find_paypal_order(payment_id, custom_order_id)

                if order and state == 'completed':
                    order.payment_id = payment_id or order.payment_id
                    order.payment_status = 'succeeded'
                    if order.status == 'initial':
                        order.status = 'in_process'
                    order.save(update_fields=['payment_id', 'payment_status', 'status', 'updated_at'])
                    finalize_order_carts(order)

                    _record_payment_event(
                        order=order,
                        event_id=event_id,
                        event_type=event_type,
                        payment_intent_id=payment_id,
                        payment_status='succeeded',
                        amount=Decimal(str(amount)),
                        currency=_paypal_currency(),
                        payment_gateway='paypal',
                        payload=webhook_event,
                    )

            elif event_type == 'PAYMENT.SALE.DENIED':
                order = _find_paypal_order(payment_id, custom_order_id)

                if order:
                    cancel_unpaid_order(order)

                    _record_payment_event(
                        order=order,
                        event_id=event_id,
                        event_type=event_type,
                        payment_intent_id=payment_id,
                        payment_status='failed',
                        payment_gateway='paypal',
                        payload=webhook_event,
                    )

            elif event_type == 'PAYMENT.SALE.REFUNDED':
                parent_payment = resource.get('parent_payment', '')
                amount = resource.get('amount', {}).get('total', '0')
                order = _find_paypal_order(parent_payment, custom_order_id)

                if order:
                    order.payment_status = 'refunded'
                    order.save(update_fields=['payment_status', 'updated_at'])

                    _record_payment_event(
                        order=order,
                        event_id=event_id,
                        event_type=event_type,
                        payment_intent_id=parent_payment,
                        payment_status='refunded',
                        amount=Decimal(str(amount)),
                        currency=_paypal_currency(),
                        payment_gateway='paypal',
                        payload=webhook_event,
                    )

            elif event_type == 'PAYMENT.SALE.REVERSED':
                order = _find_paypal_order(payment_id, custom_order_id)

                if order:
                    order.payment_status = 'reversed'
                    order.save(update_fields=['payment_status', 'updated_at'])

                    _record_payment_event(
                        order=order,
                        event_id=event_id,
                        event_type=event_type,
                        payment_intent_id=payment_id,
                        payment_status='reversed',
                        payment_gateway='paypal',
                        payload=webhook_event,
                    )

            return Response({'received': True}, status=status.HTTP_200_OK)

        except (json.JSONDecodeError, ValueError):
            return Response({'error': 'Invalid payload'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class PayPalPaymentCompleteView(APIView):
    """PayPal return endpoint - captures payment after user approves on PayPal"""
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        """Capture PayPal Orders API v2 checkout after approval"""
        if not paypal_configured:
            return Response(
                {'error': 'PayPal is not configured'},
                status=status.HTTP_503_SERVICE_UNAVAILABLE
            )

        try:
            paypal_order_id = (
                request.data.get('paypal_order_id')
                or request.data.get('token')
                or request.data.get('payment_id')
            )
            order_id = request.data.get('order_id')

            if not paypal_order_id:
                return Response({
                    'error': 'Missing PayPal order id'
                }, status=status.HTTP_400_BAD_REQUEST)

            order = None
            if order_id:
                try:
                    order = Order.objects.get(id=order_id, user=request.user)
                except Order.DoesNotExist:
                    pass

            if not order:
                order = Order.objects.filter(payment_id=paypal_order_id, user=request.user).first()

            if order and order.payment_status in PAID_PAYMENT_STATUSES:
                return Response({
                    'message': 'Payment already completed',
                    'payment_id': paypal_order_id,
                    'status': order.payment_status,
                    'order_id': order.id,
                }, status=status.HTTP_200_OK)

            existing_order = get_checkout_order(paypal_order_id)
            if existing_order.get('status') == 'COMPLETED':
                purchase_units = existing_order.get('purchase_units', [])
                custom_order_id = purchase_units[0].get('custom_id') if purchase_units else None
                if not order:
                    order = _find_paypal_order(paypal_order_id, custom_order_id)
                    if order and order.user_id != request.user.id:
                        order = None
                if order and order.payment_status not in PAID_PAYMENT_STATUSES:
                    _mark_paypal_order_paid(order, paypal_order_id, existing_order, event_type='payment_captured')
                return Response({
                    'message': 'Payment already completed',
                    'payment_id': paypal_order_id,
                    'status': 'succeeded',
                    'order_id': order.id if order else order_id,
                }, status=status.HTTP_200_OK)

            capture_result = capture_checkout_order(paypal_order_id)
            if capture_result.get('status') != 'COMPLETED':
                return Response({
                    'error': 'PayPal payment was not completed'
                }, status=status.HTTP_400_BAD_REQUEST)

            if not order:
                purchase_units = capture_result.get('purchase_units', [])
                custom_order_id = purchase_units[0].get('custom_id') if purchase_units else None
                order = _find_paypal_order(paypal_order_id, custom_order_id)
                if order and order.user_id != request.user.id:
                    order = None

            if order:
                _mark_paypal_order_paid(order, paypal_order_id, capture_result, event_type='payment_captured')

            return Response({
                'message': 'Payment captured successfully',
                'payment_id': paypal_order_id,
                'status': 'succeeded',
                'order_id': order.id if order else order_id,
            }, status=status.HTTP_200_OK)

        except PayPalAPIError as e:
            return Response({
                'error': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({
                'error': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)


class ReturnAndReplaceViewSet(ModelViewSet):
    """ViewSet for Return and Replace requests"""
    serializer_class = ReturnAndReplaceOrderSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['action', 'requested', 'approved', 'active']
    ordering = ['-created_at']

    def get_queryset(self):
        """Users can only access their own return/replace requests"""
        user = self.request.user
        queryset = ReturnAndReplaceOrder.objects.filter(user=user, active=True)

        # Admin and suppliers can see all requests
        if hasattr(user, 'user_role') and user.user_role:
            if user.user_role.name in ['admin'] or user.is_superuser:
                queryset = ReturnAndReplaceOrder.objects.filter(active=True)
            elif user.user_role.name == 'supplier':
                # Suppliers can see requests for their products
                queryset = ReturnAndReplaceOrder.objects.filter(
                    order__cart__product__user=user,
                    active=True
                )

        return queryset

    def get_serializer_class(self):
        if self.action == 'create':
            return ReturnAndReplaceCreateSerializer
        return ReturnAndReplaceOrderSerializer

    @action(detail=True, methods=['post'])
    def approve(self, request, pk=None):
        """Approve return/replace request (Admin/Supplier only)"""
        return_replace = self.get_object()

        # Check permissions
        if not (hasattr(request.user, 'user_role') and request.user.user_role):
            return Response(
                {'error': 'Permission denied'},
                status=status.HTTP_403_FORBIDDEN
            )

        if request.user.user_role.name not in ['admin', 'supplier'] and not request.user.is_superuser:
            return Response(
                {'error': 'Permission denied'},
                status=status.HTTP_403_FORBIDDEN
            )

        return_replace.approved = True
        return_replace.save()
        order = return_replace.order.order
        order.status = 'return' if return_replace.action == 'Return' else 'replace'
        order.save(update_fields=['status', 'updated_at'])

        # Process refund for returns
        if return_replace.action == 'Return':
            if order.payment_id and order.payment_status in ['authorized', 'succeeded', 'processing'] and order.payment_method == 'razorpay' and razorpay_client:
                try:
                    refunded_amount = return_replace.order.cart.product.price * return_replace.order.cart.quantity
                    refund = razorpay_client.payment.refund(
                        order.payment_id,
                        {'amount': int(refunded_amount * 100)}
                    )
                    order.payment_status = 'refunded'
                    if refunded_amount < order.total_amount:
                        order.payment_status = 'partially_refunded'
                    order.save(update_fields=['payment_status', 'updated_at'])
                    _record_payment_event(
                        order=order,
                        event_id=refund.get('id', ''),
                        event_type='manual_refund',
                        payment_intent_id=order.payment_id,
                        payment_status=order.payment_status,
                        amount=refunded_amount,
                        payment_gateway='razorpay',
                        razorpay_payment_id=refund.get('id', ''),
                        payload={
                            'refund_id': refund.get('id'),
                            'status': refund.get('status'),
                            'source': 'return_approval',
                            'order_item_id': return_replace.order_id,
                        },
                    )
                except Exception:
                    pass  # Handle refund error silently for now

        return Response({
            'message': f'{return_replace.action} request approved successfully'
        })

    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        """Cancel return/replace request"""
        return_replace = self.get_object()

        if return_replace.user != request.user:
            return Response(
                {'error': 'You can only cancel your own requests'},
                status=status.HTTP_403_FORBIDDEN
            )

        return_replace.active = False
        return_replace.save()

        return Response({
            'message': 'Request cancelled successfully'
        })


class OrderTrackingView(APIView):
    """API view for order tracking"""
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request):
        """Track order by ID"""
        serializer = OrderTrackingSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            order_id = serializer.validated_data['order_id']
            order = Order.objects.get(id=order_id, user=request.user)
            
            order_items = OrderItem.objects.filter(order=order, active=True)
            
            return Response({
                'order': OrderSerializer(order, context={'request': request}).data,
                'order_items': OrderItemSerializer(order_items, many=True).data,
                'tracking_info': {
                    'status': order.status,
                    'created_at': order.created_at,
                    'updated_at': order.updated_at,
                    'estimated_delivery': None  # You can add delivery estimation logic
                }
            })
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
