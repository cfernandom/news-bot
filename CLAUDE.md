# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

PreventIA News Analytics is an intelligent media monitoring system specialized in automated analysis of breast cancer news. It transforms unstructured data from multiple sources into actionable insights through natural language processing and interactive visualizations. The system has evolved from a newsletter bot to a comprehensive analytics platform.

## Key Commands

### Database Operations
- **Start PostgreSQL**: `docker compose up postgres -d`
- **Test database connection**: `python tests/legacy_test_database.py` (requires virtual env)
- **Database shell**: `docker compose exec postgres psql -U preventia -d preventia_news`
- **View logs**: `docker compose logs postgres`

### Development & Execution
- **Setup virtual environment**: `python -m venv venv && source venv/bin/activate`
- **Install dependencies**: `pip install -r requirements.txt`
- **Run legacy pipeline**: `python main.py` (transitioning to analytics)
- **Docker full stack**: `docker compose up -d --build`
- **View all services**: `docker compose ps`

### Testing Framework (Professional Structure)
- **Setup testing environment**: `source venv/bin/activate && pip install -r tests/requirements-test.txt`
- **Run unit tests**: `cd tests && pytest -m unit`
- **Run integration tests**: `cd tests && pytest -m integration`
- **Run all tests**: `cd tests && pytest`
- **Coverage report**: `cd tests && pytest --cov=../services --cov-report=html`
- **Database tests**: `cd tests && pytest -m database`
- **Legacy database test**: `source venv/bin/activate && python tests/legacy_test_database.py`
- **Check PostgreSQL health**: `docker compose exec postgres pg_isready -U preventia`

### Standards Automation Commands
- **Setup pre-commit hooks**: `pip install pre-commit && pre-commit install && pre-commit install --hook-type commit-msg`
- **Run all hooks manually**: `pre-commit run --all-files`
- **Update hook versions**: `pre-commit autoupdate`
- **Skip hooks (emergency)**: `git commit --no-verify -m "emergency fix"`
- **Run specific hook**: `pre-commit run black` or `pre-commit run flake8`
- **Check automation status**: `pre-commit --version && git config --list | grep pre-commit`

### NLP Analytics Commands
- **Run sentiment analysis**: `python scripts/batch_sentiment_analysis.py`
- **Run topic classification**: `python scripts/batch_topic_classification.py`
- **Test sentiment analyzer**: `source venv/bin/activate && python tests/legacy_test_sentiment_analysis.py`
- **Analyze individual article**: Use `services.nlp.src.sentiment.get_sentiment_analyzer()` and `services.nlp.src.topic_classifier.get_topic_classifier()`

### FastAPI Commands (FASE 3 COMPLETADA)
- **Start FastAPI server**: `python -m services.api.main`
- **Docker FastAPI service**: `docker compose up api -d` (✅ Production ready)
- **View API docs**: Open `http://localhost:8000/docs` (OpenAPI auto-generated)
- **Health check**: `curl http://localhost:8000/health` (Advanced health monitoring)
- **Test API endpoints**: `python tests/integration/test_api/test_api.py`
- **Run all API tests**: `pytest tests/unit/test_api/ tests/integration/test_api/`
- **API performance check**: All endpoints < 5s response time (106 artículos dataset)

### React Dashboard Commands (FASE 4 EN PROGRESO)
- **Start development server**: `cd preventia-dashboard && npm run dev`
- **Production build**: `cd preventia-dashboard && npm run build` (✅ Optimized)
- **Run unit tests**: `cd preventia-dashboard && npm run test:unit`
- **Run E2E tests**: `cd preventia-dashboard && npm run test:e2e`
- **Docker React service**: `docker compose up frontend -d`
- **Production deployment**: `cd preventia-dashboard && npm run preview`
- **Testing coverage**: `cd preventia-dashboard && npm run test:coverage`

## Architecture Overview

