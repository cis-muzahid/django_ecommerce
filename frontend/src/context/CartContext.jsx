import { createContext, useState, useContext, useEffect } from 'react';
import { useAuth } from './AuthContext';
import * as cartApi from '../services/cartApi';

const CartContext = createContext();

export const useCart = () => {
  const context = useContext(CartContext);
  if (!context) {
    throw new Error('useCart must be used within a CartProvider');
  }
  return context;
};

export const CartProvider = ({ children }) => {
  const { isAuthenticated } = useAuth();
  const [cartItems, setCartItems] = useState([]);
  const [wishlistItems, setWishlistItems] = useState([]);
  const [cartCount, setCartCount] = useState(0);
  const [wishlistCount, setWishlistCount] = useState(0);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (isAuthenticated) {
      fetchCartData();
      fetchWishlistData();
    } else {
      setCartItems([]);
      setWishlistItems([]);
      setCartCount(0);
      setWishlistCount(0);
    }
  }, [isAuthenticated]);

  const fetchCartData = async () => {
    try {
      const data = await cartApi.getCart();
      setCartItems(data.results || data);
      setCartCount(data.results?.length || data.length || 0);
    } catch (error) {
      console.error('Failed to fetch cart:', error);
    }
  };

  const fetchWishlistData = async () => {
    try {
      const data = await cartApi.getWishlist();
      setWishlistItems(data.results || data);
      setWishlistCount(data.results?.length || data.length || 0);
    } catch (error) {
      console.error('Failed to fetch wishlist:', error);
    }
  };

  const addToCart = async (productId, quantity = 1) => {
    try {
      setLoading(true);
      await cartApi.addToCart(productId, quantity);
      await fetchCartData();
      return { success: true };
    } catch (error) {
      return { success: false, error: error.message };
    } finally {
      setLoading(false);
    }
  };

  const removeFromCart = async (cartItemId) => {
    try {
      setLoading(true);
      await cartApi.removeFromCart(cartItemId);
      await fetchCartData();
      return { success: true };
    } catch (error) {
      return { success: false, error: error.message };
    } finally {
      setLoading(false);
    }
  };

  const updateCartQuantity = async (cartItemId, quantity) => {
    try {
      setLoading(true);
      await cartApi.updateCartItem(cartItemId, { quantity });
      await fetchCartData();
      return { success: true };
    } catch (error) {
      return { success: false, error: error.message };
    } finally {
      setLoading(false);
    }
  };

  const clearCart = async () => {
    try {
      setLoading(true);
      await cartApi.clearCart();
      await fetchCartData();
      return { success: true };
    } catch (error) {
      return { success: false, error: error.message };
    } finally {
      setLoading(false);
    }
  };

  const addToWishlist = async (productId) => {
    try {
      setLoading(true);
      await cartApi.addToWishlist(productId);
      await fetchWishlistData();
      return { success: true };
    } catch (error) {
      return { success: false, error: error.message };
    } finally {
      setLoading(false);
    }
  };

  const removeFromWishlist = async (wishlistItemId) => {
    try {
      setLoading(true);
      await cartApi.removeFromWishlist(wishlistItemId);
      await fetchWishlistData();
      return { success: true };
    } catch (error) {
      return { success: false, error: error.message };
    } finally {
      setLoading(false);
    }
  };

  const moveToCart = async (wishlistItemId) => {
    try {
      setLoading(true);
      await cartApi.moveToCart(wishlistItemId);
      await fetchWishlistData();
      await fetchCartData();
      return { success: true };
    } catch (error) {
      return { success: false, error: error.message };
    } finally {
      setLoading(false);
    }
  };

  const value = {
    cartItems,
    wishlistItems,
    cartCount,
    wishlistCount,
    loading,
    addToCart,
    removeFromCart,
    updateCartQuantity,
    clearCart,
    addToWishlist,
    removeFromWishlist,
    moveToCart,
    refreshCart: fetchCartData,
    refreshWishlist: fetchWishlistData,
  };

  return <CartContext.Provider value={value}>{children}</CartContext.Provider>;
};
