# UX/UI Design Session - PreventIA News Analytics

**Hola, soy Cristhian Fernando Moreno Manrique, Product Owner & Lead Developer de PreventIA News Analytics (UCOMPENSAR).**

## **Quién Soy**

**Cristhian Fernando Moreno Manrique**
- Docente e Investigador, Fundación Universitaria Compensar (UCOMPENSAR), Bogotá
- Ingeniero Electrónico → Ingeniería de Sistemas → Product Development
- Desarrollador web 3 años → Docente universitario 1 año → Tech Lead PreventIA
- Email: cfmorenom@ucompensar.edu.co

## **Mi Enfoque de Diseño**

**Filosofía UX:**
- Diseño centrado en datos médicos y científicos
- Accesibilidad prioritaria para stakeholders académicos
- Diseño ético responsable para información de salud
- Estética profesional médica/académica
- Performance-first design (sub-3s load times)

**Experiencia en Diseño:**
- Interfaces web responsivas y accesibles
- Dashboards analytics con visualizaciones complejas
- Design systems consistentes
- UX research con stakeholders académicos/médicos

## **PreventIA News Analytics - Contexto del Proyecto**

### **Misión del Sistema**
Plataforma de intelligence médico que transforma noticias sobre cáncer de seno en insights accionables para investigación académica, toma de decisiones médicas y awareness pública.

### **Usuarios Target**
1. **Investigadores Académicos** (UCOMPENSAR, universidades)
2. **Profesionales Médicos** (oncólogos, mastólogos)
3. **Estudiantes de Medicina** (pregrado y posgrado)
4. **Autoridades de Salud Pública** (análisis de tendencias)
5. **Pacientes y Familiares** (información confiable)

### **Estado Técnico Actual**
- ✅ **106 artículos** procesados con sentiment analysis completo
- ✅ **4 scrapers** operativos (Breast Cancer Org, WebMD, CureToday, News Medical)
- ✅ **PostgreSQL analytics** con 100% coverage NLP
- ✅ **20+ FastAPI endpoints** operativos (< 5s response times)
- ✅ **Legal compliance** framework completo (GDPR, robots.txt, fair use)
- ✅ **Prototipo HTML funcional** (dashboard_v0.1.html) disponible

### **Dashboard Data Available**

**KPIs Disponibles:**
- Total artículos procesados: 106
- Distribución geográfica: 4 países (US, MX, CO, ES)
- Distribución idiomas: Inglés (64%) vs Español (36%)
- Análisis sentiment: Positivo/Neutro/Negativo con scores
- Categorización topics: 7 categorías médicas
- Fuentes más activas: WebMD, Breast Cancer Org, etc.

**Visualizaciones Disponibles:**
- Sentiment distribution (pie charts)
- Temporal trends (line charts)
- Geographic heatmaps (Leaflet maps)
- Topics by language (grouped bar charts)
- Weekly analytics evolution
- Source activity analysis

**Datos en Tiempo Real:**
- Nuevos artículos diarios
- Sentiment scoring automático
- Topic classification
- Geographic categorization
- Source reliability metrics

## **Design System Actual (del Prototipo)**

### **Paleta de Colores Médica/Académica**
```css
:root {
    --primary-pink: #F8BBD9;        /* Breast cancer awareness pink */
    --primary-blue: #4A90E2;        /* Medical trust blue */
    --light-gray: #F5F5F5;          /* Clean background */
    --dark-gray: #666666;           /* Professional text */
    --white: #FFFFFF;               /* Clean space */
    --gradient: linear-gradient(135deg, #F8BBD9 0%, #4A90E2 100%);

    /* Sentiment Colors */
    --positive: #d1fae5 / #065f46;  /* Medical positive green */
    --negative: #fef2f2 / #991b1b;  /* Alert red */
    --neutral: #f3f4f6 / #374151;   /* Neutral gray */
}
```

### **Typography Hierarchy**
- **Headers**: 3rem → 2.5rem → 1.5rem (clear hierarchy)
- **Body**: 1rem optimizado para lectura científica
- **Data labels**: 0.75rem para métricas
- **Font**: Arial (accesible, readable, medical standard)

### **Component Patterns Establecidos**
- **Cards**: Border-radius 15px + shadow médica profesional
- **Badges**: Color-coded sentiment + topic categorization
- **Tables**: Clean medical data presentation
- **Charts**: Professional medical visualization standards
- **Maps**: Geographic medical data overlay
- **Modals**: Article detail overlays

## **Arquitectura UX/UI Target**

### **Layout Principal**
```
┌─ Header (fixed) ─────────────────────────────────────┐
│ 🎗️ PreventIA | Navigation | User Profile           │
├─ Main Dashboard ─────────────────────────────────────┤
│ ┌─ KPI Cards Row ────────────────────────────────────┐ │
│ │ 📊 106 Articles │ 🌍 4 Countries │ 💬 Sentiment   │ │
│ └─────────────────────────────────────────────────────┘ │
│ ┌─ Filters Panel ─┐ ┌─ Main Content Area ──────────┐ │
│ │ 🔍 Country       │ │ 📈 Charts & Visualizations    │ │
│ │ 🗣️ Language      │ │ 🗺️ Geographic Map             │ │
│ │ 📅 Date Range    │ │ 📋 Articles Table             │ │
│ │ 🏷️ Topics        │ │ 📊 Analytics Panels          │ │
│ └──────────────────┘ └────────────────────────────────┘ │
└───────────────────────────────────────────────────────┘
```

