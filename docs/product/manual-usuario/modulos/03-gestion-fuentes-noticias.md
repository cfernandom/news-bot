# Módulo 3: Gestión de Fuentes de Noticias
## Manual de Usuario - PreventIA News Analytics

---

## 🎯 ¿Qué aprenderás en este módulo?

Al completar este módulo serás capaz de:
- Acceder y navegar por el panel de administración de fuentes
- Interpretar el dashboard de compliance y calidad de fuentes
- Entender cómo se monitorean las 9 fuentes configuradas
- Interpretar métricas de compliance y validation status
- Evaluar la cobertura geográfica e idiomática del sistema
- Identificar oportunidades para nuevas fuentes de monitoreo

---

## 🌐 ¿Qué son las Fuentes de Noticias?

### **Definición**
Las **fuentes de noticias** son los sitios web especializados de donde PreventIA News Analytics recopila automáticamente artículos sobre cáncer de mama. Cada fuente ha sido:

- ✅ **Validada legalmente** para cumplir con robots.txt y términos de servicio
- ✅ **Verificada médicamente** como fuente confiable de información científica
- ✅ **Configurada técnicamente** con extractores especializados
- ✅ **Monitoreada continuamente** para garantizar calidad y compliance

### **¿Por qué es importante la gestión de fuentes?**

#### **🔍 Para Investigadores:**
- **Transparencia**: Saber exactamente de dónde provienen los datos
- **Calidad**: Asegurar que las fuentes sean médicamente confiables
- **Cobertura**: Evaluar representatividad geográfica e idiomática
- **Reproducibilidad**: Poder validar y replicar análisis

#### **👩‍💼 Para Administradores:**
- **Compliance**: Verificar cumplimiento legal y ético
- **Performance**: Monitorear funcionamiento de extractores
- **Expansión**: Identificar necesidades de nuevas fuentes
- **Mantenimiento**: Detectar fuentes problemáticas

#### **🎓 Para Estudiantes:**
- **Metodología**: Entender la base de datos utilizada
- **Sesgos**: Identificar potenciales limitaciones del dataset
- **Contexto**: Relacionar resultados con origen de los datos

---

## 🔑 Acceso al Panel de Administración

### **URL de Acceso**
```
🔗 Panel de Administración: http://localhost:5173/admin
```

### **🚀 Cómo Acceder**

#### **Paso 1: Navega a la URL Admin**
1. Desde el dashboard principal (`http://localhost:5173`)
2. Busca enlace "Admin" o "Administración" en el menú
3. O navega directamente a `http://localhost:5173/admin`

#### **Paso 2: Verificar Acceso**
Si tienes acceso correctamente, verás:
- ✅ **Dashboard de fuentes** con tabla de sitios web
- ✅ **Métricas de compliance** en la parte superior
- ✅ **Estado de validación** para cada fuente
- ✅ **Opciones de configuración** disponibles

> **💡 Nota**: Dependiendo de tu rol de usuario, algunas funciones pueden estar limitadas. Los usuarios básicos pueden ver información, mientras que administradores pueden modificar configuraciones.

---

## 📊 Dashboard de Compliance Verificado

### **Estado Actual del Sistema (2025-07-08)**
Basado en verificación directa de la base de datos operativa:

#### **📈 Métricas Generales**
- **Total de Fuentes**: 9 sitios web configurados
- **Status de Validación**: 8 fuentes validadas, 1 pendiente
- **Compliance Score Promedio**: 0.80/1.00 (excelente)
- **Cobertura Geográfica**: 3 regiones (EE.UU., Internacional, Reino Unido)

### **🌍 Distribución Geográfica Actual**

#### **Estados Unidos (4 fuentes - 44%)**
- **Breast Cancer Org** (`breastcancer.org`)
- **CureToday** (`curetoday.com`)
- **WebMD** (`webmd.com`)
- **Medical News Today** (`medicalnewstoday.com`)

#### **Internacional (4 fuentes - 44%)**
- **Medical Xpress** (`medicalxpress.com`)
- **News Medical** (`news-medical.net`)
- **Science Daily** (`sciencedaily.com`)
- **Nature** (`nature.com`)

