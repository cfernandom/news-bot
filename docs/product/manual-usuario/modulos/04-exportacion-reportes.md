# Módulo 4: Exportación y Reportes
## Manual de Usuario - PreventIA News Analytics

---

## 🎯 ¿Qué aprenderás en este módulo?

Al completar este módulo serás capaz de:
- Generar reportes profesionales en múltiples formatos (CSV, XLSX, PNG, SVG, PDF)
- Interpretar y gestionar el historial de exportaciones
- Personalizar reportes para diferentes audiencias (académica, ejecutiva, pública)
- Aplicar mejores prácticas para presentaciones y publicaciones
- Compartir resultados efectivamente con colegas y stakeholders
- Optimizar el flujo de trabajo de exportación para investigación

---

## 📊 ¿Qué tipos de exportaciones están disponibles?

### **Sistema de Exportación Verificado**
PreventIA News Analytics incluye un **sistema completo de exportación** con 7 tipos de reportes diferentes, cada uno optimizado para casos de uso específicos.

### **📁 Formatos de Datos**

#### **📋 CSV (Comma-Separated Values)**
- **Mejor para**: Análisis estadístico en Excel, R, Python, SPSS
- **Contenido**: Datos tabulares de artículos con metadatos completos
- **Tamaño**: Liviano, fácil de manipular
- **Uso típico**: Import en software estadístico para análisis cuantitativo

#### **📊 XLSX (Microsoft Excel)**
- **Mejor para**: Reportes ejecutivos, análisis exploratorio, presentaciones
- **Contenido**: Datos formateados con hojas múltiples
- **Ventajas**: Formato familiar, funciones de Excel disponibles
- **Uso típico**: Reportes para stakeholders no técnicos

### **🖼️ Formatos Visuales**

#### **📈 PNG (Gráficos de Alta Resolución)**
- **Mejor para**: Presentaciones, documentos Word, reportes impresos
- **Calidad**: 300 DPI, óptimo para impresión
- **Tipos de gráficos**: Sentimientos, temas, tendencias temporales
- **Uso típico**: Slides de PowerPoint, informes ejecutivos

#### **🎨 SVG (Gráficos Vectoriales)**
- **Mejor para**: Publicaciones académicas, documentos escalables
- **Ventaja**: Calidad infinita, redimensionable sin pérdida
- **Tipos de gráficos**: Todos los disponibles en PNG
- **Uso típico**: Papers científicos, posters médicos, tesis

### **📄 Formatos de Reportes Completos**

#### **📋 PDF (Reportes Profesionales)**
- **Mejor para**: Documentos formales, archivos permanentes
- **Contenido**: Análisis completo con gráficos + interpretación + metadatos
- **Características**: Formato profesional, fácil de compartir
- **Uso típico**: Reportes trimestrales, estudios de caso, documentación oficial

---

## 🔗 Endpoints de Exportación Disponibles

### **Base URL del Sistema de Exportación**
```
🔗 Base: http://localhost:8000/api/v1/export/
```

### **📊 Exportaciones de Datos**

#### **CSV de Noticias**
```
📋 Endpoint: GET /api/v1/export/news.csv
📝 Descripción: Dataset completo en formato CSV
💾 Tamaño típico: ~50KB para 106 artículos
⚡ Velocidad: Generación en <2 segundos
```

#### **Excel de Noticias**
```
📊 Endpoint: GET /api/v1/export/news.xlsx
📝 Descripción: Dataset formateado para Excel
💾 Tamaño típico: ~75KB para 106 artículos
⚡ Velocidad: Generación en <3 segundos
```

### **🖼️ Exportaciones de Gráficos**

#### **Gráficos PNG (Alta Resolución)**
```
📈 Sentimientos: GET /api/v1/export/charts/sentiment.png
📊 Temas: GET /api/v1/export/charts/topics.png
📅 Timeline: GET /api/v1/export/charts/timeline.png
```

#### **Gráficos SVG (Vectoriales)**
```
🎨 Sentimientos: GET /api/v1/export/charts/sentiment.svg
🎨 Temas: GET /api/v1/export/charts/topics.svg
🎨 Timeline: GET /api/v1/export/charts/timeline.svg
```

### **📄 Reportes Completos**
```
📋 Reporte PDF: POST /api/v1/export/report
📝 Descripción: Reporte completo con análisis integrado
💾 Tamaño típico: ~500KB - 2MB dependiendo de gráficos
⚡ Velocidad: Generación en <10 segundos
```

