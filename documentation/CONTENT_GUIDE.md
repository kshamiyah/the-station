# Newsletter Content Guide

## How to Update Newsletter Content

Simply edit the `data/newsletter_content.json` file - no coding required!

### File Structure

The JSON file contains all the content for your newsletter. Here's the standard four-section template:

### 1. **date_label**
- The month/year displayed at the top of the newsletter
- Example: `"April 2026"` or `"May 2026"`

### 2. **message_heading** & **message_to_team**
- **message_heading**: Short label for the team message (e.g., "Team Huddle", "Under Pressure")
- **message_to_team**: Departmental message displayed after the header
- Use this for theme introduction, important context, or key messages
- Example: `"Hypertensive disorders of pregnancy remain one of the leading causes of maternal death..."`

### 3. **theme**
- Monthly theme section
- **enabled**: `true` to show, `false` to hide
- **title**: Main theme title
- **intro**: Brief 1–2 sentence introduction

### 4. **ctg_meeting** — Section 1
- CTG case study section
- **week_label**: Badge label (e.g., "CTG MEETING")
- **title**: Case title
- **presented_by**: Presenter's full name
- **background**: Clinical context/patient presentation
- **interpretation**: CTG findings and clinical significance
- **outcome**: What happened to patient/baby
- **learning_point**: Key clinical teaching point (2–3 sentences)
- **trace_image**: Path to CTG trace image (e.g., `"images/CTG April.png"`)
- **trace_caption**: Figure caption for the trace

### 5. **journal_club** — Section 2
- Journal Club section (research paper discussion)
- **week_label**: Badge label (e.g., "JOURNAL CLUB")
- **title**: Full paper title
- **journal**: Journal name and publication year
- **presented_by**: Presenter's full name
- **key_findings**: 1–2 sentences describing the study design
- **key_results**: 2–4 sentences with main findings and numbers
- **take_home**: 1–2 sentences with actionable clinical message
- **paper_link**: URL to the paper (optional)
- **image**: Path to paper figure or supplementary image (optional)
- **image_caption**: Figure caption (optional)

### 6. **guidelines** — Section 3
- Guideline update section
- **week_label**: Badge label (e.g., "GUIDELINES")
- **title**: Full guideline name (e.g., "NICE NG133: Hypertension in Pregnancy")
- **presented_by**: Presenter's full name
- **sections**: Array of guideline sections, each with:
  - **label**: Section heading (e.g., "Definitions", "Prevention & targets")
  - **text**: Content for that section
- **guideline_link**: URL to the full guideline (optional)

### 7. **ai_in_clinical_practice** — Section 4
- AI teaching/tools section
- **week_label**: Badge label (e.g., "AI IN CLINICAL PRACTICE")
- **title**: Topic title
- **presented_by**: Presenter's full name
- **key_points**: Array of key points, each with:
  - **label**: Point heading (e.g., "Set up custom instructions")
  - **detail**: Explanation (1–2 sentences)
- **safety_reminders**: Important safety/ethical reminders (displayed in warning box)

### 8. **historical_fact** (Optional)
- Historical Obs and Gynae perspective
- **title**: Title with era (e.g., "The Urine That Changed Everything — Guy's Hospital, 1843")
- **year**: Year or decade
- **fact**: 3–5 sentence engaging narrative
- **image**: Path to historical image (optional)
- **image_caption**: Image caption
- **reference_link**: URL to PubMed or academic source (optional)
- Leave empty object `{}` to hide

### 9. **schedule** (Optional)
- Schedule table for next month's meetings
- **month**: Month label (e.g., "May 2026")
- **theme_subheading**: Optional subheading describing next month's theme
- **meetings**: Array of meeting objects, each with:
  - **date**: Date (e.g., "May 5")
  - **day**: Day of week (e.g., "Tuesday")
  - **time**: Time (e.g., "08:30–09:00")
  - **event**: Event type (e.g., "CTG", "Journal Club", "Guidelines")
  - **topic**: Topic/presenter name
  - **location**: Location (e.g., "Microsoft Teams")
- Leave empty object `{}` to hide

