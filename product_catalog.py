import pytest
from playwright.sync_api import sync_playwright

BASE_URL = "https://builders.intel.com/ecosystem-engagement/solution-hub/edge-ai-catalog/partner-spotlight"

PARTNER_NAME = "AAEON"

HT_USERNAME = "admin"
HT_PASSWORD = "Intel@2025"


# ================================
# WAIT
# ================================
def wait_for_page(page):
    page.wait_for_load_state("domcontentloaded")
    page.wait_for_selector("input[placeholder='Search Products With Keywords']", timeout=10000)


# ================================
# GET ONLY PRODUCT TITLES (STRICT)
# ================================
def get_product_titles(page):
    cards = page.locator("a[href*='/edge-ai-catalog/'][href*='product']").all()

    titles = []
    for card in cards:
        try:
            t = card.inner_text().strip()

            # ✅ STRICT FILTER
            if (
                len(t) > 5
                and "Catalog" not in t
                and "Highlight" not in t
                and "Spotlight" not in t
                and "Details" not in t
            ):
                titles.append(t)

        except:
            continue

    return list(set(titles))


# ================================
# SEARCH
# ================================
def search_by_keyword(page, keyword):
    search = page.locator("input[placeholder='Search Products With Keywords']")
    search.fill(keyword)
    search.press("Enter")
    wait_for_page(page)


# ================================
# FILTER
# ================================
def filter_by_partner_dropdown(page, partner):
    page.locator("text=Filter By Partners").first.click()
    page.locator(f"text={partner}").first.click()
    wait_for_page(page)


# ================================
# TEST
# ================================
def test_search_vs_dropdown():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)

        context = browser.new_context(
            http_credentials={
                "username": HT_USERNAME,
                "password": HT_PASSWORD
            }
        )

        page = context.new_page()

        print("🚀 Opening page...")
        page.goto(BASE_URL)

        wait_for_page(page)

        # ---------- SEARCH ----------
        print("🔍 SEARCH")
        search_by_keyword(page, PARTNER_NAME)

        search_results = set(get_product_titles(page))
        print("Search Products:", search_results)

        # ---------- FILTER ----------
        print("\n📂 FILTER")
        page.goto(BASE_URL)  # ✅ CLEAN STATE (IMPORTANT FIX)

        wait_for_page(page)

        filter_by_partner_dropdown(page, PARTNER_NAME)

        dropdown_results = set(get_product_titles(page))
        print("Dropdown Products:", dropdown_results)

        # ---------- VALIDATION ----------
        print("\n⚖️ VALIDATION")

        missing_in_search = dropdown_results - search_results

        if missing_in_search:
            print("\n❌ REAL DEFECT FOUND")
            print("Products missing in search:", missing_in_search)

            pytest.fail(
                f"Search is missing partner products: {missing_in_search}"
            )

        print("✅ PASS: All dropdown products present in search")

        browser.close()