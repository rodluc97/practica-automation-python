import pytest
import json
import os
from datetime import datetime
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.remote.webdriver import WebDriver

# Importamos las clases desde la carpeta pages
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage


# --- CONFIGURATION FOR REPORTS ---
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    setattr(item, "rep_" + rep.when, rep)


class TestShoppingCart:

    @pytest.fixture
    def web(self, request):
        # 1. Load data from JSON (fallback to defaults if not present)
        try:
            with open("data.json", "r") as f:
                data = json.load(f)
        except FileNotFoundError:
            data = {
                "url": "https://www.saucedemo.com/",
                "user": "standard_user",
                "pass": "secret_sauce",
            }

        options = Options()
        # options.add_argument("--headless") # Opcional para correr sin interfaz
        driver = Chrome(options=options)
        driver.implicitly_wait(10)

        # 2. Setup: Perform Login
        driver.get(data["url"])
        login_page = LoginPage(driver)
        login_page.login(data["user"], data["pass"])  # Cambiado a 'login' en inglés

        yield driver

        # 3. Teardown: Automated evidence and cleanup
        # Verificamos si el test falló
        if hasattr(request.node, "rep_call") and request.node.rep_call.failed:
            # Crear ruta: Evidences/DD-MM-YYYY/Errors
            today = datetime.now().strftime("%d-%m-%Y")
            error_path = os.path.join("Evidences", today, "Errors")

            if not os.path.exists(error_path):
                os.makedirs(error_path)

            # Nombre del archivo con hora y nombre del test
            timestamp = datetime.now().strftime("%H-%M-%S")
            test_name = request.node.name
            screenshot_name = f"FAIL_{test_name}_{timestamp}.png"

            driver.save_screenshot(os.path.join(error_path, screenshot_name))
            print(f"\n[Error Evidence] Captured: {screenshot_name}")

        driver.quit()

    # --- TEST CASE ---
    def test_1_should_add_item_to_cart(self, web: WebDriver):
        # Initialize Inventory Page
        inventory = InventoryPage(web)

        # Evidence: Initial state (Success folder)
        inventory.take_screenshot("1_initial_state")

        # Action: Add product
        inventory.add_first_product()

        # Evidence: Product added (Success folder)
        inventory.take_screenshot("2_product_added")

        # Assertion
        assert inventory.is_remove_button_displayed()
