# PreventIA News Analytics - Documentation Hub

Documentación central del proyecto PreventIA News Analytics - Sistema inteligente de monitoreo y análisis de medios especializados en noticias de cáncer de mama.

## 📖 Índice de Documentación

### 🏗️ Arquitectura
- [System Overview](architecture/system-overview.md) - ✅ Visión general del sistema analytics
- [Directory Structure](architecture/directory-structure.md) - ✅ Estructura completa del proyecto
- [Data Flow](architecture/data-flow.md) - (Pendiente) Flujo de datos entre servicios
- [Tech Stack](architecture/tech-stack.md) - (Pendiente) Stack tecnológico y justificaciones

### 🎯 Decisiones Técnicas
- [Architecture Decision Records](decisions/README.md) - ✅ Índice de ADRs (5 ADRs completados)
- [ADR Template](decisions/adr-template.md) - ✅ Plantilla para nuevas decisiones

### 🛠️ Desarrollo
- **Setup**
  - [Local Development](development/setup/local-development.md) - ✅ Configuración local
  - [Docker Setup](development/setup/docker-setup.md) - (Pendiente) Configuración Docker
  - [Environment Variables](development/setup/environment-variables.md) - (Pendiente) Variables de entorno
- **Estándares**
  - [Testing Strategy](development/standards/testing-strategy.md) - ✅ Estrategia completa de testing
  - [Testing Structure](development/standards/testing-structure.md) - ✅ Estructura de testing profesional
  - [Language Usage Standard](development/standards/language-usage-standard.md) - ✅ Estándar de uso de idiomas
  - [Git Workflow](development/standards/git-workflow.md) - ✅ Flujo de trabajo Git
- **Guías**
  - [Scrapers Usage Guide](development/scrapers-usage-guide.md) - ✅ Guía de uso de scrapers migrados
  - [Adding Extractors](development/guides/adding-extractors.md) - (Pendiente) Agregar nuevos extractors
  - [Debugging Pipeline](development/guides/debugging-pipeline.md) - (Pendiente) Debugging del pipeline

### ⚙️ Operaciones
- **Deployment**
  - [Production Deployment](operations/deployment/production-deployment.md) - (Pendiente) Deploy a producción
  - [Staging Deployment](operations/deployment/staging-deployment.md) - (Pendiente) Deploy a staging
- **Monitoring**
  - [Logging Strategy](operations/monitoring/logging-strategy.md) - (Pendiente) Estrategia de logging
  - [Metrics Dashboard](operations/monitoring/metrics-dashboard.md) - (Pendiente) Dashboard de métricas

### 💬 Conversaciones Técnicas
- [Índice de Conversaciones](conversations/README.md) - ✅ Registro de sesiones técnicas
- [Template](conversations/templates/conversation-template.md) - ✅ Plantilla para nuevas conversaciones

### 📊 API Documentation
- **Services**
  - [NLP API](api/services/nlp-api.md) - ✅ Sentiment Analysis & Text Processing API
  - [Scraper API](api/services/scraper-api.md) - (Pendiente) Web scraping endpoints
  - [Analytics API](api/services/analytics-api.md) - (Pendiente) Dashboard analytics endpoints
- **External**
  - [OpenAI Integration](api/external/openai-integration.md) - (Futuro) LLM integration patterns
  - [Database API](api/external/database-api.md) - (Pendiente) PostgreSQL integration patterns

### 📋 Implementación y Resultados
- **Resultados por Fase**
  - [Phase 1 Results](implementation/phase-1-results.md) - ✅ Migración de scrapers a PostgreSQL
  - [Phase 2 Results](implementation/phase-2-nlp-analytics.md) - ✅ NLP Analytics y Testing Framework
  - [Migration Roadmap](implementation/migration-roadmap.md) - ✅ Roadmap completo del proyecto
