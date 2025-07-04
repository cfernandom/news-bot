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

  const hasRealData = data && data.length > 0;

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

  const chartData = data;

  const renderBarChart = () => (
    <ResponsiveContainer width="100%" height={300}>
      <BarChart data={chartData}>
        <CartesianGrid strokeDasharray="3 3" stroke="var(--legacy-border)" />
        <XAxis
          dataKey={
            chartData[0] && 'day' in chartData[0] ? 'day' :
            chartData[0] && 'week' in chartData[0] ? 'week' : 'date'
          }
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
            <strong>Tendencia:</strong> Análisis basado en datos reales de evolución temporal del sentimiento.
          </p>
        ) : (
          <p>
            <strong>Patrón:</strong> Análisis basado en datos reales de distribución temporal de artículos.
          </p>
        )}
      </div>
    </div>
  );
};

export default LegacyTrendChart;
