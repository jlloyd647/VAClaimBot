import os, json, requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

# Load all scraped URLs
existing_urls = set()
for root, _, files in os.walk("data/sections"):
    for file in files:
        if file.endswith(".json"):
            with open(os.path.join(root, file), "r", encoding="utf-8") as f:
                try:
                    existing_urls.add(json.load(f).get("url", ""))
                except: pass

# Pull the TOC
toc_url = "https://www.knowva.ebenefits.va.gov/system/templates/selfservice/va_ssnew/help/customer/locale/en-US/portal/554400000001018/content/554400000073398/M21-1-Adjudication-Procedures-Manual-Table-of-Contents"
response = requests.get(toc_url)
soup = BeautifulSoup(response.text, "html.parser")

# Get links
all_links = []
for a in soup.select("a[href]"):
    href = a["href"]
    full_url = urljoin(toc_url, href)
    if "/content/" in full_url and "Table-of-Contents" not in full_url:
        all_links.append((a.get_text(strip=True), full_url))

# Compare
toc_urls = {url for _, url in all_links}
missing = toc_urls - existing_urls

print(f"\n🔍 Missing {len(missing)} sections from your scrape.\n")
for text, url in all_links:
    if url in missing:
        print(f"- {text:60} :: {url}")
