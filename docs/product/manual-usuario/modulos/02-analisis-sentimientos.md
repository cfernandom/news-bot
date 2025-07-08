# Módulo 2: Análisis de Sentimientos
## Manual de Usuario - PreventIA News Analytics

---

## 🎯 ¿Qué aprenderás en este módulo?

Al completar este módulo serás capaz de:
- Interpretar correctamente los gráficos de análisis de sentimientos
- Entender qué significan los diferentes tipos de sentimiento en noticias médicas
- Usar filtros para análisis específicos por fecha y categoría
- Aplicar el análisis de sentimientos a casos de investigación reales
- Exportar y compartir resultados de análisis de sentimientos

---

## 📊 ¿Qué es el Análisis de Sentimientos?

### **Definición Simple**
El análisis de sentimientos es una tecnología que **automaticamente identifica el tono emocional** de las noticias médicas. El sistema lee cada artículo y determina si el contenido es:

- 🟢 **POSITIVO**: Noticias optimistas, avances, éxitos en tratamientos
- 🔴 **NEGATIVO**: Noticias preocupantes, desafíos, problemas identificados
- ⚫ **NEUTRAL**: Noticias informativas, datos objetivos, sin sesgo emocional

### **¿Por qué es importante en medicina?**
- **Para investigadores**: Identificar tendencias en la percepción pública de tratamientos
- **Para profesionales**: Monitorear cómo se comunican los avances médicos
- **Para gestores**: Evaluar el impacto mediático de políticas de salud
- **Para estudiantes**: Entender la evolución del discurso médico

---

## 📈 Distribución Actual del Sistema

### **Estado Verificado (2025-07-08)**
Basado en **106 artículos analizados** en el sistema operativo:

#### **🔴 Sentimiento Negativo: 79 artículos (75%)**
- **Promedio de intensidad**: -0.713 (fuertemente negativo)
- **Ejemplos típicos**: Estadísticas de incidencia, desafíos en tratamiento, efectos secundarios

#### **🟢 Sentimiento Positivo: 24 artículos (23%)**
- **Promedio de intensidad**: +0.462 (moderadamente positivo)
- **Ejemplos típicos**: Nuevos tratamientos exitosos, testimonios de recuperación, avances en investigación

#### **⚫ Sentimiento Neutral: 3 artículos (3%)**
- **Promedio de intensidad**: +0.034 (prácticamente neutral)
- **Ejemplos típicos**: Estudios descriptivos, datos epidemiológicos, información técnica

### **🎯 Interpretación para Investigación**
Esta distribución es **típica y esperada** en noticias médicas especializadas porque:
- Las noticias médicas tienden a informar sobre **desafíos y problemas** (75% negativo)
- Los **avances positivos** son menos frecuentes pero significativos (23% positivo)
- La **información puramente técnica** es minoritaria (3% neutral)

---

## 🖼️ Interpretando los Gráficos de Sentimientos

### **📊 Gráfico Circular (Pie Chart)**
Es la visualización principal que verás en el dashboard:

#### **Cómo Leerlo:**
1. **Tamaño de cada sección** = proporción de artículos con ese sentimiento
2. **Colores estándar**:
   - 🟢 Verde = Positivo
   - 🔴 Rojo = Negativo
   - ⚫ Gris/Negro = Neutral
3. **Porcentajes** mostrados en cada sección
4. **Números absolutos** (ej: "79 artículos") en tooltip al hacer hover

#### **Interpretación Práctica:**
```
Si ves: 75% Negativo, 23% Positivo, 3% Neutral

Significa:
- La mayoría de noticias abordan desafíos/problemas
- Hay un 23% de cobertura optimista significativa
- Poca información puramente técnica/neutral
```

### **📈 Gráfico de Barras (Bar Chart)**
Algunos dashboards pueden mostrar barras horizontales o verticales:

#### **Ventajas:**
- Fácil comparación entre categorías
- Mejor para mostrar números exactos
- Útil cuando hay muchas subcategorías

#### **Cómo Interpretarlo:**
- **Altura/longitud de barra** = cantidad de artículos
- **Colores** mantienen el mismo código (verde/rojo/gris)
- **Etiquetas numéricas** muestran valores exactos

---

## 🔍 Filtros Avanzados para Análisis Específicos

### **📅 Filtros Temporales**

