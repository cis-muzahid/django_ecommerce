import apiClient from './apiClient';

/**
 * Home/Homepage API Service
 * Handles all homepage-related API calls
 */

/**
 * Get complete homepage data
 * @returns {Promise} Homepage data including banners, products, categories, blogs, facilities
 */
export const getHomePageData = async () => {
  try {
    const response = await apiClient.get('/homepage/');
    return response.data;
  } catch (error) {
    console.error('Error fetching homepage data:', error);
    throw error;
  }
};

/**
 * Get all banners
 * @param {Object} params - Query parameters
 * @returns {Promise} List of banners
 */
export const getBanners = async (params = {}) => {
  try {
    const response = await apiClient.get('/banners/', { params });
    return response.data;
  } catch (error) {
    console.error('Error fetching banners:', error);
    throw error;
  }
};

/**
 * Get banner by ID
 * @param {number} id - Banner ID
 * @returns {Promise} Banner details
 */
export const getBanner = async (id) => {
  try {
    const response = await apiClient.get(`/banners/${id}/`);
    return response.data;
  } catch (error) {
    console.error('Error fetching banner:', error);
    throw error;
  }
};

/**
 * Get header banners
 * @returns {Promise} List of header banners
 */
export const getHeaderBanners = async () => {
  try {
    const response = await apiClient.get('/banners/header_banners/');
    return response.data;
  } catch (error) {
    console.error('Error fetching header banners:', error);
    throw error;
  }
};

/**
 * Get middle banners
 * @returns {Promise} List of middle banners
 */
export const getMiddleBanners = async () => {
  try {
    const response = await apiClient.get('/banners/middle_banners/');
    return response.data;
  } catch (error) {
    console.error('Error fetching middle banners:', error);
    throw error;
  }
};

/**
 * Get banners grouped by type
 * @returns {Promise} Banners grouped by type
 */
export const getBannersByType = async () => {
  try {
    const response = await apiClient.get('/banners/by_type/');
    return response.data;
  } catch (error) {
    console.error('Error fetching banners by type:', error);
    throw error;
  }
};

/**
 * Create a new banner
 * @param {Object} bannerData - Banner data
 * @returns {Promise} Created banner
 */
export const createBanner = async (bannerData) => {
  try {
    const response = await apiClient.post('/banners/', bannerData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    return response.data;
  } catch (error) {
    console.error('Error creating banner:', error);
    throw error;
  }
};

/**
 * Update a banner
 * @param {number} id - Banner ID
 * @param {Object} bannerData - Updated banner data
 * @returns {Promise} Updated banner
 */
export const updateBanner = async (id, bannerData) => {
  try {
    const response = await apiClient.put(`/banners/${id}/`, bannerData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    return response.data;
  } catch (error) {
    console.error('Error updating banner:', error);
    throw error;
  }
};

/**
 * Delete a banner
 * @param {number} id - Banner ID
 * @returns {Promise} Deletion confirmation
 */
export const deleteBanner = async (id) => {
  try {
    const response = await apiClient.delete(`/banners/${id}/`);
    return response.data;
  } catch (error) {
    console.error('Error deleting banner:', error);
    throw error;
  }
};

/**
 * Get all facilities
 * @param {Object} params - Query parameters
 * @returns {Promise} List of facilities
 */
export const getFacilities = async (params = {}) => {
  try {
    const response = await apiClient.get('/facilities/', { params });
    return response.data;
  } catch (error) {
    console.error('Error fetching facilities:', error);
    throw error;
  }
};

/**
 * Get facility by ID
 * @param {number} id - Facility ID
 * @returns {Promise} Facility details
 */
export const getFacility = async (id) => {
  try {
    const response = await apiClient.get(`/facilities/${id}/`);
    return response.data;
  } catch (error) {
    console.error('Error fetching facility:', error);
    throw error;
  }
};

/**
 * Create a new facility
 * @param {Object} facilityData - Facility data
 * @returns {Promise} Created facility
 */
export const createFacility = async (facilityData) => {
  try {
    const response = await apiClient.post('/facilities/', facilityData);
    return response.data;
  } catch (error) {
    console.error('Error creating facility:', error);
    throw error;
  }
};

/**
 * Update a facility
 * @param {number} id - Facility ID
 * @param {Object} facilityData - Updated facility data
 * @returns {Promise} Updated facility
 */
export const updateFacility = async (id, facilityData) => {
  try {
    const response = await apiClient.put(`/facilities/${id}/`, facilityData);
    return response.data;
  } catch (error) {
    console.error('Error updating facility:', error);
    throw error;
  }
};

/**
 * Delete a facility
 * @param {number} id - Facility ID
 * @returns {Promise} Deletion confirmation
 */
export const deleteFacility = async (id) => {
  try {
    const response = await apiClient.delete(`/facilities/${id}/`);
    return response.data;
  } catch (error) {
    console.error('Error deleting facility:', error);
    throw error;
  }
};

/**
 * Get products by category
 * @param {string} categoryName - Category name
 * @param {Object} params - Query parameters (min_price, max_price, search, page)
 * @returns {Promise} Category products data
 */
export const getCategoryProducts = async (categoryName, params = {}) => {
  try {
    const response = await apiClient.get(`/category/${encodeURIComponent(categoryName)}/`, { params });
    return response.data;
  } catch (error) {
    console.error('Error fetching category products:', error);
    throw error;
  }
};

/**
 * Filter products by price range
 * @param {string} categoryName - Category name
 * @param {string} priceRange - Price range "min,max"
 * @returns {Promise} Filtered products
 */
export const filterProductsByPrice = async (categoryName, priceRange) => {
  try {
    const response = await apiClient.post(`/category/${encodeURIComponent(categoryName)}/`, {
      price: priceRange,
    });
    return response.data;
  } catch (error) {
    console.error('Error filtering products by price:', error);
    throw error;
  }
};

/**
 * Get product detail with related data
 * @param {string} categoryName - Category name
 * @param {string} productSlug - Product slug
 * @returns {Promise} Product detail with related data
 */
export const getProductDetail = async (categoryName, productSlug) => {
  try {
    const response = await apiClient.get(
      `/category/${encodeURIComponent(categoryName)}/${encodeURIComponent(productSlug)}/`,
    );
    return response.data;
  } catch (error) {
    console.error('Error fetching product detail:', error);
    throw error;
  }
};
