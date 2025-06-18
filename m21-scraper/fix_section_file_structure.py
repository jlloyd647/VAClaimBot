import os
import json
import re
import shutil

UNORGANIZED_DIR = "data/sections"

# Walk the base folder and collect misfiled top-level JSONs
for filename in os.listdir(UNORGANIZED_DIR):
    if not filename.endswith(".json") or os.path.isdir(os.path.join(UNORGANIZED_DIR, filename)):
        continue

    full_path = os.path.join(UNORGANIZED_DIR, filename)

    with open(full_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    title = data.get("title", "")

    # Match full structure (Part, Subpart, Chapter, Section)
    pattern_full = r"Part\s+([IVXLC]+),\s+Subpart\s+([ivxlc]+),\s+Chapter\s+(\d+)(?:,\s+Section\s+([A-Z]+))?"
    # Match partial structure (Part, Chapter)
    pattern_partial = r"Part\s+([IVXLC]+),\s+Chapter\s+(\d+)(?:\s+-|$)"

    match = re.search(pattern_full, title)
    if match:
        part, subpart, chapter, section = match.groups()
        folder_parts = [f"Part-{part}", f"Subpart-{subpart}", f"Chapter-{chapter}"]
        dest_folder = os.path.join(UNORGANIZED_DIR, *folder_parts)
        os.makedirs(dest_folder, exist_ok=True)

        if section:
            dest_filename = f"Section-{section}.json"
        else:
            dest_filename = f"_overview.json"

    else:
        match = re.search(pattern_partial, title)
        if match:
            part, chapter = match.groups()
            folder_parts = [f"Part-{part}", f"Chapter-{chapter}"]
            dest_folder = os.path.join(UNORGANIZED_DIR, *folder_parts)
            os.makedirs(dest_folder, exist_ok=True)
            dest_filename = f"_overview.json"

        elif "Prologue" in title:
            dest_folder = os.path.join(UNORGANIZED_DIR, "Prologue")
            os.makedirs(dest_folder, exist_ok=True)
            dest_filename = "_prologue.json"

        else:
            print(f"❌ Could not parse: {filename} | {title}")
            continue

    dest_path = os.path.join(dest_folder, dest_filename)
    shutil.move(full_path, dest_path)
    print(f"✅ Moved: {filename} → {dest_path}")
