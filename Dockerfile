## Базовый образ с Python 3.11 (минимальный debian‑slim)
FROM python:3.11-slim

## Рабочая директория приложения внутри контейнера
WORKDIR /app

## Устанавливаем системные утилиты (curl) — используем для health/wait и отладки
RUN apt-get update \
    && apt-get install -y --no-install-recommends curl \
    && rm -rf /var/lib/apt/lists/*

## Python‑зависимости устанавливаем отдельно — это ускорит сборку при неизменных deps
COPY requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt

## Исходники монтируются во время запуска; команду задаёт docker-compose
CMD ["pytest", "-q"]


