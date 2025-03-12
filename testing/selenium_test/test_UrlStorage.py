from selenium.webdriver.common.by import By
import random, string,time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import test_logout
def test_url_storage(driver, username, password,testWebsite):
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
        
        inputField = wait.until(EC.presence_of_element_located((By.CLASS_NAME,"form-control")))
        button = wait.until(EC.presence_of_element_located((By.CLASS_NAME,"btn-custom")))
        inputField.send_keys(testWebsite)
        
        
        
    
        button.click()
        time.sleep(3)
        link =  wait.until(EC.presence_of_element_located((By.PARTIAL_LINK_TEXT, "http://localhost:8000/api/url/r/")))
        actualShortUrl = link.text
        driver.refresh()
        
        shortUrl = wait.until(EC.presence_of_element_located((By.PARTIAL_LINK_TEXT,"http://localhost:8000/api/url/r/")))
        longUrl = wait.until(EC.presence_of_element_located((By.LINK_TEXT,testWebsite)))
        if shortUrl.text != actualShortUrl and longUrl.text != testWebsite:
            print(shortUrl.text +"  "+longUrl.text)
            return False
        assert test_logout.test_logout_success(driver) is True
        
        return True
    except AssertionError:
        return False

    
    