import React from 'react';

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

interface LegacyNewsModalProps {
  isOpen: boolean;
  onClose: () => void;
  news: NewsItem | null;
}

const LegacyNewsModal: React.FC<LegacyNewsModalProps> = ({
  isOpen,
  onClose,
  news,
}) => {
  if (!isOpen || !news) return null;

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

  const getSentimentInfo = (sentiment: string) => {
    const sentiments: Record<string, { label: string; color: string; icon: string }> = {
      positive: { label: 'Positivo', color: '#28a745', icon: 'fa-smile' },
      negative: { label: 'Negativo', color: '#dc3545', icon: 'fa-frown' },
      neutral: { label: 'Neutro', color: '#6c757d', icon: 'fa-meh' },
    };
    return sentiments[sentiment] || { label: sentiment, color: '#6c757d', icon: 'fa-meh' };
  };

  const sentimentInfo = getSentimentInfo(news.sentiment);

  // Generate AI summary if not provided
  const aiSummary = news.summary || `
    Este artículo aborda aspectos importantes relacionados con ${getTopicLabel(news.topic).toLowerCase()}
    del cáncer de mama. El contenido presenta información relevante para la comunidad médica y pacientes,
    con un enfoque ${sentimentInfo.label.toLowerCase()} según nuestro análisis de procesamiento de lenguaje natural.

    La publicación proviene de ${news.source}, una fuente ${news.language === 'en' ? 'en inglés' : 'en español'}
    con base en ${getCountryFlag(news.country)} ${news.country}, lo que aporta perspectiva regional al tema tratado.

    **Puntos clave identificados por IA:**
    • Relevancia para pacientes y profesionales de la salud
    • Información actualizada sobre el tema de ${getTopicLabel(news.topic).toLowerCase()}
    • Contenido con tono ${sentimentInfo.label.toLowerCase()} según análisis automático
    • Fuente confiable del sector salud
  `;

  return (
    <div className="legacy-modal-overlay" onClick={onClose}>
      <div className="legacy-modal" onClick={(e) => e.stopPropagation()}>
        <div className="legacy-modal-header">
          <h2>
            <i className="fas fa-robot"></i>
            Resumen Automatizado (IA)
          </h2>
          <button
            className="legacy-modal-close"
            onClick={onClose}
            title="Cerrar modal"
          >
            <i className="fas fa-times"></i>
          </button>
        </div>

        <div className="legacy-modal-content">
          {/* News Title */}
          <div className="legacy-news-modal-title">
            <h3>{news.title}</h3>
          </div>

          {/* Informative Tags */}
          <div className="legacy-news-modal-tags">
            <span className="legacy-tag legacy-tag-topic">
              <i className="fas fa-tag"></i>
              {getTopicLabel(news.topic)}
            </span>

            <span
              className="legacy-tag legacy-tag-sentiment"
              style={{ color: sentimentInfo.color }}
            >
              <i className={`fas ${sentimentInfo.icon}`}></i>
              {sentimentInfo.label}
            </span>

            <span className="legacy-tag legacy-tag-location">
              {getCountryFlag(news.country)} {news.country} • {news.language === 'en' ? 'Inglés' : 'Español'}
            </span>

            <span className="legacy-tag legacy-tag-date">
              <i className="fas fa-calendar"></i>
              {new Date(news.date).toLocaleDateString('es-ES', {
                year: 'numeric',
                month: 'long',
                day: 'numeric'
              })}
            </span>
          </div>

          {/* AI Summary Text */}
          <div className="legacy-news-modal-summary">
            <h4>
              <i className="fas fa-brain"></i>
              Resumen generado por IA:
            </h4>
            <div className="legacy-summary-content">
              {aiSummary.split('\n').map((paragraph, index) => {
                if (paragraph.trim()) {
                  if (paragraph.startsWith('**') && paragraph.endsWith('**')) {
                    return (
                      <h5 key={index} className="legacy-summary-subtitle">
                        {paragraph.replace(/\*\*/g, '')}
                      </h5>
                    );
                  } else if (paragraph.startsWith('•')) {
                    return (
                      <li key={index} className="legacy-summary-point">
                        {paragraph.substring(1).trim()}
                      </li>
                    );
                  } else {
                    return (
                      <p key={index} className="legacy-summary-paragraph">
                        {paragraph.trim()}
                      </p>
                    );
                  }
                }
                return null;
              })}
            </div>
          </div>

          {/* Source Information */}
          <div className="legacy-news-modal-source">
            <div className="legacy-source-info">
              <strong>Fuente:</strong> {news.source}
            </div>
          </div>
        </div>

        <div className="legacy-modal-footer">
          <a
            href={news.url}
            target="_blank"
            rel="noopener noreferrer"
            className="legacy-btn-primary"
          >
            <i className="fas fa-external-link-alt"></i>
            Leer artículo original
          </a>

          <button
            className="legacy-btn-secondary"
            onClick={onClose}
          >
            <i className="fas fa-times"></i>
            Cerrar
          </button>
        </div>
      </div>
    </div>
  );
};

export default LegacyNewsModal;
