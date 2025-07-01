# FASE 4: React Dashboard Implementation Plan

**Fecha**: 2025-07-01
**Versión**: 1.0
**Autor**: Cristhian Fernando Moreno Manrique
**Estado**: 📋 Planificado - Listo para ejecución

---

## 🎯 **Executive Summary**

Plan detallado para implementar el dashboard React de PreventIA News Analytics, basado en el prototipo HTML funcional y la estrategia UX/UI médica documentada. La implementación aprovecha los 20+ endpoints FastAPI existentes y el design system médico definido.

**Objetivo**: Migrar dashboard médico HTML a React professional con performance < 3s y accessibility WCAG AA.

**Base técnica**: 106 artículos procesados, sentiment analysis 100%, FastAPI operativo, design system médico definido.

---

## 📊 **Current State Assessment**

### **Assets Disponibles**
- ✅ **Prototipo HTML funcional** - `docs/assets/prototypes/dashboard_v0.1.html`
- ✅ **20+ FastAPI endpoints** operativos con performance < 5s
- ✅ **106 artículos analizados** con sentiment + topic classification
- ✅ **Design system médico** completo documentado
- ✅ **UX/UI strategy** médica definida para stakeholders UCOMPENSAR
- ✅ **Legal compliance** framework implementado

### **API Endpoints Ready para Integration**
```typescript
// Endpoints mapeados del prototipo
const EndpointsMapping = {
  // KPI Cards
  '/api/analytics/summary': 'Dashboard overview metrics',
  '/api/analytics/article-count': 'Total articles (106)',
  '/api/analytics/language-distribution': 'Español/Inglés breakdown',
  '/api/analytics/country-distribution': 'Geographic coverage',
  '/api/analytics/top-sources': 'Most active sources',

  // Visualizations
  '/api/analytics/sentiment-distribution': 'Pie chart sentiment',
  '/api/analytics/sentiment-trends': 'Weekly sentiment evolution',
  '/api/analytics/topics-by-language': 'Grouped bar chart topics',
  '/api/analytics/geographic-distribution': 'Map data with coordinates',

  // Articles Management
  '/api/articles/search': 'Filtered articles table',
  '/api/articles/{id}': 'Individual article details',
  '/api/articles/export': 'Academic export functionality'
};
```

### **Prototipo Components Identificados**
```typescript
// Componentes extraídos del HTML prototype
const PrototypeComponents = {
  layout: ['Header', 'Navigation', 'Footer'],

  kpis: [
    'ArticleCountCard (106)',
    'LanguageDistributionCard (64% EN / 36% ES)',
    'TopCountryCard (Estados Unidos)',
    'TopSourceCard (WebMD)'
  ],

  visualizations: [
    'SentimentPieChart (71% Negative, 27% Positive, 2% Neutral)',
    'WeeklyTrendsLineChart (sentiment evolution)',
    'TopicsByLanguageBarChart (7 medical categories)',
    'GeographicMap (4 countries with Leaflet)',
    'DailyNewsBarChart (articles by day of week)'
  ],

  dataManagement: [
    'FilterPanel (country, language, date, topic)',
    'ArticlesTable (paginated with sorting)',
    'ArticleModal (detailed view)',
    'ExportButtons (PDF, Excel simulation)'
  ],

  medical: [
    'SentimentBadges (color-coded medical)',
    'TopicBadges (7 medical categories)',
    'SourceCredibilityIndicators',
    'MedicalDisclaimer components'
  ]
};
```

---

## 🏗️ **Technical Architecture**

### **Frontend Stack definido**
```json
{
  "framework": "React 18 + TypeScript",
  "stateManagement": "TanStack Query v5 (React Query)",
  "styling": "Tailwind CSS v3 + Medical Design System",
  "routing": "React Router v6",
  "charts": "Recharts v2 (medical-grade)",
  "maps": "React-Leaflet v4",
  "forms": "React Hook Form v7",
  "icons": "Lucide React + Font Awesome Medical",
  "build": "Vite v5",
  "testing": "Vitest + React Testing Library",
  "accessibility": "react-aria + axe-core"
}
```

### **Project Structure**
```
frontend/
├── public/
│   ├── index.html
│   └── medical-icons/
├── src/
│   ├── components/
│   │   ├── layout/
│   │   │   ├── Header.tsx
│   │   │   ├── Navigation.tsx
│   │   │   └── Footer.tsx
│   │   ├── dashboard/
│   │   │   ├── KPICard.tsx
│   │   │   ├── KPIGrid.tsx
│   │   │   ├── SentimentChart.tsx
│   │   │   ├── GeographicMap.tsx
│   │   │   ├── TopicsChart.tsx
│   │   │   └── TrendsChart.tsx
│   │   ├── articles/
│   │   │   ├── ArticlesTable.tsx
│   │   │   ├── ArticleModal.tsx
│   │   │   ├── FilterPanel.tsx
│   │   │   └── ExportButton.tsx
│   │   ├── medical/
│   │   │   ├── MedicalBadge.tsx
│   │   │   ├── SentimentBadge.tsx
│   │   │   ├── TopicBadge.tsx
│   │   │   └── SourceCredibility.tsx
│   │   └── common/
│   │       ├── LoadingSpinner.tsx
│   │       ├── ErrorBoundary.tsx
│   │       ├── Toast.tsx
│   │       └── Modal.tsx
│   ├── hooks/
│   │   ├── useApi.ts
│   │   ├── useMedicalFilters.ts
│   │   ├── usePerformanceTracking.ts
│   │   └── useAccessibility.ts
│   ├── services/
│   │   ├── api.ts
│   │   ├── analytics.ts
│   │   ├── articles.ts
│   │   └── export.ts
│   ├── types/
│   │   ├── medical.ts
│   │   ├── analytics.ts
│   │   ├── articles.ts
│   │   └── api.ts
│   ├── utils/
│   │   ├── medical-formatting.ts
│   │   ├── date-utils.ts
│   │   ├── export-utils.ts
│   │   └── accessibility.ts
│   ├── styles/
│   │   ├── globals.css
│   │   ├── medical-components.css
│   │   └── accessibility.css
│   └── App.tsx
├── package.json
├── tailwind.config.js (medical theme)
├── vite.config.ts
└── tsconfig.json
```

