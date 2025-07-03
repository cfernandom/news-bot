import React from 'react';
import { Routes, Route } from 'react-router-dom';
import LegacyLayout from '../components/legacy/Layout/LegacyLayout';
import LegacyHomePage from '../pages/legacy/LegacyHomePage';
import LegacyAnalyticsPage from '../pages/legacy/LegacyAnalyticsPage';

// Placeholder components for other pages
const LegacyAboutPage = () => (
  <div className="legacy-hero">
    <h1>Sobre el Cáncer de Mama</h1>
    <p>Información educativa sobre el cáncer de mama, factores de riesgo, síntomas y tratamientos.</p>
  </div>
);

const LegacyPreventionPage = () => (
  <div className="legacy-hero">
    <h1>Prevención</h1>
    <p>Guías y recomendaciones para la prevención del cáncer de mama.</p>
  </div>
);

const LegacySelfExamPage = () => (
  <div className="legacy-hero">
    <h1>Autoexamen</h1>
    <p>Tutorial paso a paso para realizar el autoexamen de mama.</p>
  </div>
);

const LegacyInstitutionsPage = () => (
  <div className="legacy-hero">
    <h1>Instituciones</h1>
    <p>Directorio de instituciones médicas especializadas en cáncer de mama en Colombia.</p>
  </div>
);

const LegacyProjectPage = () => (
  <div className="legacy-hero">
    <h1>Proyecto</h1>
    <p>Metodología de investigación desarrollada por UCOMPENSAR.</p>
  </div>
);

const LegacyContactPage = () => (
  <div className="legacy-hero">
    <h1>Contacto</h1>
    <p>Formulario de contacto para consultas y colaboraciones.</p>
  </div>
);

// LegacyAnalyticsPage is now imported as a full component

const LegacyRoutes: React.FC = () => {
  return (
    <Routes>
      <Route path="/" element={<LegacyLayout />}>
        <Route index element={<LegacyHomePage />} />
        <Route path="about" element={<LegacyAboutPage />} />
        <Route path="prevention" element={<LegacyPreventionPage />} />
        <Route path="self-exam" element={<LegacySelfExamPage />} />
        <Route path="institutions" element={<LegacyInstitutionsPage />} />
        <Route path="project" element={<LegacyProjectPage />} />
        <Route path="contact" element={<LegacyContactPage />} />
        <Route path="noticias" element={<LegacyAnalyticsPage />} />
      </Route>
    </Routes>
  );
};

export default LegacyRoutes;
