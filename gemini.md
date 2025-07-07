# Gemini Project Brief: PreventIA News Analytics Platform

## 1. Project Overview

**Goal:** An intelligent media monitoring system specialized in the automated analysis of breast cancer news. It processes data from multiple sources using NLP to provide actionable insights.

**Current Status:** Phase 2 (Data Scraping and NLP Analysis) is complete. Phase 3 (FastAPI backend) is fully implemented and ready for frontend integration. Phase 4 (React-based visualization dashboard) has successfully completed Week 1, with core components and dual-mode system operational. The project is now preparing for production deployment, with export functionality fully implemented. The current work is being done on the `feature/legacy-prototype-rollback` branch.

## 2. Technology Stack

- **Backend:** Python 3.13+, FastAPI (planned)
- **Database:** PostgreSQL 16+ with SQLAlchemy 2.0 and asyncpg
- **NLP:** spaCy for preprocessing, VADER for sentiment analysis
- **Frontend:** React with Vite (planned)
- **Infrastructure:** Docker, Docker Compose
- **Testing:** pytest (unit, integration, E2E)
- **Development:** Pre-commit hooks for quality assurance.

## 3. Development Workflow & Standards

**Critical:** Adherence to the project's automated workflow is mandatory.

- **Git Commits:** Must follow the **Conventional Commits** specification.
  - **Prefixes:** `feat:`, `fix:`, `docs:`, `style:`, `refactor:`, `test:`, `chore:`.
  - **Structure:** A concise subject line, followed by an optional descriptive body.
  - **Example:** `feat(api): add endpoint for sentiment analysis results`

- **Pre-commit Hooks:** Hooks are configured and run automatically on `git commit`. They enforce:
  - **Formatting:** `black` and `isort`.
  - **Linting:** `flake8`.
  - **Security:** `gitleaks` for secret scanning.
  - **File Health:** `trailing-whitespace`, `end-of-file-fixer`.

- **Process:**
  1. Make changes.
  2. `git add .`
  3. `git commit -m "prefix(scope): message"`
  4. If hooks fail, they may auto-correct files. Simply `git add .` the corrected files and re-run the commit command.

## 4. Key Commands

- **Setup Environment:**
  ```bash
  python -m venv venv
  source venv/bin/activate
  pip install -r requirements.txt
  pre-commit install
  ```
- **Start Database:**
  ```bash
  docker compose up postgres -d
  ```
- **Run Tests:**
  ```bash
  pytest
  ```
- **Run Pipeline (Example):**
  ```bash
  python scripts/run_migrated_scrapers.py www.breastcancer.org
  python scripts/batch_sentiment_analysis.py
  ```

## 5. Project Structure Overview

```
preventia-news-bot/
├───services/              # Core microservices (data, scraper, nlp, api)
├───preventia-dashboard/   # React frontend application
├───tests/                 # Pytest tests (unit, integration, e2e)
├───scripts/               # Automation and operational scripts
├───docs/                  # Project documentation
├───legal/                 # Legal and compliance documents
├───.pre-commit-config.yaml # Pre-commit hook configurations
├───docker-compose.yml     # Docker configuration for local dev
└───requirements.txt       # Python dependencies
```
