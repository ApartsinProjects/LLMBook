"""Enforce the canonical 'See Also' pattern for cross-ref callouts.

Two rules are enforced (post wave-63 sweep):

  1. Title MUST be exactly 'See Also' (no variants like 'Cross-References',
     'Cross-Reference: ...', 'See also' lowercase 'a', or 'Canonical reference').
     The single canonical title is reader-friendlier than the legacy 'Canonical
     reference' phrasing and removes title fragmentation across the book.

  2. Body MUST contain at least one <a href="..."> link. A See Also callout
     with no target is useless to the reader (the whole point of a See Also
     is to navigate). Plain prose like "see Section 6.1" inside the callout
     without an anchor element is flagged.

Both rules apply to every callout whose opening tag is exactly:
    <div class="callout cross-ref">

Other callout-canonical checks (title prefix, structure) live in:
    - p2_callout_canonical_structure.py
    - p2_callout_title_prefix.py
This check is the stricter, per-type enforcement for cross-ref only.
"""
import re
from collections import namedtuple

PRIORITY = "P2"
CHECK_ID = "SEE_ALSO_CANONICAL"
DESCRIPTION = "Cross-ref callout deviates from canonical 'See Also' pattern (title or missing link)"

Issue = namedtuple("Issue", ["priority", "check_id", "filepath", "line", "message"])

# Exact canonical title (case-sensitive).
CANONICAL_TITLE = "See Also"

# Opening tag for cross-ref callout.
CROSS_REF_OPEN_RE = re.compile(r'<div\s+class="callout\s+cross-ref"\s*>', re.IGNORECASE)
# Match the first callout-title within the callout block.
TITLE_INNER_RE = re.compile(
    r'<div\s+class="callout-title"[^>]*>(.*?)</div>',
    re.IGNORECASE | re.DOTALL,
)
# Anchor with href.
HAS_LINK_RE = re.compile(r'<a\s+[^>]*href=', re.IGNORECASE)
# Tag stripper for title text comparison.
TAG_RE = re.compile(r'<[^>]+>')


def _line(html, pos):
    return html.count("\n", 0, pos) + 1


def _find_callout_block_end(html, start_pos):
    """Walk forward from start_pos and return the index just past the </div>
    that closes the callout. Uses simple depth tracking on <div>/</div>.

    start_pos is the offset immediately AFTER the opening <div class="callout cross-ref">.
    """
    depth = 1
    j = start_pos
    open_re = re.compile(r'<div\b', re.IGNORECASE)
    close_re = re.compile(r'</div>', re.IGNORECASE)
    while depth > 0 and j < len(html):
        no = open_re.search(html, j)
        nc = close_re.search(html, j)
        if not nc:
            return len(html)
        if no and no.start() < nc.start():
            depth += 1
            j = no.end()
        else:
            depth -= 1
            j = nc.end()
    return j


def run(filepath, html, context):
    issues = []
    if filepath.suffix != ".html":
        return issues

    for m in CROSS_REF_OPEN_RE.finditer(html):
        line = _line(html, m.start())
        block_end = _find_callout_block_end(html, m.end())
        block = html[m.start():block_end]

        # Rule 1: title must be exactly "See Also".
        tm = TITLE_INNER_RE.search(block)
        if not tm:
            issues.append(Issue(PRIORITY, CHECK_ID, filepath, line,
                "Cross-ref callout has no <div class='callout-title'>"))
        else:
            title_text = TAG_RE.sub('', tm.group(1)).strip()
            if title_text != CANONICAL_TITLE:
                issues.append(Issue(PRIORITY, CHECK_ID, filepath, line,
                    f"Cross-ref callout title is {title_text!r}, expected {CANONICAL_TITLE!r}"))

        # Rule 2: body must contain at least one <a href=...>.
        # Look only at the body (everything after the callout-title close).
        body_start = tm.end() if tm else m.end()
        body = block[body_start - m.start():]
        if not HAS_LINK_RE.search(body):
            issues.append(Issue(PRIORITY, CHECK_ID, filepath, line,
                "Cross-ref callout body has no <a href=...> link (See Also without targets is useless)"))

    return issues
