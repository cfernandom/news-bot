# Módulo 6: Troubleshooting y FAQ
## Manual de Usuario - PreventIA News Analytics

---

## 🎯 ¿Qué aprenderás en este módulo?

Al completar este módulo serás capaz de:
- Solucionar problemas comunes de acceso y funcionalidad
- Interpretar mensajes de error del sistema
- Contactar soporte técnico de manera efectiva
- Manejar limitaciones conocidas y aplicar workarounds
- Optimizar rendimiento del sistema para análisis grandes
- Prepararte para uso avanzado y expansión del sistema

---

## 🔧 Problemas Comunes y Soluciones

### **🌐 Problemas de Acceso**

#### **❌ No puedo acceder al dashboard principal**

**Síntomas:**
- Página no carga en `http://localhost:5173`
- Error "This site can't be reached"
- Timeout de conexión

**Diagnóstico paso a paso:**
1. **Verificar servicios Docker**:
   ```bash
   docker compose ps
   ```
   **Esperado**: `preventia_frontend` con status "Up X hours (healthy)"

2. **Verificar estado específico del frontend**:
   ```bash
   curl -I http://localhost:5173
   ```
   **Esperado**: `HTTP/1.1 200 OK`

**Soluciones:**

**🔄 Solución 1: Reiniciar frontend**
```bash
docker compose restart frontend
# Esperar 30-60 segundos
curl http://localhost:5173
```

**🔄 Solución 2: Verificar puertos**
```bash
# Verificar que puerto 5173 no esté ocupado
netstat -tulpn | grep 5173
# Si hay conflicto, cambiar puerto en docker-compose.yml
```

**🔄 Solución 3: Reconstruir servicios**
```bash
docker compose down
docker compose up -d --build
```

#### **❌ No puedo acceder al panel de administración**

**Síntomas:**
- Error 404 en `http://localhost:5173/admin`
- Dashboard funciona pero admin no

**Diagnóstico:**
1. **Verificar ruta exacta**: Asegurar `/admin` (no `/administration`)
2. **Verificar permisos**: Tu usuario puede tener acceso limitado
3. **Verificar router**: Frontend puede tener routing issues

**Soluciones:**

**✅ Solución 1: Acceso directo desde dashboard**
- Buscar enlace "Admin" o "Administración" en menú principal
- Usar navegación interna en lugar de URL directa

**✅ Solución 2: Verificar roles de usuario**
- Contactar administrador para verificar permisos
- Usuarios básicos pueden tener acceso read-only

### **🚀 Problemas de API**

#### **❌ Error "API not responding" o timeouts**

**Síntomas:**
- Gráficos no cargan
- Exportaciones fallan
- Dashboard muestra errores de conexión

**Diagnóstico:**
1. **Verificar API health**:
   ```bash
   curl http://localhost:8000/health
   ```
   **Esperado**: `{"status":"healthy","database":"connected","articles_count":121,"version":"1.0.0"}`

2. **Verificar servicios backend**:
   ```bash
   docker compose ps | grep api
   ```
   **Esperado**: `preventia_api` con status "Up X hours (healthy)"

**Soluciones:**

**🔄 Solución 1: Reiniciar API**
```bash
docker compose restart api
# Esperar 60-90 segundos para startup completo
curl http://localhost:8000/health
```

**🔄 Solución 2: Verificar logs**
```bash
docker compose logs api
# Buscar errores de conexión a base de datos
# Verificar que no hay errores de importación Python
```

**🔄 Solución 3: Verificar base de datos**
```bash
docker compose exec postgres pg_isready -U preventia
# Debe responder: "accepting connections"
```

#### **❌ Exportaciones fallan o generan archivos corruptos**

**Síntomas:**
- Error "Chart export not yet implemented"
- Archivos PNG/SVG vacíos o corruptos
- Timeouts en exportaciones PDF

**Diagnóstico y soluciones:**

