#!/usr/bin/env python3
"""Convert non-standard content boxes to proper callout format."""
import glob, re

total = 0
files_fixed = 0

# --- 1. Convert <div class="tip-box"> to <div class="callout tip"> ---
def fix_tip_boxes(content):
    count = 0
    # Pattern: <div class="tip-box">\n    <strong>Tip:</strong> TEXT\n</div>
    def replace_tip(m):
        nonlocal count
        count += 1
        inner = m.group(1).strip()
        # Remove leading <strong>Tip:</strong> if present
        inner = re.sub(r'^\s*<strong>Tip:?\s*</strong>\s*', '', inner)
        return f'<div class="callout tip">\n    <div class="callout-title">Tip</div>\n    <p>{inner}</p>\n</div>'

    content = re.sub(
        r'<div class="tip-box">\s*(.*?)\s*</div>',
        replace_tip, content, flags=re.DOTALL
    )
    return content, count

# --- 2. Convert <div class="highlight-box"> to <div class="callout key-insight"> ---
def fix_highlight_boxes(content):
    count = 0
    def replace_hl(m):
        nonlocal count
        count += 1
        inner = m.group(1).strip()
        return f'<div class="callout key-insight">\n    <div class="callout-title">Key Insight</div>\n    {inner}\n</div>'

    content = re.sub(
        r'<div class="highlight-box">\s*(.*?)\s*</div>',
        replace_hl, content, flags=re.DOTALL
    )
    return content, count

files = sorted(set(
    glob.glob('part-*/module-*/**/*.html', recursive=True) +
    glob.glob('appendices/**/*.html', recursive=True) +
    glob.glob('front-matter/**/*.html', recursive=True) +
    glob.glob('capstone/**/*.html', recursive=True)
))

for f in files:
    content = open(f, 'r', encoding='utf-8').read()
    original = content

    content, c1 = fix_tip_boxes(content)
    content, c2 = fix_highlight_boxes(content)
    count = c1 + c2

    if content != original:
        open(f, 'w', encoding='utf-8').write(content)
        total += count
        files_fixed += 1
        print(f'{f}: {count} boxes converted (tip-box={c1}, highlight-box={c2})')

print(f'\nTotal: {total} boxes converted in {files_fixed} files')
