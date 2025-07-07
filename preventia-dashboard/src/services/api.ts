// Unified API client that includes both medical and sources administration
import { medicalApiClient } from './medical-api';
import { sourcesApiClient } from './sources-api';

// Re-export the clients
export { medicalApiClient };
export { sourcesApiClient };

// Create a unified API client for common operations
// Exposes the axios instance directly for HTTP methods
export const api = sourcesApiClient.axiosClient;

// Set up auth interceptor for the unified client
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('auth_token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export default api;
