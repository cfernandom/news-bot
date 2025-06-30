# Quick Debugging Session - PreventIA News Analytics

**Hola, soy Cristhian Fernando Moreno, desarrollador PreventIA News Analytics (UCOMPENSAR). Tengo un issue técnico que necesita resolución rápida.**

## **System Context:**

**PreventIA:** Sistema analytics noticias cáncer de seno  
**Stack:** Python 3.13, FastAPI, PostgreSQL, Playwright, spaCy  
**Status:** Fase 3 - 106 artículos, compliance completo, API en desarrollo  
**Environment:** Docker Compose, testing 95% coverage

**Technical Setup:**
- PostgreSQL 16 running on port 5433
- Python 3.13 + asyncio + SQLAlchemy 2.0
- spaCy 3.8.7 + VADER sentiment analysis
- Playwright 1.51 para web scraping
- Testing framework: pytest con 95% coverage

**Current State:**
- ✅ 106 artículos procesados con sentiment analysis
- ✅ 4 scrapers operativos (Breast Cancer Org, WebMD, CureToday, News Medical)
- ✅ Legal compliance framework completo
- ✅ Database schema analytics-ready
- 🚧 FastAPI API en desarrollo (Fase 3)

---

## **🐛 Issue Details:**

**Component Affected:** [PERSONALIZAR - scraper/NLP/database/API/frontend/testing]

**Error Description:** [DESCRIBIR ERROR ESPECÍFICO]

**Priority:** [HIGH/MEDIUM/LOW]

**When It Started:** [Timestamp o cambios recientes]

**Reproduction Steps:**
1. [Paso 1]
2. [Paso 2]  
3. [Error occurs]

**Expected Behavior:** [Lo que debería pasar]

**Actual Behavior:** [Lo que está pasando]

**Error Logs/Stack Trace:**
```
[PEGAR LOGS DE ERROR AQUÍ]
```

**Recent Changes:** [Commits recientes, cambios de config, updates]

**Environment Info:**
```bash
# Database status
docker compose ps postgres

# Python environment  
source venv/bin/activate
python --version

# Git state
git status
git log --oneline -3
```

---

## **🔧 Common Debug Commands Available:**

```bash
# Check services
docker compose ps
docker compose logs postgres

# Database debugging  
docker compose exec postgres psql -U preventia -d preventia_news
SELECT COUNT(*) FROM articles;
SELECT * FROM compliance_dashboard;

# Python debugging
cd tests && pytest -v -s
python -c "import [MODULE]; print([MODULE].__version__)"

# Scraper debugging
python scripts/test_robots_checker.py
python scripts/run_migrated_scrapers.py [SCRAPER_NAME] --debug

# NLP debugging  
python -c "from services.nlp.src.sentiment import get_sentiment_analyzer; print('NLP OK')"
```

## **⚡ Request:**

**Need:** Quick diagnosis and fix for [COMPONENTE ESPECÍFICO]

**Time constraint:** [urgent/normal] - [context if urgent]

**Dependencies affected:** [any dependencies that might be impacted]

**System ready for investigation. What's the most likely cause and solution?**

---

**Quick debugging session ready. Let's solve this issue efficiently.**