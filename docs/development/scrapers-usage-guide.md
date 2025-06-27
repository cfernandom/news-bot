# Guía de Uso - Scrapers Migrados a PostgreSQL

Documentación completa para el uso, testing y mantenimiento de los scrapers migrados en FASE 1.

## Resumen Ejecutivo

4 scrapers han sido migrados exitosamente a PostgreSQL con estructura analytics-ready:
- **Breast Cancer Org**: 25 artículos
- **WebMD**: 31 artículos  
- **CureToday**: 30 artículos
- **News Medical**: 20 artículos

**Total: 106 artículos** con integridad 100% y 0% duplicados.

## Uso Básico

### Ejecutar Scraper Individual

```bash
# Activar entorno virtual
source venv/bin/activate

# Ejecutar scraper específico
python scripts/run_migrated_scrapers.py breastcancer.org
python scripts/run_migrated_scrapers.py webmd.com
python scripts/run_migrated_scrapers.py curetoday.com
python scripts/run_migrated_scrapers.py news-medical.net
```

### Verificar Scrapers Disponibles

```bash
# Ver lista de scrapers disponibles
python scripts/run_migrated_scrapers.py
```

### Ejecutar Todos los Scrapers

```bash
# Ejecutar batch completo (experimental)
python scripts/run_migrated_scrapers.py all
```

## Testing y Validación

### Framework de Testing

```bash
# Test individual con framework estandarizado
cd tests/scrapers/
python test_scraper_framework.py

# Suite completo de tests
python test_all_migrated_scrapers.py

# Debug específico de estructura HTML
python debug_breastcancer_structure.py
```

### Métricas de Validación

El framework mide automáticamente:
- **Execution Time**: Tiempo de ejecución del scraper
- **Data Quality**: Completeness de campos obligatorios  
- **Performance**: Artículos por segundo
- **Uniqueness**: Detección de duplicados
- **Specific Tests**: Validaciones específicas por scraper

## Arquitectura Técnica

### Estructura de Scraper Migrado

```python
async def scrape_[source]_to_postgres() -> List[int]:
    """
    Patrón estándar de scraper migrado:
    1. Obtener source_id de PostgreSQL
    2. Usar Playwright para JavaScript rendering
    3. Parsear con BeautifulSoup
    4. Calcular metadata (hash, word_count)
    5. Verificar duplicados por URL
    6. Insertar directamente en PostgreSQL
    7. Retornar lista de IDs insertados
    """
```

### Campos Analytics Preparados

```sql
-- Campos obligatorios
title, url, published_at, scraped_at, source_id

-- Metadata automática
content_hash, word_count, language, country

-- Preparados para FASE 2
sentiment_score, sentiment_label, topic_category
```

### Detección de Duplicados

```python
# Verificación automática por URL antes de insertar
existing_query = "SELECT id FROM articles WHERE url = $1 LIMIT 1"
existing = await db_manager.execute_sql_one(existing_query, full_url)

if existing:
    articles_duplicated += 1
    continue  # Skip duplicate
```

## Configuración y Requisitos

### Variables de Entorno

```bash
# .env file required
DATABASE_URL=postgresql://user:pass@localhost:5433/db_name
POSTGRES_DB=preventia_news
POSTGRES_USER=preventia  
POSTGRES_PASSWORD=preventia123
```

### Dependencias

```bash
# Core dependencies
pip install playwright beautifulsoup4 asyncpg python-dotenv

# Install browser for Playwright
playwright install chromium
```

### Base de Datos

PostgreSQL debe estar ejecutándose con:
- Tabla `news_sources` poblada con las 8 fuentes
- Tabla `articles` con estructura analytics completa
- Conexión en puerto 5433 (configurado en docker-compose)

## Scrapers Específicos

### 1. Breast Cancer Org
- **URL**: `https://www.breastcancer.org/research-news`
- **Tecnología**: Playwright (React/Next.js site)
- **Particularidades**: Estructura dinámica, selectores CSS específicos
- **Performance**: ~2.5s, 25 artículos típicos

```python
# Uso programático
from services.scraper.src.extractors.www_breastcancer_org_postgres import scrape_breastcancer_org_to_postgres

article_ids = await scrape_breastcancer_org_to_postgres()
print(f"Inserted {len(article_ids)} articles")
```

### 2. WebMD
- **URL**: `https://www.webmd.com/breast-cancer/news-features`
- **Tecnología**: Playwright + parsing de fechas múltiples formatos  
- **Particularidades**: Estructura de listas complejas, metadatos en spans
- **Performance**: ~45s, 31 artículos típicos

```python
# Parsing de fechas específico WebMD
formats = ["%B %d, %Y", "%b %d, %Y", "%B %d %Y", "%b %d %Y"]
```

### 3. CureToday
- **URL**: `https://www.curetoday.com/tumor/breast`
- **Tecnología**: Playwright + detección duplicados local
- **Particularidades**: Contenido dinámico, múltiples patrones de fecha
- **Performance**: ~50s, 30 artículos típicos

