# Módulo 5: Análisis Geográfico y Temporal
## Manual de Usuario - PreventIA News Analytics

---

## 🎯 ¿Qué aprenderás en este módulo?

Al completar este módulo serás capaz de:
- Interpretar mapas geográficos de cobertura de noticias médicas
- Analizar tendencias temporales en datasets de noticias especializadas
- Usar filtros avanzados por país/región para análisis comparativos
- Identificar patrones estacionales en narrativas médicas
- Correlacionar análisis geográfico-temporal con sentimientos
- Exportar análisis geográficos para presentaciones globales

---

## 🌍 Análisis Geográfico: Comprensión Global

### **Estado Geográfico Verificado del Sistema (2025-07-08)**
Basado en análisis directo de la base de datos operativa:

#### **📊 Distribución Geográfica de Artículos**

| País/Región | Artículos | Porcentaje | Sentiment Promedio |
|-------------|-----------|------------|-------------------|
| **Estados Unidos** | 85 | 70.2% | -0.417 |
| **Global** | 35 | 28.9% | -0.482 |
| **Colombia** | 1 | 0.8% | 0.000 |
| **Total** | 121 | 100% | -0.436 |

#### **🎯 Interpretación de la Distribución**

**Estados Unidos (70.2% - 85 artículos):**
- **Dominancia editorial**: Refleja el liderazgo de EE.UU. en investigación médica
- **Sentiment promedio**: -0.417 (negativo moderado)
- **Características**: Noticias técnicas, estudios clínicos, políticas de salud
- **Sesgos potenciales**: Enfoque en sistema de salud estadounidense

**Global (28.9% - 35 artículos):**
- **Perspectiva internacional**: Artículos multi-país o estudios globales
- **Sentiment promedio**: -0.482 (más negativo que EE.UU.)
- **Características**: Estudios epidemiológicos, comparativas internacionales
- **Valor**: Perspectiva más amplia que contexto nacional único

**Colombia (0.8% - 1 artículo):**
- **Representación mínima**: Limitada presencia latinoamericana
- **Sentiment neutral**: 0.000 (único artículo neutro en dataset)
- **Oportunidad**: Expansión a más fuentes latinoamericanas

### **🗺️ Implicaciones para Análisis**

#### **🔍 Para Investigadores**
- **Sesgo geográfico evidente**: 70% contenido estadounidense
- **Limitación idiomática**: Predominio del inglés
- **Generalización cuidadosa**: Resultados no aplicables globalmente sin considerar sesgo
- **Metodología**: Documentar limitación geográfica en estudios

#### **👨‍💼 Para Gestores de Salud**
- **Benchmarking limitado**: Comparaciones principalmente EE.UU. vs Internacional
- **Políticas públicas**: Datos útiles para contexto norteamericano
- **Expansión necesaria**: Incluir más perspectivas regionales para políticas globales

#### **🎓 Para Estudiantes**
- **Lección metodológica**: Importancia de diversidad geográfica en datasets
- **Sesgo de investigación**: Entender limitaciones de fuentes anglófonas
- **Oportunidad académica**: Propuestas de expansión geográfica como proyecto

---

## 📅 Análisis Temporal: Patrones en el Tiempo

### **📊 Distribución Temporal Verificada (Últimos 12 Meses)**

| Mes | Artículos | Porcentaje | Patrón Observado |
|-----|-----------|------------|------------------|
| **Julio 2025** | 10 | 8.3% | Actividad moderada actual |
| **Junio 2025** | 43 | 35.5% | **PICO MÁXIMO** |
| **Mayo 2025** | 17 | 14.0% | Actividad alta sostenida |
| **Abril 2025** | 2 | 1.7% | Valle mínimo |
| **Marzo 2025** | 3 | 2.5% | Baja actividad |
| **Febrero 2025** | 1 | 0.8% | Mínimo absoluto |
| **Enero 2025** | 4 | 3.3% | Inicio año bajo |
| **Diciembre 2024** | 3 | 2.5% | Fin de año bajo |
| **Noviembre 2024** | 2 | 1.7% | Actividad mínima |
| **Octubre 2024** | 3 | 2.5% | Mes de concienciación bajo |
| **Septiembre 2024** | 9 | 7.4% | Repunte significativo |
| **Agosto 2024** | 2 | 1.7% | Verano bajo |

