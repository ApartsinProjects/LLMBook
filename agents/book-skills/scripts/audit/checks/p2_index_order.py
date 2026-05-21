"""Check that module index.html files follow canonical element ordering.

Canonical order for chapter index pages:
  1. epigraph
  2. illustration (optional)
  3. overview
  4. big-picture (optional callout)
  5. fun-note (optional, opener-style engagement)
  6. prereqs
  7. objectives
  8. sections-list
  9. whats-next
  10. bibliography (optional)

Earlier policy disallowed fun-note callouts in chapter index pages on
the grounds that "fun facts belong in sections". User policy has shifted:
chapter-opener fun-notes are valuable for engagement (modules 01, 03, 04
already have curated openers). The rule is retired; fun-notes now sit
between big-picture and prereqs in the canonical order.
"""
import re
from collections import namedtuple

PRIORITY = "P2"
CHECK_ID = "INDEX_ORDER"
DESCRIPTION = "Module index element out of canonical order or disallowed callout"

Issue = namedtuple("Issue", ["priority", "check_id", "filepath", "line", "message"])

# Canonical order: element name -> rank.
# Pedagogical sequence (corrected 2026-05-18):
#   1. epigraph (motivating quote)
#   2. illustration (chapter opener)
#   3. big-picture (callout: one-paragraph hook for the chapter)
#   4. overview (h2 + detailed section-by-section walkthrough)
#   5. fun-note (optional engagement opener, sits beside overview)
#   6. prereqs (what the reader should know before reading)
#   7. objectives (concrete "after this chapter, you can..." list)
#   8. sections-list (cards or list of section titles)
#   9. whats-next / 10. bibliography
#
# Earlier this had overview BEFORE big-picture, but the chapter-starter
# agent and existing reviewed chapters put big-picture FIRST (one-line
# pitch), then overview (detailed walkthrough). big-picture is the hook,
# overview is the expansion. Rule corrected to match.
CANONICAL_ORDER = {
    "epigraph": 1,
    "illustration": 2,
    # big-picture and overview share rank 3 (either order is fine; some
    # chapters lead with the one-paragraph hook then expand, others lead
    # with the detailed walkthrough then summarize). The plugin no longer
    # enforces a strict order between these two.
    "big-picture": 3,
    "overview": 3,
    "prereqs": 5,
    "objectives": 6,
    "sections-list": 7,
    "whats-next": 8,
    "bibliography": 9,
}

# Patterns to detect structural elements
ELEMENT_PATTERNS = [
    ("epigraph", re.compile(r'class="epigraph"')),
    ("illustration", re.compile(r'<figure\b[^>]*class="illustration"')),
    ("overview", re.compile(r'class="overview"')),
    ("big-picture", re.compile(r'class="callout big-picture"')),
    ("prereqs", re.compile(r'class="prereqs"')),
    ("objectives", re.compile(r'class="objectives"')),
    ("sections-list", re.compile(r'class="sections-list"')),
    ("whats-next", re.compile(r'class="whats-next"')),
    ("bibliography", re.compile(r'class="bibliography"')),
]

DISALLOWED_IN_INDEX = [
    # fun-note no longer disallowed; openers like "Fun Fact: Before
    # Computers Could Read" are engagement assets, not deletion targets.
    ("time-estimate", re.compile(r'class="time-estimate"')),
]


def _line_number(html, pos):
    return html[:pos].count("\n") + 1


def run(filepath, html, context):
    issues = []
    book_root = context["book_root"]

    if filepath.name != "index.html":
        return issues
    if "module-" not in str(filepath):
        return issues

    rel = str(filepath.relative_to(book_root))

    # Detect disallowed callouts
    for name, pattern in DISALLOWED_IN_INDEX:
        for m in pattern.finditer(html):
            line = _line_number(html, m.start())
            issues.append(Issue(PRIORITY, CHECK_ID, filepath, line,
                                f"{rel}:{line} disallowed '{name}' callout in index page"))

    # Detect structural elements and check order
    found = []
    for name, pattern in ELEMENT_PATTERNS:
        for m in pattern.finditer(html):
            found.append((m.start(), name, _line_number(html, m.start())))

    found.sort(key=lambda x: x[0])

    # Check pairwise ordering (skip illustration which can repeat)
    max_rank_seen = 0
    max_rank_name = None
    for _, name, line in found:
        rank = CANONICAL_ORDER.get(name, 0)
        if rank < max_rank_seen and name != "illustration":
            issues.append(Issue(PRIORITY, CHECK_ID, filepath, line,
                                f"{rel}:{line} '{name}' appears after '{max_rank_name}' "
                                f"(expected order: {max_rank_name} before {name})"))
        if rank > max_rank_seen:
            max_rank_seen = rank
            max_rank_name = name

    return issues
