from threading import Thread
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
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
    try:
        # 1. Go to homepage and login to account
        driver.get("https://www.browserstack.com/")
        time.sleep(3)  # Wait for the page to load
        login_button = driver.find_element_by_link_text("Sign in")
        login_button.click()
        time.sleep(5)  # Wait for the login page to load

        # Login using your trial credentials
        user_input = driver.find_element_by_id("user_email_login")
        user_input.send_keys(bs_email)
        pass_input = driver.find_element_by_id("user_password")
        pass_input.send_keys(bs_password)
        pass_input.send_keys(Keys.RETURN)

        # 2. Make sure that the homepage includes a link to invite users and retrieve the link’s URL
        time.sleep(5)  # Wait for the login to complete and the homepage to load
        invite_link = driver.find_element_by_link_text("Invite team")
        assert invite_link.is_displayed(), "Invite user link not found on the homepage" # No invite link found in homepage when logged in
        invite_url = invite_link.get_attribute("href")
        print("URL to invite users:", invite_url)

        # 3. Log out of BrowserStack
        user_account = driver.find_element_by_class_name("account-dropdown-toggle")
        user_account.click()
        time.sleep(1)  # Wait for the dropdown menu to open
        logout_button = driver.find_element_by_link_text("Logout")
        logout_button.click()
    
    except NoSuchElementException as err:
        message = "Exception: " + str(err.__class__) + str(err.msg)
        driver.execute_script(
            'browserstack_executor: {"action": "setSessionStatus", "arguments": {"status":"failed", "reason": ' + json.dumps(message) + '}}')
    except Exception as err:
        message = "Exception: " + str(err.__class__) + str(err.msg)
        driver.execute_script(
            'browserstack_executor: {"action": "setSessionStatus", "arguments": {"status":"failed", "reason": ' + json.dumps(message) + '}}')
        
    # For marking test as passed
    driver.execute_script('browserstack_executor: {"action": "setSessionStatus", "arguments": {"status":"passed", "reason": "Test passed"}}')
    
    # Close the browser
    driver.quit()
for browser in browsers:
  Thread(target=run_session, args=(browser,)).start()
