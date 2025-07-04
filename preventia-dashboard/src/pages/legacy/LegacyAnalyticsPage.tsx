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
import { useLegacyGeneralStats, useLegacySentimentStats, useLegacyTopicsStats, useLegacyGeographicData, useLegacyNews, useLegacyLanguageStats, useLegacyDailyArticles, useLegacySentimentTimeline, useLegacyTopicsWithLanguage } from '../../hooks/useLegacyData';

interface FilterState {
  country: string;
  language: string;
  date: string;
  topic: string;
  keyword: string;
}

interface NewsItem {
  id: string;
  title: string;
  country: string;
  language: string;
  date: string;
  published_at?: string;
  topic: string;
  sentiment: string;
  url: string;
  source: string;
  summary?: string;
}

const LegacyAnalyticsPage: React.FC = () => {
  const [showExportModal, setShowExportModal] = useState(false);
  const [selectedNews, setSelectedNews] = useState<NewsItem | null>(null);

  // Separate filter states for each section
  const [topicFilters, setTopicFilters] = useState<FilterState>({
    country: '',
    language: '',
    date: '',
    topic: '',
    keyword: ''
  });

  const [sentimentFilters, setSentimentFilters] = useState<FilterState>({
    country: '',
    language: '',
    date: '',
    topic: '',
    keyword: ''
  });

  const [geoFilters, setGeoFilters] = useState<FilterState>({
    country: '',
    language: '',
    date: '',
    topic: '',
    keyword: ''
  });

  const [newsFilters, setNewsFilters] = useState<FilterState>({
    country: '',
    language: '',
    date: '',
    topic: '',
    keyword: ''
  });

  const { data: generalStats, isLoading: statsLoading } = useLegacyGeneralStats();
  const { data: sentimentData, isLoading: sentimentLoading } = useLegacySentimentStats(sentimentFilters);
  const { data: topicsData, isLoading: topicsLoading } = useLegacyTopicsStats(topicFilters);
  const { data: geographicData, isLoading: geoLoading } = useLegacyGeographicData(geoFilters);
  const { data: newsData, isLoading: newsLoading } = useLegacyNews(newsFilters);
  const { data: languageData, isLoading: languageLoading } = useLegacyLanguageStats();
  const { data: dailyArticlesData, isLoading: dailyArticlesLoading } = useLegacyDailyArticles(14);
  const { data: sentimentTimelineData, isLoading: sentimentTimelineLoading } = useLegacySentimentTimeline(8);
  const { data: topicsWithLanguageData, isLoading: topicsWithLanguageLoading } = useLegacyTopicsWithLanguage(8);

  // Calculate date ranges and temporal context
  const getGlobalDateRange = (): { startDate: string; endDate: string } | undefined => {
    if (!generalStats?.latest_article_date) return undefined;

    // Calculate approximate start date based on total articles and daily average
    const totalArticles = generalStats.total_articles || 0;
    const estimatedDaysBack = Math.max(30, Math.min(365, totalArticles * 2)); // Estimate 2 days per article, min 30 days, max 1 year
    const endDate = new Date(generalStats.latest_article_date);
    const startDate = new Date(endDate);
    startDate.setDate(endDate.getDate() - estimatedDaysBack);

    return {
      startDate: startDate.toISOString().split('T')[0],
      endDate: generalStats.latest_article_date
    };
  };

  const getFilteredDateRange = (): { startDate: string; endDate: string } | undefined => {
    if (!newsData || !Array.isArray(newsData) || newsData.length === 0) return undefined;

    const dates: string[] = newsData
      .map((item: NewsItem) => item.date || item.published_at)
      .filter((date: string | undefined): date is string => date !== undefined)
      .sort();

    return dates.length > 0 ? {
      startDate: dates[0],
      endDate: dates[dates.length - 1]
    } : undefined;
  };

  const globalDateRange = getGlobalDateRange();
  const filteredDateRange = getFilteredDateRange();
  const totalArticles = generalStats?.total_articles || 0;
  const filteredArticles = newsData?.length || 0;

  // Determine if filters are applied for news section
  const hasActiveNewsFilters = Object.values(newsFilters).some(value => value && value.trim() !== '');
  const hasActiveFilters = hasActiveNewsFilters; // Alias for backward compatibility
  const displayDateRange = hasActiveNewsFilters ? filteredDateRange : globalDateRange;
  const displayArticleCount = hasActiveNewsFilters ? filteredArticles : totalArticles;

  // Filter change handlers for each section
  const handleTopicFilterChange = (newFilters: Partial<FilterState>) => {
    setTopicFilters(prev => ({ ...prev, ...newFilters }));
  };

  const handleSentimentFilterChange = (newFilters: Partial<FilterState>) => {
    setSentimentFilters(prev => ({ ...prev, ...newFilters }));
  };

  const handleGeoFilterChange = (newFilters: Partial<FilterState>) => {
    setGeoFilters(prev => ({ ...prev, ...newFilters }));
  };

  const handleNewsFilterChange = (newFilters: Partial<FilterState>) => {
    setNewsFilters(prev => ({ ...prev, ...newFilters }));
  };

  const handleNewsSelect = (news: NewsItem) => {
    setSelectedNews(news);
  };

  if (statsLoading || sentimentLoading || topicsLoading || languageLoading || dailyArticlesLoading || sentimentTimelineLoading || topicsWithLanguageLoading) {
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
          {displayArticleCount > 0 && (
            <><br />
            <strong>{hasActiveFilters ? 'Datos filtrados:' : 'Dataset completo:'}</strong> {displayArticleCount} artículos
            {displayDateRange && (
              <> desde {new Date(displayDateRange.startDate).toLocaleDateString('es-ES')} hasta {new Date(displayDateRange.endDate).toLocaleDateString('es-ES')}</>
            )}
            {hasActiveFilters && totalArticles > 0 && (
              <><br /><small>Dataset total: {totalArticles} artículos</small></>
            )}
            </>
          )}
        </p>

        <button
          className="legacy-export-btn"
          onClick={() => setShowExportModal(true)}
        >
          <i className="fas fa-download"></i>
          Exportar Datos
        </button>
      </div>

      {/* 4.1 Resumen General */}
      <section className="legacy-analytics-section">
        <h2 className="legacy-section-title">📈 Resumen General</h2>
        <p className="legacy-section-description">
          {hasActiveFilters
            ? `Visión general de ${filteredArticles} artículos que coinciden con los filtros aplicados${filteredDateRange ? ` (${new Date(filteredDateRange.startDate).toLocaleDateString('es-ES')} - ${new Date(filteredDateRange.endDate).toLocaleDateString('es-ES')})` : ''}.`
            : globalDateRange
            ? `Visión general y cuantitativa de la cobertura informativa desde ${new Date(globalDateRange.startDate).toLocaleDateString('es-ES')} hasta ${new Date(globalDateRange.endDate).toLocaleDateString('es-ES')}.`
            : 'Visión general y cuantitativa de la cobertura informativa en el dataset histórico acumulado.'
          }
        </p>

        {/* a) Tarjetas de Indicadores */}
        <div className="legacy-analytics-grid">
          <LegacyKPICard
            title={hasActiveFilters ? "Noticias Filtradas" : "Noticias Recolectadas"}
            value={displayArticleCount > 0 ? displayArticleCount : 'Sin datos'}
            subtitle={displayDateRange
              ? `Del ${new Date(displayDateRange.startDate).toLocaleDateString('es-ES')} al ${new Date(displayDateRange.endDate).toLocaleDateString('es-ES')}`
              : hasActiveFilters
              ? 'Filtros aplicados'
              : 'Datos históricos acumulados'
            }
            icon="fa-newspaper"
          />

          <LegacyKPICard
            title="Idioma Dominante"
            value={generalStats?.dominant_language || 'No disponible'}
            subtitle={generalStats?.language_percentage
              ? `${generalStats.language_percentage}% del contenido`
              : 'Información no disponible'
            }
            icon="fa-language"
          />

          <LegacyKPICard
            title="País Más Activo"
            value={generalStats?.most_active_country || 'No disponible'}
            subtitle={generalStats?.most_active_country
              ? "Mayor generación de publicaciones"
              : "Información geográfica no disponible"
            }
            icon="fa-flag"
          />

          <LegacyKPICard
            title="Medio Más Frecuente"
            value={generalStats?.most_frequent_source || 'No disponible'}
            subtitle={generalStats?.most_frequent_source
              ? "Fuente con mayor cantidad de artículos"
              : "Información de fuentes no disponible"
            }
            icon="fa-globe"
          />
        </div>

        {/* b) Gráficos Complementarios */}
        <div className="legacy-charts-main-grid">
          <LegacySentimentChart
            data={languageData || []}
            loading={languageLoading}
            title="Distribución de Idiomas"
            subtitle={`Dataset completo: ${totalArticles} artículos`}
            type="language"
          />

          <LegacyTrendChart
            data={dailyArticlesData || []}
            loading={dailyArticlesLoading}
            title="Noticias por Día"
            subtitle="Últimos 14 días"
          />
        </div>

        {/* c) Resumen Automatizado (IA) */}
        <div className="legacy-ai-summary">
          <h3><i className="fas fa-robot"></i> Resumen Automatizado (IA)</h3>
          <p>
            {generalStats?.ai_summary ||
            (totalArticles > 0
              ? `Análisis de ${totalArticles} artículos recopilados${globalDateRange ? ` desde ${new Date(globalDateRange.startDate).toLocaleDateString('es-ES')} hasta ${new Date(globalDateRange.endDate).toLocaleDateString('es-ES')}` : ' en el dataset actual'}. El sistema de IA está procesando la información para generar insights automáticos.`
              : "No hay datos suficientes para generar un resumen automatizado. Verifique la conexión con la API o la disponibilidad de datos."
            )}
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
          filters={topicFilters}
          onFilterChange={handleTopicFilterChange}
          showTopicFilter={true}
          showDateFilter={true}
        />

        {/* b) Visualización de Temas */}
        <div className="legacy-chart-container">
          <LegacyTopicsChart
            data={topicsWithLanguageData || []}
            loading={topicsWithLanguageLoading}
            title="Frecuencia por Temas"
            subtitle={`Últimas 8 semanas${Object.values(topicFilters).some(value => value && value.trim() !== '') ? ' (filtros aplicados)' : ''}`}
            showLanguageBreakdown={true}
            dateRange={displayDateRange}
            totalArticles={displayArticleCount}
          />
        </div>

        {/* c) Resumen Automatizado (IA) */}
        <div className="legacy-ai-summary">
          <h3><i className="fas fa-robot"></i> Análisis Temático (IA)</h3>
          <p>
            {topicsData?.ai_summary ||
            (topicsWithLanguageData && topicsWithLanguageData.length > 0
              ? `Análisis temático de ${topicsWithLanguageData.reduce((sum: number, item: { count?: number }) => sum + (item.count || 0), 0)} artículos categorizados en ${topicsWithLanguageData.length} temas principales. El sistema está procesando patrones y tendencias temáticas.`
              : "No hay datos temáticos suficientes para generar análisis automatizado. Los artículos pueden estar en proceso de categorización."
            )}
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
          filters={sentimentFilters}
          onFilterChange={handleSentimentFilterChange}
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
            subtitle={Object.values(sentimentFilters).some(value => value && value.trim() !== '') ? `Datos filtrados` : `Dataset completo: ${totalArticles} artículos`}
            type="sentiment"
          />

          <LegacyTrendChart
            data={sentimentTimelineData || []}
            loading={sentimentTimelineLoading}
            title="Evolución Temporal del Tono"
            subtitle="Últimas 8 semanas"
            showSentimentLines={true}
          />
        </div>

        {/* d) Resumen Automatizado (IA) */}
        <div className="legacy-ai-summary">
          <h3><i className="fas fa-robot"></i> Análisis de Tono (IA)</h3>
          <p>
            {sentimentData?.ai_summary ||
            (sentimentData && sentimentData.length > 0
              ? `Análisis de sentimiento procesado en ${sentimentData.reduce((sum: number, item: { count?: number }) => sum + (item.count || 0), 0)} artículos. El sistema está evaluando la carga emocional y distribución tonal del contenido.`
              : "No hay datos de sentimiento suficientes para generar análisis automatizado. Los artículos pueden estar en proceso de análisis de PLN."
            )}
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
          filters={geoFilters}
          onFilterChange={handleGeoFilterChange}
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
            subtitle={Object.values(geoFilters).some(value => value && value.trim() !== '') ? `Datos filtrados` : `Dataset completo: ${totalArticles} artículos`}
          />
        </div>

        {/* d) Resumen Automatizado (IA) */}
        <div className="legacy-ai-summary">
          <h3><i className="fas fa-robot"></i> Análisis Geográfico (IA)</h3>
          <p>
            {geographicData?.ai_summary ||
            (geographicData && geographicData.length > 0
              ? `Análisis geográfico de ${geographicData.reduce((sum: number, item: { total?: number }) => sum + (item.total || 0), 0)} artículos distribuidos en ${geographicData.length} países. El sistema está evaluando patrones de cobertura internacional.`
              : "No hay datos geográficos suficientes para generar análisis automatizado. La información de ubicación puede estar en proceso de geocodificación."
            )}
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
          filters={newsFilters}
          onFilterChange={handleNewsFilterChange}
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
            filters={newsFilters}
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
