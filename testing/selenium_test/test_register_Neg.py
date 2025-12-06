from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import random
import time


def test_register_fail_with_empty_box(driver):
    try:
        usernames = ["","satori","satori"]
        passwords = ["kawa11","","kawa11"]
        confirm_passwords = ["kawa11","kawa11",""]
        ## 進入註冊

        for i in range(0,3):
            a_element = driver.find_element(By.LINK_TEXT, "Home")
            a_element.click()
            a_element = driver.find_element(By.LINK_TEXT, "Register")
            a_element.click()
            input_username_element = driver.find_element(By.ID, "username")
            input_password_element = driver.find_element(By.ID, "password")
            input_confirmPw_element = driver.find_element(By.ID, "confirmPassword")
            button_elemnt = driver.find_element(By.TAG_NAME, "button")
            error_elements = [input_username_element,input_password_element,input_confirmPw_element]
            input_username_element.clear()
            input_password_element.clear()
            input_confirmPw_element.clear()
            input_username_element.send_keys(usernames[i])
            input_password_element.send_keys(passwords[i])
            input_confirmPw_element.send_keys(confirm_passwords[i])
            button_elemnt.click()
            time.sleep(0.5)
            error_message = error_elements[i].get_attribute("validationMessage")
            assert error_message == "Please fill out this field."
        return True
    except AssertionError:
        return False
def test_register_fail_with_nonsame_password(driver):
    try:
        a_element = driver.find_element(By.LINK_TEXT, "Register")
        a_element.click()
        random_id = random.randint(1, 1000000)
        username = f"satori{random_id}"
        password = "kawa11"
        confirm_password = "satori_kawa11"
        input_username_element = driver.find_element(By.ID, "username")
        input_password_element = driver.find_element(By.ID, "password")
        input_confirmPw_element = driver.find_element(By.ID, "confirmPassword")
        button_elemnt = driver.find_element(By.TAG_NAME, "button")
        input_username_element.clear()
        input_password_element.clear()
        input_confirmPw_element.clear()
        input_username_element.send_keys(username)
        input_password_element.send_keys(password)
        input_confirmPw_element.send_keys(confirm_password)
        button_elemnt.click()
        time.sleep(0.5)
        error_message_element = driver.find_element(By.XPATH, "//div[contains(text(), 'Passwords do not match')]")
        error_message = error_message_element.text
        assert error_message == "Passwords do not match"
        return True
    except AssertionError:
        return False
    
def test_register_fail_with_nonaccept_password(driver):
    try:
        username = "satori"
        passwords = ["kawaii","123456","12ab","______","kawa11"]
        ## 進入註冊

        for password in passwords:
            a_element = driver.find_element(By.LINK_TEXT, "Home")
            a_element.click()
            a_element = driver.find_element(By.LINK_TEXT, "Register")
            a_element.click()
            input_username_element = driver.find_element(By.ID, "username")
            input_password_element = driver.find_element(By.ID, "password")
            input_confirmPw_element = driver.find_element(By.ID, "confirmPassword")
            button_elemnt = driver.find_element(By.TAG_NAME, "button")
            error_elements = [input_username_element,input_password_element,input_confirmPw_element]
            input_username_element.clear()
            input_password_element.clear()
            input_confirmPw_element.clear()
            input_username_element.send_keys(username)
            input_password_element.send_keys(password)
            input_confirmPw_element.send_keys(password)
            button_elemnt.click()
            time.sleep(0.5)
            error_message_element = driver.find_element(By.XPATH, "//div[contains(text(), 'Password must be > 6 chars and include letters and numbers')]")
            error_message = error_message_element.text
            assert error_message == "Password must be > 6 chars and include letters and numbers"
        return True
    except AssertionError:
        return False