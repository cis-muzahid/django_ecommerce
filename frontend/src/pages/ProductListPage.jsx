import { useEffect, useState } from 'react';
import ProductCard from '../components/ProductCard';
import Breadcrumbs from '../components/Breadcrumbs';
import Sidebar from '../components/Sidebar';
import apiClient from '../services/apiClient';
import { useAuth } from '../context/AuthContext';
import { useCart } from '../context/CartContext';
import { useLayout } from '../context/LayoutContext';

function flattenCategories(categories, result = []) {
  categories.forEach((category) => {
    result.push(category);
    if (category.subcategories?.length) {
      flattenCategories(category.subcategories, result);
    }
  });
  return result;
}

export default function ProductListPage() {
  const { categories } = useLayout();
  const { isAuthenticated } = useAuth();
  const { addToCart, addToWishlist } = useCart();
  const [products, setProducts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [filters, setFilters] = useState({
    category: '',
    min_price: '',
    max_price: '',
    search: '',
    ordering: '',
  });

  const flatCategories = flattenCategories(categories);

  useEffect(() => {
    fetchProducts();
  }, [filters]);

  const fetchProducts = async () => {
    try {
      setLoading(true);
      const params = new URLSearchParams();
      Object.entries(filters).forEach(([key, value]) => {
        if (value) params.append(key, value);
      });

      const response = await apiClient.get(`/products/?${params.toString()}`);
      setProducts(response.data.results || response.data);
    } catch (error) {
      console.error('Failed to fetch products:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleFilterChange = (e) => {
    setFilters({
      ...filters,
      [e.target.name]: e.target.value,
    });
  };

  async function handleAddCart(productId) {
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
  }

  async function handleAddWishlist(productId) {
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
  }

  return (
    <>
      <Breadcrumbs items={[{ label: 'Products' }]} />

      <div className="row">
        <Sidebar categories={categories}>
          <div className="sidebar-module-container">
            <div className="sidebar-filter">
              <div className="sidebar-widget">
                <h3 className="section-title">Filter by Category</h3>
                <select
                  name="category"
                  className="form-control"
                  value={filters.category}
                  onChange={handleFilterChange}
                >
                  <option value="">All Categories</option>
                  {flatCategories.map((cat) => (
                    <option key={cat.id} value={cat.id}>
                      {cat.name}
                    </option>
                  ))}
                </select>
              </div>

              <div className="sidebar-widget">
                <h3 className="section-title">Price Range</h3>
                <div className="form-group">
                  <input
                    type="number"
                    name="min_price"
                    className="form-control"
                    placeholder="Min Price"
                    value={filters.min_price}
                    onChange={handleFilterChange}
                  />
                </div>
                <div className="form-group">
                  <input
                    type="number"
                    name="max_price"
                    className="form-control"
                    placeholder="Max Price"
                    value={filters.max_price}
                    onChange={handleFilterChange}
                  />
                </div>
              </div>

              <div className="sidebar-widget">
                <h3 className="section-title">Sort By</h3>
                <select
                  name="ordering"
                  className="form-control"
                  value={filters.ordering}
                  onChange={handleFilterChange}
                >
                  <option value="">Default</option>
                  <option value="name">Name (A-Z)</option>
                  <option value="-name">Name (Z-A)</option>
                  <option value="price">Price (Low to High)</option>
                  <option value="-price">Price (High to Low)</option>
                  <option value="-created_at">Newest First</option>
                </select>
              </div>
            </div>
          </div>
        </Sidebar>

        <div className="col-xs-12 col-sm-12 col-md-9 homebanner-holder">
          <div className="row">
            {loading ? (
              <div className="col-12 text-center">
                <p>Loading products...</p>
              </div>
            ) : products.length > 0 ? (
              products.map((product) => (
                <div key={product.id} className="col-sm-6 col-md-4 wow fadeInUp">
                  <ProductCard
                    product={product}
                    isAuthenticated={isAuthenticated}
                    onAddCart={handleAddCart}
                    onAddWishlist={handleAddWishlist}
                  />
                </div>
              ))
            ) : (
              <div className="col-12 text-center">
                <p>No products found</p>
              </div>
            )}
          </div>
        </div>
      </div>
    </>
  );
}
