class DashboardPage:
    def __init__(self, page):
        self.page = page

    def navigate_to_solutions_challenge(self):
        self.page.goto("https://builders-qa.onsumaye.com/ecosystem-engagement/solutions-challenge")
        self.page.wait_for_load_state("load")

    def click_ai_edge_tab(self):
        self.page.wait_for_selector("text=AI Edge Application", timeout=15000)
        self.page.click("text=AI Edge Application")

    def click_learn_more(self):
        self.page.wait_for_selector("text=Learn More", timeout=15000)
        self.page.click("text=Learn More")

        # ✅ STEP 1 (ADD HERE)
        self.page.wait_for_load_state("load")
        print("👉 URL after Learn More:", self.page.url)
        self.page.screenshot(path="after_learn_more.png")

    def verify_projects_page(self):
        self.page.wait_for_load_state("load")

        print("👉 Final URL:", self.page.url)

        # ✅ UI validation (strong)
        self.page.wait_for_selector("text=AI Edge Application", timeout=15000)

        print("🎉 Successfully landed on AI Edge page")