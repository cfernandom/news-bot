import React from 'react';
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
} from 'recharts';

interface TopicData {
  topic_category: string;
  count: number;
  spanish?: number;
  english?: number;
  español?: number;
  inglés?: number;
}

interface LegacyTopicsChartProps {
  data: TopicData[];
  loading?: boolean;
  title?: string;
  showLanguageBreakdown?: boolean;
  dateRange?: {
    startDate?: string;
    endDate?: string;
  };
  totalArticles?: number;
}

const LegacyTopicsChart: React.FC<LegacyTopicsChartProps> = ({
  data,
  loading,
  title = "Temas Más Relevantes",
  showLanguageBreakdown = false,
  dateRange,
  totalArticles
}) => {
  // Handle different empty states
  const hasRealData = data && Array.isArray(data) && data.length > 0;
  const hasValidData = hasRealData && data.some(item => item.count && item.count > 0);

  // Topic translation mapping
  const topicTranslations: { [key: string]: string } = {
    'treatment': 'Tratamiento',
    'research': 'Investigación',
    'diagnosis': 'Diagnóstico',
    'prevention': 'Prevención',
    'surgery': 'Cirugía',
    'screening': 'Detección',
    'support': 'Apoyo',
    'genetics': 'Genética',
    'lifestyle': 'Estilo de vida',
    'policy': 'Política',
    'general': 'General',
    'awareness': 'Concienciación',
    'nutrition': 'Nutrición',
    'rehabilitation': 'Rehabilitación'
  };

  // Safe topic name translation
  const getTopicName = (category: string) => {
    if (!category) return 'Sin categoría';
    const lowerCategory = category.toLowerCase();
    return topicTranslations[lowerCategory] ||
           category.charAt(0).toUpperCase() + category.slice(1);
  };

  // Transform and sort data for Recharts (top 8 topics) - only if we have valid data
  const chartData = hasValidData ? (showLanguageBreakdown
    ? data
        .filter(item => item.count && item.count > 0)
        .sort((a, b) => (b.count || 0) - (a.count || 0))
        .slice(0, 8)
        .map(item => ({
          name: getTopicName(item.topic_category),
          español: (item as any).spanish || (item as any).español || 0,
          inglés: (item as any).english || (item as any).inglés || 0,
          total: item.count || 0,
        }))
    : data
        .filter(item => item.count && item.count > 0)
        .sort((a, b) => (b.count || 0) - (a.count || 0))
        .slice(0, 8)
        .map(item => ({
          name: getTopicName(item.topic_category),
          value: item.count || 0,
        }))) : [];

  const CustomTooltip = ({ active, payload, label }: any) => {
    if (active && payload && payload.length) {
      return (
        <div
          className="legacy-chart-tooltip"
          style={{
            backgroundColor: 'var(--legacy-card-bg)',
            border: '1px solid var(--legacy-border)',
            borderRadius: '8px',
            padding: '12px',
            color: 'var(--text-primary)',
            fontSize: '14px',
            fontWeight: '500',
            boxShadow: '0 4px 12px rgba(0, 0, 0, 0.15)',
          }}
        >
          <p style={{ color: 'var(--text-primary)', fontWeight: 600, margin: '0 0 8px 0' }}>
            {label || 'Sin etiqueta'}
          </p>
          {showLanguageBreakdown ? (
            <>
              <p style={{ color: '#4A90E2', margin: '4px 0' }}>
                Español: {payload.find((p: any) => p.dataKey === 'español')?.value || 0}
              </p>
              <p style={{ color: '#10b981', margin: '4px 0' }}>
                Inglés: {payload.find((p: any) => p.dataKey === 'inglés')?.value || 0}
              </p>
              <p style={{ color: 'var(--text-secondary)', margin: '4px 0 0 0' }}>
                Total: {payload[0]?.payload?.total || 0}
              </p>
            </>
          ) : (
            <p style={{ color: 'var(--text-secondary)', margin: 0 }}>
              Artículos: {payload[0]?.value || 0}
            </p>
          )}
        </div>
      );
    }
    return null;
  };

  if (loading) {
    return (
      <div className="legacy-chart-container">
        <h3>{title}</h3>
        <div style={{ height: '400px', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
          <div className="legacy-loading-spinner">
            <i className="fas fa-spinner fa-spin" style={{ fontSize: '24px', color: 'var(--primary-blue)' }}></i>
            <p style={{ marginTop: '10px', color: 'var(--text-secondary)' }}>Cargando datos...</p>
          </div>
        </div>
      </div>
    );
  }

  if (!hasRealData) {
    return (
      <div className="legacy-chart-container">
        <h3>{title}</h3>
        <div style={{ height: '400px', display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center' }}>
          <i className="fas fa-tags" style={{ fontSize: '48px', color: '#6b7280', marginBottom: '20px' }}></i>
          <p style={{ color: 'var(--text-secondary)', textAlign: 'center' }}>
            No se pudieron obtener los datos de temas.<br />
            Verifique la conexión con la API.
          </p>
        </div>
      </div>
    );
  }

  if (!hasValidData) {
    return (
      <div className="legacy-chart-container">
        <h3>{title}</h3>
        <div style={{ height: '400px', display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center' }}>
          <i className="fas fa-exclamation-triangle" style={{ fontSize: '48px', color: '#f59e0b', marginBottom: '20px' }}></i>
          <p style={{ color: 'var(--text-secondary)', textAlign: 'center' }}>
            Los datos de temas están vacíos.<br />
            No hay categorías con artículos disponibles para mostrar.
          </p>
        </div>
      </div>
    );
  }

  if (chartData.length === 0) {
    return (
      <div className="legacy-chart-container">
        <h3>{title}</h3>
        <div style={{ height: '400px', display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center' }}>
          <i className="fas fa-ban" style={{ fontSize: '48px', color: '#6b7280', marginBottom: '20px' }}></i>
          <p style={{ color: 'var(--text-secondary)', textAlign: 'center' }}>
            No hay temas con datos suficientes para mostrar.<br />
            Intente ajustar los filtros o criterios de búsqueda.
          </p>
        </div>
      </div>
    );
  }

  // Calculate statistics
  const getTopicsStats = () => {
    if (showLanguageBreakdown) {
      const totalSpanish = chartData.reduce((sum, item) => {
        return sum + ((item as any).español || 0);
      }, 0);
      const totalEnglish = chartData.reduce((sum, item) => {
        return sum + ((item as any).inglés || 0);
      }, 0);
      const total = totalSpanish + totalEnglish;

      return {
        total,
        details: `${totalSpanish} en español, ${totalEnglish} en inglés`,
        categories: chartData.length
      };
    } else {
      const total = chartData.reduce((sum, item) => {
        return sum + ((item as any).value || 0);
      }, 0);

      return {
        total,
        details: `distribuidos en ${chartData.length} categoría${chartData.length > 1 ? 's' : ''}`,
        categories: chartData.length
      };
    }
  };

  const stats = getTopicsStats();

  // Enhanced title with temporal context
  const getEnhancedTitle = () => {
    if (dateRange && dateRange.startDate && dateRange.endDate) {
      const startDate = new Date(dateRange.startDate).toLocaleDateString('es-ES', {
        month: 'short',
        year: 'numeric'
      });
      const endDate = new Date(dateRange.endDate).toLocaleDateString('es-ES', {
        month: 'short',
        year: 'numeric'
      });

      return `${title} (${startDate} - ${endDate})`;
    }
    return title;
  };

  return (
    <div className="legacy-chart-container">
      <h3>{getEnhancedTitle()}</h3>
      <ResponsiveContainer width="100%" height={400}>
        <BarChart
          data={chartData}
          margin={{
            top: 20,
            right: 30,
            left: 20,
            bottom: 60,
          }}
        >
          <CartesianGrid strokeDasharray="3 3" stroke="var(--legacy-border)" />
          <XAxis
            dataKey="name"
            tick={{ fontSize: 12, fill: 'var(--text-primary)' }}
            angle={-45}
            textAnchor="end"
            height={80}
          />
          <YAxis
            tick={{ fontSize: 12, fill: 'var(--text-primary)' }}
          />
          <Tooltip content={<CustomTooltip />} />
          {showLanguageBreakdown ? (
            <>
              <Bar
                dataKey="español"
                fill="#4A90E2"
                name="Español"
                radius={[4, 4, 0, 0]}
              />
              <Bar
                dataKey="inglés"
                fill="#10b981"
                name="Inglés"
                radius={[4, 4, 0, 0]}
              />
            </>
          ) : (
            <Bar
              dataKey="value"
              fill="var(--primary-blue)"
              radius={[4, 4, 0, 0]}
              name="Artículos"
            />
          )}
        </BarChart>
      </ResponsiveContainer>

      {/* Chart Statistics */}
      <div className="legacy-chart-insights">
        <p>
          <strong>Análisis de temas:</strong> {stats.total} artículos {stats.details}
          {stats.categories < 8 && data.length > 8 && (
            <span style={{ color: 'var(--text-secondary)', fontStyle: 'italic' }}>
              {' '}(mostrando top {stats.categories} de {data.length} temas)
            </span>
          )}
        </p>

        {/* Temporal Context */}
        {(dateRange || totalArticles) && (
          <div style={{
            marginTop: '10px',
            padding: '10px',
            backgroundColor: 'rgba(74, 144, 226, 0.05)',
            borderRadius: '6px',
            fontSize: '14px'
          }}>
            {dateRange && dateRange.startDate && dateRange.endDate && (
              <p style={{ margin: '0 0 5px 0', color: 'var(--text-secondary)' }}>
                <strong>Período:</strong> {new Date(dateRange.startDate).toLocaleDateString('es-ES')} - {new Date(dateRange.endDate).toLocaleDateString('es-ES')}
              </p>
            )}
            {totalArticles && (
              <p style={{ margin: 0, color: 'var(--text-secondary)' }}>
                <strong>Total del dataset:</strong> {totalArticles} artículos
                {stats.total !== totalArticles && (
                  <span style={{ fontStyle: 'italic' }}>
                    {' '}({((stats.total / totalArticles) * 100).toFixed(1)}% categorizado)
                  </span>
                )}
              </p>
            )}
            {!dateRange && !totalArticles && (
              <p style={{ margin: 0, color: 'var(--text-secondary)', fontStyle: 'italic' }}>
                Datos acumulados históricos - Sin rango temporal específico
              </p>
            )}
          </div>
        )}
      </div>
    </div>
  );
};

export default LegacyTopicsChart;
