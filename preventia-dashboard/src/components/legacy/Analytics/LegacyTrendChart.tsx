import React from 'react';
import {
  LineChart,
  Line,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from 'recharts';

interface TrendDataPoint {
  date?: string;
  day?: string;
  week?: string;
  positive?: number;
  negative?: number;
  neutral?: number;
  value?: number;
  count?: number;
}

interface LegacyTrendChartProps {
  data: TrendDataPoint[];
  loading?: boolean;
  title?: string;
  subtitle?: string;
  showSentimentLines?: boolean;
  type?: 'bar' | 'line';
}

const LegacyTrendChart: React.FC<LegacyTrendChartProps> = ({
  data,
  loading = false,
  title = 'Gráfico de Tendencias',
  subtitle,
  showSentimentLines = false
}) => {
  // Handle different empty states
  const hasRealData = data && Array.isArray(data) && data.length > 0;
  const hasValidData = hasRealData && data.some(item => {
    if (showSentimentLines) {
      return (item.positive && item.positive > 0) ||
             (item.negative && item.negative > 0) ||
             (item.neutral && item.neutral > 0);
    } else {
      return (item.count && item.count > 0) || (item.value && item.value > 0);
    }
  });

  if (loading) {
    return (
      <div className="legacy-chart-container">
        <h3>{title}</h3>
        <div style={{ height: '300px', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
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
        <div style={{ height: '300px', display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center' }}>
          <i className="fas fa-chart-line" style={{ fontSize: '48px', color: '#6b7280', marginBottom: '20px' }}></i>
          <p style={{ color: 'var(--text-secondary)', textAlign: 'center' }}>
            No se pudieron obtener los datos de tendencias.<br />
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
        <div style={{ height: '300px', display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center' }}>
          <i className="fas fa-exclamation-triangle" style={{ fontSize: '48px', color: '#f59e0b', marginBottom: '20px' }}></i>
          <p style={{ color: 'var(--text-secondary)', textAlign: 'center' }}>
            Los datos de tendencias están vacíos.<br />
            No hay {showSentimentLines ? 'información de sentimientos' : 'valores'} disponibles para mostrar.
          </p>
        </div>
      </div>
    );
  }

  // Process data safely
  const chartData = data.map(item => ({
    ...item,
    // Ensure safe values for bar chart
    count: item.count || item.value || 0,
    value: item.value || item.count || 0,
    // Ensure safe values for sentiment chart
    positive: item.positive || 0,
    negative: item.negative || 0,
    neutral: item.neutral || 0,
    // Ensure date labels are available
    date: item.date || item.day || item.week || 'Sin fecha',
    day: item.day || item.date || item.week || 'Sin fecha',
    week: item.week || item.date || item.day || 'Sin fecha'
  }));

  const renderBarChart = () => {
    // Determine the best dataKey for X-axis
    const getXAxisKey = () => {
      if (chartData.length === 0) return 'date';
      const firstItem = chartData[0];
      if (firstItem.day && firstItem.day !== 'Sin fecha') return 'day';
      if (firstItem.week && firstItem.week !== 'Sin fecha') return 'week';
      return 'date';
    };

    return (
      <ResponsiveContainer width="100%" height={300}>
        <BarChart data={chartData}>
          <CartesianGrid strokeDasharray="3 3" stroke="var(--legacy-border)" />
          <XAxis
            dataKey={getXAxisKey()}
            stroke="var(--text-primary)"
            fontSize={12}
            tick={{ fill: 'var(--text-primary)' }}
          />
          <YAxis
            stroke="var(--text-primary)"
            fontSize={12}
            tick={{ fill: 'var(--text-primary)' }}
          />
          <Tooltip
            contentStyle={{
              backgroundColor: 'var(--legacy-card-bg)',
              border: '1px solid var(--legacy-border)',
              borderRadius: '8px',
              color: 'var(--text-primary)',
              fontSize: '14px',
              fontWeight: '500',
              boxShadow: '0 4px 12px rgba(0, 0, 0, 0.15)',
            }}
            formatter={(value, name) => [value || 0, name || 'Valor']}
            labelFormatter={(label) => label || 'Sin etiqueta'}
          />
          <Bar
            dataKey="count"
            fill="var(--primary-blue)"
            radius={[4, 4, 0, 0]}
            name="Noticias"
          />
        </BarChart>
      </ResponsiveContainer>
    );
  };

  const renderSentimentChart = () => {
    // Determine the best dataKey for X-axis in sentiment chart
    const getXAxisKey = () => {
      if (chartData.length === 0) return 'week';
      const firstItem = chartData[0];
      if (firstItem.week && firstItem.week !== 'Sin fecha') return 'week';
      if (firstItem.day && firstItem.day !== 'Sin fecha') return 'day';
      return 'date';
    };

    return (
      <ResponsiveContainer width="100%" height={300}>
        <LineChart data={chartData}>
          <CartesianGrid strokeDasharray="3 3" stroke="var(--legacy-border)" />
          <XAxis
            dataKey={getXAxisKey()}
            stroke="var(--text-primary)"
            fontSize={12}
            tick={{ fill: 'var(--text-primary)' }}
          />
          <YAxis
            stroke="var(--text-primary)"
            fontSize={12}
            tick={{ fill: 'var(--text-primary)' }}
          />
          <Tooltip
            contentStyle={{
              backgroundColor: 'var(--legacy-card-bg)',
              border: '1px solid var(--legacy-border)',
              borderRadius: '8px',
              color: 'var(--text-primary)',
              fontSize: '14px',
              fontWeight: '500',
              boxShadow: '0 4px 12px rgba(0, 0, 0, 0.15)',
            }}
            formatter={(value, name) => [value || 0, name || 'Valor']}
            labelFormatter={(label) => label || 'Sin etiqueta'}
          />
          <Legend
            wrapperStyle={{ color: 'var(--text-primary)' }}
          />
          <Line
            type="monotone"
            dataKey="positive"
            stroke="#28a745"
            strokeWidth={3}
            name="Positivo"
            dot={{ fill: '#28a745', strokeWidth: 2, r: 4 }}
            connectNulls={false}
          />
          <Line
            type="monotone"
            dataKey="neutral"
            stroke="#6c757d"
            strokeWidth={3}
            name="Neutro"
            dot={{ fill: '#6c757d', strokeWidth: 2, r: 4 }}
            connectNulls={false}
          />
          <Line
            type="monotone"
            dataKey="negative"
            stroke="#dc3545"
            strokeWidth={3}
            name="Negativo"
            dot={{ fill: '#dc3545', strokeWidth: 2, r: 4 }}
            connectNulls={false}
          />
        </LineChart>
      </ResponsiveContainer>
    );
  };

  // Calculate statistics
  const getChartStats = () => {
    if (showSentimentLines) {
      const totalPositive = chartData.reduce((sum, item) => sum + (item.positive || 0), 0);
      const totalNegative = chartData.reduce((sum, item) => sum + (item.negative || 0), 0);
      const totalNeutral = chartData.reduce((sum, item) => sum + (item.neutral || 0), 0);
      const total = totalPositive + totalNegative + totalNeutral;

      return {
        type: 'sentiment',
        total,
        details: `${totalPositive} positivos, ${totalNegative} negativos, ${totalNeutral} neutros`
      };
    } else {
      const total = chartData.reduce((sum, item) => sum + (item.count || 0), 0);
      const periods = chartData.length;

      return {
        type: 'volume',
        total,
        details: `distribuidos en ${periods} período${periods > 1 ? 's' : ''}`
      };
    }
  };

  const stats = getChartStats();

  return (
    <div className="legacy-chart-container">
      <h3>{title}</h3>
      {subtitle && <p className="legacy-chart-subtitle">{subtitle}</p>}

      {showSentimentLines ? renderSentimentChart() : renderBarChart()}

      {/* Chart insights */}
      <div className="legacy-chart-insights">
        {showSentimentLines ? (
          <p>
            <strong>Análisis temporal:</strong> {stats.total} artículos con sentimiento analizado ({stats.details})
          </p>
        ) : (
          <p>
            <strong>Volumen temporal:</strong> {stats.total} artículos {stats.details}
          </p>
        )}
      </div>
    </div>
  );
};

export default LegacyTrendChart;
