# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

PreventIA News Analytics is an intelligent media monitoring system specialized in automated analysis of breast cancer news. It transforms unstructured data from multiple sources into actionable insights through natural language processing and interactive visualizations. The system has evolved from a newsletter bot to a comprehensive analytics platform.

## Key Commands

### Database Operations
- **Start PostgreSQL**: `docker compose up postgres -d`
- **Test database connection**: `python test_database.py` (requires virtual env)
- **Database shell**: `docker compose exec postgres psql -U preventia -d preventia_news`
- **View logs**: `docker compose logs postgres`

### Development & Execution
- **Setup virtual environment**: `python -m venv venv && source venv/bin/activate`
- **Install dependencies**: `pip install -r requirements.txt`
- **Run legacy pipeline**: `python main.py` (transitioning to analytics)
- **Docker full stack**: `docker compose up -d --build`
- **View all services**: `docker compose ps`

### Testing
- **Database tests**: `source venv/bin/activate && python test_database.py`
- **Check PostgreSQL health**: `docker compose exec postgres pg_isready -U preventia`

## Architecture Overview

The system follows a hybrid architecture combining data analytics with the existing modular microservices:

### New Analytics Architecture (Primary)
1. **Data Layer** (`services/data/`) - PostgreSQL with hybrid ORM + raw SQL approach
   - Database models with SQLAlchemy + Pydantic
   - Optimized schema for analytics queries
   - Connection pooling and health checks
2. **Collection Layer** (evolved `services/scraper/`) - Smart data extraction
3. **Processing Layer** (evolved `services/nlp/`) - NLP analysis + sentiment analysis
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
PostgreSQL Storage → NLP Analysis → Sentiment/Topic Classification → 
Analytics Aggregation → (Future: API → React Dashboard)
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
- **Testing**: Always run `python test_database.py` after database changes

### Adding New Features
- **New endpoints**: Plan for FastAPI in `services/api/` (future)
- **Analytics**: Extend `services/data/database/models.py` with new analytics models
- **NLP features**: Enhance `services/nlp/` for new analysis types

### Site-Specific Extractors
- **Basic extractors**: `services/scraper/src/extractors/`
- **Full-text extractors**: `services/scraper/fulltext/src/extractors/`
- **Follow existing patterns** when adding new sources
- **Test with database storage** instead of file output

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
- `test_database.py` - Comprehensive database testing suite
- `requirements.txt` - All dependencies with verified versions

### Database Layer
- `services/data/database/connection.py` - Hybrid connection manager
- `services/data/database/models.py` - SQLAlchemy + Pydantic models
- `services/data/database/migrations/001_initial_schema.sql` - Database schema

### Configuration
- `.env.template` - Configuration template with all variables
- `docker-compose.yml` - PostgreSQL + Redis + analytics service
- `DEPLOYMENT.md` - Deployment instructions

### Documentation
- `docs/README.md` - Documentation hub
- `docs/architecture/system-overview.md` - Complete system architecture
- `docs/development/setup/local-development.md` - Local setup guide
- `docs/decisions/` - Architecture Decision Records (ADRs)

## Current Implementation Status

### ✅ Completed
- PostgreSQL database with optimized analytics schema
- Hybrid ORM + raw SQL data layer
- Docker containerization with health checks
- Comprehensive testing suite
- Complete documentation structure

### 🔄 In Progress
- Migration of existing scrapers to new database
- Analytics pipeline implementation
- Sentiment analysis integration

### 📋 Planned
- FastAPI REST API endpoints
- React dashboard frontend
- Advanced analytics (geographic, trend analysis)
- Real-time WebSocket updates

## Migration Notes

This system is transitioning from a newsletter generation bot to an analytics platform. Key changes:
- **No longer publishes to WordPress** - focus is on data analysis
- **PostgreSQL replaces file-based storage** - enables complex analytics
- **Analytics-first architecture** - optimized for dashboard and insights
- **Hybrid database approach** - performance + productivity

For historical context, see `docs/decisions/ADR-001-project-scope-change.md`.