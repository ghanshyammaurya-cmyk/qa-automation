"""
ISBC Project Test — End-to-End (Create → Publish)
builders-qa.onsumaye.com
Based on exact UI screenshots provided.
"""

import sys
import os
import json
import re
import time
from dotenv import load_dotenv
from playwright.sync_api import sync_playwright, TimeoutError as PWTimeout

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE_DIR)
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass
load_dotenv(dotenv_path=os.path.join(BASE_DIR, ".env"))

BASE_URL  = os.getenv("BASE_URL")   # e.g. https://builders-qa.onsumaye.com
EMAIL     = os.getenv("EMAIL")
PASSWORD  = os.getenv("PASSWORD")
HT_USER   = os.getenv("HT_USER")
HT_PASS   = os.getenv("HT_PASS")
AUTH_PATH = os.path.join(BASE_DIR, "auth.json")
REGISTRATION_URL = os.getenv(
    "REGISTRATION_URL",
    "https://builders-qa.onsumaye.com/ecosystem-engagement/"
    "solutions-challenge/ai-edge/registration",
)

# ── Cookies (from your EditThisCookie export) ─────────────────
COOKIES_JSON = """
[
{
    "domain": ".builders-qa.onsumaye.com",
    "expirationDate": 1814944952.84474,
    "hostOnly": false,
    "httpOnly": false,
    "name": "_ga",
    "path": "/",
    "sameSite": "no_restriction",
    "secure": true,
    "session": false,
    "storeId": "0",
    "value": "GA1.1.890492541.1780384952",
    "id": 1
},
{
    "domain": ".builders-qa.onsumaye.com",
    "expirationDate": 1780569562,
    "hostOnly": false,
    "httpOnly": false,
    "name": "_gid",
    "path": "/",
    "sameSite": "no_restriction",
    "secure": true,
    "session": false,
    "storeId": "0",
    "value": "GA1.1.934475073.1780483162",
    "id": 2
},
{
    "domain": ".builders-qa.onsumaye.com",
    "expirationDate": 1812019324,
    "hostOnly": false,
    "httpOnly": false,
    "name": "utag_main",
    "path": "/",
    "sameSite": "unspecified",
    "secure": true,
    "session": false,
    "storeId": "0",
    "value": "ad_blocker:0$wa_ecid:21414667369712867406568179067214458563",
    "id": 3
},
{
    "domain": ".onsumaye.com",
    "expirationDate": 1803712953,
    "hostOnly": false,
    "httpOnly": false,
    "name": "_cc_id",
    "path": "/",
    "sameSite": "lax",
    "secure": false,
    "session": false,
    "storeId": "0",
    "value": "5461db51314bbb3976690bac238c060d",
    "id": 4
},
{
    "domain": ".onsumaye.com",
    "expirationDate": 1815046812.243073,
    "hostOnly": false,
    "httpOnly": false,
    "name": "_ga",
    "path": "/",
    "sameSite": "unspecified",
    "secure": false,
    "session": false,
    "storeId": "0",
    "value": "GA1.1.890492541.1780384952",
    "id": 5
},
{
    "domain": ".onsumaye.com",
    "expirationDate": 1815046816.595555,
    "hostOnly": false,
    "httpOnly": false,
    "name": "_ga_H2MRQMFXV5",
    "path": "/",
    "sameSite": "unspecified",
    "secure": false,
    "session": false,
    "storeId": "0",
    "value": "GS2.1.s1780486772$o6$g1$t1780486816$j16$l0$h0",
    "id": 6
},
{
    "domain": ".onsumaye.com",
    "expirationDate": 1815046816.587199,
    "hostOnly": false,
    "httpOnly": false,
    "name": "_ga_TRJS24038B",
    "path": "/",
    "sameSite": "unspecified",
    "secure": false,
    "session": false,
    "storeId": "0",
    "value": "GS2.1.s1780486766$o6$g1$t1780486816$j10$l0$h0",
    "id": 7
},
{
    "domain": ".onsumaye.com",
    "expirationDate": 1814080954,
    "hostOnly": false,
    "httpOnly": false,
    "name": "AMCV_AD2A1C8B53308E600A490D4D%40AdobeOrg",
    "path": "/",
    "sameSite": "no_restriction",
    "secure": true,
    "session": false,
    "storeId": "0",
    "value": "MCMID|21414667369712867406568179067214458563",
    "id": 8
},
{
    "domain": ".onsumaye.com",
    "expirationDate": 1811910849.668348,
    "hostOnly": false,
    "httpOnly": false,
    "name": "fpestid",
    "path": "/",
    "sameSite": "no_restriction",
    "secure": true,
    "session": false,
    "storeId": "0",
    "value": "Plw7QhndW8DxwkVQhz2FAFL2mdq624h7WqgQ6BA6Skm4Ma3N2FKEoKQhCy6RNODSopP65w",
    "id": 9
},
{
    "domain": ".onsumaye.com",
    "expirationDate": 1814611325,
    "hostOnly": false,
    "httpOnly": false,
    "name": "kndctr_AD2A1C8B53308E600A490D4D_AdobeOrg_identity",
    "path": "/",
    "sameSite": "no_restriction",
    "secure": true,
    "session": false,
    "storeId": "0",
    "value": "CiYyMTQxNDY2NzM2OTcxMjg2NzQwNjU2ODE3OTA2NzIxNDQ1ODU2M1IRCIfE8LToMxgBKgRJTkQxMAKgAcjOxrXoM7ABA_ABr_HN6Ogz",
    "id": 10
},
{
    "domain": "builders-qa.onsumaye.com",
    "hostOnly": true,
    "httpOnly": true,
    "name": "9b8e6586e381547382d1defd0fbb61b7",
    "path": "/",
    "sameSite": "unspecified",
    "secure": true,
    "session": true,
    "storeId": "0",
    "value": "4kdbi57s7sq4bggekh9bdm15q2",
    "id": 11
},
{
    "domain": "builders-qa.onsumaye.com",
    "hostOnly": true,
    "httpOnly": true,
    "name": "authCode",
    "path": "/",
    "sameSite": "lax",
    "secure": true,
    "session": true,
    "storeId": "0",
    "value": "aXNic3NvdGVzdDEwMUBtYWlsaW5hdG9yLmNvbQ",
    "id": 12
},
{
    "domain": "builders-qa.onsumaye.com",
    "expirationDate": 1781091619.09443,
    "hostOnly": true,
    "httpOnly": false,
    "name": "AWSALBAPP-0",
    "path": "/",
    "sameSite": "no_restriction",
    "secure": true,
    "session": false,
    "storeId": "0",
    "value": "_remove_",
    "id": 13
},
{
    "domain": "builders-qa.onsumaye.com",
    "expirationDate": 1781091619.094685,
    "hostOnly": true,
    "httpOnly": false,
    "name": "AWSALBAPP-1",
    "path": "/",
    "sameSite": "no_restriction",
    "secure": true,
    "session": false,
    "storeId": "0",
    "value": "_remove_",
    "id": 14
},
{
    "domain": "builders-qa.onsumaye.com",
    "expirationDate": 1781091619.094843,
    "hostOnly": true,
    "httpOnly": false,
    "name": "AWSALBAPP-2",
    "path": "/",
    "sameSite": "no_restriction",
    "secure": true,
    "session": false,
    "storeId": "0",
    "value": "_remove_",
    "id": 15
},
{
    "domain": "builders-qa.onsumaye.com",
    "expirationDate": 1781091619.094979,
    "hostOnly": true,
    "httpOnly": false,
    "name": "AWSALBAPP-3",
    "path": "/",
    "sameSite": "no_restriction",
    "secure": true,
    "session": false,
    "storeId": "0",
    "value": "_remove_",
    "id": 16
},
{
    "domain": "builders-qa.onsumaye.com",
    "hostOnly": true,
    "httpOnly": false,
    "name": "joomla_logged_in",
    "path": "/",
    "sameSite": "unspecified",
    "secure": true,
    "session": true,
    "storeId": "0",
    "value": "1",
    "id": 17
},
{
    "domain": "builders-qa.onsumaye.com",
    "hostOnly": true,
    "httpOnly": true,
    "name": "joomla_user_state",
    "path": "/",
    "sameSite": "unspecified",
    "secure": true,
    "session": true,
    "storeId": "0",
    "value": "logged_in",
    "id": 18
},
{
    "domain": "builders-qa.onsumaye.com",
    "hostOnly": true,
    "httpOnly": false,
    "name": "logged_in",
    "path": "/",
    "sameSite": "unspecified",
    "secure": true,
    "session": true,
    "storeId": "0",
    "value": "yes",
    "id": 19
},
{
    "domain": "builders-qa.onsumaye.com",
    "hostOnly": true,
    "httpOnly": false,
    "name": "logged_in_name",
    "path": "/",
    "sameSite": "unspecified",
    "secure": true,
    "session": true,
    "storeId": "0",
    "value": "ISBSSO100%20Test",
    "id": 20
},
{
    "domain": "builders-qa.onsumaye.com",
    "expirationDate": 1780573216.404563,
    "hostOnly": true,
    "httpOnly": false,
    "name": "userData",
    "path": "/",
    "sameSite": "unspecified",
    "secure": false,
    "session": false,
    "storeId": "0",
    "value": "%7B%22id%22%3A54120%2C%22username%22%3A%22isbssotest101%40mailinator.com%22%2C%22email%22%3A%22isbssotest101%40mailinator.com%22%2C%22name%22%3A%22ISBSSO100%20Test%22%2C%22block%22%3A0%7D",
    "id": 21
}
]
"""

# ── Dummy test data ───────────────────────────────────────────
import random, string
_uid = ''.join(random.choices(string.digits, k=4))

PROJECT_NAME     = f"AI Edge Analytics Platform {_uid}"
PROJECT_DESC     = "This platform delivers real-time AI inferencing at the edge for industrial IoT."
BUSINESS_PROBLEM = ("Manufacturing lacks real-time visibility into equipment health, "
                    "causing unplanned downtime and costly production losses.")
SOLUTION_FEATURES= ("Our app deploys AI models on Intel-powered edge devices. "
                    "Key features: (1) Real-time anomaly detection, "
                    "(2) Predictive maintenance alerts, "
                    "(3) OPC-UA integration, "
                    "(4) Cloud dashboard for fleet management.")
