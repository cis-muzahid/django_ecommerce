import { useEffect, useState } from 'react';
import { Link, useSearchParams, useNavigate } from 'react-router-dom';
import BrandsCarousel from '../components/BrandsCarousel';
import Breadcrumbs from '../components/Breadcrumbs';
import { useAuth } from '../context/AuthContext';
import apiClient from '../services/apiClient';
import { productHref, productImage } from '../utils/catalog';

// ─── Status pipeline ──────────────────────────────────────────────────────────
// Maps every possible order.status to a step index (0-based) in the stepper.
// cancelled / return / replace are handled separately as terminal states.
const STEPS = [
  { key: 'ordered',   label: 'Order Placed',   icon: 'fa-shopping-cart' },
  { key: 'confirmed', label: 'Confirmed',       icon: 'fa-check-circle' },
  { key: 'shipped',   label: 'Shipped',         icon: 'fa-truck' },
  { key: 'delivered', label: 'Delivered',       icon: 'fa-home' },
];

// Which stepper index each backend status maps to
const STATUS_TO_STEP = {
  initial:    0,
  in_process: 1,
  shipped:    2,   // if you add this status later
  deliverd:   3,   // note: backend has typo "deliverd"
  delivered:  3,
};

// Non-linear terminal statuses handled outside the stepper
const TERMINAL_STATUS = {
  cancelled: { label: 'Cancelled',    color: '#dc3545', icon: 'fa-times-circle' },
  return:    { label: 'Return Requested', color: '#fd7e14', icon: 'fa-undo' },
  replace:   { label: 'Replacement Requested', color: '#6f42c1', icon: 'fa-exchange' },
};

function getActiveStep(status) {
  return STATUS_TO_STEP[status] ?? 0;
}

function formatDate(iso) {
  if (!iso) return null;
  return new Date(iso).toLocaleDateString('en-IN', {
    day: 'numeric', month: 'short', year: 'numeric',
  });
}

function formatDateTime(iso) {
  if (!iso) return '—';
  return new Date(iso).toLocaleString('en-IN', {
    day: 'numeric', month: 'short', year: 'numeric',
    hour: '2-digit', minute: '2-digit',
  });
}

function estimatedDelivery(createdAt) {
  if (!createdAt) return null;
  const d = new Date(createdAt);
  d.setDate(d.getDate() + 7);
  return formatDate(d.toISOString());
}

function paymentMethodLabel(method) {
  const map = { razorpay: 'Razorpay', paypal: 'PayPal', stripe: 'Card', none: 'Cash on Delivery' };
  return map[method] || method || 'N/A';
}

function paymentStatusBadge(status) {
  const map = {
    succeeded:          { color: '#28a745', label: 'Paid' },
    authorized:         { color: '#28a745', label: 'Paid' },
    pending:            { color: '#ffc107', label: 'Pending' },
    failed:             { color: '#dc3545', label: 'Failed' },
    refunded:           { color: '#17a2b8', label: 'Refunded' },
    partially_refunded: { color: '#fd7e14', label: 'Partially Refunded' },
    cod_pending:        { color: '#fd7e14', label: '💵 Pay on Delivery' },
    cod_collected:      { color: '#28a745', label: '✓ Cash Collected' },
    cod_cancelled:      { color: '#6c757d', label: 'COD Cancelled' },
  };
  const entry = map[status] || { color: '#6c757d', label: status || 'N/A' };
  return (
    <span style={{
      background: entry.color, color: '#fff', padding: '2px 10px',
      borderRadius: 12, fontSize: 12, fontWeight: 600,
    }}>
      {entry.label}
    </span>
  );
}

