from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
        random_id = random.randint(1, 1000000)
        user_name = f"Tester{random_id}"
        assert input_username_element.text == ""
        input_username_element.send_keys(user_name)
        assert input_password_element.text == ""
        input_password_element.send_keys("111111A")
        assert input_confirmPw_element.text == ""
        input_confirmPw_element.send_keys("111111A")

        button_elemnt.click()

        time.sleep(2)

        wait = WebDriverWait(driver, timeout=2)
        alert = wait.until(lambda d : d.switch_to.alert)
        text = alert.text
        alert.accept()
        assert text == "Sign up successful, please sign in"

        a_element = driver.find_element(By.LINK_TEXT,"Home")
        a_element.click()
        return True
    
    except AssertionError:
        return False