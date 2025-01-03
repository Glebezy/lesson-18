import pytest
from selene import browser
from selenium import webdriver


@pytest.fixture(scope='session', autouse=True)
def browser_settings():
    driver_options = webdriver.ChromeOptions()
    driver_options.page_load_strategy = 'eager'
    browser.driver.delete_all_cookies()
    browser.config.driver_options = driver_options
    browser.config.window_width = 1920
    browser.config.window_height = 1080
    browser.config.base_url = 'https://demowebshop.tricentis.com/'

    yield

    browser.quit()
