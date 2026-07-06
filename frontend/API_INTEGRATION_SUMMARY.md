# API Integration Summary

## ✅ Complete API Integration Structure

### API Service Files Created

All API services are now properly organized and use the correct Django DRF endpoints:

#### 1. **Authentication Service** (`src/services/authService.js`)
- ✅ Register user
- ✅ Login user
- ✅ Logout user
- ✅ Refresh token
- ✅ Get/Update profile
- ✅ Change password
- ✅ Password reset
- ✅ Get roles
- ✅ Address management (CRUD)

#### 2. **Product Service** (`src/services/productService.js`)
- ✅ Get products with pagination & filters
- ✅ Get product by ID
- ✅ Search products
- ✅ Create/Update/Delete products
- ✅ Product attributes (CRUD)
- ✅ Product specifications (CRUD)
- ✅ Product reviews (CRUD)
- ✅ Get categories

#### 3. **Home Service** (`src/services/homeService.js`)
- ✅ Get homepage data (banners, products, categories, blogs, facilities)
- ✅ Banner management (CRUD)
- ✅ Facility management (CRUD)
- ✅ Get category products
- ✅ Filter products by price
- ✅ Get product detail with related data

#### 4. **Cart Service** (`src/services/cartService.js`)
- ✅ Get cart items
- ✅ Add to cart
- ✅ Update cart item quantity
- ✅ Remove from cart
- ✅ Clear cart
- ✅ Wishlist management (CRUD)
- ✅ Get cart/wishlist stats

#### 5. **Order Service** (`src/services/orderService.js`)
- ✅ Get orders with pagination
- ✅ Get order by ID
- ✅ Create order
- ✅ Update order
- ✅ Process checkout
- ✅ Process payment
- ✅ Track order
- ✅ Return/Replace requests (CRUD)
- ✅ Cancel order

#### 6. **Blog Service** (`src/services/blogService.js`)
- ✅ Get blogs with pagination & filters
- ✅ Get blog by ID/slug
- ✅ Create/Update/Delete blogs
- ✅ Blog comments (CRUD)
- ✅ Blog categories (CRUD)

#### 7. **Supplier Services** (`src/supplier/services/`)
- ✅ Product service (uses main product API)
- ✅ Order service (uses main order API)
- ✅ Banner service (uses main banner API)
- ✅ Blog service (uses main blog API)
- **Note**: Backend handles supplier filtering automatically

### API Client Configuration

**File**: `src/services/apiClient.js`

Features:
- ✅ Axios instance with base URL
- ✅ Request interceptor for JWT token
- ✅ Response interceptor for token refresh
- ✅ Automatic retry on 401 errors
- ✅ Auto logout on refresh failure

### Central Export

**File**: `src/services/index.js`

All services exported from single file for easy imports:
```javascript
import { login, register, getProfile } from '@/services';
```

## API Endpoints Used

### Base URL
```
http://localhost:8000/api/v1/
```

### Authentication
- POST `/auth/register/`
- POST `/auth/login/`
- POST `/auth/logout/`
- POST `/auth/token/refresh/`
- GET `/auth/profile/`
- POST `/auth/change-password/`
- POST `/auth/password-reset/`

### Products
- GET `/products/` (with pagination, search, filters)
- GET `/products/{id}/`
- GET `/products/search/?q=query`
- POST `/products/`
- PUT `/products/{id}/`
- DELETE `/products/{id}/`
- GET `/products/{id}/attributes/`
- GET `/products/{id}/specifications/`
- GET `/products/{id}/reviews/`

### Home/Homepage
- GET `/homepage/` (complete homepage data)
- GET `/banners/`
- GET `/banners/header_banners/`
- GET `/banners/middle_banners/`
- GET `/facilities/`
- GET `/category/{category_name}/`
- GET `/category/{category_name}/{product_slug}/`

### Cart & Wishlist
- GET `/cart/`
- POST `/cart/`
- PUT `/cart/{id}/`
- DELETE `/cart/{id}/`
- GET `/wishlist/`
- POST `/wishlist/`
- DELETE `/wishlist/{id}/`
- GET `/cart-wishlist-stats/`

### Orders
- GET `/orders/`
- GET `/orders/{id}/`
- POST `/orders/`
- POST `/checkout/`
- POST `/payment/`
- GET `/order-tracking/?order_id=123`
- GET `/returns-replacements/`

