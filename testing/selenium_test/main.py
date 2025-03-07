from selenium import webdriver
from selenium.webdriver.common.by import By
import test_title

def setup_driver():
    driver = webdriver.Chrome()
    driver.get("http://localhost:5173/")
    return driver

def run_test(driver):
    success = True
    
    ###############複製我 複製我 複製我去寫##############
    result = test_title.test_h1_exists(driver)
    print("test_h1_exists passed" if result else "test_h1_exists failed")
    success = success and result
    ###################################################

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
