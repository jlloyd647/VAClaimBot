import os
import json

TOC_PATH = "data/meta/m21_toc.json"
SECTIONS_ROOT = "data/sections"
OUTPUT_PATH = "data/meta/missing_from_toc.json"

# Load TOC links
with open(TOC_PATH, "r", encoding="utf-8") as f:
    toc_entries = json.load(f)

toc_urls = {entry["url"] for entry in toc_entries}

# Collect scraped URLs
scraped_urls = set()
for root, _, files in os.walk(SECTIONS_ROOT):
    for file in files:
        if file.endswith(".json"):
            path = os.path.join(root, file)
            try:
                with open(path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    if "url" in data:
                        scraped_urls.add(data["url"])
            except Exception as e:
                print(f"❌ Failed to read {path}: {e}")

# Compare and collect missing
missing = [entry for entry in toc_entries if entry["url"] not in scraped_urls]

# Save missing list
os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
    json.dump(missing, f, ensure_ascii=False, indent=2)

print(f"✅ Compared {len(toc_urls)} TOC URLs with {len(scraped_urls)} scraped URLs")
print(f"❌ Missing: {len(missing)} URLs saved to {OUTPUT_PATH}")
