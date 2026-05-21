"""Wave 36c: Wire part-opener.png into part-index pages.

Same pattern as wave36_wire_chapter_openers.py, but for part landings:
inserts `<figure class="illustration part-opener">` right after `<main class="content">`.
"""
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')

ROOT = Path(__file__).resolve().parents[1]

INSERT_AFTER_MAIN = re.compile(
    r'(<main\s+class="content"[^>]*>\s*)',
    re.IGNORECASE,
)


def make_figure(part_title: str) -> str:
    alt = f'Warm cartoon-style hero illustration introducing part "{part_title}", in the Kurzgesagt-meets-XKCD style with friendly characters and clear iconography'
    return (
        f'<figure class="illustration part-opener">'
        f'<img alt="{alt}" src="images/part-opener.png"/>'
        f'</figure>\n'
    )


def extract_title(html: str) -> str:
    m = re.search(r'<h1[^>]*>([^<]+)</h1>', html)
    if m:
        return m.group(1).strip()
    return "this part"


def main():
    n_wired = 0
    for p in sorted(ROOT.glob('part-*/index.html')):
        if not p.parent.name.startswith('part-'):
            continue
        text = p.read_text(encoding='utf-8')
        if 'part-opener' in text or 'illustration chapter-opener' in text:
            continue
        img_path = p.parent / 'images' / 'part-opener.png'
        if not img_path.exists():
            continue
        title = extract_title(text)
        figure = make_figure(title)
        new, n = INSERT_AFTER_MAIN.subn(
            lambda m: m.group(1) + figure,
            text,
            count=1,
        )
        if n > 0 and new != text:
            p.write_text(new, encoding='utf-8')
            n_wired += 1
            print(f'  {p.relative_to(ROOT)}: wired')
    print(f'\nWired {n_wired} part-opener images')


if __name__ == '__main__':
    main()
