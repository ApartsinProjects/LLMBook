#!/usr/bin/env python3
"""SVG Quality Sweep: fixes stroke-linecap, small fonts, font-family, and detects text overlap."""

import os
import re
import glob

ROOT = r"E:\Projects\LLMCourse"

# Counters
count_linecap = 0
count_fontsize = 0
count_fontfamily = 0
overlap_warnings = []
files_modified = 0
files_scanned = 0

# Regex to isolate SVG blocks
SVG_BLOCK_RE = re.compile(r'(<svg[\s\S]*?</svg>)', re.IGNORECASE)

# --- Fix 1: stroke-linecap="round" ---
# Match <line or <path elements that have stroke= but no stroke-linecap
def fix_linecap(svg_text):
    global count_linecap

    def add_linecap(m):
        global count_linecap
        tag = m.group(0)
        # Skip if already has stroke-linecap
        if 'stroke-linecap' in tag:
            return tag
        # Only add if has stroke attribute (but not stroke-width/stroke-dasharray alone)
        if re.search(r'\bstroke="', tag):
            count_linecap += 1
            # Insert stroke-linecap="round" before the closing > or />
            tag = re.sub(r'(/?>)', r' stroke-linecap="round"\1', tag, count=1)
        return tag

    # Match <line ... > or <line ... /> and <path ... > or <path ... />
    svg_text = re.sub(r'<line\b[^>]*/?>', add_linecap, svg_text)
    svg_text = re.sub(r'<path\b[^>]*/?>', add_linecap, svg_text)
    return svg_text


# --- Fix 2: Small font sizes (< 10) -> 11 ---
def fix_small_fonts(svg_text):
    global count_fontsize

    def bump_font(m):
        global count_fontsize
        val = int(m.group(1))
        if val < 10:
            count_fontsize += 1
            return 'font-size="11"'
        return m.group(0)

    return re.sub(r'font-size="(\d+)"', bump_font, svg_text)


# --- Fix 3: Standardize font-family ---
MONOSPACE_KEYWORDS = ['monospace', 'Consolas', 'Courier', 'mono']
TARGET_FONT = 'Segoe UI, system-ui, sans-serif'

def fix_fontfamily(svg_text):
    global count_fontfamily

    def replace_ff(m):
        global count_fontfamily
        val = m.group(1)

        # Skip monospace fonts
        for kw in MONOSPACE_KEYWORDS:
            if kw.lower() in val.lower():
                return m.group(0)

        # Already correct
        if val == TARGET_FONT:
            return m.group(0)

        # "Segoe UI, sans-serif" -> add system-ui
        if val == 'Segoe UI, sans-serif':
            count_fontfamily += 1
            return f'font-family="{TARGET_FONT}"'

        # Georgia, serif
        if 'Georgia' in val:
            count_fontfamily += 1
            return f'font-family="{TARGET_FONT}"'

        # Arial variants
        if 'Arial' in val:
            count_fontfamily += 1
            return f'font-family="{TARGET_FONT}"'

        # Helvetica variants
        if 'Helvetica' in val:
            count_fontfamily += 1
            return f'font-family="{TARGET_FONT}"'

        # Other sans-serif that isn't already Segoe UI
        # Leave unknown fonts alone
        return m.group(0)

    return re.sub(r'font-family="([^"]*)"', replace_ff, svg_text)


# --- Fix 4: Detect text overlap ---
TEXT_ELEM_RE = re.compile(r'<text\b([^>]*)>([^<]*)</text>', re.IGNORECASE)
COORD_X_RE = re.compile(r'\bx="([^"]*)"')
COORD_Y_RE = re.compile(r'\by="([^"]*)"')

def detect_overlap(svg_text, filepath, svg_start_line):
    texts = []
    # Find all text elements with positions
    for m in TEXT_ELEM_RE.finditer(svg_text):
        attrs = m.group(1)
        content = m.group(2).strip()
        x_m = COORD_X_RE.search(attrs)
        y_m = COORD_Y_RE.search(attrs)
        if x_m and y_m:
            try:
                x = float(x_m.group(1))
                y = float(y_m.group(1))
            except ValueError:
                continue
            # Approximate line number within SVG
            offset = m.start()
            line_in_svg = svg_text[:offset].count('\n')
            texts.append((x, y, content, svg_start_line + line_in_svg))

    # Pairwise comparison
    for i in range(len(texts)):
        for j in range(i + 1, len(texts)):
            x1, y1, c1, l1 = texts[i]
            x2, y2, c2, l2 = texts[j]
            if abs(x1 - x2) <= 30 and abs(y1 - y2) <= 12:
                overlap_warnings.append(
                    f"  {filepath}\n"
                    f"    Lines ~{l1} & ~{l2}: "
                    f"({x1},{y1}) \"{c1[:40]}\" vs ({x2},{y2}) \"{c2[:40]}\""
                )


def process_file(filepath):
    global files_modified, files_scanned

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    if '<svg' not in content.lower():
        return

    files_scanned += 1
    original = content

    # Process each SVG block
    def process_svg_block(m):
        svg = m.group(1)
        # Determine start line of this SVG in the file
        start_pos = m.start()
        start_line = content[:start_pos].count('\n') + 1

        # Fix 4: detect overlap (before modifications, coords unchanged)
        detect_overlap(svg, filepath, start_line)

        # Fix 1
        svg = fix_linecap(svg)
        # Fix 2
        svg = fix_small_fonts(svg)
        # Fix 3
        svg = fix_fontfamily(svg)

        return svg

    new_content = SVG_BLOCK_RE.sub(process_svg_block, content)

    if new_content != original:
        files_modified += 1
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)


# Collect all HTML files
html_files = glob.glob(os.path.join(ROOT, '**', '*.html'), recursive=True)

print(f"Found {len(html_files)} HTML files to scan...")

for fpath in sorted(html_files):
    process_file(fpath)

print(f"\n{'='*60}")
print(f"SVG Quality Sweep Complete")
print(f"{'='*60}")
print(f"Files scanned (with SVGs):  {files_scanned}")
print(f"Files modified:             {files_modified}")
print(f"{'='*60}")
print(f"Fix 1 - stroke-linecap added:   {count_linecap}")
print(f"Fix 2 - small fonts bumped:     {count_fontsize}")
print(f"Fix 3 - font-family fixed:      {count_fontfamily}")
print(f"Fix 4 - overlap warnings:       {len(overlap_warnings)}")
print(f"{'='*60}")

if overlap_warnings:
    print(f"\nText Overlap Warnings (TASK-024):")
    print("-" * 50)
    for w in overlap_warnings:
        print(w.encode('ascii', 'replace').decode('ascii'))
