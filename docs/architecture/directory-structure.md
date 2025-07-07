---
version: "1.0"
last_updated: "2025-07-04"
maintainer: "Claude (Technical Director)"
status: "active"
language: "English"
---

# Directory Structure - PreventIA News Analytics

This documentation records the complete directory structure and files of the NewsBot project transformed into an analytics system.

## 📁 Main Structure

```
news_bot_3/
├── 📄 CLAUDE.md                    # Claude Code guidance
├── 📄 README.md                    # Main project documentation
├── 📄 DEPLOYMENT.md               # Deployment guide
├── 📄 requirements.txt            # Python dependencies
├── 📄 main.py                     # Application entry point
├── 📄 test_database.py           # Database tests
├── 📄 .env.template              # Configuration template
├── 📄 docker-compose.yml         # Container orchestration
├── 📄 Dockerfile                 # Service image
├── 📄 entrypoint.sh              # Container entry script
├── 📄 run_bot.sh                 # Execution script
├── 📄 crontab.template           # Cron jobs template
│
├── 📁 docs/                      # Complete documentation
├── 📁 services/                  # System services
├── 📁 venv/                      # Python virtual environment
└── 📁 logs/                      # Application logs (generated)
```

## 📚 Documentation (`docs/`)

### Complete Structure
```
docs/
├── 📄 README.md                          # Central documentation hub
├── 📁 architecture/                      # System architecture
│   ├── 📄 system-overview.md            # General overview with diagrams
│   └── 📄 directory-structure.md        # This document
├── 📁 decisions/                         # Architecture Decision Records
│   ├── 📄 README.md                     # ADR index
│   ├── 📄 adr-template.md               # Template for new ADRs
│   ├── 📄 ADR-001-project-scope-change.md    # Scope change
│   └── 📄 ADR-002-database-architecture.md   # Database architecture
├── 📁 development/                       # Development guides
│   ├── 📁 setup/
│   │   └── 📄 local-development.md      # Complete local setup
│   ├── 📁 standards/                    # Code standards (pending)
│   └── 📁 guides/                       # Specific guides (pending)
├── 📁 conversations/                     # Technical conversations
│   ├── 📄 README.md                     # Conversation index
│   ├── 📁 templates/
│   │   └── 📄 conversation-template.md  # Template for new conversations
│   ├── 📄 2025-06-27_project-kickoff.md      # Initial session
│   └── 📄 2025-06-27_database-implementation.md  # Database implementation
├── 📁 operations/                        # Operations and deployment
│   ├── 📁 deployment/                   # (Structure ready, pending content)
│   ├── 📁 monitoring/
│   └── 📁 maintenance/
├── 📁 api/                              # API documentation
│   ├── 📁 services/                     # Internal APIs
│   └── 📁 external/                     # External APIs
├── 📁 product/                          # Product documentation
│   ├── 📁 requirements/                 # Functional requirements
│   ├── 📁 roadmap/                      # Roadmap and planning
│   └── 📁 research/                     # Market research
└── 📁 assets/                           # Documentation assets
    ├── 📁 diagrams/                     # Architecture diagrams
    ├── 📁 screenshots/                  # UI screenshots
    └── 📁 templates/                    # Various templates
```

## 🔧 Services (`services/`)

### Implemented Services
```
services/
├── 📁 data/                             # 🆕 New data layer
│   └── 📁 database/
│       ├── 📄 connection.py            # Hybrid connection manager
│       ├── 📄 models.py               # SQLAlchemy + Pydantic models
│       └── 📁 migrations/
│           └── 📄 001_initial_schema.sql    # Initial PostgreSQL schema
│
├── 📁 scraper/                          # ♻️ Reused/adapted
│   ├── 📁 src/
│   │   ├── 📄 main.py
│   │   ├── 📄 utils.py
│   │   └── 📁 extractors/              # 9 existing extractors
│   │       ├── 📄 www_breastcancer_org.py
│   │       ├── 📄 www_curetoday_com_tumor_breast.py
│   │       ├── 📄 www_medicalxpress_breast_cancer.py
│   │       └── 📄 ... (6 more)
│   └── 📁 fulltext/                    # Full-text extraction
│       └── 📁 src/
│           ├── 📄 fulltext_scraper.py
│           ├── 📄 registry.py
│           └── 📁 extractors/          # 8 full-text extractors
│               ├── 📄 breastcancernow_org.py
│               ├── 📄 www_nature_com.py
│               └── 📄 ... (6 more)
│
├── 📁 nlp/                             # ♻️ Reused - base for analytics
│   └── 📁 src/
│       ├── 📄 main.py
│       ├── 📄 analyzer.py
│       ├── 📄 keywords.py
│       └── 📄 models.py
│
├── 📁 orchestrator/                     # ♻️ Evolving for analytics
│   └── 📁 src/
│       ├── 📄 main.py                  # Main pipeline
│       └── 📄 utils.py
│
├── 📁 shared/                          # ♻️ Shared models
│   ├── 📁 models/
│   │   └── 📄 article.py              # Base Article model
│   └── 📁 utils/
│       └── 📄 dates.py
│
└── 📁 legacy/                          # 🔄 Services in transition
    ├── 📁 copywriter/                  # For newsletter (deprecated)
    │   ├── 📁 src/
    │   ├── 📁 article_selector/
    │   ├── 📁 structure_builder/
    │   └── 📁 summary_generator/
    ├── 📁 decision_engine/             # Will evolve to analytics
    │   └── 📁 src/
    └── 📁 publisher/                   # No longer publishes to WordPress
        └── 📁 src/
```

