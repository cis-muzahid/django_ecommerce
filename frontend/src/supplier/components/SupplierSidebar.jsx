import { Link, useLocation } from 'react-router-dom';

export default function SupplierSidebar() {
  const location = useLocation();

  const isActive = (path) => {
    return location.pathname.startsWith(path) ? 'active' : '';
  };

  return (
    <div className="side-menu animate-dropdown outer-bottom-xs">
      <div className="head">
        <i className="icon fa fa-align-justify fa-fw"></i> Supplier Panel
      </div>
      <nav className="yamm megamenu-horizontal">
        <ul className="nav">
          <li className={isActive('/supplier/products')}>
            <Link to="/supplier/products">
              <i className="icon fa fa-shopping-bag"></i> Products Management
            </Link>
          </li>
          <li className={isActive('/supplier/orders')}>
            <Link to="/supplier/orders">
              <i className="icon fa fa-shopping-cart"></i> Orders Management
            </Link>
          </li>
          <li className={isActive('/supplier/returns')}>
            <Link to="/supplier/returns">
              <i className="icon fa fa-undo"></i> Returns &amp; Replacements
            </Link>
          </li>
          <li className={isActive('/supplier/banners')}>
            <Link to="/supplier/banners">
              <i className="icon fa fa-image"></i> Banners Management
            </Link>
          </li>
          <li className={isActive('/supplier/blogs')}>
            <Link to="/supplier/blogs">
              <i className="icon fa fa-pencil"></i> Blog Management
            </Link>
          </li>
        </ul>
      </nav>
    </div>
  );
}