---

## 📅 **Implementation Timeline**

### **Week 1: Foundation & Core (Days 1-7)**

#### **Day 1-2: Project Setup & Medical Design System**
```bash
# Setup Commands
npm create vite@latest preventia-dashboard --template react-ts
cd preventia-dashboard
npm install

# Medical Dependencies
npm install @tanstack/react-query @tanstack/react-query-devtools
npm install react-router-dom react-hook-form
npm install tailwindcss @tailwindcss/forms @tailwindcss/typography
npm install recharts react-leaflet leaflet
npm install lucide-react @heroicons/react
npm install axios clsx tailwind-merge
npm install @testing-library/react @testing-library/jest-dom vitest

# Medical Accessibility
npm install react-aria @axe-core/react
npm install @types/leaflet
```

**Deliverables Day 1-2:**
- ✅ Project initialized with medical stack
- ✅ Tailwind medical theme configured
- ✅ Medical design system tokens implemented
- ✅ Basic folder structure created
- ✅ TypeScript medical types defined

#### **Day 3-4: Core Medical Components**
**Priority: KPI Cards + Medical Layout**

```typescript
// KPICard.tsx - Core medical metric display
interface KPICardProps {
  title: string;
  value: number | string;
  subtitle?: string;
  trend?: {
    direction: 'up' | 'down' | 'stable';
    percentage: number;
    timeframe: string;
  };
  icon: string;
  loading?: boolean;
  onClick?: () => void;
}

// MedicalHeader.tsx - UCOMPENSAR branded navigation
interface MedicalHeaderProps {
  currentUser?: User;
  notifications?: Notification[];
  onNavigate: (route: string) => void;
}

// MedicalLayout.tsx - Main dashboard layout
interface MedicalLayoutProps {
  children: React.ReactNode;
  sidebar?: React.ReactNode;
  filters?: React.ReactNode;
}
```

**Deliverables Day 3-4:**
- ✅ KPICard component with medical styling
- ✅ Medical header with UCOMPENSAR branding
- ✅ Basic layout with responsive medical design
- ✅ Loading states and error boundaries
- ✅ Medical accessibility features implemented

#### **Day 5-6: API Integration Foundation**
**Priority: Connect to FastAPI endpoints**

```typescript
// api.ts - Medical API client
class MedicalApiClient {
  private baseURL = 'http://localhost:8000/api';

  async getAnalyticsSummary(): Promise<AnalyticsSummary> {
    // Connect to /api/analytics/summary
  }

  async getSentimentDistribution(filters?: MedicalFilters): Promise<SentimentData> {
    // Connect to /api/analytics/sentiment-distribution
  }

  async getArticles(filters: ArticleFilters): Promise<PaginatedArticles> {
    // Connect to /api/articles/search
  }
}

// useMedicalData.ts - TanStack Query hooks
export const useMedicalAnalytics = () => {
  return useQuery({
    queryKey: ['medical-analytics'],
    queryFn: () => medicalApi.getAnalyticsSummary(),
    staleTime: 5 * 60 * 1000, // 5 min cache for medical data
  });
};
```

**Deliverables Day 5-6:**
- ✅ API client with all FastAPI endpoints
- ✅ TanStack Query setup with medical caching
- ✅ Error handling for medical data
- ✅ Loading states for clinical contexts
- ✅ Real data flowing to KPI cards

#### **Day 7: Medical Articles Table**
**Priority: Core data display functionality**

```typescript
// ArticlesTable.tsx - Medical literature table
interface ArticlesTableProps {
  articles: MedicalArticle[];
  filters: MedicalFilters;
  onFilterChange: (filters: MedicalFilters) => void;
  onArticleSelect: (article: MedicalArticle) => void;
  loading?: boolean;
}

// Medical badges integration
const SentimentBadge = ({ sentiment }: { sentiment: SentimentType }) => (
  <span className={`medical-badge badge-sentiment-${sentiment}`}>
    {sentiment === 'positive' && '✓ Positivo'}
    {sentiment === 'negative' && '⚠ Negativo'}
    {sentiment === 'neutral' && '— Neutro'}
  </span>
);
```

**Deliverables Day 7:**
- ✅ Articles table with medical styling
- ✅ Pagination and sorting functionality
- ✅ Medical sentiment and topic badges
- ✅ Filter integration working
- ✅ Basic export functionality

**Week 1 Success Criteria:**
- [ ] Dashboard loads with real KPI data < 2s
- [ ] Articles table displays 106 articles correctly
- [ ] Medical styling consistent with design system
- [ ] Basic filtering functionality working
- [ ] Mobile responsive medical layout

---

### **Week 2: Advanced Visualizations (Days 8-14)**

#### **Day 8-9: Medical Sentiment Visualization**
**Priority: Sentiment analysis charts**

