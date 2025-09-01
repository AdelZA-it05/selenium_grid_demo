#!/bin/sh

# Немедленно завершаем скрипт при ошибке
set -e

# URL хаба (можно переопределить переменной окружения). Пингуем /status (не /wd/hub)
SELENOID_URL=${SELENOID_URL:-http://selenoid:4444/wd/hub}

echo "Waiting for Selenoid at ${SELENOID_URL%/wd/hub}/status ..."
for i in $(seq 1 120); do
  if curl -fsS "${SELENOID_URL%/wd/hub}/status" >/dev/null; then
    echo "Selenoid is up"
    exit 0
  fi
  sleep 1
done
echo "Timeout waiting for Selenoid"
exit 1


