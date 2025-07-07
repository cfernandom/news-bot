// Medical API Client for legacy medical data endpoints
import axios, { AxiosInstance } from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

class MedicalApiClient {
  public client: AxiosInstance;

  constructor() {
    this.client = axios.create({
      baseURL: API_BASE_URL,
      timeout: 10000,
      headers: {
        'Content-Type': 'application/json',
      },
    });
  }

  // Health check
  async checkHealth() {
    const response = await this.client.get('/health');
    return response.data;
  }

  // Analytics
  async getAnalyticsSummary() {
    const response = await this.client.get('/api/v1/analytics/summary');
    return response.data;
  }

  // Sentiment
  async getSentimentDistribution(filters?: any) {
    const response = await this.client.get('/api/v1/analytics/sentiment', {
      params: filters,
    });
    return response.data;
  }

  // Geographic
  async getGeographicDistribution() {
    const response = await this.client.get('/api/v1/analytics/geographic');
    return response.data;
  }

  // Topics
  async getTopicsDistribution() {
    const response = await this.client.get('/api/v1/analytics/topics');
    return response.data;
  }

  // Trends
  async getWeeklyTrends() {
    const response = await this.client.get('/api/v1/analytics/trends/weekly');
    return response.data;
  }

  // Articles
  async getArticles(filters?: any) {
    const response = await this.client.get('/api/v1/articles/', {
      params: filters,
    });
    return response.data;
  }

  async getArticlesPaginated(page: number = 1, limit: number = 20, filters?: any) {
    const response = await this.client.get('/api/v1/articles/', {
      params: {
        page,
        limit,
        ...filters,
      },
    });
    return response.data;
  }

  async getArticle(id: number) {
    const response = await this.client.get(`/api/v1/articles/${id}`);
    return response.data;
  }

  // Source credibility
  async getSourceCredibility() {
    const response = await this.client.get('/api/v1/analytics/sources');
    return response.data;
  }

  // Articles stats
  async getArticlesStats() {
    const response = await this.client.get('/api/v1/articles/stats');
    return response.data;
  }
}

export const medicalApiClient = new MedicalApiClient();
