import React, { useState } from 'react';

interface NewsItem {
  id: string;
  title: string;
  country: string;
  language: string;
  date: string;
  topic: string;
  sentiment: string;
  url: string;
  source: string;
  summary?: string;
}

interface FilterState {
  country: string;
  language: string;
  date: string;
  topic: string;
  keyword: string;
}

interface LegacyNewsTableProps {
  data: NewsItem[];
  loading?: boolean;
  onNewsSelect: (news: NewsItem) => void;
  filters: FilterState;
}

const LegacyNewsTable: React.FC<LegacyNewsTableProps> = ({
  data,
  loading = false,
  onNewsSelect,
  filters,
}) => {
  const [currentPage, setCurrentPage] = useState(1);
  const itemsPerPage = 10;

  // Default data for demonstration
  const defaultData: NewsItem[] = [
    {
      id: '1',
      title: 'Breakthrough in Early Breast Cancer Detection Using AI',
      country: 'US',
      language: 'en',
      date: '2024-06-15',
      topic: 'diagnosis',
      sentiment: 'positive',
      url: 'https://example.com/article1',
      source: 'WebMD',
      summary: 'Investigadores desarrollan nueva tecnología de IA para detección temprana.',
    },
    {
      id: '2',
      title: 'Nuevo tratamiento inmunoterapéutico muestra resultados prometedores',
      country: 'ES',
      language: 'es',
      date: '2024-06-14',
      topic: 'treatment',
      sentiment: 'positive',
      url: 'https://example.com/article2',
      source: 'Medical News',
      summary: 'Ensayo clínico fase III demuestra eficacia del 85% en pacientes.',
    },
    {
      id: '3',
      title: 'Rising Breast Cancer Rates in Young Women Concern Experts',
      country: 'US',
      language: 'en',
      date: '2024-06-13',
      topic: 'public_policy',
      sentiment: 'negative',
      url: 'https://example.com/article3',
      source: 'Health News',
      summary: 'Estadísticas muestran aumento preocupante en mujeres menores de 40.',
    },
    {
      id: '4',
      title: 'Campaña de prevención alcanza 50,000 mujeres en Colombia',
      country: 'CO',
      language: 'es',
      date: '2024-06-12',
      topic: 'prevention',
      sentiment: 'positive',
      url: 'https://example.com/article4',
      source: 'El Tiempo Salud',
      summary: 'Programa nacional supera metas de cobertura en zonas rurales.',
    },
    {
      id: '5',
      title: 'Patient Stories: Surviving Triple-Negative Breast Cancer',
      country: 'US',
      language: 'en',
      date: '2024-06-11',
      topic: 'testimonials',
      sentiment: 'neutral',
      url: 'https://example.com/article5',
      source: 'Cancer Support',
      summary: 'Testimonios inspiradores de supervivientes comparten su experiencia.',
    },
  ];

  const newsData = data && data.length > 0 ? data : defaultData;

  // Filter data based on filters
  const filteredData = newsData.filter((item) => {
    if (filters.keyword && !item.title.toLowerCase().includes(filters.keyword.toLowerCase()) &&
        !item.source.toLowerCase().includes(filters.keyword.toLowerCase())) {
      return false;
    }
    if (filters.country && item.country !== filters.country) return false;
    if (filters.language && item.language !== filters.language) return false;
    if (filters.date && item.date !== filters.date) return false;
    if (filters.topic && item.topic !== filters.topic) return false;
    return true;
  });

  // Pagination
  const totalPages = Math.ceil(filteredData.length / itemsPerPage);
  const startIndex = (currentPage - 1) * itemsPerPage;
  const endIndex = startIndex + itemsPerPage;
  const currentData = filteredData.slice(startIndex, endIndex);

  const getCountryFlag = (country: string) => {
    const flags: Record<string, string> = {
      US: '🇺🇸',
      CO: '🇨🇴',
      ES: '🇪🇸',
      MX: '🇲🇽',
    };
    return flags[country] || '🌍';
  };

  const getTopicLabel = (topic: string) => {
    const topics: Record<string, string> = {
      prevention: 'Prevención',
      treatment: 'Tratamiento',
      diagnosis: 'Diagnóstico',
      testimonials: 'Testimonios',
      public_policy: 'Política Pública',
      research: 'Investigación',
      other: 'Otros',
    };
    return topics[topic] || topic;
  };

  const getSentimentLabel = (sentiment: string) => {
    const sentiments: Record<string, { label: string; color: string; icon: string }> = {
      positive: { label: 'Positivo', color: '#28a745', icon: 'fa-smile' },
      negative: { label: 'Negativo', color: '#dc3545', icon: 'fa-frown' },
      neutral: { label: 'Neutro', color: '#6c757d', icon: 'fa-meh' },
    };
    return sentiments[sentiment] || { label: sentiment, color: '#6c757d', icon: 'fa-meh' };
  };

  if (loading) {
    return (
      <div className="legacy-news-table">
        <h3>Tabla de Noticias</h3>
        <div className="legacy-loading">
          <i className="fas fa-spinner fa-spin"></i>
          <p>Cargando noticias...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="legacy-news-table">
      <div className="legacy-table-header">
        <h3>Noticias Filtradas</h3>
        <p>{filteredData.length} resultados encontrados</p>
      </div>

      <div className="legacy-table-container">
        <table className="legacy-table">
          <thead>
            <tr>
              <th>Título</th>
              <th>País</th>
              <th>Idioma</th>
              <th>Fecha</th>
              <th>Tema</th>
              <th>Tono</th>
              <th>Acciones</th>
            </tr>
          </thead>
          <tbody>
            {currentData.map((item) => {
              const sentimentInfo = getSentimentLabel(item.sentiment);
              return (
                <tr key={item.id}>
                  <td>
                    <a
                      href={item.url}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="legacy-news-link"
                      title="Abrir artículo original"
                    >
                      {item.title}
                    </a>
                    <div className="legacy-news-source">{item.source}</div>
                  </td>
                  <td>
                    <span className="legacy-country">
                      {getCountryFlag(item.country)} {item.country}
                    </span>
                  </td>
                  <td>
                    <span className="legacy-language">
                      {item.language === 'en' ? 'Inglés' : 'Español'}
                    </span>
                  </td>
                  <td>{new Date(item.date).toLocaleDateString('es-ES')}</td>
                  <td>
                    <span className="legacy-topic-badge">
                      {getTopicLabel(item.topic)}
                    </span>
                  </td>
                  <td>
                    <span
                      className="legacy-sentiment-badge"
                      style={{ color: sentimentInfo.color }}
                    >
                      <i className={`fas ${sentimentInfo.icon}`}></i>
                      {sentimentInfo.label}
                    </span>
                  </td>
                  <td>
                    <button
                      className="legacy-btn-small legacy-btn-primary"
                      onClick={() => onNewsSelect(item)}
                      title="Ver resumen automatizado"
                    >
                      <i className="fas fa-eye"></i>
                      Ver resumen
                    </button>
                  </td>
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>

      {/* Pagination */}
      {totalPages > 1 && (
        <div className="legacy-pagination">
          <button
            className="legacy-btn-secondary"
            disabled={currentPage === 1}
            onClick={() => setCurrentPage(currentPage - 1)}
          >
            <i className="fas fa-chevron-left"></i>
            Anterior
          </button>

          <span className="legacy-pagination-info">
            Página {currentPage} de {totalPages}
          </span>

          <button
            className="legacy-btn-secondary"
            disabled={currentPage === totalPages}
            onClick={() => setCurrentPage(currentPage + 1)}
          >
            Siguiente
            <i className="fas fa-chevron-right"></i>
          </button>
        </div>
      )}
    </div>
  );
};

export default LegacyNewsTable;
