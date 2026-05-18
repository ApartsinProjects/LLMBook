"""Check for heading level skips (e.g. h1 followed by h3, h2 followed by h4).

Skips headings inside canonical meta-info wrapper divs (prerequisites,
objectives, learning-outcomes, callouts) since those carry their own
visual hierarchy and aren't part of the section's content outline.
"""
import re
import os
from collections import namedtuple

PRIORITY = "P2"
CHECK_ID = "HEADING_HIERARCHY"
DESCRIPTION = "Heading level skip detected (e.g. h1 to h3)"

Issue = namedtuple("Issue", ["priority", "check_id", "filepath", "line", "message"])

HEADING_RE = re.compile(r'<(h[1-6])\b[^>]*>(.*?)</\1>', re.DOTALL | re.IGNORECASE)
TAG_RE = re.compile(r'<[^>]+>')

# Wrapper-div / aside classes whose internal headings are meta-info (visually
# styled as a small banner, not part of the main content outline).
META_WRAPPER_CLASSES = {
    "prerequisites", "prereqs", "learning-objectives", "objectives",
    "learning-outcomes", "outcomes", "callout",
    "section-internal-toc",   # <aside class="section-internal-toc"> with h3 toc heading
    "takeaways",              # <div class="takeaways"> with h2 Key Takeaways
    "page-breadcrumb",
}
# Match wrapper div opens: <div class="prerequisites">, <div class="callout TYPE">, etc.
META_OPEN_RE = re.compile(
    r'<div\s+class\s*=\s*"([^"]*)"',
    re.IGNORECASE,
)
META_CLOSE_RE = re.compile(r'</div>', re.IGNORECASE)


def is_inside_meta(html: str, pos: int) -> bool:
    """Return True if `pos` sits inside an open meta-info wrapper (div OR aside)."""
    # Heuristic: scan backward up to 1200 chars and see if the nearest meta
    # wrapper open tag is unclosed.
    window = html[max(0, pos - 1200):pos]
    # Find nearest opening of either <div class="META"> or <aside class="META">
    meta_open_re = re.compile(
        r'<(?:div|aside)\s+class\s*=\s*"([^"]*)"',
        re.IGNORECASE,
    )
    last_open = None
    for m in meta_open_re.finditer(window):
        classes = m.group(1).split()
        if any(c in META_WRAPPER_CLASSES or c in {"section-internal-toc"} for c in classes):
            last_open = m
    if not last_open:
        return False
    # Find nearest close of EITHER div or aside after the open
    close_re = re.compile(r'</(?:div|aside)>', re.IGNORECASE)
    last_close_pos = -1
    for m in close_re.finditer(window):
        if m.start() > last_open.start():
            last_close_pos = m.start()
    if last_close_pos != -1:
        return False
    return True


def run(filepath, html, context):
    # Only check section files
    basename = os.path.basename(filepath)
    if "section-" not in basename:
        return []

    issues = []
    prev_level = 0
    # Iterate over all headings in document order
    for m in HEADING_RE.finditer(html):
        tag = m.group(1).lower()
        level = int(tag[1])
        text = TAG_RE.sub('', m.group(2)).strip()
        # Skip headings inside meta-info wrappers — they don't break the
        # document's logical content outline.
        if is_inside_meta(html, m.start()):
            continue
        line_no = html.count("\n", 0, m.start()) + 1
        if prev_level > 0 and level > prev_level + 1:
            issues.append(Issue(PRIORITY, CHECK_ID, filepath, line_no,
                f'Heading skip: h{prev_level} to h{level} ("{text}")'))
        prev_level = level
    return issues
