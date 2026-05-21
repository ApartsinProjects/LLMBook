"""Check for text in SVG shapes that overflows the shape boundaries.

Only checks at the top level of an SVG (text outside <g transform=...>),
because nested transforms make the (cx,cy) of the circle and the (x,y) of
the text live in different coordinate frames; the simple distance check
returns garbage in that case.
"""
import re
import html as html_mod
from collections import namedtuple

PRIORITY = "P2"
CHECK_ID = "SVG_TEXT_OVERFLOW"
DESCRIPTION = "SVG text likely overflows its containing shape"

Issue = namedtuple("Issue", ["priority", "check_id", "filepath", "line", "message"])

CIRCLE_RE = re.compile(r'<circle\b[^>]*?cx=["\']([^"\']+)["\'][^>]*?cy=["\']([^"\']+)["\'][^>]*?r=["\']([^"\']+)["\']')
TEXT_RE = re.compile(r'<text\b([^>]*)>([^<]+)</text>')
X_RE = re.compile(r'\bx=["\']([^"\']+)["\']')
Y_RE = re.compile(r'\by=["\']([^"\']+)["\']')
FSIZE_RE = re.compile(r'\bfont-size=["\']([^"\']+)["\']')
FONT_RE = re.compile(r'\bfont-family=["\']([^"\']+)["\']')

MONO_FONTS = {"consolas", "courier", "monospace", "source code pro", "fira code"}


def _estimate_width(text, font_size, font_family):
    decoded = html_mod.unescape(text.strip())
    char_count = len(decoded)
    is_mono = any(f in font_family.lower() for f in MONO_FONTS) if font_family else False
    factor = 0.62 if is_mono else 0.55
    return char_count * font_size * factor


def _walk_tokens(html_str):
    """Yield (kind, attrs_or_text, start_offset) where kind is one of
    'svg_open','svg_close','g_open','g_close','circle','text_open','text_full'.

    'text_full' includes the inner content between opening tag and </text>.
    """
    pat = re.compile(
        r'<svg\b[^>]*>|</svg>|<g\b([^>]*)>|</g>|<circle\b[^>]*?/>|<text\b[^>]*>',
        re.IGNORECASE | re.DOTALL,
    )
    for m in pat.finditer(html_str):
        tok = m.group(0)
        low = tok.lower()
        if low.startswith("<svg"):
            yield ("svg_open", tok, m.start())
        elif low.startswith("</svg"):
            yield ("svg_close", tok, m.start())
        elif low.startswith("</g"):
            yield ("g_close", tok, m.start())
        elif low.startswith("<g"):
            yield ("g_open", tok, m.start())
        elif low.startswith("<circle"):
            yield ("circle", tok, m.start())
        elif low.startswith("<text"):
            yield ("text_open", tok, m.start())


def run(filepath, html, context):
    issues = []
    if filepath.suffix != ".html":
        return issues

    # First pass: collect top-level circles per SVG (those NOT inside a
    # <g transform=...>). For now we look at ALL circles at top-level only.
    in_svg = False
    g_stack = []  # list[bool]: True if g has transform

    # Pre-compute per-SVG top-level circles by walking once.
    svg_circles = []   # list of (cx, cy, r, line, svg_index)
    svg_index = -1
    pat = re.compile(
        r'<svg\b[^>]*>|</svg>|<g\b([^>]*)>|</g>|<circle\b[^>]*/>',
        re.IGNORECASE | re.DOTALL,
    )
    for m in pat.finditer(html):
        tok = m.group(0)
        low = tok.lower()
        if low.startswith("<svg"):
            in_svg = True
            svg_index += 1
            g_stack = []
            continue
        if low.startswith("</svg"):
            in_svg = False
            g_stack = []
            continue
        if not in_svg:
            continue
        if low.startswith("</g"):
            if g_stack:
                g_stack.pop()
            continue
        if low.startswith("<g"):
            attrs = m.group(1) or ""
            g_stack.append("transform=" in attrs.lower())
            continue
        if low.startswith("<circle") and not any(g_stack):
            cm = CIRCLE_RE.search(tok)
            if cm:
                try:
                    cx, cy, r = float(cm.group(1)), float(cm.group(2)), float(cm.group(3))
                    line_num = html.count("\n", 0, m.start()) + 1
                    svg_circles.append((cx, cy, r, line_num, svg_index))
                except ValueError:
                    pass

    if not svg_circles:
        return issues

    # Second pass: text elements at top level only.
    in_svg = False
    g_stack = []
    current_svg_index = -1

    text_pat = re.compile(
        r'<svg\b[^>]*>|</svg>|<g\b([^>]*)>|</g>|<text\b[^>]*?>([^<]*)</text>',
        re.IGNORECASE | re.DOTALL,
    )
    for m in text_pat.finditer(html):
        tok = m.group(0)
        low = tok.lower()
        if low.startswith("<svg"):
            in_svg = True
            current_svg_index += 1
            g_stack = []
            continue
        if low.startswith("</svg"):
            in_svg = False
            g_stack = []
            continue
        if not in_svg:
            continue
        if low.startswith("</g"):
            if g_stack:
                g_stack.pop()
            continue
        if low.startswith("<g"):
            attrs = m.group(1) or ""
            g_stack.append("transform=" in attrs.lower())
            continue
        if low.startswith("<text"):
            if any(g_stack):
                continue
            # Parse text element with attrs and inner text
            tm = TEXT_RE.search(tok)
            if not tm:
                continue
            attrs = tm.group(1)
            text_content = tm.group(2).strip()
            x_match = X_RE.search(attrs)
            y_match = Y_RE.search(attrs)
            fsize_match = FSIZE_RE.search(attrs)
            font_match = FONT_RE.search(attrs)
            if not x_match or not y_match or not fsize_match:
                continue
            try:
                tx = float(x_match.group(1))
                ty = float(y_match.group(1))
                fsize = float(fsize_match.group(1))
            except ValueError:
                continue
            font_family = font_match.group(1) if font_match else ""
            est_width = _estimate_width(text_content, fsize, font_family)
            # Find nearest top-level circle in the same SVG. We use distance
            # < r * 0.8 (text anchor strictly inside the circle's inner 80%
            # area) to avoid false positives from text positioned just outside
            # one circle but close to another adjacent circle's edge.
            for cx, cy, r, _, c_svg_idx in svg_circles:
                if c_svg_idx != current_svg_index:
                    continue
                if r < 12:
                    continue
                dist = ((tx - cx) ** 2 + (ty - cy) ** 2) ** 0.5
                if dist < r * 0.8:
                    diameter = 2 * r
                    # Threshold 1.5x: text must be 50% wider than the diameter
                    # to be flagged. Below that, designers commonly position
                    # text labels just outside the circle on purpose (multi-line
                    # bubble labels). Visual rendering is fine.
                    if est_width > diameter * 1.5:
                        overflow_pct = int((est_width / diameter - 1) * 100)
                        decoded = html_mod.unescape(text_content)[:30]
                        line_num = html.count("\n", 0, m.start()) + 1
                        issues.append(Issue(PRIORITY, CHECK_ID, filepath, line_num,
                            f'Text "{decoded}" overflows circle (r={r:.0f}): '
                            f'est {est_width:.0f}px vs {diameter:.0f}px diameter '
                            f'(+{overflow_pct}%)'))
                    break

    return issues
