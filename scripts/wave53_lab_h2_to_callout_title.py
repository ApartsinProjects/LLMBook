"""Wave 53: Convert <h2>/<h3>/<h4> that's the FIRST child inside a lab/exercise
callout to <div class="callout-title">.

Pattern observed in residual lab callouts:
    <div class="callout lab" id="lab-X">
    <h2 id="hands-on-lab-...">Hands-On Lab: Title</h2>
    <div class="lab-meta">...

Becomes:
    <div class="callout lab" id="lab-X">
    <div class="callout-title">Hands-On Lab: Title</div>
    <div class="lab-meta">...
"""
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')

ROOT = Path(__file__).resolve().parents[1]
SKIP = {'.git', 'node_modules', 'KDP', 'build', 'source_fix_backups',
        'pagefind', '.book-update', 'vendor', '.claude', '_archive',
        'agents', 'templates', 'docs', 'scripts'}

# Match: <div class="callout (lab|exercise)" ...>\s*<hN ...>Title</hN>
PATTERN = re.compile(
    r'(<div\s+class="callout (?:lab|exercise)"[^>]*>\s*)<h[234]\b[^>]*>([^<]+)</h[234]>',
    re.IGNORECASE,
)


def fix_file(p: Path) -> int:
    text = p.read_text(encoding='utf-8')
    n = 0

    def repl(m: re.Match) -> str:
        nonlocal n
        n += 1
        prefix = m.group(1)
        title = m.group(2).strip()
        return f'{prefix}<div class="callout-title">{title}</div>'

    new_text = PATTERN.sub(repl, text)
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
    print(f'Lab/exercise hN -> callout-title (inside callout): {n_total}')
    print(f'Files touched: {files_touched}')


if __name__ == '__main__':
    main()
