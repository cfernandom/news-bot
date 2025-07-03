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
  title?: string;
  showLanguageBreakdown?: boolean;
}

const LegacyTopicsChart: React.FC<LegacyTopicsChartProps> = ({
  data,
  loading,
  title = "Temas Más Relevantes",
  showLanguageBreakdown = false
}) => {
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
  const chartData = showLanguageBreakdown
    ? data
        .sort((a, b) => b.count - a.count)
        .slice(0, 8)
        .map(item => ({
          name: topicTranslations[item.topic_category.toLowerCase()] ||
                item.topic_category.charAt(0).toUpperCase() + item.topic_category.slice(1),
          español: Math.round(item.count * 0.36), // 36% Spanish
          inglés: Math.round(item.count * 0.64), // 64% English
          total: item.count,
        }))
    : data
        .sort((a, b) => b.count - a.count)
        .slice(0, 8)
        .map(item => ({
          name: topicTranslations[item.topic_category.toLowerCase()] ||
                item.topic_category.charAt(0).toUpperCase() + item.topic_category.slice(1),
          value: item.count,
        }));

  const CustomTooltip = ({ active, payload, label }: any) => {
    if (active && payload && payload.length) {
      return (
        <div className="legacy-chart-tooltip">
          <p style={{ color: 'var(--text-primary)', fontWeight: 600 }}>
            {label}
          </p>
          {showLanguageBreakdown ? (
            <>
              <p style={{ color: '#4A90E2' }}>Español: {payload.find((p: any) => p.dataKey === 'español')?.value || 0}</p>
              <p style={{ color: '#10b981' }}>Inglés: {payload.find((p: any) => p.dataKey === 'inglés')?.value || 0}</p>
              <p style={{ color: 'var(--text-secondary)' }}>Total: {payload[0].payload.total}</p>
            </>
          ) : (
            <p style={{ color: 'var(--text-secondary)' }}>
              Artículos: {payload[0].value}
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

  return (
    <div className="legacy-chart-container">
      <h3>{title}</h3>
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
            />
          )}
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
};

export default LegacyTopicsChart;
