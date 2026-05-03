# The Station — O&G Newsletter Generator

A professional, Apple-style monthly newsletter generator for Obstetrics & Gynaecology resident updates.

## Quick Start

### 1. Edit Content
Open `data/newsletter_content.json` and update:
- Date label
- Team message
- Week 1-3 content (AI, Guidelines, Journal Club)
- Historical perspective
- Schedule for next month

See `documentation/CONTENT_GUIDE.md` for detailed field descriptions.

### 2. Add Images
Place image files in `images/` folder and reference them in the JSON:
```json
"image": "../images/your_image.png",
"image_caption": "Figure description"
```

### 3. Generate Newsletter
```bash
cd scripts
python3 generate_newsletter.py
```
Output: `build/newsletter.html`

### 4. Archive Final Version
Once satisfied:
```bash
cd scripts
python3 archive_newsletter.py
```
Saves to: `published/2026_April/` (with all images & content)

### 5. (Optional) Export to PDF
```bash
pip install playwright && playwright install chromium
python3 scripts/html_to_pdf.py
```

## Folder Structure

```
The Station/
├── scripts/                      # Python generation & publishing scripts
│   ├── generate_newsletter.py    # Generates HTML from JSON
│   ├── send_newsletter.py        # Sends via email (Gmail)
│   ├── archive_newsletter.py     # Archives final editions
│   └── html_to_pdf.py            # Converts to PDF
├── data/                         # Newsletter content
│   └── newsletter_content.json   # Edit this file
├── build/                        # Generated files (temporary)
│   ├── newsletter.html
│   └── index.html
├── images/                       # Images & media
├── published/                    # Final archived editions by month
├── documentation/                # Guides & help
│   ├── README.md                 # Main documentation
│   └── CONTENT_GUIDE.md          # Content editing guide
├── requirements.txt              # Python dependencies
└── .gitignore                    # Git ignore rules
```

## Features

✅ **Professional Design** — Apple-style layout with navy blue accents  
✅ **Customizable** — Edit JSON, no coding required  
✅ **Responsive** — Works in email clients  
✅ **Image Support** — CTG traces, historical photos, QR codes  
✅ **Auto-Archive** — Track all published editions  
✅ **PDF Export** — Print-ready versions  

## Requirements

- Python 3.6+
- No additional packages for generate/archive/send (uses standard library)
- **Playwright** (optional): `pip install -r requirements.txt` for PDF export

## Workflow

```
Edit data/newsletter_content.json
         ↓
python3 scripts/generate_newsletter.py
         ↓
Preview build/newsletter.html
         ↓
python3 scripts/send_newsletter.py (optional)
         ↓
python3 scripts/archive_newsletter.py
```

## Content Sections

Each edition includes:

- **Team Huddle** — Departmental announcement
- **Week 1 • AI/Clinical Topic** — Educational feature or case study
- **Week 2 • Guideline** — Updated clinical guidelines
- **Week 3 • Journal Club** — Key research findings
- **Historical Perspective** — O&G history fact with image
- **Schedule** — Next month's meetings
- **MDT Reminder** — Teaching session with Teams link

## Styling

- **Font**: Apple system stack (-apple-system, BlinkMacSystemFont, Segoe UI)
- **Colors**: Navy blue (#003d82) accents on professional gray/black
- **Layout**: Compact, email-optimized
- **Typography**: 14px body text, 24px headings

## Examples

See `published/` folder for past editions with complete content and images.

## Tips

1. **Keep JSON valid** — Use a JSON validator if unsure
2. **Image paths** — Use relative paths like `../images/filename.png`
3. **Special characters** — Quotes and dashes are handled automatically
4. **Line breaks** — Use `\n` in JSON for multi-line text
5. **Links** — Full URLs including `https://`

## Support

For questions about editing: See `documentation/CONTENT_GUIDE.md`

---

Built with ❤️ for the O&G team