**📊 Para exportaciones de gráficos:**
```bash
# Verificar endpoints específicos
curl -I http://localhost:8000/api/v1/export/charts/sentiment.png

# Si obtienes 405 Method Not Allowed, usar GET:
curl -O http://localhost:8000/api/v1/export/charts/sentiment.png
```

**📋 Para exportaciones de datos:**
```bash
# CSV siempre debe funcionar:
curl -O http://localhost:8000/api/v1/export/news.csv

# Verificar tamaño del archivo:
ls -lh news.csv
# Esperado: ~50KB para 121 artículos
```

**⚠️ Limitaciones conocidas:**
- Exportaciones PDF pueden requerir >30 segundos
- Gráficos SVG requieren más memoria que PNG
- Exportaciones simultáneas máximo 5

### **📊 Problemas de Base de Datos**

#### **❌ Error "Database connection failed"**

**Síntomas:**
- Dashboard muestra "No data available"
- API health check falla en database
- Conteos de artículos en 0

**Diagnóstico:**
```bash
# 1. Verificar PostgreSQL está corriendo
docker compose ps | grep postgres

# 2. Verificar conectividad
docker compose exec postgres pg_isready -U preventia

# 3. Verificar datos
docker compose exec postgres psql -U preventia -d preventia_news -c "SELECT COUNT(*) FROM articles;"
```

**Soluciones:**

**🔄 Solución 1: Reiniciar PostgreSQL**
```bash
docker compose restart postgres
# Esperar 2-3 minutos para startup completo
docker compose exec postgres pg_isready -U preventia
```

**🔄 Solución 2: Verificar variables de entorno**
```bash
# Verificar .env tiene configuración correcta:
# DATABASE_URL=postgresql://preventia:password@postgres:5432/preventia_news
```

**🔄 Solución 3: Recrear base de datos**
```bash
# ⚠️ CUIDADO: Esto elimina todos los datos
docker compose down
docker volume rm news_bot_3_postgres_data
docker compose up -d
# Requiere re-ejecutar migraciones
```

---

## ⚠️ Limitaciones Conocidas y Workarounds

### **📊 Limitaciones de Datos**

#### **🌍 Sesgo Geográfico (70% EE.UU.)**
**Limitación**: Dataset dominado por fuentes estadounidenses

**Impacto**:
- Análisis globales sesgados hacia perspectiva estadounidense
- Sub-representación de regiones no anglófonas
- Generalizaciones limitadas fuera de contexto norteamericano

**Workarounds**:
```
✅ Para investigación estadounidense:
- Usar dataset completo apropiadamente
- Documentar ventaja de representatividad local

✅ Para análisis global:
- Filtrar solo artículos "Global" (35 artículos)
- Documentar limitación geográfica en metodología
- Sugerir expansión de fuentes como trabajo futuro

✅ Para estudios comparativos:
- Usar análisis EE.UU. vs Internacional como proxy
- Reconocer limitaciones de generalización
- Proponer replicación con fuentes diversas
```

#### **📅 Concentración Temporal (49.6% en 2 meses)**
**Limitación**: Distribución temporal extremadamente desigual

**Impacto**:
- Análisis de tendencias sesgado por pico mayo-junio 2025
- Comparaciones temporales problemáticas
- Estacionalidad artificial vs natural

**Workarounds**:
```
✅ Para análisis de tendencias:
- Usar normalización estacional
- Comparar períodos equivalentes año anterior
- Aplicar suavizado temporal (moving averages)

✅ Para análisis de eventos:
- Separar análisis "pico" vs "baseline"
- Usar mayo-junio como caso especial
- Documentar concentración como característica del dataset

✅ Para comparaciones:
- Usar análisis por trimestres balanceados
- Evitar comparaciones dic-feb vs may-jun
- Aplicar ponderación temporal
```

### **🔧 Limitaciones Técnicas**

#### **📤 Exportaciones**
**Limitaciones verificadas**:
- Máximo 5 exportaciones simultáneas
- Timeout de 30 segundos por exportación
- Tamaño máximo 10MB por archivo
- Historial limitado a 100 exportaciones

