import unittest
from selenium import webdriver
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import os
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService
import allure

class PythonOrgSearch(unittest.TestCase):
    def setUp(self):
        WINDOW_SIZE = "1920,1080"
        chrome_options = Options()
        #chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--disable-popup-blocking")
        chrome_options.add_argument("--window-size=%s" % WINDOW_SIZE)
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--start-maximized')

        chrome_options.add_argument('--disable-setuid-sandbox')

        # s = Service(executable_path=ChromeDriverManager().install())
        #s = Service('/home/ubuntu/script/pipeline/test/chromdriver/chromedriver')
        
        service = ChromeService(executable_path=ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service , options=chrome_options)
        # s = Service('/Users/qualityassurance/Desktop/automation-scripts/AVAXDEV_SHAHWAR/chromedriver')
        #self.driver = webdriver.Chrome(path, options=chrome_options)

    def test_search_in_python_org(self):
        self.driver.maximize_window()
        url = "https://avaxdev.akru.co"
        afterLoginURL = 'https://avaxdev.akru.co/dashboard'
        email = "ib_automation_seller@yopmail.com"
        wait = WebDriverWait(self.driver, 50)

        #comment change
        #new comment
        self.driver.get(url)
        print('SUCCESS: "'+url+'" saved in webdriver')

        time.sleep(3)
        try:
            loginButton=wait.until(EC.element_to_be_clickable((By.ID,"navbar-header-sticky-login")))
            loginButton.click()
            print('SUCCESS: Login button clicked')
        except:
            print("FAILED: Login button could not be clicked")
            raise Exception

        try:
            userPortalButton=wait.until(EC.element_to_be_clickable((By.XPATH,"//a[text()='User portal']")))
            userPortalButton.click()
            print('SUCCESS: User Portal button clicked')
        except:
            print("FAILED: User Portal button could not be clicked")
            raise Exception

        def cookiesHandle():
            try:
                time.sleep(3)
                cookiesClickerFound=wait.until(EC.element_to_be_clickable((By.XPATH,"//div[@class='d-flex justify-content-end']/button[3]")))
                cookiesClickerFound.click()
                print('SUCCESS: "Allow all cookies" button clicked')
            except:
                print('FAILED: "Allow all cookies" button could not be clicked')
                raise Exception
        cookiesHandle()

        time.sleep(3)
        MagicModalButtonFound= wait.until(EC.element_to_be_clickable((By.ID,"navbar-select-magic")))
        if MagicModalButtonFound:
            MagicModalButtonFound.click()
            print('SUCCESS: Magic button clicked')
        else:
            print("FAILED: Magic button could not be clicked")
            raise Exception

        time.sleep(3)
        emailBox= wait.until(EC.element_to_be_clickable((By.ID, 'navbar-magic-email')))
        if emailBox:
            emailBox.send_keys(email)
            print('SUCCESS: Email entered in magic modal')
        else:
            print('FAILED: Email could not be entered in magic modal')
            raise Exception

        time.sleep(3)
        magicNextButton = wait.until(EC.visibility_of_element_located((By.ID, "navbar-magic-next")))
        if magicNextButton:
            magicNextButton.click()
            print('SUCCESS: Magic next button clicked')
        else:
            print('FAILED: Magic next button could not be clicked')
            raise Exception

        def emailLogin():
            self.driver.execute_script("window.open('http://www.yopmail.com', 'new window')")
            self.driver.switch_to.window(self.driver.window_handles[1])
            print('SUCCESS: Switched to YOPMAIL tab')

            try:
                time.sleep(3)
                search = wait.until(EC.element_to_be_clickable((By.ID,"login")))
                search.clear()
                search.send_keys(email)
                search.send_keys(Keys.RETURN)
                print('SUCCESS: Email entered in YOPMAIL input field')
            except:
                print('FAILED: Email could not be entered in YOPMAIL input field')
                raise Exception

            time.sleep(3)
            self.driver.refresh()
            time.sleep(5)

            try:
                self.driver.switch_to.frame('ifmail')
                print('SUCCESS: Switched to YOPMAIL iframe')
            except:
                print("FAILED: Could not switch to iframe in YOPMAIL.")
                raise Exception

            try:
                time.sleep(3)
                LoginEmailButton=wait.until(EC.element_to_be_clickable((By.XPATH,'//strong[text()="Log in to Akru TestNet"]')))
                LoginEmailButton.click()
                print('SUCCESS: "Log in to Akru TestNet" button clicked from YOPMAIL')
            except:
                print('FAILED: Could not find "Log in to Akru TestNet" button.')
                raise Exception

        emailLogin()

        time.sleep(10)
        self.driver.close()
        self.driver.switch_to.window(self.driver.window_handles[1])
        self.driver.close()
        self.driver.switch_to.window(self.driver.window_handles[0])
        time.sleep(10)

        try:
            time.sleep(5)
            loader = wait.until(EC.invisibility_of_element_located((By.CLASS_NAME, 'loader-overlay')))
            time.sleep(3)
            print('SUCCESS: Loader Disappeared')
        except:
            print('FAILED: Loader did not appear or still loading')

        try:
            LoginToasterMessage = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'Toastify__toast-body')))
            print('SUCCESS: Toaster Appeared')
        except:
            print('FAILED: Toaster could not be appeared')

        if self.driver.current_url == afterLoginURL:
            print('\nSUCCESS: SUCCESSFULLY LOGGED IN. New URL is '+ afterLoginURL)
        else:
            print('\nFAILED: Could not login. As dashboard did not appear.\n')
            # print('\nFAILED: Success toaster could not be appeared. Instead toaster with the text: "'+LoginToasterMessage.text+'" appeared\n')
            raise Exception

    def tearDown(self):
        time.sleep(3)
        self.driver.save_screenshot("login.PNG")
        allure.attach.file(r"login.PNG", "screenshot",attachment_type=allure.attachment_type.PNG)
        time.sleep(3)
        self.driver.quit()

if __name__ == "__main__":
    unittest.main()
