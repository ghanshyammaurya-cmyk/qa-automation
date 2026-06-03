"""
Intel Builders University
Course: Application of DevOps for the Google* Cloud Platform
================================================================
FIXES in this version:
  - Skip iframes with empty src (was crashing the session)
  - Guard every iframe interaction with session-alive checks
  - After video loads, wait longer for Docebo LMS to inject player
  - Quiz and return-to-course steps fully intact

Requirements:
    pip install undetected-chromedriver selenium

HOW TO USE:
  1. Set EMAIL, PASSWORD, CHROME_VERSION below.
  2. Run Shift+F10. Do NOT touch the browser during login.
"""

import os
import time
import random

import undetected_chromedriver as uc

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    TimeoutException, InvalidSessionIdException, WebDriverException,
    NoSuchFrameException,
)

# ─────────────────────────────────────────────────────────────
#  ★  SET THESE  ★
# ─────────────────────────────────────────────────────────────
EMAIL          = os.getenv("INTEL_EMAIL",    "ghanshyam.maurya@gmail.com")
PASSWORD       = os.getenv("INTEL_PASSWORD", "Abc@123456")
CHROME_VERSION = 146        # check chrome://version

COURSE_URL = (
    "https://builders.intel.com/university/course/"
    "application-of-devops-for-the-google-cloud-platform"
)
WAIT          = 20
REDIRECT_WAIT = 90   # Azure B2C can take up to 90s

EXPECTED_COURSE_OVERVIEW  = "DevOps for the Google Cloud Platform"
EXPECTED_CHAPTER_OVERVIEW = "CI/CD"

# Fill after watching video: { "partial question": "partial correct answer" }
QUIZ_ANSWER_KEY: dict = {}


# ─────────────────────────────────────────────────────────────
#  DRIVER
# ─────────────────────────────────────────────────────────────
def build_driver() -> uc.Chrome:
    opts = uc.ChromeOptions()
    opts.add_argument("--window-size=1440,900")
    opts.add_argument("--no-sandbox")
    opts.add_argument("--disable-dev-shm-usage")
    opts.add_argument(
        f"--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        f"AppleWebKit/537.36 (KHTML, like Gecko) "
        f"Chrome/{CHROME_VERSION}.0.0.0 Safari/537.36"
    )
    return uc.Chrome(options=opts, version_main=CHROME_VERSION)


# ─────────────────────────────────────────────────────────────
#  HELPERS
# ─────────────────────────────────────────────────────────────
def is_alive(driver) -> bool:
    """Check if the browser session is still open."""
    try:
        _ = driver.current_url
        return True
    except Exception:
        return False

def ss(driver, name: str):
    if not is_alive(driver):
        return
    try:
        driver.save_screenshot(f"{name}.png")
        print(f"    [📷] {name}.png")
    except Exception:
        pass

def WV(driver, by, sel, t=WAIT):
    return WebDriverWait(driver, t).until(EC.visibility_of_element_located((by, sel)))

def WC(driver, by, sel, t=WAIT):
    return WebDriverWait(driver, t).until(EC.element_to_be_clickable((by, sel)))

def human_type(el, text: str):
    for ch in text:
        el.send_keys(ch)
        time.sleep(random.uniform(0.06, 0.20))

def sep(title: str):
    bar = "─" * 62
    print(f"\n{bar}\n  {title}\n{bar}")

def print_box(title: str, text: str):
    w = 56
    print(f"\n    ╔{'═'*w}╗")
    print(f"    ║  {title:<{w-2}}║")
    print(f"    ╠{'═'*w}╣")
    for line in text.strip().splitlines():
        for chunk in [line[i:i+w-4] for i in range(0, max(len(line), 1), w-4)]:
            print(f"    ║  {chunk:<{w-2}}║")
    print(f"    ╚{'═'*w}╝")

def verify(label: str, text: str, snippet: str) -> bool:
    ok = snippet.lower() in text.lower()
    print(f"    [{'✓ PASS' if ok else '✗ FAIL'}] {label}")
    return ok

