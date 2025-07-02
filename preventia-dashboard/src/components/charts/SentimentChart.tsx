// SentimentChart.tsx - Medical Sentiment Visualization for PreventIA Dashboard
// High-impact component for stakeholder presentations

import React, { useState } from 'react';
import {
  PieChart,
  Pie,
  Cell,
  ResponsiveContainer,
  Tooltip,
  Legend,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
} from 'recharts';
import { useDualMode } from '../../contexts/DualModeContext';
import { SentimentData } from '../../types/medical';

interface SentimentChartProps {
  data: SentimentData[];
  loading?: boolean;
  className?: string;
}

// Medical color palette for sentiment visualization
const MEDICAL_COLORS = {
  positive: '#10b981', // Medical green - healing, positive outcomes
  negative: '#ef4444', // Medical red - alerts, risks
  neutral: '#6b7280',  // Medical gray - neutral clinical data
} as const;

// Custom tooltip for medical context
interface TooltipProps {
  active?: boolean;
  payload?: Array<{ payload: SentimentData }>;
}

const MedicalTooltip = ({ active, payload }: TooltipProps) => {
  if (active && payload && payload.length) {
    const data = payload[0].payload;
    return (
      <div className="bg-white border border-gray-200 rounded-lg shadow-lg p-4 max-w-sm">
        <h4 className="font-semibold text-gray-900 mb-2">
          Sentimiento: {data.sentiment === 'positive' ? 'Positivo' :
                      data.sentiment === 'negative' ? 'Negativo' : 'Neutro'}
        </h4>
        <div className="space-y-1 text-sm">
          <p className="text-gray-700">
            <span className="font-medium">Artículos:</span> {data.value}
          </p>
          <p className="text-gray-700">
            <span className="font-medium">Porcentaje:</span> {data.percentage}%
          </p>
          <p className="text-gray-600 text-xs mt-2">
            {data.sentiment === 'positive' && "Noticias sobre avances médicos, tratamientos exitosos"}
            {data.sentiment === 'negative' && "Noticias sobre riesgos, problemas, estadísticas preocupantes"}
            {data.sentiment === 'neutral' && "Información médica objetiva, datos estadísticos"}
          </p>
        </div>
      </div>
    );
  }
  return null;
};

// Educational explanation component
const EducationalExplanation = ({ isVisible, onToggle }: { isVisible: boolean; onToggle: () => void }) => (
  <div className="mt-4">
    <button
      onClick={onToggle}
      className="text-blue-600 hover:text-blue-800 text-sm font-medium flex items-center gap-2"
    >
      <span>{isVisible ? '📖' : '💡'}</span>
      {isVisible ? 'Ocultar explicación' : '¿Qué significa esto?'}
    </button>

    {isVisible && (
      <div className="mt-3 p-4 bg-blue-50 rounded-lg border border-blue-200">
        <h4 className="font-semibold text-blue-900 mb-2">
          📊 Análisis de Sentimiento en Noticias Médicas
        </h4>
        <div className="text-sm text-blue-800 space-y-2">
          <p>
            <strong>¿Qué es?</strong> Una técnica que usa inteligencia artificial para identificar
            si una noticia médica transmite emociones positivas, negativas o neutrales.
          </p>
          <p>
            <strong>¿Por qué importa?</strong> Nos ayuda a entender cómo se comunica la información
            sobre cáncer de mama y su posible impacto emocional en pacientes y familias.
          </p>
          <div className="mt-3 space-y-1">
            <div className="flex items-center gap-2">
              <div className="w-3 h-3 bg-green-500 rounded-full"></div>
              <span><strong>Verde (Positivo):</strong> Avances médicos, tratamientos exitosos</span>
            </div>
            <div className="flex items-center gap-2">
              <div className="w-3 h-3 bg-red-500 rounded-full"></div>
              <span><strong>Rojo (Negativo):</strong> Riesgos, problemas, estadísticas preocupantes</span>
            </div>
            <div className="flex items-center gap-2">
              <div className="w-3 h-3 bg-gray-500 rounded-full"></div>
              <span><strong>Gris (Neutro):</strong> Información médica objetiva</span>
            </div>
          </div>
        </div>
      </div>
    )}
  </div>
);

// Professional statistics panel
const ProfessionalStats = ({ data }: { data: SentimentData[] }) => {
  const total = data.reduce((sum, item) => sum + item.value, 0);
  const negativeRatio = data.find(d => d.sentiment === 'negative')?.percentage || 0;

  return (
    <div className="mt-4 p-4 bg-gray-50 rounded-lg border">
      <h4 className="font-semibold text-gray-900 mb-3">📈 Análisis Estadístico</h4>
      <div className="grid grid-cols-2 gap-4 text-sm">
        <div>
          <p className="text-gray-600">Total artículos analizados</p>
          <p className="text-2xl font-bold text-gray-900">{total}</p>
        </div>
        <div>
          <p className="text-gray-600">Sentimiento predominante</p>
          <p className="text-lg font-semibold text-red-600">
            {negativeRatio}% Negativo
          </p>
        </div>
        <div className="col-span-2">
          <p className="text-gray-600 text-xs">
            <strong>Interpretación médica:</strong> El {negativeRatio}% de sentimiento negativo
            puede reflejar la naturaleza seria del tema de cáncer de mama en medios de comunicación.
          </p>
        </div>
      </div>
    </div>
  );
};

