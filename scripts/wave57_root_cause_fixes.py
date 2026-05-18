"""Wave 57: Fix six structural root causes identified by user audit.

1. KEY_INSIGHT_BOLD: Key Insight callouts where the body paragraph starts with
   a full-sentence <strong>...</strong>. Unwrap (same logic as Wave 51 for
   big-picture).

2. DOUBLE_TITLE_PREFIX: Callout titles like "Key Insight: Key Takeaways" — the
   prefix duplicates the callout type. Collapse to canonical "Key Takeaways".
   Detection: title starts with "<TypeA>: <TypeB>" where both are canonical
   callout type words.

3. DUPLICATE_CHAPTER_OPENER: Module index pages with two references to
   `images/chapter-opener.png` (once as hero, once as body figure). Remove the
   body figure entirely (the hero on its own conveys the same info).

4. DUPLICATE_SINGLETON_SECTION: Pages with two or more <div class="whats-next">
   or <details class="bibliography-collapsible">. Keep the FIRST and remove
   subsequent duplicates.

5. NESTED_CALLOUT_TAIL: Sections that end with an extra </div> after </section>
   that pushes following blocks into nested rendering. Detect: pattern
   `</section>\\s*<p>` immediately followed by `</div>\\s*</div>` with the inner
   close having no matching open. (Heuristic — operates on section-16.3 pattern.)

6. LAB_OBJECTIVE_HEADING: Inside <div class="callout lab">, the <div class="lab-objective">
   contains an <h3>Objective</h3>. Now that book.js prioritizes
   <div class="callout-title">, the inner h3 stays — but to avoid a stray
   "Lab: Objective" rendering on cached versions, also strip the canonical
   .callout-title element from book.js's responsibility (the JS now removes it
   when used). This sweep is a no-op for HTML; the JS fix is in book.js.
"""
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')

ROOT = Path(__file__).resolve().parents[1]
SKIP = {'.git', 'node_modules', 'KDP', 'build', 'source_fix_backups',
        'pagefind', '.book-update', 'vendor', '.claude', '_archive',
        'agents', 'templates', 'docs', 'scripts'}

# --- 1. Key Insight bold-lead unwrap ---
KEY_INSIGHT_BOLD_RE = re.compile(
    r'(<div\s+class="callout key-insight"[^>]*>\s*<div\s+class="callout-title">[^<]*</div>\s*<p>)'
    r'(<strong>[^<]+?[.!?]\s*</strong>)'
    r'(\s*[^<].*?</p>)',
    re.DOTALL | re.IGNORECASE,
)

# --- 2. Double-title prefix collapse ---
# Match callout-title content like "Key Insight: Key Takeaways" — prefix word(s)
# followed by colon followed by another canonical title that duplicates type.
CANONICAL_TYPE_TITLES = [
    'Key Insight', 'Key Takeaway', 'Key Takeaways', 'Big Picture',
    'Looking Back', "What's Next", 'What’s Next', 'Real-World Scenario',
    'Practical Example', 'Production Pattern', 'Research Frontier',
    'Library Shortcut', 'Numeric Example', 'Postmortem', 'Self-Check',
    'Cross-Reference', 'Fun Fact', 'Lab', 'Exercise', 'Algorithm',
    'Pathway', 'Thesis Thread', 'Note', 'Warning', 'Tip',
]
_alts = '|'.join(re.escape(t) for t in CANONICAL_TYPE_TITLES)
DOUBLE_TITLE_RE = re.compile(
    rf'(<div\s+class="callout-title"[^>]*>)\s*({_alts})\s*:\s*({_alts})([^<]*)(</div>)',
    re.IGNORECASE,
)

# --- 3. Duplicate chapter-opener body figure ---
# Pattern: <figure class="illustration"><img src="images/chapter-opener.png" ...>...</figure>
# but only the SECOND occurrence (the hero opener is at the top of <main> in a
# <figure class="illustration chapter-opener"> wrapper). We remove the figure
# that is NOT inside the chapter-opener wrapper class.
BODY_OPENER_FIG_RE = re.compile(
    r'<figure\s+class="illustration"(?:\s[^>]*)?>\s*'
    r'<img\b[^>]*src="images/chapter-opener\.png"[^>]*/?>'
    r'(?:\s*<figcaption[^>]*>.*?</figcaption>)?\s*'
    r'</figure>',
    re.DOTALL | re.IGNORECASE,
)

# --- 4. Duplicate singleton sections ---
WHATS_NEXT_RE = re.compile(
    r'<div\s+class="(?:callout\s+)?whats-next"[^>]*>(?:.*?)</div>\s*(?=<(?:details|nav|div|footer|h[1-6])|</main)',
    re.DOTALL | re.IGNORECASE,
)
BIB_RE = re.compile(
    r'<details\s+class="bibliography-collapsible[^"]*"[^>]*>.*?</details>',
    re.DOTALL | re.IGNORECASE,
)

