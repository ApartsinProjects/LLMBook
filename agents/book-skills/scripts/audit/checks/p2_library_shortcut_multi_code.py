"""Detect library-shortcut callouts with multiple <div class="code-block-wrapper">.

A library-shortcut should be a single, focused 8-line snippet that shows
how to call ONE library. Multiple code blocks inside one shortcut signal
either:
  - Two related snippets that should be merged into one
  - A snippet + an output-collapse that book.js will double-wrap into
    a confusing "Show code" + "Show code (output)" nested toggle
  - Two genuinely different examples that belong in separate
    library-shortcut callouts

The audit flags these so the author can decide which fix applies.
"""
import re
from collections import namedtuple

PRIORITY = "P2"
CHECK_ID = "LIBRARY_SHORTCUT_MULTI_CODE"
DESCRIPTION = "library-shortcut callout contains more than one code-block-wrapper"

Issue = namedtuple("Issue", ["priority", "check_id", "filepath", "line", "message"])

OPEN_RE = re.compile(
    r'<div\s+class="callout\s+library-shortcut"[^>]*>', re.IGNORECASE
)


def _find_div_close(html: str, after_open: int) -> int:
    depth = 1
    pos = after_open
    tag_re = re.compile(r'<(/?)div\b', re.IGNORECASE)
    while pos < len(html) and depth > 0:
        m = tag_re.search(html, pos)
        if not m:
            return -1
        if m.group(1) == "/":
            depth -= 1
        else:
            depth += 1
        pos = m.end()
        if depth == 0:
            return m.start()
    return -1


def run(filepath, html, context):
    issues = []
    if filepath.suffix != ".html":
        return issues
    for m in OPEN_RE.finditer(html):
        body_start = m.end()
        body_end = _find_div_close(html, body_start)
        if body_end < 0:
            continue
        body = html[body_start:body_end]
        n_blocks = len(re.findall(
            r'<div\s+class="code-block-wrapper"', body, re.IGNORECASE
        ))
        if n_blocks <= 1:
            continue
        line = html.count("\n", 0, m.start()) + 1
        issues.append(Issue(
            PRIORITY, CHECK_ID, filepath, line,
            f'library-shortcut at line {line} contains {n_blocks} '
            f'code-block-wrappers; merge into one snippet, OR split into '
            f'separate library-shortcut callouts. Multiple blocks render '
            f'as a confusing "Show code (N blocks)" toggle.'
        ))
    return issues
