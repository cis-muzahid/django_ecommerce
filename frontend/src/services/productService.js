import apiClient from './apiClient';

/**
 * Product API Service
 * Handles all product-related API calls
 */

/**
 * Get all products with pagination and filters
 * @param {Object} params - Query parameters (page, search, category, min_price, max_price, etc.)
 * @returns {Promise} Paginated list of products
 */
export const getProducts = async (params = {}) => {
  try {
    const response = await apiClient.get('/products/', { params });
    return response.data;
  } catch (error) {
    console.error('Error fetching products:', error);
    throw error;
  }
};

/**
 * Get product by ID
 * @param {number} id - Product ID
 * @returns {Promise} Product details
 */
export const getProduct = async (id) => {
  try {
    const response = await apiClient.get(`/products/${id}/`);
    return response.data;
  } catch (error) {
    console.error('Error fetching product:', error);
    throw error;
  }
};

/**
 * Search products
 * @param {string} query - Search query
 * @returns {Promise} Search results
 */
export const searchProducts = async (query) => {
  try {
    const response = await apiClient.get('/products/search/', {
      params: { q: query },
    });
    return response.data;
  } catch (error) {
    console.error('Error searching products:', error);
    throw error;
  }
};

/**
 * Create a new product
 * @param {Object} productData - Product data
 * @returns {Promise} Created product
 */
