import pytest
import requests
import uuid
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

BASE_URL = "https://stellarburgers.education-services.ru"
API_URL = BASE_URL + "/api"


@pytest.fixture
def registered_user(driver):
    email = f"test_{uuid.uuid4().hex[:8]}@yandex.ru"
    password = "Test12345"
    name = "TestUser"

    requests.post(f"{API_URL}/auth/register", json={
        "email": email, "password": password, "name": name
    })

    driver.get(BASE_URL + "/login")
    driver.find_element(By.CSS_SELECTOR, 'input[type="text"]').send_keys(email)
    driver.find_element(By.CSS_SELECTOR, 'input[type="password"]').send_keys(password)

    login_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Войти')]"))
    )
    driver.execute_script("arguments[0].click();", login_button)

    WebDriverWait(driver, 10).until(lambda d: "/login" not in d.current_url)

    yield

    token = driver.execute_script("return window.localStorage.getItem('accessToken');")
    requests.delete(f"{API_URL}/auth/user", headers={"Authorization": token})

@pytest.fixture(params=["chrome", "firefox"])
def driver(request):
    if request.param == "chrome":
        drv = webdriver.Chrome()
    else:
        drv = webdriver.Firefox()
    yield drv
    drv.quit()
    