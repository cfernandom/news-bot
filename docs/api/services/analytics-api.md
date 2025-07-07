---
version: "1.0"
last_updated: "2025-07-07"
maintainer: "Claude (Technical Director)"
status: "active"
language: "English"
---

# Analytics API Documentation

FastAPI analytics endpoints for PreventIA News Analytics dashboard. Provides comprehensive analytics data for sentiment analysis, topic classification, geographic distribution, and temporal trends.

## 🚀 Quick Start

### Base URL
```
Development: http://localhost:8000/api/v1/analytics
Production: https://api.preventia.com/api/v1/analytics
```

### Authentication
```bash
# JWT token required for all endpoints
curl -H "Authorization: Bearer your-jwt-token" \
     http://localhost:8000/api/v1/analytics/sentiment
```

### Health Check
```bash
curl http://localhost:8000/health
# Response: {"status": "healthy", "timestamp": "2025-07-07T12:00:00Z"}
```

## 📊 Sentiment Analytics Endpoints

### GET /sentiment
Get overall sentiment distribution for articles.

#### Parameters
```yaml
time_range: string (optional)
  - "7d", "30d", "90d", "1y", "all"
  - Default: "30d"

source_ids: array[int] (optional)
  - Filter by specific news sources
  - Example: [1, 2, 3]

language: string (optional)
  - "en", "es", "all"
  - Default: "all"
```

#### Response
```json
{
  "status": "success",
  "data": {
    "total_articles": 106,
    "sentiment_distribution": {
      "positive": {
        "count": 24,
        "percentage": 22.6,
        "average_score": 0.415
      },
      "negative": {
        "count": 79,
        "percentage": 74.5,
        "average_score": -0.700
      },
      "neutral": {
        "count": 3,
        "percentage": 2.8,
        "average_score": 0.000
      }
    },
    "trend": {
      "direction": "stable",
      "change_percentage": -2.1,
      "confidence": 0.75
    }
  },
  "meta": {
    "timestamp": "2025-07-07T12:00:00Z",
    "cache_age": 300,
    "processing_time_ms": 45
  }
}
```

#### Example Usage
```bash
# Get sentiment data for last 7 days
curl "http://localhost:8000/api/v1/analytics/sentiment?time_range=7d"

# Get sentiment for specific sources
curl "http://localhost:8000/api/v1/analytics/sentiment?source_ids=[1,2]"

# Get English-only sentiment data
curl "http://localhost:8000/api/v1/analytics/sentiment?language=en"
```

### GET /sentiment/timeline
Get sentiment trends over time for timeline visualization.

#### Parameters
```yaml
time_range: string (optional)
  - "7d", "30d", "90d", "1y"
  - Default: "30d"

granularity: string (optional)
  - "daily", "weekly", "monthly"
  - Default: "daily"

sentiment_type: string (optional)
  - "positive", "negative", "neutral", "all"
  - Default: "all"
```

#### Response
```json
{
  "status": "success",
  "data": {
    "timeline": [
      {
        "date": "2025-07-01",
        "positive": 3,
        "negative": 8,
        "neutral": 1,
        "total": 12,
        "sentiment_score": -0.42
      },
      {
        "date": "2025-07-02",
        "positive": 2,
        "negative": 6,
        "neutral": 0,
        "total": 8,
        "sentiment_score": -0.38
      }
    ],
    "summary": {
      "total_days": 30,
      "average_daily_articles": 3.5,
      "sentiment_volatility": 0.15
    }
  }
}
```

### GET /sentiment/sources
Get sentiment breakdown by news source.

#### Response
```json
{
  "status": "success",
  "data": {
    "sources": [
      {
        "source_id": 1,
        "source_name": "Breast Cancer Organization",
        "url": "breastcancer.org",
        "article_count": 25,
        "sentiment_distribution": {
          "positive": 18,
          "negative": 6,
          "neutral": 1
        },
        "average_sentiment_score": 0.23,
        "quality_score": 0.85
      }
    ],
    "summary": {
      "total_sources": 4,
      "most_positive_source": "breastcancer.org",
      "most_negative_source": "medicalnews.com"
    }
  }
}
```

## 🏷️ Topic Classification Endpoints

### GET /topics
Get overall topic distribution across articles.

#### Parameters
```yaml
time_range: string (optional)
  - Default: "30d"

min_confidence: float (optional)
  - Minimum confidence score (0.0-1.0)
  - Default: 0.5

include_subcategories: boolean (optional)
  - Include detailed subcategory breakdown
  - Default: false
```

#### Response
```json
{
  "status": "success",
  "data": {
    "total_articles": 106,
    "topic_distribution": [
      {
        "topic": "treatment",
        "count": 39,
        "percentage": 36.8,
        "average_confidence": 0.89,
        "trend": "increasing"
      },
      {
        "topic": "research",
        "count": 19,
        "percentage": 17.9,
        "average_confidence": 0.82,
        "trend": "stable"
      },
      {
        "topic": "general",
        "count": 19,
        "percentage": 17.9,
        "average_confidence": 0.75,
        "trend": "decreasing"
      }
    ],
    "trending_topics": [
      {
        "topic": "immunotherapy",
        "growth_rate": 45.2,
        "recent_articles": 8
      }
    ]
  }
}
```