**Workarounds**:
```
✅ Para exportaciones grandes:
- Usar CSV para datasets grandes (más eficiente)
- Dividir exportaciones en lotes más pequeños
- Usar PNG en lugar de SVG para gráficos complejos

✅ Para múltiples exportaciones:
- Espaciar requests por 2-3 segundos
- Usar queue secuencial en lugar de paralela
- Verificar estado antes de nueva exportación

✅ Para archivos de backup:
- Descargar exportaciones críticas inmediatamente
- Mantener backup local de CSVs importantes
- Documentar IDs de exportación para auditoria
```

#### **🔍 Filtros y Búsqueda**
**Limitaciones actuales**:
- Sin filtros por fuente específica en exportaciones
- Sin búsqueda por texto en dashboard
- Filtros temporales limitados a períodos predefinidos

**Workarounds**:
```
✅ Para filtros por fuente:
- Exportar CSV completo
- Filtrar en Excel/R/Python por columna 'source_url'
- Usar análisis post-procesamiento

✅ Para búsqueda por contenido:
- Exportar dataset completo
- Usar herramientas externas para text mining
- Aplicar análisis NLP personalizado

✅ Para filtros temporales específicos:
- Usar exportaciones CSV con filtrado manual
- Aplicar análisis por fecha en herramientas externas
- Proponer fechas específicas como mejora futura
```

### **🎯 Limitaciones de Análisis**

#### **📈 Análisis de Sentimientos**
**Limitaciones metodológicas**:
- VADER optimizado para inglés
- Thresholds ajustados para contenido médico
- Sin análisis de aspectos específicos

**Workarounds**:
```
✅ Para contenido no-inglés:
- Documentar limitación idiomática
- Usar solo artículos verificados en inglés
- Considerar traducción para análisis específicos

✅ Para análisis granular:
- Exportar scores numéricos (CSV)
- Aplicar análisis estadístico personalizado
- Usar sentiment_score en lugar de labels

✅ Para validación:
- Revisar muestra manual de artículos
- Verificar coherencia sentiment vs contenido
- Reportar confidence intervals
```

---

## 📞 Contacto y Soporte Técnico

### **🆘 Cuándo Contactar Soporte**

#### **🔴 Problemas Críticos (Contacto Inmediato)**
- Sistema completamente inaccesible por >1 hora
- Pérdida de datos o corrupción de base de datos
- Errores de seguridad o acceso no autorizado
- Fallos masivos de exportación que afectan investigación

#### **🟡 Problemas Moderados (Contacto en 24h)**
- Funcionalidades específicas no funcionan
- Performance degradado significativamente
- Errores intermitentes que afectan workflow
- Necesidad de nuevas fuentes de datos

#### **🟢 Consultas Generales (Contacto en 48-72h)**
- Preguntas sobre interpretación de datos
- Solicitudes de mejoras o nuevas funcionalidades
- Consultas sobre metodología de análisis
- Training adicional o documentación

### **📋 Información a Incluir en Contacto**

#### **✅ Checklist de Información Necesaria**
```
📧 Plantilla de Reporte de Issue:

Asunto: [CRÍTICO/MODERADO/CONSULTA] - Descripción breve

1. INFORMACIÓN DEL SISTEMA:
   - URL de acceso: http://localhost:5173
   - Navegador y versión: [Chrome 91, Firefox 89, etc.]
   - Sistema operativo: [Windows 10, macOS 12, Ubuntu 20.04]
   - Timestamp del problema: [YYYY-MM-DD HH:MM]

2. DESCRIPCIÓN DEL PROBLEMA:
   - ¿Qué estabas intentando hacer?
   - ¿Qué esperabas que pasara?
   - ¿Qué pasó en realidad?
   - ¿Es la primera vez que ocurre?

3. PASOS PARA REPRODUCIR:
   1. [Paso específico]
   2. [Paso específico]
   3. [Resultado observado]

4. DIAGNÓSTICO BÁSICO REALIZADO:
   - [ ] Verificé http://localhost:8000/health
   - [ ] Reinicié navegador
   - [ ] Probé en ventana incógnita
   - [ ] Verifiqué docker compose ps

5. IMPACTO:
   - ¿Esto bloquea tu trabajo completamente?
   - ¿Hay workaround temporal disponible?
   - ¿Cuánta urgencia tiene la resolución?

6. ARCHIVOS ADJUNTOS:
   - Screenshots del error
   - Archivos de log (si tienes acceso)
   - Exportaciones problemáticas
```

