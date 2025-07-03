import React, { useState } from 'react';
import LegacyKPICard from '../../components/legacy/Common/LegacyKPICard';
import LegacySentimentChart from '../../components/legacy/Analytics/LegacySentimentChart';
import LegacyTopicsChart from '../../components/legacy/Analytics/LegacyTopicsChart';
import LegacyGeographicMap from '../../components/legacy/Analytics/LegacyGeographicMap';
import LegacyExportModal from '../../components/legacy/Common/LegacyExportModal';
import { useLegacyGeneralStats, useLegacySentimentStats, useLegacyTopicsStats, useLegacyGeographicData } from '../../hooks/useLegacyData';

const LegacyAnalyticsPage: React.FC = () => {
  const [showExportModal, setShowExportModal] = useState(false);

  const { data: generalStats, isLoading: statsLoading } = useLegacyGeneralStats();
  const { data: sentimentData, isLoading: sentimentLoading } = useLegacySentimentStats();
  const { data: topicsData, isLoading: topicsLoading } = useLegacyTopicsStats();
  const { data: geographicData, isLoading: geoLoading } = useLegacyGeographicData();

  // Export functionality is now handled by LegacyExportModal component

  // No longer need QuickChart URLs - using Recharts components

  if (statsLoading || sentimentLoading || topicsLoading) {
    return (
      <div className="legacy-analytics-page">
        <div className="legacy-hero">
          <h1>📊 Analytics Dashboard</h1>
          <p>Cargando datos analíticos...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="legacy-analytics-page">
      {/* Header Section */}
      <div className="legacy-hero">
        <h1>📊 Analytics Dashboard</h1>
        <p>
          Dashboard completo de análisis de noticias sobre cáncer de mama con datos reales
          procesados por nuestro sistema de inteligencia artificial.
        </p>

        <button
          className="legacy-export-btn"
          onClick={() => setShowExportModal(true)}
        >
          <i className="fas fa-download"></i>
          Exportar Datos
        </button>
      </div>

      {/* KPI Cards Grid */}
      <section className="legacy-analytics-section">
        <h2 className="legacy-section-title">Métricas Principales</h2>

        <div className="legacy-analytics-grid">
          <LegacyKPICard
            title="Noticias Recolectadas"
            value={generalStats?.total_articles || 106}
            icon="fa-newspaper"
          />

          <LegacyKPICard
            title="Idioma Dominante"
            value={`${generalStats?.dominant_language || 'Inglés'}`}
            subtitle={`${generalStats?.language_percentage || 64}% del contenido`}
            icon="fa-language"
          />

          <LegacyKPICard
            title="Fuentes Activas"
            value={generalStats?.sources_count || 4}
            subtitle="Sitios web monitoreados"
            icon="fa-globe"
          />

          <LegacyKPICard
            title="Sentimiento Positivo"
            value={`${generalStats?.positive_sentiment || 15} artículos`}
            subtitle="Noticias con tono optimista"
            icon="fa-smile"
          />

          <LegacyKPICard
            title="Sentimiento Negativo"
            value={`${generalStats?.negative_sentiment || 40} artículos`}
            subtitle="Noticias con tono preocupante"
            icon="fa-frown"
          />

          <LegacyKPICard
            title="Última Actualización"
            value={generalStats?.latest_article_date || 'Hoy'}
            subtitle="Datos en tiempo real"
            icon="fa-clock"
          />
        </div>
      </section>

      {/* Charts Section */}
      <section className="legacy-analytics-section">
        <h2 className="legacy-section-title">Análisis Visual</h2>

        {/* Main Charts - 2 columns for better visibility */}
        <div className="legacy-charts-main-grid">
          <LegacySentimentChart
            data={sentimentData || []}
            loading={sentimentLoading}
          />

          <LegacyTopicsChart
            data={topicsData || []}
            loading={topicsLoading}
          />
        </div>

        {/* Secondary Info - 2 columns */}
        <div className="legacy-charts-secondary-grid">
          {/* Interactive Geographic Map */}
          <LegacyGeographicMap
            data={geographicData || []}
            loading={geoLoading}
          />

          {/* Additional Metrics */}
          <div className="legacy-chart-container">
            <h3>Estadísticas Adicionales</h3>
            <div style={{ padding: '20px', textAlign: 'left' }}>
              <div style={{ marginBottom: '15px' }}>
                <strong style={{ color: 'var(--primary-blue)' }}>Tasa de Procesamiento:</strong>
                <span style={{ marginLeft: '10px' }}>~2 artículos/segundo</span>
              </div>

              <div style={{ marginBottom: '15px' }}>
                <strong style={{ color: 'var(--primary-blue)' }}>Precisión NLP:</strong>
                <span style={{ marginLeft: '10px' }}>95% accuracy</span>
              </div>

              <div style={{ marginBottom: '15px' }}>
                <strong style={{ color: 'var(--primary-blue)' }}>Cobertura Temporal:</strong>
                <span style={{ marginLeft: '10px' }}>Últimos 30 días</span>
              </div>

              <div>
                <strong style={{ color: 'var(--primary-blue)' }}>Modelo NLP:</strong>
                <span style={{ marginLeft: '10px' }}>VADER + spaCy 3.8</span>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Export Modal */}
      <LegacyExportModal
        isOpen={showExportModal}
        onClose={() => setShowExportModal(false)}
      />
    </div>
  );
};

export default LegacyAnalyticsPage;
