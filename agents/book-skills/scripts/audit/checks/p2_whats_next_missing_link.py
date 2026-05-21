"""Detect What's Next blocks that lack a hyperlink to the next section.

Canonical (section-23.1.html):
    <div class="whats-next">
    <h2 id="what-comes-next">What Comes Next</h2>
    <p>In the next section, <a href="section-X.Y.html">Section X.Y: Title</a>, we ...</p>
    </div>

A whats-next block with no anchor inside is non-canonical (reader has no way
to click through).
"""
import re
from collections import namedtuple

PRIORITY = "P2"
CHECK_ID = "WHATS_NEXT_NO_LINK"
DESCRIPTION = "What's Next block lacks <a href> to the next section"

Issue = namedtuple("Issue", ["priority", "check_id", "filepath", "line", "message"])

WHATS_NEXT_RE = re.compile(
    r'<div\s+class="whats-next"[^>]*>([\s\S]*?)</div>\s*(?=<div|<h[1-6]|<nav|<details|<section)',
    re.IGNORECASE,
)


def _line(html, pos):
    return html.count("\n", 0, pos) + 1


def run(filepath, html, context):
    issues = []
    if filepath.suffix != ".html":
        return issues
    for m in WHATS_NEXT_RE.finditer(html):
        body = m.group(1)
        if '<a ' not in body and '<a\t' not in body:
            issues.append(Issue(
                PRIORITY, CHECK_ID, filepath, _line(html, m.start()),
                'What\'s Next block has no <a href> link to the next section',
            ))
    return issues
