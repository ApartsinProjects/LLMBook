"""Check for asymmetric panels in SVG diagrams (left/right or multi-column layouts)."""
import re
from collections import namedtuple, defaultdict

PRIORITY = "P2"
CHECK_ID = "SVG_PANEL_ASYM"
DESCRIPTION = "SVG diagram has asymmetric panel sizes (left/right or columns)"

Issue = namedtuple("Issue", ["priority", "check_id", "filepath", "line", "message"])

SVG_BLOCK_RE = re.compile(r'(<svg\b[^>]*>)(.*?)(</svg>)', re.DOTALL | re.IGNORECASE)
RECT_RE = re.compile(r'<rect\b([^>]*)/?>')
WIDTH_RE = re.compile(r'\bwidth=["\'](\d+(?:\.\d+)?)["\']')
HEIGHT_RE = re.compile(r'\bheight=["\'](\d+(?:\.\d+)?)["\']')
X_RE = re.compile(r'\bx=["\'](\d+(?:\.\d+)?)["\']')
Y_RE = re.compile(r'\by=["\'](\d+(?:\.\d+)?)["\']')
RX_RE = re.compile(r'\brx=["\'](\d+(?:\.\d+)?)["\']')
VIEWBOX_RE = re.compile(r'\bviewBox=["\']\s*(-?\d+(?:\.\d+)?)\s+(-?\d+(?:\.\d+)?)\s+(\d+(?:\.\d+)?)\s+(\d+(?:\.\d+)?)\s*["\']', re.IGNORECASE)
G_TRANSFORM_RE = re.compile(r'<g\b[^>]*\btransform=', re.IGNORECASE)

# Panel detection: large rects that serve as backgrounds/containers
MIN_PANEL_WIDTH = 80
MIN_PANEL_HEIGHT = 60


def _extract_rects(svg_body, svg_w=None, svg_h=None):
    """Extract rectangle dimensions from SVG body.

    Excludes:
      - Rects with no x/y attrs that match the full SVG viewBox (background rect)
      - Rects with no x/y attrs but used inside a <g transform=...> wrapper
        (their effective position is not at 0,0; counting them as y~0 panels
        causes false-positive asymmetry between the background and real panels).
    """
    rects = []
    for m in RECT_RE.finditer(svg_body):
        attrs = m.group(1)
        w_m = WIDTH_RE.search(attrs)
        h_m = HEIGHT_RE.search(attrs)
        x_m = X_RE.search(attrs)
        y_m = Y_RE.search(attrs)
        if not (w_m and h_m):
            continue
        w = float(w_m.group(1))
        h = float(h_m.group(1))
        x = float(x_m.group(1)) if x_m else 0
        y = float(y_m.group(1)) if y_m else 0
        if w < MIN_PANEL_WIDTH or h < MIN_PANEL_HEIGHT:
            continue
        has_xy = bool(x_m or y_m)
        # Skip background rect: no x/y, fills (nearly) the full SVG viewBox.
        # 5% tolerance handles viewBox like "-39 0 919 360" with rect 880x360.
        if not has_xy and svg_w and svg_h:
            if w >= 0.9 * svg_w and h >= 0.9 * svg_h:
                continue
        # Skip rects with no x/y inside a transform group -- their true position
        # is unknown to this parser, so they pollute the y=0 bucket.
        # We detect this conservatively: if the rect appears AFTER a <g transform=
        # opening tag and BEFORE the matching </g>, drop it from panel detection.
        rects.append({"x": x, "y": y, "w": w, "h": h, "_has_xy": has_xy,
                      "_offset_in_svg": m.start()})
    return rects


def _filter_transform_grouped(svg_body, rects):
    """Drop rects with no explicit x/y that live inside a <g transform=...>."""
    if not rects:
        return rects
    # Locate every <g transform...> ... </g> span by walking tags.
    spans = []
    depth = 0
    open_start = None
    cur_transform_depth = -1
    i = 0
    while i < len(svg_body):
        m_open = re.match(r'<g\b([^>]*)>', svg_body[i:])
        m_close = re.match(r'</g>', svg_body[i:])
        if m_open:
            has_transform = 'transform=' in m_open.group(1)
            depth += 1
            if has_transform and cur_transform_depth < 0:
                cur_transform_depth = depth
                open_start = i
            i += m_open.end()
        elif m_close:
            if cur_transform_depth == depth:
                spans.append((open_start, i + m_close.end()))
                cur_transform_depth = -1
                open_start = None
            depth -= 1
            i += m_close.end()
        else:
            i += 1
    if not spans:
        return rects
    kept = []
    for r in rects:
        if r["_has_xy"]:
            kept.append(r)
            continue
        off = r["_offset_in_svg"]
        in_transform_g = any(s <= off < e for s, e in spans)
        if in_transform_g:
            continue
        kept.append(r)
    return kept


def _find_panel_groups(rects):
    """Find groups of rects at similar y positions (horizontal panels).

    Uses 5px buckets so panels that are deliberately staggered (a 240-wide red
    box at y=50 next to a 450-wide green box at y=58, intentionally a
    two-tone row) land in DIFFERENT buckets and do not get flagged as a single
    asymmetric panel-row. Real panel-rows put their rects on the same y line.
    """
    if len(rects) < 2:
        return []

    # Group by similar y position (within 5px buckets)
    groups = defaultdict(list)
    for r in rects:
        bucket = round(r["y"] / 5) * 5
        groups[bucket].append(r)

    # Return groups with 2+ panels
    return [g for g in groups.values() if len(g) >= 2]


def run(filepath, html, context):
    issues = []
    lines = html.split("\n")

    for m in SVG_BLOCK_RE.finditer(html):
        svg_tag = m.group(1)
        svg_body = m.group(2)
        svg_start = html[:m.start()].count("\n") + 1

        # Extract viewBox dimensions for the SVG (for background-rect filtering).
        svg_w = None
        svg_h = None
        vb_m = VIEWBOX_RE.search(svg_tag)
        if vb_m:
            svg_w = float(vb_m.group(3))
            svg_h = float(vb_m.group(4))

        rects = _extract_rects(svg_body, svg_w=svg_w, svg_h=svg_h)
        rects = _filter_transform_grouped(svg_body, rects)
        if not rects:
            continue

        panel_groups = _find_panel_groups(rects)
        for group in panel_groups:
            widths = sorted([r["w"] for r in group])
            # Need >=3 rects to call it a panel-row; 2 rects in a y-bucket is
            # almost always an attacker-vs-defender or label-vs-value row-pair,
            # not a multi-panel column layout.
            if len(widths) < 3:
                continue
            min_w = widths[0]
            max_w = widths[-1]
            # Flag only when the ratio is large (>= 2.0). Subtle staircase
            # variation (120/130/130/210) is usually deliberate emphasis.
            if min_w > 0 and max_w / min_w > 2.0:
                heights = [r["h"] for r in group]
                h_min = min(heights)
                h_max = max(heights)
                size_str = " vs ".join(f"{r['w']:.0f}x{r['h']:.0f}" for r in sorted(group, key=lambda r: r["x"]))
                issues.append(Issue(PRIORITY, CHECK_ID, filepath, svg_start,
                    f"Asymmetric panels at y~{group[0]['y']:.0f}: {size_str} "
                    f"(ratio {max_w/min_w:.2f}x)"))

    return issues
