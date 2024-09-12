import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec


@pytest.fixture
def driver():
    driver = webdriver.Chrome()
    yield driver


def login_page(driver):
    driver.get("https://store.steampowered.com/")
    WebDriverWait(driver, 10)

    login_link = driver.find_element(By.XPATH, "//a[contains(@href, 'login') and contains(text(), 'войти')]")
    login_link.click()


def input_creds(driver):
    WebDriverWait(driver, 10).until(
        ec.presence_of_element_located(
            (By.XPATH, "//input[@type='text' and contains(@class, '_2GBWeup5cttgbTw8FM3tfx')]"))
    )
    login_input = driver.find_element(By.XPATH, "//input[@type='text' and contains(@class, '_2GBWeup5cttgbTw8FM3tfx')]")
    login_input.send_keys("your_username")

    pass_input = driver.find_element(By.XPATH, "//input[@type='password']")
    pass_input.send_keys("your_username")

    press_button = driver.find_element(By.XPATH, "//button[@type='submit' and contains(text(), 'Войти')]")
    press_button.click()


def check_loading_element(driver):
    WebDriverWait(driver, 10).until(
        ec.presence_of_element_located((By.CSS_SELECTOR, "._1VLukpV8qjL4BULw7Zob_l.WYrJyNEVnjgAnMVZgvPeg"))
        # locator loading

    )


def check_error_message(driver):
    WebDriverWait(driver, 10).until(
        ec.invisibility_of_element_located((By.CSS_SELECTOR, "._1VLukpV8qjL4BULw7Zob_l.WYrJyNEVnjgAnMVZgvPeg"))
        # locator loading
    )

    error_message = WebDriverWait(driver, 10).until(
        ec.presence_of_element_located((By.CLASS_NAME, "_1W_6HXiG4JJ0By1qN_0fGZ"))
    )
    assert error_message.is_displayed()


def test_login(driver):
    login_page(driver)
    input_creds(driver)
    check_loading_element(driver)
    check_error_message(driver)