```typescript
// SentimentChart.tsx - Medical pie chart
import { PieChart, Pie, Cell, ResponsiveContainer, Tooltip, Legend } from 'recharts';

const MedicalSentimentChart = ({ data }: { data: SentimentData[] }) => {
  const MEDICAL_COLORS = {
    positive: '#10b981', // Medical green
    negative: '#ef4444', // Medical red
    neutral: '#6b7280'   // Medical gray
  };

  return (
    <div className="medical-chart-container">
      <h3 className="medical-chart-title">Análisis de Sentimiento Médico</h3>
      <ResponsiveContainer width="100%" height={300}>
        <PieChart>
          <Pie
            data={data}
            cx="50%"
            cy="50%"
            innerRadius={60}
            outerRadius={120}
            paddingAngle={2}
            dataKey="value"
          >
            {data.map((entry, index) => (
              <Cell key={`cell-${index}`} fill={MEDICAL_COLORS[entry.sentiment]} />
            ))}
          </Pie>
          <Tooltip formatter={(value) => [`${value}%`, 'Porcentaje']} />
          <Legend />
        </PieChart>
      </ResponsiveContainer>
    </div>
  );
};
```

**Deliverables Day 8-9:**
- ✅ Sentiment pie chart with medical colors
- ✅ Responsive chart container
- ✅ Medical tooltips and legends
- ✅ Accessibility support for charts
- ✅ Real sentiment data integration

#### **Day 10-11: Medical Geographic Visualization**
**Priority: Geographic coverage map**

```typescript
// GeographicMap.tsx - Medical coverage map
import { MapContainer, TileLayer, CircleMarker, Popup } from 'react-leaflet';

const MedicalGeographicMap = ({ data }: { data: GeographicData[] }) => {
  return (
    <div className="medical-map-container">
      <h3 className="medical-chart-title">Cobertura Geográfica Médica</h3>
      <MapContainer
        center={[20, -100]} // Centro en América
        zoom={3}
        style={{ height: '400px', width: '100%' }}
      >
        <TileLayer
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
          attribution="Medical data visualization"
        />
        {data.map((country) => (
          <CircleMarker
            key={country.code}
            center={[country.lat, country.lon]}
            radius={Math.sqrt(country.articleCount) * 2}
            fillColor={getSentimentColor(country.predominantSentiment)}
            color="#fff"
            weight={2}
            opacity={1}
            fillOpacity={0.7}
          >
            <Popup>
              <div className="medical-map-popup">
                <h4 className="medical-map-popup-title">{country.name}</h4>
                <p>Artículos analizados: {country.articleCount}</p>
                <p>Sentimiento predominante: {country.predominantSentiment}</p>
                <p>Idioma principal: {country.primaryLanguage}</p>
              </div>
            </Popup>
          </CircleMarker>
        ))}
      </MapContainer>
    </div>
  );
};
```

**Deliverables Day 10-11:**
- ✅ Interactive medical map with Leaflet
- ✅ Circle markers scaled by article count
- ✅ Medical popups with country details
- ✅ Sentiment color-coding for regions
- ✅ Mobile-friendly map interactions

#### **Day 12-13: Medical Topics & Trends**
**Priority: Topic analysis and temporal trends**

```typescript
// TopicsChart.tsx - Medical topics by language
const MedicalTopicsChart = ({ data }: { data: TopicData[] }) => {
  return (
    <div className="medical-chart-container">
      <h3 className="medical-chart-title">Temas Médicos por Idioma</h3>
      <ResponsiveContainer width="100%" height={350}>
        <BarChart data={data} margin={{ top: 20, right: 30, left: 20, bottom: 5 }}>
          <CartesianGrid strokeDasharray="3 3" stroke="#f3f4f6" />
          <XAxis dataKey="topic" tick={{ fontSize: 12 }} />
          <YAxis />
          <Tooltip
            labelFormatter={(topic) => `Tema médico: ${topic}`}
            formatter={(value, name) => [`${value} artículos`, name]}
          />
          <Legend />
          <Bar dataKey="español" fill="#F8BBD9" name="Español" />
          <Bar dataKey="inglés" fill="#4A90E2" name="Inglés" />
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
};

// TrendsChart.tsx - Medical sentiment evolution
const MedicalTrendsChart = ({ data }: { data: TrendData[] }) => {
  return (
    <div className="medical-chart-container">
      <h3 className="medical-chart-title">Evolución del Sentimiento Médico</h3>
      <ResponsiveContainer width="100%" height={300}>
        <LineChart data={data}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="week" />
          <YAxis domain={[0, 1]} tickFormatter={(value) => `${(value * 100).toFixed(0)}%`} />
          <Tooltip
            labelFormatter={(week) => `Semana: ${week}`}
            formatter={(value) => [`${(value * 100).toFixed(1)}%`, 'Porcentaje']}
          />
          <Legend />
          <Line type="monotone" dataKey="positive" stroke="#10b981" strokeWidth={3} name="Positivo" />
          <Line type="monotone" dataKey="negative" stroke="#ef4444" strokeWidth={3} name="Negativo" />
          <Line type="monotone" dataKey="neutral" stroke="#6b7280" strokeWidth={2} name="Neutro" />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
};
```

**Deliverables Day 12-13:**
- ✅ Topics bar chart with medical categories
- ✅ Temporal trends line chart
- ✅ Medical color coding for all charts
- ✅ Responsive chart behavior
- ✅ Chart accessibility for screen readers

#### **Day 14: Advanced Filtering & Integration**
**Priority: Complete dashboard integration**

