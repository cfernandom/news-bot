# Conversaciones Técnicas - Índice

Este directorio contiene el registro de todas las conversaciones técnicas importantes del proyecto NewsBot.

## 📋 Índice de Conversaciones

| Fecha | Título | Participantes | Tipo | Temas Clave | Estado |
|-------|--------|---------------|------|-------------|--------|
| 2025-06-27 | [Project Kickoff & Documentation Structure](2025-06-27_project-kickoff.md) | Claude, cfernandom | Planning | Estructura inicial, Roadmap técnico | ✅ Completado |
| 2025-06-27 | [Database Implementation & Architecture Setup](2025-06-27_database-implementation.md) | Claude, cfernandom | Development/Architecture | PostgreSQL, Híbrido ORM+SQL, Testing | ✅ Completado |
| 2025-06-28 | [NLP Sentiment Analysis + Testing Framework](2025-06-28_nlp-sentiment-analysis-implementation.md) | Claude, cfernandom | Development | VADER+spaCy, Testing profesional, Metrics validation | ✅ Completado |

## 📝 Cómo Usar Este Registro

### Para Desarrolladores
1. **Antes de trabajar en algo nuevo**: Revisa conversaciones relacionadas
2. **Después de sesiones importantes**: Documenta usando el [template](templates/conversation-template.md)
3. **Al buscar decisiones pasadas**: Usa la tabla de índice arriba

### Para Mantener el Registro
1. **Crear nueva conversación**: Usa el template en `templates/conversation-template.md`
2. **Nombrar archivos**: Formato `YYYY-MM-DD_titulo-descriptivo.md`
3. **Actualizar índice**: Agregar entrada en la tabla arriba
4. **Referencias cruzadas**: Linkear a ADRs y documentación relacionada

## 🏷️ Tipos de Conversaciones

- **Planning**: Sesiones de planificación y roadmap
- **Development**: Conversaciones durante desarrollo activo
- **Review**: Revisiones de código y arquitectura
- **Architecture**: Decisiones arquitectónicas importantes
- **Debugging**: Sesiones de resolución de problemas
- **Retrospective**: Retrospectivas y lecciones aprendidas

## 📊 Estadísticas

- **Total conversaciones documentadas**: 3
- **Conversaciones activas este mes**: 3
- **Decisiones técnicas derivadas**: 8
- **Action items pendientes**: 1 (ADR creation pending)

## 🔍 Búsqueda Rápida

### Por Tema
- **Arquitectura**: [2025-06-27 Project Kickoff](2025-06-27_project-kickoff.md), [2025-06-27 Database Implementation](2025-06-27_database-implementation.md)
- **Documentación**: [2025-06-27 Project Kickoff](2025-06-27_project-kickoff.md), [2025-06-27 Database Implementation](2025-06-27_database-implementation.md)
- **Database**: [2025-06-27 Database Implementation](2025-06-27_database-implementation.md)
- **Testing**: [2025-06-27 Database Implementation](2025-06-27_database-implementation.md), [2025-06-28 NLP Implementation](2025-06-28_nlp-sentiment-analysis-implementation.md)
- **NLP/Sentiment**: [2025-06-28 NLP Implementation](2025-06-28_nlp-sentiment-analysis-implementation.md)
- **Metrics Validation**: [2025-06-28 NLP Implementation](2025-06-28_nlp-sentiment-analysis-implementation.md)
- **Performance**: [Pendiente]
- **Deployment**: [Pendiente]

### Por Componente
- **Database**: [2025-06-27 Database Implementation](2025-06-27_database-implementation.md)
- **Analytics Pipeline**: [2025-06-27 Project Kickoff](2025-06-27_project-kickoff.md), [2025-06-27 Database Implementation](2025-06-27_database-implementation.md)
- **Scraper**: [2025-06-27 Database Implementation](2025-06-27_database-implementation.md)
- **NLP**: [2025-06-28 NLP Implementation](2025-06-28_nlp-sentiment-analysis-implementation.md)
- **Testing Framework**: [2025-06-28 NLP Implementation](2025-06-28_nlp-sentiment-analysis-implementation.md)
- **FastAPI**: [Pendiente]
- **React Dashboard**: [Pendiente]

## 📋 Templates Disponibles

- [Conversation Template](templates/conversation-template.md) - Template estándar para conversaciones
- ADR Template - Ver [decisions/adr-template.md](../decisions/adr-template.md)

## ⚠️ Buenas Prácticas

1. **Documenta en tiempo real**: Es mejor documentar durante o inmediatamente después de la conversación
2. **Sé específico**: Incluye comandos exactos, decisiones concretas, y next steps claros
3. **Referencia cruzada**: Linkea a ADRs, issues, PRs relevantes
4. **Update action items**: Marca como completados cuando sea apropiado
5. **Mantén el índice actualizado**: El índice es la puerta de entrada principal

---
**Última actualización**: 2025-06-28  
**Próxima revisión del proceso**: 2025-07-27