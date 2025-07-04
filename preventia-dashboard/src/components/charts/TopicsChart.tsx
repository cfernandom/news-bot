// TopicsChart.tsx - Medical Topics Distribution Visualization
// High-impact component showing 10 medical categories with article distribution

import React, { useState } from 'react';
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
  PieChart,
  Pie,
  Cell,
} from 'recharts';
import { useDualMode } from '../../contexts/DualModeContext';
import { TopicData } from '../../types/medical';

interface TopicsChartProps {
  data: TopicData[];
  loading?: boolean;
  className?: string;
}

// Medical topic color palette - specialized for medical categories
const MEDICAL_TOPIC_COLORS = {
  treatment: '#10b981',    // Green - treatment success
  research: '#3b82f6',     // Blue - scientific research
  surgery: '#8b5cf6',      // Purple - surgical procedures
  general: '#6b7280',      // Gray - general information
  diagnosis: '#f59e0b',    // Orange - diagnostic procedures
  genetics: '#ec4899',     // Pink - genetic factors
  lifestyle: '#84cc16',    // Lime - lifestyle factors
  screening: '#06b6d4',    // Cyan - early detection
  support: '#f97316',      // Orange-red - patient support
  policy: '#64748b',       // Slate - health policy
} as const;

// Medical topic translations and descriptions
const MEDICAL_TOPIC_INFO = {
  treatment: {
    es: 'Tratamiento',
    description: 'Terapias, medicamentos y procedimientos curativos',
    examples: 'Quimioterapia, radioterapia, terapias dirigidas'
  },
  research: {
    es: 'Investigación',
    description: 'Estudios científicos y avances en investigación médica',
    examples: 'Ensayos clínicos, estudios epidemiológicos, nuevos descubrimientos'
  },
  surgery: {
    es: 'Cirugía',
    description: 'Procedimientos quirúrgicos y técnicas operatorias',
    examples: 'Mastectomía, cirugía conservadora, reconstrucción mamaria'
  },
  general: {
    es: 'General',
    description: 'Información médica general sobre cáncer de mama',
    examples: 'Estadísticas, información básica, concienciación'
  },
  diagnosis: {
    es: 'Diagnóstico',
    description: 'Métodos y procedimientos de diagnóstico médico',
    examples: 'Mamografías, biopsias, marcadores tumorales'
  },
  genetics: {
    es: 'Genética',
    description: 'Factores genéticos y hereditarios',
    examples: 'BRCA1, BRCA2, consejería genética, pruebas hereditarias'
  },
  lifestyle: {
    es: 'Estilo de Vida',
    description: 'Factores de estilo de vida y prevención',
    examples: 'Dieta, ejercicio, factores de riesgo modificables'
  },
  screening: {
    es: 'Detección',
    description: 'Programas de detección temprana y cribado',
    examples: 'Mamografías de rutina, autoexploración, programas de cribado'
  },
  support: {
    es: 'Apoyo',
    description: 'Apoyo psicológico y social para pacientes',
    examples: 'Grupos de apoyo, counseling, cuidados paliativos'
  },
  policy: {
    es: 'Política',
    description: 'Políticas de salud pública y regulaciones',
    examples: 'Políticas de screening, acceso a tratamientos, regulaciones'
  }
} as const;

// Custom tooltip for medical topics context
interface TopicsTooltipProps {
  active?: boolean;
  payload?: Array<{ payload: TopicData; value: number; name: string }>;
  label?: string;
}

const MedicalTopicsTooltip = ({ active, payload }: TopicsTooltipProps) => {
  if (active && payload && payload.length) {
    const data = payload[0].payload;
    const topicKey = data.topic as keyof typeof MEDICAL_TOPIC_INFO;
    const topicInfo = MEDICAL_TOPIC_INFO[topicKey];

    return (
      <div className="bg-white border border-gray-200 rounded-lg shadow-lg p-4 max-w-sm">
        <h4 className="font-semibold text-gray-900 mb-2">
          📊 {topicInfo?.es || data.topic}
        </h4>
        <div className="space-y-2 text-sm">
          <p className="text-gray-700">
            <span className="font-medium">Artículos:</span> {data.total}
          </p>
          {topicInfo && (
            <>
              <p className="text-gray-600 text-xs">
                <strong>Descripción:</strong> {topicInfo.description}
              </p>
              <p className="text-gray-600 text-xs">
                <strong>Ejemplos:</strong> {topicInfo.examples}
              </p>
            </>
          )}
        </div>
      </div>
    );
  }
  return null;
};

