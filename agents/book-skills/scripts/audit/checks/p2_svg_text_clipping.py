"""Detect SVG <text> elements whose coordinates fall outside or near the viewBox boundary.

Skips text elements inside <g transform=...> wrappers because their coordinates
are in a translated frame; negative or out-of-bounds coords are not real
clipping there.
"""
import re
from collections import namedtuple

PRIORITY = "P2"
CHECK_ID = "SVG_TEXT_CLIPPING"
DESCRIPTION = "SVG text element positioned near or outside viewBox boundary (likely clipped)"

Issue = namedtuple("Issue", ["priority", "check_id", "filepath", "line", "message"])

VIEWBOX_RE = re.compile(
    r'<svg\b[^>]*\bviewBox=["\']'
    r'\s*(-?[\d.]+)\s+(-?[\d.]+)\s+([\d.]+)\s+([\d.]+)\s*'
    r'["\']',
    re.IGNORECASE
)

TEXT_COORD_RE = re.compile(
    r'<text\b[^>]*?\bx=["\'](-?[\d.]+)["\'][^>]*?\by=["\'](-?[\d.]+)["\']',
    re.IGNORECASE
)
TEXT_COORD_RE2 = re.compile(
    r'<text\b[^>]*?\by=["\'](-?[\d.]+)["\'][^>]*?\bx=["\'](-?[\d.]+)["\']',
    re.IGNORECASE
)

# Tokens we care about within an SVG block.
SVG_TOKEN_RE = re.compile(
    r'<svg\b[^>]*>|</svg>|<g\b([^>]*)>|</g>|<text\b[^>]*>',
    re.IGNORECASE | re.DOTALL
)

MARGIN = 1


def run(filepath, html, context):
    issues = []
    if filepath.suffix != ".html":
        return issues

    # Walk tokens in order to maintain a g-stack so we know when text is
    # inside a <g transform=...> wrapper.
    current_vb = None  # (minX, minY, width, height)
    in_svg = False
    g_stack = []  # list[bool]: True if g has transform

    for m in re.finditer(
        r'<svg\b[^>]*>|</svg>|<g\b[^>]*>|</g>|<text\b[^>]*?>',
        html, re.IGNORECASE | re.DOTALL,
    ):
        tok = m.group(0)
        tok_lower = tok.lower()
        if tok_lower.startswith("<svg"):
            in_svg = True
            vb_match = VIEWBOX_RE.search(tok)
            if vb_match:
                current_vb = (
                    float(vb_match.group(1)),
                    float(vb_match.group(2)),
                    float(vb_match.group(3)),
                    float(vb_match.group(4)),
                )
            else:
                current_vb = None
        elif tok_lower.startswith("</svg"):
            in_svg = False
            current_vb = None
            g_stack = []
        elif tok_lower.startswith("</g"):
            if g_stack:
                g_stack.pop()
        elif tok_lower.startswith("<g"):
            g_stack.append("transform=" in tok_lower)
        elif tok_lower.startswith("<text"):
            if not in_svg or current_vb is None:
                continue
            if any(g_stack):
                continue
            # Extract x,y
            attrs_only = tok
            mxy = TEXT_COORD_RE.search(attrs_only)
            if mxy:
                tx, ty = float(mxy.group(1)), float(mxy.group(2))
            else:
                myx = TEXT_COORD_RE2.search(attrs_only)
                if not myx:
                    continue
                ty, tx = float(myx.group(1)), float(myx.group(2))
            vb_x, vb_y, vb_w, vb_h = current_vb
            max_x = vb_x + vb_w
            max_y = vb_y + vb_h
            clipped = []
            if tx < vb_x + MARGIN:
                clipped.append(f"x={tx} near left edge ({vb_x})")
            if tx > max_x - MARGIN:
                clipped.append(f"x={tx} near right edge ({max_x})")
            if ty < vb_y + MARGIN:
                clipped.append(f"y={ty} near top edge ({vb_y})")
            if ty > max_y - MARGIN:
                clipped.append(f"y={ty} near bottom edge ({max_y})")
            if clipped:
                line_num = html.count("\n", 0, m.start()) + 1
                # Extract text content (next chunk up to </text>)
                end = html.find("</text>", m.end())
                text_content = ""
                if end > 0:
                    text_content = re.sub(r"<[^>]+>", "", html[m.end():end]).strip()[:60]
                issues.append(Issue(
                    priority=PRIORITY,
                    check_id=CHECK_ID,
                    filepath=filepath,
                    line=line_num,
                    message=f"Text \"{text_content}\" may be clipped: {'; '.join(clipped)}",
                ))
    return issues
