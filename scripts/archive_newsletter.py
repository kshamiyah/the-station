#!/usr/bin/env python3
"""
Archive the current newsletter as a final version.
Creates a dated folder in archive/ containing the HTML, content JSON, and all images used.
Run this after generating the newsletter and before or after sending.
"""

import json
import os
import re
import shutil
from datetime import datetime

ARCHIVE_DIR = "../published"
CONTENT_FILE = "../data/newsletter_content.json"
HTML_FILE = "../build/newsletter.html"


def get_archive_folder_name(data):
    """Derive archive folder name from content, e.g. 2026_January."""
    date_label = (data.get("date_label") or "").strip()
    if not date_label:
        date_label = datetime.now().strftime("%B")  # current month name
    # Try to get year from schedule.month (e.g. "FEBRUARY 2026" -> 2026)
    schedule = data.get("schedule") or {}
    month_str = schedule.get("month") or ""
    match = re.search(r"\d{4}", month_str)
    year = int(match.group(0)) if match else datetime.now().year
    safe_name = date_label.replace(" ", "_")
    return f"{year}_{safe_name}"


def _is_local_path(s):
    """True if s looks like a local file path (not URL/data URI)."""
    if not s or not str(s).strip():
        return False
    s = str(s).strip()
    return not s.startswith(("http://", "https://", "data:"))


def get_image_paths(data):
    """Collect all local image paths from the content (skip URLs)."""
    paths = []
    seen = set()

    def add(p):
        if p and _is_local_path(p) and p not in seen:
            seen.add(p)
            paths.append(p)

    # Barcode / Teams QR
    add((data.get("barcode") or {}).get("barcode_image") or "")

    # Historical fact image
    add((data.get("historical_fact") or {}).get("image") or "")

    # CTG: main trace and side image
    ctg = data.get("ctg") or {}
    add(ctg.get("trace_image") or "")
    add(ctg.get("trace_image_side") or "")

    # Journal club sections (e.g. obs_jc CSE image, gynae_jc if ever used)
    for key in ("gynae_jc", "obs_jc"):
        add((data.get(key) or {}).get("image") or "")

    return paths


def main():
    if not os.path.exists(CONTENT_FILE):
        print(f"❌ {CONTENT_FILE} not found. Run from the project folder.")
        return 1
    if not os.path.exists(HTML_FILE):
        print(f"❌ {HTML_FILE} not found. Run generate_newsletter.py first.")
        return 1

    with open(CONTENT_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    folder_name = get_archive_folder_name(data)
    archive_path = os.path.join(ARCHIVE_DIR, folder_name)
    os.makedirs(archive_path, exist_ok=True)

    # Copy final HTML
    shutil.copy2(HTML_FILE, os.path.join(archive_path, "newsletter.html"))
    print(f"  ✓ newsletter.html → {archive_path}/")

    # Copy content JSON (source data for this edition)
    shutil.copy2(CONTENT_FILE, os.path.join(archive_path, "content.json"))
    print(f"  ✓ content.json → {archive_path}/")

    # Copy images (local files only)
    for path in get_image_paths(data):
        if os.path.exists(path):
            name = os.path.basename(path)
            dest = os.path.join(archive_path, name)
            shutil.copy2(path, dest)
            print(f"  ✓ {path} → {archive_path}/{name}")
        else:
            print(f"  ⚠ Image not found (skipped): {path}")

    print()
    print(f"✓ Archived as: {archive_path}")
    return 0


if __name__ == "__main__":
    print("Archiving current newsletter...")
    print()
    exit(main())
