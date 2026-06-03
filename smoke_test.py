from playwright.sync_api import sync_playwright

URL = "https://builders.intel.com/ecosystem-engagement/solution-hub/edge-ai-catalog/partner-showcase"

def test_partner_filter_smoke():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=500)
        context = browser.new_context()
        page = context.new_page()

        # IMPORTANT: use domcontentloaded, NOT networkidle
        page.goto(URL, wait_until="domcontentloaded")

        # Extra explicit wait for page stability
        page.wait_for_timeout(5000)

        # Screenshot to confirm page loaded
        page.screenshot(path="page_loaded.png", full_page=True)

        print("Page title:", page.title())

        # Close safely
        context.close()
        browser.close()

if __name__ == "__main__":
    test_partner_filter_smoke()
