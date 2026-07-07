import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import MainLayout from './components/MainLayout.jsx';
import HomePage from './pages/HomePage.jsx';
import LoginPage from './pages/LoginPage.jsx';
import SignupPage from './pages/SignupPage.jsx';
import ProductListPage from './pages/ProductListPage.jsx';
import ProductDetailPage from './pages/ProductDetailPage.jsx';
import CategoryPage from './pages/CategoryPage.jsx';
import CartPage from './pages/CartPage.jsx';
import WishlistPage from './pages/WishlistPage.jsx';
import CheckoutPage from './pages/CheckoutPage.jsx';
import OrdersPage from './pages/OrdersPage.jsx';
import OrderTrackingPage from './pages/OrderTrackingPage.jsx';
import OrderConfirmationPage from './pages/OrderConfirmationPage.jsx';
import PayPalReturnPage from './pages/PayPalReturnPage.jsx';
import PayPalCancelPage from './pages/PayPalCancelPage.jsx';
import ProfilePage from './pages/ProfilePage.jsx';
import UserReviewsPage from './pages/UserReviewsPage.jsx';
import BlogListPage from './pages/BlogListPage.jsx';
import BlogDetailPage from './pages/BlogDetailPage.jsx';
import SearchPage from './pages/SearchPage.jsx';
import AboutPage from './pages/AboutPage.jsx';
import ContactPage from './pages/ContactPage.jsx';
import PolicyPage from './pages/PolicyPage.jsx';
import NotFoundPage from './pages/NotFoundPage.jsx';
import { supplierRoutes } from './supplier/routes/supplierRoutes.jsx';

export default function App() {
  return (
    <Router>
      <Routes>
        {/* Auth routes - outside layout */}
        <Route path="/login" element={<LoginPage />} />
        <Route path="/login_user" element={<LoginPage />} />
        <Route path="/login_user/" element={<LoginPage />} />
        <Route path="/signup" element={<SignupPage />} />
        <Route path="/signup_user" element={<SignupPage />} />
        <Route path="/signup_user/" element={<SignupPage />} />
        
        {/* Payment return routes - outside layout for direct handling */}
        <Route path="/payment-success/paypal" element={<PayPalReturnPage />} />
        <Route path="/payment-cancel" element={<PayPalCancelPage />} />

        {/* Supplier dashboard - separate from storefront chrome */}
        {supplierRoutes}

        {/* Storefront routes with shared MainLayout */}
        <Route element={<MainLayout />}>
          <Route path="/" element={<HomePage />} />
          <Route path="/products" element={<ProductListPage />} />
          <Route path="/product/:slug" element={<ProductDetailPage />} />
          <Route path="/category/:categoryName" element={<CategoryPage />} />
          <Route path="/category/:categoryName/:slug" element={<ProductDetailPage />} />
          <Route
            path="/category/:parentCategory/:childCategory/:slug"
            element={<ProductDetailPage />}
          />
          <Route path="/cart" element={<CartPage />} />
          <Route path="/my_cart" element={<CartPage />} />
          <Route path="/my_cart/" element={<CartPage />} />
          <Route path="/wishlist" element={<WishlistPage />} />
          <Route path="/my_wishlist" element={<WishlistPage />} />
          <Route path="/my_wishlist/" element={<WishlistPage />} />
          <Route path="/checkout" element={<CheckoutPage />} />
          <Route path="/orders" element={<OrdersPage />} />
          <Route path="/orders/tracking" element={<OrderTrackingPage />} />
          <Route path="/order_tracking" element={<OrderTrackingPage />} />
          <Route path="/order_tracking/" element={<OrderTrackingPage />} />
          <Route path="/profile" element={<ProfilePage />} />
          <Route path="/user_profile" element={<ProfilePage />} />
          <Route path="/user_profile/" element={<ProfilePage />} />
          <Route path="/user_review" element={<UserReviewsPage />} />
          <Route path="/user_review/" element={<UserReviewsPage />} />
          <Route path="/blogs" element={<BlogListPage />} />
          <Route path="/user/blogs" element={<BlogListPage />} />
          <Route path="/user/blogs/:categoryId" element={<BlogListPage />} />
          <Route path="/blog/:slug" element={<BlogDetailPage />} />
          <Route path="/user/blog/:id" element={<BlogDetailPage />} />
          <Route path="/search" element={<SearchPage />} />
          <Route path="/about" element={<AboutPage />} />
          <Route path="/contact" element={<ContactPage />} />
          <Route path="/faq" element={<PolicyPage type="faq" />} />
          <Route path="/terms" element={<PolicyPage type="terms" />} />
          <Route path="/privacy" element={<PolicyPage type="privacy" />} />
          <Route path="/returns" element={<PolicyPage type="returns" />} />
          <Route path="/refund-policy" element={<PolicyPage type="returns" />} />
          <Route path="/shipping" element={<PolicyPage type="shipping" />} />
          <Route path="/shipping-policy" element={<PolicyPage type="shipping" />} />
          <Route path="/order-confirmation/:orderId" element={<OrderConfirmationPage />} />
          <Route path="*" element={<NotFoundPage />} />
        </Route>
      </Routes>
    </Router>
  );
}
