# Test Case
#----------------------------
# 1) Open Web Browser (Chrome/firefox/Edge)\
# 2) Open URL https://networkbuilders.intel.com/
# 3) Enter user name
# 4) Enter Password
# 5) Click on Login
# 6) Capture title of the home page
# 7) Verify title of the page
# 8) Close Browser

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# ChromeDriver path
service_obj = Service(r"C:\Drivers\chromedriver-win64\chromedriver.exe")

# Chrome Options
chrome_options = Options()
chrome_options.add_argument("--remote-debugging-port=9222")

try:
    # Initialize WebDriver
    print("Starting WebDriver...")
    driver = webdriver.Chrome(service=service_obj, options=chrome_options)
    print("WebDriver started successfully.")

    # Open URL
    print("Navigating to the URL...")
    driver.get("https://networkbuilders.intel.com")

    # Wait and interact with elements
    username_field = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.NAME, "username"))
    )
    username_field.send_keys("ghanshyamons")

    password_field = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.ID, "password"))
    )
    password_field.send_keys("abc@1234567")

    submit_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "btnsubmit"))
    )
    submit_button.click()

    # Verify title
    WebDriverWait(driver, 10).until(
        EC.title_is("Login | Intel® Industry Solution Builders")
    )
    print("Login Test Passed.")

except Exception as e:
    print(f"An error occurred: {e}")

finally:
    # Quit WebDriver
    driver.quit()
    print("WebDriver closed.")
