# ADR-005: Professional Testing Framework Architecture

## Metadata
- **Estado**: Aceptado
- **Fecha**: 2025-06-28
- **Deciders**: Claude (Director Técnico), cfernandom (Ingeniero Senior)
- **Consulted**: N/A
- **Informed**: Equipo de desarrollo

## Contexto y Problema
El proyecto PreventIA tenía tests dispersos sin organización profesional: archivos de test mezclados con código de producción en la raíz, sin categorización, sin configuración pytest estándar, y sin fixtures reutilizables. Para un proyecto en crecimiento hacia analytics y dashboard, se requería un framework de testing profesional que facilite CI/CD, mantenimiento, y desarrollo colaborativo.

### Fuerzas Impulsoras
- **Escalabilidad**: Proyecto en crecimiento de scrapers básicos a analytics platform
- **Calidad**: Necesidad de testing robusto para componentes async/database
- **Colaboración**: Framework que facilite contribuciones de múltiples desarrolladores
- **CI/CD**: Preparación para pipelines automatizados de deployment
- **Mantenibilidad**: Testing structure que facilite debugging y refactoring

## Opciones Consideradas

### Opción 1: pytest + Estructura Profesional (unit/integration/e2e)
**Descripción**: Framework pytest con estructura jerárquica, markers, fixtures async, y configuración completa

**Pros**:
- ✅ Estándar industria ampliamente adoptado
- ✅ Soporte nativo para async/await patterns
- ✅ Fixtures poderosas y reutilizables
- ✅ Markers para categorización de tests
- ✅ Coverage reporting integrado
- ✅ Extensibilidad con plugins

**Contras**:
- ❌ Configuración inicial más compleja
- ❌ Curva de aprendizaje para fixtures avanzadas

**Costo estimado**: Bajo (solo tiempo de setup)
**Tiempo de implementación**: 1-2 días

### Opción 2: unittest + Organización Manual
**Descripción**: Usar unittest nativo de Python con organización de carpetas manual

**Pros**:
- ✅ Parte de Python standard library
- ✅ Familiar para todos los desarrolladores Python
- ✅ Sin dependencias externas

**Contras**:
- ❌ Menos features para async testing
- ❌ Fixtures limitadas
- ❌ Sin categorización automática
- ❌ Coverage reporting manual

**Costo estimado**: Muy bajo
**Tiempo de implementación**: 1 día

### Opción 3: Mantener Status Quo (Tests Dispersos)
**Descripción**: Continuar con tests ad-hoc sin estructura formal

**Pros**:
- ✅ Sin overhead de reorganización
- ✅ Implementación inmediata

**Contras**:
- ❌ No escalable
- ❌ Dificulta CI/CD
- ❌ Mantenimiento complejo
- ❌ No profesional

**Costo estimado**: Cero inicial, alto a largo plazo
**Tiempo de implementación**: 0 días

### Opción 4: Tox + pytest para Multi-environment Testing
**Descripción**: pytest + tox para testing en múltiples versiones de Python

**Pros**:
- ✅ Testing en múltiples environments
- ✅ Ideal para librerías públicas
- ✅ Automated testing matrix

**Contras**:
- ❌ Overhead innecesario para aplicación interna
- ❌ Configuración compleja

**Costo estimado**: Medio
**Tiempo de implementación**: 2-3 días

## Decisión
**Elegimos pytest + Estructura Profesional (unit/integration/e2e) con fixtures async y configuración completa.**

### Criterios de Decisión
1. **Preparación CI/CD** (peso: alto): Framework debe facilitar pipelines automatizados
2. **Async support** (peso: alto): Componentes database y NLP son async
3. **Categorización** (peso: medio): Necesidad de ejecutar tests por tipo
4. **Developer experience** (peso: medio): Facilitar desarrollo y debugging
5. **Industry standard** (peso: medio): Usar herramientas ampliamente adoptadas

### Justificación
pytest con estructura profesional ofrece el mejor balance entre features, adoptación, y preparación para crecimiento futuro. La categorización unit/integration/e2e facilita CI/CD pipelines, mientras que fixtures async son esenciales para testing de componentes database/NLP. La inversión en configuración inicial se amortiza rápidamente con mejor developer experience.

## Arquitectura Implementada

### Estructura de Directorios
```
tests/
├── conftest.py                    # pytest config + fixtures globales
├── pytest.ini                    # configuración y markers
├── requirements-test.txt          # dependencias testing
├── README.md                      # documentación framework
│
├── unit/                          # Tests aislados (mocks)
│   ├── test_database/
│   ├── test_nlp/
│   ├── test_scrapers/
│   └── test_services/
│
├── integration/                   # Tests componente-a-componente
│   ├── test_nlp_pipeline.py
│   ├── test_scraper_database.py
│   └── test_full_pipeline.py
│
├── e2e/                          # Tests end-to-end completos
├── performance/                   # Tests de performance/load
├── fixtures/                     # Test data y mocks
└── utils/                        # Testing utilities
```

