from playwright.sync_api import sync_playwright

def save_login():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)

        context = browser.new_context(
            http_credentials={
                "username": "admin",
                "password": "Intel@2025"
            }
        )

        page = context.new_page()

        page.goto("https://builders-qa.onsumaye.com/")

        print("👉 Please login manually in browser...")

        input("✅ After successful login, press ENTER here...")

        # Save session
        context.storage_state(path="auth.json")

        print("🎉 Session saved successfully!")

        browser.close()

save_login()