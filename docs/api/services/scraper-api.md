---
version: "1.0"
last_updated: "2025-07-07"
maintainer: "Claude (Technical Director)"
status: "active"
language: "English"
---

# Scraper API Documentation

FastAPI endpoints for web scraping management and automation in PreventIA News Analytics. Provides comprehensive control over scraper operations, source management, and automated scraper generation.

## 🚀 Quick Start

### Base URL
```
Development: http://localhost:8000/api/v1/scrapers
Production: https://api.preventia.com/api/v1/scrapers
```

### Authentication
```bash
# JWT token required for all endpoints
curl -H "Authorization: Bearer your-jwt-token" \
     http://localhost:8000/api/v1/scrapers/sources
```

### Health Check
```bash
curl http://localhost:8000/api/v1/scrapers/health
# Response: {"status": "healthy", "active_scrapers": 4, "last_run": "2025-07-07T12:00:00Z"}
```

## 🌐 Source Management Endpoints

### GET /sources
List all configured news sources with compliance status.

#### Parameters
```yaml
status: string (optional)
  - "active", "inactive", "pending", "failed"
  - Default: "active"

compliance_status: string (optional)
  - "compliant", "non_compliant", "pending_review"
  - Default: all statuses

page: int (optional)
  - Default: 1

limit: int (optional)
  - Default: 20, Max: 100
```

#### Response
```json
{
  "status": "success",
  "data": {
    "sources": [
      {
        "id": 1,
        "name": "Breast Cancer Organization",
        "base_url": "https://breastcancer.org",
        "status": "active",
        "compliance": {
          "is_compliant": true,
          "robots_txt_status": "compliant",
          "crawl_delay": 2.0,
          "last_check": "2025-07-07T10:00:00Z"
        },
        "performance": {
          "last_successful_run": "2025-07-07T11:30:00Z",
          "success_rate": 0.95,
          "avg_response_time": 1.2,
          "articles_collected": 25
        },
        "next_scheduled_run": "2025-07-07T14:00:00Z"
      }
    ],
    "pagination": {
      "page": 1,
      "limit": 20,
      "total": 4,
      "pages": 1
    }
  },
  "meta": {
    "timestamp": "2025-07-07T12:00:00Z",
    "total_sources": 4,
    "active_sources": 4,
    "compliance_rate": 1.0
  }
}
```

### POST /sources
Add a new news source with automatic compliance validation.

#### Request Body
```json
{
  "name": "Medical News Today",
  "base_url": "https://medicalnewstoday.com",
  "source_type": "news_site",
  "language": "en",
  "country": "US",
  "description": "General medical news with breast cancer coverage",
  "target_sections": [
    "/category/breast-cancer",
    "/tag/oncology"
  ],
  "scraping_config": {
    "max_articles_per_run": 50,
    "crawl_delay": 2.0,
    "respect_robots_txt": true,
    "user_agent": "PreventIA-NewsBot/1.0"
  }
}
```

#### Response
```json
{
  "status": "success",
  "data": {
    "source_id": 5,
    "name": "Medical News Today",
    "validation_result": {
      "compliance_check": "passed",
      "robots_txt_found": true,
      "required_delay": 2.0,
      "accessibility_score": 0.85
    },
    "estimated_setup_time": "5-10 minutes",
    "next_steps": [
      "Generate scraper code",
      "Run test extraction",
      "Deploy to production"
    ]
  }
}
```

### PUT /sources/{source_id}
Update existing source configuration.

#### Request Body
```json
{
  "status": "active",
  "scraping_config": {
    "max_articles_per_run": 30,
    "crawl_delay": 3.0
  },
  "target_sections": [
    "/category/breast-cancer",
    "/tag/oncology",
    "/news/cancer-research"
  ]
}
```

### DELETE /sources/{source_id}
Deactivate a news source (soft delete with compliance audit trail).

#### Response
```json
{
  "status": "success",
  "data": {
    "source_id": 5,
    "deactivation_timestamp": "2025-07-07T12:00:00Z",
    "final_stats": {
      "total_articles_collected": 156,
      "days_active": 45,
      "compliance_violations": 0
    },
    "data_retention": {
      "articles_preserved": true,
      "retention_period_days": 365
    }
  }
}
```

