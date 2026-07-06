import { Link, useNavigate } from 'react-router-dom';
import { useState } from 'react';
import { useCart } from '../context/CartContext';
import { useAuth } from '../context/AuthContext';
import { categoryNavPath } from '../utils/navigation';

export default function HeaderMain({ categories = [] }) {
  const navigate = useNavigate();
  const { isAuthenticated } = useAuth();
  const { cartCount, cartItems } = useCart();
  const [searchDropdownOpen, setSearchDropdownOpen] = useState(false);

  const cartTotal = cartItems.reduce((sum, item) => sum + (item.product?.price || 0) * item.quantity, 0);

  function handleSubmit(event) {
    event.preventDefault();
    const form = new FormData(event.currentTarget);
    const query = String(form.get('q') || '').trim();

    if (!query) {
      alert('Please enter a search item.');
      return;
    }

    navigate(`/search?q=${encodeURIComponent(query)}`);
  }

  function navigateTo(event, path) {
    event.preventDefault();
    navigate(path);
  }

  return (
    <div className="main-header">
      <div className="container">
        <div className="row">
          <div className="col-xs-12 col-sm-12 col-md-3 logo-holder">
            <div className="logo">
              <Link to="/"><img src="/assets/images/logo.png" alt="logo" /></Link>
            </div>
          </div>
          <div className="col-lg-7 col-md-6 col-sm-8 col-xs-12 top-search-holder">
            <div className="search-area">
              <form id="search-form" onSubmit={handleSubmit}>
                <div className="control-group" style={{ padding: 1 }}>
                  <ul className="categories-filter animate-dropdown">
                    <li
                      className={`dropdown ${searchDropdownOpen ? 'open' : ''}`}
                      onMouseEnter={() => setSearchDropdownOpen(true)}
                      onMouseLeave={() => setSearchDropdownOpen(false)}
                    >
                      <a
                        className="dropdown-toggle"
                        data-toggle="dropdown"
                        href="home/category.html"
                        onClick={(event) => {
                          event.preventDefault();
                          setSearchDropdownOpen((open) => !open);
                        }}
                        style={{ cursor: 'pointer' }}
                      >
                        Categories <b className="caret"></b>
                      </a>
                      <ul className="dropdown-menu" role="menu">
                        {categories.map((category) => (
                          <li role="presentation" key={category.id}>
                            <a 
                              role="menuitem" 
                              tabIndex="-1" 
                              href={categoryNavPath(category.name)}
                              onClick={(event) => navigateTo(event, categoryNavPath(category.name))}
                            >
                              - {String(category.name).charAt(0).toUpperCase() + String(category.name).slice(1)}
                            </a>
                          </li>
                        ))}
                      </ul>
                    </li>
                  </ul>
                  <input className="search-field" name="q" id="search-input" placeholder="Search here..." />
                  <button className="search-button" type="submit" style={{ padding: '18px 25px' }}></button>
                </div>
              </form>
            </div>
          </div>
          <div className="col-lg-2 col-md-3 col-sm-4 col-xs-12 animate-dropdown top-cart-row">
            <div className="dropdown dropdown-cart">
              <Link 
                id="my_cart_checkout" 
                to="/my_cart" 
                className="dropdown-toggle lnk-cart header_cart hidden-xs"
                data-toggle="dropdown"
                onClick={(event) => navigateTo(event, '/my_cart')}
              >
                <div className="items-cart-inner background-color-danger">
                  <div className="basket">
                    <div className="basket-item-count"><span className="count">{cartCount}</span></div>
                    <div className="total-price-basket">
                      <span className="lbl">Shopping Cart</span> <span className="value">{isAuthenticated ? `${cartTotal} INR` : '0 INR'}</span>
                    </div>
                  </div>
                </div>
              </Link>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
