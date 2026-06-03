import re
import pytest
from playwright.sync_api import sync_playwright
from openpyxl import Workbook
from datetime import datetime

# Excel file name
REPORT_FILE = f"Static_Report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"

PAGES = [
    {
        "name": "Industrial",
        "url": "https://builders-demo.onsumaye.com/communities/industrial",
        "expected_text": ["Industrial Builders", "Overview", "Solutions", "Training"],
    },
    {
        "name": "Network",
        "url": "https://builders-demo.onsumaye.com/communities/network",
        "expected_text": ["Network Builders", "Overview"],
    },
    {
        "name": "Retail",
        "url": "https://builders-demo.onsumaye.com/communities/retail",
        "expected_text": ["Retail Builders", "Overview"],
    },
    {
        "name": "Video AI Cities",
        "url": "https://builders-demo.onsumaye.com/communities/video-ai-cities",
        "expected_text": ["Video", "Overview"],
    },
    {
        "name": "Healthcare",
        "url": "https://builders-demo.onsumaye.com/communities/healthcare-life-sciences",
        "expected_text": ["Healthcare", "Overview"],
    },
]

IGNORED_PATTERNS = [
    r"google-analytics",
    r"googlesyndication",
    r"doubleclick",
    r"sharethis",
    r"onetrust",
    r"recaptcha",
    r"dogo.intel",
    r"googletagmanager",
    r"gstatic",
    r"crwdcntrl"
]

SUSPECT_PATTERNS = [
    r"/api/",
    r"/graphql",
    r"/ajax",
    r"/json",
    r"search",
    r"listing",
    r"filter"
]

# Create Excel workbook
wb = Workbook()
ws = wb.active
ws.title = "Static Test Report"

# Header
ws.append([
    "Page Name", "URL", "HTTP Status",
    "Visible Content", "Source Content",
    "API Check", "Final Result"
])


def is_ignored(url):
    return any(re.search(p, url.lower()) for p in IGNORED_PATTERNS)


def is_suspect(url):
    return any(re.search(p, url.lower()) for p in SUSPECT_PATTERNS)


@pytest.mark.parametrize("page_data", PAGES)
def test_static_pages(page_data):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        suspect_requests = []

        def capture_request(request):
            if request.resource_type in ["xhr", "fetch"]:
                url = request.url
                if not is_ignored(url) and is_suspect(url):
                    suspect_requests.append(url)

        page.on("request", capture_request)

        response = page.goto(page_data["url"], wait_until="domcontentloaded", timeout=60000)
        page.wait_for_load_state("networkidle")

        body_text = page.locator("body").inner_text()
        html = page.content()

        # Checks
        visible_pass = all(t.lower() in body_text.lower() for t in page_data["expected_text"])
        source_pass = all(t.lower() in html.lower() for t in page_data["expected_text"])
        api_pass = len(suspect_requests) == 0

        final_result = "STATIC" if (visible_pass and source_pass and api_pass) else "DYNAMIC"

        # Write to Excel
        ws.append([
            page_data["name"],
            page_data["url"],
            response.status if response else "Fail",
            "PASS" if visible_pass else "FAIL",
            "PASS" if source_pass else "FAIL",
            "PASS" if api_pass else "FAIL",
            final_result
        ])

        print(f"\n{page_data['name']} → {final_result}")

        browser.close()


def teardown_module(module):
    wb.save(REPORT_FILE)
    print(f"\n📊 Excel Report Generated: {REPORT_FILE}")