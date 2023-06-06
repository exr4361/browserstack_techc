from threading import Thread
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import os

# Environment Variables
BS_USERNAME = os.environ.get(
    "BROWSERSTACK_USERNAME")
BS_ACCESS_KEY = os.environ.get(
    "BROWSERSTACK_ACCESS_KEY")
URL = "https://{}:{}@hub.browserstack.com/wd/hub".format(BS_USERNAME, BS_ACCESS_KEY)
BS_BUILD_NAME = os.environ.get("BROWSERSTACK_BUILD_NAME")

# BrowserStack Trial credentials
bs_email = os.getenv("BS_Credentials_USR")  # BrowserStack email from Jenkinsfile
bs_password = os.getenv("BS_Credentials_PSW")  # BrowerStack password from JenkinsFile

# Set up capabilities for each browser
browsers = [
    {
        "os": "OS X",
        "osVersion": "Ventura",
        "sessionName": "BStack parallel python 1",
        "browserName": "firefox",
        "browserVersion": "latest",
        "build": BS_BUILD_NAME
    },
    {
        "os": "Windows",
        "osVersion": "10",
        "sessionName": "BStack parallel python 2",
        "browserName": "chrome",
        "browserVersion": "latest",
        "build": BS_BUILD_NAME
    },
    {
        "deviceName": "Samsung Galaxy S22",
        "osVersion": "12.0",
        "sessionName": "BStack parallel python 3",
        "browserName": "samsung",
        "deviceOrientation": "portrait",
        "realMobile": "true",
        "build": BS_BUILD_NAME
    }
]

# Run function for test 
def tech_challenge(browser):
  driver = webdriver.Remote(
      command_executor=URL,
      desired_capabilities=browser)
  if "deviceName" not in browser:
      try:
            # 1. Go to homepage and login to account
            login_button = driver.find_element(By.CLASS_NAME, "sign-in-link")
            mobile_menu = driver.find_element(By.ID, "primary-menu-toggle")
            driver.get("https://www.browserstack.com/")
            if login_button.is_displayed():
                driver.maximize_window()
                WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.CLASS_NAME, "sign-in-link")))
                login_button.click()
             else:
                mobile_menu.click()
                login_button.click()

            # Login using your trial credentials
            user_input =
            user_input = WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.ID, "user_email_login")))
            user_input.send_keys(bs_email)
            pass_input = driver.find_element_by_id("user_password")
            pass_input.send_keys(bs_password)
            pass_input.send_keys(Keys.RETURN)

            # 2. Make sure that the homepage includes a link to invite users and retrieve the link’s URL  
            invite_link = WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.ID, "invite-link"))) # Wait for the login to complete and the homepage to load
            invite_link.click()
            assert invite_link.is_displayed(), "Invite user link not found on the homepage" # No invite link found in homepage when logged in
            invite_page = WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.CLASS_NAME, "manage-users__invite-copyLink-text")))
            invite_url = invite_page.get_attribute("innerHTML")
            print("URL to invite users:", invite_url)

            # 3. Log out of BrowserStack
            user_account = WebDriverWait(driver, 1).until(EC.element_to_be_clickable((By.ID, "account-menu-toggle"))) # Wait for the dropdown menu to open
            user_account.click()
            logout_button = WebDriverWait(driver, 1).until(EC.element_to_be_clickable((By.ID, "sign_out_link")))
            logout_button.click()

            # For marking test as passed
            driver.execute_script('browserstack_executor: {"action": "setSessionStatus", "arguments": {"status":"passed", "reason": "Test passed!"}}')

            

      except NoSuchElementException as err:
            message = "Exception: " + str(err.__class__) + str(err.msg)
            driver.execute_script(
                'browserstack_executor: {"action": "setSessionStatus", "arguments": {"status":"failed", "reason": ' + json.dumps(message) + '}}')
      except Exception as err:
            message = "Exception: " + str(err.__class__) + str(err.msg)
            driver.execute_script(
                'browserstack_executor: {"action": "setSessionStatus", "arguments": {"status":"failed", "reason": ' + json.dumps(message) + '}}')
      finally:
            # Close the browser
            driver.quit()
            
for browser in browsers:
  Thread(target=tech_challenge, args=(browser,)).start()
