#!/usr/bin/env python3
"""
Generate QR code for The Station GitHub Pages URL
"""

try:
    import qrcode
except ImportError:
    print("❌ qrcode library not installed")
    print("Install with: pip install qrcode[pil]")
    exit(1)

from pathlib import Path

# GitHub Pages URL for The Station newsletter
NEWSLETTER_URL = "https://kshamiyah.github.io/the-station/"

def generate_qr_code(url, output_path):
    """Generate QR code and save as PNG"""
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(url)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")
    img.save(output_path)
    return output_path

if __name__ == "__main__":
    output_file = Path(__file__).parent / "docs" / "newsletter-qr-code.png"

    print(f"📱 Generating QR code for: {NEWSLETTER_URL}")
    generate_qr_code(NEWSLETTER_URL, output_file)
    print(f"✓ QR code saved to: {output_file}")
    print(f"\nYou can now add this QR code to your poster!")
