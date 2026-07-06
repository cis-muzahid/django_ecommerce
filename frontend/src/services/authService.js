import apiClient from './apiClient';

/**
 * Authentication API Service
 * Handles all authentication-related API calls
 */

/**
 * Register a new user
 * @param {Object} userData - User registration data
 * @param {string} userData.email - User email
 * @param {string} userData.password - User password
 * @param {string} userData.password_confirm - Password confirmation
 * @param {string} userData.first_name - First name
 * @param {string} userData.last_name - Last name
 * @param {string} userData.mobile_no - Mobile number
 * @param {number} userData.user_role_id - User role ID
 * @returns {Promise} Registration response with user and tokens
 */
export const register = async (userData) => {
  try {
    const response = await apiClient.post('/auth/register/', userData);
    return response.data;
  } catch (error) {
    console.error('Error registering user:', error);
    throw error;
  }
};

/**
 * Login user
 * @param {string} email - User email
 * @param {string} password - User password
 * @returns {Promise} Login response with user and tokens
 */
export const login = async (email, password) => {
  try {
    const response = await apiClient.post('/auth/login/', { email, password });
    return response.data;
  } catch (error) {
    console.error('Error logging in:', error);
    throw error;
  }
};

/**
 * Logout user
 * @param {string} refreshToken - Refresh token to blacklist
 * @returns {Promise} Logout confirmation
 */
export const logout = async (refreshToken) => {
  try {
    const response = await apiClient.post('/auth/logout/', {
      refresh_token: refreshToken,
    });
    return response.data;
  } catch (error) {
    console.error('Error logging out:', error);
    throw error;
  }
};

/**
 * Refresh access token
 * @param {string} refreshToken - Refresh token
 * @returns {Promise} New access token
 */
export const refreshToken = async (refreshToken) => {
  try {
    const response = await apiClient.post('/auth/token/refresh/', {
      refresh: refreshToken,
    });
    return response.data;
  } catch (error) {
    console.error('Error refreshing token:', error);
    throw error;
  }
};

/**
 * Get user profile
 * @returns {Promise} User profile data
 */
export const getProfile = async () => {
  try {
    const response = await apiClient.get('/auth/profile/');
    return response.data;
  } catch (error) {
    console.error('Error fetching profile:', error);
    throw error;
  }
};

/**
 * Update user profile
 * @param {Object} profileData - Updated profile data
 * @returns {Promise} Updated profile
 */
export const updateProfile = async (profileData) => {
  try {
    const response = await apiClient.put('/auth/profile/', profileData);
    return response.data;
  } catch (error) {
    console.error('Error updating profile:', error);
    throw error;
  }
};

/**
 * Change password
 * @param {string} oldPassword - Current password
 * @param {string} newPassword - New password
 * @returns {Promise} Password change confirmation
 */
export const changePassword = async (oldPassword, newPassword) => {
  try {
    const response = await apiClient.post('/auth/change-password/', {
      old_password: oldPassword,
      new_password: newPassword,
    });
    return response.data;
  } catch (error) {
    console.error('Error changing password:', error);
    throw error;
  }
};

/**
 * Request password reset
 * @param {string} email - User email
 * @returns {Promise} Password reset request confirmation
 */
export const requestPasswordReset = async (email) => {
  try {
    const response = await apiClient.post('/auth/password-reset/', { email });
    return response.data;
  } catch (error) {
    console.error('Error requesting password reset:', error);
    throw error;
  }
};

/**
 * Confirm password reset
 * @param {string} uid - User ID from reset link
 * @param {string} token - Reset token from link
 * @param {string} newPassword - New password
 * @returns {Promise} Password reset confirmation
 */
export const confirmPasswordReset = async (uid, token, newPassword) => {
  try {
    const response = await apiClient.post(
      `/auth/password-reset-confirm/${uid}/${token}/`,
      { new_password: newPassword }
    );
    return response.data;
  } catch (error) {
    console.error('Error confirming password reset:', error);
    throw error;
  }
};

/**
 * Get all roles
 * @returns {Promise} List of roles
 */
export const getRoles = async () => {
  try {
    const response = await apiClient.get('/roles/');
    return response.data;
  } catch (error) {
    console.error('Error fetching roles:', error);
    throw error;
  }
};

/**
 * Get user addresses
 * @returns {Promise} List of user addresses
 */
export const getAddresses = async () => {
  try {
    const response = await apiClient.get('/addresses/');
    return response.data;
  } catch (error) {
    console.error('Error fetching addresses:', error);
    throw error;
  }
};

/**
 * Get address by ID
 * @param {number} id - Address ID
 * @returns {Promise} Address details
 */
export const getAddress = async (id) => {
  try {
    const response = await apiClient.get(`/addresses/${id}/`);
    return response.data;
  } catch (error) {
    console.error('Error fetching address:', error);
    throw error;
  }
};

/**
 * Create a new address
 * @param {Object} addressData - Address data
 * @returns {Promise} Created address
 */
export const createAddress = async (addressData) => {
  try {
    const response = await apiClient.post('/addresses/', addressData);
    return response.data;
  } catch (error) {
    console.error('Error creating address:', error);
    throw error;
  }
};

/**
 * Update an address
 * @param {number} id - Address ID
 * @param {Object} addressData - Updated address data
 * @returns {Promise} Updated address
 */
export const updateAddress = async (id, addressData) => {
  try {
    const response = await apiClient.put(`/addresses/${id}/`, addressData);
    return response.data;
  } catch (error) {
    console.error('Error updating address:', error);
    throw error;
  }
};

/**
 * Delete an address
 * @param {number} id - Address ID
 * @returns {Promise} Deletion confirmation
 */
export const deleteAddress = async (id) => {
  try {
    const response = await apiClient.delete(`/addresses/${id}/`);
    return response.data;
  } catch (error) {
    console.error('Error deleting address:', error);
    throw error;
  }
};
