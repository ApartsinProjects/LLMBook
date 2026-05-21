"""Wave 34h: Move callouts that appear AFTER bibliography to BEFORE bibliography.

Canonical order: ... callouts -> whats-next -> bibliography -> chapter-nav.

Bug pattern (49 instances in 11+ files): callouts placed AFTER the closing
`</details>` of the bibliography, between bibliography and chapter-nav.

Bad:
    <details class="bibliography-collapsible">...</details>
    <div class="callout tip">...</div>
    <div class="callout key-insight">...</div>
    <nav class="chapter-nav">...</nav>

Good:
    <div class="callout tip">...</div>
    <div class="callout key-insight">...</div>
    <details class="bibliography-collapsible">...</details>
    <nav class="chapter-nav">...</nav>
"""
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')

ROOT = Path(__file__).resolve().parents[1]
SKIP = {'.git', 'node_modules', 'KDP', 'build', 'source_fix_backups', 'pagefind',
        '.book-update', 'vendor', '.claude', '_archive', 'agents', 'templates',
        'docs', 'scripts'}

PATTERN = re.compile(
    r'(<details\s+class="bibliography-collapsible"[^>]*>[\s\S]*?</details>\s*)'
    r'((?:<div\s+class="callout\s+[^"]+"[^>]*>[\s\S]*?</div>\s*)+)'
    r'(?=<nav\s+class="chapter-nav"|<footer|</main>)',
    re.IGNORECASE,
)


def fix(text: str) -> tuple[str, int]:
    def repl(m: re.Match) -> str:
        bib_block = m.group(1)
        callouts = m.group(2)
        return callouts + bib_block
    return PATTERN.subn(repl, text)


def main():
    n_files = 0
    n_callouts_moved = 0
    for p in sorted(ROOT.rglob('section-*.html')):
        if set(p.parts) & SKIP:
            continue
        text = p.read_text(encoding='utf-8')
        if 'bibliography-collapsible' not in text:
            continue
        new, n = fix(text)
        if n > 0 and new != text:
            # Count callouts moved
            n_callouts_in_block = len(re.findall(r'<div\s+class="callout\s+', text)) - len(re.findall(r'<div\s+class="callout\s+', new[:new.find('</details>') + len('</details>')]))
            p.write_text(new, encoding='utf-8')
            n_files += 1
            n_callouts_moved += n
            print(f'  {p.relative_to(ROOT)}: callouts moved before bib')
    print(f'\nMoved callouts before bibliography in {n_files} files ({n_callouts_moved} block sweeps)')


if __name__ == '__main__':
    main()
