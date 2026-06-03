"""
Intel Builders University - Course Automation Test Script
Validates Programs, Courses, SCORM & Video playback across 3 category URLs.

Requirements:
    pip install playwright
    playwright install chromium

Run:
    python intel_course_automation.py
"""

import time
import re
import json
from dataclasses import dataclass
from typing import List
from playwright.sync_api import sync_playwright, Page

# ─────────────────────────── CONFIGURATION ───────────────────────────────────

CREDENTIALS = {
    "username": "ghanshyam.maurya@gmail.com",
    "password": "Abc@123456",
}

BASE_URL  = "https://builders.intel.com/"
LOGIN_URL = "https://builders.intel.com/login"

CATEGORY_URLS = {
    "AI Everywhere - AI PCs":          "https://builders.intel.com/university/coursescategory/ai-everywhere-ai-pcs",
    "Principles of AI Transformation": "https://builders.intel.com/university/coursescategory/principles-of-ai-transformation",
    "AI on Intel Xeon Processors":     "https://builders.intel.com/university/coursescategory/ai-on-intel-xeon-processors",
}

VIDEO_PLAY_SECONDS = 8


# ─────────────────────────── EXPECTED DATA (from Excel) ──────────────────────

@dataclass
class ProgramData:
    name: str
    description: str

@dataclass
class CourseData:
    program: str
    name: str
    catalog_id: str
    course_type: str
    duration_sec: int
    notes: str = ""


PROGRAMS: List[ProgramData] = [
    ProgramData(
        name="Principles of AI Transformation",
        description=(
            "AI isn't the future and customers need trusted advisors "
            "who can recommend real solutions. This competency develops your expertise across "
            "Intel complete AI ecosystem Intel Xeon processors Intel Gaudi accelerators "
            "OpenVINO toolkit and Agentic AI foundations."
        ),
    ),
    ProgramData(
        name="AI Everywhere AI PCs",
        description=(
            "Empowering the future with AI PCs. Artificial Intelligence AI is transforming "
            "industries at a rapid pace. Discover the tangible benefits of AI PCs"
        ),
    ),
    ProgramData(
        name="AI on Intel Xeon Processors",
        description=(
            "AI is transforming how we work create and solve problems but it needs the right "
            "foundation to deliver on its promise."
        ),
    ),
]

