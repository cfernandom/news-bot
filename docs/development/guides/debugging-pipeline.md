---
version: "1.0"
last_updated: "2025-07-07"
maintainer: "Claude (Technical Director)"
status: "active"
language: "English"
---

# Debugging Pipeline Guide

Comprehensive guide for debugging issues in the PreventIA News Analytics pipeline, including common problems, diagnostic tools, and resolution strategies.

## 🎯 Overview

### Pipeline Components
1. **Data Collection**: Web scrapers and content extraction
2. **Data Processing**: NLP analysis and sentiment classification
3. **Data Storage**: PostgreSQL database operations
4. **API Layer**: FastAPI endpoints and responses
5. **Frontend**: React dashboard and visualizations
6. **Background Tasks**: Scheduled jobs and async processing

### Common Issue Categories
- **Scraper Failures**: Site changes, blocking, rate limiting
- **Database Issues**: Connection problems, query performance
- **NLP Processing**: Analysis errors, language detection
- **API Problems**: Timeouts, authentication, rate limits
- **Frontend Issues**: Data loading, visualization rendering
- **Performance**: Slow responses, memory usage, bottlenecks

## 🔧 Diagnostic Tools and Commands

### 1. System Health Checks

#### Quick Health Assessment
```bash
# Overall system status
curl http://localhost:8000/health

# Detailed health check
curl http://localhost:8000/health/detailed

# Database connectivity
docker compose exec postgres pg_isready -U preventia

# Redis connectivity
docker compose exec redis redis-cli ping

# Service status
docker compose ps
```

#### Performance Monitoring
```bash
# Container resource usage
docker stats

# System resources
htop
free -h
df -h

# Network connections
netstat -tulpn | grep :8000
```

### 2. Log Analysis Tools

#### Log Locations
```bash
# Application logs
tail -f logs/api/app.log
tail -f logs/scraper/scraper.log

# Database logs
docker compose logs postgres

# Nginx logs (production)
tail -f /var/log/nginx/access.log
tail -f /var/log/nginx/error.log

# Container logs
docker compose logs -f api
docker compose logs -f frontend
```

#### Structured Log Analysis
```bash
# Filter API errors
grep "ERROR" logs/api/app.log | tail -20

# Search for specific patterns
grep "sentiment analysis" logs/api/app.log | head -10

# Count error frequency
grep "ERROR" logs/api/app.log | cut -d' ' -f3 | sort | uniq -c

# Monitor logs in real-time with filtering
tail -f logs/api/app.log | grep -E "(ERROR|WARNING)"
```

### 3. Database Debugging

#### Connection Diagnostics
```sql
-- Check active connections
SELECT pid, usename, application_name, client_addr, state
FROM pg_stat_activity
WHERE state = 'active';

-- Check slow queries
SELECT query, mean_exec_time, calls, total_exec_time
FROM pg_stat_statements
ORDER BY mean_exec_time DESC
LIMIT 10;

-- Check table sizes
SELECT schemaname, tablename,
       pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename)) as size
FROM pg_tables
WHERE schemaname = 'public'
ORDER BY pg_total_relation_size(schemaname||'.'||tablename) DESC;
```

#### Data Quality Checks
```sql
-- Check for duplicate articles
SELECT content_hash, COUNT(*) as duplicates
FROM articles
GROUP BY content_hash
HAVING COUNT(*) > 1;

-- Check sentiment analysis coverage
SELECT
    sentiment_label,
    COUNT(*) as count,
    ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM articles), 2) as percentage
FROM articles
GROUP BY sentiment_label;

-- Check recent articles
SELECT id, title, published_at, sentiment_label, word_count
FROM articles
ORDER BY created_at DESC
LIMIT 10;
```

### 4. API Debugging Tools

#### Endpoint Testing
```bash
# Test authentication
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username": "test", "password": "test"}'

# Test analytics endpoints
curl -H "Authorization: Bearer $TOKEN" \
  http://localhost:8000/api/v1/analytics/sentiment

# Test with detailed timing
curl -w "@curl-format.txt" -o /dev/null -s \
  http://localhost:8000/api/v1/analytics/sentiment
```

#### Performance Profiling
```python
# Add to FastAPI for debugging
import time
from fastapi import Request

@app.middleware("http")
async def debug_middleware(request: Request, call_next):
    start_time = time.time()

    # Log request details
    print(f"🔍 {request.method} {request.url}")
    print(f"Headers: {dict(request.headers)}")

    response = await call_next(request)

    process_time = time.time() - start_time
    print(f"⏱️ Process time: {process_time:.3f}s")

    return response
```

