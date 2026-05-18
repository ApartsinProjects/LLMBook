"""Deeper layout/format validator for chapter-index pages (part-*/module-*/index.html).

Canonical structure (verified against module-01-foundations-nlp-text-representation/index.html):
  1. <head> with meta-desc, title, GA
  2. <header class="chapter-header"> + nav + breadcrumb + h1
  3. <main class="content">
  4. <figure class="illustration chapter-opener"> hero image (recommended)
  5. <span class="pagefind-meta-injected" data-pagefind-meta="chapter:..."> and "part:..."
  6. <blockquote class="epigraph">
  7. <div class="callout looking-back"> (link to prev chapter)
  8. <div class="overview"><h2>Chapter Overview</h2></div>
  9. <div class="callout big-picture">
 10. <div class="callout pathway"> with title "Learning Objectives"
 11. <div class="callout note"> with title "Prerequisites" (or <div class="prereqs">)
 12. <h2>Sections</h2> <ul class="sections-list"> with <a class="section-card">
 13. <div class="whats-next"> with link to first section
 14. <nav class="chapter-nav"> with prev-chapter / up-to-part / next-chapter
 15. <footer> inside </main>
"""
import re
from collections import namedtuple

PRIORITY = "P1"
CHECK_ID = "CHAPTER_INDEX_LAYOUT"
DESCRIPTION = "Chapter-index page missing canonical structural element or has wrong layout"

Issue = namedtuple("Issue", ["priority", "check_id", "filepath", "line", "message"])

REQUIRED_PATTERNS = [
    ("header.chapter-header", re.compile(r'<header\s+class="chapter-header"', re.I)),
    ("main.content", re.compile(r'<main\s+class="content"', re.I)),
    ("h1", re.compile(r'<h1\b', re.I)),
    ("breadcrumb", re.compile(r'class="page-breadcrumb"', re.I)),
    ("pagefind chapter meta", re.compile(r'data-pagefind-meta="chapter:', re.I)),
    ("epigraph", re.compile(r'class="epigraph"', re.I)),
    ("big-picture callout", re.compile(r'class="callout\s+big-picture"', re.I)),
    ("sections-list", re.compile(r'class="sections-list"', re.I)),
    ("section-card", re.compile(r'class="section-card"', re.I)),
    ("whats-next", re.compile(r'class="whats-next"', re.I)),
    ("chapter-nav", re.compile(r'<nav\s+class="chapter-nav"', re.I)),
    ("footer", re.compile(r'<footer\b', re.I)),
    ("ga snippet", re.compile(r'G-PWPHBQL2VL', re.I)),
]

# Optional but strongly-recommended
RECOMMENDED_PATTERNS = [
    ("chapter-opener hero image", re.compile(r'class="illustration\s+chapter-opener"', re.I)),
    ("looking-back callout", re.compile(r'class="callout\s+looking-back"', re.I)),
    ("overview block", re.compile(r'<div\s+class="overview"', re.I)),
    ("Learning Objectives", re.compile(r'Learning Objectives', re.I)),
    ("Prerequisites", re.compile(r'(class="prereqs"|>\s*Prerequisites\s*<)', re.I)),
]

FOOTER_OUTSIDE_MAIN = re.compile(r'</main>\s*<footer', re.I)


def run(filepath, html, context):
    issues = []
    book_root = context["book_root"]
    rel = str(filepath.relative_to(book_root)).replace("\\", "/")
    parts = rel.split("/")
    # part-*/module-*/index.html
    if not (len(parts) == 3 and parts[0].startswith("part-") and parts[1].startswith("module-") and parts[2] == "index.html"):
        return issues

    for name, pat in REQUIRED_PATTERNS:
        if not pat.search(html):
            issues.append(Issue(PRIORITY, CHECK_ID, filepath, 1,
                f'Chapter-index missing canonical {name}'))

    for name, pat in RECOMMENDED_PATTERNS:
        if not pat.search(html):
            issues.append(Issue("P2", CHECK_ID, filepath, 1,
                f'Chapter-index missing recommended {name}'))

    if FOOTER_OUTSIDE_MAIN.search(html):
        issues.append(Issue(PRIORITY, CHECK_ID, filepath, 1,
            'Chapter-index footer is outside <main>'))

    # Chapter-nav should have prev/up/next
    nav_m = re.search(r'<nav\s+class="chapter-nav"[^>]*>([\s\S]*?)</nav>', html, re.I)
    if nav_m:
        body = nav_m.group(1)
        if 'class="up"' not in body:
            issues.append(Issue(PRIORITY, CHECK_ID, filepath, 1,
                'Chapter-index nav missing <a class="up"> link to part index'))

    return issues
