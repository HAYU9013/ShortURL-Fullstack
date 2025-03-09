from selenium.webdriver.common.by import By

def test_login_exists(driver):
    try:
        a_element = driver.find_element(By.LINK_TEXT, "登入")
        assert a_element.text == "登入"
        a_element.click()

        h2_element = driver.find_element(By.TAG_NAME, "h2")
        assert h2_element.text == "登入"
        return True
    
    except AssertionError:
        return False

def test_login_success(driver):
    try:
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
        return True
    
    except AssertionError:
        return False