The system follows a hybrid architecture combining data analytics with the existing modular microservices:

### New Analytics Architecture (Primary)
1. **Data Layer** (`services/data/`) - PostgreSQL with hybrid ORM + raw SQL approach
   - Database models with SQLAlchemy + Pydantic
   - Optimized schema for analytics queries
   - Connection pooling and health checks
2. **Collection Layer** (evolved `services/scraper/`) - Smart data extraction
3. **Processing Layer** (evolved `services/nlp/`) - NLP analysis + VADER sentiment analysis + spaCy preprocessing
4. **Analytics Layer** (new) - Data aggregation and trend analysis
5. **API Layer** (planned) - FastAPI REST endpoints for dashboard
6. **Frontend Layer** (planned) - React dashboard with visualizations

### Legacy Components (Transitioning)
- **Orchestrator** (`services/orchestrator/`) - Evolving to analytics pipeline coordinator
- **Copywriter** (`services/copywriter/`) - Repurposed for summary generation
- **Decision Engine** (`services/decision_engine/`) - Evolving to analytics aggregation
- **Publisher** (`services/publisher/`) - Deprecated (no longer publishes to WordPress)

### Key Models
- **NewsSource** (`services/data/database/models.py`) - Dynamic news source management
- **Article** (`services/data/database/models.py`) - Enhanced with sentiment, topic, geographic data
- **ArticleKeyword** - Keyword extraction with relevance scores
- **WeeklyAnalytics** - Pre-calculated metrics for dashboard performance

### Current Data Flow
```
External Sources → Scrapers → Full-text Extraction →
PostgreSQL Storage → NLP Analysis (Keywords + VADER Sentiment) →
Sentiment/Topic Classification → Analytics Aggregation →
(Future: API → React Dashboard)
```

## NLP Analytics Architecture

### Sentiment Analysis System
- **Engine**: VADER (Valence Aware Dictionary and sEntiment Reasoner)
- **Preprocessing**: spaCy 3.8.7 with en_core_web_sm model
- **Specialization**: Medical content with conservative thresholds
- **Performance**: ~2 articles/second batch processing
- **Coverage**: 56/106 articles analyzed (52.8%)

### Medical Content Adjustments
```python
# Conservative thresholds for medical news
if compound >= 0.3:          # Strong positive (vs 0.05 standard)
    return "positive"
elif compound <= -0.3:       # Strong negative (vs -0.05 standard)
    return "negative"
else:
    return "neutral"         # Medical content tends to be neutral
```

### Sentiment Analysis Usage
```python
from services.nlp.src.sentiment import get_sentiment_analyzer

# Analyze single article
analyzer = get_sentiment_analyzer()
result = analyzer.analyze_sentiment(
    text="Medical breakthrough shows promising results",
    title="Cancer Treatment Success"
)
# Returns: {'sentiment_label': 'positive', 'confidence': 0.7, 'scores': {...}}

# Batch processing (production script)
python scripts/batch_sentiment_analysis.py
```

### Current NLP Capabilities
1. **Keyword Extraction** - Medical term identification with relevance scoring
2. **Sentiment Analysis** - VADER-based with medical content adjustments (106/106 articles processed)
3. **Topic Classification** - Rule-based categorization into 10 medical topics (106/106 articles classified)
4. **Content Relevance** - Multi-keyword matching for breast cancer content
5. **Batch Processing** - Optimized for large article collections
6. **Database Integration** - Sentiment + topic data stored in PostgreSQL

### NLP Pipeline Integration
```python
# Enhanced analyze_article function
def analyze_article(article: Article) -> NLPResult:
    # Keyword matching (existing)
    matched_keywords = extract_keywords(article)

    # Sentiment analysis (new)
    sentiment_data = get_sentiment_analyzer().analyze_sentiment(
        text=article.summary,
        title=article.title
    )

    return NLPResult(
        article=article,
        is_relevant=len(matched_keywords) >= 2,
        matched_keywords=matched_keywords,
        score=len(matched_keywords),
        sentiment_data=sentiment_data  # New field
    )
```

