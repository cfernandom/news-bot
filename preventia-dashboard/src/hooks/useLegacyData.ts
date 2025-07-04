import { useQuery } from '@tanstack/react-query';
import apiClient from '../api/client';

// Types for legacy data
interface LegacyArticle {
  id: number;
  title: string;
  summary: string;
  published_at: string;
  source_name: string;
  sentiment_label?: string;
  topic_category?: string;
  url: string;
}

interface LegacySentimentData {
  sentiment_label: string;
  count: number;
  percentage?: number;
  temporal_evolution?: Array<{ day: string; positive: number; negative: number; neutral: number; }>;
  ai_summary?: string;
}

interface LegacyTopicData {
  topic_category: string;
  count: number;
  percentage?: number;
}

interface LegacyGeographicData {
  country: string;
  lat: number;
  lon: number;
  total: number;
  idioma: string;
  tono: string;
  detalles: {
    positivo: number;
    negativo: number;
    neutro: number;
  };
}

// Extended array types with additional properties
interface LegacySentimentArray extends Array<LegacySentimentData> {
  temporal_evolution?: Array<{ day: string; positive: number; negative: number; neutral: number; }>;
  ai_summary?: string;
}

interface LegacyTopicArray extends Array<LegacyTopicData> {
  ai_summary?: string;
}

interface LegacyGeographicArray extends Array<LegacyGeographicData> {
  ai_summary?: string;
}

interface LegacyStats {
  total_articles: number;
  positive_sentiment: number;
  negative_sentiment: number;
  neutral_sentiment: number;
  dominant_language: string;
  language_percentage: number;
  sources_count: number;
  latest_article_date: string;
  most_active_country?: string;
  most_frequent_source?: string;
  daily_articles?: Array<{ day: string; count: number; }>;
  ai_summary?: string;
}

// Custom hooks for legacy data
export const useLegacyArticles = (page: number = 1, limit: number = 20) => {
  return useQuery({
    queryKey: ['legacy-articles', page, limit],
    queryFn: async () => {
      const response = await apiClient.get(`/api/v1/news?page=${page}&page_size=${limit}`);
      return response.data;
    },
    staleTime: 5 * 60 * 1000, // 5 minutes
  });
};

export const useLegacySentimentStats = (filters?: any) => {
  return useQuery({
    queryKey: ['legacy-sentiment-stats', filters],
    queryFn: async (): Promise<LegacySentimentArray> => {
      const response = await apiClient.get('/api/v1/stats/tones');
      const data = response.data.data;

      console.log('API Response for sentiment stats:', data);

      // Transform to expected format
      const result = [
        { sentiment_label: 'positive', count: data.positive || 0 },
        { sentiment_label: 'negative', count: data.negative || 0 },
        { sentiment_label: 'neutral', count: data.neutral || 0 }
      ] as LegacySentimentArray;

      // Add mock data for temporal evolution and AI summary
      result.temporal_evolution = [
        { day: '2025-06-29', positive: 0, negative: 0, neutral: 0 },
        { day: '2025-06-30', positive: 0, negative: 0, neutral: 0 },
        { day: '2025-07-01', positive: 0, negative: 0, neutral: 0 },
        { day: '2025-07-02', positive: 0, negative: 0, neutral: 0 },
        { day: '2025-07-03', positive: 0, negative: 0, neutral: 0 }
      ];

      result.ai_summary = "No se pudo establecer conexión.";

      return result;
    },
    staleTime: 5 * 60 * 1000,
  });
};

export const useLegacyTopicsStats = (filters?: any) => {
  return useQuery({
    queryKey: ['legacy-topics-stats', filters],
    queryFn: async (): Promise<LegacyTopicArray> => {
      const response = await apiClient.get('/api/v1/stats/topics');
      const data = response.data.data;

      // Transform to expected format
      const result = Object.entries(data || {}).map(([topic, count]) => ({
        topic_category: topic,
        count: count as number
      })) as LegacyTopicArray;

      // Add AI summary
      result.ai_summary = "No se pudo establecer conexión.";

      return result;
    },
    staleTime: 5 * 60 * 1000,
  });
};