COURSES: List[CourseData] = [
    # Principles of AI Transformation
    CourseData("Principles of AI Transformation", "Getting Started with AI using Intel Technologies",              "en_E-06KYMP", "SCORM", 2400),
    CourseData("Principles of AI Transformation", "Driving AI in the Data Center with Intel Xeon 6 Processors",   "en_E-VZOX98", "SCORM", 1500, "has Xeon Advisor Tool"),
    CourseData("Principles of AI Transformation", "Selling Intel Gaudi 3 AI Accelerators",                        "en_E-02ZNWJ", "SCORM", 1800),
    CourseData("Principles of AI Transformation", "Powering AI Workloads with Intel Software",                    "en_E-VO3YJO", "SCORM", 1800),
    CourseData("Principles of AI Transformation", "Accelerate AI Inference with the OpenVINO Toolkit",            "en_E-04DNQD", "SCORM", 1800),
    CourseData("Principles of AI Transformation", "Unlocking AI Performance with Intel oneAPI Tools",             "en_E-08WX93", "SCORM", 1800),
    CourseData("Principles of AI Transformation", "Confidential AI with Intel",                                   "en_E-VP52QQ", "SCORM", 1800),
    CourseData("Principles of AI Transformation", "Foundations of Agentic AI",                                    "en_E-04D3XK", "SCORM", 1800),
    # AI Everywhere AI PCs
    CourseData("AI Everywhere - AI PCs", "AI PC Overview",                                                         "en_E-VR6O2M", "SCORM",  780),
    CourseData("AI Everywhere - AI PCs", "AI PC Use Cases",                                                        "en_E-1KNQQD", "SCORM", 1500),
    CourseData("AI Everywhere - AI PCs", "Core Conversations AI PCs",                                              "en_E-VR6OO7", "Video",  1200, "no pdf attachment"),
    CourseData("AI Everywhere - AI PCs", "What is TOPS",                                                           "en_E-VZOXX8", "SCORM",  300,  "no pdf attachment"),
    CourseData("AI Everywhere - AI PCs", "Intel Core Ultra Desktop Processors Series 2 for Everyday AI",           "en_E-VO3EYW", "SCORM",  300,  "no pdf attachment"),
    CourseData("AI Everywhere - AI PCs", "AI Privacy and Security",                                                "en_E-033KK8", "SCORM",  300,  "no pdf attachment"),
    CourseData("AI Everywhere - AI PCs", "Hardware vs Software for AI Performance",                                "en_E-1GLK89", "SCORM",  300,  "no pdf attachment"),
    CourseData("AI Everywhere - AI PCs", "Selling into Commercial",                                                "en_E-05WJZ9", "Video",  2280),
    CourseData("AI Everywhere - AI PCs", "Whats New in Commercial Client",                                         "en_E-1QW8GR", "Video",  1200, "has additional PDF: Sales Card"),
    CourseData("AI Everywhere - AI PCs", "Intels AI for IT Powering Large Enterprise Innovation",                  "en_E-VR6XG3", "Video",  1260, "has additional PDF: Sales Card"),
    CourseData("AI Everywhere - AI PCs", "Unlocking SMB Growth Driving Opportunity",                               "en_E-1LNM4L", "Video",   900, "has additional PDF: Sales Card x2"),
    CourseData("AI Everywhere - AI PCs", "Delivering Mission Critical Outcomes with AI PCs",                       "en_E-VNPW8R", "Video",  1020, "has additional PDF: Sales Card"),
    CourseData("AI Everywhere - AI PCs", "AI PC Partnerships",                                                     "en_E-VD4OOP", "SCORM",  300,  "no pdf attachment"),
    # AI on Intel Xeon Processors
    CourseData("AI on Intel Xeon Processors", "Classic AI Powers the World",                                                  "en_E-0JMLWM", "SCORM", 1800, "has course survey"),
    CourseData("AI on Intel Xeon Processors", "AI Data Pipelines",                                                            "en_E-19WJMP", "SCORM", 1800, "has course survey"),
    CourseData("AI on Intel Xeon Processors", "Driving AI in the Data Center with Intel Xeon 6 Processors",                   "en_E-VZOX98", "SCORM", 1500, "has Xeon Advisor Tool"),
    CourseData("AI on Intel Xeon Processors", "HPC and AI Workload Acceleration with Intel Xeon Processors",                  "en_E-1QW4QZ", "SCORM", 1200, "has Xeon Advisor Tool"),
    CourseData("AI on Intel Xeon Processors", "Intel Xeon Processors as the Host CPU for AI Accelerated Systems",             "en_E-0EO4W8", "SCORM", 1800, "has course survey"),
    CourseData("AI on Intel Xeon Processors", "Powering Enterprise AI with Intel Xeon Processors and Leading Industry Partners","en_E-04DNRK","SCORM", 1800, "has course survey"),
    CourseData("AI on Intel Xeon Processors", "Exploring AI Software Solutions Powered by Intel Xeon Processors",             "en_E-02ZNRW", "SCORM", 1800, "has course survey"),
    CourseData("AI on Intel Xeon Processors", "Real World Use Cases Powered by Intel Xeon Processors",                        "en_E-VO3YLW", "SCORM", 2100, "has course survey"),
    CourseData("AI on Intel Xeon Processors", "Agentic AI and Intel Xeon Processors",                                         "en_E-08WXRJ", "SCORM", 1800, "has course survey"),
    CourseData("AI on Intel Xeon Processors", "Building Next Gen AI with OPEA and Intel Xeon Processors",                     "en_E-VP53L3", "SCORM", 1800, "has course survey"),
    CourseData("AI on Intel Xeon Processors", "Securing AI Workloads with Confidential Computing on Intel Xeon Processors",   "en_E-VP53DQ", "SCORM", 2100, "has course survey"),
]


# ─────────────────────────── RESULT TRACKING ─────────────────────────────────

results: List[dict] = []


def log(status: str, category: str, item: str, detail: str = ""):
    icon = "PASS" if status == "PASS" else ("WARN" if status == "WARN" else "FAIL")
    symbol = "[OK]" if status == "PASS" else ("[!!]" if status == "WARN" else "[XX]")
    msg = f"{symbol} [{status}] [{category[:35]}] {item}"
    if detail:
        msg += f" -- {detail}"
    print(msg)
    results.append({"status": status, "category": category, "item": item, "detail": detail})