## 🐛 Common Issues and Solutions

### 1. Scraper Failures

#### Issue: Selector Not Found
```
ERROR: CSS selector 'h1.article-title' not found on page
```

**Diagnosis:**
```bash
# Test selectors manually
python scripts/test_selectors.py example.com \
  --selector "h1.article-title" \
  --url "https://example.com/article/123"

# Debug with browser
python scripts/debug_scraper.py example.com --headless=false
```

**Solutions:**
```python
# 1. Update selectors in extractor
selectors = {
    'title': ['h1.article-title', 'h1.post-title', 'h1'],  # Fallback chain
    'content': ['.article-content', '.post-content', 'main']
}

# 2. Add wait conditions
await page.wait_for_selector('h1.article-title', timeout=10000)

# 3. Handle dynamic content
await page.wait_for_load_state('networkidle')
await page.wait_for_timeout(2000)
```

#### Issue: Rate Limiting/Blocking
```
ERROR: HTTP 429 Too Many Requests
ERROR: HTTP 403 Forbidden
```

**Diagnosis:**
```bash
# Check robots.txt
curl https://example.com/robots.txt

# Test with different user agents
curl -H "User-Agent: Mozilla/5.0..." https://example.com

# Check IP reputation
curl https://httpbin.org/ip
```

**Solutions:**
```python
# 1. Increase delays
CRAWL_DELAY = 5.0  # Increase from 2.0

# 2. Rotate user agents
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
]

# 3. Add proxy rotation (if necessary)
proxy_servers = ["proxy1:8080", "proxy2:8080"]
```

#### Issue: JavaScript Rendering Problems
```
ERROR: Content not loaded, blank page returned
```

**Diagnosis:**
```bash
# Test with Playwright manually
python -c "
import asyncio
from playwright.async_api import async_playwright

async def test():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()
        await page.goto('https://example.com')
        await page.screenshot(path='debug.png')
        print(await page.content())
        await browser.close()

asyncio.run(test())
"
```

**Solutions:**
```python
# 1. Add longer wait times
await page.wait_for_load_state('networkidle')
await page.wait_for_timeout(5000)

# 2. Wait for specific elements
await page.wait_for_selector('.article-content', state='visible')

# 3. Disable images for faster loading
context = await browser.new_context(
    user_agent="PreventIA-NewsBot/1.0",
    extra_http_headers={"Accept-Language": "en-US,en;q=0.9"}
)
await context.route("**/*.{png,jpg,jpeg,gif,svg,ico}", handler=lambda route: route.abort())
```

### 2. Database Issues

#### Issue: Connection Pool Exhausted
```
ERROR: asyncpg.exceptions.TooManyConnectionsError
```

**Diagnosis:**
```sql
-- Check connection count
SELECT COUNT(*) FROM pg_stat_activity;

-- Check connection limits
SHOW max_connections;

-- Check pool settings
SELECT name, setting FROM pg_settings WHERE name LIKE '%connection%';
```

**Solutions:**
```python
# 1. Increase pool size
DATABASE_CONFIG = {
    "pool_size": 20,
    "max_overflow": 30,
    "pool_timeout": 10,
    "pool_recycle": 3600
}

# 2. Proper connection management
async with db_manager.get_session() as session:
    # Use session here
    pass  # Connection automatically returned to pool

# 3. Close connections explicitly
await db_manager.close_all_sessions()
```

#### Issue: Slow Query Performance
```
ERROR: Query timeout after 30 seconds
```

**Diagnosis:**
```sql
-- Enable query logging
ALTER SYSTEM SET log_min_duration_statement = 1000;
SELECT pg_reload_conf();

-- Check missing indexes
SELECT schemaname, tablename, attname, n_distinct, correlation
FROM pg_stats
WHERE schemaname = 'public' AND n_distinct > 100;

-- Analyze query plans
EXPLAIN ANALYZE SELECT * FROM articles WHERE published_at > '2025-01-01';
```

**Solutions:**
```sql
-- 1. Add appropriate indexes
CREATE INDEX CONCURRENTLY idx_articles_published_sentiment
ON articles (published_at DESC, sentiment_label);

-- 2. Optimize queries
-- Instead of:
SELECT * FROM articles ORDER BY published_at DESC LIMIT 100;

-- Use:
SELECT id, title, published_at, sentiment_label
FROM articles
ORDER BY published_at DESC
LIMIT 100;

-- 3. Use pagination
SELECT * FROM articles
WHERE id > $last_id
ORDER BY id
LIMIT 50;
```