export const useLegacyGeneralStats = () => {
  return useQuery({
    queryKey: ['legacy-general-stats'],
    queryFn: async (): Promise<LegacyStats> => {
      try {
        // Get comprehensive data from multiple endpoints
        const [newsResponse, tonesResponse, languageResponse] = await Promise.all([
          apiClient.get('/api/v1/news?page=1&page_size=1'), // Get total count from meta
          apiClient.get('/api/v1/stats/tones'), // Get total sentiment distribution
          apiClient.get('/api/v1/analytics/language-distribution') // Get language distribution
        ]);

        const newsData = newsResponse.data;
        const tonesData = tonesResponse.data.data;
        const languageData = languageResponse.data.data || [];

        // Calculate dominant language
        const totalLanguageArticles = languageData.reduce((sum: number, item: any) => sum + item.count, 0);
        const englishData = languageData.find((item: any) => item.sentiment_label === 'english');
        const spanishData = languageData.find((item: any) => item.sentiment_label === 'spanish');

        const englishCount = englishData?.count || 0;
        const spanishCount = spanishData?.count || 0;

        const dominantLanguage = englishCount > spanishCount ? 'Inglés' : 'Español';
        const dominantPercentage = totalLanguageArticles > 0 ?
          Math.round(((englishCount > spanishCount ? englishCount : spanishCount) / totalLanguageArticles) * 100) : 0;

        return {
          total_articles: newsData.meta?.total || 0,
          positive_sentiment: tonesData.positive || 0,
          negative_sentiment: tonesData.negative || 0,
          neutral_sentiment: tonesData.neutral || 0,
          dominant_language: dominantLanguage,
          language_percentage: dominantPercentage,
          sources_count: 4, // Known from database setup
          latest_article_date: new Date().toISOString().split('T')[0],
          most_active_country: 'Estados Unidos', // Based on current data sources
          most_frequent_source: 'News Medical', // Based on current scraping results
          daily_articles: [], // Will be loaded separately
          ai_summary: `Análisis basado en ${newsData.meta?.total || 0} artículos con distribución de sentimientos: ${tonesData.positive || 0} positivos, ${tonesData.negative || 0} negativos, ${tonesData.neutral || 0} neutrales.`
        };
      } catch (error) {
        console.error('Failed to fetch general stats:', error);
        // Return minimal data to avoid showing hardcoded fallbacks
        return {
          total_articles: 0,
          positive_sentiment: 0,
          negative_sentiment: 0,
          neutral_sentiment: 0,
          dominant_language: 'Sin datos',
          language_percentage: 0,
          sources_count: 0,
          latest_article_date: 'Sin datos',
          most_active_country: 'Sin datos',
          most_frequent_source: 'Sin datos',
          daily_articles: [],
          ai_summary: "No se pudo establecer conexión con la API para generar el resumen."
        };
      }
    },
    staleTime: 5 * 60 * 1000,
  });
};