## 🎯 New Service Architecture (Roadmap)

### Future Services (to be implemented)
```
services/
├── 📁 api/                             # 🔮 FastAPI REST endpoints
│   ├── 📄 main.py                     # Main FastAPI app
│   ├── 📁 endpoints/
│   │   ├── 📄 articles.py             # Article CRUD
│   │   ├── 📄 sources.py              # Source management
│   │   ├── 📄 analytics.py            # Analytics metrics
│   │   └── 📄 exports.py              # Data export
│   ├── 📁 middleware/                 # Auth, CORS, rate limiting
│   └── 📁 schemas/                    # API Pydantic schemas
│
├── 📁 analytics/                       # 🔮 Analytics processing
│   ├── 📁 sentiment/                  # Sentiment analysis
│   ├── 📁 topic_classifier/           # Topic classification
│   ├── 📁 geographic/                 # Geographic analysis
│   └── 📁 aggregation/                # Aggregated metrics
│
├── 📁 collection/                      # 🔮 Optimized collection
│   ├── 📁 source_validator/           # Dynamic source validation
│   └── 📁 scheduler/                  # Intelligent scheduling
│
└── 📁 export/                          # 🔮 Export and reports
    ├── 📁 reports/                    # Report generation
    └── 📁 formats/                    # CSV, PDF, Excel export
```

## 📊 Configuration Files

### Main Configuration
```
├── 📄 .env.template                   # Configuration template (versioned)
├── 📄 .env                           # Local configuration (ignored)
├── 📄 docker-compose.yml             # Services: PostgreSQL, Redis, Analytics
├── 📄 requirements.txt               # 45+ verified dependencies
├── 📄 Dockerfile                     # Python image with dependencies
└── 📄 .gitignore                     # Ignored files
```

### Development Configuration
```
├── 📄 .dockerignore                  # Files ignored in build
├── 📄 .gitattributes                 # Git line endings
└── 📁 venv/                          # Virtual environment (ignored)
    ├── 📁 bin/                       # Python executables
    ├── 📁 lib/                       # Installed site packages
    └── 📁 include/                   # C headers
```

## 🔍 Files by Type

### Python (`.py`)
- **Total**: ~25 main files
- **New**: `connection.py`, `models.py`, `test_database.py`
- **Existing**: All original `services/` directory

### Documentation (`.md`)
- **Total**: 10 documentation files
- **Structure**: 8 organized directories
- **Templates**: 2 reusable templates

### Configuration
- **Docker**: `docker-compose.yml`, `Dockerfile`, `.dockerignore`
- **Python**: `requirements.txt`, `.env.template`
- **Shell**: `run_bot.sh`, `entrypoint.sh`
- **SQL**: `001_initial_schema.sql`

## 📈 Project Statistics

### Lines of Code
- **Database Layer**: ~650 lines (models, connection, migration)
- **Documentation**: ~2,000 lines
- **Configuration**: ~100 lines
- **Tests**: ~120 lines

### File Structure
- **📁 Directories**: 35+ organized directories
- **📄 Files**: 50+ active files
- **🔧 Configuration**: 8 config files
- **📚 Documentation**: 10 .md files

## 🎯 Implementation Status

### ✅ Completed
- ✅ **Database Layer**: PostgreSQL + hybrid SQLAlchemy
- ✅ **Documentation**: Complete structure and ADRs
- ✅ **Infrastructure**: Docker + PostgreSQL + Redis
- ✅ **Testing**: Database tests working

### 🔄 In Progress
- 🔄 **API Layer**: FastAPI endpoints (upcoming)
- 🔄 **Analytics**: Sentiment analysis (upcoming)
- 🔄 **Migration**: Adapting existing scrapers

### 📋 Pending
- 📋 **Frontend**: React dashboard
- 📋 **Advanced Analytics**: Topic classification, geographic analysis
- 📋 **Operations**: Monitoring, deployment automation

---

**Last updated**: 2025-06-27
**Structure version**: v2.0 (Analytics Architecture)
**Next update**: When FastAPI layer is implemented
