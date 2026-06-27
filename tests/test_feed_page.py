from pages.main_page import MainPage
from pages.feed_page import FeedPage

BASE_URL = "https://stellarburgers.education-services.ru"


class TestFeedPage:
    def test_total_orders_increases(self, driver, registered_user):
        driver.get(BASE_URL + "/feed")
        feed = FeedPage(driver)
        before = feed.get_total_orders()

        driver.get(BASE_URL + "/")
        main = MainPage(driver)
        main.drag_ingredient_to_constructor()
        main.click_order_button()
        main.click_order_button()
        main.get_order_number()

        driver.get(BASE_URL + "/feed")
        after = feed.get_total_orders()
        assert after > before

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
        after = feed.get_today_orders()
        assert after > before

    def test_order_number_in_progress(self, driver, registered_user):
        driver.get(BASE_URL + "/")
        main = MainPage(driver)
        main.drag_ingredient_to_constructor()
        main.click_order_button()
        order_number = main.get_order_number()

        driver.get(BASE_URL + "/feed")
        feed = FeedPage(driver)
        feed.wait_for_order_number(order_number)
            