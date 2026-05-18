"""Fix SVG_TEXT_CLIPPING issues by extending the viewBox of each affected
SVG to a range that includes all flagged text coordinates with a small
margin. The plugin compares raw text x/y to viewBox bounds without
accounting for ancestor <g transform="..."> elements, so a generous
viewBox is the safe fix. We then keep the max-width style intact so the
diagram renders at roughly the same visible size.
"""

import re
import os

ROOT = r'E:\Projects\BookBlogsHome\LLMBook'

with open(r'E:/temp_svg_clipping.txt', encoding='utf-8') as f:
    audit_output = f.read()

# Parse: [SVG_TEXT_CLIPPING] path:line  Text "..." may be clipped: x=N near left edge (M); y=N near top edge (M)...
issue_re = re.compile(
    r'\[SVG_TEXT_CLIPPING\] ([^\s:]+):(\d+)\s+Text "[^"]*" may be clipped:\s+(.*?)(?=\n\s*\[|\n\n|\nScanned|\Z)',
    re.DOTALL
)
issues_by_file = {}
for m in issue_re.finditer(audit_output):
    relpath = m.group(1)
    ln = int(m.group(2))
    details = m.group(3).strip()
    # Parse the details, e.g. "x=-12.0 near left edge (0.0); y=-20.0 near top edge (0.0)"
    coord_data = {}  # dim -> (val, edge_pos)
    for cm in re.finditer(r'([xy])=(-?[\d.]+) near (\w+) edge \((-?[\d.]+)\)', details):
        dim = cm.group(1)
        val = float(cm.group(2))
        edge_name = cm.group(3)
        edge_pos = float(cm.group(4))
        # Map: dim + edge_name -> val
        key = f'{dim}_{edge_name}'
        coord_data[key] = (val, edge_pos)
    issues_by_file.setdefault(relpath, []).append({
        'line': ln, 'coords': coord_data
    })

print(f'Files with clipping issues: {len(issues_by_file)}')

def find_enclosing_svg(content, target_pos):
    before = content[:target_pos]
    last_open = before.rfind('<svg')
    last_close = before.rfind('</svg>')
    if last_open <= last_close:
        return None, None
    tag_end = content.find('>', last_open)
    if tag_end < 0:
        return None, None
    return last_open, tag_end + 1


def parse_viewbox(opening_tag):
    """Parse viewBox attribute and return (vb_x, vb_y, vb_w, vb_h) or None."""
    m = re.search(r'\bview[Bb]ox\s*=\s*"([^"]+)"', opening_tag)
    if not m:
        return None
    parts = m.group(1).split()
    if len(parts) != 4:
        return None
    try:
        return (float(parts[0]), float(parts[1]), float(parts[2]), float(parts[3]))
    except ValueError:
        return None


def fmt(v):
    return str(int(v)) if v == int(v) else f'{v:g}'


total_updated = 0
files_updated = 0

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

    # Group issues by enclosing SVG
    svg_clamps = {}  # svg_start -> {'min_x': float, 'max_x': float, 'min_y': float, 'max_y': float}

    for issue in issues:
        ln = issue['line']
        if ln - 1 >= len(line_offsets):
            continue
        pos = line_offsets[ln - 1]
        svg_start, svg_end = find_enclosing_svg(content, pos)
        if svg_start is None:
            continue
        rec = svg_clamps.setdefault(svg_start, {
            'min_x': None, 'max_x': None, 'min_y': None, 'max_y': None
        })
        for key, (val, edge_pos) in issue['coords'].items():
            if key == 'x_left':
                if rec['min_x'] is None or val < rec['min_x']:
                    rec['min_x'] = val
            elif key == 'x_right':
                if rec['max_x'] is None or val > rec['max_x']:
                    rec['max_x'] = val
            elif key == 'y_top':
                if rec['min_y'] is None or val < rec['min_y']:
                    rec['min_y'] = val
            elif key == 'y_bottom':
                if rec['max_y'] is None or val > rec['max_y']:
                    rec['max_y'] = val

    # Process from end to beginning
    for svg_start in sorted(svg_clamps.keys(), reverse=True):
        rec = svg_clamps[svg_start]
        svg_tag_end = new_content.find('>', svg_start) + 1
        opening = new_content[svg_start:svg_tag_end]
        vb = parse_viewbox(opening)
        if vb is None:
            print(f'  WARN: no viewBox in {relpath}')
            continue
        vb_x, vb_y, vb_w, vb_h = vb
        new_vb_x, new_vb_y = vb_x, vb_y
        new_vb_w, new_vb_h = vb_w, vb_h

        MARGIN = 5
        # Left
        if rec['min_x'] is not None and rec['min_x'] < vb_x + 1:
            shift = (vb_x + MARGIN) - rec['min_x']  # how much to push viewBox left
            new_vb_x -= shift
            new_vb_w += shift
        # Top
        if rec['min_y'] is not None and rec['min_y'] < vb_y + 1:
            shift = (vb_y + MARGIN) - rec['min_y']
            new_vb_y -= shift
            new_vb_h += shift
        # Right (rare for this check, but include)
        if rec['max_x'] is not None and rec['max_x'] > vb_x + vb_w - 1:
            shift = rec['max_x'] - (vb_x + vb_w - MARGIN)
            new_vb_w += shift
        # Bottom
        if rec['max_y'] is not None and rec['max_y'] > vb_y + vb_h - 1:
            shift = rec['max_y'] - (vb_y + vb_h - MARGIN)
            new_vb_h += shift

        if (new_vb_x == vb_x and new_vb_y == vb_y and
                new_vb_w == vb_w and new_vb_h == vb_h):
            continue

        new_vb_str = f'{fmt(new_vb_x)} {fmt(new_vb_y)} {fmt(new_vb_w)} {fmt(new_vb_h)}'
        new_opening = re.sub(
            r'(\bview[Bb]ox\s*=\s*")[^"]+(")',
            lambda m: m.group(1) + new_vb_str + m.group(2),
            opening, count=1
        )

        # Also bump max-width style if it's smaller than new vb width
        sty_re = re.compile(r'(max-width\s*:\s*)(\d+)(px)')
        sty_m = sty_re.search(new_opening)
        if sty_m:
            old_mw = int(sty_m.group(2))
            if old_mw < new_vb_w:
                new_mw = int(new_vb_w)
                new_opening = new_opening[:sty_m.start(2)] + str(new_mw) + new_opening[sty_m.end(2):]

        new_content = new_content[:svg_start] + new_opening + new_content[svg_tag_end:]
        total_updated += 1
        print(f'  {relpath}: viewBox ({vb_x},{vb_y},{vb_w},{vb_h}) -> ({new_vb_x},{new_vb_y},{new_vb_w},{new_vb_h})')

    if new_content != content:
        with open(full, 'w', encoding='utf-8', newline='') as f:
            f.write(new_content)
        files_updated += 1

print(f'\nSVGs updated: {total_updated}')
print(f'Files updated: {files_updated}')