## 🤖 Automated Scraper Generation

### POST /generate
Generate a new scraper for a domain using AI-powered analysis.

#### Request Body
```json
{
  "domain": "healthline.com",
  "config": {
    "language": "en",
    "max_articles": 10,
    "focus_keywords": ["breast cancer", "oncology"],
    "respect_robots_txt": true,
    "test_mode": true
  }
}
```

#### Response
```json
{
  "status": "success",
  "data": {
    "generation_id": "gen_123e4567",
    "domain": "healthline.com",
    "analysis_result": {
      "cms_type": "custom",
      "complexity_score": 7.5,
      "requires_playwright": true,
      "detected_selectors": {
        "article_links": "a.article-link",
        "title": "h1.article-title",
        "content": "div.article-content",
        "date": "time.publish-date"
      }
    },
    "compliance_result": {
      "is_compliant": true,
      "robots_txt_compliant": true,
      "crawl_delay": 1.0,
      "legal_contact_verified": true
    },
    "scraper_code": "# Generated scraper code...",
    "template_used": "news_site_template",
    "deployment_status": "ready_for_testing",
    "estimated_performance": {
      "articles_per_minute": 2.5,
      "memory_usage": "50MB",
      "cpu_usage": "low"
    }
  }
}
```

### GET /generate/{generation_id}/status
Check the status of scraper generation process.

#### Response
```json
{
  "status": "success",
  "data": {
    "generation_id": "gen_123e4567",
    "status": "completed",
    "progress": 100,
    "steps_completed": [
      "domain_analysis",
      "compliance_check",
      "structure_analysis",
      "code_generation",
      "testing"
    ],
    "test_results": {
      "success_rate": 0.9,
      "articles_extracted": 9,
      "errors": 1,
      "performance_score": 8.5
    },
    "recommendation": "deploy_to_production"
  }
}
```

### POST /generate/batch
Generate scrapers for multiple domains in batch.

#### Request Body
```json
{
  "domains": [
    "cancer.gov",
    "mayoclinic.org",
    "webmd.com"
  ],
  "config": {
    "parallel_processing": true,
    "max_concurrent": 3,
    "timeout_minutes": 30
  }
}
```

#### Response
```json
{
  "status": "success",
  "data": {
    "batch_id": "batch_789abc",
    "total_domains": 3,
    "estimated_completion": "2025-07-07T12:30:00Z",
    "status_url": "/api/v1/scrapers/generate/batch/batch_789abc/status"
  }
}
```

## 🏃‍♂️ Scraper Execution

### POST /run/{source_id}
Execute a scraper for a specific source.

#### Request Body
```json
{
  "mode": "full",
  "max_articles": 50,
  "force_refresh": false,
  "dry_run": false,
  "notify_completion": true
}
```

#### Response
```json
{
  "status": "success",
  "data": {
    "run_id": "run_456def",
    "source_id": 1,
    "status": "started",
    "estimated_duration": "2-3 minutes",
    "progress_url": "/api/v1/scrapers/runs/run_456def/progress"
  }
}
```

### POST /run/all
Execute all active scrapers in sequence or parallel.

#### Request Body
```json
{
  "execution_mode": "parallel",
  "max_concurrent": 2,
  "skip_recent": true,
  "recent_threshold_hours": 6
}
```

### GET /runs
List recent scraper execution runs.

#### Parameters
```yaml
status: string (optional)
  - "running", "completed", "failed", "cancelled"

source_id: int (optional)
  - Filter by specific source

limit: int (optional)
  - Default: 20
```

#### Response
```json
{
  "status": "success",
  "data": {
    "runs": [
      {
        "run_id": "run_456def",
        "source_id": 1,
        "source_name": "Breast Cancer Organization",
        "status": "completed",
        "started_at": "2025-07-07T11:30:00Z",
        "completed_at": "2025-07-07T11:32:15Z",
        "duration_seconds": 135,
        "results": {
          "articles_found": 8,
          "articles_new": 3,
          "articles_updated": 1,
          "articles_skipped": 4,
          "errors": 0
        },
        "performance": {
          "avg_response_time": 1.1,
          "memory_peak": "45MB",
          "cpu_avg": 15.2
        }
      }
    ]
  }
}
```

