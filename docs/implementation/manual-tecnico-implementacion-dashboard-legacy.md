# 📋 Manual Técnico de Implementación - PreventIA Dashboard Legacy

**Versión**: 1.0
**Fecha**: 2025-07-03
**Estado**: Production Ready
**Mantenedor**: Equipo Desarrollo PreventIA
**Documento**: Guía completa de implementación del dashboard legacy

---

## 📊 RESUMEN EJECUTIVO

PreventIA News Analytics Dashboard Legacy es un sistema completo de análisis de noticias médicas especializado en cáncer de mama. El sistema transforma datos no estructurados de múltiples fuentes en insights accionables mediante procesamiento de lenguaje natural y visualizaciones interactivas.

### Estado Actual
- **✅ PRODUCTION READY** - Sistema completo y funcional
- **106 artículos** procesados con análisis NLP completo
- **4 scrapers operativos** con integración Playwright
- **8 elementos críticos** del dashboard implementados
- **20+ endpoints API** con performance < 5s
- **Testing framework profesional** configurado

### Características Principales
- Dashboard analytics completo con 8 secciones
- Análisis de sentimiento con VADER especializado
- Clasificación de tópicos médicos
- Mapas geográficos con intensidad de cobertura
- Sistema de exportación con historial
- Arquitectura dual Professional/Educational

---

## 🏗️ ARQUITECTURA DEL SISTEMA

### Stack Tecnológico Completo

#### Frontend
```
React 19.1.0      - Framework principal
TypeScript 5.8.3  - Tipado estático
Vite 7.0.0        - Build tool optimizado
TailwindCSS 4.1.11 - Styling framework
Recharts 3.0.2    - Visualizaciones
Leaflet 1.9.4     - Mapas interactivos
```

#### Backend
```
FastAPI 0.115     - API REST framework
PostgreSQL 16     - Base de datos principal
Redis 8           - Caching y sesiones
SQLAlchemy 2.0    - ORM async
asyncpg 0.30      - Driver PostgreSQL
```

#### Infrastructure
```
Docker            - Containerización
Docker Compose    - Orquestación servicios
Nginx             - Reverse proxy
SSL/TLS           - Seguridad transporte
```

#### Testing & Quality
```
Vitest 3.2.4      - Testing frontend
Pytest            - Testing backend
Playwright        - E2E testing
ESLint            - Code quality
```

### Arquitectura de Componentes

```
┌─────────────────────────────────────────────────────────────┐
│                    FRONTEND LAYER                           │
├─────────────────────────────────────────────────────────────┤
│  React Dashboard (Port 3000/5173)                          │
│  ├── Legacy Components (8 elementos)                       │
│  ├── Professional Mode                                     │
│  ├── Educational Mode                                      │
│  └── Export System                                         │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                     API LAYER                              │
├─────────────────────────────────────────────────────────────┤
│  FastAPI (Port 8000)                                       │
│  ├── 20+ Endpoints                                         │
│  ├── OpenAPI Documentation                                 │
│  ├── Health Checks                                         │
│  └── Performance < 5s                                      │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                   DATABASE LAYER                           │
├─────────────────────────────────────────────────────────────┤
│  PostgreSQL (Port 5433)                                    │
│  ├── 106 Artículos procesados                              │
│  ├── NLP Analysis results                                  │
│  ├── Sentiment scores                                      │
│  └── Geographic data                                       │
└─────────────────────────────────────────────────────────────┘
```

### Modelo de Datos

#### Tablas Principales
```sql
-- Artículos con análisis NLP
articles (
    id, title, content, url,
    sentiment_label, sentiment_score,
    topic_category, publication_date,
    geographic_region, language
)

-- Fuentes de noticias
news_sources (
    id, name, url, scraper_type,
    is_active, last_scraped
)

-- Análisis semanal pre-calculado
weekly_analytics (
    id, week_start, article_count,
    sentiment_distribution, topic_breakdown
)
```

---

## 📋 PRERREQUISITOS

### Sistema Base Requerido

