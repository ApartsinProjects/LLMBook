"""Audit image opportunities: chapter openers, section illustrations, comic
fun-illustrations.

Per user request to "audit images for fun/comic/opener images opportunities."

We flag:
  - Chapter index pages with no `<figure class="illustration chapter-opener">` hero
    image (49 such pages were flagged by CHAPTER_INDEX_LAYOUT)
  - Section pages with no <figure class="illustration"> at all (sections without
    any image, which read as text-heavy walls)
  - Section pages with no <div class="callout fun-note"> (the closest we have
    to a comic-illustration placeholder; many old pages have fun-note callouts
    with embedded illustrations)
"""
import re
from collections import namedtuple

PRIORITY = "P2"
CHECK_ID = "IMAGE_OPPORTUNITY"
DESCRIPTION = "Page has no hero image, no figure illustrations, or no fun-note comic"

Issue = namedtuple("Issue", ["priority", "check_id", "filepath", "line", "message"])

CHAPTER_OPENER = re.compile(r'class="illustration\s+chapter-opener"', re.I)
ANY_FIGURE = re.compile(r'<figure\s+class="illustration"', re.I)
ANY_DIAGRAM = re.compile(r'class="diagram-container"|<svg\b', re.I)
FUN_NOTE = re.compile(r'class="callout\s+fun-note"', re.I)


def run(filepath, html, context):
    issues = []
    book_root = context["book_root"]
    rel = str(filepath.relative_to(book_root)).replace("\\", "/")

    # Chapter index pages: require a chapter-opener hero image
    if filepath.name == 'index.html' and 'module-' in rel:
        if not CHAPTER_OPENER.search(html):
            issues.append(Issue(PRIORITY, CHECK_ID, filepath, 1,
                'Chapter-index has no <figure class="illustration chapter-opener"> hero image'))

    # Section pages: should have at least one figure illustration OR diagram
    if filepath.name.startswith('section-'):
        if not ANY_FIGURE.search(html) and not ANY_DIAGRAM.search(html):
            issues.append(Issue(PRIORITY, CHECK_ID, filepath, 1,
                'Section has no figure or diagram (text-heavy; consider adding illustration or fun-note comic)'))
        # Fun-note presence is "nice to have"
        if not FUN_NOTE.search(html):
            issues.append(Issue("P3", CHECK_ID, filepath, 1,
                'Section has no <div class="callout fun-note"> (consider adding comic/analogy)'))

    return issues