// ─── Stepper component ────────────────────────────────────────────────────────
function OrderStepper({ status, createdAt, updatedAt }) {
  const terminal = TERMINAL_STATUS[status];
  const activeStep = getActiveStep(status);

  if (terminal) {
    return (
      <div style={{
        display: 'flex', alignItems: 'center', justifyContent: 'center',
        gap: 12, padding: '28px 0 20px',
      }}>
        <i
          className={`fa ${terminal.icon}`}
          style={{ fontSize: 36, color: terminal.color }}
        />
        <div>
          <div style={{ fontWeight: 700, fontSize: 18, color: terminal.color }}>
            {terminal.label}
          </div>
          <div style={{ color: '#888', fontSize: 13, marginTop: 2 }}>
            {formatDateTime(updatedAt)}
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="order-stepper">
      {STEPS.map((step, idx) => {
        const done    = idx < activeStep;
        const current = idx === activeStep;
        const color   = done || current ? '#2874f0' : '#c8c8c8';
        return (
          <div key={step.key} className="order-stepper-item">
            {/* Connector line before each step (except first) */}
            {idx > 0 && (
              <div
                className="order-stepper-line"
                style={{ background: done || current ? '#2874f0' : '#e0e0e0' }}
              />
            )}

            <div className="order-stepper-circle" style={{ borderColor: color, background: done || current ? color : '#fff' }}>
              <i
                className={`fa ${step.icon}`}
                style={{ color: done || current ? '#fff' : '#c8c8c8', fontSize: 16 }}
              />
            </div>

            <div className="order-stepper-label" style={{ color: done || current ? '#333' : '#aaa' }}>
              <div style={{ fontWeight: current ? 700 : 500, fontSize: 13 }}>{step.label}</div>
              {current && (
                <div style={{ fontSize: 11, color: '#2874f0', marginTop: 2 }}>
                  {formatDate(updatedAt)}
                </div>
              )}
              {step.key === 'delivered' && done && (
                <div style={{ fontSize: 11, color: '#28a745', marginTop: 2 }}>
                  Delivered on {formatDate(updatedAt)}
                </div>
              )}
              {step.key === 'ordered' && (
                <div style={{ fontSize: 11, color: '#888', marginTop: 2 }}>
                  {formatDate(createdAt)}
                </div>
              )}
            </div>
          </div>
        );
      })}
    </div>
  );
}

// ─── Main Page ────────────────────────────────────────────────────────────────
export default function OrderTrackingPage() {
  const navigate = useNavigate();
  const { isAuthenticated, loading: authLoading } = useAuth();
  const [searchParams] = useSearchParams();
  const orderId = searchParams.get('order_id');

  const [order, setOrder] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    if (authLoading) return;
    if (!isAuthenticated) { navigate('/login'); return; }
    if (orderId) fetchOrder();
    else setLoading(false);
  }, [authLoading, isAuthenticated, orderId]);

  const fetchOrder = async () => {
    try {
      setLoading(true);
      setError(null);
      const res = await apiClient.get(`/orders/${orderId}/`);
      setOrder(res.data);
    } catch {
      setError('Could not load order details. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const activeItems = order?.order_items?.filter((i) => i.active !== false) || [];
  const isDelivered = order?.status === 'deliverd' || order?.status === 'delivered';

  return (
    <>
      <Breadcrumbs items={[{ label: 'My Orders', link: '/orders' }, { label: 'Track Order' }]} />

      <div className="order-tracking-page">
        {authLoading || loading ? (
          <div className="text-center" style={{ padding: 60 }}>
            <i className="fa fa-spinner fa-spin fa-2x" style={{ color: '#2874f0' }} />
            <p style={{ marginTop: 12, color: '#888' }}>Loading order details…</p>
          </div>
        ) : error ? (
          <div className="text-center" style={{ padding: 60 }}>
            <i className="fa fa-exclamation-circle fa-3x" style={{ color: '#dc3545' }} />
            <p style={{ marginTop: 12 }}>{error}</p>
            <Link to="/orders" className="btn btn-primary">Back to Orders</Link>
          </div>
        ) : !order ? (
          <div className="text-center" style={{ padding: 60 }}>
            <i className="fa fa-search fa-3x" style={{ color: '#ccc' }} />
            <h4 style={{ marginTop: 16 }}>No order ID provided</h4>
            <Link to="/orders" className="btn btn-primary" style={{ marginTop: 12 }}>View My Orders</Link>
          </div>
        ) : (
          <div className="order-tracking-wrap">

            {/* ── Header card ── */}
            <div className="ot-card ot-header-card">
              <div className="ot-header-left">
                <div className="ot-order-id">Order #{order.id}</div>
                <div className="ot-order-meta">
                  Placed on {formatDate(order.created_at)}
                  &nbsp;·&nbsp;
                  {activeItems.length} item{activeItems.length !== 1 ? 's' : ''}
                  &nbsp;·&nbsp;
                  <strong>₹{Number(order.total_amount || 0).toFixed(2)}</strong>
                </div>
              </div>
              <div className="ot-header-right">
                {paymentStatusBadge(order.payment_status)}
                <div className="ot-payment-method">{paymentMethodLabel(order.payment_method)}</div>
              </div>
            </div>

            {/* ── Progress stepper ── */}
            <div className="ot-card">
              <div className="ot-section-title">
                <i className="fa fa-map-marker" /> Delivery Status
              </div>

              {/* Estimated delivery line */}
              {!TERMINAL_STATUS[order.status] && !isDelivered && (
                <div style={{ textAlign: 'center', marginBottom: 8 }}>
                  <span style={{ background: '#fff3cd', color: '#856404', padding: '4px 14px', borderRadius: 20, fontSize: 13, fontWeight: 600 }}>
                    <i className="fa fa-calendar" /> Expected by {estimatedDelivery(order.created_at)}
                  </span>
                </div>
              )}
              {isDelivered && (
                <div style={{ textAlign: 'center', marginBottom: 8 }}>
                  <span style={{ background: '#d4edda', color: '#155724', padding: '4px 14px', borderRadius: 20, fontSize: 13, fontWeight: 600 }}>
                    <i className="fa fa-check" /> Delivered on {formatDate(order.updated_at)}
                  </span>
                </div>
              )}

              <OrderStepper
                status={order.status}
                createdAt={order.created_at}
                updatedAt={order.updated_at}
              />

              {/* COD notice */}
              {order.payment_status === 'cod_pending' && !TERMINAL_STATUS[order.status] && (
                <div className="ot-refund-notice" style={{ borderColor: '#fd7e14', color: '#7d3c00' }}>
                  <i className="fa fa-money" /> Please keep <strong>₹{Number(order.total_amount || 0).toFixed(2)}</strong> ready to pay the delivery partner.
                </div>
              )}
              {order.payment_status === 'cod_collected' && (
                <div className="ot-refund-notice" style={{ borderColor: '#28a745', color: '#155724' }}>
                  <i className="fa fa-check-circle" /> Cash on delivery payment collected successfully.
                </div>
              )}

              {/* Refund notice if applicable */}
              {order.payment_status === 'refunded' && (
                <div className="ot-refund-notice" style={{ borderColor: '#17a2b8', color: '#0c6268' }}>
                  <i className="fa fa-check-circle" /> Refund has been processed to your original payment method.
                </div>
              )}
              {order.payment_status === 'partially_refunded' && (
                <div className="ot-refund-notice" style={{ borderColor: '#fd7e14', color: '#7d3c00' }}>
                  <i className="fa fa-info-circle" /> A partial refund has been processed.
                </div>
              )}
              {order.payment_status === 'succeeded' && order.status === 'cancelled' && (
                <div className="ot-refund-notice" style={{ borderColor: '#dc3545', color: '#7b1a1a' }}>
                  <i className="fa fa-clock-o" /> Refund is being processed. It may take 5–7 business days.
                </div>
              )}
            </div>

            {/* ── Order items ── */}
            <div className="ot-card">
              <div className="ot-section-title">
                <i className="fa fa-shopping-bag" /> Items in this order
              </div>
              <div className="ot-items-list">
                {activeItems.map((item) => {
                  const product = item.cart?.product;
                  return (
                    <div key={item.id} className="ot-item-row">
                      <Link to={productHref(product)} className="ot-item-image-wrap">
                        <img
                          src={productImage(product)}
                          alt={item.product_name || product?.name}
                          className="ot-item-image"
                        />
                      </Link>
                      <div className="ot-item-info">
                        <Link to={productHref(product)} className="ot-item-name">
                          {item.product_name || product?.name || 'Product'}
                        </Link>
                        <div className="ot-item-meta">
                          Qty: {item.cart?.quantity || 1}
                          &nbsp;·&nbsp;
                          ₹{Number(item.product_price || 0).toFixed(2)} each
                        </div>
                      </div>
                      <div className="ot-item-total">
                        ₹{Number(item.total_price || 0).toFixed(2)}
                      </div>
                    </div>
                  );
                })}
              </div>

              {/* Price summary */}
              <div className="ot-price-summary">
                <div className="ot-price-row">
                  <span>Subtotal ({activeItems.length} items)</span>
                  <span>₹{Number(order.total_amount || 0).toFixed(2)}</span>
                </div>
                <div className="ot-price-row">
                  <span>Delivery Charges</span>
                  <span style={{ color: '#28a745', fontWeight: 600 }}>FREE</span>
                </div>
                <div className="ot-price-row ot-price-total">
                  <span>Total Amount</span>
                  <span>₹{Number(order.total_amount || 0).toFixed(2)}</span>
                </div>
              </div>
            </div>

            {/* ── Delivery address + Payment info side by side ── */}
            <div className="ot-two-col">
              <div className="ot-card">
                <div className="ot-section-title">
                  <i className="fa fa-map-marker" /> Delivery Address
                </div>
                <div className="ot-address-text">
                  {order.address || 'No address on record'}
                </div>
              </div>

              <div className="ot-card">
                <div className="ot-section-title">
                  <i className="fa fa-credit-card" /> Payment Details
                </div>
                <table className="ot-detail-table">
                  <tbody>
                    <tr>
                      <td className="ot-detail-label">Method</td>
                      <td>{paymentMethodLabel(order.payment_method)}</td>
                    </tr>
                    <tr>
                      <td className="ot-detail-label">Status</td>
                      <td>{paymentStatusBadge(order.payment_status)}</td>
                    </tr>
                    {order.payment_id && order.payment_id !== 'none' && (
                      <tr>
                        <td className="ot-detail-label">Transaction ID</td>
                        <td>
                          <span style={{ fontFamily: 'monospace', fontSize: 12, wordBreak: 'break-all' }}>
                            {order.payment_id}
                          </span>
                        </td>
                      </tr>
                    )}
                    <tr>
                      <td className="ot-detail-label">Amount Paid</td>
                      <td><strong>₹{Number(order.total_amount || 0).toFixed(2)}</strong></td>
                    </tr>
                  </tbody>
                </table>
              </div>
            </div>

            {/* ── Order timeline ── */}
            <div className="ot-card">
              <div className="ot-section-title">
                <i className="fa fa-history" /> Order Timeline
              </div>
              <div className="ot-timeline">
                <div className="ot-timeline-item ot-timeline-active">
                  <div className="ot-timeline-dot" />
                  <div className="ot-timeline-content">
                    <div className="ot-timeline-title">Order Placed</div>
                    <div className="ot-timeline-date">{formatDateTime(order.created_at)}</div>
                  </div>
                </div>

                {order.status !== 'initial' && (
                  <div className="ot-timeline-item ot-timeline-active">
                    <div className="ot-timeline-dot" />
                    <div className="ot-timeline-content">
                      <div className="ot-timeline-title">Order Confirmed &amp; Payment Received</div>
                      <div className="ot-timeline-date">{formatDateTime(order.updated_at)}</div>
                    </div>
                  </div>
                )}

                {(order.status === 'deliverd' || order.status === 'delivered') && (
                  <div className="ot-timeline-item ot-timeline-active">
                    <div className="ot-timeline-dot" style={{ background: '#28a745', borderColor: '#28a745' }} />
                    <div className="ot-timeline-content">
                      <div className="ot-timeline-title" style={{ color: '#28a745' }}>
                        <i className="fa fa-check-circle" /> Delivered
                      </div>
                      <div className="ot-timeline-date">{formatDateTime(order.updated_at)}</div>
                    </div>
                  </div>
                )}

                {order.status === 'cancelled' && (
                  <div className="ot-timeline-item">
                    <div className="ot-timeline-dot" style={{ background: '#dc3545', borderColor: '#dc3545' }} />
                    <div className="ot-timeline-content">
                      <div className="ot-timeline-title" style={{ color: '#dc3545' }}>
                        <i className="fa fa-times-circle" /> Order Cancelled
                      </div>
                      <div className="ot-timeline-date">{formatDateTime(order.updated_at)}</div>
                    </div>
                  </div>
                )}

                {(order.status === 'return' || order.status === 'replace') && (
                  <div className="ot-timeline-item">
                    <div className="ot-timeline-dot" style={{ background: '#fd7e14', borderColor: '#fd7e14' }} />
                    <div className="ot-timeline-content">
                      <div className="ot-timeline-title" style={{ color: '#fd7e14' }}>
                        <i className="fa fa-undo" /> {order.status === 'return' ? 'Return' : 'Replacement'} Requested
                      </div>
                      <div className="ot-timeline-date">{formatDateTime(order.updated_at)}</div>
                    </div>
                  </div>
                )}

                {order.payment_status === 'cod_collected' && (
                  <div className="ot-timeline-item ot-timeline-active">
                    <div className="ot-timeline-dot" style={{ background: '#28a745', borderColor: '#28a745' }} />
                    <div className="ot-timeline-content">
                      <div className="ot-timeline-title" style={{ color: '#28a745' }}>
                        <i className="fa fa-money" /> Cash on Delivery — Payment Collected
                      </div>
                      <div className="ot-timeline-date">{formatDateTime(order.updated_at)}</div>
                    </div>
                  </div>
                )}

                {(order.payment_status === 'refunded' || order.payment_status === 'partially_refunded') && (                  <div className="ot-timeline-item ot-timeline-active">
                    <div className="ot-timeline-dot" style={{ background: '#17a2b8', borderColor: '#17a2b8' }} />
                    <div className="ot-timeline-content">
                      <div className="ot-timeline-title" style={{ color: '#17a2b8' }}>
                        <i className="fa fa-inr" />{' '}
                        {order.payment_status === 'refunded' ? 'Full Refund Processed' : 'Partial Refund Processed'}
                      </div>
                      <div className="ot-timeline-date">Credited back to your account within 5–7 business days</div>
                    </div>
                  </div>
                )}
              </div>
            </div>

            {/* ── Actions ── */}
            <div className="ot-actions">
              <Link to="/orders" className="btn btn-default ot-btn">
                <i className="fa fa-arrow-left" /> Back to My Orders
              </Link>
              <Link to="/" className="btn btn-primary ot-btn">
                Continue Shopping
              </Link>
            </div>

          </div>
        )}
      </div>

      <BrandsCarousel />
    </>
  );
}
