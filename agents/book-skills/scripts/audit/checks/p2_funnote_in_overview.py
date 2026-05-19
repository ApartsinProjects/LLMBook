"""Detect <div class="callout fun-note"> blocks nested inside
<div class="overview"> (the Chapter Overview block).

The book convention is: chapter overview is plain prose + maybe a
big-picture callout. Fun-notes belong AFTER the overview, not interleaved
with overview paragraphs.

Detection: walk the html. When we see <div class="overview">, track its
depth. If we encounter <div class="callout fun-note"> while inside the
overview's div tree, flag it.
"""
import re
from collections import namedtuple

PRIORITY = "P2"
CHECK_ID = "FUNNOTE_IN_OVERVIEW"
DESCRIPTION = 'Fun-note callout nested inside <div class="overview"> (should follow it)'

Issue = namedtuple("Issue", ["priority", "check_id", "filepath", "line", "message"])


def run(filepath, html, context):
    issues = []
    # Only check chapter index files
    if filepath.name != "index.html":
        return issues
    if "module-" not in str(filepath):
        return issues

    # Walk tokens
    tok_re = re.compile(
        r'<div\s+class="overview"\s*>|<div\s+class="callout\s+fun-note"|<div\b|</div>',
        re.IGNORECASE,
    )
    overview_depth = -1
    cur_depth = 0
    for m in tok_re.finditer(html):
        tok = m.group(0).lower()
        if 'class="overview"' in tok:
            overview_depth = cur_depth
            cur_depth += 1
        elif 'class="callout' in tok and 'fun-note' in tok:
            cur_depth += 1
            if overview_depth >= 0 and cur_depth > overview_depth + 1:
                # We are INSIDE the overview block AND deeper than the
                # overview's opening depth - that means the fun-note is
                # nested.
                line = html[:m.start()].count('\n') + 1
                issues.append(Issue(
                    PRIORITY, CHECK_ID, filepath, line,
                    'Fun-note callout nested inside <div class="overview">; should follow it'
                ))
        elif tok == '</div>':
            cur_depth -= 1
            if overview_depth >= 0 and cur_depth == overview_depth:
                overview_depth = -1
        else:
            # generic <div...>
            cur_depth += 1
    return issues