### **🗂️ Gestión de Exportaciones**
```
📋 Historial usuario: GET /api/v1/export/user/exports
📊 Estadísticas: GET /api/v1/export/exports/stats
```

---

## 🎯 Casos de Uso por Tipo de Exportación

### **🔬 Para Investigadores Académicos**

#### **Caso: Análisis Estadístico Avanzado**
**Objetivo**: Realizar análisis cuantitativo de sentimientos para paper científico

**Flujo de trabajo:**
1. **Exportar datos**: `GET /api/v1/export/news.csv`
2. **Importar en R/Python**: Análisis estadístico personalizado
3. **Exportar gráficos**: `GET /api/v1/export/charts/sentiment.svg`
4. **Integrar en paper**: SVG para máxima calidad de publicación

**Beneficios:**
- Control total sobre análisis estadístico
- Gráficos de calidad de publicación académica
- Datos trazables y reproducibles

#### **Caso: Tesis de Posgrado**
**Objetivo**: Documentar metodología y resultados para tesis doctoral

**Flujo de trabajo:**
1. **Exportar dataset**: CSV para documentar muestra exacta
2. **Generar gráficos**: SVG para figuras de tesis
3. **Crear reporte**: PDF como evidencia de análisis
4. **Documentar fuentes**: Historial de exportaciones como anexo

### **👨‍💼 Para Ejecutivos y Gestores**

#### **Caso: Reporte Mensual para Dirección**
**Objetivo**: Presentar tendencias de sentimientos en formato ejecutivo

**Flujo de trabajo:**
1. **Generar reporte PDF**: Documento completo con interpretación
2. **Exportar gráficos PNG**: Para slides de presentación
3. **Exportar Excel**: Para manipulación adicional del equipo
4. **Presentar insights**: Focus en implicaciones estratégicas

**Beneficios:**
- Formato familiar para audiencia ejecutiva
- Visualizaciones claras y profesionales
- Datos adicionales disponibles para deep dive

#### **Caso: Evaluación de Campañas de Salud Pública**
**Objetivo**: Medir impacto mediático de campaña de concienciación

**Flujo de trabajo:**
1. **Filtrar por período**: Antes, durante, después de campaña
2. **Exportar análisis temporal**: Timeline charts en PNG
3. **Comparar sentimientos**: Múltiples exports por período
4. **Consolidar hallazgos**: Reporte PDF final

### **🎓 Para Estudiantes de Medicina**

#### **Caso: Proyecto de Investigación Formativa**
**Objetivo**: Analizar evolución de narrativas médicas para proyecto final

**Flujo de trabajo:**
1. **Exportar datos básicos**: Excel para análisis exploratorio
2. **Generar visualizaciones**: PNG para presentación en clase
3. **Documentar proceso**: Historial de exportaciones como metodología
4. **Crear presentación**: Combinar gráficos con análisis textual

**Beneficios:**
- Proceso de aprendizaje estructurado
- Experiencia con herramientas de investigación real
- Resultados presentables en contexto académico

---

## 📋 Guía Paso a Paso: Tu Primera Exportación

### **Ejercicio Práctico: Generar Reporte de Sentimientos Completo**

#### **Objetivo del Ejercicio**
Crear un paquete de exportaciones completo que incluya datos, visualizaciones y reporte para presentar análisis de sentimientos en noticias de cáncer de mama.

#### **Paso 1: Preparación**
1. **Verificar acceso al sistema**:
   - Dashboard: `http://localhost:5173`
   - API: `http://localhost:8000`
2. **Identificar tu caso de uso**:
   - ¿Presentación ejecutiva, análisis académico, o proyecto estudiantil?
   - ¿Audiencia técnica o no técnica?
3. **Definir período de análisis**:
   - ¿Datos de todo el período disponible?
   - ¿Filtro temporal específico?

#### **Paso 2: Exportar Dataset Base**
1. **Abrir nueva pestaña del navegador**
2. **Navegar a**: `http://localhost:8000/api/v1/export/news.csv`
3. **Guardar archivo** como: `preventia_dataset_[fecha].csv`
4. **Verificar descarga**:
   - Tamaño esperado: ~50KB
   - Número de filas: ~107 (header + 106 artículos)

#### **Paso 3: Generar Gráfico de Sentimientos**

**Para Presentaciones (PNG):**
1. **Navegar a**: `http://localhost:8000/api/v1/export/charts/sentiment.png`
2. **Guardar imagen** como: `sentimientos_analisis_[fecha].png`
3. **Verificar calidad**: 300 DPI, alta resolución

