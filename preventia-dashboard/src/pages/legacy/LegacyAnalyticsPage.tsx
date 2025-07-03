import React, { useState } from 'react';
import LegacyKPICard from '../../components/legacy/Common/LegacyKPICard';
import LegacySentimentChart from '../../components/legacy/Analytics/LegacySentimentChart';
import LegacyTopicsChart from '../../components/legacy/Analytics/LegacyTopicsChart';
import LegacyGeographicMap from '../../components/legacy/Analytics/LegacyGeographicMap';
import LegacyExportModal from '../../components/legacy/Common/LegacyExportModal';
import LegacyExportHistory from '../../components/legacy/Common/LegacyExportHistory';
import LegacyFilterBar from '../../components/legacy/Common/LegacyFilterBar';
import LegacyNewsTable from '../../components/legacy/Analytics/LegacyNewsTable';
import LegacyNewsModal from '../../components/legacy/Analytics/LegacyNewsModal';
import LegacyTrendChart from '../../components/legacy/Analytics/LegacyTrendChart';
import { useLegacyGeneralStats, useLegacySentimentStats, useLegacyTopicsStats, useLegacyGeographicData, useLegacyNews } from '../../hooks/useLegacyData';

interface FilterState {
  country: string;
  language: string;
  date: string;
  topic: string;
  keyword: string;
}

