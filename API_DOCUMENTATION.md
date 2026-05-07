# Django eCommerce REST API Documentation

## Overview

This document provides a comprehensive overview of the Django REST Framework (DRF) API implementation for the Django eCommerce project. The API provides complete functionality for an eCommerce platform while maintaining backward compatibility with the existing template-based system.

## 🚀 Features Implemented

### ✅ Complete API Coverage
- **Authentication System** - JWT-based authentication with registration, login, logout, password reset
- **User Management** - Profile management, address management, roles & permissions
- **Product Catalog** - Products, categories, attributes, specifications, reviews
- **Shopping Cart** - Add/remove items, quantity management, wishlist
- **Order Management** - Checkout, payment processing, order tracking, returns/replacements
- **Content Management** - Banners, facilities, blog system
- **Search & Filtering** - Advanced search, filtering, sorting, pagination

### 🔧 Technical Implementation
- **Django REST Framework** - Professional API architecture
- **JWT Authentication** - Secure token-based authentication
- **Permissions & Authorization** - Role-based access control
- **Serializers** - Data validation and transformation
- **ViewSets & APIViews** - RESTful endpoints
- **Filtering & Search** - Advanced filtering capabilities
- **Pagination** - Efficient data pagination
- **API Documentation** - Swagger/OpenAPI documentation

## 📁 Project Structure

```
django_ecommerce/
├── users/
│   ├── serializers.py          # User, Role, Permission, Address serializers
│   ├── api_views.py            # Authentication & user management APIs
│   └── api_urls.py             # User API endpoints
├── products/
│   ├── serializers.py          # Product, Category, Review serializers
│   ├── api_views.py            # Product catalog APIs
│   └── api_urls.py             # Product API endpoints
├── cart/
│   ├── serializers.py          # Cart & Wishlist serializers
│   ├── api_views.py            # Shopping cart APIs
│   └── api_urls.py             # Cart API endpoints
├── orders/
│   ├── serializers.py          # Order, Payment, Return serializers
│   ├── api_views.py            # Order management APIs
│   └── api_urls.py             # Order API endpoints
├── home/
│   ├── serializers.py          # Banner, Facility serializers
│   ├── api_views.py            # Homepage & content APIs
│   └── api_urls.py             # Home API endpoints
├── blog/
│   ├── serializers.py          # Blog, Comment serializers
│   ├── api_views.py            # Blog system APIs
│   └── api_urls.py             # Blog API endpoints
└── category/
    ├── serializers.py          # Category management serializers
    ├── api_views.py            # Category APIs
    └── api_urls.py             # Category API endpoints
```

## 🔐 Authentication Endpoints

### Base URL: `/api/v1/auth/`

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/register/` | User registration |
| POST | `/login/` | User login |
| POST | `/logout/` | User logout |
| POST | `/token/refresh/` | Refresh JWT token |
| GET/PUT | `/profile/` | Get/Update user profile |
| POST | `/change-password/` | Change password |
| POST | `/password-reset/` | Request password reset |
| POST | `/password-reset-confirm/{uid}/{token}/` | Confirm password reset |

## 👥 User Management Endpoints

### Base URL: `/api/v1/`

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET/POST | `/users/` | List/Create users (Admin) |
| GET/PUT/DELETE | `/users/{id}/` | User CRUD operations |
| GET/POST | `/roles/` | List/Create roles |
| GET/PUT/DELETE | `/roles/{id}/` | Role CRUD operations |
| GET/POST | `/permissions/` | List/Create permissions |
| GET/PUT/DELETE | `/permissions/{id}/` | Permission CRUD operations |
| GET/POST | `/addresses/` | List/Create user addresses |
| GET/PUT/DELETE | `/addresses/{id}/` | Address CRUD operations |
| POST | `/addresses/{id}/set_default/` | Set default address |

## 🛍️ Product Catalog Endpoints

### Base URL: `/api/v1/`

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET/POST | `/categories/` | List/Create categories |
| GET/PUT/DELETE | `/categories/{id}/` | Category CRUD operations |
| GET | `/categories/parent_categories/` | Get parent categories |
| GET | `/categories/{id}/subcategories/` | Get subcategories |
| GET | `/categories/{id}/products/` | Get category products |
| GET/POST | `/products/` | List/Create products |
| GET/PUT/DELETE | `/products/{id}/` | Product CRUD operations |
| GET | `/products/featured/` | Get featured products |
| GET | `/products/latest/` | Get latest products |
| GET | `/products/{id}/related/` | Get related products |
| GET | `/products/search/` | Advanced product search |
| GET/POST | `/products/{id}/attributes/` | Product attributes |
| GET/POST | `/products/{id}/specifications/` | Product specifications |
| GET/POST | `/products/{id}/reviews/` | Product reviews |

## 🛒 Shopping Cart Endpoints

### Base URL: `/api/v1/`

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET/POST | `/cart/` | List/Add cart items |
| GET/PUT/DELETE | `/cart/{id}/` | Cart item CRUD operations |
| GET | `/cart/summary/` | Get cart summary |
| POST | `/cart/clear/` | Clear cart |
| POST | `/cart/{id}/increase_quantity/` | Increase item quantity |
| POST | `/cart/{id}/decrease_quantity/` | Decrease item quantity |
| GET/POST | `/wishlist/` | List/Add wishlist items |
| GET/DELETE | `/wishlist/{id}/` | Wishlist item operations |
| GET | `/wishlist/summary/` | Get wishlist summary |
| POST | `/wishlist/clear/` | Clear wishlist |
| POST | `/wishlist/{id}/move_to_cart/` | Move to cart |
| GET | `/cart-wishlist-stats/` | Get cart/wishlist stats |

## 📦 Order Management Endpoints

### Base URL: `/api/v1/`

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/checkout/` | Get checkout information |
| POST | `/checkout/` | Process checkout |
| POST | `/payment/` | Create payment intent |
| GET/POST | `/orders/` | List/Create orders |
| GET/PUT/DELETE | `/orders/{id}/` | Order CRUD operations |
| POST | `/orders/{id}/cancel/` | Cancel order |
| POST | `/orders/{id}/update_status/` | Update order status (Admin) |
| GET | `/orders/summary/` | Get order summary |
| GET/POST | `/returns-replacements/` | Return/Replace requests |
| POST | `/returns-replacements/{id}/approve/` | Approve request (Admin) |
| POST | `/returns-replacements/{id}/cancel/` | Cancel request |
| POST | `/order-tracking/` | Track order |