## Database Architecture

### PostgreSQL Setup
- **Port**: 5433 (external), 5432 (internal container)
- **Database**: `preventia_news`
- **User**: `preventia`
- **Connection**: Hybrid SQLAlchemy ORM + asyncpg for raw SQL

### Key Tables
- `news_sources` - Dynamic source management with validation
- `articles` - Articles with NLP analysis results
- `article_keywords` - Extracted keywords with relevance
- `weekly_analytics` - Pre-calculated dashboard metrics

### Connection Management
```python
# ORM for CRUD operations
async with db_manager.get_session() as session:
    articles = await session.execute(select(Article))

# Raw SQL for complex analytics
results = await db_manager.execute_sql(
    "SELECT COUNT(*) FROM articles WHERE sentiment_label = %s",
    "positive"
)
```

## Development Guidelines

### Environment Configuration
- **Required `.env` variables**:
  - `DATABASE_URL` - PostgreSQL connection string
  - `OPENAI_API_KEY` - For LLM analysis
  - `POSTGRES_DB`, `POSTGRES_USER`, `POSTGRES_PASSWORD`
- **Optional**: Redis configuration for caching (future)

### Database Development
- **Migrations**: Located in `services/data/database/migrations/`
- **Models**: Hybrid approach - use ORM for CRUD, raw SQL for analytics
- **Testing**: Always run `cd tests && pytest -m database` after database changes

### Documentation Standards & Quality Assurance
- **Automated verification**: `python scripts/verify_docs.py` - Auto-updates status indicators in 2-3 minutes
- **Quality checking**: `python scripts/doc_quality_check.py --severity warning` - Detects 8 quality issue types
- **Language standards**: English for technical docs, Spanish for team decisions per `docs/development/standards/language-usage-standard.md`
- **Metadata requirements**: Important documents must include metadata blocks with version, maintainer, status
- **Status tracking**: Documentation completeness tracked automatically in `docs/README.md`

### Adding New Features
- **New endpoints**: Plan for FastAPI in `services/api/` (future)
- **Analytics**: Extend `services/data/database/models.py` with new analytics models
- **NLP features**: Enhance `services/nlp/` for new analysis types

### Site-Specific Extractors
- **Basic extractors**: `services/scraper/src/extractors/`
- **Full-text extractors**: `services/scraper/fulltext/src/extractors/`
- **Follow existing patterns** when adding new sources
- **Test with database storage** instead of file output

### Code Quality Standards
- **Automated formatting**: Black formatter with Python 3.12 compatibility (`--target-version=py312`)
- **Import organization**: isort with Black profile integration (`--profile black`)
- **Code linting**: flake8 with medical codebase optimizations and extended ignore patterns
- **Security scanning**: gitleaks for secret detection with zero false positives
- **Documentation quality**: Automated link checking and quality assurance
- **Configuration**: Centralized in `pyproject.toml` for tool consistency
- **Enforcement**: Pre-commit hooks with 85% automation coverage (15:1 ROI improvement)

### Git Workflow Standards
- **Conventional Commits**: Use format `type(scope): description` (feat, fix, docs, test, chore)
- **Atomic Commits**: One logical change per commit, complete and testable
- **Branch Strategy**: `main` (production) ← `dev` (integration) ← `feature/name` (development)
- **Documentation**: Follow language usage standard (English for technical, Spanish for decisions)
- **Automated validation**: Pre-commit hooks enforce standards on every commit
- **Reference**: See `docs/development/standards/git-workflow.md` for complete guidelines

