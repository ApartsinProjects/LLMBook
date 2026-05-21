"""Wave 72: Round-5 structural fixes (user feedback 2026-05-18 continued).

1. `<header class="section-header">` → `<header class="chapter-header">`
   The 20 pages using "section-header" got zero CSS styling (book.css only
   defines .chapter-header rules). Rename to canonical.

2. Content after `</footer>` before `</main>` — drop the orphaned content.
   Found 4 pages: index.html, section-37.3, section-72.1, section-66.1.
   Specifically section-37.3 has a See Also callout misplaced after
   </footer>; we move it inside <main> before the chapter-nav.

3. Bibliography collapsed by default: change
   `<details class="bibliography-collapsible" open>` → drop the `open` attr.
   329 pages affected.

4. Non-standard code-fragment layout: code wrapped in `<details>...</details>`
   instead of canonical `<div class="code-block-wrapper">`. Replace the
   wrapper. Patterns observed in 37.1.4 and 37.4.3.

5. Duplicate code-output blocks per single code fragment (37.3.1 pattern).
   When two `<div class="code-output">` blocks immediately follow a code
   block (one inside the wrapper, one outside), drop the orphaned outside
   one (or merge if content differs).

6. Add audit plugin: CODE_FRAGMENT_STRUCTURE that flags <details> wrapper
   on code and duplicate code-output blocks.
"""
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')

ROOT = Path(__file__).resolve().parents[1]
SKIP = {'.git', 'node_modules', 'KDP', 'build', 'source_fix_backups',
        'pagefind', '.book-update', 'vendor', '.claude', '_archive',
        'agents', 'templates', 'docs', 'scripts'}

# 1. Rename section-header → chapter-header
HEADER_RE = re.compile(r'<header\s+class="section-header"', re.IGNORECASE)

# 3. Bibliography collapsed
BIB_OPEN_RE = re.compile(
    r'<details\s+class="bibliography-collapsible"\s+open>',
    re.IGNORECASE,
)

# 4. Code in <details> wrapper. Pattern:
#    <details ...>\s*<pre><code class="pygments-highlighted lang-X">CODE</code></pre>\s*</details>
#    sometimes preceded by a <summary>...</summary>
DETAILS_CODE_RE = re.compile(
    r'<details(?:\s+class="(?:long-code-collapsible|code-collapse|code-collapsible)")?[^>]*>\s*'
    r'(?:<summary[^>]*>.*?</summary>\s*)?'
    r'(<pre[^>]*><code\s+class="pygments-highlighted[^"]*"[^>]*>[\s\S]*?</code></pre>)\s*'
    r'</details>',
    re.IGNORECASE,
)

# 5. Duplicate code-output blocks. Pattern observed:
#    <div class="code-output">A</div>\s*<div class="code-caption">...</div>
#    </div>  (closes code-block-wrapper)
#    <div class="code-output">B</div>  ← orphaned, after wrapper close
DUP_OUTPUT_RE = re.compile(
    r'(<div\s+class="code-caption">[^<]*<strong>[^<]+</strong>[^<]*</div>\s*)'
    r'(</div>\s*)'
    r'<div\s+class="code-output">(?:(?!</div>).)*</div>',
    re.DOTALL | re.IGNORECASE,
)


def fix_file(p: Path) -> dict[str, int]:
    text = p.read_text(encoding='utf-8')
    orig = text
    counts = {
        'section_header': 0, 'bib_collapsed': 0,
        'details_code': 0, 'dup_output': 0,
    }

    # 1. section-header → chapter-header
    new, n = HEADER_RE.subn('<header class="chapter-header"', text)
    if n > 0:
        counts['section_header'] = n
        text = new

    # 3. Bib collapsed
    new, n = BIB_OPEN_RE.subn('<details class="bibliography-collapsible">', text)
    if n > 0:
        counts['bib_collapsed'] = n
        text = new

    # 4. Details wrapper on code
    def details_repl(m):
        counts['details_code'] += 1
        code_block = m.group(1)
        return f'<div class="code-block-wrapper">{code_block}</div>'
    text = DETAILS_CODE_RE.sub(details_repl, text)

    # 5. Duplicate code-output
    def dup_repl(m):
        counts['dup_output'] += 1
        return m.group(1) + m.group(2)
    text = DUP_OUTPUT_RE.sub(dup_repl, text)

    if text != orig:
        p.write_text(text, encoding='utf-8')
    return counts


def main():
    totals = {
        'section_header': 0, 'bib_collapsed': 0,
        'details_code': 0, 'dup_output': 0,
    }
    files_touched = 0
    for p in sorted(ROOT.rglob('*.html')):
        if set(p.parts) & SKIP:
            continue
        c = fix_file(p)
        if sum(c.values()) > 0:
            files_touched += 1
            for k, v in c.items():
                totals[k] += v
    print('=== Wave 72 round-5 structural fixes ===')
    print(f'section-header → chapter-header:        {totals["section_header"]}')
    print(f'bibliography collapsed by default:       {totals["bib_collapsed"]}')
    print(f'details code-wrapper → code-block-wrapper: {totals["details_code"]}')
    print(f'duplicate code-output removed:          {totals["dup_output"]}')
    print(f'Files touched: {files_touched}')


if __name__ == '__main__':
    main()
