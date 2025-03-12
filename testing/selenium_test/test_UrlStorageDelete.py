from selenium.webdriver.common.by import By
import random, string,time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoAlertPresentException
def test_url_storage_delete(driver, username, password):
    try:
        
        wait = WebDriverWait(driver, 10)
        a_element = driver.find_element(By.LINK_TEXT, "登入")
        assert a_element.text == "登入"
        a_element.click()
        
        password_input = driver.find_element(By.XPATH, "//input[@type='password']")
        username_input = driver.find_element(By.XPATH, "//input[@type='text']")
        a_element = driver.find_element(By.XPATH, "//button[@type= 'submit']")
        assert a_element.text == "登入"
        username_input.send_keys(username)
        password_input.send_keys(password)
        a_element.click()
        time.sleep(2)
        tag = wait.until(EC.presence_of_element_located((By.TAG_NAME,"h2")))
        
        assert tag.text == f"歡迎回來, {username}!"

        button = wait.until(EC.presence_of_element_located((By.CLASS_NAME,"btn-danger")))
        button.click()
        time.sleep(2)
        try:
            alert = wait.until(EC.alert_is_present())
            assert alert.text == "確定刪除此短網址？"
            alert.accept()
        except NoAlertPresentException:
            print("alert1")
            return False 
        try:
            alert = wait.until(EC.alert_is_present())
            assert alert.text == "刪除成功", "alert2"
            alert.accept()
        except NoAlertPresentException:
            print("alert2")
            return False
        return True
    except AssertionError:
        return False