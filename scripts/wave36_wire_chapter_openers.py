"""Wave 36b: Wire chapter-opener.png into chapter-index pages.

Inserts `<figure class="illustration chapter-opener">` markup right after
`<main class="content">` (or after the first <span pagefind-meta-injected>
if present, to keep the hero visually first).

Skips pages that already contain `illustration chapter-opener`.
Skips pages where images/chapter-opener.png does not exist.
"""
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')

ROOT = Path(__file__).resolve().parents[1]

# Insert immediately after the opening <main class="content"> tag
INSERT_AFTER_MAIN = re.compile(
    r'(<main\s+class="content"[^>]*>\s*)',
    re.IGNORECASE,
)


def make_figure(chapter_title: str) -> str:
    alt = f'Warm cartoon-style hero illustration introducing chapter "{chapter_title}", in the Kurzgesagt-meets-XKCD style with friendly characters and clear iconography'
    return (
        f'<figure class="illustration chapter-opener">'
        f'<img alt="{alt}" src="images/chapter-opener.png"/>'
        f'</figure>\n'
    )


def extract_title(html: str) -> str:
    m = re.search(r'<h1[^>]*>([^<]+)</h1>', html)
    if m:
        return m.group(1).strip()
    return "this chapter"


def main():
    n_wired = 0
    n_skipped = 0
    n_no_image = 0
    for p in sorted(ROOT.glob('part-*/module-*/index.html')):
        text = p.read_text(encoding='utf-8')
        if 'illustration chapter-opener' in text:
            n_skipped += 1
            continue
        img_path = p.parent / 'images' / 'chapter-opener.png'
        if not img_path.exists():
            n_no_image += 1
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
    print(f'\nWired {n_wired} chapter-opener images')
    if n_skipped:
        print(f'Skipped {n_skipped} pages already containing chapter-opener markup')
    if n_no_image:
        print(f'Skipped {n_no_image} pages without chapter-opener.png file')


if __name__ == '__main__':
    main()
