#!/usr/bin/env python3
"""Add dashed annotation lines to SVGs where text labels point to shapes but lack connecting lines.

Finds inline SVGs in HTML files and adds subtle dashed lines connecting
label text elements to their nearest relevant shape when no such line exists.

Usage:
    python svg_add_annotation_lines.py [--dry-run] [--path FILE] [--verbose]
"""

import argparse
import math
import os
import re
import sys


def setup_encoding():
    """Ensure stdout can handle Unicode."""
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')


def parse_float(val, default=0.0):
    """Safely parse a float from an attribute value."""
    if val is None:
        return default
    try:
        return float(val)
    except (ValueError, TypeError):
        return default


def extract_attr(elem_str, attr_name):
    """Extract an attribute value from an element string."""
    m = re.search(rf'{attr_name}\s*=\s*"([^"]*)"', elem_str)
    if m:
        return m.group(1)
    m = re.search(rf"{attr_name}\s*=\s*'([^']*)'", elem_str)
    if m:
        return m.group(1)
    return None


def get_text_content(text_elem_str):
    """Extract visible text content from a <text> element string."""
    content = re.sub(r'<[^>]+>', '', text_elem_str)
    content = content.replace('&amp;', '&')
    content = content.replace('&lt;', '<')
    content = content.replace('&gt;', '>')
    content = content.replace('&rarr;', '->')
    content = content.replace('&larr;', '<-')
    content = content.replace('&times;', 'x')
    content = content.replace('&Sigma;', 'S')
    content = re.sub(r'&#\d+;', '', content)
    content = re.sub(r'&\w+;', '', content)
    return content.strip()


def distance(x1, y1, x2, y2):
    """Euclidean distance between two points."""
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)


def point_near_line_segment(px, py, lx1, ly1, lx2, ly2, threshold=15):
    """Check if point (px,py) is within threshold of line segment (lx1,ly1)-(lx2,ly2)."""
    seg_len = distance(lx1, ly1, lx2, ly2)
    if seg_len < 1:
        return distance(px, py, lx1, ly1) < threshold

    # Project point onto line
    t = ((px - lx1) * (lx2 - lx1) + (py - ly1) * (ly2 - ly1)) / (seg_len * seg_len)
    t = max(0, min(1, t))
    proj_x = lx1 + t * (lx2 - lx1)
    proj_y = ly1 + t * (ly2 - ly1)
    return distance(px, py, proj_x, proj_y) < threshold


def get_viewbox(svg_str):
    """Extract viewBox dimensions."""
    m = re.search(r'viewBox\s*=\s*"([^"]*)"', svg_str)
    if m:
        parts = m.group(1).split()
        if len(parts) == 4:
            return [float(p) for p in parts]
    return [0, 0, 600, 400]


# ---------- Parsing ----------

def parse_texts(svg_str):
    """Parse all <text> elements from an SVG string. Returns list of dicts."""
    texts = []
    for m in re.finditer(r'<text\b([^>]*)>(.*?)</text>', svg_str, re.DOTALL):
        full = m.group(0)
        content = get_text_content(full)
        if not content:
            continue

        x = parse_float(extract_attr(full, 'x'))
        y = parse_float(extract_attr(full, 'y'))
        anchor = extract_attr(full, 'text-anchor') or 'start'
        font_size = parse_float(extract_attr(full, 'font-size'), 12.0)
        fw = extract_attr(full, 'font-weight') or ''
        fstyle = extract_attr(full, 'font-style') or ''
        fill = extract_attr(full, 'fill') or '#000'

        texts.append({
            'x': x, 'y': y, 'text': content, 'anchor': anchor,
            'font_size': font_size, 'elem_str': full,
            'is_bold': 'bold' in fw,
            'is_italic': 'italic' in fstyle,
            'fill': fill,
        })
    return texts


