import pytest
from playwright.sync_api import Page, expect

BASE_URL = (
    "https://builders-upgrade.onsumaye.com/"
    "ecosystem-engagement/solution-hub/edge-ai-catalog/"
    "partner-showcase?type=system&pageNum=1"
)

def test_partner_filter_backend_consistency(page: Page):
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
    page.wait_for_timeout(5000)

    # 5️⃣ Validate filter param is applied
    current_url = page.url
    assert "ecoP=" in current_url, "Partner filter param not applied in URL"

    # 6️⃣ Count products (Drupal views)
    products = page.locator("article, .views-row")
    product_count = products.count()

    print(f"[INFO] Products returned for ASUS partner: {product_count}")

    # 7️⃣ Conditional validation (CORRECT QA LOGIC)
    if product_count == 0:
        pytest.fail(
            "DEFECT: Partner filter applied (ecoP param present) "
            "but backend returned 0 products. "
            "Expected ASUS products to be available."
        )

    # 8️⃣ Evidence
    page.screenshot(path="partner_filter_backend_defect.png", full_page=True)
