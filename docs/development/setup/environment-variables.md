---
version: "1.0"
last_updated: "2025-07-07"
maintainer: "Claude (Technical Director)"
status: "active"
language: "English"
---

# Environment Variables Configuration

This document describes all environment variables used in the PreventIA News Analytics system, including setup instructions, security considerations, and examples.

## 📋 Quick Setup

### 1. Copy Template
```bash
cp .env.template .env
```

### 2. Configure Required Variables
```bash
# Edit with your values
nano .env
```

### 3. Verify Configuration
```bash
# Test database connection
python scripts/test_database_connection.py

# Verify all services
docker compose config
```

## 🔧 Core Environment Variables

### Database Configuration
```bash
# PostgreSQL connection (required)
DATABASE_URL=postgresql://preventia:password@localhost:5433/preventia_news
POSTGRES_DB=preventia_news
POSTGRES_USER=preventia
POSTGRES_PASSWORD=your_secure_password
POSTGRES_HOST=localhost
POSTGRES_PORT=5433

# Connection pool settings (optional)
DB_POOL_SIZE=10
DB_MAX_OVERFLOW=20
DB_POOL_TIMEOUT=30
```

### External APIs
```bash
# OpenAI API for LLM features (required for summaries)
OPENAI_API_KEY=sk-your-openai-api-key-here

# Optional: Alternative LLM providers
ANTHROPIC_API_KEY=your_anthropic_key
HUGGINGFACE_API_KEY=your_huggingface_key
```

### Application Settings
```bash
# Application environment
ENVIRONMENT=development  # development, staging, production
DEBUG=true              # Set to false in production
LOG_LEVEL=INFO          # DEBUG, INFO, WARNING, ERROR

# Security settings
SECRET_KEY=your-secret-key-for-jwt-tokens
JWT_ALGORITHM=HS256
JWT_EXPIRATION_HOURS=24

# API rate limiting
RATE_LIMIT_PER_MINUTE=60
RATE_LIMIT_BURST=10
```

### Web Scraping Configuration
```bash
# Scraping behavior
SCRAPER_DELAY_SECONDS=2
SCRAPER_TIMEOUT_SECONDS=30
SCRAPER_MAX_RETRIES=3
SCRAPER_USER_AGENT="PreventIA-NewsBot/1.0 (Academic Research)"

# Compliance settings
RESPECT_ROBOTS_TXT=true
ENABLE_COMPLIANCE_CHECKS=true
```

### Cache Configuration
```bash
# Redis cache (optional but recommended)
REDIS_URL=redis://localhost:6379/0
REDIS_PASSWORD=your_redis_password
CACHE_TTL_SECONDS=3600
ENABLE_CACHING=true
```

### FastAPI Configuration
```bash
# API server settings
API_HOST=0.0.0.0
API_PORT=8000
API_WORKERS=4
API_TITLE="PreventIA News Analytics API"
API_VERSION=1.0.0

# CORS settings
CORS_ORIGINS=["http://localhost:3000", "http://localhost:5173"]
CORS_ALLOW_CREDENTIALS=true
```

### Frontend Configuration
```bash
# React dashboard settings
REACT_APP_API_BASE_URL=http://localhost:8000
REACT_APP_ENVIRONMENT=development
REACT_APP_VERSION=1.0.0
REACT_APP_ENABLE_MOCK_DATA=false
```

## 🔒 Security Best Practices

### Production Security
```bash
# Production-only settings
ENVIRONMENT=production
DEBUG=false
LOG_LEVEL=WARNING

# Strong security keys (use generators)
SECRET_KEY=$(openssl rand -hex 32)
POSTGRES_PASSWORD=$(openssl rand -base64 32)
REDIS_PASSWORD=$(openssl rand -base64 32)

# SSL/TLS settings
SSL_CERT_PATH=/path/to/ssl/cert.pem
SSL_KEY_PATH=/path/to/ssl/key.pem
FORCE_HTTPS=true
```

### API Key Management
```bash
# Never commit real API keys!
# Use placeholder values in .env.template:
OPENAI_API_KEY=sk-placeholder-replace-with-real-key

# For production, use environment variable injection:
# docker run -e OPENAI_API_KEY=$OPENAI_API_KEY ...
```

### Database Security
```bash
# Production database settings
POSTGRES_SSL_MODE=require
DB_ENCRYPTION_KEY=your-encryption-key
ENABLE_DB_AUDIT_LOG=true
DB_CONNECTION_TIMEOUT=5
```

## 🏗️ Environment-Specific Configurations

### Development Environment
```bash
# .env.development
ENVIRONMENT=development
DEBUG=true
LOG_LEVEL=DEBUG
DATABASE_URL=postgresql://preventia:dev_password@localhost:5433/preventia_news_dev
REACT_APP_ENABLE_MOCK_DATA=true
ENABLE_PERFORMANCE_PROFILING=true
```

