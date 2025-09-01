# Демонстрация Selenium + Selenoid (Docker Compose)

## Предварительные требования
- Docker и Docker Compose
- Python 3.10+

## Запуск Selenoid локально
```bash
cd /Users/sergeytsarev/selenium-selenoid-demo
mkdir -p selenoid/video selenoid/logs
docker compose up -d
```

- Хаб Selenoid: `http://localhost:4444/wd/hub`
- UI Selenoid: `http://localhost:8080`

## Установка зависимостей и запуск тестов локально
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pytest -q
```

## Запуск тестов через Docker Compose
```bash
docker compose up -d selenoid selenoid-ui
docker compose run --rm tests
```

Контейнер с тестами ждёт готовности Selenoid (healthcheck). Видео называются по `TEST_NAME` и сохраняются в `selenoid/video`.

Тест использует переменную `SELENOID_URL`, если она задана (по умолчанию `http://localhost:4444/wd/hub`).

## Видео и логи
- Видео: `selenoid/video`
- Логи драйверов: `selenoid/logs`

Также записи можно скачать через Selenoid UI после завершения сессии.

## Что делает каждый файл
- docker-compose.yml: поднимает Selenoid hub (порт 4444), Selenoid UI (порт 8080) и контейнер с тестами. Использует отдельную сеть `selenoid_grid`, чтобы браузерные контейнеры были доступны, а тесты могли резолвить хостнейм `selenoid`. На macOS путь к видео параметризован `OVERRIDE_VIDEO_OUTPUT_DIR`.
- selenoid/browsers.json: реестр доступных браузеров. Здесь используется `selenoid/chrome:121.0` (без VNC) с WebDriver на порту 4444. При необходимости корректируйте `default` и список версий.
- Dockerfile.tests: лёгкий Python‑образ с pytest + selenium (и curl), исходники монтируются при запуске.
- tests/test_google.py: пример Selenium‑теста, подключается к Selenoid как к удалённому WebDriver, включает VNC/видео через `selenoid:options`, закрывает окно согласия Google и проверяет заголовок.

## Частые вопросы
- Если меняется версия Chrome, обновите `selenoid/browsers.json` и `browserVersion` в тесте.
- На Apple Silicon можно увеличить ресурсы Docker Desktop (Settings → Resources).

## GitHub Actions
- Workflow `.github/workflows/ci.yml` поднимает Selenoid, затем выполняет `docker compose run --rm tests`.
- Видео и логи загружаются как артефакты job.
