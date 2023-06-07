from threading import Thread
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
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
        "maskCommands" : "setValues, getValues",
        "seleniumLogs" : "false",
        "build": BS_BUILD_NAME
    },
    {
        "os": "Windows",
        "osVersion": "10",
        "sessionName": "BStack parallel python 2",
        "browserName": "chrome",
        "browserVersion": "latest",
        "maskCommands" : "setValues, getValues",
        "seleniumLogs" : "false",
        "build": BS_BUILD_NAME
    },
    {
        "deviceName": "Samsung Galaxy S22",
        "osVersion": "12.0",
        "sessionName": "BStack parallel python 3",
        "browserName": "samsung",
        "real_mobile": "true",
        "browserVersion": "latest",
        "deviceOrientation": "portrait",
        "maskCommands" : "setValues, getValues",
        "seleniumLogs" : "false",
        "build": BS_BUILD_NAME
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
        driver.find_element_by_id("primary-menu-toggle").click()
        # Go to login page
        login_button = driver.find_element(By.LINK_TEXT, "Sign in")
        login_button.click()
        
        # Login using your trial credentials
        # Find the email and password input fields
        email_input = driver.find_element_by_id("user_email_login")
        pass_input = driver.find_element_by_id("user_password")

        # Set the email value
        email_input.send_keys(bs_email)
        driver.execute_script("arguments[0].setAttribute('value', arguments[1]);", pass_input, bs_pass)

        # Trigger the "Enter" key event on the password input field
        driver.execute_script("var event = new KeyboardEvent('keydown', { key: 'Enter' }); arguments[0].dispatchEvent(event);", pass_input)
        
        # 2. Retrieve share link
        driver.find_element_by_id("primary-menu-toggle").click()
        invite_link = driver.find_element(By.ID, "invite-link")
        invite_link.click()
        
        invite_url = driver.find_element_by_xpath('.//span[@class = "manage-users__invite-copyLink-text"]')
        invite_page = invite_url.get_property('textContent')
        print("URL to invite users:", invite_page)
        
        # 3. Log out of BrowserStack
        driver.find_element(By.ID, "primary-menu-toggle").click()
        driver.find_element(By.LINK_TEXT, "Sign out").click()
        
        driver.execute_script('browserstack_executor: {"action": "setSessionStatus", "arguments": {"status":"passed", "reason": "Test passed"}}')
        driver.quit()
  except:
       pass
  try:
    # Desktop Browser Test
    if windowWidth > 991 :
        driver.find_element(By.LINK_TEXT, "Sign in").click()
        driver.execute_script('browserstack_executor: {"action": "setSessionStatus", "arguments": {"status":"passed", "reason": "Test passed"}}')
        driver.quit()
  except:
    pass

for browser in browsers:
  Thread(target=tech_challenge, args=(browser,)).start()
