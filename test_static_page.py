import re
import pytest
from playwright.sync_api import sync_playwright

URL = "https://builders-demo.onsumaye.com/communities/industrial"

EXPECTED_TEXT = [
    "Industrial Builders",
    "Overview",
    "Solutions",
    "Training"
]

# Domains/endpoints that should be ignored because they are tracking,
# analytics, ads, captcha, or third-party widgets
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
    r"gstatic\.com"
]

# Patterns that usually indicate real dynamic content/API loading
SUSPECT_CONTENT_PATTERNS = [
    r"/api/",
    r"/graphql",
    r"/rest/",
    r"/ajax/",
    r"/json",
    r"content",
    r"listing",
    r"search",
    r"filter",
    r"loadmore"
]


def is_ignored_request(url: str) -> bool:
    url = url.lower()
    return any(re.search(pattern, url) for pattern in IGNORED_PATTERNS)


def is_suspect_content_request(url: str) -> bool:
    url = url.lower()
    return any(re.search(pattern, url) for pattern in SUSPECT_CONTENT_PATTERNS)


@pytest.fixture(scope="function")
def browser_page():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(ignore_https_errors=True)
        page = context.new_page()
        yield page
        browser.close()


def test_page_loads_successfully(browser_page):
    page = browser_page
    response = page.goto(URL, wait_until="domcontentloaded", timeout=90000)
    page.wait_for_load_state("networkidle", timeout=90000)

    assert response is not None, "FAIL: No response received from page."
    assert response.status == 200, f"FAIL: Expected status 200, got {response.status}"

    print(f"\nPASS: Page loaded successfully with status {response.status}")


def test_expected_text_is_visible(browser_page):
    page = browser_page
    page.goto(URL, wait_until="domcontentloaded", timeout=90000)
    page.wait_for_load_state("networkidle", timeout=90000)

    body_text = page.locator("body").inner_text()

    missing_text = [text for text in EXPECTED_TEXT if text.lower() not in body_text.lower()]

    assert not missing_text, f"FAIL: Expected visible text missing: {missing_text}"

    print(f"\nPASS: All expected visible texts found: {EXPECTED_TEXT}")


def test_expected_text_exists_in_html_source(browser_page):
    page = browser_page
    page.goto(URL, wait_until="domcontentloaded", timeout=90000)
    page.wait_for_load_state("networkidle", timeout=90000)

    html_source = page.content()

    missing_in_source = [text for text in EXPECTED_TEXT if text.lower() not in html_source.lower()]

    assert not missing_in_source, f"FAIL: Expected text missing in HTML source: {missing_in_source}"

    print(f"\nPASS: All expected texts are present in HTML source: {EXPECTED_TEXT}")


def test_no_real_content_api_calls(browser_page):
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

    page.goto(URL, wait_until="domcontentloaded", timeout=90000)
    page.wait_for_load_state("networkidle", timeout=90000)

    print("\nINFO: All XHR/FETCH requests seen during test:")
    if all_xhr_fetch_requests:
        for req in all_xhr_fetch_requests:
            print(f" - {req}")
    else:
        print(" - None")

    assert not suspect_requests, (
        "FAIL: Real content/API requests detected, page may still be dynamic.\n"
        + "\n".join(suspect_requests)
    )

    print("\nPASS: No real content/API XHR-FETCH requests detected.")


def test_staticization_summary(browser_page):
    page = browser_page
    suspect_requests = []

    def capture_request(request):
        if request.resource_type in ["xhr", "fetch"]:
            url = request.url
            if not is_ignored_request(url) and is_suspect_content_request(url):
                suspect_requests.append(url)

    page.on("request", capture_request)

    response = page.goto(URL, wait_until="domcontentloaded", timeout=90000)
    page.wait_for_load_state("networkidle", timeout=90000)

    body_text = page.locator("body").inner_text()
    html_source = page.content()

    missing_visible = [text for text in EXPECTED_TEXT if text.lower() not in body_text.lower()]
    missing_source = [text for text in EXPECTED_TEXT if text.lower() not in html_source.lower()]

    assert response is not None and response.status == 200, "FAIL: Page did not load successfully."
    assert not missing_visible, f"FAIL: Visible content missing: {missing_visible}"
    assert not missing_source, f"FAIL: Source content missing: {missing_source}"
    assert not suspect_requests, (
        "FAIL: Dynamic content/API requests detected:\n" + "\n".join(suspect_requests)
    )

    print("\nFINAL RESULT: PASS")
    print("Page appears STATIC / SERVER-RENDERED.")