# 🐳 Docker Implementation Validation Guide

## Overview

Este documento te permite validar que la implementación Docker para PreventIA Dashboard funcione correctamente en **desarrollo** y **producción**.

## 📋 Pre-requisitos

```bash
# Verificar que tengas Docker y Docker Compose
docker --version          # Debe ser >= 20.x
docker compose version    # Debe ser >= 2.x

# Verificar puertos libres
lsof -i :3000             # Debe estar libre para frontend
lsof -i :8000             # Debe estar libre para API
lsof -i :5433             # Debe estar libre para PostgreSQL
```

## 🔧 Entorno de Desarrollo - Validación Completa

### 1. Levantar Stack Completo

```bash
# Desde el directorio raíz del proyecto
cd /home/cfernandom/proyectos/preventia/news_bot_3

# Levantar todos los servicios
docker compose up -d

# Verificar que todos los servicios estén corriendo
docker compose ps
```

**✅ Resultado Esperado:**
```
NAME                 STATUS                    PORTS
preventia_api        Up X minutes (healthy)    0.0.0.0:8000->8000/tcp
preventia_frontend   Up X minutes              0.0.0.0:3000->5173/tcp
preventia_postgres   Up X minutes (healthy)    0.0.0.0:5433->5432/tcp
```

### 2. Validar Servicios Individuales

#### PostgreSQL Database
```bash
# Test 1: Verificar conexión a la base de datos
docker compose exec postgres pg_isready -U preventia

# Test 2: Contar artículos almacenados
docker compose exec postgres psql -U preventia -d preventia_news -c "SELECT COUNT(*) FROM articles;"
```

**✅ Resultado Esperado:**
- Conexión exitosa
- Conteo de ~106 artículos

#### FastAPI Backend
```bash
# Test 1: Health check
curl http://localhost:8000/health

# Test 2: API documentation
curl -s http://localhost:8000/docs | grep -i "swagger"

# Test 3: Dashboard analytics
curl http://localhost:8000/api/analytics/dashboard
```

**✅ Resultado Esperado:**
```json
// Health
{"status":"healthy","database":"connected","articles_count":106,"version":"1.0.0"}

// Analytics (ejemplo)
{"total_articles":106,"sentiment_distribution":{"negative":79,"positive":24,"neutral":3}}
```

#### React Frontend
```bash
# Test 1: Frontend accesible
curl -s http://localhost:3000 | grep -i "vite"

# Test 2: Verificar hot reload (desarrollo)
# Edita cualquier archivo en preventia-dashboard/src/
# El browser debería recargar automáticamente
```

**✅ Resultado Esperado:**
- HTML con scripts de Vite
- Hot reload funcionando

### 3. Validar Integración API ↔ Frontend

```bash
# Abrir en browser: http://localhost:3000
# Verificar manualmente:
```

**✅ Checklist Manual:**
- [ ] Dashboard carga sin errores 404/500
- [ ] KPI cards muestran datos numéricos reales
- [ ] SentimentChart renderiza con datos
- [ ] TopicsChart muestra distribución
- [ ] Modo Professional/Educational switch funciona
- [ ] Network tab muestra llamadas exitosas a http://localhost:8000/api/*

### 4. Validar Hot Reload y Desarrollo

```bash
# Test de desarrollo: Modificar componente
echo "console.log('Docker validation test');" >> preventia-dashboard/src/main.tsx

# Verificar en browser que el cambio se refleje automáticamente
# Luego revertir el cambio
git checkout -- preventia-dashboard/src/main.tsx
```

**✅ Resultado Esperado:**
- Cambio visible inmediatamente
- No necesidad de rebuild del container

## 🏭 Entorno de Producción - Validación

### 1. Build de Producción Local

```bash
# Desde preventia-dashboard/
cd preventia-dashboard

# Crear archivo de producción
cp .env.production.template .env.production

# Modificar .env.production si es necesario:
# VITE_API_URL=http://localhost:8000/api

# Build local
npm run build
```

**✅ Resultado Esperado:**
```
✓ 1438 modules transformed.
dist/index.html                   0.46 kB
dist/assets/index-xxxxx.css      ~38 kB
dist/assets/index-xxxxx.js       ~758 kB
✓ built in ~5s
```

### 2. Dockerfile Multi-stage Validation

