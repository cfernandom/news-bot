// Medical Types for PreventIA Dashboard
// Following the medical domain modeling from the plan

export interface MedicalArticle {
  id: number;
  title: string;
  url: string;
  summary: string;
  content?: string;
  publishedAt: string;
  source: string;
  language: string;
  country?: string;

  // NLP Analysis Results
  sentimentLabel: 'positive' | 'negative' | 'neutral';
  sentimentScore: number;
  sentimentConfidence: number;
  topicCategory?: string;

  // Medical metadata
  keywords: string[];
  relevanceScore: number;
  medicalTermsCount?: number;

  // Timestamps
  createdAt: string;
  updatedAt: string;
}

// Alternative interface matching API response format
export interface Article {
  id: number;
  title: string;
  url: string;
  summary?: string;
  content?: string;
  published_at: string;
  language: string;
  country: string;

  // Source information
  source?: {
    name: string;
    base_url: string;
    language: string;
    country: string;
  };

  // NLP Analysis Results
  sentiment_label?: 'positive' | 'negative' | 'neutral';
  sentiment_score?: number;
  sentiment_confidence?: number;
  topic_category?: string;
  topic_confidence?: number;

  // Processing metadata
  processing_status?: string;
  processing_error?: string;
  word_count?: number;

  // Timestamps
  created_at: string;
  updated_at: string;
  scraped_at: string;
}

export interface AnalyticsSummary {
  totalArticles: number;
  totalSources: number;
  languageDistribution: {
    español: number;
    inglés: number;
  };
  sentimentDistribution: {
    positive: number;
    negative: number;
    neutral: number;
  };
  topCountry: string;
  topSource: string;
  lastUpdated: string;
}

export interface SentimentData {
  sentiment: 'positive' | 'negative' | 'neutral';
  value: number;
  percentage: number;
  color: string;
}

export interface GeographicData {
  code: string;
  name: string;
  lat: number;
  lon: number;
  articleCount: number;
  predominantSentiment: 'positive' | 'negative' | 'neutral';
  primaryLanguage: string;
}

export interface TopicData {
  topic: string;
  español: number;
  inglés: number;
  total: number;
}

export interface TrendData {
  week: string;
  positive: number;
  negative: number;
  neutral: number;
  total: number;
}

export interface MedicalFilters {
  country?: string;
  language?: 'español' | 'inglés' | 'all';
  sentiment?: 'positive' | 'negative' | 'neutral' | 'all';
  topic?: string;
  source?: string;
  startDate?: string;
  endDate?: string;
  searchQuery?: string;
  limit?: number;
  offset?: number;
}

export interface PaginatedArticles {
  articles: MedicalArticle[];
  total: number;
  page: number;
  limit: number;
  hasNext: boolean;
  hasPrevious: boolean;
}

export interface ApiResponse<T> {
  data: T;
  success: boolean;
  message?: string;
  timestamp: string;
}

export interface MedicalError {
  code: string;
  message: string;
  details?: Record<string, any>;
  timestamp: string;
}

// Source credibility types
export interface SourceCredibility {
  source: string;
  credibilityScore: number;
  articleCount: number;
  averageSentiment: number;
  reliability: 'high' | 'medium' | 'low';
}

// Performance metrics for medical dashboard
export interface PerformanceMetrics {
  firstContentfulPaint?: number;
  largestContentfulPaint?: number;
  timeToInteractive?: number;
  apiResponseTime?: number;
  chartRenderTime?: number;
}
