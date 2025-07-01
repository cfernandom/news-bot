import React from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { useDualMode, useModeStyles } from '../../contexts/DualModeContext';

interface ModeToggleProps {
  className?: string;
  showLabels?: boolean;
  size?: 'sm' | 'md' | 'lg';
}

export const ModeToggle: React.FC<ModeToggleProps> = ({
  className = '',
  showLabels = true,
  size = 'md'
}) => {
  const { mode, toggleMode, isLoading } = useDualMode();
  const { modeClass } = useModeStyles();

  const sizeClasses = {
    sm: 'text-xs p-2',
    md: 'text-sm p-3',
    lg: 'text-base p-4',
  };

  const switchSizeClasses = {
    sm: 'w-12 h-6',
    md: 'w-14 h-7',
    lg: 'w-16 h-8',
  };

  const knobSizeClasses = {
    sm: 'w-4 h-4',
    md: 'w-5 h-5',
    lg: 'w-6 h-6',
  };

  if (isLoading) {
    return (
      <div className={`mode-toggle ${sizeClasses[size]} ${className}`}>
        <div className="animate-pulse bg-gray-200 rounded-full w-20 h-6"></div>
      </div>
    );
  }

  return (
    <div className={`mode-toggle ${sizeClasses[size]} ${className} ${modeClass}`}>
      {showLabels && (
        <AnimatePresence mode="wait">
          <motion.span
            key={`professional-${mode}`}
            initial={{ opacity: 0.5, scale: 0.95 }}
            animate={{
              opacity: mode === 'professional' ? 1 : 0.7,
              scale: mode === 'professional' ? 1 : 0.95,
              fontWeight: mode === 'professional' ? 600 : 400
            }}
            transition={{ duration: 0.2 }}
            className={`mode-toggle-label ${mode === 'professional' ? 'active' : ''}`}
          >
            Modo Profesional
          </motion.span>
        </AnimatePresence>
      )}

      {/* Toggle Switch */}
      <button
        onClick={toggleMode}
        className={`
          relative inline-flex items-center ${switchSizeClasses[size]}
          rounded-full border-2 transition-colors duration-300 focus:outline-none
          focus:ring-2 focus:ring-primary-blue focus:ring-offset-2
          ${mode === 'professional'
            ? 'bg-professional-200 border-professional-300'
            : 'bg-educational-500 border-educational-600'
          }
        `}
        role="switch"
        aria-checked={mode === 'educational'}
        aria-label={`Cambiar a modo ${mode === 'professional' ? 'educativo' : 'profesional'}`}
      >
        <motion.div
          className={`
            ${knobSizeClasses[size]} rounded-full shadow-lg transition-colors duration-300
            ${mode === 'professional'
              ? 'bg-professional-600'
              : 'bg-white'
            }
          `}
          animate={{
            x: mode === 'professional' ? 2 : switchSizeClasses[size] === 'w-12 h-6' ? 22 :
                switchSizeClasses[size] === 'w-14 h-7' ? 26 : 30
          }}
          transition={{
            type: "spring",
            stiffness: 500,
            damping: 30
          }}
        />
      </button>

      {showLabels && (
        <AnimatePresence mode="wait">
          <motion.span
            key={`educational-${mode}`}
            initial={{ opacity: 0.5, scale: 0.95 }}
            animate={{
              opacity: mode === 'educational' ? 1 : 0.7,
              scale: mode === 'educational' ? 1 : 0.95,
              fontWeight: mode === 'educational' ? 600 : 400
            }}
            transition={{ duration: 0.2 }}
            className={`mode-toggle-label ${mode === 'educational' ? 'active' : ''}`}
          >
            Modo Educativo
          </motion.span>
        </AnimatePresence>
      )}

      {/* Screen reader announcement */}
      <div className="sr-only" aria-live="polite">
        {mode === 'professional'
          ? 'Modo profesional activo. Interfaz optimizada para análisis médico avanzado.'
          : 'Modo educativo activo. Interfaz simplificada con explicaciones detalladas.'
        }
      </div>
    </div>
  );
};

// Compact version for header/navbar
export const CompactModeToggle: React.FC<{ className?: string }> = ({ className }) => {
  return (
    <ModeToggle
      className={className}
      showLabels={false}
      size="sm"
    />
  );
};

// Extended version with mode descriptions
export const ExtendedModeToggle: React.FC<{ className?: string }> = ({ className }) => {
  const { mode } = useDualMode();

  return (
    <div className={`space-y-3 ${className}`}>
      <ModeToggle size="lg" />

      <AnimatePresence mode="wait">
        <motion.div
          key={mode}
          initial={{ opacity: 0, y: -10 }}
          animate={{ opacity: 1, y: 0 }}
          exit={{ opacity: 0, y: 10 }}
          transition={{ duration: 0.3 }}
          className="text-center text-sm text-gray-600"
        >
          {mode === 'professional' ? (
            <div>
              <p className="font-medium text-professional-700">Modo Profesional</p>
              <p className="text-xs mt-1">
                Análisis estadístico avanzado, intervalos de confianza,
                y terminología médica especializada.
              </p>
            </div>
          ) : (
            <div>
              <p className="font-medium text-educational-700">Modo Educativo</p>
              <p className="text-xs mt-1">
                Explicaciones simplificadas, definiciones médicas,
                y visualizaciones educativas.
              </p>
            </div>
          )}
        </motion.div>
      </AnimatePresence>
    </div>
  );
};
