import { useEffect, useState } from 'react';
import { useParams, Link } from 'react-router-dom';
import Breadcrumbs from '../components/Breadcrumbs';
import BrandsCarousel from '../components/BrandsCarousel';
import ProductCard from '../components/ProductCard';
import { useAuth } from '../context/AuthContext';
import { useCart } from '../context/CartContext';
import apiClient from '../services/apiClient';
import { categoryHref, productHref } from '../utils/catalog';

export default function ProductDetailPage() {
  const { slug, categoryName, parentCategory, childCategory } = useParams();
  const { isAuthenticated } = useAuth();
  const { addToCart, addToWishlist } = useCart();

  // Determine the actual category name
  // If parentCategory and childCategory exist, use childCategory
  // Otherwise use categoryName
  const actualCategoryName = childCategory || categoryName;
  const [product, setProduct] = useState(null);
  const [quantity, setQuantity] = useState(1);
  const [loading, setLoading] = useState(true);
  const [reviews, setReviews] = useState([]);
  const [relatedProducts, setRelatedProducts] = useState([]);
  const [hotDeals, setHotDeals] = useState([]);
  const [activeTab, setActiveTab] = useState('description');
  const [banner, setBanner] = useState(null);
  const [showReviewModal, setShowReviewModal] = useState(false);
  const [reviewData, setReviewData] = useState({
    rating: 0,
    title: '',
    comment: ''
  });
  const [submittingReview, setSubmittingReview] = useState(false);
  const [reviewError, setReviewError] = useState(null);
  const [reviewSuccess, setReviewSuccess] = useState(false);
  const [attributes, setAttributes] = useState([]);
  const [selectedAttributeId, setSelectedAttributeId] = useState(null);
  const [specifications, setSpecifications] = useState([]);
  const [breadcrumbs, setBreadcrumbs] = useState([]);

  useEffect(() => {
    fetchProductDetail();
  }, [slug, actualCategoryName]);

  useEffect(() => {
    if (!showReviewModal) {
      document.body.classList.remove('modal-open');
      return undefined;
    }

    document.body.classList.add('modal-open');
    return () => {
      document.body.classList.remove('modal-open');
    };
  }, [showReviewModal]);

  useEffect(() => {
    // Initialize owl carousel for product images
    if (product && window.$) {
      setTimeout(() => {
        if (window.$('#owl-single-product').length && !window.$('#owl-single-product').hasClass('owl-loaded')) {
          window.$('#owl-single-product').owlCarousel({
            items: 1,
            nav: true,
            dots: false,
            navText: ['<i class="fa fa-angle-left"></i>', '<i class="fa fa-angle-right"></i>']
          });
        }

        if (window.$('#owl-single-product-thumbnails').length && !window.$('#owl-single-product-thumbnails').hasClass('owl-loaded')) {
          window.$('#owl-single-product-thumbnails').owlCarousel({
            items: 4,
            nav: false,
            dots: false
          });
        }

        if (window.$('.upsell-product').length && !window.$('.upsell-product').hasClass('owl-loaded')) {
          window.$('.upsell-product').owlCarousel({
            items: 4,
            nav: true,
            dots: false,
            navText: ['<i class="fa fa-angle-left"></i>', '<i class="fa fa-angle-right"></i>'],
            responsive: {
              0: { items: 1 },
              480: { items: 2 },
              768: { items: 3 },
              992: { items: 4 }
            }
          });
        }

        if (window.$('.sidebar-carousel').length && !window.$('.sidebar-carousel').hasClass('owl-loaded')) {
          window.$('.sidebar-carousel').owlCarousel({
            items: 1,
            nav: true,
            dots: false,
            navText: ['<i class="fa fa-angle-left"></i>', '<i class="fa fa-angle-right"></i>']
          });
        }
      }, 300);
    }
  }, [product, relatedProducts]);

  // Fetch product detail using the correct API endpoint
  const fetchProductDetail = async () => {
    try {
      setLoading(true);

      // Use the dedicated product detail endpoint that matches Django implementation
      // Endpoint: /api/v1/category/<category_name>/<product_slug>/
      const response = await apiClient.get(
        `/category/${encodeURIComponent(actualCategoryName)}/${encodeURIComponent(slug)}/`,
      );

      if (response.data && response.data.product) {
        setProduct(response.data.product);
        setReviews(response.data.product.reviews || []);
        setRelatedProducts(response.data.related_products || []);
        setHotDeals(response.data.hot_deals || []);
        setBanner(response.data.banner);
        // Build breadcrumbs by walking up parent_category chain
        const crumbs = [];
        let current = response.data.product.category;

        while (current) {
          crumbs.unshift({ name: current.name, slug: current.name });
          if (current.parent_category) {
            current = current.parent_category;
          } else {
            break;
          }
        }

        setBreadcrumbs(crumbs);

        // Fetch attributes and specifications
        try {
          const attrsResponse = await apiClient.get(`/products/${response.data.product.id}/attributes/`);
          const attrs = attrsResponse.data.results || attrsResponse.data;
          setAttributes(attrs);
          const firstAvailable = attrs.find((attr) => !(attr.out_of_stoke || attr.out_of_stock) && attr.is_display !== false);
          setSelectedAttributeId(firstAvailable?.id || null);
        } catch (error) {
          console.error('Failed to fetch attributes:', error);
        }

        try {
          const specsResponse = await apiClient.get(`/products/${response.data.product.id}/specifications/`);
          setSpecifications(specsResponse.data.results || specsResponse.data);
        } catch (error) {
          console.error('Failed to fetch specifications:', error);
        }

        // Fetch related products
        try {
          const relatedResponse = await apiClient.get(`/products/${response.data.product.id}/related/`);
          setRelatedProducts(relatedResponse.data.results || relatedResponse.data);
        } catch (error) {
          console.error('Failed to fetch related products:', error);
        }
      }
    } catch (error) {
      console.error('Failed to fetch product detail:', error);
      setProduct(null);
    } finally {
      setLoading(false);
    }
  };

  const handleAddToCart = async () => {
    if (!isAuthenticated) {
      alert('Please login to add items to cart');
      return;
    }
    const selectedAttribute = attributes.find((attr) => attr.id === selectedAttributeId);
    if (attributes.length > 0 && !selectedAttribute) {
      alert('Please select an available product option');
      return;
    }
    if (selectedAttribute?.out_of_stoke || selectedAttribute?.out_of_stock) {
      alert('Selected option is out of stock');
      return;
    }
    const result = await addToCart(product.id, quantity);
    if (result.success) {
      alert('Product added to cart!');
    } else {
      alert('Failed to add product to cart');
    }
  };

  const handleAddToWishlist = async () => {
    if (!isAuthenticated) {
      alert('Please login to add items to wishlist');
      return;
    }
    const result = await addToWishlist(product.id);
    if (result.success) {
      alert('Product added to wishlist!');
    } else {
      alert('Failed to add product to wishlist');
    }
  };

  const increaseQuantity = () => {
    setQuantity(prev => prev + 1);
  };

  const decreaseQuantity = () => {
    setQuantity(prev => Math.max(1, prev - 1));
  };

  const handleRatingClick = (rating) => {
    setReviewData(prev => ({ ...prev, rating }));
  };

  const handleReviewInputChange = (e) => {
    const { name, value } = e.target;
    setReviewData(prev => ({ ...prev, [name]: value }));
  };

  const handleSubmitReview = async () => {
    if (!reviewData.rating) {
      setReviewError('Please select a rating');
      return;
    }
    if (!reviewData.title.trim()) {
      setReviewError('Please enter a review title');
      return;
    }
    if (!reviewData.comment.trim()) {
      setReviewError('Please enter a review comment');
      return;
    }

    setSubmittingReview(true);
    setReviewError(null);

    try {
      await apiClient.post(`/products/${product.id}/reviews/`, {
        review: reviewData.rating,
        title: reviewData.title,
        comment: reviewData.comment
      });

        setReviewSuccess(true);
        setReviewData({ rating: 0, title: '', comment: '' });
        setTimeout(() => {
          setShowReviewModal(false);
          setReviewSuccess(false);
          fetchProductDetail();
        }, 2000);
    } catch (error) {
      console.error('Error submitting review:', error);
      setReviewError(error.response?.data?.error || 'Failed to submit review. Please try again.');
    } finally {
      setSubmittingReview(false);
    }
  };

  if (loading) {
    return <p className="text-center" style={{ padding: '50px' }}>Loading product...</p>;
  }

  if (!product) {
    return <p className="text-center" style={{ padding: '50px' }}>Product not found</p>;
  }

  // Calculate average rating from reviews
  const averageRating = reviews.length > 0
    ? Math.round(reviews.reduce((sum, r) => sum + (r.review || 0), 0) / reviews.length)
    : 0;
  const selectedAttribute = attributes.find((attr) => attr.id === selectedAttributeId);
  const displayImage = selectedAttribute?.product_image || product.main_image || '/assets/images/products/p1.jpg';

  const breadcrumbItems = [
    ...breadcrumbs.map((crumb, index) => ({
      label: crumb.name,
      link: categoryHref(crumb.name),
      active: false
    })),
    { label: product?.name, link: '#', active: true }
  ];

  return (
    <>
      <Breadcrumbs items={breadcrumbItems} />

      <div className='row single-product'>
            {/* Sidebar */}
            <div className='col-xs-12 col-sm-12 col-md-3 sidebar'>
              <div className="sidebar-module-container">
                {/* Category Banner */}
                {banner && (
                  <div className="sidebar-widget outer-bottom-small">
                    <div style={{
                      background: `url('${banner.image_url || banner.image}')`,
                      backgroundSize: 'cover',
                      padding: '30px 20px',
                      textAlign: 'center',
                      color: 'white'
                    }}>
                      <h3 style={{ fontSize: '18px', fontWeight: 'bold', marginBottom: '10px' }}>
                        {banner.subtitle || 'ELECTRONICS'}
                      </h3>
                      <h2 style={{ fontSize: '24px', fontWeight: 'bold', marginBottom: '10px' }}>
                        {banner.title || 'Top Brands'}
                      </h2>
                      <h2 style={{ fontSize: '24px', fontWeight: 'bold', marginBottom: '20px' }}>
                        Huge Selection
                      </h2>
                      <button
                        className="btn btn-warning"
                        style={{
                          backgroundColor: '#FFD700',
                          border: 'none',
                          padding: '10px 30px',
                          fontWeight: 'bold'
                        }}
                      >
                        BUY NOW
                      </button>
                    </div>
                  </div>
                )}

                {/* Hot Deals */}
                <div className="sidebar-widget hot-deals outer-bottom-xs">
                  <h3 className="section-title">Hot deals</h3>
                  <div className="owl-carousel sidebar-carousel custom-carousel owl-theme outer-top-ss">
                    {hotDeals.length > 0 ? hotDeals.map(deal => (
                      <div key={deal.id} className="item">
                        <div className="products">
                          <div className="hot-deal-wrapper">
                            <div className="image">
                              <Link to={productHref(deal)}>
                                <img
                                  src={deal.main_image || deal.image || '/assets/images/products/p1.jpg'}
                                  alt={deal.name}
                                  onError={(e) => {
                                    e.target.onerror = null;
                                    e.target.src = '/assets/images/products/p1.jpg';
                                  }}
                                />
                              </Link>
                            </div>
                            {deal.tag && (
                              <div className="sale-offer-tag">
                                <span>{deal.tag}<br />off</span>
                              </div>
                            )}
                          </div>
                          <div className="product-info text-left m-t-20">
                            <h3 className="name">
                              <Link to={productHref(deal)}>{deal.name}</Link>
                            </h3>
                            <div className="rating">
                              {[1, 2, 3, 4, 5].map(star => (
                                <span key={star} className={star <= deal.average_rating ? 'star' : 'empty-star'}>★</span>
                              ))}
                            </div>
                            <div className="product-price">
                              <span className="price">${deal.price}</span>
                            </div>
                          </div>
                          {isAuthenticated && (
                            <div className="cart clearfix animate-effect">
                              <div className="action">
                                <div className="add-cart-button btn-group">
                                  <button
                                    onClick={() => addToCart(deal.id, 1)}
                                    className="btn btn-primary icon"
                                    title="Add Cart"
                                  >
                                    <i className="fa fa-shopping-cart"></i> Add to cart
                                  </button>
                                </div>
                              </div>
                            </div>
                          )}
                        </div>
                      </div>
                    )) : (
                      <div className="item">
                        <p className="text-center">No hot deals available</p>
                      </div>
                    )}
                  </div>
                </div>

                {/* Newsletter */}
                {!isAuthenticated && (
                  <div className="sidebar-widget newsletter outer-bottom-small outer-top-vs">
                    <h3 className="section-title">Newsletters</h3>
                    <div className="sidebar-widget-body outer-top-xs">
                      <p>Sign Up for Our Newsletter!</p>
                      <form>
                        <div className="form-group">
                          <label className="sr-only" htmlFor="productNewsletterEmail">Email address</label>
                          <input
                            type="email"
                            className="form-control"
                            id="productNewsletterEmail"
                            placeholder="Subscribe to our newsletter"
                          />
                        </div>
                        <button type="button" className="btn btn-primary">Subscribe</button>
                      </form>
                    </div>
                  </div>
                )}
              </div>
            </div>

            {/* Main Content */}
            <div className='col-xs-12 col-sm-12 col-md-9 rht-col'>
              <div className="detail-block">
                <div className="row">
                  {/* Product Images */}
                  <div className="col-xs-12 col-sm-12 col-md-4 col-lg-4 gallery-holder">
                    <div className="product-item-holder size-big single-product-gallery small-gallery">
                      <div id="owl-single-product">
                        <div className="single-product-gallery-item">
                          <a data-lightbox="image-1" data-title="Gallery" href={displayImage}>
                            <img
                              className="img-responsive"
                              alt={product.name}
                              src={displayImage}
                            />
                          </a>
                        </div>
                      </div>

                      <div className="single-product-gallery-thumbs gallery-thumbs">
                        <div id="owl-single-product-thumbnails">
                          <div className="item">
                            <a className="horizontal-thumb active" data-target="#owl-single-product" data-slide="1" href="#slide1">
                              <img className="img-responsive" alt={product.name} src={product.main_image || '/assets/images/products/p1.jpg'} />
                            </a>
                          </div>
                          {product.attributes && product.attributes.map((attr, idx) => (
                            attr.product_image && (
                              <div key={idx} className="item">
                                <a className="horizontal-thumb" data-target="#owl-single-product" data-slide={idx + 2} href={`#slide${idx + 2}`}>
                                  <img className="img-responsive" alt={attr.title} src={attr.product_image} />
                                </a>
                              </div>
                            )
                          ))}
                        </div>
                      </div>
                    </div>
                  </div>

                  {/* Product Info */}
                  <div className='col-sm-12 col-md-8 col-lg-8 product-info-block'>
                    <div className="product-info">
                      <h1 className="name">{product.name}</h1>

                      <div className="rating-reviews m-t-20">
                        <div className="row">
                          <div className="col-lg-12">
                            <div className="pull-left">
                              <div className="rating">
                                {[1, 2, 3, 4, 5].map(star => (
                                  <span key={star} className={star <= averageRating ? 'star' : 'empty-star'}>★</span>
                                ))}
                              </div>
                            </div>
                            <div className="pull-left">
                              <div className="reviews">
                                <a href="#review" className="lnk">({reviews.length} Reviews)</a>
                              </div>
                            </div>
                          </div>
                        </div>
                      </div>

                      <div className="stock-container info-container m-t-10">
                        <div className="row">
                          <div className="col-lg-12">
                            <div className="pull-left">
                              <div className="stock-box">
                                <span className="label">Availability :</span>
                              </div>
                            </div>
                            <div className="pull-left">
                              <div className="stock-box">
                                <span className="value">In Stock</span>
                              </div>
                            </div>
                          </div>
                        </div>
                      </div>

                      <div className="description-container m-t-20">
                        <p>{product.description}</p>
                      </div>

                      {/* Product Attributes */}
                      {attributes && attributes.length > 0 && (
                        <div className="attributes-container m-t-20">
                          {/* <h4>Choose Option</h4> */}
                          <div className="btn-group" role="group" aria-label="Product options">
                            {attributes.map((attr) => {
                              const isDisabled = attr.out_of_stoke || attr.out_of_stock || attr.is_display === false;
                              return (
                                <button
                                  key={attr.id}
                                  type="button"
                                  className={`btn ${selectedAttributeId === attr.id ? 'btn-primary' : 'btn-default'}`}
                                  onClick={() => setSelectedAttributeId(attr.id)}
                                  disabled={isDisabled}
                                  title={isDisabled ? 'Out of stock' : `${attr.title}: ${attr.value}`}
                                  style={{ marginRight: '8px', marginBottom: '8px' }}
                                >
                                  <strong>{attr.title}</strong>: {attr.value}
                                  {isDisabled ? ' (Out of stock)' : ''}
                                </button>
                              );
                            })}
                          </div>
                        </div>
                      )}

                      {/* Product Specifications */}
                      {specifications && specifications.length > 0 && (
                        <div className="specifications-container m-t-20">
                          <h4>Specifications</h4>
                          <table className="table table-striped">
                            <tbody>
                              {specifications.map((spec, idx) => (
                                <tr key={idx}>
                                  <td><strong>{spec.title}</strong></td>
                                  <td>{spec.description}</td>
                                </tr>
                              ))}
                            </tbody>
                          </table>
                        </div>
                      )}

                      <div className="price-container info-container m-t-30">
                        <div className="row">
                          <div className="col-sm-6 col-xs-6">
                            <div className="price-box">
                              <span className="price">${product.price}</span>
                            </div>
                          </div>
                          <div className="col-sm-6 col-xs-6">
                            <div className="favorite-button m-t-5">
                              <button
                                onClick={handleAddToWishlist}
                                className="btn btn-primary"
                                title="Wishlist"
                              >
                                <i className="fa fa-heart"></i>
                              </button>
                              <a className="btn btn-primary" title="Add to Compare" href="#">
                                <i className="fa fa-signal"></i>
                              </a>
                              <a className="btn btn-primary" title="E-mail" href="#">
                                <i className="fa fa-envelope"></i>
                              </a>
                            </div>
                          </div>
                        </div>
                      </div>

                      <div className="quantity-container info-container">
                        <div className="row">
                          <div className="qty">
                            <span className="label">Qty :</span>
                          </div>
                          <div className="qty-count">
                            <div className="cart-quantity">
                              <div className="quant-input">
                                <div className="arrows">
                                  <div className="arrow plus gradient" onClick={increaseQuantity}>
                                    <span className="ir"><i className="icon fa fa-sort-asc"></i></span>
                                  </div>
                                  <div className="arrow minus gradient" onClick={decreaseQuantity}>
                                    <span className="ir"><i className="icon fa fa-sort-desc"></i></span>
                                  </div>
                                </div>
                                <input
                                  type="number"
                                  value={quantity}
                                  onChange={(e) => setQuantity(Math.max(1, parseInt(e.target.value) || 1))}
                                  min="1"
                                  id="quantity-input"
                                />
                              </div>
                            </div>
                          </div>
                          <div className="add-btn">
                            <button onClick={handleAddToCart} className="btn btn-primary">
                              <i className="fa fa-shopping-cart inner-right-vs"></i>
                              ADD TO CART
                            </button>
                          </div>
                          <div className="add-btn">
                            <button
                              type="button"
                              className="btn btn-primary"
                              onClick={() => setShowReviewModal(true)}
                            >
                              ADD REVIEW
                            </button>
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>

              {/* Product Tabs */}
              <div className="product-tabs inner-bottom-xs">
                <div className="row">
                  <div className="col-sm-12 col-md-3 col-lg-3">
                    <ul id="product-tabs" className="nav nav-tabs nav-tab-cell">
                      <li className={activeTab === 'description' ? 'active' : ''}>
                        <a onClick={() => setActiveTab('description')} href="#description" data-toggle="tab">DESCRIPTION</a>
                      </li>
                      <li className={activeTab === 'review' ? 'active' : ''}>
                        <a onClick={() => setActiveTab('review')} href="#review" data-toggle="tab">REVIEW</a>
                      </li>
                    </ul>
                  </div>
                  <div className="col-sm-12 col-md-9 col-lg-9">
                    <div className="tab-content">
                      <div id="description" className={`tab-pane ${activeTab === 'description' ? 'in active' : ''}`}>
                        <div className="product-tab">
                          <p className="text">{product.description}</p>
                        </div>
                      </div>

                      <div id="review" className={`tab-pane ${activeTab === 'review' ? 'in active' : ''}`}>
                        <div className="product-tab">
                          <div className="product-reviews">
                            <h4 className="title">Customer Reviews</h4>
                            <div className="reviews">
                              {reviews.length > 0 ? (
                                reviews.map(review => (
                                  <div key={review.id} className="review">
                                    <div className="review-title">
                                      <span className="summary">{review.title}</span>
                                      <span className="date">
                                        <i className="fa fa-calendar"></i>
                                        <span>{new Date(review.created_at).toLocaleDateString()}</span>
                                      </span>
                                    </div>
                                    <div className="text">{review.comment}</div>
                                  </div>
                                ))
                              ) : (
                                <p>No reviews yet. Be the first to review this product!</p>
                              )}
                            </div>
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>

              {/* Upsell Products */}
              {relatedProducts.length > 0 && (
                <section className="section featured-product">
                  <div className="row">
                    <div className="col-lg-3">
                      <h3 className="section-title">Upsell Products</h3>
                    </div>
                    <div className="col-lg-9">
                      <div className="owl-carousel homepage-owl-carousel upsell-product custom-carousel owl-theme outer-top-xs">
                        {relatedProducts.map((relatedProduct) => (
                          <ProductCard
                            key={relatedProduct.id}
                            product={relatedProduct}
                            isAuthenticated={isAuthenticated}
                            onAddCart={async (productId) => {
                              const result = await addToCart(productId, 1);
                              alert(result.success ? 'Product added to cart!' : 'Failed to add product to cart');
                            }}
                            onAddWishlist={async (productId) => {
                              const result = await addToWishlist(productId);
                              alert(result.success ? 'Product added to wishlist!' : 'Failed to add product to wishlist');
                            }}
                          />
                        ))}
                      </div>
                    </div>
                  </div>
                </section>
              )}
            </div>
          </div>

          {/* Brands Carousel */}
          <BrandsCarousel />

      {/* Review Modal */}
      {showReviewModal && (
        <>
        <div className="modal fade in product-review-modal" style={{ display: 'block' }} role="dialog" aria-modal="true">
          <div className="modal-dialog" role="document">
            <div className="modal-content">
              <div className="modal-header text-center">
                <h3 className="modal-title">Add your review</h3>
                <button
                  type="button"
                  className="close"
                  onClick={() => setShowReviewModal(false)}
                >
                  <span>&times;</span>
                </button>
              </div>
              <div className="modal-body">
                {reviewSuccess && (
                  <div className="alert alert-success">
                    Thank you! Your review has been submitted successfully.
                  </div>
                )}
                {reviewError && (
                  <div className="alert alert-danger">
                    {reviewError}
                  </div>
                )}

                {!reviewSuccess && (
                  <form onSubmit={(event) => event.preventDefault()}>
                    <div className="form-group text-center product-review-stars">
                      <h4>How much you like this product</h4>
                      <div className="star-rating">
                        {[1, 2, 3, 4, 5].map(star => (
                          <button
                            type="button"
                            key={star}
                            onClick={() => handleRatingClick(star)}
                            className={star <= reviewData.rating ? 'selected' : ''}
                            aria-label={`${star} star`}
                          >
                            ★
                          </button>
                        ))}
                      </div>
                      <input type="hidden" name="review" value={reviewData.rating} />
                    </div>

                    <div className="form-horizontal">
                      <div className="form-group">
                        <label className="col-sm-2 control-label" htmlFor="reviewTitle">Title :</label>
                        <div className="col-sm-10">
                          <input
                            type="text"
                            className="form-control"
                            id="reviewTitle"
                            name="title"
                            value={reviewData.title}
                            onChange={handleReviewInputChange}
                            disabled={submittingReview}
                          />
                        </div>
                      </div>

                      <div className="form-group">
                        <label className="col-sm-2 control-label" htmlFor="reviewComment">Comment :</label>
                        <div className="col-sm-10">
                          <input
                            type="text"
                            className="form-control"
                            id="reviewComment"
                            name="comment"
                            value={reviewData.comment}
                            onChange={handleReviewInputChange}
                            disabled={submittingReview}
                          />
                        </div>
                      </div>
                    </div>
                  </form>
                )}
              </div>
              <div className="modal-footer">
                <button
                  type="button"
                  className="btn btn-secondary"
                  onClick={() => setShowReviewModal(false)}
                  disabled={submittingReview}
                >
                  Close
                </button>
                {!reviewSuccess && (
                  <button
                    type="button"
                    className="btn btn-primary"
                    onClick={handleSubmitReview}
                    disabled={submittingReview}
                  >
                    {submittingReview ? 'Submitting...' : 'Submit Review'}
                  </button>
                )}
              </div>
            </div>
          </div>
        </div>
        <div className="modal-backdrop fade in"></div>
        </>
      )}
    </>
  );
}
