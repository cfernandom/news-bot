# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

PreventIA News Analytics is an intelligent media monitoring system specialized in automated analysis of breast cancer news. It combines web scraping, NLP sentiment analysis, and data visualization with a React dashboard and comprehensive CLI tools.

**Key Architecture:**
- Microservices backend with FastAPI
- React + TypeScript frontend with Vite
- PostgreSQL database with Redis caching
- Docker containerization for development and production

## Essential Development Commands

### Backend (Python 3.13)

```bash
# Environment setup
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Testing
pytest                                    # Run all tests
pytest -m unit                          # Unit tests only
pytest -m integration                   # Integration tests only
pytest --cov=services --cov-report=html # Coverage report (85% required)

# Code quality
black .                                  # Format code
isort .                                  # Sort imports
flake8 .                                # Lint code
bandit .                                # Security scan

# CLI operations
./preventia-cli status                   # System health check
./preventia-cli scraper run-all          # Run all scrapers
./preventia-cli source list             # List news sources
./main.py                               # Run main pipeline
```

### Frontend (React + TypeScript)

```bash
# Development (from preventia-dashboard/)
npm install
npm run dev                             # Start dev server (port 5173)
npm run build                           # Production build
npm run preview                         # Preview production build

# Testing
npm run test                            # Run Vitest tests
npm run test:unit                       # Unit tests only
npm run test:integration                # Integration tests only
npm run test:e2e                        # End-to-end tests with Puppeteer
npm run test:coverage                   # Coverage report
npm run validate                        # Final validation

# Quality
npm run lint                            # ESLint
```

**Dashboard Access (Priority Order):**
- **🔥 HIGH PRIORITY - Legacy Interface:** `http://localhost:5173/` (main user interface, pink-blue theme)
- **🔥 HIGH PRIORITY - Admin Panel:** `http://localhost:5173/admin` (source administration, compliance)
- **🔄 LOW PRIORITY - Modern Dashboard:** `http://localhost:5173/dashboard` (has errors, future enhancement)

### Docker Development

```bash
# Full development environment
docker-compose up -d                    # Start all services
docker-compose logs -f api              # View API logs
docker-compose exec api bash            # Access API container

# Production build
docker-compose -f docker-compose.prod.yml up -d
```

## Project Structure

```
news_bot_3/
├── services/                   # Backend microservices
│   ├── api/                   # FastAPI REST API
│   ├── scraper/               # Web scraping (Beautiful Soup + Playwright)
│   ├── nlp/                   # Sentiment analysis (Spacy + VADER)
│   ├── data/                  # SQLAlchemy database layer
│   ├── copywriter/            # Newsletter generation
│   ├── decision_engine/       # Business logic
│   ├── orchestrator/          # Pipeline coordination
│   └── publisher/             # Content publishing
├── preventia-dashboard/        # React frontend
├── cli/                       # Command-line interface
├── tests/                     # Test suites (unit/integration/e2e)
├── scripts/                   # Automation scripts
└── config/                    # Configuration files
```

## Key Technologies

**Backend:** FastAPI, SQLAlchemy, PostgreSQL, Redis, Spacy, VaderSentiment, Beautiful Soup, Playwright, OpenAI API
**Frontend:** React 19, TypeScript 5.8, Vite, TanStack Query, Tailwind CSS, Recharts, Leaflet
**Testing:** pytest (Python), Vitest (JavaScript), Puppeteer (E2E)
**Tools:** Black, isort, ESLint, Docker, pre-commit hooks

## Testing Framework

- **Markers:** `unit`, `integration`, `e2e`, `performance`, `database`, `slow`
- **Coverage:** Minimum 85% required for services and scripts
- **Structure:** Tests organized by type in `tests/unit/`, `tests/integration/`, `tests/e2e/`
- **Frontend:** Vitest for unit/integration, Puppeteer for E2E validation

## Development Notes

- **Python version:** 3.13+ required
- **Code style:** Black formatting (88 char line length), isort for imports
- **Dashboard Architecture:** Multi-interface implementation
  - **🔥 PRIORITY 1 - Legacy:** Production-ready interface at `/` (pink-blue theme, Spanish, full functionality)
  - **🔥 PRIORITY 2 - Admin:** Source administration at `/admin` (compliance management, auth required)
  - **🔄 FUTURE - Modern:** Professional dashboard at `/dashboard` (medical design, has errors, enhancement)
- **API Compatibility:** Both modern (`/api/`) and legacy (`/api/v1/`) endpoints
- **Medical focus:** Specialized for breast cancer news analysis
- **CLI-first:** Comprehensive CLI tools for system management in `./preventia-cli`
- **Security:** Bandit scanning, pre-commit hooks, secrets detection

## Current Project Status (2025-07-14)

- **MVP Status:** 80% complete, ~12-15 days to functional MVP
- **✅ RESOLVED:** TypeScript errors fixed, build process working
- **Data Status:** 121 articles processed, 8 scrapers operational
- **Backend:** 95% functional (FastAPI + PostgreSQL + Redis)
- **Frontend:** 75% functional (legacy + admin interfaces priority)
- **Current Focus:** Legacy interface `/` and admin panel `/admin` functionality
- **Next Priority:** Complete admin panel integration and ensure legacy dashboard works perfectly

## Recent Key Findings

- **Architecture Reality:** News source administration system (not traditional pipeline)
- **Compliance-First:** Rigorous ethical/legal validation before any scraping
- **NLP Processing:** Batch/manual execution (not automatic post-scraping)
- **Scraper Generation:** Automated creation system fully implemented
- **Documentation:** `PROJECT_STATUS_ANALYSIS.md` contains comprehensive technical analysis

## Configuration

- **Environment:** Use `.env` files for local development
- **Database:** PostgreSQL with asyncpg driver
- **Cache:** Redis for performance optimization
- **AI:** OpenAI integration for advanced text processing
