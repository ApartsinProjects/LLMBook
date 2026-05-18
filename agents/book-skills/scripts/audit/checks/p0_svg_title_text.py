"""Flag SVG title-text headers, but only when the SVG lacks a descriptive aria-label.

The book has three layers of accessibility for each diagram:
  1. aria-label on the <svg> (screen-reader primary source)
  2. <text> visual title inside the SVG (sighted-reader header)
  3. <figcaption> below the SVG (document-level reference)

Earlier the check flagged ALL three as redundant. After the SVG aria-label
agent (wave 82-segment) wrote rich descriptive aria-labels on every SVG,
the inline text title is a deliberate visual choice for sighted readers,
not an accessibility duplication. We now only flag inline title text on
SVGs whose aria-label is missing, too short, or generic.
"""
import re
from collections import namedtuple

PRIORITY = "P3"
CHECK_ID = "SVG_TITLE_TEXT"
DESCRIPTION = "SVG contains a title-like <text> element that duplicates the external caption"

Issue = namedtuple("Issue", ["priority", "check_id", "filepath", "line", "message"])

# Match <text ... y="N" ... font-size="N" ... font-weight="bold" ...>long text</text>
TEXT_RE = re.compile(
    r'<text\b([^>]*)>([^<]{10,})</text>', re.IGNORECASE
)
Y_RE = re.compile(r'\by=["\'](\d+(?:\.\d+)?)["\']')
FSIZE_RE = re.compile(r'\bfont-size=["\'](\d+(?:\.\d+)?)["\']')
BOLD_RE = re.compile(r'\bfont-weight=["\'](?:bold|[67]00)["\']')


def _is_inside_svg(html, pos):
    """Check if position is inside an <svg> block."""
    before = html[:pos]
    last_open = before.rfind("<svg")
    last_close = before.rfind("</svg>")
    return last_open > last_close


def _enclosing_svg_aria_label(html, pos):
    """Return the aria-label of the <svg> enclosing pos, or '' if none/short."""
    before = html[:pos]
    last_open = before.rfind("<svg")
    if last_open < 0:
        return ""
    # Find the end of the opening tag
    tag_end = html.find(">", last_open)
    if tag_end < 0:
        return ""
    opening = html[last_open:tag_end]
    m = re.search(r'aria-label=["\']([^"\']+)["\']', opening)
    return m.group(1).strip() if m else ""


def run(filepath, html, context):
    issues = []
    lines = html.split("\n")
    for i, line_text in enumerate(lines, 1):
        for m in TEXT_RE.finditer(line_text):
            attrs = m.group(1)
            text_content = m.group(2).strip()

            # Must be bold or large font
            y_match = Y_RE.search(attrs)
            fsize_match = FSIZE_RE.search(attrs)
            is_bold = bool(BOLD_RE.search(attrs))

            if not y_match or not fsize_match:
                continue

            y_val = float(y_match.group(1))
            fsize_val = float(fsize_match.group(1))

            # Title criteria: near top (y <= 45), large font (>= 13), bold
            if y_val <= 45 and fsize_val >= 13 and is_bold:
                # Check word count (titles have 3+ words)
                words = text_content.split()
                if len(words) >= 3:
                    # Verify inside SVG
                    line_start = sum(len(lines[j]) + 1 for j in range(i - 1))
                    if not _is_inside_svg(html, line_start):
                        continue
                    # Exempt if the enclosing SVG has a descriptive aria-label
                    # (>= 30 chars and not generic). Descriptive aria-labels
                    # mean the inline title is purely visual for sighted
                    # readers, not an accessibility duplication.
                    aria = _enclosing_svg_aria_label(html, line_start)
                    if (len(aria) >= 30 and
                            aria.lower() not in ("diagram", "figure", "illustration", "image")):
                        continue
                    display = text_content[:60]
                    issues.append(Issue(PRIORITY, CHECK_ID, filepath, i,
                        f'SVG title text (redundant with caption): "{display}"'))
    return issues
