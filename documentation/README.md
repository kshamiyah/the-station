# Obs and Gynae Newsletter Generator

A simple tool to generate professional, Apple-style newsletters for Obs and Gynae resident updates.

## Quick Start

### Weekly Content Updates

1. **Edit the content file**: Open `data/newsletter_content.json` in any text editor
2. **Update your content**: Change the text, dates, titles, etc. (see `documentation/CONTENT_GUIDE.md` for details)
3. **Generate the newsletter**: Run `python3 scripts/generate_newsletter.py`
4. **Send it**: Run `python3 scripts/send_newsletter.py` (or copy HTML from `build/newsletter.html`)

That's it! No coding required.

## Folder Structure

```
The Station/
├── scripts/                      # Python scripts
│   ├── generate_newsletter.py    # Generates HTML from JSON
│   ├── send_newsletter.py        # Sends newsletter via email
│   ├── archive_newsletter.py     # Archives editions
│   └── html_to_pdf.py            # Converts HTML to PDF
├── data/                         # Newsletter content
│   └── newsletter_content.json   # Edit this to update content
├── build/                        # Generated files (temporary, auto-created)
│   ├── newsletter.html           # Current working version (gets overwritten)
│   └── index.html                # Same as newsletter.html
├── images/                       # Images and media
│   ├── CTG_March.png
│   ├── Redman.png
│   ├── CSE.png
│   └── teams_meeting_qr.png
├── published/                    # Final published versions by month
├── documentation/                # Documentation
│   ├── README.md                 # This file
│   └── CONTENT_GUIDE.md          # How to edit content
├── requirements.txt              # Python dependencies
└── .gitignore                    # Git ignore rules
```

## Workflow

```
Edit data/newsletter_content.json 
  ↓
Run: python3 scripts/generate_newsletter.py
  ↓
Output: build/newsletter.html (created/overwritten)
  ↓
Send: python3 scripts/send_newsletter.py
```

## Archive final versions

To save a final copy of each monthly newsletter (HTML + images + content JSON) in `published/`:

```bash
python3 scripts/generate_newsletter.py   # ensure latest HTML exists
python3 scripts/archive_newsletter.py    # creates published/YYYY_MonthName/ with newsletter.html, content.json, and images
```

See **`published/README.md`** for details.

## PDF version

To generate a PDF from the newsletter HTML (e.g. for printing or sharing):

```bash
pip install playwright && playwright install chromium   # first time only (or: pip install -r requirements.txt)
python3 scripts/html_to_pdf.py                              # uses build/newsletter.html
python3 scripts/html_to_pdf.py published/2026_January/newsletter.html   # from a published folder
```

The PDF is written next to the HTML file (same name, `.pdf` extension). Use `-o path/to/output.pdf` to set a different output path. By default the newsletter is scaled to **fit on 4 pages** (readable size). Use `--pages 1` for one page, `--pages 3` for three, or `--multi-page` for no scaling (natural page breaks).

## Requirements

- Python 3.6+
- No additional packages needed for generate/archive/send (uses standard library only)
- **Playwright** (optional): `pip install playwright` then `playwright install chromium` for PDF export

## Need Help?

See `documentation/CONTENT_GUIDE.md` for detailed instructions on editing the content file.