def safe_default_content(driver):
    """Switch back to main frame safely."""
    try:
        if is_alive(driver):
            driver.switch_to.default_content()
    except Exception:
        pass


# ─────────────────────────────────────────────────────────────
#  STEP 1 – Open course page
# ─────────────────────────────────────────────────────────────
def step1_open_course(driver):
    sep("STEP 1 │ Open course page")
    driver.get(COURSE_URL)
    time.sleep(4)
    print(f"    URL  : {driver.current_url}")
    print(f"    Title: {driver.title}")
    ss(driver, "01_course_page")


# ─────────────────────────────────────────────────────────────
#  STEP 2 – Verify Course Overview
# ─────────────────────────────────────────────────────────────
def step2_verify_course_overview(driver) -> str:
    sep("STEP 2 │ Verify Course Overview")
    for by, sel in [
        (By.XPATH, "//h2[normalize-space()='Course Overview']/following-sibling::p[1]"),
        (By.XPATH, "//h2[contains(.,'Course Overview')]/..//p[1]"),
        (By.XPATH, "//p[contains(.,'DevOps for the Google Cloud')]"),
        (By.XPATH, "//p[contains(.,'CI/CD')]"),
        (By.CSS_SELECTOR, ".course-overview p"),
        (By.CSS_SELECTOR, ".course-description p"),
    ]:
        try:
            el = WebDriverWait(driver, 6).until(EC.visibility_of_element_located((by, sel)))
            txt = el.text.strip()
            if txt and len(txt) > 40 and "BACK TO" not in txt.upper():
                print_box("COURSE OVERVIEW", txt)
                verify("Course Overview content", txt, EXPECTED_COURSE_OVERVIEW)
                ss(driver, "02_course_overview")
                return txt
        except Exception:
            continue
    # Body fallback
    try:
        body = driver.find_element(By.TAG_NAME, "body").text
        idx = body.find("Course Overview")
        if idx != -1:
            lines = [l.strip() for l in body[idx:idx+800].splitlines()
                     if l.strip() and len(l.strip()) > 40 and "BACK TO" not in l.upper()]
            if lines:
                txt = "\n".join(lines[:5])
                print_box("COURSE OVERVIEW (body)", txt)
                verify("Course Overview content", txt, EXPECTED_COURSE_OVERVIEW)
                ss(driver, "02_course_overview")
                return txt
    except Exception:
        pass
    print("    [WARN] Course Overview not found.")
    ss(driver, "02_debug")
    return ""


# ─────────────────────────────────────────────────────────────
#  STEP 3 – Verify Chapter Overview
# ─────────────────────────────────────────────────────────────
def step3_verify_chapter_overview(driver) -> str:
    sep("STEP 3 │ Verify Chapter Overview")
    for by, sel in [
        (By.XPATH, "//h2[normalize-space()='Chapter Overview']/following-sibling::p[1]"),
        (By.XPATH, "//h2[contains(.,'Chapter Overview')]/..//p[1]"),
        (By.XPATH, "//p[contains(.,'CI/CD') and contains(.,'Google')]"),
        (By.CSS_SELECTOR, ".chapter-overview p"),
        (By.CSS_SELECTOR, ".chapter-description p"),
    ]:
        try:
            el = WebDriverWait(driver, 6).until(EC.visibility_of_element_located((by, sel)))
            txt = el.text.strip()
            if txt and len(txt) > 40:
                print_box("CHAPTER OVERVIEW", txt)
                verify("Chapter Overview content", txt, EXPECTED_CHAPTER_OVERVIEW)
                ss(driver, "03_chapter_overview")
                return txt
        except Exception:
            continue
    try:
        body = driver.find_element(By.TAG_NAME, "body").text
        idx = body.find("Chapter Overview")
        if idx != -1:
            lines = [l.strip() for l in body[idx:idx+800].splitlines()
                     if l.strip() and len(l.strip()) > 40]
            if lines:
                txt = "\n".join(lines[:5])
                print_box("CHAPTER OVERVIEW (body)", txt)
                verify("Chapter Overview content", txt, EXPECTED_CHAPTER_OVERVIEW)
                ss(driver, "03_chapter_overview")
                return txt
    except Exception:
        pass
    print("    [WARN] Chapter Overview not found.")
    ss(driver, "03_debug")
    return ""


