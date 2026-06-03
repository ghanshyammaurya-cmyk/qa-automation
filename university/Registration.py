from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time

# Define credentials and URLs
USERNAME = "admin"
PASSWORD = "Intel@2025"
BASE_URL = "https://builders-qa.onsumaye.com"
#LOGIN_URL = f"https://{USERNAME}:{PASSWORD}@builders-qa.onsumaye.com/login"
#COURSE_URL = "https://builders-qa.onsumaye.com/university/course/ai-in-retail-workshop"

# Configure Chrome options
chrome_options = Options()
chrome_options.add_argument("--start-maximized")

# Path to your ChromeDriver
chrome_driver_path = r'C:\Drivers\chromedriver-win64\chromedriver.exe'

# Initialize the WebDriver
service = Service(chrome_driver_path)
driver = webdriver.Chrome(service=service, options=chrome_options)

# Navigate to the registration page
driver.get("https://builders-qa.onsumaye.com/registration")

try:
    # Fill in the Email ID
    email_field = driver.find_element(By.NAME, "c_email")
    email_field.send_keys("johndoe@tcx.com")

    # Fill in the Company Name
    company_field = driver.find_element(By.NAME, "c_name")
    company_field.send_keys("TCX")

    # Select Community Memberships (Multi-checkbox)
    # Assuming checkboxes have specific IDs or names; update accordingly
    communities = ["Network Builders", "Industrial Builders"]  # Example selections
    for community in communities:
        checkbox = driver.find_element(By.XPATH, f"//input[@type='checkbox' and @value='{community}']")
        if not checkbox.is_selected():
            checkbox.click()

    # Fill in the Contact Name
    contact_name_field = driver.find_element(By.NAME, "c_contact_name")
    contact_name_field.send_keys("John Doe")

    # Fill in the Job Title
    job_title_field = driver.find_element(By.NAME, "jobDesignation")
    job_title_field.send_keys("Software Engineer")

    # Select Country/Region from Drop-down
    country_dropdown = Select(driver.find_element(By.NAME, "countryId"))
    country_dropdown.select_by_visible_text("United States")  # Update as needed

    # Submit the form
    submit_button = driver.find_element(By.XPATH, "//button[@type='submit']")
    submit_button.click()

    # Optional: Wait for confirmation page to load
    time.sleep(5)

except Exception as e:
    print(f"An error occurred: {e}")

finally:
    # Close the browser
    driver.quit()
