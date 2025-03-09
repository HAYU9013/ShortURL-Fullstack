import sys
import platform
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import test_title
import test_register
import test_login
import test_logout

def setup_driver():
    chrome_options = Options()
    system_name = platform.system()

    if system_name == "Windows":
        # Windows 環境：設定 Windows 專用的參數
        chrome_options.add_argument("--user-data-dir=C:\\temp\\unique_user_data_dir")
        
        service = Service()  
        driver = webdriver.Chrome(service=service, options=chrome_options)
    elif system_name == "Linux":
        # Ubuntu/CI 環境：設定 headless 模式與相關參數
        chrome_options.add_argument("--user-data-dir=/tmp/unique_user_data_dir")
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")

        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    else:
        raise Exception("不支援的作業系統: " + system_name)

    driver.get("http://localhost:5173/")
    return driver

def run_test(driver):
    success = True

    try:
        ###############複製我 複製我 複製我去寫##############
        result = test_title.test_title_exists(driver)
        print("test_h1_exists passed" if result else "test_h1_exists failed")
        success = success and result
        ###################################################

        ###############複製我 複製我 複製我去寫##############
        result = test_title.test_title_exists(driver)
        print("test_h1_exists2 passed" if result else "test_h1_exists failed")
        success = success and result
        ###################################################

        ###############其他 testcase 寫在下面###############
        
        login_result = test_login.test_login_exists(driver)
        print("test_login_exists passed" if login_result else "test_login_exists failed")
        success = success and login_result

        register_result = test_register.test_register_exists(driver)
        print("test_register_exists passed" if register_result else "test_register_exists failed")
        success = success and register_result

        register_success_result = test_register.test_register_success(driver)
        print("test_register_success passed" if register_success_result else "test_register_success failed")
        success = success and register_success_result

        login_success_result = test_login.test_login_success(driver)
        print("test_login_success passed" if login_success_result else "test_login_success failed")
        success = success and login_success_result

        logout_success_result = test_logout.test_logout_success(driver)
        print("test_logout_success passed" if logout_success_result else "test_logout_success failed")
        success = success and logout_success_result

    except Exception as e:
        print(f"An error occurred: {e}")
        success = False
    finally:
        driver.quit()
    
    return success

if __name__ == "__main__":
    driver = setup_driver()
    success = run_test(driver)
    if success:
        print("All tests passed!")
        exit(0)
    else:
        print("Some tests failed.")
        exit(1)