# ─────────────────────────── HELPERS ─────────────────────────────────────────

def fuzzy_match(actual: str, expected: str, ratio: float = 0.55) -> bool:
    if not expected:
        return True
    exp_words = re.sub(r"[^\w\s]", "", expected.lower()).split()
    act_lower = re.sub(r"[^\w\s]", "", actual.lower())
    if not exp_words:
        return True
    matched = sum(1 for w in exp_words if w in act_lower)
    return (matched / len(exp_words)) >= ratio


def dismiss_overlays(page: Page):
    for sel in [
        "#onetrust-accept-btn-handler",
        "button[id*='accept']",
        "button[aria-label*='close']",
        "button[aria-label*='Close']",
        "button[aria-label*='dismiss']",
        ".modal-close",
        "[class*='cookie'] button",
        "[class*='banner'] button[class*='close']",
    ]:
        try:
            btn = page.locator(sel).first
            if btn.is_visible(timeout=1500):
                btn.click()
                time.sleep(0.3)
        except Exception:
            pass


def safe_goto(page: Page, url: str, retries: int = 2):
    for attempt in range(retries + 1):
        try:
            page.goto(url, wait_until="domcontentloaded", timeout=60000)
            return
        except Exception as e:
            if attempt == retries:
                print(f"   [!!] Navigation failed after {retries+1} attempts: {e}")
                raise
            print(f"   [!!] Nav retry {attempt+1}: {e}")
            time.sleep(3)


def get_active_page(context, pages_before: int) -> Page:
    pages = context.pages
    if len(pages) > pages_before:
        return pages[-1]
    return pages[-1]


# ─────────────────────────── LOGIN ───────────────────────────────────────────

def login(page: Page, context) -> Page:
    print("\n--- Logging in ---")

    # Navigate - use domcontentloaded, never networkidle (causes closed-page crash on redirect)
    try:
        page.goto(LOGIN_URL, wait_until="domcontentloaded", timeout=60000)
    except Exception as e:
        print(f"   [!!] Page load warning (continuing): {e}")

    time.sleep(3)
    dismiss_overlays(page)

    # Print current URL for debugging
    print(f"   Current URL: {page.url}")

    # Fill username
    username_done = False
    for sel in [
        "input[name='username']",
        "input[type='email']",
        "input[name='email']",
        "#username",
        "#email",
        "input[autocomplete='username']",
        "input[autocomplete='email']",
        "input[placeholder*='email' i]",
        "input[placeholder*='user' i]",
        "input[placeholder*='Email' i]",
    ]:
        try:
            el = page.locator(sel).first
            if el.is_visible(timeout=3000):
                el.click()
                el.fill("")
                el.type(CREDENTIALS["username"], delay=50)
                username_done = True
                print(f"   [OK] Username typed via: {sel}")
                break
        except Exception:
            continue

    if not username_done:
        # Dump all inputs for debugging
        inputs = page.locator("input").all()
        print(f"   [!!] Found {len(inputs)} input(s) on page:")
        for i, inp in enumerate(inputs):
            try:
                print(f"        [{i}] type={inp.get_attribute('type')} name={inp.get_attribute('name')} id={inp.get_attribute('id')} placeholder={inp.get_attribute('placeholder')}")
            except Exception:
                pass
        raise RuntimeError("Could not find username/email input field.")

    time.sleep(0.5)

    # Fill password
    password_done = False
    for sel in [
        "input[name='password']",
        "input[type='password']",
        "#password",
        "input[autocomplete='current-password']",
        "input[placeholder*='password' i]",
        "input[placeholder*='Password' i]",
    ]:
        try:
            el = page.locator(sel).first
            if el.is_visible(timeout=3000):
                el.click()
                el.fill("")
                el.type(CREDENTIALS["password"], delay=50)
                password_done = True
                print(f"   [OK] Password typed via: {sel}")
                break
        except Exception:
            continue

    if not password_done:
        raise RuntimeError("Could not find password input field.")

    time.sleep(0.5)

    # Click submit - use expect_navigation to handle redirect gracefully
    submit_done = False
    submit_selectors = [
        "button[type='submit']",
        "input[type='submit']",
        "button:has-text('Sign In')",
        "button:has-text('Log In')",
        "button:has-text('Login')",
        "button:has-text('Sign in')",
        "button:has-text('Submit')",
        "[class*='login-btn']",
        "[class*='submit-btn']",
    ]

    for sel in submit_selectors:
        try:
            el = page.locator(sel).first
            if el.is_visible(timeout=3000):
                print(f"   [OK] Clicking submit via: {sel}")
                # Use expect_navigation to properly handle the redirect
                try:
                    with page.expect_navigation(wait_until="domcontentloaded", timeout=30000):
                        el.click()
                except Exception:
                    # If navigation wrapper fails, do a plain click then sleep
                    el.click()

                submit_done = True
                break
        except Exception:
            continue

    if not submit_done:
        # Try pressing Enter on the password field as fallback
        try:
            page.locator("input[type='password']").first.press("Enter")
            submit_done = True
            print("   [OK] Submitted via Enter key on password field")
        except Exception:
            raise RuntimeError("Could not click submit button or press Enter.")

    # Wait for redirect to fully settle - use time.sleep instead of
    # wait_for_load_state to avoid "Target page closed" error on SSO redirects
    print("   Waiting for post-login redirect to settle ...")
    time.sleep(6)

    # Grab the most recent page (SSO may have opened a new one)
    active = context.pages[-1]

    # Keep polling until we are off any auth/login URL
    for attempt in range(8):
        current = active.url.lower()
        if any(x in current for x in ["login", "signin", "auth", "oauth", "sso", "saml"]):
            print(f"   Still on auth URL (attempt {attempt+1}): {active.url[:70]}")
            time.sleep(4)
            active = context.pages[-1]
        else:
            break

    print(f"   [OK] Login complete. URL: {active.url}")
    return active


