import apiClient from './apiClient.js';

export async function getHomepageData() {
  const response = await apiClient.get('/homepage/');
  return response.data;
}
