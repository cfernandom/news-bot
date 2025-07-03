# Prompt: Fix Legacy Critical Issues - PreventIA News Analytics

## Contexto de la Sesión

Soy el Director Técnico de PreventIA News Analytics trabajando en resolver **6 issues críticos** identificados durante el testing comprehensivo del sistema legacy. El testing suite está completamente implementado (18 API tests + 120+ React tests) pero revela problemas que bloquean el deployment a producción.

## Estado Actual del Sistema

- **✅ COMPLETADO**: Legacy testing suite implementado y documentado
- **⚠️ CRÍTICO**: 6 issues identificados requieren fixes inmediatos
- **🎯 OBJETIVO**: Resolver issues críticos y alcanzar 90%+ test pass rate
- **⏱️ ETA TOTAL**: ~2 horas para fixes críticos + validación

## Issues Críticos Priorizados (En Orden de Ejecución)

### 🔴 ISSUE #1: Timezone Handling API Timeline (ETA: 30min)
```python
# Location: services/api/routers/legacy.py:257
# Error: TypeError: can't subtract offset-naive and offset-aware datetimes
# Tests Failing: test_get_tones_timeline_legacy (2 tests)

# Current Code (BROKEN):
cutoff_date = datetime.now() - timedelta(weeks=weeks)

# Required Fix:
cutoff_date = datetime.now(timezone.utc) - timedelta(weeks=weeks)
```

### 🔴 ISSUE #2: Data Format Mismatch Components (ETA: 15min)
```typescript
// Location: src/components/legacy/Analytics/LegacySentimentChart.tsx
// Error: data.map is not a function
// Tests Failing: LegacySentimentChart (5/10 tests)

// Component expects SentimentData[] but receives Object format
// Need to ensure consistent interface throughout
```

### 🔴 ISSUE #3: SQL Query Geographic Endpoints (ETA: 45min)
```python
# Location: services/api/routers/legacy.py:337-361
# Error: Raw SQL parameter formatting issues
# Tests Failing: test_get_stats_geo_legacy (2 tests)

# Issue: Incorrect asyncpg parameter binding in raw SQL queries
```

### 🟡 ISSUE #4-6: Secondary Issues (ETA: 3h total)
- Chart Library Mismatch (Tests mock Chart.js, components use Recharts)
- Language Inconsistency (Spanish titles, English test expectations)
- Input Validation (API crashes on invalid date inputs)

## Comandos de Testing para Validación

```bash
# Test individual issues after fixes
pytest integration/test_api/test_legacy_api.py::TestLegacyAPIEndpoints::test_get_tones_timeline_legacy -v
npx vitest run src/components/legacy/__tests__/LegacySentimentChart.test.tsx
pytest integration/test_api/test_legacy_api.py::TestLegacyAPIEndpoints::test_get_stats_geo_legacy -v

# Run complete legacy test suite
cd tests && pytest integration/test_api/test_legacy_api.py -v
cd preventia-dashboard && npx vitest run src/components/legacy/__tests__/

# Verify target metrics
# Target: 90%+ API tests passing (currently 67% - 12/18)
# Target: 85%+ Component tests passing (currently 50%+)
```

## Documentación de Referencia

- **`docs/implementation/legacy-testing-results.md`** - Análisis detallado de issues
- **`docs/implementation/testing-coverage-dashboard.md`** - Dashboard visual con métricas
- **Current test status**: 72% overall coverage, 6 critical blockers identified

## Objetivos de la Sesión

### 🎯 Primary Goals (Must Complete)
1. **Fix timezone issues** en API timeline endpoints
2. **Fix data format mismatch** en LegacySentimentChart component
3. **Fix SQL query issues** en geographic endpoints
4. **Validate fixes** con re-run de test suite completo
5. **Update documentation** con resultados post-fix

### 🎯 Secondary Goals (If Time Permits)
1. **Fix chart library mismatch** (Recharts vs Chart.js mocks)
2. **Standardize language** (español vs inglés en tests/components)
3. **Implement input validation** para error handling graceful
4. **Performance baseline** measurements

## Success Criteria

- ✅ **90%+ API legacy tests passing** (from current 67%)
- ✅ **85%+ React component tests passing** (from current 50%+)
- ✅ **Zero critical blockers** outstanding
- ✅ **Documentation updated** with post-fix results
- ✅ **Production readiness** confidence level > 90%

## Arquitectura y Contexto Técnico

**Sistema**: PreventIA News Analytics - Plataforma de análisis de noticias médicas
**Stack**: FastAPI + PostgreSQL + React + TypeScript + Recharts
**Deployment**: Docker containers con health checks
**Testing**: pytest + vitest + 138+ tests implementados

**Key Files**:
- API Legacy: `services/api/routers/legacy.py` (378 líneas)
- Components: `src/components/legacy/Analytics/` (8 componentes)
- Tests: `tests/integration/test_api/test_legacy_api.py` + `src/components/legacy/__tests__/`

## Approach Recomendado

1. **Start con Issue #1** (timezone) - Es el más directo y desbloqueará 2 tests
2. **Continue con Issue #2** (data format) - Quick win para component tests
3. **Tackle Issue #3** (SQL queries) - Más complejo pero crítico para geographic analytics
4. **Validate extensively** después de cada fix
5. **Update documentation** para reflejar nuevo estado
6. **Assess secondary issues** si hay tiempo disponible

## Working Directory
```bash
cd /home/cfernandom/proyectos/preventia/news_bot_3
```

**INSTRUCCIONES**: Asume el rol de Senior Software Engineer y procede a resolver estos issues críticos sistemáticamente. Usa los tests como validación continua y mantén la documentación actualizada con el progreso.