### GET /runs/{run_id}
Get detailed information about a specific run.

#### Response
```json
{
  "status": "success",
  "data": {
    "run_id": "run_456def",
    "source_id": 1,
    "status": "completed",
    "timeline": [
      {
        "timestamp": "2025-07-07T11:30:00Z",
        "event": "started",
        "details": "Scraper initialization"
      },
      {
        "timestamp": "2025-07-07T11:30:05Z",
        "event": "fetching_articles",
        "details": "Found 15 article links"
      },
      {
        "timestamp": "2025-07-07T11:32:15Z",
        "event": "completed",
        "details": "Successfully processed 8 articles"
      }
    ],
    "articles_processed": [
      {
        "article_id": "123e4567",
        "title": "New Treatment Breakthrough",
        "status": "inserted",
        "processing_time": 2.3,
        "nlp_results": {
          "sentiment": "positive",
          "topics": ["treatment", "research"]
        }
      }
    ],
    "errors": [],
    "logs": [
      {
        "level": "INFO",
        "timestamp": "2025-07-07T11:30:00Z",
        "message": "Starting scraper for breastcancer.org"
      }
    ]
  }
}
```

### DELETE /runs/{run_id}
Cancel a running scraper execution.

#### Response
```json
{
  "status": "success",
  "data": {
    "run_id": "run_456def",
    "cancelled_at": "2025-07-07T11:31:00Z",
    "reason": "user_requested",
    "partial_results": {
      "articles_processed": 3,
      "articles_remaining": 5
    }
  }
}
```

## 📊 Performance Monitoring

### GET /performance
Get aggregated performance metrics for all scrapers.

#### Parameters
```yaml
time_range: string (optional)
  - "1h", "24h", "7d", "30d"
  - Default: "24h"

source_ids: array[int] (optional)
  - Filter by specific sources
```

#### Response
```json
{
  "status": "success",
  "data": {
    "summary": {
      "total_runs": 156,
      "success_rate": 0.94,
      "average_duration": 125.5,
      "total_articles_collected": 1240,
      "unique_articles": 1180
    },
    "by_source": [
      {
        "source_id": 1,
        "source_name": "Breast Cancer Organization",
        "runs": 45,
        "success_rate": 0.98,
        "avg_duration": 95.2,
        "articles_collected": 345,
        "performance_score": 9.2
      }
    ],
    "trends": {
      "success_rate_trend": "stable",
      "duration_trend": "improving",
      "article_volume_trend": "increasing"
    },
    "alerts": [
      {
        "source_id": 3,
        "type": "performance_degradation",
        "message": "Response time increased by 40% in last 24h",
        "severity": "medium"
      }
    ]
  }
}
```

### GET /performance/{source_id}
Get detailed performance metrics for a specific source.

#### Response
```json
{
  "status": "success",
  "data": {
    "source_id": 1,
    "performance_metrics": {
      "uptime_percentage": 99.2,
      "average_response_time": 1.15,
      "error_rate": 0.02,
      "articles_per_run": 8.5,
      "data_quality_score": 0.92
    },
    "historical_data": [
      {
        "date": "2025-07-01",
        "runs": 3,
        "success_rate": 1.0,
        "avg_duration": 90.5,
        "articles": 25
      }
    ],
    "bottlenecks": [
      {
        "component": "html_parsing",
        "avg_time": 0.5,
        "percentage_of_total": 45.2
      }
    ],
    "recommendations": [
      "Consider increasing crawl delay to improve stability",
      "Optimize CSS selectors for better performance"
    ]
  }
}
```

## 🔧 Configuration Management

### GET /config/templates
List available scraper templates.

