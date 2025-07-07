import React, { createContext, useContext, useState, useEffect, ReactNode } from 'react';
import { api } from '@/services/api';

interface User {
  email: string;
  full_name: string;
  role: 'admin' | 'user';
}

interface AuthContextType {
  user: User | null;
  token: string | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  login: (email: string, password: string) => Promise<void>;
  logout: () => void;
  refreshToken: () => Promise<void>;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};

interface AuthProviderProps {
  children: ReactNode;
}

export const AuthProvider: React.FC<AuthProviderProps> = ({ children }) => {
  const [user, setUser] = useState<User | null>(null);
  const [token, setToken] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    // Check for stored token on mount
    const storedToken = localStorage.getItem('auth_token');
    if (storedToken) {
      setToken(storedToken);
      // Set up API default headers
      api.defaults.headers.common['Authorization'] = `Bearer ${storedToken}`;
      // Validate token and get user info
      validateToken(storedToken);
    } else {
      setIsLoading(false);
    }
  }, []);

  const validateToken = async (token: string) => {
    try {
      const response = await api.get('/api/v1/auth/profile');
      if (response.data.status === 'success') {
        setUser(response.data.data);
      } else {
        // Token invalid, clear it
        handleLogout();
      }
    } catch (error) {
      console.error('Token validation failed:', error);
      handleLogout();
    } finally {
      setIsLoading(false);
    }
  };

  const login = async (email: string, password: string) => {
    try {
      const response = await api.post('/api/v1/auth/login', {
        email,
        password,
      });

      if (response.data.status === 'success') {
        const { access_token, user: userData } = response.data.data;

        // Store token
        localStorage.setItem('auth_token', access_token);
        setToken(access_token);
        setUser(userData);

        // Set up API default headers
        api.defaults.headers.common['Authorization'] = `Bearer ${access_token}`;
      } else {
        throw new Error('Login failed');
      }
    } catch (error) {
      console.error('Login error:', error);
      throw error;
    }
  };

  const logout = async () => {
    try {
      // Call logout endpoint if authenticated
      if (token) {
        await api.post('/api/v1/auth/logout');
      }
    } catch (error) {
      console.error('Logout error:', error);
    } finally {
      handleLogout();
    }
  };

  const handleLogout = () => {
    localStorage.removeItem('auth_token');
    setToken(null);
    setUser(null);
    delete api.defaults.headers.common['Authorization'];
  };

  const refreshToken = async () => {
    try {
      const response = await api.post('/api/v1/auth/refresh');
      if (response.data.status === 'success') {
        const { access_token } = response.data.data;

        localStorage.setItem('auth_token', access_token);
        setToken(access_token);
        api.defaults.headers.common['Authorization'] = `Bearer ${access_token}`;
      }
    } catch (error) {
      console.error('Token refresh failed:', error);
      handleLogout();
    }
  };

  const value = {
    user,
    token,
    isAuthenticated: !!user && !!token,
    isLoading,
    login,
    logout,
    refreshToken,
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};
