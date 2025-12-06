from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def test_logout_success(driver):
    try:
        ## ?»å‡º
        a_element = driver.find_element(By.LINK_TEXT, "Logout")
        assert a_element.text == "Logout"
        a_element.click()

        logout_element = driver.find_element(By.CLASS_NAME, "logout-message")
        assert logout_element.text == "Logging out..."

        return True
    except AssertionError:
        return False
