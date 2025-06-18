import os
import json
import re

ROOT_DIR = "data/sections"
INDEX_FILE = "data/section_index.json"

def extract_metadata_from_filename(filepath):
    """
    Example path: data/sections/Part-I/Subpart-ii/Chapter-3/Section-B.json
    Returns: { part: 'I', subpart: 'ii', chapter: '3', section: 'B' }
    """
    parts = filepath.split(os.sep)

    result = {
        "part": None,
        "subpart": None,
        "chapter": None,
        "section": None
    }

    for part in parts:
        if part.startswith("Part-"):
            result["part"] = part.replace("Part-", "")
        elif part.startswith("Subpart-"):
            result["subpart"] = part.replace("Subpart-", "")
        elif part.startswith("Chapter-"):
            result["chapter"] = part.replace("Chapter-", "")
        elif part.endswith(".json") and part.startswith("Section-"):
            result["section"] = part.replace("Section-", "").replace(".json", "")

    return result

def build_index():
    index = []

    for root, _, files in os.walk(ROOT_DIR):
        for file in files:
            if not file.endswith(".json"):
                continue

            filepath = os.path.join(root, file)
            with open(filepath, "r", encoding="utf-8") as f:
                try:
                    data = json.load(f)
                except Exception as e:
                    print(f"❌ Failed to load {filepath}: {e}")
                    continue

            meta = extract_metadata_from_filename(filepath)

            index.append({
                **meta,
                "title": data.get("title", ""),
                "filepath": filepath,
                "url": data.get("url", ""),
                "scraped_at": data.get("scraped_at", ""),
                "external_links": data.get("external_links", [])
            })

    # Save index
    with open(INDEX_FILE, "w", encoding="utf-8") as f:
        json.dump(index, f, ensure_ascii=False, indent=2)

    print(f"✅ Index built with {len(index)} entries: {INDEX_FILE}")

if __name__ == "__main__":
    build_index()
