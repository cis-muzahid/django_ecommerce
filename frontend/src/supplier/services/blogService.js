import apiClient from '../../services/apiClient';

/**
 * Supplier Blog Service
 * Uses main blog API endpoints with supplier filtering handled by backend
 */

export const getBlogs = async (page = 1) => {
  try {
    const response = await apiClient.get('/blogs/', { params: { page } });
    return response.data;
  } catch (error) {
    console.error('Error fetching blogs:', error);
    throw error;
  }
};

export const getBlog = async (id) => {
  try {
    const response = await apiClient.get(`/blogs/${id}/`);
    return response.data;
  } catch (error) {
    console.error('Error fetching blog:', error);
    throw error;
  }
};

export const createBlog = async (blogData) => {
  try {
    const response = await apiClient.post('/blogs/', blogData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    });
    return response.data;
  } catch (error) {
    console.error('Error creating blog:', error);
    throw error;
  }
};

export const updateBlog = async (id, blogData) => {
  try {
    const response = await apiClient.put(`/blogs/${id}/`, blogData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    });
    return response.data;
  } catch (error) {
    console.error('Error updating blog:', error);
    throw error;
  }
};

export const deleteBlog = async (id) => {
  try {
    const response = await apiClient.delete(`/blogs/${id}/`);
    return response.data;
  } catch (error) {
    console.error('Error deleting blog:', error);
    throw error;
  }
};

export const getBlogCategories = async () => {
  try {
    const response = await apiClient.get('/blog-categories/');
    return response.data;
  } catch (error) {
    console.error('Error fetching blog categories:', error);
    throw error;
  }
};
