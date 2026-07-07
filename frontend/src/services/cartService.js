import apiClient from './apiClient';

/**
 * Cart & Wishlist API Service
 * Handles all cart and wishlist-related API calls
 */

/**
 * Get user's cart items
 * @returns {Promise} List of cart items
 */
export const getCartItems = async () => {
  try {
    const response = await apiClient.get('/cart/');
    return response.data;
  } catch (error) {
    console.error('Error fetching cart items:', error);
    throw error;
  }
};

/**
 * Add item to cart
 * @param {number} productId - Product ID
 * @param {number} quantity - Quantity to add
 * @returns {Promise} Added cart item
 */
export const addToCart = async (productId, quantity = 1) => {
  try {
    const response = await apiClient.post('/cart/', {
      product: productId,
      quantity,
    });
    return response.data;
  } catch (error) {
    console.error('Error adding to cart:', error);
    throw error;
  }
};

/**
 * Update cart item quantity
 * @param {number} cartItemId - Cart item ID
 * @param {number} quantity - New quantity
 * @returns {Promise} Updated cart item
 */
export const updateCartItem = async (cartItemId, quantity) => {
  try {
    const response = await apiClient.put(`/cart/${cartItemId}/`, { quantity });
    return response.data;
  } catch (error) {
    console.error('Error updating cart item:', error);
    throw error;
  }
};

/**
 * Remove item from cart
 * @param {number} cartItemId - Cart item ID
 * @returns {Promise} Deletion confirmation
 */
export const removeFromCart = async (cartItemId) => {
  try {
    const response = await apiClient.delete(`/cart/${cartItemId}/`);
    return response.data;
  } catch (error) {
    console.error('Error removing from cart:', error);
    throw error;
  }
};

/**
 * Clear all cart items
 * @returns {Promise} Clear confirmation
 */
export const clearCart = async () => {
  try {
    const response = await apiClient.delete('/cart/clear/');
    return response.data;
  } catch (error) {
    console.error('Error clearing cart:', error);
    throw error;
  }
};

/**
 * Get user's wishlist items
 * @returns {Promise} List of wishlist items
 */
export const getWishlistItems = async () => {
  try {
    const response = await apiClient.get('/wishlist/');
    return response.data;
  } catch (error) {
    console.error('Error fetching wishlist items:', error);
    throw error;
  }
};

/**
 * Add item to wishlist
 * @param {number} productId - Product ID
 * @returns {Promise} Added wishlist item
 */
export const addToWishlist = async (productId) => {
  try {
    const response = await apiClient.post('/wishlist/', {
      product: productId,
    });
    return response.data;
  } catch (error) {
    console.error('Error adding to wishlist:', error);
    throw error;
  }
};

/**
 * Remove item from wishlist
 * @param {number} wishlistItemId - Wishlist item ID
 * @returns {Promise} Deletion confirmation
 */
export const removeFromWishlist = async (wishlistItemId) => {
  try {
    const response = await apiClient.delete(`/wishlist/${wishlistItemId}/`);
    return response.data;
  } catch (error) {
    console.error('Error removing from wishlist:', error);
    throw error;
  }
};

/**
 * Get cart and wishlist statistics
 * @returns {Promise} Cart and wishlist counts
 */
export const getCartWishlistStats = async () => {
  try {
    const response = await apiClient.get('/cart-wishlist-stats/');
    return response.data;
  } catch (error) {
    console.error('Error fetching cart/wishlist stats:', error);
    throw error;
  }
};