AI_WORKLOAD_DESC = ("The application performs computer vision and Generative AI workloads "
                    "using OpenVINO-optimized models for real-time object detection.")
SUCCESS_STORY    = ("An automotive OEM deployed our solution across 12 production lines, "
                    "reducing unplanned downtime by 34% and saving $2.1M annually.")
SUPPORT_DESC     = ("We provide 24/7 enterprise support via dedicated Slack channels, "
                    "a self-service knowledge base, and an assigned customer success manager.")
ADDITIONAL_INFO  = ("Our platform is built on Intel OpenVINO and integrates with MES and "
                    "SCADA systems. Supports Intel Core Ultra and Xeon processors.")
STEP_TITLE       = "Deploy the Edge AI Runtime"
STEP_DESC        = ("Install Intel OpenVINO runtime. Configure the inference pipeline "
                    "using the provided Docker Compose templates. Connect to OPC-UA source.")
USE_CASES_TEXT    = ("Predictive maintenance, computer vision quality inspection, "
                     "and real-time anomaly detection on the factory floor.")
OPEN_SOFTWARE_TEXT = (
    "Our application uses OpenVINO Toolkit, oneAPI, Intel Distribution of OpenVINO, "
    "Open Edge Platform, and Intel OpenDL Streamer — ingredients from the "
    "Open Software Platform for edge AI inference and deployment."
)
Q7_NO_REASON      = ("Pilot deployments with select customers; full commercial "
                     "availability planned in Q3 2026.")
Q10_YES_PARTNERS  = ("Contracted distribution agreements with TD SYNNEX and "
                     "Ingram Micro in North America and Europe.")
DIST_PARTNER_TEXT = Q10_YES_PARTNERS
ODM_TEXT         = (
    "Dell Technologies, Advantech, Kontron, and Super Micro Computer."
)
Q9_VERIFY_MARKER = "Dell Technologies"


# ─────────────────────────────────────────────────────────────
#  UTILITIES
# ─────────────────────────────────────────────────────────────
def parse_cookies(raw: str) -> list:
    try:
        items = json.loads(raw.strip())
    except Exception:
        return []
    mp = {"no_restriction": "None", "lax": "Lax", "strict": "Strict", "unspecified": "None"}
    out = []
    for c in items:
        ck = {
            "name":     c.get("name", ""),
            "value":    c.get("value", ""),
            "domain":   c.get("domain", ""),
            "path":     c.get("path", "/"),
            "secure":   bool(c.get("secure", False)),
            "httpOnly": bool(c.get("httpOnly", False)),
            "sameSite": mp.get(str(c.get("sameSite", "")).lower(), "None"),
        }
        if "expirationDate" in c:
            ck["expires"] = int(c["expirationDate"])
        out.append(ck)
    return out


def sep(n, title):
    print(f"\n{'─'*62}\n  STEP {n} │ {title}\n{'─'*62}")


def shot(page, name):
    try:
        page.screenshot(path=f"{name}.png")
        print(f"  [📷] {name}.png")
    except Exception:
        pass


def _visible_locators(page, selector):
    """Yield locators for every visible match (avoids hidden duplicate nodes)."""
    try:
        for el in page.locator(selector).all():
            try:
                if el.is_visible():
                    yield el
            except Exception:
                continue
    except Exception:
        pass


def try_click(page, selectors, label, timeout=12000):
    """Try each selector and click the first visible match."""
    if isinstance(selectors, str):
        selectors = [selectors]
    deadline = time.time() + (timeout / 1000)
    while time.time() < deadline:
        for sel in selectors:
            for el in _visible_locators(page, sel):
                try:
                    el.scroll_into_view_if_needed()
                    time.sleep(0.2)
                    el.click(timeout=5000)
                    print(f"  [OK] Clicked '{label}'")
                    return True
                except Exception:
                    try:
                        el.click(force=True, timeout=3000)
                        print(f"  [OK] Clicked '{label}' (force)")
                        return True
                    except Exception:
                        continue
        time.sleep(0.4)
    print(f"  [WARN] Could not click '{label}' — dumping buttons:")
    try:
        for b in page.query_selector_all("button")[:20]:
            try:
                t = b.inner_text().strip()
                if t:
                    print(f"    • '{t}'")
            except Exception:
                pass
    except Exception:
        pass
    shot(page, f"dbg_{label[:25].replace(' ','_')}")
    return False


def try_fill(page, selectors, value, label, timeout=10000, silent=False):
    """Fill a plain text input or textarea."""
    if isinstance(selectors, str):
        selectors = [selectors]
    deadline = time.time() + (timeout / 1000)
    while time.time() < deadline:
        for sel in selectors:
            for el in _visible_locators(page, sel):
                try:
                    el.scroll_into_view_if_needed()
                    el.click()
                    el.fill(value)
                    print(f"  [OK] Filled '{label}'")
                    return True
                except Exception:
                    continue
        time.sleep(0.3)
    if not silent:
        print(f"  [WARN] Could not fill '{label}'")
    return False


def fill_rich_text(page, container_sel, value, label, timeout=10000):
    """
    Fill a rich-text (contenteditable) editor.
    From screenshots Q3/Q4/Q6 etc. use a rich-text editor with a toolbar.
    """
    for sel in [
        f"{container_sel} .ql-editor",
        f"{container_sel} [contenteditable='true']",
        f"{container_sel} .tox-edit-area__iframe",
        f"{container_sel} textarea",
        f"{container_sel} input[type='text']",
    ]:
        try:
            el = page.wait_for_selector(sel, timeout=timeout, state="visible")
            el.scroll_into_view_if_needed()
            el.click()
            # Clear and type
            el.fill("") if sel.endswith("textarea") or "input" in sel else None
            page.keyboard.press("Control+a")
            page.keyboard.type(value)
            print(f"  [OK] Rich-text filled '{label}'")
            return True
        except Exception:
            continue
    # Fallback: just find any visible contenteditable near the label
    try:
        page.evaluate(f"""
            var editors = document.querySelectorAll('[contenteditable="true"]');
            if(editors.length > 0) {{
                editors[editors.length-1].focus();
                document.execCommand('selectAll', false, null);
                document.execCommand('insertText', false, {json.dumps(value)});
            }}
        """)
        print(f"  [OK] Rich-text filled '{label}' via JS")
        return True
    except Exception as e:
        print(f"  [WARN] Could not fill rich-text '{label}': {e}")
    return False


def select_from_dropdown(page, dropdown_trigger_sels, option_text, label, timeout=10000):
    """
    Click a custom multi-select dropdown to open it,
    then click the matching option.
    From screenshots Q2/Q3/Q4/Q8 use "Select from this list" style dropdowns.
    """
    if isinstance(dropdown_trigger_sels, str):
        dropdown_trigger_sels = [dropdown_trigger_sels]

    for trig in dropdown_trigger_sels:
        for el in _visible_locators(page, trig):
            try:
                el.scroll_into_view_if_needed()
                el.click()
                time.sleep(0.7)
                opt_patterns = [
                    f"[role='option']:has-text('{option_text}')",
                    f"li:has-text('{option_text}')",
                    f"div[class*='option']:has-text('{option_text}')",
                    f"span:has-text('{option_text}')",
                    f"text={option_text}",
                ]
                if len(option_text) > 4:
                    short = option_text.split()[-1] if " " in option_text else option_text[:6]
                    opt_patterns.append(f"[role='option']:has-text('{short}')")
                for opt_sel in opt_patterns:
                    for opt in _visible_locators(page, opt_sel):
                        try:
                            opt.scroll_into_view_if_needed()
                            opt.click()
                            print(f"  [OK] Selected '{option_text}' in '{label}'")
                            time.sleep(0.3)
                            page.keyboard.press("Escape")
                            time.sleep(0.2)
                            return True
                        except Exception:
                            continue
                try:
                    page.get_by_text(option_text, exact=False).last.click(timeout=3000)
                    print(f"  [OK] Selected '{option_text}' in '{label}' (text match)")
                    page.keyboard.press("Escape")
                    return True
                except Exception:
                    pass
                page.keyboard.press("Escape")
            except Exception:
                continue
    print(f"  [WARN] Could not select '{option_text}' in '{label}'")
    return False


def wait_for_section_view(page, section_name, timeout_sec=15):
    """Wait until the named section heading is visible in the form body."""
    markers = [section_name, "Overall Progress"]
    for _ in range(timeout_sec):
        for m in markers:
            try:
                if page.locator(f"text={m}").first.is_visible():
                    return True
            except Exception:
                pass
        time.sleep(1)
    return False


def click_section_edit(page, section_name=""):
    """Click the visible Edit control for the active intake section."""
    if section_name:
        wait_for_section_view(page, section_name)
        time.sleep(0.8)
    sels = [
        "xpath=//*[contains(.,'Overall Progress')]/following::button[contains(.,'Edit') and not(contains(.,'Project'))][1]",
        "xpath=//*[contains(.,'Overall Progress')]/following::a[contains(.,'Edit') and not(contains(.,'Project'))][1]",
        "xpath=//*[contains(.,'Please do not post any confidential')]/following::button[contains(.,'Edit')][1]",
        "xpath=//*[contains(.,'Please do not post any confidential')]/following::a[contains(.,'Edit')][1]",
        "button:has-text('Edit'):not(:has-text('Project'))",
        "a:has-text('Edit'):not(:has-text('Project'))",
        "[title='Edit']",
        "[aria-label='Edit']",
    ]
    return try_click(page, sels, f"Edit ({section_name or 'section'})", timeout=15000)


def fill_plain_text_only(page, question_fragment, value, label):
    """Fill a plain input/textarea only (no rich-text editor)."""
    sels = [
        f"xpath=//*[contains(.,'{question_fragment}')]/following::textarea[not(@disabled)][1]",
        f"xpath=//*[contains(.,'{question_fragment}')]/following::input[@type='text'][not(@disabled)][1]",
        f"xpath=//*[contains(.,'{question_fragment}')]/ancestor::div[contains(@class,'question') or contains(@class,'field') or contains(@class,'form-group')][1]//textarea[1]",
        f"xpath=//*[contains(.,'{question_fragment}')]/ancestor::div[contains(@class,'question') or contains(@class,'field') or contains(@class,'form-group')][1]//input[@type='text'][1]",
        f"xpath=//label[contains(.,'{question_fragment}')]/following::textarea[1]",
        f"xpath=//label[contains(.,'{question_fragment}')]/following::input[@type='text'][1]",
    ]
    return try_fill(page, sels, value, label)


