import { useEffect, useState } from 'react';
import { getReturnRequests, approveReturnRequest } from '../services/orderService';

const FILTER_TABS = [
  { key: 'all', label: 'All' },
  { key: 'return', label: 'Return' },
  { key: 'replace', label: 'Replace' },
  { key: 'pending', label: 'Pending' },
  { key: 'approved', label: 'Approved' },
];

export default function ReturnsPage() {
  const [requests, setRequests] = useState([]);
  const [loading, setLoading] = useState(true);
  const [activeTab, setActiveTab] = useState('all');
  const [successMsg, setSuccessMsg] = useState('');
  const [errorMsg, setErrorMsg] = useState('');
  const [approvingId, setApprovingId] = useState(null);

  useEffect(() => {
    fetchRequests();
  }, []);

  const fetchRequests = async () => {
    try {
      setLoading(true);
      const data = await getReturnRequests();
      setRequests(data.results || data);
    } catch (error) {
      console.error('Failed to fetch return requests:', error);
      setErrorMsg('Failed to load return/replacement requests.');
    } finally {
      setLoading(false);
    }
  };

  const handleApprove = async (req) => {
    const actionLabel = req.action === 'return' ? 'return' : 'replacement';
    const note =
      req.action === 'return'
        ? 'Approving this return will trigger an automatic refund. Continue?'
        : 'Approve this replacement request?';
    if (!confirm(note)) return;

    setApprovingId(req.id);
    setSuccessMsg('');
    setErrorMsg('');
    try {
      await approveReturnRequest(req.id);
      setSuccessMsg(`${actionLabel.charAt(0).toUpperCase() + actionLabel.slice(1)} request #${req.id} approved successfully.`);
      fetchRequests();
    } catch (error) {
      console.error('Failed to approve request:', error);
      const errData = error.response?.data;
      setErrorMsg(
        errData
          ? Object.values(errData).flat().join(', ')
          : `Failed to approve ${actionLabel} request.`
      );
    } finally {
      setApprovingId(null);
    }
  };

  const formatDate = (dateString) => {
    if (!dateString) return 'N/A';
    return new Date(dateString).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
    });
  };

  const filteredRequests = requests.filter((req) => {
    if (activeTab === 'all') return true;
    if (activeTab === 'return') return req.action === 'return';
    if (activeTab === 'replace') return req.action === 'replace' || req.action === 'replacement';
    if (activeTab === 'pending')
      return req.status === 'pending' || (!req.is_approved && req.status !== 'approved');
    if (activeTab === 'approved')
      return req.is_approved || req.status === 'approved';
    return true;
  });

  return (
    <div className="container">
      <div className="row categorie_main">
        <div className="col-12 card">
          <div className="card-header">
            <h3 className="card-title font-weight-bold mt-2">Returns &amp; Replacements</h3>
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

            {/* Filter Tabs */}
            <ul className="nav nav-tabs mb-3">
              {FILTER_TABS.map((tab) => (
                <li className="nav-item" key={tab.key}>
                  <a
                    className={`nav-link ${activeTab === tab.key ? 'active' : ''}`}
                    href="#"
                    onClick={(e) => {
                      e.preventDefault();
                      setActiveTab(tab.key);
                    }}
                  >
                    {tab.label}
                    {tab.key !== 'all' && (
                      <span className="badge badge-secondary ml-1">
                        {requests.filter((r) => {
                          if (tab.key === 'return') return r.action === 'return';
                          if (tab.key === 'replace')
                            return r.action === 'replace' || r.action === 'replacement';
                          if (tab.key === 'pending')
                            return r.status === 'pending' || (!r.is_approved && r.status !== 'approved');
                          if (tab.key === 'approved')
                            return r.is_approved || r.status === 'approved';
                          return false;
                        }).length}
                      </span>
                    )}
                  </a>
                </li>
              ))}
            </ul>

            {loading ? (
              <p style={{ margin: 'auto', textAlign: 'center' }}>
                <b>Loading...</b>
              </p>
            ) : filteredRequests.length > 0 ? (
              <table className="table table-striped table-hover">
                <thead>
                  <tr className="text-center">
                    <th scope="col">#</th>
                    <th scope="col">Customer</th>
                    <th scope="col">Product</th>
                    <th scope="col">Action</th>
                    <th scope="col">Reason</th>
                    <th scope="col">Payment Method</th>
                    <th scope="col">Date</th>
                    <th scope="col">Status</th>
                    <th scope="col">Approve</th>
                  </tr>
                </thead>
                <tbody>
                  {filteredRequests.map((req, index) => {
                    const isApproved = req.is_approved || req.status === 'approved';
                    return (
                      <tr key={req.id} className="text-center">
                        <td>{index + 1}</td>
                        <td>
                          {req.order?.user?.email ||
                            req.user?.email ||
                            req.customer_email ||
                            'N/A'}
                        </td>
                        <td>
                          {req.product?.name ||
                            req.order_item?.product?.name ||
                            req.product_name ||
                            `Order #${req.order?.id || req.order_id || 'N/A'}`}
                        </td>
                        <td>
                          <span
                            className={`badge ${
                              req.action === 'return' ? 'badge-warning' : 'badge-info'
                            }`}
                          >
                            {req.action === 'return' ? 'Return' : 'Replace'}
                          </span>
                        </td>
                        <td style={{ maxWidth: '200px' }}>
                          <span title={req.reason || ''}>
                            {req.reason
                              ? req.reason.length > 60
                                ? req.reason.substring(0, 60) + '...'
                                : req.reason
                              : 'N/A'}
                          </span>
                        </td>
                        <td>
                          {req.order?.payment_method || req.payment_method || 'N/A'}
                        </td>
                        <td>{formatDate(req.created_at)}</td>
                        <td>
                          {isApproved ? (
                            <span className="badge badge-success">Approved</span>
                          ) : (
                            <span className="badge badge-secondary">Pending</span>
                          )}
                        </td>
                        <td>
                          {!isApproved ? (
                            <div>
                              <button
                                className="btn btn-sm btn-primary"
                                onClick={() => handleApprove(req)}
                                disabled={approvingId === req.id}
                              >
                                {approvingId === req.id ? 'Approving...' : 'Approve'}
                              </button>
                              {req.action === 'return' && (
                                <div className="mt-1">
                                  <small className="text-danger">
                                    <i className="fa fa-info-circle"></i> Approving will trigger automatic refund
                                  </small>
                                </div>
                              )}
                            </div>
                          ) : (
                            <span className="text-muted">—</span>
                          )}
                        </td>
                      </tr>
                    );
                  })}
                </tbody>
              </table>
            ) : (
              <p style={{ margin: 'auto', textAlign: 'center' }}>
                <b>No requests found</b>
              </p>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