#### Response
```json
{
  "status": "success",
  "data": {
    "templates": [
      {
        "name": "wordpress",
        "description": "Standard WordPress sites",
        "compatibility": 0.85,
        "features": ["article_list", "full_content", "metadata"]
      },
      {
        "name": "custom_medical",
        "description": "Medical news sites with specialized structure",
        "compatibility": 0.92,
        "features": ["medical_entities", "drug_names", "clinical_data"]
      }
    ]
  }
}
```

### GET /config/selectors/{source_id}
Get CSS selectors configuration for a source.

#### Response
```json
{
  "status": "success",
  "data": {
    "source_id": 1,
    "selectors": {
      "article_links": "a.post-title-link",
      "title": "h1.post-title",
      "content": "div.post-content",
      "author": "span.author-name",
      "publish_date": "time.publish-date",
      "tags": "a.tag-link"
    },
    "validation_results": {
      "title": {"success_rate": 0.98, "last_validated": "2025-07-07T10:00:00Z"},
      "content": {"success_rate": 0.95, "last_validated": "2025-07-07T10:00:00Z"}
    },
    "auto_update_enabled": true
  }
}
```

### PUT /config/selectors/{source_id}
Update CSS selectors for a source.

#### Request Body
```json
{
  "selectors": {
    "title": "h1.article-title",
    "content": "div.article-body"
  },
  "validate_immediately": true
}
```

## 🛡️ Compliance and Legal

### GET /compliance
Get overall compliance status across all sources.

#### Response
```json
{
  "status": "success",
  "data": {
    "compliance_summary": {
      "total_sources": 4,
      "compliant_sources": 4,
      "compliance_rate": 1.0,
      "last_audit": "2025-07-07T09:00:00Z"
    },
    "compliance_checks": [
      {
        "check_type": "robots_txt",
        "passing_sources": 4,
        "failing_sources": 0
      },
      {
        "check_type": "rate_limiting",
        "passing_sources": 4,
        "failing_sources": 0
      },
      {
        "check_type": "legal_contact",
        "passing_sources": 4,
        "failing_sources": 0
      }
    ],
    "upcoming_reviews": [
      {
        "source_id": 2,
        "review_date": "2025-07-14T00:00:00Z",
        "review_type": "quarterly_compliance"
      }
    ]
  }
}
```

### GET /compliance/{source_id}
Get detailed compliance information for a specific source.

#### Response
```json
{
  "status": "success",
  "data": {
    "source_id": 1,
    "compliance_status": "compliant",
    "last_check": "2025-07-07T09:00:00Z",
    "checks": {
      "robots_txt_compliant": true,
      "rate_limiting_respected": true,
      "legal_contact_verified": true,
      "terms_of_service_acceptable": true,
      "gdpr_compliant": true
    },
    "crawl_policies": {
      "required_delay": 2.0,
      "allowed_user_agents": ["*"],
      "restricted_paths": ["/admin", "/private"],
      "request_rate_limit": "30/minute"
    },
    "audit_trail": [
      {
        "date": "2025-07-07T09:00:00Z",
        "check_type": "automated_review",
        "result": "passed",
        "details": "All compliance checks successful"
      }
    ]
  }
}
```

### POST /compliance/audit
Trigger a comprehensive compliance audit.

#### Request Body
```json
{
  "audit_type": "full",
  "sources": [1, 2, 3, 4],
  "include_legal_review": true,
  "generate_report": true
}
```

## 🔍 Debugging and Troubleshooting

### GET /debug/{source_id}
Get debugging information for scraper issues.

#### Response
```json
{
  "status": "success",
  "data": {
    "source_id": 1,
    "last_error": {
      "timestamp": "2025-07-06T15:30:00Z",
      "error_type": "selector_not_found",
      "message": "CSS selector 'h1.title' not found on page",
      "url": "https://example.com/article/123",
      "stack_trace": "..."
    },
    "selector_validation": {
      "title": {"found": true, "count": 1},
      "content": {"found": false, "count": 0},
      "date": {"found": true, "count": 1}
    },
    "page_analysis": {
      "status_code": 200,
      "load_time": 2.3,
      "page_size": "245KB",
      "javascript_required": true,
      "detected_changes": [
        "New CSS class structure detected",
        "Article layout modified"
      ]
    },
    "suggested_fixes": [
      "Update content selector to 'div.article-body'",
      "Enable JavaScript rendering with Playwright"
    ]
  }
}
```

