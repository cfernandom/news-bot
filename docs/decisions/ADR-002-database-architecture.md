# ADR-002: Arquitectura de Base de Datos - PostgreSQL con Enfoque Híbrido

## Metadata
- **Estado**: Aceptado
- **Fecha**: 2025-06-27
- **Deciders**: Claude (Dirección Técnica), cfernandom (Ingeniero Senior)
- **Consulted**: N/A (equipo inicial)
- **Informed**: Equipo de desarrollo futuro

## Contexto y Problema
El cambio de alcance del proyecto requiere una nueva arquitectura de base de datos optimizada para analytics complejos en lugar de simple storage de artículos. Necesitamos soportar consultas analíticas pesadas, agregaciones temporales, y análisis de sentimientos mientras mantenemos performance para operaciones CRUD básicas.

### Fuerzas Impulsoras
- **Analytics complejos**: Consultas de agregación, trending analysis, geographic distribution
- **Performance**: Dashboard debe cargar rápido con miles de artículos
- **Escalabilidad**: Sistema debe crecer a múltiples países y fuentes
- **Flexibilidad**: Estructura debe adaptarse a nuevos tipos de análisis
- **Experiencia del equipo**: cfernandom tiene experiencia sólida con PostgreSQL

## Opciones Consideradas

### Opción 1: SQLite (mantener simplicidad)
**Descripción**: Continuar con SQLite local para development, deployment simple

**Pros**:
- ✅ Sin configuración de servidor
- ✅ Deployment simple
- ✅ Zero-configuration development
- ✅ Backup simple (archivos)

**Contras**:
- ❌ Performance limitada para analytics complejos
- ❌ Sin concurrent writes efectivos
- ❌ Limitado para agregaciones pesadas
- ❌ No escalable para múltiples usuarios

**Costo estimado**: Muy bajo
**Tiempo de implementación**: Continuar actual

### Opción 2: PostgreSQL con ORM puro
**Descripción**: PostgreSQL con SQLAlchemy ORM exclusivamente

**Pros**:
- ✅ Performance excelente para analytics
- ✅ Concurrent access robusto
- ✅ Extensiones avanzadas (JSON, full-text search)
- ✅ Experiencia del equipo
- ✅ Ecosystem maduro Python

**Contras**:
- ❌ ORM puede ser lento para queries complejos
- ❌ Menos control sobre optimizaciones SQL
- ❌ Curva de aprendizaje para queries avanzados

**Costo estimado**: Medio
**Tiempo de implementación**: 1 semana

### Opción 3: PostgreSQL híbrido (ORM + Raw SQL)
**Descripción**: PostgreSQL con SQLAlchemy para CRUD, raw SQL para analytics

**Pros**:
- ✅ Mejores características de ambos enfoques
- ✅ Performance óptima para analytics (raw SQL)
- ✅ Productividad para CRUD (ORM)
- ✅ Flexibilidad máxima
- ✅ Control granular sobre optimizaciones

**Contras**:
- ❌ Complejidad adicional mantener dos paradigmas
- ❌ Más curva de aprendizaje
- ❌ Potential inconsistencies entre enfoques

**Costo estimado**: Medio-Alto
**Tiempo de implementación**: 1-2 semanas

### Opción 4: NoSQL (MongoDB/Redis)
**Descripción**: Base de datos orientada a documentos para flexibilidad

**Pros**:
- ✅ Schema flexible
- ✅ JSON nativo
- ✅ Horizontal scaling fácil

**Contras**:
- ❌ Menos experiencia del equipo
- ❌ Analytics complejos más difíciles
- ❌ Menos maduro para reporting
- ❌ Migration path más complejo

**Costo estimado**: Alto
**Tiempo de implementación**: 3-4 semanas

## Decisión
**Opción elegida**: PostgreSQL híbrido (ORM + Raw SQL) - Opción 3

### Criterios de Decisión
1. **Performance para analytics** (peso: crítico): Raw SQL permite optimizaciones máximas
2. **Productividad desarrollo** (peso: alto): ORM acelera operaciones CRUD comunes
3. **Experiencia del equipo** (peso: alto): cfernandom domina PostgreSQL
4. **Escalabilidad** (peso: alto): PostgreSQL probado para analytics pesados
5. **Flexibilidad futura** (peso: medio): Híbrido permite adaptación

### Justificación
El enfoque híbrido maximiza las fortalezas de ambos paradigmas. Para operaciones CRUD básicas (gestión de fuentes, artículos individuales), SQLAlchemy ORM proporciona productividad y type safety. Para analytics complejos (trending analysis, agregaciones temporales, queries de dashboard), raw SQL permite optimizaciones granulares y uso de características avanzadas de PostgreSQL.

## Consecuencias

