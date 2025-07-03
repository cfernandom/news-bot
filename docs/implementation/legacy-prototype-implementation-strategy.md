# Legacy Prototype Implementation Strategy

## 📋 Documento de Estrategia - Implementación Prototipo dashboard_v0.1.html

**Versión:** 1.0
**Fecha:** 2025-01-03
**Autor:** Claude Code Assistant
**Estado:** ✅ ESTRATEGIA APROBADA - LISTO PARA IMPLEMENTACIÓN

---

## 🎯 Objetivo

Implementar el prototipo legacy `docs/assets/prototypes/dashboard_v0.1.html` como una aplicación React funcional que aproveche toda la infraestructura existente (FastAPI + PostgreSQL + 106 artículos reales) sin modificar la branch actual `feature/fase4-react-dashboard-dual-mode`.

## 📊 Análisis de Situación Actual

### ✅ Infraestructura Disponible
- **FastAPI Backend:** 20+ endpoints operativos
- **PostgreSQL Database:** 106 artículos con sentiment/topic analysis
- **React Dashboard:** Components avanzados ya implementados
- **Testing Framework:** Unit/Integration/E2E tests establecidos
- **Docker Stack:** Containerización completa
- **Dual Mode System:** Professional/Educational modes funcionales

### 🎨 Análisis del Prototipo Legacy

#### Estructura Principal (8 Secciones)
1. **Inicio** - Página principal con carousel y hero
2. **Sobre el Cáncer** - Contenido educativo médico
3. **Prevención** - Guías y recomendaciones
4. **Autoexamen** - Tutorial paso-a-paso
5. **Instituciones** - Directorio médico
6. **Proyecto** - Metodología investigación
7. **Contacto** - Formulario y datos institucionales
8. **Noticias** - Dashboard analytics avanzado

#### Características Técnicas
- **Theme:** Gradient pink-blue (`#F8BBD9` → `#4A90E2`)
- **Navigation:** SPA con 8 páginas principales
- **Analytics:** Charts, geographic map, export functionality
- **Responsive:** Mobile-first design
- **Animations:** Carousel, scroll effects, hover transitions

---

## 🚀 Estrategia de Implementación

### **Opción Seleccionada: Branch Paralelo**

**Comando de inicio:**
```bash
git checkout -b feature/legacy-prototype-implementation
```

### **Ventajas de Esta Estrategia**
- ✅ **No modifica branch protegida** `feature/fase4-react-dashboard-dual-mode`
- ✅ **Reutiliza 100% infraestructura** existente (FastAPI, DB, componentes)
- ✅ **Aprovecha datos reales** (106 artículos con analytics)
- ✅ **Mantiene testing framework** y quality standards
- ✅ **Permite merge posterior** si se decide integrar
- ✅ **Desarrollo paralelo** sin conflictos

### **Alternativas Descartadas**
- ❌ **Modificar branch actual:** Riesgo de conflictos
- ❌ **Directorio independiente:** Duplicación innecesaria
- ❌ **Fork del repositorio:** Complejidad de sincronización

---

## 📦 Plan de Implementación Detallado

### **FASE 1: Core Structure Setup** (2-3 horas)

#### 1.1 Branch y Configuración Inicial
```bash
# Crear nueva branch
git checkout feature/fase4-react-dashboard-dual-mode
git checkout -b feature/legacy-prototype-implementation

# Verificar dependencies (ya instaladas)
npm list react-router-dom react-leaflet leaflet framer-motion
```

#### 1.2 Estructura de Archivos
```
src/
├── pages/legacy/              # Nuevas páginas prototipo
│   ├── LegacyHomePage.tsx    # Página principal
│   ├── AboutCancerPage.tsx   # Educación médica
│   ├── PreventionPage.tsx    # Prevención
│   ├── SelfExamPage.tsx      # Autoexamen
│   ├── InstitutionsPage.tsx  # Directorio
│   ├── ProjectPage.tsx       # Metodología
│   ├── ContactPage.tsx       # Contacto
│   └── NewsAnalyticsPage.tsx # Analytics (mejorado)
├── components/legacy/         # Componentes específicos
│   ├── LegacyLayout.tsx      # Layout principal
│   ├── LegacyHeader.tsx      # Header con gradient
│   ├── LegacyCarousel.tsx    # Carousel component
│   ├── GeographicMap.tsx     # Mapa react-leaflet
│   ├── ExportModal.tsx       # Export functionality
│   └── LegacyNavigation.tsx  # Sistema navegación
├── styles/legacy/            # Estilos específicos
│   ├── legacy-theme.css      # Variables CSS prototipo
│   └── legacy-components.css # Componentes específicos
└── routes/
    └── LegacyRoutes.tsx      # Routing sistema
```

