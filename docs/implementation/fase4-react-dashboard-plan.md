# FASE 4: React Dashboard Implementation Plan

**Fecha**: 2025-07-01
**Versión**: 1.0
**Autor**: Cristhian Fernando Moreno Manrique
**Estado**: 📋 Planificado - Listo para ejecución

---

## 🎯 **Executive Summary**

Plan detallado para implementar el dashboard React de PreventIA News Analytics con **estrategia de público híbrido**, basado en el prototipo HTML funcional y la estrategia UX/UI dual-mode documentada en ADR-008. Como proyecto de investigación académica UCOMPENSAR, implementa **Modo Profesional** y **Modo Educativo** para maximizar impacto científico y social.

**Objetivo**: Migrar dashboard HTML a React dual-mode con performance < 3s, accessibility WCAG AA+ y máximo impacto de investigación UCOMPENSAR.

**Base técnica**: 106 artículos procesados, sentiment analysis 100%, FastAPI operativo, design system dual-mode definido.

**Innovation**: Primera implementación de interfaz adaptativa médica/educativa en proyectos UCOMPENSAR.

---

## 📊 **Current State Assessment**

### **Assets Disponibles**
- ✅ **Prototipo HTML funcional** - `docs/assets/prototypes/dashboard_v0.1.html`
- ✅ **ADR-008 Hybrid Strategy** - Estrategia dual-mode documentada y aprobada
- ✅ **20+ FastAPI endpoints** operativos con performance < 5s
- ✅ **106 artículos analizados** con sentiment + topic classification
- ✅ **Design system dual-mode** completo documentado
- ✅ **UX/UI strategy híbrida** definida para stakeholders UCOMPENSAR
- ✅ **Público objetivo dual** - Profesionales + Educativo
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

### **Dual-Mode Components Architecture**
```typescript
// Componentes adaptivos para dual-mode interface
const DualModeComponents = {
  core: [
    'ModeToggle (Professional ↔ Educational)',
    'DualModeProvider (Context)',
    'AdaptiveHeader (mode-aware)',
    'AdaptiveNavigation (mode-specific)',
    'AdaptiveFooter (contextual)'
  ],

  kpis: [
    'AdaptiveKPICard (technical vs simplified)',
    'ArticleCountCard (106 articles)',
    'LanguageDistributionCard (64% EN / 36% ES)',
    'TopCountryCard (Estados Unidos)',
    'TopSourceCard (WebMD)'
  ],

  visualizations: [
    'AdaptiveSentimentChart (detailed vs explained)',
    'AdaptiveWeeklyTrends (technical vs guided)',
    'AdaptiveTopicsChart (clinical vs educational)',
    'AdaptiveGeographicMap (research vs informative)',
    'AdaptiveNewsChart (statistical vs accessible)'
  ],

  dataManagement: [
    'AdaptiveFilterPanel (advanced vs simplified)',
    'AdaptiveArticlesTable (complete vs summarized)',
    'AdaptiveArticleModal (technical vs explained)',
    'AdaptiveExportButtons (research vs educational)'
  ],

  educational: [
    'DefinitionsTooltip (medical terms)',
    'MedicalGlossary (expandable)',
    'ContextualHelp (mode-specific)',
    'GuidedTour (educational flow)',
    'LearningObjectives (educational mode)'
  ],

  professional: [
    'AdvancedAnalytics (statistical significance)',
    'ResearchExport (citations, methodology)',
    'PeerReviewContext (evidence levels)',
    'ConfidenceIntervals (medical precision)',
    'MethodologyDetails (research-grade)'
  ]
};
```

---

## 🏗️ **Technical Architecture**

### **Dual-Mode Frontend Stack**
```json
{
  "framework": "React 18 + TypeScript",
  "stateManagement": "TanStack Query v5 + Context API (dual-mode)",
  "styling": "Tailwind CSS v3 + Dual Design System",
  "routing": "React Router v6 + mode-aware routing",
  "charts": "Recharts v2 (adaptive medical visualizations)",
  "maps": "React-Leaflet v4 (contextual geographic data)",
  "forms": "React Hook Form v7 + adaptive validation",
  "icons": "Lucide React + Font Awesome Medical + Educational",
  "tooltips": "Floating UI (medical definitions)",
  "accessibility": "react-aria + axe-core (WCAG AA+ dual-mode)",
  "build": "Vite v5 + dual-mode optimization",
  "testing": "Vitest + React Testing Library (dual-mode testing)",
  "performance": "React DevTools Profiler + dual-mode metrics"
}
```

