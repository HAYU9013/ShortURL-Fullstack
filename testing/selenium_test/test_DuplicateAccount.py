from selenium.webdriver.common.by import By
import random, string,time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

accountList = ()

def RegisterAccount(driver,usernameText, passwordText):
    try:
        username = driver.find_element(By.ID,"username")
        password = driver.find_element(By.ID,"password")
        confirmPassword = driver.find_element(By.ID,"confirmPassword")
        assert username.text == ""
        assert password.text == ""
        assert confirmPassword.text == ""
        username.send_keys(usernameText)
        password.send_keys(passwordText)
        confirmPassword.send_keys(passwordText)
        return True
    except AssertionError:
        return False

def test_register_Duplicate(driver):
    global accountList
    try:
        ## 進入註冊
        username = '1'.join(random.choice(string.ascii_letters + string.digits) for _ in range(10))
        password = '2'.join(random.choice(string.ascii_letters + string.digits) for _ in range(10))
        
        accountList = (username,password)
        for i in range(0,2):
            a_element = driver.find_element(By.LINK_TEXT, "註冊")
            
            assert a_element.text == "註冊"
            a_element.click()
            
            R_result = RegisterAccount(driver, username, password)
            assert R_result == True

            a_element = driver.find_element(By.TAG_NAME, "button")
            a_element.click()
            
            if i == 0:
                WebDriverWait(driver, 10).until(EC.alert_is_present())
                alert = driver.switch_to.alert
                assert alert.text =='註冊成功，請登入'
                alert.accept()
                time.sleep(2)
            

        danger = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "alert-danger")))
        

        assert danger.text == "註冊時發生錯誤"   
        return True

    except AssertionError:
        return False