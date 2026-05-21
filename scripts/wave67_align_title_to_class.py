"""Wave 67: Align callout title to its (already-correct) class.

After wave 66 reclassified key-insight → key-takeaway when the body contained
a list, the title text often still says "Key Insight". Update the title to
"Key Takeaways" to match the new class.

Generalizes the same way as wave 59 but in the reverse direction.
"""
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')

ROOT = Path(__file__).resolve().parents[1]
SKIP = {'.git', 'node_modules', 'KDP', 'build', 'source_fix_backups',
        'pagefind', '.book-update', 'vendor', '.claude', '_archive',
        'agents', 'templates', 'docs', 'scripts'}

# Match: <div class="callout key-takeaway">\s*<div class="callout-title">Key Insight: ...</div>
KEY_TAKE_BAD_TITLE_RE = re.compile(
    r'(<div\s+class="callout key-takeaway"[^>]*>\s*<div\s+class="callout-title"[^>]*>)'
    r'\s*Key\s*Insight[s]?\s*(:?)\s*',
    re.IGNORECASE,
)


def fix_file(p: Path) -> int:
    text = p.read_text(encoding='utf-8')
    n = 0

    def repl(m: re.Match) -> str:
        nonlocal n
        n += 1
        colon = m.group(2)
        # If the original had a colon (Key Insight: Title), preserve it
        if colon:
            return m.group(1) + 'Key Takeaways: '
        return m.group(1) + 'Key Takeaways'

    new_text = KEY_TAKE_BAD_TITLE_RE.sub(repl, text)
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
    print(f'Title fixed: Key Insight → Key Takeaways: {n_total}')
    print(f'Files touched: {files_touched}')


if __name__ == '__main__':
    main()