- **Producto**
  - [Current Roadmap](product/roadmap/current-roadmap.md) - (Pendiente) Roadmap para FASE 3
  - [Requirements](product/requirements/functional-requirements.md) - (Pendiente) Requisitos funcionales

## 🚀 Quick Start

1. **Para desarrolladores nuevos**: Empieza con [Local Development Setup](development/setup/local-development.md)
2. **Para entender la transformación**: Lee [System Overview](architecture/system-overview.md) y [ADR-001: Project Scope Change](decisions/ADR-001-project-scope-change.md)
3. **Para usar scrapers migrados**: Consulta [Scrapers Usage Guide](development/scrapers-usage-guide.md)
4. **Para NLP Analytics**: Revisa [NLP API Documentation](api/services/nlp-api.md) y [Phase 2 Results](implementation/phase-2-nlp-analytics.md)
5. **Para decisiones técnicas**: Consulta [Architecture Decision Records](decisions/README.md)

## 📝 Contribuir a la Documentación

1. **Sigue el estándar de idiomas**: [Language Usage Standard](development/standards/language-usage-standard.md)
2. **Documenta decisiones importantes**: Usa ADRs para cambios arquitectónicos
3. **Mantén consistencia**: Usa templates correspondientes
4. **Actualiza índices**: Incluye nuevos documentos en este README
5. **Testing**: Documenta estrategias de testing en [Testing Strategy](development/standards/testing-strategy.md)

## 🏷️ Convenciones y Estándares

- **🌐 Idiomas**: Inglés para código/APIs, español para decisiones de equipo
- **📁 Archivos técnicos**: Siempre con ejemplos ejecutables
- **🧪 Testing**: Framework profesional con unit/integration/e2e
- **📊 Métricas**: Validar con datos reales antes de reportar
- **⚠️ Alertas**: Usa callouts para información crítica

---

## 📊 Estado Actual del Proyecto

### ✅ Completado (FASE 1 & 2)
- **FASE 1**: Migración de 4 scrapers a PostgreSQL (106 artículos)
- **FASE 2**: NLP Analytics con sentiment analysis (56 artículos procesados)
- **Testing Framework**: Estructura profesional pytest con 24 tests
- **Documentación**: ADRs, API docs, estándares técnicos

### 🚀 Próximo (FASE 3)
- **FastAPI Endpoints**: REST API para analytics dashboard
- **React Dashboard**: Frontend con visualizaciones
- **Real-time Analytics**: WebSocket updates y métricas live

## 📋 Estado de la Documentación

### ✅ **Documentación Completada (15 archivos)**
- **Arquitectura**: 2/4 archivos (System Overview, Directory Structure)
- **Decisiones**: 7/7 archivos (5 ADRs + README + Template)
- **Estándares**: 4/4 archivos (Testing, Language, Git Workflow)
- **API**: 1/3 archivos (NLP API completa)
- **Implementación**: 3/3 archivos (Resultados FASE 1, 2 y Roadmap)
- **Conversaciones**: 5/5 archivos (3 sesiones + README + Template)

### 📋 **Documentación Pendiente (13 archivos)**
- **Arquitectura**: Data Flow, Tech Stack
- **Setup**: Docker Setup, Environment Variables  
- **Guías**: Adding Extractors, Debugging Pipeline
- **Operaciones**: 4 archivos (deployment + monitoring)
- **API**: 2 archivos (Scraper API, Analytics API)
- **Producto**: 2 archivos (roadmap + requirements)

### 🎯 **Prioridad para FASE 3**
1. **Alta**: Docker Setup, FastAPI Analytics API
2. **Media**: Data Flow, Tech Stack, Production Deployment
3. **Baja**: Monitoring, Debugging guides

---

**Última actualización**: 2025-06-28  
**Estado**: FASE 2 Completada ✅ | Documentación: 54% completada  
**Mantenedores**: Claude (Director Técnico), cfernandom (Ingeniero Senior)