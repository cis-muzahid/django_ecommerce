import { Link } from 'react-router-dom';
import { useAuth } from '../../context/AuthContext';

export default function SupplierHeader() {
  const { user, logout } = useAuth();

  return (
    <header className="header-style-1">
      {/* Top Bar */}
      <div className="top-bar animate-dropdown">
        <div className="container">
          <div className="header-top-inner">
            <div className="cnt-account">
              <ul className="list-unstyled">
                <li><Link to="/supplier"><i className="icon fa fa-user"></i>Home</Link></li>
                <li><Link to="/"><i className="icon fa fa-home"></i>My Site</Link></li>
                <li><a href="#" onClick={(e) => { e.preventDefault(); logout(); }}><i className="icon fa fa-sign-out"></i>Logout</a></li>
              </ul>
            </div>
            <div className="cnt-block">
              <ul className="list-unstyled list-inline">
                <li className="dropdown dropdown-small">
                  <a href="#" className="dropdown-toggle" data-hover="dropdown" data-toggle="dropdown">
                    <span className="value">{user?.email || 'Supplier'}</span>
                  </a>
                </li>
              </ul>
            </div>
            <div className="clearfix"></div>
          </div>
        </div>
      </div>

      {/* Main Header */}
      <div className="main-header">
        <div className="container">
          <div className="row">
            <div className="col-xs-12 col-sm-12 col-md-3 logo-holder">
              <div className="logo">
                <Link to="/supplier">
                  <img src="/assets/images/logo.png" alt="Marazzo" />
                </Link>
              </div>
            </div>
            <div className="col-xs-12 col-sm-12 col-md-7 top-search-holder">
              <div className="search-area">
                <form>
                  <div className="control-group">
                    <input className="search-field" placeholder="Search here..." />
                    <button className="search-button" type="submit"></button>
                  </div>
                </form>
              </div>
            </div>
            <div className="col-xs-12 col-sm-12 col-md-2 animate-dropdown top-cart-row">
              <div className="dropdown dropdown-cart">
                <Link to="/supplier" className="lnk-cart">
                  <div className="items-cart-inner">
                    <div className="basket">
                      <i className="glyphicon glyphicon-user"></i>
                    </div>
                    <div className="basket-item-count">
                      <span className="count">{user?.email?.substring(0, 10) || 'Supplier'}</span>
                    </div>
                  </div>
                </Link>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Navigation */}
      <div className="header-nav animate-dropdown">
        <div className="container">
          <div className="yamm navbar navbar-default" role="navigation">
            <div className="navbar-header">
              <button data-target="#mc-horizontal-menu-collapse" data-toggle="collapse" className="navbar-toggle collapsed" type="button">
                <span className="sr-only">Toggle navigation</span>
                <span className="icon-bar"></span>
                <span className="icon-bar"></span>
                <span className="icon-bar"></span>
              </button>
            </div>
            <div className="nav-bg-class">
              <div className="navbar-collapse collapse" id="mc-horizontal-menu-collapse">
                <div className="nav-outer">
                  <ul className="nav navbar-nav">
                    <li className="active">
                      <Link to="/supplier">Home</Link>
                    </li>
                    <li>
                      <Link to="/supplier/products">My Site</Link>
                    </li>
                    <li>
                      <a href="#" onClick={(e) => { e.preventDefault(); logout(); }}>Logout</a>
                    </li>
                  </ul>
                  <div className="clearfix"></div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </header>
  );
}
