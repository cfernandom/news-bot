# System Overview - PreventIA News Analytics

---
**Document Metadata**
- **Version**: 1.1
- **Last Updated**: 2025-06-28
- **Maintainer**: Technical Team
- **Category**: Architecture
- **Priority**: High
- **Status**: Approved
- **Language**: English (Technical Standard)
---

## General Vision
PreventIA News Analytics is a media intelligence system specialized in automated analysis of breast cancer news. It transforms unstructured data from multiple sources into actionable insights through natural language processing and interactive visualizations.

## Main Objectives
- **Automated monitoring** of breast cancer media coverage
- **Trend analysis** across different countries and languages
- **Market intelligence** for decision makers
- **Interactive visualization** of patterns and insights

## High-Level Architecture

```mermaid
graph TB
    subgraph "Data Sources"
        S1[Medical News Sites]
        S2[Scientific Publications] 
        S3[Health Organizations]
        S4[News Aggregators]
    end

    subgraph "Collection Layer"
        SC[Smart Scrapers]
        SV[Source Validator]
        FT[Full-text Extractor]
    end

    subgraph "Processing Layer"
        NLP[NLP Analyzer]
        SA[Sentiment Analysis]
        TC[Topic Classifier]
        GC[Geographic Classifier]
    end

    subgraph "Storage Layer"
        PG[(PostgreSQL)]
        RD[(Redis Cache)]
    end

    subgraph "Analytics Layer"
        AG[Data Aggregator]
        TR[Trend Analyzer]
        SG[Summary Generator]
        WA[Weekly Analytics]
    end

    subgraph "API Layer"
        API[FastAPI REST]
        WS[WebSocket Real-time]
        EX[Export Service]
    end

    subgraph "Frontend Layer"
        DB[React Dashboard]
        VZ[Data Visualizations]
        MP[Interactive Maps]
        RP[Report Generator]
    end

    S1 --> SC
    S2 --> SC
    S3 --> SC
    S4 --> SC
    
    SC --> SV
    SV --> FT
    FT --> NLP
    
    NLP --> SA
    NLP --> TC
    NLP --> GC
    
    SA --> PG
    TC --> PG
    GC --> PG
    
    PG --> AG
    PG --> TR
    AG --> SG
    TR --> WA
    
    WA --> RD
    SG --> RD
    
    RD --> API
    API --> WS
    API --> EX
    
    API --> DB
    WS --> VZ
    EX --> RP
    DB --> MP
```

## System Components

### 1. Collection Layer
**Purpose**: Intelligent and validated content extraction from web sources

#### Smart Scrapers
- Site-specific scrapers
- Automatic content structure detection
- Intelligent rate limiting
- Duplicate detection by content hash

#### Source Validator
- Automatic validation of new sources
- Verification of robots.txt and policies
- Extraction testing before activation
- Health monitoring of existing sources

#### Full-text Extractor
- Complete article content extraction
- Text cleaning and normalization
- Automatic language detection
- Important metadata preservation

### 2. Processing Layer
**Purpose**: Intelligent analysis and content enrichment

#### NLP Analyzer
- Keyword extraction with relevance
- Medical entity detection
- Content structure analysis
- Source quality classification

#### Sentiment Analysis ✅ **IMPLEMENTADO**
- **106 artículos procesados** con sentiment analysis (100% coverage)
- **Distribution**: Negative 74.5% (79 articles), Positive 22.6% (24 articles), Neutral 2.8% (3 articles)
- **VADER + spaCy**: Specialized for medical content with conservative thresholds
- **Performance**: ~2 articles/second batch processing
- **Medical optimization**: Compound threshold ±0.3 for strong sentiment classification

#### Topic Classifier ✅ **IMPLEMENTADO**
- **106 artículos clasificados** en 10 categorías médicas:
  - Treatment (36.8% - 39 artículos)
  - Research (17.9% - 19 artículos)
  - General (17.9% - 19 artículos)
  - Surgery (11.3% - 12 artículos)
  - Genetics, Diagnosis, Lifestyle (3.8% cada una)
  - Screening (2.8%), Support, Policy (0.9% cada una)
- **Rule-based keyword matching** con weighted scoring
- **High confidence scoring**: Surgery 88.3%, Diagnosis 83.3%, Genetics 82.0%
- **Batch processing**: 106 artículos en ~30 segundos

#### Geographic Classifier
- Identificación automática de país/región
- Clasificación por relevancia geográfica
- Detección de estudios multi-país
- Mapeo a códigos ISO estándar

### 3. Storage Layer (Capa de Almacenamiento)
**Propósito**: Persistencia optimizada para analytics y performance

#### PostgreSQL Database
- **Schema híbrido**: ORM para CRUD, raw SQL para analytics
- **Indexing inteligente**: Optimizado para queries de dashboard
- **JSONB columns**: Flexibilidad para metadata variable
- **Temporal queries**: Optimizado para análisis de tendencias

#### Redis Cache
- Cache de consultas frecuentes del dashboard
- Session storage para usuarios
- Real-time data para WebSocket updates
- Rate limiting para APIs

### 4. Analytics Layer (Capa de Análisis)
**Propósito**: Generación de insights y métricas agregadas

#### Data Aggregator
- Pre-cálculo de métricas semanales/mensuales
- Agregaciones por país, idioma, tema
- Pipeline de procesamiento batch
- Optimización para performance del dashboard

#### Trend Analyzer
- Detección de trending topics
- Análisis de crecimiento/decrecimiento
- Comparaciones temporales
- Identificación de anomalías