def parse_shapes(svg_str):
    """Parse rect, circle, ellipse shapes. Returns list of dicts with bounding info."""
    shapes = []

    for m in re.finditer(r'<rect\b([^>]*?)/?>', svg_str):
        elem = m.group(0)
        x = parse_float(extract_attr(elem, 'x'))
        y = parse_float(extract_attr(elem, 'y'))
        w = parse_float(extract_attr(elem, 'width'))
        h = parse_float(extract_attr(elem, 'height'))
        if w > 500 and h > 200:
            continue  # background rect
        shapes.append({
            'tag': 'rect', 'cx': x + w / 2, 'cy': y + h / 2,
            'x1': x, 'y1': y, 'x2': x + w, 'y2': y + h,
            'elem': elem,
        })

    for m in re.finditer(r'<circle\b([^>]*?)/?>', svg_str):
        elem = m.group(0)
        cx = parse_float(extract_attr(elem, 'cx'))
        cy = parse_float(extract_attr(elem, 'cy'))
        r = parse_float(extract_attr(elem, 'r'))
        if r < 4:
            continue  # tiny marker dots
        shapes.append({
            'tag': 'circle', 'cx': cx, 'cy': cy,
            'x1': cx - r, 'y1': cy - r, 'x2': cx + r, 'y2': cy + r,
            'elem': elem,
        })

    for m in re.finditer(r'<ellipse\b([^>]*?)/?>', svg_str):
        elem = m.group(0)
        cx = parse_float(extract_attr(elem, 'cx'))
        cy = parse_float(extract_attr(elem, 'cy'))
        rx = parse_float(extract_attr(elem, 'rx'))
        ry = parse_float(extract_attr(elem, 'ry'))
        shapes.append({
            'tag': 'ellipse', 'cx': cx, 'cy': cy,
            'x1': cx - rx, 'y1': cy - ry, 'x2': cx + rx, 'y2': cy + ry,
            'elem': elem,
        })

    return shapes


def parse_lines(svg_str):
    """Parse <line> elements. Returns list of dicts."""
    lines = []
    for m in re.finditer(r'<line\b([^>]*?)/?>', svg_str):
        elem = m.group(0)
        lines.append({
            'x1': parse_float(extract_attr(elem, 'x1')),
            'y1': parse_float(extract_attr(elem, 'y1')),
            'x2': parse_float(extract_attr(elem, 'x2')),
            'y2': parse_float(extract_attr(elem, 'y2')),
        })
    return lines


# ---------- Heuristic filters ----------

def text_approx_bounds(t):
    """Approximate bounding box of a text element."""
    char_w = t['font_size'] * 0.6
    tw = len(t['text']) * char_w
    th = t['font_size']

    if t['anchor'] == 'middle':
        tx1 = t['x'] - tw / 2
    elif t['anchor'] == 'end':
        tx1 = t['x'] - tw
    else:
        tx1 = t['x']
    return tx1, t['y'] - th, tx1 + tw, t['y']


def is_inside_shape(px, py, shape, margin=5):
    """Check if a point is inside a shape bounding box (with margin)."""
    return (shape['x1'] - margin <= px <= shape['x2'] + margin and
            shape['y1'] - margin <= py <= shape['y2'] + margin)


def text_inside_any_shape(t, shapes):
    """Check if the text center falls inside any shape."""
    tx1, ty1, tx2, ty2 = text_approx_bounds(t)
    cx = (tx1 + tx2) / 2
    cy = (ty1 + ty2) / 2
    for s in shapes:
        if is_inside_shape(cx, cy, s):
            return True
    return False


def text_on_existing_line(t, lines):
    """Check if a text element sits on or near an existing line (edge label)."""
    tx1, ty1, tx2, ty2 = text_approx_bounds(t)
    cx = (tx1 + tx2) / 2
    cy = (ty1 + ty2) / 2
    for ln in lines:
        if point_near_line_segment(cx, cy, ln['x1'], ln['y1'], ln['x2'], ln['y2'], threshold=18):
            return True
    return False


def is_title(t, vb):
    """Check if text looks like a diagram title."""
    _, vy, _, _ = vb
    if t['y'] < vy + 40 and t['is_bold'] and t['anchor'] == 'middle':
        return True
    if t['y'] < vy + 35 and t['font_size'] >= 14:
        return True
    return False


def is_axis_label(t, vb):
    """Check if text is an axis label (at edges, or rotated)."""
    _, _, vw, vh = vb
    if 'transform' in t['elem_str'] and 'rotate' in t['elem_str']:
        return True
    if t['y'] > vh - 40:
        return True
    if t['x'] < 40 and t['font_size'] <= 12:
        return True
    return False


def looks_like_formula(text):
    """Check if text looks like a math formula rather than a plain label."""
    # Contains = sign with variables (e.g. "z = Swx + b")
    if '=' in text and len(text) > 5:
        return True
    return False


