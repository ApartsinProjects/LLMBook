"""Wave 33c: Fix corrupted pagefind-meta-injected spans book-wide.

Random-detector + anomalous-styling audits found 29 pages where the chapter
metadata span lost its attribute-name and chapter-number prefix:

  bad:  <span class="pagefind-meta-injected" b: LLM Evaluation &amp; Quality Metrics" hidden=""></span>
  good: <span class="pagefind-meta-injected" data-pagefind-meta="chapter:Chapter 42: LLM Evaluation &amp; Quality Metrics" hidden=""></span>

The single-letter prefix (b:/c:/d:/f:) is corruption noise; we recover the real
chapter number from the file path: `module-NN-slug` -> Chapter NN.
"""
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')

ROOT = Path(__file__).resolve().parents[1]
MODULE_NUM_RE = re.compile(r'module-(\d+)-')
BAD_SPAN_RE = re.compile(
    r'<span\s+class="pagefind-meta-injected"\s+[a-z]:\s+([^"]+)"\s+hidden=""></span>'
)


def fix(text: str, chapter_num: str) -> tuple[str, int]:
    def repl(m: re.Match) -> str:
        chapter_title = m.group(1)
        return (
            f'<span class="pagefind-meta-injected" '
            f'data-pagefind-meta="chapter:Chapter {chapter_num}: {chapter_title}" '
            f'hidden=""></span>'
        )
    return BAD_SPAN_RE.subn(repl, text)


def main():
    n_files = 0
    n_total = 0
    for p in sorted(ROOT.rglob('*.html')):
        # Skip backups / docs / agents / archives
        if any(s in p.parts for s in {
            '.git', 'node_modules', 'KDP', 'build', 'source_fix_backups',
            'pagefind', '.book-update', 'vendor', '.claude', '_archive',
            'agents', 'templates', 'docs', 'scripts',
        }):
            continue
        # Determine chapter number from path
        m = None
        for part in p.parts:
            m = MODULE_NUM_RE.match(part)
            if m:
                break
        if not m:
            continue
        chapter_num = str(int(m.group(1)))  # drop leading zero (module-01 -> 1)
        text = p.read_text(encoding='utf-8')
        if 'pagefind-meta-injected' not in text:
            continue
        new, n = fix(text, chapter_num)
        if n > 0:
            p.write_text(new, encoding='utf-8')
            n_files += 1
            n_total += n
            print(f'  Ch {chapter_num}  {p.relative_to(ROOT)}: {n} fix(es)')
    print(f'\nFixed {n_total} corrupted pagefind-meta spans in {n_files} files')


if __name__ == '__main__':
    main()
