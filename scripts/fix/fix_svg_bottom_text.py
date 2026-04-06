"""
fix_svg_bottom_text.py
Remove redundant bottom text from inline SVG diagrams that duplicates
the figure caption below the SVG.

Usage:
    python fix_svg_bottom_text.py              # dry-run (default)
    python fix_svg_bottom_text.py --apply      # apply changes

The script:
1. Scans all .html files under part-*/ and appendices/ (skips _archive)
2. Finds inline <svg> elements with viewBox
3. Identifies "summary-style" text elements near the bottom of the viewBox:
   - Parse the viewBox to get the height
   - Find <text> elements where the y coordinate is in the bottom 15%
   - Filter for summary text (bold, colored, long, with background rect)
4. Compares bottom text to the nearby <figcaption> or <div class="diagram-caption">
5. Reports (or removes) redundant bottom text and adjusts the viewBox height
"""

import re
import sys
from pathlib import Path
from difflib import SequenceMatcher

BOOK_ROOT = Path(r"E:/Projects/LLMCourse")
APPLY = "--apply" in sys.argv

# Similarity threshold for considering text redundant with caption
SIMILARITY_THRESHOLD = 0.30

# Minimum text length to consider as a "summary" bottom text
# Short labels like "Model Size" are likely axis labels, not summaries
MIN_SUMMARY_LENGTH = 25


def collect_html_files():
    """Gather all .html files under part-*/ and appendices/, skip _archive."""
    files = []
    for pattern in ["part-*/**/*.html", "appendices/**/*.html"]:
        for p in BOOK_ROOT.glob(pattern):
            if "_archive" in str(p):
                continue
            files.append(p)
    return sorted(set(files))


def parse_viewbox(svg_tag):
    """Extract (min_x, min_y, width, height) from a viewBox attribute."""
    m = re.search(r'viewBox\s*=\s*"([^"]+)"', svg_tag)
    if not m:
        return None
    parts = m.group(1).split()
    if len(parts) != 4:
        return None
    try:
        return tuple(float(x) for x in parts)
    except ValueError:
        return None


def get_text_y(text_el):
    """Extract the y coordinate from a <text> element string."""
    m = re.search(r'\by\s*=\s*"([^"]+)"', text_el)
    if m:
        try:
            return float(m.group(1))
        except ValueError:
            return None
    return None