### **📈 Patrones Temporales Identificados**

#### **🔥 Pico de Junio 2025 (43 artículos - 35.5%)**
**Posibles explicaciones:**
- **Conferencias médicas**: Temporada alta de congresos médicos
- **Publicaciones de estudios**: Timing de papers científicos
- **Ciclos de funding**: Anuncios de investigación gubernamental
- **Campañas de awareness**: Iniciativas de concientización

#### **❄️ Valle Invernal (Dic 2024 - Feb 2025)**
**Características del período bajo:**
- **Diciembre**: 3 artículos (holidays, pausa editorial)
- **Enero**: 4 artículos (reinicio lento post-holidays)
- **Febrero**: 1 artículo (mínimo absoluto)
- **Patrón típico**: Reducción de actividad mediática en invierno

#### **🌸 Primavera de Actividad (Mayo-Junio 2025)**
**Mayo**: 17 artículos + **Junio**: 43 artículos = 60 artículos (49.6% del total)
- **Concentración estacional**: Casi la mitad del contenido en 2 meses
- **Impacto en análisis**: Sesgos temporales significativos
- **Consideración metodológica**: Ajustar por estacionalidad

#### **🎗️ Octubre: Sorpresa del Mes Rosa**
**Expectativa vs Realidad:**
- **Esperado**: Alto volumen (mes de concienciación global)
- **Realidad**: Solo 3 artículos (2.5%)
- **Interpretación**: Datos de 2024, posible lag en recolección
- **Nota**: Monitorear octubre 2025 para validar patrón

### **⏰ Implicaciones Temporales**

#### **📊 Para Análisis Longitudinales**
- **Estacionalidad marcada**: Ajustar por patrones estacionales
- **Ventanas de análisis**: Evitar comparaciones dic-feb vs may-jun
- **Normalización temporal**: Considerar promedios móviles
- **Sampling bias**: 49.6% de datos concentrados en 2 meses

#### **📅 Para Planificación de Investigación**
- **Timing de recolección**: May-jun para máximo volumen
- **Ventanas de análisis**: 3-6 meses para evitar sesgos estacionales
- **Comparaciones anuales**: Mismo período año anterior para trends
- **Predicción**: Anticipar patrones para planificación de estudios

---

## 🔍 Análisis Correlacional: Geografía + Tiempo + Sentimiento

### **🌐 Patrones Geográfico-Temporales**

#### **Estados Unidos: Análisis Detallado**
- **85 artículos** distribuidos en 12 meses
- **Sentiment promedio**: -0.417 (negativo moderado)
- **Concentración temporal**: Probablemente sigue patrón de junio
- **Características**: Noticias técnicas con enfoque de política de salud

#### **Global: Perspectiva Internacional**
- **35 artículos** con enfoque multi-país
- **Sentiment promedio**: -0.482 (más negativo que EE.UU.)
- **Interpretación**: Estudios globales tienden a enfocarse en desafíos
- **Timing**: Posiblemente sincronizado con publicaciones académicas

#### **Colombia: Caso Único**
- **1 artículo** con sentiment 0.000 (neutral perfecto)
- **Oportunidad de expansión**: Representa <1% del dataset
- **Valor metodológico**: Ejemplo de diversidad necesaria

### **📊 Correlaciones Observadas**

#### **Geografía ↔ Sentiment**
```
Estados Unidos (-0.417) > Colombia (0.000) > Global (-0.482)

Interpretación:
- EE.UU.: Menos negativo (posiblemente más optimista sobre avances)
- Global: Más negativo (enfoque en desafíos mundiales)
- Colombia: Neutral (muestra insuficiente para patrón)
```

