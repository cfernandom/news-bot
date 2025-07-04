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

  // Handle different empty states
  const hasRealData = data && Array.isArray(data) && data.length > 0;
  const hasValidData = hasRealData && data.some(item => item.title && item.id);

  if (loading) {
    return (
      <div className="legacy-news-table">
        <div className="legacy-table-header">
          <h3>Tabla de Noticias</h3>
          <p>Cargando datos...</p>
        </div>
        <div style={{ height: '400px', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
          <div className="legacy-loading-spinner">
            <i className="fas fa-spinner fa-spin" style={{ fontSize: '24px', color: 'var(--primary-blue)' }}></i>
            <p style={{ marginTop: '10px', color: 'var(--text-secondary)' }}>Cargando noticias...</p>
          </div>
        </div>
      </div>
    );
  }

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
            Verifique la conexión con la API o los filtros aplicados.
          </p>
        </div>
      </div>
    );
  }

  if (!hasValidData) {
    return (
      <div className="legacy-news-table">
        <div className="legacy-table-header">
          <h3>Noticias Filtradas</h3>
          <p>Datos incompletos</p>
        </div>
        <div style={{ height: '400px', display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center' }}>
          <i className="fas fa-exclamation-triangle" style={{ fontSize: '48px', color: '#f59e0b', marginBottom: '20px' }}></i>
          <p style={{ color: 'var(--text-secondary)', textAlign: 'center' }}>
            Los datos de noticias están incompletos.<br />
            Faltan campos obligatorios como título o identificador.
          </p>
        </div>
      </div>
    );
  }

  const newsData = data;

  // Filter data based on filters - with safe null checks
  const filteredData = newsData.filter((item) => {
    // Safe keyword filtering
    if (filters.keyword) {
      const keyword = filters.keyword.toLowerCase();
      const title = (item.title || '').toLowerCase();
      const source = (item.source || '').toLowerCase();

      if (!title.includes(keyword) && !source.includes(keyword)) {
        return false;
      }
    }

    // Safe field filtering with null checks
    if (filters.country && (item.country || '') !== filters.country) return false;
    if (filters.language && (item.language || '') !== filters.language) return false;
    if (filters.date && (item.date || '') !== filters.date) return false;
    if (filters.topic && (item.topic || '') !== filters.topic) return false;

    return true;
  });

  // Pagination
  const totalPages = Math.ceil(filteredData.length / itemsPerPage);
  const startIndex = (currentPage - 1) * itemsPerPage;
  const endIndex = startIndex + itemsPerPage;
  const currentData = filteredData.slice(startIndex, endIndex);

  const getCountryFlag = (country: string) => {
    if (!country) return '🌍';

    const flags: Record<string, string> = {
      US: '🇺🇸', USA: '🇺🇸', 'United States': '🇺🇸',
      UK: '🇬🇧', GB: '🇬🇧', 'United Kingdom': '🇬🇧',
      DE: '🇩🇪', Germany: '🇩🇪', Alemania: '🇩🇪',
      CO: '🇨🇴', Colombia: '🇨🇴',
      ES: '🇪🇸', Spain: '🇪🇸', España: '🇪🇸',
      MX: '🇲🇽', Mexico: '🇲🇽', México: '🇲🇽',
      Unknown: '🌍', unknown: '🌍',
    };
    return flags[country] || flags[country.toUpperCase()] || '🌍';
  };

  const getCountryName = (country: string) => {
    if (!country) return 'No especificado';

    const names: Record<string, string> = {
      US: 'Estados Unidos', USA: 'Estados Unidos', 'United States': 'Estados Unidos',
      UK: 'Reino Unido', GB: 'Reino Unido', 'United Kingdom': 'Reino Unido',
      DE: 'Alemania', Germany: 'Alemania',
      CO: 'Colombia', Colombia: 'Colombia',
      ES: 'España', Spain: 'España',
      MX: 'México', Mexico: 'México',
      Unknown: 'Desconocido', unknown: 'Desconocido',
    };
    return names[country] || names[country.toUpperCase()] || country;
  };

  const getLanguageName = (language: string) => {
    if (!language) return 'No especificado';

    const languages: Record<string, string> = {
      en: 'Inglés', english: 'Inglés', English: 'Inglés',
      es: 'Español', spanish: 'Español', Spanish: 'Español',
      de: 'Alemán', german: 'Alemán', German: 'Alemán',
      fr: 'Francés', french: 'Francés', French: 'Francés',
      it: 'Italiano', italian: 'Italiano', Italian: 'Italiano',
      pt: 'Portugués', portuguese: 'Portugués', Portuguese: 'Portugués',
    };
    return languages[language] || languages[language.toLowerCase()] || language;
  };

  const getTopicLabel = (topic: string) => {
    if (!topic) return 'Sin categoría';

    const topics: Record<string, string> = {
      prevention: 'Prevención', Prevención: 'Prevención',
      treatment: 'Tratamiento', Tratamiento: 'Tratamiento',
      diagnosis: 'Diagnóstico', Diagnóstico: 'Diagnóstico',
      testimonials: 'Testimonios', Testimonios: 'Testimonios',
      public_policy: 'Política Pública', 'Política Pública': 'Política Pública',
      research: 'Investigación', Investigación: 'Investigación',
      surgery: 'Cirugía', Cirugía: 'Cirugía',
      screening: 'Detección', Detección: 'Detección',
      support: 'Apoyo', Apoyo: 'Apoyo',
      genetics: 'Genética', Genética: 'Genética',
      lifestyle: 'Estilo de vida', 'Estilo de vida': 'Estilo de vida',
      policy: 'Política', Política: 'Política',
      general: 'General', General: 'General',
      awareness: 'Concienciación', Concienciación: 'Concienciación',
      nutrition: 'Nutrición', Nutrición: 'Nutrición',
      rehabilitation: 'Rehabilitación', Rehabilitación: 'Rehabilitación',
      other: 'Otros', Otros: 'Otros',
    };
    return topics[topic] || topics[topic.toLowerCase()] || topic;
  };

  const getSentimentLabel = (sentiment: string) => {
    if (!sentiment) return { label: 'Sin análisis', color: '#9ca3af', icon: 'fa-question' };

    const sentiments: Record<string, { label: string; color: string; icon: string }> = {
      positive: { label: 'Positivo', color: '#28a745', icon: 'fa-smile' },
      Positivo: { label: 'Positivo', color: '#28a745', icon: 'fa-smile' },
      negative: { label: 'Negativo', color: '#dc3545', icon: 'fa-frown' },
      Negativo: { label: 'Negativo', color: '#dc3545', icon: 'fa-frown' },
      neutral: { label: 'Neutro', color: '#6c757d', icon: 'fa-meh' },
      Neutro: { label: 'Neutro', color: '#6c757d', icon: 'fa-meh' },
    };
    return sentiments[sentiment] || sentiments[sentiment.toLowerCase()] ||
           { label: sentiment, color: '#6c757d', icon: 'fa-meh' };
  };

  // Check if we have any data after filtering
  if (filteredData.length === 0 && hasRealData) {
    return (
      <div className="legacy-news-table">
        <div className="legacy-table-header">
          <h3>Noticias Filtradas</h3>
          <p>0 resultados encontrados</p>
        </div>
        <div style={{ height: '400px', display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center' }}>
          <i className="fas fa-filter" style={{ fontSize: '48px', color: '#6b7280', marginBottom: '20px' }}></i>
          <p style={{ color: 'var(--text-secondary)', textAlign: 'center' }}>
            No se encontraron noticias que coincidan con los filtros aplicados.<br />
            Intente ajustar los criterios de búsqueda.
          </p>
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
                <tr key={item.id || `news-${Math.random()}`}>
                  <td>
                    {item.url ? (
                      <a
                        href={item.url}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="legacy-news-link"
                        title="Abrir artículo original"
                      >
                        {item.title || 'Título no disponible'}
                      </a>
                    ) : (
                      <span className="legacy-news-link" style={{ color: 'var(--text-secondary)' }}>
                        {item.title || 'Título no disponible'}
                      </span>
                    )}
                    <div className="legacy-news-source">
                      {item.source || 'Fuente no especificada'}
                    </div>
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
                  <td>
                    {item.date ? (
                      new Date(item.date).toLocaleDateString('es-ES')
                    ) : (
                      <span style={{ color: 'var(--text-secondary)', fontStyle: 'italic' }}>
                        Sin fecha
                      </span>
                    )}
                  </td>
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