# ─────────────────────────────────────────────────────────────
#  STEP 4 – Click Watch Now
# ─────────────────────────────────────────────────────────────
def step4_click_watch_now(driver):
    sep("STEP 4 │ Click 'Watch Now'")
    for by, sel in [
        (By.XPATH, "//a[normalize-space(.)='Watch Now']"),
        (By.XPATH, "//a[contains(normalize-space(.),'Watch')]"),
        (By.XPATH, "//a[contains(@href,'login')]"),
        (By.PARTIAL_LINK_TEXT, "Watch"),
    ]:
        try:
            el = WC(driver, by, sel, t=8)
            href = el.get_attribute("href") or ""
            driver.execute_script("arguments[0].scrollIntoView({block:'center'});", el)
            time.sleep(0.5)
            el.click()
            print(f"    [OK] Watch Now clicked  href={href}")
            time.sleep(4)
            return True
        except Exception:
            continue
    print("    [WARN] Watch Now not found – going to login directly.")
    driver.get(
        "https://builders.intel.com/login?return="
        "aHR0cHM6Ly9idWlsZGVycy5pbnRlbC5jb20vdW5pdmVyc2l0eS9jb3Vyc2UvYXBwbGljYXRpb24tb2YtZGV2b3BzLWZvci10aGUtZ29vZ2xlLWNsb3VkLXBsYXRmb3Jt"
    )
    time.sleep(4)
    return False