def fill_rich_text_near_question(page, question_fragment, value, label):
    """Fill the rich-text / Quill editor that belongs to a specific question."""
    try:
        page.locator(f"text={question_fragment}").first.scroll_into_view_if_needed()
    except Exception:
        pass
    time.sleep(0.4)

    block = _question_block_xpath(question_fragment)
    editor_sels = [
        f"xpath={block}//div[contains(@class,'ql-editor')]",
        f"xpath={block}//div[contains(@class,'ql-container')]//*[@contenteditable='true']",
        f"xpath=//*[contains(.,'{question_fragment}')]/following::div[contains(@class,'ql-editor')][1]",
        f"xpath=//*[contains(.,'{question_fragment}')]/following::div[contains(@class,'ql-container')][1]//*[@contenteditable='true']",
        f"xpath=//*[contains(.,'{question_fragment}')]/following::*[@contenteditable='true'][1]",
    ]
    for sel in editor_sels:
        for el in _visible_locators(page, sel):
            try:
                el.scroll_into_view_if_needed()
                el.click()
                time.sleep(0.2)
                page.keyboard.press("Control+a")
                page.keyboard.type(value)
                page.keyboard.press("Tab")
                print(f"  [OK] Filled '{label}' (rich text editor)")
                time.sleep(0.6)
                return True
            except Exception:
                continue

    try:
        filled = page.evaluate(
            """([frag, text]) => {
                const anchor = [...document.querySelectorAll('*')].find(
                    n => n.textContent && n.textContent.includes(frag)
                );
                if (!anchor) return false;
                let root = anchor;
                for (let i = 0; i < 10 && root; i++) {
                    const ed = root.querySelector('.ql-editor, [contenteditable="true"]');
                    if (ed) {
                        ed.focus();
                        ed.textContent = text;
                        ed.dispatchEvent(new Event('input', { bubbles: true }));
                        ed.dispatchEvent(new Event('change', { bubbles: true }));
                        ed.dispatchEvent(new Event('blur', { bubbles: true }));
                        return true;
                    }
                    root = root.parentElement;
                }
                return false;
            }""",
            [question_fragment, value],
        )
        if filled:
            print(f"  [OK] Filled '{label}' (rich text editor via JS)")
            time.sleep(0.6)
            return True
    except Exception:
        pass

    print(f"  [WARN] Could not fill '{label}' in rich text editor")
    return False


# JS helper — locate the input between Q9 and Q10 headings in document order.
_JS_FIND_Q9_FIELD = """
() => {
    const isQHeading = (t, n) => t && new RegExp('^Q' + n + '\\\\s*:', 'i').test(t.trim()) && t.length < 400;
    const isInput = (el) => el.matches(
        'textarea:not([disabled]), input[type="text"]:not([disabled]), ' +
        '.ql-editor, [contenteditable="true"]'
    ) && el.offsetParent !== null;

    let zone = 'before';
    const q9fields = [];
    const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_ELEMENT);
    while (walker.nextNode()) {
        const el = walker.currentNode;
        const t = (el.innerText || '').trim();
        if (isQHeading(t, 9)) { zone = 'q9'; continue; }
        if (isQHeading(t, 10)) { zone = 'after'; continue; }
        if (zone === 'q9' && isInput(el)) q9fields.push(el);
    }
    if (q9fields.length) return q9fields[0];

    // Fallback: title line contains ODM question text
    const title = [...document.querySelectorAll('h4,h5,h6,label,span,strong,p,div')].find(el => {
        const t = (el.innerText || '').trim();
        return (/^Q9\\s*:/i.test(t) || t.startsWith('Q9'))
            && /ODM/i.test(t) && /OEM/i.test(t) && t.length < 400;
    });
    if (!title) return null;
    let node = title;
    for (let i = 0; i < 12 && node; i++) {
        const inp = [...node.querySelectorAll(
            'textarea, input[type="text"], .ql-editor, [contenteditable="true"]'
        )].find(isInput);
        if (inp) return inp;
        node = node.parentElement;
    }
    return null;
}
"""

_JS_Q9_FIELD_VALUE = f"""
() => {{
    const find = {_JS_FIND_Q9_FIELD};
    const field = find();
    if (!field) return '';
    return (field.value || field.innerText || field.textContent || '').trim();
}}
"""

_JS_FILL_Q9_FIELD = f"""
(text) => {{
    const find = {_JS_FIND_Q9_FIELD};
    const field = find();
    if (!field) return {{ ok: false, reason: 'field not found' }};

    field.scrollIntoView({{ block: 'center' }});
    field.focus();

    const fire = (el) => {{
        el.dispatchEvent(new Event('input', {{ bubbles: true }}));
        el.dispatchEvent(new Event('change', {{ bubbles: true }}));
        el.dispatchEvent(new Event('blur', {{ bubbles: true }}));
    }};

    if (field.tagName === 'TEXTAREA' || field.tagName === 'INPUT') {{
        const proto = field.tagName === 'TEXTAREA'
            ? window.HTMLTextAreaElement.prototype
            : window.HTMLInputElement.prototype;
        const setter = Object.getOwnPropertyDescriptor(proto, 'value');
        if (setter && setter.set) setter.set.call(field, text);
        else field.value = text;
        fire(field);
    }} else {{
        field.innerHTML = '';
        field.textContent = text;
        fire(field);
    }}

    const val = (field.value || field.innerText || field.textContent || '').trim();
    return {{ ok: val.length > 3, len: val.length, preview: val.substring(0, 60) }};
}}
"""


def _q9_field_has_content(page, min_len=5):
    """True only when the Q9-specific field (between Q9 and Q10) has text."""
    try:
        val = page.evaluate(_JS_Q9_FIELD_VALUE)
        if not val or len(val.strip()) < min_len:
            return False
        return Q9_VERIFY_MARKER.lower() in val.lower()
    except Exception:
        return False


def fill_details_q9_odm_oem(page, value=None, label="Q9: Hardware ODMs/OEMs"):
    """Fill Details Q9 text field — targets input strictly between Q9 and Q10 labels."""
    if value is None:
        value = ODM_TEXT

    for marker in ("Q9:", "Which Hardware ODMs/OEMs", "qualified to operate"):
        try:
            page.locator(f"text={marker}").first.scroll_into_view_if_needed()
            time.sleep(0.6)
            break
        except Exception:
            continue

    # Playwright: first textbox after the Q9 heading
    try:
        q9_title = page.locator(
            "xpath=//*[starts-with(normalize-space(),'Q9') and contains(.,'ODM')]"
        ).first
        if q9_title.is_visible():
            q9_title.scroll_into_view_if_needed()
            for candidate in (
                q9_title.locator("xpath=following::textarea[not(@disabled)][1]"),
                q9_title.locator("xpath=following::input[@type='text'][not(@disabled)][1]"),
                q9_title.locator("xpath=following::div[contains(@class,'ql-editor')][1]"),
            ):
                try:
                    if candidate.count() and candidate.first.is_visible():
                        el = candidate.first
                        el.scroll_into_view_if_needed()
                        el.click()
                        tag = el.evaluate("e => e.tagName.toLowerCase()")
                        if tag in ("textarea", "input"):
                            el.fill(value)
                        else:
                            el.click()
                            page.keyboard.press("Control+a")
                            page.keyboard.type(value)
                        page.keyboard.press("Tab")
                        time.sleep(0.8)
                        if _q9_field_has_content(page):
                            print(f"  [OK] Filled '{label}'")
                            return True
                except Exception:
                    continue
    except Exception:
        pass

    try:
        result = page.evaluate(_JS_FILL_Q9_FIELD, value)
        time.sleep(0.8)
        if result and result.get("ok") and _q9_field_has_content(page):
            print(f"  [OK] Filled '{label}' (JS: {result.get('preview', '')[:50]})")
            return True
        if result:
            print(f"  [INFO] Q9 JS fill result: {result}")
    except Exception as exc:
        print(f"  [INFO] Q9 JS fill error: {exc}")

    print(f"  [WARN] Could not fill '{label}'")
    return False


def ensure_details_q9_filled(page, max_attempts=5):
    """Always fill Q9 and verify the Q9-specific field contains dummy ODM/OEM data."""
    for attempt in range(1, max_attempts + 1):
        print(f"  [INFO] Q9 fill attempt {attempt}/{max_attempts}...")
        try:
            page.locator("text=Which Hardware ODMs").first.scroll_into_view_if_needed()
        except Exception:
            pass
        time.sleep(0.4)
        fill_details_q9_odm_oem(page)
        time.sleep(1)
        if _q9_field_has_content(page):
            print("  [OK] Q9 verified — ODM/OEM data saved in Q9 field")
            return True
    print("  [WARN] Q9 still blank after retries")
    shot(page, "dbg_Q9_blank")
    return False


def fill_near_question(page, question_fragment, value, label, multiline=True):
    """Fill text/textarea or rich-text field that follows a question label."""
    tag = "textarea" if multiline else "input[@type='text']"
    plain_sels = [
        f"xpath=//*[contains(.,'{question_fragment}')]/following::{tag}[not(@disabled)][1]",
        f"xpath=//*[contains(.,'{question_fragment}')]/ancestor::div[contains(@class,'question') or contains(@class,'field') or contains(@class,'form-group')][1]//{tag}[1]",
        f"xpath=//label[contains(.,'{question_fragment}')]/following::{tag}[1]",
    ]
    rich_sels = [
        f"xpath=//*[contains(.,'{question_fragment}')]/following::div[contains(@class,'ql-container')]//div[contains(@class,'ql-editor')]",
        f"xpath=//*[contains(.,'{question_fragment}')]/following::*[@contenteditable='true'][1]",
    ]
    if try_fill(page, plain_sels, value, label, silent=True):
        return True
    for sel in rich_sels:
        for el in _visible_locators(page, sel):
            try:
                el.scroll_into_view_if_needed()
                el.click()
                page.keyboard.press("Control+a")
                page.keyboard.type(value)
                print(f"  [OK] Filled '{label}'")
                return True
            except Exception:
                continue
    print(f"  [WARN] Could not fill '{label}'")
    return False


