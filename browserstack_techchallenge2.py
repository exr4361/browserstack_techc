from threading import Thread
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json
import os

# Environment Variables
BS_USERNAME = os.environ.get(
    "BROWSERSTACK_USERNAME")
BS_ACCESS_KEY = os.environ.get(
    "BROWSERSTACK_ACCESS_KEY")
URL = "https://{}:{}@hub.browserstack.com/wd/hub".format(BS_USERNAME, BS_ACCESS_KEY)
BS_BUILD_NAME = os.environ.get("BROWSERSTACK_BUILD_NAME")


# BrowserStack trial credentials
bs_email = os.getenv("BS_Credentials_USR")  # BrowserStack email from Jenkinsfile
bs_pass = os.getenv("BS_Credentials_PSW")  # BrowerStack password from JenkinsFile

# Set up capabilities for each browser
browsers = [
    {
        "os": "OS X",
        "osVersion": "Ventura",
        "sessionName": "BStack parallel python 1",
        "browserName": "firefox",
        "browserVersion": "latest",
        "browserstack.maskCommands": "setValues",
        "buildName": BS_BUILD_NAME
    },
    {
        "os": "Windows",
        "osVersion": "10",
        "sessionName": "BStack parallel python 2",
        "browserName": "chrome",
        "browserVersion": "latest",
        "browserstack.maskCommands": "setValues",
        "buildName": BS_BUILD_NAME
    },
    {
        "deviceName": "Samsung Galaxy S22",
        "osVersion": "12.0",
        "sessionName": "BStack parallel python 3",
        "browserName": "samsung",
        "browserVersion": "latest",
        "deviceOrientation": "portrait",
        "browserstack.maskCommands": "setValues",
        "buildName": BS_BUILD_NAME,
    }
]

# Run function for test 
def tech_challenge(browser):
  driver = webdriver.Remote(
      command_executor=URL,
      desired_capabilities=browser)

  # 1. Go to homepage
  driver.get("https://www.browserstack.com/")
  driver.maximize_window() # Full width for desktop tests
  windowSize = driver.get_window_size()
  windowWidth = windowSize['width']
  try:
    # Mobile Browser Test
    if windowWidth < 991:
        
        # Go to login page
        driver.find_element_by_id("primary-menu-toggle").click()
        login_button = driver.find_element(By.LINK_TEXT, "Sign in")
        login_button.click()
        
        # Login using your trial credentials
        user_input = driver.find_element(By.ID, "user_email_login")
        user_input.send_keys(bs_email)
        pass_input = driver.find_element(By.ID, "user_password")
        pass_input.send_keys(bs_pass)

        # Trigger the "Enter" key event on the password input field
        pass_input.send_keys(Keys.RETURN)
        
        # 2. Retrieve share link
        driver.find_element(By.ID, "primary-menu-toggle").click()
        invite_link = driver.find_element(By.ID, "invite-link")
        assert invite_link.is_displayed(), "Invite user link not found" # No invite link found when logged in
        invite_link.click()
        
        # Find the exact span element with the share link
        invite_url = driver.find_element_by_xpath('.//span[@class = "manage-users__invite-copyLink-text"]')
        invite_page = invite_url.get_property('textContent') # Get the innerHTML of the span element
        print("URL to invite users:", invite_page)
        
        # 3. Log out of BrowserStack
        driver.find_element(By.ID, "primary-menu-toggle").click()
        driver.find_element(By.LINK_TEXT, "Sign out").click()
        
        driver.execute_script('browserstack_executor: {"action": "setSessionStatus", "arguments": {"status":"passed", "reason": "Test passed"}}')
        driver.quit()
        
  except Exception as err:
        message = "Exception: " + str(err.__class__) + str(err.msg)
        driver.execute_script(
            'browserstack_executor: {"action": "setSessionStatus", "arguments": {"status":"failed", "reason": ' + json.dumps(message) + '}}')

  try:
    # Desktop Browser Test
    if windowWidth > 991 :
        
        # Go to login page on desktop
        driver.find_element(By.LINK_TEXT, "Sign in").click()
    
        # Login using your trial credentials
        user_input = driver.find_element(By.ID, "user_email_login")
        user_input.send_keys(bs_email)
        pass_input = driver.find_element(By.ID, "user_password")
        pass_input.send_keys(bs_pass)
        pass_input.send_keys(Keys.RETURN)
                
        # 2. Make sure that the homepage includes a link to invite users and retrieve the link’s URL 
        invite_link = WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.ID, "invite-link")))
        assert invite_link.is_displayed(), "Invite user link not found on the homepage" # No invite link found in homepage when logged in
        invite_link.click()
        invite_page = WebDriverWait(driver, 3).until(EC.visibility_of_element_located((By.CLASS_NAME, "manage-users__invite-copyLink-text")))
        invite_url = invite_page.get_attribute('innerHTML')
        print("URL to invite users:", invite_url)
                
        # 3. Log out of BrowserStack
        user_account = driver.find_element(By.ID, "account-menu-toggle").click() # Wait for the dropdown menu to open
        logout_button = driver.find_element(By.TEXT_LINK, "Sign out")
        logout_button.click()
                
        # Mark test as passed
        driver.execute_script('browserstack_executor: {"action": "setSessionStatus", "arguments": {"status":"passed", "reason": "Test passed"}}')
        driver.quit()
        
  except Exception as err:
        message = "Exception: " + str(err.__class__) + str(err.msg)
        driver.execute_script(
            'browserstack_executor: {"action": "setSessionStatus", "arguments": {"status":"failed", "reason": ' + json.dumps(message) + '}}')

for browser in browsers:
  Thread(target=tech_challenge, args=(browser,)).start()