#### Hardware Mínimo
- **CPU**: 2 cores mínimo (4 cores recomendado)
- **RAM**: 8GB mínimo (16GB recomendado)
- **Storage**: 50GB disponible (100GB recomendado)
- **Network**: Conexión estable a internet

#### Software Requerido
```bash
# Sistema operativo
Ubuntu 20.04+ / CentOS 8+ / macOS 12+ / Windows 10+

# Contenedores
Docker 24.0+
Docker Compose 2.0+

# Desarrollo (opcional)
Node.js 18.0+
Python 3.11+
Git 2.30+
```

### Configuración de Red
```bash
# Puertos requeridos
3000/5173  - Frontend development
8000       - FastAPI backend
5433       - PostgreSQL database
6379       - Redis cache
80/443     - Production web server
```

### Variables de Entorno Críticas
```env
# Base de datos
DATABASE_URL=postgresql://preventia:password@localhost:5433/preventia_news
POSTGRES_DB=preventia_news
POSTGRES_USER=preventia
POSTGRES_PASSWORD=preventia123

# API Configuration
API_HOST=0.0.0.0
API_PORT=8000
API_RELOAD=false

# Frontend
VITE_API_URL=http://localhost:8000
NODE_ENV=development

# Optional
OPENAI_API_KEY=sk-...
REDIS_URL=redis://localhost:6379
```

---

## 🚀 INSTALACIÓN PASO A PASO

### PASO 1: Configuración Inicial

#### 1.1 Clonar Repositorio
```bash
# Clonar código fuente
git clone [repository-url]
cd preventia/news_bot_3

# Verificar branch
git branch
git status
```

#### 1.2 Configurar Variables de Entorno
```bash
# Copiar template
cp .env.template .env

# Editar configuración
nano .env
# Configurar DATABASE_URL, API keys, etc.
```

#### 1.3 Verificar Prerrequisitos
```bash
# Verificar Docker
docker --version
docker-compose --version

# Verificar puertos disponibles
netstat -tulpn | grep -E "(3000|8000|5433|6379)"
```

### PASO 2: Base de Datos

#### 2.1 Inicializar PostgreSQL
```bash
# Iniciar contenedor PostgreSQL
docker compose up postgres -d

# Verificar estado
docker compose ps
docker compose logs postgres

# Verificar conexión
docker compose exec postgres pg_isready -U preventia
```

#### 2.2 Verificar Esquema
```bash
# Conectar a base de datos
docker compose exec postgres psql -U preventia -d preventia_news

# Verificar tablas
\dt

# Verificar datos
SELECT COUNT(*) FROM articles;
SELECT COUNT(*) FROM news_sources;

# Salir
\q
```

#### 2.3 Poblar Datos (si es necesario)
```bash
# Ejecutar scrapers para poblar datos
python scripts/run_migrated_scrapers.py

# O ejecutar scraper específico
python scripts/run_migrated_scrapers.py webmd.com
```

### PASO 3: Backend API

#### 3.1 Configurar Python Environment
```bash
# Crear entorno virtual
python -m venv venv

# Activar entorno
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows

# Instalar dependencias
pip install -r requirements.txt
```

#### 3.2 Iniciar FastAPI
```bash
# Desarrollo
python -m services.api.main

# O usando Docker
docker compose up api -d

# Verificar API
curl http://localhost:8000/health
curl http://localhost:8000/docs
```

#### 3.3 Validar Endpoints
```bash
# Test endpoints principales
curl http://localhost:8000/api/v1/articles/ | jq
curl http://localhost:8000/api/v1/analytics/sentiment | jq
curl http://localhost:8000/api/v1/analytics/geographic | jq
```

### PASO 4: Frontend Dashboard

#### 4.1 Configurar Node.js
```bash
# Cambiar al directorio frontend
cd preventia-dashboard

# Instalar dependencias
npm install

# Verificar configuración
npm list --depth=0
```

#### 4.2 Iniciar en Modo Desarrollo
```bash
# Servidor desarrollo
npm run dev

# Verificar en navegador
open http://localhost:5173
```