#### **Reino Unido (1 fuente - 11%)**
- **Breast Cancer Now** (`breastcancernow.org`)

### **🏆 Compliance Scores Detallado**

| Fuente | Score | Interpretación |
|--------|-------|----------------|
| 8 fuentes principales | 0.80/1.00 | **Excelente compliance** |
| 1 fuente pendiente | Sin score | **En proceso de validación** |

**📊 Interpretación del Score 0.80:**
- ✅ **Robots.txt**: Cumplimiento verificado
- ✅ **Términos de servicio**: Revisados y compatibles
- ✅ **Rate limiting**: Respeta crawl delays
- ✅ **Fair use**: Uso académico justificado
- 🔄 **Monitoreo continuo**: Verificación automática

---

## 🔍 Interpretando la Tabla de Fuentes

### **Columnas Principales**

#### **🏷️ Nombre (Name)**
- **Propósito**: Identificación clara de la fuente
- **Ejemplo**: "Breast Cancer Org", "WebMD", "Nature"
- **Uso**: Referencia en reportes y análisis

#### **🌐 URL Base (Base URL)**
- **Propósito**: Dominio principal monitoreado
- **Ejemplo**: `https://www.breastcancer.org`
- **Importancia**: Define alcance de extracción

#### **🗺️ País/Región (Country)**
- **EE.UU.**: Fuentes estadounidenses especializadas
- **Internacional**: Alcance global, múltiples idiomas
- **Reino Unido**: Perspectiva europea especializada
- **Uso**: Análisis de sesgos geográficos

#### **✅ Estado de Validación**
- **"Validated"**: Fuente verificada y operativa
- **"Pending"**: En proceso de validación legal/técnica
- **"Error"**: Problemas detectados que requieren atención

#### **📊 Score de Compliance**
- **0.80+**: Excelente (cumple todos los criterios)
- **0.60-0.79**: Bueno (minor issues)
- **0.40-0.59**: Moderado (requiere revisión)
- **<0.40**: Problemático (requiere intervención)

---

## 🎯 Casos de Uso del Panel de Administración

### **Caso 1: Investigador Evaluando Calidad de Datos**

#### **Escenario:**
Necesitas determinar si tu análisis de sentimientos tiene sesgos geográficos significativos.

#### **Pasos en el Panel Admin:**
1. **Acceder a la tabla de fuentes**
2. **Analizar distribución geográfica**:
   - 44% EE.UU. (4 fuentes)
   - 44% Internacional (4 fuentes)
   - 11% Reino Unido (1 fuente)
3. **Evaluar compliance scores**: Todas las fuentes activas tienen 0.80
4. **Interpretar para tu investigación**:
   - Sesgo hacia perspectiva anglófona
   - Cobertura equilibrada EE.UU./Internacional
   - Representación limitada de Europa (solo Reino Unido)

#### **Aplicación:**
- Documentar limitaciones metodológicas en tu estudio
- Sugerir inclusión de fuentes españolas/latinoamericanas
- Interpretar resultados considerando el sesgo identificado

### **Caso 2: Administrador Monitoreando Sistema**

#### **Escenario:**
Verificación rutinaria del estado del sistema y identificación de problemas.

#### **Pasos en el Panel Admin:**
1. **Revisar scores de compliance**:
   - Verificar que todas las fuentes mantengan score ≥0.80
   - Identificar cualquier fuente con score decreciente
2. **Verificar estados de validación**:
   - Confirmar que fuentes "Pending" no permanezcan así indefinidamente
   - Investigar fuentes con estado "Error"
3. **Monitorear cobertura geográfica**:
   - Evaluar si la distribución actual es apropiada
   - Identificar regiones sub-representadas

#### **Aplicación:**
- Planificar mantenimiento de fuentes problemáticas
- Proponer expansión a nuevas regiones geográficas
- Reportar estado del sistema a stakeholders

### **Caso 3: Estudiante Analizando Metodología**

