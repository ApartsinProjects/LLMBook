"""v6.17: Add part/chapter breadcrumb to Pagefind search results.

USER REQUEST
"any way for search to show also part/chapter/module of found pages"

DESIGN
Pagefind UI renders result titles via innerHTML (so it can show <mark>
match highlights). We exploit that:

  1. Tag the existing breadcrumb DOM elements with `data-pagefind-meta`
     so Pagefind extracts them as per-page metadata:
        <div class="part-label" data-pagefind-meta="part">Part 2: ...</div>
        <div class="chapter-label" data-pagefind-meta="chapter">Chapter 06: ...</div>
     The text content of each becomes result.meta.part / result.meta.chapter.

  2. Update every PagefindUI initialization to add a processResult callback
     that prepends a styled breadcrumb to result.meta.title:
        <span class="pf-crumb">Part 2 › Chapter 06</span> Real Title
     Pagefind UI keeps the <span> intact (same path that supports <mark>).

  3. CSS rule in styles/book.css renders .pf-crumb in muted small text
     above the link target.

  4. Run `pagefind` to rebuild the index — must be a separate manual step.

Idempotent: skipped if the file is already updated.
"""
from __future__ import annotations
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent


# ---- (1) Add data-pagefind-meta to .part-label and .chapter-label divs ----

PART_LABEL_BEFORE = re.compile(
    r'<div class="part-label"(?![^>]*data-pagefind-meta)([^>]*)>'
)
CHAPTER_LABEL_BEFORE = re.compile(
    r'<div class="chapter-label"(?![^>]*data-pagefind-meta)([^>]*)>'
)


def tag_breadcrumb_meta(text: str) -> tuple[str, int]:
    n = 0
    new = PART_LABEL_BEFORE.sub(
        lambda m: f'<div class="part-label" data-pagefind-meta="part"{m.group(1)}>',
        text,
    )
    n += new != text
    text = new
    new = CHAPTER_LABEL_BEFORE.sub(
        lambda m: f'<div class="chapter-label" data-pagefind-meta="chapter"{m.group(1)}>',
        text,
    )
    n += new != text
    return new, n


# ---- (2) Update PagefindUI init to add processResult callback ----

NEW_INIT_BLOCK = '''new PagefindUI({
      element: "#search",
      showSubResults: true,
      showImages: false,
      resetStyles: false,
      pageSize: 8,
      autofocus: false,
      translations: {
        placeholder: "Search the book\\u2026",
      },
      processResult: function (result) {
        try {
          var part = (result && result.meta && result.meta.part) ? result.meta.part : "";
          var chap = (result && result.meta && result.meta.chapter) ? result.meta.chapter : "";
          // Strip "Part 2: Understanding LLMs" -> "Part 2" and "Chapter 06: ..." -> "Chapter 06"
          var partShort = part.split(":")[0].trim();
          var chapShort = chap.split(":")[0].trim();
          var crumb = [partShort, chapShort].filter(Boolean).join(" \\u203a ");
          if (crumb && result.meta && result.meta.title
              && result.meta.title.indexOf("pf-crumb") === -1) {
            result.meta.title = "<span class=\\"pf-crumb\\">" + crumb + "</span> "
                              + result.meta.title;
          }
        } catch (e) { /* fall through */ }
        return result;
      },
    });'''

OLD_INIT_RE = re.compile(
    r'new PagefindUI\(\{\s*'
    r'element:\s*"#search",\s*'
    r'showSubResults:\s*true,\s*'
    r'showImages:\s*false,\s*'
    r'resetStyles:\s*false,\s*'
    r'pageSize:\s*8,\s*'
    r'autofocus:\s*false,\s*'
    r'translations:\s*\{\s*'
    r'placeholder:\s*"Search the book[^"]*",?\s*'
    r'\},?\s*'
    r'\}\);',
    re.DOTALL,
)


def update_pagefind_init(text: str) -> tuple[str, int]:
    # Skip if already updated
    if 'processResult' in text and 'pf-crumb' in text:
        return text, 0
    new, n = OLD_INIT_RE.subn(lambda m: NEW_INIT_BLOCK, text, count=1)
    return new, n


# ---- main ----

def process_file(p: Path) -> tuple[bool, bool]:
    """Return (meta_changed, init_changed)."""
    text = p.read_text(encoding='utf-8')
    original = text
    text, meta_n = tag_breadcrumb_meta(text)
    text, init_n = update_pagefind_init(text)
    if text != original:
        p.write_text(text, encoding='utf-8')
    return meta_n > 0, init_n > 0


def main() -> int:
    files = sorted({
        *ROOT.glob('part-*/module-*/section-*.html'),
        *ROOT.glob('part-*/module-*/index.html'),
        *ROOT.glob('appendices/appendix-*/section-*.html'),
        *ROOT.glob('appendices/appendix-*/index.html'),
        *ROOT.glob('front-matter/**/*.html'),
        ROOT / 'toc.html',
        ROOT / 'index.html',
    })
    meta_total = init_total = 0
    for p in files:
        if not p.exists():
            continue
        meta_changed, init_changed = process_file(p)
        meta_total += int(meta_changed)
        init_total += int(init_changed)
    print(f'data-pagefind-meta attrs added: {meta_total} files')
    print(f'PagefindUI inits upgraded:     {init_total} files')
    print()
    print('NEXT: rebuild Pagefind index')
    print('   npx pagefind --site . --output-path pagefind')
    return 0


if __name__ == '__main__':
    sys.exit(main())
