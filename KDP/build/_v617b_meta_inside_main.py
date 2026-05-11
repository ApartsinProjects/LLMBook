"""v6.17b: Move breadcrumb meta inside <main> so Pagefind picks it up.

Problem with v6.17a: `data-pagefind-meta="part"` was placed on `.part-label`
inside `<header class="chapter-header">`, which is in pagefind.yml's
`exclude_selectors`. Pagefind skips the whole subtree and ignores the
metadata.

Fix: inject two hidden <span> elements right after `<main class="content">`
opens, each carrying the breadcrumb as a literal value
(`data-pagefind-meta="part:Part 2: Understanding LLMs"`). These live inside
the indexed content tree, so Pagefind extracts them.

The literal values are pulled from each page's existing .part-label /
.chapter-label DOM (the anchor inside each).

Also: keep the v6.17a attributes on the visible labels (harmless, future-proof
if exclude_selectors changes).
"""
from __future__ import annotations
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent

PART_LABEL_RE = re.compile(
    r'<div class="part-label"[^>]*>\s*(?:<a[^>]*>)?([^<]+)(?:</a>)?\s*</div>'
)
CHAPTER_LABEL_RE = re.compile(
    r'<div class="chapter-label"[^>]*>\s*(?:<a[^>]*>)?([^<]+)(?:</a>)?\s*</div>'
)
MAIN_OPEN_RE = re.compile(r'(<main class="content"[^>]*>)')


def html_escape(s: str) -> str:
    return (
        s.replace('&', '&amp;')
         .replace('"', '&quot;')
         .replace('<', '&lt;')
         .replace('>', '&gt;')
    )


def process(p: Path) -> bool:
    text = p.read_text(encoding='utf-8')
    if 'pagefind-meta-injected' in text:
        return False  # idempotent guard
    part_m = PART_LABEL_RE.search(text)
    chap_m = CHAPTER_LABEL_RE.search(text)
    if not part_m and not chap_m:
        return False
    part_val = part_m.group(1).strip() if part_m else ''
    chap_val = chap_m.group(1).strip() if chap_m else ''
    if not (part_val or chap_val):
        return False

    spans = []
    if part_val:
        spans.append(
            f'<span class="pagefind-meta-injected" hidden '
            f'data-pagefind-meta="part:{html_escape(part_val)}"></span>'
        )
    if chap_val:
        spans.append(
            f'<span class="pagefind-meta-injected" hidden '
            f'data-pagefind-meta="chapter:{html_escape(chap_val)}"></span>'
        )
    injection = ''.join(spans)

    new_text, n = MAIN_OPEN_RE.subn(
        lambda m: m.group(1) + injection,
        text,
        count=1,
    )
    if n == 0:
        # Fallback: insert just before </header>
        new_text, n = re.subn(
            r'</header>',
            injection + '</header>',
            text,
            count=1,
        )
    if new_text == text:
        return False
    p.write_text(new_text, encoding='utf-8')
    return True


def main() -> int:
    files = sorted({
        *ROOT.glob('part-*/module-*/section-*.html'),
        *ROOT.glob('part-*/module-*/index.html'),
        *ROOT.glob('appendices/appendix-*/section-*.html'),
        *ROOT.glob('appendices/appendix-*/index.html'),
        *ROOT.glob('front-matter/**/*.html'),
    })
    fixed = 0
    for p in files:
        if not p.exists():
            continue
        if process(p):
            fixed += 1
    print(f'Injected breadcrumb meta into {fixed} files')
    print('NEXT: rebuild Pagefind index')
    return 0


if __name__ == '__main__':
    sys.exit(main())
