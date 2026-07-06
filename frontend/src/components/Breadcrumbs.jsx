import { Link } from 'react-router-dom';

export default function Breadcrumbs({ items = [] }) {
  return (
    <div className="breadcrumb">
      <div className="breadcrumb-inner">
        <ul className="list-inline list-unstyled">
          <li>
            <Link to="/">Home</Link>
          </li>
          {items.map((item, index) => (
            <li key={index} className={index === items.length - 1 ? 'active' : ''}>
              {item.link && index !== items.length - 1 ? (
                <Link to={item.link}>{item.label}</Link>
              ) : (
                <span>{item.label}</span>
              )}
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
}
