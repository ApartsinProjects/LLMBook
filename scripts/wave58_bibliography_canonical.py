"""Wave 58: Canonicalize all bibliography forms book-wide.

Canonical form (single source of truth):
    <details class="bibliography-collapsible" open>
    <summary><strong>Further Reading</strong></summary>
    <section class="bibliography">
      <div class="bib-entry-card">
        <div class="bib-ref">...</div>
      </div>
      <!-- optional <h3> group headings inside -->
      <div class="bib-entry-card">...</div>
    </section>
    </details>

Patterns flagged and converted:
1. Non-canonical "X.Y.Z References" pattern:
       <h2 id="X-Y-Z-references">X.Y.Z References</h2>
       <div class="bib-entries">
         <div class="bib-entry-card">...</div>
       </div>
   → wrap in canonical <details><summary>Further Reading</summary><section>.

2. Summary label != "Further Reading" (e.g., "Bibliography: the durable venues")
   → replace with canonical "Further Reading".

3. h2/h3 INSIDE bibliography section whose text IS just "References",
   "Bibliography", or "Further Reading" — redundant with the summary, remove.
"""
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')

ROOT = Path(__file__).resolve().parents[1]
SKIP = {'.git', 'node_modules', 'KDP', 'build', 'source_fix_backups',
        'pagefind', '.book-update', 'vendor', '.claude', '_archive',
        'agents', 'templates', 'docs', 'scripts'}

# Pattern 1: bare references h2 + bib-entries div
BARE_REF_BLOCK_RE = re.compile(
    r'<h2\s+id="[^"]*-references?"[^>]*>[^<]*[Rr]eferences[^<]*</h2>\s*'
    r'<div\s+class="bib-entries">(.*?)</div>\s*(?=<nav|<details|<footer|</main)',
    re.DOTALL | re.IGNORECASE,
)

# Pattern 2: non-canonical summary label
NON_CANON_SUMMARY_RE = re.compile(
    r'(<details\s+class="bibliography-collapsible[^"]*"[^>]*>\s*)<summary[^>]*>(?!\s*<strong>Further Reading</strong>\s*</summary>)(.*?)</summary>',
    re.DOTALL | re.IGNORECASE,
)

# Pattern 3: redundant h2/h3 inside <section class="bibliography"> whose text
# is just "References" / "Bibliography" / "Further Reading" (with optional
# section number prefix)
REDUNDANT_BIB_HEADING_RE = re.compile(
    r'(<section\s+class="bibliography"[^>]*>\s*)'
    r'<h[23][^>]*>\s*(?:\d+(?:\.\d+)*\s+)?(?:References|Bibliography|Further Reading)\s*</h[23]>',
    re.IGNORECASE,
)


def fix_file(p: Path) -> dict[str, int]:
    text = p.read_text(encoding='utf-8')
    orig = text
    counts = {'bare_ref_wrapped': 0, 'summary_canonical': 0, 'redundant_heading_removed': 0}

    # 1. Wrap bare references blocks in canonical details
    def bare_repl(m):
        counts['bare_ref_wrapped'] += 1
        inner = m.group(1)
        return (
            '<details class="bibliography-collapsible" open>\n'
            '<summary><strong>Further Reading</strong></summary>\n'
            '<section class="bibliography">\n'
            + inner
            + '\n</section>\n</details>\n'
        )
    text = BARE_REF_BLOCK_RE.sub(bare_repl, text)

    # 2. Canonical summary label
    def summary_repl(m):
        counts['summary_canonical'] += 1
        return m.group(1) + '<summary><strong>Further Reading</strong></summary>'
    text = NON_CANON_SUMMARY_RE.sub(summary_repl, text)

    # 3. Remove redundant heading inside <section class="bibliography">
    def heading_repl(m):
        counts['redundant_heading_removed'] += 1
        return m.group(1)
    text = REDUNDANT_BIB_HEADING_RE.sub(heading_repl, text)

    if text != orig:
        p.write_text(text, encoding='utf-8')
    return counts


def main():
    totals = {'bare_ref_wrapped': 0, 'summary_canonical': 0, 'redundant_heading_removed': 0}
    files_touched = 0
    for p in sorted(ROOT.rglob('*.html')):
        if set(p.parts) & SKIP:
            continue
        counts = fix_file(p)
        if sum(counts.values()) > 0:
            files_touched += 1
            for k, v in counts.items():
                totals[k] += v
    print('=== Wave 58 Bibliography Canonicalization ===')
    print(f'Bare X.Y.Z references wrapped in <details>: {totals["bare_ref_wrapped"]}')
    print(f'Summary label canonicalized:               {totals["summary_canonical"]}')
    print(f'Redundant inner heading removed:           {totals["redundant_heading_removed"]}')
    print(f'Files touched:                             {files_touched}')


if __name__ == '__main__':
    main()
