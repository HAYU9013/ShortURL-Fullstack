from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
        assert input_password_element.text == ""
        input_password_element.send_keys("abc123456")

        button_element = driver.find_element(By.TAG_NAME, "button")
        button_element.click()

        time.sleep(2)

        h2_welcome_message = driver.find_element(By.TAG_NAME, "h2")
        assert h2_welcome_message.text == f"Welcome, {user_name}!"

        return True
    
    except AssertionError:
        return False