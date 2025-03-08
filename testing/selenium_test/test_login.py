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
    finally:
        driver.quit()
