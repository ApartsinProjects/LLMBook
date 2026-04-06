#!/usr/bin/env python3
"""Audit SVGs for redundant title/description text inside diagrams.

Finds two patterns:
1. TITLE TEXT: Bold text near the top of the SVG (y < 35, font-weight bold/700,
   font-size >= 13) that duplicates info already in the diagram-caption.
2. BOTTOM TEXT: Light-colored description text near the bottom of the SVG
   (y within 40px of viewBox bottom, fill="#888" or similar muted colors)
   that duplicates info already in the diagram-caption.

Both patterns are redundant because every diagram has a <div class="diagram-caption">
below it with a figure number and description.

Usage:
  python audit_svg_redundant_text.py
"""

import re
from pathlib import Path

BOOK_ROOT = Path(r"E:/Projects/LLMCourse")
SKIP_DIRS = {".git", "node_modules", "__pycache__", "_archive", "agents", "vendor", "templates"}

# Parse viewBox to get bounds
VIEWBOX_RE = re.compile(r'viewBox="([^"]+)"')
# Find text elements inside SVGs
TEXT_RE = re.compile(
    r'<text\s+([^>]+)>([^<]*(?:<[^/][^>]*>[^<]*</[^>]*>)*[^<]*)</text>',
    re.DOTALL
)
# Extract attributes
ATTR_Y = re.compile(r'\by="([^"]+)"')
ATTR_FONT_SIZE = re.compile(r'font-size="(\d+)"')
ATTR_FONT_WEIGHT = re.compile(r'font-weight="([^"]+)"')
ATTR_FILL = re.compile(r'\bfill="([^"]+)"')
ATTR_TEXT_ANCHOR = re.compile(r'text-anchor="([^"]+)"')

# SVG block detection
SVG_OPEN_RE = re.compile(r'<svg\b[^>]*>')
SVG_CLOSE_RE = re.compile(r'</svg>')
DIAGRAM_CONTAINER_RE = re.compile(r'<div\s+class="diagram-container">')

MUTED_FILLS = {"#888", "#999", "#aaa", "#bbb", "#888888", "#999999", "#777", "#666"}


def parse_viewbox_height(svg_tag):
    m = VIEWBOX_RE.search(svg_tag)
    if not m:
        return None, None
    parts = m.group(1).split()
    if len(parts) == 4:
        min_y = float(parts[1])
        height = float(parts[3])
        return min_y, min_y + height
    return None, None


def audit_file(filepath):
    content = filepath.read_text(encoding="utf-8")
    if 'http-equiv="refresh"' in content:
        return []

    issues = []
    lines = content.split('\n')

    # Find all SVGs within diagram-containers
    # Simple approach: find each SVG tag and its content
    svg_starts = [(m.start(), m.group()) for m in SVG_OPEN_RE.finditer(content)]

    for svg_start_pos, svg_tag in svg_starts:
        svg_end_m = SVG_CLOSE_RE.search(content, svg_start_pos)
        if not svg_end_m:
            continue
        svg_content = content[svg_start_pos:svg_end_m.end()]

        min_y, max_y = parse_viewbox_height(svg_tag)
        if max_y is None:
            continue

        # Check if this SVG is inside a diagram-container
        # Look backwards for diagram-container
        preceding = content[max(0, svg_start_pos - 200):svg_start_pos]
        if 'diagram-container' not in preceding:
            continue

        # Find line number for reporting
        line_num = content[:svg_start_pos].count('\n') + 1

        for text_m in TEXT_RE.finditer(svg_content):
            attrs = text_m.group(1)
            text_content = re.sub(r'<[^>]+>', '', text_m.group(2)).strip()
            if not text_content or len(text_content) < 10:
                continue

            y_m = ATTR_Y.search(attrs)
            if not y_m:
                continue
            y_val = float(y_m.group(1))

            fs_m = ATTR_FONT_SIZE.search(attrs)
            font_size = int(fs_m.group(1)) if fs_m else 11

            fw_m = ATTR_FONT_WEIGHT.search(attrs)
            font_weight = fw_m.group(1) if fw_m else "normal"

            fill_m = ATTR_FILL.search(attrs)
            fill = fill_m.group(1) if fill_m else "#000"

            anchor_m = ATTR_TEXT_ANCHOR.search(attrs)
            anchor = anchor_m.group(1) if anchor_m else "start"

            # Pattern 1: Title text at top
            is_bold = font_weight in ("bold", "700", "600")
            if y_val < 35 and font_size >= 13 and is_bold and anchor == "middle":
                text_line = content[:svg_start_pos + text_m.start()].count('\n') + 1
                issues.append({
                    'type': 'TITLE_TEXT',
                    'line': text_line,
                    'y': y_val,
                    'text': text_content[:80],
                    'font_size': font_size,
                })

            # Pattern 2: Bottom description text
            if max_y and y_val > max_y - 45 and fill.lower() in MUTED_FILLS:
                text_line = content[:svg_start_pos + text_m.start()].count('\n') + 1
                issues.append({
                    'type': 'BOTTOM_TEXT',
                    'line': text_line,
                    'y': y_val,
                    'text': text_content[:80],
                    'fill': fill,
                })

    return issues


def main():
    all_files = sorted(BOOK_ROOT.rglob("*.html"))
    total_issues = 0
    files_with_issues = 0

    for f in all_files:
        if any(s in f.parts for s in SKIP_DIRS):
            continue
        issues = audit_file(f)
        if issues:
            files_with_issues += 1
            rel = f.relative_to(BOOK_ROOT)
            print(f"\n{rel}:")
            for issue in issues:
                total_issues += 1
                if issue['type'] == 'TITLE_TEXT':
                    print(f"  [TITLE] Line {issue['line']}: y={issue['y']}, "
                          f"size={issue['font_size']}: \"{issue['text']}\"")
                else:
                    print(f"  [BOTTOM] Line {issue['line']}: y={issue['y']}, "
                          f"fill={issue['fill']}: \"{issue['text']}\"")

    print(f"\n{'=' * 60}")
    print(f"Total issues: {total_issues}")
    print(f"Files affected: {files_with_issues}")


if __name__ == "__main__":
    main()
