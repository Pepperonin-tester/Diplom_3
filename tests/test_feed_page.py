import allure
from pages.main_page import MainPage
from pages.feed_page import FeedPage
from urls import BASE_URL


class TestFeedPage:
    @allure.title("Увеличение счётчика 'Выполнено за всё время' при создании заказа")
    def test_total_orders_increases(self, driver, registered_user):
        driver.get(BASE_URL + "/feed")
        feed = FeedPage(driver)
        before = feed.get_total_orders()

        driver.get(BASE_URL + "/")
        main = MainPage(driver)
        main.drag_ingredient_to_constructor()
        main.click_order_button()
        main.get_order_number()

        driver.get(BASE_URL + "/feed")
        with allure.step("Проверить, что счётчик 'за всё время' увеличился"):
            after = feed.get_total_orders()
            assert after > before

    @allure.title("Увеличение счётчика 'Выполнено за сегодня' при создании заказа")
    def test_today_orders_increases(self, driver, registered_user):
        driver.get(BASE_URL + "/feed")
        feed = FeedPage(driver)
        before = feed.get_today_orders()

        driver.get(BASE_URL + "/")
        main = MainPage(driver)
        main.drag_ingredient_to_constructor()
        main.click_order_button()
        main.get_order_number()

        driver.get(BASE_URL + "/feed")
        with allure.step("Проверить, что счётчик 'за сегодня' увеличился"):
            after = feed.get_today_orders()
            assert after > before

    @allure.title("Номер заказа появляется в разделе 'В работе'")
    def test_order_number_in_progress(self, driver, registered_user):
        driver.get(BASE_URL + "/")
        main = MainPage(driver)
        main.drag_ingredient_to_constructor()
        main.click_order_button()
        order_number = main.get_order_number()

        driver.get(BASE_URL + "/feed")
        feed = FeedPage(driver)
        feed.wait_for_order_number(order_number)
        