// Core types for dual-mode PreventIA dashboard

export type Mode = 'professional' | 'educational';

// User preferences for dual-mode interface
export interface UserPreferences {
  defaultMode: Mode;
  language: 'en' | 'es';
  accessibility: {
    highContrast: boolean;
    reducedMotion: boolean;
    screenReader: boolean;
  };
  professional: {
    showStatisticalDetails: boolean;
    showConfidenceIntervals: boolean;
    defaultChartType: 'detailed' | 'simplified';
    exportFormat: 'csv' | 'json' | 'pdf';
  };
  educational: {
    showDefinitions: boolean;
    showExplanations: boolean;
    enableGuidedTour: boolean;
    simplifyCharts: boolean;
  };
}

// Dual-mode context type
export interface DualModeContextType {
  mode: Mode;
  toggleMode: () => void;
  setMode: (mode: Mode) => void;
  userPreferences: UserPreferences;
  updatePreferences: (prefs: Partial<UserPreferences>) => void;
  isLoading: boolean;
}

// Article data structure (from FastAPI)
export interface Article {
  id: number;
  title: string;
  summary: string;
  url: string;
  source: string;
  published_date: string;
  language: 'en' | 'es';
  country: string;
  sentiment_label?: 'positive' | 'negative' | 'neutral';
  sentiment_score?: number;
  confidence_score?: number;
  topic_category?: string;
  keywords: string[];
  relevance_score: number;
}

// Analytics data structures
export interface AnalyticsSummary {
  totalArticles: number;
  sentimentDistribution: {
    positive: number;
    negative: number;
    neutral: number;
  };
  languageDistribution: {
    en: number;
    es: number;
  };
  topCountries: Array<{
    country: string;
    count: number;
    percentage: number;
  }>;
  topSources: Array<{
    source: string;
    count: number;
    reliability_score?: number;
  }>;
  averageRelevanceScore: number;
  lastUpdated: string;
}

// Chart data types
export interface ChartDataPoint {
  name: string;
  value: number;
  percentage?: number;
  color?: string;
  confidence?: number;
}

export interface TimeSeriesDataPoint {
  date: string;
  positive: number;
  negative: number;
  neutral: number;
  total: number;
}

export interface GeographicDataPoint {
  country: string;
  count: number;
  coordinates: [number, number];
  articles: Article[];
}

// Component props for adaptive components
export interface AdaptiveComponentProps {
  mode: Mode;
  className?: string;
  children?: React.ReactNode;
}

export interface AdaptiveWrapperProps {
  mode?: Mode;
  className?: string;
  children?: React.ReactNode;
  professionalVariant: React.ComponentType<any>;
  educationalVariant: React.ComponentType<any>;
  fallback?: React.ComponentType<any>;
  data?: any;
}

// KPI card props
export interface KPICardProps {
  mode?: Mode;
  className?: string;
  children?: React.ReactNode;
  title: string;
  value: string | number;
  subtitle?: string;
  trend?: {
    direction: 'up' | 'down' | 'stable';
    value: number;
    period: string;
  };
  icon?: React.ComponentType<{ className?: string }>;
  onClick?: () => void;
}

// Chart component props
export interface ChartProps extends AdaptiveComponentProps {
  data: ChartDataPoint[];
  title: string;
  subtitle?: string;
  height?: number;
  showLegend?: boolean;
  showTooltip?: boolean;
  color?: string;
}

// Filter types
export interface FilterOptions {
  sentiment?: ('positive' | 'negative' | 'neutral')[];
  language?: ('en' | 'es')[];
  country?: string[];
  source?: string[];
  dateRange?: {
    start: string;
    end: string;
  };
  relevanceScore?: {
    min: number;
    max: number;
  };
  // Professional mode filters
  confidenceInterval?: [number, number];
  statisticalSignificance?: boolean;
  peerReviewed?: boolean;
  sampleSize?: {
    min: number;
    max: number;
  };
}

// API response types
export interface APIResponse<T> {
  data: T;
  meta?: {
    total: number;
    page: number;
    limit: number;
    hasNext: boolean;
    hasPrev: boolean;
  };
  message?: string;
  timestamp: string;
}

export interface APIError {
  error: string;
  message: string;
  code: number;
  timestamp: string;
}

// Search and pagination
export interface SearchParams {
  query?: string;
  filters?: FilterOptions;
  page?: number;
  limit?: number;
  sortBy?: 'date' | 'relevance' | 'sentiment';
  sortOrder?: 'asc' | 'desc';
}

// Educational mode specific types
export interface MedicalDefinition {
  term: string;
  simple: string;
  detailed: string;
  examples?: string[];
  relatedTerms?: string[];
}

export interface LearningObjective {
  id: string;
  title: string;
  description: string;
  completed: boolean;
  requiredActions: string[];
}

export interface GuidedTourStep {
  id: string;
  target: string;
  title: string;
  content: string;
  explanation?: string;
  position: 'top' | 'bottom' | 'left' | 'right';
  actions?: Array<{
    type: 'click' | 'hover' | 'scroll';
    target: string;
    description: string;
  }>;
}

// Professional mode specific types
export interface StatisticalMetrics {
  mean: number;
  median: number;
  standardDeviation: number;
  confidenceInterval: [number, number];
  sampleSize: number;
  pValue?: number;
  effectSize?: number;
}

export interface ResearchExport {
  format: 'csv' | 'json' | 'pdf' | 'bibtex';
  includeMetadata: boolean;
  includeStatistics: boolean;
  includeCharts: boolean;
  dateRange?: {
    start: string;
    end: string;
  };
  filters?: FilterOptions;
}

// Performance monitoring
export interface PerformanceMetrics {
  loadTime: number;
  renderTime: number;
  apiResponseTime: number;
  chartRenderTime: number;
  mode: Mode;
  timestamp: string;
}

// Accessibility types
export interface AccessibilityFeatures {
  ariaLabel?: string;
  ariaDescription?: string;
  role?: string;
  tabIndex?: number;
  keyboardShortcuts?: Record<string, () => void>;
  screenReaderText?: string;
}

// Theme and styling
export interface ThemeConfig {
  mode: Mode;
  colorScheme: 'light' | 'dark' | 'auto';
  fontSize: 'small' | 'medium' | 'large';
  contrast: 'normal' | 'high';
  animations: boolean;
}

// Export all types
// Note: React types imported directly where needed