```python
# Detección duplicados local adicional
processed_urls: Set[str] = set()
if full_url in processed_urls:
    continue
```

### 4. News Medical
- **URL**: `https://www.news-medical.net/condition/Breast-Cancer`
- **Tecnología**: Playwright + parsing de metadatos estructurados
- **Particularidades**: Formato de fecha estándar, estructura consistente
- **Performance**: ~30s, 20 artículos típicos

```python
# Metadata específica para fuente internacional
language='en', country='International'
```

## Troubleshooting

### Errores Comunes

#### 1. ModuleNotFoundError
```bash
# Problema: Import paths incorrectos
# Solución: Ejecutar desde raíz del proyecto
cd /path/to/news_bot_3
python scripts/run_migrated_scrapers.py scraper_name
```

#### 2. Database Connection Failed
```bash
# Problema: PostgreSQL no ejecutándose
# Solución: Verificar Docker container
docker-compose ps
docker-compose up -d postgres
```

#### 3. Pool is Closed
```bash
# Problema: Conexiones múltiples no manejadas
# Solución: Ejecutar scrapers individualmente
python scripts/run_migrated_scrapers.py webmd.com
# En lugar de usar 'all'
```

#### 4. Playwright Timeout
```bash
# Problema: Sitio lento o inaccesible
# Solución: Verificar conectividad y aumentar timeout
# Código: await page.goto(URL, timeout=60000)
```

### Debug Tips

1. **HTML Structure Changes**
   ```bash
   # Usar debug para verificar estructura actual
   python tests/scrapers/debug_breastcancer_structure.py
   ```

2. **Performance Issues**
   ```bash
   # Monitorear execution time
   python test_scraper_framework.py
   # Verificar métricas en output
   ```

3. **Data Quality Issues**
   ```bash
   # Verificar integridad en PostgreSQL
   SELECT COUNT(*), COUNT(DISTINCT url) FROM articles WHERE source_id = 1;
   ```

## Mantenimiento

### Actualizaciones de Scrapers

1. **Cambios en Estructura HTML**
   - Usar debug tools para identificar nuevos selectores
   - Actualizar selectores CSS en scraper específico
   - Ejecutar tests para validar cambios

2. **Nuevos Campos**
   - Agregar campos en función de scraper
   - Actualizar query de inserción
   - Ejecutar migration si es necesario

3. **Performance Optimization**
   - Monitorear métricas de execution time
   - Optimizar selectores CSS
   - Implementar caching si es apropiado

### Extensión a Nuevos Scrapers

1. **Crear Nuevo Scraper**
   ```python
   # Copiar template desde existing scraper
   # Modificar URL, selectores, y metadata específica
   # Agregar a scripts/run_migrated_scrapers.py
   ```

2. **Implementar Test**
   ```python
   # Heredar de ScraperTestFramework
   # Implementar test_scraper_specific()
   # Agregar a test suite
   ```

3. **Documentar**
   - Agregar sección en esta guía
   - Actualizar README con nuevo scraper
   - Documentar particularidades específicas

## Métricas y Monitoreo

### KPIs de Scrapers

- **Execution Time**: <60s por scraper
- **Success Rate**: >95% artículos extraídos
- **Data Quality**: >95% campos completos
- **Uniqueness**: 100% URLs únicas

### Monitoring Queries

```sql
-- Articles por fuente
SELECT ns.name, COUNT(a.id) as articles
FROM news_sources ns
LEFT JOIN articles a ON ns.id = a.source_id
GROUP BY ns.name;

-- Calidad de datos
SELECT 
    COUNT(*) as total,
    COUNT(content_hash) / COUNT(*) * 100 as hash_completeness,
    COUNT(word_count) / COUNT(*) * 100 as wordcount_completeness
FROM articles;

-- Performance por día
SELECT DATE(scraped_at), COUNT(*) 
FROM articles 
WHERE scraped_at >= CURRENT_DATE - INTERVAL '7 days'
GROUP BY DATE(scraped_at)
ORDER BY DATE(scraped_at) DESC;
```

## Próximos Pasos

### FASE 2: NLP Analytics
Con los scrapers establecidos, el siguiente paso es implementar:
- Análisis de sentimientos con VADER + spaCy
- Categorización automática de temas médicos
- APIs FastAPI para dashboard analytics

### Scrapers Pendientes
- Medical Xpress
- Nature  
- Breast Cancer Now
- Science Daily (opcional - términos restrictivos)

### Optimizaciones
- Connection pooling para ejecución batch
- Rate limiting para respetar sitios web  
- Paralelización de scrapers
- Caching inteligente

---
*Guía creada: 2025-06-27*  
*Autor: Claude Code (Director Técnico)*  
*Revisor: Cristhian F. Moreno (Senior Engineer)*  
*Versión: 1.0 - FASE 1*