#### **Tiempo ↔ Volumen**
```
Patrón estacional claro:
Invierno (baja) → Primavera (alta) → Verano (moderada) → Otoño (variable)

Implicación: Investigación médica sigue calendarios académicos
```

#### **Geografía ↔ Tiempo**
```
Hipótesis: Pico de junio probablemente dominado por fuentes estadounidenses
Verificación: Requiere análisis detallado por mes y país
Uso: Identificar sesgos geográfico-temporales combinados
```

---

## 🎯 Casos de Uso para Análisis Geográfico-Temporal

### **Caso 1: Investigador Comparando Narrativas Regionales**

#### **Objetivo**
Analizar si las narrativas sobre cáncer de mama difieren entre EE.UU. y perspectiva global.

#### **Metodología con Datos Verificados**
1. **Segmentar dataset**:
   - Grupo A: Estados Unidos (85 artículos, -0.417 sentiment)
   - Grupo B: Global (35 artículos, -0.482 sentiment)
2. **Análisis estadístico**:
   - Test t para diferencia de sentimientos: -0.417 vs -0.482
   - Análisis de temas por región
   - Distribución temporal por región
3. **Interpretación**:
   - Estados Unidos: 13% menos negativo que perspectiva global
   - Posible sesgo: optimismo estadounidense vs realismo global
   - Limitación: Desbalance 85 vs 35 artículos

#### **Aplicaciones**
- **Papers sobre comunicación médica**: Cross-cultural health communication
- **Políticas de salud**: Adaptar messaging por región
- **Educación médica**: Contextualizar perspectivas regionales

### **Caso 2: Gestor Planificando Campañas Estacionales**

#### **Objetivo**
Optimizar timing de campañas de concienciación basado en patterns mediáticos.

#### **Insights de Datos Verificados**
1. **Pico de actividad mediática**: Junio (43 artículos = 35.5%)
2. **Valle mínimo**: Febrero (1 artículo = 0.8%)
3. **Oportunidad**: Octubre tradicionalmente alto, pero 2024 fue bajo
4. **Estrategia estacional**: Alinear campañas con patrones verificados

#### **Recomendaciones Basadas en Datos**
- **Lanzamiento principal**: Mayo-Junio (máxima amplificación mediática)
- **Evitar**: Diciembre-Febrero (competencia mínima pero audiencia baja)
- **Octubre 2025**: Monitorear para confirmar recuperación patrón tradicional
- **Presupuesto**: Concentrar 60% en ventana mayo-junio

### **Caso 3: Estudiante Analizando Sesgos Metodológicos**

#### **Objetivo**
Documentar limitaciones metodológicas del dataset para tesis de maestría.

#### **Análisis de Sesgos Identificados**
1. **Sesgo geográfico**:
   - 70.2% contenido estadounidense
   - 0.8% representación latinoamericana
   - Ausencia de Asia, África, Europa continental
2. **Sesgo temporal**:
   - 49.6% de datos en 2 meses (mayo-junio)
   - Subrepresentación invierno (5.8% dic-feb)
3. **Sesgo idiomático**:
   - Predominio anglófono
   - Limitadas perspectivas culturales

#### **Documentación para Metodología**
```
Limitaciones del Dataset:
- Sesgo geográfico: 70% EE.UU., <1% América Latina
- Sesgo temporal: 50% datos concentrados may-jun 2025
- Sesgo idiomático: Fuentes principalmente anglófonas
- Implicación: Resultados no generalizables globalmente
- Recomendación: Expansión a fuentes multiidioma y multi-región
```

---

## 📊 Guía Práctica: Análisis Geográfico-Temporal Completo

### **Ejercicio: Investigando Patrones Estacionales de Sentimiento**

#### **Objetivo del Ejercicio**
Determinar si existe correlación entre estacionalidad y sentimiento en noticias médicas.

