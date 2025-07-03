// API client for PreventIA FastAPI backend
import axios, { AxiosInstance, AxiosError } from 'axios';
import { APIResponse, APIError, Article, AnalyticsSummary, SearchParams } from '../types';

// API configuration
const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api';

// Create axios instance with default configuration
const createApiClient = (): AxiosInstance => {
  const client = axios.create({
    baseURL: API_BASE_URL,
    timeout: 10000, // 10 seconds
    headers: {
      'Content-Type': 'application/json',
      'Accept': 'application/json',
    },
  });

  // Request interceptor
  client.interceptors.request.use(
    (config) => {
      // Simple request logging without cache busting
      return config;
    },
    (error) => {
      console.error('Request error:', error);
      return Promise.reject(error);
    }
  );

  // Response interceptor
  client.interceptors.response.use(
    (response) => {
      return response;
    },
    (error: AxiosError) => {
      const apiError: APIError = {
        error: error.name,
        message: error.message || 'An unexpected error occurred',
        code: error.response?.status || 500,
        timestamp: new Date().toISOString(),
      };

      if (error.response?.data) {
        const errorData = error.response.data as any;
        apiError.message = errorData.detail || errorData.message || apiError.message;
      }

      console.error('API Error:', apiError);
      return Promise.reject(apiError);
    }
  );

  return client;
};

// API client instance
const apiClient = createApiClient();

// API service class
export class PreventiaAPI {
  // Health check
  static async healthCheck(): Promise<{ status: string; timestamp: string }> {
    const response = await apiClient.get('/health');
    return response.data;
  }

  // Analytics endpoints
  static async getAnalyticsSummary(): Promise<AnalyticsSummary> {
    const response = await apiClient.get<APIResponse<AnalyticsSummary>>('/analytics/summary');
    return response.data.data || response.data;
  }

  static async getArticleCount(): Promise<{ total: number; by_language: Record<string, number> }> {
    const response = await apiClient.get('/analytics/article-count');
    return response.data;
  }

  static async getLanguageDistribution(): Promise<{ en: number; es: number }> {
    const response = await apiClient.get('/analytics/language-distribution');
    return response.data;
  }

  static async getCountryDistribution(): Promise<Array<{ country: string; count: number; percentage: number }>> {
    const response = await apiClient.get('/analytics/country-distribution');
    return response.data;
  }

  static async getTopSources(): Promise<Array<{ source: string; count: number; reliability_score?: number }>> {
    const response = await apiClient.get('/analytics/top-sources');
    return response.data;
  }

  static async getSentimentDistribution(): Promise<{
    positive: number;
    negative: number;
    neutral: number;
  }> {
    const response = await apiClient.get('/analytics/sentiment-distribution');
    return response.data;
  }

  static async getSentimentTrends(period: '7d' | '30d' | '90d' = '30d'): Promise<Array<{
    date: string;
    positive: number;
    negative: number;
    neutral: number;
    total: number;
  }>> {
    const response = await apiClient.get(`/analytics/sentiment-trends?period=${period}`);
    return response.data;
  }

  static async getTopicsByLanguage(): Promise<Record<string, Array<{ topic: string; count: number }>>> {
    const response = await apiClient.get('/analytics/topics-by-language');
    return response.data;
  }

  static async getGeographicDistribution(): Promise<Array<{
    country: string;
    count: number;
    coordinates: [number, number];
    articles?: Article[];
  }>> {
    const response = await apiClient.get('/analytics/geographic-distribution');
    return response.data;
  }

  // Articles endpoints
  static async getArticles(params?: SearchParams): Promise<APIResponse<Article[]>> {
    const response = await apiClient.get('/articles/search', { params });
    return response.data;
  }

  static async getArticleById(id: number): Promise<Article> {
    const response = await apiClient.get(`/articles/${id}`);
    return response.data;
  }

  static async getArticleStats(): Promise<{
    total: number;
    processed: number;
    pending: number;
    last_updated: string;
  }> {
    const response = await apiClient.get('/articles/stats');
    return response.data;
  }