```typescript
// FilterPanel.tsx - Medical advanced filtering
const MedicalFilterPanel = ({ filters, onFilterChange }: FilterPanelProps) => {
  return (
    <div className="medical-filter-panel">
      <h3 className="clinical-subtitle">Filtros de Análisis Médico</h3>

      <div className="medical-filter-grid">
        <MedicalSelect
          label="País"
          value={filters.country}
          onChange={(country) => onFilterChange({ ...filters, country })}
          options={COUNTRY_OPTIONS}
        />

        <MedicalSelect
          label="Idioma"
          value={filters.language}
          onChange={(language) => onFilterChange({ ...filters, language })}
          options={LANGUAGE_OPTIONS}
        />

        <MedicalDateRange
          label="Rango de Fechas"
          startDate={filters.startDate}
          endDate={filters.endDate}
          onChange={(dateRange) => onFilterChange({ ...filters, ...dateRange })}
        />

        <MedicalSelect
          label="Tema Médico"
          value={filters.topic}
          onChange={(topic) => onFilterChange({ ...filters, topic })}
          options={MEDICAL_TOPIC_OPTIONS}
        />
      </div>

      <div className="medical-filter-actions">
        <button className="btn-medical-primary" onClick={applyFilters}>
          Aplicar Filtros
        </button>
        <button className="btn-medical-secondary" onClick={clearFilters}>
          Limpiar Filtros
        </button>
      </div>
    </div>
  );
};
```

**Deliverables Day 14:**
- ✅ Advanced medical filtering system
- ✅ Filter state synchronization across components
- ✅ URL state management for filters
- ✅ Filter presets for common medical scenarios
- ✅ Clear and apply filter functionality

**Week 2 Success Criteria:**
- [ ] All 5 visualizations rendering with real data
- [ ] Charts responsive and accessible
- [ ] Medical color scheme consistently applied
- [ ] Advanced filtering working across all components
- [ ] Performance maintained < 3s load time

---

### **Week 3: Advanced Features & Polish (Days 15-21)**

#### **Day 15-16: Article Details & Export**
**Priority: Medical article deep-dive functionality**

```typescript
// ArticleModal.tsx - Detailed medical article view
const MedicalArticleModal = ({ article, isOpen, onClose }: ArticleModalProps) => {
  return (
    <Modal isOpen={isOpen} onClose={onClose} className="medical-modal">
      <div className="medical-modal-header">
        <h2 className="medical-title">{article.title}</h2>
        <button onClick={onClose} className="medical-modal-close">
          <X size={24} />
        </button>
      </div>

      <div className="medical-modal-content">
        <div className="medical-article-metadata">
          <SentimentBadge sentiment={article.sentimentLabel} />
          <TopicBadge topic={article.topicCategory} />
          <SourceCredibility source={article.source} />
        </div>

        <div className="medical-article-summary">
          <h3 className="clinical-subtitle">Resumen Médico</h3>
          <p className="medical-body">{article.summary}</p>
        </div>

        <div className="medical-article-analysis">
          <h3 className="clinical-subtitle">Análisis de Sentimiento</h3>
          <div className="sentiment-details">
            <div className="sentiment-score">
              Puntuación: {(article.sentimentScore * 100).toFixed(1)}%
            </div>
            <div className="sentiment-confidence">
              Confianza: {(article.sentimentConfidence * 100).toFixed(1)}%
            </div>
          </div>
        </div>

        <div className="medical-article-actions">
          <a
            href={article.url}
            target="_blank"
            rel="noopener noreferrer"
            className="btn-medical-primary"
          >
            Ver Artículo Original
          </a>
          <button
            onClick={() => exportArticleCitation(article)}
            className="btn-medical-secondary"
          >
            Generar Cita Académica
          </button>
        </div>
      </div>
    </Modal>
  );
};

// ExportButton.tsx - Academic export functionality
const MedicalExportButton = ({ filters }: { filters: MedicalFilters }) => {
  const [isExporting, setIsExporting] = useState(false);

  const handleExport = async (format: 'pdf' | 'excel' | 'csv') => {
    setIsExporting(true);
    try {
      const exportData = await medicalApi.exportDashboard(filters, format);
      downloadFile(exportData, `preventia-medical-report.${format}`);
    } catch (error) {
      showErrorToast('Error al exportar datos médicos');
    } finally {
      setIsExporting(false);
    }
  };

  return (
    <div className="medical-export-controls">
      <h3 className="clinical-subtitle">Exportar Análisis Médico</h3>
      <div className="export-buttons">
        <button
          onClick={() => handleExport('pdf')}
          disabled={isExporting}
          className="btn-medical-primary"
        >
          {isExporting ? <Loader2 className="animate-spin" /> : <FileText />}
          Reporte PDF
        </button>
        <button
          onClick={() => handleExport('excel')}
          disabled={isExporting}
          className="btn-medical-secondary"
        >
          <FileSpreadsheet />
          Datos Excel
        </button>
        <button
          onClick={() => handleExport('csv')}
          disabled={isExporting}
          className="btn-medical-secondary"
        >
          <Download />
          CSV Académico
        </button>
      </div>
    </div>
  );
};
```

**Deliverables Day 15-16:**
- ✅ Article detail modal with medical context
- ✅ Export functionality (PDF, Excel, CSV)
- ✅ Academic citation generator
- ✅ Source credibility indicators
- ✅ Medical metadata display

#### **Day 17-18: Performance Optimization**
**Priority: Medical-grade performance**