### GET /topics/timeline
Get topic trends over time.

#### Response
```json
{
  "status": "success",
  "data": {
    "timeline": [
      {
        "date": "2025-07-01",
        "topics": {
          "treatment": 5,
          "research": 3,
          "diagnosis": 2,
          "prevention": 1
        }
      }
    ],
    "topic_velocity": {
      "treatment": 0.15,
      "research": -0.05,
      "diagnosis": 0.08
    }
  }
}
```

### GET /topics/correlation
Get correlation matrix between topics and sentiment.

#### Response
```json
{
  "status": "success",
  "data": {
    "correlations": {
      "treatment_positive": 0.65,
      "research_positive": 0.23,
      "diagnosis_negative": -0.45,
      "prevention_neutral": 0.12
    },
    "insights": [
      "Treatment articles tend to be more positive",
      "Diagnosis articles skew negative",
      "Research articles are generally neutral"
    ]
  }
}
```

## 🌍 Geographic Analytics Endpoints

### GET /geographic
Get geographic distribution of article coverage.

#### Parameters
```yaml
country_codes: array[string] (optional)
  - ISO country codes: ["US", "UK", "CA"]
  - Default: all countries

metric: string (optional)
  - "article_count", "sentiment_avg", "topic_diversity"
  - Default: "article_count"
```

#### Response
```json
{
  "status": "success",
  "data": {
    "countries": [
      {
        "country_code": "US",
        "country_name": "United States",
        "article_count": 45,
        "sentiment_average": -0.23,
        "dominant_topics": ["treatment", "research"],
        "coverage_intensity": "high"
      },
      {
        "country_code": "UK",
        "country_name": "United Kingdom",
        "article_count": 23,
        "sentiment_average": 0.12,
        "dominant_topics": ["prevention", "screening"],
        "coverage_intensity": "medium"
      }
    ],
    "global_summary": {
      "total_countries": 12,
      "top_coverage_country": "US",
      "most_positive_country": "UK",
      "geographic_diversity_score": 0.67
    }
  }
}
```

### GET /geographic/heatmap
Get data formatted for geographic heatmap visualization.

#### Response
```json
{
  "status": "success",
  "data": {
    "heatmap_data": [
      {
        "country": "US",
        "value": 45,
        "intensity": 0.85,
        "color": "#ff6b6b"
      }
    ],
    "legend": {
      "min_value": 1,
      "max_value": 45,
      "color_scale": ["#ffffcc", "#ff6b6b"]
    }
  }
}
```

## 📈 Trend Analysis Endpoints

### GET /trends/weekly
Get weekly analytics summary.

#### Response
```json
{
  "status": "success",
  "data": {
    "current_week": {
      "week_start": "2025-07-01",
      "week_end": "2025-07-07",
      "article_count": 28,
      "sentiment_average": -0.15,
      "top_topics": ["treatment", "research"],
      "notable_events": [
        "FDA approval announcement increased positive sentiment"
      ]
    },
    "comparison": {
      "previous_week": {
        "article_count": 23,
        "sentiment_average": -0.28
      },
      "changes": {
        "article_count_change": 21.7,
        "sentiment_change": 46.4,
        "trend_direction": "improving"
      }
    },
    "predictions": {
      "next_week_articles": 31,
      "sentiment_forecast": -0.10,
      "confidence": 0.72
    }
  }
}
```

### GET /trends/anomalies
Detect unusual patterns in the data.

#### Response
```json
{
  "status": "success",
  "data": {
    "anomalies": [
      {
        "date": "2025-07-05",
        "type": "sentiment_spike",
        "description": "Unusual positive sentiment increase",
        "severity": "medium",
        "affected_articles": 8,
        "possible_cause": "breakthrough treatment announcement"
      }
    ],
    "summary": {
      "total_anomalies": 3,
      "severity_distribution": {
        "high": 0,
        "medium": 2,
        "low": 1
      }
    }
  }
}
```

## 🔍 Search and Filter Endpoints

### GET /search
Advanced search with analytics integration.

#### Parameters
```yaml
q: string (required)
  - Search query

filters: object (optional)
  - sentiment: ["positive", "negative", "neutral"]
  - topics: ["treatment", "research"]
  - date_range: {"start": "2025-07-01", "end": "2025-07-07"}
  - sources: [1, 2, 3]

sort: string (optional)
  - "relevance", "date", "sentiment_score"
  - Default: "relevance"

limit: int (optional)
  - Default: 20, Max: 100
```

