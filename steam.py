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


def test(driver):
    WebDriverWait(driver, TIMEOUT).until(
        ec.element_to_be_clickable(INSTALL))

    login_link = WebDriverWait(driver, TIMEOUT).until(
        ec.element_to_be_clickable(LOG_IN)
    )

    login_link.click()

    username_elem = WebDriverWait(driver, TIMEOUT).until(
        ec.element_to_be_clickable(USERNAME)
    )
    assert username_elem.is_displayed(), 'Login page was not opened'

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

    loading_elem = WebDriverWait(driver, TIMEOUT).until(
        ec.presence_of_element_located(LOADING)

    )
    assert loading_elem.is_displayed(), "Элемент загрузки не отображается"

    WebDriverWait(driver, TIMEOUT).until(
        ec.invisibility_of_element_located(LOADING)

    )

    error_message = WebDriverWait(driver, TIMEOUT).until(
        ec.presence_of_element_located(ERROR)
    )
    assert error_message.is_displayed(), "Сообщение об ошибке не отображается"
