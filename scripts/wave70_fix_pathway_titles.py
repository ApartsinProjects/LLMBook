"""Wave 70: Fix the 41 callout note titles that wave 69 missed.

Pattern: <div class="callout note"><div class="callout-title">Learning Objectives</div>
These came from `callout pathway` blocks that didn't have the "Learning
Objectives:" colon-form prefix. The body is usually a <ul> listing chapter
learning objectives. Fix: prepend "Note: " to the title to satisfy the
CALLOUT_TITLE_PREFIX rule for `note` callouts.
"""
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')

ROOT = Path(__file__).resolve().parents[1]
SKIP = {'.git', 'node_modules', 'KDP', 'build', 'source_fix_backups',
        'pagefind', '.book-update', 'vendor', '.claude', '_archive',
        'agents', 'templates', 'docs', 'scripts'}

# Match: <div class="callout note"><div class="callout-title">Learning Objectives</div>
# or "Note: What Comes Next" inside whats-next class
TITLE_FIX_RE = re.compile(
    r'(<div\s+class="callout note"[^>]*>\s*<div\s+class="callout-title"[^>]*>)'
    r'\s*(?:Note:\s*)?Learning Objectives?\s*'
    r'(</div>)',
    re.IGNORECASE,
)
# Also the wave 69 over-prefixed Note onto a whats-next callout
WN_DOUBLE_RE = re.compile(
    r'(<div\s+class="callout whats-next"[^>]*>\s*<div\s+class="callout-title"[^>]*>)'
    r'\s*Note:\s*What\s+Comes\s+Next\s*'
    r'(</div>)',
    re.IGNORECASE,
)


def fix_file(p: Path) -> int:
    text = p.read_text(encoding='utf-8')
    n = 0

    def fix_lo(m):
        nonlocal n
        n += 1
        return m.group(1) + 'Note: Learning Objectives' + m.group(2)
    text2 = TITLE_FIX_RE.sub(fix_lo, text)

    def fix_wn(m):
        nonlocal n
        n += 1
        return m.group(1) + "What's Next" + m.group(2)
    text2 = WN_DOUBLE_RE.sub(fix_wn, text2)

    if text2 != text:
        p.write_text(text2, encoding='utf-8')
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
    print(f'Title fixes: {n_total} across {files_touched} files')


if __name__ == '__main__':
    main()
