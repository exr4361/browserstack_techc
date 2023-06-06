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
        "maskCommands" : "setValues, getValues",
        "build": BS_BUILD_NAME
    },
    {
        "os": "Windows",
        "osVersion": "10",
        "sessionName": "BStack parallel python 2",
        "browserName": "chrome",
        "browserVersion": "latest",
        "maskCommands" : "setValues, getValues",
        "build": BS_BUILD_NAME
    },
    {
        "deviceName": "Samsung Galaxy S22",
        "osVersion": "12.0",
        "sessionName": "BStack parallel python 3",
        "browserName": "chrome",
        "real_mobile": "true",
        "browserVersion": "latest",
        "deviceOrientation": "portrait",
        "maskCommands" : "setValues, getValues",
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

  try: # Mobile only test
    mobile_menu = driver.find_element_by_id("primary-menu-toggle") # Checks if menu is visible
    mobile_menu.click()
    try:
                # Go to login page on mobile
                mobile_menu.click()
                login_button = driver.find_element(By.LINK_TEXT, "Sign in")
                login_button.click()
                
                # Login using your trial credentials
                user_input = WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.ID, "user_email_login")))
                user_input.send_keys(bs_email)
                pass_input = driver.find_element_by_id("user_password")
                pass_input.send_keys(bs_password)
                pass_input.send_keys(Keys.RETURN)
                
                # 2. Make sure that the homepage includes a link to invite users and retrieve the link’s URL  
                driver.implicitly_wait(1) # Wait for dashboard/home to load
                mobile_menu.click()
                invite_link = find_element(By.LINK_TEXT, "Invite team")
                invite_page = WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.CLASS_NAME, "manage-users__invite-copyLink-text")))
                invite_url = invite_page.get_attribute('innerHTML')
                print("URL to invite users:", invite_url)
   
                # 3. Log out of BrowserStack
                mobile_menu.click()
                logout_button = driver.find_element(By.TEXT_LINK, "Sign out")
                logout_button.click()
                                                         
                
    except NoSuchElementException as err:
        message = "Exception: " + str(err.__class__) + str(err.msg)
        driver.execute_script(
            'browserstack_executor: {"action": "setSessionStatus", "arguments": {"status":"failed", "reason": ' + json.dumps(message) + '}}')
    except Exception as err:
        message = "Exception: " + str(err.__class__) + str(err.msg)
        driver.execute_script(
            'browserstack_executor: {"action": "setSessionStatus", "arguments": {"status":"failed", "reason": ' + json.dumps(message) + '}}')
                
    # Mark test as passed
    driver.execute_script(
        'browserstack_executor: {"action": "setSessionStatus", "arguments": {"status":"failed", "reason": ' + json.dumps(message) + '}}')          
            
  except: # Desktop only test
    try:
                # Go to login page on desktop
                login_button = WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.LINK_TEXT, "Sign in")))
                login_button.click()
                
                # Login using your trial credentials
                user_input = WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.ID, "user_email_login")))
                user_input.send_keys(bs_email)
                pass_input = driver.find_element_by_id("user_password")
                pass_input.send_keys(bs_password)
                pass_input.send_keys(Keys.RETURN)
                
                # 2. Make sure that the homepage includes a link to invite users and retrieve the link’s URL 
                invite_link = WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.LINK_TEXT, "Invite team")))
                assert invite_link.is_displayed(), "Invite user link not found on the homepage" # No invite link found in homepage when logged in
                invite_link.click()
                invite_page = WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.CLASS_NAME, "manage-users__invite-copyLink-text")))
                invite_url = invite_page.get_attribute('innerHTML')
                print("URL to invite users:", invite_url)
                
                # 3. Log out of BrowserStack
                user_account = WebDriverWait(driver, 1).until(EC.element_to_be_clickable((By.ID, "account-menu-toggle"))).click() # Wait for the dropdown menu to open
                logout_button = driver.find_element(By.TEXT_LINK, "Sign out")
                logout_button.click()
                                                                                                                
                
    except NoSuchElementException as err:
        message = "Exception: " + str(err.__class__) + str(err.msg)
        driver.execute_script(
            'browserstack_executor: {"action": "setSessionStatus", "arguments": {"status":"failed", "reason": ' + json.dumps(message) + '}}')
    except Exception as err:
        message = "Exception: " + str(err.__class__) + str(err.msg)
        driver.execute_script(
            'browserstack_executor: {"action": "setSessionStatus", "arguments": {"status":"failed", "reason": ' + json.dumps(message) + '}}')
    
    # Mark test as passed
    driver.execute_script(
        'browserstack_executor: {"action": "setSessionStatus", "arguments": {"status":"failed", "reason": ' + json.dumps(message) + '}}')    
  finally:
    # Close the browser
    driver.quit()
            
for browser in browsers:
  Thread(target=tech_challenge, args=(browser,)).start()
