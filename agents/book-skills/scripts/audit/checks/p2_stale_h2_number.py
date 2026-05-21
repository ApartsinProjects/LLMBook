"""Detect h2/h3 elements where the id has a chapter number but the
display text starts with a DIFFERENT number.

Pattern (BAD):
  <h2 id="75-4-1-the-universal-recipe">80.4.1 The Universal Recipe</h2>
                ^^^                    ^^^
                new                    stale

This pattern emerged after the Part 14 drop renumbered modules and
sections but missed bare h2 display numbers. The id was updated (because
id substitution had an explicit context-anchored rule), but the display
text wasn't.

Detection: parse the id like "75-4-1-..." to get the canonical number
"75.4.1", then check if the display text starts with a different
"X.Y.Z" prefix.
"""
import re
from collections import namedtuple

PRIORITY = "P2"
CHECK_ID = "STALE_H2_NUMBER"
DESCRIPTION = "Heading display text starts with a different number than its id implies"

Issue = namedtuple("Issue", ["priority", "check_id", "filepath", "line", "message"])

H_RE = re.compile(
    r'<(h[23])\s+id="(\d+(?:-\d+){1,3})[^"]*"[^>]*>([^<]+?)</\1>',
    re.IGNORECASE | re.DOTALL,
)


def run(filepath, html, context):
    issues = []
    if not filepath.name.startswith("section-"):
        return issues
    for m in H_RE.finditer(html):
        tag = m.group(1)
        hid_nums = m.group(2)
        body = m.group(3).strip()
        expected = hid_nums.replace('-', '.')
        # Extract leading "X.Y" or "X.Y.Z" from body
        bm = re.match(r'^((?:\d+\.)+\d+)\s*', body)
        if not bm:
            continue
        stale = bm.group(1)
        if stale == expected:
            continue
        # Only flag if same depth (chapter.subsec vs chapter.subsec.subsubsec
        # are different concerns)
        if stale.count('.') != expected.count('.'):
            continue
        line = html[:m.start()].count('\n') + 1
        issues.append(Issue(
            PRIORITY, CHECK_ID, filepath, line,
            f'Heading {tag} id "{hid_nums}" implies "{expected}" but display text starts with "{stale}"'
        ))
    return issues
