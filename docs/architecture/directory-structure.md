# Directory Structure - PreventIA News Analytics

Esta documentación registra la estructura completa de directorios y archivos del proyecto NewsBot transformado a sistema de analytics.

## 📁 Estructura Principal

```
news_bot_3/
├── 📄 CLAUDE.md                    # Guía para Claude Code
├── 📄 README.md                    # Documentación principal del proyecto
├── 📄 DEPLOYMENT.md               # Guía de deployment
├── 📄 requirements.txt            # Dependencias Python
├── 📄 main.py                     # Entry point de la aplicación
├── 📄 test_database.py           # Tests de base de datos
├── 📄 .env.template              # Template de configuración
├── 📄 docker-compose.yml         # Orquestación de containers
├── 📄 Dockerfile                 # Imagen del servicio
├── 📄 entrypoint.sh              # Script de entrada container
├── 📄 run_bot.sh                 # Script de ejecución
├── 📄 crontab.template           # Template para cron jobs
│
├── 📁 docs/                      # Documentación completa
├── 📁 services/                  # Servicios del sistema
├── 📁 venv/                      # Virtual environment Python
└── 📁 logs/                      # Logs de aplicación (generado)
```

## 📚 Documentación (`docs/`)

### Estructura Completa
```
docs/
├── 📄 README.md                          # Hub central de documentación
├── 📁 architecture/                      # Arquitectura del sistema
│   ├── 📄 system-overview.md            # Visión general con diagramas
│   └── 📄 directory-structure.md        # Este documento
├── 📁 decisions/                         # Architecture Decision Records
│   ├── 📄 README.md                     # Índice de ADRs
│   ├── 📄 adr-template.md               # Template para nuevos ADRs
│   ├── 📄 ADR-001-project-scope-change.md    # Cambio de alcance
│   └── 📄 ADR-002-database-architecture.md   # Arquitectura BD
├── 📁 development/                       # Guías de desarrollo
│   ├── 📁 setup/
│   │   └── 📄 local-development.md      # Setup completo local
│   ├── 📁 standards/                    # Estándares de código (pendiente)
│   └── 📁 guides/                       # Guías específicas (pendiente)
├── 📁 conversations/                     # Conversaciones técnicas
│   ├── 📄 README.md                     # Índice de conversaciones
│   ├── 📁 templates/
│   │   └── 📄 conversation-template.md  # Template para nuevas conversaciones
│   ├── 📄 2025-06-27_project-kickoff.md      # Sesión inicial
│   └── 📄 2025-06-27_database-implementation.md  # Implementación BD
├── 📁 operations/                        # Operaciones y deployment
│   ├── 📁 deployment/                   # (Estructura lista, pendiente contenido)
│   ├── 📁 monitoring/
│   └── 📁 maintenance/
├── 📁 api/                              # Documentación de APIs
│   ├── 📁 services/                     # APIs internas
│   └── 📁 external/                     # APIs externas
├── 📁 product/                          # Documentación de producto
│   ├── 📁 requirements/                 # Requirements funcionales
│   ├── 📁 roadmap/                      # Roadmap y planificación
│   └── 📁 research/                     # Investigación de mercado
└── 📁 assets/                           # Assets de documentación
    ├── 📁 diagrams/                     # Diagramas arquitectónicos
    ├── 📁 screenshots/                  # Screenshots de UI
    └── 📁 templates/                    # Templates diversos
```

## 🔧 Servicios (`services/`)

### Servicios Implementados
```
services/
├── 📁 data/                             # 🆕 Nueva capa de datos
│   └── 📁 database/
│       ├── 📄 connection.py            # Manager de conexiones híbrido
│       ├── 📄 models.py               # Modelos SQLAlchemy + Pydantic
│       └── 📁 migrations/
│           └── 📄 001_initial_schema.sql    # Schema inicial PostgreSQL
│
├── 📁 scraper/                          # ♻️ Reutilizado/adaptado
│   ├── 📁 src/
│   │   ├── 📄 main.py
│   │   ├── 📄 utils.py
│   │   └── 📁 extractors/              # 9 extractors existentes
│   │       ├── 📄 www_breastcancer_org.py
│   │       ├── 📄 www_curetoday_com_tumor_breast.py
│   │       ├── 📄 www_medicalxpress_breast_cancer.py
│   │       └── 📄 ... (6 más)
│   └── 📁 fulltext/                    # Extracción texto completo
│       └── 📁 src/
│           ├── 📄 fulltext_scraper.py
│           ├── 📄 registry.py
│           └── 📁 extractors/          # 8 extractors full-text
│               ├── 📄 breastcancernow_org.py
│               ├── 📄 www_nature_com.py
│               └── 📄 ... (6 más)
│
├── 📁 nlp/                             # ♻️ Reutilizado - base para analytics
│   └── 📁 src/
│       ├── 📄 main.py
│       ├── 📄 analyzer.py
│       ├── 📄 keywords.py
│       └── 📄 models.py
│
├── 📁 orchestrator/                     # ♻️ Evolucionando para analytics
│   └── 📁 src/
│       ├── 📄 main.py                  # Pipeline principal
│       └── 📄 utils.py
│
├── 📁 shared/                          # ♻️ Modelos compartidos
│   ├── 📁 models/
│   │   └── 📄 article.py              # Modelo base Article
│   └── 📁 utils/
│       └── 📄 dates.py
│
└── 📁 legacy/                          # 🔄 Servicios en transición
    ├── 📁 copywriter/                  # Para newsletter (deprecado)
    │   ├── 📁 src/
    │   ├── 📁 article_selector/
    │   ├── 📁 structure_builder/
    │   └── 📁 summary_generator/
    ├── 📁 decision_engine/             # Evolucionará a analytics
    │   └── 📁 src/
    └── 📁 publisher/                   # Ya no publica a WordPress
        └── 📁 src/
```