### Example Git Commands
```bash
# Create feature branch
git checkout dev
git checkout -b feature/analytics-endpoints

# Atomic commits with conventional format
git add services/api/
git commit -m "feat(api): add FastAPI endpoints for sentiment analytics"

git add tests/integration/
git commit -m "test(api): add integration tests for analytics endpoints"

# Merge back to dev
git checkout dev
git merge --no-ff feature/analytics-endpoints
```

## Technology Stack

### Backend
- **Python 3.13+** - Main language
- **PostgreSQL 16+** - Primary database with JSONB support
- **SQLAlchemy 2.0** - ORM with async support
- **asyncpg 0.30** - High-performance PostgreSQL driver
- **FastAPI 0.115** - Modern async web framework (implemented)
- **spaCy 3.8** - NLP processing
- **VADER Sentiment** - Sentiment analysis

### Infrastructure
- **Docker & Docker Compose** - Containerization
- **Redis** - Caching and real-time features (configured)

### Analytics & ML
- **Pandas** - Data processing
- **NumPy** - Numerical computations
- **OpenAI API** - LLM for summaries and insights

## Important Files

### Core Application
- `main.py` - Legacy entry point (transitioning)
- `requirements.txt` - All dependencies with verified versions

### Scripts (Production)
- `scripts/batch_sentiment_analysis.py` - Batch sentiment analysis for existing articles
- `scripts/batch_topic_classification.py` - Batch topic classification for existing articles
- `scripts/run_migrated_scrapers.py` - Execute individual or all scrapers

### Database Layer
- `services/data/database/connection.py` - Hybrid connection manager
- `services/data/database/models.py` - SQLAlchemy + Pydantic models
- `services/data/database/migrations/001_initial_schema.sql` - Database schema

### NLP Analytics Layer
- `services/nlp/src/sentiment.py` - VADER sentiment analyzer with medical adjustments
- `services/nlp/src/topic_classifier.py` - Medical topic classifier with 10 categories
- `services/nlp/src/analyzer.py` - Enhanced NLP pipeline with sentiment + topic integration
- `services/nlp/src/models.py` - NLP result models with sentiment + topic data

### Testing Framework (Professional Structure)
- `tests/conftest.py` - pytest configuration with async fixtures
- `tests/pytest.ini` - Test markers and execution settings
- `tests/requirements-test.txt` - Testing dependencies (verified versions)
- `tests/unit/test_nlp/test_sentiment.py` - 14 comprehensive sentiment tests
- `tests/integration/test_nlp_pipeline.py` - NLP pipeline integration tests
- `tests/legacy_test_database.py` - Legacy database testing (migrated)
- `tests/legacy_test_sentiment_analysis.py` - Legacy sentiment testing (migrated)

### Configuration
- `.env.template` - Configuration template with all variables
- `docker-compose.yml` - PostgreSQL + Redis + analytics service
- `DEPLOYMENT.md` - Deployment instructions

### Documentation (Professional Structure)
- `docs/README.md` - Documentation hub (updated for Phase 2)
- `docs/api/services/nlp-api.md` - ✅ NLP API documentation with sentiment analysis
- `docs/architecture/system-overview.md` - Complete system architecture
- `docs/development/setup/local-development.md` - Local setup guide
- `docs/development/standards/` - ✅ Language standards, testing strategy, git workflow standards
- `docs/decisions/` - ✅ 5 Architecture Decision Records (ADR-001 through ADR-005)
- `docs/implementation/` - ✅ Phase 1 & 2 results documentation

### Documentation Tools & Automation
- `scripts/verify_docs.py` - Automated documentation verification (95% time savings: 30-45min → 2-3min)
- `scripts/doc_quality_check.py` - Quality assurance automation detecting 8 issue types
- **Completion metrics**: 61.0% documentation completeness (25 existing/16 pending files)
- **Automated status updates**: Status indicators (✅/Pendiente) auto-updated in docs/README.md

