import { useEffect, useState } from 'react';
import { useParams, useNavigate, Link } from 'react-router-dom';
import { getOrder, updateOrderStatus } from '../services/orderService';

const STATUS_OPTIONS = [
  { value: 'in_process', label: 'In Process' },
  { value: 'deliverd', label: 'Delivered' },
  { value: 'cancelled', label: 'Cancelled' },
];

const STATUS_BADGE = {
  initial: 'badge-secondary',
  in_process: 'badge-warning',
  deliverd: 'badge-success',
  delivered: 'badge-success',
  cancelled: 'badge-danger',
  return: 'badge-info',
  replace: 'badge-info',
};

export default function OrderDetailPage() {
  const { id } = useParams();
  const navigate = useNavigate();

  const [order, setOrder] = useState(null);
  const [loading, setLoading] = useState(true);
  const [selectedStatus, setSelectedStatus] = useState('');
  const [statusUpdating, setStatusUpdating] = useState(false);
  const [successMsg, setSuccessMsg] = useState('');
  const [errorMsg, setErrorMsg] = useState('');

  useEffect(() => {
    fetchOrder();
  }, [id]);

  const fetchOrder = async () => {
    try {
      setLoading(true);
      const data = await getOrder(id);
      setOrder(data);
      setSelectedStatus(data.status || 'initial');
    } catch (error) {
      console.error('Failed to fetch order:', error);
      setErrorMsg('Failed to load order details.');
    } finally {
      setLoading(false);
    }
  };

  const handleStatusUpdate = async (e) => {
    e.preventDefault();
    if (!selectedStatus) return;
    setStatusUpdating(true);
    setSuccessMsg('');
    setErrorMsg('');
    try {
      await updateOrderStatus(id, selectedStatus);
      setSuccessMsg('Order status updated successfully.');
      setOrder((prev) => ({ ...prev, status: selectedStatus }));
    } catch (error) {
      console.error('Failed to update status:', error);
      const errData = error.response?.data;
      setErrorMsg(
        errData
          ? Object.values(errData).flat().join(', ')
          : 'Failed to update order status.'
      );
    } finally {
      setStatusUpdating(false);
    }
  };

  const formatDate = (dateString) => {
    if (!dateString) return 'N/A';
    return new Date(dateString).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit',
    });
  };

  if (loading) {
    return (
      <div className="container">
        <p style={{ margin: 'auto', textAlign: 'center' }}>
          <b>Loading...</b>
        </p>
      </div>
    );
  }

  if (!order) {
    return (
      <div className="container">
        <div className="alert alert-danger">Order not found.</div>
        <Link to="/supplier/orders" className="btn btn-secondary">
          &larr; Back to Orders
        </Link>
      </div>
    );
  }

  const items = order.items || order.order_items || [];
  const address = order.shipping_address || order.address || {};

  return (
    <div className="container">
      <div className="row categorie_main">
        <div className="col-12 card">
          <div className="card-header">
            <h3 className="card-title font-weight-bold mt-2">
              Order #{order.id}
            </h3>
            <div className="d-grid gap-2 d-md-flex justify-content-md-end">
              <Link to="/supplier/orders" className="btn btn-secondary">
                <i className="fa fa-arrow-left"></i> Back to Orders
              </Link>
            </div>
          </div>

          <div className="card-body">
            {successMsg && (
              <div className="alert alert-success alert-dismissible">
                <button type="button" className="close" onClick={() => setSuccessMsg('')}>
                  <span>&times;</span>
                </button>
                {successMsg}
              </div>
            )}
            {errorMsg && (
              <div className="alert alert-danger alert-dismissible">
                <button type="button" className="close" onClick={() => setErrorMsg('')}>
                  <span>&times;</span>
                </button>
                {errorMsg}
              </div>
            )}

            {/* Order Info */}
            <div className="row mb-4">
              <div className="col-md-6">
                <h5 className="font-weight-bold mb-3">Order Information</h5>
                <table className="table table-bordered table-sm">
                  <tbody>
                    <tr>
                      <th>Order ID</th>
                      <td>#{order.id}</td>
                    </tr>
                    <tr>
                      <th>Customer</th>
                      <td>{order.user?.email || order.email || 'N/A'}</td>
                    </tr>
                    <tr>
                      <th>Date</th>
                      <td>{formatDate(order.created_at)}</td>
                    </tr>
                    <tr>
                      <th>Total Amount</th>
                      <td>₹{parseFloat(order.total_amount || 0).toFixed(2)}</td>
                    </tr>
                    <tr>
                      <th>Payment Method</th>
                      <td>{order.payment_method || 'N/A'}</td>
                    </tr>
                    <tr>
                      <th>Payment Status</th>
                      <td>
                        <span className={`badge ${order.payment_status === 'paid' ? 'badge-success' : 'badge-warning'}`}>
                          {order.payment_status || 'pending'}
                        </span>
                      </td>
                    </tr>
                    <tr>
                      <th>Order Status</th>
                      <td>
                        <span className={`badge ${STATUS_BADGE[order.status] || 'badge-secondary'}`}>
                          {order.status || 'initial'}
                        </span>
                      </td>
                    </tr>
                  </tbody>
                </table>
              </div>

              <div className="col-md-6">
                <h5 className="font-weight-bold mb-3">Shipping Address</h5>
                <table className="table table-bordered table-sm">
                  <tbody>
                    <tr>
                      <th>Name</th>
                      <td>{address.full_name || address.name || order.user?.full_name || 'N/A'}</td>
                    </tr>
                    <tr>
                      <th>Phone</th>
                      <td>{address.phone || address.mobile || 'N/A'}</td>
                    </tr>
                    <tr>
                      <th>Address</th>
                      <td>{address.address || address.street || 'N/A'}</td>
                    </tr>
                    <tr>
                      <th>City</th>
                      <td>{address.city || 'N/A'}</td>
                    </tr>
                    <tr>
                      <th>State</th>
                      <td>{address.state || 'N/A'}</td>
                    </tr>
                    <tr>
                      <th>Pincode</th>
                      <td>{address.pincode || address.zip_code || 'N/A'}</td>
                    </tr>
                  </tbody>
                </table>
              </div>
            </div>

            {/* Order Items */}
            <h5 className="font-weight-bold mb-3">Order Items</h5>
            {items.length > 0 ? (
              <table className="table table-striped table-hover mb-4">
                <thead>
                  <tr className="text-center">
                    <th>Image</th>
                    <th>Product</th>
                    <th>Price</th>
                    <th>Quantity</th>
                    <th>Subtotal</th>
                  </tr>
                </thead>
                <tbody>
                  {items.map((item, idx) => (
                    <tr key={item.id || idx} className="text-center">
                      <td>
                        {(item.product?.image || item.image) ? (
                          <img
                            src={item.product?.image || item.image}
                            alt={item.product?.name || item.name}
                            style={{ width: '60px', height: '60px', objectFit: 'cover' }}
                          />
                        ) : (
                          <span className="text-muted">No image</span>
                        )}
                      </td>
                      <td>{item.product?.name || item.product_name || item.name || 'N/A'}</td>
                      <td>₹{parseFloat(item.price || 0).toFixed(2)}</td>
                      <td>{item.quantity}</td>
                      <td>₹{(parseFloat(item.price || 0) * parseInt(item.quantity || 1)).toFixed(2)}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            ) : (
              <p className="text-muted mb-4">No items found for this order.</p>
            )}

            {/* Status Update */}
            <h5 className="font-weight-bold mb-3">Update Order Status</h5>
            <form onSubmit={handleStatusUpdate}>
              <div className="form-group row">
                <label className="col-sm-4 col-form-label">New Status</label>
                <div className="col-sm-8">
                  <select
                    className="form-control"
                    value={selectedStatus}
                    onChange={(e) => setSelectedStatus(e.target.value)}
                    style={{ maxWidth: '300px' }}
                  >
                    <option value="" disabled>Select status...</option>
                    {STATUS_OPTIONS.map((opt) => (
                      <option key={opt.value} value={opt.value}>
                        {opt.label}
                      </option>
                    ))}
                  </select>
                </div>
              </div>
              <div className="form-group row">
                <div className="col-sm-8 offset-sm-4">
                  <button
                    type="submit"
                    className="btn btn-primary"
                    disabled={statusUpdating}
                  >
                    {statusUpdating ? 'Updating...' : 'Update Status'}
                  </button>
                </div>
              </div>
            </form>
          </div>
        </div>
      </div>
    </div>
  );
}