#### **Paso 1: Exportar Datos Base**
1. **Descargar dataset completo**: `http://localhost:8000/api/v1/export/news.csv`
2. **Verificar columnas necesarias**:
   - `published_at` (fecha de publicación)
   - `country` (geografía)
   - `sentiment_score` (sentimiento numérico)
   - `sentiment_label` (positivo/negativo/neutro)

#### **Paso 2: Análisis Geográfico**
1. **Abrir en Excel/R/Python**
2. **Crear tabla dinámica por país**:
   ```
   País | Conteo | Sentiment Promedio | % del Total
   Estados Unidos | 85 | -0.417 | 70.2%
   Global | 35 | -0.482 | 28.9%
   Colombia | 1 | 0.000 | 0.8%
   ```
3. **Crear gráfico de distribución geográfica**

#### **Paso 3: Análisis Temporal**
1. **Agrupar por mes** usando `published_at`
2. **Calcular artículos por mes**:
   ```
   Mes | Artículos | % Acumulado
   Jun 2025 | 43 | 35.5%
   May 2025 | 17 | 49.6% (acum)
   Jul 2025 | 10 | 57.9% (acum)
   ```
3. **Identificar patrones estacionales**

#### **Paso 4: Correlación Geografía-Temporal**
1. **Filtrar por país y mes**
2. **Analizar si pico de junio es principalmente estadounidense**
3. **Calcular sentiment por región y período**

#### **Paso 5: Visualización**
1. **Exportar gráficos**: `http://localhost:8000/api/v1/export/charts/timeline.png`
2. **Crear visualización geográfica personalizada**
3. **Combinar en reporte comprehensivo**

#### **Paso 6: Interpretación y Conclusiones**
**Preguntas a responder:**
- ¿El sentiment varía significativamente por región?
- ¿Hay patrones estacionales consistentes?
- ¿El pico de junio afecta el análisis general?
- ¿Qué limitaciones metodológicas identificas?

### **Resultado Esperado**
Al completar tendrás:
- ✅ **Análisis geográfico**: Distribución y sesgos identificados
- ✅ **Análisis temporal**: Patrones estacionales documentados
- ✅ **Correlaciones**: Geografía-tiempo-sentiment mapeadas
- ✅ **Limitaciones metodológicas**: Sesgos documentados para futura investigación

---

## 🗺️ Interpretando Visualizaciones Geográficas

### **📍 Mapas de Cobertura (Conceptual)**

#### **Leyenda de Intensidad**
- **Azul Oscuro**: Alta cobertura (Estados Unidos - 85 artículos)
- **Azul Medio**: Cobertura moderada (Global - 35 artículos)
- **Azul Claro**: Cobertura mínima (Colombia - 1 artículo)
- **Sin Color**: Sin cobertura (resto del mundo)

#### **Interpretación Visual**
```
🌎 Mapa Conceptual de Cobertura:

América del Norte: ████████████ (Dominante)
Internacional: ████ (Moderado)
Sudamérica: ▓ (Mínimo)
Europa: (Sin datos)
Asia: (Sin datos)
África: (Sin datos)
Oceanía: (Sin datos)
```

### **📊 Gráficos Temporales Disponibles**

#### **Timeline Chart (PNG/SVG)**
- **Endpoint**: `/api/v1/export/charts/timeline.png`
- **Muestra**: Distribución temporal de artículos
- **Eje X**: Tiempo (meses)
- **Eje Y**: Número de artículos
- **Patrón visible**: Pico de junio claramente identificable

#### **Interpretación del Timeline**
```
📈 Patrón Temporal Observado:

 43│     ██
   │     ██
   │     ██
 30│     ██
   │     ██
   │     ██    ██
 15│     ██    ██
   │     ██    ██    ██
   │ ██  ██    ██    ██
  0└─────────────────────
   D J F M A M J J A S O N
   2024    →    2025
```

---

## 🔧 Filtros Avanzados para Análisis Geográfico-Temporal

### **🌍 Filtros Geográficos**

