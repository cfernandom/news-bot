---
version: "1.0"
last_updated: "2025-07-07"
maintainer: "Claude (Technical Director)"
status: "active"
language: "English"
---

# Production Deployment Guide

Comprehensive guide for deploying PreventIA News Analytics to production environment. Covers infrastructure setup, security configuration, monitoring, and maintenance procedures.

## 🎯 Deployment Overview

### Architecture Components
- **Frontend**: React dashboard (Nginx + static files)
- **Backend**: FastAPI application (Gunicorn + Uvicorn workers)
- **Database**: PostgreSQL with connection pooling
- **Cache**: Redis for session storage and API caching
- **Reverse Proxy**: Nginx for load balancing and SSL termination
- **Monitoring**: Prometheus + Grafana + logs aggregation

### Deployment Environments
- **Production**: Live system for end users
- **Staging**: Pre-production testing environment
- **Development**: Local development environment

## 🏗️ Infrastructure Requirements

### Server Specifications

#### Minimum Requirements (Small Scale)
```yaml
CPU: 4 cores (2.5GHz+)
RAM: 8GB
Storage: 100GB SSD
Network: 1Gbps
OS: Ubuntu 22.04 LTS or RHEL 8+
```

#### Recommended Requirements (Medium Scale)
```yaml
CPU: 8 cores (3.0GHz+)
RAM: 16GB
Storage: 500GB SSD
Network: 1Gbps
OS: Ubuntu 22.04 LTS
```

#### High Availability Setup
```yaml
Load Balancer: 2 nodes (2 cores, 4GB each)
Application Servers: 3 nodes (4 cores, 8GB each)
Database Server: 1 node (8 cores, 32GB, 1TB SSD)
Redis Server: 1 node (2 cores, 4GB)
Monitoring: 1 node (4 cores, 8GB)
```

### Network Configuration
```yaml
Ports Required:
  - 80 (HTTP redirect to HTTPS)
  - 443 (HTTPS)
  - 22 (SSH - restricted)
  - 5432 (PostgreSQL - internal only)
  - 6379 (Redis - internal only)
  - 9090 (Prometheus - internal only)
  - 3000 (Grafana - internal only)

Firewall Rules:
  - Allow 80, 443 from anywhere
  - Allow 22 from admin IPs only
  - Block all other external access
  - Allow internal communication between services
```

## 🐳 Docker Production Setup

### 1. Production Docker Compose

Create `docker-compose.prod.yml`:

