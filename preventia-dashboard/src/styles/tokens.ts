// Design tokens for dual-mode medical interface
export const designTokens = {
  // Medical color palette
  colors: {
    primary: {
      pink: '#F8BBD9',        // Breast cancer awareness
      blue: '#4A90E2',        // Medical trust
      navy: '#1e3a8a',        // UCOMPENSAR authority
    },
    professional: {
      50: '#f8fafc',
      100: '#f1f5f9',
      200: '#e2e8f0',
      300: '#cbd5e1',
      400: '#94a3b8',
      500: '#64748b',
      600: '#475569',
      700: '#334155',
      800: '#1e293b',
      900: '#0f172a'
    },
    educational: {
      50: '#fef7ff',
      100: '#fce7ff',
      200: '#f5c2ff',
      300: '#f0abfc',
      400: '#e879f9',
      500: '#a855f7',
      600: '#9333ea',
      700: '#7c3aed',
      800: '#6b21a8',
      900: '#581c87'
    },
    sentiment: {
      positive: '#d1fae5',    // Medical hope
      negative: '#fef2f2',    // Medical alert
      neutral: '#f3f4f6',     // Medical neutral
    },
    status: {
      success: '#10b981',
      warning: '#f59e0b',
      error: '#ef4444',
      info: '#3b82f6',
    }
  },

  // Typography system
  typography: {
    fontFamily: {
      medical: ['Inter', 'system-ui', 'sans-serif'],
      mono: ['Fira Code', 'monospace'],
    },
    fontSize: {
      xs: '0.75rem',    // 12px
      sm: '0.875rem',   // 14px
      base: '1rem',     // 16px
      lg: '1.125rem',   // 18px
      xl: '1.25rem',    // 20px
      '2xl': '1.5rem',  // 24px
      '3xl': '1.875rem', // 30px
      '4xl': '2.25rem', // 36px
      '5xl': '3rem',    // 48px
    },
    fontWeight: {
      normal: 400,
      medium: 500,
      semibold: 600,
      bold: 700,
      extrabold: 800,
    },
    lineHeight: {
      tight: 1.2,
      normal: 1.6,
      relaxed: 1.8,
    }
  },

  // Spacing system
  spacing: {
    0: '0',
    1: '0.25rem',   // 4px
    2: '0.5rem',    // 8px
    3: '0.75rem',   // 12px
    4: '1rem',      // 16px
    5: '1.25rem',   // 20px
    6: '1.5rem',    // 24px
    8: '2rem',      // 32px
    10: '2.5rem',   // 40px
    12: '3rem',     // 48px
    16: '4rem',     // 64px
    20: '5rem',     // 80px
    24: '6rem',     // 96px
  },

  // Border radius
  borderRadius: {
    none: '0',
    sm: '0.125rem',   // 2px
    base: '0.25rem',  // 4px
    md: '0.375rem',   // 6px
    lg: '0.5rem',     // 8px
    xl: '0.75rem',    // 12px
    '2xl': '1rem',    // 16px
    '3xl': '1.5rem',  // 24px
    full: '9999px',
  },

  // Shadows
  shadows: {
    sm: '0 1px 2px 0 rgb(0 0 0 / 0.05)',
    base: '0 1px 3px 0 rgb(0 0 0 / 0.1), 0 1px 2px -1px rgb(0 0 0 / 0.1)',
    md: '0 4px 6px -1px rgb(0 0 0 / 0.1), 0 2px 4px -2px rgb(0 0 0 / 0.1)',
    lg: '0 10px 15px -3px rgb(0 0 0 / 0.1), 0 4px 6px -4px rgb(0 0 0 / 0.1)',
    xl: '0 20px 25px -5px rgb(0 0 0 / 0.1), 0 8px 10px -6px rgb(0 0 0 / 0.1)',
  },

  // Animation and transitions
  animation: {
    duration: {
      fast: '150ms',
      normal: '300ms',
      slow: '500ms',
    },
    easing: {
      ease: 'cubic-bezier(0.4, 0, 0.2, 1)',
      easeIn: 'cubic-bezier(0.4, 0, 1, 1)',
      easeOut: 'cubic-bezier(0, 0, 0.2, 1)',
      easeInOut: 'cubic-bezier(0.4, 0, 0.2, 1)',
    }
  },

  // Medical-specific tokens
  medical: {
    // Color coding for medical data
    severity: {
      low: '#10b981',      // Green
      medium: '#f59e0b',   // Yellow
      high: '#ef4444',     // Red
      critical: '#dc2626', // Dark red
    },

    // Confidence intervals
    confidence: {
      high: '#059669',     // High confidence (green)
      medium: '#d97706',   // Medium confidence (orange)
      low: '#dc2626',      // Low confidence (red)
    },

    // Evidence quality
    evidence: {
      peer_reviewed: '#059669',
      preprint: '#d97706',
      news: '#6b7280',
      opinion: '#9ca3af',
    }
  },

  // Mode-specific variations
  modes: {
    professional: {
      cardPadding: '1.5rem',        // 24px
      borderWidth: '1px',
      borderRadius: '0.5rem',       // 8px
      shadowLevel: 'sm',
      backgroundColor: '#ffffff',
      textColor: '#1e293b',
    },
    educational: {
      cardPadding: '2rem',          // 32px
      borderWidth: '2px',
      borderRadius: '1rem',         // 16px
      shadowLevel: 'lg',
      backgroundColor: '#ffffff',
      textColor: '#6b21a8',
    }
  },

  // Breakpoints for responsive design
  breakpoints: {
    sm: '640px',
    md: '768px',
    lg: '1024px',
    xl: '1280px',
    '2xl': '1536px',
  },

  // Z-index scale
  zIndex: {
    auto: 'auto',
    0: '0',
    10: '10',
    20: '20',
    30: '30',
    40: '40',
    50: '50',
    modal: '1000',
    tooltip: '1100',
    dropdown: '1200',
    overlay: '1300',
    max: '9999',
  }
} as const;

// Type definitions for design tokens
export type DesignTokens = typeof designTokens;
export type ColorScale = keyof typeof designTokens.colors.professional;
export type FontSize = keyof typeof designTokens.typography.fontSize;
export type Spacing = keyof typeof designTokens.spacing;
export type Mode = 'professional' | 'educational';

// Utility functions for accessing tokens
export const getColorValue = (color: string): string => {
  const keys = color.split('.');
  let value: unknown = designTokens.colors;

  for (const key of keys) {
    if (typeof value === 'object' && value !== null && key in value) {
      value = (value as Record<string, unknown>)[key];
    } else {
      return color; // Return original if not found
    }
  }

  return value as string;
};

export const getModeTokens = (mode: Mode) => {
  return designTokens.modes[mode];
};

export const getSentimentColor = (sentiment: 'positive' | 'negative' | 'neutral'): string => {
  return designTokens.colors.sentiment[sentiment];
};

export const getMedicalSeverityColor = (severity: 'low' | 'medium' | 'high' | 'critical'): string => {
  return designTokens.medical.severity[severity];
};
