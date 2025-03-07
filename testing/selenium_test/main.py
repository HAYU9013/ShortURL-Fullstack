import sys
import platform
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import test_title

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

        ###############其他 testcase 寫在下面###############




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
