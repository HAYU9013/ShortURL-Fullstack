from selenium.webdriver.common.by import By
import random, string,time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import test_logout

def test_storageUrl(driver,username ,password,testWebsite):
    try:
        wait = WebDriverWait(driver,10)
        a_element = driver.find_element(By.LINK_TEXT, "Login")
        assert a_element.text == "Login"
        a_element.click()
        
        password_input = driver.find_element(By.XPATH, "//input[@type='password']")
        username_input = driver.find_element(By.XPATH, "//input[@type='text']")
        a_element = driver.find_element(By.XPATH, "//button[@type= 'submit']")
        assert a_element.text == "Sign In"
        username_input.send_keys(username)
        password_input.send_keys(password)
        a_element.click()
        time.sleep(2)
        tag = wait.until(EC.presence_of_element_located((By.TAG_NAME,"h2")))
        
        assert tag.text == f"Welcome, {username}!"

        wait.until(EC.presence_of_element_located((By.PARTIAL_LINK_TEXT, testWebsite)))
        a_shortUrl = wait.until(EC.presence_of_element_located((By.PARTIAL_LINK_TEXT,"http://localhost:8000/api/url/r/")))

        driver.get(a_shortUrl.text)
        time.sleep(1)
        assert str(driver.current_url) == testWebsite
        driver.back()
        
        assert test_logout.test_logout_success(driver) is True
        return True
    except AssertionError:
        return False