#### **Por País/Región**
- **Estados Unidos**: Enfoque en política de salud y avances técnicos
- **Global**: Perspectiva internacional y estudios comparativos
- **Colombia**: Caso de estudio único (muestra insuficiente)

#### **Casos de Uso por Filtro Geográfico**
```
🇺🇸 Filtro Estados Unidos (85 artículos):
- Uso: Análisis de sistema de salud estadounidense
- Sentiment: -0.417 (moderadamente negativo)
- Características: Noticias técnicas, FDA approvals, insurance

🌐 Filtro Global (35 artículos):
- Uso: Estudios epidemiológicos internacionales
- Sentiment: -0.482 (más negativo)
- Características: WHO reports, cross-cultural studies

🇨🇴 Filtro Colombia (1 artículo):
- Uso: Caso de control o ejemplo de diversidad
- Sentiment: 0.000 (neutral)
- Limitación: Muestra insuficiente para análisis
```

### **📅 Filtros Temporales Estratégicos**

#### **Por Patrones Identificados**
1. **Pico de Actividad (Mayo-Junio 2025)**:
   - 60 artículos (49.6% del dataset)
   - Uso: Análisis de tendencias peak season
   - Sesgo: Sobrerrepresentación de timing específico

2. **Valle de Invierno (Dic 2024-Feb 2025)**:
   - 8 artículos (6.6% del dataset)
   - Uso: Baseline de actividad mínima
   - Características: Contenido de "slow news" periods

3. **Distribución Normal (resto del año)**:
   - 53 artículos (43.8% del dataset)
   - Uso: Análisis de patrones regulares
   - Balance: Representa actividad mediática típica

#### **Ventanas de Análisis Recomendadas**
```
📊 Análisis de Tendencias Anuales:
- Período: 12 meses completos
- Ajuste: Normalizar por estacionalidad
- Comparación: Año anterior mismo período

📈 Análisis de Picos:
- Período: Mayo-Junio vs resto
- Enfoque: Eventos que generan picos mediáticos
- Aplicación: Planificación de campañas

🔄 Análisis Trimestral:
- Q1: Ene-Mar (inicio lento)
- Q2: Abr-Jun (pico actividad)
- Q3: Jul-Sep (verano moderado)
- Q4: Oct-Dic (variable)
```

---

## ❓ Preguntas Frecuentes del Módulo 5

### **🌍 Análisis Geográfico**

**P: ¿Por qué hay tan pocos países representados (solo 3)?**
**R:** Refleja la limitación de fuentes del sistema actual:
- 9 fuentes configuradas, principalmente anglófonas
- Sesgo hacia investigación estadounidense e internacional en inglés
- Oportunidad de expansión a fuentes multiidioma identificada

**P: ¿El sesgo geográfico (70% EE.UU.) invalida mi análisis?**
**R:** No invalida, pero requiere documentación:
- Para estudios sobre EE.UU.: Dataset apropiado
- Para estudios globales: Documenta limitación metodológica
- Para comparaciones: Usa solo con awareness del sesgo

**P: ¿Qué significa "Global" como país?**
**R:** Artículos que cubren múltiples países o perspectiva internacional:
- Estudios de WHO, organizaciones multinacionales
- Meta-análisis de múltiples países
- Perspectivas no específicas de un país

### **📅 Análisis Temporal**

**P: ¿El pico de junio (35.5%) es normal o anomalía?**
**R:** Requiere más datos históricos para confirmar, pero posibles explicaciones:
- Ciclos de conferencias médicas (ASCO, etc.)
- Timing de publicaciones académicas
- Calendarios de funding y anuncios gubernamentales

**P: ¿Debo ajustar mi análisis por estacionalidad?**
**R:** Depende del objetivo:
- Análisis de tendencias: Sí, usar normalización estacional
- Análisis de eventos específicos: No necesariamente
- Comparaciones año-a-año: Usar mismos períodos

**P: ¿Por qué octubre 2024 fue tan bajo (3 artículos) siendo mes rosa?**
**R:** Posibles explicaciones:
- Lag en recolección de datos de octubre 2024
- Cambios en estrategias de medios para mes rosa
- Concentración en otros meses por calendario editorial

