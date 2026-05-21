"""Detect callout titles with duplicated word AND an emoji/icon
between the duplicates.

Pattern (BAD):
  <div class="callout-title">Key Takeaways: &#128204; Key Takeaways</div>
                            ^^^^^^^^^^^^^^^^^^^      ^^^^^^^^^^^^^^^^^

The CSS ::before pseudo-element already adds an icon for canonical
callout types. The emoji in title TEXT is a doubled icon. And the
duplicated word is a copy-paste template artifact.

Detection: title body matches pattern "<word>: <emoji-or-entity> <same-word>".
"""
import re
from collections import namedtuple

PRIORITY = "P2"
CHECK_ID = "DOUBLE_TITLE_EMOJI"
DESCRIPTION = "Callout title repeats its word around an emoji/icon"

Issue = namedtuple("Issue", ["priority", "check_id", "filepath", "line", "message"])

# Multi-line-safe regex. Word is captured; same word required after the
# emoji/entity.
PAT = re.compile(
    r'<div class="callout-title">'
    r'([\w\s\']+):\s+'
    r'(?:&#x?[\w]+;|[\U0001F300-\U0001FAFF☀-➿✀-➿]+)\s+'
    r'\1'
    r'\s*</div>',
    re.UNICODE,
)


def run(filepath, html, context):
    issues = []
    for m in PAT.finditer(html):
        line = html[:m.start()].count('\n') + 1
        word = m.group(1).strip()
        issues.append(Issue(
            PRIORITY, CHECK_ID, filepath, line,
            f'Callout title doubles its word ("{word}: <emoji> {word}"); CSS ::before already adds the icon'
        ))
    return issues
