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

# Wrapper-div classes whose internal headings are meta-info (visually styled
# as a small banner, not part of the main content outline).
META_WRAPPER_CLASSES = {
    "prerequisites", "prereqs", "learning-objectives", "objectives",
    "learning-outcomes", "outcomes", "callout",
}
# Match wrapper div opens: <div class="prerequisites">, <div class="callout TYPE">, etc.
META_OPEN_RE = re.compile(
    r'<div\s+class\s*=\s*"([^"]*)"',
    re.IGNORECASE,
)
META_CLOSE_RE = re.compile(r'</div>', re.IGNORECASE)


def is_inside_meta(html: str, pos: int) -> bool:
    """Return True if `pos` sits inside an open meta-info wrapper div."""
    # Walk through opens/closes before `pos` and track depth of meta wrappers.
    depth = 0
    for m in re.finditer(r'<div\s+class\s*=\s*"([^"]*)"|</div>', html[:pos], re.IGNORECASE):
        token = m.group()
        if token.startswith('</'):
            if depth > 0:
                depth -= 1
        else:
            classes = m.group(1).split()
            if any(c in META_WRAPPER_CLASSES for c in classes):
                depth += 1
            else:
                # Non-meta div — but we still increment because we need to
                # pair it with the right close. Track with a separate counter
                # by signaling "0 increment" via not changing depth (we only
                # pair meta opens to subsequent closes).
                # Simpler: bump depth so closes pair correctly; but then
                # non-meta wrappers would falsely shield meta headings. Use a
                # two-counter approach instead.
                pass
    # The naive single-counter approach above is wrong because </div> closes
    # apply to the most-recent <div>, not specifically to meta wrappers.
    # Fall back to a simpler heuristic: scan backward up to 1200 chars and
    # see if the nearest open <div> is a meta wrapper.
    window = html[max(0, pos - 1200):pos]
    last_open = None
    for m in META_OPEN_RE.finditer(window):
        last_open = m
    last_close_pos = window.rfind('</div>')
    if not last_open:
        return False
    if last_close_pos > last_open.start():
        return False
    classes = last_open.group(1).split()
    return any(c in META_WRAPPER_CLASSES for c in classes)


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
