"""Post-build EPUB patch: strip web-only navigation chrome from every chapter.

DEEP-HUNT finding (2026-05-29): all 605 of 607 content pages start with
IDENTICAL web-only scaffolding (skip-link, chapter-header with nav-bar
+ search box + part-label, then H1; and at end nav.chapter-nav pager +
footer). This is the same pattern KDP's classifier likely uses to
identify fixed-layout / paginated content: 605 pages with identical
chrome at top and bottom.

The chrome is:
  - Visually hidden on Kindle by CSS (header-nav has position:fixed,
    chapter-nav has display:grid, header-search has CSS that doesn't
    render). But the DOM is STILL THERE for the classifier to scan.

What this patch does (carefully preserves content):
  1. Strip <a class="skip-link">...</a> (web accessibility shortcut)
  2. Replace <header class="chapter-header">...</header> with just the
     inner <h1>...</h1> (preserving chapter title, dropping nav/search/
     part-label wrapper)
  3. Strip <nav class="chapter-nav">...</nav> (web prev/next pager)
  4. Strip <footer>...</footer> elements that appear inside chapters
     (only chapter-edition footer, not page-level footers)
  5. Strip <span class="pagefind-meta-injected" hidden></span> markers
  6. Strip data-pagefind-meta="..." attributes
  7. Strip target="_blank" and rel="noopener|noreferrer" attrs from <a>
  8. Unwrap <main class="content">...</main> (keep contents, drop main
     element so we don't have a single root other than body)

After stripping, each chapter body is just: [H1] + [content] + nothing.
Visually identical on Kindle (chrome was already CSS-hidden) but the
DOM no longer has repeated chrome elements that a classifier could
flag.

Run AFTER fix_fxl_filenames.py, BEFORE final OPF cleanup.
"""
from __future__ import annotations
import argparse
import os
import re
import sys
import zipfile
from pathlib import Path


# 1. Skip link at body start
SKIP_LINK_RE = re.compile(
    r'<a\b[^>]*\bclass="[^"]*skip-link[^"]*"[^>]*>.*?</a>',
    re.DOTALL | re.IGNORECASE)

# 2. <header class="chapter-header">...</header>  — replace with inner <h1>
CHAPTER_HEADER_RE = re.compile(
    r'<header\b[^>]*\bclass="[^"]*chapter-header[^"]*"[^>]*>(.*?)</header>',
    re.DOTALL | re.IGNORECASE)
INNER_H1_RE = re.compile(
    r'<h1\b[^>]*>.*?</h1>', re.DOTALL | re.IGNORECASE)

# 3. <nav class="chapter-nav">...</nav>  — strip entirely
CHAPTER_NAV_RE = re.compile(
    r'<nav\b[^>]*\bclass="[^"]*chapter-nav[^"]*"[^>]*>.*?</nav>',
    re.DOTALL | re.IGNORECASE)

# 4. <footer>...</footer>  — strip (chapter-edition footer)
FOOTER_RE = re.compile(
    r'<footer\b[^>]*>.*?</footer>', re.DOTALL | re.IGNORECASE)

# 5. <span class="pagefind-meta-injected" hidden></span>
PAGEFIND_SPAN_RE = re.compile(
    r'<span\b[^>]*\bclass="[^"]*pagefind-meta-injected[^"]*"[^>]*>.*?</span>',
    re.DOTALL | re.IGNORECASE)

# 6. data-pagefind-meta="..." attributes
PAGEFIND_ATTR_RE = re.compile(
    r'\s*\bdata-pagefind-meta="[^"]*"', re.IGNORECASE)

# 7. target="_blank" and rel="noopener noreferrer" on <a>
TARGET_BLANK_RE = re.compile(
    r'\s*\btarget="_blank"', re.IGNORECASE)
REL_NOOPENER_RE = re.compile(
    r'\s*\brel="(?:noopener|noreferrer|noopener noreferrer|noreferrer noopener)"',
    re.IGNORECASE)

# 8. <main class="content"...>...</main>  — unwrap (keep inner content)
MAIN_OPEN_RE = re.compile(
    r'<main\b[^>]*>', re.IGNORECASE)
MAIN_CLOSE_RE = re.compile(
    r'</main>', re.IGNORECASE)


