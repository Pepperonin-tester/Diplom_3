import pytest
from selenium import webdriver


@pytest.fixture(params=["chrome", "firefox"])
def driver(request):
    if request.param == "chrome":
        drv = webdriver.Chrome()
    else:
        drv = webdriver.Firefox()
    yield drv
    drv.quit()
    