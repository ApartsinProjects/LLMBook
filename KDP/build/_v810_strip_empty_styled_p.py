"""v810: Strip empty <p style="text-align: center..."> wrappers
that surround math-block divs. These were author-added before
v804 converted the inner span.math to div.math-block. The <p>
auto-closes when the HTML parser hits the <div>, leaving the
opening <p style=...> as a sibling empty paragraph.
"""
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[2]
SKIP = ['node_modules', '.git', 'output', 'backup', 'agents/', 'templates/',
        'KDP/build', 'KDP/html2epub', 'pagefind']


def is_skip(p):
    sp = str(p).replace('\\', '/')
    return any(s in sp for s in SKIP)


# Pattern: <p style="text-align: center; ..."> followed by <div class="math-block">
# Replace the standalone opening <p style=...> with nothing.
PATTERN = re.compile(
    r'<p\s+style="[^"]*text-align[^"]*"\s*>\s*\n?\s*(?=<div\s+class="math-block")',
    re.IGNORECASE
)
# And the closing </p> that follows the </div>
CLOSE_PATTERN = re.compile(
    r'(</div>\s*)</p>',
    re.IGNORECASE
)

n_files = 0
n_open = 0
n_close = 0

for p in ROOT.rglob('*.html'):
    if is_skip(p):
        continue
    try:
        s = p.read_text(encoding='utf-8')
    except UnicodeDecodeError:
        continue
    orig = s

    s, ko = PATTERN.subn('', s)
    n_open += ko

    # Now remove </p> that follows </div> of a math-block.
    # Be conservative: only strip if the resulting structure looks clean.
    # We'll use a simpler pass: find sequences like:
    #   <div class="math-block">...</div>\n</p>
    # and remove the stray </p>.
    s, kc = re.subn(
        r'(<div class="math-block">[^<]*<[^>]+>.*?</div>\s*)</p>',
        r'\1',
        s, flags=re.DOTALL
    )
    n_close += kc

    if s != orig:
        p.write_text(s, encoding='utf-8')
        n_files += 1

print(f'Stripped open <p style=text-align:center>: {n_open}')
print(f'Stripped close </p> after math-block:      {n_close}')
print(f'Files touched: {n_files}')
