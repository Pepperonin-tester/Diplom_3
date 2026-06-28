import allure
from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class MainPage(BasePage):
    CONSTRUCTOR_LINK = (By.LINK_TEXT, "Конструктор")
    ORDERS_LINK = (By.LINK_TEXT, "Лента Заказов")
    ORDER_BUTTON = (By.XPATH, "//button[contains(., 'Оформить заказ')]")
    ORDER_NUMBER = (By.CSS_SELECTOR, '[class*="opened"] h2[class*="text_type_digits-large"]')
    FIRST_INGREDIENT = (By.CSS_SELECTOR, '[class*="BurgerIngredient_ingredient_"][href]')
    CONSTRUCTOR_BASKET = (By.CSS_SELECTOR, '[class*="BurgerConstructor_basket"]')
    INGREDIENT_COUNTER = (By.CSS_SELECTOR, '[class*="counter_counter_"]')

    @allure.step("Кликнуть по ссылке 'Конструктор' в шапке")
    def click_constructor(self):
        self.click(self.CONSTRUCTOR_LINK)

    @allure.step("Кликнуть по ссылке 'Лента заказов' в шапке")
    def click_orders_feed(self):
        self.click(self.ORDERS_LINK)

    @allure.step("Кликнуть на первый ингредиент")
    def click_first_ingredient(self):
        self.click(self.FIRST_INGREDIENT)

    @allure.step("Перетащить ингредиент в конструктор")
    def drag_ingredient_to_constructor(self):
        source = self.find(self.FIRST_INGREDIENT)
        target = self.find(self.CONSTRUCTOR_BASKET)

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
        self.execute_script(js_script, source, target)

    @allure.step("Получить значение счётчика первого ингредиента")
    def get_first_ingredient_counter(self):
        source = self.find(self.FIRST_INGREDIENT)
        counter = source.find_element(*self.INGREDIENT_COUNTER)
        return counter.text

    @allure.step("Нажать кнопку 'Оформить заказ'")
    def click_order_button(self):
        self.click(self.ORDER_BUTTON)

    @allure.step("Дождаться и получить номер оформленного заказа")
    def get_order_number(self, timeout=15):
        self.wait_until(
            lambda d: d.find_element(*self.ORDER_NUMBER).text.strip() not in ("", "9999"),
            timeout=timeout
        )
        return self.find(self.ORDER_NUMBER).text


class IngredientPopup(BasePage):
    POPUP_TITLE = (By.CSS_SELECTOR, '[class*="Modal_modal_opened"] h2')
    CLOSE_BUTTON = (By.CSS_SELECTOR, '[class*="opened"] [class*="Modal_modal__close"]')

    @allure.step("Проверить, открыт ли попап с деталями ингредиента")
    def popup_is_open(self, timeout=10):
        return self.is_visible(self.POPUP_TITLE, timeout)

    @allure.step("Закрыть попап по крестику")
    def popup_close(self):
        self.click(self.CLOSE_BUTTON)
        self.wait_invisible(self.POPUP_TITLE, timeout=5)
        