#### **Por Períodos Predefinidos:**
- **Última semana**: Tendencias más recientes
- **Último mes**: Patrones mensuales
- **Último trimestre**: Tendencias estacionales
- **Último año**: Análisis de largo plazo

#### **Por Fechas Personalizadas:**
- **Fecha inicial**: Desde cuándo analizar
- **Fecha final**: Hasta cuándo analizar
- **Períodos específicos**: Eventos médicos importantes, conferencias

#### **Casos de Uso Temporal:**
```
🎯 Análisis de Conferencia Médica:
- Filtro: "1 semana antes + 1 semana después"
- Objetivo: Medir impacto mediático del evento

🎯 Análisis Estacional:
- Filtro: "Octubre (mes de concienciación)"
- Objetivo: Evaluar cobertura en campañas específicas

🎯 Análisis de Tendencia:
- Filtro: "Últimos 12 meses"
- Objetivo: Identificar cambios en narrativa médica
```

### **🏷️ Filtros por Categoría Médica**

#### **Categorías Disponibles en el Sistema:**
Basado en datos verificados del sistema operativo:

1. **Treatment (Tratamiento)**: 39 artículos
   - Incluye: Terapias, medicamentos, protocolos
   - Sentimiento típico: Mixto (positivo para éxitos, negativo para efectos)

2. **General**: 19 artículos
   - Incluye: Información general, estadísticas
   - Sentimiento típico: Neutro a negativo

3. **Research (Investigación)**: 19 artículos
   - Incluye: Estudios, descubrimientos, ensayos clínicos
   - Sentimiento típico: Positivo (avances) o neutro (datos)

4. **Surgery (Cirugía)**: 12 artículos
   - Incluye: Procedimientos quirúrgicos, técnicas
   - Sentimiento típico: Técnico, neutro a positivo

5. **Genetics (Genética)**: 4 artículos
   - Incluye: Factores hereditarios, biomarcadores
   - Sentimiento típico: Informativo, neutro

#### **Cómo Usar Filtros de Categoría:**
```
📊 Análisis por Tratamiento:
- Filtro: "Treatment"
- Pregunta: "¿Cómo se perciben los nuevos tratamientos?"
- Análisis: 39 artículos enfocados en terapias

🔬 Análisis por Investigación:
- Filtro: "Research"
- Pregunta: "¿Qué tan optimistas son las noticias de investigación?"
- Análisis: 19 artículos sobre estudios y descubrimientos
```

---

## 🎯 Casos de Uso Prácticos

### **Caso 1: Investigador Evaluando Percepción de Nuevos Tratamientos**

#### **Objetivo:**
Entender cómo los medios presentan los nuevos tratamientos para cáncer de mama.

#### **Pasos:**
1. **Filtrar por categoría**: Seleccionar "Treatment"
2. **Filtrar por tiempo**: "Últimos 6 meses"
3. **Analizar distribución**: Comparar % positivo vs negativo
4. **Interpretar resultado**:
   - Si >60% positivo = Cobertura optimista de tratamientos
   - Si >60% negativo = Énfasis en desafíos/efectos secundarios

#### **Aplicación:**
- Diseñar estrategias de comunicación más efectivas
- Identificar brechas en narrativas médicas
- Preparar contenido educativo equilibrado

### **Caso 2: Profesional Médico Monitoreando Tendencias**

#### **Objetivo:**
Identificar cambios en la narrativa mediática durante campañas de concienciación.

#### **Pasos:**
1. **Comparar períodos**: "Octubre 2024" vs "Octubre 2023"
2. **Analizar todos los sentimientos** sin filtros de categoría
3. **Buscar cambios**: ¿Aumentó el % positivo?
4. **Correlacionar con eventos**: Campañas, conferencias, políticas públicas

#### **Aplicación:**
- Evaluar efectividad de campañas de salud pública
- Planificar futuras estrategias de comunicación
- Identificar necesidades de educación médica

### **Caso 3: Estudiante Analizando Evolución del Discurso**

#### **Objetivo:**
Estudiar cómo ha evolucionado la narrativa sobre investigación genética.

#### **Pasos:**
1. **Filtrar por categoría**: Seleccionar "Genetics"
2. **Análisis temporal**: Comparar trimestres consecutivos
3. **Documentar cambios**: Capturar tendencias con exportaciones
4. **Contextualizar**: Relacionar con avances científicos conocidos

#### **Aplicación:**
- Proyectos de investigación académica
- Tesis sobre comunicación médica
- Análisis de impacto social de avances científicos

