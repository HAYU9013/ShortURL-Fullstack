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
        a_element = driver.find_element(By.LINK_TEXT, "註冊")
        assert a_element.text == "註冊"
        a_element.click()
        h2_element = driver.find_element(By.TAG_NAME, "h2")
        assert h2_element.text == "註冊"
        return True
    except AssertionError:
        return False
    
def test_register_success(driver):
    try:
        # 進入註冊
        a_element = driver.find_element(By.LINK_TEXT, "註冊")
        assert a_element.text == "註冊"
        a_element.click()
        h2_register_element = driver.find_element(By.TAG_NAME, "h2")
        assert h2_register_element.text == "註冊"

        input_username_element = driver.find_element(By.ID, "username")
        input_password_element = driver.find_element(By.ID, "password")
        input_confirmPw_element = driver.find_element(By.ID, "confirmPassword")
        button_element = driver.find_element(By.TAG_NAME, "button")

        # 初次嘗試使用 "Tester"
        input_username_element.clear()
        input_username_element.send_keys("Tester")
        input_password_element.clear()
        input_password_element.send_keys("abc123456")
        input_confirmPw_element.clear()
        input_confirmPw_element.send_keys("abc123456")
        button_element.click()

        time.sleep(2)

        try:
            # 等待註冊錯誤訊息的出現
            register_error = WebDriverWait(driver, timeout=2).until(
                EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div/div/div'))
            )

            # 若有錯誤訊息，隨機產生帳號再嘗試
            if register_error.text == "註冊時發生錯誤":
                random_id = random.randint(1, 1000000)

                input_username_element.clear()
                input_username_element.send_keys(f"Tester{random_id}")
                input_password_element.clear()
                input_password_element.send_keys("abc123456")
                input_confirmPw_element.clear()
                input_confirmPw_element.send_keys("abc123456")
                button_element.click()

        except TimeoutException:
            # 沒有註冊錯誤訊息，代表註冊成功
            pass

        # 驗證註冊成功的警告訊息

        time.sleep(2)
        
        wait = WebDriverWait(driver, timeout=2)
        alert = wait.until(lambda d : d.switch_to.alert)
        text = alert.text
        alert.accept()
        assert text == "註冊成功，請登入"

        return True

    except AssertionError:
        return False