### **Dual-Mode Project Structure**
```
frontend/
├── public/
│   ├── index.html
│   ├── medical-icons/
│   └── educational-icons/
├── src/
│   ├── components/
│   │   ├── core/
│   │   │   ├── ModeToggle.tsx
│   │   │   ├── DualModeProvider.tsx
│   │   │   └── AdaptiveWrapper.tsx
│   │   ├── layout/
│   │   │   ├── AdaptiveHeader.tsx
│   │   │   ├── AdaptiveNavigation.tsx
│   │   │   └── AdaptiveFooter.tsx
│   │   ├── dashboard/
│   │   │   ├── adaptive/
│   │   │   │   ├── AdaptiveKPICard.tsx
│   │   │   │   ├── AdaptiveSentimentChart.tsx
│   │   │   │   ├── AdaptiveGeographicMap.tsx
│   │   │   │   ├── AdaptiveTopicsChart.tsx
│   │   │   │   └── AdaptiveTrendsChart.tsx
│   │   │   ├── professional/
│   │   │   │   ├── AdvancedAnalytics.tsx
│   │   │   │   ├── ResearchExport.tsx
│   │   │   │   ├── PeerReviewContext.tsx
│   │   │   │   └── MethodologyDetails.tsx
│   │   │   └── educational/
│   │   │       ├── DefinitionsTooltip.tsx
│   │   │       ├── MedicalGlossary.tsx
│   │   │       ├── GuidedTour.tsx
│   │   │       └── LearningObjectives.tsx
│   │   ├── articles/
│   │   │   ├── AdaptiveArticlesTable.tsx
│   │   │   ├── AdaptiveArticleModal.tsx
│   │   │   ├── AdaptiveFilterPanel.tsx
│   │   │   └── AdaptiveExportButton.tsx
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
│   ├── contexts/
│   │   ├── DualModeContext.tsx
│   │   ├── UserModeContext.tsx
│   │   └── AccessibilityContext.tsx
│   ├── hooks/
│   │   ├── useApi.ts
│   │   ├── useDualMode.ts
│   │   ├── useAdaptiveFilters.ts
│   │   ├── usePerformanceTracking.ts
│   │   ├── useAccessibility.ts
│   │   └── useEducationalMode.ts
│   ├── services/
│   │   ├── api.ts
│   │   ├── analytics.ts
│   │   ├── articles.ts
│   │   ├── export.ts
│   │   └── dualMode.ts
│   ├── types/
│   │   ├── dualMode.ts
│   │   ├── medical.ts
│   │   ├── educational.ts
│   │   ├── analytics.ts
│   │   ├── articles.ts
│   │   └── api.ts
│   ├── utils/
│   │   ├── adaptive-formatting.ts
│   │   ├── medical-terminology.ts
│   │   ├── educational-simplification.ts
│   │   ├── date-utils.ts
│   │   ├── export-utils.ts
│   │   └── accessibility.ts
│   ├── styles/
│   │   ├── globals.css
│   │   ├── dual-mode-components.css
│   │   ├── professional-theme.css
│   │   ├── educational-theme.css
│   │   └── accessibility.css
│   └── App.tsx
├── package.json
├── tailwind.config.js (dual-mode theme)
├── vite.config.ts
└── tsconfig.json
```

---

## 📅 **Dual-Mode Implementation Timeline (4 Semanas)**

### **Week 1: Dual Foundation (2025-07-08)**

#### **Day 1-2: Project Setup & Dual-Mode Design System**
```bash
# Setup Commands
npm create vite@latest preventia-dashboard --template react-ts
cd preventia-dashboard
npm install

# Dual-Mode Dependencies
npm install @tanstack/react-query @tanstack/react-query-devtools
npm install react-router-dom react-hook-form
npm install tailwindcss @tailwindcss/forms @tailwindcss/typography
npm install recharts react-leaflet leaflet
npm install lucide-react @heroicons/react
npm install axios clsx tailwind-merge
npm install @testing-library/react @testing-library/jest-dom vitest

# Dual-Mode Specific
npm install @floating-ui/react  # Medical definitions tooltips
npm install react-aria @axe-core/react  # Dual accessibility
npm install framer-motion  # Mode transitions
npm install react-hotkeys-hook  # Professional keyboard shortcuts
npm install @types/leaflet
```

**Deliverables Day 1-2:**
- ✅ Project initialized with dual-mode stack
- ✅ Tailwind dual-mode theme configured (professional + educational)
- ✅ Dual design system tokens implemented
- ✅ DualModeProvider context created
- ✅ ModeToggle component implemented
- ✅ Basic adaptive folder structure created
- ✅ TypeScript dual-mode types defined

#### **Day 3-4: Core Dual-Mode Infrastructure**
**Priority: Mode Toggle + Adaptive Layout Foundation**

```typescript
// DualModeContext.tsx - Core dual-mode state management
interface DualModeContextType {
  mode: 'professional' | 'educational';
  toggleMode: () => void;
  userPreferences: UserPreferences;
  updatePreferences: (prefs: Partial<UserPreferences>) => void;
}

// AdaptiveWrapper.tsx - Component adaptation engine
interface AdaptiveWrapperProps {
  children: React.ReactNode;
  professionalVariant: React.ComponentType;
  educationalVariant: React.ComponentType;
  fallback?: React.ComponentType;
}

// ModeToggle.tsx - Professional ↔ Educational switch
const ModeToggle = () => {
  const { mode, toggleMode } = useDualMode();

  return (
    <motion.div className="mode-toggle">
      <span className={mode === 'professional' ? 'active' : ''}>
        Modo Profesional
      </span>
      <Switch checked={mode === 'educational'} onChange={toggleMode} />
      <span className={mode === 'educational' ? 'active' : ''}>
        Modo Educativo
      </span>
    </motion.div>
  );
};
```

**Deliverables Day 3-4:**
- ✅ DualModeProvider context functioning
- ✅ ModeToggle with smooth transitions
- ✅ AdaptiveWrapper component engine
- ✅ Basic adaptive layout structure
- ✅ Mode persistence in localStorage

#### **Day 5-6: API Integration & Data Layer**
**Priority: FastAPI connection + dual-mode data adaptation**

```typescript
// api.ts - Dual-mode API client
class DualModeApiClient {
  private baseURL = 'http://localhost:8000/api';

  async getAnalyticsSummary(mode: 'professional' | 'educational'): Promise<AnalyticsSummary> {
    const response = await fetch(`${this.baseURL}/analytics/summary`);
    const data = await response.json();

    // Adapt data based on mode
    return mode === 'professional'
      ? this.formatProfessional(data)
      : this.formatEducational(data);
  }

  private formatProfessional(data: any): AnalyticsSummary {
    return {
      ...data,
      terminologyLevel: 'medical',
      showConfidenceIntervals: true,
      showMethodology: true
    };
  }

  private formatEducational(data: any): AnalyticsSummary {
    return {
      ...data,
      terminologyLevel: 'accessible',
      includeExplanations: true,
      showSimplifiedMetrics: true
    };
  }
}

// useDualModeData.ts - TanStack Query with dual adaptation
export const useDualAnalytics = () => {
  const { mode } = useDualMode();

  return useQuery({
    queryKey: ['analytics', mode],
    queryFn: () => dualApiClient.getAnalyticsSummary(mode),
    staleTime: 5 * 60 * 1000, // 5 min cache
  });
};
```

