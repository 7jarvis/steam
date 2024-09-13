import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from faker import Faker

STEAM_LINK = 'https://store.steampowered.com/'
LOG_IN = (By.XPATH, "//a[contains(@href, 'login') and contains(text(), 'войти')]")
USERNAME = (By.XPATH, "//form//div[contains(@class, '_3BkiHun-mminuTO-Y-zXke')]//input[@type='text']")
PASSWORD = (By.XPATH, "//input[@type='password']")
SUBMIT = (By.XPATH, "//button[@type='submit' and contains(text(), 'Войти')]")
LOADING = (By.XPATH , "//button[@type='submit']//div//div")
ERROR = (By.CLASS_NAME, "_1W_6HXiG4JJ0By1qN_0fGZ")


@pytest.fixture
def driver():
    driver = webdriver.Chrome()
    driver.get(STEAM_LINK)
    yield driver
    driver.quit()


def login_page(driver):
    login_link = WebDriverWait(driver, 10).until(
        ec.element_to_be_clickable(LOG_IN)
    )

    login_link.click()


def input_creds(driver):
    faker = Faker()
    login_input = WebDriverWait(driver, 10).until(
        ec.element_to_be_clickable(USERNAME))

    login_input.send_keys(faker.user_name())

    pass_input = WebDriverWait(driver, 10).until(
        ec.element_to_be_clickable(PASSWORD))
    pass_input.send_keys(faker.password())

    press_button =WebDriverWait(driver, 10).until(
        ec.element_to_be_clickable(SUBMIT))
    press_button.click()


def check_loading_element(driver):
    WebDriverWait(driver, 10).until(
        ec.presence_of_element_located(LOADING)
        # locator loading

    )


def check_error_message(driver):
    WebDriverWait(driver, 10).until(
        ec.invisibility_of_element_located(LOADING)
        # locator loading
    )

    error_message = WebDriverWait(driver, 10).until(
        ec.presence_of_element_located(ERROR)
    )
    assert error_message.is_displayed(), "Сообщение об ошибке не отображается"


def test_login(driver):
    login_page(driver)
    input_creds(driver)
    check_loading_element(driver)
    check_error_message(driver)