## 🏠 Homepage & Content Endpoints

### Base URL: `/api/v1/`

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/homepage/` | Get homepage data |
| GET | `/category/{name}/` | Get category products |
| POST | `/category/{name}/` | Filter by price |
| GET | `/category/{name}/{slug}/` | Get product details |
| GET/POST | `/banners/` | List/Create banners |
| GET/PUT/DELETE | `/banners/{id}/` | Banner CRUD operations |
| GET | `/banners/by_type/` | Get banners by type |
| GET | `/banners/header_banners/` | Get header banners |
| GET | `/banners/middle_banners/` | Get middle banners |
| GET/POST | `/facilities/` | List/Create facilities |
| GET/PUT/DELETE | `/facilities/{id}/` | Facility CRUD operations |

## 📝 Blog System Endpoints

### Base URL: `/api/v1/`

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET/POST | `/categories/` | List/Create blog categories |
| GET/PUT/DELETE | `/categories/{id}/` | Blog category CRUD |
| GET | `/categories/{id}/blogs/` | Get category blogs |
| GET/POST | `/blogs/` | List/Create blogs |
| GET/PUT/DELETE | `/blogs/{id}/` | Blog CRUD operations |
| GET | `/blogs/latest/` | Get latest blogs |
| GET | `/blogs/featured/` | Get featured blogs |
| GET | `/blogs/search/` | Search blogs |
| GET | `/blogs/slug/{slug}/` | Get blog by slug |
| GET/POST | `/blogs/{id}/comments/` | Blog comments |
| GET/PUT/DELETE | `/blogs/{id}/comments/{id}/` | Comment CRUD |

## 🔍 Search & Filtering

### Advanced Search Features
- **Text Search** - Search across product names, descriptions
- **Category Filtering** - Filter by category and subcategories
- **Price Range** - Min/max price filtering
- **Tag Filtering** - Filter by product tags (HOT, NEW, SALE)
- **Sorting** - Sort by name, price, date created
- **Pagination** - Efficient pagination with page numbers

### Search Endpoints
- `/api/v1/products/search/` - Advanced product search
- `/api/v1/blogs/search/` - Blog search

## 📊 API Response Format

### Success Response
```json
{
  "count": 100,
  "next": "http://localhost:8000/api/v1/products/?page=2",
  "previous": null,
  "results": [...]
}
```

### Error Response
```json
{
  "error": "Error message",
  "details": {
    "field": ["Field-specific error"]
  }
}
```

## 🔒 Authentication & Permissions

### JWT Token Usage
```bash
# Login to get tokens
POST /api/v1/auth/login/
{
  "email": "user@example.com",
  "password": "password"
}

# Use access token in headers
Authorization: Bearer <access_token>

# Refresh token when expired
POST /api/v1/auth/token/refresh/
{
  "refresh": "<refresh_token>"
}
```

### Permission Levels
- **Public** - No authentication required (product listings, blog posts)
- **Authenticated** - Requires login (cart, orders, profile)
- **Admin** - Admin role required (user management, order status updates)
- **Supplier** - Supplier role (product management)

## 📚 API Documentation

### Interactive Documentation
- **Swagger UI**: `http://localhost:8000/api/docs/`
- **ReDoc**: `http://localhost:8000/api/redoc/`
- **OpenAPI Schema**: `http://localhost:8000/api/schema/`