```typescript
// Performance optimization strategies
const PerformanceOptimizations = {
  // Code splitting for medical components
  lazyLoading: {
    'GeographicMap': lazy(() => import('./components/dashboard/GeographicMap')),
    'ArticleModal': lazy(() => import('./components/articles/ArticleModal')),
    'ExportButton': lazy(() => import('./components/articles/ExportButton'))
  },

  // Memoization for expensive medical calculations
  memoizedComponents: [
    'SentimentChart',
    'TopicsChart',
    'KPIGrid',
    'ArticlesTable'
  ],

  // Virtual scrolling for large medical datasets
  virtualizedTables: true,

  // Medical data caching strategy
  cachingStrategy: {
    kpiData: '5 minutes',
    sentimentData: '15 minutes',
    articles: '1 hour',
    staticData: '24 hours'
  }
};

// useMedicalPerformance.ts - Performance monitoring
export const useMedicalPerformance = () => {
  const [metrics, setMetrics] = useState<PerformanceMetrics>();

  useEffect(() => {
    // Track medical dashboard load times
    const observer = new PerformanceObserver((list) => {
      const entries = list.getEntries();
      const medicalMetrics = {
        firstContentfulPaint: entries.find(e => e.name === 'first-contentful-paint')?.value,
        largestContentfulPaint: entries.find(e => e.name === 'largest-contentful-paint')?.value,
        timeToInteractive: performance.now()
      };
      setMetrics(medicalMetrics);
    });

    observer.observe({ entryTypes: ['paint', 'navigation'] });
    return () => observer.disconnect();
  }, []);

  return metrics;
};
```

**Deliverables Day 17-18:**
- ✅ Code splitting implemented for heavy components
- ✅ Memoization for expensive medical calculations
- ✅ Virtual scrolling for articles table
- ✅ Performance monitoring dashboard
- ✅ Medical data caching optimization

#### **Day 19-20: Accessibility & Testing**
**Priority: Medical WCAG compliance**

```typescript
// MedicalAccessibility.tsx - WCAG compliance features
export const useMedicalAccessibility = () => {
  const [screenReaderAnnouncements, setAnnouncements] = useState<string[]>([]);

  const announceToScreenReader = (message: string) => {
    setAnnouncements(prev => [...prev, message]);
    // Clear after screen reader processes
    setTimeout(() => {
      setAnnouncements(prev => prev.slice(1));
    }, 1000);
  };

  return { announceToScreenReader, screenReaderAnnouncements };
};

// Medical keyboard navigation
const MedicalKeyboardNavigation = {
  shortcuts: {
    'Alt + O': () => navigateTo('/dashboard'),
    'Alt + A': () => navigateTo('/articles'),
    'Alt + F': () => focusFilters(),
    'Alt + E': () => openExportDialog(),
    'Escape': () => closeModals(),
    'Tab': () => navigateNext(),
    'Shift + Tab': () => navigatePrevious()
  }
};

// Medical test suite
describe('Medical Dashboard Accessibility', () => {
  test('should have proper ARIA labels for medical data', () => {
    render(<KPICard title="Artículos Analizados" value={106} />);
    expect(screen.getByLabelText('Métrica médica: Artículos Analizados')).toBeInTheDocument();
  });

  test('should announce sentiment changes to screen readers', () => {
    const { result } = renderHook(() => useMedicalAccessibility());
    act(() => {
      result.current.announceToScreenReader('Análisis de sentimiento actualizado: 71% negativo');
    });
    expect(result.current.screenReaderAnnouncements).toContain('Análisis de sentimiento actualizado: 71% negativo');
  });

  test('should support medical keyboard navigation', () => {
    render(<MedicalDashboard />);
    fireEvent.keyDown(document, { key: 'Alt+O' });
    expect(window.location.pathname).toBe('/dashboard');
  });
});
```

**Deliverables Day 19-20:**
- ✅ WCAG 2.1 AA compliance audit completed
- ✅ Screen reader optimization for medical data
- ✅ Keyboard navigation for all functionality
- ✅ Color contrast verification (4.5:1 minimum)
- ✅ Medical accessibility test suite

#### **Day 21: Final Integration & Documentation**
**Priority: Production readiness**

```typescript
// MedicalDashboard.tsx - Final integrated component
const MedicalDashboard = () => {
  const { data: analytics, isLoading: analyticsLoading } = useMedicalAnalytics();
  const { data: articles, isLoading: articlesLoading } = useMedicalArticles();
  const [filters, setFilters] = useMedicalFilters();
  const { announceToScreenReader } = useMedicalAccessibility();
  const performanceMetrics = useMedicalPerformance();

  // Announce data updates to screen readers
  useEffect(() => {
    if (analytics && !analyticsLoading) {
      announceToScreenReader(`Datos médicos actualizados: ${analytics.totalArticles} artículos analizados`);
    }
  }, [analytics, analyticsLoading]);

  return (
    <div className="medical-dashboard">
      <MedicalHeader />

      <main className="medical-main-content">
        <div className="medical-dashboard-grid">
          {/* KPI Cards */}
          <section className="medical-kpi-section">
            <h2 className="medical-title">Métricas Clínicas</h2>
            <Suspense fallback={<MedicalLoadingSpinner />}>
              <KPIGrid analytics={analytics} loading={analyticsLoading} />
            </Suspense>
          </section>

          {/* Visualizations */}
          <section className="medical-charts-section">
            <h2 className="medical-title">Análisis Médico</h2>
            <div className="medical-charts-grid">
              <Suspense fallback={<MedicalLoadingSpinner />}>
                <SentimentChart data={analytics?.sentimentDistribution} />
                <GeographicMap data={analytics?.geographicDistribution} />
                <TopicsChart data={analytics?.topicsByLanguage} />
                <TrendsChart data={analytics?.weeklyTrends} />
              </Suspense>
            </div>
          </section>

          {/* Articles Management */}
          <section className="medical-articles-section">
            <h2 className="medical-title">Literatura Médica</h2>
            <div className="medical-articles-container">
              <FilterPanel filters={filters} onFilterChange={setFilters} />
              <ArticlesTable
                articles={articles}
                filters={filters}
                loading={articlesLoading}
              />
              <ExportButton filters={filters} />
            </div>
          </section>
        </div>
      </main>

      <MedicalFooter />

      {/* Performance monitoring (development only) */}
      {process.env.NODE_ENV === 'development' && (
        <PerformanceMonitor metrics={performanceMetrics} />
      )}
    </div>
  );
};
```

