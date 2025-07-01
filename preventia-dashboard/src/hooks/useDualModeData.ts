import { useQuery, UseQueryResult } from '@tanstack/react-query';
import { useDualMode } from '../contexts/DualModeContext';
import { apiQueries, PreventiaAPI } from '../api/client';
import { AnalyticsSummary, Article, Mode } from '../types';

// Data adaptation utilities
const adaptDataForMode = <T>(data: T, mode: Mode): T => {
  // For now, return data as-is
  // Later we can implement mode-specific data transformations
  return data;
};

// Format numbers based on mode
const formatNumberForMode = (value: number, mode: Mode): string => {
  if (mode === 'professional') {
    return value.toLocaleString('en-US', { maximumFractionDigits: 2 });
  } else {
    // Educational mode - simpler formatting
    return value.toLocaleString('es-ES');
  }
};

// Format percentages based on mode
const formatPercentageForMode = (value: number, mode: Mode): string => {
  const percentage = (value * 100).toFixed(mode === 'professional' ? 1 : 0);
  return `${percentage}%`;
};

// Custom hook for analytics summary with dual-mode adaptation
export const useDualAnalyticsSummary = (): UseQueryResult<AnalyticsSummary> & {
  formattedData: {
    totalArticles: string;
    sentimentDistribution: {
      positive: string;
      negative: string;
      neutral: string;
    };
    topCountry: string;
    topSource: string;
  };
} => {
  const { mode } = useDualMode();
  const query = useQuery(apiQueries.analyticsSummary());

  const formattedData = {
    totalArticles: query.data ? formatNumberForMode(query.data.totalArticles, mode) : '0',
    sentimentDistribution: {
      positive: query.data ?
        formatPercentageForMode(query.data.sentimentDistribution.positive / query.data.totalArticles, mode) : '0%',
      negative: query.data ?
        formatPercentageForMode(query.data.sentimentDistribution.negative / query.data.totalArticles, mode) : '0%',
      neutral: query.data ?
        formatPercentageForMode(query.data.sentimentDistribution.neutral / query.data.totalArticles, mode) : '0%',
    },
    topCountry: query.data?.topCountries[0]?.country || 'N/A',
    topSource: query.data?.topSources[0]?.source || 'N/A',
  };

  return {
    ...query,
    formattedData,
  };
};

// Custom hook for article count with dual-mode formatting
export const useDualArticleCount = () => {
  const { mode } = useDualMode();
  const query = useQuery(apiQueries.articleCount());

  const formattedData = {
    total: query.data ? formatNumberForMode(query.data.total, mode) : '0',
    english: query.data ? formatNumberForMode(query.data.by_language.en || 0, mode) : '0',
    spanish: query.data ? formatNumberForMode(query.data.by_language.es || 0, mode) : '0',
    englishPercentage: query.data && query.data.total > 0 ?
      formatPercentageForMode((query.data.by_language.en || 0) / query.data.total, mode) : '0%',
    spanishPercentage: query.data && query.data.total > 0 ?
      formatPercentageForMode((query.data.by_language.es || 0) / query.data.total, mode) : '0%',
  };

  return {
    ...query,
    formattedData,
  };
};

