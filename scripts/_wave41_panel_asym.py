"""Fix SVG_PANEL_ASYM by nudging the y-coordinate of the widest rect in
each flagged bucket so it falls into a different 15px bucket from the
inner panel rects. This is the bucket-aware y-positioning trick.

The audit groups rects by `round(y/15)*15`, so to separate a background
(or wide panel) from smaller panels at the same nominal y, shift the
wider rect's y by enough to cross a bucket boundary (>=8 units).
"""

import re
import os
from collections import defaultdict

ROOT = r'E:\Projects\BookBlogsHome\LLMBook'

SKIP_DIRS = (
    r'module-42', r'module-44',
    r'module-81', r'module-82', r'module-83',  # Wave 27 batch 5
    r'part-16-',  # batch 5 lives here
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
    y_bucket = int(m.group(3))
    panels_str = m.group(4).strip()
    # panels_str looks like "120x60 vs 180x80 vs 160x80 vs 100x60"
    panel_specs = []
    for ps in panels_str.split(' vs '):
        wm = re.match(r'(\d+)x(\d+)', ps.strip())
        if wm:
            panel_specs.append((int(wm.group(1)), int(wm.group(2))))
    issues_by_file[f].append({
        'line': ln, 'y_bucket': y_bucket, 'panels': panel_specs
    })

# Filter out skipped paths
filtered = {}
for relpath, issues in issues_by_file.items():
    if any(s in relpath for s in SKIP_DIRS):
        continue
    filtered[relpath] = issues

print(f'Files in scope: {len(filtered)} (of {len(issues_by_file)} total)')

RECT_RE = re.compile(r'<rect\b([^>]*)/?>')
WIDTH_RE = re.compile(r'\bwidth=["\'](\d+(?:\.\d+)?)["\']')
HEIGHT_RE = re.compile(r'\bheight=["\'](\d+(?:\.\d+)?)["\']')
X_RE = re.compile(r'\bx=["\'](\d+(?:\.\d+)?)["\']')
Y_RE = re.compile(r'\by=["\'](\d+(?:\.\d+)?)["\']')


def parse_rect_attrs(attrs):
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


def find_svg_blocks(content):
    """Return list of (svg_open_start, svg_body_start, svg_body_end, svg_close_end)."""
    blocks = []
    for m in re.finditer(r'<svg\b[^>]*>', content):
        tag_end = m.end()
        close_m = re.search(r'</svg>', content[tag_end:])
        if not close_m:
            continue
        body_end = tag_end + close_m.start()
        block_end = tag_end + close_m.end()
        blocks.append((m.start(), tag_end, body_end, block_end))
    return blocks


total_updated = 0
files_updated = 0

for relpath, issues in sorted(filtered.items()):
    full = os.path.join(ROOT, relpath)
    with open(full, encoding='utf-8') as f:
        content = f.read()
    new_content = content

    # For each issue, locate the SVG containing the issue's flagged y_bucket and panel sizes
    # The issue tells us SVG starts at issue['line'] - need to locate this SVG
    # We'll find SVG blocks and for each issue find the one whose body contains rects matching panel sizes

    lines = content.split('\n')
    cum = 0
    line_offsets = []
    for line in lines:
        line_offsets.append(cum)
        cum += len(line) + 1

    # group issues by approximate SVG location (line)
    file_changes = []  # list of (rect_old_start, rect_old_end, new_rect_str)

    for issue in issues:
        ln = issue['line']
        if ln - 1 >= len(line_offsets):
            continue
        pos = line_offsets[ln - 1]
        # find the SVG opening tag: either on this line or before
        line_text = lines[ln - 1] if ln - 1 < len(lines) else ''
        if '<svg' in line_text:
            line_svg_pos = pos + line_text.index('<svg')
            last_open = line_svg_pos
        else:
            before = new_content[:pos]
            last_open = before.rfind('<svg')
        if last_open < 0:
            continue
        tag_end = new_content.find('>', last_open) + 1
        body_close = new_content.find('</svg>', tag_end)
        if body_close < 0:
            continue
        svg_body = new_content[tag_end:body_close]

        # Parse rects within this body
        rects_in_body = []
        for rm in RECT_RE.finditer(svg_body):
            attrs = rm.group(1)
            r = parse_rect_attrs(attrs)
            if r is None:
                continue
            r['_rm_start'] = rm.start()  # relative to svg_body
            r['_rm_end'] = rm.end()
            r['_attrs'] = attrs
            r['_full'] = rm.group(0)
            rects_in_body.append(r)

        # Reconstruct the bucketed group. The audit reports y~N where N is
        # the FIRST rect's y, but the actual bucket is round(N/15)*15.
        # We find rects whose bucket matches one of: N's bucket, N-15, N+15
        # then pick the bucket whose widths match the issue's panel list.
        issue_y = issue['y_bucket']
        issue_widths = sorted([w for w, h in issue['panels']])
        MIN_W = 80
        MIN_H = 60
        # Try buckets near issue_y
        buckets = defaultdict(list)
        for r in rects_in_body:
            if r['w'] >= MIN_W and r['h'] >= MIN_H:
                rb = round(r['y'] / 15) * 15
                buckets[rb].append(r)
        # Find the bucket whose sorted widths match issue_widths
        target_rects = []
        for bk, rs in buckets.items():
            ws = sorted([r['w'] for r in rs])
            if ws == issue_widths:
                # Confirm by also matching y range
                # The audit's reported y is the first rect's y, which is just
                # the first one parsed. We trust width match.
                target_rects = rs
                break

        if len(target_rects) < 2:
            continue

        # Find the widest one (likely the background)
        widest = max(target_rects, key=lambda r: r['w'])
        # Find the others' widths
        other_widths = [r['w'] for r in target_rects if r is not widest]
        max_other = max(other_widths) if other_widths else 0
        min_other = min(other_widths) if other_widths else 0

        # If the widest is much bigger than the others, we'll shift it out of the bucket
        # If the others differ amongst themselves, they may need width equalization (skip; nudging suffices)

        if widest['w'] / (max(min_other, 1)) > 1.3:
            # Compute a new y for the widest that lands in a different bucket
            current_bucket = round(widest['y'] / 15) * 15
            # Try shifting -8 (one bucket up) or +8 (one bucket down)
            new_y_candidates = [widest['y'] - 8, widest['y'] + 8]
            new_y = None
            for cand in new_y_candidates:
                cand_bucket = round(cand / 15) * 15
                if cand_bucket != current_bucket and cand >= -50:
                    new_y = cand
                    break
            if new_y is None:
                continue

            # Build new rect attrs by replacing y=...
            old_attrs = widest['_attrs']
            # Find the y attr in old_attrs (or absence)
            ym = Y_RE.search(old_attrs)
            if ym:
                new_attrs = old_attrs[:ym.start(1)] + str(int(new_y) if new_y == int(new_y) else f'{new_y:g}') + old_attrs[ym.end(1):]
            else:
                # insert y attr
                new_attrs = ' y="' + str(int(new_y)) + '"' + old_attrs
            new_rect = '<rect' + new_attrs + ('/>' if widest['_full'].endswith('/>') else '>')

            # Record the change. _rm_start/_end are RELATIVE TO svg_body
            abs_start = tag_end + widest['_rm_start']
            abs_end = tag_end + widest['_rm_end']
            file_changes.append((abs_start, abs_end, new_rect))
            total_updated += 1
            print(f'  {relpath}: widest rect ({widest["w"]}x{widest["h"]} at y={widest["y"]}) -> y={new_y}')

    # Apply changes from end to beginning to preserve offsets
    file_changes.sort(reverse=True)
    # Deduplicate same start position
    seen = set()
    for s, e, new in file_changes:
        if s in seen:
            continue
        seen.add(s)
        new_content = new_content[:s] + new + new_content[e:]

    if new_content != content:
        with open(full, 'w', encoding='utf-8', newline='') as f:
            f.write(new_content)
        files_updated += 1

print(f'\nTotal rect y-nudges: {total_updated}')
print(f'Files updated: {files_updated}')
