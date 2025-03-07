from selenium.webdriver.common.by import By

def test_title_exists(driver):
    try:
        h1_element = driver.find_element(By.TAG_NAME, "h1")
        assert h1_element.text == "就只是個縮網址的網站"
        return True
    except AssertionError:
        return False
    finally:
        driver.quit()
