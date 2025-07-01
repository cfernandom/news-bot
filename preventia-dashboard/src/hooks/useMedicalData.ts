// Medical Data Hooks using TanStack Query
// Implementation following fase4-react-dashboard-plan.md specifications

import { useQuery, useQueryClient } from '@tanstack/react-query';
import { medicalApiClient } from '../services/api';
import {
  MedicalFilters,
} from '../types/medical';

// Query keys for medical data cache management
export const MEDICAL_QUERY_KEYS = {
  health: ['medical', 'health'] as const,
  analytics: ['medical', 'analytics'] as const,
  analyticsSummary: ['medical', 'analytics', 'summary'] as const,
  sentiment: ['medical', 'sentiment'] as const,
  sentimentDistribution: (filters?: MedicalFilters) =>
    ['medical', 'sentiment', 'distribution', filters] as const,
  geographic: ['medical', 'geographic'] as const,
  topics: ['medical', 'topics'] as const,
  trends: ['medical', 'trends'] as const,
  weeklyTrends: ['medical', 'trends', 'weekly'] as const,
  articles: (filters?: MedicalFilters) =>
    ['medical', 'articles', filters] as const,
  article: (id: number) =>
    ['medical', 'articles', id] as const,
  sources: ['medical', 'sources'] as const,
  sourceCredibility: ['medical', 'sources', 'credibility'] as const,
  articlesStats: ['medical', 'articles', 'stats'] as const,
} as const;

// Medical cache configuration for clinical data
const MEDICAL_CACHE_CONFIG = {
  // Critical medical data - longer cache for stability
  analytics: 5 * 60 * 1000, // 5 minutes
  articles: 10 * 60 * 1000, // 10 minutes

  // Frequently changing data - shorter cache
  health: 2 * 60 * 1000, // 2 minutes
  trends: 15 * 60 * 1000, // 15 minutes

  // Stable reference data - longer cache
  sources: 30 * 60 * 1000, // 30 minutes
  topics: 30 * 60 * 1000, // 30 minutes
};

// Health check hook for medical API monitoring
export const useMedicalHealth = () => {
  return useQuery({
    queryKey: MEDICAL_QUERY_KEYS.health,
    queryFn: () => medicalApiClient.checkHealth(),
    staleTime: MEDICAL_CACHE_CONFIG.health,
    refetchInterval: MEDICAL_CACHE_CONFIG.health,
    retry: 3,
    retryDelay: (attemptIndex) => Math.min(1000 * 2 ** attemptIndex, 30000),
  });
};

// Main analytics summary for medical dashboard
export const useMedicalAnalytics = () => {
  return useQuery({
    queryKey: MEDICAL_QUERY_KEYS.analyticsSummary,
    queryFn: () => medicalApiClient.getAnalyticsSummary(),
    staleTime: MEDICAL_CACHE_CONFIG.analytics,
    retry: 2,
    meta: {
      medicalContext: 'dashboard-overview',
      critical: true,
    },
  });
};

// Sentiment distribution for medical sentiment analysis
export const useMedicalSentimentDistribution = (filters?: MedicalFilters) => {
  return useQuery({
    queryKey: MEDICAL_QUERY_KEYS.sentimentDistribution(filters),
    queryFn: () => medicalApiClient.getSentimentDistribution(filters),
    staleTime: MEDICAL_CACHE_CONFIG.analytics,
    enabled: true, // Always enabled for medical sentiment monitoring
    retry: 2,
    meta: {
      medicalContext: 'sentiment-analysis',
    },
  });
};

// Geographic distribution for medical coverage mapping
export const useMedicalGeographicDistribution = () => {
  return useQuery({
    queryKey: MEDICAL_QUERY_KEYS.geographic,
    queryFn: () => medicalApiClient.getGeographicDistribution(),
    staleTime: MEDICAL_CACHE_CONFIG.analytics,
    retry: 2,
    meta: {
      medicalContext: 'geographic-coverage',
    },
  });
};

// Topics distribution for medical categorization
export const useMedicalTopicsDistribution = () => {
  return useQuery({
    queryKey: MEDICAL_QUERY_KEYS.topics,
    queryFn: () => medicalApiClient.getTopicsDistribution(),
    staleTime: MEDICAL_CACHE_CONFIG.topics,
    retry: 2,
    meta: {
      medicalContext: 'topic-classification',
    },
  });
};

// Weekly trends for medical temporal analysis
export const useMedicalWeeklyTrends = () => {
  return useQuery({
    queryKey: MEDICAL_QUERY_KEYS.weeklyTrends,
    queryFn: () => medicalApiClient.getWeeklyTrends(),
    staleTime: MEDICAL_CACHE_CONFIG.trends,
    retry: 2,
    meta: {
      medicalContext: 'temporal-trends',
    },
  });
};

