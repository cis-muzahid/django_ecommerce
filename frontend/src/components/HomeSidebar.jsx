import { Link } from 'react-router-dom';
import Sidebar from './Sidebar.jsx';
import MicroProduct from './MicroProduct.jsx';
import Rating from './Rating.jsx';
import { chunk, money, productHref, productImage } from '../utils/catalog.js';
import { categoryNavPath } from '../utils/navigation';

export default function HomeSidebar({ categories, hotDeals, specialOffers, isAuthenticated, onAddCart }) {
  const offerGroups = chunk(specialOffers, 3);
  const parentCategories = categories.filter((cat) => !cat.parent_category);

  return (
    <Sidebar categories={categories}>
      <div className="sidebar-widget hot-deals outer-bottom-xs">
        <h3 className="section-title">Hot deals</h3>
        <div className="owl-carousel sidebar-carousel custom-carousel owl-theme outer-top-ss">
          {hotDeals.length ? (
            hotDeals.map((product) => (
              <div className="item" key={product.id}>
                <div className="products">
                  <div className="hot-deal-wrapper">
                    <div className="image">
                      <Link to={productHref(product)}>
                        <img src={productImage(product)} alt="" />
                        <img src={productImage(product)} alt="" className="hover-image" />
                      </Link>
                    </div>
                    <div className="sale-offer-tag">
                      <span>
                        49%
                        <br />
                        off
                      </span>
                    </div>
                    <div className="timing-wrapper">
                      {[
                        ['120', 'DAYS'],
                        ['20', 'HRS'],
                        ['36', 'MINS'],
                        ['60', 'SEC'],
                      ].map(([key, value]) => (
                        <div className="box-wrapper" key={value}>
                          <div className="date box">
                            <span className="key">{key}</span>{' '}
                            <span className="value">{value}</span>
                          </div>
                        </div>
                      ))}
                    </div>
                  </div>
                  <div className="product-info text-left m-t-20">
                    <h3 className="name">
                      <Link to={productHref(product)}>{product.name}</Link>
                    </h3>
                    <Rating value={product.average_rating} />
                    <div className="product-price">
                      <span className="price">{money(product.price)}</span>
                      <span className="price-before-discount">$800.00</span>
                    </div>
                  </div>
                  {isAuthenticated ? (
                    <div className="cart clearfix animate-effect">
                      <div className="action">
                        <div className="add-cart-button btn-group">
                          <button
                            type="button"
                            data-toggle="tooltip"
                            className="btn btn-primary icon"
                            title="Add Cart"
                            onClick={() => onAddCart(product.id)}
                          >
                            <i className="fa fa-shopping-cart"></i> Add to cart
                          </button>
                        </div>
                      </div>
                    </div>
                  ) : null}
                </div>
              </div>
            ))
          ) : (
            <p className="text-center">No Data Found</p>
          )}
        </div>
      </div>

      {['Special Offer', 'Special Deals'].map((title) => (
        <div className="sidebar-widget outer-bottom-small" key={title}>
          <h3 className="section-title">{title}</h3>
          <div className="sidebar-widget-body outer-top-xs">
            <div className="owl-carousel sidebar-carousel special-offer custom-carousel owl-theme outer-top-xs">
              {offerGroups.length ? (
                offerGroups.map((group, index) => (
                  <div className="item" key={index}>
                    <div className="products special-product">
                      {group.map((product) => (
                        <MicroProduct product={product} key={product.id} />
                      ))}
                    </div>
                  </div>
                ))
              ) : (
                <p className="text-center">No Data Found</p>
              )}
            </div>
          </div>
        </div>
      ))}

      <div className="sidebar-widget product-tag">
        <h3 className="section-title">Product tags</h3>
        <div className="sidebar-widget-body outer-top-xs">
          <div className="tag-list">
            {parentCategories.length ? (
              parentCategories.map((category) => (
                <Link
                  className="item"
                  title={category.name}
                  to={categoryNavPath(category.name)}
                  key={category.id}
                >
                  {category.name}
                </Link>
              ))
            ) : (
              <p className="text-center">No Data Found</p>
            )}
          </div>
        </div>
      </div>

      {!isAuthenticated && (
        <div className="sidebar-widget newsletter outer-bottom-small">
          <h3 className="section-title">Newsletters</h3>
          <div className="sidebar-widget-body outer-top-xs">
            <p>Sign Up for Our Newsletter!</p>
            <form>
              <div className="form-group">
                <label className="sr-only" htmlFor="homeNewsletterEmail">
                  Email address
                </label>
                <input
                  type="email"
                  className="form-control"
                  id="homeNewsletterEmail"
                  placeholder="Subscribe to our newsletter"
                />
              </div>
              <button type="button" className="btn btn-primary">
                Subscribe
              </button>
            </form>
          </div>
        </div>
      )}

      <div className="sidebar-widget outer-top-vs">
        <div id="advertisement" className="advertisement">
          {[
            ['member1.png', 'John Doe', 'Abc Company'],
            ['member3.png', 'Stephen Doe', 'Xperia Designs'],
            ['member2.png', 'Saraha Smith', 'Datsun & Co'],
          ].map(([image, name, company]) => (
            <div className="item" key={name}>
              <div className="avatar">
                <img src={`/assets/images/testimonials/${image}`} alt="Image" />
              </div>
              <div className="testimonials">
                <em>"</em> Vtae sodales aliq uam morbi non sem lacus port mollis. Nunc condime tum metus
                eud molest sed consectetuer. Sed quia non numquam eius modi tempora incidunt ut labore et
                dolore magnam aliquam quaerat.<em>"</em>
              </div>
              <div className="clients_author">
                {name} <span>{company}</span>
              </div>
            </div>
          ))}
        </div>
      </div>
    </Sidebar>
  );
}