#### 1.3 CSS Theme Configuration
```css
/* src/styles/legacy/legacy-theme.css */
:root {
  --legacy-primary-pink: #F8BBD9;
  --legacy-primary-blue: #4A90E2;
  --legacy-light-gray: #F5F5F5;
  --legacy-dark-gray: #666666;
  --legacy-white: #FFFFFF;
  --legacy-gradient: linear-gradient(135deg, #F8BBD9 0%, #4A90E2 100%);
}
```

#### 1.4 React Router Setup
```typescript
// App.tsx modification
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import LegacyRoutes from './routes/LegacyRoutes';

// Add legacy routes alongside existing dashboard
```

### **FASE 2: Páginas Educativas** (4-6 horas)

#### 2.1 Contenido Estático (2-3 horas)
- **AboutCancerPage:** Información médica sobre cáncer de mama
- **PreventionPage:** Guías de prevención y recomendaciones
- **SelfExamPage:** Tutorial autoexamen con pasos visuales
- **InstitutionsPage:** Directorio instituciones médicas Colombia
- **ProjectPage:** Metodología investigación UCOMPENSAR

#### 2.2 Componentes Interactivos (2-3 horas)
- **LegacyCarousel:** Hero carousel página principal
- **ContactPage:** Formulario funcional con validación
- **LegacyNavigation:** Sistema navegación responsivo

### **FASE 3: Legacy API Compatibility Layer** (4-6 horas)

#### 3.1 Legacy Router Implementation (2-3 horas)
```typescript
// services/api/routers/legacy.py - NEW FILE
@router.get("/api/v1/news")
async def get_news_legacy(page: int = 1, page_size: int = 20, ...):
    # Call current /api/articles/ endpoint
    current_response = await get_articles(page, page_size, ...)

    # Transform to legacy format
    return {
        "status": "success",
        "data": transform_articles_to_legacy(current_response.items),
        "meta": {"page": page, "page_size": page_size, "total": current_response.total}
    }
```

#### 3.2 Response Format Transformers (1-2 horas)
- **Format Converter:** Current response → Legacy format
- **Field Mapping:** `sentiment_label` → `tone`, `published_at` → `date`
- **Pagination Transform:** `size` → `page_size`, standardize meta object

#### 3.3 Export Functionality Implementation (2-3 horas)
```python
# services/api/routers/exports.py - NEW FILE
@router.get("/api/v1/export/news.csv")
async def export_news_csv(filters...):
    # Query articles with filters
    # Generate CSV using pandas
    # Return StreamingResponse

@router.post("/api/v1/export/report")
async def generate_pdf_report(request: ReportRequest):
    # Generate PDF using reportlab
    # Return download URL
```

#### 3.4 Enhanced Analytics Dashboard (2-3 horas)
- **GeographicMap:** Mapa interactivo con react-leaflet
- **ExportModal:** CSV/XLSX/PDF export functionality
- **Legacy Data Integration:** Connect with legacy-compatible endpoints

### **FASE 4: Legacy UI/UX Polish** (2-3 horas)

#### 4.1 Visual Design (1-2 horas)
- Aplicar theme pink-blue gradient
- Responsive design optimization
- Typography y spacing adjustments

#### 4.2 Animations & Interactions (1 hora)
- Scroll animations con Intersection Observer
- Hover effects y transitions
- Mobile menu functionality

---

## 🛠️ Especificaciones Técnicas

### **Dependencies Requeridas**

