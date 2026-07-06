import { Link } from 'react-router-dom';
import Breadcrumbs from '../components/Breadcrumbs';

export default function NotFoundPage() {
  return (
    <>
      <Breadcrumbs items={[{ label: 'Page Not Found' }]} />
      <div className="row">
        <div className="col-md-8 col-md-offset-2 text-center" style={{ padding: '60px 20px' }}>
          <h1 style={{ fontSize: '72px', fontWeight: 700, marginBottom: '10px' }}>404</h1>
          <h2 style={{ marginBottom: '15px' }}>Page not found</h2>
          <p className="text-muted" style={{ marginBottom: '30px' }}>
            The page you are looking for may have moved or is no longer available.
          </p>
          <Link to="/" className="btn btn-primary">
            <i className="fa fa-home"></i> Back to Home
          </Link>
          <Link to="/products" className="btn btn-default" style={{ marginLeft: '10px' }}>
            Browse Products
          </Link>
        </div>
      </div>
    </>
  );
}