**Deliverables Day 5-6:**
- ✅ API client with dual-mode data adaptation
- ✅ TanStack Query hooks for both modes
- ✅ Error handling for both audiences
- ✅ Loading states adapted to user context
- ✅ Real data flowing to adaptive components

#### **Day 7: First Adaptive Components**
**Priority: AdaptiveKPICard + basic adaptive navigation**

```typescript
// AdaptiveKPICard.tsx - Dual-mode metric display
interface AdaptiveKPICardProps {
  title: string;
  value: number | string;
  mode: 'professional' | 'educational';
  explanation?: string; // Educational mode
  technicalDetails?: string; // Professional mode
  confidenceInterval?: [number, number]; // Professional mode
}

const AdaptiveKPICard: React.FC<AdaptiveKPICardProps> = ({
  title, value, mode, explanation, technicalDetails, confidenceInterval
}) => {
  if (mode === 'professional') {
    return (
      <div className="kpi-card professional">
        <h3 className="text-lg font-semibold text-academic-navy">{title}</h3>
        <div className="value-display">
          <span className="text-3xl font-bold text-primary-blue">{value}</span>
          {confidenceInterval && (
            <span className="text-sm text-gray-600">
              CI: [{confidenceInterval[0]}, {confidenceInterval[1]}]
            </span>
          )}
        </div>
        {technicalDetails && (
          <p className="text-sm text-gray-700">{technicalDetails}</p>
        )}
      </div>
    );
  }

  return (
    <div className="kpi-card educational">
      <h3 className="text-lg font-medium text-gray-800">{title}</h3>
      <div className="value-display">
        <span className="text-2xl font-semibold text-primary-pink">{value}</span>
      </div>
      {explanation && (
        <div className="explanation">
          <DefinitionTooltip term={title} definition={explanation} />
          <p className="text-sm text-gray-600 mt-2">{explanation}</p>
        </div>
      )}
    </div>
  );
};
```

**Deliverables Day 7:**
- ✅ AdaptiveKPICard functioning in both modes
- ✅ Basic adaptive navigation structure
- ✅ DefinitionTooltip component for educational mode
- ✅ Professional vs educational styling differentiation
- ✅ First end-to-end dual-mode user experience

**Week 1 Success Criteria:**
- [ ] Mode toggle functions smoothly between professional/educational
- [ ] KPI cards display correctly in both modes
- [ ] API data loads and adapts based on mode
- [ ] Basic dual-mode navigation working
- [ ] Performance < 3s for initial load in both modes

---

### **Week 2: Professional Mode Implementation (2025-07-15)**

#### **Day 8-9: Advanced Professional Components**
**Priority: Research-grade analytics for medical professionals**

```typescript
// AdvancedAnalytics.tsx - Professional statistical analysis
interface AdvancedAnalyticsProps {
  data: AnalyticsData;
  showConfidenceIntervals: boolean;
  showStatisticalSignificance: boolean;
}

const AdvancedAnalytics: React.FC<AdvancedAnalyticsProps> = ({ data }) => {
  return (
    <div className="professional-analytics">
      <StatisticalSummary data={data} />
      <ConfidenceIntervals metrics={data.metrics} />
      <SignificanceTests results={data.tests} />
      <MethodologyDetails methods={data.methodology} />
    </div>
  );
};

// ProfessionalSentimentChart.tsx - Medical-grade sentiment visualization
const ProfessionalSentimentChart = () => {
  return (
    <div className="professional-chart">
      <ResponsiveContainer width="100%" height={400}>
        <PieChart>
          <Pie
            data={sentimentData}
            dataKey="value"
            nameKey="sentiment"
            cx="50%"
            cy="50%"
            outerRadius={120}
            label={({ name, value, percentage }) =>
              `${name}: ${value} (${percentage.toFixed(1)}%, CI: ±${confidenceMargin}%)`
            }
          />
          <Tooltip content={<ProfessionalTooltip />} />
          <Legend content={<ProfessionalLegend />} />
        </PieChart>
      </ResponsiveContainer>
    </div>
  );
};
```

**Deliverables Day 8-9:**
- ✅ Advanced analytics dashboard for professionals
- ✅ Statistical significance indicators
- ✅ Confidence intervals display
- ✅ Methodology details sections
- ✅ Professional-grade chart tooltips and legends

#### **Day 10-11: Research Export & Citation System**
**Priority: Academic research functionality**

```typescript
// ResearchExport.tsx - Academic export functionality
interface ResearchExportProps {
  data: AnalyticsData;
  format: 'pdf' | 'excel' | 'csv' | 'bibtex';
}

const ResearchExport: React.FC<ResearchExportProps> = ({ data, format }) => {
  const generateCitation = () => {
    return {
      apa: "Moreno, C. F. (2025). PreventIA News Analytics: Sentiment Analysis of Breast Cancer Media Coverage. UCOMPENSAR Research.",
      mla: "Moreno, Cristhian Fernando. \"PreventIA News Analytics.\" UCOMPENSAR, 2025.",
      vancouver: "Moreno CF. PreventIA News Analytics: Sentiment Analysis of Breast Cancer Media Coverage. UCOMPENSAR Research. 2025."
    };
  };

  const exportData = async () => {
    switch (format) {
      case 'pdf':
        return generatePDFReport(data, generateCitation());
      case 'excel':
        return generateExcelWorkbook(data);
      case 'bibtex':
        return generateBibTeX(generateCitation());
      default:
        return generateCSV(data);
    }
  };

  return (
    <div className="research-export">
      <ExportOptions onExport={exportData} />
      <CitationGenerator citations={generateCitation()} />
      <MethodologySection methodology={data.methodology} />
    </div>
  );
};

// PeerReviewContext.tsx - Evidence levels and quality indicators
const PeerReviewContext = ({ article }: { article: Article }) => {
  const evidenceLevel = calculateEvidenceLevel(article);
  const qualityScore = calculateQualityScore(article);

  return (
    <div className="peer-review-context">
      <EvidenceLevel level={evidenceLevel} />
      <QualityIndicators score={qualityScore} />
      <SourceCredibility source={article.source} />
      <BiasAssessment content={article.content} />
    </div>
  );
};
```