#### Frontend (React) - ✅ Instaladas
```json
{
  "react-router-dom": "^7.6.3",  // ✅ Instalado
  "react-leaflet": "^5.0.0",     // ✅ Instalado
  "leaflet": "^1.9.4",          // ✅ Instalado
  "framer-motion": "^12.22.0",   // ✅ Instalado
  "@types/leaflet": "^1.9.19"    // ✅ Instalado
}
```

#### Backend (FastAPI) - 🆕 Requeridas para Legacy Compatibility
```python
# Add to requirements.txt
pandas>=2.0.0          # Para CSV/Excel export
openpyxl>=3.1.0       # Para generación Excel
reportlab>=4.0.0      # Para generación PDF
python-jose>=3.3.0    # Para JWT tokens (auth)
passlib>=1.7.4        # Para password hashing
```

### **API Endpoints: Legacy vs Current Analysis**

#### Current FastAPI Implementation (20+ endpoints)
```typescript
// Articles Management
GET /api/articles/              // 106 artículos con paginación
GET /api/articles/{id}          // Detalles artículo individual
GET /api/articles/search/       // Búsqueda por contenido
GET /api/articles/stats/summary // Estadísticas artículos

// Analytics Dashboard
GET /api/analytics/dashboard           // Dashboard principal
GET /api/analytics/sentiment/trends   // Tendencias sentiment
GET /api/analytics/topics/distribution // Distribución temas
GET /api/analytics/geographic/distribution // Distribución geográfica
```

#### Legacy Requirements (15 endpoints)
```typescript
// From docs/assets/prototypes/endpoints.md
GET /api/v1/news                    // ⚠️ Formato diferente
GET /api/v1/news/{id}              // ⚠️ Formato diferente
GET /api/v1/stats/summary          // ⚠️ Estructura diferente
GET /api/v1/stats/topics           // ⚠️ Formato diferente
GET /api/v1/stats/tones            // ⚠️ Campo 'tone' vs 'sentiment_label'
GET /api/v1/stats/tones/timeline   // ⚠️ Formato diferente
GET /api/v1/stats/geo              // ⚠️ Formato diferente
GET /api/v1/export/news.csv        // ❌ FALTA - Critical gap
GET /api/v1/export/news.xlsx       // ❌ FALTA - Critical gap
POST /api/v1/export/report         // ❌ FALTA - PDF generation
POST /api/v1/auth/login            // ❌ FALTA - Authentication
```

### **Componentes Reutilizables**
```typescript
// Components ya implementados para reutilizar
ArticlesDataTable     // ✅ Table con filtros avanzados
SentimentChart       // ✅ Pie chart sentiment analysis
TopicsChart          // ✅ Bar chart categorías médicas
DualModeContext      // ✅ Professional/Educational modes
AdaptiveWrapper      // ✅ Responsive containers
ErrorBoundary        // ✅ Error handling
```

---

## 📊 Timeline y Recursos

### **Estimación Total: 15-22 horas (Actualizada con Legacy API)**

| Fase | Descripción | Tiempo | Prioridad |
|------|-------------|---------|-----------|
| **Fase 1** | Core Structure Setup | 2-3h | 🔴 Crítica |
| **Fase 2** | Páginas Educativas | 4-6h | 🟡 Alta |
| **Fase 3** | Legacy API Compatibility | 4-6h | 🔴 Crítica |
| **Fase 4** | Enhanced Analytics Dashboard | 3-4h | 🟡 Alta |
| **Fase 5** | UI/UX Polish | 2-3h | 🟢 Media |

### **Distribución Recomendada (Actualizada)**
- **Day 1:** Fase 1 completa + inicio Fase 2 (4-5h)
- **Day 2:** Fase 2 completa + inicio Fase 3 (Backend Legacy API) (5-7h)
- **Day 3:** Fase 3 completa + Fase 4 (Enhanced Analytics) (4-6h)
- **Day 4:** Fase 5 (UI/UX Polish) + Testing final (3-4h)

---

## ✅ Criterios de Éxito

