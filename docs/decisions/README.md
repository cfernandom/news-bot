# Architecture Decision Records (ADRs)

Este directorio contiene todas las decisiones arquitectónicas importantes del proyecto PreventIA News Analytics, documentadas siguiendo el formato ADR estándar.

## 📋 Índice de Decisiones

| ADR | Título | Estado | Fecha | Impacto |
|-----|--------|--------|-------|---------|
| [ADR-001](./ADR-001-project-scope-change.md) | Cambio de Alcance - De Newsletter Bot a Sistema de Analytics | Aceptado | 2025-06-27 | 🔴 Crítico |
| [ADR-002](./ADR-002-database-architecture.md) | Arquitectura de Base de Datos - PostgreSQL con Enfoque Híbrido | Aceptado | 2025-06-27 | 🔴 Crítico |

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
- 📋 Pendiente: React + TypeScript decisions

### Infrastructure
- 📋 Pendiente: Docker deployment strategy
- 📋 Pendiente: CI/CD pipeline decisions

### Analytics & AI
- 📋 Pendiente: Sentiment analysis approach
- 📋 Pendiente: LLM integration strategy

## 📅 Cronología de Decisiones

### 2025-06-27 - Project Foundation
- **ADR-001**: Redefinición completa del proyecto de newsletter bot a analytics system
- **ADR-002**: Establecimiento de arquitectura de base de datos PostgreSQL

### Próximas Decisiones (Roadmap)
- **ADR-003**: FastAPI architecture y API design patterns
- **ADR-004**: Sentiment analysis technology selection
- **ADR-005**: Frontend architecture (React + state management)
- **ADR-006**: Deployment y infrastructure strategy

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
**Última actualización**: 2025-06-27  
**Próxima revisión**: 2025-07-27  
**Template**: [adr-template.md](./adr-template.md)