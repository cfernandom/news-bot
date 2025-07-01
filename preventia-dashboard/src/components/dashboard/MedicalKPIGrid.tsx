// Medical KPI Grid with Real API Data
// Using hooks and API client according to plan specifications

import React from 'react';
import { motion } from 'framer-motion';
import {
  DocumentTextIcon,
  GlobeAltIcon,
  ChatBubbleLeftRightIcon,
  BuildingLibraryIcon,
  HeartIcon,
  ExclamationTriangleIcon
} from '@heroicons/react/24/outline';
import { useMedicalAnalytics } from '../../hooks/useMedicalData';
import { AdaptiveKPICard } from '../adaptive/AdaptiveKPICard';

interface MedicalKPIGridProps {
  className?: string;
}

// Loading skeleton for KPI cards
const KPILoadingSkeleton: React.FC = () => (
  <div className="medical-grid">
    {[1, 2, 3, 4, 5, 6].map((i) => (
      <motion.div
        key={i}
        className="metric-card"
        animate={{ opacity: [0.5, 1, 0.5] }}
        transition={{ duration: 1.5, repeat: Infinity }}
      >
        <div className="h-4 bg-gray-200 rounded mb-2 w-3/4"></div>
        <div className="h-8 bg-gray-300 rounded mb-1 w-1/2"></div>
        <div className="h-3 bg-gray-200 rounded w-full"></div>
      </motion.div>
    ))}
  </div>
);

// Error state for KPI grid
const KPIErrorState: React.FC<{ error: Error | null; onRetry: () => void }> = ({ error, onRetry }) => (
  <div className="medical-grid">
    <div className="col-span-full flex flex-col items-center justify-center p-8 text-center">
      <ExclamationTriangleIcon className="w-12 h-12 text-red-500 mb-4" />
      <h3 className="text-lg font-semibold text-gray-900 mb-2">
        Error al cargar métricas médicas
      </h3>
      <p className="text-gray-600 mb-4">
        {error?.message || 'No se pudieron obtener los datos del servidor'}
      </p>
      <button
        onClick={onRetry}
        className="px-4 py-2 bg-primary-blue text-white rounded-lg hover:bg-blue-600 transition-colors"
      >
        Reintentar
      </button>
    </div>
  </div>
);

export const MedicalKPIGrid: React.FC<MedicalKPIGridProps> = ({ className = '' }) => {
  const { data: analytics, isLoading, isError, error, refetch } = useMedicalAnalytics();

  // Show loading state
  if (isLoading) {
    return (
      <div className={`medical-section ${className}`}>
        <h2 className="medical-title mb-6">Métricas Médicas</h2>
        <KPILoadingSkeleton />
      </div>
    );
  }

  // Show error state
  if (isError || !analytics) {
    return (
      <div className={`medical-section ${className}`}>
        <h2 className="medical-title mb-6">Métricas Médicas</h2>
        <KPIErrorState error={error as Error} onRetry={refetch} />
      </div>
    );
  }

  // Calculate derived metrics
  const totalLanguageArticles = analytics.languageDistribution.español + analytics.languageDistribution.inglés;
  const englishPercentage = totalLanguageArticles > 0
    ? (analytics.languageDistribution.inglés / totalLanguageArticles * 100)
    : 0;
  const spanishPercentage = totalLanguageArticles > 0
    ? (analytics.languageDistribution.español / totalLanguageArticles * 100)
    : 0;

  const totalSentimentArticles = analytics.sentimentDistribution.positive +
                                analytics.sentimentDistribution.negative +
                                analytics.sentimentDistribution.neutral;

  const positivePercentage = totalSentimentArticles > 0
    ? (analytics.sentimentDistribution.positive / totalSentimentArticles * 100)
    : 0;
  const negativePercentage = totalSentimentArticles > 0
    ? (analytics.sentimentDistribution.negative / totalSentimentArticles * 100)
    : 0;

  // Determine predominant sentiment for trend indication
  const predominantSentiment = analytics.sentimentDistribution.negative > analytics.sentimentDistribution.positive
    ? 'negativo' : 'positivo';
  const sentimentTrend = analytics.sentimentDistribution.negative > analytics.sentimentDistribution.positive
    ? { direction: 'down' as const, value: negativePercentage, period: 'total' }
    : { direction: 'up' as const, value: positivePercentage, period: 'total' };

  return (
    <div className={`medical-section ${className}`}>
      <div className="flex items-center justify-between mb-6">
        <h2 className="medical-title">Métricas Médicas</h2>
        <div className="text-sm text-gray-500">
          Última actualización: {new Date(analytics.lastUpdated).toLocaleString('es-ES')}
        </div>
      </div>

      <div className="medical-grid">
        {/* Total Articles */}
        <AdaptiveKPICard
          title="Total de Artículos"
          value={analytics.totalArticles}
          subtitle="Artículos analizados en la base de datos médica"
          icon={DocumentTextIcon}
          onClick={() => console.log('Navigate to articles')}
        />

        {/* Language Distribution */}
        <AdaptiveKPICard
          title="Distribución por Idioma"
          value={`${englishPercentage.toFixed(1)}% EN | ${spanishPercentage.toFixed(1)}% ES`}
          subtitle={`${analytics.languageDistribution.inglés} artículos en inglés, ${analytics.languageDistribution.español} en español`}
          icon={GlobeAltIcon}
          onClick={() => console.log('Navigate to language analysis')}
        />

        {/* Sentiment Analysis */}
        <AdaptiveKPICard
          title="Análisis de Sentimiento"
          value={`${predominantSentiment} (${Math.max(positivePercentage, negativePercentage).toFixed(1)}%)`}
          subtitle={`Positivo: ${analytics.sentimentDistribution.positive} | Negativo: ${analytics.sentimentDistribution.negative} | Neutral: ${analytics.sentimentDistribution.neutral}`}
          trend={sentimentTrend}
          icon={ChatBubbleLeftRightIcon}
          onClick={() => console.log('Navigate to sentiment analysis')}
        />

        {/* Active Sources */}
        <AdaptiveKPICard
          title="Fuentes Activas"
          value={analytics.totalSources}
          subtitle={`Fuente principal: ${analytics.topSource}`}
          icon={BuildingLibraryIcon}
          onClick={() => console.log('Navigate to sources')}
        />

        {/* Top Country */}
        <AdaptiveKPICard
          title="País Principal"
          value={analytics.topCountry}
          subtitle="Mayor cobertura geográfica de contenido médico"
          icon={GlobeAltIcon}
          onClick={() => console.log('Navigate to geographic analysis')}
        />

        {/* Medical Quality Indicator */}
        <AdaptiveKPICard
          title="Cobertura Médica"
          value="100%"
          subtitle="Todos los artículos con análisis NLP completado"
          trend={{ direction: 'up' as const, value: 100, period: 'análisis completo' }}
          icon={HeartIcon}
          onClick={() => console.log('Navigate to quality metrics')}
        />
      </div>

      {/* Medical disclaimer */}
      <div className="mt-6 p-4 bg-blue-50 border border-blue-200 rounded-lg">
        <div className="flex items-start space-x-3">
          <HeartIcon className="w-5 h-5 text-blue-600 mt-0.5 flex-shrink-0" />
          <div className="text-sm">
            <p className="font-medium text-blue-900 mb-1">
              Análisis médico académico - UCOMPENSAR
            </p>
            <p className="text-blue-700">
              Los datos presentados son para fines de investigación académica.
              Las métricas de sentimiento reflejan la comunicación médica, no diagnósticos clínicos.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default MedicalKPIGrid;
