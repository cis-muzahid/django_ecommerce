# Complete API Integration Guide

## ✅ What Has Been Done

### 1. API Service Layer Created
All API services are now properly structured and use correct Django DRF endpoints:

- ✅ **authService.js** - Authentication & user management
- ✅ **productService.js** - Products, categories, reviews
- ✅ **homeService.js** - Homepage data, banners, facilities
- ✅ **cartService.js** - Cart & wishlist management
- ✅ **orderService.js** - Orders, checkout, payments
- ✅ **blogService.js** - Blogs & comments
- ✅ **apiClient.js** - Axios instance with JWT handling
- ✅ **index.js** - Central export for all services

### 2. Supplier Services Updated
All supplier services now use the correct main API endpoints:

- ✅ **supplier/services/productService.js**
- ✅ **supplier/services/orderService.js**
- ✅ **supplier/services/bannerService.js**
- ✅ **supplier/services/blogService.js**

Backend automatically filters data by supplier user ID.

### 3. API Documentation Created
- ✅ **API_ENDPOINTS.md** - Complete endpoint documentation
- ✅ **API_INTEGRATION_SUMMARY.md** - Integration summary & examples
- ✅ **.env.example** - Environment variables template
- ✅ **.env** - Environment configuration

### 4. API Client Features
- ✅ JWT token in request headers
- ✅ Automatic token refresh on 401
- ✅ Auto logout on refresh failure
- ✅ Proper error handling
- ✅ Multipart form data support

## 📋 Next Steps: Frontend Integration

### Phase 1: Update Context Providers

#### 1.1 Update AuthContext
**File**: `src/context/AuthContext.jsx`

**Current Issues**:
- Uses apiClient directly instead of authService
- Manual token handling

**Required Changes**:
```javascript
import { login as loginService, register as registerService, getProfile, logout as logoutService } from '../services';

// Replace login function
const login = async (email, password) => {
  try {
    const response = await loginService(email, password);
    const { tokens, user: userData } = response;
    
    localStorage.setItem('access_token', tokens.access);
    localStorage.setItem('refresh_token', tokens.refresh);
    setToken(tokens.access);
    setUser(userData);
    
    // Role-based redirect
    let redirectPath = '/';
    if (userData.is_superuser) {
      redirectPath = '/admin';
    } else if (userData.user_role?.name === 'supplier') {
      redirectPath = '/supplier';
    }
    
    return { success: true, redirectPath };
  } catch (error) {
    return { 
      success: false, 
      error: error.response?.data?.error || 'Login failed' 
    };
  }
};

// Replace signup function
const signup = async (userData) => {
  try {
    const response = await registerService(userData);
    return { success: true, data: response };
  } catch (error) {
    return { 
      success: false, 
      error: error.response?.data || 'Signup failed' 
    };
  }
};

// Replace logout function
const logout = async () => {
  try {
    const refreshToken = localStorage.getItem('refresh_token');
    if (refreshToken) {
      await logoutService(refreshToken);
    }
  } catch (error) {
    console.error('Logout error:', error);
  } finally {
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    setToken(null);
    setUser(null);
  }
};

// Replace fetchUserProfile
const fetchUserProfile = async () => {
  try {
    const userData = await getProfile();
    setUser(userData);
  } catch (error) {
    console.error('Failed to fetch user profile:', error);
    logout();
  } finally {
    setLoading(false);
  }
};
```

#### 1.2 Update CartContext
**File**: `src/context/CartContext.jsx`

**Current Issues**:
- Uses apiClient directly
- Manual cart management

**Required Changes**:
```javascript
import { 
  getCartItems, addToCart as addToCartService, 
  updateCartItem, removeFromCart as removeFromCartService,
  getWishlistItems, addToWishlist as addToWishlistService,
  removeFromWishlist as removeFromWishlistService,
  getCartWishlistStats
} from '../services';

// Replace fetchCart
const fetchCart = async () => {
  try {
    const data = await getCartItems();
    setCartItems(data.results || data);
  } catch (error) {
    console.error('Failed to fetch cart:', error);
  }
};

// Replace addToCart
const addToCart = async (productId, quantity = 1) => {
  try {
    await addToCartService(productId, quantity);
    await fetchCart();
    return { success: true };
  } catch (error) {
    return { success: false, error: error.response?.data };
  }
};

// Similar updates for other cart functions
```

### Phase 2: Update Pages

#### 2.1 Update HomePage
**File**: `src/pages/HomePage.jsx`

**Replace**:
```javascript
const response = await apiClient.get('/homepage/');
```

**With**:
```javascript
import { getHomePageData } from '../services';

const data = await getHomePageData();
setHomeData(data);
```

**Data Structure**:
```javascript
{
  banners: {
    header_banners: [],
    wide_banner_large: {},
    wide_banner_small: {},
    middle_banners: []
  },
  latest_products: [],
  special_offers: {
    products_1: [],
    products_2: [],
    products_3: []
  },
  hot_deals: [],
  categories: [],
  blogs: [],
  facilities: []
}
```

