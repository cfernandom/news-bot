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

### NLP Analytics Commands
- **Run sentiment analysis**: `python scripts/batch_sentiment_analysis.py`
- **Run topic classification**: `python scripts/batch_topic_classification.py`
- **Test sentiment analyzer**: `source venv/bin/activate && python tests/legacy_test_sentiment_analysis.py`
- **Analyze individual article**: Use `services.nlp.src.sentiment.get_sentiment_analyzer()` and `services.nlp.src.topic_classifier.get_topic_classifier()`

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

### Git Workflow Standards
- **Conventional Commits**: Use format `type(scope): description` (feat, fix, docs, test, chore)
- **Atomic Commits**: One logical change per commit, complete and testable
- **Branch Strategy**: `main` (production) ← `dev` (integration) ← `feature/name` (development)
- **Documentation**: Follow language usage standard (English for technical, Spanish for decisions)
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
- **FastAPI 0.115** - Modern async web framework (planned)
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

# 📊 Estado del Proyecto: CUMPLIMIENTO LEGAL COMPLETADO - Sistema Listo para Producción (2025-06-30)

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

## 🎯 Estado Actual del Sistema
**Status:** ✅ CUMPLIMIENTO LEGAL COMPLETADO - SISTEMA LISTO PARA PRODUCCIÓN
**Próximo paso recomendado:** 🚀 **FASE 3 - FastAPI Dashboard Implementation**

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

## Current Implementation Status

### ✅ Completed - FASE 1 & FASE 2
- PostgreSQL database with optimized analytics schema
- Hybrid ORM + raw SQL data layer  
- Docker containerization with health checks
- 4 scrapers migrados con Playwright integration
- **VADER sentiment analysis** with medical content specialization
- **Professional testing framework** (unit/integration/e2e/performance)
- **24 comprehensive tests** with 95% coverage and HTML reporting
- Complete documentation structure and usage guides
- **Git workflow profesional** con conventional commits, commits atómicos y branch strategy

### 🚀 Ready for FASE 3 - Dashboard Analytics
- FastAPI REST API endpoints implementation
- React dashboard frontend with sentiment visualizations
- Real-time WebSocket updates for live analytics
- Geographic and trending analysis expansion

### 📋 Pending Issues & Next Steps
- **Coverage Investigation**: 50 artículos sin procesar (47.2% pending sentiment analysis)
- **Topic Categorization**: Automatic medical topic classification implementation
- **Performance Optimization**: Batch processing parallelization

## Migration Notes

This system is transitioning from a newsletter generation bot to an analytics platform. Key changes:
- **No longer publishes to WordPress** - focus is on data analysis
- **PostgreSQL replaces file-based storage** - enables complex analytics
- **Analytics-first architecture** - optimized for dashboard and insights
- **Hybrid database approach** - performance + productivity

For historical context, see `docs/decisions/ADR-001-project-scope-change.md`.