#### **Escenario:**
Necesitas documentar la metodología de recolección de datos para tu tesis.

#### **Pasos en el Panel Admin:**
1. **Documentar lista completa de fuentes**:
   - 9 fuentes especializadas en cancer research
   - Mix de fuentes académicas (Nature) y divulgativas (WebMD)
2. **Registrar criterios de calidad**:
   - Compliance score promedio: 0.80/1.00
   - 100% de fuentes validadas legalmente
3. **Analizar representatividad**:
   - Cobertura idiomática: Principalmente inglés
   - Alcance geográfico: EE.UU., Internacional, Reino Unido

#### **Aplicación:**
- Sección "Metodología" de tu tesis con datos precisos
- Sección "Limitaciones" documentando sesgos identificados
- Justificación de representatividad del dataset

---

## 🔧 Funcionalidades del Panel Admin

### **👀 Funciones de Visualización (Todos los usuarios)**

#### **📊 Dashboard General**
- **Métricas de compliance** en tiempo real
- **Estado de todas las fuentes** en tabla organizada
- **Distribución geográfica** visual
- **Histórico de validaciones** por fuente

#### **🔍 Detalles por Fuente**
- **Información técnica**: URL, extractor class, configuración
- **Compliance detail**: Robots.txt, terms of service, crawl delays
- **Historial de validación**: Fechas, resultados, errores
- **Métricas de performance**: Artículos extraídos, success rate

### **⚙️ Funciones de Configuración (Solo administradores)**

#### **➕ Añadir Nueva Fuente**
- **Configuración básica**: Nombre, URL, país, idioma
- **Validación automática**: Verificación de robots.txt y términos
- **Configuración técnica**: Selección de extractor, parámetros
- **Testing inicial**: Prueba de extracción antes de activar

#### **✏️ Editar Fuente Existente**
- **Actualizar información**: Cambios en URL, configuración
- **Recalibrar extractor**: Ajustes por cambios en el sitio web
- **Actualizar compliance**: Re-verificar términos y robots.txt
- **Activar/desactivar**: Control de fuentes temporalmente problemáticas

#### **🗑️ Gestión de Fuentes**
- **Desactivar fuentes**: Mantener historial pero pausar extracción
- **Eliminar fuentes**: Removal completo (afecta datos históricos)
- **Backup de configuración**: Export/import de configuraciones

---

## 🚨 Interpretando Alertas y Estados

### **🟢 Estados Saludables**

#### **"Validated" + Score 0.80**
- **Significado**: Fuente completamente operativa y cumple todos los criterios
- **Acción requerida**: Ninguna, monitoreo rutinario
- **Frecuencia**: La mayoría de fuentes deben mantener este estado

#### **"Validated" + Score 0.60-0.79**
- **Significado**: Fuente operativa con minor compliance issues
- **Acción requerida**: Revisar periódicamente, considerar mejoras
- **Frecuencia**: Aceptable ocasionalmente

### **🟡 Estados de Atención**

#### **"Pending" + Sin Score**
- **Significado**: Fuente en proceso de validación inicial
- **Acción requerida**: Monitorear progreso, intervenir si se extiende
- **Tiempo esperado**: 24-48 horas para validación automática

#### **"Validated" + Score <0.60**
- **Significado**: Problemas de compliance que requieren atención
- **Acción requerida**: Investigar issues específicos, considerar correcciones
- **Urgencia**: Moderada, abordar en próxima ventana de mantenimiento

### **🔴 Estados Problemáticos**

#### **"Error" + Cualquier Score**
- **Significado**: Problemas técnicos o legales detectados
- **Acción requerida**: Investigación inmediata y corrección
- **Impacto**: Fuente no contribuye datos hasta resolución

#### **"Validated" + Score <0.40**
- **Significado**: Compliance severamente comprometido
- **Acción requerida**: Revisión legal/técnica urgente
- **Consideración**: Evaluación de desactivación temporal

---

## 📋 Ejercicio Práctico: Evaluación de Fuentes