### **User Journey Paths**
1. **Quick Overview** → KPI cards → Key insights
2. **Deep Analysis** → Filters → Specific visualizations → Detailed data
3. **Research Mode** → Articles table → Individual analysis → Export
4. **Monitoring** → Trends dashboard → Alerts → Regular reports

## **Design Challenges & Oportunidades**

### **Challenges Identificados**
1. **Medical Data Complexity**: Múltiples dimensiones (sentiment, geographic, temporal, topics)
2. **Bilingual Support**: Español + Inglés seamless integration
3. **Academic Credibility**: Visual authority for university presentation
4. **Accessibility**: WCAG compliance para instituciones educativas
5. **Performance**: Large datasets (106+ articles) need optimized rendering

### **Oportunidades de Excelencia**
1. **First-class Medical UX**: Diseño específico para profesionales médicos
2. **Data Storytelling**: Narrativa visual de trends del cáncer de seno
3. **Research Integration**: Export academic-ready reports y citations
4. **Real-time Intelligence**: Live updates de nuevas noticias/insights
5. **Educational Interface**: Designed for medical students y learning

## **Especificaciones Técnicas UX**

### **Performance Requirements**
- **Page Load**: < 3 segundos (critical para stakeholders médicos)
- **Data Visualization**: < 5s para complex charts (106+ articles)
- **Responsive**: Mobile-first médico-friendly
- **Accessibility**: WCAG 2.1 AA compliance mínimo

### **Frontend Tech Stack**
- **React 18** + TypeScript (type safety para datos médicos)
- **TanStack Query** (API state management optimizado)
- **Tailwind CSS** (design system implementation)
- **Recharts** (medical-grade data visualization)
- **React-Leaflet** (geographic medical data)
- **React Hook Form** (professional filters)

### **API Integration Pattern**
```typescript
// Design pattern para medical data
const { data: sentimentData, isLoading } = useQuery({
  queryKey: ['sentiment-distribution', filters],
  queryFn: () => api.getSentimentDistribution(filters),
  staleTime: 5 * 60 * 1000, // 5min cache médico-appropriate
});
```

## **Sesión UX/UI Request Template**

**Por favor ayúdame con [ESPECÍFICO_DESIGN_CHALLENGE]:**

### **Tipo de Sesión**
- [ ] **Component Design** - Diseñar componente específico
- [ ] **User Flow** - Optimizar journey de usuario
- [ ] **Visual System** - Refinar design system
- [ ] **Accessibility** - WCAG compliance review
- [ ] **Performance UX** - Optimización de experiencia
- [ ] **Medical UX Research** - Investigación específica usuarios médicos

### **Contexto Específico**
- **Target Users**: [Investigadores/Médicos/Estudiantes/Pacientes]
- **Use Case**: [Análisis diario/Investigación académica/Presentación/Export]
- **Data Scope**: [106 articles/Filtered subset/Real-time/Historical]
- **Device Context**: [Desktop profesional/Tablet clínico/Mobile responsivo]

### **Design Constraints**
- **Brand**: Medical authority + academic credibility
- **Timeline**: [Urgente/1 semana/2-3 semanas/Investigación exploratoria]
- **Technical**: React + FastAPI endpoints + 106 articles dataset
- **Compliance**: GDPR + medical data ethics + academic standards

### **Success Criteria**
- **Usability**: [Specific metrics]
- **Performance**: [Load times, interaction responsiveness]
- **Accessibility**: [WCAG level, specific needs]
- **Medical Impact**: [Clinical utility, research value]

### **Current Prototype Reference**
Tengo prototipo HTML funcional en `docs/assets/prototypes/dashboard_v0.1.html` con:
- 6 KPI cards funcionales
- 5 visualizaciones de datos
- Mapa geográfico interactivo
- Sistema de filtros
- Tabla de artículos completa
- Design system médico implementado

---

## **Examples de Requests Típicos**

### **Component Design**
```
"Necesito diseñar un ArticleCard component que muestre sentiment analysis de manera médicamente apropiada. Users: oncólogos que necesitan quick article evaluation. Data: title, summary, sentiment_score, topic_category, source_credibility."
```

### **User Flow Optimization**
```
"Optimizar el research workflow para investigadores académicos. Journey: entrada → filter setup → data analysis → export citations. Challenge: 106 articles es demasiado para scroll, necesito intelligent pagination + smart filtering."
```

### **Medical Data Visualization**
```
"Diseñar sentiment trends visualization que sea clínicamente meaningful. Data: weekly sentiment scores over time. Users: medical researchers tracking public opinion sobre breast cancer treatments. Need: professional medical chart standards."
```

### **Accessibility Implementation**
```
"WCAG 2.1 AA compliance review para dashboard completo. Specific focus: color contrast para sentiment badges, keyboard navigation para complex charts, screen reader optimization para data tables."
```

---

**Ready para sesión UX/UI específica. Incluye contexto médico, technical constraints, y prototype reference para optimal design guidance.**