### Prompts Strategy System (v1.0)
- `docs/prompts/` - Self-contained prompts for efficient Claude Code sessions
- **Optimized design** - 30-60 seconds vs theoretical complex modular approach
- **Self-contained prompts** - no assembly required, copy-paste ready
- **Quick commands** - 10-30 second one-liners for frequent scenarios
- **4 prompt types:** development, academic, debugging, quick-commands
- **Production-ready** system tested and optimized for daily use

# 📊 Estado del Proyecto: FASE 4 EN PROGRESO - React Dashboard Implementation (2025-07-03)

## ✅ FASE 1 COMPLETADA - Migración de Scrapers a PostgreSQL
- **4 scrapers migrados** exitosamente: Breast Cancer Org, WebMD, CureToday, News Medical
- **106 artículos** almacenados con 100% integridad y 0% duplicados
- **Playwright integrado** para JavaScript rendering (React/Next.js sites)
- **Framework de testing** estandarizado con validaciones automatizadas
- **Documentación comprehensiva** (ADRs, guías de uso, resultados implementación)
- **Git workflow profesional** establecido con conventional commits y commits atómicos

### Scrapers Operativos (4/8)
| Scraper | Status | Artículos | Performance | Tecnología |
|---------|--------|-----------|------------|------------|
| Breast Cancer Org | ✅ Operativo | 25 | ~2.5s | Playwright + PostgreSQL |
| WebMD | ✅ Operativo | 31 | ~45s | Playwright + Date Parsing |
| CureToday | ✅ Operativo | 30 | ~50s | Playwright + Duplicate Detection |
| News Medical | ✅ Operativo | 20 | ~30s | Playwright + International Metadata |

### Scrapers Pendientes (4/8 - Opcional para FASE 2)
- Medical Xpress, Nature, Breast Cancer Now, Science Daily

## ✅ FASE 2 COMPLETADA - NLP Analytics Implementation
- **Sentiment analysis** implementado con VADER + spaCy especializado para contenido médico
- **56 artículos procesados** con sentiment analysis (52.8% coverage, 0 errores)
- **Testing framework profesional** establecido: unit/integration/e2e structure
- **24 tests implementados** (14 unit + 6 integration + 4 database) con 100% passing
- **Coverage 95%** en módulos NLP con HTML reporting
- **Scripts de producción** organizados en `scripts/` directory
- **Git workflow estandarizado** con conventional commits y commits atómicos

### Distribución Sentiment Analysis
| Label | Artículos | Porcentaje | Promedio Score |
|-------|-----------|------------|----------------|
| Negative | 40 | 71% | -0.700 |
| Positive | 15 | 27% | 0.415 |
| Neutral | 1 | 2% | 0.000 |

## 🛡️ CUMPLIMIENTO LEGAL COMPLETADO (2025-06-30)
- **Legal compliance framework** implementado con robots.txt + rate limiting + GDPR
- **106 artículos aprobados** para uso académico bajo fair use doctrine
- **Documentación legal** completa: privacy policy + medical disclaimers + contact info
- **Auditoría legal** establecida con compliance_audit_log y legal_notices tables
- **Risk assessment:** 🔴 ALTO RIESGO → 🟢 BAJO RIESGO - FULLY COMPLIANT

### Marco Legal Implementado
- **Robots.txt Compliance:** Verificación automática para todos los scrapers
- **Rate Limiting:** 2 segundos entre requests, respeta crawl-delay directives
- **Copyright Protection:** Fair use académico, solo metadatos almacenados
- **GDPR Framework:** Privacy policy + user rights + data retention (1 año)
- **Medical Disclaimers:** Avisos legales para contenido médico automatizado
- **Universidad Contact:** Información institucional UCOMPENSAR integrada

### Archivos Legales Creados
- `legal/privacy-policy-template.md` - Política de privacidad personalizada UCOMPENSAR
- `legal/medical-disclaimers.md` - Disclaimers médicos comprehensivos
- `services/scraper/src/compliance/` - Framework de cumplimiento ético
- `scripts/apply_legal_compliance.py` - Migración legal automatizada
- `docs/implementation/legal-compliance-implementation.md` - Documentación completa