### Positivas
- ✅ **Performance optimizada**: Raw SQL para queries pesados
- ✅ **Productividad alta**: ORM para operaciones comunes
- ✅ **Escalabilidad probada**: PostgreSQL handle millones de registros
- ✅ **Flexibilidad máxima**: Híbrido adapta a diferentes necesidades
- ✅ **Ecosystem maduro**: Herramientas, monitoring, backup

### Negativas
- ⚠️ **Complejidad adicional**: Dos paradigmas para mantener
- ⚠️ **Curva de aprendizaje**: Team debe dominar ambos enfoques
- ⚠️ **Potential inconsistencies**: Lógica dividida entre ORM y raw SQL

### Neutrales
- ℹ️ **Infrastructure**: Requiere PostgreSQL server (Docker)
- ℹ️ **Backup strategy**: Más complejo que SQLite
- ℹ️ **Development setup**: Configuración inicial más compleja

## Plan de Implementación

### Schema Design
```sql
-- Fuentes dinámicas con validación
news_sources: gestión de fuentes que pueden agregarse dinámicamente
articles: artículos con campos de análisis (sentiment, topic, keywords)
article_keywords: keywords extraídas con relevance scores
weekly_analytics: métricas pre-calculadas para performance dashboard
```

### Technology Stack
- **Database**: PostgreSQL 16+ 
- **ORM**: SQLAlchemy 2.0 con async support
- **Raw SQL**: asyncpg para maximum performance
- **Migrations**: Alembic para schema versioning
- **Connection pooling**: Built-in asyncpg pooling

### Separation of Concerns
```python
# ORM para CRUD básico
class ArticleRepository:
    async def create_article(self, article_data) -> Article
    async def get_article_by_id(self, article_id) -> Article
    async def update_article(self, article_id, updates) -> Article

# Raw SQL para analytics
class AnalyticsService:
    async def get_weekly_trends(self, date_range) -> WeeklyTrends
    async def get_sentiment_distribution(self, filters) -> SentimentStats
    async def get_geographic_analysis(self) -> GeographicData
```

### Performance Optimizations
- **Indexes**: Optimizados para queries de dashboard
- **Materialized views**: Para métricas costosas de calcular
- **Query optimization**: EXPLAIN ANALYZE para todas las queries críticas
- **Connection pooling**: Configurado para concurrent dashboard users

## Monitoreo y Validación

### Métricas de Performance
- **CRUD operations**: <100ms para operaciones básicas
- **Analytics queries**: <2s para consultas de dashboard
- **Concurrent users**: Soporte para 20+ usuarios simultáneos
- **Data volume**: Eficiente hasta 100K+ artículos

### Criterios de Rollback
- **Performance degradation**: >5s para queries críticos
- **Data integrity issues**: Cualquier corrupción o inconsistencia
- **Complexity overhead**: Si hybrid approach genera más problemas que beneficios

### Fecha de Revisión
**2025-10-27** - Evaluar performance y considerar optimizaciones adicionales

## Schema Implementation

### Core Tables
```sql
news_sources    -- Fuentes dinámicas con validación automática
articles        -- Artículos con análisis NLP integrado  
article_keywords -- Keywords con relevance scoring
weekly_analytics -- Métricas agregadas pre-calculadas
```

### Key Features
- **UUID support**: Para mejor distribution y security
- **JSONB columns**: Para data flexible (sentiment details, metadata)
- **Full-text search**: PostgreSQL native para article content
- **Temporal queries**: Optimizado para time-series analysis
- **Audit trails**: Tracking de cambios para compliance

### Data Integrity
- **Foreign key constraints**: Relationships enforced at DB level
- **Check constraints**: Data validation (sentiment scores -1 to 1)
- **Unique constraints**: Prevent duplicate articles by URL
- **Triggers**: Automatic timestamp updates

## Referencias
- [ADR-001 Project Scope Change](./ADR-001-project-scope-change.md)
- [Database Models Implementation](../../../services/data/database/models.py)
- [Migration Scripts](../../../services/data/database/migrations/)
- [Database Connection Management](../../../services/data/database/connection.py)

## Testing Strategy
- **Unit tests**: Para repositories y services
- **Integration tests**: Database operations end-to-end
- **Performance tests**: Load testing con datasets grandes
- **Migration tests**: Forward/backward compatibility

## Historial de Cambios
| Fecha | Cambio | Autor |
|-------|--------|-------|
| 2025-06-27 | Creación del ADR con decisión híbrida | Claude |
| 2025-06-27 | Implementación schema inicial | Claude |

---
**Próxima revisión**: 2025-09-27 (revisión trimestral)
**ADRs relacionados**: ADR-001 (Project Scope), ADR-003 (API Architecture)