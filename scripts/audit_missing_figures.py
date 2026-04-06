#!/usr/bin/env python3
"""Audit all section HTML files for missing or broken figures.

Checks:
1. <figure> elements with no <img> or <svg> child (empty figures)
2. <figcaption> / diagram-caption referencing a figure number but no visual content
3. Prose references like "Figure X.Y.Z" pointing to non-existent figure numbers
4. <figure class="illustration"> blocks where the image src file doesn't exist on disk
"""

import os
import re
import sys
from pathlib import Path
from collections import defaultdict

ROOT = Path(__file__).resolve().parent.parent

# Patterns
FIGURE_TAG_RE = re.compile(r'<figure[^>]*>(.*?)</figure>', re.DOTALL | re.IGNORECASE)
FIGURE_OPEN_RE = re.compile(r'<figure[^>]*>', re.IGNORECASE)
FIGURE_CLOSE_RE = re.compile(r'</figure>', re.IGNORECASE)
IMG_RE = re.compile(r'<img\b[^>]*>', re.IGNORECASE)
SVG_RE = re.compile(r'<svg\b[^>]*>.*?</svg>', re.DOTALL | re.IGNORECASE)
SVG_OPEN_RE = re.compile(r'<svg\b', re.IGNORECASE)
TABLE_RE = re.compile(r'<table\b', re.IGNORECASE)
FIGCAPTION_RE = re.compile(r'<figcaption[^>]*>(.*?)</figcaption>', re.DOTALL | re.IGNORECASE)
DIAGRAM_CAPTION_RE = re.compile(
    r'<div\s+class="diagram-caption"[^>]*>(.*?)</div>', re.DOTALL | re.IGNORECASE
)
FIGURE_NUM_RE = re.compile(r'Figure\s+(\d+\.\d+\.\d+)', re.IGNORECASE)
IMG_SRC_RE = re.compile(r'<img\b[^>]*\bsrc="([^"]*)"', re.IGNORECASE)
ILLUSTRATION_CLASS_RE = re.compile(r'class="[^"]*illustration[^"]*"', re.IGNORECASE)


def find_section_files():
    """Find all section HTML files in the project."""
    files = []
    for dirpath, dirnames, filenames in os.walk(ROOT):
        # Skip hidden dirs, node_modules, templates, etc.
        dirnames[:] = [d for d in dirnames if not d.startswith('.') and d not in ('node_modules', '_archive', '__pycache__', 'templates')]
        for fn in filenames:
            if fn.startswith('section-') and fn.endswith('.html'):
                files.append(Path(dirpath) / fn)
            # Also check index.html files (chapter indexes sometimes have figures)
            elif fn == 'index.html' and ('module-' in dirpath or 'part-' in dirpath or 'appendix' in dirpath.lower()):
                files.append(Path(dirpath) / fn)
    return sorted(files)


def extract_figures_with_positions(html):
    """Extract figure blocks by tracking open/close tags (handles nesting)."""
    figures = []
    # Simple approach: find all <figure...>...</figure> blocks
    # Use a stack-based approach for nested figures
    pos = 0
    while pos < len(html):
        m = FIGURE_OPEN_RE.search(html, pos)
        if not m:
            break
        start = m.start()
        # Find matching </figure>
        depth = 1
        search_pos = m.end()
        while depth > 0 and search_pos < len(html):
            next_open = FIGURE_OPEN_RE.search(html, search_pos)
            next_close = FIGURE_CLOSE_RE.search(html, search_pos)
            if not next_close:
                break
            if next_open and next_open.start() < next_close.start():
                depth += 1
                search_pos = next_open.end()
            else:
                depth -= 1
                if depth == 0:
                    end = next_close.end()
                    line_num = html[:start].count('\n') + 1
                    figures.append((html[start:end], line_num, m.group()))
                search_pos = next_close.end()
        pos = search_pos if search_pos > pos else pos + 1
    return figures


def get_defined_figure_numbers(html):
    """Get all figure numbers defined in captions (figcaption or diagram-caption)."""
    nums = set()
    for m in FIGCAPTION_RE.finditer(html):
        for fm in FIGURE_NUM_RE.finditer(m.group(1)):
            nums.add(fm.group(1))
    for m in DIAGRAM_CAPTION_RE.finditer(html):
        for fm in FIGURE_NUM_RE.finditer(m.group(1)):
            nums.add(fm.group(1))
    return nums


def get_prose_figure_refs(html):
    """Get all figure references in prose text (outside of figcaption/diagram-caption)."""
    # Remove captions first so we only find prose refs
    cleaned = FIGCAPTION_RE.sub('', html)
    cleaned = DIAGRAM_CAPTION_RE.sub('', cleaned)
    refs = []
    for m in FIGURE_NUM_RE.finditer(cleaned):
        line_num = html[:html.find(m.group())].count('\n') + 1
        refs.append((m.group(1), line_num))
    return refs


