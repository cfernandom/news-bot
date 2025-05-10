#!/usr/bin/env bash
set -euo pipefail

datetime=$(date --iso-8601=seconds)
echo "[$datetime] Iniciando pipeline" >> logs/run_bot.log

python main.py >> logs/run_bot.log 2>&1
exit_code=$?

echo "[$datetime] Pipeline finalizado con código $exit_code" >> logs/run_bot.log
exit $exit_code
