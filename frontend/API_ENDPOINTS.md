# Django DRF API Endpoints Documentation

## Base URL
```
http://localhost:8000/api/v1/
```

## Authentication Endpoints

### Register
- **POST** `/auth/register/`
- **Body**: `{ email, password, password_confirm, first_name, last_name, mobile_no, user_role_id }`
- **Response**: `{ user, tokens: { access, refresh } }`

### Login
- **POST** `/auth/login/`
- **Body**: `{ email, password }`
- **Response**: `{ user, tokens: { access, refresh } }`

### Logout
- **POST** `/auth/logout/`
- **Headers**: `Authorization: Bearer <access_token>`
- **Body**: `{ refresh_token }`

### Token Refresh
- **POST** `/auth/token/refresh/`
- **Body**: `{ refresh }`
- **Response**: `{ access }`

### Profile
- **GET** `/auth/profile/`
- **Headers**: `Authorization: Bearer <access_token>`
- **Response**: `{ id, email, first_name, last_name, mobile_no, user_role }`

### Change Password
- **POST** `/auth/change-password/`
- **Headers**: `Authorization: Bearer <access_token>`
- **Body**: `{ old_password, new_password }`

## Home/Homepage Endpoints

### Homepage Data
- **GET** `/homepage/`
- **Response**: 
```json
{
  "banners": {
    "header_banners": [],
    "wide_banner_large": {},
    "wide_banner_small": {},
    "middle_banners": []
  },
  "latest_products": [],
  "special_offers": {
    "products_1": [],
    "products_2": [],
    "products_3": []
  },
  "hot_deals": [],
  "categories": [],
  "blogs": [],
  "facilities": []
}
```

### Banners
- **GET** `/banners/` - List all banners
- **GET** `/banners/{id}/` - Get banner detail
- **GET** `/banners/header_banners/` - Get header banners
- **GET** `/banners/middle_banners/` - Get middle banners
- **GET** `/banners/by_type/` - Get banners grouped by type
- **POST** `/banners/` - Create banner (Auth required)
- **PUT** `/banners/{id}/` - Update banner (Auth required)
- **DELETE** `/banners/{id}/` - Delete banner (Auth required)

### Facilities
- **GET** `/facilities/` - List all facilities
- **GET** `/facilities/{id}/` - Get facility detail
- **POST** `/facilities/` - Create facility (Auth required)
- **PUT** `/facilities/{id}/` - Update facility (Auth required)
- **DELETE** `/facilities/{id}/` - Delete facility (Auth required)

## Product Endpoints

### Products
- **GET** `/products/` - List all products
  - Query params: `?page=1&search=query&category=id&min_price=0&max_price=1000`
- **GET** `/products/{id}/` - Get product detail
- **GET** `/products/search/` - Search products
  - Query params: `?q=search_term`
- **POST** `/products/` - Create product (Auth required)
- **PUT** `/products/{id}/` - Update product (Auth required)
- **DELETE** `/products/{id}/` - Delete product (Auth required)

### Product Attributes
- **GET** `/products/{product_id}/attributes/` - List product attributes
- **POST** `/products/{product_id}/attributes/` - Create attribute
- **PUT** `/products/{product_id}/attributes/{id}/` - Update attribute
- **DELETE** `/products/{product_id}/attributes/{id}/` - Delete attribute

### Product Specifications
- **GET** `/products/{product_id}/specifications/` - List product specifications
- **POST** `/products/{product_id}/specifications/` - Create specification
- **PUT** `/products/{product_id}/specifications/{id}/` - Update specification
- **DELETE** `/products/{product_id}/specifications/{id}/` - Delete specification

### Product Reviews
- **GET** `/products/{product_id}/reviews/` - List product reviews
- **POST** `/products/{product_id}/reviews/` - Create review (Auth required)
- **PUT** `/products/{product_id}/reviews/{id}/` - Update review (Auth required)
- **DELETE** `/products/{product_id}/reviews/{id}/` - Delete review (Auth required)

### Category Products
- **GET** `/category/{category_name}/` - Get products by category
  - Query params: `?min_price=0&max_price=1000&search=query`
- **POST** `/category/{category_name}/` - Filter by price range
  - Body: `{ price: "min,max" }`

### Product Detail
- **GET** `/category/{category_name}/{product_slug}/` - Get product detail with related data

## Category Endpoints

### Categories
- **GET** `/categories/` - List all categories
- **GET** `/categories/{id}/` - Get category detail
- **POST** `/categories/` - Create category (Auth required)
- **PUT** `/categories/{id}/` - Update category (Auth required)
- **DELETE** `/categories/{id}/` - Delete category (Auth required)

## Cart Endpoints

### Cart
- **GET** `/cart/` - Get user's cart items (Auth required)
- **POST** `/cart/` - Add item to cart (Auth required)
  - Body: `{ product, quantity }`
