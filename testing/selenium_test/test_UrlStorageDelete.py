from selenium.webdriver.common.by import By
import random, string,time
from selenium.webdriver.support.ui import WebDriverWait
        username_input.send_keys(username)
        password_input.send_keys(password)
        a_element.click()
        time.sleep(2)
        tag = wait.until(EC.presence_of_element_located((By.TAG_NAME,"h2")))
        
        assert tag.text == f"Welcome, {username}!"

        button = wait.until(EC.presence_of_element_located((By.CLASS_NAME,"btn-danger")))
        button.click()
        time.sleep(2)
        try:
            alert = wait.until(EC.alert_is_present())
            assert alert.text == "Are you sure you want to delete this short URL?"
            alert.accept()
        except NoAlertPresentException:
            print("alert1")
            return False 
        try:
            alert = wait.until(EC.alert_is_present())
            assert alert.text == "Deleted successfully", "alert2"
            alert.accept()
        except NoAlertPresentException:
            print("alert2")
            return False
        return True
    except AssertionError:
        return False