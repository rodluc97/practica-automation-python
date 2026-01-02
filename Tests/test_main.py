import pytest
import os
from datetime import datetime
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver


# --- CONFIGURACIÓN DE REPORTES (FUERA) ---
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    setattr(item, "rep_" + rep.when, rep)


# --- FIXTURE (FUERA DE LA CLASE) ---
@pytest.fixture
def web(request):
    options = Options()
    driver = Chrome(options=options)
    driver.implicitly_wait(10)

    driver.get("https://www.saucedemo.com/")
    driver.find_element(By.CSS_SELECTOR, "[data-test=username]").send_keys(
        "standard_user"
    )
    driver.find_element(By.CSS_SELECTOR, "[data-test=password]").send_keys(
        "secret_sauce"
    )
    driver.find_element(By.CSS_SELECTOR, "[data-test=login-button]").click()

    yield driver

    if hasattr(request.node, "rep_call") and request.node.rep_call.failed:
        evid_dir = os.path.join(os.getcwd(), "Evidences")
        if not os.path.exists(evid_dir):
            os.makedirs(evid_dir)
        timestamp = datetime.now().strftime("%H-%M-%S")
        driver.save_screenshot(os.path.join(evid_dir, f"error_{timestamp}.png"))

    driver.quit()