// Educational explanation component for topics
const TopicsEducationalExplanation = ({ isVisible, onToggle }: { isVisible: boolean; onToggle: () => void }) => (
  <div className="mt-4">
    <button
      onClick={onToggle}
      className="text-blue-600 hover:text-blue-800 text-sm font-medium flex items-center gap-2"
    >
      <span>{isVisible ? '📚' : '🎓'}</span>
      {isVisible ? 'Ocultar guía médica' : '¿Cómo leer este gráfico?'}
    </button>

    {isVisible && (
      <div className="mt-3 p-4 bg-blue-50 rounded-lg border border-blue-200">
        <h4 className="font-semibold text-blue-900 mb-2">
          🩺 Categorías de Noticias Médicas sobre Cáncer de Mama
        </h4>
        <div className="text-sm text-blue-800 space-y-2">
          <p>
            <strong>¿Qué muestra?</strong> Este gráfico categoriza las noticias médicas según su tema principal,
            ayudándonos a entender qué aspectos del cáncer de mama reciben más cobertura mediática.
          </p>
          <div className="mt-3 space-y-1">
            <div className="flex items-center gap-2">
              <div className="w-3 h-3 bg-green-500 rounded-full"></div>
              <span><strong>Tratamiento (39):</strong> La categoría más grande - noticias sobre terapias y medicamentos</span>
            </div>
            <div className="flex items-center gap-2">
              <div className="w-3 h-3 bg-blue-500 rounded-full"></div>
              <span><strong>Investigación (19):</strong> Estudios científicos y avances médicos</span>
            </div>
            <div className="flex items-center gap-2">
              <div className="w-3 h-3 bg-purple-500 rounded-full"></div>
              <span><strong>Cirugía (12):</strong> Procedimientos quirúrgicos y técnicas operatorias</span>
            </div>
          </div>
          <p className="text-xs text-blue-700 mt-2">
            <strong>Interpretación:</strong> El enfoque principal en "Tratamiento" sugiere que los medios
            priorizan informar sobre opciones terapéuticas disponibles para pacientes.
          </p>
        </div>
      </div>
    )}
  </div>
);

// Professional statistics panel for topics
const ProfessionalTopicsStats = ({ data }: { data: TopicData[] }) => {
  const total = data.reduce((sum, item) => sum + item.total, 0);
  const topCategory = data.reduce((prev, current) =>
    prev.total > current.total ? prev : current
  );
  const diversity = data.length;

  return (
    <div className="mt-4 p-4 bg-gray-50 rounded-lg border">
      <h4 className="font-semibold text-gray-900 mb-3">📈 Análisis Estadístico de Categorías</h4>
      <div className="grid grid-cols-3 gap-4 text-sm">
        <div>
          <p className="text-gray-600">Total artículos categorizados</p>
          <p className="text-2xl font-bold text-gray-900">{total}</p>
        </div>
        <div>
          <p className="text-gray-600">Categoría predominante</p>
          <p className="text-lg font-semibold text-green-600">
            {MEDICAL_TOPIC_INFO[topCategory.topic as keyof typeof MEDICAL_TOPIC_INFO]?.es || topCategory.topic} ({topCategory.total})
          </p>
        </div>
        <div>
          <p className="text-gray-600">Diversidad temática</p>
          <p className="text-lg font-semibold text-blue-600">{diversity} categorías</p>
        </div>
        <div className="col-span-3">
          <p className="text-gray-600 text-xs">
            <strong>Interpretación clínica:</strong> La concentración en tratamiento ({topCategory.total}/{total} artículos)
            refleja el enfoque mediático en opciones terapéuticas actuales para pacientes con cáncer de mama.
          </p>
        </div>
      </div>
    </div>
  );
};

// Custom legend for medical topics
interface TopicsLegendProps {
  payload?: Array<{
    value: string;
    color: string;
    payload?: TopicData;
  }>;
}

const MedicalTopicsLegend = ({ payload }: TopicsLegendProps) => (
  <div className="flex flex-wrap justify-center gap-3 mt-4 text-xs">
    {payload?.map((entry, index: number) => {
      const topicKey = entry.payload?.topic as keyof typeof MEDICAL_TOPIC_INFO;
      const topicInfo = MEDICAL_TOPIC_INFO[topicKey];

      return (
        <div key={index} className="flex items-center gap-1">
          <div
            className="w-3 h-3 rounded-full"
            style={{ backgroundColor: entry.color }}
          />
          <span className="font-medium">
            {topicInfo?.es || entry.payload?.topic}
          </span>
          <span className="text-gray-600">
            ({entry.payload?.total})
          </span>
        </div>
      );
    })}
  </div>
);