### **Escenario: Análisis de Representatividad Geográfica**
Como investigador, necesitas evaluar si las fuentes actuales proporcionan una perspectiva geográficamente equilibrada para tu estudio sobre percepciones globales del cáncer de mama.

### **Paso 1: Acceso y Navegación**
1. **Navega al panel admin**: `http://localhost:5173/admin`
2. **Localiza la tabla de fuentes** en el dashboard principal
3. **Identifica las columnas clave**: Name, Base URL, Country, Validation Status

### **Paso 2: Análisis de Distribución Geográfica**
1. **Cuenta fuentes por región**:
   - Estados Unidos: ¿Cuántas fuentes?
   - Internacional: ¿Cuántas fuentes?
   - Reino Unido: ¿Cuántas fuentes?
   - Otras regiones: ¿Faltan regiones importantes?

2. **Evalúa tipos de fuentes**:
   - Académicas vs divulgativas
   - Especializadas vs generalistas
   - Institucionales vs comerciales

### **Paso 3: Análisis de Calidad**
1. **Revisar compliance scores**:
   - ¿Todas las fuentes tienen score ≥0.80?
   - ¿Hay fuentes con scores problemáticos?
   - ¿El promedio es aceptable para investigación académica?

2. **Verificar estados de validación**:
   - ¿Cuántas fuentes están "Validated"?
   - ¿Hay fuentes "Pending" o "Error"?
   - ¿Afecta esto la representatividad del dataset?

### **Paso 4: Identificación de Brechas**
1. **Regiones sub-representadas**:
   - ¿Faltan fuentes de Latinoamérica?
   - ¿Hay representación asiática?
   - ¿Se incluyen perspectivas africanas?

2. **Idiomas limitados**:
   - ¿Todas las fuentes son en inglés?
   - ¿Limita esto la generalización de resultados?
   - ¿Afecta el tipo de pacientes representados?

### **Paso 5: Documentación de Hallazgos**
**Completa esta evaluación:**

```
📊 EVALUACIÓN DE REPRESENTATIVIDAD GEOGRÁFICA

Distribución Actual:
- Estados Unidos: [X] fuentes ([X]%)
- Internacional: [X] fuentes ([X]%)
- Reino Unido: [X] fuentes ([X]%)

Calidad del Sistema:
- Compliance promedio: [X]/1.00
- Fuentes validadas: [X]/9 ([X]%)
- Fuentes problemáticas: [X]

Brechas Identificadas:
1. [Describe limitación geográfica]
2. [Describe limitación idiomática]
3. [Describe limitación de tipo de fuente]

Recomendaciones:
1. [Sugerencia de nueva región/fuente]
2. [Sugerencia de mejora de diversity]
3. [Sugerencia metodológica para tu estudio]

Impacto en mi Investigación:
- Fortalezas del dataset actual: [X]
- Limitaciones a documentar: [X]
- Ajustes metodológicos necesarios: [X]
```

### **Resultado Esperado**
Al completar este ejercicio tendrás:
- ✅ **Comprensión clara** de la composición del dataset
- ✅ **Identificación de sesgos** geográficos y metodológicos
- ✅ **Documentación precisa** para tu metodología de investigación
- ✅ **Recomendaciones informadas** para mejoras del sistema

---

## ❓ Preguntas Frecuentes del Módulo 3

### **🔐 Acceso y Permisos**

**P: No puedo acceder al panel de administración, ¿qué hago?**
**R:** Verifica que:
- La URL sea correcta: `http://localhost:5173/admin`
- Tu cuenta tenga permisos de administrador
- El servicio frontend esté ejecutándose correctamente
- Contacta al administrador técnico si persiste el problema

**P: Veo la información pero no puedo modificar fuentes**
**R:** Es normal si tienes rol de usuario básico. Solo administradores pueden modificar configuraciones. Puedes ver toda la información para análisis e investigación.

### **📊 Interpretación de Métricas**

**P: ¿Un compliance score de 0.80 es bueno?**
**R:** Sí, es excelente. Los scores de compliance van de 0.00 a 1.00:
- 0.80+: Excelente compliance
- 0.60-0.79: Bueno
- 0.40-0.59: Aceptable
- <0.40: Problemático

