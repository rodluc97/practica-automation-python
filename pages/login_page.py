from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver


class LoginPage:
    def __init__(self, driver: WebDriver):
        self.driver = driver
        self.username_field = (By.CSS_SELECTOR, "[data-test=username]")
        self.password_field = (By.CSS_SELECTOR, "[data-test=password]")
        self.login_button = (By.CSS_SELECTOR, "[data-test=login-button]")

    def ingresar_credenciales(self, usuario, contrasena):
        self.driver.find_element(*self.username_field).send_keys(usuario)
        self.driver.find_element(*self.password_field).send_keys(contrasena)
        self.driver.find_element(*self.login_button).click()

    # Backwards/English-compatible alias
    def login(self, usuario, contrasena):
        return self.ingresar_credenciales(usuario, contrasena)
