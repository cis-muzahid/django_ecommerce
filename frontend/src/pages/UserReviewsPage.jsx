import { useEffect, useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import BrandsCarousel from '../components/BrandsCarousel';
import Breadcrumbs from '../components/Breadcrumbs';
import Rating from '../components/Rating';
import { useAuth } from '../context/AuthContext';
import apiClient from '../services/apiClient';
import { productHref, productImage } from '../utils/catalog';

export default function UserReviewsPage() {
  const navigate = useNavigate();
  const { isAuthenticated, loading: authLoading } = useAuth();
  const [reviews, setReviews] = useState([]);
  const [loading, setLoading] = useState(true);
  const [editingReview, setEditingReview] = useState(null);
  const [reviewForm, setReviewForm] = useState({ review: 0, title: '', comment: '' });
  const [saving, setSaving] = useState(false);

  useEffect(() => {
    if (authLoading) return;
    if (!isAuthenticated) {
      navigate('/login');
      return;
    }

    fetchReviews();
  }, [authLoading, isAuthenticated]);

  async function fetchReviews() {
    try {
      setLoading(true);
      const response = await apiClient.get('/reviews/my/');
      setReviews(response.data.results || response.data || []);
    } catch (error) {
      console.error('Failed to fetch reviews:', error);
    } finally {
      setLoading(false);
    }
  }

  function openEditModal(review) {
    setEditingReview(review);
    setReviewForm({
      review: review.review || 0,
      title: review.title || '',
      comment: review.comment || '',
    });
  }

  async function handleUpdateReview(event) {
    event.preventDefault();
    if (!editingReview?.product?.id) return;

    setSaving(true);
    try {
      await apiClient.put(
        `/products/${editingReview.product.id}/reviews/${editingReview.id}/`,
        reviewForm,
      );
      setEditingReview(null);
      await fetchReviews();
    } catch (error) {
      console.error('Failed to update review:', error);
      alert(error.response?.data?.error || 'Failed to update review');
    } finally {
      setSaving(false);
    }
  }

  async function handleDeleteReview(review) {
    if (!confirm('Delete this review?') || !review.product?.id) return;

    try {
      await apiClient.delete(`/products/${review.product.id}/reviews/${review.id}/`);
      await fetchReviews();
    } catch (error) {
      console.error('Failed to delete review:', error);
      alert(error.response?.data?.error || 'Failed to delete review');
    }
  }

  if (authLoading || loading) {
    return <p className="text-center" style={{ padding: '50px' }}>Loading reviews...</p>;
  }

  return (
    <>
      <Breadcrumbs items={[{ label: 'Your Reviews' }]} />

      <div className="row">
        <div className="shopping-cart user-reviews-page">
          <div className="shopping-cart-table">
            <div className="table-responsive">
              <table className="table">
                <thead>
                  <tr>
                    <th className="cart-description item">Image</th>
                    <th className="cart-product-name item text-left">Product Name</th>
                    <th className="cart-edit item">Edit</th>
                    <th className="cart-review item">Review</th>
                    <th className="cart-romove item">Remove</th>
                  </tr>
                </thead>
                <tbody>
                  {reviews.length ? (
                    reviews.map((item) => (
                      <tr key={item.id}>
                        <td className="cart-image">
                          <Link className="entry-thumbnail" to={productHref(item.product)}>
                            <img src={productImage(item.product)} alt={item.product?.name || ''} />
                          </Link>
                        </td>
                        <td className="cart-product-name-info text-center">
                          <h4 className="cart-product-description">
                            <Link to={productHref(item.product)}>{item.product?.name}</Link>
                          </h4>
                          <Rating value={item.review} />
                          <div className="reviews">({item.product?.review_count || 0} Reviews)</div>
                          <div className="cart-product-info">
                            <span className="product-color">COLOR:<span>Blue</span></span>
                          </div>
                        </td>
                        <td className="cart-product-edit">
                          <button type="button" className="btn-link" onClick={() => openEditModal(item)}>
                            Update Review
                          </button>
                        </td>
                        <td className="cart-product-sub-total">
                          <h4 className="cart-sub-total-price">{item.title}</h4>
                          <p className="review-title">{item.comment}</p>
                        </td>
                        <td className="romove-item">
                          <button
                            type="button"
                            data-toggle="tooltip"
                            className="btn-upper btn btn-link"
                            onClick={() => handleDeleteReview(item)}
                          >
                            <i className="fa fa-trash-o"></i>
                          </button>
                        </td>
                      </tr>
                    ))
                  ) : (
                    <tr>
                      <td colSpan="5" className="text-center" style={{ padding: '50px' }}>
                        No Data Found
                      </td>
                    </tr>
                  )}
                </tbody>
              </table>
            </div>
          </div>
        </div>
      </div>

      {editingReview && (
        <div className="modal fade show review-edit-modal" role="dialog">
          <div className="modal-dialog" role="document">
            <div className="modal-content">
              <form onSubmit={handleUpdateReview}>
                <div className="modal-header text-center">
                  <h3 className="modal-title">Update your review</h3>
                </div>
                <div className="modal-body">
                  <div className="form-group text-center">
                    <h4 className="form-label">How much you like this product</h4>
                    <div className="star-rating">
                      {[1, 2, 3, 4, 5].map((star) => (
                        <button
                          type="button"
                          className={star <= reviewForm.review ? 'selected' : ''}
                          key={star}
                          onClick={() => setReviewForm((prev) => ({ ...prev, review: star }))}
                        >
                          ★
                        </button>
                      ))}
                    </div>
                  </div>
                  <div className="form-group row">
                    <label className="col-sm-2 col-form-label" htmlFor="review-title">Title :</label>
                    <div className="col-sm-10">
                      <input
                        id="review-title"
                        type="text"
                        className="form-control"
                        value={reviewForm.title}
                        onChange={(event) => setReviewForm((prev) => ({ ...prev, title: event.target.value }))}
                      />
                    </div>
                  </div>
                  <div className="form-group row">
                    <label className="col-sm-2 col-form-label" htmlFor="review-comment">Comment :</label>
                    <div className="col-sm-10">
                      <input
                        id="review-comment"
                        type="text"
                        className="form-control"
                        value={reviewForm.comment}
                        onChange={(event) => setReviewForm((prev) => ({ ...prev, comment: event.target.value }))}
                      />
                    </div>
                  </div>
                </div>
                <div className="modal-footer">
                  <button type="button" className="btn btn-secondary" onClick={() => setEditingReview(null)}>
                    Close
                  </button>
                  <button type="submit" className="btn btn-info" disabled={saving}>
                    {saving ? 'Updating...' : 'Update Review'}
                  </button>
                </div>
              </form>
            </div>
          </div>
        </div>
      )}

      {editingReview ? <div className="modal-backdrop fade in"></div> : null}

      <BrandsCarousel />
    </>
  );
}