### Staging Environment
```bash
# .env.staging
ENVIRONMENT=staging
DEBUG=false
LOG_LEVEL=INFO
DATABASE_URL=postgresql://preventia:staging_password@staging-db:5432/preventia_news_staging
RATE_LIMIT_PER_MINUTE=30
API_WORKERS=2
```

### Production Environment
```bash
# .env.production
ENVIRONMENT=production
DEBUG=false
LOG_LEVEL=WARNING
DATABASE_URL=postgresql://preventia:prod_password@prod-db:5432/preventia_news
RATE_LIMIT_PER_MINUTE=100
API_WORKERS=8
FORCE_HTTPS=true
ENABLE_MONITORING=true
```

## 🧪 Testing Configuration

### Test Environment Variables
```bash
# Test-specific settings
TEST_DATABASE_URL=postgresql://preventia:test@localhost:5433/preventia_test
PYTEST_TIMEOUT=60
ENABLE_TEST_COVERAGE=true
TEST_LOG_LEVEL=DEBUG

# Mock settings for testing
MOCK_OPENAI_API=true
MOCK_EXTERNAL_APIS=true
TEST_DATA_PATH=tests/fixtures/
```

### CI/CD Environment
```bash
# GitHub Actions / CI settings
CI=true
GITHUB_TOKEN=${{ secrets.GITHUB_TOKEN }}
DOCKER_REGISTRY=ghcr.io
DEPLOYMENT_ENVIRONMENT=staging
```

## 📊 Monitoring and Observability

### Logging Configuration
```bash
# Structured logging
LOG_FORMAT=json
LOG_OUTPUT=stdout
ENABLE_REQUEST_LOGGING=true
LOG_RETENTION_DAYS=30

# Performance monitoring
ENABLE_METRICS=true
METRICS_PORT=9090
PROMETHEUS_ENDPOINT=/metrics
```

### Health Check Settings
```bash
# Health check configuration
HEALTH_CHECK_INTERVAL=30
HEALTH_CHECK_TIMEOUT=5
HEALTH_CHECK_RETRIES=3
ENABLE_DEEP_HEALTH_CHECKS=true
```

## 🔧 Docker Compose Integration

### Environment File Loading
```yaml
# docker-compose.yml
services:
  api:
    env_file:
      - .env
      - .env.local  # Optional local overrides
    environment:
      - ENVIRONMENT=${ENVIRONMENT:-development}
```

### Multiple Environment Files
```bash
# Load order (later files override earlier ones)
1. .env.template (defaults)
2. .env (main configuration)
3. .env.local (local overrides, gitignored)
4. docker-compose override values
```

## ⚠️ Common Issues and Solutions

### Database Connection Issues
```bash
# Check if PostgreSQL is running
docker compose ps postgres

# Test connection manually
psql $DATABASE_URL

# Common fix: Wrong port or credentials
DATABASE_URL=postgresql://preventia:password@localhost:5433/preventia_news
```

### API Key Issues
```bash
# Verify API key format
echo $OPENAI_API_KEY | wc -c  # Should be 51 characters

# Test API key
curl -H "Authorization: Bearer $OPENAI_API_KEY" https://api.openai.com/v1/models
```

### Docker Environment Issues
```bash
# Rebuild with fresh environment
docker compose down
docker compose build --no-cache
docker compose up -d
```

## 📋 Environment Validation Script

Create a script to validate your environment:

```bash
#!/bin/bash
# scripts/validate_environment.sh

echo "🔍 Validating environment configuration..."

# Check required variables
required_vars=("DATABASE_URL" "OPENAI_API_KEY" "SECRET_KEY")
for var in "${required_vars[@]}"; do
    if [ -z "${!var}" ]; then
        echo "❌ Missing required variable: $var"
        exit 1
    else
        echo "✅ $var is set"
    fi
done

# Test database connection
python -c "
import os
from services.data.database.connection import db_manager
import asyncio

async def test_db():
    try:
        await db_manager.execute_sql('SELECT 1')
        print('✅ Database connection successful')
    except Exception as e:
        print(f'❌ Database connection failed: {e}')
        exit(1)

asyncio.run(test_db())
"

echo "✅ Environment validation completed successfully!"
```

## 📚 Additional Resources

- [Docker Setup Guide](docker-setup.md)
- [Local Development Setup](local-development.md)
- [Production Deployment](../../operations/deployment/production-deployment.md)
- [Security Best Practices](../standards/security-standards.md)

---

**Last Updated**: 2025-07-07
**Next Review**: 2025-08-07
**Maintainer**: Claude (Technical Director)