**Deliverables Day 21:**
- ✅ Complete dashboard integration
- ✅ Production build optimization
- ✅ Performance benchmarks met (< 3s load)
- ✅ Medical documentation completed
- ✅ Deployment readiness checklist

**Week 3 Success Criteria:**
- [ ] Full dashboard functionality operational
- [ ] WCAG 2.1 AA compliance verified
- [ ] Performance targets achieved (< 3s load, < 100ms interactions)
- [ ] All 106 articles displayable with full medical context
- [ ] Export functionality working for academic use
- [ ] Mobile responsive across all medical devices

---

## 🎯 **Success Metrics & KPIs**

### **Technical Performance Targets**

#### **Medical Load Time Requirements**
```typescript
const MedicalPerformanceTargets = {
  // Critical for medical emergency access
  firstContentfulPaint: '<1.5s',

  // Professional medical standard
  largestContentfulPaint: '<2.5s',

  // Responsive clinical interaction
  firstInputDelay: '<100ms',

  // Stable medical data presentation
  cumulativeLayoutShift: '<0.1',

  // Full dashboard medical functionality
  timeToInteractive: '<3s',

  // Medical data loading
  apiResponseTimes: '<2s',
  chartRenderTimes: '<1s',
  tableFilterTimes: '<500ms',
  modalOpenTimes: '<300ms'
};
```

#### **Medical Functionality Requirements**
```typescript
const MedicalFunctionalityTargets = {
  dataAccuracy: {
    articlesDisplayed: 106,
    sentimentCoverage: '100%',
    topicClassification: '100%',
    geographicCoverage: '4 countries'
  },

  userExperience: {
    clickToInsight: '<5 seconds',
    filterResponseTime: '<1 second',
    exportGeneration: '<10 seconds',
    mobileUsability: 'Full functionality'
  },

  accessibility: {
    wcagCompliance: 'AA level minimum',
    keyboardNavigation: '100% functional',
    screenReaderSupport: 'Complete',
    colorContrastRatio: '>4.5:1'
  }
};
```

### **Medical User Acceptance Criteria**

#### **Clinical Stakeholder Requirements**
```typescript
const ClinicalAcceptanceCriteria = {
  // UCOMPENSAR Medical Researchers
  academicResearchers: {
    dataExportFormats: ['PDF', 'Excel', 'CSV', 'Citations'],
    filteringCapability: 'Advanced multi-dimensional',
    visualizationClarity: 'Professional medical standard',
    dataIntegrity: '100% accurate',
    responseTime: '<3 seconds for all operations'
  },

  // Medical Professionals
  clinicalProfessionals: {
    quickInsights: '<2 minutes to key information',
    mobileAccess: 'Full functionality on tablets/phones',
    medicalRelevance: 'Clinically meaningful data',
    trustworthiness: 'Source credibility clear',
    patientEducation: 'Suitable for patient discussions'
  },

  // Medical Students
  medicalStudents: {
    educationalValue: 'Clear learning objectives',
    easyNavigation: 'Intuitive medical interface',
    comprehensiveData: 'Broad medical topic coverage',
    citationSupport: 'Academic reference generation',
    guidedLearning: 'Self-explanatory medical insights'
  }
};
```

---

## 🧪 **Testing Strategy**

### **Medical Testing Framework**

#### **Unit Testing (Medical Components)**
```typescript
// Medical component testing
describe('MedicalKPICard', () => {
  test('displays medical metrics correctly', () => {
    render(<KPICard title="Artículos Médicos" value={106} />);
    expect(screen.getByText('106')).toBeInTheDocument();
    expect(screen.getByText('Artículos Médicos')).toBeInTheDocument();
  });

  test('handles medical loading states', () => {
    render(<KPICard title="Test" value={0} loading={true} />);
    expect(screen.getByTestId('medical-loading-spinner')).toBeInTheDocument();
  });

  test('announces updates to screen readers', () => {
    const mockAnnounce = jest.fn();
    render(<KPICard onUpdate={mockAnnounce} title="Test" value={106} />);
    expect(mockAnnounce).toHaveBeenCalledWith('Métrica médica actualizada: Test con valor 106');
  });
});
```

#### **Integration Testing (Medical API)**
```typescript
// Medical API integration testing
describe('Medical Dashboard Integration', () => {
  test('loads all medical data correctly', async () => {
    const mockData = createMedicalMockData();

    render(<MedicalDashboard />);

    await waitFor(() => {
      expect(screen.getByText('106')).toBeInTheDocument(); // Total articles
      expect(screen.getByText('71%')).toBeInTheDocument(); // Negative sentiment
      expect(screen.getByText('Estados Unidos')).toBeInTheDocument(); // Top country
    });
  });

  test('handles medical filter changes', async () => {
    render(<MedicalDashboard />);

    fireEvent.change(screen.getByLabelText('País'), { target: { value: 'México' } });
    fireEvent.click(screen.getByText('Aplicar Filtros'));

    await waitFor(() => {
      expect(mockApi.getArticles).toHaveBeenCalledWith({ country: 'México' });
    });
  });
});
```

