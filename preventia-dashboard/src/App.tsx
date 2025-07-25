import React from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { ReactQueryDevtools } from '@tanstack/react-query-devtools';
import { DualModeProvider } from './contexts/DualModeContext';
import { AdaptiveContainer } from './components/adaptive/AdaptiveWrapper';
import { ModeToggle } from './components/ui/ModeToggle';
import MedicalKPIGrid from './components/dashboard/MedicalKPIGrid';
import MedicalErrorBoundary from './components/common/ErrorBoundary';
import SentimentChart from './components/charts/SentimentChart';
import TopicsChart from './components/charts/TopicsChart';
import ArticlesTableSection from './components/sections/ArticlesTableSection';
import { useMedicalSentimentDistribution, useMedicalTopicsDistribution } from './hooks/useMedicalData';
import LegacyRoutes from './routes/LegacyRoutes';
import { AdminPage } from './pages/admin/AdminPage';

// Create a query client
const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 5 * 60 * 1000, // 5 minutes
      refetchOnWindowFocus: false,
    },
  },
});

// Header component
const AppHeader: React.FC = () => {
  return (
    <header className="bg-white shadow-sm border-b border-gray-200 sticky top-0 z-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          {/* Logo and title */}
          <div className="flex items-center space-x-4">
            <div className="flex-shrink-0">
              <h1 className="text-2xl font-bold text-academic-navy">
                PreventIA
              </h1>
            </div>
            <div className="hidden md:block">
              <p className="text-sm text-professional-600">
                Analytics Dashboard - UCOMPENSAR
              </p>
            </div>
          </div>

          {/* Navigation and Mode toggle */}
          <div className="flex items-center space-x-4">
            {/* Admin link */}
            <Link
              to="/admin"
              className="inline-flex items-center px-3 py-2 border border-transparent text-sm leading-4 font-medium rounded-md text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 transition-colors duration-200"
            >
              🛠️ Admin
            </Link>

            <ModeToggle />
          </div>
        </div>
      </div>
    </header>
  );
};

// Medical Visualizations Section
const MedicalVisualizationsSection: React.FC = () => {
  const { data: sentimentData, isLoading: sentimentLoading, isError: sentimentError } = useMedicalSentimentDistribution();
  const { data: topicsData, isLoading: topicsLoading, isError: topicsError } = useMedicalTopicsDistribution();

  if (sentimentError || topicsError) {
    return (
      <div className="bg-red-50 border border-red-200 rounded-lg p-6 text-center">
        <p className="text-red-700">Error al cargar datos de visualización</p>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h2 className="text-2xl font-bold text-gray-900">
          📊 Análisis Visual de Datos Médicos
        </h2>
        <div className="text-sm text-gray-500">
          Visualizaciones interactivas con datos reales de 106 artículos
        </div>
      </div>

      {/* Medical Charts Grid - Day 1 & Day 2 Implementation */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Sentiment Analysis Chart - DAY 1 COMPLETED */}
        <div className="lg:col-span-1">
          <SentimentChart
            data={sentimentData || []}
            loading={sentimentLoading}
            className="h-full"
          />
        </div>

        {/* Topics Distribution Chart - DAY 2 IMPLEMENTATION */}
        <div className="lg:col-span-1">
          <TopicsChart
            data={topicsData || []}
            loading={topicsLoading}
            className="h-full"
          />
        </div>
      </div>

      {/* Future Visualizations Preview */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Geographic Map Placeholder - DAY 4 */}
        <div className="lg:col-span-1 bg-white rounded-lg border shadow-sm p-6">
          <div className="text-center py-12">
            <div className="text-4xl mb-4">🗺️</div>
            <h3 className="text-lg font-semibold text-gray-700 mb-2">
              Mapa Geográfico
            </h3>
            <p className="text-gray-500 text-sm">
              Cobertura internacional - Day 4 implementation
            </p>
          </div>
        </div>

        {/* Articles Table - DAY 3 IMPLEMENTED */}
        <div className="lg:col-span-1">
          <ArticlesTableSection className="h-full" />
        </div>
      </div>
    </div>
  );
};

// Main dashboard content
const DashboardContent: React.FC = () => {
  return (
    <div className="space-y-8">
      {/* Welcome section */}
      <div className="text-center py-8">
        <h2 className="text-3xl font-bold text-gray-900 mb-4">
          PreventIA News Analytics Dashboard
        </h2>
        <p className="text-lg text-gray-600 max-w-3xl mx-auto">
          Sistema inteligente de monitoreo y análisis de noticias especializadas
          en prevención y detección temprana del cáncer de mama
        </p>
      </div>

      {/* Medical KPI Grid with Real Data */}
      <MedicalKPIGrid />

      {/* Medical Visualizations - NEW SECTION */}
      <MedicalVisualizationsSection />

      {/* Implementation status */}
      <div className="bg-green-50 border border-green-200 rounded-lg p-6 text-center">
        <div className="flex items-center justify-center space-x-2 mb-2">
          <svg className="w-5 h-5 text-green-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2}
                  d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
          <h3 className="text-lg font-semibold text-green-900">
            🚀 Week 2 Sprint - Day 2 En Progreso
          </h3>
        </div>
        <p className="text-green-700">
          ✅ SentimentChart (Day 1) + TopicsChart (Day 2) operativos con 10 categorías médicas.
          Próximo: ArticlesTable (Day 3), GeographicMap (Day 4).
        </p>
      </div>
    </div>
  );
};

// Main Dashboard App (existing functionality)
const MainDashboardApp: React.FC = () => {
  return (
    <DualModeProvider initialMode="professional">
      <div className="min-h-screen bg-gray-50">
        <AppHeader />

        <main className="py-8">
          <AdaptiveContainer maxWidth="full">
            <MedicalErrorBoundary>
              <DashboardContent />
            </MedicalErrorBoundary>
          </AdaptiveContainer>
        </main>
      </div>
    </DualModeProvider>
  );
};

// Main App component with routing
function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <MedicalErrorBoundary>
        <Router>
          <Routes>
            {/* Admin route */}
            <Route path="/admin" element={<AdminPage />} />

            {/* Main dashboard route */}
            <Route path="/dashboard" element={<MainDashboardApp />} />

            {/* Legacy prototype routes as main routes */}
            <Route path="/*" element={<LegacyRoutes />} />
          </Routes>

          {/* React Query DevTools (only in development) */}
          <ReactQueryDevtools initialIsOpen={false} />
        </Router>
      </MedicalErrorBoundary>
    </QueryClientProvider>
  );
}

export default App;