def is_annotation_label(t, shapes, lines, vb):
    """Conservative check: is this text an annotation label needing a connecting line?

    Requirements (all must be true):
    - Not a title or axis label
    - Short text (under 25 chars), not a formula
    - Not inside any shape (those are shape-interior labels)
    - Not sitting on an existing line (those are edge labels like weights)
    - Positioned near (20-100px) a shape but not overlapping
    - Font size 10-13 (typical annotation size)
    - Preferably has comment context like <!-- Labels --> nearby
    """
    if is_title(t, vb):
        return False
    if is_axis_label(t, vb):
        return False

    text = t['text']
    if len(text) > 25:
        return False
    if len(text) < 2:
        return False

    # Skip arrow chars, pure numbers, single symbols
    if text in ['->', '<-', '|', '/', '\\', '+', '=', '...']:
        return False
    if re.match(r'^[\d.,%]+$', text):
        return False

    # Skip formulas
    if looks_like_formula(text):
        return False

    # Skip italic text on lines (weight labels like w1, w2)
    if t['is_italic']:
        return False

    # Must be smallish font (labels, not headings)
    if t['font_size'] > 13:
        return False
    if t['font_size'] < 9:
        return False

    # Must not be inside a shape
    if text_inside_any_shape(t, shapes):
        return False

    # Must not be sitting on an existing line
    if text_on_existing_line(t, lines):
        return False

    # Must be near a shape (20-100px from center)
    min_dist = float('inf')
    for s in shapes:
        d = distance(t['x'], t['y'], s['cx'], s['cy'])
        min_dist = min(min_dist, d)

    if min_dist > 80:
        return False
    if min_dist < 5:
        return False  # Overlapping, probably inside

    return True


# ---------- Line generation ----------

def find_nearest_shape(t, shapes):
    """Return (shape, distance) for the nearest shape."""
    best = None
    best_d = float('inf')
    for s in shapes:
        d = distance(t['x'], t['y'], s['cx'], s['cy'])
        if d < best_d:
            best_d = d
            best = s
    return best, best_d


def has_existing_connection(t, shape, lines, threshold=30):
    """Check if a line already connects the text area to the shape area."""
    tx1, ty1, tx2, ty2 = text_approx_bounds(t)
    tcx = (tx1 + tx2) / 2
    tcy = (ty1 + ty2) / 2

    for ln in lines:
        nt1 = distance(ln['x1'], ln['y1'], tcx, tcy) < threshold
        nt2 = distance(ln['x2'], ln['y2'], tcx, tcy) < threshold
        ns1 = distance(ln['x1'], ln['y1'], shape['cx'], shape['cy']) < threshold + 20
        ns2 = distance(ln['x2'], ln['y2'], shape['cx'], shape['cy']) < threshold + 20
        if (nt1 and ns2) or (nt2 and ns1):
            return True
    return False


def compute_annotation_line(t, shape):
    """Compute start/end for a dashed line from text to shape. Returns None if unsuitable."""
    tx1, ty1, tx2, ty2 = text_approx_bounds(t)
    tcx = (tx1 + tx2) / 2
    tcy = (ty1 + ty2) / 2

    dx = shape['cx'] - tcx
    dy = shape['cy'] - tcy
    dist = math.sqrt(dx * dx + dy * dy)
    if dist < 1:
        return None

    # Start point: from edge of text bounding box toward shape
    if abs(dy) > abs(dx):
        if dy > 0:
            sx, sy = tcx, ty2 + 2
        else:
            sx, sy = tcx, ty1 - 2
    else:
        if dx > 0:
            sx, sy = tx2 + 2, tcy
        else:
            sx, sy = tx1 - 2, tcy

    # End point: at shape edge
    if shape['tag'] == 'circle':
        r = (shape['x2'] - shape['x1']) / 2
        ndx = dx / dist
        ndy = dy / dist
        ex = shape['cx'] - ndx * (r + 2)
        ey = shape['cy'] - ndy * (r + 2)
    else:
        if abs(dy) > abs(dx):
            ey = shape['y1'] - 2 if dy > 0 else shape['y2'] + 2
            ratio = (ey - tcy) / dy if dy != 0 else 0
            ex = tcx + dx * ratio
            ex = max(shape['x1'], min(shape['x2'], ex))
        else:
            ex = shape['x1'] - 2 if dx > 0 else shape['x2'] + 2
            ratio = (ex - tcx) / dx if dx != 0 else 0
            ey = tcy + dy * ratio
            ey = max(shape['y1'], min(shape['y2'], ey))

    line_len = distance(sx, sy, ex, ey)
    if line_len < 10 or line_len > 70:
        return None

    return round(sx, 1), round(sy, 1), round(ex, 1), round(ey, 1)