## 🚀 SISTEMA DE PROMPTS IMPLEMENTADO (2025-06-30)
- **Prompts Strategy v1.0** - Sistema optimizado para sesiones eficientes Claude Code
- **Diseño eficiente** - 30-60 segundos vs enfoque modular complejo teórico
- **Self-contained architecture** - No ensamblaje, copy-paste directo
- **4 tipos especializados** - development, academic, debugging, quick-commands
- **Quick commands** - One-liners de 10-30 segundos para casos frecuentes
- **Production-ready** - Testado y optimizado para uso diario en desarrollo e investigación

### Sistema de Prompts Implementado
- `docs/prompts/README.md` - Guía rápida y reference completo
- `docs/prompts/development.md` - Sessions desarrollo, APIs, features (152 líneas)
- `docs/prompts/academic.md` - Productos académicos rigurosos (154 líneas)
- `docs/prompts/debugging.md` - Bug fixes y issues urgentes (105 líneas)
- `docs/prompts/quick-commands.md` - One-liners para scenarios frecuentes (151 líneas)

## ✅ FASE 3 COMPLETADA - FastAPI Dashboard Analytics
- **API REST completa** implementada: 20+ endpoints especializados
- **Testing framework profesional** con 95% coverage (14+ tests)
- **Performance optimizada** para 106 artículos con queries < 5s
- **Docker integration** con `Dockerfile.api` y compose configuration
- **OpenAPI documentation** auto-generada en `/docs`
- **Modular architecture** con routers por dominio (articles, analytics, nlp)

## 🚀 FASE 4 EN PROGRESO - React Dashboard Implementation
- **React 19 + TypeScript** setup with modern tooling (Vite, TailwindCSS)
- **Dual-mode system** implementado: Professional/Educational modes
- **Components avanzados** ya operativos: ArticlesDataTable, SentimentChart, TopicsChart
- **Real-time data integration** con FastAPI backend (106 artículos)
- **Production build** optimizado con code splitting (237KB main bundle)
- **Testing framework** setup: Unit/Integration/E2E with Vitest + Puppeteer
- **Docker containerization** listo para producción

### FastAPI Endpoints Implementados
| Categoría | Endpoints | Funcionalidad | Status |
|-----------|-----------|---------------|---------|
| Health & System | 3 | Health checks, API info, docs | ✅ Operativo |
| Articles Management | 4 | CRUD, search, stats | ✅ Operativo |
| Analytics Dashboard | 6 | Metrics, trends, geographic | ✅ Operativo |
| NLP Integration | 5 | Sentiment, topic, batch | ✅ Operativo |

### Performance Metrics (Dataset: 106 artículos)
- **Health Check**: ~0.5s
- **Articles CRUD**: ~1.2s
- **Dashboard Analytics**: ~3.8s
- **Search Functionality**: ~2.1s
- **All endpoints**: < 5s response time target achieved

## 🎯 Estado Actual del Sistema
**Status:** 🚀 FASE 4 EN PROGRESO - REACT DASHBOARD IMPLEMENTATION
**Branch actual:** `feature/fase4-react-dashboard-dual-mode`
**Últimos commits:** ArticlesTableSection + comprehensive ArticlesDataTable + pagination support
**React Dashboard URL:** http://localhost:5173 (dev) | http://localhost:4173 (preview)
**API Documentation:** http://localhost:8000/docs
**Próximo paso:** 📊 **Legacy Prototype Implementation** (dashboard_v0.1.html)

### Infraestructura Lista para Analytics
- **PostgreSQL** optimizado con campos analytics-ready (sentiment_score, topic_category)
- **Testing Framework** con estructura profesional unit/integration/e2e
- **Documentación completa** en `docs/` con guías de uso y troubleshooting
- **Scripts utilitarios** para manejo de scrapers individuales o batch