  // NLP endpoints
  static async analyzeSentiment(text: string, title?: string): Promise<{
    sentiment_label: 'positive' | 'negative' | 'neutral';
    confidence: number;
    scores: {
      positive: number;
      negative: number;
      neutral: number;
      compound: number;
    };
  }> {
    const response = await apiClient.post('/nlp/analyze-sentiment', {
      text,
      title: title || '',
    });
    return response.data;
  }

  static async classifyTopic(text: string): Promise<{
    topic_category: string;
    confidence: number;
    all_categories: Record<string, number>;
  }> {
    const response = await apiClient.post('/nlp/classify-topic', {
      text,
    });
    return response.data;
  }

  static async batchProcessing(articleIds: number[]): Promise<{
    processed: number;
    failed: number;
    results: Array<{
      article_id: number;
      status: 'success' | 'failed';
      sentiment?: any;
      topic?: any;
      error?: string;
    }>;
  }> {
    const response = await apiClient.post('/nlp/batch-process', {
      article_ids: articleIds,
    });
    return response.data;
  }

  // Export functionality
  static async exportData(format: 'csv' | 'json', params?: SearchParams): Promise<Blob> {
    const response = await apiClient.get('/articles/export', {
      params: { ...params, format },
      responseType: 'blob',
    });
    return response.data;
  }
}

// React Query hooks for data fetching
export const apiQueries = {
  // Analytics queries
  analyticsSummary: () => ({
    queryKey: ['analytics', 'summary'],
    queryFn: PreventiaAPI.getAnalyticsSummary,
    staleTime: 5 * 60 * 1000, // 5 minutes
  }),

  articleCount: () => ({
    queryKey: ['analytics', 'article-count'],
    queryFn: PreventiaAPI.getArticleCount,
    staleTime: 10 * 60 * 1000, // 10 minutes
  }),

  languageDistribution: () => ({
    queryKey: ['analytics', 'language-distribution'],
    queryFn: PreventiaAPI.getLanguageDistribution,
    staleTime: 10 * 60 * 1000,
  }),

  countryDistribution: () => ({
    queryKey: ['analytics', 'country-distribution'],
    queryFn: PreventiaAPI.getCountryDistribution,
    staleTime: 10 * 60 * 1000,
  }),

  topSources: () => ({
    queryKey: ['analytics', 'top-sources'],
    queryFn: PreventiaAPI.getTopSources,
    staleTime: 10 * 60 * 1000,
  }),

  sentimentDistribution: () => ({
    queryKey: ['analytics', 'sentiment-distribution'],
    queryFn: PreventiaAPI.getSentimentDistribution,
    staleTime: 5 * 60 * 1000,
  }),

  sentimentTrends: (period: '7d' | '30d' | '90d' = '30d') => ({
    queryKey: ['analytics', 'sentiment-trends', period],
    queryFn: () => PreventiaAPI.getSentimentTrends(period),
    staleTime: 5 * 60 * 1000,
  }),

  geographicDistribution: () => ({
    queryKey: ['analytics', 'geographic-distribution'],
    queryFn: PreventiaAPI.getGeographicDistribution,
    staleTime: 10 * 60 * 1000,
  }),

  // Articles queries
  articles: (params?: SearchParams) => ({
    queryKey: ['articles', 'search', params],
    queryFn: () => PreventiaAPI.getArticles(params),
    staleTime: 2 * 60 * 1000, // 2 minutes
  }),

  article: (id: number) => ({
    queryKey: ['articles', id],
    queryFn: () => PreventiaAPI.getArticleById(id),
    staleTime: 5 * 60 * 1000,
  }),

  articleStats: () => ({
    queryKey: ['articles', 'stats'],
    queryFn: PreventiaAPI.getArticleStats,
    staleTime: 1 * 60 * 1000, // 1 minute
  }),
};

// Health check utility
export const checkAPIHealth = async (): Promise<boolean> => {
  try {
    await PreventiaAPI.healthCheck();
    return true;
  } catch (error) {
    console.error('API health check failed:', error);
    return false;
  }
};

// Export default API client
export default apiClient;
