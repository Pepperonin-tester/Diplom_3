from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


class MainPage:
    CONSTRUCTOR_LINK = (By.LINK_TEXT, "Конструктор")
    ORDERS_LINK = (By.LINK_TEXT, "Лента Заказов")
    ORDER_BUTTON = (By.XPATH, "//button[contains(., 'Оформить заказ')]")
    ORDER_NUMBER = (By.CSS_SELECTOR, '[class*="opened"] h2[class*="text_type_digits-large"]')

    def __init__(self, driver):
        self.driver = driver

    def click_order_button(self):
        button = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(self.ORDER_BUTTON))
        self.driver.execute_script("arguments[0].click();", button)

    def click_constructor(self):
        el = self.driver.find_element(*self.CONSTRUCTOR_LINK)
        self.driver.execute_script("arguments[0].click();", el)

    def click_orders_feed(self):
        el = self.driver.find_element(*self.ORDERS_LINK)
        self.driver.execute_script("arguments[0].click();", el)

    def click_first_ingredient(self):
        el = self.driver.find_element(By.CSS_SELECTOR, '[class*="BurgerIngredient_ingredient_"][href]')
        self.driver.execute_script("arguments[0].click();", el)

    def drag_ingredient_to_constructor(self):
        source = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '[class*="BurgerIngredient_ingredient_"][href]'))
        )
        target = self.driver.find_element(By.CSS_SELECTOR, '[class*="BurgerConstructor_basket"]')

        js_script = """
        function simulateDragDrop(sourceNode, destinationNode) {
            function createEvent(type) {
                var event = new CustomEvent(type, {bubbles: true, cancelable: true});
                event.dataTransfer = {
                    data: {},
                    setData: function(t, v) { this.data[t] = v; },
                    getData: function(t) { return this.data[t]; }
                };
                return event;
        }
        var dragStart = createEvent('dragstart');
        sourceNode.dispatchEvent(dragStart);

        var drop = createEvent('drop');
        drop.dataTransfer = dragStart.dataTransfer;
        destinationNode.dispatchEvent(drop);

        var dragEnd = createEvent('dragend');
        dragEnd.dataTransfer = dragStart.dataTransfer;
        sourceNode.dispatchEvent(dragEnd);
    }
    simulateDragDrop(arguments[0], arguments[1]);
    """
        self.driver.execute_script(js_script, source, target)

    def get_first_ingredient_counter(self):
        source = self.driver.find_element(By.CSS_SELECTOR, '[class*="BurgerIngredient_ingredient_"][href]')
        counter = source.find_element(By.CSS_SELECTOR, '[class*="counter_counter_"]')
        return counter.text
    
    def get_order_number(self, timeout=15):
        WebDriverWait(self.driver, timeout).until(
            lambda d: d.find_element(*self.ORDER_NUMBER).text.strip() not in ("", "9999")
        )
        return self.driver.find_element(*self.ORDER_NUMBER).text


class IngredientPopup:
    POPUP_TITLE = (By.CSS_SELECTOR, '[class*="Modal_modal_opened"] h2')
    CLOSE_BUTTON = (By.CSS_SELECTOR, '[class*="opened"] [class*="Modal_modal__close"]')

    def __init__(self, driver):
        self.driver = driver

    def popup_is_open(self, timeout=10):
        try:
            WebDriverWait(self.driver, timeout).until(EC.visibility_of_element_located(self.POPUP_TITLE))
            return True
        except TimeoutException:
            return False

    def popup_close(self):
        self.driver.find_element(*self.CLOSE_BUTTON).click()
        WebDriverWait(self.driver, 5).until(EC.invisibility_of_element_located(self.POPUP_TITLE))
