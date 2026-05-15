"""v809: Standardize bibliography section headers book-wide.

PROBLEM
=======
Across the book, bibliography sections use inconsistent (or missing)
top-level headers:
  - 224 `<section class="bibliography">` (canonical wrapper)
  - Some have `<h2>Bibliography</h2>`, `<h3>Bibliography</h3>`,
    `<h3>References</h3>`, `<h3>Further Reading</h3>`
  - Others have NO header — straight into `<div class="bib-category">`
  - User reports inconsistency: "sometimes absent, sometimes
    Bibliography section, sometimes different (bibliography,
    references etc.)"

STANDARD
========
Every bibliography section gets a canonical `<h3>Further Reading</h3>`
header as its FIRST child. The book's content is technical with
curated references, not a formal "Bibliography" — "Further Reading"
is more semantically accurate.

FIX
===
For each `<section class="bibliography">` (and similar wrappers):
  - If it already has an h2/h3 with "Bibliography", "References",
    or "Further Reading" → rename to "Further Reading"
  - If it has NO header → insert `<h3>Further Reading</h3>` at the top
"""
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[2]
SKIP = ['node_modules', '.git', 'output', 'backup', 'agents/', 'templates/',
        'KDP/build', 'KDP/html2pub', 'pagefind']


def is_skip(p):
    sp = str(p).replace('\\', '/')
    return any(s in sp for s in SKIP)


n_files = 0
n_inserted = 0
n_renamed = 0

# Pattern: <section class="bibliography"...> ... </section>
SECTION_RE = re.compile(
    r'(<section\s+class="bibliography[^"]*"[^>]*>)(\s*)(.*?)(</section>)',
    re.DOTALL
)


def process_section(m):
    global n_inserted, n_renamed
    open_tag = m.group(1)
    ws = m.group(2)
    body = m.group(3)
    close_tag = m.group(4)

    # Check if body starts with a Bibliography/References/Further Reading heading
    head_match = re.match(
        r'\s*<(h[1-6])[^>]*>\s*(Bibliography|References|Further Reading|Foundational Papers|Bibliographic References)\s*</\1>',
        body, re.IGNORECASE
    )

    if head_match:
        old_tag = head_match.group(1)
        old_text = head_match.group(2)
        # Normalize: always use <h3>Further Reading</h3>
        new_heading = '<h3>Further Reading</h3>'
        new_body = new_heading + body[head_match.end():]
        n_renamed += 1
        return open_tag + ws + new_body + close_tag

    # No matching heading — insert one at the top
    new_body = '<h3>Further Reading</h3>\n' + body
    n_inserted += 1
    return open_tag + ws + new_body + close_tag


for p in ROOT.rglob('*.html'):
    if is_skip(p):
        continue
    try:
        s = p.read_text(encoding='utf-8')
    except UnicodeDecodeError:
        continue
    orig = s
    s = SECTION_RE.sub(process_section, s)
    if s != orig:
        p.write_text(s, encoding='utf-8')
        n_files += 1

print(f'Bibliography header standardization:')
print(f'  Renamed existing heading: {n_renamed}')
print(f'  Inserted new heading:     {n_inserted}')
print(f'  Files touched:            {n_files}')