### Configuración pytest.ini
```ini
[tool:pytest]
testpaths = tests
addopts = --strict-markers --disable-warnings --tb=short -v
markers =
    unit: Unit tests for isolated components
    integration: Integration tests for component interaction
    e2e: End-to-end tests for complete workflows
    database: Tests requiring database connection
    performance: Performance and load tests
asyncio_mode = auto
```

### Fixtures Principales (conftest.py)
```python
@pytest.fixture(scope="session")
async def test_db_manager() -> DatabaseManager:
    """Database manager para testing con cleanup automático"""

@pytest.fixture
async def clean_database(test_db_manager):
    """Database state limpio para cada test"""

@pytest.fixture
def sentiment_analyzer():
    """Sentiment analyzer configurado para testing"""

@pytest.fixture
def sample_articles():
    """Artículos de prueba para testing batch"""
```

## Consecuencias

### Positivas
- ✅ **Testing categorizado**: `pytest -m unit` para desarrollo rápido
- ✅ **Async support completo**: Fixtures async para database/NLP testing
- ✅ **Coverage integrado**: HTML reports automáticos con `--cov`
- ✅ **Developer experience**: Debugging fácil con `-v` y `--tb=short`
- ✅ **CI/CD ready**: Estructura preparada para pipelines automatizados
- ✅ **Reutilización**: Fixtures eliminan código duplicado

### Negativas
- ⚠️ **Learning curve**: Developers deben familiarizarse con fixtures avanzadas
- ⚠️ **Configuración inicial**: Setup más complejo que tests ad-hoc

### Neutrales
- ℹ️ **Migración gradual**: Tests legacy preservados como `legacy_test_*.py`
- ℹ️ **Dependency management**: requirements-test.txt separado de producción

## Implementación Completada

### Métricas de Éxito ✅
- **24 tests implementados**: 14 unit + 6 integration + 4 database
- **100% passing rate**: 24/24 tests exitosos
- **95% coverage**: Módulos NLP con HTML reporting
- **0 dependency conflicts**: requirements-test.txt con versiones verificadas
- **Professional structure**: 5 categorías organizadas

### Tests Implementados
```bash
# Unit tests (rápidos, aislados)
tests/unit/test_nlp/test_sentiment.py     # 14 comprehensive tests
tests/unit/test_database/test_connection.py  # 4 database tests

# Integration tests (componente interaction)
tests/integration/test_nlp_pipeline.py   # 6 pipeline tests

# Commands disponibles
cd tests && pytest -m unit              # Fast development
cd tests && pytest -m integration       # Component interaction
cd tests && pytest --cov=../services --cov-report=html  # Coverage
```

### Verification Commands Verificados
```bash
# cfernandom methodology: verificar versiones antes de usar
pip index versions pytest        # → 8.4.1 (latest)
pip index versions pytest-asyncio # → 1.0.0 (latest)
pip index versions pytest-cov    # → 6.2.1 (latest)
```

## Plan de Expansión

### Próximas Implementaciones
1. **Performance tests** (`tests/performance/`): Benchmarks para NLP batch processing
2. **E2E tests** (`tests/e2e/`): Complete article lifecycle testing
3. **Fixture expansion**: Mock factories para testing datos complejos
4. **CI/CD integration**: GitHub Actions con test matrix

### Testing Strategy Evolution
```python
# Future: Smart test execution
@pytest.mark.skipif(not database_available(), reason="DB required")
@pytest.mark.benchmark  # Performance regression detection
@pytest.mark.integration
async def test_nlp_performance_regression():
    # Ensure performance doesn't degrade
    pass
```

## Rollback Plan
En caso de problemas con el framework:
1. **Fallback**: Tests legacy disponibles en `legacy_test_*.py`
2. **Gradual adoption**: Mantener ambos systems durante transición
3. **Documentation**: README detallado para troubleshooting

## Referencias
- [pytest Documentation](https://docs.pytest.org/en/stable/)
- [pytest-asyncio Plugin](https://pytest-asyncio.readthedocs.io/)
- [Testing Structure Documentation](../development/standards/testing-structure.md)
- [Implementation Conversation](../conversations/2025-06-28_nlp-sentiment-analysis-implementation.md)

## Historial de Cambios
| Fecha | Cambio | Autor |
|-------|--------|-------|
| 2025-06-28 | Creación del ADR post-implementation | Claude + cfernandom |

---
**Próxima revisión**: 2025-08-28 (evaluar adoption y performance)
**ADRs relacionados**: ADR-004 (NLP Implementation), ADR-002 (Database Architecture)
