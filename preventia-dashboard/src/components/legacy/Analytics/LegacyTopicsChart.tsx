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
}

interface LegacyTopicsChartProps {
  data: TopicData[];
  loading?: boolean;
}

const LegacyTopicsChart: React.FC<LegacyTopicsChartProps> = ({ data, loading }) => {
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

  // Transform and sort data for Recharts (top 8 topics)
  const chartData = data
    .sort((a, b) => b.count - a.count)
    .slice(0, 8)
    .map(item => ({
      name: topicTranslations[item.topic_category.toLowerCase()] ||
            item.topic_category.charAt(0).toUpperCase() + item.topic_category.slice(1),
      value: item.count,
    }));

  const CustomTooltip = ({ active, payload, label }: any) => {
    if (active && payload && payload.length) {
      const data = payload[0];
      return (
        <div className="legacy-chart-tooltip">
          <p style={{ color: 'var(--text-primary)', fontWeight: 600 }}>
            {label}
          </p>
          <p style={{ color: 'var(--text-secondary)' }}>
            Artículos: {data.value}
          </p>
        </div>
      );
    }
    return null;
  };

  if (loading) {
    return (
      <div className="legacy-chart-container">
        <h3>Temas Más Relevantes</h3>
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
      <h3>Temas Más Relevantes</h3>
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
          <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" />
          <XAxis
            dataKey="name"
            tick={{ fontSize: 12, fill: 'var(--text-secondary)' }}
            angle={-45}
            textAnchor="end"
            height={80}
          />
          <YAxis
            tick={{ fontSize: 12, fill: 'var(--text-secondary)' }}
          />
          <Tooltip content={<CustomTooltip />} />
          <Bar
            dataKey="value"
            fill="var(--primary-blue)"
            radius={[4, 4, 0, 0]}
          />
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
};

export default LegacyTopicsChart;
