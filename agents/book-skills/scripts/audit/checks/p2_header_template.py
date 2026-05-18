"""Verify all part/chapter/section pages match their canonical header template.

See docs/content-audit/HEADER_TEMPLATES.md for the three templates.

Each page type must have certain header elements:

  Part index   (part-N-*/index.html):
    - <header class="chapter-header">
    - <nav class="header-nav">
    - <a class="book-title-link"> with href "../index.html"
    - <a class="toc-link"> with href "../toc.html"
    - <div class="page-breadcrumb" data-pagefind-meta="part">
    - <h1> with "Part {Roman}:"
    - NO <div class="header-search">
    - NO <div class="page-current">

  Chapter index (part-N-*/module-NN-*/index.html):
    - <header class="chapter-header">
    - <nav class="header-nav">
    - <div class="header-search">
    - <div class="page-breadcrumb" data-pagefind-meta="chapter">
    - <h1>
    - NO <div class="page-current">

  Section (part-N-*/module-NN-*/section-NN.M.html):
    - <header class="chapter-header">
    - <nav class="header-nav">
    - <div class="header-search">
    - <div class="page-breadcrumb" data-pagefind-meta="chapter">
    - <h1>
    - <div class="page-current"> with "Section NN.M"
"""
import re
from collections import namedtuple
from pathlib import Path

PRIORITY = "P2"
CHECK_ID = "HEADER_TEMPLATE"
DESCRIPTION = "Page header does not match the canonical template (part/chapter/section)"

Issue = namedtuple("Issue", ["priority", "check_id", "filepath", "line", "message"])


def _classify(filepath: Path) -> str | None:
    """Return 'part', 'chapter', 'section', or None."""
    name = filepath.name
    parts = filepath.parts
    # Section pages
    if name.startswith('section-') and name.endswith('.html'):
        return 'section'
    # Chapter index: inside a module-* dir, name == index.html
    if name == 'index.html':
        for p in parts[-3:]:
            if p.startswith('module-'):
                return 'chapter'
        # Part index: filename index.html, directly under part-*/
        for p in parts:
            if p.startswith('part-') and parts[parts.index(p) + 1] == name:
                return 'part'
    return None


# Required-presence checks
HEADER_CLASS_RE = re.compile(r'<header\s+class="chapter-header"', re.IGNORECASE)
HEADER_NAV_RE = re.compile(r'<nav\s+class="header-nav"', re.IGNORECASE)
BOOK_TITLE_RE = re.compile(r'<a\s+class="book-title-link"', re.IGNORECASE)
TOC_LINK_RE = re.compile(r'<a\s+class="toc-link"', re.IGNORECASE)
HEADER_SEARCH_RE = re.compile(r'<div\s+class="header-search"', re.IGNORECASE)
BREADCRUMB_PART_RE = re.compile(r'<div\s+class="page-breadcrumb"\s+data-pagefind-meta="part"', re.IGNORECASE)
BREADCRUMB_CH_RE = re.compile(r'<div\s+class="page-breadcrumb"\s+data-pagefind-meta="chapter"', re.IGNORECASE)
H1_RE = re.compile(r'<h1\b', re.IGNORECASE)
PAGE_CURRENT_RE = re.compile(r'<div\s+class="page-current"', re.IGNORECASE)
# Wrong header classes (must be chapter-header)
WRONG_HEADER_RE = re.compile(r'<header\s+class="(section-header|part-header)"', re.IGNORECASE)


def run(filepath, html, context):
    issues = []
    if filepath.suffix != ".html":
        return issues

    kind = _classify(filepath)
    if kind is None:
        return issues

    def _line(pat):
        m = pat.search(html)
        return html.count("\n", 0, m.start()) + 1 if m else 0

    def _check_present(pat, name):
        if not pat.search(html):
            issues.append(Issue(
                PRIORITY, CHECK_ID, filepath, 1,
                f'{kind.upper()} template: missing {name}',
            ))

    def _check_absent(pat, name):
        m = pat.search(html)
        if m:
            line = html.count("\n", 0, m.start()) + 1
            issues.append(Issue(
                PRIORITY, CHECK_ID, filepath, line,
                f'{kind.upper()} template: should NOT have {name}',
            ))

    # Wrong header class
    m = WRONG_HEADER_RE.search(html)
    if m:
        line = html.count("\n", 0, m.start()) + 1
        issues.append(Issue(
            PRIORITY, CHECK_ID, filepath, line,
            f'Header uses wrong class "{m.group(1)}"; must be "chapter-header"',
        ))

    # Common to all
    _check_present(HEADER_CLASS_RE, '<header class="chapter-header">')
    _check_present(HEADER_NAV_RE, '<nav class="header-nav">')
    _check_present(BOOK_TITLE_RE, '<a class="book-title-link">')
    _check_present(TOC_LINK_RE, '<a class="toc-link">')
    _check_present(H1_RE, '<h1>')

    # Type-specific
    if kind == 'part':
        _check_present(BREADCRUMB_PART_RE, 'breadcrumb with data-pagefind-meta="part"')
        _check_absent(HEADER_SEARCH_RE, '<div class="header-search"> (only chapter/section pages have it)')
        _check_absent(PAGE_CURRENT_RE, '<div class="page-current"> (only section pages have it)')
    elif kind == 'chapter':
        _check_present(HEADER_SEARCH_RE, '<div class="header-search">')
        _check_present(BREADCRUMB_CH_RE, 'breadcrumb with data-pagefind-meta="chapter"')
        _check_absent(PAGE_CURRENT_RE, '<div class="page-current"> (only section pages have it)')
    elif kind == 'section':
        _check_present(HEADER_SEARCH_RE, '<div class="header-search">')
        _check_present(BREADCRUMB_CH_RE, 'breadcrumb with data-pagefind-meta="chapter"')
        _check_present(PAGE_CURRENT_RE, '<div class="page-current">Section NN.M</div>')

    return issues
