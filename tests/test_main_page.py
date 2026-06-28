import allure
from pages.main_page import MainPage, IngredientPopup
from urls import BASE_URL


class TestMainPage:
    @allure.title("Переход в конструктор по клику на 'Конструктор'")
    def test_click_constructor(self, driver):
        driver.get(BASE_URL + "/feed")
        main = MainPage(driver)
        main.click_constructor()
        with allure.step("Проверить, что URL изменился на главную страницу"):
            assert main.get_current_url() == BASE_URL + "/"

    @allure.title("Переход в ленту заказов по клику на 'Лента заказов'")
    def test_click_orders_feed(self, driver):
        driver.get(BASE_URL + "/")
        main = MainPage(driver)
        main.click_orders_feed()
        with allure.step("Проверить, что URL изменился на ленту заказов"):
            assert main.get_current_url() == BASE_URL + "/feed"

    @allure.title("Открытие попапа с деталями ингредиента по клику")
    def test_open_ingredient_popup(self, driver):
        driver.get(BASE_URL + "/")
        main = MainPage(driver)
        main.click_first_ingredient()
        popup = IngredientPopup(driver)
        with allure.step("Проверить, что попап открылся"):
            assert popup.popup_is_open() is True

    @allure.title("Закрытие попапа ингредиента по клику на крестик")
    def test_close_ingredient_popup(self, driver):
        driver.get(BASE_URL + "/")
        main = MainPage(driver)
        main.click_first_ingredient()
        popup = IngredientPopup(driver)
        with allure.step("Проверить, что попап открылся"):
            assert popup.popup_is_open() is True
        popup.popup_close()
        with allure.step("Проверить, что попап закрылся"):
            assert popup.popup_is_open(timeout=2) is False

    @allure.title("Увеличение счётчика ингредиента при добавлении в заказ")
    def test_ingredient_counter_increases(self, driver):
        driver.get(BASE_URL + "/")
        main = MainPage(driver)
        initial_counter = main.get_first_ingredient_counter()
        main.drag_ingredient_to_constructor()
        with allure.step("Проверить, что счётчик увеличился"):
            updated_counter = main.get_first_ingredient_counter()
            assert int(updated_counter) > int(initial_counter)
            