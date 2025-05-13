#!/bin/bash
set -euo pipefail

# (Opcional) Comprobar que el script a ejecutar existe y es ejecutable
if [[ ! -x "/app/run_bot.sh" ]]; then
    echo "Error: /app/run_bot.sh no existe o no es ejecutable." >&2
    exit 1
fi

# Inicializar variables locales
MINUTE=""
HOUR=""
WEEKLY_DAY_NUM=""
DAYS_INTERVAL_NUM=""

# Validar y procesar WEEKLY_TIME y WEEKLY_DAY
if [[ -n "${WEEKLY_TIME:-}" || -n "${WEEKLY_DAY:-}" ]]; then
    if [[ -z "${WEEKLY_TIME:-}" || -z "${WEEKLY_DAY:-}" ]]; then
        echo "Error: debe especificar WEEKLY_TIME y WEEKLY_DAY juntos." >&2
        exit 1
    fi
    # Verificar formato HH:MM
    if [[ ! "$WEEKLY_TIME" =~ ^([0-1]?[0-9]|2[0-3]):([0-5]?[0-9])$ ]]; then
        echo "Error: WEEKLY_TIME inválido (se espera HH:MM)" >&2
        exit 1
    fi
    # Separar hora y minuto
    IFS=":" read -r HOUR STR_MINUTE <<< "$WEEKLY_TIME"
    # Verificar y convertir a entero (elimina ceros a la izquierda)
    if ! [[ "$WEEKLY_DAY" =~ ^[0-9]+$ ]]; then
        echo "Error: WEEKLY_DAY debe ser un número entero." >&2
        exit 1
    fi
    # Pasar a decimal para eliminar ceros iniciales
    WEEKLY_DAY_NUM=$((10#$WEEKLY_DAY))
    MINUTE=$((10#$STR_MINUTE))
    HOUR=$((10#$HOUR))
    # Rango válido de día de semana
    if (( WEEKLY_DAY_NUM < 0 || WEEKLY_DAY_NUM > 6 )); then
        echo "Error: WEEKLY_DAY fuera de rango (0-6)" >&2
        exit 1
    fi
    # Asegurar rango válido de hora y minuto
    if (( HOUR < 0 || HOUR > 23 || MINUTE < 0 || MINUTE > 59 )); then
        echo "Error: hora o minuto inválidos en WEEKLY_TIME." >&2
        exit 1
    fi
fi

# Validar y procesar DAYS_INTERVAL
if [[ -n "${DAYS_INTERVAL:-}" ]]; then
    # No permitir combinar semanal e intervalo al mismo tiempo
    if [[ -n "${WEEKLY_TIME:-}" ]]; then
        echo "Error: no se puede usar DAYS_INTERVAL junto con WEEKLY_TIME/WEEKLY_DAY." >&2
        exit 1
    fi
    if ! [[ "$DAYS_INTERVAL" =~ ^[0-9]+$ ]]; then
        echo "Error: DAYS_INTERVAL debe ser un entero." >&2
        exit 1
    fi
    DAYS_INTERVAL_NUM=$((10#$DAYS_INTERVAL))
    if (( DAYS_INTERVAL_NUM < 1 )); then
        echo "Error: DAYS_INTERVAL debe ser >= 1." >&2
        exit 1
    fi
fi

# Construir la línea de cron según el modo configurado
CRON_LINE=""
if [[ -n "${WEEKLY_TIME:-}" ]]; then
    # Modo semanal: minuto hora * * día_semana
    CRON_LINE="${MINUTE} ${HOUR} * * ${WEEKLY_DAY_NUM} /app/run_bot.sh"
    echo "Configurando cron para ejecutar semanalmente a las ${WEEKLY_TIME} el día ${WEEKLY_DAY_NUM}"
elif [[ -n "${DAYS_INTERVAL:-}" ]]; then
    # Modo intervalo de días: 00:00 cada N días
    CRON_LINE="0 0 */${DAYS_INTERVAL_NUM} * * /app/run_bot.sh"
    echo "Configurando cron para ejecutar cada ${DAYS_INTERVAL_NUM} días a las 00:00"
else
    # Sin programación configurada
    CRON_LINE="# No se ha configurado una programación de cron"
fi

# Escribir el cronfile en /etc/cron.d/news-bot-cron
echo "${CRON_LINE}" > /etc/cron.d/news-bot-cron
# Establecer permisos seguros
chmod 0600 /etc/cron.d/news-bot-cron

# Cargar el crontab (modo usuario, sin campo de usuario en la línea)
crontab /etc/cron.d/news-bot-cron

# Iniciar cron en primer plano (foreground) para que el contenedor no se detenga
echo "Cron job configurado: ${CRON_LINE}"
exec cron -f
