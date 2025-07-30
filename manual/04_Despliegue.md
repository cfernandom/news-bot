# 4. Despliegue y Configuración de Producción

## Índice del Contenido

1. [Arquitectura de Despliegue](#arquitectura-de-despliegue)
2. [Despliegue con Docker](#despliegue-con-docker)
3. [Configuración de Producción](#configuración-de-producción)
4. [Monitoreo y Logging](#monitoreo-y-logging)
5. [Respaldos y Recuperación](#respaldos-y-recuperación)
6. [Escalamiento](#escalamiento)
7. [Seguridad en Producción](#seguridad-en-producción)

## Arquitectura de Despliegue

### Diagrama de Despliegue

```mermaid
graph TB
    subgraph "Internet"
        I[Users]
    end

    subgraph "DMZ"
        LB[Load Balancer<br/>Nginx]
        FW1[Firewall]
    end

    subgraph "Application Tier"
        WEB1[Frontend Container<br/>React - Port 3000]
        WEB2[Frontend Container<br/>React - Port 3001]
        API1[API Container<br/>FastAPI - Port 8000]
        API2[API Container<br/>FastAPI - Port 8001]
    end

    subgraph "Service Tier"
        ANALYTICS[Analytics Service]
        SCRAPER[Scraper Service]
        NLP[NLP Service]
    end

    subgraph "Data Tier"
        DB[(PostgreSQL<br/>Primary)]
        DB2[(PostgreSQL<br/>Replica)]
        REDIS[(Redis Cluster)]
    end

    subgraph "Storage"
        S3[Object Storage<br/>Exports/Backups]
        LOGS[Log Storage]
    end

    I --> FW1
    FW1 --> LB
    LB --> WEB1
    LB --> WEB2
    LB --> API1
    LB --> API2

    API1 --> ANALYTICS
    API2 --> ANALYTICS
    API1 --> SCRAPER
    API2 --> SCRAPER

    SCRAPER --> NLP

    API1 --> DB
    API2 --> DB
    API1 --> REDIS
    API2 --> REDIS

    DB --> DB2

    ANALYTICS --> S3
    API1 --> LOGS
    API2 --> LOGS
```

### Especificaciones del Servidor de Producción

| Componente | Mínimo | Recomendado | Óptimo |
|------------|---------|-------------|---------|
| **CPU** | 4 cores | 8 cores | 16 cores |
| **RAM** | 8 GB | 16 GB | 32 GB |
| **Almacenamiento** | 100 GB SSD | 250 GB SSD | 500 GB NVMe |
| **Red** | 100 Mbps | 1 Gbps | 10 Gbps |
| **OS** | Ubuntu 20.04 | Ubuntu 22.04 | Ubuntu 22.04 |

## Despliegue con Docker

### Docker Compose para Producción

```yaml
# docker-compose.prod.yml
version: '3.9'

services:
  postgres:
    image: postgres:16-alpine
    container_name: preventia_postgres
    restart: always
    environment:
      - POSTGRES_DB=${POSTGRES_DB}
      - POSTGRES_USER=${POSTGRES_USER}
      - POSTGRES_PASSWORD=${POSTGRES_PASSWORD}
      - POSTGRES_INITDB_ARGS=--encoding=UTF8 --locale=C
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./backups:/backups
    ports:
      - "127.0.0.1:5432:5432"
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U ${POSTGRES_USER}"]
      interval: 30s
      timeout: 10s
      retries: 5
    deploy:
      resources:
        limits:
          cpus: '2'
          memory: 4G
        reservations:
          cpus: '1'
          memory: 2G

  api:
    build:
      context: .
      dockerfile: Dockerfile.api
      args:
        - ENVIRONMENT=production
    container_name: preventia_api
    restart: always
    env_file:
      - .env.production
    environment:
      - API_HOST=0.0.0.0
      - API_PORT=8000
      - API_RELOAD=false
      - LOG_LEVEL=info
    volumes:
      - ./logs:/app/logs
      - ./exports:/app/exports
    depends_on:
      postgres:
        condition: service_healthy
      redis:
        condition: service_healthy
    ports:
      - "127.0.0.1:8000:8000"
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
    deploy:
      replicas: 2
      resources:
        limits:
          cpus: '2'
          memory: 2G

  frontend:
    build:
      context: ./preventia-dashboard
      dockerfile: Dockerfile.prod
    container_name: preventia_frontend
    restart: always
    environment:
      - NODE_ENV=production
      - VITE_API_URL=https://api.preventia.com
    ports:
      - "127.0.0.1:3000:80"
    healthcheck:
      test: ["CMD", "wget", "--spider", "http://localhost:80"]
      interval: 30s
      timeout: 10s
      retries: 3
    deploy:
      replicas: 2
      resources:
        limits:
          cpus: '1'
          memory: 1G

  redis:
    image: redis:8-alpine
    container_name: preventia_redis
    restart: always
    command: redis-server --maxmemory 512mb --maxmemory-policy allkeys-lru
    volumes:
      - redis_data:/data
    ports:
      - "127.0.0.1:6379:6379"
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 30s
      timeout: 10s
      retries: 3

  analytics_service:
    build:
      context: .
      dockerfile: Dockerfile
    container_name: preventia_analytics
    restart: always
    env_file:
      - .env.production
    volumes:
      - ./logs:/app/logs
    depends_on:
      - postgres
      - redis
    deploy:
      resources:
        limits:
          cpus: '2'
          memory: 4G

volumes:
  postgres_data:
    driver: local
  redis_data:
    driver: local

networks:
  default:
    driver: bridge
    ipam:
      config:
        - subnet: 172.20.0.0/16
```

### Dockerfile Optimizado para Producción

```dockerfile
# Dockerfile.api
FROM python:3.13-slim AS builder

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Crear directorio de trabajo
WORKDIR /app

# Copiar requirements y instalar dependencias
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Etapa final
FROM python:3.13-slim

# Instalar solo runtime dependencies
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Crear usuario no-root
RUN useradd -m -u 1000 appuser

WORKDIR /app

# Copiar dependencias desde builder
COPY --from=builder /usr/local/lib/python3.13/site-packages /usr/local/lib/python3.13/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Copiar código de la aplicación
COPY --chown=appuser:appuser . .

# Cambiar a usuario no-root
USER appuser

# Exponer puerto
EXPOSE 8000

# Comando de inicio
CMD ["uvicorn", "services.api.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]
```

## Configuración de Producción

### Variables de Entorno de Producción

```bash
# .env.production
# Base de Datos
POSTGRES_DB=preventia_news_prod
POSTGRES_USER=preventia_prod
POSTGRES_PASSWORD=${DB_PASSWORD} # Usar secreto externo
DATABASE_URL=postgresql://preventia_prod:${DB_PASSWORD}@postgres:5432/preventia_news_prod

# API Configuration
API_HOST=0.0.0.0
API_PORT=8000
API_WORKERS=4
LOG_LEVEL=info
ENVIRONMENT=production

# Security
JWT_SECRET_KEY=${JWT_SECRET} # Usar secreto externo
JWT_ALGORITHM=HS256
JWT_EXPIRATION_HOURS=24

# Redis
REDIS_URL=redis://redis:6379/0

# External Services
OPENAI_API_KEY=${OPENAI_KEY} # Usar secreto externo

# Monitoring
SENTRY_DSN=${SENTRY_DSN}
ENABLE_METRICS=true
METRICS_PORT=9090
```

### Configuración de Nginx para Producción

```nginx
# /etc/nginx/sites-available/preventia
upstream api_backend {
    least_conn;
    server 127.0.0.1:8000 max_fails=3 fail_timeout=30s;
    server 127.0.0.1:8001 max_fails=3 fail_timeout=30s;
}

upstream frontend_backend {
    least_conn;
    server 127.0.0.1:3000 max_fails=3 fail_timeout=30s;
    server 127.0.0.1:3001 max_fails=3 fail_timeout=30s;
}

# Rate limiting
limit_req_zone $binary_remote_addr zone=api_limit:10m rate=10r/s;
limit_req_zone $binary_remote_addr zone=login_limit:10m rate=5r/m;

server {
    listen 80;
    server_name preventia.com www.preventia.com;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name preventia.com www.preventia.com;

    # SSL Configuration
    ssl_certificate /etc/letsencrypt/live/preventia.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/preventia.com/privkey.pem;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;
    ssl_prefer_server_ciphers on;

    # Security Headers
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;

    # Frontend
    location / {
        proxy_pass http://frontend_backend;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;

        # Cache static assets
        location ~* \.(js|css|png|jpg|jpeg|gif|ico|svg)$ {
            expires 1y;
            add_header Cache-Control "public, immutable";
        }
    }

    # API
    location /api {
        limit_req zone=api_limit burst=20 nodelay;

        proxy_pass http://api_backend;
        proxy_http_version 1.1;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header Host $host;
        proxy_set_header X-Forwarded-Proto $scheme;

        # Timeouts
        proxy_connect_timeout 60s;
        proxy_send_timeout 60s;
        proxy_read_timeout 60s;
    }

    # Special rate limit for login
    location /api/auth/login {
        limit_req zone=login_limit burst=2 nodelay;
        proxy_pass http://api_backend;
        proxy_http_version 1.1;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header Host $host;
    }

    # Health check endpoint (no rate limit)
    location /health {
        proxy_pass http://api_backend;
        access_log off;
    }
}
```

## Monitoreo y Logging

### Stack de Monitoreo

```yaml
# monitoring/docker-compose.yml
version: '3.9'

services:
  prometheus:
    image: prom/prometheus:latest
    container_name: prometheus
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml
      - prometheus_data:/prometheus
    ports:
      - "9090:9090"
    command:
      - '--config.file=/etc/prometheus/prometheus.yml'
      - '--storage.tsdb.path=/prometheus'

  grafana:
    image: grafana/grafana:latest
    container_name: grafana
    volumes:
      - grafana_data:/var/lib/grafana
      - ./grafana/dashboards:/etc/grafana/provisioning/dashboards
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=${GRAFANA_PASSWORD}
      - GF_USERS_ALLOW_SIGN_UP=false
    ports:
      - "3001:3000"

  loki:
    image: grafana/loki:latest
    container_name: loki
    ports:
      - "3100:3100"
    volumes:
      - ./loki-config.yml:/etc/loki/local-config.yaml
      - loki_data:/loki

  promtail:
    image: grafana/promtail:latest
    container_name: promtail
    volumes:
      - ./promtail-config.yml:/etc/promtail/config.yml
      - /var/log:/var/log
      - ../logs:/app/logs
    command: -config.file=/etc/promtail/config.yml

volumes:
  prometheus_data:
  grafana_data:
  loki_data:
```

### Configuración de Logging

```python
# services/shared/logging_config.py
import logging
import sys
from pythonjsonlogger import jsonlogger

def setup_logging(level="INFO"):
    """Configurar logging estructurado para producción"""

    # Formato JSON para logs
    logHandler = logging.StreamHandler(sys.stdout)
    formatter = jsonlogger.JsonFormatter(
        fmt='%(asctime)s %(levelname)s %(name)s %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    logHandler.setFormatter(formatter)

    # Configurar root logger
    logging.root.setLevel(level)
    logging.root.addHandler(logHandler)

    # Configurar loggers específicos
    logging.getLogger("uvicorn.access").setLevel(logging.WARNING)
    logging.getLogger("sqlalchemy.engine").setLevel(logging.WARNING)

    return logging.getLogger(__name__)
```

## Respaldos y Recuperación

### Script de Respaldo Automático

```bash
#!/bin/bash
# backup.sh - Script de respaldo automático

set -e

# Configuración
BACKUP_DIR="/backups"
RETENTION_DAYS=30
DB_NAME="preventia_news_prod"
DB_USER="preventia_prod"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)

# Crear directorio de respaldo
mkdir -p ${BACKUP_DIR}/{database,files,configs}

echo "🔄 Iniciando respaldo ${TIMESTAMP}..."

# Respaldo de base de datos
echo "💾 Respaldando base de datos..."
docker-compose exec -T postgres pg_dump \
    -U ${DB_USER} \
    -d ${DB_NAME} \
    --format=custom \
    --compress=9 \
    > ${BACKUP_DIR}/database/db_${TIMESTAMP}.dump

# Respaldo de archivos exportados
echo "📁 Respaldando archivos exportados..."
tar -czf ${BACKUP_DIR}/files/exports_${TIMESTAMP}.tar.gz \
    -C /app exports/

# Respaldo de configuraciones
echo "⚙️ Respaldando configuraciones..."
tar -czf ${BACKUP_DIR}/configs/config_${TIMESTAMP}.tar.gz \
    .env.production \
    docker-compose.prod.yml \
    nginx/

# Verificar respaldos
echo "✅ Verificando respaldos..."
pg_restore --list ${BACKUP_DIR}/database/db_${TIMESTAMP}.dump > /dev/null

# Limpiar respaldos antiguos
echo "🧹 Limpiando respaldos antiguos..."
find ${BACKUP_DIR} -type f -mtime +${RETENTION_DAYS} -delete

# Sincronizar con almacenamiento remoto (opcional)
if [ ! -z "$S3_BUCKET" ]; then
    echo "☁️ Sincronizando con S3..."
    aws s3 sync ${BACKUP_DIR} s3://${S3_BUCKET}/backups/ \
        --exclude "*.tmp" \
        --delete
fi

echo "✅ Respaldo completado: ${TIMESTAMP}"
```

### Procedimiento de Recuperación

```bash
#!/bin/bash
# restore.sh - Script de recuperación

set -e

# Verificar argumentos
if [ "$#" -ne 1 ]; then
    echo "Uso: $0 <timestamp>"
    echo "Ejemplo: $0 20240729_120000"
    exit 1
fi

TIMESTAMP=$1
BACKUP_DIR="/backups"

echo "🔄 Iniciando recuperación desde ${TIMESTAMP}..."

# Detener servicios
echo "🛑 Deteniendo servicios..."
docker-compose stop api frontend analytics_service

# Restaurar base de datos
echo "💾 Restaurando base de datos..."
docker-compose exec -T postgres pg_restore \
    --clean \
    --if-exists \
    -U preventia_prod \
    -d preventia_news_prod \
    < ${BACKUP_DIR}/database/db_${TIMESTAMP}.dump

# Restaurar archivos
echo "📁 Restaurando archivos..."
tar -xzf ${BACKUP_DIR}/files/exports_${TIMESTAMP}.tar.gz \
    -C /app/

# Reiniciar servicios
echo "🚀 Reiniciando servicios..."
docker-compose start api frontend analytics_service

# Verificar salud
echo "🏥 Verificando salud del sistema..."
sleep 10
curl -f http://localhost:8000/health || exit 1

echo "✅ Recuperación completada"
```

## Escalamiento

### Escalamiento Horizontal

```bash
# Escalar API a 4 réplicas
docker-compose up -d --scale api=4

# Escalar frontend a 3 réplicas
docker-compose up -d --scale frontend=3
```

### Configuración de Auto-scaling (Kubernetes)

```yaml
# k8s/api-hpa.yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: api-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: preventia-api
  minReplicas: 2
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
  - type: Resource
    resource:
      name: memory
      target:
        type: Utilization
        averageUtilization: 80
```

## Seguridad en Producción

### Checklist de Seguridad

- [ ] **SSL/TLS configurado** con certificados válidos
- [ ] **Firewall configurado** con reglas restrictivas
- [ ] **Secretos externalizados** (no en código)
- [ ] **Actualizaciones automáticas** de seguridad
- [ ] **Monitoreo de seguridad** activo
- [ ] **Respaldos encriptados**
- [ ] **Logs de auditoría** habilitados
- [ ] **Rate limiting** configurado
- [ ] **CORS restrictivo**
- [ ] **Headers de seguridad** configurados

### Script de Hardening

```bash
#!/bin/bash
# security-hardening.sh

# Deshabilitar servicios innecesarios
systemctl disable bluetooth
systemctl disable cups

# Configurar firewall
ufw default deny incoming
ufw default allow outgoing
ufw allow 22/tcp  # SSH
ufw allow 80/tcp  # HTTP
ufw allow 443/tcp # HTTPS
ufw --force enable

# Configurar fail2ban
apt-get install -y fail2ban
cp /etc/fail2ban/jail.conf /etc/fail2ban/jail.local

# Configurar auditoría
apt-get install -y auditd
systemctl enable auditd

# Configurar límites del sistema
cat >> /etc/security/limits.conf <<EOF
* soft nofile 65536
* hard nofile 65536
* soft nproc 32768
* hard nproc 32768
EOF

# Deshabilitar root SSH
sed -i 's/PermitRootLogin yes/PermitRootLogin no/' /etc/ssh/sshd_config
systemctl restart sshd

echo "✅ Hardening completado"
```

---

*Siguiente: [05. Resolución de Problemas](05_ResolucionProblemas.md)*