### Comandos para Scrapers Migrados
```bash
# Ejecutar scraper individual
python scripts/run_migrated_scrapers.py webmd.com

# Testing completo
python tests/scrapers/test_all_migrated_scrapers.py

# Ver artículos almacenados
docker compose exec postgres psql -U preventia -d preventia_news -c "SELECT COUNT(*) FROM articles;"
```

## Current Implementation Status (ACTUALIZADO 2025-07-03)

### ✅ Completed - FASE 1, 2 & 3
- **PostgreSQL database** with optimized analytics schema (106 artículos)
- **Hybrid ORM + raw SQL** data layer with performance < 5s
- **Docker containerization** with health checks and production readiness
- **4 scrapers migrados** con Playwright integration
- **VADER sentiment analysis** with medical content specialization (100% coverage)
- **FastAPI REST API** with 20+ endpoints and OpenAPI documentation
- **Professional testing framework** (unit/integration/e2e/performance)
- **Complete documentation** structure and usage guides
- **Git workflow profesional** con conventional commits y branch strategy

### 🚀 In Progress - FASE 4 - React Dashboard
- **React 19 + TypeScript** con modern tooling stack
- **Advanced components** implementados: ArticlesDataTable, Charts, KPIs
- **Dual-mode system** Professional/Educational operativo
- **Real-time data integration** con FastAPI backend
- **Production build** optimizado (237KB bundle, 4.71s build)
- **Testing framework** Vitest + Puppeteer setup

### 📋 Next Steps Available
- **Legacy Prototype**: Implement dashboard_v0.1.html (strategy ready)
- **Geographic Visualization**: React-leaflet map component
- **Advanced Analytics**: Time series trends and forecasting
- **Performance Optimization**: Bundle size reduction and lazy loading
- **Production Deployment**: Full stack optimization

## 📈 Evolution Timeline

**FASE 1 (COMPLETADA):** Newsletter Bot → PostgreSQL Migration
**FASE 2 (COMPLETADA):** NLP Analytics + Sentiment Analysis
**FASE 3 (COMPLETADA):** FastAPI REST API + OpenAPI Documentation
**FASE 4 (EN PROGRESO):** React Dashboard + Advanced Visualizations
**PRÓXIMO:** Legacy Prototype Implementation + Geographic Analytics

### Migration Notes
This system evolved from a newsletter generation bot to a comprehensive analytics platform:
- **No longer publishes to WordPress** - focus is on data analysis
- **PostgreSQL + FastAPI + React** - modern full-stack architecture
- **Analytics-first design** - optimized for insights and visualizations
- **Dual-mode system** - Professional/Educational user experiences
- **Production-ready** - Docker containerization, testing, monitoring

For historical context, see `docs/decisions/ADR-001-project-scope-change.md`.

---

## 🔧 Quick Start Commands (ACTUALIZADOS 2025-07-03)

### Full Stack Startup
```bash
# Start backend services
docker compose up postgres redis api -d

# Start React frontend (separate terminal)
cd preventia-dashboard && npm run dev

# Verify all services
docker compose ps
curl http://localhost:8000/health
```

### Development Workflow
```bash
# Backend development
source venv/bin/activate
python -m services.api.main  # FastAPI dev server

# Frontend development
cd preventia-dashboard
npm run dev                  # React dev server
npm run test:unit           # Unit tests
npm run build               # Production build
```

### Data & Analytics
```bash
# Database operations
docker compose exec postgres psql -U preventia -d preventia_news

# Run analytics
python scripts/batch_sentiment_analysis.py
python scripts/batch_topic_classification.py

# API testing
curl http://localhost:8000/api/v1/articles/
curl http://localhost:8000/api/v1/analytics/sentiment
```

