# Selenium + Selenoid (Docker Compose) demo

## Prerequisites
- Docker and Docker Compose
- Python 3.10+

## Start Selenoid stack
```bash
cd /Users/sergeytsarev/selenium-selenoid-demo
mkdir -p selenoid/video selenoid/logs
docker compose up -d
```

- Selenoid hub: `http://localhost:4444/wd/hub`
- Selenoid UI: `http://localhost:8080`

## Install deps and run tests locally
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pytest -q
```

## Run tests via Docker Compose
```bash
docker compose up -d selenoid selenoid-ui
docker compose run --rm tests
```

The tests container waits until Selenoid is ready. Videos are named after `TEST_NAME` and stored in `selenoid/video`.

The test uses `SELENOID_URL` env var if set (defaults to `http://localhost:4444/wd/hub`).

## Videos and logs
- Videos are saved to `selenoid/video`
- Driver logs are saved to `selenoid/logs`

You can also download recordings from Selenoid UI after the session completes.

## Что делает каждый файл
- docker-compose.yml: поднимает Selenoid hub (порт 4444), Selenoid UI (порт 8080) и контейнер с тестами. Использует отдельную сеть `selenoid_grid`, чтобы браузерные контейнеры были доступны, а тесты могли резолвить хостнейм `selenoid`. На macOS каталог видео смонтирован в путь, расшаренный в Docker Desktop.
- selenoid/browsers.json: реестр доступных браузеров. Здесь используется `selenoid/chrome:121.0` (без VNC) с WebDriver на порту 4444. При необходимости корректируйте `default` и список версий.
- scripts/wait-for-selenoid.sh: простой скрипт ожидания готовности, который пингует `http://selenoid:4444/status` перед запуском pytest.
- Dockerfile.tests: лёгкий Python‑образ с pytest + selenium и curl для скрипта ожидания. Папка проекта монтируется при запуске, чтобы можно было менять код без пересборки.
- tests/test_google.py: пример Selenium‑теста, подключается к Selenoid как к удалённому WebDriver, задаёт имя видео через `selenoid:options`, закрывает окно согласия Google и проверяет заголовок.

## Common issues
- If Chrome version changes, update `selenoid/browsers.json` and the `browserVersion` in test caps.
- On Apple Silicon, Docker may need additional resources (Settings → Resources).
