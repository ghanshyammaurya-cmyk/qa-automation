class SSOPage:
    def __init__(self, page):
        self.page = page

    def login(self, email, password):

        # Step 1: Enter Email
        self.page.wait_for_selector("input[type='email']", timeout=20000)
        self.page.fill("input[type='email']", email)

        # Step 2: Click Next / Continue
        try:
            self.page.click("button:has-text('Next')")
        except:
            try:
                self.page.click("button:has-text('Continue')")
            except:
                pass

        # 🔥 IMPORTANT: wait for navigation AFTER email
        self.page.wait_for_load_state("networkidle")

        print("➡ Email submitted, waiting for password screen...")

        # Step 3: Wait for password field PROPERLY
        self.page.wait_for_selector(
            "input[type='password'], input[name='password']",
            timeout=30000
        )

        # Step 4: Enter Password
        self.page.fill("input[type='password'], input[name='password']", password)

        # Step 5: Click Sign in
        self.page.click("button:has-text('Sign in'), button:has-text('Login')")

        # Step 6: Wait for redirect back to app
        self.page.wait_for_url("**builders-qa.onsumaye.com**", timeout=60000)

        print("✅ Login successful, redirected back")