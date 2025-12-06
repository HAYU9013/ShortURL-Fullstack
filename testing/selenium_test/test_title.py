from selenium.webdriver.common.by import By

def test_title_exists(driver):
    try:
        h1_element = driver.find_element(By.TAG_NAME, "h1")
        assert h1_element.text == "URL Shortener"
        return True
    
    except AssertionError:
        return False
