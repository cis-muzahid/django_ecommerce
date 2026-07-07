import { Route } from 'react-router-dom';
import SupplierLayout from '../layouts/SupplierLayout';
import ProductsPage from '../pages/ProductsPage';
import ProductFormPage from '../pages/ProductFormPage';
import ProductDetailPage from '../pages/ProductDetailPage';
import OrdersPage from '../pages/OrdersPage';
import OrderDetailPage from '../pages/OrderDetailPage';
import ReturnsPage from '../pages/ReturnsPage';
import BannersPage from '../pages/BannersPage';
import BlogsPage from '../pages/BlogsPage';
import ProtectedRoute from '../../components/ProtectedRoute';

export const supplierRoutes = (
  <Route
    path="/supplier"
    element={
      <ProtectedRoute requiredRole="supplier">
        <SupplierLayout />
      </ProtectedRoute>
    }
  >
    <Route index element={<ProductsPage />} />
    <Route path="products" element={<ProductsPage />} />
    <Route path="products/add" element={<ProductFormPage />} />
    <Route path="products/:id" element={<ProductDetailPage />} />
    <Route path="products/:id/edit" element={<ProductFormPage />} />
    <Route path="orders" element={<OrdersPage />} />
    <Route path="orders/:id" element={<OrderDetailPage />} />
    <Route path="returns" element={<ReturnsPage />} />
    <Route path="banners" element={<BannersPage />} />
    <Route path="blogs" element={<BlogsPage />} />
  </Route>
);