#### **Accessibility Testing (Medical WCAG)**
```typescript
// Medical accessibility testing
describe('Medical Dashboard Accessibility', () => {
  test('meets WCAG AA standards', async () => {
    const { container } = render(<MedicalDashboard />);
    const results = await axe(container);
    expect(results).toHaveNoViolations();
  });

  test('supports medical keyboard navigation', () => {
    render(<MedicalDashboard />);

    // Test medical shortcuts
    fireEvent.keyDown(document, { key: 'Alt', code: 'AltLeft' });
    fireEvent.keyDown(document, { key: 'o', code: 'KeyO' });

    expect(screen.getByTestId('medical-overview')).toHaveFocus();
  });
});
```

### **Medical User Testing Protocol**

#### **Clinical User Testing Plan**
```typescript
const MedicalUserTestingProtocol = {
  participants: {
    medicalProfessionals: {
      count: 5,
      criteria: 'Active clinical practice, oncology preferred',
      scenarios: ['Quick clinical assessment', 'Patient education prep']
    },
    academicResearchers: {
      count: 4,
      criteria: 'UCOMPENSAR affiliation, research experience',
      scenarios: ['Research data export', 'Academic citation generation']
    },
    medicalStudents: {
      count: 3,
      criteria: 'Advanced medical students',
      scenarios: ['Educational exploration', 'Thesis research']
    }
  },

  testingScenarios: [
    {
      scenario: 'Emergency clinical insight access',
      goal: 'Get key sentiment insights for patient education',
      successCriteria: 'Complete in <2 minutes on mobile',
      medicalContext: 'Clinical rounds, limited time'
    },
    {
      scenario: 'Academic research preparation',
      goal: 'Filter and export relevant articles for research',
      successCriteria: 'Find and export 10 relevant articles in <5 minutes',
      medicalContext: 'Research paper preparation'
    },
    {
      scenario: 'Medical student learning',
      goal: 'Understand sentiment trends in breast cancer news',
      successCriteria: 'Navigate and comprehend insights independently',
      medicalContext: 'Self-directed learning session'
    }
  ],

  metrics: [
    'Task completion rate (medical context)',
    'Time to medical insight',
    'Error rate in medical navigation',
    'Subjective satisfaction with medical relevance',
    'Clinical utility rating (1-5)',
    'Academic authority perception',
    'Likelihood to recommend to colleagues'
  ]
};
```

---

## 🚀 **Deployment Strategy**

### **Medical Production Environment**

#### **Hosting & Infrastructure**
```yaml
# Medical deployment configuration
production:
  frontend:
    platform: "Vercel/Netlify"
    domain: "dashboard.preventia.ucompensar.edu.co"
    ssl: "Required for medical data"

  backend:
    platform: "Railway/DigitalOcean"
    api: "api.preventia.ucompensar.edu.co"
    database: "PostgreSQL managed service"

  monitoring:
    uptime: "UptimeRobot"
    performance: "Web Vitals"
    errors: "Sentry"
    medical_compliance: "Custom monitoring"

security:
  https: "Enforced"
  cors: "Restricted to medical domains"
  rate_limiting: "Medical-appropriate limits"
  data_protection: "GDPR compliant"
```

#### **Medical CI/CD Pipeline**
```yaml
# Medical deployment pipeline
name: Medical Dashboard Deployment

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  medical-quality-checks:
    runs-on: ubuntu-latest
    steps:
      - name: Medical Code Quality
        run: |
          npm run lint:medical
          npm run type-check
          npm run test:medical-coverage

      - name: Medical Accessibility Audit
        run: npm run a11y:medical

      - name: Medical Performance Audit
        run: npm run lighthouse:medical

  medical-deployment:
    needs: medical-quality-checks
    runs-on: ubuntu-latest
    steps:
      - name: Build Medical Dashboard
        run: npm run build:medical

      - name: Deploy to Medical Production
        run: npm run deploy:medical

      - name: Medical Health Check
        run: npm run health-check:medical
```

### **Medical Monitoring & Maintenance**

#### **Production Monitoring**
```typescript
// Medical production monitoring
const MedicalMonitoring = {
  healthChecks: {
    apiEndpoints: 'Every 5 minutes',
    dashboardLoad: 'Every 10 minutes',
    databaseConnection: 'Every 2 minutes',
    medicalDataIntegrity: 'Every hour'
  },

  performanceTracking: {
    coreWebVitals: 'Continuous',
    medicalLoadTimes: 'Real-time',
    apiResponseTimes: 'Per request',
    errorRates: 'Real-time alerts'
  },

  medicalAlerts: {
    dashboardDown: 'Immediate SMS/email',
    slowPerformance: '>3s load time',
    highErrorRate: '>1% medical errors',
    dataInconsistency: 'Medical data mismatch'
  }
};
```

---

## 📋 **Risk Assessment & Mitigation**

### **Medical Implementation Risks**

