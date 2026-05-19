"""Detect <div class="callout algorithm"> blocks whose title lacks
"Algorithm X.Y.Z:" numbering.

Pattern (GOOD):
  <div class="callout-title">Algorithm 48.1.1: GCG Targeted Attack</div>

Pattern (BAD):
  <div class="callout-title">GCG Targeted Attack</div>
  <div class="callout-title">Algorithm: GCG Targeted Attack</div>

Detection: callout titles inside <div class="callout algorithm"> must
match: ^Algorithm\\s+\\d+\\.\\d+(\\.\\d+)?[a-z]?: .+
"""
import re
from collections import namedtuple

PRIORITY = "P2"
CHECK_ID = "ALGORITHM_NO_NUMBERING"
DESCRIPTION = "Algorithm callout title lacks canonical 'Algorithm X.Y.Z:' numbering"

Issue = namedtuple("Issue", ["priority", "check_id", "filepath", "line", "message"])

CALLOUT_TITLE_RE = re.compile(
    r'<div\s+class="callout\s+algorithm"[^>]*>\s*<div\s+class="callout-title"[^>]*>([^<]+)</div>',
    re.IGNORECASE | re.DOTALL,
)
NUMBERED_RE = re.compile(r'^Algorithm\s+\d+\.\d+(?:\.\d+)?[a-z]?:\s+\S', re.IGNORECASE)


def run(filepath, html, context):
    issues = []
    if not filepath.name.endswith('.html'):
        return issues
    for m in CALLOUT_TITLE_RE.finditer(html):
        title = m.group(1).strip()
        if NUMBERED_RE.match(title):
            continue
        line = html[:m.start()].count('\n') + 1
        issues.append(Issue(
            PRIORITY, CHECK_ID, filepath, line,
            f'Algorithm callout title "{title[:50]}" lacks "Algorithm X.Y.Z:" numbering'
        ))
    return issues
