# Guía de Uso de Scripts - PreventIA News Analytics

## 📋 Resumen de Scripts Disponibles

Esta guía describe el uso de los scripts implementados para automatizar tareas comunes de instalación, validación, backup y mantenimiento del sistema PreventIA News Analytics.

### Scripts Implementados
1. **`install.sh`** - Instalación automatizada del sistema
2. **`init_data.py`** - Carga de datos de ejemplo
3. **`validate_installation.sh`** - Validación del sistema
4. **`backup_system.sh`** - Backup automatizado
5. **`validate_documentation.sh`** - Validación de documentación

---

## 🚀 Script de Instalación (install.sh)

**Propósito:** Instalar automáticamente todo el sistema PreventIA desde cero.

### Uso Básico
```bash
# Instalación estándar
./scripts/install.sh

# Ver ayuda
./scripts/install.sh --help
```

### Características
- ✅ Verifica todas las dependencias del sistema
- ✅ Valida configuración de Docker
- ✅ Construye y levanta todos los servicios
- ✅ Inicializa la base de datos con migraciones
- ✅ Crea usuario administrador
- ✅ Verifica conectividad de servicios

### Salida Esperada
```
🚀 PreventIA News Analytics - Instalación completada exitosamente!
========================================

🌐 Servicios disponibles:
   📊 Dashboard Principal: http://localhost:3000/
   🔧 Panel Admin:        http://localhost:3000/admin
   📚 API Docs:           http://localhost:8000/docs
   ❤️  API Health:         http://localhost:8000/health

👤 Usuario administrador creado:
   Email: admin@preventia.com
   Password: admin123
```

---

## 📊 Script de Datos de Ejemplo (init_data.py)

**Propósito:** Cargar datos médicos de ejemplo para demostración y testing.

### Uso Básico
```bash
# Cargar datos de ejemplo
./scripts/init_data.py

# Ejecutar desde Docker (si hay problemas de conectividad)
docker-compose exec api python /app/scripts/init_data.py
```

### Datos Cargados
- **5 Fuentes Médicas:** Instituto Nacional del Cáncer, AECC, Mayo Clinic, etc.
- **5 Artículos Ejemplo:** Con análisis NLP completo (sentimiento + tópicos)
- **Datos de Compliance:** Registros de auditoría y validación
- **Analytics:** Datos para demostrar funcionalidad del dashboard

### Verificación
```bash
# Verificar datos cargados
./preventia-cli status
# Output esperado: Articles: 5, Active Sources: 5+
```

---

## 🔍 Script de Validación (validate_installation.sh)

**Propósito:** Verificar que el sistema esté funcionando correctamente.

### Uso Básico
```bash
# Validación completa
./scripts/validate_installation.sh

# Modo silencioso
./scripts/validate_installation.sh --quiet

# Ver ayuda
./scripts/validate_installation.sh --help
```

### Verificaciones Realizadas (37 total)
1. **Dependencias del Sistema** (6 checks)
   - Docker, Docker Compose, Python, Node.js, curl

2. **Archivos de Configuración** (5 checks)
   - docker-compose.yml, .env, requirements.txt, package.json, migraciones

3. **Servicios Docker** (6 checks)
   - Estado de contenedores (postgres, api, frontend, redis, analytics)

4. **Conectividad de Red** (4 checks)
   - API (puerto 8000), Frontend (puerto 3000), PostgreSQL, Redis

5. **Base de Datos** (7 checks)
   - Conectividad, tablas principales, usuario administrador

6. **Endpoints de API** (5 checks)
   - Health check, documentación, endpoints principales

7. **Análisis de Logs** (2 checks)
   - Errores en API y PostgreSQL

8. **Rendimiento Básico** (2 checks)
   - Tiempo de respuesta, uso de memoria

### Interpretación de Resultados
- **✅ PASS:** Verificación exitosa
- **⚠️ WARNING:** Funciona pero requiere atención
- **❌ FAIL:** Problema crítico que debe resolverse

### Códigos de Salida
- `0`: Todo correcto (sin errores críticos)
- `1`: Algunos problemas menores
- `2`: Problemas críticos que requieren atención

---

## 💾 Script de Backup (backup_system.sh)

**Propósito:** Realizar backup completo del sistema.

### Uso Básico
```bash
# Backup básico
./scripts/backup_system.sh

# Backup completo con logs
./scripts/backup_system.sh --full

# Backup en directorio específico
./scripts/backup_system.sh --dir /mnt/backups

# Ver ayuda
./scripts/backup_system.sh --help
```

### Opciones Avanzadas
```bash
# Backup completo, sin compresión, retención 30 días
./scripts/backup_system.sh -f -n -r 30

# Backup silencioso para automatización
./scripts/backup_system.sh --quiet --dir /backup/auto
```

### Componentes Respaldados
1. **Base de Datos PostgreSQL** (SQL dump)
2. **Archivos de Configuración** (docker-compose, .env, etc.)
3. **Volúmenes Docker** (datos persistentes)
4. **Logs del Sistema** (solo en modo `--full`)
5. **Código Fuente** (solo en modo `--full`)

