"""Wave 55b: Promote numbered <h3>X.Y.Z Title</h3> to <h2> in files where:
  - The file has at least one numbered h3 (id="X-Y-Z-...")
  - The file has NO numbered h2 (id="X-Y-Z-...") — only navigation h2s like
    Exercises, What Comes Next, Prerequisites

This catches cases like section-47.1 (1157 lines, 2 h2 because Exercises + What
Comes Next are the only h2s; the actual subsections use h3).
"""
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')

ROOT = Path(__file__).resolve().parents[1]
SKIP = {'.git', 'node_modules', 'KDP', 'build', 'source_fix_backups',
        'pagefind', '.book-update', 'vendor', '.claude', '_archive',
        'agents', 'templates', 'docs', 'scripts'}

NUMBERED_H2_ID_RE = re.compile(r'<h2\b[^>]*\bid="\d+-\d+-\d+', re.IGNORECASE)
# Match numbered h3: id like "47-1-1" or "47-1-1-rag-poisoning-attacks".
# DO NOT match deeper numbering like "47-1-4-1" (those are h3 sub-subsections
# and should stay h3 even when peers get promoted).
H3_NUMBERED_RE = re.compile(
    r'<h3(\s+id="\d+-\d+-\d+(?:-[a-z][^"]*)?")[^>]*>(\d+\.\d+\.\d+\s+[^<]+)</h3>',
    re.IGNORECASE,
)


def fix_file(p: Path) -> int:
    text = p.read_text(encoding='utf-8')
    main_open = re.search(r'<main\b[^>]*>', text, re.IGNORECASE)
    main_close = re.search(r'</main>', text, re.IGNORECASE)
    if not main_open or not main_close:
        return 0
    main_text = text[main_open.end():main_close.start()]
    # Check if there are numbered h2s already
    if NUMBERED_H2_ID_RE.search(main_text):
        return 0
    # Promote numbered h3 to h2
    n = 0

    def repl(m: re.Match) -> str:
        nonlocal n
        n += 1
        attrs = m.group(1)
        content = m.group(2)
        return f'<h2{attrs}>{content}</h2>'

    new_main = H3_NUMBERED_RE.sub(repl, main_text)
    if n == 0:
        return 0
    new_text = text[:main_open.end()] + new_main + text[main_close.start():]
    p.write_text(new_text, encoding='utf-8')
    return n


def main():
    n_total = 0
    files_touched = 0
    for p in sorted(ROOT.rglob('*.html')):
        if set(p.parts) & SKIP:
            continue
        if not p.name.startswith('section-'):
            continue
        n = fix_file(p)
        if n > 0:
            n_total += n
            files_touched += 1
            print(f'  {p.relative_to(ROOT)}: {n} h3 -> h2')
    print(f'\nTotal: {n_total} promotions across {files_touched} files')


if __name__ == '__main__':
    main()
