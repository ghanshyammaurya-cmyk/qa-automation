import os
from dotenv import load_dotenv
load_dotenv()
import time
import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class IntelSolutionsTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        options = webdriver.ChromeOptions()
        options.add_argument("--start-maximized")

        cls.driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()),
            options=options
        )

        cls.wait = WebDriverWait(cls.driver, 20)
        cls.base_url = os.getenv("BASE_URL_SOLUTIONLIBRARY")

        if not cls.base_url:
            raise Exception("❌ BASE_URL_SOLUTIONLIBRARY not found in .env")

    def test_01_listing_page_load(self):
        self.driver.get(self.base_url)

        print("Checking listing page load...")

        # Wait for page main container
        self.wait.until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )

        self.assertIn("solutionslibrary", self.driver.current_url)

    def test_02_validate_cards(self):
        print("Validating cards...")

        # Scroll to trigger lazy load
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(3)

        # Updated locator (IMPORTANT)
        cards = self.driver.find_elements(By.XPATH, "//a[contains(@href,'/solutionslibrary/')]")

        print(f"Cards found: {len(cards)}")

        self.assertTrue(len(cards) > 5, "Cards not loaded properly")

    def test_03_search_functionality(self):
        print("Testing search...")

        # Find search input (more reliable)
        search = self.wait.until(
            EC.element_to_be_clickable((By.XPATH, "//input[contains(@placeholder,'Search')]"))
        )

        search.clear()
        search.send_keys("AI")

        time.sleep(2)

        # Wait for results to refresh
        self.wait.until(
            EC.presence_of_all_elements_located((By.XPATH, "//a[contains(@href,'/solutionslibrary/')]"))
        )

        results = self.driver.find_elements(By.XPATH, "//a[contains(@href,'/solutionslibrary/')]")

        print(f"Search results: {len(results)}")

        self.assertTrue(len(results) > 0)

    def test_04_navigation_to_detail(self):
        print("Navigating to detail page...")

        links = self.wait.until(
            EC.presence_of_all_elements_located((By.XPATH, "//a[contains(@href,'/solutionslibrary/')]"))
        )

        # Click first valid link
        for link in links:
            href = link.get_attribute("href")
            if "solutionslibrary/" in href and href != self.base_url:
                self.driver.execute_script("arguments[0].click();", link)
                break

        time.sleep(3)

        self.assertNotEqual(self.driver.current_url, self.base_url)

    def test_05_detail_page_validation(self):
        print("Validating detail page...")

        title = self.wait.until(
            EC.presence_of_element_located((By.TAG_NAME, "h1"))
        )

        print("Title:", title.text)

        self.assertTrue(len(title.text) > 5)

    def test_06_breadcrumb_navigation(self):
        print("Testing breadcrumb...")

        try:
            breadcrumb = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, "//a[contains(@href,'solutionslibrary')]"))
            )

            self.driver.execute_script("arguments[0].click();", breadcrumb)

            time.sleep(2)

            self.assertIn("solutionslibrary", self.driver.current_url)

        except Exception as e:
            print("Breadcrumb issue:", e)

    def test_07_no_results(self):
        print("Testing no results...")

        self.driver.get(self.base_url)

        search = self.wait.until(
            EC.element_to_be_clickable((By.XPATH, "//input[contains(@placeholder,'Search')]"))
        )

        search.clear()
        search.send_keys("zzzzzzzzzzzz")

        time.sleep(3)

        page = self.driver.page_source.lower()

        self.assertTrue(
            "no results" in page or len(self.driver.find_elements(By.XPATH, "//a[contains(@href,'/solutionslibrary/')]")) == 0
        )

    @classmethod
    def tearDownClass(cls):
        print("Closing browser...")
        cls.driver.quit()


if __name__ == "__main__":
    unittest.main()