#### 4.3 Build para Producción
```bash
# Crear build optimizado
npm run build

# Verificar bundle
ls -la dist/
du -sh dist/

# Probar build
npm run preview
```

### PASO 5: Configuración Completa

#### 5.1 Iniciar Stack Completo
```bash
# Regresar al directorio raíz
cd ..

# Iniciar todos los servicios
docker compose up -d

# Verificar estado
docker compose ps
```

#### 5.2 Validación Final
```bash
# Verificar servicios
curl http://localhost:8000/health
curl http://localhost:3000/

# Verificar logs
docker compose logs -f api
docker compose logs -f frontend
```

---

## 🧩 COMPONENTES LEGACY IMPLEMENTADOS

### 1. LegacySentimentChart

**Funcionalidad**: Visualización de análisis de sentimiento con soporte dual

```tsx
// Configuración básica
<LegacySentimentChart
  type="sentiment"           // 'sentiment' | 'language'
  showPieChart={true}        // Mostrar gráfico circular
  data={sentimentData}       // Datos de entrada
  title="Análisis de Sentimiento"
/>

// Datos esperados
interface SentimentData {
  label: string;
  value: number;
  color: string;
  percentage: number;
}
```

**Características**:
- Soporte para distribución de sentimientos y idiomas
- Gráfico circular con tooltips interactivos
- Colores personalizables por categoría
- Responsive design

### 2. LegacyTopicsChart

**Funcionalidad**: Visualización de tópicos médicos con breakdown por idioma

```tsx
// Configuración con breakdown
<LegacyTopicsChart
  showLanguageBreakdown={true}
  data={topicsData}
  title="Distribución de Tópicos"
/>

// Datos esperados
interface TopicData {
  topic: string;
  count: number;
  spanish: number;    // 36%
  english: number;    // 64%
}
```

**Características**:
- Barras duales por idioma (español/inglés)
- Colores diferenciados (azul/verde)
- Tooltips con desglose detallado
- 10 categorías médicas

### 3. LegacyGeographicMap

**Funcionalidad**: Mapa interactivo con leyenda de intensidad

```tsx
<LegacyGeographicMap
  data={geographicData}
  showIntensityLegend={true}
  title="Distribución Geográfica"
/>

// Datos esperados
interface GeographicData {
  region: string;
  count: number;
  intensity: 'low' | 'medium' | 'high';
  coordinates: [number, number];
}
```

**Características**:
- Leyenda de intensidad (azul claro → oscuro)
- Tooltips con información detallada
- Zoom y pan interactivo
- Markers con tamaño variable

### 4. LegacyExportHistory

**Funcionalidad**: Historial de exportaciones con gestión de archivos

```tsx
<LegacyExportHistory
  exports={exportHistory}
  onDownload={handleDownload}
  onDelete={handleDelete}
/>

// Datos esperados
interface ExportRecord {
  id: string;
  filename: string;
  size: string;
  status: 'completed' | 'failed';
  timestamp: Date;
  downloadUrl: string;
}
```

**Características**:
- Lista cronológica de exportaciones
- Estados visual (completado/fallido)
- Acciones (descargar/eliminar)
- Responsive design

### 5. Elementos Adicionales

#### 5.1 Export Progress Indicator
```tsx
// Estados de exportación
enum ExportStatus {
  PREPARING = 'Preparando exportación...',
  GENERATING = 'Generando archivo...',
  COMPLETED = 'Exportación completada',
  FAILED = 'Error en exportación'
}
```

#### 5.2 Sentiment Pie Chart
```tsx
// Configuración para gráfico circular
const sentimentConfig = {
  positive: { color: '#10b981', label: 'Positivo' },
  neutral: { color: '#6b7280', label: 'Neutral' },
  negative: { color: '#ef4444', label: 'Negativo' }
};
```

#### 5.3 Map Legend
```tsx
// Leyenda de intensidad
const intensityLevels = [
  { level: 'low', color: '#dbeafe', label: 'Baja' },
  { level: 'medium', color: '#3b82f6', label: 'Media' },
  { level: 'high', color: '#1e40af', label: 'Alta' }
];
```

