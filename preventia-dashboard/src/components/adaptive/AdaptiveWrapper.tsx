import React, { Suspense } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { useDualMode, useModeStyles } from '../../contexts/DualModeContext';
import { AdaptiveWrapperProps } from '../../types';

// Loading fallback component
const LoadingFallback: React.FC<{ mode: 'professional' | 'educational' }> = ({ mode }) => (
  <div className={`${mode === 'professional' ? 'loading-professional' : 'loading-educational'}
                   rounded-lg h-32 flex items-center justify-center`}>
    <div className="flex items-center space-x-2">
      <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-primary-blue"></div>
      <span className="text-sm text-gray-600">Cargando...</span>
    </div>
  </div>
);

// Main adaptive wrapper component
export const AdaptiveWrapper: React.FC<AdaptiveWrapperProps> = ({
  mode: propMode,
  professionalVariant: ProfessionalComponent,
  educationalVariant: EducationalComponent,
  fallback: FallbackComponent,
  data,
  className = '',
  children,
  ...props
}) => {
  const { mode: contextMode, userPreferences } = useDualMode();
  const { fullClass } = useModeStyles();

  // Use prop mode if provided, otherwise use context mode
  const currentMode = propMode || contextMode;

  // Determine which component to render
  const ComponentToRender = currentMode === 'professional'
    ? ProfessionalComponent
    : EducationalComponent;

  // Fallback component (defaults to loading state)
  const FallbackToRender = FallbackComponent || (() => <LoadingFallback mode={currentMode} />);

  // Animation variants for mode switching
  const variants = {
    enter: {
      opacity: 0,
      y: userPreferences.accessibility.reducedMotion ? 0 : -10,
      scale: userPreferences.accessibility.reducedMotion ? 1 : 0.95,
    },
    center: {
      opacity: 1,
      y: 0,
      scale: 1,
    },
    exit: {
      opacity: 0,
      y: userPreferences.accessibility.reducedMotion ? 0 : 10,
      scale: userPreferences.accessibility.reducedMotion ? 1 : 0.95,
    },
  };

  const transition = {
    duration: userPreferences.accessibility.reducedMotion ? 0 : 0.3,
  };

  return (
    <div className={`adaptive-wrapper ${fullClass} ${className}`} {...props}>
      <AnimatePresence mode="wait">
        <motion.div
          key={`${currentMode}-${ComponentToRender.name || 'component'}`}
          variants={variants}
          initial="enter"
          animate="center"
          exit="exit"
          transition={transition}
          className="w-full"
        >
          <Suspense fallback={<FallbackToRender />}>
            <ComponentToRender
              mode={currentMode}
              data={data}
              {...props}
            />
            {children}
          </Suspense>
        </motion.div>
      </AnimatePresence>
    </div>
  );
};

// Higher-order component for creating adaptive components
export const withAdaptiveMode = <P extends object>(
  professionalComponent: React.ComponentType<P & { mode: 'professional' }>,
  educationalComponent: React.ComponentType<P & { mode: 'educational' }>,
  fallbackComponent?: React.ComponentType<P>
) => {
  return React.forwardRef<HTMLDivElement, P & { className?: string }>((props, ref) => {
    return (
      <div ref={ref}>
        <AdaptiveWrapper
          professionalVariant={professionalComponent}
          educationalVariant={educationalComponent}
          fallback={fallbackComponent}
          {...props}
        />
      </div>
    );
  });
};

// Hook for conditional rendering based on mode
export const useAdaptiveRender = () => {
  const { mode } = useDualMode();

  const renderForMode = <T,>(
    professionalContent: T,
    educationalContent: T
  ): T => {
    return mode === 'professional' ? professionalContent : educationalContent;
  };

  const renderConditional = (
    condition: boolean,
    content: React.ReactNode
  ): React.ReactNode => {
    return condition ? content : null;
  };

  const isProfessional = mode === 'professional';
  const isEducational = mode === 'educational';

  return {
    mode,
    isProfessional,
    isEducational,
    renderForMode,
    renderConditional,
    professional: (content: React.ReactNode) => isProfessional ? content : null,
    educational: (content: React.ReactNode) => isEducational ? content : null,
  };
};

// Adaptive container for layout components
export const AdaptiveContainer: React.FC<{
  children: React.ReactNode;
  className?: string;
  maxWidth?: 'sm' | 'md' | 'lg' | 'xl' | '2xl' | 'full';
}> = ({
  children,
  className = '',
  maxWidth = 'full'
}) => {
  const { mode } = useDualMode();
  const { fullClass } = useModeStyles();

  const maxWidthClasses = {
    sm: 'max-w-sm',
    md: 'max-w-md',
    lg: 'max-w-lg',
    xl: 'max-w-xl',
    '2xl': 'max-w-2xl',
    full: 'max-w-full',
  };

  const modeSpecificClasses = mode === 'professional'
    ? 'bg-professional-50 min-h-screen'
    : 'bg-educational-50 min-h-screen';

  return (
    <div className={`
      adaptive-container medical-container
      ${maxWidthClasses[maxWidth]}
      ${modeSpecificClasses}
      ${fullClass}
      ${className}
    `}>
      {children}
    </div>
  );
};

// Adaptive section wrapper
export const AdaptiveSection: React.FC<{
  children: React.ReactNode;
  title?: string;
  subtitle?: string;
  className?: string;
}> = ({
  children,
  title,
  subtitle,
  className = ''
}) => {
  const { mode } = useDualMode();

  return (
    <section className={`medical-section ${className}`}>
      {title && (
        <div className="mb-6">
          <h2 className={`
            ${mode === 'professional'
              ? 'text-2xl font-semibold text-professional-800'
              : 'text-3xl font-bold text-educational-800'
            }
          `}>
            {title}
          </h2>
          {subtitle && (
            <p className={`
              mt-2
              ${mode === 'professional'
                ? 'text-sm text-professional-600'
                : 'text-base text-educational-600'
              }
            `}>
              {subtitle}
            </p>
          )}
        </div>
      )}
      {children}
    </section>
  );
};