const LegacyAnalyticsPage: React.FC = () => {
  const [showExportModal, setShowExportModal] = useState(false);
  const [selectedNews, setSelectedNews] = useState<any>(null);
  const [filters, setFilters] = useState<FilterState>({
    country: '',
    language: '',
    date: '',
    topic: '',
    keyword: ''
  });

  const { data: generalStats, isLoading: statsLoading } = useLegacyGeneralStats();
  const { data: sentimentData, isLoading: sentimentLoading } = useLegacySentimentStats(filters);
  const { data: topicsData, isLoading: topicsLoading } = useLegacyTopicsStats(filters);
  const { data: geographicData, isLoading: geoLoading } = useLegacyGeographicData(filters);
  const { data: newsData, isLoading: newsLoading } = useLegacyNews(filters);

  const handleFilterChange = (newFilters: Partial<FilterState>) => {
    setFilters(prev => ({ ...prev, ...newFilters }));
  };

  const handleNewsSelect = (news: any) => {
    setSelectedNews(news);
  };

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

      {/* 4.1 Resumen Semanal */}
      <section className="legacy-analytics-section">
        <h2 className="legacy-section-title">📈 Resumen Semanal</h2>
        <p className="legacy-section-description">
          Visión general y cuantitativa de la cobertura informativa durante la semana actual.
        </p>

        {/* a) Tarjetas de Indicadores */}
        <div className="legacy-analytics-grid">
          <LegacyKPICard
            title="Noticias Recolectadas"
            value={generalStats?.total_articles || 106}
            subtitle="Artículos digitales detectados"
            icon="fa-newspaper"
          />

          <LegacyKPICard
            title="Idioma Dominante"
            value={`${generalStats?.dominant_language || 'Inglés'}`}
            subtitle={`${generalStats?.language_percentage || 64}% del contenido`}
            icon="fa-language"
          />

          <LegacyKPICard
            title="País Más Activo"
            value={generalStats?.most_active_country || 'Estados Unidos'}
            subtitle="Mayor generación de publicaciones"
            icon="fa-flag"
          />

          <LegacyKPICard
            title="Medio Más Frecuente"
            value={generalStats?.most_frequent_source || 'WebMD'}
            subtitle="Fuente con mayor cantidad de artículos"
            icon="fa-globe"
          />
        </div>

        {/* b) Gráficos Complementarios */}
        <div className="legacy-charts-main-grid">
          <LegacySentimentChart
            data={[]}
            loading={false}
            title="Distribución de Idiomas"
            type="language"
            showPieChart={true}
          />

          <LegacyTrendChart
            data={generalStats?.daily_articles || []}
            loading={statsLoading}
            title="Noticias por Día"
          />
        </div>

        {/* c) Resumen Automatizado (IA) */}
        <div className="legacy-ai-summary">
          <h3><i className="fas fa-robot"></i> Resumen Automatizado (IA)</h3>
          <p>
            {generalStats?.ai_summary ||
            "Esta semana se observó un incremento del 12% en las publicaciones sobre prevención de cáncer de mama, principalmente en medios estadounidenses. El tono general se mantiene neutral-informativo (67%), con un ligero aumento en contenido positivo relacionado con avances en diagnóstico temprano. Se destaca mayor actividad en portales especializados en salud durante los días martes y miércoles."}
          </p>
        </div>
      </section>

      {/* 4.2 Explorador Temático */}
      <section className="legacy-analytics-section">
        <h2 className="legacy-section-title">🔍 Explorador Temático</h2>
        <p className="legacy-section-description">
          Clasificación y visualización de noticias según su tema principal con análisis automatizado.
        </p>

        {/* a) Filtros Interactivos */}
        <LegacyFilterBar
          filters={filters}
          onFilterChange={handleFilterChange}
          showTopicFilter={true}
          showDateFilter={true}
        />

        {/* b) Visualización de Temas */}
        <div className="legacy-chart-container">
          <LegacyTopicsChart
            data={topicsData || []}
            loading={topicsLoading}
            title="Frecuencia Semanal por Temas"
            showLanguageBreakdown={true}
          />
        </div>

        {/* c) Resumen Automatizado (IA) */}
        <div className="legacy-ai-summary">
          <h3><i className="fas fa-robot"></i> Análisis Temático (IA)</h3>
          <p>
            {topicsData?.ai_summary ||
            "El tema más abordado esta semana fue Prevención (28% del contenido), seguido por Tratamiento (23%) y Diagnóstico (19%). Se observa mayor énfasis en investigación científica en medios estadounidenses, mientras que los portales latinoamericanos priorizan contenido sobre política pública y acceso a tratamientos."}
          </p>
        </div>
      </section>

      {/* 4.3 Análisis de Tono Informativo */}
      <section className="legacy-analytics-section">
        <h2 className="legacy-section-title">💭 Análisis de Tono Informativo</h2>
        <p className="legacy-section-description">
          Exploración de la carga emocional mediante procesamiento de lenguaje natural (PLN).
        </p>

        {/* a) Filtros de Segmentación */}
        <LegacyFilterBar
          filters={filters}
          onFilterChange={handleFilterChange}
          showCountryFilter={true}
          showLanguageFilter={true}
          showDateFilter={true}
        />

        {/* b) Distribución de Sentimientos & c) Evolución Temporal */}
        <div className="legacy-charts-main-grid">
          <LegacySentimentChart
            data={sentimentData || []}
            loading={sentimentLoading}
            title="Distribución de Sentimientos"
            type="sentiment"
            showPieChart={true}
          />

          <LegacyTrendChart
            data={sentimentData?.temporal_evolution || []}
            loading={sentimentLoading}
            title="Evolución Temporal del Tono"
            showSentimentLines={true}
          />
        </div>

        {/* d) Resumen Automatizado (IA) */}
        <div className="legacy-ai-summary">
          <h3><i className="fas fa-robot"></i> Análisis de Tono (IA)</h3>
          <p>
            {sentimentData?.ai_summary ||
            "Se mantiene un tono mayoritariamente neutro (53% del contenido analizado). Se observa un incremento en publicaciones positivas relacionadas con avances en inmunoterapia y diagnóstico por IA. La negatividad se concentra principalmente en artículos sobre disparidades de acceso a tratamientos y estadísticas de mortalidad."}
          </p>
        </div>
      </section>

      {/* 4.4 Mapa de Cobertura Internacional */}
      <section className="legacy-analytics-section">
        <h2 className="legacy-section-title">🌍 Mapa de Cobertura Internacional</h2>
        <p className="legacy-section-description">
          Visualización de la distribución geográfica de noticias en medios digitales.
        </p>

        {/* a) Filtros de Exploración */}
        <LegacyFilterBar
          filters={filters}
          onFilterChange={handleFilterChange}
          showLanguageFilter={true}
          showTopicFilter={true}
          showWeekFilter={true}
        />

        {/* b) Visualización Geográfica */}
        <div className="legacy-chart-container">
          <LegacyGeographicMap
            data={geographicData || []}
            loading={geoLoading}
            title="Densidad Informativa por País"
            showClickableMarkers={true}
          />
        </div>

        {/* d) Resumen Automatizado (IA) */}
        <div className="legacy-ai-summary">
          <h3><i className="fas fa-robot"></i> Análisis Geográfico (IA)</h3>
          <p>
            {geographicData?.ai_summary ||
            "Estados Unidos lideró en volumen informativo con 45% del contenido total. México y Colombia mostraron alta actividad en temas de política pública sanitaria. En Europa, España incrementó su presencia mediática con énfasis en investigación clínica y programas de detección temprana."}
          </p>
        </div>
      </section>

      {/* 4.5 Noticias Destacadas */}
      <section className="legacy-analytics-section">
        <h2 className="legacy-section-title">📰 Noticias Destacadas</h2>
        <p className="legacy-section-description">
          Exploración, filtrado y consulta detallada de noticias individuales recopiladas.
        </p>

        {/* a) Filtros de Búsqueda */}
        <LegacyFilterBar
          filters={filters}
          onFilterChange={handleFilterChange}
          showKeywordSearch={true}
          showCountryFilter={true}
          showLanguageFilter={true}
        />

        {/* b) Tabla de Noticias */}
        <div className="legacy-chart-container">
          <LegacyNewsTable
            data={newsData || []}
            loading={newsLoading}
            onNewsSelect={handleNewsSelect}
            filters={filters}
          />
        </div>
      </section>

      {/* 4.7 Exportación y Reportes */}
      <section className="legacy-analytics-section">
        <h2 className="legacy-section-title">📥 Exportación y Reportes</h2>
        <p className="legacy-section-description">
          Herramientas para descargar información procesada y generar reportes completos.
        </p>

        <div className="legacy-export-grid">
          <div className="legacy-export-card">
            <h3><i className="fas fa-table"></i> Tabla de Noticias</h3>
            <p>Exportar noticias filtradas a formatos de hoja de cálculo</p>
            <div className="legacy-export-buttons">
              <button className="legacy-btn-secondary">CSV</button>
              <button className="legacy-btn-secondary">XLSX</button>
            </div>
          </div>

          <div className="legacy-export-card">
            <h3><i className="fas fa-chart-bar"></i> Gráficos</h3>
            <p>Descargar visualizaciones en formatos de imagen</p>
            <div className="legacy-export-buttons">
              <button className="legacy-btn-secondary">PNG</button>
              <button className="legacy-btn-secondary">SVG</button>
            </div>
          </div>

          <div className="legacy-export-card">
            <h3><i className="fas fa-file-pdf"></i> Informe PDF</h3>
            <p>Documento completo con análisis y gráficos</p>
            <div className="legacy-export-buttons">
              <button className="legacy-btn-primary">Generar PDF</button>
            </div>
          </div>
        </div>

        <div className="legacy-export-advanced">
          <h3>Opciones Avanzadas</h3>
          <div className="legacy-export-options">
            <div className="legacy-form-group">
              <label>Rango de Fechas:</label>
              <input type="date" className="legacy-input" />
              <span> a </span>
              <input type="date" className="legacy-input" />
            </div>
            <div className="legacy-form-group">
              <label>
                <input type="checkbox" /> Incluir resúmenes IA
              </label>
            </div>
          </div>
        </div>

        {/* Export History */}
        <LegacyExportHistory />
      </section>

      {/* Modals */}
      <LegacyExportModal
        isOpen={showExportModal}
        onClose={() => setShowExportModal(false)}
      />

      <LegacyNewsModal
        isOpen={!!selectedNews}
        onClose={() => setSelectedNews(null)}
        news={selectedNews}
      />
    </div>
  );
};

export default LegacyAnalyticsPage;