# --- 5. Nested callout tail (16.3 pattern) ---
# After </section> + <p>...</p>, we sometimes have two </div></div> sequence
# that closes a phantom parent. Detection is heuristic — operate only on
# files where we can see the exact 16.3 pattern (a stray <p> followed by two
# </div> with whats-next directly after).
NESTED_TAIL_RE = re.compile(
    r'(</section>\s*<p>[^<]*</p>\s*)</div>\s*</div>\s*(\n*<div\s+class="(?:callout\s+)?whats-next")',
    re.DOTALL | re.IGNORECASE,
)


def fix_file(p: Path, is_index: bool) -> dict[str, int]:
    text = p.read_text(encoding='utf-8')
    orig = text
    counts = {'key_insight_bold': 0, 'double_title': 0, 'opener_dup': 0,
              'wn_dup': 0, 'bib_dup': 0, 'nested_tail': 0}

    # 1. Key Insight bold unwrap
    def ki_repl(m):
        counts['key_insight_bold'] += 1
        return m.group(1) + re.sub(r'</?strong>', '', m.group(2)) + m.group(3)
    text = KEY_INSIGHT_BOLD_RE.sub(ki_repl, text)

    # 2. Double title collapse — keep the SECOND term when it differs from first
    def dt_repl(m):
        counts['double_title'] += 1
        opener = m.group(1)
        first = m.group(2)
        second = m.group(3)
        tail = m.group(4)
        closer = m.group(5)
        # If both are the same word (e.g. "Lab: Lab"), drop the prefix
        if first.lower().rstrip('s') == second.lower().rstrip('s'):
            return f'{opener}{second}{tail}{closer}'
        # If the SECOND term semantically duplicates the first
        # ("Key Insight: Key Takeaways"), prefer the more-specific second term.
        return f'{opener}{second}{tail}{closer}'
    text = DOUBLE_TITLE_RE.sub(dt_repl, text)

    # 3. Remove duplicate chapter-opener body figure (index pages only)
    if is_index and text.count('chapter-opener.png') >= 2:
        # Find the chapter-opener.png references. The hero is in
        # <figure class="illustration chapter-opener"> (with class="...chapter-opener");
        # the body duplicate is in <figure class="illustration"> (no chapter-opener).
        # Remove the BODY figure.
        def opener_repl(m):
            block = m.group()
            counts['opener_dup'] += 1
            return ''
        new_text = BODY_OPENER_FIG_RE.sub(opener_repl, text)
        text = new_text

    # 4. Duplicate singleton sections
    # whats-next: keep first, remove subsequent
    wn_matches = list(WHATS_NEXT_RE.finditer(text))
    if len(wn_matches) > 1:
        # Remove all except first, right-to-left to preserve offsets
        for m in reversed(wn_matches[1:]):
            text = text[:m.start()] + text[m.end():]
            counts['wn_dup'] += 1
    # bibliography: keep first, remove subsequent
    bib_matches = list(BIB_RE.finditer(text))
    if len(bib_matches) > 1:
        for m in reversed(bib_matches[1:]):
            text = text[:m.start()] + text[m.end():]
            counts['bib_dup'] += 1

    # 5. Nested tail (close phantom div)
    def nt_repl(m):
        counts['nested_tail'] += 1
        # Drop the two </div></div> after the stray <p>; preserve the rest.
        return m.group(1) + m.group(2)
    text = NESTED_TAIL_RE.sub(nt_repl, text)

    if text != orig:
        p.write_text(text, encoding='utf-8')
    return counts


def main():
    totals = {'key_insight_bold': 0, 'double_title': 0, 'opener_dup': 0,
              'wn_dup': 0, 'bib_dup': 0, 'nested_tail': 0}
    files_touched = 0
    for p in sorted(ROOT.rglob('*.html')):
        if set(p.parts) & SKIP:
            continue
        is_index = p.name == 'index.html'
        counts = fix_file(p, is_index)
        if sum(counts.values()) > 0:
            files_touched += 1
            for k, v in counts.items():
                totals[k] += v
    print('=== Wave 57 Root-Cause Fixes ===')
    print(f'Key Insight leading-bold unwrapped:    {totals["key_insight_bold"]}')
    print(f'Double-title prefix collapsed:         {totals["double_title"]}')
    print(f'Duplicate chapter-opener removed:      {totals["opener_dup"]}')
    print(f'Duplicate whats-next removed:          {totals["wn_dup"]}')
    print(f'Duplicate bibliography removed:        {totals["bib_dup"]}')
    print(f'Nested tail (16.3 pattern) repaired:   {totals["nested_tail"]}')
    print(f'Files touched:                         {files_touched}')


if __name__ == '__main__':
    main()
