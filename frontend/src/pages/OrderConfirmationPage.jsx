import { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { Link } from 'react-router-dom';
import BrandsCarousel from '../components/BrandsCarousel';
import Breadcrumbs from '../components/Breadcrumbs';
import { useAuth } from '../context/AuthContext';
import apiClient from '../services/apiClient';
import * as orderService from '../services/orderService';
import { productHref } from '../utils/catalog';

export default function OrderConfirmationPage() {
  const { orderId } = useParams();
  const navigate = useNavigate();
  const { isAuthenticated, loading: authLoading } = useAuth();
  const [order, setOrder] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    if (authLoading) {
      return;
    }
    if (!isAuthenticated) {
      navigate('/login');
      return;
    }

    if (!orderId) {
      setError('Order ID not provided');
      setLoading(false);
      return;
    }

    fetchOrderDetails();
  }, [authLoading, isAuthenticated, orderId]);

  const fetchOrderDetails = async () => {
    try {
      setLoading(true);
      const response = await orderService.getOrder(orderId);
      setOrder(response);
    } catch (error) {
      console.error('Failed to fetch order:', error);
      setError('Failed to load order details');
    } finally {
      setLoading(false);
    }
  };

  const formatDate = (dateString) => {
    const options = { year: 'numeric', month: 'long', day: 'numeric' };
    return new Date(dateString).toLocaleDateString(undefined, options);
  };

  const getStatusBadge = (status) => {
    const statusColors = {
      pending: 'warning',
      processing: 'info',
      shipped: 'primary',
      delivered: 'success',
      cancelled: 'danger'
    };
    return statusColors[status] || 'secondary';
  };

  if (authLoading || loading) {
    return (
      <>
        <Breadcrumbs items={[{ label: 'Order Confirmation' }]} />
        <div className="container">
          <p className="text-center" style={{ padding: '50px' }}>Loading order details...</p>
        </div>
      </>
    );
  }

  if (error || !order) {
    return (
      <>
        <Breadcrumbs items={[{ label: 'Order Confirmation' }]} />
        <div className="container">
          <div className="alert alert-danger">{error || 'Order not found'}</div>
          <Link to="/" className="btn btn-primary">Back to Home</Link>
        </div>
      </>
    );
  }

  return (
    <>
      <Breadcrumbs items={[{ label: 'Order Confirmation' }]} />

      <div className="container">
        {/* Success Message */}
        <div className="row">
          <div className="col-md-12">
            <div className="alert alert-success" role="alert">
              <h4 className="alert-heading">
                <i className="fa fa-check-circle"></i> Thank You for Your Order!
              </h4>
              <p>
                Your order has been confirmed and will be processed shortly. You can track your order
                status below.
              </p>
            </div>
          </div>
        </div>

        {/* Order Confirmation Details */}
        <div className="row">
          <div className="col-md-8">
            {/* Order Information */}
            <div className="panel panel-default">
              <div className="panel-heading">
                <h4 className="panel-title">Order Information</h4>
              </div>
              <div className="panel-body">
                <div className="row">
                  <div className="col-md-6">
                    <div className="form-group">
                      <label className="info-title">Order Number</label>
                      <p className="form-control" style={{ border: 'none', background: '#f9f9f9' }}>
                        #{order.id}
                      </p>
                    </div>
                  </div>
                  <div className="col-md-6">
                    <div className="form-group">
                      <label className="info-title">Order Date</label>
                      <p className="form-control" style={{ border: 'none', background: '#f9f9f9' }}>
                        {formatDate(order.created_at)}
                      </p>
                    </div>
                  </div>
                </div>
                <div className="row">
                  <div className="col-md-6">
                    <div className="form-group">
                      <label className="info-title">Order Status</label>
                      <p>
                        <span className={`badge badge-${getStatusBadge(order.status)}`}>
                          {(order.status || 'initial').charAt(0).toUpperCase() + (order.status || 'initial').slice(1)}
                        </span>
                      </p>
                    </div>
                  </div>
                  <div className="col-md-6">
                    <div className="form-group">
                      <label className="info-title">Payment Status</label>
                      <p>
                        <span className={`badge badge-${getStatusBadge(order.payment_status)}`}>
                          {(order.payment_status || 'pending').charAt(0).toUpperCase() + (order.payment_status || 'pending').slice(1)}
                        </span>
                      </p>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            {/* Shipping Address */}
            <div className="panel panel-default">
              <div className="panel-heading">
                <h4 className="panel-title">Shipping Address</h4>
              </div>
              <div className="panel-body">
                {order.address ? (
                  <address>{order.address}</address>
                ) : (
                  <p>No shipping address provided</p>
                )}
              </div>
            </div>

            {/* Order Items */}
            <div className="panel panel-default">
              <div className="panel-heading">
                <h4 className="panel-title">Order Items</h4>
              </div>
              <div className="panel-body">
                <div className="table-responsive">
                  <table className="table table-striped">
                    <thead>
                      <tr>
                        <th>Product</th>
                        <th>Quantity</th>
                        <th>Price</th>
                        <th>Total</th>
                      </tr>
                    </thead>
                    <tbody>
                      {order.order_items && order.order_items.length > 0 ? (
                        order.order_items.map(item => (
                          <tr key={item.id}>
                            <td>
                              {item.cart?.product ? (
                                <Link to={productHref(item.cart.product)}>
                                  {item.product_name || item.cart.product.name}
                                </Link>
                              ) : (
                                item.product_name || 'Product'
                              )}
                            </td>
                            <td>{item.cart?.quantity || 1}</td>
                            <td>${Number(item.product_price || 0).toFixed(2)}</td>
                            <td>${Number(item.total_price || 0).toFixed(2)}</td>
                          </tr>
                        ))
                      ) : (
                        <tr>
                          <td colSpan="4" className="text-center">
                            No items in this order
                          </td>
                        </tr>
                      )}
                    </tbody>
                  </table>
                </div>
              </div>
            </div>
          </div>

          {/* Order Summary Sidebar */}
          <div className="col-md-4">
            <div className="panel panel-default">
              <div className="panel-heading">
                <h4 className="panel-title">Order Summary</h4>
              </div>
              <div className="panel-body">
                <div className="summary-item">
                  <label>Subtotal:</label>
                  <span className="price">${Number(order.total_amount || 0).toFixed(2)}</span>
                </div>
                <div className="summary-item">
                  <label>Shipping:</label>
                  <span className="price">$0.00</span>
                </div>
                <div className="summary-item">
                  <label>Tax:</label>
                  <span className="price">$0.00</span>
                </div>
                {order.discount_amount && order.discount_amount > 0 && (
                  <div className="summary-item">
                    <label>Discount:</label>
                    <span className="price">-${order.discount_amount.toFixed(2)}</span>
                  </div>
                )}
                <hr />
                <div className="summary-item total">
                  <label>Total:</label>
                  <span className="price">${Number(order.total_amount || 0).toFixed(2)}</span>
                </div>
              </div>
            </div>

            {/* Next Steps */}
            <div className="panel panel-default">
              <div className="panel-heading">
                <h4 className="panel-title">What's Next?</h4>
              </div>
              <div className="panel-body">
                <ol>
                  <li>We'll process your order within 24 hours</li>
                  <li>You'll receive a confirmation email</li>
                  <li>Track your order status anytime from your dashboard</li>
                  <li>Your order will be shipped soon!</li>
                </ol>
              </div>
            </div>

            {/* Action Buttons */}
            <div style={{ marginTop: '20px' }}>
              <Link to="/orders" className="btn btn-primary btn-block">
                View All Orders
              </Link>
              <Link
                to={`/orders/tracking?order_id=${orderId}`}
                className="btn btn-info btn-block"
                style={{ marginTop: '10px' }}
              >
                Track This Order
              </Link>
              <Link to="/" className="btn btn-default btn-block" style={{ marginTop: '10px' }}>
                Continue Shopping
              </Link>
            </div>
          </div>
        </div>

        {/* Brands Carousel */}
        <BrandsCarousel />
      </div>
    </>
  );
}