- **PUT** `/cart/{id}/` - Update cart item (Auth required)
  - Body: `{ quantity }`
- **DELETE** `/cart/{id}/` - Remove item from cart (Auth required)
- **DELETE** `/cart/clear/` - Clear all cart items (Auth required)

### Wishlist
- **GET** `/wishlist/` - Get user's wishlist (Auth required)
- **POST** `/wishlist/` - Add item to wishlist (Auth required)
  - Body: `{ product }`
- **DELETE** `/wishlist/{id}/` - Remove item from wishlist (Auth required)

### Cart/Wishlist Stats
- **GET** `/cart-wishlist-stats/` - Get cart and wishlist counts (Auth required)
- **Response**: `{ cart_count, wishlist_count }`

## Order Endpoints

### Orders
- **GET** `/orders/` - List user's orders (Auth required)
- **GET** `/orders/{id}/` - Get order detail (Auth required)
- **POST** `/orders/` - Create order (Auth required)
- **PUT** `/orders/{id}/` - Update order (Auth required)

### Checkout
- **POST** `/checkout/` - Process checkout (Auth required)
- **Body**: `{ address, payment_method, items }`

### Payment
- **POST** `/payment/` - Process payment (Auth required)
- **Body**: `{ order_id, payment_method, amount }`

### Order Tracking
- **GET** `/order-tracking/` - Track order (Auth required)
  - Query params: `?order_id=123`

### Returns & Replacements
- **GET** `/returns-replacements/` - List return/replace requests (Auth required)
- **POST** `/returns-replacements/` - Create return/replace request (Auth required)
- **PUT** `/returns-replacements/{id}/` - Update request (Auth required)

## Blog Endpoints

### Blog Categories
- **GET** `/categories/` - List blog categories
- **GET** `/categories/{id}/` - Get blog category detail
- **POST** `/categories/` - Create blog category (Auth required)
- **PUT** `/categories/{id}/` - Update blog category (Auth required)
- **DELETE** `/categories/{id}/` - Delete blog category (Auth required)

### Blogs
- **GET** `/blogs/` - List all blogs
  - Query params: `?page=1&search=query&category=id`
- **GET** `/blogs/{id}/` - Get blog detail
- **GET** `/blogs/slug/{slug}/` - Get blog by slug
- **POST** `/blogs/` - Create blog (Auth required)
- **PUT** `/blogs/{id}/` - Update blog (Auth required)
- **DELETE** `/blogs/{id}/` - Delete blog (Auth required)

### Blog Comments
- **GET** `/blogs/{blog_id}/comments/` - List blog comments
- **POST** `/blogs/{blog_id}/comments/` - Create comment (Auth required)
- **PUT** `/blogs/{blog_id}/comments/{id}/` - Update comment (Auth required)
- **DELETE** `/blogs/{blog_id}/comments/{id}/` - Delete comment (Auth required)

## User Management Endpoints (Admin/Supplier)

### Users
- **GET** `/users/` - List all users (Admin only)
- **GET** `/users/{id}/` - Get user detail (Admin only)
- **PUT** `/users/{id}/` - Update user (Admin only)
- **DELETE** `/users/{id}/` - Delete user (Admin only)

### Roles
- **GET** `/roles/` - List all roles
- **GET** `/roles/{id}/` - Get role detail
- **POST** `/roles/` - Create role (Admin only)
- **PUT** `/roles/{id}/` - Update role (Admin only)
- **DELETE** `/roles/{id}/` - Delete role (Admin only)

### Permissions
- **GET** `/permissions/` - List all permissions
- **GET** `/permissions/{id}/` - Get permission detail
- **POST** `/permissions/` - Create permission (Admin only)
- **PUT** `/permissions/{id}/` - Update permission (Admin only)
- **DELETE** `/permissions/{id}/` - Delete permission (Admin only)

### User Addresses
- **GET** `/addresses/` - List user addresses (Auth required)
- **GET** `/addresses/{id}/` - Get address detail (Auth required)
- **POST** `/addresses/` - Create address (Auth required)
- **PUT** `/addresses/{id}/` - Update address (Auth required)
- **DELETE** `/addresses/{id}/` - Delete address (Auth required)

## Response Format

### Success Response
```json
{
  "data": {},
  "message": "Success message"
}
```

### Error Response
```json
{
  "error": "Error message",
  "details": {}
}
```

### Paginated Response
```json
{
  "count": 100,
  "next": "http://api.example.com/api/v1/products/?page=2",
  "previous": null,
  "results": []
}
```

## Authentication

All authenticated endpoints require JWT token in header:
```
Authorization: Bearer <access_token>
```

## Media URLs

All image URLs are relative to media root:
```
http://localhost:8000/media/{image_path}
```
