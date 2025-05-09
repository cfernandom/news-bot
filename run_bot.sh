#!/usr/bin/env bash
set -euo pipefail

# Activar entorno virtual
if [[ -f "venv/bin/activate" ]]; then
    # shellcheck disable=SC1091
    source venv/bin/activate
else
    echo "ERROR: Entorno virtual venv no encontrado en $(pwd)/venv" >&2
    exit 1
fi

# Ejecutar pipeline y loguear
datetime=$(date --iso-8601=seconds)
echo "[$datetime] Iniciando pipeline" >> logs/run_bot.log
python main.py >> logs/run_bot.log 2>&1
exit_code=$?
echo "[$datetime] Pipeline finalizado con código $exit_code" >> logs/run_bot.log
exit $exit_code