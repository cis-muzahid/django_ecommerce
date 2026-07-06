import { useEffect, useMemo, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import Breadcrumbs from '../components/Breadcrumbs';
import { useAuth } from '../context/AuthContext';
import { useCart } from '../context/CartContext';
import apiClient from '../services/apiClient';
import * as orderService from '../services/orderService';

const RAZORPAY_SCRIPT_ID = 'razorpay-js-sdk';

function loadRazorpayScript() {
  if (window.Razorpay) {
    return Promise.resolve(window.Razorpay);
  }

  return new Promise((resolve, reject) => {
    const existing = document.getElementById(RAZORPAY_SCRIPT_ID);
    if (existing) {
      existing.addEventListener('load', () => resolve(window.Razorpay), { once: true });
      existing.addEventListener('error', reject, { once: true });
      return;
    }

    const script = document.createElement('script');
    script.id = RAZORPAY_SCRIPT_ID;
    script.src = 'https://checkout.razorpay.com/v1/checkout.js';
    script.async = true;
    script.onload = () => resolve(window.Razorpay);
    script.onerror = reject;
    document.head.appendChild(script);
  });
}

async function pollOrderStatus(orderId, maxAttempts = 8, delayMs = 1500) {
  for (let attempt = 0; attempt < maxAttempts; attempt += 1) {
    const refreshed = await orderService.getOrder(orderId);
    const status = refreshed?.payment_status || 'pending';
    if (['succeeded', 'failed', 'refunded', 'partially_refunded'].includes(status)) {
      return refreshed;
    }
    await new Promise((resolve) => setTimeout(resolve, delayMs));
  }

  return orderService.getOrder(orderId);
}

function addressText(address) {
  if (!address) {
    return '';
  }

  return [
    address.street,
    address.city,
    address.state,
    address.postal_code,
    address.country,
  ].filter(Boolean).join(', ');
}

export default function CheckoutPage() {
  const navigate = useNavigate();
  const { isAuthenticated, loading: authLoading } = useAuth();
  const { clearCart, refreshCart } = useCart();

  const [loading, setLoading] = useState(true);
  const [checkoutData, setCheckoutData] = useState(null);
  const [addresses, setAddresses] = useState([]);
  const [selectedAddress, setSelectedAddress] = useState(null);
  const [paymentMethod, setPaymentMethod] = useState('razorpay');
  const [showAddressChoices, setShowAddressChoices] = useState(false);
  const [showAddressForm, setShowAddressForm] = useState(false);
  const [addressForm, setAddressForm] = useState({
    street: '',
    city: '',
    state: '',
    postal_code: '',
    country: '',
    is_default: true,
  });
  const [processing, setProcessing] = useState(false);
  const [savingAddress, setSavingAddress] = useState(false);
  const [error, setError] = useState(null);

  const defaultAddress = useMemo(
    () => checkoutData?.default_address || addresses.find((address) => address.is_default) || null,
    [checkoutData, addresses],
  );
  const selectedAddressRecord = useMemo(
    () => addresses.find((address) => address.id === selectedAddress) || defaultAddress,
    [addresses, selectedAddress, defaultAddress],
  );

  useEffect(() => {
    if (authLoading) {
      return;
    }
    if (!isAuthenticated) {
      navigate('/login');
      return;
    }

    fetchCheckoutData();
  }, [authLoading, isAuthenticated]);

  async function fetchCheckoutData() {
    try {
      setLoading(true);
      const response = await orderService.getCheckoutInfo();
      const nextAddresses = response.addresses || [];
      const nextDefault = response.default_address || nextAddresses.find((address) => address.is_default);

      setCheckoutData(response);
      setAddresses(nextAddresses);
      setSelectedAddress(nextDefault?.id || nextAddresses[0]?.id || null);
      setShowAddressForm(!nextAddresses.length);
      setShowAddressChoices(!nextDefault && nextAddresses.length > 0);
    } catch (error) {
      console.error('Failed to fetch checkout data:', error);
      if (error.response?.status === 400) {
        setError('Your cart is empty. Please add items before checkout.');
        setTimeout(() => navigate('/cart'), 2000);
      } else {
        setError('Unable to load checkout. Please try again.');
      }
    } finally {
      setLoading(false);
    }
  }

  function handleAddressInputChange(event) {
    const { name, value, type, checked } = event.target;
    setAddressForm((prev) => ({
      ...prev,
      [name]: type === 'checkbox' ? checked : value,
    }));
  }

  async function handleAddAddress(event) {
    event.preventDefault();
    if (!addressForm.street || !addressForm.city || !addressForm.state || !addressForm.postal_code || !addressForm.country) {
      setError('Please fill in every address field');
      return;
    }

    setSavingAddress(true);
    setError(null);

    try {
      const response = await apiClient.post('/addresses/', addressForm);
      const newAddress = response.data;
      setAddresses((prev) => [...prev, newAddress]);
      setSelectedAddress(newAddress.id);
      setAddressForm({
        street: '',
        city: '',
        state: '',
        postal_code: '',
        country: '',
        is_default: false,
      });
      setShowAddressForm(false);
      setShowAddressChoices(false);
    } catch (error) {
      console.error('Failed to add address:', error);
      setError(error.response?.data?.error || 'Failed to add address. Please try again.');
    } finally {
      setSavingAddress(false);
    }
  }

  async function abandonUnpaidOrder(orderId) {
    if (!orderId) {
      return;
    }

    try {
      await orderService.cancelOrder(orderId);
    } catch (cancelError) {
      console.error('Failed to cancel unpaid order:', cancelError);
    }

    await refreshCart();
  }

  async function handlePlaceOrder(event) {
    event.preventDefault();
    if (!selectedAddress) {
      setError('Please select a shipping address');
      return;
    }

    setProcessing(true);
    setError(null);
    let createdOrderId = null;

    try {
      const order = await orderService.createOrder({
        address_id: selectedAddress,
        payment_method: paymentMethod,
      });
      createdOrderId = order.id;

      if (paymentMethod === 'razorpay') {
        const paymentIntent = await orderService.processPayment({
          order_id: order.id,
          payment_method: 'razorpay',
        });

        const RazorpayCtor = await loadRazorpayScript();
        const razorpay = new RazorpayCtor({
          key: paymentIntent.key_id,
          amount: Math.round(paymentIntent.amount * 100),
          currency: paymentIntent.currency,
          order_id: paymentIntent.razorpay_order_id,
          name: 'Ecommerce Store',
          description: `Order #${order.id}`,
          handler: async (response) => {
            if (!response?.razorpay_payment_id) {
              setError('Payment could not be completed. Please try again.');
              setProcessing(false);
              return;
            }

            try {
              const refreshedOrder = await pollOrderStatus(order.id);
              if (['succeeded', 'authorized'].includes(refreshedOrder.payment_status)) {
                await clearCart();
                navigate(`/order-confirmation/${order.id}`);
                return;
              }

              await abandonUnpaidOrder(order.id);
              setError('Payment could not be confirmed. Your cart has been restored.');
            } catch (pollError) {
              console.error('Failed to confirm Razorpay payment:', pollError);
              await abandonUnpaidOrder(order.id);
              setError('Unable to verify payment right now. Your cart has been restored.');
            } finally {
              setProcessing(false);
            }
          },
          modal: {
            ondismiss: async () => {
              await abandonUnpaidOrder(order.id);
              setProcessing(false);
              setError('Payment was cancelled. Your cart has been restored.');
            },
          },
        });

        razorpay.open();
        return;
      }

      if (paymentMethod === 'paypal') {
        const paymentIntent = await orderService.processPayment({
          order_id: order.id,
          payment_method: 'paypal',
        });

        if (paymentIntent?.approval_url) {
          sessionStorage.setItem('paypal_order_id', String(order.id));
          if (paymentIntent.payment_id) {
            sessionStorage.setItem('paypal_payment_id', paymentIntent.payment_id);
          }
          window.location.href = paymentIntent.approval_url;
          return;
        } else {
          await abandonUnpaidOrder(order.id);
          setError('Failed to get PayPal payment approval URL. Please try again.');
          setProcessing(false);
          return;
        }
      }

      await clearCart();
      navigate(`/order-confirmation/${order.id}`);
    } catch (error) {
      console.error('Failed to create order:', error);
      if (createdOrderId) {
        await abandonUnpaidOrder(createdOrderId);
      }
      setError(error.response?.data?.error || 'Failed to create order. Please try again.');
    } finally {
      setProcessing(false);
    }
  }

  if (authLoading || loading) {
    return <p className="text-center" style={{ padding: '50px' }}>Loading checkout...</p>;
  }

  if (!checkoutData?.cart_items?.length) {
    return (
      <>
        <Breadcrumbs items={[{ label: 'Checkout' }]} />
        <div className="checkout-box checkout-page">
          <div className="checkout-empty">Your cart is empty</div>
        </div>
      </>
    );
  }

  return (
    <>
      <Breadcrumbs items={[{ label: 'Checkout' }]} />

      <div className="checkout-box checkout-page">
        <div className="row">
          <div className="col-xs-12 col-sm-9 col-md-9 rht-col">
            <div className="panel-group checkout-steps" id="accordion">
              <div className="panel panel-default checkout-step-01">
                <div className="panel-heading">
                  <h4 className="unicase-checkout-title">
                    <a href="#collapseOne" onClick={(event) => event.preventDefault()}>
                      <span>1</span>Address Details
                    </a>
                  </h4>
                </div>

                <div id="collapseOne" className="panel-collapse collapse in">
                  <div className="panel-body">
                    {error && (
                      <div className="alert alert-danger" role="alert">
                        {error}
                      </div>
                    )}

                    {selectedAddressRecord && !showAddressChoices && !showAddressForm && (
                      <div className="alert alert-info checkout-default-address">
                        <p>
                          {selectedAddressRecord.id === defaultAddress?.id
                            ? 'You have a default address:'
                            : 'Selected address:'}
                        </p>
                        <p><strong>{addressText(selectedAddressRecord)}</strong></p>
                        <p>Would you like to use this address or add a new one?</p>
                        {defaultAddress && (
                          <button
                            type="button"
                            className="btn btn-primary"
                            onClick={() => setSelectedAddress(defaultAddress.id)}
                          >
                            Use Default Address
                          </button>
                        )}
                        <button
                          type="button"
                          className="btn btn-secondary"
                          onClick={() => setShowAddressChoices(true)}
                        >
                          Use other Address
                        </button>
                      </div>
                    )}

                    {showAddressChoices && (
                      <div className="checkout-address-list">
                        {addresses.map((address) => (
                          <div className="alert alert-info" key={address.id}>
                            <p><strong>{addressText(address)}</strong></p>
                            <button
                              type="button"
                              className="btn btn-info"
                              onClick={() => {
                                setSelectedAddress(address.id);
                                setShowAddressChoices(false);
                                setShowAddressForm(false);
                                setError(null);
                              }}
                            >
                              Use this address for this order.
                            </button>
                          </div>
                        ))}
                        <button
                          type="button"
                          className="btn btn-secondary"
                          onClick={() => setShowAddressForm(true)}
                        >
                          Use New Address
                        </button>
                      </div>
                    )}

                    {showAddressForm && (
                      <form className="checkout-address-form div-center" onSubmit={handleAddAddress}>
                        <div className="form-group">
                          <h4 className="checkout-subtitle">Add Shipping Address</h4>
                          <label className="info-title" htmlFor="street">Street <span>*</span></label>
                          <input id="street" name="street" className="form-control unicase-form-control text-input" value={addressForm.street} onChange={handleAddressInputChange} disabled={savingAddress} />

                          <label className="info-title" htmlFor="city">City <span>*</span></label>
                          <input id="city" name="city" className="form-control unicase-form-control text-input" value={addressForm.city} onChange={handleAddressInputChange} disabled={savingAddress} />

                          <label className="info-title" htmlFor="state">State <span>*</span></label>
                          <input id="state" name="state" className="form-control unicase-form-control text-input" value={addressForm.state} onChange={handleAddressInputChange} disabled={savingAddress} />

                          <label className="info-title" htmlFor="postal_code">Postal Code <span>*</span></label>
                          <input id="postal_code" name="postal_code" className="form-control unicase-form-control text-input" value={addressForm.postal_code} onChange={handleAddressInputChange} disabled={savingAddress} />

                          <label className="info-title" htmlFor="country">Country <span>*</span></label>
                          <input id="country" name="country" className="form-control unicase-form-control text-input" value={addressForm.country} onChange={handleAddressInputChange} disabled={savingAddress} />
                        </div>
                        <button type="submit" className="btn-checkout btn-upper btn btn-primary" disabled={savingAddress}>
                          {savingAddress ? 'Adding Address...' : 'Add Address'}
                        </button>
                      </form>
                    )}
                  </div>

                  <div className="checkout-payment-area text-center">
                    <h1>Proceed to checkout</h1>
                    <div className="div-center">
                      <form id="payment-form" onSubmit={handlePlaceOrder}>
                        <div className="form-group">
                          <h4 className="checkout-subtitle">Add Shipping Address</h4>
                          <label className="info-title" htmlFor="shipping-address">Shipping Address <span>*</span></label>
                          <input
                            id="shipping-address"
                            className="form-control unicase-form-control text-input"
                            type="hidden"
                            value={addressText(selectedAddressRecord)}
                            readOnly
                          />
                        </div>
                        <br />
                        <br />
                        <h4>Select your account method to continue</h4>
                        <div className="payment-methods">
                          <label htmlFor="razorpay-radio">
                            <input
                              type="radio"
                              id="razorpay-radio"
                              name="payment_method"
                              value="razorpay"
                              checked={paymentMethod === 'razorpay'}
                              onChange={(event) => setPaymentMethod(event.target.value)}
                            />
                            Razorpay
                          </label>
                          <label htmlFor="paypal-radio">
                            <input
                              type="radio"
                              id="paypal-radio"
                              name="payment_method"
                              value="paypal"
                              checked={paymentMethod === 'paypal'}
                              onChange={(event) => setPaymentMethod(event.target.value)}
                            />
                            PayPal
                          </label>
                          <label htmlFor="no-payment-radio">
                            <input
                              type="radio"
                              id="no-payment-radio"
                              name="payment_method"
                              value="none"
                              checked={paymentMethod === 'none'}
                              onChange={(event) => setPaymentMethod(event.target.value)}
                            />
                            Cash on Delivery
                          </label>
                        </div>
                        <br />
                        <br />
                        <button type="submit" className="btn btn-primary checkout-pay-button" disabled={processing || !selectedAddress}>
                          {processing
                            ? 'Processing...'
                            : paymentMethod === 'none'
                              ? 'Continue with Cash on Delivery'
                              : paymentMethod === 'paypal'
                                ? 'Continue with PayPal'
                                : paymentMethod === 'razorpay'
                                    ? 'Pay with Razorpay'
                                    : 'Pay'}
                        </button>
                      </form>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </>
  );
}
