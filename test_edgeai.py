# test_edgeai.py
import pytest
import re
from playwright.sync_api import Page

BASE_URL = (
    "https://builders-upgrade.onsumaye.com/ecosystem-engagement/"
    "solution-hub/edge-ai-catalog/partner-showcase"
)


@pytest.fixture(scope="session")
def browser(playwright):
    browser = playwright.chromium.launch(headless=True)
    yield browser
    browser.close()


@pytest.fixture()
def page(browser):
    context = browser.new_context()
    page = context.new_page()
    yield page
    context.close()


def test_partner_facet_mismatch_when_asus_selected(page: Page):
    """
    PRECONDITION (MANUAL / ENV):
    Partner = 'AsusTek Computer Inc.' is already selected

    EXPECTED:
    - Product cards = 9
    - Sizing facet total != product count (BUG)
    """

    page.goto(BASE_URL, wait_until="domcontentloaded")
    page.wait_for_timeout(5000)

    cards = page.locator(
        '[data-test="solution-card"], .solution-card, .catalog-item'
    )
    product_count = cards.count()

    # Hard guard – prevents false automation failures
    if product_count == 0:
        pytest.skip(
            "Partner filter is not applied. "
            "This test validates facet mismatch AFTER AsusTek is selected."
        )

    # Expected from requirement
    assert product_count == 9, (
        f"Expected 9 products for AsusTek, found {product_count}"
    )

    # Collect sizing facet counts
    sizing_labels = page.locator("xpath=//label[contains(., '(')]")

    facet_total = 0
    for i in range(sizing_labels.count()):
        text = sizing_labels.nth(i).inner_text()
        m = re.search(r"\((\d+)\)", text)
        if m:
            facet_total += int(m.group(1))

    # This assertion exposes the bug
    assert facet_total == product_count, (
        f"BUG: Sizing facets show {facet_total} items "
        f"but only {product_count} products are displayed"
    )

    page.screenshot(path="facet_mismatch_evidence.png", full_page=True)
