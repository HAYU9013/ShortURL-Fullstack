from selenium.webdriver.common.by import By
import random, string,time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
def test_login_with_wrong_password(driver):
    try:
        ## 進入註冊
        a_element = driver.find_element(By.LINK_TEXT, "註冊")
        a_element.click()

        input_username_element = driver.find_element(By.ID, "username")
        input_password_element = driver.find_element(By.ID, "password")
        input_confirmPw_element = driver.find_element(By.ID, "confirmPassword")
        button_elemnt = driver.find_element(By.TAG_NAME, "button")

        random_id = random.randint(1, 1000000)
        input_username_element.send_keys(f"Tester{random_id}")
        input_password_element.send_keys("abc123456")
        input_confirmPw_element.send_keys("abc123456")

        button_elemnt.click()

        time.sleep(2)

        wait = WebDriverWait(driver, timeout=2)
        alert = wait.until(lambda d : d.switch_to.alert)
        alert.accept()
        ## 進入登入
        a_element = driver.find_element(By.LINK_TEXT, "登入")
        a_element.click()

        input_username_element = driver.find_element(By.XPATH, '/html/body/div[1]/div/div/form/div[1]/input')
        input_password_element = driver.find_element(By.XPATH, '/html/body/div[1]/div/div/form/div[2]/input')
        input_username_element.send_keys(f"Tester{random_id}")
        input_password_element.send_keys("wrongpassword")

        button_element = driver.find_element(By.TAG_NAME, "button")
        button_element.click()
        error_message_element = driver.find_element(By.XPATH, "//div[contains(text(), '登入時發生錯誤')]")
        error_message = error_message_element.text
        assert error_message == "登入時發生錯誤"
        return True
    
    except AssertionError:
        return False
    
def test_login_with_wrong_username(driver):
    try:
        #todo
        return True
    except AssertionError:
        return False
def test_login_with_empty_username(driver):
    try:
        #todo
        return True
    except AssertionError:
        return False
def test_login_with_empty_password(driver):
    try:
        #todo
        return True
    except AssertionError:
        return False
