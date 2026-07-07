import { Link } from 'react-router-dom';
import Rating from './Rating.jsx';
import { money, productHref, productImage } from '../utils/catalog.js';

export default function ProductCard({
  product,
  isAuthenticated = false,
  onAddCart = () => {},
  onAddWishlist = () => {},
  showCompare = true,
}) {
  const href = productHref(product);
  const image = productImage(product);

  return (
    <div className="item item-carousel">
      <div className="products">
        <div className="product">
          <div className="product-image">
            <div className="image">
              <Link to={href}>
                <img src={image} alt="" />
                <img src={image} alt="" className="hover-image" />
              </Link>
            </div>
            {/* /.image */}
            
            {product.tag ? (
              <div className={`tag ${String(product.tag).toLowerCase()}`}>
                <span>{product.tag}</span>
              </div>
            ) : null}
          </div>
          {/* /.product-image */}

          <div className="product-info text-left">
            <h3 className="name">
              <Link to={href}>{product.name}</Link>
            </h3>
            <Rating value={product.average_rating} />
            <div className="description"></div>
            <div className="product-price">
              <span className="price">{money(product.price)}</span>
              <span className="price-before-discount">$ 800</span>
            </div>
            {/* /.product-price */}
          </div>
          {/* /.product-info */}

          {isAuthenticated ? (
            <div className="cart clearfix animate-effect">
              <div className="action">
                <ul className="list-unstyled">
                  <li className="add-cart-button btn-group">
                    <button
                      type="button"
                      data-toggle="tooltip"
                      className="btn btn-primary icon"
                      title="Add Cart"
                      onClick={() => onAddCart(product.id)}
                    >
                      <i className="fa fa-shopping-cart"></i>
                    </button>
                    <button 
                      className="btn btn-primary cart-btn" 
                      type="button" 
                      onClick={() => onAddCart(product.id)}
                    >
                      Add to cart
                    </button>
                  </li>
                  <li className="lnk wishlist">
                    <button
                      type="button"
                      data-toggle="tooltip"
                      className="add-to-cart wishlist_css"
                      title="Wishlist"
                      onClick={() => onAddWishlist(product.id)}
                    >
                      <i className="icon fa fa-heart"></i>
                    </button>
                  </li>
                  {showCompare ? (
                    <li className="lnk">
                      <Link className="add-to-cart" to={href} title="Compare">
                        <i className="fa fa-signal" aria-hidden="true"></i>
                      </Link>
                    </li>
                  ) : null}
                </ul>
              </div>
              {/* /.action */}
            </div>
          ) : null}
          {/* /.cart */}
        </div>
        {/* /.product */}
      </div>
    </div>
  );
}
