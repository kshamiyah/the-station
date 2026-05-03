#!/usr/bin/env python3
"""
Obs and Gynae Resident Review Newsletter Generator v2.0
Improved Apple-Editorial Design
"""

import base64
import json
import os
import sys

# ==========================================
# 📝 LOAD CONTENT FROM JSON FILE
# ==========================================

def load_newsletter_content(content_file="../data/newsletter_content.json"):
    """
    Load newsletter content from JSON file.
    Returns the content dictionary or exits with error message.
    """
    if not os.path.exists(content_file):
        print(f"❌ Error: Content file '{content_file}' not found!")
        print(f"\nPlease create '{content_file}' with your newsletter content.")
        print("See CONTENT_GUIDE.md for instructions.")
        sys.exit(1)
    
    try:
        with open(content_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        print(f"✓ Loaded content from {content_file}")
        return data
    except json.JSONDecodeError as e:
        print(f"❌ Error: Invalid JSON in '{content_file}'")
        print(f"   {e}")
        print("\nPlease check your JSON syntax. Make sure:")
        print("  - All strings are in quotes")
        print("  - Commas are between items (not after the last item)")
        print("  - All brackets are properly closed")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error reading '{content_file}': {e}")
        sys.exit(1)

# ==========================================
# 🎨 LAYOUT ENGINE
# ==========================================

def escape_html(text):
    if not text: return ""
    return str(text).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;").replace("'", "&#39;")

def escape_html_with_br(text):
    """Escape HTML and convert newlines to <br> for multi-paragraph content."""
    if not text: return ""
    return escape_html(text).replace("\n", "<br>\n")

def image_to_src(value):
    """If value is a local file path, return data URI (base64). Otherwise return value (URL)."""
    if not value or not str(value).strip():
        return ""
    value = str(value).strip()
    if value.startswith(("http://", "https://", "data:")):
        return value
    if not os.path.exists(value):
        return value
    try:
        with open(value, "rb") as f:
            raw = f.read()
        b64 = base64.b64encode(raw).decode("ascii")
        ext = os.path.splitext(value)[1].lower()
        mime = "image/png" if ext == ".png" else "image/jpeg" if ext in (".jpg", ".jpeg") else "image/png"
        return f"data:{mime};base64,{b64}"
    except Exception:
        return value

def get_common_styles():
    return {
        "font_stack": "-apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif",
        "text_primary": "#1d1d1f",
        "text_secondary": "#86868b",
        "accent_blue": "#0066cc",
        "navy_blue": "#003d82",
        "card_shadow": "0 8px 30px rgba(0,0,0,0.04)"
    }

STYLE = get_common_styles()

def generate_header(date_label):
    return f"""
    <table width="100%" cellpadding="0" cellspacing="0" border="0" style="margin-bottom: 48px;">
        <tr>
            <td style="text-align: center;">
                <div style="background-color: #f9f9f9; border-radius: 12px; padding: 32px 40px; margin-bottom: 0;">
                    <div style="font-family: {STYLE['font_stack']}; font-size: 48px; font-weight: 700; color: {STYLE['text_primary']}; letter-spacing: -1px; line-height: 1.05; margin-bottom: 16px;">
                        <span style="color: #d1d1d6; font-weight: 300;">—</span>&nbsp;&nbsp;The Station&nbsp;&nbsp;<span style="color: #d1d1d6; font-weight: 300;">—</span>
                    </div>
                    <div style="font-family: Georgia, 'Times New Roman', Times, serif; font-size: 20px; font-weight: 400; color: #424245; font-style: italic; letter-spacing: 0.3px; margin-bottom: 16px;">
                        Engaged with the evidence.
                    </div>
                    <div style="font-family: {STYLE['font_stack']}; font-size: 12px; font-weight: 500; color: {STYLE['text_secondary']}; letter-spacing: 1.5px;">
                        {escape_html(str(date_label).capitalize())}'s Edition
                    </div>
                </div>
            </td>
        </tr>
    </table>"""

def generate_message_to_team(message, heading=None):
    """Team Huddle / message to team section (no avatar). Uses heading as badge label when provided."""
    if not message or message.strip() == "":
        return ""
    heading_text = (heading or "").strip()
    badge_label = heading_text or "Team Huddle"
    return f"""
    <table width="100%" cellpadding="0" cellspacing="0" border="0" style="margin-bottom: 32px; background-color: #ffffff; border-radius: 12px; border: 1px solid #e5e5e7;">
        <tr>
            <td style="padding: 28px; border-left: 3px solid {STYLE['navy_blue']};">
                {generate_badge(badge_label)}
                <div style="font-family: {STYLE['font_stack']}; font-size: 14px; color: #1d1d1f; line-height: 1.6;">
                    {escape_html(message)}
                </div>
            </td>
        </tr>
    </table>"""

def generate_theme_section(theme_data):
    """Theme section in a card box with subtle left border."""
    theme_label = theme_data.get('label', 'Monthly Theme')
    return f"""
    <table width="100%" cellpadding="0" cellspacing="0" border="0" style="margin-bottom: 32px; background-color: #ffffff; border-radius: 12px; border: 1px solid #e5e5e7;">
        <tr>
            <td style="padding: 28px; border-left: 3px solid {STYLE['navy_blue']};">
                <div style="font-family: {STYLE['font_stack']}; font-size: 24px; font-weight: 700; color: {STYLE['text_primary']}; margin-bottom: 12px; letter-spacing: -0.5px;">
                    {escape_html(theme_label)}: {escape_html(theme_data['title'])}
                </div>
                <div style="font-family: {STYLE['font_stack']}; font-size: 14px; font-weight: 400; color: #424245; line-height: 1.6;">
                    {escape_html(theme_data['intro'])}
                </div>
            </td>
        </tr>
    </table>"""

def generate_card_wrapper(content):
    """Wraps content in minimal card style with thin border"""
    return f"""
    <table width="100%" cellpadding="0" cellspacing="0" border="0" style="margin-bottom: 32px; background-color: #ffffff; border-radius: 12px; border: 1px solid #e5e5e7;">
        <tr>
            <td style="padding: 28px;">
                {content}
            </td>
        </tr>
    </table>"""

def generate_badge(label):
    return f"""
    <div style="margin-bottom: 16px;">
        <span style="color: {STYLE['navy_blue']}; font-family: {STYLE['font_stack']}; font-size: 13px; font-weight: 500; letter-spacing: 1px; text-transform: uppercase;">
            {escape_html(label)}
        </span>
    </div>"""

def generate_meta_row(journal=None, presented_by=None):
    """Compact one-line metadata row (journal • presented by)."""
    journal = (journal or "").strip()
    presented_by = (presented_by or "").strip()
    if not journal and not presented_by:
        return ""

    # Keep this email-safe: simple spans, no flex/grid.
    parts = []
    if journal:
        parts.append(f'<span style="font-weight: 600;">{escape_html(journal)}</span>')
    if journal and presented_by:
        parts.append('<span style="padding: 0 8px; color: #d1d1d6;">•</span>')
    if presented_by:
        parts.append(f'<span>Presented by <span style="font-weight: 600; color: {STYLE["text_primary"]};">{escape_html(presented_by)}</span></span>')

    return f"""
    <div style="font-family: {STYLE['font_stack']}; font-size: 12px; color: {STYLE['text_secondary']}; letter-spacing: 0.3px; line-height: 1.35;">
        {''.join(parts)}
    </div>"""

def generate_title_meta_block(title, journal=None, presented_by=None):
    """Shaded header block containing the title + a divider + the metadata row."""
    meta = generate_meta_row(journal, presented_by)
    # If there's no meta, fall back to just the title (unshaded) so we don't add empty UI.
    if not meta:
        return f"""
    <div style="font-family: {STYLE['font_stack']}; font-size: 24px; font-weight: 600; color: {STYLE['text_primary']}; margin-bottom: 8px; margin-top: 4px; letter-spacing: -0.3px; line-height: 1.2;">
        {escape_html(title)}
    </div>"""

    return f"""
    <div style="margin-bottom: 20px;">
        <div style="background-color: #f9f9f9; border-radius: 8px; padding: 16px;">
            <div style="font-family: {STYLE['font_stack']}; font-size: 24px; font-weight: 600; color: {STYLE['text_primary']}; letter-spacing: -0.3px; line-height: 1.2;">
                {escape_html(title)}
            </div>
            <div style="border-top: 1px solid #e5e5e7; margin: 12px 0;"></div>
            {meta}
        </div>
    </div>"""

def generate_shaded_header_block(title, meta_text=None, title_size_px=24):
    """Shaded header block for non-JC sections (title + divider + optional meta text)."""
    meta_text = (meta_text or "").strip()
    if not meta_text:
        return f"""
    <div style="font-family: {STYLE['font_stack']}; font-size: {int(title_size_px)}px; font-weight: 600; color: {STYLE['text_primary']}; margin-bottom: 12px; letter-spacing: -0.3px; line-height: 1.2;">
        {escape_html(title)}
    </div>"""

    return f"""
    <div style="margin-bottom: 20px;">
        <div style="background-color: #f9f9f9; border-radius: 8px; padding: 16px;">
            <div style="font-family: {STYLE['font_stack']}; font-size: {int(title_size_px)}px; font-weight: 600; color: {STYLE['text_primary']}; letter-spacing: -0.3px; line-height: 1.2;">
                {escape_html(title)}
            </div>
            <div style="border-top: 1px solid #e5e5e7; margin: 12px 0;"></div>
            <div style="font-family: {STYLE['font_stack']}; font-size: 12px; color: {STYLE['text_secondary']}; letter-spacing: 0.3px; line-height: 1.4;">
                {escape_html(meta_text)}
            </div>
        </div>
    </div>"""

def generate_button(link, text="Link to paper"):
    """Generate a minimal text link"""
    if not link:
        return ""
    return f"""
    <div style="margin-top: 20px; padding-top: 20px; border-top: 1px solid #e5e5e7;">
        <a href="{escape_html(link)}" style="color: {STYLE['text_secondary']}; font-family: {STYLE['font_stack']}; font-size: 14px; font-weight: 500; text-decoration: underline; text-underline-offset: 3px;">
            {escape_html(text)} ↗
        </a>
    </div>"""

def generate_ctg_section(data):
    no_meeting = data.get('no_meeting', False)
    if no_meeting:
        pearl = (data.get('learning_point') or '').strip()
        pearl_block = f"""
    <div style="background-color: #f5f5f7; border-radius: 6px; padding: 12px; margin-top: 12px;">
        <strong style="font-family: {STYLE['font_stack']}; font-size: 12px; color: {STYLE['accent_blue']}; display: block; margin-bottom: 3px;">💡 CLINICAL PEARL</strong>
        <span style="font-family: {STYLE['font_stack']}; font-size: 14px; color: {STYLE['text_primary']}; line-height: 1.4;">{escape_html(pearl)}</span>
    </div>
    """ if pearl else ""
        content = f"""
    {generate_badge(data['week_label'])}
    
    <div style="font-family: {STYLE['font_stack']}; font-size: 24px; font-weight: 700; color: {STYLE['text_primary']}; margin-bottom: 6px; margin-top: 4px; letter-spacing: -0.5px; line-height: 1.2;">
        {escape_html(data['title'])}
    </div>

    {pearl_block}
    """
    else:
        # Clinical Pearl body: learning point only (Fig. 2 caption appears under the image)
        pearl_body = escape_html((data.get("learning_point") or "").strip())

        # Custom labels (support both defaults and custom labels like "WHAT IS IT", "WHAT CAN IT DO", etc.)
        label_1 = (data.get('label_background') or 'BACKGROUND').strip()
        label_2 = (data.get('label_interpretation') or 'INTERPRETATION').strip()
        label_3 = (data.get('label_outcome') or 'OUTCOME').strip()

        # Content table – customizable labels with fallback to defaults
        content_table = f"""
    <table width="100%" cellpadding="0" cellspacing="0" border="0">
        <tr>
            <td width="25%" style="font-family: {STYLE['font_stack']}; font-size: 12px; font-weight: 600; color: {STYLE['text_secondary']}; padding-bottom: 10px; vertical-align: top;">{escape_html(label_1)}</td>
            <td style="font-family: {STYLE['font_stack']}; font-size: 14px; color: {STYLE['text_primary']}; padding-bottom: 10px; line-height: 1.5;">{escape_html(data.get('background', data.get('context', '')))}</td>
        </tr>
        <tr>
            <td style="font-family: {STYLE['font_stack']}; font-size: 12px; font-weight: 600; color: {STYLE['text_secondary']}; padding-bottom: 10px; vertical-align: top;">{escape_html(label_2)}</td>
            <td style="font-family: {STYLE['font_stack']}; font-size: 14px; color: {STYLE['text_primary']}; padding-bottom: 10px; line-height: 1.5;">{escape_html(data.get('interpretation', data.get('physiology', '')))}</td>
        </tr>
        <tr>
            <td style="font-family: {STYLE['font_stack']}; font-size: 12px; font-weight: 600; color: {STYLE['text_secondary']}; padding-bottom: 10px; vertical-align: top;">{escape_html(label_3)}</td>
            <td style="font-family: {STYLE['font_stack']}; font-size: 14px; color: {STYLE['text_primary']}; padding-bottom: 10px; line-height: 1.5;">{escape_html(data['outcome'])}</td>
        </tr>
        <tr>
            <td colspan="2" style="padding-top: 8px; padding-bottom: 12px;">
                <div style="background-color: #f5f5f7; border-radius: 6px; padding: 12px;">
                    <strong style="font-family: {STYLE['font_stack']}; font-size: 12px; color: {STYLE['accent_blue']}; display: block; margin-bottom: 3px;">💡 CLINICAL PEARL</strong>
                    <span style="font-family: {STYLE['font_stack']}; font-size: 14px; color: {STYLE['text_primary']}; line-height: 1.4;">{pearl_body}</span>
                </div>
            </td>
        </tr>
    </table>"""

        # Badge, title, content table (full width)
        content = f"""
    {generate_badge(data['week_label'])}
    {generate_title_meta_block(data['title'], None, data.get('presented_by', ''))}
    {content_table}
    """

        # Images row: CTG trace and optional side image, same height; short figure labels only (long caption is in Clinical Pearl)
        trace_src = image_to_src(data.get("trace_image") or "") if data.get("trace_image") else ""
        side_src = image_to_src(data.get("trace_image_side") or "") if data.get("trace_image_side") else ""
        trace_cap = escape_html((data.get("trace_caption") or "Fig. 1. CTG trace").strip())
        side_cap_short = escape_html((data.get("trace_side_caption") or "Fig. 2").strip())
        img_height = "200px"  # same height for both
        img_style = f"width: 100%; height: {img_height}; object-fit: contain; border-radius: 6px; display: block; background: #f9f9f9;"
        if trace_src and side_src:
            images_block = f"""
    <table width="100%" cellpadding="0" cellspacing="0" border="0" style="margin-top: 12px;">
        <tr>
            <td style="vertical-align: top; padding-right: 16px;">
                <figure style="margin: 0;">
                    <img src="{escape_html(trace_src)}" style="{img_style}" alt="" />
                    <figcaption style="font-family: {STYLE['font_stack']}; font-size: 11px; color: {STYLE['text_secondary']}; margin-top: 4px; line-height: 1.3;">{trace_cap}</figcaption>
                </figure>
            </td>
            <td style="vertical-align: top; width: 200px;">
                <figure style="margin: 0;">
                    <img src="{escape_html(side_src)}" style="max-width: 180px; width: 100%; height: {img_height}; object-fit: contain; border-radius: 6px; display: block; background: #f9f9f9;" alt="" />
                    <figcaption style="font-family: {STYLE['font_stack']}; font-size: 11px; color: {STYLE['text_secondary']}; margin-top: 4px; line-height: 1.3;">{side_cap_short}</figcaption>
                </figure>
            </td>
        </tr>
    </table>"""
        elif trace_src:
            images_block = f"""
    <figure style="margin: 12px 0 0 0;">
        <img src="{escape_html(trace_src)}" style="width: 100%; height: {img_height}; object-fit: contain; border-radius: 6px; display: block; background: #f9f9f9;" alt="" />
        <figcaption style="font-family: {STYLE['font_stack']}; font-size: 11px; color: {STYLE['text_secondary']}; margin-top: 4px; line-height: 1.3;">{trace_cap}</figcaption>
    </figure>"""
        elif side_src:
            images_block = f"""
    <figure style="margin: 12px 0 0 0;">
        <img src="{escape_html(side_src)}" style="max-width: 180px; height: {img_height}; object-fit: contain; border-radius: 6px; display: block; background: #f9f9f9;" alt="" />
        <figcaption style="font-family: {STYLE['font_stack']}; font-size: 11px; color: {STYLE['text_secondary']}; margin-top: 4px; line-height: 1.3;">{side_cap_short}</figcaption>
    </figure>"""
        else:
            images_block = ""

        # Optional link button
        link_button = generate_button(data.get('link', ''), data.get('link_text', 'Learn more')) if data.get('link') else ""

        content = content + f"""
    {images_block}
    {link_button}
    """
    return generate_card_wrapper(content)

def generate_jc_section(data):
    content = f"""
    {generate_badge(data['week_label'])}
    
    {generate_title_meta_block(data['title'], data.get('journal', ''), data.get('presented_by', ''))}

    <table width="100%" cellpadding="0" cellspacing="0" border="0">
        <tr>
            <td width="25%" style="font-family: {STYLE['font_stack']}; font-size: 12px; font-weight: 600; color: {STYLE['text_secondary']}; padding-bottom: 10px; vertical-align: top;">{escape_html(data.get('label_findings', 'KEY FINDINGS'))}</td>
            <td style="font-family: {STYLE['font_stack']}; font-size: 14px; color: {STYLE['text_primary']}; padding-bottom: 10px; line-height: 1.5;">{escape_html_with_br(data.get('key_findings', data.get('verdict', '')))}</td>
        </tr>
        <tr>
            <td style="font-family: {STYLE['font_stack']}; font-size: 12px; font-weight: 600; color: {STYLE['text_secondary']}; padding-bottom: 10px; vertical-align: top;">{escape_html(data.get('label_results', 'KEY RESULTS'))}</td>
            <td style="font-family: {STYLE['font_stack']}; font-size: 14px; color: {STYLE['text_primary']}; padding-bottom: 10px; line-height: 1.5;">{escape_html_with_br(data.get('key_results', ''))}</td>
        </tr>
        <tr>
            <td style="font-family: {STYLE['font_stack']}; font-size: 12px; font-weight: 600; color: {STYLE['text_secondary']}; padding-bottom: 10px; vertical-align: top;">{escape_html(data.get('label_take_home', 'TAKE HOME'))}</td>
            <td style="font-family: {STYLE['font_stack']}; font-size: 14px; color: {STYLE['text_primary']}; padding-bottom: 10px; line-height: 1.5;">{escape_html_with_br(data.get('take_home', data.get('practice_detail', '')))}</td>
        </tr>
    </table>
    
    {f'<div style="margin-bottom: 16px;"><img src="{escape_html(image_to_src(data.get("image") or ""))}" style="max-width: 100%; width: 100%; height: auto; border-radius: 6px; display: block;" alt="" />' + (f'<div style="font-family: {STYLE["font_stack"]}; font-size: 11px; color: {STYLE["text_secondary"]}; margin-top: 6px; line-height: 1.3;">{escape_html((data.get("image_caption") or "").strip())}</div>' if (data.get("image_caption") or "").strip() else '') + '</div>' if data.get('image') and image_to_src(data.get('image') or '') else ''}
    {generate_button(data.get('paper_link', ''), 'Link to paper')}
    """
    return generate_card_wrapper(content)

def generate_guideline_section(data):
    # If structured sections are provided, render them like JC rows (label on left, text on right).
    sections = data.get('sections')
    if isinstance(sections, list) and sections:
        rows = []
        for s in sections:
            label = (s or {}).get('label', '')
            text = (s or {}).get('text', '')
            if not (str(label).strip() or str(text).strip()):
                continue
            # Table layout keeps the body text aligned in its own column (so wraps don't fall under the heading).
            rows.append(f"""
        <tr>
            <td width="25%" style="font-family: {STYLE['font_stack']}; font-size: 12px; font-weight: 600; color: {STYLE['text_secondary']}; padding-bottom: 10px; vertical-align: top;">
                {escape_html_with_br(label)}:
            </td>
            <td style="font-family: {STYLE['font_stack']}; font-size: 14px; color: {STYLE['text_primary']}; padding-bottom: 10px; line-height: 1.5;">
                {escape_html_with_br(text)}
            </td>
        </tr>""")

        content = f"""
    {generate_badge(data['week_label'])}
    
    {generate_title_meta_block(data['title'], data.get('journal', ''), data.get('presented_by', ''))}

    <table width="100%" cellpadding="0" cellspacing="0" border="0">
        {''.join(rows)}
    </table>
    
    {generate_button(data.get('guideline_link', ''), 'Link to guideline')}
    """
        return generate_card_wrapper(content)

    summary_text = data.get('summary', '')
    if '\n' in summary_text:
        lines = [s.strip() for s in summary_text.split('\n') if s.strip()]
        parts = []
        current_bullets = []
        for line in lines:
            if line.startswith('## '):
                if current_bullets:
                    parts.append(f'<ul style="margin: 0 0 16px 0; padding-left: 20px; font-family: {STYLE["font_stack"]}; font-size: 14px; color: {STYLE["text_primary"]}; line-height: 1.6;">' + ''.join(f'<li style="margin-bottom: 8px;">{escape_html(b)}</li>' for b in current_bullets) + '</ul>')
                    current_bullets = []
                parts.append(f'<div style="font-family: {STYLE["font_stack"]}; font-size: 14px; font-weight: 700; color: {STYLE["text_primary"]}; margin-top: 16px; margin-bottom: 8px;">{escape_html(line[3:].strip())}</div>')
            else:
                current_bullets.append(line)
        if current_bullets:
            parts.append(f'<ul style="margin: 0 0 16px 0; padding-left: 20px; font-family: {STYLE["font_stack"]}; font-size: 14px; color: {STYLE["text_primary"]}; line-height: 1.6;">' + ''.join(f'<li style="margin-bottom: 8px;">{escape_html(b)}</li>' for b in current_bullets) + '</ul>')
        summary_html = ''.join(parts)
    else:
        summary_html = f'<div style="font-family: {STYLE["font_stack"]}; font-size: 14px; color: {STYLE["text_primary"]}; line-height: 1.6; margin-bottom: 16px;">{escape_html(summary_text)}</div>'
    content = f"""
    {generate_badge(data['week_label'])}
    
    <div style="font-family: {STYLE['font_stack']}; font-size: 24px; font-weight: 700; color: {STYLE['text_primary']}; margin-bottom: 6px; margin-top: 4px; letter-spacing: -0.5px; line-height: 1.2;">
        {escape_html(data['title'])}
    </div>
    <div style="font-family: {STYLE['font_stack']}; font-size: 13px; color: {STYLE['text_secondary']}; margin-bottom: 20px; font-style: italic;">
        Presented by: {escape_html(data.get('presented_by', ''))}
    </div>

    {summary_html}
    
    {generate_button(data.get('guideline_link', ''), 'Link to guideline')}
    """
    return generate_card_wrapper(content)

def generate_historical_fact_section(data):
    """Historical Obs and Gynae facts section. Optional image shown to the right of the text."""
    if not data or not data.get('fact'):
        return ""

    image_url = data.get('image', '')
    image_src = image_to_src(image_url)
    image_caption = data.get('image_caption', '')
    caption_html = f'<div style="font-family: {STYLE["font_stack"]}; font-size: 11px; color: {STYLE["text_secondary"]}; line-height: 1.4; margin-top: 8px; font-style: italic;">{escape_html(image_caption)}</div>' if image_caption else ''
    image_cell = f'<td width="160" style="vertical-align: top; padding-left: 20px;"><img src="{escape_html(image_src)}" alt="Historical illustration" style="max-width: 160px; width: 100%; height: auto; border-radius: 8px; display: block;" />{caption_html}</td>' if image_src else ''

    # Header on its own row, then fact text and image side by side
    header_html = generate_shaded_header_block(data.get('title', 'Did You Know?'), data.get('year', ''), 24)
    fact_html = f"""
                <div style="font-family: {STYLE['font_stack']}; font-size: 14px; color: {STYLE['text_primary']}; line-height: 1.6;">
                    {escape_html_with_br(data['fact'])}
                </div>
    
                {generate_button(data.get('reference_link', ''), 'View on PubMed')}
    """

    content = f"""
    {generate_badge("Historical Perspective")}
    
    <table width="100%" cellpadding="0" cellspacing="0" border="0">
        <tr>
            <td colspan="2" style="vertical-align: top;">
                {header_html}
            </td>
        </tr>
        <tr>
            <td style="vertical-align: top;">
                {fact_html}
            </td>
            {image_cell}
        </tr>
    </table>
    """
    return generate_card_wrapper(content)

def generate_schedule_table(data):
    """Schedule of meetings for next month"""
    if not data or not data.get('meetings') or len(data['meetings']) == 0:
        return ""
    
    month = data.get('month', 'Next Month')
    theme_subheading = (data.get('theme_subheading') or '').strip()
    theme_block = f'<div style="font-family: {STYLE["font_stack"]}; font-size: 14px; font-weight: 600; color: {STYLE["text_secondary"]}; margin-bottom: 16px; letter-spacing: -0.2px;">{escape_html(theme_subheading)}</div>' if theme_subheading else ''
    
    # Build table rows
    rows = ""
    for meeting in data['meetings']:
        rows += f"""
        <tr style="border-bottom: 1px solid #e5e5e7;">
            <td style="padding: 10px 6px 10px 10px; font-family: {STYLE['font_stack']}; font-size: 14px; font-weight: 600; color: {STYLE['text_primary']}; vertical-align: top; width: 72px; line-height: 1.3;">
                {escape_html(meeting.get('date', ''))}<br>
                <span style="font-size: 10px; font-weight: 400; color: #86868b;">{escape_html(meeting.get('day', ''))}</span>
            </td>
            <td style="padding: 10px 6px; font-family: {STYLE['font_stack']}; font-size: 13px; color: {STYLE['text_secondary']}; vertical-align: top; white-space: nowrap; width: 75px;">
                {escape_html(meeting.get('time', ''))}
            </td>
            <td style="padding: 10px 6px; font-family: {STYLE['font_stack']}; font-size: 14px; font-weight: 600; color: {STYLE['text_primary']}; vertical-align: top; width: 85px;">
                {escape_html(meeting.get('event', ''))}
            </td>
            <td style="padding: 10px 10px; font-family: {STYLE['font_stack']}; font-size: 13px; color: {STYLE['text_primary']}; vertical-align: top; min-width: 200px; width: 38%;">
                {escape_html(meeting.get('topic', ''))}
            </td>
            <td style="padding: 10px 10px; font-family: {STYLE['font_stack']}; font-size: 12px; color: {STYLE['text_secondary']}; vertical-align: top;">
                {escape_html(meeting.get('location', ''))}
            </td>
        </tr>"""
    
    content = f"""
    {generate_badge(f"{month} Schedule")}

    <div style="font-family: {STYLE['font_stack']}; font-size: 18px; font-weight: 600; color: {STYLE['text_primary']}; margin-bottom: 8px; letter-spacing: -0.3px;">
        Upcoming Meetings
    </div>
    {theme_block}
    <table width="100%" cellpadding="0" cellspacing="0" border="0" style="border-collapse: collapse;">
        <thead>
            <tr style="background-color: #f5f5f7; border-bottom: 2px solid #d1d1d6;">
                <th style="padding: 8px 6px 8px 10px; text-align: left; font-family: {STYLE['font_stack']}; font-size: 11px; font-weight: 700; color: {STYLE['text_secondary']}; text-transform: uppercase; letter-spacing: 0.5px; width: 72px;">Date</th>
                <th style="padding: 10px 6px; text-align: left; font-family: {STYLE['font_stack']}; font-size: 11px; font-weight: 700; color: {STYLE['text_secondary']}; text-transform: uppercase; letter-spacing: 0.5px; white-space: nowrap; width: 75px;">Time</th>
                <th style="padding: 10px 6px; text-align: left; font-family: {STYLE['font_stack']}; font-size: 11px; font-weight: 700; color: {STYLE['text_secondary']}; text-transform: uppercase; letter-spacing: 0.5px; width: 85px;">Event</th>
                <th style="padding: 10px; text-align: left; font-family: {STYLE['font_stack']}; font-size: 11px; font-weight: 700; color: {STYLE['text_secondary']}; text-transform: uppercase; letter-spacing: 0.5px; min-width: 200px; width: 38%;">Topic</th>
                <th style="padding: 10px; text-align: left; font-family: {STYLE['font_stack']}; font-size: 11px; font-weight: 700; color: {STYLE['text_secondary']}; text-transform: uppercase; letter-spacing: 0.5px;">Location</th>
            </tr>
        </thead>
        <tbody>
            {rows}
        </tbody>
    </table>
    """
    return generate_card_wrapper(content)

def generate_mdt_reminder(data, barcode_data=None):
    """MDT Teaching reminder section - minimal style. Optional barcode/QR and meeting link."""
    if not data or not data.get('enabled', False):
        return ""

    time_text = data.get('time', '8:30-09:00')
    day_text = data.get('day', 'Tuesday')
    meeting_link = (data.get('meeting_link') or '').strip()
    barcode_img = (barcode_data or {}).get('barcode_image', '')
    barcode_src = image_to_src(barcode_img)
    barcode_cell = f'<td width="120" style="vertical-align: middle; padding-left: 16px; text-align: right;"><img src="{escape_html(barcode_src)}" style="max-width: 120px; width: 120px; height: auto; display: block; margin-left: auto;" alt="Teams meeting QR" /></td>' if barcode_src else ''

    time_display = f"{escape_html(day_text)} morning {escape_html(time_text)}"
    button_html = generate_button(meeting_link, "Join MDT Teaching") if meeting_link else ""
    time_block = time_display

    return f"""
    <table width="100%" cellpadding="0" cellspacing="0" border="0" style="margin-bottom: 32px;">
        <tr>
            <td style="background-color: #ffffff; border: 1px solid #e5e5e7; border-radius: 12px; padding: 20px 24px;">
                <table width="100%" cellpadding="0" cellspacing="0" border="0">
                    <tr>
                        <td style="vertical-align: middle;">
                            <div style="font-family: {STYLE['font_stack']}; font-size: 12px; font-weight: 500; color: {STYLE['text_secondary']}; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 8px;">
                                Reminder
                            </div>
                            <div style="font-family: {STYLE['font_stack']}; font-size: 18px; font-weight: 600; color: {STYLE['text_primary']}; margin-bottom: 4px;">
                                MDT Teaching
                            </div>
                            <div style="font-family: {STYLE['font_stack']}; font-size: 14px; color: #424245; line-height: 1.4;">
                                {time_block}
                            </div>
                            {button_html}
                        </td>
                        {barcode_cell}
                    </tr>
                </table>
            </td>
        </tr>
    </table>"""

def generate_barcode_section(data):
    """Barcode/QR code insertion section"""
    if not data or not data.get('barcode_image'):
        return ""
    barcode_src = image_to_src(data.get('barcode_image', ''))
    if not barcode_src:
        return ""
    return f"""
    <table width="100%" cellpadding="0" cellspacing="0" border="0" style="margin-bottom: 32px;">
        <tr>
            <td align="center" style="background-color: #ffffff; padding: 28px; border-radius: 12px; border: 1px solid #e5e5e7;">
                <img src="{escape_html(barcode_src)}" style="max-width: 100%; height: auto; display: block; margin: 0 auto;" alt="Barcode" />
            </td>
        </tr>
    </table>"""

def generate_footer():
    return f"""
    <table width="100%" cellpadding="0" cellspacing="0" border="0" style="margin-top: 48px;">
        <tr>
            <td style="text-align: center; padding-bottom: 40px;">
                <hr style="border: 0; border-top: 1px solid #e5e5e7; margin: 0 0 24px 0; padding: 0;">
                <div style="font-family: {STYLE['font_stack']}; font-size: 12px; color: {STYLE['text_secondary']}; margin-bottom: 8px;">
                    Next Issue: First Sunday of Next Month
                </div>
                <div style="font-family: {STYLE['font_stack']}; font-size: 12px; color: {STYLE['text_secondary']}; opacity: 0.6;">
                    Department of Obstetrics & Gynaecology
                </div>
            </td>
        </tr>
    </table>"""

def generate_newsletter_html(data):
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="Cache-Control" content="no-cache, no-store, must-revalidate">
    <meta http-equiv="Pragma" content="no-cache">
    <meta http-equiv="Expires" content="0">
    <title>The Station</title>
</head>
<body style="margin: 0; padding: 0; background-color: #f5f5f7; -webkit-font-smoothing: antialiased;">
    <table width="100%" cellpadding="0" cellspacing="0" border="0" style="background-color: #f5f5f7; padding: 60px 20px;">
        <tr>
            <td align="center">
                <table width="100%" cellpadding="0" cellspacing="0" border="0" style="max-width: 680px;">
                    <tr>
                        <td>
                            {generate_header(data['date_label'])}
                            {generate_message_to_team(data.get('message_to_team', ''), data.get('message_heading', ''))}
                            {generate_theme_section(data['theme']) if data.get('theme', {}).get('enabled', True) else ''}
                            {generate_ctg_section(data['ctg'])}
                            {generate_jc_section(data['gynae_jc']) if data.get('gynae_jc', {}).get('week_label') else ''}
                            {generate_guideline_section(data['guideline'])}
                            {generate_jc_section(data['obs_jc'])}
                            {generate_historical_fact_section(data.get('historical_fact', {}))}
                            {generate_schedule_table(data.get('schedule', {}))}
                            {generate_mdt_reminder(data.get('mdt_reminder', {}), data.get('barcode', {}))}
                            {generate_footer()}
                        </td>
                    </tr>
                </table>
            </td>
        </tr>
    </table>
</body>
</html>"""
    return html

def main():
    print("=" * 60)
    print("Obs and Gynae Newsletter Generator")
    print("=" * 60)
    print()
    
    # Load content from JSON file
    newsletter_data = load_newsletter_content()
    
    print("Generating Newsletter...")
    html_content = generate_newsletter_html(newsletter_data)
    
    output_dir = "../build"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    output_file = os.path.join(output_dir, "newsletter.html")
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html_content)

    # Also create index.html for easy local server access
    with open(os.path.join(output_dir, "index.html"), 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"✓ Newsletter generated successfully!")
    print(f"✓ Output saved to: {output_file}")
    print(f"✓ Also saved to: index.html (for local server)")
    print("\nYou can now:")
    print("  1. Open newsletter.html to preview")
    print("  2. View at http://localhost:8000/ (if server is running)")
    print("  3. Copy the HTML into your email client")
    print("  4. Or run: python3 send_newsletter.py")

if __name__ == "__main__":
    main()
