import { useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import BrandsCarousel from '../components/BrandsCarousel';
import Breadcrumbs from '../components/Breadcrumbs';
import { useAuth } from '../context/AuthContext';
import { useCart } from '../context/CartContext';
import { productHref, productImage } from '../utils/catalog';

export default function WishlistPage() {
  const navigate = useNavigate();
  const { isAuthenticated, loading: authLoading } = useAuth();
  const { wishlistItems, removeFromWishlist, addToCart, refreshWishlist } = useCart();

  useEffect(() => {
    if (authLoading) {
      return;
    }
    if (!isAuthenticated) {
      navigate('/login');
      return;
    }
    refreshWishlist();
  }, [authLoading, isAuthenticated]);

  const handleRemove = async (wishlistItemId) => {
    await removeFromWishlist(wishlistItemId);
  };

  const handleAddToCart = async (productId) => {
    const result = await addToCart(productId, 1);
    if (result.success) {
      alert('Item added to cart!');
    }
  };

  const renderStars = (rating) => {
    const stars = [];
    for (let i = 0; i < 5; i++) {
      if (i < rating) {
        stars.push(
          <span key={i} className={`star_${rating}`}>
            ★
          </span>,
        );
      } else {
        stars.push(
          <span key={i} className="empty-star">
            ★
          </span>,
        );
      }
    }
    return stars;
  };

  return (
    <>
      <Breadcrumbs items={[{ label: 'Wishlist' }]} />

      <div className="my-wishlist-page">
        <div className="row">
          <div className="col-md-12 my-wishlist">
            {wishlistItems.length > 0 ? (
              <div className="table-responsive">
                <table className="table">
                  <thead>
                    <tr>
                      <th colSpan="4" className="heading-title">
                        My Wishlist
                      </th>
                    </tr>
                  </thead>
                  <tbody>
                    {wishlistItems.map((wishlist) => (
                      <tr key={wishlist.id}>
                        <td className="col-md-2 col-sm-6 col-xs-6">
                          <Link to={productHref(wishlist.product)}>
                            <img
                              src={productImage(wishlist.product) || '/assets/images/products/p1.jpg'}
                              alt={wishlist.product?.name || 'product'}
                            />
                          </Link>
                        </td>
                        <td className="col-md-7 col-sm-6 col-xs-6">
                          <div className="product-name">
                            <Link to={productHref(wishlist.product)}>{wishlist.product?.name}</Link>
                          </div>
                          <div className="p-0">{renderStars(wishlist.product?.rating || 0)}</div>
                          <span className="review">( {wishlist.product?.review_count || 0} Reviews )</span>
                          <div className="price">
                            ${wishlist.product?.price}
                            <span>
                              ${wishlist.product?.original_price || wishlist.product?.price}
                            </span>
                          </div>
                        </td>
                        <td className="col-md-2">
                          <button
                            type="button"
                            onClick={() => handleAddToCart(wishlist.product?.id)}
                            data-toggle="tooltip"
                            className="btn-upper btn btn-primary"
                            title="Add to cart"
                          >
                            Add to cart
                          </button>
                        </td>
                        <td className="col-md-1 close-btn wishlist-remove-action">
                          <button
                            type="button"
                            className="btn btn-danger wishlist-remove-button"
                            onClick={() => handleRemove(wishlist.id)}
                          >
                            Remove
                          </button>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            ) : (
              <section className="section new-arriavls">
                <h3 className="section-title">My Wishlist</h3>
                <div
                  style={{
                    display: 'flex',
                    justifyContent: 'center',
                    alignItems: 'center',
                    height: '230px',
                    backgroundColor: 'white',
                  }}
                >
                  <div className="inner-container">
                    <h3 className="text-center">No Data Found</h3>
                  </div>
                </div>
              </section>
            )}
          </div>
        </div>

        <BrandsCarousel />
      </div>
    </>
  );
}
