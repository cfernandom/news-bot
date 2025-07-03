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
  date: string;
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
  showSentimentLines?: boolean;
  type?: 'bar' | 'line';
}

const LegacyTrendChart: React.FC<LegacyTrendChartProps> = ({
  data,
  loading = false,
  title = 'Gráfico de Tendencias',
  showSentimentLines = false,
  type = 'bar',
}) => {
  if (loading) {
    return (
      <div className="legacy-chart-container">
        <h3>{title}</h3>
        <div className="legacy-loading">
          <i className="fas fa-spinner fa-spin"></i>
          <p>Cargando datos...</p>
        </div>
      </div>
    );
  }

  // Default data for demonstration
  const defaultBarData = [
    { day: 'Lunes', count: 18 },
    { day: 'Martes', count: 24 },
    { day: 'Miércoles', count: 21 },
    { day: 'Jueves', count: 16 },
    { day: 'Viernes', count: 14 },
    { day: 'Sábado', count: 8 },
    { day: 'Domingo', count: 5 },
  ];

  const defaultSentimentData = [
    { week: 'Sem 20', positive: 25, neutral: 60, negative: 15 },
    { week: 'Sem 21', positive: 30, neutral: 55, negative: 15 },
    { week: 'Sem 22', positive: 28, neutral: 57, negative: 15 },
    { week: 'Sem 23', positive: 32, neutral: 53, negative: 15 },
    { week: 'Sem 24', positive: 27, neutral: 58, negative: 15 },
  ];

  const chartData = data && data.length > 0 ? data : (showSentimentLines ? defaultSentimentData : defaultBarData);

  const renderBarChart = () => (
    <ResponsiveContainer width="100%" height={300}>
      <BarChart data={chartData}>
        <CartesianGrid strokeDasharray="3 3" stroke="var(--legacy-border)" />
        <XAxis
          dataKey={chartData[0]?.day ? 'day' : 'date'}
          stroke="var(--text-primary)"
          fontSize={12}
        />
        <YAxis stroke="var(--text-primary)" fontSize={12} />
        <Tooltip
          contentStyle={{
            backgroundColor: 'var(--legacy-card-bg)',
            border: '1px solid var(--legacy-border)',
            borderRadius: '8px',
          }}
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

  const renderSentimentChart = () => (
    <ResponsiveContainer width="100%" height={300}>
      <LineChart data={chartData}>
        <CartesianGrid strokeDasharray="3 3" stroke="var(--legacy-border)" />
        <XAxis
          dataKey="week"
          stroke="var(--text-primary)"
          fontSize={12}
        />
        <YAxis stroke="var(--text-primary)" fontSize={12} />
        <Tooltip
          contentStyle={{
            backgroundColor: 'var(--legacy-card-bg)',
            border: '1px solid var(--legacy-border)',
            borderRadius: '8px',
          }}
        />
        <Legend />
        <Line
          type="monotone"
          dataKey="positive"
          stroke="#28a745"
          strokeWidth={3}
          name="Positivo"
          dot={{ fill: '#28a745', strokeWidth: 2, r: 4 }}
        />
        <Line
          type="monotone"
          dataKey="neutral"
          stroke="#6c757d"
          strokeWidth={3}
          name="Neutro"
          dot={{ fill: '#6c757d', strokeWidth: 2, r: 4 }}
        />
        <Line
          type="monotone"
          dataKey="negative"
          stroke="#dc3545"
          strokeWidth={3}
          name="Negativo"
          dot={{ fill: '#dc3545', strokeWidth: 2, r: 4 }}
        />
      </LineChart>
    </ResponsiveContainer>
  );

  return (
    <div className="legacy-chart-container">
      <h3>{title}</h3>
      {showSentimentLines ? renderSentimentChart() : renderBarChart()}

      {/* Chart insights */}
      <div className="legacy-chart-insights">
        {showSentimentLines ? (
          <p>
            <strong>Tendencia:</strong> El sentimiento neutral se mantiene estable (~55%),
            mientras que el contenido positivo muestra ligeras variaciones semanales.
          </p>
        ) : (
          <p>
            <strong>Patrón:</strong> Mayor actividad informativa durante días laborales,
            con picos los martes y miércoles.
          </p>
        )}
      </div>
    </div>
  );
};

export default LegacyTrendChart;
