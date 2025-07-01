import React from 'react';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { ReactQueryDevtools } from '@tanstack/react-query-devtools';
import { DualModeProvider } from './contexts/DualModeContext';
import { AdaptiveContainer } from './components/adaptive/AdaptiveWrapper';
import { ModeToggle } from './components/ui/ModeToggle';
import { AdaptiveKPICard, ArticleCountCard } from './components/adaptive/AdaptiveKPICard';

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

          {/* Mode toggle */}
          <div className="flex items-center space-x-4">
            <ModeToggle />
          </div>
        </div>
      </div>
    </header>
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

      {/* KPI Cards Grid */}
      <div className="medical-grid">
        <ArticleCountCard count={106} />

        <AdaptiveKPICard
          title="Análisis Completado"
          value="100%"
          subtitle="Todos los artículos procesados"
          trend={{
            direction: 'up',
            value: 5.2,
            period: 'última semana'
          }}
          icon={({ className }) => (
            <svg className={className} fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2}
                    d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
          )}
        />

        <AdaptiveKPICard
          title="Sentimiento Promedio"
          value="Neutral"
          subtitle="Distribución: 27% Positivo, 71% Negativo, 2% Neutral"
          icon={({ className }) => (
            <svg className={className} fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2}
                    d="M7 8h10M7 12h4m1 8l-4-4H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-3l-4 4z" />
            </svg>
          )}
        />

        <AdaptiveKPICard
          title="Fuentes Activas"
          value="4"
          subtitle="WebMD, BreastCancer.org, CureToday, News-Medical"
          icon={({ className }) => (
            <svg className={className} fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2}
                    d="M19 20H5a2 2 0 01-2-2V6a2 2 0 012-2h10a2 2 0 012 2v1m2 13a2 2 0 01-2-2V7m2 13a2 2 0 002-2V9a2 2 0 00-2-2h-2m-4-3H9M7 16h6M7 8h6v4H7V8z" />
            </svg>
          )}
        />
      </div>

      {/* Status message */}
      <div className="bg-blue-50 border border-blue-200 rounded-lg p-6 text-center">
        <div className="flex items-center justify-center space-x-2 mb-2">
          <svg className="w-5 h-5 text-blue-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2}
                  d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
          <h3 className="text-lg font-semibold text-blue-900">
            Dashboard en Construcción
          </h3>
        </div>
        <p className="text-blue-700">
          Esta es la implementación base del sistema dual-mode. Los componentes de visualización
          avanzada (gráficos, mapas, tablas) se implementarán en las siguientes fases del desarrollo.
        </p>
      </div>
    </div>
  );
};

// Main App component
function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <DualModeProvider initialMode="professional">
        <div className="min-h-screen bg-gray-50">
          <AppHeader />

          <main className="py-8">
            <AdaptiveContainer maxWidth="full">
              <DashboardContent />
            </AdaptiveContainer>
          </main>
        </div>

        {/* React Query DevTools (only in development) */}
        <ReactQueryDevtools initialIsOpen={false} />
      </DualModeProvider>
    </QueryClientProvider>
  );
}

export default App;