# Alternate labels seen in QA dropdown options
_DROPDOWN_ALIASES = {
    "GPU": ["GPU", "Graphics Processing Unit (GPU)"],
    "Europe": ["Europe", "Europe, Middle East and Africa", "EMEA"],
    "Intel® Core™ Ultra Processors": [
        "Ultra Processors", "Core Ultra", "Intel Core Ultra", "Intel® Core™ Ultra",
        "Intel® Core™ Ultra Processors", "Intel Core Ultra Processors",
    ],
    "Intel® Xeon® Processors": [
        "Xeon", "Intel Xeon", "Intel® Xeon®", "Intel Xeon Processors",
        "Intel® Xeon® Processors",
    ],
}


def _dropdown_triggers(page, question_fragment):
    return [
        f"xpath=//*[contains(.,'{question_fragment}')]/ancestor::div[contains(@class,'question') or contains(@class,'field') or contains(@class,'form-group')][1]//div[contains(@class,'select') or contains(@class,'multiselect') or contains(@class,'v-select')][1]",
        f"xpath=//*[contains(.,'{question_fragment}')]/following::div[contains(@class,'select') or contains(@class,'multiselect') or contains(@class,'v-select')][1]",
        f"xpath=//*[contains(.,'{question_fragment}')]/following::select[1]",
    ]


def select_multi_near_question(page, question_fragment, options, label):
    """Select multiple values from dropdown near a question (Details Q2/Q3/Q4/Q8)."""
    triggers = _dropdown_triggers(page, question_fragment)
    ok = False
    for opt in options:
        variants = _DROPDOWN_ALIASES.get(opt, [opt])
        for variant in variants:
            if select_from_dropdown(page, triggers, variant, f"{label}: {opt}"):
                ok = True
                break
        time.sleep(0.4)
    return ok


def _question_block_xpath(question_fragment):
    q = question_fragment.replace("'", "\\'")
    return (
        f"//*[contains(.,'{q}')]/ancestor::div"
        f"[contains(@class,'question') or contains(@class,'field') "
        f"or contains(@class,'form-group')][1]"
    )


def _open_multiselect_panel(page, question_fragment):
    """Open 'Select from the list below' checkbox panel for a question."""
    block = _question_block_xpath(question_fragment)
    open_sels = [
        f"xpath={block}//*[contains(.,'Select from')]",
        f"xpath={block}//div[contains(@class,'multiselect') or contains(@class,'v-select')]",
        f"xpath=//*[contains(.,'{question_fragment}')]/following::*[contains(.,'Select from')][1]",
        f"xpath=//*[contains(.,'{question_fragment}')]/following::div[contains(@class,'multiselect') or contains(@class,'v-select')][1]",
    ]
    for sel in open_sels:
        for el in _visible_locators(page, sel):
            try:
                el.scroll_into_view_if_needed()
                el.click()
                time.sleep(0.8)
                return True
            except Exception:
                continue
    return False


def _click_checkbox_option(page, question_fragment, opt):
    """Click a visible checkbox option (inside open panel or inline list)."""
    block = _question_block_xpath(question_fragment)
    sels = [
        f"xpath=//div[contains(@class,'multiselect') and contains(@class,'open')]//label[contains(.,'{opt}')]",
        f"xpath=//*[@role='listbox' or @role='menu']//*[contains(.,'{opt}')]",
        f"xpath={block}//label[contains(.,'{opt}')]",
        f"xpath={block}//input[@type='checkbox'][following-sibling::*[contains(.,'{opt}')] or parent::label[contains(.,'{opt}')]]",
        f"xpath=//label[contains(.,'{opt}')]//input[@type='checkbox']",
        f"label:has-text('{opt}')",
    ]
    for sel in sels:
        for el in _visible_locators(page, sel):
            try:
                el.scroll_into_view_if_needed()
                cb = el.locator("input[type='checkbox']").first
                if cb.count() > 0:
                    try:
                        if not cb.is_checked():
                            cb.click()
                        else:
                            print(f"  [INFO] '{opt}' already checked")
                    except Exception:
                        el.click()
                else:
                    el.click()
                return True
            except Exception:
                try:
                    el.click(force=True)
                    return True
                except Exception:
                    continue
    return False


def check_multiselect_checkboxes(page, question_fragment, options, label="",
                                 max_count=3, select_all=False):
    """
    Open multiselect list and check checkbox options.
    Overview Q5: up to 3 industries. Details Q2: all workload locations.
    """
    try:
        page.locator(f"text={question_fragment}").first.scroll_into_view_if_needed()
    except Exception:
        pass
    time.sleep(0.4)

    _open_multiselect_panel(page, question_fragment)

    checked = 0
    limit = len(options) if select_all else max_count
    for opt in options:
        if checked >= limit:
            break
        if not _open_multiselect_panel(page, question_fragment) and checked > 0:
            time.sleep(0.5)
        if _click_checkbox_option(page, question_fragment, opt):
            checked += 1
            print(f"  [OK] Checked '{opt}' for {label or question_fragment}")
            time.sleep(0.35)
        else:
            print(f"  [WARN] Could not check '{opt}' for {label or question_fragment}")

    try:
        page.locator("text=Overall Progress").first.click()
    except Exception:
        page.keyboard.press("Escape")
    time.sleep(0.5)
    return checked > 0


def check_checkbox_options(page, question_fragment, options, max_count=3, label=""):
    """Alias — check multiselect checkbox options near a question."""
    return check_multiselect_checkboxes(
        page, question_fragment, options, label=label, max_count=max_count,
    )


def wait_for_field_valid(page, question_fragment, timeout_sec=12):
    """Wait until a required field shows valid state (green check, no red error)."""
    block_xpath = _question_block_xpath(question_fragment)
    for _ in range(timeout_sec):
        try:
            block = page.locator(f"xpath={block_xpath}")
            if block.count() == 0:
                time.sleep(1)
                continue
            if block.locator("[class*='error'], [class*='invalid'], [class*='warning-icon']").count() > 0:
                time.sleep(1)
                continue
            if block.locator("[class*='success'], [class*='valid'], [class*='check']").count() > 0:
                return True
            # No red icon visible near the question row
            return True
        except Exception:
            pass
        time.sleep(1)
    return False


def wait_for_sidebar_green(page, section_name, timeout_sec=25):
    """Wait until sidebar section shows green completion check."""
    for _ in range(timeout_sec):
        try:
            row = page.locator(
                f"xpath=//li[contains(.,'{section_name}')]"
                f" | //a[contains(.,'{section_name}')]/ancestor::li[1]"
            ).first
            if row.count() == 0:
                time.sleep(1)
                continue
            html = (row.get_attribute("class") or "") + row.inner_html()
            html_l = html.lower()
            has_green = any(k in html_l for k in (
                "complete", "success", "check", "valid", "done", "green",
            ))
            has_red = any(k in html_l for k in (
                "error", "invalid", "warning", "incomplete", "required-error",
            ))
            icon_green = row.locator(
                "[class*='check'], [class*='success'], [class*='complete'], svg"
            ).count() > 0
            if has_green and not has_red:
                print(f"  [OK] Sidebar '{section_name}' — green check visible")
                return True
            if icon_green and not has_red:
                print(f"  [OK] Sidebar '{section_name}' — section complete")
                return True
        except Exception:
            pass
        time.sleep(1)
    print(f"  [INFO] Sidebar '{section_name}' green check not confirmed yet")
    return False


def click_radio_yn(page, q_text_fragment, answer, label):
    """Select Yes or No radio button for a question."""
    selectors = [
        f"xpath=//*[contains(.,'{q_text_fragment}')]/ancestor::div[contains(@class,'question') or contains(@class,'field') or contains(@class,'form-group')][1]//label[normalize-space()='{answer}']",
        f"xpath=//*[contains(.,'{q_text_fragment}')]/following::label[normalize-space()='{answer}'][1]",
        f"xpath=//*[contains(.,'{q_text_fragment}')]/following::span[normalize-space()='{answer}'][1]",
        f"xpath=//*[contains(.,'{q_text_fragment}')]/following::input[@type='radio'][@value='{answer}'][1]",
        f"xpath=//*[contains(.,'{q_text_fragment}')]/following::input[@type='radio'][following-sibling::*[contains(.,'{answer}')]][1]",
        f"xpath=//*[contains(.,'{q_text_fragment}')]/following::*[contains(@class,'radio')][contains(.,'{answer}')][1]",
    ]
    for sel in selectors:
        for el in _visible_locators(page, sel):
            try:
                el.scroll_into_view_if_needed()
                el.click()
                print(f"  [OK] Radio '{answer}' for '{label}'")
                time.sleep(0.4)
                return True
            except Exception:
                try:
                    el.click(force=True)
                    print(f"  [OK] Radio '{answer}' for '{label}' (force)")
                    time.sleep(0.4)
                    return True
                except Exception:
                    continue
    print(f"  [WARN] Could not click radio '{answer}' for '{label}'")
    return False


def fill_conditional_after_radio(page, question_fragment, value, label):
    """Fill text field that appears after a Yes/No radio selection."""
    time.sleep(0.8)
    sels = [
        f"xpath=//*[contains(.,'{question_fragment}')]/following::textarea[not(@disabled)][1]",
        f"xpath=//*[contains(.,'{question_fragment}')]/following::input[@type='text'][not(@disabled)][1]",
        "xpath=(//textarea[not(@disabled)])[last()]",
        "xpath=(//input[@type='text' and not(@disabled)])[last()]",
    ]
    return try_fill(page, sels, value, label)


def click_sidebar_tab(page, tab_name):
    return try_click(page, [
        f"xpath=//li[.//*[normalize-space()='{tab_name}']]//a",
        f"xpath=//span[normalize-space()='{tab_name}']/ancestor::a[1]",
        f"xpath=//a[normalize-space()='{tab_name}']",
        f"text={tab_name}",
    ], f"{tab_name} sidebar tab", timeout=10000)


def click_done(page):
    """Exit section edit mode (Done button top-right of active section)."""
    return try_click(page, [
        "xpath=//*[contains(.,'Overall Progress')]/following::button[normalize-space()='Done'][1]",
        "xpath=//button[normalize-space()='Done']",
        "button:has-text('Done')",
    ], "Done", timeout=12000)


