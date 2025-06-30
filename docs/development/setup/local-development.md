# Local Development Setup - PreventIA News Analytics

---
**Document Metadata**
- **Version**: 1.0
- **Last Updated**: 2025-06-28
- **Maintainer**: Technical Team
- **Category**: Development Setup
- **Priority**: High
- **Status**: Approved
- **Language**: Spanish (Team Documentation)
---

Esta guía te ayudará a configurar el entorno de desarrollo local para el proyecto PreventIA News Analytics.

## 📋 Prerequisitos

### Software Requerido
- **Python 3.13+**: [Descargar Python](https://python.org/downloads/)
- **Docker & Docker Compose**: [Instalar Docker](https://docs.docker.com/get-docker/)
- **Git**: Para clonar el repositorio
- **Un editor de código**: VS Code recomendado

### Hardware Recomendado
- **RAM**: 8GB mínimo, 16GB recomendado
- **Disco**: 5GB libres para containers y dependencies
- **CPU**: Multi-core recomendado para scraping paralelo

## 🚀 Setup Rápido

### 1. Clonar el Repositorio
```bash
git clone <repository-url>
cd news_bot_3
```

### 2. Configurar Variables de Entorno
```bash
# Copiar template de configuración
cp .env.example .env

# Editar variables necesarias
nano .env
```

**Variables mínimas requeridas:**
```env
# Database Configuration
POSTGRES_DB=preventia_news
POSTGRES_USER=preventia
POSTGRES_PASSWORD=preventia123
DATABASE_URL=postgresql://preventia:preventia123@localhost:5433/preventia_news

# API Configuration
OPENAI_API_KEY=your_openai_api_key_here

# Analytics Configuration
DAYS_INTERVAL=3
WEEKLY_DAY=1
WEEKLY_TIME=06:00
```

### 3. Crear Entorno Virtual Python
```bash
# Crear virtual environment
python -m venv venv

# Activar virtual environment
# En Linux/Mac:
source venv/bin/activate
# En Windows:
# venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt
```

### 4. Levantar Base de Datos
```bash
# Iniciar PostgreSQL
docker compose up postgres -d

# Verificar que esté corriendo
docker compose ps

# Ver logs si hay problemas
docker compose logs postgres
```

### 5. Verificar Setup
```bash
# Activar virtual environment
source venv/bin/activate

# Ejecutar tests de base de datos
python test_database.py
```

**Output esperado:**
```
🔧 Inicializando conexión a PostgreSQL...
✅ Conexión establecida exitosamente
...
🎉 Todos los tests pasaron exitosamente!
```

## 🔧 Configuración Detallada

### PostgreSQL Database

#### Puerto y Configuración
- **Puerto local**: `5433` (para evitar conflictos con PostgreSQL local)
- **Puerto interno**: `5432` (dentro del container)
- **Database**: `preventia_news`
- **Usuario**: `preventia`
- **Password**: `preventia123`

#### Conexión Manual
```bash
# Conectar vía psql
psql -h localhost -p 5433 -U preventia -d preventia_news

# Conectar vía Docker
docker compose exec postgres psql -U preventia -d preventia_news
```

#### Reset de Base de Datos
```bash
# Parar containers
docker compose down

# Eliminar volúmenes (⚠️ BORRA TODOS LOS DATOS)
docker compose down -v

# Reiniciar limpio
docker compose up postgres -d
```

### Python Virtual Environment

#### Gestión de Dependencias
```bash
# Activar environment
source venv/bin/activate

# Instalar nueva dependencia
pip install nueva-dependencia

# Actualizar requirements.txt
pip freeze > requirements.txt

# Instalar de requirements.txt
pip install -r requirements.txt
```

#### Verificar Instalación
```bash
# Verificar versión de Python
python --version  # Debe ser 3.13+

# Verificar paquetes clave
python -c "import fastapi; print('FastAPI OK')"
python -c "import sqlalchemy; print('SQLAlchemy OK')"
python -c "import asyncpg; print('asyncpg OK')"
```

### Variables de Entorno

#### Archivo .env Completo
```env
# =============================================================================
# DATABASE CONFIGURATION
# =============================================================================
POSTGRES_DB=preventia_news
POSTGRES_USER=preventia
POSTGRES_PASSWORD=preventia123
DATABASE_URL=postgresql://preventia:preventia123@localhost:5433/preventia_news
DATABASE_ECHO=false  # Set to true for SQL query logging

# =============================================================================
# API CONFIGURATION
# =============================================================================
OPENAI_API_KEY=sk-your-openai-api-key-here
API_HOST=0.0.0.0
API_PORT=8000
API_RELOAD=true  # Hot reload for development

# =============================================================================
# ANALYTICS CONFIGURATION
# =============================================================================
DAYS_INTERVAL=3
WEEKLY_DAY=1        # Monday = 1, Sunday = 7
WEEKLY_TIME=06:00
MAX_ARTICLES_PER_RUN=100

# =============================================================================
# SCRAPING CONFIGURATION
# =============================================================================
USER_AGENT=PreventIA News Analytics Bot 1.0
REQUEST_DELAY=1.0   # Seconds between requests
MAX_RETRIES=3
TIMEOUT=30          # Request timeout in seconds

# =============================================================================
# REDIS CONFIGURATION (opcional)
# =============================================================================
REDIS_URL=redis://localhost:6379/0
REDIS_PASSWORD=
CACHE_TTL=3600      # Cache TTL in seconds

# =============================================================================
# DEVELOPMENT FLAGS
# =============================================================================
DEBUG=true
LOG_LEVEL=INFO      # DEBUG, INFO, WARNING, ERROR
ENVIRONMENT=development
```

## 🛠️ Comandos de Desarrollo

### Database Operations
```bash
# Ver tablas en la base de datos
docker compose exec postgres psql -U preventia -d preventia_news -c "\dt"

# Ejecutar query SQL
docker compose exec postgres psql -U preventia -d preventia_news -c "SELECT COUNT(*) FROM articles;"

# Backup de base de datos
docker compose exec postgres pg_dump -U preventia preventia_news > backup.sql

# Restaurar backup
cat backup.sql | docker compose exec -T postgres psql -U preventia preventia_news
```

### Testing y Debugging
```bash
# Activar virtual environment
source venv/bin/activate

# Test de conexión a base de datos
python test_database.py

# Test específico de scraping (cuando esté implementado)
python -m services.scraper.src.main

# Test de sentiment analysis (cuando esté implementado)
python -m services.analysis.sentiment.main

# Ver logs de containers
docker compose logs postgres
docker compose logs -f postgres  # Follow logs
```

### FastAPI Development (cuando esté implementado)
```bash
# Activar virtual environment
source venv/bin/activate

# Correr FastAPI en desarrollo
uvicorn services.api.main:app --reload --host 0.0.0.0 --port 8000

# API Docs automáticas en:
# http://localhost:8000/docs (local development only)
# http://localhost:8000/redoc (local development only)
```

## 📊 Verificación del Setup

### Checklist de Verificación
- [ ] Python 3.13+ instalado y funcionando
- [ ] Docker y Docker Compose funcionando
- [ ] Virtual environment creado y activado
- [ ] Dependencias de requirements.txt instaladas
- [ ] Archivo .env configurado con valores correctos
- [ ] PostgreSQL container corriendo en puerto 5433
- [ ] test_database.py ejecuta sin errores
- [ ] Puedes conectarte a PostgreSQL manualmente
- [ ] Tablas de base de datos creadas correctamente

### Tests de Conectividad
```bash
# Test 1: PostgreSQL accesible
docker compose exec postgres pg_isready -U preventia

# Test 2: Base de datos existe
docker compose exec postgres psql -U preventia -d preventia_news -c "SELECT version();"

# Test 3: Tablas creadas
docker compose exec postgres psql -U preventia -d preventia_news -c "\dt"

# Test 4: Python puede conectarse
source venv/bin/activate && python test_database.py
```

## 🐛 Troubleshooting

### Problemas Comunes

#### Error: Puerto 5432 ya en uso
```bash
# Solución: Usar puerto 5433 (ya configurado)
# O parar PostgreSQL local:
sudo systemctl stop postgresql
```

#### Error: ModuleNotFoundError
```bash
# Verificar que virtual environment esté activo
which python  # Debe mostrar path dentro de venv/

# Reinstalar dependencias
pip install -r requirements.txt
```

#### Error: Database connection failed
```bash
# Verificar que PostgreSQL esté corriendo
docker compose ps

# Verificar logs
docker compose logs postgres

# Verificar variables de entorno
echo $DATABASE_URL
```

#### Error: Permission denied en Docker
```bash
# En Linux, agregar usuario a grupo docker
sudo usermod -aG docker $USER
# Logout y login de nuevo
```

### Reset Completo
```bash
# Si todo falla, reset completo:
docker compose down -v  # ⚠️ BORRA DATOS
rm -rf venv/
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
docker compose up postgres -d
python test_database.py
```

## 📝 Próximos Pasos

Una vez completado este setup, puedes continuar con:

1. **[FastAPI Development](../guides/fastapi-development.md)** - Implementar endpoints de API
2. **[Sentiment Analysis Setup](../guides/sentiment-analysis.md)** - Configurar análisis de sentimientos
3. **[Frontend Development](../guides/react-setup.md)** - Setup del dashboard React
4. **[Adding Data Sources](../guides/adding-extractors.md)** - Agregar nuevas fuentes

## 🔧 Troubleshooting

### Common Issues

#### Database Connection Failed
**Problem**: `could not connect to server: Connection refused`
**Causes**:
- PostgreSQL container not running
- Wrong port configuration
- Firewall blocking connection

**Solutions**:
```bash
# Check if container is running
docker compose ps

# Restart PostgreSQL
docker compose restart postgres

# Check logs for errors
docker compose logs postgres

# Verify port is available
netstat -tlnp | grep 5433
```

#### Virtual Environment Issues
**Problem**: `pip: command not found` or import errors
**Causes**:
- Virtual environment not activated
- Wrong Python version
- Missing dependencies

**Solutions**:
```bash
# Activate virtual environment
source venv/bin/activate

# Verify Python version
python --version  # Should be 3.13+

# Reinstall requirements
pip install -r requirements.txt

# Check if venv is activated (should show venv in prompt)
which python
```

#### Docker Issues
**Problem**: `docker: command not found` or permission errors
**Causes**:
- Docker not installed
- User not in docker group
- Docker daemon not running

**Solutions**:
```bash
# Install Docker (Ubuntu/Debian)
sudo apt update && sudo apt install docker.io docker-compose

# Add user to docker group
sudo usermod -aG docker $USER
# Then logout and login again

# Start Docker daemon
sudo systemctl start docker
sudo systemctl enable docker
```

#### Port Already in Use
**Problem**: `port 5433 is already allocated`
**Solutions**:
```bash
# Find process using port
sudo lsof -i :5433

# Kill process if safe
sudo kill -9 <PID>

# Or change port in docker-compose.yml
# Change "5433:5432" to "5434:5432"
```

### Performance Issues

#### Slow Database Queries
**Problem**: Queries taking too long
**Solutions**:
- Check database indexes
- Analyze query execution plans
- Consider connection pooling

#### Memory Issues
**Problem**: High memory usage during development
**Solutions**:
- Reduce batch sizes in scripts
- Monitor memory with `htop` or `top`
- Restart containers if memory leaks detected

### FAQ

**Q: Which Python version should I use?**
A: Python 3.13+ is required. Check with `python --version`.

**Q: How do I reset the database?**
A: `docker compose down postgres && docker compose up postgres -d`

**Q: Can I use a different database port?**
A: Yes, change the port mapping in `docker-compose.yml` and update `DATABASE_URL` in `.env`.

**Q: Where do I put API keys?**
A: In the `.env` file, never commit them to git.

## 🔗 Referencias

- [Docker Documentation](https://docs.docker.com/)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)

---
**Última actualización**: 2025-06-28
**Versión**: 1.1