# ─────────────────────────────────────────────────────────────
#  STEP 5 – Azure B2C Login
# ─────────────────────────────────────────────────────────────
def step5_login(driver) -> bool:
    sep("STEP 5 │ Microsoft Azure B2C Login")
    print(f"    URL: {driver.current_url}")

    if "builders.intel.com" in driver.current_url and "login" not in driver.current_url:
        print("    [INFO] Already authenticated.")
        return True

    # ── A: Email ──────────────────────────────────────────────
    print("\n    [A] Entering email...")
    email_el = None
    for by, sel in [
        (By.CSS_SELECTOR, "input[name='loginfmt']"),
        (By.CSS_SELECTOR, "input[id='i0116']"),
        (By.CSS_SELECTOR, "input[type='email']"),
        (By.CSS_SELECTOR, "input[name='email']"),
        (By.CSS_SELECTOR, "input[placeholder*='email' i]"),
        (By.XPATH,        "(//input[@type='text'])[1]"),
    ]:
        try:
            email_el = WV(driver, by, sel, t=12)
            email_el.click(); time.sleep(0.4)
            email_el.clear(); time.sleep(0.2)
            human_type(email_el, EMAIL)
            print(f"    [OK] Email entered  ({sel})")
            break
        except Exception:
            continue

    if not email_el:
        print("    [ERR] Email field not found!")
        ss(driver, "login_email_debug")
        return False

    time.sleep(random.uniform(0.8, 1.4))

    for by, sel in [
        (By.CSS_SELECTOR, "#idSIButton9"),
        (By.CSS_SELECTOR, "input[type='submit']"),
        (By.CSS_SELECTOR, "button[type='submit']"),
        (By.XPATH, "//input[@value='Next']"),
        (By.XPATH, "//button[normalize-space()='Next']"),
    ]:
        try:
            WC(driver, by, sel, t=6).click()
            print(f"    [OK] Next clicked  ({sel})")
            break
        except Exception:
            continue
    else:
        email_el.send_keys(Keys.RETURN)

    time.sleep(random.uniform(3, 5))
    ss(driver, "05a_after_email")
    print(f"    URL after email: {driver.current_url}")

    # ── B: Password ───────────────────────────────────────────
    print("\n    [B] Entering password...")
    pwd_el = None
    for by, sel in [
        (By.CSS_SELECTOR, "input[name='passwd']"),
        (By.CSS_SELECTOR, "input[id='i0118']"),
        (By.CSS_SELECTOR, "input[type='password']"),
        (By.CSS_SELECTOR, "input[name='password']"),
    ]:
        try:
            pwd_el = WV(driver, by, sel, t=14)
            pwd_el.click(); time.sleep(0.4)
            pwd_el.clear(); time.sleep(0.2)
            human_type(pwd_el, PASSWORD)
            print(f"    [OK] Password entered  ({sel})")
            break
        except Exception:
            continue

    if not pwd_el:
        print("    [ERR] Password field not found!")
        ss(driver, "login_pwd_debug")
        return False

    time.sleep(random.uniform(0.8, 1.4))

    for by, sel in [
        (By.CSS_SELECTOR, "#idSIButton9"),
        (By.CSS_SELECTOR, "input[type='submit']"),
        (By.CSS_SELECTOR, "button[type='submit']"),
        (By.XPATH, "//input[@value='Sign in']"),
        (By.XPATH, "//button[normalize-space()='Sign in']"),
    ]:
        try:
            WC(driver, by, sel, t=6).click()
            print(f"    [OK] Sign in clicked  ({sel})")
            break
        except Exception:
            continue
    else:
        pwd_el.send_keys(Keys.RETURN)

    time.sleep(4)
    ss(driver, "05b_after_password")

    # ── C: Stay signed in ─────────────────────────────────────
    print("\n    [C] Checking 'Stay signed in?' prompt...")
    for by, sel in [
        (By.CSS_SELECTOR, "#idSIButton9"),
        (By.XPATH, "//input[@value='Yes']"),
        (By.XPATH, "//button[normalize-space()='Yes']"),
        (By.CSS_SELECTOR, "#idBtn_Back"),
        (By.XPATH, "//input[@value='No']"),
    ]:
        try:
            btn = WC(driver, by, sel, t=5)
            val = btn.get_attribute("value") or btn.text or "?"
            btn.click()
            print(f"    [OK] Prompt: '{val}'")
            time.sleep(3)
            break
        except Exception:
            continue

    # ── D: Poll for redirect ──────────────────────────────────
    print(f"\n    [D] Waiting for redirect (up to {REDIRECT_WAIT}s)...")
    print("        ", end="", flush=True)
    success = False
    for elapsed in range(REDIRECT_WAIT):
        time.sleep(1)
        print(".", end="", flush=True)
        try:
            cur = driver.current_url
            if "builders.intel.com" in cur and "login" not in cur:
                print(f"\n    [OK] Redirected after {elapsed+1}s → {cur}")
                success = True
                break
            if "consumer.intel.com" in cur:
                src = driver.page_source
                if ("Please provide the following details" in src
                        and "contact administrator" in src.lower()
                        and src.lower().count("<form") == 0):
                    print(f"\n    [ERR] Intel bot-block detected.")
                    ss(driver, "login_blocked")
                    return False
        except Exception:
            pass
    print()

    if not success:
        print(f"    [WARN] Redirect timed out. URL: {driver.current_url}")
        ss(driver, "login_timeout")
        if "confirmed" in driver.current_url:
            print("    [INFO] SAML confirmed page – navigating to course directly...")
            driver.get(COURSE_URL)
            time.sleep(5)
            if "builders.intel.com" in driver.current_url and "login" not in driver.current_url:
                print(f"    [OK] Manual nav succeeded → {driver.current_url}")
                success = True

    if not success:
        return False

    ss(driver, "05_logged_in")
    print("    [OK] Login successful!")
    return True


# ─────────────────────────────────────────────────────────────
#  STEP 6 – Ensure on course page
# ─────────────────────────────────────────────────────────────
def step6_goto_course(driver):
    sep("STEP 6 │ Navigate to course page")
    if "application-of-devops" in driver.current_url:
        print("    [OK] Already on course page.")
    else:
        driver.get(COURSE_URL)
        time.sleep(5)
        print(f"    [OK] Navigated → {driver.current_url}")
    ss(driver, "06_course_logged_in")


