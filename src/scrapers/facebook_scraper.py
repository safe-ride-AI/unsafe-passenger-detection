"""
facebook_scraper.py
Facebook Full-Size Photo Downloader (Login Required + Authenticated Downloads)
Deep-scroll + Auto-resume
"""

import os
import time
import random
import tempfile
import requests
from typing import List, Set, Dict, Optional
from urllib.parse import urlparse

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager


# ===============================================================
# Chrome Driver Setup
# ===============================================================
def make_chrome_driver(headless=False, chrome_bin="/usr/bin/google-chrome"):
    options = Options()
    if os.path.exists(chrome_bin):
        options.binary_location = chrome_bin
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--window-size=1920,1080")

    temp_profile = tempfile.mkdtemp()
    options.add_argument(f"--user-data-dir={temp_profile}")
    if headless:
        options.add_argument("--headless=new")

    service = Service(ChromeDriverManager().install())
    return webdriver.Chrome(service=service, options=options)


# ===============================================================
# Login Facebook
# ===============================================================
def login_facebook(driver, email, password):
    print("Logging into Facebook...")
    driver.get("https://www.facebook.com/login")
    try:
        WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.ID, "email"))).send_keys(email)
        pass_el = driver.find_element(By.ID, "pass")
        pass_el.send_keys(password)
        pass_el.send_keys(Keys.ENTER)
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        time.sleep(3)
        if "checkpoint" in driver.current_url or "/login" in driver.current_url:
            print("Login failed or checkpoint detected!!!")
            return False
        print("Logged in successfully!")
        return True
    except Exception as e:
        print(f"Login error: {e}")
        return False


# ===============================================================
# Cookie Transfer
# ===============================================================
def get_cookies_dict(driver):
    cookies = driver.get_cookies()
    return {c["name"]: c["value"] for c in cookies}


# ===============================================================
# Collect Photo Links (Deep Scroll)
# ===============================================================
def collect_photo_links(driver, photos_url: str, max_scrolls=400) -> List[str]:
    print(f"Visiting {photos_url}")
    driver.get(photos_url)
    WebDriverWait(driver, 25).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
    time.sleep(5)

    actions = ActionChains(driver)
    links: Set[str] = set()
    stagnant = 0
    last_count = 0
    last_height = 0

    for i in range(max_scrolls):
        # Scroll to bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(3)
        
        # Calculate new scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")

        # collect links (safe loop to avoid stale elements)
        anchors = driver.find_elements(By.CSS_SELECTOR, "a[href*='photo.php?fbid=']")
        for a in anchors:
            try:
                href = a.get_attribute("href")
                if href and "photo.php?fbid=" in href:
                    links.add(href.split("&")[0])
            except Exception:
                # stale element — ignore and continue
                continue

        # scroll a bit further
        actions.move_by_offset(random.randint(0, 15), random.randint(0, 15)).perform()
        time.sleep(random.uniform(1.5, 2.5))

        print(f"{len(links)} links after scroll {i+1}")

        # stagnation detection
        if len(links) == last_count:
            stagnant += 1
            if stagnant >= 8:
                print("Stopped: no new photos detected.")
                break
        else:
            stagnant = 0
        last_count = len(links)

    return list(links)
def get_full_image_url(driver, photo_url: str) -> Optional[str]:
    try:
        driver.get(photo_url)
        WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.TAG_NAME, "img")))
        time.sleep(2)
        imgs = driver.find_elements(By.TAG_NAME, "img")
        max_width = 0
        largest_img = None
        
        for img in imgs:
            src = img.get_attribute("src") or ""
            if "scontent" in src:
                try:
                    width = int(img.get_attribute("width") or 0)
                    if width > max_width:
                        max_width = width
                        largest_img = src
                except ValueError:
                    continue
        
        return largest_img
        for img in imgs:
            src = img.get_attribute("src") or ""
            if "scontent" in src and ("_n.jpg" in src or "_n.png" in src):
                return src
        return None
    except Exception as e:
        print(f"Error loading {photo_url}: {e}")
        return None


# ===============================================================
# Download (with skip if exists)
# ===============================================================
def download_image(url: str, outdir: str, fname: str, cookies: Dict[str, str], ua: str):
    os.makedirs(outdir, exist_ok=True)
    path = os.path.join(outdir, fname)

    # Skip if already downloaded
    if os.path.exists(path):
        print(f"Skipping {fname} (already exists)")
        return path

    headers = {"User-Agent": ua, "Referer": "https://www.facebook.com"}
    try:
        r = requests.get(url, headers=headers, cookies=cookies, stream=True, timeout=30)
        r.raise_for_status()
        with open(path, "wb") as f:
            for chunk in r.iter_content(8192):
                f.write(chunk)
        return path
    except Exception as e:
        print(f"Download error: {e}")
        return None


# ===============================================================
# MAIN
# ===============================================================
if __name__ == "__main__":
    PHOTOS_URL = "https://www.facebook.com/groups/407606286547442/media"  # Change this to the desired Facebook page's photos URL
    parsed = urlparse(PHOTOS_URL)
    page_name = parsed.path.strip("/").split("/")[0] or parsed.netloc
    OUT_DIR = f"facebook_full_images_{page_name}"
    HEADLESS = False
    MAX_SCROLLS = 90

    email = os.getenv("FB_EMAIL")
    password = os.getenv("FB_PASSWORD")

    if not email or not password:
        print("Set FB_EMAIL and FB_PASSWORD environment variables before running.")
        exit(1)

    driver = make_chrome_driver(headless=HEADLESS)
    try:
        if not login_facebook(driver, email, password):
            exit(1)

        cookies = get_cookies_dict(driver)
        ua = driver.execute_script("return navigator.userAgent")

        print("Collecting photo links...")
        photo_links = collect_photo_links(driver, PHOTOS_URL, MAX_SCROLLS)
        print(f"Total {len(photo_links)} photo links found.")

        downloaded = 0
        for i, link in enumerate(photo_links, 1):
            fname = f"photo_{i:04d}.jpg"
            if os.path.exists(os.path.join(OUT_DIR, fname)):
                print(f"Skipping already downloaded image {fname}")
                continue

            print(f"\n[{i}/{len(photo_links)}] Opening photo page...")
            full_url = get_full_image_url(driver, link)
            if full_url:
                path = download_image(full_url, OUT_DIR, fname, cookies, ua)
                if path:
                    downloaded += 1
                    print(f"Saved: {path}")
                else:
                    print("Failed to save image")
            else:
                print("No image found")

        print(f"\nDone! Downloaded {downloaded}/{len(photo_links)} new images → '{OUT_DIR}/'")

    finally:
        driver.quit()