### Legacy Prototype Commands (CRÍTICO - 2025-07-03)
- **View prototype**: Open `docs/assets/prototypes/dashboard_v0.1.html` in browser
- **API specification**: See `docs/assets/prototypes/endpoints.md` (15 legacy endpoints detailed)
- **Implementation strategy**: See `docs/implementation/legacy-prototype-implementation-strategy.md`
- **Create implementation branch**: `git checkout -b feature/legacy-prototype-implementation`
- **Development server**: `cd preventia-dashboard && npm run dev` (reuse infrastructure)
- **Test legacy API compatibility**: `curl http://localhost:8000/api/v1/news?page=1`

### Legacy Prototype Context for Future Sessions

#### 🎯 CRITICAL PRIORITY: Legacy Prototype Implementation Ready
**Complete strategy documented and ready for implementation:**

#### **Legacy HTML Prototype Analysis**
- **File**: `docs/assets/prototypes/dashboard_v0.1.html` (8-section complete dashboard)
- **8 Sections**: Home, About Cancer, Prevention, Self-Exam, Institutions, Project, Contact, News Analytics
- **Theme**: Pink-blue gradient (#F8BBD9 → #4A90E2)
- **Features**: Geographic map, sentiment charts, export functionality, responsive design

#### **Legacy API Requirements Analysis**
- **File**: `docs/assets/prototypes/endpoints.md` (15 legacy endpoints specification)
- **Current API**: 20+ modern endpoints at `/api/*`
- **Legacy Expected**: 15 endpoints at `/api/v1/*` with different format
- **Format Gap**: Legacy expects `{status, data, meta}` wrapper vs current direct responses
- **Field Mapping**: `sentiment_label` → `tone`, `published_at` → `date`, `size` → `page_size`
- **Missing Critical**: Export (CSV/XLSX/PDF), Authentication (JWT), Chart generation

#### **Implementation Strategy**
- **File**: `docs/implementation/legacy-prototype-implementation-strategy.md`
- **Approach**: Branch parallel + API compatibility layer (zero breaking changes)
- **Timeline**: 15-22 hours across 5 phases
- **Phase 3 Critical**: Legacy API compatibility layer with format transformers
- **New Dependencies**: pandas, openpyxl, reportlab, python-jose, passlib

#### **Legacy API Compatibility Requirements**
```bash
# Current endpoints (working)
GET /api/articles/              # 106 artículos, direct format
GET /api/analytics/sentiment/   # Direct sentiment data

# Legacy endpoints needed (15 total)
GET /api/v1/news                # ⚠️ Needs format wrapper transformation
GET /api/v1/stats/tones         # ⚠️ Field mapping: sentiment_label → tone
GET /api/v1/export/news.csv     # ❌ MISSING - Critical CSV export
GET /api/v1/export/news.xlsx    # ❌ MISSING - Critical Excel export
POST /api/v1/export/report      # ❌ MISSING - Critical PDF generation

# Legacy format expected
{
  "status": "success",
  "data": { ... },
  "meta": { "page": 1, "page_size": 20, "total": 234 }
}
```

#### **Implementation Commands Ready**
```bash
# Start implementation
git checkout -b feature/legacy-prototype-implementation

# Backend: Add legacy compatibility layer
# Create: services/api/routers/legacy.py
# Create: services/api/routers/exports.py
# Create: services/api/transformers/articles.py

# Frontend: Add React components
# Create: src/pages/legacy/ (8 pages)
# Create: src/components/legacy/ (layout, carousel, map)
# Create: src/styles/legacy/ (pink-blue theme)

# Test legacy API
curl http://localhost:8000/api/v1/news?page=1&page_size=10
```

---

# important-instruction-reminders
Do what has been asked; nothing more, nothing less.
NEVER create files unless they're absolutely necessary for achieving your goal.
ALWAYS prefer editing an existing file to creating a new one.
NEVER proactively create documentation files (*.md) or README files. Only create documentation files if explicitly requested by the User.