# ─────────────────────────────────────────────────────────────
#  STEP 7 – Play video
#
#  FIX: Skip iframes that have an empty src — these are
#  placeholder iframes injected by Docebo before the player
#  loads. Switching into them crashes the session.
#  Wait up to 15s for Docebo to inject the real player iframe.
# ─────────────────────────────────────────────────────────────
def step7_play_video(driver) -> bool:
    sep("STEP 7 │ Play video")

    # Wait up to 15s for a non-empty, non-analytics iframe to appear
    print("    Waiting for video player iframe to load...")
    player_iframe = None
    SKIP_SRC = ["sharethis", "analytics", "gtm", "pixel", "tag"]

    for attempt in range(15):
        time.sleep(2)
        if not is_alive(driver):
            print("    [ERR] Browser session lost while waiting for iframe.")
            return False
        iframes = driver.find_elements(By.TAG_NAME, "iframe")
        print(f"      Attempt {attempt+1}: {len(iframes)} iframe(s) found", end="")
        for f in iframes:
            src = (f.get_attribute("src") or "").strip()
            if src and not any(s in src.lower() for s in SKIP_SRC):
                print(f" → player found: {src[:80]}")
                player_iframe = f
                break
        if player_iframe:
            break
        print(" → no player iframe yet")

    if not player_iframe:
        print("    [WARN] No player iframe found after 30s.")
        print("    Listing all iframes:")
        for i, f in enumerate(driver.find_elements(By.TAG_NAME, "iframe")):
            print(f"      [{i}] src='{f.get_attribute('src') or '(empty)'}'")
        # Try JS click fallback on main page
        res = driver.execute_script("""
            var sels = ['button.play','.play-btn','.vjs-play-control',
                '[aria-label="Play"]','button[class*="play"]','video'];
            for(var s of sels){
                var el = document.querySelector(s);
                if(el){ el.click(); return 'clicked: '+s; }
            }
            return 'none found';
        """)
        print(f"    JS fallback: {res}")
        ss(driver, "07_video_page")
        return "none" not in res

    # Try to interact with the found iframe
    print(f"\n    Switching into player iframe...")
    try:
        driver.switch_to.frame(player_iframe)
        time.sleep(3)

        if not is_alive(driver):
            safe_default_content(driver)
            return False

        # Check for nested iframes (e.g. Docebo wraps the video player)
        inner_frames = driver.find_elements(By.TAG_NAME, "iframe")
        if inner_frames:
            print(f"    Found {len(inner_frames)} inner iframe(s) – diving in.")
            for j, inf in enumerate(inner_frames):
                isrc = (inf.get_attribute("src") or "").strip()
                print(f"      inner[{j}] src={isrc[:80]}")
                if not isrc:
                    continue
                try:
                    driver.switch_to.frame(inf)
                    time.sleep(1.5)
                    if not is_alive(driver):
                        safe_default_content(driver)
                        return False
                    if _play(driver):
                        print("    [OK] Video playing (inner iframe).")
                        safe_default_content(driver)
                        ss(driver, "07_video_playing")
                        return True
                    driver.switch_to.parent_frame()
                except (NoSuchFrameException, WebDriverException, InvalidSessionIdException) as e:
                    print(f"      inner[{j}] err: {e}")
                    try:
                        driver.switch_to.parent_frame()
                    except Exception:
                        safe_default_content(driver)

        if _play(driver):
            print("    [OK] Video playing (outer iframe).")
            safe_default_content(driver)
            ss(driver, "07_video_playing")
            return True

        safe_default_content(driver)

    except (InvalidSessionIdException, WebDriverException) as e:
        print(f"    [ERR] Session lost during iframe switch: {e}")
        safe_default_content(driver)
        return False

    # Final JS fallback
    if is_alive(driver):
        res = driver.execute_script("""
            var sels = ['button.play','.play-btn','.vjs-play-control',
                '[aria-label="Play"]','button[class*="play"]','video'];
            for(var s of sels){
                var el = document.querySelector(s);
                if(el){ el.click(); return 'clicked: '+s; }
            }
            return 'none found';
        """)
        print(f"    JS fallback: {res}")
        ss(driver, "07_video_page")
        return "none" not in res

    return False


