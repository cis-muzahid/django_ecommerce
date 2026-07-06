import apiClient from '../../services/apiClient';

/**
 * Supplier Banner Service
 * Uses main banner API endpoints with supplier filtering handled by backend
 */

export const getBanners = async (page = 1) => {
  try {
    const response = await apiClient.get('/banners/', { params: { page } });
    return response.data;
  } catch (error) {
    console.error('Error fetching banners:', error);
    throw error;
  }
};

export const getBanner = async (id) => {
  try {
    const response = await apiClient.get(`/banners/${id}/`);
    return response.data;
  } catch (error) {
    console.error('Error fetching banner:', error);
    throw error;
  }
};

export const createBanner = async (bannerData) => {
  try {
    const response = await apiClient.post('/banners/', bannerData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    });
    return response.data;
  } catch (error) {
    console.error('Error creating banner:', error);
    throw error;
  }
};

export const updateBanner = async (id, bannerData) => {
  try {
    const response = await apiClient.put(`/banners/${id}/`, bannerData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    });
    return response.data;
  } catch (error) {
    console.error('Error updating banner:', error);
    throw error;
  }
};

export const deleteBanner = async (id) => {
  try {
    const response = await apiClient.delete(`/banners/${id}/`);
    return response.data;
  } catch (error) {
    console.error('Error deleting banner:', error);
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
