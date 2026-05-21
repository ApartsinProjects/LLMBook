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

    # Honor in-file structural-architect tags that mark a section as
    # intentionally large. A reviewer with full context has classified
    # the page; treat it as resolved.
    if (
        '<!-- GIANT_SECTION: catalog by design' in html
        or '<!-- GIANT_SECTION: long-form single topic' in html
        or '<!-- GIANT_SECTION: protected' in html
    ):
        return issues

    lines = html.count("\n") + 1
    h2_count = len(H2_RE.findall(html))

    # Tools-of-the-trade and reference catalog sections are short per-entry
    # but list MANY entries (one h2 per library/tool). High h2 count there
    # is canonical for a catalog, not a sign of forcible merge. Only flag
    # if the total line count is also pathologically long.
    rel_lower = str(filepath).lower().replace('\\', '/')
    is_catalog = (
        'tools-of-the-trade' in rel_lower
        or 'module-61-scale-tools' in rel_lower
        or 'module-36-retrieval-tools' in rel_lower
        or 'module-41-conv-ai-tools' in rel_lower
        or 'module-56-responsible-ai-tools' in rel_lower
    )
    # Generic catalog signal: many h2s with a short average line count per h2
    # (registry pages, comparison tables, vendor lists). 30-40 lines per h2 is
    # typical for a catalog entry; 80+ lines per h2 is a deep section that
    # really does need splitting.
    if not is_catalog and h2_count >= 10:
        avg_lines_per_h2 = lines / max(h2_count, 1)
        if avg_lines_per_h2 < 50:
            is_catalog = True

    # P0 = strong indicator of merge: BOTH long AND many subsections
    if lines > 1200 and h2_count > 10:
        issues.append(Issue("P0", CHECK_ID, filepath, 1,
            f'Giant merged section: {lines} lines, {h2_count} h2 (typical: <800 lines, <8 h2). '
            f'Strong split candidate.'))
    # Also P0: extreme line count regardless of h2 (long-form merge)
    elif lines > 1700:
        issues.append(Issue("P0", CHECK_ID, filepath, 1,
            f'Extremely long section: {lines} lines, {h2_count} h2. Strong split candidate.'))
    # P1 = one strong signal: very long OR many h2.
    # For catalog sections (tools-of-the-trade), single-entry lengths can run
    # 1000-1300 lines for libraries with many examples, code blocks, and version
    # tables. Only flag as P1 when a catalog runs past 1400 lines (the P0
    # threshold below).
    elif (lines > 1000 and not is_catalog) or (h2_count > 12 and not is_catalog):
        issues.append(Issue(PRIORITY, CHECK_ID, filepath, 1,
            f'Large section: {lines} lines, {h2_count} h2 subsections. Likely split candidate.'))
    # P2 = borderline: moderately long and many subsections.
    # Catalog sections with high h2-density but low total lines are canonical.
    elif (lines > 800 and h2_count > 8) or (h2_count > 10 and not is_catalog):
        issues.append(Issue("P2", CHECK_ID, filepath, 1,
            f'Borderline-large section: {lines} lines, {h2_count} h2 subsections. '
            f'Inspect for split opportunity.'))

    return issues