# ─────────────────────────── PROGRAM VALIDATION ──────────────────────────────

def validate_program(page: Page, program: ProgramData, url: str):
    safe_goto(page, url)
    dismiss_overlays(page)
    time.sleep(2)

    page_name = ""
    for sel in ["h1", "h2", ".program-title", ".course-category-title",
                ".page-title", "[class*='hero'] h1", "[class*='banner'] h1",
                "[class*='program-name']", "[class*='category-name']"]:
        try:
            txt = page.locator(sel).first.inner_text(timeout=4000).strip()
            if txt:
                page_name = txt
                break
        except Exception:
            continue

    if fuzzy_match(page_name, program.name):
        log("PASS", program.name, "Program Name", f"Found: '{page_name[:80]}'")
    else:
        log("WARN", program.name, "Program Name",
            f"Expected fragment of '{program.name}' -- got '{page_name[:80]}'")

    page_desc = ""
    for sel in [".program-description", ".category-description", ".hero-description",
                "[class*='description']", "[class*='intro'] p", "section p",
                ".program-intro", "main p"]:
        try:
            txt = page.locator(sel).first.inner_text(timeout=3000).strip()
            if len(txt) > 40:
                page_desc = txt
                break
        except Exception:
            continue

    if fuzzy_match(page_desc, program.description[:100]):
        log("PASS", program.name, "Program Description", "Partial match confirmed")
    else:
        log("WARN", program.name, "Program Description",
            f"Could not confirm description ({len(page_desc)} chars found)")


# ─────────────────────────── COURSE HELPERS ──────────────────────────────────

def find_course_card(page: Page, course_name: str):
    # Use first 40 chars to keep selector manageable
    short = course_name[:40].replace("'", "").replace('"', "")
    for sel in [
        f"[class*='course-card']:has-text('{short}')",
        f"[class*='course-item']:has-text('{short}')",
        f"[class*='course']:has-text('{short}')",
        f"article:has-text('{short}')",
        f"li:has-text('{short}')",
    ]:
        try:
            el = page.locator(sel).first
            if el.is_visible(timeout=3000):
                return el
        except Exception:
            continue

    # Fallback: search all visible text on page
    try:
        all_cards = page.locator("[class*='course'], article, li").all()
        for card in all_cards:
            try:
                txt = card.inner_text(timeout=1000)
                if fuzzy_match(txt, course_name, ratio=0.60):
                    return card
            except Exception:
                continue
    except Exception:
        pass

    return None