---

## 🔧 CONFIGURACIÓN DE PRODUCCIÓN

### Docker Compose Producción

#### docker-compose.prod.yml
```yaml
version: '3.8'
services:
  # Frontend optimizado
  frontend:
    build:
      context: ./preventia-dashboard
      dockerfile: Dockerfile
      target: production
    environment:
      - NODE_ENV=production
      - VITE_API_URL=${PRODUCTION_API_URL}
    restart: unless-stopped
    depends_on:
      - api

  # API con optimizaciones
  api:
    build:
      context: .
      dockerfile: Dockerfile.api
    environment:
      - ENVIRONMENT=production
      - DATABASE_URL=${DATABASE_URL}
      - REDIS_URL=${REDIS_URL}
      - API_WORKERS=4
    restart: unless-stopped
    depends_on:
      - postgres
      - redis

  # PostgreSQL con persistencia
  postgres:
    image: postgres:16-alpine
    environment:
      - POSTGRES_DB=${POSTGRES_DB}
      - POSTGRES_USER=${POSTGRES_USER}
      - POSTGRES_PASSWORD=${POSTGRES_PASSWORD}
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./backups:/backups
    restart: unless-stopped

  # Redis para caching
  redis:
    image: redis:8-alpine
    restart: unless-stopped
    volumes:
      - redis_data:/data

  # Nginx reverse proxy
  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
      - ./ssl:/etc/nginx/ssl
    depends_on:
      - frontend
      - api
    restart: unless-stopped

volumes:
  postgres_data:
  redis_data:
```

### Nginx Configuration

#### nginx.conf
```nginx
events {
    worker_connections 1024;
}

http {
    upstream api {
        server api:8000;
    }

    upstream frontend {
        server frontend:3000;
    }

    # Redirect HTTP to HTTPS
    server {
        listen 80;
        server_name example.com;
        return 301 https://$server_name$request_uri;
    }

    # Main HTTPS server
    server {
        listen 443 ssl http2;
        server_name example.com;

        ssl_certificate /etc/nginx/ssl/cert.pem;
        ssl_certificate_key /etc/nginx/ssl/key.pem;

        # Frontend
        location / {
            proxy_pass http://frontend;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
        }

        # API
        location /api/ {
            proxy_pass http://api;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
        }

        # Health checks
        location /health {
            proxy_pass http://api;
        }
    }
}
```

### Variables de Producción

#### .env.production
```env
# Database
DATABASE_URL=postgresql://user:password@postgres:5432/preventia_news
POSTGRES_DB=preventia_news
POSTGRES_USER=preventia
POSTGRES_PASSWORD=secure_password_here

# API
API_HOST=0.0.0.0
API_PORT=8000
API_WORKERS=4
API_RELOAD=false

# Frontend
VITE_API_URL=https://api.example.com/api
NODE_ENV=production

# Security
SSL_CERT_PATH=/etc/nginx/ssl/cert.pem
SSL_KEY_PATH=/etc/nginx/ssl/key.pem

# Monitoring
SENTRY_DSN=https://...
NEW_RELIC_LICENSE_KEY=...
```

---

## 🧪 TESTING Y VALIDACIÓN

### Testing Framework

#### Estructura de Tests
```
tests/
├── unit/                 # Tests unitarios
│   ├── test_api/         # Tests API
│   └── test_nlp/         # Tests NLP
├── integration/          # Tests integración
│   ├── test_api/         # Tests API completos
│   └── test_database/    # Tests base de datos
├── e2e/                  # Tests end-to-end
│   └── test_dashboard/   # Tests dashboard
└── conftest.py          # Configuración pytest
```

#### Frontend Tests
```bash
# Tests unitarios
cd preventia-dashboard
npm run test:unit

# Tests con coverage
npm run test:coverage

# Tests E2E
npm run test:e2e

# Specific component tests
npx vitest run src/components/legacy/__tests__/
```

