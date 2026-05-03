#!/usr/bin/env python3
"""
Convert newsletter.html (or any HTML file) to PDF.
Uses Playwright (Chromium) for high-quality, print-style output. Handles inline styles and base64 images.

Usage:
  pip install playwright && playwright install chromium   # first time only
  python3 html_to_pdf.py                          # uses newsletter.html in current dir
  python3 html_to_pdf.py path/to/newsletter.html  # specific file
  python3 html_to_pdf.py path/to/newsletter.html -o path/to/output.pdf
"""

import argparse
import os
import sys


def main():
    parser = argparse.ArgumentParser(
        description="Convert newsletter HTML to PDF.",
        epilog="Example: python3 html_to_pdf.py archive/2026_January/newsletter.html",
    )
    parser.add_argument(
        "html_file",
        nargs="?",
        default="../build/newsletter.html",
        help="Path to the HTML file (default: ../build/newsletter.html)",
    )
    parser.add_argument(
        "-o", "--output",
        dest="output",
        default=None,
        help="Output PDF path (default: same as HTML with .pdf extension)",
    )
    parser.add_argument(
        "--pages",
        type=int,
        default=4,
        metavar="N",
        help="Fit newsletter to N pages (default: 4). Use 1 for one page, or --multi-page for no scaling.",
    )
    parser.add_argument(
        "--multi-page",
        action="store_true",
        help="No scaling; use natural page breaks (typically 4 pages).",
    )
    args = parser.parse_args()

    html_path = os.path.abspath(args.html_file)
    if not os.path.exists(html_path):
        print(f"❌ File not found: {html_path}")
        return 1

    out_path = args.output
    if not out_path:
        base, _ = os.path.splitext(html_path)
        out_path = base + ".pdf"
    else:
        out_path = os.path.abspath(out_path)

    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print("❌ Playwright is not installed. Install it with:")
        print("   pip install playwright")
        print("   playwright install chromium")
        return 1

    # Use file:// URL so the page loads with correct base for relative resources
    file_url = "file://" + html_path

    print(f"Converting: {html_path}")
    print(f"Output:     {out_path}")

    margin_px = 20
    # A4 at 96dpi: ~794 x 1123 px; content area after margins
    a4_content_w = 794 - 2 * margin_px
    a4_content_h = 1123 - 2 * margin_px
    min_scale = 0.1  # Playwright's minimum

    try:
        with sync_playwright() as p:
            browser = p.chromium.launch()
            # Normal viewport so we measure actual content height (not viewport height)
            page = browser.new_page(viewport={"width": 800, "height": 1200})
            page.goto(file_url, wait_until="networkidle")

            # Keep section cards on one page (no mid-section breaks)
            page.add_style_tag(
                content="""
                    table[style*="border-radius: 12px"][style*="background-color: #ffffff"] {
                        page-break-inside: avoid;
                        break-inside: avoid;
                    }
                """
            )

            # Measure total content size
            dims = page.evaluate(
                """() => {
                    const d = document.documentElement;
                    const b = document.body;
                    return {
                        width: Math.max(d.scrollWidth, b?.scrollWidth || 0, 800),
                        height: Math.max(d.scrollHeight, b?.scrollHeight || 0)
                    };
                }"""
            )
            content_w = dims["width"]
            content_h = dims["height"]

            if args.multi_page:
                scale = 1.0
                print("Using natural page breaks (--multi-page).")
            elif args.pages <= 1:
                # Scale to fit one page
                scale_w = a4_content_w / content_w if content_w > 0 else 1.0
                scale_h = a4_content_h / content_h if content_h > 0 else 1.0
                scale = min(scale_w, scale_h, 1.0) * 0.98
                scale = max(scale, min_scale)
                if scale < min_scale:
                    inject_scale = min(scale_w, scale_h, 1.0) * 0.98
                    page.evaluate(
                        """(s) => {
                            const style = document.createElement('style');
                            style.textContent = `body { transform: scale(${s}); transform-origin: top left; } html { width: ${100/s}%; height: ${100/s}%; }`;
                            document.head.appendChild(style);
                        }""",
                        inject_scale,
                    )
                    scale = 1.0
                    print(f"Content size: {content_w}×{content_h} px → scale {inject_scale:.3f} (1 page).")
                else:
                    print(f"Content size: {content_w}×{content_h} px → scale {scale:.3f} (1 page).")
            else:
                # Scale to fit N pages (default 3)
                target_pages = max(1, args.pages)
                scale_h = (target_pages * a4_content_h) / content_h if content_h > 0 else 1.0
                scale_w = a4_content_w / content_w if content_w > 0 else 1.0
                scale = min(scale_h, scale_w, 1.0) * 0.98
                scale = max(min(scale, 2.0), min_scale)
                print(f"Content size: {content_w}×{content_h} px → scale {scale:.3f} (~{target_pages} pages).")

            page.pdf(
                path=out_path,
                format="A4",
                print_background=True,
                scale=scale,
                margin={"top": f"{margin_px}px", "right": f"{margin_px}px", "bottom": f"{margin_px}px", "left": f"{margin_px}px"},
            )
            browser.close()
    except Exception as e:
        print(f"❌ Error generating PDF: {e}")
        return 1

    print(f"✓ PDF saved: {out_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
