"""Detect duplicate id="..." values within a single HTML file.

HTML requires id attributes to be unique within a document. Duplicates
break anchor navigation (a `<a href="#foo">` jumps to the FIRST element
with id="foo", silently shadowing the later one) and cause non-deterministic
behavior in JS-driven readers.

Common causes:
  - A subagent insert duplicates an id from a copy-pasted template
  - A heading renumber assigns the same numeric-slug id to two adjacent
    headings (e.g. id="5-1-2-foo" and id="5-1-2-bar")
  - Anchor targets carried over from a deleted-then-restored block
"""
import re
from collections import Counter, namedtuple

PRIORITY = "P2"
CHECK_ID = "DUPLICATE_ID"
DESCRIPTION = "Two or more elements in the same HTML file share an id attribute"

Issue = namedtuple("Issue", ["priority", "check_id", "filepath", "line", "message"])

ID_RE = re.compile(r'\sid="([^"]+)"')


def run(filepath, html, context):
    issues = []
    # Map id -> [line numbers where it appears]
    by_id = {}
    for i, line in enumerate(html.split("\n"), 1):
        for m in ID_RE.finditer(line):
            by_id.setdefault(m.group(1), []).append(i)

    for id_val, lines in by_id.items():
        if len(lines) > 1:
            issues.append(Issue(PRIORITY, CHECK_ID, filepath, lines[0],
                                f'Duplicate id="{id_val}" on lines {lines}'))
    return issues