### **🔧 Auto-Diagnóstico Antes de Contactar**

#### **📋 Checklist de Verificación Rápida (5 minutos)**
```bash
# 1. Verificar conectividad básica
curl http://localhost:5173
curl http://localhost:8000/health

# 2. Verificar servicios Docker
docker compose ps

# 3. Verificar logs recientes
docker compose logs --tail=50 api
docker compose logs --tail=50 frontend

# 4. Verificar base de datos
docker compose exec postgres pg_isready -U preventia

# 5. Verificar datos básicos
curl -s http://localhost:8000/health | grep articles_count
```

#### **📊 Información de Estado del Sistema**
```
Estado verificado 2025-07-08:
✅ API: http://localhost:8000 (healthy)
✅ Frontend: http://localhost:5173 (operational)
✅ Database: 121 artículos, 9 fuentes
✅ Services: 5 contenedores corriendo
✅ Exports: 7 endpoints funcionales
```

---

## 🚀 Optimización de Performance

### **⚡ Para Análisis Grandes**

#### **📊 Optimización de Exportaciones**
```
🎯 Para datasets grandes (>1000 artículos):
- Usar CSV en lugar de XLSX (3x más rápido)
- Evitar exportaciones PNG simultáneas
- Procesar en lotes de 500 artículos máximo

⚡ Para gráficos complejos:
- PNG para presentaciones (mejor performance)
- SVG solo para publicaciones académicas
- Evitar múltiples gráficos simultáneos

💾 Para almacenamiento:
- Comprimir CSVs grandes antes de backup
- Usar PNG para archivos frecuentemente accedidos
- PDF solo para documentos finales
```

#### **🔍 Optimización de Análisis**
```
📈 Para análisis estadísticos:
- Exportar raw data (CSV) para análisis externo
- Usar R/Python para análisis complejos
- Mantener PreventIA para visualización inicial

🌐 Para análisis geográficos:
- Filtrar por región antes de análisis detallado
- Usar herramientas GIS externas para mapas complejos
- Combinar con datos demográficos externos

⏰ Para análisis temporales:
- Usar herramientas de time series especializadas
- Aplicar normalización estacional externa
- Combinar con datos de eventos médicos
```

### **💻 Optimización del Sistema**

#### **🖥️ Configuración del Cliente**
```
✅ Navegador recomendado:
- Chrome/Edge: Mejor performance para gráficos
- Firefox: Compatible, ligeramente más lento
- Safari: Funcional, issues menores con SVG

💾 Configuración recomendada:
- RAM: Mínimo 4GB, recomendado 8GB+
- Conexión: Estable para exportaciones grandes
- Resolución: 1920x1080 para dashboard óptimo

🔧 Settings de navegador:
- JavaScript habilitado (esencial)
- Cookies habilitadas para sesiones
- Pop-ups permitidos para exportaciones
```

#### **🐳 Configuración Docker (Admins)**
```
⚡ Para mejor performance:
- Asignar 4GB+ RAM a Docker
- Usar SSD para volúmenes de datos
- Optimizar memoria compartida PostgreSQL

📊 Monitoreo de recursos:
docker stats preventia_api preventia_postgres
# Verificar CPU y memoria bajo carga

🔧 Optimización de base de datos:
# Vacuum periódico para PostgreSQL
docker compose exec postgres psql -U preventia -d preventia_news -c "VACUUM ANALYZE;"
```

---

## 📚 Recursos Adicionales

### **📖 Documentación de Referencia**

