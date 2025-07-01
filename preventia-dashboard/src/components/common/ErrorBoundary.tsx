// Medical Error Boundary for Dashboard
// Handles medical data errors gracefully according to plan specifications

import { Component, ErrorInfo, ReactNode } from 'react';
import { ExclamationTriangleIcon, ArrowPathIcon } from '@heroicons/react/24/outline';

interface Props {
  children: ReactNode;
  fallback?: ReactNode;
  onError?: (error: Error, errorInfo: ErrorInfo) => void;
}

interface State {
  hasError: boolean;
  error: Error | null;
  errorInfo: ErrorInfo | null;
}

export class MedicalErrorBoundary extends Component<Props, State> {
  public state: State = {
    hasError: false,
    error: null,
    errorInfo: null,
  };

  public static getDerivedStateFromError(error: Error): State {
    // Update state so the next render will show the fallback UI
    return {
      hasError: true,
      error,
      errorInfo: null,
    };
  }

  public componentDidCatch(error: Error, errorInfo: ErrorInfo) {
    console.error('Medical Dashboard Error:', error, errorInfo);

    this.setState({
      error,
      errorInfo,
    });

    // Call optional error handler
    if (this.props.onError) {
      this.props.onError(error, errorInfo);
    }

    // Log to medical monitoring (production)
    if (import.meta.env.MODE === 'production') {
      // Send to monitoring service
      this.logMedicalError(error, errorInfo);
    }
  }

  private logMedicalError(error: Error, errorInfo: ErrorInfo) {
    // Medical error logging for production monitoring
    const medicalErrorData = {
      timestamp: new Date().toISOString(),
      error: {
        name: error.name,
        message: error.message,
        stack: error.stack,
      },
      errorInfo: {
        componentStack: errorInfo.componentStack,
      },
      context: 'medical-dashboard',
      institution: 'UCOMPENSAR',
      severity: 'high',
    };

    // Send to monitoring service (implement based on chosen service)
    console.error('Medical Error Logged:', medicalErrorData);
  }

  private handleRetry = () => {
    this.setState({
      hasError: false,
      error: null,
      errorInfo: null,
    });
  };

  public render() {
    if (this.state.hasError) {
      // Custom fallback UI
      if (this.props.fallback) {
        return this.props.fallback;
      }

      // Default medical error UI
      return (
        <div className="min-h-[400px] flex items-center justify-center">
          <div className="max-w-md w-full bg-white rounded-lg shadow-lg p-6 text-center">
            {/* Error icon */}
            <div className="mx-auto flex items-center justify-center h-12 w-12 rounded-full bg-red-100 mb-4">
              <ExclamationTriangleIcon className="h-6 w-6 text-red-600" />
            </div>

            {/* Error message */}
            <h3 className="text-lg font-medium text-gray-900 mb-2">
              Error en Dashboard Médico
            </h3>
            <p className="text-sm text-gray-600 mb-4">
              Se produjo un error inesperado al cargar los datos médicos.
              Por favor, intente nuevamente.
            </p>

            {/* Error details (development only) */}
            {import.meta.env.DEV && this.state.error && (
              <details className="text-left mb-4">
                <summary className="text-xs text-gray-500 cursor-pointer">
                  Detalles técnicos
                </summary>
                <pre className="text-xs text-red-600 mt-2 p-2 bg-red-50 rounded overflow-auto">
                  {this.state.error.message}
                  {this.state.error.stack && '\n\n' + this.state.error.stack}
                </pre>
              </details>
            )}

            {/* Actions */}
            <div className="flex space-x-3 justify-center">
              <button
                onClick={this.handleRetry}
                className="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-primary-blue hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
              >
                <ArrowPathIcon className="w-4 h-4 mr-2" />
                Reintentar
              </button>

              <button
                onClick={() => window.location.reload()}
                className="inline-flex items-center px-4 py-2 border border-gray-300 text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-blue"
              >
                Recargar página
              </button>
            </div>

            {/* Medical disclaimer */}
            <div className="mt-6 p-3 bg-blue-50 rounded-md">
              <p className="text-xs text-blue-700">
                <strong>UCOMPENSAR:</strong> Si el problema persiste,
                contacte al equipo técnico para garantizar la continuidad
                del análisis médico.
              </p>
            </div>
          </div>
        </div>
      );
    }

    return this.props.children;
  }
}

// Hook for functional components to handle medical errors
export const useMedicalErrorHandler = () => {
  const handleMedicalError = (error: Error, context?: string) => {
    console.error(`Medical Error in ${context || 'component'}:`, error);

    // You can extend this to send to error reporting service
    if (import.meta.env.MODE === 'production') {
      // Send to monitoring
    }
  };

  return { handleMedicalError };
};

export default MedicalErrorBoundary;
