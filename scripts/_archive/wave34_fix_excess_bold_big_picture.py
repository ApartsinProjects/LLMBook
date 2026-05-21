"""Wave 34b: Strip outer `<strong>` wrapping entire Big Picture paragraph.

Targets the section-23.1 / section-11.4 pattern where the WHOLE Big Picture
paragraph is wrapped in <strong>, making it visually heavy. The fix:
unwrap the outer <strong> only when it wraps the entire paragraph content.

Inner <strong> spans for key terms are preserved.
"""
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')

ROOT = Path(__file__).resolve().parents[1]
SKIP = {'.git', 'node_modules', 'KDP', 'build', 'source_fix_backups', 'pagefind',
        '.book-update', 'vendor', '.claude', '_archive', 'agents', 'templates',
        'docs', 'scripts'}

BIG_PICTURE_RE = re.compile(
    r'(<div\s+class="callout\s+big-picture"[^>]*>[\s\S]*?<div\s+class="callout-title"[^>]*>[^<]*</div>\s*)'
    r'<p>\s*<strong>([\s\S]*?)</strong>\s*</p>',
    re.IGNORECASE,
)


def fix(text: str) -> tuple[str, int]:
    """Unwrap outer <strong> from Big Picture full-paragraph wrapping."""
    def repl(m: re.Match) -> str:
        prefix = m.group(1)
        inner = m.group(2)
        # Only apply when inner doesn't contain a closing </p> already
        # (which would mean the strong was multi-paragraph - rare/broken)
        if '</p>' in inner:
            return m.group(0)
        return f'{prefix}<p>{inner}</p>'
    return BIG_PICTURE_RE.subn(repl, text)


def main():
    n_files = 0
    n_total = 0
    for p in sorted(ROOT.rglob('section-*.html')):
        if set(p.parts) & SKIP:
            continue
        text = p.read_text(encoding='utf-8')
        new, n = fix(text)
        if n > 0:
            p.write_text(new, encoding='utf-8')
            n_files += 1
            n_total += n
            print(f'  {p.relative_to(ROOT)}: {n} block(s) unwrapped')
    print(f'\nUnwrapped {n_total} outer <strong> in Big Picture, {n_files} files')


if __name__ == '__main__':
    main()
