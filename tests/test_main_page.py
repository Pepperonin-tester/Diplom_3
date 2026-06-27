import allure
from pages.main_page import MainPage, IngredientPopup

BASE_URL = "https://stellarburgers.education-services.ru"


class TestMainPage:
    @allure.title("Переход в конструктор по клику на 'Конструктор'")
    def test_click_constructor(self, driver):
        with allure.step("Открыть страницу ленты заказов"):
            driver.get(BASE_URL + "/feed")
        with allure.step("Кликнуть по ссылке 'Конструктор' в шапке"):
            main = MainPage(driver)
            main.click_constructor()
        with allure.step("Проверить, что URL изменился на главную страницу"):
            assert driver.current_url == BASE_URL + "/"

    @allure.title("Переход в ленту заказов по клику на 'Лента заказов'")
    def test_click_orders_feed(self, driver):
        with allure.step("Открыть главную страницу"):
            driver.get(BASE_URL + "/")
        with allure.step("Кликнуть по ссылке 'Лента заказов' в шапке"):
            main = MainPage(driver)
            main.click_orders_feed()
        with allure.step("Проверить, что URL изменился на ленту заказов"):
            assert driver.current_url == BASE_URL + "/feed"

    @allure.title("Открытие попапа с деталями ингредиента по клику")
    def test_open_ingredient_popup(self, driver):
        with allure.step("Открыть главную страницу"):
            driver.get(BASE_URL + "/")
        with allure.step("Кликнуть на первый ингредиент"):
            main = MainPage(driver)
            main.click_first_ingredient()
        with allure.step("Проверить, что попап открылся"):
            popup = IngredientPopup(driver)
            assert popup.popup_is_open() is True

    @allure.title("Закрытие попапа ингредиента по клику на крестик")
    def test_close_ingredient_popup(self, driver):
        with allure.step("Открыть главную страницу"):
            driver.get(BASE_URL + "/")
        with allure.step("Кликнуть на первый ингредиент"):
            main = MainPage(driver)
            main.click_first_ingredient()
        with allure.step("Проверить, что попап открылся"):
            popup = IngredientPopup(driver)
            assert popup.popup_is_open() is True
        with allure.step("Закрыть попап по крестику"):
            popup.popup_close()

    @allure.title("Увеличение счётчика ингредиента при добавлении в заказ")
    def test_ingredient_counter_increases(self, driver):
        with allure.step("Открыть главную страницу"):
            driver.get(BASE_URL + "/")
        with allure.step("Запомнить начальное значение счётчика"):
            main = MainPage(driver)
            initial_counter = main.get_first_ingredient_counter()
        with allure.step("Перетащить ингредиент в конструктор"):
            main.drag_ingredient_to_constructor()
        with allure.step("Проверить, что счётчик увеличился"):
            updated_counter = main.get_first_ingredient_counter()
            assert int(updated_counter) > int(initial_counter)
            