#### Response
```json
{
  "status": "success",
  "data": {
    "articles": [
      {
        "id": "123e4567-e89b-12d3-a456-426614174000",
        "title": "New Treatment Shows Promise",
        "summary": "Clinical trial results indicate...",
        "sentiment": {
          "label": "positive",
          "score": 0.75
        },
        "topics": ["treatment", "clinical-trial"],
        "published_at": "2025-07-07T10:00:00Z",
        "relevance_score": 0.95
      }
    ],
    "aggregations": {
      "sentiment_distribution": {...},
      "topic_breakdown": {...},
      "temporal_distribution": {...}
    },
    "meta": {
      "total_results": 156,
      "search_time_ms": 23,
      "suggestions": ["immunotherapy", "targeted therapy"]
    }
  }
}
```

## 📊 Export Endpoints

### GET /export
Export analytics data in various formats.

#### Parameters
```yaml
format: string (required)
  - "csv", "json", "xlsx"

data_type: string (required)
  - "sentiment", "topics", "geographic", "articles"

time_range: string (optional)
  - Default: "30d"

filters: object (optional)
  - Same as search endpoint
```

#### Response Headers
```
Content-Type: application/octet-stream
Content-Disposition: attachment; filename="analytics_export_20250707.csv"
```

#### Usage
```bash
# Export sentiment data as CSV
curl -H "Authorization: Bearer token" \
     "http://localhost:8000/api/v1/analytics/export?format=csv&data_type=sentiment" \
     --output sentiment_data.csv

# Export filtered articles as JSON
curl -H "Authorization: Bearer token" \
     "http://localhost:8000/api/v1/analytics/export?format=json&data_type=articles&time_range=7d" \
     --output recent_articles.json
```

## 🔄 Real-time WebSocket Endpoints

### WebSocket /ws/analytics
Real-time analytics updates via WebSocket.

#### Connection
```javascript
const ws = new WebSocket('ws://localhost:8000/api/v1/analytics/ws');

// Subscribe to specific analytics
ws.send(JSON.stringify({
  action: 'subscribe',
  channels: ['sentiment_updates', 'new_articles', 'trending_topics']
}));
```

#### Message Format
```json
{
  "channel": "sentiment_updates",
  "timestamp": "2025-07-07T12:00:00Z",
  "data": {
    "new_article_id": "123e4567-e89b-12d3-a456-426614174000",
    "sentiment_change": {
      "before": {"positive": 24, "negative": 79},
      "after": {"positive": 25, "negative": 79}
    },
    "updated_metrics": {
      "sentiment_average": -0.315
    }
  }
}
```

## 🛡️ Rate Limiting and Security

### Rate Limits
```yaml
Authenticated Users:
  - 1000 requests per hour
  - 100 requests per minute
  - Burst limit: 20 requests per 10 seconds

Anonymous Users:
  - 100 requests per hour
  - 10 requests per minute
  - No access to real-time endpoints

Premium Users:
  - 5000 requests per hour
  - 500 requests per minute
  - Priority queue processing
```

### Error Responses
```json
{
  "status": "error",
  "error": {
    "code": "RATE_LIMIT_EXCEEDED",
    "message": "Rate limit exceeded. Try again in 60 seconds.",
    "details": {
      "limit": 100,
      "remaining": 0,
      "reset_at": "2025-07-07T13:00:00Z"
    }
  }
}
```

## 📈 Performance and Caching

### Response Times
```yaml
Target Performance:
  - Simple aggregations: <500ms
  - Complex analytics: <2s
  - Export generation: <10s
  - Real-time updates: <100ms

Caching Strategy:
  - Analytics summaries: 5 minutes
  - Historical data: 1 hour
  - Export files: 30 minutes
  - Real-time data: No cache
```

### Monitoring
```bash
# Check API performance metrics
curl http://localhost:8000/metrics

# Health check with database connectivity
curl http://localhost:8000/health/detailed
```

## 🧪 Testing the API

### Test Data Setup
```bash
# Load test data
python scripts/load_test_data.py

# Verify test environment
curl http://localhost:8000/api/v1/analytics/sentiment?time_range=all
```

### Example Test Suite
```python
import pytest
import httpx

@pytest.mark.asyncio
async def test_sentiment_analytics():
    async with httpx.AsyncClient() as client:
        response = await client.get(
            "http://localhost:8000/api/v1/analytics/sentiment",
            headers={"Authorization": "Bearer test-token"}
        )
        assert response.status_code == 200
        data = response.json()
        assert "sentiment_distribution" in data["data"]
        assert data["data"]["total_articles"] > 0
```

## 📚 Related Documentation

- [NLP API Documentation](nlp-api.md)
- [Database Schema](../../architecture/data-flow.md)
- [Frontend Integration](../../development/guides/frontend-integration.md)
- [Production Deployment](../../operations/deployment/production-deployment.md)

---

**API Principles:**
- **Fast Response Times**: All endpoints optimized for <2s response
- **Comprehensive Analytics**: Full spectrum of medical news insights
- **Real-time Updates**: WebSocket integration for live dashboard
- **Export Capabilities**: Multiple formats for research and reporting
- **Security First**: Authentication, rate limiting, data validation

**Last Updated**: 2025-07-07
**API Version**: 1.0.0
**Maintainer**: Claude (Technical Director)