**Para Publicaciones Académicas (SVG):**
1. **Navegar a**: `http://localhost:8000/api/v1/export/charts/sentiment.svg`
2. **Guardar imagen** como: `sentimientos_analisis_[fecha].svg`
3. **Verificar escalabilidad**: Calidad vectorial infinita

#### **Paso 4: Generar Gráfico de Temas**
1. **PNG**: `http://localhost:8000/api/v1/export/charts/topics.png`
2. **SVG**: `http://localhost:8000/api/v1/export/charts/topics.svg`
3. **Guardar** con nomenclatura consistente

#### **Paso 5: Exportar Datos Estructurados (Excel)**
1. **Navegar a**: `http://localhost:8000/api/v1/export/news.xlsx`
2. **Guardar archivo** como: `preventia_dataset_[fecha].xlsx`
3. **Abrir en Excel** para verificar formato

#### **Paso 6: Verificar Historial de Exportaciones**
1. **Navegar a**: `http://localhost:8000/api/v1/export/user/exports`
2. **Verificar** que aparezcan tus exportaciones recientes
3. **Documentar** IDs de exportación para trazabilidad

### **Resultado del Ejercicio**
Al completar tendrás:
- ✅ **Dataset CSV**: Para análisis estadístico
- ✅ **Dataset Excel**: Para exploración y manipulación
- ✅ **Gráficos PNG**: Para presentaciones
- ✅ **Gráficos SVG**: Para publicaciones académicas
- ✅ **Historial**: Registro de exportaciones realizadas

### **Tiempo Estimado**: 10-15 minutos

---

## 🎨 Mejores Prácticas de Exportación

### **📁 Organización de Archivos**

#### **Estructura de Directorios Recomendada**
```
proyecto_preventia/
├── datos/
│   ├── preventia_dataset_2025-01-08.csv
│   └── preventia_dataset_2025-01-08.xlsx
├── graficos/
│   ├── png/
│   │   ├── sentimientos_2025-01-08.png
│   │   └── temas_2025-01-08.png
│   └── svg/
│       ├── sentimientos_2025-01-08.svg
│       └── temas_2025-01-08.svg
├── reportes/
│   └── analisis_completo_2025-01-08.pdf
└── documentacion/
    └── historial_exportaciones.txt
```

#### **Nomenclatura Consistente**
```
Formato recomendado:
[tipo]_[categoria]_[fecha].[extension]

Ejemplos:
- dataset_completo_2025-01-08.csv
- grafico_sentimientos_2025-01-08.png
- reporte_mensual_enero_2025.pdf
```

### **🎯 Por Tipo de Audiencia**

#### **📚 Academia/Investigación**
- **Formatos**: SVG + CSV + documentación completa
- **Prioridad**: Reproducibilidad y trazabilidad
- **Extras**: Metadatos, versiones, changelog

#### **👨‍💼 Ejecutivos/Gestores**
- **Formatos**: PDF + PNG + Excel (opcional)
- **Prioridad**: Claridad visual y insights accionables
- **Extras**: Resumen ejecutivo, recomendaciones

#### **🎓 Estudiantes/Formación**
- **Formatos**: PNG + Excel + proceso documentado
- **Prioridad**: Comprensión del proceso y learning
- **Extras**: Pasos de metodología, interpretaciones

### **📊 Por Caso de Uso**

#### **📖 Publicaciones Científicas**
```
Checklist de exportación:
☐ SVG de alta calidad para figuras
☐ CSV con datos exactos para reproducibilidad
☐ Metadatos completos (fechas, versiones, filtros)
☐ Documentación de metodología de extracción
☐ Compliance con estándares de data sharing
```

#### **📑 Presentaciones Corporativas**
```
Checklist de exportación:
☐ PNG optimizado para proyectores (1920x1080)
☐ Colores corporativos y branding consistente
☐ Gráficos autoexplicativos con títulos claros
☐ Excel para backup de datos si hay preguntas
☐ PDF como handout para audiencia
```

#### **🔍 Análisis Exploratorio**
```
Checklist de exportación:
☐ CSV para análisis estadístico personalizado
☐ Excel para pivots y análisis ad-hoc
☐ PNG para documentar hallazgos preliminares
☐ Historial para track de iteraciones
```

---

## 🗂️ Gestión del Historial de Exportaciones

### **📊 Dashboard de Exportaciones**

#### **Información Disponible**
Accede a: `http://localhost:8000/api/v1/export/user/exports`