### POST /debug/test-selectors
Test CSS selectors against a specific URL.

#### Request Body
```json
{
  "url": "https://breastcancer.org/news/research/breakthrough-treatment",
  "selectors": {
    "title": "h1.post-title",
    "content": "div.post-content",
    "date": "time.publish-date"
  }
}
```

#### Response
```json
{
  "status": "success",
  "data": {
    "url": "https://breastcancer.org/news/research/breakthrough-treatment",
    "results": {
      "title": {
        "found": true,
        "count": 1,
        "sample": "Breakthrough Treatment Shows 95% Success Rate"
      },
      "content": {
        "found": true,
        "count": 1,
        "sample": "Researchers at Johns Hopkins have developed..."
      },
      "date": {
        "found": true,
        "count": 1,
        "sample": "2025-07-06T14:30:00Z"
      }
    },
    "page_info": {
      "status_code": 200,
      "final_url": "https://breastcancer.org/news/research/breakthrough-treatment",
      "load_time": 1.2
    }
  }
}
```

## 📚 Integration Examples

### Python Client Example
```python
import httpx

class ScraperAPI:
    def __init__(self, base_url, token):
        self.base_url = base_url
        self.headers = {"Authorization": f"Bearer {token}"}

    async def run_scraper(self, source_id, max_articles=None):
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/run/{source_id}",
                json={"max_articles": max_articles},
                headers=self.headers
            )
            return response.json()

    async def get_performance(self, time_range="24h"):
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.base_url}/performance?time_range={time_range}",
                headers=self.headers
            )
            return response.json()

# Usage
api = ScraperAPI("http://localhost:8000/api/v1/scrapers", "your-token")
result = await api.run_scraper(1, max_articles=20)
performance = await api.get_performance("7d")
```

### JavaScript/Node.js Example
```javascript
class ScraperAPI {
  constructor(baseUrl, token) {
    this.baseUrl = baseUrl;
    this.headers = { 'Authorization': `Bearer ${token}` };
  }

  async generateScraper(domain, config = {}) {
    const response = await fetch(`${this.baseUrl}/generate`, {
      method: 'POST',
      headers: { ...this.headers, 'Content-Type': 'application/json' },
      body: JSON.stringify({ domain, config })
    });
    return response.json();
  }

  async monitorRun(runId) {
    const response = await fetch(`${this.baseUrl}/runs/${runId}`, {
      headers: this.headers
    });
    return response.json();
  }
}

// Usage
const api = new ScraperAPI('http://localhost:8000/api/v1/scrapers', 'your-token');
const generation = await api.generateScraper('healthline.com');
const runStatus = await api.monitorRun('run_456def');
```

## 📈 Rate Limiting and Quotas

### Rate Limits
```yaml
Standard Users:
  - 100 API calls per hour
  - 10 scraper runs per day
  - 5 concurrent operations

Premium Users:
  - 1000 API calls per hour
  - 50 scraper runs per day
  - 20 concurrent operations

Enterprise Users:
  - Unlimited API calls
  - Unlimited scraper runs
  - Custom concurrency limits
```

## 📚 Related Documentation

- [Analytics API](analytics-api.md)
- [Source Discovery System](../../development/guides/source-discovery.md)
- [Compliance Framework](../../development/standards/compliance-standards.md)
- [Performance Optimization](../../operations/monitoring/performance-optimization.md)

---

**Scraper API Principles:**
- **Compliance First**: All operations respect legal and ethical boundaries
- **Performance Optimized**: Sub-2s response times for management operations
- **Comprehensive Monitoring**: Full visibility into scraper performance
- **Automated Generation**: AI-powered scraper creation and maintenance
- **Robust Error Handling**: Graceful degradation and detailed error reporting

**Last Updated**: 2025-07-07
**API Version**: 1.0.0
**Maintainer**: Claude (Technical Director)
