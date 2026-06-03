import pytest
from playwright.sync_api import Page, expect

BASE_URL = (
    "https://builders-upgrade.onsumaye.com/"
    "ecosystem-engagement/solution-hub/edge-ai-catalog/"
    "partner-showcase?type=system&pageNum=1"
)

def test_filter_combination(page: Page):
    # 1️⃣ Load page (slow env safe)
    page.goto(BASE_URL, wait_until="load", timeout=90000)
    page.wait_for_timeout(6000)

    # 2️⃣ Open Partner filter
    partner_filter = page.locator("text=Filter By Partners").first
    expect(partner_filter).to_be_visible(timeout=30000)
    partner_filter.click()
    page.wait_for_timeout(3000)

    # 3️⃣ Select ASUS partner
    partner_option = page.locator(
        "xpath=//*[normalize-space()='ASUSTek Computer Inc.']"
    ).first
    expect(partner_option).to_be_visible(timeout=30000)
    partner_option.click(force=True)

    # 4️⃣ Wait for backend response
    page.wait_for_load_state("networkidle", timeout=60000)
    page.wait_for_timeout(4000)

    # 5️⃣ Expand "AI Edge System Sizing" (FIXED)
    sizing_filter = page.locator("text=AI Edge System Sizing").first
    sizing_filter.scroll_into_view_if_needed()
    sizing_filter.click(force=True)   # <-- key fix
    page.wait_for_timeout(2000)

    # 6️⃣ Select "Scalable Performance"
    sizing_option = page.locator("text=Scalable Performance").first
    sizing_option.scroll_into_view_if_needed()
    sizing_option.click(force=True)

    # 7️⃣ Wait for results refresh
    page.wait_for_load_state("networkidle", timeout=60000)
    page.wait_for_timeout(5000)

    # 8️⃣ Validate URL params
    current_url = page.url
    assert "ecoP=" in current_url, "Partner filter param missing"
    assert "cid=" in current_url or "cp=" in current_url, (
        "Category filter param missing"
    )

    # 9️⃣ Validate products
    products = page.locator("article, .views-row")
    product_count = products.count()
    print(f"[INFO] Products after partner + category filter: {product_count}")

    if product_count == 0:
        pytest.fail(
            "DEFECT: Partner + Category filters applied but "
            "backend returned 0 products."
        )

    # 🔟 Evidence
    page.screenshot(
        path="partner_category_filter_result.png",
        full_page=True
    )