#### **High Priority Risks**
```typescript
const MedicalRisks = {
  technical: {
    apiCompatibility: {
      risk: 'FastAPI endpoints change breaking frontend',
      probability: 'Medium',
      impact: 'High',
      mitigation: 'API versioning + comprehensive testing'
    },

    performanceRegression: {
      risk: 'Dashboard becomes slower than 3s target',
      probability: 'Medium',
      impact: 'High',
      mitigation: 'Performance monitoring + optimization pipeline'
    },

    dataInconsistency: {
      risk: 'Medical data display differs from API data',
      probability: 'Low',
      impact: 'Critical',
      mitigation: 'Real-time data validation + automated testing'
    }
  },

  medical: {
    clinicalAccuracy: {
      risk: 'Medical professionals question data authority',
      probability: 'Low',
      impact: 'High',
      mitigation: 'Medical review process + source credibility display'
    },

    accessibilityCompliance: {
      risk: 'WCAG compliance issues block institutional use',
      probability: 'Medium',
      impact: 'High',
      mitigation: 'Automated a11y testing + manual expert review'
    }
  },

  timeline: {
    scopeCreep: {
      risk: '3-week timeline extends due to additional features',
      probability: 'High',
      impact: 'Medium',
      mitigation: 'Strict MVP scope + post-launch iteration plan'
    }
  }
};
```

#### **Risk Mitigation Strategies**
```typescript
const MitigationStrategies = {
  technicalRisks: [
    'Comprehensive API integration testing',
    'Performance budgets with CI/CD enforcement',
    'Real-time medical data validation',
    'Rollback strategy for failed deployments'
  ],

  medicalRisks: [
    'Medical stakeholder review at key milestones',
    'WCAG compliance automation in CI/CD',
    'Medical professional user testing sessions',
    'Clinical authority validation process'
  ],

  timelineRisks: [
    'MVP-first approach with clear feature prioritization',
    'Daily progress tracking with blockers identification',
    'Parallel development where possible',
    'Buffer time for medical review iterations'
  ]
};
```

---

## 📚 **Documentation & Handoff**

### **Medical Documentation Deliverables**

#### **Technical Documentation**
```typescript
const MedicalDocumentation = {
  technical: [
    'Component library documentation (Storybook)',
    'API integration guide',
    'Medical design system implementation',
    'Performance optimization guide',
    'Accessibility compliance documentation'
  ],

  medical: [
    'Clinical user guide (UCOMPENSAR stakeholders)',
    'Medical data interpretation guide',
    'Source credibility explanation',
    'Academic citation generation guide',
    'Patient education usage guidelines'
  ],

  operational: [
    'Deployment and maintenance guide',
    'Medical monitoring and alerting setup',
    'Troubleshooting common medical scenarios',
    'User feedback collection process',
    'Medical compliance audit checklist'
  ]
};
```

#### **Medical Training Materials**
```typescript
const MedicalTrainingPlan = {
  medicalProfessionals: {
    format: 'Interactive demo + PDF guide',
    duration: '30 minutes',
    content: [
      'Quick clinical insights access',
      'Patient education data usage',
      'Mobile access during rounds',
      'Source credibility evaluation'
    ]
  },

  academicResearchers: {
    format: 'Workshop + detailed documentation',
    duration: '60 minutes',
    content: [
      'Advanced filtering for research',
      'Academic export and citation',
      'Data interpretation for papers',
      'API access for custom analysis'
    ]
  },

  medicalStudents: {
    format: 'Self-guided tutorial',
    duration: '45 minutes',
    content: [
      'Dashboard navigation basics',
      'Educational data exploration',
      'Thesis research workflows',
      'Citation and reference generation'
    ]
  }
};
```

---

## 🎯 **Next Actions**

### **Immediate Implementation Steps**

#### **Week 1 Preparation (Before Implementation)**
1. **Final stakeholder approval** - Present plan to UCOMPENSAR medical team
2. **Technical environment setup** - Verify FastAPI endpoints availability
3. **Design system finalization** - Complete medical tokens implementation
4. **Team alignment** - Ensure development resources available

#### **Implementation Kickoff (Day 1)**
1. **Project initialization** - React + TypeScript + Medical dependencies
2. **Repository setup** - Git workflow + CI/CD medical pipeline
3. **Environment configuration** - API connections + medical monitoring
4. **First medical component** - KPICard with real data integration

#### **Weekly Checkpoints**
```typescript
const WeeklyCheckpoints = {
  week1: {
    milestone: 'Medical Foundation Complete',
    deliverables: ['KPI cards', 'Articles table', 'Basic filtering'],
    stakeholderReview: 'Medical professional feedback session'
  },

  week2: {
    milestone: 'Medical Visualizations Complete',
    deliverables: ['All 5 charts', 'Advanced filtering', 'Map integration'],
    stakeholderReview: 'Academic researcher feedback session'
  },

  week3: {
    milestone: 'Medical Production Ready',
    deliverables: ['Complete dashboard', 'Accessibility certified', 'Performance optimized'],
    stakeholderReview: 'Final UCOMPENSAR approval'
  }
};
```

---

**Este plan está listo para ejecución inmediata, con todos los componentes técnicos, médicos y académicos necesarios para crear un dashboard de clase mundial para PreventIA News Analytics.**

**Próximo paso**: Iniciar implementación Week 1, Day 1 con setup del proyecto React y configuración del medical design system.**

---

## 📖 **Referencias**

- [React 18 Documentation](https://react.dev/)
- [TanStack Query v5](https://tanstack.com/query/latest)
- [Tailwind CSS Medical Design](https://tailwindcss.com/docs)
- [Recharts Medical Visualization](https://recharts.org/)
- [React-Leaflet Geographic Maps](https://react-leaflet.js.org/)
- [WCAG 2.1 Medical Accessibility](https://www.w3.org/WAI/WCAG21/quickref/)
- [Web Vitals Performance](https://web.dev/vitals/)

**Plan implementación preparado por**: Cristhian Fernando Moreno Manrique, UCOMPENSAR
**Revisión médica**: Pendiente stakeholders UCOMPENSAR
**Implementación target**: Semana del 2025-07-08