def click_watch_button(page: Page, card=None) -> bool:
    scope = card if card else page
    for sel in [
        "a:has-text('Watch Now')", "button:has-text('Watch Now')",
        "a:has-text('Watch')",     "button:has-text('Watch')",
        "a:has-text('Start')",     "button:has-text('Start')",
        "a:has-text('Launch')",    "button:has-text('Launch')",
        "a:has-text('Begin')",     "button:has-text('Begin')",
        "a:has-text('Play')",      "button:has-text('Play')",
        "[class*='watch-btn']", "[class*='watch-now']",
        "[class*='launch-btn']", "[class*='start-course']",
        "[class*='cta-button']", "[class*='enroll']",
    ]:
        try:
            btn = scope.locator(sel).first
            if btn.is_visible(timeout=2000):
                btn.click()
                return True
        except Exception:
            continue
    return False


def try_play_video(page: Page, course_name: str, context) -> bool:
    pages_before = len(context.pages)
    clicked = click_watch_button(page)

    if not clicked:
        log("WARN", course_name, "Watch Button", "No Watch/Watch Now button found")
        return False

    log("PASS", course_name, "Watch Button Clicked", "Watch/Watch Now button clicked")
    time.sleep(4)

    active = get_active_page(context, pages_before)
    try:
        active.wait_for_load_state("domcontentloaded", timeout=20000)
    except Exception:
        pass

    time.sleep(2)
    dismiss_overlays(active)

    # Look for video / SCORM player
    for sel in [
        "video",
        "iframe[src*='scorm']", "iframe[src*='video']",
        "iframe[src*='player']", "iframe[src*='vimeo']",
        "iframe[src*='youtube']", "iframe[src*='brightcove']",
        "iframe[src*='kaltura']", "iframe[src*='wistia']",
        "[class*='video-player']", "[class*='scorm-player']",
        "[class*='media-player']",
    ]:
        try:
            el = active.locator(sel).first
            if el.is_visible(timeout=5000):
                # Try to click play
                for play_sel in [
                    "button[aria-label*='Play' i]",
                    "button[title*='Play' i]",
                    ".vjs-play-button",
                    ".play-button",
                    "[class*='play-btn']",
                    "button:has-text('Play')",
                ]:
                    try:
                        pb = active.locator(play_sel).first
                        if pb.is_visible(timeout=2000):
                            pb.click()
                            print(f"   [OK] Play button clicked: {play_sel}")
                            break
                    except Exception:
                        continue

                time.sleep(VIDEO_PLAY_SECONDS)
                log("PASS", course_name, "Video/SCORM Playback",
                    f"Media element found and started ({sel})")
                return True
        except Exception:
            continue

    log("WARN", course_name, "Video/SCORM Playback",
        f"No media element found after Watch click. URL: {active.url[:80]}")
    return False


# ─────────────────────────── COURSE VALIDATION ───────────────────────────────

