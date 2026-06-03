from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import time

# Setup Chrome options
options = Options()
options.add_argument("--start-maximized")

# Initialize ChromeDriver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# Correct URL with embedded credentials
username = "admin"
password = "Intel%402025"

domain_with_path = "builders-qa.onsumaye.com/contact-us"
url = "https://admin:Intel%402025@builders-qa.onsumaye.com/contact-us"
#url = f"https://{username}:{password}@{domain_with_path}"

# Open the page
driver.get(url)

# Wait for form to load
wait = WebDriverWait(driver, 20)

# Fill out text fields
wait.until(EC.presence_of_element_located((By.NAME, "cname"))).send_keys("John")
driver.find_element(By.NAME, "phone").send_keys("87873456778")
driver.find_element(By.NAME, "email").send_keys("johndoe@example.com")

# Fill in message
#driver.find_element(By.NAME, "message").send_keys("This is a test message submitted via Selenium automation.")

# Accept Terms (checkbox)
#driver.find_element(By.NAME, "acceptTerms").click()

# Submit form
submit_button = driver.find_element(By.XPATH, "//button[@type='submit']")  # corrected button type if necessary
submit_button.click()

# Wait before closing
time.sleep(5)
driver.quit()
