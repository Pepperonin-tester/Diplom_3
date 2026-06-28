import pytest
import requests
import uuid
from selenium import webdriver
from pages.login_page import LoginPage
from urls import BASE_URL, API_URL


@pytest.fixture
def registered_user(driver):
    email = f"test_{uuid.uuid4().hex[:8]}@yandex.ru"
    password = "Test12345"
    name = "TestUser"

    requests.post(f"{API_URL}/auth/register", json={
        "email": email, "password": password, "name": name
    })

    driver.get(BASE_URL + "/login")
    login_page = LoginPage(driver)
    login_page.login(email, password)

    yield

    token = login_page.get_access_token()
    requests.delete(f"{API_URL}/auth/user", headers={"Authorization": token})


@pytest.fixture(params=["chrome", "firefox"])
def driver(request):
    if request.param == "chrome":
        drv = webdriver.Chrome()
    else:
        drv = webdriver.Firefox()
    yield drv
    drv.quit()
    