---

## 📤 Exportación de Análisis de Sentimientos

### **Formatos Disponibles**

#### **🖼️ PNG (Imagen)**
- **Mejor para**: Presentaciones, reportes, redes sociales
- **Calidad**: Alta resolución (300 DPI)
- **Tamaño**: Óptimo para proyectores y documentos

#### **📊 SVG (Vector)**
- **Mejor para**: Publicaciones académicas, documentos escalables
- **Ventaja**: Se puede redimensionar sin pérdida de calidad
- **Uso**: Artículos científicos, posters médicos

#### **📄 PDF (Reporte)**
- **Mejor para**: Documentos formales, archivos permanentes
- **Incluye**: Gráfico + metadatos + interpretación automática
- **Ventaja**: Formato profesional completo

### **Pasos para Exportar:**

#### **1. Configurar el Análisis**
- Aplicar filtros deseados (fecha, categoría)
- Verificar que el gráfico muestre la información correcta
- Asegurar que los datos sean representativos

#### **2. Acceder a Exportación**
- Buscar botón "Exportar" o ícono de descarga
- Seleccionar formato deseado (PNG/SVG/PDF)
- Configurar opciones adicionales si están disponibles

#### **3. Descargar y Verificar**
- Guardar archivo en ubicación apropiada
- Abrir archivo para verificar calidad
- Renombrar con descripción clara (ej: "sentimientos_tratamiento_oct2024.png")

### **Mejores Prácticas de Exportación:**

#### **📋 Nomenclatura de Archivos:**
```
Formato recomendado:
sentimiento_[categoria]_[periodo]_[fecha].extension

Ejemplos:
- sentimiento_treatment_ultimo_mes_2025-01-08.png
- sentimiento_general_octubre_2024.svg
- sentimiento_research_2024_completo.pdf
```

#### **🎯 Para Presentaciones:**
- **PNG alta resolución** para claridad en proyectores
- **Colores contrastantes** para visibilidad
- **Tamaño consistente** entre gráficos relacionados

#### **📚 Para Publicaciones Académicas:**
- **SVG** para máxima calidad de impresión
- **Leyendas claras** y autoexplicativas
- **Metadatos incluidos** (fecha, muestra, criterios)

---

## ❓ Preguntas Frecuentes del Módulo 2

### **🔍 Interpretación de Resultados**

**P: ¿Por qué hay tanto sentimiento negativo (75%) en las noticias médicas?**
**R:** Es normal y esperado. Las noticias médicas tienden a reportar desafíos, estadísticas de incidencia y efectos adversos más frecuentemente que solo éxitos. Un 75% negativo no significa "malas noticias", sino información realista sobre desafíos médicos.

**P: ¿Un 23% de sentimiento positivo es bueno o malo?**
**R:** Es una proporción saludable. Indica que sí hay cobertura de avances y éxitos, pero balanceada con realismo médico. En investigación, busca tendencias en el tiempo más que números absolutos.

**P: ¿Qué significa un score de -0.713 vs +0.462?**
**R:**
- **-0.713**: Sentimiento negativo moderadamente fuerte (escala típica -1 a +1)
- **+0.462**: Sentimiento positivo moderado
- La **intensidad diferente** es normal; las noticias médicas negativas tienden a ser más intensas que las positivas

### **🛠️ Uso de Filtros**

**P: ¿Cuál es el mejor período para analizar tendencias?**
**R:** Depende del objetivo:
- **Últimas 2 semanas**: Reacciones a eventos específicos
- **Último trimestre**: Tendencias estacionales
- **Último año**: Patrones de largo plazo
- **Períodos personalizados**: Para eventos médicos específicos

**P: ¿Puedo combinar múltiples filtros?**
**R:** Sí, puedes filtrar simultáneamente por fecha Y categoría. Por ejemplo: "Tratamientos en el último mes" combina filtro temporal + categoría.

**P: ¿Los filtros afectan la exportación?**
**R:** Sí, cuando exportas un gráfico, incluye solo los datos que cumplen los filtros activos. Esto te permite crear reportes específicos.

### **📊 Exportación y Compartir**

**P: ¿Cuál formato es mejor para mi tesis universitaria?**
**R:** **SVG** para máxima calidad de impresión, o **PDF** si necesitas incluir metadatos automáticos. Evita PNG para documentos que se imprimirán.