def strip_tags(html):
    """Remove HTML/SVG tags, collapse whitespace."""
    text = re.sub(r'<[^>]+>', '', html)
    text = re.sub(r'&[a-zA-Z#0-9]+;', ' ', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text


def similarity(a, b):
    """Compute similarity ratio between two strings (case-insensitive)."""
    a_lower = a.lower().strip()
    b_lower = b.lower().strip()
    if not a_lower or not b_lower:
        return 0.0
    return SequenceMatcher(None, a_lower, b_lower).ratio()


def has_summary_styling(text_el):
    """
    Check if a <text> element has styling typical of summary/banner text:
    bold, colored (often #e94560 or similar), or italic annotation.
    """
    has_bold = 'font-weight="bold"' in text_el or 'font-weight:bold' in text_el
    # Common summary/accent colors
    accent_colors = ['#e94560', '#e74c3c', '#c0392b', '#d35400', '#8e44ad']
    has_accent = any(f'fill="{c}"' in text_el for c in accent_colors)
    return has_bold or has_accent


def find_background_rect(svg_content, text_y, text_start):
    """
    Find a <rect> background element near the text (the rounded pill/banner).
    Returns the rect element string and positions if found.
    """
    search_start = max(0, text_start - 400)
    search_region = svg_content[search_start:text_start + 10]

    rects = []
    for m in re.finditer(r'(<rect[^>]*/>|<rect[^>]*>.*?</rect>)', search_region, re.DOTALL):
        rect_el = m.group(1)
        ym = re.search(r'\by\s*=\s*"([^"]+)"', rect_el)
        if ym:
            try:
                rect_y = float(ym.group(1))
            except ValueError:
                continue
            # Background rect is typically 10-30px above the text
            if 0 <= (text_y - rect_y) <= 40:
                # Check if it looks like a banner (has opacity, rounded corners, fill)
                is_banner = ('opacity' in rect_el or 'rx=' in rect_el)
                rects.append((rect_el, search_start + m.start(), search_start + m.end(), is_banner))

    return rects


def find_caption_after_svg(html, svg_end_pos):
    """Find the diagram-caption or figcaption text after the SVG closing tag."""
    search_region = html[svg_end_pos:svg_end_pos + 500]

    m = re.search(r'<div\s+class="diagram-caption">(.*?)</div>', search_region, re.DOTALL)
    if m:
        return strip_tags(m.group(1))

    m = re.search(r'<figcaption>(.*?)</figcaption>', search_region, re.DOTALL)
    if m:
        return strip_tags(m.group(1))

    return None


def find_bottom_text_elements(svg_content, vb):
    """
    Find <text> elements in the bottom 15% of the viewBox that look like
    summary/banner text (not axis labels or diagram annotations).
    Returns list of (text_element_string, text_content, y_coord, start, end, has_bg_rect).
    """
    min_x, min_y, width, height = vb
    bottom_threshold = min_y + height * 0.85

    results = []

    for m in re.finditer(r'(<text[^>]*>.*?</text>)', svg_content, re.DOTALL):
        text_el = m.group(1)
        y = get_text_y(text_el)
        if y is None or y < bottom_threshold:
            continue

        content = strip_tags(text_el)
        if not content:
            continue

        # Check for background rect (banner style)
        bg_rects = find_background_rect(svg_content, y, m.start())
        has_bg = any(is_banner for _, _, _, is_banner in bg_rects)

        # A bottom text is a "summary" candidate if:
        # 1. It has summary styling (bold, accent color) AND a background rect, OR
        # 2. It is long enough (>= MIN_SUMMARY_LENGTH) AND has styling or bg rect
        is_styled = has_summary_styling(text_el)
        is_long = len(content) >= MIN_SUMMARY_LENGTH

        is_summary_candidate = False
        if is_styled and has_bg:
            is_summary_candidate = True
        elif is_long and (is_styled or has_bg):
            is_summary_candidate = True
        elif is_long and len(content) >= 50:
            # Very long text near bottom is likely a summary even without styling
            is_summary_candidate = True

        if is_summary_candidate:
            results.append((text_el, content, y, m.start(), m.end(), bg_rects))

    return results


def find_comment_before(svg_content, element_start):
    """Find an HTML comment just before the element (within 150 chars)."""
    search_start = max(0, element_start - 200)
    search_region = svg_content[search_start:element_start]
    m = re.search(r'(<!--[^>]*-->)\s*$', search_region)
    if m:
        return (m.group(1), search_start + m.start(), search_start + m.end())
    return None


def adjust_viewbox(svg_tag, reduction):
    """Reduce the height in the viewBox by the given amount."""
    m = re.search(r'(viewBox\s*=\s*")([^"]+)(")', svg_tag)
    if not m:
        return svg_tag
    parts = m.group(2).split()
    if len(parts) != 4:
        return svg_tag
    try:
        min_x, min_y, w, h = (float(x) for x in parts)
    except ValueError:
        return svg_tag
    new_h = h - reduction
    def fmt(v):
        return str(int(v)) if v == int(v) else str(v)
    new_vb = f"{fmt(min_x)} {fmt(min_y)} {fmt(w)} {fmt(new_h)}"
    return svg_tag[:m.start(2)] + new_vb + svg_tag[m.end(2):]


def process_file(filepath, findings):
    """Process a single HTML file."""
    html = filepath.read_text(encoding="utf-8")

    svg_pattern = re.compile(r'(<svg[^>]*viewBox[^>]*>)(.*?)(</svg>)', re.DOTALL)

    modifications = []

    for svg_idx, m in enumerate(svg_pattern.finditer(html)):
        svg_open = m.group(1)
        svg_body = m.group(2)
        svg_close = m.group(3)
        svg_start = m.start()
        svg_end = m.end()

        vb = parse_viewbox(svg_open)
        if not vb:
            continue

        min_x, min_y, width, height = vb

        caption_text = find_caption_after_svg(html, svg_end)
        if not caption_text:
            continue

        bottom_texts = find_bottom_text_elements(svg_body, vb)
        if not bottom_texts:
            continue

        for text_el, text_content, text_y, t_start, t_end, bg_rects in bottom_texts:
            sim = similarity(text_content, caption_text)
            is_redundant = sim >= SIMILARITY_THRESHOLD

            rel_path = filepath.relative_to(BOOK_ROOT)
            finding = {
                "file": str(rel_path),
                "svg_num": svg_idx + 1,
                "bottom_text": text_content,
                "caption": caption_text,
                "similarity": sim,
                "redundant": is_redundant,
                "text_y": text_y,
                "viewbox_height": height,
                "has_bg_rect": bool(bg_rects),
            }
            findings.append(finding)

            if is_redundant and APPLY:
                elements_to_remove = []
                elements_to_remove.append((t_start, t_end))

                # Remove background rects
                for rect_el, r_start, r_end, is_banner in bg_rects:
                    if is_banner:
                        elements_to_remove.append((r_start, r_end))

                # Remove preceding comment
                earliest_start = min(s for s, e in elements_to_remove)
                comment = find_comment_before(svg_body, earliest_start)
                if comment:
                    _, c_start, c_end = comment
                    elements_to_remove.append((c_start, c_end))

                elements_to_remove.sort(key=lambda x: x[0], reverse=True)

                new_body = svg_body
                for s, e in elements_to_remove:
                    line_start = new_body.rfind('\n', 0, s)
                    line_end = new_body.find('\n', e)
                    if line_start == -1:
                        line_start = s
                    if line_end == -1:
                        line_end = e
                    else:
                        line_end += 1

                    line_content = new_body[line_start:line_end].strip()
                    el_content = new_body[s:e].strip()
                    if line_content == el_content or line_content.startswith('<!--'):
                        new_body = new_body[:line_start] + new_body[line_end:]
                    else:
                        new_body = new_body[:s] + new_body[e:]

                reduction = (min_y + height) - text_y + 20
                reduction = max(20, min(60, reduction))
                new_open = adjust_viewbox(svg_open, reduction)

                new_svg = new_open + new_body + svg_close
                modifications.append((svg_start, svg_end, new_svg))

    if modifications and APPLY:
        modifications.sort(key=lambda x: x[0], reverse=True)
        for start, end, replacement in modifications:
            html = html[:start] + replacement + html[end:]
        filepath.write_text(html, encoding="utf-8")

    return len(modifications)


def main():
    mode = "APPLY" if APPLY else "DRY RUN"
    print(f"=== SVG Bottom Text Audit ({mode}) ===")
    print(f"Book root: {BOOK_ROOT}")
    print(f"Similarity threshold: {SIMILARITY_THRESHOLD}")
    print(f"Min summary length: {MIN_SUMMARY_LENGTH}")
    print()

    files = collect_html_files()
    print(f"Scanning {len(files)} HTML files...")
    print()

    findings = []
    files_modified = 0

    for f in files:
        count = process_file(f, findings)
        if count > 0:
            files_modified += 1

    redundant = [f for f in findings if f["redundant"]]
    not_redundant = [f for f in findings if not f["redundant"]]

    print(f"{'='*90}")
    print(f"REDUNDANT BOTTOM TEXT (similarity >= {SIMILARITY_THRESHOLD})")
    print(f"{'='*90}")
    for i, f in enumerate(redundant, 1):
        print(f"\n{i}. {f['file']} (SVG #{f['svg_num']})")
        print(f"   Bottom text: \"{f['bottom_text']}\"")
        cap = f['caption'][:100] + ('...' if len(f['caption']) > 100 else '')
        print(f"   Caption:     \"{cap}\"")
        print(f"   Similarity:  {f['similarity']:.2f}  BgRect: {f['has_bg_rect']}")
        print(f"   Text Y={f['text_y']}, ViewBox height={f['viewbox_height']}")

    if not_redundant:
        print(f"\n{'='*90}")
        print(f"NON-REDUNDANT bottom summary text (kept, similarity < {SIMILARITY_THRESHOLD})")
        print(f"{'='*90}")
        for i, f in enumerate(not_redundant, 1):
            print(f"\n{i}. {f['file']} (SVG #{f['svg_num']})")
            print(f"   Bottom text: \"{f['bottom_text']}\"")
            cap = f['caption'][:100] + ('...' if len(f['caption']) > 100 else '')
            print(f"   Caption:     \"{cap}\"")
            print(f"   Similarity:  {f['similarity']:.2f}  BgRect: {f['has_bg_rect']}")

    print(f"\n{'='*90}")
    print(f"SUMMARY")
    print(f"{'='*90}")
    print(f"  Files scanned:               {len(files)}")
    print(f"  Summary-style bottom texts:  {len(findings)}")
    print(f"  Redundant (to remove):       {len(redundant)}")
    print(f"  Non-redundant (keep):        {len(not_redundant)}")
    if APPLY:
        print(f"  Files modified:              {files_modified}")
    else:
        print(f"  Mode: DRY RUN (use --apply to make changes)")


if __name__ == "__main__":
    main()
