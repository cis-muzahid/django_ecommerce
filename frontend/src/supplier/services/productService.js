import apiClient from '../../services/apiClient';

/**
 * Supplier Product Service
 * Uses main product API endpoints with supplier filtering handled by backend
 */

export const getProducts = async (page = 1, search = '') => {
  try {
    const params = { page };
    if (search) {
      params.search = search;
    }
    const response = await apiClient.get('/products/', { params });
    return response.data;
  } catch (error) {
    console.error('Error fetching products:', error);
    throw error;
  }
};

export const getProduct = async (id) => {
  try {
    const response = await apiClient.get(`/products/${id}/`);
    return response.data;
  } catch (error) {
    console.error('Error fetching product:', error);
    throw error;
  }
};

export const createProduct = async (productData) => {
  try {
    const response = await apiClient.post('/products/', productData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    });
    return response.data;
  } catch (error) {
    console.error('Error creating product:', error);
    throw error;
  }
};

export const updateProduct = async (id, productData) => {
  try {
    const response = await apiClient.put(`/products/${id}/`, productData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    });
    return response.data;
  } catch (error) {
    console.error('Error updating product:', error);
    throw error;
  }
};

export const deleteProduct = async (id) => {
  try {
    const response = await apiClient.delete(`/products/${id}/`);
    return response.data;
  } catch (error) {
    console.error('Error deleting product:', error);
    throw error;
  }
};

export const getCategories = async () => {
  try {
    const response = await apiClient.get('/categories/');
    return response.data;
  } catch (error) {
    console.error('Error fetching categories:', error);
    throw error;
  }
};

// Product Attributes
export const getProductAttributes = async (productId) => {
  try {
    const response = await apiClient.get(`/products/${productId}/attributes/`);
    return response.data;
  } catch (error) {
    console.error('Error fetching product attributes:', error);
    throw error;
  }
};

export const createProductAttribute = async (productId, data) => {
  try {
    const response = await apiClient.post(`/products/${productId}/attributes/`, data, {
      headers: { 'Content-Type': 'multipart/form-data' },
    });
    return response.data;
  } catch (error) {
    console.error('Error creating product attribute:', error);
    throw error;
  }
};

export const updateProductAttribute = async (productId, attrId, data) => {
  try {
    const response = await apiClient.put(`/products/${productId}/attributes/${attrId}/`, data, {
      headers: { 'Content-Type': 'multipart/form-data' },
    });
    return response.data;
  } catch (error) {
    console.error('Error updating product attribute:', error);
    throw error;
  }
};

export const deleteProductAttribute = async (productId, attrId) => {
  try {
    const response = await apiClient.delete(`/products/${productId}/attributes/${attrId}/`);
    return response.data;
  } catch (error) {
    console.error('Error deleting product attribute:', error);
    throw error;
  }
};

// Product Specifications
export const getProductSpecifications = async (productId) => {
  try {
    const response = await apiClient.get(`/products/${productId}/specifications/`);
    return response.data;
  } catch (error) {
    console.error('Error fetching product specifications:', error);
    throw error;
  }
};

export const createProductSpecification = async (productId, data) => {
  try {
    const response = await apiClient.post(`/products/${productId}/specifications/`, data);
    return response.data;
  } catch (error) {
    console.error('Error creating product specification:', error);
    throw error;
  }
};

export const updateProductSpecification = async (productId, specId, data) => {
  try {
    const response = await apiClient.put(`/products/${productId}/specifications/${specId}/`, data);
    return response.data;
  } catch (error) {
    console.error('Error updating product specification:', error);
    throw error;
  }
};

export const deleteProductSpecification = async (productId, specId) => {
  try {
    const response = await apiClient.delete(`/products/${productId}/specifications/${specId}/`);
    return response.data;
  } catch (error) {
    console.error('Error deleting product specification:', error);
    throw error;
  }
};
