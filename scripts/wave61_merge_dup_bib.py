"""Wave 61: Merge back-to-back duplicate bibliography <details> blocks.

Pattern: two consecutive
    <details class="bibliography-collapsible" open>
    <summary><strong>Further Reading</strong></summary>
    <section class="bibliography">
      ...entries A...
    </section>
    </details>
    <details class="bibliography-collapsible" open>
    <summary><strong>Further Reading</strong></summary>
    <section class="bibliography">
      ...entries B...
    </section>
    </details>

Fix: merge entries B into the FIRST <section class="bibliography">, drop the
second <details> wrapper. Preserves all entries.
"""
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')

ROOT = Path(__file__).resolve().parents[1]
SKIP = {'.git', 'node_modules', 'KDP', 'build', 'source_fix_backups',
        'pagefind', '.book-update', 'vendor', '.claude', '_archive',
        'agents', 'templates', 'docs', 'scripts'}

# Match: </section>\s*</details>\s*<details class="bibliography-collapsible"...>
#        \s*<summary...>...</summary>\s*<section class="bibliography"...>
MERGE_RE = re.compile(
    r'(</section>)\s*</details>\s*'
    r'<details\s+class="bibliography-collapsible[^"]*"[^>]*>\s*'
    r'<summary[^>]*>.*?</summary>\s*'
    r'<section\s+class="bibliography"[^>]*>\s*',
    re.DOTALL | re.IGNORECASE,
)


def fix_file(p: Path) -> int:
    text = p.read_text(encoding='utf-8')
    n = 0

    def repl(m: re.Match) -> str:
        nonlocal n
        n += 1
        # Replace "</section></details><details><summary></summary><section>" with empty
        # (so the inner entries flow into the existing <section>).
        return ''

    new_text = MERGE_RE.sub(repl, text)
    if new_text != text:
        p.write_text(new_text, encoding='utf-8')
    return n


def main():
    n_total = 0
    files_touched = 0
    for p in sorted(ROOT.rglob('*.html')):
        if set(p.parts) & SKIP:
            continue
        n = fix_file(p)
        if n > 0:
            n_total += n
            files_touched += 1
            print(f'  {p.relative_to(ROOT)}: merged {n} duplicate bib block(s)')
    print(f'\nTotal merges: {n_total}')
    print(f'Files touched: {files_touched}')


if __name__ == '__main__':
    main()