**Deliverables Day 10-11:**
- ✅ PDF/Excel export with academic formatting
- ✅ Citation generation (APA, MLA, Vancouver)
- ✅ Methodology documentation
- ✅ Evidence level indicators
- ✅ Source credibility assessment

#### **Day 12-13: Professional Data Tables & Filtering**
**Priority: Advanced filtering and professional data management**

```typescript
// ProfessionalArticlesTable.tsx - Research-grade data table
const ProfessionalArticlesTable = () => {
  const [sortConfig, setSortConfig] = useState<SortConfig>();
  const [filters, setFilters] = useState<ProfessionalFilters>({
    evidenceLevel: 'all',
    statisticalSignificance: false,
    peerReviewed: false,
    confidenceInterval: [0.95, 1.0],
    sampleSize: { min: 0, max: Infinity }
  });

  return (
    <div className="professional-table">
      <AdvancedFilterPanel
        filters={filters}
        onFiltersChange={setFilters}
      />
      <DataTable
        columns={professionalColumns}
        data={filteredData}
        sortConfig={sortConfig}
        onSort={setSortConfig}
        renderRow={ProfessionalTableRow}
      />
      <StatisticalSummary data={filteredData} />
    </div>
  );
};

// AdvancedFilterPanel.tsx - Professional filtering options
const AdvancedFilterPanel = ({ filters, onFiltersChange }) => {
  return (
    <div className="advanced-filters">
      <FilterGroup title="Statistical Criteria">
        <ConfidenceIntervalSlider />
        <SampleSizeRange />
        <SignificanceLevel />
      </FilterGroup>

      <FilterGroup title="Evidence Quality">
        <EvidenceLevelSelect />
        <PeerReviewedToggle />
        <SourceCredibilityFilter />
      </FilterGroup>

      <FilterGroup title="Methodological">
        <StudyDesignFilter />
        <BiasRiskFilter />
        <ReplicationStatusFilter />
      </FilterGroup>
    </div>
  );
};
```

**Deliverables Day 12-13:**
- ✅ Advanced filtering system for professionals
- ✅ Statistical criteria filters
- ✅ Evidence quality indicators
- ✅ Professional data table with sorting
- ✅ Real-time statistical summaries

#### **Day 14: Professional Mode Polish & Testing**
**Priority: Professional user experience optimization**

**Deliverables Day 14:**
- ✅ Professional mode fully functional
- ✅ All professional components polished
- ✅ Professional keyboard shortcuts implemented
- ✅ Professional accessibility features
- ✅ Professional mode performance optimization

**Week 2 Success Criteria:**
- [ ] Professional mode provides research-grade analytics
- [ ] Export functionality works for academic use
- [ ] Advanced filtering meets professional needs
- [ ] Performance < 3s for professional complex queries
- [ ] Statistical accuracy verified

---

### **Week 3: Educational Mode Implementation (2025-07-22)**

#### **Day 15-16: Educational Interface Foundation**
**Priority: Accessible and guided educational experience**

```typescript
// EducationalWrapper.tsx - Simplified interface wrapper
const EducationalWrapper = ({ children, concept, explanation }) => {
  return (
    <div className="educational-wrapper">
      <ConceptHeader concept={concept} />
      <div className="simplified-content">
        {children}
      </div>
      <EducationalFooter explanation={explanation} />
    </div>
  );
};

// MedicalGlossary.tsx - Expandable medical definitions
const MedicalGlossary = () => {
  const [selectedTerm, setSelectedTerm] = useState(null);

  const medicalTerms = {
    'sentiment_analysis': {
      simple: 'Análisis de si una noticia es positiva o negativa',
      detailed: 'Técnica que usa inteligencia artificial para identificar emociones en textos médicos'
    },
    'confidence_interval': {
      simple: 'Qué tan seguros estamos del resultado',
      detailed: 'Rango estadístico que indica la precisión de una medición científica'
    }
  };

  return (
    <div className="medical-glossary">
      <GlossarySearch onTermSelect={setSelectedTerm} />
      <TermsList terms={medicalTerms} />
      {selectedTerm && (
        <TermDefinition term={selectedTerm} />
      )}
    </div>
  );
};

// DefinitionsTooltip.tsx - Contextual help for medical terms
const DefinitionsTooltip = ({ term, definition, children }) => {
  return (
    <FloatingUI
      content={
        <div className="definition-tooltip">
          <h4 className="font-semibold">{term}</h4>
          <p className="text-sm">{definition}</p>
          <a href={`/glossary/${term}`} className="learn-more">
            Aprender más →
          </a>
        </div>
      }
      placement="top"
    >
      <span className="underline decoration-dotted cursor-help">
        {children}
      </span>
    </FloatingUI>
  );
};
```

**Deliverables Day 15-16:**
- ✅ Educational wrapper components
- ✅ Medical glossary with search
- ✅ Contextual definitions tooltips
- ✅ Simplified terminology system
- ✅ Educational navigation structure

#### **Day 17-18: Guided Learning Experience**
**Priority: Educational tour and learning objectives**