### 3. NLP Processing Issues

#### Issue: Sentiment Analysis Errors
```
ERROR: VADER sentiment analysis failed for article 123
```

**Diagnosis:**
```python
# Test sentiment analysis manually
from services.nlp.src.sentiment import get_sentiment_analyzer

analyzer = get_sentiment_analyzer()
text = "Test article content here..."
result = analyzer.analyze_sentiment(text, "Test Title")
print(result)
```

**Solutions:**
```python
# 1. Add error handling
try:
    sentiment_result = analyzer.analyze_sentiment(text, title)
except Exception as e:
    logger.error(f"Sentiment analysis failed: {e}")
    sentiment_result = {
        'sentiment_label': 'neutral',
        'confidence': 0.0,
        'error': str(e)
    }

# 2. Handle encoding issues
import unicodedata

def clean_text(text):
    # Normalize unicode
    text = unicodedata.normalize('NFKD', text)
    # Remove null bytes
    text = text.replace('\x00', '')
    # Limit length
    return text[:10000]

# 3. Validate input
def validate_text_input(text, title):
    if not text or len(text.strip()) < 10:
        raise ValueError("Text too short for analysis")
    if not title or len(title.strip()) < 3:
        raise ValueError("Title too short")
    return True
```

#### Issue: Language Detection Problems
```
ERROR: Could not detect language for article
```

**Diagnosis:**
```python
# Test language detection
import spacy
from langdetect import detect

text = "Sample article text..."
try:
    lang = detect(text)
    print(f"Detected language: {lang}")
except:
    print("Language detection failed")

# Test spaCy model
nlp = spacy.load("en_core_web_sm")
doc = nlp(text[:1000])  # Test with smaller sample
print(f"Language: {doc.lang_}")
```

**Solutions:**
```python
# 1. Multiple detection methods
def detect_language(text):
    methods = []

    # Method 1: langdetect
    try:
        from langdetect import detect
        lang1 = detect(text)
        methods.append(lang1)
    except:
        pass

    # Method 2: spaCy
    try:
        nlp = spacy.load("en_core_web_sm")
        doc = nlp(text[:500])
        lang2 = doc.lang_
        methods.append(lang2)
    except:
        pass

    # Method 3: keyword-based heuristics
    spanish_keywords = ['el', 'la', 'de', 'que', 'y', 'en', 'un']
    english_keywords = ['the', 'and', 'of', 'to', 'a', 'in', 'is']

    text_lower = text.lower()
    spanish_count = sum(1 for word in spanish_keywords if word in text_lower)
    english_count = sum(1 for word in english_keywords if word in text_lower)

    if english_count > spanish_count:
        methods.append('en')
    else:
        methods.append('es')

    # Return most common detection
    from collections import Counter
    return Counter(methods).most_common(1)[0][0] if methods else 'en'
```

### 4. API Performance Issues

#### Issue: Slow Response Times
```
ERROR: Request timeout after 30 seconds
```

**Diagnosis:**
```bash
# Profile API endpoints
curl -w "@curl-format.txt" -o /dev/null -s \
  "http://localhost:8000/api/v1/analytics/sentiment"

# Monitor database queries
grep "SLOW QUERY" logs/postgres.log

# Check Redis cache hit rate
redis-cli info stats | grep keyspace
```

**Solutions:**
```python
# 1. Add caching
from fastapi_cache import FastAPICache
from fastapi_cache.decorator import cache

@app.get("/api/v1/analytics/sentiment")
@cache(expire=300)  # Cache for 5 minutes
async def get_sentiment_analytics():
    # Heavy computation here
    pass

# 2. Optimize database queries
# Instead of N+1 queries:
for article in articles:
    article.keywords = await get_keywords(article.id)

# Use join:
articles_with_keywords = await session.execute(
    select(Article, ArticleKeyword)
    .join(ArticleKeyword)
    .where(Article.id.in_(article_ids))
)

# 3. Add pagination
@app.get("/api/v1/articles")
async def get_articles(page: int = 1, limit: int = 20):
    offset = (page - 1) * limit
    articles = await session.execute(
        select(Article)
        .offset(offset)
        .limit(limit)
        .order_by(Article.published_at.desc())
    )
    return articles.scalars().all()
```

### 5. Frontend Debugging

#### Issue: Data Not Loading
```
ERROR: Failed to fetch data from API
```

