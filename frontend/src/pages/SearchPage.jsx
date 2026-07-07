import { useEffect, useState } from 'react';
import { Link, useSearchParams } from 'react-router-dom';
import Breadcrumbs from '../components/Breadcrumbs';
import ProductCard from '../components/ProductCard';
import apiClient from '../services/apiClient';
import { useAuth } from '../context/AuthContext';
import { useCart } from '../context/CartContext';

export default function SearchPage() {
  const [searchParams] = useSearchParams();
  const { isAuthenticated } = useAuth();
  const { addToCart, addToWishlist } = useCart();

  const query = searchParams.get('q') || '';

  const [products, setProducts] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (query) {
      searchProducts();
    }
  }, [query]);

  const searchProducts = async () => {
    try {
      setLoading(true);

      const response = await apiClient.get(
        `/products/search/?q=${encodeURIComponent(query)}`
      );

      setProducts(response.data.results || response.data);
    } catch (error) {
      console.error('Failed to search products:', error);
    } finally {
      setLoading(false);
    }
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
      <Breadcrumbs items={[{ label: 'Search Results' }]} />

      <div className="row">
            <div className="col-xs-12">

              <h2 className="section-title">
                Search Results for "{query}"
              </h2>

              <p className="text-muted">
                Found {products.length} products
              </p>

              <div className="search-result-container">
                <div className="category-product">
                  <div className="row">

                    {loading ? (
                      <div
                        className="col-xs-12 text-center"
                        style={{ padding: '50px' }}
                      >
                        <p>Searching...</p>
                      </div>
                    ) : products.length > 0 ? (
                      products.map((product) => (
                        <div
                          key={product.id}
                          className="col-sm-6 col-md-4 col-lg-3"
                        >
                          <ProductCard
                            product={product}
                            isAuthenticated={isAuthenticated}
                            onAddCart={handleAddCart}
                            onAddWishlist={handleAddWishlist}
                          />
                        </div>
                      ))
                    ) : (
                      <div
                        className="col-xs-12 text-center"
                        style={{ padding: '50px' }}
                      >
                        <h3>No products found</h3>

                        <p>
                          Try searching with different keywords
                        </p>

                        <Link
                          to="/"
                          className="btn btn-primary"
                        >
                          Continue Shopping
                        </Link>
                      </div>
                    )}

                  </div>
                </div>
              </div>

            </div>
      </div>
    </>
  );
}
