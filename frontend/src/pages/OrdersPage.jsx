import { useEffect, useMemo, useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import BrandsCarousel from '../components/BrandsCarousel';
import Breadcrumbs from '../components/Breadcrumbs';
import { useAuth } from '../context/AuthContext';
import apiClient from '../services/apiClient';
import * as orderService from '../services/orderService';
import { productHref, productImage } from '../utils/catalog';

// Orders that have not been paid yet — payment started but never completed
const UNPAID_STATUSES = ['pending', null, undefined, ''];
// COD payment statuses
const COD_STATUSES = ['cod_pending', 'cod_collected', 'cod_cancelled'];

const SEVEN_DAYS_MS = 7 * 24 * 60 * 60 * 1000;

function isWithinLastSevenDays(order) {
  const createdAt = new Date(order.created_at).getTime();
  return Number.isFinite(createdAt) && Date.now() - createdAt <= SEVEN_DAYS_MS;
}

function formatDate(iso) {
  if (!iso) return '';
  return new Date(iso).toLocaleDateString('en-IN', {
    day: 'numeric', month: 'short', year: 'numeric',
  });
}

function formatMoney(value) {
  return `₹${Number(value || 0).toFixed(2)}`;
}

function paymentMethodLabel(method) {
  const map = { razorpay: 'Razorpay', paypal: 'PayPal', stripe: 'Card', none: 'Cash on Delivery' };
  return map[method] || method || 'N/A';
}

// ─── Status chip ──────────────────────────────────────────────────────────────
function OrderStatusChip({ status }) {
  const config = {
    initial:    { label: 'Order Placed',  bg: '#e3f0ff', color: '#1a56a0' },
    in_process: { label: 'Confirmed',     bg: '#fff3cd', color: '#856404' },
    shipped:    { label: 'Shipped',       bg: '#d4edda', color: '#155724' },
    deliverd:   { label: 'Delivered',     bg: '#d4edda', color: '#155724' },
    delivered:  { label: 'Delivered',     bg: '#d4edda', color: '#155724' },
    cancelled:  { label: 'Cancelled',     bg: '#f8d7da', color: '#721c24' },
    return:     { label: 'Return Requested', bg: '#fff3e0', color: '#7d4a00' },
    replace:    { label: 'Replacement',   bg: '#ede7f6', color: '#4a235a' },
  };
  const c = config[status] || { label: status || 'Placed', bg: '#f0f0f0', color: '#555' };
  return (
    <span style={{
      background: c.bg, color: c.color,
      padding: '3px 10px', borderRadius: 12,
      fontSize: 11, fontWeight: 700, letterSpacing: 0.3,
      whiteSpace: 'nowrap',
    }}>
      {c.label}
    </span>
  );
}

// ─── Payment badge ────────────────────────────────────────────────────────────
function PaymentBadge({ paymentStatus, orderStatus }) {
  // COD statuses
  if (paymentStatus === 'cod_pending') {
    return <span className="op-badge op-badge-orange">💵 Pay on Delivery</span>;
  }
  if (paymentStatus === 'cod_collected') {
    return <span className="op-badge op-badge-green">✓ Cash Collected</span>;
  }
  if (paymentStatus === 'cod_cancelled') {
    return <span className="op-badge" style={{ background: '#f0f0f0', color: '#888' }}>COD Cancelled</span>;
  }
  // Online payment statuses
  if (paymentStatus === 'refunded') {
    return <span className="op-badge op-badge-teal">✓ Refunded</span>;
  }
  if (paymentStatus === 'partially_refunded') {
    return <span className="op-badge op-badge-orange">⚡ Partial Refund</span>;
  }
  if (paymentStatus === 'succeeded' && orderStatus === 'cancelled') {
    return <span className="op-badge op-badge-red">⚠ Refund Pending</span>;
  }
  if (paymentStatus === 'succeeded' || paymentStatus === 'authorized') {
    return <span className="op-badge op-badge-green">✓ Paid</span>;
  }
  return null;
}

// ─── Mini stepper strip ───────────────────────────────────────────────────────
const STEP_ORDER = ['initial', 'in_process', 'shipped', 'deliverd'];
function MiniStepper({ status }) {
  if (['cancelled', 'return', 'replace'].includes(status)) return null;
  const activeIdx = Math.max(STEP_ORDER.indexOf(status), 0);
  const labels = ['Placed', 'Confirmed', 'Shipped', 'Delivered'];
  return (
    <div className="op-mini-stepper">
      {labels.map((label, idx) => (
        <div key={label} className="op-mini-step">
          {idx > 0 && (
            <div className={`op-mini-line${idx <= activeIdx ? ' op-mini-line-done' : ''}`} />
          )}
          <div className={`op-mini-dot${idx <= activeIdx ? ' op-mini-dot-done' : ''}`} />
          <span className={`op-mini-label${idx === activeIdx ? ' op-mini-label-active' : ''}`}>
            {label}
          </span>
        </div>
      ))}
    </div>
  );
}

// ─── Return request state helper ──────────────────────────────────────────────
function getReturnState(item, returnRequestByItemId) {
  const request = returnRequestByItemId.get(item.id);
  if (!request) return null;
  if (request.approved && request.action === 'Return') {
    const refundDone = ['refunded', 'partially_refunded'].includes(request.payment_status);
    return { label: refundDone ? 'Return Approved — Refund Issued' : 'Return Approved', color: '#28a745' };
  }
  if (request.approved && request.action === 'Replace') {
    return { label: 'Replacement Approved', color: '#6f42c1' };
  }
  return { label: `In Process: ${request.action}`, color: '#fd7e14' };
}

// ─── Main page ────────────────────────────────────────────────────────────────
export default function OrdersPage() {
  const navigate = useNavigate();
  const { isAuthenticated, loading: authLoading } = useAuth();
  const [orders, setOrders] = useState([]);
  const [returnRequests, setReturnRequests] = useState([]);
  const [loading, setLoading] = useState(true);
  const [requestingItem, setRequestingItem] = useState(null);
  const [returnForm, setReturnForm] = useState({ action: '', reason: '' });
  const [message, setMessage] = useState(null);
  const [cancellingId, setCancellingId] = useState(null);
  const [expandedOrderId, setExpandedOrderId] = useState(null);

  useEffect(() => {
    if (authLoading) return;
    if (!isAuthenticated) { navigate('/login'); return; }
    fetchOrders();
  }, [authLoading, isAuthenticated]);

  const fetchOrders = async () => {
    try {
      setLoading(true);
      const [ordersRes, requestsRes] = await Promise.all([
        apiClient.get('/orders/'),
        orderService.getReturnReplaceRequests().catch(() => []),
      ]);
      setOrders(ordersRes.data.results || ordersRes.data || []);
      setReturnRequests(requestsRes.results || requestsRes || []);
    } catch {
      // silently fail — user sees empty state
    } finally {
      setLoading(false);
    }
  };

  // Only show orders where payment actually happened (not abandoned checkouts)
  const paidOrders = useMemo(() => orders.filter((o) => {
    // COD orders are always valid (cod_pending, cod_collected, cod_cancelled all show)
    if (o.payment_method === 'none' || COD_STATUSES.includes(o.payment_status)) return true;
    // Online: only show if payment succeeded / authorized / or it's been refunded
    return !UNPAID_STATUSES.includes(o.payment_status);
  }), [orders]);

  const returnRequestByItemId = useMemo(() => {
    const map = new Map();
    returnRequests.forEach((r) => { if (r.order?.id) map.set(r.order.id, r); });
    return map;
  }, [returnRequests]);

  function canReturn(order) {
    return (
      isWithinLastSevenDays(order) &&
      ['deliverd', 'delivered', 'in_process'].includes(order.status)
    );
  }

  function canCancel(order) {
    return (
      isWithinLastSevenDays(order) &&
      !['cancelled', 'deliverd', 'delivered'].includes(order.status)
    );
  }

  const handleCancelOrder = async (orderId) => {
    if (!confirm('Cancel this order?')) return;
    setCancellingId(orderId);
    try {
      const res = await orderService.cancelOrder(orderId);
      setMessage({ type: 'success', text: res?.message || 'Order cancelled successfully' });
      fetchOrders();
    } catch (err) {
      setMessage({ type: 'danger', text: err.response?.data?.error || 'Unable to cancel this order' });
    } finally {
      setCancellingId(null);
    }
  };

  const handleReturnRequest = async (e) => {
    e.preventDefault();
    if (!returnForm.reason.trim()) {
      setMessage({ type: 'danger', text: 'Please enter a reason' });
      return;
    }
    if (!returnForm.action) {
      setMessage({ type: 'danger', text: 'Please select Return or Replace' });
      return;
    }
    try {
      await orderService.createReturnReplaceRequest({
        order_item_id: requestingItem.id,
        action: returnForm.action,
        reason: returnForm.reason,
      });
      setMessage({ type: 'success', text: `${returnForm.action} request submitted` });
      setRequestingItem(null);
      setReturnForm({ action: '', reason: '' });
      fetchOrders();
    } catch (err) {
      setMessage({ type: 'danger', text: err.response?.data?.error || 'Unable to submit request' });
    }
  };

  return (
    <>
      <Breadcrumbs items={[{ label: 'My Orders' }]} />

      <div className="op-page">

        {message && (
          <div className={`alert alert-${message.type} op-alert`} role="alert">
            {message.text}
            <button type="button" className="close" onClick={() => setMessage(null)}>
              <span>&times;</span>
            </button>
          </div>
        )}

        <div className="op-header">
          <h2 className="op-title">My Orders</h2>
          {!loading && (
            <span className="op-count">
              {paidOrders.length} order{paidOrders.length !== 1 ? 's' : ''}
            </span>
          )}
        </div>

        {loading ? (
          <div className="op-loading">
            <i className="fa fa-spinner fa-spin fa-2x" style={{ color: '#2874f0' }} />
            <p>Loading your orders…</p>
          </div>
        ) : paidOrders.length === 0 ? (
          <div className="op-empty">
            <i className="fa fa-shopping-bag op-empty-icon" />
            <h3>No orders yet</h3>
            <p>Looks like you haven't placed any orders. Start shopping!</p>
            <Link to="/" className="btn btn-primary op-shop-btn">Start Shopping</Link>
          </div>
        ) : (
          <div className="op-orders-list">
            {paidOrders.map((order) => {
              const activeItems = (order.order_items || []).filter((i) => i.active !== false);
              const isExpanded = expandedOrderId === order.id;

              return (
                <div key={order.id} className="op-order-card">

                  {/* ── Order card header ── */}
                  <div className="op-order-header">
                    <div className="op-order-header-left">
                      <span className="op-order-id">Order #{order.id}</span>
                      <span className="op-order-date">{formatDate(order.created_at)}</span>
                    </div>
                    <div className="op-order-header-right">
                      <OrderStatusChip status={order.status} />
                      <PaymentBadge paymentStatus={order.payment_status} orderStatus={order.status} />
                      <span className="op-order-total">{formatMoney(order.total_amount)}</span>
                      {activeItems.length > 1 && (
                        <button
                          type="button"
                          className="op-toggle-btn"
                          aria-label={isExpanded ? 'Collapse' : 'Expand'}
                          onClick={() => setExpandedOrderId(isExpanded ? null : order.id)}
                        >
                          <i className={`fa fa-chevron-${isExpanded ? 'up' : 'down'}`} />
                        </button>
                      )}
                    </div>
                  </div>

                  {/* ── Mini progress stepper (always visible) ── */}
                  <MiniStepper status={order.status} />

                  {/* ── Items (first item always visible, rest shown on expand) ── */}
                  <div className="op-items-wrap">
                    {activeItems.map((item, idx) => {
                      const product = item.cart?.product;
                      const returnState = getReturnState(item, returnRequestByItemId);
                      // Always show first item; show rest only when expanded
                      if (idx > 0 && !isExpanded) return null;

                      return (
                        <div key={item.id} className="op-item-row">
                          <Link to={productHref(product)} className="op-item-img-wrap">
                            <img
                              src={productImage(product)}
                              alt={item.product_name || product?.name}
                              className="op-item-img"
                            />
                          </Link>

                          <div className="op-item-info">
                            <Link to={productHref(product)} className="op-item-name">
                              {item.product_name || product?.name || 'Product'}
                            </Link>
                            <div className="op-item-meta">
                              Qty: {item.cart?.quantity || 1}
                              &nbsp;·&nbsp;
                              {formatMoney(item.product_price)} each
                            </div>
                            {returnState && (
                              <div className="op-return-state" style={{ color: returnState.color }}>
                                <i className="fa fa-info-circle" /> {returnState.label}
                              </div>
                            )}
                          </div>

                          <div className="op-item-total">{formatMoney(item.total_price)}</div>
                        </div>
                      );
                    })}

                    {/* Show "X more items" toggle */}
                    {activeItems.length > 1 && !isExpanded && (
                      <button
                        type="button"
                        className="op-more-btn"
                        onClick={() => setExpandedOrderId(order.id)}
                      >
                        + {activeItems.length - 1} more item{activeItems.length - 1 !== 1 ? 's' : ''}
                      </button>
                    )}
                  </div>

                  {/* ── Payment info row ── */}
                  <div className="op-payment-row">
                    <span className="op-payment-method">
                      <i className="fa fa-credit-card" /> {paymentMethodLabel(order.payment_method)}
                    </span>
                    <span className="op-delivery-info">
                      <i className="fa fa-truck" />
                      {order.status === 'deliverd' || order.status === 'delivered'
                        ? ` Delivered on ${formatDate(order.updated_at)}`
                        : order.status === 'cancelled'
                          ? ' Order Cancelled'
                          : ` Expected by ${formatDate(new Date(new Date(order.created_at).getTime() + 7 * 24 * 60 * 60 * 1000).toISOString())}`
                      }
                    </span>
                  </div>

                  {/* ── Action buttons ── */}
                  <div className="op-actions-row">
                    <Link
                      to={`/orders/tracking?order_id=${order.id}`}
                      className="op-action-btn op-action-track"
                    >
                      <i className="fa fa-map-marker" /> Track Order
                    </Link>

                    {canReturn(order) && activeItems.map((item) => {
                      const returnState = getReturnState(item, returnRequestByItemId);
                      if (returnState) return null;
                      return (
                        <button
                          key={item.id}
                          type="button"
                          className="op-action-btn op-action-return"
                          onClick={() => setRequestingItem(item)}
                        >
                          <i className="fa fa-undo" /> Return / Replace
                        </button>
                      );
                    })}

                    {canCancel(order) && (
                      <button
                        type="button"
                        className="op-action-btn op-action-cancel"
                        disabled={cancellingId === order.id}
                        onClick={() => handleCancelOrder(order.id)}
                      >
                        {cancellingId === order.id
                          ? <><i className="fa fa-spinner fa-spin" /> Cancelling…</>
                          : <><i className="fa fa-times" /> Cancel Order</>
                        }
                      </button>
                    )}
                  </div>

                </div>
              );
            })}
          </div>
        )}
      </div>

      {/* ── Return / Replace modal ── */}
      {requestingItem && (
        <div className="modal fade show orders-return-modal" role="dialog" aria-modal="true">
          <div className="modal-dialog modal-dialog-centered" role="document">
            <div className="modal-content">
              <form onSubmit={handleReturnRequest}>
                <div className="modal-header">
                  <h5 className="modal-title">Return / Replace Item</h5>
                  <button
                    type="button"
                    className="close"
                    aria-label="Close"
                    onClick={() => { setRequestingItem(null); setReturnForm({ action: '', reason: '' }); }}
                  >
                    <span>&times;</span>
                  </button>
                </div>
                <div className="modal-body">
                  <div className="op-return-item-preview">
                    <img
                      src={productImage(requestingItem.cart?.product)}
                      alt={requestingItem.product_name}
                      className="op-return-item-img"
                    />
                    <div>
                      <div className="op-return-item-name">{requestingItem.product_name}</div>
                      <div className="op-return-item-price">{formatMoney(requestingItem.product_price)}</div>
                    </div>
                  </div>

                  <div className="form-group" style={{ marginTop: 16 }}>
                    <label htmlFor="return-action" style={{ fontWeight: 600, marginBottom: 6 }}>
                      What would you like to do?
                    </label>
                    <div className="op-return-choices">
                      {['Return', 'Replace'].map((choice) => (
                        <label key={choice} className={`op-return-choice${returnForm.action === choice ? ' op-return-choice-active' : ''}`}>
                          <input
                            type="radio"
                            name="action"
                            value={choice}
                            checked={returnForm.action === choice}
                            onChange={() => setReturnForm((p) => ({ ...p, action: choice }))}
                            style={{ marginRight: 6 }}
                          />
                          {choice === 'Return' ? '↩ Return & Refund' : '🔄 Replace Item'}
                        </label>
                      ))}
                    </div>
                  </div>

                  <div className="form-group" style={{ marginTop: 12 }}>
                    <label htmlFor="return-reason" style={{ fontWeight: 600, marginBottom: 6 }}>
                      Reason <span style={{ color: '#dc3545' }}>*</span>
                    </label>
                    <textarea
                      id="return-reason"
                      className="form-control"
                      rows={3}
                      placeholder="e.g. Damaged product, wrong item received, not as described…"
                      value={returnForm.reason}
                      onChange={(e) => setReturnForm((p) => ({ ...p, reason: e.target.value }))}
                    />
                  </div>
                </div>
                <div className="modal-footer">
                  <button
                    type="button"
                    className="btn btn-default"
                    onClick={() => { setRequestingItem(null); setReturnForm({ action: '', reason: '' }); }}
                  >
                    Cancel
                  </button>
                  <button type="submit" className="btn btn-primary">
                    Submit Request
                  </button>
                </div>
              </form>
            </div>
          </div>
        </div>
      )}

      <BrandsCarousel />
    </>
  );
}
