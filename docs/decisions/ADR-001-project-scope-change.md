# ADR-001: Cambio de Alcance - De Newsletter Bot a Sistema de Analytics

## Metadata
- **Estado**: Aceptado
- **Fecha**: 2025-06-27
- **Deciders**: Claude (Dirección Técnica), cfernandom (Ingeniero Senior)
- **Consulted**: N/A (equipo inicial)
- **Informed**: Equipo de desarrollo futuro

## Contexto y Problema
El proyecto NewsBot fue inicialmente diseñado como un sistema de generación y publicación automática de newsletters médicos sobre cáncer de seno. Sin embargo, se identificaron problemas legales y éticos críticos que requieren un cambio fundamental de enfoque.

### Fuerzas Impulsoras
- **Derechos de autor**: La generación automática de boletines informativos entra en conflicto con las políticas de la mayoría de sitios web médicos
- **Riesgo legal**: Potential copyright infringement al republificar contenido médico
- **Oportunidad técnica**: El avance del proyecto permite pivotear a un sistema de análisis más valioso
- **Valor agregado**: Analytics de tendencias mediáticas es más útil que duplicar contenido existente

## Opciones Consideradas

### Opción 1: Continuar con newsletter bot modificado
**Descripción**: Mantener generación de newsletters pero con mayor énfasis en resúmenes originales

**Pros**:
- ✅ Aprovecha trabajo existente de LLM integration
- ✅ Funcionalidad completa ya implementada
- ✅ Menor impacto en roadmap

**Contras**:
- ❌ Sigue teniendo riesgos legales de copyright
- ❌ Limitado valor agregado vs contenido original
- ❌ Posibles problemas con sitios web source

**Costo estimado**: Bajo
**Tiempo de implementación**: Continuar desarrollo actual

### Opción 2: Sistema de analytics y dashboard
**Descripción**: Transformar en sistema de análisis de inteligencia mediática con dashboard React

**Pros**:
- ✅ Elimina problemas de derechos de autor
- ✅ Mayor valor agregado para stakeholders
- ✅ Análisis de tendencias único en el mercado
- ✅ Reutiliza componentes de scraping y NLP
- ✅ Escalable a múltiples regiones/idiomas

**Contras**:
- ❌ Requiere desarrollo de frontend React
- ❌ Cambio en arquitectura backend
- ❌ Redefinición de métricas de éxito

**Costo estimado**: Medio
**Tiempo de implementación**: 6-8 semanas

### Opción 3: Híbrido - Analytics + newsletters internas
**Descripción**: Sistema de analytics principal con newsletters solo para uso interno/research

**Pros**:
- ✅ Mantiene alguna funcionalidad de newsletters
- ✅ Reduce riesgos legales (uso interno)
- ✅ Flexibilidad de características

**Contras**:
- ❌ Complejidad adicional mantener dos sistemas
- ❌ Unclear valor de newsletters internas
- ❌ Recursos divididos entre dos objetivos

**Costo estimado**: Alto
**Tiempo de implementación**: 8-10 semanas

## Decisión
**Opción elegida**: Sistema de analytics y dashboard (Opción 2)

### Criterios de Decisión
1. **Riesgo legal** (peso: crítico): Eliminar completamente problemas de copyright
2. **Valor para usuarios** (peso: alto): Analytics únicos vs contenido duplicado
3. **Escalabilidad técnica** (peso: alto): Fundación sólida para crecimiento
4. **Reutilización de trabajo** (peso: medio): Aprovechar scraping y NLP existente

### Justificación
La transformación a sistema de analytics elimina completamente los riesgos legales mientras proporciona mayor valor. El sistema de análisis de tendencias mediáticas sobre cáncer de seno es único y escalable. Los componentes existentes (scraping, NLP, LLM) se reutilizan efectivamente en el nuevo contexto.

## Consecuencias

### Positivas
- ✅ **Eliminación de riesgos legales**: Sin problemas de copyright
- ✅ **Valor único**: Analytics de tendencias mediáticas especializadas
- ✅ **Escalabilidad**: Fácil agregar nuevas fuentes y regiones
- ✅ **Reutilización**: 70% del código base se mantiene útil
- ✅ **Mercado diferenciado**: Producto único en el nicho

