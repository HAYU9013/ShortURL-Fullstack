from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import random
import time

def test_register_exists(driver):
    try:
        a_element = driver.find_element(By.LINK_TEXT, "Register")
        assert a_element.text == "Register"
        a_element.click()
        h2_element = driver.find_element(By.TAG_NAME, "h2")
        assert h2_element.text == "Sign Up"
        return True
    except AssertionError:
        return False

def test_register_success(driver):
    try:
        ## Enter Register
        a_element = driver.find_element(By.LINK_TEXT, "Register")
        assert a_element.text == "Register"
        a_element.click()
        h2_register_element = driver.find_element(By.TAG_NAME, "h2")
        assert h2_register_element.text == "Sign Up"

        input_username_element = driver.find_element(By.ID, "username")
        input_password_element = driver.find_element(By.ID, "password")
        input_confirmPw_element = driver.find_element(By.ID, "confirmPassword")
        button_elemnt = driver.find_element(By.TAG_NAME, "button")

        random_id = random.randint(1, 1000000)
        assert input_username_element.text == ""
        input_username_element.send_keys(f"Tester{random_id}")
        assert input_password_element.text == ""
        input_password_element.send_keys("abc123456")
        assert input_confirmPw_element.text == ""
        input_confirmPw_element.send_keys("abc123456")

        button_elemnt.click()

        time.sleep(2)

        wait = WebDriverWait(driver, timeout=2)
        alert = wait.until(lambda d : d.switch_to.alert)
        text = alert.text
        alert.accept()
        assert text == "Sign up successful, please sign in"

        return True
    
    except AssertionError:
        return False