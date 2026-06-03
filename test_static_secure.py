import re
import os
import pytest
from playwright.sync_api import sync_playwright

# =========================
# LOAD ENV VARIABLES (FIXED PATH)
# =========================
from dotenv import load_dotenv
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # same folder
env_path = os.path.join(BASE_DIR, ".env")

load_dotenv(env_path)

HTACCESS_USERNAME = os.getenv("HT_USER")
HTACCESS_PASSWORD = os.getenv("HT_PASS")

if not HTACCESS_USERNAME or not HTACCESS_PASSWORD:
    raise ValueError("❌ HT Access credentials not set. Please set HT_USER and HT_PASS")

# =========================
# TEST DATA
# =========================
PAGES = [
    {
        "name": "Industrial Community",
        "url": os.getenv("BASE_URL_INDUSTRIAL"),
        "expected_text": ["Industrial Builders", "Overview", "Solutions", "Training"],
    },
    {
        "name": "Retail Community",
        "url": os.getenv("BASE_URL_RETAIL"),
        "expected_text": ["Retail Builders", "Overview"],
    },
    {
        "name": "Video and AI Cities Community",
        "url": os.getenv("BASE_URL_VIDEO"),
        "expected_text": ["Video", "Overview"],
    },
    {
        "name": "Healthcare Community",
        "url": os.getenv("BASE_URL_HEALTH"),
        "expected_text": ["Healthcare", "Overview"],
    },
]

for page in PAGES:
    if not page["url"]:
        raise ValueError(f"❌ URL missing in .env for: {page['name']}")

IGNORED_PATTERNS = [
    r"google-analytics\.com",
    r"googlesyndication\.com",
    r"doubleclick\.net",
    r"sharethis\.com",
    r"onetrust\.com",
    r"cookieconsent",
    r"recaptcha",
    r"google\.com/recaptcha",
    r"dogo\.intel\.com",
    r"googletagmanager\.com",
    r"gstatic\.com",
    r"crwdcntrl\.net",
]

SUSPECT_CONTENT_PATTERNS = [
    r"/api/",
    r"/graphql",
    r"/rest/",
    r"/ajax/",
    r"/json",
    r"search",
    r"listing",
    r"filter",
    r"loadmore",
]
# =========================
# HELPERS
# =========================
def is_ignored_request(url: str) -> bool:
    url = url.lower()
    return any(re.search(pattern, url) for pattern in IGNORED_PATTERNS)


def is_suspect_content_request(url: str) -> bool:
    url = url.lower()
    return any(re.search(pattern, url) for pattern in SUSPECT_CONTENT_PATTERNS)

# =========================
# FIXTURE
# =========================
@pytest.fixture(scope="function")
def browser_page():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)

        context = browser.new_context(
            ignore_https_errors=False,  # 🔐 safer than True
            http_credentials={
                "username": HTACCESS_USERNAME,
                "password": HTACCESS_PASSWORD,
            },
        )

        page = context.new_page()
        yield page
        browser.close()

# =========================
# TEST
# =========================
@pytest.mark.parametrize("page_data", PAGES, ids=[p["name"] for p in PAGES])
def test_staticized_pages(browser_page, page_data):
    page = browser_page
    suspect_requests = []
    all_xhr_fetch_requests = []

    def capture_request(request):
        if request.resource_type in ["xhr", "fetch"]:
            url = request.url
            all_xhr_fetch_requests.append(url)

            if not is_ignored_request(url) and is_suspect_content_request(url):
                suspect_requests.append(url)

    page.on("request", capture_request)

    # Stable load (avoid networkidle issues)
    response = page.goto(page_data["url"], wait_until="domcontentloaded", timeout=90000)
    page.wait_for_timeout(5000)

    body_text = page.locator("body").inner_text()
    html_source = page.content()

    missing_visible = [
        text for text in page_data["expected_text"]
        if text.lower() not in body_text.lower()
    ]

    missing_source = [
        text for text in page_data["expected_text"]
        if text.lower() not in html_source.lower()
    ]

    print("\n" + "=" * 80)
    print(f"Testing Page: {page_data['name']}")
    print(f"URL: {page_data['url']}")
    print(f"HTTP Status: {response.status if response else 'No response'}")

    print("\nVisible text check:")
    print("PASS" if not missing_visible else f"FAIL: {missing_visible}")

    print("\nHTML source check:")
    print("PASS" if not missing_source else f"FAIL: {missing_source}")

    print("\nAPI check:")
    print("PASS" if not suspect_requests else f"FAIL: {len(suspect_requests)} suspect requests")

    # Assertions
    assert response is not None
    assert response.status == 200
    assert not missing_visible
    assert not missing_source
    assert not suspect_requests

    print(f"\nFINAL RESULT for {page_data['name']}: PASS")

