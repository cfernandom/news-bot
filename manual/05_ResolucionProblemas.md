# 5. Resolución de Problemas

## Índice del Contenido

1. [Errores Técnicos Más Comunes](#errores-técnicos-más-comunes)
2. [Problemas de Base de Datos](#problemas-de-base-de-datos)
3. [Problemas de API y Backend](#problemas-de-api-y-backend)
4. [Problemas de Frontend](#problemas-de-frontend)
5. [Problemas de Scraping](#problemas-de-scraping)
6. [Problemas de Docker](#problemas-de-docker)
7. [Problemas de Rendimiento](#problemas-de-rendimiento)
8. [Diagnóstico Rápido](#diagnóstico-rápido)
9. [FAQ Técnico](#faq-técnico)

## Errores Técnicos Más Comunes

### Error: Database Connection Failed

**Síntomas:**
- API retorna error 500
- Logs muestran: `asyncpg.exceptions.InvalidPasswordError`
- Health check falla con "database: disconnected"

**Causas Posibles:**
1. Credenciales incorrectas en `.env`
2. PostgreSQL no está ejecutándose
3. Firewall bloqueando puerto 5432/5433

**Solución:**
```bash
# 1. Verificar que PostgreSQL esté ejecutándose
docker-compose ps postgres

# 2. Verificar credenciales
docker-compose exec postgres psql -U preventia -d preventia_news

# 3. Revisar variables de entorno
cat .env | grep POSTGRES

# 4. Reiniciar servicio
docker-compose restart postgres
docker-compose restart api

# 5. Verificar logs
docker-compose logs -f postgres
```

### Error: JWT Token Invalid

**Síntomas:**
- Error 401 Unauthorized
- Mensaje: "Invalid authentication credentials"

**Causas Posibles:**
1. Token expirado (>24 horas)
2. JWT_SECRET_KEY cambió
3. Token malformado

**Solución:**
```bash
# 1. Verificar configuración JWT
grep JWT_SECRET_KEY .env

# 2. Generar nuevo token
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=admin&password=admin123"

# 3. Verificar expiración del token
# Decodificar token en jwt.io para ver exp claim
```

### Error: CORS Policy Blocked

**Síntomas:**
- Console del navegador muestra: "CORS policy: No 'Access-Control-Allow-Origin'"
- Frontend no puede conectar con API

**Causas Posibles:**
1. URL del frontend no está en CORS origins
2. Protocolo incorrecto (http vs https)

**Solución:**
```python
# services/api/main.py
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:5173",
        "https://preventia.example.com"  # Agregar dominio de producción
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

## Problemas de Base de Datos

### Error: Migration Failed

**Síntomas:**
- Error al ejecutar migraciones
- Mensaje: "relation already exists" o "column does not exist"

**Causas Posibles:**
1. Migraciones duplicadas
2. Estado inconsistente de BD

**Solución:**
```bash
# 1. Verificar estado de migraciones
docker-compose exec postgres psql -U preventia -d preventia_news \
  -c "SELECT * FROM alembic_version;"

# 2. Resetear migraciones (CUIDADO: esto borrará datos)
docker-compose down -v
docker-compose up -d postgres
docker-compose exec api alembic upgrade head

# 3. Aplicar migraciones manualmente
docker-compose exec postgres psql -U preventia -d preventia_news \
  -f services/data/database/migrations/001_initial_schema.sql
```

### Error: Disk Space Full

**Síntomas:**
- Error: "could not extend file: No space left on device"
- Base de datos deja de aceptar escrituras

**Causas Posibles:**
1. Logs muy grandes
2. Respaldos acumulados
3. Tabla de artículos muy grande

**Solución:**
```bash
# 1. Verificar espacio
df -h
du -sh /var/lib/docker/volumes/*

# 2. Limpiar logs antiguos
docker-compose exec postgres vacuumdb -U preventia -d preventia_news -f -z

# 3. Rotar logs
find ./logs -name "*.log" -mtime +30 -delete

# 4. Limpiar Docker
docker system prune -af --volumes
```

## Problemas de API y Backend

### Error: Worker Timeout

**Síntomas:**
- Requests largos fallan después de 30-60 segundos
- Error: "Worker timeout"

**Causas Posibles:**
1. Operación toma más tiempo del timeout configurado
2. Deadlock en base de datos

**Solución:**
```bash
# 1. Aumentar timeout en producción
# Dockerfile.api
CMD ["uvicorn", "services.api.main:app", "--timeout-keep-alive", "120"]

# 2. Verificar queries lentos
docker-compose exec postgres psql -U preventia -d preventia_news \
  -c "SELECT * FROM pg_stat_activity WHERE state = 'active' AND query_start < now() - interval '1 minute';"

# 3. Agregar índices si es necesario
CREATE INDEX idx_articles_created_at ON articles(created_at DESC);
```

### Error: Memory Leak

**Síntomas:**
- Consumo de memoria aumenta constantemente
- Container se reinicia por OOM killer

**Causas Posibles:**
1. Queries retornando demasiados datos
2. Caché sin límite

**Solución:**
```python
# 1. Limitar resultados de queries
@app.get("/api/articles")
async def get_articles(limit: int = Query(100, le=1000)):
    # Máximo 1000 artículos por request

# 2. Configurar límites de memoria en Docker
services:
  api:
    deploy:
      resources:
        limits:
          memory: 4G
        reservations:
          memory: 2G
```

## Problemas de Frontend

### Error: Blank White Screen

**Síntomas:**
- Página en blanco al cargar
- Console muestra errores de JavaScript

**Causas Posibles:**
1. Error en build de producción
2. Variable VITE_API_URL incorrecta

**Solución:**
```bash
# 1. Verificar build
cd preventia-dashboard
npm run build
npm run preview

# 2. Verificar variables de entorno
grep VITE_API_URL .env

# 3. Rebuild con cache limpio
rm -rf node_modules dist
npm install
npm run build

# 4. Verificar logs del navegador
# Abrir Developer Tools > Console
```

### Error: Components Not Rendering

**Síntomas:**
- Partes de la UI no se muestran
- Errores de React en console

**Causas Posibles:**
1. Versión incompatible de React
2. Estado corrupto en localStorage

**Solución:**
```javascript
// 1. Limpiar localStorage
localStorage.clear();
sessionStorage.clear();

// 2. Verificar versiones
npm list react react-dom

// 3. Forzar re-render
window.location.reload(true);
```

## Problemas de Scraping

### Error: Scraper Blocked

**Síntomas:**
- Scraper retorna 403 Forbidden
- Mensaje: "Access denied"

**Causas Posibles:**
1. User-Agent bloqueado
2. Rate limit excedido
3. IP bloqueada

**Solución:**
```python
# 1. Actualizar User-Agent
SCRAPER_USER_AGENT = "PreventIA-Bot/1.0 (+https://preventia.edu.co/bot)"

# 2. Aumentar delay entre requests
crawl_delay_seconds = max(source.crawl_delay_seconds, 3)

# 3. Implementar retry con backoff
@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
async def fetch_article(url):
    # código de scraping
```

### Error: Content Extraction Failed

**Síntomas:**
- Artículos vacíos o con contenido incorrecto
- Selectores CSS no encuentran elementos

**Causas Posibles:**
1. Estructura del sitio cambió
2. Contenido cargado con JavaScript

**Solución:**
```bash
# 1. Verificar selectores manualmente
docker-compose exec api python
>>> from bs4 import BeautifulSoup
>>> import requests
>>> resp = requests.get("https://example.com/article")
>>> soup = BeautifulSoup(resp.content, 'html.parser')
>>> soup.select('.article-content')

# 2. Usar Playwright para sitios con JS
from playwright.async_api import async_playwright

async def scrape_with_js(url):
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        await page.goto(url)
        await page.wait_for_selector('.article-content')
        content = await page.content()
        await browser.close()
    return content
```

## Problemas de Integración NLP

### Error: "Spacy model not found"

**Síntomas:**
- Error al procesar análisis de sentimiento
- Logs muestran: `OSError: [E050] Can't find model 'es_core_news_sm'`
- Artículos quedan en estado "processing"

**Causas Posibles:**
1. Modelo Spacy no instalado en container
2. Versión incorrecta del modelo
3. Memoria insuficiente para cargar modelo

**Solución:**
```bash
# 1. Verificar modelos instalados
docker-compose exec api python -c "import spacy; print(spacy.info())"

# 2. Instalar modelo español
docker-compose exec api python -m spacy download es_core_news_sm

# 3. Verificar carga del modelo
docker-compose exec api python -c "import spacy; nlp = spacy.load('es_core_news_sm'); print('Modelo cargado correctamente')"

# 4. Reiniciar servicio API
docker-compose restart api

# 5. Verificar memoria disponible
docker stats preventia_api
```

### Error: "VADER sentiment analysis timeout"

**Síntomas:**
- Timeout en análisis de sentimiento
- Logs muestran: `asyncio.TimeoutError`
- Processing se bloquea en artículos largos

**Causas Posibles:**
1. Artículos muy largos (>10,000 palabras)
2. Timeout configurado muy bajo
3. Alta carga de CPU

**Solución:**
```bash
# 1. Verificar configuración de timeout
grep -r "SENTIMENT_TIMEOUT" services/nlp/

# 2. Ajustar timeout en variables de entorno
echo "SENTIMENT_TIMEOUT=300" >> .env

# 3. Procesar artículo específico manualmente
docker-compose exec api python -c "
from services.nlp.sentiment_analyzer import analyze_sentiment
result = analyze_sentiment('Texto de prueba...')
print(result)
"

# 4. Verificar CPU usage
docker stats --no-stream | grep preventia
```

### Error: "OpenAI API rate limit exceeded"

**Síntomas:**
- Error 429 en clasificación de tópicos
- Logs muestran: `openai.RateLimitError`
- Batch processing se detiene

**Causas Posibles:**
1. Límite de requests por minuto alcanzado
2. API key inválida o sin créditos
3. Múltiples instancias usando la misma key

**Solución:**
```bash
# 1. Verificar API key
curl -H "Authorization: Bearer $OPENAI_API_KEY" \
     -H "Content-Type: application/json" \
     https://api.openai.com/v1/models

# 2. Verificar límites actuales
grep -r "OPENAI_RATE_LIMIT" services/nlp/

# 3. Implementar backoff exponencial
# Ajustar en services/nlp/topic_classifier.py:
# time.sleep(2 ** retry_count)

# 4. Usar modelo local como fallback
echo "USE_LOCAL_CLASSIFICATION=true" >> .env
```

## Problemas de Scraping Específicos

### Error: "robots.txt validation failed"

**Síntomas:**
- Fuente rechazada en validación de compliance
- Logs muestran: `ComplianceError: robots.txt disallows scraping`
- Status de fuente cambia a "failed"

**Causas Posibles:**
1. robots.txt prohíbe scraping de la ruta
2. robots.txt no accesible (404, 500)
3. Parsing incorrecto de robots.txt

**Solución:**
```bash
# 1. Verificar robots.txt manualmente
curl -v https://example.com/robots.txt

# 2. Probar validación específica
docker-compose exec api python -c "
from services.scraper.compliance_checker import check_robots_compliance
result = check_robots_compliance('https://example.com', '/news/article')
print(result)
"

# 3. Revisar logs de compliance
docker-compose logs api | grep "robots.txt"

# 4. Ajustar crawl delay si es necesario
# En la base de datos, actualizar crawl_delay_seconds
docker-compose exec postgres psql -U preventia -d preventia_news -c "
UPDATE news_sources SET crawl_delay_seconds = 5 WHERE base_url = 'https://example.com';
"
```

### Error: "Content hash collision detected"

**Síntomas:**
- Artículos duplicados no se insertan
- Logs muestran: `IntegrityError: duplicate key value violates unique constraint`
- Hash MD5 idéntico para contenido diferente

**Causas Posibles:**
1. Contenido realmente duplicado
2. Hash collision (muy raro)
3. Normalización de contenido agresiva

**Solución:**
```bash
# 1. Verificar artículos con hash similar
docker-compose exec postgres psql -U preventia -d preventia_news -c "
SELECT title, content_hash, LEFT(content, 100) FROM articles
WHERE content_hash = 'hash_problematico';
"

# 2. Regenerar hashes si es necesario
docker-compose exec api python -c "
from services.data.content_processor import regenerate_content_hashes
regenerate_content_hashes()
"

# 3. Ajustar algoritmo de hash
# Cambiar en services/data/models.py de MD5 a SHA256
```

### Error: "Playwright browser timeout"

**Síntomas:**
- Timeout en sitios con JavaScript pesado
- Logs muestran: `playwright._impl._api_types.TimeoutError`
- Scraping falla en sitios SPA

**Causas Posibles:**
1. Sitio muy lento en cargar
2. JavaScript que nunca termina
3. Recursos bloqueados (ads, analytics)

**Solución:**
```bash
# 1. Aumentar timeout para sitios específicos
# En services/scraper/extractors/default_extractor.py:
# await page.goto(url, timeout=60000)

# 2. Bloquear recursos innecesarios
# await page.route("**/*.{png,jpg,jpeg,gif,svg,css}", lambda route: route.abort())

# 3. Usar headless más rápido
# browser = await p.chromium.launch(args=['--disable-dev-shm-usage', '--no-sandbox'])

# 4. Verificar scraping manual
docker-compose exec api python -c "
from services.scraper.automation.template_engine import generate_scraper_code
code = generate_scraper_code('https://example.com')
print(code)
"
```

## Problemas de Performance Específicos

### Error: Query lenta en dashboard analytics

**Síntomas:**
- Dashboard tarda >10 segundos en cargar
- Timeout en endpoint `/api/analytics/summary`
- Alta CPU en PostgreSQL

**Causas Posibles:**
1. Falta de índices en tablas grandes
2. Consultas N+1 en análisis
3. Sin cache de resultados

**Solución:**
```bash
# 1. Identificar queries lentas
docker-compose exec postgres psql -U preventia -d preventia_news -c "
SELECT query, mean_exec_time, calls
FROM pg_stat_statements
ORDER BY mean_exec_time DESC LIMIT 10;
"

# 2. Agregar índices faltantes
docker-compose exec postgres psql -U preventia -d preventia_news -c "
CREATE INDEX CONCURRENTLY idx_articles_published_sentiment
ON articles(published_at, sentiment_score)
WHERE processing_status = 'completed';
"

# 3. Verificar uso de cache Redis
docker-compose exec redis redis-cli INFO memory

# 4. Implementar cache en endpoint específico
# Agregar @cache decorator en services/api/routers/analytics.py
```

### Error: Memory leak en procesamiento batch

**Síntomas:**
- Memoria del container API crece constantemente
- OOM killer mata el proceso
- Procesamiento se vuelve más lento

**Causas Posibles:**
1. Objects no liberados en análisis NLP
2. Cache interno sin límite
3. Conexiones de BD no cerradas

**Solución:**
```bash
# 1. Monitorear memoria en tiempo real
docker stats preventia_api --no-stream

# 2. Usar memory profiler
docker-compose exec api python -c "
import tracemalloc
tracemalloc.start()
# ... código de procesamiento
current, peak = tracemalloc.get_traced_memory()
print(f'Current: {current / 1024 / 1024:.1f} MB, Peak: {peak / 1024 / 1024:.1f} MB')
"

# 3. Implementar garbage collection manual
# En services/nlp/batch_processor.py:
# import gc; gc.collect()

# 4. Reducir batch size
echo "NLP_BATCH_SIZE=25" >> .env
docker-compose restart api
```

### Error: Cache Redis lleno

**Síntomas:**
- Errors: `OOM command not allowed when used memory > 'maxmemory'`
- Performance degradada
- Cache hits = 0%

**Causas Posibles:**
1. Maxmemory muy bajo
2. Keys sin TTL acumulándose
3. Política de eviction incorrecta

**Solución:**
```bash
# 1. Verificar configuración de memoria
docker-compose exec redis redis-cli CONFIG GET maxmemory

# 2. Ver estadísticas de uso
docker-compose exec redis redis-cli INFO memory

# 3. Limpiar cache manualmente si es necesario
docker-compose exec redis redis-cli FLUSHDB

# 4. Ajustar política de eviction
docker-compose exec redis redis-cli CONFIG SET maxmemory-policy allkeys-lru

# 5. Aumentar memoria disponible
# En docker-compose.yml:
# redis:
#   deploy:
#     resources:
#       limits:
#         memory: 1G
```

## Problemas de Docker

### Error: Container Keeps Restarting

**Síntomas:**
- Container en loop de reinicio
- Estado: "Restarting (1) X seconds ago"

**Causas Posibles:**
1. Error en startup
2. Healthcheck fallando
3. Falta de recursos

**Solución:**
```bash
# 1. Ver logs del container
docker-compose logs --tail=100 <service_name>

# 2. Desactivar restart temporalmente
docker-compose stop <service_name>
docker-compose run --rm <service_name> bash

# 3. Verificar healthcheck
docker inspect <container_name> | grep -A 10 Healthcheck

# 4. Aumentar recursos
docker update --memory=4g --memory-swap=4g <container_name>
```

### Error: Volume Permission Denied

**Síntomas:**
- Error: "Permission denied" al escribir en volúmenes
- Logs no se crean

**Causas Posibles:**
1. UID/GID mismatch
2. SELinux o AppArmor

**Solución:**
```bash
# 1. Verificar permisos
ls -la ./logs

# 2. Cambiar propietario
sudo chown -R 1000:1000 ./logs ./exports

# 3. Para SELinux
sudo chcon -R -t container_file_t ./logs

# 4. Agregar :Z flag en docker-compose
volumes:
  - ./logs:/app/logs:Z
```

## Problemas de Rendimiento

### Queries Lentos

**Síntomas:**
- API responde lentamente
- Timeout en requests

**Diagnóstico:**
```sql
-- Queries más lentos
SELECT query, mean_exec_time, calls
FROM pg_stat_statements
ORDER BY mean_exec_time DESC
LIMIT 10;

-- Índices faltantes
SELECT schemaname, tablename, attname, n_distinct, correlation
FROM pg_stats
WHERE schemaname = 'public'
AND n_distinct > 100
AND correlation < 0.1
ORDER BY n_distinct DESC;
```

**Solución:**
```sql
-- Agregar índices necesarios
CREATE INDEX CONCURRENTLY idx_articles_published_at ON articles(published_at DESC);
CREATE INDEX CONCURRENTLY idx_articles_source_sentiment ON articles(source_id, sentiment_label);

-- Actualizar estadísticas
ANALYZE articles;
VACUUM ANALYZE news_sources;
```

### Alto Consumo de CPU

**Síntomas:**
- CPU al 100%
- Sistema lento

**Diagnóstico:**
```bash
# Top procesos por CPU
docker stats --no-stream

# Dentro del container
docker-compose exec api top

# Profiling Python
python -m cProfile -o profile.out services/api/main.py
```

**Solución:**
```python
# 1. Implementar caché
from functools import lru_cache

@lru_cache(maxsize=128)
def expensive_calculation(param):
    # cálculo costoso

# 2. Usar Redis para caché distribuido
import redis
cache = redis.Redis(host='redis', port=6379, decode_responses=True)

def get_analytics():
    cached = cache.get('analytics_summary')
    if cached:
        return json.loads(cached)

    result = calculate_analytics()
    cache.setex('analytics_summary', 3600, json.dumps(result))
    return result
```

## Diagnóstico Rápido

### Script de Diagnóstico Completo

```bash
#!/bin/bash
# diagnose.sh - Diagnóstico rápido del sistema

echo "🔍 Diagnóstico del Sistema PreventIA"
echo "===================================="

# 1. Estado de servicios
echo -e "\n📊 Estado de Servicios:"
docker-compose ps

# 2. Uso de recursos
echo -e "\n💻 Uso de Recursos:"
docker stats --no-stream --format "table {{.Container}}\t{{.CPUPerc}}\t{{.MemUsage}}"

# 3. Espacio en disco
echo -e "\n💾 Espacio en Disco:"
df -h | grep -E "(Filesystem|docker|/dev/)"

# 4. Conectividad
echo -e "\n🌐 Pruebas de Conectividad:"
curl -s -o /dev/null -w "API Health: %{http_code}\n" http://localhost:8000/health
curl -s -o /dev/null -w "Frontend: %{http_code}\n" http://localhost:3000

# 5. Últimos errores
echo -e "\n❌ Últimos Errores (API):"
docker-compose logs --tail=20 api | grep -E "(ERROR|CRITICAL|Exception)"

# 6. Base de datos
echo -e "\n🗄️ Estado Base de Datos:"
docker-compose exec -T postgres psql -U preventia -d preventia_news -c \
  "SELECT COUNT(*) as articles,
          COUNT(DISTINCT source_id) as sources,
          MIN(created_at) as oldest,
          MAX(created_at) as newest
   FROM articles;"

# 7. Redis
echo -e "\n📦 Estado Redis:"
docker-compose exec -T redis redis-cli INFO keyspace

echo -e "\n✅ Diagnóstico completado"
```

### Comandos de Diagnóstico Útiles

```bash
# Logs en tiempo real con filtro
docker-compose logs -f api | grep -E "(ERROR|WARNING)"

# Conexiones de red activas
docker-compose exec api netstat -an | grep ESTABLISHED

# Procesos zombie
docker-compose exec api ps aux | grep defunct

# Memoria detallada
docker-compose exec api cat /proc/meminfo

# IO Stats
docker-compose exec api iostat -x 1

# Verificar certificados SSL
openssl s_client -connect preventia.example.com:443 -servername preventia.example.com
```

## FAQ Técnico

### ¿Cómo resetear la contraseña de admin?

```python
# reset_admin_password.py
import asyncio
from services.data.database.connection import DatabaseManager
from services.api.auth.utils import get_password_hash

async def reset_password():
    db = DatabaseManager()
    await db.initialize()

    new_password = "nuevaPassword123!"
    hashed = get_password_hash(new_password)

    await db.execute_sql(
        "UPDATE users SET hashed_password = :password WHERE username = 'admin'",
        {"password": hashed}
    )
    print(f"✅ Password actualizado a: {new_password}")

    await db.close()

asyncio.run(reset_password())
```

### ¿Cómo migrar a un nuevo servidor?

1. Respaldar datos del servidor actual:
```bash
./scripts/backup.sh
```

2. Copiar archivos al nuevo servidor:
```bash
rsync -avz --progress /backups/ user@nuevo-servidor:/backups/
rsync -avz --progress /opt/preventia/ user@nuevo-servidor:/opt/preventia/
```

3. Restaurar en nuevo servidor:
```bash
./scripts/restore.sh /backups/db/ultimo_respaldo.dump
```

### ¿Cómo monitorear el uso de API keys?

```sql
-- Crear vista para monitoreo
CREATE VIEW api_usage_stats AS
SELECT
    DATE(created_at) as date,
    endpoint,
    COUNT(*) as requests,
    AVG(response_time_ms) as avg_response_time,
    MAX(response_time_ms) as max_response_time
FROM api_logs
GROUP BY DATE(created_at), endpoint
ORDER BY date DESC, requests DESC;

-- Consultar uso
SELECT * FROM api_usage_stats WHERE date >= CURRENT_DATE - INTERVAL '7 days';
```

### ¿Cómo debuggear problemas de memoria?

```python
# memory_debug.py
import tracemalloc
import asyncio
from services.api.main import app

tracemalloc.start()

# Ejecutar operación sospechosa
async def test_endpoint():
    # código a probar
    pass

asyncio.run(test_endpoint())

# Obtener estadísticas
current, peak = tracemalloc.get_traced_memory()
print(f"Current memory usage: {current / 10**6:.1f} MB")
print(f"Peak memory usage: {peak / 10**6:.1f} MB")

# Top 10 líneas que consumen memoria
snapshot = tracemalloc.take_snapshot()
top_stats = snapshot.statistics('lineno')
for stat in top_stats[:10]:
    print(stat)
```

### ¿Cómo optimizar las imágenes Docker?

```dockerfile
# Dockerfile.api optimizado
# Build stage
FROM python:3.13-slim as builder
WORKDIR /build
COPY requirements.txt .
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /wheels -r requirements.txt

# Runtime stage
FROM python:3.13-slim
WORKDIR /app

# Instalar solo dependencias runtime
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq5 \
    && rm -rf /var/lib/apt/lists/*

# Copiar wheels pre-construidos
COPY --from=builder /wheels /wheels
RUN pip install --no-cache /wheels/*

# Copiar código
COPY . .

# Usuario no-root
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

CMD ["uvicorn", "services.api.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

---

## Contacto de Soporte

Para problemas no resueltos en esta guía:

- **Email**: soporte@preventia.edu.co
- **Issues**: https://github.com/preventia/news_bot_3/issues
- **Documentación**: https://docs.preventia.edu.co

---

*[Volver al índice principal](README.md)*
