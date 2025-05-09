FROM python:3.14-slim

# Evitar archivos pyc y hacer output inmediato
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Instala cron y dependencias del sistema, limpia cache
RUN apt-get update \
    && apt-get install -y --no-install-recommends cron bash \
    && rm -rf /var/lib/apt/lists/*

# Crear usuario no-root para ejecutar el bot
RUN useradd --create-home botuser

# Crea directorios de trabajo y logs
WORKDIR /app
RUN mkdir -p /app/logs
RUN chown -R botuser:botuser /app

# Copiar y preparar código
COPY --chown=botuser:botuser . /app

# Instalar dependencias de Python con versiones fijas
RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Copiar scripts de entrypoint y cron
COPY --chown=botuser:botuser entrypoint.sh /entrypoint.sh
COPY --chown=botuser:botuser crontab.template /crontab.template
COPY --chown=botuser:botuser run_bot.sh /app/run_bot.sh
RUN chmod +x /entrypoint.sh

# Cambiar a usuario no-root
USER botuser

ENTRYPOINT ["/entrypoint.sh"]