```typescript
// GuidedTour.tsx - Step-by-step educational experience
const GuidedTour = () => {
  const [currentStep, setCurrentStep] = useState(0);

  const tourSteps = [
    {
      target: '.kpi-cards',
      title: '¿Qué son las métricas de salud?',
      content: 'Estas tarjetas muestran información importante sobre noticias de cáncer de mama',
      explanation: 'Las métricas nos ayudan a entender patrones en la información médica'
    },
    {
      target: '.sentiment-chart',
      title: 'Análisis de sentimientos',
      content: 'Este gráfico muestra si las noticias son positivas o negativas',
      explanation: 'Es importante para entender cómo se comunica la información médica'
    }
  ];

  return (
    <Joyride
      steps={tourSteps}
      run={true}
      continuous={true}
      showProgress={true}
      showSkipButton={true}
      callback={handleTourCallback}
      styles={{
        options: {
          primaryColor: '#F8BBD9', // Medical pink
        }
      }}
    />
  );
};

// LearningObjectives.tsx - Educational goals for each section
const LearningObjectives = ({ section }) => {
  const objectives = {
    dashboard: [
      'Entender qué información muestran las métricas de salud',
      'Aprender a interpretar gráficos médicos básicos',
      'Conocer fuentes confiables de información médica'
    ],
    sentiment: [
      'Comprender qué es el análisis de sentimientos',
      'Identificar noticias positivas vs negativas',
      'Evaluar la calidad de información médica'
    ]
  };

  return (
    <div className="learning-objectives">
      <h3 className="educational-heading">Objetivos de Aprendizaje</h3>
      <ul className="objectives-list">
        {objectives[section]?.map((objective, index) => (
          <li key={index} className="objective-item">
            <CheckIcon className="complete-icon" />
            {objective}
          </li>
        ))}
      </ul>
    </div>
  );
};
```

**Deliverables Day 17-18:**
- ✅ Guided tour system implemented
- ✅ Learning objectives for each section
- ✅ Progressive disclosure of information
- ✅ Educational progress tracking
- ✅ Contextual help system

#### **Day 19-20: Educational Visualizations**
**Priority: Simplified and explained charts**

```typescript
// EducationalSentimentChart.tsx - Simplified visualization with explanations
const EducationalSentimentChart = () => {
  const [showExplanation, setShowExplanation] = useState(false);

  return (
    <div className="educational-chart">
      <div className="chart-header">
        <h3>Análisis de Sentimientos en Noticias Médicas</h3>
        <button
          onClick={() => setShowExplanation(!showExplanation)}
          className="explain-button"
        >
          ¿Qué significa esto?
        </button>
      </div>

      {showExplanation && (
        <div className="explanation-panel">
          <h4>¿Qué es el análisis de sentimientos?</h4>
          <p>Es una técnica que nos ayuda a entender si una noticia médica
             transmite emociones positivas, negativas o neutrales.</p>

          <h4>¿Por qué es importante?</h4>
          <p>Nos ayuda a entender cómo se comunica la información médica
             y su posible impacto en los pacientes.</p>
        </div>
      )}

      <SimplifiedPieChart
        data={sentimentData}
        showLabels={true}
        showPercentages={true}
        colors={educationalColors}
      />

      <ChartSummary
        insights={[
          'La mayoría de noticias son informativas (neutral)',
          'Las noticias positivas hablan de avances médicos',
          'Las noticias negativas discuten riesgos o problemas'
        ]}
      />
    </div>
  );
};

// InteractiveMap.tsx - Educational geographic visualization
const InteractiveMap = () => {
  const [selectedCountry, setSelectedCountry] = useState(null);

  return (
    <div className="educational-map">
      <MapLegend
        title="Fuentes de Información Médica por País"
        explanation="Este mapa muestra de dónde vienen las noticias médicas que analizamos"
      />

      <Map
        center={[20, 0]}
        zoom={2}
        style={{ height: '400px' }}
      >
        {countryData.map(country => (
          <CountryMarker
            key={country.code}
            country={country}
            onClick={setSelectedCountry}
            simplified={true}
          />
        ))}
      </Map>

      {selectedCountry && (
        <CountryInfo
          country={selectedCountry}
          educationalMode={true}
        />
      )}
    </div>
  );
};
```

**Deliverables Day 19-20:**
- ✅ Simplified educational charts
- ✅ Interactive explanations
- ✅ Educational color schemes
- ✅ Chart summaries with insights
- ✅ Interactive educational map

#### **Day 21: Educational Mode Polish & Integration**
**Priority: Complete educational experience**

**Deliverables Day 21:**
- ✅ Educational mode fully functional
- ✅ All educational components integrated
- ✅ Educational accessibility features
- ✅ Educational mode performance optimization
- ✅ Educational content validation

**Week 3 Success Criteria:**
- [ ] Educational mode provides clear, accessible information
- [ ] Guided tour helps users understand medical concepts
- [ ] All medical terms have accessible explanations
- [ ] Educational visualizations are intuitive
- [ ] Learning objectives are achievable

---

### **Week 4: Integration, Testing & Production (2025-07-29)**

#### **Day 22-23: Dual-Mode Integration & Testing**
**Priority: Seamless mode switching and comprehensive testing**

