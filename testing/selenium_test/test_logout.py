from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def test_logout_success(driver):
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

        assert input_username_element.text == ""
        input_username_element.send_keys("Tester")
        assert input_password_element.text == ""
        input_password_element.send_keys("abc123456")
        assert input_confirmPw_element.text == ""
        input_confirmPw_element.send_keys("abc123456")

        button_elemnt.click()
        ## 進入登入
        a_element = driver.find_element(By.LINK_TEXT, "登入")
        assert a_element.text == "登入"
        a_element.click()

        h2_login_element = driver.find_element(By.TAG_NAME, "h2")
        assert h2_login_element.text == "登入"

        input_username_element = driver.find_element(By.XPATH, '/html/body/div[1]/div/div/form/div[1]/input')
        input_password_element = driver.find_element(By.XPATH, '/html/body/div[1]/div/div/form/div[2]/input')

        assert input_username_element.text == ""
        input_username_element.send_keys("Tester")
        assert input_password_element.text == ""
        input_password_element.send_keys("abc123456")

        button_element = driver.find_element(By.TAG_NAME, "button")
        button_element.click()
        

        ## 登出
        a_element = driver.find_element(By.LINK_TEXT, "登出")
        assert a_element.text == "登出"
        a_element.click()

        logout_element = driver.find_element(By.CLASS_NAME, "logout-message")
        assert logout_element.text == "Logging out..."

        return True
    except AssertionError:
        return False
