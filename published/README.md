# Newsletter archive

This folder holds the **final version** of each monthly newsletter.

Each edition is stored in a subfolder named `YYYY_MonthName` (e.g. `2026_January`), containing:

- **newsletter.html** – Final HTML (images embedded as base64 for email)
- **content.json** – Source content used for that edition
- **Image files** – Copies of any images used (e.g. `teams_meeting_qr.png`, `incubator.png`)

## How to archive

After generating and finalising a newsletter, run from the project root:

```bash
python3 archive_newsletter.py
```

The script reads `newsletter_content.json` and `newsletter.html`, then creates (or updates) the folder for that edition and copies the HTML, content, and images into it.