def strip_chrome(html: str) -> tuple[str, dict]:
    stats = {
        'skip_link': 0,
        'chapter_header_unwrapped': 0,
        'chapter_nav': 0,
        'footer': 0,
        'pagefind_span': 0,
        'pagefind_attr': 0,
        'target_blank': 0,
        'rel_noopener': 0,
        'main_unwrapped': 0,
    }

    # 1. Skip link
    html, n = SKIP_LINK_RE.subn('', html)
    stats['skip_link'] = n

    # 2. <header class="chapter-header"> -> just <h1> inside
    def replace_header(m):
        inner = m.group(1)
        h1 = INNER_H1_RE.search(inner)
        return h1.group(0) if h1 else ''
    html, n = CHAPTER_HEADER_RE.subn(replace_header, html)
    stats['chapter_header_unwrapped'] = n

    # 3. <nav class="chapter-nav">
    html, n = CHAPTER_NAV_RE.subn('', html)
    stats['chapter_nav'] = n

    # 4. <footer>
    html, n = FOOTER_RE.subn('', html)
    stats['footer'] = n

    # 5. <span class="pagefind-meta-injected">
    html, n = PAGEFIND_SPAN_RE.subn('', html)
    stats['pagefind_span'] = n

    # 6. data-pagefind-meta attrs
    html, n = PAGEFIND_ATTR_RE.subn('', html)
    stats['pagefind_attr'] = n

    # 7. target="_blank" and rel="noopener"
    html, n = TARGET_BLANK_RE.subn('', html)
    stats['target_blank'] = n
    html, n = REL_NOOPENER_RE.subn('', html)
    stats['rel_noopener'] = n

    # 8. <main> unwrap (open and close tags removed; inner content stays)
    html, n_open = MAIN_OPEN_RE.subn('', html)
    html, n_close = MAIN_CLOSE_RE.subn('', html)
    stats['main_unwrapped'] = min(n_open, n_close)

    return html, stats


def patch(epub_path: Path) -> dict:
    totals = {
        'files_scanned': 0,
        'files_modified': 0,
        'skip_link': 0,
        'chapter_header_unwrapped': 0,
        'chapter_nav': 0,
        'footer': 0,
        'pagefind_span': 0,
        'pagefind_attr': 0,
        'target_blank': 0,
        'rel_noopener': 0,
        'main_unwrapped': 0,
    }
    tmp_out = epub_path.with_suffix(epub_path.suffix + '.tmp')
    with zipfile.ZipFile(epub_path, 'r') as zin, \
         zipfile.ZipFile(tmp_out, 'w', zipfile.ZIP_DEFLATED) as zout:
        # mimetype first uncompressed
        for info in zin.infolist():
            if info.filename == 'mimetype':
                zout.writestr(info, zin.read(info.filename),
                              compress_type=zipfile.ZIP_STORED)
                break

        for info in zin.infolist():
            if info.filename == 'mimetype':
                continue
            data = zin.read(info.filename)
            if info.filename.lower().endswith(('.xhtml', '.html')):
                # Skip cover.xhtml and nav.xhtml (don't have the chrome)
                base = info.filename.split('/')[-1].lower()
                if base in ('cover.xhtml', 'nav.xhtml'):
                    zout.writestr(info.filename, data, compress_type=zipfile.ZIP_DEFLATED)
                    continue
                totals['files_scanned'] += 1
                html = data.decode('utf-8', errors='ignore')
                new_html, s = strip_chrome(html)
                if any(s[k] for k in s):
                    totals['files_modified'] += 1
                    for k in s:
                        totals[k] += s[k]
                    data = new_html.encode('utf-8')
            zout.writestr(info.filename, data, compress_type=zipfile.ZIP_DEFLATED)
    os.replace(tmp_out, epub_path)
    return totals


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('epub', type=Path)
    args = ap.parse_args()
    if not args.epub.exists():
        sys.exit(f'EPUB not found: {args.epub}')
    print(f'Stripping web chrome from {args.epub}')
    t = patch(args.epub)
    print(f'  Files scanned:                {t["files_scanned"]}')
    print(f'  Files modified:               {t["files_modified"]}')
    print(f'  Skip-link removed:            {t["skip_link"]}')
    print(f'  Chapter-header unwrapped:     {t["chapter_header_unwrapped"]}')
    print(f'  Chapter-nav removed:          {t["chapter_nav"]}')
    print(f'  Footer removed:               {t["footer"]}')
    print(f'  Pagefind-meta span removed:   {t["pagefind_span"]}')
    print(f'  data-pagefind-meta attr removed: {t["pagefind_attr"]}')
    print(f'  target="_blank" removed:      {t["target_blank"]}')
    print(f'  rel="noopener" removed:       {t["rel_noopener"]}')
    print(f'  <main> unwrapped:             {t["main_unwrapped"]}')
    print('DONE.')


if __name__ == '__main__':
    main()