### **Funcionalidad**
- [ ] 8 páginas principales navegables
- [ ] Analytics dashboard funcional con datos reales
- [ ] **Legacy API compatibility** (15 endpoints)
- [ ] **Export functionality completa** (CSV, XLSX, PDF)
- [ ] **Response format transformation** (legacy format)
- [ ] Responsive design mobile/desktop
- [ ] Geographic map interactivo
- [ ] Formulario contacto funcional

### **Calidad Técnica**
- [ ] Tests unitarios para nuevos componentes
- [ ] Integration tests para nuevas páginas
- [ ] Performance < 3s load time
- [ ] Accessibility compliance (WCAG 2.1)
- [ ] Cross-browser compatibility

### **Visual Design**
- [ ] Theme pink-blue gradient aplicado
- [ ] Animations y transitions suaves
- [ ] Typography consistente
- [ ] Spacing y layout correctos

---

## 📊 Legacy API Compatibility Analysis

### **Endpoint Mapping Strategy**

| Legacy Endpoint | Current Equivalent | Compatibility | Action Required |
|----------------|-------------------|---------------|------------------|
| `GET /api/v1/news` | `GET /api/articles/` | ⚠️ Format diff | Transform response |
| `GET /api/v1/news/{id}` | `GET /api/articles/{id}` | ⚠️ Format diff | Transform response |
| `GET /api/v1/stats/summary` | `GET /api/analytics/dashboard` | ⚠️ Partial | Restructure data |
| `GET /api/v1/stats/topics` | `GET /api/analytics/topics/distribution` | ⚠️ Format diff | Transform response |
| `GET /api/v1/stats/tones` | `GET /api/analytics/sentiment/trends` | ⚠️ Field names | Map `sentiment_label` → `tone` |
| `GET /api/v1/stats/geo` | `GET /api/analytics/geographic/distribution` | ⚠️ Format diff | Transform response |
| `GET /api/v1/export/news.csv` | ❌ Missing | 🔴 Critical | **NEW Implementation** |
| `GET /api/v1/export/news.xlsx` | ❌ Missing | 🔴 Critical | **NEW Implementation** |
| `POST /api/v1/export/report` | ❌ Missing | 🔴 Critical | **NEW Implementation** |
| `POST /api/v1/auth/login` | ❌ Missing | 🟡 Optional | **NEW Implementation** |

### **Response Format Transformation**

#### Legacy Expected Format:
```json
{
  "status": "success",
  "data": { ... },
  "meta": { "page": 1, "page_size": 20, "total": 234 }
}
```

#### Current Format:
```json
{
  "items": [...],
  "total": 234,
  "page": 1,
  "size": 20,
  "pages": 12
}
```

### **Field Mapping Requirements**
- `sentiment_label` → `tone`
- `published_at` → `date`
- `size` → `page_size`
- `country` → maintain but ensure ISO codes
- `topic_category` → `topic`

## 🚨 Riesgos y Mitigaciones

### **Riesgos Identificados**

| Riesgo | Probabilidad | Impacto | Mitigación |
|--------|--------------|---------|------------|
| **Conflictos git** | Baja | Alto | Branch paralelo independiente |
| **API compatibility issues** | Media | Alto | Extensive testing + format validation |
| **Export performance** | Media | Medio | Streaming responses + async processing |
| **Dependencies conflicts** | Baja | Medio | Usar versions compatibles |
| **Legacy format complexity** | Media | Medio | Transform layer + comprehensive tests |
| **Design inconsistencies** | Media | Bajo | CSS variables y design system |

### **Plan de Contingencia**
- **Backup branch:** Crear checkpoint antes de cada fase
- **Rollback strategy:** `git reset --hard` a commits estables
- **Alternative approach:** Directorio independiente si branch falla

---

## 📚 Recursos y Referencias

### **Documentación Interna**
- `docs/architecture/system-overview.md` - Arquitectura sistema
- `docs/api/services/api-endpoints.md` - Endpoints FastAPI
- `docs/implementation/fase3-fastapi-implementation.md` - FASE 3 resultados
- `preventia-dashboard/README.md` - Setup React dashboard

### **Prototipo Legacy**
- `docs/assets/prototypes/dashboard_v0.1.html` - Prototipo original
- **URL local:** `file:///path/to/dashboard_v0.1.html`