#### Backend Tests
```bash
# Setup testing environment
cd tests
source ../venv/bin/activate
pip install -r requirements-test.txt

# Run all tests
pytest

# Tests by category
pytest -m unit
pytest -m integration
pytest -m database

# Coverage report
pytest --cov=../services --cov-report=html
```

### Validation Checklist

#### Pre-deployment Validation
```bash
# 1. All tests passing
cd tests && pytest
cd preventia-dashboard && npm run test:unit

# 2. Build successful
cd preventia-dashboard && npm run build

# 3. Performance metrics
npm run build --report
ls -la dist/  # Check bundle size < 500KB

# 4. API health
curl http://localhost:8000/health
curl http://localhost:8000/docs

# 5. Database integrity
docker compose exec postgres psql -U preventia -d preventia_news \
  -c "SELECT COUNT(*) FROM articles;"
```

#### Production Readiness
```bash
# 1. Docker production build
docker-compose -f docker-compose.prod.yml build

# 2. Security scan
docker scan preventia_api
docker scan preventia_frontend

# 3. Performance test
ab -n 1000 -c 10 http://localhost:8000/api/v1/articles/

# 4. Load test
hey -n 1000 -c 50 http://localhost:3000/

# 5. SSL verification
openssl s_client -connect example.com:443 -servername example.com
```

---

## 🔧 MANTENIMIENTO Y MONITOREO

### Health Checks

#### Automated Health Monitoring
```bash
# API health check
curl -f http://localhost:8000/health || exit 1

# Database health
docker compose exec postgres pg_isready -U preventia || exit 1

# Frontend health
curl -f http://localhost:3000/ || exit 1

# Redis health
docker compose exec redis redis-cli ping || exit 1
```

#### Monitoring Script
```bash
#!/bin/bash
# health-check.sh

echo "=== PreventIA Health Check ==="
echo "Timestamp: $(date)"

# Check API
if curl -f http://localhost:8000/health > /dev/null 2>&1; then
  echo "✅ API: Healthy"
else
  echo "❌ API: Unhealthy"
fi

# Check Database
if docker compose exec postgres pg_isready -U preventia > /dev/null 2>&1; then
  echo "✅ Database: Healthy"
else
  echo "❌ Database: Unhealthy"
fi

# Check Frontend
if curl -f http://localhost:3000/ > /dev/null 2>&1; then
  echo "✅ Frontend: Healthy"
else
  echo "❌ Frontend: Unhealthy"
fi

echo "=== End Health Check ==="
```

### Backup Procedures

#### Database Backup
```bash
# Daily backup
docker compose exec postgres pg_dump -U preventia preventia_news > backup_$(date +%Y%m%d).sql

# Automated backup script
#!/bin/bash
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="/backups"
BACKUP_FILE="preventia_backup_${DATE}.sql"

# Create backup
docker compose exec postgres pg_dump -U preventia preventia_news > "${BACKUP_DIR}/${BACKUP_FILE}"

# Compress backup
gzip "${BACKUP_DIR}/${BACKUP_FILE}"

# Remove old backups (keep last 7 days)
find ${BACKUP_DIR} -name "*.gz" -mtime +7 -delete

echo "Backup completed: ${BACKUP_FILE}.gz"
```

#### Log Management
```bash
# View logs
docker compose logs -f api
docker compose logs -f frontend
docker compose logs -f postgres

# Log rotation
docker compose exec postgres logrotate /etc/logrotate.conf

# Clear old logs
docker system prune -f
```

### Performance Monitoring

#### Key Metrics
```bash
# API response times
curl -w "@curl-format.txt" -o /dev/null -s http://localhost:8000/api/v1/articles/

# Database performance
docker compose exec postgres psql -U preventia -d preventia_news \
  -c "SELECT query, mean_time, calls FROM pg_stat_statements ORDER BY mean_time DESC LIMIT 10;"

# Memory usage
docker stats --no-stream

# Disk usage
df -h
du -sh /var/lib/docker/
```

