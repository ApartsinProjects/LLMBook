"""Wave 49: Convert h3.lab-title that sits OUTSIDE the callout lab div into
a <div class="callout-title"> INSIDE the callout.

Pattern observed:
    <h3 ... class="lab-title">Lab: Title</h3>     <-- title outside
    <div class="callout lab">                       <-- callout starts here
    <p>Body...</p>

Becomes:
    <div class="callout lab">
    <div class="callout-title">Lab: Title</div>     <-- title inside
    <p>Body...</p>

Also handles the parallel <h3 class="exercise-title"> outside <div class="callout exercise">.
"""
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')

ROOT = Path(__file__).resolve().parents[1]
SKIP = {'.git', 'node_modules', 'KDP', 'build', 'source_fix_backups',
        'pagefind', '.book-update', 'vendor', '.claude', '_archive',
        'agents', 'templates', 'docs', 'scripts'}

# Match: <h3 ... class="lab-title">Title</h3>\s*<div class="callout lab"[...]>
# OR same for exercise. Captures the title and the callout open tag.
PATTERN = re.compile(
    r'<h[34]\b[^>]*class="(lab-title|exercise-title)"[^>]*>([^<]+)</h[34]>\s*(<div\s+class="callout (?:lab|exercise)"[^>]*>)',
    re.IGNORECASE,
)


def fix_file(p: Path) -> int:
    text = p.read_text(encoding='utf-8')
    n = 0

    def repl(m: re.Match) -> str:
        nonlocal n
        n += 1
        title = m.group(2).strip()
        callout_open = m.group(3)
        return f'{callout_open}\n<div class="callout-title">{title}</div>'

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
    print(f'Lab/exercise titles moved inside callout: {n_total}')
    print(f'Files touched: {files_touched}')


if __name__ == '__main__':
    main()
