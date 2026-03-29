"""
Fix SVG accessibility: add role="img" and aria-label to inline SVGs in HTML files.

Scans HTML files for inline <svg> tags missing accessibility attributes and adds:
  - role="img"
  - aria-label="..." derived from surrounding context

Label derivation priority:
  1. Nearest preceding HTML comment (<!-- SVG: ..., <!-- DIAGRAM ..., etc.)
  2. Nearest preceding <div class="figure-caption"> text
  3. Nearest preceding <figcaption> text
  4. Nearest preceding <strong>Figure ...</strong> text
  5. Nearest preceding heading (h2, h3, h4)
  6. Fallback: "Diagram N.M" from filename, or just "Diagram"
"""

import glob
import os
import re
import sys

GLOB_PATTERNS = [
    "part-*/module-*/**/*.html",
    "appendices/**/*.html",
    "capstone/**/*.html",
    "front-matter/**/*.html",
]


def strip_html_tags(text):
    """Remove HTML tags and collapse whitespace."""
    text = re.sub(r"<[^>]+>", " ", text)
    text = re.sub(r"&amp;", "&", text)
    text = re.sub(r"&lt;", "<", text)
    text = re.sub(r"&gt;", ">", text)
    text = re.sub(r"&nbsp;", " ", text)
    text = re.sub(r"&#\d+;", " ", text)
    text = re.sub(r"&\w+;", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def extract_section_number(filepath):
    """Extract section number from filename like section-2.3.html."""
    basename = os.path.basename(filepath)
    m = re.search(r"section-(\d+\.\d+)", basename)
    if m:
        return m.group(1)
    # Try module number from path
    m = re.search(r"module-(\d+)", filepath)
    if m:
        return m.group(1)
    return None


def derive_label(content_before, filepath, svg_index_in_file):
    """Derive an aria-label from context preceding the SVG tag.

    Args:
        content_before: up to 800 chars of HTML before the <svg tag
        filepath: the HTML file path (for fallback section numbering)
        svg_index_in_file: 0-based index of this SVG in the file

    Returns:
        A descriptive label string.
    """
    # 1. HTML comment: <!-- SVG: ... --> or <!-- DIAGRAM ... --> or any comment nearby
    #    Look for the closest comment (last one in the before-text)
    comments = re.findall(r"<!--\s*(.+?)\s*-->", content_before)
    if comments:
        last_comment = comments[-1]
        # Skip separator-only comments like "======" or "------"
        cleaned = re.sub(r"[=\-\s]", "", last_comment)
        if len(cleaned) > 2:
            label = last_comment
            # Remove leading "SVG:" or "SVG " prefix for cleaner label
            label = re.sub(r"^SVG\s*:\s*", "", label, flags=re.IGNORECASE)
            label = re.sub(r"^DIAGRAM\s*\d*\s*:\s*", "", label, flags=re.IGNORECASE)
            label = strip_html_tags(label).strip()
            if label:
                return "Diagram: " + label[:120] if not label.lower().startswith("diagram") else label[:120]

    # 2. <div class="figure-caption">...</div>
    figcaps = re.findall(
        r'<div\s+class="figure-caption">(.*?)</div>', content_before, re.DOTALL
    )
    if figcaps:
        text = strip_html_tags(figcaps[-1])
        if text:
            return text[:120]

    # 3. <figcaption>...</figcaption>
    figcaptions = re.findall(
        r"<figcaption[^>]*>(.*?)</figcaption>", content_before, re.DOTALL
    )
    if figcaptions:
        text = strip_html_tags(figcaptions[-1])
        if text:
            return text[:120]

    # 4. <strong>Figure ...</strong>
    strong_figs = re.findall(r"<strong>(Figure\s+[^<]+)</strong>", content_before)
    if strong_figs:
        text = strip_html_tags(strong_figs[-1])
        if text:
            return text[:120]

    # 5. Nearest preceding heading (h2, h3, h4)
    headings = re.findall(r"<h[234][^>]*>(.*?)</h[234]>", content_before)
    if headings:
        text = strip_html_tags(headings[-1])
        if text:
            return "Diagram: " + text[:110]

    # 6. Fallback: section number from filename
    sec_num = extract_section_number(filepath)
    if sec_num:
        suffix = f" {sec_num}"
        if svg_index_in_file > 0:
            suffix += f".{svg_index_in_file + 1}"
        return "Diagram" + suffix
    return "Diagram"


def escape_for_attr(text):
    """Escape text for use inside a double-quoted HTML attribute."""
    text = text.replace("&", "&amp;")
    text = text.replace('"', "&quot;")
    text = text.replace("<", "&lt;")
    text = text.replace(">", "&gt;")
    return text


def process_file(filepath):
    """Process a single HTML file. Returns count of SVGs fixed."""
    with open(filepath, encoding="utf-8") as f:
        content = f.read()

    fixed_count = 0
    svg_index = -1
    offset = 0  # track cumulative offset from insertions

    # Find all <svg ...> opening tags
    svg_pattern = re.compile(r"<svg\b([^>]*)>")

    for m in svg_pattern.finditer(content):
        svg_index += 1

    # Reset and process with offset tracking
    svg_index = -1
    new_content = content
    # We need to re-find after each edit; use a different approach
    # Collect all edit positions first, then apply from end to start

    edits = []  # list of (start, end, new_tag) to apply

    for m in svg_pattern.finditer(content):
        svg_index += 1
        attrs = m.group(1)
        full_tag = m.group(0)

        has_role = re.search(r'\brole\s*=', attrs) is not None
        has_aria = re.search(r'\baria-label\s*=', attrs) is not None

        if has_role and has_aria:
            continue  # already accessible

        # Get context before this SVG (up to 800 chars)
        before_start = max(0, m.start() - 800)
        content_before = content[before_start : m.start()]

        label = derive_label(content_before, filepath, svg_index)

        # Build new attributes to insert
        new_attrs = []
        if not has_role:
            new_attrs.append('role="img"')
        if not has_aria:
            new_attrs.append(f'aria-label="{escape_for_attr(label)}"')

        # Insert after "<svg " (before existing attributes)
        insert_str = " ".join(new_attrs)
        # Replace <svg ... > with <svg [new_attrs] ...>
        new_tag = "<svg " + insert_str + " " + attrs.lstrip() + ">"

        edits.append((m.start(), m.end(), new_tag))
        fixed_count += 1

    if not edits:
        return 0

    # Apply edits from end to start to preserve positions
    for start, end, new_tag in reversed(edits):
        new_content = new_content[:start] + new_tag + new_content[end:]

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(new_content)

    return fixed_count


def main():
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    # Collect files
    files = []
    for pat in GLOB_PATTERNS:
        files.extend(glob.glob(pat, recursive=True))
    files = sorted(set(files))

    print(f"Scanning {len(files)} HTML files...")
    total_fixed = 0
    files_modified = 0

    for filepath in files:
        count = process_file(filepath)
        if count > 0:
            print(f"  {filepath}: fixed {count} SVG(s)")
            total_fixed += count
            files_modified += 1

    print(f"\nDone. Fixed {total_fixed} SVGs across {files_modified} files.")
    return total_fixed


if __name__ == "__main__":
    total = main()
    sys.exit(0 if total >= 0 else 1)
