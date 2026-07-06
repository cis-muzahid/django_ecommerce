import apiClient from './apiClient';

/**
 * Order API Service
 * Handles all order-related API calls
 */

/**
 * Get user's orders
 * @param {Object} params - Query parameters (page, status, etc.)
 * @returns {Promise} List of orders
 */
export const getOrders = async (params = {}) => {
  try {
    const response = await apiClient.get('/orders/', { params });
    return response.data;
  } catch (error) {
    console.error('Error fetching orders:', error);
    throw error;
  }
};

/**
 * Get order by ID
 * @param {number} id - Order ID
 * @returns {Promise} Order details
 */
export const getOrder = async (id) => {
  try {
    const response = await apiClient.get(`/orders/${id}/`);
    return response.data;
  } catch (error) {
    console.error('Error fetching order:', error);
    throw error;
  }
};

/**
 * Create a new order
 * @param {Object} orderData - Order data
 * @returns {Promise} Created order
 */
export const createOrder = async (orderData) => {
  try {
    const response = await apiClient.post('/orders/', orderData);
    return response.data.order || response.data;
  } catch (error) {
    console.error('Error creating order:', error);
    throw error;
  }
};

/**
 * Get checkout information for the current cart
 * @returns {Promise} Checkout cart, totals, and addresses
 */
export const getCheckoutInfo = async () => {
  try {
    const response = await apiClient.get('/checkout/');
    return response.data;
  } catch (error) {
    console.error('Error fetching checkout info:', error);
    throw error;
  }
};

/**
 * Update order
 * @param {number} id - Order ID
 * @param {Object} orderData - Updated order data
 * @returns {Promise} Updated order
 */
export const updateOrder = async (id, orderData) => {
  try {
    const response = await apiClient.put(`/orders/${id}/`, orderData);
    return response.data;
  } catch (error) {
    console.error('Error updating order:', error);
    throw error;
  }
};

/**
 * Process checkout
 * @param {Object} checkoutData - Checkout data (address, payment_method, items)
 * @returns {Promise} Checkout response
 */
export const processCheckout = async (checkoutData) => {
  try {
    const response = await apiClient.post('/checkout/', checkoutData);
    return response.data.order || response.data;
  } catch (error) {
    console.error('Error processing checkout:', error);
    throw error;
  }
};

/**
 * Process payment
 * @param {Object} paymentData - Payment data (order_id, payment_method, amount)
 * @returns {Promise} Payment response
 */
export const processPayment = async (paymentData) => {
  try {
    const response = await apiClient.post('/payment/', paymentData);
    return response.data;
  } catch (error) {
    console.error('Error processing payment:', error);
    throw error;
  }
};

/**
 * Complete PayPal payment after user approval on PayPal
 * @param {Object} paymentData - { payment_id, payer_id, order_id? }
 * @returns {Promise} Payment completion response
 */
export const completePayPalPayment = async (paymentData) => {
  try {
    const response = await apiClient.post('/paypal/complete/', paymentData);
    return response.data;
  } catch (error) {
    console.error('Error completing PayPal payment:', error);
    throw error;
  }
};

/**
 * Track order
 * @param {number} orderId - Order ID
 * @returns {Promise} Order tracking information
 */
export const trackOrder = async (orderId) => {
  try {
    const response = await apiClient.get('/order-tracking/', {
      params: { order_id: orderId },
    });
    return response.data;
  } catch (error) {
    console.error('Error tracking order:', error);
    throw error;
  }
};

/**
 * Get return/replace requests
 * @param {Object} params - Query parameters
 * @returns {Promise} List of return/replace requests
 */
export const getReturnReplaceRequests = async (params = {}) => {
  try {
    const response = await apiClient.get('/returns-replacements/', { params });
    return response.data;
  } catch (error) {
    console.error('Error fetching return/replace requests:', error);
    throw error;
  }
};

/**
 * Create return/replace request
 * @param {Object} requestData - Request data
 * @returns {Promise} Created request
 */
export const createReturnReplaceRequest = async (requestData) => {
  try {
    const response = await apiClient.post('/returns-replacements/', requestData);
    return response.data;
  } catch (error) {
    console.error('Error creating return/replace request:', error);
    throw error;
  }
};

/**
 * Update return/replace request
 * @param {number} id - Request ID
 * @param {Object} requestData - Updated request data
 * @returns {Promise} Updated request
 */
export const updateReturnReplaceRequest = async (id, requestData) => {
  try {
    const response = await apiClient.put(`/returns-replacements/${id}/`, requestData);
    return response.data;
  } catch (error) {
    console.error('Error updating return/replace request:', error);
    throw error;
  }
};

/**
 * Cancel order
 * @param {number} orderId - Order ID
 * @returns {Promise} Cancellation confirmation
 */
export const cancelOrder = async (orderId) => {
  try {
    const response = await apiClient.post(`/orders/${orderId}/cancel/`);
    return response.data;
  } catch (error) {
    console.error('Error cancelling order:', error);
    throw error;
  }
};

/**
 * Approve a return/replace request (Admin/Supplier only).
 * For Return requests this also triggers a refund via the payment gateway.
 * @param {number} requestId - ReturnAndReplaceOrder ID
 * @returns {Promise} Approval response
 */
export const approveReturnReplaceRequest = async (requestId) => {
  try {
    const response = await apiClient.post(`/returns-replacements/${requestId}/approve/`);
    return response.data;
  } catch (error) {
    console.error('Error approving return/replace request:', error);
    throw error;
  }
};