#### **🔗 Enlaces Rápidos del Sistema**
```
🌐 Acceso Principal:
- Dashboard: http://localhost:5173
- API Docs: http://localhost:8000/docs
- Admin Panel: http://localhost:5173/admin
- Health Check: http://localhost:8000/health

📊 Exportaciones Directas:
- CSV: http://localhost:8000/api/v1/export/news.csv
- Gráfico Sentimientos: http://localhost:8000/api/v1/export/charts/sentiment.png
- Historial: http://localhost:8000/api/v1/export/user/exports

📋 Estado del Sistema:
- Servicios: docker compose ps
- Logs API: docker compose logs api
- Logs Frontend: docker compose logs frontend
```

#### **📚 Documentación Adicional**
```
📁 Ubicación: docs/product/manual-usuario/

📖 Módulos completados:
1. Introducción y Primeros Pasos
2. Análisis de Sentimientos
3. Gestión de Fuentes de Noticias
4. Exportación y Reportes
5. Análisis Geográfico y Temporal
6. Troubleshooting y FAQ (este módulo)

🔧 Documentación técnica:
- docs/api/: API documentation
- docs/architecture/: System architecture
- docs/development/: Development guides
```

### **🎓 Para Usuarios Avanzados**

#### **🔬 Extensión del Análisis**
```
🐍 Análisis con Python:
import pandas as pd
# Cargar CSV exportado
df = pd.read_csv('preventia_dataset.csv')
# Análisis personalizado con pandas/numpy/scikit-learn

📊 Análisis con R:
library(tidyverse)
data <- read_csv("preventia_dataset.csv")
# Análisis con ggplot2, dplyr, statistical tests

📈 Visualización avanzada:
- Tableau: Import CSV para dashboards complejos
- Power BI: Connect para análisis empresarial
- D3.js: Custom visualizations con datos exportados
```

#### **🔌 Integración con Otros Sistemas**
```
📡 APIs externas:
- Combinar con datos epidemiológicos (CDC, WHO)
- Integrar con datos de redes sociales
- Correlacionar con eventos médicos (conferences, approvals)

🗄️ Bases de datos externas:
- PubMed para literatura académica
- ClinicalTrials.gov para estudios clínicos
- FDA databases para approvals y warnings

🌐 Herramientas complementarias:
- Google Trends para validación temporal
- Social media APIs para sentiment comparison
- Financial data para correlación con biotech stocks
```

---

## ❓ FAQ Comprehensivo

### **🔧 Preguntas Técnicas**

**P: ¿Puedo usar el sistema sin conexión a internet?**
**R:** Parcialmente. Una vez cargado, el dashboard funciona offline, pero:
- No se actualizan datos nuevos
- Exportaciones requieren conexión a API local
- Funcionalidades admin pueden fallar

**P: ¿Qué pasa si mi análisis requiere más de 121 artículos?**
**R:** Opciones:
- Solicitar expansión del dataset al equipo técnico
- Combinar con datos externos usando methodología similar
- Usar dataset actual como pilot study para proyectos más grandes

**P: ¿Puedo modificar los algoritmos de sentiment analysis?**
**R:** No directamente en la interfaz, pero:
- Exporta raw text (CSV) para análisis personalizado
- Usa sentiment_score (numérico) en lugar de labels
- Propón mejoras al equipo de desarrollo

### **📊 Preguntas de Análisis**

**P: ¿Cómo sé si mis resultados son estadísticamente significativos?**
**R:** Consideraciones:
- n=121 es suficiente para análisis exploratorio
- Para significancia estadística: usar tests apropiados (t-test, chi-square)
- Reportar siempre intervalos de confianza
- Considerar power analysis para planificar estudios futuros

**P: ¿El sesgo geográfico invalida mis resultados?**
**R:** No necesariamente:
- Para estudios de EE.UU.: Dataset apropiado
- Para estudios globales: Documentar limitación y ajustar interpretación
- Para metodología: Usar como ejemplo de bias en data collection

**P: ¿Puedo comparar resultados con otros estudios?**
**R:** Con precauciones:
- Documentar diferencias metodológicas
- Comparar solo estudios con fuentes similares
- Considerar período temporal y criterios de inclusión

