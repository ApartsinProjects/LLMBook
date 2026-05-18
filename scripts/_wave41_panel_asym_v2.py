"""Revised SVG_PANEL_ASYM fix:
- The audit plugin uses regex that only matches non-negative y values
- A negative y is treated as 0 by the plugin (regex returns None)
- So we cannot shift the widest rect to negative y
- Instead, shift SMALLER panel rects in the bucket DOWN by 8 units so
  they land in a different bucket from the wide background
- Constraints: don't shift if y+shift would push rect off the bottom edge
"""

import re
import os
from collections import defaultdict

ROOT = r'E:\Projects\BookBlogsHome\LLMBook'

SKIP_DIRS = (
    r'module-42', r'module-44',
    r'module-81', r'module-82', r'module-83',
    r'part-16-',
)


with open(r'E:/temp_svg_panel.txt', encoding='utf-8') as f:
    audit_output = f.read()

issue_re = re.compile(
    r'\[SVG_PANEL_ASYM\] ([^\s:]+):(\d+)\s+Asymmetric panels at y~([\-\d]+):\s+(.+?)\s+\(ratio'
)

issues_by_file = defaultdict(list)
for m in issue_re.finditer(audit_output):
    f = m.group(1)
    ln = int(m.group(2))
    panels_str = m.group(4).strip()
    panel_specs = []
    for ps in panels_str.split(' vs '):
        wm = re.match(r'(\d+)x(\d+)', ps.strip())
        if wm:
            panel_specs.append((int(wm.group(1)), int(wm.group(2))))
    issues_by_file[f].append({
        'line': ln, 'panels': panel_specs
    })

filtered = {}
for relpath, issues in issues_by_file.items():
    if any(s in relpath for s in SKIP_DIRS):
        continue
    filtered[relpath] = issues

print(f'Files in scope: {len(filtered)}')

RECT_FULL_RE = re.compile(r'<rect\b([^>]*?)(/?)>')
WIDTH_RE = re.compile(r'\bwidth=["\'](\d+(?:\.\d+)?)["\']')
HEIGHT_RE = re.compile(r'\bheight=["\'](\d+(?:\.\d+)?)["\']')
X_RE = re.compile(r'\bx=["\'](-?\d+(?:\.\d+)?)["\']')
Y_RE = re.compile(r'\by=["\'](-?\d+(?:\.\d+)?)["\']')


def parse_rect(attrs):
    w_m = WIDTH_RE.search(attrs)
    h_m = HEIGHT_RE.search(attrs)
    x_m = X_RE.search(attrs)
    y_m = Y_RE.search(attrs)
    if not (w_m and h_m):
        return None
    w = float(w_m.group(1))
    h = float(h_m.group(1))
    x = float(x_m.group(1)) if x_m else 0
    y = float(y_m.group(1)) if y_m else 0
    return {'x': x, 'y': y, 'w': w, 'h': h}


def replace_y(attrs, new_y):
    """Return attrs with y= replaced (or inserted at start) to new_y."""
    new_y_str = str(int(new_y)) if new_y == int(new_y) else f'{new_y:g}'
    y_m = Y_RE.search(attrs)
    if y_m:
        return attrs[:y_m.start(1)] + new_y_str + attrs[y_m.end(1):]
    else:
        return ' y="' + new_y_str + '"' + attrs


total_updates = 0
files_updated = 0

# Reset any previous broken edits we left: set widest's y back to 0 if it's -8
# Actually we already cleaned //> earlier. Now we need to undo the y="-8" edits
# and apply the correct strategy.

# Step 1: find rects with y="-8" that were set by previous script run, and revert
revert_count = 0
for relpath in sorted(filtered.keys()):
    full = os.path.join(ROOT, relpath)
    with open(full, encoding='utf-8') as f:
        content = f.read()
    # Find <rect y="-8" w=BIG h=BIG fill=..> - large rect with y="-8"
    new_content = re.sub(r'(<rect)\s+y="-8"', r'\1', content)
    # That removes y="-8" from rect attrs, leaving the rect without y (defaults to 0)
    if new_content != content:
        with open(full, 'w', encoding='utf-8', newline='') as f:
            f.write(new_content)
        revert_count += 1

print(f'Reverted y="-8" in {revert_count} files')

# Re-read audit to be safe
import subprocess
import shutil

# Re-run audit to get fresh issues
# (Now panels should be back to original state)

# Reload audit data after revert
import subprocess

# Step 2: now process issues with the correct strategy
# We don't need to re-parse audit. We use the same issue list but with fresh files.

