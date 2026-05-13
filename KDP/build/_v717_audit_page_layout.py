"""9th edition follow-up: standard page-layout audit.

Verifies that every section / index page in the book follows the
canonical layout invariants:

  L1. Has exactly one <header class="chapter-header"> block.
  L2. Has exactly one <main class="content"> block.
  L3. Has at least one <nav class="chapter-nav"> block.
  L4. Has at least one <footer> block.
  L5. The LAST chapter-nav appears AFTER the LAST <h2> in the file's
      main content (i.e., the nav is not stranded above subsequent
      content like a merged-section).
  L6. The LAST footer is the LAST element before </main> (or before
      the closing <script> if <main> already closed).
  L7. Chapter-opener images do NOT live inside <header>.

Read-only audit. Reports any violation per-file.
"""
from __future__ import annotations
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
SKIP = ('node_modules', '.git/', 'pagefind/', 'KDP/build/', 'KDP/output/',
        'templates/', '_archive/', 'temp_epub/', 'vendor/', '/agents/')

HEADER_RE = re.compile(r'<header\s+class="chapter-header"[^>]*>', re.IGNORECASE)
HEADER_CLOSE = re.compile(r'</header\s*>', re.IGNORECASE)
MAIN_RE = re.compile(r'<main\s+class="content"[^>]*>', re.IGNORECASE)
MAIN_CLOSE = re.compile(r'</main\s*>', re.IGNORECASE)
NAV_RE = re.compile(
    r'<nav\s+class="(?:[^"]*\s)?chapter-nav(?:\s[^"]*)?"[^>]*>', re.IGNORECASE)
FOOTER_RE = re.compile(r'<footer\b', re.IGNORECASE)
H2_RE = re.compile(r'<h2\b', re.IGNORECASE)
FIG_OR_IMG = re.compile(r'<(?:figure\b|img\b)', re.IGNORECASE)
TOC_ICON = re.compile(r'class="toc-icon"', re.IGNORECASE)
AVATAR = re.compile(r'class="agent-avatar-inline[^"]*"', re.IGNORECASE)


def is_book_page(text: str) -> bool:
    """A book page has both chapter-header and main.content."""
    return bool(HEADER_RE.search(text) and MAIN_RE.search(text))


# Special pages that don't need chapter-nav (they ARE the navigation surface).
NAV_EXEMPT = (
    'toc.html',
    'index.html',  # the landing page (root index)
)


def audit(text: str, path_name: str = '') -> list[str]:
    issues: list[str] = []
    is_exempt = any(path_name.endswith(n) for n in NAV_EXEMPT)

    headers = list(HEADER_RE.finditer(text))
    if len(headers) != 1:
        issues.append(f'L1: {len(headers)} <header class="chapter-header"> (expected 1)')

    mains = list(MAIN_RE.finditer(text))
    if len(mains) != 1:
        issues.append(f'L2: {len(mains)} <main class="content"> (expected 1)')

    navs = list(NAV_RE.finditer(text))
    footers = list(FOOTER_RE.finditer(text))

    if not is_exempt:
        if not navs:
            issues.append('L3: no <nav class="chapter-nav">')
        if not footers:
            issues.append('L4: no <footer>')

    # L5: last chapter-nav appears after last h2
    if navs:
        h2s = list(H2_RE.finditer(text))
        if h2s:
            last_h2 = h2s[-1].start()
            last_nav = navs[-1].start()
            if last_nav < last_h2:
                last_h2_line = text[:last_h2].count('\n') + 1
                last_nav_line = text[:last_nav].count('\n') + 1
                issues.append(
                    f'L5: last chapter-nav at L{last_nav_line} comes BEFORE '
                    f'last <h2> at L{last_h2_line} (content after the nav)')

    # L6: last footer closes right before </main>, with only whitespace,
    # comments, or </section> (for pages whose <main> contains a <section>)
    # between them.
    if footers and mains:
        # Find the </footer> matching the last <footer
        last_footer_open = footers[-1].start()
        footer_close_re = re.compile(r'</footer\s*>', re.IGNORECASE)
        fc = footer_close_re.search(text, last_footer_open)
        main_close = MAIN_CLOSE.search(text)
        if fc and main_close and fc.end() < main_close.start():
            between = text[fc.end():main_close.start()]
            # Strip whitespace, HTML comments, benign closing tags, and
            # the trailing PagefindUI initialization <script>.
            cleaned = re.sub(r'<!--.*?-->', '', between, flags=re.DOTALL)
            cleaned = re.sub(r'<script\b[\s\S]*?</script\s*>', '', cleaned,
                             flags=re.IGNORECASE)
            cleaned = re.sub(r'</section\s*>', '', cleaned, flags=re.IGNORECASE)
            cleaned = re.sub(r'</div\s*>', '', cleaned, flags=re.IGNORECASE)
            cleaned = re.sub(r'\s+', '', cleaned)
            if cleaned:
                fl = text[:fc.end()].count('\n') + 1
                ml = text[:main_close.start()].count('\n') + 1
                # Show first 60 chars of the offending content
                snippet = between.strip()[:80].replace('\n', ' ')
                issues.append(
                    f'L6: content between </footer> L{fl} and </main> L{ml}: '
                    f'"{snippet}"')

    # L7: chapter-opener images inside <header>
    if headers:
        header_close = HEADER_CLOSE.search(text, headers[0].end())
        if header_close:
            header_inner = text[headers[0].end():header_close.start()]
            # Strip avatar inline images + the search/toc icon area
            inner_clean = AVATAR.sub('', header_inner)
            # Find <figure or <img occurrences after stripping
            f_or_i = list(FIG_OR_IMG.finditer(inner_clean))
            for m in f_or_i:
                # Check if it's a toc-icon (in nav, not content)
                ctx = inner_clean[max(0, m.start() - 30):m.end() + 60]
                if 'toc-icon' in ctx or 'header-search' in ctx:
                    continue
                issues.append('L7: chapter-opener <figure>/<img> inside <header>')
                break

    return issues


def main() -> int:
    n_files = 0
    n_bad = 0
    n_issues = 0
    for p in sorted(ROOT.rglob('*.html')):
        sp = str(p).replace('\\', '/')
        if any(s in sp for s in SKIP):
            continue
        try:
            text = p.read_text(encoding='utf-8', errors='replace')
        except Exception:
            continue
        if not is_book_page(text):
            continue
        n_files += 1
        issues = audit(text, p.name)
        if issues:
            n_bad += 1
            n_issues += len(issues)
            print(f'  {p.relative_to(ROOT)}:')
            for issue in issues:
                print(f'    - {issue}')
    print(f'\nPages scanned: {n_files}')
    print(f'Files with layout issues: {n_bad}; total issues: {n_issues}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