### Estructura del Backup
```
backups/
├── preventia_backup_20250729_153746_database.sql
├── preventia_backup_20250729_153746_config/
├── preventia_backup_20250729_153746_volumes/
├── preventia_backup_20250729_153746_report.txt
└── (logs y source si --full)
```

### Automatización
```bash
# Agregar a crontab para backup diario a las 2 AM
0 2 * * * /path/to/preventia/scripts/backup_system.sh -q -d /backup/daily
```

---

## 📝 Script de Validación de Documentación (validate_documentation.sh)

**Propósito:** Verificar la calidad y consistencia de la documentación.

### Uso Básico
```bash
# Validación completa
./scripts/validate_documentation.sh

# Modo silencioso con reporte
./scripts/validate_documentation.sh --quiet --output docs_report.txt

# Ver ayuda
./scripts/validate_documentation.sh --help
```

### Verificaciones Realizadas
1. **Estructura de Documentación**
   - Archivos requeridos (README, manuales 01-05)
   - Directorio de assets

2. **Enlaces Internos**
   - Links entre documentos
   - Referencias válidas

3. **Comandos Documentados**
   - Bloques de código bash
   - Comandos ejecutables

4. **Scripts Referenciados**
   - Referencias a archivos en scripts/
   - Existencia de scripts mencionados

5. **Consistencia de Versiones**
   - Versiones de Python, Node.js
   - Dependencias en package.json

6. **Ejemplos de Código**
   - Sintaxis de bloques de código
   - Balanceado de código markdown

7. **Actualización de Documentación**
   - Archivos modificados recientemente
   - Documentación obsoleta

### Corrección Automática
```bash
# Intentar corregir errores automáticamente (futura funcionalidad)
./scripts/validate_documentation.sh --fix
```

---

## 🔄 Flujos de Trabajo Recomendados

### Instalación Nueva
1. **Preparación:**
   ```bash
   git clone <repo>
   cd preventia-news-analytics
   cp .env.example .env
   # Editar .env con configuraciones específicas
   ```

2. **Instalación:**
   ```bash
   ./scripts/install.sh
   ```

3. **Datos de Ejemplo:**
   ```bash
   ./scripts/init_data.py
   ```

4. **Validación:**
   ```bash
   ./scripts/validate_installation.sh
   ```

### Mantenimiento Diario
1. **Health Check:**
   ```bash
   ./scripts/validate_installation.sh --quiet
   ```

2. **Backup (si configurado):**
   ```bash
   ./scripts/backup_system.sh --quiet
   ```

3. **Validación de Docs (semanal):**
   ```bash
   ./scripts/validate_documentation.sh
   ```

### Troubleshooting
1. **Sistema no funciona correctamente:**
   ```bash
   # Diagnóstico completo
   ./scripts/validate_installation.sh

   # Ver logs específicos
   docker-compose logs -f api
   docker-compose logs -f postgres
   ```

2. **Después de cambios importantes:**
   ```bash
   # Validar instalación
   ./scripts/validate_installation.sh

   # Backup antes de cambios
   ./scripts/backup_system.sh --full
   ```

3. **Problemas de documentación:**
   ```bash
   # Verificar consistencia
   ./scripts/validate_documentation.sh --output problems.txt
   cat problems.txt
   ```

---

## ⚙️ Variables de Entorno para Scripts

### Variables Globales
```bash
# Configuración de backup
export BACKUP_DIR="/mnt/backups"
export RETENTION_DAYS=14
export COMPRESS=true

# Configuración de validación
export VALIDATION_TIMEOUT=30
export QUIET_MODE=false
```

### Personalización por Script
Cada script respeta sus propias variables de entorno. Consulta `--help` de cada script para detalles específicos.

---

## 🚨 Solución de Problemas Comunes

### Script de Instalación
**Error:** "Docker no está ejecutándose"
```bash
# Solución
sudo systemctl start docker
sudo usermod -aG docker $USER  # Requiere logout/login
```

**Error:** "PostgreSQL no responde"
```bash
# Solución
docker-compose down
docker-compose up -d postgres
# Esperar 30 segundos y reintentar
```

### Script de Validación
**Error:** "Algunos servicios no están corriendo"
```bash
# Diagnóstico
docker-compose ps
docker-compose logs <service_name>

# Solución típica
docker-compose restart <service_name>
```

### Script de Backup
**Error:** "No se puede escribir en directorio de backup"
```bash
# Solución
sudo mkdir -p /path/to/backup
sudo chown $USER:$USER /path/to/backup
chmod 755 /path/to/backup
```

### Script de Documentación
**Error:** "Enlaces rotos encontrados"
```bash
# Verificar manualmente
find manual/ -name "*.md" -exec grep -l "broken_link" {} \;

# Corregir enlaces en los archivos identificados
```

---

## 📞 Soporte y Recursos Adicionales

- **Documentación completa:** `manual/README.md`
- **Troubleshooting detallado:** `manual/05_ResolucionProblemas.md`
- **API Reference:** `manual/07_APIReference.md`
- **CLI del sistema:** `./preventia-cli --help`

Para problemas no cubiertos en esta guía, consultar la documentación completa o ejecutar los scripts con `--help` para opciones avanzadas.
