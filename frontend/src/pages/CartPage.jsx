import { useEffect, useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import BrandsCarousel from '../components/BrandsCarousel';
import { useAuth } from '../context/AuthContext';
import { useCart } from '../context/CartContext';
import Breadcrumbs from '../components/Breadcrumbs';
import { productHref, productImage } from '../utils/catalog';
import Rating from '../components/Rating';

export default function CartPage() {
  const navigate = useNavigate();
  const { isAuthenticated, loading: authLoading } = useAuth();
  const { cartItems, removeFromCart, updateCartQuantity, refreshCart } = useCart();
  const [updatingItemId, setUpdatingItemId] = useState(null);
  useEffect(() => {
    if (authLoading) {
      return;
    }
    if (!isAuthenticated) {
      navigate('/login');
      return;
    }
    refreshCart();
  }, [authLoading, isAuthenticated]);

  const handleRemove = async (cartItemId) => {
    if (confirm('Are you sure you want to remove this item?')) {
      await removeFromCart(cartItemId);
    }
  };

  const handleQuantityChange = async (item, quantity) => {
    const nextQuantity = Math.max(1, Number(quantity) || 1);
    setUpdatingItemId(item.id);
    await updateCartQuantity(item.id, nextQuantity);
    setUpdatingItemId(null);
  };

  const calculateSubtotal = () => {
    return cartItems.reduce((sum, item) => sum + (item.product?.price || 0) * item.quantity, 0);
  };

  const calculateTotal = () => {
    return calculateSubtotal(); // Add tax/shipping if needed
  };

  return (
    <>
      <Breadcrumbs items={[{ label: 'Shopping Cart' }]} />

      <div className="row">
            <div className="shopping-cart">
              <div className="shopping-cart-table">
                {cartItems.length > 0 ? (
                  <div className="table-responsive">
                    <table className="table">
                      <thead>
                        <tr>
                          <th className="cart-description item">Image</th>
                          <th className="cart-product-name item">Product Name</th>
                          <th className="cart-edit item">Edit</th>
                          <th className="cart-qty item">Quantity</th>
                          <th className="cart-sub-total item">Subtotal</th>
                          <th className="cart-total last-item">Grandtotal</th>
                          <th className="cart-romove item">Remove</th>
                        </tr>
                      </thead>
                      <tbody>
                        {cartItems.map((item) => (
                          <tr key={item.id}>
                            <td className="cart-image">
                              <Link className="entry-thumbnail" to={productHref(item.product)}>
                                <img src={productImage(item.product) || '/assets/images/products/p1.jpg'} alt={item.product?.name} />
                              </Link>
                            </td>
                            <td className="cart-product-name-info">
                              <h4 className='cart-product-description'>
                                <Link to={productHref(item.product)}>{item.product?.name}</Link>
                              </h4>
                              <div className="row">
                                <div className="col-sm-12">
                                  <div className="">
                                    {/* Rating stars would go here */}
                                  </div>
                                </div>
                                <div className="col-sm-12">
                                  <div className="reviews">({item.product?.review_count || 0} Reviews)</div>
                                </div>
                              </div>
                              <div className="cart-product-info">
                                <span className="product-color">COLOR:<span>Blue</span></span>
                              </div>
                            </td>
                            <td className="cart-product-edit">
                              <Link to={productHref(item.product)} className="product-edit">Edit</Link>
                            </td>
                            <td className="cart-product-quantity">
                              <div className="cart-quantity">
                                <div className="quant-input" style={{ display: 'inline-block' }}>
                                  <div className="arrows">
                                    <button
                                      type="button"
                                      className="arrow plus gradient"
                                      onClick={() => handleQuantityChange(item, item.quantity + 1)}
                                      disabled={updatingItemId === item.id}
                                      aria-label="Increase quantity"
                                    >
                                      <span className="ir"><i className="icon fa fa-sort-asc"></i></span>
                                    </button>
                                    <button
                                      type="button"
                                      className="arrow minus gradient"
                                      onClick={() => handleQuantityChange(item, item.quantity - 1)}
                                      disabled={updatingItemId === item.id || item.quantity <= 1}
                                      aria-label="Decrease quantity"
                                    >
                                      <span className="ir"><i className="icon fa fa-sort-desc"></i></span>
                                    </button>
                                  </div>
                                  <input
                                    type="number"
                                    min="1"
                                    value={item.quantity}
                                    onChange={(e) => handleQuantityChange(item, e.target.value)}
                                    disabled={updatingItemId === item.id}
                                    aria-label={`${item.product?.name || 'Product'} quantity`}
                                  />
                                </div>
                              </div>
                            </td>
                            <td className="cart-product-sub-total">
                              <span className="cart-sub-total-price">${item.product?.price}</span>
                            </td>
                            <td className="cart-product-grand-total">
                              <span className="cart-grand-total-price">${((item.product?.price || 0) * item.quantity).toFixed(2)}</span>
                            </td>
                            <td className="romove-item">
                              <button onClick={() => handleRemove(item.id)} className="btn btn-link" title="Remove">
                                <i className="fa fa-trash-o"></i>
                              </button>
                            </td>
                          </tr>
                        ))}
                      </tbody>
                      <tfoot>
                        <tr>
                          <td colSpan="6">
                            <div className="shopping-cart-btn">
                              <span>
                                <Link to="/" className="btn btn-upper btn-primary outer-left-xs">Continue Shopping</Link>
                              </span>
                            </div>
                          </td>
                        </tr>
                      </tfoot>
                    </table>
                  </div>
                ) : (
                  <div className="text-center" style={{ padding: '50px' }}>
                    <h3>Your cart is empty</h3>
                    <Link to="/" className="btn btn-primary">Continue Shopping</Link>
                  </div>
                )}
              </div>

              {cartItems.length > 0 && (
                <div className="cart-shopping-total">
                  <table className="table">
                    <thead>
                      <tr>
                        <th>
                          <div className="cart-sub-total">
                            Subtotal<span className="inner-left-md">${calculateSubtotal().toFixed(2)}</span>
                          </div>
                          <div className="cart-grand-total">
                            Grand Total<span className="inner-left-md">${calculateTotal().toFixed(2)}</span>
                          </div>
                        </th>
                      </tr>
                    </thead>
                    <tbody>
                      <tr>
                        <td>
                          <div className="cart-checkout-btn pull-right">
                            <Link to='/checkout' className="btn btn-primary checkout-btn">PROCEED TO CHECKOUT</Link>
                          </div>
                        </td>
                      </tr>
                    </tbody>
                  </table>
                </div>
              )}
            </div>
          </div>

      <BrandsCarousel />
    </>
  );
}