```typescript
// DualModeIntegration.test.tsx - Comprehensive dual-mode testing
describe('Dual Mode Integration', () => {
  test('mode toggle preserves user data', async () => {
    const { user } = render(<DashboardApp />);

    // Set filters in professional mode
    await user.click(screen.getByRole('combobox', { name: /evidence level/i }));
    await user.selectOption(screen.getByRole('option', { name: /high/i }));

    // Switch to educational mode
    await user.click(screen.getByRole('switch', { name: /modo educativo/i }));

    // Switch back to professional mode
    await user.click(screen.getByRole('switch', { name: /modo profesional/i }));

    // Verify filters are preserved
    expect(screen.getByDisplayValue('high')).toBeInTheDocument();
  });

  test('educational mode shows simplified content', async () => {
    render(<DashboardApp initialMode="educational" />);

    expect(screen.getByText(/análisis de sentimientos/i)).toBeInTheDocument();
    expect(screen.queryByText(/confidence interval/i)).not.toBeInTheDocument();
    expect(screen.getByRole('button', { name: /qué significa esto/i })).toBeInTheDocument();
  });

  test('professional mode shows advanced analytics', async () => {
    render(<DashboardApp initialMode="professional" />);

    expect(screen.getByText(/statistical significance/i)).toBeInTheDocument();
    expect(screen.getByText(/confidence interval/i)).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /export research/i })).toBeInTheDocument();
  });
});

// PerformanceTesting.test.tsx - Dual-mode performance validation
describe('Performance Testing', () => {
  test('professional mode loads within 3s', async () => {
    const startTime = performance.now();
    render(<DashboardApp initialMode="professional" />);

    await waitFor(() => {
      expect(screen.getByTestId('dashboard-loaded')).toBeInTheDocument();
    });

    const loadTime = performance.now() - startTime;
    expect(loadTime).toBeLessThan(3000);
  });

  test('educational mode loads within 3s', async () => {
    const startTime = performance.now();
    render(<DashboardApp initialMode="educational" />);

    await waitFor(() => {
      expect(screen.getByTestId('dashboard-loaded')).toBeInTheDocument();
    });

    const loadTime = performance.now() - startTime;
    expect(loadTime).toBeLessThan(3000);
  });
});
```

**Deliverables Day 22-23:**
- ✅ Comprehensive dual-mode testing suite
- ✅ Performance testing for both modes
- ✅ User experience testing
- ✅ Data persistence testing
- ✅ Accessibility testing (WCAG AA+)

#### **Day 24-25: Accessibility & Polish**
**Priority: WCAG 2.1 AA+ compliance and final UX polish**

```typescript
// AccessibilityAudit.test.tsx - WCAG compliance testing
describe('Accessibility Compliance', () => {
  test('professional mode meets WCAG AA+ standards', async () => {
    const { container } = render(<DashboardApp initialMode="professional" />);
    const results = await axe(container);
    expect(results).toHaveNoViolations();
  });

  test('educational mode meets WCAG AA+ standards', async () => {
    const { container } = render(<DashboardApp initialMode="educational" />);
    const results = await axe(container);
    expect(results).toHaveNoViolations();
  });

  test('keyboard navigation works in both modes', async () => {
    const user = userEvent.setup();
    render(<DashboardApp />);

    // Test tab navigation
    await user.keyboard('{Tab}');
    expect(screen.getByRole('switch', { name: /modo/i })).toHaveFocus();

    // Test mode switching with keyboard
    await user.keyboard('{Space}');
    expect(screen.getByText(/modo educativo activo/i)).toBeInTheDocument();
  });
});

// FinalPolish.tsx - Production-ready optimizations
const ProductionOptimizations = {
  // Code splitting by mode
  ProfessionalMode: lazy(() => import('./modes/ProfessionalMode')),
  EducationalMode: lazy(() => import('./modes/EducationalMode')),

  // Performance optimizations
  memoizeComponents: true,
  enableServiceWorker: true,
  optimizeImages: true,

  // Accessibility enhancements
  screenReaderSupport: true,
  keyboardShortcuts: true,
  highContrastMode: true,

  // Analytics
  trackModeUsage: true,
  trackUserJourney: true,
  trackPerformanceMetrics: true
};
```

**Deliverables Day 24-25:**
- ✅ WCAG 2.1 AA+ compliance verified
- ✅ Keyboard navigation perfected
- ✅ Screen reader support optimized
- ✅ High contrast mode implemented
- ✅ Final UX polish applied

#### **Day 26-27: User Testing & Validation**
**Priority: Stakeholder validation with UCOMPENSAR community**

```typescript
// UserTesting.plan.ts - Structured user testing approach
const UserTestingPlan = {
  professionalUsers: {
    participants: ['medical_professionals', 'researchers', 'academic_staff'],
    tasks: [
      'Find statistical significance of sentiment trends',
      'Export data for academic publication',
      'Navigate advanced filtering options',
      'Interpret confidence intervals'
    ],
    successCriteria: {
      taskCompletion: '>90%',
      satisfaction: '>4.5/5',
      efficiency: '<60s per task'
    }
  },

  educationalUsers: {
    participants: ['medical_students', 'educated_public', 'healthcare_students'],
    tasks: [
      'Understand what sentiment analysis means',
      'Learn about medical information sources',
      'Use guided tour to explore dashboard',
      'Find and understand medical definitions'
    ],
    successCriteria: {
      comprehension: '>85%',
      satisfaction: '>4.0/5',
      learningObjectives: '>80% achieved'
    }
  }
};

// UserFeedback.component.tsx - Integrated feedback collection
const UserFeedbackCollector = () => {
  const { mode } = useDualMode();

  const collectFeedback = async (feedback: UserFeedback) => {
    await analytics.track('user_feedback', {
      mode,
      rating: feedback.rating,
      category: feedback.category,
      improvements: feedback.improvements,
      timestamp: new Date().toISOString()
    });
  };

  return (
    <FeedbackModal
      mode={mode}
      onSubmit={collectFeedback}
      questions={mode === 'professional' ? professionalQuestions : educationalQuestions}
    />
  );
};
```

**Deliverables Day 26-27:**
- ✅ User testing completed with both audiences
- ✅ Feedback collection system implemented
- ✅ User satisfaction metrics gathered
- ✅ Performance validation with real users
- ✅ Accessibility validation with diverse users

#### **Day 28: Production Deployment & Launch**
**Priority: Production deployment and monitoring setup**