**Diagnosis:**
```javascript
// Check network requests in browser dev tools
// Add debugging to React components

useEffect(() => {
    console.log('🔍 Fetching analytics data...');

    fetchAnalytics()
        .then(data => {
            console.log('✅ Data received:', data);
            setAnalytics(data);
        })
        .catch(error => {
            console.error('❌ Fetch failed:', error);
            setError(error.message);
        });
}, []);
```

**Solutions:**
```typescript
// 1. Add error boundaries
class ErrorBoundary extends React.Component {
    constructor(props) {
        super(props);
        this.state = { hasError: false, error: null };
    }

    static getDerivedStateFromError(error) {
        return { hasError: true, error };
    }

    componentDidCatch(error, errorInfo) {
        console.error('React Error Boundary:', error, errorInfo);
    }

    render() {
        if (this.state.hasError) {
            return <div>Something went wrong: {this.state.error?.message}</div>;
        }
        return this.props.children;
    }
}

// 2. Add retry logic
const useApiData = (url: string) => {
    const [data, setData] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        let retries = 3;

        const fetchWithRetry = async () => {
            while (retries > 0) {
                try {
                    const response = await fetch(url);
                    if (!response.ok) throw new Error(`HTTP ${response.status}`);
                    const result = await response.json();
                    setData(result);
                    setError(null);
                    break;
                } catch (err) {
                    retries--;
                    if (retries === 0) {
                        setError(err.message);
                    } else {
                        await new Promise(resolve => setTimeout(resolve, 1000));
                    }
                }
            }
            setLoading(false);
        };

        fetchWithRetry();
    }, [url]);

    return { data, loading, error };
};

// 3. Add loading states
const Dashboard = () => {
    const { data, loading, error } = useApiData('/api/v1/analytics/sentiment');

    if (loading) return <LoadingSpinner />;
    if (error) return <ErrorMessage error={error} />;
    if (!data) return <NoDataMessage />;

    return <AnalyticsCharts data={data} />;
};
```

## 🔍 Debugging Workflows

### 1. Systematic Issue Investigation

#### Step-by-Step Debugging Process
```bash
# 1. Identify the scope
echo "🔍 Step 1: Identify the problem scope"
curl http://localhost:8000/health/detailed

# 2. Check recent logs
echo "📝 Step 2: Check recent logs"
tail -n 50 logs/api/app.log | grep ERROR

# 3. Verify dependencies
echo "🔗 Step 3: Verify dependencies"
docker compose ps
docker compose exec postgres pg_isready -U preventia
docker compose exec redis redis-cli ping

# 4. Test specific components
echo "🧪 Step 4: Test specific components"
python scripts/test_component.py --component=database
python scripts/test_component.py --component=nlp
python scripts/test_component.py --component=scraper

# 5. Performance check
echo "⚡ Step 5: Performance check"
docker stats --no-stream
```

### 2. Issue Reproduction

#### Create Minimal Test Cases
```python
# test_reproduction.py
import asyncio
import pytest
from services.nlp.src.sentiment import get_sentiment_analyzer

class TestIssueReproduction:

    async def test_sentiment_analysis_error(self):
        """Reproduce sentiment analysis error with specific text"""
        analyzer = get_sentiment_analyzer()

        # Problematic text that causes errors
        problematic_text = "Text that causes the error..."

        try:
            result = await analyzer.analyze_sentiment(problematic_text, "Test Title")
            assert result is not None
        except Exception as e:
            pytest.fail(f"Sentiment analysis failed: {e}")

    async def test_database_connection_issue(self):
        """Reproduce database connection issue"""
        from services.data.database.connection import db_manager

        try:
            result = await db_manager.execute_sql("SELECT 1")
            assert result is not None
        except Exception as e:
            pytest.fail(f"Database connection failed: {e}")
```

### 3. Performance Profiling

#### Memory Usage Analysis
```python
# memory_profiler.py
import psutil
import time
from memory_profiler import profile

@profile
def analyze_memory_usage():
    """Profile memory usage of heavy operations"""

    # Simulate heavy NLP processing
    from services.nlp.src.sentiment import get_sentiment_analyzer
    analyzer = get_sentiment_analyzer()

    # Process multiple articles
    for i in range(100):
        text = f"Sample article text {i} " * 100
        result = analyzer.analyze_sentiment(text, f"Title {i}")

        if i % 10 == 0:
            process = psutil.Process()
            memory_mb = process.memory_info().rss / 1024 / 1024
            print(f"Memory usage after {i} articles: {memory_mb:.1f} MB")

if __name__ == "__main__":
    analyze_memory_usage()
```

