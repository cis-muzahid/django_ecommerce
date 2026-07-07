import apiClient from './apiClient.js';

// Cart APIs
export async function getCart() {
  const response = await apiClient.get('/cart/');
  return response.data;
}

export async function getCartSummary() {
  const response = await apiClient.get('/cart/summary/');
  return response.data;
}

export async function addToCart(productId, quantity = 1) {
  const response = await apiClient.post('/cart/', { product: productId, quantity });
  return response.data;
}

export async function updateCartItem(cartItemId, data) {
  const response = await apiClient.patch(`/cart/${cartItemId}/`, data);
  return response.data;
}

export async function removeFromCart(cartItemId) {
  const response = await apiClient.delete(`/cart/${cartItemId}/`);
  return response.data;
}

export async function clearCart() {
  const response = await apiClient.post('/cart/clear/');
  return response.data;
}

// Wishlist APIs
export async function getWishlist() {
  const response = await apiClient.get('/wishlist/');
  return response.data;
}

export async function addToWishlist(productId) {
  const response = await apiClient.post('/wishlist/', { product: productId });
  return response.data;
}

export async function removeFromWishlist(wishlistItemId) {
  const response = await apiClient.delete(`/wishlist/${wishlistItemId}/`);
  return response.data;
}

export async function moveToCart(wishlistItemId) {
  const response = await apiClient.post(`/wishlist/${wishlistItemId}/move_to_cart/`);
  return response.data;
}

// Legacy exports for backward compatibility
export const addCartItem = addToCart;
export const addWishlistItem = addToWishlist;
