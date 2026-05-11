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
    """Update index.html to include links to all newsletters with Apple-style design"""

    # Sort chronologically by month
    month_order = {'january': 1, 'february': 2, 'march': 3, 'april': 4, 'may': 5, 'june': 6,
                   'july': 7, 'august': 8, 'september': 9, 'october': 10, 'november': 11, 'december': 12}

    def sort_key(item):
        filename, label = item
        month = label.split()[0].lower()
        return (month_order.get(month, 13), filename)

    newsletter_files.sort(key=sort_key)

    newsletter_links = "\n".join([
        f'''                <a href="{filename}" class="newsletter-item">
                    <div class="item-content">
                        <div class="item-title">{label}</div>
                        <div class="item-meta">Edition</div>
                    </div>
                    <div class="item-arrow">→</div>
                </a>'''
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
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
            background-color: #ffffff;
            color: #1d1d1f;
            line-height: 1.6;
        }}

        .container {{
            max-width: 980px;
            margin: 0 auto;
            padding: 60px 20px;
        }}

        .header {{
            text-align: center;
            margin-bottom: 80px;
        }}

        h1 {{
            font-size: 3.5rem;
            font-weight: 700;
            margin-bottom: 16px;
            letter-spacing: -0.5px;
        }}

        .tagline {{
            font-size: 1.25rem;
            color: #86868b;
            font-weight: 400;
            letter-spacing: 0.3px;
        }}

        .subtitle {{
            font-size: 1rem;
            color: #86868b;
            margin-top: 8px;
            font-weight: 400;
        }}

        .newsletter-section {{
            margin-bottom: 60px;
            display: flex;
            flex-direction: column;
            align-items: center;
        }}

        .section-title {{
            font-size: 1.5rem;
            font-weight: 600;
            margin-bottom: 24px;
            color: #1d1d1f;
            text-align: center;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }}

        .newsletter-list {{
            display: flex;
            flex-direction: column;
            gap: 16px;
            max-width: 540px;
            margin: 0 auto;
            width: 100%;
        }}

        .newsletter-item {{
            background-color: #ffffff;
            border: 1px solid #e5e5e7;
            border-radius: 10px;
            padding: 18px 24px;
            text-decoration: none;
            color: inherit;
            transition: all 0.2s ease;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }}

        .newsletter-item:hover {{
            background-color: #f9f9f9;
            border-color: #d1d1d6;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
        }}

        .newsletter-item:active {{
            transform: scale(0.99);
        }}

        .item-content {{
            text-align: left;
        }}

        .item-title {{
            font-size: 1.1rem;
            font-weight: 600;
            margin-bottom: 4px;
        }}

        .item-meta {{
            font-size: 0.9rem;
            color: #86868b;
        }}

        .item-arrow {{
            color: #d1d1d6;
            font-size: 1.1rem;
            margin-left: 16px;
            flex-shrink: 0;
        }}

        @media (max-width: 640px) {{
            .container {{
                padding: 40px 16px;
            }}

            h1 {{
                font-size: 2rem;
            }}

            .tagline {{
                font-size: 1rem;
            }}

            .newsletter-list {{
                gap: 12px;
                max-width: 100%;
            }}

            .newsletter-item {{
                padding: 16px 16px;
            }}

            .item-title {{
                font-size: 1rem;
            }}

            .item-meta {{
                font-size: 0.85rem;
            }}

            .item-arrow {{
                font-size: 1rem;
                margin-left: 12px;
            }}

            .section-title {{
                font-size: 1.2rem;
            }}
        }}

        .footer {{
            text-align: center;
            padding-top: 60px;
            border-top: 1px solid #e5e5e7;
            margin-top: 60px;
        }}

        .footer-text {{
            font-size: 0.9rem;
            color: #86868b;
        }}

        @media (max-width: 768px) {{
            .container {{
                padding: 40px 16px;
            }}

            h1 {{
                font-size: 2.5rem;
            }}

            .tagline {{
                font-size: 1.1rem;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>The Station</h1>
            <p class="tagline">Engaged with the evidence.</p>
            <p class="subtitle">O&G Departmental Educational Newsletter</p>
        </div>

        <div class="newsletter-section">
            <h2 class="section-title">Latest Editions</h2>
            <div class="newsletter-list">
{newsletter_links}
            </div>
        </div>

        <div class="footer">
            <p class="footer-text">Created and published by Khalid Shamiyah</p>
        </div>
    </div>
</body>
</html>'''

    with open(docs_dir / "index.html", 'w', encoding='utf-8') as f:
        f.write(html)

if __name__ == "__main__":
    main()
