from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

# Enable auth handling
driver.execute_cdp_cmd(
    "Network.enable", {}
)

driver.execute_cdp_cmd(
    "Network.setExtraHTTPHeaders",
    {
        "headers": {
            "Authorization": "Basic YWRtaW46SW50ZWxAMjAyNQ=="
        }
    }
)

driver.get("https://builders-demo.onsumaye.com/contact-us")

wait = WebDriverWait(driver, 25)

email_input = wait.until(
    EC.presence_of_element_located((By.CSS_SELECTOR, "input[name='email']"))
)
email_input.send_keys("user@example.com")

submit_btn = wait.until(
    EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']"))
)
submit_btn.click()

print("✅ HT Access authenticated via headers")

driver.quit()
