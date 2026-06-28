import allure
from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class LoginPage(BasePage):
    EMAIL_INPUT = (By.CSS_SELECTOR, 'input[type="text"]')
    PASSWORD_INPUT = (By.CSS_SELECTOR, 'input[type="password"]')
    LOGIN_BUTTON = (By.XPATH, "//button[contains(., 'Войти')]")

    @allure.step("Авторизоваться через форму логина")
    def login(self, email, password):
        self.find(self.EMAIL_INPUT).send_keys(email)
        self.find(self.PASSWORD_INPUT).send_keys(password)
        self.click(self.LOGIN_BUTTON)
        self.wait_until(lambda d: "/login" not in d.current_url)

    @allure.step("Получить accessToken из localStorage")
    def get_access_token(self):
        return self.execute_script("return window.localStorage.getItem('accessToken');")
    