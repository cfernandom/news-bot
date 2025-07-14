# Metodología de Procesamiento de Imágenes - Pattern Seeker

## **INTRODUCCIÓN TÉCNICA**

La preparación de datos influye directamente en la calidad del sistema de inteligencia artificial desarrollado. En el contexto específico de la detección temprana del cáncer de seno, se adquiere relevancia crítica relacionada con la precisión diagnóstica, afectando directamente el pronóstico de supervivencia de los pacientes.

### **Desafíos del Procesamiento Médico**
- Preservación de información clínica crítica
- Estandarización para procesamiento computacional eficiente
- Equilibrio entre calidad diagnóstica y eficiencia técnica
- Validación médica de transformaciones aplicadas

## **ADQUISICIÓN DEL DATASET**

### **Fuente de Datos Verificada**
- **Repositorio:** The Cancer Imaging Archive (TCIA)
- **Respaldo:** National Cancer Institute (NIH)
- **Programa:** Cancer Imaging Program (CIP)
- **Software:** NBIA Data Retriever (versión Windows)

### **Composición del Dataset**
- **Total de imágenes:** 4,137 analizadas
- **Pacientes únicos:** 626
- **Registros de estudios:** 1,546
- **Volumen de datos:** Más de 100GB procesados

### **Variables Incluidas**
- Densidad mamaria (1, 2, 3, 4)
- Patología (Benigno, Maligno, Benigno en seguimiento)
- Tipo de anormalidad y calcificación
- Lado (izquierdo/derecho), vista (CC/MLO)
- Nivel de sutileza (1-5)

### **Distribución Estadística**

#### **Densidad Mamaria (ACR)**
- Tipo 1 (grasa): 11.3%
- Tipo 2 (mixta): 32.4%
- Tipo 3 (densa): 34.9%
- Tipo 4 (extremadamente densa): 21.4%

#### **Distribución Anatómica**
- Lado izquierdo: 52.9%
- Lado derecho: 47.1%
- Vista CC (craneocaudal): 47.8%
- Vista MLO (mediolateral oblicua): 52.2%

#### **Clasificación Patológica**
- Maligno: 35.2%
- Benigno: 34.2%
- Benigno con seguimiento: 30.7%

#### **Tipos de Calcificación Predominantes**
- Pleomórfica: 42.9%
- Amorfa: 8.9%
- Puntiforme: 6.9%
- Centro lucente: 6.0%
- Vascular: 5.3%
- Ramificación lineal fina: 5.0%

## **CRITERIOS DE SELECCIÓN Y CLASIFICACIÓN**

### **Clasificación por Tipos de Imagen**

#### **Imágenes Tipo 1 (Originales)**
- **Descripción:** Mamografías completas originales
- **Características:** Escala de grises, campo completo
- **Tejidos visibles:** Graso, fibroglandular, denso
- **Uso:** Clasificación de densidad, análisis contextual

#### **Imágenes Tipo 2 (Máscaras ROI)**
- **Descripción:** Regiones de interés segmentadas
- **Características:** Fondo negro, zona blanca irregular
- **Propósito:** Delimitación exacta de anormalidades
- **Uso:** Segmentación precisa, análisis morfológico

### **Lógica de Procesamiento Implementada**

#### **Para Imágenes Tipo 1:**
- Clasificación de densidad mamaria
- Detección global de patrones
- Análisis de distribución de calcificaciones
- Clasificación patológica (maligno/benigno/seguimiento)

#### **Para Imágenes Tipo 2:**
- Segmentación precisa de calcificaciones
- Análisis morfológico detallado
- Entrenamiento de detectores automáticos
- Caracterización específica de anomalías

## **PREPROCESAMIENTO Y NORMALIZACIÓN**

### **Visor de Datos Especializado**
- **Formato:** HTML responsivo
- **Registros:** 1,546 organizados
- **Columnas:** 14 variables relevantes
- **Funcionalidades:** Filtros tiempo real, búsquedas, estadísticas