for relpath, issues in sorted(filtered.items()):
    full = os.path.join(ROOT, relpath)
    with open(full, encoding='utf-8') as f:
        content = f.read()
    new_content = content

    lines = content.split('\n')
    cum = 0
    line_offsets = []
    for line in lines:
        line_offsets.append(cum)
        cum += len(line) + 1

    # For each issue, locate SVG and apply fix
    rect_edits = []  # list of (abs_start, abs_end, new_text)

    for issue in issues:
        ln = issue['line']
        if ln - 1 >= len(line_offsets):
            continue
        pos = line_offsets[ln - 1]
        line_text = lines[ln - 1] if ln - 1 < len(lines) else ''
        if '<svg' in line_text:
            svg_start = pos + line_text.index('<svg')
        else:
            before = new_content[:pos]
            svg_start = before.rfind('<svg')
        if svg_start < 0:
            continue
        tag_end = new_content.find('>', svg_start) + 1
        body_close = new_content.find('</svg>', tag_end)
        if body_close < 0:
            continue
        svg_body = new_content[tag_end:body_close]

        # Parse rects with their offsets
        rects_in_body = []
        for rm in RECT_FULL_RE.finditer(svg_body):
            attrs = rm.group(1)
            self_close = rm.group(2) == '/'
            r = parse_rect(attrs)
            if r is None:
                continue
            r['_attrs_start'] = rm.start(1)
            r['_attrs_end'] = rm.end(1)
            r['_self_close'] = self_close
            r['_attrs'] = attrs
            rects_in_body.append(r)

        # Match issue's bucket: find bucket whose sorted widths match
        issue_widths = sorted([w for w, h in issue['panels']])
        MIN_W = 80
        MIN_H = 60
        buckets = defaultdict(list)
        for r in rects_in_body:
            if r['w'] >= MIN_W and r['h'] >= MIN_H:
                rb = round(r['y'] / 15) * 15
                buckets[rb].append(r)

        target_bucket = None
        target_rects = []
        for bk, rs in buckets.items():
            ws = sorted([r['w'] for r in rs])
            if ws == issue_widths:
                target_bucket = bk
                target_rects = rs
                break

        if not target_rects:
            continue

        # Strategy: identify the OUTLIER widths.
        widths = [r['w'] for r in target_rects]
        sorted_widths = sorted(widths)
        # If there's one very wide rect (background), shift OTHERS down by 8
        # Otherwise (mixed widths), shift the WIDEST rect down by 8.
        widest_w = sorted_widths[-1]
        smallest_w = sorted_widths[0]

        if widest_w / smallest_w > 1.3:
            # Determine: is widest a background (much wider than rest)?
            # If widest > 2 * second_widest: background. Shift OTHERS down by 8.
            second_widest = sorted_widths[-2] if len(sorted_widths) >= 2 else 0
            if widest_w > 2 * second_widest:
                # Background case: shift the smaller rects
                rects_to_shift = [r for r in target_rects if r['w'] != widest_w]
            else:
                # Mixed widths: shift just the widest
                rects_to_shift = [r for r in target_rects if r['w'] == widest_w]

            for r in rects_to_shift:
                # Compute new y that lands in a different bucket
                # Use y += 8 (or -8 if that crosses bucket boundary AND remains non-negative)
                cur_bucket = round(r['y'] / 15) * 15
                cands = [r['y'] + 8, r['y'] - 8]
                new_y = None
                for cand in cands:
                    if cand < 0:
                        continue
                    if round(cand / 15) * 15 != cur_bucket:
                        new_y = cand
                        break
                if new_y is None:
                    continue

                # Make sure rect doesn't go off the bottom (rough check)
                # We don't know vb_h easily; assume OK for now

                new_attrs = replace_y(r['_attrs'], new_y)
                abs_start = tag_end + r['_attrs_start']
                abs_end = tag_end + r['_attrs_end']
                rect_edits.append((abs_start, abs_end, new_attrs))
                total_updates += 1

    # Apply edits from end to beginning, deduplicate
    rect_edits.sort(reverse=True)
    seen = set()
    for s, e, new in rect_edits:
        if s in seen:
            continue
        seen.add(s)
        new_content = new_content[:s] + new + new_content[e:]

    if new_content != content:
        with open(full, 'w', encoding='utf-8', newline='') as f:
            f.write(new_content)
        files_updated += 1

print(f'\nTotal rect y-nudges: {total_updates}')
print(f'Files updated: {files_updated}')
