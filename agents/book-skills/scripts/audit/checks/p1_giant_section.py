"""Detect giant sections that may be forcibly-merged or need splitting.

The canonical section page has 5-7 `<h2>` subsections and runs 200-700 lines.
Pages well outside that envelope are candidates for splitting:
  - Lines > 1200: clearly merged or over-long
  - h2 count > 10: too many subsections for one section
  - h2 count > 7 AND lines > 800: borderline candidates
"""
import re
from collections import namedtuple

PRIORITY = "P1"
CHECK_ID = "GIANT_SECTION"
DESCRIPTION = "Section page is unusually large (likely forcibly-merged; consider splitting)"

Issue = namedtuple("Issue", ["priority", "check_id", "filepath", "line", "message"])

H2_RE = re.compile(r'<h2\b', re.I)


def run(filepath, html, context):
    issues = []
    if not filepath.name.startswith("section-"):
        return issues
    lines = html.count("\n") + 1
    h2_count = len(H2_RE.findall(html))

    # P0 = strong indicator of merge: BOTH long AND many subsections
    if lines > 1200 and h2_count > 10:
        issues.append(Issue("P0", CHECK_ID, filepath, 1,
            f'Giant merged section: {lines} lines, {h2_count} h2 (typical: <800 lines, <8 h2). '
            f'Strong split candidate.'))
    # Also P0: extreme line count regardless of h2 (long-form merge)
    elif lines > 1700:
        issues.append(Issue("P0", CHECK_ID, filepath, 1,
            f'Extremely long section: {lines} lines, {h2_count} h2. Strong split candidate.'))
    # P1 = one strong signal: very long OR many h2
    elif lines > 1000 or h2_count > 12:
        issues.append(Issue(PRIORITY, CHECK_ID, filepath, 1,
            f'Large section: {lines} lines, {h2_count} h2 subsections. Likely split candidate.'))
    # P2 = borderline: moderately long and many subsections
    elif (lines > 800 and h2_count > 8) or h2_count > 10:
        issues.append(Issue("P2", CHECK_ID, filepath, 1,
            f'Borderline-large section: {lines} lines, {h2_count} h2 subsections. '
            f'Inspect for split opportunity.'))

    return issues
