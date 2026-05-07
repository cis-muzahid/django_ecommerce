# Django eCommerce API Setup Guide

## 🚀 Quick Start

### 1. Install Dependencies

```bash
# Install required packages
pip install -r requirements.txt
```

### 2. Environment Setup

Create a `.env` file in the project root with:

```env
DJANGO_KEY=your-secret-key-here
STRIPE_PUBLISHABLE_KEY=pk_test_your_stripe_key
STRIPE_SECRET_KEY=sk_test_your_stripe_key
PAYPAL_CLIENT_ID=your_paypal_client_id
PAYPAL_SECRET=your_paypal_secret
TRACKING_SECRET=your_tracking_secret
BACKEND_DOMAIN=http://localhost:8000
PAYMENT_SUCCESS_URL=http://localhost:8000/success
PAYMENT_CANCEL_URL=http://localhost:8000/cancel
```

### 3. Database Setup

```bash
# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser
```

### 4. Start Development Server

```bash
python manage.py runserver
```

### 5. Access API Documentation

- **Swagger UI**: http://localhost:8000/api/docs/
- **ReDoc**: http://localhost:8000/api/redoc/
- **Admin Panel**: http://localhost:8000/admin/

## 📦 Dependencies Added

The following packages have been added to `requirements.txt`:

```
djangorestframework
djangorestframework-simplejwt
django-filter
drf-spectacular
drf-nested-routers
```

## 🔧 Configuration Changes

### Settings Updated

1. **INSTALLED_APPS** - Added DRF packages
2. **REST_FRAMEWORK** - DRF configuration
3. **SIMPLE_JWT** - JWT authentication settings
4. **SPECTACULAR_SETTINGS** - API documentation

### URLs Updated

- Added API endpoints under `/api/v1/`
- Added documentation endpoints

## 🧪 Testing the API

### 1. Register a User

```bash
curl -X POST http://localhost:8000/api/v1/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "testpassword123",
    "first_name": "Test",
    "last_name": "User"
  }'
```

### 2. Login

```bash
curl -X POST http://localhost:8000/api/v1/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "testpassword123"
  }'
```

### 3. Get Products

```bash
curl -X GET http://localhost:8000/api/v1/products/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

## 🔍 Verification Checklist

- [ ] Dependencies installed successfully
- [ ] Migrations run without errors
- [ ] Server starts without issues
- [ ] API documentation accessible
- [ ] User registration works
- [ ] JWT authentication works
- [ ] Product endpoints accessible
- [ ] Cart functionality works
- [ ] Order creation works

## 🛠️ Troubleshooting

### Common Issues

1. **Import Errors**
   - Ensure all dependencies are installed
   - Check Python path and virtual environment

2. **Migration Errors**
   - Delete migration files and recreate if needed
   - Check database connectivity

3. **JWT Token Issues**
   - Verify SECRET_KEY is set
   - Check token expiration settings

4. **Permission Errors**
   - Ensure user has proper roles
   - Check permission classes in views

## 📚 Next Steps

1. **Explore API Documentation** - Visit `/api/docs/` for interactive docs
2. **Test Endpoints** - Use Postman or curl to test API endpoints
3. **Build Frontend** - Create React/Vue.js frontend using the API
4. **Mobile Development** - Build mobile apps using the API
5. **Customize** - Modify serializers and views as needed

## 🔗 Useful Links

- [Django REST Framework Documentation](https://www.django-rest-framework.org/)
- [JWT Authentication](https://django-rest-framework-simplejwt.readthedocs.io/)
- [API Documentation](https://drf-spectacular.readthedocs.io/)
- [Django Filters](https://django-filter.readthedocs.io/)

## Support

If you encounter any issues:

1. Check the error logs
2. Verify all dependencies are installed
3. Ensure environment variables are set
4. Check the API documentation for correct usage
5. Review the Django and DRF documentation

---

**🎉 Congratulations! Your Django eCommerce API is now ready for development.**