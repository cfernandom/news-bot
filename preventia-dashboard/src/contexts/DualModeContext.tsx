import React, { createContext, useContext, useState, useEffect, ReactNode } from 'react';
import { Mode, DualModeContextType, UserPreferences } from '../types';

// Default user preferences
const defaultPreferences: UserPreferences = {
  defaultMode: 'professional',
  language: 'es',
  accessibility: {
    highContrast: false,
    reducedMotion: false,
    screenReader: false,
  },
  professional: {
    showStatisticalDetails: true,
    showConfidenceIntervals: true,
    defaultChartType: 'detailed',
    exportFormat: 'csv',
  },
  educational: {
    showDefinitions: true,
    showExplanations: true,
    enableGuidedTour: true,
    simplifyCharts: true,
  },
};

// Create the context
const DualModeContext = createContext<DualModeContextType | undefined>(undefined);

// Context provider props
interface DualModeProviderProps {
  children: ReactNode;
  initialMode?: Mode;
}

// Context provider component
export const DualModeProvider: React.FC<DualModeProviderProps> = ({
  children,
  initialMode = 'professional'
}) => {
  const [mode, setMode] = useState<Mode>(initialMode);
  const [userPreferences, setUserPreferences] = useState<UserPreferences>(defaultPreferences);
  const [isLoading, setIsLoading] = useState(true);

  // Load preferences from localStorage on mount
  useEffect(() => {
    const loadPreferences = () => {
      try {
        // Load saved mode
        const savedMode = localStorage.getItem('preventia-mode') as Mode;
        if (savedMode && (savedMode === 'professional' || savedMode === 'educational')) {
          setMode(savedMode);
        }

        // Load saved preferences
        const savedPreferences = localStorage.getItem('preventia-preferences');
        if (savedPreferences) {
          const parsed = JSON.parse(savedPreferences);
          setUserPreferences({ ...defaultPreferences, ...parsed });
        }

        // Check for accessibility preferences from system
        const hasReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
        const hasHighContrast = window.matchMedia('(prefers-contrast: high)').matches;

        if (hasReducedMotion || hasHighContrast) {
          setUserPreferences(prev => ({
            ...prev,
            accessibility: {
              ...prev.accessibility,
              reducedMotion: hasReducedMotion,
              highContrast: hasHighContrast,
            }
          }));
        }
      } catch (error) {
        console.warn('Failed to load user preferences:', error);
      } finally {
        setIsLoading(false);
      }
    };

    // Small delay to simulate loading and avoid hydration issues
    const timeoutId = setTimeout(loadPreferences, 100);
    return () => clearTimeout(timeoutId);
  }, []);

  // Save mode to localStorage whenever it changes
  useEffect(() => {
    if (!isLoading) {
      localStorage.setItem('preventia-mode', mode);

      // Track mode usage for analytics
      if (typeof window !== 'undefined' && (window as any).gtag) {
        (window as any).gtag('event', 'mode_change', {
          mode,
          timestamp: new Date().toISOString(),
        });
      }
    }
  }, [mode, isLoading]);

  // Save preferences to localStorage whenever they change
  useEffect(() => {
    if (!isLoading) {
      localStorage.setItem('preventia-preferences', JSON.stringify(userPreferences));
    }
  }, [userPreferences, isLoading]);

  // Apply accessibility preferences to document
  useEffect(() => {
    const root = document.documentElement;

    // High contrast mode
    if (userPreferences.accessibility.highContrast) {
      root.classList.add('high-contrast');
    } else {
      root.classList.remove('high-contrast');
    }

    // Reduced motion
    if (userPreferences.accessibility.reducedMotion) {
      root.classList.add('reduce-motion');
    } else {
      root.classList.remove('reduce-motion');
    }

    // Mode-specific body classes
    root.classList.remove('mode-professional', 'mode-educational');
    root.classList.add(`mode-${mode}`);
  }, [userPreferences.accessibility, mode]);

  // Toggle between modes
  const toggleMode = () => {
    setMode(prev => prev === 'professional' ? 'educational' : 'professional');
  };

  // Update user preferences
  const updatePreferences = (newPreferences: Partial<UserPreferences>) => {
    setUserPreferences(prev => ({
      ...prev,
      ...newPreferences,
      // Handle nested objects specifically
      accessibility: newPreferences.accessibility
        ? { ...prev.accessibility, ...newPreferences.accessibility }
        : prev.accessibility,
      professional: newPreferences.professional
        ? { ...prev.professional, ...newPreferences.professional }
        : prev.professional,
      educational: newPreferences.educational
        ? { ...prev.educational, ...newPreferences.educational }
        : prev.educational,
    }));
  };

  // Context value
  const contextValue: DualModeContextType = {
    mode,
    toggleMode,
    setMode,
    userPreferences,
    updatePreferences,
    isLoading,
  };

  return (
    <DualModeContext.Provider value={contextValue}>
      {children}
    </DualModeContext.Provider>
  );
};

// Custom hook to use the dual mode context
export const useDualMode = (): DualModeContextType => {
  const context = useContext(DualModeContext);

  if (context === undefined) {
    throw new Error('useDualMode must be used within a DualModeProvider');
  }

  return context;
};

// Hook for getting mode-specific values
export const useModeValue = <T,>(professionalValue: T, educationalValue: T): T => {
  const { mode } = useDualMode();
  return mode === 'professional' ? professionalValue : educationalValue;
};

// Hook for getting mode-specific styles
export const useModeStyles = () => {
  const { mode, userPreferences } = useDualMode();

  const baseClasses = `mode-${mode}`;
  const accessibilityClasses = [
    userPreferences.accessibility.highContrast && 'high-contrast',
    userPreferences.accessibility.reducedMotion && 'reduce-motion',
  ].filter(Boolean).join(' ');

  return {
    mode,
    modeClass: baseClasses,
    accessibilityClass: accessibilityClasses,
    fullClass: [baseClasses, accessibilityClasses].filter(Boolean).join(' '),
  };
};

// Export context for testing
export { DualModeContext };
