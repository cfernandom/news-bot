# NewsBot Documentation Hub

Documentación central del proyecto NewsBot - Sistema autónomo de curación y publicación de noticias médicas.

## 📖 Índice de Documentación

### 🏗️ Arquitectura
- [System Overview](architecture/system-overview.md) - Visión general del sistema
- [Component Diagram](architecture/component-diagram.md) - Diagramas de componentes
- [Data Flow](architecture/data-flow.md) - Flujo de datos entre servicios
- [Tech Stack](architecture/tech-stack.md) - Stack tecnológico y justificaciones

### 🎯 Decisiones Técnicas
- [Architecture Decision Records](decisions/README.md) - Índice de ADRs
- [ADR Template](decisions/adr-template.md) - Plantilla para nuevas decisiones

### 🛠️ Desarrollo
- **Setup**
  - [Local Development](development/setup/local-development.md) - Configuración local
  - [Docker Setup](development/setup/docker-setup.md) - Configuración Docker
  - [Environment Variables](development/setup/environment-variables.md) - Variables de entorno
- **Estándares**
  - [Coding Standards](development/standards/coding-standards.md) - Estándares de código
  - [Testing Strategy](development/standards/testing-strategy.md) - Estrategia de testing
  - [Git Workflow](development/standards/git-workflow.md) - Flujo de trabajo Git
- **Guías**
  - [Adding Extractors](development/guides/adding-extractors.md) - Agregar nuevos extractors
  - [Debugging Pipeline](development/guides/debugging-pipeline.md) - Debugging del pipeline

### ⚙️ Operaciones
- **Deployment**
  - [Production Deployment](operations/deployment/production-deployment.md)
  - [Staging Deployment](operations/deployment/staging-deployment.md)
- **Monitoring**
  - [Logging Strategy](operations/monitoring/logging-strategy.md)
  - [Metrics Dashboard](operations/monitoring/metrics-dashboard.md)

### 💬 Conversaciones Técnicas
- [Índice de Conversaciones](conversations/README.md) - Registro de sesiones técnicas
- [Template](conversations/templates/conversation-template.md) - Plantilla para nuevas conversaciones

### 📊 API Documentation
- **Services**
  - [Scraper API](api/services/scraper-api.md)
  - [NLP API](api/services/nlp-api.md)
  - [Decision Engine API](api/services/decision-engine-api.md)
  - [Publisher API](api/services/publisher-api.md)
- **External**
  - [OpenAI Integration](api/external/openai-integration.md)
  - [WordPress API](api/external/wordpress-api.md)

### 🎯 Producto
- **Requirements**
  - [Functional Requirements](product/requirements/functional-requirements.md)
  - [Non-Functional Requirements](product/requirements/non-functional-requirements.md)
- **Roadmap**
  - [Current Roadmap](product/roadmap/current-roadmap.md)
  - [Completed Features](product/roadmap/completed-features.md)

## 🚀 Quick Start

1. **Para desarrolladores nuevos**: Empieza con [Local Development Setup](development/setup/local-development.md)
2. **Para entender la arquitectura**: Lee [System Overview](architecture/system-overview.md)
3. **Para decisiones técnicas**: Consulta [Architecture Decision Records](decisions/README.md)
4. **Para deployment**: Sigue [Production Deployment](operations/deployment/production-deployment.md)

## 📝 Contribuir a la Documentación

1. Usa los templates correspondientes
2. Mantén consistencia con el estilo existente
3. Actualiza este índice cuando agregues nuevos documentos
4. Documenta decisiones técnicas importantes en ADRs

## 🏷️ Convenciones

- **📁 Archivos de configuración**: Siempre con ejemplos y explicaciones
- **🔧 Guías técnicas**: Paso a paso con comandos ejecutables
- **📊 Diagramas**: Formato Mermaid cuando sea posible
- **⚠️ Alertas**: Usa callouts para información crítica

---

**Última actualización**: 2025-06-27  
**Mantenedores**: Claude (Dirección Técnica), cfernandom (Ingeniero Senior)