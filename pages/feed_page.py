from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class FeedPage:
    TOTAL_ORDERS = (By.XPATH, "//p[text()='Выполнено за все время:']/following-sibling::p")
    TODAY_ORDERS = (By.XPATH, "//p[text()='Выполнено за сегодня:']/following-sibling::p")
    IN_PROGRESS_LIST = (By.CSS_SELECTOR, '[class*="OrderFeed_orderStatusBox"] ul')

    def __init__(self, driver):
        self.driver = driver

    def get_total_orders(self):
        element = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(self.TOTAL_ORDERS))
        return int(element.text)

    def get_today_orders(self):
        element = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(self.TODAY_ORDERS))
        return int(element.text)

    def get_in_progress_numbers(self):
        lists = WebDriverWait(self.driver, 10).until(
            lambda d: d.find_elements(*self.IN_PROGRESS_LIST) if len(d.find_elements(*self.IN_PROGRESS_LIST)) >= 2 else False
        )
        items = lists[1].find_elements(By.TAG_NAME, "li")
        return [item.text for item in items]
    def wait_for_order_number(self, order_number, timeout=15):
        def check(d):
            lists = d.find_elements(*self.IN_PROGRESS_LIST)
            if len(lists) < 2:
                return False
            items = [li.text.lstrip('0') for li in lists[1].find_elements(By.TAG_NAME, "li")]
            return order_number in items
        WebDriverWait(self.driver, timeout).until(check)
        