#### **Características del Visor**
- Códigos de color BI-RADS: Gris (0), Verde (2), Amarillo (3), Naranja (4), Rojo (5)
- Indicadores de patología visuales
- Círculos numerados para densidad mamaria
- Estadísticas en tiempo real según filtros

### **Clasificación Automatizada por Scripts**

#### **1. Clasificación por Densidad**
- **Objetivo:** Organizar según densidad ACR
- **Método:** Script automatizado Python
- **Resultado:** 4 categorías balanceadas
- **Validación:** Contraste con archivo CSV base

#### **2. Clasificación por Patología**
- **Categorías:** Benigno, Maligno, Benigno en Seguimiento
- **Proceso:** Subdivisión automática por densidad
- **Trazabilidad:** ID de paciente preservado
- **Control:** Verificación manual de categorías

#### **3. Clasificación por Tipo de Calcificación**
- **Tipos identificados:** 8 categorías principales
- **Manejo:** Imágenes sin clasificar aisladas
- **Proceso:** Validación automática + manual
- **Resultado:** Dataset limpio y categorizado

#### **4. Clasificación por Distribución**
- **Patrones:** Clustered, Linear, Segmental, Regional, Diffusely_Scattered
- **Método:** Script de clasificación automática
- **Validación:** Contraste con información médica
- **Depuración:** Eliminación de casos sin clasificar

## **ANÁLISIS DE RESOLUCIONES Y NORMALIZACIÓN**

### **Estadísticas del Dataset Completo**

#### **Métricas Generales**
- **Total de imágenes analizadas:** 4,137
- **Resoluciones únicas encontradas:** 2,317
- **Resolución máxima:** 4064x5592 (22.7MP)
- **Resolución mínima:** 113x129 (0.01MP)
- **Promedio ponderado:** 12.95 MP

#### **Distribución por Rangos de Megapíxeles**
- **Muy Baja (<1MP):** 18.3%
- **Baja (1-5 MP):** 0.0%
- **Media (5-15 MP):** 51.4%
- **Alta (15-25 MP):** 30.3%
- **Muy Alta (>25MP):** 0.0%

#### **Análisis de Percentiles**
- **P50 (mediana):** 3088x4608 (14.2 MP)
- **P75:** 2911x5491 (16.0 MP)
- **P90:** 4064x5592 (22.7 MP)
- **P95-P99:** 4040x5720 (23.1 MP)

### **Decisión de Normalización**

#### **Tamaño Seleccionado: 2048x2048 píxeles**
- **Justificación técnica:** Balance entre calidad y eficiencia
- **Preservación diagnóstica:** Características críticas mantenidas
- **Compatibilidad:** Campo de visión mamográfico típico
- **Procesamiento:** Optimizado para CNN profundas

#### **Impacto de la Normalización**
- **Sin pérdida:** 26 imágenes (18.3%)
- **Requieren recorte:** 116 imágenes (81.7%)
- **Necesitan upscaling:** 26 imágenes (18.3%)
- **Calidad preservada:** Información diagnóstica mantenida

## **TÉCNICAS DE AUMENTO DE DATOS**

### **Justificación Clínica**
- Variaciones naturales en posicionamiento del paciente
- Diferencias en técnicas de adquisición radiológica
- Preservación de clasificación BI-RADS de densidad
- Mantenimiento de arquitectura morfológica compleja

### **Framework de Implementación**
- **Biblioteca principal:** Albumentations (Python)
- **Detección automática:** Dimensiones por análisis estadístico
- **Preservación:** Relación de aspecto original
- **Validación:** Relevancia clínica mantenida

### **Transformaciones Implementadas**

#### **Geométricas**
- **Rotación:** ±15° (probabilidad 0.7)
  - Simula variaciones en posicionamiento
  - Preserva orientación anatómica
- **Traslación:** ±10% (probabilidad 0.5)
  - Reproduce diferencias en centrado
  - Mantiene estructura principal
