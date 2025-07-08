# Manual de Usuario - Estrategia Modular
## PreventIA News Analytics Platform

---

**Metadata:**
- **Documento**: Estrategia de Desarrollo Manual de Usuario
- **Versión**: 1.0
- **Fecha**: 2025-07-08
- **Estado**: En Planificación
- **Audiencia**: Usuarios finales (público general)
- **Maintainer**: Equipo de Desarrollo

---

## 📋 Estrategia Modular Detallada

### 🎯 **Objetivo**
Crear un manual de usuario comprehensivo para PreventIA News Analytics que permita a usuarios no técnicos utilizar efectivamente la plataforma de análisis de noticias médicas.

### 🔧 **Enfoque Modular**
Desarrollo iterativo en 6 sesiones especializadas, cada una produciendo 2-3 páginas de documentación de alta calidad.

---

## 📚 **Estructura del Manual (6 Módulos)**

### **Módulo 1: Introducción y Primeros Pasos**
*Sesión 1 - Duración: 30-45 min*

**Contenido:**
- ¿Qué es PreventIA News Analytics?
- Beneficios para investigadores y profesionales médicos
- Cómo acceder a la plataforma (URLs, navegadores soportados)
- Tour del dashboard principal
- Navegación básica entre secciones

**Páginas objetivo:** 2-3 páginas
**Screenshots necesarios:** Dashboard principal, menú de navegación

---

### **Módulo 2: Análisis de Sentimientos**
*Sesión 2 - Duración: 30-45 min*

**Contenido:**
- Interpretación de gráficos de sentimientos
- Cómo leer distribuciones (positivo/negativo/neutro)
- Filtros de fecha y categoría
- Exportación de gráficos de sentimientos
- Casos de uso prácticos

**Páginas objetivo:** 2-3 páginas
**Screenshots necesarios:** LegacySentimentChart, filtros, opciones de exportación

---

### **Módulo 3: Gestión de Fuentes de Noticias**
*Sesión 3 - Duración: 30-45 min*

**Contenido:**
- Acceso al panel de administración (/admin)
- Visualización de fuentes configuradas
- Interpretación del compliance dashboard
- Monitoreo de estado de fuentes
- Interpretación de métricas de calidad

**Páginas objetivo:** 2-3 páginas
**Screenshots necesarios:** Admin interface, compliance dashboard, tabla de fuentes

---

### **Módulo 4: Exportación y Reportes**
*Sesión 4 - Duración: 30-45 min*

**Contenido:**
- Tipos de exportación disponibles (PDF, PNG, SVG)
- Cómo generar reportes de análisis
- Interpretación del historial de exportaciones
- Mejores prácticas para presentaciones
- Compartir resultados con colegas

**Páginas objetivo:** 2-3 páginas
**Screenshots necesarios:** Export modal, historial, ejemplos de reportes

---

### **Módulo 5: Análisis Geográfico y Temporal**
*Sesión 5 - Duración: 30-45 min*

**Contenido:**
- Interpretación del mapa geográfico
- Análisis de tendencias temporales
- Filtros avanzados por país/región
- Identificación de patrones estacionales
- Correlaciones geográfico-temporales

**Páginas objetivo:** 2-3 páginas
**Screenshots necesarios:** Geographic map, trend charts, filtros temporales

---

### **Módulo 6: Troubleshooting y FAQ**
*Sesión 6 - Duración: 30-45 min*

**Contenido:**
- Problemas comunes y soluciones
- Interpretación de mensajes de error
- Contacto para soporte técnico
- FAQ sobre funcionalidades
- Limitaciones conocidas y workarounds

**Páginas objetivo:** 2-3 páginas
**Screenshots necesarios:** Error messages, contact info

---

## 🛠️ **Especificaciones Técnicas**

### **Formato y Estructura**
- **Formato**: Markdown (.md) con conversión a PDF
- **Ubicación**: `docs/product/manual-usuario/`
- **Idioma**: Español (audiencia UCOMPENSAR)
- **Estilo**: Lenguaje claro, no técnico, orientado a resultados

### **Elementos Visuales**
- **Screenshots**: Resolución 1920x1080, formato PNG
- **Diagramas**: Simples, orientados a flujo de trabajo
- **Iconos**: Uso consistente de emojis para navegación
- **Colores**: Esquema médico (azules, verdes, coherente con UI)

### **Navegación**
- **Índice principal**: Links directos a cada módulo
- **Cross-references**: Enlaces entre módulos relacionados
- **Búsqueda**: Tags y keywords para fácil localización

---

## 📅 **Timeline de Desarrollo**

### **Fase 1: Preparación (1 sesión)**
- Captura de screenshots del sistema operativo
- Definición de casos de uso por módulo
- Setup de estructura de archivos

### **Fase 2: Desarrollo Modular (6 sesiones)**
- 1 módulo por sesión
- Revisión inmediata tras cada módulo
- Iteración basada en feedback

### **Fase 3: Integración (1 sesión)**
- Ensamblaje de módulos
- Índice general y navegación
- Review final y ajustes de coherencia

**Total estimado**: 8 sesiones (6-8 horas)

---

## 🎯 **Criterios de Éxito**

### **Métricas de Calidad**
- **Claridad**: Usuario no técnico puede seguir instrucciones sin ayuda
- **Completitud**: Cubre 100% de funcionalidades user-facing
- **Precisión**: Screenshots y procedimientos coinciden con sistema actual
- **Usabilidad**: Tiempo promedio de onboarding < 15 minutos

### **Validación**
- **Review técnico**: Verificación de precisión técnica
- **Review UX**: Evaluación de claridad para usuarios finales
- **Testing**: Prueba con usuario real (preferiblemente no técnico)

---

## 📝 **Plantilla por Módulo**

### **Estructura Estándar**
```markdown
# [Título del Módulo]

## ¿Qué aprenderás?
- Objetivo 1
- Objetivo 2
- Objetivo 3

## Paso a paso
### 1. [Acción principal]
[Descripción clara + screenshot]

### 2. [Siguiente acción]
[Descripción + screenshot]

## Casos de uso prácticos
- Escenario A: [Descripción]
- Escenario B: [Descripción]

## Preguntas frecuentes
- **P**: [Pregunta común]
- **R**: [Respuesta clara]

## Siguiente paso
👉 [Link al siguiente módulo]
```

---

## 🚀 **Próximos Pasos**

### **Inmediato (Próxima sesión)**
1. **Captura de screenshots**: Sistema operativo actual
2. **Inicio Módulo 1**: Introducción y Primeros Pasos
3. **Setup estructura**: Directorios y archivos base

### **Seguimiento**
- **1 módulo por sesión**: Desarrollo iterativo
- **Review continuo**: Ajustes basados en precisión técnica
- **Integration testing**: Validación con usuarios reales

---

**🎯 Objetivo final**: Manual de usuario completo, claro y actionable que reduzca el tiempo de onboarding de nuevos usuarios a menos de 15 minutos.