### Blogs
- GET `/blogs/`
- GET `/blogs/{id}/`
- GET `/blogs/slug/{slug}/`
- POST `/blogs/`
- GET `/blogs/{id}/comments/`
- POST `/blogs/{id}/comments/`

### Categories
- GET `/categories/`
- GET `/categories/{id}/`

## Authentication Flow

### 1. Registration
```javascript
import { register } from '@/services';

const userData = {
  email: 'user@example.com',
  password: 'password123',
  password_confirm: 'password123',
  first_name: 'John',
  last_name: 'Doe',
  mobile_no: '1234567890',
  user_role_id: 2 // 1=admin, 2=supplier, 3=customer
};

const response = await register(userData);
// Response: { user, tokens: { access, refresh } }
```

### 2. Login
```javascript
import { login } from '@/services';

const response = await login('user@example.com', 'password123');
// Response: { user, tokens: { access, refresh } }

// Store tokens
localStorage.setItem('access_token', response.tokens.access);
localStorage.setItem('refresh_token', response.tokens.refresh);
```

### 3. Token Refresh (Automatic)
The API client automatically refreshes tokens on 401 errors.

### 4. Logout
```javascript
import { logout } from '@/services';

const refreshToken = localStorage.getItem('refresh_token');
await logout(refreshToken);

// Clear tokens
localStorage.removeItem('access_token');
localStorage.removeItem('refresh_token');
```

## Usage Examples

### Get Homepage Data
```javascript
import { getHomePageData } from '@/services';

const data = await getHomePageData();
// Returns: banners, products, categories, blogs, facilities
```

### Get Products with Filters
```javascript
import { getProducts } from '@/services';

const products = await getProducts({
  page: 1,
  search: 'laptop',
  category: 5,
  min_price: 100,
  max_price: 1000
});
```

### Add to Cart
```javascript
import { addToCart } from '@/services';

const cartItem = await addToCart(productId, quantity);
```

### Create Order
```javascript
import { processCheckout } from '@/services';

const checkoutData = {
  address: addressId,
  payment_method: 'stripe',
  items: cartItems
};

const order = await processCheckout(checkoutData);
```

### Supplier: Get Products
```javascript
import { getProducts } from '@/supplier/services/productService';

// Backend automatically filters by supplier user
const products = await getProducts(1, 'search query');
```

## Error Handling

All services include try-catch blocks and throw errors for handling in components:

```javascript
try {
  const products = await getProducts();
  // Handle success
} catch (error) {
  // Handle error
  console.error('Error:', error.response?.data || error.message);
}
```

## Next Steps

### Frontend Integration Tasks:

1. **Update HomePage.jsx**
   - Replace mock data with `getHomePageData()`
   - Use real banners, products, categories

2. **Update ProductListPage.jsx**
   - Use `getProducts()` with filters
   - Implement pagination

3. **Update ProductDetailPage.jsx**
   - Use `getProductDetail()` for complete data
   - Implement reviews with `getProductReviews()`

4. **Update CartContext.jsx**
   - Use cart service functions
   - Sync with backend

5. **Update AuthContext.jsx**
   - Use auth service functions
   - Handle token refresh

6. **Update Supplier Pages**
   - Already using correct services
   - Just need to handle responses properly

7. **Add Loading States**
   - Show spinners during API calls
   - Handle loading in all pages

8. **Add Error Handling**
   - Toast notifications for errors
   - User-friendly error messages

9. **Add Success Messages**
   - Toast notifications for success
   - Confirmation messages

10. **Test All Flows**
    - Registration → Login → Browse → Add to Cart → Checkout
    - Supplier: Login → Manage Products → View Orders

## Important Notes

- ✅ All services use correct Django DRF endpoints
- ✅ No mock/dummy data in services
- ✅ Proper error handling in all functions
- ✅ Multipart form data for file uploads
- ✅ JWT token handling in API client
- ✅ Automatic token refresh
- ✅ Supplier filtering handled by backend
- ✅ Pagination support
- ✅ Search and filter support
- ✅ CRUD operations for all resources

## Environment Variables

Create `.env` file in frontend root:

```env
VITE_API_BASE_URL=http://localhost:8000/api/v1
```

## Testing APIs

Use the Swagger documentation:
```
http://localhost:8000/api/docs/
```

All endpoints are documented with request/response examples.