- **Escalado:** 0.9-1.1 (probabilidad 0.5)
  - Simula diferencias distancia foco-receptor
  - Preserva proporciones diagnósticas

#### **Fotométricas**
- **Brillo/Contraste:** ±20% (probabilidad 0.7)
  - Aborda diferencias técnicas radiológicas
  - Simula variaciones en exposición
- **Corrección Gamma:** 0.8-1.2 (probabilidad 0.5)
  - Emula respuesta del detector
  - Normaliza características de imagen
- **CLAHE:** clip=2.0 (probabilidad 0.5)
  - Contraste local adaptativo
  - Realza estructuras sutiles en tejidos densos

#### **Morfológicas**
- **Deformación Elástica:** α=1, σ=500 (probabilidad 0.3)
  - Simula compresión tisular variable
  - Preserva características morfológicas

#### **Estocásticas**
- **Ruido Gaussiano:** σ=10-50 (probabilidad 0.3)
  - Simula condiciones de adquisición
  - Mejora robustez del modelo

### **Estrategia de Balanceo**
- **Objetivo:** 20,000 imágenes por categoría BI-RADS
- **Método:** Aumento dirigido según necesidad
- **Resultados:**
  - Tipo A (Grasa): 9,450 → 20,000 (factor 2.12×)
  - Tipo B (Mixta): 10,680 → 20,000 (factor 1.87×)
  - Tipo C (Densa): 13,320 → 20,000 (factor 1.50×)
  - Tipo D (Extrema): 8,180 → 20,000 (factor 2.45×)

## **VALIDACIÓN Y CONTROL DE CALIDAD**

### **Protocolo de Validación**
- **Revisión médica:** Especialistas oncólogos
- **Preservación clínica:** Características diagnósticas
- **Control de artefactos:** Eliminación de distorsiones
- **Trazabilidad:** Seguimiento de transformaciones

### **Criterios de Calidad**
- **Información diagnóstica:** Completamente preservada
- **Características morfológicas:** Sin alteración significativa
- **Gradientes de gris:** Mantenidos para Tipo 1
- **Segmentación binaria:** Optimizada para Tipo 2

### **Herramientas de Monitoreo**
- **Scripts de validación:** Automáticos
- **Métricas de calidad:** Implementadas
- **Reportes de estado:** Generados automáticamente
- **Alertas de inconsistencia:** Sistema implementado

## **ARQUITECTURA TÉCNICA DEL PROCESAMIENTO**

### **Diagrama de Flujo Principal**
1. **Carga y análisis inicial**
2. **Clasificación automática por tipos**
3. **Organización por categorías médicas**
4. **Análisis estadístico de resoluciones**
5. **Normalización a tamaño objetivo**
6. **Aplicación de técnicas de aumento**
7. **Validación de calidad final**
8. **Generación de dataset equilibrado**

### **Implementación en Python**
- **Bibliotecas utilizadas:** OpenCV, NumPy, Pandas, Albumentations
- **Procesamiento:** Paralelo cuando es posible
- **Memoria:** Optimización para datasets grandes
- **Escalabilidad:** Diseño modular y extensible

## **RESULTADOS Y IMPACTO**

### **Dataset Final Generado**
- **Imágenes balanceadas:** 80,000 (20k por categoría BI-RADS)
- **Calidad preservada:** Validación médica confirmada
- **Diversidad aumentada:** Robustez mejorada para entrenamiento
- **Representatividad:** Casos clínicos diversos incluidos

### **Contribución Metodológica**
- **Pipeline reproducible:** Metodología documentada
- **Herramientas reutilizables:** Scripts generalizables
- **Estándares establecidos:** Para procesamiento médico
- **Base para investigación:** Futura expansión posible

Esta metodología proporciona una base sólida para sistemas de screening mamográfico automatizado que pueden contribuir significativamente a la detección temprana de cáncer de mama, especialmente en contextos con recursos limitados como las zonas rurales colombianas.