**P: ¿Puedo usar estos gráficos en presentaciones públicas?**
**R:** Sí, los datos son de fuentes públicas procesados para análisis académico. Incluye siempre la fuente: "PreventIA News Analytics Platform, [fecha]".

**P: ¿Los gráficos incluyen información sobre la muestra?**
**R:** Depende del formato. Los PDF incluyen metadatos automáticos. Para otros formatos, documenta manualmente: período analizado, número de artículos, filtros aplicados.

---

## 🧠 Ejercicio Práctico: Tu Primer Análisis Completo

### **Escenario:**
Eres un investigador que necesita evaluar cómo se perciben los tratamientos de cáncer de mama en la cobertura mediática reciente.

### **Paso 1: Configuración Inicial**
1. Accede al dashboard principal: `http://localhost:5173`
2. Localiza el gráfico de análisis de sentimientos
3. Verifica que muestre datos de todos los períodos (sin filtros)

### **Paso 2: Análisis General**
1. **Observa la distribución actual**: ~75% negativo, 23% positivo, 3% neutral
2. **Anota estos valores** como tu línea base
3. **Pregúntate**: "¿Esta distribución es lo que esperaba?"

### **Paso 3: Análisis Específico de Tratamientos**
1. **Aplica filtro de categoría**: Selecciona "Treatment"
2. **Observa cómo cambia** la distribución
3. **Compara con el análisis general**: ¿Los tratamientos son más o menos positivos que el promedio?

### **Paso 4: Análisis Temporal**
1. **Aplica filtro temporal**: "Últimos 3 meses"
2. **Mantén el filtro "Treatment"** activo
3. **Analiza la tendencia**: ¿Es diferente al período completo?

### **Paso 5: Documentar Hallazgos**
1. **Exporta el gráfico final** en formato PNG
2. **Escribe 3 observaciones clave**:
   - Distribución general de sentimientos en tratamientos
   - Diferencia temporal (3 meses vs todo el período)
   - Implicaciones para comunicación médica

### **Paso 6: Reflexión**
**Preguntas para responder:**
- ¿Qué te sorprendió de los resultados?
- ¿Cómo usarías esta información en tu investigación?
- ¿Qué preguntas adicionales te surgen?

### **Resultado Esperado:**
Al final tendrás:
- ✅ Un gráfico exportado con datos específicos
- ✅ Comprensión práctica de filtros
- ✅ 3 observaciones documentadas
- ✅ Experiencia en interpretación de sentimientos

---

## 🎯 Resumen del Módulo 2

### ✅ **Has Aprendido:**
- Interpretar gráficos de análisis de sentimientos en contexto médico
- Entender qué significan las distribuciones típicas (75% negativo es normal)
- Usar filtros temporales y de categoría para análisis específicos
- Aplicar el análisis a casos de investigación reales
- Exportar resultados en diferentes formatos profesionales

### 📊 **Datos Clave del Sistema:**
- **106 artículos analizados** con distribución: 75% negativo, 23% positivo, 3% neutral
- **5 categorías principales**: Treatment (39), General (19), Research (19), Surgery (12), Genetics (4)
- **Sistema operativo** verificado con análisis en tiempo real

### 📋 **Checklist de Progreso:**
- [ ] Interpreté correctamente un gráfico de sentimientos
- [ ] Apliqué filtros temporales y de categoría
- [ ] Realicé un análisis específico de mi área de interés
- [ ] Exporté mi primer gráfico en formato profesional
- [ ] Documenté 3 observaciones clave de mis resultados

---

## 👉 Siguiente Paso

**🌍 Módulo 3: Gestión de Fuentes de Noticias**

En el próximo módulo aprenderás a:
- Acceder y navegar por el panel de administración
- Interpretar el dashboard de compliance y calidad de fuentes
- Entender cómo se monitorean las 9 fuentes configuradas
- Solicitar nuevas fuentes para análisis específicos
- Interpretar métricas de cobertura geográfica (3 países actualmente)

---

**🔗 Enlaces Útiles:**
- **Dashboard Principal**: http://localhost:5173
- **Módulo Anterior**: [Introducción y Primeros Pasos](01-introduccion-primeros-pasos.md)
- **Índice General**: [Manual de Usuario](../indice-principal.md)

**💡 Tip**: Practica con diferentes combinaciones de filtros para familiarizarte con todas las posibilidades de análisis antes de continuar al siguiente módulo.
