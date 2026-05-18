"""Fix SVG_TEXT_RIGHT_CLIP by extending the viewBox width to accommodate
text that overflows the right edge.

Strategy: for each SVG, compute the maximum overflow across all flagged
text elements, then widen viewBox by that much (rounded up to nearest 10
units). Update both the viewBox attribute and any explicit width attribute
(removed in favor of width="100%" already via CSS).
"""

import re
import os

ROOT = r'E:\Projects\BookBlogsHome\LLMBook'

with open(r'E:/temp_svg_right_clip.txt', encoding='utf-8') as f:
    audit_output = f.read()

issue_re = re.compile(
    r'\[SVG_TEXT_RIGHT_CLIP\] ([^\s:]+):(\d+)\s+Text "([^"]+)" at x=([\d.]+) extends ~(\d+)px beyond viewBox width (\d+)'
)
issues_by_file = {}
for m in issue_re.finditer(audit_output):
    f = m.group(1)
    ln = int(m.group(2))
    text = m.group(3)
    x = float(m.group(4))
    overflow = int(m.group(5))
    vb_width = int(m.group(6))
    issues_by_file.setdefault(f, []).append({
        'line': ln, 'text': text, 'x': x, 'overflow': overflow, 'vb_width': vb_width
    })

print(f'Files with right-clip issues: {len(issues_by_file)}')

updated = 0
for relpath, issues in sorted(issues_by_file.items()):
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

    # Group issues by enclosing SVG so we extend each SVG's viewBox once
    svg_overflow_map = {}  # svg_open_start -> (max_overflow, vb_width)
    for issue in issues:
        ln = issue['line']
        pos = line_offsets[ln - 1] if ln - 1 < len(line_offsets) else len(content)
        before = new_content[:pos]
        last_open = before.rfind('<svg')
        last_close = before.rfind('</svg>')
        if last_open <= last_close:
            continue
        svg_overflow_map.setdefault(last_open, {
            'max_overflow': 0, 'vb_width': issue['vb_width']
        })
        if issue['overflow'] > svg_overflow_map[last_open]['max_overflow']:
            svg_overflow_map[last_open]['max_overflow'] = issue['overflow']

    # Process from end to beginning so offsets don't shift
    for svg_start in sorted(svg_overflow_map.keys(), reverse=True):
        info = svg_overflow_map[svg_start]
        max_overflow = info['max_overflow']
        # Round up to nearest 10 with margin
        extra = ((max_overflow + 19) // 10) * 10  # round up to 10, +10 margin
        if extra < 20:
            extra = 20  # minimum 20px margin

        svg_tag_end = new_content.find('>', svg_start) + 1
        opening = new_content[svg_start:svg_tag_end]
        # Find viewBox attribute. Allow viewbox or viewBox.
        vb_re = re.compile(r'(\bview[Bb]ox\s*=\s*")([^"]+)(")')
        vbm = vb_re.search(opening)
        if not vbm:
            print(f'  WARN: no viewBox in {relpath} at {svg_start}')
            continue
        vb_parts = vbm.group(2).split()
        if len(vb_parts) != 4:
            print(f'  WARN: malformed viewBox in {relpath}')
            continue
        try:
            vb_x, vb_y, vb_w, vb_h = [float(p) for p in vb_parts]
        except ValueError:
            print(f'  WARN: non-numeric viewBox in {relpath}')
            continue

        new_vb_w = vb_w + extra
        # Build new viewBox preserving integer/decimal format
        def fmt(v):
            return str(int(v)) if v == int(v) else str(v)
        new_vb = f'{fmt(vb_x)} {fmt(vb_y)} {fmt(new_vb_w)} {fmt(vb_h)}'
        new_opening = opening[:vbm.start(2)] + new_vb + opening[vbm.end(2):]

        # Update max-width in style and width="..." if present to track new aspect ratio
        # We do NOT necessarily change max-width; the SVG will just render thinner.
        # However the inline style has max-width:760px. Keep it but bump if smaller than vb_w
        sty_re = re.compile(r'(max-width\s*:\s*)(\d+)(px)')
        sty_m = sty_re.search(new_opening)
        if sty_m:
            old_mw = int(sty_m.group(2))
            if old_mw < new_vb_w:
                new_mw = int(new_vb_w)
                new_opening = new_opening[:sty_m.start(2)] + str(new_mw) + new_opening[sty_m.end(2):]

        # Update standalone width="..." attribute if numeric
        w_re = re.compile(r'\bwidth\s*=\s*"(\d+)"')
        wm = w_re.search(new_opening)
        if wm:
            old_w = int(wm.group(1))
            if old_w < new_vb_w:
                new_opening = new_opening[:wm.start(1)] + str(int(new_vb_w)) + new_opening[wm.end(1):]

        new_content = new_content[:svg_start] + new_opening + new_content[svg_tag_end:]
        updated += 1
        print(f'  {relpath}: viewBox {vb_w} -> {new_vb_w} (extra={extra}, max_overflow={max_overflow})')

    if new_content != content:
        with open(full, 'w', encoding='utf-8', newline='') as f:
            f.write(new_content)

print(f'\nSVGs widened: {updated}')
