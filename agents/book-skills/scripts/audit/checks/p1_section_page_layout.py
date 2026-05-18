"""Comprehensive layout/format validator for section pages (section-*.html).

Canonical structure (verified against section-42.2.html, section-1.1.html, section-23.1.html):
  1. <head> with meta-desc, title, GA snippet
  2. <header class="chapter-header"> with nav + breadcrumb + h1 + page-current
  3. <main class="content">
  4. <span class="pagefind-meta-injected"> (part: + chapter:)
  5. <blockquote class="epigraph"> (with AI-Agent style attribution)
  6. <div class="callout big-picture"> (with bridge to LLM/agent context)
  7. <div class="prerequisites"> (with h3 + paragraph)
  8. Optional <figure class="illustration"> opener
  9. Body content: <h2>/<h3> headings + paragraphs + code + figures + callouts
 10. <div class="whats-next"> with link to next section
 11. <details class="bibliography-collapsible"> (canonical: open, with <summary>)
 12. <nav class="chapter-nav"> with prev-section / up-to-chapter / next-section
 13. <footer> INSIDE </main>

This validator is the meta-check that aggregates many sub-rules. It complements
the more specific plugins (SELFCHECK_NON_CANONICAL, BIG_PICTURE_EXCESS_BOLD,
SECTION_ORDER, etc.) by providing a single per-page summary.
"""
import re
from collections import namedtuple

PRIORITY = "P1"
CHECK_ID = "SECTION_PAGE_LAYOUT"
DESCRIPTION = "Section page missing canonical structural element"

Issue = namedtuple("Issue", ["priority", "check_id", "filepath", "line", "message"])

REQUIRED = [
    ("ga snippet", re.compile(r'G-PWPHBQL2VL', re.I)),
    ("meta description", re.compile(r'<meta\s+[^>]*name="description"', re.I)),
    ("header.chapter-header|section-header", re.compile(r'<header\s+class="(?:chapter-header|section-header)"', re.I)),
    ("breadcrumb", re.compile(r'class="page-breadcrumb"', re.I)),
    ("page-current", re.compile(r'class="page-current"', re.I)),
    ("main.content", re.compile(r'<main\s+class="content"', re.I)),
    ("pagefind chapter meta", re.compile(r'data-pagefind-meta="chapter:', re.I)),
    ("h1", re.compile(r'<h1\b', re.I)),
    ("chapter-nav", re.compile(r'<nav\s+class="chapter-nav"', re.I)),
    ("footer", re.compile(r'<footer\b', re.I)),
]

RECOMMENDED = [
    ("epigraph", re.compile(r'class="epigraph"', re.I)),
    ("big-picture callout", re.compile(r'class="callout\s+big-picture"', re.I)),
    ("prerequisites block", re.compile(r'class="prerequisites"', re.I)),
    # Accept both legacy <div class="whats-next"> and canonical
    # <div class="callout whats-next">.
    ("whats-next", re.compile(r'class="(?:callout\s+)?whats-next"', re.I)),
    ("bibliography-collapsible", re.compile(r'class="bibliography-collapsible"', re.I)),
]

FOOTER_OUTSIDE_MAIN = re.compile(r'</main>\s*<footer', re.I)
NAV_OUTSIDE_MAIN = re.compile(r'</main>\s*<nav\s+class="chapter-nav"', re.I)


def run(filepath, html, context):
    issues = []
    book_root = context["book_root"]
    if not filepath.name.startswith("section-"):
        return issues

    rel = str(filepath.relative_to(book_root)).replace("\\", "/")

    # Reference-style sections (tools-of-the-trade, appendix, scale-tools) are
    # catalog-style content, not narrative. Skip epigraph and big-picture
    # recommendations for them.
    rel_lower = rel.lower()
    is_reference_section = (
        'module-05-tools-of-the-trade' in rel_lower
        or '/tools-of-the-trade/' in rel_lower
        or 'module-19-tools-of-the-trade' in rel_lower
        or 'module-30-tools-of-the-trade' in rel_lower
        or 'module-45-tools-of-the-trade' in rel_lower
        or 'module-51-tools-of-the-trade' in rel_lower
        or 'module-61-scale-tools' in rel_lower
        or 'module-71-tools-of-the-trade' in rel_lower
        or 'module-79-tools-of-the-trade' in rel_lower
        or '/appendices/' in rel_lower
        or '/appendix-' in rel_lower
    )

    for name, pat in REQUIRED:
        if not pat.search(html):
            issues.append(Issue(PRIORITY, CHECK_ID, filepath, 1,
                f'Section missing REQUIRED {name}'))

    for name, pat in RECOMMENDED:
        # Reference sections (tools-of-the-trade, appendix) don't need narrative
        # elements: epigraph, big-picture, prerequisites, whats-next. They keep
        # bibliography-collapsible since vendor catalogs benefit from refs.
        if is_reference_section and name in (
            "epigraph", "big-picture callout", "prerequisites block", "whats-next"
        ):
            continue
        if not pat.search(html):
            issues.append(Issue("P2", CHECK_ID, filepath, 1,
                f'Section missing recommended {name}'))

    if FOOTER_OUTSIDE_MAIN.search(html):
        issues.append(Issue(PRIORITY, CHECK_ID, filepath, 1,
            'Section footer is outside <main>'))

    if NAV_OUTSIDE_MAIN.search(html):
        issues.append(Issue(PRIORITY, CHECK_ID, filepath, 1,
            'Section chapter-nav is outside <main>'))

    # Detect merged-content marker (e.g. section-40.1 with "(merged content)" h2)
    if re.search(r'\(merged\s+content\)', html, re.I):
        issues.append(Issue("P0", CHECK_ID, filepath, 1,
            'Section contains "(merged content)" marker -- likely forcibly-joined sections that should be split'))

    # Detect duplicate h2 numbering (e.g. two "40.1.1" h2 in the same file)
    # Match the FULL dotted number (so "14.2.3.5" doesn't collide with "14.2.3").
    h2_nums = re.findall(r'<h2[^>]*>\s*(\d+(?:\.\d+)+)\s', html)
    dup_nums = [n for n in set(h2_nums) if h2_nums.count(n) > 1]
    if dup_nums:
        issues.append(Issue("P0", CHECK_ID, filepath, 1,
            f'Section has duplicate h2 numbering: {sorted(dup_nums)}'))

    return issues