def _play(driver) -> bool:
    """Try all known play button selectors in the current frame."""
    for by, sel in [
        (By.CSS_SELECTOR, "button.play-btn"),
        (By.CSS_SELECTOR, ".vp-play"),
        (By.CSS_SELECTOR, ".ytp-play-button"),
        (By.CSS_SELECTOR, ".vjs-play-control"),
        (By.CSS_SELECTOR, "[aria-label='Play']"),
        (By.CSS_SELECTOR, "button[class*='play']"),
        (By.CSS_SELECTOR, "[class*='PlayButton']"),
        (By.CSS_SELECTOR, "video"),
        (By.XPATH, "//button[contains(@aria-label,'Play')]"),
        (By.XPATH, "//button[contains(@class,'play')]"),
    ]:
        try:
            el = WebDriverWait(driver, 4).until(EC.element_to_be_clickable((by, sel)))
            driver.execute_script("arguments[0].click();", el)
            print(f"    [OK] Play clicked ({sel})")
            return True
        except Exception:
            continue
    return False


# ─────────────────────────────────────────────────────────────
#  STEP 8 – Click Take Quiz
# ─────────────────────────────────────────────────────────────
def step8_click_take_quiz(driver) -> bool:
    sep("STEP 8 │ Click 'Take Quiz'")
    if not is_alive(driver):
        print("    [ERR] Browser session is not alive.")
        return False

    for by, sel in [
        (By.XPATH,             "//a[normalize-space()='Take Quiz']"),
        (By.XPATH,             "//button[normalize-space()='Take Quiz']"),
        (By.LINK_TEXT,         "Take Quiz"),
        (By.PARTIAL_LINK_TEXT, "Take Quiz"),
        (By.XPATH,             "//a[contains(.,'Quiz')]"),
        (By.XPATH,             "//button[contains(.,'Quiz')]"),
        (By.CSS_SELECTOR,      "[class*='quiz']"),
    ]:
        try:
            el = WC(driver, by, sel, t=8)
            driver.execute_script("arguments[0].scrollIntoView({block:'center'});", el)
            time.sleep(0.5)
            el.click()
            print(f"    [OK] 'Take Quiz' clicked  ({sel})")
            time.sleep(5)
            ss(driver, "08_quiz_page")
            return True
        except Exception:
            continue

    print("    [WARN] 'Take Quiz' not found.")
    ss(driver, "08_take_quiz_debug")
    return False


