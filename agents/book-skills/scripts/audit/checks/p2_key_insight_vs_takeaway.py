"""Detect callouts where key-insight and key-takeaway are swapped.

The two callout types look similar but play different pedagogical roles:

- `key-insight` is a single inline aha-moment. ONE paragraph, observational.
  Misuse: a key-insight that wraps a <ul> or <ol> list of bullets.

- `key-takeaway` is an end-of-section bulleted recap. Multiple bullets that
  summarize the section. Misuse: a key-takeaway that contains only one <p>
  and no list at all.

This check flags both shapes so the writer can swap the class, or restructure
the body, before the section ships.
"""
import re
from collections import namedtuple

PRIORITY = "P2"
CHECK_ID = "KEY_INSIGHT_VS_TAKEAWAY"
DESCRIPTION = (
    "key-insight callout contains a list (should be key-takeaway), "
    "or key-takeaway callout contains only one paragraph (should be key-insight)"
)

Issue = namedtuple("Issue", ["priority", "check_id", "filepath", "line", "message"])

# Find a <div class="callout key-insight"> or <div class="callout key-takeaway">.
# The class list may contain other tokens, so accept any order.
CALLOUT_OPEN_RE = re.compile(
    r'<div\s+class="(?P<classes>[^"]*\bcallout\b[^"]*)"', re.IGNORECASE
)

LIST_RE = re.compile(r'<(?:ul|ol)\b', re.IGNORECASE)
LI_RE = re.compile(r'<li\b', re.IGNORECASE)
P_RE = re.compile(r'<p\b', re.IGNORECASE)


def _line(html, pos):
    return html.count("\n", 0, pos) + 1


def _find_block_end(html, start_pos):
    """Find the matching </div> for the callout opened at start_pos.

    The opening <div ...> has already been consumed by the caller, so depth
    starts at 1 and we walk forward counting <div> and </div> tags.
    """
    depth = 1
    pos = start_pos
    tag_re = re.compile(r'<(/?)div\b', re.IGNORECASE)
    while pos < len(html) and depth > 0:
        m = tag_re.search(html, pos)
        if not m:
            return len(html)
        if m.group(1) == "/":
            depth -= 1
        else:
            depth += 1
        pos = m.end()
        if depth == 0:
            return pos
    return pos


def _has_class(classes, target):
    return target in classes.split()


def _count_paragraphs(block):
    return len(P_RE.findall(block))


def _has_list(block):
    return bool(LIST_RE.search(block))


def _count_list_items(block):
    return len(LI_RE.findall(block))


def run(filepath, html, context):
    issues = []
    if filepath.suffix != ".html":
        return issues

    for m in CALLOUT_OPEN_RE.finditer(html):
        classes = m.group("classes")
        if not (_has_class(classes, "key-insight") or _has_class(classes, "key-takeaway")):
            continue

        line = _line(html, m.start())
        # Find end of this opening tag, then end of the matching </div>.
        tag_close = html.find(">", m.end())
        if tag_close == -1:
            continue
        block_end = _find_block_end(html, tag_close + 1)
        # The block body excludes the opening <div ...> and the matching </div>.
        # We approximate by taking everything between them.
        block = html[tag_close + 1:block_end]

        if _has_class(classes, "key-insight"):
            # Misuse: list inside key-insight.
            if _has_list(block):
                n_items = _count_list_items(block)
                issues.append(Issue(
                    PRIORITY, CHECK_ID, filepath, line,
                    f'key-insight callout contains a list ({n_items} items); '
                    f'use key-takeaway for bulleted end-of-section recaps, '
                    f'or split the bullets into individual key-insight paragraphs'
                ))
        elif _has_class(classes, "key-takeaway"):
            # Misuse: only one <p> and no list.
            n_paragraphs = _count_paragraphs(block)
            if not _has_list(block) and n_paragraphs <= 1:
                issues.append(Issue(
                    PRIORITY, CHECK_ID, filepath, line,
                    f'key-takeaway callout has a single paragraph and no list; '
                    f'rewrite as a bulleted recap, or convert to key-insight '
                    f'if it captures one mental model'
                ))

    return issues
