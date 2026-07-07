import { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { getOrders } from '../services/orderService';

const STATUS_BADGE = {
  initial: 'badge-secondary',
  in_process: 'badge-warning',
  deliverd: 'badge-success',
  delivered: 'badge-success',
  cancelled: 'badge-danger',
  return: 'badge-info',
  replace: 'badge-info',
};

export default function OrdersPage() {
  const [orders, setOrders] = useState([]);
  const [loading, setLoading] = useState(true);
  const [currentPage, setCurrentPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);

  useEffect(() => {
    fetchOrders();
  }, [currentPage]);

  const fetchOrders = async () => {
    try {
      setLoading(true);
      const data = await getOrders(currentPage);
      setOrders(data.results || data);
      if (data.count) {
        setTotalPages(Math.ceil(data.count / 10));
      } else {
        setTotalPages(data.total_pages || 1);
      }
    } catch (error) {
      console.error('Failed to fetch orders:', error);
    } finally {
      setLoading(false);
    }
  };

  const formatDate = (dateString) => {
    return new Date(dateString).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
    });
  };

  return (
    <div className="container">
      <div className="row categorie_main">
        <div className="col-12 card">
          <div className="card-header">
            <h3 className="card-title font-weight-bold mt-2">Orders</h3>
            <div className="d-grid gap-2 d-md-flex justify-content-md-end">
              <Link to="/supplier/returns" className="btn btn-info mr-2" type="button">
                <i className="fa fa-undo"></i> Returns &amp; Replacements
              </Link>
            </div>
          </div>

          <div className="card-body">
            {loading ? (
              <p style={{ margin: 'auto', textAlign: 'center' }}>
                <b>Loading...</b>
              </p>
            ) : orders.length > 0 ? (
              <table className="table table-striped table-hover">
                <thead>
                  <tr className="text-center">
                    <th scope="col">Order ID</th>
                    <th scope="col">Customer</th>
                    <th scope="col">Date</th>
                    <th scope="col">Total Amount</th>
                    <th scope="col">Payment Method</th>
                    <th scope="col">Payment Status</th>
                    <th scope="col">Status</th>
                    <th scope="col">Action</th>
                  </tr>
                </thead>
                <tbody>
                  {orders.map((order) => (
                    <tr key={order.id} className="text-center">
                      <td>#{order.id}</td>
                      <td>{order.user?.email || order.email || 'N/A'}</td>
                      <td>{formatDate(order.created_at)}</td>
                      <td>₹{parseFloat(order.total_amount || 0).toFixed(2)}</td>
                      <td>{order.payment_method || 'N/A'}</td>
                      <td>
                        <span className={`badge ${order.payment_status === 'paid' ? 'badge-success' : 'badge-warning'}`}>
                          {order.payment_status || 'pending'}
                        </span>
                      </td>
                      <td>
                        <span className={`badge ${STATUS_BADGE[order.status] || 'badge-secondary'}`}>
                          {order.status || 'initial'}
                        </span>
                      </td>
                      <td>
                        <div className="d-flex justify-content-center">
                          <span className="ml-2 mr-2">
                            <Link
                              to={`/supplier/orders/${order.id}`}
                              style={{ fontWeight: 100, color: 'black' }}
                              title="View Order"
                            >
                              <i className="fa fa-eye text-info"></i>
                            </Link>
                          </span>
                        </div>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            ) : (
              <p style={{ margin: 'auto', textAlign: 'center' }}>
                <b>No Data Found</b>
              </p>
            )}
          </div>

          <hr />

          <div className="card-footer clearfix bg-white justify-content-md-start">
            <ul className="pagination pagination-sm m-0 float-right">
              {currentPage > 1 && (
                <li className="page-item">
                  <a
                    className="page-link"
                    href="#"
                    onClick={(e) => {
                      e.preventDefault();
                      setCurrentPage(currentPage - 1);
                    }}
                  >
                    &laquo;
                  </a>
                </li>
              )}
              {[...Array(totalPages)].map((_, i) => (
                <li key={i + 1} className={`page-item ${currentPage === i + 1 ? 'active' : ''}`}>
                  <a
                    className="page-link"
                    href="#"
                    onClick={(e) => {
                      e.preventDefault();
                      setCurrentPage(i + 1);
                    }}
                  >
                    {i + 1}
                  </a>
                </li>
              ))}
              {currentPage < totalPages && (
                <li className="page-item">
                  <a
                    className="page-link"
                    href="#"
                    onClick={(e) => {
                      e.preventDefault();
                      setCurrentPage(currentPage + 1);
                    }}
                  >
                    &raquo;
                  </a>
                </li>
              )}
            </ul>
          </div>
        </div>
      </div>
    </div>
  );
}