```yaml
version: '3.8'

services:
  nginx:
    image: nginx:1.24-alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx/nginx.conf:/etc/nginx/nginx.conf:ro
      - ./nginx/sites-enabled:/etc/nginx/sites-enabled:ro
      - ./ssl:/etc/nginx/ssl:ro
      - ./logs/nginx:/var/log/nginx
      - frontend_build:/usr/share/nginx/html:ro
    depends_on:
      - api
      - frontend
    restart: unless-stopped
    networks:
      - frontend_network
      - backend_network

  frontend:
    build:
      context: ./preventia-dashboard
      dockerfile: Dockerfile.prod
    volumes:
      - frontend_build:/app/dist
    environment:
      - NODE_ENV=production
      - REACT_APP_API_BASE_URL=https://api.preventia.com
    restart: unless-stopped
    networks:
      - frontend_network

  api:
    build:
      context: .
      dockerfile: Dockerfile.api.prod
    environment:
      - ENVIRONMENT=production
      - DATABASE_URL=${DATABASE_URL}
      - REDIS_URL=${REDIS_URL}
      - OPENAI_API_KEY=${OPENAI_API_KEY}
      - SECRET_KEY=${SECRET_KEY}
      - LOG_LEVEL=WARNING
      - API_WORKERS=4
    volumes:
      - ./logs/api:/app/logs
    depends_on:
      - postgres
      - redis
    restart: unless-stopped
    networks:
      - backend_network
    deploy:
      resources:
        limits:
          memory: 2G
          cpus: '1.0'

  postgres:
    image: postgres:16-alpine
    environment:
      - POSTGRES_DB=${POSTGRES_DB}
      - POSTGRES_USER=${POSTGRES_USER}
      - POSTGRES_PASSWORD=${POSTGRES_PASSWORD}
      - POSTGRES_INITDB_ARGS=--auth-host=scram-sha-256
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./postgres/postgresql.conf:/etc/postgresql/postgresql.conf:ro
      - ./postgres/pg_hba.conf:/etc/postgresql/pg_hba.conf:ro
      - ./backups:/backups
      - ./logs/postgres:/var/log/postgresql
    restart: unless-stopped
    networks:
      - backend_network
    deploy:
      resources:
        limits:
          memory: 4G
          cpus: '2.0'

  redis:
    image: redis:7-alpine
    command: redis-server /etc/redis/redis.conf
    volumes:
      - redis_data:/data
      - ./redis/redis.conf:/etc/redis/redis.conf:ro
      - ./logs/redis:/var/log/redis
    restart: unless-stopped
    networks:
      - backend_network
    deploy:
      resources:
        limits:
          memory: 1G
          cpus: '0.5'

  prometheus:
    image: prom/prometheus:v2.45.0
    command:
      - '--config.file=/etc/prometheus/prometheus.yml'
      - '--storage.tsdb.path=/prometheus'
      - '--web.console.libraries=/etc/prometheus/console_libraries'
      - '--web.console.templates=/etc/prometheus/consoles'
    volumes:
      - ./monitoring/prometheus.yml:/etc/prometheus/prometheus.yml:ro
      - prometheus_data:/prometheus
    restart: unless-stopped
    networks:
      - monitoring_network
      - backend_network

  grafana:
    image: grafana/grafana:10.0.0
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=${GRAFANA_ADMIN_PASSWORD}
      - GF_INSTALL_PLUGINS=grafana-clock-panel,grafana-simple-json-datasource
    volumes:
      - grafana_data:/var/lib/grafana
      - ./monitoring/grafana/dashboards:/var/lib/grafana/dashboards
      - ./monitoring/grafana/provisioning:/etc/grafana/provisioning
    restart: unless-stopped
    networks:
      - monitoring_network
    depends_on:
      - prometheus

volumes:
  postgres_data:
    driver: local
  redis_data:
    driver: local
  prometheus_data:
    driver: local
  grafana_data:
    driver: local
  frontend_build:
    driver: local

networks:
  frontend_network:
    driver: bridge
  backend_network:
    driver: bridge
  monitoring_network:
    driver: bridge
```

### 2. Production Dockerfiles

#### API Dockerfile (`Dockerfile.api.prod`)
```dockerfile
FROM python:3.13-slim AS builder

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

FROM python:3.13-slim AS runtime

# Create non-root user
RUN useradd --create-home --shell /bin/bash app

# Install runtime dependencies
RUN apt-get update && apt-get install -y \
    libpq5 \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy Python packages from builder
COPY --from=builder /root/.local /home/app/.local

# Set up application
WORKDIR /app
COPY . .
RUN chown -R app:app /app

# Switch to non-root user
USER app

# Add local packages to PATH
ENV PATH=/home/app/.local/bin:$PATH

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Run application
CMD ["gunicorn", "services.api.main:app", \
     "--worker-class", "uvicorn.workers.UvicornWorker", \
     "--workers", "4", \
     "--bind", "0.0.0.0:8000", \
     "--timeout", "60", \
     "--keepalive", "5", \
     "--max-requests", "1000", \
     "--max-requests-jitter", "100"]
```

#### Frontend Dockerfile (`preventia-dashboard/Dockerfile.prod`)
```dockerfile
FROM node:20-alpine AS builder

WORKDIR /app

# Copy package files
COPY package*.json ./
RUN npm ci --only=production

# Copy source and build
COPY . .
RUN npm run build

FROM nginx:1.24-alpine AS runtime

# Copy built application
COPY --from=builder /app/dist /usr/share/nginx/html

# Copy nginx configuration
COPY nginx.conf /etc/nginx/nginx.conf

# Add health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=30s --retries=3 \
    CMD wget --no-verbose --tries=1 --spider http://localhost/ || exit 1

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

## ⚙️ Configuration Files

### 1. Nginx Configuration

Create `nginx/nginx.conf`:

```nginx
user nginx;
worker_processes auto;
error_log /var/log/nginx/error.log notice;
pid /var/run/nginx.pid;