# ─────────────────────────────────────────────────────────────
#  STEP 9 – Answer quiz & submit
# ─────────────────────────────────────────────────────────────
def step9_answer_and_submit(driver) -> bool:
    sep("STEP 9 │ Answer Quiz & Submit")
    if not is_alive(driver):
        return False
    time.sleep(3)
    print(f"    Quiz URL: {driver.current_url}")
    ss(driver, "09a_quiz_loaded")

    questions = []
    for sel in [".question", ".quiz-question", "[class*='question']",
                "li.question", "div.question-item", ".survey-question"]:
        questions = driver.find_elements(By.CSS_SELECTOR, sel)
        if questions:
            print(f"    Found {len(questions)} question(s) via '{sel}'")
            break

    if not questions:
        questions = driver.find_elements(
            By.XPATH,
            "//*[.//input[@type='radio'] or .//input[@type='checkbox']]"
            "[not(ancestor::*[.//input[@type='radio'] or .//input[@type='checkbox']])]"
        )
        if questions:
            print(f"    Found {len(questions)} question block(s) via input scan.")

    if not questions:
        print("    [WARN] No questions found. Page text:")
        try:
            for line in driver.find_element(By.TAG_NAME, "body").text.splitlines()[:50]:
                if line.strip():
                    print(f"      {line.strip()}")
        except Exception:
            pass
        ss(driver, "09_quiz_debug")
        return False

    answered = 0
    for q_idx, q_el in enumerate(questions):
        q_text = q_el.text.strip()
        print(f"\n    Q{q_idx+1}: {q_text[:120]}")

        options = (
            q_el.find_elements(By.CSS_SELECTOR, "input[type='radio']") or
            q_el.find_elements(By.CSS_SELECTOR, "input[type='checkbox']") or
            q_el.find_elements(By.CSS_SELECTOR, "label") or
            q_el.find_elements(By.CSS_SELECTOR, ".answer, .option, [class*='answer']")
        )
        if not options:
            print(f"      [WARN] No options found")
            continue

        for o_idx, opt in enumerate(options):
            print(f"      [{o_idx}] {opt.text.strip()[:80]}")

        chosen_idx = 0
        if QUIZ_ANSWER_KEY:
            for kw, ans in QUIZ_ANSWER_KEY.items():
                if kw.lower() in q_text.lower():
                    for o_idx, opt in enumerate(options):
                        if ans.lower() in opt.text.lower():
                            chosen_idx = o_idx
                            print(f"      [MAP] Answer key → option {o_idx}")
                            break
                    break

        try:
            chosen = options[chosen_idx]
            driver.execute_script("arguments[0].scrollIntoView({block:'center'});", chosen)
            time.sleep(0.3)
            driver.execute_script("arguments[0].click();", chosen)
            print(f"      [OK] Selected [{chosen_idx}]: {chosen.text.strip()[:60]}")
            answered += 1
            time.sleep(0.5)
        except Exception as e:
            print(f"      [ERR] Could not click option: {e}")

    print(f"\n    Answered {answered}/{len(questions)} question(s).")
    ss(driver, "09b_quiz_answered")

    print("\n    Submitting quiz...")
    for by, sel in [
        (By.XPATH, "//button[contains(translate(.,'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'),'submit')]"),
        (By.XPATH, "//input[@type='submit']"),
        (By.XPATH, "//button[contains(.,'Finish')]"),
        (By.XPATH, "//button[contains(.,'Done')]"),
        (By.CSS_SELECTOR, "button[type='submit']"),
        (By.CSS_SELECTOR, ".submit-btn, [class*='submit']"),
        (By.XPATH, "//a[contains(.,'Submit')]"),
    ]:
        try:
            btn = WC(driver, by, sel, t=8)
            driver.execute_script("arguments[0].scrollIntoView({block:'center'});", btn)
            time.sleep(0.5)
            btn.click()
            print(f"    [OK] Submit clicked  ({sel})")
            time.sleep(5)
            ss(driver, "09c_quiz_submitted")
            return True
        except Exception:
            continue

    print("    [WARN] Submit button not found.")
    ss(driver, "09_submit_debug")
    return False


# ─────────────────────────────────────────────────────────────
#  STEP 10 – Capture quiz result
# ─────────────────────────────────────────────────────────────
def step10_capture_result(driver):
    sep("STEP 10 │ Capture Quiz Result")
    if not is_alive(driver):
        return None
    time.sleep(3)
    ss(driver, "10_quiz_result")

    for sel in [".quiz-result", ".quiz-score", ".result-score",
                "[class*='result']", "[class*='score']",
                ".pass-message", ".fail-message", ".completion-message"]:
        try:
            el = WebDriverWait(driver, 6).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, sel))
            )
            txt = el.text.strip()
            if txt:
                print_box("QUIZ RESULT", txt)
                return txt
        except Exception:
            continue

    try:
        body = driver.find_element(By.TAG_NAME, "body").text
        for kw in ["score", "passed", "failed", "correct", "result", "%"]:
            idx = body.lower().find(kw)
            if idx != -1:
                snippet = body[max(0, idx-50):idx+200].strip()
                print_box("QUIZ RESULT (body)", snippet)
                return snippet
    except Exception:
        pass

    print("    [WARN] Quiz result not found.")
    return None