#### Performance Optimization
```bash
# Optimize database
docker compose exec postgres psql -U preventia -d preventia_news \
  -c "VACUUM ANALYZE;"

# Clear Redis cache
docker compose exec redis redis-cli FLUSHALL

# Optimize frontend bundle
cd preventia-dashboard
npm run build --analyze
```

---

## 🚨 SOLUCIÓN DE PROBLEMAS

### Problemas Comunes

#### 1. Database Connection Issues
```bash
# Síntoma: Error connecting to database
# Causa: PostgreSQL no iniciado o configuración incorrecta

# Solución:
docker compose up postgres -d
docker compose logs postgres
docker compose exec postgres pg_isready -U preventia

# Verificar variables
echo $DATABASE_URL
```

#### 2. API 500 Internal Server Error
```bash
# Síntoma: API endpoints devuelven 500
# Causa: Error en backend o base de datos

# Solución:
docker compose logs api
python -m services.api.main  # Run in development mode
tail -f logs/api.log
```

#### 3. Frontend 404 Not Found
```bash
# Síntoma: Frontend muestra 404 para API calls
# Causa: VITE_API_URL mal configurado

# Solución:
echo $VITE_API_URL
# Debe ser: http://localhost:8000/api

# Verificar en navegador
curl http://localhost:8000/api/v1/articles/
```

#### 4. Build Failures
```bash
# Síntoma: npm run build falla
# Causa: Dependencias o TypeScript errors

# Solución:
cd preventia-dashboard
npm install
npm run lint
npm run build --verbose
```

#### 5. Docker Issues
```bash
# Síntoma: Contenedores no inician
# Causa: Puertos ocupados o recursos insuficientes

# Solución:
docker compose down
docker system prune -f
docker compose up -d
docker compose ps
```

### Comandos de Diagnóstico

#### System Status
```bash
# Estado general del sistema
docker compose ps
docker compose logs --tail=50
docker stats --no-stream

# Espacio en disco
df -h
du -sh /var/lib/docker/

# Puertos en uso
netstat -tulpn | grep -E "(3000|8000|5433|6379)"
```

#### Database Diagnostics
```bash
# Conexión a base de datos
docker compose exec postgres psql -U preventia -d preventia_news

# Verificar tablas
\dt

# Verificar datos
SELECT COUNT(*) FROM articles;
SELECT sentiment_label, COUNT(*) FROM articles GROUP BY sentiment_label;

# Performance queries
SELECT query, mean_time FROM pg_stat_statements ORDER BY mean_time DESC LIMIT 5;
```

#### API Diagnostics
```bash
# Test endpoints
curl -v http://localhost:8000/health
curl -v http://localhost:8000/docs
curl -v http://localhost:8000/api/v1/articles/ | jq

# Performance test
time curl http://localhost:8000/api/v1/analytics/sentiment
```

#### Frontend Diagnostics
```bash
# Build analysis
cd preventia-dashboard
npm run build --analyze

# Bundle size check
ls -la dist/
du -sh dist/

# Development server
npm run dev --verbose
```

---

## 📈 ROADMAP DE MEJORAS

### Fase 1: Optimización Inmediata (1-2 semanas)

#### Performance
- [ ] Lazy loading para componentes pesados
- [ ] Image optimization y CDN
- [ ] API response caching con Redis
- [ ] Database query optimization
- [ ] Bundle splitting más granular

#### Security
- [ ] Rate limiting implementation
- [ ] Input validation enhancement
- [ ] Security headers configuration
- [ ] CSRF protection
- [ ] SQL injection prevention

### Fase 2: Funcionalidades Avanzadas (1-2 meses)

#### Features
- [ ] Real-time updates con WebSockets
- [ ] Advanced filtering system
- [ ] User authentication y roles
- [ ] Scheduled exports
- [ ] Email notifications

#### Analytics
- [ ] Predictive analytics con ML
- [ ] Advanced sentiment analysis
- [ ] Trend prediction
- [ ] Anomaly detection
- [ ] Custom dashboards

### Fase 3: Escalabilidad (2-3 meses)

