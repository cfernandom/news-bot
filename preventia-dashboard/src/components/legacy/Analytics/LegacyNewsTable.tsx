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

  const hasRealData = data && data.length > 0;

  if (!hasRealData) {
    return (
      <div className="legacy-news-table">
        <div className="legacy-table-header">
          <h3>Noticias Filtradas</h3>
          <p>0 resultados encontrados</p>
        </div>
        <div style={{ height: '400px', display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center' }}>
          <i className="fas fa-newspaper" style={{ fontSize: '48px', color: '#6b7280', marginBottom: '20px' }}></i>
          <p style={{ color: 'var(--text-secondary)', textAlign: 'center' }}>
            No se pudieron obtener los datos de noticias.<br />
            Verifique la conexión con la API.
          </p>
        </div>
      </div>
    );
  }

  const newsData = data;

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
      UK: '🇬🇧',
      DE: '🇩🇪',
      CO: '🇨🇴',
      ES: '🇪🇸',
      MX: '🇲🇽',
      Unknown: '🌍',
    };
    return flags[country] || '🌍';
  };

  const getCountryName = (country: string) => {
    const names: Record<string, string> = {
      US: 'Estados Unidos',
      UK: 'Reino Unido',
      DE: 'Alemania',
      CO: 'Colombia',
      ES: 'España',
      MX: 'México',
      Unknown: 'Desconocido',
    };
    return names[country] || country;
  };

  const getLanguageName = (language: string) => {
    const languages: Record<string, string> = {
      en: 'Inglés',
      es: 'Español',
      de: 'Alemán',
      fr: 'Francés',
      it: 'Italiano',
      pt: 'Portugués',
    };
    return languages[language.toLowerCase()] || language;
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
                      {getCountryFlag(item.country)} {getCountryName(item.country)}
                    </span>
                  </td>
                  <td>
                    <span className="legacy-language">
                      {getLanguageName(item.language)}
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