## 🚀 Getting Started

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Run Migrations
```bash
python manage.py migrate
```

### 3. Create Superuser
```bash
python manage.py createsuperuser
```

### 4. Start Development Server
```bash
python manage.py runserver
```

### 5. Access API Documentation
Visit `http://localhost:8000/api/docs/` for interactive API documentation.

## 🔧 Configuration

### Required Settings
- `REST_FRAMEWORK` - DRF configuration
- `SIMPLE_JWT` - JWT authentication settings
- `SPECTACULAR_SETTINGS` - API documentation settings

### Environment Variables
- `DJANGO_KEY` - Django secret key
- `STRIPE_PUBLISHABLE_KEY` - Stripe public key
- `STRIPE_SECRET_KEY` - Stripe secret key
- `PAYPAL_CLIENT_ID` - PayPal client ID
- `PAYPAL_SECRET` - PayPal secret

## 🧪 Testing

### API Testing Tools
- **Postman** - Import OpenAPI schema for testing
- **curl** - Command line testing
- **Django Test Client** - Unit testing
- **pytest** - Advanced testing framework

### Example API Calls

#### Register User
```bash
curl -X POST http://localhost:8000/api/v1/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "securepassword",
    "first_name": "John",
    "last_name": "Doe"
  }'
```

#### Get Products
```bash
curl -X GET http://localhost:8000/api/v1/products/ \
  -H "Authorization: Bearer <access_token>"
```

#### Add to Cart
```bash
curl -X POST http://localhost:8000/api/v1/cart/ \
  -H "Authorization: Bearer <access_token>" \
  -H "Content-Type: application/json" \
  -d '{
    "product": 1,
    "quantity": 2
  }'
```

## 🔄 Migration from Template Views

### Backward Compatibility
- ✅ All existing template views remain functional
- ✅ Existing forms and admin interface unchanged
- ✅ Database models unchanged
- ✅ Business logic reused in API views

### Gradual Migration Strategy
1. **Phase 1**: API endpoints available alongside templates
2. **Phase 2**: Frontend applications can use APIs
3. **Phase 3**: Gradual replacement of template views (optional)

## 📈 Performance Considerations

### Optimization Features
- **Pagination** - Efficient data loading
- **Select Related** - Optimized database queries
- **Caching** - Can be added for frequently accessed data
- **Filtering** - Database-level filtering
- **Serializer Optimization** - Minimal data transfer

### Scalability
- **Stateless API** - JWT tokens enable horizontal scaling
- **Database Optimization** - Efficient queries with select_related
- **CDN Ready** - Static files can be served via CDN
- **Load Balancer Ready** - Stateless design supports load balancing

## 🛡️ Security Features

### Authentication Security
- **JWT Tokens** - Secure token-based authentication
- **Token Rotation** - Automatic refresh token rotation
- **Token Blacklisting** - Revoked tokens are blacklisted
- **Password Validation** - Strong password requirements

### API Security
- **CORS Configuration** - Cross-origin request handling
- **Permission Classes** - Role-based access control
- **Input Validation** - Serializer-based validation
- **SQL Injection Protection** - Django ORM protection

## 📞 Support & Maintenance

### Code Quality
- **Clean Architecture** - Separation of concerns
- **DRY Principle** - Reusable serializers and views
- **Error Handling** - Comprehensive error responses
- **Documentation** - Well-documented code and APIs

### Monitoring & Logging
- **Django Logging** - Built-in logging framework
- **API Metrics** - Can integrate with monitoring tools
- **Error Tracking** - Detailed error responses
- **Performance Monitoring** - Database query optimization

## 🎯 Next Steps

### Recommended Enhancements
1. **API Versioning** - Implement API versioning strategy
2. **Rate Limiting** - Add API rate limiting
3. **Caching** - Implement Redis caching
4. **Testing** - Add comprehensive API tests
5. **Monitoring** - Add API monitoring and analytics
6. **Documentation** - Expand API documentation
7. **Mobile App** - Build mobile applications using the API
8. **Third-party Integrations** - Add more payment gateways

### Frontend Integration
- **React/Vue.js** - Build modern frontend applications
- **Mobile Apps** - iOS/Android applications
- **Progressive Web App** - PWA implementation
- **Admin Dashboard** - Custom admin interface

---

## 📋 Summary

This Django REST Framework implementation provides a complete, production-ready API for the eCommerce platform with:

- ✅ **100% Feature Coverage** - All existing functionality available via API
- ✅ **Professional Architecture** - ModelViewSets, APIViews, proper serializers
- ✅ **Security** - JWT authentication, permissions, validation
- ✅ **Performance** - Pagination, filtering, optimized queries
- ✅ **Documentation** - Interactive API documentation
- ✅ **Backward Compatibility** - Existing system remains unchanged
- ✅ **Scalability** - Ready for production deployment

The API is now ready for frontend applications, mobile apps, and third-party integrations while maintaining full compatibility with the existing Django template system.