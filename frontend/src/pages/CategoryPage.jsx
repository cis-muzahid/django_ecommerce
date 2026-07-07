import { useEffect, useState } from 'react';
import { Link, useParams } from 'react-router-dom';
import ProductCard from '../components/ProductCard';
import BrandsCarousel from '../components/BrandsCarousel';
import Breadcrumbs from '../components/Breadcrumbs';
import Sidebar from '../components/Sidebar';
import apiClient from '../services/apiClient';
import { useAuth } from '../context/AuthContext';
import { useCart } from '../context/CartContext';
import { useLayout } from '../context/LayoutContext';
import { categoryNavPath } from '../utils/navigation';
import { categoryHref } from '../utils/catalog';

function getSubcategories(category) {
  return category.subcategories || category.children || [];
}

export default function CategoryPage() {
  const { categoryName } = useParams();
  const activeCategoryName = decodeURIComponent(categoryName || '');
  const { isAuthenticated } = useAuth();
  const { addToCart, addToWishlist } = useCart();
  const { categories } = useLayout();
  const [products, setProducts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [priceRange, setPriceRange] = useState({ min: 0, max: 1000 });
  const [currentPage, setCurrentPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);
  const [pageSize] = useState(12);
  const [breadcrumbItems, setBreadcrumbItems] = useState([]);
  const [openCategoryIds, setOpenCategoryIds] = useState([]);

  useEffect(() => {
    if (categoryName) {
      fetchCategoryProducts();
    }
  }, [categoryName]);

  useEffect(() => {
    const activeParent = categories.find(
      (category) => category.name === activeCategoryName || hasDescendant(category, activeCategoryName),
    );

    if (activeParent) {
      setOpenCategoryIds((current) => (
        current.includes(activeParent.id) ? current : [...current, activeParent.id]
      ));
    }
  }, [categories, activeCategoryName]);

  const fetchCategoryProducts = async (page = 1) => {
    try {
      setLoading(true);
      const response = await apiClient.get(`/category/${encodeURIComponent(categoryName)}/`, {
        params: { page },
      });
      const data = response.data.results || response.data;

      setProducts(data.products || []);

      const crumbs = [];
      let current = data.category;

      while (current) {
        crumbs.unshift({
          label: current.name,
          link: categoryNavPath(current.name),
        });
        if (current.parent_category) {
          current = current.parent_category;
        } else {
          break;
        }
      }

      setBreadcrumbItems(crumbs);

      const count = response.data.count || data.count;
      if (count) {
        setTotalPages(Math.ceil(count / pageSize));
      }
      setCurrentPage(page);
    } catch (error) {
      console.error('Failed to fetch category products:', error);
    } finally {
      setLoading(false);
    }
  };

  const handlePriceFilter = async () => {
    try {
      setLoading(true);
      const response = await apiClient.post(
        `/category/${encodeURIComponent(categoryName)}/`,
        { price: `${priceRange.min},${priceRange.max}` },
        { params: { page: 1 } },
      );
      const data = response.data.results || response.data;

      setProducts(data.products || []);
      setCurrentPage(1);

      const count = response.data.count || data.count;
      if (count) {
        setTotalPages(Math.ceil(count / pageSize));
      }
    } catch (error) {
      console.error('Failed to filter products:', error);
    } finally {
      setLoading(false);
    }
  };

  const handlePriceChange = (e) => {
    const { name, value } = e.target;
    setPriceRange((prev) => ({ ...prev, [name]: parseInt(value, 10) }));
  };

  const toggleCategory = (categoryId) => {
    setOpenCategoryIds((current) => (
      current.includes(categoryId)
        ? current.filter((id) => id !== categoryId)
        : [...current, categoryId]
    ));
  };

  function hasDescendant(category, name) {
    return getSubcategories(category).some(
      (subcategory) => subcategory.name === name || hasDescendant(subcategory, name),
    );
  }

  const handleAddCart = async (productId) => {
    if (!isAuthenticated) {
      alert('Please log in to add items to cart.');
      return;
    }
    try {
      const result = await addToCart(productId, 1);
      if (result.success) {
        alert('Product added to cart!');
      } else {
        alert('Failed to add product to cart');
      }
    } catch (error) {
      console.error('Failed to add to cart:', error);
      alert('Failed to add product to cart');
    }
  };

  const handleAddWishlist = async (productId) => {
    if (!isAuthenticated) {
      alert('Please log in to add items to wishlist.');
      return;
    }
    try {
      const result = await addToWishlist(productId);
      if (result.success) {
        alert('Product added to wishlist!');
      } else {
        alert('Failed to add product to wishlist');
      }

    } catch (error) {
      console.error('Failed to add to wishlist:', error);
      alert('Failed to add product to wishlist');
    }
  };

  return (
    <>
      <Breadcrumbs items={breadcrumbItems} />

      <div className="row">
        <Sidebar categories={categories}>
          <div className="sidebar-module-container">
            <div className="sidebar-filter">
              <div className="sidebar-widget">
                <h3 className="section-title">Shop by</h3>
                <div className="widget-header">
                  <h4 className="widget-title">Category</h4>
                </div>
                <div className="sidebar-widget-body">
                  {categories.length ? (
                    <div className="accordion">
                      {categories.map((category) => {
                        const subcategories = getSubcategories(category);

                        if (subcategories.length) {
                          const isOpen = openCategoryIds.includes(category.id);

                          return (
                            <div className="accordion-group" key={category.id}>
                              <div className="accordion-heading">
                                <div className={`category-accordion-title${isOpen ? '' : ' collapsed'}`}>
                                  <Link to={categoryNavPath(category.name)}>{category.name}</Link>
                                  <button
                                    type="button"
                                    className="category-toggle-btn"
                                    onClick={() => toggleCategory(category.id)}
                                    aria-label={`${isOpen ? 'Collapse' : 'Expand'} ${category.name}`}
                                  >
                                    {isOpen ? '-' : '+'}
                                  </button>
                                </div>
                              </div>
                              <div className={`accordion-body collapse${isOpen ? ' in' : ''}`} id={`collapse_${category.id}`}>
                                <div className="accordion-inner" style={isOpen ? undefined : { display: 'none' }}>
                                  {isOpen && (
                                    <ul>
                                      {subcategories.map((subcategory) => (
                                        <li key={subcategory.id}>
                                          <Link to={categoryNavPath(subcategory.name)}>{subcategory.name}</Link>
                                        </li>
                                      ))}
                                    </ul>
                                  )}
                                </div>
                              </div>
                            </div>
                          );
                        }

                        return (
                          <Link to={categoryNavPath(category.name)} key={category.id}>
                            {category.name}
                          </Link>
                        );
                      })}
                    </div>
                  ) : (
                    <p>No Data Found</p>
                  )}
                </div>
              </div>

              <div className="sidebar-widget">
                <div className="widget-header">
                  <h4 className="widget-title">Price Slider</h4>
                </div>
                <div className="sidebar-widget-body m-t-10">
                  <div className="price-range-holder">
                    <span className="min-max">
                      <span className="pull-left">${priceRange.min}</span>
                      <span className="pull-right">${priceRange.max}</span>
                    </span>
                    <div style={{ marginTop: '10px' }}>
                      <div className="form-group">
                        <label>Min: ${priceRange.min}</label>
                        <input
                          type="range"
                          name="min"
                          min="0"
                          max="1000"
                          value={priceRange.min}
                          onChange={handlePriceChange}
                          className="form-control"
                        />
                      </div>
                      <div className="form-group">
                        <label>Max: ${priceRange.max}</label>
                        <input
                          type="range"
                          name="max"
                          min="0"
                          max="1000"
                          value={priceRange.max}
                          onChange={handlePriceChange}
                          className="form-control"
                        />
                      </div>
                      <button
                        type="button"
                        className="lnk btn btn-primary"
                        onClick={handlePriceFilter}
                        style={{ width: '100%' }}
                      >
                        Show Now
                      </button>
                    </div>
                  </div>
                </div>
              </div>

              <div className="sidebar-widget product-tag outer-top-vs">
                <h3 className="section-title">Product tags</h3>
                <div className="sidebar-widget-body outer-top-xs">
                  <div className="tag-list">
                    {categories.length ? (
                      categories.map((category) => (
                        <Link className="item" title={category.name} to={categoryHref(category)} key={category.id}>
                          {category.name}
                        </Link>
                      ))
                    ) : (
                      <p className="text-center">No Data Found</p>
                    )}
                  </div>
                </div>
              </div>
            </div>
          </div>
        </Sidebar>

        <div className="col-xs-12 col-sm-12 col-md-9 rht-col">
          <div className="search-result-container">
            <div className="tab-content category-list">
              <div className="tab-pane active" id="grid-container">
                <div className="category-product">
                  <div className="row">
                    {loading ? (
                      <div className="col-12 text-center" style={{ padding: '50px' }}>
                        <p>Loading products...</p>
                      </div>
                    ) : products.length > 0 ? (
                      products.map((product) => (
                        <div key={product.id} className="col-sm-6 col-md-4 col-lg-3">
                          <ProductCard
                            product={product}
                            isAuthenticated={isAuthenticated}
                            onAddCart={handleAddCart}
                            onAddWishlist={handleAddWishlist}
                          />
                        </div>
                      ))
                    ) : (
                      <div className="col-12 text-center" style={{ padding: '50px' }}>
                        <p>No products found in this category</p>
                      </div>
                    )}
                  </div>
                </div>
              </div>
            </div>

            {totalPages > 1 && (
              <div className="clearfix filters-container bottom-row">
                <div className="text-right">
                  <div className="pagination-container">
                    <ul className="list-inline list-unstyled">
                      {currentPage > 1 && (
                        <li className="prev">
                          <button
                            type="button"
                            className="page-link"
                            onClick={() => fetchCategoryProducts(currentPage - 1)}
                          >
                            <i className="fa fa-angle-left"></i>
                          </button>
                        </li>
                      )}

                      {Array.from({ length: Math.min(totalPages, 5) }, (_, i) => {
                        const startPage = Math.max(1, currentPage - 2);
                        return startPage + i;
                      }).map((page) => (
                        <li key={page} className={`page-item ${currentPage === page ? 'active' : ''}`}>
                          <button
                            type="button"
                            className="page-link"
                            onClick={() => fetchCategoryProducts(page)}
                          >
                            {page}
                          </button>
                        </li>
                      ))}

                      {currentPage < totalPages && (
                        <li className="next">
                          <button
                            type="button"
                            className="page-link"
                            onClick={() => fetchCategoryProducts(currentPage + 1)}
                          >
                            <i className="fa fa-angle-right"></i>
                          </button>
                        </li>
                      )}
                    </ul>
                  </div>
                </div>
              </div>
            )}
          </div>
        </div>
      </div>

      <BrandsCarousel />
    </>
  );
}
