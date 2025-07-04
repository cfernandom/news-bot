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
  // Transform data based on type
  const chartData = type === 'language'
    ? data.map(item => ({
        name: item.sentiment_label === 'english' ? 'Inglés' :
              item.sentiment_label === 'spanish' ? 'Español' : 'Otros',
        value: item.count,
        color: item.sentiment_label === 'english' ? '#4A90E2' :
               item.sentiment_label === 'spanish' ? '#F8BBD9' : '#9CA3AF'
      }))
    : data.map(item => ({
        name: item.sentiment_label === 'positive' ? 'Positivo' :
              item.sentiment_label === 'negative' ? 'Negativo' : 'Neutro',
        value: item.count,
        color: item.sentiment_label === 'positive' ? '#10b981' :
               item.sentiment_label === 'negative' ? '#ef4444' : '#6b7280'
      }));

  // Filter out items with 0 value for better visualization
  const filteredChartData = chartData.filter(item => item.value > 0);

  const COLORS = type === 'language'
    ? ['#4A90E2', '#F8BBD9', '#9CA3AF']
    : ['#10b981', '#ef4444', '#6b7280'];

  const CustomTooltip = ({ active, payload }: any) => {
    if (active && payload && payload.length) {
      const data = payload[0];
      return (
        <div className="legacy-chart-tooltip">
          <p style={{ color: 'var(--text-primary)', fontWeight: 600 }}>
            {data.name}
          </p>
          <p style={{ color: 'var(--text-secondary)' }}>
            {type === 'language' ? 'Porcentaje' : 'Artículos'}: {data.value}{type === 'language' ? '%' : ''}
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
            label={({ name, percent }) => `${name} ${percent ? (percent * 100).toFixed(0) : 0}%`}
            outerRadius={80}
            fill="#8884d8"
            dataKey="value"
          >
            {filteredChartData.map((entry, index) => (
              <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
            ))}
          </Pie>
          <Tooltip content={<CustomTooltip />} />
          <Legend />
        </PieChart>
      </ResponsiveContainer>
    </div>
  );
};

export default LegacySentimentChart;