def click_continue(page):
    return try_click(page, [
        "xpath=//*[contains(.,'Overall Progress')]/following::button[normalize-space()='Continue'][1]",
        "xpath=//button[normalize-space()='Continue']",
        "button:has-text('Continue')",
        "xpath=//input[@value='Continue']",
    ], "Continue", timeout=15000)


def click_next_step(page):
    return try_click(page, [
        "xpath=//*[contains(.,'Overall Progress')]/following::button[normalize-space()='Next Step'][1]",
        "xpath=//button[normalize-space()='Next Step']",
        "button:has-text('Next Step')",
        "xpath=//a[normalize-space()='Next Step']",
    ], "Next Step", timeout=15000)


def slow_scroll_top_to_bottom(page, step_px=100, pause_sec=0.4):
    """Slowly scroll the page from top to bottom (e.g. after Preview)."""
    print("  [INFO] Slow scroll: top → bottom...", flush=True)
    try:
        page.evaluate("window.scrollTo(0, 0)")
        time.sleep(0.6)
        viewport = page.viewport_size or {"height": 800}
        vh = viewport.get("height", 800)
        y = 0
        max_rounds = 200
        for _ in range(max_rounds):
            height = page.evaluate(
                "() => Math.max(document.body.scrollHeight, document.documentElement.scrollHeight)"
            )
            if y >= height - vh:
                page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
                break
            y += step_px
            page.evaluate(f"window.scrollTo(0, {y})")
            time.sleep(pause_sec)
        time.sleep(0.8)
        print("  [OK] Slow scroll complete")
    except Exception as exc:
        print(f"  [WARN] Slow scroll failed: {exc}")


def wait_on_projects_listing(page, wait_sec=20):
    """Stay on the Projects listing page after publish."""
    print(f"  [INFO] Staying on Projects listing page for {wait_sec}s...", flush=True)
    time.sleep(wait_sec)
    print("  [OK] Projects listing wait complete")


def wait_for_publish_enabled(page, timeout_sec=90):
    """Wait until Publish Project button is enabled (required sections complete)."""
    print(f"  Waiting for Publish Project to enable (up to {timeout_sec}s)...", flush=True)
    for i in range(timeout_sec):
        for el in _visible_locators(page, "button:has-text('Publish Project')"):
            try:
                disabled = el.get_attribute("disabled")
                aria_disabled = el.get_attribute("aria-disabled")
                if el.is_enabled() and not disabled and aria_disabled != "true":
                    print(f"  [OK] Publish Project enabled after {i + 1}s")
                    return True
            except Exception:
                continue
        if (i + 1) % 15 == 0:
            print(f"  ... Publish still disabled ({i + 1}s)", flush=True)
        time.sleep(1)
    print("  [WARN] Publish Project did not become enabled in time")
    return False


def click_publish_project(page):
    """Click Publish Project only when the banner button is enabled."""
    try:
        page.locator("text=Overall Progress").first.scroll_into_view_if_needed()
    except Exception:
        pass
    if not wait_for_publish_enabled(page):
        shot(page, "dbg_Publish_Project")
        return False
    sels = [
        "xpath=//*[contains(.,'Overall Progress')]/following::button[contains(.,'Publish Project')][1]",
        "button:has-text('Publish Project')",
        "xpath=//button[contains(.,'Publish Project')]",
    ]
    for sel in sels:
        for el in _visible_locators(page, sel):
            try:
                el.scroll_into_view_if_needed()
                el.click()
                print("  [OK] Clicked 'Publish Project'")
                return True
            except Exception:
                continue
    print("  [WARN] Could not click 'Publish Project'")
    shot(page, "dbg_Publish_Project")
    return False


def is_login_page(page) -> bool:
    url = page.url.lower()
    return (
        "consumer.intel.com" in url
        or "consumerint.intel.com" in url
        or "b2c_1a_unifiedlogin" in url
        or ("login" in url and "onsumaye" not in url)
    )


def is_on_hub(page) -> bool:
    """True when on the AI Edge area after SSO (registration or profile hub)."""
    if is_login_page(page):
        return False
    url = page.url.lower()
    return (
        "ai-edge/registration" in url
        or "ai-edge/profile" in url
        or ("solutions-challenge/ai-edge" in url and "onsumaye.com" in url)
    )


def wait_for_hub_content(page, timeout_sec=90) -> bool:
    """Wait until '+ Create a Project' is visible (hub can take 60+ seconds)."""
    print(f"  Waiting for '+ Create a Project' (up to {timeout_sec}s)...", flush=True)
    shell_ready = False
    for i in range(timeout_sec):
        time.sleep(1)
        try:
            if page.locator("text=Create a Project").count() > 0:
                print(f"  [OK] '+ Create a Project' ready after {i + 1}s", flush=True)
                return True
            if not shell_ready and (
                page.locator("text=Projects").count() > 0
                or page.locator("text=Intake").count() > 0
            ):
                shell_ready = True
                print(f"  [INFO] Hub shell loaded ({i + 1}s), waiting for Create button...", flush=True)
        except Exception:
            pass
        if (i + 1) % 15 == 0:
            print(f"  ... still loading ({i + 1}s)", flush=True)
    print("  [WARN] '+ Create a Project' did not appear in time.", flush=True)
    return False


PROJECT_SECTIONS = [
    "Overview",
    "Details",
    "Additional Info",
    "Application Steps",
    "Media",
]


def count_visible_sections(page) -> list:
    """Return sidebar section names currently visible on the project form."""
    found = []
    for sec in PROJECT_SECTIONS:
        try:
            loc = page.locator(
                f"xpath=//*[contains(@class,'sidebar') or contains(@class,'step') "
                f"or contains(@class,'progress') or self::aside]"
                f"//*[normalize-space()='{sec}']"
            )
            if loc.count() == 0:
                loc = page.get_by_text(sec, exact=True)
            if loc.count() > 0:
                found.append(sec)
        except Exception:
            pass
    return found


def wait_for_all_sections(page, timeout_sec=120) -> bool:
    """Wait until all project form sections appear in the sidebar."""
    print(f"  Waiting for all sections (up to {timeout_sec}s)...", flush=True)
    for i in range(timeout_sec):
        time.sleep(1)
        found = count_visible_sections(page)
        if len(found) == len(PROJECT_SECTIONS):
            print(f"  [OK] All sections visible after {i + 1}s:", flush=True)
            for sec in PROJECT_SECTIONS:
                print(f"    ✅ {sec}")
            return True
        if (i + 1) % 15 == 0:
            print(f"  ... {len(found)}/{len(PROJECT_SECTIONS)} sections at {i + 1}s: {found}",
                  flush=True)
    found = count_visible_sections(page)
    print(f"  [WARN] Missing sections: {set(PROJECT_SECTIONS) - set(found)}", flush=True)
    return False


def open_new_project_from_list(page) -> bool:
    """If still on listing after Create, open the newest project row."""
    print("  [INFO] Opening project from listing...")
    for sel in [
        "xpath=(//a[contains(@href,'/projects/') and not(contains(@href,'projects?'))])[1]",
        "xpath=(//table//tbody//tr[1]//a)[1]",
        "xpath=(//div[contains(@class,'project')]//a)[1]",
        "xpath=(//a[contains(.,'AI Edge')])[1]",
    ]:
        try:
            el = page.wait_for_selector(sel, timeout=8000, state="visible")
            el.click()
            time.sleep(3)
            print(f"  [OK] Opened project link")
            return True
        except Exception:
            continue
    return False


def is_on_project_editor(page) -> bool:
    """True when the project create/edit form is open with sidebar sections."""
    url = page.url.lower()
    if re.search(r"/projects/\d+", url):
        return len(count_visible_sections(page)) >= 3
    if "/create" in url or "/edit" in url:
        return len(count_visible_sections(page)) >= 3
    return len(count_visible_sections(page)) >= 4


def wait_for_project_editor(page, timeout_sec=90) -> bool:
    return wait_for_all_sections(page, timeout_sec=timeout_sec)


def click_create_project(page) -> bool:
    """Click '+ Create a Project' and wait until all form sections load."""
    selectors = [
        "xpath=//button[contains(normalize-space(),'Create a Project')]",
        "xpath=//a[contains(normalize-space(),'Create a Project')]",
        "xpath=//*[contains(normalize-space(),'+ Create a Project')]",
        "text=+ Create a Project",
        "text=Create a Project",
    ]
    for attempt in range(1, 4):
        print(f"\n➡ Clicking '+ Create a Project' (attempt {attempt}/3)...")
        clicked = False
        for sel in selectors:
            try:
                el = page.wait_for_selector(sel, timeout=15000, state="visible")
                el.scroll_into_view_if_needed()
                time.sleep(0.5)
                try:
                    with page.expect_navigation(timeout=60000, wait_until="load"):
                        el.click()
                except Exception:
                    el.click()
                clicked = True
                print("  [OK] Clicked '+ Create a Project'")
                break
            except Exception:
                continue
        if not clicked:
            for role in ("button", "link"):
                try:
                    loc = page.get_by_role(role, name="Create a Project").first
                    loc.scroll_into_view_if_needed()
                    try:
                        with page.expect_navigation(timeout=60000, wait_until="load"):
                            loc.click(timeout=10000)
                    except Exception:
                        loc.click(timeout=10000)
                    clicked = True
                    print(f"  [OK] Clicked via role={role}")
                    break
                except Exception:
                    pass

        if not clicked:
            print(f"  [WARN] Could not click Create on attempt {attempt}")
            time.sleep(10)
            continue

        time.sleep(3)
        print(f"  URL: {page.url}")

        if wait_for_all_sections(page, timeout_sec=120):
            shot(page, "04_create_project")
            return True

        if open_new_project_from_list(page):
            if wait_for_all_sections(page, timeout_sec=60):
                shot(page, "04_create_project")
                return True

        print(f"  [WARN] Sections not fully loaded after attempt {attempt} — retrying...")
        time.sleep(10)
        wait_for_hub_content(page, timeout_sec=20)

    shot(page, "dbg_+_Create_a_Project")
    return False


