from selenium.webdriver.common.by import By
import random, string,time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def test_shortUrl(driver,testWebsite): 

    try:
        a_element = driver.find_element(By.LINK_TEXT,"Home")
        a_element.click()
        inputField = driver.find_element(By.XPATH, "//input[@class='form-control']")
        inputField.send_keys(testWebsite)
        button = driver.find_element(By.CLASS_NAME, "btn-custom")
        button.click()
        link = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.PARTIAL_LINK_TEXT, "http://localhost:8000/api/url/r/")))

        driver.get(link.text)
        assert str(driver.current_url) == testWebsite
        driver.back()
        driver.refresh()
        
        return True
    except AssertionError as E:
        print(f"Error {E}")
        return False

