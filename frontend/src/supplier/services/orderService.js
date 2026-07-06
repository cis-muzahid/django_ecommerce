import apiClient from '../../services/apiClient';

/**
 * Supplier Order Service
 * Uses main order API endpoints with supplier filtering handled by backend
 */

export const getOrders = async (page = 1) => {
  try {
    const response = await apiClient.get('/orders/', { params: { page } });
    return response.data;
  } catch (error) {
    console.error('Error fetching orders:', error);
    throw error;
  }
};

export const getOrder = async (id) => {
  try {
    const response = await apiClient.get(`/orders/${id}/`);
    return response.data;
  } catch (error) {
    console.error('Error fetching order:', error);
    throw error;
  }
};

export const updateOrderStatus = async (orderId, status) => {
  try {
    const response = await apiClient.post(`/orders/${orderId}/update_status/`, { status });
    return response.data;
  } catch (error) {
    console.error('Error updating order status:', error);
    throw error;
  }
};

export const getReturnRequests = async () => {
  try {
    const response = await apiClient.get('/returns-replacements/');
    return response.data;
  } catch (error) {
    console.error('Error fetching return requests:', error);
    throw error;
  }
};

export const approveReturnRequest = async (id) => {
  try {
    const response = await apiClient.post(`/returns-replacements/${id}/approve/`);
    return response.data;
  } catch (error) {
    console.error('Error approving return request:', error);
    throw error;
  }
};
