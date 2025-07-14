# Contenido Verificado para PreventIA

## **INFORMACIÓN DEL PROYECTO (VERIFICADA)**

### **Datos del Dataset Real**
- **Fuente:** The Cancer Imaging Archive (TCIA)
- **Respaldo:** National Cancer Institute (NIH)
- **Total imágenes:** 4,137 imágenes analizadas
- **Pacientes:** 626 pacientes únicos
- **Registros:** 1,546 estudios mamográficos
- **Volumen:** Más de 100GB de datos procesados

### **Distribución del Dataset**
- **Densidad mamaria:**
  - Tipo 1 (grasa): 11.3%
  - Tipo 2 (mixta): 32.4%
  - Tipo 3 (densa): 34.9%
  - Tipo 4 (extrema): 21.4%

- **Lateralidad:**
  - Izquierdo: 52.9%
  - Derecho: 47.1%

- **Vistas radiológicas:**
  - CC (craneocaudal): 47.8%
  - MLO (mediolateral oblicua): 52.2%

- **Clasificación patológica:**
  - Maligno: 35.2%
  - Benigno: 34.2%
  - Benigno en seguimiento: 30.7%

### **Tipos de Calcificación Analizados**
- Pleomórfica: 42.9%
- Amorfa: 8.9%
- Puntiforme: 6.9%
- Centro lucente: 6.0%
- Vascular: 5.3%
- Ramificación lineal fina: 5.0%

## **MODELO PATTERN SEEKER (INFORMACIÓN TÉCNICA)**

### **Innovación Principal**
- **Filtros gaussianos adaptativos** integrados en CNN
- **Mecanismo de atención local-global** balanceado
- **Arquitectura combinacional** para extracción de características
- **4 bloques convolucionales** consecutivos

### **Especificaciones Técnicas**
- **Normalización:** 2048x2048 píxeles
- **Resoluciones procesadas:** 2,317 resoluciones únicas
- **Rango de resolución:** 113x129 hasta 4064x5592 píxeles
- **Promedio ponderado:** 12.95 megapíxeles

### **Metodología de Procesamiento**
1. **Clasificación inicial:** Tipo 1 (originales) y Tipo 2 (máscaras ROI)
2. **Visor de datos:** HTML especializado con 1,546 registros
3. **4 niveles de clasificación:** densidad, patología, calcificación, distribución
4. **Técnicas de aumento:** Preservando características diagnósticas

### **Ecuaciones Fundamentales**
- **Imagen base:** I ∈ R^(H×W×C)
- **Filtro gaussiano:** G(x,y) = (1/2πσ²)e^(-(x²+y²)/2σ²)
- **Atención local-global:** A_final = αA_local + (1-α)A_global
- **Optimizadores evaluados:** Adam y AdamW

## **EQUIPO DE INVESTIGACIÓN (VERIFICADO)**

### **Investigadores Confirmados**
1. **Ing. Angie Paola Rique Sabogal**
   - Rol: Directora del Proyecto
   - Especialidad: Ingeniera Electrónica

2. **Ing. Neider Duan Barbosa Castro**
   - Rol: Ingeniero de Sistemas
   - Especialidad: Sistemas

3. **Ing. Miguel Angel Guatame Medina**
   - Rol: Especialista en Seguridad Informática
   - Especialidad: Ingeniero de Sistemas

4. **Ing. Cristhian Fernando Moreno Manrique**
   - Rol: Ingeniero Electrónico
   - Especialidad: Desarrollador Full Stack

### **Institución**
- **Universidad:** Fundación Universitaria Compensar
- **Facultad:** Ingeniería
- **Enfoque:** Investigación aplicada en IA médica

## **OBJETIVO Y ALCANCE**

### **Problemática Específica**
- **Zonas objetivo:** Municipios categoría 4, 5 y 6 de Colombia
- **Limitaciones:** Acceso limitado a tecnología diagnóstica especializada
- **Impacto esperado:** Democratización del diagnóstico temprano

### **Aplicaciones Planificadas**

#### **Software para Profesionales**
- Sistema multiplataforma
- Integración del modelo Pattern Seeker
- Interfaz especializada para diagnóstico asistido
- Validación clínica en desarrollo

#### **Aplicación Comunitaria**
- Módulo educativo sobre cáncer de seno
- Sistema de actualizaciones
- Visualización de análisis estadísticos
- Guía interactiva de autoexamen
- Directorio de instituciones de salud

## **ESTADO ACTUAL DEL PROYECTO**

### **Fases Completadas**
- ✅ Adquisición y procesamiento del dataset
- ✅ Desarrollo del modelo matemático Pattern Seeker
- ✅ Implementación de filtros gaussianos adaptativos
- ✅ Visor de datos CSV especializado
- ✅ Metodología de normalización establecida

### **En Desarrollo**
- 🔄 Validación clínica del modelo
- 🔄 Software especializado para profesionales
- 🔄 Aplicación comunitaria
- 🔄 Optimización computacional

### **Pendiente**
- ⏳ Publicaciones científicas en revisión
- ⏳ Pruebas piloto en instituciones
- ⏳ Implementación en zonas rurales
- ⏳ Certificaciones médicas

## **DISCLAIMERS IMPORTANTES**

### **Estado de Desarrollo**
- Este es un proyecto de investigación académica en desarrollo
- Los resultados están sujetos a validación clínica
- No sustituye la consulta médica profesional
- La información tiene fines educativos y de investigación

### **Limitaciones Actuales**
- Modelo en fase de optimización
- Pendiente validación con especialistas oncólogos
- Resultados preliminares sujetos a confirmación
- Implementación clínica en evaluación

## **INFORMACIÓN MÉDICA VERIFICADA**

### **Detección Temprana**
- Supervivencia a 5 años en etapa I: 99%
- Importancia del diagnóstico precoz confirmada
- Factores de riesgo establecidos por literatura médica

### **Recomendaciones de Tamizaje**
- Basadas en guías internacionales (American Cancer Society)
- Adaptaciones para contexto colombiano en evaluación
- Autoexamen mensual recomendado
- Mamografía según grupos etarios

### **Señales de Alerta (Confirmadas)**
- Bultos o masas palpables
- Cambios en forma/tamaño del seno
- Secreción del pezón (especialmente hemática)
- Alteraciones cutáneas
- Retracción del pezón
- Dolor persistente no cíclico

## **RECURSOS COMUNITARIOS**

### **Líneas de Emergencia (Verificar Actualización)**
- 123 - Emergencias nacionales
- Liga Contra el Cáncer: 01-8000-423-000
- Apoyo Emocional: 01-8000-113-012
- Información EPS: 01-8000-951-097

### **Instituciones de Referencia**
- Instituto Nacional de Cancerología
- Liga Colombiana Contra el Cáncer
- Fundación Santa Fe de Bogotá
- Hospital Universitario Nacional
- (Directorio completo requiere verificación 2024)

## **NOTAS PARA IMPLEMENTACIÓN**

### **Prioridades de Contenido**
1. Mantener utilidad comunitaria
2. Presentar investigación con transparencia
3. Incluir disclaimers apropiados
4. Verificar datos de contacto institucionales

### **Aspectos Técnicos**
- Preservar diseño y UX actual
- Mantener accesibilidad web
- Optimizar para dispositivos móviles
- Incluir enlaces a fuentes verificables