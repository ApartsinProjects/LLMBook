"""Check for placeholder or pending content in published HTML files."""
import re
from collections import namedtuple

PRIORITY = "P1"
CHECK_ID = "PLACEHOLDER_CONTENT"
DESCRIPTION = "Placeholder or pending content detected in published page"

Issue = namedtuple("Issue", ["priority", "check_id", "filepath", "line", "message"])

PLACEHOLDER_PATTERNS = [
    re.compile(r'\bContent\s+pending\b', re.IGNORECASE),
    re.compile(r'\bTODO\b'),
    re.compile(r'\bFIXME\b'),
    re.compile(r'\bTBD\b'),
    re.compile(r'\bplaceholder\b', re.IGNORECASE),
    re.compile(r'\bwill be produced\b', re.IGNORECASE),
    re.compile(r'\bwill be generated\b', re.IGNORECASE),
    re.compile(r'\bcoming soon\b', re.IGNORECASE),
]

COMMENT_RE = re.compile(r'<!--.*?-->', re.DOTALL)
MAIN_OPEN = re.compile(r'<main[\s>]', re.IGNORECASE)
MAIN_CLOSE = re.compile(r'</main>', re.IGNORECASE)


def run(filepath, html, context):
    issues = []
    # Strip HTML comments to avoid false positives
    cleaned = COMMENT_RE.sub('', html)
    lines = cleaned.split("\n")
    in_main = False
    for i, line in enumerate(lines, 1):
        if MAIN_OPEN.search(line):
            in_main = True
        if MAIN_CLOSE.search(line):
            in_main = False
            continue
        if not in_main:
            continue
        for pat in PLACEHOLDER_PATTERNS:
            m = pat.search(line)
            if m:
                issues.append(Issue(PRIORITY, CHECK_ID, filepath, i,
                    f'Placeholder content found: "{m.group()}"'))
                break
    return issues
