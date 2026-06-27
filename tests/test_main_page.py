from pages.main_page import MainPage, IngredientPopup

BASE_URL = "https://stellarburgers.education-services.ru"


class TestMainPage:
    def test_click_constructor(self, driver):
        driver.get(BASE_URL + "/feed")
        page = MainPage(driver)
        page.click_constructor()
        assert driver.current_url == BASE_URL + "/"

    def test_click_orders_feed(self, driver):
        driver.get(BASE_URL + "/")
        page = MainPage(driver)
        page.click_orders_feed()
        assert driver.current_url == BASE_URL + "/feed"

    def test_open_ingredient_popup(self, driver):
        driver.get(BASE_URL + "/")
        page = MainPage(driver)
        page.click_first_ingredient()
        popup = IngredientPopup(driver)
        assert popup.popup_is_open() is True

    def test_close_ingredient_popup(self, driver):
        driver.get(BASE_URL + "/")
        page = MainPage(driver)
        page.click_first_ingredient()
        popup = IngredientPopup(driver)
        assert popup.popup_is_open() is True
        popup.popup_close()

    def test_ingredient_counter_increases(self, driver):
        driver.get(BASE_URL + "/")
        page = MainPage(driver)
        initial_counter = page.get_first_ingredient_counter()
        page.drag_ingredient_to_constructor()
        updated_counter = page.get_first_ingredient_counter()
        assert int(updated_counter) > int(initial_counter)
