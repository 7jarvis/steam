import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from faker import Faker

TIMEOUT = 10
STEAM_LINK = 'https://store.steampowered.com/'
INSTALL = (By.XPATH, "//a//div[contains(text(), 'Установить')]")
LOG_IN = (By.XPATH, "//a[contains(@href, 'login') and contains(text(), 'войти')]")
USERNAME = (By.XPATH, "//form//div//input[@type='text'][1]")
PASSWORD = (By.XPATH, "//input[@type='password']")
SUBMIT = (By.XPATH, "//button[@type='submit' and contains(text(), 'Войти')]")
LOADING = (By.XPATH, "//button[@type='submit']//div//div")
ERROR = (By.XPATH, "//div[contains(text(), 'Пожалуйста, проверьте')]")


@pytest.fixture
def driver():
    driver = webdriver.Chrome()
    driver.get(STEAM_LINK)
    yield driver
    driver.quit()


def main_page(driver):
    login_link = WebDriverWait(driver, TIMEOUT).until(
        ec.element_to_be_clickable(INSTALL)
    )


def login_page(driver):
    login_link = WebDriverWait(driver, TIMEOUT).until(
        ec.element_to_be_clickable(LOG_IN)
    )

    login_link.click()

    WebDriverWait(driver, TIMEOUT).until(
        ec.url_contains("login")
    )


def input_creds(driver):
    faker = Faker()
    login_input = WebDriverWait(driver, TIMEOUT).until(
        ec.element_to_be_clickable(USERNAME))

    login_input.send_keys(faker.user_name())

    pass_input = WebDriverWait(driver, TIMEOUT).until(
        ec.element_to_be_clickable(PASSWORD))
    pass_input.send_keys(faker.password())

    press_button = WebDriverWait(driver, TIMEOUT).until(
        ec.element_to_be_clickable(SUBMIT))
    press_button.click()


def loading_element(driver):
    loading_elem = WebDriverWait(driver, TIMEOUT).until(
        ec.presence_of_element_located(LOADING)

    )
    assert loading_elem.is_displayed(), "Элемент загрузки не отображается"


def check_error_message(driver):
    WebDriverWait(driver, TIMEOUT).until(
        ec.invisibility_of_element_located(LOADING)

    )

    error_message = WebDriverWait(driver, 10).until(
        ec.presence_of_element_located(ERROR)
    )
    assert error_message.is_displayed(), "Сообщение об ошибке не отображается"


def test_login(driver):
    main_page(driver)
    login_page(driver)
    input_creds(driver)
    loading_element(driver)
    check_error_message(driver)