#### 2.2 Update ProductListPage
**File**: `src/pages/ProductListPage.jsx`

**Replace**:
```javascript
const response = await apiClient.get('/products/');
```

**With**:
```javascript
import { getProducts } from '../services';

const data = await getProducts({
  page: currentPage,
  search: searchQuery,
  category: categoryId,
  min_price: minPrice,
  max_price: maxPrice
});

setProducts(data.results || data);
setTotalPages(Math.ceil(data.count / 20)); // 20 items per page
```

#### 2.3 Update ProductDetailPage
**File**: `src/pages/ProductDetailPage.jsx`

**Replace**:
```javascript
const response = await apiClient.get(`/products/?slug=${slug}`);
```

**With**:
```javascript
import { getProductDetail } from '../services';

const data = await getProductDetail(categoryName, productSlug);
setProduct(data.product);
setRelatedProducts(data.related_products);
setHotDeals(data.hot_deals);
setReviews(data.product.reviews || []);
```

#### 2.4 Update CategoryPage
**File**: `src/pages/CategoryPage.jsx`

**Replace**:
```javascript
const response = await apiClient.get(`/category/${categoryName}/`);
```

**With**:
```javascript
import { getCategoryProducts } from '../services';

const data = await getCategoryProducts(categoryName, {
  page: currentPage,
  min_price: minPrice,
  max_price: maxPrice,
  search: searchQuery
});

setProducts(data.products);
setCategory(data.category);
setBanner(data.banner);
```

#### 2.5 Update CartPage
**File**: `src/pages/CartPage.jsx`

Use CartContext functions (already updated in Phase 1).

#### 2.6 Update CheckoutPage
**File**: `src/pages/CheckoutPage.jsx`

**Add**:
```javascript
import { processCheckout, processPayment } from '../services';

const handleCheckout = async () => {
  try {
    const checkoutData = {
      address: selectedAddressId,
      payment_method: paymentMethod,
      items: cartItems.map(item => ({
        product: item.product.id,
        quantity: item.quantity
      }))
    };
    
    const order = await processCheckout(checkoutData);
    
    if (paymentMethod === 'stripe') {
      const payment = await processPayment({
        order_id: order.id,
        payment_method: 'stripe',
        amount: order.total_amount
      });
      // Handle payment response
    }
    
    navigate('/orders');
  } catch (error) {
    console.error('Checkout error:', error);
    alert('Checkout failed');
  }
};
```

#### 2.7 Update OrdersPage
**File**: `src/pages/OrdersPage.jsx`

**Replace**:
```javascript
const response = await apiClient.get('/orders/');
```

**With**:
```javascript
import { getOrders } from '../services';

const data = await getOrders({ page: currentPage });
setOrders(data.results || data);
```

#### 2.8 Update BlogListPage
**File**: `src/pages/BlogListPage.jsx`

**Replace**:
```javascript
const response = await apiClient.get('/blogs/');
```

**With**:
```javascript
import { getBlogs } from '../services';

const data = await getBlogs({ 
  page: currentPage,
  search: searchQuery,
  category: categoryId
});

setBlogs(data.results || data);
```

#### 2.9 Update BlogDetailPage
**File**: `src/pages/BlogDetailPage.jsx`

**Replace**:
```javascript
const response = await apiClient.get(`/blogs/?slug=${slug}`);
```

**With**:
```javascript
import { getBlogBySlug, getBlogComments } from '../services';

const blogData = await getBlogBySlug(slug);
setBlog(blogData);

const commentsData = await getBlogComments(blogData.id);
setComments(commentsData.results || commentsData);
```

### Phase 3: Update Supplier Pages

Supplier pages already use correct services, just need to handle responses properly.

#### 3.1 Update SupplierProductsPage
**File**: `src/supplier/pages/ProductsPage.jsx`

**Current**: ✅ Already using correct service
**Check**: Response handling for pagination

```javascript
const data = await getProducts(currentPage, searchQuery);
setProducts(data.results || data);
setTotalPages(data.total_pages || Math.ceil(data.count / 10));
```

#### 3.2 Update SupplierOrdersPage
**File**: `src/supplier/pages/OrdersPage.jsx`

**Current**: ✅ Already using correct service
**Check**: Response handling

#### 3.3 Update SupplierBannersPage
**File**: `src/supplier/pages/BannersPage.jsx`

**Current**: ✅ Already using correct service
**Check**: Response handling

#### 3.4 Update SupplierBlogsPage
**File**: `src/supplier/pages/BlogsPage.jsx`

**Current**: ✅ Already using correct service
**Check**: Response handling

### Phase 4: Add Loading & Error Handling

#### 4.1 Create Toast Notification Component
**File**: `src/components/Toast.jsx`