// Custom legend for medical context
interface LegendProps {
  payload?: Array<{
    value: string;
    color: string;
    payload?: SentimentData;
  }>;
}

const MedicalLegend = ({ payload }: LegendProps) => (
  <div className="flex justify-center mt-4">
    <div className="flex flex-wrap gap-4 text-sm">
      {payload?.map((entry, index: number) => (
        <div key={index} className="flex items-center gap-2">
          <div
            className="w-3 h-3 rounded-full"
            style={{ backgroundColor: entry.color }}
          />
          <span className="font-medium">
            {entry.value === 'positive' ? 'Positivo' :
             entry.value === 'negative' ? 'Negativo' : 'Neutro'}
          </span>
          <span className="text-gray-600">
            ({entry.payload?.value} artículos)
          </span>
        </div>
      ))}
    </div>
  </div>
);

export const SentimentChart: React.FC<SentimentChartProps> = ({
  data,
  loading = false,
  className = ''
}) => {
  const { mode } = useDualMode();
  const [showExplanation, setShowExplanation] = useState(false);
  const [viewType, setViewType] = useState<'pie' | 'bar'>('pie');

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
        <p className="text-gray-600">No hay datos de sentimiento disponibles</p>
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
            {isEducational ? '😊 Sentimientos en Noticias Médicas' : '📊 Análisis de Sentimiento'}
          </h3>
          <p className="text-sm text-gray-600 mt-1">
            {isEducational
              ? 'Cómo se sienten las noticias sobre cáncer de mama'
              : 'Distribución emocional en literatura médica analizada'
            }
          </p>
        </div>

        {/* View toggle for professional mode */}
        {!isEducational && (
          <div className="flex bg-gray-100 rounded-lg p-1">
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
          </div>
        )}
      </div>

      {/* Chart visualization */}
      <div className="h-64 mb-4">
        <ResponsiveContainer width="100%" height="100%">
          {viewType === 'pie' ? (
            <PieChart>
              <Pie
                data={data}
                cx="50%"
                cy="50%"
                innerRadius={isEducational ? 40 : 60}
                outerRadius={isEducational ? 80 : 100}
                paddingAngle={2}
                dataKey="value"
                nameKey="sentiment"
              >
                {data.map((entry, index) => (
                  <Cell
                    key={`cell-${index}`}
                    fill={MEDICAL_COLORS[entry.sentiment as keyof typeof MEDICAL_COLORS]}
                  />
                ))}
              </Pie>
              <Tooltip content={<MedicalTooltip />} />
              <Legend content={<MedicalLegend />} />
            </PieChart>
          ) : (
            <BarChart data={data} margin={{ top: 20, right: 30, left: 20, bottom: 5 }}>
              <CartesianGrid strokeDasharray="3 3" stroke="#f3f4f6" />
              <XAxis
                dataKey="sentiment"
                tick={{ fontSize: 12 }}
                tickFormatter={(value) =>
                  value === 'positive' ? 'Positivo' :
                  value === 'negative' ? 'Negativo' : 'Neutro'
                }
              />
              <YAxis tick={{ fontSize: 12 }} />
              <Tooltip content={<MedicalTooltip />} />
              <Bar
                dataKey="value"
                radius={[4, 4, 0, 0]}
              >
                {data.map((entry, index) => (
                  <Cell
                    key={`cell-${index}`}
                    fill={MEDICAL_COLORS[entry.sentiment as keyof typeof MEDICAL_COLORS]}
                  />
                ))}
              </Bar>
            </BarChart>
          )}
        </ResponsiveContainer>
      </div>

      {/* Mode-specific content */}
      {isEducational ? (
        <EducationalExplanation
          isVisible={showExplanation}
          onToggle={() => setShowExplanation(!showExplanation)}
        />
      ) : (
        <ProfessionalStats data={data} />
      )}

      {/* Summary insights for both modes */}
      <div className={`mt-4 p-3 rounded-lg ${isEducational ? 'bg-blue-50 border-blue-200' : 'bg-gray-50 border-gray-200'} border`}>
        <h4 className={`font-medium mb-2 ${isEducational ? 'text-blue-900' : 'text-gray-900'}`}>
          🔍 {isEducational ? 'Hallazgos Principales' : 'Key Insights'}
        </h4>
        <div className="text-sm space-y-1">
          {data.map((item) => (
            <p key={item.sentiment} className={isEducational ? 'text-blue-800' : 'text-gray-700'}>
              <strong>{item.percentage}%</strong> de las noticias son{' '}
              <span className="font-medium">
                {item.sentiment === 'positive' ? 'positivas' :
                 item.sentiment === 'negative' ? 'negativas' : 'neutrales'}
              </span>
              {' '}({item.value} artículos)
            </p>
          ))}
        </div>
      </div>
    </div>
  );
};

export default SentimentChart;