export const createProduct = async (productData) => {
  try {
    const response = await apiClient.post('/products/', productData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    return response.data;
  } catch (error) {
    console.error('Error creating product:', error);
    throw error;
  }
};

/**
 * Update a product
 * @param {number} id - Product ID
 * @param {Object} productData - Updated product data
 * @returns {Promise} Updated product
 */
export const updateProduct = async (id, productData) => {
  try {
    const response = await apiClient.put(`/products/${id}/`, productData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    return response.data;
  } catch (error) {
    console.error('Error updating product:', error);
    throw error;
  }
};

/**
 * Partially update a product
 * @param {number} id - Product ID
 * @param {Object} productData - Partial product data
 * @returns {Promise} Updated product
 */
export const patchProduct = async (id, productData) => {
  try {
    const response = await apiClient.patch(`/products/${id}/`, productData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    return response.data;
  } catch (error) {
    console.error('Error patching product:', error);
    throw error;
  }
};

/**
 * Delete a product
 * @param {number} id - Product ID
 * @returns {Promise} Deletion confirmation
 */
export const deleteProduct = async (id) => {
  try {
    const response = await apiClient.delete(`/products/${id}/`);
    return response.data;
  } catch (error) {
    console.error('Error deleting product:', error);
    throw error;
  }
};

/**
 * Get product attributes
 * @param {number} productId - Product ID
 * @returns {Promise} List of product attributes
 */
export const getProductAttributes = async (productId) => {
  try {
    const response = await apiClient.get(`/products/${productId}/attributes/`);
    return response.data;
  } catch (error) {
    console.error('Error fetching product attributes:', error);
    throw error;
  }
};

/**
 * Create product attribute
 * @param {number} productId - Product ID
 * @param {Object} attributeData - Attribute data
 * @returns {Promise} Created attribute
 */
export const createProductAttribute = async (productId, attributeData) => {
  try {
    const response = await apiClient.post(
      `/products/${productId}/attributes/`,
      attributeData,
      {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      }
    );
    return response.data;
  } catch (error) {
    console.error('Error creating product attribute:', error);
    throw error;
  }
};

/**
 * Update product attribute
 * @param {number} productId - Product ID
 * @param {number} attributeId - Attribute ID
 * @param {Object} attributeData - Updated attribute data
 * @returns {Promise} Updated attribute
 */
export const updateProductAttribute = async (productId, attributeId, attributeData) => {
  try {
    const response = await apiClient.put(
      `/products/${productId}/attributes/${attributeId}/`,
      attributeData,
      {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      }
    );
    return response.data;
  } catch (error) {
    console.error('Error updating product attribute:', error);
    throw error;
  }
};

/**
 * Delete product attribute
 * @param {number} productId - Product ID
 * @param {number} attributeId - Attribute ID
 * @returns {Promise} Deletion confirmation
 */
export const deleteProductAttribute = async (productId, attributeId) => {
  try {
    const response = await apiClient.delete(
      `/products/${productId}/attributes/${attributeId}/`
    );
    return response.data;
  } catch (error) {
    console.error('Error deleting product attribute:', error);
    throw error;
  }
};

/**
 * Get product specifications
 * @param {number} productId - Product ID
 * @returns {Promise} List of product specifications
 */
export const getProductSpecifications = async (productId) => {
  try {
    const response = await apiClient.get(`/products/${productId}/specifications/`);
    return response.data;
  } catch (error) {
    console.error('Error fetching product specifications:', error);
    throw error;
  }
};

/**
 * Create product specification
 * @param {number} productId - Product ID
 * @param {Object} specData - Specification data
 * @returns {Promise} Created specification
 */
export const createProductSpecification = async (productId, specData) => {
  try {
    const response = await apiClient.post(
      `/products/${productId}/specifications/`,
      specData
    );
    return response.data;
  } catch (error) {
    console.error('Error creating product specification:', error);
    throw error;
  }
};

/**
 * Update product specification
 * @param {number} productId - Product ID
 * @param {number} specId - Specification ID
 * @param {Object} specData - Updated specification data
 * @returns {Promise} Updated specification
 */
export const updateProductSpecification = async (productId, specId, specData) => {
  try {
    const response = await apiClient.put(
      `/products/${productId}/specifications/${specId}/`,
      specData
    );
    return response.data;
  } catch (error) {
    console.error('Error updating product specification:', error);
    throw error;
  }
};

/**
 * Delete product specification
 * @param {number} productId - Product ID
 * @param {number} specId - Specification ID
 * @returns {Promise} Deletion confirmation
 */
export const deleteProductSpecification = async (productId, specId) => {
  try {
    const response = await apiClient.delete(
      `/products/${productId}/specifications/${specId}/`
    );
    return response.data;
  } catch (error) {
    console.error('Error deleting product specification:', error);
    throw error;
  }
};

/**
 * Get product reviews
 * @param {number} productId - Product ID
 * @returns {Promise} List of product reviews
 */
export const getProductReviews = async (productId) => {
  try {
    const response = await apiClient.get(`/products/${productId}/reviews/`);
    return response.data;
  } catch (error) {
    console.error('Error fetching product reviews:', error);
    throw error;
  }
};

/**
 * Create product review
 * @param {number} productId - Product ID
 * @param {Object} reviewData - Review data (rating, title, comment)
 * @returns {Promise} Created review
 */
export const createProductReview = async (productId, reviewData) => {
  try {
    const response = await apiClient.post(
      `/products/${productId}/reviews/`,
      reviewData
    );
    return response.data;
  } catch (error) {
    console.error('Error creating product review:', error);
    throw error;
  }
};

/**
 * Update product review
 * @param {number} productId - Product ID
 * @param {number} reviewId - Review ID
 * @param {Object} reviewData - Updated review data
 * @returns {Promise} Updated review
 */
export const updateProductReview = async (productId, reviewId, reviewData) => {
  try {
    const response = await apiClient.put(
      `/products/${productId}/reviews/${reviewId}/`,
      reviewData
    );
    return response.data;
  } catch (error) {
    console.error('Error updating product review:', error);
    throw error;
  }
};

/**
 * Delete product review
 * @param {number} productId - Product ID
 * @param {number} reviewId - Review ID
 * @returns {Promise} Deletion confirmation
 */
export const deleteProductReview = async (productId, reviewId) => {
  try {
    const response = await apiClient.delete(
      `/products/${productId}/reviews/${reviewId}/`
    );
    return response.data;
  } catch (error) {
    console.error('Error deleting product review:', error);
    throw error;
  }
};

/**
 * Get all categories
 * @returns {Promise} List of categories
 */
export const getCategories = async () => {
  try {
    const response = await apiClient.get('/categories/');
    return response.data;
  } catch (error) {
    console.error('Error fetching categories:', error);
    throw error;
  }
};

/**
 * Get category by ID
 * @param {number} id - Category ID
 * @returns {Promise} Category details
 */
export const getCategory = async (id) => {
  try {
    const response = await apiClient.get(`/categories/${id}/`);
    return response.data;
  } catch (error) {
    console.error('Error fetching category:', error);
    throw error;
  }
};
