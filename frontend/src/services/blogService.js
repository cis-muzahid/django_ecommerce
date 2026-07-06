import apiClient from './apiClient';

/**
 * Blog API Service
 * Handles all blog-related API calls
 */

/**
 * Get all blogs with pagination and filters
 * @param {Object} params - Query parameters (page, search, category, etc.)
 * @returns {Promise} Paginated list of blogs
 */
export const getBlogs = async (params = {}) => {
  try {
    const response = await apiClient.get('/blogs/', { params });
    return response.data;
  } catch (error) {
    console.error('Error fetching blogs:', error);
    throw error;
  }
};

/**
 * Get blog by ID
 * @param {number} id - Blog ID
 * @returns {Promise} Blog details
 */
export const getBlog = async (id) => {
  try {
    const response = await apiClient.get(`/blogs/${id}/`);
    return response.data;
  } catch (error) {
    console.error('Error fetching blog:', error);
    throw error;
  }
};

/**
 * Get blog by slug
 * @param {string} slug - Blog slug
 * @returns {Promise} Blog details
 */
export const getBlogBySlug = async (slug) => {
  try {
    const response = await apiClient.get(`/blogs/slug/${slug}/`);
    return response.data;
  } catch (error) {
    console.error('Error fetching blog by slug:', error);
    throw error;
  }
};

/**
 * Create a new blog
 * @param {Object} blogData - Blog data
 * @returns {Promise} Created blog
 */
export const createBlog = async (blogData) => {
  try {
    const response = await apiClient.post('/blogs/', blogData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    return response.data;
  } catch (error) {
    console.error('Error creating blog:', error);
    throw error;
  }
};

/**
 * Update a blog
 * @param {number} id - Blog ID
 * @param {Object} blogData - Updated blog data
 * @returns {Promise} Updated blog
 */
export const updateBlog = async (id, blogData) => {
  try {
    const response = await apiClient.put(`/blogs/${id}/`, blogData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    return response.data;
  } catch (error) {
    console.error('Error updating blog:', error);
    throw error;
  }
};

/**
 * Delete a blog
 * @param {number} id - Blog ID
 * @returns {Promise} Deletion confirmation
 */
export const deleteBlog = async (id) => {
  try {
    const response = await apiClient.delete(`/blogs/${id}/`);
    return response.data;
  } catch (error) {
    console.error('Error deleting blog:', error);
    throw error;
  }
};

/**
 * Get blog comments
 * @param {number} blogId - Blog ID
 * @returns {Promise} List of blog comments
 */
export const getBlogComments = async (blogId) => {
  try {
    const response = await apiClient.get(`/blogs/${blogId}/comments/`);
    return response.data;
  } catch (error) {
    console.error('Error fetching blog comments:', error);
    throw error;
  }
};

/**
 * Create blog comment
 * @param {number} blogId - Blog ID
 * @param {Object} commentData - Comment data
 * @returns {Promise} Created comment
 */
export const createBlogComment = async (blogId, commentData) => {
  try {
    const response = await apiClient.post(`/blogs/${blogId}/comments/`, commentData);
    return response.data;
  } catch (error) {
    console.error('Error creating blog comment:', error);
    throw error;
  }
};

/**
 * Update blog comment
 * @param {number} blogId - Blog ID
 * @param {number} commentId - Comment ID
 * @param {Object} commentData - Updated comment data
 * @returns {Promise} Updated comment
 */
export const updateBlogComment = async (blogId, commentId, commentData) => {
  try {
    const response = await apiClient.put(
      `/blogs/${blogId}/comments/${commentId}/`,
      commentData
    );
    return response.data;
  } catch (error) {
    console.error('Error updating blog comment:', error);
    throw error;
  }
};

/**
 * Delete blog comment
 * @param {number} blogId - Blog ID
 * @param {number} commentId - Comment ID
 * @returns {Promise} Deletion confirmation
 */
export const deleteBlogComment = async (blogId, commentId) => {
  try {
    const response = await apiClient.delete(`/blogs/${blogId}/comments/${commentId}/`);
    return response.data;
  } catch (error) {
    console.error('Error deleting blog comment:', error);
    throw error;
  }
};

/**
 * Get all blog categories
 * @returns {Promise} List of blog categories
 */
export const getBlogCategories = async () => {
  try {
    const response = await apiClient.get('/blog-categories/');
    return response.data;
  } catch (error) {
    console.error('Error fetching blog categories:', error);
    throw error;
  }
};

/**
 * Get blog category by ID
 * @param {number} id - Category ID
 * @returns {Promise} Category details
 */
export const getBlogCategory = async (id) => {
  try {
    const response = await apiClient.get(`/blog-categories/${id}/`);
    return response.data;
  } catch (error) {
    console.error('Error fetching blog category:', error);
    throw error;
  }
};

/**
 * Create blog category
 * @param {Object} categoryData - Category data
 * @returns {Promise} Created category
 */
export const createBlogCategory = async (categoryData) => {
  try {
    const response = await apiClient.post('/blog-categories/', categoryData);
    return response.data;
  } catch (error) {
    console.error('Error creating blog category:', error);
    throw error;
  }
};

/**
 * Update blog category
 * @param {number} id - Category ID
 * @param {Object} categoryData - Updated category data
 * @returns {Promise} Updated category
 */
export const updateBlogCategory = async (id, categoryData) => {
  try {
    const response = await apiClient.put(`/blog-categories/${id}/`, categoryData);
    return response.data;
  } catch (error) {
    console.error('Error updating blog category:', error);
    throw error;
  }
};

/**
 * Delete blog category
 * @param {number} id - Category ID
 * @returns {Promise} Deletion confirmation
 */
export const deleteBlogCategory = async (id) => {
  try {
    const response = await apiClient.delete(`/blog-categories/${id}/`);
    return response.data;
  } catch (error) {
    console.error('Error deleting blog category:', error);
    throw error;
  }
};