### **Testing References**
- `tests/README.md` - Testing framework guide
- `tests/e2e/final-validation.js` - E2E testing patterns

---

## 🔄 Proceso de Desarrollo

### **Git Workflow**
```bash
# 1. Crear branch
git checkout feature/fase4-react-dashboard-dual-mode
git checkout -b feature/legacy-prototype-implementation

# 2. Desarrollo incremental
git add .
git commit -m "feat(legacy): implement core structure setup"

# 3. Testing antes de push
npm run test:unit
npm run test:e2e
npm run build

# 4. Push y documentation
git push origin feature/legacy-prototype-implementation
```

### **Quality Gates**
1. **Cada commit:** Unit tests passing
2. **Cada fase:** Integration tests + manual validation
3. **Final:** E2E tests + performance validation
4. **Pre-merge:** Code review + documentation update

---

## 📞 Soporte y Contacto

### **Para Dudas Técnicas**
- **Claude Code Sessions:** Use docs/prompts/ strategy system
- **Debugging:** Use `docs/prompts/debugging.md` prompts
- **Development:** Use `docs/prompts/development.md` prompts

### **Para Decisiones Arquitectónicas**
- **ADR Process:** Create new ADR in `docs/decisions/`
- **Team Review:** Include stakeholders UCOMPENSAR
- **Documentation:** Update this strategy document

---

## 📝 Notas de Implementación

### **Comandos de Inicio Rápido**
```bash
# Iniciar implementación
git checkout -b feature/legacy-prototype-implementation
cd preventia-dashboard
npm run dev

# Validar setup
npm run test:unit
npm run lint
```

### **Archivos a Crear Primero**

#### Backend (Legacy API Compatibility)
1. `services/api/routers/legacy.py`
2. `services/api/routers/exports.py`
3. `services/api/transformers/articles.py`
4. `services/api/transformers/analytics.py`

#### Frontend (React Components)
5. `src/routes/LegacyRoutes.tsx`
6. `src/styles/legacy/legacy-theme.css`
7. `src/components/legacy/LegacyLayout.tsx`
8. `src/pages/legacy/LegacyHomePage.tsx`

### **Testing durante Desarrollo**
```bash
# Backend testing (Legacy API)
curl http://localhost:8000/api/v1/news?page=1&page_size=10
curl http://localhost:8000/api/v1/stats/summary
curl http://localhost:8000/api/v1/export/news.csv

# Frontend testing
npm run test:watch

# Validation periódica
npm run test:e2e
npm run validate

# API format validation
python -c "import requests; print(requests.get('http://localhost:8000/api/v1/news').json())"
```

---

## 🎯 Implementation Phases Summary

### **FASE 3 (NEW): Legacy API Compatibility - CRÍTICA**

#### Backend Implementation:
```python
# services/api/routers/legacy.py
from fastapi import APIRouter, Depends
from ..transformers.articles import transform_to_legacy_format

router = APIRouter(prefix="/api/v1")

@router.get("/news")
async def get_news_legacy(page: int = 1, page_size: int = 20, ...):
    # Call existing endpoint
    current_data = await get_articles_current(page, page_size, ...)

    # Transform to legacy format
    return {
        "status": "success",
        "data": transform_to_legacy_format(current_data.items),
        "meta": {
            "page": page,
            "page_size": page_size,
            "total": current_data.total
        }
    }
```

#### Export Implementation:
```python
# services/api/routers/exports.py
import pandas as pd
from fastapi.responses import StreamingResponse

@router.get("/export/news.csv")
async def export_csv(filters...):
    articles = await query_articles_with_filters(filters)
    df = pd.DataFrame(articles)

    output = io.StringIO()
    df.to_csv(output, index=False)
    output.seek(0)

    return StreamingResponse(
        io.BytesIO(output.getvalue().encode()),
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=news.csv"}
    )
```

**✅ ESTRATEGIA ACTUALIZADA - INCLUYENDO LEGACY API COMPATIBILITY**

**Próximo paso:** Ejecutar comandos de inicio y comenzar Fase 1 + Legacy API setup
