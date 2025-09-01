import os
import time

import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys


@pytest.fixture
def driver():
    # Настраиваем Chrome и капабилити для удалённого запуска в Selenoid
    options = Options()
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.set_capability("browserName", "chrome")
    options.set_capability("browserVersion", "121.0")
    options.set_capability(
        "selenoid:options",
        {
            # Включаем VNC и запись видео на стороне Selenoid
            "enableVNC": True,
            "enableVideo": True,
            # Имя сессии в UI и логах
            "name": os.getenv("TEST_NAME", "test_google"),
            # Детеминированное имя видеофайла
            "labels": {"videoName": os.getenv("TEST_NAME", "test_google") + ".mp4"},
        },
    )

    driver = webdriver.Remote(
        # URL хаба Selenoid (из переменной окружения или значение по умолчанию)
        command_executor=os.getenv("SELENOID_URL", "http://localhost:4444/wd/hub"),
        options=options,
    )

    yield driver
    # Дадим Selenoid время завершить запись видео
    time.sleep(1)
    driver.quit()


def test_google_search(driver):
    # /ncr — чтобы избежать редиректов на региональные домены Google
    driver.get("https://www.google.com/ncr")
    # Закрываем окно согласия, если появится (ID может отличаться по региону)
    try:
        WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.ID, "L2AGLb"))
        ).click()
    except Exception:
        pass

    # Ждём, пока поле поиска станет кликабельным
    box = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.NAME, "q"))
    )
    box.clear()
    box.send_keys("Selenoid")
    box.send_keys(Keys.ENTER)
    # Ждём, пока заголовок страницы будет содержать запрос
    WebDriverWait(driver, 10).until(EC.title_contains("Selenoid"))
    assert "Selenoid" in driver.title


