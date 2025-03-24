from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import random

def test_password_valid1(driver):
    try:
        ## 進入註冊
        a_element = driver.find_element(By.LINK_TEXT, "註冊")
        assert a_element.text == "註冊"
        a_element.click()
        h2_register_element = driver.find_element(By.TAG_NAME, "h2")
        assert h2_register_element.text == "註冊"

        input_username_element = driver.find_element(By.ID, "username")
        input_password_element = driver.find_element(By.ID, "password")
        input_confirmPw_element = driver.find_element(By.ID, "confirmPassword")
        button_elemnt = driver.find_element(By.TAG_NAME, "button")

        random_id = random.randint(1, 1000000)
        user_name = f"Tester{random_id}"
        assert input_username_element.text == ""
        input_username_element.send_keys(user_name)
        assert input_password_element.text == ""
        input_password_element.send_keys("aaa123")
        assert input_confirmPw_element.text == ""
        input_confirmPw_element.send_keys("aaa123")

        button_elemnt.click()

        time.sleep(2)

        result = '密碼必須超過6個字符，且包含字母和數字' in driver.page_source
        a_element = driver.find_element(By.LINK_TEXT,"首頁")
        a_element.click()
        return result
    
    except AssertionError:
        return False