import React from 'react';
import {
  PieChart,
  Pie,
  Cell,
  ResponsiveContainer,
  Tooltip,
  Legend,
} from 'recharts';

interface SentimentData {
  sentiment_label: string;
  count: number;
}

interface LegacySentimentChartProps {
  data: SentimentData[];
  loading?: boolean;
  title?: string;
  showPieChart?: boolean;
  type?: 'sentiment' | 'language';
}

const LegacySentimentChart: React.FC<LegacySentimentChartProps> = ({
  data,
  loading,
  title = "Sentiment Analysis",
  showPieChart = false,
  type = 'sentiment'
}) => {
  // Handle different empty states
  const hasRealData = data && Array.isArray(data) && data.length > 0;
  const hasValidData = hasRealData && data.some(item => item.count && item.count > 0);

  // Transform data based on type - only if we have valid data
  const chartData = hasValidData ? (type === 'language'
    ? data.map(item => ({
        name: item.sentiment_label === 'english' ? 'Inglés' :
              item.sentiment_label === 'spanish' ? 'Español' : 'Otros',
        value: item.count || 0,
        color: item.sentiment_label === 'english' ? '#4A90E2' :
               item.sentiment_label === 'spanish' ? '#F8BBD9' : '#9CA3AF'
      }))
    : data.map(item => ({
        name: item.sentiment_label === 'positive' ? 'Positivo' :
              item.sentiment_label === 'negative' ? 'Negativo' : 'Neutro',
        value: item.count || 0,
        color: item.sentiment_label === 'positive' ? '#10b981' :
               item.sentiment_label === 'negative' ? '#ef4444' : '#6b7280'
      }))) : [];

  // Filter out items with 0 value for better visualization
  const filteredChartData = chartData.filter(item => item.value > 0);

  const COLORS = type === 'language'
    ? ['#4A90E2', '#F8BBD9', '#9CA3AF']
    : ['#10b981', '#ef4444', '#6b7280'];

  const CustomTooltip = ({ active, payload }: any) => {
    if (active && payload && payload.length) {
      const data = payload[0];
      const total = filteredChartData.reduce((sum, item) => sum + item.value, 0);
      const percentage = total > 0 ? ((data.value / total) * 100).toFixed(1) : '0';

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
          <p style={{ color: 'var(--text-primary)', fontWeight: 600, margin: '0 0 4px 0' }}>
            {data.name || 'Sin etiqueta'}
          </p>
          <p style={{ color: 'var(--text-secondary)', margin: 0 }}>
            Artículos: {data.value || 0} ({percentage}%)
          </p>
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
          <i className="fas fa-chart-pie" style={{ fontSize: '48px', color: '#6b7280', marginBottom: '20px' }}></i>
          <p style={{ color: 'var(--text-secondary)', textAlign: 'center' }}>
            No se pudieron obtener los datos de {type === 'language' ? 'idiomas' : 'sentimientos'}.<br />
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
            Los datos de {type === 'language' ? 'idiomas' : 'sentimientos'} están vacíos.<br />
            No hay información disponible para mostrar.
          </p>
        </div>
      </div>
    );
  }

  if (filteredChartData.length === 0) {
    return (
      <div className="legacy-chart-container">
        <h3>{title}</h3>
        <div style={{ height: '400px', display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center' }}>
          <i className="fas fa-ban" style={{ fontSize: '48px', color: '#6b7280', marginBottom: '20px' }}></i>
          <p style={{ color: 'var(--text-secondary)', textAlign: 'center' }}>
            Todos los valores de {type === 'language' ? 'idiomas' : 'sentimientos'} son cero.<br />
            No hay datos suficientes para generar el gráfico.
          </p>
        </div>
      </div>
    );
  }

  return (
    <div className="legacy-chart-container">
      <h3>{title}</h3>
      <ResponsiveContainer width="100%" height={400}>
        <PieChart>
          <Pie
            data={filteredChartData}
            cx="50%"
            cy="50%"
            labelLine={false}
            label={({ name, percent }) => {
              const safeName = name || 'Sin etiqueta';
              const safePercent = percent ? (percent * 100).toFixed(0) : '0';
              return `${safeName} ${safePercent}%`;
            }}
            outerRadius={80}
            fill="#8884d8"
            dataKey="value"
          >
            {filteredChartData.map((entry, index) => (
              <Cell
                key={`cell-${index}`}
                fill={entry.color || COLORS[index % COLORS.length]}
              />
            ))}
          </Pie>
          <Tooltip content={<CustomTooltip />} />
          <Legend
            formatter={(value) => value || 'Sin etiqueta'}
            wrapperStyle={{ color: 'var(--text-primary)' }}
          />
        </PieChart>
      </ResponsiveContainer>

      {/* Chart Statistics */}
      <div className="legacy-chart-insights">
        <p>
          <strong>Total de artículos:</strong> {filteredChartData.reduce((sum, item) => sum + item.value, 0)}
          {type === 'language'
            ? ` distribuidos en ${filteredChartData.length} idioma${filteredChartData.length > 1 ? 's' : ''}`
            : ` con análisis de sentimiento`
          }
        </p>
      </div>
    </div>
  );
};

export default LegacySentimentChart;
