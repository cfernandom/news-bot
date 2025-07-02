// Medical API Client for PreventIA Dashboard
// Implementation according to fase4-react-dashboard-plan.md specifications

import axios, { AxiosInstance } from 'axios';
import {
  MedicalArticle,
  AnalyticsSummary,
  SentimentData,
  GeographicData,
  TopicData,
  TrendData,
  MedicalFilters,
  PaginatedArticles,
  MedicalError,
  SourceCredibility,
} from '../types/medical';

// API Response interfaces
interface ApiAnalyticsResponse {
  total_articles?: number;
  total_sources?: number;
  language_distribution?: {
    spanish?: number;
    english?: number;
  };
  sentiment_distribution?: {
    positive?: number;
    negative?: number;
    neutral?: number;
  };
  top_country?: string;
  top_source?: string;
  last_updated?: string;
}

interface ApiGeographicResponse {
  distribution?: Record<string, {
    article_count?: number;
    avg_sentiment?: number;
  }>;
}

interface ApiTopicsResponse {
  distribution?: Record<string, number>;
}

interface ApiTrendsResponse {
  trends?: Array<{
    week: string;
    positive_percentage?: number;
    negative_percentage?: number;
    neutral_percentage?: number;
    total_articles?: number;
  }>;
}

interface ApiArticlesResponse {
  items?: unknown[];
}

interface ApiSourcesResponse {
  sources?: Array<{
    name: string;
    credibility_score?: number;
    article_count?: number;
    average_sentiment?: number;
  }>;
}

export class MedicalApiClient {
  private baseURL: string;
  private client: AxiosInstance;

  constructor(baseURL: string = 'http://localhost:8000') {
    this.baseURL = baseURL;
    this.client = axios.create({
      baseURL: this.baseURL,
      timeout: 10000, // 10s timeout for medical data
      headers: {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
      },
    });

    // Request interceptor for medical context
    this.client.interceptors.request.use(
      (config) => {
        config.headers['X-Medical-Context'] = 'preventia-dashboard';
        config.headers['X-Institution'] = 'UCOMPENSAR';
        return config;
      },
      (error) => Promise.reject(this.handleMedicalError(error))
    );

    // Response interceptor for medical error handling
    this.client.interceptors.response.use(
      (response) => response,
      (error) => Promise.reject(this.handleMedicalError(error))
    );
  }

  private handleMedicalError(error: unknown): MedicalError {
    // Type guard for axios errors
    const isAxiosError = (err: unknown): err is { code?: string; message?: string; response?: { data?: unknown } } => {
      return typeof err === 'object' && err !== null;
    };

    const errorObj = isAxiosError(error) ? error : {};

    const medicalError: MedicalError = {
      code: errorObj.code || 'MEDICAL_API_ERROR',
      message: errorObj.message || 'Error en conexión con datos médicos',
      details: errorObj.response?.data || {},
      timestamp: new Date().toISOString(),
    };

    // Log medical errors for monitoring
    console.error('Medical API Error:', medicalError);

    return medicalError;
  }

  // Health check for medical API
  async checkHealth(): Promise<{ status: string; articlesCount: number }> {
    try {
      const response = await this.client.get('/health');
      return response.data;
    } catch (error) {
      throw this.handleMedicalError(error);
    }
  }

  // Core analytics summary for medical dashboard
  async getAnalyticsSummary(): Promise<AnalyticsSummary> {
    try {
      // Get dashboard data and articles to calculate missing fields
      const [dashboardResponse, articlesResponse] = await Promise.all([
        this.client.get<ApiAnalyticsResponse>('/api/analytics/dashboard'),
        this.client.get<ApiArticlesResponse>('/api/articles/?size=200')
      ]);

      const dashboardData = dashboardResponse.data;
      const articles = articlesResponse.data.items || [];

      // Calculate language distribution from articles
      const languageCount = articles.reduce((acc: Record<string, number>, article: any) => {
        const lang = article.language === 'es' ? 'spanish' : 'english';
        acc[lang] = (acc[lang] || 0) + 1;
        return acc;
      }, {});

      // Calculate top country and source from articles
      const countryCount = articles.reduce((acc: Record<string, number>, article: any) => {
        const country = article.country || 'Unknown';
        acc[country] = (acc[country] || 0) + 1;
        return acc;
      }, {});

      const sourceCount = articles.reduce((acc: Record<string, number>, article: any) => {
        const sourceName = article.source?.name || 'Unknown';
        acc[sourceName] = (acc[sourceName] || 0) + 1;
        return acc;
      }, {});

      const topCountry = Object.entries(countryCount)
        .filter(([country]) => country !== 'Global' && country !== 'Unknown')
        .sort(([,a], [,b]) => (b as number) - (a as number))[0]?.[0] || 'N/A';

      const topSource = Object.entries(sourceCount)
        .sort(([,a], [,b]) => (b as number) - (a as number))[0]?.[0] || 'N/A';

      // Calculate total language articles for percentage
      const totalLanguageArticles = (languageCount.spanish || 0) + (languageCount.english || 0);

      return {
        totalArticles: dashboardData.total_articles || articles.length,
        totalSources: dashboardData.total_sources || Object.keys(sourceCount).length,
        languageDistribution: {
          español: totalLanguageArticles > 0 ? Math.round(((languageCount.spanish || 0) / totalLanguageArticles) * 100) : 0,
          inglés: totalLanguageArticles > 0 ? Math.round(((languageCount.english || 0) / totalLanguageArticles) * 100) : 0,
        },
        sentimentDistribution: {
          positive: dashboardData.sentiment_distribution?.positive || 0,
          negative: dashboardData.sentiment_distribution?.negative || 0,
          neutral: dashboardData.sentiment_distribution?.neutral || 0,
        },
        topCountry,
        topSource,
        lastUpdated: new Date().toISOString(),
      };
    } catch (error) {
      throw this.handleMedicalError(error);
    }
  }