// Geographic data from real API endpoint - organized by countries as per endpoints.md spec
export const useLegacyGeographicData = (filters?: any) => {
  return useQuery({
    queryKey: ['legacy-geographic', filters],
    queryFn: async (): Promise<LegacyGeographicArray> => {
      try {
        const response = await apiClient.get('/api/v1/stats/geo');
        const geoData = response.data.data || [];

        // Country mapping for display and coordinates as per endpoints.md
        const countryMapping: { [key: string]: { name: string, lat: number, lon: number, idioma: string } } = {
          'US': { name: 'Estados Unidos', lat: 39.8, lon: -98.5, idioma: 'Inglés' },
          'UK': { name: 'Reino Unido', lat: 55.4, lon: -3.4, idioma: 'Inglés' },
          'Other': { name: 'Otros', lat: 0, lon: 0, idioma: 'Varios' }
        };

        // Sentiment translation
        const sentimentMapping: { [key: string]: string } = {
          'positive': 'Positivo',
          'negative': 'Negativo',
          'neutral': 'Neutro'
        };

        // Group data by country to show aggregated totals per country
        const countryAggregates: { [key: string]: { positive: number, negative: number, neutral: number } } = {};

        geoData.forEach((item: any) => {
          const country = item.country; // US, UK, Other as returned by API
          if (!countryAggregates[country]) {
            countryAggregates[country] = { positive: 0, negative: 0, neutral: 0 };
          }
          // The API returns individual records per country+sentiment, so we aggregate them
          const tone = item.tone || 'neutral';
          if (tone in countryAggregates[country]) {
            countryAggregates[country][tone as keyof typeof countryAggregates[typeof country]] += item.total;
          }
        });

        const result = Object.entries(countryAggregates).map(([country, counts]) => {
          const countryInfo = countryMapping[country] || {
            name: country,
            lat: 0,
            lon: 0,
            idioma: 'Desconocido'
          };

          // Calculate total and dominant sentiment
          const total = counts.positive + counts.negative + counts.neutral;
          const dominantTone = counts.negative > counts.positive && counts.negative > counts.neutral ? 'Negativo' :
                             counts.positive > counts.neutral ? 'Positivo' : 'Neutro';

          return {
            country: countryInfo.name,
            lat: countryInfo.lat,
            lon: countryInfo.lon,
            total,
            idioma: countryInfo.idioma,
            tono: dominantTone,
            detalles: {
              positivo: counts.positive,
              negativo: counts.negative,
              neutro: counts.neutral
            }
          };
        }).filter((item: any) => item.total > 0) as LegacyGeographicArray;

        // Add AI summary
        result.ai_summary = "No se pudo establecer conexión.";

        return result;

      } catch (error) {
        console.error('Failed to fetch geographic data:', error);
        // Return empty array to trigger error state in component
        const emptyResult = [] as LegacyGeographicArray;
        emptyResult.ai_summary = "";
        return emptyResult;
      }
    },
    staleTime: 10 * 60 * 1000, // 10 minutes
  });
};

// News data with filters
export const useLegacyNews = (filters?: any) => {
  return useQuery({
    queryKey: ['legacy-news', filters],
    queryFn: async () => {
      try {
        // Build query parameters based on filters
        const params = new URLSearchParams();
        params.append('page', '1');
        params.append('page_size', '50');

        if (filters?.country) params.append('country', filters.country);
        if (filters?.language) params.append('language', filters.language);
        if (filters?.date) params.append('date', filters.date);
        if (filters?.topic) params.append('topic', filters.topic);
        if (filters?.keyword) params.append('search', filters.keyword);

        const response = await apiClient.get(`/api/v1/news?${params.toString()}`);
        const rawData = response.data.data || [];

        // Transform API data to match NewsItem interface expected by LegacyNewsTable
        return rawData.map((item: any) => ({
          id: item.id,
          title: item.title,
          country: item.country,
          language: item.language,
          date: item.date,
          topic: item.topic,
          sentiment: item.tone || 'neutral', // Map 'tone' to 'sentiment'
          url: item.url,
          source: extractSourceName(item.url), // Extract source from URL
          summary: item.summary
        }));
      } catch (error) {
        console.error('Failed to fetch news data:', error);
        return []; // Return empty array to trigger error state in component
      }
    },
    staleTime: 5 * 60 * 1000,
  });
};

// Helper function to extract source name from URL
function extractSourceName(url: string): string {
  try {
    const domain = new URL(url).hostname;
    if (domain.includes('breastcancer.org')) return 'Breast Cancer Org';
    if (domain.includes('webmd.com')) return 'WebMD';
    if (domain.includes('curetoday.com')) return 'CureToday';
    if (domain.includes('news-medical.net')) return 'News Medical';
    if (domain.includes('test.com')) return 'Test Source';
    return domain.replace('www.', '');
  } catch {
    return 'Fuente desconocida';
  }
}

