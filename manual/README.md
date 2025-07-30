# Manual Técnico y de Operación - Sistema PreventIA News Analytics

**Versión:** 1.0
**Fecha:** 29 de Julio de 2025
**Estado:** Final

## Control de Versiones

| Versión | Fecha | Descripción | Autores |
|---------|-------|-------------|---------|
| 1.0 | 29 de Julio de 2025 | Versión Inicial del Documento | Equipo PreventIA |

## Tabla de Contenido

1. [Objetivo](#objetivo)
2. [Alcance](#alcance)
3. [Términos y Definiciones](#términos-y-definiciones)
4. [¿Qué es el Manual Técnico y de Operación del Sistema?](#qué-es-el-manual-técnico-y-de-operación-del-sistema)
5. [Introducción](#introducción)
6. [Estructura del Manual](#estructura-del-manual)
7. [Documentos Adicionales](#documentos-adicionales)

## Objetivo

El objetivo de este documento es brindar a las dependencias del proyecto PreventIA una guía completa para la operación del sistema de información PreventIA News Analytics, ilustrando sobre la definición, diseño, organización y estructura al personal encargado de mantener la prestación del servicio.

## Alcance

Este documento describe el contenido completo del manual técnico y de operación del sistema PreventIA News Analytics siguiendo los lineamientos del Departamento Nacional de Planeación (DNP) y las políticas de gobierno digital, así como las mejores prácticas internacionales de documentación técnica.

## Términos y Definiciones

### Términos Técnicos Generales

- **Navegador Web**: Software utilizado para visualizar la información contenida en los sitios de Internet
- **API (Application Programming Interface)**: Interfaz de programación que permite la comunicación entre componentes
- **Framework**: Conjunto de prácticas y estándares estructurado que permiten la consecución de objetivos
- **Microservicios**: Arquitectura de software donde las aplicaciones se estructuran como servicios independientes
- **Docker**: Plataforma de contenedorización para empaquetar aplicaciones y sus dependencias

### Términos Específicos del Sistema

- **Web Scraping**: Técnica automatizada de extracción de datos de sitios web
- **NLP (Natural Language Processing)**: Procesamiento de Lenguaje Natural para análisis de texto
- **VADER**: Herramienta de análisis de sentimiento basada en reglas y léxico
- **Compliance Score**: Puntuación de cumplimiento legal de fuentes de noticias (0.00 a 1.00)
- **JWT (JSON Web Token)**: Estándar para autenticación segura en el sistema

## ¿Qué es el Manual Técnico y de Operación del Sistema?

El manual técnico de PreventIA News Analytics tiene como propósito ilustrar sobre la definición, diseño, organización y estructura del sistema al personal encargado de mantener la prestación del servicio. Los lectores incluyen:

- Desarrolladores
- Arquitectos de software
- Ingenieros de pruebas
- Administradores de sistemas
- Personal de operaciones

## Introducción

PreventIA News Analytics es un sistema de información desarrollado en el marco del proyecto de investigación multidisciplinario PreventIA de la Fundación Universitaria Compensar. El sistema cumple con el ciclo de desarrollo de software ajustado a la metodología definida en la política de Gobierno Digital de MinTIC.

El presente documento aplica el lineamiento LI.SIS.16 que establece:

> "La dirección de Tecnologías y Sistemas de la Información o quien haga sus veces debe asegurar que todos sus sistemas de información cuenten con la documentación de usuario, técnica y de operación, debidamente actualizada, que asegure la transferencia de conocimiento hacia los usuarios, hacia la dirección de Tecnologías y Sistemas de la Información o quien haga sus veces y hacia los servicios de soporte tecnológico"

## Estructura del Manual

El manual técnico está organizado en los siguientes documentos:

### [01. Descripción del Sistema](01_DescripcionSistema.md)
- Índice del contenido
- Introducción al sistema
- Objetivos del sistema
- Módulos y funcionalidades principales

### [02. Diseño Técnico](02_DisenoTecnico.md)
- Esquema o modelo de requerimientos
- Software base del sistema y prerequisitos
- Componentes y estándares
- Modelo de datos
- Funcionalidad y servicios ofrecidos

### [03. Instalación y Configuración](03_InstalacionConfiguracion.md)
- Organización de componentes
- Instalación paso a paso
- Configuración del sistema
- Scripts de instalación

### [04. Despliegue](04_Despliegue.md)
- Diagramas de despliegue
- Configuración de producción
- Gestión de contenedores Docker
- Monitoreo y mantenimiento

### [05. Resolución de Problemas](05_ResolucionProblemas.md)
- Errores técnicos más comunes y su solución
- Diagnóstico rápido
- Procedimientos de recuperación
- FAQ técnico

## Documentos Adicionales

### [07. Referencia de API](07_APIReference.md)
- Documentación completa de endpoints
- Autenticación y autorización
- Modelos de datos y respuestas
- Ejemplos de uso en JavaScript y Python

### [Guía de Scripts](GUIA_SCRIPTS.md)
- Manual de uso de scripts automatizados
- Scripts de instalación y validación
- Herramientas de backup y mantenimiento
- Flujos de trabajo recomendados

### [Plan de Mejoras del Manual](PLAN_MEJORAS_MANUAL_TECNICO.md)
- Plan detallado de mejoras implementadas
- Cronograma de implementación
- Métricas de éxito y validación
- Estado actual del proyecto

### [Auditoría del Manual](AUDITORIA_MANUAL_TECNICO.md)
- Análisis de calidad de la documentación
- Identificación de mejoras necesarias
- Evaluación de completitud y precisión

## Información de Contacto

**Proyecto**: PreventIA - Fundación Universitaria Compensar
**Equipo de Desarrollo**: Grupo de Gestión de Sistemas de Información
**Soporte Técnico**: soporte@preventia.edu.co

---

*Este manual técnico ha sido elaborado siguiendo los lineamientos de la Guía para la Elaboración del Manual Técnico y de Operación de los Sistemas de Información del Departamento Nacional de Planeación (DNP) de Colombia.*