### 10. **mdt_reminder** (Optional)
- Reminder box for regular meeting details
- **enabled**: `true` to show, `false` to hide
- **day**: Day of week (e.g., "Tuesday")
- **time**: Time (e.g., "08:30–09:00")
- **meeting_link**: Microsoft Teams (or other) meeting link

### 11. **barcode** (Optional)
- QR code or barcode image
- **barcode_image**: Path to QR code image (e.g., `"images/teams_meeting_qr.png"`)

## Image Handling

- Store all images in the `images/` folder
- Reference them with relative paths: `"images/filename.png"`
- The script automatically converts local images to base64 and embeds them in the HTML
- This means the email is self-contained—no broken image links

## Example JSON Structure

```json
{
  "date_label": "April 2026",
  "message_heading": "Under Pressure",
  "message_to_team": "Hypertensive disorders of pregnancy remain...",
  "theme": {
    "enabled": true,
    "title": "Under Pressure",
    "intro": "Hypertensive disorders in pregnancy..."
  },
  "ctg_meeting": {
    "week_label": "CTG MEETING",
    "title": "The Baseline That Was Telling Us Something",
    "presented_by": "Dr Joanna Pawlak",
    "background": "Patient on IOL...",
    "interpretation": "At consultant ward round...",
    "outcome": "Baby delivered in theatre...",
    "learning_point": "A 10% rise in baseline is a red flag...",
    "trace_image": "images/CTG April.png",
    "trace_caption": "Figure 1. CTG trace demonstrating..."
  },
  "journal_club": {
    "week_label": "JOURNAL CLUB",
    "title": "Nifedipine vs Enalapril for Postpartum Hypertension...",
    "journal": "RCT, 2020–2021, tertiary centre, USA",
    "presented_by": "Dr Zachary Chan",
    "key_findings": "Open-label RCT of 94 women...",
    "key_results": "Only a 2% difference...",
    "take_home": "Evidence does not support switching...",
    "paper_link": "https://..."
  },
  "guidelines": {
    "week_label": "GUIDELINES",
    "title": "NICE NG133: Hypertension in Pregnancy",
    "presented_by": "Dr Chloe Unwin",
    "sections": [
      {
        "label": "Definitions",
        "text": "Chronic hypertension (booking or <20 weeks)..."
      }
    ],
    "guideline_link": "https://www.nice.org.uk/guidance/ng133"
  },
  "ai_in_clinical_practice": {
    "week_label": "AI IN CLINICAL PRACTICE",
    "title": "Using AI Better: Four Prompting Habits",
    "presented_by": "Dr Khalid Shamiyah",
    "key_points": [
      {
        "label": "Set up custom instructions",
        "detail": "Tell ChatGPT who you are..."
      }
    ],
    "safety_reminders": "Never share patient-identifiable data..."
  },
  "historical_fact": {
    "title": "The Urine That Changed Everything — Guy's Hospital, 1843",
    "year": 1843,
    "fact": "In 1843, John C. W. Lever...",
    "image": "images/Historical April.png",
    "image_caption": "Figure 2. The title page of...",
    "reference_link": "https://..."
  },
  "schedule": {
    "month": "May 2026",
    "theme_subheading": "May's Theme: Fertility",
    "meetings": [
      {
        "date": "May 5",
        "day": "Tuesday",
        "time": "08:30–09:00",
        "event": "CTG",
        "topic": "By Dr Smith",
        "location": "Microsoft Teams"
      }
    ]
  },
  "mdt_reminder": {
    "enabled": true,
    "day": "Tuesday",
    "time": "08:30–09:00",
    "meeting_link": "https://teams.microsoft.com/..."
  },
  "barcode": {
    "barcode_image": "images/teams_meeting_qr.png"
  }
}
```

## Tips

- **Keep captions brief**: 1–2 sentences max for image captions
- **Numbers in results**: Always include specific figures (percentages, N values, etc.)
- **Actionable messages**: Take-home points should guide clinical practice
- **Tone**: Educational, collegial, third-person factual (except take-home messages, which can be direct)
- **Security**: Never include patient-identifiable information

## Generating the Newsletter

Once you've updated `data/newsletter_content.json`, run:

```bash
cd scripts
python3 generate_newsletter.py
```

Output: `build/newsletter.html`
