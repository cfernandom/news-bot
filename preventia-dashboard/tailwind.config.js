/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        // Medical color palette for dual-mode
        'primary-pink': '#F8BBD9',      // Breast cancer awareness
        'primary-blue': '#4A90E2',      // Medical trust
        'academic-navy': '#1e3a8a',     // UCOMPENSAR authority
        'professional-gray': '#6b7280', // Professional text

        // Sentiment analysis colors
        'positive-sentiment': '#d1fae5', // Medical hope
        'negative-sentiment': '#fef2f2', // Medical alert
        'neutral-sentiment': '#f3f4f6',  // Medical neutral

        // Mode-specific colors
        'professional': {
          50: '#f8fafc',
          100: '#f1f5f9',
          500: '#64748b',
          600: '#475569',
          700: '#334155',
          800: '#1e293b',
          900: '#0f172a'
        },
        'educational': {
          50: '#fef7ff',
          100: '#fce7ff',
          500: '#a855f7',
          600: '#9333ea',
          700: '#7c3aed',
          800: '#6b21a8',
          900: '#581c87'
        }
      },
      fontFamily: {
        'medical': ['Inter', 'system-ui', 'sans-serif'],
      },
      animation: {
        'mode-switch': 'mode-switch 0.3s ease-in-out',
        'fade-in': 'fade-in 0.2s ease-out',
      },
      keyframes: {
        'mode-switch': {
          '0%': { opacity: '0', transform: 'translateY(-10px)' },
          '100%': { opacity: '1', transform: 'translateY(0)' },
        },
        'fade-in': {
          '0%': { opacity: '0' },
          '100%': { opacity: '1' },
        }
      }
    },
  },
  plugins: [
    require('@tailwindcss/forms'),
    require('@tailwindcss/typography'),
  ],
}