#### Summary Generator
- Resúmenes automáticos con LLM
- Insights clave del período
- Contexto de tendencias importantes
- Personalización por audiencia

### 5. API Layer (Capa de APIs)
**Propósito**: Interface programática para frontend y integraciones

#### FastAPI REST
- **CRUD Operations**: Gestión de fuentes y artículos
- **Analytics Endpoints**: Datos para visualizaciones
- **Export APIs**: Múltiples formatos (CSV, JSON, PDF)
- **Authentication**: JWT tokens para seguridad

#### WebSocket Real-time
- Updates en tiempo real del dashboard
- Notificaciones de nuevos artículos importantes
- Status de procesamiento en vivo
- Collaborative features

#### Export Service
- Generación de reportes personalizados
- Múltiples formatos de salida
- Filtros avanzados por fecha/región/tema
- Historial de exportaciones

### 6. Frontend Layer (Capa de Presentación)
**Propósito**: Interface de usuario interactiva y visualizaciones

#### React Dashboard
- **Resumen Semanal**: Métricas clave y tendencias
- **Explorador Temático**: Filtros y segmentación avanzada
- **Análisis de Tono**: Distribución de sentimientos
- **Timeline Interactive**: Evolución temporal

#### Data Visualizations
- Charts responsivos con D3.js/Chart.js
- Visualizaciones interactivas
- Export de gráficos en múltiples formatos
- Personalización de visualizaciones

#### Interactive Maps
- Mapa mundial con Leaflet.js
- Burbujas proporcionales por volumen
- Filtros por idioma y categoría
- Drill-down por país/región

## Flujo de Datos Principales

### 1. Article Processing Pipeline
```
Web Sources → Scrapers → Validation → Full-text Extraction → 
NLP Analysis → Sentiment/Topic Classification → Database Storage → 
Cache Update → Dashboard Refresh
```

### 2. Analytics Generation Pipeline
```
Raw Articles → Weekly Aggregation → Trend Analysis → 
LLM Summary Generation → Cache Storage → API Serving → 
Dashboard Visualization
```

### 3. Real-time Updates Pipeline
```
New Article Detection → Processing Queue → Analysis → 
WebSocket Notification → Dashboard Update → User Notification
```

## Tecnologías Utilizadas

### Backend
- **Python 3.13+**: Lenguaje principal
- **FastAPI**: Framework web moderno y rápido
- **PostgreSQL 16+**: Base de datos principal
- **Redis**: Cache y real-time features
- **SQLAlchemy**: ORM híbrido
- **asyncpg**: Driver PostgreSQL asíncrono
- **spaCy**: Procesamiento de lenguaje natural
- **VADER**: Análisis de sentimientos
- **OpenAI API**: Generación de resúmenes

### Frontend
- **React**: Framework de UI
- **TypeScript**: Tipado estático
- **D3.js/Chart.js**: Visualizaciones
- **Leaflet.js**: Mapas interactivos
- **Material-UI**: Componentes de UI

### Infrastructure
- **Docker**: Containerización
- **Docker Compose**: Orquestación local
- **GitHub Actions**: CI/CD (futuro)
- **Nginx**: Reverse proxy (producción)

## Características Clave del Sistema

### Escalabilidad
- **Horizontal scaling**: Microservicios independientes
- **Database sharding**: Por región/idioma (futuro)
- **Cache distribuido**: Redis cluster
- **Load balancing**: Multiple API instances

### Performance
- **Sub-3s dashboard loading**: Cache inteligente + pre-agregación
- **Concurrent processing**: Async I/O en todo el stack
- **Smart indexing**: Queries optimizadas para analytics
- **CDN ready**: Static assets y reports

### Monitoring & Observability
- **Health checks**: Todos los servicios
- **Metrics collection**: Performance y usage
- **Error tracking**: Centralized logging
- **Alerting**: Critical failures y anomalies

### Security
- **JWT authentication**: API access control
- **Rate limiting**: Protection contra abuse
- **Input validation**: SQL injection prevention
- **HTTPS enforcement**: Todas las comunicaciones

## Roadmap de Desarrollo

### MVP (Fase 1) - Semanas 1-4
- ✅ PostgreSQL setup y migraciones
- ✅ Scrapers básicos funcionando
- 🔄 FastAPI con endpoints básicos
- 🔄 Sentiment analysis pipeline
- 🔄 Dashboard React básico

### Enhanced Analytics (Fase 2) - Semanas 5-8
- 📋 Topic classification avanzada
- 📋 Geographic analysis
- 📋 Weekly analytics automation
- 📋 Interactive visualizations
- 📋 Export functionality

### Advanced Features (Fase 3) - Semanas 9-12
- 📋 Real-time WebSocket updates
- 📋 Advanced filtering
- 📋 Multi-language support expansion
- 📋 Mobile responsive design
- 📋 API rate limiting

### Scale & Optimize (Fase 4) - Semanas 13-16
- 📋 Performance optimization
- 📋 Caching estrategy refinement
- 📋 Additional data sources
- 📋 Advanced analytics (ML trends)
- 📋 Production deployment

## Estado Actual
- **Database**: ✅ PostgreSQL funcionando con schema completo
- **Models**: ✅ SQLAlchemy models implementados
- **Connection**: ✅ Hybrid ORM + raw SQL funcionando
- **Testing**: ✅ Database tests passing
- **Docker**: ✅ PostgreSQL containerizado
- **Next**: 🔄 FastAPI implementation

---
**Última actualización**: 2025-06-27  
**Próxima revisión**: 2025-07-27