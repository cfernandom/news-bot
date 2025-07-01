import React from 'react';
import { motion } from 'framer-motion';
import { ArrowUpIcon, ArrowDownIcon, MinusIcon } from '@heroicons/react/24/outline';
import { KPICardProps } from '../../types';
import { AdaptiveWrapper } from './AdaptiveWrapper';

// Professional mode KPI card - technical and concise
const ProfessionalKPICard: React.FC<KPICardProps & { data?: any }> = ({
  title,
  value,
  subtitle,
  trend,
  icon: Icon,
  onClick,
  className = '',
}) => {
  const getTrendIcon = () => {
    if (!trend) return null;

    const iconClass = "w-4 h-4";
    switch (trend.direction) {
      case 'up':
        return <ArrowUpIcon className={`${iconClass} text-green-600`} />;
      case 'down':
        return <ArrowDownIcon className={`${iconClass} text-red-600`} />;
      default:
        return <MinusIcon className={`${iconClass} text-gray-500`} />;
    }
  };

  const getTrendColor = () => {
    if (!trend) return 'text-gray-600';
    return trend.direction === 'up' ? 'text-green-600' :
           trend.direction === 'down' ? 'text-red-600' : 'text-gray-600';
  };

  return (
    <motion.div
      className={`metric-card cursor-pointer ${className}`}
      onClick={onClick}
      whileHover={{ scale: 1.02 }}
      whileTap={{ scale: 0.98 }}
      transition={{ duration: 0.2 }}
    >
      {/* Header */}
      <div className="flex items-center justify-between mb-2">
        <h3 className="text-sm font-medium text-professional-600 truncate">
          {title}
        </h3>
        {Icon && (
          <Icon className="w-5 h-5 text-professional-400 flex-shrink-0" />
        )}
      </div>

      {/* Main value */}
      <div className="flex items-baseline space-x-2">
        <span className="metric-value text-3xl font-bold text-professional-900">
          {typeof value === 'number' ? value.toLocaleString() : value}
        </span>

        {trend && (
          <div className={`flex items-center space-x-1 ${getTrendColor()}`}>
            {getTrendIcon()}
            <span className="text-sm font-medium">
              {typeof trend.value === 'number' ?
                `${trend.value > 0 ? '+' : ''}${trend.value.toFixed(1)}%` :
                trend.value
              }
            </span>
          </div>
        )}
      </div>

      {/* Subtitle */}
      {subtitle && (
        <p className="text-xs text-professional-500 mt-1 truncate">
          {subtitle}
        </p>
      )}

      {/* Trend period */}
      {trend?.period && (
        <p className="text-xs text-professional-400 mt-2">
          vs {trend.period}
        </p>
      )}
    </motion.div>
  );
};

// Educational mode KPI card - visual and explanatory
const EducationalKPICard: React.FC<KPICardProps & { data?: any }> = ({
  title,
  value,
  subtitle,
  trend,
  icon: Icon,
  onClick,
  className = '',
}) => {
  const getTrendIcon = () => {
    if (!trend) return null;

    const iconClass = "w-6 h-6";
    switch (trend.direction) {
      case 'up':
        return <ArrowUpIcon className={`${iconClass} text-green-600`} />;
      case 'down':
        return <ArrowDownIcon className={`${iconClass} text-red-600`} />;
      default:
        return <MinusIcon className={`${iconClass} text-gray-500`} />;
    }
  };

  const getTrendDescription = () => {
    if (!trend) return '';

    const direction = trend.direction === 'up' ? 'aumentó' :
                     trend.direction === 'down' ? 'disminuyó' : 'se mantuvo';

    return `Este indicador ${direction} ${Math.abs(trend.value)}% comparado con ${trend.period}`;
  };

  return (
    <motion.div
      className={`metric-card cursor-pointer ${className}`}
      onClick={onClick}
      whileHover={{
        scale: 1.03,
        y: -2
      }}
      whileTap={{ scale: 0.97 }}
      transition={{ duration: 0.3, ease: "easeOut" }}
    >
      {/* Header with icon */}
      <div className="flex items-center space-x-3 mb-4">
        {Icon && (
          <div className="flex-shrink-0 p-3 bg-educational-100 rounded-xl">
            <Icon className="w-6 h-6 text-educational-600" />
          </div>
        )}
        <div className="flex-1">
          <h3 className="text-lg font-semibold text-educational-800">
            {title}
          </h3>
          {subtitle && (
            <p className="text-sm text-educational-600 mt-1">
              {subtitle}
            </p>
          )}
        </div>
      </div>

      {/* Main value with emphasis */}
      <div className="text-center py-4">
        <span className="metric-value text-5xl font-extrabold bg-gradient-to-r from-educational-600 to-primary-blue bg-clip-text text-transparent">
          {typeof value === 'number' ? value.toLocaleString() : value}
        </span>
      </div>

      {/* Trend visualization */}
      {trend && (
        <div className="mt-4 p-3 bg-gray-50 rounded-lg">
          <div className="flex items-center justify-center space-x-2">
            {getTrendIcon()}
            <span className="text-lg font-semibold">
              {trend.direction === 'up' ? '↗️' : trend.direction === 'down' ? '↘️' : '➡️'}
              {typeof trend.value === 'number' ?
                ` ${trend.value > 0 ? '+' : ''}${trend.value.toFixed(1)}%` :
                ` ${trend.value}`
              }
            </span>
          </div>

          <p className="text-sm text-gray-600 text-center mt-2">
            {getTrendDescription()}
          </p>
        </div>
      )}

      {/* Educational note */}
      <div className="mt-4 text-xs text-educational-500 text-center">
        💡 Haz clic para ver más detalles
      </div>
    </motion.div>
  );
};