**Datos por exportación:**
- **ID único**: Para referencia y trazabilidad
- **Tipo de exportación**: CSV, PNG, SVG, XLSX, PDF
- **Timestamp**: Fecha y hora exacta de generación
- **Tamaño de archivo**: Para gestión de almacenamiento
- **Estado**: Completado, en proceso, error
- **Usuario**: Tracking de autoría (si aplicable)

#### **Estadísticas del Sistema**
Accede a: `http://localhost:8000/api/v1/export/exports/stats`

**Métricas disponibles:**
- **Total de exportaciones**: Histórico del sistema
- **Tipos más populares**: CSV vs PNG vs SVG vs PDF
- **Tendencias temporales**: Uso del sistema por período
- **Tamaños promedio**: Para optimización de performance

### **🔍 Casos de Uso del Historial**

#### **📋 Auditoría de Investigación**
**Escenario**: Necesitas documentar todas las exportaciones utilizadas en un paper

**Proceso:**
1. **Filtrar por período**: Durante el período de investigación
2. **Identificar exportaciones**: Relacionadas con tu proyecto
3. **Documentar en metodología**: IDs, fechas, tipos
4. **Crear anexo**: Lista completa para transparencia

#### **🔄 Replicación de Análisis**
**Escenario**: Colega necesita replicar tu análisis con datos exactos

**Proceso:**
1. **Identificar exportaciones originales**: Por fecha y ID
2. **Re-exportar datasets**: Con mismos filtros y parámetros
3. **Compartir configuración**: Filtros temporales, categorías
4. **Validar consistencia**: Comparar tamaños y checksums

#### **📈 Tracking de Uso Institucional**
**Escenario**: Institución necesita reportar uso de la plataforma

**Proceso:**
1. **Exportar estadísticas**: Dashboard completo de métricas
2. **Analizar tendencias**: Crecimiento de uso por tipo
3. **Identificar patrones**: Tipos de análisis más demandados
4. **Planificar recursos**: Basado en uso proyectado

---

## ⚠️ Consideraciones Técnicas y Limitaciones

### **📊 Capacidad del Sistema**

#### **Límites Verificados**
- **Exportaciones simultáneas**: 5 máximo (prevent overload)
- **Tamaño máximo de archivo**: 10MB por exportación
- **Tiempo máximo de generación**: 30 segundos
- **Historial conservado**: 100 exportaciones más recientes

#### **Optimización de Performance**
- **CSV**: Más rápido para datasets grandes
- **PNG**: Requiere más procesamiento que SVG
- **PDF**: Más lento por integración de múltiples elementos
- **Caché**: Exportaciones idénticas se sirven desde caché

### **🔒 Consideraciones de Seguridad**

#### **Datos Incluidos en Exportaciones**
- **Contenido público**: Solo metadatos y análisis
- **Sin información personal**: No emails, IPs, datos privados
- **Fuentes citadas**: URLs y referencias bibliográficas
- **Compliance**: Cumple con fair use y términos de servicio

#### **Mejores Prácticas de Manejo**
- **Almacenamiento seguro**: No subir a servicios públicos inadecuados
- **Sharing controlado**: Verificar audiencia antes de compartir
- **Versionado**: Mantener track de versiones para reproducibilidad
- **Backup**: Respaldar exportaciones críticas

### **📱 Compatibilidad**

#### **Formatos Soportados por Plataforma**
- **CSV**: Universal (Excel, R, Python, SPSS, etc.)
- **XLSX**: Microsoft Office, LibreOffice, Google Sheets
- **PNG**: Universal (todos los viewers y editores)
- **SVG**: Adobe Illustrator, Inkscape, navegadores modernos
- **PDF**: Universal (todas las plataformas)

#### **Optimización por Dispositivo**
- **Desktop**: Todos los formatos funcionan óptimamente
- **Mobile**: PNG y PDF son más compatibles
- **Tablets**: SVG puede tener issues en apps específicas
- **Proyectores**: PNG garantiza mejor compatibility

---

## ❓ Preguntas Frecuentes del Módulo 4

### **📥 Proceso de Exportación**

**P: ¿Cuánto tiempo tarda en generar una exportación?**
**R:** Depende del tipo:
- CSV/XLSX: 2-5 segundos
- PNG/SVG: 5-10 segundos
- PDF completo: 10-30 segundos
- El sistema muestra progreso para exportaciones >5 segundos

**P: ¿Puedo cancelar una exportación en progreso?**
**R:** No hay cancelación manual, pero todas las exportaciones tienen timeout de 30 segundos. Si una exportación falla, se registra en el historial con estado "error".

