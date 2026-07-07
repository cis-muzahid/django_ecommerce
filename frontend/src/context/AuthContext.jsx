import { createContext, useState, useContext, useEffect, useRef } from 'react';
import apiClient from '../services/apiClient';
import axios from 'axios';

const AuthContext = createContext();

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const [token, setToken] = useState(localStorage.getItem('access_token'));
  const initilizedRef = useRef(false);

  // Initialize auth on component mount
  useEffect(() => {
    if (!initilizedRef.current) {
      initilizedRef.current = true;
      initializeAuth();
    }
  }, []);

  // Listen for logout events from apiClient
  useEffect(() => {
    const handleLogout = () => {
      setUser(null);
      setToken(null);
    };

    window.addEventListener('auth-logout', handleLogout);

    // Also listen for storage changes (for multi-tab sync)
    const handleStorageChange = (e) => {
      if (e.key === 'access_token') {
        if (!e.newValue) {
          // Token was cleared, logout user
          setUser(null);
          setToken(null);
        } else {
          // Token was updated from another tab
          setToken(e.newValue);
        }
      }
    };

    window.addEventListener('storage', handleStorageChange);

    return () => {
      window.removeEventListener('auth-logout', handleLogout);
      window.removeEventListener('storage', handleStorageChange);
    };
  }, []);

  const initializeAuth = async () => {
    const storedToken = localStorage.getItem('access_token');
    const storedRefreshToken = localStorage.getItem('refresh_token');

    if (storedToken && storedRefreshToken) {
      // Try to refresh token first to ensure it's valid
      await refreshTokenIfNeeded();
      // Then fetch profile
      const newToken = localStorage.getItem('access_token');
      if (newToken) {
        setToken(newToken);
        await fetchUserProfile();
      } else {
        setLoading(false);
      }
    } else {
      setLoading(false);
    }
  };

  const refreshTokenIfNeeded = async () => {
    try {
      const refreshToken = localStorage.getItem('refresh_token');
      if (!refreshToken) return;

      const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api/v1';
      const response = await axios.post(`${API_BASE_URL}/auth/token/refresh/`, {
        refresh: refreshToken,
      });

      if (response.data.access) {
        localStorage.setItem('access_token', response.data.access);
      }
    } catch (error) {
      console.error('Token refresh failed on initialization:', error);
      localStorage.removeItem('access_token');
      localStorage.removeItem('refresh_token');
    }
  };

  const fetchUserProfile = async () => {
    try {
      const response = await apiClient.get('/auth/profile/');
      setUser(response.data);
      return response.data;
    } catch (error) {
      console.error('Failed to fetch user profile:', error);
      // Don't call logout here, let the response interceptor handle it
      return null;
    } finally {
      setLoading(false);
    }
  };

  const login = async (email, password) => {
    try {
      const response = await apiClient.post('/auth/login/', { email, password });
      const { tokens, user: userData } = response.data;

      if (tokens && tokens.access && tokens.refresh) {
        localStorage.setItem('access_token', tokens.access);
        localStorage.setItem('refresh_token', tokens.refresh);
        setToken(tokens.access);
        setUser(userData);

        // Determine redirect path based on user role
        let redirectPath = '/';
        if (userData.is_superuser) {
          redirectPath = '/admin';
        } else if (userData.user_role?.name === 'supplier') {
          redirectPath = '/supplier';
        }

        return { success: true, redirectPath };
      } else {
        return { success: false, error: 'Invalid response from server' };
      }
    } catch (error) {
      return {
        success: false,
        error: error.response?.data?.error || error.response?.data?.message || 'Login failed'
      };
    }
  };

  const signup = async (userData) => {
    try {
      const response = await apiClient.post('/auth/register/', userData);
      return { success: true, data: response.data };
    } catch (error) {
      return {
        success: false,
        error: error.response?.data || 'Signup failed'
      };
    }
  };

  const logout = () => {
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    setToken(null);
    setUser(null);
  };

  const value = {
    user,
    loading,
    isAuthenticated: !!user,
    login,
    signup,
    logout,
    refreshUserProfile: fetchUserProfile,
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};
