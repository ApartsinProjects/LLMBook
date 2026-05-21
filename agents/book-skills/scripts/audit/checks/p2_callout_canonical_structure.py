"""Detect callouts whose structure deviates from the canonical pattern.

Canonical callout (from section-42.2.html and book.css):

    <div class="callout TYPE">
    <div class="callout-title">Title text</div>
    <p>Body</p>
    <!-- optional more body -->
    </div>

Deviations flagged:
  - Callout with <h3> or <h4> instead of <div class="callout-title">
  - Callout with no callout-title at all
  - Callout class with unknown / non-canonical type
  - Callout with `class="callout"` (no type modifier)
"""
import re
from collections import namedtuple

PRIORITY = "P2"
CHECK_ID = "CALLOUT_NON_CANONICAL"
DESCRIPTION = "Callout structure deviates from canonical (<div class=\"callout TYPE\"><div class=\"callout-title\">...)"

Issue = namedtuple("Issue", ["priority", "check_id", "filepath", "line", "message"])

# 23 canonical callout types (confirmed from book.css ::before icon definitions)
CANONICAL_TYPES = {
    "algorithm", "big-picture", "cross-ref", "exercise", "fun-note", "key-insight",
    "key-takeaway", "lab", "library-shortcut", "looking-back", "note",
    "numeric-example", "postmortem", "practical-example",
    "production-pattern", "research-frontier", "self-check",
    "tip", "under-the-hood", "warning", "whats-next",
}

CALLOUT_RE = re.compile(r'<div\s+class="callout(?:\s+([a-z-]+))?"', re.I)
# Within a callout block, look for the first child element
TITLE_RE = re.compile(r'<div\s+class="callout-title"', re.I)
H3_H4_RE = re.compile(r'<h[34]\b', re.I)


def _line(html, pos):
    return html.count("\n", 0, pos) + 1


def _block_end(html, start_pos):
    """Find the end of this callout block. Heuristic: look for </div> followed
    by a peer-level element."""
    m = re.search(r'</div>\s*(?=<(?:div|section|nav|details|footer|h[1-6]|p))', html[start_pos:])
    if not m:
        return len(html)
    return start_pos + m.end()


def run(filepath, html, context):
    issues = []
    if filepath.suffix != ".html":
        return issues

    for m in CALLOUT_RE.finditer(html):
        callout_type = m.group(1)
        line = _line(html, m.start())
        block_end = _block_end(html, m.end())
        block = html[m.end():block_end]

        # 1. Missing type modifier
        if not callout_type:
            issues.append(Issue(PRIORITY, CHECK_ID, filepath, line,
                'Callout has class="callout" with no type modifier'))
            continue

        # 2. Non-canonical type
        if callout_type not in CANONICAL_TYPES:
            issues.append(Issue(PRIORITY, CHECK_ID, filepath, line,
                f'Callout type "{callout_type}" not in canonical set'))

        # 3. Missing callout-title or using h3/h4 instead
        has_title = TITLE_RE.search(block[:500])
        has_h3_h4 = H3_H4_RE.search(block[:500])
        if not has_title:
            if has_h3_h4:
                issues.append(Issue(PRIORITY, CHECK_ID, filepath, line,
                    f'Callout ({callout_type}) uses <h3>/<h4> instead of <div class="callout-title">'))
            else:
                issues.append(Issue(PRIORITY, CHECK_ID, filepath, line,
                    f'Callout ({callout_type}) missing <div class="callout-title">'))

    return issues