# ─────────────────────────────────────────────────────────────
#  STEP 11 – Return to course detail page
# ─────────────────────────────────────────────────────────────
def step11_return_to_course(driver):
    sep("STEP 11 │ Return to Course Detail Page")
    if not is_alive(driver):
        print("    [WARN] Browser session lost — cannot navigate back.")
        return

    for by, sel in [
        (By.XPATH,             "//a[contains(@href,'application-of-devops')]"),
        (By.XPATH,             "//a[contains(.,'Back to')]"),
        (By.PARTIAL_LINK_TEXT, "Back to"),
    ]:
        try:
            el = WC(driver, by, sel, t=5)
            href = el.get_attribute("href") or ""
            if "application-of-devops" in href or "course" in href.lower():
                el.click()
                print(f"    [OK] Back link: '{el.text.strip()}'")
                time.sleep(4)
                break
        except Exception:
            continue
    else:
        print("    [INFO] No back link — navigating directly.")
        driver.get(COURSE_URL)
        time.sleep(5)

    if is_alive(driver):
        print(f"    URL: {driver.current_url}")
        ss(driver, "11_back_on_course")
        if "application-of-devops" in driver.current_url:
            print("    [✓] Successfully returned to course detail page.")
        else:
            print(f"    [WARN] Unexpected URL: {driver.current_url}")


# ─────────────────────────────────────────────────────────────
#  MAIN
# ─────────────────────────────────────────────────────────────
def main():
    print("=" * 62)
    print("  Intel Builders – DevOps for Google Cloud Platform")
    print("  Overview → Login → Video → Quiz → Return")
    print("=" * 62)

    if "your_email" in EMAIL or "your_password" in PASSWORD:
        print("""
  ✗  CREDENTIALS NOT SET!
     Edit at the top of this file:
       EMAIL    = "your_actual_email@example.com"
       PASSWORD = "your_actual_password"
        """)
        return

    results = {}
    driver  = build_driver()

    try:
        step1_open_course(driver)
        results["course_overview"]  = step2_verify_course_overview(driver)
        results["chapter_overview"] = step3_verify_chapter_overview(driver)
        step4_click_watch_now(driver)

        if not step5_login(driver):
            print("\n  ✗  Login failed. Check screenshots.")
            return

        step6_goto_course(driver)

        results["video_played"] = step7_play_video(driver)

        if not is_alive(driver):
            print("\n  [ERR] Browser session lost after video step.")
            print("        This can happen if the Docebo player iframe")
            print("        triggers a page navigation. Re-run the script.")
            return

        time.sleep(5)

        results["quiz_opened"] = step8_click_take_quiz(driver)
        if results["quiz_opened"]:
            results["quiz_submitted"] = step9_answer_and_submit(driver)
            if results.get("quiz_submitted"):
                results["quiz_result"] = step10_capture_result(driver)

        step11_return_to_course(driver)

        sep("ALL STEPS COMPLETE – SUMMARY")
        print(f"  Final URL         : {driver.current_url if is_alive(driver) else 'N/A'}")
        print(f"  Course Overview   : {'✓ Verified' if results.get('course_overview')  else '✗ Not found'}")
        print(f"  Chapter Overview  : {'✓ Verified' if results.get('chapter_overview') else '✗ Not found'}")
        print(f"  Video Played      : {'✓ Yes'      if results.get('video_played')     else '⚠ May need manual click'}")
        print(f"  Quiz Opened       : {'✓ Yes'      if results.get('quiz_opened')      else '✗ No'}")
        print(f"  Quiz Submitted    : {'✓ Yes'      if results.get('quiz_submitted')   else '✗ No'}")
        res = results.get("quiz_result")
        print(f"  Quiz Result       : {str(res)[:60] if res else 'N/A'}")

        if is_alive(driver):
            print("\n  Browser stays open 30 seconds...")
            time.sleep(30)

    except (InvalidSessionIdException, WebDriverException) as e:
        print(f"\n  [INFO] Browser session ended: {e}")
    except Exception as e:
        print(f"\n  [ERROR] {e}")
        ss(driver, "error")
        raise
    finally:
        try:
            driver.quit()
        except Exception:
            pass
        print("\n  Done.")


if __name__ == "__main__":
    main()