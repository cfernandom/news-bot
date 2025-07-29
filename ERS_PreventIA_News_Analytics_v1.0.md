# Especificación de Requerimientos del Software (ERS)
## Sistema PreventIA News Analytics

**Versión:** 1.0
**Fecha:** 29 de Julio de 2025
**Estado:** BORRADOR - Pendiente información del usuario

---

## Tabla de Contenidos

1. [Introducción](#1-introducción)
   1.1 [Propósito](#11-propósito)
   1.2 [Alcance](#12-alcance)
   1.3 [Definiciones, Acrónimos y Abreviaturas](#13-definiciones-acrónimos-y-abreviaturas)
   1.4 [Referencias](#14-referencias)
   1.5 [Visión General del Documento](#15-visión-general-del-documento)

2. [Descripción General del Sistema](#2-descripción-general-del-sistema)
   2.1 [Perspectiva del Producto](#21-perspectiva-del-producto)
   2.2 [Funciones del Producto](#22-funciones-del-producto)
   2.3 [Características de los Usuarios](#23-características-de-los-usuarios)
   2.4 [Restricciones](#24-restricciones)
   2.5 [Suposiciones y Dependencias](#25-suposiciones-y-dependencias)

3. [Requerimientos Funcionales](#3-requerimientos-funcionales)
   3.1 [Gestión de Fuentes de Noticias](#31-gestión-de-fuentes-de-noticias)
   3.2 [Web Scraping Automatizado](#32-web-scraping-automatizado)
   3.3 [Análisis de Sentimiento y NLP](#33-análisis-de-sentimiento-y-nlp)
   3.4 [Dashboard de Visualización](#34-dashboard-de-visualización)
   3.5 [Sistema de Exportación](#35-sistema-de-exportación)
   3.6 [Gestión de Usuarios y Autenticación](#36-gestión-de-usuarios-y-autenticación)
   3.7 [CLI de Administración](#37-cli-de-administración)

4. [Requerimientos No Funcionales](#4-requerimientos-no-funcionales)
   4.1 [Requisitos de Rendimiento](#41-requisitos-de-rendimiento)
   4.2 [Requisitos de Seguridad](#42-requisitos-de-seguridad)
   4.3 [Requisitos de Fiabilidad](#43-requisitos-de-fiabilidad)
   4.4 [Requisitos de Mantenibilidad](#44-requisitos-de-mantenibilidad)
   4.5 [Requisitos de Portabilidad](#45-requisitos-de-portabilidad)

5. [Requerimientos de Interfaz](#5-requerimientos-de-interfaz)
   5.1 [Interfaces de Usuario](#51-interfaces-de-usuario)
   5.2 [Interfaces de Hardware](#52-interfaces-de-hardware)
   5.3 [Interfaces de Software](#53-interfaces-de-software)
   5.4 [Interfaces de Comunicación](#54-interfaces-de-comunicación)

6. [Apéndices](#6-apéndices)
   6.1 [Arquitectura del Sistema](#61-arquitectura-del-sistema)
   6.2 [Modelo de Datos](#62-modelo-de-datos)
   6.3 [Stack Tecnológico](#63-stack-tecnológico)

---

## 1. Introducción

### 1.1 Propósito

Este documento establece la especificación completa de requerimientos del software para el sistema **PreventIA News Analytics**, una plataforma inteligente de monitoreo y análisis de noticias especializada en el análisis automatizado de información relacionada con el cáncer de mama.

El propósito principal de este documento es:
- Definir las funcionalidades completas del sistema
- Establecer los requerimientos funcionales y no funcionales
- Servir como referencia para el desarrollo y mantenimiento
- Facilitar la comunicación entre stakeholders técnicos y no técnicos

### 1.2 Alcance

PreventIA News Analytics es un sistema integral que automatiza la recopilación, análisis y visualización de noticias sobre cáncer de mama, proporcionando:

**Incluye:**
- Web scraping automatizado de fuentes de noticias médicas
- Análisis de sentimiento mediante procesamiento de lenguaje natural (NLP)
- Clasificación temática de artículos
- Dashboard interactivo para visualización de analytics
- Sistema de exportación multi-formato (CSV, Excel, PDF)
- Gestión de usuarios con roles y permisos
- CLI para administración del sistema

**No incluye:**
- Diagnóstico médico automatizado
- Recomendaciones de tratamiento
- Almacenamiento de historiales clínicos de pacientes
- Integración directa con sistemas hospitalarios (en esta versión)

### 1.3 Definiciones, Acrónimos y Abreviaturas

- **API**: Application Programming Interface
- **CLI**: Command Line Interface
- **CRUD**: Create, Read, Update, Delete
- **JWT**: JSON Web Token
- **NLP**: Natural Language Processing
- **ORM**: Object-Relational Mapping
- **REST**: Representational State Transfer
- **SPA**: Single Page Application
- **VADER**: Valence Aware Dictionary and sEntiment Reasoner
- **WebScraping**: Técnica de extracción automatizada de datos de sitios web

### 1.4 Referencias

- Estándar IEEE 830-1998 para Especificación de Requerimientos de Software
- Documentación de FastAPI v0.115.14
- Documentación de React v19.1.0
- Documentación de PostgreSQL v13+
- Principios de Fair Use y robots.txt

### 1.5 Visión General del Documento

Este documento está estructurado siguiendo el estándar IEEE 830, organizado en secciones que cubren desde la descripción general del sistema hasta los requerimientos específicos funcionales y no funcionales, concluyendo con apéndices técnicos detallados.

---

## 2. Descripción General del Sistema

### 2.1 Perspectiva del Producto

PreventIA News Analytics es un sistema autónomo diseñado para operar como una plataforma independiente de monitoreo de medios especializados. El sistema se integra con:

- **Fuentes de datos externas**: Sitios web de noticias médicas mediante web scraping
- **Servicios de IA**: OpenAI API para procesamiento avanzado de texto
- **Infraestructura de contenedores**: Docker para despliegue y escalabilidad

**Arquitectura del Sistema:**
```
┌─────────────────────────────────────────────────────────────┐
│                    Frontend (React + TypeScript)             │
│  ┌─────────────┐  ┌──────────────┐  ┌──────────────────┐   │
│  │   Legacy    │  │    Admin     │  │  Modern Dashboard│   │
│  │  Interface  │  │    Panel     │  │   (Future)       │   │
│  └─────────────┘  └──────────────┘  └──────────────────┘   │
└─────────────────────────────┬───────────────────────────────┘
                              │ HTTP/REST
┌─────────────────────────────┴───────────────────────────────┐
│                      API Gateway (FastAPI)                   │
├─────────────────────────────────────────────────────────────┤
│                        Microservicios                        │
│  ┌──────────┐ ┌──────────┐ ┌─────────┐ ┌───────────────┐  │
│  │ Scraper  │ │   NLP    │ │  Data   │ │ Decision      │  │
│  │ Service  │ │ Service  │ │ Service │ │ Engine        │  │
│  └──────────┘ └──────────┘ └─────────┘ └───────────────┘  │
│  ┌──────────┐ ┌──────────┐ ┌─────────┐ ┌───────────────┐  │
│  │Copywriter│ │Publisher │ │Orchestr.│ │ Analytics     │  │
│  │ Service  │ │ Service  │ │ Service │ │ Service       │  │
│  └──────────┘ └──────────┘ └─────────┘ └───────────────┘  │
└─────────────────────────────────────────────────────────────┘
                              │
┌─────────────────────────────┴───────────────────────────────┐
│                    Capa de Persistencia                      │
│  ┌──────────────────────┐        ┌─────────────────────┐   │
│  │    PostgreSQL DB     │        │    Redis Cache      │   │
│  └──────────────────────┘        └─────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

### 2.2 Funciones del Producto

Las funciones principales del sistema incluyen:

1. **Monitoreo Automatizado de Noticias**
   - Recopilación automática de artículos de fuentes configuradas
   - Detección de duplicados y contenido relevante
   - Respeto de políticas de robots.txt y términos de servicio

2. **Análisis Inteligente de Contenido**
   - Análisis de sentimiento (positivo, neutral, negativo)
   - Clasificación temática (prevención, tratamiento, investigación, etc.)
   - Extracción de palabras clave y entidades

3. **Visualización y Analytics**
   - Dashboard en tiempo real con métricas agregadas
   - Gráficos de tendencias temporales
   - Mapas geográficos de distribución de noticias

4. **Gestión y Administración**
   - Panel de administración para gestión de fuentes
   - Sistema de compliance y validación legal
   - Herramientas CLI para operaciones avanzadas

### 2.3 Características de los Usuarios

**[PENDIENTE: Información requerida del usuario]**

Tipos de usuarios identificados preliminarmente:
- Administradores del sistema
- Analistas de contenido
- Usuarios de consulta

### 2.4 Restricciones

1. **Restricciones Técnicas:**
   - Python 3.13+ requerido para el backend
   - Node.js 18+ para el frontend
   - PostgreSQL 13+ como base de datos principal
   - Contenedores Docker para despliegue

2. **Restricciones Legales:**
   - Cumplimiento con políticas de robots.txt
   - Respeto de términos de servicio de fuentes
   - Aplicación de principios de Fair Use
   - Protección de datos personales

3. **Restricciones de Diseño:**
   - Arquitectura de microservicios
   - API RESTful para comunicación
   - Interfaz responsive para múltiples dispositivos

### 2.5 Suposiciones y Dependencias

**Suposiciones:**
- Disponibilidad continua de las fuentes de noticias externas
- Acceso estable a Internet para web scraping
- Disponibilidad de OpenAI API para procesamiento avanzado

**Dependencias:**
- Beautiful Soup y Playwright para web scraping
- Spacy y VADER para análisis de sentimiento
- FastAPI para el servidor de API
- React para la interfaz de usuario
- PostgreSQL para almacenamiento de datos

---

## 3. Requerimientos Funcionales

### 3.1 Gestión de Fuentes de Noticias

**RF-3.1.1** El sistema debe permitir crear nuevas fuentes de noticias con los siguientes campos obligatorios:
- Nombre de la fuente
- URL base
- País
- Idioma
- Email de contacto legal

**RF-3.1.2** El sistema debe validar automáticamente el cumplimiento legal de cada fuente:
- Verificación de robots.txt
- Análisis de términos de servicio
- Cálculo de score de compliance (0.00 a 1.00)

**RF-3.1.3** El sistema debe rechazar automáticamente fuentes con compliance score < 0.5

**RF-3.1.4** El sistema debe permitir operaciones CRUD completas sobre fuentes existentes

**RF-3.1.5** El sistema debe mantener un registro de auditoría de todos los cambios en fuentes

### 3.2 Web Scraping Automatizado

**RF-3.2.1** El sistema debe generar automáticamente scrapers específicos para cada fuente basándose en:
- Detección del CMS (WordPress, Drupal, etc.)
- Análisis de la estructura HTML
- Patrones de contenido médico

**RF-3.2.2** El sistema debe respetar el crawl delay especificado en robots.txt (mínimo 2 segundos)

**RF-3.2.3** El sistema debe extraer de cada artículo:
- Título
- Contenido (respetando limitaciones de copyright)
- Fecha de publicación
- URL original
- Metadatos relevantes

**RF-3.2.4** El sistema debe detectar y evitar contenido duplicado mediante hash de contenido

**RF-3.2.5** El sistema debe ejecutar scrapers de forma programada o bajo demanda

### 3.3 Análisis de Sentimiento y NLP

**RF-3.3.1** El sistema debe analizar el sentimiento de cada artículo generando:
- Score numérico (-1.000 a 1.000)
- Etiqueta categórica (positivo, neutral, negativo)
- Nivel de confianza (0.00 a 1.00)

**RF-3.3.2** El sistema debe clasificar artículos en categorías temáticas:
- Prevención
- Tratamiento
- Diagnóstico
- Testimonios
- Investigación
- Ensayos clínicos
- Otros

**RF-3.3.3** El sistema debe extraer palabras clave relevantes con sus tipos:
- Términos médicos
- Medicamentos
- Procedimientos
- Organizaciones
- Personas
- Ubicaciones

**RF-3.3.4** El sistema debe soportar análisis en español e inglés

### 3.4 Dashboard de Visualización

**RF-3.4.1** El sistema debe proporcionar una interfaz web responsive con tres vistas:
- Dashboard principal (legacy)
- Panel de administración
- Dashboard moderno (futuro)

**RF-3.4.2** El dashboard debe mostrar en tiempo real:
- Total de artículos procesados
- Distribución de sentimientos
- Tendencias temporales
- Top de palabras clave
- Mapa geográfico de noticias

**RF-3.4.3** El sistema debe permitir filtrar información por:
- Rango de fechas
- Fuente de noticias
- Sentimiento
- Categoría temática
- País/Región

**RF-3.4.4** El sistema debe actualizar los datos sin recargar la página (SPA)

### 3.5 Sistema de Exportación

**RF-3.5.1** El sistema debe exportar datos en formato CSV con todos los campos de artículos

**RF-3.5.2** El sistema debe exportar en Excel con múltiples hojas:
- Resumen ejecutivo
- Listado de artículos
- Análisis de sentimientos
- Palabras clave

**RF-3.5.3** El sistema debe generar reportes PDF con:
- Gráficos de visualización
- Tablas de datos
- Resumen estadístico

**RF-3.5.4** El sistema debe exportar gráficos como imágenes PNG

**RF-3.5.5** Las exportaciones deben respetar los filtros aplicados en el dashboard

### 3.6 Gestión de Usuarios y Autenticación

**RF-3.6.1** El sistema debe implementar autenticación basada en JWT

**RF-3.6.2** El sistema debe soportar los siguientes roles:
- Administrador (acceso total)
- Analista (lectura y exportación)
- Demo (acceso limitado)

**RF-3.6.3** El sistema debe crear automáticamente un usuario administrador en la primera ejecución

**RF-3.6.4** El sistema debe permitir gestión CRUD de usuarios solo a administradores

**RF-3.6.5** Los tokens JWT deben expirar después de 24 horas

### 3.7 CLI de Administración

**RF-3.7.1** El CLI debe proporcionar comandos para:
- Gestión de fuentes
- Ejecución de scrapers
- Gestión de usuarios
- Monitoreo de compliance
- Verificación de estado del sistema

**RF-3.7.2** El CLI debe soportar operaciones batch para procesamiento masivo

**RF-3.7.3** El CLI debe proporcionar salida formateada y códigos de retorno estándar

---

## 4. Requerimientos No Funcionales

### 4.1 Requisitos de Rendimiento

**[PENDIENTE: Información específica requerida del usuario]**

**RNF-4.1.1** El sistema debe procesar al menos 100 artículos por minuto

**RNF-4.1.2** El dashboard debe cargar en menos de 3 segundos

**RNF-4.1.3** Las consultas a la API deben responder en menos de 1 segundo

**RNF-4.1.4** El sistema debe soportar al menos 50 usuarios concurrentes

**RNF-4.1.5** El análisis NLP debe completarse en menos de 2 segundos por artículo

### 4.2 Requisitos de Seguridad

**RNF-4.2.1** Todas las contraseñas deben almacenarse con hash bcrypt

**RNF-4.2.2** La comunicación API debe usar HTTPS en producción

**RNF-4.2.3** El sistema debe validar y sanitizar todas las entradas de usuario

**RNF-4.2.4** Los logs no deben contener información sensible

**RNF-4.2.5** El sistema debe implementar rate limiting en endpoints públicos

### 4.3 Requisitos de Fiabilidad

**[PENDIENTE: Nivel de disponibilidad requerido]**

**RNF-4.3.1** El sistema debe tener una disponibilidad mínima del 99%

**RNF-4.3.2** El sistema debe recuperarse automáticamente de fallos de scraping

**RNF-4.3.3** Los datos deben respaldarse diariamente

**RNF-4.3.4** El sistema debe mantener logs de auditoría por al menos 90 días

### 4.4 Requisitos de Mantenibilidad

**RNF-4.4.1** El código debe mantener una cobertura de tests mínima del 85%

**RNF-4.4.2** El código debe seguir los estándares PEP8 (Python) y ESLint (JavaScript)

**RNF-4.4.3** Toda la API debe estar documentada con OpenAPI/Swagger

**RNF-4.4.4** Los componentes deben estar desacoplados mediante interfaces

### 4.5 Requisitos de Portabilidad

**RNF-4.5.1** El sistema debe ser desplegable mediante Docker

**RNF-4.5.2** El sistema debe funcionar en Linux, macOS y Windows (mediante Docker)

**RNF-4.5.3** La base de datos debe ser portable mediante dumps SQL estándar

**RNF-4.5.4** El frontend debe ser compatible con navegadores modernos (Chrome, Firefox, Safari, Edge)

---

## 5. Requerimientos de Interfaz

### 5.1 Interfaces de Usuario

**RI-5.1.1** Dashboard Principal (Legacy)
- Tema rosa-azul médico
- Diseño responsive con breakpoints en 768px y 1024px
- Navegación mediante tabs
- Gráficos interactivos con Recharts
- Idioma: Español

**RI-5.1.2** Panel de Administración
- Acceso mediante /admin
- Tablas con paginación y búsqueda
- Formularios modales para CRUD
- Validación en tiempo real
- Confirmación para acciones destructivas

**RI-5.1.3** Dashboard Moderno (Futuro)
- Diseño profesional médico
- Componentes accesibles (WCAG 2.1)
- Tema claro/oscuro
- Internacionalización preparada

### 5.2 Interfaces de Hardware

**RI-5.2.1** Servidor de Aplicación
- Mínimo 4 CPU cores
- Mínimo 8GB RAM
- 50GB almacenamiento SSD
- Conexión de red estable

**RI-5.2.2** Cliente
- Cualquier dispositivo con navegador web moderno
- Resolución mínima 1024x768
- Conexión a Internet

### 5.3 Interfaces de Software

**RI-5.3.1** Base de Datos
- PostgreSQL 13+ con extensión asyncpg
- Conexión mediante SQLAlchemy ORM

**RI-5.3.2** Cache
- Redis 5.2+ para caché de sesiones y resultados

**RI-5.3.3** Servicios Externos
- OpenAI API para procesamiento avanzado de texto
- Servicios de noticias mediante HTTP/HTTPS

**RI-5.3.4** Contenedores
- Docker 20+ y Docker Compose 2.0+

### 5.4 Interfaces de Comunicación

**RI-5.4.1** API REST
- Protocolo HTTP/HTTPS
- Formato JSON para request/response
- Autenticación mediante Bearer token (JWT)
- Versionado de API (/api/v1/)

**RI-5.4.2** WebSockets (Futuro)
- Para actualizaciones en tiempo real del dashboard

**RI-5.4.3** CLI
- Interfaz de línea de comandos con salida formateada
- Soporte para pipes y redirección estándar Unix

---

## 6. Apéndices

### 6.1 Arquitectura del Sistema

El sistema sigue una arquitectura de microservicios con los siguientes componentes:

1. **Frontend Layer**
   - React SPA con TypeScript
   - Vite como bundler
   - TanStack Query para estado del servidor
   - Tailwind CSS para estilos

2. **API Gateway**
   - FastAPI como framework principal
   - Middleware CORS configurado
   - Rate limiting y validación

3. **Microservicios**
   - **Scraper Service**: Web scraping con BeautifulSoup y Playwright
   - **NLP Service**: Análisis con Spacy y VADER
   - **Data Service**: Capa de acceso a datos con SQLAlchemy
   - **Analytics Service**: Agregación y cálculo de métricas
   - **Decision Engine**: Lógica de negocio y reglas
   - **Orchestrator**: Coordinación de pipeline
   - **Publisher**: Publicación de resultados
   - **Copywriter**: Generación de contenido

4. **Data Layer**
   - PostgreSQL para persistencia principal
   - Redis para caché y sesiones

### 6.2 Modelo de Datos

Entidades principales:

```
news_sources
├── id (PK)
├── name
├── base_url
├── language
├── country
├── compliance_score
└── [campos de compliance]

articles
├── id (PK)
├── source_id (FK)
├── title
├── url
├── content
├── sentiment_score
├── sentiment_label
├── topic_category
└── [metadatos]

article_keywords
├── id (PK)
├── article_id (FK)
├── keyword
├── relevance_score
└── keyword_type

users
├── id (PK)
├── username
├── email
├── hashed_password
└── [timestamps]

user_roles
├── user_id (FK)
└── role_id (FK)
```

### 6.3 Stack Tecnológico

**Backend:**
- Python 3.13+
- FastAPI 0.115.14
- SQLAlchemy 2.0.41
- Spacy 3.8.7
- VaderSentiment 3.3.2
- Beautiful Soup 4.13.4
- Playwright 1.51.0

**Frontend:**
- React 19.1.0
- TypeScript 5.8.3
- Vite 7.0.0
- TanStack Query 5.81.5
- Tailwind CSS 4.1.11
- Recharts 3.0.2

**Infraestructura:**
- Docker & Docker Compose
- PostgreSQL 13+
- Redis 5.2+
- Nginx (producción)

**Herramientas:**
- pytest (testing Python)
- Vitest (testing JavaScript)
- Black & isort (formateo Python)
- ESLint (linting JavaScript)
- Pre-commit hooks

---

## Estado del Documento

**NOTA:** Este documento está en estado BORRADOR y requiere la siguiente información del usuario para ser completado:

1. Perfiles detallados de usuarios y sus necesidades
2. Requisitos específicos de rendimiento (volumen de datos, usuarios concurrentes)
3. Nivel de disponibilidad requerido
4. Regulaciones de protección de datos aplicables
5. Alcance geográfico y lingüístico definitivo
6. Planes de integración con otros sistemas
7. Ventanas de mantenimiento aceptables

Una vez proporcionada esta información, se actualizarán las secciones correspondientes para crear la versión final del documento.
