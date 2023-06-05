from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.safari.options import Options as SafariOptions
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from threading import Thread
import time
import json
import os

# Environment Variables
username = os.getenv("BROWSERSTACK_USERNAME")
access_key = os.getenv("BROWSERSTACK_ACCESS_KEY")
build_name = os.getenv("BROWSERSTACK_BUILD_NAME")
browserstack_local = os.getenv("BROWSERSTACK_LOCAL")
browserstack_local_identifier = os.getenv("BROWSERSTACK_LOCAL_IDENTIFIER")
URL = "https://hub.browserstack.com/wd/hub"

bs_local_args = { "key": access_key, "proxyHost": "127.0.0.1", "proxyPort": "8000"}

# BrowserStack Trial credentials
bs_email = os.getenv("BS_Credentials_USR")  # BrowserStack email from Jenkinsfile
bs_password = os.getenv("BS_Credentials_PSW")  # BrowerStack password from JenkinsFile
print("email:",bs_email);

# Set up capabilities for each browser
browsers = [
    {
        "os": "OS X",
        "osVersion": "Ventura",
        "sessionName": "BStack parallel python: " + build_name,
        "seleniumVersion" : "4.0.0",
        "browserName": "firefox",
        "browserVersion": "latest"
    },
    {
        "os": "Windows",
        "osVersion": "10",
        "sessionName": "BStack parallel python: " + build_name,
        "seleniumVersion" : "4.0.0",
        "browserName": "chrome",
        "browserVersion": "latest"
    },
    {
        "osVersion": "12.1",
        "deviceName": "Samsung Galaxy S22",
        "sessionName": "BStack parallel python: " + build_name,
        "seleniumVersion" : "4.0.0",
        "browserName": "samsung",
    },
]

# Function switch for desired browser
def get_browser_option(browser):
    switcher = {
        "chrome": ChromeOptions(),
        "firefox": FirefoxOptions(),
        "safari": SafariOptions(),
    }
    return switcher.get(browser, ChromeOptions())

# Run function for test
def tech_challenge(browser):
    # Set up the WebDriver with the desired capabilities
    bstack_options = {
        "osVersion": browser["osVersion"],
        "sessionName": browser["sessionName"],
        "build": build_name,
        "userName": username,
        "accessKey": access_key,
        "browserstack.local": browserstack_local,
        "browserstack.localIdentifier": browserstack_local_identifier,
    }
    if "os" in browser:
        bstack_options["os"] = browser["os"]
    if "deviceName" in browser:
        bstack_options['deviceName'] = browser["deviceName"]
    bstack_options["source"] = "python:tech-challenge:v1.2"
    if browser['browserName'] in ['ios']:
        browser['browserName'] = 'safari'
    options = get_browser_option(browser["browserName"].lower())
    if "browserVersion" in browser:
        options.browser_version = browser["browserVersion"]
    options.set_capability('bstack:options', bstack_options)
    if browser['browserName'].lower() == 'samsung':
        options.set_capability('browserName', 'samsung')
    driver = webdriver.Remote(
        command_executor=URL,
        options=options)
  
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
    
    # Run test on browsers in parallel
    for browser in browsers:
        Thread(target=tech_challenge, args=(browser,)).start()
        





