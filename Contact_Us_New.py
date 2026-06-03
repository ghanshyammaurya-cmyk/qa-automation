from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

USERNAME = "admin"
PASSWORD = "Intel@2025"

url = f"https://{USERNAME}:{PASSWORD}@builders-demo.onsumaye.com/contact-us"

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
wait = WebDriverWait(driver, 40)

driver.get(url)

# ---------------- SWITCH TO CORRECT IFRAME ----------------
wait.until(EC.presence_of_element_located((By.TAG_NAME, "iframe")))
iframe = driver.find_elements(By.TAG_NAME, "iframe")[0]
driver.switch_to.frame(iframe)

# ---------------- REQUEST TYPE (RADIO BUTTON) ----------------
# Select FIRST radio button safely (Feedback)
radio_buttons = wait.until(
    EC.presence_of_all_elements_located((By.XPATH, "//input[@type='radio']"))
)

driver.execute_script("arguments[0].click();", radio_buttons[0])

# ---------------- PROGRAM DROPDOWN ----------------
program_dropdown = wait.until(
    EC.element_to_be_clickable((By.TAG_NAME, "select"))
)
Select(program_dropdown).select_by_visible_text("Intel® Network Builders")

# ---------------- YOUR NAME ----------------
wait.until(
    EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Your Name']"))
).send_keys("QA Automation User")

# ---------------- EMAIL ----------------
wait.until(
    EC.presence_of_element_located(
        (By.XPATH, "//input[contains(@placeholder,'Email') or @type='email']")
    )
).send_keys("user@example.com")

# ---------------- PHONE ----------------
wait.until(
    EC.presence_of_element_located((By.XPATH, "//input[contains(@placeholder,'Phone')]"))
).send_keys("9876543210")

# ---------------- COUNTRY ----------------
country_dropdowns = driver.find_elements(By.TAG_NAME, "select")
Select(country_dropdowns[-1]).select_by_visible_text("India")

# ---------------- DESCRIPTION ----------------
wait.until(
    EC.presence_of_element_located((By.TAG_NAME, "textarea"))
).send_keys(
    "Automated QA test submission for Contact Us form with Bouncer email validation."
)

# ---------------- SUBMIT ----------------
submit = wait.until(
    EC.presence_of_element_located((
        By.XPATH,
        "//button[not(@disabled)] | //input[@type='submit' and not(@disabled)]"
    ))
)

driver.execute_script("arguments[0].scrollIntoView(true);", submit)
driver.execute_script("arguments[0].click();", submit)

print("✅ Contact Us form submitted successfully")

driver.quit()