# ---------- Idempotency ----------

ANNOTATION_MARKER = 'data-annotation-line="auto"'


def make_line_element(x1, y1, x2, y2):
    """Create the dashed annotation line SVG element."""
    return (f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" '
            f'stroke="#999" stroke-width="1" stroke-dasharray="4 3" '
            f'opacity="0.7" {ANNOTATION_MARKER}/>')


# ---------- Processing ----------

def process_svg(svg_str, verbose=False):
    """Analyze one SVG and return (modified_svg, addition_count)."""
    if ANNOTATION_MARKER in svg_str:
        return svg_str, 0

    vb = get_viewbox(svg_str)
    texts = parse_texts(svg_str)
    shapes = parse_shapes(svg_str)
    lines = parse_lines(svg_str)

    if not texts or not shapes:
        return svg_str, 0

    additions = []

    for t in texts:
        if not is_annotation_label(t, shapes, lines, vb):
            continue

        nearest, dist = find_nearest_shape(t, shapes)
        if nearest is None:
            continue

        if has_existing_connection(t, nearest, lines, threshold=30):
            continue

        endpoints = compute_annotation_line(t, nearest)
        if endpoints is None:
            continue

        x1, y1, x2, y2 = endpoints

        if verbose:
            safe_text = t['text'].encode('ascii', 'replace').decode()
            print(f"    Label: '{safe_text}' at ({t['x']},{t['y']}) -> "
                  f"{nearest['tag']} at ({nearest['cx']},{nearest['cy']}), "
                  f"line: ({x1},{y1})->({x2},{y2})")

        additions.append((t['elem_str'], make_line_element(x1, y1, x2, y2)))

    if not additions:
        return svg_str, 0

    modified = svg_str
    for text_str, line_str in additions:
        modified = modified.replace(text_str, line_str + '\n            ' + text_str, 1)

    return modified, len(additions)


def process_file(filepath, dry_run=False, verbose=False):
    """Process a single HTML file. Returns number of annotation lines added."""
    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()

    svg_pat = re.compile(r'(<svg\b[^>]*>.*?</svg>)', re.DOTALL)
    total = 0

    def replace_svg(m):
        nonlocal total
        mod, count = process_svg(m.group(1), verbose=verbose)
        total += count
        return mod

    new_content = svg_pat.sub(replace_svg, content)

    if total > 0 and not dry_run:
        with open(filepath, 'w', encoding='utf-8', newline='\n') as f:
            f.write(new_content)

    return total


def find_html_files(root_dir):
    """Recursively find HTML files, skipping hidden/vendor dirs."""
    skip = {'.git', 'node_modules', '.venv', '__pycache__', 'scripts'}
    result = []
    for dirpath, dirnames, filenames in os.walk(root_dir):
        dirnames[:] = [d for d in dirnames if d not in skip]
        for fn in filenames:
            if fn.endswith('.html'):
                result.append(os.path.join(dirpath, fn))
    return sorted(result)


def main():
    setup_encoding()

    parser = argparse.ArgumentParser(
        description='Add dashed annotation lines to SVGs with unconnected labels.')
    parser.add_argument('--dry-run', action='store_true',
                        help='Report what would change without modifying files')
    parser.add_argument('--path', type=str, default=None,
                        help='Process a single file instead of the whole project')
    parser.add_argument('--verbose', action='store_true',
                        help='Print details about each annotation line added')
    args = parser.parse_args()

    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    if args.path:
        files = [os.path.abspath(args.path)]
    else:
        files = find_html_files(root)

    tag = "[DRY RUN] " if args.dry_run else ""
    print(f"{tag}Scanning {len(files)} HTML file(s) for SVGs needing annotation lines...")

    files_changed = 0
    lines_added = 0

    for fp in files:
        count = process_file(fp, dry_run=args.dry_run, verbose=args.verbose)
        if count > 0:
            rel = os.path.relpath(fp, root)
            print(f"  {tag}{rel}: +{count} annotation line(s)")
            files_changed += 1
            lines_added += count

    print(f"\n{tag}Summary: {lines_added} annotation line(s) added across {files_changed} file(s).")


if __name__ == '__main__':
    main()