  // Sentiment distribution for medical visualization
  async getSentimentDistribution(filters?: MedicalFilters): Promise<SentimentData[]> {
    try {
      const params = this.buildFilterParams(filters);
      const response = await this.client.get('/api/analytics/dashboard', { params });

      const distribution = response.data.sentiment_distribution || {};
      const total = (distribution.positive || 0) + (distribution.negative || 0) + (distribution.neutral || 0);

      if (total === 0) {
        return [
          { sentiment: 'neutral', value: 0, percentage: 0, color: '#6b7280' }
        ];
      }

      return [
        {
          sentiment: 'positive' as const,
          value: distribution.positive || 0,
          percentage: Math.round(((distribution.positive || 0) / total) * 100),
          color: '#10b981' // Medical green
        },
        {
          sentiment: 'negative' as const,
          value: distribution.negative || 0,
          percentage: Math.round(((distribution.negative || 0) / total) * 100),
          color: '#ef4444' // Medical red
        },
        {
          sentiment: 'neutral' as const,
          value: distribution.neutral || 0,
          percentage: Math.round(((distribution.neutral || 0) / total) * 100),
          color: '#6b7280' // Medical gray
        }
      ].filter(item => item.value > 0);
    } catch (error) {
      throw this.handleMedicalError(error);
    }
  }

  // Geographic distribution for medical coverage mapping
  async getGeographicDistribution(): Promise<GeographicData[]> {
    try {
      const response = await this.client.get<ApiGeographicResponse>('/api/analytics/geographic/distribution');

      // The API returns { distribution: { "Other/Unknown": { article_count: 106, avg_sentiment: -0.426 } } }
      const distribution = response.data.distribution || {};

      return Object.entries(distribution).map(([countryName, data]: [string, any]) => ({
        code: countryName.toLowerCase().replace(/[^a-z]/g, ''),
        name: countryName,
        lat: 0, // Default coordinates since not provided by API
        lon: 0,
        articleCount: data.article_count || 0,
        predominantSentiment: data.avg_sentiment > 0 ? 'positive' as const :
                             data.avg_sentiment < 0 ? 'negative' as const :
                             'neutral' as const,
        primaryLanguage: 'english', // Default since not provided
      }));
    } catch (error) {
      throw this.handleMedicalError(error);
    }
  }

  // Topics distribution for medical categorization
  async getTopicsDistribution(): Promise<TopicData[]> {
    try {
      const response = await this.client.get<ApiTopicsResponse>('/api/analytics/topics/distribution');

      // The API returns { distribution: { "treatment": 39, "general": 19, ... } }
      const distribution = response.data.distribution || {};

      return Object.entries(distribution).map(([topicName, count]: [string, any]) => ({
        topic: topicName,
        español: 0, // API doesn't provide language breakdown
        inglés: 0,
        total: count || 0,
      }));
    } catch (error) {
      throw this.handleMedicalError(error);
    }
  }

  // Weekly trends for medical temporal analysis
  async getWeeklyTrends(): Promise<TrendData[]> {
    try {
      const response = await this.client.get('/api/analytics/trends/weekly');

      return (response.data.trends || []).map((trend: any) => ({
        week: trend.week,
        positive: trend.positive_percentage || 0,
        negative: trend.negative_percentage || 0,
        neutral: trend.neutral_percentage || 0,
        total: trend.total_articles || 0,
      }));
    } catch (error) {
      throw this.handleMedicalError(error);
    }
  }

