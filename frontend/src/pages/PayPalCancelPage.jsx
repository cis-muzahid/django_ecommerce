import { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useCart } from '../context/CartContext';
import * as orderService from '../services/orderService';

export default function PayPalCancelPage() {
  const navigate = useNavigate();
  const { refreshCart } = useCart();

  useEffect(() => {
    async function handleCancel() {
      const orderId = sessionStorage.getItem('paypal_order_id');

      if (orderId) {
        try {
          await orderService.cancelOrder(orderId);
        } catch (error) {
          console.error('Failed to cancel unpaid PayPal order:', error);
        }
      }

      sessionStorage.removeItem('paypal_order_id');
      sessionStorage.removeItem('paypal_payment_id');
      await refreshCart();
      navigate('/checkout', { replace: true });
    }

    handleCancel();
  }, [navigate, refreshCart]);

  return (
    <div className="text-center" style={{ padding: '100px 20px' }}>
      <div className="alert alert-warning">
        <h2>Payment Cancelled</h2>
        <p>You cancelled the PayPal payment process.</p>
        <p>Your cart has been restored. Redirecting you back to checkout...</p>
      </div>
    </div>
  );
}
