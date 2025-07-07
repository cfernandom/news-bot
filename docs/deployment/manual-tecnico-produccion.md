# Manual Técnico de Despliegue a Producción
## PreventIA News Analytics Platform

**Versión:** 2.0
**Fecha:** Enero 2025
**Estado:** Production Ready

---

## 📋 Tabla de Contenidos

1. [Resumen Ejecutivo](#resumen-ejecutivo)
2. [Arquitectura del Sistema](#arquitectura-del-sistema)
3. [Requisitos de Infraestructura](#requisitos-de-infraestructura)
4. [Preparación del Entorno](#preparación-del-entorno)
5. [Configuración de Seguridad](#configuración-de-seguridad)
6. [Despliegue Paso a Paso](#despliegue-paso-a-paso)
7. [Verificación y Testing](#verificación-y-testing)
8. [Monitoreo y Mantenimiento](#monitoreo-y-mantenimiento)
9. [Backup y Recuperación](#backup-y-recuperación)
10. [Troubleshooting](#troubleshooting)
11. [Optimización de Rendimiento](#optimización-de-rendimiento)

---

## 🎯 Resumen Ejecutivo

### Arquitectura del Sistema
PreventIA News Analytics es una plataforma de análisis de medios especializada en noticias de cáncer de mama que utiliza:

- **Backend:** FastAPI + PostgreSQL + Redis
- **Frontend:** React 19 + TypeScript + Tailwind CSS
- **Containerización:** Docker + Docker Compose
- **Proxy Reverso:** Nginx con SSL/TLS
- **Monitoreo:** Prometheus + Grafana
- **NLP:** VADER + spaCy para análisis de sentimientos

### Especificaciones de Rendimiento
- **Tiempo de respuesta API:** < 5 segundos (objetivo de producción)
- **Capacidad:** 106+ artículos procesados con análisis completo
- **Disponibilidad:** 99.9% uptime objetivo
- **Seguridad:** HTTPS, rate limiting, headers de seguridad

---

## 🏗️ Arquitectura del Sistema

### Diagrama de Componentes

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Load Balancer │────│   Nginx Proxy   │────│   SSL/TLS Term. │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                │
                ┌───────────────┼───────────────┐
                │               │               │
        ┌───────▼──────┐ ┌──────▼──────┐ ┌─────▼─────┐
        │   Frontend   │ │  FastAPI    │ │ Monitoring│
        │  (React 19)  │ │   Backend   │ │(Prom/Graf)│
        └──────────────┘ └──────┬──────┘ └───────────┘
                                │
                ┌───────────────┼───────────────┐
                │               │               │
        ┌───────▼──────┐ ┌──────▼──────┐ ┌─────▼─────┐
        │ PostgreSQL   │ │    Redis    │ │  Scrapers │
        │   Database   │ │    Cache    │ │ Analytics │
        └──────────────┘ └─────────────┘ └───────────┘
```

### Stack Tecnológico

| Componente | Tecnología | Versión | Puerto | Función |
|------------|------------|---------|--------|---------|
| **Frontend** | React + TypeScript | 19.1.0 | 80/443 | Dashboard de Analytics |
| **API Backend** | FastAPI + Python | 0.115+ | 8000 | REST API + NLP Processing |
| **Base de Datos** | PostgreSQL | 16+ | 5432 | Almacenamiento principal |
| **Cache** | Redis | 8-alpine | 6379 | Cache y sesiones |
| **Proxy** | Nginx | 1.27-alpine | 80/443 | Load balancer + SSL |
| **Monitoreo** | Prometheus + Grafana | Latest | 9090/3000 | Métricas y alertas |

---

## 💻 Requisitos de Infraestructura

### Servidor de Producción

#### Especificaciones Mínimas
- **CPU:** 4 cores (Intel/AMD)
- **RAM:** 8 GB
- **Almacenamiento:** 100 GB SSD
- **Red:** 1 Gbps
- **OS:** Ubuntu 22.04 LTS / CentOS 8+ / RHEL 8+

#### Especificaciones Recomendadas
- **CPU:** 8 cores (Intel/AMD)
- **RAM:** 16 GB
- **Almacenamiento:** 500 GB SSD (NVMe preferido)
- **Red:** 10 Gbps
- **OS:** Ubuntu 22.04 LTS

### Software Base Requerido

```bash
# Docker Engine
docker --version  # >= 24.0
docker-compose --version  # >= 2.0

# SSL/TLS
openssl version  # >= 1.1.1

# Herramientas de sistema
curl --version
wget --version
git --version
```

### Puertos de Red

| Puerto | Protocolo | Servicio | Acceso |
|--------|-----------|----------|---------|
| 80 | HTTP | Nginx (redirect) | Público |
| 443 | HTTPS | Nginx + App | Público |
| 8000 | HTTP | FastAPI | Interno |
| 5432 | TCP | PostgreSQL | Interno |
| 6379 | TCP | Redis | Interno |
| 9090 | HTTP | Prometheus | Administrativo |
| 3000 | HTTP | Grafana | Administrativo |

---

## 🛠️ Preparación del Entorno

### 1. Configuración del Servidor

#### Actualización del Sistema
```bash
# Ubuntu/Debian
sudo apt update && sudo apt upgrade -y
sudo apt install curl wget git htop nano -y

# CentOS/RHEL
sudo yum update -y
sudo yum install curl wget git htop nano -y
```

#### Instalación de Docker
```bash
# Instalar Docker Engine
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Instalar Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Configurar usuario
sudo usermod -aG docker $USER
newgrp docker

# Verificar instalación
docker --version
docker-compose --version
```

### 2. Preparación de Directorios

```bash
# Crear estructura de directorios
sudo mkdir -p /opt/preventia/{logs,backups,ssl,config,data}
sudo chown -R $USER:$USER /opt/preventia

# Crear directorios de datos
mkdir -p /opt/preventia/data/{postgres,redis,grafana,prometheus}
```

### 3. Clonación del Repositorio

```bash
cd /opt/preventia
git clone <repository-url> preventia-app
cd preventia-app

# Verificar rama de producción
git checkout main
git pull origin main
```

---

## 🔒 Configuración de Seguridad

### 1. Certificados SSL/TLS

#### Opción A: Let's Encrypt (Recomendado)
```bash
# Instalar Certbot
sudo apt install certbot python3-certbot-nginx -y

# Generar certificados
sudo certbot certonly --standalone -d yourdomain.com -d www.yourdomain.com

# Copiar certificados
sudo cp /etc/letsencrypt/live/yourdomain.com/fullchain.pem /opt/preventia/ssl/cert.pem
sudo cp /etc/letsencrypt/live/yourdomain.com/privkey.pem /opt/preventia/ssl/key.pem
sudo chown $USER:$USER /opt/preventia/ssl/*.pem
```

#### Opción B: Certificados Autofirmados (Desarrollo)
```bash
cd /opt/preventia/ssl
openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
  -keyout key.pem -out cert.pem \
  -subj "/C=CO/ST=Cundinamarca/L=Bogota/O=UCOMPENSAR/CN=yourdomain.com"
```

### 2. Configuración de Firewall

```bash
# UFW (Ubuntu)
sudo ufw enable
sudo ufw allow 22/tcp    # SSH
sudo ufw allow 80/tcp    # HTTP
sudo ufw allow 443/tcp   # HTTPS
sudo ufw status

# Firewalld (CentOS/RHEL)
sudo firewall-cmd --permanent --add-service=http
sudo firewall-cmd --permanent --add-service=https
sudo firewall-cmd --permanent --add-service=ssh
sudo firewall-cmd --reload
```

### 3. Variables de Entorno de Producción

```bash
# Copiar plantilla de configuración
cp .env.production.template .env.production

# Editar configuración (CRÍTICO - cambiar todos los valores por defecto)
nano .env.production
```

#### Valores Críticos a Cambiar:
```bash
# Base de datos
POSTGRES_PASSWORD=YOUR_SECURE_DB_PASSWORD_HERE
DATABASE_URL=postgresql://preventia:YOUR_SECURE_DB_PASSWORD_HERE@postgres:5432/preventia_news

# Seguridad
SECRET_KEY=YOUR_32_CHAR_SECRET_KEY_HERE
JWT_SECRET_KEY=YOUR_JWT_SECRET_KEY_HERE
ENCRYPTION_KEY=YOUR_32_BYTE_ENCRYPTION_KEY_HERE

# OpenAI
OPENAI_API_KEY=sk-YOUR_ACTUAL_OPENAI_API_KEY

# Dominio
DOMAIN_NAME=yourdomain.com
CORS_ORIGINS=["https://yourdomain.com","https://www.yourdomain.com"]

# Monitoreo
GRAFANA_PASSWORD=YOUR_GRAFANA_PASSWORD
SMTP_PASSWORD=YOUR_SMTP_PASSWORD

# AWS (si se usa backup en S3)
AWS_ACCESS_KEY_ID=YOUR_AWS_ACCESS_KEY
AWS_SECRET_ACCESS_KEY=YOUR_AWS_SECRET_ACCESS_KEY
```

---

## 🚀 Despliegue Paso a Paso

### Fase 1: Verificación Pre-Despliegue

```bash
cd /opt/preventia/preventia-app

# 1. Verificar configuración
./scripts/run_production_tests.sh

# 2. Optimizar base de datos
python scripts/optimize_database.py --health

# 3. Validar Docker builds
docker-compose -f docker-compose.prod.yml config
```

### Fase 2: Despliegue de Base de Datos

```bash
# 1. Iniciar solo PostgreSQL
docker-compose -f docker-compose.prod.yml up postgres -d

# 2. Esperar que esté listo
docker-compose -f docker-compose.prod.yml logs postgres

# 3. Verificar conectividad
docker-compose -f docker-compose.prod.yml exec postgres pg_isready -U preventia

# 4. Crear esquema inicial (si es necesario)
docker-compose -f docker-compose.prod.yml exec postgres psql -U preventia -d preventia_news -f /docker-entrypoint-initdb.d/001_initial_schema.sql
```

### Fase 3: Despliegue de Cache y Backend

```bash
# 1. Iniciar Redis
docker-compose -f docker-compose.prod.yml up redis -d

# 2. Verificar Redis
docker-compose -f docker-compose.prod.yml exec redis redis-cli ping

# 3. Construir y desplegar API
docker-compose -f docker-compose.prod.yml up api -d

# 4. Verificar API health
curl -f http://localhost:8000/health
```

### Fase 4: Despliegue de Frontend

```bash
# 1. Construir frontend
cd preventia-dashboard
npm ci --production
npm run build

# 2. Desplegar frontend
cd /opt/preventia/preventia-app
docker-compose -f docker-compose.prod.yml up frontend -d

# 3. Verificar frontend
curl -f http://localhost:3000
```

### Fase 5: Configuración de Proxy y SSL

```bash
# 1. Configurar Nginx
cp config/nginx.prod.conf /opt/preventia/config/

# 2. Actualizar configuración con dominio real
sed -i 's/yourdomain.com/ACTUAL_DOMAIN.com/g' /opt/preventia/config/nginx.prod.conf

# 3. Desplegar Nginx
docker-compose -f docker-compose.prod.yml up nginx -d

# 4. Verificar SSL
curl -I https://yourdomain.com
```

### Fase 6: Monitoreo y Métricas

```bash
# 1. Desplegar servicios de monitoreo
docker-compose -f docker-compose.prod.yml --profile monitoring up -d

# 2. Verificar Prometheus
curl -f http://localhost:9090/-/healthy

# 3. Verificar Grafana
curl -f http://localhost:3000/api/health

# 4. Configurar dashboards iniciales
# (Acceder a http://localhost:3000, admin/GRAFANA_PASSWORD)
```

### Comando de Despliegue Completo

```bash
# Despliegue completo en un comando
docker-compose -f docker-compose.prod.yml --profile monitoring up -d

# Verificar todos los servicios
docker-compose -f docker-compose.prod.yml ps
```

---

## ✅ Verificación y Testing

### 1. Tests Automatizados de Producción

```bash
# Ejecutar suite completa de tests
./scripts/run_production_tests.sh

# Resultado esperado:
# 🎉 ALL TESTS PASSED! System is ready for production.
```

### 2. Verificación Manual de Servicios

#### Health Checks
```bash
# API Backend
curl -f https://yourdomain.com/health
# Respuesta: {"status":"healthy","timestamp":"...","version":"...","services":{...}}

# Frontend
curl -I https://yourdomain.com
# Respuesta: HTTP/2 200

# Base de datos
docker-compose -f docker-compose.prod.yml exec postgres pg_isready -U preventia
# Respuesta: postgres:5432 - accepting connections

# Redis
docker-compose -f docker-compose.prod.yml exec redis redis-cli ping
# Respuesta: PONG
```

#### Endpoints Críticos
```bash
# API endpoints
curl -f https://yourdomain.com/api/v1/articles/
curl -f https://yourdomain.com/api/v1/analytics/sentiment
curl -f https://yourdomain.com/api/v1/analytics/topics
curl -f https://yourdomain.com/docs

# Métricas
curl -f https://yourdomain.com:9090/metrics
curl -f https://yourdomain.com:3000/api/health
```

### 3. Testing de Rendimiento

```bash
# Test de carga básico con Apache Bench
ab -n 100 -c 10 https://yourdomain.com/api/v1/articles/

# Test de rendimiento de base de datos
python scripts/optimize_database.py --optimize

# Resultado esperado: Total query time < 10s
```

### 4. Testing de Seguridad

```bash
# Verificar headers de seguridad
curl -I https://yourdomain.com | grep -E "(X-Frame-Options|X-Content-Type-Options|Strict-Transport-Security)"

# Test SSL
openssl s_client -connect yourdomain.com:443 -servername yourdomain.com

# Verificar rate limiting
for i in {1..20}; do curl -w "%{http_code}\n" -o /dev/null -s https://yourdomain.com/api/v1/articles/; done
```

---

## 📊 Monitoreo y Mantenimiento

### 1. Dashboards de Monitoreo

#### Acceso a Grafana
- **URL:** https://yourdomain.com:3000
- **Usuario:** admin
- **Contraseña:** [GRAFANA_PASSWORD del .env.production]

#### Métricas Clave a Monitorear

| Métrica | Umbral Crítico | Descripción |
|---------|----------------|-------------|
| **API Response Time** | > 5 segundos | Tiempo de respuesta de endpoints |
| **Database Connections** | > 80% max | Conexiones activas PostgreSQL |
| **Memory Usage** | > 85% | Uso de memoria del sistema |
| **CPU Usage** | > 80% | Uso de CPU promedio |
| **Disk Space** | > 90% | Espacio en disco usado |
| **Error Rate** | > 5% | Tasa de errores HTTP 5xx |

### 2. Logs del Sistema

#### Ubicación de Logs
```bash
# Logs de aplicación
tail -f /opt/preventia/logs/access.log
tail -f /opt/preventia/logs/error.log
tail -f /opt/preventia/logs/application.log

# Logs de Docker
docker-compose -f docker-compose.prod.yml logs -f api
docker-compose -f docker-compose.prod.yml logs -f postgres
docker-compose -f docker-compose.prod.yml logs -f nginx
```

#### Rotación de Logs
```bash
# Configurar logrotate
sudo nano /etc/logrotate.d/preventia

# Contenido:
/opt/preventia/logs/*.log {
    daily
    rotate 30
    compress
    delaycompress
    missingok
    notifempty
    create 644 preventia preventia
}
```

### 3. Alertas Automatizadas

#### Configuración de Alertas (Grafana)
1. **High Response Time:** > 5 segundos por 2 minutos
2. **Database Error:** Conexiones fallidas > 5%
3. **Memory Alert:** Uso > 85% por 5 minutos
4. **Disk Space:** > 90% usado
5. **Service Down:** Health check fallido por 1 minuto

#### Notificaciones
- **Email:** Configure SMTP en Grafana
- **Slack:** Webhook integration disponible
- **PagerDuty:** Para alertas críticas 24/7

### 4. Tareas de Mantenimiento

#### Diarias
```bash
# Script de mantenimiento diario
#!/bin/bash
# /opt/preventia/scripts/daily_maintenance.sh

# Verificar servicios
docker-compose -f docker-compose.prod.yml ps

# Limpiar logs antiguos
find /opt/preventia/logs -name "*.log" -mtime +30 -delete

# Backup de base de datos
docker-compose -f docker-compose.prod.yml exec postgres pg_dump -U preventia preventia_news > /opt/preventia/backups/db_$(date +%Y%m%d).sql

# Verificar espacio en disco
df -h | grep -E "(80%|90%|100%)"
```

#### Semanales
```bash
# Script de mantenimiento semanal
#!/bin/bash
# /opt/preventia/scripts/weekly_maintenance.sh

# Optimizar base de datos
python scripts/optimize_database.py --all

# Limpiar imágenes Docker no utilizadas
docker system prune -af

# Verificar certificados SSL
openssl x509 -in /opt/preventia/ssl/cert.pem -text -noout | grep "Not After"

# Actualizar estadísticas de base de datos
docker-compose -f docker-compose.prod.yml exec postgres psql -U preventia -d preventia_news -c "VACUUM ANALYZE;"
```

#### Mensuales
```bash
# Script de mantenimiento mensual
#!/bin/bash
# /opt/preventia/scripts/monthly_maintenance.sh

# Backup completo del sistema
tar -czf /opt/preventia/backups/full_backup_$(date +%Y%m%d).tar.gz /opt/preventia

# Revisar y limpiar backups antiguos
find /opt/preventia/backups -name "*.sql" -mtime +90 -delete
find /opt/preventia/backups -name "*.tar.gz" -mtime +180 -delete

# Verificar actualizaciones de seguridad
sudo apt list --upgradable | grep -i security

# Renovar certificados SSL (si usa Let's Encrypt)
sudo certbot renew --quiet
```

---

## 💾 Backup y Recuperación

### 1. Estrategia de Backup

#### Tipos de Backup
- **Incremental:** Diario (datos modificados)
- **Completo:** Semanal (sistema completo)
- **Archival:** Mensual (almacenamiento a largo plazo)

#### Retención
- **Diarios:** 30 días
- **Semanales:** 12 semanas
- **Mensuales:** 12 meses
- **Anuales:** 5 años

### 2. Scripts de Backup

#### Backup de Base de Datos
```bash
#!/bin/bash
# /opt/preventia/scripts/backup_database.sh

DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="/opt/preventia/backups"
DB_NAME="preventia_news"

# Backup completo
docker-compose -f docker-compose.prod.yml exec postgres pg_dump -U preventia -Fc $DB_NAME > $BACKUP_DIR/db_full_$DATE.dump

# Backup solo esquema
docker-compose -f docker-compose.prod.yml exec postgres pg_dump -U preventia -s $DB_NAME > $BACKUP_DIR/db_schema_$DATE.sql

# Backup solo datos
docker-compose -f docker-compose.prod.yml exec postgres pg_dump -U preventia -a $DB_NAME > $BACKUP_DIR/db_data_$DATE.sql

# Comprimir backups antiguos
find $BACKUP_DIR -name "*.dump" -mtime +7 -exec gzip {} \;

echo "Backup completed: $DATE"
```

#### Backup Completo del Sistema
```bash
#!/bin/bash
# /opt/preventia/scripts/backup_system.sh

DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="/opt/preventia/backups"

# Crear backup completo excluyendo logs y caches
tar -czf $BACKUP_DIR/system_backup_$DATE.tar.gz \
  --exclude='/opt/preventia/logs/*' \
  --exclude='/opt/preventia/data/redis/*' \
  /opt/preventia

# Verificar integridad
tar -tzf $BACKUP_DIR/system_backup_$DATE.tar.gz > /dev/null

if [ $? -eq 0 ]; then
    echo "System backup completed successfully: $DATE"
else
    echo "System backup failed: $DATE"
    exit 1
fi
```

### 3. Procedimientos de Recuperación

#### Recuperación de Base de Datos
```bash
# 1. Detener servicios que usan la BD
docker-compose -f docker-compose.prod.yml stop api analytics_service

# 2. Crear backup de seguridad de la BD actual
docker-compose -f docker-compose.prod.yml exec postgres pg_dump -U preventia -Fc preventia_news > /tmp/current_db_backup.dump

# 3. Restaurar desde backup
docker-compose -f docker-compose.prod.yml exec postgres pg_restore -U preventia -d preventia_news --clean --if-exists /backups/db_full_YYYYMMDD.dump

# 4. Verificar restauración
docker-compose -f docker-compose.prod.yml exec postgres psql -U preventia -d preventia_news -c "SELECT COUNT(*) FROM articles;"

# 5. Reiniciar servicios
docker-compose -f docker-compose.prod.yml start api analytics_service
```

#### Recuperación Completa del Sistema
```bash
# 1. Detener todos los servicios
docker-compose -f docker-compose.prod.yml down

# 2. Restaurar archivos del sistema
cd /opt
sudo rm -rf preventia_old
sudo mv preventia preventia_old
sudo tar -xzf preventia/backups/system_backup_YYYYMMDD.tar.gz

# 3. Restaurar permisos
sudo chown -R $USER:$USER /opt/preventia

# 4. Reiniciar servicios
cd /opt/preventia/preventia-app
docker-compose -f docker-compose.prod.yml up -d

# 5. Verificar funcionamiento
./scripts/run_production_tests.sh
```

### 4. Backup en Cloud (AWS S3)

```bash
# Configurar AWS CLI
aws configure

# Script de backup a S3
#!/bin/bash
# /opt/preventia/scripts/backup_to_s3.sh

BUCKET="preventia-backups"
DATE=$(date +%Y%m%d)

# Sincronizar backups locales a S3
aws s3 sync /opt/preventia/backups s3://$BUCKET/daily/$DATE/

# Verificar sincronización
aws s3 ls s3://$BUCKET/daily/$DATE/

echo "S3 backup completed: $DATE"
```

---

## 🔧 Troubleshooting

### 1. Problemas Comunes y Soluciones

#### Servicio No Responde
```bash
# 1. Verificar estado de contenedores
docker-compose -f docker-compose.prod.yml ps

# 2. Revisar logs
docker-compose -f docker-compose.prod.yml logs api

# 3. Reiniciar servicio específico
docker-compose -f docker-compose.prod.yml restart api

# 4. Verificar recursos del sistema
htop
df -h
free -h
```

#### Error de Conexión a Base de Datos
```bash
# 1. Verificar PostgreSQL está corriendo
docker-compose -f docker-compose.prod.yml exec postgres pg_isready -U preventia

# 2. Verificar configuración de conexión
grep DATABASE_URL .env.production

# 3. Verificar logs de PostgreSQL
docker-compose -f docker-compose.prod.yml logs postgres

# 4. Reiniciar PostgreSQL
docker-compose -f docker-compose.prod.yml restart postgres
```

#### Alto Uso de CPU/Memoria
```bash
# 1. Identificar proceso problemático
htop
docker stats

# 2. Verificar queries lentas en BD
docker-compose -f docker-compose.prod.yml exec postgres psql -U preventia -d preventia_news -c "
SELECT query, mean_exec_time, calls
FROM pg_stat_statements
ORDER BY mean_exec_time DESC
LIMIT 10;"

# 3. Optimizar base de datos
python scripts/optimize_database.py --optimize

# 4. Escalar recursos si es necesario
```

#### Certificados SSL Expirados
```bash
# 1. Verificar fecha de expiración
openssl x509 -in /opt/preventia/ssl/cert.pem -text -noout | grep "Not After"

# 2. Renovar certificados Let's Encrypt
sudo certbot renew

# 3. Copiar nuevos certificados
sudo cp /etc/letsencrypt/live/yourdomain.com/fullchain.pem /opt/preventia/ssl/cert.pem
sudo cp /etc/letsencrypt/live/yourdomain.com/privkey.pem /opt/preventia/ssl/key.pem

# 4. Reiniciar Nginx
docker-compose -f docker-compose.prod.yml restart nginx
```

### 2. Comandos de Diagnóstico

#### Verificación Completa del Sistema
```bash
#!/bin/bash
# /opt/preventia/scripts/system_diagnostic.sh

echo "=== PreventIA System Diagnostic ==="
echo "Date: $(date)"
echo ""

echo "1. Docker Services Status:"
docker-compose -f docker-compose.prod.yml ps
echo ""

echo "2. System Resources:"
echo "CPU Usage: $(top -bn1 | grep "Cpu(s)" | awk '{print $2}' | cut -d'%' -f1)%"
echo "Memory Usage: $(free | grep Mem | awk '{printf("%.1f%%\n", ($3/$2) * 100.0)}')"
echo "Disk Usage: $(df -h / | awk 'NR==2{printf "%s\n", $5}')"
echo ""

echo "3. Network Connectivity:"
curl -s -o /dev/null -w "API Health: %{http_code}\n" https://yourdomain.com/health
curl -s -o /dev/null -w "Frontend: %{http_code}\n" https://yourdomain.com/
echo ""

echo "4. Database Status:"
docker-compose -f docker-compose.prod.yml exec postgres pg_isready -U preventia
echo ""

echo "5. Recent Errors (last 10):"
tail -n 10 /opt/preventia/logs/error.log
echo ""

echo "=== Diagnostic Complete ==="
```

#### Logs Centralizados
```bash
# Ver todos los logs en tiempo real
docker-compose -f docker-compose.prod.yml logs -f

# Filtrar por servicio
docker-compose -f docker-compose.prod.yml logs -f api | grep ERROR

# Buscar errores específicos
grep -r "ERROR" /opt/preventia/logs/ | tail -20
```

### 3. Procedimientos de Emergencia

#### Rollback Rápido
```bash
#!/bin/bash
# /opt/preventia/scripts/emergency_rollback.sh

echo "⚠️  EMERGENCY ROLLBACK INITIATED"

# 1. Detener servicios actuales
docker-compose -f docker-compose.prod.yml down

# 2. Restaurar backup más reciente
LATEST_BACKUP=$(ls -t /opt/preventia/backups/system_backup_*.tar.gz | head -1)
echo "Restoring from: $LATEST_BACKUP"

# 3. Crear respaldo del estado actual
mv /opt/preventia /opt/preventia_failed_$(date +%Y%m%d_%H%M%S)

# 4. Restaurar desde backup
cd /opt
tar -xzf $LATEST_BACKUP

# 5. Reiniciar servicios
cd /opt/preventia/preventia-app
docker-compose -f docker-compose.prod.yml up -d

# 6. Verificar servicios
sleep 30
curl -f https://yourdomain.com/health

echo "✅ Rollback completed"
```

#### Modo de Mantenimiento
```bash
# Activar modo mantenimiento
docker-compose -f docker-compose.prod.yml stop frontend api

# Configurar página de mantenimiento en Nginx
echo "<h1>Sistema en Mantenimiento</h1><p>Volveremos pronto...</p>" > /opt/preventia/maintenance.html

# Configurar Nginx para mostrar página de mantenimiento
# (Editar nginx.conf para servir maintenance.html)

# Desactivar modo mantenimiento
docker-compose -f docker-compose.prod.yml start frontend api
```

---

## ⚡ Optimización de Rendimiento

### 1. Optimización de Base de Datos

#### Índices Críticos
```sql
-- Ejecutar en PostgreSQL para optimización
-- Índices para analytics
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_articles_published_at ON articles(published_at DESC);
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_articles_sentiment_label ON articles(sentiment_label);
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_articles_topic_category ON articles(topic_category);
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_articles_processing_status ON articles(processing_status);

-- Índice compuesto para analytics
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_articles_composite_analytics
ON articles(processing_status, published_at DESC, sentiment_label, topic_category);

-- Índice de texto completo para búsquedas
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_articles_fulltext
ON articles USING gin(to_tsvector('english', title || ' ' || content || ' ' || summary));
```

#### Configuración PostgreSQL
```bash
# Editar postgresql.conf
docker-compose -f docker-compose.prod.yml exec postgres psql -U preventia -c "
ALTER SYSTEM SET shared_buffers = '256MB';
ALTER SYSTEM SET effective_cache_size = '1GB';
ALTER SYSTEM SET maintenance_work_mem = '64MB';
ALTER SYSTEM SET checkpoint_completion_target = 0.9;
ALTER SYSTEM SET wal_buffers = '16MB';
ALTER SYSTEM SET default_statistics_target = 100;
SELECT pg_reload_conf();
"
```

### 2. Optimización de Redis

#### Configuración Optimizada
```redis
# /opt/preventia/config/redis.conf
maxmemory 256mb
maxmemory-policy allkeys-lru
save 900 1
save 300 10
save 60 10000
tcp-keepalive 60
timeout 300
```

### 3. Optimización de Nginx

#### Configuración de Cache
```nginx
# Agregar a nginx.conf
location ~* \.(jpg|jpeg|png|gif|ico|css|js)$ {
    expires 1y;
    add_header Cache-Control "public, immutable";
}

location /api/ {
    proxy_cache api_cache;
    proxy_cache_valid 200 5m;
    proxy_cache_use_stale error timeout updating;
}
```

### 4. Monitoreo de Rendimiento

#### Métricas Clave
```bash
# Script de monitoreo de rendimiento
#!/bin/bash
# /opt/preventia/scripts/performance_monitor.sh

echo "=== Performance Metrics ==="
echo "Timestamp: $(date)"

# API Response Times
echo "API Response Times:"
for endpoint in "/health" "/api/v1/articles/" "/api/v1/analytics/sentiment"; do
    time=$(curl -w "%{time_total}" -s -o /dev/null https://yourdomain.com$endpoint)
    echo "  $endpoint: ${time}s"
done

# Database Performance
echo ""
echo "Database Metrics:"
docker-compose -f docker-compose.prod.yml exec postgres psql -U preventia -d preventia_news -c "
SELECT
    'Active Connections' as metric,
    count(*) as value
FROM pg_stat_activity
WHERE state = 'active'
UNION ALL
SELECT
    'Cache Hit Ratio',
    round(100.0 * sum(blks_hit) / (sum(blks_hit) + sum(blks_read)), 2)
FROM pg_stat_database;
"

# System Resources
echo ""
echo "System Resources:"
echo "CPU: $(top -bn1 | grep "Cpu(s)" | awk '{print $2}' | cut -d'%' -f1)%"
echo "Memory: $(free | grep Mem | awk '{printf("%.1f%%\n", ($3/$2) * 100.0)}')"
echo "Disk: $(df -h / | awk 'NR==2{printf "%s\n", $5}')"
```

### 5. Escalabilidad

#### Escalado Horizontal
```yaml
# docker-compose.scale.yml
version: '3.8'
services:
  api:
    deploy:
      replicas: 3
    environment:
      - WORKERS=2

  nginx:
    depends_on:
      - api
    environment:
      - NGINX_WORKER_PROCESSES=auto
```

#### Load Balancing
```nginx
# nginx upstream configuration
upstream api_backend {
    least_conn;
    server api_1:8000;
    server api_2:8000;
    server api_3:8000;
    keepalive 32;
}
```

---

## 📋 Checklist de Despliegue

### Pre-Despliegue
- [ ] Servidor configurado con especificaciones mínimas
- [ ] Docker y Docker Compose instalados
- [ ] Certificados SSL configurados
- [ ] Variables de entorno de producción configuradas
- [ ] Firewall configurado correctamente
- [ ] Backup del sistema anterior realizado

### Despliegue
- [ ] Repositorio clonado y en rama correcta
- [ ] Tests de pre-despliegue ejecutados
- [ ] Base de datos PostgreSQL iniciada
- [ ] Cache Redis iniciado
- [ ] API Backend desplegada y verificada
- [ ] Frontend desplegado y verificado
- [ ] Nginx proxy configurado con SSL
- [ ] Servicios de monitoreo iniciados

### Post-Despliegue
- [ ] Tests de producción ejecutados satisfactoriamente
- [ ] Health checks de todos los servicios OK
- [ ] Certificados SSL válidos y funcionando
- [ ] Monitoreo y alertas configurados
- [ ] Logs siendo recolectados correctamente
- [ ] Backup automatizado configurado
- [ ] Documentación actualizada
- [ ] Equipo notificado del despliegue exitoso

### Verificación 24h
- [ ] Sistema estable sin errores críticos
- [ ] Rendimiento dentro de parámetros esperados
- [ ] Monitoreo funcionando correctamente
- [ ] Backups ejecutándose automáticamente
- [ ] Logs sin errores recurrentes

---

## 📞 Contacto y Soporte

### Equipo Técnico
- **Desarrollador Principal:** [contacto@ucompensar.edu.co]
- **Infraestructura:** [infraestructura@ucompensar.edu.co]
- **Soporte 24/7:** [soporte@ucompensar.edu.co]

### Recursos Adicionales
- **Documentación:** `/opt/preventia/preventia-app/docs/`
- **Logs del Sistema:** `/opt/preventia/logs/`
- **Monitoreo:** `https://yourdomain.com:3000`
- **Repositorio:** [URL del repositorio Git]

### Escalación de Incidentes
1. **Nivel 1 (Info):** Logs locales + Monitoreo
2. **Nivel 2 (Warning):** Email a equipo técnico
3. **Nivel 3 (Critical):** PagerDuty + Llamada telefónica
4. **Nivel 4 (Emergency):** Activación de equipo completo

---

**Fin del Manual Técnico de Despliegue a Producción**

*Versión 2.0 - Enero 2025*
*PreventIA News Analytics Platform*
*Universidad Compensar (UCOMPENSAR)*
