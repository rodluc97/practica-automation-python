import os
from datetime import datetime
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver


class InventoryPage:
    def __init__(self, driver: WebDriver):
        self.driver = driver
        self.add_to_cart_buttons = (By.CSS_SELECTOR, "[data-test^='add-to-cart']")
        self.remove_buttons = (By.CSS_SELECTOR, "[data-test^='remove']")

    def agregar_primer_producto(self):
        productos = self.driver.find_elements(*self.add_to_cart_buttons)
        if len(productos) > 0:
            productos[0].click()

    def el_boton_remove_es_visible(self):
        return self.driver.find_element(*self.remove_buttons).is_displayed()

    def tomar_captura_evidencia(self, nombre_paso):
        """Save a screenshot under `Evidences/<YYYY-MM-DD>/...` with a timestamp."""
        fecha_carpeta = datetime.now().strftime("%Y-%m-%d")
        ruta_carpeta = os.path.join("Evidences", fecha_carpeta)
        os.makedirs(ruta_carpeta, exist_ok=True)

        ts = datetime.now().strftime("%H-%M-%S")
        ruta = os.path.join(ruta_carpeta, f"{nombre_paso}_{ts}.png")
        self.driver.save_screenshot(ruta)
        print(f"Evidencia guardada: {ruta}")

    # English-friendly aliases for older tests or English-named helpers
    def take_screenshot(self, step_name):
        return self.tomar_captura_evidencia(step_name)

    def add_first_product(self):
        return self.agregar_primer_producto()

    def is_remove_button_displayed(self):
        return self.el_boton_remove_es_visible()
