#!/usr/bin/env bash

set -euo pipefail

# Verificar variables críticas
: "${OPENAI_API_KEY:?OPENAI_API_KEY no definida}"  # fallará si no existe
: "${WP_USER:?WP_USER no definida}"
: "${WP_PASSWORD:?WP_PASSWORD no definida}"

# Determinar programación: semanal o intervalo de días
# Si WEEKLY_DAY está definido, usar programación semanal
if [[ -n "${WEEKLY_DAY:-}" ]]; then
    # Hora y minuto para la ejecución (por defecto 08:00)
    WEEKLY_TIME="${WEEKLY_TIME:-08:00}"
    IFS=":" read -r HOUR MINUTE <<< "$WEEKLY_TIME"
    # Validar valores
    if [[ ! "$HOUR" =~ ^[0-9]{1,2}$ ]] || [[ ! "$MINUTE" =~ ^[0-9]{1,2}$ ]]; then
        echo "ERROR: WEEKLY_TIME inválido: '$WEEKLY_TIME'. Formato HH:MM" >&2
        exit 1
    fi
    # Cron: MIN HOUR * * DOW
    CRON_EXPR="$MINUTE $HOUR * * $WEEKLY_DAY"
else
    # Intervalo en días (entero)
    DAYS_INTERVAL="${DAYS_INTERVAL:-1}"
    if [[ ! "$DAYS_INTERVAL" =~ ^[0-9]+$ ]]; then
        echo "ERROR: DAYS_INTERVAL debe ser un número entero, no '$DAYS_INTERVAL'" >&2
        exit 1
    fi
    # Ejecutar a las 08:00 cada N días
    CRON_EXPR="0 8 */${DAYS_INTERVAL} * *"
fi

# Generar el crontab
envsubst '${CRON_EXPR}' < /crontab.template > /etc/cron.d/news-bot-cron
chmod 0644 /etc/cron.d/news-bot-cron
crontab /etc/cron.d/news-bot-cron

echo "🕒 Cron programado con: $CRON_EXPR"

echo "📅 Ejecución configurada: ";
if [[ -n "${WEEKLY_DAY:-}" ]]; then
    echo "Cada semana el día $WEEKLY_DAY a las ${WEEKLY_TIME:-08:00}."
else
    echo "Cada $DAYS_INTERVAL día(s) a las 08:00."
fi

# Iniciar cron en primer plano
cron -f