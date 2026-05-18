"""Check for duplicate figure, table, or listing numbers within a single file.

Only counts numbers that appear INSIDE a caption-bearing element
(figcaption, code-caption, diagram-caption, table caption). Prose cross-
references and aria-labels are expected to repeat the same number and are
excluded.

Implementation detail: book HTML is often compact-formatted with both a caption
div and surrounding prose on a single line. We extract each caption-bearing
substring explicitly via regex and only count numbers that fall inside it.
"""
import re
from collections import defaultdict, namedtuple

PRIORITY = "P0"
CHECK_ID = "DUP_FIGURE_NUM"
DESCRIPTION = "Same Figure/Table/Listing number used multiple times in one file"

Issue = namedtuple("Issue", ["priority", "check_id", "filepath", "line", "message"])

NUM_RE = re.compile(r'(?:Figure|Table|Listing|Code Fragment)\s+(\d+\.\d+(?:\.\d+)?)')

# Caption substrings to extract — we only count numbers INSIDE these:
CAPTION_SUBSTRING_RE = re.compile(
    r'<figcaption\b[^>]*>(.*?)</figcaption>'
    r'|<div\s+class="(?:code-caption|diagram-caption)"[^>]*>(.*?)</div>'
    r'|<caption\b[^>]*>(.*?)</caption>',
    re.IGNORECASE | re.DOTALL,
)


def run(filepath, html, context):
    issues = []
    occurrences = defaultdict(list)
    for m in CAPTION_SUBSTRING_RE.finditer(html):
        caption_text = m.group(1) or m.group(2) or m.group(3) or ''
        line_no = html.count("\n", 0, m.start()) + 1
        # Only count the FIRST figure/table/listing/code-fragment number in
        # each caption. The caption's own number is always emitted at the
        # very start (e.g., "Code Fragment 42.9.3: ..."); any later mentions
        # are author-written cross-references to OTHER captions inside the
        # caption's descriptive text and must not be counted as duplicates.
        nm = NUM_RE.search(caption_text)
        if nm:
            occurrences[nm.group(0)].append(line_no)
    for label, lines in sorted(occurrences.items()):
        if len(lines) > 1:
            issues.append(Issue(PRIORITY, CHECK_ID, filepath, lines[0],
                f'Duplicate "{label}" on lines: {", ".join(str(l) for l in lines)}'))
    return issues