#### Database Query Analysis
```python
# query_profiler.py
import time
import asyncio
from services.data.database.connection import db_manager

async def profile_queries():
    """Profile database query performance"""

    queries = [
        ("Count articles", "SELECT COUNT(*) FROM articles"),
        ("Recent articles", "SELECT * FROM articles ORDER BY published_at DESC LIMIT 10"),
        ("Sentiment distribution", """
            SELECT sentiment_label, COUNT(*)
            FROM articles
            GROUP BY sentiment_label
        """),
        ("Heavy join", """
            SELECT a.title, ak.keyword, ak.relevance_score
            FROM articles a
            JOIN article_keywords ak ON a.id = ak.article_id
            WHERE a.published_at > NOW() - INTERVAL '30 days'
            ORDER BY ak.relevance_score DESC
            LIMIT 100
        """)
    ]

    for name, query in queries:
        start_time = time.time()
        try:
            result = await db_manager.execute_sql(query)
            execution_time = time.time() - start_time
            print(f"✅ {name}: {execution_time:.3f}s")
        except Exception as e:
            execution_time = time.time() - start_time
            print(f"❌ {name}: {execution_time:.3f}s - Error: {e}")

if __name__ == "__main__":
    asyncio.run(profile_queries())
```

## 🛠️ Debugging Tools and Scripts

### 1. Health Check Script

Create `scripts/health_check.py`:

```python
#!/usr/bin/env python3
"""
Comprehensive health check script for debugging
"""

import asyncio
import sys
import time
import aiohttp
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

from services.data.database.connection import db_manager

async def check_database():
    """Check database connectivity and basic operations"""
    try:
        # Test connection
        result = await db_manager.execute_sql("SELECT 1 as test")
        assert result[0]['test'] == 1

        # Test article count
        articles = await db_manager.execute_sql("SELECT COUNT(*) as count FROM articles")
        article_count = articles[0]['count']

        # Test recent articles
        recent = await db_manager.execute_sql(
            "SELECT COUNT(*) as count FROM articles WHERE published_at > NOW() - INTERVAL '7 days'"
        )
        recent_count = recent[0]['count']

        print(f"✅ Database: {article_count} total articles, {recent_count} recent")
        return True

    except Exception as e:
        print(f"❌ Database error: {e}")
        return False

async def check_api():
    """Check API endpoints"""
    endpoints = [
        "/health",
        "/api/v1/analytics/sentiment",
        "/api/v1/sources"
    ]

    base_url = "http://localhost:8000"
    results = []

    async with aiohttp.ClientSession() as session:
        for endpoint in endpoints:
            try:
                start_time = time.time()
                async with session.get(f"{base_url}{endpoint}") as response:
                    response_time = time.time() - start_time
                    if response.status == 200:
                        print(f"✅ API {endpoint}: {response.status} ({response_time:.3f}s)")
                        results.append(True)
                    else:
                        print(f"⚠️ API {endpoint}: {response.status} ({response_time:.3f}s)")
                        results.append(False)
            except Exception as e:
                print(f"❌ API {endpoint}: {e}")
                results.append(False)

    return all(results)

async def check_nlp():
    """Check NLP processing"""
    try:
        from services.nlp.src.sentiment import get_sentiment_analyzer

        analyzer = get_sentiment_analyzer()
        test_text = "This is a breakthrough in breast cancer treatment showing promising results."

        start_time = time.time()
        result = analyzer.analyze_sentiment(test_text, "Test Article")
        processing_time = time.time() - start_time

        if result and 'sentiment_label' in result:
            print(f"✅ NLP: Sentiment analysis working ({processing_time:.3f}s)")
            print(f"   Result: {result['sentiment_label']} (confidence: {result.get('confidence', 0):.2f})")
            return True
        else:
            print(f"❌ NLP: Invalid result format")
            return False

    except Exception as e:
        print(f"❌ NLP error: {e}")
        return False

async def main():
    """Run comprehensive health check"""
    print("🏥 Running comprehensive health check...\n")

    checks = [
        ("Database", check_database()),
        ("API", check_api()),
        ("NLP", check_nlp())
    ]

    results = []
    for name, check_coro in checks:
        print(f"🔍 Checking {name}...")
        result = await check_coro
        results.append(result)
        print()

    # Summary
    passed = sum(results)
    total = len(results)

    print(f"📊 Health Check Summary: {passed}/{total} checks passed")

    if passed == total:
        print("🎉 All systems healthy!")
        return 0
    else:
        print("⚠️ Some issues detected. Check logs for details.")
        return 1

if __name__ == "__main__":
    exit(asyncio.run(main()))
```

