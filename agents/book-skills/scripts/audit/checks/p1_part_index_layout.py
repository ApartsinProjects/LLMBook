"""Deeper layout/format validator for part-index pages (part-N-*/index.html).

Canonical structure (verified against part-1, part-2, etc.):
  1. <head> with meta-desc, title, GA, vendor CSS/JS
  2. <header class="chapter-header"> with header-nav + book-title-link + toc-link
  3. <h1> with part title
  4. <main class="content">
  5. (optional) <figure class="illustration chapter-opener"> hero image
  6. <span class="pagefind-meta-injected" data-pagefind-meta="part:...">
  7. <blockquote class="epigraph"> (recommended)
  8. <div class="part-label">Part NN</div>
  9. <div class="part-overview"> opening paragraph(s)
 10. <div class="chapter-card"> ... </div> (one per chapter in the part)
 11. <div class="whats-next"> with link to first chapter
 12. <nav class="chapter-nav"> with prev-part / up-to-TOC / next-part
 13. <footer> inside </main>
"""
import re
from collections import namedtuple

PRIORITY = "P1"
CHECK_ID = "PART_INDEX_LAYOUT"
DESCRIPTION = "Part-index page missing canonical structural element or has wrong layout"

Issue = namedtuple("Issue", ["priority", "check_id", "filepath", "line", "message"])

REQUIRED_PATTERNS = [
    ("header.chapter-header", re.compile(r'<header\s+class="chapter-header"', re.I)),
    ("main.content", re.compile(r'<main\s+class="content"', re.I)),
    ("h1", re.compile(r'<h1\b', re.I)),
    ("part-overview", re.compile(r'class="part-overview"', re.I)),
    ("chapter-card", re.compile(r'class="chapter-card"', re.I)),
    ("whats-next", re.compile(r'class="whats-next"', re.I)),
    ("chapter-nav", re.compile(r'<nav\s+class="chapter-nav"', re.I)),
    ("footer", re.compile(r'<footer\b', re.I)),
    ("ga snippet", re.compile(r'G-PWPHBQL2VL', re.I)),
]

# Footer should be inside main
FOOTER_OUTSIDE_MAIN = re.compile(r'</main>\s*<footer', re.I)


def run(filepath, html, context):
    issues = []
    book_root = context["book_root"]
    rel = str(filepath.relative_to(book_root)).replace("\\", "/")
    # Only part-N/index.html (length 2 parts: ["part-N-...", "index.html"])
    parts = rel.split("/")
    if not (len(parts) == 2 and parts[0].startswith("part-") and parts[1] == "index.html"):
        return issues

    for name, pat in REQUIRED_PATTERNS:
        if not pat.search(html):
            issues.append(Issue(PRIORITY, CHECK_ID, filepath, 1,
                f'Part-index missing canonical {name}'))

    if FOOTER_OUTSIDE_MAIN.search(html):
        issues.append(Issue(PRIORITY, CHECK_ID, filepath, 1,
            'Part-index footer is outside <main> (move inside before </main>)'))

    # Check chapter-nav has up link to TOC
    nav_m = re.search(r'<nav\s+class="chapter-nav"[^>]*>([\s\S]*?)</nav>', html, re.I)
    if nav_m:
        body = nav_m.group(1)
        if 'href="../toc.html"' not in body and 'href="../index.html"' not in body:
            issues.append(Issue(PRIORITY, CHECK_ID, filepath, 1,
                'Part-index chapter-nav missing up-link to ../toc.html or ../index.html'))

    return issues
