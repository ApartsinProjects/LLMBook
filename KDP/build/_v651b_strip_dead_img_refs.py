"""v6.51b: Strip <figure>/<img> blocks pointing to deleted images.

For each <img src=> where the file doesn't exist, remove the wrapping
<figure>...</figure> block (or the bare <img> + adjacent caption div) so
the page doesn't render a broken-image icon + dangling caption.
"""
from __future__ import annotations
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
SKIP = ('node_modules', '.git/', 'pagefind/', 'KDP/build/', 'KDP/output/',
        'templates/', '_archive/')


def main() -> int:
    total_removed = 0
    files_changed = 0
    for p in ROOT.rglob('*.html'):
        sp = str(p).replace('\\', '/')
        if any(s in sp for s in SKIP):
            continue
        try:
            text = p.read_text(encoding='utf-8', errors='replace')
        except Exception:
            continue
        original = text
        # Find all <img src> in this file
        broken_srcs = []
        for m in re.finditer(r'<img[^>]+src="([^"]+)"', text):
            src = m.group(1)
            if src.startswith('http'):
                continue
            target = (p.parent / src).resolve()
            if not target.exists():
                broken_srcs.append(src)
        if not broken_srcs:
            continue
        # For each broken src, strip its containing block
        for src in broken_srcs:
            # Try: <figure>...<img src="<src>"...></figure>
            fig_re = re.compile(
                rf'\n?\s*<figure[^>]*>\s*(?:.|\n)*?<img[^>]+src="{re.escape(src)}"[^>]*/?>(?:.|\n)*?</figure>\s*',
                re.MULTILINE,
            )
            new_text = fig_re.sub('\n', text)
            if new_text == text:
                # Try: <img> + adjacent <div class="diagram-caption">
                bare_re = re.compile(
                    rf'\n?\s*<img[^>]+src="{re.escape(src)}"[^>]*/?>'
                    rf'\s*<div class="diagram-caption">(?:.|\n)*?</div>\s*',
                    re.MULTILINE,
                )
                new_text = bare_re.sub('\n', text)
            if new_text == text:
                # Strip the bare <img>
                bare_img = re.compile(
                    rf'\n?\s*<img[^>]+src="{re.escape(src)}"[^>]*/?>\s*'
                )
                new_text = bare_img.sub('\n', text)
            if new_text != text:
                text = new_text
                total_removed += 1
        if text != original:
            p.write_text(text, encoding='utf-8')
            files_changed += 1
            print(f'  cleaned: {p.relative_to(ROOT)}')

    print(f'\nRemoved {total_removed} broken <img> blocks across {files_changed} files.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
