from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC

driver = webdriver.Chrome()

# Include HT Access login in URL
driver.get("https://admin:CommLoan%402025@www.commloan-staging.com/get-a-quote")

wait = WebDriverWait(driver, 20)

# -----------------------------
# NO IFRAME – Form is in main DOM
# -----------------------------

# Loan Purpose
loan_purpose = wait.until(EC.element_to_be_clickable((By.ID, "loanPurposeID")))
Select(loan_purpose).select_by_visible_text("Purchase")

# Loan Amount
loan_amount = wait.until(EC.element_to_be_clickable((By.ID, "loanAmount")))
loan_amount.send_keys("5000000")

# Full Name
full_name = driver.find_element(By.ID, "applicantFname")
full_name.send_keys("John Test")

# Cell Number
cell_number = driver.find_element(By.ID, "applicantPhone")
cell_number.send_keys("123-123-9900")

# Email
email = driver.find_element(By.ID, "applicantEmail")
email.send_keys("john.test@gmail.com")

# Role in Deal
role = driver.find_element(By.ID, "roleDeal")
Select(role).select_by_visible_text("Borrower")

# Checkbox
checkbox = wait.until(EC.element_to_be_clickable((By.ID, "applicantAgree")))
checkbox.click()

print("Form filled successfully!")
