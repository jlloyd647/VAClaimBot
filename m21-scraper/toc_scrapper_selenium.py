from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import os
import json
import time

TOC_URL = "https://www.knowva.ebenefits.va.gov/system/templates/selfservice/va_ssnew/help/customer/locale/en-US/portal/554400000001018/content/554400000073398/M21-1-Adjudication-Procedures-Manual-Table-of-Contents"
OUTPUT_PATH = "data/meta/m21_toc.json"

# Setup Selenium
options = Options()
options.headless = False  # Set to True if you want to run headless
browser = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

def scrape_toc():
    print(f"🌐 Navigating to TOC: {TOC_URL}")
    browser.get(TOC_URL)
    time.sleep(5)  # Wait for JS to render fully

    soup = BeautifulSoup(browser.page_source, "html.parser")
    links = []

    for a in soup.select("a[href]"):
        href = a["href"]
        full_url = urljoin(TOC_URL, href)
        text = a.get_text(strip=True)

        if "/content/" in full_url and "Table-of-Contents" not in full_url:
            links.append({
                "title": text,
                "url": full_url
            })

    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(links, f, ensure_ascii=False, indent=2)

    print(f"✅ Saved {len(links)} TOC links to {OUTPUT_PATH}")
    browser.quit()

if __name__ == "__main__":
    scrape_toc()
