"""Wave 72: Reorder singleton callouts to match canonical order.

Reads docs/content-audit/cycle_snapshots/cycle_38.json, filters CALLOUT_ORDER
issues, and for each affected section file rewrites the singleton callouts in
canonical order:

  1. big-picture
  2. prerequisites (div, NOT callout)
  3. research-frontier
  4. lab
  5. key-takeaway
  6. self-check
  7. exercises  (section.exercises OR h2#exercises + contiguous exercise callouts)
  8. whats-next
  9. bibliography (details.bibliography-collapsible)

Strategy: locate each singleton block via balanced-div matching, collect the
(canonical_index, start, end, html) tuples. If they are NOT already sorted by
start, snip them out, then re-insert them in canonical order at the position
of the FIRST singleton. Inter-singleton content (plural callouts, prose)
moves UP so it precedes the singletons, which matches the canonical "body
before singletons" rule.

Usage:
    python wave72_reorder_callouts.py [--dry] [--limit N] [--files glob]
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Optional

ROOT = Path('E:/Projects/BookBlogsHome/LLMBook')
SNAPSHOT = ROOT / 'docs' / 'content-audit' / 'cycle_snapshots' / 'cycle_38.json'

# Canonical ordering names (index in this list = canonical priority).
CANONICAL = [
    'big-picture',
    'prerequisites',
    'research-frontier',
    'lab',
    'key-takeaway',
    'self-check',
    'exercises',
    'whats-next',
    'bibliography',
]
RANK = {n: i for i, n in enumerate(CANONICAL)}

SKIP_HINTS = (
    '/tools-of-the-trade/', '/appendices/', '/appendix-',
    '/kdp/', '/build/',
    'module-05-tools', 'module-14-tools', 'module-19-tools',
    'module-30-tools', 'module-36-retrieval-tools', 'module-41-conv-ai',
    'module-45-tools', 'module-51-tools', 'module-56-responsible-ai',
    'module-61-scale', 'module-71-tools', 'module-79-tools',
)


def should_skip(p: Path) -> bool:
    s = str(p).lower().replace('\\', '/')
    if not p.name.startswith('section-'):
        return True
    return any(x in s for x in SKIP_HINTS)


# -------------------- balanced tag matcher --------------------

# We use a simple character-by-character scanner that tracks nested
# opening/closing tags of a given name.

def find_balanced(html: str, start: int, tag: str) -> int:
    """Return the index AFTER the closing </tag> that balances the opening
    tag at position `start`. The opening tag must already be located, but
    we re-parse it to allow attributes.

    Returns -1 if no match.
    """
    # Scan forward, counting nested <tag and </tag.
    tag_l = tag.lower()
    open_re = re.compile(rf'<{tag_l}\b', re.IGNORECASE)
    close_re = re.compile(rf'</{tag_l}\s*>', re.IGNORECASE)

    # Position of the opening tag's '<'
    # The first '<' may not be at `start` exactly; the caller passes the
    # match start. We need to step PAST that opening tag's '>' before
    # counting.
    # Find the '>' that closes the opening <tag ...>.
    pos = html.find('>', start)
    if pos == -1:
        return -1
    # Check if it's a self-closing tag (rare for div/section/details).
    if html[pos - 1:pos] == '/':
        return pos + 1
    cursor = pos + 1
    depth = 1
    while cursor < len(html) and depth > 0:
        # Find next open or close at this point.
        n_open = open_re.search(html, cursor)
        n_close = close_re.search(html, cursor)
        if not n_close:
            return -1
        if n_open and n_open.start() < n_close.start():
            # nested open
            # advance past its '>'
            after_gt = html.find('>', n_open.start())
            if after_gt == -1:
                return -1
            # account for self-closing
            if html[after_gt - 1:after_gt] == '/':
                cursor = after_gt + 1
                continue
            depth += 1
            cursor = after_gt + 1
        else:
            depth -= 1
            cursor = n_close.end()
    if depth == 0:
        return cursor
    return -1


# -------------------- singleton block locators --------------------

# Each returns (start, end) or None.

def find_simple_div(html: str, class_re: str) -> Optional[tuple[int, int]]:
    """Find a <div class="..."> matching class_re (used inside class=""),
    then balanced-match to its closing </div>.
    """
    pat = re.compile(rf'<div\s+class="{class_re}"', re.IGNORECASE)
    m = pat.search(html)
    if not m:
        return None
    end = find_balanced(html, m.start(), 'div')
    if end < 0:
        return None
    return (m.start(), end)


def find_details(html: str, class_re: str) -> Optional[tuple[int, int]]:
    pat = re.compile(rf'<details\s+class="{class_re}"', re.IGNORECASE)
    m = pat.search(html)
    if not m:
        return None
    end = find_balanced(html, m.start(), 'details')
    if end < 0:
        return None
    return (m.start(), end)


def find_exercises(html: str) -> Optional[tuple[int, int]]:
    """Locate the 'exercises' block.

    Variants:
      (A) <section class="exercises"> ... </section>
      (B) <h2 id="exercises">Exercises</h2> followed by one or more
          <div class="callout exercise"> ... </div> blocks (with optional
          whitespace and comments between).

    For (B) the block runs from the h2 start to the end of the LAST
    consecutive exercise-callout. Trailing whitespace is NOT included.
    """
    # Try (A)
    pat_a = re.compile(r'<section\s+class="exercises"', re.IGNORECASE)
    m_a = pat_a.search(html)
    if m_a:
        end_a = find_balanced(html, m_a.start(), 'section')
        if end_a > 0:
            return (m_a.start(), end_a)

    # Try (B)
    pat_h2 = re.compile(r'<h2\s+id="exercises"[^>]*>.*?</h2>', re.IGNORECASE | re.DOTALL)
    m_h2 = pat_h2.search(html)
    if not m_h2:
        return None
    start = m_h2.start()
    cursor = m_h2.end()
    # Skip whitespace and HTML comments; accept any number of consecutive
    # <div class="callout exercise"> blocks.
    ex_re = re.compile(r'<div\s+class="callout\s+exercise"', re.IGNORECASE)
    last_end = m_h2.end()
    while True:
        # Skip whitespace and comments.
        c = cursor
        while c < len(html):
            if html[c].isspace():
                c += 1
                continue
            if html.startswith('<!--', c):
                end_c = html.find('-->', c)
                if end_c == -1:
                    break
                c = end_c + 3
                continue
            break
        if c >= len(html):
            break
        m_ex = ex_re.match(html, c)
        if not m_ex:
            break
        end_ex = find_balanced(html, m_ex.start(), 'div')
        if end_ex < 0:
            break
        last_end = end_ex
        cursor = end_ex
    if last_end == m_h2.end():
        # No exercise callouts followed; treat the h2 alone as the block.
        return (start, last_end)
    return (start, last_end)


def find_whats_next(html: str) -> Optional[tuple[int, int]]:
    # Two forms: callout whats-next, or div.whats-next
    pat = re.compile(r'<div\s+class="(?:callout\s+)?whats-next"', re.IGNORECASE)
    m = pat.search(html)
    if not m:
        return None
    end = find_balanced(html, m.start(), 'div')
    if end < 0:
        return None
    return (m.start(), end)


def locate_singletons(html: str) -> list[tuple[int, int, int, str]]:
    """Return a list of (rank, start, end, name) for each singleton found.

    Sorted by start position.
    """
    found: list[tuple[int, int, int, str]] = []

    def add(name: str, span: Optional[tuple[int, int]]):
        if span is None:
            return
        s, e = span
        found.append((RANK[name], s, e, name))

    add('big-picture',       find_simple_div(html, r'callout\s+big-picture'))
    add('prerequisites',     find_simple_div(html, r'prerequisites'))
    add('research-frontier', find_simple_div(html, r'callout\s+research-frontier'))
    add('lab',               find_simple_div(html, r'callout\s+lab'))
    add('key-takeaway',      find_simple_div(html, r'callout\s+key-takeaway'))
    add('self-check',        find_simple_div(html, r'callout\s+self-check'))
    add('whats-next',        find_whats_next(html))
    add('bibliography',      find_details(html, r'bibliography-collapsible.*?'))

    # exercises handled separately
    ex_span = find_exercises(html)
    if ex_span is not None:
        s, e = ex_span
        found.append((RANK['exercises'], s, e, 'exercises'))

    found.sort(key=lambda t: t[1])
    return found


# -------------------- rewrite logic --------------------

def needs_reorder(spans: list[tuple[int, int, int, str]]) -> bool:
    # spans is already sorted by start; needs reorder iff ranks not non-decreasing
    last_rank = -1
    for r, s, e, n in spans:
        if r < last_rank:
            return True
        last_rank = r
    return False


class OverlapError(Exception):
    """Raised when singleton spans overlap, indicating malformed HTML
    (e.g., one singleton nested inside another). The file needs manual
    inspection before automated reordering can run safely.
    """


def reorder_html(html: str, spans: list[tuple[int, int, int, str]]) -> str:
    """Snip each span out and re-insert all of them in canonical order at the
    position of the first span. Preserves a single newline as a separator
    between re-inserted blocks.
    """
    if not spans:
        return html

    # Validate no overlaps.
    spans_sorted_by_start = sorted(spans, key=lambda t: t[1])
    for i in range(len(spans_sorted_by_start) - 1):
        if spans_sorted_by_start[i][2] > spans_sorted_by_start[i + 1][1]:
            outer = spans_sorted_by_start[i]
            inner = spans_sorted_by_start[i + 1]
            raise OverlapError(
                f'{outer[3]} (lines {html.count(chr(10), 0, outer[1])+1}-'
                f'{html.count(chr(10), 0, outer[2])+1}) contains '
                f'{inner[3]} (line {html.count(chr(10), 0, inner[1])+1})'
            )

    first_start = spans_sorted_by_start[0][1]

    # Extract block texts and their position info.
    blocks = []  # list of (rank, start, end, name, html)
    for rank, s, e, name in spans_sorted_by_start:
        blocks.append((rank, s, e, name, html[s:e]))

    # Build "remaining" HTML by stitching all gaps between blocks (and
    # before/after) together. We delete every block span.
    pieces = []
    cursor = 0
    for rank, s, e, name, body in blocks:
        pieces.append(html[cursor:s])
        cursor = e
    pieces.append(html[cursor:])
    stripped = ''.join(pieces)

    # Compute the insertion offset within `stripped`. After removing all
    # blocks, the position that previously was `first_start` is now at:
    #   first_start (because nothing before first_start was changed)
    insert_pos = first_start
    # However, we must be careful: any inter-block content shifts down.
    # Actually, characters AT or AFTER first_start in the original have
    # been compressed. The very first character at first_start in the
    # original is now whatever followed the first block (after deletion).
    # We want our singletons to appear AT `first_start`. Yes, insert_pos
    # is `first_start` because positions before that are untouched.

    # Order blocks canonically and join with '\n'.
    blocks_by_rank = sorted(blocks, key=lambda t: t[0])
    payload = '\n'.join(body for _, _, _, _, body in blocks_by_rank)

    # Make sure there is a newline before and after the inserted payload
    # so we do not glue HTML tags onto a non-block predecessor.
    prefix = stripped[:insert_pos]
    suffix = stripped[insert_pos:]
    if prefix and not prefix.endswith('\n'):
        payload = '\n' + payload
    if suffix and not suffix.startswith('\n'):
        payload = payload + '\n'

    return prefix + payload + suffix


# -------------------- main --------------------

def load_target_files() -> list[Path]:
    with SNAPSHOT.open('r', encoding='utf-8') as f:
        data = json.load(f)
    files = set()
    for issue in data['issues']:
        if issue['check_id'] == 'CALLOUT_ORDER':
            files.add(issue['file'])
    return sorted({ROOT / f.replace('\\', '/') for f in files})


def process(fp: Path, dry: bool) -> tuple[bool, str]:
    """Return (changed, summary). summary lists the singleton names in old vs new order."""
    if should_skip(fp):
        return False, 'skipped'
    html = fp.read_text(encoding='utf-8', errors='ignore')
    spans = locate_singletons(html)
    if not spans:
        return False, 'no singletons'
    if not needs_reorder(spans):
        return False, 'already ordered'

    old_order = [n for _, _, _, n in spans]
    new_html = reorder_html(html, spans)
    if new_html == html:
        return False, 'no change'

    # Verify the new ordering passes the audit's pairwise rule.
    new_spans = locate_singletons(new_html)
    new_order = [n for _, _, _, n in new_spans]
    last_rank = -1
    for r, _, _, _ in new_spans:
        if r < last_rank:
            summary = f'POSTCHECK FAIL old={old_order} new={new_order}'
            return False, summary
        last_rank = r

    if not dry:
        fp.write_text(new_html, encoding='utf-8')
    return True, f'old={old_order} new={new_order}'


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--dry', action='store_true', help='Do not write files')
    ap.add_argument('--limit', type=int, default=0, help='Process at most N files')
    ap.add_argument('--only', type=str, default=None,
                    help='Substring filter on filenames')
    args = ap.parse_args()

    targets = load_target_files()
    if args.only:
        sub = args.only.lower()
        targets = [t for t in targets if sub in str(t).lower()]
    if args.limit:
        targets = targets[:args.limit]

    changed = 0
    skipped = 0
    failed = 0
    no_change = 0
    examples = []
    manual_needed = []
    for fp in targets:
        try:
            did, summary = process(fp, args.dry)
        except OverlapError as exc:
            manual_needed.append((fp, str(exc)))
            continue
        except Exception as exc:
            failed += 1
            print(f'FAIL {fp}: {exc!r}')
            continue
        if did:
            changed += 1
            if len(examples) < 8:
                examples.append((fp.name, summary))
        elif summary == 'skipped':
            skipped += 1
        else:
            no_change += 1

    print()
    print(f'Total targets:    {len(targets)}')
    print(f'Changed:          {changed}')
    print(f'No change:        {no_change}')
    print(f'Skipped:          {skipped}')
    print(f'Failed:           {failed}')
    print(f'Manual needed:    {len(manual_needed)}')
    if examples:
        print()
        print('Sample changes:')
        for name, summary in examples:
            print(f'  {name}: {summary}')
    if manual_needed:
        print()
        print('Manual review needed (overlapping spans):')
        for fp, msg in manual_needed:
            rel = str(fp).replace(str(ROOT), '').lstrip('\\').lstrip('/')
            print(f'  {rel}: {msg}')


if __name__ == '__main__':
    main()
