"""Detect SVG bottom-text-banners that duplicate the external figcaption.

Pattern: an SVG has a wide <rect> near the bottom of its viewBox with
prose-like <text> inside, repeating what the figcaption below the image
already says. Common shapes:
  <g transform="translate(40,460)">
    <rect width="1020" height="54" .../>
    <text font-weight="700">Ensembles outperform single detectors...</text>
    <text font-style="italic">Each model is fooled differently...</text>
  </g>

The visual effect is a caption-inside-the-diagram + a caption-below the
diagram. We flag when:
  1. SVG has a bottom-region <rect> spanning >= 70% of viewBox width
  2. The rect contains <text> with prose (3+ words)
  3. The text appears in the lower 30% of the viewBox

Author should drop the bottom banner and consolidate into the figcaption
prose if the message is worth keeping.
"""
import re
from collections import namedtuple

PRIORITY = "P2"
CHECK_ID = "DIAGRAM_BOTTOM_CAPTION"
DESCRIPTION = "SVG has a bottom-text-banner duplicating the external figcaption"

Issue = namedtuple("Issue", ["priority", "check_id", "filepath", "line", "message"])

SVG_OPEN = re.compile(
    r'<svg\b[^>]*viewBox\s*=\s*"([^"]+)"',
    re.IGNORECASE,
)
SVG_CLOSE = re.compile(r'</svg>', re.IGNORECASE)
G_TRANSLATE = re.compile(
    r'<g\s+transform\s*=\s*"translate\(\s*([\d.]+)\s*,\s*([\d.]+)\s*\)"[^>]*>'
    r'(.*?)</g>',
    re.IGNORECASE | re.DOTALL,
)
RECT_WIDTH = re.compile(r'<rect\s+[^>]*\bwidth\s*=\s*"(\d+)"', re.IGNORECASE)
TEXT_RE = re.compile(r'<text\b[^>]*>([^<]+)</text>', re.IGNORECASE)


def _scan_svg(svg_text: str):
    """Yield (line_offset, message) for each bottom banner."""
    m = SVG_OPEN.search(svg_text)
    if not m:
        return
    vb_parts = m.group(1).split()
    if len(vb_parts) != 4:
        return
    try:
        vb_w = float(vb_parts[2])
        vb_h = float(vb_parts[3])
    except ValueError:
        return
    for gm in G_TRANSLATE.finditer(svg_text):
        try:
            ty = float(gm.group(2))
        except ValueError:
            continue
        # Only the bottom region (y > 70% of viewBox height)
        if ty < vb_h * 0.70:
            continue
        body = gm.group(3)
        rm = RECT_WIDTH.search(body)
        if not rm:
            continue
        try:
            rect_w = float(rm.group(1))
        except ValueError:
            continue
        if rect_w < vb_w * 0.70:
            continue
        # Collect text content
        texts = [t.group(1).strip() for t in TEXT_RE.finditer(body)]
        texts = [t for t in texts if len(t.split()) >= 3]
        if not texts:
            continue
        yield (gm.start(), "; ".join(texts)[:120])


def run(filepath, html, context):
    issues = []
    if filepath.suffix not in (".html", ".svg"):
        return issues
    if filepath.suffix == ".svg":
        for offset, msg in _scan_svg(html):
            line = html.count("\n", 0, offset) + 1
            issues.append(Issue(PRIORITY, CHECK_ID, filepath, line,
                f'SVG bottom-banner text: "{msg}" (duplicates figcaption; drop or move to figcaption)'))
        return issues
    # HTML: scan each inline <svg>...</svg> block
    for m in re.finditer(r'<svg\b[\s\S]*?</svg>', html, re.IGNORECASE):
        svg_text = m.group(0)
        base_offset = m.start()
        for offset, msg in _scan_svg(svg_text):
            abs_offset = base_offset + offset
            line = html.count("\n", 0, abs_offset) + 1
            issues.append(Issue(PRIORITY, CHECK_ID, filepath, line,
                f'SVG bottom-banner text: "{msg}" (duplicates figcaption; drop or move to figcaption)'))
    return issues