### 2. Log Analysis Script

Create `scripts/analyze_logs.py`:

```python
#!/usr/bin/env python3
"""
Log analysis tool for identifying patterns and issues
"""

import re
import sys
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path

def analyze_log_file(log_path: Path):
    """Analyze a single log file for patterns"""

    if not log_path.exists():
        print(f"❌ Log file not found: {log_path}")
        return

    print(f"📝 Analyzing {log_path}")

    errors = []
    warnings = []
    response_times = []
    endpoints = Counter()
    hourly_activity = defaultdict(int)

    with open(log_path, 'r') as f:
        for line_num, line in enumerate(f, 1):
            try:
                # Parse timestamp
                timestamp_match = re.search(r'(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})', line)
                if timestamp_match:
                    timestamp = datetime.strptime(timestamp_match.group(1), '%Y-%m-%d %H:%M:%S')
                    hour_key = timestamp.strftime('%H:00')
                    hourly_activity[hour_key] += 1

                # Parse log levels
                if 'ERROR' in line:
                    errors.append((line_num, line.strip()))
                elif 'WARNING' in line:
                    warnings.append((line_num, line.strip()))

                # Parse API endpoints
                endpoint_match = re.search(r'(GET|POST|PUT|DELETE) (/\S+)', line)
                if endpoint_match:
                    method, path = endpoint_match.groups()
                    endpoints[f"{method} {path}"] += 1

                # Parse response times
                time_match = re.search(r'(\d+\.?\d*)ms', line)
                if time_match:
                    response_times.append(float(time_match.group(1)))

            except Exception as e:
                print(f"⚠️ Error parsing line {line_num}: {e}")
                continue

    # Print analysis results
    print(f"\n📊 Analysis Results for {log_path.name}")
    print(f"   Total lines: {line_num}")
    print(f"   Errors: {len(errors)}")
    print(f"   Warnings: {len(warnings)}")

    if errors:
        print(f"\n❌ Recent Errors (last 5):")
        for line_num, error in errors[-5:]:
            print(f"   Line {line_num}: {error[:100]}...")

    if warnings:
        print(f"\n⚠️ Recent Warnings (last 3):")
        for line_num, warning in warnings[-3:]:
            print(f"   Line {line_num}: {warning[:100]}...")

    if endpoints:
        print(f"\n🔗 Top Endpoints:")
        for endpoint, count in endpoints.most_common(5):
            print(f"   {endpoint}: {count} requests")

    if response_times:
        avg_time = sum(response_times) / len(response_times)
        max_time = max(response_times)
        print(f"\n⏱️ Response Times:")
        print(f"   Average: {avg_time:.1f}ms")
        print(f"   Maximum: {max_time:.1f}ms")
        print(f"   Samples: {len(response_times)}")

    if hourly_activity:
        print(f"\n📈 Hourly Activity:")
        for hour in sorted(hourly_activity.keys()):
            count = hourly_activity[hour]
            bar = "█" * min(count // 10, 20)
            print(f"   {hour}: {count:4d} {bar}")

def main():
    """Analyze all log files"""

    log_dirs = [
        Path("logs/api"),
        Path("logs/scraper"),
        Path("logs/nlp")
    ]

    for log_dir in log_dirs:
        if log_dir.exists():
            for log_file in log_dir.glob("*.log"):
                analyze_log_file(log_file)
                print("-" * 50)
        else:
            print(f"⚠️ Log directory not found: {log_dir}")

if __name__ == "__main__":
    main()
```

## 📚 Related Documentation

- [Testing Strategy](../standards/testing-strategy.md)
- [Production Deployment](../../operations/deployment/production-deployment.md)
- [Performance Monitoring](../../operations/monitoring/metrics-dashboard.md)
- [API Documentation](../../api/services/)

---

**Debugging Principles:**
- **Systematic Approach**: Follow structured debugging workflows
- **Comprehensive Logging**: Log all important operations and errors
- **Performance Monitoring**: Track metrics and identify bottlenecks
- **Reproducible Testing**: Create test cases that isolate issues
- **Documentation**: Document solutions for future reference

**Last Updated**: 2025-07-07
**Next Review**: 2025-10-07
**Maintainer**: Claude (Technical Director)
