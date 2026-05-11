"""v6.10: Inject Pagefind search UI into every section HTML file.

Pagefind ships a self-contained UI bundle. We add:
  1. <link> to pagefind-ui.css in <head>
  2. <script> to load pagefind-ui.js (deferred)
  3. <div id="search"> placeholder in the header-nav (right of Contents link)
  4. <script> to instantiate PagefindUI() once DOMContentLoaded

Pagefind is at /pagefind/ at the site root, so we compute the relative path
based on the file's depth.
"""
from __future__ import annotations
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
SKIP_PARTS = {'agents', 'KDP', 'node_modules', 'scripts', '.git',
              'chapter_review', 'downloads', '_archive',
              '_lab_fragments', 'templates'}


def rel_prefix(p: Path) -> str:
    """How many '../' to prepend to reach the site root."""
    depth = len(p.relative_to(ROOT).parts) - 1
    return '../' * depth if depth > 0 else './'


def inject(p: Path) -> bool:
    text = p.read_text(encoding='utf-8', errors='replace')
    if 'pagefind-ui' in text:
        return False  # idempotent

    prefix = rel_prefix(p)
    # Asset paths (vendored under /pagefind/)
    css_href = f'{prefix}pagefind/pagefind-ui.css'
    js_src   = f'{prefix}pagefind/pagefind-ui.js'

    # 1) Add <link rel="stylesheet" ...> + <script defer ...> to <head>
    head_inject = (
        f'<link rel="stylesheet" href="{css_href}">\n'
        f'<script defer src="{js_src}"></script>\n'
    )
    if '</head>' not in text:
        return False
    text = text.replace('</head>', head_inject + '</head>', 1)

    # 2) Add <div id="search"> ... </div> after the </nav> in the header-nav
    # The pattern is:
    #   <nav class="header-nav">
    #     <a class="book-title-link" href="...">Building...</a>
    #     <a class="toc-link" href="...">Contents</a>
    #   </nav>
    # We insert a <div class="header-search"> right after the </nav> closes.
    SEARCH_DIV = (
        '<div class="header-search">\n'
        '<div id="search"></div>\n'
        '</div>\n'
    )
    nav_pat = re.compile(r'(<nav class="header-nav">(?:.|\n)*?</nav>)')
    if nav_pat.search(text):
        text = nav_pat.sub(lambda m: m.group(1) + '\n' + SEARCH_DIV, text, count=1)
    else:
        # Fallback: inject after opening <body>
        text = text.replace('<body>', '<body>\n' + SEARCH_DIV, 1)

    # 3) Add init script just before </body>
    init = '''<script>
window.addEventListener("DOMContentLoaded", function() {
  if (window.PagefindUI) {
    new PagefindUI({
      element: "#search",
      showSubResults: true,
      showImages: false,
      resetStyles: false,
      pageSize: 8,
      autofocus: false,
      translations: {
        placeholder: "Search the book…",
      },
    });
  }
});
</script>
'''
    if '</body>' in text:
        text = text.replace('</body>', init + '</body>', 1)

    p.write_text(text, encoding='utf-8')
    return True


def main() -> int:
    n = 0
    for p in sorted(ROOT.rglob('*.html')):
        rel = p.relative_to(ROOT)
        if rel.parts and rel.parts[0] in SKIP_PARTS:
            continue
        if inject(p):
            n += 1
    print(f'Injected Pagefind UI into {n} HTML files.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
