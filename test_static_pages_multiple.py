import re
import pytest
from playwright.sync_api import sync_playwright

# Add all community pages here
PAGES = [
    {
        "name": "Industrial Community",
        "url": "https://builders-demo.onsumaye.com/communities/industrial",
        "expected_text": ["Industrial Builders", "Overview", "Solutions", "Training"],
    },
    {
        "name": "Network Community",
        "url": "https://builders-demo.onsumaye.com/communities/network",
        "expected_text": ["Network Builders", "Overview"],
    },
    {
        "name": "Retail Community",
        "url": "https://builders-demo.onsumaye.com/communities/retail",
        "expected_text": ["Retail Builders", "Overview"],
    },
    {
        "name": "Video and AI Cities Community",
        "url": "https://builders-demo.onsumaye.com/communities/video-ai-cities",
        "expected_text": ["Video & AI Cities", "Overview"],
    },
    {
        "name": "Healthcare Community",
        "url": "https://builders-demo.onsumaye.com/communities/healthcare-life-sciences",
        "expected_text": ["Healthcare and Life Sciences", "Overview"],
    },
]

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
    r"content",
    r"listing",
    r"search",
    r"filter",
    r"loadmore",
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

    response = page.goto(page_data["url"], wait_until="domcontentloaded", timeout=90000)
    page.wait_for_load_state("networkidle", timeout=90000)

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
    if missing_visible:
        print(f"Missing visible text: {missing_visible}")
    else:
        print("PASS: All expected text is visible.")

    print("\nHTML source check:")
    if missing_source:
        print(f"Missing text in source: {missing_source}")
    else:
        print("PASS: All expected text is present in HTML source.")

    print("\nXHR/FETCH requests:")
    if all_xhr_fetch_requests:
        for req in all_xhr_fetch_requests:
            print(f" - {req}")
    else:
        print("No XHR/FETCH requests found.")

    if suspect_requests:
        print("\nSuspect content/API requests:")
        for req in suspect_requests:
            print(f" - {req}")
    else:
        print("\nPASS: No real content/API requests detected.")

    assert response is not None, f"FAIL: No response for {page_data['url']}"
    assert response.status == 200, f"FAIL: Expected status 200, got {response.status} for {page_data['url']}"
    assert not missing_visible, f"FAIL: Missing visible text on {page_data['name']}: {missing_visible}"
    assert not missing_source, f"FAIL: Missing HTML source text on {page_data['name']}: {missing_source}"
    assert not suspect_requests, (
        f"FAIL: Dynamic content/API requests found on {page_data['name']}:\n" +
        "\n".join(suspect_requests)
    )

    print(f"\nFINAL RESULT for {page_data['name']}: PASS")
    print("Page appears STATIC / SERVER-RENDERED.")