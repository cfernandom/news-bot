# Configuración de Entorno Docker para Desarrollo

Este documento detalla cómo configurar y gestionar el entorno de desarrollo de PreventIA News Analytics utilizando Docker y Docker Compose. Esto permite un entorno consistente y aislado para todos los desarrolladores.

## 1. Visión General de Docker en el Proyecto

El proyecto PreventIA News Analytics utiliza Docker para contenerizar sus diversos servicios, asegurando que las dependencias y el entorno de ejecución sean idénticos en todas las máquinas de desarrollo y producción.

Los servicios principales que se ejecutan en Docker son:
*   **`postgres`**: Base de datos PostgreSQL para almacenar artículos y datos analíticos.
*   **`api`**: La API de FastAPI que expone los endpoints para el dashboard y otros servicios.
*   **`analytics_service`**: Un servicio de análisis en segundo plano (posiblemente el bot de noticias o un procesador de datos).
*   **`frontend`**: El dashboard de React en modo de desarrollo.
*   **`redis`**: Una instancia de Redis para caching o gestión de colas.

## 2. Prerrequisitos

Asegúrate de tener instalados los siguientes componentes en tu sistema:
*   **Docker Engine**: Versión 20.10 o superior.
*   **Docker Compose**: Versión 2 o superior.

Puedes verificar tus versiones ejecutando:
```bash
docker --version
docker compose version
```

## 3. Componentes Clave de Docker

### `docker-compose.yml`

Este archivo define la configuración de todos los servicios que componen el entorno de desarrollo. Incluye la configuración de la red, volúmenes, puertos, variables de entorno y dependencias entre servicios.

*   **`postgres`**: Utiliza la imagen `postgres:16-alpine`. Los datos se persisten en un volumen (`postgres_data`) y se mapea el puerto `5433` del host al `5432` del contenedor.
*   **`api`**: Construido a partir de `Dockerfile.api`. Expone el puerto `8000`. Depende de `postgres`.
*   **`analytics_service`**: Construido a partir de `Dockerfile`. Este servicio parece ser el bot de noticias o un procesador de datos en segundo plano.
*   **`frontend`**: Construido a partir de `preventia-dashboard/Dockerfile.dev`. Expone el puerto `3000` del host al `5173` del contenedor (puerto de desarrollo de Vite). Monta el código fuente local para facilitar el desarrollo.
*   **`redis`**: Utiliza la imagen `redis:8-alpine`. Los datos se persisten en un volumen (`redis_data`) y se mapea el puerto `6379`.

### Dockerfiles

*   **`Dockerfile`**: Utilizado por el servicio `analytics_service`. Configura un entorno Python con Playwright y cron para tareas programadas.
*   **`Dockerfile.api`**: Utilizado por el servicio `api`. Configura un entorno Python para la aplicación FastAPI.
*   **`Dockerfile.api.prod`**: Una versión optimizada para producción de la API de FastAPI, utilizando Gunicorn y un usuario no-root. No se usa directamente en `docker-compose.yml` de desarrollo, pero es relevante para el despliegue en producción.
*   **`preventia-dashboard/Dockerfile.dev`**: Utilizado por el servicio `frontend`. Configura un entorno Node.js para el desarrollo del dashboard de React.

## 4. Configuración del Entorno de Desarrollo

1.  **Clonar el Repositorio:**
    ```bash
    git clone <URL_DEL_REPOSITORIO>
    cd news_bot_3
    ```

2.  **Configurar Variables de Entorno:**
    Crea un archivo `.env` en la raíz del proyecto. Puedes usar `.env.template` como base. Este archivo contendrá variables como credenciales de base de datos y claves de API.
    ```ini
    # Ejemplo de .env
    POSTGRES_DB=preventia_news
    POSTGRES_USER=preventia
    POSTGRES_PASSWORD=preventia123
    OPENAI_API_KEY=tu_clave_openai
    # Otras variables necesarias para analytics_service o frontend
    ```

3.  **Iniciar los Servicios Docker:**
    Desde la raíz del proyecto, ejecuta:
    ```bash
    docker compose up --build -d
    ```
    *   `up`: Inicia los servicios definidos en `docker-compose.yml`.
    *   `--build`: Reconstruye las imágenes de los servicios si hay cambios en los Dockerfiles o en el contexto de construcción.
    *   `-d`: Ejecuta los contenedores en modo "detached" (en segundo plano).

    La primera vez que ejecutes este comando, Docker descargará las imágenes necesarias y construirá las imágenes personalizadas, lo que puede tardar unos minutos.

## 5. Gestión de Servicios Docker

*   **Verificar el Estado de los Servicios:**
    ```bash
    docker compose ps
    ```

*   **Ver los Logs de un Servicio:**
    Para ver los logs en tiempo real de un servicio (ej. `api`):
    ```bash
    docker compose logs -f api
    ```
    Reemplaza `api` por el nombre del servicio que desees inspeccionar (`postgres`, `analytics_service`, `frontend`, `redis`).

*   **Detener los Servicios:**
    ```bash
    docker compose stop
    ```

*   **Detener y Eliminar los Contenedores y Redes:**
    ```bash
    docker compose down
    ```

*   **Detener y Eliminar Contenedores, Redes y Volúmenes (¡Cuidado! Esto eliminará los datos de la base de datos):**
    ```bash
    docker compose down --volumes
    ```

*   **Ejecutar Comandos dentro de un Contenedor:**
    Para ejecutar un comando dentro de un contenedor en ejecución (ej. abrir un shell bash en el contenedor `api`):
    ```bash
    docker compose exec api bash
    ```

## 6. Consideraciones para Producción

Aunque este documento se centra en el desarrollo, es importante notar que el proyecto también incluye configuraciones para producción.

*   **`Dockerfile.api.prod`**: Este Dockerfile está optimizado para el despliegue de la API en producción, utilizando Gunicorn y un usuario no-root para mayor seguridad y rendimiento.
*   **`docker-compose.prod.yml`**: (No incluido en este documento, pero referenciado en la documentación de despliegue) Este archivo define la configuración de los servicios para un entorno de producción, incluyendo Nginx como proxy inverso y otras optimizaciones.

Para detalles sobre el despliegue en producción, consulta:
*   [docs/implementation/production-deployment-roadmap.md](../../implementation/production-deployment-roadmap.md)
*   [DEPLOYMENT.md](../../../DEPLOYMENT.md) (para el bot de noticias específico)
