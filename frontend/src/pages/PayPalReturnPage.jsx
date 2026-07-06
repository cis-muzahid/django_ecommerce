import { useEffect, useRef, useState } from 'react';
import { useNavigate, useSearchParams } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { useCart } from '../context/CartContext';
import apiClient from '../services/apiClient';
import * as orderService from '../services/orderService';

export default function PayPalReturnPage() {
  const navigate = useNavigate();
  const { isAuthenticated, loading: authLoading } = useAuth();
  const { clearCart, refreshCart } = useCart();
  const [searchParams] = useSearchParams();
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const completionStarted = useRef(false);

  useEffect(() => {
    if (authLoading || completionStarted.current) {
      return;
    }

    if (!isAuthenticated) {
      navigate('/login');
      return;
    }

    const paypalOrderId = searchParams.get('token') || searchParams.get('paymentId');
    const storedOrderId = sessionStorage.getItem('paypal_order_id');

    if (!paypalOrderId) {
      setError('Missing payment information');
      setLoading(false);
      return;
    }

    completionStarted.current = true;
    completePayPalPayment(paypalOrderId, storedOrderId);
  }, [authLoading, isAuthenticated, searchParams, navigate]);

  async function completePayPalPayment(paypalOrderId, orderId) {
    try {
      setLoading(true);
      setError(null);

      const response = await apiClient.post('/paypal/complete/', {
        paypal_order_id: paypalOrderId,
        order_id: orderId || undefined,
      });

      if (response.data?.order_id) {
        sessionStorage.removeItem('paypal_order_id');
        sessionStorage.removeItem('paypal_payment_id');
        await clearCart();
        navigate(`/order-confirmation/${response.data.order_id}`, { replace: true });
        return;
      }

      setError('Unable to confirm payment. Please check your orders.');
      setTimeout(() => {
        navigate('/orders');
      }, 3000);
    } catch (err) {
      console.error('Failed to complete PayPal payment:', err);
      const storedOrderId = sessionStorage.getItem('paypal_order_id');
      if (storedOrderId) {
        try {
          await orderService.cancelOrder(storedOrderId);
        } catch (cancelError) {
          console.error('Failed to cancel unpaid PayPal order:', cancelError);
        }
      }
      sessionStorage.removeItem('paypal_order_id');
      sessionStorage.removeItem('paypal_payment_id');
      await refreshCart();
      setError(err.response?.data?.error || 'Payment confirmation failed. Your cart has been restored.');
      setTimeout(() => {
        navigate('/checkout');
      }, 3000);
    } finally {
      setLoading(false);
    }
  }

  if (authLoading || loading) {
    return (
      <div className="text-center" style={{ padding: '100px 20px' }}>
        <h2>Processing your PayPal payment...</h2>
        <p>Please wait while we confirm your payment.</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="text-center" style={{ padding: '100px 20px' }}>
        <div className="alert alert-danger">
          <h3>Payment Error</h3>
          <p>{error}</p>
          <p>Redirecting you back...</p>
        </div>
      </div>
    );
  }

  return null;
}
