"""Pytest fixtures for the test suite.

Provides a `web` fixture that yields a Selenium `WebDriver` instance.

Requirements:
- `pip install selenium`
- A compatible Chrome/Chromium browser installed. Selenium Manager will try to obtain the driver automatically.
"""

import os
import pytest
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By


@pytest.fixture
def web(request):
    """Create and yield a Chrome WebDriver instance named `web`.

    This fixture also logs into the demo site used by the tests and saves
    a screenshot into `Evidences/` if the test failed.
    """
    options = Options()
    headless_env = os.getenv("HEADLESS", "1")
    if headless_env.lower() in ("1", "true", "yes"):
        options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(10)

    # Navigate and login to the test site (same as earlier local fixture)
    driver.get("https://www.saucedemo.com/")
    driver.find_element(By.CSS_SELECTOR, "[data-test=username]").send_keys(
        "standard_user"
    )
    driver.find_element(By.CSS_SELECTOR, "[data-test=password]").send_keys(
        "secret_sauce"
    )
    driver.find_element(By.CSS_SELECTOR, "[data-test=login-button]").click()

    try:
        yield driver
    finally:
        if hasattr(request.node, "rep_call") and request.node.rep_call.failed:
            evid_dir = os.path.join(os.getcwd(), "Evidences")
            if not os.path.exists(evid_dir):
                os.makedirs(evid_dir)
            timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            driver.save_screenshot(os.path.join(evid_dir, f"error_{timestamp}.png"))
        try:
            driver.quit()
        except Exception:
            pass
