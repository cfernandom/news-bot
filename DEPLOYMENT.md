# Guía de Despliegue – Bot de Noticias sobre Cáncer de Mama

El presente documento describe el procedimiento para la implementación del sistema autónomo de recopilación y publicación de noticias relacionadas con el cáncer de mama. Este proyecto ha sido diseñado para operar de manera periódica y autónoma, generando contenido susceptible de ser publicado en una plataforma WordPress mediante su interfaz de programación de aplicaciones (API).

---

## Requisitos del Sistema

* Docker ≥ 20.10
* Docker Compose ≥ 2
* Acceso a una terminal compatible con entornos Unix (Linux/macOS o Subsistema de Windows para Linux en Windows)
* Credenciales de OpenAI para la generación de contenido (requiere una cuenta de OpenAI).
* Credenciales de WordPress (usuario y contraseña de aplicación para acceso API).

---

## Estructura del Proyecto

```bash
.
├── docker-compose.yml
├── Dockerfile
├── entrypoint.sh
├── crontab.template
├── run_bot.sh
├── requirements.txt
├── .env                 # Configuración sensible (no versionado)
└── services/            # Código principal del sistema
``` 

---

## Preparación del Entorno

### 1. Clonación del Repositorio

```bash
git clone https://github.com/cfernandom/news-bot
cd news-bot
```

---

### 2. Creación del Archivo `.env`

Se recomienda copiar el archivo `.env.template` (si estuviera presente) o crear un archivo con el nombre `.env` de forma manual, incluyendo las siguientes variables de entorno:

```ini
# 🔑 Clave de API para OpenAI
OPENAI_API_KEY=sk-...

# 🔗 WordPress REST API
WP_BASE_URL=https://tusitio.com
WP_USER=tu_usuario
WP_PASSWORD=tu_password_seguro

# Configuración de ejecución automática
WEEKLY_DAY=1               # (Lunes=0, Domingo=6)
WEEKLY_TIME=06:00          # Hora de ejecución (formato HH:MM)
DAYS_INTERVAL=3            # (Ejecutar cada N días) — opcional: Si WEEKLY_DAY no se define, se usará DAYS_INTERVAL
```

---

### 3. Construcción e Inicio del Contenedor

```bash
docker compose up --build -d
```

Esta instrucción compila la imagen del contenedor, configura el entorno y establece la tarea `cron` interna para la ejecución recurrente del bot en el horario especificado.

---

### 4. Verificación de Registros (Logs)

Para supervisar la ejecución automática del bot, puede utilizar el siguiente comando:

```bash
docker compose logs -f newsbot
```

---

### 5. Ejecución Manual Forzada

En caso de requerir la ejecución inmediata del bot, sin esperar la próxima ejecución programada, utilice el siguiente comando:

```bash
docker compose exec newsbot /app/run_bot.sh
```

---

### 6. Detener y Eliminar el Contenedor
Para detener y eliminar el contenedor, así como los volúmenes asociados, ejecute:

```bash
docker compose down --volumes
```
Esto eliminará todos los datos generados por el bot, incluyendo las publicaciones en WordPress.
Si desea conservar los datos generados, puede omitir la opción `--volumes`.

---

## 🔄 Despliegue Continuo (Opcional)

Para automatizar los despliegues desde GitHub, se pueden emplear Acciones de GitHub (GitHub Actions) con ejecutores (runners) que ejecuten las siguientes instrucciones:

```bash
docker compose pull
docker compose up -d --build
```

---

## 🔐 Seguridad y Buenas Prácticas

* **Se recomienda no compartir públicamente el archivo `.env`** ni incluirlo en el repositorio del proyecto.
* Asegúrese de utilizar el protocolo **HTTPS** en su instalación de WordPress.
* Restrinja el acceso de la cuenta de la API en WordPress únicamente a las funcionalidades necesarias.
* Implemente archivos `.dockerignore` y `.gitignore` para excluir archivos sensibles del repositorio y de la imagen del contenedor.

---

## 📤 Publicación de Contenido

Una vez implementado de forma exitosa, el bot ejecutará su flujo de trabajo, que comprende las etapas de extracción de información (scraping), procesamiento del lenguaje natural (NLP), toma de decisiones, redacción (copywriting) y publicación en WordPress, de acuerdo con la programación definida en la configuración de `cron`.