### Negativas
- ⚠️ **Desarrollo adicional**: Requiere frontend React y API REST
- ⚠️ **Cambio de métricas**: Redefinir KPIs y objetivos de usuario
- ⚠️ **Curva de aprendizaje**: Team debe entender analytics en lugar de publishing

### Neutrales
- ℹ️ **Base de datos**: Cambio de estructura de datos necesario
- ℹ️ **Arquitectura**: Migración de monolito a API + frontend

## Plan de Implementación

### Fase 1: Infraestructura (Semanas 1-2)
**Objetivo**: Establecer nueva arquitectura
- Migrar a PostgreSQL para analytics complejos
- Implementar FastAPI REST endpoints
- Establecer modelos de datos para analytics
- Setup básico de Docker Compose

**Entregables**:
- PostgreSQL funcional con migraciones
- FastAPI con endpoints CRUD básicos
- Modelos de datos para analytics

### Fase 2: Analytics Backend (Semanas 3-4)
**Objetivo**: Implementar lógica de análisis
- Análisis de sentimientos (spaCy + VADER)
- Clasificación temática automática
- Métricas agregadas semanales
- APIs para dashboard

**Entregables**:
- Sentiment analysis pipeline
- Topic classification
- Weekly analytics pre-calculation
- REST API completa

### Fase 3: Dashboard Frontend (Semanas 5-6)
**Objetivo**: Interface de usuario
- Dashboard React con visualizaciones
- Integración con backend APIs
- Exportación de reportes
- Mapa interactivo de cobertura

**Entregables**:
- Dashboard React funcional
- Visualizaciones con charts
- Sistema de exportación

### Fase 4: Optimización (Semanas 7-8)
**Objetivo**: Performance y features avanzadas
- Cache inteligente con Redis
- Filtros avanzados
- Real-time updates
- Mobile responsiveness

**Entregables**:
- Sistema optimizado
- Features avanzadas
- Documentation completa

### Rollback Plan
En caso de problemas críticos:
1. **Rollback a newsletter**: Versión previa mantenida en git
2. **Rollback de datos**: Backups automáticos de PostgreSQL
3. **Rollback de arquitectura**: Docker compose con versiones previas

## Monitoreo y Validación

### Métricas de Éxito
- **Performance**: Dashboard carga en <3 segundos
- **Usabilidad**: >80% user satisfaction en testing
- **Cobertura**: >15 fuentes de noticias activas
- **Analytics**: Datos de ≥6 meses para tendencias significativas

### Criterios de Rollback
- **Performance crítica**: Dashboard inutilizable (>10s carga)
- **Data integrity**: Pérdida o corrupción de datos analytics
- **Legal issues**: Cualquier problema legal emergente

### Fecha de Revisión
**2025-09-27** - Evaluar éxito del cambio y planificar próximas expansiones

## Referencias
- [Conversación de Kickoff](../conversations/2025-06-27_project-kickoff.md)
- [README Original](../../README.md) - Documentación del sistema original
- [Prototipo Dashboard](../product/requirements/functional-requirements.md) (Pendiente)

## Impacto en Componentes Existentes

### Componentes Eliminados
- **Publisher WordPress**: Ya no se publica a WordPress
- **Newsletter Generation**: LLM ya no genera newsletters completos
- **Copywriter Structure Builder**: Específico para newsletters

### Componentes Transformados
- **Scraper**: Mantiene funcionalidad, cambia destino (PostgreSQL vs archivos)
- **NLP Analyzer**: Expande a sentiment analysis y topic classification
- **Decision Engine**: Cambia de "¿publicar?" a "analytics aggregation"
- **Orchestrator**: Coordina analytics pipeline vs publishing pipeline

### Componentes Nuevos
- **Analytics Aggregation Service**: Pre-calcula métricas para dashboard
- **REST API Service**: Sirve datos al frontend React
- **Sentiment Analysis Service**: Clasifica tono emocional
- **Geographic Classification**: Clasifica por países/regiones

## Historial de Cambios
| Fecha | Cambio | Autor |
|-------|--------|-------|
| 2025-06-27 | Creación del ADR tras identificación de problemas legales | Claude |

---
**Próxima revisión**: 2025-08-27 (revisión bimensual)
**ADRs relacionados**: ADR-002 (Database Architecture), ADR-003 (Technology Stack)
