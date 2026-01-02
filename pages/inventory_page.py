import os
import logging
from datetime import datetime
from typing import Tuple
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver


EVIDENCE_ROOT = "Evidences"
DATE_FMT = "%Y-%m-%d"
TIME_FMT = "%H-%M-%S"

logger = logging.getLogger(__name__)
if not logger.handlers:
    # Basic configuration if the project doesn't configure logging
    logging.basicConfig(level=logging.INFO)


class InventoryPage:
    """Page object for the inventory page of the demo app.

    Provides action methods and helpers to collect screenshots (evidence).
    """

    def __init__(self, driver: WebDriver):
        self.driver = driver
        # Locators
        self._add_to_cart: Tuple[str, str] = (
            By.CSS_SELECTOR,
            "[data-test^='add-to-cart']",
        )
        self._remove_button: Tuple[str, str] = (
            By.CSS_SELECTOR,
            "[data-test^='remove']",
        )

    # Actions
    def add_first_product(self) -> None:
        """Click the first available 'add to cart' button, if any."""
        products = self.driver.find_elements(*self._add_to_cart)
        if products:
            products[0].click()

    def is_remove_button_displayed(self) -> bool:
        """Return True if a 'remove' button is visible on the page."""
        return self.driver.find_element(*self._remove_button).is_displayed()

    # Evidence helpers
    def tomar_captura_evidencia(self, nombre_paso: str) -> str:
        """Take a screenshot and return the path to the saved file.

        Screenshots are saved under: EVIDENCE_ROOT/YYYY-MM-DD/<nombre_paso>_HH-MM-SS.png
        """
        date_folder = datetime.now().strftime(DATE_FMT)
        dest_folder = os.path.join(EVIDENCE_ROOT, date_folder)
        os.makedirs(dest_folder, exist_ok=True)

        ts = datetime.now().strftime(TIME_FMT)
        filename = f"{nombre_paso}_{ts}.png"
        path = os.path.join(dest_folder, filename)

        try:
            self.driver.save_screenshot(path)
            logger.info("Saved evidence: %s", path)
        except Exception as exc:
            logger.exception("Failed to save screenshot: %s", exc)

        return path

    # English-friendly aliases
    def take_screenshot(self, step_name: str) -> str:
        return self.tomar_captura_evidencia(step_name)

    def el_boton_remove_es_visible(self) -> bool:
        return self.is_remove_button_displayed()

    def agregar_primer_producto(self) -> None:
        return self.add_first_product()
