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
import test_DuplicateAccount,test_ShortUrl, test_UrlStorage,test_UrlStorageDelete,test_StorageUrl
import test_ShortUrl_Neg, test_register_Neg, test_login_Neg
import test_welcome_message, test_password_valid1, test_password_valid2, test_password_valid3, test_spacebar_username


def setup_driver():
    chrome_options = Options()
    system_name = platform.system()

    if system_name == "Windows":
        # Windows 環境：設定 Windows 專用的參數
        #chrome_options.add_argument("--user-data-dir=C:\\temp\\unique_user_data_dir")
        chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
        service = Service()  
        driver = webdriver.Chrome(service=service, options=chrome_options)
    elif system_name == "Linux":
        # Ubuntu/CI 環境：設定 headless 模式與相關參數
        chrome_options.add_argument("--user-data-dir=/tmp/unique_user_data_dir")
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--window-size=1920,1080")
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

        result = test_welcome_message.test_welcome_message(driver)
        print("test_welocome_message passed" if result else "test_welocome_message failed")
        success = success and result

        result = test_password_valid1.test_password_valid1(driver)
        print("test_password_valid1 passed" if result else "test_password_valid1 failed")
        success = success and result

        result = test_password_valid2.test_password_valid2(driver)
        print("test_password_valid2 passed" if result else "test_password_valid2 failed")
        success = success and result

        result = test_password_valid3.test_password_valid3(driver)
        print("test_password_valid3 passed" if result else "test_password_valid3 failed")
        success = success and result

        result = test_spacebar_username.test_spacebar_username(driver)
        print("test_spacebar_username passed" if result else "test_spacebar_username failed")
        success = success and result

        #####
        
        login_result = test_login.test_login_exists(driver)
        print("test_login_exists passed" if login_result else "test_login_exists failed")
        success = success and login_result

        register_result = test_register.test_register_exists(driver)
        print("test_register_exists passed" if register_result else "test_register_exists failed")
        success = success and register_result

        register_result = test_register_Neg.test_register_fail_with_empty_box(driver)
        print("test_register_fail_with_empty_box passed" if register_result else "test_register_fail_with_empty_box failed")
        success = success and register_result
        
        register_result = test_register_Neg.test_register_fail_with_nonsame_password(driver)
        print("test_register_fail_with_nonsame_password passed" if register_result else "test_register_fail_with_nonsame_password failed")
        success = success and register_result
        
        register_result = test_register_Neg.test_register_fail_with_nonaccept_password(driver)
        print("test_register_fail_with_nonaccept_password passed" if register_result else "test_register_fail_with_nonaccept_password failed")
        success = success and register_result
        
        register_success_result = test_register.test_register_success(driver)
        print("test_register_success passed" if register_success_result else "test_register_success failed")
        success = success and register_success_result

        login_success_result = test_login.test_login_success(driver)
        print("test_login_success passed" if login_success_result else "test_login_success failed")
        success = success and login_success_result
        
        login_success_result = test_login_Neg.test_login_with_wrong_password(driver)
        print("test_login_with_wrong_password passed" if login_success_result else "test_login_with_wrong_password failed")
        success = success and login_success_result
        
        login_success_result = test_login.test_login_success(driver)
        print("test_login_success passed" if login_success_result else "test_login_success failed")
        success = success and login_success_result

        logout_success_result = test_logout.test_logout_success(driver)
        print("test_logout_success passed" if logout_success_result else "test_logout_success failed")
        success = success and logout_success_result
        #####
        
        
        result  = test_ShortUrl.test_shortUrl(driver, "https://www.google.com/")
        print("test_ShoutUrl passed" if result else "test_ShortUrl failed")
        success = success and result

        result  = test_ShortUrl_Neg.test_shortUrl_Neg(driver)
        print("test_ShoutUrl_Neg passed" if result else "test_ShortUrl_Neg failed")
        success = success and result

        result  = test_DuplicateAccount.test_register_Duplicate(driver)
        print("test_DuplicateAccount passed" if result else "test_DuplicateAccount failed")
        success = success and result


        result = test_UrlStorage.test_url_storage(driver,test_DuplicateAccount.accountList[0],test_DuplicateAccount.accountList[1],testWebsite= "https://www.google.com/")
        print("test_UrlStorage passed" if result else "test_UrlStorage failed")
        success = success and result

        result = test_StorageUrl.test_storageUrl(driver,test_DuplicateAccount.accountList[0],test_DuplicateAccount.accountList[1],testWebsite= "https://www.google.com/")
        print("test_StorageUrl passed" if result else "test_StorageUrl failed")
        success = success and result
        
        result = test_UrlStorageDelete.test_url_storage_delete(driver,test_DuplicateAccount.accountList[0],test_DuplicateAccount.accountList[1])
        print("test_UrlStorageDelete passed" if result else "test_UrlStorageDelete failed")
        success = success and result
        

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
