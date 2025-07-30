# 2. Diseño Técnico del Sistema de Información

## Índice del Contenido

1. [Esquema o Modelo de Requerimientos](#esquema-o-modelo-de-requerimientos)
2. [Software Base del Sistema y Prerequisitos](#software-base-del-sistema-y-prerequisitos)
3. [Componentes y Estándares](#componentes-y-estándares)
4. [Modelo de Datos](#modelo-de-datos)
5. [Funcionalidad y Servicios Ofrecidos](#funcionalidad-y-servicios-ofrecidos)

## Esquema o Modelo de Requerimientos

### Requerimientos Funcionales Principales

El sistema implementa los siguientes requerimientos funcionales críticos:

#### RF-001: Gestión de Fuentes de Noticias
```mermaid
graph LR
    A[Usuario Admin] --> B[CRUD Fuentes]
    B --> C[Validación Compliance]
    C --> D[Cálculo Score]
    D --> E[Auditoría]
    E --> F[Re-evaluación Mensual]
```

**Criterios de Aceptación:**
- Compliance score calculado automáticamente (0.00 - 1.00)
- Crawl delay mínimo de 2 segundos
- Registro completo de auditoría
- Rechazo automático de fuentes no conformes

#### RF-002: Web Scraping Automatizado
```mermaid
graph TD
    A[Fuente Configurada] --> B{Detectar CMS}
    B -->|WordPress| C[Template WordPress]
    B -->|Drupal| D[Template Drupal]
    B -->|Otro| E[Template Genérico]
    C --> F[Generar Scraper]
    D --> F
    E --> F
    F --> G[Ejecutar Scraping]
    G --> H[Detectar Duplicados]
    H --> I[Almacenar Artículo]
```

#### RF-003: Análisis NLP
```mermaid
graph LR
    A[Artículo] --> B[Preprocesamiento]
    B --> C[VADER Analysis]
    C --> D[Sentiment Score]
    D --> E[Clasificación Temática]
    E --> F[Extracción Keywords]
    F --> G[Resultado NLP]
```

### Requerimientos No Funcionales

| Categoría | Requerimiento | Métrica |
|-----------|---------------|---------|
| **Rendimiento** | Procesamiento de artículos | 50+ artículos/minuto |
| **Rendimiento** | Tiempo de carga dashboard | < 3 segundos |
| **Rendimiento** | Respuesta API | < 2 segundos |
| **Rendimiento** | Pipeline completo | < 4 horas |
| **Disponibilidad** | Uptime en horario laboral | ≥ 95% |
| **Seguridad** | Autenticación | JWT con expiración 24h |
| **Seguridad** | Contraseñas | Hash bcrypt |
| **Escalabilidad** | Usuarios concurrentes | 20+ usuarios |
| **Mantenibilidad** | Cobertura de tests | ≥ 85% |

### Casos de Uso del Sistema

```mermaid
graph TD
    subgraph "Actores"
        A1[Administrador]
        A2[Analista]
        A3[Usuario Demo]
        A4[Sistema]
    end

    subgraph "Casos de Uso"
        UC1[Gestionar Fuentes]
        UC2[Ejecutar Scrapers]
        UC3[Ver Dashboard]
        UC4[Exportar Datos]
        UC5[Gestionar Usuarios]
        UC6[Analizar Sentimiento]
        UC7[Monitorear Compliance]
    end

    A1 --> UC1
    A1 --> UC2
    A1 --> UC5
    A1 --> UC7
    A2 --> UC3
    A2 --> UC4
    A3 --> UC3
    A4 --> UC6
    A4 --> UC7
```

## Software Base del Sistema y Prerequisitos

### Requerimientos Mínimos de Hardware

| Componente | Desarrollo | Producción |
|------------|------------|------------|
| **CPU** | 2 cores | 4+ cores |
| **RAM** | 4 GB | 8+ GB |
| **Almacenamiento** | 20 GB SSD | 50+ GB SSD |
| **Red** | 10 Mbps | 100+ Mbps |

### Requerimientos de Software

#### Sistema Operativo
- **Desarrollo**: Windows 10+, macOS 10.15+, Ubuntu 20.04+
- **Producción**: Ubuntu 20.04 LTS o superior
- **Contenedores**: Docker 20.10+ y Docker Compose 2.0+

#### Runtime y Lenguajes
```yaml
Backend:
  - Python: 3.13.5 (específico)
  - pip: 24.3+

Frontend:
  - Node.js: 24.4.1
  - npm: 11.4.2

Base de Datos:
  - PostgreSQL: 16-alpine
  - Redis: 8-alpine
```

#### Navegadores Compatibles
- Chrome 90+
- Firefox 88+
- Safari 14+
- Edge 90+

## Componentes y Estándares

### Frameworks y Librerías Backend

```python
# Framework Principal
FastAPI==0.115.14          # Framework web asíncrono
uvicorn[standard]==0.34.0  # Servidor ASGI

# ORM y Base de Datos
SQLAlchemy==2.0.41        # ORM principal
asyncpg==0.30.0           # Driver PostgreSQL asíncrono
alembic==1.14.0           # Migraciones de BD

# NLP y Análisis
spacy==3.8.7              # Framework NLP
vaderSentiment==3.3.2     # Análisis de sentimiento

# Web Scraping
beautifulsoup4==4.13.4    # Parser HTML
playwright==1.51.0        # Automatización web

# Utilidades
pydantic==2.11.3          # Validación de datos
python-jose==3.5.0        # JWT tokens
passlib[bcrypt]==1.7.4    # Hashing de contraseñas
redis==5.2.1              # Cliente Redis
```

### Frameworks y Librerías Frontend

```json
{
  "frameworks": {
    "react": "19.1.0",
    "vite": "7.0.0",
    "typescript": "5.8.3"
  },
  "ui_components": {
    "@tailwindcss/forms": "0.5.10",
    "tailwindcss": "4.1.11",
    "lucide-react": "0.525.0",
    "@heroicons/react": "2.2.0"
  },
  "state_management": {
    "@tanstack/react-query": "5.81.5",
    "react-hook-form": "7.59.0"
  },
  "visualization": {
    "recharts": "3.0.2",
    "leaflet": "1.9.4",
    "react-leaflet": "5.0.0"
  }
}
```

### Estándares de Codificación

#### Python (Backend)
- **PEP 8**: Guía de estilo oficial de Python
- **Black**: Formateador automático (línea máx: 88 caracteres)
- **isort**: Ordenamiento de imports
- **flake8**: Linting y verificación de estilo

#### JavaScript/TypeScript (Frontend)
- **ESLint**: Linting con configuración estricta
- **Prettier**: Formateador de código
- **TypeScript**: Tipado estático estricto

### Patrones de Diseño Implementados

1. **Repository Pattern**: Capa de acceso a datos
2. **Dependency Injection**: Inyección de dependencias con FastAPI
3. **Factory Pattern**: Generación de scrapers
4. **Observer Pattern**: Sistema de eventos y notificaciones
5. **Singleton**: Conexiones a base de datos y cache

### Protocolos y Estándares

#### Seguridad
- **HTTPS**: TLS 1.2+ en producción
- **CORS**: Configuración restrictiva
- **Rate Limiting**: Límites por endpoint
- **Input Validation**: Pydantic models

#### APIs
- **REST**: Arquitectura RESTful
- **OpenAPI 3.0**: Documentación automática
- **JSON**: Formato de intercambio
- **UTF-8**: Codificación de caracteres

## Modelo de Datos

### Diagrama Entidad-Relación

```mermaid
erDiagram
    NEWS_SOURCES ||--o{ ARTICLES : "publica"
    ARTICLES ||--o{ ARTICLE_KEYWORDS : "contiene"
    USERS ||--o{ USER_ROLE_ASSIGNMENTS : "tiene"
    USER_ROLES ||--o{ USER_ROLE_ASSIGNMENTS : "asignado_a"
    NEWS_SOURCES ||--o{ COMPLIANCE_AUDIT_LOG : "genera"
    NEWS_SOURCES ||--o{ COMPLIANCE_VALIDATIONS : "valida"
    NEWS_SOURCES ||--o{ LEGAL_NOTICES : "genera"
    NEWS_SOURCES ||--o{ SCRAPER_AUTOMATION_LOG : "automatiza"
    ARTICLES ||--o{ WEEKLY_ANALYTICS : "analiza"

    NEWS_SOURCES {
        int id PK
        varchar name UK
        varchar base_url UK
        varchar language
        varchar country
        varchar extractor_class
        boolean is_active
        varchar validation_status
        text validation_error
        timestamp last_validation_at
        varchar robots_txt_url
        timestamp robots_txt_last_checked
        int crawl_delay_seconds
        boolean scraping_allowed
        varchar terms_of_service_url
        timestamp terms_reviewed_at
        varchar legal_contact_email
        text fair_use_basis
        decimal compliance_score
        timestamp last_compliance_check
        timestamp created_at
        timestamp updated_at
    }

    ARTICLES {
        int id PK
        int source_id FK
        text title
        varchar url UK
        text content
        timestamp published_at
        varchar processing_status
        decimal sentiment_score
        varchar sentiment_label
        varchar topic_category
        decimal topic_confidence
        varchar content_hash UK
        int word_count
        text summary
        json metadata
        timestamp created_at
        timestamp updated_at
    }

    USERS {
        int id PK
        varchar username UK
        varchar email UK
        varchar hashed_password
        boolean is_active
        timestamp created_at
        timestamp updated_at
    }

    USER_ROLES {
        int id PK
        varchar name UK
        text description
        timestamp created_at
    }

    USER_ROLE_ASSIGNMENTS {
        int id PK
        int user_id FK
        int role_id FK
        timestamp assigned_at
    }

    ARTICLE_KEYWORDS {
        int id PK
        int article_id FK
        varchar keyword
        varchar keyword_type
        decimal confidence_score
        timestamp extracted_at
    }

    COMPLIANCE_AUDIT_LOG {
        int id PK
        int source_id FK
        varchar check_type
        varchar status
        text details
        timestamp checked_at
    }

    COMPLIANCE_VALIDATIONS {
        int id PK
        int source_id FK
        varchar validation_type
        boolean passed
        text error_message
        json validation_details
        timestamp validated_at
    }

    LEGAL_NOTICES {
        int id PK
        int source_id FK
        varchar notice_type
        text content
        boolean acknowledged
        timestamp created_at
        timestamp acknowledged_at
    }

    SCRAPER_AUTOMATION_LOG {
        int id PK
        int source_id FK
        varchar action_type
        varchar status
        text details
        json generated_code
        timestamp executed_at
    }

    WEEKLY_ANALYTICS {
        int id PK
        int article_id FK
        date week_start
        int views_count
        decimal sentiment_avg
        varchar top_keywords
        timestamp calculated_at
    }
```

### Diccionario de Datos

#### Tabla: news_sources
| Campo | Tipo | Descripción | Restricciones |
|-------|------|-------------|---------------|
| id | INTEGER | Identificador único | PK, AUTO_INCREMENT |
| name | VARCHAR(255) | Nombre de la fuente | NOT NULL, UNIQUE |
| base_url | VARCHAR(500) | URL base del sitio | NOT NULL, UNIQUE |
| language | VARCHAR(10) | Código ISO del idioma | NOT NULL |
| country | VARCHAR(100) | País de origen | NOT NULL |
| compliance_score | DECIMAL(3,2) | Score de cumplimiento | 0.00 - 1.00 |
| is_active | BOOLEAN | Estado activo/inactivo | DEFAULT TRUE |
| crawl_delay_seconds | INTEGER | Delay entre requests | MIN 2 |
| created_at | TIMESTAMP | Fecha de creación | NOT NULL |
| updated_at | TIMESTAMP | Última actualización | NOT NULL |

#### Tabla: articles
| Campo | Tipo | Descripción | Restricciones |
|-------|------|-------------|---------------|
| id | INTEGER | Identificador único | PK, AUTO_INCREMENT |
| source_id | INTEGER | ID de la fuente | FK → news_sources(id) |
| title | TEXT | Título del artículo | NOT NULL |
| url | VARCHAR(1000) | URL del artículo | NOT NULL, UNIQUE |
| content | TEXT | Contenido completo | NULL |
| published_at | TIMESTAMP | Fecha de publicación | NOT NULL |
| sentiment_score | DECIMAL(4,3) | Score de sentimiento | -1.000 a 1.000 |
| sentiment_label | VARCHAR(20) | Etiqueta sentimiento | ENUM: positive/negative/neutral |
| topic_category | VARCHAR(50) | Categoría temática | NOT NULL |
| content_hash | VARCHAR(64) | Hash SHA-256 | UNIQUE |
| word_count | INTEGER | Conteo de palabras | >= 0 |

### Índices de Base de Datos

```sql
-- Índices de rendimiento
CREATE INDEX idx_articles_source_id ON articles(source_id);
CREATE INDEX idx_articles_published_at ON articles(published_at DESC);
CREATE INDEX idx_articles_sentiment ON articles(sentiment_label, sentiment_score);
CREATE INDEX idx_articles_topic ON articles(topic_category);

-- Índices únicos
CREATE UNIQUE INDEX idx_sources_base_url ON news_sources(base_url);
CREATE UNIQUE INDEX idx_articles_url ON articles(url);
CREATE UNIQUE INDEX idx_articles_hash ON articles(content_hash);
```

## Funcionalidad y Servicios Ofrecidos

### Arquitectura de Servicios

```mermaid
graph TB
    subgraph "Frontend Layer"
        FE[React SPA]
    end

    subgraph "API Gateway"
        GW[FastAPI Gateway]
    end

    subgraph "Service Layer"
        S1[Scraper Service]
        S2[NLP Service]
        S3[Data Service]
        S4[Analytics Service]
        S5[Auth Service]
    end

    subgraph "Data Layer"
        DB[(PostgreSQL)]
        RD[(Redis Cache)]
    end

    subgraph "External Services"
        EX1[OpenAI API]
        EX2[News Sites]
    end

    FE --> GW
    GW --> S1
    GW --> S2
    GW --> S3
    GW --> S4
    GW --> S5

    S1 --> DB
    S2 --> DB
    S3 --> DB
    S4 --> DB
    S5 --> DB

    S1 --> RD
    S4 --> RD

    S1 --> EX2
    S2 --> EX1
```

### Endpoints API Principales

#### Autenticación
```http
POST   /api/auth/login      # Login de usuario
POST   /api/auth/refresh    # Renovar token
GET    /api/auth/me         # Usuario actual
```

#### Gestión de Fuentes
```http
GET    /api/sources         # Listar fuentes
POST   /api/sources         # Crear fuente
PUT    /api/sources/{id}    # Actualizar fuente
DELETE /api/sources/{id}    # Eliminar fuente
POST   /api/sources/{id}/validate  # Validar compliance
```

#### Artículos y Analytics
```http
GET    /api/articles        # Listar artículos con filtros
GET    /api/articles/{id}   # Detalle de artículo
GET    /api/analytics/summary      # Resumen estadístico
GET    /api/analytics/sentiment    # Distribución sentimiento
GET    /api/analytics/trends       # Tendencias temporales
```

#### Exportación
```http
POST   /api/export/csv      # Exportar a CSV
POST   /api/export/excel    # Exportar a Excel
POST   /api/export/pdf      # Exportar a PDF
POST   /api/export/chart    # Exportar gráfico PNG
```

### Flujos de Proceso Principales

#### Flujo de Scraping
```mermaid
sequenceDiagram
    participant Scheduler
    participant Scraper
    participant Validator
    participant NLP
    participant Database

    Scheduler->>Scraper: Iniciar scraping
    Scraper->>Validator: Verificar compliance
    Validator-->>Scraper: OK/Error
    Scraper->>Scraper: Extraer artículo
    Scraper->>NLP: Analizar contenido
    NLP->>NLP: Sentiment analysis
    NLP->>NLP: Topic classification
    NLP-->>Scraper: Resultados
    Scraper->>Database: Guardar artículo
    Database-->>Scheduler: Confirmación
```

### Servicios de Monitoreo

- **Health Check**: `/health` - Estado del sistema
- **Metrics**: Métricas de rendimiento internas
- **Logging**: Logs estructurados con niveles
- **Alertas**: Notificaciones de eventos críticos

---

*Siguiente: [03. Instalación y Configuración](03_InstalacionConfiguracion.md)*