def has_create_project_button(page) -> bool:
    for sel in [
        "xpath=//a[contains(.,'Create a Project')]",
        "xpath=//button[contains(.,'Create a Project')]",
        "text=Create a Project",
        "text=+ Create a Project",
    ]:
        try:
            page.wait_for_selector(sel, timeout=2000, state="visible")
            return True
        except PWTimeout:
            continue
    return False


def open_project_hub(page) -> bool:
    """Wait for hub shell, ensure Projects tab, then wait for Create button."""
    if wait_for_hub_content(page, timeout_sec=90):
        shot(page, "02b_registration_hub")
        return True

    if "ai-edge/profile" in page.url.lower():
        print("\n➡ Hub still blank — opening registration URL...")
        page.goto(REGISTRATION_URL, wait_until="load", timeout=90000)

    if wait_for_hub_content(page, timeout_sec=60):
        shot(page, "02b_registration_hub")
        return True

    print("  [INFO] Clicking 'Projects' sub-menu...")
    try_click(page, [
        "xpath=//nav//a[normalize-space()='Projects']",
        "xpath=//a[normalize-space()='Projects']",
        "text=Projects",
    ], "Projects (sub-menu)", timeout=15000)
    time.sleep(5)
    shot(page, "02c_projects_tab")

    return wait_for_hub_content(page, timeout_sec=45)


def is_b2c_blocked(page) -> bool:
    try:
        body = page.inner_text("body") or ""
        low = body.lower()
        return "not allowed" in low and "contact administrator" in low
    except Exception:
        return False


def try_sso_login(page) -> bool:
    """Automated Intel SSO using .env credentials (same as PyCharm flow)."""
    if not EMAIL or not PASSWORD:
        print("  [WARN] EMAIL/PASSWORD missing in .env")
        return False
    if not is_login_page(page):
        return True

    print("  Logging in with .env credentials...")
    print(f"  Email: {EMAIL}")

    email_sels = [
        "input[placeholder='Email']", "input[type='email']",
        "input[name='loginfmt']", "#i0116",
    ]
    pwd_sels = [
        "input[placeholder='Password']", "input[type='password']",
        "input[name='passwd']", "#i0118",
    ]

    for sel in email_sels:
        try:
            page.wait_for_selector(sel, timeout=10000, state="visible")
            page.click(sel)
            time.sleep(0.4)
            page.fill(sel, "")
            page.locator(sel).press_sequentially(EMAIL, delay=60)
            print("  [OK] Email entered")
            break
        except PWTimeout:
            continue
    else:
        print("  [ERR] Email field not found")
        return False

    time.sleep(0.8)
    for sel in ["button:has-text('Next')", "#idSIButton9", "input[value='Next']"]:
        try:
            page.click(sel, timeout=6000)
            print("  [OK] Next clicked")
            break
        except PWTimeout:
            continue

    time.sleep(2.5)
    shot(page, "login_after_email")

    for sel in pwd_sels:
        try:
            page.wait_for_selector(sel, timeout=15000, state="visible")
            page.click(sel)
            time.sleep(0.4)
            page.fill(sel, "")
            page.locator(sel).press_sequentially(PASSWORD, delay=60)
            print("  [OK] Password entered")
            break
        except PWTimeout:
            continue
    else:
        print("  [ERR] Password field not found")
        return False

    time.sleep(0.8)
    for sel in [
        "button:has-text('Sign In')", "button:has-text('Sign in')",
        "#idSIButton9", "input[value='Sign in']",
    ]:
        try:
            page.click(sel, timeout=6000)
            print("  [OK] Sign In clicked")
            break
        except PWTimeout:
            continue

    time.sleep(2)
    for sel in ["button:has-text('Yes')", "#idSIButton9", "input[value='Yes']", "#idBtn_Back"]:
        try:
            page.click(sel, timeout=3000)
            print("  [OK] Stay-signed-in prompt handled")
            break
        except PWTimeout:
            pass

    print("  Waiting for redirect after login", end="", flush=True)
    for _ in range(90):
        time.sleep(1)
        print(".", end="", flush=True)
        if is_b2c_blocked(page):
            print("\n  [ERR] Intel blocked login — try manual login or contact admin.")
            shot(page, "login_blocked")
            return False
        if "onsumaye.com" in page.url.lower() and not is_login_page(page):
            print(f"\n  [OK] Redirected → {page.url}")
            shot(page, "login_after_signin")
            return True

    print("\n  [WARN] Login redirect timed out.")
    shot(page, "login_timeout")
    return False


def is_ai_edge_logged_in(page) -> bool:
    """True when past Intel SSO and on the AI Edge portal (profile/registration/projects)."""
    if is_login_page(page):
        return False
    url = page.url.lower()
    return (
        "solutions-challenge/ai-edge" in url
        or ("ecosystem-engagement" in url and "ai-edge" in url)
    )


def wait_for_ai_edge(page, timeout_sec=120) -> bool:
    """Poll until SSO completes and AI Edge URL loads."""
    print(f"  Waiting for AI Edge portal (up to {timeout_sec}s)...", end="", flush=True)
    for i in range(timeout_sec):
        time.sleep(1)
        if is_b2c_blocked(page):
            print("\n  [ERR] Intel blocked this account.")
            shot(page, "login_blocked")
            return False
        if is_ai_edge_logged_in(page):
            print(f"\n  [OK] AI Edge portal ready after {i + 1}s → {page.url}")
            return True
        if (i + 1) % 20 == 0 and is_login_page(page):
            print(f"\n  [INFO] Still on SSO ({i + 1}s) — retrying automated login...")
            try_sso_login(page)
        print(".", end="", flush=True)
    print("\n  [WARN] Timed out waiting for AI Edge portal.")
    return False


def ensure_hub_access(page, context) -> bool:
    """Log in via Intel SSO and reach the AI Edge project area."""
    print(f"  Checking access — URL: {page.url[:100]}...")

    if is_ai_edge_logged_in(page):
        print(f"  [OK] Already on AI Edge portal")
        try:
            context.storage_state(path=AUTH_PATH)
            print("  [OK] Session saved to auth.json")
        except Exception as e:
            print(f"  [WARN] Could not save auth.json: {e}")
        return True

    if is_login_page(page):
        print("\n➡ Intel SSO login required...")
        try_sso_login(page)
        if not is_ai_edge_logged_in(page):
            print("  [INFO] Retrying SSO login...")
            time.sleep(3)
            try_sso_login(page)
        if not wait_for_ai_edge(page, timeout_sec=120):
            if is_login_page(page):
                shot(page, "login_blocked")
                print(f"  [ERR] SSO login failed. URL: {page.url[:120]}")
                return False

    if not is_ai_edge_logged_in(page) and not is_login_page(page):
        print("  [INFO] Navigating to AI Edge hub...")
        try:
            page.goto(REGISTRATION_URL, wait_until="load", timeout=90000)
        except Exception:
            page.goto(REGISTRATION_URL, wait_until="domcontentloaded", timeout=90000)
        time.sleep(5)
        if is_login_page(page):
            print("  [INFO] SSO required after navigation...")
            try_sso_login(page)
            if not wait_for_ai_edge(page, timeout_sec=120):
                shot(page, "login_blocked")
                return False

    if not is_ai_edge_logged_in(page):
        if not wait_for_ai_edge(page, timeout_sec=60):
            shot(page, "login_wrong_page")
            print(f"  [ERR] Could not reach AI Edge portal. URL: {page.url[:120]}")
            return False

    try:
        context.storage_state(path=AUTH_PATH)
        print("  [OK] Session saved to auth.json")
    except Exception as e:
        print(f"  [WARN] Could not save auth.json: {e}")

    print(f"  [OK] Hub access OK → {page.url[:100]}...")
    return True


# ─────────────────────────────────────────────────────────────
#  LOGIN (legacy — kept for reference, not used)
# ─────────────────────────────────────────────────────────────
def _do_login_automated_unused(page):
    """
    From screenshots Image 2 & 3:
      Page 1: single Email field + Next button
      Page 2: Password field + Sign In button
    """
    print("  Login page detected — entering credentials from .env ...")
    print(f"  URL: {page.url}")

    # ── Email ──────────────────────────────────────────────
    for sel in ["input[placeholder='Email']", "input[type='email']",
                "input[name='loginfmt']", "input[id='i0116']"]:
        try:
            page.wait_for_selector(sel, timeout=10000, state="visible")
            page.fill(sel, EMAIL)
            print(f"  [OK] Email entered")
            break
        except PWTimeout:
            continue
    else:
        print("  [ERR] Email field not found")
        shot(page, "login_email_debug")
        return False

    time.sleep(0.5)

    # ── Next ───────────────────────────────────────────────
    for sel in ["button:has-text('Next')", "#idSIButton9",
                "button[type='submit']", "input[value='Next']"]:
        try:
            page.click(sel, timeout=6000)
            print("  [OK] Next clicked")
            break
        except PWTimeout:
            continue

    time.sleep(3)
    shot(page, "login_after_email")

    # ── Password ───────────────────────────────────────────
    # Image 3 shows placeholder "Password" field
    for sel in ["input[placeholder='Password']", "input[type='password']",
                "input[name='passwd']", "input[id='i0118']"]:
        try:
            page.wait_for_selector(sel, timeout=12000, state="visible")
            page.fill(sel, PASSWORD)
            print("  [OK] Password entered")
            break
        except PWTimeout:
            continue
    else:
        print("  [ERR] Password field not found")
        shot(page, "login_pwd_debug")
        return False

    time.sleep(0.5)

    # ── Sign In ────────────────────────────────────────────
    # Image 3 shows "Sign In" button
    for sel in ["button:has-text('Sign In')", "button:has-text('Sign in')",
                "#idSIButton9", "button[type='submit']", "input[value='Sign in']"]:
        try:
            page.click(sel, timeout=6000)
            print("  [OK] Sign In clicked")
            break
        except PWTimeout:
            continue

    time.sleep(4)
    shot(page, "login_after_signin")

    # Stay signed in prompt
    for sel in ["button:has-text('Yes')", "#idSIButton9", "input[value='Yes']", "#idBtn_Back"]:
        try:
            page.click(sel, timeout=4000)
            print("  [OK] Stay-signed-in prompt handled")
            time.sleep(2)
            break
        except PWTimeout:
            continue

    # Poll for redirect back to app (up to 60s)
    print("  Waiting for redirect", end="", flush=True)
    for i in range(60):
        time.sleep(1)
        print(".", end="", flush=True)
        if "onsumaye.com" in page.url and "login" not in page.url.lower():
            print(f"\n  [OK] Redirected → {page.url}")
            return True
        try:
            body = page.inner_text("body") or ""
            if "Please provide the following details" in body and "contact administrator" in body:
                print("\n  [ERR] Azure B2C bot-block. Refresh cookies.")
                shot(page, "login_blocked")
                return False
        except Exception:
            pass

    print()
    # Direct nav fallback
    page.goto(BASE_URL, wait_until="domcontentloaded", timeout=30000)
    time.sleep(4)
    return "onsumaye.com" in page.url


