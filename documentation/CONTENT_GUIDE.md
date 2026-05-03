# Newsletter Content Guide

## How to Update Newsletter Content

Simply edit the `newsletter_content.json` file - no coding required!

### File Structure

The JSON file contains all the content for your newsletter. Here's what each section means:

### 1. **date_label**
- The month/year displayed at the top of the newsletter
- Example: `"OCTOBER 2025"` or `"NOVEMBER 2025"`

### 2. **message_to_team** (Optional)
- Departmental message displayed at the top of the newsletter (right after the header)
- Use this for announcements, updates, or important messages to the team
- Leave empty string `""` or omit to hide this section
- Example: `"Welcome to this month's newsletter! We're excited to share important updates..."`

### 3. **theme**
- Monthly theme section
- **title**: Main theme title
- **intro**: Brief introduction paragraph

### 4. **ctg** - Week 1 Content
- CTG case study section
- **week_label**: Badge label (usually "WEEK 1 • CTG")
- **title**: Case title
- **context**: Patient context/background
- **physiology**: Physiological explanation
- **outcome**: Clinical outcome
- **learning_point**: Key takeaway/clinical pearl
- **trace_image**: URL to CTG image (or leave empty string "" to remove image)

### 5. **gynae_jc** - Week 2 Content
- Gynaecology Journal Club section
- **week_label**: Badge label (usually "WEEK 2 • GYNAE JC")
- **title**: Paper/article title
- **journal**: Journal name and year
- **verdict**: Summary of findings
- **practice_changer**: "Yes" or "No"
- **practice_detail**: What to change in practice

### 6. **guideline** - Week 3 Content
- Guideline update section
- **week_label**: Badge label (usually "WEEK 3 • GUIDELINES")
- **title**: Guideline name
- **old_way**: Previous recommendation
- **new_way**: New recommendation

### 7. **obs_jc** - Week 4 Content
- Obstetrics Journal Club section
- **week_label**: Badge label (usually "WEEK 4 • OBS JC")
- **title**: Paper/article title
- **journal**: Journal name and year
- **verdict**: Summary of findings
- **practice_changer**: "Yes" or "No"
- **practice_detail**: What to change in practice

### 8. **historical_fact** (Optional)
- Historical Obs and Gynae facts section
- **title**: Title of the historical fact (e.g., "The First Successful Cesarean Section")
- **fact**: The historical fact text
- **year**: Year or time period (e.g., "1500")
- Leave empty object `{}` or omit to hide this section

### 9. **schedule** (Optional)
- Schedule table for next month's meetings
- **month**: Month label (e.g., "NOVEMBER 2025")
- **meetings**: Array of meeting objects, each with:
  - **date**: Date (e.g., "Nov 5")
  - **day**: Day of week (e.g., "Tuesday")
  - **time**: Time (e.g., "7:00 AM")
  - **event**: Event type (e.g., "Grand Rounds", "Journal Club")
  - **topic**: Topic/title of the meeting
  - **location**: Location/room
- Leave empty object `{}` or omit to hide this section

## Editing Tips

1. **Keep JSON syntax correct**: Make sure all strings are in quotes and commas are in the right places
2. **Remove image**: Set `"trace_image": ""` to remove the CTG image
3. **Special characters**: Use quotes normally - the system handles them automatically
4. **Line breaks**: Keep text on single lines or use `\n` for line breaks if needed

## After Editing

1. Save the `newsletter_content.json` file
2. Run: `python3 generate_newsletter.py`
3. The updated newsletter will be in `newsletter.html`

## Example Update

To change the date and theme for November:

```json
{
  "date_label": "NOVEMBER 2025",
  "theme": {
    "title": "Gestational Diabetes Management",
    "intro": "This month we explore the latest evidence on GDM screening and management protocols."
  },
  ...
}
```

That's it! No code changes needed.
