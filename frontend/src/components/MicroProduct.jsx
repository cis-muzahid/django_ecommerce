import Rating from './Rating.jsx';
import { money, productHref, productImage } from '../utils/catalog.js';

export default function MicroProduct({ product }) {
  return (
    <div className="product">
      <div className="product-micro">
        <div className="row product-micro-row">
          <div className="col col-xs-5">
            <div className="product-image">
              <div className="image">
                <a href={productHref(product)}>
                  <img src={productImage(product)} alt="" />
                </a>
              </div>
            </div>
          </div>
          <div className="col col-xs-7">
            <div className="product-info">
              <h3 className="name">
                <a href={productHref(product)}>{product.name}</a>
              </h3>
              <Rating value={product.average_rating} />
              <div className="product-price">
                <span className="price">{money(product.price)}</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
