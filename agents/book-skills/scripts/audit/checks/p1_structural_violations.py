"""Detect structural violations identified in user audits (waves 57-58).

Single plugin covers five distinct violations to keep audit output organized:
  1. DUPLICATE_SINGLETON: a page has >1 whats-next or >1 bibliography
  2. DOUBLE_TITLE_PREFIX: callout-title like "Key Insight: Key Takeaways"
     (the prefix duplicates the second canonical type word)
  3. KEY_INSIGHT_BOLD: Key Insight callout body opens with a full-sentence
     <strong>...</strong> (excess visual weight; bold should be key terms only)
  4. INDEX_DUPLICATE_OPENER: a module/part index references
     `images/chapter-opener.png` (or `images/part-opener.png`) more than once
  5. NON_CANONICAL_BIB: bibliography uses a bare h2 X.Y.Z References pattern
     or a summary label other than "Further Reading"
"""
import re
from collections import namedtuple

PRIORITY = "P1"
CHECK_ID = "STRUCTURAL_VIOLATION"
DESCRIPTION = "Structural canonical violation (duplicate singleton / double-title / bold-lead / non-canon bib)"

Issue = namedtuple("Issue", ["priority", "check_id", "filepath", "line", "message"])

WHATS_NEXT_RE = re.compile(
    r'<div\s+class="(?:callout\s+)?whats-next"', re.IGNORECASE,
)
BIB_RE = re.compile(
    r'<details\s+class="bibliography-collapsible[^"]*"', re.IGNORECASE,
)

# Canonical callout-type words (used in DOUBLE_TITLE check)
CANONICAL_TITLES = [
    'Key Insight', 'Key Takeaway', 'Key Takeaways', 'Big Picture',
    'Looking Back', "What's Next", 'What’s Next', 'Real-World Scenario',
    'Practical Example', 'Production Pattern', 'Research Frontier',
    'Library Shortcut', 'Numeric Example', 'Postmortem', 'Self-Check',
    'Cross-Reference', 'Fun Fact', 'Lab', 'Exercise', 'Algorithm', 'Thesis Thread', 'Note', 'Warning', 'Tip',
]
_alt = '|'.join(re.escape(t) for t in CANONICAL_TITLES)
DOUBLE_TITLE_RE = re.compile(
    rf'<div\s+class="callout-title"[^>]*>\s*({_alt})\s*:\s*({_alt})\b',
    re.IGNORECASE,
)
KEY_INSIGHT_BOLD_RE = re.compile(
    r'<div\s+class="callout key-insight"[^>]*>\s*<div\s+class="callout-title">[^<]+</div>\s*<p>\s*<strong>[^<]+?[.!?]\s*</strong>',
    re.IGNORECASE,
)
INDEX_OPENER_RE = re.compile(r'images/(?:chapter|part)-opener\.png', re.IGNORECASE)
BARE_REF_RE = re.compile(
    r'<h2\s+id="[^"]*-references?"[^>]*>[^<]*[Rr]eferences[^<]*</h2>\s*<div\s+class="bib-entries"',
    re.IGNORECASE,
)
NON_CANON_SUMMARY_RE = re.compile(
    r'<details\s+class="bibliography-collapsible[^"]*"[^>]*>\s*<summary[^>]*>((?:(?!</summary>).)*?)</summary>',
    re.DOTALL | re.IGNORECASE,
)


def _line(html, pos):
    return html.count("\n", 0, pos) + 1


def run(filepath, html, context):
    issues = []
    if filepath.suffix != ".html":
        return issues

    is_index = filepath.name == "index.html"

    # 1. Duplicate singleton sections
    wn_matches = list(WHATS_NEXT_RE.finditer(html))
    if len(wn_matches) > 1:
        for m in wn_matches[1:]:
            issues.append(Issue(
                PRIORITY, CHECK_ID, filepath, _line(html, m.start()),
                f'DUPLICATE_SINGLETON: extra whats-next block (only one allowed per section)',
            ))
    bib_matches = list(BIB_RE.finditer(html))
    if len(bib_matches) > 1:
        for m in bib_matches[1:]:
            issues.append(Issue(
                PRIORITY, CHECK_ID, filepath, _line(html, m.start()),
                f'DUPLICATE_SINGLETON: extra bibliography-collapsible (only one allowed)',
            ))

    # 2. Double-title prefix
    for m in DOUBLE_TITLE_RE.finditer(html):
        first = m.group(1)
        second = m.group(2)
        # Don't flag if first IS the second (or its singular/plural form)
        if first.lower().rstrip('s') == second.lower().rstrip('s'):
            continue
        issues.append(Issue(
            PRIORITY, CHECK_ID, filepath, _line(html, m.start()),
            f'DOUBLE_TITLE_PREFIX: callout-title "{first}: {second}..." (drop "{first}: " prefix)',
        ))

    # 3. Key Insight bold-lead
    for m in KEY_INSIGHT_BOLD_RE.finditer(html):
        issues.append(Issue(
            "P2", CHECK_ID, filepath, _line(html, m.start()),
            'KEY_INSIGHT_BOLD: Key Insight body opens with full-sentence <strong> (bold is for key terms only)',
        ))

    # 4. Index pages with duplicate chapter/part-opener.png
    if is_index:
        opener_count = len(INDEX_OPENER_RE.findall(html))
        if opener_count >= 2:
            # Find first occurrence line
            m = INDEX_OPENER_RE.search(html)
            issues.append(Issue(
                PRIORITY, CHECK_ID, filepath, _line(html, m.start()) if m else 1,
                f'INDEX_DUPLICATE_OPENER: chapter/part-opener.png referenced {opener_count}x (remove body figure duplicate)',
            ))

    # 5. Bare references h2 (non-canonical bibliography wrapper)
    for m in BARE_REF_RE.finditer(html):
        issues.append(Issue(
            PRIORITY, CHECK_ID, filepath, _line(html, m.start()),
            'NON_CANONICAL_BIB: bare <h2>...References</h2> + <div class="bib-entries"> — wrap in <details class="bibliography-collapsible">',
        ))

    # 6. Non-canonical summary label
    for m in NON_CANON_SUMMARY_RE.finditer(html):
        inner = re.sub(r'<[^>]+>', '', m.group(1)).strip()
        if inner.lower() != "further reading":
            issues.append(Issue(
                "P2", CHECK_ID, filepath, _line(html, m.start()),
                f'NON_CANONICAL_BIB: summary label "{inner[:50]}" (canonical: "Further Reading")',
            ))

    return issues