#### Infrastructure
- [ ] Kubernetes deployment
- [ ] Microservices architecture
- [ ] Load balancing
- [ ] Auto-scaling
- [ ] Multi-region deployment

#### Monitoring
- [ ] Comprehensive logging
- [ ] APM integration
- [ ] Custom metrics
- [ ] Alerting system
- [ ] SLA monitoring

---

## 📞 SOPORTE Y DOCUMENTACIÓN

### Recursos Adicionales

#### Documentación Técnica
- `docs/api/services/nlp-api.md` - API NLP documentation
- `docs/architecture/system-overview.md` - System architecture
- `docs/development/setup/local-development.md` - Local setup guide
- `docs/implementation/production-deployment-roadmap.md` - Production roadmap

#### Guías de Desarrollo
- `docs/development/standards/git-workflow.md` - Git workflow
- `docs/development/standards/testing-strategy.md` - Testing strategy
- `docs/development/standards/documentation-standards.md` - Documentation standards

#### Decisiones de Arquitectura
- `docs/decisions/ADR-001-project-scope-change.md` - Project scope
- `docs/decisions/ADR-002-database-architecture.md` - Database architecture
- `docs/decisions/ADR-004-nlp-sentiment-analysis.md` - NLP strategy

### Contacto y Soporte

#### Equipo de Desarrollo
- **Maintainer**: Equipo Desarrollo PreventIA
- **Repository**: [GitHub Repository]
- **Documentation**: `docs/README.md`

#### Escalación de Issues
1. **Nivel 1**: Consultar documentación y troubleshooting
2. **Nivel 2**: Revisar logs y ejecutar diagnósticos
3. **Nivel 3**: Contactar equipo de desarrollo
4. **Nivel 4**: Escalación a arquitectos de sistema

---

## 🎯 CRITERIOS DE ÉXITO

### Métricas Técnicas
- **Uptime**: > 99.9%
- **Response Time**: < 2 segundos promedio
- **Error Rate**: < 0.1%
- **Build Time**: < 5 minutos
- **Bundle Size**: < 500KB

### Métricas de Calidad
- **Test Coverage**: > 85%
- **Code Quality**: Grade A (SonarQube)
- **Security Score**: Grade A (OWASP)
- **Performance Score**: > 90 (Lighthouse)
- **Accessibility Score**: > 95 (WCAG)

### Métricas de Producto
- **Feature Adoption**: > 80%
- **User Satisfaction**: > 4.5/5
- **Data Accuracy**: 100%
- **Export Success Rate**: > 99%
- **Time to Insight**: < 30 segundos

---

## 📋 CHECKLIST DE IMPLEMENTACIÓN

### Pre-implementación
- [ ] Verificar prerrequisitos de sistema
- [ ] Configurar variables de entorno
- [ ] Validar conectividad de red
- [ ] Verificar permisos de usuario
- [ ] Backup de configuraciones existentes

### Implementación
- [ ] Clonar repositorio
- [ ] Configurar base de datos
- [ ] Inicializar servicios backend
- [ ] Configurar frontend
- [ ] Ejecutar tests de validación

### Post-implementación
- [ ] Verificar health checks
- [ ] Validar funcionalidades críticas
- [ ] Configurar monitoreo
- [ ] Documentar configuración específica
- [ ] Capacitar usuarios finales

### Producción
- [ ] Configurar SSL/TLS
- [ ] Implementar backup automático
- [ ] Configurar alertas
- [ ] Validar performance bajo carga
- [ ] Documentar procedimientos operacionales

---

**📍 ESTADO ACTUAL: PRODUCTION READY**

Este manual técnico cubre la implementación completa del PreventIA Dashboard Legacy. El sistema está listo para producción con todas las funcionalidades críticas implementadas y validadas.

**Última actualización**: 2025-07-03
**Versión del manual**: 1.0
**Próxima revisión**: Post-deployment

---

*Para soporte técnico adicional, consultar la documentación completa en `docs/` o contactar al equipo de desarrollo.*
