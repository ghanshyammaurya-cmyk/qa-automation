from playwright.sync_api import sync_playwright

SSO_LOGIN_URL = "https://your-app.com/login"
PROTECTED_URL = "https://your-app.com/dashboard"

USERNAME = "qa_test_user@company.com"
PASSWORD = "Password@123"   # Use test account only

def test_sso_login():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)  # keep False for debugging
        context = browser.new_context()
        page = context.new_page()

        # Step 1: Open App Login Page
        page.goto(SSO_LOGIN_URL)

        # Step 2: Click SSO Button
        page.click("text=Login with SSO")

        # Step 3: Enter SSO Credentials (IdP page)
        page.fill("input[type='email']", USERNAME)
        page.click("button:has-text('Next')")

        page.fill("input[type='password']", PASSWORD)
        page.click("button:has-text('Sign in')")

        # Optional: Handle "Stay signed in?"
        if page.locator("text=Yes").is_visible():
            page.click("text=Yes")

        # Step 4: Verify redirect back to app
        page.wait_for_url("**/dashboard**", timeout=15000)

        # Step 5: Validate protected page access
        page.goto(PROTECTED_URL)
        assert page.locator("text=Welcome").is_visible()

        print("✅ SSO Login Test Passed")

        browser.close()

if __name__ == "__main__":
    test_sso_login()
