from selenium.webdriver.common.by import By

def test_register_exists(driver):
    try:
        a_element = driver.find_element(By.LINK_TEXT, "註冊")
        assert a_element.text == "註冊"
        a_element.click()
        h2_element = driver.find_element(By.TAG_NAME, "h2")
        assert a_element.text == "註冊"
        return True
    except AssertionError:
        return False
    finally:
        driver.quit()
