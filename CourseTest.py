import csv
import time
import pickle
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

# Define credentials and URLs
USERNAME = "admin"
PASSWORD = "Intel@2025"
BASE_URL = "https://builders-qa.onsumaye.com"
LOGIN_URL = f"https://{USERNAME}:{PASSWORD}@builders-qa.onsumaye.com/login"
COURSE_URL = "https://builders-qa.onsumaye.com/university/course/ai-in-retail-workshop"

# Initialize WebDriver with HT Access Handling
options = Options()
options.add_argument("--ignore-certificate-errors")  # Ignore SSL issues
options.add_argument("--disable-popup-blocking")
options.add_argument("--start-maximized")

driver = webdriver.Chrome(options=options)
driver.get(LOGIN_URL)

# File to save test results
CSV_REPORT_FILE = "course_test_report.csv"

# Function to check all links on the course page
def check_links():
    broken_links = []
    try:
        links = driver.find_elements(By.TAG_NAME, "a")
        for link in links:
            url = link.get_attribute("href")
            if url and "http" in url:
                driver.execute_script(f"window.open('{url}');")
                time.sleep(2)
                driver.switch_to.window(driver.window_handles[-1])
                if "404" in driver.title:
                    print(f"Broken Link Detected: {url}")
                    broken_links.append(["Broken Link", url])
                driver.close()
                driver.switch_to.window(driver.window_handles[0])
        print("Link validation completed.")
    except Exception as e:
        print(f"Error checking links: {e}")
    return broken_links

# Function to test quiz functionality
def test_quiz():
    quiz_results = []
    try:
        quiz_buttons = driver.find_elements(By.CLASS_NAME, "quiz-start-button")  # Adjust class as per actual HTML
        for index, btn in enumerate(quiz_buttons, start=1):
            btn.click()
            time.sleep(2)
            options = driver.find_elements(By.CLASS_NAME, "quiz-option")  # Adjust class as per actual HTML
            if options:
                options[0].click()  # Select first answer
                submit_btn = driver.find_element(By.CLASS_NAME, "quiz-submit-button")  # Adjust class as per actual HTML
                submit_btn.click()
                time.sleep(2)
                print(f"Quiz {index} tested successfully")
                quiz_results.append([f"Quiz {index}", "Passed"])
            else:
                print(f"Quiz {index} has no options available.")
                quiz_results.append([f"Quiz {index}", "Failed - No Options"])
    except Exception as e:
        print(f"Quiz test failed: {e}")
        quiz_results.append(["Quiz Error", str(e)])
    return quiz_results

# Function to generate a CSV test report
def generate_report(link_results, quiz_results):
    with open(CSV_REPORT_FILE, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Test Type", "Details"])
        writer.writerows(link_results)
        writer.writerows(quiz_results)
    print(f"Test report saved: {CSV_REPORT_FILE}")

# Run the complete test process
check_links()
quiz_results = test_quiz()
generate_report(check_links(), quiz_results)

# Close browser
driver.quit()