```javascript
import { useState, useEffect } from 'react';

export default function Toast({ message, type = 'success', duration = 3000, onClose }) {
  useEffect(() => {
    const timer = setTimeout(() => {
      onClose();
    }, duration);
    
    return () => clearTimeout(timer);
  }, [duration, onClose]);
  
  return (
    <div className={`toast toast-${type}`}>
      {message}
    </div>
  );
}
```

#### 4.2 Create Loading Spinner Component
**File**: `src/components/LoadingSpinner.jsx`

```javascript
export default function LoadingSpinner({ fullScreen = false }) {
  if (fullScreen) {
    return (
      <div className="loading-overlay">
        <div className="spinner"></div>
      </div>
    );
  }
  
  return <div className="spinner"></div>;
}
```

#### 4.3 Add Error Boundary
**File**: `src/components/ErrorBoundary.jsx`

```javascript
import { Component } from 'react';

class ErrorBoundary extends Component {
  constructor(props) {
    super(props);
    this.state = { hasError: false, error: null };
  }
  
  static getDerivedStateFromError(error) {
    return { hasError: true, error };
  }
  
  componentDidCatch(error, errorInfo) {
    console.error('Error caught by boundary:', error, errorInfo);
  }
  
  render() {
    if (this.state.hasError) {
      return (
        <div className="error-page">
          <h1>Something went wrong</h1>
          <p>{this.state.error?.message}</p>
          <button onClick={() => window.location.reload()}>
            Reload Page
          </button>
        </div>
      );
    }
    
    return this.props.children;
  }
}

export default ErrorBoundary;
```

### Phase 5: Testing Checklist

#### Customer Flow
- [ ] Register new customer account
- [ ] Login with customer credentials
- [ ] Browse homepage (banners, products, categories)
- [ ] Search products
- [ ] Filter products by category
- [ ] View product details
- [ ] Add product to cart
- [ ] Update cart quantity
- [ ] Remove from cart
- [ ] Add to wishlist
- [ ] View wishlist
- [ ] Proceed to checkout
- [ ] Add delivery address
- [ ] Complete payment
- [ ] View orders
- [ ] Track order
- [ ] View profile
- [ ] Update profile
- [ ] Change password
- [ ] Browse blogs
- [ ] View blog details
- [ ] Add blog comment
- [ ] Logout

#### Supplier Flow
- [ ] Register supplier account
- [ ] Login with supplier credentials
- [ ] View supplier dashboard
- [ ] View products list
- [ ] Search products
- [ ] Add new product
- [ ] Edit product
- [ ] Delete product
- [ ] View orders
- [ ] Update order status
- [ ] View banners
- [ ] Add banner
- [ ] Edit banner
- [ ] Delete banner
- [ ] View blogs
- [ ] Add blog
- [ ] Edit blog
- [ ] Delete blog
- [ ] Logout

#### API Integration Tests
- [ ] All endpoints return correct data
- [ ] Pagination works correctly
- [ ] Search works correctly
- [ ] Filters work correctly
- [ ] JWT token refresh works
- [ ] Auto logout on token expiry
- [ ] Error messages display correctly
- [ ] Success messages display correctly
- [ ] Loading states show correctly
- [ ] Images load from media URL

## 🚀 Quick Start

### 1. Install Dependencies
```bash
cd ecommerce/frontend
npm install
```

### 2. Configure Environment
```bash
cp .env.example .env
# Edit .env with correct API URL
```

### 3. Start Development Server
```bash
npm run dev
```

### 4. Start Django Backend
```bash
cd ecommerce/django_ecommerce
python manage.py runserver
```

### 5. Test API Endpoints
Visit: `http://localhost:8000/api/docs/`

## 📝 Important Notes

1. **No Mock Data**: All services use real backend APIs
2. **Supplier Filtering**: Backend automatically filters by user
3. **Token Refresh**: Automatic on 401 errors
4. **Error Handling**: All services throw errors for component handling
5. **File Uploads**: Use multipart/form-data for images
6. **Pagination**: Backend returns paginated responses
7. **Media URLs**: Images are served from `/media/` path

## 🔧 Troubleshooting

### CORS Issues
Add to Django settings:
```python
CORS_ALLOWED_ORIGINS = [
    "http://localhost:5173",
    "http://localhost:3000",
]
```

### Token Not Working
Check:
1. Token is stored in localStorage
2. API client adds Bearer prefix
3. Token hasn't expired

### Images Not Loading
Check:
1. MEDIA_URL in Django settings
2. Media files served in development
3. Correct image path in response

## ✅ Summary

- ✅ All API services created and documented
- ✅ Correct Django DRF endpoints used
- ✅ JWT authentication implemented
- ✅ Token refresh automatic
- ✅ Supplier services use main APIs
- ✅ No mock/dummy data
- ✅ Proper error handling
- ✅ File upload support
- ✅ Pagination support
- ✅ Search & filter support

**Next**: Follow Phase 1-5 to complete frontend integration!