```typescript
// Production.config.ts - Production deployment configuration
const ProductionConfig = {
  deployment: {
    platform: 'Docker + nginx',
    environment: 'production',
    domain: 'preventia.ucompensar.edu.co',
    ssl: true,
    cdn: true
  },

  monitoring: {
    performance: 'Web Vitals + Lighthouse',
    errors: 'Sentry error tracking',
    analytics: 'Google Analytics + custom dual-mode tracking',
    uptime: '99.9% SLA target'
  },

  security: {
    contentSecurityPolicy: true,
    httpsOnly: true,
    securityHeaders: true,
    accessLogging: true
  },

  backup: {
    userPreferences: 'daily backup',
    usageAnalytics: 'real-time sync',
    performanceMetrics: 'continuous monitoring'
  }
};

// Deployment.script.sh - Automated deployment
#!/bin/bash
echo "🚀 Deploying PreventIA Dual-Mode Dashboard..."

# Build dual-mode application
npm run build:dual-mode

# Run final tests
npm run test:production

# Deploy to production
docker build -t preventia-dashboard:dual-mode .
docker push registry.ucompensar.edu.co/preventia-dashboard:dual-mode

# Update production environment
kubectl apply -f k8s/production/
kubectl rollout status deployment/preventia-dashboard

echo "✅ Dual-Mode Dashboard deployed successfully!"
echo "🔗 Professional Mode: https://preventia.ucompensar.edu.co/?mode=professional"
echo "🎓 Educational Mode: https://preventia.ucompensar.edu.co/?mode=educational"
```

**Deliverables Day 28:**
- ✅ Production deployment completed
- ✅ Monitoring and analytics configured
- ✅ Security measures implemented
- ✅ Backup systems operational
- ✅ Documentation updated
- ✅ UCOMPENSAR team training completed

**Week 4 Success Criteria:**
- [ ] Both modes pass all tests with >95% success rate
- [ ] WCAG 2.1 AA+ compliance verified across both modes
- [ ] User satisfaction >4.5/5 (professional) and >4.0/5 (educational)
- [ ] Performance <3s for both modes in production
- [ ] Production deployment successful with monitoring active

---

## 📊 **Success Metrics & Validation**

### **Dual-Mode Performance Targets**

#### **Technical Performance**
- **Load Time**: <3s for initial dashboard load (both modes)
- **Mode Switching**: <500ms transition time
- **API Response**: <2s for all data queries
- **Memory Usage**: <100MB baseline memory footprint
- **Bundle Size**: <2MB total (with code splitting)

#### **User Experience Metrics**
- **Professional Mode**:
  - Task completion rate: >90%
  - User satisfaction: >4.5/5
  - Feature discovery: >80%
  - Research workflow efficiency: >85%

- **Educational Mode**:
  - Comprehension rate: >85%
  - Learning objective achievement: >80%
  - User satisfaction: >4.0/5
  - Concept retention: >75%

#### **Accessibility Compliance**
- **WCAG 2.1 AA+**: 100% compliance for both modes
- **Keyboard Navigation**: Full functionality without mouse
- **Screen Reader Support**: Complete content accessibility
- **Color Contrast**: >4.5:1 ratio for all text
- **Focus Management**: Clear focus indicators throughout

### **Research Impact Metrics**

#### **Academic Value**
- **Publication Potential**: Data structured for academic papers
- **Citation Ready**: Proper attribution and methodology documentation
- **Reproducibility**: All analyses documentd and replicable
- **Research Export**: PDF, Excel, BibTeX export functionality

#### **Educational Impact**
- **Knowledge Transfer**: Medical concepts accessible to broader audience
- **Learning Outcomes**: Measurable educational objectives achieved
- **Engagement**: >70% users explore multiple sections
- **Retention**: >60% return visits within 30 days

#### **Social Impact**
- **Reach**: Serving both professional and educational communities
- **Accessibility**: Universal design principles implemented
- **Inclusivity**: Multiple language support (ES/EN)
- **Sustainability**: Maintainable dual-mode architecture

---

## 🔧 **Testing Strategy**

### **Dual-Mode Testing Approach**

#### **Unit Testing (Jest + React Testing Library)**
```bash
# Run all dual-mode tests
npm run test:dual-mode

# Test professional mode components
npm run test:professional

# Test educational mode components
npm run test:educational

# Test mode switching logic
npm run test:mode-switching
```

#### **Integration Testing**
```typescript
// Integration test example
describe('Dual Mode Integration', () => {
  test('data consistency across mode switches', async () => {
    const { user } = renderDashboard();

    // Apply filters in professional mode
    await user.click(professionalFilter);

    // Switch to educational mode
    await user.click(modeToggle);

    // Verify data remains filtered appropriately
    expect(educationalView).toShowFilteredData();

    // Switch back and verify professional filters persist
    await user.click(modeToggle);
    expect(professionalFilter).toBeSelected();
  });
});
```

#### **Accessibility Testing (axe-core)**
```bash
# Automated accessibility testing
npm run test:a11y:professional
npm run test:a11y:educational
npm run test:a11y:mode-switching
```

#### **Performance Testing (Lighthouse)**
```bash
# Performance testing for both modes
npm run lighthouse:professional
npm run lighthouse:educational
npm run lighthouse:mode-switching
```

#### **User Testing Protocol**
1. **Professional User Testing**:
   - Medical professionals (5 participants)
   - Researchers (5 participants)
   - Academic staff (3 participants)

2. **Educational User Testing**:
   - Medical students (8 participants)
   - Educated public (7 participants)
   - Healthcare students (5 participants)

3. **Accessibility Testing**:
   - Screen reader users (3 participants)
   - Keyboard-only users (3 participants)
   - Users with cognitive disabilities (2 participants)

---

## 🚀 **Deployment Strategy**

### **Production Architecture**

#### **Infrastructure**
```yaml
# docker-compose.production.yml
version: '3.8'
services:
  preventia-dashboard:
    image: preventia-dashboard:dual-mode
    ports:
      - "80:80"
      - "443:443"
    environment:
      - NODE_ENV=production
      - REACT_APP_API_URL=https://api.preventia.ucompensar.edu.co
      - REACT_APP_MODE_ANALYTICS=enabled
    volumes:
      - ssl-certs:/etc/ssl/certs
    restart: unless-stopped

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
      - ssl-certs:/etc/ssl/certs
    depends_on:
      - preventia-dashboard
```

