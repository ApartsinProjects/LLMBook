"""Wave 41: Inject canonical skip-to-main-content link into all section/index
pages, and add corresponding CSS to book.css.

The skip-link is a WCAG 2.4.1 (Bypass Blocks) accessibility requirement:
a keyboard/screen-reader user lands on an `<a href="#main-content">` as the
first focusable element and can skip over the long repeated header nav.

Steps:
1. Add `.skip-link` rule to styles/book.css (idempotent — skips if already present)
2. For each .html file in book content:
   a. Add `id="main-content"` to `<main class="content">` (if missing)
   b. Inject `<a href="#main-content" class="skip-link">Skip to main content</a>`
      immediately after the `<body>` open tag (if no skip-link already exists)

Excludes nav/build/vendor/script directories.
"""
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')

ROOT = Path(__file__).resolve().parents[1]
SKIP = {'.git', 'node_modules', 'KDP', 'build', 'source_fix_backups',
        'pagefind', '.book-update', 'vendor', '.claude', '_archive',
        'agents', 'templates', 'docs', 'scripts'}

SKIP_LINK_HTML = '<a class="skip-link" href="#main-content">Skip to main content</a>\n'

SKIP_LINK_CSS = """
/* ----- Accessibility: skip-to-main-content link (WCAG 2.4.1) ----- */
.skip-link {
    position: absolute;
    top: -40px;
    left: 0;
    background: #1a4078;
    color: #ffffff;
    padding: 8px 16px;
    z-index: 10000;
    text-decoration: none;
    border-radius: 0 0 4px 0;
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    font-size: 0.95rem;
}
.skip-link:focus {
    top: 0;
    outline: 2px solid #f6c945;
    outline-offset: 2px;
}
"""

BODY_OPEN = re.compile(r'(<body\b[^>]*>)', re.IGNORECASE)
MAIN_OPEN_NO_ID = re.compile(
    r'<main\s+class="content"(?![^>]*\bid=)([^>]*)>',
    re.IGNORECASE,
)
HAS_SKIP_LINK = re.compile(r'class="skip-link"|href="#main-content"', re.IGNORECASE)


def update_css():
    css_path = ROOT / 'styles' / 'book.css'
    text = css_path.read_text(encoding='utf-8')
    if '.skip-link' in text:
        return False  # already present
    # Append at the end with a separator comment
    text = text.rstrip() + '\n' + SKIP_LINK_CSS + '\n'
    css_path.write_text(text, encoding='utf-8')
    return True


def fix_file(p: Path) -> tuple[int, int]:
    """Returns (n_main_id_added, n_skip_link_added)."""
    text = p.read_text(encoding='utf-8')
    orig = text
    n_main = 0
    n_skip = 0

    # 1. Add id="main-content" to <main class="content">
    if 'class="content"' in text and 'id="main-content"' not in text:
        new = MAIN_OPEN_NO_ID.sub(
            r'<main class="content" id="main-content"\1>',
            text,
            count=1,  # Only first <main> per file
        )
        if new != text:
            text = new
            n_main = 1

    # 2. Inject skip-link after <body>
    if not HAS_SKIP_LINK.search(text):
        m = BODY_OPEN.search(text)
        if m:
            # Insert right after </body> open tag
            new = text[:m.end()] + '\n' + SKIP_LINK_HTML + text[m.end():]
            # Avoid double-newline (handle if body was followed by \n)
            new = new.replace(m.group() + '\n\n', m.group() + '\n', 1)
            if new != text:
                text = new
                n_skip = 1

    if text != orig:
        p.write_text(text, encoding='utf-8')
    return n_main, n_skip


def main():
    css_added = update_css()
    print(f'CSS rule added to book.css: {css_added}')

    n_files = 0
    n_main_total = 0
    n_skip_total = 0
    for p in sorted(ROOT.rglob('*.html')):
        if set(p.parts) & SKIP:
            continue
        n_main, n_skip = fix_file(p)
        if n_main or n_skip:
            n_files += 1
            n_main_total += n_main
            n_skip_total += n_skip
    print(f'main id="main-content" added: {n_main_total} files')
    print(f'skip-link injected: {n_skip_total} files')
    print(f'Total files touched: {n_files}')


if __name__ == '__main__':
    main()