// Language distribution from dedicated API endpoint
// Daily articles timeline
export const useLegacyDailyArticles = (days: number = 14) => {
  return useQuery({
    queryKey: ['legacy-daily-articles', days],
    queryFn: async () => {
      try {
        const response = await apiClient.get(`/api/v1/stats/articles/daily?days=${days}`);
        const data = response.data.data || [];

        console.log('Daily articles data:', data);

        // Transform to format expected by LegacyTrendChart
        return data.map((item: any) => ({
          day: new Date(item.day).toLocaleDateString('es-ES', { weekday: 'short', day: 'numeric', month: 'short' }),
          count: item.count
        }));
      } catch (error) {
        console.error('Failed to fetch daily articles:', error);
        return [];
      }
    },
    staleTime: 5 * 60 * 1000, // 5 minutes
  });
};

// Sentiment timeline (weekly evolution)
export const useLegacySentimentTimeline = (weeks: number = 12) => {
  return useQuery({
    queryKey: ['legacy-sentiment-timeline', weeks],
    queryFn: async () => {
      try {
        const response = await apiClient.get(`/api/v1/stats/tones/timeline?weeks=${weeks}`);
        const data = response.data.data;

        console.log('Sentiment timeline data:', data);

        if (!data || !data.labels) return [];

        // Transform to format expected by LegacyTrendChart with sentiment lines
        return data.labels.map((weekNum: number, index: number) => ({
          week: `Sem ${weekNum}`,
          positive: data.positive[index] || 0,
          negative: data.negative[index] || 0,
          neutral: data.neutral[index] || 0
        }));
      } catch (error) {
        console.error('Failed to fetch sentiment timeline:', error);
        return [];
      }
    },
    staleTime: 5 * 60 * 1000, // 5 minutes
  });
};

// Topics with language breakdown
export const useLegacyTopicsWithLanguage = (weeks: number = 8) => {
  return useQuery({
    queryKey: ['legacy-topics-language', weeks],
    queryFn: async () => {
      try {
        const response = await apiClient.get(`/api/v1/stats/topics/language-breakdown?weeks=${weeks}`);
        const data = response.data.data || [];

        console.log('Topics with language breakdown:', data);

        // Transform to format expected by LegacyTopicsChart with language breakdown
        return data.map((item: any) => ({
          topic_category: item.topic_category,
          count: item.total,
          english: item.english || 0,
          spanish: item.spanish || 0
        }));
      } catch (error) {
        console.error('Failed to fetch topics with language breakdown:', error);
        return [];
      }
    },
    staleTime: 5 * 60 * 1000, // 5 minutes
  });
};

export const useLegacyLanguageStats = () => {
  return useQuery({
    queryKey: ['legacy-language-stats'],
    queryFn: async (): Promise<LegacySentimentArray> => {
      try {
        const response = await apiClient.get('/api/v1/analytics/language-distribution');
        const data = response.data.data || [];

        console.log('Language distribution from API:', data);

        // Data is already in the correct format from the API
        const result = data as LegacySentimentArray;

        // Add empty temporal evolution and AI summary
        result.temporal_evolution = [];
        const totalArticles = data.reduce((sum: number, item: any) => sum + item.count, 0);
        result.ai_summary = `Distribución de idiomas basada en ${totalArticles} artículos analizados desde la base de datos.`;

        return result;
      } catch (error) {
        console.error('Failed to fetch language stats:', error);
        // Return empty array to trigger error state in component
        const emptyResult = [] as LegacySentimentArray;
        emptyResult.temporal_evolution = [];
        emptyResult.ai_summary = "";
        return emptyResult;
      }
    },
    staleTime: 10 * 60 * 1000, // 10 minutes
  });
};

export type {
  LegacyArticle,
  LegacySentimentData,
  LegacyTopicData,
  LegacyGeographicData,
  LegacyStats,
  LegacySentimentArray,
  LegacyTopicArray,
  LegacyGeographicArray
};