// Main adaptive KPI card component
export const AdaptiveKPICard: React.FC<KPICardProps> = (props) => {
  return (
    <AdaptiveWrapper
      professionalVariant={ProfessionalKPICard}
      educationalVariant={EducationalKPICard}
      {...props}
    />
  );
};

// Pre-configured KPI cards for common metrics
export const ArticleCountCard: React.FC<{ count: number; trend?: KPICardProps['trend'] }> = ({
  count,
  trend
}) => (
  <AdaptiveKPICard
    title="Total de Artículos"
    value={count}
    subtitle="Artículos analizados en la base de datos"
    trend={trend}
    icon={({ className }) => (
      <svg className={className} fill="none" viewBox="0 0 24 24" stroke="currentColor">
        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2}
              d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
      </svg>
    )}
  />
);

export const LanguageDistributionCard: React.FC<{
  englishCount: number;
  spanishCount: number;
}> = ({
  englishCount,
  spanishCount
}) => {
  const total = englishCount + spanishCount;
  const englishPercentage = total > 0 ? (englishCount / total * 100).toFixed(1) : 0;
  const spanishPercentage = total > 0 ? (spanishCount / total * 100).toFixed(1) : 0;

  return (
    <AdaptiveKPICard
      title="Distribución por Idioma"
      value={`${englishPercentage}% EN | ${spanishPercentage}% ES`}
      subtitle={`${englishCount} artículos en inglés, ${spanishCount} en español`}
      icon={({ className }) => (
        <svg className={className} fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2}
                d="M3 5h12M9 3v2m1.048 9.5A18.022 18.022 0 016.412 9m6.088 9h7M11 21l5-10 5 10M12.751 5C11.783 10.77 8.07 15.61 3 18.129" />
        </svg>
      )}
    />
  );
};

export const TopCountryCard: React.FC<{
  country: string;
  count: number;
  percentage: number;
}> = ({
  country,
  count,
  percentage
}) => (
  <AdaptiveKPICard
    title="País Principal"
    value={country}
    subtitle={`${count} artículos (${percentage.toFixed(1)}%)`}
    icon={({ className }) => (
      <svg className={className} fill="none" viewBox="0 0 24 24" stroke="currentColor">
        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2}
              d="M3.055 11H5a2 2 0 012 2v1a2 2 0 002 2 2 2 0 012 2v2.945M8 3.935V5.5A2.5 2.5 0 0010.5 8h.5a2 2 0 012 2 2 2 0 104 0 2 2 0 012-2h1.064M15 20.488V18a2 2 0 012-2h3.064M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
      </svg>
    )}
  />
);

export const TopSourceCard: React.FC<{
  source: string;
  count: number;
  reliabilityScore?: number;
}> = ({
  source,
  count,
  reliabilityScore
}) => (
  <AdaptiveKPICard
    title="Fuente Principal"
    value={source}
    subtitle={`${count} artículos${reliabilityScore ? ` | Confiabilidad: ${reliabilityScore.toFixed(1)}/5` : ''}`}
    icon={({ className }) => (
      <svg className={className} fill="none" viewBox="0 0 24 24" stroke="currentColor">
        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2}
              d="M19 20H5a2 2 0 01-2-2V6a2 2 0 012-2h10a2 2 0 012 2v1m2 13a2 2 0 01-2-2V7m2 13a2 2 0 002-2V9a2 2 0 00-2-2h-2m-4-3H9M7 16h6M7 8h6v4H7V8z" />
      </svg>
    )}
  />
);
