"""v757: Move agent-avatar <img> out of <cite> for KPV/Kindle compatibility.

Root cause: Kindle Previewer (KPV) emits E21018 "Enhanced Mobi building
failure, while parsing content. Content: <img>" when it encounters an
<img> nested inside an inline <cite> element. This is a long-standing
quirk of Amazon's Mobi/KFX converter: <cite> is treated as strict inline
phrasing and embedded replaced elements (img) inside it confuse the
converter even though the markup is valid XHTML and passes EPUBCheck.

The pattern across this book is (from epigraphs):
    <cite>
      <span class="agent-avatar-inline" style="background-color: #XXX;">
        <img alt="..." src="..." width="28" height="28"/>
      </span> Name, <span class="agent-desc">role</span>
    </cite>

This script transforms it to:
    <span class="agent-avatar-inline" style="background-color: #XXX;">
      <img alt="..." src="..." width="28" height="28"/>
    </span>
    <cite>Name, <span class="agent-desc">role</span></cite>

The avatar lives BEFORE the <cite> instead of inside it. Visually the
result is identical (the avatar still appears immediately to the left
of the name) and KPV can now parse the chapter.

Idempotent: skips files where the avatar has already been hoisted.
"""
from __future__ import annotations
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent

# Match an entire <cite>...avatar...</cite> block.
# Group 1: avatar span (entire span including img)
# Group 2: leading whitespace/space inside cite, after the span
# Group 3: rest of cite contents (name, desc, etc.)
PAT = re.compile(
    r'<cite>\s*'
    r'(<span\s+class="agent-avatar-inline"[^>]*>\s*<img\b[^>]*/?>\s*</span>)'
    r'(\s*)'
    r'(.*?)'
    r'</cite>',
    re.DOTALL | re.IGNORECASE,
)


def transform(html: str) -> tuple[str, int]:
    n = 0

    def repl(m: re.Match) -> str:
        nonlocal n
        n += 1
        avatar = m.group(1)
        rest = m.group(3).strip()
        return f'{avatar}<cite>{rest}</cite>'

    new = PAT.sub(repl, html)
    return new, n


SKIP_DIRS = {'.git', 'node_modules', 'KDP/build/source_fix_backups',
             'pagefind', 'venv', '.venv'}


def should_skip(p: Path) -> bool:
    s = str(p).replace('\\', '/')
    for sd in SKIP_DIRS:
        if f'/{sd}/' in s or s.endswith(f'/{sd}'):
            return True
    if 'KDP/build/source_fix_backups' in s:
        return True
    return False


def main() -> int:
    files = []
    for p in ROOT.rglob('*.html'):
        if should_skip(p):
            continue
        files.append(p)
    print(f'Scanning {len(files)} HTML files')

    total_fixes = 0
    files_changed = 0
    for p in files:
        try:
            src = p.read_text(encoding='utf-8')
        except UnicodeDecodeError:
            continue
        if 'agent-avatar-inline' not in src:
            continue
        new, n = transform(src)
        if n > 0 and new != src:
            p.write_text(new, encoding='utf-8')
            total_fixes += n
            files_changed += 1
            rel = p.relative_to(ROOT)
            print(f'  [fix x{n}] {rel}')

    print('-' * 60)
    print(f'Files changed: {files_changed}')
    print(f'Total <cite>-wrapped <img> fixes: {total_fixes}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