def audit_file(filepath):
    """Audit a single HTML file. Returns list of issues."""
    issues = []
    html = filepath.read_text(encoding='utf-8', errors='replace')
    file_dir = filepath.parent
    rel_path = filepath.relative_to(ROOT)

    # 1 & 2: Check <figure> elements for missing visual content
    figures = extract_figures_with_positions(html)
    for fig_html, line_num, open_tag in figures:
        has_img = bool(IMG_RE.search(fig_html))
        has_svg = bool(SVG_OPEN_RE.search(fig_html))
        has_table = bool(TABLE_RE.search(fig_html))
        is_illustration = bool(ILLUSTRATION_CLASS_RE.search(open_tag))

        # Check for empty figures (no img, no svg, no table)
        # Tables inside <figure> are valid (used for data figures)
        if not has_img and not has_svg and not has_table:
            # Get the caption text if any
            cap_match = FIGCAPTION_RE.search(fig_html)
            cap_text = cap_match.group(1).strip()[:100] if cap_match else "(no caption)"
            issues.append({
                'type': 'EMPTY_FIGURE',
                'file': str(rel_path),
                'line': line_num,
                'detail': f'<figure> has no <img>, <svg>, or <table>. Caption: {cap_text}'
            })

        # 4: Check illustration figures for missing image files
        if has_img:
            for img_match in IMG_SRC_RE.finditer(fig_html):
                src = img_match.group(1)
                # Skip external URLs
                if src.startswith(('http://', 'https://', 'data:')):
                    continue
                img_path = (file_dir / src).resolve()
                if not img_path.exists():
                    issues.append({
                        'type': 'MISSING_IMAGE_FILE',
                        'file': str(rel_path),
                        'line': line_num,
                        'detail': f'Image file not found: {src}'
                    })

    # Also check standalone <img> tags outside <figure> for missing files
    # (some images are outside figure tags, paired with diagram-caption divs)
    for img_match in IMG_SRC_RE.finditer(html):
        src = img_match.group(1)
        if src.startswith(('http://', 'https://', 'data:')):
            continue
        img_path = (file_dir / src).resolve()
        if not img_path.exists():
            line_num = html[:img_match.start()].count('\n') + 1
            # Check if already reported inside a figure
            already = any(
                i['type'] == 'MISSING_IMAGE_FILE' and src in i['detail']
                for i in issues
            )
            if not already:
                issues.append({
                    'type': 'MISSING_IMAGE_FILE_STANDALONE',
                    'file': str(rel_path),
                    'line': line_num,
                    'detail': f'Image file not found (standalone <img>): {src}'
                })

    # 3: Check prose references to figure numbers that aren't defined
    defined = get_defined_figure_numbers(html)
    prose_refs = get_prose_figure_refs(html)
    for fig_num, line_num in prose_refs:
        if fig_num not in defined:
            issues.append({
                'type': 'DANGLING_FIGURE_REF',
                'file': str(rel_path),
                'line': line_num,
                'detail': f'Prose references "Figure {fig_num}" but no such figure is defined in this file'
            })

    # 2 extra: Check diagram-caption divs that are NOT preceded by svg/img content
    # Find diagram-caption divs and check if they have visual content nearby
    for m in DIAGRAM_CAPTION_RE.finditer(html):
        cap_text = m.group(1)
        fig_nums = FIGURE_NUM_RE.findall(cap_text)
        if not fig_nums:
            continue
        # Look at the 2000 chars before this caption for an svg or img
        start = max(0, m.start() - 2000)
        preceding = html[start:m.start()]
        # Check if there's an svg close tag or img tag in the preceding chunk
        has_preceding_svg = bool(re.search(r'</svg>', preceding, re.IGNORECASE))
        has_preceding_img = bool(IMG_RE.search(preceding))
        # Also check if it's inside a figure (already caught above)
        inside_figure = bool(re.search(r'<figure[^>]*>', preceding[-500:], re.IGNORECASE))
        if not has_preceding_svg and not has_preceding_img and not inside_figure:
            line_num = html[:m.start()].count('\n') + 1
            issues.append({
                'type': 'CAPTION_NO_VISUAL',
                'file': str(rel_path),
                'line': line_num,
                'detail': f'diagram-caption for Figure {fig_nums[0]} has no preceding image or SVG'
            })

    return issues


def main():
    files = find_section_files()
    print(f"Scanning {len(files)} HTML files for figure issues...\n")

    all_issues = []
    files_with_issues = 0

    for f in files:
        try:
            issues = audit_file(f)
        except Exception as e:
            print(f"ERROR processing {f}: {e}")
            continue
        if issues:
            files_with_issues += 1
            all_issues.extend(issues)

    # Group by type
    by_type = defaultdict(list)
    for issue in all_issues:
        by_type[issue['type']].append(issue)

    # Print summary
    print("=" * 80)
    print("FIGURE AUDIT REPORT")
    print("=" * 80)
    print(f"\nFiles scanned:        {len(files)}")
    print(f"Files with issues:    {files_with_issues}")
    print(f"Total issues found:   {len(all_issues)}")
    print()

    type_labels = {
        'EMPTY_FIGURE': 'Empty <figure> (no <img>, <svg>, or <table>)',
        'MISSING_IMAGE_FILE': 'Missing image file (inside <figure>)',
        'MISSING_IMAGE_FILE_STANDALONE': 'Missing image file (standalone <img>)',
        'DANGLING_FIGURE_REF': 'Prose references non-existent figure',
        'CAPTION_NO_VISUAL': 'Caption with no preceding visual content',
    }

    print("Issues by category:")
    for typ, label in type_labels.items():
        count = len(by_type.get(typ, []))
        if count:
            print(f"  {label}: {count}")
    print()

    # Print details grouped by type
    for typ, label in type_labels.items():
        items = by_type.get(typ, [])
        if not items:
            continue
        print("-" * 80)
        print(f"{label} ({len(items)} issues)")
        print("-" * 80)
        for item in sorted(items, key=lambda x: (x['file'], x['line'])):
            print(f"  {item['file']}:{item['line']}")
            print(f"    {item['detail']}")
        print()

    if not all_issues:
        print("No issues found. All figures look good!")

    return 1 if all_issues else 0


if __name__ == '__main__':
    sys.exit(main())
