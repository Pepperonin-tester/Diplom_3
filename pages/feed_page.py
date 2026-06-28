import allure
from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class FeedPage(BasePage):
    TOTAL_ORDERS = (By.XPATH, "//p[text()='Выполнено за все время:']/following-sibling::p")
    TODAY_ORDERS = (By.XPATH, "//p[text()='Выполнено за сегодня:']/following-sibling::p")
    IN_PROGRESS_LIST = (By.CSS_SELECTOR, '[class*="OrderFeed_orderStatusBox"] ul')

    @allure.step("Получить значение счётчика 'Выполнено за всё время'")
    def get_total_orders(self):
        element = self.find_visible(self.TOTAL_ORDERS)
        return int(element.text)

    @allure.step("Получить значение счётчика 'Выполнено за сегодня'")
    def get_today_orders(self):
        element = self.find_visible(self.TODAY_ORDERS)
        return int(element.text)

    @allure.step("Получить список номеров заказов в разделе 'В работе'")
    def get_in_progress_numbers(self):
        lists = self.wait_until(
            lambda d: d.find_elements(*self.IN_PROGRESS_LIST) if len(d.find_elements(*self.IN_PROGRESS_LIST)) >= 2 else False
        )
        items = lists[1].find_elements(By.TAG_NAME, "li")
        return [item.text for item in items]

    @allure.step("Дождаться появления номера заказа в разделе 'В работе'")
    def wait_for_order_number(self, order_number, timeout=15):
        def check(d):
            lists = d.find_elements(*self.IN_PROGRESS_LIST)
            if len(lists) < 2:
                return False
            items = [li.text.lstrip('0') for li in lists[1].find_elements(By.TAG_NAME, "li")]
            return order_number in items
        self.wait_until(check, timeout=timeout)
        