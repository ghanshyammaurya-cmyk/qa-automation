"""
Save Playwright storage state after manual Intel SSO login.
Run once; ISBC_Project_Test.py will reuse auth.json to skip automated SSO.
"""

import os
from dotenv import load_dotenv
from playwright.sync_api import sync_playwright

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(BASE_DIR, ".env"))

BASE_URL = os.getenv("BASE_URL", "https://builders-qa.onsumaye.com/")
REGISTRATION_URL = os.getenv(
    "REGISTRATION_URL",
    "https://builders-qa.onsumaye.com/ecosystem-engagement/solutions-challenge/ai-edge/registration",
)
HT_USER = os.getenv("HT_USER", "")
HT_PASS = os.getenv("HT_PASS", "")
AUTH_PATH = os.path.join(BASE_DIR, "auth.json")


def save_login():
    print("=" * 62)
    print("  Save Intel SSO session → auth.json")
    print("=" * 62)
    print(f"  Hub: {REGISTRATION_URL}")
    print()
    print("  In the browser:")
    print("    1. ENGAGEMENT → Submit an Offering (or open hub URL below)")
    print("    2. Complete Intel SSO manually")
    print("    3. Land on the AI Edge registration page (see Projects sub-menu)")
    print("    4. Press ENTER here")
    print()

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        ctx_args = {}
        if HT_USER and HT_PASS:
            ctx_args["http_credentials"] = {"username": HT_USER, "password": HT_PASS}
        context = browser.new_context(**ctx_args)
        page = context.new_page()
        page.goto(REGISTRATION_URL.rstrip("/"), wait_until="domcontentloaded", timeout=60000)

        input("✅ After login on the registration hub, press ENTER...")

        context.storage_state(path=AUTH_PATH)
        print(f"🎉 Session saved to {AUTH_PATH}")
        browser.close()


if __name__ == "__main__":
    save_login()
