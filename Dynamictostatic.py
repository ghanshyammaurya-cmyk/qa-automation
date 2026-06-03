from playwright.sync_api import sync_playwright
import re

URL = "https://builders-demo.onsumaye.com/communities/industrial"

# Keywords expected on the page
EXPECTED_TEXT = [
    "Industrial Builders",
    "Overview",
    "Solutions",
    "Training"
]

# Patterns that often indicate dynamic/API content loading
API_HINT_PATTERNS = [
    r"/api/",
    r"/graphql",
    r"/json",
    r"ajax",
    r"fetch",
    r"content",
    r"search"
]


def check_staticization():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(ignore_https_errors=True)
        page = context.new_page()

        api_requests = []
        failed_requests = []

        def capture_request(request):
            url = request.url.lower()
            resource_type = request.resource_type
            if resource_type in ["xhr", "fetch"]:
                api_requests.append({
                    "url": request.url,
                    "method": request.method,
                    "resource_type": resource_type
                })

        def capture_failed_request(request):
            failed_requests.append({
                "url": request.url,
                "method": request.method,
                "resource_type": request.resource_type,
                "failure": request.failure
            })

        page.on("request", capture_request)
        page.on("requestfailed", capture_failed_request)

        print(f"\nOpening page: {URL}")
        response = page.goto(URL, wait_until="domcontentloaded", timeout=90000)
        page.wait_for_load_state("networkidle", timeout=90000)

        # Page HTML after render
        rendered_html = page.content()

        # Raw source-like content via JS fetch in browser context
        raw_html = page.evaluate("() => document.documentElement.outerHTML")

        # Visible body text
        body_text = page.locator("body").inner_text()

        print("\n--- BASIC PAGE INFO ---")
        print("HTTP Status:", response.status if response else "No response")
        print("Page Title:", page.title())

        print("\n--- TEXT VALIDATION ---")
        all_keywords_found = True
        for text in EXPECTED_TEXT:
            found = text.lower() in body_text.lower()
            print(f"'{text}' found on page: {found}")
            if not found:
                all_keywords_found = False

        print("\n--- XHR/FETCH REQUESTS ---")
        if api_requests:
            print(f"Dynamic requests detected: {len(api_requests)}")
            for i, req in enumerate(api_requests, start=1):
                print(f"{i}. [{req['resource_type'].upper()}] {req['method']} {req['url']}")
        else:
            print("No XHR/FETCH requests detected.")

        print("\n--- RAW HTML / SOURCE CHECK ---")
        source_keyword_results = {}
        for text in EXPECTED_TEXT:
            found_in_source = text.lower() in raw_html.lower()
            source_keyword_results[text] = found_in_source
            print(f"'{text}' present in HTML source: {found_in_source}")

        print("\n--- API HINT CHECK IN REQUEST URLS ---")
        matched_api_hints = []
        for req in api_requests:
            for pattern in API_HINT_PATTERNS:
                if re.search(pattern, req["url"].lower()):
                    matched_api_hints.append(req["url"])
                    break

        if matched_api_hints:
            print("Possible dynamic/API endpoints found:")
            for url in matched_api_hints:
                print("-", url)
        else:
            print("No obvious API endpoint patterns found in XHR/FETCH calls.")

        print("\n--- FINAL ASSESSMENT ---")
        if not api_requests and all(source_keyword_results.values()):
            print("RESULT: Likely STATIC or server-rendered page.")
            print("Reason: Page content is available in source and no XHR/FETCH content-loading requests were detected.")
        elif api_requests and matched_api_hints:
            print("RESULT: Likely DYNAMIC page.")
            print("Reason: XHR/FETCH requests and API-like endpoints were detected.")
        else:
            print("RESULT: MIXED / NEEDS REVIEW.")
            print("Reason: Some content is present in source, but additional dynamic behavior may still exist.")

        if failed_requests:
            print("\n--- FAILED REQUESTS ---")
            for req in failed_requests:
                print(f"- {req['method']} {req['url']} | {req['resource_type']} | {req['failure']}")

        browser.close()


if __name__ == "__main__":
    check_staticization()