## 🎯 Nueva Arquitectura de Servicios (Roadmap)

### Servicios Futuros (a implementar)
```
services/
├── 📁 api/                             # 🔮 FastAPI REST endpoints
│   ├── 📄 main.py                     # FastAPI app principal
│   ├── 📁 endpoints/
│   │   ├── 📄 articles.py             # CRUD artículos
│   │   ├── 📄 sources.py              # Gestión fuentes
│   │   ├── 📄 analytics.py            # Métricas analytics
│   │   └── 📄 exports.py              # Exportación datos
│   ├── 📁 middleware/                 # Auth, CORS, rate limiting
│   └── 📁 schemas/                    # Pydantic schemas API
│
├── 📁 analytics/                       # 🔮 Procesamiento analytics
│   ├── 📁 sentiment/                  # Análisis sentimientos
│   ├── 📁 topic_classifier/           # Clasificación temática
│   ├── 📁 geographic/                 # Análisis geográfico
│   └── 📁 aggregation/                # Métricas agregadas
│
├── 📁 collection/                      # 🔮 Recolección optimizada
│   ├── 📁 source_validator/           # Validación fuentes dinámicas
│   └── 📁 scheduler/                  # Scheduling inteligente
│
└── 📁 export/                          # 🔮 Exportación y reportes
    ├── 📁 reports/                    # Generación reportes
    └── 📁 formats/                    # CSV, PDF, Excel export
```

## 📊 Archivos de Configuración

### Configuración Principal
```
├── 📄 .env.template                   # Template configuración (versionado)
├── 📄 .env                           # Configuración local (ignorado)
├── 📄 docker-compose.yml             # Servicios: PostgreSQL, Redis, Analytics
├── 📄 requirements.txt               # 45+ dependencias verificadas
├── 📄 Dockerfile                     # Imagen Python con dependencias
└── 📄 .gitignore                     # Archivos ignorados
```

### Configuración de Desarrollo
```
├── 📄 .dockerignore                  # Archivos ignorados en build
├── 📄 .gitattributes                 # Git line endings
└── 📁 venv/                          # Virtual environment (ignorado)
    ├── 📁 bin/                       # Executables Python
    ├── 📁 lib/                       # Site packages instalados
    └── 📁 include/                   # Headers C
```

## 🔍 Archivos por Tipo

### Python (`.py`)
- **Total**: ~25 archivos principales
- **Nuevos**: `connection.py`, `models.py`, `test_database.py`
- **Existentes**: Todo el directorio `services/` original

### Documentación (`.md`)
- **Total**: 10 archivos de documentación
- **Estructura**: 8 directorios organizados
- **Templates**: 2 templates reutilizables

### Configuración
- **Docker**: `docker-compose.yml`, `Dockerfile`, `.dockerignore`
- **Python**: `requirements.txt`, `.env.template`
- **Shell**: `run_bot.sh`, `entrypoint.sh`
- **SQL**: `001_initial_schema.sql`

## 📈 Estadísticas del Proyecto

### Líneas de Código
- **Database Layer**: ~650 líneas (models, connection, migration)
- **Documentation**: ~2,000 líneas
- **Configuration**: ~100 líneas
- **Tests**: ~120 líneas

### Estructura de Archivos
- **📁 Directorios**: 35+ directorios organizados
- **📄 Archivos**: 50+ archivos activos
- **🔧 Configuración**: 8 archivos de config
- **📚 Documentación**: 10 archivos .md

## 🎯 Estado de Implementación

### ✅ Completado
- ✅ **Database Layer**: PostgreSQL + SQLAlchemy híbrido
- ✅ **Documentation**: Estructura completa y ADRs
- ✅ **Infrastructure**: Docker + PostgreSQL + Redis
- ✅ **Testing**: Database tests funcionando

### 🔄 En Progreso
- 🔄 **API Layer**: FastAPI endpoints (próximo)
- 🔄 **Analytics**: Sentiment analysis (próximo)
- 🔄 **Migration**: Adaptar scrapers existentes

### 📋 Pendiente
- 📋 **Frontend**: React dashboard
- 📋 **Advanced Analytics**: Topic classification, geographic analysis
- 📋 **Operations**: Monitoring, deployment automation

---

**Última actualización**: 2025-06-27
**Versión de la estructura**: v2.0 (Analytics Architecture)
**Próxima actualización**: Cuando se implemente FastAPI layer
