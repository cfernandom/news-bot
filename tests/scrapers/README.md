# Testing Framework para Scrapers Migrados

Sistema de testing estandarizado para validar scrapers migrados a PostgreSQL con métricas consistentes y reportes detallados.

## Estructura de Tests

### 🧪 Framework Base
- `test_scraper_framework.py` - Framework estandarizado para testing de scrapers
- `test_all_migrated_scrapers.py` - Suite completo para todos los scrapers migrados

### 📊 Tests Disponibles
- `test_phase1_scraper.py` - Test original de validación de Fase 1
- `test_breastcancer_scraper.py` - Test específico de debugging
- `debug_breastcancer_structure.py` - Debug de estructura HTML

## Framework de Testing

### Características Principales

#### ✅ Tests Obligatorios
1. **Database Connection** - Verificar conexión PostgreSQL
2. **Source Verification** - Confirmar que la fuente existe en news_sources
3. **Scraper Execution** - Ejecutar scraper y medir performance
4. **Data Quality** - Validar integridad y completeness de datos
5. **Performance Metrics** - Medir eficiencia y velocidad
6. **Scraper Specific** - Tests específicos por scraper (implementado por subclase)

#### 📊 Métricas Medidas
- **Execution Time** - Tiempo total de ejecución
- **Articles Added** - Número de artículos nuevos insertados
- **Data Completeness** - Porcentaje de campos completos
- **URL Uniqueness** - Detección de duplicados
- **Performance Efficiency** - Artículos por segundo

## Uso del Framework

### Test Individual
```bash
# Ejecutar framework de test específico
cd tests/scrapers/
python test_scraper_framework.py
```

### Suite Completo
```bash
# Ejecutar todos los scrapers migrados
python test_all_migrated_scrapers.py
```

### Test de Debugging
```bash
# Debug específico de estructura HTML
python debug_breastcancer_structure.py
```

## Implementar Nuevo Test

### 1. Crear Clase de Test
```python
from test_scraper_framework import ScraperTestFramework

class MiScraperTest(ScraperTestFramework):
    def __init__(self):
        super().__init__(
            scraper_name="Mi Scraper",
            scraper_function=mi_scraper_function,
            expected_source_name="Mi Fuente"
        )
    
    async def test_scraper_specific(self):
        """Tests específicos para mi scraper"""
        # Implementar validaciones específicas
        pass
```

### 2. Ejecutar Test
```python
async def main():
    results = await run_scraper_test(MiScraperTest)
    print(results)

asyncio.run(main())
```

## Reportes de Test

### Métricas Estándar
- **Success Rate** - Porcentaje de tests pasados
- **Execution Time** - Tiempo de ejecución del scraper
- **Data Quality Score** - Completeness de campos obligatorios
- **Performance Rating** - Eficiencia (excellent/good/needs_optimization)

### Interpretación de Resultados
- **✅ 80%+ Success Rate** - EXCELLENT - Listo para producción
- **✅ 60-79% Success Rate** - GOOD - Revisar tests fallidos
- **⚠️  <60% Success Rate** - NEEDS IMPROVEMENT - Requiere atención

## Tests Específicos por Scraper

### Breast Cancer Org
- Verificación de patrón URL `/research-news/`
- Validación de estructura React/Next.js

### WebMD
- Calidad de parsing de fechas múltiples formatos
- Validación de estructura de metadatos

### CureToday
- Calidad de summaries extraídos
- Validación de detección de duplicados local

### News Medical
- Consistencia de metadata (country: International)
- Validación de campos de clasificación

## Configuración

### Prerequisitos
```bash
# Variables de entorno requeridas
DATABASE_URL=postgresql://user:pass@localhost:5433/db_name

# Dependencias
pip install playwright beautifulsoup4 asyncpg python-dotenv
```

### Base de Datos
- PostgreSQL debe estar ejecutándose
- Tablas `news_sources` y `articles` deben existir
- Al menos una fuente configurada por scraper

## Extensiones Futuras

### 📈 Métricas Avanzadas
- Rate limiting compliance
- Error handling robustness
- Memory usage profiling
- Network efficiency

### 🤖 Automatización
- CI/CD integration
- Scheduled test runs
- Alertas automáticas
- Regression testing

### 📊 Reporting
- HTML reports
- Trend analysis
- Performance baselines
- Quality scorecards

## Troubleshooting

### Errores Comunes
1. **ModuleNotFoundError** - Verificar PYTHONPATH en setup
2. **Database Connection** - Confirmar PostgreSQL ejecutándose
3. **Source Not Found** - Verificar datos en tabla news_sources
4. **Playwright Issues** - Instalar navegadores: `playwright install chromium`

### Debug Tips
1. Usar `debug_breastcancer_structure.py` para analizar HTML
2. Verificar logs de scraper para patrones no detectados
3. Validar selectores CSS en browser dev tools
4. Confirmar estructura de datos en PostgreSQL

---
*Framework creado: 2025-06-27*  
*Autor: Claude Code (Director Técnico)*  
*Revisor: Cristhian F. Moreno (Senior Engineer)*