import React from 'react';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { ReactQueryDevtools } from '@tanstack/react-query-devtools';
import { DualModeProvider } from './contexts/DualModeContext';
import { AdaptiveContainer } from './components/adaptive/AdaptiveWrapper';
import { ModeToggle } from './components/ui/ModeToggle';
import MedicalKPIGrid from './components/dashboard/MedicalKPIGrid';
import MedicalErrorBoundary from './components/common/ErrorBoundary';

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

      {/* Medical KPI Grid with Real Data */}
      <MedicalKPIGrid />

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
      <MedicalErrorBoundary>
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

          {/* React Query DevTools (only in development) */}
          <ReactQueryDevtools initialIsOpen={false} />
        </DualModeProvider>
      </MedicalErrorBoundary>
    </QueryClientProvider>
  );
}

export default App;
