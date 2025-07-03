import React from 'react';
import { Link } from 'react-router-dom';
import LegacyCarousel from '../../components/legacy/Common/LegacyCarousel';

const LegacyHomePage: React.FC = () => {
  const carouselSlides = [
    {
      id: 1,
      icon: 'fa-microscope',
      title: 'Investigación Avanzada',
      content: 'Utilizamos tecnología de punta para analizar patrones en noticias sobre cáncer de mama, proporcionando insights valiosos para la prevención y tratamiento.'
    },
    {
      id: 2,
      icon: 'fa-shield-heart',
      title: 'Prevención Temprana',
      content: 'La detección temprana es clave. Nuestras herramientas ayudan a identificar tendencias y factores de riesgo para mejorar las estrategias de prevención.'
    },
    {
      id: 3,
      icon: 'fa-users',
      title: 'Comunidad Unida',
      content: 'Conectamos a profesionales de la salud, investigadores y pacientes para crear una red de apoyo y conocimiento compartido.'
    },
    {
      id: 4,
      icon: 'fa-chart-line',
      title: 'Análisis Predictivo',
      content: 'Transformamos datos en conocimiento accionable para mejorar los resultados de salud y optimizar las estrategias de tratamiento.'
    }
  ];

  return (
    <div className="legacy-home-page">
      {/* Hero Section */}
      <section className="legacy-hero">
        <h1>PreventIA</h1>
        <p>
          Plataforma inteligente de análisis de noticias sobre cáncer de mama.
          Transformamos información en conocimiento para la prevención y el tratamiento.
        </p>
        <div className="legacy-hero-buttons">
          <Link to="/noticias" className="legacy-btn legacy-btn-primary">
            Ver Analytics
          </Link>
          <Link to="/about" className="legacy-btn legacy-btn-secondary">
            Sobre el Cáncer
          </Link>
        </div>
      </section>

      {/* Carousel Section */}
      <section className="legacy-carousel-section">
        <LegacyCarousel slides={carouselSlides} />
      </section>

      {/* Features Grid */}
      <section className="legacy-features">
        <h2 className="legacy-section-title">Características Principales</h2>
        <div className="legacy-cards-grid">
          <div className="legacy-info-card">
            <i className="fas fa-brain" style={{ fontSize: '32px', color: 'var(--primary-blue)', marginBottom: '15px' }}></i>
            <h3>Análisis Inteligente</h3>
            <p>
              Procesamiento avanzado de lenguaje natural para extraer insights
              significativos de miles de artículos médicos.
            </p>
          </div>

          <div className="legacy-info-card">
            <i className="fas fa-globe" style={{ fontSize: '32px', color: 'var(--primary-blue)', marginBottom: '15px' }}></i>
            <h3>Cobertura Global</h3>
            <p>
              Monitoreo de fuentes internacionales para obtener una perspectiva
              completa de los avances en cáncer de mama.
            </p>
          </div>

          <div className="legacy-info-card">
            <i className="fas fa-chart-bar" style={{ fontSize: '32px', color: 'var(--primary-blue)', marginBottom: '15px' }}></i>
            <h3>Visualización Avanzada</h3>
            <p>
              Dashboards interactivos que transforman datos complejos en
              información comprensible y accionable.
            </p>
          </div>

          <div className="legacy-info-card">
            <i className="fas fa-heartbeat" style={{ fontSize: '32px', color: 'var(--primary-blue)', marginBottom: '15px' }}></i>
            <h3>Impacto en Salud</h3>
            <p>
              Contribuimos a mejorar los resultados de salud mediante análisis
              predictivos y recomendaciones basadas en evidencia.
            </p>
          </div>
        </div>
      </section>

      {/* Call to Action */}
      <section className="legacy-cta">
        <div className="legacy-cta-content">
          <h2>¿Listo para explorar los datos?</h2>
          <p>
            Descubre patrones, tendencias y insights que pueden marcar la diferencia
            en la lucha contra el cáncer de mama.
          </p>
          <Link to="/noticias" className="legacy-btn legacy-btn-primary">
            Explorar Dashboard
          </Link>
        </div>
      </section>
    </div>
  );
};

export default LegacyHomePage;
