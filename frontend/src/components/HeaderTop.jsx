import { Link, useNavigate, useLocation } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { topNavLinkClass } from '../utils/navigation';

export default function HeaderTop() {
  const navigate = useNavigate();
  const location = useLocation();
  const { isAuthenticated, logout } = useAuth();
  const pathname = location.pathname;

  function handleLogout(e) {
    e.preventDefault();
    logout();
    navigate('/login');
  }

  return (
    <div className="top-bar animate-dropdown">
      <div className="container">
        <div className="header-top-inner">
          <div className="cnt-account">
            <ul className="list-unstyled">
              {isAuthenticated ? (
                <>
                  <li className="myaccount">
                    <Link to="/user_profile" className={topNavLinkClass(pathname, 'profile')}>
                      My Account
                    </Link>
                  </li>
                  <li className="wishlist">
                    <Link to="/my_wishlist" id="my_wishlist" className={topNavLinkClass(pathname, 'wishlist')}>
                      Wishlist
                    </Link>
                  </li>
                  <li className="header_cart hidden-xs">
                    <Link to="/my_cart" id="my_cart" className={topNavLinkClass(pathname, 'cart')}>
                      My Cart
                    </Link>
                  </li>
                  <li className="check">
                    <Link to="/orders" id="checkoutLink" className={topNavLinkClass(pathname, 'order')}>
                      My Orders
                    </Link>
                  </li>
                  <li className="logout">
                    <a href="#" onClick={handleLogout}>Logout</a>
                  </li>
                </>
              ) : (
                <>
                  <li className="login">
                    <Link to="/login_user" className={topNavLinkClass(pathname, 'login')}>
                      Login
                    </Link>
                  </li>
                  <li className="signup_user">
                    <Link to="/signup_user" className={topNavLinkClass(pathname, 'signup')}>
                      Sign up
                    </Link>
                  </li>
                </>
              )}
            </ul>
          </div>
          <div className="cnt-block">
            <ul className="list-unstyled list-inline">
              <li className="dropdown dropdown-small">
                <a href="#" className="dropdown-toggle" data-hover="dropdown" data-toggle="dropdown">
                  <span className="value">INR</span><b className="caret"></b>
                </a>
              </li>
              <li className="dropdown dropdown-small lang">
                <a href="#" className="dropdown-toggle" data-hover="dropdown" data-toggle="dropdown">
                  <span className="value">English</span><b className="caret"></b>
                </a>
              </li>
            </ul>
          </div>
          <div className="clearfix"></div>
        </div>
      </div>
    </div>
  );
}
