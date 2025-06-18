import os
import json
import re
from bs4 import BeautifulSoup

SOURCE_DIR = "data/sections"
CHUNK_OUTPUT_DIR = "data/chunks"
os.makedirs(CHUNK_OUTPUT_DIR, exist_ok=True)

def extract_metadata_from_filepath(filepath):
    parts = filepath.split(os.sep)
    meta = {
        "part": None,
        "subpart": None,
        "chapter": None,
        "section": None
    }

    for part in parts:
        if part.startswith("Part-"):
            meta["part"] = part.replace("Part-", "")
        elif part.startswith("Subpart-"):
            meta["subpart"] = part.replace("Subpart-", "")
        elif part.startswith("Chapter-"):
            meta["chapter"] = part.replace("Chapter-", "")
        elif part.startswith("Section-") and part.endswith(".json"):
            meta["section"] = part.replace("Section-", "").replace(".json", "")

    citation_parts = [f"Part {meta['part']}"]
    if meta["subpart"]:
        citation_parts.append(f"Subpart {meta['subpart']}")
    citation_parts.append(f"Chapter {meta['chapter']}")
    citation_parts.append(f"Section {meta['section']}")
    meta["citation"] = ", ".join(citation_parts)

    return meta

def chunk_section(file_path, section_data, meta):
    chunks = []
    html = section_data.get("content_html", "")
    soup = BeautifulSoup(html, "html.parser")

    content_div = soup.select_one("div.article-content")
    if not content_div:
        return []

    parts = str(content_div).split("<hr")
    for i, part_html in enumerate(parts):
        text = BeautifulSoup(part_html, "html.parser").get_text(separator="\n", strip=True)
        if len(text) < 50:
            continue

        chunk = {
            "chunk_id": f"{meta['part']}_{meta['subpart'] or 'none'}_{meta['chapter']}_{meta['section']}_{i+1}",
            "content": text,
            "title": section_data.get("title", ""),
            "citation": meta["citation"],
            "source_url": section_data.get("url", ""),
            "updated": section_data.get("updated", ""),
            "scraped_at": section_data.get("scraped_at", "")
        }
        chunks.append(chunk)

    return chunks

def run_chunking():
    chunk_count = 0
    all_chunks = []

    for root, _, files in os.walk(SOURCE_DIR):
        for file in files:
            if not file.endswith(".json"):
                continue

            path = os.path.join(root, file)
            with open(path, "r", encoding="utf-8") as f:
                try:
                    section_data = json.load(f)
                except Exception as e:
                    print(f"❌ Failed to load {path}: {e}")
                    continue

            meta = extract_metadata_from_filepath(path)
            chunks = chunk_section(path, section_data, meta)
            all_chunks.extend(chunks)

    # Write out all chunks as numbered JSON files
    for i, chunk in enumerate(all_chunks):
        out_path = os.path.join(CHUNK_OUTPUT_DIR, f"{i:04}.json")
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(chunk, f, ensure_ascii=False, indent=2)
        chunk_count += 1

    print(f"\n✅ Chunked {chunk_count} chunks across {len(all_chunks)} sections into {CHUNK_OUTPUT_DIR}")

if __name__ == "__main__":
    run_chunking()
