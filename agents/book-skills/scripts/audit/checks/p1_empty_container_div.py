"""Check for empty container divs that render as blank boxes.

Specifically guards against stray `<div class="takeaways"></div>` and similar
container divs that have no content but render as a styled empty box.
"""
import re
from collections import namedtuple

PRIORITY = "P1"
CHECK_ID = "EMPTY_CONTAINER_DIV"
DESCRIPTION = "Empty container div renders as a blank styled box"

Issue = namedtuple("Issue", ["priority", "check_id", "filepath", "line", "message"])

# Classes that are container-shaped and should never be empty. (We do NOT
# flag every empty div, only ones whose class normally implies content.)
EMPTY_TRIGGER_CLASSES = {
    'takeaways',
    'whats-next',
    'big-picture',
    'prerequisites',
    'see-also',
    'further-reading',
    'self-check',
    'key-takeaways',
    'exercises',
    'callout-title',  # title-only callout with no body
}

EMPTY_DIV_RE = re.compile(r'<div class="([^"]+)">\s*</div>')


def run(filepath, html, context):
    issues = []
    for m in EMPTY_DIV_RE.finditer(html):
        classes = m.group(1).split()
        flagged = [c for c in classes if c in EMPTY_TRIGGER_CLASSES]
        if not flagged:
            continue
        line = html[:m.start()].count('\n') + 1
        issues.append(Issue(
            priority=PRIORITY,
            check_id=CHECK_ID,
            filepath=filepath,
            line=line,
            message=f'Empty <div class="{m.group(1)}"></div> renders as blank box',
        ))
    return issues