events {
    worker_connections 1024;
    use epoll;
    multi_accept on;
}

http {
    include /etc/nginx/mime.types;
    default_type application/octet-stream;

    # Logging format
    log_format main '$remote_addr - $remote_user [$time_local] "$request" '
                   '$status $body_bytes_sent "$http_referer" '
                   '"$http_user_agent" "$http_x_forwarded_for" '
                   'rt=$request_time uct="$upstream_connect_time" '
                   'uht="$upstream_header_time" urt="$upstream_response_time"';

    access_log /var/log/nginx/access.log main;

    # Performance settings
    sendfile on;
    tcp_nopush on;
    tcp_nodelay on;
    keepalive_timeout 65;
    types_hash_max_size 2048;
    client_max_body_size 50M;

    # Gzip compression
    gzip on;
    gzip_vary on;
    gzip_min_length 1024;
    gzip_types
        text/plain
        text/css
        text/xml
        text/javascript
        application/javascript
        application/xml+rss
        application/json;

    # Security headers
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header Referrer-Policy "strict-origin-when-cross-origin" always;
    add_header Content-Security-Policy "default-src 'self'; script-src 'self' 'unsafe-inline' 'unsafe-eval'; style-src 'self' 'unsafe-inline'; img-src 'self' data: https:; font-src 'self' data:; connect-src 'self';" always;

    # Rate limiting
    limit_req_zone $binary_remote_addr zone=api:10m rate=10r/s;
    limit_req_zone $binary_remote_addr zone=general:10m rate=1r/s;

    include /etc/nginx/sites-enabled/*;
}
```

Create `nginx/sites-enabled/preventia.conf`:

```nginx
# Redirect HTTP to HTTPS
server {
    listen 80;
    server_name preventia.com www.preventia.com;
    return 301 https://$server_name$request_uri;
}

# HTTPS configuration
server {
    listen 443 ssl http2;
    server_name preventia.com www.preventia.com;

    # SSL configuration
    ssl_certificate /etc/nginx/ssl/preventia.com.crt;
    ssl_certificate_key /etc/nginx/ssl/preventia.com.key;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers ECDHE-RSA-AES256-GCM-SHA512:DHE-RSA-AES256-GCM-SHA512:ECDHE-RSA-AES256-GCM-SHA384:DHE-RSA-AES256-GCM-SHA384;
    ssl_prefer_server_ciphers off;
    ssl_session_cache shared:SSL:10m;
    ssl_session_timeout 10m;

    # Security headers
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;

    # Frontend (React app)
    location / {
        root /usr/share/nginx/html;
        index index.html;
        try_files $uri $uri/ /index.html;

        # Cache static assets
        location ~* \.(js|css|png|jpg|jpeg|gif|ico|svg|woff|woff2|ttf|eot)$ {
            expires 1y;
            add_header Cache-Control "public, immutable";
        }
    }

    # API endpoints
    location /api/ {
        limit_req zone=api burst=20 nodelay;

        proxy_pass http://api:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;

        # Timeouts
        proxy_connect_timeout 5s;
        proxy_send_timeout 60s;
        proxy_read_timeout 60s;

        # WebSocket support
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
    }

    # Health check endpoint
    location /health {
        proxy_pass http://api:8000/health;
        access_log off;
    }

    # Monitoring endpoints (internal only)
    location /metrics {
        allow 127.0.0.1;
        allow 10.0.0.0/8;
        allow 172.16.0.0/12;
        allow 192.168.0.0/16;
        deny all;

        proxy_pass http://api:8000/metrics;
    }
}
```

### 2. PostgreSQL Configuration

Create `postgres/postgresql.conf`:

```conf
# Connection settings
listen_addresses = '*'
port = 5432
max_connections = 100
superuser_reserved_connections = 3

# Memory settings
shared_buffers = 256MB
effective_cache_size = 1GB
maintenance_work_mem = 64MB
checkpoint_completion_target = 0.9
wal_buffers = 16MB
default_statistics_target = 100
random_page_cost = 1.1
effective_io_concurrency = 200

# Logging
logging_collector = on
log_directory = '/var/log/postgresql'
log_filename = 'postgresql-%Y-%m-%d_%H%M%S.log'
log_rotation_age = 1d
log_rotation_size = 100MB
log_min_duration_statement = 1000
log_line_prefix = '%t [%p-%l] %q%u@%d '
log_checkpoints = on
log_connections = on
log_disconnections = on
log_lock_waits = on

# Performance monitoring
track_activities = on
track_counts = on
track_io_timing = on
track_functions = all

# Security
ssl = on
ssl_cert_file = '/etc/ssl/certs/ssl-cert-snakeoil.pem'
ssl_key_file = '/etc/ssl/private/ssl-cert-snakeoil.key'
```

Create `postgres/pg_hba.conf`:

```conf
# TYPE  DATABASE        USER            ADDRESS                 METHOD
local   all             postgres                                peer
local   all             all                                     scram-sha-256
host    all             all             127.0.0.1/32            scram-sha-256
host    all             all             ::1/128                 scram-sha-256
host    all             all             10.0.0.0/8              scram-sha-256
host    all             all             172.16.0.0/12           scram-sha-256
host    all             all             192.168.0.0/16          scram-sha-256
```

### 3. Redis Configuration

Create `redis/redis.conf`:

```conf
# Network
bind 127.0.0.1 ::1 172.16.0.0/12
port 6379
protected-mode yes
timeout 300
keepalive 300

# Memory management
maxmemory 512mb
maxmemory-policy allkeys-lru

# Persistence
save 900 1
save 300 10
save 60 10000
rdbcompression yes
rdbchecksum yes
dbfilename dump.rdb
dir /data

# Logging
loglevel notice
logfile /var/log/redis/redis-server.log

# Security
requirepass ${REDIS_PASSWORD}

# Performance
tcp-keepalive 60
tcp-backlog 511
```

## 🔐 Security Configuration

### 1. Environment Variables

Create `.env.production`:

```bash
# Application
ENVIRONMENT=production
DEBUG=false
LOG_LEVEL=WARNING
SECRET_KEY=your-super-secure-secret-key-here

# Database
DATABASE_URL=postgresql://preventia:secure_password@postgres:5432/preventia_news
POSTGRES_DB=preventia_news
POSTGRES_USER=preventia
POSTGRES_PASSWORD=secure_database_password

# Redis
REDIS_URL=redis://:secure_redis_password@redis:6379/0
REDIS_PASSWORD=secure_redis_password

# API Keys
OPENAI_API_KEY=sk-your-production-openai-api-key

# API Configuration
API_HOST=0.0.0.0
API_PORT=8000
API_WORKERS=4
CORS_ORIGINS=["https://preventia.com"]

# Security
JWT_ALGORITHM=HS256
JWT_EXPIRATION_HOURS=24
RATE_LIMIT_PER_MINUTE=100

# Monitoring
GRAFANA_ADMIN_PASSWORD=secure_grafana_password

# SSL
SSL_CERT_PATH=/etc/nginx/ssl/preventia.com.crt
SSL_KEY_PATH=/etc/nginx/ssl/preventia.com.key
```

### 2. SSL Certificate Setup

```bash
# Using Let's Encrypt (recommended)
sudo apt update
sudo apt install certbot python3-certbot-nginx

# Get certificate
sudo certbot --nginx -d preventia.com -d www.preventia.com

# Auto-renewal setup
sudo crontab -e
# Add: 0 12 * * * /usr/bin/certbot renew --quiet

# Or use existing certificate
sudo mkdir -p /etc/nginx/ssl
sudo cp your-certificate.crt /etc/nginx/ssl/preventia.com.crt
sudo cp your-private-key.key /etc/nginx/ssl/preventia.com.key
sudo chmod 600 /etc/nginx/ssl/*
```

### 3. Firewall Configuration

```bash
# UFW setup
sudo ufw default deny incoming
sudo ufw default allow outgoing

# Allow SSH (change port if needed)
sudo ufw allow 22/tcp

# Allow HTTP/HTTPS
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp

# Enable firewall
sudo ufw enable

# Check status
sudo ufw status verbose
```

## 📊 Monitoring Setup

### 1. Prometheus Configuration

Create `monitoring/prometheus.yml`:

```yaml
global:
  scrape_interval: 15s
  evaluation_interval: 15s

rule_files:
  - "alert_rules.yml"

alerting:
  alertmanagers:
    - static_configs:
        - targets:
          - alertmanager:9093

scrape_configs:
  - job_name: 'prometheus'
    static_configs:
      - targets: ['localhost:9090']

  - job_name: 'preventia-api'
    static_configs:
      - targets: ['api:8000']
    metrics_path: '/metrics'
    scrape_interval: 30s

  - job_name: 'postgres'
    static_configs:
      - targets: ['postgres-exporter:9187']

  - job_name: 'redis'
    static_configs:
      - targets: ['redis-exporter:9121']

  - job_name: 'nginx'
    static_configs:
      - targets: ['nginx-exporter:9113']

  - job_name: 'node'
    static_configs:
      - targets: ['node-exporter:9100']
```

### 2. Grafana Dashboards

Create `monitoring/grafana/dashboards/preventia-dashboard.json`:

```json
{
  "dashboard": {
    "title": "PreventIA News Analytics",
    "panels": [
      {
        "title": "API Response Time",
        "type": "graph",
        "targets": [
          {
            "expr": "rate(http_request_duration_seconds_sum[5m]) / rate(http_request_duration_seconds_count[5m])",
            "legendFormat": "{{method}} {{endpoint}}"
          }
        ]
      },
      {
        "title": "Database Connections",
        "type": "graph",
        "targets": [
          {
            "expr": "pg_stat_activity_count",
            "legendFormat": "Active Connections"
          }
        ]
      },
      {
        "title": "Scraper Performance",
        "type": "table",
        "targets": [
          {
            "expr": "scraper_articles_collected_total",
            "legendFormat": "Articles Collected"
          }
        ]
      }
    ]
  }
}
```

## 🚀 Deployment Process

### 1. Pre-deployment Checklist

```bash
# Verify environment
./scripts/verify_environment.sh production

# Run tests
cd tests && pytest --env=production

# Build images
docker-compose -f docker-compose.prod.yml build

# Test configuration
docker-compose -f docker-compose.prod.yml config
```

### 2. Initial Deployment

```bash
# Clone repository
git clone https://github.com/your-org/preventia-news-analytics.git
cd preventia-news-analytics

# Checkout production branch
git checkout main

# Setup environment
cp .env.template .env.production
# Edit .env.production with production values

# Create directories
mkdir -p logs/{nginx,api,postgres,redis}
mkdir -p backups
mkdir -p ssl

# Setup SSL certificates (Let's Encrypt or custom)
./scripts/setup_ssl.sh

# Initialize database
docker-compose -f docker-compose.prod.yml up -d postgres
sleep 30
docker-compose -f docker-compose.prod.yml exec postgres createdb -U preventia preventia_news

# Run migrations
docker-compose -f docker-compose.prod.yml exec api alembic upgrade head

# Start all services
docker-compose -f docker-compose.prod.yml up -d

# Verify deployment
./scripts/verify_deployment.sh
```

### 3. Deployment Verification Script

Create `scripts/verify_deployment.sh`:

```bash
#!/bin/bash
set -e

echo "🔍 Verifying production deployment..."

# Check services are running
echo "Checking services..."
docker-compose -f docker-compose.prod.yml ps

# Check health endpoints
echo "Checking health endpoints..."
curl -f https://preventia.com/health || exit 1
curl -f https://preventia.com/api/v1/health || exit 1

# Check database connectivity
echo "Checking database..."
docker-compose -f docker-compose.prod.yml exec -T postgres psql -U preventia -d preventia_news -c "SELECT COUNT(*) FROM articles;" || exit 1

# Check Redis
echo "Checking Redis..."
docker-compose -f docker-compose.prod.yml exec -T redis redis-cli ping || exit 1

# Check SSL certificate
echo "Checking SSL certificate..."
openssl s_client -connect preventia.com:443 -servername preventia.com < /dev/null 2>/dev/null | openssl x509 -noout -dates

# Performance test
echo "Running performance test..."
ab -n 100 -c 10 https://preventia.com/api/v1/health

echo "✅ Deployment verification completed successfully!"
```

## 🔄 Maintenance Procedures

### 1. Regular Backup Script

Create `scripts/backup.sh`:

```bash
#!/bin/bash
set -e

BACKUP_DIR="/backups"
DATE=$(date +%Y%m%d_%H%M%S)

echo "🗄️ Starting backup process..."

# Database backup
echo "Backing up PostgreSQL..."
docker-compose -f docker-compose.prod.yml exec -T postgres pg_dump -U preventia preventia_news | gzip > "${BACKUP_DIR}/db_backup_${DATE}.sql.gz"

# Redis backup
echo "Backing up Redis..."
docker-compose -f docker-compose.prod.yml exec -T redis redis-cli BGSAVE
sleep 5
docker cp $(docker-compose -f docker-compose.prod.yml ps -q redis):/data/dump.rdb "${BACKUP_DIR}/redis_backup_${DATE}.rdb"

# Configuration backup
echo "Backing up configuration..."
tar -czf "${BACKUP_DIR}/config_backup_${DATE}.tar.gz" \
    nginx/ postgres/ redis/ monitoring/ .env.production

# Clean old backups (keep 30 days)
find ${BACKUP_DIR} -name "*.gz" -mtime +30 -delete
find ${BACKUP_DIR} -name "*.rdb" -mtime +30 -delete

echo "✅ Backup completed: ${DATE}"
```

### 2. Update Deployment Script

Create `scripts/update_deployment.sh`:

```bash
#!/bin/bash
set -e

echo "🚀 Starting deployment update..."

# Pull latest code
git fetch origin
git checkout main
git pull origin main

# Backup before update
./scripts/backup.sh

# Build new images
docker-compose -f docker-compose.prod.yml build

# Rolling update
echo "Performing rolling update..."

# Update API (with health checks)
docker-compose -f docker-compose.prod.yml up -d --no-deps api
sleep 30
curl -f https://preventia.com/health || exit 1

# Update frontend
docker-compose -f docker-compose.prod.yml up -d --no-deps frontend nginx
sleep 10
curl -f https://preventia.com/ || exit 1

# Run migrations if needed
docker-compose -f docker-compose.prod.yml exec api alembic upgrade head

# Verify deployment
./scripts/verify_deployment.sh

echo "✅ Deployment update completed successfully!"
```

### 3. Log Rotation Setup

Create `/etc/logrotate.d/preventia`:

```conf
/opt/preventia/logs/*/*.log {
    daily
    missingok
    rotate 30
    compress
    delaycompress
    notifempty
    create 644 root root
    postrotate
        docker-compose -f /opt/preventia/docker-compose.prod.yml exec nginx nginx -s reload
    endscript
}
```

## 📈 Performance Optimization

### 1. Database Optimization

```sql
-- Create indexes for performance
CREATE INDEX CONCURRENTLY idx_articles_published_at ON articles (published_at DESC);
CREATE INDEX CONCURRENTLY idx_articles_source_id ON articles (source_id);
CREATE INDEX CONCURRENTLY idx_articles_sentiment ON articles (sentiment_label);
CREATE INDEX CONCURRENTLY idx_articles_hash ON articles (content_hash);

-- Analyze tables
ANALYZE articles;
ANALYZE news_sources;
ANALYZE article_keywords;

-- Vacuum tables
VACUUM ANALYZE;
```

### 2. Application Performance

```python
# Add to FastAPI app for production optimizations
@app.middleware("http")
async def add_performance_headers(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response

# Enable compression
from fastapi.middleware.gzip import GZipMiddleware
app.add_middleware(GZipMiddleware, minimum_size=1000)

# Add caching
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend

@app.on_event("startup")
async def startup():
    redis = aioredis.from_url("redis://redis:6379")
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")
```

## 🚨 Monitoring and Alerting

### 1. Alert Rules

Create `monitoring/alert_rules.yml`:

```yaml
groups:
  - name: preventia.rules
    rules:
      - alert: HighErrorRate
        expr: rate(http_requests_total{status=~"5.."}[5m]) > 0.1
        for: 5m
        labels:
          severity: critical
        annotations:
          summary: High error rate detected
          description: "Error rate is {{ $value }} errors per second"

      - alert: DatabaseDown
        expr: up{job="postgres"} == 0
        for: 1m
        labels:
          severity: critical
        annotations:
          summary: PostgreSQL is down
          description: "PostgreSQL database is not responding"

      - alert: HighMemoryUsage
        expr: (node_memory_MemTotal_bytes - node_memory_MemAvailable_bytes) / node_memory_MemTotal_bytes > 0.9
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: High memory usage
          description: "Memory usage is above 90%"

      - alert: DiskSpaceLow
        expr: (node_filesystem_size_bytes - node_filesystem_free_bytes) / node_filesystem_size_bytes > 0.8
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: Low disk space
          description: "Disk usage is above 80%"
```

### 2. Health Check Endpoints

```python
# Enhanced health check in FastAPI
@app.get("/health/detailed")
async def detailed_health_check():
    checks = {
        "timestamp": datetime.utcnow().isoformat(),
        "status": "healthy",
        "checks": {}
    }

    # Database check
    try:
        await db_manager.execute_sql("SELECT 1")
        checks["checks"]["database"] = {"status": "healthy", "response_time": 0.05}
    except Exception as e:
        checks["checks"]["database"] = {"status": "unhealthy", "error": str(e)}
        checks["status"] = "unhealthy"

    # Redis check
    try:
        redis = await aioredis.from_url(settings.REDIS_URL)
        await redis.ping()
        checks["checks"]["redis"] = {"status": "healthy", "response_time": 0.01}
    except Exception as e:
        checks["checks"]["redis"] = {"status": "unhealthy", "error": str(e)}
        checks["status"] = "unhealthy"

    return checks
```

## 🔧 Troubleshooting

### Common Issues and Solutions

#### 1. SSL Certificate Issues
```bash
# Check certificate expiry
openssl x509 -in /etc/nginx/ssl/preventia.com.crt -noout -dates

# Renew Let's Encrypt certificate
sudo certbot renew --nginx

# Test SSL configuration
sudo nginx -t
```

#### 2. Database Connection Issues
```bash
# Check PostgreSQL logs
docker-compose -f docker-compose.prod.yml logs postgres

# Check connection limits
docker-compose -f docker-compose.prod.yml exec postgres psql -U preventia -c "SELECT * FROM pg_stat_activity;"

# Reset connections
docker-compose -f docker-compose.prod.yml restart postgres
```

#### 3. High Memory Usage
```bash
# Check container memory usage
docker stats

# Check system memory
free -h

# Restart services if needed
docker-compose -f docker-compose.prod.yml restart api
```

#### 4. API Performance Issues
```bash
# Check API logs
docker-compose -f docker-compose.prod.yml logs api

# Monitor response times
curl -w "@curl-format.txt" -o /dev/null -s https://preventia.com/api/v1/health

# Scale API workers
docker-compose -f docker-compose.prod.yml up -d --scale api=3
```

## 📚 Related Documentation

- [Local Development Setup](../development/setup/local-development.md)
- [Environment Variables](../development/setup/environment-variables.md)
- [Monitoring Strategy](../monitoring/logging-strategy.md)
- [Security Standards](../../development/standards/security-standards.md)

---

**Production Deployment Principles:**
- **Security First**: All communications encrypted, minimal attack surface
- **High Availability**: Redundancy and graceful failure handling
- **Performance Optimized**: Sub-2s response times under load
- **Monitoring Complete**: Full observability into system health
- **Backup Strategy**: Regular automated backups with tested recovery

**Last Updated**: 2025-07-07
**Next Review**: 2025-08-07
**Maintainer**: Claude (Technical Director)
