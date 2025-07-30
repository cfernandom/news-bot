# 1. Descripción del Sistema de Información Desarrollado

## Índice del Contenido

1. [Introducción](#introducción)
2. [Objetivos del Sistema](#objetivos-del-sistema)
   - 2.1 [Objetivo General](#objetivo-general)
   - 2.2 [Objetivos Específicos](#objetivos-específicos)
3. [Módulos Principales](#módulos-principales)
4. [Funcionalidades del Sistema](#funcionalidades-del-sistema)
5. [Arquitectura General](#arquitectura-general)

## Introducción

PreventIA News Analytics es una plataforma inteligente de monitoreo y análisis de noticias especializada en el análisis automatizado de información relacionada con el cáncer de mama. El sistema forma parte del proyecto de investigación multidisciplinario PreventIA, desarrollado en el marco del programa de Investigación y Desarrollo de la Fundación Universitaria Compensar en Colombia.

El sistema combina tecnologías de vanguardia para proporcionar:
- Monitoreo automatizado de fuentes de noticias médicas
- Análisis de sentimiento mediante procesamiento de lenguaje natural
- Visualización interactiva de tendencias mediáticas
- Portal informativo sobre prevención del cáncer de mama
- Herramientas de exportación de datos para investigadores

## Objetivos del Sistema

### Objetivo General

Desarrollar e implementar una plataforma integral de análisis de narrativas mediáticas sobre cáncer de mama que permita a investigadores, profesionales de la salud y tomadores de decisiones comprender las tendencias, sentimientos y patrones en la cobertura mediática de esta enfermedad en Colombia y a nivel internacional.

### Objetivos Específicos

1. **Automatizar la recopilación de noticias**
   - Implementar un sistema de web scraping respetuoso con las políticas de robots.txt
   - Mantener un registro actualizado de fuentes de noticias médicas confiables
   - Detectar y evitar la duplicación de contenido

2. **Analizar el contenido mediático**
   - Aplicar técnicas de NLP para análisis de sentimiento en español e inglés
   - Clasificar artículos por categorías temáticas relevantes
   - Extraer palabras clave y entidades médicas

3. **Visualizar tendencias y patrones**
   - Proporcionar dashboards interactivos con métricas en tiempo real
   - Generar gráficos de tendencias temporales
   - Ofrecer filtros avanzados para análisis específicos

4. **Facilitar la investigación académica**
   - Exportar datos en múltiples formatos (CSV, Excel, PDF)
   - Mantener trazabilidad completa para publicaciones científicas
   - Garantizar la reproducibilidad de los análisis

5. **Educar sobre prevención**
   - Ofrecer un portal público con información confiable
   - Mantener un directorio de instituciones de apoyo
   - Promover la detección temprana del cáncer de mama

## Módulos Principales

### 1. Módulo de Gestión de Fuentes
- **Función**: Administración CRUD de fuentes de noticias
- **Características**:
  - Validación automática de cumplimiento legal
  - Cálculo de compliance score
  - Auditoría de cambios
  - Re-evaluación mensual automática

### 2. Módulo de Web Scraping
- **Función**: Extracción automatizada de artículos
- **Características**:
  - Generación automática de scrapers por CMS
  - Respeto de crawl delay (mínimo 2 segundos)
  - Detección de contenido duplicado
  - Ejecución programada o bajo demanda

### 3. Módulo de Análisis NLP
- **Función**: Procesamiento de lenguaje natural
- **Características**:
  - Análisis de sentimiento con VADER
  - Clasificación temática automática
  - Extracción de entidades médicas
  - Soporte bilingüe (español/inglés)

### 4. Módulo de Visualización
- **Función**: Dashboards y analytics
- **Características**:
  - Portal público informativo
  - Dashboard de analytics con autenticación
  - Panel administrativo
  - Diseño responsive

### 5. Módulo de Exportación
- **Función**: Generación de reportes
- **Características**:
  - Exportación CSV con todos los campos
  - Excel con múltiples hojas
  - PDF con gráficos y estadísticas
  - Imágenes PNG de visualizaciones

### 6. Módulo de Autenticación
- **Función**: Gestión de usuarios y accesos
- **Características**:
  - Autenticación JWT
  - Roles diferenciados (Admin, Analista, Demo)
  - Gestión CRUD de usuarios
  - Tokens con expiración de 24 horas

### 7. CLI de Administración
- **Función**: Herramientas de línea de comandos
- **Características**:
  - Gestión de fuentes y scrapers
  - Monitoreo de compliance
  - Operaciones batch
  - Verificación de estado del sistema

## Funcionalidades del Sistema

### Funcionalidades Principales

1. **Monitoreo Automatizado**
   - Recopilación continua de artículos de múltiples fuentes
   - Procesamiento en pipeline completo en menos de 4 horas
   - Capacidad de procesar 50+ artículos por minuto

2. **Análisis Inteligente**
   - Sentiment score compuesto (-1.0 a 1.0)
   - Clasificación en 7 categorías temáticas
   - Confianza de análisis calculada automáticamente

3. **Cumplimiento Legal**
   - Validación automática de robots.txt
   - Documentación de fair use
   - Política de retención de datos conservadora
   - Trazabilidad completa de auditoría

4. **Accesibilidad**
   - Interfaz optimizada para conexiones de 1 Mbps
   - Soporte para 20+ usuarios concurrentes
   - Tiempos de respuesta < 2 segundos

### Funcionalidades de Soporte

- Respaldo diario con retención de 30 días
- Recuperación automática de fallos
- Logs estructurados para monitoreo
- Health checks integrados

## Arquitectura General

El sistema sigue una arquitectura de microservicios simplificada con las siguientes capas:

### Capa de Presentación
- **Frontend React SPA**: Aplicación de página única con tres interfaces principales
  - Portal público (ruta: `/`)
  - Panel administrativo (ruta: `/admin`)
  - Dashboard experimental (ruta: `/dashboard`)

### Capa de Aplicación
- **API Gateway FastAPI**: Punto de entrada centralizado
  - Autenticación JWT
  - Enrutamiento de peticiones
  - Middleware CORS

### Capa de Servicios
- **Servicios especializados**:
  - Scraper Service
  - NLP Service
  - Data Service
  - Analytics Service
  - Orchestrator Service

### Capa de Datos
- **PostgreSQL**: Base de datos principal
- **Redis**: Cache y optimización
- **Almacenamiento**: Logs y archivos exportados

### Integraciones Externas
- **OpenAI API**: Procesamiento avanzado de texto
- **Sitios de noticias**: Fuentes de información
- **Servicios de notificación**: Alertas del sistema

## Estado Actual del Sistema

### Métricas de Producción
- **Artículos procesados**: 121+ artículos activos
- **Fuentes configuradas**: Múltiples fuentes médicas nacionales e internacionales
- **Disponibilidad**: 95%+ en horario de investigación
- **Performance**: Sub-segundo en respuestas API

### Logros Técnicos
- ✅ Sistema 100% operacional en producción
- ✅ Despliegue automatizado con Docker
- ✅ Cobertura de tests > 85%
- ✅ Documentación completa y actualizada
- ✅ Cumplimiento de estándares de calidad

---

*Siguiente: [02. Diseño Técnico del Sistema](02_DisenoTecnico.md)*