**P: ¿Qué significa que una fuente esté "Pending"?**
**R:** Está en proceso de validación inicial. Esto incluye verificación de robots.txt, términos de servicio, y configuración técnica. Normalmente se resuelve en 24-48 horas.

**P: ¿Por qué casi todas las fuentes son en inglés?**
**R:** Refleja la realidad de la literatura médica especializada, donde el inglés es predominante. Para estudios que requieran perspectivas multiidioma, documenta esta limitación en tu metodología.

### **🌍 Representatividad Geográfica**

**P: ¿El sesgo hacia fuentes estadounidenses afecta mi investigación?**
**R:** Potencialmente sí. Documenta esto como limitación metodológica y considera:
- Si tu estudio es específico para contexto estadounidense, es apropiado
- Si buscas perspectiva global, nota la sub-representación de otras regiones
- Interpreta resultados considerando este sesgo

**P: ¿Puedo solicitar que se añadan fuentes de mi región?**
**R:** Sí, puedes solicitar nuevas fuentes al equipo técnico. Proporciona:
- URL de la fuente propuesta
- Justificación de su relevancia médica
- Verificación de que permite web scraping
- Idioma y región que representaría

### **🔧 Aspectos Técnicos**

**P: ¿Qué es un "extractor class"?**
**R:** Es el componente técnico que sabe cómo extraer información específicamente de cada sitio web. Cada fuente requiere su propio extractor porque los sitios web tienen estructuras diferentes.

**P: ¿Con qué frecuencia se actualizan los compliance scores?**
**R:** Automáticamente cada 24-48 horas. Los scores pueden cambiar si los sitios web modifican sus robots.txt, términos de servicio, o estructura técnica.

---

## 🎯 Resumen del Módulo 3

### ✅ **Has Aprendido:**
- Acceder y navegar por el panel de administración de fuentes
- Interpretar dashboard de compliance con 9 fuentes configuradas
- Entender distribución geográfica (44% EE.UU., 44% Internacional, 11% Reino Unido)
- Interpretar compliance scores (promedio 0.80/1.00 = excelente)
- Evaluar representatividad y identificar sesgos potenciales
- Documentar limitaciones metodológicas para investigación

### 📊 **Datos Verificados del Sistema:**
- **9 fuentes activas** con alta calidad (8 validadas, 1 pendiente)
- **Compliance score promedio**: 0.80/1.00 (excelente)
- **Cobertura geográfica**: 3 regiones principales
- **Tipos de fuentes**: Mix académico-divulgativo balanceado

### 📋 **Checklist de Progreso:**
- [ ] Accedí al panel de administración exitosamente
- [ ] Interpreté la tabla de fuentes y sus columnas principales
- [ ] Analicé la distribución geográfica de las 9 fuentes
- [ ] Evalué compliance scores y estados de validación
- [ ] Identifiqué potenciales sesgos y limitaciones
- [ ] Documenté hallazgos para uso en mi investigación

---

## 👉 Siguiente Paso

**📤 Módulo 4: Exportación y Reportes**

En el próximo módulo aprenderás a:
- Generar reportes profesionales en PDF, PNG y SVG
- Interpretar y gestionar el historial de exportaciones
- Personalizar reportes para diferentes audiencias (académica, ejecutiva, pública)
- Aplicar mejores prácticas para presentaciones y publicaciones
- Compartir resultados efectivamente con colegas y stakeholders

---

**🔗 Enlaces Útiles:**
- **Panel de Administración**: http://localhost:5173/admin
- **Dashboard Principal**: http://localhost:5173
- **Módulo Anterior**: [Análisis de Sentimientos](02-analisis-sentimientos.md)
- **Índice General**: [Manual de Usuario](../indice-principal.md)

**💡 Tip**: Familiarízate con la distribución geográfica actual de fuentes antes de continuar, ya que esta información será relevante para interpretar correctamente los análisis geográficos en módulos posteriores.
