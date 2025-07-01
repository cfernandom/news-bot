# Architecture Decision Records (ADRs)

Este directorio contiene todas las decisiones arquitectónicas importantes del proyecto PreventIA News Analytics, documentadas siguiendo el formato ADR estándar.

## 📋 Índice de Decisiones

| ADR | Título | Estado | Fecha | Impacto |
|-----|--------|--------|-------|---------|
| [ADR-001](./ADR-001-project-scope-change.md) | Cambio de Alcance - De Newsletter Bot a Sistema de Analytics | Aceptado | 2025-06-27 | 🔴 Crítico |
| [ADR-002](./ADR-002-database-architecture.md) | Arquitectura de Base de Datos - PostgreSQL con Enfoque Híbrido | Aceptado | 2025-06-27 | 🔴 Crítico |
| [ADR-003](./ADR-003-migration-strategy.md) | Estrategia de Migración - Scrapers a PostgreSQL | Aceptado | 2025-06-27 | 🟡 Alto |
| [ADR-004](./ADR-004-nlp-sentiment-analysis.md) | NLP Sentiment Analysis - VADER para Contenido Médico | Aceptado | 2025-06-28 | 🟡 Alto |
| [ADR-005](./ADR-005-testing-framework-architecture.md) | Testing Framework - pytest con Estructura Profesional | Aceptado | 2025-06-28 | 🟡 Alto |
| [ADR-006](./ADR-006-legal-compliance-framework.md) | Legal Compliance Framework - GDPR + Robots.txt + Fair Use | Aceptado | 2025-06-30 | 🟡 Alto |
| [ADR-007](./ADR-007-prompts-strategy-optimization.md) | Prompts Strategy Optimization - Self-Contained Architecture | Aceptado | 2025-06-30 | 🟢 Medio |
| [ADR-008](./ADR-008-medical-ux-ui-design-strategy.md) | Medical UX/UI Design Strategy - FASE 4 React Dashboard | Aceptado | 2025-07-01 | 🔴 Crítico |

## 📝 Cómo Usar los ADRs

### Para Desarrolladores
1. **Antes de hacer cambios arquitectónicos**: Revisa ADRs existentes para entender el contexto
2. **Al proponer cambios**: Crea un nuevo ADR usando el [template](./adr-template.md)
3. **Durante code reviews**: Referencia ADRs relevantes para justificar decisiones

### Para Nuevos Team Members
1. **Onboarding**: Lee ADRs en orden cronológico para entender evolución
2. **Context**: Cada ADR explica el "por qué" detrás de decisiones técnicas
3. **Referencias**: ADRs cross-reference para entender dependencies

## 🏷️ Estados de ADRs

- **🟢 Propuesto**: ADR en review, no implementado
- **✅ Aceptado**: ADR aprobado e implementado
- **❌ Rechazado**: ADR evaluado pero no adoptado
- **🔄 Reemplazado**: ADR obsoleto, reemplazado por uno más reciente
- **⚠️ Obsoleto**: ADR ya no aplicable al sistema actual

## 📊 Categorías de Impacto

- **🔴 Crítico**: Afecta arquitectura fundamental del sistema
- **🟡 Alto**: Afecta múltiples componentes o modules
- **🟢 Medio**: Afecta componente específico
- **⚪ Bajo**: Cambio localizado, mínimo impacto

## 🔍 ADRs por Categoría

### Arquitectura de Sistema
- [ADR-001](./ADR-001-project-scope-change.md) - Cambio fundamental de alcance del proyecto
- [ADR-002](./ADR-002-database-architecture.md) - Decisiones de base de datos

### Backend Technology Stack
- [ADR-002](./ADR-002-database-architecture.md) - PostgreSQL híbrido (ORM + Raw SQL)

### Frontend Technology Stack
- [ADR-008](./ADR-008-medical-ux-ui-design-strategy.md) - Medical UX/UI Design Strategy para React Dashboard

### Infrastructure
- 📋 Pendiente: Docker deployment strategy
- 📋 Pendiente: CI/CD pipeline decisions

### Analytics & AI
- [ADR-004](./ADR-004-nlp-sentiment-analysis.md) - VADER sentiment analysis para contenido médico
- 📋 Pendiente: LLM integration strategy avanzada

## 📅 Cronología de Decisiones

### 2025-06-27 - Project Foundation
- **ADR-001**: Redefinición completa del proyecto de newsletter bot a analytics system
- **ADR-002**: Establecimiento de arquitectura de base de datos PostgreSQL

### 2025-06-28 - Analytics & Testing Foundation
- **ADR-003**: Estrategia de migración de scrapers a PostgreSQL
- **ADR-004**: NLP sentiment analysis con VADER para contenido médico
- **ADR-005**: Testing framework profesional con pytest

### 2025-06-30 - Compliance & Optimization
- **ADR-006**: Legal compliance framework (GDPR + robots.txt + fair use)
- **ADR-007**: Prompts strategy optimization con arquitectura self-contained

### 2025-07-01 - Frontend & UX Strategy
- **ADR-008**: Medical UX/UI design strategy para FASE 4 React Dashboard

### Próximas Decisiones (Roadmap)
- **ADR-009**: Deployment y infrastructure strategy (Docker + CI/CD)
- **ADR-010**: LLM integration strategy avanzada
- **ADR-011**: Real-time analytics con WebSocket integration

## 🔗 Referencias Externas

### ADR Methodology
- [Architecture Decision Records](https://adr.github.io/) - Methodology overview
- [ADR Tools](https://github.com/npryce/adr-tools) - Command line tools
- [When to Write an ADR](https://cognitect.com/blog/2011/11/15/documenting-architecture-decisions) - Guidelines

### Related Documentation
- [System Overview](../architecture/system-overview.md) - Current architecture state
- [Technical Conversations](../conversations/README.md) - Decision discussions
- [Development Setup](../development/setup/local-development.md) - Implementation guides

## ✅ Best Practices

### Cuándo Crear un ADR
- **Cambios arquitectónicos**: Cualquier cambio que afecte múltiples componentes
- **Technology selection**: Elección entre múltiples opciones técnicas
- **Trade-offs importantes**: Decisiones con pros/cons significativos
- **Constraints del proyecto**: Limitaciones que afectan design choices

### Qué NO Requiere ADR
- **Bug fixes**: Correcciones que no cambian arquitectura
- **Feature implementations**: Que siguen patterns existentes
- **Configuration changes**: Cambios de configuración menores
- **Code refactoring**: Que no afecta interfaces públicas

### Quality Checklist
- [ ] Contexto y problema claramente explicados
- [ ] Opciones consideradas con pros/cons
- [ ] Decisión justificada con criterios específicos
- [ ] Consecuencias (positivas y negativas) identificadas
- [ ] Plan de implementación definido
- [ ] Criterios de rollback establecidos

---
**Última actualización**: 2025-07-01
**Próxima revisión**: 2025-07-27
**Template**: [adr-template.md](./adr-template.md)