def validate_courses_on_page(page: Page, program_name: str, context):
    # Match program key (strip special chars for comparison)
    def norm(s):
        return re.sub(r"[^\w\s]", "", s.lower())

    expected = [c for c in COURSES if norm(c.program) in norm(program_name) or
                norm(program_name) in norm(c.program)]

    if not expected:
        log("WARN", program_name, "Course List", "No matching courses found in expected data")
        return

    for course in expected:
        print(f"\n  --- Course: {course.name[:60]} ---")

        card = find_course_card(page, course.name)
        if card is None:
            log("FAIL", course.program, f"Course Card: {course.name[:50]}", "Not found on page")
            continue
        log("PASS", course.program, f"Course Card: {course.name[:50]}", "Visible on page")

        # Verify name in card
        try:
            card_text = card.inner_text(timeout=3000)
            if fuzzy_match(card_text, course.name, ratio=0.50):
                log("PASS", course.program, f"Course Name Match: {course.name[:50]}")
            else:
                log("WARN", course.program, f"Course Name Match: {course.name[:50]}",
                    f"Card text snippet: {card_text[:80]}")
        except Exception:
            pass

        # Resolve course URL from card link
        course_url = None
        try:
            href = card.locator("a").first.get_attribute("href", timeout=3000)
            if href:
                course_url = href if href.startswith("http") else BASE_URL + href
        except Exception:
            pass

        if course_url:
            safe_goto(page, course_url)
            dismiss_overlays(page)
            time.sleep(2)

            # Course description
            desc_text = ""
            for sel in [".course-description", "[class*='description']",
                        "section p", "article p", "main p"]:
                try:
                    t = page.locator(sel).first.inner_text(timeout=3000).strip()
                    if len(t) > 30:
                        desc_text = t
                        break
                except Exception:
                    continue

            if desc_text:
                log("PASS", course.program, f"Course Description: {course.name[:45]}",
                    f"{desc_text[:80]}...")
            else:
                log("WARN", course.program, f"Course Description: {course.name[:45]}",
                    "Description not found")

            # Detect course type
            src = page.content().lower()
            if "scorm" in src:
                detected = "SCORM"
            elif "video" in src or "<video" in src:
                detected = "Video"
            else:
                detected = "unknown"

            exp_type = course.course_type.replace("?", "").strip()
            if detected.lower() == exp_type.lower():
                log("PASS", course.program, f"Course Type ({exp_type}): {course.name[:45]}",
                    f"Detected: {detected}")
            else:
                log("WARN", course.program, f"Course Type: {course.name[:45]}",
                    f"Expected={exp_type}, Detected={detected}")

            # Click Watch / Watch Now and play video
            try_play_video(page, course.name[:50], context)

        else:
            log("WARN", course.program, f"Course URL: {course.name[:50]}",
                "Could not resolve course detail link")

        # Return to category page for next course
        cat_url = CATEGORY_URLS.get(program_name, "")
        if not cat_url:
            # Try fuzzy match on key
            for key, url in CATEGORY_URLS.items():
                if norm(key) in norm(program_name) or norm(program_name) in norm(key):
                    cat_url = url
                    break
        if cat_url:
            safe_goto(page, cat_url)
            dismiss_overlays(page)
            time.sleep(2)


# ─────────────────────────── MAIN ────────────────────────────────────────────

def run():
    with sync_playwright() as pw:
        browser = pw.chromium.launch(
            headless=False,
            slow_mo=100,   # slight slowdown helps stability
            args=[
                "--disable-blink-features=AutomationControlled",
                "--start-maximized",
                "--no-sandbox",
                "--disable-dev-shm-usage",
                "--disable-infobars",
            ],
        )
        context = browser.new_context(
            viewport={"width": 1440, "height": 900},
            user_agent=(
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/124.0.0.0 Safari/537.36"
            ),
            ignore_https_errors=True,
        )

        page = context.new_page()

        # Step 1: Login
        page = login(page, context)

        # Step 2: Validate each program and its courses
        for program_name, url in CATEGORY_URLS.items():
            print(f"\n\n{'='*65}")
            print(f"PROGRAM: {program_name}")
            print(f"URL    : {url}")
            print(f"{'='*65}")

            # Find matching program metadata
            def norm(s):
                return re.sub(r"[^\w\s]", "", s.lower())

            prog_meta = next(
                (p for p in PROGRAMS if norm(p.name) in norm(program_name) or
                 norm(program_name) in norm(p.name)),
                None
            )

            if prog_meta:
                validate_program(page, prog_meta, url)
            else:
                log("WARN", program_name, "Program Metadata", "Not found in test data")

            # Load category page fresh before course iteration
            safe_goto(page, url)
            dismiss_overlays(page)
            time.sleep(2)

            validate_courses_on_page(page, program_name, context)

        browser.close()

    print_summary()


def print_summary():
    total  = len(results)
    passed = sum(1 for r in results if r["status"] == "PASS")
    warned = sum(1 for r in results if r["status"] == "WARN")
    failed = sum(1 for r in results if r["status"] == "FAIL")

    print("\n" + "="*65)
    print("TEST SUMMARY")
    print("="*65)
    print(f"  Total checks : {total}")
    print(f"  [OK] PASS    : {passed}")
    print(f"  [!!] WARN    : {warned}")
    print(f"  [XX] FAIL    : {failed}")
    print("="*65)

    if warned or failed:
        print("\nItems needing attention:")
        for r in results:
            if r["status"] in ("WARN", "FAIL"):
                sym = "[!!]" if r["status"] == "WARN" else "[XX]"
                print(f"  {sym} [{r['category'][:35]}] {r['item']}")
                if r["detail"]:
                    print(f"        -> {r['detail']}")

    with open("test_report.json", "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    print("\nFull report saved to: test_report.json")


if __name__ == "__main__":
    run()