### **🚀 Preguntas de Uso Avanzado**

**P: ¿Cómo propongo nuevas fuentes de datos?**
**R:** Proceso recomendado:
- Identificar fuentes médicas relevantes y confiables
- Verificar que permiten web scraping (robots.txt)
- Contactar equipo técnico con justificación científica
- Proporcionar URLs específicas y criterios de calidad

**P: ¿Puedo colaborar con otros investigadores usando este sistema?**
**R:** Sí, estrategias:
- Compartir exportaciones CSV para replicación
- Documentar metodología exacta (filtros, períodos)
- Usar IDs de exportación para auditoria
- Coordinar timing de análisis para datos consistentes

**P: ¿El sistema se puede usar para otros tipos de cáncer?**
**R:** Actualmente especializado en cáncer de mama, pero:
- Framework es adaptable a otros tipos
- Requiere nuevas fuentes especializadas
- Algoritmos NLP necesitarían re-entrenamiento
- Propuesta viable para expansión futura

---

## 🎯 Resumen del Módulo 6

### ✅ **Has Aprendido:**
- Solucionar problemas comunes de acceso, API y base de datos
- Interpretar y reportar errores del sistema efectivamente
- Manejar limitaciones conocidas con workarounds apropiados
- Optimizar performance para análisis grandes y complejos
- Contactar soporte técnico con información útil
- Usar recursos avanzados para análisis personalizado

### 🔧 **Problemas Cubiertos:**
- **Acceso**: Dashboard, admin panel, conectividad
- **API**: Timeouts, exportaciones, health checks
- **Base de datos**: Conexiones, datos, performance
- **Limitaciones**: Geográficas, temporales, técnicas
- **Performance**: Optimización cliente y servidor

### 📋 **Checklist de Troubleshooting:**
- [ ] Memoricé comandos básicos de verificación del sistema
- [ ] Entiendo limitaciones principales y sus workarounds
- [ ] Sé cómo reportar problemas con información completa
- [ ] Conozco optimizaciones para mi tipo de análisis
- [ ] Identifiqué recursos adicionales para uso avanzado
- [ ] Entiendo cuándo contactar soporte vs autosolucionar

---

## 🏆 Felicitaciones: Manual Completo

**🎉 Has completado los 6 módulos del Manual de Usuario de PreventIA News Analytics**

### **📚 Lo que has dominado:**
1. **Navegación básica** y acceso al sistema
2. **Análisis de sentimientos** con interpretación médica especializada
3. **Gestión de fuentes** y comprensión de compliance
4. **Exportación profesional** en múltiples formatos
5. **Análisis geográfico-temporal** con consciencia de sesgos
6. **Troubleshooting independiente** y resolución de problemas

### **🎯 Estás preparado para:**
- **Investigación académica** con metodología rigurosa
- **Análisis ejecutivo** con reportes profesionales
- **Proyectos estudiantiles** con comprensión completa del sistema
- **Uso avanzado** con herramientas complementarias
- **Colaboración efectiva** con otros investigadores

### **🚀 Próximos pasos recomendados:**
1. **Practica** con un proyecto real usando todos los módulos
2. **Explora** herramientas avanzadas (R, Python, Tableau)
3. **Documenta** tu metodología usando las mejores prácticas aprendidas
4. **Comparte** conocimiento con colegas interesados
5. **Propón mejoras** basadas en tu experiencia de uso

---

**🔗 Enlaces de Referencia Rápida:**
- **Dashboard**: http://localhost:5173
- **API Health**: http://localhost:8000/health
- **Exportaciones**: http://localhost:8000/api/v1/export/
- **Índice del Manual**: [Manual de Usuario](../indice-principal.md)

**💡 Recordatorio final**: PreventIA News Analytics es una herramienta poderosa para análisis de noticias médicas. Úsala responsablemente, documenta limitaciones apropiadamente, y contribuye al avance del conocimiento médico con investigación rigurosa y ética.