**P: ¿Los filtros aplicados en el dashboard afectan las exportaciones?**
**R:** Actualmente las exportaciones incluyen todo el dataset. Los filtros personalizados están en desarrollo para versiones futuras.

### **📊 Calidad y Formatos**

**P: ¿Qué resolución tienen los gráficos PNG?**
**R:** 300 DPI con tamaño optimizado (típicamente 1920x1080), ideal para impresión y presentaciones profesionales.

**P: ¿Los gráficos SVG incluyen los datos originales?**
**R:** No, son solo visualizaciones. Para datos usa CSV/XLSX. SVG es óptimo para publicaciones que requieren escalabilidad infinita.

**P: ¿Puedo modificar los colores o estilo de los gráficos?**
**R:** Los gráficos usan esquema médico profesional estándar. Para personalización, exporta SVG y edita en Adobe Illustrator o Inkscape.

### **🗂️ Gestión de Archivos**

**P: ¿Cuánto espacio ocupan típicamente las exportaciones?**
**R:**
- CSV: ~50KB (106 artículos)
- XLSX: ~75KB
- PNG: ~200KB por gráfico
- SVG: ~50KB por gráfico
- PDF: ~500KB-2MB (completo)

**P: ¿Las exportaciones incluyen metadatos sobre las fuentes?**
**R:** Sí, CSV y XLSX incluyen URL source, fecha de publicación, categoría médica, y compliance score de la fuente.

**P: ¿Puedo exportar solo artículos de fuentes específicas?**
**R:** Actualmente no hay filtros por fuente en la exportación. Usa CSV completo y filtra en Excel/R/Python por la columna 'source_url'.

### **🔄 Reproducibilidad**

**P: ¿Cómo garantizo que mi análisis sea reproducible?**
**R:**
1. Documenta fecha exacta de exportación
2. Guarda ID de exportación del historial
3. Incluye versión del sistema en tu metodología
4. Conserva CSV original como archivo de referencia

**P: ¿Los datos cambian entre exportaciones?**
**R:** El dataset base es estable, pero se actualiza periódicamente con nuevos artículos. Para análisis longitudinal, conserva snapshots por fecha.

---

## 🎯 Resumen del Módulo 4

### ✅ **Has Aprendido:**
- Generar reportes en 5 formatos diferentes (CSV, XLSX, PNG, SVG, PDF)
- Interpretar y usar el sistema de historial de exportaciones
- Aplicar mejores prácticas de organización y nomenclatura
- Personalizar exportaciones para diferentes audiencias
- Gestionar flujo de trabajo completo de exportación
- Optimizar calidad y compatibility por caso de uso

### 📊 **Sistema de Exportación Verificado:**
- **7 endpoints activos** con exportación funcional
- **Formatos múltiples** para diferentes casos de uso
- **Calidad profesional** (300 DPI PNG, SVG vectorial)
- **Historial integrado** con tracking completo
- **Performance optimizada** (<30 segundos todas las exportaciones)

### 📋 **Checklist de Progreso:**
- [ ] Generé mi primera exportación CSV exitosamente
- [ ] Creé gráficos en PNG y SVG para diferentes usos
- [ ] Exporté datos estructurados en Excel
- [ ] Verifiqué mi historial de exportaciones
- [ ] Organicé archivos con nomenclatura consistente
- [ ] Identifiqué mejores prácticas para mi caso de uso específico

---

## 👉 Siguiente Paso

**🗺️ Módulo 5: Análisis Geográfico y Temporal**

En el próximo módulo aprenderás a:
- Interpretar mapas geográficos de cobertura (3 países disponibles)
- Analizar tendencias temporales en datasets de noticias médicas
- Usar filtros avanzados por país/región para análisis comparativos
- Identificar patrones estacionales en narrativas médicas
- Correlacionar análisis geográfico-temporal con sentimientos
- Exportar análisis geográficos para presentaciones globales

---

**🔗 Enlaces Útiles:**
- **API de Exportación**: http://localhost:8000/api/v1/export/
- **Dashboard Principal**: http://localhost:5173
- **Módulo Anterior**: [Gestión de Fuentes](03-gestion-fuentes-noticias.md)
- **Índice General**: [Manual de Usuario](../indice-principal.md)

**💡 Tip**: Mantén una carpeta organizada de exportaciones con nomenclatura consistente desde el principio - esto será invaluable cuando tengas múltiples proyectos y análisis longitudinales.
