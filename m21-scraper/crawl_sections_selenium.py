from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from datetime import datetime
import time
import json
import os

url = "https://www.knowva.ebenefits.va.gov/system/templates/selfservice/va_ssnew/help/customer/locale/en-US/portal/554400000001018/content/554400000013969/M21-1-Part-I-Chapter-1-Section-A-Historical"

# Setup Chrome (you can toggle headless to True later)
options = Options()
options.headless = False
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# Load page
print(f"Opening: {url}")
driver.get(url)
time.sleep(3)

soup = BeautifulSoup(driver.page_source, "html.parser")

# Extract title
title_tag = soup.select_one("b.article-name > h1")
title = title_tag.get_text(strip=True) if title_tag else "❌ Title not found"

# Extract content
content_div = soup.select_one("div.article-content")
content = content_div.get_text(separator="\n", strip=True) if content_div else "❌ Content not found"

# Extract next section link
next_link = None
for a in soup.find_all("a"):
    if "Next Section" in a.get_text():
        next_link = urljoin(url, a.get("href"))
        break

# Show output
print("\n=== Title ===")
print(title)
print("\n=== Content Preview ===")
print(content[:1000])
print("\n=== Next Section Link ===")
print(next_link or "❌ Next Section link not found")

# Save to JSON
os.makedirs("data/sections", exist_ok=True)
timestamp = datetime.now().isoformat()
filename = "data/sections/debug_0000.json"

with open(filename, "w", encoding="utf-8") as f:
    json.dump({
        "title": title,
        "url": url,
        "content": content,
        "scraped_at": timestamp,
        "next_section": next_link
    }, f, ensure_ascii=False, indent=2)

print(f"\n✅ Saved to: {filename}")

# Close browser
driver.quit()