// Articles with medical filtering
export const useMedicalArticles = (filters: MedicalFilters = {}) => {
  return useQuery({
    queryKey: MEDICAL_QUERY_KEYS.articles(filters),
    queryFn: () => medicalApiClient.getArticles(filters),
    staleTime: MEDICAL_CACHE_CONFIG.articles,
    retry: 2,
    placeholderData: (previousData) => previousData, // Smooth pagination experience
    meta: {
      medicalContext: 'articles-listing',
    },
  });
};

// Individual article for medical detail view
export const useMedicalArticle = (articleId: number | null) => {
  return useQuery({
    queryKey: MEDICAL_QUERY_KEYS.article(articleId!),
    queryFn: () => medicalApiClient.getArticle(articleId!),
    enabled: articleId !== null && articleId > 0,
    staleTime: MEDICAL_CACHE_CONFIG.articles,
    retry: 2,
    meta: {
      medicalContext: 'article-detail',
    },
  });
};

// Source credibility for medical trust assessment
export const useMedicalSourceCredibility = () => {
  return useQuery({
    queryKey: MEDICAL_QUERY_KEYS.sourceCredibility,
    queryFn: () => medicalApiClient.getSourceCredibility(),
    staleTime: MEDICAL_CACHE_CONFIG.sources,
    retry: 2,
    meta: {
      medicalContext: 'source-credibility',
    },
  });
};

// Articles statistics
export const useMedicalArticlesStats = () => {
  return useQuery({
    queryKey: MEDICAL_QUERY_KEYS.articlesStats,
    queryFn: () => medicalApiClient.getArticlesStats(),
    staleTime: MEDICAL_CACHE_CONFIG.analytics,
    retry: 2,
    meta: {
      medicalContext: 'articles-statistics',
    },
  });
};

// Combined hook for complete medical dashboard data
export const useMedicalDashboard = (filters?: MedicalFilters) => {
  const analytics = useMedicalAnalytics();
  const sentiment = useMedicalSentimentDistribution(filters);
  const geographic = useMedicalGeographicDistribution();
  const topics = useMedicalTopicsDistribution();
  const trends = useMedicalWeeklyTrends();
  const sources = useMedicalSourceCredibility();

  return {
    analytics,
    sentiment,
    geographic,
    topics,
    trends,
    sources,

    // Computed states
    isLoading: analytics.isLoading || sentiment.isLoading || geographic.isLoading,
    isError: analytics.isError || sentiment.isError || geographic.isError,
    error: analytics.error || sentiment.error || geographic.error,

    // Refetch all medical data
    refetchAll: () => {
      analytics.refetch();
      sentiment.refetch();
      geographic.refetch();
      topics.refetch();
      trends.refetch();
      sources.refetch();
    },
  };
};

// Medical filters management hook
export const useMedicalFilters = (initialFilters: MedicalFilters = {}) => {
  const queryClient = useQueryClient();
  const [filters, setFilters] = useState<MedicalFilters>(initialFilters);

  const updateFilters = (newFilters: Partial<MedicalFilters>) => {
    const updatedFilters = { ...filters, ...newFilters };
    setFilters(updatedFilters);

    // Invalidate relevant queries when filters change
    queryClient.invalidateQueries({
      queryKey: MEDICAL_QUERY_KEYS.sentimentDistribution(updatedFilters)
    });
    queryClient.invalidateQueries({
      queryKey: MEDICAL_QUERY_KEYS.articles(updatedFilters)
    });
  };

  const clearFilters = () => {
    setFilters({});
    queryClient.invalidateQueries({ queryKey: ['medical'] });
  };

  return {
    filters,
    updateFilters,
    clearFilters,
    setFilters,
  };
};

// Medical performance monitoring hook
export const useMedicalPerformance = () => {
  const queryClient = useQueryClient();

  const getQueryMetrics = () => {
    const queryCache = queryClient.getQueryCache();
    const medicalQueries = queryCache.getAll().filter(
      query => query.queryKey[0] === 'medical'
    );

    return {
      totalMedicalQueries: medicalQueries.length,
      loadingQueries: medicalQueries.filter(q => q.state.status === 'pending').length,
      errorQueries: medicalQueries.filter(q => q.state.status === 'error').length,
      successQueries: medicalQueries.filter(q => q.state.status === 'success').length,
      staleQueries: medicalQueries.filter(q => q.isStale()).length,
    };
  };

  return {
    getQueryMetrics,
    invalidateAllMedical: () => queryClient.invalidateQueries({ queryKey: ['medical'] }),
    clearMedicalCache: () => queryClient.removeQueries({ queryKey: ['medical'] }),
  };
};

// Export useState for filters hook
import { useState } from 'react';