  // Articles retrieval with medical filtering
  async getArticles(filters: MedicalFilters = {}): Promise<PaginatedArticles> {
    try {
      // Use the articles/ endpoint with size=200 to get all articles
      const response = await this.client.get<ApiArticlesResponse>('/api/articles/?size=200');

      // The API returns { items: [...] } format
      const items = response.data.items || [];

      return {
        articles: items.map((item: unknown) => this.transformArticle(item as Record<string, unknown>)),
        total: items.length,
        page: 1,
        limit: items.length,
        hasNext: false,
        hasPrevious: false,
      };
    } catch (error) {
      throw this.handleMedicalError(error);
    }
  }

  // Individual article retrieval for medical detail view
  async getArticle(articleId: number): Promise<MedicalArticle> {
    try {
      const response = await this.client.get(`/api/articles/${articleId}`);
      return this.transformArticle(response.data);
    } catch (error) {
      throw this.handleMedicalError(error);
    }
  }

  // Source credibility analysis for medical trust assessment
  async getSourceCredibility(): Promise<SourceCredibility[]> {
    try {
      const response = await this.client.get('/api/analytics/sources/performance');

      return (response.data.sources || []).map((source: any) => ({
        source: source.name,
        credibilityScore: source.credibility_score || 0,
        articleCount: source.article_count || 0,
        averageSentiment: source.average_sentiment || 0,
        reliability: this.calculateReliability(source.credibility_score || 0),
      }));
    } catch (error) {
      throw this.handleMedicalError(error);
    }
  }

  // Articles statistics summary
  async getArticlesStats(): Promise<{ summary: any }> {
    try {
      const response = await this.client.get('/api/articles/stats/summary');
      return response.data;
    } catch (error) {
      throw this.handleMedicalError(error);
    }
  }

  // Helper method to transform API article to MedicalArticle type
  private transformArticle(apiArticle: Record<string, unknown>): MedicalArticle {
    // Safe casting function
    const getString = (key: string, fallback = ''): string =>
      typeof apiArticle[key] === 'string' ? apiArticle[key] as string : fallback;

    const getNumber = (key: string, fallback = 0): number =>
      typeof apiArticle[key] === 'number' ? apiArticle[key] as number : fallback;

    const getArray = (key: string, fallback: string[] = []): string[] =>
      Array.isArray(apiArticle[key]) ? apiArticle[key] as string[] : fallback;

    const getSentiment = (key: string): 'positive' | 'negative' | 'neutral' => {
      const value = getString(key);
      return ['positive', 'negative', 'neutral'].includes(value)
        ? value as 'positive' | 'negative' | 'neutral'
        : 'neutral';
    };

    return {
      id: getNumber('id'),
      title: getString('title'),
      url: getString('url'),
      summary: getString('summary'),
      content: getString('content'),
      publishedAt: getString('published_at') || getString('publishedAt'),
      source: getString('source'),
      language: getString('language', 'english'),
      country: getString('country'),

      // NLP Analysis Results
      sentimentLabel: getSentiment('sentiment_label') || getSentiment('sentimentLabel'),
      sentimentScore: getNumber('sentiment_score') || getNumber('sentimentScore'),
      sentimentConfidence: getNumber('sentiment_confidence') || getNumber('sentimentConfidence'),
      topicCategory: getString('topic_category') || getString('topicCategory'),

      // Medical metadata
      keywords: getArray('keywords'),
      relevanceScore: getNumber('relevance_score') || getNumber('relevanceScore'),
      medicalTermsCount: getNumber('medical_terms_count'),

      // Timestamps
      createdAt: getString('created_at') || getString('createdAt'),
      updatedAt: getString('updated_at') || getString('updatedAt'),
    };
  }

  // Helper method to build filter parameters
  private buildFilterParams(filters?: MedicalFilters): Record<string, string | number> {
    if (!filters) return {};

    const params: Record<string, string | number> = {};

    if (filters.country && filters.country !== 'all') {
      params.country = filters.country;
    }
    if (filters.language && filters.language !== 'all') {
      params.language = filters.language === 'español' ? 'spanish' : 'english';
    }
    if (filters.sentiment && filters.sentiment !== 'all') {
      params.sentiment = filters.sentiment;
    }
    if (filters.topic) {
      params.topic = filters.topic;
    }
    if (filters.source) {
      params.source = filters.source;
    }
    if (filters.startDate) {
      params.start_date = filters.startDate;
    }
    if (filters.endDate) {
      params.end_date = filters.endDate;
    }
    if (filters.searchQuery) {
      params.search = filters.searchQuery;
    }
    if (filters.limit) {
      params.limit = filters.limit;
    }
    if (filters.offset) {
      params.offset = filters.offset;
    }

    return params;
  }

  // Helper method to calculate source reliability
  private calculateReliability(score: number): 'high' | 'medium' | 'low' {
    if (score >= 0.8) return 'high';
    if (score >= 0.6) return 'medium';
    return 'low';
  }
}

// Singleton instance for medical API client
export const medicalApiClient = new MedicalApiClient();

// Export default instance
export default medicalApiClient;
