class HomePage:
    def __init__(self, page):
        self.page = page

    def open_url(self, url):
        self.page.goto(url)

    def click_engagement_menu(self):
        self.page.click("text=Engagement")

    def click_submit_offering(self):
        self.page.click("text=Submit an Offering")