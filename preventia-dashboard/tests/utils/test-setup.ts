// Test setup configuration for PreventIA Dashboard
import { expect, afterEach, vi } from 'vitest';
import { cleanup } from '@testing-library/react';
import * as matchers from '@testing-library/jest-dom/matchers';

// Extend Vitest's expect with Testing Library matchers
expect.extend(matchers);

// Cleanup after each test
afterEach(() => {
  cleanup();
});

// Mock window.matchMedia (required for responsive components)
Object.defineProperty(window, 'matchMedia', {
  writable: true,
  value: (query: string) => ({
    matches: false,
    media: query,
    onchange: null,
    addListener: () => {},
    removeListener: () => {},
    addEventListener: () => {},
    removeEventListener: () => {},
    dispatchEvent: () => {},
  }),
});

// Mock ResizeObserver (required for chart components)
global.ResizeObserver = class ResizeObserver {
  observe() {}
  unobserve() {}
  disconnect() {}
};

// Mock IntersectionObserver (required for lazy loading)
global.IntersectionObserver = class IntersectionObserver {
  constructor() {}
  observe() {}
  unobserve() {}
  disconnect() {}
};

// Mock Framer Motion for testing
vi.mock('framer-motion', () => ({
  motion: {
    div: 'div',
    span: 'span',
    h1: 'h1',
    h2: 'h2',
    h3: 'h3',
    p: 'p',
    button: 'button',
  },
  AnimatePresence: ({ children }: { children: React.ReactNode }) => children,
}));

// Medical testing utilities
export const MOCK_MEDICAL_DATA = {
  analytics: {
    totalArticles: 106,
    totalSources: 4,
    languageDistribution: {
      español: 0,
      inglés: 106,
    },
    sentimentDistribution: {
      positive: 24,
      negative: 79,
      neutral: 3,
    },
    topCountry: 'Other/Unknown',
    topSource: 'webmd.com',
    lastUpdated: '2025-01-01T00:00:00Z',
  },
  sentimentData: [
    {
      sentiment: 'negative',
      value: 79,
      percentage: 74,
      color: '#ef4444',
    },
    {
      sentiment: 'positive',
      value: 24,
      percentage: 23,
      color: '#10b981',
    },
    {
      sentiment: 'neutral',
      value: 3,
      percentage: 3,
      color: '#6b7280',
    },
  ],
  articles: {
    articles: [
      {
        id: 1,
        title: 'Test Medical Article',
        url: 'https://example.com/article-1',
        summary: 'Test summary for medical article',
        content: 'Test content with medical information',
        publishedAt: '2025-01-01T00:00:00Z',
        source: 'webmd.com',
        language: 'english',
        country: 'Other/Unknown',
        sentimentLabel: 'negative',
        sentimentScore: -0.5,
        sentimentConfidence: 0.8,
        topicCategory: 'treatment',
        keywords: ['cancer', 'treatment', 'breast'],
        relevanceScore: 0.9,
        medicalTermsCount: 15,
        createdAt: '2025-01-01T00:00:00Z',
        updatedAt: '2025-01-01T00:00:00Z',
      },
    ],
    total: 1,
    page: 1,
    limit: 10,
    hasNext: false,
    hasPrevious: false,
  },
};

// Medical error for testing
export const MOCK_MEDICAL_ERROR = {
  code: 'MEDICAL_API_ERROR',
  message: 'Error en conexión con datos médicos',
  details: { status: 500 },
  timestamp: '2025-01-01T00:00:00Z',
};

declare global {
  var vi: any;
}