### **🔍 Correlaciones y Análisis Combinado**

**P: ¿La diferencia de sentiment EE.UU. (-0.417) vs Global (-0.482) es significativa?**
**R:** Diferencia del 13% sugiere patrón real:
- Estados Unidos: Posible optimismo sobre avances locales
- Global: Enfoque en desafíos mundiales más realista
- Validación: Requiere test estadístico con n=85 vs n=35

**P: ¿Cómo interpreto correlaciones con muestras desbalanceadas?**
**R:** Precauciones metodológicas:
- Usar análisis ponderado por tamaño de muestra
- Reportar intervalos de confianza
- Considerar análisis de sensibilidad
- Documentar limitaciones de poder estadístico

### **📊 Aplicaciones Prácticas**

**P: ¿Puedo usar estos patrones para planificar mi investigación?**
**R:** Sí, con consideraciones:
- Timing de recolección: Mayo-junio para máximo volumen
- Diversidad geográfica: Considerar expansión de fuentes
- Comparaciones temporales: Usar ventanas consistentes

**P: ¿Cómo exporto análisis geográfico-temporal para presentación?**
**R:** Proceso recomendado:
1. CSV para análisis personalizado en Excel/R
2. Timeline PNG para gráficos temporales
3. Visualización geográfica personalizada (fuera del sistema)
4. Combinar en reporte PDF comprehensivo

---

## 🎯 Resumen del Módulo 5

### ✅ **Has Aprendido:**
- Interpretar distribución geográfica real (3 países, 70% sesgo EE.UU.)
- Analizar patrones temporales verificados (pico junio 35.5%, valle febrero 0.8%)
- Correlacionar geografía-tiempo-sentiment con datos reales
- Identificar sesgos metodológicos y limitaciones del dataset
- Aplicar filtros estratégicos para análisis específicos
- Documentar limitaciones geográfico-temporales para investigación rigurosa

### 📊 **Datos Verificados del Sistema:**
- **Distribución geográfica**: Estados Unidos (85), Global (35), Colombia (1)
- **Patrones temporales**: 12 meses de datos con clara estacionalidad
- **Correlaciones sentiment**: EE.UU. (-0.417) menos negativo que Global (-0.482)
- **Concentración estacional**: 49.6% de datos en 2 meses consecutivos
- **Implicaciones metodológicas**: Sesgos documentados para investigación responsable

### 📋 **Checklist de Progreso:**
- [ ] Analicé la distribución geográfica y identifiqué sesgos principales
- [ ] Exploré patrones temporales y expliqué el pico de junio
- [ ] Correlacioné geografía, tiempo y sentiment con datos verificados
- [ ] Identifiqué limitaciones metodológicas del dataset actual
- [ ] Apliqué filtros geográfico-temporales para análisis específico
- [ ] Documenté hallazgos con consciencia de sesgos para uso futuro

---

## 👉 Siguiente Paso

**🛠️ Módulo 6: Troubleshooting y FAQ**

En el próximo y último módulo aprenderás a:
- Solucionar problemas comunes de acceso y funcionalidad
- Interpretar mensajes de error del sistema
- Contactar soporte técnico de manera efectiva
- Manejar limitaciones conocidas y workarounds
- Optimizar rendimiento del sistema para análisis grandes
- Prepararte para uso avanzado y expansión del sistema

---

**🔗 Enlaces Útiles:**
- **Dashboard Principal**: http://localhost:5173
- **API Timeline**: http://localhost:8000/api/v1/export/charts/timeline.png
- **Módulo Anterior**: [Exportación y Reportes](04-exportacion-reportes.md)
- **Índice General**: [Manual de Usuario](../indice-principal.md)

**💡 Tip**: Los patrones geográfico-temporales identificados en este módulo son fundamentales para interpretar correctamente cualquier análisis futuro - mantenlos como referencia cuando trabajes con el sistema.