```bash
# Build imagen de producción (puede tomar 5-10 minutos)
docker build -f Dockerfile -t preventia-dashboard-prod .

# Verificar que la imagen se creó
docker images | grep preventia-dashboard-prod
```

**✅ Resultado Esperado:**
```
preventia-dashboard-prod   latest   xxxxxxxx   X minutes ago   XX MB
```

### 3. Test Imagen de Producción

```bash
# Parar frontend de desarrollo
docker compose stop frontend

# Ejecutar imagen de producción
docker run -d --name test-prod-frontend \
  --network news_bot_3_default \
  -p 3001:80 \
  preventia-dashboard-prod

# Verificar que funcione
curl -s http://localhost:3001 | grep -i "html"

# Test de API integration desde producción
curl -s http://localhost:3001 | grep -i "vite" && echo "❌ VITE encontrado - no es build de producción" || echo "✅ Build de producción correcto"
```

**✅ Resultado Esperado:**
- HTML válido sin referencias a Vite
- Estilos compilados y minificados
- JavaScript bundleado

### 4. Nginx Configuration Validation

```bash
# Verificar configuración de Nginx
docker exec test-prod-frontend cat /etc/nginx/nginx.conf | grep -A 5 "location /api"

# Test proxy hacia API
curl -s http://localhost:3001/api/health
```

**✅ Resultado Esperado:**
- Proxy configurado hacia API interno
- API accesible a través del frontend

### 5. Production Performance Test

```bash
# Test de carga de assets
time curl -s http://localhost:3001/assets/index-*.js > /dev/null

# Test de respuesta de API a través del proxy
time curl -s http://localhost:3001/api/analytics/dashboard > /dev/null
```

**✅ Resultado Esperado:**
- Assets cargan en < 1s
- API responde en < 2s

## 🧹 Cleanup y Reset

```bash
# Limpiar test de producción
docker stop test-prod-frontend
docker rm test-prod-frontend
docker rmi preventia-dashboard-prod

# Reiniciar entorno de desarrollo
docker compose down
docker compose up -d

# Verificar estado final
docker compose ps
```

## 🚨 Troubleshooting Común

### Frontend no carga
```bash
# Verificar logs
docker compose logs frontend

# Verificar puerto correcto
docker compose ps | grep frontend
```

### API no responde
```bash
# Verificar health del API
docker compose logs api
curl http://localhost:8000/health
```

### Build de producción falla
```bash
# Verificar dependencias
cd preventia-dashboard && npm install

# Verificar archivo .env.production existe
ls -la .env.production*

# Build local antes de Docker
npm run build
```

### Hot reload no funciona
```bash
# Verificar volúmenes montados
docker compose config | grep -A 5 volumes

# Verificar permisos de archivos
ls -la preventia-dashboard/src/
```

## ✅ Validation Checklist Final

### Desarrollo ✓
- [ ] `docker compose up -d` exitoso
- [ ] PostgreSQL (5433) healthy con 106 artículos
- [ ] FastAPI (8000) healthy con endpoints funcionando
- [ ] React Frontend (3000) con hot reload
- [ ] Integración API ↔ Frontend funcional
- [ ] Dual-mode switching operativo

### Producción ✓
- [ ] `npm run build` exitoso localmente
- [ ] `docker build -f Dockerfile` exitoso
- [ ] Imagen de producción ejecuta correctamente
- [ ] Nginx proxy API funcional
- [ ] Assets minificados y optimizados
- [ ] Performance < 2s para cargas

### Integration ✓
- [ ] API accessible desde ambos entornos
- [ ] Datos reales (106 artículos) visibles en dashboard
- [ ] Error handling funcional
- [ ] Environment variables correctamente configuradas

## 📝 Resultados de Validación

**Fecha de validación:** ___________

**Entorno de Desarrollo:**
- PostgreSQL: ✅ / ❌
- FastAPI: ✅ / ❌
- React Frontend: ✅ / ❌
- Integración: ✅ / ❌

**Entorno de Producción:**
- Build Local: ✅ / ❌
- Docker Build: ✅ / ❌
- Nginx Config: ✅ / ❌
- Performance: ✅ / ❌

**Issues encontrados:**
_________________________________
_________________________________
_________________________________

**Validación completada por:** ___________
