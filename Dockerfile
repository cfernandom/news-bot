FROM python:3.13-slim

# Evitar archivos pyc y hacer output inmediato
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Instalar cron, dependencias del sistema y dependencias para Playwright
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        cron \
        bash \
        gettext \
        curl \
        wget \
        gnupg \
        unzip \
        fonts-liberation \
        libatk-bridge2.0-0 \
        libatk1.0-0 \
        libcups2 \
        libdbus-1-3 \
        libgdk-pixbuf2.0-0 \
        libnspr4 \
        libnss3 \
        libx11-xcb1 \
        libxcomposite1 \
        libxdamage1 \
        libxrandr2 \
        xdg-utils \
        libgbm1 \
        libasound2 \
    && rm -rf /var/lib/apt/lists/*

# Crear usuario no-root para ejecutar el bot
RUN useradd --create-home botuser

# Crear directorios de trabajo y logs
WORKDIR /app
RUN mkdir -p /app/logs
RUN chown -R botuser:botuser /app

# Copiar y preparar código
COPY --chown=botuser:botuser . /app

# Instalar dependencias de Python
RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Instalar navegadores de Playwright
RUN playwright install --with-deps

# Copiar scripts de entrada y cron
COPY --chown=botuser:botuser entrypoint.sh /entrypoint.sh
COPY --chown=botuser:botuser crontab.template /crontab.template
COPY --chown=botuser:botuser run_bot.sh /app/run_bot.sh

RUN chmod +x /entrypoint.sh /app/run_bot.sh

ENTRYPOINT ["/entrypoint.sh"]