#### **Performance Optimizations**
- **Code Splitting**: Separate bundles for professional/educational modes
- **Service Worker**: Offline functionality and caching
- **CDN**: Static assets served via CDN
- **Image Optimization**: WebP format with fallbacks
- **Bundle Analysis**: Regular bundle size monitoring

#### **Monitoring & Analytics**
```typescript
// Analytics configuration
const AnalyticsConfig = {
  googleAnalytics: {
    trackingId: 'GA-UCOMPENSAR-PREVENTIA',
    customDimensions: {
      userMode: 'dimension1',
      institutionAffiliation: 'dimension2',
      accessibilityFeatures: 'dimension3'
    }
  },

  customAnalytics: {
    modeUsage: 'track professional vs educational usage',
    featureAdoption: 'track feature discovery and usage',
    learningOutcomes: 'track educational objective completion',
    researchUsage: 'track export and citation usage'
  }
};
```

---

## 📖 **References & Documentation**

### **Technical References**
- [React 18 Concurrent Features](https://react.dev/blog/2022/03/29/react-v18)
- [TanStack Query v5](https://tanstack.com/query/latest/docs/react/overview)
- [Tailwind CSS v3 Design System](https://tailwindcss.com/docs/utility-first)
- [React-Aria Accessibility](https://react-spectrum.adobe.com/react-aria/)
- [WCAG 2.1 AA Guidelines](https://www.w3.org/WAI/WCAG21/quickref/)

### **Medical UX References**
- [Medical Interface Design Principles](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC6371158/)
- [Healthcare Data Visualization Best Practices](https://www.healthit.gov/topic/usability-and-user-experience)
- [Accessible Medical Information Design](https://www.cdc.gov/healthliteracy/developmaterials/index.html)

### **Educational Design References**
- [Universal Design for Learning](https://www.cast.org/impact/universal-design-for-learning-udl)
- [Cognitive Load Theory in Interface Design](https://www.interaction-design.org/literature/article/cognitive-load-theory)
- [Medical Education Technology Standards](https://www.aamc.org/initiatives/meded/)

### **Related Documentation**
- [ADR-008: Medical UX/UI Design Strategy](../decisions/ADR-008-medical-ux-ui-design-strategy.md)
- [Medical Design System Specification](../product/design-system.md)
- [UX/UI Strategy Document](../product/ux-ui-strategy.md)
- [FastAPI Integration Guide](../api/services/nlp-api.md)

---

## 🎯 **Project Impact & Innovation**

### **Academic Innovation**
- **First Dual-Mode Medical Interface**: Pioneer implementation at UCOMPENSAR
- **Knowledge Translation**: Bridge between professional and educational contexts
- **Research Methodology**: Reproducible analytics with academic standards
- **Open Science**: Transparent methodology and data accessibility

### **Technical Innovation**
- **Adaptive Component Architecture**: Reusable dual-mode component system
- **Context-Aware UX**: Interface adapts to user expertise level
- **Performance Optimization**: Sub-3s load times for complex medical data
- **Accessibility Excellence**: WCAG 2.1 AA+ compliance across all modes

### **Social Impact**
- **Health Literacy**: Making medical research accessible to broader audience
- **Educational Equity**: Equal access to medical information regardless of expertise
- **Research Democratization**: Professional tools available to students and public
- **Institutional Excellence**: Showcasing UCOMPENSAR's commitment to innovation

### **Future Scalability**
- **Modular Architecture**: Easy extension to other medical domains
- **Multi-language Support**: Framework for additional language implementations
- **AI Integration**: Foundation for machine learning feature additions
- **Cross-platform**: Responsive design supports mobile and tablet usage

---

**Plan implementación preparado por**: Cristhian Fernando Moreno Manrique, UCOMPENSAR
**Estrategia validada por**: ADR-008 Medical UX/UI Design Strategy
**Implementación target**: 4 semanas comenzando 2025-07-08
**Revisión programada**: 2025-08-01 (post-deployment evaluation)

---

*Este plan implementa la primera interfaz dual-mode médica/educativa en proyectos UCOMPENSAR, maximizando el impacto de investigación a través de estrategia de público híbrido que mantiene rigor científico mientras genera valor educativo y social.*

#### **Day 1-2: Project Setup & Dual-Mode Design System**
```bash
# Setup Commands
npm create vite@latest preventia-dashboard --template react-ts
cd preventia-dashboard
npm install

# Dual-Mode Dependencies
npm install @tanstack/react-query @tanstack/react-query-devtools
npm install react-router-dom react-hook-form
npm install tailwindcss @tailwindcss/forms @tailwindcss/typography
npm install recharts react-leaflet leaflet
npm install lucide-react @heroicons/react
npm install axios clsx tailwind-merge
npm install @testing-library/react @testing-library/jest-dom vitest

# Dual-Mode Specific
npm install @floating-ui/react  # Medical definitions tooltips
npm install react-aria @axe-core/react  # Dual accessibility
npm install framer-motion  # Mode transitions
npm install react-hotkeys-hook  # Professional keyboard shortcuts
npm install @types/leaflet
```

**Deliverables Day 1-2:**
- ✅ Project initialized with dual-mode stack
- ✅ Tailwind dual-mode theme configured (professional + educational)
- ✅ Dual design system tokens implemented
- ✅ DualModeProvider context created
- ✅ ModeToggle component implemented
- ✅ Basic adaptive folder structure created
- ✅ TypeScript dual-mode types defined

#### **Day 3-4: Core Adaptive Components**
**Priority: AdaptiveKPICard + Dual Layout Foundation**

```typescript
// AdaptiveKPICard.tsx - Dual-mode metric display
interface AdaptiveKPICardProps {
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
  mode: 'professional' | 'educational';
  explanation?: string; // Educational mode explanation
  technicalDetails?: string; // Professional mode details
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