// Custom hook for sentiment distribution with dual-mode adaptation
export const useDualSentimentDistribution = () => {
  const { mode } = useDualMode();
  const query = useQuery(apiQueries.sentimentDistribution());

  const adaptedData = query.data ? {
    // Professional mode - exact numbers and percentages
    professional: {
      positive: {
        count: query.data.positive,
        percentage: formatPercentageForMode(
          query.data.positive / (query.data.positive + query.data.negative + query.data.neutral),
          'professional'
        ),
      },
      negative: {
        count: query.data.negative,
        percentage: formatPercentageForMode(
          query.data.negative / (query.data.positive + query.data.negative + query.data.neutral),
          'professional'
        ),
      },
      neutral: {
        count: query.data.neutral,
        percentage: formatPercentageForMode(
          query.data.neutral / (query.data.positive + query.data.negative + query.data.neutral),
          'professional'
        ),
      },
    },
    // Educational mode - simplified descriptions
    educational: {
      positive: {
        count: query.data.positive,
        description: query.data.positive > 20 ? 'Muchas noticias positivas' :
                    query.data.positive > 10 ? 'Algunas noticias positivas' : 'Pocas noticias positivas',
        emoji: '😊',
      },
      negative: {
        count: query.data.negative,
        description: query.data.negative > 50 ? 'Mayoría de noticias preocupantes' :
                    query.data.negative > 20 ? 'Varias noticias preocupantes' : 'Pocas noticias preocupantes',
        emoji: '😟',
      },
      neutral: {
        count: query.data.neutral,
        description: query.data.neutral > 20 ? 'Muchas noticias informativas' :
                    query.data.neutral > 5 ? 'Algunas noticias informativas' : 'Pocas noticias informativas',
        emoji: '📊',
      },
    },
  } : null;

  return {
    ...query,
    adaptedData,
    currentModeData: adaptedData?.[mode] || null,
  };
};

// Custom hook for geographic distribution with dual-mode formatting
export const useDualGeographicDistribution = () => {
  const { mode } = useDualMode();
  const query = useQuery(apiQueries.geographicDistribution());

  const adaptedData = query.data?.map(country => ({
    ...country,
    formattedCount: formatNumberForMode(country.count, mode),
    description: mode === 'educational' ?
      `${country.country} tiene ${country.count} ${country.count === 1 ? 'artículo' : 'artículos'}` :
      `${country.country}: ${country.count} articles`,
  })) || [];

  return {
    ...query,
    adaptedData,
  };
};

// Custom hook for articles with dual-mode adaptation
export const useDualArticles = (params?: any) => {
  const { mode } = useDualMode();
  const query = useQuery(apiQueries.articles(params));

  const adaptedArticles = query.data?.data?.map((article: Article) => ({
    ...article,
    formattedDate: new Date(article.published_date).toLocaleDateString(
      mode === 'professional' ? 'en-US' : 'es-ES',
      {
        year: 'numeric',
        month: mode === 'professional' ? 'short' : 'long',
        day: 'numeric'
      }
    ),
    sentimentDisplay: mode === 'educational' ? {
      positive: '😊 Positivo',
      negative: '😟 Preocupante',
      neutral: '📊 Informativo',
    }[article.sentiment_label || 'neutral'] : article.sentiment_label,
    relevanceDisplay: mode === 'educational' ?
      article.relevance_score > 0.8 ? 'Muy relevante' :
      article.relevance_score > 0.6 ? 'Relevante' : 'Algo relevante' :
      `${(article.relevance_score * 100).toFixed(1)}%`,
  })) || [];

  return {
    ...query,
    adaptedArticles,
    meta: query.data?.meta,
  };
};

// Custom hook for API health status
export const useAPIHealth = () => {
  const query = useQuery({
    queryKey: ['api', 'health'],
    queryFn: PreventiaAPI.healthCheck,
    staleTime: 30 * 1000, // 30 seconds
    retry: 3,
    retryDelay: 1000,
  });

  return {
    ...query,
    isHealthy: query.isSuccess && !query.isError,
    status: query.isLoading ? 'checking' :
            query.isError ? 'unhealthy' :
            query.isSuccess ? 'healthy' : 'unknown',
  };
};

// Custom hook for real-time data updates
export const useDualModeRefresh = () => {
  const { mode } = useDualMode();

  // Different refresh strategies based on mode
  const refreshInterval = mode === 'professional' ?
    2 * 60 * 1000 : // Professional: 2 minutes
    5 * 60 * 1000;  // Educational: 5 minutes

  return {
    refreshInterval,
    shouldRefresh: true,
  };
};

// Export all hooks
export {
  formatNumberForMode,
  formatPercentageForMode,
  adaptDataForMode,
};
