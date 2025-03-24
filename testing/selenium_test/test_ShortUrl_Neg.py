from selenium.webdriver.common.by import By
import random, string,time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def test_shortUrl_Neg(driver): 
    try:
        longstr = "_"*1000
        testWebsite = ["00","","[]","{}",longstr,"https://\\<script>alert('test')</script>","/ or 1=1","<script>alert('test')</script>","<img src=x onerror=alert('test')>"]
        a_element = driver.find_element(By.LINK_TEXT,"首頁")
        a_element.click()
        for website in testWebsite:
            inputField = driver.find_element(By.XPATH, "//input[@class='form-control']")
            inputField.send_keys(website)
            time.sleep(2)
            wait = WebDriverWait(driver, timeout=2)
            error_message = inputField.get_attribute("validationMessage")
            assert error_message == "請輸入網址。" or error_message == "請填寫這個欄位。"
            inputField.clear()
            
        
        driver.back()
        driver.refresh()
        
        return True
    except AssertionError as E:
        print(f"Error {E}")
        return False
    

