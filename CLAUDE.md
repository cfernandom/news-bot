# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

This is an autonomous news bot system for breast cancer medical news. It scrapes medical articles, analyzes them with NLP/LLM, and automatically publishes newsletters to WordPress. The system is containerized and runs on scheduled cron jobs.

## Key Commands

### Development & Execution
- **Run the main pipeline**: `python main.py` (requires .env file with API keys)
- **Run via shell script**: `./run_bot.sh` (logs to logs/run_bot.log)
- **Docker build and run**: `docker compose up -d --build`
- **View container logs**: `docker compose logs -f newsbot`
- **Manual execution in container**: `docker compose exec newsbot /app/run_bot.sh`

### Dependencies
- **Install Python dependencies**: `pip install -r requirements.txt`
- Uses Python 3.13+ with key packages: openai, beautifulsoup4, playwright, pydantic, python-dotenv

## Architecture Overview

The system follows a modular microservices architecture with these core components:

### Service Pipeline Flow
1. **Orchestrator** (`services/orchestrator/`) - Coordinates the entire pipeline
2. **Scraper** (`services/scraper/`) - Extracts articles from medical news sites
3. **Full-text Scraper** (`services/scraper/fulltext/`) - Extracts complete article content using site-specific extractors
4. **NLP Analyzer** (`services/nlp/`) - Analyzes content semantically using keywords
5. **Decision Engine** (`services/decision_engine/`) - Determines which articles to publish
6. **Copywriter** (`services/copywriter/`) - Multi-stage LLM content generation:
   - Structure Builder - Proposes newsletter structure
   - Article Selector - Chooses articles for each section  
   - Summary Generator - Creates detailed summaries
7. **Publisher** (`services/publisher/`) - Publishes to WordPress via REST API

### Key Models
- **Article** (`services/shared/models/article.py`) - Central data structure with title, published_at, summary, content, url
- Pydantic models used throughout for data validation

### Data Flow
```
External Sources → Scraper → NLP Analysis → Decision Engine → 
LLM Structure/Selection/Summary → Markdown → HTML → WordPress
```

## Development Guidelines

### Environment Configuration
- Required `.env` variables: OPENAI_API_KEY, WP_POSTS_ENDPOINT, WP_USER, WP_PASSWORD
- Scheduling: WEEKLY_DAY, WEEKLY_TIME, DAYS_INTERVAL

### Site-Specific Extractors
- Located in `services/scraper/src/extractors/` and `services/scraper/fulltext/src/extractors/`
- Each extractor handles a specific medical news website
- Follow existing patterns when adding new sources

### LLM Integration
- Uses OpenAI GPT-4.1-mini for content generation
- Prompts stored in `prompts/` directories within each copywriter service
- Temperature set to 0.1 for consistency

### Error Handling
- Pipeline continues with fallback summaries if full-text extraction fails
- Comprehensive logging throughout the pipeline
- Graceful degradation when external services are unavailable

## Important Files
- `main.py` - Entry point that loads environment and runs orchestrator
- `services/orchestrator/src/main.py` - Main pipeline logic (run_pipeline function)
- `requirements.txt` - Python dependencies
- `docker-compose.yml` - Container orchestration
- `run_bot.sh` - Shell wrapper with logging
- `DEPLOYMENT.md` - Detailed deployment instructions