# ─────────────────────────────────────────────────────────────
#  MAIN TEST
# ─────────────────────────────────────────────────────────────
def run_test():
    use_auth = os.path.isfile(AUTH_PATH)

    print("=" * 62)
    print("  ISBC Project Test — End-to-End Create → Publish")
    print("=" * 62)
    print(f"  BASE_URL : {BASE_URL}")
    print(f"  EMAIL    : {EMAIL}")
    print(f"  Session  : {'auth.json' if use_auth else 'none (manual login required)'}")
    print(f"  Hub URL  : {REGISTRATION_URL}")
    print(f"  Project  : {PROJECT_NAME}")

    with sync_playwright() as p:
        print("\n🚀 Launching browser...")
        launch_args = {
            "headless": False,
            "args": [
                "--disable-blink-features=AutomationControlled",
                "--no-sandbox",
                "--window-size=1440,900",
                "--start-maximized",
            ],
        }
        try:
            browser = p.chromium.launch(channel="chrome", **launch_args)
            print("  [OK] Using installed Google Chrome")
        except Exception:
            browser = p.chromium.launch(**launch_args)
            print("  [INFO] Using Playwright Chromium")
        ctx_args = {
            "viewport":   {"width": 1440, "height": 900},
            "user_agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/146.0.0.0 Safari/537.36"
            ),
        }
        if HT_USER and HT_PASS:
            ctx_args["http_credentials"] = {"username": HT_USER, "password": HT_PASS}
            print(f"  HTTP Auth: {HT_USER}")

        if use_auth:
            ctx_args["storage_state"] = AUTH_PATH
            context = browser.new_context(**ctx_args)
            print("  [OK] Loaded saved session from auth.json")
        else:
            context = browser.new_context(**ctx_args)
            print("  [WARN] No auth.json — SSO login will run from .env")

        page = context.new_page()
        page.add_init_script(
            "Object.defineProperty(navigator, 'webdriver', { get: () => undefined });"
        )

        # ── Open portal → ENGAGEMENT → Submit an Offering (PyCharm flow) ──
        print(f"\n➡ Opening {BASE_URL} ...")
        page.goto(BASE_URL, timeout=60000, wait_until="domcontentloaded")
        time.sleep(3)
        shot(page, "00_opened")
        print(f"  URL: {page.url}")

        print("\n➡ Clicking ENGAGEMENT in top nav...")
        try_click(page, [
            "xpath=//nav//a[normalize-space()='ENGAGEMENT']",
            "xpath=//a[normalize-space()='ENGAGEMENT']",
            "xpath=//li[normalize-space()='ENGAGEMENT']/a",
            "text=ENGAGEMENT",
            "text=Engagement",
        ], "ENGAGEMENT", timeout=15000)
        time.sleep(2)
        shot(page, "01_engagement_menu")

        print("\n➡ Clicking 'Submit an Offering'...")
        try_click(page, [
            "xpath=//a[normalize-space()='Submit an Offering']",
            "text=Submit an Offering",
            "xpath=//a[contains(.,'Submit an Offering')]",
        ], "Submit an Offering", timeout=15000)
        time.sleep(3)
        shot(page, "02_submit_offering")
        print(f"  URL: {page.url}")

        if not ensure_hub_access(page, context):
            print("❌ Could not reach AI Edge portal — cannot continue.")
            print("   Tip: delete auth.json and re-run, or check EMAIL/PASSWORD in .env")
            browser.close()
            return

        shot(page, "03_after_login")
        print(f"  URL: {page.url}")

        if not open_project_hub(page):
            print("❌ Project hub did not finish loading.")
            browser.close()
            return

        if not click_create_project(page):
            print("❌ Could not open project form with all sections — aborting.")
            browser.close()
            return

        shot(page, "04b_all_sections_visible")

        # ══════════════════════════════════════════════════════
        # STEP 1 — Click Edit (on Overview section)
        # Image 5: shows pencil ✎ Edit button on the right side
        # ══════════════════════════════════════════════════════
        sep(1, "Click Edit button on Overview")
        click_section_edit(page, "Overview")
        time.sleep(2)
        shot(page, "S01_edit_clicked")

        # ══════════════════════════════════════════════════════
        # STEP 2 — Overview: fill Q1–Q6
        # Image 6: shows the edit form with Q1-Q6
        # ══════════════════════════════════════════════════════
        sep(2, "Overview — fill Q1 to Q6")

        # Q1: Project Name — simple text input
        # Image 6: Q1 "Project Name *" is a plain input field
        try_fill(page, [
            "xpath=//label[contains(.,'Project Name')]/following::input[@type='text'][1]",
            "input[name*='project_name' i]",
            "input[id*='project_name' i]",
            "input[placeholder*='name' i]",
            "xpath=(//input[@type='text'])[1]",
        ], PROJECT_NAME, "Q1: Project Name")
        time.sleep(0.5)

        # Q2: Project Description — simple textarea
        # Image 6: Q2 "Project Description *" is a plain textarea
        try_fill(page, [
            "xpath=//label[contains(.,'Project Description')]/following::textarea[1]",
            "textarea[name*='project_desc' i]",
            "textarea[name*='description' i]",
            "textarea[placeholder*='project description' i]",
            "xpath=(//textarea)[1]",
        ], PROJECT_DESC, "Q2: Project Description")
        time.sleep(0.5)

        # Q3–Q4: rich text editors
        fill_near_question(page, "business problem", BUSINESS_PROBLEM, "Q3: Business Problem")
        if not fill_near_question(page, "key features", SOLUTION_FEATURES, "Q4: Solution & Key Features"):
            fill_near_question(page, "solution", SOLUTION_FEATURES, "Q4: Solution & Key Features")
        time.sleep(0.5)

        # Q5: Industry — multiselect checkbox list (select up to 3)
        page.locator("text=industry does your application apply").first.scroll_into_view_if_needed()
        time.sleep(0.3)
        check_multiselect_checkboxes(
            page, "industry does your application apply",
            ["Manufacturing", "Healthcare", "Retail"],
            label="Q5: Industry", max_count=3,
        )
        wait_for_field_valid(page, "industry does your application apply")

        # Q6: Use Cases — plain text field
        fill_near_question(
            page, "use cases does your application address",
            USE_CASES_TEXT, "Q6: Use Cases", multiline=True,
        )
        time.sleep(0.5)

        shot(page, "S02_overview_filled")

        # ══════════════════════════════════════════════════════
        # STEP 3 — Click Continue
        # Image 6: "Done" button bottom-left, Continue bottom-right
        # ══════════════════════════════════════════════════════
        sep(3, "Click Continue (Overview → Details)")
        click_continue(page)
        time.sleep(3)
        wait_for_sidebar_green(page, "Overview")
        shot(page, "S03_after_continue_overview")
        print(f"  URL: {page.url}")

        # ══════════════════════════════════════════════════════
        # STEP 4 — Details tab: click Edit, fill Q1–Q12
        # Image 7: shows all 12 questions on Details tab
        # ══════════════════════════════════════════════════════
        sep(4, "Details tab — click Edit + fill Q1–Q12")

        click_sidebar_tab(page, "Details")
        time.sleep(2)
        if not click_section_edit(page, "Details"):
            try_click(page, [
                "button:has-text('Edit'):not(:has-text('Project'))",
                "a:has-text('Edit'):not(:has-text('Project'))",
            ], "Edit (Details fallback)", timeout=10000)
        time.sleep(2)
        shot(page, "S04_details_edit_open")

        def _scroll_q(fragment):
            try:
                page.locator(f"text={fragment}").first.scroll_into_view_if_needed()
                time.sleep(0.3)
            except Exception:
                pass

        # Q1: AI workload description — text field
        fill_near_question(
            page, "type of AI workload your application performs",
            AI_WORKLOAD_DESC, "Q1: AI Workload", multiline=True,
        )
        wait_for_field_valid(page, "type of AI workload your application performs")

        # Q2: workload location — multiselect checkboxes (select all that apply)
        page.locator("text=AI workload take place").first.scroll_into_view_if_needed()
        time.sleep(0.3)
        check_multiselect_checkboxes(
            page, "AI workload take place",
            ["Edge", "Cloud", "On-Premises", "Hybrid"],
            label="Q2: Workload Location", select_all=True,
        )
        wait_for_field_valid(page, "AI workload take place")

        # Q3–Q4: multi-select dropdowns
        select_multi_near_question(
            page, "hardware components run the AI workload",
            ["CPU", "GPU", "NPU"], "Q3: Hardware Components",
        )
        select_multi_near_question(
            page, "What hardware does your application run on",
            ["Intel® Core™ Ultra Processors", "Intel® Xeon® Processors"],
            "Q4: Application Hardware",
        )

        # Q5: Open Software Platform — required rich text editor field
        _scroll_q("ingredients from the Open Software Platform")
        fill_rich_text_near_question(
            page, "ingredients from the Open Software Platform",
            OPEN_SOFTWARE_TEXT, "Q5: Open Software Platform",
        )
        if not wait_for_field_valid(page, "Open Software Platform"):
            fill_rich_text_near_question(
                page, "one or more ingredients",
                OPEN_SOFTWARE_TEXT, "Q5: Open Software Platform (retry)",
            )
            wait_for_field_valid(page, "Open Software Platform")

        # Q6: Onboard process — Yes/No
        _scroll_q("onboard process")
        click_radio_yn(page, "onboard process", "Yes", "Q6: Onboard Process")

        # Q7: Commercially available — Yes/No (No reveals follow-up text field)
        _scroll_q("commercially available")
        click_radio_yn(page, "commercially available", "No", "Q7: Commercially Available")
        fill_conditional_after_radio(
            page, "commercially available", Q7_NO_REASON, "Q7: Not Available Reason",
        )

        # Q8: Geographies — multi-select dropdown
        _scroll_q("geographies")
        select_multi_near_question(
            page, "geographies where this application",
            ["North America", "Europe", "Asia Pacific"], "Q8: Geographies",
        )

        # Q9: Hardware ODMs/OEMs — required field (one ODM/OEM name per line)
        _scroll_q("Which Hardware ODMs/OEMs")
        ensure_details_q9_filled(page)

        # Q10: Distribution Partners — Yes/No (Yes reveals follow-up text field)
        _scroll_q("Distribution Partners")
        click_radio_yn(page, "Distribution Partners", "Yes", "Q10: Distribution Partners")
        fill_conditional_after_radio(
            page, "Distribution Partners", Q10_YES_PARTNERS, "Q10: Partner Details",
        )

        # Q11: Customer Support — text field
        _scroll_q("customer support")
        fill_near_question(
            page, "manage customer support",
            SUPPORT_DESC, "Q11: Customer Support", multiline=True,
        )
        wait_for_field_valid(page, "manage customer support")

        # Q12: Success Stories — rich text editor
        _scroll_q("success stories")
        if not fill_rich_text_near_question(
            page, "success stories", SUCCESS_STORY, "Q12: Success Story",
        ):
            fill_near_question(
                page, "success stories",
                SUCCESS_STORY, "Q12: Success Story", multiline=True,
            )
        wait_for_field_valid(page, "success stories")

        # Final pass — Q9 must have content before leaving Details
        _scroll_q("Which Hardware ODMs/OEMs")
        ensure_details_q9_filled(page)

        shot(page, "S04_details_filled")

        # ══════════════════════════════════════════════════════
        # STEP 5 — Click Continue (Details → Additional Info)
        # ══════════════════════════════════════════════════════
        sep(5, "Click Continue (Details)")
        if not _q9_field_has_content(page):
            ensure_details_q9_filled(page)
        click_continue(page)
        time.sleep(3)
        wait_for_sidebar_green(page, "Details")
        shot(page, "S05_after_continue_details")

        # ══════════════════════════════════════════════════════
        # STEP 6 — Additional Info: click Edit
        # Image 8: shows Additional Info tab with Edit button top-right
        # ══════════════════════════════════════════════════════
        sep(6, "Additional Info — click Edit")
        click_sidebar_tab(page, "Additional Info")
        time.sleep(2)
        if not click_section_edit(page, "Additional Info"):
            try_click(page, [
                "button:has-text('Edit'):not(:has-text('Project'))",
            ], "Edit (Additional Info fallback)", timeout=10000)
        time.sleep(2)
        shot(page, "S06_additional_info_edit")

        # ══════════════════════════════════════════════════════
        # STEP 7 — Click '+ Add New Section', fill Section 1
        # Image 8: "+ Add New Section" button
        # Image 9: after clicking, shows "Section 1" label + rich text editor
        # ══════════════════════════════════════════════════════
        sep(7, "Add New Section + fill Section 1")
        try_click(page, [
            "xpath=//*[contains(.,'Additional Info')]/following::button[contains(.,'Add New Section')][1]",
            "xpath=//button[contains(.,'Add New Section')]",
            "xpath=//a[contains(.,'Add New Section')]",
            "button:has-text('Add New Section')",
            "text=+ Add New Section",
            "text=Add New Section",
        ], "+ Add New Section", timeout=15000)
        time.sleep(2)
        shot(page, "S07_section_added")

        # Fill Section 1 (textarea or rich text)
        if not fill_near_question(page, "Section 1", ADDITIONAL_INFO, "Section 1", multiline=True):
            fill_rich_text(page, "xpath=//*[contains(.,'Section 1')]", ADDITIONAL_INFO, "Section 1")
        shot(page, "S07_section_filled")

        # ══════════════════════════════════════════════════════
        # STEP 8 — Click Continue (Additional Info → App Steps)
        # ══════════════════════════════════════════════════════
        sep(8, "Click Continue (Additional Info)")
        click_continue(page)
        time.sleep(3)
        shot(page, "S08_after_continue_additional")

        # ══════════════════════════════════════════════════════
        # STEP 9 — Application Steps: Next Step → Edit → fill step
        # ══════════════════════════════════════════════════════
        sep(9, "Application Steps — Edit then fill step")
        click_sidebar_tab(page, "Application Steps")
        time.sleep(2)
        if not click_section_edit(page, "Application Steps"):
            try_click(page, [
                "button:has-text('Edit'):not(:has-text('Project'))",
            ], "Edit (Application Steps fallback)", timeout=10000)
        time.sleep(2)
        shot(page, "S09_appsteps_edit")

        # ══════════════════════════════════════════════════════
        # STEP 10 — Fill Step Title + Step Description
        # ══════════════════════════════════════════════════════
        sep(10, "Fill Step Title & Description")
        try_click(page, [
            "xpath=//button[contains(.,'Add New Steps')]",
            "button:has-text('Add New Steps')",
            "text=+ Add New Steps",
        ], "+ Add New Steps", timeout=10000)
        time.sleep(1)

        try_fill(page, [
            "xpath=//label[contains(.,'Step Title')]/following::input[1]",
            "input[placeholder*='Step Title' i]",
            "input[name*='step_title' i]",
            "xpath=//*[contains(.,'Step Title')]/following::input[@type='text'][1]",
        ], STEP_TITLE, "Step Title")
        time.sleep(0.4)

        if not fill_near_question(page, "Step Description", STEP_DESC, "Step Description", multiline=True):
            fill_rich_text(page, "xpath=//*[contains(.,'Step Description')]", STEP_DESC, "Step Description")
        shot(page, "S10_step_filled")

        # ══════════════════════════════════════════════════════
        # STEP 11 — Done (save App Steps) → go to Media
        # ══════════════════════════════════════════════════════
        sep(11, "Done (Application Steps) → Media")
        click_done(page)
        time.sleep(2)
        click_sidebar_tab(page, "Media")
        time.sleep(2)
        shot(page, "S11_after_continue_appsteps")

        # ══════════════════════════════════════════════════════
        # STEP 12 — Skip Media: click Next Step
        # Image 12: Media tab shows "No media" + "Next Step" button (bottom right)
        # ══════════════════════════════════════════════════════
        sep(12, "Skip Media — click Next Step")
        if not click_next_step(page):
            click_done(page)
            time.sleep(1)
            click_next_step(page)
        time.sleep(3)
        shot(page, "S12_skip_media")
        print(f"  URL: {page.url}")

        # ══════════════════════════════════════════════════════
        # STEP 13 — Click Preview (under the progress banner; skip My Team)
        # Image 13: shows "Preview" button in the dark progress bar (bottom of banner)
        # ══════════════════════════════════════════════════════
        sep(13, "Click Preview (in progress banner)")
        try_click(page, [
            "xpath=//button[normalize-space()='Preview']",
            "xpath=//a[normalize-space()='Preview']",
            "button:has-text('Preview')",
            "a:has-text('Preview')",
            "text=Preview",
        ], "Preview", timeout=15000)
        time.sleep(3)
        print(f"  URL: {page.url}")
        slow_scroll_top_to_bottom(page)
        shot(page, "S13_preview_page")

        # ══════════════════════════════════════════════════════
        # STEP 14 — Click Edit Project (top right corner)
        # Image 14: shows "Edit Project" button at top right of the preview page
        # ══════════════════════════════════════════════════════
        sep(14, "Click Edit Project (top-right on preview)")
        try_click(page, [
            "xpath=//button[normalize-space()='Edit Project']",
            "xpath=//a[normalize-space()='Edit Project']",
            "button:has-text('Edit Project')",
            "a:has-text('Edit Project')",
            "text=Edit Project",
        ], "Edit Project", timeout=15000)
        time.sleep(3)
        shot(page, "S14_edit_project")
        print(f"  URL: {page.url}")

        # ══════════════════════════════════════════════════════
        # STEP 15 — Click Publish Project
        # Image 13: shows "Publish Project" button in dark banner (100% progress)
        # ══════════════════════════════════════════════════════
        sep(15, "Click Publish Project")
        wait_for_sidebar_green(page, "Overview")
        wait_for_sidebar_green(page, "Details")
        click_publish_project(page)
        time.sleep(3)
        shot(page, "S15_after_publish_click")

        # Confirmation dialog (if any)
        for conf in ["button:has-text('Confirm')", "button:has-text('Yes')",
                     "button:has-text('Publish')", "button:has-text('OK')"]:
            try:
                page.wait_for_selector(conf, timeout=4000, state="visible")
                page.click(conf)
                print(f"  [OK] Confirmation: {conf}")
                time.sleep(2)
                break
            except PWTimeout:
                continue

        shot(page, "S15_published")
        print(f"  URL: {page.url}")

        # ══════════════════════════════════════════════════════
        # STEP 16 — Click Projects under sub-menu
        # Image 4: "Projects" is in the blue sub-navigation bar
        # ══════════════════════════════════════════════════════
        sep(16, "Click 'Projects' in sub-menu")
        try_click(page, [
            # Blue sub-nav bar has: Intake form | Projects | Resources | Advisors | Help
            "xpath=//nav[contains(@class,'sub') or contains(@class,'inner')]//a[normalize-space()='Projects']",
            "xpath=//div[contains(@class,'sub-nav') or contains(@class,'secondary')]//a[normalize-space()='Projects']",
            "xpath=//ul//a[normalize-space()='Projects']",
            "xpath=//a[normalize-space()='Projects']",
            "text=Projects",
        ], "Projects (sub-menu)", timeout=15000)
        time.sleep(2)
        shot(page, "S16_projects_page")
        print(f"  URL: {page.url}")
        wait_on_projects_listing(page, wait_sec=20)

        # ── Final summary ─────────────────────────────────────
        print(f"\n{'═'*62}")
        print("  🎉 END-TO-END TEST COMPLETE")
        print(f"{'═'*62}")
        print(f"  Project Name : {PROJECT_NAME}")
        print(f"  Final URL    : {page.url}")
        print("  Screenshots  : S01 → S16 saved")

        time.sleep(5)
        browser.close()
        print("\nBrowser closed. Done.")


if __name__ == "__main__":
    run_test()

# end hee