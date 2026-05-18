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

Exclusions for the fun-note suggestion: tools-of-the-trade catalogs,
reference and "libraries and frameworks" sections, appendices, and the
front matter all have a reference-style register where comic-style
fun-notes would feel out of place. Flagging them was just noise.
"""
import re
from collections import namedtuple

PRIORITY = "P2"
CHECK_ID = "IMAGE_OPPORTUNITY"
DESCRIPTION = "Page has no hero image, no figure illustrations, or no fun-note comic"

Issue = namedtuple("Issue", ["priority", "check_id", "filepath", "line", "message"])

CHAPTER_OPENER = re.compile(r'class="illustration\s+chapter-opener"', re.I)
# Any <figure> element with an actual image OR svg counts as a figure.
# We accept the bare <figure>, <figure class="illustration">, and
# <figure class="diagram"> variants used across the book. A <figure> that
# contains only a <table> is also a figure (numbered table); the detector
# requires the inner <img> or <svg> only when the wrapping class is omitted.
ANY_FIGURE = re.compile(
    r'<figure(?:\s+class="[^"]+")?\s*>',
    re.I,
)
ANY_DIAGRAM = re.compile(r'class="diagram-container"|<svg\b', re.I)
FUN_NOTE = re.compile(r'class="callout\s+fun-note"', re.I)

# Path fragments where reference / catalog content lives. Fun-note
# comics don't belong in any of these.
REFERENCE_PATHS = (
    "tools-of-the-trade", "retrieval-tools", "conv-ai-tools",
    "responsible-ai-tools", "scale-tools",
    "appendices", "appendix-",
    "front-matter", "back-matter",
)


def _is_reference_section(rel: str) -> bool:
    return any(frag in rel for frag in REFERENCE_PATHS)


def run(filepath, html, context):
    issues = []
    book_root = context["book_root"]
    rel = str(filepath.relative_to(book_root)).replace("\\", "/").lower()

    # Chapter index pages: require a chapter-opener hero image
    if filepath.name == 'index.html' and 'module-' in rel:
        if not CHAPTER_OPENER.search(html):
            issues.append(Issue(PRIORITY, CHECK_ID, filepath, 1,
                'Chapter-index has no <figure class="illustration chapter-opener"> hero image'))

    # Section pages: should have at least one figure illustration OR diagram.
    # This is a soft suggestion (P3, informational), not a content error.
    # Many sections are pure-prose by design (theory, math derivations,
    # discussion) and don't need a diagram; flagging them as P2 issues
    # produced 200+ noise lines.
    if filepath.name.startswith('section-'):
        if not ANY_FIGURE.search(html) and not ANY_DIAGRAM.search(html):
            issues.append(Issue("P3", CHECK_ID, filepath, 1,
                'Section has no figure or diagram (consider adding illustration when content invites it)'))
        # Fun-note presence is "nice to have", and only in non-reference content.
        if not FUN_NOTE.search(html) and not _is_reference_section(rel):
            issues.append(Issue("P3", CHECK_ID, filepath, 1,
                'Section has no <div class="callout fun-note"> (consider adding comic/analogy)'))

    return issues