export const TopicsChart: React.FC<TopicsChartProps> = ({
  data,
  loading = false,
  className = ''
}) => {
  const { mode } = useDualMode();
  const [showExplanation, setShowExplanation] = useState(false);
  const [viewType, setViewType] = useState<'bar' | 'pie'>('bar');

  // Transform data to include colors
  const transformedData = data.map(item => ({
    ...item,
    fill: MEDICAL_TOPIC_COLORS[item.topic as keyof typeof MEDICAL_TOPIC_COLORS] || '#6b7280'
  }));

  // Loading state
  if (loading) {
    return (
      <div className={`animate-pulse ${className}`}>
        <div className="h-8 bg-gray-200 rounded w-3/4 mb-4"></div>
        <div className="h-64 bg-gray-200 rounded"></div>
      </div>
    );
  }

  // No data state
  if (!data || data.length === 0) {
    return (
      <div className={`text-center py-8 ${className}`}>
        <div className="text-gray-500 mb-2">📊</div>
        <p className="text-gray-600">No hay datos de categorías disponibles</p>
      </div>
    );
  }

  const isEducational = mode === 'educational';

  return (
    <div className={`bg-white rounded-lg border shadow-sm p-6 ${className}`}>
      {/* Header */}
      <div className="flex items-center justify-between mb-6">
        <div>
          <h3 className={`text-lg font-semibold ${isEducational ? 'text-gray-800' : 'text-gray-900'}`}>
            {isEducational ? '🩺 Categorías de Noticias Médicas' : '📊 Distribución por Categorías Médicas'}
          </h3>
          <p className="text-sm text-gray-600 mt-1">
            {isEducational
              ? 'Temas principales en noticias sobre cáncer de mama'
              : 'Análisis categórico de literatura médica por temas especializados'
            }
          </p>
        </div>

        {/* View toggle for professional mode */}
        {!isEducational && (
          <div className="flex bg-gray-100 rounded-lg p-1">
            <button
              onClick={() => setViewType('bar')}
              className={`px-3 py-1 text-sm rounded ${
                viewType === 'bar'
                  ? 'bg-white shadow text-gray-900'
                  : 'text-gray-600 hover:text-gray-900'
              }`}
            >
              Barras
            </button>
            <button
              onClick={() => setViewType('pie')}
              className={`px-3 py-1 text-sm rounded ${
                viewType === 'pie'
                  ? 'bg-white shadow text-gray-900'
                  : 'text-gray-600 hover:text-gray-900'
              }`}
            >
              Circular
            </button>
          </div>
        )}
      </div>

      {/* Chart visualization */}
      <div className="h-80 mb-4">
        <ResponsiveContainer width="100%" height="100%">
          {viewType === 'bar' ? (
            <BarChart
              data={transformedData}
              margin={{ top: 20, right: 30, left: 20, bottom: 5 }}
            >
              <CartesianGrid strokeDasharray="3 3" stroke="#f3f4f6" />
              <XAxis
                dataKey="topic"
                tick={{ fontSize: 11 }}
                angle={-45}
                textAnchor="end"
                height={80}
                tickFormatter={(value) =>
                  MEDICAL_TOPIC_INFO[value as keyof typeof MEDICAL_TOPIC_INFO]?.es || value
                }
              />
              <YAxis
                tick={{ fontSize: 12 }}
              />
              <Tooltip content={<MedicalTopicsTooltip />} />
              <Bar
                dataKey="total"
                radius={[4, 4, 0, 0]}
              >
                {transformedData.map((entry, index) => (
                  <Cell
                    key={`cell-${index}`}
                    fill={entry.fill}
                  />
                ))}
              </Bar>
            </BarChart>
          ) : (
            <PieChart>
              <Pie
                data={transformedData}
                cx="50%"
                cy="50%"
                innerRadius={isEducational ? 40 : 60}
                outerRadius={isEducational ? 100 : 120}
                paddingAngle={2}
                dataKey="total"
                nameKey="topic"
              >
                {transformedData.map((entry, index) => (
                  <Cell
                    key={`cell-${index}`}
                    fill={entry.fill}
                  />
                ))}
              </Pie>
              <Tooltip content={<MedicalTopicsTooltip />} />
              <Legend content={<MedicalTopicsLegend />} />
            </PieChart>
          )}
        </ResponsiveContainer>
      </div>

      {/* Mode-specific content */}
      {isEducational ? (
        <TopicsEducationalExplanation
          isVisible={showExplanation}
          onToggle={() => setShowExplanation(!showExplanation)}
        />
      ) : (
        <ProfessionalTopicsStats data={data} />
      )}

      {/* Key insights for both modes */}
      <div className={`mt-4 p-3 rounded-lg ${isEducational ? 'bg-blue-50 border-blue-200' : 'bg-gray-50 border-gray-200'} border`}>
        <h4 className={`font-medium mb-2 ${isEducational ? 'text-blue-900' : 'text-gray-900'}`}>
          🔍 {isEducational ? 'Hallazgos Principales' : 'Key Medical Insights'}
        </h4>
        <div className="text-sm space-y-1">
          {data.slice(0, 3).map((item, index) => {
            const topicInfo = MEDICAL_TOPIC_INFO[item.topic as keyof typeof MEDICAL_TOPIC_INFO];
            const percentage = ((item.total / data.reduce((sum, d) => sum + d.total, 0)) * 100).toFixed(1);

            return (
              <p key={index} className={isEducational ? 'text-blue-800' : 'text-gray-700'}>
                <strong>{percentage}%</strong> de las noticias se enfocan en{' '}
                <span className="font-medium">
                  {topicInfo?.es || item.topic}
                </span>
                {' '}({item.total} artículos)
              </p>
            );
          })}
        </div>
      </div>
    </div>
  );
};

export default TopicsChart;
