#!/usr/bin/env python3
"""
Build the website for GitHub Pages by converting published newsletters to HTML
"""

import json
import os
import sys
import shutil
from pathlib import Path

# Import the generator module
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'scripts'))
from generate_newsletter import generate_newsletter_html

def get_newsletter_name(folder_name):
    """Convert folder name like '2026_April_2026' to 'april-2026' """
    parts = folder_name.split('_')
    if len(parts) >= 2:
        month = parts[1].lower()
        year = parts[0]
        return f"{month}-{year}"
    return folder_name.lower()

def resolve_image_paths(content_data, base_folder):
    """
    Recursively resolve relative image paths to GitHub raw content URLs
    """
    github_base = "https://raw.githubusercontent.com/kshamiyah/the-station/main"

    if isinstance(content_data, dict):
        for key, value in content_data.items():
            if key in ('image', 'trace_image', 'trace_image_side', 'barcode_image'):
                if isinstance(value, str) and value and not value.startswith(('http://', 'https://', 'data:')):
                    # Convert relative path to GitHub raw URL
                    resolved_path = (base_folder / value).resolve()
                    if resolved_path.exists():
                        # Get relative path from repo root
                        rel_path = resolved_path.relative_to(Path(__file__).parent)
                        github_url = f"{github_base}/{rel_path}".replace("\\", "/")
                        content_data[key] = github_url
            elif isinstance(value, (dict, list)):
                resolve_image_paths(value, base_folder)
    elif isinstance(content_data, list):
        for item in content_data:
            resolve_image_paths(item, base_folder)

def main():
    published_dir = Path(__file__).parent / "published"
    docs_dir = Path(__file__).parent / "docs"

    print("📰 Building website for GitHub Pages...\n")

    # Find all published newsletters
    newsletter_folders = sorted([d for d in published_dir.iterdir() if d.is_dir()])

    if not newsletter_folders:
        print("❌ No published newsletters found!")
        return

    generated_files = []

    for folder in newsletter_folders:
        content_file = folder / "content.json"

        if not content_file.exists():
            print(f"⊘ Skipped {folder.name} (no content.json)")
            continue

        try:
            # Load content
            with open(content_file, 'r', encoding='utf-8') as f:
                content_data = json.load(f)

            # Resolve relative image paths to absolute paths
            resolve_image_paths(content_data, folder)

            # Generate HTML
            html_content = generate_newsletter_html(content_data)

            # Save to docs folder
            filename = get_newsletter_name(folder.name) + ".html"
            output_file = docs_dir / filename

            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(html_content)

            print(f"✓ Generated {filename}")
            generated_files.append((filename, content_data.get('date_label', folder.name)))

        except Exception as e:
            print(f"✗ Failed to generate {folder.name}: {e}")

    # Update index.html with links to generated newsletters
    if generated_files:
        update_index_page(docs_dir, generated_files)
        print(f"\n✓ Updated index.html with {len(generated_files)} newsletter links")

    print(f"\n✅ Website built successfully!")
    print(f"   Files saved to: docs/")
    print(f"   Ready for GitHub Pages deployment")

def update_index_page(docs_dir, newsletter_files):
    """Update index.html to include links to all newsletters"""

    # Sort by name (reverse chronological)
    newsletter_files.sort(reverse=True)

    newsletter_links = "\n".join([
        f'            <a href="{filename}" class="newsletter-item">{label} Edition</a>'
        for filename, label in newsletter_files
    ])

    html = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>The Station - O&G Newsletter</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 20px;
        }}
        .container {{
            background: white;
            border-radius: 12px;
            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
            max-width: 600px;
            padding: 40px;
            text-align: center;
        }}
        h1 {{
            color: #333;
            margin-bottom: 8px;
            font-size: 2.5em;
        }}
        .tagline {{
            color: #666;
            font-size: 1em;
            font-style: italic;
            margin-bottom: 32px;
            opacity: 0.8;
        }}
        .subtitle {{
            color: #888;
            font-size: 0.95em;
            margin-bottom: 24px;
            font-weight: 500;
        }}
        .newsletter-list {{
            text-align: left;
            margin: 32px 0;
        }}
        .newsletter-item {{
            background: #f5f5f5;
            padding: 16px 20px;
            margin-bottom: 12px;
            border-radius: 8px;
            text-decoration: none;
            color: #667eea;
            font-weight: 500;
            transition: all 0.3s ease;
            display: block;
            border-left: 4px solid #667eea;
        }}
        .newsletter-item:hover {{
            background: #667eea;
            color: white;
            transform: translateX(4px);
            border-left-color: white;
        }}
        .footer {{
            color: #999;
            font-size: 0.9em;
            margin-top: 32px;
            border-top: 1px solid #eee;
            padding-top: 24px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>📰 The Station</h1>
        <div class="tagline">Engaged with the evidence.</div>
        <p class="subtitle">O&G Departmental Educational Newsletter</p>

        <div class="newsletter-list">
{newsletter_links}
        </div>

        <p class="footer">Latest editions of The Station newsletter</p>
    </div>
</body>
</html>'''

    with open(docs_dir / "index.html", 'w', encoding='utf-8') as f:
        f.write(html)

if __name__ == "__main__":
    main()
